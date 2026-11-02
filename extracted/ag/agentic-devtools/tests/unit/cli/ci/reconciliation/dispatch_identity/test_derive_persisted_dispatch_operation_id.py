"""Tests for derive_persisted_dispatch_operation_id()."""

from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.ci.reconciliation.dispatch_identity import (
    derive_dispatch_operation_id,
    derive_persisted_dispatch_operation_id,
)
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus


def test_derives_operation_id_from_matching_persisted_item() -> None:
    item = WorkItem(
        42,
        "owner/repo",
        "head-1",
        "eligible",
        datetime.now(UTC),
        WorkItemStatus.QUEUED,
        observation_watermark="observation-1",
    )
    state = QueueState("owner/repo", 3, {42: item}, [], [])

    assert derive_persisted_dispatch_operation_id(state, 42, "head-1") == derive_dispatch_operation_id(item)


@pytest.mark.parametrize(
    ("state", "pr_number", "change_id"),
    [
        (None, 42, "head-1"),
        (QueueState("owner/repo", 3, {}, [], []), 42, "head-1"),
        (QueueState("owner/repo", 3, {}, [], []), None, "head-1"),
        (QueueState("owner/repo", 3, {}, [], []), 42, ""),
        (
            QueueState(
                "owner/repo",
                3,
                {
                    42: WorkItem(
                        42,
                        "owner/repo",
                        "head-2",
                        "eligible",
                        None,
                        WorkItemStatus.QUEUED,
                    )
                },
                [],
                [],
            ),
            42,
            "head-1",
        ),
        (
            QueueState(
                "owner/repo",
                3,
                {
                    42: WorkItem(
                        43,
                        "owner/repo",
                        "head-1",
                        "eligible",
                        None,
                        WorkItemStatus.QUEUED,
                    )
                },
                [],
                [],
            ),
            42,
            "head-1",
        ),
    ],
)
def test_requires_persisted_pr_and_head(state, pr_number, change_id) -> None:
    assert derive_persisted_dispatch_operation_id(state, pr_number, change_id) is None
