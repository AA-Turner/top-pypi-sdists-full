"""Tests for GitHubActionsProvider._fetch_agent_tasks()."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci import github_provider
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


def test_fetch_agent_tasks_preserves_remote_404_diagnostics() -> None:
    """Propagates a remote task-list 404 instead of returning an empty inventory."""
    error = RuntimeError("GitHub API error: HTTP 404; http_status=404")
    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=error),
        pytest.raises(RuntimeError) as exc_info,
    ):
        GitHubActionsProvider(repo="owner/repo")._fetch_agent_tasks("owner/repo", "token")

    assert exc_info.value is error
    assert "HTTP 404" in str(exc_info.value)


def test_fetch_agent_tasks_preserves_transport_404_diagnostics(monkeypatch: pytest.MonkeyPatch) -> None:
    result = SimpleNamespace(returncode=1, stdout="HTTP/1.1 404 Not Found\n\n", stderr="Not Found")
    monkeypatch.setattr(github_provider, "run_safe", Mock(return_value=result))

    with pytest.raises(RuntimeError) as exc_info:
        GitHubActionsProvider(repo="owner/repo")._fetch_agent_tasks("owner/repo", "token")

    assert "http_status=404; http_status_source=response_headers" in str(exc_info.value)
    assert "returncode=1; response_body=not captured" in str(exc_info.value)
