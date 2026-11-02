from unittest.mock import patch

import pytest

from agentic_devtools.adapters.pull_request_publish import (
    GitHubPullRequestPublishAdapter,
    PullRequestPublishRequest,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


@pytest.fixture(autouse=True)
def _default_repo_workflow_token(monkeypatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "token")


def test_dry_run() -> None:
    request = PullRequestPublishRequest("github", 1, "owner/repo", dry_run=True)
    result = GitHubPullRequestPublishAdapter().publish(request)
    assert result.status == "dry_run"


def test_rejects_provider_mismatch() -> None:
    result = GitHubPullRequestPublishAdapter().publish(PullRequestPublishRequest("azure_devops", 1))
    assert not result.success
    assert result.status == "provider_mismatch"


@patch("agentic_devtools.adapters.pull_request_publish.require_default_repo_workflow_token", return_value="token")
@patch("agentic_devtools.adapters.pull_request_publish.GitHubActionsProvider.publish_pr")
def test_publishes(mock_publish_pr, mock_token) -> None:
    result = GitHubPullRequestPublishAdapter().publish(PullRequestPublishRequest("github", 1, "owner/repo"))
    assert result.success
    mock_publish_pr.assert_called_once()
    assert mock_publish_pr.call_args.args == (1,)
    assert mock_publish_pr.call_args.kwargs["env"]["GH_TOKEN"] == "token"
    mock_token.assert_called_once_with("publish the GitHub pull request")


@patch("agentic_devtools.adapters.pull_request_publish.GitHubActionsProvider.publish_pr")
def test_returns_error_on_failure(mock_publish_pr) -> None:
    mock_publish_pr.side_effect = RuntimeError("denied")
    result = GitHubPullRequestPublishAdapter().publish(PullRequestPublishRequest("github", 1, "owner/repo"))
    assert not result.success
    assert result.status == "failed"
    assert result.error == "denied"


@patch("agentic_devtools.adapters.pull_request_publish.GitHubActionsProvider.publish_pr")
def test_returns_retryable_failure_status(mock_publish_pr) -> None:
    mock_publish_pr.side_effect = RetryableError("temporary")
    result = GitHubPullRequestPublishAdapter().publish(PullRequestPublishRequest("github", 1, "owner/repo"))
    assert not result.success
    assert result.status == "retryable_failure"


@patch("agentic_devtools.adapters.pull_request_publish.GitHubActionsProvider.publish_pr")
def test_returns_rate_limit_status(mock_publish_pr) -> None:
    mock_publish_pr.side_effect = ProviderRateLimitError(provider="github")
    result = GitHubPullRequestPublishAdapter().publish(PullRequestPublishRequest("github", 1, "owner/repo"))
    assert not result.success
    assert result.status == "rate_limited"
