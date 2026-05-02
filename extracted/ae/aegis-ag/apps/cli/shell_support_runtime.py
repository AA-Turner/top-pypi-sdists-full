"""Support classes and helper functions for the productized shell."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from difflib import unified_diff
import os
from pathlib import Path
import re
import shlex
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

@dataclass(frozen=True, slots=True)
class TranscriptEntry:
    kind: str
    title: str
    body: str
    meta: str = ""

@dataclass(frozen=True, slots=True)
class _PendingFileReview:
    path: Path
    before_text: str | None

@dataclass(frozen=True, slots=True)
class PendingShellCommand:
    command: str

@dataclass(frozen=True, slots=True)
class ShellCommandSpec:
    name: str
    description: str

@dataclass(frozen=True, slots=True)
class SkillSlashSpec:
    command: str
    skill_id: str
    display_name: str
    summary: str
    aliases: tuple[str, ...] = ()
    trigger_phrases: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()

def _skill_metadata_values(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (list, tuple, set)):
        raw_items = tuple(value)
    else:
        text = str(value).strip()
        if not text:
            return ()
        raw_items = tuple(segment.strip() for segment in text.split(","))
    normalized: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        token = str(item).strip().strip("\"'")
        if not token:
            continue
        dedupe_key = token.lower()
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        normalized.append(token)
    return tuple(normalized)

def _normalize_skill_match_text(value: str) -> str:
    normalized = value.strip().lower().replace("/", " ").replace("_", " ").replace("-", " ")
    normalized = re.sub(r"[^\w\s\u4e00-\u9fff]+", " ", normalized)
    return " ".join(normalized.split())

def _skill_phrase_in_message(message: str, phrase: str) -> bool:
    normalized_message = _normalize_skill_match_text(message)
    normalized_phrase = _normalize_skill_match_text(phrase)
    if not normalized_phrase:
        return False
    if re.search(r"[\u4e00-\u9fff]", normalized_phrase):
        return normalized_phrase in normalized_message
    return f" {normalized_phrase} " in f" {normalized_message} "

def _completion(text: str, *, start_position: int, display: str, meta: str = "") -> Completion:
    try:
        return Completion(text, start_position=start_position, display=display, display_meta=meta)
    except TypeError:  # pragma: no cover - fallback signature
        return Completion(text, start_position=start_position, display=display)

class ShellCompleter(Completer):
    def __init__(self, shell: "ProductizedShell") -> None:
        self.shell = shell

    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor
        stripped = text.lstrip()
        if not stripped.startswith("/"):
            return
        words = stripped.split()
        current_word = document.get_word_before_cursor(WORD=True)
        if not words:
            return
        command = words[0]
        if len(words) <= 1 and not text.endswith(" "):
            for spec in self.shell.command_specs:
                if spec.name.startswith(command):
                    yield _completion(
                        spec.name,
                        start_position=-len(current_word),
                        display=spec.name,
                        meta=spec.description,
                    )
            return

        if command == "/resume":
            candidates = (
                ("latest", "Resume the latest Aegis clone"),
                *tuple((clone_id, "Resume the latest session for a clone") for clone_id in self.shell.recent_clone_ids()),
            ) + tuple(
                (session_id, "Resume a known session")
                for session_id in self.shell.recent_session_ids()
            )
        elif command == "/profile":
            if len(words) >= 2 and words[1] == "charter":
                candidates = (
                    ("show", "Inspect the current profile charter extension"),
                    ("set", "Replace the current profile charter extension"),
                    ("clear", "Clear the current profile charter extension"),
                )
            elif len(words) >= 2 and words[1] in {"preset", "personality"}:
                candidates = tuple(
                    (preset_id, description)
                    for preset_id, description in self.shell.personality_preset_choices()
                )
            elif len(words) >= 2 and words[1] == "user":
                candidates = (
                    ("show", "Inspect the current shared user state"),
                    ("set", "Replace the current shared user state"),
                    ("append", "Append durable shared user facts"),
                    ("clear", "Clear the current shared user state"),
                )
            elif len(words) >= 2 and words[1] == "relationship":
                candidates = (
                    ("show", "Inspect the current clone-local relationship continuity"),
                    ("set", "Replace the current relationship continuity notes"),
                    ("append", "Append clone-local continuity notes"),
                    ("clear", "Clear the current relationship continuity notes"),
                )
            elif len(words) == 2 and text.endswith(" "):
                candidates = (
                    ("inspect", "Show current identity, user, and relationship state"),
                    ("set-name", "Rename the active clone"),
                    ("charter", "Show, set, or clear the profile charter extension"),
                    ("initiative", "Tune proactive initiative"),
                    ("preset", "Choose a personality preset"),
                    ("user", "Inspect or patch shared user truth"),
                    ("relationship", "Inspect or patch clone-local continuity"),
                )
            else:
                candidates = (
                    ("inspect", "Show current identity, user, and relationship state"),
                    ("set-name", "Rename the active clone"),
                    ("charter", "Show, set, or clear the profile charter extension"),
                    ("initiative", "Tune proactive initiative"),
                    ("preset", "Choose a personality preset"),
                    ("user", "Inspect or patch shared user truth"),
                    ("relationship", "Inspect or patch clone-local continuity"),
                )
        elif command == "/activity":
            candidates = (
                ("inspect", "Inspect one durable work item"),
                ("create", "Create a durable work item"),
                ("focus", "Focus one durable work item"),
                ("drop", "Drop one durable work item"),
            )
        elif command == "/audit":
            candidates = (
                ("inspect", "Inspect current recall, work, and procedure overlays"),
                ("prompt", "Inspect the rendered prompt envelope"),
            )
        elif command == "/tools":
            candidates = (
                ("inspect", "Show metadata for one tool"),
                ("enable", "Enable a tool for this clone"),
                ("disable", "Disable a tool for this clone"),
                ("install", "Load a tool manifest into this clone"),
                ("run", "Run a tool with explicit key=value arguments"),
            )
        elif command == "/skills":
            candidates = (
                ("list", "List discoverable skill packages from local shelves"),
                ("active", "Show currently active installed skills"),
                ("search", "Search installable skill packages from local shelves"),
                ("view", "Load one skill package and show its instructions"),
                ("inspect", "Alias for view"),
                ("enable", "Enable a skill for this clone"),
                ("disable", "Disable a skill for this clone"),
                ("install", "Install a skill package or manifest into this clone"),
            )
        elif command == "/providers":
            candidates = (
                ("configure", "Choose a provider, endpoint, key, model, and context window"),
                ("status", "Show the active provider configuration"),
                ("list", "List supported provider catalogs"),
            )
        elif command == "/models":
            candidates = (
                ("configure", "Choose the active model and context window"),
                ("status", "Show the active model configuration"),
                ("list", "List models exposed by the active provider endpoint"),
            )
        elif command == "/cron":
            candidates = (
                ("create", "Create a scheduled greeting, web search, or prompt"),
                ("inspect", "Show one cron job"),
                ("pause", "Pause a cron job"),
                ("resume", "Resume a paused cron job"),
                ("remove", "Remove a cron job"),
            )
        else:
            return

        for value, description in candidates:
            if value.startswith(current_word):
                yield _completion(
                    value,
                    start_position=-len(current_word),
                    display=value,
                    meta=description,
                )

__all__ = [
    "TranscriptEntry",
    "_PendingFileReview",
    "PendingShellCommand",
    "ShellCommandSpec",
    "SkillSlashSpec",
    "_skill_metadata_values",
    "_normalize_skill_match_text",
    "_skill_phrase_in_message",
    "_completion",
    "ShellCompleter",
]
