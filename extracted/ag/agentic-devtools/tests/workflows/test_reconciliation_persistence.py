"""Integration tests for reconciliation queue-state persistence.

Covers FR-001, FR-006, FR-011, and FR-017: atomic persistence, concurrent
runs, quarantine handling, and recovery epochs.
"""

from __future__ import annotations

import uuid
from dataclasses import replace
from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.ci.reconciliation.models import QuarantineRecord, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    InMemoryBackingStore,
    QuarantineActiveError,
    QueueStore,
)
from agentic_devtools.cli.ci.reconciliation.queue_transitions import claim_work_item


def _make_shared_backing() -> InMemoryBackingStore:
    return InMemoryBackingStore()


def _make_store(repo: str = "owner/repo", backing: InMemoryBackingStore | None = None) -> QueueStore:
    if backing is None:
        backing = _make_shared_backing()
    return QueueStore(repo=repo, backing=backing)


def _make_item(pr_number: int = 1) -> WorkItem:
    return WorkItem(
        pr_number=pr_number,
        repo="owner/repo",
        change_id=str(uuid.uuid4()),
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.QUEUED,
    )


class TestFoundationalPersistence:
    def test_load_returns_initial_empty_state(self) -> None:
        store = _make_store()
        state = store.load()
        assert state.repo == "owner/repo"
        assert state.revision == 0
        assert state.items == {}

    def test_save_and_reload_preserves_items(self) -> None:
        backing = _make_shared_backing()
        store = _make_store(backing=backing)
        state = store.load()
        state.items[1] = _make_item(1)
        saved = store.save(state, expected_revision=state.revision)
        reloaded = _make_store(backing=backing).load()
        assert 1 in reloaded.items
        assert reloaded.revision == saved.revision == 1

    def test_stale_write_rejected(self) -> None:
        backing = _make_shared_backing()
        store1 = QueueStore(repo="owner/repo", backing=backing)
        store2 = QueueStore(repo="owner/repo", backing=backing)
        s1 = store1.load()
        s2 = store2.load()
        s1.items[1] = _make_item(1)
        store1.save(s1, expected_revision=s1.revision)
        s2.items[2] = _make_item(2)
        with pytest.raises(ConcurrentModificationError):
            store2.save(s2, expected_revision=s2.revision)

    def test_revision_increments_on_each_save(self) -> None:
        store = _make_store()
        state = store.load()
        for i in range(1, 4):
            state.items[i] = _make_item(i)
            state = store.save(state, expected_revision=state.revision)
        assert state.revision == 3


class TestConcurrentRunSuppression:
    def test_concurrent_claim_save_on_same_item_raises_conflict(self) -> None:
        backing = _make_shared_backing()
        store = _make_store(backing=backing)
        state = store.load()
        state.items[1] = _make_item(1)
        state = store.save(state, expected_revision=state.revision)

        current_a = QueueStore(repo="owner/repo", backing=backing).load()
        current_b = QueueStore(repo="owner/repo", backing=backing).load()
        claimed_a, _ = claim_work_item(current_a, 1, str(uuid.uuid4()))
        QueueStore(repo="owner/repo", backing=backing).save(claimed_a, expected_revision=current_a.revision)
        claimed_b, _ = claim_work_item(current_b, 1, str(uuid.uuid4()))
        with pytest.raises(ConcurrentModificationError):
            QueueStore(repo="owner/repo", backing=backing).save(claimed_b, expected_revision=current_b.revision)


class TestQuarantineHandling:
    def test_quarantine_blocks_mutation(self) -> None:
        store = _make_store()
        state = store.load()
        store.quarantine(state, reason="test", evidence="{}")
        state = store.load()
        state.items[1] = _make_item(1)
        with pytest.raises(QuarantineActiveError):
            store.save(state, expected_revision=state.revision)

    def test_quarantine_without_recovery_epoch_stays_blocked(self) -> None:
        store = _make_store()
        state = store.save(store.load(), expected_revision=0)
        quarantined = replace(
            state,
            quarantines=[
                QuarantineRecord(
                    quarantine_id="q1",
                    repo="owner/repo",
                    reason="test fault",
                    evidence_digest="deadbeef",
                    evidence='{"fault": true}',
                    quarantined_at=datetime.now(UTC),
                )
            ],
        )
        store._store[("owner/repo", "ai-pr-loop-state")] = (quarantined.revision, quarantined)
        reloaded = store.load()
        reloaded.items[99] = _make_item(99)
        with pytest.raises(QuarantineActiveError):
            store.save(reloaded, expected_revision=reloaded.revision)


class TestRecoveryEpoch:
    def test_recovery_epoch_advances_on_save(self) -> None:
        store = _make_store()
        state = store.load()
        assert state.recovery_epoch == 0
        state.recovery_epoch = 1
        store.save(state, expected_revision=state.revision)
        reloaded = store.load()
        assert reloaded.recovery_epoch == 1
