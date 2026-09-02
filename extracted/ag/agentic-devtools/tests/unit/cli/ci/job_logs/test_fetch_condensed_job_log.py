"""Tests for fetch_condensed_job_log()."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.job_logs import fetch_condensed_job_log
from agentic_devtools.cli.ci.models import CheckRunStatus
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

_JOB_URL = "https://github.com/owner/repo/actions/runs/28005239943/job/82885697587"


def _check(html_url: str = _JOB_URL) -> CheckRunStatus:
    return CheckRunStatus(id=1, name="Run Targeted Checks", status="completed", conclusion="failure", html_url=html_url)


class TestFetchCondensedJobLog:
    """Tests for fetching + condensing a failing check's job log."""

    def test_returns_empty_when_no_job_id(self) -> None:
        check = _check(html_url="https://github.com/owner/repo/security/code-scanning/42")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api") as mock_api:
            result = fetch_condensed_job_log(check, repo="owner/repo")
        assert result == ""
        mock_api.assert_not_called()

    def test_returns_empty_when_repo_missing(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api") as mock_api:
            result = fetch_condensed_job_log(_check(), repo="")
        assert result == ""
        mock_api.assert_not_called()

    def test_returns_empty_when_gh_api_raises(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RuntimeError("410 Gone")):
            result = fetch_condensed_job_log(_check(), repo="owner/repo")
        assert result == ""

    def test_propagates_rate_limit_from_gh_api(self) -> None:
        error = ProviderRateLimitError(provider="github", credential_identity="SPECKIT_PR_TOKEN")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=error):
            with pytest.raises(ProviderRateLimitError):
                fetch_condensed_job_log(_check(), repo="owner/repo")

    def test_converts_retryable_rate_limit_from_gh_api(self) -> None:
        error = RetryableError("rate limited", is_rate_limit=True)
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=error):
            with pytest.raises(ProviderRateLimitError):
                fetch_condensed_job_log(_check(), repo="owner/repo")

    def test_returns_empty_when_log_blank(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="   \n  "):
            result = fetch_condensed_job_log(_check(), repo="owner/repo")
        assert result == ""

    def test_returns_empty_when_log_is_empty(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=""):
            result = fetch_condensed_job_log(_check(), repo="owner/repo")
        assert result == ""

    def test_returns_empty_when_gh_api_has_non_rate_limit_retryable_error(self) -> None:
        error = RetryableError("temporary failure", is_rate_limit=False)
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=error):
            result = fetch_condensed_job_log(_check(), repo="owner/repo")
        assert result == ""

    def test_returns_condensed_log_on_success(self) -> None:
        raw = "2026-06-23T10:00:00.1234567Z Error: boom\n2026-06-23T10:00:01.0000000Z stack trace"
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=raw) as mock_api:
            result = fetch_condensed_job_log(_check(), repo="owner/repo", token="tok")
        assert "Error: boom" in result
        assert "2026-06-23T10:00:00" not in result
        mock_api.assert_called_once_with(
            "/repos/owner/repo/actions/jobs/82885697587/logs",
            token="tok",
        )
