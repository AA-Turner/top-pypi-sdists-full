"""Tests for GitHubActionsProvider.get_agent_task_prompt."""

import json
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def test_returns_prompt_from_agent_task_detail() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    task_detail = {"id": "task-1", "prompt": "Original repair findings"}

    with (
        patch.dict("os.environ", {"COPILOT_GITHUB_TOKEN": "token"}),
        patch.object(provider, "_fetch_agent_task_detail", return_value=json.dumps(task_detail)) as fetch,
    ):
        assert provider.get_agent_task_prompt("task-1") == "Original repair findings"

    fetch.assert_called_once_with("owner/repo", "task-1", "token")


def test_returns_prompt_from_nested_agent_task_detail() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    task_detail = {"task": {"task_id": "task-1", "prompt": "Nested repair findings"}}

    with (
        patch.dict("os.environ", {"COPILOT_GITHUB_TOKEN": "token"}),
        patch.object(provider, "_fetch_agent_task_detail", return_value=json.dumps(task_detail)),
    ):
        assert provider.get_agent_task_prompt("task-1") == "Nested repair findings"


def test_ignores_prompt_when_task_detail_identity_does_not_match() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    task_detail = {"id": "other-task", "prompt": "Unrelated task prompt"}

    with (
        patch.dict("os.environ", {"COPILOT_GITHUB_TOKEN": "token"}),
        patch.object(provider, "_fetch_agent_task_detail", return_value=json.dumps(task_detail)),
    ):
        assert provider.get_agent_task_prompt("task-1") == ""


def test_returns_empty_when_task_detail_is_not_an_object() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")

    with (
        patch.dict("os.environ", {"COPILOT_GITHUB_TOKEN": "token"}),
        patch.object(provider, "_fetch_agent_task_detail", return_value="[]"),
    ):
        assert provider.get_agent_task_prompt("task-1") == ""


def test_returns_empty_when_task_detail_has_no_prompt() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")

    with (
        patch.dict("os.environ", {"COPILOT_GITHUB_TOKEN": "token"}),
        patch.object(provider, "_fetch_agent_task_detail", return_value=json.dumps({"id": "task-1"})),
    ):
        assert provider.get_agent_task_prompt("task-1") == ""


def test_empty_task_id_skips_agent_task_request() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")

    with patch.object(provider, "_fetch_agent_task_detail") as fetch:
        assert provider.get_agent_task_prompt("") == ""

    fetch.assert_not_called()
