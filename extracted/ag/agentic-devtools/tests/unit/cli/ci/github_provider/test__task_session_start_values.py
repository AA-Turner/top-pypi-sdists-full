"""Tests for validated Agent Task session timestamp aliases."""

import json
from collections.abc import Mapping
from datetime import UTC, datetime
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.agent_task_lifecycle import session_lifecycle_timestamp_values
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.pipeline.session_detector import classify_agent_task_inventory

NOW = datetime(2026, 10, 16, 10, 0, tzinfo=UTC)


@pytest.fixture(autouse=True)
def _default_workflow_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "workflow-token")


def _inventory(task: dict[str, object], detail: Mapping[str, object] | None = None):
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "_fetch_agent_task_pages", return_value=([task], True, ())),
        patch.object(provider, "_fetch_agent_task_detail", return_value=json.dumps(detail or task)),
    ):
        return provider.list_pr_agent_task_lifecycles(42, head_branch="copilot/pr-42")


def test_alias_selection_validates_all_values_and_keeps_creation_separate() -> None:
    assert session_lifecycle_timestamp_values(
        {
            "started_at": "invalid",
            "startedAt": "2026-10-16T09:55:00Z",
            "created_at": "invalid",
            "createdAt": "2026-10-16T09:50:00Z",
            "idle_at": "invalid",
            "idleSince": "2026-10-16T09:58:00Z",
            "idleSince_earlier": "2026-10-16T09:30:00Z",
        }
    ) == (
        "2026-10-16T09:55:00Z",
        "2026-10-16T09:50:00Z",
        "2026-10-16T09:58:00Z",
    )


def test_maps_session_creation_separately_from_validated_activity() -> None:
    task = {"id": "task-1", "state": "in_progress", "pullRequestNumber": 42}
    detail = {
        **task,
        "sessions": [
            {
                "id": "session-1",
                "state": "in_progress",
                "started_at": "invalid",
                "startedAt": "2026-10-16T09:55:00Z",
                "created_at": "invalid",
                "createdAt": "2026-10-16T09:50:00Z",
            }
        ],
    }
    session = _inventory(task, detail).tasks[0].sessions[0]

    assert (session.started_at, session.created_at) == (
        "2026-10-16T09:55:00Z",
        "2026-10-16T09:50:00Z",
    )


@pytest.mark.parametrize(
    "detail",
    [
        {"sessions": [{"id": "session-1", "state": "in_progress"}]},
        {"id": "task-1"},
    ],
    ids=("nested-session", "synthetic-session"),
)
def test_session_mapping_preserves_parent_creation_fallback(detail: Mapping[str, object]) -> None:
    task = {
        "id": "task-1",
        "state": "in_progress",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-16T08:00:00Z",
        "idleSince": "2026-10-16T08:30:00Z",
    }
    inventory = _inventory(task, detail)

    assert inventory.tasks[0].sessions[0].created_at == ""
    assert inventory.tasks[0].created_at == "2026-10-16T08:00:00Z"


def test_synthetic_session_does_not_promote_recent_task_creation_to_activity() -> None:
    task = {
        "id": "task-1",
        "state": "in_progress",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-16T09:55:00Z",
        "idleSince": "2026-10-16T08:30:00Z",
    }
    inventory = _inventory(task, {"id": "task-1"})
    session = inventory.tasks[0].sessions[0]
    assessment = classify_agent_task_inventory(inventory, now=NOW)

    assert (session.started_at, session.created_at, session.idle_at) == ("", "", "2026-10-16T08:30:00Z")
    assert assessment.blocking is False
    assert assessment.expired is True


def test_provider_validates_nested_idle_aliases() -> None:
    task = {
        "id": "task-1",
        "state": "in_progress",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-16T08:30:00Z",
        "sessions": [
            {
                "id": "session-1",
                "state": "in_progress",
                "startedAt": "2026-10-16T08:30:00Z",
                "idle_at": "invalid",
                "idleSince": "2026-10-16T09:55:00Z",
            }
        ],
    }
    inventory = _inventory(task)
    assessment = classify_agent_task_inventory(inventory, now=NOW)

    assert inventory.tasks[0].sessions[0].idle_at == "2026-10-16T09:55:00Z"
    assert assessment.blocking is True
    assert assessment.since == datetime(2026, 10, 16, 9, 55, tzinfo=UTC)


def test_anonymous_creation_only_child_is_retained_as_unknown_evidence() -> None:
    task = {
        "id": "task-1",
        "state": "in_progress",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-16T08:30:00Z",
        "sessions": [{"createdAt": "2026-10-16T09:55:00Z"}],
    }
    inventory = _inventory(task)
    assessment = classify_agent_task_inventory(inventory, now=NOW)

    assert inventory.complete is False
    assert inventory.tasks[0].sessions[0].session_id == ""
    assert inventory.tasks[0].sessions[0].created_at == "2026-10-16T09:55:00Z"
    assert inventory.incomplete_reasons == ("missing-session-id:task-1",)
    assert assessment.blocking is None
    assert assessment.expired is False
    assert assessment.reason == "malformed-lifecycle"
    assert assessment.since == datetime(2026, 10, 16, 9, 55, tzinfo=UTC)


def test_synthetic_session_uses_resolved_task_state() -> None:
    task = {
        "id": "task-1",
        "state": "in_progress",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-16T08:30:00Z",
    }
    detail = {"id": "task-1", "status": "completed", "startedAt": "2026-10-16T09:55:00Z"}
    inventory = _inventory(task, detail)
    assessment = classify_agent_task_inventory(inventory, now=NOW)

    assert inventory.tasks[0].state == "completed"
    assert inventory.tasks[0].sessions[0].state == "completed"
    assert assessment.blocking is None
    assert assessment.expired is False
    assert assessment.reason == "incomplete-inventory"


def test_invalid_only_activity_uses_task_creation_fallback() -> None:
    task = {
        "id": "task-1",
        "state": "in_progress",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-16T08:30:00Z",
    }
    inventory = _inventory(task, {"id": "task-1", "startedAt": "invalid"})
    assessment = classify_agent_task_inventory(inventory, now=NOW)

    assert inventory.tasks[0].sessions == ()
    assert inventory.tasks[0].created_at == task["createdAt"]
    assert assessment.blocking is False
    assert assessment.expired is True
    assert assessment.reason == "expired-lifecycle"
