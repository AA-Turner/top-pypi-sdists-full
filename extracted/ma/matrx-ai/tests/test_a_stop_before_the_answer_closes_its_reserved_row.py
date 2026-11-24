"""A Stop that lands before any answer text never leaves the reply row ``pending`` (CGU-09 P2-3).

Independent iPhone verification (run c1c4c9f3…, 2026-10-31): Send, then Stop within ~0.5 s.
The executor reserves the turn's assistant row (``status='pending'``, empty content) at stream
start, the cancel is seen at the first iteration boundary (or the provider call is stopped
before a single seen frame), and the run finalizes ``cancelled`` with NO assistant message in
the window. Persistence only ever closed an unfilled reservation for a FAILED run, so the
cancelled run's reply row stayed ``pending`` with ``[]`` content until the watchdog swept it
to ``abandoned`` and raised a false stuck-row alarm. A stop later in the stream was fine only
because the partial answer filled the row.

The ruling: a stopped turn whose answer never reached the person closes its reservation as the
stopped turn it is — ``status='active'``, empty content, ``metadata.stopped=True`` (the same
marker a stopped partial carries), hidden from the MODEL (an empty assistant turn must never
be replayed to a provider). An INTERRUPT also hides it from the person, like every abandoned
tail. Seam: the real ``persist_completed_request``; only queue writers, the model lookup and
the app context are doubles (the harness of test_system_run_keeps_full_history.py).
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from test_system_run_keeps_full_history import (  # noqa: F401 — registers the harness fixture by name
    CONVERSATION_ID,
    REQUEST_ID,
    system_run_harness,
)

from matrx_ai.config import MessageList, TextContent, TokenUsage, UnifiedConfig, UnifiedMessage
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

USER_ROW = "6b5c9b0c-d4cc-46cd-b49e-187433cc0c1c"
REPLY_ROW = "018bd08c-3615-46d8-8f9b-58eb8c277d1f"


def _state() -> SimpleNamespace:
    # What the executor's reservation step leaves on its owned state: the trigger at 0,
    # the reply at 1 (first_assistant_position).
    return SimpleNamespace(
        reserved_message_ids={0: USER_ROW, 1: REPLY_ROW},
        reserved_request_ids={},
        pre_existing_message_ids=set(),
        persist_from_position=None,
    )


def _stopped(*, answered: str | None = None, status: str = "cancelled", **meta) -> CompletedRequest:
    messages = [UnifiedMessage(role="user", content=[TextContent(text="Write a long essay.")])]
    if answered is not None:
        messages.append(
            UnifiedMessage(role="assistant", content=[TextContent(text=answered)], metadata={"stopped": True})
        )
    cfg = UnifiedConfig(model="test-model", messages=MessageList(_messages=messages))
    req = AIMatrixRequest(conversation_id=CONVERSATION_ID, config=cfg, request_id=REQUEST_ID)
    req.add_usage(TokenUsage(input_tokens=0, output_tokens=0, matrx_model_name="test-model", api="test"))
    return CompletedRequest(
        request=req,
        iterations=1,
        final_response=None,
        trigger_message_position=0,
        result_start_position=1,
        result_end_position=len(messages) - 1,
        metadata={"status": status, "error": "Request canceled before the next provider call.", **meta},
    )


def _reply_updates(calls) -> list[dict]:
    return [kw for mid, kw in calls["message_update"] if mid == REPLY_ROW]


@pytest.mark.asyncio
async def test_a_stop_before_any_text_closes_the_reserved_reply_row(request):
    persistence_mod, calls = request.getfixturevalue("system_run_harness")
    await persistence_mod.persist_completed_request(
        _stopped(), conversation_id=CONVERSATION_ID, state=_state()
    )

    updates = _reply_updates(calls)
    assert len(updates) == 1, f"the reserved reply row must be closed exactly once: {calls['message_update']}"
    row = updates[0]
    assert row["status"] == "active", "a stopped turn is a terminal, ordinary turn — never left 'pending'"
    assert row["content"] == []
    assert row["metadata"] == {"stopped": True}
    assert row["is_visible_to_model"] is False, "an empty assistant turn must never reach a provider"
    assert row.get("is_visible_to_user", True) is True
    # No invented error turn for a Stop.
    assert [kw for kw in calls["message_create"] if kw.get("status") == "failed"] == []


@pytest.mark.asyncio
async def test_an_interrupt_before_any_text_hides_the_closed_row_from_the_person(request):
    persistence_mod, calls = request.getfixturevalue("system_run_harness")
    await persistence_mod.persist_completed_request(
        _stopped(interrupted=True, hidden_tail_messages=0), conversation_id=CONVERSATION_ID, state=_state()
    )
    (row,) = _reply_updates(calls)
    assert row["status"] == "active"
    assert row["is_visible_to_user"] is False
    assert row["is_visible_to_model"] is False


@pytest.mark.asyncio
async def test_a_stop_after_text_keeps_the_partial_and_is_not_closed_empty(request):
    persistence_mod, calls = request.getfixturevalue("system_run_harness")
    await persistence_mod.persist_completed_request(
        _stopped(answered="Urban cycling will"), conversation_id=CONVERSATION_ID, state=_state()
    )
    (row,) = _reply_updates(calls)
    assert row["content"] != [], "the partial the person saw fills the row"
    assert row.get("is_visible_to_model", True) is not False


@pytest.mark.asyncio
async def test_a_mid_run_flush_never_closes_the_reservation(request):
    persistence_mod, calls = request.getfixturevalue("system_run_harness")
    await persistence_mod.persist_completed_request(
        _stopped(), conversation_id=CONVERSATION_ID, state=_state(), is_final=False
    )
    assert _reply_updates(calls) == []


@pytest.mark.asyncio
async def test_a_cancel_that_lands_before_the_run_registers_is_remembered():
    # The phone POSTs /ai/cancel/{id} the instant Stop is pressed — possibly before the run
    # has polled once or linked its tree. The registry keys the signal on the id alone (no
    # prior registration), so the run's first boundary poll still sees it.
    from matrx_connect.request_controls import RequestControlRegistry

    registry = RequestControlRegistry()
    await registry.cancel("never-seen-before-run")
    assert registry.is_cancelled("never-seen-before-run") is True
    assert registry.is_interrupted("never-seen-before-run") is False
    await registry.interrupt("never-seen-before-run-2")
    assert registry.is_cancelled("never-seen-before-run-2") is True
    assert registry.is_interrupted("never-seen-before-run-2") is True
