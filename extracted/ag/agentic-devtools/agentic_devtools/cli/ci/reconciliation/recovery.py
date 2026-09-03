"""Recovery primitives for bounded rehydration, lease reclamation, and quarantine epochs."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.reconciliation.models import (
    OperationStatus,
    QuarantineRecord,
    QueueState,
    ReconciliationRecord,
    RecoveryEpoch,
    WorkItemStatus,
)
from agentic_devtools.cli.ci.reconciliation.queue_store import QueueStoreError
from agentic_devtools.cli.ci.reconciliation.queue_transitions import reclaim_expired


class RecoveryExhaustedError(QueueStoreError):
    """Raised when authoritative rehydration exhausts its bounded attempts."""

    def __init__(self, state: QueueState, message: str) -> None:
        super().__init__(message)
        self.state = state


def confirm_recovery(
    state: QueueState,
    *,
    quarantine_id: str,
    confirmed_by: str,
) -> tuple[QueueState, RecoveryEpoch]:
    """Confirm operator-approved recovery from quarantine and advance the recovery epoch.

    Args:
        state: Current queue state with at least one quarantine record.
        quarantine_id: Identifier of the quarantine to recover from.
        confirmed_by: Identity string of the operator confirming recovery.

    Returns:
        Tuple of (updated_state, new_recovery_epoch).

    Raises:
        KeyError: No quarantine record with the given quarantine_id.
        ValueError: The confirming identity is empty.
    """
    if not confirmed_by.strip():
        raise ValueError("confirmed_by must not be empty")
    matching = next((q for q in state.quarantines if q.quarantine_id == quarantine_id), None)
    if matching is None:
        raise KeyError(f"Unknown quarantine_id={quarantine_id!r}")
    active_items = [
        item.pr_number
        for item in state.items.values()
        if item.status in (WorkItemStatus.CLAIMED, WorkItemStatus.LEASED)
    ]
    if active_items:
        raise ValueError(f"Cannot confirm recovery while active operations exist: {active_items!r}")
    now = datetime.now(UTC)
    new_epoch_number = state.recovery_epoch + 1
    epoch = RecoveryEpoch(
        epoch_id=new_epoch_number,
        repo=state.repo,
        confirmed_at=now,
        confirmed_by=confirmed_by,
        quarantine_id=quarantine_id,
        prior_epoch=state.recovery_epoch,
    )
    updated_quarantines = [
        replace(q, rehydration_attempted=True) if q.quarantine_id == quarantine_id else q for q in state.quarantines
    ]
    return replace(state, recovery_epoch=new_epoch_number, quarantines=updated_quarantines), epoch


def reclaim_leases(
    state: QueueState,
    *,
    now_utc: datetime | None = None,
    max_reclaims: int | None = None,
) -> QueueState:
    """Reclaim expired leases and return updated state.

    Args:
        state: Current queue state.
        now_utc: Timezone-aware current time; defaults to ``datetime.now(UTC)``.

    Returns:
        Updated state with expired leases reclaimed.

    Raises:
        ValueError: ``now_utc`` is naive.
    """
    current = datetime.now(UTC) if now_utc is None else now_utc
    limit = config.MAX_LEASE_RECLAIMS_PER_CYCLE if max_reclaims is None else max_reclaims
    updated, _ = reclaim_expired(state, current, max_reclaims=limit)
    expired_items = _expired_inflight_pr_numbers(updated, current)
    has_expired_items = bool(expired_items)
    if not has_expired_items:
        return replace(updated, lease_reclaim_cycles=0, reclamation_limit_reached=False)
    cycles = state.lease_reclaim_cycles + 1 if has_expired_items else 0
    limit_reached = has_expired_items and cycles >= config.MAX_LEASE_RECLAIM_CYCLES
    if limit_reached:
        quarantined_items = dict(updated.items)
        for pr_number in expired_items:
            item = quarantined_items[pr_number]
            quarantined_items[pr_number] = replace(
                item,
                status=WorkItemStatus.QUARANTINED,
                operation_status=OperationStatus.EXPIRED,
                claim_id="",
                lease_id="",
                claim_expires_at=None,
                lease_expires_at=None,
                claimed_at=None,
            )
        return _append_record(
            replace(
                updated,
                items=quarantined_items,
                lease_reclaim_cycles=0,
                reclamation_limit_reached=False,
            ),
            "alertable",
            f"lease reclamation exhausted for pr_numbers={expired_items!r}",
        )
    return replace(
        updated,
        lease_reclaim_cycles=cycles,
        reclamation_limit_reached=limit_reached,
    )


def rehydrate_state(
    state: QueueState,
    authoritative_loader: Callable[[], QueueState],
    *,
    max_attempts: int | None = None,
) -> QueueState:
    """Rebuild state from an authoritative source within a finite attempt budget.

    A successful rehydration preserves quarantine evidence, marks it as attempted,
    and advances the recovery epoch so the recovered state can be saved again.
    Failed attempts are recorded as a terminal alert once the budget is exhausted;
    the last exception is then re-raised.
    """
    attempts = config.MAX_RECOVERY_ATTEMPTS if max_attempts is None else max_attempts
    if attempts <= 0:
        raise ValueError("max_attempts must be > 0")
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            rebuilt = authoritative_loader()
            if rebuilt.repo != state.repo or rebuilt.state_ref != state.state_ref:
                raise ValueError("authoritative state identity does not match quarantined state")
            updated_quarantines = [replace(record, rehydration_attempted=True) for record in state.quarantines]
            return replace(
                rebuilt,
                recovery_epoch=state.recovery_epoch + 1,
                quarantines=updated_quarantines,
            )
        except Exception as exc:
            last_error = exc
    assert last_error is not None
    alerted = _terminal_alert(state, "rehydration_exhausted", str(last_error))
    raise RecoveryExhaustedError(alerted, "Authoritative state rehydration exhausted") from last_error


def enforce_retry_limit(
    state: QueueState,
    pr_number: int,
    *,
    max_attempts: int | None = None,
) -> QueueState:
    """Increment an item's retry count and quarantine it at the configured limit."""
    limit = config.MAX_RETRY_ATTEMPTS if max_attempts is None else max_attempts
    if limit <= 0:
        raise ValueError("max_attempts must be > 0")
    item = state.items.get(pr_number)
    if item is None:
        raise KeyError(f"No work item for pr_number={pr_number}")
    updated_item = replace(item, retry_count=item.retry_count + 1)
    updated = replace(state, items={**state.items, pr_number: updated_item})
    if updated_item.retry_count < limit:
        return updated
    quarantined = replace(
        updated,
        items={**updated.items, pr_number: replace(updated_item, status=WorkItemStatus.QUARANTINED)},
    )
    return _terminal_alert(quarantined, "retry_limit_exhausted", f"pr_number={pr_number}")


def record_provider_failure(
    state: QueueState,
    *,
    failure_started_at: datetime,
    now_utc: datetime | None = None,
) -> QueueState:
    """Record a provider failure and emit a terminal alert after its duration limit."""
    now = datetime.now(UTC) if now_utc is None else now_utc
    if failure_started_at.tzinfo is None or now.tzinfo is None:
        raise ValueError("failure timestamps must be timezone-aware")
    duration = (now - failure_started_at).total_seconds()
    status = "alertable" if duration >= config.MAX_PROVIDER_FAILURE_DURATION else "provider_failure"
    return _append_record(state, status, f"provider failure duration={duration:.1f}s")


def handle_pagination_exhaustion(state: QueueState, *, cursor: str = "") -> QueueState:
    """Persist an alertable record when pagination reaches its configured bound."""
    return _append_record(state, "alertable", f"pagination exhausted at cursor={cursor!r}")


def _append_record(state: QueueState, provider_status: str, message: str) -> QueueState:
    record = ReconciliationRecord(
        record_id=str(uuid4()),
        repo=state.repo,
        run_id="recovery",
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        provider_status=provider_status,
        message=message,
        unknown_outcomes=(),
    )
    return replace(state, records=[*state.records, record])


def _expired_inflight_pr_numbers(state: QueueState, current: datetime) -> list[int]:
    return [
        pr_number
        for pr_number, item in state.items.items()
        if (
            item.status == WorkItemStatus.LEASED
            and item.lease_expires_at is not None
            and item.lease_expires_at <= current
        )
        or (
            item.status == WorkItemStatus.CLAIMED
            and (
                item.claim_expires_at is not None
                and item.claim_expires_at <= current
                or (
                    item.claim_expires_at is None
                    and item.claimed_at is not None
                    and (current - item.claimed_at).total_seconds() > 300
                )
            )
        )
    ]


def _terminal_alert(state: QueueState, reason: str, evidence: str) -> QueueState:
    """Persist a terminal alert and immutable evidence for the unsafe state."""
    quarantine = QuarantineRecord(
        quarantine_id=str(uuid4()),
        repo=state.repo,
        reason=reason,
        evidence_digest=hashlib.sha256(evidence.encode("utf-8")).hexdigest(),
        evidence=evidence,
        quarantined_at=datetime.now(UTC),
        recovery_epoch=state.recovery_epoch,
    )
    return _append_record(
        replace(state, quarantines=[*state.quarantines, quarantine]),
        "alertable",
        f"{reason}: {evidence}",
    )
