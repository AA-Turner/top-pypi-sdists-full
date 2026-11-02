"""Tests for evaluate_dispatch_eligibility()."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.dispatch import evaluate_dispatch_eligibility
from agentic_devtools.cli.ci.reconciliation.models import WorkItem, WorkItemStatus


def _item(
    *,
    pr_number: int = 1,
    eligibility: str = "eligible",
    due_at: datetime | None = None,
) -> WorkItem:
    return WorkItem(pr_number, "owner/repo", "change", eligibility, due_at, WorkItemStatus.QUEUED)


def test_returns_eligible_for_eligible_item() -> None:
    result = evaluate_dispatch_eligibility(_item(), datetime.now(UTC))
    assert result.is_eligible is True
    assert result.pr_number == 1


def test_returns_not_eligible_for_ineligible_item() -> None:
    assert evaluate_dispatch_eligibility(_item(eligibility="ineligible"), datetime.now(UTC)).is_eligible is False


def test_returns_not_eligible_for_unknown_eligibility() -> None:
    assert evaluate_dispatch_eligibility(_item(eligibility="unknown"), datetime.now(UTC)).is_eligible is False


def test_rejects_naive_now() -> None:
    with pytest.raises(ValueError, match="timezone"):
        evaluate_dispatch_eligibility(_item(), datetime(2024, 1, 1))


def test_records_evaluated_at() -> None:
    now = datetime.now(UTC)
    assert evaluate_dispatch_eligibility(_item(), now).evaluated_at == now


def test_marks_due_item_as_due() -> None:
    result = evaluate_dispatch_eligibility(
        _item(due_at=datetime.now(UTC) - timedelta(seconds=1)),
        datetime.now(UTC),
    )
    assert result.is_due is True


def test_marks_future_item_as_not_due() -> None:
    assert (
        evaluate_dispatch_eligibility(_item(due_at=datetime.now(UTC) + timedelta(hours=1)), datetime.now(UTC)).is_due
        is False
    )
