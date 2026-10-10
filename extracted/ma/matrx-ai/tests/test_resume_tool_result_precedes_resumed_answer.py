"""A resumed turn writes the answered tool result BEFORE the resumed answer.

Positions come from the database in queue order (APPEND). The executor used to
reserve the resumed assistant row first, so the answered ``ask_person`` result
landed one position AFTER the answer: call -> answer -> result (live:
conversations 0e0358f7 and 6017eaf3, 2026-10-09). The tool trigger row must be
queued first.
"""

from __future__ import annotations

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest

from typing import Any


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
async def test_resumed_tool_result_is_queued_before_the_resumed_answer(monkeypatch):
    import matrx_ai.persistence.queue_helpers as qh

    created: list[dict] = []
    monkeypatch.setattr(qh, "queue_message_create", lambda **k: created.append(k) or "id")
    monkeypatch.setattr(qh, "get_coordinator", lambda: _StubCoordinator())

    async def _noop(*a, **k):
        return None

    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _CapturingTracker())
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _StubAppContext())

    messages = MessageList(
        _messages=[
            UnifiedMessage(role="user", id="a" * 8 + "-0000-4000-8000-000000000001", content=[TextContent(text="make me something")], position=0),
            UnifiedMessage(
                role="assistant",
                id="a" * 8 + "-0000-4000-8000-000000000002",
                position=1,
                content=[ToolCallContent(id="call-1", name="ask_person", arguments={})],
            ),
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id="call-1", call_id="call-1", name="ask_person", content=[{"type": "text", "text": "{}"}])],
            ),
        ]
    )
    req = AIMatrixRequest(
        conversation_id=_StubAppContext.conversation_id,
        config=UnifiedConfig(model="claude-haiku-4-5", messages=messages),
        request_id=_StubAppContext.request_id,
    )

    class _Abort:
        async def execute(self, *a, **k):
            raise _AbortIteration()

    with pytest.raises(BaseException):
        await executor_mod._execute_until_complete_inner(
            exec_ctx=_StubAppContext(),
            state=ExecutionState(),
            initial_request=req,
            client=_Abort(),
            max_iterations=1,
            max_retries_per_iteration=0,
        )

    roles = [c["role"] for c in created]
    assert roles == ["tool", "assistant"], roles
