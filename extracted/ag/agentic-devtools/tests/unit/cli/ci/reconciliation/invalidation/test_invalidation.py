"""Tests for trusted invalidation helpers."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.invalidation import invalidate_ledger, unavailable_non_terminal_scope
from agentic_devtools.cli.ci.reconciliation.ledger import WorkLedgerService
from agentic_devtools.cli.ci.reconciliation.models import (
    CandidateInventoryRecord,
    DecisionStatus,
    InvalidationReason,
    LifecycleState,
    ObservationOutcome,
    ScopeClassification,
    TriStateValue,
)


def _record() -> CandidateInventoryRecord:
    return CandidateInventoryRecord(
        record_id="owner/repo#1",
        repo="owner/repo",
        pr_number=1,
        target_branch="main",
        lifecycle_state=LifecycleState.NON_TERMINAL,
        scope_classification=ScopeClassification.ACTIVE,
        eligibility_state=TriStateValue.TRUE,
        observation_outcome=ObservationOutcome.TRUSTED_OBSERVATION,
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10.0,
    )


def test_invalidate_ledger_marks_decision_superseded() -> None:
    service = WorkLedgerService()
    record = _record()
    ledger = service.ensure_ledger(record)
    ledger = service.record_observation(
        ledger=ledger, record=record, change_id="sha", outcome=ObservationOutcome.TRUSTED_OBSERVATION
    )
    ledger = service.record_decision(
        ledger=ledger,
        record=record,
        status=DecisionStatus.ALLOWED,
        reason="ok",
        evidence_digest="digest",
    )
    invalidated = invalidate_ledger(
        ledger=ledger,
        reason=InvalidationReason.STALE_EVIDENCE,
        invalidated_at_utc_z="2026-09-15T12:30:00Z",
        details="stale",
    )
    assert invalidated.current_work_state == "invalidated"
    assert invalidated.superseded_decision_ids


def test_unavailable_non_terminal_scope_returns_pending() -> None:
    assert unavailable_non_terminal_scope() == ScopeClassification.PENDING_UNVERIFIED


def test_invalidate_ledger_without_decision_keeps_superseded_empty() -> None:
    record = _record()
    ledger = WorkLedgerService().ensure_ledger(record)
    invalidated = invalidate_ledger(
        ledger=ledger,
        reason=InvalidationReason.UNVERIFIABLE,
        invalidated_at_utc_z="2026-09-15T12:05:00Z",
        details="no trusted evidence",
    )
    assert invalidated.superseded_decision_ids == ()
