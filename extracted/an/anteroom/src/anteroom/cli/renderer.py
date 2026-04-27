"""Rich-based terminal output for the CLI chat."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import sys
import time
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from rich.console import Console
from rich.markdown import Markdown
from rich.markup import escape
from rich.status import Status
from rich.style import Style
from rich.text import Text
from rich.theme import Theme

from ..services.user_errors import format_user_error
from .density import ToolResultDensity, collapse_diff_hunks, densify_output
from .themes import CliTheme

console = Console(stderr=True)
# Separate console for stdout markdown rendering (not stderr)
_stdout_console = Console()
_stdout = sys.stdout

# ---------------------------------------------------------------------------
# Theme — loaded from config, defaults to midnight.
# All color references go through _theme instead of hardcoded values.
# ---------------------------------------------------------------------------

_theme: CliTheme = CliTheme.load("midnight")
_ANSI_ESCAPE_RE = re.compile(
    r"(?:"
    r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\|$)"  # OSC
    r"|\x9d[^\x07\x9c]*(?:\x07|\x9c|$)"  # 8-bit OSC
    r"|\x1b[PX^_][^\x1b]*(?:\x1b\\|$)"  # DCS/SOS/PM/APC
    r"|[\x90\x98\x9e\x9f][^\x9c]*(?:\x9c|$)"  # 8-bit DCS/SOS/PM/APC
    r"|\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
    r"|\x9b[0-?]*[ -/]*[@-~]"
    r")"
)
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")


def set_theme(theme: CliTheme) -> None:
    """Set the active theme. Called during REPL/exec startup."""
    global _theme
    _theme = theme
    _refresh_aliases()
    _apply_markdown_theme()


# Backward-compatible module-level aliases for code that imports these.
# These are properties that delegate to the active theme.
GOLD = _theme.accent
SLATE = _theme.secondary
BLUE = _theme.logo_blue
MUTED = _theme.muted
CHROME = _theme.chrome
ERROR_RED = _theme.error


def _refresh_aliases() -> None:
    """Update module-level color aliases after a theme change."""
    global GOLD, SLATE, BLUE, MUTED, CHROME, ERROR_RED
    GOLD = _theme.accent
    SLATE = _theme.secondary
    BLUE = _theme.logo_blue
    MUTED = _theme.muted
    CHROME = _theme.chrome
    ERROR_RED = _theme.error


def _apply_markdown_theme() -> None:
    """Apply the active theme's inline-code color onto both consoles.

    Rich uses the ``markdown.code`` style for inline code spans.  The default
    is ``bold cyan on black`` which creates a harsh filled-chip look.  We
    override it with a subtle themed foreground and no background.

    This helper runs during startup and on theme changes, so it must be
    idempotent rather than stacking repeated ``push_theme()`` calls.
    """
    color = _theme.code_inline or _theme.secondary
    if not color:
        return
    override = Theme({"markdown.code": Style(color=color, bold=True)})
    for c in (console, _stdout_console):
        if getattr(c, "_anteroom_markdown_theme_applied", False):
            c.pop_theme()
        c.push_theme(override)
        setattr(c, "_anteroom_markdown_theme_applied", True)


def _strip_terminal_control(text: str) -> str:
    """Remove untrusted control sequences before raw terminal writes."""
    return _CONTROL_CHAR_RE.sub("", _ANSI_ESCAPE_RE.sub("", text))


_ESC_HINT_DELAY: float = 5.0  # seconds before showing "esc to cancel" hint
_STALL_THRESHOLD: float = 15.0  # seconds before showing API stall warning
_REPL_THINKING_REVEAL_DELAY: float = 2.0  # seconds before first REPL thinking line


def use_stdout_console() -> None:
    """Switch renderer to REPL-compatible mode.

    Routes Rich console output through ``sys.stdout`` (the ``patch_stdout``
    proxy) so prompt_toolkit can manage cursor positioning — the prompt and
    bottom toolbar stay anchored at the terminal bottom while output scrolls
    above.

    A duplicated stderr fd is kept as ``_stdout`` for raw ANSI escape writes
    (thinking spinner, tool ticker) that need direct terminal access without
    proxy buffering.

    Call from inside ``patch_stdout()`` context.
    """
    global console, _stdout_console, _stdout, _repl_mode
    # Rich consoles write through the patch_stdout proxy so prompt_toolkit
    # knows about output and can keep the prompt at the bottom.
    console = Console(file=sys.stdout, force_terminal=True)
    _stdout_console = Console(file=sys.stdout, force_terminal=True)
    # Raw ANSI writes (spinners, tickers) go to a real stderr fd to avoid
    # proxy buffering and allow carriage-return cursor manipulation.
    _real_stderr = os.fdopen(os.dup(sys.stderr.fileno()), "w", newline="")
    _stdout = _real_stderr
    _repl_mode = True
    _apply_markdown_theme()


def write_raw(text: str) -> None:
    """Write text directly to the real terminal fd, bypassing patch_stdout.

    Used for sub-prompt text (approval prompts, ask_user) that must be
    visible immediately without buffering through prompt_toolkit's proxy.
    """
    if _stdout:
        _stdout.write(text)
        _stdout.flush()


def configure_streaming(
    *,
    enabled: bool = True,
    refresh_hz: float = 20.0,
    code_fence_container: bool = True,
    exec_mode: bool = False,
    live_in_exec_mode: bool = False,
) -> None:
    """Install a :class:`StreamingMarkdownRenderer` for the active session.

    Called once by the REPL/exec bootstrap after ``use_stdout_console``
    (if applicable) so the renderer writes into the same console as
    downstream static prints. Idempotent: later calls replace the
    previous renderer (cleanly stopping it if active).

    When Live is unavailable at the console level (non-TTY, NO_COLOR,
    exec without opt-in, or ``enabled=False``), ``render_token`` stays
    on the historical buffer-only path so there is zero observable
    change.
    """
    global _streaming_renderer
    from .streaming import StreamingMarkdownRenderer

    # Tear down any previous renderer before replacing.
    if _streaming_renderer is not None:
        try:
            _streaming_renderer.stop()
        except Exception:
            pass

    _streaming_renderer = StreamingMarkdownRenderer(
        console=_stdout_console,
        enabled=enabled,
        refresh_hz=refresh_hz,
        code_fence_container=code_fence_container,
        exec_mode=exec_mode,
        live_in_exec_mode=live_in_exec_mode,
        finalize_render=render_assistant_prose,
    )


def reset_streaming() -> None:
    """Clear the active streaming renderer (tests, teardown)."""
    global _streaming_renderer
    if _streaming_renderer is not None:
        try:
            _streaming_renderer.stop()
        except Exception:
            pass
    _streaming_renderer = None


def configure_thresholds(
    esc_hint_delay: float | None = None,
    stall_display: float | None = None,
    stall_warning: float | None = None,
    throughput_threshold: float | None = None,
) -> None:
    """Override default visual thresholds from config."""
    global _ESC_HINT_DELAY, _MID_STREAM_STALL, _STALL_THRESHOLD, _THROUGHPUT_STALL_THRESHOLD
    if esc_hint_delay is not None:
        _ESC_HINT_DELAY = esc_hint_delay
    if stall_display is not None:
        _MID_STREAM_STALL = stall_display
    if stall_warning is not None:
        _STALL_THRESHOLD = stall_warning
    if throughput_threshold is not None:
        _THROUGHPUT_STALL_THRESHOLD = throughput_threshold


# Response buffer (tokens collected silently, rendered on completion)
_streaming_buffer: list[str] = []

# Live-markdown streaming state (#1365). Initialised to None; wired from the
# REPL/exec bootstrap via ``configure_streaming()``. When non-None and Live
# is available, ``render_token``/``flush_buffered_text``/``render_response_end``
# route through the Live renderer; otherwise the buffer-only path runs
# exactly as before (complete backward compatibility).
_streaming_renderer: Any = None  # StreamingMarkdownRenderer | None

# Spinner state
_thinking_start: float = 0
_spinner: Status | None = None
_last_spinner_update: float = 0
_thinking_ticker_task: asyncio.Task[None] | None = None
_thinking_cancelled: bool = False  # guard flag to suppress stale ticker output (#937)
_thinking_line_visible: bool = False

# Lifecycle phase tracking
_thinking_phase: str = ""  # current phase: connecting, waiting, streaming, tool_exec
_thinking_phase_data: dict[str, Any] = {}
_thinking_tokens: int = 0  # token counter during streaming
_streaming_chars: int = 0  # character counter during streaming
_last_chunk_time: float = 0  # monotonic time of last token (for stall detection)
_phase_start_time: float = 0  # monotonic time when current phase began
_MID_STREAM_STALL: float = 5.0  # seconds of silence before marking "stalled"

# Tool execution phase tracking (#1366)
_active_tool_count: int = 0
_active_tool_names: list[str] = []
_active_tool_summaries: list[str] = []

# Throughput-based stall detection (#774): catches slow-trickle streams where
# tiny chunks arrive often enough to avoid gap-based detection but overall
# throughput is extremely low (e.g. 6 chars/sec over 2 minutes).
_throughput_window: deque[tuple[float, int]] = deque()  # (monotonic_time, chars) entries
_THROUGHPUT_STALL_THRESHOLD: float = 30.0  # chars/sec below which "stalled" triggers
_THROUGHPUT_WINDOW_SECS: float = 10.0  # rolling window size
_THROUGHPUT_WARMUP_SECS: float = 8.0  # don't trigger throughput stall before this


def _thinking_elapsed() -> float:
    """Return elapsed thinking time, clamped for unset or invalid starts."""
    if _thinking_start <= 0:
        return 0.0
    return max(0.0, time.monotonic() - _thinking_start)


# Tool call timing
_tool_start: float = 0
_tool_ticker_task: asyncio.Task[None] | None = None
_tool_ticker_summary: str = ""
_tool_spinner: Status | None = None
_tool_line_visible: bool = False

# Dedup tracking for repeated similar tool calls
_dedup_key: str = ""  # tool action type (e.g. "Editing", "Reading", "bash")
_dedup_count: int = 0
_dedup_first_summary: str = ""  # first summary in the group (printed immediately)

# Legacy alias used by tests — kept in sync with _dedup_key
_dedup_summary: str = ""

# Whether dedup is enabled (set from config)
_tool_dedup_enabled: bool = True

# Track whether we've started a tool call batch (for spacing)
_tool_batch_active: bool = False

# ---------------------------------------------------------------------------
# Plan checklist state
# ---------------------------------------------------------------------------

_plan_steps: list[dict[str, str]] = []  # [{"text": "...", "status": "pending|in_progress|complete"}]
_plan_visible: bool = False
_plan_written_lines: int = 0  # lines currently on screen (for cursor-up on redraw)


# ---------------------------------------------------------------------------
# Plan checklist API
# ---------------------------------------------------------------------------


def start_plan(steps: list[str]) -> None:
    """Initialize the plan checklist with step descriptions.

    Call this when a plan is approved and execution begins.
    The checklist is rendered above the thinking line during agentic runs.
    """
    global _plan_steps, _plan_visible, _plan_written_lines
    _plan_steps = [{"text": s, "status": "pending"} for s in steps]
    _plan_visible = True
    _plan_written_lines = 0


def update_plan_step(index: int, status: str) -> None:
    """Update a plan step status: 'pending', 'in_progress', or 'complete'.

    Triggers a redraw if the thinking block is currently displayed.
    """
    if not _plan_steps or index < 0 or index >= len(_plan_steps):
        return
    _plan_steps[index]["status"] = status

    # Redraw if thinking block is on screen
    if _repl_mode and _thinking_start and _stdout and _plan_written_lines > 0:
        elapsed = time.monotonic() - _thinking_start
        _write_thinking_block(elapsed)


def clear_plan() -> None:
    """Clear plan state entirely (e.g. on /plan off or new conversation)."""
    global _plan_steps, _plan_visible, _plan_written_lines
    _plan_steps = []
    _plan_visible = False
    _plan_written_lines = 0


def _plan_block_height() -> int:
    """Number of terminal lines the plan block occupies (0 if no plan)."""
    if not _plan_visible or not _plan_steps:
        return 0
    return len(_plan_steps) + 1  # header line + one line per step


def _collapse_plan() -> None:
    """Replace the plan checklist with a one-line summary.

    Called when the agentic run completes (done event).
    """
    global _plan_visible, _plan_written_lines
    if not _plan_steps:
        _plan_visible = False
        _plan_written_lines = 0
        return

    completed = sum(1 for s in _plan_steps if s["status"] == "complete")
    total = len(_plan_steps)

    if _repl_mode and _stdout:
        green = _theme.ansi_fg("success")
        muted = _theme.ansi_fg("muted")
        rst = _theme.ansi_reset
        if completed == total:
            line = f"  {green}\u2713 Plan: {completed}/{total} steps complete{rst}"
        else:
            line = f"  {muted}\u25cb Plan: {completed}/{total} steps complete{rst}"
        _stdout.write(f"{line}\n")
        _stdout.flush()

    _plan_visible = False
    _plan_written_lines = 0


def get_plan_steps() -> list[dict[str, str]]:
    """Return the current plan steps (for testing/inspection)."""
    return list(_plan_steps)


def is_plan_visible() -> bool:
    """Return whether a plan checklist is currently active."""
    return _plan_visible


# ---------------------------------------------------------------------------
# Verbosity
# ---------------------------------------------------------------------------


class Verbosity(Enum):
    COMPACT = "compact"
    DETAILED = "detailed"
    VERBOSE = "verbose"


_verbosity: Verbosity = Verbosity.COMPACT

# Tool call history for /detail replay
_tool_history: list[dict[str, Any]] = []
_current_turn_tools: list[dict[str, Any]] = []


def get_verbosity() -> Verbosity:
    return _verbosity


def set_verbosity(v: Verbosity) -> None:
    global _verbosity
    _verbosity = v


_show_rag_status: bool = True
_show_memory_recall_status: bool = True


def set_rag_status_visible(show: bool) -> None:
    global _show_rag_status
    _show_rag_status = show


def set_memory_recall_status_visible(show: bool) -> None:
    global _show_memory_recall_status
    _show_memory_recall_status = show


def set_tool_dedup(enabled: bool) -> None:
    global _tool_dedup_enabled
    _tool_dedup_enabled = enabled


def cycle_verbosity() -> Verbosity:
    global _verbosity
    order = [Verbosity.COMPACT, Verbosity.DETAILED, Verbosity.VERBOSE]
    idx = order.index(_verbosity)
    _verbosity = order[(idx + 1) % len(order)]
    return _verbosity


# ---------------------------------------------------------------------------
# Tool-result density (#1367)
#
# Orthogonal to ``Verbosity``. ``Verbosity`` controls turn-level summary /
# legacy output style; ``ToolResultDensity`` controls the per-tool end-of-call
# body rendering. Default is ``NORMAL`` which is byte-identical to the
# pre-#1367 tool-end rendering path — the renderer routes through
# ``densify_output`` / ``collapse_diff_hunks`` only when the density is
# non-normal, so zero-config users see no change.
# ---------------------------------------------------------------------------


_density: ToolResultDensity = ToolResultDensity.NORMAL

# User-facing tunables sourced from ``CliDensityConfig``. Set by ``apply_config``
# during REPL/exec startup; the renderer reads these when the mode is non-normal.
_density_head_lines: int = 3
_density_tail_lines: int = 2
_density_diff_context_lines: int = 3
_density_collapse_repeats: bool = True

# Turn-local flag: True once the "/detail to expand" hint has been shown in
# compact/minimal mode; reset each turn.
_density_hint_shown: bool = False

# Rolling state for ``cli.density.collapse_repeats`` (#1367). When enabled and
# density is COMPACT/MINIMAL, consecutive successful tool calls that produce
# the same (tool_name, output shape) are collapsed to a single summary line
# followed by a ``× N`` count. Reset at turn boundaries and on density flush.
_repeat_shape_hash: str = ""
_repeat_count: int = 0
_repeat_summary: str = ""

# When True, the diff-hunk renderer bypasses ``collapse_diff_hunks`` and shows
# the full un-collapsed diff regardless of active density. Used by
# ``/expand`` (#1367) for diff-backed tool outputs.
_force_full_diff: bool = False


def get_density() -> ToolResultDensity:
    return _density


def set_density(density: ToolResultDensity) -> None:
    """Set the active tool-result density (called by config loader and /density)."""
    global _density
    _density = density


def configure_density(
    *,
    mode: ToolResultDensity | None = None,
    head_lines: int | None = None,
    tail_lines: int | None = None,
    diff_context_lines: int | None = None,
    collapse_repeats: bool | None = None,
) -> None:
    """Apply density knobs loaded from ``CliDensityConfig``.

    Any arguments left as ``None`` keep their current value.
    """
    global _density, _density_head_lines, _density_tail_lines
    global _density_diff_context_lines, _density_collapse_repeats
    if mode is not None:
        _density = mode
    if head_lines is not None:
        _density_head_lines = max(0, head_lines)
    if tail_lines is not None:
        _density_tail_lines = max(0, tail_lines)
    if diff_context_lines is not None:
        _density_diff_context_lines = max(0, diff_context_lines)
    if collapse_repeats is not None:
        _density_collapse_repeats = bool(collapse_repeats)


def clear_turn_history() -> None:
    """Clear current turn tool history. Called at start of each turn."""
    global _streaming_buffer, _density_hint_shown
    _current_turn_tools.clear()
    _streaming_buffer = []
    _density_hint_shown = False
    _flush_repeat_collapse()


def _repeat_shape_key(tool_name: str, output: Any) -> str:
    """Compute a shape hash for collapse-repeats detection (#1367).

    The key combines ``tool_name`` with a stable hash of the entire output
    payload — including internal ``_``-prefixed fields such as
    ``_old_content`` / ``_new_content``. This ensures two distinct
    ``write_file`` / ``edit_file`` diffs for the same path NEVER collapse
    into a single ``↻ … × N`` line (which would hide real file changes).

    Implementation note: we serialise the full dict (no key stripping) and
    reduce it to a short SHA-256 prefix so the hash stays cheap to compare
    even when diff blobs are large. Non-dict outputs hash their ``str``
    representation; ``None`` yields a distinguished empty payload.
    """
    if output is None:
        payload = ""
    elif isinstance(output, dict):
        # Include every field — including ``_old_content`` / ``_new_content``
        # — so two distinct diffs never produce the same shape key.
        try:
            payload = json.dumps(output, sort_keys=True, default=str)
        except Exception:
            payload = repr(output)
    elif isinstance(output, str):
        payload = output
    else:
        try:
            payload = repr(output)
        except Exception:
            payload = ""
    digest = hashlib.sha256(payload.encode("utf-8", errors="replace")).hexdigest()[:16]
    return f"{tool_name}:{digest}"


def _flush_repeat_collapse() -> None:
    """Emit the ``× N`` summary for a pending collapse-repeats run, if any.

    Called when a different-shape tool result arrives, at turn boundaries,
    when density is flipped, and before ``/expand`` renders.
    """
    global _repeat_shape_hash, _repeat_count, _repeat_summary
    if _repeat_count > 1:
        label = f"↻ {_repeat_summary} × {_repeat_count}"
        console.print(f"    [{MUTED}]{escape(label)}[/{MUTED}]")
    _repeat_shape_hash = ""
    _repeat_count = 0
    _repeat_summary = ""


def save_turn_history() -> None:
    """Save current turn tools to history. Called at end of each turn."""
    global _tool_batch_active
    _flush_dedup()
    _flush_repeat_collapse()
    _tool_batch_active = False
    if _current_turn_tools:
        _tool_history.clear()
        _tool_history.extend(_current_turn_tools)


# ---------------------------------------------------------------------------
# Tool call summary helpers
# ---------------------------------------------------------------------------


def _humanize_tool(tool_name: str, arguments: dict[str, Any]) -> str:
    """Convert tool_name + args into a human-readable breadcrumb."""
    name_lower = tool_name.lower()

    # Built-in tools: extract the key argument
    if name_lower == "bash":
        cmd = arguments.get("command", "")
        if len(cmd) > 100:
            cmd = cmd[:97] + "..."
        return f"bash {cmd}"
    elif name_lower in ("file_read", "read_file"):
        path = arguments.get("path", arguments.get("file_path", ""))
        return f"Reading {_short_path(path)}"
    elif name_lower in ("file_write", "write_file"):
        path = arguments.get("path", arguments.get("file_path", ""))
        return f"Writing {_short_path(path)}"
    elif name_lower in ("file_edit", "edit_file"):
        path = arguments.get("path", arguments.get("file_path", ""))
        return f"Editing {_short_path(path)}"
    elif name_lower in ("grep", "search", "ripgrep"):
        pattern = arguments.get("pattern", arguments.get("query", ""))
        return f"Searching for '{pattern}'"
    elif name_lower in ("glob", "glob_files", "find_files"):
        pattern = arguments.get("pattern", "")
        return f"Finding {pattern}"
    elif name_lower == "run_agent":
        prompt = arguments.get("prompt", "")
        if len(prompt) > 60:
            prompt = prompt[:57] + "..."
        return f"Sub-agent: {prompt}"
    elif name_lower == "list_directory":
        path = arguments.get("path", ".")
        return f"Listing {_short_path(path)}"

    # MCP / unknown tools: show name + first string arg
    first_str = ""
    for v in arguments.values():
        if isinstance(v, str) and v:
            first_str = v
            if len(first_str) > 40:
                first_str = first_str[:37] + "..."
            break
    if first_str:
        return f"{tool_name} {first_str}"
    return tool_name


def _dedup_key_from_summary(summary: str) -> str:
    """Extract a dedup grouping key from a humanized tool summary.

    Groups by the action verb (e.g. "Editing", "Reading", "Writing", "bash")
    so consecutive edits to different files collapse together.
    """
    # Known action prefixes from _humanize_tool
    for prefix in ("Editing", "Reading", "Writing", "Searching", "Finding", "Listing", "Sub-agent:"):
        if summary.startswith(prefix):
            return prefix
    # bash commands: group all bash calls together
    if summary.startswith("bash "):
        return "bash"
    # MCP / unknown tools: use the tool name (first word)
    return summary.split(" ", 1)[0] if " " in summary else summary


def _dedup_flush_label(key: str, count: int) -> str:
    """Build a human-readable summary for a flushed dedup group."""
    verb_map = {
        "Editing": "edited",
        "Reading": "read",
        "Writing": "wrote",
        "Searching": "searched",
        "Finding": "found patterns in",
        "Listing": "listed",
        "bash": "ran",
    }
    verb = verb_map.get(key, f"called {key}")
    noun = "files" if key in ("Editing", "Reading", "Writing") else "times"
    return f"... {verb} {count} {noun} total"


def _short_path(path: str) -> str:
    """Shorten absolute path using ~ for home and cwd-relative."""
    if not path:
        return path
    home = os.path.expanduser("~")
    cwd = os.getcwd()
    # Try cwd-relative first
    try:
        rel = os.path.relpath(path, cwd)
        if not rel.startswith(".."):
            return rel
    except ValueError:
        pass
    # Fall back to ~-relative
    if path.startswith(home):
        return "~" + path[len(home) :]
    return path


def _format_tokens(n: int) -> str:
    """Format token count: 1234 -> '1.2k', 128000 -> '128k'."""
    if n >= 1000:
        k = n / 1000
        if k >= 10:
            return f"{k:.0f}k"
        return f"{k:.1f}k"
    return str(n)


def _error_summary(output: Any) -> str:
    """Extract a one-line error summary from tool output."""
    if not isinstance(output, dict):
        return ""
    err = output.get("error", "")
    if err:
        # First line only, truncated
        first_line = str(err).split("\n")[0]
        if len(first_line) > 80:
            first_line = first_line[:77] + "..."
        return first_line
    return ""


def _output_summary(output: Any) -> str:
    """Extract a brief output summary for detailed mode."""
    if not isinstance(output, dict):
        return ""
    if "error" in output:
        return _error_summary(output)
    if "content" in output:
        content = output["content"]
        if isinstance(content, str):
            lines = content.count("\n") + 1
            chars = len(content)
            if chars > 80:
                return f"{lines} lines, {chars:,} chars"
            # Short enough to show inline
            oneline = content.replace("\n", " ").strip()
            if len(oneline) > 60:
                return oneline[:57] + "..."
            return oneline
    if "stdout" in output:
        stdout: str = output.get("stdout", "")
        if stdout:
            lines = stdout.count("\n") + 1
            oneline = stdout.split("\n")[0].strip()
            if lines > 1:
                if len(oneline) > 40:
                    oneline = oneline[:37] + "..."
                return f"{oneline} (+{lines - 1} lines)"
            if len(oneline) > 60:
                return oneline[:57] + "..."
            return oneline
    return ""


# ---------------------------------------------------------------------------
# Busy status for toolbar integration
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BusyStatus:
    """Busy-state data for rendering in the bottom toolbar."""

    thinking_text: str
    tool_label: str | None = None
    show_cancel_hint: bool = False


# Footer mode: when True, thinking/tool tickers update the toolbar instead
# of writing raw ANSI escape sequences to the terminal.  Set when _repl_mode
# is True and no plan checklist is active.
_footer_mode: bool = False

# Callback set by repl.py to invalidate+redraw the toolbar.
_toolbar_invalidator: Callable[[], None] | None = None

# Probe set by repl.py; returns True only while the prompt_toolkit app is
# actively running (i.e. the toolbar surface is live). During an active turn
# the prompt session is usually no longer running, so footer mode must fall
# back to the raw in-place thinking line.
_toolbar_is_active: Callable[[], bool] | None = None

# Probe set by repl.py while the concurrent input collector is inside
# ``PromptSession.prompt_async()``.  This is distinct from toolbar
# availability: prompt_toolkit may be accepting queued input even when the
# toolbar active probe is false.
_prompt_is_active: Callable[[], bool] | None = None


def _invalidate_footer_toolbar() -> None:
    """Repaint the footer immediately when the live busy state changes."""
    if _footer_mode and _toolbar_invalidator:
        _toolbar_invalidator()


def format_busy_status_toolbar(busy_status: BusyStatus | None) -> list[tuple[str, str]]:
    """Format only the live busy fragments for the bottom toolbar."""
    parts: list[tuple[str, str]] = []
    if busy_status is None:
        return parts
    tool_label = _strip_terminal_control(busy_status.tool_label) if busy_status.tool_label else ""
    thinking_text = _strip_terminal_control(busy_status.thinking_text) if busy_status.thinking_text else ""
    if tool_label and not thinking_text:
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))
        parts.append(("class:bottom-toolbar.model", tool_label))
    if thinking_text:
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))
        parts.append(("class:bottom-toolbar.tokens-warn", thinking_text))
    if busy_status.show_cancel_hint:
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))
        parts.append(("class:bottom-toolbar.dim", "esc to cancel"))
    return parts


def get_busy_status() -> BusyStatus | None:
    """Return current busy state for toolbar rendering, or None if idle."""
    if not _thinking_start and not _tool_ticker_summary:
        return None
    thinking_text = ""
    show_cancel = False
    if _thinking_start:
        elapsed = time.monotonic() - _thinking_start
        # Build plain text for the toolbar — _build_thinking_text returns raw
        # ANSI escapes which would render as garbled text in prompt_toolkit.
        if elapsed >= _REPL_THINKING_REVEAL_DELAY or _plan_visible:
            suffix = _phase_suffix(elapsed)
            label = _phase_label()
            thinking_text = f"{label} {elapsed:.0f}s"
            if suffix:
                thinking_text += f"  {suffix}"
            thinking_text = _strip_terminal_control(thinking_text)
        show_cancel = elapsed >= _ESC_HINT_DELAY
    tool_label = _strip_terminal_control(_tool_ticker_summary) or None
    return BusyStatus(
        thinking_text=thinking_text,
        tool_label=tool_label,
        show_cancel_hint=show_cancel,
    )


# ---------------------------------------------------------------------------
# Thinking spinner
# ---------------------------------------------------------------------------


_repl_mode: bool = False


async def _thinking_ticker() -> None:
    """Background task that updates the thinking spinner every 0.5s."""
    try:
        while True:
            await asyncio.sleep(0.5)
            if _thinking_cancelled:
                return
            if _thinking_start:
                elapsed = time.monotonic() - _thinking_start
                suffix = _phase_suffix(elapsed)
                if _spinner:
                    plabel = _phase_label()
                    label = f"[{GOLD}]{plabel}[/] [{CHROME}]{elapsed:.0f}s[/{CHROME}]"
                    if suffix:
                        label += f"  [{MUTED}]{suffix}[/{MUTED}]"
                    _spinner.update(label)
                elif _footer_mode and _toolbar_invalidator:
                    _toolbar_invalidator()
                elif _repl_mode:
                    _write_thinking_line(elapsed)
    except asyncio.CancelledError:
        return


def start_thinking(*, newline: bool = False) -> None:
    """Show a spinner with timer while AI is generating.

    In REPL mode, pass ``newline=True`` on the first call per user message
    so the visual separator and "Thinking..." text are written as a single
    atomic write, preventing prompt_toolkit's cursor teardown from
    interleaving between them (#249).  Retry calls should omit it.
    """
    global _thinking_start, _spinner, _last_spinner_update, _tool_batch_active, _thinking_ticker_task
    global _thinking_phase, _thinking_phase_data, _thinking_tokens
    global _streaming_chars, _last_chunk_time, _phase_start_time
    global _retrying_info
    global _plan_written_lines, _thinking_cancelled, _thinking_line_visible, _footer_mode
    _flush_dedup()
    _thinking_cancelled = False
    # Emit spacing after tool call block before AI narration text (#680).
    # Must happen here because start_thinking() is called before
    # render_response_end(), which would otherwise handle this.
    if _tool_batch_active:
        console.print()
    _tool_batch_active = False
    _reset_tool_phase()
    _thinking_start = time.monotonic()
    _thinking_phase = ""
    _thinking_phase_data = {}
    _thinking_tokens = 0
    _streaming_chars = 0
    _last_chunk_time = 0
    _phase_start_time = _thinking_start
    _retrying_info = {}
    _throughput_window.clear()
    _last_spinner_update = _thinking_start
    _thinking_line_visible = False
    # Reset plan written lines — the block will be freshly written
    _plan_written_lines = 0
    if _repl_mode:
        # Footer mode: toolbar owns the busy indicator.  Only active when
        # no plan checklist is on screen (plan uses raw cursor-up rendering).
        _inv = _toolbar_invalidator
        toolbar_ready = _inv is not None and (_toolbar_is_active is None or _toolbar_is_active())
        if not (_plan_visible and _plan_steps) and toolbar_ready and _inv is not None:
            _footer_mode = True
            _spinner = None
            _inv()
        else:
            _footer_mode = False
            # Rich Status conflicts with prompt_toolkit's patch_stdout, so
            # we write a plain "Thinking..." line and overwrite it in-place
            # via ANSI escape codes as the timer ticks.
            if newline and _stdout:
                # Atomic \n + initial thinking block prevents prompt_toolkit race (#249).
                if _plan_visible and _plan_steps:
                    # Write newline then full plan + thinking block
                    _stdout.write("\n")
                    _stdout.flush()
                    _write_thinking_block(0.0)
                else:
                    _stdout.write("\n")
                    _stdout.flush()
            elif _plan_visible and _plan_steps:
                _write_thinking_line(0.0)
            _spinner = None
    else:
        _spinner = Status(f"[{GOLD}]Thinking...[/]", console=console, spinner="dots12")
        _spinner.start()
    # Cancel any existing ticker before creating a new one (prevents task leak)
    if _thinking_ticker_task is not None:
        _thinking_ticker_task.cancel()
        _thinking_ticker_task = None
    # Start background ticker
    try:
        loop = asyncio.get_running_loop()
        _thinking_ticker_task = loop.create_task(_thinking_ticker())
    except RuntimeError:
        _thinking_ticker_task = None


def _build_thinking_text(
    elapsed: float,
    *,
    error_msg: str = "",
    countdown: int = 0,
    cancel_msg: str = "",
) -> str:
    """Build the thinking line text (without cursor/clear prefixes)."""
    gold = _theme.ansi_fg("accent")
    timer_c = _theme.ansi_fg("chrome")
    muted = _theme.ansi_fg("muted")
    err_c = _theme.ansi_fg("error")
    rst = _theme.ansi_reset

    if (
        elapsed < _REPL_THINKING_REVEAL_DELAY
        and not error_msg
        and not cancel_msg
        and countdown <= 0
        and not _plan_visible
        # #1428: accepted phase bypasses the calm window so the user gets an
        # immediate ack that the prompt landed. Subsequent phases (connecting,
        # waiting) still defer to the reveal delay for minimal early chrome.
        and _thinking_phase != "accepted"
    ):
        return ""

    label = _strip_terminal_control(_phase_label())

    if elapsed < 3.0 and not error_msg and not cancel_msg:
        return f"{gold}{label}{rst}"

    timer = f"{timer_c}{elapsed:.0f}s{rst}"
    if cancel_msg:
        return f"{gold}{label}{rst} {timer}  {muted}{cancel_msg}{rst}"
    if error_msg:
        err_text = f"  {err_c}{error_msg}{rst}"
        if countdown > 0:
            retry_text = f" \u00b7 {muted}retrying in {countdown}s{rst}"
            hint = f"  {muted}esc to give up{rst}"
            return f"{gold}{label}{rst} {timer}{err_text}{retry_text}{hint}"
        return f"{gold}{label}{rst} {timer}{err_text}"

    hint = f"  {muted}esc to cancel{rst}" if elapsed >= _ESC_HINT_DELAY else ""
    suffix = _phase_suffix(elapsed)
    phase_text = f"  {muted}{suffix}{rst}" if suffix else ""
    return f"{gold}{label}{rst} {timer}{phase_text}{hint}"


def _write_thinking_block(
    elapsed: float,
    *,
    error_msg: str = "",
    countdown: int = 0,
    cancel_msg: str = "",
) -> None:
    """Write the full thinking block: plan checklist (if active) + thinking line.

    Uses cursor-up ANSI codes to redraw the block in place.
    """
    global _plan_written_lines, _thinking_line_visible
    if not _stdout:
        return

    height = _plan_block_height()
    thinking_text = _build_thinking_text(elapsed, error_msg=error_msg, countdown=countdown, cancel_msg=cancel_msg)

    if height == 0:
        # No plan — single-line thinking only
        if not thinking_text:
            if _thinking_line_visible:
                _stdout.write("\r\033[2K")
                _stdout.flush()
            _thinking_line_visible = False
            return
        _stdout.write(f"\r\033[2K{thinking_text}")
        _stdout.flush()
        _thinking_line_visible = True
        return

    if not thinking_text:
        gold = _theme.ansi_fg("accent")
        rst = _theme.ansi_reset
        thinking_text = f"{gold}Thinking...{rst}"

    # Multi-line block: plan header + steps + thinking line
    buf: list[str] = []

    # Move cursor up to the top of the block (if we've written it before)
    if _plan_written_lines > 0:
        up = _plan_written_lines  # lines above the thinking line
        buf.append(f"\033[{up}A")

    # ANSI colors
    green = _theme.ansi_fg("success")
    gold_c = _theme.ansi_fg("accent")
    muted_c = _theme.ansi_fg("muted")
    rst = _theme.ansi_reset

    # Plan header
    buf.append(f"\r\033[2K  {muted_c}\U0001f4cb Plan{rst}\n")

    # Steps
    for step in _plan_steps:
        status = step["status"]
        if status == "complete":
            icon = f"{green}\u2713{rst}"
            text_style = green
        elif status == "in_progress":
            icon = f"{gold_c}\u2192{rst}"
            text_style = gold_c
        else:
            icon = f"{muted_c}\u25cb{rst}"
            text_style = muted_c
        buf.append(f"\r\033[2K    {icon} {text_style}{step['text']}{rst}\n")

    # Thinking line (no trailing newline — cursor stays here)
    buf.append(f"\r\033[2K{thinking_text}")

    _stdout.write("".join(buf))
    _stdout.flush()
    _plan_written_lines = height  # remember how many plan lines we wrote
    _thinking_line_visible = True


def _write_thinking_line(
    elapsed: float,
    *,
    error_msg: str = "",
    countdown: int = 0,
    cancel_msg: str = "",
) -> None:
    """Overwrite the current line with Thinking + elapsed timer + phase status.

    When a plan checklist is active, delegates to ``_write_thinking_block()``
    to render the full plan + thinking block.

    Optional keyword args for special states:
    - ``error_msg``: pale-red inline error replacing phase text
    - ``countdown``: seconds remaining for auto-retry (shown after error_msg)
    - ``cancel_msg``: muted message like "cancelled" (user-initiated, not error)
    """
    if _plan_visible and _plan_steps:
        _write_thinking_block(elapsed, error_msg=error_msg, countdown=countdown, cancel_msg=cancel_msg)
        return

    text_body = _build_thinking_text(elapsed, error_msg=error_msg, countdown=countdown, cancel_msg=cancel_msg)
    if not text_body:
        global _thinking_line_visible
        if _stdout and _thinking_line_visible:
            _stdout.write("\r\033[2K")
            _stdout.flush()
        _thinking_line_visible = False
        return

    text = f"\r\033[2K{text_body}"
    if _stdout:
        _stdout.write(text)
        _stdout.flush()
    _thinking_line_visible = True


def _detach_thinking_line_for_output() -> bool:
    """Move subsequent normal output onto a fresh line when thinking is visible."""
    global _thinking_line_visible
    if _footer_mode:
        return False
    if not (_repl_mode and _stdout and _thinking_start and _thinking_line_visible):
        return False
    _stdout.write("\n")
    _stdout.flush()
    _thinking_line_visible = False
    return True


def update_thinking() -> None:
    """Update the spinner timer (throttled to once per second).

    No-op when the background ticker is running — the ticker handles updates.
    """
    global _last_spinner_update
    if _thinking_ticker_task is not None:
        return
    if _spinner:
        now = time.monotonic()
        if now - _last_spinner_update >= 1.0:
            elapsed = now - _thinking_start
            _spinner.update(f"[{GOLD}]Thinking...[/] [{CHROME}]{elapsed:.0f}s[/{CHROME}]")
            _last_spinner_update = now
    elif _repl_mode:
        now = time.monotonic()
        if now - _last_spinner_update >= 1.0:
            elapsed = now - _thinking_start
            _write_thinking_line(elapsed)
            _last_spinner_update = now


async def stop_thinking(
    *,
    error_msg: str = "",
    cancel_msg: str = "",
    collapse_plan: bool = False,
    quiet: bool = False,
) -> float:
    """Stop the spinner, return elapsed seconds.

    Awaits ticker task termination to prevent output races.

    Optional keyword args control the final thinking line:
    - ``error_msg``: pale-red inline error (system failure)
    - ``cancel_msg``: muted message (user-initiated cancel)
    - ``collapse_plan``: if True, collapse the plan to a one-line summary
    - Neither: clean final line (just "Thinking... Ns")
    - ``quiet``: clear the current thinking line without printing a final status
    """
    global _spinner, _thinking_ticker_task, _thinking_phase, _plan_written_lines
    global _thinking_start, _thinking_line_visible, _footer_mode
    elapsed = 0.0
    # Await ticker termination to prevent race conditions
    if _thinking_ticker_task is not None:
        _thinking_ticker_task.cancel()
        try:
            await _thinking_ticker_task
        except (asyncio.CancelledError, Exception):
            pass
        _thinking_ticker_task = None
    if _spinner:
        elapsed = _thinking_elapsed()
        _spinner.stop()
        _spinner = None
    elif _footer_mode:
        # Footer mode: commit final status via Rich console (through
        # patch_stdout proxy) so prompt_toolkit stays in control.
        # Use Rich markup throughout — _build_thinking_text returns raw
        # ANSI escapes which would render as garbled text in console.print().
        elapsed = _thinking_elapsed()
        if not quiet:
            _thinking_phase = ""
            if error_msg:
                final = (
                    f"[{_theme.accent}]Thinking...[/] [{_theme.chrome}]{elapsed:.0f}s[/]"
                    f"  [{_theme.error}]{error_msg}[/]"
                )
            elif cancel_msg:
                final = (
                    f"[{_theme.accent}]Thinking...[/] [{_theme.chrome}]{elapsed:.0f}s[/]"
                    f"  [{_theme.muted}]{cancel_msg}[/]"
                )
            else:
                final = f"[{_theme.accent}]Thinking...[/] [{_theme.chrome}]{elapsed:.0f}s[/]"
            if final:
                console.print(final)
        _footer_mode = False
        if _toolbar_invalidator:
            _toolbar_invalidator()
    else:
        elapsed = _thinking_elapsed()
        if _repl_mode and _stdout:
            # Clear the plan block if it's on screen
            if _plan_written_lines > 0:
                # Move cursor up to the top of the plan block
                _stdout.write(f"\033[{_plan_written_lines}A")
                # Clear all plan lines + thinking line
                for _ in range(_plan_written_lines + 1):
                    _stdout.write("\r\033[2K\n")
                # Move back up one line (we wrote one too many \n)
                _stdout.write("\033[1A")
                _plan_written_lines = 0

            if collapse_plan:
                _collapse_plan()

            if quiet:
                if _thinking_line_visible or _plan_written_lines > 0:
                    _stdout.write("\r\033[2K")
                    _stdout.flush()
            elif error_msg:
                _write_thinking_line(elapsed, error_msg=error_msg)
                _stdout.write("\n")
                _stdout.flush()
            elif cancel_msg:
                _write_thinking_line(elapsed, cancel_msg=cancel_msg)
                _stdout.write("\n")
                _stdout.flush()
            else:
                # Clean final line: just "Thinking... Ns" — no phase, no hint.
                _thinking_phase = ""
                gold = _theme.ansi_fg("accent")
                timer_c = _theme.ansi_fg("chrome")
                rst = _theme.ansi_reset
                _stdout.write(f"\r\033[2K{gold}Thinking...{rst} {timer_c}{elapsed:.0f}s{rst}\n")
                _stdout.flush()
    _thinking_start = 0
    _thinking_line_visible = False
    return elapsed


def stop_thinking_sync(*, cancel_msg: str = "") -> float:
    """Synchronous fallback for stop_thinking (KeyboardInterrupt handlers).

    Does not await the ticker — use only when an event loop is unavailable.
    Renders an optional *cancel_msg* in all three render modes so the user
    sees immediate visual acknowledgment from the keybinding handler thread.
    """
    global _spinner, _thinking_ticker_task, _plan_written_lines, _thinking_start
    global _thinking_cancelled, _thinking_line_visible, _footer_mode
    elapsed = 0.0
    _thinking_cancelled = True  # suppress stale ticker output before cancel propagates (#937)
    if _thinking_ticker_task is not None:
        _thinking_ticker_task.cancel()
        _thinking_ticker_task = None
    if _spinner:
        elapsed = _thinking_elapsed()
        _spinner.stop()
        _spinner = None
    elif _footer_mode:
        elapsed = _thinking_elapsed()
        # Footer mode: toolbar owns the busy indicator.  Clear footer state
        # FIRST to prevent the ticker from writing concurrently, then render
        # the cancel ack directly to the raw stderr fd.
        #
        # Cannot use console.print() here — it routes through patch_stdout
        # proxy which requires the event loop to flush.  _stdout bypasses
        # the proxy (same pattern as approval prompts via write_raw()).
        _footer_mode = False
        if cancel_msg and _stdout:
            gold = _theme.ansi_fg("accent")
            timer_c = _theme.ansi_fg("chrome")
            muted = _theme.ansi_fg("muted")
            rst = _theme.ansi_reset
            text = f"{gold}Thinking...{rst} {timer_c}{elapsed:.0f}s{rst}  {muted}{cancel_msg}{rst}"
            _stdout.write(f"\r\033[2K{text}\n")
            _stdout.flush()
        if _toolbar_invalidator:
            _toolbar_invalidator()
    else:
        elapsed = _thinking_elapsed()
        if _repl_mode and _stdout:
            # Clear plan block if present
            if _plan_written_lines > 0:
                _stdout.write(f"\033[{_plan_written_lines}A")
                for _ in range(_plan_written_lines + 1):
                    _stdout.write("\r\033[2K\n")
                _stdout.write("\033[1A")
                _plan_written_lines = 0
            if cancel_msg:
                _write_thinking_line(elapsed, cancel_msg=cancel_msg)
                _stdout.write("\n")
                _stdout.flush()
            else:
                _stdout.write("\r\033[2K")
                _stdout.flush()
    _thinking_start = 0
    _thinking_line_visible = False
    return elapsed


async def thinking_countdown(
    delay: float,
    cancel_event: "asyncio.Event",
    error_msg: str,
) -> bool:
    """Show a retry countdown on the thinking line after a system error.

    Ticks once per second displaying ``error_msg · retrying in Ns``.
    Returns ``True`` if countdown completed (caller should retry),
    ``False`` if ``cancel_event`` fired (caller should give up).
    """
    global _thinking_ticker_task
    # Stop the background ticker so it doesn't race with countdown writes (#245)
    if _thinking_ticker_task is not None:
        _thinking_ticker_task.cancel()
        try:
            await _thinking_ticker_task
        except (asyncio.CancelledError, Exception):
            pass
        _thinking_ticker_task = None
    remaining = int(delay)
    while remaining > 0:
        elapsed = time.monotonic() - _thinking_start if _thinking_start else 0.0
        if _footer_mode and _toolbar_invalidator:
            # In footer mode, push countdown state into the toolbar.
            # get_busy_status() will pick up the error via _thinking_phase.
            _toolbar_invalidator()
        elif _repl_mode and _stdout:
            _write_thinking_line(elapsed, error_msg=error_msg, countdown=remaining)
        try:
            await asyncio.wait_for(cancel_event.wait(), timeout=1.0)
            # cancel_event fired — give up
            if _footer_mode and _toolbar_invalidator:
                _toolbar_invalidator()
            elif _repl_mode and _stdout:
                _write_thinking_line(elapsed, cancel_msg="cancelled")
                _stdout.write("\n")
                _stdout.flush()
            return False
        except asyncio.TimeoutError:
            remaining -= 1
    return True


_retrying_info: dict[str, Any] = {}


def set_thinking_phase(phase: str, data: dict[str, Any] | None = None) -> None:
    """Update the current lifecycle phase displayed by the thinking ticker."""
    global _thinking_phase, _thinking_phase_data, _last_chunk_time, _phase_start_time
    changed = phase != _thinking_phase
    _thinking_phase = phase
    _thinking_phase_data = dict(data or {})
    _phase_start_time = time.monotonic()
    _last_chunk_time = time.monotonic()
    if changed:
        _invalidate_footer_toolbar()


def set_retrying(data: dict[str, Any]) -> None:
    """Update retry state displayed by the thinking ticker."""
    global _thinking_phase, _thinking_phase_data, _retrying_info
    _retrying_info = data
    _thinking_phase = "retrying"
    _thinking_phase_data = dict(data or {})
    _invalidate_footer_toolbar()


def increment_thinking_tokens() -> None:
    """Increment the streaming token counter and mark chunk arrival time.

    Calling this implicitly transitions to the 'streaming' phase.
    """
    global _thinking_tokens, _thinking_phase, _last_chunk_time, _phase_start_time
    _thinking_tokens += 1
    phase_changed = _thinking_phase != "streaming"
    # Set chunk time before phase to avoid a race with the background ticker:
    # if the ticker reads _thinking_phase=="streaming" before _last_chunk_time
    # is updated, it could briefly show "stalled" on a fresh phase transition.
    _last_chunk_time = time.monotonic()
    if phase_changed:
        _phase_start_time = _last_chunk_time
    _thinking_phase = "streaming"
    if phase_changed:
        _invalidate_footer_toolbar()


def increment_streaming_chars(n: int) -> None:
    """Accumulate character count during streaming for the health display."""
    global _streaming_chars
    _streaming_chars += n
    now = time.monotonic()
    _throughput_window.append((now, n))
    cutoff = now - _THROUGHPUT_WINDOW_SECS
    while _throughput_window and _throughput_window[0][0] < cutoff:
        _throughput_window.popleft()


def _format_count(value: Any) -> str:
    if isinstance(value, int):
        return f"{value:,}"
    return "?"


def _compaction_phase_detail(data: dict[str, Any] | None = None) -> str:
    """Return a compact human-readable reason for a compaction phase."""
    payload = data if data is not None else _thinking_phase_data
    reason = payload.get("reason")
    if reason == "context_error_recovery":
        return "context-error recovery"
    if reason == "compaction_prompt_too_long":
        return (
            "summary prompt too long; "
            f"attempt {_format_count(payload.get('attempt'))}/{_format_count(payload.get('max_attempts'))}, "
            f"dropped {_format_count(payload.get('dropped_messages'))} messages"
        )

    token_detail = (
        f"token threshold {_format_count(payload.get('estimated_tokens'))}/"
        f"{_format_count(payload.get('token_threshold'))}"
    )
    message_detail = (
        f"message threshold {_format_count(payload.get('message_count'))}/"
        f"{_format_count(payload.get('message_threshold'))}"
    )

    if reason == "token_threshold":
        return token_detail
    if reason == "message_count":
        return message_detail
    if reason == "token_and_message_threshold":
        return f"{token_detail} · {message_detail}"
    return ""


def _phase_label() -> str:
    """Return a phase-aware label for the thinking line (#1366, #1428).

    Maps the current ``_thinking_phase`` to a user-friendly label:
    - ``""`` / unknown → ``"Thinking..."``
    - ``accepted`` → ``"Working..."`` (initial ack between prompt submit and first phase)
    - ``connecting`` → ``"Connecting..."``
    - ``waiting`` → ``"Thinking..."``
    - ``streaming`` → ``"Writing..."``
    - ``retrying`` → ``"Thinking..."`` (retry suffix handles detail)
    - ``tool_exec`` → tool-context label via ``_tool_phase_label()``
    - ``compacting`` → compaction-context label via ``_compaction_phase_detail()``
    """
    phase = _thinking_phase
    if phase == "accepted":
        return "Working..."
    if phase == "connecting":
        return "Connecting..."
    if phase == "streaming":
        return "Writing..."
    if phase == "tool_exec":
        return _tool_phase_label()
    if phase == "compacting":
        detail = _compaction_phase_detail()
        return f"Compacting conversation history... {detail}" if detail else "Compacting conversation history..."
    # waiting, retrying, empty, unknown → default
    return "Thinking..."


def _tool_phase_label() -> str:
    """Build the tool execution phase label from active tool state (#1366).

    - 1 tool: use humanized summary (e.g. "Reading src/foo.py...")
    - N tools of same action: group label (e.g. "Reading 3 files...")
    - N tools of mixed actions: "Running N tools..."
    - 0 tools (shouldn't happen): "Running tools..."
    """
    if _active_tool_count == 0:
        return "Running tools..."
    if _active_tool_count == 1 and _active_tool_summaries:
        summary = _strip_terminal_control(_active_tool_summaries[0])
        if not summary.endswith("..."):
            summary += "..."
        return summary
    # Multiple tools: check if they share an action prefix
    if _active_tool_summaries:
        prefixes = set()
        for s in (_strip_terminal_control(summary) for summary in _active_tool_summaries):
            prefix = s.split(" ", 1)[0] if " " in s else s
            prefixes.add(prefix)
        if len(prefixes) == 1:
            prefix = next(iter(prefixes))
            noun = "files" if prefix in ("Reading", "Writing", "Editing") else "patterns"
            return f"{prefix} {_active_tool_count} {noun}..."
    return f"Running {_active_tool_count} tools..."


def enter_tool_phase(tool_name: str, arguments: dict[str, Any]) -> None:
    """Track a tool starting execution for phase display (#1366)."""
    global _active_tool_count
    _active_tool_count += 1
    _active_tool_names.append(tool_name)
    summary = _humanize_tool(tool_name, arguments)
    _active_tool_summaries.append(summary)
    _invalidate_footer_toolbar()


def exit_tool_phase(tool_name: str) -> None:
    """Track a tool completing execution (#1366, #1428)."""
    global _active_tool_count, _tool_ticker_summary
    if _active_tool_count > 0:
        _active_tool_count -= 1
    # Remove the first occurrence of this tool name
    if tool_name in _active_tool_names:
        idx = _active_tool_names.index(tool_name)
        _active_tool_names.pop(idx)
        if idx < len(_active_tool_summaries):
            _active_tool_summaries.pop(idx)
    # Clear tool_exec phase when all tools complete
    if _active_tool_count == 0:
        _active_tool_names.clear()
        _active_tool_summaries.clear()
        # #1428: fold the ticker-summary clear into the phase exit so stale
        # tool context doesn't linger across turns regardless of whether the
        # legacy ticker ran (footer mode no-ops it).
        _tool_ticker_summary = ""
    _invalidate_footer_toolbar()


def _reset_tool_phase() -> None:
    """Reset tool phase tracking state."""
    global _active_tool_count
    _active_tool_count = 0
    _active_tool_names.clear()
    _active_tool_summaries.clear()


def _phase_suffix(elapsed: float) -> str:
    """Build the dim phase text appended to the thinking line.

    Retry and stall conditions are always shown immediately.  Normal phase
    detail (connecting, waiting, streaming char count) is suppressed for the
    first 5 seconds to keep short waits calm (#1052).
    """
    if not _thinking_phase:
        return ""
    phase = _thinking_phase
    # Retry is always shown immediately regardless of elapsed time
    if phase == "retrying":
        attempt = _retrying_info.get("attempt", 2)
        max_attempts = _retrying_info.get("max_attempts", 3)
        return f"retry {attempt}/{max_attempts}"
    if phase == "streaming":
        now = time.monotonic()
        # Gap-based stall: always shown immediately
        if _last_chunk_time and now - _last_chunk_time > _MID_STREAM_STALL:
            stall_secs = now - _last_chunk_time
            return f"{_streaming_chars:,} chars · stalled {stall_secs:.0f}s"
        # Throughput-based stall (#774): always shown after warmup
        if _phase_start_time and now - _phase_start_time > _THROUGHPUT_WARMUP_SECS and _throughput_window:
            window_span = now - _throughput_window[0][0]
            if window_span > 0:
                window_chars = sum(n for _, n in _throughput_window)
                throughput = window_chars / window_span
                if throughput < _THROUGHPUT_STALL_THRESHOLD:
                    return f"{_streaming_chars:,} chars · slow ({throughput:.0f} chars/s)"
        # Normal streaming detail suppressed during calm window
        if elapsed < 5.0:
            return ""
        return f"{_streaming_chars:,} chars"
    # tool_exec: label already shows tool context via _phase_label(); no suffix needed
    if phase == "tool_exec":
        return ""
    if phase == "compacting":
        return ""
    # connecting: label already says "Connecting..." — no suffix needed (#1382)
    if phase == "connecting":
        return ""
    # waiting suppressed during calm window
    if elapsed < 5.0:
        return ""
    if phase == "waiting":
        return "waiting for first token"
    return phase


# ---------------------------------------------------------------------------
# Token / response rendering
# ---------------------------------------------------------------------------


def _make_markdown(text: str) -> Markdown:
    """Create a Markdown renderable with left-aligned headings."""
    _patch_heading_left()
    return Markdown(text)


_heading_patched = False


def _patch_heading_left() -> None:
    """Monkey-patch Rich's Heading to render left-aligned instead of centered."""
    global _heading_patched
    if _heading_patched:
        return
    from rich.markdown import Heading

    def _left_aligned(self: Any, console: Any, options: Any) -> Any:
        self.text.justify = "left"
        if self.tag == "h2":
            yield Text("")
        yield self.text

    Heading.__rich_console__ = _left_aligned  # type: ignore[method-assign]
    _heading_patched = True


def flush_buffered_text() -> None:
    """Flush buffered AI text at a tool boundary when live streaming is active.

    Called before tool calls start. With live streaming enabled, the AI's
    task explanation (e.g. 'Let me review your auth files') settles before
    tool output. With streaming disabled/unavailable, the text remains
    buffered for the end-of-turn static render.

    When live streaming is active (#1365), the Live region is torn down
    cleanly so the subsequent tool output renders underneath a settled
    static paragraph (no Live-vs-static overwrite flicker).
    """
    global _streaming_buffer, _tool_batch_active
    text = "".join(_streaming_buffer)

    # If the live-streaming renderer was driving the turn, let it emit its
    # own static finalize (which uses the hierarchy-aware
    # ``render_assistant_prose`` helper) and then return. We still honour
    # tool-batch spacing semantics.
    if _streaming_renderer is not None and _streaming_renderer.live_available():
        _streaming_buffer = []
        if not text.strip():
            # Buffer-only whitespace: still clear the live renderer state
            # so a fresh segment can start next.
            try:
                _streaming_renderer.flush_to_static()
            except Exception:
                pass
            return
        if _tool_batch_active:
            console.print()
            _tool_batch_active = False
        try:
            _streaming_renderer.flush_to_static()
        except Exception:
            # Hard fallback: treat as non-streaming.
            from rich.padding import Padding as _Padding

            _stdout_console.print(_Padding(_make_markdown(text), (0, 2, 0, 2)))
        return

    # When streaming is configured but unavailable (disabled by config,
    # non-TTY, NO_COLOR, or exec without opt-in), preserve the documented
    # fallback contract: keep prose buffered until render_response_end().
    if _streaming_renderer is not None:
        if not text.strip():
            _streaming_buffer = []
        return

    _streaming_buffer = []

    if not text.strip():
        return

    # Add spacing after tool call block before narration text.
    # This handles mid-turn narration; render_response_end() handles end-of-turn.
    if _tool_batch_active:
        console.print()
        _tool_batch_active = False

    from rich.padding import Padding

    _stdout_console.print(Padding(_make_markdown(text), (0, 2, 0, 2)))


def _flush_dedup() -> None:
    """Flush accumulated dedup counter if needed."""
    global _dedup_key, _dedup_count, _dedup_first_summary, _dedup_summary
    if _dedup_count > 1:
        label = _dedup_flush_label(_dedup_key, _dedup_count)
        console.print(f"    [{MUTED}]{label}[/{MUTED}]")
    _dedup_key = ""
    _dedup_count = 0
    _dedup_first_summary = ""
    _dedup_summary = ""


def render_token(content: str) -> None:
    """Buffer token content; when live streaming is configured and the
    console supports it, also feed the live-markdown renderer so the
    user sees formatting incrementally (#1365).

    The legacy buffer is kept populated in parallel so the end-of-turn
    fallback (``render_response_end`` called in contexts where Live is
    unavailable) still works unchanged.
    """
    _streaming_buffer.append(content)
    if _streaming_renderer is not None and _streaming_renderer.live_available():
        try:
            _streaming_renderer.feed(content)
        except Exception:
            # Never let a rendering hiccup crash the REPL loop.
            pass


def render_response_end() -> None:
    """Render the complete buffered response with Rich Markdown.

    When live streaming is active (#1365) the Live region is stopped
    here; its ``stop()`` finalizes the assistant prose via
    ``render_assistant_prose`` (our injected ``finalize_render``
    callback), matching the hierarchy-container output of the legacy
    path exactly.
    """
    global _streaming_buffer, _tool_batch_active
    _flush_dedup()
    _flush_repeat_collapse()

    full_text = "".join(_streaming_buffer)
    _streaming_buffer = []

    if _streaming_renderer is not None and _streaming_renderer.live_available():
        # Streaming path: live region owns the final render.
        if _tool_batch_active:
            console.print()
            _tool_batch_active = False
        try:
            _streaming_renderer.stop()
        except Exception:
            # Hard fallback: static render below.
            if full_text.strip():
                render_assistant_prose(full_text)
        return

    if not full_text.strip():
        _tool_batch_active = False
        return

    # Add spacing after tool call block before AI response
    if _tool_batch_active:
        console.print()
        _tool_batch_active = False

    # Route through the assistant-prose hierarchy helper so the REPL and
    # workflow replay share the same padding/gutter behaviour (#1370).
    render_assistant_prose(full_text)


def render_newline() -> None:
    console.print()


# ---------------------------------------------------------------------------
# Per-turn completion summary (#1428)
# ---------------------------------------------------------------------------


def _humanize_tool_verb(tool_name: str) -> str:
    """Return a short, past-tense verb for a tool name used in the turn summary.

    Maps common tool names to compact verbs suitable for a single-line recap.
    Unknown tools fall back to the tool name itself.
    """
    verb_map = {
        "read_file": "read",
        "file_read": "read",
        "write_file": "write",
        "file_write": "write",
        "edit_file": "edit",
        "file_edit": "edit",
        "bash": "bash",
        "glob_files": "glob",
        "grep": "grep",
        "run_agent": "subagent",
        "create_canvas": "canvas",
        "update_canvas": "canvas",
        "patch_canvas": "canvas",
        "ask_user": "ask",
        "introspect": "introspect",
    }
    return verb_map.get(tool_name, tool_name)


def _humanize_tool_verb_past(tool_name: str) -> str:
    """Return a capitalised past-tense verb for tool-call completion lines (#1364).

    Parallel to ``_humanize_tool_verb`` (which feeds the per-turn summary
    in its own short-verb form); this table produces the verb-first phrasing
    for the completion line (``Read src/foo.py``, ``Ran pytest -q``).

    Unknown tools fall back to ``"Called"`` so MCP/custom tools still read
    as an execution log entry (``Called mcp.some_tool``).
    """
    verb_map = {
        "read_file": "Read",
        "file_read": "Read",
        "write_file": "Wrote",
        "file_write": "Wrote",
        "edit_file": "Edited",
        "file_edit": "Edited",
        "bash": "Ran",
        "grep": "Searched",
        "search": "Searched",
        "ripgrep": "Searched",
        "glob_files": "Globbed",
        "glob": "Globbed",
        "find_files": "Globbed",
        "list_directory": "Listed",
        "run_agent": "Delegated",
        "create_canvas": "Created canvas",
        "update_canvas": "Updated canvas",
        "patch_canvas": "Patched canvas",
        "ask_user": "Asked",
        "ask_human": "Asked",
        "introspect": "Introspected",
    }
    return verb_map.get(tool_name, "Called")


def render_turn_summary(
    *,
    elapsed: float,
    tools: list[dict[str, Any]] | None = None,
    cancelled: bool = False,
    error: str | None = None,
) -> None:
    """Render the single-line per-turn completion summary (#1428).

    Composes one of:
    - ``✓ done · 3.2s · 1 tool`` (success, one tool)
    - ``✓ done · 7.0s · 3 tools`` (success, multiple tools)
    - ``✓ done · 2.5s`` (success, no tools)
    - ``cancelled · 1.1s`` (user cancelled)
    - ``failed: {error} · 2.0s`` (error; takes priority over cancelled)

    In ``Verbosity.DETAILED`` mode, appends up to 3 distinct tool verbs after
    the tool count to give a quick recap of what happened.

    Theme-aware: uses ``_theme.success``/``.muted``/``.error`` so it honours
    the active CLI theme.

    Non-blocking: writes one line and returns. Must render *after*
    ``stop_thinking_sync()``'s cancel ack and *before* ``render_response_end()``
    so the assistant's final markdown body appears under the summary.
    """
    tools = tools or []
    muted = _theme.muted
    success = _theme.success
    err = _theme.error or "red"
    sep = "·"

    # Error branch (wins over cancelled — more actionable).
    if error:
        text = Text()
        text.append("failed: ", style=err)
        text.append(error, style=err)
        text.append(f"  {sep}  ", style=muted)
        text.append(f"{elapsed:.1f}s", style=muted)
        console.print(text)
        return

    # Cancelled branch.
    if cancelled:
        text = Text()
        text.append("cancelled", style=muted)
        text.append(f"  {sep}  ", style=muted)
        text.append(f"{elapsed:.1f}s", style=muted)
        console.print(text)
        return

    # Success branch.
    text = Text()
    text.append("\u2713 done", style=success)
    text.append(f"  {sep}  ", style=muted)
    text.append(f"{elapsed:.1f}s", style=muted)
    if tools:
        text.append(f"  {sep}  ", style=muted)
        n = len(tools)
        word = "tool" if n == 1 else "tools"
        text.append(f"{n} {word}", style=muted)
        # DETAILED: top 3 distinct verbs
        if _verbosity == Verbosity.DETAILED:
            seen: list[str] = []
            for entry in tools:
                verb = _humanize_tool_verb(entry.get("tool_name", ""))
                if verb and verb not in seen:
                    seen.append(verb)
                if len(seen) >= 3:
                    break
            if seen:
                text.append(f"  {sep}  ", style=muted)
                text.append(" ".join(seen), style=muted)
    console.print(text)


def render_debug_summary(summary: dict[str, Any]) -> None:
    """Render an opt-in per-turn debug diagnostics summary."""
    if not summary:
        return
    muted = _theme.muted
    accent = _theme.accent or _theme.secondary
    sep = "·"

    duration = summary.get("total_duration_seconds")
    duration_text = f"{duration:.1f}s" if isinstance(duration, int | float) else "?s"
    stop_reason = str(summary.get("stop_reason") or "unknown")
    final_phase = str(summary.get("final_phase") or "unknown")
    turn_id = str(summary.get("turn_id") or summary.get("request_id") or "")

    header = Text()
    header.append("debug", style=accent)
    if turn_id:
        header.append(f"  {sep}  ", style=muted)
        header.append(turn_id, style=muted)
    header.append(f"  {sep}  ", style=muted)
    header.append(duration_text, style=muted)
    header.append(f"  {sep}  ", style=muted)
    header.append(stop_reason, style=muted)
    header.append(f"  {sep}  ", style=muted)
    header.append(final_phase, style=muted)
    console.print(header)

    usage_raw = summary.get("usage")
    counters_raw = summary.get("counters")
    model_raw = summary.get("model")
    usage: dict[str, Any] = usage_raw if isinstance(usage_raw, dict) else {}
    counters: dict[str, Any] = counters_raw if isinstance(counters_raw, dict) else {}
    model: dict[str, Any] = model_raw if isinstance(model_raw, dict) else {}
    details: list[str] = []
    model_label = " / ".join(str(x) for x in (model.get("provider"), model.get("name")) if x)
    if model_label:
        details.append(f"model {model_label}")
    if summary.get("interface"):
        details.append(f"interface {summary.get('interface')}")
    if usage.get("total_tokens") is not None:
        details.append(f"tokens {usage.get('total_tokens')}")
    details.append(f"stream {counters.get('tokens', 0)} chunks/{counters.get('token_chars', 0)} chars")
    retries_raw = summary.get("retries")
    retries: list[Any] = retries_raw if isinstance(retries_raw, list) else []
    if retries:
        details.append(f"retries {len(retries)}")
    if details:
        line = Text("  " + "  ".join(details), style=muted)
        console.print(line)

    tools_raw = summary.get("tools")
    tools: list[Any] = tools_raw if isinstance(tools_raw, list) else []
    if tools:
        tool_bits: list[str] = []
        for tool in tools[:5]:
            if not isinstance(tool, dict):
                continue
            name = str(tool.get("name") or "tool")
            status = str(tool.get("status") or "unknown")
            elapsed = tool.get("duration_seconds")
            elapsed_text = f" {elapsed:.2f}s" if isinstance(elapsed, int | float) else ""
            tool_bits.append(f"{name}:{status}{elapsed_text}")
        if tool_bits:
            console.print(Text("  tools " + ", ".join(tool_bits), style=muted))

    active_tools_raw = summary.get("active_tools")
    active_tools: list[Any] = active_tools_raw if isinstance(active_tools_raw, list) else []
    if active_tools:
        active_bits: list[str] = []
        for tool in active_tools[:4]:
            if not isinstance(tool, dict):
                continue
            name = str(tool.get("name") or "tool")
            elapsed = tool.get("duration_seconds")
            timeout = tool.get("timeout_seconds")
            elapsed_text = f" {elapsed:.1f}s" if isinstance(elapsed, int | float) else ""
            timeout_text = f"/{timeout:.0f}s" if isinstance(timeout, int | float) else ""
            active_bits.append(f"{name}:running{elapsed_text}{timeout_text}")
        if active_bits:
            console.print(Text("  active " + ", ".join(active_bits), style=muted))

    phases_raw = summary.get("phases")
    phases: list[Any] = phases_raw if isinstance(phases_raw, list) else []
    compactions = [p for p in phases if isinstance(p, dict) and p.get("phase") == "compacting"]
    events_raw = summary.get("runtime_events")
    events: list[Any] = events_raw if isinstance(events_raw, list) else []
    compactions.extend(e for e in events if isinstance(e, dict) and e.get("kind") == "compaction")
    if compactions:
        comp = compactions[-1]
        bits = [
            str(comp.get("reason") or comp.get("strategy") or "compaction"),
        ]
        if comp.get("estimated_tokens") is not None:
            bits.append(f"~{comp.get('estimated_tokens')} tokens")
        if comp.get("message_count") is not None:
            bits.append(f"{comp.get('message_count')} msgs")
        if comp.get("message_threshold") is not None:
            bits.append(f"threshold {comp.get('message_threshold')}")
        if comp.get("messages_compacted") is not None:
            bits.append(f"compacted {comp.get('messages_compacted')}")
        if comp.get("tail_preserved") is not None:
            bits.append(f"tail {comp.get('tail_preserved')}")
        if comp.get("bytes_saved") is not None:
            bits.append(f"saved {comp.get('bytes_saved')} bytes")
        console.print(Text("  compaction " + ", ".join(bits), style=muted))

    event_names = [str(e.get("kind")) for e in events[:6] if isinstance(e, dict) and e.get("kind")]
    if event_names:
        console.print(Text("  events " + ", ".join(event_names), style=muted))

    errors_raw = summary.get("errors")
    errors: list[Any] = errors_raw if isinstance(errors_raw, list) else []
    if errors:
        err = errors[-1]
        if isinstance(err, dict):
            code = str(err.get("code") or "error")
            timeout_type = err.get("timeout_type")
            elapsed = err.get("elapsed_seconds")
            bits = [code]
            if timeout_type:
                bits.append(str(timeout_type))
            if isinstance(elapsed, int | float):
                bits.append(f"{elapsed:.1f}s")
            console.print(Text("  error " + ", ".join(bits), style=muted))


# ---------------------------------------------------------------------------
# Inline diff rendering (Claude Code-style)
# ---------------------------------------------------------------------------

_DIFF_CONTEXT_LINES = 3  # lines of context around each change


def _diff_remove_bg() -> str:
    return f"on {_theme.diff_remove_bg}" if _theme.diff_remove_bg else ""


def _diff_add_bg() -> str:
    return f"on {_theme.diff_add_bg}" if _theme.diff_add_bg else ""


def _diff_line_no() -> str:
    return _theme.chrome


def _render_inline_diff(tool_name: str, output: dict[str, Any]) -> None:
    """Render Claude Code-style color-coded inline diff for file changes.

    Requires ``_old_content`` and/or ``_new_content`` keys in the output dict.
    """
    import difflib

    old_content: str | None = output.get("_old_content")
    new_content: str | None = output.get("_new_content")
    file_path = output.get("path", "")
    short = _short_path(file_path) if file_path else tool_name

    # Determine action label
    action = output.get("action", "")
    if action == "created":
        lines = output.get("lines", 0)
        header_text = Text()
        header_text.append("  ● ", style=_theme.success)
        header_text.append(f"Write({short})", style="bold")
        console.print(header_text)
        summary_text = Text()
        summary_text.append(f"  └ Created, {lines} lines", style=_theme.muted)
        console.print(summary_text)
        return

    if old_content is None or new_content is None:
        return

    # Compute diff
    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    # Ensure trailing newline for clean diffing
    if old_lines and not old_lines[-1].endswith("\n"):
        old_lines[-1] += "\n"
    if new_lines and not new_lines[-1].endswith("\n"):
        new_lines[-1] += "\n"

    diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=""))
    if len(diff) < 3:
        return  # no changes

    # Count added/removed
    added = sum(1 for line in diff[2:] if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff[2:] if line.startswith("-") and not line.startswith("---"))

    # Header
    label = "Update" if tool_name.lower() in ("edit_file", "file_edit") else "Write"
    header_text = Text()
    header_text.append("  ● ", style=_theme.success)
    header_text.append(f"{label}({short})", style="bold")
    console.print(header_text)

    summary_text = Text()
    summary_text.append("  └ ", style=_theme.muted)
    summary_text.append(f"Added {added} lines", style=_theme.success) if added else None
    if added and removed:
        summary_text.append(", ", style=_theme.muted)
    summary_text.append(f"removed {removed} lines", style=_theme.error) if removed else None
    if not added and not removed:
        summary_text.append("no line changes", style=_theme.muted)
    console.print(summary_text)

    # Parse hunks from unified diff and render with context collapsing
    _render_diff_hunks(diff, old_lines, new_lines)


def _render_diff_hunks(diff: list[str], old_lines: list[str], new_lines: list[str]) -> None:
    """Parse unified diff output and render color-coded hunks with line numbers."""
    import re

    hunk_header_re = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")
    hunks: list[tuple[int, int, list[tuple[str, str]]]] = []  # (old_start, new_start, lines)

    current_hunk: list[tuple[str, str]] = []
    old_start = new_start = 0

    for line in diff[2:]:  # skip --- and +++ headers
        m = hunk_header_re.match(line)
        if m:
            if current_hunk:
                hunks.append((old_start, new_start, current_hunk))
            old_start = int(m.group(1))
            new_start = int(m.group(2))
            current_hunk = []
        elif line.startswith("+"):
            current_hunk.append(("+", line[1:]))
        elif line.startswith("-"):
            current_hunk.append(("-", line[1:]))
        elif line.startswith(" "):
            current_hunk.append((" ", line[1:]))
    if current_hunk:
        hunks.append((old_start, new_start, current_hunk))

    for i, (old_start, new_start, hunk_lines) in enumerate(hunks):
        if i > 0:
            console.print(f"    [{MUTED}]...[/{MUTED}]")

        # Density-aware context collapsing (#1367). NORMAL/DETAILED fall through
        # to full hunk rendering, preserving byte-identical pre-#1367 output.
        # ``/expand`` sets ``_force_full_diff`` to force the pass-through path
        # regardless of the active density.
        display_hunk: list[tuple[str, str]]
        if _force_full_diff:
            display_hunk = hunk_lines
        elif _density in (ToolResultDensity.COMPACT, ToolResultDensity.MINIMAL):
            display_hunk = list(
                collapse_diff_hunks(
                    hunk_lines,
                    context_lines=_density_diff_context_lines,
                    density=_density,
                )
            )
        else:
            display_hunk = hunk_lines

        old_num = old_start
        new_num = new_start
        for tag, content in display_hunk:
            # Truncate long lines for display
            display = content.rstrip("\n")
            if len(display) > 120:
                display = display[:117] + "..."

            if tag == "-":
                line_text = Text()
                line_text.append(f"    {old_num:>4} ", style=_diff_line_no())
                line_text.append(f" {display} ", style=_diff_remove_bg())
                console.print(line_text)
                old_num += 1
            elif tag == "+":
                line_text = Text()
                line_text.append(f"    {new_num:>4} ", style=_diff_line_no())
                line_text.append(f" {display} ", style=_diff_add_bg())
                console.print(line_text)
                new_num += 1
            elif tag == "~":
                # Collapsed-context marker (compact mode).
                console.print(f"    [{MUTED}]  {escape(display)}[/{MUTED}]")
            else:
                line_text = Text()
                line_text.append(f"    {new_num:>4} ", style=_diff_line_no())
                line_text.append(f" {display}", style=MUTED)
                console.print(line_text)
                old_num += 1
                new_num += 1


def _has_diff_data(tool_name: str, output: Any) -> bool:
    """Check if tool output contains diff rendering data."""
    if not isinstance(output, dict):
        return False
    name = tool_name.lower()
    if name not in ("write_file", "file_write", "edit_file", "file_edit"):
        return False
    return "_new_content" in output or "_old_content" in output


# ---------------------------------------------------------------------------
# Tool elapsed timer (mirrors _thinking_ticker for tool execution)
# ---------------------------------------------------------------------------


async def _tool_ticker() -> None:
    """Background task that updates tool elapsed time every 0.5s."""
    global _tool_line_visible
    try:
        while True:
            await asyncio.sleep(0.5)
            if _tool_start:
                elapsed = time.monotonic() - _tool_start
                if _tool_spinner:
                    label = f"  [{MUTED}]{escape(_tool_ticker_summary)}  {elapsed:.0f}s[/{MUTED}]"
                    _tool_spinner.update(label)
                elif _invalidate_tool_status_toolbar():
                    pass
                elif _repl_mode and _stdout:
                    muted = _theme.ansi_fg("muted")
                    rst = _theme.ansi_reset
                    summary = _strip_terminal_control(_tool_ticker_summary)
                    _stdout.write(f"\r\033[2K{muted}  {summary}  {elapsed:.0f}s{rst}")
                    _stdout.flush()
                    _tool_line_visible = True
    except asyncio.CancelledError:
        return


def _tool_status_uses_toolbar() -> bool:
    """Return True when tool-only status should render via prompt_toolkit.

    Tool calls often start after ``stop_thinking()`` has cleared ``_footer_mode``.
    By then the input collector may already have mounted the next
    ``PromptSession.prompt_async()`` for queued input.  Falling back to raw
    carriage-return writes in that state can visually overwrite the prompt.

    Keep the raw fallback for #1512's inactive-toolbar case, but prefer the
    prompt_toolkit invalidation surface whenever the REPL prompt is live.
    """
    if not _repl_mode or _toolbar_invalidator is None:
        return False
    if _footer_mode:
        return True
    if _prompt_is_active is not None and _prompt_is_active():
        return True
    return bool(_toolbar_is_active is not None and _toolbar_is_active())


def _invalidate_tool_status_toolbar() -> bool:
    """Invalidate the prompt_toolkit status surface when available."""
    if not _tool_status_uses_toolbar():
        return False
    invalidator = _toolbar_invalidator
    if invalidator is None:
        return False
    _clear_tool_line()
    invalidator()
    return True


def _clear_tool_line() -> None:
    """Clear a raw tool ticker line if one is currently visible."""
    global _tool_line_visible
    if not _tool_line_visible:
        return
    if _repl_mode and _stdout:
        _stdout.write("\r\033[2K")
        _stdout.flush()
    _tool_line_visible = False


def start_tool_ticker(summary: str) -> None:
    """Start a live elapsed timer for the current tool call.

    #1428: When the unified thinking ticker owns footer mode, this becomes a
    no-op — the thinking ticker already routes through ``_phase_label()`` →
    ``_tool_phase_label()`` when ``_thinking_phase == "tool_exec"``. Starting a
    parallel tool ticker would produce two competing status surfaces (the very
    thing #1428 exists to fix).

    In non-footer paths (REPL without a bottom toolbar invalidator, or
    non-REPL Rich Status spinner mode) the legacy ticker is still used so
    those environments still get a live elapsed time.
    """
    global _tool_ticker_task, _tool_ticker_summary, _tool_spinner
    # Unified surface: in footer mode the thinking ticker already owns the
    # busy indicator. Skip starting a parallel ticker task; leave
    # _tool_ticker_summary empty so get_busy_status() returns a single slot.
    if _footer_mode:
        _tool_ticker_summary = ""
        if _tool_ticker_task is not None:
            _tool_ticker_task.cancel()
            _tool_ticker_task = None
        return
    # When multiple tools are active in parallel, show a grouped summary (#1366)
    if _active_tool_count > 1:
        _tool_ticker_summary = _tool_phase_label()
    else:
        _tool_ticker_summary = _strip_terminal_control(summary)
    if _tool_ticker_task is not None:
        _tool_ticker_task.cancel()
        _tool_ticker_task = None
    if not _repl_mode:
        _tool_spinner = Status(
            f"  [{MUTED}]{escape(_tool_ticker_summary)}[/{MUTED}]",
            console=console,
            spinner="dots12",
        )
        _tool_spinner.start()
    elif _invalidate_tool_status_toolbar():
        pass
    try:
        loop = asyncio.get_running_loop()
        _tool_ticker_task = loop.create_task(_tool_ticker())
    except RuntimeError:
        _tool_ticker_task = None


def stop_tool_ticker_sync() -> None:
    """Stop the tool ticker synchronously (safe from sync render_tool_call_end)."""
    global _tool_ticker_task, _tool_spinner, _tool_ticker_summary
    uses_toolbar = _tool_status_uses_toolbar()
    if _tool_ticker_task is not None:
        _tool_ticker_task.cancel()
        _tool_ticker_task = None
    if _tool_spinner:
        _tool_spinner.stop()
        _tool_spinner = None
    else:
        _clear_tool_line()
    # Always clear summary so get_busy_status() doesn't return a stale tool label.
    _tool_ticker_summary = ""
    if uses_toolbar and _toolbar_invalidator:
        _toolbar_invalidator()


# ---------------------------------------------------------------------------
# Tool call rendering (verbosity-aware)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Compact tool-call completion (#1364)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _LiveToolsState:
    """In-renderer snapshot of the ``cli.live_tools`` config.

    Mirrors ``CliLiveToolsConfig`` so the renderer does not import
    ``anteroom.config`` at module level (keeps the renderer importable
    from trimmed-down contexts like exec mode).
    """

    show_args_in_verbose: bool = True
    show_metric_suffix: bool = True
    metric_max_chars: int = 40


_live_tools_state: _LiveToolsState = _LiveToolsState()


def configure_live_tools(
    *,
    show_args_in_verbose: bool = True,
    show_metric_suffix: bool = True,
    metric_max_chars: int = 40,
) -> None:
    """Install live tool-call lifecycle renderer settings (#1364).

    Called from ``cli/repl.py`` at startup with values sourced from
    ``config.cli.live_tools``. Safe to call repeatedly; each call fully
    replaces the previous state.
    """
    global _live_tools_state
    # Clamp defensively — config.py already clamps, but the renderer must
    # not rely on that when called directly from tests or embedders.
    clamped = max(1, min(int(metric_max_chars), 200))
    _live_tools_state = _LiveToolsState(
        show_args_in_verbose=bool(show_args_in_verbose),
        show_metric_suffix=bool(show_metric_suffix),
        metric_max_chars=clamped,
    )


def get_live_tools_config() -> _LiveToolsState:
    """Return the current live tools renderer state (test helper)."""
    return _live_tools_state


def _completion_metric(tool_name: str, output: Any) -> str:
    """Extract a short metric suffix for a tool-call completion line.

    Reads structured keys from the tool's output dict (``content``,
    ``stdout``, ``bytes_written``, ``exit_code``, ``matches``, ``files``)
    and returns a clamped-length string such as ``"42 lines"`` or
    ``"exit 0"``. Returns ``""`` when nothing meaningful can be extracted
    (including when the ``show_metric_suffix`` flag is off).
    """
    if not _live_tools_state.show_metric_suffix:
        return ""
    if not isinstance(output, dict):
        return ""

    name = tool_name.lower()
    metric = ""

    if name in ("read_file", "file_read", "edit_file", "file_edit"):
        content = output.get("content")
        if isinstance(content, str) and content:
            lines = content.count("\n") + (0 if content.endswith("\n") else 1)
            if lines <= 0:
                lines = 1
            metric = f"{lines} line" if lines == 1 else f"{lines} lines"
    elif name in ("write_file", "file_write"):
        bw = output.get("bytes_written")
        if isinstance(bw, int) and bw >= 0:
            if bw >= 1_048_576:
                metric = f"{bw / 1_048_576:.1f} MB"
            elif bw >= 1024:
                metric = f"{bw / 1024:.1f} KB"
            else:
                metric = f"{bw} B"
        else:
            content = output.get("content")
            if isinstance(content, str) and content:
                lines = content.count("\n") + (0 if content.endswith("\n") else 1)
                if lines <= 0:
                    lines = 1
                metric = f"{lines} line" if lines == 1 else f"{lines} lines"
    elif name == "bash":
        exit_code = output.get("exit_code")
        if isinstance(exit_code, int):
            metric = f"exit {exit_code}"
        else:
            stdout = output.get("stdout")
            if isinstance(stdout, str) and stdout:
                lines = stdout.count("\n") + (0 if stdout.endswith("\n") else 1)
                if lines <= 0:
                    lines = 1
                metric = f"{lines} lines stdout" if lines != 1 else "1 line stdout"
    elif name in ("grep", "search", "ripgrep"):
        matches = output.get("matches")
        if isinstance(matches, int):
            metric = f"{matches} matches"
        else:
            content = output.get("content")
            if isinstance(content, str) and content:
                metric = f"{content.count(chr(10)) + 1} matches"
    elif name in ("glob_files", "glob", "find_files"):
        files = output.get("files")
        if isinstance(files, list):
            # glob_files now includes directories in its `files` list, so report a neutral count.
            metric = f"{len(files)} paths"

    # Generic fallback: if nothing matched but stdout/bytes are present,
    # surface something compact. This keeps MCP/unknown tools quiet when
    # they don't expose a recognised shape.
    if not metric:
        return ""

    # Clamp
    max_chars = _live_tools_state.metric_max_chars
    if len(metric) > max_chars:
        metric = metric[: max(1, max_chars - 1)] + "\u2026"  # ellipsis
        metric = metric[:max_chars]
    return metric


def render_tool_call_completion(
    tool_name: str,
    status: str,
    elapsed: float,
    arguments: dict[str, Any],
    output: Any,
) -> None:
    """Render a single compact completion line for a tool call (#1364).

    Layout (compact/detailed):

        │ ✓ Read src/foo.py  ·  5 lines  0.5s

    Layout (failure):

        │ ✗ Ran ls /nope  1.2s
            No such file or directory

    Layout (verbose + show_args_in_verbose): the completion line plus a
    dim ``args: {...}`` footline underneath.

    The gutter glyph is drawn from ``_TOOL_GUTTER_CHAR`` and styled with
    ``_theme.tool_gutter``. Past-tense verb is sourced from
    ``_humanize_tool_verb_past`` and the target phrase from the existing
    ``_humanize_tool`` helper (stripped of its present-tense action prefix
    when recognised).
    """
    muted = _theme.muted or ""
    success = _theme.success or ""
    err = _theme.error or "red"
    gutter_color = _theme.tool_gutter or muted

    # Verb + target
    verb = _humanize_tool_verb_past(tool_name)
    summary = _humanize_tool(tool_name, arguments)
    # Strip the present-tense prefix (Reading/Writing/Editing/Searching/…) so
    # "Read src/foo.py" reads cleanly rather than "Read Reading src/foo.py".
    target = summary
    for prefix in ("Reading ", "Writing ", "Editing ", "Searching for ", "Finding ", "Listing ", "Sub-agent: "):
        if target.startswith(prefix):
            target = target[len(prefix) :]
            break
    if target.startswith("bash "):
        target = target[len("bash ") :]

    icon = "\u2713" if status == "success" else "\u2717"
    icon_style = success if status == "success" else err

    line = Text()
    if gutter_color:
        line.append(f"{_TOOL_GUTTER_CHAR} ", style=gutter_color)
    else:
        line.append(f"{_TOOL_GUTTER_CHAR} ")
    line.append(icon, style=icon_style)
    line.append(" ")
    line.append(f"{verb} {target}".rstrip(), style="bold" if muted == "" else muted)

    # Metric suffix (muted) — only on success
    if status == "success":
        metric = _completion_metric(tool_name, output)
        if metric:
            if muted:
                line.append("  \u00b7  ", style=muted)
                line.append(metric, style=muted)
            else:
                line.append(f"  \u00b7  {metric}")

    # Elapsed (muted) — suppressed for very short runs (<100 ms)
    if elapsed >= 0.1:
        if muted:
            line.append("  ", style=muted)
            line.append(f"{elapsed:.1f}s", style=muted)
        else:
            line.append(f"  {elapsed:.1f}s")

    console.print(line)

    # Failure error summary (one line, muted error color)
    if status != "success":
        summary_err = _error_summary(output)
        if summary_err:
            if err:
                console.print(f"    [{err}]{escape(summary_err)}[/{err}]")
            else:
                console.print(f"    {escape(summary_err)}")

    # Verbose args footline (opt-in) — only in VERBOSE mode.
    if _verbosity == Verbosity.VERBOSE and _live_tools_state.show_args_in_verbose and arguments:
        try:
            args_str = json.dumps(arguments, indent=None, default=str)
        except (TypeError, ValueError):
            args_str = str(arguments)
        if len(args_str) > 200:
            args_str = args_str[:200] + "..."
        chrome = _theme.chrome or muted
        if chrome:
            console.print(f"    [{chrome}]args: {escape(args_str)}[/{chrome}]")
        else:
            console.print(f"    args: {escape(args_str)}")


def render_tool_call_start(tool_name: str, arguments: dict[str, Any]) -> None:
    """Begin a tool-call lifecycle (#1364).

    Under the compact lifecycle, the running phase lives entirely in the
    unified thinking/footer ticker (fed via ``enter_tool_phase`` in the
    caller). This helper:

    1. Flushes any buffered AI prose so narration renders before tool output.
    2. Records per-tool start time for accurate parallel elapsed.
    3. Spaces before the first tool in a batch.
    4. Kicks off the live elapsed ticker (no-op in footer mode).

    It does NOT print a ``> tool(args)`` breadcrumb in VERBOSE any longer —
    the completion line now carries the args footline instead, eliminating
    the dual-surface duplication.
    """
    global _tool_start, _tool_batch_active

    # Flush any buffered AI text so task explanations appear before tool output
    flush_buffered_text()

    summary = _humanize_tool(tool_name, arguments)

    _tool_start = time.monotonic()

    # Store for history — include start time per-tool so parallel tool
    # calls get correct elapsed times (the global _tool_start gets
    # overwritten by each subsequent start).
    _current_turn_tools.append(
        {
            "tool_name": tool_name,
            "arguments": arguments,
            "summary": summary,
            "status": "running",
            "output": None,
            "start_time": _tool_start,
        }
    )

    detached = _detach_thinking_line_for_output()

    # Add spacing before the first tool call in a batch
    if not _tool_batch_active:
        if not detached:
            console.print()
        _tool_batch_active = True

    # Start live elapsed timer — skip for interactive tools that use the terminal.
    # Stop any existing ticker first so it doesn't keep printing during input.
    if tool_name in ("ask_user", "ask_human"):
        stop_tool_ticker_sync()
    else:
        start_tool_ticker(summary)


def render_tool_call_end(tool_name: str, status: str, output: Any) -> None:
    """Render the tool-call completion phase (#1364).

    Delegates the actual single-line layout to
    ``render_tool_call_completion``; this function handles state-plumbing
    concerns — stopping the elapsed ticker, matching the right
    ``_current_turn_tools`` entry (important for parallel tools), updating
    history, running the dedup accumulator, and routing through the inline
    diff path for file-modifying tools.

    Verbosity behaviour:
    - All three modes (compact/detailed/verbose) share the same completion
      line produced by ``render_tool_call_completion``. VERBOSE adds an
      args footline inside the helper when ``cli.live_tools.show_args_in_verbose``
      is on.
    """
    stop_tool_ticker_sync()
    _detach_thinking_line_for_output()

    # Update history — find the first *running* entry that matches tool_name.
    # Using [-1] would grab the wrong entry when parallel tools complete
    # out of order (asyncio.as_completed returns fastest-first).
    matched_entry = None
    for entry in _current_turn_tools:
        if entry["tool_name"] == tool_name and entry["status"] == "running":
            matched_entry = entry
            break
    if matched_entry is None and _current_turn_tools:
        # Fallback: no running match (e.g. duplicate tool names all completed)
        matched_entry = _current_turn_tools[-1]

    # Use per-tool start time for accurate parallel elapsed calculation
    start = matched_entry.get("start_time", _tool_start) if matched_entry else _tool_start
    elapsed = time.monotonic() - start if start else 0.0

    arguments = matched_entry.get("arguments", {}) if matched_entry else {}

    if matched_entry:
        matched_entry["status"] = status
        matched_entry["output"] = output
        matched_entry["elapsed"] = elapsed

    summary = matched_entry["summary"] if matched_entry else tool_name

    # Dedup: collapse consecutive similar tool calls (success only).
    global _dedup_key, _dedup_count, _dedup_first_summary, _dedup_summary
    global _repeat_shape_hash, _repeat_count, _repeat_summary

    # Collapse-repeats (#1367): in compact/minimal modes with the knob on,
    # identical successive successful tool outputs are suppressed and summed
    # into a ``× N`` line. NORMAL/DETAILED modes are always pass-through so
    # the byte-identical-default contract is preserved.
    if (
        status == "success"
        and _density_collapse_repeats
        and _density in (ToolResultDensity.COMPACT, ToolResultDensity.MINIMAL)
    ):
        shape = _repeat_shape_key(tool_name, output)
        if shape and shape == _repeat_shape_hash and _repeat_count >= 1:
            _repeat_count += 1
            return
        # Different shape (or first): flush any pending repeat group, then
        # stash this one as the new head. Fall through to the normal render.
        _flush_repeat_collapse()
        _repeat_shape_hash = shape
        _repeat_count = 1
        _repeat_summary = summary
    else:
        # Any non-eligible tool event flushes a pending repeat group so the
        # ``× N`` line lands before new output.
        if _repeat_count >= 1:
            _flush_repeat_collapse()

    # Dedup: collapse consecutive similar tool calls (compact/detailed only)
    key = _dedup_key_from_summary(summary) if _tool_dedup_enabled else ""
    if _tool_dedup_enabled and status == "success" and key == _dedup_key and _dedup_count >= 1:
        _dedup_count += 1
        return

    # Different tool type or first occurrence — flush previous dedup, print new line
    _flush_dedup()

    # Inline diff for file-modifying tools (all verbosity levels). Diff path
    # prints its own header and body — the completion helper is skipped so
    # we don't double-print.
    if status == "success" and _has_diff_data(tool_name, output):
        _render_inline_diff(tool_name, output)
        _dedup_key = ""
        _dedup_count = 0
        _dedup_summary = ""
        return

    # ask_user / ask_human in COMPACT mode: the interactive prompt was the
    # user-visible surface; suppress a completion line entirely.
    if status == "success" and _verbosity == Verbosity.COMPACT and tool_name in ("ask_user", "ask_human"):
        _dedup_key = ""
        _dedup_count = 0
        _dedup_summary = ""
        return

    # Unified completion line — single source of truth for the tool-call
    # output shape across all verbosity modes.
    render_tool_call_completion(
        tool_name,
        status,
        elapsed=elapsed,
        arguments=arguments if isinstance(arguments, dict) else {},
        output=output,
    )

    if status != "success":
        _dedup_key = ""
        _dedup_count = 0
        _dedup_summary = ""
    else:
        _dedup_key = key
        _dedup_count = 1
        _dedup_first_summary = summary
        _dedup_summary = summary

    # Density-aware body augmentation (#1367). Only active when density is
    # non-NORMAL, so the zero-config default stays byte-identical to legacy.
    if _density != ToolResultDensity.NORMAL and status == "success":
        _render_density_body(output)


# ---------------------------------------------------------------------------
# Density-aware body rendering (#1367)
# ---------------------------------------------------------------------------


def _extract_bulk_text(output: Any) -> str:
    """Return the best "bulk content" string from a tool output for summarising."""
    if output is None:
        return ""
    if isinstance(output, str):
        return output
    if isinstance(output, dict):
        for key in ("stdout", "content", "text", "output", "result"):
            value = output.get(key)
            if isinstance(value, str) and value:
                return value
            if value:
                try:
                    return json.dumps(value, default=str)
                except Exception:
                    return str(value)
        return ""
    try:
        return str(output)
    except Exception:
        return ""


def _render_density_body(output: Any) -> None:
    """Print a density-aware body fragment below the result line (#1367).

    Only called when ``_density != NORMAL``. For ``MINIMAL`` we emit nothing.
    For ``COMPACT`` we emit a ``[+N lines]`` hint when the body was trimmed.
    For ``DETAILED`` we inline the head/tail-expanded body.
    """
    if _density == ToolResultDensity.NORMAL:
        return
    bulk = _extract_bulk_text(output)
    if _density == ToolResultDensity.MINIMAL:
        return
    if not bulk:
        return
    densified = densify_output(
        bulk,
        _density,
        head_lines=_density_head_lines,
        tail_lines=_density_tail_lines,
    )
    if not densified:
        return
    for line in densified.split("\n"):
        console.print(f"    [{MUTED}]{escape(line)}[/{MUTED}]")


def render_tool_expand() -> None:
    """Re-render the most recent tool call at ``DETAILED`` density.

    Invoked by the ``/expand`` slash command. Reuses ``_current_turn_tools``
    (or the saved ``_tool_history`` when called between turns) so no extra
    state needs to be tracked.

    #1367 follow-up: diff-backed outputs (``write_file``/``edit_file`` with
    ``_old_content``/``_new_content``) reuse ``_render_inline_diff`` with the
    ``_force_full_diff`` flag set, so the full un-collapsed diff renders
    regardless of the active density.
    """
    global _force_full_diff
    # Make sure any pending collapse-repeats group is printed before the
    # expanded render lands.
    _flush_repeat_collapse()

    tools = _current_turn_tools or _tool_history
    if not tools:
        console.print(f"[{CHROME}]No tool call to expand in the current turn.[/{CHROME}]\n")
        return
    tc = tools[-1]
    tool_name = tc.get("tool_name", "")
    status = tc.get("status", "")
    output = tc.get("output")
    elapsed = tc.get("elapsed", 0) or 0
    _s = _theme.success
    _e = _theme.error
    status_icon = f"[{_s}]  ✓[/{_s}]" if status == "success" else f"[{_e}]  ✗[/{_e}]"
    elapsed_str = f" {elapsed:.1f}s" if elapsed >= 0.1 else ""
    summary = tc.get("summary", tool_name)
    console.print(f"{status_icon} [bold]{escape(summary)}[/bold]{elapsed_str}")

    # Diff-backed results: route through the inline diff renderer with
    # hunk-collapsing disabled so ``/expand`` shows the full context.
    if status == "success" and _has_diff_data(tool_name, output) and isinstance(output, dict):
        _force_full_diff = True
        try:
            _render_inline_diff(tool_name, output)
        finally:
            _force_full_diff = False
        return

    bulk = _extract_bulk_text(output)
    if not bulk:
        err = _error_summary(output) if isinstance(output, dict) else ""
        if err:
            console.print(f"    [{_theme.error}]{escape(err)}[/{_theme.error}]")
        return
    expanded = densify_output(
        bulk,
        ToolResultDensity.DETAILED,
        head_lines=_density_head_lines,
        tail_lines=_density_tail_lines,
    )
    for line in expanded.split("\n"):
        console.print(f"    [{CHROME}]{escape(line)}[/{CHROME}]")


def render_density_change(density: ToolResultDensity) -> None:
    """Announce a runtime density change (from the ``/density`` slash command)."""
    labels = {
        ToolResultDensity.MINIMAL: "minimal",
        ToolResultDensity.COMPACT: "compact",
        ToolResultDensity.NORMAL: "normal (default)",
        ToolResultDensity.DETAILED: "detailed",
    }
    console.print(f"[{CHROME}]Density: {labels[density]}[/{CHROME}]\n")


# ---------------------------------------------------------------------------
# Visual hierarchy containers (#1370)
#
# Pure helpers that emit Rich renderables for each message type: user input,
# AI prose, system messages (info/warning/error), turn separators, and code
# blocks. Callers (render_response_end, render_error, render_warning, the
# queued-message separator, transcript_renderer) route through these helpers
# so the same theme-aware visual lanes apply consistently across the REPL
# and workflow replays.
# ---------------------------------------------------------------------------


_USER_GUTTER_CHAR = "\u2502"  # │
_ASSISTANT_GUTTER_CHAR = "\u2502"  # │
_TOOL_GUTTER_CHAR = "\u2502"  # │
_SYSTEM_GUTTER_CHAR = "\u2502"  # │


def _system_kind_style(kind: str) -> tuple[str, str]:
    """Return ``(label, color)`` for a system-message kind.

    Unknown kinds degrade to ``info``.
    """
    if kind == "error":
        return "Error", _theme.error or "red"
    if kind == "warning":
        return "Warning", _theme.warning or "yellow"
    # default / "info" / anything else
    return "Info", _theme.chrome or _theme.muted or ""


def render_user_message(
    text: str,
    *,
    position: int | None = None,
    queue_depth: int = 0,
) -> None:
    """Render a user message with the user-gutter lane.

    ``position`` and ``queue_depth`` are optional for queued-message
    rendering in the REPL: if both are provided, a ``[position/total]``
    prefix is appended to the gutter line. Whitespace-only inputs are
    still rendered (an empty gutter line is visually unhelpful but the
    caller already decides whether to invoke this helper).
    """
    color = _theme.user_gutter or _theme.accent or ""
    meta = ""
    if isinstance(position, int) and queue_depth >= 0:
        total = position + queue_depth
        meta = f" [{position}/{total}]"
    gutter = _USER_GUTTER_CHAR
    if color:
        line = f"\n[{color}]{gutter}{escape(meta)} {escape(text)}[/{color}]"
    else:
        line = f"\n{gutter}{escape(meta)} {escape(text)}"
    console.print(line)


def render_assistant_prose(markdown_text: str) -> None:
    """Render assistant prose via Rich Markdown inside a padded lane.

    Whitespace-only inputs are suppressed (matches the pre-existing
    behaviour of ``render_response_end``).
    """
    if not markdown_text or not markdown_text.strip():
        return

    from rich.padding import Padding

    _stdout_console.print(Padding(_make_markdown(markdown_text), (0, 2, 1, 2)))


def render_system_message(kind: str, text: str) -> None:
    """Render an info/warning/error system message with consistent framing."""
    label, color = _system_kind_style(kind)
    if color:
        console.print(f"\n[bold {color}]{label}:[/] {escape(text)}")
    else:
        console.print(f"\n{label}: {escape(text)}")


def render_turn_separator(char: str | None = None) -> None:
    """Render a thin horizontal separator between conversation turns.

    ``char`` defaults to ``"\u2500"`` (box-drawing light horizontal). Callers
    that have config access can pass ``config.cli.hierarchy.turn_separator_char``
    to honour user preferences.
    """
    sep_char = char if char else "\u2500"
    color = _theme.turn_separator or _theme.chrome or ""
    # Build a short separator line (24 cols is scanable without dominating the
    # terminal); the left indent matches the 2-col padding used by the other
    # hierarchy helpers.
    body = sep_char * 24
    if color:
        console.print(f"  [{color}]{body}[/{color}]")
    else:
        console.print(f"  {body}")


def _code_block_container(
    language: str,
    source: str,
    *,
    show_label: bool = True,
) -> Any:
    """Return a Rich renderable wrapping ``source`` as a syntax-highlighted
    code block, optionally prefixed by a small language label.

    Used internally by the markdown renderer for fenced code blocks and by
    future callers that render structured code output. Kept as a helper
    rather than a free-standing ``render_*`` so callers choose where to
    emit the renderable.
    """
    from rich.console import Group
    from rich.syntax import Syntax
    from rich.text import Text

    label_color = _theme.code_label or _theme.code_inline or ""
    bg = _theme.code_bg or ""
    syntax = Syntax(
        source,
        language or "text",
        theme="monokai",
        background_color=bg or None,
        word_wrap=True,
    )
    if show_label and language:
        label = Text(f"  {language}", style=label_color or "")
        return Group(label, syntax)
    return syntax


# ---------------------------------------------------------------------------
# Errors / warnings — thin wrappers around render_system_message
# ---------------------------------------------------------------------------


def render_error(message: str | dict[str, Any]) -> None:
    render_system_message("error", format_user_error(message))


def render_warning(message: str) -> None:
    render_system_message("warning", message)


def render_hook_outcome(
    outcome: str,
    tool_name: str,
    *,
    message: str = "",
    hook_id: str = "",
    error_type: str = "",
) -> None:
    """Render a hook-caused tool block, warn, or timeout on the existing error/warning surface.

    Maps hook outcomes to the closest existing surface:
    - ``"deny"`` (pre or post tool) → error surface: "Hook blocked <tool>: <message>"
    - ``"ask"`` when no approval channel → error surface: "Hook requires approval for <tool>"
    - ``"warn"`` (non-blocking, informational) → warning surface
    - ``error_type="timeout"`` → warning surface with timeout context
    - ``error_type="exception"`` → warning surface

    ``outcome="allow"`` with no ``error_type`` is a no-op (hooks that allow are
    invisible to the user).  A failed/timed-out hook still produces a warning
    even if its outcome defaults to ``"allow"`` (fail-open contract).
    """
    if outcome == "allow" and not error_type:
        return

    err = _theme.error or "red"
    warn = _theme.warning or "yellow"
    muted = _theme.muted or ""

    tool_label = escape(tool_name) if tool_name else "tool"
    msg_suffix = f": {escape(message)}" if message else ""
    id_suffix = f" [{escape(hook_id)}]" if hook_id else ""

    if error_type == "timeout":
        color = warn
        label = "Warning"
        body = f"Hook timed out for {tool_label}{id_suffix} — continuing"
    elif error_type == "exception":
        color = warn
        label = "Warning"
        body = f"Hook error for {tool_label}{id_suffix} — continuing"
    elif outcome == "deny":
        color = err
        label = "Hook blocked"
        body = f"{tool_label}{id_suffix}{msg_suffix}"
    elif outcome == "warn":
        color = warn
        label = "Hook warning"
        body = f"{tool_label}{id_suffix}{msg_suffix}"
    else:
        color = warn
        label = "Hook"
        body = f"{outcome} for {tool_label}{id_suffix}{msg_suffix}"

    if color:
        console.print(f"\n[bold {color}]{escape(label)}:[/] {body}")
    else:
        console.print(f"\n{escape(label)}: {body}")

    if muted and hook_id and outcome not in ("allow", "warn") and not error_type:
        console.print(f"  [{muted}]hook: {escape(hook_id)}[/{muted}]")


def startup_step(message: str) -> Status:
    """Create a dim animated spinner for a startup step.

    Returns a **sync** context manager (Rich Status).  Use ``with``,
    not ``async with`` — ``await`` inside a sync ``with`` block is
    valid Python in async functions::

        with renderer.startup_step("Connecting to servers..."):
            await slow_operation()
    """
    return console.status(f"  [{MUTED}]{message}[/{MUTED}]", spinner="dots12", spinner_style=MUTED)


# ---------------------------------------------------------------------------
# Welcome / help
# ---------------------------------------------------------------------------


def _get_build_date() -> str:
    try:
        from datetime import datetime

        from .._build_info import BUILD_TIMESTAMP

        dt = datetime.fromisoformat(BUILD_TIMESTAMP)
        return dt.astimezone().strftime("%b %d, %Y %I:%M %p")
    except Exception:
        return ""


_SEP = " \u00b7 "


def render_welcome(
    model: str,
    tool_count: int,
    instructions_loaded: bool,
    working_dir: str,
    git_branch: str | None = None,
    version: str = "",
    build_date: str = "",
    skill_count: int = 0,
    pack_count: int = 0,
    pack_names: list[str] | None = None,
    is_first_run: bool = False,
    project_display: str = "",
) -> None:
    display_dir = _short_path(working_dir)
    branch = f" ({git_branch})" if git_branch else ""

    console.print(Text("      \u25b2", style=GOLD))
    console.print(Text("     / \\", style=GOLD))
    console.print(Text("    /   \\", style=GOLD))
    _logo4 = Text()
    _logo4.append("   / ", style=GOLD)
    _logo4.append("\u25a0\u25a0", style=BLUE)
    _logo4.append("  \\", style=GOLD)
    _logo4.append("   ")
    _logo4.append("A N T E R O O M", style="bold")
    console.print(_logo4)
    _logo5 = Text()
    _logo5.append("  /       \\", style=GOLD)
    _logo5.append("  ")
    _logo5.append("the secure AI gateway", style=SLATE)
    console.print(_logo5)
    console.print()

    version_parts = []
    if version:
        version_parts.append(f"v{version}")
    if build_date:
        version_parts.append(f"Built {build_date}")
    if project_display:
        version_parts.append(project_display)
    console.print(f"  [{MUTED}]{_SEP.join(version_parts)}[/{MUTED}]")
    console.print()

    console.print(f"  [{SLATE}]{escape(display_dir)}{branch}[/]")
    parts = [escape(model), f"{tool_count} tools"]
    if skill_count > 0:
        parts.append(f"{skill_count} skills")
    if pack_count > 0:
        parts.append(f"{pack_count} packs")
    if instructions_loaded:
        parts.append("instructions")
    console.print(f"  [{MUTED}]{_SEP.join(parts)}[/{MUTED}]")
    if pack_names:
        console.print(f"  [{MUTED}]Packs: {', '.join(pack_names)}[/{MUTED}]")
    console.print()
    if is_first_run:
        console.print(f"  [{GOLD}]Getting started:[/{GOLD}]")
        console.print(f"  [{MUTED}]Just type a message to start chatting[/{MUTED}]")
        console.print(f"  [{MUTED}]/space init   \u2014 set up a workspace with custom instructions[/{MUTED}]")
        console.print(f"  [{MUTED}]/help         \u2014 see all commands[/{MUTED}]")
        console.print()
    else:
        console.print(f"  [{MUTED}]Type a message, or /help for commands[/{MUTED}]\n")


def render_update_available(message: str) -> None:
    console.print(f"  [{GOLD}]{escape(message)}[/{GOLD}]\n")


def render_help() -> None:
    console.print()
    console.print("  /new  /last  /list [N]  /resume <N|id>  /search <query>  /delete <N|id>  /rewind")
    console.print("  /compact  /model <name>  /tools  /skills  /reload-skills  /mcp  /verbose  /detail")
    m = MUTED
    console.print(f"  @<path> [{m}]include file[/]  Alt+Enter [{m}]newline[/]  Esc [{m}]cancel[/]  /quit \u00b7 Ctrl+D")
    console.print()


def render_tools(tool_names: list[str]) -> None:
    console.print("\n[bold]Available tools:[/bold]")
    for name in sorted(tool_names):
        console.print(f"  - {name}")
    console.print()


def render_conversation_recap(messages: list[dict[str, Any]]) -> None:
    """Show the last user/assistant exchange for context on resume."""
    last_user = None
    last_assistant = None
    for msg in reversed(messages):
        role = msg.get("role", "")
        content = msg.get("content", "")
        if not content or not isinstance(content, str):
            continue
        if role == "assistant" and last_assistant is None:
            last_assistant = content
        elif role == "user" and last_user is None:
            last_user = content
        if last_user and last_assistant:
            break

    if not last_user and not last_assistant:
        return

    console.print(f"  [{MUTED}]Last exchange:[/{MUTED}]")
    if last_user:
        truncated = last_user[:200].replace("\n", " ")
        if len(last_user) > 200:
            truncated += "..."
        console.print(f"  [{SLATE}]You:[/] [{MUTED}]{escape(truncated)}[/{MUTED}]")
    if last_assistant:
        from rich.padding import Padding

        if len(last_assistant) > 500:
            # Truncate at a line boundary to preserve markdown structure
            cut = last_assistant[:500]
            last_newline = cut.rfind("\n")
            if last_newline > 100:
                truncated = cut[:last_newline] + "\n\n..."
            else:
                truncated = cut + "\n\n..."
        else:
            truncated = last_assistant
        console.print(f"  [{SLATE}]AI:[/{SLATE}]")
        _stdout_console.print(Padding(_make_markdown(truncated), (0, 2, 0, 4)))
    console.print()


def render_compact_done(original: int, compacted: int) -> None:
    console.print(f"\n[{CHROME}]Compacted {original} messages -> {compacted} messages[/{CHROME}]")


# ---------------------------------------------------------------------------
# Status toolbar
# ---------------------------------------------------------------------------


def format_status_toolbar(
    *,
    model: str = "",
    current_tokens: int = 0,
    max_context: int = 128_000,
    message_count: int = 0,
    approval_mode: str = "",
    tool_count: int = 0,
    mcp_statuses: dict[str, dict[str, Any]] | None = None,
    space_name: str = "",
    plan_mode: bool = False,
    working_dir: str = "",
    git_branch: str = "",
    conversation_name: str = "",
    busy_status: BusyStatus | None = None,
) -> list[tuple[str, str]]:
    """Format the persistent bottom toolbar for the REPL.

    Returns a list of (style, text) tuples for prompt_toolkit FormattedText.
    """
    from .layout import _shorten_path

    parts: list[tuple[str, str]] = [("class:bottom-toolbar", " ")]

    if model:
        parts.append(("class:bottom-toolbar.model", model))
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))

    if working_dir:
        dir_text = _shorten_path(working_dir)
        if git_branch:
            dir_text += f" ({git_branch})"
        parts.append(("class:bottom-toolbar.dir", dir_text))
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))

    if conversation_name:
        parts.append(("class:bottom-toolbar.dir", conversation_name))
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))

    if space_name:
        parts.append(("class:bottom-toolbar.mcp", space_name))
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))

    if plan_mode:
        parts.append(("class:bottom-toolbar.tokens-warn", "PLAN"))
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))

    if max_context > 0:
        pct = min(100, (current_tokens / max_context) * 100) if max_context else 0
        token_text = f"{_format_tokens(current_tokens)}/{_format_tokens(max_context)} ({pct:.0f}%)"
        if pct > 75:
            parts.append(("class:bottom-toolbar.tokens-danger", token_text))
        elif pct > 50:
            parts.append(("class:bottom-toolbar.tokens-warn", token_text))
        else:
            parts.append(("class:bottom-toolbar.tokens", token_text))
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))

    if message_count > 0:
        parts.append(("class:bottom-toolbar.dim", f"{message_count} msgs"))
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))

    if approval_mode:
        parts.append(("class:bottom-toolbar.dim", approval_mode))
        parts.append(("class:bottom-toolbar.sep", " \u00b7 "))

    if tool_count > 0:
        parts.append(("class:bottom-toolbar.dim", f"{tool_count} tools"))

    # Append MCP connecting status if any servers are still resolving
    if mcp_statuses:
        connecting = [n for n, s in mcp_statuses.items() if s.get("status") == "connecting"]
        if connecting:
            parts.append(("class:bottom-toolbar.sep", " \u00b7 "))
            parts.append(("class:bottom-toolbar.mcp", f"MCP: {', '.join(connecting)}"))

    # Busy state: single unified slot for the live-turn status (#1428).
    # When thinking_text is present it already carries the label (including
    # tool-context via _phase_label() → _tool_phase_label() during tool_exec),
    # so we suppress the separate tool_label slot to avoid two competing
    # surfaces. tool_label still renders when it is the only busy signal.
    parts.extend(format_busy_status_toolbar(busy_status))

    # Strip trailing separator if present
    if parts and parts[-1][0] == "class:bottom-toolbar.sep":
        parts.pop()

    parts.append(("class:bottom-toolbar", " "))
    return parts


def format_mcp_toolbar(statuses: dict[str, dict[str, Any]]) -> list[tuple[str, str]] | None:
    """Format MCP server statuses for prompt_toolkit bottom_toolbar.

    Returns a list of (style, text) tuples for FormattedText, or None
    when all servers have resolved (toolbar should disappear).
    """
    if not statuses:
        return None

    # Check if all servers have resolved (no longer connecting)
    all_resolved = all(s.get("status") != "connecting" for s in statuses.values())
    if all_resolved:
        return None

    parts: list[tuple[str, str]] = [("class:mcp-label", " MCP: ")]
    for i, (name, info) in enumerate(statuses.items()):
        status = info.get("status", "unknown")
        if i > 0:
            parts.append(("", "  "))
        if status == "connecting":
            parts.append(("class:mcp-connecting", f"● {name}"))
        elif status == "connected":
            count = info.get("tool_count", 0)
            parts.append(("class:mcp-connected", f"✓ {name} ({count} tools)"))
        elif status == "error":
            err = info.get("error_message", "failed")
            if len(err) > 30:
                err = err[:27] + "..."
            parts.append(("class:mcp-error", f"✗ {name} ({err})"))
        else:
            parts.append(("class:mcp-connecting", f"○ {name}"))
    parts.append(("", " "))
    return parts


def render_mcp_status(statuses: dict[str, dict[str, Any]]) -> None:
    """Render MCP server status as a Rich table."""
    from rich.table import Table

    if not statuses:
        console.print(f"\n[{CHROME}]No MCP servers configured.[/{CHROME}]\n")
        return

    table = Table(title="MCP Servers", show_header=True, header_style="bold")
    table.add_column("Server", style=_theme.mcp_indicator or "cyan")
    table.add_column("Transport")
    table.add_column("Status")
    table.add_column("Tools", justify="right")

    for name, info in statuses.items():
        status = info.get("status", "unknown")
        if status == "connected":
            status_text = f"[{_theme.success}]● connected[/{_theme.success}]"
        elif status == "error":
            err = info.get("error_message", "")
            status_text = f"[{_theme.error}]● error[/{_theme.error}]"
            if err:
                # Truncate long error messages in table
                if len(err) > 40:
                    err = err[:37] + "..."
                status_text += f" [{CHROME}]({err})[/{CHROME}]"
        elif status == "disconnected":
            status_text = f"[{CHROME}]○ disconnected[/{CHROME}]"
        else:
            status_text = f"[{CHROME}]○ {status}[/{CHROME}]"

        table.add_row(
            name,
            info.get("transport", "?"),
            status_text,
            str(info.get("tool_count", 0)),
        )

    console.print()
    console.print(table)
    console.print(f"  [{CHROME}]Usage: /mcp [status <name>|connect|disconnect|reconnect <name>][/{CHROME}]\n")


def render_mcp_server_detail(name: str, statuses: dict[str, dict[str, Any]], mcp_manager: Any) -> None:
    """Render detailed diagnostics for a single MCP server."""
    if name not in statuses:
        console.print(f"\n[{_theme.error}]Unknown server: {escape(name)}[/{_theme.error}]")
        known = ", ".join(statuses.keys())
        console.print(f"  [{CHROME}]Available: {known}[/{CHROME}]\n")
        return

    info = statuses[name]
    status = info.get("status", "unknown")

    if status == "connected":
        status_styled = f"[{_theme.success}]● connected[/{_theme.success}]"
    elif status == "error":
        status_styled = f"[{_theme.error}]● error[/{_theme.error}]"
    else:
        status_styled = f"[{CHROME}]○ {status}[/{CHROME}]"

    console.print(f"\n[bold]MCP Server: {escape(name)}[/bold]")
    console.print(f"  Status:    {status_styled}")
    console.print(f"  Transport: {info.get('transport', '?')}")

    config = mcp_manager._configs.get(name)
    if config:
        if config.command:
            cmd = f"{config.command} {' '.join(config.args)}" if config.args else config.command
            console.print(f"  Command:   {escape(cmd)}")
        if config.url:
            console.print(f"  URL:       {escape(config.url)}")
        if config.env:
            console.print(f"  Env keys:  {', '.join(config.env.keys())}")
        console.print(f"  Timeout:   {config.timeout}s")

    err = info.get("error_message")
    if err:
        console.print(f"  [red]Error:     {escape(err)}[/red]")

    tool_count = info.get("tool_count", 0)
    console.print(f"  Tools:     {tool_count}")
    if tool_count > 0:
        server_tools = mcp_manager._server_tools.get(name, [])
        for t in server_tools:
            desc = t.get("description", "")
            if desc and len(desc) > 60:
                desc = desc[:60] + "..."
            if desc:
                console.print(f"    - {t['name']} [{CHROME}]({desc})[/{CHROME}]")
            else:
                console.print(f"    - {t['name']}")

    console.print()


# ---------------------------------------------------------------------------
# /detail - replay last turn's tool calls with full output
# ---------------------------------------------------------------------------


def render_tool_detail() -> None:
    """Render full detail of the last turn's tool calls."""
    if not _tool_history:
        console.print(f"[{CHROME}]No tool calls in the last turn.[/{CHROME}]\n")
        return

    console.print(f"\n[bold]Last turn: {len(_tool_history)} tool call(s)[/bold]\n")
    for i, tc in enumerate(_tool_history, 1):
        status = tc.get("status", "unknown")
        elapsed = tc.get("elapsed", 0)
        _s = _theme.success
        _e = _theme.error
        status_icon = f"[{_s}]✓[/{_s}]" if status == "success" else f"[{_e}]✗[/{_e}]"
        elapsed_str = f" ({elapsed:.1f}s)" if elapsed >= 0.1 else ""

        console.print(f"  {status_icon} [bold]{escape(tc['tool_name'])}[/bold]{elapsed_str}")

        # Show full arguments
        args_str = json.dumps(tc["arguments"], indent=2, default=str)
        for line in args_str.split("\n"):
            console.print(f"    [{MUTED}]{escape(line)}[/{MUTED}]")

        # Show output
        output = tc.get("output")
        if output:
            if isinstance(output, dict):
                if "error" in output:
                    console.print(f"    [{_theme.error}]{escape(str(output['error'])[:500])}[/{_theme.error}]")
                elif "content" in output:
                    content = str(output["content"])
                    if len(content) > 500:
                        content = content[:500] + "..."
                    for line in content.split("\n")[:20]:
                        console.print(f"    [{CHROME}]{escape(line)}[/{CHROME}]")
                    total_lines = str(output["content"]).count("\n") + 1
                    if total_lines > 20:
                        console.print(f"    [{MUTED}]... ({total_lines - 20} more lines)[/{MUTED}]")
                elif "stdout" in output:
                    stdout = str(output.get("stdout", ""))
                    if len(stdout) > 500:
                        stdout = stdout[:500] + "..."
                    for line in stdout.split("\n")[:20]:
                        console.print(f"    [{CHROME}]{escape(line)}[/{CHROME}]")
            else:
                console.print(f"    [{CHROME}]{escape(str(output)[:200])}[/{CHROME}]")
        console.print()


# ---------------------------------------------------------------------------
# Verbosity display
# ---------------------------------------------------------------------------


def render_verbosity_change(v: Verbosity) -> None:
    labels = {
        Verbosity.COMPACT: "compact",
        Verbosity.DETAILED: "detailed",
        Verbosity.VERBOSE: "verbose",
    }
    console.print(f"[{CHROME}]Verbosity: {labels[v]}[/{CHROME}]\n")


# ---------------------------------------------------------------------------
# Context footer (compact)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Sub-agent rendering
# ---------------------------------------------------------------------------

_active_subagents: dict[str, dict[str, Any]] = {}


def clear_subagent_state() -> None:
    """Reset sub-agent tracking state between sessions."""
    _active_subagents.clear()


def render_subagent_start(agent_id: str, prompt: str, model: str, depth: int) -> None:
    """Show that a sub-agent has been launched (#1460 compact surface).

    One single line per agent. Per-tool events do not print — they just bump
    the internal tool count used by ``render_subagent_end``. The terminal
    line is rendered later by ``render_subagent_end``.
    """
    _active_subagents[agent_id] = {
        "prompt": prompt,
        "model": model,
        "depth": depth,
        "tools": [],
        "start_time": time.monotonic(),
    }
    indent = "  " * depth
    truncated_prompt = _subagent_prompt_preview(prompt, limit=60)
    model_chip = f" [{MUTED}]({escape(model)})[/{MUTED}]" if model else ""
    console.print(
        f"{indent}[{GOLD}]▶ {escape(agent_id)}[/{GOLD}]{model_chip} [{CHROME}]{escape(truncated_prompt)}[/{CHROME}]"
    )


def render_subagent_tool(agent_id: str, tool_name: str, arguments: dict[str, Any] | None = None) -> None:
    """Track a sub-agent tool call (#1460 — count only, no stdout spam)."""
    info = _active_subagents.get(agent_id)
    if not info:
        return
    info["tools"].append(tool_name)


def render_subagent_end(agent_id: str, elapsed: float, tool_calls: list[str], error: str | None = None) -> None:
    """Render the sub-agent terminal status line (#1460).

    Format: ``{indent}<marker> <agent_id>: <status> · <duration> · <summary>``

    - Success → theme ``success`` color, ``✓`` marker
    - Failure → theme ``error`` color, ``✗`` marker, first-line error preview
    """
    info = _active_subagents.pop(agent_id, None)
    depth = info.get("depth", 1) if info else 1
    indent = "  " * depth
    tool_count = len(tool_calls)
    plural = "s" if tool_count != 1 else ""

    if error:
        first_line = str(error).split("\n")[0].strip()
        if len(first_line) > 80:
            first_line = first_line[:77] + "..."
        e = _theme.error
        console.print(f"{indent}[{e}]✗ {escape(agent_id)}: failed · {elapsed:.1f}s · {escape(first_line)}[/{e}]")
    else:
        s = _theme.success
        console.print(
            f"{indent}[{s}]✓ {escape(agent_id)}[/{s}] "
            f"[{MUTED}]done · {elapsed:.1f}s · {tool_count} tool{plural}[/{MUTED}]"
        )


def _subagent_prompt_preview(prompt: str, limit: int = 60) -> str:
    """Collapse newlines and truncate a sub-agent prompt for a single-line surface."""
    oneline = " ".join(prompt.split())
    if len(oneline) > limit:
        return oneline[: limit - 3].rstrip() + "..."
    return oneline


def render_rag_sources(chunks: list[Any]) -> None:
    """Render a muted line listing which sources contributed RAG context.

    Accepts either RetrievedChunk objects (with attributes) or dicts (from persisted metadata).
    """
    if not chunks:
        return
    seen: set[str] = set()
    parts: list[str] = []
    for c in chunks:
        if isinstance(c, dict):
            label = c.get("label") or "?"
            stype = c.get("type") or "?"
        else:
            label = getattr(c, "source_label", None) or "?"
            stype = getattr(c, "source_type", None) or "?"
        key = f"{stype}:{label}"
        if key in seen:
            continue
        seen.add(key)
        badge = "knowledge" if stype == "source_chunk" else "conversation"
        parts.append(f'"{escape(label)}" ({badge})')
    if parts:
        console.print(f"  [{MUTED}]Sources: {', '.join(parts)}[/{MUTED}]")


# ---------------------------------------------------------------------------
# Attribution footer (#923)
# ---------------------------------------------------------------------------

# Last attribution snapshot for the current REPL session. Stored at module
# scope because the renderer is already a module-level singleton and the
# `/attribution` slash command reads back from here.
_last_attribution: Any = None


def set_last_attribution(snapshot: Any) -> None:
    """Store the latest attribution snapshot for later ``/attribution`` expansion."""
    global _last_attribution
    _last_attribution = snapshot


def get_last_attribution() -> Any:
    """Return the last attribution snapshot (or ``None`` if the turn produced none)."""
    return _last_attribution


def render_attribution_footer(snapshot: Any) -> None:
    """Render a compact one-line attribution summary after a turn.

    Safe against None, plain objects, and older persisted dicts so replay
    of older turns without attribution metadata doesn't crash the
    renderer.
    """
    if snapshot is None:
        return
    # Structural check: accept AttributionSnapshot (has `turns` attr) or
    # a persisted dict (has `turns` key). Anything else is ignored.
    if isinstance(snapshot, dict):
        if "turns" not in snapshot:
            return
    elif getattr(snapshot, "turns", None) is None:
        return
    try:
        from .attribution_counts import _attribution_count

        if isinstance(snapshot, dict):
            turns = _attribution_count(snapshot, "turns")
            memory = _attribution_count(snapshot, "memory")
            sources = _attribution_count(snapshot, "sources")
            tools = _attribution_count(snapshot, "tools")
            packs = _attribution_count(snapshot, "packs")
            instructions = _attribution_count(snapshot, "instructions")
            dlp = int(snapshot.get("dlp_match_count", 0) or 0)
            of = int(snapshot.get("output_filter_match_count", 0) or 0)
        else:
            turns = _attribution_count(snapshot, "turns")
            memory = _attribution_count(snapshot, "memory")
            sources = _attribution_count(snapshot, "sources")
            tools = _attribution_count(snapshot, "tools")
            packs = _attribution_count(snapshot, "packs")
            instructions = _attribution_count(snapshot, "instructions")
            dlp = int(getattr(snapshot, "dlp_match_count", 0) or 0)
            of = int(getattr(snapshot, "output_filter_match_count", 0) or 0)
    except Exception:
        return
    parts: list[str] = [
        f"{turns} turns",
        f"{memory} memories",
        f"{sources} sources",
        f"{tools} tools",
        f"{packs} packs",
    ]
    # Instructions segment (#1462) — hidden when no file was loaded so the
    # default zero-context footer stays compact.
    if instructions:
        noun = "instruction file" if instructions == 1 else "instruction files"
        parts.append(f"{instructions} {noun}")
    if dlp:
        parts.append(f"DLP:{dlp}")
    if of:
        parts.append(f"OF:{of}")
    # ``\\[ctx\\]`` so Rich doesn't interpret it as a markup tag.
    console.print(f"  [{MUTED}]\\[ctx] {' · '.join(parts)}  — /attribution for detail[/{MUTED}]")


# ---------------------------------------------------------------------------
# Auto-propose memory notice (#1454)
# ---------------------------------------------------------------------------

# Compact items list (each {fqn, category, content_preview}) for the most
# recent assistant turn. Restored on conversation resume from
# ``messages.metadata["memory_auto_proposed"]`` so the inline notice
# survives reload / replay.
_last_auto_propose_notice: list[dict[str, Any]] | None = None


def set_last_auto_propose_notice(items: list[dict[str, Any]] | None) -> None:
    """Cache the latest auto-propose result for resume / replay restore."""
    global _last_auto_propose_notice
    _last_auto_propose_notice = items if items else None


def get_last_auto_propose_notice() -> list[dict[str, Any]] | None:
    """Return the cached auto-propose items, or ``None`` if the last turn produced none."""
    return _last_auto_propose_notice


def render_auto_propose_notice(items: list[dict[str, Any]] | None) -> None:
    """Render a compact one-line notice when auto-propose surfaces candidates.

    Items shape: ``[{"fqn": str, "category": str, "content_preview": str}]``.
    Renders nothing when ``items`` is empty / None — callers don't need to
    pre-check.
    """
    if not items:
        return
    count = len(items)
    suffix = "memory" if count == 1 else "memories"
    # Keep the notice tight: count + first FQN + reviewer hint.
    first_fqn = items[0].get("fqn", "")
    head = f"💡 {count} {suffix} queued for review"
    if first_fqn:
        head += f" — first: {first_fqn}"
    console.print(f"  [{MUTED}]{head}  · /memory candidates to review[/{MUTED}]")


def render_rag_status(status: str, chunk_count: int = 0, reason: str | None = None) -> None:
    """Render RAG retrieval status with consistent formatting.

    In COMPACT mode (default), suppress low-value diagnostics and soften
    failure wording.  DETAILED/VERBOSE modes show full diagnostic output.
    """
    if not _show_rag_status:
        return
    if _verbosity == Verbosity.COMPACT:
        # Only surface actionable status; suppress ok/no_results noise
        if status == "failed":
            console.print(f"  [{MUTED}]Knowledge search unavailable[/{MUTED}]")
        elif status == "no_vec_support":
            console.print(f"  [{MUTED}]Knowledge search not configured[/{MUTED}]")
        return
    # DETAILED / VERBOSE — full diagnostic output
    if status == "ok" and chunk_count > 0:
        console.print(f"  [{MUTED}][RAG: {chunk_count} relevant chunk(s) retrieved][/{MUTED}]")
    elif status == "no_results":
        suffix = f" — {reason}" if reason else ""
        console.print(f"  [{MUTED}][RAG: no results{suffix}][/{MUTED}]")
    elif status == "failed":
        console.print(f"  [{MUTED}][RAG: retrieval failed][/{MUTED}]")
    elif status == "no_vec_support":
        console.print(f"  [{MUTED}][RAG: embedding service unavailable][/{MUTED}]")
    # Silent for: disabled, no_config, skipped_plan_mode, skipped


def render_memory_recall_status(status: str, count: int = 0, reason: str | None = None) -> None:
    """Render memory recall status with consistent formatting.

    Mirrors ``render_rag_status`` but for the per-turn memory recall pipeline
    (#921).  When the gate toggle ``_show_memory_recall_status`` is off, emits
    nothing.  COMPACT mode suppresses informational messages; DETAILED/VERBOSE
    show full diagnostics.
    """
    if not _show_memory_recall_status:
        return
    if _verbosity == Verbosity.COMPACT:
        if status == "failed":
            console.print(f"  [{MUTED}]Memory recall unavailable[/{MUTED}]")
        elif status == "no_vec_support":
            console.print(f"  [{MUTED}]Memory recall not configured[/{MUTED}]")
        return
    # DETAILED / VERBOSE — full diagnostic output
    if status == "ok" and count > 0:
        console.print(f"  [{MUTED}][Memory: {count} memory(ies) recalled][/{MUTED}]")
    elif status == "no_results":
        suffix = f" — {reason}" if reason else ""
        console.print(f"  [{MUTED}][Memory: no results{suffix}][/{MUTED}]")
    elif status == "failed":
        console.print(f"  [{MUTED}][Memory: recall failed][/{MUTED}]")
    elif status == "no_vec_support":
        console.print(f"  [{MUTED}][Memory: embedding service unavailable][/{MUTED}]")
    # Silent for: disabled, skipped


def render_context_footer(
    current_tokens: int,
    auto_compact_threshold: int,
    response_tokens: int = 0,
    elapsed: float = 0.0,
    max_context: int = 128_000,
) -> None:
    """Render a compact footer showing context usage."""
    pct_full = min(100, (current_tokens / max_context) * 100)
    tokens_remaining = auto_compact_threshold - current_tokens

    if pct_full > 75:
        color = _theme.danger
    elif pct_full > 50:
        color = _theme.warning
    else:
        color = _theme.chrome

    parts = [f"{_format_tokens(current_tokens)}/{_format_tokens(max_context)} ({pct_full:.0f}%)"]
    if response_tokens:
        parts.append(f"{_format_tokens(response_tokens)} resp")
    if elapsed > 0:
        parts.append(f"{elapsed:.1f}s")
    if pct_full > 50:
        parts.append(f"compact in {_format_tokens(max(0, tokens_remaining))}")

    console.print(f"[{color}]  ▪ {' · '.join(parts)}[/{color}]")


def format_bg_indicator(count: int) -> str:
    """Return a Rich-markup string for background task count, or empty when zero.

    Used by the CLI prompt to show how many background tasks are running
    while the foreground is idle (#1313).
    """
    if count <= 0:
        return ""
    return f"[dim] [{count} bg][/dim]"
