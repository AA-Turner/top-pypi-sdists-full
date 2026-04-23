"""Visual hierarchy snapshot tests (#1370).

Uses Syrupy to snapshot the Rich-rendered output of each new hierarchy helper
across all four built-in themes so any unintended ANSI/layout drift shows up
as a reviewable diff in
``tests/unit/__snapshots__/test_renderer_hierarchy_snapshot.ambr``.

Per `.claude/rules/ux-testing.md`, `cli/renderer.py` changes MUST have
Syrupy visual snapshot coverage.
"""

from __future__ import annotations

import io
import sys
import time

import pytest
from rich.console import Console

from anteroom.cli import renderer
from anteroom.cli.themes import CliTheme

_THEME_NAMES = ["midnight", "dawn", "high-contrast", "accessible"]


@pytest.fixture(autouse=True)
def _clear_no_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)


@pytest.fixture(autouse=True)
def _restore_midnight_theme() -> None:  # type: ignore[return]
    """Restore the midnight theme after each test so state does not leak."""
    yield
    renderer.set_theme(CliTheme.load("midnight"))


@pytest.fixture(autouse=True)
def _reset_renderer_state() -> None:
    """Keep hierarchy snapshots isolated from leaked REPL/footer state."""
    renderer.reset_streaming()
    renderer.clear_plan()
    renderer.clear_turn_history()
    renderer.console = Console(stderr=True)
    renderer._stdout_console = Console()
    renderer._stdout = sys.stdout
    renderer._repl_mode = False
    renderer._footer_mode = False
    renderer._toolbar_invalidator = None
    renderer._thinking_start = 0.0
    renderer._thinking_line_visible = False
    renderer._plan_written_lines = 0
    yield
    renderer.reset_streaming()
    renderer.clear_plan()
    renderer.clear_turn_history()
    renderer.console = Console(stderr=True)
    renderer._stdout_console = Console()
    renderer._stdout = sys.stdout
    renderer._repl_mode = False
    renderer._footer_mode = False
    renderer._toolbar_invalidator = None
    renderer._thinking_start = 0.0
    renderer._thinking_line_visible = False
    renderer._plan_written_lines = 0


def _render_to_string(callable_) -> str:  # type: ignore[no-untyped-def]
    """Run ``callable_`` with a fresh capture Console and return ANSI output."""
    buf = io.StringIO()
    capture = Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=80,
        highlight=False,
        record=False,
    )
    original_console = renderer.console
    original_stdout_console = renderer._stdout_console
    renderer.console = capture
    renderer._stdout_console = capture
    try:
        callable_()
    finally:
        renderer.console = original_console
        renderer._stdout_console = original_stdout_console
    return buf.getvalue()


def _normalize_snapshot_text(text: str) -> str:
    """Strip surrounding blank lines so snapshots stay git-clean."""
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(line.rstrip() for line in lines)


class _PersistentFrameLive:
    """Fake Live that preserves its final frame when transient=False."""

    def __init__(
        self,
        renderable,
        *,
        console,
        refresh_per_second: float,
        transient: bool,
        vertical_overflow: str,
    ) -> None:
        self.renderable = renderable
        self.console = console
        self.transient = transient

    def start(self) -> None:
        return None

    def update(self, renderable, refresh: bool = True) -> None:
        self.renderable = renderable

    def stop(self) -> None:
        if not self.transient:
            self.console.print(self.renderable)


# ---------------------------------------------------------------------------
# render_user_message
# ---------------------------------------------------------------------------


class TestRenderUserMessage:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        out = _render_to_string(lambda: renderer.render_user_message("hello world"))
        assert out == snapshot

    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_snapshot_with_queue(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        out = _render_to_string(
            lambda: renderer.render_user_message(
                "second queued",
                position=2,
                queue_depth=1,
            )
        )
        assert out == snapshot

    def test_contains_gutter_char(self) -> None:
        renderer.set_theme(CliTheme.load("midnight"))
        out = _render_to_string(lambda: renderer.render_user_message("hello"))
        assert "\u2502" in out  # left gutter "│"
        assert "hello" in out


# ---------------------------------------------------------------------------
# render_assistant_prose
# ---------------------------------------------------------------------------


class TestRenderAssistantProse:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        out = _render_to_string(lambda: renderer.render_assistant_prose("This is the **assistant** reply."))
        assert out == snapshot

    def test_empty_text_is_noop(self) -> None:
        renderer.set_theme(CliTheme.load("midnight"))
        out = _render_to_string(lambda: renderer.render_assistant_prose(""))
        assert out == ""

    def test_whitespace_only_is_noop(self) -> None:
        renderer.set_theme(CliTheme.load("midnight"))
        out = _render_to_string(lambda: renderer.render_assistant_prose("   \n  "))
        assert out == ""

    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_streamed_turn_snapshot(self, theme_name: str, snapshot, monkeypatch: pytest.MonkeyPatch) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))

        def _stream_then_finalize() -> None:
            monkeypatch.setattr("anteroom.cli.streaming.Live", _PersistentFrameLive)
            renderer.configure_streaming(enabled=True, refresh_hz=60.0)
            try:
                for chunk in [
                    "This is the ",
                    "**streamed** ",
                    "assistant reply.",
                ]:
                    renderer.render_token(chunk)
                    time.sleep(0.02)
                renderer.render_response_end()
            finally:
                renderer.reset_streaming()

        out = _normalize_snapshot_text(_render_to_string(_stream_then_finalize))
        assert out == snapshot


# ---------------------------------------------------------------------------
# render_system_message
# ---------------------------------------------------------------------------


class TestRenderSystemMessage:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    @pytest.mark.parametrize("kind", ["info", "warning", "error"])
    def test_snapshot(self, theme_name: str, kind: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        out = _render_to_string(lambda: renderer.render_system_message(kind, f"a {kind} message"))
        assert out == snapshot

    def test_unknown_kind_defaults_to_info(self) -> None:
        renderer.set_theme(CliTheme.load("midnight"))
        out = _render_to_string(lambda: renderer.render_system_message("nonexistent", "body"))
        assert "body" in out

    def test_error_kind_uses_theme_error_color(self) -> None:
        midnight = CliTheme.load("midnight")
        renderer.set_theme(midnight)
        out = _render_to_string(lambda: renderer.render_system_message("error", "boom"))
        h = midnight.error.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        assert f"38;2;{r};{g};{b}" in out


# ---------------------------------------------------------------------------
# render_turn_separator
# ---------------------------------------------------------------------------


class TestRenderTurnSeparator:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_snapshot(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        out = _render_to_string(lambda: renderer.render_turn_separator())
        assert out == snapshot

    def test_default_char_is_line(self) -> None:
        renderer.set_theme(CliTheme.load("midnight"))
        out = _render_to_string(lambda: renderer.render_turn_separator())
        assert "\u2500" in out


# ---------------------------------------------------------------------------
# _code_block_container
# ---------------------------------------------------------------------------


class TestCodeBlockContainer:
    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_snapshot_with_language(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        out = _render_to_string(
            lambda: renderer.console.print(renderer._code_block_container("python", "print('hi')\n", show_label=True))
        )
        assert out == snapshot

    @pytest.mark.parametrize("theme_name", _THEME_NAMES)
    def test_snapshot_without_language(self, theme_name: str, snapshot) -> None:  # type: ignore[no-untyped-def]
        renderer.set_theme(CliTheme.load(theme_name))
        out = _render_to_string(
            lambda: renderer.console.print(renderer._code_block_container("python", "print('hi')\n", show_label=False))
        )
        assert out == snapshot

    def test_label_present_when_requested(self) -> None:
        renderer.set_theme(CliTheme.load("midnight"))
        out = _render_to_string(
            lambda: renderer.console.print(renderer._code_block_container("python", "print('hi')\n", show_label=True))
        )
        assert "python" in out

    def test_label_absent_when_suppressed(self) -> None:
        renderer.set_theme(CliTheme.load("midnight"))
        out = _render_to_string(
            lambda: renderer.console.print(renderer._code_block_container("python", "print('hi')\n", show_label=False))
        )
        # The label line (with the "python" token prefix) must not appear
        assert not any(line.strip().startswith("python") for line in out.splitlines())


# ---------------------------------------------------------------------------
# NO_COLOR degrades gracefully
# ---------------------------------------------------------------------------


class TestNoColorDegradation:
    def test_user_message_has_no_ansi_under_no_color(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("NO_COLOR", "1")
        renderer.set_theme(CliTheme.load("midnight"))

        buf = io.StringIO()
        capture = Console(file=buf, force_terminal=False, no_color=True, width=80)
        original = renderer.console
        original_stdout = renderer._stdout_console
        renderer.console = capture
        renderer._stdout_console = capture
        try:
            renderer.render_user_message("hello")
        finally:
            renderer.console = original
            renderer._stdout_console = original_stdout
        raw = buf.getvalue()
        assert "\u2502" in raw  # gutter still emitted
        assert "\x1b[38;2;" not in raw  # no 24-bit ANSI

    def test_turn_separator_has_no_ansi_under_no_color(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("NO_COLOR", "1")
        renderer.set_theme(CliTheme.load("midnight"))
        buf = io.StringIO()
        capture = Console(file=buf, force_terminal=False, no_color=True, width=80)
        original = renderer.console
        original_stdout = renderer._stdout_console
        renderer.console = capture
        renderer._stdout_console = capture
        try:
            renderer.render_turn_separator()
        finally:
            renderer.console = original
            renderer._stdout_console = original_stdout
        raw = buf.getvalue()
        assert "\u2500" in raw
        assert "\x1b[38;2;" not in raw
