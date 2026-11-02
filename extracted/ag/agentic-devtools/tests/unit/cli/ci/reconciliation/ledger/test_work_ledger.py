"""Tests for WorkLedgerService."""

from __future__ import annotations

from dataclasses import replace

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
        record_id="owner/repo#42",
        repo="owner/repo",
        pr_number=42,
        target_branch="main",
        lifecycle_state=LifecycleState.NON_TERMINAL,
        scope_classification=ScopeClassification.ACTIVE,
        eligibility_state=TriStateValue.TRUE,
        observation_outcome=ObservationOutcome.TRUSTED_OBSERVATION,
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10.0,
    )


def test_record_observation_is_idempotent() -> None:
    service = WorkLedgerService()
    ledger = service.ensure_ledger(_record())
    first = service.record_observation(
        ledger=ledger, record=_record(), change_id="sha", outcome=ObservationOutcome.TRUSTED_OBSERVATION
    )
    second = service.record_observation(
        ledger=first, record=_record(), change_id="sha", outcome=ObservationOutcome.TRUSTED_OBSERVATION
    )
    assert len(first.observations) == 1
    assert len(second.observations) == 1


def test_record_decision_is_idempotent_by_key() -> None:
    service = WorkLedgerService()
    record = _record()
    ledger = service.ensure_ledger(record)
    ledger = service.record_observation(
        ledger=ledger, record=record, change_id="sha", outcome=ObservationOutcome.TRUSTED_OBSERVATION
    )
    first = service.record_decision(
        ledger=ledger,
        record=record,
        status=DecisionStatus.ALLOWED,
        reason="fresh evidence",
        evidence_digest="digest",
    )
    second = service.record_decision(
        ledger=first,
        record=record,
        status=DecisionStatus.ALLOWED,
        reason="fresh evidence",
        evidence_digest="digest",
    )
    assert len(first.decisions) == 1
    assert len(second.decisions) == 1
    assert first.action_eligibility == TriStateValue.TRUE


def test_record_decision_without_unfinished_observation_is_noop() -> None:
    service = WorkLedgerService()
    record = _record()
    ledger = service.ensure_ledger(record)
    decided = service.record_decision(
        ledger=ledger,
        record=record,
        status=DecisionStatus.BLOCKED,
        reason="not ready",
        evidence_digest="digest",
    )
    assert decided == ledger


def test_record_decision_skips_when_idempotency_key_already_present() -> None:
    service = WorkLedgerService()
    record = _record()
    ledger = service.ensure_ledger(record)
    observed = service.record_observation(
        ledger=ledger,
        record=record,
        change_id="sha",
        outcome=ObservationOutcome.TRUSTED_OBSERVATION,
    )
    expected_key = service.record_decision(
        ledger=observed,
        record=record,
        status=DecisionStatus.ALLOWED,
        reason="x",
        evidence_digest="digest",
    ).idempotency_keys[0]
    prepared = replace(
        observed,
        idempotency_keys=(expected_key,),
        unfinished_decision_observation_id=observed.unfinished_decision_observation_id,
    )
    skipped = service.record_decision(
        ledger=prepared,
        record=record,
        status=DecisionStatus.ALLOWED,
        reason="duplicate",
        evidence_digest="digest",
    )
    assert skipped == prepared
