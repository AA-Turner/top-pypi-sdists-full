"""A message drained ahead of the first answer must not take the answer's reserved row.

Live (conversation 9b2bbbb9…, 2026-11-18, three turns; and 647f897d…): the loop-start
reservation for the reply is keyed by logical index ``pre_execution_message_count``. The
iteration-1 turn-boundary drain appended a host ``injection:system_message`` turn at exactly
that index, so persistence handed the reply's reserved row to the injection and INSERTed the
real answer as a second row. The reserved assistant row stayed ``pending`` with ``[]`` until the
lifecycle watchdog swept it to ``abandoned`` (``lifecycle_watchdog_stuck_rows`` chat.message).

Contract: after the drain, the reply reservation is re-keyed to the answer's new index, so the
reserved row receives the answer and the drained message is a fresh row.
"""

from __future__ import annotations

from uuid import uuid4

import pytest
from test_iteration_assistant_announcement import (  # noqa: F401 — fixtures
    CONVERSATION_ID,
    REQUEST_ID,
    _parent_user_request_exists,
    persist_harness,
)

from matrx_ai.config import (
    MessageList,
    TextContent,
    UnifiedConfig,
    UnifiedMessage,
    host_authored_user_turn,
)
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.executor import _shift_reply_reservation_past_drained
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest


def test_reservation_moves_only_when_the_drain_lands_before_the_answer():
    state = ExecutionState()
    state.reserved_message_ids = {0: "user-row", 1: "reply-row"}

    # Nothing drained: unchanged.
    assert _shift_reply_reservation_past_drained(state, reply_position=1, before=1, after=1) == 1
    assert state.reserved_message_ids == {0: "user-row", 1: "reply-row"}

    # The answer already exists (a later iteration's drain): unchanged.
    assert _shift_reply_reservation_past_drained(state, reply_position=1, before=3, after=4) == 1
    assert state.reserved_message_ids == {0: "user-row", 1: "reply-row"}

    # Two messages drained ahead of the first answer: the reply row follows the answer.
    assert _shift_reply_reservation_past_drained(state, reply_position=1, before=1, after=3) == 3
    assert state.reserved_message_ids == {0: "user-row", 3: "reply-row"}


@pytest.mark.asyncio
async def test_the_reserved_reply_row_receives_the_answer_not_the_drained_turn(persist_harness):  # noqa: F811 — the imported fixture
    persistence_mod, creates, updates, _request_creates, _tracker = persist_harness
    user_row, reply_row = str(uuid4()), str(uuid4())
    state = ExecutionState()
    state.reserved_message_ids = {0: user_row, 1: reply_row}

    # Loop start: [trigger]. The iteration-1 drain appends the host turn at index 1.
    messages = [UnifiedMessage(role="user", content=[TextContent(text="add one note")])]
    before = len(messages)
    messages.append(host_authored_user_turn("Your proposal was rejected.", reason="injection:system_message"))
    reply_position = _shift_reply_reservation_past_drained(
        state, reply_position=1, before=before, after=len(messages)
    )
    assert reply_position == 2
    messages.append(
        UnifiedMessage(
            role="assistant", content=[TextContent(text="done")], metadata={"provider_iteration": 1}
        )
    )

    cfg = UnifiedConfig(model="claude-test", messages=MessageList(_messages=messages))
    completed = CompletedRequest(
        request=AIMatrixRequest(conversation_id=CONVERSATION_ID, config=cfg, request_id=REQUEST_ID),
        iterations=1,
        final_response=UnifiedResponse(messages=[messages[-1]]),
        trigger_message_position=0,
        result_start_position=1,
        result_end_position=2,
    )
    await persistence_mod.persist_completed_request(
        completed, conversation_id=CONVERSATION_ID, state=state
    )

    roles_by_row = {mid: fields.get("role") for mid, fields in updates if "role" in fields}
    assert roles_by_row.get(reply_row) == "assistant", (
        "the reply's reserved row must receive the answer; otherwise it stays pending and the "
        "watchdog sweeps it to 'abandoned'"
    )
    assert roles_by_row.get(user_row) == "user"
    created_roles = [row.get("role") for row in creates]
    assert created_roles == ["user"], "the drained host turn is a fresh row; no second assistant row"
