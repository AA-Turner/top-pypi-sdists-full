"""Bound methods extracted from apps/cli/shell.py."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from difflib import unified_diff
import os
from pathlib import Path
import re
import shlex
import threading
import time

from packages.contracts import ExperienceRecord
from packages.kernel.runtime import KernelOutcome
from packages.operator import (
    MemoryOperatorDetail,
    MemorySearchHit,
    build_audit_surface,
    build_memory_operator_surface,
    build_profile_operator_surface,
    build_activity_operator_surface,
    render_audit_lines,
    render_memory_lines,
    render_profile_lines,
    render_activity_lines,
)
from packages.tools.handler_support import resolve_workspace_path
from .provider_flow import provider_setup_defaults, run_provider_selection_wizard
from .runtime import CliRuntime
from .wizard import WIZARD_BACK
from .shell_composer import (
    build_command_palette as _build_shell_command_palette,
    build_composer_body as _build_shell_composer_body,
    build_divider_window as _build_shell_divider_window,
    build_input_window as _build_shell_input_window,
    build_key_bindings as _build_shell_key_bindings,
    build_prompt_buffer as _build_shell_prompt_buffer,
    build_queue_preview_window as _build_shell_queue_preview_window,
    prompt_continuation as _shell_prompt_continuation,
    prompt_label as _shell_prompt_label,
    prompt_style as _shell_prompt_style,
    prompt_style_map as _shell_prompt_style_map,
    prompt_toolkit_composer_available as _shell_prompt_toolkit_composer_available,
    read_command as _read_shell_command,
    shell_history as _shell_history,
)
from .shell_boot import STARTUP_SEQUENCE_STEPS, BootFrameContext, render_boot_frame
from .shell_opening import (
    ShellOpeningContext,
    compose_shell_opening_instruction,
    compose_shell_opener,
)
from .shell_progress import (
    animations_enabled as _shell_animations_enabled,
    render_queued_followup_fragments as _render_shell_queued_followup_fragments,
    render_tool_frame as _render_shell_tool_frame,
    tool_trace_line as _shell_tool_trace_line,
    render_turn_frame as _render_shell_turn_frame,
    render_turn_progress_fragments as _render_shell_turn_progress_fragments,
    run_tool_with_progress as _run_shell_tool_with_progress,
    run_turn_with_progress as _run_shell_turn_with_progress,
    run_turn_with_queued_input as _run_shell_turn_with_queued_input,
    summarize_progress_prompt as _summarize_shell_progress_prompt,
    tool_event_lines as _shell_tool_event_lines,
    tool_event_summary as _shell_tool_event_summary,
    tool_event_tracker as _shell_tool_event_tracker,
    tool_frame_phases as _shell_tool_frame_phases,
    turn_phase as _shell_turn_phase,
    _tool_trace_emoji as _shell_tool_trace_emoji,
)
from .shell_render import (
    center_brand_block as _center_shell_brand_block,
    displayable_experiences as _displayable_shell_experiences,
    format_experience_status as _format_shell_experience_status,
    growth_panel_lines as _shell_growth_panel_lines,
    growth_progress_bar as _shell_growth_progress_bar,
    growth_progress_counts as _shell_growth_progress_counts,
    recent_activity_lines as _shell_recent_activity_lines,
    recent_experience_lines as _shell_recent_experience_lines,
    render_brand_column as _render_shell_brand_column,
    render_chat_entry as _render_shell_chat_entry,
    render_entry as _render_shell_entry,
    render_guardian_brand_mark as _render_shell_guardian_mark,
    render_growth_mark_for_stage as _render_shell_growth_mark,
    render_pending_entries as _render_shell_pending_entries,
    render_shell_frame as _render_shell_frame_view,
    render_status_column as _render_shell_status_column,
    should_display_experience as _should_display_shell_experience,
    styled_growth_progress_bar as _styled_shell_growth_progress_bar,
)
from .shell_stack import (
    Align,
    Completion,
    Completer,
    Console,
    Document,
    FormattedText,
    Group,
    Live,
    PROMPT_TOOLKIT_AVAILABLE,
    Panel,
    RICH_AVAILABLE,
    Table,
    Text,
)
from .shell_ui import (
    BRAND_ACCENT,
    BRAND_ACCENT_STRONG,
    BRAND_DARK,
    BRAND_LIGHT,
    BRAND_MUTED,
    COMMAND_PALETTE_VISIBLE_ROWS,
    EGG_STAGE_ROWS,
    GROWTH_HIGHLIGHT_FG,
    GROWTH_PROGRESS_EMPTY,
    GROWTH_PROGRESS_FILLED,
    GROWTH_PROGRESS_WIDTH,
    GUARDIAN_HEAD_ROWS,
    GUARDIAN_STAGE_ROWS,
    HATCHLING_STAGE_ROWS,
    QUEUE_PREVIEW_INSET,
    SCOUT_STAGE_ROWS,
    SEED_STAGE_ROWS,
    SHELL_WELCOME_HEADLINE,
    STARTUP_SEQUENCE_FINAL_DELAY,
    STARTUP_SEQUENCE_STEP_DELAY,
    USER_HISTORY_BG,
    USER_HISTORY_FG,
    WEB_URL_PATTERN,
    compact_line as _compact_line,
    centered_guardian_rows as _centered_guardian_rows,
    display_path as _display_path,
    display_width as _display_width,
    render_guardian_mark,
    resolve_aegis_version as _resolve_aegis_version,
)

__all__ = [
    "BRAND_ACCENT",
    "BRAND_ACCENT_STRONG",
    "BRAND_DARK",
    "BRAND_LIGHT",
    "BRAND_MUTED",
    "COMMAND_PALETTE_VISIBLE_ROWS",
    "Console",
    "Document",
    "EGG_STAGE_ROWS",
    "GROWTH_HIGHLIGHT_FG",
    "GROWTH_PROGRESS_EMPTY",
    "GROWTH_PROGRESS_FILLED",
    "GROWTH_PROGRESS_WIDTH",
    "GUARDIAN_HEAD_ROWS",
    "GUARDIAN_STAGE_ROWS",
    "HATCHLING_STAGE_ROWS",
    "PendingShellCommand",
    "ProductizedShell",
    "QUEUE_PREVIEW_INSET",
    "RICH_AVAILABLE",
    "SCOUT_STAGE_ROWS",
    "SEED_STAGE_ROWS",
    "SHELL_WELCOME_HEADLINE",
    "STARTUP_SEQUENCE_FINAL_DELAY",
    "STARTUP_SEQUENCE_STEP_DELAY",
    "ShellCompleter",
    "TranscriptEntry",
    "USER_HISTORY_BG",
    "USER_HISTORY_FG",
    "_centered_guardian_rows",
    "_display_width",
    "render_guardian_mark",
]



from .shell_support_runtime import *  # noqa: F401,F403

def _next_command(self) -> PendingShellCommand:
    if self._pending_commands:
        return self._pending_commands.popleft()
    return PendingShellCommand(self._read_command())

def _prompt_toolkit_composer_available(self) -> bool:
    return _shell_prompt_toolkit_composer_available(self)

def _shell_history(self):
    return _shell_history(self)

def _build_prompt_buffer(self):
    return _build_shell_prompt_buffer(self)

def _build_input_window(self, buffer):
    return _build_shell_input_window(self, buffer)

def _build_command_palette(self):
    return _build_shell_command_palette(self)

def _build_queue_preview_window(self):
    return _build_shell_queue_preview_window(self)

def _build_divider_window(self):
    return _build_shell_divider_window(self)

def _build_composer_body(self, *, input_window, command_palette, top_windows=()):
    return _build_shell_composer_body(
        self,
        input_window=input_window,
        command_palette=command_palette,
        top_windows=top_windows,
    )

def _read_command(self) -> str:
    return _read_shell_command(self)

def personality_preset_choices(self) -> tuple[tuple[str, str], ...]:
    return tuple(
        (preset.preset_id, preset.summary)
        for preset in self.runtime.personality_presets()
        if preset.preset_id != "custom"
    )

def _prompt_label(self) -> str:
    return _shell_prompt_label(self)

def _prompt_continuation(self):
    return _shell_prompt_continuation()

def _prompt_style(self):
    return _shell_prompt_style()

def _prompt_style_map(self) -> dict[str, str]:
    return _shell_prompt_style_map()

def _build_key_bindings(self, *, submit=None, allow_exit: bool = True) -> KeyBindings:
    return _build_shell_key_bindings(submit=submit, allow_exit=allow_exit)

def _composer_divider(self) -> str:
    width = getattr(self.console, "width", 100)
    try:
        width = self.console.size.width
    except AttributeError:
        pass
    return "─" * max(24, width - 1)

def _format_status_tokens(self, value: int | None) -> str:
    if value is None or value <= 0:
        return "--"
    if value >= 1_000_000:
        whole = round(value / 1_000_000, 1)
        return f"{whole:g}M"
    if value >= 1_000:
        whole = round(value / 1_000)
        return f"{whole}K"
    return str(value)

def _status_bar_context_style(self, percent_used: int | None) -> str:
    if percent_used is None:
        return "class:status-bar-muted"
    if percent_used >= 95:
        return "class:status-bar-critical"
    if percent_used > 80:
        return "class:status-bar-warn"
    return "class:status-bar-good"

def _build_context_bar(self, percent_used: int | None, width: int = 12) -> str:
    safe_percent = max(0, min(100, percent_used or 0))
    filled = round((safe_percent / 100) * width)
    return f"[{('█' * filled) + ('░' * max(0, width - filled))}]"

def _build_growth_bar_fragments(self, growth, *, width: int = 10) -> list[tuple[str, str]]:
    filled, empty = self._growth_progress_counts(growth, width=width)
    fragments: list[tuple[str, str]] = [("class:status-bar-growth-bracket", "[")]
    if filled:
        fragments.append(("class:status-bar-growth-fill", GROWTH_PROGRESS_FILLED * filled))
    if empty:
        fragments.append(("class:status-bar-growth-empty", GROWTH_PROGRESS_EMPTY * empty))
    fragments.append(("class:status-bar-growth-bracket", "]"))
    return fragments

def _status_bar_elapsed_fragments(elapsed_seconds: int, *, streaming_active: bool = False) -> list[tuple[str, str]]:
    fragments: list[tuple[str, str]] = [("class:status-bar-muted", f"{elapsed_seconds}s")]
    if streaming_active:
        fragments.extend(
            [
                ("class:status-bar-sep", " · "),
                ("class:status-bar-stream", "streaming"),
            ]
        )
    return fragments

def _status_bar_snapshot(self) -> dict[str, object]:
    provider = dict(self.runtime.provider_summary())
    model_name = str(provider.get("strong_model") or "<unset>")
    model_short = model_name.split("/")[-1] if "/" in model_name else model_name
    model_short = _compact_line(model_short, limit=26)
    context_window = provider.get("context_window_tokens")
    try:
        context_limit = int(context_window) if context_window is not None else None
    except (TypeError, ValueError):
        context_limit = None
    context_used = max(0, self._last_prompt_tokens)
    context_percent = None
    if context_limit:
        context_percent = max(0, min(100, round((context_used / context_limit) * 100)))
    if self._turn_started_at is not None:
        elapsed_seconds = max(0, round(time.monotonic() - self._turn_started_at))
    else:
        elapsed_seconds = max(0, int(self._last_turn_elapsed_seconds))
    return {
        "model_short": model_short,
        "context_used": context_used,
        "context_limit": context_limit,
        "context_percent": context_percent,
        "elapsed_seconds": elapsed_seconds,
    }

def _status_bar_fragments(self):
    snapshot = self._status_bar_snapshot()
    growth = self.runtime.inspect_growth(session_id=self.session_id)
    percent = snapshot["context_percent"]
    percent_style = self._status_bar_context_style(percent if isinstance(percent, int) else None)
    context_used = self._format_status_tokens(snapshot["context_used"])
    context_limit = self._format_status_tokens(snapshot["context_limit"])
    percent_label = f"{percent}%" if isinstance(percent, int) else "--"
    elapsed_seconds = int(snapshot["elapsed_seconds"])
    streaming_active = bool(getattr(self, "_streaming_response_active", False))
    return [
        ("class:status-bar-edge", " "),
        ("class:status-bar-model", str(snapshot["model_short"])),
        ("class:status-bar-sep", " │ "),
        ("class:status-bar-muted", f"{context_used}/{context_limit}"),
        ("class:status-bar-sep", " │ "),
        (percent_style, self._build_context_bar(percent if isinstance(percent, int) else None)),
        ("class:status-bar-sep", " "),
        (percent_style, percent_label),
        ("class:status-bar-sep", " │ "),
        *_status_bar_elapsed_fragments(elapsed_seconds, streaming_active=streaming_active),
        ("class:status-bar-sep", " │ "),
        ("class:status-bar-level", growth.cycle_label),
        ("class:status-bar-sep", " "),
        *self._build_growth_bar_fragments(growth),
        ("class:status-bar-sep", " "),
        ("class:status-bar-level", f"Lv.{growth.ascension_level} · {growth.progress_percent}%"),
        ("class:status-bar-edge", " "),
    ]

def _clear_composer(self, command: str) -> None:
    if PROMPT_TOOLKIT_AVAILABLE:
        return
    stream = getattr(self.console, "file", None)
    if stream is None or not hasattr(stream, "isatty") or not stream.isatty():
        return
    logical_lines = 3 + command.count("\n")
    stream.write("\r\x1b[2K")
    for _ in range(logical_lines):
        stream.write("\x1b[1A\r\x1b[2K")
    stream.flush()

def _enqueue_followup_command(self, raw_command: str) -> None:
    command = raw_command.strip()
    if not command:
        return
    self._pending_commands.append(PendingShellCommand(command=command))

def _is_startup_conversational_command(self, raw_command: str) -> bool:
    command = raw_command.strip()
    return bool(command) and not command.startswith("/")

def _startup_intent_dispatch_ready(self) -> bool:
    status = self.runtime.intent_runtime_status()
    intent_mode = str(status.get("intent_mode") or "skip").strip().lower()
    if intent_mode != "embedded":
        return True
    return bool(status.get("intent_ready"))

def _startup_should_hold_user_command(self, raw_command: str) -> bool:
    if not self._is_startup_conversational_command(raw_command):
        return False
    return not self._startup_transcript_primed

def _mark_startup_user_turn_submitted(self, raw_command: str) -> None:
    if self._is_startup_conversational_command(raw_command):
        self._startup_user_turn_submitted = True

def _startup_should_surface_intent_notices(self) -> bool:
    if not self._startup_surface_prepared or not self._intent_runtime_ready_seen:
        return True
    return not self._startup_transcript_primed

def _append_intent_runtime_notice(self, title: str, body: str) -> None:
    notice = (title, body)
    if self._intent_runtime_notices and self._intent_runtime_notices[-1] == notice:
        return
    self._intent_runtime_notices.append(notice)
    if len(self._intent_runtime_notices) > 3:
        del self._intent_runtime_notices[:-3]

def _sync_intent_runtime_notices(self) -> None:
    status = self.runtime.intent_runtime_status()
    intent_mode = str(status.get("intent_mode") or "skip").strip().lower()
    if intent_mode != "embedded":
        return
    if not self._intent_runtime_notice_seeded:
        self._append_intent_runtime_notice(
            "✦ intent init",
            "aegis intent is initialized 💯",
        )
        self._intent_runtime_notice_seeded = True
    runtime_state = str(status.get("runtime_state") or "cold").strip().lower() or "cold"
    if runtime_state == self._intent_runtime_last_state:
        return
    self._intent_runtime_last_state = runtime_state
    if runtime_state == "warming":
        self._append_intent_runtime_notice(
            "✦ intent warm",
            "aegis intent is warming up ⏳",
        )
        return
    if runtime_state == "loaded":
        self._append_intent_runtime_notice(
            "✦ intent ready",
            "aegis intent is ready now ✅",
        )
        self._intent_runtime_ready_seen = True
        self._intent_runtime_ready_seen_at = time.monotonic()
        self._intent_ready_notice_until = None
        return
    health_status = str(status.get("health_status") or "").strip().lower()
    if health_status in {"pending", "downloading"}:
        self._append_intent_runtime_notice(
            "✦ intent init",
            "aegis intent is bootstrapping ⌛️",
        )
        return

def _prepare_startup_surface(self) -> None:
    self._sync_intent_runtime_notices()
    if self._startup_surface_prepared or self._startup_surface_prepare_started:
        return
    self._startup_surface_prepare_started = True

    def prepare_surface() -> None:
        try:
            self.runtime.prepare_session_surface(self.session_id)
            self._refresh_skill_slash_specs()
        finally:
            self._startup_surface_prepared = True
            self._sync_intent_runtime_notices()

    threading.Thread(
        target=prepare_surface,
        name="aegis-startup-surface",
        daemon=True,
    ).start()

def _prime_startup_transcript_if_needed(self) -> None:
    if self._startup_transcript_primed:
        self._sync_intent_runtime_notices()
        return
    self._prime_transcript()
    self._startup_transcript_primed = True
    self._sync_intent_runtime_notices()

def _prime_transcript(self, *, use_proactive_opening: bool = True) -> None:
    session = self.runtime.inspect_session(self.session_id)
    continuity = self.runtime.inspect_continuity(session_id=self.session_id)
    assistant_name = continuity.profile.state.display_name or "Aegis"
    goals = self.runtime.inspect_goals(self.session_id)
    opening_context = ShellOpeningContext(
        opened=self.opened,
        display_name=assistant_name,
        user_profile_text=(continuity.profile.user_profile_text or "").strip(),
        personality=continuity.profile.companion.personality if continuity.profile.companion is not None else (),
        reengagement_style=continuity.reengagement_style,
        wake_action=continuity.wake_action or "",
        wake_summary=continuity.wake_summary or "",
        has_goals=bool(goals),
    )
    startup_outcome = None
    if use_proactive_opening:
        try:
            startup_outcome = self.runtime.generate_opening_reply(
                session_id=self.session_id,
                prompt=compose_shell_opening_instruction(opening_context),
                opening_label=self.opened,
            )
        except Exception as error:
            if self.debug:
                self._append_entry("notice", "Startup prompt", f"fallback to local opener\nreason: {error}")
    if startup_outcome is not None and startup_outcome.execution.summary.strip():
        self._append_entry("assistant", assistant_name, startup_outcome.execution.summary.strip())
    else:
        self._append_entry("assistant", assistant_name, compose_shell_opener(opening_context))
    for execution in self.runtime.run_due_cron_jobs(session_id=self.session_id):
        if execution.job.action_kind == "greeting":
            self._append_entry(
                "assistant",
                assistant_name,
                execution.summary,
                meta=f"cron · {execution.job.name}",
            )
        else:
            self._append_entry(
                "notice",
                "Cron job",
                execution.summary,
                meta=f"{execution.job.name} · {execution.job.action_kind}",
            )
    if self.debug:
        self._append_entry(
            "notice",
            "Growth context",
            "\n".join(
                [
                    f"session_id: {session.session_id}",
                    f"clone_id: {self.runtime.clone_id_for_session(session)}",
                    f"continuity: {continuity.continuity_summary}",
                    f"growth_action: {continuity.wake_action}",
                    f"growth_summary: {continuity.wake_summary}",
                    f"reengagement_style: {continuity.reengagement_style}",
                    f"reengagement_prompt: {continuity.reengagement_prompt}",
                ]
            ),
        )
    self._startup_transcript_primed = True

def _assistant_name(self) -> str:
    session = self.runtime.inspect_session(self.session_id)
    return self.runtime.inspect_profile(session.profile_id).state.display_name or "Aegis"

def _append_assistant_surface_reply(self, body: str, *, meta: str = "") -> None:
    self._append_entry("assistant", self._assistant_name(), body, meta=meta)

def _render_shell_frame(self):
    return _render_shell_frame_view(self)

def _render_brand_column(self, session, provider, growth):
    return _render_shell_brand_column(self, session, provider, growth)

def _render_status_column(self, session, continuity, context_frame, provider, growth):
    return _render_shell_status_column(self, session, continuity, context_frame, provider, growth)
