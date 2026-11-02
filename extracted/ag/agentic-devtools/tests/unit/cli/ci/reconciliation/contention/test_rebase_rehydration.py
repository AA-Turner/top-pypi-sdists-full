"""Recovery rebasing preserves winning records and rejects changed authority."""

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.ci.reconciliation.contention import rebase_rehydration
from agentic_devtools.cli.ci.reconciliation.models import (
    OperationStatus,
    QuarantineRecord,
    QueueState,
    WorkItem,
    WorkItemStatus,
)


def test_reapplies_only_planned_epoch_and_quarantine_marking():
    quarantine = QuarantineRecord("q", "o/r", "bad", "digest", "evidence", datetime.now(UTC))
    current = QueueState("o/r", 4, {}, [], [quarantine])
    seed = replace(current, revision=3, recovery_epoch=1, quarantines=[replace(quarantine, rehydration_attempted=True)])
    result = rebase_rehydration(current, seed)
    assert result.revision == current.revision
    assert result.items == current.items
    assert result.recovery_epoch == 1
    assert result.quarantines == seed.quarantines


@pytest.mark.parametrize("change", ["epoch", "quarantine"])
def test_rejects_newer_recovery_authority(change):
    seed = QueueState("o/r", 3, {}, [], [], recovery_epoch=1)
    current = replace(seed, revision=4)
    if change == "epoch":
        current = replace(current, recovery_epoch=2)
    else:
        current = replace(
            current, quarantines=[QuarantineRecord("q", "o/r", "bad", "digest", "evidence", datetime.now(UTC))]
        )
    with pytest.raises(RuntimeError, match="Recovery authority changed"):
        rebase_rehydration(current, seed)


def test_reapplies_unknown_fence_to_matching_active_dispatch():
    now = datetime.now(UTC)
    seed_item = WorkItem(
        42,
        "o/r",
        "head",
        "ineligible",
        None,
        WorkItemStatus.UNKNOWN,
        claim_id="claim",
        lease_id="lease",
        operation_id="operation",
    )
    winner_item = replace(seed_item, status=WorkItemStatus.LEASED, eligibility="eligible", due_at=now)
    seed = QueueState("o/r", 3, {42: seed_item}, [], [])
    current = replace(seed, revision=4, items={42: winner_item})

    result = rebase_rehydration(current, seed, unresolved_dispatch_pr=42)

    assert result.items[42] == seed_item


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("change_id", "new-head"),
        ("claim_id", "new-claim"),
        ("lease_id", "new-lease"),
        ("operation_id", "new-operation"),
    ],
)
def test_preserves_new_dispatch_owner(field, value):
    seed_item = WorkItem(
        42,
        "o/r",
        "head",
        "ineligible",
        None,
        WorkItemStatus.UNKNOWN,
        claim_id="claim",
        lease_id="lease",
        operation_id="operation",
    )
    winning_item = replace(seed_item, status=WorkItemStatus.LEASED, **{field: value})
    seed = QueueState("o/r", 3, {42: seed_item}, [], [])
    current = replace(seed, revision=4, items={42: winning_item})

    result = rebase_rehydration(current, seed, unresolved_dispatch_pr=42)

    assert result.items[42] == winning_item


def test_preserves_completed_dispatch_outcome():
    seed_item = WorkItem(
        42,
        "o/r",
        "head",
        "ineligible",
        None,
        WorkItemStatus.UNKNOWN,
        claim_id="claim",
        lease_id="lease",
        operation_id="operation",
    )
    completed_item = replace(
        seed_item,
        status=WorkItemStatus.COMPLETED,
        operation_status=OperationStatus.COMPLETED,
    )
    seed = QueueState("o/r", 3, {42: seed_item}, [], [])
    current = replace(seed, revision=4, items={42: completed_item})

    result = rebase_rehydration(current, seed, unresolved_dispatch_pr=42)

    assert result.items[42] == completed_item


@pytest.mark.parametrize("missing", ["seed_item", "winning_item", "seed_identity"])
def test_does_not_reapply_fence_without_matching_seed_and_winner(missing):
    seed_item = WorkItem(
        42,
        "o/r",
        "head",
        "ineligible",
        None,
        WorkItemStatus.UNKNOWN,
        claim_id="claim",
        lease_id="lease",
        operation_id="operation",
    )
    seed = QueueState("o/r", 3, {42: seed_item}, [], [])
    winning_item = replace(seed_item, status=WorkItemStatus.LEASED)
    current = replace(seed, revision=4, items={42: winning_item})
    if missing == "seed_item":
        seed = replace(seed, items={})
    elif missing == "winning_item":
        current = replace(current, items={})
    else:
        seed = replace(seed, items={42: replace(seed_item, lease_id="")})

    result = rebase_rehydration(current, seed, unresolved_dispatch_pr=42)

    assert result.items == current.items
