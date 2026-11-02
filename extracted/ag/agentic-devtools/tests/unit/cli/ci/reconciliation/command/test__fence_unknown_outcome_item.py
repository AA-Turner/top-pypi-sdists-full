"""Tests for _fence_unknown_outcome_item()."""

from __future__ import annotations

from datetime import UTC, datetime

from agentic_devtools.cli.ci.reconciliation.command import _fence_unknown_outcome_item
from agentic_devtools.cli.ci.reconciliation.models import OperationStatus, QueueState, WorkItem, WorkItemStatus


def _work_item(
    *,
    eligibility: str = "eligible",
    due_at: datetime | None = None,
    status: WorkItemStatus = WorkItemStatus.LEASED,
) -> WorkItem:
    return WorkItem(
        pr_number=42,
        repo="owner/repo",
        change_id="sha-1",
        eligibility=eligibility,
        due_at=due_at,
        status=status,
    )


class TestFenceUnknownOutcomeItem:
    """Tests for _fence_unknown_outcome_item()."""

    def test_returns_state_unchanged_when_pr_number_is_none(self) -> None:
        """No pr_number means there is nothing to fence."""
        state = QueueState(repo="owner/repo", revision=0, items={42: _work_item()}, records=[], quarantines=[])

        result = _fence_unknown_outcome_item(state, None)

        assert result is state

    def test_returns_state_unchanged_when_item_is_absent(self) -> None:
        """A PR that is not tracked cannot be fenced."""
        state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])

        result = _fence_unknown_outcome_item(state, 42)

        assert result is state

    def test_returns_state_unchanged_when_already_unknown_status(self) -> None:
        """An already-fenced item (status held at UNKNOWN) is left untouched (idempotent)."""
        item = _work_item(eligibility="ineligible", status=WorkItemStatus.UNKNOWN)
        state = QueueState(repo="owner/repo", revision=0, items={42: item}, records=[], quarantines=[])

        result = _fence_unknown_outcome_item(state, 42)

        assert result is state

    def test_returns_state_unchanged_when_already_completed(self) -> None:
        """A completed item cannot be converted into an unknown outcome."""
        item = _work_item(status=WorkItemStatus.COMPLETED)
        state = QueueState(repo="owner/repo", revision=0, items={42: item}, records=[], quarantines=[])

        result = _fence_unknown_outcome_item(state, 42)

        assert result is state

    def test_fences_item_that_is_ineligible_but_not_yet_unknown_status(self) -> None:
        """Eligibility alone must not short-circuit fencing: status must reach UNKNOWN too.

        Regression test: a prior ordinary refresh cycle could leave an item ineligible for
        unrelated reasons (e.g. it fell outside the observed page) while its status remains
        e.g. LEASED. Idempotency must be keyed off ``status``, not ``eligibility``, or a
        later refresh cycle could still reset eligibility back to "eligible" and re-expose
        the item to dispatch.
        """
        item = _work_item(eligibility="ineligible", status=WorkItemStatus.LEASED)
        state = QueueState(repo="owner/repo", revision=0, items={42: item}, records=[], quarantines=[])

        result = _fence_unknown_outcome_item(state, 42)

        assert result is not state
        fenced_item = result.items[42]
        assert fenced_item.eligibility == "ineligible"
        assert fenced_item.due_at is None
        assert fenced_item.status == WorkItemStatus.UNKNOWN

    def test_marks_eligible_item_ineligible_and_clears_due_at(self) -> None:
        """An eligible, dispatchable item is fenced so it cannot be dispatched again."""
        due_at = datetime.now(UTC)
        item = _work_item(eligibility="eligible", due_at=due_at)
        state = QueueState(repo="owner/repo", revision=0, items={42: item}, records=[], quarantines=[])

        result = _fence_unknown_outcome_item(state, 42)

        assert result is not state
        fenced_item = result.items[42]
        assert fenced_item.eligibility == "ineligible"
        assert fenced_item.due_at is None
        assert fenced_item.status == WorkItemStatus.UNKNOWN

    def test_fences_only_when_original_active_identity_matches(self) -> None:
        """An active item is fenced only when all original operation identifiers match."""
        item = WorkItem(
            **{
                **_work_item(status=WorkItemStatus.LEASED).__dict__,
                "claim_id": "claim-1",
                "lease_id": "lease-1",
                "operation_id": "operation-1",
                "operation_status": OperationStatus.ACTIVE,
            }
        )
        state = QueueState(repo="owner/repo", revision=0, items={42: item}, records=[], quarantines=[])

        result = _fence_unknown_outcome_item(
            state,
            42,
            claim_id="claim-1",
            lease_id="lease-1",
            operation_id="operation-1",
        )

        assert result.items[42].status == WorkItemStatus.UNKNOWN
