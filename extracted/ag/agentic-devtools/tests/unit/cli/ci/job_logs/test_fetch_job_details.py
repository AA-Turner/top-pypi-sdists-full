"""Tests for fetch_job_details()."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.job_logs import fetch_job_details
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


class TestFetchJobDetails:
    """Tests for fetching a GitHub Actions job's metadata."""

    def test_returns_none_when_repo_missing(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api") as mock_api:
            result = fetch_job_details(123, repo="")
        assert result is None
        mock_api.assert_not_called()

    def test_returns_dict_on_success(self) -> None:
        raw = '{"workflow_name": "CI", "name": "Run", "run_id": 99}'
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=raw) as mock_api:
            result = fetch_job_details(123, repo="owner/repo", token="tok")
        assert result == {"workflow_name": "CI", "name": "Run", "run_id": 99}
        mock_api.assert_called_once_with("/repos/owner/repo/actions/jobs/123", token="tok")

    def test_returns_none_when_gh_api_raises(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RuntimeError("404 Not Found")):
            result = fetch_job_details(123, repo="owner/repo")
        assert result is None

    def test_returns_none_when_gh_api_has_non_rate_limit_retryable_error(self) -> None:
        error = RetryableError("temporary failure", is_rate_limit=False)
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=error):
            result = fetch_job_details(123, repo="owner/repo")
        assert result is None

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
                fetch_job_details(123, repo="owner/repo")
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
                fetch_job_details(123, repo="owner/repo")
        assert exc_info.value is error

    def test_returns_none_when_json_malformed(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="not json"):
            result = fetch_job_details(123, repo="owner/repo")
        assert result is None

    def test_returns_none_when_json_not_object(self) -> None:
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="[1, 2, 3]"):
            result = fetch_job_details(123, repo="owner/repo")
        assert result is None
