"""Tests for GitHubActionsProvider.list_pr_session_summaries()."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


@pytest.fixture(autouse=True)
def _default_workflow_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "workflow-token")


def test_returns_completed_sessions_for_matching_pull_request() -> None:
    """Parses completed task sessions and ignores other pull requests and states."""
    raw_tasks = {
        "tasks": [
            {
                "id": "task-1",
                "status": "completed",
                "pull_request_number": 42,
                "sessions": [
                    {
                        "id": "session-1",
                        "state": "completed",
                        "started_at": "2026-01-02T00:00:00Z",
                        "completed_at": "2026-01-02T01:00:00Z",
                        "finishing_text": "Changed files and ran tests.",
                    }
                ],
            },
            {"id": "task-2", "status": "in_progress", "pull_request_number": 42},
            {"id": "task-3", "status": "completed", "pull_request_number": 99},
        ]
    }
    detail = raw_tasks["tasks"][0]
    incomplete_detail = raw_tasks["tasks"][1]
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.dict("os.environ", {"COPILOT_GITHUB_TOKEN": "copilot-token"}),
        patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=[MagicMock(), MagicMock(), MagicMock()],
        ) as api,
        patch(
            "agentic_devtools.cli.ci.github_provider._parse_paginated_json",
            side_effect=[raw_tasks, detail, incomplete_detail],
        ),
    ):
        result = provider.list_pr_session_summaries(42)
        cached_result = provider.list_pr_session_summaries(42)

    assert len(result) == 1
    assert result[0].finishing_text == "Changed files and ran tests."
    assert cached_result == result
    assert api.call_args_list[0].kwargs["token"] == "copilot-token"
    assert api.call_args_list[1].kwargs["token"] == "copilot-token"


def test_skips_malformed_session_records() -> None:
    """Returns no summary when a completed task lacks session identity or start time."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=MagicMock()),
        patch(
            "agentic_devtools.cli.ci.github_provider._parse_paginated_json",
            return_value=[{"id": "task-1", "status": "completed", "pr_number": 42, "sessions": [None, {}]}],
        ),
    ):
        assert provider.list_pr_session_summaries(42) == []


def test_skips_matching_tasks_without_string_ids() -> None:
    """Skips matching pull-request tasks that lack a usable task identifier."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=MagicMock()),
        patch(
            "agentic_devtools.cli.ci.github_provider._parse_paginated_json",
            return_value=[{"id": 1, "status": "completed", "pr_number": 42}],
        ),
    ):
        assert provider.list_pr_session_summaries(42) == []


def test_supports_nested_pr_metadata_and_task_level_session() -> None:
    """Reads nested pull-request metadata and a task-level session record."""
    provider = GitHubActionsProvider(repo="owner/repo")
    raw_tasks = [
        {
            "id": "task-1",
            "state": "completed",
            "pullRequest": {"number": 42},
            "session_id": "session-1",
            "createdAt": "2026-01-02T00:00:00Z",
            "summary": "Finished.",
        },
    ]
    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=MagicMock()) as api,
        patch(
            "agentic_devtools.cli.ci.github_provider._parse_paginated_json",
            side_effect=[raw_tasks, raw_tasks[0]],
        ),
    ):
        result = provider.list_pr_session_summaries(42)

    assert len(result) == 1
    assert result[0].finishing_text == "Finished."
    assert api.call_count == 2
    assert api.call_args_list[0].kwargs["token"] == "workflow-token"
    assert api.call_args_list[1].kwargs["token"] == "workflow-token"


def test_fetches_task_details_for_pull_artifact_tasks() -> None:
    """Fetches task details before extracting sessions from pull artifacts."""
    provider = GitHubActionsProvider(repo="owner/repo")
    task = {
        "id": "task-1",
        "status": "completed",
        "artifacts": [{"type": "pull", "url": "https://github.com/owner/repo/pull/42"}],
    }
    detail = {
        "id": "task-1",
        "sessions": [
            {
                "id": "session-1",
                "state": "completed",
                "started_at": "2026-01-02T00:00:00Z",
                "finishing_text": "Finished.",
            }
        ],
    }
    with (
        patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=[MagicMock(), MagicMock()],
        ) as api,
        patch(
            "agentic_devtools.cli.ci.github_provider._parse_paginated_json",
            side_effect=[{"tasks": [task]}, detail],
        ),
    ):
        result = provider.list_pr_session_summaries(42)

    assert len(result) == 1
    assert result[0].session_id == "session-1"
    assert api.call_args_list[1].args[0] == "/agents/repos/owner/repo/tasks/task-1"


def test_returns_empty_for_invalid_tasks_payload() -> None:
    """Returns no summaries when the Agent Tasks response does not contain a task list."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=MagicMock()),
        patch("agentic_devtools.cli.ci.github_provider._parse_paginated_json", return_value={"tasks": {}}),
    ):
        assert provider.list_pr_session_summaries(42) == []
