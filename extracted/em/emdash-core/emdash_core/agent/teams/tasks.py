"""Team task coordination — bridges Agent Teams with Tasks v2.

Agent Teams does NOT create its own task system. Instead, it creates
a Tasks v2 task list and lets teammates use the standard claim/complete
tools. This module provides the bridge:

  1. Creates the team's shared task list in Tasks v2
  2. Provides helper functions for the lead to create/assign tasks
  3. Extends task creation with team-specific metadata (assigned_to, labels)
  4. Wires up task completion events to trigger team hooks

The key insight is: Tasks v2 already has atomic claiming, dependency
management, label filtering, and file-based locking. We reuse all of it.
The only addition is team-aware helpers for the lead.
"""

from typing import Any, Optional

from ...utils.logger import log


def create_team_task_list(team_name: str) -> str:
    """Create a Tasks v2 task list for a team.

    Returns the task_list_id.
    """
    from ...tasks.store import TaskStore

    task_list_id = f"team-{team_name}"
    store = TaskStore()

    # Create the task list if it doesn't exist
    store.create_task_list(
        task_list_id=task_list_id,
        name=f"Agent Team: {team_name}",
        description=f"Shared task list for agent team '{team_name}'",
    )

    log.info(f"Created team task list: {task_list_id}")
    return task_list_id


def create_team_task(
    task_list_id: str,
    title: str,
    description: str = "",
    labels: list[str] | None = None,
    depends_on: list[str] | None = None,
    priority: int = 0,
    assigned_to: str | None = None,
    created_by: str = "lead",
) -> dict[str, Any]:
    """Create a task in the team's shared task list.

    This is a convenience wrapper over TaskStore.add_task() that
    adds team-specific behavior:
    - If assigned_to is set, auto-claim the task for that teammate
    - Labels are used for teammate filtering (e.g., ["backend", "security"])

    Args:
        task_list_id: The team's task list ID.
        title: Task title.
        description: Detailed description.
        labels: Labels for categorization and teammate filtering.
        depends_on: Task IDs that must complete first.
        priority: Higher = more important.
        assigned_to: Teammate session ID to auto-assign.
        created_by: Who created the task (default "lead").

    Returns:
        Dict with task info including the new task ID.
    """
    from ...tasks.store import TaskStore

    store = TaskStore()

    task = store.add_task(
        task_list_id=task_list_id,
        title=title,
        description=description,
        labels=labels or [],
        depends_on=depends_on or [],
        priority=priority,
        created_by=created_by,
    )

    result = {
        "task_id": task.id,
        "title": task.title,
        "labels": task.labels,
        "depends_on": task.depends_on,
    }

    # Auto-assign if requested
    if assigned_to:
        success, message = store.claim_task(
            task_list_id=task_list_id,
            task_id=task.id,
            session_id=assigned_to,
        )
        result["assigned_to"] = assigned_to
        result["assignment_success"] = success
        result["assignment_message"] = message

    return result


def get_team_task_summary(task_list_id: str) -> dict[str, Any]:
    """Get a summary of the team's task list.

    Returns task counts by status and per-teammate progress.
    """
    from ...tasks.store import TaskStore
    from ...tasks.models import TaskStatus

    store = TaskStore()
    all_tasks = store.get_all_tasks(task_list_id)

    by_status = {"pending": 0, "in_progress": 0, "completed": 0, "blocked": 0}
    by_assignee: dict[str, dict] = {}

    for task in all_tasks:
        by_status[task.status.value] = by_status.get(task.status.value, 0) + 1

        assignee = task.claimed_by or "unassigned"
        if assignee not in by_assignee:
            by_assignee[assignee] = {"total": 0, "completed": 0, "in_progress": 0}
        by_assignee[assignee]["total"] += 1
        if task.status == TaskStatus.COMPLETED:
            by_assignee[assignee]["completed"] += 1
        elif task.status == TaskStatus.IN_PROGRESS:
            by_assignee[assignee]["in_progress"] += 1

    total = len(all_tasks)
    completed = by_status.get("completed", 0)

    return {
        "task_list_id": task_list_id,
        "total": total,
        "by_status": by_status,
        "by_assignee": by_assignee,
        "progress_percent": round((completed / total * 100) if total > 0 else 0, 1),
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status.value,
                "labels": t.labels,
                "claimed_by": t.claimed_by,
                "depends_on": t.depends_on,
                "priority": t.priority,
            }
            for t in all_tasks
        ],
    }
