"""`send_chat_message` after a post-send failure: return if the message landed, else raise."""

from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import httpx
import pytest
from tenacity import wait_none

from edison_client.clients.chat_methods import ChatError, ChatMethods
from edison_client.models.chat import (
    ChatDispatchStatus,
    ConversationDetail,
    ConversationMessage,
)

_MESSAGE = "next task"


def _ok_response(session_id: Any) -> MagicMock:
    response = MagicMock(spec=httpx.Response)
    response.status_code = 200
    response.raise_for_status.return_value = None
    response.json.return_value = {"session_id": str(session_id), "status": "dispatched"}
    return response


def _queue_response(contents: list[str]) -> MagicMock:
    response = MagicMock(spec=httpx.Response)
    response.raise_for_status.return_value = None
    response.json.return_value = [{"message": {"content": c}} for c in contents]
    return response


def _user_message(content: str, *, seconds_ago: float) -> ConversationMessage:
    return ConversationMessage(
        role="user",
        content=content,
        created_at=datetime.now(UTC) - timedelta(seconds=seconds_ago),
    )


class _StubChatClient(ChatMethods):
    """`post` raises `failures` in order, then succeeds; `get` serves the pending queue."""

    def __init__(
        self,
        *,
        session_id: Any,
        failures: list[Exception],
        queued: list[str] | None = None,
        stored: list[ConversationMessage] | None = None,
    ) -> None:
        self._stored = stored or []
        self.sync_post = MagicMock(side_effect=[*failures, _ok_response(session_id)])
        self.async_post = AsyncMock(side_effect=[*failures, _ok_response(session_id)])
        self.sync_get = MagicMock(return_value=_queue_response(queued or []))
        self.async_get = AsyncMock(return_value=_queue_response(queued or []))
        self._sync = MagicMock(
            spec=httpx.Client, post=self.sync_post, get=self.sync_get
        )
        self._async = MagicMock(
            spec=httpx.AsyncClient, post=self.async_post, get=self.async_get
        )

    @property
    def client(self) -> httpx.Client:
        return self._sync

    @property
    def async_client(self) -> httpx.AsyncClient:
        return self._async

    def get_conversation(self, session_id: Any, **_: Any) -> ConversationDetail:
        return ConversationDetail(session_id=session_id, messages=self._stored)

    async def aget_conversation(self, session_id: Any, **_: Any) -> ConversationDetail:
        return ConversationDetail(session_id=session_id, messages=self._stored)


@pytest.fixture(autouse=True)
def no_waits(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "edison_client.clients.chat_methods._DELIVERY_CHECK_WAIT_S", 0.0
    )


async def _asend(chat: _StubChatClient, session_id: Any) -> Any:
    send = ChatMethods.asend_chat_message.retry_with(wait=wait_none())  # type: ignore[attr-defined]
    return await send(chat, uuid4(), _MESSAGE, session_id=session_id)


@pytest.mark.asyncio
async def test_read_timeout_returns_when_message_is_queued() -> None:
    session_id = uuid4()
    chat = _StubChatClient(
        session_id=session_id, failures=[httpx.ReadTimeout("slow")], queued=[_MESSAGE]
    )
    result = await _asend(chat, session_id)
    assert result.session_id == session_id
    assert result.status is ChatDispatchStatus.PENDING
    assert chat.async_post.await_count == 1


@pytest.mark.asyncio
async def test_read_timeout_returns_when_message_is_stored() -> None:
    session_id = uuid4()
    chat = _StubChatClient(
        session_id=session_id,
        failures=[httpx.ReadTimeout("slow")],
        stored=[_user_message(_MESSAGE, seconds_ago=5)],
    )
    result = await _asend(chat, session_id)
    assert result.status is ChatDispatchStatus.PENDING
    assert chat.async_post.await_count == 1


@pytest.mark.asyncio
async def test_read_timeout_raises_when_message_never_landed() -> None:
    # An identical prompt from long ago (a repeat task) does not count as delivered.
    # The message is not re-sent: the server may still be processing the request.
    session_id = uuid4()
    chat = _StubChatClient(
        session_id=session_id,
        failures=[httpx.ReadTimeout("slow")],
        stored=[_user_message(_MESSAGE, seconds_ago=3600)],
    )
    with pytest.raises(httpx.ReadTimeout):
        await _asend(chat, session_id)
    assert chat.async_post.await_count == 1


@pytest.mark.asyncio
async def test_read_timeout_raises_when_delivery_check_fails() -> None:
    # A failing check is not evidence of absence, so the send error propagates unchanged.
    session_id = uuid4()
    chat = _StubChatClient(session_id=session_id, failures=[httpx.ReadTimeout("slow")])
    chat.async_get.side_effect = httpx.ConnectError("refused")
    with pytest.raises(httpx.ReadTimeout):
        await _asend(chat, session_id)
    assert chat.async_post.await_count == 1


@pytest.mark.asyncio
async def test_read_timeout_on_a_new_session_is_not_retried() -> None:
    # No session to check against, and a re-send could create a second session.
    chat = _StubChatClient(session_id=uuid4(), failures=[httpx.ReadTimeout("slow")])
    with pytest.raises(httpx.ReadTimeout):
        await _asend(chat, None)
    assert chat.async_post.await_count == 1
    chat.async_get.assert_not_awaited()


@pytest.mark.asyncio
async def test_connect_error_is_resent_without_checking() -> None:
    session_id = uuid4()
    chat = _StubChatClient(
        session_id=session_id, failures=[httpx.ConnectError("refused")]
    )
    result = await _asend(chat, session_id)
    assert result.status is ChatDispatchStatus.DISPATCHED
    assert chat.async_post.await_count == 2
    chat.async_get.assert_not_awaited()


def _status_error(status_code: int) -> httpx.HTTPStatusError:
    request = httpx.Request("POST", "https://api.test/v0.1/chat")
    response = httpx.Response(status_code, request=request)
    return httpx.HTTPStatusError(str(status_code), request=request, response=response)


@pytest.mark.asyncio
async def test_bad_gateway_returns_when_message_is_stored() -> None:
    session_id = uuid4()
    chat = _StubChatClient(
        session_id=session_id,
        failures=[_status_error(502)],
        stored=[_user_message(_MESSAGE, seconds_ago=5)],
    )
    result = await _asend(chat, session_id)
    assert result.status is ChatDispatchStatus.PENDING
    assert chat.async_post.await_count == 1


@pytest.mark.asyncio
async def test_bad_gateway_raises_when_message_never_landed() -> None:
    session_id = uuid4()
    chat = _StubChatClient(session_id=session_id, failures=[_status_error(502)])
    with pytest.raises(httpx.HTTPStatusError):
        await _asend(chat, session_id)
    assert chat.async_post.await_count == 1


@pytest.mark.asyncio
async def test_too_many_requests_is_resent_without_checking() -> None:
    session_id = uuid4()
    chat = _StubChatClient(session_id=session_id, failures=[_status_error(429)])
    result = await _asend(chat, session_id)
    assert result.status is ChatDispatchStatus.DISPATCHED
    assert chat.async_post.await_count == 2
    chat.async_get.assert_not_awaited()


@pytest.mark.asyncio
async def test_forbidden_is_a_chat_error() -> None:
    session_id = uuid4()
    chat = _StubChatClient(session_id=session_id, failures=[_status_error(403)])
    with pytest.raises(ChatError):
        await _asend(chat, session_id)
    assert chat.async_post.await_count == 1
    chat.async_get.assert_not_awaited()


def test_sync_read_timeout_returns_when_message_is_queued() -> None:
    session_id = uuid4()
    chat = _StubChatClient(
        session_id=session_id, failures=[httpx.ReadTimeout("slow")], queued=[_MESSAGE]
    )
    send = ChatMethods.send_chat_message.retry_with(wait=wait_none())  # type: ignore[attr-defined]
    result = send(chat, uuid4(), _MESSAGE, session_id=session_id)
    assert result.status is ChatDispatchStatus.PENDING
    assert chat.sync_post.call_count == 1
