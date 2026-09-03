"""Tests for acquire_dispatch_claim()."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.dispatch import DispatchConflictError, acquire_dispatch_claim
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus


def _make_state(items: dict[int, WorkItem] | None = None) -> QueueState:
    return QueueState(repo="owner/repo", revision=0, items=items or {}, records=[], quarantines=[])


def _item(
    *,
    pr_number: int = 1,
    status: WorkItemStatus = WorkItemStatus.QUEUED,
    due_at: datetime | None = None,
    eligibility: str = "eligible",
) -> WorkItem:
    return WorkItem(pr_number, "owner/repo", str(uuid.uuid4()), eligibility, due_at, status)


def test_eligible_queued_item_gets_claim() -> None:
    new_state, claim = acquire_dispatch_claim(_make_state({1: _item()}), 1, str(uuid.uuid4()))
    assert claim.pr_number == 1
    assert new_state.items[1].status == WorkItemStatus.CLAIMED


def test_already_claimed_raises_conflict() -> None:
    with pytest.raises(DispatchConflictError):
        acquire_dispatch_claim(_make_state({1: _item(status=WorkItemStatus.CLAIMED)}), 1, str(uuid.uuid4()))


def test_already_leased_raises_conflict() -> None:
    with pytest.raises(DispatchConflictError):
        acquire_dispatch_claim(_make_state({1: _item(status=WorkItemStatus.LEASED)}), 1, str(uuid.uuid4()))


def test_missing_item_raises_key_error() -> None:
    with pytest.raises(KeyError):
        acquire_dispatch_claim(_make_state(), 99, str(uuid.uuid4()))


def test_ineligible_item_raises_value_error() -> None:
    with pytest.raises(ValueError, match="[Ee]ligib"):
        acquire_dispatch_claim(_make_state({1: _item(eligibility="ineligible")}), 1, str(uuid.uuid4()))


def test_unknown_eligibility_raises_value_error() -> None:
    with pytest.raises(ValueError, match="[Ee]ligib"):
        acquire_dispatch_claim(_make_state({1: _item(eligibility="unknown")}), 1, str(uuid.uuid4()))


def test_future_due_item_raises_conflict() -> None:
    with pytest.raises(DispatchConflictError, match="not due"):
        acquire_dispatch_claim(
            _make_state({1: _item(due_at=datetime.now(UTC) + timedelta(hours=1))}),
            1,
            str(uuid.uuid4()),
        )


def test_wraps_claim_conflict_error(monkeypatch: pytest.MonkeyPatch) -> None:
    from agentic_devtools.cli.ci.reconciliation.dispatch import ClaimConflictError

    def _raise(*_args: object, **_kwargs: object) -> tuple[QueueState, object]:
        raise ClaimConflictError("claimed elsewhere")

    monkeypatch.setattr(
        "agentic_devtools.cli.ci.reconciliation.dispatch.claim_work_item",
        _raise,
    )
    with pytest.raises(DispatchConflictError, match="claimed elsewhere"):
        acquire_dispatch_claim(_make_state({1: _item()}), 1, str(uuid.uuid4()))
