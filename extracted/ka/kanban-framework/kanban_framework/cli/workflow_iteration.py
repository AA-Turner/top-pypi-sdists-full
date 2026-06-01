"""Iteration workflow handlers: start-iteration and collect-iteration-artifacts.

Contains handlers for managing iteration lifecycle — starting new iterations
(hot/full) with artifact isolation, and collecting iteration artifacts.
"""

from __future__ import annotations

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.task import TaskManager
from kanban_framework.domain.workflow import WorkflowEngine
from kanban_framework.types import Phase
from kanban_framework.cli.run_helpers import _resolve, _collect_iteration_artifacts


def handle_start_iteration(args: list[str], fs: Filesystem, tm: TaskManager,
                           we: WorkflowEngine) -> dict:
    """Start a new iteration (hot or full) with artifact isolation."""
    if len(args) < 3:
        return {"error": "task_id and type (hot/full) required"}
    task_id = args[1]
    itype = args[2]
    if itype not in ("hot", "full"):
        return {"error": "iteration type must be hot or full"}

    fs2, _, tm2, _ = _resolve()
    task = tm2.show(task_id)
    old_iter = task.iteration
    new_iter = old_iter + 1
    task_dir = fs2.task_dir(task_id)

    # Move execution artifacts from task root to iteration-{N}/ for isolation
    for fname in ["execution_summary.md", "execution_pitfalls.md", "execution_decisions.md"]:
        src = task_dir / fname
        if fs2.file_exists(src):
            dest_dir = fs2.iteration_dir(task_id, old_iter)
            fs2.ensure_dir(dest_dir)
            src.rename(dest_dir / fname)

    # Set phase and increment iteration
    target_phase = Phase.EXECUTE if itype == "hot" else Phase.PLAN
    tm2.update(task_id, phase=target_phase.value, iteration=new_iter)
    return {
        "task_id": task_id,
        "type": itype,
        "iteration": new_iter,
        "phase": target_phase.value,
    }


def handle_collect_iteration_artifacts(args: list[str], fs: Filesystem,
                                       tm: TaskManager,
                                       we: WorkflowEngine) -> dict:
    """Collect all artifacts for the current iteration."""
    if len(args) < 2:
        return {"error": "task_id required"}
    fs3, _, _, _ = _resolve()
    return {"task_id": args[1], "artifacts": _collect_iteration_artifacts(fs3, args[1])}
