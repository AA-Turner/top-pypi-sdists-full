"""Tests for BudgetViolation dataclass."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.orchestration.policies.types import BudgetViolation


class TestBudgetViolation:
    """Test BudgetViolation attributes and immutability."""

    def test_creation(self) -> None:
        v = BudgetViolation(
            constraint_name="token_budget",
            configured_limit=500000,
            actual_value=520000,
            message="Token consumption 520000/500000 exceeded budget.",
        )
        assert v.constraint_name == "token_budget"
        assert v.configured_limit == 500000
        assert v.actual_value == 520000
        assert "520000/500000" in v.message

    def test_frozen(self) -> None:
        v = BudgetViolation(
            constraint_name="time_budget",
            configured_limit=60,
            actual_value=65,
            message="Time exceeded.",
        )
        with pytest.raises(FrozenInstanceError):
            v.constraint_name = "changed"  # type: ignore[misc]
        assert v.constraint_name == "time_budget"
