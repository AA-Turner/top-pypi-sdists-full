"""Primary CLI shell implementation assembled from bound method modules."""

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
from .runtime_snapshot import load_snapshot_session_context_epoch
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
from .shell_clarify import ShellInteractiveClarifySurface
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
from . import shell_methods_activity as _shell_activity
from . import shell_methods_commands as _shell_commands
from . import shell_methods_dispatch as _shell_dispatch
from . import shell_methods_prompt as _shell_prompt_methods
from . import shell_methods_skills as _shell_skills
from . import shell_methods_trace as _shell_trace
from . import turn_metrics as _shell_turn_metrics
from . import shell_methods_ui as _shell_ui_methods

class ProductizedShell:
    command_specs = (
        ShellCommandSpec("/help", "Open the command palette and interaction hints"),
        ShellCommandSpec("/status", "Refresh session, provider, and growth posture"),
        ShellCommandSpec("/resume", "Resume the latest or a known Aegis clone"),
        ShellCommandSpec("/profile", "Inspect or patch owner-aligned profile state"),
        ShellCommandSpec("/activity", "Inspect or mutate owner-aligned durable activity state"),
        ShellCommandSpec("/memory", "Inspect remembered context for this clone"),
        ShellCommandSpec("/procedure", "Inspect or govern promoted procedures and overlays"),
        ShellCommandSpec("/audit", "Inspect the current context, recall reasons, and overlays"),
        ShellCommandSpec("/frozen", "Inspect the current session's frozen prompt sections"),
        ShellCommandSpec("/tools", "Inspect, install, toggle, and run built-in or manifest-backed tools"),
        ShellCommandSpec("/skills", "Discover, inspect, install, and toggle built-in or external skill packages"),
        ShellCommandSpec("/cron", "Inspect, create, pause, resume, and remove built-in scheduled jobs"),
        ShellCommandSpec("/providers", "Set or switch the active provider, endpoint, and encrypted key"),
        ShellCommandSpec("/models", "Set or switch the active model and context window"),
        ShellCommandSpec("/clear", "Start a fresh session in this thread and replay the opening reply"),
        ShellCommandSpec("/exit", "Leave the wake surface"),
    )

def __init__(self, runtime: CliRuntime, *, session_id: str, opened: str, debug: bool = False) -> None:
    self.runtime = runtime
    self.session_id = session_id
    self.opened = opened
    self.debug = debug or os.environ.get("AEGIS_DEBUG") == "1"
    self.console = Console(highlight=False, soft_wrap=True)
    self.version = _resolve_aegis_version()
    self.cwd = _display_path(Path.cwd())
    self.transcript: list[TranscriptEntry] = []
    self._pending_file_reviews: dict[str, _PendingFileReview] = {}
    self._pending_commands: deque[PendingShellCommand] = deque()
    self._rendered_entries = 0
    self._opened_at = time.monotonic()
    self._turn_started_at: float | None = None
    self._last_turn_elapsed_seconds = 0
    self._last_prompt_tokens = 0
    self._last_provider_prompt_tokens = 0
    self._last_completion_tokens = 0
    self._last_total_tokens = 0
    self._pending_context_compaction_frame: dict[str, object] | None = None
    self._pending_context_compaction_frame_rendered = False
    self._intent_runtime_ready_seen = False
    self._intent_runtime_ready_seen_at: float | None = None
    self._intent_ready_notice_until: float | None = None
    self._intent_runtime_notice_seeded = False
    self._intent_runtime_last_state: str | None = None
    self._intent_runtime_notices: list[tuple[str, str]] = []
    self._startup_surface_prepared = False
    self._startup_surface_prepare_started = False
    self._startup_transcript_primed = False
    self._startup_prime_started = False
    self._startup_user_turn_submitted = False
    self._last_shell_frame_token: tuple[object, ...] | None = None
    self._clarify_state = None
    self._clarify_lock = threading.Lock()
    self._clarify_invalidator = None
    self.runtime.prepare_session_surface(self.session_id, warm_embeddings=False)
    self._skill_slash_specs = self._load_skill_slash_specs()

def run(self) -> int:
    self._render_startup_sequence()
    self._refresh_shell_frame()
    self._prepare_startup_surface()
    while True:
        try:
            command = self._next_command()
        except KeyboardInterrupt:
            self._append_entry(
                "notice",
                "Grow surface",
                "Prompt interrupted. Type a request, use /help, or /exit when you are done.",
            )
            self._render_pending_entries()
            continue
        except EOFError:
            self._append_entry("notice", "Grow surface", f"Leaving session {self.session_id}.")
            self._render_pending_entries()
            break
        if command.command == "__aegis.startup.prime__":
            self._prime_startup_transcript_if_needed()
            self._render_pending_entries()
            if not (self._pending_commands and self._startup_intent_dispatch_ready()):
                continue
            command = self._pending_commands.popleft()
        if command.command == "__aegis.startup.dispatch-pending__":
            if not self._pending_commands:
                continue
            command = self._pending_commands.popleft()
        if command.command == "__aegis.cron.tick__":
            self._append_due_cron_jobs()
            self._render_pending_entries()
            continue
        if self._dispatch(command.command):
            self._refresh_shell_frame()
            self._render_pending_entries()
            break
        self._render_pending_entries()
    self.console.print("Aegis stays by your side.")
    return 0

def _append_due_cron_jobs(self) -> None:
    assistant_name = self._assistant_name()
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

def _interactive_clarify_surface(self) -> ShellInteractiveClarifySurface:
    return ShellInteractiveClarifySurface(self)

def _render_startup_sequence(self) -> None:
    if not self._animations_enabled() or Group is None or Table is None:
        return
    with Live(
        self._render_boot_frame(STARTUP_SEQUENCE_STEPS, active=-1),
        console=self.console,
        refresh_per_second=30,
        screen=True,
        transient=True,
    ) as live:
        time.sleep(STARTUP_SEQUENCE_STEP_DELAY)
        for index in range(len(STARTUP_SEQUENCE_STEPS)):
            live.update(self._render_boot_frame(STARTUP_SEQUENCE_STEPS, active=index), refresh=True)
            time.sleep(STARTUP_SEQUENCE_STEP_DELAY)

def _render_boot_frame(self, steps: tuple[tuple[str, str], ...], *, active: int):
    continuity = self.runtime.inspect_continuity(session_id=self.session_id)
    growth = self.runtime.inspect_growth(session_id=self.session_id)
    provider = dict(self.runtime.provider_summary())
    viewport = getattr(self.console, "size", None)
    boot_stage_id, boot_level = self._boot_growth_stage(active)
    return render_boot_frame(
        context=BootFrameContext(
            display_name=continuity.profile.state.display_name or "Aegis",
            growth_stage_title=growth.identity_line,
            growth_level=growth.ascension_level,
            provider_model=provider.get("strong_model") or "<unset>",
            viewport_width=int(getattr(viewport, "width", 0) or 0),
            viewport_height=int(getattr(viewport, "height", 0) or 0),
        ),
        steps=steps,
        active=active,
        rich_available=RICH_AVAILABLE,
        table_cls=Table,
        group_cls=Group,
        text_cls=Text,
        panel_cls=Panel,
        align_cls=Align,
        brand_accent=BRAND_ACCENT,
        brand_accent_strong=BRAND_ACCENT_STRONG,
        brand_light=BRAND_LIGHT,
        brand_muted=BRAND_MUTED,
        brand_dark=BRAND_DARK,
        center_brand_block=self._center_brand_block,
        brand_mark=self._render_growth_mark(boot_stage_id, level=boot_level),
    )

def _refresh_shell_frame(self) -> None:
    self._rendered_entries = 0
    if self._pending_context_compaction_frame is not None:
        self._pending_context_compaction_frame_rendered = False
    self.console.clear(home=True)
    self.console.print(self._render_shell_frame())
    self._last_shell_frame_token = self._current_shell_frame_token()

def _refresh_shell_frame_if_needed(self) -> bool:
    current = self._current_shell_frame_token()
    if current == self._last_shell_frame_token:
        return False
    self._refresh_shell_frame()
    return True

def _current_shell_frame_token(self) -> tuple[object, ...]:
    growth = self.runtime.inspect_growth(session_id=self.session_id)
    epoch = load_snapshot_session_context_epoch(self.runtime, session_id=self.session_id)
    return (
        self.session_id,
        getattr(growth, "ascension_level", 0),
        getattr(growth, "stage_title", ""),
        getattr(growth, "ring_index", 1),
        bool(epoch is not None and epoch.frozen),
        getattr(epoch, "thread_focus", "") if epoch is not None else "",
        getattr(epoch, "frozen_skill_count", 0) if epoch is not None else 0,
        getattr(epoch, "frozen_tool_count", 0) if epoch is not None else 0,
    )

def _append_providers(self, args: list[str]) -> None:
    action = args[0] if args else "configure"
    if action in {"list", "ls"}:
        lines = [
            (
                f"{state.provider_id} | {state.display_name} | {state.transport_display_name} | "
                f"status={state.status} | source={state.source}"
            )
            for state in self.runtime.provider_inventory()
            if state.runtime_enabled
        ] or ["<empty>"]
        lines.extend(
            [
                "",
                "/providers - open the unified provider and model setup flow",
                "/providers status - inspect the active provider and model posture",
            ]
        )
        self._append_entry("notice", "Providers", "\n".join(lines))
        return
    if action == "status":
        provider = dict(self.runtime.provider_summary())
        discovered = self.runtime.discovered_provider(str(provider.get("provider_id") or "openai-compatible"))
        self._append_entry(
            "status",
            "Provider",
            "\n".join(
                [
                    f"provider_id: {provider.get('provider_id', '<unset>')}",
                    f"display_name: {provider.get('display_name', provider.get('provider_id', '<unset>'))}",
                    f"base_url: {provider.get('base_url') or '<unset>'}",
                    f"strong_model: {provider.get('strong_model') or '<unset>'}",
                    f"weak_model: {provider.get('weak_model') or '<unset>'}",
                    f"intent_mode: {provider.get('intent_mode') or '<unset>'}",
                    f"embedding_bootstrap_status: {provider.get('embedding_bootstrap_status') or '<unset>'}",
                    f"context_window_tokens: {provider.get('context_window_tokens') or '<unset>'}",
                    f"context_window_mode: {provider.get('context_window_mode') or '<unset>'}",
                    f"reasoning_effort: {provider.get('reasoning_effort') or '<unset>'}",
                    f"reasoning_efforts: {', '.join(provider.get('reasoning_efforts', ())) or '<none>'}",
                    f"secret_status: {provider.get('secret_status', '<unknown>')}",
                    f"secret_source: {provider.get('secret_source', '<unknown>')}",
                    f"discovery_status: {discovered.status}",
                    f"discovery_source: {discovered.source}",
                    f"transport: {provider.get('transport_display_name', provider.get('transport_id', '<unset>'))}",
                ]
            ),
        )
        return
    session = self.runtime.inspect_session(self.session_id)
    profile = self.runtime.inspect_profile(session.profile_id)
    provider = dict(self.runtime.provider_summary())
    current_provider_id = str(provider.get("provider_id") or "openai-compatible")
    initial_state = provider_setup_defaults(self.runtime, current_provider_id)
    initial_state.base_url = str(provider.get("base_url") or initial_state.base_url)
    initial_state.strong_model = str(provider.get("strong_model") or initial_state.strong_model)
    initial_state.weak_model = str(provider.get("weak_model") or initial_state.weak_model or initial_state.strong_model)
    initial_state.intent_mode = str(provider.get("intent_mode") or initial_state.intent_mode)
    initial_state.reasoning_effort = (
        str(provider.get("reasoning_effort")).strip()
        if provider.get("reasoning_effort") is not None
        else initial_state.reasoning_effort
    ) or None
    configured = run_provider_selection_wizard(
        self.runtime,
        initial_state=initial_state,
        allow_back=True,
    )
    if configured is WIZARD_BACK:
        self._append_entry("notice", "Providers", "Provider setup cancelled.")
        return
    updated = self.runtime.set_default_provider(
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
        "Provider updated",
        "\n".join(
            [
                f"provider_id: {configured.provider_id}",
                f"base_url: {configured.base_url}",
                f"strong_model: {configured.strong_model}",
                f"weak_model: {configured.weak_model}",
                f"intent_mode: {configured.intent_mode}",
                f"context_window_tokens: {configured.context_window_tokens or '<unset>'}",
                f"context_window_mode: {configured.context_window_mode}",
                f"reasoning_effort: {configured.reasoning_effort or '<unset>'}",
                f"display_name: {updated.state.display_name}",
            ]
        ),
    )

def _show_growth_celebration_if_needed(self):
    update = self.runtime.consume_growth_update(session_id=self.session_id)
    if update is None:
        return None
    transition = self.runtime.inspect_growth_transition(update, session_id=self.session_id)
    if not transition.leveled_up:
        return None
    if not self._animations_enabled() or Live is None:
        return transition
    if transition.stage_changed:
        final_tick = 5
        with Live(
            self._render_stage_transition_frame(transition, tick=0),
            console=self.console,
            refresh_per_second=24,
            transient=True,
        ) as live:
            for tick in range(final_tick + 1):
                live.update(self._render_stage_transition_frame(transition, tick=tick), refresh=True)
                time.sleep(0.14)
        self.console.print(self._render_stage_transition_frame(transition, tick=final_tick))
        time.sleep(1.05)
        return transition
    final_tick = 5
    with Live(
        self._render_level_up_frame(transition, tick=0),
        console=self.console,
        refresh_per_second=24,
        transient=True,
    ) as live:
        for tick in range(final_tick + 1):
            live.update(self._render_level_up_frame(transition, tick=tick), refresh=True)
            time.sleep(0.12)
    self.console.print(self._render_level_up_frame(transition, tick=final_tick))
    time.sleep(1.2)
    return transition

def _render_level_up_frame(self, update, *, tick: int):
    marker = ("*", "+", "*", "+")[tick % 4]
    body = Text()
    body.append(f"{marker} LEVEL UP\n", style=f"bold {BRAND_ACCENT_STRONG}")
    body.append(f"{update.after.identity_line}\n", style=f"bold {BRAND_LIGHT}")
    body.append(f"Lv.{update.before.ascension_level} -> Lv.{update.after.ascension_level}\n", style=BRAND_LIGHT)
    body.append(f"Power +{update.delta_score} · ", style=BRAND_MUTED)
    body.append_text(self._styled_growth_progress_bar(update.after))
    body.append(f" · {update.after.progress_percent}%", style=BRAND_MUTED)
    return Panel(
        body,
        title=f"[bold {BRAND_ACCENT}]Aegis is evolving[/bold {BRAND_ACCENT}]",
        border_style=BRAND_ACCENT,
        padding=(0, 1),
    )

def _render_stage_transition_frame(self, update, *, tick: int):
    if Table is None or Group is None:
        return Text(
            f"Title shift: {update.before.stage_title} -> {update.after.stage_title} "
            f"({update.after.cycle_label})"
        )
    body = Table.grid(expand=True)
    body.add_column(ratio=1, justify="center")
    body.add_column(ratio=1, justify="center")
    left_mark = self._render_growth_mark(update.before.brand_stage_id, level=update.before.ascension_level)
    right_mark = self._render_growth_mark(update.after.brand_stage_id, level=update.after.ascension_level)
    if tick % 2 == 1:
        left_mark, right_mark = right_mark, left_mark
    body.add_row(left_mark, right_mark)
    caption = Text()
    caption.append("TITLE SHIFT\n", style=f"bold {BRAND_ACCENT_STRONG}")
    caption.append(
        f"{update.before.identity_line} -> {update.after.identity_line}\n",
        style=f"bold {BRAND_LIGHT}",
    )
    caption.append(
        f"Lv.{update.before.ascension_level} -> Lv.{update.after.ascension_level} · {update.after.next_milestone}",
        style=BRAND_MUTED,
    )
    return Panel(
        Group(body, caption),
        title=f"[bold {BRAND_ACCENT}]Aegis crossed a new title window[/bold {BRAND_ACCENT}]",
        border_style=BRAND_ACCENT,
        padding=(0, 1),
    )

ProductizedShell.__init__ = __init__
ProductizedShell.run = run
ProductizedShell._append_due_cron_jobs = _append_due_cron_jobs
ProductizedShell._interactive_clarify_surface = _interactive_clarify_surface
ProductizedShell._render_startup_sequence = _render_startup_sequence
ProductizedShell._render_boot_frame = _render_boot_frame
ProductizedShell._refresh_shell_frame = _refresh_shell_frame
ProductizedShell._refresh_shell_frame_if_needed = _refresh_shell_frame_if_needed
ProductizedShell._current_shell_frame_token = _current_shell_frame_token
ProductizedShell._append_providers = _append_providers
ProductizedShell._show_growth_celebration_if_needed = _show_growth_celebration_if_needed
ProductizedShell._render_level_up_frame = _render_level_up_frame
ProductizedShell._render_stage_transition_frame = _render_stage_transition_frame

ProductizedShell.recent_session_ids = _shell_skills.recent_session_ids
ProductizedShell.recent_clone_ids = _shell_skills.recent_clone_ids
ProductizedShell.skill_slash_specs = _shell_skills.skill_slash_specs
ProductizedShell._refresh_skill_slash_specs = _shell_skills._refresh_skill_slash_specs
ProductizedShell._load_skill_slash_specs = _shell_skills._load_skill_slash_specs
ProductizedShell._resolve_skill_slash_spec = _shell_skills._resolve_skill_slash_spec
ProductizedShell._resolve_explicit_skill_request = _shell_skills._resolve_explicit_skill_request
ProductizedShell._resolve_contextual_skill_request = _shell_skills._resolve_contextual_skill_request
ProductizedShell._resolved_skill_route = _shell_skills._resolved_skill_route
ProductizedShell._dispatch_skill_slash_command = _shell_skills._dispatch_skill_slash_command
ProductizedShell._compose_skill_turn_prompt = _shell_skills._compose_skill_turn_prompt

ProductizedShell._next_command = _shell_ui_methods._next_command
ProductizedShell._prompt_toolkit_composer_available = _shell_ui_methods._prompt_toolkit_composer_available
ProductizedShell._shell_history = _shell_ui_methods._shell_history
ProductizedShell._build_prompt_buffer = _shell_ui_methods._build_prompt_buffer
ProductizedShell._build_input_window = _shell_ui_methods._build_input_window
ProductizedShell._build_command_palette = _shell_ui_methods._build_command_palette
ProductizedShell._build_queue_preview_window = _shell_ui_methods._build_queue_preview_window
ProductizedShell._build_divider_window = _shell_ui_methods._build_divider_window
ProductizedShell._build_composer_body = _shell_ui_methods._build_composer_body
ProductizedShell._read_command = _shell_ui_methods._read_command
ProductizedShell.personality_preset_choices = _shell_ui_methods.personality_preset_choices
ProductizedShell._prompt_label = _shell_ui_methods._prompt_label
ProductizedShell._prompt_continuation = _shell_ui_methods._prompt_continuation
ProductizedShell._prompt_style = _shell_ui_methods._prompt_style
ProductizedShell._prompt_style_map = _shell_ui_methods._prompt_style_map
ProductizedShell._build_key_bindings = _shell_ui_methods._build_key_bindings
ProductizedShell._composer_divider = _shell_ui_methods._composer_divider
ProductizedShell._format_status_tokens = _shell_ui_methods._format_status_tokens
ProductizedShell._status_bar_context_style = _shell_ui_methods._status_bar_context_style
ProductizedShell._build_context_bar = _shell_ui_methods._build_context_bar
ProductizedShell._build_growth_bar_fragments = _shell_ui_methods._build_growth_bar_fragments
ProductizedShell._status_bar_snapshot = _shell_ui_methods._status_bar_snapshot
ProductizedShell._status_bar_fragments = _shell_ui_methods._status_bar_fragments
ProductizedShell._clear_composer = _shell_ui_methods._clear_composer
ProductizedShell._enqueue_followup_command = _shell_ui_methods._enqueue_followup_command
ProductizedShell._is_startup_conversational_command = _shell_ui_methods._is_startup_conversational_command
ProductizedShell._startup_intent_dispatch_ready = _shell_ui_methods._startup_intent_dispatch_ready
ProductizedShell._startup_should_hold_user_command = _shell_ui_methods._startup_should_hold_user_command
ProductizedShell._mark_startup_user_turn_submitted = _shell_ui_methods._mark_startup_user_turn_submitted
ProductizedShell._startup_should_surface_intent_notices = _shell_ui_methods._startup_should_surface_intent_notices
ProductizedShell._append_intent_runtime_notice = _shell_ui_methods._append_intent_runtime_notice
ProductizedShell._sync_intent_runtime_notices = _shell_ui_methods._sync_intent_runtime_notices
ProductizedShell._prepare_startup_surface = _shell_ui_methods._prepare_startup_surface
ProductizedShell._prime_startup_transcript_if_needed = _shell_ui_methods._prime_startup_transcript_if_needed
ProductizedShell._prime_transcript = _shell_ui_methods._prime_transcript
ProductizedShell._assistant_name = _shell_ui_methods._assistant_name
ProductizedShell._append_assistant_surface_reply = _shell_ui_methods._append_assistant_surface_reply
ProductizedShell._render_shell_frame = _shell_ui_methods._render_shell_frame
ProductizedShell._render_brand_column = _shell_ui_methods._render_brand_column
ProductizedShell._render_status_column = _shell_ui_methods._render_status_column

ProductizedShell._dispatch = _shell_dispatch._dispatch
ProductizedShell._handle_conversational_surface_request = _shell_dispatch._handle_conversational_surface_request
ProductizedShell._handle_slash_command = _shell_dispatch._handle_slash_command
ProductizedShell._parse_slash_command = _shell_dispatch._parse_slash_command
ProductizedShell._text_surface_fallback_parts = _shell_dispatch._text_surface_fallback_parts

ProductizedShell._append_help = _shell_commands._append_help
ProductizedShell._append_tools = _shell_commands._append_tools
ProductizedShell._append_skills = _shell_skills._append_skills
ProductizedShell._append_cron = _shell_commands._append_cron
ProductizedShell._parse_named_arguments = _shell_commands._parse_named_arguments
ProductizedShell._requested_webpage_url = _shell_commands._requested_webpage_url
ProductizedShell._strip_wrapping_quotes = _shell_commands._strip_wrapping_quotes
ProductizedShell._append_status = _shell_commands._append_status
ProductizedShell._append_profile = _shell_commands._append_profile
ProductizedShell._append_work = _shell_activity._append_work
ProductizedShell._append_memory = _shell_commands._append_memory
ProductizedShell._append_procedure = _shell_commands._append_procedure
ProductizedShell._append_audit = _shell_activity._append_audit
ProductizedShell._append_frozen = _shell_prompt_methods._append_frozen
ProductizedShell._resume_session = _shell_commands._resume_session
ProductizedShell._append_identity_charter = _shell_commands._append_identity_charter
ProductizedShell._append_user = _shell_commands._append_user
ProductizedShell._append_relationship = _shell_commands._append_relationship
ProductizedShell._append_models = _shell_commands._append_models
ProductizedShell._append_outcome = _shell_turn_metrics._append_outcome
ProductizedShell._append_growth_update_message = _shell_commands._append_growth_update_message

ProductizedShell._user_lines = _shell_trace._user_lines
ProductizedShell._relationship_lines = _shell_trace._relationship_lines
ProductizedShell._append_entry = _shell_trace._append_entry
ProductizedShell._append_tooltrace_line = _shell_trace._append_tooltrace_line
ProductizedShell._capture_pending_file_review = _shell_trace._capture_pending_file_review
ProductizedShell._todo_trace_lines = _shell_trace._todo_trace_lines
ProductizedShell._display_tool_diff_path = _shell_trace._display_tool_diff_path
ProductizedShell._file_review_trace_lines = _shell_trace._file_review_trace_lines
ProductizedShell._tool_result_trace_lines = _shell_trace._tool_result_trace_lines
ProductizedShell._boot_growth_stage = _shell_trace._boot_growth_stage
ProductizedShell._record_tool_event_trace = _shell_trace._record_tool_event_trace
ProductizedShell._kernel_trace_line = _shell_trace._kernel_trace_line
ProductizedShell._record_kernel_event_trace = _shell_trace._record_kernel_event_trace
ProductizedShell._animations_enabled = _shell_trace._animations_enabled
ProductizedShell._turn_phase = _shell_trace._turn_phase
ProductizedShell._summarize_progress_prompt = _shell_trace._summarize_progress_prompt
ProductizedShell._render_turn_progress_fragments = _shell_trace._render_turn_progress_fragments
ProductizedShell._render_queued_followup_fragments = _shell_trace._render_queued_followup_fragments
ProductizedShell._run_turn_with_queued_input = _shell_trace._run_turn_with_queued_input
ProductizedShell._run_turn_with_progress = _shell_trace._run_turn_with_progress
ProductizedShell._run_tool_with_progress = _shell_trace._run_tool_with_progress
ProductizedShell._tool_event_tracker = _shell_trace._tool_event_tracker
ProductizedShell._render_turn_frame = _shell_trace._render_turn_frame
ProductizedShell._render_tool_frame = _shell_trace._render_tool_frame
ProductizedShell._tool_frame_phases = _shell_trace._tool_frame_phases
ProductizedShell._tool_event_lines = _shell_trace._tool_event_lines
ProductizedShell._tool_event_summary = _shell_trace._tool_event_summary
ProductizedShell._tool_trace_line = _shell_trace._tool_trace_line
ProductizedShell._render_pending_entries = _shell_trace._render_pending_entries
ProductizedShell._render_entry = _shell_trace._render_entry
ProductizedShell._growth_panel_lines = _shell_trace._growth_panel_lines
ProductizedShell._recent_activity_lines = _shell_trace._recent_activity_lines
ProductizedShell._recent_experience_lines = _shell_trace._recent_experience_lines
ProductizedShell._displayable_experiences = _shell_trace._displayable_experiences
ProductizedShell._should_display_experience = _shell_trace._should_display_experience
ProductizedShell._format_experience_status = _shell_trace._format_experience_status
ProductizedShell._growth_progress_counts = _shell_trace._growth_progress_counts
ProductizedShell._growth_progress_bar = _shell_trace._growth_progress_bar
ProductizedShell._styled_growth_progress_bar = _shell_trace._styled_growth_progress_bar
ProductizedShell._render_chat_entry = _shell_trace._render_chat_entry
ProductizedShell._history_row_width = _shell_trace._history_row_width
ProductizedShell._queue_preview_row_width = _shell_trace._queue_preview_row_width
ProductizedShell._pad_history_line = _shell_trace._pad_history_line
ProductizedShell._pad_queue_preview_line = _shell_trace._pad_queue_preview_line
ProductizedShell._center_brand_block = _shell_trace._center_brand_block
ProductizedShell._render_growth_mark = _shell_trace._render_growth_mark
ProductizedShell._render_guardian_mark = _shell_trace._render_guardian_mark

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
