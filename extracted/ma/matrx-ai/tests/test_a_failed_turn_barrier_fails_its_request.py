"""Forcing-function: a run stopped by a failed PER-TURN commit barrier never leaves its
``chat.user_request`` 'pending'.

Live 2026-11-20 03:17 (``knowledge_buckets.tidy_topics`` workflow steps, user requests
701b5856… / 6c85067e…): the per-turn barrier (``_persist_turn_and_commit`` → the
standalone Coordinator's ``finalize``) raised ``PersistenceBarrierError`` (the rows were
refused by ``org_foreign_to_parent``). The loop's barrier handler degraded, recorded
``run_history_write_failure`` and re-raised — but nothing moved the request row to
``failed``. It sat 'pending' until the lifecycle watchdog abandoned it 30 minutes later
(``lifecycle_watchdog_stuck_rows``), with no error on the row.

The final-commit path already settles (``test_a_failed_final_commit_still_fails_its_request``);
this pins the in-loop barrier path through the REAL loop and the REAL settle helper. Only
the provider client, the tool dispatch, the DB gates and the row write are doubled.

Gut check: remove the settle from the loop's ``except PersistenceBarrierError`` handler and
the row stays 'pending'.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage, UnifiedResponse
from matrx_ai.db import conversation_gate as gate
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.persistence.coordinator import FlushReport, PersistenceBarrierError

_CONVERSATION_ID = "f022a228-3056-4c16-897b-d1405945396c"
_REQUEST_ID = "701b5856-1935-4a84-bb53-9a37edd499a6"
_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"


class _Emitter:
    def get_turn_text(self) -> str:
        return ""

    def reset_turn_text(self) -> None:
        return None

    def __getattr__(self, name: str) -> Any:
        async def _noop(*a: Any, **k: Any) -> None:
            return None

        return _noop


class _Tracker:
    async def reserve(self, *a: Any, **k: Any) -> None:
        return None

    async def mark_active(self, *a: Any, **k: Any) -> None:
        return None

    def register_existing(self, *a: Any, **k: Any) -> None:
        return None


class _AnsweringClient:
    async def execute(self, *a: Any, **k: Any) -> UnifiedResponse:
        return UnifiedResponse(
            messages=[UnifiedMessage(role="assistant", content=[TextContent(text="Tidied.")])]
        )


def _barrier_error() -> PersistenceBarrierError:
    return PersistenceBarrierError(
        reason="persist_completed_request",
        report=FlushReport(
            reason="persist_completed_request",
            error="current:3 op(s) unwritable even individually; org_foreign_to_parent",
            ops_lost=3,
        ),
        conversation_id=_CONVERSATION_ID,
        request_id=_REQUEST_ID,
    )


@pytest.mark.asyncio
async def test_a_failed_turn_barrier_moves_the_request_to_failed(monkeypatch) -> None:
    # The stored chat.user_request row, as the gate left it when the run began.
    row: dict[str, Any] = {"id": _REQUEST_ID, "status": "pending", "error": None}

    async def _direct_update(request_id: str, update_kwargs: dict, *, reason: str) -> None:
        assert request_id == _REQUEST_ID
        row.update(update_kwargs)

    monkeypatch.setattr(gate, "_direct_update_user_request", _direct_update)
    monkeypatch.setattr("matrx_ai.client_host.get_conversation_store", lambda: None)

    async def _noop_async(*a: Any, **k: Any) -> None:
        return None

    async def _no_tools(*a: Any, **k: Any) -> tuple:
        return (None, None, [], [], [], None)

    async def _failing_barrier(**k: Any) -> None:
        raise _barrier_error()

    async def _empty_inbox(config: Any, app_ctx: Any) -> Any:
        return app_ctx

    import matrx_ai.db.persistence as persistence_mod
    import matrx_ai.persistence.queue_helpers as queue_helpers

    monkeypatch.setattr(queue_helpers, "queue_message_create", lambda **k: None)
    monkeypatch.setattr(queue_helpers, "queue_message_update", lambda *a, **k: None)
    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: None)
    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", _noop_async)
    monkeypatch.setattr(persistence_mod, "record_run_history_write_failure", _noop_async)
    monkeypatch.setattr(executor_mod, "_persist_turn_and_commit", _failing_barrier)
    monkeypatch.setattr(executor_mod, "handle_tool_calls", _no_tools)
    monkeypatch.setattr(executor_mod, "ensure_conversation_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "ensure_user_request_exists", _noop_async)
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: _Tracker())
    monkeypatch.setattr(executor_mod, "capture_issue", _noop_async)
    monkeypatch.setattr("matrx_ai.tools.dynamic_drain.drain_pending", _empty_inbox)

    ctx = AppContext(
        emitter=_Emitter(),  # type: ignore[arg-type]
        user_id=_USER_ID,
        request_id=_REQUEST_ID,
        conversation_id=_CONVERSATION_ID,
        store=True,
        debug=False,
        snapshot=False,
    )
    monkeypatch.setattr(executor_mod, "get_app_context", lambda: ctx)
    messages = MessageList()
    messages.append_or_extend_user_text("Tidy the topics in this bucket.")
    request = AIMatrixRequest(
        conversation_id=_CONVERSATION_ID,
        request_id=_REQUEST_ID,
        config=UnifiedConfig(model="98a2638a-27ef-434c-80a9-96368b22e0f8", messages=messages),
    )
    token = set_app_context(ctx)
    try:
        with pytest.raises(PersistenceBarrierError):
            await executor_mod._execute_until_complete_inner(
                exec_ctx=ctx,
                state=ExecutionState(),
                initial_request=request,
                client=_AnsweringClient(),
                max_iterations=1,
                max_retries_per_iteration=1,
            )
    finally:
        clear_app_context(token)

    assert row["status"] == "failed", (
        "a run stopped by a failed turn barrier left its chat.user_request "
        f"{row['status']!r} — the lifecycle watchdog abandons it 30 minutes later"
    )
    assert row["error"] and "PersistenceBarrierError" in row["error"], row["error"]
    assert row.get("completed_at") is not None
