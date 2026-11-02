import asyncio
import time
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest

from edison_client.clients.chat_methods import ChatError, ChatFetchError, ChatMethods
from edison_client.clients.rest_client import RestClient
from edison_client.models.chat import (
    ChatConversationList,
    ChatMessageResponse,
    ConversationDetail,
    ConversationMessage,
    QueueMessageResponse,
)

# Chat agents are hidden from /v0.1/crows submissions, so the live chat tests
# use a dedicated chat-only dummy crow instead of the submit-capable dummy job.
CHAT_JOB_NAME = "job-futurehouse-dummy-env-chat"
TEST_TIMEOUT = 300  # seconds before pytest kills a test
WAIT_FOR_ASSISTANT_RESPONSE_TIME = 180  # seconds to poll for assistant reply
POLL_INTERVAL = 3  # seconds between polls
RETRY_ATTEMPTS = 3

# Seconds to wait for a newly-sent chat message to become visible in
# /v0.1/conversations. Sized to cover a cold-start chat sandbox dispatch:
# /chat returns 202 immediately and backgrounds provisioning, but the message
# only appears in ConversationsDB after the sandbox pod starts and consumes
# the pending message. During warmpool rotations or bursts this can take
# longer than a minute; shorter windows (e.g. 30s) cause the fixture teardown
# to delete the project before dispatch completes, producing FK violations.
WAIT_FOR_CONVERSATION_VISIBLE_TIME = 180


@pytest.fixture(name="chat_project_id")
def fixture_chat_project_id(admin_client: RestClient) -> Generator[UUID, None, None]:
    """Create a fresh project for chat tests, clean up afterwards."""
    project_id = admin_client.create_project(f"chat-e2e-{uuid4()}")
    workspace_id = admin_client.create_workspace(
        name=f"chat-e2e-ws-{uuid4()}", project_id=project_id
    ).data_storage.id
    yield project_id
    admin_client.delete_workspace(workspace_id)
    admin_client.delete_project(project_id)


class TestConversationDetailMultimodal:
    """ConversationDetail must accept multimodal content from the server."""

    def test_multimodal_content_validates(self):
        """Server returns content as list of blocks for multimodal messages."""
        created_at = "2026-01-01T00:00:00+00:00"
        raw = {
            "session_id": "b4a7c59a-f274-4e32-8bd5-06c2ea61873a",
            "messages": [
                {"role": "user", "content": "plain text", "created_at": created_at},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": "data:image/png;base64,abc"},
                        },
                        {"type": "text", "text": "See images below."},
                    ],
                    "created_at": created_at,
                },
                {
                    "role": "assistant",
                    "content": "I can see the image.",
                    "created_at": created_at,
                },
            ],
        }
        detail = ConversationDetail.model_validate(raw)
        assert isinstance(detail.messages[0].content, str)
        assert isinstance(detail.messages[1].content, list)
        assert detail.messages[1].content[0]["type"] == "image_url"
        assert isinstance(detail.messages[2].content, str)

    def test_conversation_message_accepts_string(self):
        msg = ConversationMessage.model_validate({
            "role": "user",
            "content": "hello",
            "created_at": "2026-01-01T00:00:00+00:00",
        })
        assert msg.content == "hello"

    def test_conversation_message_accepts_content_blocks(self):
        msg = ConversationMessage.model_validate({
            "role": "user",
            "content": [{"type": "text", "text": "See images below."}],
            "created_at": "2026-01-01T00:00:00+00:00",
        })
        assert isinstance(msg.content, list)
        assert len(msg.content) == 1


def _conversation_response(payload: dict) -> MagicMock:
    # The server stamps created_at on every stored row, so the stub does too.
    for message in payload.get("messages", []):
        message.setdefault("created_at", "2026-01-01T00:00:00+00:00")
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = payload
    return response


class _ChatMethodsStub(ChatMethods):
    def __init__(self, *responses: dict):
        mocked_responses = [_conversation_response(payload) for payload in responses]
        self._client = MagicMock()
        self._client.get.side_effect = mocked_responses
        self._async_client = MagicMock()
        self._async_client.get = AsyncMock(side_effect=mocked_responses)

    @property
    def client(self):
        return self._client

    @property
    def async_client(self):
        return self._async_client


class TestConversationPagination:
    @pytest.mark.parametrize("mode", ["sync", "async"])
    @pytest.mark.asyncio
    async def test_limit_none_fetches_all_message_pages(self, mode: str):
        session_id = uuid4()
        methods = _ChatMethodsStub(
            {
                "session_id": str(session_id),
                "messages": [
                    {"role": "user", "content": "three"},
                    {"role": "assistant", "content": "four"},
                ],
                "has_more": True,
                "continuation_cursor": None,
            },
            {
                "session_id": str(session_id),
                "messages": [
                    {"role": "user", "content": "one"},
                    {"role": "assistant", "content": "two"},
                ],
                "has_more": False,
                "continuation_cursor": None,
            },
        )

        if mode == "async":
            detail = await methods.aget_conversation(session_id, limit=None)
            client = methods.async_client
        else:
            detail = methods.get_conversation(session_id, limit=None)
            client = methods.client

        assert [message.content for message in detail.messages] == [
            "one",
            "two",
            "three",
            "four",
        ]
        # Fetch-all pages at the endpoint's limit cap; offset advances by
        # messages actually received, which may be fewer than requested.
        assert client.get.call_args_list[0].kwargs["params"] == {"limit": 1000}
        assert client.get.call_args_list[1].kwargs["params"] == {
            "limit": 1000,
            "offset": 2,
        }

    @pytest.mark.parametrize("mode", ["sync", "async"])
    @pytest.mark.asyncio
    async def test_fetch_reassembles_content_continuation(self, mode: str):
        session_id = uuid4()
        message_id = uuid4()
        older_block = {"type": "text", "text": "older"}
        newer_block = {"type": "text", "text": "newer"}
        methods = _ChatMethodsStub(
            {
                "session_id": str(session_id),
                "messages": [
                    {
                        "role": "tool",
                        "content": [newer_block],
                        "message_id": str(message_id),
                        "tool_call_id": "tool-1",
                        "name": "run_cell",
                        "content_block_start": 1,
                        "content_block_end": 2,
                        "content_block_total": 2,
                    }
                ],
                "has_more": True,
                "continuation_cursor": {
                    "message_id": str(message_id),
                    "block_index": 1,
                },
            },
            {
                "session_id": str(session_id),
                "messages": [
                    {
                        "role": "tool",
                        "content": [older_block],
                        "message_id": str(message_id),
                        "tool_call_id": "tool-1",
                        "name": "run_cell",
                        "content_block_start": 0,
                        "content_block_end": 1,
                        "content_block_total": 2,
                    }
                ],
                "has_more": False,
                "continuation_cursor": None,
            },
        )

        if mode == "async":
            detail = await methods.aget_conversation(session_id)
            client = methods.async_client
        else:
            detail = methods.get_conversation(session_id)
            client = methods.client

        assert detail.messages[0].content == [older_block, newer_block]
        assert detail.has_more is True
        params = client.get.call_args_list[1].kwargs["params"]
        assert params == {
            "continuation_message_id": str(message_id),
            "continuation_block_index": 1,
        }

    def test_fetch_all_completes_continuation_before_loading_next_page(self):
        session_id = uuid4()
        message_id = uuid4()
        older_block = {"type": "text", "text": "older"}
        newer_block = {"type": "text", "text": "newer"}
        methods = _ChatMethodsStub(
            {
                "session_id": str(session_id),
                "messages": [
                    {
                        "role": "user",
                        "content": [newer_block],
                        "message_id": str(message_id),
                        "content_block_start": 1,
                        "content_block_end": 2,
                        "content_block_total": 2,
                    }
                ],
                "has_more": True,
                "continuation_cursor": {
                    "message_id": str(message_id),
                    "block_index": 1,
                },
            },
            {
                "session_id": str(session_id),
                "messages": [
                    {
                        "role": "user",
                        "content": [older_block],
                        "message_id": str(message_id),
                        "content_block_start": 0,
                        "content_block_end": 1,
                        "content_block_total": 2,
                    }
                ],
                "has_more": True,
                "continuation_cursor": None,
            },
            {
                "session_id": str(session_id),
                "messages": [{"role": "assistant", "content": "oldest"}],
                "has_more": False,
                "continuation_cursor": None,
            },
        )

        detail = methods.get_conversation(session_id, limit=None)

        assert [message.content for message in detail.messages] == [
            "oldest",
            [older_block, newer_block],
        ]
        assert [
            call.kwargs["params"] for call in methods.client.get.call_args_list
        ] == [
            {"limit": 1000},
            {
                "continuation_message_id": str(message_id),
                "continuation_block_index": 1,
            },
            {"limit": 1000, "offset": 1},
        ]

    def test_fetch_all_preserves_has_more_across_continuation(self):
        session_id = uuid4()
        message_id = uuid4()
        older_block = {"type": "text", "text": "older"}
        newer_block = {"type": "text", "text": "newer"}
        methods = _ChatMethodsStub(
            {
                "session_id": str(session_id),
                "messages": [
                    {
                        "role": "user",
                        "content": [newer_block],
                        "message_id": str(message_id),
                        "content_block_start": 1,
                        "content_block_end": 2,
                        "content_block_total": 2,
                    }
                ],
                "has_more": True,
                "continuation_cursor": {
                    "message_id": str(message_id),
                    "block_index": 1,
                },
            },
            {
                "session_id": str(session_id),
                "messages": [
                    {
                        "role": "user",
                        "content": [older_block],
                        "message_id": str(message_id),
                        "content_block_start": 0,
                        "content_block_end": 1,
                        "content_block_total": 2,
                    }
                ],
                "has_more": False,
                "continuation_cursor": None,
            },
            {
                "session_id": str(session_id),
                "messages": [{"role": "assistant", "content": "oldest"}],
                "has_more": False,
                "continuation_cursor": None,
            },
        )

        detail = methods.get_conversation(session_id, limit=None)

        assert [message.content for message in detail.messages] == [
            "oldest",
            [older_block, newer_block],
        ]
        assert methods.client.get.call_count == 3


class TestSyncChatLifecycle:
    """Sync e2e: send_chat_message → get_conversations → get_conversation → store_conversation_message."""

    @pytest.mark.live_agent
    @pytest.mark.timeout(TEST_TIMEOUT)
    @pytest.mark.flaky(reruns=RETRY_ATTEMPTS)
    def test_e2e_sync_chat_flow(self, admin_client: RestClient, chat_project_id: UUID):
        """Full sync lifecycle against the real API."""
        # 1. Send a chat message — creates a new session
        send_result = admin_client.send_chat_message(
            project_id=chat_project_id,
            message="Hello from sync e2e test",
            job_name=CHAT_JOB_NAME,
        )
        assert isinstance(send_result, ChatMessageResponse)
        assert send_result.session_id is not None
        session_id = send_result.session_id

        # 2. List conversations — the session we just created should appear
        #    Poll because the conversation isn't visible until the sandbox
        #    consumes the pending message; see WAIT_FOR_CONVERSATION_VISIBLE_TIME.
        matching: list = []
        for _ in range(WAIT_FOR_CONVERSATION_VISIBLE_TIME):
            convos = admin_client.get_conversations(session_id=session_id)
            assert isinstance(convos, ChatConversationList)
            matching = [c for c in convos.conversations if c.session_id == session_id]
            if matching:
                break
            time.sleep(1)
        assert len(matching) == 1

        # 3. Get conversation detail — poll until assistant reply arrives
        detail = admin_client.get_conversation(session_id)
        assert isinstance(detail, ConversationDetail)
        assert detail.session_id == session_id
        assert len(detail.messages) >= 1
        first_msg = detail.messages[0]
        assert first_msg.role == "user"
        assert "Hello from sync e2e test" in first_msg.content

        assistant_msg = None
        for _ in range(WAIT_FOR_ASSISTANT_RESPONSE_TIME // POLL_INTERVAL):
            detail = admin_client.get_conversation(session_id)
            assistant_msgs = [m for m in detail.messages if m.role == "assistant"]
            if assistant_msgs:
                assistant_msg = assistant_msgs[0]
                break
            time.sleep(POLL_INTERVAL)
        assert assistant_msg is not None, "Assistant never replied"

        # 4. Store an additional message into the conversation
        admin_client.store_conversation_message(
            session_id=session_id,
            message={"role": "user", "content": "Follow-up from sync e2e"},
        )

        # 5. Verify the stored message appears in conversation detail
        detail_after = admin_client.get_conversation(session_id)
        assert len(detail_after.messages) > len(detail.messages)

    @pytest.mark.live_agent
    @pytest.mark.timeout(TEST_TIMEOUT)
    @pytest.mark.flaky(reruns=RETRY_ATTEMPTS)
    def test_send_chat_message_follow_up(
        self, admin_client: RestClient, chat_project_id: UUID
    ):
        """Send a follow-up message to an existing session (sync)."""
        # Create session
        first = admin_client.send_chat_message(
            project_id=chat_project_id,
            message="First message",
            job_name=CHAT_JOB_NAME,
        )
        session_id = first.session_id

        # Follow-up on same session
        second = admin_client.send_chat_message(
            project_id=chat_project_id,
            message="Second message",
            session_id=session_id,
            job_name=CHAT_JOB_NAME,
        )
        assert second.session_id == session_id

    def test_send_chat_message_bad_project(self, admin_client: RestClient):
        """Sending a message with a non-existent project_id returns 404."""
        fake_project_id = uuid4()
        with pytest.raises(
            ChatError,
            match=r"404.*project_not_found_or_unauthorized",
        ):
            admin_client.send_chat_message(
                project_id=fake_project_id,
                message="Should fail",
            )

    def test_get_conversations_empty(self, admin_client: RestClient):
        """Listing conversations with no filter returns without error."""
        convos = admin_client.get_conversations(limit=5)
        assert isinstance(convos, ChatConversationList)
        assert isinstance(convos.conversations, list)

    def test_get_conversation_not_found(self, admin_client: RestClient):
        """Fetching a non-existent session returns 404."""
        with pytest.raises(ChatFetchError, match="404") as exc_info:
            admin_client.get_conversation(uuid4())
        assert "not found" in str(exc_info.value).lower()

    def test_store_message_bad_session(self, admin_client: RestClient):
        """Storing a message to a non-existent session returns 404."""
        with pytest.raises(ChatError, match="404") as exc_info:
            admin_client.store_conversation_message(
                session_id=uuid4(),
                message={"role": "user", "content": "orphan"},
            )
        assert "not found" in str(exc_info.value).lower()

    def test_queue_chat_message_bad_project(self, admin_client: RestClient):
        """Queueing a message with a non-existent project_id returns 404."""
        with pytest.raises(ChatError, match="404") as exc_info:
            admin_client.queue_chat_message(
                session_id=uuid4(),
                project_id=uuid4(),
                message="Should fail",
            )
        assert "not found" in str(exc_info.value).lower()

    @pytest.mark.live_agent
    @pytest.mark.timeout(TEST_TIMEOUT)
    @pytest.mark.flaky(reruns=RETRY_ATTEMPTS)
    def test_queue_chat_message(self, admin_client: RestClient, chat_project_id: UUID):
        """Queue a message into a running chat session (sync)."""
        send_result = admin_client.send_chat_message(
            project_id=chat_project_id,
            message="Setting up for queue test",
            job_name=CHAT_JOB_NAME,
        )
        session_id = send_result.session_id

        result = admin_client.queue_chat_message(
            session_id=session_id,
            project_id=chat_project_id,
            message="Injected via queue",
        )
        assert isinstance(result, QueueMessageResponse)
        assert result.id is not None
        assert result.target_id == session_id


class TestAsyncChatLifecycle:
    """Async e2e: asend_chat_message → aget_conversations → aget_conversation → astore_conversation_message."""

    @pytest.mark.live_agent
    @pytest.mark.timeout(TEST_TIMEOUT)
    @pytest.mark.flaky(reruns=RETRY_ATTEMPTS)
    @pytest.mark.asyncio
    async def test_e2e_async_chat_flow(
        self, admin_client: RestClient, chat_project_id: UUID
    ):
        """Full async lifecycle against the real API."""
        # 1. Send a chat message — creates a new session
        send_result = await admin_client.asend_chat_message(
            project_id=chat_project_id,
            message="Hello from async e2e test",
            job_name=CHAT_JOB_NAME,
        )
        assert isinstance(send_result, ChatMessageResponse)
        assert send_result.session_id is not None
        session_id = send_result.session_id

        # 2. List conversations
        #    Poll because the conversation isn't visible until the sandbox
        #    consumes the pending message; see WAIT_FOR_CONVERSATION_VISIBLE_TIME.
        matching: list = []
        for _ in range(WAIT_FOR_CONVERSATION_VISIBLE_TIME):
            convos = await admin_client.aget_conversations(session_id=session_id)
            assert isinstance(convos, ChatConversationList)
            matching = [c for c in convos.conversations if c.session_id == session_id]
            if matching:
                break
            await asyncio.sleep(1)
        assert len(matching) == 1

        # 3. Get conversation detail — poll until assistant reply arrives
        detail = await admin_client.aget_conversation(session_id)
        assert isinstance(detail, ConversationDetail)
        assert detail.session_id == session_id
        assert len(detail.messages) >= 1
        first_msg = detail.messages[0]
        assert first_msg.role == "user"
        assert "Hello from async e2e test" in first_msg.content

        assistant_msg = None
        for _ in range(WAIT_FOR_ASSISTANT_RESPONSE_TIME // POLL_INTERVAL):
            detail = await admin_client.aget_conversation(session_id)
            assistant_msgs = [m for m in detail.messages if m.role == "assistant"]
            if assistant_msgs:
                assistant_msg = assistant_msgs[0]
                break
            await asyncio.sleep(POLL_INTERVAL)
        assert assistant_msg is not None, "Assistant never replied"

        # 4. Store an additional message
        await admin_client.astore_conversation_message(
            session_id=session_id,
            message={"role": "user", "content": "Follow-up from async e2e"},
        )

        # 5. Verify the stored message appears
        detail_after = await admin_client.aget_conversation(session_id)
        assert len(detail_after.messages) > len(detail.messages)

    @pytest.mark.live_agent
    @pytest.mark.timeout(TEST_TIMEOUT)
    @pytest.mark.flaky(reruns=RETRY_ATTEMPTS)
    @pytest.mark.asyncio
    async def test_asend_chat_message_follow_up(
        self, admin_client: RestClient, chat_project_id: UUID
    ):
        """Send a follow-up message to an existing session (async)."""
        first = await admin_client.asend_chat_message(
            project_id=chat_project_id,
            message="First async message",
            job_name=CHAT_JOB_NAME,
        )
        session_id = first.session_id

        second = await admin_client.asend_chat_message(
            project_id=chat_project_id,
            message="Second async message",
            session_id=session_id,
            job_name=CHAT_JOB_NAME,
        )
        assert second.session_id == session_id

    @pytest.mark.asyncio
    async def test_asend_chat_message_bad_project(self, admin_client: RestClient):
        """Sending a message with a non-existent project_id returns 404 (async)."""
        with pytest.raises(
            ChatError,
            match=r"404.*project_not_found_or_unauthorized",
        ):
            await admin_client.asend_chat_message(
                project_id=uuid4(),
                message="Should fail",
            )

    @pytest.mark.asyncio
    async def test_aget_conversations_empty(self, admin_client: RestClient):
        """Listing conversations with no filter returns without error (async)."""
        convos = await admin_client.aget_conversations(limit=5)
        assert isinstance(convos, ChatConversationList)
        assert isinstance(convos.conversations, list)

    @pytest.mark.asyncio
    async def test_aget_conversation_not_found(self, admin_client: RestClient):
        """Fetching a non-existent session returns 404 (async)."""
        with pytest.raises(ChatFetchError, match="404") as exc_info:
            await admin_client.aget_conversation(uuid4())
        assert "not found" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_astore_message_bad_session(self, admin_client: RestClient):
        """Storing a message to a non-existent session returns 404 (async)."""
        with pytest.raises(ChatError, match="404") as exc_info:
            await admin_client.astore_conversation_message(
                session_id=uuid4(),
                message={"role": "user", "content": "orphan"},
            )
        assert "not found" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_aqueue_chat_message_bad_project(self, admin_client: RestClient):
        """Queueing a message with a non-existent project_id returns 404 (async)."""
        with pytest.raises(ChatError, match="404") as exc_info:
            await admin_client.aqueue_chat_message(
                session_id=uuid4(),
                project_id=uuid4(),
                message="Should fail",
            )
        assert "not found" in str(exc_info.value).lower()

    @pytest.mark.live_agent
    @pytest.mark.timeout(TEST_TIMEOUT)
    @pytest.mark.flaky(reruns=RETRY_ATTEMPTS)
    @pytest.mark.asyncio
    async def test_aqueue_chat_message(
        self, admin_client: RestClient, chat_project_id: UUID
    ):
        """Queue a message into a running chat session (async)."""
        send_result = await admin_client.asend_chat_message(
            project_id=chat_project_id,
            message="Setting up for async queue test",
            job_name=CHAT_JOB_NAME,
        )
        session_id = send_result.session_id

        result = await admin_client.aqueue_chat_message(
            session_id=session_id,
            project_id=chat_project_id,
            message="Injected via async queue",
        )
        assert isinstance(result, QueueMessageResponse)
        assert result.id is not None
        assert result.target_id == session_id
