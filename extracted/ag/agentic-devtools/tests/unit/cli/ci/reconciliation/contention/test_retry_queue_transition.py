"""Only pure queue transitions are retried against freshly loaded winners."""

from dataclasses import replace
from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.reconciliation.contention import (
    QueueTransitionRetryExhaustedError,
    retry_queue_transition,
)
from agentic_devtools.cli.ci.reconciliation.dispatch_identity import derive_dispatch_operation_id
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    InMemoryBackingStore,
    QueueStore,
    QueueStoreError,
)


@pytest.mark.parametrize("authoritative", [False, True])
def test_reloads_each_winner_and_recomputes(authoritative, caplog):
    states = [QueueState("o/r", revision, {}, [], []) for revision in (1, 2, 3)]
    store = MagicMock()
    store.load.side_effect = states[1:]
    save = store.save_rehydration if authoritative else store.save
    saved = replace(states[-1], revision=4, recovery_epoch=4)
    save.side_effect = [ConcurrentModificationError("race 1"), ConcurrentModificationError("race 2"), saved]
    transition = MagicMock(side_effect=lambda state: replace(state, recovery_epoch=state.revision + 1))
    with patch("agentic_devtools.cli.ci.reconciliation.contention.wait_for_contention") as wait:
        with caplog.at_level("INFO"):
            result = retry_queue_transition(store, states[0], transition, authoritative=authoritative)
    assert result is saved
    assert [call.args[0] for call in transition.call_args_list] == states
    assert [call.kwargs["expected_revision"] for call in save.call_args_list] == [1, 2, 3]
    assert wait.call_count == 2
    assert "retry recovered" in caplog.text


def test_winner_already_covers_transition_without_another_save():
    state = QueueState("o/r", 1, {}, [], [], inventory_invalidated=False)
    winner = replace(state, revision=2, inventory_invalidated=True)
    store = MagicMock()
    store.load.return_value = winner
    store.save.side_effect = ConcurrentModificationError("race")
    with patch("agentic_devtools.cli.ci.reconciliation.contention.wait_for_contention"):
        result = retry_queue_transition(store, state, lambda current: replace(current, inventory_invalidated=True))
    assert result is winner
    store.save.assert_called_once()


def test_exhaustion_is_bounded_and_preserves_last_conflict(monkeypatch):
    from agentic_devtools.cli.ci.reconciliation import config

    monkeypatch.setattr(config, "MAX_RETRY_ATTEMPTS", 2)
    state = QueueState("o/r", 1, {}, [], [], inventory_invalidated=False)
    store = MagicMock()
    store.load.return_value = replace(state, revision=2)
    store.save.side_effect = [ConcurrentModificationError("first"), ConcurrentModificationError("last conflict")]
    with patch("agentic_devtools.cli.ci.reconciliation.contention.wait_for_contention") as wait:
        with pytest.raises(QueueTransitionRetryExhaustedError, match="budget of 2 exhausted: last conflict") as error:
            retry_queue_transition(store, state, lambda current: replace(current, inventory_invalidated=True))
    assert isinstance(error.value.__cause__, ConcurrentModificationError)
    assert store.save.call_count == 2
    store.load.assert_called_once()
    wait.assert_called_once_with(1)


def test_exhaustion_preserves_operation_id_from_triggering_transition(monkeypatch):
    from agentic_devtools.cli.ci.reconciliation import config

    monkeypatch.setattr(config, "MAX_RETRY_ATTEMPTS", 1)
    now = datetime.now(UTC)
    item = WorkItem(42, "o/r", "head-1", "eligible", now, WorkItemStatus.QUEUED, observation_watermark="event-1")
    store = QueueStore("o/r", backing=InMemoryBackingStore())
    store.save(QueueState("o/r", 0, {42: item}, [], []), expected_revision=0)
    state = store.load()
    store.save(state, expected_revision=state.revision)

    with pytest.raises(QueueTransitionRetryExhaustedError) as error:
        retry_queue_transition(
            store,
            state,
            lambda current: replace(current, full_scan_complete=True),
            triggering_pr=(42, "head-1"),
        )

    assert error.value.operation_id == derive_dispatch_operation_id(item)


@pytest.mark.parametrize(
    "error",
    [
        QueueStoreError("storage unavailable"),
        ValueError("invalid transition"),
        RuntimeError("unrelated runtime failure"),
    ],
)
def test_non_cas_failures_are_not_retried(error):
    store = MagicMock()
    store.save.side_effect = error
    state = QueueState("o/r", 1, {}, [], [], inventory_invalidated=False)
    with pytest.raises(type(error), match=str(error)) as caught:
        retry_queue_transition(store, state, lambda current: replace(current, inventory_invalidated=True))
    assert type(caught.value) is type(error)
    store.load.assert_not_called()


def test_zero_budget_is_rejected(monkeypatch):
    from agentic_devtools.cli.ci.reconciliation import config

    monkeypatch.setattr(config, "MAX_RETRY_ATTEMPTS", 0)
    with pytest.raises(ValueError, match="positive"):
        retry_queue_transition(MagicMock(), QueueState("o/r", 1, {}, [], []), lambda state: state)


def test_success_without_conflict():
    store = MagicMock()
    state = QueueState("o/r", 1, {}, [], [], inventory_invalidated=False)
    assert (
        retry_queue_transition(store, state, lambda current: replace(current, inventory_invalidated=True))
        is store.save.return_value
    )
