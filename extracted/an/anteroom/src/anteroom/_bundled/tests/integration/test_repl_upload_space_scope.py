"""CLI integration tests for /upload auto-linking into the active space (#1545)."""

from __future__ import annotations

import asyncio
import sqlite3
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from rich.console import Console

from anteroom.config import AIConfig, AppConfig, AppSettings, CliConfig, SafetyConfig, ServerConfig
from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.storage import get_space_sources


def _make_db(tmp_path: Any) -> ThreadSafeConnection:
    db_path = str(tmp_path / "test.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


def _seed_space(db: ThreadSafeConnection, space_id: str = "sp1", name: str = "docs") -> dict[str, str]:
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO spaces (id, name, source_file, source_hash, last_loaded_at, created_at, updated_at) "
        "VALUES (?, ?, ?, '', '', ?, ?)",
        (space_id, name, "/space.yaml", now, now),
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
    *,
    space: dict[str, Any] | None = None,
) -> str:
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
        patch("anteroom.cli.repl._embed_after_upload", AsyncMock(return_value=None)),
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
                space=space,
            )
        except (EOFError, KeyboardInterrupt, SystemExit):
            pass

    return buf.getvalue()


@pytest.mark.asyncio
class TestReplUploadSpaceScope:
    async def test_upload_links_file_to_active_space(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        space = _seed_space(db)
        config = _make_config(tmp_path)
        upload_path = Path(tmp_path) / "notes.txt"
        upload_path.write_text("Important notes for the active space", encoding="utf-8")

        output = await _run_repl_with_commands([f"/upload {upload_path}"], config, db, space=space)

        assert "linked to active space: docs" in output
        linked = get_space_sources(db, space["id"])
        assert len(linked) == 1
        assert linked[0]["filename"] == "notes.txt"

    async def test_upload_rejects_files_over_configured_server_limit(self, tmp_path: Any) -> None:
        db = _make_db(tmp_path)
        config = _make_config(tmp_path)
        config.server = ServerConfig(max_upload_mb=1)
        upload_path = Path(tmp_path) / "too-big.txt"
        with upload_path.open("wb") as fh:
            fh.truncate((1 * 1024 * 1024) + 1)

        output = await _run_repl_with_commands([f"/upload {upload_path}"], config, db)

        assert "File too large (1 MB). Maximum is 1 MB." in output
