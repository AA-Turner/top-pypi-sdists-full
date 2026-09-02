"""Tests for selecting the latest agent task for a pull request."""

from agentic_devtools.cli.ci.supervisor import select_latest_agent_task


def test_select_latest_agent_task_filters_pr_and_orders_by_update_time() -> None:
    tasks = [
        {"id": "older", "pullRequestNumber": 7, "status": "completed", "updatedAt": "2026-08-31T10:00:00Z"},
        {"id": "other", "pullRequestNumber": 8, "status": "completed", "updatedAt": "2026-08-31T12:00:00Z"},
        {"id": "newer", "pullRequestNumber": 7, "status": "in_progress", "updatedAt": "2026-08-31T11:00:00Z"},
    ]

    assert select_latest_agent_task(tasks, 7) == tasks[2]


def test_select_latest_agent_task_returns_none_for_no_matching_task() -> None:
    assert select_latest_agent_task([], 7) is None


def test_select_latest_agent_task_ignores_malformed_entries_and_accepts_string_pr_numbers() -> None:
    tasks = [
        "malformed",
        {"id": "one", "pullRequestNumber": "7", "createdAt": "2026-08-31T10:00:00Z"},
        {"id": "missing-time", "pullRequestNumber": 7},
    ]

    assert select_latest_agent_task(tasks, 7) == tasks[1]
