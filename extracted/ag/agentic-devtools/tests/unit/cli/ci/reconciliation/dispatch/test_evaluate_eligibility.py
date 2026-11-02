"""Tests for evaluate_eligibility()."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.dispatch import evaluate_eligibility
from agentic_devtools.cli.ci.reconciliation.models import WorkItem, WorkItemStatus


def _item(pr_number: int = 1, due_at: datetime | None = None) -> WorkItem:
    return WorkItem(pr_number, "o/r", "c", "eligible", due_at, WorkItemStatus.QUEUED)


def test_rejects_unknown_checker() -> None:
    now = datetime.now(UTC)
    item = WorkItem(1, "o/r", "c", "cached", now - timedelta(seconds=1), WorkItemStatus.QUEUED)
    result = evaluate_eligibility(item, now=now, checker=lambda _: None)
    assert result.is_eligible is False
    assert result.eligibility_reason == "eligibility_unknown"


def test_not_due_returns_not_eligible() -> None:
    result = evaluate_eligibility(_item(due_at=datetime.now(UTC) + timedelta(hours=1)), now=datetime.now(UTC))
    assert result.is_eligible is False


def test_naive_now_raises() -> None:
    with pytest.raises(ValueError, match="timezone"):
        evaluate_eligibility(_item(), now=datetime(2024, 1, 1))


def test_checker_returns_false_marks_not_eligible() -> None:
    now = datetime.now(UTC)
    result = evaluate_eligibility(_item(), now=now, checker=lambda _: False)
    assert result.is_eligible is False
    assert result.eligibility_reason == "not_eligible"


def test_checker_returns_true_marks_eligible() -> None:
    now = datetime.now(UTC)
    result = evaluate_eligibility(_item(), now=now, checker=lambda _: True)
    assert result.is_eligible is True
    assert result.eligibility_reason == "eligible"
