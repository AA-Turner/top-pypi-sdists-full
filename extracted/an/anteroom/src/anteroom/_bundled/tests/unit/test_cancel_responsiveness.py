"""Tests for instant cancel responsiveness (#1372)."""

from __future__ import annotations

import asyncio
import re
import threading
from typing import Any
from unittest.mock import MagicMock, patch

import pytest


class TestRouteCancelSignal:
    """Tests for _route_cancel_signal with visual ack and force-cancel."""

    def test_first_cancel_sets_event_and_acks(self) -> None:
        from anteroom.cli.repl import _route_cancel_signal

        agent_busy = asyncio.Event()
        agent_busy.set()
        cancel_event = asyncio.Event()
        cancel_ref: list[asyncio.Event | None] = [cancel_event]
        acked: list[bool] = [False]

        with patch("anteroom.cli.repl.renderer") as mock_renderer:
            result = _route_cancel_signal(agent_busy, cancel_ref, acked)

        assert result is True
        assert cancel_event.is_set()
        assert acked[0] is True
        mock_renderer.stop_thinking_sync.assert_called_once_with(cancel_msg="cancelled")

    def test_double_cancel_sets_force_event(self) -> None:
        from anteroom.cli.repl import _route_cancel_signal

        agent_busy = asyncio.Event()
        agent_busy.set()
        cancel_event = asyncio.Event()
        cancel_event.set()  # already cancelled
        cancel_ref: list[asyncio.Event | None] = [cancel_event]
        force_event = threading.Event()
        force_ref: list[threading.Event | None] = [force_event]

        with patch("anteroom.cli.repl.renderer"):
            result = _route_cancel_signal(agent_busy, cancel_ref, force_cancel_event=force_ref)

        assert result is True
        assert force_event.is_set()

    def test_idle_agent_returns_false(self) -> None:
        from anteroom.cli.repl import _route_cancel_signal

        agent_busy = asyncio.Event()  # not set
        cancel_ref: list[asyncio.Event | None] = [asyncio.Event()]
        acked: list[bool] = [False]

        result = _route_cancel_signal(agent_busy, cancel_ref, acked)

        assert result is False
        assert acked[0] is False

    def test_no_cancel_event_returns_false(self) -> None:
        from anteroom.cli.repl import _route_cancel_signal

        agent_busy = asyncio.Event()
        agent_busy.set()
        cancel_ref: list[asyncio.Event | None] = [None]

        result = _route_cancel_signal(agent_busy, cancel_ref)

        assert result is False


class TestStopThinkingSyncCancelMsg:
    """Tests for stop_thinking_sync cancel message rendering."""

    def test_footer_mode_renders_cancel_to_stdout(self) -> None:
        from anteroom.cli import renderer

        original_footer = renderer._footer_mode
        original_start = renderer._thinking_start
        original_stdout = renderer._stdout
        original_invalidator = renderer._toolbar_invalidator
        try:
            renderer._footer_mode = True
            renderer._thinking_start = 0.0
            mock_stdout = MagicMock()
            renderer._stdout = mock_stdout
            renderer._toolbar_invalidator = MagicMock()

            elapsed = renderer.stop_thinking_sync(cancel_msg="cancelled")

            assert not renderer._footer_mode
            assert elapsed == 0.0
            mock_stdout.write.assert_called()
            written = mock_stdout.write.call_args[0][0]
            assert "cancelled" in written
            assert not re.search(r"\b\d{6,}s\b", written)
            mock_stdout.flush.assert_called()
        finally:
            renderer._footer_mode = original_footer
            renderer._thinking_start = original_start
            renderer._stdout = original_stdout
            renderer._toolbar_invalidator = original_invalidator

    def test_raw_mode_cancel_with_unset_start_does_not_render_uptime(self) -> None:
        from anteroom.cli import renderer

        original_footer = renderer._footer_mode
        original_repl = renderer._repl_mode
        original_start = renderer._thinking_start
        original_stdout = renderer._stdout
        try:
            renderer._footer_mode = False
            renderer._repl_mode = True
            renderer._thinking_start = 0.0
            mock_stdout = MagicMock()
            renderer._stdout = mock_stdout

            elapsed = renderer.stop_thinking_sync(cancel_msg="cancelled")

            assert elapsed == 0.0
            written = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
            assert "cancelled" in written
            assert not re.search(r"\b\d{6,}s\b", written)
        finally:
            renderer._footer_mode = original_footer
            renderer._repl_mode = original_repl
            renderer._thinking_start = original_start
            renderer._stdout = original_stdout

    def test_footer_mode_no_msg_clears_silently(self) -> None:
        from anteroom.cli import renderer

        original_footer = renderer._footer_mode
        original_start = renderer._thinking_start
        original_stdout = renderer._stdout
        original_invalidator = renderer._toolbar_invalidator
        try:
            renderer._footer_mode = True
            renderer._thinking_start = 0.0
            mock_stdout = MagicMock()
            renderer._stdout = mock_stdout
            renderer._toolbar_invalidator = MagicMock()

            renderer.stop_thinking_sync()

            assert not renderer._footer_mode
            # No write when cancel_msg is empty
            mock_stdout.write.assert_not_called()
        finally:
            renderer._footer_mode = original_footer
            renderer._thinking_start = original_start
            renderer._stdout = original_stdout
            renderer._toolbar_invalidator = original_invalidator


class TestTurnWasCancelled:
    """Tests for cancelled turn summary decisions."""

    def test_acknowledged_cancel_counts_even_before_thinking(self) -> None:
        from anteroom.cli.repl import _turn_was_cancelled

        cancel_event = asyncio.Event()
        cancel_event.set()

        assert _turn_was_cancelled(False, cancel_event, [True]) is True

    def test_programmatic_cancel_before_thinking_does_not_count_as_user_cancel(self) -> None:
        from anteroom.cli.repl import _turn_was_cancelled

        cancel_event = asyncio.Event()
        cancel_event.set()

        assert _turn_was_cancelled(False, cancel_event, [False]) is False


class TestBashCancelAwareness:
    """Tests for cancel-aware bash command execution."""

    @pytest.mark.asyncio
    async def test_cancel_event_terminates_process(self) -> None:
        from anteroom.tools.bash import handle

        cancel_event = asyncio.Event()

        # Start a long-running command
        task = asyncio.create_task(handle("sleep 60", timeout=120, _cancel_event=cancel_event))

        # Give it a moment to start, then cancel
        await asyncio.sleep(0.2)
        cancel_event.set()

        result = await asyncio.wait_for(task, timeout=5.0)
        assert result.get("cancelled") is True or result.get("exit_code") == -1

    @pytest.mark.asyncio
    async def test_force_cancel_kills_process_immediately(self) -> None:
        """Double-cancel must kill within 0.5s, not wait for 2s SIGTERM grace."""
        import time

        from anteroom.tools.bash import handle

        cancel_event = asyncio.Event()
        force_event = threading.Event()

        task = asyncio.create_task(
            handle(
                "sleep 60",
                timeout=120,
                _cancel_event=cancel_event,
                _force_cancel_event=force_event,
            )
        )

        await asyncio.sleep(0.2)
        cancel_event.set()
        # Simulate double-cancel arriving 100ms after first cancel
        await asyncio.sleep(0.1)
        force_event.set()

        start = time.monotonic()
        result = await asyncio.wait_for(task, timeout=3.0)
        elapsed = time.monotonic() - start

        assert result.get("cancelled") is True or result.get("exit_code") == -1
        # Must complete well under the 2s SIGTERM grace window
        assert elapsed < 1.0, f"Force-cancel took {elapsed:.1f}s, expected <1s"

    @pytest.mark.asyncio
    async def test_no_cancel_event_works_normally(self) -> None:
        from anteroom.tools.bash import handle

        result = await handle("echo hello", timeout=10)
        assert result["exit_code"] == 0
        assert "hello" in result["stdout"]


class TestExecuteToolTimeout:
    """Tests for reduced cancel timeout in _execute_tool."""

    @pytest.mark.asyncio
    async def test_cancel_cleanup_timeout_is_short(self) -> None:
        """Verify that cancel cleanup doesn't block for 5 seconds."""
        from anteroom.services.agent_loop import _execute_tool

        cancel_event = asyncio.Event()
        call_count = 0

        async def slow_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(60)  # simulate stuck tool
            return {}

        tc = {"function_name": "test_tool", "arguments": {}, "id": "tc1"}

        # Set cancel immediately
        cancel_event.set()
        import time

        start = time.monotonic()
        _tc, result, status = await _execute_tool(tc, slow_tool, cancel_event)
        elapsed = time.monotonic() - start

        assert status == "cancelled"
        # Should complete in under 2 seconds (0.5s timeout + overhead)
        assert elapsed < 2.0, f"Cancel cleanup took {elapsed:.1f}s, expected <2s"
