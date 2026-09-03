"""Conflict-safe queue state transitions."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from agentic_devtools.cli.ci.reconciliation.models import (
    Claim,
    Lease,
    OperationStatus,
    QueueState,
    ReconciliationRecord,
    WorkItem,
    WorkItemStatus,
)


class ClaimConflictError(Exception):
    """Raised when a work item is already claimed or leased."""


class StaleCompletionError(Exception):
    """Raised when completing with a stale operation_id or recovery epoch."""


class LeaseExpiredError(Exception):
    """Raised when attempting to use an expired lease."""


def _matches_current_or_pending_revision(token_revision: int, state_revision: int) -> bool:
    """Return True when a token matches the current revision or the next saved revision."""
    return token_revision in {state_revision, state_revision + 1}


def claim_work_item(
    state: QueueState,
    pr_number: int,
    operation_id: str,
    claim_ttl_seconds: int = 300,
) -> tuple[QueueState, Claim]:
    """Acquire a claim on a work item."""
    if pr_number <= 0:
        raise ValueError(f"pr_number must be > 0, got {pr_number}")
    if not operation_id:
        raise ValueError("operation_id must not be empty")
    if claim_ttl_seconds <= 0:
        raise ValueError("claim_ttl_seconds must be > 0")
    item = state.items.get(pr_number)
    if item is None:
        raise KeyError(f"No work item for pr_number={pr_number}")
    if item.status != WorkItemStatus.QUEUED:
        raise ClaimConflictError(f"pr_number={pr_number} is already in status {item.status}")
    now = datetime.now(UTC)
    claim = Claim(
        claim_id=str(uuid4()),
        pr_number=pr_number,
        repo=state.repo,
        operation_id=operation_id,
        acquired_at=now,
        expires_at=now + timedelta(seconds=claim_ttl_seconds),
        revision=state.revision + 1,
    )
    updated_item = replace(
        item,
        status=WorkItemStatus.CLAIMED,
        claim_id=claim.claim_id,
        claimed_at=now,
        claim_expires_at=claim.expires_at,
        operation_id=operation_id,
        operation_status=OperationStatus.ACTIVE,
    )
    return replace(state, items={**state.items, pr_number: updated_item}), claim


def acquire_lease(
    state: QueueState,
    claim: Claim,
    lease_ttl_seconds: int = 600,
) -> tuple[QueueState, Lease]:
    """Convert a claim to a lease."""
    if lease_ttl_seconds <= 0:
        raise ValueError("lease_ttl_seconds must be > 0")
    item = state.items.get(claim.pr_number)
    if item is None:
        raise KeyError(f"No work item for pr_number={claim.pr_number}")
    if item.status != WorkItemStatus.CLAIMED or item.claim_id != claim.claim_id:
        raise ClaimConflictError(f"pr_number={claim.pr_number} is not claimable with claim {claim.claim_id}")
    now = datetime.now(UTC)
    if not _matches_current_or_pending_revision(claim.revision, state.revision):
        raise ClaimConflictError(f"claim revision mismatch: claim has {claim.revision}, state has {state.revision}")
    if item.claim_expires_at != claim.expires_at:
        raise ClaimConflictError("persisted claim expiry no longer matches the claim")
    if claim.expires_at <= now:
        raise ClaimConflictError(f"claim_id {claim.claim_id!r} has expired")
    lease = Lease(
        lease_id=str(uuid4()),
        claim_id=claim.claim_id,
        pr_number=claim.pr_number,
        repo=state.repo,
        operation_id=claim.operation_id,
        acquired_at=now,
        expires_at=now + timedelta(seconds=lease_ttl_seconds),
        revision=state.revision + 1,
        recovery_epoch=state.recovery_epoch,
    )
    updated_item = replace(
        item,
        status=WorkItemStatus.LEASED,
        lease_id=lease.lease_id,
        claim_expires_at=None,
        lease_expires_at=lease.expires_at,
    )
    return replace(state, items={**state.items, claim.pr_number: updated_item}), lease


def complete_work_item(
    state: QueueState,
    lease: Lease,
    operation_id: str,
    recovery_epoch: int,
) -> QueueState:
    """Mark a work item as completed."""
    now = datetime.now(UTC)
    if lease.operation_id != operation_id:
        raise StaleCompletionError(f"operation_id mismatch: lease has {lease.operation_id!r}, got {operation_id!r}")
    if lease.recovery_epoch != recovery_epoch:
        raise StaleCompletionError(f"recovery_epoch mismatch: lease has {lease.recovery_epoch}, got {recovery_epoch}")
    if recovery_epoch != state.recovery_epoch:
        raise StaleCompletionError(f"recovery_epoch mismatch: state has {state.recovery_epoch}, got {recovery_epoch}")
    item = state.items.get(lease.pr_number)
    if item is None:
        raise KeyError(f"No work item for pr_number={lease.pr_number}")
    if item.status != WorkItemStatus.LEASED or item.lease_id != lease.lease_id:
        raise StaleCompletionError("lease no longer owns the work item")
    if item.lease_expires_at is None:
        raise StaleCompletionError(f"persisted lease expiry is missing for lease_id {lease.lease_id!r}")
    if item.lease_expires_at != lease.expires_at:
        raise StaleCompletionError("persisted lease expiry no longer matches the lease")
    if item.lease_expires_at <= now:
        raise LeaseExpiredError(f"lease_id {lease.lease_id!r} has expired in persisted state")
    if item.operation_id != operation_id or item.operation_status != OperationStatus.ACTIVE:
        raise StaleCompletionError("operation is no longer active")
    pending_change_id = item.pending_change_id.strip()
    if pending_change_id:
        updated_item = replace(
            item,
            status=WorkItemStatus.QUEUED,
            change_id=pending_change_id,
            pending_change_id="",
            due_at=now,
            claim_id="",
            lease_id="",
            claim_expires_at=None,
            lease_expires_at=None,
            claimed_at=None,
            operation_status=OperationStatus.ACTIVE,
            completed_at=None,
        )
        return replace(state, items={**state.items, lease.pr_number: updated_item})
    updated_item = replace(
        item,
        status=WorkItemStatus.COMPLETED,
        operation_status=OperationStatus.COMPLETED,
        completed_at=now,
    )
    return replace(state, items={**state.items, lease.pr_number: updated_item})


def reclaim_expired(
    state: QueueState,
    now: datetime | None = None,
    max_reclaims: int | None = None,
) -> tuple[QueueState, list[int]]:
    """Reclaim expired leases and stale claims."""
    if now is None:
        now = datetime.now(UTC)
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    if max_reclaims is not None and max_reclaims <= 0:
        raise ValueError("max_reclaims must be > 0")
    reclaimed: list[int] = []
    new_items = dict(state.items)
    for pr_number, item in state.items.items():
        if max_reclaims is not None and len(reclaimed) >= max_reclaims:
            break
        if item.status == WorkItemStatus.LEASED and item.lease_expires_at is not None:
            if item.lease_expires_at <= now:
                new_items[pr_number] = replace(
                    item,
                    status=WorkItemStatus.QUEUED,
                    operation_status=OperationStatus.EXPIRED,
                    claim_id="",
                    lease_id="",
                    claim_expires_at=None,
                    lease_expires_at=None,
                    claimed_at=None,
                )
                reclaimed.append(pr_number)
        elif item.status == WorkItemStatus.CLAIMED:
            claim_expires_at = _resolve_claim_expiry(item)
            if claim_expires_at is not None and claim_expires_at <= now:
                new_items[pr_number] = replace(
                    item,
                    status=WorkItemStatus.QUEUED,
                    operation_status=OperationStatus.EXPIRED,
                    claim_id="",
                    claim_expires_at=None,
                    claimed_at=None,
                )
                reclaimed.append(pr_number)
    return replace(state, items=new_items), reclaimed


def _resolve_claim_expiry(item: WorkItem) -> datetime | None:
    """Return the persisted claim expiry, or a legacy fallback for older states."""
    if item.claim_expires_at is not None:
        return item.claim_expires_at
    if item.claimed_at is None:
        return None
    return item.claimed_at + timedelta(seconds=300)


def quarantine_transition(
    state: QueueState,
    pr_number: int,
    reason: str,
) -> QueueState:
    """Move a work item to QUARANTINED status."""
    if not reason:
        raise ValueError("reason must not be empty")
    item = state.items.get(pr_number)
    if item is None:
        raise KeyError(f"No work item for pr_number={pr_number}")
    now = datetime.now(UTC)
    updated_item = replace(item, status=WorkItemStatus.QUARANTINED)
    record = ReconciliationRecord(
        record_id=str(uuid4()),
        repo=state.repo,
        run_id="queue_transition",
        started_at=now,
        completed_at=now,
        provider_status="quarantined",
        message=reason,
    )
    return replace(
        state,
        items={**state.items, pr_number: updated_item},
        records=[*state.records, record],
    )
