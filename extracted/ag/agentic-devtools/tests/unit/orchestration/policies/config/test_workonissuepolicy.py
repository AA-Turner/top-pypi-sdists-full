"""Tests for WorkOnIssuePolicy dataclass."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.policies.config import WorkOnIssuePolicy
from agentic_devtools.orchestration.policies.defaults import (
    DEFAULT_BLOCKED_AFTER_MINUTES,
    DEFAULT_COVERAGE_THRESHOLD,
    DEFAULT_RETRY_BUDGET,
)


class TestWorkOnIssuePolicy:
    """Test WorkOnIssuePolicy defaults and immutability."""

    def test_defaults(self) -> None:
        p = WorkOnIssuePolicy()
        assert p.retry_budget == DEFAULT_RETRY_BUDGET
        assert p.blocked_after_minutes == DEFAULT_BLOCKED_AFTER_MINUTES
        assert p.coverage_threshold == DEFAULT_COVERAGE_THRESHOLD

    def test_custom_values(self) -> None:
        p = WorkOnIssuePolicy(retry_budget=5, blocked_after_minutes=45, coverage_threshold=80)
        assert p.retry_budget == 5
        assert p.blocked_after_minutes == 45
        assert p.coverage_threshold == 80

    def test_frozen(self) -> None:
        p = WorkOnIssuePolicy()
        with pytest.raises(Exception):
            p.retry_budget = 10  # type: ignore[misc]
