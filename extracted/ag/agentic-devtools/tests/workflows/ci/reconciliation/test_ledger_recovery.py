"""Workflow tests for ledger idempotency and recovery behavior."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.ledger import WorkLedgerService
from agentic_devtools.cli.ci.reconciliation.models import (
    CandidateInventoryRecord,
    DecisionStatus,
    LifecycleState,
    ObservationOutcome,
    ScopeClassification,
    TriStateValue,
)


def _record() -> CandidateInventoryRecord:
    return CandidateInventoryRecord(
        record_id="owner/repo#7",
        repo="owner/repo",
        pr_number=7,
        target_branch="main",
        lifecycle_state=LifecycleState.NON_TERMINAL,
        scope_classification=ScopeClassification.ACTIVE,
        eligibility_state=TriStateValue.TRUE,
        observation_outcome=ObservationOutcome.TRUSTED_OBSERVATION,
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10.0,
    )


def test_ledger_recovery_avoids_duplicate_decisions() -> None:
    service = WorkLedgerService()
    record = _record()
    ledger = service.ensure_ledger(record)
    ledger = service.record_observation(
        ledger=ledger, record=record, change_id="sha", outcome=ObservationOutcome.TRUSTED_OBSERVATION
    )
    ledger = service.record_decision(
        ledger=ledger, record=record, status=DecisionStatus.ALLOWED, reason="ok", evidence_digest="digest"
    )
    replay = service.record_decision(
        ledger=ledger, record=record, status=DecisionStatus.ALLOWED, reason="ok", evidence_digest="digest"
    )
    assert len(replay.decisions) == 1
