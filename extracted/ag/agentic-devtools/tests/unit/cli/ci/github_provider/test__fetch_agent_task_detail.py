"""Tests for GitHubActionsProvider._fetch_agent_task_detail()."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def test_fetches_task_detail_with_quoted_task_id_and_headers() -> None:
    """Fetches one task detail while quoting unsafe task-id characters."""
    with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="response") as api:
        result = GitHubActionsProvider(repo="owner/repo")._fetch_agent_task_detail("owner/repo", "task/id", "token")

    assert result == "response"
    api.assert_called_once_with(
        "/agents/repos/owner/repo/tasks/task%2Fid",
        token="token",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
        },
    )


def test_fetch_agent_task_detail_preserves_remote_404() -> None:
    """Propagates a remote task-detail 404 rather than fabricating empty detail."""
    error = RuntimeError("GitHub API error: HTTP 404; http_status=404")
    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=error),
        pytest.raises(RuntimeError) as exc_info,
    ):
        GitHubActionsProvider(repo="owner/repo")._fetch_agent_task_detail("owner/repo", "task-1", "token")

    assert exc_info.value is error
    assert "HTTP 404" in str(exc_info.value)
