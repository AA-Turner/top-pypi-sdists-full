"""Tests for GitHubActionsProvider.get_pr_body."""

import json
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


@patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps({"body": "description"}))
def test_returns_pull_request_description(_mock_api) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    assert provider.get_pr_body(7) == "description"


@patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps({"body": None}))
def test_non_string_body_degrades_to_empty(_mock_api) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    assert provider.get_pr_body(7) == ""
