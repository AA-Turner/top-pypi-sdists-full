"""Workflow command dispatcher.

Routes workflow subcommands to handler modules using the Command pattern.
Handler modules:
- workflow_phase: transition, complete-phase, self-improve-check, get-roles,
  next-phase, checkpoint
- workflow_step: next-step, mark-step, progress, steps, run-step, skip-step
- workflow_iteration: start-iteration, collect-iteration-artifacts
- workflow_recovery: rollback, replan
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.task import TaskManager
from kanban_framework.domain.workflow import WorkflowEngine
from kanban_framework.cli.run_helpers import _resolve
from kanban_framework.cli.workflow_phase import (
    GuardError,
    handle_transition,
    handle_complete_phase,
    handle_self_improve_check,
    handle_get_roles,
    handle_next_phase,
    handle_checkpoint,
)
from kanban_framework.cli.workflow_step import (
    handle_next_step,
    handle_mark_step,
    handle_progress,
    handle_steps,
    handle_run_step,
    handle_skip_step,
)
from kanban_framework.cli.workflow_iteration import (
    handle_start_iteration,
    handle_collect_iteration_artifacts,
)
from kanban_framework.cli.workflow_recovery import (
    handle_rollback,
    handle_replan,
)

# Subcommand → handler dispatch table (Command pattern)
HandlerFn = Callable[[list[str], Filesystem, TaskManager, WorkflowEngine], dict]
_DISPATCH_TABLE: dict[str, HandlerFn] = {
    "transition": handle_transition,
    "complete-phase": handle_complete_phase,
    "self-improve-check": handle_self_improve_check,
    "get-roles": handle_get_roles,
    "get-phase-agents": handle_get_roles,
    "next-phase": handle_next_phase,
    "checkpoint": handle_checkpoint,
    "next-step": handle_next_step,
    "mark-step": handle_mark_step,
    "progress": handle_progress,
    "steps": handle_steps,
    "run-step": handle_run_step,
    "skip-step": handle_skip_step,
    "start-iteration": handle_start_iteration,
    "collect-iteration-artifacts": handle_collect_iteration_artifacts,
    "rollback": handle_rollback,
    "replan": handle_replan,
}


def cmd_workflow(args: list[str]) -> dict:
    """Dispatch workflow subcommand to the appropriate handler."""
    if not args:
        return {"error": "subcommand required", "available": sorted(_DISPATCH_TABLE.keys())}
    sub = args[0]

    # v0.194: workflow stats — reads from JSONL, not task dirs
    if sub == "stats" and len(args) >= 2:
        from kanban_framework.domain.workflow_stats import WorkflowStatsReader
        reader = WorkflowStatsReader(fs.kanban_dir.parent if (fs := _resolve()[0]) else Path.cwd())
        return reader.get_workflow_summary(args[1])

    fs, _, tm, we = _resolve()
    handler = _DISPATCH_TABLE.get(sub)
    if handler:
        return handler(args, fs, tm, we)
    return {"error": f"unknown workflow subcommand: {sub}", "available": sorted(_DISPATCH_TABLE.keys())}
