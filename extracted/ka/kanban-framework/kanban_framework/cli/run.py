from __future__ import annotations
import logging
import time
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.infra.git import Git, GitError
from kanban_framework.infra.worktree import Worktree, WorktreeError
from kanban_framework.domain.task import TaskManager, TaskNotFoundError
from kanban_framework.domain.workflow import WorkflowEngine, TransitionError
from kanban_framework.domain.nlp import parse_nlp
from kanban_framework.domain.recovery import recover_list, recover_check_timeout, resume_task, rollback_task
from kanban_framework.types import Phase
from kanban_framework.infra.scheduler import Scheduler
from kanban_framework.infra.consts import Consts


def _resolve_phase(phase_str: str):
    """Resolve phase string to Phase enum or plain string for custom phases."""
    try:
        return Phase(phase_str)
    except ValueError:
        return phase_str
from kanban_framework.cli.run_helpers import (
    _resolve,
    _resolve_worktree,
    _validate_fsm_state,
    _track_phase_time,
    _get_agents_for_phase,
    _apply_trigger_conditions,
    _get_time_summary,
    _append_time_token_to_retrospective,
    _knowledge_health_on_archive,
    _move_to_archive,
    _check_brainstorming_gate,
)

# Re-exports for backward compatibility
from kanban_framework.cli.guard_cmd import cmd_guard       # noqa: F401
from kanban_framework.cli.workflow_cmd import cmd_workflow  # noqa: F401
from kanban_framework.cli.workflow_cmd import GuardError    # noqa: F401


# ── run ──────────────────────────────────────────────────────────

def cmd_run(args: list[str]) -> dict:
    _log = logging.getLogger("kanban")
    if not args:
        return {"error": "task_id required"}
    task_id = args[0]
    fs, cfg, tm, we = _resolve()
    task = tm.show(task_id)
    _log.info("run: task=%s phase=%s mode=%s",
              task_id, task.phase_id, getattr(task, 'mode', '') or Consts.DEFAULT_MODE)
    # FSM state validation (skip for --lightweight override, which changes mode)
    lightweight_requested = "--lightweight" in args
    if not lightweight_requested:
        validation = _validate_fsm_state(task, tm)
        if validation:
            return validation
    # Set default mode BEFORE transition (fix #147, --lightweight backward compat)
    if lightweight_requested and task.mode != Consts.DEFAULT_MODE:
        task = tm.update(task_id, mode=Consts.DEFAULT_MODE)
    if len(args) > 2 and args[1] == "--phase":
        target = _resolve_phase(args[2])
    elif len(args) > 3 and args[2] == "--phase":
        target = _resolve_phase(args[3])
    else:
        next_p = Scheduler.next_phase(task.phase,
                                      mode=getattr(task, 'mode', None), workflow=cfg.workflow,
                                      kanban_dir=fs.kanban_dir)
        if next_p is None:
            return {
                "task_id": task_id,
                "phase": task.phase_id,
                "message": "already at terminal phase",
            }
        target = next_p

    # IR-16: brainstorming gate before plan → plan_review
    brainstorming = None
    target_str = target.value if isinstance(target, Phase) else str(target)
    if task.phase_id == Phase.PLAN.value and target_str == Phase.PLAN_REVIEW.value:
        brainstorming = _check_brainstorming_gate(task.description, cfg.workflow, getattr(task, 'mode', None), fs.kanban_dir)
        if not brainstorming["passed"]:
            return {
                "task_id": task_id,
                "phase": task.phase_id,
                "message": (
                    "brainstorming gate blocked: task description lacks "
                    + ", ".join(m["label"] for m in brainstorming["missing"])
                ),
                "brainstorming_gate": brainstorming,
                "required_action": (
                    "complete Plan Step A (superpowers:brainstorming) to "
                    "produce spec.md before transitioning to plan_review"
                ),
            }

    # Record knowledge usage before phase transition (#478)
    try:
        from kanban_framework.domain.context import _load_knowledge_summary
        _load_knowledge_summary(fs, task)
    except Exception:
        pass

    try:
        new_phase = we.transition(task, target)
        _log.info("transition: task=%s %s -> %s", task_id, task.phase_id, new_phase)
    except TransitionError as e:
        _log.warning("transition blocked: task=%s %s -> %s: %s", task_id, task.phase_id, target_str, e)
        from kanban_framework.infra.issue_capture import capture_issue
        capture_issue(fs, task, e, {"action": "transition", "target": target_str})
        return {
            "task_id": task_id,
            "phase": task.phase_id,
            "message": str(e),
        }
    except Exception as e:
        from kanban_framework.infra.issue_capture import capture_issue
        capture_issue(fs, task, e, {"action": "run", "target": target_str})
        raise
    new_phase_str = new_phase.value if isinstance(new_phase, Phase) else str(new_phase)
    tm.update(task_id, phase=new_phase_str, history=task.history)
    _track_phase_time(task_id, new_phase_str, "start")
    agents = _get_agents_for_phase(fs, new_phase_str,
                                     task_description=task.description,
                                     mode=task.mode or Consts.DEFAULT_MODE)
    result = {
        "task_id": task_id,
        "phase": new_phase_str,
        "message": f"entered {new_phase_str} phase",
        "guard": {"passed": True},
        "agents_to_spawn": agents,
        "agent_count": len(agents),
    }
    # Include step info for the new phase
    from kanban_framework.domain.steps import _get_steps
    mode = task.mode or Consts.DEFAULT_MODE
    steps_map = _get_steps(mode)
    phase_steps = steps_map.get(new_phase_str, [])
    if not phase_steps:
        # Check extensions for custom phase steps
        from kanban_framework.domain.workflow_extensions import WorkflowExtension
        ext = WorkflowExtension(cfg.workflow)
        ext_steps = ext.build_step_map(steps_map, mode=mode)
        phase_steps = ext_steps.get(new_phase_str, [])
    if phase_steps:
        result["phase_steps"] = [
            {"id": s.id, "description": s.description, "agent_type": s.agent_type}
            for s in phase_steps
        ]
    if brainstorming is not None:
        result["brainstorming_gate"] = brainstorming

    # Mode handling: show phase order for any non-custom mode
    if task.mode == "custom" and task.custom_fsm:
        result["mode"] = "custom"
        custom_phases = task.custom_fsm.get("phases", [])
        custom_eval_agents = task.custom_fsm.get("evaluate_agents", [])
        result["phase_order"] = custom_phases
        result["message"] = (
            f"自定义模式: {' → '.join(custom_phases)}, "
            f"评估 Agent: {', '.join(a['name'] for a in custom_eval_agents) if custom_eval_agents else '无'}"
        )
    else:
        # Show phase order for any mode (lightweight, quick, or custom workflow)
        from kanban_framework.infra.config import Config
        cfg = Config(fs)
        mode_phases = [p.value if hasattr(p, "value") else str(p)
                       for p in Scheduler.dispatch_order(
                           mode=task.mode, workflow=cfg.workflow,
                           kanban_dir=fs.kanban_dir)]
        result["mode"] = task.mode
        result["phase_order"] = mode_phases
        result["message"] = f"模式: {task.mode} — {' → '.join(mode_phases)}"

    # Subagent dispatch info
    for agent in agents:
        if agent.get("subagent_required"):
            result.setdefault("subagent_required", []).append(agent["role"])

    return result


# ── decide ───────────────────────────────────────────────────────

def cmd_decide(args: list[str]) -> dict:
    if not args:
        return {"error": "task_id required"}
    # Parse args order-independently: task_id is the first non-flag arg
    task_id = ""
    action = "approve_and_archive"
    i = 0
    while i < len(args):
        if args[i] == "--action" and i + 1 < len(args):
            action = args[i + 1]
            i += 2
        elif not task_id and not args[i].startswith("-"):
            task_id = args[i]
            i += 1
        else:
            i += 1
    if not task_id:
        return {"error": "task_id required"}
    fs, _, tm, we = _resolve()
    task = tm.show(task_id)
    valid_actions = {"approve_and_archive", "abort", "restart_from_plan", "restart_from_execute"}
    if action not in valid_actions:
        return {"error": f"unknown action: {action}", "valid_actions": sorted(valid_actions)}

    # Phase validation (Issue #111, #352-6)
    # abort is allowed from any phase; other actions require specific phases
    allowed_phases = {Phase.USER_DECISION, Phase.EVALUATE, Phase.RETROSPECTIVE, Phase.ARCHIVE}
    if action == "abort":
        pass  # abort from any phase
    elif task.phase not in allowed_phases and task.phase_id != Phase.ARCHIVE.value:
        return {
            "error": f"cannot decide at phase {task.phase_id}",
            "expected_phases": sorted(p.value for p in allowed_phases),
        }

    tm.record_decision(task_id, action)
    tm.update(task_id, user_decision={"action": action})

    # Guard check before approve_and_archive (#402-2)
    if action == "approve_and_archive":
        from kanban_framework.domain.guard import Guard
        from kanban_framework.infra.config import Config
        cfg = Config(fs)
        guard = Guard(fs, cfg)
        guard_result = guard.check_artifacts(task, task.phase)
        if not guard_result.passed:
            return {
                "error": f"guard check failed: {'; '.join(guard_result.failures)}",
                "guard_failures": guard_result.failures,
            }

    # Execute the action (fix #82)
    if action == "approve_and_archive":
        # Ensure score_history is synced before archiving (#440)
        if not task.score_history:
            from kanban_framework.cli.evaluator import _record_score
            sync_result = _record_score(fs, tm, task_id)
            if sync_result.get("recorded"):
                task = tm.show(task_id)
        tm.update(task_id, phase="archive", status="archived")
        time_summary = _get_time_summary(task_id)
        # Write artifacts BEFORE moving directory (#262)
        _append_time_token_to_retrospective(task_id)
        _knowledge_health_on_archive(task_id)
        _move_to_archive(fs, task_id)
        # Auto-archive inbox items (Issue #108)
        from kanban_framework.cli.inbox import archive_on_task_completion
        inbox_result = archive_on_task_completion(task_id)
        result = {
            "task_id": task_id,
            "action": action,
            "message": f"user decision: {action} — executed",
            "time": time_summary,
        }
        if inbox_result.get("archived_count", 0) > 0:
            result["inbox_archived"] = inbox_result.get("archived_count")
        return result
    elif action == "abort":
        tm.update(task_id, phase="archive", status="cancelled")
        time_summary = _get_time_summary(task_id)
        _move_to_archive(fs, task_id)
        return {
            "task_id": task_id,
            "action": action,
            "message": f"user decision: {action} — executed",
            "time": time_summary,
        }
    elif action == "restart_from_plan":
        tm.update(task_id, phase="plan", status="in_progress", iteration=task.iteration + 1)
    elif action == "restart_from_execute":
        tm.update(task_id, phase="execute", status="in_progress", iteration=task.iteration + 1)

    return {
        "task_id": task_id,
        "action": action,
        "message": f"user decision: {action} — executed",
    }


# ── worktree ─────────────────────────────────────────────────────

def cmd_worktree(args: list[str]) -> dict:
    if not args:
        return {"error": "subcommand required"}
    sub = args[0]
    g, wt = _resolve_worktree()

    if sub == "create":
        if len(args) < 2:
            return {"error": "task_id required"}
        task_id = args[1]
        branch = f"task/{task_id}"
        try:
            path = wt.create(task_id, branch)
            # Persist worktree path to task.json
            fs3, _, tm3, _ = _resolve()
            try:
                tm3.update(task_id, worktree_path=str(path))
            except TaskNotFoundError:
                pass
            return {
                "subcommand": sub,
                "task_id": task_id,
                "branch": branch,
                "path": str(path),
            }
        except WorktreeError as e:
            return {"error": str(e)}

    if sub == "remove":
        if len(args) < 2:
            return {"error": "task_id required"}
        task_id = args[1]
        force = "--force" in args
        try:
            wt.remove(task_id, force=force)
            return {"subcommand": sub, "task_id": task_id, "removed": True}
        except WorktreeError as e:
            return {"error": str(e)}

    if sub == "exists":
        if len(args) < 2:
            return {"error": "task_id required"}
        return {"subcommand": sub, "task_id": args[1], "exists": wt.exists(args[1])}

    if sub == "list":
        return {"subcommand": sub, "worktrees": wt.list_all()}

    if sub == "merge":
        if len(args) < 2:
            return {"error": "task_id required"}
        task_id = args[1]
        branch = f"task/{task_id}"
        try:
            g._run(["checkout", g.current_branch()])
            # Check if already merged (#191)
            merged_branches = g._run(["branch", "--merged", "HEAD"], check=False).strip().splitlines()
            already_merged = any(branch in line.strip() for line in merged_branches)
            if already_merged:
                return {"subcommand": sub, "task_id": task_id, "merged": True, "already_merged": True}
            g._run(["merge", branch, "--no-ff", "-m", f"merge: {task_id}"])
            g.push()
            return {"subcommand": sub, "task_id": task_id, "merged": True}
        except GitError as e:
            return {"error": str(e)}

    if sub == "cleanup":
        if len(args) < 2:
            return {"error": "task_id required"}
        task_id = args[1]
        branch = f"task/{task_id}"
        try:
            wt.remove(task_id, force=True)
            try:
                g._run(["branch", "-D", branch], check=False)
            except GitError:
                pass
            return {"subcommand": sub, "task_id": task_id, "cleaned": True}
        except WorktreeError as e:
            return {"error": str(e)}

    return {"error": f"unknown worktree subcommand: {sub}"}


# ── nlp ──────────────────────────────────────────────────────────

def cmd_nlp(args: list[str]) -> dict:
    """Return available commands + raw input for LLM interpretation.

    No keyword matching — the orchestrator (Claude Code) uses its LLM
    to map natural language to the exact command from the list below.
    """
    text = " ".join(args)
    from kanban_framework.domain.nlp import extract_task_id, detect_work_intent
    work_intent = detect_work_intent(text)
    return {
        "input": text,
        "task_id": extract_task_id(text),
        "interpret_by_llm": True,
        "routing_guidance": {
            "intent": work_intent["intent"],
            "suggested_command": work_intent["suggested_command"],
            "has_task_id": work_intent["has_task_id"],
            "rule": (
                "If intent=knowledge → use 'knowledge add' or 'knowledge search' for knowledge management. "
                "If intent=work and has_task_id=false → use 'create' to create a task first, then 'run' it. "
                "If intent=work and has_task_id=true → use 'run' to continue the task. "
                "If intent=query → use 'status' or 'show'. "
                "NEVER execute work directly — always route through create+run. "
                "NEVER create a task for knowledge management operations (#313)."
            ),
        },
        "available_commands": [
            {"command": "init",                  "example": "/kanban init"},
            {"command": "create",                "example": '/kanban create "<title>" [--desc "<desc>"] [--auto-mode <brainstorm|iteration|lightweight|archive|all>]'},
            {"command": "status",                "example": "/kanban status"},
            {"command": "show",                  "example": "/kanban show <task_id>"},
            {"command": "run",                   "example": "/kanban run <task_id> [--phase <phase>]"},
            {"command": "decide",                "example": "/kanban decide <task_id> --action approve_and_archive|abort|restart_from_plan|restart_from_execute"},
            {"command": "score",                 "example": "/kanban score <task_id>"},
            {"command": "summary",               "example": "/kanban summary <task_id>"},
            {"command": "recover",               "example": "/kanban recover [<task_id>]"},
            {"command": "resume",                "example": "/kanban resume <task_id>"},
            {"command": "rollback",              "example": "/kanban rollback <task_id>"},
            {"command": "clean",                 "example": "/kanban clean [<task_id>|--all|--before <date>]"},
            {"command": "time",                  "example": "/kanban time [<task_id>]"},
            {"command": "tokens",                "example": "/kanban tokens <task_id>"},
            {"command": "progress",              "example": "/kanban progress <task_id>"},
            {"command": "subtask",               "example": "/kanban subtask start|done <task_id> <subtask_id>"},
            {"command": "dashboard",             "example": "/kanban dashboard [start|stop|status|restart]"},
            {"command": "version",               "example": "/kanban version list|record"},
            {"command": "knowledge",             "example": "/kanban knowledge search <keyword>"},
            {"command": "feedback",              "example": "/kanban feedback <task_id>"},
            {"command": "evolve-skills",         "example": "/kanban evolve-skills"},
            {"command": "check-env",             "example": "/kanban check-env"},
        ],
    }


# ── recover / rollback / resume ──────────────────────────────────

def cmd_recover(args: list[str]) -> dict:
    if args:
        task_id = args[0]
        if "--check-timeout" in args:
            result = recover_check_timeout(task_id)
            return {"task_id": task_id, "timeout": result}
        return {"task_id": task_id, "action": "recover"}
    return {"action": "recover", "interrupted_tasks": recover_list()}


def cmd_rollback(args: list[str]) -> dict:
    if not args:
        return {"error": "task_id required"}
    task_id = args[0]
    result = rollback_task(task_id)
    return {"task_id": task_id, "action": "rollback", "result": result}


def cmd_resume(args: list[str]) -> dict:
    if not args:
        return {"error": "task_id required"}
    task_id = args[0]
    result = resume_task(task_id)
    return {"task_id": task_id, "action": "resume", "result": result}
