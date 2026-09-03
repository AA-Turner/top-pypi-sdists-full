"""Tests for WorkItemStatus."""

from agentic_devtools.cli.ci.reconciliation.models import WorkItemStatus


def test_contains_expected_values() -> None:
    assert WorkItemStatus.UNKNOWN.value == "unknown"
    assert WorkItemStatus.QUEUED.value == "queued"
    assert WorkItemStatus.CLAIMED.value == "claimed"
    assert WorkItemStatus.LEASED.value == "leased"
    assert WorkItemStatus.COMPLETED.value == "completed"
    assert WorkItemStatus.QUARANTINED.value == "quarantined"
