"""Tests for filter_eligible_prs."""

from typing import Any

from agentic_devtools.cli.ci.scheduler import EligiblePR, filter_eligible_prs


class TestFilterEligiblePrs:
    """Tests for the filter_eligible_prs pure function."""

    def test_eligible_pr_passes_through(self) -> None:
        prs = [{"number": 100, "createdAt": "2024-01-01T00:00:00Z", "isCrossRepository": False, "labels": []}]
        result = filter_eligible_prs(prs)
        assert result == [EligiblePR(number=100, created_at="2024-01-01T00:00:00Z")]

    def test_skip_fork_pr(self) -> None:
        prs = [{"number": 100, "createdAt": "2024-01-01T00:00:00Z", "isCrossRepository": True, "labels": []}]
        assert filter_eligible_prs(prs) == []

    def test_skip_ignored_label(self) -> None:
        prs = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [{"name": "ai-pr-loop-ignore"}],
            }
        ]
        assert filter_eligible_prs(prs) == []

    def test_skip_human_blocked(self) -> None:
        prs = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [],
                "is_human_blocked": True,
            }
        ]
        assert filter_eligible_prs(prs) == []

    def test_keeps_human_blocked_when_requested(self) -> None:
        prs = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [],
                "is_human_blocked": True,
            }
        ]
        assert filter_eligible_prs(prs, exclude_human_blocked=False) == [
            EligiblePR(number=100, created_at="2024-01-01T00:00:00Z")
        ]

    def test_preserves_creation_order(self) -> None:
        prs = [
            {"number": 3, "createdAt": "2024-01-03T00:00:00Z", "isCrossRepository": False, "labels": []},
            {"number": 1, "createdAt": "2024-01-01T00:00:00Z", "isCrossRepository": False, "labels": []},
            {"number": 2, "createdAt": "2024-01-02T00:00:00Z", "isCrossRepository": False, "labels": []},
        ]
        result = filter_eligible_prs(prs)
        assert [pr.number for pr in result] == [3, 1, 2]  # Preserves input order

    def test_empty_input(self) -> None:
        assert filter_eligible_prs([]) == []

    def test_custom_skip_label(self) -> None:
        prs = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [{"name": "custom-skip"}],
            }
        ]
        assert filter_eligible_prs(prs, skip_label="custom-skip") == []

    def test_mixed_eligible_and_ineligible(self) -> None:
        prs = [
            {"number": 1, "createdAt": "2024-01-01T00:00:00Z", "isCrossRepository": True, "labels": []},
            {"number": 2, "createdAt": "2024-01-02T00:00:00Z", "isCrossRepository": False, "labels": []},
            {
                "number": 3,
                "createdAt": "2024-01-03T00:00:00Z",
                "isCrossRepository": False,
                "labels": [{"name": "ai-pr-loop-ignore"}],
            },
            {"number": 4, "createdAt": "2024-01-04T00:00:00Z", "isCrossRepository": False, "labels": []},
        ]
        result = filter_eligible_prs(prs)
        assert [pr.number for pr in result] == [2, 4]

    def test_skips_non_positive_or_invalid_numbers(self) -> None:
        prs = [
            {"number": 0, "createdAt": "2024-01-01T00:00:00Z", "isCrossRepository": False, "labels": []},
            {"number": -1, "createdAt": "2024-01-02T00:00:00Z", "isCrossRepository": False, "labels": []},
            {"number": "abc", "createdAt": "2024-01-03T00:00:00Z", "isCrossRepository": False, "labels": []},
            {"number": 5, "createdAt": "2024-01-04T00:00:00Z", "isCrossRepository": False, "labels": []},
        ]
        result = filter_eligible_prs(prs)
        assert [pr.number for pr in result] == [5]

    def test_skips_non_string_non_int_number_values(self) -> None:
        prs: list[dict[str, Any]] = [
            {"number": None, "createdAt": "2024-01-01T00:00:00Z", "isCrossRepository": False, "labels": []},
            {"number": True, "createdAt": "2024-01-02T00:00:00Z", "isCrossRepository": False, "labels": []},
            {"number": {"value": 7}, "createdAt": "2024-01-03T00:00:00Z", "isCrossRepository": False, "labels": []},
            {"number": 8, "createdAt": "2024-01-04T00:00:00Z", "isCrossRepository": False, "labels": []},
        ]
        result = filter_eligible_prs(prs)
        assert [pr.number for pr in result] == [8]

    def test_coerces_non_string_createdat_to_string_or_empty(self) -> None:
        prs: list[dict[str, Any]] = [
            {"number": 100, "createdAt": None, "isCrossRepository": False, "labels": []},
            {"number": 101, "createdAt": 1704067200, "isCrossRepository": False, "labels": []},
        ]
        result = filter_eligible_prs(prs)
        assert result == [
            EligiblePR(number=100, created_at=""),
            EligiblePR(number=101, created_at="1704067200"),
        ]

    def test_treats_non_list_labels_as_empty(self) -> None:
        prs: list[dict[str, Any]] = [
            {"number": 100, "createdAt": "2024-01-01T00:00:00Z", "isCrossRepository": False, "labels": None}
        ]
        result = filter_eligible_prs(prs)
        assert result == [EligiblePR(number=100, created_at="2024-01-01T00:00:00Z")]

    def test_excludes_copilot_branch_when_touching_audit_agent_output(self) -> None:
        prs = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [],
                "headRefName": "copilot/auditbatch-123",
                "touches_audit_agent_output": True,
            }
        ]
        assert filter_eligible_prs(prs) == []

    def test_keeps_audit_handoff_when_requested(self) -> None:
        prs = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [],
                "headRefName": "copilot/auditbatch-123",
                "touches_audit_agent_output": True,
            }
        ]
        assert filter_eligible_prs(prs, exclude_audit_handoff=False) == [
            EligiblePR(number=100, created_at="2024-01-01T00:00:00Z")
        ]

    def test_keeps_copilot_branch_when_not_touching_audit_agent_output(self) -> None:
        prs = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [],
                "headRefName": "copilot/feature-123",
                "touches_audit_agent_output": False,
            }
        ]
        assert filter_eligible_prs(prs) == [EligiblePR(number=100, created_at="2024-01-01T00:00:00Z")]

    def test_keeps_non_copilot_branch_even_when_touching_audit_agent_output(self) -> None:
        prs = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [],
                "headRefName": "feature/audit-output-fix",
                "touches_audit_agent_output": True,
            }
        ]
        assert filter_eligible_prs(prs) == [EligiblePR(number=100, created_at="2024-01-01T00:00:00Z")]

    def test_keeps_copilot_branch_when_enrichment_fails_open(self) -> None:
        prs = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [],
                "headRefName": "copilot/auditbatch-123",
            }
        ]
        assert filter_eligible_prs(prs) == [EligiblePR(number=100, created_at="2024-01-01T00:00:00Z")]

    def test_carries_labels_to_propagate_through(self) -> None:
        prs: list[dict[str, Any]] = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [],
                "labels_to_propagate": ["ai-auto-merge-allowed", "suppressed-comment-follow-up"],
            }
        ]
        assert filter_eligible_prs(prs) == [
            EligiblePR(
                number=100,
                created_at="2024-01-01T00:00:00Z",
                labels_to_propagate=("ai-auto-merge-allowed", "suppressed-comment-follow-up"),
            )
        ]

    def test_drops_non_string_labels_to_propagate_entries(self) -> None:
        prs: list[dict[str, Any]] = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [],
                "labels_to_propagate": ["ai-auto-merge-allowed", None, "", 7],
            }
        ]
        result = filter_eligible_prs(prs)
        assert result[0].labels_to_propagate == ("ai-auto-merge-allowed",)

    def test_treats_non_sequence_labels_to_propagate_as_empty(self) -> None:
        prs: list[dict[str, Any]] = [
            {
                "number": 100,
                "createdAt": "2024-01-01T00:00:00Z",
                "isCrossRepository": False,
                "labels": [],
                "labels_to_propagate": "ai-auto-merge-allowed",
            }
        ]
        result = filter_eligible_prs(prs)
        assert result[0].labels_to_propagate == ()
