"""Tests for _fence_unknown_dispatch_outcome()."""

from __future__ import annotations

import logging
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.reconciliation.command import _fence_unknown_dispatch_outcome
from agentic_devtools.cli.ci.reconciliation.dispatch import select_due_work
from agentic_devtools.cli.ci.reconciliation.models import (
    Lease,
    OperationStatus,
    QueueState,
    WorkItem,
    WorkItemStatus,
)
from agentic_devtools.cli.ci.reconciliation.queue_store import ConcurrentModificationError, QueueStoreError


def _work_item() -> WorkItem:
    return WorkItem(
        pr_number=42,
        repo="owner/repo",
        change_id="sha-1",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.LEASED,
    )


class TestFenceUnknownDispatchOutcome:
    """Tests for _fence_unknown_dispatch_outcome()."""

    def test_no_retry_budget_cannot_report_a_successful_fence(self, monkeypatch, caplog) -> None:
        """A disabled fencing budget cannot permit a success-shaped deferred result."""
        monkeypatch.setattr(config, "MAX_RETRY_ATTEMPTS", 0)
        queue_store = MagicMock()
        assert _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "message") is False
        queue_store.load.assert_not_called()
        assert "no fencing retry attempts" in caplog.text

    def test_fences_and_persists_the_reloaded_winning_state(self) -> None:
        """A successful reload is fenced, alerted, and saved through a fresh revision-CAS."""
        winning_state = QueueState(repo="owner/repo", revision=3, items={42: _work_item()}, records=[], quarantines=[])
        queue_store = MagicMock()
        queue_store.load.return_value = winning_state

        def persist_alert(alerted_state: QueueState, **kwargs) -> None:
            queue_store.load.return_value = alerted_state

        queue_store.save_alert.side_effect = persist_alert

        assert (
            _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "provider dispatch failed for pr_number=42")
            is True
        )

        assert queue_store.load.call_count == 2
        assert queue_store.save_alert.call_count == 1
        saved_state, save_kwargs = queue_store.save_alert.call_args
        alerted_state = saved_state[0]
        assert save_kwargs == {"expected_revision": winning_state.revision}
        assert alerted_state.items[42].eligibility == "ineligible"
        assert alerted_state.items[42].status is WorkItemStatus.UNKNOWN
        assert all(item.pr_number != 42 for item in select_due_work(alerted_state))
        assert alerted_state.records[-1].unknown_outcomes == (42,)

    def test_does_not_report_a_reclaimed_queued_item_as_fenced(self, caplog: pytest.LogCaptureFixture) -> None:
        """A persisted alert cannot claim fencing when a reclaimed item remains dispatchable."""
        reclaimed_item = replace(
            _work_item(),
            status=WorkItemStatus.QUEUED,
            claim_id="",
            lease_id="",
            lease_expires_at=None,
            claim_expires_at=None,
            claimed_at=None,
            operation_status=OperationStatus.EXPIRED,
        )
        winning_state = QueueState(
            repo="owner/repo", revision=3, items={42: reclaimed_item}, records=[], quarantines=[]
        )
        lease = Lease(
            lease_id="old-lease",
            claim_id="old-claim",
            pr_number=42,
            repo="owner/repo",
            operation_id="old-operation",
            acquired_at=datetime.now(UTC),
            expires_at=datetime.now(UTC) + timedelta(minutes=5),
        )
        queue_store = MagicMock()
        queue_store.load.return_value = winning_state
        queue_store.save_alert.side_effect = lambda *_args, **_kwargs: None

        with caplog.at_level(logging.ERROR):
            assert _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "message", lease=lease) is False

        saved_state = queue_store.save_alert.call_args.args[0]
        assert saved_state.items[42] == reclaimed_item
        assert [item.pr_number for item in select_due_work(saved_state)] == [42]
        assert queue_store.load.call_count == 2
        assert "does not fence unknown dispatch" in caplog.text

    def test_does_not_report_a_missing_item_as_fenced(self, caplog: pytest.LogCaptureFixture) -> None:
        """A persisted alert cannot claim fencing when the affected item is absent."""
        winning_state = QueueState(repo="owner/repo", revision=3, items={}, records=[], quarantines=[])
        queue_store = MagicMock()
        queue_store.load.return_value = winning_state

        with caplog.at_level(logging.ERROR):
            assert _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "message") is False

        assert queue_store.save_alert.call_count == 1
        assert "does not fence unknown dispatch" in caplog.text

    def test_logs_when_post_save_fence_verification_fails(self, caplog: pytest.LogCaptureFixture) -> None:
        """A failed read-back cannot be mistaken for a verified fence."""
        winning_state = QueueState(repo="owner/repo", revision=3, items={42: _work_item()}, records=[], quarantines=[])
        queue_store = MagicMock()
        queue_store.load.side_effect = [winning_state, QueueStoreError("read-back failed")]

        with caplog.at_level(logging.ERROR):
            assert _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "message") is False

        queue_store.save_alert.assert_called_once()
        assert "Unable to verify unknown dispatch outcome fence" in caplog.text

    def test_logs_and_returns_without_saving_when_load_raises_queue_store_error(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A QueueStoreError on load is logged and no save is attempted."""
        queue_store = MagicMock()
        queue_store.load.side_effect = QueueStoreError("corrupt state")

        with caplog.at_level(logging.ERROR):
            assert _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "message") is False

        queue_store.save_alert.assert_not_called()
        assert "Unable to record unknown dispatch outcome" in caplog.text

    def test_logs_and_returns_without_saving_when_load_raises_runtime_error(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A bare RuntimeError from the backing store's load path is also handled, not propagated."""
        queue_store = MagicMock()
        queue_store.load.side_effect = RuntimeError("HTTP 500 from GitHub API")

        with caplog.at_level(logging.ERROR):
            assert _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "message") is False

        queue_store.save_alert.assert_not_called()
        assert "Unable to record unknown dispatch outcome" in caplog.text

    def test_logs_when_save_raises_queue_store_error(self, caplog: pytest.LogCaptureFixture) -> None:
        """A QueueStoreError on save is logged rather than propagated, without retrying."""
        winning_state = QueueState(repo="owner/repo", revision=3, items={}, records=[], quarantines=[])
        queue_store = MagicMock()
        queue_store.load.return_value = winning_state
        queue_store.save_alert.side_effect = QueueStoreError("revision changed")

        with caplog.at_level(logging.ERROR):
            assert _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "message") is False

        assert queue_store.save_alert.call_count == 1
        assert "Unable to persist unknown dispatch outcome" in caplog.text

    def test_logs_when_save_raises_runtime_error(self, caplog: pytest.LogCaptureFixture) -> None:
        """A bare RuntimeError from the backing store's save path is also handled, not propagated."""
        winning_state = QueueState(repo="owner/repo", revision=3, items={}, records=[], quarantines=[])
        queue_store = MagicMock()
        queue_store.load.return_value = winning_state
        queue_store.save_alert.side_effect = RuntimeError("HTTP 500 from GitHub API")

        with caplog.at_level(logging.ERROR):
            assert _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "message") is False

        assert queue_store.save_alert.call_count == 1
        assert "Unable to persist unknown dispatch outcome" in caplog.text

    def test_retries_within_bounded_budget_after_repeated_concurrent_conflicts(self) -> None:
        """A repeated CAS conflict is retried with a fresh reload/fence/save, not just logged once."""
        verified_state = QueueState(
            repo="owner/repo",
            revision=6,
            items={42: replace(_work_item(), status=WorkItemStatus.UNKNOWN, eligibility="ineligible")},
            records=[],
            quarantines=[],
        )
        winning_states = [
            QueueState(repo="owner/repo", revision=3, items={42: _work_item()}, records=[], quarantines=[]),
            QueueState(repo="owner/repo", revision=4, items={42: _work_item()}, records=[], quarantines=[]),
            QueueState(repo="owner/repo", revision=5, items={42: _work_item()}, records=[], quarantines=[]),
            verified_state,
        ]
        queue_store = MagicMock()
        queue_store.load.side_effect = winning_states
        queue_store.save_alert.side_effect = [
            ConcurrentModificationError("state changed during save"),
            ConcurrentModificationError("state changed during save"),
            None,
        ]

        assert _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "message") is True

        assert queue_store.load.call_count == 4
        assert queue_store.save_alert.call_count == 3
        last_expected_revision = queue_store.save_alert.call_args_list[-1].kwargs["expected_revision"]
        assert last_expected_revision == winning_states[-2].revision

    def test_logs_after_exhausting_the_conflict_retry_budget(self, caplog: pytest.LogCaptureFixture) -> None:
        """Exhausting every retry attempt on persistent conflicts still returns without raising."""
        winning_state = QueueState(repo="owner/repo", revision=3, items={}, records=[], quarantines=[])
        queue_store = MagicMock()
        queue_store.load.return_value = winning_state
        queue_store.save_alert.side_effect = ConcurrentModificationError("state changed during save")

        with caplog.at_level(logging.ERROR):
            assert _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "message") is False

        assert queue_store.load.call_count == config.MAX_RETRY_ATTEMPTS
        assert queue_store.save_alert.call_count == config.MAX_RETRY_ATTEMPTS
        assert "kept changing concurrently" in caplog.text

    def test_preserves_a_winner_owned_by_a_different_operation(self, caplog: pytest.LogCaptureFixture) -> None:
        """A newer or completed winner is not fenced by an older dispatch failure."""
        winning_item = WorkItem(
            **{
                **_work_item().__dict__,
                "status": WorkItemStatus.COMPLETED,
                "claim_id": "new-claim",
                "lease_id": "new-lease",
                "operation_id": "new-operation",
                "operation_status": OperationStatus.COMPLETED,
                "completed_at": datetime.now(UTC),
            }
        )
        winning_state = QueueState(repo="owner/repo", revision=3, items={42: winning_item}, records=[], quarantines=[])
        queue_store = MagicMock()
        queue_store.load.return_value = winning_state
        original_lease = Lease(
            lease_id="old-lease",
            claim_id="old-claim",
            pr_number=42,
            repo="owner/repo",
            operation_id="old-operation",
            acquired_at=datetime.now(UTC),
            expires_at=datetime.now(UTC) + timedelta(minutes=5),
        )

        with caplog.at_level(logging.ERROR):
            assert (
                _fence_unknown_dispatch_outcome(queue_store, "owner/repo", 42, "message", lease=original_lease) is False
            )

        saved_state = queue_store.save_alert.call_args.args[0]
        assert saved_state.items[42] == winning_item
        assert "does not fence unknown dispatch" in caplog.text
