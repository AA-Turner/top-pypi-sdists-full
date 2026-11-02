"""Workflow tests for invalidation and historical retention."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.invalidation import invalidate_ledger
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


def test_invalidation_workflow_preserves_history() -> None:
    service = WorkLedgerService()
    record = CandidateInventoryRecord(
        record_id="owner/repo#9",
        repo="owner/repo",
        pr_number=9,
        target_branch="main",
        lifecycle_state=LifecycleState.NON_TERMINAL,
        scope_classification=ScopeClassification.ACTIVE,
        eligibility_state=TriStateValue.TRUE,
        observation_outcome=ObservationOutcome.TRUSTED_OBSERVATION,
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10.0,
    )
    ledger = service.ensure_ledger(record)
    ledger = service.record_observation(
        ledger=ledger, record=record, change_id="sha", outcome=ObservationOutcome.TRUSTED_OBSERVATION
    )
    ledger = service.record_decision(
        ledger=ledger, record=record, status=DecisionStatus.ALLOWED, reason="ok", evidence_digest="digest"
    )
    invalidated = invalidate_ledger(
        ledger=ledger,
        reason=InvalidationReason.PROVIDER_STATE_CHANGED,
        invalidated_at_utc_z="2026-09-15T12:30:00Z",
        details="head changed",
    )
    assert invalidated.invalidations
    assert invalidated.decisions
