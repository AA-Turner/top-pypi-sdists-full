"""
Session hook — inject active kanban task context into the model's view.

Registered as a SessionStart hook in .claude/settings.json so the model
always knows the current task state when a conversation starts.
"""

from __future__ import annotations
import json
from pathlib import Path
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.task import TaskManager
from kanban_framework.infra.config import Config
from kanban_framework.infra.consts import Consts


def cmd_hook(args: list[str]) -> dict:
    sub = args[0] if args else "context"

    if sub == "context":
        return _session_context()

    if sub == "install":
        return _install_hook()

    return {"error": f"unknown hook subcommand: {sub}"}


def _install_hook() -> dict:
    """Register kanban session hook in .claude/settings.json."""
    import json as _json
    root = Filesystem.find_project_root()
    settings_dir = root / ".claude"
    settings_path = settings_dir / "settings.json"
    settings_dir.mkdir(parents=True, exist_ok=True)

    settings = {}
    if settings_path.is_file():
        try:
            settings = _json.loads(settings_path.read_text(encoding="utf-8"))
        except _json.JSONDecodeError:
            settings = {}

    hooks = settings.setdefault("hooks", {})
    session_hooks = hooks.setdefault("SessionStart", [])

    # Check if already installed
    for h in session_hooks:
        if "kanban_framework hook context" in h.get("command", ""):
            return {"installed": False, "reason": "already configured"}

    session_hooks.append({
        "matcher": "",
        "command": "kanban hook context 2>/dev/null || python3 -m kanban_framework hook context 2>/dev/null || python -m kanban_framework hook context 2>/dev/null || echo '{\"kanban_active\":false}'"
    })

    settings_path.write_text(_json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"installed": True, "file": str(settings_path)}


def _session_context() -> dict:
    """Generate session-start context about active kanban tasks."""
    try:
        root = Filesystem.find_project_root()
        fs = Filesystem(root=root)
    except Exception:
        return {"kanban_active": False}

    kanban_dir = fs.kanban_dir
    if not kanban_dir.is_dir():
        return {"kanban_active": False}

    # Check for active tasks
    cfg = Config(fs)
    tm = TaskManager(fs, cfg)
    active_tasks = []
    try:
        tasks_dir = kanban_dir / "tasks"
        if tasks_dir.is_dir():
            for d in sorted(tasks_dir.iterdir()):
                if not d.is_dir():
                    continue
                task_json = d / "task.json"
                if not task_json.is_file():
                    continue
                data = json.loads(task_json.read_text(encoding="utf-8"))
                status = data.get("status", "")
                phase = data.get("phase", "")
                if status not in ("archived", "cancelled") and phase:
                    # Get next step
                    from kanban_framework.domain.state_machine import next_step, next_step_to_dict
                    try:
                        task = tm.show(data["id"])
                        ns = next_step(fs, cfg, task)
                        step_info = next_step_to_dict(ns)
                    except Exception:
                        step_info = None

                    # Check inbox
                    inbox_pending = 0
                    inbox_path = d / "inbox.md"
                    if inbox_path.is_file():
                        for line in inbox_path.read_text(encoding="utf-8").splitlines():
                            s = line.strip()
                            if s.startswith("- [ ]"):
                                inbox_pending += 1

                    # Check blocking subtasks
                    blocking_incomplete = 0
                    breakdown_path = d / "task_breakdown.json"
                    if breakdown_path.is_file():
                        bd = json.loads(breakdown_path.read_text(encoding="utf-8"))
                        for st in bd.get("subtasks", []):
                            if st.get("blocking") and st.get("status", "pending") != "completed":
                                blocking_incomplete += 1

                    active_tasks.append({
                        "id": data["id"],
                        "title": data.get("title", ""),
                        "phase": phase,
                        "status": status,
                        "iteration": data.get("iteration", 1),
                        "mode": data.get("mode", Consts.DEFAULT_MODE),
                        "auto_mode": data.get("auto_mode", {}),
                        "next_step": step_info.get("description") if step_info else None,
                        "next_step_id": step_info.get("step_id") if step_info else None,
                        "user_action_needed": step_info.get("user_action", False) if step_info else False,
                        "inbox_pending": inbox_pending,
                        "blocking_subtasks": blocking_incomplete,
                    })

    except Exception:
        pass

    if not active_tasks:
        return {"kanban_active": False, "message": "No active kanban tasks."}

    return {
        "kanban_active": True,
        "active_tasks": active_tasks,
        "task_count": len(active_tasks),
        "summary": _format_summary(active_tasks),
    }


def _format_summary(tasks: list[dict]) -> str:
    """Produce a human-readable summary for context injection."""
    lines = ["[KANBAN SESSION CONTEXT]"]
    for t in tasks:
        mode = t.get("mode", Consts.DEFAULT_MODE)
        auto = "auto" if any(t.get("auto_mode", {}).values()) else "manual"
        lines.append(
            f"  {t['id']}: {t['title'][:50]} "
            f"[{t['phase']} | iter {t['iteration']} | {mode} | {auto}]"
        )
        if t.get("next_step"):
            lines.append(f"    Next: {t['next_step']}")
        if t.get("user_action_needed"):
            lines.append(f"    ⚠ User action required — ask user before proceeding")
        if t.get("inbox_pending"):
            lines.append(f"    Inbox: {t['inbox_pending']} pending items")
        if t.get("blocking_subtasks"):
            lines.append(f"    Blocking subtasks: {t['blocking_subtasks']} incomplete")
    lines.append("  → Use kanban workflow next-step <id> for authoritative FSM instruction")
    return "\n".join(lines)
