import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cpsl.app import App
from cpsl.clients.capsule import (
    WaitForApprovalResponse,
    WaitForIntegrationResponse,
)
from cpsl.db import reset_active_identity, set_active_identity
from cpsl.msg import Message
from cpsl.session import (
    Block,
    IntegrationTimeout,
    RequestContext,
    Session,
    SessionChannel,
    UserInfo,
    current_session,
)
from cpsl.task_types import TaskDescriptor
from cpsl.image import Image


class RuntimeSessionTests(unittest.TestCase):
    def test_current_session_returns_active_session(self):
        session = Session(
            id="",
            user=UserInfo(id="owner-123", org_id="org_123"),
            channel=SessionChannel(type="chat"),
            history=[],
            data={},
        )
        token = set_active_identity(session)
        try:
            self.assertIs(current_session(), session)
        finally:
            reset_active_identity(token)

    def test_current_session_ignores_non_session_identity(self):
        ctx = RequestContext(user=UserInfo(id="user-123"), integrations={})
        token = set_active_identity(ctx)
        try:
            self.assertIsNone(current_session())
        finally:
            reset_active_identity(token)

    def test_task_descriptor_detects_session_parameter_anywhere(self):
        async def with_session(session, value):
            return value

        async def with_trailing_session(value, session=None):
            return value

        async def without_session(value):
            return value

        class Example:
            async def method_with_session(self, session, value):
                return value

            async def method_with_trailing_session(self, value, session=None):
                return value

            async def method_without_session(self, value):
                return value

        self.assertTrue(TaskDescriptor(with_session)._wants_session)
        self.assertTrue(TaskDescriptor(with_trailing_session)._wants_session)
        self.assertFalse(TaskDescriptor(without_session)._wants_session)
        self.assertTrue(TaskDescriptor(Example.method_with_session)._wants_session)
        self.assertTrue(TaskDescriptor(Example.method_with_trailing_session)._wants_session)
        self.assertFalse(TaskDescriptor(Example.method_without_session)._wants_session)

    def test_functional_app_finalize_exposes_collection_refs_for_subprocess_tasks(self):
        app = App(
            name="finalize-collection-test",
            image=Image(),
        )
        ref = app.collection("activity_log", scope="user")

        @app.task()
        async def work(session=None):
            return None

        app._finalize_config()

        self.assertIn(ref, app._cpsl_config["collection_refs"])


class SessionPromptTests(unittest.IsolatedAsyncioTestCase):
    def new_session(self) -> Session:
        return Session(
            id="sess-1",
            user=UserInfo(id="user-1", email="user@example.com"),
            channel=SessionChannel(type="chat"),
            history=[],
            data={},
        )

    async def test_prompt_approval_returns_true_and_marks_completed(self):
        session = self.new_session()
        replies: list[str] = []
        blocks: list[str] = []

        class StubSessionService:
            def wait_for_approval(self, _req):
                return WaitForApprovalResponse(approved=True)

        async def reply_cb(msg: Message):
            replies.append(msg.text)

        async def block_cb(block_json: str):
            blocks.append(block_json)

        session._session_stub = StubSessionService()
        session._reply_callback = reply_cb
        session._block_callback = block_cb

        approved = await session.prompt_approval("Send these drafts?")

        self.assertTrue(approved)
        # The prompt headline now lives inside the block, not as a separate reply.
        self.assertEqual(replies, [])
        self.assertEqual(len(blocks), 2)
        self.assertIn('"approval_prompt"', blocks[0])
        self.assertIn('"message": "Send these drafts?"', blocks[0])
        self.assertIn('"completed": true', blocks[1])
        self.assertIn('"approved": true', blocks[1])
        self.assertIn('"message": "Send these drafts?"', blocks[1])

    async def test_prompt_integration_persists_reason_as_reply(self):
        session = self.new_session()
        replies: list[str] = []
        blocks: list[str] = []

        class StubSessionService:
            def wait_for_integration(self, _req):
                return WaitForIntegrationResponse(timed_out=True)

        async def reply_cb(msg: Message):
            replies.append(msg.text)

        async def block_cb(block_json: str):
            blocks.append(block_json)

        session._app_id = "app-1"
        session._session_stub = StubSessionService()
        session._reply_callback = reply_cb
        session._block_callback = block_cb

        with self.assertRaises(IntegrationTimeout):
            await session.prompt_integration("gmail", reason="Connect Gmail to draft replies.")

        self.assertEqual(replies, ["Connect Gmail to draft replies."])
        self.assertEqual(len(blocks), 1)
        self.assertIn('"integration_prompt"', blocks[0])
        self.assertIn('"reason": ""', blocks[0])

    async def test_external_file_prompt_emits_text_fallback(self):
        session = Session(
            id="sess-telegram",
            user=UserInfo(id="user-1", email="user@example.com"),
            channel=SessionChannel(type="telegram"),
            history=[],
            data={},
        )
        notifies: list[str] = []
        blocks: list[str] = []

        async def notify_cb(msg: Message):
            notifies.append(msg.text)

        async def block_cb(block_json: str):
            blocks.append(block_json)

        session._notify_callback = notify_cb
        session._block_callback = block_cb

        await session.show(
            Block(
                type="file_upload",
                payload={"message": "Please upload the receipt.", "blocking": True},
            )
        )

        self.assertEqual(len(blocks), 1)
        self.assertIn("Please upload the receipt.", notifies[0])
        self.assertIn("send the file here as your next message", notifies[0])

    async def test_chat_file_prompt_does_not_emit_text_fallback(self):
        session = self.new_session()
        notifies: list[str] = []
        blocks: list[str] = []

        async def notify_cb(msg: Message):
            notifies.append(msg.text)

        async def block_cb(block_json: str):
            blocks.append(block_json)

        session._notify_callback = notify_cb
        session._block_callback = block_cb

        await session.show(Block(type="file_upload", payload={"message": "Upload it"}))

        self.assertEqual(notifies, [])
        self.assertEqual(len(blocks), 1)

    async def test_external_integration_prompt_emits_text_fallback(self):
        session = Session(
            id="sess-telegram",
            user=UserInfo(id="user-1", email="user@example.com"),
            channel=SessionChannel(type="telegram"),
            history=[],
            data={},
        )
        notifies: list[str] = []

        async def notify_cb(msg: Message):
            notifies.append(msg.text)

        async def block_cb(_block_json: str):
            pass

        session._notify_callback = notify_cb
        session._block_callback = block_cb

        await session.show(
            Block(
                type="integration_prompt",
                payload={"type": "gmail", "reason": "Connect Gmail to draft replies.", "blocking": True},
            )
        )

        self.assertIn("Connect Gmail to draft replies.", notifies[0])
        self.assertIn("Open the web app", notifies[0])


class ShowStepTests(unittest.IsolatedAsyncioTestCase):
    def new_session(self) -> Session:
        return Session(
            id="sess-step",
            user=UserInfo(id="user-1"),
            channel=SessionChannel(type="chat"),
            history=[],
            data={},
        )

    async def test_show_step_emits_block_with_stable_id(self):
        import json as _json

        session = self.new_session()
        blocks: list[dict] = []

        async def block_cb(block_json: str):
            blocks.append(_json.loads(block_json))

        session._block_callback = block_cb

        sid = await session.show_step("Research ICP")
        sid2 = await session.show_step(
            "Research ICP", status="completed", detail="Found 18 accounts"
        )

        self.assertEqual(sid, "research_icp")
        self.assertEqual(sid, sid2)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0]["type"], "step_status")
        self.assertEqual(blocks[0]["id"], "step_research_icp")
        self.assertEqual(blocks[0]["payload"]["status"], "running")
        self.assertEqual(blocks[1]["id"], "step_research_icp")
        self.assertEqual(blocks[1]["payload"]["status"], "completed")
        self.assertEqual(blocks[1]["payload"]["detail"], "Found 18 accounts")

    async def test_show_step_respects_explicit_step_id(self):
        import json as _json

        session = self.new_session()
        blocks: list[dict] = []

        async def block_cb(block_json: str):
            blocks.append(_json.loads(block_json))

        session._block_callback = block_cb

        sid = await session.show_step("Anything", step_id="custom-id")
        self.assertEqual(sid, "custom-id")
        self.assertEqual(blocks[0]["id"], "step_custom-id")
        self.assertEqual(blocks[0]["payload"]["step_id"], "custom-id")


class NotifyTests(unittest.IsolatedAsyncioTestCase):
    def new_session(self) -> Session:
        return Session(
            id="sess-notify",
            user=UserInfo(id="u-1"),
            channel=SessionChannel(type="chat"),
            history=[],
            data={},
        )

    async def test_notify_emits_notification_block_not_reply(self):
        import json as _json

        session = self.new_session()
        replies: list[str] = []
        blocks: list[dict] = []

        async def reply_cb(msg: Message):
            replies.append(msg.text)

        async def block_cb(block_json: str):
            blocks.append(_json.loads(block_json))

        session._reply_callback = reply_cb
        session._block_callback = block_cb

        await session.notify("Thinking...")

        # Notify must NOT pollute the assistant bubble via reply_callback.
        self.assertEqual(replies, [])
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["type"], "notification")
        self.assertEqual(blocks[0]["payload"]["text"], "Thinking...")
        # Stable per-session id so subsequent notifies replace, not stack.
        self.assertEqual(blocks[0]["id"], "notify_sess-notify")

    async def test_notify_uses_explicit_callback_when_provided(self):
        session = self.new_session()
        notifies: list[str] = []
        blocks: list[dict] = []

        async def notify_cb(msg: Message):
            notifies.append(msg.text)

        async def block_cb(block_json: str):
            blocks.append(block_json)

        session._notify_callback = notify_cb
        session._block_callback = block_cb

        await session.notify("Loading data")
        self.assertEqual(notifies, ["Loading data"])
        self.assertEqual(blocks, [])

    async def test_notify_with_detail_is_passed_through(self):
        import json as _json

        session = self.new_session()
        blocks: list[dict] = []

        async def block_cb(block_json: str):
            blocks.append(_json.loads(block_json))

        session._block_callback = block_cb

        await session.notify("Crawling pages", detail="visited 12 / 50\nlast: example.com/team")
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["payload"]["text"], "Crawling pages")
        self.assertEqual(
            blocks[0]["payload"]["detail"],
            "visited 12 / 50\nlast: example.com/team",
        )


if __name__ == "__main__":
    unittest.main()
