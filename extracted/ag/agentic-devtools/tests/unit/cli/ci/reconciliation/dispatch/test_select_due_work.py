"""Tests for select_due_work()."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.dispatch import select_due_work
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus


def _make_state(items: dict[int, WorkItem] | None = None) -> QueueState:
    return QueueState(
        repo="owner/repo",
        revision=0,
        items=items or {},
        records=[],
        quarantines=[],
    )


def _item(
    pr_number: int = 1,
    due_at: datetime | None = None,
    *,
    status: WorkItemStatus = WorkItemStatus.QUEUED,
    eligibility: str = "eligible",
) -> WorkItem:
    return WorkItem(pr_number, "owner/repo", str(uuid.uuid4()), eligibility, due_at, status)


def test_returns_empty_for_no_items() -> None:
    assert select_due_work(_make_state(), datetime.now(UTC)) == []


def test_rejects_naive_now() -> None:
    with pytest.raises(ValueError, match="timezone"):
        select_due_work(_make_state(), datetime(2024, 1, 1))


def test_queued_item_without_due_at_is_due() -> None:
    result = select_due_work(_make_state({1: _item()}), datetime.now(UTC))
    assert [item.pr_number for item in result] == [1]


def test_select_due_work_returns_oldest_due_queued_items() -> None:
    now = datetime.now(UTC)
    state = _make_state({2: _item(2, now), 1: _item(1, now - timedelta(seconds=1))})
    assert [item.pr_number for item in select_due_work(state, now)] == [1, 2]


def test_item_with_future_due_at_is_not_due() -> None:
    state = _make_state({1: _item(due_at=datetime.now(UTC) + timedelta(hours=1))})
    assert select_due_work(state, datetime.now(UTC)) == []


def test_due_items_no_due_at_sorted_by_pr_number() -> None:
    now = datetime.now(UTC)
    result = select_due_work(_make_state({2: _item(2, None), 1: _item(1, None)}), now)
    assert [item.pr_number for item in result] == [1, 2]


def test_claimed_item_is_not_due() -> None:
    assert select_due_work(_make_state({1: _item(status=WorkItemStatus.CLAIMED)}), datetime.now(UTC)) == []


def test_leased_item_is_not_due() -> None:
    assert select_due_work(_make_state({1: _item(status=WorkItemStatus.LEASED)}), datetime.now(UTC)) == []


def test_completed_item_is_not_due() -> None:
    assert select_due_work(_make_state({1: _item(status=WorkItemStatus.COMPLETED)}), datetime.now(UTC)) == []


def test_ineligible_item_is_not_due() -> None:
    assert select_due_work(_make_state({1: _item(eligibility="ineligible")}), datetime.now(UTC)) == []


def test_unknown_eligibility_item_is_not_due() -> None:
    assert select_due_work(_make_state({1: _item(eligibility="unknown")}), datetime.now(UTC)) == []
