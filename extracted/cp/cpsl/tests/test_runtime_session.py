import os
import sys
import unittest
import json
import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cpsl.app import App
from cpsl.clients.capsule import (
    GetSessionResponse,
    InboundMessage,
    SaveSessionDataResponse,
    UploadFileResponse,
    WaitForApprovalResponse,
    WaitForIntegrationResponse,
)
from cpsl.db import reset_active_identity, set_active_identity
from cpsl.msg import Message
from cpsl.runner.session import RunnerSessionMixin
from cpsl.session import (
    Block,
    IntegrationTimeout,
    RequestContext,
    Session,
    SessionChannel,
    UserInfo,
    current_session,
    pipedream,
    session_data_base_checksum,
    session_data_checksum,
    session_data_revision,
    session_data_json,
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

    def test_request_context_pipedream_uses_gateway_context(self):
        stub = object()
        ctx = RequestContext(
            user=UserInfo(id="user-123", email="user@example.com", org_id="org-1"),
            integrations={},
            session_stub=stub,
            app_id="app-1",
            env="deploy",
        )

        transport = ctx.pipedream("microsoft_outlook")

        self.assertIs(transport._stub, stub)
        self.assertEqual(transport._app_id, "app-1")
        self.assertEqual(transport._user_email, "user@example.com")
        self.assertEqual(transport._owner_id, "org:org-1")
        self.assertEqual(transport._env, "deploy")
        self.assertEqual(transport._integration_type, "microsoft_outlook")

    def test_module_pipedream_supports_active_request_context(self):
        stub = object()
        ctx = RequestContext(
            user=UserInfo(id="user-123", email="user@example.com"),
            integrations={},
            session_stub=stub,
            app_id="app-1",
            env="serve",
        )
        token = set_active_identity(ctx)
        try:
            transport = pipedream("gmail")
        finally:
            reset_active_identity(token)

        self.assertIs(transport._stub, stub)
        self.assertEqual(transport._app_id, "app-1")
        self.assertEqual(transport._user_email, "user@example.com")
        self.assertEqual(transport._owner_id, "user-123")
        self.assertEqual(transport._env, "serve")
        self.assertEqual(transport._integration_type, "gmail")

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

    def test_session_data_json_handles_common_python_values(self):
        @dataclass
        class Payload:
            value: int

        class Opaque:
            def __reduce_ex__(self, protocol):
                raise AssertionError("__reduce__ should not be called")

            def __str__(self):
                return "opaque"

        encoded = session_data_json(
            {
                "dt": datetime(2026, 5, 10, tzinfo=timezone.utc),
                "payload": Payload(3),
                "bytes": b"hello",
                "opaque": Opaque(),
            }
        )

        decoded = json.loads(encoded)
        self.assertEqual(decoded["dt"], "2026-05-10T00:00:00+00:00")
        self.assertEqual(decoded["payload"], {"value": 3})
        self.assertEqual(decoded["bytes"], "hello")
        self.assertEqual(decoded["opaque"], "opaque")


class RuntimeSessionPersistenceTests(unittest.IsolatedAsyncioTestCase):
    class StubSessionService:
        def __init__(self):
            self.data_json = "{}"
            self.saved: list[dict] = []
            self.requests = []
            self.conflict_once = False
            self.raise_once = False
            self.reject_once = False

        def get_session(self, _req):
            return GetSessionResponse(
                session_id="sess-1",
                channel_type="chat",
                user_id="user-1",
                data_json=self.data_json,
            )

        def save_session_data(self, req):
            self.requests.append(req)
            if self.raise_once:
                self.raise_once = False
                raise RuntimeError("save failed")
            data = json.loads(req.data_json or "{}")
            expected_checksum = session_data_checksum(data)
            if req.checksum != expected_checksum:
                return SaveSessionDataResponse(ok=False, checksum=expected_checksum)
            if self.conflict_once:
                self.conflict_once = False
                current = {"server": "current", "remove": True, "__cpsl_session_rev": 5}
                current["__cpsl_session_checksum"] = session_data_checksum(current)
                self.data_json = json.dumps(current)
                return SaveSessionDataResponse(
                    ok=False,
                    conflict=True,
                    revision=5,
                    checksum=current["__cpsl_session_checksum"],
                    data_json=self.data_json,
                )
            if self.reject_once:
                self.reject_once = False
                return SaveSessionDataResponse(ok=False)
            current = json.loads(self.data_json or "{}")
            current_revision = session_data_revision(current)
            current_checksum = session_data_base_checksum(current)
            if req.base_revision != current_revision or req.base_checksum != current_checksum:
                return SaveSessionDataResponse(
                    ok=False,
                    conflict=True,
                    revision=current_revision,
                    checksum=current_checksum,
                    data_json=self.data_json or "{}",
                )
            revision = current_revision + 1
            checksum = session_data_checksum(data)
            data["__cpsl_session_rev"] = revision
            data["__cpsl_session_checksum"] = checksum
            if req.nonce:
                data["__cpsl_session_nonce"] = req.nonce
            self.data_json = json.dumps(data)
            self.saved.append(json.loads(req.data_json))
            return SaveSessionDataResponse(
                ok=True,
                revision=revision,
                checksum=checksum,
                data_json=self.data_json,
            )

    class StubRunner(RunnerSessionMixin):
        def __init__(self):
            self._sessions = {}
            self._session_locks = {}
            self._active_lock = asyncio.Lock()
            self._active_count = 0
            self._last_activity = 0.0
            self._keep_warm = 0
            self._session_stub = RuntimeSessionPersistenceTests.StubSessionService()
            self._runner_stub = None
            self._data_stub = None
            self._data_app_id = ""
            self._app_id = "app-1"
            self._version_type = "serve"
            self._stop_event = None
            self._hooks = {}
            self._session_handlers = {}
            self._action_handlers = {}
            self._message_handlers = {}
            self._workflows = {}
            self.submitted: list[tuple[str, bool]] = []
            self.widget_updates = 0
            self.session_data_snapshots: list[dict] = []

        async def _run_rpc(self, fn, *args):
            return fn(*args)

        def _submit(self, _request_id, text, done, session_id=None):
            self.submitted.append((text, done))

        async def _stream_chunks(self, *_args, **_kwargs):
            return None

        def _submit_block(self, *_args, **_kwargs):
            return None

        def _submit_widget_update(self, *_args, **_kwargs):
            self.widget_updates += 1

        def _submit_session_data_snapshot(self, _session_id, data_json):
            self.session_data_snapshots.append(json.loads(data_json))

    def inbound(
        self,
        *,
        action_name: str = "set_value",
        payload: dict | None = None,
        chat_name: str = "",
    ):
        return InboundMessage(
            request_id="req-1",
            session_id="sess-1",
            channel_type="chat",
            user_id="user-1",
            action_name=action_name,
            action_payload_json=json.dumps(payload or {}),
            chat_name=chat_name,
        )

    async def test_cached_session_rehydrates_from_durable_state_between_actions(self):
        runner = self.StubRunner()
        runner._session_stub.data_json = json.dumps({"value": "persisted"})

        session, is_new = await runner._get_session(self.inbound())
        self.assertTrue(is_new)
        self.assertEqual(session.data["value"], "persisted")

        session.data["value"] = "local"
        runner._session_stub.data_json = json.dumps({"value": "stale"})

        same_session, is_new = await runner._get_session(self.inbound())
        self.assertFalse(is_new)
        self.assertIs(same_session, session)
        self.assertEqual(same_session.data["value"], "stale")

    async def test_action_persists_before_handle_returns(self):
        runner = self.StubRunner()

        async def set_value(session, event):
            await session.data.set("value", event.payload["value"])

        runner._action_handlers["set_value"] = set_value

        await runner._handle(self.inbound(payload={"value": "handled"}))

        self.assertEqual(runner._session_stub.saved[-1]["value"], "handled")
        self.assertEqual(len(runner._session_stub.saved), 1)
        self.assertEqual(runner.widget_updates, 0)
        self.assertEqual(runner.session_data_snapshots[-1]["value"], "handled")
        self.assertIn(("", True), runner.submitted)

    async def test_minimal_state_repro_persists_and_rehydrates(self):
        runner = self.StubRunner()

        async def set_probe(session, event):
            await session.data.set("probe", event.payload["value"])

        runner._action_handlers["set_value"] = set_probe

        await runner._handle(self.inbound(payload={"value": "boring"}))

        req = runner._session_stub.requests[-1]
        self.assertEqual(json.loads(req.data_json), {"probe": "boring"})
        self.assertEqual(req.base_revision, 0)
        self.assertEqual(req.base_checksum, session_data_checksum({}))
        self.assertEqual(runner.session_data_snapshots[-1]["probe"], "boring")
        self.assertEqual(runner.session_data_snapshots[-1]["__cpsl_session_rev"], 1)

        runner._sessions.clear()
        session, _is_new = await runner._get_session(self.inbound())
        self.assertEqual(session.data["probe"], "boring")
        self.assertEqual(session.data["__cpsl_session_rev"], 1)

    async def test_first_save_uses_empty_server_base_despite_handler_metadata(self):
        runner = self.StubRunner()

        async def set_value(session, event):
            await session.data.set("value", event.payload["value"])

        runner._action_handlers["set_value"] = set_value

        await runner._handle(self.inbound(payload={"value": "handled"}, chat_name="chat"))

        req = runner._session_stub.requests[-1]
        self.assertEqual(req.base_revision, 0)
        self.assertEqual(req.base_checksum, session_data_checksum({}))
        self.assertEqual(runner._session_stub.saved[-1]["__chat_name__"], "chat")
        self.assertEqual(runner._session_stub.saved[-1]["value"], "handled")

    async def test_save_rejection_does_not_drop_dirty_state(self):
        runner = self.StubRunner()
        runner._session_stub.reject_once = True

        async def set_value(session, _event):
            await session.data.set("value", "eventually-persisted")

        runner._action_handlers["set_value"] = set_value

        await runner._handle(self.inbound())

        self.assertEqual(len(runner._session_stub.requests), 2)
        self.assertEqual(runner._session_stub.saved[-1]["value"], "eventually-persisted")
        self.assertEqual(runner.session_data_snapshots[-1]["value"], "eventually-persisted")

    async def test_save_exception_does_not_drop_dirty_state(self):
        runner = self.StubRunner()
        runner._session_stub.raise_once = True

        async def set_value(session, _event):
            await session.data.set("value", "after-error")

        runner._action_handlers["set_value"] = set_value

        await runner._handle(self.inbound())

        self.assertEqual(len(runner._session_stub.requests), 2)
        self.assertEqual(runner._session_stub.saved[-1]["value"], "after-error")

    async def test_multiple_session_data_sets_persist_once(self):
        runner = self.StubRunner()

        async def set_values(session, _event):
            await session.data.set("a", 1)
            await session.data.set("b", 2)
            await session.data.set("c", 3)

        runner._action_handlers["set_value"] = set_values

        await runner._handle(self.inbound())

        self.assertEqual(len(runner._session_stub.saved), 1)
        self.assertEqual(runner._session_stub.saved[-1]["a"], 1)
        self.assertEqual(runner._session_stub.saved[-1]["b"], 2)
        self.assertEqual(runner._session_stub.saved[-1]["c"], 3)
        self.assertEqual(runner.widget_updates, 0)
        self.assertEqual(len(runner.session_data_snapshots), 1)
        self.assertEqual(runner.session_data_snapshots[0]["c"], 3)

    async def test_persistence_sends_base_revision_and_checksum_from_hydrated_state(self):
        runner = self.StubRunner()
        hydrated = {"existing": True, "__cpsl_session_rev": 7}
        hydrated["__cpsl_session_checksum"] = session_data_checksum(hydrated)
        runner._session_stub.data_json = json.dumps(hydrated)

        async def set_value(session, _event):
            await session.data.set("value", "next")

        runner._action_handlers["set_value"] = set_value

        await runner._handle(self.inbound())

        req = runner._session_stub.requests[-1]
        self.assertEqual(req.base_revision, 7)
        self.assertEqual(req.base_checksum, hydrated["__cpsl_session_checksum"])
        self.assertTrue(req.nonce)
        self.assertEqual(req.checksum, session_data_checksum(json.loads(req.data_json)))

    async def test_conflict_response_rehydrates_and_retries_once(self):
        runner = self.StubRunner()
        runner._session_stub.conflict_once = True

        async def set_value(session, _event):
            await session.data.set("value", "client")

        runner._action_handlers["set_value"] = set_value

        await runner._handle(self.inbound())

        self.assertEqual(len(runner._session_stub.requests), 2)
        self.assertEqual(runner._session_stub.requests[1].base_revision, 5)
        self.assertEqual(runner._session_stub.saved[-1]["server"], "current")
        self.assertEqual(runner._session_stub.saved[-1]["value"], "client")
        self.assertEqual(runner._sessions["sess-1"].data["value"], "client")

    async def test_conflict_retry_preserves_intended_deletes(self):
        runner = self.StubRunner()
        hydrated = {"remove": True, "__cpsl_session_rev": 1}
        hydrated["__cpsl_session_checksum"] = session_data_checksum(hydrated)
        runner._session_stub.data_json = json.dumps(hydrated)
        runner._session_stub.conflict_once = True

        async def delete_value(session, _event):
            session.data.pop("remove")

        runner._action_handlers["set_value"] = delete_value

        await runner._handle(self.inbound())

        self.assertEqual(len(runner._session_stub.requests), 2)
        self.assertNotIn("remove", runner._session_stub.saved[-1])
        self.assertNotIn("remove", runner._sessions["sess-1"].data)

    async def test_publish_flushes_intermediate_snapshot(self):
        runner = self.StubRunner()

        async def publish_status(session, _event):
            await session.data.set("before", True)
            await session.publish("status", "drafting")
            await session.data.set("after", True)

        runner._action_handlers["set_value"] = publish_status

        await runner._handle(self.inbound())

        self.assertEqual(len(runner._session_stub.saved), 2)
        self.assertEqual(runner._session_stub.saved[0]["before"], True)
        self.assertEqual(runner._session_stub.saved[0]["status"], "drafting")
        self.assertNotIn("after", runner._session_stub.saved[0])
        self.assertEqual(runner._session_stub.saved[1]["after"], True)
        self.assertEqual(len(runner.session_data_snapshots), 2)
        self.assertNotIn("after", runner.session_data_snapshots[0])
        self.assertEqual(runner.session_data_snapshots[1]["after"], True)
        self.assertEqual(runner.widget_updates, 0)

    async def test_flush_data_without_changes_is_noop(self):
        runner = self.StubRunner()

        async def flush_clean(session, _event):
            await session.flush_data()

        runner._action_handlers["set_value"] = flush_clean

        await runner._handle(self.inbound())

        self.assertEqual(runner._session_stub.saved, [])

    async def test_internal_session_set_action_persists_data(self):
        runner = self.StubRunner()

        await runner._handle(
            self.inbound(
                action_name="__session_set__",
                payload={"key": "selected_id", "value": "row-1"},
            )
        )

        self.assertEqual(runner._sessions["sess-1"].data["selected_id"], "row-1")
        self.assertEqual(runner._session_stub.saved[-1]["selected_id"], "row-1")
        self.assertEqual(len(runner._session_stub.saved), 1)
        self.assertEqual(runner.widget_updates, 0)
        self.assertEqual(runner.session_data_snapshots[-1]["selected_id"], "row-1")


class SessionPromptTests(unittest.IsolatedAsyncioTestCase):
    def new_session(self) -> Session:
        return Session(
            id="sess-1",
            user=UserInfo(id="user-1", email="user@example.com"),
            channel=SessionChannel(type="chat"),
            history=[],
            data={},
        )

    async def test_terminal_shell_and_exec_emit_stable_terminal_block(self):
        session = self.new_session()
        blocks: list[str] = []

        async def block_cb(block_json: str):
            blocks.append(block_json)

        session._block_callback = block_cb
        term = await session.show_terminal(name="checks", title="Checks")

        shell_result = await term.shell("printf hello")
        exec_result = await term.exec(sys.executable, "-c", "print('ok')")

        self.assertEqual(shell_result.exit_code, 0)
        self.assertEqual(int(shell_result), 0)
        self.assertTrue(shell_result.ok)
        self.assertTrue(shell_result)
        self.assertEqual(shell_result.stdout, "hello")
        self.assertEqual(shell_result.stderr, "")
        self.assertEqual(exec_result.exit_code, 0)
        self.assertIn("ok", exec_result.stdout)
        self.assertGreaterEqual(len(blocks), 4)
        latest = json.loads(blocks[-1])
        self.assertEqual(latest["type"], "terminal")
        self.assertEqual(latest["id"], term.block_id)
        self.assertEqual(latest["payload"]["title"], "Checks")
        self.assertGreater(latest["payload"]["revision"], 0)
        self.assertEqual(len(latest["payload"]["runs"]), 2)
        self.assertEqual(latest["payload"]["runs"][0]["mode"], "shell")
        self.assertEqual(latest["payload"]["runs"][1]["mode"], "exec")
        output = "".join(
            chunk["text"] for run in latest["payload"]["runs"] for chunk in run["chunks"]
        )
        self.assertIn("hello", output)
        self.assertIn("ok", output)

    async def test_session_data_nested_append_emits_change_callback(self):
        session = self.new_session()
        calls = 0

        def changed():
            nonlocal calls
            calls += 1

        session._data_change_callback = changed
        session.data.setdefault("generated_media", [])
        session.data["generated_media"].append({"src": "https://example.com/a.png"})

        self.assertEqual(calls, 2)
        self.assertEqual(session.data["generated_media"][0]["src"], "https://example.com/a.png")

    async def test_session_data_set_works_with_preloaded_state(self):
        session = Session(
            id="sess-preloaded",
            user=UserInfo(id="user-1"),
            channel=SessionChannel(type="chat"),
            history=[],
            data={"existing": {"value": 1}},
        )
        calls = 0

        async def changed():
            nonlocal calls
            calls += 1

        session._data_change_callback = changed
        await session.data.set("next", {"ok": True})

        self.assertEqual(calls, 1)
        self.assertEqual(session.data["next"]["ok"], True)

    async def test_session_media_helpers_return_gallery_items(self):
        session = self.new_session()
        uploads: list[tuple[str, str]] = []

        class StubRunnerService:
            def upload_file(self, req):
                uploads.append((req.filename, req.content_type))
                return UploadFileResponse(url=f"https://files.example/{req.filename}")

        session._runner_stub = StubRunnerService()
        session._app_id = "app-1"

        image = await session.media.image(
            b"fake-image",
            filename="image.png",
            mime_type="image/png",
            caption="A",
        )
        video = await session.media.video(
            "https://cdn.example/video.mp4",
            poster=b"poster",
            caption="V",
        )

        self.assertEqual(image["type"], "image")
        self.assertEqual(image["src"], "https://files.example/image.png")
        self.assertEqual(image["download_url"], image["src"])
        self.assertEqual(image["caption"], "A")
        self.assertEqual(video["type"], "video")
        self.assertEqual(video["src"], "https://cdn.example/video.mp4")
        self.assertEqual(video["poster"], "https://files.example/poster")
        self.assertIn(("image.png", "image/png"), uploads)

    async def test_terminal_handle_does_not_render_until_shown(self):
        session = self.new_session()
        blocks: list[str] = []

        async def block_cb(block_json: str):
            blocks.append(block_json)

        session._block_callback = block_cb
        term = session.terminal("checks")

        result = await term.shell("printf hidden")

        self.assertEqual(result.stdout, "hidden")
        self.assertEqual(blocks, [])

        await session.show_terminal(terminal=term, title="Checks")

        latest = json.loads(blocks[-1])
        self.assertEqual(latest["payload"]["title"], "Checks")
        self.assertEqual(len(latest["payload"]["runs"]), 1)

    async def test_terminal_result_captures_stderr_and_nonzero_exit(self):
        session = self.new_session()

        async def block_cb(_block_json: str):
            return None

        session._block_callback = block_cb
        term = session.terminal("checks", title="Checks")

        result = await term.exec(
            sys.executable,
            "-c",
            "import sys; print('bad', file=sys.stderr); raise SystemExit(7)",
        )

        self.assertEqual(result.exit_code, 7)
        self.assertFalse(result.ok)
        self.assertFalse(result)
        self.assertEqual(result.stdout, "")
        self.assertIn("bad", result.stderr)

    async def test_terminal_handle_reopens_from_history(self):
        session = self.new_session()
        block_id = "term_" + __import__("hashlib").sha1(b"sess-1:checks").hexdigest()[:16]
        session.history.append(
            Message(
                text=json.dumps(
                    {
                        "id": block_id,
                        "type": "terminal",
                        "payload": {
                            "title": "Checks",
                            "revision": 12,
                            "runs": [
                                {
                                    "id": "run_existing",
                                    "mode": "shell",
                                    "command": "echo old",
                                    "status": "completed",
                                    "chunks": [{"stream": "stdout", "text": "old\n", "seq": 0}],
                                }
                            ],
                        },
                    }
                ),
                sender="block",
                channel_type="chat",
            )
        )
        blocks: list[str] = []

        async def block_cb(block_json: str):
            blocks.append(block_json)

        session._block_callback = block_cb
        term = session.terminal("checks", title="Checks")
        await term.shell("printf new")

        latest = json.loads(blocks[-1])
        self.assertEqual(latest["id"], block_id)
        self.assertGreater(latest["payload"]["revision"], 12)
        self.assertEqual(len(latest["payload"]["runs"]), 2)
        self.assertEqual(latest["payload"]["runs"][0]["id"], "run_existing")

    async def test_show_terminal_can_render_existing_handle(self):
        session = self.new_session()
        blocks: list[str] = []

        async def block_cb(block_json: str):
            blocks.append(block_json)

        session._block_callback = block_cb
        term = session.terminal("diagnostics")
        await term.shell("printf ok")

        self.assertEqual(blocks, [])

        shown = await session.show_terminal(terminal=term, title="Diagnostics")

        self.assertIs(shown, term)
        latest = json.loads(blocks[-1])
        self.assertEqual(latest["id"], term.block_id)
        self.assertEqual(latest["payload"]["title"], "Diagnostics")
        self.assertEqual(len(latest["payload"]["runs"]), 1)

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
                payload={
                    "type": "gmail",
                    "reason": "Connect Gmail to draft replies.",
                    "blocking": True,
                },
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
