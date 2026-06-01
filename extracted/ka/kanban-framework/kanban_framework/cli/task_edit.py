"""Task editing commands — mode, priority, auto-mode, skip-to."""
from __future__ import annotations

import argparse
import time

from kanban_framework.cli.task_utils import _resolve
from kanban_framework.infra.scheduler import Scheduler
from kanban_framework.types import Phase


def _sync_phase_for_mode(current_phase: str, target_mode: str) -> str | None:
    """Find the nearest valid phase when switching to lightweight/quick mode.

    If current phase is in the target mode's phase order, return None (no change).
    Otherwise, find the closest phase that exists in the target order.
    """
    if target_mode == "quick":
        target_order = [p.value for p in Scheduler.QUICK_PHASE_ORDER]
    elif target_mode == "lightweight":
        target_order = [p.value for p in Scheduler.LIGHTWEIGHT_PHASE_ORDER]
    else:
        return None

    if current_phase in target_order:
        return None

    # Map current phase to nearest valid phase in target order
    _FULL_ORDER = [p.value for p in Scheduler.PHASE_ORDER]
    try:
        current_idx = _FULL_ORDER.index(current_phase)
    except ValueError:
        # Custom phase: fall back to first phase of target order
        return target_order[0]

    # Find the latest target phase whose full-order index <= current
    best = target_order[0]
    for tp in target_order:
        try:
            tp_idx = _FULL_ORDER.index(tp)
        except ValueError:
            continue
        if tp_idx <= current_idx:
            best = tp
    return best


_SKIP_TO_REQUIRED_ARTIFACTS = {
    "execute": [
        ("spec.md", "需求文档"),
        ("task_breakdown.json", "任务拆解"),
        ("plan/index.md", "Plan 索引"),
    ],
    "evaluate": [
        ("spec.md", "需求文档"),
        ("task_breakdown.json", "任务拆解"),
        ("plan/index.md", "Plan 索引"),
        ("execution_summary.md", "执行总结"),
    ],
}


def cmd_task(args: list[str]) -> dict:
    """Dispatch: kanban task <subcommand>"""
    if not args:
        return {"error": "subcommand required: edit"}
    sub = args[0]
    if sub == "edit":
        return _cmd_task_edit(args[1:])
    return {"error": f"unknown task subcommand: {sub}"}


def _handle_skip_to(task_id: str, target: str, task) -> dict:
    """Validate artifacts, mark skipped steps, and record history for --skip-to."""
    fs, _, tm = _resolve()
    from kanban_framework.domain.step_progress import load_progress, save_progress
    from kanban_framework.domain.steps import _get_steps

    task_dir = fs.task_dir(task_id)
    missing = []
    for filename, label in _SKIP_TO_REQUIRED_ARTIFACTS.get(target, []):
        candidates = [task_dir / filename]
        iter_dir = task_dir / f"iteration-{task.iteration}"
        candidates.append(iter_dir / filename)
        candidates.append(iter_dir / "execute" / filename)
        if not any(c.is_file() and c.stat().st_size > 0 for c in candidates):
            missing.append(f"{filename} ({label})")

    if missing:
        return {"error": f"无法跳到 {target} 阶段，缺少必要产物: {', '.join(missing)}。请先手动创建这些文件。"}

    progress = load_progress(fs, task_id)
    steps_map = _get_steps("quick" if getattr(task, 'mode', '') == "quick"
                           else ("lightweight" if task.lightweight else "full"))
    from kanban_framework.types import Phase
    from kanban_framework.infra.scheduler import Scheduler
    quick = getattr(task, 'mode', '') == "quick"
    mode_order = Scheduler.dispatch_order(lightweight=task.lightweight, quick=quick)
    phases_to_skip = []
    for p in mode_order:
        if p.value == target:
            break
        phases_to_skip.append(p.value)

    for phase_name in phases_to_skip:
        for step in steps_map.get(phase_name, []):
            if step.id not in progress["steps"]:
                progress["steps"][step.id] = {"status": "skipped", "updated_at": time.time()}
    save_progress(fs, task_id, progress)

    now = time.time()
    history = list(task.history)
    for phase_name in phases_to_skip:
        already = any(
            h.get("phase") == phase_name and h.get("status") == "completed"
            for h in history
        )
        if not already:
            history.append({
                "phase": phase_name,
                "status": "completed",
                "completed_at": now,
                "iteration": task.iteration,
                "note": "skipped via --skip-to",
            })
    tm.update(task_id, history=history)

    return {
        "target_phase": target,
        "skipped_phases": phases_to_skip,
        "validated_artifacts": [f[0] for f in _SKIP_TO_REQUIRED_ARTIFACTS[target]],
    }


def _cmd_task_edit(args: list[str]) -> dict:
    parser = argparse.ArgumentParser(prog="kanban task edit", add_help=False)
    parser.add_argument("task_id")
    parser.add_argument("--mode", type=str, default=None, help="Task mode: full, lightweight, quick, custom, or any custom mode from workflow.json")
    parser.add_argument("--lightweight", action="store_true", default=False)
    parser.add_argument("--priority", type=int, default=None)
    parser.add_argument("--auto-mode", type=str, default=None,
                        help="Auto-mode flags: all, brainstorm, iteration, lightweight, archive, worktree (comma-separated), or 'none' to disable all")
    parser.add_argument("--control-mode", type=str, default=None, choices=["auto", "semi", "manual"],
                        help="Control mode: auto (full auto), semi (default, user confirms at gates), manual (user drives each step)")
    parser.add_argument("--skip-to", type=str, default=None, dest="skip_to",
                        choices=["execute", "evaluate"],
                        help="Skip plan phases and jump to a later phase. Requires plan artifacts to exist.")
    try:
        parsed = parser.parse_args(args)
    except SystemExit:
        return {"error": "invalid arguments, usage: kanban task edit <task_id> [--mode ...] [--skip-to execute|evaluate] [--priority N] [--auto-mode ...] [--control-mode ...]"}

    _, _, tm = _resolve()
    task = tm.show(parsed.task_id)

    updates: dict = {}
    mode = parsed.mode
    if parsed.lightweight:
        mode = "lightweight"
        updates["lightweight"] = True
    if mode:
        updates["mode"] = mode
        if mode in ("lightweight", "quick"):
            updates["lightweight"] = True
            synced = _sync_phase_for_mode(task.phase_id, mode)
            if synced is not None:
                updates["phase"] = synced
        elif mode == "full":
            updates["lightweight"] = False
    if parsed.priority is not None:
        updates["priority"] = max(0, min(10, parsed.priority))
    if parsed.control_mode:
        updates["control_mode"] = parsed.control_mode

    if parsed.auto_mode is not None:
        from kanban_framework.types import AutoMode
        flags = [f.strip().lower() for f in parsed.auto_mode.split(",")]
        if "all" in flags:
            updates["auto_mode"] = AutoMode(
                auto_brainstorm=True, auto_iteration=True,
                auto_lightweight=True, auto_archive=True, auto_worktree=True,
            )
        elif "none" in flags:
            updates["auto_mode"] = AutoMode()
        else:
            am = task.auto_mode
            for f in flags:
                if f == "brainstorm":
                    am.auto_brainstorm = True
                elif f == "iteration":
                    am.auto_iteration = True
                elif f == "lightweight":
                    am.auto_lightweight = True
                elif f == "archive":
                    am.auto_archive = True
                elif f == "worktree":
                    am.auto_worktree = True
            updates["auto_mode"] = am

    if not updates and not parsed.skip_to:
        return {"error": "no changes specified (--mode, --lightweight, --priority, --auto-mode, --control-mode, --skip-to)"}

    skip_info = None
    if parsed.skip_to:
        skip_info = _handle_skip_to(parsed.task_id, parsed.skip_to, task)
        if "error" in skip_info:
            return skip_info
        updates["phase"] = skip_info["target_phase"]

    if updates:
        tm.update(parsed.task_id, **updates)
    result = {
        "task_id": parsed.task_id,
        "updated": list(updates.keys()),
        "mode": mode or task.mode,
        "lightweight": updates.get("lightweight", task.lightweight),
        "control_mode": updates.get("control_mode", task.control_mode.value if task.control_mode else "semi"),
        "message": f"Task {parsed.task_id} updated",
    }
    if "auto_mode" in updates:
        am = updates["auto_mode"]
        result["auto_mode"] = {
            "auto_brainstorm": am.auto_brainstorm,
            "auto_iteration": am.auto_iteration,
            "auto_lightweight": am.auto_lightweight,
            "auto_archive": am.auto_archive,
            "auto_worktree": am.auto_worktree,
        }
    if skip_info:
        result["skip_to"] = skip_info
        result["message"] = (f"Task {parsed.task_id} 跳到 {skip_info['target_phase']} 阶段。"
                             f"已跳过: {', '.join(skip_info['skipped_phases'])}")
    return result
