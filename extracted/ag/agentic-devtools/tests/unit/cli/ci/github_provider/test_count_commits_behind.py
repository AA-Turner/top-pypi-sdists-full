"""Tests for GitHubActionsProvider.count_commits_behind."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.retry import RetryableError


class TestCountCommitsBehind:
    """Tests for count_commits_behind method."""

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value='{"behind_by":3}')
    def test_uses_pooled_rest_api_endpoint(self, mock_gh_api) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.count_commits_behind(pr_number=1, base_branch="main", head_branch="feature") == 3

        mock_gh_api.assert_called_once_with("/repos/owner/repo/compare/main...feature")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value='{"behind_by":3}')
    def test_returns_count_on_success(self, mock_gh_api) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.count_commits_behind(pr_number=1, base_branch="main", head_branch="feature")

        assert result == 3
        assert "/repos/owner/repo/compare/main...feature" in mock_gh_api.call_args.args

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value='{"behind_by":3}')
    def test_url_encodes_branch_names(self, mock_gh_api) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        provider.count_commits_behind(pr_number=1, base_branch="release/v1", head_branch="feature/foo")

        assert mock_gh_api.call_args.args == ("/repos/owner/repo/compare/release%2Fv1...feature%2Ffoo",)

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RuntimeError("not found"))
    def test_raises_on_nonzero_returncode(self, _mock_gh_api) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="PR #1: compare API request failed"):
            provider.count_commits_behind(pr_number=1, base_branch="main", head_branch="feature")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RuntimeError("network error"))
    def test_raises_on_exception(self, _mock_gh_api) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="PR #1: compare API request failed"):
            provider.count_commits_behind(pr_number=1, base_branch="main", head_branch="feature")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RetryableError("rate limited"))
    def test_preserves_retryable_api_errors(self, _mock_gh_api) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RetryableError, match="rate limited"):
            provider.count_commits_behind(pr_number=1, base_branch="main", head_branch="feature")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="invalid")
    def test_raises_for_invalid_json(self, _mock_gh_api) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="compare API returned invalid JSON"):
            provider.count_commits_behind(pr_number=1, base_branch="main", head_branch="feature")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="[]")
    def test_raises_for_non_object_json(self, _mock_gh_api) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="compare API returned a non-object"):
            provider.count_commits_behind(pr_number=1, base_branch="main", head_branch="feature")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value='{"behind_by":null}')
    def test_returns_zero_on_empty_stdout(self, _mock_gh_api) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.count_commits_behind(pr_number=1, base_branch="main", head_branch="feature")

        assert result == 0
