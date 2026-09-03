"""Tests for InMemoryBackingStore."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.reconciliation.models import QueueState
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    InMemoryBackingStore,
    QueueStore,
)


def test_load_entry_returns_none_initially() -> None:
    backing = InMemoryBackingStore()

    assert backing.load_entry(("owner/repo", "ai-pr-loop-state")) is None


def test_save_entry_persists_revision() -> None:
    backing = InMemoryBackingStore()
    state = QueueState(repo="owner/repo", revision=1, items={}, records=[], quarantines=[])

    backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, state)

    assert backing.load_entry(("owner/repo", "ai-pr-loop-state")) == (1, state)


def test_save_entry_cas_conflict_raises() -> None:
    backing = InMemoryBackingStore()
    state = QueueState(repo="owner/repo", revision=1, items={}, records=[], quarantines=[])
    backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, state)

    with pytest.raises(ConcurrentModificationError):
        backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, state)


def test_two_queue_stores_sharing_backing_see_each_others_writes() -> None:
    backing = InMemoryBackingStore()
    store_one = QueueStore(repo="owner/repo", backing=backing)
    store_two = QueueStore(repo="owner/repo", backing=backing)

    state = store_one.save(store_one.load(), expected_revision=0)
    reloaded = store_two.load()

    assert state.revision == 1
    assert reloaded.revision == state.revision


def test_recovery_entry_uses_revision_token_and_rejects_stale_token() -> None:
    backing = InMemoryBackingStore()
    state = QueueState(repo="owner/repo", revision=1, items={}, records=[], quarantines=[])
    backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, state)

    assert backing.recovery_token(("owner/repo", "ai-pr-loop-state")) == "1"
    with pytest.raises(ConcurrentModificationError):
        backing.save_recovery_entry(("owner/repo", "ai-pr-loop-state"), "0", state)
