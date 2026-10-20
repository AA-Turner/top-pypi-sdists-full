"""FORCING GUARD — every xAI completion of one conversation carries ``x-grok-conv-id``.

xAI's prompt cache is automatic but only hits when a conversation's requests
land on the same server, which xAI decides from the ``x-grok-conv-id`` header
(docs: "maximizing cache hits"). Our native gRPC path sent nothing: live on
2026-10-16 a two-turn Grok conversation read 128 of ~11.5k prompt tokens from
cache on BOTH turns. xai_sdk 1.19.0 has no public per-request metadata seam, so
the chat's stub is wrapped (``xai_api.route_chat_to_conversation``) and the
header rides each RPC's ``metadata=``.

These run the REAL ``xai_sdk.aio.chat.Chat`` against a recording stub. Red on
origin/main (no routing at all), green after.
"""

from __future__ import annotations

import asyncio
import inspect
from typing import Any

import pytest
from xai_sdk.aio.chat import Chat
from xai_sdk.chat import user
from xai_sdk.proto import chat_pb2

from matrx_ai.providers.xai import xai_api


class _Stop(Exception):
    pass


class _RecordingStub:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []

    async def GetCompletion(self, request: Any, *, metadata: Any = None, **_kw: Any) -> Any:  # noqa: N802
        self.calls.append(("GetCompletion", metadata))
        raise _Stop

    def GetStoredCompletion(self, request: Any, *, metadata: Any = None) -> Any:  # noqa: N802
        self.calls.append(("GetStoredCompletion", metadata))
        return None


def _header(metadata: Any) -> str | None:
    return dict(metadata or ()).get("x-grok-conv-id")


def _chat(stub: _RecordingStub, text: str) -> Chat:
    return Chat(stub, None, None, model="grok-4.3", messages=[user(text)])


def _sample(chat: Chat) -> None:
    with pytest.raises(_Stop):
        asyncio.run(chat.sample())


def test_two_turns_of_one_conversation_carry_the_same_routing_header() -> None:
    route = getattr(xai_api, "route_chat_to_conversation", None)
    assert route is not None, "the xAI path attaches no conversation routing at all"
    headers = []
    for turn in ("first question", "second question"):
        stub = _RecordingStub()
        chat = _chat(stub, turn)
        assert route(chat, "081a351a-0264-4fe4-8d55-a12d4e8f9a11") is True
        _sample(chat)
        headers.append(_header(stub.calls[-1][1]))
    assert headers[0] and headers[0] == headers[1]
    assert "081a351a" not in headers[0], "the raw conversation id must not leave the platform"


def test_two_conversations_route_apart_and_no_id_means_no_header() -> None:
    a = xai_api.xai_conversation_routing_id("conv-a")
    b = xai_api.xai_conversation_routing_id("conv-b")
    assert a and b and a != b
    stub = _RecordingStub()
    chat = _chat(stub, "hi")
    assert xai_api.route_chat_to_conversation(chat, None) is False
    _sample(chat)
    assert _header(stub.calls[-1][1]) is None


def test_the_execute_path_attaches_the_header() -> None:
    """Wired into XAIChat.execute, after the chat is created — not only callable."""
    source = inspect.getsource(xai_api.XAIChat.execute)
    create = source.index("self.client.chat.create(")
    routed = source.index("route_chat_to_conversation(chat, get_app_context().conversation_id)")
    assert routed > create


def test_non_completion_rpcs_are_passed_through_untouched() -> None:
    stub = _RecordingStub()
    chat = _chat(stub, "hi")
    xai_api.route_chat_to_conversation(chat, "conv-a")
    chat._stub.GetStoredCompletion(chat_pb2.GetStoredCompletionRequest(response_id="r"))
    assert stub.calls == [("GetStoredCompletion", None)]
