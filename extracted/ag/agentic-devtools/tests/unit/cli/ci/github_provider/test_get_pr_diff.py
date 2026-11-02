"""Tests for GitHubActionsProvider.get_pr_diff()."""

import os
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.credential_roles import DEFAULT_CLASSIC_REPO_WORKFLOW_PAT, GH_TOKEN
from agentic_devtools.cli.ci.exceptions import ProviderRateLimitError
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.retry import RetryableError


@pytest.fixture(autouse=True)
def configured_github_token(monkeypatch) -> None:
    monkeypatch.setenv(DEFAULT_CLASSIC_REPO_WORKFLOW_PAT, "test-workflow-token")
    monkeypatch.delenv(GH_TOKEN, raising=False)


class TestGetPrDiff:
    """Tests for PR diff retrieval."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="diff --git a/x b/x")
    def test_uses_pooled_rest_api_diff_endpoint(self, mock_gh_api, mock_run_safe):
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.get_pr_diff(42) == "diff --git a/x b/x"

        mock_gh_api.assert_called_once_with(
            "/repos/owner/repo/pulls/42",
            token="test-workflow-token",
            headers={"Accept": "application/vnd.github.v3.diff"},
            timeout_seconds=60,
        )
        mock_run_safe.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="diff --git a/x b/x")
    def test_returns_stdout_on_success(self, mock_gh_api):
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.get_pr_diff(42)

        assert result == "diff --git a/x b/x"
        assert mock_gh_api.call_args.kwargs["token"] == "test-workflow-token"

    def test_preserves_diff_context_that_resembles_response_headers(self):
        diff_body = (
            "diff --git a/x b/x\n@@ -1,3 +1,3 @@\n HTTP/1.1 200 OK\n Header: unchanged diff context\n \n+new line\n"
        )
        response = (
            "HTTP/2 200 OK\r\n"
            "content-type: application/vnd.github.v3.diff\r\n"
            "x-ratelimit-remaining: 80\r\n\r\n" + diff_body
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with patch(
            "agentic_devtools.cli.ci.github_provider.run_safe",
            return_value=SimpleNamespace(returncode=0, stdout=response, stderr=""),
        ):
            assert provider.get_pr_diff(42) == diff_body

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="diff")
    def test_passes_the_configured_token_without_mutating_process_environment(self, mock_gh_api, monkeypatch):
        monkeypatch.setenv(GH_TOKEN, "ambient-token")
        provider = GitHubActionsProvider(repo="owner/repo")

        provider.get_pr_diff(42)

        assert mock_gh_api.call_args.kwargs["token"] == "test-workflow-token"
        assert os.environ[GH_TOKEN] == "ambient-token"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_requires_the_configured_token(self, mock_gh_api, monkeypatch):
        monkeypatch.delenv(DEFAULT_CLASSIC_REPO_WORKFLOW_PAT)
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match=DEFAULT_CLASSIC_REPO_WORKFLOW_PAT):
            provider.get_pr_diff(42)

        mock_gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RuntimeError("boom"))
    def test_raises_runtime_error_on_failure(self, _mock_gh_api):
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="gh pr diff failed: boom"):
            provider.get_pr_diff(42)

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch(
        "agentic_devtools.cli.ci.github_provider._gh_api",
        side_effect=RetryableError("HTTP 503 service unavailable"),
    )
    def test_raises_retryable_error_on_transient_failure(self, _mock_gh_api, _mock_sleep):
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RetryableError) as exc_info:
            provider.get_pr_diff(42)
        assert exc_info.value.is_rate_limit is False

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=ProviderRateLimitError())
    def test_raises_provider_rate_limit_error_on_rate_limit_phrase(self, _mock_gh_api, _mock_sleep):
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ProviderRateLimitError):
            provider.get_pr_diff(42)

    @patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RuntimeError("line 429 failed"))
    def test_non_status_numbers_in_stderr_remain_non_retryable(self, _mock_gh_api):
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="gh pr diff failed: line 429 failed"):
            provider.get_pr_diff(42)

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RetryableError("timed out after 60s"))
    def test_raises_retryable_error_on_timeout(self, _mock_gh_api, _mock_sleep):
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RetryableError, match="timed out"):
            provider.get_pr_diff(42)
