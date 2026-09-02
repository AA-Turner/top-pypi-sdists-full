"""Tests for _linked_issue_label_names."""

from typing import Any

from agentic_devtools.cli.ci.github_provider import _linked_issue_label_names


class TestLinkedIssueLabelNames:
    """Tests for the _linked_issue_label_names GraphQL payload reader."""

    def test_returns_label_names_from_single_linked_issue(self) -> None:
        node: dict[str, Any] = {
            "closingIssuesReferences": {
                "nodes": [{"labels": {"nodes": [{"name": "ai-auto-merge-allowed"}, {"name": "Subtask"}]}}]
            }
        }
        assert _linked_issue_label_names(node) == ["ai-auto-merge-allowed", "Subtask"]

    def test_aggregates_labels_across_linked_issues(self) -> None:
        node: dict[str, Any] = {
            "closingIssuesReferences": {
                "nodes": [
                    {"labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]}},
                    {"labels": {"nodes": [{"name": "suppressed-comment-follow-up"}]}},
                ]
            }
        }
        assert _linked_issue_label_names(node) == [
            "ai-auto-merge-allowed",
            "suppressed-comment-follow-up",
        ]

    def test_missing_references_returns_empty(self) -> None:
        assert _linked_issue_label_names({}) == []

    def test_non_dict_references_returns_empty(self) -> None:
        assert _linked_issue_label_names({"closingIssuesReferences": None}) == []

    def test_non_list_issue_nodes_returns_empty(self) -> None:
        assert _linked_issue_label_names({"closingIssuesReferences": {"nodes": None}}) == []

    def test_empty_issue_nodes_returns_empty(self) -> None:
        assert _linked_issue_label_names({"closingIssuesReferences": {"nodes": []}}) == []

    def test_skips_malformed_entries(self) -> None:
        node: dict[str, Any] = {
            "closingIssuesReferences": {
                "nodes": [
                    "not-a-dict",
                    {"labels": None},
                    {"labels": {"nodes": None}},
                    {"labels": {"nodes": ["not-a-dict", {"name": None}, {"name": ""}, {}]}},
                    {"labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]}},
                ]
            }
        }
        assert _linked_issue_label_names(node) == ["ai-auto-merge-allowed"]
