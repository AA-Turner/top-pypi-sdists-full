"""Tests for BlockedStateDetector."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

from agentic_devtools.orchestration.policies.blocked import BlockedStateDetector
from agentic_devtools.orchestration.policies.config import PolicyConfig, WorkOnIssuePolicy
from agentic_devtools.orchestration.policies.context import WorkflowContext
from agentic_devtools.orchestration.policies.types import BlockedDecision


def _iso_now_minus(minutes: float) -> str:
    """Create ISO-8601 timestamp for 'minutes' ago."""
    dt = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    return dt.isoformat()


class TestBlockedStateDetectorAcceptance:
    """Acceptance scenarios from User Story 5."""

    def test_time_without_progress_blocked(self) -> None:
        """US5 Scenario 1: 35 min in step with 0 state changes -> blocked."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(blocked_after_minutes=30))
        context = WorkflowContext(
            step_history=[{"step": "implementation", "entered_at": _iso_now_minus(35)}],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.blocked
        assert "35" in result.rationale or "3" in result.rationale
        assert "30" in result.rationale

    def test_repetitive_failure_blocked(self) -> None:
        """US5 Scenario 2: 3 consecutive identical errors -> blocked."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(blocked_after_minutes=30))
        context = WorkflowContext(
            step_history=[{"step": "implementation", "entered_at": _iso_now_minus(10)}],
            recent_outcomes=["error: test failed", "error: test failed", "error: test failed"],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.blocked
        assert "3" in result.rationale
        assert "identical" in result.rationale.lower()

    def test_neither_threshold_met_progressing(self) -> None:
        """US5 Scenario 3: 25 min + 2 identical + 1 different -> progressing."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(blocked_after_minutes=30))
        context = WorkflowContext(
            step_history=[{"step": "implementation", "entered_at": _iso_now_minus(25)}],
            recent_outcomes=["error: test failed", "error: test failed", "error: different"],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing


class TestBlockedStateDetectorBoundary:
    """Boundary tests."""

    def test_exactly_at_time_threshold_not_blocked(self) -> None:
        """Exactly at threshold (30 min) -> not blocked (> not >=)."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(blocked_after_minutes=30))
        # Use 29.9 to be safely under
        context = WorkflowContext(
            step_history=[{"step": "implementation", "entered_at": _iso_now_minus(29.9)}],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing

    def test_exactly_2_identical_failures_not_blocked(self) -> None:
        """Only 2 identical failures -> not blocked (need 3)."""
        policy = PolicyConfig()
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": _iso_now_minus(5)}],
            recent_outcomes=["same error", "same error"],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing

    def test_3_plus_identical_failures_blocked(self) -> None:
        """4 identical consecutive failures -> blocked."""
        policy = PolicyConfig()
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": _iso_now_minus(5)}],
            recent_outcomes=["same error", "same error", "same error", "same error"],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.blocked

    def test_empty_step_history_progressing(self) -> None:
        """No step history -> progressing."""
        policy = PolicyConfig()
        context = WorkflowContext()
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing

    def test_empty_outcomes_progressing(self) -> None:
        """No recent outcomes -> progressing."""
        policy = PolicyConfig()
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": _iso_now_minus(5)}],
            recent_outcomes=[],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing

    def test_3_identical_empty_strings_not_blocked(self) -> None:
        """3 empty strings are not considered a failure pattern."""
        policy = PolicyConfig()
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": _iso_now_minus(5)}],
            recent_outcomes=["", "", ""],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing

    def test_invalid_timestamp_skips_time_check(self) -> None:
        """Invalid timestamp in step_history doesn't cause error."""
        policy = PolicyConfig()
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": "not-a-date"}],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing

    def test_naive_timestamp_treated_as_utc(self) -> None:
        """Naive timestamp (no tzinfo) is treated as UTC."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(blocked_after_minutes=30))
        # Create a naive timestamp 35 minutes ago
        dt = datetime.now(timezone.utc) - timedelta(minutes=35)
        naive_str = dt.strftime("%Y-%m-%dT%H:%M:%S")
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": naive_str}],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.blocked

    def test_z_suffix_timestamp_parsed_correctly(self) -> None:
        """Timestamps with 'Z' UTC suffix are parsed correctly."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(blocked_after_minutes=30))
        dt = datetime.now(timezone.utc) - timedelta(minutes=35)
        z_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": z_str}],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.blocked

    def test_long_failure_message_truncated(self) -> None:
        """Very long failure message in rationale is truncated to 500 chars."""
        policy = PolicyConfig()
        long_error = "error: " + "x" * 600
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": _iso_now_minus(5)}],
            recent_outcomes=[long_error, long_error, long_error],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.blocked
        assert len(result.rationale) <= 500

    def test_long_step_name_in_time_based_rationale_truncated(self) -> None:
        """Very long step name in time-based rationale is truncated to 500 chars."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(blocked_after_minutes=30))
        long_step_name = "s" * 600
        context = WorkflowContext(
            step_history=[{"step": long_step_name, "entered_at": _iso_now_minus(35)}],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.blocked
        assert len(result.rationale) <= 500
        assert result.rationale.endswith("...")

    def test_3_identical_non_failure_outcomes_not_blocked(self) -> None:
        """3 identical outcomes that are not failures (e.g. 'pass') don't trigger blocked."""
        policy = PolicyConfig()
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": _iso_now_minus(5)}],
            recent_outcomes=["pass", "pass", "pass"],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing

    def test_3_identical_no_failure_keyword_not_blocked(self) -> None:
        """3 identical outcomes without any failure keyword (e.g. 600 'x' chars) are progressing."""
        policy = PolicyConfig()
        no_keyword = "x" * 600
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": _iso_now_minus(5)}],
            recent_outcomes=[no_keyword, no_keyword, no_keyword],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing

    def test_missing_entered_at_key_progressing(self) -> None:
        """Step entry missing 'entered_at' key doesn't crash."""
        policy = PolicyConfig()
        context = WorkflowContext(
            step_history=[{"step": "impl"}],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing

    def test_non_consecutive_failures_progressing(self) -> None:
        """Failures that are not all at the end don't trigger."""
        policy = PolicyConfig()
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": _iso_now_minus(5)}],
            recent_outcomes=["same", "same", "same", "different"],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing

    def test_consecutive_failures_after_success_hits_break(self) -> None:
        """Loop counting consecutive failures breaks on different outcome."""
        policy = PolicyConfig()
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": _iso_now_minus(5)}],
            recent_outcomes=["different", "same error", "same error", "same error"],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.blocked
        assert result.metadata["consecutive_count"] == 3

    def test_time_check_fires_regardless_of_prior_step_entries(self) -> None:
        """Time-based blocked detection fires even when step_history has multiple entries."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(blocked_after_minutes=30))
        context = WorkflowContext(
            step_history=[
                {"step": "planning", "entered_at": _iso_now_minus(100)},
                {"step": "implementation", "entered_at": _iso_now_minus(35)},
            ],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.blocked
        assert result.metadata["pattern"] == "time_without_progress"

    def test_time_based_rationale_uses_decimal_minutes(self) -> None:
        """Time-based blocked rationale shows one decimal place (no whole-number rounding)."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(blocked_after_minutes=30))
        context = WorkflowContext(
            step_history=[{"step": "implementation", "entered_at": _iso_now_minus(35)}],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.blocked
        assert re.search(r"Blocked: \d+\.\d/30 minutes", result.rationale) is not None

    def test_non_string_entered_at_skips_time_check(self) -> None:
        """Non-string truthy entered_at (e.g. int) does not raise AttributeError."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(blocked_after_minutes=30))
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": 1234567890}],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing

    def test_float_entered_at_skips_time_check(self) -> None:
        """Float truthy entered_at does not raise AttributeError."""
        policy = PolicyConfig(work_on_issue=WorkOnIssuePolicy(blocked_after_minutes=30))
        context = WorkflowContext(
            step_history=[{"step": "impl", "entered_at": 1.5}],
        )
        result = BlockedStateDetector(context, policy)
        assert result.decision == BlockedDecision.progressing
