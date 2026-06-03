"""Step-level workflow handlers: next-step, mark-step, progress, steps, run-step, skip-step.

Contains handlers for granular step progress tracking within a phase,
including querying available steps, marking step status, and resolving
step execution parameters.
"""

from __future__ import annotations

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.scheduler import Scheduler
from kanban_framework.domain.task import TaskManager
from kanban_framework.domain.workflow import WorkflowEngine
from kanban_framework.cli.run_helpers import _resolve, _auto_track_step


def handle_next_step(args: list[str], fs: Filesystem, tm: TaskManager,
                     we: WorkflowEngine) -> dict:
    """Get the next available step for a task."""
    if len(args) < 2:
        return {"error": "task_id required"}
    fs, cfg, _, _ = _resolve()
    task = tm.show(args[1])
    from kanban_framework.domain.state_machine import next_step, next_step_to_dict
    result = next_step(fs, cfg, task)
    return next_step_to_dict(result)


def handle_mark_step(args: list[str], fs: Filesystem, tm: TaskManager,
                     we: WorkflowEngine) -> dict:
    """Mark a step as completed/skipped with optional session tracking.

    When marking as completed, validates any required_artifacts defined
    on the step. Missing artifacts are reported as warnings but do not
    block the step from being marked completed (the phase-level Guard
    provides the hard block).
    """
    if len(args) < 3:
        return {"error": "task_id and step_id required"}
    fs, cfg, _, _ = _resolve()
    task_id = args[1]
    step_id = args[2]
    status = "completed"
    if len(args) >= 4:
        status = args[3]
    session_id = ""
    for i, a in enumerate(args):
        if a == "--session" and i + 1 < len(args):
            session_id = args[i + 1]

    from kanban_framework.domain.state_machine import mark_step
    progress = mark_step(fs, task_id, step_id, status)
    _auto_track_step(fs, task_id, step_id, status, session_id)

    result = {
        "task_id": task_id, "step_id": step_id, "status": status,
        "progress": progress, "session_tracked": bool(session_id),
    }

    # Step-level artifact verification on completion
    if status == "completed":
        artifact_check = _check_step_artifacts(fs, cfg, task_id, step_id)
        if artifact_check:
            result["artifact_check"] = artifact_check
            # Write artifact check results into progress.json
            progress["steps"][step_id]["artifact_check"] = artifact_check
            from kanban_framework.domain.step_progress import save_progress
            save_progress(fs, task_id, progress)

    # Auto-decider: parse decision result and suggest action
    if status == "completed":
        from kanban_framework.domain.auto_decide import should_auto_decide, parse_auto_decision
        from kanban_framework.domain.auto_decide import _decide_mode
        try:
            task = tm.show(task_id)
            if should_auto_decide(task, step_id):
                decide_mode = _decide_mode(task)
                decision = parse_auto_decision(
                    fs.task_dir(task_id), task.iteration, decide_mode)
                if decision:
                    result["auto_decision"] = decision
        except Exception:
            pass

    return result


def _check_step_artifacts(fs: Filesystem, cfg, task_id: str, step_id: str) -> dict | None:
    """Verify required_artifacts for a step. Returns None if no artifacts defined."""
    from kanban_framework.domain.step_registry import find_step_def
    quick = False
    try:
        from kanban_framework.domain.task import TaskManager
        tm = TaskManager(fs, cfg)
        task = tm.show(task_id)
        quick = getattr(task, 'mode', '') == 'quick'
        step_def = find_step_def(step_id, lightweight=getattr(task, 'lightweight', False), quick=quick)
    except Exception:
        step_def = find_step_def(step_id)

    if not step_def or not step_def.required_artifacts:
        return None

    task_dir = fs.task_dir(task_id)
    found = []
    missing = []
    for filename in step_def.required_artifacts:
        if _find_artifact_file(task_dir, filename):
            found.append(filename)
        else:
            missing.append(filename)

    return {
        "required": step_def.required_artifacts,
        "found": found,
        "missing": missing,
        "passed": len(missing) == 0,
    }


def _find_artifact_file(task_dir: Path, filename: str) -> bool:
    """Search for an artifact file across standard locations within a task dir."""
    candidates = [
        task_dir / filename,
        task_dir / "execute" / filename,
        task_dir / "evaluate" / filename,
        task_dir / "plan" / filename,
    ]
    # Also check iteration subdirectories
    for iter_dir in sorted(task_dir.glob("iteration-*")):
        candidates.append(iter_dir / filename)
        candidates.append(iter_dir / "execute" / filename)
        candidates.append(iter_dir / "evaluate" / filename)
        candidates.append(iter_dir / "reviews" / filename)
    return any(c.is_file() and c.stat().st_size > 0 for c in candidates)


def handle_progress(args: list[str], fs: Filesystem, tm: TaskManager,
                    we: WorkflowEngine) -> dict:
    """Load and return step progress for a task."""
    if len(args) < 2:
        return {"error": "task_id required"}
    fs, _, _, _ = _resolve()
    from kanban_framework.domain.state_machine import load_progress
    return {"task_id": args[1], "progress": load_progress(fs, args[1])}


def handle_steps(args: list[str], fs: Filesystem, tm: TaskManager,
                 we: WorkflowEngine) -> dict:
    """List all steps with status and available steps for a task."""
    if len(args) < 2:
        return {"error": "task_id required"}
    fs, cfg, _, _ = _resolve()
    task = tm.show(args[1])
    from kanban_framework.domain.step_registry import build_step_dag, get_available_steps
    from kanban_framework.domain.state_machine import load_progress
    from kanban_framework.domain.steps import _get_steps, _get_phase_order
    from kanban_framework.types import Phase

    # Load extensions for custom phases/steps
    mode = task.mode if task.mode not in Scheduler.BUILTIN_MODE_NAMES else ("quick" if task.mode == "quick" else ("lightweight" if task.lightweight else "full"))
    quick = task.mode == "quick"
    base_steps = _get_steps(mode)  # _get_steps already applies extensions
    base_order = _get_phase_order(task.lightweight, quick=quick, mode=task.mode,
                                   kanban_dir=cfg._fs.kanban_dir if cfg else None)
    str_order = [p.value if isinstance(p, Phase) else str(p) for p in base_order]
    dag = build_step_dag(
        lightweight=task.lightweight, quick=quick,
        mode=mode, kanban_dir=fs.kanban_dir,
        custom_steps=base_steps, custom_order=str_order,
    )
    progress = load_progress(fs, task.id)
    completed = {k for k, v in progress.get("steps", {}).items() if v.get("status") == "completed"}
    skipped = {k for k, v in progress.get("steps", {}).items() if v.get("status") == "skipped"}
    available = get_available_steps(dag, completed, skipped)
    all_steps = []
    for s in dag["steps"]:
        status = "completed" if s["id"] in completed else ("skipped" if s["id"] in skipped else "pending")
        all_steps.append({**s, "status": status})
    return {
        "task_id": task.id,
        "control_mode": task.control_mode.value,
        "mode": task.mode,
        "lightweight": task.lightweight,
        "steps": all_steps,
        "available_steps": available,
        "available_count": len(available),
    }


def handle_run_step(args: list[str], fs: Filesystem, tm: TaskManager,
                    we: WorkflowEngine) -> dict:
    """Resolve step execution parameters (prompt, actions, agent_type) for a step."""
    if len(args) < 3:
        return {"error": "task_id and step_id required"}
    fs, cfg, _, _ = _resolve()
    task = tm.show(args[1])
    step_id = args[2]
    from kanban_framework.domain.step_registry import find_step_def
    quick = getattr(task, 'mode', '') == 'quick'
    step_def = find_step_def(step_id, lightweight=task.lightweight, quick=quick)
    if not step_def:
        return {"error": f"step {step_id} not found in workflow"}
    prompt = step_def.spawn_prompt
    if prompt:
        td = fs.task_dir(task.id)
        iter_dir = td / f"iteration-{task.iteration}"
        from kanban_framework.domain.steps import _resolve_workflow_prompt, KNOWLEDGE_SEARCH_PROTOCOL
        prompt = prompt.replace("$knowledge_protocol", _resolve_workflow_prompt(cfg.workflow, "knowledge_protocol", KNOWLEDGE_SEARCH_PROTOCOL))
        prompt = prompt.replace("$task_id", task.id)
        prompt = prompt.replace("$task_dir", str(td))
        prompt = prompt.replace("$report_dir", str(iter_dir))
        prompt = prompt.replace("$iteration", str(task.iteration))
        prompt = prompt.replace("$biz_tag", task.biz_tag or "")
        prompt = prompt.replace("$title", task.title or "")
        prompt = prompt.replace("$description", task.description or "")
        prompt = prompt.replace("$phase", task.phase_id or "")
        prompt = prompt.replace("$mode", task.mode or "")
    # Auto-decider: inject spawn_prompt for user_action steps when auto_mode enabled
    if not prompt and step_def.user_action:
        from kanban_framework.domain.auto_decide import should_auto_decide, build_auto_decide_prompt
        if should_auto_decide(task, step_id):
            prompt = build_auto_decide_prompt(task, step_id, fs)
    from kanban_framework.domain.state_machine import _inject_knowledge_json
    actions = _inject_knowledge_json(
        [a.replace("$task_id", task.id).replace("$biz_tag", task.biz_tag or "") for a in step_def.actions])
    # Map kanban-* agent types to Claude Code subagent_type
    kanban_type = step_def.agent_type or ""
    subagent_type = "general-purpose" if kanban_type.startswith("kanban-") else kanban_type
    return {
        "task_id": task.id,
        "step_id": step_id,
        "description": step_def.description,
        "actions": actions,
        "agent_type": kanban_type,
        "subagent_type": subagent_type,
        "parallel": step_def.parallel,
        "user_action": step_def.user_action,
        "interactive": step_def.interactive,
        "spawn_prompt": prompt,
        "required_artifacts": step_def.required_artifacts,
    }


def handle_skip_step(args: list[str], fs: Filesystem, tm: TaskManager,
                     we: WorkflowEngine) -> dict:
    """Skip a step that is not required."""
    if len(args) < 3:
        return {"error": "task_id and step_id required"}
    fs, _, tm, _ = _resolve()
    task = tm.show(args[1])
    from kanban_framework.domain.step_registry import find_step_def
    quick = getattr(task, 'mode', '') == 'quick'
    step_def = find_step_def(args[2], lightweight=task.lightweight, quick=quick, mode=getattr(task, 'mode', None))
    if not step_def:
        return {"error": f"step {args[2]} not found in workflow"}
    from kanban_framework.domain.state_machine import mark_step
    progress = mark_step(fs, args[1], args[2], "skipped")
    return {"task_id": args[1], "step_id": args[2], "status": "skipped",
            "progress": progress}
