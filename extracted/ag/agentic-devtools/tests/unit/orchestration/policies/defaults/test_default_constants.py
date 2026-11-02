"""Tests for default policy constants."""

from __future__ import annotations

from agentic_devtools.orchestration.policies.defaults import (
    DEFAULT_BLOCKED_AFTER_MINUTES,
    DEFAULT_CONFIDENCE_MINIMUM,
    DEFAULT_COVERAGE_THRESHOLD,
    DEFAULT_ESCALATION_TRIGGERS,
    DEFAULT_MAX_HIGH_SEVERITY,
    DEFAULT_MAX_MEDIUM_SEVERITY,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MAX_WALL_CLOCK_MINUTES,
    DEFAULT_RETRY_BUDGET,
)


class TestDefaultConstants:
    """Verify all 9 default constants match spec values."""

    def test_max_high_severity(self) -> None:
        assert DEFAULT_MAX_HIGH_SEVERITY == 0

    def test_max_medium_severity(self) -> None:
        assert DEFAULT_MAX_MEDIUM_SEVERITY == 3

    def test_confidence_minimum(self) -> None:
        assert DEFAULT_CONFIDENCE_MINIMUM == 0.7

    def test_escalation_triggers(self) -> None:
        assert DEFAULT_ESCALATION_TRIGGERS == ()
        assert isinstance(DEFAULT_ESCALATION_TRIGGERS, tuple)

    def test_retry_budget(self) -> None:
        assert DEFAULT_RETRY_BUDGET == 3

    def test_max_tokens(self) -> None:
        assert DEFAULT_MAX_TOKENS == 500000

    def test_max_wall_clock_minutes(self) -> None:
        assert DEFAULT_MAX_WALL_CLOCK_MINUTES == 60

    def test_blocked_after_minutes(self) -> None:
        assert DEFAULT_BLOCKED_AFTER_MINUTES == 30

    def test_coverage_threshold(self) -> None:
        assert DEFAULT_COVERAGE_THRESHOLD == 100
