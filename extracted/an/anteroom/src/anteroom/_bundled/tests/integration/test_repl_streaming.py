"""Integration tests: live markdown streaming renders end-to-end (#1365).

Drives the renderer through the same token → tool_call_start → token →
response_end sequence that the REPL emits for an assistant turn, and asserts
that the Live region produces visible output, tears down cleanly before tool
output, and finalizes through ``render_assistant_prose``.

Per ``.claude/rules/ux-testing.md``, ``cli/renderer.py`` and ``cli/repl.py``
changes require CLI integration coverage. We exercise the renderer-level
contract (rather than spinning up the full prompt_toolkit REPL) because the
streaming wiring lives entirely in the renderer module and the repl.py
caller is a pure pass-through.
"""

from __future__ import annotations

import io
import re
import time
from unittest.mock import patch

import pytest
from rich.console import Console

from anteroom.cli import renderer
from anteroom.cli.themes import CliTheme

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


@pytest.fixture(autouse=True)
def _clear_no_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)


@pytest.fixture(autouse=True)
def _restore_midnight_theme() -> None:  # type: ignore[return]
    yield
    renderer.set_theme(CliTheme.load("midnight"))
    renderer.reset_streaming()


@pytest.fixture(autouse=True)
def _reset_renderer_state() -> None:  # type: ignore[return]
    """Clear renderer module-level state between tests."""
    renderer._streaming_buffer.clear()
    renderer._tool_batch_active = False
    yield
    renderer._streaming_buffer.clear()
    renderer._tool_batch_active = False


def _install_capture_console() -> tuple[Console, io.StringIO]:
    buf = io.StringIO()
    capture = Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=80,
        highlight=False,
    )
    renderer.console = capture
    renderer._stdout_console = capture
    return capture, buf


class _PersistentFrameLive:
    """Fake Live that leaves the final frame visible when transient=False.

    This models the duplication boundary behind #1466: if the live region's
    last frame persists and the renderer also prints a permanent static copy,
    users see duplicate assistant prose.
    """

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


class TestStreamingTurnIntegration:
    """End-to-end: live markdown streaming across a full assistant turn."""

    def test_basic_stream_then_end_emits_formatted_output(self) -> None:
        capture, buf = _install_capture_console()
        renderer.set_theme(CliTheme.load("midnight"))
        renderer.configure_streaming(enabled=True, refresh_hz=60.0)

        # Simulate the REPL's token loop.
        for chunk in [
            "Here is ",
            "some **bold** text ",
            "and `inline` code.",
        ]:
            renderer.render_token(chunk)

        # End of turn — streaming finalizes.
        renderer.render_response_end()

        output = buf.getvalue()
        assert "bold" in output
        assert "inline" in output

    def test_tool_call_mid_stream_flushes_cleanly(self) -> None:
        capture, buf = _install_capture_console()
        renderer.set_theme(CliTheme.load("midnight"))
        renderer.configure_streaming(enabled=True, refresh_hz=60.0)

        # Assistant says a narration line, then a tool call interrupts.
        renderer.render_token("Let me check ")
        renderer.render_token("the **auth** module.")
        # Mid-turn flush: REPL calls this right before render_tool_call_start.
        renderer.flush_buffered_text()
        # After flush_to_static, buffer is cleared and live region torn down.
        # A fresh segment starts on the next token.
        renderer.render_token("Done. ")
        renderer.render_token("Results above.")
        renderer.render_response_end()

        output = buf.getvalue()
        assert "auth" in output
        assert "Results above" in output

    def test_persistent_live_frame_flushes_mid_turn_reply_once(self) -> None:
        capture, buf = _install_capture_console()
        renderer.set_theme(CliTheme.load("midnight"))
        with patch("anteroom.cli.streaming.Live", _PersistentFrameLive):
            renderer.configure_streaming(enabled=True, refresh_hz=60.0)
            renderer.render_token("Let me check ")
            renderer.render_token("the **auth** module.")
            renderer.flush_buffered_text()

        output = _ANSI_RE.sub("", buf.getvalue())
        assert output.count("Let me check the auth module.") == 1

    def test_live_frame_persistence_still_yields_one_visible_reply(self) -> None:
        capture, buf = _install_capture_console()
        renderer.set_theme(CliTheme.load("midnight"))
        with patch("anteroom.cli.streaming.Live", _PersistentFrameLive):
            renderer.configure_streaming(enabled=True, refresh_hz=60.0)
            for chunk in [
                "Hello! I'm ",
                "Anteroom, your ",
                "AI coding assistant.",
            ]:
                renderer.render_token(chunk)
                time.sleep(0.02)
            renderer.render_response_end()

        output = buf.getvalue()
        assert output.count("Hello! I'm Anteroom, your AI coding assistant.") == 1

    def test_narration_before_tool_does_not_duplicate_as_prose(self) -> None:
        """Regression for #1471: narration shown on the Thinking/status line
        must not be re-emitted as permanent prose when a tool call follows.

        With the real Rich ``Live`` region (transient=True), the first
        painted frame writes the narration into the captured stream; Live's
        visual teardown relies on cursor movement to erase those characters
        from the terminal view, but the characters remain in the captured
        output. ``flush_buffered_text()`` then emits a permanent static
        print of the same narration. Users who can see the streamed frame
        (either through a very fast paint, an interfering direct stdout
        write, or a terminal that doesn't act on cursor-hide/rewrite)
        observe the narration twice: once as transient text still visible
        on the line that now says "Thinking... Ns", and again as permanent
        prose below the tool output.

        The fix must ensure the narration appears AT MOST ONCE in the
        captured output across the full turn, regardless of how the Live
        region's transient cleanup interacts with out-of-band writes.
        """
        # Do NOT patch Live here — we want the real Rich Live region so the
        # failure mode matches production (#1471).
        ansi_esc_re = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]")
        capture, buf = _install_capture_console()
        renderer.set_theme(CliTheme.load("midnight"))
        narration = "I'm checking the config file layout first."
        renderer.configure_streaming(enabled=True, refresh_hz=60.0)
        # Fake agent loop: thinking -> token(narration) -> tool_call_start
        # -> tool_call_end -> done. We call the renderer entry points in
        # the same order the REPL dispatcher calls them (repl.py ~7740).
        renderer.render_token(narration)
        # tool_call_start → render_tool_call_start → flush_buffered_text.
        renderer.flush_buffered_text()
        # tool_call_end: no further prose.
        # done: final render (buffer now empty).
        renderer.render_response_end()

        # Strip ANSI control sequences so a Live paint + a later static
        # print of the same narration both count as occurrences (Live's
        # "transient" cleanup is visual-only; the raw text stays in the
        # captured stream).
        plain = ansi_esc_re.sub("", buf.getvalue())
        assert plain.count(narration) == 1, f"narration printed {plain.count(narration)} times; output was:\n{plain!r}"

    def test_disabled_streaming_preserves_legacy_output(self) -> None:
        capture, buf = _install_capture_console()
        renderer.set_theme(CliTheme.load("midnight"))
        # Streaming explicitly disabled: legacy buffer-then-render path runs.
        renderer.configure_streaming(enabled=False, refresh_hz=20.0)

        for chunk in ["This is ", "**bold** only."]:
            renderer.render_token(chunk)
        renderer.render_response_end()

        output = buf.getvalue()
        assert "bold" in output

    def test_disabled_streaming_does_not_flush_mid_turn_narration(self) -> None:
        capture, buf = _install_capture_console()
        renderer.set_theme(CliTheme.load("midnight"))
        renderer.configure_streaming(enabled=False, refresh_hz=20.0)

        renderer.render_token("I'm checking the config first.")
        renderer.flush_buffered_text()

        assert "checking the config" not in buf.getvalue()

        renderer.render_response_end()

        assert "checking the config" in buf.getvalue()

    def test_exec_mode_without_opt_in_disables_live(self) -> None:
        capture, buf = _install_capture_console()
        renderer.set_theme(CliTheme.load("midnight"))
        renderer.configure_streaming(
            enabled=True,
            refresh_hz=20.0,
            exec_mode=True,
            live_in_exec_mode=False,
        )

        for chunk in ["some ", "**text**"]:
            renderer.render_token(chunk)
        renderer.render_response_end()

        # Live is unavailable; legacy final-render path still emits output.
        output = buf.getvalue()
        assert "text" in output
        # And the streaming renderer reports unavailable.
        assert renderer._streaming_renderer is not None
        assert not renderer._streaming_renderer.live_available()

    def test_exec_mode_opt_in_enables_live(self) -> None:
        capture, buf = _install_capture_console()
        renderer.set_theme(CliTheme.load("midnight"))
        renderer.configure_streaming(
            enabled=True,
            refresh_hz=60.0,
            exec_mode=True,
            live_in_exec_mode=True,
        )

        assert renderer._streaming_renderer is not None
        assert renderer._streaming_renderer.live_available()

        for chunk in ["echo ", "**ok**"]:
            renderer.render_token(chunk)
        renderer.render_response_end()

        output = buf.getvalue()
        assert "ok" in output

    def test_reset_streaming_tears_down(self) -> None:
        capture, buf = _install_capture_console()
        renderer.configure_streaming(enabled=True, refresh_hz=60.0)
        assert renderer._streaming_renderer is not None
        renderer.reset_streaming()
        assert renderer._streaming_renderer is None

    def test_whitespace_only_stream_is_silent(self) -> None:
        capture, buf = _install_capture_console()
        renderer.set_theme(CliTheme.load("midnight"))
        renderer.configure_streaming(enabled=True, refresh_hz=60.0)

        renderer.render_token("   ")
        renderer.render_token("\n\n")
        renderer.render_response_end()

        # No visible content should have been printed.
        stripped = buf.getvalue().strip()
        # Allow cursor hide/show ANSI if Live opened, but no content:
        # assert there is no actual text content in the output.
        assert all(c in "\x1b[]?25lhm0;" for c in stripped) or stripped == ""
