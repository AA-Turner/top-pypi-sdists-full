from __future__ import annotations
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.domain.task import TaskManager
from kanban_framework.domain.guard import Guard, CheckResult
from kanban_framework.types import Phase
from kanban_framework.cli.run_helpers import _resolve


_GUARD_SUBCOMMANDS = [
    "check-artifacts", "check-evaluation", "check-plan-quality",
    "check-inbox", "check-spec", "check-parallel-conflicts",
    "check-cross-task-conflicts", "check-phase-completeness",
    "batch-check", "check-archive-stray", "check-pending-subtasks",
]

def cmd_guard(args: list[str]) -> dict:
    if not args:
        return {"error": "subcommand required", "available": _GUARD_SUBCOMMANDS}
    sub = args[0]
    fs, cfg, tm, _ = _resolve()
    guard = Guard(fs, cfg)

    if sub == "check-artifacts":
        if len(args) < 2:
            return {"error": "task_id required"}
        task = tm.show(args[1])
        phase = Phase(args[2]) if len(args) > 2 else task.phase
        result = guard.check_artifacts(task, phase, lightweight=task.lightweight)
        return {
            "subcommand": sub,
            "task_id": task.id,
            "phase": phase.value,
            "passed": result.passed,
            "failures": result.failures,
            "warnings": result.warnings,
        }

    if sub == "check-evaluation":
        if len(args) < 2:
            return {"error": "task_id required"}
        task = tm.show(args[1])
        iteration = int(args[2]) if len(args) > 2 else task.iteration
        result = guard.check_evaluation(task, iteration, lightweight=task.lightweight)
        return {
            "subcommand": sub,
            "task_id": task.id,
            "iteration": iteration,
            "passed": result.passed,
            "failures": result.failures,
        }

    if sub == "check-plan-quality":
        if len(args) < 2:
            return {"error": "task_id required"}
        task = tm.show(args[1])
        report_dir = fs.report_dir(task.id, task.iteration)
        result = guard.check_plan_quality(task, report_dir)
        return {
            "subcommand": sub,
            "task_id": task.id,
            "passed": result.passed,
            "failures": result.failures,
        }

    if sub == "check-inbox":
        if len(args) < 2:
            return {"error": "task_id required"}
        task = tm.show(args[1])
        inbox_path = fs.task_dir(task.id) / "inbox.md"
        pending = []
        unverified = []  # checked [x] but no verification tag
        if fs.file_exists(inbox_path):
            content = inbox_path.read_text(encoding="utf-8")
            import re
            _tag_done = re.compile(r'done:(\S+)')
            _tag_migrated = re.compile(r'migrated:(\S+)')
            _tag_wontfix = re.compile(r'wontfix:(.+?)(?:-->|$)')
            for line in content.split("\n"):
                stripped = line.strip()
                # Layer 1: unchecked / natural-language items
                if (stripped and
                    not stripped.startswith("#") and
                    not stripped.startswith("<!--") and
                    not stripped.startswith("---") and
                    not stripped.startswith("**") and
                    not stripped.startswith("- [x]") and
                    not stripped.startswith("* [x]")):
                    pending.append(stripped)
                # Layer 2: checked but no verification tag
                if stripped.startswith("- [x]") or stripped.startswith("* [x]"):
                    has_tag = bool(_tag_done.search(stripped) or
                                   _tag_migrated.search(stripped) or
                                   _tag_wontfix.search(stripped))
                    if not has_tag:
                        unverified.append(stripped)
        can_archive = len(pending) == 0 and len(unverified) == 0
        return {
            "subcommand": sub,
            "task_id": task.id,
            "has_pending": len(pending) > 0,
            "pending_count": len(pending),
            "pending": pending,
            "has_unverified": len(unverified) > 0,
            "unverified_count": len(unverified),
            "unverified": unverified,
            "can_archive": can_archive,
        }

    if sub == "check-spec":
        if len(args) < 2:
            return {"error": "task_id required"}
        task = tm.show(args[1])
        result = guard.check_spec(task, fs.report_dir(task.id, task.iteration))
        return {
            "subcommand": sub,
            "task_id": task.id,
            "passed": result.passed,
            "failures": result.failures,
        }

    if sub == "check-parallel-conflicts":
        if len(args) < 2:
            return {"error": "task_id required"}
        task = tm.show(args[1])
        result = guard.check_parallel_conflicts(task)
        return {
            "subcommand": sub,
            "task_id": task.id,
            "passed": result.passed,
            "failures": result.failures,
        }

    if sub == "check-cross-task-conflicts":
        result = guard.check_cross_task_conflicts()
        return {
            "subcommand": sub,
            "passed": result.passed,
            "failures": result.failures,
            "warnings": result.warnings,
        }

    if sub == "check-phase-completeness":
        if len(args) < 2:
            return {"error": "task_id required"}
        task = tm.show(args[1])
        result = guard.check_phase_completeness(task, lightweight=task.lightweight)
        return {
            "subcommand": sub,
            "task_id": task.id,
            "current_phase": task.phase.value,
            "passed": result.passed,
            "failures": result.failures,
        }

    if sub == "batch-check":
        if len(args) < 2:
            return {"error": "task_id required"}
        task = tm.show(args[1])
        report_dir = fs.report_dir(task.id, task.iteration)
        result = guard.batch_check_combined(task, report_dir)
        return {
            "subcommand": sub,
            "task_id": task.id,
            "passed": result.passed,
            "failures": result.failures,
            "warnings": result.warnings,
        }

    if sub == "check-archive-stray":
        if len(args) < 2:
            return {"error": "task_id required"}
        task = tm.show(args[1])
        project_root = Filesystem.find_project_root()
        stray_archive = project_root / "archive"
        stray_task = stray_archive / task.id
        if stray_task.is_dir():
            # Stray archive found in project root — clean it up
            import shutil
            shutil.rmtree(stray_task)
            # If stray archive is now empty, remove it too
            if stray_archive.is_dir() and not list(stray_archive.iterdir()):
                stray_archive.rmdir()
            return {
                "subcommand": sub,
                "task_id": task.id,
                "stray_found": True,
                "cleaned": str(stray_task),
                "message": "Stray archive/ directory in project root cleaned up. Use .kanban/archive/ instead.",
            }
        return {
            "subcommand": sub,
            "task_id": task.id,
            "stray_found": False,
        }

    if sub == "check-pending-subtasks":
        if len(args) < 2:
            return {"error": "task_id required"}
        task = tm.show(args[1])
        import json as _json
        breakdown_path = fs.task_dir(task.id) / "task_breakdown.json"
        blocking_incomplete = []
        if fs.file_exists(breakdown_path):
            breakdown = _json.loads(breakdown_path.read_text(encoding="utf-8"))
            for st in breakdown.get("subtasks", []):
                if st.get("blocking") and st.get("status", "pending") != "completed":
                    blocking_incomplete.append({
                        "id": st.get("id", ""),
                        "title": st.get("title", ""),
                        "status": st.get("status", "pending"),
                        "needs_coordination": st.get("needs_coordination"),
                    })
        return {
            "subcommand": sub,
            "task_id": task.id,
            "has_blocking_incomplete": len(blocking_incomplete) > 0,
            "blocking_incomplete": blocking_incomplete,
            "count": len(blocking_incomplete),
            "can_archive": len(blocking_incomplete) == 0,
        }

    return {"error": f"unknown guard subcommand: {sub}", "available": _GUARD_SUBCOMMANDS}
