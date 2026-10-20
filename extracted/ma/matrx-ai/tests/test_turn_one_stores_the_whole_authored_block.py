"""Turn 1 stores every authored input message, in order, on every door (Agent Evaluation, 2026-10-16).

Persistence wrote from the trigger (the last user message), so authored few-shot pairs — and any
history a client carried into a new conversation — were never stored, and turn 2 reloaded a
history the model never saw. The executor now reserves the whole new input block before the
trigger (APPEND positions follow queue order) and persistence writes from the first new message.
"""

from __future__ import annotations

from typing import Any

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.template_substitution import (
    authored_template_messages,
    fold_typed_turn_into_template,
)
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest


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


class _StubTracker:
    async def reserve(self, *a, **k):
        return None

    async def mark_active(self, *a, **k):
        return None

    def register_existing(self, *a, **k):
        return None


class _StubCoordinator:
    """Truthy stand-in for the streaming lane's WriteCoordinator (reservation is gated on it)."""

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
    """Raised by the stub client right after the reservation block has run."""


EX_Q, EX_A, TYPED = (
    "Example: two-tier, Saturday",
    "NAME: Example Person",
    "Three tiers, Sunday pickup.",
)


async def _reservations(monkeypatch, config: UnifiedConfig) -> list[tuple[str, str, bool]]:
    import matrx_ai.persistence.queue_helpers as qh

    created: list[dict[str, Any]] = []
    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: created.append(kw) or "id")
    monkeypatch.setattr(qh, "get_coordinator", lambda: _StubCoordinator())

    async def _noop(*a, **k):
        return None

    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _StubTracker())
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: _StubAppContext())

    class _Abort:
        async def execute(self, *a, **k):
            raise _AbortIteration()

    req = AIMatrixRequest(
        conversation_id=_StubAppContext.conversation_id,
        config=config,
        request_id=_StubAppContext.request_id,
    )
    with pytest.raises(BaseException):
        await executor_mod._execute_until_complete_inner(
            exec_ctx=_StubAppContext(),
            state=ExecutionState(),
            initial_request=req,
            client=_Abort(),
            max_iterations=1,
            max_retries_per_iteration=0,
        )
    out = []
    for c in created:
        text = " ".join(b.get("text", "") for b in (c.get("content") or []) if isinstance(b, dict))
        out.append((c["role"], text, bool(c.get("authored"))))
    return out


def _assert_whole_block(rows: list[tuple[str, str, bool]]) -> None:
    roles = [r for r, _, _ in rows]
    assert roles == ["user", "assistant", "user", "assistant"], rows
    assert EX_Q in rows[0][1] and EX_A in rows[1][1] and TYPED in rows[2][1], rows
    assert rows[3][1] == "", "the last reservation is the reply placeholder"
    # One author for the whole authored block, so the flush (one group per author, in order)
    # writes it before the person's trigger and the model's reply.
    assert [a for _, _, a in rows] == [True, True, False, False], rows


@pytest.mark.asyncio
async def test_agents_door_stores_few_shot_pairs_before_the_trigger(monkeypatch) -> None:
    messages = MessageList(
        _messages=[
            UnifiedMessage(role="user", content=[TextContent(text=EX_Q)]),
            UnifiedMessage(role="assistant", content=[TextContent(text=EX_A)]),
            UnifiedMessage(role="user", content=[TextContent(text="Order name: Benedita")]),
        ]
    )
    messages.append_or_extend_user_text(TYPED, own_block=True)
    _assert_whole_block(
        await _reservations(monkeypatch, UnifiedConfig(model="claude-haiku-4-5", messages=messages))
    )


@pytest.mark.asyncio
async def test_manual_door_stores_the_authored_block_before_the_trigger(monkeypatch) -> None:
    wire = [
        {"role": "system", "content": "You keep the card."},
        {"role": "user", "content": EX_Q},
        {"role": "assistant", "content": EX_A},
        {"role": "user", "content": "Order name: {{order_name}}"},
        {"role": "user", "content": TYPED},
    ]
    config = UnifiedConfig.from_dict(
        {"model": "claude-haiku-4-5", "messages": wire}, authored_message_count=4
    )
    template = authored_template_messages(wire, 4, config.messages)
    config.replace_variables({"order_name": "Benedita"}, template_messages=template)
    fold_typed_turn_into_template(config.messages, template)
    _assert_whole_block(await _reservations(monkeypatch, config))


@pytest.mark.asyncio
async def test_chat_door_stores_carried_history_of_a_new_conversation(monkeypatch) -> None:
    wire = [
        {"role": "user", "content": EX_Q},
        {"role": "assistant", "content": EX_A},
        {"role": "user", "content": TYPED},
    ]
    config = UnifiedConfig.from_dict(
        {"model": "claude-haiku-4-5", "messages": wire}, authored_message_count=0
    )
    _assert_whole_block(await _reservations(monkeypatch, config))


def test_a_continuation_persists_from_the_trigger_only() -> None:
    stored = [
        UnifiedMessage(role="user", content=[TextContent(text="q")], id="m1", position=0, from_store=True),
        UnifiedMessage(role="assistant", content=[TextContent(text="a")], id="m2", position=1, from_store=True),
        UnifiedMessage(role="user", content=[TextContent(text="new")]),
    ]
    assert executor_mod.first_new_input_position(stored, 2) == 2
    fresh = [UnifiedMessage(role="user", content=[TextContent(text="x")]) for _ in range(3)]
    assert executor_mod.first_new_input_position(fresh, 2) == 0


def test_an_authored_row_keeps_its_author_through_the_update() -> None:
    """Coalescing keeps the LAST declared author; an UPDATE that re-declared the assistant role
    moved the example's reply into the agent's flush group, after the trigger (live 2026-10-16)."""
    from matrx_orm.core.session_context import current_actor

    import matrx_ai.persistence.queue_helpers as qh

    seen = []

    def capture(*a, **k):
        seen.append(current_actor())
        return ""

    original = qh._queue_or_drop
    qh._queue_or_drop = capture
    try:
        qh.queue_message_create(
            id="a", conversation_id="c", role="assistant", content=[], authored=True
        )
        qh.queue_message_update("a", role="assistant", content=[], authored=True)
        qh.queue_message_update("b", role="assistant", content=[])
    finally:
        qh._queue_or_drop = original
    assert str(seen[0]) == str(seen[1]) and str(seen[0]) != str(seen[2]), seen


@pytest.mark.asyncio
async def test_a_resent_turn_one_never_stores_the_authored_block_twice(monkeypatch) -> None:
    """Review 2026-10-17 item 1.1: turn 1 flushed its block, then the client re-sent the same first
    turn against the now-saved conversation. The history comes from the DB (id + position) and
    the re-sent template/typed messages are new again — they must not become a second copy of the
    authored block; only the trigger is written, as on any continuation."""
    stored = [
        UnifiedMessage(role="user", content=[TextContent(text=EX_Q)], id="m0", position=0, from_store=True),
        UnifiedMessage(role="assistant", content=[TextContent(text=EX_A)], id="m1", position=1, from_store=True),
        UnifiedMessage(
            role="user",
            content=[TextContent(text="Order name: Benedita"), TextContent(text=TYPED)],
            id="m2",
            position=2,
            from_store=True,
        ),
    ]
    resent = [
        UnifiedMessage(role="user", content=[TextContent(text=EX_Q)]),
        UnifiedMessage(role="assistant", content=[TextContent(text=EX_A)]),
        UnifiedMessage(role="user", content=[TextContent(text="Order name: Benedita")]),
        UnifiedMessage(role="user", content=[TextContent(text=TYPED)]),
    ]
    config = UnifiedConfig(
        model="claude-haiku-4-5", messages=MessageList(_messages=stored + resent)
    )
    rows = await _reservations(monkeypatch, config)
    assert [r for r, _, _ in rows] == ["user", "assistant"], rows
    assert rows[0][1] == TYPED and not rows[0][2], (
        "only the trigger; no authored row on a continuation"
    )
