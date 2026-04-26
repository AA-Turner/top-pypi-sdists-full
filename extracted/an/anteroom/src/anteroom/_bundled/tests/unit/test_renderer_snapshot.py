"""Snapshot-style tests for theme-aware renderer output.

Verifies that:
- set_theme() updates the module-level _theme and refreshes aliases
- _refresh_aliases() correctly updates module aliases from the theme
- Theme colors flow through render_error(), render_warning(), and
  _build_thinking_text() instead of being hardcoded
- All built-in themes round-trip correctly through set_theme()
"""

from __future__ import annotations

import io
import re
from collections.abc import Callable

import pytest
from rich.console import Console

import anteroom.cli.renderer as renderer
from anteroom.cli.renderer import (
    BusyStatus,
    Verbosity,
    _build_thinking_text,
    _refresh_aliases,
    format_busy_status_toolbar,
    format_status_toolbar,
    render_error,
    render_turn_summary,
    render_warning,
    set_theme,
    set_verbosity,
)
from anteroom.cli.themes import _BUILTIN_THEMES, CliTheme

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _capture_console() -> tuple[Console, io.StringIO]:
    """Return a (console, buffer) pair that captures Rich output as plain text."""
    buf = io.StringIO()
    con = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
    return con, buf


def _plain(text: str) -> str:
    """Strip ANSI escapes for assertion-friendly comparisons."""
    import re

    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def _hex_to_ansi_rgb(hex_color: str) -> str:
    """Convert #RRGGBB to the ANSI 24-bit foreground RGB sequence Rich emits."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"38;2;{r};{g};{b}"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clear_no_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)


@pytest.fixture(autouse=True)
def restore_midnight_theme() -> None:  # type: ignore[return]
    """Reset to midnight after every test so state doesn't leak."""
    yield
    set_theme(CliTheme.load("midnight"))


# ---------------------------------------------------------------------------
# set_theme() and _refresh_aliases()
# ---------------------------------------------------------------------------


class TestSetTheme:
    def test_set_theme_updates_module_theme(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        assert renderer._theme is dawn

    def test_set_theme_refreshes_gold_alias(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        assert renderer.GOLD == dawn.accent

    def test_set_theme_refreshes_muted_alias(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        assert renderer.MUTED == dawn.muted

    def test_set_theme_refreshes_chrome_alias(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        assert renderer.CHROME == dawn.chrome

    def test_set_theme_refreshes_error_red_alias(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        assert renderer.ERROR_RED == dawn.error

    def test_set_theme_refreshes_slate_alias(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        assert renderer.SLATE == dawn.secondary

    def test_set_theme_refreshes_blue_alias(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        assert renderer.BLUE == dawn.logo_blue

    def test_set_theme_midnight_accent(self) -> None:
        midnight = CliTheme.load("midnight")
        set_theme(midnight)
        assert renderer._theme.accent == midnight.accent

    def test_set_theme_dawn_accent(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        assert renderer._theme.accent == dawn.accent

    def test_aliases_differ_between_themes(self) -> None:
        set_theme(CliTheme.load("midnight"))
        midnight_gold = renderer.GOLD

        set_theme(CliTheme.load("dawn"))
        dawn_gold = renderer.GOLD

        # Midnight accent is #C5A059; dawn accent is #B8860B — they must differ
        assert midnight_gold != dawn_gold

    def test_set_theme_replaces_markdown_theme_instead_of_stacking(self) -> None:
        original_console = renderer.console
        original_stdout_console = renderer._stdout_console
        renderer.console, _ = _capture_console()
        renderer._stdout_console, _ = _capture_console()
        try:
            baseline = len(renderer.console._theme_stack._entries)
            set_theme(CliTheme.load("dawn"))
            after_first = len(renderer.console._theme_stack._entries)
            set_theme(CliTheme.load("midnight"))
            after_second = len(renderer.console._theme_stack._entries)
        finally:
            renderer.console = original_console
            renderer._stdout_console = original_stdout_console
        assert after_first == baseline + 1
        assert after_second == baseline + 1


class TestRefreshAliases:
    def test_refresh_aliases_updates_gold(self) -> None:
        renderer._theme = CliTheme.load("dawn")
        _refresh_aliases()
        assert renderer.GOLD == CliTheme.load("dawn").accent

    def test_refresh_aliases_updates_muted(self) -> None:
        renderer._theme = CliTheme.load("high-contrast")
        _refresh_aliases()
        assert renderer.MUTED == CliTheme.load("high-contrast").muted

    def test_refresh_aliases_updates_chrome(self) -> None:
        renderer._theme = CliTheme.load("accessible")
        _refresh_aliases()
        assert renderer.CHROME == CliTheme.load("accessible").chrome

    def test_refresh_aliases_all_fields_in_sync(self) -> None:
        theme = CliTheme.load("dawn")
        renderer._theme = theme
        _refresh_aliases()
        assert renderer.GOLD == theme.accent
        assert renderer.SLATE == theme.secondary
        assert renderer.BLUE == theme.logo_blue
        assert renderer.MUTED == theme.muted
        assert renderer.CHROME == theme.chrome
        assert renderer.ERROR_RED == theme.error


# ---------------------------------------------------------------------------
# Dawn theme accent
# ---------------------------------------------------------------------------


class TestDawnThemeAccent:
    def test_dawn_accent_value(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        assert renderer._theme.accent == "#B8860B"

    def test_dawn_error_value(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        assert renderer._theme.error == "#DC2626"

    def test_dawn_warning_value(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        assert renderer._theme.warning == "#D97706"


# ---------------------------------------------------------------------------
# Midnight theme aliases
# ---------------------------------------------------------------------------


class TestMidnightAliases:
    def test_midnight_gold_alias(self) -> None:
        set_theme(CliTheme.load("midnight"))
        assert renderer.GOLD == "#C5A059"

    def test_midnight_muted_alias(self) -> None:
        set_theme(CliTheme.load("midnight"))
        assert renderer.MUTED == "#8b8b8b"

    def test_midnight_chrome_alias(self) -> None:
        set_theme(CliTheme.load("midnight"))
        assert renderer.CHROME == "#6b7280"

    def test_midnight_error_alias(self) -> None:
        set_theme(CliTheme.load("midnight"))
        assert renderer.ERROR_RED == "#CD6B6B"


# ---------------------------------------------------------------------------
# render_error() uses theme error color
# ---------------------------------------------------------------------------


class TestRenderErrorTheme:
    def test_render_error_uses_theme_error_color(self) -> None:
        """render_error() must embed the theme's error color, not 'red'."""
        dawn = CliTheme.load("dawn")
        set_theme(dawn)

        buf = io.StringIO()
        # Patch the module-level console so render_error() writes to our buffer
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            render_error("something went wrong")
        finally:
            renderer.console = original_console

        output = buf.getvalue()
        # Rich converts #RRGGBB to ANSI 24-bit sequences; check for the RGB portion
        assert _hex_to_ansi_rgb(dawn.error) in output
        assert "something went wrong" in _plain(output)

    def test_render_error_output_contains_error_label(self) -> None:
        set_theme(CliTheme.load("midnight"))

        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            render_error("disk full")
        finally:
            renderer.console = original_console

        plain = _plain(buf.getvalue())
        assert "Error:" in plain
        assert "disk full" in plain

    def test_render_error_midnight_error_color(self) -> None:
        midnight = CliTheme.load("midnight")
        set_theme(midnight)

        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            render_error("connection refused")
        finally:
            renderer.console = original_console

        assert _hex_to_ansi_rgb(midnight.error) in buf.getvalue()

    def test_render_error_no_hardcoded_red(self) -> None:
        """'red' must not appear as a standalone markup tag in error output."""
        set_theme(CliTheme.load("midnight"))

        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            render_error("boom")
        finally:
            renderer.console = original_console

        # Rich markup uses [red] or [red bold]; neither should be present
        # when the theme drives the color via a hex value
        raw = buf.getvalue()
        assert "[red]" not in raw
        assert "[red bold]" not in raw


# ---------------------------------------------------------------------------
# render_warning() uses theme warning color
# ---------------------------------------------------------------------------


class TestRenderWarningTheme:
    def test_render_warning_uses_theme_warning_color(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)

        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            render_warning("low memory")
        finally:
            renderer.console = original_console

        output = buf.getvalue()
        assert _hex_to_ansi_rgb(dawn.warning) in output
        assert "low memory" in _plain(output)

    def test_render_warning_output_contains_warning_label(self) -> None:
        set_theme(CliTheme.load("midnight"))

        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            render_warning("approaching token limit")
        finally:
            renderer.console = original_console

        plain = _plain(buf.getvalue())
        assert "Warning:" in plain
        assert "approaching token limit" in plain

    def test_render_warning_no_hardcoded_yellow(self) -> None:
        set_theme(CliTheme.load("midnight"))

        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            render_warning("something")
        finally:
            renderer.console = original_console

        raw = buf.getvalue()
        assert "[yellow]" not in raw
        assert "[yellow bold]" not in raw

    def test_render_warning_accessible_theme(self) -> None:
        accessible = CliTheme.load("accessible")
        set_theme(accessible)

        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            render_warning("cvd safe warning")
        finally:
            renderer.console = original_console

        assert _hex_to_ansi_rgb(accessible.warning) in buf.getvalue()


# ---------------------------------------------------------------------------
# _build_thinking_text() uses theme colors
# ---------------------------------------------------------------------------


class TestBuildThinkingTextTheme:
    def test_thinking_text_uses_accent_color(self) -> None:
        midnight = CliTheme.load("midnight")
        set_theme(midnight)
        # elapsed must be >= _REPL_THINKING_REVEAL_DELAY (2s) to produce output (#1052)
        text = _build_thinking_text(2.5)
        # The accent ANSI code should appear in the output
        assert midnight.ansi_fg("accent") in text

    def test_thinking_text_elapsed_uses_chrome_color(self) -> None:
        midnight = CliTheme.load("midnight")
        set_theme(midnight)
        # Use elapsed > 3.0 to get the timer line (#1052 raised calm window to 3s)
        text = _build_thinking_text(4.0)
        assert midnight.ansi_fg("chrome") in text

    def test_thinking_text_error_uses_error_color(self) -> None:
        midnight = CliTheme.load("midnight")
        set_theme(midnight)
        text = _build_thinking_text(1.0, error_msg="timeout")
        assert midnight.ansi_fg("error") in text

    def test_thinking_text_dawn_accent(self) -> None:
        dawn = CliTheme.load("dawn")
        set_theme(dawn)
        text = _build_thinking_text(2.5)
        assert dawn.ansi_fg("accent") in text

    def test_thinking_text_high_contrast_accent(self) -> None:
        hc = CliTheme.load("high-contrast")
        set_theme(hc)
        text = _build_thinking_text(2.5)
        assert hc.ansi_fg("accent") in text

    def test_thinking_text_muted_in_cancel(self) -> None:
        midnight = CliTheme.load("midnight")
        set_theme(midnight)
        text = _build_thinking_text(1.0, cancel_msg="cancelled")
        assert midnight.ansi_fg("muted") in text

    def test_thinking_text_zero_elapsed_cancel_is_sane(self) -> None:
        set_theme(CliTheme.load("midnight"))
        text = _build_thinking_text(0.0, cancel_msg="cancelled")
        plain = _plain(text)
        assert "cancelled" in plain
        assert "0s" in plain
        assert not re.search(r"\b\d{6,}s\b", plain)


# ---------------------------------------------------------------------------
# All built-in themes round-trip through set_theme()
# ---------------------------------------------------------------------------


class TestAllBuiltInThemes:
    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_set_theme_returns_correct_theme_object(self, theme_name: str) -> None:
        expected = CliTheme.load(theme_name)
        set_theme(expected)
        assert renderer._theme is expected

    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_aliases_match_theme_after_set(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        set_theme(theme)
        assert renderer.GOLD == theme.accent
        assert renderer.MUTED == theme.muted
        assert renderer.CHROME == theme.chrome
        assert renderer.ERROR_RED == theme.error

    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_render_error_uses_theme_error_for_each_builtin(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        set_theme(theme)

        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            render_error("test error")
        finally:
            renderer.console = original_console

        assert _hex_to_ansi_rgb(theme.error) in buf.getvalue()

    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_render_warning_uses_theme_warning_for_each_builtin(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        set_theme(theme)

        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            render_warning("test warning")
        finally:
            renderer.console = original_console

        assert _hex_to_ansi_rgb(theme.warning) in buf.getvalue()

    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_theme_accent_is_non_empty(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        assert theme.accent != ""

    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_theme_error_is_non_empty(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        assert theme.error != ""

    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_theme_warning_is_non_empty(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        assert theme.warning != ""


# ---------------------------------------------------------------------------
# Busy toolbar visual snapshot tests (#1134)
# ---------------------------------------------------------------------------


class TestBusyToolbarTheme:
    """Verify that busy-state toolbar segments use the correct theme colors."""

    @pytest.fixture(autouse=True)
    def restore_midnight_theme(self) -> None:
        yield
        set_theme(CliTheme.load("midnight"))

    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_toolbar_busy_thinking_text_present(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        set_theme(theme)
        busy = BusyStatus(thinking_text="Thinking... 6s")
        result = format_status_toolbar(model="gpt-4o", busy_status=busy)
        text = "".join(t[1] for t in result)
        assert "Thinking... 6s" in text

    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_toolbar_busy_thinking_uses_warn_style(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        set_theme(theme)
        busy = BusyStatus(thinking_text="Thinking... 6s")
        result = format_status_toolbar(busy_status=busy)
        thinking_parts = [t for t in result if "Thinking" in t[1]]
        assert thinking_parts
        assert thinking_parts[0][0] == "class:bottom-toolbar.tokens-warn"

    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_toolbar_busy_cancel_hint_uses_dim_style(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        set_theme(theme)
        busy = BusyStatus(thinking_text="Thinking... 10s", show_cancel_hint=True)
        result = format_status_toolbar(busy_status=busy)
        cancel_parts = [t for t in result if "esc to cancel" in t[1]]
        assert cancel_parts
        assert cancel_parts[0][0] == "class:bottom-toolbar.dim"

    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_toolbar_busy_tool_label_uses_model_style(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        set_theme(theme)
        busy = BusyStatus(thinking_text="", tool_label="grep")
        result = format_status_toolbar(busy_status=busy)
        tool_parts = [t for t in result if "grep" in t[1]]
        assert tool_parts
        assert tool_parts[0][0] == "class:bottom-toolbar.model"


# ---------------------------------------------------------------------------
# Toolbar snapshots for unified live-turn status (#1428)
# ---------------------------------------------------------------------------


class TestUnifiedStatusToolbarSnapshot:
    """Snapshot-style checks that the unified live-turn status surface (#1428)
    produces exactly one busy slot, regardless of phase.
    """

    @pytest.fixture(autouse=True)
    def restore_midnight_theme(self) -> None:
        yield
        set_theme(CliTheme.load("midnight"))

    def test_format_toolbar_busy_thinking_snapshot(self) -> None:
        set_theme(CliTheme.load("midnight"))
        busy = BusyStatus(thinking_text="Thinking... 4s")
        result = format_status_toolbar(model="gpt-4o", busy_status=busy)
        text = "".join(t[1] for t in result)
        # Exactly one busy indicator — no lingering 'tool_label' slot
        assert text.count("Thinking") == 1
        assert "Thinking... 4s" in text

    def test_format_toolbar_busy_tool_exec_single_slot_snapshot(self) -> None:
        """tool_exec phase: thinking_text carries tool context, tool_label is None.

        The toolbar must show one slot, not two. This is the core visual change
        of #1428.
        """
        set_theme(CliTheme.load("midnight"))
        # Unified surface: thinking_text owns the tool label; tool_label is None.
        busy = BusyStatus(thinking_text="Reading src/foo.py... 3s", tool_label=None)
        result = format_status_toolbar(model="gpt-4o", busy_status=busy)
        text = "".join(t[1] for t in result)
        assert "Reading src/foo.py" in text
        # No duplicated "src/foo.py" from a second slot
        assert text.count("src/foo.py") == 1

    def test_format_toolbar_busy_retry_snapshot(self) -> None:
        set_theme(CliTheme.load("midnight"))
        busy = BusyStatus(thinking_text="Thinking... 7s  retry 2/3")
        result = format_status_toolbar(model="gpt-4o", busy_status=busy)
        text = "".join(t[1] for t in result)
        assert "retry 2/3" in text
        assert "Thinking" in text

    def test_format_busy_status_toolbar_only_returns_live_slot(self) -> None:
        busy = BusyStatus(thinking_text="Thinking... 7s  retry 2/3", tool_label="read_file", show_cancel_hint=True)
        result = format_busy_status_toolbar(busy)
        text = "".join(t[1] for t in result)
        assert "Thinking... 7s  retry 2/3" in text
        assert "read_file" not in text
        assert "esc to cancel" in text

    def test_render_turn_summary_success_snapshot(self) -> None:
        set_theme(CliTheme.load("midnight"))
        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=False, width=120, highlight=False)
        try:
            set_verbosity(Verbosity.COMPACT)
            render_turn_summary(
                elapsed=3.2,
                tools=[{"tool_name": "read_file"}],
                cancelled=False,
                error=None,
            )
        finally:
            renderer.console = original_console
            set_verbosity(Verbosity.COMPACT)
        plain = _plain(buf.getvalue())
        assert "done" in plain
        assert "3.2s" in plain
        assert "1 tool" in plain

    def test_render_turn_summary_cancelled_snapshot(self) -> None:
        set_theme(CliTheme.load("midnight"))
        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=False, width=120, highlight=False)
        try:
            render_turn_summary(elapsed=1.1, tools=[], cancelled=True, error=None)
        finally:
            renderer.console = original_console
        plain = _plain(buf.getvalue())
        assert "cancelled" in plain
        assert "1.1s" in plain

    def test_render_turn_summary_error_snapshot(self) -> None:
        set_theme(CliTheme.load("midnight"))
        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=False, width=120, highlight=False)
        try:
            render_turn_summary(elapsed=2.0, tools=[], cancelled=False, error="connection refused")
        finally:
            renderer.console = original_console
        plain = _plain(buf.getvalue())
        assert "failed" in plain
        assert "connection refused" in plain
        assert "2.0s" in plain

    @pytest.mark.parametrize("theme_name", list(_BUILTIN_THEMES.keys()))
    def test_render_turn_summary_uses_theme_colors(self, theme_name: str) -> None:
        """Turn summary must route success/error/muted via the active theme."""
        theme = CliTheme.load(theme_name)
        set_theme(theme)
        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            # Success should emit the theme's success color
            render_turn_summary(elapsed=1.0, tools=[], cancelled=False, error=None)
        finally:
            renderer.console = original_console
        raw = buf.getvalue()
        assert _hex_to_ansi_rgb(theme.success) in raw


# ---------------------------------------------------------------------------
# Sub-agent live status surface snapshots (#1460)
#
# The compact live-status surface replaces the breadcrumb-per-tool rendering
# with one start line + one terminal line per agent. Per-tool events only
# bump the internal count; they do not print.
# ---------------------------------------------------------------------------


class TestSubagentLiveStatusSnapshot:
    @pytest.fixture(autouse=True)
    def _reset(self) -> None:
        set_theme(CliTheme.load("midnight"))
        renderer.clear_subagent_state()
        yield
        renderer.clear_subagent_state()
        set_theme(CliTheme.load("midnight"))

    def _capture(self, func: Callable[[], None]) -> str:
        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=False, width=120, highlight=False)
        try:
            func()
        finally:
            renderer.console = original_console
        return _plain(buf.getvalue())

    def test_start_renders_single_compact_line(self) -> None:
        plain = self._capture(
            lambda: renderer.render_subagent_start(
                "agent-1", prompt="analyze the log for error spikes", model="haiku", depth=1
            )
        )
        # Exactly one line — compact, not the prior two-line "▶ Agent" header.
        non_blank = [line for line in plain.splitlines() if line.strip()]
        assert len(non_blank) == 1
        assert "agent-1" in plain
        assert "haiku" in plain
        assert "analyze the log" in plain
        # Start glyph (▶) anchors the eye at launch.
        assert "▶" in plain

    def test_tool_events_do_not_print(self) -> None:
        """tool_call_start must only bump internal tool count — no stdout spam."""
        renderer.render_subagent_start("agent-1", prompt="x", model="haiku", depth=1)
        plain = self._capture(
            lambda: (
                renderer.render_subagent_tool("agent-1", "read_file", {"file_path": "/a"}),
                renderer.render_subagent_tool("agent-1", "bash", {"command": "ls"}),
            )
        )
        assert plain.strip() == ""

    def test_terminal_success_line(self) -> None:
        renderer.render_subagent_start("agent-1", prompt="x", model="haiku", depth=1)
        plain = self._capture(
            lambda: renderer.render_subagent_end(
                "agent-1", elapsed=2.3, tool_calls=["read_file", "bash", "grep"], error=None
            )
        )
        non_blank = [line for line in plain.splitlines() if line.strip()]
        assert len(non_blank) == 1
        assert "agent-1" in plain
        assert "2.3s" in plain
        assert "3 tool" in plain
        # Success marker must be present; failure marker must not be.
        assert "✓" in plain
        assert "✗" not in plain

    def test_terminal_failure_line_uses_error_theme(self) -> None:
        theme = CliTheme.load("midnight")
        set_theme(theme)
        renderer.render_subagent_start("agent-1", prompt="x", model="haiku", depth=1)
        buf = io.StringIO()
        original_console = renderer.console
        renderer.console = Console(file=buf, force_terminal=True, color_system="truecolor", width=120, highlight=False)
        try:
            renderer.render_subagent_end("agent-1", elapsed=1.1, tool_calls=[], error="boom crashed hard")
        finally:
            renderer.console = original_console
        raw = buf.getvalue()
        plain = _plain(raw)
        assert "✗" in plain
        assert "boom crashed hard" in plain
        # Error must route through the theme error color, not hardcoded red.
        assert _hex_to_ansi_rgb(theme.error) in raw

    def test_parallel_agents_each_render_independently(self) -> None:
        plain = self._capture(
            lambda: (
                renderer.render_subagent_start("agent-1", prompt="task A", model="haiku", depth=1),
                renderer.render_subagent_start("agent-2", prompt="task B", model="haiku", depth=1),
                # tool events do not print
                renderer.render_subagent_tool("agent-1", "read_file", {}),
                renderer.render_subagent_tool("agent-2", "bash", {}),
                renderer.render_subagent_end("agent-1", elapsed=1.5, tool_calls=["read_file"], error=None),
                renderer.render_subagent_end("agent-2", elapsed=2.0, tool_calls=["bash"], error=None),
            )
        )
        # Four lines: two starts, two ends. No per-tool lines.
        non_blank = [line for line in plain.splitlines() if line.strip()]
        assert len(non_blank) == 4
        assert plain.count("agent-1") == 2
        assert plain.count("agent-2") == 2


# ---------------------------------------------------------------------------
# Detached agent completion notification label tests (#1461)
#
# poll_detached_agents uses get_run_label() so the description shows in the
# notification when present; falls back to prompt-derived title otherwise.
# ---------------------------------------------------------------------------


class TestDetachedNotificationLabel:
    """Verify get_run_label() is used in the detached completion notification."""

    @pytest.fixture(autouse=True)
    def _reset(self) -> None:
        set_theme(CliTheme.load("midnight"))
        renderer.clear_subagent_state()
        yield
        renderer.clear_subagent_state()
        set_theme(CliTheme.load("midnight"))

    def _run_poll(self, runs: list[dict]) -> str:
        """Run poll_detached_agents with fake completed runs, capture output."""
        from unittest.mock import MagicMock

        from anteroom.cli.repl import poll_detached_agents

        buf = io.StringIO()
        console = Console(file=buf, force_terminal=False, width=120, highlight=False)

        fake_mgr = MagicMock()
        fake_mgr.poll_completed.return_value = runs
        poll_detached_agents(fake_mgr, console)
        return _plain(buf.getvalue())

    def _make_run(
        self, status: str = "completed", description: str | None = None, title: str = "do something useful"
    ) -> dict:
        import uuid

        meta: dict = {
            "elapsed_seconds": 1.5,
            "task_result": {
                "summary": "analysis done",
                "tool_calls": ["read_file"],
                "duration_seconds": 1.5,
            },
        }
        if description is not None:
            meta["description"] = description
        return {
            "id": str(uuid.uuid4()),
            "status": status,
            "title": title,
            "metadata": meta,
        }

    def test_description_shown_in_completed_notification(self) -> None:
        """Run with description → notification shows description as label."""
        run = self._make_run(status="completed", description="Investigate auth bug")
        plain = self._run_poll([run])
        assert "Investigate auth bug" in plain

    def test_title_fallback_when_no_description(self) -> None:
        """Run without description → notification falls back to prompt-derived title."""
        run = self._make_run(status="completed", description=None, title="analyze the logs")
        plain = self._run_poll([run])
        assert "analyze the logs" in plain

    def test_description_shown_in_failed_notification(self) -> None:
        """Failed run with description → description in notification."""
        meta: dict = {
            "elapsed_seconds": 0.5,
            "error": "connection refused",
            "task_result": {
                "summary": "",
                "tool_calls": [],
                "duration_seconds": 0.5,
                "error": "connection refused",
            },
            "description": "Deploy check",
        }
        import uuid

        run = {"id": str(uuid.uuid4()), "status": "failed", "title": "long prompt text", "metadata": meta}
        plain = self._run_poll([run])
        assert "Deploy check" in plain

    def test_no_label_part_when_no_description_and_no_title(self) -> None:
        """Run with no description and no title → no label quotes in output."""
        import uuid

        meta: dict = {
            "elapsed_seconds": 1.0,
            "task_result": {"summary": "", "tool_calls": [], "duration_seconds": 1.0},
        }
        run = {"id": str(uuid.uuid4()), "status": "completed", "title": "", "metadata": meta}
        plain = self._run_poll([run])
        # No quoted label segment should appear
        assert "\u201c" not in plain  # left double quotation mark


# ---------------------------------------------------------------------------
# Footer-mode availability snapshots (#1512)
#
# Verify that start_thinking() enters footer mode only when the prompt_toolkit
# toolbar surface is live, and falls back to the raw in-place line path when
# the toolbar is inactive.
# ---------------------------------------------------------------------------


class TestFooterModeAvailability:
    """start_thinking() path selection based on toolbar-active probe (#1512)."""

    def setup_method(self) -> None:
        self._orig_repl = renderer._repl_mode
        self._orig_footer = renderer._footer_mode
        self._orig_inv = renderer._toolbar_invalidator
        self._orig_active = renderer._toolbar_is_active
        self._orig_stdout = renderer._stdout
        self._orig_plan_visible = renderer._plan_visible
        self._orig_plan_steps = renderer._plan_steps
        self._orig_spinner = renderer._spinner
        self._orig_task = renderer._thinking_ticker_task
        renderer._thinking_ticker_task = None
        renderer._spinner = None
        renderer._plan_visible = False
        renderer._plan_steps = []

    def teardown_method(self) -> None:
        renderer._repl_mode = self._orig_repl
        renderer._footer_mode = self._orig_footer
        renderer._toolbar_invalidator = self._orig_inv
        renderer._toolbar_is_active = self._orig_active
        renderer._stdout = self._orig_stdout
        renderer._plan_visible = self._orig_plan_visible
        renderer._plan_steps = self._orig_plan_steps
        renderer._spinner = self._orig_spinner
        renderer._thinking_ticker_task = self._orig_task

    def test_footer_mode_entered_when_toolbar_active(self) -> None:
        """start_thinking() sets _footer_mode=True when both invalidator and active probe are live."""
        renderer._repl_mode = True
        renderer._toolbar_invalidator = lambda: None
        renderer._toolbar_is_active = lambda: True
        renderer._stdout = io.StringIO()

        renderer.start_thinking()

        assert renderer._footer_mode is True

    def test_footer_mode_not_entered_when_toolbar_inactive(self) -> None:
        """start_thinking() stays on raw-line path when toolbar surface is not running (#1512)."""
        renderer._repl_mode = True
        renderer._toolbar_invalidator = lambda: None
        renderer._toolbar_is_active = lambda: False
        buf = io.StringIO()
        renderer._stdout = buf

        renderer.start_thinking(newline=True)

        assert renderer._footer_mode is False
        # Raw-line path writes to _stdout — buffer must have received output.
        assert len(buf.getvalue()) > 0

    def test_footer_mode_not_entered_when_toolbar_inactive_no_stdout_call(self) -> None:
        """Invalidator is NOT called when toolbar surface is inactive."""
        called: list[int] = []
        renderer._repl_mode = True
        renderer._toolbar_invalidator = lambda: called.append(1)
        renderer._toolbar_is_active = lambda: False
        renderer._stdout = io.StringIO()

        renderer.start_thinking()

        assert called == []
