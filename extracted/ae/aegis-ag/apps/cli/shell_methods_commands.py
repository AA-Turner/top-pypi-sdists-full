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
    build_procedure_operator_surface,
    build_activity_operator_surface,
    render_audit_lines,
    render_memory_lines,
    render_procedure_lines,
    render_profile_lines,
    render_activity_lines,
)
from packages.tools.handler_support import resolve_workspace_path
from .provider_flow import provider_setup_defaults, run_provider_selection_wizard
from .runtime import CliRuntime
from .shell_progress_support import outcome_intent_meta
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

def _append_help(self) -> None:
    lines = [
        "Stay in the conversation. Slash commands exist only for orientation and control.",
        "",
        "/status - refresh session, provider, and growth posture",
        "/resume latest|<clone-id>|<session-id> - re-enter a clone or jump to a known session",
        "/profile [inspect|set-name|initiative|preset|charter|user|relationship] - inspect or patch owner-aligned profile state",
        "/activity [inspect|create|focus|drop] - inspect or mutate owner-aligned activity state",
        "/memory [list|inspect|search|lineage|correct|pin|unpin|delete] - inspect or govern durable evidence",
        "/procedure [list|inspect|patch|retire] - inspect or govern promoted procedures",
        "/audit - inspect the current context, recall reasons, and procedure overlays",
        "/tools [inspect|enable|disable|install|run] - govern built-ins and manifest-backed tools",
        "/skills [list|active|search|view|enable|disable|install] - discover, inspect, and govern skill packages",
        "/cron [create|inspect|pause|resume|remove] - govern built-in scheduled jobs",
        "/providers [configure|status|list] - switch provider, endpoint, and encrypted key",
        "/models [configure|status|list] - switch model and context window",
        "/clear - reset the transcript and replay the opening reply",
        "/exit - leave the wake surface",
        "",
        "Use /skills to inspect installed skills, search shelves, or view one skill package before invoking it.",
        "Examples: /skills active · /skills search notes · /skills view apple-notes",
        "",
        'Clone management stays in the CLI: aegis clone <name> --initial-goal "..."',
        "Clone inventory and retirement stay in the CLI: aegis clones / aegis clones bye <name>",
        "",
        "Tip: type / and keep typing to open the command palette.",
    ]
    self._append_entry("notice", "Command palette", "\n".join(lines))


def _append_tools(self, args: list[str]) -> None:
    command = args[0] if args else "list"
    if command in {"list", "ls"}:
        tools = self.runtime.tool_catalog(session_id=self.session_id)
        lines = [
            (
                f"{tool.tool_id} | enabled={tool.enabled} | available={tool.available} | "
                f"family={tool.family} | audience={tool.audience} | {tool.display_name} | {tool.description}"
            )
            for tool in tools
        ] or ["<empty>"]
        lines.extend(
            [
                "",
                "inspect: /tools inspect <tool-id>",
                "enable: /tools enable <tool-id>",
                "disable: /tools disable <tool-id>",
                "install: /tools install </path/to/tools.json>",
                'run terminal: /tools run tool.terminal.exec command="pwd"',
                'run search: /tools run tool.file.search query="aegis"',
                'run web: /tools run tool.web.search query="agentic intelligence"',
                'read page: /tools run tool.web.read url="https://example.com"',
                'inspect profile: /tools run tool.profile.manage action=inspect',
                'run recall: /tools run tool.memory.recall query="next step"',
                'pin memory: /tools run tool.memory.upload action=pin memory_id="memory:..."',
                'inspect procedures: /tools run tool.procedure.inspect action=list',
                'manage cron: /tools run tool.cron.manage action=list',
            ]
        )
        self._append_entry("notice", "Tools", "\n".join(lines))
        return
    if command == "inspect":
        if len(args) < 2:
            self._append_entry("recovery", "Tools", "Usage: /tools inspect <tool-id>")
            return
        tool = self.runtime.inspect_tool(args[1], session_id=self.session_id)
        self._append_entry(
            "status",
            "Tool",
            "\n".join(
                [
                    f"tool_id: {tool.tool_id}",
                    f"display_name: {tool.display_name}",
                    f"enabled: {tool.enabled}",
                    f"available: {tool.available}",
                    f"availability_reason: {tool.availability.reason or '<none>'}",
                    f"version: {tool.version}",
                    f"family: {tool.family}",
                    f"audience: {tool.audience}",
                    f"backend: {tool.backend or '<none>'}",
                    f"description: {tool.description}",
                    f"categories: {', '.join(tool.side_effects.categories) or '<none>'}",
                    f"approval_class: {tool.side_effects.approval_class}",
                    f"risk_class: {tool.side_effects.risk_class}",
                    f"provenance: {tool.provenance or 'built-in'}",
                ]
            ),
        )
        return
    if command in {"enable", "disable"}:
        if len(args) < 2:
            self._append_entry("recovery", "Tools", f"Usage: /tools {command} <tool-id>")
            return
        updated = self.runtime.set_tool_enabled(
            args[1],
            command == "enable",
            session_id=self.session_id,
        )
        self._append_entry("status", "Tool updated", f"{updated.tool_id}\nenabled: {updated.enabled}")
        return
    if command == "install":
        if len(args) < 2:
            self._append_entry("recovery", "Tools", "Usage: /tools install </path/to/tools.json>")
            return
        try:
            record = self.runtime.install_tool_manifest(args[1], session_id=self.session_id)
        except Exception as error:
            self._append_entry("recovery", "Tools", str(error))
            return
        self._append_entry(
            "status",
            "Tool manifest installed",
            "\n".join(
                [
                    f"source_path: {record.source_path}",
                    f"tool_ids: {', '.join(record.tool_ids) or '<empty>'}",
                    f"executable_tool_ids: {', '.join(record.executable_tool_ids) or '<empty>'}",
                ]
            ),
        )
        return
    if command == "run":
        if len(args) < 2:
            self._append_entry("recovery", "Tools", "Usage: /tools run <tool-id> key=value ...")
            return
        try:
            arguments = self._parse_named_arguments(args[2:])
        except ValueError as error:
            self._append_entry("recovery", "Tools", str(error))
            return
        try:
            result = self._run_tool_with_progress(args[1], arguments)
        except Exception as error:
            self._append_entry("recovery", "Tool result", str(error), meta=args[1])
            return
        self._append_entry(
            "assistant" if result.outcome == "success" else "recovery",
            "Tool result",
            result.summary,
            meta=f"{args[1]} · outcome={result.outcome}",
        )
        return
    self._append_entry("recovery", "Tools", "Usage: /tools [inspect|enable|disable|install|run]")

def _append_skills(self, args: list[str]) -> None:
    command = args[0] if args else "list"
    if command in {"list", "ls"}:
        entries = self.runtime.list_skill_hub(limit=24)
        lines = [
            f"{_display_skill_reference(entry)} | {entry.display_name} | source={entry.source_id} | {entry.summary}"
            for entry in entries
        ] or ["<empty>"]
        lines.extend(
            [
                "",
                "active installed skills: /skills active",
                "search external sources: /skills search <query>",
                "view local or remote: /skills view <skill-id|reference>",
                "enable: /skills enable <skill-id>",
                "disable: /skills disable <skill-id>",
                "install from source: /skills install <skill-id|reference>",
                "install from path: /skills install </path/to/skill-or-skills.json>",
            ]
        )
        self._append_entry("notice", "Skills", "\n".join(lines))
        return
    if command == "active":
        skills = self.runtime.skill_catalog(session_id=self.session_id)
        lines = [
            f"{skill.skill_id} | enabled={skill.enabled} | {skill.display_name} | {skill.summary}"
            for skill in skills
            if skill.enabled
        ] or ["<empty>"]
        self._append_entry("notice", "Active skills", "\n".join(lines))
        return
    if command == "search":
        if len(args) < 2:
            self._append_entry("recovery", "Skills", "Usage: /skills search <query>")
            return
        query = " ".join(args[1:]).strip()
        local_entries = self.runtime.search_skill_hub(query, limit=12)
        external_entries = self.runtime.search_skill_sources(query, limit=12)
        lines: list[str] = []
        if local_entries:
            lines.append("local shelves:")
            lines.extend(
                f"- {_display_skill_reference(entry)} | {entry.display_name} | source={entry.source_id} | {entry.summary}"
                for entry in local_entries
            )
        if external_entries:
            if lines:
                lines.append("")
            lines.append("external sources:")
            lines.extend(
                f"- {entry.reference} | {entry.display_name} | source={entry.source_id} | trust={entry.trust_level or '<unknown>'} | {entry.summary}"
                for entry in external_entries
            )
        if not lines:
            lines.append("<empty>")
        lines.extend(
            [
                "",
                "install one: /skills install <skill-id|reference>",
                "view one: /skills view <skill-id|reference>",
            ]
        )
        self._append_entry("notice", "Skill search", "\n".join(lines))
        return
    if command in {"inspect", "view"}:
        if len(args) < 2:
            self._append_entry("recovery", "Skills", "Usage: /skills view <skill-id|reference>")
            return
        try:
            skill = self.runtime.inspect_skill(args[1], session_id=self.session_id)
        except Exception as error:
            self._append_entry("recovery", "Skills", str(error))
            return
        lines = [
            f"skill_id: {skill.skill_id}",
            f"display_name: {skill.display_name}",
            f"enabled: {skill.enabled}",
            f"version: {skill.version}",
            f"summary: {skill.summary}",
            f"provenance: {skill.provenance or 'built-in'}",
        ]
        installed = skill.metadata.get("installed")
        if isinstance(installed, bool):
            lines.append(f"installed: {installed}")
        slash_command = str(skill.metadata.get("slash_command") or "").strip()
        if slash_command:
            lines.append(f"slash_command: /{slash_command}")
        if skill.instruction_text.strip():
            lines.extend(["", skill.instruction_text.strip()])
        self._append_entry(
            "status",
            "Skill",
            "\n".join(lines),
        )
        return
    if command in {"enable", "disable"}:
        if len(args) < 2:
            self._append_entry("recovery", "Skills", f"Usage: /skills {command} <skill-id>")
            return
        try:
            updated = self.runtime.set_skill_enabled(
                args[1],
                command == "enable",
                session_id=self.session_id,
            )
        except Exception as error:
            self._append_entry("recovery", "Skills", str(error))
            return
        self._append_entry("status", "Skill updated", f"{updated.skill_id}\nenabled: {updated.enabled}")
        return
    if command == "install":
        if len(args) < 2:
            self._append_entry("recovery", "Skills", "Usage: /skills install <skill-id|/path/to/skill|/path/to/skills.json>")
            return
        try:
            result = self.runtime.install_skill_source(args[1], session_id=self.session_id)
        except Exception as error:
            self._append_entry("recovery", "Skills", str(error))
            return
        self._append_entry(
            "status",
            "Skill installed",
            "\n".join(
                [
                    f"source_path: {result.source_path}",
                    f"skill_ids: {', '.join(result.skill_ids) or '<empty>'}",
                    f"status: {result.status}",
                ]
            ),
        )
        self._refresh_skill_slash_specs()
        return
    self._append_entry("recovery", "Skills", "Usage: /skills [list|active|search|view|enable|disable|install]")


def _display_skill_reference(entry) -> str:
    if getattr(entry, "source_id", "") == "builtin":
        return str(getattr(entry, "skill_id", "")).strip() or str(getattr(entry, "reference", ""))
    return str(getattr(entry, "reference", "")).strip()

def _append_cron(self, args: list[str]) -> None:
    command = args[0] if args else "list"
    if command in {"list", "ls"}:
        jobs = self.runtime.cron_jobs(session_id=self.session_id)
        lines = [
            f"{job.job_id} | {job.status} | {job.name} | {job.schedule_text} | {job.action_kind}"
            for job in jobs
        ] or ["<empty>"]
        lines.extend(
            [
                "",
                'create greeting: /cron create name="Morning hello" schedule="every morning" kind=greeting message="Good morning."',
                'create web search: /cron create name="Web check" schedule="every 2h" kind=web_search query="agentic ai news"',
                "inspect: /cron inspect <job-id>",
                "pause: /cron pause <job-id>",
                "resume: /cron resume <job-id>",
                "remove: /cron remove <job-id>",
            ]
        )
        self._append_entry("notice", "Cron jobs", "\n".join(lines))
        return
    if command == "create":
        try:
            arguments = self._parse_named_arguments(args[1:])
        except ValueError as error:
            self._append_entry("recovery", "Cron jobs", str(error))
            return
        schedule = arguments.get("schedule", "").strip()
        action_kind = arguments.get("kind", "").strip()
        if not schedule or not action_kind:
            self._append_entry(
                "recovery",
                "Cron jobs",
                "Usage: /cron create name=<name> schedule=<schedule> kind=greeting|web_search|prompt [message=...] [query=...] [prompt=...]",
            )
            return
        payload = {
            key: value
            for key, value in (
                ("message", arguments.get("message")),
                ("query", arguments.get("query")),
                ("prompt", arguments.get("prompt")),
            )
            if value
        }
        name = arguments.get("name", "").strip() or f"Cron · {action_kind}"
        try:
            job = self.runtime.create_cron_job(
                session_id=self.session_id,
                name=name,
                schedule=schedule,
                action_kind=action_kind,
                payload=payload,
            )
        except Exception as error:
            self._append_entry("recovery", "Cron jobs", str(error))
            return
        self._append_entry(
            "status",
            "Cron job created",
            "\n".join(
                [
                    f"job_id: {job.job_id}",
                    f"name: {job.name}",
                    f"schedule: {job.schedule_text}",
                    f"action_kind: {job.action_kind}",
                    f"next_run_at: {job.next_run_at.isoformat() if job.next_run_at is not None else '<none>'}",
                ]
            ),
        )
        return
    if command == "inspect":
        if len(args) < 2:
            self._append_entry("recovery", "Cron jobs", "Usage: /cron inspect <job-id>")
            return
        try:
            job = self.runtime.inspect_cron_job(args[1])
        except Exception as error:
            self._append_entry("recovery", "Cron jobs", str(error))
            return
        self._append_entry(
            "status",
            "Cron job",
            "\n".join(
                [
                    f"job_id: {job.job_id}",
                    f"name: {job.name}",
                    f"status: {job.status}",
                    f"schedule: {job.schedule_text}",
                    f"action_kind: {job.action_kind}",
                    f"last_summary: {job.last_summary or '<none>'}",
                ]
            ),
        )
        return
    if command in {"pause", "resume", "remove"}:
        if len(args) < 2:
            self._append_entry("recovery", "Cron jobs", f"Usage: /cron {command} <job-id>")
            return
        try:
            if command == "pause":
                job = self.runtime.pause_cron_job(args[1])
            elif command == "resume":
                job = self.runtime.resume_cron_job(args[1])
            else:
                job = self.runtime.remove_cron_job(args[1])
        except Exception as error:
            self._append_entry("recovery", "Cron jobs", str(error))
            return
        self._append_entry(
            "status",
            "Cron job updated",
            "\n".join(
                [
                    f"job_id: {job.job_id}",
                    f"name: {job.name}",
                    f"status: {'removed' if command == 'remove' else job.status}",
                ]
            ),
        )
        return
    self._append_entry("recovery", "Cron jobs", "Usage: /cron [create|inspect|pause|resume|remove]")

def _parse_named_arguments(self, args: list[str]) -> dict[str, str]:
    payload: dict[str, str] = {}
    for item in args:
        if "=" not in item:
            raise ValueError("tool arguments must be key=value pairs")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError("tool argument keys must not be empty")
        payload[key] = self._strip_wrapping_quotes(value.strip())
    return payload

def _requested_webpage_url(self, message: str) -> str | None:
    lowered = message.strip().lower()
    match = WEB_URL_PATTERN.search(message)
    if match is None:
        return None
    if not any(
        phrase in lowered
        for phrase in (
            "read ",
            "open ",
            "fetch ",
            "visit ",
            "browse ",
            "look at ",
            "check ",
            "web page",
            "website",
            " url",
        )
    ):
        return None
    return match.group(1).rstrip(").,!?\"'")

def _strip_wrapping_quotes(self, value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1].strip()
    return value

def _append_status(self) -> None:
    session = self.runtime.inspect_session(self.session_id)
    provider = dict(self.runtime.provider_summary())
    continuity = self.runtime.inspect_continuity(session_id=self.session_id)
    growth = self.runtime.inspect_growth(session_id=self.session_id)
    provider_doctor = self.runtime.provider_doctor()
    voice_doctor = self.runtime.voice_doctor(profile_id=session.profile_id)
    security_doctor = self.runtime.security_doctor()
    try:
        wake_outcome = self.runtime.wake(self.session_id, inspect_only=True)
    except Exception:
        wake_lines = [
            "wake_mode: foreground",
            f"wake_selected_kind: {continuity.wake_action}",
            "wake_selected_goal_id: <none>",
            f"wake_rationale: {continuity.wake_summary}",
            "wake_planned_active_goal_id: <none>",
        ]
    else:
        wake_lines = [
            f"wake_mode: {wake_outcome.decision.mode}",
            f"wake_selected_kind: {wake_outcome.decision.selected_move.kind}",
            f"wake_selected_goal_id: {wake_outcome.decision.selected_move.goal_id or '<none>'}",
            f"wake_rationale: {wake_outcome.decision.rationale.summary}",
            f"wake_planned_active_goal_id: {wake_outcome.planned_goal_graph.active_goal_id or '<none>'}",
            f"wake_reconciliation: {wake_outcome.reconciliation.summary}",
        ]
    lines = [
        f"session_id: {session.session_id}",
        f"clone_id: {self.runtime.clone_id_for_session(session)}",
        f"status: {session.status}",
        f"provider_id: {provider.get('provider_id', '<unset>')}",
        f"provider_source: {provider.get('source', '<unknown>')}",
        f"provider_strong_model: {provider.get('strong_model') or '<unset>'}",
        f"provider_weak_model: {provider.get('weak_model') or '<unset>'}",
        f"provider_intent_mode: {provider.get('intent_mode') or '<unset>'}",
        f"provider_context_window: {provider.get('context_window_tokens') or '<unset>'}",
        f"provider_secret_status: {provider.get('secret_status', '<unknown>')}",
        f"provider_status: {provider_doctor['status']}",
        f"voice_status: {voice_doctor['status']}",
        f"security_status: {security_doctor['status']}",
        *wake_lines,
        f"growth_action: {continuity.wake_action}",
        f"growth_summary: {continuity.wake_summary}",
        f"progression_title: {growth.stage_title}",
        f"progression_cycle: {growth.cycle_label}",
        f"progression_level: Lv.{growth.ascension_level}",
        f"progression_power: {growth.power_score}",
        f"progression_progress: {growth.progress_percent}%",
        f"progression_next: {growth.next_milestone}",
        f"progression_momentum: {growth.momentum_state}",
        f"progression_path: {growth.dominant_archetype}",
        f"progression_proof: {growth.proof_state}",
        (
            "progression_lifetime: "
            f"dialogues={growth.canonical_dialogues} "
            f"tokens={growth.state.total_tokens} "
            f"experiences={growth.canonical_experiences} "
            f"promoted={growth.canonical_promoted_procedures} "
            f"active_days={growth.canonical_active_days}"
        ),
    ]
    if growth.active_challenge_tracks:
        lines.append(f"progression_challenge: {growth.active_challenge_tracks[0].summary}")
    for check in provider_doctor["checks"]:
        summary = f" | {check['summary']}" if check.get("summary") else ""
        lines.append(f"provider/{check['check']}: {check['status']}{summary}")
    for check in voice_doctor["checks"]:
        summary = f" | {check['summary']}" if check.get("summary") else ""
        lines.append(f"voice/{check['check']}: {check['status']}{summary}")
    for check in security_doctor["checks"]:
        summary = f" | {check['summary']}" if check.get("summary") else ""
        lines.append(f"security/{check['check']}: {check['status']}{summary}")
    experiences = self.runtime.inspect_experiences(session_id=self.session_id, limit=2)
    displayable = self._displayable_experiences(experiences)
    if displayable:
        lines.append(f"latest_learning: {self._format_experience_status(displayable[0])}")
    else:
        lines.append("latest_learning: no captured experience yet")
    if provider_doctor["status"] != "ready":
        lines.append("next: exit and run aegis init")
    else:
        lines.append("next: keep talking")
    self._append_entry("status", "Clone status", "\n".join(lines))

def _append_profile(self, args: list[str]) -> None:
    action = args[0] if args else "inspect"
    if action in {"inspect", "show"}:
        surface = self.runtime.inspect_profile_surface(self.session_id)
        lines = list(render_profile_lines(surface))
        lines.extend(
            [
                "",
                "set name: /profile set-name <display-name>",
                "initiative: /profile initiative <value>",
                "preset: /profile preset <preset-id>",
                "charter: /profile charter show|set|clear",
                "user: /profile user show|set|append|clear",
                "relationship: /profile relationship show|set|append|clear",
            ]
        )
        self._append_entry("notice", "Profile", "\n".join(lines))
        return
    if action in {"set-name", "name"}:
        if len(args) < 2:
            self._append_entry("recovery", "Profile", "Usage: /profile set-name <display-name>")
            return
        surface = self.runtime.patch_profile_surface(self.session_id, {"display_name": " ".join(args[1:]).strip()})
        self._append_entry("notice", "Profile updated", "\n".join(render_profile_lines(surface)))
        return
    if action == "initiative":
        if len(args) != 2:
            self._append_entry("recovery", "Profile", "Usage: /profile initiative <value>")
            return
        surface = self.runtime.patch_profile_surface(self.session_id, {"initiative": args[1]})
        self._append_entry("notice", "Profile updated", "\n".join(render_profile_lines(surface)))
        return
    if action in {"preset", "personality"}:
        if len(args) != 2:
            self._append_entry("recovery", "Profile", "Usage: /profile preset <preset-id>")
            return
        surface = self.runtime.patch_profile_surface(self.session_id, {"personality_preset": args[1]})
        self._append_entry("notice", "Profile updated", "\n".join(render_profile_lines(surface)))
        return
    if action == "charter":
        self._append_identity_charter(self.session_id, args[1:], alias_label="Profile charter")
        return
    if action == "user":
        self._append_user(args[1:], alias_title="Profile / user")
        return
    if action == "relationship":
        self._append_relationship(args[1:])
        return
    self._append_entry("recovery", "Profile", "Usage: /profile [inspect|set-name|initiative|preset|charter|user|relationship]")

def _append_work(self, args: list[str]) -> None:
    action = args[0] if args else "inspect"
    continuity = self.runtime.inspect_continuity(session_id=self.session_id)
    graph = self.runtime.repository.load_activity_graph(self.session_id)
    surface = build_activity_operator_surface(
        session_id=self.session_id,
        active_goal_id=graph.active_goal_id if graph is not None else None,
        active_goal_reason=continuity.wake_summary,
        wake_action=continuity.wake_action,
        wake_factors=continuity.wake_factors,
        goal_graph_revision=graph.revision_id if graph is not None else None,
        goals=graph.goals if graph is not None else (),
    )
    if action in {"inspect", "show", "list", "ls"} and len(args) <= 1:
        lines = list(render_activity_lines(surface))
        lines.extend(
            [
                "",
                "create: /activity create <title>",
                "inspect: /activity inspect <goal-id>",
                "focus: /activity focus <goal-id>",
                "drop: /activity drop <goal-id>",
            ]
        )
        self._append_entry("notice", "Work", "\n".join(lines))
        return
    if action == "inspect":
        if len(args) < 2:
            self._append_entry("recovery", "Work", "Usage: /activity inspect <goal-id>")
            return
        goal = self.runtime.inspect_goal(self.session_id, args[1])
        lines = [
            f"id: {goal.goal_id}",
            f"title: {goal.title}",
            f"status: {goal.status}",
            f"priority: {goal.priority}",
            f"owner: {goal.owner or 'none'}",
            f"parent: {goal.parent_goal_id or 'none'}",
            f"dependencies: {', '.join(goal.dependencies) or 'none'}",
            f"evidence: {', '.join(goal.evidence_refs) or 'none'}",
        ]
        self._append_entry("notice", "Activity item", "\n".join(lines))
        return
    if action == "create":
        title = " ".join(args[1:]).strip()
        if not title:
            self._append_entry("recovery", "Work", "Usage: /activity create <title>")
            return
        goal = self.runtime.create_goal(self.session_id, title=title)
        self._append_entry("notice", "Activity item created", f"{goal.goal_id} | {goal.status} | {goal.priority} | {goal.title}")
        return
    if action == "focus":
        if len(args) < 2:
            self._append_entry("recovery", "Work", "Usage: /activity focus <goal-id>")
            return
        _, updated, reason = self.runtime.update_goal(self.session_id, args[1], status="active", reason="work focused from /activity surface")
        self._append_entry("notice", "Activity item focused", f"{reason}: {updated.goal_id} | {updated.status} | {updated.priority} | {updated.title}")
        return
    if action in {"drop", "delete"}:
        if len(args) < 2:
            self._append_entry("recovery", "Work", "Usage: /activity drop <goal-id>")
            return
        _, updated = self.runtime.delete_goal(self.session_id, args[1], reason="work dropped from /activity surface")
        self._append_entry("notice", "Activity item dropped", f"{updated.goal_id} | {updated.status} | {updated.priority} | {updated.title}")
        return
    self._append_entry("recovery", "Work", "Usage: /activity [inspect|create|focus|drop]")

def _append_memory(self, args: list[str]) -> None:
    action = args[0] if args else "inspect"
    if action in {"inspect", "show", "list", "ls"} and len(args) <= 1:
        surface = self.runtime.inspect_memory_surface(self.session_id)
        lines = list(render_memory_lines(surface))
        lines.extend(
            [
                "",
                "inspect: /memory inspect <memory-id>",
                "search: /memory search <query>",
                "correct: /memory correct <memory-id> <content>",
                "pin: /memory pin <memory-id> [reason]",
                "unpin: /memory unpin <memory-id> [reason]",
                "delete: /memory delete <memory-id> [reason]",
            ]
        )
        self._append_entry("notice", "Memory", "\n".join(lines))
        return
    if action == "inspect":
        if len(args) < 2:
            self._append_entry("recovery", "Memory", "Usage: /memory inspect <memory-id>")
            return
        memory = self.runtime.inspect_memory(self.session_id, args[1])
        detail = MemoryOperatorDetail(
            memory=memory,
            state=self.runtime.memory_state(memory.memory_id),
            lineage=self.runtime.memory_lineage(memory.memory_id),
        )
        surface = build_memory_operator_surface(
            session_id=self.session_id,
            memories=(detail,),
            index_policy=self.runtime.memory_runtime.index_policy(),
        )
        self._append_entry("notice", "Memory detail", "\n".join(render_memory_lines(surface)))
        return
    if action == "search":
        query = " ".join(args[1:]).strip()
        if not query:
            self._append_entry("recovery", "Memory", "Usage: /memory search <query>")
            return
        surface = self.runtime.search_memory_surface(self.session_id, query=query)
        self._append_entry("notice", "Memory search", "\n".join(render_memory_lines(surface)))
        return
    if action == "lineage":
        if len(args) < 2:
            self._append_entry("recovery", "Memory", "Usage: /memory lineage <memory-id>")
            return
        memory_id = args[1]
        self._append_entry(
            "notice",
            "Memory lineage",
            "\n".join(
                [
                    f"memory_id: {memory_id}",
                    f"state: {self.runtime.memory_state(memory_id) or 'unknown'}",
                    f"lineage: {self.runtime.memory_lineage(memory_id) or '<none>'}",
                ]
            ),
        )
        return
    if action == "correct":
        if len(args) < 3:
            self._append_entry("recovery", "Memory", "Usage: /memory correct <memory-id> <content>")
            return
        _, corrected, reason, lineage = self.runtime.correct_memory(
            self.session_id,
            args[1],
            corrected_content=" ".join(args[2:]).strip(),
            reason="memory corrected from /memory surface",
        )
        target = corrected if corrected is not None else self.runtime.inspect_memory(self.session_id, args[1])
        self._append_entry(
            "notice",
            "Memory corrected",
            "\n".join(
                [
                    f"memory_id: {target.memory_id}",
                    f"lineage: {lineage or '<none>'}",
                    f"reason: {reason}",
                    f"content: {target.content}",
                ]
            ),
        )
        return
    if action in {"pin", "freeze"}:
        if len(args) < 2:
            self._append_entry("recovery", "Memory", "Usage: /memory pin <memory-id> [reason]")
            return
        reason = " ".join(args[2:]).strip() or "memory pinned from /memory surface"
        record, decision_reason = self.runtime.pin_memory(self.session_id, args[1], reason=reason)
        self._append_entry(
            "notice",
            "Memory pinned",
            "\n".join(
                [
                    f"memory_id: {record.memory_id}",
                    f"tags: {', '.join(record.tags) or '<none>'}",
                    f"reason: {decision_reason or reason}",
                ]
            ),
        )
        return
    if action in {"unpin", "unfreeze", "thaw"}:
        if len(args) < 2:
            self._append_entry("recovery", "Memory", "Usage: /memory unpin <memory-id> [reason]")
            return
        reason = " ".join(args[2:]).strip() or "memory unpinned from /memory surface"
        record, decision_reason = self.runtime.unpin_memory(self.session_id, args[1], reason=reason)
        self._append_entry(
            "notice",
            "Memory unpinned",
            "\n".join(
                [
                    f"memory_id: {record.memory_id}",
                    f"tags: {', '.join(record.tags) or '<none>'}",
                    f"reason: {decision_reason or reason}",
                ]
            ),
        )
        return
    if action in {"delete", "drop"}:
        if len(args) < 2:
            self._append_entry("recovery", "Memory", "Usage: /memory delete <memory-id> [reason]")
            return
        reason = " ".join(args[2:]).strip() or "memory deleted from /memory surface"
        original, decision_reason = self.runtime.delete_memory(self.session_id, args[1], reason=reason)
        self._append_entry(
            "notice",
            "Memory deleted",
            "\n".join(
                [
                    f"memory_id: {original.memory_id}",
                    f"state: {self.runtime.memory_state(original.memory_id) or 'deleted'}",
                    f"reason: {decision_reason or reason}",
                ]
            ),
        )
        return
    self._append_entry("recovery", "Memory", "Usage: /memory [list|inspect|search|lineage|correct|pin|unpin|delete]")

def _append_procedure(self, args: list[str]) -> None:
    action = args[0] if args else "list"
    if action in {"list", "ls", "show"} and len(args) <= 1:
        surface = self.runtime.inspect_procedure_surface(self.session_id)
        lines = list(render_procedure_lines(surface))
        lines.extend(
            [
                "",
                "inspect: /procedure inspect <procedure-id>",
                "patch: /procedure patch <procedure-id> title=<...> summary=<...> status=<...> trigger_refs=a,b",
                "retire: /procedure retire <procedure-id>",
            ]
        )
        self._append_entry("notice", "Procedure", "\n".join(lines))
        return
    if action == "inspect":
        if len(args) < 2:
            self._append_entry("recovery", "Procedure", "Usage: /procedure inspect <procedure-id>")
            return
        try:
            detail = self.runtime.inspect_procedure_detail(self.session_id, args[1])
        except Exception as error:
            self._append_entry("recovery", "Procedure", str(error))
            return
        surface = build_procedure_operator_surface(
            session_id=self.session_id,
            profile_id=self.runtime.inspect_session(self.session_id).profile_id,
            procedures=(detail,),
            candidates=(),
        )
        self._append_entry("notice", "Procedure detail", "\n".join(render_procedure_lines(surface)))
        return
    if action in {"patch", "update"}:
        if len(args) < 2:
            self._append_entry("recovery", "Procedure", "Usage: /procedure patch <procedure-id> key=value ...")
            return
        try:
            payload = self._parse_named_arguments(args[2:])
            detail = self.runtime.patch_procedure_surface(self.session_id, args[1], payload)
        except Exception as error:
            self._append_entry("recovery", "Procedure", str(error))
            return
        surface = build_procedure_operator_surface(
            session_id=self.session_id,
            profile_id=self.runtime.inspect_session(self.session_id).profile_id,
            procedures=(detail,),
            candidates=(),
        )
        self._append_entry("notice", "Procedure updated", "\n".join(render_procedure_lines(surface)))
        return
    if action == "retire":
        if len(args) < 2:
            self._append_entry("recovery", "Procedure", "Usage: /procedure retire <procedure-id>")
            return
        try:
            detail = self.runtime.retire_procedure_surface(self.session_id, args[1])
        except Exception as error:
            self._append_entry("recovery", "Procedure", str(error))
            return
        surface = build_procedure_operator_surface(
            session_id=self.session_id,
            profile_id=self.runtime.inspect_session(self.session_id).profile_id,
            procedures=(detail,),
            candidates=(),
        )
        self._append_entry("notice", "Procedure retired", "\n".join(render_procedure_lines(surface)))
        return
    self._append_entry("recovery", "Procedure", "Usage: /procedure [list|inspect|patch|retire]")

def _append_audit(self, args: list[str]) -> None:
    continuity = self.runtime.inspect_continuity(session_id=self.session_id)
    graph = self.runtime.repository.load_activity_graph(self.session_id)
    work_surface = build_activity_operator_surface(
        session_id=self.session_id,
        active_goal_id=graph.active_goal_id if graph is not None else None,
        active_goal_reason=continuity.wake_summary,
        wake_action=continuity.wake_action,
        wake_factors=continuity.wake_factors,
        goal_graph_revision=graph.revision_id if graph is not None else None,
        goals=graph.goals if graph is not None else (),
    )
    audit = build_audit_surface(
        session_id=self.session_id,
        active_goal_id=work_surface.active_goal_id,
        active_goal_reason=work_surface.active_goal_reason,
        context_result=self.runtime.inspect_context_frame(self.session_id),
    )
    lines = list(render_audit_lines(audit))
    if args and args[0] == "prompt":
        lines.extend(("", "rendered_prompt:", audit.rendered_prompt))
    else:
        first_line = audit.rendered_prompt.splitlines()[0] if audit.rendered_prompt else "<empty>"
        lines.append("")
        lines.append(f"rendered_prompt_preview: {first_line}")
        lines.append("full prompt: /audit prompt")
    self._append_entry("notice", "Audit", "\n".join(lines))

def _resume_session(self, target: str) -> None:
    if target == "latest":
        latest = self.runtime.latest_session()
        if latest is None:
            self._append_entry(
                "recovery",
                "Resume",
                'No existing clone is available. Create one from the CLI with: aegis clone <name> --initial-goal "..."',
            )
            return
        self.session_id = latest.session_id
        self.opened = f"Opened clone {self.runtime.clone_id_for_session(latest)}"
    else:
        clone_session = self.runtime.latest_session_for_clone(target)
        if clone_session is not None:
            self.session_id = clone_session.session_id
            self.opened = f"Opened clone {target}"
        else:
            self.runtime.inspect_session(target)
            self.session_id = target
            selected = self.runtime.inspect_session(target)
            self.opened = f"Opened clone {self.runtime.clone_id_for_session(selected)}"
    self._append_entry("status", "Resume", f"{self.opened} via session {self.session_id}.")
    self._append_status()

def _append_identity_charter(self, session_id: str, args: list[str], *, alias_label: str = "Identity charter") -> None:
    action = args[0] if args else "show"
    profile_id = self.runtime.inspect_session(session_id).profile_id
    if action == "show":
        record = self.runtime.inspect_profile_surface(session_id).identity
        self._append_entry(
            "notice",
            alias_label,
            "\n".join(
                [
                    f"profile_id: {record.profile_id}",
                    f"clone_id: {record.clone_id}",
                    f"charter_extension: {record.charter_extension or '<empty>'}",
                ]
            ),
        )
        return
    if action == "set":
        if len(args) < 2:
            self._append_entry("recovery", alias_label, "Usage: /profile charter set <text>")
            return
        try:
            surface = self.runtime.patch_profile_surface(
                session_id,
                {"charter_text": " ".join(args[1:]).strip()},
            )
        except Exception as error:
            self._append_entry("recovery", alias_label, str(error))
            return
        self._append_entry(
            "notice",
            f"{alias_label} updated",
            f"charter_extension: {surface.identity.charter_extension or '<empty>'}",
        )
        return
    if action == "clear":
        try:
            self.runtime.patch_profile_surface(session_id, {"clear_charter": True})
        except Exception as error:
            self._append_entry("recovery", alias_label, str(error))
            return
        self._append_entry("notice", f"{alias_label} updated", "status: cleared")
        return
    self._append_entry("recovery", alias_label, "Usage: /profile charter show|set|clear")

def _append_user(self, args: list[str], *, alias_title: str = "User", usage_prefix: str = "/profile user") -> None:
    action = args[0] if args else "show"
    profile_id = self.runtime.inspect_session(self.session_id).profile_id
    if action == "show":
        self._append_entry("notice", alias_title, "\n".join(self._user_lines(profile_id)))
        return
    if action == "set":
        if len(args) < 2:
            self._append_entry("recovery", alias_title, f"Usage: {usage_prefix} set <text>")
            return
        try:
            self.runtime.update_user_state(session_id=self.session_id, text=" ".join(args[1:]), append=False, clear=False)
        except Exception as error:
            self._append_entry("recovery", alias_title, str(error))
            return
        self._append_entry("notice", f"{alias_title} updated", "\n".join(self._user_lines(profile_id)))
        return
    if action == "append":
        if len(args) < 2:
            self._append_entry("recovery", alias_title, f"Usage: {usage_prefix} append <text>")
            return
        try:
            self.runtime.update_user_state(session_id=self.session_id, text=" ".join(args[1:]), append=True, clear=False)
        except Exception as error:
            self._append_entry("recovery", alias_title, str(error))
            return
        self._append_entry("notice", f"{alias_title} updated", "\n".join(self._user_lines(profile_id)))
        return
    if action == "clear":
        try:
            self.runtime.update_user_state(session_id=self.session_id, clear=True)
        except Exception as error:
            self._append_entry("recovery", alias_title, str(error))
            return
        self._append_entry("notice", f"{alias_title} updated", "status: cleared")
        return
    self._append_entry("recovery", alias_title, f"Usage: {usage_prefix} show|set|append|clear")

def _append_relationship(
    self,
    args: list[str],
    *,
    alias_title: str = "Relationship",
    usage_prefix: str = "/profile relationship",
) -> None:
    action = args[0] if args else "show"
    profile_id = self.runtime.inspect_session(self.session_id).profile_id
    if action == "show":
        self._append_entry("notice", alias_title, "\n".join(self._relationship_lines(profile_id)))
        return
    if action == "set":
        if len(args) < 2:
            self._append_entry("recovery", alias_title, f"Usage: {usage_prefix} set <text>")
            return
        try:
            self.runtime.update_relationship_state(session_id=self.session_id, text=" ".join(args[1:]), append=False, clear=False)
        except Exception as error:
            self._append_entry("recovery", alias_title, str(error))
            return
        self._append_entry("notice", f"{alias_title} updated", "\n".join(self._relationship_lines(profile_id)))
        return
    if action == "append":
        if len(args) < 2:
            self._append_entry("recovery", alias_title, f"Usage: {usage_prefix} append <text>")
            return
        try:
            self.runtime.update_relationship_state(session_id=self.session_id, text=" ".join(args[1:]), append=True, clear=False)
        except Exception as error:
            self._append_entry("recovery", alias_title, str(error))
            return
        self._append_entry("notice", f"{alias_title} updated", "\n".join(self._relationship_lines(profile_id)))
        return
    if action == "clear":
        try:
            self.runtime.update_relationship_state(session_id=self.session_id, clear=True)
        except Exception as error:
            self._append_entry("recovery", alias_title, str(error))
            return
        self._append_entry("notice", f"{alias_title} updated", "status: cleared")
        return
    self._append_entry("recovery", alias_title, f"Usage: {usage_prefix} show|set|append|clear")

def _append_models(self, args: list[str]) -> None:
    action = args[0] if args else "configure"
    provider = dict(self.runtime.provider_summary())
    provider_id = str(provider.get("provider_id") or "")
    if provider_id in {"", "preview"}:
        self._append_entry("recovery", "Models", "Configure a provider first with /providers.")
        return
    if action in {"list", "ls"}:
        try:
            models = self.runtime.discover_provider_models(provider_id=provider_id)
        except Exception as error:
            self._append_entry("recovery", "Models", str(error))
            return
        lines = [
            (
                f"{model.model_id} | context={model.context_window_tokens or '<unknown>'} | "
                f"output={model.max_output_tokens or '<unknown>'}"
            )
            for model in models
        ] or ["<empty>"]
        lines.extend(
            [
                "",
                "/providers - open the unified provider and model setup flow",
                "/providers status - inspect the active provider and model posture",
            ]
        )
        self._append_entry("notice", "Models", "\n".join(lines))
        return
    if action == "status":
        self._append_entry(
            "status",
            "Model",
            "\n".join(
                [
                    f"provider_id: {provider_id}",
                    f"strong_model: {provider.get('strong_model') or '<unset>'}",
                    f"weak_model: {provider.get('weak_model') or '<unset>'}",
                    f"intent_mode: {provider.get('intent_mode') or '<unset>'}",
                    f"embedding_bootstrap_status: {provider.get('embedding_bootstrap_status') or '<unset>'}",
                    f"context_window_tokens: {provider.get('context_window_tokens') or '<unset>'}",
                    f"context_window_mode: {provider.get('context_window_mode') or '<unset>'}",
                    f"reasoning_effort: {provider.get('reasoning_effort') or '<unset>'}",
                    f"reasoning_efforts: {', '.join(provider.get('reasoning_efforts', ())) or '<none>'}",
                    f"supports_streaming: {provider.get('supports_streaming', '<unknown>')}",
                ]
            ),
        )
        return
    session = self.runtime.inspect_session(self.session_id)
    profile = self.runtime.inspect_profile(session.profile_id)
    initial_state = provider_setup_defaults(self.runtime, provider_id)
    initial_state.base_url = str(provider.get("base_url") or initial_state.base_url)
    initial_state.strong_model = str(provider.get("strong_model") or initial_state.strong_model)
    initial_state.weak_model = str(provider.get("weak_model") or initial_state.weak_model or initial_state.strong_model)
    initial_state.intent_mode = str(provider.get("intent_mode") or initial_state.intent_mode)
    initial_state.reasoning_effort = (
        str(provider.get("reasoning_effort")).strip()
        if provider.get("reasoning_effort") is not None
        else initial_state.reasoning_effort
    ) or None
    initial_state.context_window_mode = str(provider.get("context_window_mode") or initial_state.context_window_mode)
    if provider.get("context_window_tokens") is not None:
        try:
            initial_state.context_window_tokens = int(provider["context_window_tokens"])
        except (TypeError, ValueError):
            initial_state.context_window_tokens = initial_state.context_window_tokens
    from . import shell as _shell_module

    configured = _shell_module.run_provider_selection_wizard(
        self.runtime,
        initial_state=initial_state,
        allow_back=True,
        provider_locked=True,
    )
    if configured is WIZARD_BACK:
        self._append_entry("notice", "Models", "Model setup cancelled.")
        return
    self.runtime.set_default_provider(
        provider_id=configured.provider_id,
        profile_id=profile.state.profile_id,
        display_name=profile.state.display_name,
        mode=profile.state.mode,
        base_url=configured.base_url,
        strong_model=configured.strong_model,
        weak_model=configured.weak_model,
        intent_mode=configured.intent_mode,
        api_key=configured.api_key,
        context_window_tokens=configured.context_window_tokens,
        context_window_mode=configured.context_window_mode,
        reasoning_effort=configured.reasoning_effort,
    )
    self._append_entry(
        "status",
        "Model updated",
        "\n".join(
            [
                f"provider_id: {configured.provider_id}",
                f"strong_model: {configured.strong_model}",
                f"weak_model: {configured.weak_model}",
                f"intent_mode: {configured.intent_mode}",
                f"context_window_tokens: {configured.context_window_tokens or '<unset>'}",
                f"context_window_mode: {configured.context_window_mode}",
                f"reasoning_effort: {configured.reasoning_effort or '<unset>'}",
            ]
        ),
    )

def _append_outcome(self, outcome: KernelOutcome) -> None:
    self._last_prompt_tokens = outcome.execution.prompt_tokens
    self._last_completion_tokens = outcome.execution.completion_tokens
    self._last_total_tokens = outcome.execution.total_tokens
    if self.debug and outcome.stages:
        stage_lines = [
            f"{stage.stage} | {stage.detail} | {stage.recorded_at.isoformat(timespec='seconds')}"
            for stage in outcome.stages
        ]
        self._append_entry("status", "Runtime stages", "\n".join(stage_lines))
    assistant_name = self.runtime.inspect_profile(self.runtime.inspect_session(self.session_id).profile_id).state.display_name
    assistant_lines = [outcome.execution.summary]
    if self.debug and outcome.plan is not None:
        assistant_lines.append(f"plan: {outcome.plan.rationale}")
    if self.debug:
        assistant_lines.extend(
            [
                f"execution: {outcome.execution.outcome}",
                f"goals_in_play: {len(outcome.goals)}",
                f"memory_hits: {len(outcome.memories)}",
            ]
        )
    self._append_entry("assistant", assistant_name, "\n".join(assistant_lines), meta=outcome_intent_meta(outcome))

def _append_growth_update_message(self, update) -> None:
    if update is None:
        return
    continuity = self.runtime.inspect_continuity(session_id=self.session_id)
    assistant_name = continuity.profile.state.display_name or "Aegis"
    after = update.after
    after_level = getattr(after, "ascension_level", getattr(after, "level", 0))
    after_cycle = getattr(after, "cycle_label", "Cycle I")
    after_identity = getattr(after, "identity_line", getattr(getattr(after, "stage", None), "title", "Aegis"))
    if update.stage_changed:
        body = (
            f"I just crossed into {after_identity}. "
            "Thanks for staying with me while I keep the thread moving."
        )
        meta = "growth · title-shift"
    else:
        body = (
            f"I just reached Lv.{after_level} in {after_cycle}. "
            "Thanks for staying with me while I keep the thread moving."
        )
        meta = "growth · level-up ✨"
    self._append_entry("growth", assistant_name, body, meta=meta)
