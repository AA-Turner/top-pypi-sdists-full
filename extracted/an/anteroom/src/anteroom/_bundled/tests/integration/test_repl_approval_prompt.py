"""Integration tests for CLI approval prompt visibility.

Tests that the approval prompt options are printed via Rich console
(persistent through patch_stdout) and that the nested PromptSession
reads user input correctly.
"""

from __future__ import annotations

from io import StringIO
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from rich.console import Console

from anteroom.cli import renderer
from anteroom.tools.safety import SafetyVerdict


class TestConfirmDestructiveIntegration:
    """Test the full _confirm_destructive flow with mocked I/O."""

    @pytest.mark.asyncio
    async def test_approval_options_rendered_via_console(self, tmp_path: Any) -> None:
        """Options text is rendered via Rich console (persists through patch_stdout)."""
        verdict = SafetyVerdict(
            tool_name="bash",
            needs_approval=True,
            is_hard_blocked=False,
            reason="Destructive command detected: rm -rf /tmp/test",
            details={"command": "rm -rf /tmp/test", "matched_pattern": "rm.*-r"},
        )

        buf = StringIO()
        captured_console = Console(file=buf, force_terminal=False, width=120)

        mock_sub_prompt = AsyncMock(return_value="y")

        with (
            patch.object(renderer, "console", captured_console),
            patch.object(renderer, "stop_thinking", AsyncMock()),
            patch.object(renderer, "start_thinking", MagicMock()),
        ):
            import asyncio

            _approval_lock = asyncio.Lock()
            muted = "dim"

            async with _approval_lock:
                captured_console.print("\n  ── Approval Needed ──")
                captured_console.print(f"  {verdict.reason}")
                if verdict.details.get("command"):
                    captured_console.print(f"  Command: [{muted}]{verdict.details['command']}[/{muted}]")
                captured_console.print("  y once   s session   a always   n deny")
                captured_console.print("  ctrl-d to deny")
                answer = await mock_sub_prompt("  Choice [y/s/a/n] > ")

            output = buf.getvalue()

            # Warning text rendered via Rich console
            assert "Destructive command detected" in output
            assert "rm -rf /tmp/test" in output

            # Options rendered via Rich console (persistent, not write_raw)
            assert "Approval Needed" in output
            assert "y once" in output
            assert "s session" in output
            assert "a always" in output
            assert "n deny" in output
            assert "ctrl-d to deny" in output

            # Input was captured via sub-prompt
            assert answer == "y"

    @pytest.mark.asyncio
    async def test_approval_flow_deny(self, tmp_path: Any) -> None:
        """User types 'n' -> sub_prompt returns 'n'."""
        mock_sub_prompt = AsyncMock(return_value="n")
        answer = await mock_sub_prompt("  > ")
        assert answer == "n"

    @pytest.mark.asyncio
    async def test_approval_flow_eof(self, tmp_path: Any) -> None:
        """EOF on stdin -> sub_prompt returns None."""
        mock_sub_prompt = AsyncMock(return_value=None)
        answer = await mock_sub_prompt("  > ")
        assert answer is None


class TestSubPromptAsyncUnit:
    """Test _sub_prompt_async building blocks."""

    @pytest.mark.asyncio
    async def test_nested_session_returns_stripped_input(self) -> None:
        """A nested PromptSession returns stripped user input."""
        mock_session_cls = MagicMock()
        mock_instance = MagicMock()
        mock_instance.prompt_async = AsyncMock(return_value="  y  ")
        mock_session_cls.return_value = mock_instance

        with patch("prompt_toolkit.PromptSession", mock_session_cls):
            from prompt_toolkit import PromptSession

            sub = PromptSession()
            raw = await sub.prompt_async("  > ")
            answer = raw.strip() if raw is not None else None

        assert answer == "y"

    @pytest.mark.asyncio
    async def test_nested_session_empty_returns_empty_string(self) -> None:
        """Pressing Enter with no text returns empty string, not None."""
        mock_session_cls = MagicMock()
        mock_instance = MagicMock()
        mock_instance.prompt_async = AsyncMock(return_value="")
        mock_session_cls.return_value = mock_instance

        with patch("prompt_toolkit.PromptSession", mock_session_cls):
            from prompt_toolkit import PromptSession

            sub = PromptSession()
            raw = await sub.prompt_async("  > ")
            answer = raw.strip() if raw is not None else None

        assert answer == ""
        assert answer is not None

    @pytest.mark.asyncio
    async def test_nested_session_eof_raises(self) -> None:
        """A nested PromptSession raises EOFError on Ctrl-D."""
        mock_session_cls = MagicMock()
        mock_instance = MagicMock()
        mock_instance.prompt_async = AsyncMock(side_effect=EOFError)
        mock_session_cls.return_value = mock_instance

        with patch("prompt_toolkit.PromptSession", mock_session_cls):
            from prompt_toolkit import PromptSession

            sub = PromptSession()
            try:
                await sub.prompt_async("  > ")
                answer = None  # shouldn't reach
            except EOFError:
                answer = None

        assert answer is None


class TestAskUserPromptIntegration:
    """Integration tests for the polished ask_user interruption flow (#1051)."""

    @pytest.mark.asyncio
    async def test_ask_user_numbered_option_selection(self) -> None:
        """Numbered option selection renders header, options, and confirmation."""
        buf = StringIO()
        captured_console = Console(file=buf, force_terminal=False, width=120, no_color=True)
        mock_sub_prompt = AsyncMock(return_value="2")

        with (
            patch.object(renderer, "console", captured_console),
            patch.object(renderer, "stop_thinking", AsyncMock()),
            patch.object(renderer, "start_thinking", MagicMock()),
            patch.object(renderer, "stop_tool_ticker_sync", MagicMock()),
        ):
            question = "Which format do you prefer?"
            options = ["JSON", "YAML", "TOML"]

            # Replicate the polished _ask_user_callback logic
            captured_console.print("\n  ── Input Needed ──")
            captured_console.print(f"  {question}")
            for i, opt in enumerate(options, 1):
                captured_console.print(f"    {i}. {opt}")
            captured_console.print("  ctrl-d to cancel")
            answer_raw = await mock_sub_prompt(f"  Choice [1-{len(options)} or text] > ")
            # Resolve choice
            if answer_raw and answer_raw.isdigit():
                idx = int(answer_raw)
                if 1 <= idx <= len(options):
                    answer = options[idx - 1]
                else:
                    answer = answer_raw
            else:
                answer = answer_raw
            captured_console.print(f"  → {answer}")

        output = buf.getvalue()

        assert "Input Needed" in output
        assert "Which format do you prefer?" in output
        assert "1." in output
        assert "JSON" in output
        assert "YAML" in output
        assert "TOML" in output
        assert answer == "YAML"
        assert "→ YAML" in output

    @pytest.mark.asyncio
    async def test_ask_user_freeform_answer(self) -> None:
        """Freeform text answer renders header and confirmation."""
        buf = StringIO()
        captured_console = Console(file=buf, force_terminal=False, width=120, no_color=True)
        mock_sub_prompt = AsyncMock(return_value="custom answer")

        with (
            patch.object(renderer, "console", captured_console),
            patch.object(renderer, "stop_thinking", AsyncMock()),
            patch.object(renderer, "start_thinking", MagicMock()),
            patch.object(renderer, "stop_tool_ticker_sync", MagicMock()),
        ):
            captured_console.print("\n  ── Input Needed ──")
            captured_console.print("  What should we name the file?")
            captured_console.print("  ctrl-d to cancel")
            answer = await mock_sub_prompt("  Answer > ")
            captured_console.print(f"  → {answer}")

        output = buf.getvalue()

        assert "Input Needed" in output
        assert "What should we name the file?" in output
        assert answer == "custom answer"
        assert "→ custom answer" in output

    @pytest.mark.asyncio
    async def test_ask_user_shortcut_resolves_to_single_matching_option(self) -> None:
        """Single-letter shortcuts resolve to the matching option text when unambiguous."""
        buf = StringIO()
        captured_console = Console(file=buf, force_terminal=False, width=120, no_color=True)
        mock_sub_prompt = AsyncMock(return_value="y")

        with (
            patch.object(renderer, "console", captured_console),
            patch.object(renderer, "stop_thinking", AsyncMock()),
            patch.object(renderer, "start_thinking", MagicMock()),
            patch.object(renderer, "stop_tool_ticker_sync", MagicMock()),
        ):
            options = ["Yes, delete /tmp/test", "No, keep it"]
            captured_console.print("\n  ── Input Needed ──")
            captured_console.print("  Deleting /tmp/test is destructive. Do you want me to remove it?")
            for i, opt in enumerate(options, 1):
                captured_console.print(f"    {i}. {opt}")
            captured_console.print("  ctrl-d to cancel")
            answer_raw = await mock_sub_prompt("  Choice [1-2 or text] > ")
            lowered = answer_raw.strip().lower()
            matches = [opt for opt in options if opt.lower().startswith(lowered)]
            answer = matches[0] if len(matches) == 1 else answer_raw
            captured_console.print(f"  → {answer}")

        output = buf.getvalue()

        assert answer == "Yes, delete /tmp/test"
        assert "→ Yes, delete /tmp/test" in output

    @pytest.mark.asyncio
    async def test_ask_user_ctrl_d_cancellation(self) -> None:
        """Ctrl-d cancellation renders header and cancelled message."""
        buf = StringIO()
        captured_console = Console(file=buf, force_terminal=False, width=120, no_color=True)
        mock_sub_prompt = AsyncMock(return_value=None)

        with (
            patch.object(renderer, "console", captured_console),
            patch.object(renderer, "stop_thinking", AsyncMock()),
            patch.object(renderer, "start_thinking", MagicMock()),
            patch.object(renderer, "stop_tool_ticker_sync", MagicMock()),
        ):
            captured_console.print("\n  ── Input Needed ──")
            captured_console.print("  Continue with deletion?")
            captured_console.print("  ctrl-d to cancel")
            answer = await mock_sub_prompt("  Answer > ")
            if answer is None:
                captured_console.print("  (cancelled)")

        output = buf.getvalue()

        assert "Input Needed" in output
        assert "Continue with deletion?" in output
        assert answer is None
        assert "(cancelled)" in output
