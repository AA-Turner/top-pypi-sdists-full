"""Trusted invalidation processing for stale or superseded work state."""

from __future__ import annotations

from dataclasses import replace

from agentic_devtools.cli.ci.reconciliation.identifiers import deterministic_id
from agentic_devtools.cli.ci.reconciliation.models import (
    InvalidationEvent,
    InvalidationReason,
    PullRequestWorkLedger,
    ScopeClassification,
    TriStateValue,
)


def invalidate_ledger(
    *,
    ledger: PullRequestWorkLedger,
    reason: InvalidationReason,
    invalidated_at_utc_z: str,
    details: str,
) -> PullRequestWorkLedger:
    """Invalidate current actionable state while preserving immutable history."""
    latest_observation_id = ledger.observations[-1].observation_id if ledger.observations else ""
    latest_decision_id = ledger.decisions[-1].decision_id if ledger.decisions else ""
    event = InvalidationEvent(
        invalidation_id=deterministic_id(
            "invalidation", ledger.record_id, reason.value, invalidated_at_utc_z, length=24
        ),
        reason=reason,
        invalidated_at_utc_z=invalidated_at_utc_z,
        observation_id=latest_observation_id,
        decision_id=latest_decision_id,
        details=details,
    )
    superseded = ledger.superseded_decision_ids
    if latest_decision_id:
        superseded = (*superseded, latest_decision_id)
    return replace(
        ledger,
        current_work_state="invalidated",
        action_eligibility=TriStateValue.UNKNOWN,
        invalidations=(*ledger.invalidations, event),
        superseded_decision_ids=superseded,
    )


def unavailable_non_terminal_scope() -> ScopeClassification:
    """Return pending-unverified scope for temporary evidence unavailability."""
    return ScopeClassification.PENDING_UNVERIFIED
