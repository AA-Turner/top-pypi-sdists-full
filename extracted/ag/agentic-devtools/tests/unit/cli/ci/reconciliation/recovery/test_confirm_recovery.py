"""Tests for confirm_recovery()."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.models import (
    QuarantineRecord,
    QueueState,
    WorkItem,
    WorkItemStatus,
)
from agentic_devtools.cli.ci.reconciliation.recovery import confirm_recovery


def _empty_state() -> QueueState:
    return QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])


def test_advances_epoch() -> None:
    state = _empty_state()
    state.quarantines.append(QuarantineRecord("q1", state.repo, "bad", "digest", "evidence", datetime.now(UTC)))
    recovered, epoch = confirm_recovery(state, quarantine_id="q1", confirmed_by="operator")
    assert epoch.epoch_id == 1
    assert recovered.recovery_epoch == 1
    assert recovered.quarantines[0].rehydration_attempted is True


def test_importable_from_package() -> None:
    from agentic_devtools.cli.ci.reconciliation import confirm_recovery as exported

    assert callable(exported)


def test_empty_confirmed_by_raises() -> None:
    state = _empty_state()
    state.quarantines.append(QuarantineRecord("q1", state.repo, "bad", "digest", "evidence", datetime.now(UTC)))
    with pytest.raises(ValueError, match="confirmed_by"):
        confirm_recovery(state, quarantine_id="q1", confirmed_by="")


def test_unknown_quarantine_raises() -> None:
    with pytest.raises(KeyError):
        confirm_recovery(_empty_state(), quarantine_id="nonexistent", confirmed_by="operator")


def test_rejects_active_leases() -> None:
    state = _empty_state()
    state.quarantines.append(QuarantineRecord("q1", state.repo, "bad", "digest", "evidence", datetime.now(UTC)))
    state.items[1] = WorkItem(
        pr_number=1,
        repo=state.repo,
        change_id="change",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.LEASED,
        claim_id="claim",
        lease_id="lease",
        operation_id="operation",
        lease_expires_at=datetime.now(UTC) + timedelta(minutes=5),
    )
    with pytest.raises(ValueError, match="active"):
        confirm_recovery(state, quarantine_id="q1", confirmed_by="operator")


def test_rehydration_preserves_quarantine_and_is_bounded() -> None:
    from agentic_devtools.cli.ci.reconciliation.recovery import (
        RecoveryExhaustedError,
        rehydrate_state,
    )

    state = _empty_state()
    attempts = 0

    def load() -> QueueState:
        nonlocal attempts
        attempts += 1
        raise ValueError("corrupt")

    with pytest.raises(RecoveryExhaustedError) as error:
        rehydrate_state(state, load, max_attempts=2)
    assert attempts == 2
    assert error.value.state.records[-1].provider_status == "alertable"
    assert len(error.value.state.quarantines) == 1


def test_rehydration_returns_authoritative_state() -> None:
    from agentic_devtools.cli.ci.reconciliation.recovery import rehydrate_state

    state = _empty_state()
    state.quarantines.append(QuarantineRecord("q1", state.repo, "bad", "digest", "evidence", datetime.now(UTC)))
    rebuilt = QueueState(repo=state.repo, revision=4, items={}, records=[], quarantines=[], state_ref=state.state_ref)

    recovered = rehydrate_state(state, lambda: rebuilt)

    assert recovered.revision == rebuilt.revision
    assert recovered.recovery_epoch == 1
    assert recovered.quarantines[0].quarantine_id == "q1"


def test_rehydration_rejects_invalid_budget() -> None:
    from agentic_devtools.cli.ci.reconciliation.recovery import rehydrate_state

    with pytest.raises(ValueError, match="max_attempts"):
        rehydrate_state(_empty_state(), _empty_state, max_attempts=0)


def test_rehydration_rejects_mismatched_identity() -> None:
    from agentic_devtools.cli.ci.reconciliation.recovery import RecoveryExhaustedError, rehydrate_state

    rebuilt = QueueState(repo="other/repo", revision=1, items={}, records=[], quarantines=[])
    with pytest.raises(RecoveryExhaustedError):
        rehydrate_state(_empty_state(), lambda: rebuilt, max_attempts=1)
