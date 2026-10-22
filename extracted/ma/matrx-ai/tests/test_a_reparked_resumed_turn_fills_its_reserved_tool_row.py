"""FORCING GUARD — a resumed turn that parks again never leaves its tool row empty.

A resumed turn's trigger is the TOOL message built from the answered call (the person's answer
to ``ask_person``). Its ``cx_message`` row is RESERVED at turn start, ``pending`` with empty
content (F17). When that turn parks again on a person (a second ask), the loop suspends through
``_flush_assistant_message_mid_loop`` and the end-of-loop persist never reaches the row, so the
reservation stayed empty and the watchdog swept it to ``abandoned`` (census 2026-10-21 #11).

The fix lets the mid-loop flush fill a RESERVED tool trigger row with the pointer block of the
answered call (the shape the end-of-loop persist writes). On the code before it this test fails:
without the gate (before ``12e9ed9991``) the flush drops every non-user trigger; with the gate but
the raw block (``12e9ed9991``) ``ToolResultPart`` refuses the raw ``content`` and the write is only
logged. Either way no write reaches the reserved id and the row stays empty. Seams copied from
``test_executor_user_message_reservation.py``.
"""

from __future__ import annotations

from typing import Any

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import (
    MessageList,
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
)
from matrx_ai.orchestrator.requests import AIMatrixRequest

CONVERSATION = "11111111-1111-1111-1111-111111111111"
REQUEST = "33333333-3333-3333-3333-333333333333"
ANSWER = "Use the blue logo, not the red one."


class _Ctx:
    conversation_id = CONVERSATION
    user_id = "22222222-2222-2222-2222-222222222222"
    request_id = REQUEST
    store = True
    metadata: dict[str, Any] = {}


class _Tracker:
    async def reserve(self, *a: Any, **k: Any) -> None:
        return None

    async def mark_active(self, *a: Any, **k: Any) -> None:
        return None

    def register_existing(self, *a: Any, **k: Any) -> None:
        return None


def _resumed_turn() -> AIMatrixRequest:
    """History rebuilt from the DB (rows carry ids) + the NEW tool message the resume built
    from the person's answer (no id yet: its row is only the empty reservation)."""
    history = [
        UnifiedMessage(role="user", content=[TextContent(text="Draft the post.")], id="m-user", position=0),
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="ask-1", name="ask_person", arguments={"question": "Which logo?"})],
            id="m-ask",
            position=1,
        ),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="ask-1", name="ask_person", content=ANSWER)],
        ),
    ]
    config = UnifiedConfig(model="claude-haiku-4-5", messages=MessageList(_messages=history))
    return AIMatrixRequest(conversation_id=CONVERSATION, config=config, request_id=REQUEST)


@pytest.mark.asyncio
async def test_a_reparked_resumed_turn_fills_its_reserved_tool_row(monkeypatch: pytest.MonkeyPatch) -> None:
    creates: list[dict[str, Any]] = []
    updates: list[tuple[str, dict[str, Any]]] = []

    import matrx_ai.persistence.queue_helpers as qh

    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: creates.append(kw) or "")
    monkeypatch.setattr(
        qh, "queue_message_update", lambda message_id, **kw: updates.append((message_id, kw)) or ""
    )
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _Tracker())

    from matrx_ai.orchestrator.execution_state import ExecutionState

    state = ExecutionState()
    state.committed_position = 1  # the rebuilt history is durable; the tool row is not
    reserved = {2: "reserved-tool-row"}
    # The turn parks AGAIN: the model asks the person a second question.
    response = executor_mod.UnifiedResponse(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id="ask-2", name="ask_person", arguments={"question": "Which size?"})],
            )
        ]
    )

    await executor_mod._flush_assistant_message_mid_loop(
        response=response,
        current_request=_resumed_turn(),
        exec_ctx=_Ctx(),
        reserved_messages=reserved,
        parent_refs={"conversation_id": CONVERSATION},
        trigger_position=2,
        state=state,
    )

    stored = [kw for message_id, kw in updates if message_id == "reserved-tool-row"]
    assert stored, (
        "the reserved tool row got no write: it stays pending and empty and is swept to "
        f"'abandoned' (updates={updates!r})"
    )
    content = stored[0].get("content") or []
    assert content, "the reserved tool row was written EMPTY"
    # A tool row stores the POINTER to its call (the answer itself lives on cx_tool_call), exactly
    # as the end-of-loop persist writes it.
    assert [(b.get("type"), b.get("call_id")) for b in content] == [("tool_result", "ask-1")], content
    assert stored[0].get("status") == "active"


@pytest.mark.asyncio
async def test_a_rebuilt_tool_row_is_never_rewritten(monkeypatch: pytest.MonkeyPatch) -> None:
    """The other side of the gate: a tool message rebuilt from the DB (it has its id) or one with
    no reservation is already durable and gets no write."""
    updates: list[tuple[str, dict[str, Any]]] = []

    import matrx_ai.persistence.queue_helpers as qh

    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: "")
    monkeypatch.setattr(
        qh, "queue_message_update", lambda message_id, **kw: updates.append((message_id, kw)) or ""
    )
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _Tracker())

    from matrx_ai.orchestrator.execution_state import ExecutionState

    state = ExecutionState()
    state.committed_position = 1
    response = executor_mod.UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=[TextContent(text="thinking")])]
    )
    await executor_mod._flush_assistant_message_mid_loop(
        response=response,
        current_request=_resumed_turn(),
        exec_ctx=_Ctx(),
        reserved_messages={},
        parent_refs={"conversation_id": CONVERSATION},
        trigger_position=2,
        state=state,
    )
    assert not updates, updates
