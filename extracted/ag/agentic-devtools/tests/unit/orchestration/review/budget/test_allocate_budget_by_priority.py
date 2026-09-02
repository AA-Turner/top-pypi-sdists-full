"""Tests for allocate_budget_by_priority function."""

from __future__ import annotations

from agentic_devtools.orchestration.review.budget import TokenBudget, allocate_budget_by_priority


class TestAllocateBudgetByPriority:
    """Tests for allocate_budget_by_priority."""

    def test_allocates_within_budget(self) -> None:
        """Items within budget get allocated=True."""
        budget = TokenBudget(budget_tokens=1000)
        items = [
            {"content": "short text", "priority": 1},
            {"content": "another text", "priority": 2},
        ]
        result = allocate_budget_by_priority(budget, items)
        assert all(r["allocated"] for r in result)

    def test_exceeds_budget_not_allocated(self) -> None:
        """Items exceeding budget get allocated=False."""
        budget = TokenBudget(budget_tokens=5)  # Very small budget
        items = [
            {"content": "x" * 100, "priority": 1},
            {"content": "y" * 100, "priority": 2},
        ]
        result = allocate_budget_by_priority(budget, items)
        # First item may fit, second shouldn't
        assert not all(r["allocated"] for r in result)

    def test_respects_priority_order(self) -> None:
        """Higher priority items (lower number) allocated first."""
        budget = TokenBudget(budget_tokens=10)
        items = [
            {"content": "x" * 50, "priority": 3},
            {"content": "y" * 10, "priority": 1},
        ]
        result = allocate_budget_by_priority(budget, items)
        # Priority 1 item should be processed first
        p1 = next(r for r in result if r["priority"] == 1)
        assert p1["allocated"] is True
