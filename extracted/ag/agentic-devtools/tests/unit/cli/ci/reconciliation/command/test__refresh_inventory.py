"""Concurrent inventory writers must not discard the winning queue state."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.reconciliation.command import _refresh_inventory
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    InMemoryBackingStore,
    QueueStore,
)


@pytest.mark.parametrize("trusted", [False, True])
def test_recomputes_inventory_save_without_repeating_provider_scan(trusted):
    now = datetime.now(UTC)
    original = QueueState("o/r", 1, {}, [], [], next_inventory_at=now + timedelta(minutes=5))
    unrelated = WorkItem(99, "o/r", "winner", "eligible", now, WorkItemStatus.UNKNOWN)
    winning = replace(original, revision=2, items={99: unrelated})
    provider = MagicMock()
    metadata = PRMetadata(42, "title", "feature", "head", "main")
    provider.get_pr_metadata.return_value = metadata
    provider.list_relevant_pull_requests.return_value = ([metadata], None)
    provider.get_pr_copilot_attribution.return_value = {"push": True, "observation_watermark": "head"}
    store = MagicMock()
    store.load.return_value = winning

    def save(state, *, expected_revision):
        if expected_revision == 1:
            raise ConcurrentModificationError("another writer won")
        assert expected_revision == 2
        return replace(state, revision=3)

    store.save.side_effect = save
    result = _refresh_inventory(
        provider, store, original, "o/r", trusted_pr_number=42 if trusted else None, trusted_head_sha="head"
    )

    assert result.revision == 3
    assert result.items[99] == unrelated
    assert result.items[42].change_id == "head"
    provider.get_pr_copilot_attribution.assert_called_once()
    store.load.assert_called_once()


@pytest.mark.parametrize("trusted", [False, True])
@pytest.mark.parametrize("invalidated", [False, True])
def test_newer_winning_observation_is_a_successful_noop(trusted, invalidated):
    now = datetime.now(UTC)
    original = QueueState("o/r", 1, {}, [], [], next_inventory_at=now + timedelta(minutes=5))
    item = WorkItem(
        42,
        "o/r",
        "newer-head",
        "ineligible",
        None,
        WorkItemStatus.UNKNOWN,
        last_observed_at=now + timedelta(minutes=1),
        observation_watermark="newer-watermark",
    )
    winning = replace(
        original, revision=2, items={42: item}, full_scan_complete=True, inventory_invalidated=invalidated
    )
    provider = MagicMock()
    metadata = PRMetadata(42, "title", "feature", "older-head", "main")
    provider.get_pr_metadata.return_value = metadata
    provider.list_relevant_pull_requests.return_value = ([metadata], None)
    provider.get_pr_copilot_attribution.return_value = {"push": True, "observation_watermark": "older-watermark"}
    store = MagicMock()
    store.load.return_value = winning
    store.save.side_effect = ConcurrentModificationError("winner covered event")

    result = _refresh_inventory(provider, store, original, "o/r", trusted_pr_number=42 if trusted else None)

    assert result is winning
    assert result.items[42] == item
    store.save.assert_called_once()


def test_completed_scan_recreates_missing_due_row():
    """A completed scan queues a missing open in-scope PR as due work."""
    provider = MagicMock()
    metadata = PRMetadata(42, "title", "feature", "sha-2", "main")
    provider.list_eligible_prs.return_value = [MagicMock(number=42)]
    provider.list_relevant_pull_requests.return_value = ([metadata], None)
    provider.get_pr_copilot_attribution.return_value = {"review": False, "push": False}
    store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())

    refreshed = _refresh_inventory(provider, store, store.load(), "owner/repo")

    item = refreshed.items[42]
    assert item.change_id == "sha-2"
    assert item.status is WorkItemStatus.QUEUED
    assert item.eligibility == "eligible"
    assert item.due_at is not None
    assert item.due_at <= datetime.now(UTC)
