"""Tests for queue state transitions."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.models import (
    OperationStatus,
    QueueState,
    WorkItem,
    WorkItemStatus,
)
from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore
from agentic_devtools.cli.ci.reconciliation.queue_transitions import (
    ClaimConflictError,
    LeaseExpiredError,
    StaleCompletionError,
    acquire_lease,
    claim_work_item,
    complete_work_item,
    quarantine_transition,
    reclaim_expired,
)


def _make_state(items: dict[int, WorkItem] | None = None) -> QueueState:
    return QueueState(
        repo="owner/repo",
        revision=0,
        items=items or {},
        records=[],
        quarantines=[],
    )


def _make_item(
    pr_number: int = 1,
    status: WorkItemStatus = WorkItemStatus.QUEUED,
) -> WorkItem:
    return WorkItem(
        pr_number=pr_number,
        repo="owner/repo",
        change_id="abc",
        eligibility="eligible",
        due_at=None,
        status=status,
    )


def test_claim_work_item_success() -> None:
    state = _make_state({1: _make_item(1)})
    new_state, claim = claim_work_item(state, 1, "op1")
    assert new_state.items[1].status == WorkItemStatus.CLAIMED
    assert new_state.items[1].claim_id == claim.claim_id
    assert new_state.items[1].claim_expires_at == claim.expires_at
    assert claim.operation_id == "op1"
    assert claim.revision == state.revision + 1


def test_claim_conflict_raises() -> None:
    state = _make_state({1: _make_item(1, WorkItemStatus.CLAIMED)})
    with pytest.raises(ClaimConflictError):
        claim_work_item(state, 1, "op1")


def test_acquire_lease_success() -> None:
    state = _make_state({1: _make_item(1)})
    claimed_state, claim = claim_work_item(state, 1, "op1")
    new_state, lease = acquire_lease(claimed_state, claim)
    assert new_state.items[1].status == WorkItemStatus.LEASED
    assert new_state.items[1].lease_id == lease.lease_id
    assert lease.revision == claimed_state.revision + 1


def test_complete_work_item_success() -> None:
    state = _make_state({1: _make_item(1)})
    claimed_state, claim = claim_work_item(state, 1, "op1")
    leased_state, lease = acquire_lease(claimed_state, claim)
    new_state = complete_work_item(replace(leased_state, revision=lease.revision), lease, "op1", 0)
    assert new_state.items[1].status == WorkItemStatus.COMPLETED
    assert new_state.items[1].operation_status == OperationStatus.COMPLETED


def test_complete_work_item_accepts_saved_and_reloaded_lease_revision() -> None:
    store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
    state = store.load()
    state.items[1] = _make_item(1)
    claimed_state, claim = claim_work_item(state, 1, "op1")
    saved_claimed = store.save(claimed_state, expected_revision=state.revision)
    leased_state, lease = acquire_lease(saved_claimed, claim)
    store.save(leased_state, expected_revision=saved_claimed.revision)
    reloaded = store.load()
    completed = complete_work_item(reloaded, lease, "op1", reloaded.recovery_epoch)
    assert completed.items[1].status == WorkItemStatus.COMPLETED


def test_complete_work_item_promotes_pending_change_to_queued_due_work() -> None:
    state = _make_state({1: _make_item(1)})
    claimed_state, claim = claim_work_item(state, 1, "op1")
    leased_state, lease = acquire_lease(claimed_state, claim)
    leased_state = replace(
        leased_state,
        revision=lease.revision,
        items={
            **leased_state.items,
            1: replace(leased_state.items[1], pending_change_id="new-head-sha"),
        },
    )

    new_state = complete_work_item(leased_state, lease, "op1", 0)

    updated = new_state.items[1]
    assert updated.status == WorkItemStatus.QUEUED
    assert updated.change_id == "new-head-sha"
    assert updated.pending_change_id == ""
    assert updated.operation_status == OperationStatus.ACTIVE
    assert updated.due_at is not None


def test_stale_completion_raises() -> None:
    state = _make_state({1: _make_item(1)})
    claimed_state, claim = claim_work_item(state, 1, "op1")
    leased_state, lease = acquire_lease(claimed_state, claim)
    with pytest.raises(StaleCompletionError):
        complete_work_item(replace(leased_state, revision=lease.revision), lease, "op_wrong", 0)


def test_reclaim_expired_items() -> None:
    now = datetime.now(UTC)
    expired_lease_at = now - timedelta(seconds=10)
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="abc",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.LEASED,
        claim_id="c1",
        lease_id="l1",
        lease_expires_at=expired_lease_at,
    )
    state = _make_state({1: item})
    new_state, reclaimed = reclaim_expired(state, now=now)
    assert 1 in reclaimed
    assert new_state.items[1].status == WorkItemStatus.QUEUED
    assert new_state.items[1].operation_status == OperationStatus.EXPIRED


def test_claim_invalid_pr_number_raises() -> None:
    state = _make_state()
    with pytest.raises(ValueError, match="pr_number"):
        claim_work_item(state, 0, "op1")


def test_claim_empty_operation_id_raises() -> None:
    state = _make_state({1: _make_item(1)})
    with pytest.raises(ValueError, match="operation_id"):
        claim_work_item(state, 1, "")


def test_claim_missing_item_raises() -> None:
    state = _make_state()
    with pytest.raises(KeyError):
        claim_work_item(state, 99, "op1")


def test_acquire_lease_missing_item_raises() -> None:
    from agentic_devtools.cli.ci.reconciliation.models import Claim

    now = datetime.now(UTC)
    claim = Claim(
        claim_id="c1",
        pr_number=99,
        repo="owner/repo",
        operation_id="op1",
        acquired_at=now,
        expires_at=now + timedelta(seconds=300),
    )
    state = _make_state()
    with pytest.raises(KeyError):
        acquire_lease(state, claim)


def test_acquire_lease_wrong_claim_id_raises() -> None:
    state = _make_state({1: _make_item(1)})
    claimed_state, claim = claim_work_item(state, 1, "op1")
    from agentic_devtools.cli.ci.reconciliation.models import Claim

    now = datetime.now(UTC)
    wrong_claim = Claim(
        claim_id="wrong",
        pr_number=1,
        repo="owner/repo",
        operation_id="op1",
        acquired_at=now,
        expires_at=now + timedelta(seconds=300),
    )
    with pytest.raises(ClaimConflictError):
        acquire_lease(claimed_state, wrong_claim)


def test_complete_work_item_expired_lease_raises() -> None:
    from agentic_devtools.cli.ci.reconciliation.models import Lease

    now = datetime.now(UTC)
    lease = Lease(
        lease_id="l1",
        claim_id="c1",
        pr_number=1,
        repo="owner/repo",
        operation_id="op1",
        acquired_at=now - timedelta(seconds=700),
        expires_at=now - timedelta(seconds=1),
    )
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="abc",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.LEASED,
        claim_id="c1",
        lease_id="l1",
        lease_expires_at=now - timedelta(seconds=1),
    )
    state = _make_state({1: item})
    with pytest.raises(LeaseExpiredError):
        complete_work_item(state, lease, "op1", 0)


def test_complete_work_item_stale_epoch_raises() -> None:
    state = _make_state({1: _make_item(1)})
    claimed_state, claim = claim_work_item(state, 1, "op1")
    leased_state, lease = acquire_lease(claimed_state, claim)
    with pytest.raises(StaleCompletionError):
        complete_work_item(leased_state, lease, "op1", 999)


def test_complete_work_item_rejects_state_epoch_advance() -> None:
    from dataclasses import replace as dc_replace

    state = _make_state({1: _make_item(1)})
    claimed_state, claim = claim_work_item(state, 1, "op1")
    leased_state, lease = acquire_lease(claimed_state, claim)
    advanced_state = dc_replace(leased_state, recovery_epoch=1)
    with pytest.raises(StaleCompletionError, match="state has 1"):
        complete_work_item(advanced_state, lease, "op1", 0)


def test_complete_work_item_rejects_mismatched_persisted_lease_expiry() -> None:
    from dataclasses import replace as dc_replace

    state = _make_state({1: _make_item(1)})
    claimed_state, claim = claim_work_item(state, 1, "op1")
    leased_state, lease = acquire_lease(claimed_state, claim)
    shifted_item = dc_replace(leased_state.items[1], lease_expires_at=lease.expires_at + timedelta(seconds=30))
    shifted_state = dc_replace(leased_state, revision=lease.revision, items={1: shifted_item})
    with pytest.raises(StaleCompletionError, match="lease expiry no longer matches"):
        complete_work_item(shifted_state, lease, "op1", leased_state.recovery_epoch)


def test_complete_work_item_rejects_expired_persisted_lease() -> None:
    from agentic_devtools.cli.ci.reconciliation.models import Lease

    now = datetime.now(UTC)
    lease = Lease(
        lease_id="l1",
        claim_id="c1",
        pr_number=1,
        repo="owner/repo",
        operation_id="op1",
        acquired_at=now - timedelta(seconds=600),
        expires_at=now - timedelta(seconds=1),
    )
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="abc",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.LEASED,
        claim_id="c1",
        lease_id="l1",
        lease_expires_at=lease.expires_at,
        operation_id="op1",
        operation_status=OperationStatus.ACTIVE,
    )
    expired_state = _make_state({1: item})
    with pytest.raises(LeaseExpiredError, match="persisted state"):
        complete_work_item(expired_state, lease, "op1", 0)


def test_complete_work_item_rejects_missing_persisted_lease_expiry() -> None:
    from dataclasses import replace as dc_replace

    state = _make_state({1: _make_item(1)})
    claimed_state, claim = claim_work_item(state, 1, "op1")
    leased_state, lease = acquire_lease(claimed_state, claim)
    missing_expiry_item = dc_replace(leased_state.items[1], lease_expires_at=None)
    missing_expiry_state = dc_replace(leased_state, revision=lease.revision, items={1: missing_expiry_item})
    with pytest.raises(StaleCompletionError, match="lease expiry is missing"):
        complete_work_item(missing_expiry_state, lease, "op1", leased_state.recovery_epoch)


def test_reclaim_expired_naive_now_raises() -> None:
    state = _make_state()
    with pytest.raises(ValueError, match="timezone"):
        reclaim_expired(state, now=datetime(2024, 1, 1))


def test_reclaim_expired_no_expiry_no_reclaim() -> None:
    """Items with no lease_expires_at are not reclaimed."""
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="abc",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.LEASED,
        claim_id="c1",
        lease_id="l1",
        lease_expires_at=None,
    )
    state = _make_state({1: item})
    new_state, reclaimed = reclaim_expired(state, now=datetime.now(UTC))
    assert reclaimed == []


def test_reclaim_expired_stale_claimed_items() -> None:
    now = datetime.now(UTC)
    old_claimed_at = now - timedelta(seconds=400)
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="abc",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.CLAIMED,
        claim_id="c1",
        claimed_at=old_claimed_at,
        claim_expires_at=old_claimed_at + timedelta(seconds=300),
    )
    state = _make_state({1: item})
    new_state, reclaimed = reclaim_expired(state, now=now)
    assert 1 in reclaimed
    assert new_state.items[1].status == WorkItemStatus.QUEUED
    assert new_state.items[1].operation_status == OperationStatus.EXPIRED


def test_reclaim_expired_honors_persisted_claim_expiry() -> None:
    now = datetime.now(UTC)
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="abc",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.CLAIMED,
        claim_id="c1",
        claimed_at=now - timedelta(seconds=400),
        claim_expires_at=now + timedelta(seconds=60),
        operation_id="op1",
    )
    state = _make_state({1: item})
    new_state, reclaimed = reclaim_expired(state, now=now)
    assert reclaimed == []
    assert new_state.items[1].status == WorkItemStatus.CLAIMED


def test_reclaim_expired_claim_without_any_expiry_is_left_unchanged() -> None:
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="abc",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.CLAIMED,
        claim_id="c1",
        claimed_at=None,
        claim_expires_at=None,
        operation_id="op1",
    )
    state = _make_state({1: item})
    new_state, reclaimed = reclaim_expired(state, now=datetime.now(UTC))
    assert reclaimed == []
    assert new_state.items[1].status == WorkItemStatus.CLAIMED


def test_quarantine_transition_success() -> None:
    state = _make_state({1: _make_item(1)})
    new_state = quarantine_transition(state, 1, "bad state")
    assert new_state.items[1].status == WorkItemStatus.QUARANTINED
    assert len(new_state.records) == 1
    assert new_state.records[0].provider_status == "quarantined"
    assert new_state.records[0].message == "bad state"


def test_quarantine_transition_empty_reason_raises() -> None:
    state = _make_state({1: _make_item(1)})
    with pytest.raises(ValueError, match="reason"):
        quarantine_transition(state, 1, "")


def test_quarantine_transition_missing_item_raises() -> None:
    state = _make_state()
    with pytest.raises(KeyError):
        quarantine_transition(state, 99, "bad")


def test_complete_work_item_missing_item_raises() -> None:
    from agentic_devtools.cli.ci.reconciliation.models import Lease

    now = datetime.now(UTC)
    lease = Lease(
        lease_id="l1",
        claim_id="c1",
        pr_number=99,
        repo="owner/repo",
        operation_id="op1",
        acquired_at=now,
        expires_at=now + timedelta(seconds=600),
    )
    state = _make_state()
    with pytest.raises(KeyError):
        complete_work_item(state, lease, "op1", 0)


def test_reclaim_expired_default_now() -> None:
    """reclaim_expired with no 'now' uses datetime.now(UTC) internally."""
    state = _make_state()
    new_state, reclaimed = reclaim_expired(state)
    assert reclaimed == []


def test_reclaim_non_expired_leased_item_not_reclaimed() -> None:
    """Leased item with future expiry is not reclaimed."""
    now = datetime.now(UTC)
    future_expiry = now + timedelta(seconds=600)
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="abc",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.LEASED,
        claim_id="c1",
        lease_id="l1",
        lease_expires_at=future_expiry,
    )
    state = _make_state({1: item})
    new_state, reclaimed = reclaim_expired(state, now=now)
    assert reclaimed == []
    assert new_state.items[1].status == WorkItemStatus.LEASED


def test_reclaim_fresh_claimed_item_not_reclaimed() -> None:
    """Recently claimed item (age < 300s) is not reclaimed."""
    now = datetime.now(UTC)
    recent_claimed_at = now - timedelta(seconds=100)
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="abc",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.CLAIMED,
        claim_id="c1",
        claimed_at=recent_claimed_at,
    )
    state = _make_state({1: item})
    new_state, reclaimed = reclaim_expired(state, now=now)
    assert reclaimed == []
    assert new_state.items[1].status == WorkItemStatus.CLAIMED


def test_reclaim_expired_rejects_non_positive_limit() -> None:
    """A configured reclamation limit must be positive."""
    with pytest.raises(ValueError, match="max_reclaims"):
        reclaim_expired(_make_state(), now=datetime.now(UTC), max_reclaims=0)


def test_reclaim_expired_stops_at_limit() -> None:
    """Only the configured number of expired items are reclaimed per cycle."""
    now = datetime.now(UTC)
    items = {
        number: WorkItem(
            pr_number=number,
            repo="owner/repo",
            change_id=f"change-{number}",
            eligibility="eligible",
            due_at=None,
            status=WorkItemStatus.LEASED,
            claim_id=f"claim-{number}",
            lease_id=f"lease-{number}",
            operation_id=f"operation-{number}",
            lease_expires_at=now - timedelta(seconds=1),
        )
        for number in (1, 2)
    }

    new_state, reclaimed = reclaim_expired(_make_state(items), now=now, max_reclaims=1)

    assert reclaimed == [1]
    assert new_state.items[1].status == WorkItemStatus.QUEUED
    assert new_state.items[2].status == WorkItemStatus.LEASED


# ── Additional coverage tests ─────────────────────────────────────────────


def test_claim_zero_ttl_raises() -> None:
    """claim_ttl_seconds <= 0 raises ValueError."""
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="c1",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.QUEUED,
    )
    state = _make_state({1: item})
    with pytest.raises(ValueError, match="claim_ttl_seconds"):
        claim_work_item(state, 1, "op1", claim_ttl_seconds=0)


def test_acquire_lease_zero_ttl_raises() -> None:
    """lease_ttl_seconds <= 0 raises ValueError."""
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="c1",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.QUEUED,
    )
    state = _make_state({1: item})
    state2, claim = claim_work_item(state, 1, "op1")
    with pytest.raises(ValueError, match="lease_ttl_seconds"):
        acquire_lease(state2, claim, lease_ttl_seconds=0)


def test_acquire_lease_rejects_expired_claim() -> None:
    from dataclasses import replace as dc_replace

    state = _make_state({1: _make_item(1)})
    state2, claim = claim_work_item(state, 1, "op1")
    expired_claim = dc_replace(claim, expires_at=datetime.now(UTC) - timedelta(seconds=1))
    state2.items[1] = dc_replace(state2.items[1], claim_expires_at=expired_claim.expires_at)
    with pytest.raises(ClaimConflictError, match="expired"):
        acquire_lease(state2, expired_claim)


def test_acquire_lease_rejects_revision_mismatch() -> None:
    from dataclasses import replace as dc_replace

    state = _make_state({1: _make_item(1)})
    state2, claim = claim_work_item(state, 1, "op1")
    stale_claim = dc_replace(claim, revision=claim.revision + 1)
    with pytest.raises(ClaimConflictError, match="revision mismatch"):
        acquire_lease(state2, stale_claim)


def test_acquire_lease_rejects_persisted_claim_expiry_mismatch() -> None:
    from dataclasses import replace as dc_replace

    state = _make_state({1: _make_item(1)})
    state2, claim = claim_work_item(state, 1, "op1")
    tampered_item = dc_replace(state2.items[1], claim_expires_at=claim.expires_at + timedelta(seconds=1))
    state2.items[1] = tampered_item
    with pytest.raises(ClaimConflictError, match="expiry"):
        acquire_lease(state2, claim)


def test_complete_stale_lease_raises() -> None:
    """Completing a work item with wrong lease_id raises StaleCompletionError."""
    from dataclasses import replace as dc_replace

    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="c1",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.QUEUED,
    )
    state = _make_state({1: item})
    state2, claim = claim_work_item(state, 1, "op1")
    state3, lease = acquire_lease(state2, claim)
    # Tamper: force item back to CLAIMED to trigger stale lease check
    bad_item = dc_replace(state3.items[1], status=WorkItemStatus.CLAIMED)
    state3.items[1] = bad_item
    state3.revision = lease.revision
    with pytest.raises(StaleCompletionError):
        complete_work_item(state3, lease, "op1", recovery_epoch=0)


def test_complete_stale_operation_raises() -> None:
    """Completing with a different operation_id raises StaleCompletionError."""
    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="c1",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.QUEUED,
    )
    state = _make_state({1: item})
    state2, claim = claim_work_item(state, 1, "op1")
    state3, lease = acquire_lease(state2, claim)
    with pytest.raises(StaleCompletionError):
        complete_work_item(state3, lease, "WRONG_OP", recovery_epoch=0)


def test_complete_inactive_operation_raises() -> None:
    """Completing with correct op_id but inactive operation_status raises StaleCompletionError."""
    from dataclasses import replace as dc_replace

    item = WorkItem(
        pr_number=1,
        repo="owner/repo",
        change_id="c1",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.QUEUED,
    )
    state = _make_state({1: item})
    state2, claim = claim_work_item(state, 1, "op1")
    state3, lease = acquire_lease(state2, claim)
    # Force operation_status to COMPLETED so it's no longer ACTIVE
    bad_item = dc_replace(state3.items[1], operation_status=OperationStatus.COMPLETED)
    state3.items[1] = bad_item
    state3.revision = lease.revision
    with pytest.raises(StaleCompletionError, match="no longer active"):
        complete_work_item(state3, lease, "op1", recovery_epoch=0)


def test_complete_work_item_allows_unrelated_revision_advance() -> None:
    from dataclasses import replace as dc_replace

    state = _make_state({1: _make_item(1)})
    state2, claim = claim_work_item(state, 1, "op1")
    state3, lease = acquire_lease(state2, claim)
    unrelated_state = dc_replace(state3, revision=state3.revision + 2)
    completed = complete_work_item(unrelated_state, lease, "op1", recovery_epoch=0)
    assert completed.items[1].status == WorkItemStatus.COMPLETED
