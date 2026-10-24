"""A run that fails or is refused before any answer leaves a normal VISIBLE assistant error turn.

Owner ruling 2026-10-23: every run is recorded like a chat. Before this, a run refused before a
reply row was reserved (an automation guardrail, a usage refusal, a provider rejection with no
streaming reservation) wrote the person's turn and the failed ``chat.user_request`` — and nothing
after it (agent_tests_judge: 380 conversations with 0 assistant messages). Now it writes the same
row a reserved failed turn is closed to: role assistant, status failed, the sentence as content,
the structured error in ``error``, hidden from the MODEL only.
"""

from __future__ import annotations

import pytest

from matrx_ai.config import MessageList, TextContent, TokenUsage, UnifiedConfig, UnifiedMessage
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest
from test_system_run_keeps_full_history import (  # noqa: F401 — the harness fixture
    CONVERSATION_ID,
    REQUEST_ID,
    system_run_harness,
)

REFUSAL = {
    "error_type": "automation_guardrail",
    "message": "Refused: paused by its guardrail — daily spend cap reached.",
}


def _failed(*, with_reply: bool) -> CompletedRequest:
    messages = [UnifiedMessage(role="user", content=[TextContent(text="judge this answer")])]
    if with_reply:
        messages.append(UnifiedMessage(role="assistant", content=[TextContent(text="partial")]))
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
        metadata={"status": "failed", "error": REFUSAL},
    )


def _assistant_rows(calls):
    return [kw for kw in calls["message_create"] if kw.get("role") == "assistant"] + [
        kw for _, kw in calls["message_update"] if kw.get("role") == "assistant" or kw.get("status") == "failed"
    ]


@pytest.mark.asyncio
async def test_a_refused_run_writes_one_visible_error_turn(system_run_harness):
    persistence_mod, calls = system_run_harness
    result = await persistence_mod.persist_completed_request(_failed(with_reply=False), conversation_id=CONVERSATION_ID)

    rows = _assistant_rows(calls)
    assert len(rows) == 1, rows
    row = rows[0]
    assert row["status"] == "failed"
    assert row["is_visible_to_model"] is False
    assert "is_visible_to_user" not in row or row["is_visible_to_user"] is True
    assert row["content"] == [{"type": "text", "text": REFUSAL["message"]}]
    assert row["error"] == REFUSAL
    assert row["conversation_id"] == CONVERSATION_ID
    assert row["id"] in result["message_ids"]


@pytest.mark.asyncio
async def test_a_failed_run_that_answered_gets_no_second_turn(system_run_harness):
    persistence_mod, calls = system_run_harness
    await persistence_mod.persist_completed_request(_failed(with_reply=True), conversation_id=CONVERSATION_ID)
    failed = [kw for kw in calls["message_create"] if kw.get("status") == "failed"]
    assert failed == []


@pytest.mark.asyncio
async def test_a_mid_run_flush_writes_no_error_turn(system_run_harness):
    persistence_mod, calls = system_run_harness
    await persistence_mod.persist_completed_request(
        _failed(with_reply=False), conversation_id=CONVERSATION_ID, is_final=False
    )
    assert [kw for kw in calls["message_create"] if kw.get("status") == "failed"] == []
