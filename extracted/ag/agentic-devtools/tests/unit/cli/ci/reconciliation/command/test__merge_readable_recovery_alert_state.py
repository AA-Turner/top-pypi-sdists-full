"""Tests for _merge_readable_recovery_alert_state()."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.ci.reconciliation.command import _merge_readable_recovery_alert_state
from agentic_devtools.cli.ci.reconciliation.models import (
    OperationStatus,
    QuarantineRecord,
    QueueState,
    ReconciliationRecord,
    WorkItem,
    WorkItemStatus,
)


def _record(record_id: str, provider_status: str = "alertable") -> ReconciliationRecord:
    now = datetime.now(UTC)
    return ReconciliationRecord(
        record_id=record_id,
        repo="owner/repo",
        run_id="run-1",
        started_at=now,
        completed_at=now,
        provider_status=provider_status,
        message=record_id,
    )


def _quarantine(
    quarantine_id: str,
    *,
    reason: str = "reason",
    rehydration_attempted: bool = False,
) -> QuarantineRecord:
    return QuarantineRecord(
        quarantine_id=quarantine_id,
        repo="owner/repo",
        reason=reason,
        evidence_digest=f"digest-{quarantine_id}",
        evidence=quarantine_id,
        quarantined_at=datetime.now(UTC),
        recovery_epoch=0,
        rehydration_attempted=rehydration_attempted,
    )


def _item(pr_number: int = 42, *, eligibility: str = "eligible") -> WorkItem:
    return WorkItem(
        pr_number=pr_number,
        repo="owner/repo",
        change_id=f"sha-{pr_number}",
        eligibility=eligibility,
        due_at=datetime.now(UTC),
        status=WorkItemStatus.LEASED,
    )


class TestMergeReadableRecoveryAlertState:
    """Tests for _merge_readable_recovery_alert_state()."""

    def test_rejects_rewritten_records(self) -> None:
        """Existing records must remain an exact prefix of the alert state."""
        current = QueueState(repo="owner/repo", revision=0, items={}, records=[_record("base")], quarantines=[])
        alerted = replace(current, records=[_record("rewritten")])

        with pytest.raises(RuntimeError, match="rewrote existing records"):
            _merge_readable_recovery_alert_state(current, alerted, current)

    def test_rejects_changed_item_set(self) -> None:
        """Alert retries must not add or remove items."""
        current = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])
        alerted = replace(current, items={42: _item()})

        with pytest.raises(RuntimeError, match="changed the item set"):
            _merge_readable_recovery_alert_state(current, alerted, current)

    def test_rejects_epoch_advance_that_appends_quarantines(self) -> None:
        """Epoch-advancing retries must rehydrate in-place, not append new quarantines."""
        quarantine = _quarantine("q-1")
        current = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[quarantine])
        alerted = replace(
            current,
            recovery_epoch=1,
            records=[_record("alert")],
            quarantines=[quarantine, _quarantine("q-2")],
        )

        with pytest.raises(RuntimeError, match="must not append quarantines"):
            _merge_readable_recovery_alert_state(current, alerted, current)

    def test_rejects_epoch_advance_without_rehydrated_quarantines(self) -> None:
        """Epoch-advancing retries must mark each quarantine rehydrated."""
        quarantine = _quarantine("q-1")
        current = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[quarantine])
        alerted = replace(current, recovery_epoch=1, records=[_record("alert")])

        with pytest.raises(RuntimeError, match="must mark quarantines rehydrated"):
            _merge_readable_recovery_alert_state(current, alerted, current)

    def test_rejects_rewritten_quarantines_without_epoch_advance(self) -> None:
        """Non-epoch retries may only append quarantines."""
        quarantine = _quarantine("q-1")
        current = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[quarantine])
        alerted = replace(current, quarantines=[replace(quarantine, reason="rewritten")])

        with pytest.raises(RuntimeError, match="rewrote existing quarantines"):
            _merge_readable_recovery_alert_state(current, alerted, current)

    def test_merges_fenced_item_and_appended_quarantine_without_epoch_advance(self) -> None:
        """Non-epoch retries preserve winner fields while reapplying fencing and appended data."""
        current = QueueState(
            repo="owner/repo",
            revision=0,
            items={42: _item()},
            records=[],
            quarantines=[],
        )
        alerted = replace(
            current,
            items={42: replace(current.items[42], eligibility="ineligible", due_at=None)},
            records=[_record("alert")],
            quarantines=[_quarantine("q-1")],
        )
        winning = replace(
            current,
            revision=1,
            records=[_record("winner")],
            quarantines=[_quarantine("winner-q")],
        )

        merged = _merge_readable_recovery_alert_state(current, alerted, winning)

        assert merged.items[42].eligibility == "ineligible"
        assert merged.items[42].due_at is None
        assert [record.record_id for record in merged.records] == ["winner", "alert"]
        assert [record.quarantine_id for record in merged.quarantines] == ["winner-q", "q-1"]
        assert merged.recovery_epoch == winning.recovery_epoch

    def test_preserves_completed_winning_item(self) -> None:
        """A terminal winner must not be rolled back to an unknown status."""
        current = QueueState(
            repo="owner/repo",
            revision=0,
            items={42: _item()},
            records=[],
            quarantines=[],
        )
        alerted = replace(
            current,
            items={42: replace(current.items[42], eligibility="ineligible", due_at=None)},
            records=[_record("alert")],
        )
        winning_item = replace(
            current.items[42],
            status=WorkItemStatus.COMPLETED,
            operation_status=OperationStatus.COMPLETED,
            completed_at=datetime.now(UTC),
        )
        winning = replace(current, revision=1, items={42: winning_item})

        merged = _merge_readable_recovery_alert_state(current, alerted, winning)

        assert merged.items[42] == winning_item

    def test_skips_fencing_when_the_winning_state_already_dropped_the_item(self) -> None:
        """Missing winner items stay absent rather than being reintroduced by the retry merge."""
        current = QueueState(
            repo="owner/repo",
            revision=0,
            items={42: _item()},
            records=[],
            quarantines=[],
        )
        alerted = replace(
            current,
            items={42: replace(current.items[42], eligibility="ineligible", due_at=None)},
            records=[_record("alert")],
        )
        winning = QueueState(repo="owner/repo", revision=1, items={}, records=[], quarantines=[])

        merged = _merge_readable_recovery_alert_state(current, alerted, winning)

        assert merged.items == {}
        assert [record.record_id for record in merged.records] == ["alert"]

    def test_leaves_unchanged_items_untouched(self) -> None:
        """Items with no alert-time mutation are preserved exactly from the winning state."""
        current = QueueState(
            repo="owner/repo",
            revision=0,
            items={42: _item()},
            records=[],
            quarantines=[],
        )
        winning = replace(current, revision=1)
        alerted = replace(current, records=[_record("alert")])

        merged = _merge_readable_recovery_alert_state(current, alerted, winning)

        assert merged.items[42] == winning.items[42]
        assert [record.record_id for record in merged.records] == ["alert"]

    def test_rejects_epoch_retry_when_winner_quarantines_changed(self) -> None:
        """Epoch retries stop when another writer changed the quarantine set."""
        quarantine = _quarantine("q-1")
        current = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[quarantine])
        alerted = replace(
            current,
            recovery_epoch=1,
            records=[_record("alert")],
            quarantines=[replace(quarantine, rehydration_attempted=True)],
        )
        winning = replace(current, revision=1, quarantines=[quarantine, _quarantine("q-2")])

        with pytest.raises(RuntimeError, match="quarantines changed"):
            _merge_readable_recovery_alert_state(current, alerted, winning)

    def test_rejects_epoch_retry_when_winner_rewrites_existing_quarantine(self) -> None:
        """Epoch retries stop when another writer mutated an existing quarantine in place."""
        quarantine = _quarantine("q-1")
        current = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[quarantine])
        alerted = replace(
            current,
            recovery_epoch=1,
            records=[_record("alert")],
            quarantines=[replace(quarantine, rehydration_attempted=True)],
        )
        winning = replace(current, revision=1, quarantines=[replace(quarantine, reason="changed")])

        with pytest.raises(RuntimeError, match="quarantines changed"):
            _merge_readable_recovery_alert_state(current, alerted, winning)

    def test_merges_epoch_retry_when_winner_is_still_on_current_epoch(self) -> None:
        """Epoch retries advance the winning state when no one else has advanced it yet."""
        quarantine = _quarantine("q-1")
        current = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[quarantine])
        alerted = replace(
            current,
            recovery_epoch=1,
            records=[_record("alert")],
            quarantines=[replace(quarantine, rehydration_attempted=True)],
        )
        winning = replace(current, revision=1, records=[_record("winner")])

        merged = _merge_readable_recovery_alert_state(current, alerted, winning)

        assert merged.recovery_epoch == 1
        assert merged.quarantines[0].rehydration_attempted is True
        assert [record.record_id for record in merged.records] == ["winner", "alert"]

    def test_merges_epoch_retry_when_winner_already_advanced(self) -> None:
        """Epoch retries may append the alert when another writer already advanced the epoch safely."""
        quarantine = _quarantine("q-1")
        current = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[quarantine])
        alerted = replace(
            current,
            recovery_epoch=1,
            records=[_record("alert")],
            quarantines=[replace(quarantine, rehydration_attempted=True)],
        )
        winning = replace(
            current,
            revision=1,
            recovery_epoch=1,
            records=[_record("winner")],
            quarantines=[replace(quarantine, rehydration_attempted=True)],
        )

        merged = _merge_readable_recovery_alert_state(current, alerted, winning)

        assert merged.recovery_epoch == 1
        assert [record.record_id for record in merged.records] == ["winner", "alert"]

    def test_rejects_epoch_retry_when_winner_advanced_to_unexpected_epoch(self) -> None:
        """Epoch retries stop when another writer advanced to an incompatible recovery epoch."""
        quarantine = _quarantine("q-1")
        current = QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[quarantine])
        alerted = replace(
            current,
            recovery_epoch=1,
            records=[_record("alert")],
            quarantines=[replace(quarantine, rehydration_attempted=True)],
        )
        winning = replace(current, revision=1, recovery_epoch=2)

        with pytest.raises(RuntimeError, match="recovery epoch changed"):
            _merge_readable_recovery_alert_state(current, alerted, winning)
