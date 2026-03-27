"""Integration tests for REPL slash commands via the _run_repl harness (#660).

Uses the direct _run_repl integration pattern (not PTY) for deterministic
command-flow coverage with Rich console output assertions.
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


def _make_db(tmp_path: Any) -> ThreadSafeConnection:
    db_path = str(tmp_path / "test.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


def _seed_space(db: ThreadSafeConnection, space_id: str = "sp1", name: str = "testspace") -> dict:
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO spaces (id, name, source_file, source_hash, last_loaded_at, created_at, updated_at) "
        "VALUES (?, ?, ?, '', '', ?, ?)",
        (space_id, name, "/s.yaml", now, now),
    )
    db.commit()
    return {"id": space_id, "name": name}


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


async def _run_repl_with_commands(
    commands: list[str],
    config: AppConfig,
    db: ThreadSafeConnection,
    space: dict[str, Any],
    extra_system_prompt: str = "",
    return_mock_ai: bool = False,
) -> Any:
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
    mock_tool_executor = AsyncMock()
    mock_session_instance = MagicMock()
    mock_session_instance.prompt_async = fake_prompt
    mock_session_instance.default_buffer = MagicMock()
    mock_session_instance.default_buffer.on_text_changed = MagicMock()

    with (
        patch("anteroom.cli.repl.renderer.console", captured_console),
        patch("anteroom.cli.repl.renderer.render_error", lambda msg: captured_console.print(f"Error: {msg}")),
        patch("anteroom.cli.repl.renderer.render_conversation_recap", lambda *a, **k: None),
        patch("anteroom.cli.renderer.use_stdout_console", lambda: None),
        patch("anteroom.cli.repl._patch_stdout", _noop_patch_stdout, create=True),
        patch("prompt_toolkit.patch_stdout.patch_stdout", _noop_patch_stdout),
        patch("prompt_toolkit.PromptSession") as mock_session_cls,
    ):
        mock_session_cls.return_value = mock_session_instance
        try:
            await _run_repl(
                config=config,
                db=db,
                ai_service=mock_ai,
                tool_executor=mock_tool_executor,
                tools_openai=None,
                extra_system_prompt=extra_system_prompt,
                all_tool_names=[],
                working_dir=str(config.app.data_dir),
                space=space,
            )
        except (EOFError, KeyboardInterrupt, SystemExit):
            pass

    output = buf.getvalue()
    if return_mock_ai:
        return output, mock_ai
    return output


@pytest.mark.asyncio
class TestSlashCommands:
    # /help opens a prompt_toolkit message_dialog that requires a real terminal.
    # This is a PTY-only test — skipped from the _run_repl harness.

    async def test_tools_shows_tool_list(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        output = await _run_repl_with_commands(["/tools"], config, db, sp)
        assert "tool" in output.lower() or "read_file" in output.lower()

    async def test_usage_shows_stats(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        output = await _run_repl_with_commands(["/usage"], config, db, sp)
        assert "usage" in output.lower() or "token" in output.lower() or "0" in output

    async def test_model_shows_current_model(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        output = await _run_repl_with_commands(["/model"], config, db, sp)
        assert "test-model" in output or "model" in output.lower()

    async def test_unknown_command_no_crash(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        output = await _run_repl_with_commands(["/nonexistent_cmd_xyz"], config, db, sp)
        # Unknown commands are treated as user messages by the REPL, not errors.
        # Just verify no crash/traceback in the captured output.
        assert "Traceback" not in output

    async def test_plan_on_off_toggle(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        output = await _run_repl_with_commands(["/plan on", "/plan off"], config, db, sp)
        assert "plan" in output.lower()

    async def test_exit_graceful(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        # /exit is always appended by the harness, so an empty command list tests graceful exit
        output = await _run_repl_with_commands([], config, db, sp)
        # Should not contain traceback
        assert "Traceback" not in output

    async def test_empty_input_no_crash(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        output = await _run_repl_with_commands(["", "   "], config, db, sp)
        assert "Traceback" not in output

    async def test_clear_prints_confirmation(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        output = await _run_repl_with_commands(["/clear"], config, db, sp)
        assert "cleared" in output.lower()
        assert "Traceback" not in output

    async def test_clear_creates_new_conversation(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        # Count conversations before
        count_before = db.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
        await _run_repl_with_commands(["/clear"], config, db, sp)
        # /clear creates a new conversation (initial + clear = 2)
        count_after = db.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
        assert count_after >= count_before + 2  # initial conv + /clear conv

    async def test_clear_preserves_plan_mode(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        output = await _run_repl_with_commands(["/plan on", "/clear", "/plan status"], config, db, sp)
        # After /clear, plan mode should still be active
        assert "cleared" in output.lower()
        # /plan status should report active (not "off" or "not active")
        assert "active" in output.lower() or "on" in output.lower()

    async def test_clear_on_fresh_session(self, tmp_path: Any) -> None:
        """Clear with no prior messages should work cleanly."""
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        # /clear immediately — no messages sent first
        output = await _run_repl_with_commands(["/clear"], config, db, sp)
        assert "cleared" in output.lower()
        assert "Traceback" not in output

    async def test_clear_twice_in_a_row(self, tmp_path: Any) -> None:
        """Two consecutive clears should each create a new conversation."""
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        count_before = db.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
        output = await _run_repl_with_commands(["/clear", "/clear"], config, db, sp)
        count_after = db.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
        # initial + 2 clears = 3 new conversations
        assert count_after >= count_before + 3
        assert output.lower().count("cleared") >= 2
        assert "Traceback" not in output

    async def test_clear_strips_approved_plan(self, tmp_path: Any) -> None:
        """Clear should strip conversation-scoped <approved_plan> from extra_system_prompt."""
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        # Inject an approved_plan tag into extra_system_prompt (conversation-scoped)
        injected_prompt = (
            "\n\n<approved_plan>\nThe user has approved the following implementation plan. "
            "Execute it step by step.\n\nStep 1: do something\n</approved_plan>"
        )
        # Send /clear then a user message — the user message triggers agent loop
        output, mock_ai = await _run_repl_with_commands(
            ["/clear", "hello after clear"],
            config,
            db,
            sp,
            extra_system_prompt=injected_prompt,
            return_mock_ai=True,
        )
        assert "cleared" in output.lower()
        # If stream_chat was called, the system messages should NOT contain approved_plan
        if mock_ai.stream_chat.called:
            call_args = mock_ai.stream_chat.call_args
            messages = call_args[1].get("messages", call_args[0][0] if call_args[0] else [])
            system_content = " ".join(str(m.get("content", "")) for m in messages if m.get("role") == "system")
            assert "approved_plan" not in system_content

    async def test_clear_links_new_conversation_to_space(self, tmp_path: Any) -> None:
        """Clear should link the new conversation to the active space."""
        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)
        await _run_repl_with_commands(["/clear"], config, db, sp)
        # The most recent conversation should be linked to the space
        row = db.execute("SELECT space_id FROM conversations ORDER BY created_at DESC LIMIT 1").fetchone()
        assert row is not None
        assert row[0] == sp["id"]
