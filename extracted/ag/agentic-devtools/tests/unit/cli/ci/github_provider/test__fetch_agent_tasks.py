"""Tests for GitHubActionsProvider._fetch_agent_tasks()."""

from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def test_fetches_agent_tasks_with_pagination_and_headers() -> None:
    """Fetches the repository task list using the pinned Agent Tasks API."""
    with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="response") as api:
        result = GitHubActionsProvider(repo="owner/repo")._fetch_agent_tasks("owner/repo", "token")

    assert result == "response"
    api.assert_called_once_with(
        "/agents/repos/owner/repo/tasks",
        paginate=True,
        token="token",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
        },
    )
