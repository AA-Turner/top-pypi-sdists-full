"""Auto-mode issue capture — records framework errors as task issue files.

Only active when task.control_mode == ControlMode.AUTO.
Writes structured .md issue files to .kanban/tasks/TASK-NNN/issues/.
"""
from __future__ import annotations
import json
import time
import traceback
from pathlib import Path
from kanban_framework.infra.consts import Consts


def _is_auto_mode(task) -> bool:
    """Check if the task is running in full-auto mode."""
    try:
        if hasattr(task, "control_mode"):
            from kanban_framework.types import ControlMode
            return task.control_mode == ControlMode.AUTO
    except Exception:
        pass
    return False


def _task_issues_dir(fs, task_id: str) -> Path:
    d = fs.kanban_dir / "tasks" / task_id / "issues"
    d.mkdir(parents=True, exist_ok=True)
    return d


def capture_issue(fs, task, error: Exception, context: dict | None = None) -> Path | None:
    """Capture a framework error as an issue file under the task directory.

    Returns the path to the created file, or None if auto mode is not active.
    """
    if not _is_auto_mode(task):
        return None

    ts = time.strftime("%Y%m%d-%H%M%S")
    filename = f"issue-{ts}.md"
    filepath = _task_issues_dir(fs, task.id) / filename

    ctx = context or {}
    tb_str = "".join(traceback.format_exception(type(error), error, error.__traceback__))

    lines = [
        f"# Auto-Captured Issue: {type(error).__name__}",
        "",
        f"- **Task**: {task.id}",
        f"- **Phase**: {task.phase.value if hasattr(task.phase, 'value') else str(task.phase)}",
        f"- **Iteration**: {task.iteration}",
        f"- **Mode**: {getattr(task, 'mode', '') or Consts.DEFAULT_MODE}",
        f"- **Time**: {ts}",
    ]
    if ctx:
        lines.append("")
        lines.append("## Context")
        for k, v in sorted(ctx.items()):
            lines.append(f"- **{k}**: {v}")

    lines.extend([
        "",
        "## Error",
        f"**Type**: `{type(error).__name__}`",
        f"**Message**: {error}",
        "",
        "```",
        tb_str.strip(),
        "```",
    ])

    filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return filepath


def capture_warning(fs, task, message: str, category: str = "") -> Path | None:
    """Capture a non-fatal warning as an issue file.

    Useful for recording optimization suggestions, deprecation notices, etc.
    """
    if not _is_auto_mode(task):
        return None

    ts = time.strftime("%Y%m%d-%H%M%S")
    filename = f"issue-{ts}.md"
    filepath = _task_issues_dir(fs, task.id) / filename

    lines = [
        f"# Auto-Captured Warning{f': {category}' if category else ''}",
        "",
        f"- **Task**: {task.id}",
        f"- **Phase**: {task.phase.value if hasattr(task.phase, 'value') else str(task.phase)}",
        f"- **Time**: {ts}",
        "",
        message,
    ]
    filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return filepath
