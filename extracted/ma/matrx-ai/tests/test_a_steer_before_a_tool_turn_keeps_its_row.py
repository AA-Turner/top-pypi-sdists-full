"""FORCING GUARD — a message delivered mid-run keeps its row when the next turn uses a tool.

Q-03, 2026-11-08 (conversation 2411986b…): "From now on use only cities in Texas." was consumed
(``chat.pending_injection`` 80a669c2, ``next_boundary``) and the model obeyed it, but no ``chat.message``
row was ever written. The turn after it called a tool with a browser connected, so
``_flush_assistant_message_mid_loop`` saved the assistant row and the caller moved
``state.committed_position`` past it. The flush only ever wrote the turn's TRIGGER, so anything between
the mark and the assistant (a steer, a helper's report, a wake note) fell below the mark and no later
barrier could reach it. A queued "Thanks." survived only because the turn after it used no tool.

Every message delivered above the trigger is written before the assistant, in order, once.
"""

from __future__ import annotations

from typing import Any

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, ToolCallContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.message_config import host_authored_user_turn
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest

CONVERSATION = "11111111-1111-1111-1111-111111111111"
REQUEST = "33333333-3333-3333-3333-333333333333"
STEER = "From now on use only cities in Texas."


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


class _Response:
    usage = None

    def __init__(self) -> None:
        self.messages = [
            UnifiedMessage(role="assistant", content=[ToolCallContent(id="c1", name="calculate", arguments={"x": 1})])
        ]


def _steered_run(*delivered: UnifiedMessage) -> AIMatrixRequest:
    """A committed turn (trigger + reply, rows carry ids), then what was delivered at the boundary."""
    history = [
        UnifiedMessage(role="user", content=[TextContent(text="Count again, please.")], id="m-trigger", position=0),
        UnifiedMessage(role="assistant", content=[TextContent(text="41. Forty-one.")], id="m-reply", position=1),
        *delivered,
    ]
    config = UnifiedConfig(model="claude-haiku-4-5", messages=MessageList(_messages=history))
    return AIMatrixRequest(conversation_id=CONVERSATION, config=config, request_id=REQUEST)


def _steer() -> UnifiedMessage:
    return UnifiedMessage(
        role="user",
        content=[TextContent(text=STEER)],
        user_content=[TextContent(text=STEER)],
        metadata={"injection_id": "80a669c2"},
    )


async def _flush(monkeypatch: pytest.MonkeyPatch, request: AIMatrixRequest) -> list[dict[str, Any]]:
    creates: list[dict[str, Any]] = []

    import matrx_ai.persistence.queue_helpers as qh

    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: creates.append(kw) or "")
    monkeypatch.setattr(qh, "queue_message_update", lambda message_id, **kw: "")
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _Tracker())
    state = ExecutionState()
    state.committed_position = 1
    await executor_mod._flush_assistant_message_mid_loop(
        response=_Response(),
        current_request=request,
        exec_ctx=_Ctx(),
        reserved_messages={},
        parent_refs={},
        trigger_position=0,
        state=state,
    )
    return creates


def _text(row: dict[str, Any]) -> str:
    return " ".join(str(getattr(b, "text", None) or (b.get("text") if isinstance(b, dict) else "")) for b in row["content"])


@pytest.mark.asyncio
async def test_a_steer_is_written_before_the_assistant_that_follows_it(monkeypatch: pytest.MonkeyPatch) -> None:
    creates = await _flush(monkeypatch, _steered_run(_steer()))
    assert [r["role"] for r in creates] == ["user", "assistant"], creates
    assert STEER in _text(creates[0])
    assert creates[0]["metadata"]["injection_id"] == "80a669c2"
    assert creates[0].get("user_content"), "a person's own words carry user_content"


@pytest.mark.asyncio
async def test_a_host_note_delivered_mid_run_keeps_its_row_too(monkeypatch: pytest.MonkeyPatch) -> None:
    note = host_authored_user_turn("A helper finished: the hub is Dallas.", reason="injection:system_message")
    creates = await _flush(monkeypatch, _steered_run(note))
    assert [r["role"] for r in creates] == ["user", "assistant"], creates
    assert "the hub is Dallas" in _text(creates[0])


@pytest.mark.asyncio
async def test_several_deliveries_land_in_order_and_durable_rows_are_never_rewritten(monkeypatch: pytest.MonkeyPatch) -> None:
    durable = UnifiedMessage(role="user", content=[TextContent(text="already stored")], id="m-old", position=2)
    second = UnifiedMessage(role="user", content=[TextContent(text="And keep it short.")], metadata={"injection_id": "b"})
    creates = await _flush(monkeypatch, _steered_run(durable, _steer(), second))
    assert [r["role"] for r in creates] == ["user", "user", "assistant"], creates
    assert STEER in _text(creates[0]) and "keep it short" in _text(creates[1])
