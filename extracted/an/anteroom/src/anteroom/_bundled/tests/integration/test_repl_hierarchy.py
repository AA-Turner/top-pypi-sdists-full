"""Integration tests: visual hierarchy renders correctly end-to-end (#1370).

Drives a user → assistant → tool → assistant sequence through the
hierarchy helpers and asserts that the rendered terminal output contains
the expected gutter characters and theme color for every built-in theme.

Per `.claude/rules/ux-testing.md`, the ``cli/repl.py`` row requires CLI
integration coverage for user-facing changes. This test exercises the
exact helpers the REPL invokes when flushing an assistant response and
announcing queued user messages.
"""

from __future__ import annotations

import io
import re
from unittest.mock import patch

import pytest
from rich.console import Console

from anteroom.cli import renderer
from anteroom.cli.themes import CliTheme

_BUILTIN_THEME_NAMES = ["midnight", "dawn", "high-contrast", "accessible"]

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _hex_to_ansi_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"38;2;{r};{g};{b}"


@pytest.fixture
def _capture_console() -> tuple[Console, io.StringIO]:
    """Create a Console that writes to a StringIO with full ANSI capture."""
    buf = io.StringIO()
    con = Console(file=buf, force_terminal=True, color_system="truecolor", width=80, highlight=False)
    return con, buf


@pytest.fixture(autouse=True)
def _clear_no_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)


@pytest.fixture(autouse=True)
def _restore_midnight_theme() -> None:  # type: ignore[return]
    yield
    renderer.set_theme(CliTheme.load("midnight"))


def _run_sequence(theme_name: str) -> str:
    """Run a user → assistant → tool → assistant flow through the renderer
    and return the combined ANSI output.
    """
    theme = CliTheme.load(theme_name)
    renderer.set_theme(theme)

    buf = io.StringIO()
    capture = Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=80,
        highlight=False,
    )
    original_console = renderer.console
    original_stdout_console = renderer._stdout_console
    renderer.console = capture
    renderer._stdout_console = capture
    try:
        # 1. user message (what /repl emits when a new user turn arrives)
        renderer.render_user_message("write a unit test")
        # 2. turn separator (between turns)
        renderer.render_turn_separator()
        # 3. assistant prose (what render_response_end flushes)
        renderer.render_assistant_prose("Here is the **plan**.")
        # 4. tool call start + end (existing helpers, use theme colors)
        with patch("anteroom.cli.renderer.start_tool_ticker"):
            renderer.render_tool_call_start("bash", {"command": "pytest"})
        renderer.render_tool_call_end("bash", "success", {"stdout": "1 passed"})
        # 5. assistant prose again (follow-up response)
        renderer.render_assistant_prose("Tests are passing.")
    finally:
        renderer.console = original_console
        renderer._stdout_console = original_stdout_console
    return buf.getvalue()


class TestReplHierarchyFlow:
    """End-to-end rendering of a user → assistant → tool → assistant sequence."""

    @pytest.mark.parametrize("theme_name", _BUILTIN_THEME_NAMES)
    def test_gutter_character_present_for_user_message(self, theme_name: str) -> None:
        output = _run_sequence(theme_name)
        assert "\u2502" in output, f"user gutter '│' missing for theme '{theme_name}'"

    @pytest.mark.parametrize("theme_name", _BUILTIN_THEME_NAMES)
    def test_turn_separator_character_present(self, theme_name: str) -> None:
        output = _run_sequence(theme_name)
        assert "\u2500" in output, f"turn separator '─' missing for theme '{theme_name}'"

    @pytest.mark.parametrize("theme_name", _BUILTIN_THEME_NAMES)
    def test_user_message_text_present(self, theme_name: str) -> None:
        output = _run_sequence(theme_name)
        plain = _ANSI_RE.sub("", output)
        assert "write a unit test" in plain

    @pytest.mark.parametrize("theme_name", _BUILTIN_THEME_NAMES)
    def test_assistant_prose_text_present(self, theme_name: str) -> None:
        output = _run_sequence(theme_name)
        plain = _ANSI_RE.sub("", output)
        assert "plan" in plain
        assert "Tests are passing" in plain

    @pytest.mark.parametrize("theme_name", _BUILTIN_THEME_NAMES)
    def test_user_gutter_color_matches_theme(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        output = _run_sequence(theme_name)
        assert _hex_to_ansi_rgb(theme.user_gutter) in output, (
            f"Theme '{theme_name}' user_gutter color {theme.user_gutter} not emitted"
        )

    @pytest.mark.parametrize("theme_name", _BUILTIN_THEME_NAMES)
    def test_turn_separator_color_matches_theme(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        output = _run_sequence(theme_name)
        assert _hex_to_ansi_rgb(theme.turn_separator) in output, (
            f"Theme '{theme_name}' turn_separator color {theme.turn_separator} not emitted"
        )


class TestReplHierarchyQueuedMessage:
    """The queued-message rendering matches the live user-gutter lane."""

    @pytest.mark.parametrize("theme_name", _BUILTIN_THEME_NAMES)
    def test_queued_message_includes_position_meta(self, theme_name: str) -> None:
        theme = CliTheme.load(theme_name)
        renderer.set_theme(theme)
        buf = io.StringIO()
        capture = Console(file=buf, force_terminal=True, color_system="truecolor", width=80, highlight=False)
        original = renderer.console
        original_stdout = renderer._stdout_console
        renderer.console = capture
        renderer._stdout_console = capture
        try:
            renderer.render_user_message("next prompt", position=2, queue_depth=1)
        finally:
            renderer.console = original
            renderer._stdout_console = original_stdout
        output = buf.getvalue()
        plain = _ANSI_RE.sub("", output)
        assert "[2/3]" in plain
        assert "\u2502" in plain  # gutter still rendered
        assert _hex_to_ansi_rgb(theme.user_gutter) in output


class TestReplHierarchyNoColor:
    """Hierarchy helpers degrade to plain gutter characters under NO_COLOR."""

    @pytest.mark.parametrize("theme_name", _BUILTIN_THEME_NAMES)
    def test_no_color_strips_ansi_keeps_structure(self, theme_name: str, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("NO_COLOR", "1")
        theme = CliTheme.load(theme_name)
        renderer.set_theme(theme)

        buf = io.StringIO()
        capture = Console(
            file=buf,
            force_terminal=False,
            no_color=True,
            width=80,
            highlight=False,
        )
        original = renderer.console
        original_stdout = renderer._stdout_console
        renderer.console = capture
        renderer._stdout_console = capture
        try:
            renderer.render_user_message("hello")
            renderer.render_turn_separator()
            renderer.render_system_message("warning", "low memory")
        finally:
            renderer.console = original
            renderer._stdout_console = original_stdout
        raw = buf.getvalue()
        # 24-bit ANSI must NOT appear under NO_COLOR
        assert "\x1b[38;2;" not in raw, "24-bit ANSI leaked under NO_COLOR"
        # But the structural characters must remain readable
        assert "\u2502" in raw  # user gutter
        assert "\u2500" in raw  # turn separator
        assert "low memory" in raw
        assert "Warning" in raw
