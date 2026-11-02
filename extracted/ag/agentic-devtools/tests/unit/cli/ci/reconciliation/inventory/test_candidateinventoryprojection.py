"""Tests for candidate inventory projection helpers."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.inventory import (
    CandidateInventoryProjection,
    apply_recovery_result,
    classify_scope,
    schedule_retry_due,
)
from agentic_devtools.cli.ci.reconciliation.models import (
    CandidateInventoryRecord,
    LifecycleState,
    ObservationOutcome,
    RecoveryDisposition,
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
        scope_classification=ScopeClassification.PENDING_UNVERIFIED,
        eligibility_state=TriStateValue.UNKNOWN,
        observation_outcome=ObservationOutcome.TRUSTED_OBSERVATION,
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10.0,
    )


def test_projection_upsert_replaces_existing_record() -> None:
    projection = CandidateInventoryProjection(records={})
    updated = projection.upsert(_record())
    assert "owner/repo#1" in updated.records


def test_classify_scope_variants() -> None:
    assert (
        classify_scope(
            lifecycle_state=LifecycleState.NON_TERMINAL,
            eligibility_state=TriStateValue.TRUE,
            observation_outcome=ObservationOutcome.TRUSTED_OBSERVATION,
        )
        == ScopeClassification.ACTIVE
    )
    assert (
        classify_scope(
            lifecycle_state=LifecycleState.NON_TERMINAL,
            eligibility_state=TriStateValue.FALSE,
            observation_outcome=ObservationOutcome.TRUSTED_OBSERVATION,
        )
        == ScopeClassification.NON_ACTIONABLE_INELIGIBLE
    )
    assert (
        classify_scope(
            lifecycle_state=LifecycleState.TERMINAL,
            eligibility_state=TriStateValue.TRUE,
            observation_outcome=ObservationOutcome.TRUSTED_TERMINAL,
        )
        == ScopeClassification.RETAINED_AUDIT_ONLY
    )
    assert (
        classify_scope(
            lifecycle_state=LifecycleState.NON_TERMINAL,
            eligibility_state=TriStateValue.UNKNOWN,
            observation_outcome=ObservationOutcome.PARTIAL_EVIDENCE,
        )
        == ScopeClassification.PENDING_UNVERIFIED
    )
    assert (
        classify_scope(
            lifecycle_state=LifecycleState.NON_TERMINAL,
            eligibility_state=TriStateValue.UNKNOWN,
            observation_outcome=ObservationOutcome.TRUSTED_OBSERVATION,
        )
        == ScopeClassification.PENDING_UNVERIFIED
    )


def test_schedule_retry_due_uses_utc_z() -> None:
    due = schedule_retry_due(observed_at_utc_z="2026-09-15T12:00:00Z", interval_minutes=30)
    assert due == "2026-09-15T12:30:00Z"


def test_apply_recovery_result_updates_disposition() -> None:
    record = _record()
    recovered = apply_recovery_result(record, recovered=True, exhausted=False)
    exhausted = apply_recovery_result(record, recovered=False, exhausted=True)
    due = apply_recovery_result(record, recovered=False, exhausted=False)
    assert recovered.recovery_disposition == RecoveryDisposition.NONE
    assert exhausted.recovery_disposition == RecoveryDisposition.EXHAUSTED
    assert due.recovery_disposition == RecoveryDisposition.DUE
