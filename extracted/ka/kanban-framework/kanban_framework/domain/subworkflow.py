"""Sub-workflow — spawns independent kanban tasks for complex subtasks.

When a subtask declares "workflow": "<mode_name>", the executor creates
a real kanban task that starts at plan phase. The orchestrator runs it
through all phases like any other task.

The child task runs independently with its own phases, guard checks, and
progress tracking. The parent tracks child IDs in progress.json.
"""
from __future__ import annotations
from pathlib import Path
from kanban_framework.types import Task


def spawn_subtask(kanban_dir: Path, parent_task: Task, subtask: dict) -> str | None:
    """Create a child kanban task for a subtask with workflow field.

    The child starts at plan phase and is ready for kanban run.
    Returns the child task ID, or None on failure.
    """
    st_id = subtask.get("id", "")
    st_title = subtask.get("title", st_id)
    st_workflow = subtask.get("workflow", "full")

    from kanban_framework.infra.filesystem import Filesystem
    from kanban_framework.infra.config import Config
    from kanban_framework.domain.task import TaskManager

    root = kanban_dir.parent
    fs = Filesystem(root=root)
    cfg = Config(fs)
    tm = TaskManager(fs, cfg)

    desc_parts = []
    task_dir = kanban_dir / "tasks" / parent_task.id
    try:
        spec_text = (task_dir / "spec.md").read_text(encoding="utf-8")[:600]
        desc_parts.append(spec_text)
    except OSError:
        pass
    desc = "\n".join(desc_parts) if desc_parts else f"Subtask of {parent_task.id}"

    try:
        child = tm.create(
            title=f"[{parent_task.id}] {st_title}",
            description=desc,
        )
        tm.update(child.id, mode=st_workflow)
        return child.id
    except Exception:
        return None


def check_child_status(fs, child_id: str) -> str:
    """Check a child task's completion status."""
    try:
        from kanban_framework.infra.config import Config
        from kanban_framework.domain.task import TaskManager
        cfg = Config(fs)
        tm = TaskManager(fs, cfg)
        task = tm.show(child_id)
        return task.status.value if hasattr(task.status, 'value') else str(task.status)
    except Exception:
        return "error"


def all_children_done(fs, child_ids: list[str]) -> bool:
    """Check if all child tasks have reached terminal status."""
    for cid in child_ids:
        status = check_child_status(fs, cid)
        if status not in ("completed", "archived", "cancelled"):
            return False
    return True
