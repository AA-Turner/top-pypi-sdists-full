"""Tests for SharedBudgetPolicy dataclass."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.policies.config import SharedBudgetPolicy
from agentic_devtools.orchestration.policies.defaults import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MAX_WALL_CLOCK_MINUTES,
)


class TestSharedBudgetPolicy:
    """Test SharedBudgetPolicy defaults and immutability."""

    def test_defaults(self) -> None:
        p = SharedBudgetPolicy()
        assert p.max_tokens == DEFAULT_MAX_TOKENS
        assert p.max_wall_clock_minutes == DEFAULT_MAX_WALL_CLOCK_MINUTES

    def test_custom_values(self) -> None:
        p = SharedBudgetPolicy(max_tokens=1000000, max_wall_clock_minutes=120)
        assert p.max_tokens == 1000000
        assert p.max_wall_clock_minutes == 120

    def test_frozen(self) -> None:
        p = SharedBudgetPolicy()
        with pytest.raises(Exception):
            p.max_tokens = 999  # type: ignore[misc]
