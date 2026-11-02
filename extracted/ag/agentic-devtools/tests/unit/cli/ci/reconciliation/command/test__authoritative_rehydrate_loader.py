"""Tests for _authoritative_rehydrate_loader()."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.reconciliation.command import _authoritative_rehydrate_loader
from agentic_devtools.cli.ci.reconciliation.models import QuarantineRecord, QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore
from agentic_devtools.cli.ci.reconciliation.recovery import rehydrate_state


def _seed_store(store: QueueStore, state: QueueState) -> None:
    store._backing.save_entry(store._key(), state.revision, state)


def test_authoritative_rehydrate_loader_returns_forced_inventory() -> None:
    provider = MagicMock()
    provider.list_relevant_pull_requests.return_value = ([], None)
    store = MagicMock()
    store.is_quarantined.return_value = False
    store.save_rehydration.side_effect = lambda state, expected_revision: state
    state = QueueState(repo="owner/repo", revision=2, items={}, records=[], quarantines=[])

    result = _authoritative_rehydrate_loader(provider, store, state, "owner/repo")

    assert result.full_scan_complete is True


def test_authoritative_rehydrate_loader_fences_unresolved_dispatch() -> None:
    provider = MagicMock()
    provider.list_relevant_pull_requests.return_value = (
        [PRMetadata(42, "title", "branch", "head", "main")],
        None,
    )
    provider.get_pr_copilot_attribution.return_value = {}
    store = MagicMock()
    store.save_rehydration.side_effect = lambda state, expected_revision: state
    state = QueueState(repo="owner/repo", revision=2, items={}, records=[], quarantines=[])

    result = _authoritative_rehydrate_loader(
        provider,
        store,
        state,
        "owner/repo",
        unresolved_dispatch_pr=42,
    )

    assert result.items[42].eligibility == "ineligible"
    assert result.items[42].due_at is None
    saved_state = store.save_rehydration.call_args.args[0]
    assert saved_state.items[42].eligibility == "ineligible"


def test_authoritative_rehydrate_loader_preserves_unobserved_unresolved_dispatch() -> None:
    provider = MagicMock()
    provider.list_relevant_pull_requests.return_value = (
        [PRMetadata(7, "title", "branch", "head", "main")],
        "next-page",
    )
    provider.get_pr_copilot_attribution.return_value = {}
    store = MagicMock()
    store.save_rehydration.side_effect = lambda state, expected_revision: state
    existing = WorkItem(
        pr_number=42,
        repo="owner/repo",
        change_id="sha-42",
        eligibility="eligible",
        due_at=datetime.now(UTC),
        status=WorkItemStatus.LEASED,
    )
    state = QueueState(repo="owner/repo", revision=2, items={42: existing}, records=[], quarantines=[])

    result = _authoritative_rehydrate_loader(
        provider,
        store,
        state,
        "owner/repo",
        unresolved_dispatch_pr=42,
    )

    assert result.items[42].eligibility == "ineligible"
    assert result.items[42].due_at is None
    assert result.items[42].change_id == "sha-42"


def test_authoritative_rehydrate_loader_preserves_claimed_item_without_unresolved_dispatch() -> None:
    """A claimed/leased item survives the baseline even when it is not the fenced PR.

    Regression test: the baseline used to keep only WorkItemStatus.UNKNOWN items, so any
    other still-open, in-flight (claimed/leased) PR was dropped. The forced inventory scan
    then observed that PR with no matching baseline entry and recreated it from scratch as
    WorkItemStatus.QUEUED, erasing its durable lease before reclaim_leases() could assess
    expiry and allowing the same work to be dispatched again.
    """
    provider = MagicMock()
    provider.list_relevant_pull_requests.return_value = (
        [PRMetadata(99, "title", "branch", "sha-99", "main")],
        None,
    )
    provider.get_pr_copilot_attribution.return_value = {}
    store = MagicMock()
    store.save_rehydration.side_effect = lambda state, expected_revision: state
    existing = WorkItem(
        pr_number=99,
        repo="owner/repo",
        change_id="sha-99",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.CLAIMED,
        claim_id="claim-99",
    )
    state = QueueState(repo="owner/repo", revision=2, items={99: existing}, records=[], quarantines=[])

    result = _authoritative_rehydrate_loader(provider, store, state, "owner/repo")

    assert result.items[99].status == WorkItemStatus.CLAIMED
    assert result.items[99].claim_id == "claim-99"


def test_authoritative_rehydrate_loader_rejects_unavailable_inventory() -> None:
    provider = MagicMock()
    provider.list_relevant_pull_requests.side_effect = RuntimeError("unavailable")
    store = MagicMock()
    state = QueueState(repo="owner/repo", revision=2, items={}, records=[], quarantines=[])

    with pytest.raises(RuntimeError, match="unavailable"):
        _authoritative_rehydrate_loader(provider, store, state, "owner/repo")


def test_authoritative_rehydrate_loader_persists_quarantined_state_with_real_store() -> None:
    """A quarantined state must not deadlock its own forced-scan recovery save.

    Regression test: QueueStore.save() rejects any transition whose incoming state is
    still actively quarantined. Before the recovery epoch was pre-advanced here, the
    forced-scan `store.save()` inside this loader always passed in a still-quarantined
    baseline (rehydrate_state() only advances the epoch on the value this loader
    *returns*, after this save already ran) and therefore raised QuarantineActiveError
    on every attempt in production. A mock-based store does not exercise that guard, so
    it cannot catch this.
    """
    provider = MagicMock()
    provider.list_relevant_pull_requests.return_value = ([], None)
    store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
    now = datetime.now(UTC)
    quarantine = QuarantineRecord(
        quarantine_id="q1",
        repo="owner/repo",
        reason="bad",
        evidence_digest="digest",
        evidence="evidence",
        quarantined_at=now,
        recovery_epoch=0,
    )
    state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[quarantine])
    _seed_store(store, state)
    assert store.is_quarantined(state)

    refreshed = _authoritative_rehydrate_loader(provider, store, state, "owner/repo")

    assert refreshed.recovery_epoch == state.recovery_epoch + 1
    assert all(record.rehydration_attempted for record in refreshed.quarantines)
    assert not store.is_quarantined(refreshed)
    persisted = store.load()
    assert persisted.recovery_epoch == refreshed.recovery_epoch
    assert not store.is_quarantined(persisted)


def test_rehydrates_a_quarantined_state_end_to_end() -> None:
    """The authoritative loader's internal save must not be blocked by its own baseline.

    Regression test for a bug where the loader's baseline kept the pre-recovery
    recovery_epoch, so QueueStore.save() treated both the persisted document and the
    incoming state as still quarantined and raised QuarantineActiveError on every
    attempt, permanently exhausting recovery for any genuinely quarantined queue.
    """
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    backing = InMemoryBackingStore()
    store = QueueStore(repo="owner/repo", backing=backing)
    state = QueueState(
        repo="owner/repo",
        revision=0,
        items={},
        records=[],
        quarantines=[QuarantineRecord("q1", "owner/repo", "bad", "digest", "evidence", now)],
    )
    _seed_store(store, state)
    provider = MagicMock()
    provider.list_relevant_pull_requests.return_value = ([], None)

    recovered = rehydrate_state(state, lambda: _authoritative_rehydrate_loader(provider, store, state, "owner/repo"))

    assert recovered.recovery_epoch == 1
    assert store.is_quarantined(recovered) is False
    persisted = store.load()
    assert persisted.recovery_epoch == 1
    assert persisted.revision == recovered.revision


def test_advances_epoch_when_state_is_not_quarantined() -> None:
    """A stale (but non-quarantined) state persists the same epoch returned by rehydration."""
    backing = InMemoryBackingStore()
    store = QueueStore(repo="owner/repo", backing=backing)
    state = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])
    _seed_store(store, state)
    provider = MagicMock()
    provider.list_relevant_pull_requests.return_value = ([], None)

    refreshed = _authoritative_rehydrate_loader(provider, store, state, "owner/repo")

    assert refreshed.recovery_epoch == state.recovery_epoch + 1
    assert store.load().recovery_epoch == refreshed.recovery_epoch
