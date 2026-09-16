"""Candidate inventory projection and bounded traversal helpers."""

from __future__ import annotations

from dataclasses import dataclass

from agentic_devtools.cli.ci.reconciliation.models import (
    CandidateInventoryRecord,
    LifecycleState,
    ObservationOutcome,
    RecoveryDisposition,
    ScopeClassification,
    TriStateValue,
)


@dataclass(frozen=True)
class InventoryTraversal:
    """Durable traversal cursor and bounded progress state."""

    cursor: str | None = None
    page_count: int = 0
    full_scan_complete: bool = False

    def advance(self, *, next_cursor: str | None) -> InventoryTraversal:
        return InventoryTraversal(
            cursor=next_cursor,
            page_count=self.page_count + 1,
            full_scan_complete=next_cursor is None,
        )


@dataclass(frozen=True)
class CandidateInventoryProjection:
    """Lightweight projection container for candidate inventory state."""

    records: dict[str, CandidateInventoryRecord]

    def upsert(self, record: CandidateInventoryRecord) -> CandidateInventoryProjection:
        updated = dict(self.records)
        updated[record.record_id] = record
        return CandidateInventoryProjection(records=updated)


def classify_scope(
    *,
    lifecycle_state: LifecycleState,
    eligibility_state: TriStateValue,
    observation_outcome: ObservationOutcome,
) -> ScopeClassification:
    """Classify current scope using lifecycle, eligibility, and trusted outcome."""
    if lifecycle_state in {LifecycleState.TERMINAL, LifecycleState.INACCESSIBLE} and observation_outcome in {
        ObservationOutcome.TRUSTED_TERMINAL,
        ObservationOutcome.TRUSTED_INACCESSIBLE,
    }:
        return ScopeClassification.RETAINED_AUDIT_ONLY
    if observation_outcome not in {
        ObservationOutcome.TRUSTED_OBSERVATION,
        ObservationOutcome.TRUSTED_TERMINAL,
        ObservationOutcome.TRUSTED_INACCESSIBLE,
    }:
        return ScopeClassification.PENDING_UNVERIFIED
    if eligibility_state == TriStateValue.TRUE:
        return ScopeClassification.ACTIVE
    if eligibility_state == TriStateValue.FALSE:
        return ScopeClassification.NON_ACTIONABLE_INELIGIBLE
    return ScopeClassification.PENDING_UNVERIFIED


def schedule_retry_due(*, observed_at_utc_z: str, interval_minutes: int = 30) -> str:
    """Return persisted due timestamp for the next non-terminal retry attempt."""
    from datetime import UTC, timedelta

    observed_at = __import__("datetime").datetime.fromisoformat(observed_at_utc_z.replace("Z", "+00:00"))
    due_at = observed_at.astimezone(UTC) + timedelta(minutes=interval_minutes)
    return due_at.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def apply_recovery_result(
    record: CandidateInventoryRecord,
    *,
    recovered: bool,
    exhausted: bool,
) -> CandidateInventoryRecord:
    """Apply retained-record recovery transition metadata without duplication."""
    disposition = record.recovery_disposition
    if recovered:
        disposition = RecoveryDisposition.NONE
    elif exhausted:
        disposition = RecoveryDisposition.EXHAUSTED
    else:
        disposition = RecoveryDisposition.DUE
    return CandidateInventoryRecord(
        record_id=record.record_id,
        repo=record.repo,
        pr_number=record.pr_number,
        target_branch=record.target_branch,
        lifecycle_state=record.lifecycle_state,
        scope_classification=record.scope_classification,
        eligibility_state=record.eligibility_state,
        observation_outcome=record.observation_outcome,
        observed_at_utc_z=record.observed_at_utc_z,
        observed_monotonic_seconds=record.observed_monotonic_seconds,
        next_due_at_utc_z=record.next_due_at_utc_z,
        recovery_epoch=record.recovery_epoch,
        recovery_attempt_count=record.recovery_attempt_count + (0 if recovered else 1),
        recovery_disposition=disposition,
        exhaustion_metadata=record.exhaustion_metadata,
        finality_metadata=record.finality_metadata,
    )
