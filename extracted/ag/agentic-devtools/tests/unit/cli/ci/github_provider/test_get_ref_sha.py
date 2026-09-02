"""Tests for GitHubActionsProvider.get_ref_sha()."""

import json
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _mock_run_safe_response(data: dict):
    class _Result:
        returncode = 0
        stdout = json.dumps(data)
        stderr = ""

    return _Result()


def _mock_error_response():
    class _Result:
        returncode = 1
        stdout = ""
        stderr = "Not Found"

    return _Result()


class TestGetRefSha:
    """Tests for GitHubActionsProvider.get_ref_sha()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_sha_for_existing_branch(self, mock_run_safe) -> None:
        """Returns the tip SHA for an existing branch."""
        mock_run_safe.return_value = _mock_run_safe_response(
            {"object": {"sha": "abcdef1234567890" * 2 + "abcdef12", "type": "commit"}}
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_ref_sha("main")

        assert result == "abcdef1234567890" * 2 + "abcdef12"
        args = mock_run_safe.call_args[0][0]
        assert any("/git/ref/heads/main" in a for a in args)

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_calls_correct_api_endpoint(self, mock_run_safe) -> None:
        """Calls the correct GitHub API endpoint."""
        mock_run_safe.return_value = _mock_run_safe_response({"object": {"sha": "abc123", "type": "commit"}})

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.get_ref_sha("feature/my-branch")

        args = mock_run_safe.call_args[0][0]
        assert any("feature%2Fmy-branch" in a or "feature/my-branch" in a for a in args)

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_empty_string_when_sha_absent(self, mock_run_safe) -> None:
        """Returns empty string when API response lacks 'object.sha'."""
        mock_run_safe.return_value = _mock_run_safe_response({"ref": "refs/heads/main"})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_ref_sha("main")

        assert result == ""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_returns_empty_string_when_api_call_fails(self, mock_gh_api) -> None:
        """Non-retryable API failures fall back to an empty string."""
        mock_gh_api.side_effect = RuntimeError("GitHub API error: Not Found")

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.get_ref_sha("missing-branch")

        assert result == ""
