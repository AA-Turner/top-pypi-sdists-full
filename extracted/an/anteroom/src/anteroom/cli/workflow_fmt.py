"""Shared workflow monitoring formatters.

Provides duration formatting, status icons, and timeline rendering
used by ``workflow watch``, ``workflow status``, and ``workflow history``.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any


def _no_color_enabled() -> bool:
    """Return whether ASCII-only rendering is enabled."""
    return bool(os.environ.get("NO_COLOR"))


# ---------------------------------------------------------------------------
# Duration formatting
# ---------------------------------------------------------------------------


def format_duration_ms(ms: int | None) -> str:
    """Format milliseconds as human-readable: '5m 12s', '1h 3m', '< 1s'."""
    if ms is None:
        return "—"
    seconds = ms / 1000
    return format_duration_s(seconds)


def format_duration_s(seconds: float | int | None) -> str:
    """Format seconds as human-readable: '5m 12s', '1h 3m', '< 1s'."""
    if seconds is None:
        return "—"
    seconds = int(seconds)
    if seconds < 1:
        return "< 1s"
    if seconds < 60:
        return f"{seconds}s"
    minutes, secs = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {secs}s" if secs else f"{minutes}m"
    hours, mins = divmod(minutes, 60)
    return f"{hours}h {mins}m" if mins else f"{hours}h"


def format_elapsed(started_at: str | None) -> str:
    """Live elapsed time from ISO timestamp to now."""
    if not started_at:
        return "—"
    try:
        start = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = (now - start).total_seconds()
        return format_duration_s(max(0, delta))
    except (ValueError, TypeError):
        return "—"


# ---------------------------------------------------------------------------
# Status icons and colors
# ---------------------------------------------------------------------------

STATUS_ICONS: dict[str, str] = {
    "completed": "✅",
    "success": "✅",
    "running": "●",
    "claimed": "●",
    "pending": "○",
    "failed": "❌",
    "blocked": "🚫",
    "paused": "⏸",
    "waiting_for_approval": "⏳",
    "waiting_for_input": "⏳",
    "cancelled": "⊘",
    "skipped": "⏭",
    "compensating": "↩",
    "compensated": "↩",
    "compensation_failed": "↩❌",
    "interrupted": "⚡",
}

_ASCII_ICONS: dict[str, str] = {
    "completed": "[OK]",
    "success": "[OK]",
    "running": "[..]",
    "claimed": "[..]",
    "pending": "[  ]",
    "failed": "[XX]",
    "blocked": "[!!]",
    "paused": "[||]",
    "waiting_for_approval": "[??]",
    "waiting_for_input": "[??]",
    "cancelled": "[--]",
    "skipped": "[>>]",
    "compensating": "[<-]",
    "compensated": "[<-]",
    "compensation_failed": "[<!]",
    "interrupted": "[!]",
}

STATUS_COLORS: dict[str, str] = {
    "completed": "green",
    "success": "green",
    "running": "cyan",
    "claimed": "cyan",
    "pending": "dim",
    "failed": "red",
    "blocked": "yellow",
    "paused": "yellow",
    "waiting_for_approval": "yellow",
    "waiting_for_input": "yellow",
    "cancelled": "dim",
    "skipped": "dim",
    "compensating": "magenta",
    "compensated": "magenta",
    "compensation_failed": "red",
    "interrupted": "red",
}


def status_icon(status: str) -> str:
    """Return a status icon, respecting NO_COLOR."""
    no_color = _no_color_enabled()
    icons = _ASCII_ICONS if no_color else STATUS_ICONS
    return icons.get(status, "?" if no_color else "·")


def status_color(status: str) -> str:
    """Return a Rich color string for a status value."""
    return STATUS_COLORS.get(status, "white")


# ---------------------------------------------------------------------------
# Timeline rendering
# ---------------------------------------------------------------------------


def render_step_line(step: dict[str, Any], *, indent: int = 0, id_width: int = 0) -> str:
    """One-line step summary for timeline view.

    *id_width* controls the column width for step IDs.  When 0 (default),
    the step ID is not padded — callers rendering a batch of steps should
    pre-compute the max width and pass it in for alignment.

    Returns a plain string (no Rich markup) for maximum compatibility.
    Callers can wrap in Rich markup using status_color() if desired.
    """
    result_status = step.get("result_status") or step.get("status", "pending")
    icon = status_icon(result_status)
    step_id = step.get("step_id", "?")
    dur = format_duration_ms(step.get("duration_ms"))
    runner = step.get("runner_type") or step.get("step_type", "")

    prefix = "  " * indent
    suffix = ""
    if result_status == "skipped":
        suffix = "  (skipped)"
    elif result_status == "failed" and (step.get("result_artifacts") or {}).get("continued"):
        suffix = "  (continued)"
    elif step.get("is_compensation"):
        suffix = "  (compensation)"

    if "/_fail/" in step_id:
        suffix = "  (failure handler)"

    artifacts = step.get("result_artifacts") or {}
    if artifacts.get("cache_hit"):
        suffix = "  (cached)"
    elif artifacts.get("fallback_used"):
        suffix = f"  (fallback: {artifacts.get('model', '?')})"

    loop_end = artifacts.get("loop_end_reason")
    if loop_end == "until_met":
        suffix = "  (until met)"
    elif loop_end == "until_not_met":
        suffix = "  (until not met)"
    elif loop_end == "break_when":
        suffix = "  (break condition)"
    elif loop_end == "exhausted":
        suffix = "  (exhausted)"

    outputs = step.get("result_outputs") or {}
    if outputs:
        suffix += f"  [{len(outputs)} output{'s' if len(outputs) != 1 else ''}]"

    # Pad step_id — account for indent so columns stay aligned
    effective_width = max(id_width - (indent * 2), len(step_id)) if id_width else len(step_id)
    padded_id = f"{step_id:<{effective_width}}"
    padded_dur = f"{dur:>7}" if dur != "—" else "       "

    return f"{prefix}{icon} {padded_id} {padded_dur}  {runner}{suffix}"


def compute_id_width(steps: list[dict[str, Any]], *, max_width: int = 32) -> int:
    """Compute the max step ID width across a list of steps for alignment.

    Capped at *max_width* to prevent overly wide output on narrow terminals.
    """
    if not steps:
        return 0
    return min(max(len(s.get("step_id", "")) for s in steps), max_width)


def render_run_header(run: dict[str, Any], *, step_count: int = 0, total_steps: int = 0) -> str:
    """Run header for watch/status.

    Example::

        local_claude_codex_issue_delivery  ● running  5m 12s
        Run: 20b3119a  Steps: 3/8
    """
    workflow_id = run.get("workflow_id", "?")
    status = run.get("status", "unknown")
    icon = status_icon(status)

    if status == "running" and run.get("started_at"):
        elapsed = format_elapsed(run["started_at"])
    elif run.get("completed_at") and run.get("started_at"):
        try:
            start = datetime.fromisoformat(run["started_at"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(run["completed_at"].replace("Z", "+00:00"))
            elapsed = format_duration_s((end - start).total_seconds())
        except (ValueError, TypeError):
            elapsed = "—"
    else:
        elapsed = "—"

    run_id_short = run.get("id", "?")[:8]
    step_info = f"Steps: {step_count}/{total_steps}" if total_steps else ""

    line1 = f"{workflow_id}  {icon} {status}  {elapsed}"
    line2 = f"Run: {run_id_short}  {step_info}".rstrip()
    return f"{line1}\n{line2}"


# ---------------------------------------------------------------------------
# Diagnosis rendering (#1103)
# ---------------------------------------------------------------------------


def render_diagnosis(diagnosis: Any) -> str:
    """Render a Diagnosis as a Rich-compatible panel string.

    Returns plain text lines; the caller wraps in Rich Panel/markup.
    """
    confidence_icons = {"high": "●", "medium": "◐", "low": "○"}
    conf_icon = confidence_icons.get(diagnosis.confidence, "?")

    lines = []
    lines.append("  ❌ What happened")
    lines.append(f"  {diagnosis.what}")
    lines.append("")
    lines.append("  💡 Why")
    lines.append(f"  {diagnosis.why}")
    lines.append("")

    if diagnosis.evidence:
        lines.append("  📋 Evidence")
        for ev in diagnosis.evidence:
            label = _diagnosis_evidence_label(ev.source)
            if ev.location:
                label = f"{label} ({ev.location})"
            lines.extend(_render_diagnosis_block(f"  • {label}: ", ev.content))
        lines.append("")

    if diagnosis.next_actions:
        lines.append("  👉 Next actions")
        for i, action in enumerate(diagnosis.next_actions, 1):
            lines.append(f"  {i}. {action}")
        lines.append("")

    lines.append(f"  Confidence: {conf_icon} {diagnosis.confidence}")
    return "\n".join(lines)


def _diagnosis_evidence_label(source: str) -> str:
    """Return a readable label for diagnosis evidence sources."""
    labels = {
        "stop_reason": "stop_reason",
        "step_summary": "step output",
        "step_findings": "step finding",
        "command": "command",
        "command_output": "command output",
        "exception": "exception",
        "traceback_frame": "frame",
        "raw_output": "raw output",
        "budget": "budget",
    }
    return labels.get(source, source.replace("_", " "))


def _render_diagnosis_block(prefix: str, content: str, *, max_lines: int = 4) -> list[str]:
    """Render multi-line diagnosis content with indentation and clipping."""
    lines = [line.rstrip() for line in content.splitlines() if line.strip()]
    if not lines:
        return [prefix.rstrip()]

    rendered = [f"{prefix}{lines[0]}"]
    for line in lines[1:max_lines]:
        rendered.append(f"{' ' * len(prefix)}{line}")
    if len(lines) > max_lines:
        rendered.append(f"{' ' * len(prefix)}...")
    return rendered
