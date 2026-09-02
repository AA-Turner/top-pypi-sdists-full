from __future__ import annotations

from typing import Any

import matrx_ai.client_host as client_host
from matrx_ai.persistence import queue_helpers
from matrx_ai.tools import _db_log
from matrx_ai.tools._debug_log import trace_sinks_enabled


def test_tool_trace_declares_conversation_parent_dependency(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def _capture(table: str, payload: dict[str, Any], **kwargs: Any) -> str:
        captured.update(table=table, payload=payload, **kwargs)
        return "op-1"

    monkeypatch.setattr(queue_helpers, "_queue_or_drop", _capture)

    queue_helpers.queue_tool_trace_create(
        id="trace-1",
        conversation_id="conversation-1",
        event="START",
    )

    assert captured["table"] == "chat.tool_trace"
    assert captured["depends_on"] == (("chat.conversation", "conversation-1"),)


def test_db_log_joins_active_coordinator_synchronously(monkeypatch) -> None:
    queued: list[dict[str, Any]] = []
    coordinator = object()
    monkeypatch.setattr(client_host, "get_conversation_store", lambda: None)
    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: coordinator)
    monkeypatch.setattr(
        queue_helpers,
        "queue_tool_trace_create",
        lambda **row: queued.append(row) or "op-1",
    )

    # This test asserts on the DB sink itself, so it opts past the pytest stage
    # guard that keeps ordinary test traffic out of `cx_tool_trace`.
    with trace_sinks_enabled():
        result = _db_log.db_log_event(
            "START",
            tool_name="demo",
            conversation_id="conversation-1",
            call_id="call-1",
        )

    assert len(queued) == 1
    assert queued[0]["conversation_id"] == "conversation-1"
    assert result.cr_frame is not None
    result.close()


def test_db_log_delegated_dispatch_event_classifies_ok(monkeypatch) -> None:
    """The delegated-dispatch trace (`DELEGATED`, kind=DELEGATE) is a suspension,
    not a failure — it must land in chat.tool_trace with fault_domain='ok' so
    the admin dashboard's defect counts stay honest. Pins the fix for
    client-delegated tools leaving ZERO trace rows (the executor's
    delegated_pending early-return used to skip all sink logging)."""
    queued: list[dict[str, Any]] = []
    monkeypatch.setattr(client_host, "get_conversation_store", lambda: None)
    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: object())
    monkeypatch.setattr(
        queue_helpers,
        "queue_tool_trace_create",
        lambda **row: queued.append(row) or "op-1",
    )

    with trace_sinks_enabled():
        result = _db_log.db_log_event(
            "DELEGATED",
            tool_name="apply_surface_write",
            kind="DELEGATE",
            conversation_id="conversation-1",
            call_id="call-1",
            metadata={"disposition": "suspended_for_client"},
        )

    assert len(queued) == 1
    assert queued[0]["event"] == "DELEGATED"
    assert queued[0]["kind"] == "DELEGATE"
    assert queued[0]["fault_domain"] == "ok"
    assert queued[0]["metadata"] == {"disposition": "suspended_for_client"}
    result.close()


def test_db_log_drops_trace_on_ephemeral_run(monkeypatch) -> None:
    """store=False means no conversation row is ever written, and
    tool_trace.conversation_id is NOT NULL with an FK to it. Queuing the trace
    anyway made the turn's commit barrier die on a ForeignKeyViolation that can
    NEVER self-heal (the parent is not late — it does not exist), which is
    exactly what stranded two rows in system_write_failure on 2026-07-28.
    """
    from matrx_ai import context as ai_context

    queued: list[dict[str, Any]] = []
    monkeypatch.setattr(client_host, "get_conversation_store", lambda: None)
    monkeypatch.setattr(queue_helpers, "get_coordinator", lambda: object())
    monkeypatch.setattr(
        queue_helpers,
        "queue_tool_trace_create",
        lambda **row: queued.append(row) or "op-1",
    )

    class _EphemeralCtx:
        store = False

    monkeypatch.setattr(ai_context, "try_get_app_context", lambda: _EphemeralCtx())

    with trace_sinks_enabled():
        result = _db_log.db_log_event(
            "OK",
            tool_name="memory",
            conversation_id="conversation-that-will-never-exist",
            call_id="call-1",
        )

    assert queued == []
    result.close()
