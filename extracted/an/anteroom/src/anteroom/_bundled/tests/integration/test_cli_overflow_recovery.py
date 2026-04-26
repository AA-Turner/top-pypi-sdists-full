"""Integration tests for CLI overflow recovery streaming (#1415).

Drives the actual REPL code path with a mocked ``run_agent_loop`` that
yields the staged-recovery notification tokens.  Verifies the REPL
renders them without breaking and continues accepting input after
recovery.
"""

from __future__ import annotations

import asyncio
import sqlite3
from contextlib import contextmanager
from io import StringIO
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from rich.console import Console

from anteroom.config import AIConfig, AppConfig, AppSettings, CliConfig, SafetyConfig
from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.agent_loop import AgentEvent


def _make_db(tmp_path: Any) -> ThreadSafeConnection:
    db_path = str(tmp_path / "test.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


def _make_config(tmp_path: Any) -> AppConfig:
    return AppConfig(
        ai=AIConfig(
            base_url="http://localhost:1/v1",
            api_key="test-key",
            model="test-model",
        ),
        app=AppSettings(data_dir=tmp_path, tls=False),
        safety=SafetyConfig(approval_mode="auto"),
        cli=CliConfig(),
    )


@contextmanager
def _noop_patch_stdout(**kwargs: Any) -> Any:
    yield


async def _run_repl_with_agent_loop_mock(
    commands: list[str],
    config: AppConfig,
    db: ThreadSafeConnection,
    *,
    agent_loop_side_effect: Any,
) -> tuple[str, bool]:
    from anteroom.cli.repl import _run_repl

    buf = StringIO()
    captured_console = Console(file=buf, force_terminal=False, width=120)

    command_iter = iter([*commands, "/exit"])

    async def fake_prompt(*args: Any, **kwargs: Any) -> str:
        await asyncio.sleep(0.05)
        try:
            return next(command_iter)
        except StopIteration:
            raise EOFError()

    mock_ai = MagicMock()
    mock_ai.stream_chat = AsyncMock()
    mock_ai.generate_title = AsyncMock(return_value="test")
    mock_ai.config = MagicMock()
    mock_ai.config.narration_cadence = 0
    mock_tool_executor = AsyncMock()

    mock_session_instance = MagicMock()
    mock_session_instance.prompt_async = fake_prompt
    mock_session_instance.default_buffer = MagicMock()
    mock_session_instance.default_buffer.on_text_changed = MagicMock()

    exited_cleanly = False

    with (
        patch("anteroom.cli.repl.renderer.console", captured_console),
        patch(
            "anteroom.cli.repl.renderer.render_error",
            lambda msg: captured_console.print(f"Error: {msg}"),
        ),
        patch(
            "anteroom.cli.repl.renderer.render_conversation_recap",
            lambda *a, **k: None,
        ),
        patch("anteroom.cli.renderer.use_stdout_console", lambda: None),
        patch("anteroom.cli.repl._patch_stdout", _noop_patch_stdout, create=True),
        patch("prompt_toolkit.patch_stdout.patch_stdout", _noop_patch_stdout),
        patch("prompt_toolkit.PromptSession") as mock_session_cls,
        patch(
            "anteroom.services.agent_loop.run_agent_loop",
            side_effect=agent_loop_side_effect,
        ),
    ):
        mock_session_cls.return_value = mock_session_instance

        try:
            await _run_repl(
                config=config,
                db=db,
                ai_service=mock_ai,
                tool_executor=mock_tool_executor,
                tools_openai=None,
                extra_system_prompt="",
                all_tool_names=[],
                working_dir=str(config.app.data_dir),
            )
            exited_cleanly = True
        except (EOFError, KeyboardInterrupt, SystemExit):
            exited_cleanly = True

    return buf.getvalue(), exited_cleanly


@pytest.mark.asyncio
class TestCliOverflowRecovery:
    """CLI-side integration tests for staged reactive recovery (#1415)."""

    async def test_cli_overflow_recovery_streams_notification(
        self, tmp_path: Any, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """The recovery notification tokens emitted by the staged path are
        streamed to the terminal (stdout) without breaking the REPL.
        """

        async def fake_agent_loop(**kwargs: Any) -> Any:
            # Simulate the exact token event emitted by Strategy 3 in the
            # shared agent loop.
            yield AgentEvent(
                kind="token",
                data={"content": ("\n\n*Context limit reached — dropped older conversation turns, retrying...*\n\n")},
            )
            yield AgentEvent(kind="token", data={"content": "continuing after recovery"})
            yield AgentEvent(kind="done", data={})

        db = _make_db(tmp_path)
        config = _make_config(tmp_path)

        _, exited = await _run_repl_with_agent_loop_mock(
            ["trigger overflow"],
            config,
            db,
            agent_loop_side_effect=fake_agent_loop,
        )

        assert exited, "REPL should continue after recovery notification"
        # Recovery notification surfaces in the rendered terminal output.
        captured = capsys.readouterr()
        combined = captured.out + captured.err
        assert "dropped older conversation turns" in combined or "Context limit" in combined, (
            f"Expected recovery notification in rendered output; got: {combined!r}"
        )

    async def test_cli_overflow_recovery_produces_valid_continuation(self, tmp_path: Any) -> None:
        """After recovery, the next prompt accepts input and streams
        assistant content normally.
        """
        call_count = 0

        async def fake_agent_loop(**kwargs: Any) -> Any:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First turn: recovery path fires then returns content.
                yield AgentEvent(
                    kind="token",
                    data={
                        "content": ("\n\n*Context limit reached — collapsed historical tool results, retrying...*\n\n")
                    },
                )
                yield AgentEvent(kind="token", data={"content": "first turn ok"})
                yield AgentEvent(kind="done", data={})
            else:
                # Second turn: clean stream, no recovery.
                yield AgentEvent(kind="token", data={"content": "second turn ok"})
                yield AgentEvent(kind="done", data={})

        db = _make_db(tmp_path)
        config = _make_config(tmp_path)

        _, exited = await _run_repl_with_agent_loop_mock(
            ["first", "second"],
            config,
            db,
            agent_loop_side_effect=fake_agent_loop,
        )

        assert exited, "REPL must accept input after recovery"
        # Both turns invoked the agent loop cleanly.
        assert call_count >= 2, f"Expected 2+ agent loop invocations, got {call_count}"

    async def test_cli_microcompact_narration_renders(self, tmp_path: Any, capsys: pytest.CaptureFixture[str]) -> None:
        """Proactive microcompact narration token renders in the REPL (#1266)."""

        async def fake_agent_loop(**kwargs: Any) -> Any:
            yield AgentEvent(
                kind="token",
                data={"content": "\n\n*Trimmed oversized tool outputs to stay within context limits...*\n\n"},
            )
            yield AgentEvent(kind="token", data={"content": "continuing after trim"})
            yield AgentEvent(kind="done", data={})

        db = _make_db(tmp_path)
        config = _make_config(tmp_path)

        _, exited = await _run_repl_with_agent_loop_mock(
            ["trigger microcompact"],
            config,
            db,
            agent_loop_side_effect=fake_agent_loop,
        )

        assert exited, "REPL should continue after microcompact notification"
        captured = capsys.readouterr()
        combined = captured.out + captured.err
        assert "Trimmed oversized tool outputs" in combined or "Trimmed" in combined, (
            f"Expected microcompact notification in rendered output; got: {combined!r}"
        )

    async def test_cli_compaction_summary_retry_notification_renders(
        self, tmp_path: Any, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """The shared-loop summary prompt-too-long retry notice reaches the CLI."""

        async def fake_agent_loop(**kwargs: Any) -> Any:
            yield AgentEvent(
                kind="phase",
                data={
                    "phase": "compacting",
                    "reason": "compaction_prompt_too_long",
                    "attempt": 2,
                    "max_attempts": 3,
                    "dropped_messages": 4,
                },
            )
            yield AgentEvent(
                kind="token",
                data={
                    "content": (
                        "\n\n*Compaction summary prompt was too long — dropped older safe turns and retried...*\n\n"
                    )
                },
            )
            yield AgentEvent(kind="token", data={"content": "continuing after summary retry"})
            yield AgentEvent(kind="done", data={})

        db = _make_db(tmp_path)
        config = _make_config(tmp_path)

        _, exited = await _run_repl_with_agent_loop_mock(
            ["trigger summary retry"],
            config,
            db,
            agent_loop_side_effect=fake_agent_loop,
        )

        assert exited
        captured = capsys.readouterr()
        combined = captured.out + captured.err
        assert "Compaction summary prompt was too long" in combined
