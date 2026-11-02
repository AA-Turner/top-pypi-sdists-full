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

    def test_excludes_wip_failed_and_active_prs_but_keeps_retry_pending(self) -> None:
        prs = [
            {"number": 1, "title": "[WIP] failed", "labels": [], "agent_session_outcome": "failed"},
            {
                "number": 2,
                "title": "failed retry",
                "labels": [],
                "agent_session_outcome": "failed",
                "agent_retry_pending": True,
            },
            {"number": 3, "title": "active", "labels": [], "agent_session_outcome": "active"},
            {"number": 4, "title": "labelled", "labels": [{"name": "ai-pr-loop:agent-failed"}]},
            {
                "number": 5,
                "title": "[WIP] success",
                "labels": [],
                "agent_session_outcome": "finished",
                "is_draft": True,
                "files": ["a.py"],
            },
        ]
        assert [pr.number for pr in filter_eligible_prs(prs)] == [2, 5]

    def test_finished_wip_pr_with_changed_files_is_eligible(self) -> None:
        prs = [
            {
                "number": 1,
                "title": "[WIP] finished with changedFiles",
                "labels": [],
                "agent_session_outcome": "finished",
                "is_draft": True,
                "has_changes": True,
                "files": ["src/feature.py"],
            },
            {
                "number": 2,
                "title": "[WIP] finished with file list",
                "labels": [],
                "agent_session_outcome": "finished",
                "is_draft": True,
                "has_changes": False,
                "files": ["src/app.py"],
            },
        ]
        assert [pr.number for pr in filter_eligible_prs(prs)] == [1, 2]

    def test_excludes_unsafe_finished_wip_and_keeps_later_actionable_pr(self) -> None:
        prs = [
            {
                "number": 1,
                "title": "[WIP] finished Docker change",
                "labels": [],
                "agent_session_outcome": "finished",
                "is_draft": True,
                "has_changes": True,
                "files": ["Dockerfile"],
            },
            {
                "number": 2,
                "title": "[WIP] finished privileged-path change",
                "labels": [],
                "agent_session_outcome": "finished",
                "is_draft": True,
                "has_changes": True,
                "files": [".github/workflows/deploy.yml"],
            },
            {
                "number": 3,
                "title": "Later actionable PR",
                "labels": [],
                "agent_session_outcome": "finished",
                "files": ["src/feature.py"],
            },
        ]

        assert [pr.number for pr in filter_eligible_prs(prs)] == [3]

    def test_excludes_finished_wip_when_file_paths_are_unavailable(self) -> None:
        prs = [
            {
                "number": 1,
                "title": "[WIP] finished with unknown paths",
                "labels": [],
                "agent_session_outcome": "finished",
                "is_draft": True,
                "has_changes": True,
            },
            {
                "number": 2,
                "title": "Later actionable PR",
                "labels": [],
                "files": ["src/feature.py"],
            },
        ]

        assert [pr.number for pr in filter_eligible_prs(prs)] == [2]

    def test_excludes_finished_wip_pr_without_changes(self) -> None:
        prs = [
            {
                "number": 1,
                "title": "[WIP] finished without changes",
                "labels": [],
                "agent_session_outcome": "finished",
                "is_draft": True,
                "has_changes": False,
            },
        ]
        assert filter_eligible_prs(prs) == []

    def test_excludes_finished_wip_pr_that_is_not_a_draft(self) -> None:
        prs = [
            {
                "number": 1,
                "title": "[WIP] finished non-draft",
                "labels": [],
                "agent_session_outcome": "finished",
                "is_draft": False,
                "has_changes": True,
            },
        ]
        assert filter_eligible_prs(prs) == []

    def test_excludes_finished_wip_draft_with_empty_normalized_title(self) -> None:
        prs = [
            {
                "number": 1,
                "title": "[WIP]",
                "labels": [],
                "agent_session_outcome": "finished",
                "is_draft": True,
                "has_changes": True,
            },
            {
                "number": 2,
                "title": "[WIP]   ",
                "labels": [],
                "agent_session_outcome": "finished",
                "is_draft": True,
                "has_changes": True,
            },
        ]
        assert filter_eligible_prs(prs) == []

    def test_supervisor_can_include_failed_active_wip_and_labelled_prs(self) -> None:
        prs = [
            {
                "number": 1,
                "title": "[WIP] failed",
                "labels": [{"name": "ai-pr-loop:agent-failed"}],
                "agent_session_outcome": "failed",
            },
            {"number": 2, "title": "active", "labels": [], "agent_session_outcome": "active"},
        ]
        assert [
            pr.number
            for pr in filter_eligible_prs(
                prs,
                exclude_wip=False,
                exclude_agent_failed=False,
                exclude_agent_active=False,
            )
        ] == [1, 2]

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
