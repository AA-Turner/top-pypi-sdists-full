"""Tests for summarize_and_decide_node()."""

from agentic_devtools.orchestration.review.nodes.summarize_and_decide import (
    summarize_and_decide_node,
)


class TestSummarizeAndDecideNode:
    """Tests for the summarize_and_decide node."""

    def test_empty_results_auto_approves(self) -> None:
        """Empty file_results with no errors produces auto-approval."""
        result = summarize_and_decide_node({"file_results": [], "config": {}})
        assert result["overall_decision"] == "approve"
        assert "No files to review" in result["summary"]

    def test_empty_results_with_upstream_errors_requests_changes(self) -> None:
        """Empty file_results with upstream errors defaults to request-changes, not approve."""
        result = summarize_and_decide_node(
            {
                "file_results": [],
                "config": {},
                "errors": ["fetch_pr_details: auth failure"],
            }
        )
        assert result["overall_decision"] == "request-changes"
        assert "errors" in result["summary"].lower() or "error" in result["summary"].lower()

    def test_empty_results_with_empty_errors_list_auto_approves(self) -> None:
        """Explicit empty errors list still produces auto-approval for empty file_results."""
        result = summarize_and_decide_node({"file_results": [], "config": {}, "errors": []})
        assert result["overall_decision"] == "approve"
        assert "No files to review" in result["summary"]

    def test_all_approved_files(self) -> None:
        """All approved files produce approve decision."""
        result = summarize_and_decide_node(
            {
                "file_results": [
                    {"outcome": "approve", "summary": "Good", "suggestions": []},
                    {"outcome": "approve", "summary": "Clean", "suggestions": []},
                ],
                "config": {},
            }
        )
        assert result["overall_decision"] == "approve"
        assert "2 approved" in result["summary"]

    def test_needs_work_file_with_high_severity(self) -> None:
        """High-severity finding triggers request-changes."""
        result = summarize_and_decide_node(
            {
                "file_results": [
                    {
                        "outcome": "request-changes",
                        "summary": "Bug found",
                        "suggestions": [{"severity": "high", "content": "Critical bug"}],
                    },
                ],
                "config": {},
            }
        )
        assert result["overall_decision"] == "request-changes"

    def test_cascade_mixed_statuses(self) -> None:
        """Mixed statuses cascade correctly."""
        result = summarize_and_decide_node(
            {
                "file_results": [
                    {"outcome": "approve", "summary": "OK", "suggestions": []},
                    {
                        "outcome": "request-changes",
                        "summary": "Issues",
                        "suggestions": [{"severity": "low", "content": "Minor"}],
                    },
                ],
                "config": {},
            }
        )
        assert result["overall_decision"] == "request-changes"
        assert "1 need work" in result["summary"]

    def test_custom_policy_from_config(self) -> None:
        """Custom decision policy from config is applied."""
        result = summarize_and_decide_node(
            {
                "file_results": [
                    {
                        "outcome": "request-changes",
                        "summary": "Found issues",
                        "suggestions": [
                            {"severity": "medium", "content": "Issue 1"},
                            {"severity": "medium", "content": "Issue 2"},
                            {"severity": "medium", "content": "Issue 3"},
                        ],
                    },
                ],
                "config": {
                    "review": {
                        "decision-policy": {
                            "max-medium-severity": 2,
                        }
                    }
                },
            }
        )
        assert result["overall_decision"] == "request-changes"

    def test_decision_policy_underscore_alias_accepted(self) -> None:
        """decision_policy (underscore) is accepted as an alias for decision-policy (hyphen)."""
        result = summarize_and_decide_node(
            {
                "file_results": [
                    {
                        "outcome": "request-changes",
                        "summary": "Found issues",
                        "suggestions": [
                            {"severity": "medium", "content": "Issue 1"},
                            {"severity": "medium", "content": "Issue 2"},
                            {"severity": "medium", "content": "Issue 3"},
                        ],
                    },
                ],
                "config": {
                    "review": {
                        "decision_policy": {
                            "max-medium-severity": 2,
                        }
                    }
                },
            }
        )
        assert result["overall_decision"] == "request-changes"

    def test_hyphenated_policy_null_takes_precedence_over_underscore(self) -> None:
        """decision-policy: null takes precedence; underscore alias must NOT be used as fallback."""
        # decision-policy is explicitly null (key present, value None).
        # underscore alias has max-high-severity=0 which would force request-changes.
        # Correct behaviour: key presence wins → null resolves to default policy → approve.
        result = summarize_and_decide_node(
            {
                "file_results": [
                    {"outcome": "approve", "summary": "OK", "suggestions": []},
                ],
                "config": {
                    "review": {
                        "decision-policy": None,
                        "decision_policy": {"max-high-severity": 0},
                    }
                },
            }
        )
        # hyphenated null key wins; underscore alias ignored → default policy → approve
        assert result["overall_decision"] == "approve"

    def test_hyphenated_policy_takes_precedence_over_underscore(self) -> None:
        """When both spellings are present, decision-policy (hyphen) takes precedence."""
        # hyphenated policy allows unlimited medium severity (None = unlimited),
        # underscore policy would block with max-medium-severity=0.
        result = summarize_and_decide_node(
            {
                "file_results": [
                    {
                        "outcome": "approve",
                        "summary": "OK",
                        "suggestions": [
                            {"severity": "medium", "content": "Minor note"},
                        ],
                    },
                ],
                "config": {
                    "review": {
                        "decision-policy": {"max-medium-severity": None},
                        "decision_policy": {"max-medium-severity": 0},
                    }
                },
            }
        )
        # hyphenated policy (unlimited medium) wins → should approve
        assert result["overall_decision"] == "approve"

    def test_non_dict_review_config_uses_default_policy(self) -> None:
        """When config['review'] is not a dict the default policy is applied."""
        result = summarize_and_decide_node(
            {
                "file_results": [
                    {"outcome": "approve", "summary": "OK", "suggestions": []},
                ],
                "config": {"review": "unexpected-string-value"},
            }
        )
        # Default policy should still allow approve when all files are approved
        assert result["overall_decision"] == "approve"

    def test_upstream_errors_with_file_results_forces_request_changes(self) -> None:
        """Non-empty errors list forces request-changes even when all files are approved."""
        result = summarize_and_decide_node(
            {
                "file_results": [
                    {"outcome": "approve", "summary": "Clean", "suggestions": []},
                    {"outcome": "approve", "summary": "OK", "suggestions": []},
                ],
                "config": {},
                "errors": ["scaffold_comments: ADO connection failure"],
            }
        )
        assert result["overall_decision"] == "request-changes"
        assert "error" in result["summary"].lower()

    def test_upstream_errors_note_absent_when_no_errors(self) -> None:
        """Summary does not include an error note when errors list is empty."""
        result = summarize_and_decide_node(
            {
                "file_results": [
                    {"outcome": "approve", "summary": "Clean", "suggestions": []},
                ],
                "config": {},
                "errors": [],
            }
        )
        assert result["overall_decision"] == "approve"
        assert "upstream" not in result["summary"].lower()
