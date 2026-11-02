"""Tests for GitHubActionsProvider.get_commit_author_login() method."""

import json
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _mock_run_safe_response(data: dict):
    """Create a mock run_safe return value with JSON response."""

    class _Result:
        returncode = 0
        stdout = json.dumps(data)
        stderr = ""

    return _Result()


class TestGetCommitAuthorLogin:
    """Tests for GitHubActionsProvider.get_commit_author_login()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_author_login(self, mock_run_safe) -> None:
        """Returns the GitHub login when the author maps to a user."""
        mock_run_safe.return_value = _mock_run_safe_response(
            {"author": {"login": "Copilot"}, "committer": {"login": "web-flow"}}
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.get_commit_author_login("abc123") == "Copilot"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_empty_when_author_login_missing(self, mock_run_safe) -> None:
        """Returns empty string when the author object lacks a login."""
        mock_run_safe.return_value = _mock_run_safe_response({"author": {"login": None}})
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.get_commit_author_login("abc123") == ""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_empty_when_author_is_null(self, mock_run_safe) -> None:
        """Returns empty string when author cannot be matched to a GitHub user."""
        mock_run_safe.return_value = _mock_run_safe_response({"author": None})
        provider = GitHubActionsProvider(repo="owner/repo")
        assert provider.get_commit_author_login("abc123") == ""
