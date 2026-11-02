"""Regression coverage for real provider inventory evidence reaching session resolution."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import AgentTaskInventoryLoadResult
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, get_latest_session_state


@pytest.mark.parametrize(
    ("response", "category", "http_status"),
    [
        ('{"tasks": [], "status": 500}', "provider_unavailable", 500),
        ("", "malformed_response", None),
        (" \r\n\t", "malformed_response", None),
    ],
)
def test_real_provider_failed_response_is_unknown(
    response: str, category: str, http_status: int | None, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "task-token")
    provider = GitHubActionsProvider(repo="org/repo")
    with (
        patch.object(provider, "_fetch_agent_tasks", return_value=response) as fetch,
        patch.object(provider, "list_pr_issue_events", return_value=[]) as timeline,
        patch.object(provider, "list_pr_agent_task_lifecycles") as lifecycles,
    ):
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
    assert state.outcome is SessionOutcome.UNKNOWN
    assert state.inventory_availability.value == "unavailable"
    assert (state.failure_category, state.http_status) == (category, http_status)
    assert state.failure_source == "agent-task-inventory"
    fetch.assert_called_once_with("org/repo", "task-token")
    timeline.assert_not_called()
    lifecycles.assert_not_called()


def test_real_provider_preserves_typed_http_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "task-token")
    provider = GitHubActionsProvider(repo="org/repo")
    with patch.object(provider, "_fetch_agent_tasks", return_value='{"tasks": [], "status": 500}'):
        inventory = provider._list_agent_task_inventory("org/repo")
    assert isinstance(inventory, AgentTaskInventoryLoadResult)
    assert not inventory.complete
    assert inventory.availability == "unavailable"
    assert inventory.http_status == 500
    assert inventory.failure_category == "provider_unavailable"


@pytest.mark.parametrize("response", ['{"tasks": []}', '{"tasks": [], "status": 200}'])
def test_real_provider_keeps_valid_empty_list_compatible(response: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "task-token")
    provider = GitHubActionsProvider(repo="org/repo")
    with patch.object(provider, "_fetch_agent_tasks", return_value=response):
        inventory = provider.list_agent_tasks("org/repo")
    assert isinstance(inventory, AgentTaskInventoryLoadResult)
    assert inventory.tasks == ()
    assert inventory.complete


@pytest.mark.parametrize(
    "later_page",
    [
        '{"tasks": null}',
        '{"tasks": "malformed"}',
        "{}",
        '{"tasks": [], "status": 500}',
        '{"tasks": [], "error": "failed"}',
        '{"tasks": [], "errors": ["failed"]}',
        '{"message": "failed", "tasks": []}',
        '{"tasks": [], "status": "error"}',
        '{"tasks": [], "status": null}',
        '{"tasks": [], "status": false}',
        "null",
        "[]",
        '"invalid"',
        '{"tasks": []} trailing garbage',
        '{"tasks":',
    ],
)
def test_real_provider_later_page_failure_is_unknown(later_page: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "task-token")
    provider = GitHubActionsProvider(repo="org/repo")
    task = {"id": "unrelated", "state": "completed", "pull_request": {"number": 99}}
    response = json.dumps({"tasks": [task], "status": 200}) + "\n" + later_page
    with (
        patch.object(provider, "_fetch_agent_tasks", return_value=response),
        patch.object(provider, "list_pr_issue_events", return_value=[]) as timeline,
    ):
        inventory = provider._list_agent_task_inventory("org/repo")
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
        public_inventory = provider.list_agent_tasks("org/repo")
    assert isinstance(inventory, AgentTaskInventoryLoadResult)
    assert not inventory.complete
    assert inventory.tasks[0] == task
    assert isinstance(public_inventory, AgentTaskInventoryLoadResult)
    assert public_inventory.availability is inventory.availability
    assert public_inventory.failure_category is inventory.failure_category
    assert state.outcome is SessionOutcome.UNKNOWN
    assert state.inventory_availability.value == "partial"
    timeline.assert_not_called()


def test_real_provider_all_valid_pages_stay_complete(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "task-token")
    provider = GitHubActionsProvider(repo="org/repo")
    tasks = [
        {"id": "first", "state": "completed", "pull_request": {"number": 99}},
        {"id": "second", "state": "completed", "pull_request": {"number": 98}},
    ]
    response = "\n".join(json.dumps({"tasks": [task]}) for task in tasks)
    with (
        patch.object(provider, "_fetch_agent_tasks", return_value=response),
        patch.object(provider, "list_pr_issue_events", return_value=[]),
    ):
        inventory = provider.list_agent_tasks("org/repo")
        state = get_latest_session_state(provider, 7, repo="org/repo", head_branch="", pr_id=None)
    assert isinstance(inventory, AgentTaskInventoryLoadResult)
    assert inventory.tasks == tuple(tasks)
    assert inventory.complete
    assert state.inventory_availability.value == "complete"
    assert state.outcome is SessionOutcome.NONE
