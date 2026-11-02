"""Tests for GitHubActionsProvider.publish_pr() method."""

import subprocess
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.retry import RetryableError
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestPublishPR:
    """Tests for GitHubActionsProvider.publish_pr()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_publish_pr_calls_gh_pr_ready(self, mock_run_safe) -> None:
        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.publish_pr(42)

        assert result is None
        args = mock_run_safe.call_args[0][0]
        assert args == ["gh", "pr", "ready", "42", "--repo", "owner/repo"]
        assert mock_run_safe.call_args.kwargs["timeout"] == 60

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_publish_pr_passes_environment(self, mock_run_safe) -> None:
        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.publish_pr(42, env={"GH_TOKEN": "token"})

        assert mock_run_safe.call_args.kwargs["env"] == {"GH_TOKEN": "token"}

    @patch("agentic_devtools.cli.ci.github_provider._credential_identity_for_token")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_publish_pr_attributes_failure_to_explicit_token(self, mock_run_safe, mock_identity) -> None:
        class _Result:
            returncode = 1
            stdout = ""
            stderr = "HTTP 429: API rate limit exceeded"

        mock_run_safe.return_value = _Result()
        mock_identity.return_value = "workflow-token"

        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ProviderRateLimitError) as exc_info:
            provider.publish_pr(42, env={"GH_TOKEN": "token"})

        mock_identity.assert_called_with("token")
        assert exc_info.value.credential_identity == "workflow-token"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_publish_pr_uses_stdout_when_stderr_empty(self, mock_run_safe) -> None:
        class _Result:
            returncode = 1
            stdout = "gh error from stdout"
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="gh error from stdout"):
            provider.publish_pr(42)

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_publish_pr_without_repo_omits_repo_flag(self, mock_run_safe) -> None:
        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="")
        provider.publish_pr(7)

        args = mock_run_safe.call_args[0][0]
        assert "--repo" not in args
        assert args == ["gh", "pr", "ready", "7"]

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_publish_pr_rate_limit_error_is_retryable(self, mock_run_safe, _mock_sleep) -> None:
        class _Result:
            returncode = 1
            stdout = ""
            stderr = "HTTP 429: API rate limit exceeded"

        mock_run_safe.return_value = _Result()
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ProviderRateLimitError, match="Provider rate limit exhausted"):
            provider.publish_pr(42)

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_publish_pr_transient_error_is_retryable(self, mock_run_safe, _mock_sleep) -> None:
        class _Result:
            returncode = 1
            stdout = ""
            stderr = "HTTP 503 Service Unavailable"

        mock_run_safe.return_value = _Result()
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RetryableError, match="transient failure"):
            provider.publish_pr(42)

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_publish_pr_timeout_raises_runtime_error(self, mock_run_safe) -> None:
        mock_run_safe.side_effect = subprocess.TimeoutExpired(cmd="gh", timeout=60)

        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="timed out after 60 seconds"):
            provider.publish_pr(42)
