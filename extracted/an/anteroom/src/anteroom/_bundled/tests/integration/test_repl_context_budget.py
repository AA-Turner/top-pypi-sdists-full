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
from anteroom.services import storage
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
    agent_events: list[AgentEvent] | None = None,
    phase_snapshots: list[tuple[str, str]] | None = None,
    stop_snapshots: list[tuple[str, str]] | None = None,
) -> tuple[str, bool]:
    from anteroom.cli import renderer as renderer_mod
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

    events = agent_events or [
        AgentEvent(kind="token", data={"content": "ok"}),
        AgentEvent(kind="done", data={}),
    ]

    async def fake_agent_loop(**kwargs: Any) -> Any:
        for event in events:
            yield event

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
    original_set_thinking_phase = renderer_mod.set_thinking_phase
    original_stop_thinking = renderer_mod.stop_thinking

    def tracked_set_thinking_phase(phase: str, data: dict[str, Any] | None = None) -> None:
        original_set_thinking_phase(phase, data)
        if phase_snapshots is not None:
            busy = renderer_mod.get_busy_status()
            phase_snapshots.append((phase, busy.thinking_text if busy else ""))

    async def tracked_stop_thinking(*args: Any, **kwargs: Any) -> float:
        if stop_snapshots is not None:
            before = renderer_mod.get_busy_status()
            stop_snapshots.append(("before", before.thinking_text if before else ""))
        elapsed = await original_stop_thinking(*args, **kwargs)
        if stop_snapshots is not None:
            after = renderer_mod.get_busy_status()
            stop_snapshots.append(("after", after.thinking_text if after else ""))
        return elapsed

    with (
        patch("anteroom.cli.repl.renderer.console", captured_console),
        patch("anteroom.cli.repl.renderer.render_error", lambda msg: captured_console.print(f"Error: {msg}")),
        patch("anteroom.cli.repl.renderer.render_conversation_recap", lambda *a, **k: None),
        patch("anteroom.cli.repl.renderer.set_thinking_phase", tracked_set_thinking_phase),
        patch("anteroom.cli.repl.renderer.stop_thinking", tracked_stop_thinking),
        patch("anteroom.cli.renderer._REPL_THINKING_REVEAL_DELAY", 0),
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

    async def test_small_model_window_uses_derived_warn_threshold(self, tmp_path: Any) -> None:
        """Warnings should use the active derived threshold, not the old 80k default."""
        db = _make_db(tmp_path)
        config = _make_config(tmp_path)
        config.cli.model_context_window = 32_000
        config.cli.context_warn_tokens = 17_440
        config.cli.context_auto_compact_tokens = 21_765

        output, exited = await _run_repl_with_context_budget(
            ["trigger derived warning"],
            config,
            db,
            fixed_overhead=_FixedRequestOverhead(system_prompt_tokens=18_000, tool_schema_tokens=0),
        )

        assert exited, "REPL should exit cleanly after rendering the warning"
        assert "warn at 17,440" in output
        assert "Auto-compacting" not in output

    async def test_compaction_phase_message_reason_renders_and_clears(self, tmp_path: Any) -> None:
        """The REPL surface should show the message-count compact reason only while active."""
        db = _make_db(tmp_path)
        config = _make_config(tmp_path)
        phase_snapshots: list[tuple[str, str]] = []
        stop_snapshots: list[tuple[str, str]] = []

        output, exited = await _run_repl_with_context_budget(
            ["trigger message-count compaction"],
            config,
            db,
            fixed_overhead=_FixedRequestOverhead(system_prompt_tokens=0, tool_schema_tokens=0),
            agent_events=[
                AgentEvent(kind="thinking", data={}),
                AgentEvent(
                    kind="phase",
                    data={
                        "phase": "compacting",
                        "reason": "message_count",
                        "estimated_tokens": 37_000,
                        "token_threshold": 128_000,
                        "message_count": 84,
                        "message_threshold": 80,
                    },
                ),
                AgentEvent(kind="done", data={}),
            ],
            phase_snapshots=phase_snapshots,
            stop_snapshots=stop_snapshots,
        )

        assert exited, "REPL should exit cleanly after the compaction-status turn"
        assert any(
            phase == "compacting" and "Compacting conversation history" in label and "message threshold 84/80" in label
            for phase, label in phase_snapshots
        )
        assert any(
            moment == "before" and "Compacting conversation history" in label and "message threshold 84/80" in label
            for moment, label in stop_snapshots
        )
        assert stop_snapshots[-1] == ("after", "")
        final_line = output.splitlines()[-1] if output.splitlines() else ""
        assert "message threshold 84/80" not in final_line


@pytest.mark.asyncio
async def test_cli_compact_resume_preserves_logical_tool_tail(tmp_path: Any) -> None:
    """CLI /compact persistence reloads the same assistant/tool tail shape."""
    from anteroom.cli.repl import _compact_messages, _load_conversation_messages

    db = _make_db(tmp_path)
    conv_id = storage.create_conversation(db, title="resume tail")["id"]
    storage.create_message(db, conv_id, "user", "old")
    storage.create_message(db, conv_id, "assistant", "old")
    storage.create_message(db, conv_id, "user", "recent")
    assistant = storage.create_message(db, conv_id, "assistant", "")
    storage.create_tool_call(db, assistant["id"], "bash", "builtin", {"command": "echo hi"}, tool_call_id="tc1")
    storage.update_tool_call(db, "tc1", {"stdout": "hi"}, "success")
    storage.create_message(db, conv_id, "user", "next")
    storage.create_message(db, conv_id, "assistant", "done")

    ai_messages, _stored = _load_conversation_messages(db, conv_id)
    svc = AsyncMock()
    svc.complete = AsyncMock(return_value="Summary")

    await _compact_messages(svc, ai_messages, db, conv_id, preserve_tail=4)

    resumed, _resumed_stored = _load_conversation_messages(db, conv_id)
    assert [m["role"] for m in resumed] == ["system", "system", "user", "assistant", "tool", "user", "assistant"]
    assert resumed[3]["tool_calls"][0]["id"] == "tc1"
    assert resumed[4]["tool_call_id"] == "tc1"
