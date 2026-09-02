"""Tests for ApprovalEvaluator."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.policies.approval import ApprovalEvaluator
from agentic_devtools.orchestration.policies.config import PolicyConfig, PRReviewPolicy
from agentic_devtools.orchestration.policies.types import ApprovalDecision


class TestApprovalEvaluatorAcceptance:
    """Acceptance scenarios from User Story 1."""

    def test_high_severity_blocks(self) -> None:
        """US1 Scenario 1: 1 high + 2 medium -> request_changes (high blocks)."""
        policy = PolicyConfig()
        findings = [
            {"severity": "high", "description": "Critical bug"},
            {"severity": "medium", "description": "Minor issue 1"},
            {"severity": "medium", "description": "Minor issue 2"},
        ]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.request_changes
        assert "high" in result.rationale.lower()

    def test_thresholds_satisfied_approves(self) -> None:
        """US1 Scenario 2: 0 high + 2 medium -> approve."""
        policy = PolicyConfig()
        findings = [
            {"severity": "medium", "description": "Issue 1"},
            {"severity": "medium", "description": "Issue 2"},
        ]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.approve

    def test_boundary_match_approves(self) -> None:
        """US1 Scenario 3: exactly 3 medium (boundary) -> approve (> not >=)."""
        policy = PolicyConfig()
        findings = [{"severity": "medium", "description": f"Issue {i}"} for i in range(3)]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.approve

    def test_low_confidence_escalates(self) -> None:
        """US1 Scenario 4: confidence 0.55 < 0.7 minimum -> escalate."""
        policy = PolicyConfig()
        findings = [{"severity": "low", "description": "Minor"}]
        result = ApprovalEvaluator(findings, confidence=0.55, policy=policy)
        assert result.decision == ApprovalDecision.escalate
        assert "0.55" in result.rationale
        assert "0.7" in result.rationale

    def test_confidence_meets_minimum(self) -> None:
        """US1 Scenario 5: confidence exactly 0.7 -> normal decision (not escalate)."""
        policy = PolicyConfig()
        findings = [{"severity": "low", "description": "Minor"}]
        result = ApprovalEvaluator(findings, confidence=0.7, policy=policy)
        assert result.decision != ApprovalDecision.escalate


class TestApprovalEvaluatorBoundary:
    """Boundary and matrix tests covering severity×confidence combinations."""

    @pytest.mark.parametrize(
        ("high", "medium", "confidence", "expected"),
        [
            (0, 0, 0.9, ApprovalDecision.approve),
            (0, 3, 0.9, ApprovalDecision.approve),
            (0, 4, 0.9, ApprovalDecision.request_changes),
            (1, 0, 0.9, ApprovalDecision.request_changes),
            (0, 0, 0.5, ApprovalDecision.escalate),
            (1, 4, 0.9, ApprovalDecision.request_changes),
            (0, 0, 0.7, ApprovalDecision.approve),
            (0, 0, 0.69, ApprovalDecision.escalate),
            (0, 1, 0.8, ApprovalDecision.approve),
            (0, 2, 0.9, ApprovalDecision.approve),
            (0, 3, 0.71, ApprovalDecision.approve),
            (1, 3, 0.9, ApprovalDecision.request_changes),
            (2, 0, 0.9, ApprovalDecision.request_changes),
            (0, 5, 0.9, ApprovalDecision.request_changes),
            (0, 10, 0.9, ApprovalDecision.request_changes),
        ],
    )
    def test_severity_confidence_matrix(
        self, high: int, medium: int, confidence: float, expected: ApprovalDecision
    ) -> None:
        policy = PolicyConfig()
        findings = [{"severity": "high", "description": f"H{i}"} for i in range(high)]
        findings += [{"severity": "medium", "description": f"M{i}"} for i in range(medium)]
        result = ApprovalEvaluator(findings, confidence=confidence, policy=policy)
        assert result.decision == expected

    def test_empty_findings_approves(self) -> None:
        policy = PolicyConfig()
        result = ApprovalEvaluator([], confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.approve

    def test_low_severity_informational_only(self) -> None:
        """Low-severity findings never block approval."""
        policy = PolicyConfig()
        findings = [{"severity": "low", "description": f"Info {i}"} for i in range(100)]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.approve

    def test_low_count_in_approve_metadata(self) -> None:
        """low_count is included in metadata for the approve path."""
        policy = PolicyConfig()
        findings = [
            {"severity": "low", "description": "Info 1"},
            {"severity": "low", "description": "Info 2"},
            {"severity": "medium", "description": "Medium 1"},
        ]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.approve
        assert result.metadata["low_count"] == 2

    def test_low_count_in_request_changes_high_metadata(self) -> None:
        """low_count is included in metadata when high-severity threshold is exceeded."""
        policy = PolicyConfig()
        findings = [
            {"severity": "high", "description": "High finding"},
            {"severity": "low", "description": "Info 1"},
        ]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.request_changes
        assert result.metadata["low_count"] == 1

    def test_low_count_in_request_changes_medium_metadata(self) -> None:
        """low_count is included in metadata when medium-severity threshold is exceeded."""
        policy = PolicyConfig()
        findings = [{"severity": "medium", "description": f"M{i}"} for i in range(4)] + [
            {"severity": "low", "description": "Info 1"}
        ]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.request_changes
        assert result.metadata["low_count"] == 1

    def test_critical_severity_counts_as_high(self) -> None:
        """Critical findings must block the same as high-severity findings."""
        policy = PolicyConfig()
        findings = [{"severity": "critical", "description": "Critical auth bypass"}]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.request_changes
        assert result.metadata["high_count"] == 1


class TestApprovalEvaluatorEscalation:
    """Escalation trigger tests (User Story 4)."""

    def test_trigger_match_in_description(self) -> None:
        """US4 Scenario 1: Trigger pattern matched -> escalate."""
        policy = PolicyConfig(pr_review=PRReviewPolicy(escalation_triggers=("security vulnerability detected",)))
        findings = [
            {"severity": "low", "description": "SQL injection security vulnerability detected in user input handler"},
            {"severity": "low", "description": "Minor formatting issue"},
            {"severity": "low", "description": "Comment typo"},
            {"severity": "low", "description": "Unused variable"},
            {"severity": "low", "description": "Long line"},
        ]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.escalate
        assert "security vulnerability detected" in result.rationale.lower()

    def test_no_triggers_configured_no_escalation(self) -> None:
        """US4 Scenario 2: No triggers configured -> normal threshold logic."""
        policy = PolicyConfig()
        findings = [
            {"severity": "medium", "description": "security issue found"},
            {"severity": "medium", "description": "another security concern"},
            {"severity": "medium", "description": "security fix needed"},
        ]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.approve  # 3 medium <= 3 max

    def test_multiple_triggers_matched(self) -> None:
        """US4 Scenario 3: Multiple triggers matched, both reported."""
        policy = PolicyConfig(
            pr_review=PRReviewPolicy(escalation_triggers=("security vulnerability", "breaking change"))
        )
        findings = [
            {"severity": "low", "description": "Found security vulnerability in auth"},
            {"severity": "low", "description": "This is a breaking change to API"},
        ]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.escalate
        assert "security vulnerability" in result.rationale.lower()
        assert "breaking change" in result.rationale.lower()

    def test_case_insensitive_matching(self) -> None:
        policy = PolicyConfig(pr_review=PRReviewPolicy(escalation_triggers=("Security Vulnerability",)))
        findings = [{"severity": "low", "description": "SECURITY VULNERABILITY found"}]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.escalate

    @pytest.mark.parametrize("description", [None, 12345])
    def test_non_string_descriptions_do_not_crash(self, description: object) -> None:
        """Unexpected description types should be tolerated during trigger matching."""
        policy = PolicyConfig(pr_review=PRReviewPolicy(escalation_triggers=("security",)))
        findings = [{"severity": "low", "description": description}]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.approve

    def test_trigger_takes_precedence_over_thresholds(self) -> None:
        """US4 T020: Triggers take precedence even when thresholds would permit."""
        policy = PolicyConfig(
            pr_review=PRReviewPolicy(
                max_high_severity=5,
                max_medium_severity=10,
                escalation_triggers=("critical pattern",),
            )
        )
        findings = [{"severity": "low", "description": "Has critical pattern inside"}]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.escalate

    def test_triggers_configured_but_none_match(self) -> None:
        """Triggers configured but no findings match -> normal threshold logic (branch 43->55)."""
        policy = PolicyConfig(pr_review=PRReviewPolicy(escalation_triggers=("security vulnerability",)))
        findings = [{"severity": "low", "description": "Minor formatting issue"}]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.approve

    def test_duplicate_trigger_match_deduplication(self) -> None:
        """Same trigger matched by multiple findings is deduplicated (branch 41->39)."""
        policy = PolicyConfig(pr_review=PRReviewPolicy(escalation_triggers=("security",)))
        findings = [
            {"severity": "low", "description": "security issue in auth"},
            {"severity": "low", "description": "security issue in api"},
        ]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.escalate
        assert result.rationale.count('"security"') == 1

    def test_long_trigger_rationale_is_truncated_to_500_chars(self) -> None:
        """Rationale built from a very long trigger string is capped at 500 chars."""
        long_trigger = "a" * 450  # produces rationale > 500 chars before truncation
        policy = PolicyConfig(pr_review=PRReviewPolicy(escalation_triggers=(long_trigger,)))
        findings = [{"severity": "low", "description": long_trigger}]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.decision == ApprovalDecision.escalate
        assert len(result.rationale) <= 500
        assert result.rationale.endswith("...")

    def test_matched_triggers_metadata_is_immutable_tuple(self) -> None:
        """Escalation metadata stores triggers in an immutable container."""
        policy = PolicyConfig(pr_review=PRReviewPolicy(escalation_triggers=("security",)))
        findings = [{"severity": "low", "description": "security issue found"}]
        result = ApprovalEvaluator(findings, confidence=0.9, policy=policy)
        assert result.metadata["matched_triggers"] == ("security",)


class TestApprovalEvaluatorInvalidConfidence:
    """Guard against NaN, inf, and out-of-range confidence values."""

    @pytest.mark.parametrize(
        "confidence",
        [
            float("nan"),
            float("inf"),
            float("-inf"),
            -0.001,
            1.001,
        ],
    )
    def test_non_finite_or_out_of_range_confidence_escalates(self, confidence: float) -> None:
        """NaN, inf, or out-of-range confidence must always escalate, not silently approve."""
        policy = PolicyConfig()
        result = ApprovalEvaluator([], confidence=confidence, policy=policy)
        assert result.decision == ApprovalDecision.escalate
        assert "not a valid score" in result.rationale

    def test_nan_confidence_metadata_contains_string_representation(self) -> None:
        """NaN confidence stored as string in metadata to avoid JSON-serialization issues."""
        policy = PolicyConfig()
        result = ApprovalEvaluator([], confidence=float("nan"), policy=policy)
        assert result.metadata["confidence"] == "nan"

    def test_inf_confidence_metadata_contains_string_representation(self) -> None:
        """Inf confidence stored as string in metadata to avoid JSON-serialization issues."""
        policy = PolicyConfig()
        result = ApprovalEvaluator([], confidence=float("inf"), policy=policy)
        assert result.metadata["confidence"] == "inf"

    def test_boundary_zero_confidence_uses_normal_minimum_check(self) -> None:
        """confidence=0.0 is a valid value and goes through the normal minimum check."""
        policy = PolicyConfig()
        result = ApprovalEvaluator([], confidence=0.0, policy=policy)
        # 0.0 < 0.7 minimum → escalate via normal confidence path, not the guard
        assert result.decision == ApprovalDecision.escalate
        assert "Confidence 0.0" in result.rationale

    def test_boundary_one_confidence_is_valid(self) -> None:
        """confidence=1.0 is valid and proceeds through normal evaluation."""
        policy = PolicyConfig()
        result = ApprovalEvaluator([], confidence=1.0, policy=policy)
        assert result.decision == ApprovalDecision.approve
