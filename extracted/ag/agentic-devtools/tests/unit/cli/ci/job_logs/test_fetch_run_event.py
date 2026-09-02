"""Tests for fetch_run_event()."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.job_logs import fetch_run_event
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


class TestFetchRunEvent:
    """Tests for fetching a workflow run's triggering event."""

    def test_returns_empty_when_repo_missing(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api") as mock_api:
            result = fetch_run_event(99, repo="")
        assert result == ""
        mock_api.assert_not_called()

    def test_returns_event_on_success(self) -> None:
        raw = '{"event": "pull_request"}'
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=raw) as mock_api:
            result = fetch_run_event(99, repo="owner/repo", token="tok")
        assert result == "pull_request"
        mock_api.assert_called_once_with("/repos/owner/repo/actions/runs/99", token="tok")

    def test_returns_empty_when_gh_api_raises(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RuntimeError("500 Server Error")):
            result = fetch_run_event(99, repo="owner/repo")
        assert result == ""

    def test_returns_empty_when_gh_api_has_non_rate_limit_retryable_error(self) -> None:
        error = RetryableError("temporary failure", is_rate_limit=False)
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=error):
            result = fetch_run_event(99, repo="owner/repo")
        assert result == ""

    def test_reraises_rate_limit_error(self) -> None:
        error = RetryableError(
            "rate limited",
            retry_after=30,
            reset_timestamp=200,
            remaining=0,
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
            source="actions-api",
            is_rate_limit=True,
        )
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=error):
            with pytest.raises(ProviderRateLimitError) as exc_info:
                fetch_run_event(99, repo="owner/repo")
        assert exc_info.value.retry_after_seconds == 30
        assert exc_info.value.reset_timestamp == 200
        assert exc_info.value.remaining == 0
        assert exc_info.value.provider == "github"
        assert exc_info.value.credential_identity == "SPECKIT_PR_TOKEN"
        assert exc_info.value.source == "actions-api"

    def test_preserves_provider_rate_limit_error(self) -> None:
        error = ProviderRateLimitError(provider="github", is_rate_limit=True)
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=error):
            with pytest.raises(ProviderRateLimitError) as exc_info:
                fetch_run_event(99, repo="owner/repo")
        assert exc_info.value is error

    def test_returns_empty_when_json_not_object(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="[]"):
            result = fetch_run_event(99, repo="owner/repo")
        assert result == ""

    def test_returns_empty_when_event_missing(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="{}"):
            result = fetch_run_event(99, repo="owner/repo")
        assert result == ""

    def test_returns_empty_when_event_not_string(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value='{"event": 123}'):
            result = fetch_run_event(99, repo="owner/repo")
        assert result == ""
