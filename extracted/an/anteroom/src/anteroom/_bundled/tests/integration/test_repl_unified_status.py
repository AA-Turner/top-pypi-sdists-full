"""Integration tests for the unified live-turn status surface (#1428, #1512).

These tests drive the renderer state machine directly (no PTY required) to
verify invariants that span renderer + REPL wiring:

- In footer mode (the REPL's default), a tool call does not spawn a second
  ticker task alongside the unified thinking ticker.
- ``render_turn_summary()`` prints exactly once per turn end.
- The ``accepted`` phase bypasses the 2s reveal delay so the user sees an
  immediate ack of their prompt before the first AI phase event arrives.
- Footer mode is only entered when the prompt_toolkit toolbar surface is live;
  when the app is not running the renderer falls back to raw stdout (#1512).
"""

from __future__ import annotations

import asyncio
import io
from typing import Any
from unittest.mock import MagicMock

import pytest
from rich.console import Console

import anteroom.cli.renderer as r
from anteroom.cli.renderer import (
    _reset_tool_phase,
    enter_tool_phase,
    exit_tool_phase,
    render_debug_summary,
    render_turn_summary,
    start_tool_ticker,
    stop_tool_ticker_sync,
)


@pytest.mark.integration
class TestUnifiedTurnStatus:
    """Integration tests for the unified live-turn status surface (#1428)."""

    def setup_method(self) -> None:
        self._orig_footer = r._footer_mode
        self._orig_repl = r._repl_mode
        self._orig_stdout = r._stdout
        self._orig_inv = r._toolbar_invalidator
        self._orig_active = r._toolbar_is_active
        self._orig_prompt_active = r._prompt_is_active
        self._orig_console = r.console
        self._orig_tool_start = r._tool_start
        _reset_tool_phase()
        r._tool_ticker_summary = ""
        r._tool_line_visible = False

    def teardown_method(self) -> None:
        stop_tool_ticker_sync()
        r._footer_mode = self._orig_footer
        r._repl_mode = self._orig_repl
        r._stdout = self._orig_stdout
        r._toolbar_invalidator = self._orig_inv
        r._toolbar_is_active = self._orig_active
        r._prompt_is_active = self._orig_prompt_active
        r.console = self._orig_console
        r._tool_start = self._orig_tool_start
        r._thinking_ticker_task = None
        r._tool_line_visible = False
        _reset_tool_phase()

    def test_unified_status_no_duplicate_surface(self) -> None:
        """Running a (mocked) tool call in footer mode must not spawn a
        parallel ``_tool_ticker_task`` alongside ``_thinking_ticker_task``.

        Exercises the chunk-2 consolidation: ``start_tool_ticker()`` is a
        no-op when ``_footer_mode`` is active.
        """
        r._repl_mode = True
        r._stdout = io.StringIO()
        r._footer_mode = True
        r._toolbar_invalidator = lambda: None

        # Simulate a tool_call_start event landing in the event loop.
        enter_tool_phase("read_file", {"path": "src/foo.py"})
        start_tool_ticker("Reading src/foo.py")

        # Invariant: only the thinking ticker can own the surface in footer mode.
        assert r._tool_ticker_task is None
        assert r._tool_ticker_summary == ""

        # Tool finishes — state must be pristine for the next tool/turn.
        exit_tool_phase("read_file")
        assert r._tool_ticker_summary == ""

    @pytest.mark.asyncio
    async def test_tool_only_status_uses_toolbar_when_prompt_is_active(self) -> None:
        """After thinking stops, tool-only ticker status must not raw-repaint over the prompt."""
        session = _make_mock_session(is_running=True)
        invalidator_calls: list[int] = []
        buf = io.StringIO()

        r._repl_mode = True
        r._footer_mode = False
        r._stdout = buf
        r._toolbar_invalidator = lambda: invalidator_calls.append(1)
        r._toolbar_is_active = lambda: bool(session.app and session.app.is_running)
        r._prompt_is_active = lambda: True
        r._tool_start = 1.0

        try:
            start_tool_ticker("Finding **/config.yaml")
            await asyncio.sleep(0.6)

            assert r._tool_ticker_task is not None
            assert invalidator_calls, "tool-only status should repaint through prompt_toolkit"
            assert "Finding **/config.yaml" not in buf.getvalue()
            status = r.get_busy_status()
            assert status is not None
            assert status.tool_label == "Finding **/config.yaml"

            invalidations_before_stop = len(invalidator_calls)
            stop_tool_ticker_sync()
            assert r._tool_ticker_summary == ""
            assert len(invalidator_calls) > invalidations_before_stop
        finally:
            stop_tool_ticker_sync()

    @pytest.mark.asyncio
    async def test_tool_only_status_keeps_raw_fallback_when_prompt_inactive(self) -> None:
        """#1512 fallback still applies when no prompt_toolkit input surface can render."""
        session = _make_mock_session(is_running=False)
        invalidator_calls: list[int] = []
        buf = io.StringIO()

        r._repl_mode = True
        r._footer_mode = False
        r._stdout = buf
        r._toolbar_invalidator = lambda: invalidator_calls.append(1)
        r._toolbar_is_active = lambda: bool(session.app and session.app.is_running)
        r._tool_start = 1.0

        try:
            start_tool_ticker("Finding **/config.yaml")
            await asyncio.sleep(0.6)

            assert invalidator_calls == []
            assert "Finding **/config.yaml" in buf.getvalue()
        finally:
            stop_tool_ticker_sync()

    def test_turn_summary_rendered_once(self) -> None:
        """``render_turn_summary()`` called once per turn prints exactly one line.

        Guards against accidentally double-wiring the summary hook into both
        the exec and subagent event loops for the same turn.
        """
        buf = io.StringIO()
        r.console = Console(file=buf, force_terminal=False, width=120, highlight=False)

        render_turn_summary(elapsed=2.0, tools=[{"tool_name": "bash"}], cancelled=False, error=None)

        output = buf.getvalue()
        # Exactly one "done" token; catches a stray double-print.
        assert output.count("done") == 1
        assert "2.0s" in output

    def test_debug_summary_renders_redacted_metadata(self) -> None:
        """Debug diagnostics print structured metadata without raw output."""
        buf = io.StringIO()
        r.console = Console(file=buf, force_terminal=False, width=120, highlight=False)

        render_debug_summary(
            {
                "total_duration_seconds": 1.25,
                "stop_reason": "completed",
                "final_phase": "streaming",
                "model": {"provider": "openai", "name": "gpt-test"},
                "usage": {"total_tokens": 42},
                "counters": {"tokens": 3, "token_chars": 99},
                "retries": [{"attempt": 2}],
                "tools": [{"name": "bash", "status": "success", "duration_seconds": 0.3}],
                "runtime_events": [{"kind": "queued_message"}],
            }
        )

        output = buf.getvalue()
        assert "debug" in output
        assert "completed" in output
        assert "openai / gpt-test" in output
        assert "bash:success" in output

    @pytest.mark.asyncio
    async def test_accepted_phase_shows_before_first_ai_event(self) -> None:
        """Setting the ``accepted`` phase before ``start_thinking()`` causes
        the thinking text to appear immediately (bypassing the 2s reveal
        delay), closing the idle gap between prompt submit and the first
        AI event.
        """
        # No _thinking_start yet — simulate the pre-submit state.
        r._thinking_phase = "accepted"
        # With elapsed=0.05, well below _REPL_THINKING_REVEAL_DELAY (2.0s),
        # the build helper should still emit the label because of the
        # accepted-phase bypass added in chunk 1.
        text = r._build_thinking_text(0.05)
        assert "Working..." in text

        # Switching to a downstream phase (e.g. connecting) once the AI
        # service emits its first phase event: calm window re-applies
        # (elapsed still < 2s so no label yet).
        r._thinking_phase = "connecting"
        text2 = r._build_thinking_text(0.05)
        # This returns "" because connecting is subject to the calm window;
        # and that is fine — accepted has already bridged the gap.
        assert text2 == ""
        # Clean up module state
        r._thinking_phase = ""
        # Let the event loop settle
        await asyncio.sleep(0)


def _make_mock_session(*, is_running: bool) -> Any:
    """Return a minimal mock PromptSession whose app.is_running matches the given value."""
    session = MagicMock()
    session.app.is_running = is_running
    return session


@pytest.mark.integration
class TestFooterModeAvailabilityWiring:
    """Integration tests for the REPL-level toolbar-availability probe (#1512).

    Simulates the actual wiring that ``_run_repl()`` performs:

        renderer._toolbar_is_active = lambda: bool(session.app and session.app.is_running)

    and verifies the complete turn-start lifecycle for both the active-toolbar
    (footer mode) and inactive-toolbar (raw stdout) paths.  The single-surface
    invariant — at most one busy surface visible per turn — is asserted for each
    case.
    """

    def setup_method(self) -> None:
        self._orig_repl = r._repl_mode
        self._orig_footer = r._footer_mode
        self._orig_inv = r._toolbar_invalidator
        self._orig_active = r._toolbar_is_active
        self._orig_prompt_active = r._prompt_is_active
        self._orig_stdout = r._stdout
        self._orig_plan_visible = r._plan_visible
        self._orig_plan_steps = r._plan_steps
        self._orig_spinner = r._spinner
        self._orig_task = r._thinking_ticker_task
        r._thinking_ticker_task = None
        r._spinner = None
        r._plan_visible = False
        r._plan_steps = []
        r._repl_mode = True

    def teardown_method(self) -> None:
        r.stop_thinking_sync()
        r._repl_mode = self._orig_repl
        r._footer_mode = self._orig_footer
        r._toolbar_invalidator = self._orig_inv
        r._toolbar_is_active = self._orig_active
        r._prompt_is_active = self._orig_prompt_active
        r._stdout = self._orig_stdout
        r._plan_visible = self._orig_plan_visible
        r._plan_steps = self._orig_plan_steps
        r._spinner = self._orig_spinner
        r._thinking_ticker_task = self._orig_task

    def test_active_toolbar_uses_footer_mode_not_stdout(self) -> None:
        """When session.app.is_running is True, start_thinking() enters footer
        mode and calls the invalidator — it must NOT write to stdout.

        This is the shipped REPL path: the toolbar surface is live so all busy
        state updates go through prompt_toolkit invalidation, not raw ANSI.
        """
        session = _make_mock_session(is_running=True)
        invalidator_calls: list[int] = []
        buf = io.StringIO()

        r._toolbar_invalidator = lambda: invalidator_calls.append(1)
        r._toolbar_is_active = lambda: bool(session.app and session.app.is_running)
        r._stdout = buf

        r.start_thinking(newline=True)

        assert r._footer_mode is True
        assert invalidator_calls, "invalidator must be called to update the toolbar"
        assert buf.getvalue() == "", "stdout must be silent when toolbar surface is live"

    def test_inactive_toolbar_uses_raw_stdout_not_footer_mode(self) -> None:
        """When session.app.is_running is False, start_thinking() stays on the
        raw stdout path — it must NOT enter footer mode or call the invalidator.

        This is the regression case from #1512: the prompt session exists and
        has an invalidator, but the app is not running during an active turn.
        """
        session = _make_mock_session(is_running=False)
        invalidator_calls: list[int] = []
        buf = io.StringIO()

        r._toolbar_invalidator = lambda: invalidator_calls.append(1)
        r._toolbar_is_active = lambda: bool(session.app and session.app.is_running)
        r._stdout = buf

        r.start_thinking(newline=True)

        assert r._footer_mode is False, "footer mode must not be entered when app is not running"
        assert not invalidator_calls, "invalidator must not be called when toolbar surface is inactive"
        assert len(buf.getvalue()) > 0, "raw stdout path must produce visible output"

    def test_single_busy_surface_active_toolbar(self) -> None:
        """Active-toolbar path: tool events do not spawn a second ticker surface.

        Combines the #1428 no-duplicate-surface invariant with the #1512
        active-probe wiring.  Even when a tool call lands during a turn that
        started in footer mode, start_tool_ticker() remains a no-op.
        """
        session = _make_mock_session(is_running=True)
        r._toolbar_invalidator = lambda: None
        r._toolbar_is_active = lambda: bool(session.app and session.app.is_running)
        r._stdout = io.StringIO()

        r.start_thinking()
        assert r._footer_mode is True

        enter_tool_phase("bash", {"command": "ls"})
        start_tool_ticker("Running ls")

        assert r._tool_ticker_task is None
        assert r._tool_ticker_summary == ""

        exit_tool_phase("bash")

    def test_single_busy_surface_inactive_toolbar(self) -> None:
        """Inactive-toolbar path: tool events also do not spawn a second ticker.

        When the fallback raw-line path is used (_footer_mode=False), the same
        no-duplicate-surface invariant must hold: start_tool_ticker() is a
        no-op because the thinking ticker owns the raw surface.
        """
        session = _make_mock_session(is_running=False)
        r._toolbar_invalidator = lambda: None
        r._toolbar_is_active = lambda: bool(session.app and session.app.is_running)
        r._stdout = io.StringIO()

        r.start_thinking()
        assert r._footer_mode is False

        enter_tool_phase("read_file", {"path": "foo.py"})
        start_tool_ticker("Reading foo.py")

        assert r._tool_ticker_task is None

        exit_tool_phase("read_file")

    def test_subsequent_turn_re_evaluates_toolbar_availability(self) -> None:
        """The active probe is re-evaluated at every turn start, not cached.

        Turn 1: app not running → raw path.
        Turn 2: app running → footer mode.

        This verifies that stop_thinking() + start_thinking() correctly
        transitions between surfaces when the toolbar becomes available.
        """
        session = _make_mock_session(is_running=False)
        invalidator_calls: list[int] = []
        buf = io.StringIO()

        r._toolbar_invalidator = lambda: invalidator_calls.append(1)
        r._toolbar_is_active = lambda: bool(session.app and session.app.is_running)
        r._stdout = buf

        # Turn 1: toolbar inactive → raw path.
        r.start_thinking(newline=True)
        assert r._footer_mode is False
        r.stop_thinking_sync()
        assert not invalidator_calls

        # Simulate app becoming active (user waited at prompt, toolbar is live).
        session.app.is_running = True
        buf.truncate(0)
        buf.seek(0)

        # Turn 2: toolbar now active → footer mode.
        r.start_thinking()
        assert r._footer_mode is True
        assert invalidator_calls, "invalidator must fire once toolbar is active"
        assert buf.getvalue() == "", "no raw stdout in footer mode"
