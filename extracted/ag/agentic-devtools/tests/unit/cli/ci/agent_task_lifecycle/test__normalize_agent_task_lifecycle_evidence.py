"""Tests for joining raw task clocks to typed lifecycle evidence."""

from copy import deepcopy
from typing import Any

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import FailureCategory
from agentic_devtools.cli.ci.agent_task_lifecycle import (
    AgentTaskInventory,
    AgentTaskLifecycle,
    AgentTaskSessionLifecycle,
    _normalize_agent_task_lifecycle_evidence,
    parse_lifecycle_timestamp,
    select_session_lifecycle_timestamp,
    select_task_lifecycle_timestamp,
)


def _task(**overrides: Any) -> AgentTaskLifecycle:
    fields = {
        "task_id": "task-1",
        "repository": "owner/repo",
        "pr_number": 42,
        "head_branch": "typed-branch",
        "state": "in_progress",
        "created_at": "2020-01-01T00:00:00Z",
        "started_at": "2020-01-02T00:00:00Z",
        "idle_at": "",
    }
    return AgentTaskLifecycle(**{**fields, **overrides})


def test_unions_newest_valid_task_clocks_without_changing_availability_or_identity() -> None:
    raw = {
        "id": "task-1",
        "repository": "OWNER/REPO",
        "pullRequestNumber": 42,
        "createdAt": "2026-10-25T18:00:00Z",
        "started_at": "malformed",
        "startedAt": "2026-10-25T19:00:00Z",
        "idleAt": "2026-10-25T19:30:00Z",
        "updatedAt": "9999-12-31T23:59:59Z",
    }
    original = deepcopy(raw)
    inventory = AgentTaskInventory(
        (_task(),),
        complete=False,
        incomplete_reasons=("task-detail:task-1", "page-limit"),
        failure_category=FailureCategory.RETRIEVAL_EXHAUSTED,
        http_status=503,
    )

    result = _normalize_agent_task_lifecycle_evidence([raw], inventory)
    task = result.tasks[0]

    assert (task.created_at, task.started_at, task.idle_at) == (
        "2026-10-25T18:00:00Z",
        "2026-10-25T19:00:00Z",
        "2026-10-25T19:30:00Z",
    )
    assert (task.state, task.repository, task.pr_number, task.head_branch) == (
        "in_progress",
        "owner/repo",
        42,
        "typed-branch",
    )
    assert (result.complete, result.incomplete_reasons, result.failure_category, result.http_status) == (
        False,
        ("task-detail:task-1", "page-limit"),
        FailureCategory.RETRIEVAL_EXHAUSTED,
        503,
    )
    assert raw == original
    assert inventory.tasks[0] == _task()


def test_raw_task_id_uses_first_valid_alias_and_never_joins_conflicting_ids() -> None:
    typed = AgentTaskInventory((_task(),))
    conflicting = {"id": "other", "task_id": "task-1", "idleAt": "2026-10-25T19:00:00Z"}
    valid_after_boolean = {"id": True, "task_id": "task-1", "idleAt": "2026-10-25T18:00:00Z"}

    result = _normalize_agent_task_lifecycle_evidence([conflicting], typed)
    valid_result = _normalize_agent_task_lifecycle_evidence([valid_after_boolean], typed)

    assert result.tasks[0].idle_at == ""
    assert valid_result.tasks[0].idle_at == "2026-10-25T18:00:00Z"
    assert _normalize_agent_task_lifecycle_evidence([{"id": False, "taskId": "task-1"}], typed).tasks[0].idle_at == ""


@pytest.mark.parametrize(
    "raw_identity",
    [
        {"repository": "owner/other"},
        {"repository": "owner/other", "repo": "owner/repo"},
        {"repository": "owner/repo", "repo": "owner/other"},
        {"repository": "owner/repo", "repository_full_name": "owner/other"},
        {"repository_full_name": "owner/other"},
        {"repositoryFullName": "owner/other"},
        {"repository": {"full_name": "owner/other"}},
        {"metadata": {"repository_full_name": "owner/other"}},
        {"metadata": {"repository": {"full_name": "owner/other"}}},
        {"metadata": {"repositoryFullName": "owner/other"}},
        {"metadata": {"repo": "owner/other"}},
        {"pullRequestNumber": 43},
        {"pr_number": 42, "pullRequestNumber": 43},
        {"pr_number": 43, "pullRequestNumber": 42},
        {"pullRequestNumber": 42, "metadata": {"pr_number": 43}},
        {"pullRequestNumber": 43, "metadata": {"pr_number": 42}},
        {"metadata": {"pr_number": "43"}},
        {"pullRequest": {"number": 43}},
        {"pullRequestNumber": 42, "pull_request": {"number": 43}},
        {"pullRequestNumber": 43, "pull_request": {"number": 42}},
        {"metadata": {"pull_request": {"number": 43}}},
        {"pullRequestNumber": "invalid", "pullRequest": {"number": 43}},
        {"pullRequestNumber": 42, "artifacts": [{"type": "pull", "data": {"number": 43}}]},
        {"artifacts": [{"type": "pull", "data": {"number": 43}}], "pullRequestNumber": 42},
        {"pullRequestNumber": 42, "artifacts": [{"type": "pull", "url": "https://github.com/o/r/pull/43"}]},
        {"artifacts": [{"type": "pull", "url": "https://github.com/o/r/pull/43"}], "pullRequestNumber": 42},
        {
            "pullRequestNumber": 42,
            "artifacts": [{"type": "pull", "data": {"number": 42}, "url": "https://github.com/o/r/pull/43"}],
        },
    ],
)
def test_explicit_scope_conflicts_skip_only_raw_clock_union(raw_identity: dict) -> None:
    typed = AgentTaskInventory((_task(),))
    raw = {"id": "task-1", "idleAt": "2026-10-25T19:00:00Z", **raw_identity}

    result = _normalize_agent_task_lifecycle_evidence([raw], typed)

    assert result.tasks == typed.tasks
    assert result.complete is typed.complete


@pytest.mark.parametrize(
    "raw_identity",
    [
        {"repository_full_name": "owner/repo"},
        {"repositoryFullName": "owner/repo"},
        {"repository": {"full_name": "owner/repo"}},
        {"metadata": {"repository_full_name": "owner/repo"}},
        {"metadata": {"repository": {"full_name": "owner/repo"}}},
        {"metadata": {"repositoryFullName": "owner/repo"}},
        {"metadata": {"pull_request": {"number": 42}}},
        {"pullRequest": {"number": 42}},
        {"artifacts": [{"type": "pull", "data": {"number": 42}}]},
        {"artifacts": [{"type": "pull", "url": "https://github.com/owner/repo/pull/42"}]},
    ],
)
def test_matching_scope_aliases_allow_raw_clock_union(raw_identity: dict) -> None:
    typed = AgentTaskInventory((_task(),))
    raw = {"id": "task-1", "idleAt": "2026-10-25T19:00:00Z", **raw_identity}

    result = _normalize_agent_task_lifecycle_evidence([raw], typed)

    assert result.tasks[0].idle_at == "2026-10-25T19:00:00Z"


def test_different_canonical_task_ids_do_not_union_raw_clocks() -> None:
    typed = AgentTaskInventory((_task(task_id="task-1"),))
    raw = {"id": "task-01", "task_id": "task-1", "idleAt": "2026-10-25T19:00:00Z"}

    result = _normalize_agent_task_lifecycle_evidence([raw], typed)

    assert result.tasks == typed.tasks


def test_incomplete_future_raw_clocks_are_preserved_deterministically_for_assessment() -> None:
    typed = AgentTaskInventory(
        (_task(created_at="2020-01-01T00:00:00Z"),),
        complete=False,
        incomplete_reasons=("page-limit",),
    )
    raw = {
        "id": "task-1",
        "createdAt": "2026-10-25T18:00:00Z",
        "startedAt": "2026-10-25T19:00:00Z",
        "idleAt": "9999-12-31T23:59:59Z",
    }
    original = deepcopy(raw)

    result = _normalize_agent_task_lifecycle_evidence([raw], typed)
    repeated = _normalize_agent_task_lifecycle_evidence([raw], typed)

    assert result == repeated
    assert (
        result.tasks[0].created_at,
        result.tasks[0].started_at,
        result.tasks[0].idle_at,
        result.tasks[0].sessions,
    ) == (
        "2026-10-25T18:00:00Z",
        "2026-10-25T19:00:00Z",
        "9999-12-31T23:59:59Z",
        (),
    )
    assert result.incomplete_reasons == ("page-limit",)
    assert raw == original


def test_merges_only_exact_session_ids_and_retains_distinct_and_anonymous_sessions() -> None:
    typed = _task(sessions=(AgentTaskSessionLifecycle("session-1", "running", started_at="2020-01-01T00:00:00Z"),))
    raw = {
        "id": "task-1",
        "sessions": [
            {"sessionId": "session-1", "startedAt": "2026-10-25T19:00:00Z", "state": "failed"},
            {"id": "session-2", "idle_since": "2026-10-25T19:10:00Z"},
            {"sessionId": "session-2", "idleAt": "2026-10-25T19:15:00Z"},
            {"started_at": "2026-10-25T19:20:00Z"},
            {"startedAt": "2026-10-25T19:30:00Z"},
        ],
    }

    result = _normalize_agent_task_lifecycle_evidence([raw], AgentTaskInventory((typed,)))

    assert [(session.session_id, session.state) for session in result.tasks[0].sessions] == [
        ("session-1", "running"),
        ("session-2", "in_progress"),
        ("", "in_progress"),
        ("", "in_progress"),
    ]
    assert result.tasks[0].sessions[0].started_at == "2026-10-25T19:00:00Z"
    assert result.tasks[0].sessions[1].idle_at == "2026-10-25T19:15:00Z"
    assert select_session_lifecycle_timestamp(result.tasks[0].sessions) == parse_lifecycle_timestamp(
        "2026-10-25T19:30:00Z"
    )


def test_session_creation_falls_back_only_without_activity_and_future_clocks_are_preserved() -> None:
    typed = _task(sessions=(AgentTaskSessionLifecycle("session-1", "running", created_at="2020-01-01T00:00:00Z"),))
    raw = {
        "id": "task-1",
        "createdAt": "2026-10-25T17:00:00Z",
        "idleAt": "9999-12-31T23:59:59Z",
        "sessions": [
            {"session_id": "session-1", "createdAt": "2026-10-25T19:00:00Z", "startedAt": "invalid"},
            {"id": "session-2", "createdAt": "2026-10-25T18:00:00Z", "startedAt": "2026-10-25T19:00:00Z"},
        ],
    }

    result = _normalize_agent_task_lifecycle_evidence([raw], AgentTaskInventory((typed,)))
    task = result.tasks[0]

    assert task.created_at == "2026-10-25T17:00:00Z"
    assert task.idle_at == "9999-12-31T23:59:59Z"
    assert task.sessions[0].created_at == "2026-10-25T19:00:00Z"
    assert task.sessions[0].started_at == ""
    assert task.sessions[1].created_at == "2026-10-25T18:00:00Z"
    assert task.sessions[1].started_at == "2026-10-25T19:00:00Z"
    assert select_session_lifecycle_timestamp((task.sessions[0],)) == parse_lifecycle_timestamp("2026-10-25T19:00:00Z")
    fallback = _normalize_agent_task_lifecycle_evidence(
        [{"id": "task-1", "createdAt": "2026-10-25T19:00:00Z"}],
        AgentTaskInventory((_task(started_at="", idle_at=""),)),
    )
    assert select_task_lifecycle_timestamp(fallback.tasks[0]) is None
    assert fallback.tasks[0].created_at == "2026-10-25T19:00:00Z"


def test_invalid_tasks_and_clocks_do_not_erase_typed_evidence_or_create_sessions() -> None:
    typed = _task(
        started_at="2020-01-02T00:00:00Z",
        sessions=(AgentTaskSessionLifecycle("session-1", "running", idle_at="2020-01-03T00:00:00Z"),),
    )
    inventory = AgentTaskInventory((typed,))
    raw: list[object] = [
        None,
        {"id": True, "taskId": []},
        {"id": "task-1", "startedAt": [], "idle_at": "not-a-clock", "sessions": [None, {}]},
    ]

    result = _normalize_agent_task_lifecycle_evidence(raw, inventory)

    assert result.tasks[0] == typed
    assert result.tasks[0].sessions == typed.sessions
    assert result.complete is inventory.complete
