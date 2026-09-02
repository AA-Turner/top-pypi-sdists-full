"""Tests for evaluate_decision()."""

from agentic_devtools.orchestration.review.decision_policy import (
    ReviewDecisionPolicy,
    evaluate_decision,
)


class TestEvaluateDecision:
    """Tests for threshold evaluation logic."""

    def test_approve_when_under_all_thresholds(self) -> None:
        """Approves when all counts are within thresholds."""
        policy = ReviewDecisionPolicy(max_high_severity=1, max_medium_severity=5)
        assert evaluate_decision(policy, high_count=0, medium_count=3, low_count=10) == "approve"

    def test_request_changes_when_high_exceeded(self) -> None:
        """Requests changes when high-severity threshold is exceeded."""
        policy = ReviewDecisionPolicy(max_high_severity=0)
        assert evaluate_decision(policy, high_count=1, medium_count=0, low_count=0) == "request-changes"

    def test_request_changes_when_medium_exceeded(self) -> None:
        """Requests changes when medium-severity threshold is exceeded."""
        policy = ReviewDecisionPolicy(max_medium_severity=2)
        assert evaluate_decision(policy, high_count=0, medium_count=3, low_count=0) == "request-changes"

    def test_request_changes_when_low_exceeded(self) -> None:
        """Requests changes when low-severity threshold is exceeded."""
        policy = ReviewDecisionPolicy(max_low_severity=5)
        assert evaluate_decision(policy, high_count=0, medium_count=0, low_count=6) == "request-changes"

    def test_null_threshold_bypassed(self) -> None:
        """None threshold means unlimited — never triggers request-changes."""
        policy = ReviewDecisionPolicy(
            max_high_severity=0,
            max_medium_severity=None,
            max_low_severity=None,
        )
        # No high findings, but many medium/low — should still approve
        assert evaluate_decision(policy, high_count=0, medium_count=100, low_count=200) == "approve"

    def test_default_policy_approves_clean_pr(self) -> None:
        """Default policy approves a PR with no findings."""
        policy = ReviewDecisionPolicy()
        assert evaluate_decision(policy, high_count=0, medium_count=0, low_count=0) == "approve"

    def test_default_policy_rejects_any_high(self) -> None:
        """Default policy (max_high=0) rejects any high-severity finding."""
        policy = ReviewDecisionPolicy()
        assert evaluate_decision(policy, high_count=1, medium_count=0, low_count=0) == "request-changes"

    def test_zero_threshold_means_zero_allowed(self) -> None:
        """A threshold of 0 means zero findings of that severity are allowed."""
        policy = ReviewDecisionPolicy(max_high_severity=0, max_medium_severity=0)
        assert evaluate_decision(policy, high_count=0, medium_count=1, low_count=0) == "request-changes"

    def test_exact_threshold_is_approve(self) -> None:
        """Exactly hitting the threshold (not exceeding) still approves."""
        policy = ReviewDecisionPolicy(max_high_severity=2)
        assert evaluate_decision(policy, high_count=2, medium_count=0, low_count=0) == "approve"
