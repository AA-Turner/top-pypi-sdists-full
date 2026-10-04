"""A rejoining page must see the person's own words before the turn settles.

Turn rows commit when the answer finishes. A page reloaded mid-answer rejoins
the live NDJSON journal from frame one; the only frame naming the person's
message is its ``record_reserved`` reservation. That frame must carry the
pristine ``user_content`` (text + attachment refs, no machine template, no
inline bytes) or the rejoined transcript shows an empty bubble until the end.
"""

from __future__ import annotations

from typing import Any

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, UnifiedConfig, UnifiedMessage, TextContent
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.orchestrator.user_turn_echo import (
    MAX_USER_TURN_ECHO_BYTES,
    user_turn_echo,
)

class _StubEmitter:
    async def send_info(self, *a, **k):
        return None

    async def send_phase(self, *a, **k):
        return None

    async def send_data(self, *a, **k):
        return None

    async def send_chunk(self, *a, **k):
        return None

    async def send_end(self, *a, **k):
        return None

    async def fatal_error(self, *a, **k):
        return None

    def reset_turn_text(self):
        return None

    def get_turn_text(self):
        return ""


class _StubAppContext:
    conversation_id = "11111111-1111-1111-1111-111111111111"
    user_id = "22222222-2222-2222-2222-222222222222"
    parent_conversation_id = None
    request_id = "33333333-3333-3333-3333-333333333333"
    store = True
    debug = False
    snapshot = False
    metadata: dict[str, Any] = {}
    emitter = _StubEmitter()


class _StubCoordinator:
    """Truthy stand-in: message reservation runs only on a streaming lane."""

    def queue(self, *a, **k):
        return ""

    def commit_async(self, *a, **k):
        return None

    async def check_pending(self, *a, **k):
        return None

    async def finalize(self, *a, **k):
        return None

    async def drain_and_confirm(self, *a, **k):
        return []

    async def seal(self, *a, **k):
        return None


class _AbortIteration(Exception):
    """Stops the run right after the reservation block."""


class _CapturingTracker:
    def __init__(self) -> None:
        self.reservations: list[dict[str, Any]] = []

    async def reserve(self, *a, **k):
        self.reservations.append(k)
        return None

    async def mark_active(self, *a, **k):
        return None

    def register_existing(self, *a, **k):
        return None


@pytest.mark.asyncio
async def test_user_reservation_frame_carries_the_persons_words(monkeypatch):
    import matrx_ai.persistence.queue_helpers as qh

    monkeypatch.setattr(qh, "queue_message_create", lambda **k: "msg-id")
    monkeypatch.setattr(qh, "get_coordinator", lambda: _StubCoordinator())

    async def _noop_async(*a, **k):
        return None

    tracker = _CapturingTracker()
    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: tracker)
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _StubAppContext())

    user_text = "Compare the two leases and flag every renewal clause."
    messages = MessageList(
        _messages=[
            UnifiedMessage(
                role="user",
                content=[TextContent(text="MACHINE TEMPLATE: {{context}}")],
            )
        ]
    )
    messages.append_or_extend_user_text(user_text)
    messages.append_or_extend_user_items(
        [
            {
                "type": "image",
                "file_id": "13c2a464-2ead-4611-9990-702a03e643c4",
                "base64_data": "captured-inline-png-bytes",
                "mime_type": "image/png",
                "size_bytes": 184,
                "metadata": {"display_title": "lease-page-3.png"},
            }
        ]
    )
    req = AIMatrixRequest(
        conversation_id=_StubAppContext.conversation_id,
        config=UnifiedConfig(model="claude-haiku-4-5", messages=messages),
        request_id=_StubAppContext.request_id,
    )

    class _AbortingClient:
        async def execute(self, *a, **k):
            raise _AbortIteration()

    from matrx_ai.orchestrator.execution_state import ExecutionState

    with pytest.raises(BaseException):
        await executor_mod._execute_until_complete_inner(
            exec_ctx=_StubAppContext(),
            state=ExecutionState(),
            initial_request=req,
            client=_AbortingClient(),
            max_iterations=1,
            max_retries_per_iteration=0,
        )

    user_frames = [
        r for r in tracker.reservations
        if (r.get("metadata") or {}).get("role") == "user"
    ]
    assert len(user_frames) == 1, tracker.reservations
    echoed = user_frames[0]["metadata"].get("user_content")
    assert echoed, "user reservation frame carries no user_content — a rejoin shows an empty bubble"
    assert echoed[0]["text"] == user_text
    assert "MACHINE TEMPLATE" not in str(echoed)
    assert echoed[1]["file_id"] == "13c2a464-2ead-4611-9990-702a03e643c4"
    assert echoed[1]["metadata"] == {"display_title": "lease-page-3.png"}
    assert "base64_data" not in echoed[1]

    assistant_frames = [
        r for r in tracker.reservations
        if (r.get("metadata") or {}).get("role") == "assistant"
    ]
    assert all("user_content" not in r["metadata"] for r in assistant_frames)


def test_echo_strips_inline_bytes_and_omits_oversized_content():
    assert user_turn_echo(None) == {}
    assert user_turn_echo([]) == {}
    echo = user_turn_echo(
        [{"type": "text", "text": "hi"}, {"type": "image", "base64": "AAAA", "file_id": "f"}]
    )
    assert echo == {"user_content": [{"type": "text", "text": "hi"}, {"type": "image", "file_id": "f"}]}
    huge = [{"type": "text", "text": "x" * (MAX_USER_TURN_ECHO_BYTES + 1)}]
    assert user_turn_echo(huge) == {}
