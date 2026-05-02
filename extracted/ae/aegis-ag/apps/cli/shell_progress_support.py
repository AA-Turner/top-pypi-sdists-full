"""Support types and small helpers for shell progress rendering."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
import os
import re
import threading
import time
from typing import TYPE_CHECKING

from packages.kernel.runtime import KernelOutcome
from packages.tools import ToolLifecycleEvent

from .shell_stack import (
    Application,
    Condition,
    ConditionalContainer,
    FormattedText,
    FormattedTextControl,
    Group,
    Layout,
    Live,
    Panel,
    RICH_AVAILABLE,
    Text,
    Window,
)
from .shell_ui import (
    BRAND_ACCENT,
    BRAND_ACCENT_STRONG,
    BRAND_DARK,
    BRAND_LIGHT,
    BRAND_MUTED,
    LIVE_DIFF_ADD_FG,
    LIVE_DIFF_CONTEXT_FG,
    LIVE_DIFF_FILE_FG,
    LIVE_DIFF_HUNK_FG,
    LIVE_DIFF_REMOVE_FG,
    QUEUE_PREVIEW_INSET,
    compact_line,
    strip_markdown_bold,
)

if TYPE_CHECKING:
    from .shell import ProductizedShell


_STREAM_TOOL_BLOCK_PATTERNS = (
    re.compile(
        r"<(?:[\w.-]+:)?tool_call\b[^>]*>.*?</(?:[\w.-]+:)?tool_call\s*>",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"<(?:[\w.-]+:)?invoke\b[^>]*>.*?</(?:[\w.-]+:)?invoke\s*>",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"<(?:[\w.-]+:)?parameter\b[^>]*>.*?</(?:[\w.-]+:)?parameter\s*>",
        re.IGNORECASE | re.DOTALL,
    ),
)
_STREAM_TOOL_TAG_PATTERN = re.compile(
    r"</?(?:[\w.-]+:)?(?:tool_call|invoke|parameter)\b[^>]*>",
    re.IGNORECASE,
)
_STREAM_OPEN_TOOL_TAG_PATTERN = re.compile(
    r"<(?:[\w.-]+:)?(?:tool_call|invoke|parameter)\b[^>]*>",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class _ToolTraceDisplayParts:
    rail: str
    emoji: str
    prefix: str
    label: str
    gap: str
    body: str
    duration_gap: str
    duration: str

@dataclass(frozen=True, slots=True)
class _VisibleToolEvent:
    event: ToolLifecycleEvent
    expires_at: float


@dataclass(frozen=True, slots=True)
class _KernelStageView:
    stage: str
    detail: str
    recorded_at: datetime | None

_TURN_TITLE_FRAMES: tuple[tuple[str, str], ...] = (
    ("✦", "Aegis is learning"),
    ("✦", "Aegis is weaving"),
    ("✦", "Aegis is watching"),
)

_TURN_MARKER_FRAMES: tuple[str, ...] = ("✦", "✧", "⋆", "·")
_CONTEXT_COMPACTION_MIN_VISIBLE_SECONDS = 1.5


def animations_enabled() -> bool:
    return RICH_AVAILABLE and Live is not None and os.environ.get("AEGIS_NO_ANIMATION") != "1"

def turn_title(tick: int) -> tuple[str, str]:
    return _TURN_TITLE_FRAMES[(tick // 4) % len(_TURN_TITLE_FRAMES)]

def turn_marker(tick: int) -> str:
    return _TURN_MARKER_FRAMES[tick % len(_TURN_MARKER_FRAMES)]

def turn_phase(tick: int) -> tuple[str, str, str]:
    phases = (
        ("unseal.clone", "Unsealing the active clone and its durable memory"),
        ("ward.identity", "Keeping the Aegis sigil aligned"),
        ("inscribe.reply", "Aegis is inscribing the reply"),
    )
    phase_label, phase_detail = phases[(tick // 3) % len(phases)]
    marker = turn_marker(tick)
    return marker, phase_label, phase_detail


def _parse_kernel_stage_detail(detail: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for token in str(detail).split():
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        normalized_key = key.strip().lower()
        if normalized_key:
            parsed[normalized_key] = value.strip()
    return parsed


def _kernel_stage_views(kernel_stage_events: tuple[Mapping[str, object], ...]) -> tuple[_KernelStageView, ...]:
    views: list[_KernelStageView] = []
    for event in kernel_stage_events:
        payload = event.get("payload")
        if not isinstance(payload, Mapping):
            continue
        stage = str(payload.get("stage") or "").strip()
        if not stage:
            continue
        recorded_at_value = str(payload.get("recorded_at") or "").strip()
        recorded_at = None
        if recorded_at_value:
            try:
                recorded_at = datetime.fromisoformat(recorded_at_value)
            except ValueError:
                recorded_at = None
        views.append(
            _KernelStageView(
                stage=stage,
                detail=str(payload.get("detail") or "").strip(),
                recorded_at=recorded_at,
            )
        )
    return tuple(views)


def _format_intent_scope(scope: str, *, compact: bool) -> str:
    normalized = str(scope or "").strip().lower()
    if not compact:
        return normalized
    return {
        "session": "sess",
        "workspace": "ws",
        "profile": "prof",
        "lineage": "lin",
    }.get(normalized, normalized)


def _intent_stage_summary_parts(
    kernel_stage_events: tuple[Mapping[str, object], ...],
    *,
    compact: bool = False,
) -> tuple[str, ...]:
    views = _kernel_stage_views(kernel_stage_events)
    target_index = next((index for index, view in enumerate(views) if view.stage == "intent"), None)
    if target_index is None:
        return ()
    target = views[target_index]
    detail = _parse_kernel_stage_detail(target.detail)
    parts = [detail.get("intent") or "unknown"]
    previous = views[target_index - 1] if target_index > 0 else None
    if previous is not None and previous.recorded_at is not None and target.recorded_at is not None:
        duration_ms = max(0, round((target.recorded_at - previous.recorded_at).total_seconds() * 1000))
        parts.append(f"{duration_ms}ms")
    scope = detail.get("scope")
    if scope and scope != "<none>":
        parts.append(_format_intent_scope(scope, compact=compact))
    confidence = detail.get("confidence")
    if confidence:
        parts.append(str(confidence) if compact else f"conf {confidence}")
    degradation = detail.get("degradation")
    if degradation and degradation not in {"none", "<none>"}:
        parts.append(degradation)
    return tuple(parts)


def turn_intent_progress_line(
    *,
    kernel_stage_events: tuple[Mapping[str, object], ...] = (),
) -> str:
    parts = _intent_stage_summary_parts(kernel_stage_events)
    body = "resolving…" if not parts else " · ".join(parts)
    return f"┊ 🧠 intent       {body}"


def turn_context_progress_line(
    *,
    kernel_stage_events: tuple[Mapping[str, object], ...] = (),
    now: datetime | None = None,
) -> str:
    views = _kernel_stage_views(kernel_stage_events)
    if not views:
        return "┊ 🧩 context      assembling"
    latest_context_view = next(
        (view for view in reversed(views) if view.stage in {"context-compact", "context"}),
        None,
    )
    if latest_context_view is None:
        return "┊ 🧩 context      assembling"
    compact_view = next((view for view in reversed(views) if view.stage == "context-compact"), None)
    if compact_view is not None and latest_context_view.stage == "context":
        if compact_view.recorded_at is not None and latest_context_view.recorded_at is not None:
            current = now or datetime.now(tz=compact_view.recorded_at.tzinfo)
            elapsed = (current - compact_view.recorded_at).total_seconds()
            if 0 <= elapsed <= _CONTEXT_COMPACTION_MIN_VISIBLE_SECONDS:
                latest_context_view = compact_view
        elif tuple(view.stage for view in views[-3:]).count("context-compact"):
            latest_context_view = compact_view
    detail = _parse_kernel_stage_detail(latest_context_view.detail)
    if latest_context_view.stage == "context-compact":
        tokens = detail.get("tokens")
        lines = detail.get("lines")
        reason = detail.get("reason")
        parts = ["compressing projection"]
        if tokens:
            parts.append(tokens)
        if lines:
            parts.append(f"{lines} lines")
        if reason:
            parts.append(reason)
        return f"┊ 🗜 context      {' · '.join(parts)}"
    budget = detail.get("budget")
    body = f"ready · budget {budget}" if budget else "ready"
    return f"┊ 🧩 context      {body}"


def outcome_intent_meta(outcome: KernelOutcome) -> str:
    stage_events = tuple(
        {
            "payload": {
                "stage": stage.stage,
                "detail": stage.detail,
                "recorded_at": stage.recorded_at.isoformat(),
            }
        }
        for stage in outcome.stages
    )
    parts = _intent_stage_summary_parts(stage_events, compact=True)
    if not parts:
        return ""
    return f"intent · {' · '.join(parts)}"

def summarize_progress_prompt(prompt: str) -> str:
    normalized = " ".join(prompt.split())
    if len(normalized) <= 72:
        return normalized
    return f"{normalized[:69]}..."

def pending_tooltrace_lines(shell: ProductizedShell) -> tuple[str, ...]:
    pending = shell.transcript[shell._rendered_entries :]
    lines: list[str] = []
    for entry in pending:
        if entry.kind != "tooltrace":
            continue
        body_lines = entry.body.splitlines() or [entry.body]
        for body_line in body_lines:
            normalized = strip_markdown_bold(body_line).rstrip("\n")
            if not normalized or not normalized.startswith("┊ "):
                continue
            lines.append(normalized)
    return tuple(lines)

def pending_tool_output_lines(shell: ProductizedShell) -> tuple[str, ...]:
    pending = shell.transcript[shell._rendered_entries :]
    lines: list[str] = []
    for entry in pending:
        if entry.kind != "tooltrace":
            continue
        body_lines = entry.body.splitlines() or [entry.body]
        for body_line in body_lines:
            normalized = strip_markdown_bold(body_line).rstrip("\n")
            if not normalized or normalized.startswith("┊ "):
                continue
            lines.append(normalized)
    return tuple(lines[-80:])

def pending_tool_display_lines(shell: ProductizedShell, *, limit: int | None = None) -> tuple[str, ...]:
    pending = shell.transcript[shell._rendered_entries :]
    lines: list[str] = []
    for entry in pending:
        if entry.kind != "tooltrace":
            continue
        body_lines = entry.body.splitlines() or [entry.body]
        for body_line in body_lines:
            normalized = strip_markdown_bold(body_line).rstrip("\n")
            if not normalized:
                continue
            lines.append(normalized)
    if limit is None or len(lines) <= limit:
        return tuple(lines)
    hidden = len(lines) - (limit - 1)
    return (f"… {hidden} earlier tool line(s) hidden", *lines[-(limit - 1) :])

def live_tool_feed_lines(
    shell: ProductizedShell,
    *,
    tool_event: ToolLifecycleEvent | None = None,
    tool_events: tuple[ToolLifecycleEvent, ...] = (),
    limit: int | None = None,
) -> tuple[str, ...]:
    from .shell_progress_trace import tool_event_progress_lines

    pending_limit = None if limit is None else max(limit, 8)
    lines = list(pending_tool_display_lines(shell, limit=pending_limit))
    seen = set(lines)
    for line in tool_event_progress_lines(shell, tool_event=tool_event, tool_events=tool_events):
        if line in seen:
            continue
        seen.add(line)
        lines.append(line)
    if limit is None or len(lines) <= limit:
        return tuple(lines)
    hidden = len(lines) - (limit - 1)
    return (f"… {hidden} earlier tool line(s) hidden", *lines[-(limit - 1) :])

def turn_tool_progress_lines(
    shell: ProductizedShell,
    *,
    tool_event: ToolLifecycleEvent | None = None,
    tool_events: tuple[ToolLifecycleEvent, ...] = (),
) -> tuple[str, ...]:
    from .shell_progress_trace import tool_event_progress_lines

    lines: list[str] = []
    seen: set[str] = set()
    for line in pending_tooltrace_lines(shell):
        if line in seen:
            continue
        seen.add(line)
        lines.append(line)
    for line in tool_event_progress_lines(shell, tool_event=tool_event, tool_events=tool_events):
        if line in seen:
            continue
        seen.add(line)
        lines.append(line)
    return tuple(lines[-12:])
