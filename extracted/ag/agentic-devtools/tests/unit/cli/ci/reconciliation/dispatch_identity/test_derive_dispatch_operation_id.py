"""Tests for derive_dispatch_operation_id()."""

from agentic_devtools.cli.ci.reconciliation.dispatch_identity import derive_dispatch_operation_id
from agentic_devtools.cli.ci.reconciliation.models import WorkItem, WorkItemStatus
from agentic_devtools.orchestration.safety.operation_id import compute_operation_id


def test_derives_dispatch_operation_id_from_item_and_optional_identity() -> None:
    item = WorkItem(42, "owner/repo", "head-1", "eligible", None, WorkItemStatus.QUEUED)

    assert derive_dispatch_operation_id(item) == compute_operation_id(
        "dispatch_due_work",
        "reconciliation.dispatch",
        {
            "repo": "owner/repo",
            "pr_number": 42,
            "change_id": "head-1",
            "observation_watermark": "",
        },
    )
    assert derive_dispatch_operation_id(item, operation_identity="event-1") == compute_operation_id(
        "dispatch_due_work",
        "reconciliation.dispatch",
        {
            "repo": "owner/repo",
            "pr_number": 42,
            "change_id": "head-1",
            "observation_watermark": "event-1",
        },
    )
    assert derive_dispatch_operation_id(item, operation_id="explicit") == "explicit"
