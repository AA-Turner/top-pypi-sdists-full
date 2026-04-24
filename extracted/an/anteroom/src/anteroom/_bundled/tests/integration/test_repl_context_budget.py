"""CLI integration tests for visible context-budget accounting (#1539).

Drives the actual REPL code path with a mocked ``run_agent_loop`` and a
patched fixed-overhead estimate so the end-of-turn footer can be asserted
against the same full-request accounting basis used by the warn and
auto-compact gate.
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

from anteroom.cli.repl import _FixedRequestOverhead
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


async def _run_repl_with_context_budget(
    commands: list[str],
    config: AppConfig,
    db: ThreadSafeConnection,
    *,
    fixed_overhead: _FixedRequestOverhead,
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

    async def fake_agent_loop(**kwargs: Any) -> Any:
        yield AgentEvent(kind="token", data={"content": "ok"})
        yield AgentEvent(kind="done", data={})

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
        patch("anteroom.cli.repl.renderer.render_error", lambda msg: captured_console.print(f"Error: {msg}")),
        patch("anteroom.cli.repl.renderer.render_conversation_recap", lambda *a, **k: None),
        patch("anteroom.cli.renderer.use_stdout_console", lambda: None),
        patch("anteroom.cli.repl._patch_stdout", _noop_patch_stdout, create=True),
        patch("prompt_toolkit.patch_stdout.patch_stdout", _noop_patch_stdout),
        patch("prompt_toolkit.PromptSession") as mock_session_cls,
        patch("anteroom.services.agent_loop.run_agent_loop", side_effect=fake_agent_loop),
        patch("anteroom.cli.repl._compute_fixed_request_overhead", return_value=fixed_overhead),
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
class TestReplContextBudget:
    async def test_footer_uses_full_request_accounting(self, tmp_path: Any) -> None:
        """Visible footer tokens must include fixed request overhead.

        Regression: the footer previously used message-only token counts, which
        could show a tiny context value even when the full request was close to
        the auto-compact threshold.
        """
        db = _make_db(tmp_path)
        config = _make_config(tmp_path)

        output, exited = await _run_repl_with_context_budget(
            ["trigger budget footer"],
            config,
            db,
            fixed_overhead=_FixedRequestOverhead(system_prompt_tokens=70_000, tool_schema_tokens=20_000),
        )

        assert exited, "REPL should exit cleanly after rendering the footer"
        assert "90k/128k" in output
        assert "compact in 10.0k" in output
