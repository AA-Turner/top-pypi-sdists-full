"""Tests for GitHubActionsProvider.update_pr_title."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


@patch("agentic_devtools.cli.ci.github_provider._gh_api")
def test_updates_title_with_rest_api(mock_api) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider.update_pr_title(7, "Completed work")
    assert mock_api.call_args.kwargs["method"] == "PATCH"
    assert mock_api.call_args.kwargs["body"] == {"title": "Completed work"}


@pytest.mark.parametrize("title", ["", "  "])
def test_rejects_empty_title(title: str) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with pytest.raises(ValueError, match="non-empty"):
        provider.update_pr_title(7, title)
