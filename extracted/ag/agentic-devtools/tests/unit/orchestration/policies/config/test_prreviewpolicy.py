"""Tests for PRReviewPolicy dataclass."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.policies.config import PRReviewPolicy
from agentic_devtools.orchestration.policies.defaults import (
    DEFAULT_CONFIDENCE_MINIMUM,
    DEFAULT_ESCALATION_TRIGGERS,
    DEFAULT_MAX_HIGH_SEVERITY,
    DEFAULT_MAX_MEDIUM_SEVERITY,
)


class TestPRReviewPolicy:
    """Test PRReviewPolicy defaults and immutability."""

    def test_defaults(self) -> None:
        p = PRReviewPolicy()
        assert p.max_high_severity == DEFAULT_MAX_HIGH_SEVERITY
        assert p.max_medium_severity == DEFAULT_MAX_MEDIUM_SEVERITY
        assert p.confidence_minimum == DEFAULT_CONFIDENCE_MINIMUM
        assert p.escalation_triggers == DEFAULT_ESCALATION_TRIGGERS

    def test_custom_values(self) -> None:
        p = PRReviewPolicy(
            max_high_severity=2,
            max_medium_severity=5,
            confidence_minimum=0.9,
            escalation_triggers=("security", "breaking"),
        )
        assert p.max_high_severity == 2
        assert p.max_medium_severity == 5
        assert p.confidence_minimum == 0.9
        assert p.escalation_triggers == ("security", "breaking")

    def test_frozen(self) -> None:
        p = PRReviewPolicy()
        with pytest.raises(Exception):
            p.max_high_severity = 5  # type: ignore[misc]

    def test_escalation_triggers_is_tuple(self) -> None:
        p = PRReviewPolicy(escalation_triggers=("a", "b"))
        assert isinstance(p.escalation_triggers, tuple)
