"""Recovery workflow handlers: rollback and replan.

Contains handlers for rolling back step progress and replanning tasks
by resetting to the plan phase.
"""

from __future__ import annotations

import json as _json

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.task import TaskManager
from kanban_framework.domain.workflow import WorkflowEngine
from kanban_framework.cli.run_helpers import _resolve


def handle_rollback(args: list[str], fs: Filesystem, tm: TaskManager,
                    we: WorkflowEngine) -> dict:
    """Rollback step progress to a target step."""
    if len(args) < 2:
        return {"error": "task_id required"}
    fs, _, tm2, _ = _resolve()
    task = tm2.show(args[1])
    if task.status.value in ("archived", "cancelled"):
        return {"error": "cannot rollback an archived/cancelled task"}
    target = args[2] if len(args) >= 3 else None
    if not target:
        from kanban_framework.domain.state_machine import load_progress
        progress = load_progress(fs, task.id)
        completed = [
            {"id": k, "status": v.get("status")}
            for k, v in progress.get("steps", {}).items()
            if v.get("status") in ("completed", "skipped")
        ]
        return {
            "task_id": task.id,
            "message": "请指定回退目标步骤",
            "completed_steps": completed,
        }
    from kanban_framework.domain.state_machine import rollback_step
    return rollback_step(fs, args[1], target)


def handle_replan(args: list[str], fs: Filesystem, tm: TaskManager,
                  we: WorkflowEngine) -> dict:
    """Reset task to plan phase, clearing plan-step progress for rerun."""
    if len(args) < 2:
        return {"error": "task_id required"}
    fs, _, tm, _ = _resolve()
    task = tm.show(args[1])
    if task.status.value in ("archived", "cancelled"):
        return {"error": "cannot replan an archived task"}
    old_phase = task.phase.value
    tm.update(args[1], phase="plan")
    from kanban_framework.domain.state_machine import load_progress
    progress = load_progress(fs, args[1])
    steps = progress.get("steps", {})
    for step_id in list(steps.keys()):
        if step_id.startswith("plan"):
            steps[step_id] = {"status": "pending"}
    progress["steps"] = steps
    progress_path = fs.task_dir(args[1]) / "progress.json"
    tmp_path = progress_path.with_suffix(".tmp")
    tmp_path.write_text(_json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(progress_path)
    return {
        "task_id": args[1],
        "action": "replan",
        "from_phase": old_phase,
        "to_phase": "plan",
        "message": (
            "Task reset to plan phase. plan-phase steps will rerun. "
            "Completed subtask records are preserved. "
            "Run `kanban workflow next-step {}` to continue.'.format(args[1])"
        ),
    }
