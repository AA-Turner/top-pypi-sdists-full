"""Tests for GitHubActionsProvider.get_pr_tree_state()."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import PRMetadata

_METADATA = PRMetadata(number=7, title="t", head_branch="copilot/x", head_sha="head", base_branch="main")


def _api_responses(compare: dict, head_commit: dict):
    def _fake(endpoint: str, **_kwargs: object) -> str:
        if "/compare/" in endpoint:
            return json.dumps(compare)
        return json.dumps(head_commit)

    return _fake


class TestGetPrTreeState:
    """Tests for the tree-identity read that makes the empty-diff check authoritative."""

    def test_returns_merge_base_and_both_trees(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        compare = {"merge_base_commit": {"sha": "mb", "commit": {"tree": {"sha": "tree-1"}}}}
        with (
            patch.object(GitHubActionsProvider, "get_pr_metadata", return_value=_METADATA),
            patch.object(GitHubActionsProvider, "get_ref_sha", return_value="base-sha"),
            patch(
                "agentic_devtools.cli.ci.github_provider._gh_api",
                side_effect=_api_responses(compare, {"tree": {"sha": "tree-1"}}),
            ),
        ):
            state = provider.get_pr_tree_state(7)

        assert state.merge_base_sha == "mb"
        assert state.merge_base_tree_sha == "tree-1"
        assert state.head_tree_sha == "tree-1"
        assert state.head_sha == "head"
        assert state.tree_identical is True

    def test_reports_differing_trees(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        compare = {"merge_base_commit": {"sha": "mb", "commit": {"tree": {"sha": "tree-1"}}}}
        with (
            patch.object(GitHubActionsProvider, "get_pr_metadata", return_value=_METADATA),
            patch.object(GitHubActionsProvider, "get_ref_sha", return_value="base-sha"),
            patch(
                "agentic_devtools.cli.ci.github_provider._gh_api",
                side_effect=_api_responses(compare, {"tree": {"sha": "tree-2"}}),
            ),
        ):
            state = provider.get_pr_tree_state(7)

        assert state.tree_identical is False

    def test_missing_fields_degrade_to_empty_strings(self) -> None:
        """An absent merge base or tree must not be mistaken for an identical tree."""
        provider = GitHubActionsProvider(repo="o/r")
        with (
            patch.object(GitHubActionsProvider, "get_pr_metadata", return_value=_METADATA),
            patch.object(GitHubActionsProvider, "get_ref_sha", return_value="base-sha"),
            patch(
                "agentic_devtools.cli.ci.github_provider._gh_api",
                side_effect=_api_responses({}, {}),
            ),
        ):
            state = provider.get_pr_tree_state(7)

        assert state == type(state)(merge_base_sha="", merge_base_tree_sha="", head_tree_sha="", head_sha="head")
        assert state.tree_identical is False

    def test_null_commit_and_tree_nodes_degrade_to_empty_strings(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        compare = {"merge_base_commit": {"sha": "mb", "commit": None}}
        with (
            patch.object(GitHubActionsProvider, "get_pr_metadata", return_value=_METADATA),
            patch.object(GitHubActionsProvider, "get_ref_sha", return_value="base-sha"),
            patch(
                "agentic_devtools.cli.ci.github_provider._gh_api",
                side_effect=_api_responses(compare, {"tree": None}),
            ),
        ):
            state = provider.get_pr_tree_state(7)

        assert state.merge_base_tree_sha == ""
        assert state.head_tree_sha == ""

    def test_raises_when_the_base_branch_does_not_resolve(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with (
            patch.object(GitHubActionsProvider, "get_pr_metadata", return_value=_METADATA),
            patch.object(GitHubActionsProvider, "get_ref_sha", return_value=""),
        ):
            with pytest.raises(RuntimeError, match="Could not resolve base branch 'main' for PR #7"):
                provider.get_pr_tree_state(7)
