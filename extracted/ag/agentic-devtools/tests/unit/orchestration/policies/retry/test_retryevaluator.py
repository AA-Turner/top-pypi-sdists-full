"""Tests for RetryEvaluator."""

from __future__ import annotations

from agentic_devtools.orchestration.policies.retry import RetryEvaluator
from agentic_devtools.orchestration.policies.types import RetryDecision


class TestRetryEvaluatorAcceptance:
    """Acceptance scenarios from User Story 6."""

    def test_retry_permitted(self) -> None:
        """US6 Scenario 1: retry count < budget -> retry."""
        result = RetryEvaluator(current_retry_count=1, retry_budget=3)
        assert result.decision == RetryDecision.retry
        assert "2/3" in result.rationale or "remaining" in result.rationale.lower()

    def test_retries_exhausted(self) -> None:
        """US6 Scenario 2: retry count >= budget -> stop."""
        result = RetryEvaluator(current_retry_count=3, retry_budget=3)
        assert result.decision == RetryDecision.stop
        assert "3/3" in result.rationale

    def test_zero_budget_immediate_stop(self) -> None:
        """US6 Scenario 3: budget=0 -> immediate stop."""
        result = RetryEvaluator(current_retry_count=0, retry_budget=0)
        assert result.decision == RetryDecision.stop
        assert "0" in result.rationale

    def test_remaining_count_accurate_after_current_attempt(self) -> None:
        """remaining reflects retries left *after* the current attempt (budget - count - 1)."""
        # At count=0, budget=3: attempt 1/3, 2 left after this one
        result = RetryEvaluator(current_retry_count=0, retry_budget=3)
        assert result.decision == RetryDecision.retry
        assert "2 retries remaining" in result.rationale


class TestRetryEvaluatorStrategyHint:
    """Test strategy_hint metadata field."""

    def test_first_retry_hint_retry_same(self) -> None:
        result = RetryEvaluator(current_retry_count=0, retry_budget=3)
        assert result.decision == RetryDecision.retry
        assert result.metadata["strategy_hint"] == "retry_same"

    def test_middle_retry_hint_alternative(self) -> None:
        result = RetryEvaluator(current_retry_count=1, retry_budget=3)
        assert result.decision == RetryDecision.retry
        assert result.metadata["strategy_hint"] == "retry_with_alternative"

    def test_last_retry_hint_escalate(self) -> None:
        result = RetryEvaluator(current_retry_count=2, retry_budget=3)
        assert result.decision == RetryDecision.retry
        assert result.metadata["strategy_hint"] == "escalate_to_human"

    def test_stop_decision_no_strategy_hint_required(self) -> None:
        result = RetryEvaluator(current_retry_count=3, retry_budget=3)
        assert result.decision == RetryDecision.stop
        # strategy_hint may be absent or not required for stop decisions
        assert "strategy_hint" not in result.metadata

    def test_error_output_accepted(self) -> None:
        """error_output parameter is accepted without error."""
        result = RetryEvaluator(current_retry_count=0, retry_budget=3, error_output="test failed")
        assert result.decision == RetryDecision.retry

    def test_valid_strategy_hints(self) -> None:
        """All strategy hints are from allowed set."""
        valid_hints = {"retry_same", "retry_with_alternative", "escalate_to_human"}
        for count in range(3):
            result = RetryEvaluator(current_retry_count=count, retry_budget=3)
            if result.decision == RetryDecision.retry:
                assert result.metadata["strategy_hint"] in valid_hints


class TestRetryEvaluatorInvalidInputs:
    """Guard against negative retry counts and budgets."""

    def test_negative_retry_count_stops(self) -> None:
        """Negative current_retry_count -> immediate stop."""
        result = RetryEvaluator(current_retry_count=-1, retry_budget=3)
        assert result.decision == RetryDecision.stop
        assert "Invalid" in result.rationale

    def test_negative_retry_budget_stops(self) -> None:
        """Negative retry_budget -> immediate stop."""
        result = RetryEvaluator(current_retry_count=0, retry_budget=-1)
        assert result.decision == RetryDecision.stop
        assert "Invalid" in result.rationale

    def test_both_negative_stops(self) -> None:
        """Both parameters negative -> immediate stop."""
        result = RetryEvaluator(current_retry_count=-5, retry_budget=-2)
        assert result.decision == RetryDecision.stop
        assert "Invalid" in result.rationale

    def test_negative_count_metadata_preserved(self) -> None:
        """Invalid-input stop records the raw (invalid) values in metadata."""
        result = RetryEvaluator(current_retry_count=-3, retry_budget=5)
        assert result.metadata["current_retry_count"] == -3
        assert result.metadata["retry_budget"] == 5
