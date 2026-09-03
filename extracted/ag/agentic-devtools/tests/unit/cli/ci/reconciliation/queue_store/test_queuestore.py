"""Tests for QueueStore."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict
from datetime import UTC, datetime, timedelta

import pytest

import agentic_devtools.cli.ci.reconciliation.config as cfg
from agentic_devtools.cli.ci.reconciliation.metrics import MetricEventType, create_metric_event
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    GitHubVariableBackingStore,
    InMemoryBackingStore,
    QuarantineActiveError,
    QueueStore,
    StateDecodeError,
    StateTooLargeError,
)
from agentic_devtools.state import serialize_queue_document


def _make_store() -> QueueStore:
    return QueueStore(repo="owner/repo", backing=InMemoryBackingStore())


def test_load_empty_state() -> None:
    store = _make_store()
    state = store.load()
    assert state.revision == 0
    assert state.items == {}
    assert state.records == []
    assert state.quarantines == []


def test_save_increments_revision() -> None:
    store = _make_store()
    state = store.load()
    saved = store.save(state, expected_revision=0)
    assert saved.revision == 1


def test_concurrent_modification_raises() -> None:
    store = _make_store()
    state = store.load()
    store.save(state, expected_revision=0)
    with pytest.raises(ConcurrentModificationError):
        store.save(state, expected_revision=0)


def test_quarantine_blocks_save() -> None:
    store = _make_store()
    state = store.load()
    store.quarantine(state, reason="test", evidence="bad data")
    quarantined = store.load()
    with pytest.raises(QuarantineActiveError):
        store.save(quarantined, expected_revision=quarantined.revision)


def test_quarantine_raises_on_stale_revision() -> None:
    store = _make_store()
    state = store.load()
    store.save(state, expected_revision=0)
    with pytest.raises(ConcurrentModificationError):
        store.quarantine(state, reason="test", evidence="bad data")


def test_quarantine_increments_revision() -> None:
    store = _make_store()
    state = store.load()

    store.quarantine(state, reason="test", evidence="bad data")

    quarantined = store.load()
    assert quarantined.revision == 1
    assert len(quarantined.quarantines) == 1


def test_state_too_large_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfg, "MAX_STATE_SIZE_BYTES", 1)
    store = _make_store()
    state = store.load()
    with pytest.raises(StateTooLargeError):
        store.save(state, expected_revision=0)


def test_save_rechecks_updated_payload_size(monkeypatch: pytest.MonkeyPatch) -> None:
    store = _make_store()
    state = store.load()
    payload = serialize_queue_document(asdict(state))
    monkeypatch.setattr(cfg, "MAX_STATE_SIZE_BYTES", len(payload))
    with pytest.raises(StateTooLargeError):
        store.save(state, expected_revision=0)


def test_save_returns_queuestate() -> None:
    store = _make_store()
    saved = store.save(store.load(), expected_revision=0)
    assert isinstance(saved, QueueState)


def test_save_thaws_nested_metric_attributes() -> None:
    store = _make_store()
    state = store.load()
    state.metric_events.append(
        create_metric_event(
            MetricEventType.DISCOVERY,
            "owner/repo",
            {"nested": {"values": [1, 2]}},
        )
    )

    saved = store.save(state, expected_revision=0)

    nested = saved.metric_events[0].attributes["nested"]
    assert isinstance(nested, Mapping)
    assert nested["values"] == (1, 2)


def test_save_rejects_foreign_repo_state() -> None:
    store = _make_store()
    state = store.load()
    state.repo = "other/repo"
    with pytest.raises(ValueError, match="expected repo"):
        store.save(state, expected_revision=0)


def test_save_rejects_leased_item_without_expiry() -> None:
    store = _make_store()
    state = store.load()
    state.items[1] = WorkItem(
        repo="owner/repo",
        pr_number=1,
        change_id="change-1",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.LEASED,
        claim_id="claim-1",
        lease_id="lease-1",
        operation_id="operation-1",
    )
    with pytest.raises(ValueError, match="lease_expires_at"):
        store.save(state, expected_revision=0)


def test_state_too_stale_is_available_for_recovery(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfg, "MAX_STATE_AGE_SECONDS", 1)
    store = _make_store()
    state = store.load()
    saved = store.save(state, expected_revision=0)
    stale_time = datetime.now(UTC) - timedelta(seconds=100)
    saved.last_updated_at = stale_time
    store._store[("owner/repo", "ai-pr-loop-state")] = (saved.revision, saved)
    assert store.load().revision == saved.revision


def test_load_after_save_returns_state() -> None:
    """Load after save returns the saved state."""
    store = _make_store()
    state = store.load()
    saved = store.save(state, expected_revision=0)
    loaded = store.load()
    assert loaded.revision == saved.revision


def test_load_state_with_null_updated_at() -> None:
    """Load a stored state with last_updated_at=None returns it without error."""
    store = _make_store()
    state = store.load()
    saved = store.save(state, expected_revision=0)
    saved.last_updated_at = None
    store._store[("owner/repo", "ai-pr-loop-state")] = (saved.revision, saved)
    loaded = store.load()
    assert loaded.revision == saved.revision
    assert loaded.last_updated_at is None


def test_load_invalid_entry_raises_state_decode_error() -> None:
    class _InvalidBacking:
        def load_entry(self, _key: tuple[str, str]) -> tuple[int, QueueState]:
            return (1, QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[]))

        def save_entry(self, _key: tuple[str, str], _expected_revision: int, _updated: QueueState) -> None:
            raise AssertionError("save_entry should not be called")

        def recovery_token(self, _key: tuple[str, str]) -> str | None:
            return None

        def save_recovery_entry(self, _key, _expected_token, _updated) -> None:
            raise AssertionError("save_recovery_entry should not be called")

    store = QueueStore(repo="owner/repo", backing=_InvalidBacking())

    with pytest.raises(StateDecodeError, match="Persisted revision 1"):
        store.load()


@pytest.mark.parametrize(
    ("revision", "state", "message"),
    [
        (True, QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[]), "must be an int"),
        (0, object(), "must be a QueueState"),
    ],
)
def test_load_rejects_invalid_entry_types(revision, state, message) -> None:
    class _InvalidBacking:
        def load_entry(self, _key):
            return revision, state

        def save_entry(self, _key, _expected_revision, _updated):
            raise AssertionError("save_entry should not be called")

        def recovery_token(self, _key):
            return None

        def save_recovery_entry(self, _key, _expected_token, _updated):
            raise AssertionError("save_recovery_entry should not be called")

    store = QueueStore(repo="owner/repo", backing=_InvalidBacking())

    with pytest.raises(StateDecodeError, match=message):
        store.load()


def test_load_rejects_invalid_state() -> None:
    class _InvalidBacking:
        def load_entry(self, _key):
            return 0, QueueState(repo="other/repo", revision=0, items={}, records=[], quarantines=[])

        def save_entry(self, _key, _expected_revision, _updated):
            raise AssertionError("save_entry should not be called")

        def recovery_token(self, _key):
            return None

        def save_recovery_entry(self, _key, _expected_token, _updated):
            raise AssertionError("save_recovery_entry should not be called")

    store = QueueStore(repo="owner/repo", backing=_InvalidBacking())

    with pytest.raises(StateDecodeError, match="Loaded queue state is invalid"):
        store.load()


def test_store_property_returns_empty_mapping_for_non_inmemory_backing() -> None:
    store = QueueStore(repo="owner/repo", backing=GitHubVariableBackingStore(repo="owner/repo"))

    assert store._store == {}


def test_ensure_state_ref_delegates_to_github_backing(monkeypatch: pytest.MonkeyPatch) -> None:
    backing = GitHubVariableBackingStore(repo="owner/repo")
    store = QueueStore(repo="owner/repo", backing=backing)
    calls: list[tuple[str, str]] = []

    def _create_ref(repo: str, state_ref: str) -> None:
        calls.append((repo, state_ref))

    monkeypatch.setattr(backing, "_create_state_ref", _create_ref)

    store.ensure_state_ref()

    assert calls == [("owner/repo", "ai-pr-loop-state")]


def test_ensure_state_ref_is_noop_for_inmemory_backing() -> None:
    _make_store().ensure_state_ref()


def test_recovery_save_uses_opaque_token() -> None:
    store = _make_store()
    state = store.save(store.load(), expected_revision=0)

    assert store.recovery_token() == "1"
    recovered = store.save_recovery(state, "1")

    assert recovered.revision == state.revision
