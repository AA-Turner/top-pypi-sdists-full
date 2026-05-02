"""Bound methods extracted from apps/cli/shell.py."""

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

def _dispatch(self, raw_command: str) -> bool:
    command = raw_command.strip()
    if not command:
        return False
    if self._pending_context_compaction_frame is not None:
        self._pending_context_compaction_frame = None
        self._pending_context_compaction_frame_rendered = False
        self._refresh_shell_frame()
    if command.startswith("/"):
        self._clear_composer(command)
        return self._handle_slash_command(command)
    self._clear_composer(command)
    self._append_entry("user", "You", command)
    self._render_pending_entries()
    if self._handle_conversational_surface_request(command):
        self._refresh_shell_frame_if_needed()
        return False
    try:
        if self.debug:
            self._append_entry(
                "status",
                "Runtime",
                "\n".join(
                    [
                        f"session_id: {self.session_id}",
                        "mode: shared-runtime",
                        "trace: debug diagnostics enabled",
                    ]
                ),
            )
            self._render_pending_entries()
        skill_route = self._resolved_skill_route(command)
        event_payload = None
        if skill_route is not None:
            spec, route_mode = skill_route
            event_payload = {
                "skill_route": spec.skill_id,
                "skill_route_mode": route_mode,
            }
        outcome = self._run_turn_with_progress(command, event_payload=event_payload)
    except Exception as error:  # pragma: no cover - defensive shell surface
        self._append_entry(
            "recovery",
            "Turn failed",
            f"{error}\nstatus: /status",
        )
        return False
    context_prompt_tokens = self._last_prompt_tokens
    self._append_outcome(outcome)
    self._last_provider_prompt_tokens = outcome.execution.prompt_tokens
    self._last_prompt_tokens = context_prompt_tokens
    growth_update = self._show_growth_celebration_if_needed()
    self._append_growth_update_message(growth_update)
    if getattr(growth_update, "stage_changed", False):
        self._refresh_shell_frame()
    else:
        self._refresh_shell_frame_if_needed()
    return False

def _handle_conversational_surface_request(self, message: str) -> bool:
    normalized = message.strip().lower().rstrip("?.!")
    if normalized in {
        "what tools do you have",
        "which tools do you have",
        "show tools",
        "list tools",
    }:
        tools = tuple(
            tool
            for tool in self.runtime.tool_catalog(session_id=self.session_id, audience="model")
            if tool.enabled and tool.available
        )
        lines = [
            "I can use these tools right now:",
            *[
                f"- {tool.display_name} ({tool.tool_id}): {tool.description}"
                for tool in tools
            ],
            "",
            "Ask me naturally if you want one used, or give me a manifest path if you want me to install an external tool.",
        ]
        self._append_assistant_surface_reply("\n".join(lines))
        return True
    if normalized in {
        "what cron jobs do you have",
        "which cron jobs do you have",
        "show cron jobs",
        "list cron jobs",
        "show schedules",
        "list schedules",
    }:
        jobs = self.runtime.cron_jobs(session_id=self.session_id)
        if jobs:
            body = "\n".join(
                [
                    "These scheduled jobs are active for this clone:",
                    *[
                        f"- {job.name} ({job.job_id}) · {job.status} · {job.schedule_text} · {job.action_kind}"
                        for job in jobs
                    ],
                ]
            )
        else:
            body = "I don't have any scheduled jobs running for this clone yet."
        self._append_assistant_surface_reply(body)
        return True
    tool_match = re.match(r"(?i)^(install|add|load)\s+tools?\s+(.+)$", message.strip())
    if tool_match is not None:
        reference = self._strip_wrapping_quotes(tool_match.group(2).strip())
        try:
            record = self.runtime.install_tool_manifest(reference, session_id=self.session_id)
        except Exception as error:
            self._append_assistant_surface_reply(
                "I couldn't install that tool manifest yet.\n"
                f"reason: {error}\n"
                "Right now external tools install from a local manifest path.",
            )
            return True
        self._append_assistant_surface_reply(
            "\n".join(
                [
                    "I installed that tool manifest for this clone.",
                    f"- source: {record.source_path}",
                    f"- tools: {', '.join(record.tool_ids) or '<empty>'}",
                    f"- executable: {', '.join(record.executable_tool_ids) or '<empty>'}",
                ]
            )
        )
        return True
    cron_greeting = re.match(
        r"(?is)^(?:schedule|create|set up)\s+(?:a\s+)?greeting(?:\s+job)?(?:\s+to\s+say\s+(.+?))?\s+(every .+|daily at .+|\d+[mhd])$",
        message.strip(),
    )
    if cron_greeting is not None:
        message_text = self._strip_wrapping_quotes((cron_greeting.group(1) or "").strip())
        schedule = cron_greeting.group(2).strip()
        arguments = [f'schedule="{schedule}"', "kind=greeting"]
        if message_text:
            arguments.append(f'message="{message_text}"')
            arguments.append(f'name="Greeting · {schedule}"')
        else:
            arguments.append(f'name="Greeting · {schedule}"')
        try:
            payload = self._parse_named_arguments(arguments)
            job = self.runtime.create_cron_job(
                session_id=self.session_id,
                name=payload.get("name", f"Greeting · {schedule}"),
                schedule=payload["schedule"],
                action_kind=payload["kind"],
                payload={"message": payload.get("message", "")},
            )
        except Exception as error:
            self._append_assistant_surface_reply(f"I couldn't create that scheduled greeting yet.\nreason: {error}")
            return True
        self._append_assistant_surface_reply(
            f"I scheduled that greeting for this clone.\n- {job.name} · {job.schedule_text} · {job.action_kind}"
        )
        return True
    cron_search = re.match(
        r"(?is)^(?:schedule|create|set up)\s+(?:a\s+)?(?:web\s+search|search)(?:\s+job)?\s+(?:for\s+)?(.+?)\s+(every .+|daily at .+|\d+[mhd])$",
        message.strip(),
    )
    if cron_search is not None:
        query = self._strip_wrapping_quotes(cron_search.group(1).strip())
        schedule = cron_search.group(2).strip()
        try:
            job = self.runtime.create_cron_job(
                session_id=self.session_id,
                name=f"Web search · {query[:32]}",
                schedule=schedule,
                action_kind="web_search",
                payload={"query": query},
            )
        except Exception as error:
            self._append_assistant_surface_reply(f"I couldn't create that scheduled web search yet.\nreason: {error}")
            return True
        self._append_assistant_surface_reply(
            f"I scheduled that web search for this clone.\n- {job.name} · {job.schedule_text} · {job.action_kind}"
        )
        return True
    webpage_url = self._requested_webpage_url(message)
    if webpage_url is not None:
        try:
            result = self._run_tool_with_progress("tool.web.read", {"url": webpage_url})
        except Exception as error:
            self._append_assistant_surface_reply(
                f"I couldn't fetch that web page yet.\nreason: {error}",
                meta=webpage_url,
            )
            return True
        self._append_assistant_surface_reply(
            f"I opened that page and pulled the readable content:\n{result.summary}",
            meta=webpage_url,
        )
        return True
    return False

def _handle_slash_command(self, raw_command: str) -> bool:
    try:
        parts = self._parse_slash_command(raw_command)
    except ValueError as error:
        self._append_entry("recovery", "Command parse error", str(error))
        return False
    command = parts[0]
    args = parts[1:]

    if command == "/exit":
        self._append_entry("notice", "Wake surface", f"Leaving session {self.session_id}.")
        return True
    if command == "/help":
        self._append_help()
        return False
    if command == "/status":
        self._append_status()
        return False
    if command == "/resume":
        self._resume_session(args[0] if args else "latest")
        return False
    if command == "/profile":
        self._append_profile(args)
        return False
    if command == "/activity":
        self._append_work(args)
        return False
    if command == "/memory":
        self._append_memory(args)
        return False
    if command == "/procedure":
        self._append_procedure(args)
        return False
    if command == "/audit":
        self._append_audit(args)
        return False
    if command == "/frozen":
        self._append_frozen()
        return False
    if command == "/tools":
        self._append_tools(args)
        return False
    if command == "/skills":
        self._append_skills(args)
        return False
    if command == "/cron":
        self._append_cron(args)
        return False
    if command == "/providers":
        self._append_providers(args)
        return False
    if command == "/models":
        self._append_models(args)
        return False
    if command == "/clear":
        previous_session_id = self.session_id
        resumed = self.runtime.resume(previous_session_id).session
        self.session_id = resumed.session_id
        self.opened = f"Opened thread {self.runtime.clone_id_for_session(resumed)}"
        self.transcript.clear()
        self._pending_commands.clear()
        self._prime_transcript(use_proactive_opening=True)
        self._refresh_shell_frame()
        return False

    if self._dispatch_skill_slash_command(raw_command, command, args):
        return False

    self._append_entry("command", "Unknown command", f"{command}\nhelp: /help")
    return False

def _parse_slash_command(self, raw_command: str) -> list[str]:
    try:
        return shlex.split(raw_command)
    except ValueError:
        fallback = self._text_surface_fallback_parts(raw_command)
        if fallback is not None:
            return fallback
        raise

def _text_surface_fallback_parts(self, raw_command: str) -> list[str] | None:
    stripped = raw_command.strip()
    for prefix in ("/profile charter set ", "/profile user set ", "/profile user append ", "/profile relationship set ", "/profile relationship append "):
        if stripped.startswith(prefix):
            command, subcommand, action, remainder = stripped.split(" ", 3)
            remainder = remainder.strip()
            if remainder:
                return [command, subcommand, action, remainder]
            return [command, subcommand, action]
    return None
