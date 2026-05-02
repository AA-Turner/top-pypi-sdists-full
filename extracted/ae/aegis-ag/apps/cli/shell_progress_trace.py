"""Tool trace and frame rendering helpers for shell progress."""

from __future__ import annotations

from dataclasses import dataclass
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



from .shell_progress_support import (
    _ToolTraceDisplayParts,
    _VisibleToolEvent,
    live_tool_feed_lines,
    summarize_progress_prompt,
    turn_context_progress_line,
    turn_intent_progress_line,
    turn_marker,
    turn_phase,
    turn_title,
    turn_tool_progress_lines,
)

def render_turn_frame(
    shell: ProductizedShell,
    *,
    prompt: str,
    tick: int,
    tool_event: ToolLifecycleEvent | None = None,
    tool_events: tuple[ToolLifecycleEvent, ...] = (),
    kernel_stage_events: tuple[dict[str, object], ...] = (),
    stream_text: str = "",
):
    from .shell_progress_runtime import render_live_tool_line_text

    marker, _phase_label, phase_detail = turn_phase(tick)
    title_glyph, title_copy = turn_title(tick)
    live_lines = live_tool_feed_lines(shell, tool_event=tool_event, tool_events=tool_events)
    if not RICH_AVAILABLE:
        stream_preview = _stream_response_text(stream_text, limit=280)
        body = "\n".join(
            (
                f"{marker} {phase_detail}",
                turn_intent_progress_line(kernel_stage_events=kernel_stage_events),
                turn_context_progress_line(kernel_stage_events=kernel_stage_events),
            )
        )
        if live_lines:
            body = f"{body}\n" + "\n".join(live_lines)
        if stream_preview:
            body = f"{body}\n\n{stream_preview}"
        return body
    progress_body = Text()
    progress_body.append(marker, style=BRAND_MUTED)
    progress_body.append(f" {phase_detail}", style=BRAND_LIGHT)
    progress_body.append("\n")
    progress_body.append_text(render_live_tool_line_text(turn_intent_progress_line(kernel_stage_events=kernel_stage_events)))
    progress_body.append("\n")
    progress_body.append_text(render_live_tool_line_text(turn_context_progress_line(kernel_stage_events=kernel_stage_events)))
    for live_line in live_lines:
        progress_body.append("\n")
        progress_body.append_text(render_live_tool_line_text(live_line))
    progress_panel = Panel(
        progress_body,
        title=f"[bold {BRAND_ACCENT}]{title_glyph} {title_copy}[/bold {BRAND_ACCENT}]",
        border_style=BRAND_DARK,
        padding=(0, 1),
    )
    stream_response = _stream_response_text(stream_text)
    if not stream_response:
        return progress_panel
    response_body = Text()
    response_body.append(stream_response, style=BRAND_LIGHT)
    response_panel = Panel(
        response_body,
        border_style=BRAND_ACCENT,
        padding=(0, 1),
    )
    if Group is None:
        return progress_panel
    return Group(progress_panel, response_panel)

def render_tool_frame(
    shell: ProductizedShell,
    *,
    tool_id: str,
    tick: int,
    tool_event: ToolLifecycleEvent | None = None,
    tool_events: tuple[ToolLifecycleEvent, ...] = (),
):
    from .shell_progress_runtime import render_live_tool_line_text

    phases = tool_frame_phases(shell, tool_id, tool_event=tool_event)
    phase_label, phase_detail = phases[(tick // 3) % len(phases)]
    marker = turn_marker(tick)
    live_lines = live_tool_feed_lines(shell, tool_event=tool_event, tool_events=tool_events)
    if not RICH_AVAILABLE:
        body = f"{marker} {phase_detail}"
        if live_lines:
            body = f"{body}\n" + "\n".join(live_lines)
        return body
    body = Text()
    body.append(marker, style=BRAND_MUTED)
    body.append(f" {phase_detail}\n", style=BRAND_LIGHT)
    body.append(f"{phase_label} · {tool_id}", style=BRAND_MUTED)
    for live_line in live_lines:
        body.append("\n")
        body.append_text(render_live_tool_line_text(live_line))
    return Panel(
        body,
        title=f"[bold {BRAND_ACCENT}]🛠️ Aegis is using a tool[/bold {BRAND_ACCENT}]",
        border_style=BRAND_DARK,
        padding=(0, 1),
    )

def tool_frame_phases(
    shell: ProductizedShell,
    tool_id: str,
    *,
    tool_event: ToolLifecycleEvent | None = None,
) -> tuple[tuple[str, str], ...]:
    return (
        ("tool.bind", "Summoning the requested rite"),
        ("tool.execute", "Working the rite inside the current clone surface"),
        ("tool.report", "Returning the omen to the transcript"),
    )

def tool_trace_line(
    shell: ProductizedShell,
    tool_event: ToolLifecycleEvent | None,
) -> str | None:
    if tool_event is None:
        return None
    tool_id = tool_event.invocation.tool_id
    emoji = _tool_trace_emoji(tool_id)
    label = _tool_trace_label(tool_event)
    if tool_event.phase == "requested":
        return f"┊ {emoji} preparing {_tool_trace_prepare_label(tool_event)}…"
    if tool_event.phase == "approval.denied":
        return f"┊ {emoji} {label:<12} blocked"
    if tool_event.phase == "approval.deferred":
        return f"┊ {emoji} {label:<12} awaiting approval"
    if tool_event.phase not in {"execution.completed", "execution.failed"}:
        return None
    preview = _tool_trace_preview(tool_event.invocation.arguments, tool_id=tool_id)
    duration = _tool_trace_duration(tool_event)
    duration_part = f"  {duration}" if duration else ""
    if tool_event.phase == "execution.failed":
        if preview and tool_id in {"tool.terminal.exec", "tool.process.manage"}:
            return f"┊ {emoji} {label:<12} {preview} [error]{duration_part}"
        failure_label = compact_line(tool_event.detail or "failed", limit=28)
        return f"┊ {emoji} {label:<12} {failure_label}{duration_part}"
    if preview:
        return f"┊ {emoji} {label:<12} {preview}{duration_part}"
    return f"┊ {emoji} {label}{duration_part}"

def tool_event_progress_line(
    shell: ProductizedShell,
    tool_event: ToolLifecycleEvent | None,
) -> str | None:
    if tool_event is None:
        return None
    if tool_event.phase == "execution.started":
        emoji = _tool_trace_emoji(tool_event.invocation.tool_id, tool_event.invocation.arguments)
        label = _tool_trace_started_label(tool_event)
        preview = _tool_trace_preview(tool_event.invocation.arguments, tool_id=tool_event.invocation.tool_id)
        if preview:
            return f"┊ {emoji} {label:<12} {preview}"
        return f"┊ {emoji} {label}"
    return tool_trace_line(shell, tool_event)

def tool_event_progress_lines(
    shell: ProductizedShell,
    *,
    tool_event: ToolLifecycleEvent | None = None,
    tool_events: tuple[ToolLifecycleEvent, ...] = (),
) -> tuple[str, ...]:
    lines: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    events = tool_events or ((tool_event,) if tool_event is not None else ())
    for event in events[-3:]:
        event_lines = _tool_event_progress_lines_for_event(shell, event)
        for line in event_lines:
            key = (event.invocation.invocation_id, event.phase, line)
            if key in seen:
                continue
            seen.add(key)
            lines.append(line)
    return tuple(lines)

def _tool_event_progress_lines_for_event(
    shell: ProductizedShell,
    event: ToolLifecycleEvent,
) -> tuple[str, ...]:
    if event.phase == "execution.started" and event.invocation.tool_id == "tool.sub_agents":
        expanded = _sub_agents_trace_progress_lines(event.invocation.arguments)
        if expanded:
            return expanded
    line = tool_event_progress_line(shell, event)
    return () if line is None else (line,)

def tool_event_lines(
    shell: ProductizedShell,
    tool_event: ToolLifecycleEvent | None,
) -> tuple[str | None, str | None]:
    if tool_event is None:
        return (None, None)
    phase_labels = {
        "requested": "Tool requested",
        "classified": "Tool classified",
        "approval.granted": "Approval granted",
        "approval.denied": "Approval denied",
        "approval.deferred": "Approval deferred",
        "execution.started": "Tool executing",
        "execution.completed": "Tool completed",
        "execution.failed": "Tool failed",
    }
    title = f"{phase_labels.get(tool_event.phase, tool_event.phase)} · {tool_event.invocation.tool_id}"
    detail = compact_line(" ".join((tool_event.detail or "").split()), limit=112) if tool_event.detail else ""
    details = [detail] if detail else []
    if tool_event.approval is not None and tool_event.approval.required_controls:
        details.append(f"controls: {', '.join(tool_event.approval.required_controls)}")
    if tool_event.execution is not None:
        details.append(f"outcome: {tool_event.execution.outcome}")
    return (title, " · ".join(part for part in details if part))

def tool_event_summary(shell: ProductizedShell, tool_event: ToolLifecycleEvent | None) -> str | None:
    if tool_event is None:
        return None
    line = tool_event_progress_line(shell, tool_event)
    if line:
        return compact_line(strip_markdown_bold(line.replace("┊ ", "")), limit=112)
    title, _ = tool_event_lines(shell, tool_event)
    return title

def render_tool_trace_fragments(line: str, *, leading_newline: bool = False) -> list[tuple[str, str]]:
    parts = _tool_trace_display_parts(line)
    if _is_intent_trace_line(line):
        fragments: list[tuple[str, str]] = []
        if leading_newline:
            fragments.append(("", "\n"))
        for text in (parts.rail, f"{parts.emoji} " if parts.emoji else "", parts.prefix, parts.label):
            if text:
                fragments.append(("class:progress-intent", text))
        if parts.body:
            fragments.append(("class:progress-intent", parts.gap or " "))
            fragments.append(("class:progress-intent", parts.body))
        if parts.duration:
            fragments.append(("class:progress-intent", parts.duration_gap or "  "))
            fragments.append(("class:progress-intent", parts.duration))
        return fragments
    state = _tool_trace_state(line)
    emoji_style = "class:progress-tool-emoji" if state == "done" else "class:progress-tool-verb"
    label_style = "class:progress-tool-label" if state in {"done", "error"} else "class:progress-tool-verb"
    body_style = "class:progress-tool-body" if state in {"done", "error"} else "class:progress-tool-verb"
    fragments: list[tuple[str, str]] = []
    if leading_newline:
        fragments.append(("", "\n"))
    if parts.rail:
        fragments.append(("class:progress-tool-rail", parts.rail))
    if parts.emoji:
        fragments.append((emoji_style, f"{parts.emoji} "))
    if parts.prefix:
        fragments.append(("class:progress-tool-verb", parts.prefix))
    fragments.append((label_style, parts.label))
    if parts.body:
        fragments.append(("class:progress-tool-gap", parts.gap or " "))
        fragments.append((body_style, parts.body))
    if parts.duration:
        fragments.append(("class:progress-tool-gap", parts.duration_gap or "  "))
        fragments.append(("class:progress-tool-duration", parts.duration))
    return fragments

def render_tool_trace_text(line: str) -> Text:
    parts = _tool_trace_display_parts(line)
    if _is_intent_trace_line(line):
        block = Text()
        for text in (parts.rail, f"{parts.emoji} " if parts.emoji else "", parts.prefix, parts.label):
            if text:
                block.append(text, style=BRAND_ACCENT_STRONG)
        if parts.body:
            block.append(parts.gap or " ", style=BRAND_ACCENT_STRONG)
            block.append(parts.body, style=BRAND_ACCENT_STRONG)
        if parts.duration:
            block.append(parts.duration_gap or "  ", style=BRAND_ACCENT_STRONG)
            block.append(parts.duration, style=BRAND_ACCENT_STRONG)
        return block
    state = _tool_trace_state(line)
    emoji_style = BRAND_ACCENT if state == "done" else BRAND_MUTED
    label_style = f"bold {BRAND_ACCENT_STRONG}" if state in {"done", "error"} else BRAND_MUTED
    body_style = BRAND_LIGHT if state in {"done", "error"} else BRAND_MUTED
    block = Text()
    if parts.rail:
        block.append(parts.rail, style=BRAND_DARK)
    if parts.emoji:
        block.append(f"{parts.emoji} ", style=emoji_style)
    if parts.prefix:
        block.append(parts.prefix, style=BRAND_MUTED)
    block.append(parts.label, style=label_style)
    if parts.body:
        block.append(parts.gap or " ")
        block.append(parts.body, style=body_style)
    if parts.duration:
        block.append(parts.duration_gap or "  ")
        block.append(parts.duration, style=BRAND_MUTED)
    return block


def _is_intent_trace_line(line: str) -> bool:
    return strip_markdown_bold(line).startswith("┊ 🧠 intent")

def _tool_trace_display_parts(line: str) -> _ToolTraceDisplayParts:
    body = strip_markdown_bold(line).rstrip("\n")
    rail = ""
    if body.startswith("┊ "):
        rail = "┊ "
        body = body[2:]
    emoji, separator, remainder = body.partition(" ")
    if not separator:
        return _ToolTraceDisplayParts(rail="", emoji="", prefix="", label=body, gap="", body="", duration_gap="", duration="")

    duration_gap = ""
    duration = ""
    duration_match = re.search(r"(?P<spacing>\s{2,})(?P<duration>\d+(?:\.\d)?s)$", remainder)
    if duration_match is not None:
        duration_gap = duration_match.group("spacing")
        duration = duration_match.group("duration")
        remainder = remainder[: duration_match.start()].rstrip()

    prefix = ""
    label = remainder
    gap = ""
    tail = ""
    if remainder.startswith("preparing "):
        prefix = "preparing "
        label = remainder.removeprefix("preparing ")
    else:
        detail_match = re.match(r"(?P<label>.+?)(?P<gap>\s{2,})(?P<body>.+)$", remainder)
        if detail_match is not None:
            label = detail_match.group("label")
            gap = detail_match.group("gap")
            tail = detail_match.group("body")

    return _ToolTraceDisplayParts(
        rail=rail,
        emoji=emoji,
        prefix=prefix,
        label=label,
        gap=gap,
        body=tail,
        duration_gap=duration_gap,
        duration=duration,
    )

def _tool_trace_state(line: str) -> str:
    normalized = strip_markdown_bold(line).rstrip("\n")
    parts = _tool_trace_display_parts(normalized)
    if "[error]" in normalized:
        return "error"
    if parts.prefix == "preparing ":
        return "active"
    if "awaiting approval" in normalized or normalized.endswith(" blocked"):
        return "active"
    if parts.body and not parts.duration:
        return "active"
    return "done"

def _tool_trace_emoji(tool_id: str, arguments=None) -> str:
    if tool_id in {"tool.web.search", "tool.file.search"}:
        return "🔎"
    if tool_id.startswith("tool.browser."):
        return "🌐"
    if tool_id in {"tool.web.read", "tool.file.read"}:
        return "📖"
    if tool_id in {"tool.file.write", "tool.file.patch", "tool.code.execute"}:
        return "🛠"
    if tool_id == "tool.terminal.exec":
        return "💻"
    if tool_id == "tool.process.manage":
        return "⚙"
    if tool_id == "tool.profile.manage":
        return "🪪"
    if tool_id == "tool.cron.manage":
        return "⏰"
    if tool_id == "tool.sub_agents":
        return "👾"
    if tool_id == "tool.activity.manage":
        return "🎯"
    if tool_id in {"tool.memory.recall", "tool.memory.upload"}:
        return "🧠"
    if tool_id in {"tool.procedure.inspect", "tool.procedure.manage"}:
        return "📚"
    if tool_id in {"tool.skill.list", "tool.skill.view", "tool.skill.manage"}:
        return "🧩"
    if tool_id == "tool.message.send":
        return "📨"
    if tool_id == "tool.todo.manage":
        return "📋"
    return "⚙"

def _tool_trace_label(tool_event: ToolLifecycleEvent) -> str:
    tool_id = tool_event.invocation.tool_id
    aliases = {
        "tool.file.search": "grep",
        "tool.file.read": "read",
        "tool.file.write": "write",
        "tool.file.patch": "patch",
        "tool.web.search": "search",
        "tool.web.read": "fetch",
        "tool.terminal.exec": "computer",
        "tool.process.manage": "proc",
        "tool.profile.manage": "profile",
        "tool.activity.manage": "activity",
        "tool.cron.manage": "cron",
        "tool.sub_agents": "sub_agents",
        "tool.memory.recall": "recall",
        "tool.memory.upload": "memory",
        "tool.procedure.inspect": "procedure",
        "tool.procedure.manage": "procedure",
        "tool.skill.list": "skills",
        "tool.skill.view": "skill",
        "tool.skill.manage": "skill",
        "tool.todo.manage": "todo",
        "tool.message.send": "message",
        "tool.code.execute": "code",
    }
    if tool_id.startswith("tool.browser."):
        return tool_id.removeprefix("tool.browser.")
    return aliases.get(tool_id, tool_id.removeprefix("tool."))

def _tool_trace_preview(arguments, *, tool_id: str | None = None) -> str:
    if tool_id == "tool.sub_agents":
        preview = _sub_agents_trace_preview(arguments)
        if preview:
            return preview
    if tool_id == "tool.process.manage":
        action = str(arguments.get("action") or "").strip().lower()
        process_id = str(arguments.get("process_id") or "").strip()
        if action and process_id:
            return compact_line(f"{action} {process_id}", limit=56)
        if action:
            return compact_line(action, limit=36)
    if tool_id == "tool.terminal.exec":
        command = str(arguments.get("command") or "").strip()
        if command:
            return compact_line(command, limit=96)
    preview_keys = (
        "query",
        "pattern",
        "url",
        "path",
        "command",
        "title",
        "prompt",
        "name",
        "message",
        "text",
        "content",
        "charter_text",
        "user_text",
        "user_content",
        "relationship_text",
        "relationship_content",
        "reference",
        "goal_id",
        "procedure_id",
        "skill_id",
        "server_id",
    )
    for key in preview_keys:
        value = arguments.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return compact_line(text, limit=36)
    action = str(arguments.get("action") or "").strip().lower()
    if action in {"list", "ls"}:
        return "all"
    return ""

def _sub_agents_trace_preview(arguments) -> str:
    action = _sub_agents_action_label(arguments)
    tasks = arguments.get("tasks")
    if isinstance(tasks, list) and tasks:
        previews = list(_sub_agent_task_previews(tasks, limit=3))
        if previews:
            suffix = f" +{len(tasks) - len(previews)}" if len(tasks) > len(previews) else ""
            return compact_line(f"{action} · " + "; ".join(previews) + suffix, limit=112)
    run_id = str(arguments.get("run_id") or arguments.get("sub_agent_run_id") or "").strip()
    if run_id:
        return compact_line(f"{action} · {run_id}", limit=112)
    name = str(arguments.get("name") or "").strip()
    task = str(arguments.get("task") or arguments.get("prompt") or "").strip()
    if name and task:
        return compact_line(f"{action} · {name}: {task}", limit=112)
    if task:
        return compact_line(f"{action} · {task}", limit=112)
    if name:
        return compact_line(f"{action} · {name}", limit=56)
    return action

def _sub_agents_trace_progress_lines(arguments) -> tuple[str, ...]:
    tasks = arguments.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return ()
    previews = tuple(_sub_agent_task_previews(tasks, limit=6))
    if not previews:
        return ()
    lines = [f"┊ 👾 sub_agents   {_sub_agents_action_label(arguments)} · {len(tasks)} agents"]
    lines.extend(f"┊   {index}. {compact_line(preview, limit=104)}" for index, preview in enumerate(previews, start=1))
    if len(tasks) > len(previews):
        lines.append(f"┊   … {len(tasks) - len(previews)} more")
    return tuple(lines)

def _sub_agents_action_label(arguments) -> str:
    action = str(arguments.get("action") or "run").strip().lower()
    aliases = {
        "check": "status",
        "wait": "join",
    }
    return aliases.get(action, action or "run")

def _sub_agent_task_previews(tasks: list, *, limit: int) -> tuple[str, ...]:
    previews: list[str] = []
    for item in tasks[:limit]:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        task = str(item.get("task") or item.get("prompt") or "").strip()
        if name and task:
            previews.append(f"{name}: {task}")
        elif task:
            previews.append(task)
        elif name:
            previews.append(name)
    return tuple(previews)

def _tool_trace_prepare_label(tool_event: ToolLifecycleEvent) -> str:
    return _tool_trace_label(tool_event)

def _tool_trace_started_label(tool_event: ToolLifecycleEvent) -> str:
    return _tool_trace_label(tool_event)

def _tool_trace_duration(tool_event: ToolLifecycleEvent) -> str:
    requested_at = tool_event.invocation.requested_at
    if requested_at is None:
        return ""
    delta = max(0.0, (tool_event.occurred_at - requested_at).total_seconds())
    return f"{delta:.1f}s"

def _stream_preview(stream_text: str, *, limit: int = 220) -> str:
    normalized = " ".join(stream_text.split())
    if not normalized:
        return ""
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[: limit - 3]}..."

def _stream_response_text(stream_text: str, *, limit: int = 3200) -> str:
    sanitized = _sanitize_stream_tool_markup(stream_text)
    normalized = strip_markdown_bold(sanitized.replace("\r\n", "\n").replace("\r", "\n")).lstrip("\n")
    if not normalized.strip():
        return ""
    if len(normalized) <= limit:
        return normalized
    tail = normalized[-limit:]
    newline = tail.find("\n")
    if newline >= 0:
        trimmed = tail[newline + 1 :].lstrip("\n")
        if trimmed:
            return f"...\n{trimmed}"
    return f"... {tail.lstrip()}"

def _sanitize_stream_tool_markup(raw: str) -> str:
    cleaned = raw
    for pattern in _STREAM_TOOL_BLOCK_PATTERNS:
        previous = None
        while previous != cleaned:
            previous = cleaned
            cleaned = pattern.sub("", cleaned)
    open_match = _STREAM_OPEN_TOOL_TAG_PATTERN.search(cleaned)
    if open_match is not None:
        cleaned = cleaned[: open_match.start()]
    cleaned = _STREAM_TOOL_TAG_PATTERN.sub("", cleaned)
    partial_start = _partial_tool_tag_start(cleaned)
    if partial_start is not None:
        cleaned = cleaned[:partial_start]
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned

def _partial_tool_tag_start(text: str) -> int | None:
    marker = text.rfind("<")
    if marker < 0:
        return None
    fragment = text[marker + 1 :].strip().lower()
    if ">" in fragment or not fragment:
        return marker if fragment == "" else None
    closing = fragment.startswith("/")
    if closing:
        fragment = fragment[1:]
    if ":" in fragment:
        fragment = fragment.split(":", 1)[1]
    fragment = fragment.strip()
    tool_tags = ("tool_call", "invoke", "parameter")
    if not fragment:
        return marker
    if any(name.startswith(fragment) for name in tool_tags):
        return marker
    return None
