"""Tests for _append_unknown_outcome_alert()."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.command import _append_unknown_outcome_alert
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus


def _work_item() -> WorkItem:
    return WorkItem(
        pr_number=42,
        repo="owner/repo",
        change_id="sha-1",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.LEASED,
    )


class TestAppendUnknownOutcomeAlert:
    """Tests for _append_unknown_outcome_alert()."""

    def test_appends_alertable_record_with_unknown_outcome(self) -> None:
        """The appended record captures the unresolved PR and the supplied message."""
        state = QueueState(repo="owner/repo", revision=0, items={42: _work_item()}, records=[], quarantines=[])

        result = _append_unknown_outcome_alert(
            state,
            repo="owner/repo",
            unresolved_dispatch_pr=42,
            message="dispatch outcome unknown for pr_number=42",
        )

        assert len(result.records) == 1
        record = result.records[0]
        assert record.provider_status == "alertable"
        assert record.unknown_outcomes == (42,)
        assert record.message == "dispatch outcome unknown for pr_number=42"

    def test_fences_the_unresolved_item(self) -> None:
        """The unresolved PR's item is fenced so it cannot be dispatched again."""
        state = QueueState(repo="owner/repo", revision=0, items={42: _work_item()}, records=[], quarantines=[])

        result = _append_unknown_outcome_alert(
            state,
            repo="owner/repo",
            unresolved_dispatch_pr=42,
            message="dispatch outcome unknown for pr_number=42",
        )

        assert result.items[42].eligibility == "ineligible"

    def test_records_empty_unknown_outcomes_without_a_pr(self) -> None:
        """No unresolved PR means no unknown_outcomes entry, and nothing is fenced."""
        state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])

        result = _append_unknown_outcome_alert(
            state,
            repo="owner/repo",
            unresolved_dispatch_pr=None,
            message="queue-store persistence failed",
        )

        assert result.records[0].unknown_outcomes == ()
