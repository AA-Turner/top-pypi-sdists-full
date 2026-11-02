"""Tests for trusted reconciliation model primitives."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.models import (
    CandidateInventoryRecord,
    DynamicCondition,
    LifecycleState,
    ObservationOutcome,
    RecoveryDisposition,
    ScopeClassification,
    TriStateValue,
)


def test_enums_expose_expected_values() -> None:
    assert LifecycleState.NON_TERMINAL.value == "non_terminal"
    assert ScopeClassification.RETAINED_AUDIT_ONLY.value == "retained_audit_only"
    assert TriStateValue.UNKNOWN.value == "unknown"
    assert ObservationOutcome.TRUSTED_INACCESSIBLE.value == "trusted_inaccessible"


def test_candidate_inventory_record_fields() -> None:
    record = CandidateInventoryRecord(
        record_id="owner/repo#1",
        repo="owner/repo",
        pr_number=1,
        target_branch="main",
        lifecycle_state=LifecycleState.NON_TERMINAL,
        scope_classification=ScopeClassification.PENDING_UNVERIFIED,
        eligibility_state=TriStateValue.UNKNOWN,
        observation_outcome=ObservationOutcome.PARTIAL_EVIDENCE,
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=1.0,
        recovery_disposition=RecoveryDisposition.NONE,
    )
    assert record.pr_number == 1


def test_dynamic_condition_defaults() -> None:
    condition = DynamicCondition(
        name="target_branch_match",
        value=TriStateValue.TRUE,
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=2.0,
    )
    assert condition.source == "github"
