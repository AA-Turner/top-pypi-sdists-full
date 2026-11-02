"""Tests for _validated_linked_issue_label_names."""

from __future__ import annotations

from typing import Any

import pytest

from agentic_devtools.cli.ci.github_provider import _validated_linked_issue_label_names


def _base_pr_node() -> dict[str, Any]:
    return {
        "closingIssuesReferences": {
            "pageInfo": {"hasNextPage": False},
            "nodes": [
                {
                    "labels": {
                        "pageInfo": {"hasNextPage": False},
                        "nodes": [{"name": "suppressed-comment-follow-up"}],
                    }
                }
            ],
        }
    }


class TestValidatedLinkedIssueLabelNames:
    """Tests for the strict linked-issue label reader."""

    @pytest.mark.parametrize(
        ("mutator", "match"),
        [
            (
                lambda node: node["closingIssuesReferences"].update({"pageInfo": None}),
                "closingIssuesReferences.pageInfo",
            ),
            (lambda node: node["closingIssuesReferences"].update({"nodes": None}), "closingIssuesReferences.nodes"),
            (lambda node: node["closingIssuesReferences"]["nodes"][0].update({"labels": None}), ".labels"),
            (
                lambda node: node["closingIssuesReferences"]["nodes"][0]["labels"].update({"pageInfo": None}),
                ".labels.pageInfo",
            ),
            (
                lambda node: node["closingIssuesReferences"]["nodes"][0]["labels"].update({"nodes": None}),
                ".labels.nodes",
            ),
            (
                lambda node: node["closingIssuesReferences"]["nodes"][0]["labels"].update({"nodes": ["bad-node"]}),
                ".labels.nodes\\[0\\]",
            ),
            (
                lambda node: node["closingIssuesReferences"]["nodes"][0]["labels"].update({"nodes": [{"name": None}]}),
                ".labels.nodes\\[0\\].name",
            ),
        ],
    )
    def test_raises_on_malformed_nested_shapes(self, mutator, match: str) -> None:
        node = _base_pr_node()
        mutator(node)

        with pytest.raises(RuntimeError, match=match):
            _validated_linked_issue_label_names(node, pr_number=11)

    def test_raises_when_closing_issue_references_are_truncated(self) -> None:
        node = _base_pr_node()
        node["closingIssuesReferences"]["pageInfo"]["hasNextPage"] = True

        with pytest.raises(RuntimeError, match="more than 100 closing issue references"):
            _validated_linked_issue_label_names(node, pr_number=11)

    def test_raises_when_closing_issue_references_has_next_page_is_not_bool(self) -> None:
        node = _base_pr_node()
        node["closingIssuesReferences"]["pageInfo"]["hasNextPage"] = None

        with pytest.raises(RuntimeError, match="closingIssuesReferences.pageInfo.hasNextPage"):
            _validated_linked_issue_label_names(node, pr_number=11)

    def test_raises_when_linked_issue_labels_are_truncated(self) -> None:
        node = _base_pr_node()
        node["closingIssuesReferences"]["nodes"][0]["labels"]["pageInfo"]["hasNextPage"] = True

        with pytest.raises(RuntimeError, match="more than 100 labels"):
            _validated_linked_issue_label_names(node, pr_number=11)

    def test_raises_when_linked_issue_labels_has_next_page_is_not_bool(self) -> None:
        node = _base_pr_node()
        node["closingIssuesReferences"]["nodes"][0]["labels"]["pageInfo"]["hasNextPage"] = None

        with pytest.raises(RuntimeError, match=r"\.labels\.pageInfo\.hasNextPage"):
            _validated_linked_issue_label_names(node, pr_number=11)

    def test_returns_labels_and_ignores_empty_names(self) -> None:
        node = _base_pr_node()
        node["closingIssuesReferences"]["nodes"][0]["labels"]["nodes"] = [
            {"name": ""},
            {"name": "suppressed-comment-follow-up"},
        ]

        assert _validated_linked_issue_label_names(node, pr_number=11) == ["suppressed-comment-follow-up"]
