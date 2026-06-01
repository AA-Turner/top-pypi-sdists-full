"""Phase-level workflow handlers: transition, complete-phase, and phase queries.

Contains handlers for FSM phase transitions, phase completion (with guard
checks, knowledge extraction, token tracking), and phase-related queries
(self-improve-check, get-roles, next-phase, checkpoint).
"""

from __future__ import annotations

import subprocess

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.domain.task import TaskManager
from kanban_framework.domain.workflow import WorkflowEngine
from kanban_framework.domain.guard import Guard
from kanban_framework.types import Phase
from kanban_framework.cli.run_helpers import (
    _resolve, _validate_fsm_state, _track_phase_time,
)
from kanban_framework.cli.workflow_knowledge import extract_knowledge


class GuardError(Exception):
    pass


def _raise_guard_error(fs, task, check_result, label: str):
    """Raise GuardError with issue capture for auto-mode tasks."""
    msg = f"{label} failed for {task.id}: " + "; ".join(check_result.failures)
    try:
        from kanban_framework.infra.issue_capture import capture_issue
        capture_issue(fs, task, GuardError(msg), {"action": "complete-phase", "check": label})
    except Exception:
        pass
    raise GuardError(msg)


def handle_transition(args: list[str], fs: Filesystem, tm: TaskManager,
                      we: WorkflowEngine) -> dict:
    """Transition a task to a target phase."""
    if len(args) < 3:
        # List available target phases for the task's current mode
        if len(args) >= 2:
            try:
                task = tm.show(args[1])
                quick = getattr(task, 'mode', '') == 'quick'
                from kanban_framework.infra.scheduler import Scheduler
                order = Scheduler.dispatch_order(lightweight=task.lightweight, quick=quick)
                available = [p.value if hasattr(p, 'value') else str(p) for p in order]
                return {
                    "error": "target phase required",
                    "task_id": args[1],
                    "current_phase": task.phase_id,
                    "available_phases": available,
                    "hint": f"Usage: kanban workflow transition {args[1]} <target_phase>",
                }
            except Exception:
                pass
        return {"error": "task_id and target phase required"}
    task = tm.show(args[1])
    validation = _validate_fsm_state(task, tm)
    if validation:
        return validation
    from_phase = task.phase.value
    try:
        target = Phase(args[2])
    except ValueError:
        target = args[2]
    new_phase = we.transition(task, target)
    new_phase_str = new_phase.value if isinstance(new_phase, Phase) else str(new_phase)
    tm.update(task.id, phase=new_phase_str, history=task.history)
    return {"task_id": task.id, "from": from_phase, "to": new_phase_str}


def handle_complete_phase(args: list[str], fs: Filesystem, tm: TaskManager,
                          we: WorkflowEngine) -> dict:
    """Complete current phase: guard checks, knowledge extraction, step auto-mark, token tracking."""
    if len(args) < 2:
        return {"error": "task_id required"}
    fs, cfg, tm, _ = _resolve()
    task = tm.show(args[1])
    validation = _validate_fsm_state(task, tm)
    if validation:
        return validation
    guard = Guard(fs, cfg)
    guard_result = guard.check_artifacts(task, task.phase, lightweight=task.lightweight)
    if not guard_result.passed:
        _raise_guard_error(fs, task, guard_result, "guard check")
    # Checkpoint step guard (#v0.84)
    from kanban_framework.domain.step_registry import build_step_dag
    quick = getattr(task, 'mode', '') == 'quick'
    dag = build_step_dag(lightweight=task.lightweight, quick=quick)
    for step in dag["steps"]:
        if step["phase"] == task.phase.value and step["type"] == "checkpoint":
            step_guard = guard.check_step(task, step)
            if not step_guard.passed:
                _raise_guard_error(fs, task, step_guard, f"checkpoint {step['id']}")
    phase_check = guard.check_phase_completeness(task, lightweight=task.lightweight)
    if not phase_check.passed:
        _raise_guard_error(fs, task, phase_check, "phase completeness")
    # IR-17: Evaluate phase score gate
    if task.phase == Phase.EVALUATE:
        from kanban_framework.cli.evaluator import _record_score
        sync_result = _record_score(fs, tm, args[1])
        if sync_result.get("recorded"):
            task = tm.show(args[1])
        score_check = guard.check_evaluation_score(task)
        if task.score_history and task.score_history != (tm.show(task.id).score_history or []):
            tm.update(task.id, score_history=task.score_history)
        if not score_check.passed:
            _raise_guard_error(fs, task, score_check, "evaluation score")

    knowledge_result = extract_knowledge(task, fs)

    _track_phase_time(task.id, task.phase.value, "end")
    from kanban_framework.domain.state_machine import mark_step, _get_steps
    steps_map = _get_steps(
        "quick" if getattr(task, 'mode', '') == 'quick'
        else ("lightweight" if task.lightweight else "full")
    )
    for step_def in steps_map.get(task.phase.value, []):
        mark_step(fs, task.id, step_def.id, "completed")
    updated = we.complete_phase(task)
    tm.update(task.id, phase=updated.phase.value, history=updated.history)

    _collect_token_usage(task, fs)

    result = {"task_id": task.id, "phase": updated.phase.value}
    result.update(knowledge_result)
    return result


def _collect_token_usage(task, fs: Filesystem) -> None:
    """Auto-collect token usage from JSONL for the completed phase."""
    try:
        from kanban_framework.infra.token_tracking import TokenTracker
        reports_dir = fs.kanban_dir / "reports"
        tt = TokenTracker(reports_dir / "token_tracking.json")
        t_min = None
        t_max = None
        for h in task.history:
            if h.get("phase") == task.phase.value:
                ts = h.get("started_at")
                if ts and t_min is None:
                    t_min = ts - 30 if ts else None
                ts = h.get("completed_at")
                if ts:
                    t_max = ts + 30 if t_max is None else max(t_max, ts + 30)
        if t_min and t_max:
            tt.auto_collect(task.id, task.phase.value, t_min, t_max)
    except Exception:
        pass


def handle_self_improve_check(args: list[str], fs: Filesystem, tm: TaskManager,
                              we: WorkflowEngine) -> dict:
    """Check whether task should self-improve (restart iteration) based on score."""
    if len(args) < 2:
        return {"error": "task_id required"}
    task = tm.show(args[1])
    if not task.score_history:
        from kanban_framework.cli.evaluator import _record_score
        sync_result = _record_score(fs, tm, args[1])
        if sync_result.get("recorded"):
            task = tm.show(args[1])
    avg_score = None
    for i, arg in enumerate(args):
        if arg == "--avg-score" and i + 1 < len(args):
            try:
                avg_score = float(args[i + 1])
            except (ValueError, TypeError):
                return {"error": f"invalid --avg-score value: {args[i+1]}"}
            break
    if avg_score is None and len(args) >= 3:
        try:
            avg_score = float(args[2])
        except (ValueError, TypeError):
            return {"error": f"invalid avg_score value: {args[2]}"}
    if avg_score is None:
        if task.score_history:
            latest = task.score_history[-1]
            from kanban_framework.domain.guard import _first_history_score
            resolved = _first_history_score(latest)
            avg_score = resolved if resolved is not None else 0.0
        else:
            return {"error": "no avg_score provided and no score_history in task"}
    result = we.self_improve_check(task, avg_score)
    return {"task_id": task.id, **result}


def handle_get_roles(args: list[str], fs: Filesystem, tm: TaskManager,
                     we: WorkflowEngine) -> dict:
    """Get agent roles and scheduling config for a phase."""
    phase_str = args[1] if len(args) > 1 else "evaluate"
    cfg = Config(Filesystem(root=Filesystem.find_project_root()))
    workflow = cfg.workflow
    phase_config = None
    for p in workflow.get("phases", []):
        if p.get("id") == phase_str:
            phase_config = p
            break
    agents = phase_config.get("agents", []) if phase_config else []
    if not agents and phase_str == "evaluate":
        from kanban_framework.infra.scheduler import Scheduler
        agents = Scheduler.eval_roles()
    raw = cfg.raw
    timeout = raw.get("timeout", {})
    scheduler_cfg = raw.get("scheduler", {})
    scheduling = {
        "single_agent_seconds": timeout.get("single_agent_seconds", 180),
        "phase_timeout_seconds": timeout.get(f"{phase_str}_seconds"),
        "max_parallel": scheduler_cfg.get("max_parallel", 3),
        "poll_interval_seconds": scheduler_cfg.get("poll_interval_seconds", 30),
    }
    return {"phase": phase_str, "agents": agents, "scheduling": scheduling}


def handle_next_phase(args: list[str], fs: Filesystem, tm: TaskManager,
                      we: WorkflowEngine) -> dict:
    """Get the next phase after the task's current phase."""
    if len(args) < 2:
        return {"error": "task_id required"}
    task = tm.show(args[1])
    quick = getattr(task, 'mode', '') == 'quick'
    next_p = we.next_phase(task.phase, lightweight=task.lightweight, quick=quick)
    return {
        "task_id": task.id,
        "current": task.phase.value,
        "next": next_p.value if next_p else None,
    }


def handle_checkpoint(args: list[str], fs: Filesystem, tm: TaskManager,
                      we: WorkflowEngine) -> dict:
    """Create a git checkpoint commit for the current phase."""
    if len(args) < 3:
        return {"error": "task_id and phase required"}
    task = tm.show(args[1])
    phase = args[2]
    task_dir = fs.task_dir(task.id)
    result = subprocess.run(
        ["git", "add", "-f", str(task_dir.relative_to(Filesystem.find_project_root()))],
        capture_output=True, text=True,
    )
    msg = f"checkpoint: {phase} ({task.id})"
    commit = subprocess.run(
        ["git", "commit", "-m", msg, "--allow-empty"],
        capture_output=True, text=True,
    )
    committed = commit.returncode == 0
    return {
        "subcommand": "checkpoint",
        "task_id": task.id,
        "phase": phase,
        "committed": committed,
        "message": f"Git checkpoint: {phase} ({task.id})",
    }
