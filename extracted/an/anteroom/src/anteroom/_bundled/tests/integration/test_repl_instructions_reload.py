"""Integration tests for REPL instruction reload during active sessions (#1302).

Uses the _run_repl integration harness pattern from test_repl_commands.py.
"""

from __future__ import annotations

import asyncio
import sqlite3
import time
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from rich.console import Console

from anteroom.cli.instructions import InstructionsSnapshot, capture_snapshot
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


async def _run_repl_with_instructions(
    commands: list[str],
    config: AppConfig,
    db: ThreadSafeConnection,
    space: dict[str, Any],
    extra_system_prompt: str = "",
    instructions: str | None = None,
    instructions_snapshot: InstructionsSnapshot | None = None,
) -> str:
    """Run _run_repl with instruction snapshot support and return console output."""
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
                instructions=instructions,
                instructions_snapshot=instructions_snapshot,
            )
        except (EOFError, KeyboardInterrupt, SystemExit):
            pass

    return buf.getvalue()


@pytest.mark.asyncio
class TestInstructionsReload:
    async def test_reload_on_file_change(self, tmp_path: Path) -> None:
        """When ANTEROOM.md changes between turns, the REPL reloads instructions."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "ANTEROOM.md").write_text("v1 instructions")

        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)

        prompt_with_v1 = (
            "<project_context>\nWorking directory: /tmp\n</project_context>"
            "\n<file_instructions>\n# Global Instructions\nglobal\n\n# Project Instructions\nv1 instructions"
            "\n</file_instructions>"
        )

        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(project_dir))

        # Modify the file so that has_changed() will detect the change
        time.sleep(0.05)
        (project_dir / "ANTEROOM.md").write_text("v2 instructions")

        # Mock trust to return "trusted"
        with patch(
            "anteroom.cli.repl.find_project_instructions_path",
            return_value=(project_dir / "ANTEROOM.md", "v2 instructions"),
        ):
            with patch("anteroom.cli.repl.find_global_instructions", return_value=None):
                with patch("anteroom.services.trust.check_trust", return_value="trusted"):
                    output = await _run_repl_with_instructions(
                        commands=["hello"],
                        config=config,
                        db=db,
                        space=sp,
                        extra_system_prompt=prompt_with_v1,
                        instructions="v1 instructions",
                        instructions_snapshot=snap,
                    )

        assert "Instructions reloaded" in output

    async def test_no_reload_when_unchanged(self, tmp_path: Path) -> None:
        """No reload message when instruction files haven't changed."""
        # Use tmp_path directly as working dir (matches _run_repl's working_dir = config.app.data_dir)
        (tmp_path / "ANTEROOM.md").write_text("stable")

        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)

        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(tmp_path))

        # Use slash commands to avoid triggering agent turns (which need AI mock)
        output = await _run_repl_with_instructions(
            commands=["/tools", "/tools"],
            config=config,
            db=db,
            space=sp,
            extra_system_prompt="<project_context>\nctx\n</project_context>",
            instructions="stable",
            instructions_snapshot=snap,
        )

        assert "Instructions reloaded" not in output

    async def test_trust_recheck_on_change(self, tmp_path: Path) -> None:
        """When project instructions change, trust is re-checked; warns if hash differs."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "ANTEROOM.md").write_text("original")

        db = _make_db(tmp_path)
        sp = _seed_space(db)
        config = _make_config(tmp_path)

        with patch("anteroom.cli.instructions.find_global_instructions_path", return_value=None):
            snap = capture_snapshot(str(project_dir))

        # Modify file to trigger change
        time.sleep(0.05)
        (project_dir / "ANTEROOM.md").write_text("modified")

        with (
            patch(
                "anteroom.cli.repl.find_project_instructions_path",
                return_value=(project_dir / "ANTEROOM.md", "modified"),
            ),
            patch("anteroom.cli.repl.find_global_instructions", return_value=None),
            patch("anteroom.services.trust.check_trust", return_value="changed"),
        ):
            output = await _run_repl_with_instructions(
                commands=["hello"],
                config=config,
                db=db,
                space=sp,
                extra_system_prompt="<project_context>\nctx\n</project_context>\n<file_instructions>\noriginal\n</file_instructions>",
                instructions="original",
                instructions_snapshot=snap,
            )

        assert "Instructions changed on disk" in output
        assert "Instructions reloaded" not in output
