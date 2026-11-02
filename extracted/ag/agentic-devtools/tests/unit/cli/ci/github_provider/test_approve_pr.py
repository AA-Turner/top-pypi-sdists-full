"""Tests for GitHubActionsProvider.approve_pr() method."""

import inspect
import json
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.github_api_error import GitHubApiError
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.shared.retry import RetryableError


def _api_response(
    status: int | None,
    *,
    headers: str = "",
    stderr: str = "",
) -> MagicMock:
    response = MagicMock()
    response.returncode = 1
    response.stdout = "" if status is None else f"HTTP/1.1 {status} Status\r\n{headers}\r\n{{}}"
    response.stderr = stderr
    return response


class TestApprovePR:
    """Tests for GitHubActionsProvider.approve_pr()."""

    @patch.dict("os.environ", {"AGDT_PR_APPROVER_PAT": "ghp_approver_token"})
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_approve_pr_posts_review_with_approver_token(self, mock_run_safe) -> None:
        class _Result:
            returncode = 0
            stdout = json.dumps({"id": 999})
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.approve_pr(42, "abc123", "LGTM!")

        assert result is True
        kwargs = mock_run_safe.call_args[1]
        body = json.loads(kwargs["input"])
        assert body["event"] == "APPROVE"
        assert body["commit_id"] == "abc123"
        assert body["body"] == "LGTM!"
        # Verify the approver token is passed via env
        assert kwargs["env"]["GH_TOKEN"] == "ghp_approver_token"

    @patch.dict("os.environ", {"AGDT_PR_APPROVER_PAT": ""})
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_approve_pr_skips_when_pat_empty(self, mock_run_safe) -> None:
        """Approval is skipped when AGDT_PR_APPROVER_PAT is empty."""
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.approve_pr(42, "abc123", "LGTM!")

        assert result is False
        mock_run_safe.assert_not_called()

    @patch.dict("os.environ", {"AGDT_PR_APPROVER_PAT": "not_present"})
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_approve_pr_skips_when_pat_missing(self, mock_run_safe) -> None:
        """Approval is skipped when AGDT_PR_APPROVER_PAT is not set."""
        import os

        # Remove the key after patch.dict sets it, simulating unset env var
        del os.environ["AGDT_PR_APPROVER_PAT"]
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.approve_pr(42, "abc123", "LGTM!")

        assert result is False
        mock_run_safe.assert_not_called()

    @pytest.mark.parametrize("status", [401, 403, 404, 422])
    @patch.dict("os.environ", {"AGDT_PR_APPROVER_PAT": "ghp_token"})
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_approve_pr_rejects_permanent_status_once(self, mock_run_safe, status: int) -> None:
        mock_run_safe.return_value = _api_response(status)
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(GitHubApiError) as caught:
            provider.approve_pr(42, "abc123", "LGTM!")

        assert caught.value.http_status == status
        assert mock_run_safe.call_count == 1

    @patch.dict("os.environ", {"AGDT_PR_APPROVER_PAT": "ghp_token"})
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_approve_pr_uses_none_when_http_status_is_unavailable(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _api_response(None, stderr="unrelated diagnostic mentions 401")
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(GitHubApiError) as caught:
            provider.approve_pr(42, "abc123", "LGTM!")

        assert caught.value.http_status is None
        assert str(caught.value) == "GitHub API error: status unavailable"
        assert mock_run_safe.call_count == 1

    @pytest.mark.parametrize(
        ("status", "headers", "stderr"),
        [
            (403, "", "API rate limit exceeded"),
            (429, "", ""),
            (403, "Retry-After: 30\r\n", ""),
            (403, "X-RateLimit-Remaining: 0\r\n", ""),
            (None, "Retry-After: 30\r\n", ""),
            (500, "", ""),
            (502, "", ""),
            (503, "", ""),
            (504, "", ""),
        ],
    )
    @patch.dict("os.environ", {"AGDT_PR_APPROVER_PAT": "ghp_token"})
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_approve_pr_preserves_retryable_api_classification(
        self, mock_run_safe, status: int | None, headers: str, stderr: str
    ) -> None:
        mock_run_safe.return_value = _api_response(status, headers=headers, stderr=stderr)
        provider = GitHubActionsProvider(repo="owner/repo")
        approve_pr = inspect.unwrap(GitHubActionsProvider.approve_pr)
        if status is None:
            parser = patch(
                "agentic_devtools.cli.ci.github_provider._parse_gh_api_output",
                return_value=(None, {"retry-after": "30"}, ""),
            )
            with parser, pytest.raises(RetryableError):
                approve_pr(provider, 42, "abc123", "LGTM!")
        else:
            with pytest.raises(RetryableError):
                approve_pr(provider, 42, "abc123", "LGTM!")

        assert mock_run_safe.call_count == 1
