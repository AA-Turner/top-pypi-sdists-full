"""Replay/idempotency workflow tests for trusted reconciliation."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.identifiers import make_idempotency_key
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.recovery import reclaim_leases
from agentic_devtools.orchestration.idempotency import (
    IdempotencyStateUnknownError,
    OperationLog,
    OperationLogRecord,
    is_reconciliation_run_duplicate,
)


def test_idempotency_key_is_stable_across_replay() -> None:
    first = make_idempotency_key("record", "allowed", "digest")
    second = make_idempotency_key("record", "allowed", "digest")
    assert first == second


def test_failed_record_does_not_clear_pending_after_lease_reclamation(tmp_path) -> None:
    """An ambiguous failed record still blocks dispatch after an expired lease is reclaimed."""
    now = datetime.now(UTC)
    operation_id = "dispatch-operation"
    operation_log = OperationLog(tmp_path, "dispatch-run")
    operation_log.append(
        OperationLogRecord(
            operation_id=operation_id,
            run_id="dispatch-run",
            tool_name="reconciliation.dispatch",
            status="pending",
        )
    )
    operation_log.append(
        OperationLogRecord(
            operation_id=operation_id,
            run_id="dispatch-run",
            tool_name="reconciliation.dispatch",
            status="failed",
        )
    )
    state = QueueState(
        repo="owner/repo",
        revision=0,
        items={
            42: WorkItem(
                pr_number=42,
                repo="owner/repo",
                change_id="sha-1",
                eligibility="eligible",
                due_at=None,
                status=WorkItemStatus.LEASED,
                operation_id=operation_id,
                lease_expires_at=now - timedelta(seconds=1),
            )
        },
        records=[],
        quarantines=[],
    )

    reclaimed = reclaim_leases(state, now_utc=now)
    assert reclaimed.items[42].status is WorkItemStatus.QUEUED

    retry_log = OperationLog(tmp_path, "retry-run")
    with pytest.raises(IdempotencyStateUnknownError, match="outcome is unknown"):
        is_reconciliation_run_duplicate(retry_log, "retry-run", operation_id)
