"""Real REPL-path regression coverage for streamed duplicate prose (#1466)."""

from __future__ import annotations

import asyncio
import re
import sqlite3
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from rich.console import Console

from anteroom.config import AIConfig, AppConfig, AppSettings, CliConfig, SafetyConfig
from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.agent_loop import AgentEvent
from anteroom.services.document_extractor import ExtractionResult


def _make_db(tmp_path: Path) -> ThreadSafeConnection:
    db_path = str(tmp_path / "test.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


def _make_config(tmp_path: Path) -> AppConfig:
    cfg = CliConfig()
    cfg.streaming.enabled = True
    cfg.streaming.refresh_hz = 60.0
    return AppConfig(
        ai=AIConfig(
            base_url="http://localhost:1/v1",
            api_key="test-key",
            model="test-model",
        ),
        app=AppSettings(data_dir=tmp_path, tls=False),
        safety=SafetyConfig(approval_mode="auto"),
        cli=cfg,
    )


@contextmanager
def _noop_patch_stdout(**kwargs: Any) -> Any:
    yield


class _PersistentFrameLive:
    """Fake Live that preserves the final frame when transient=False."""

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


async def _run_repl_once(tmp_path: Path) -> str:
    from anteroom.cli.repl import _run_repl

    db = _make_db(tmp_path)
    config = _make_config(tmp_path)
    buf = StringIO()
    captured_console = Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=100,
        highlight=False,
    )

    prompt_calls = 0

    async def fake_prompt(*args: Any, **kwargs: Any) -> str:
        nonlocal prompt_calls
        prompt_calls += 1
        if prompt_calls == 1:
            return "hello"
        await asyncio.sleep(0.2)
        raise EOFError()

    async def fake_agent_loop(**kwargs: Any) -> Any:
        yield AgentEvent(kind="thinking", data={})
        for chunk in [
            "Hello! I'm ",
            "Anteroom, your ",
            "AI coding assistant.",
        ]:
            yield AgentEvent(kind="token", data={"content": chunk})
            await asyncio.sleep(0.02)
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

    with (
        patch("anteroom.cli.repl.renderer.console", captured_console),
        patch("anteroom.cli.repl.renderer._stdout_console", captured_console),
        patch("anteroom.cli.repl.renderer.render_error", lambda msg: captured_console.print(f"Error: {msg}")),
        patch("anteroom.cli.repl.renderer.render_conversation_recap", lambda *a, **k: None),
        patch("anteroom.cli.repl.renderer.use_stdout_console", lambda: None),
        patch("anteroom.cli.repl._patch_stdout", _noop_patch_stdout, create=True),
        patch("prompt_toolkit.patch_stdout.patch_stdout", _noop_patch_stdout),
        patch("prompt_toolkit.PromptSession") as mock_session_cls,
        patch("anteroom.cli.streaming.Live", _PersistentFrameLive),
        patch("anteroom.services.agent_loop.run_agent_loop", side_effect=fake_agent_loop),
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
                working_dir=str(tmp_path),
            )
        except (EOFError, KeyboardInterrupt, SystemExit):
            pass

    return buf.getvalue()


@pytest.mark.asyncio
async def test_streamed_reply_renders_once_through_run_repl(tmp_path: Path) -> None:
    output = await _run_repl_once(tmp_path)
    assert output.count("Hello! I'm Anteroom, your AI coding assistant.") == 1


async def _run_repl_narration_then_tool(tmp_path: Path) -> str:
    """Drive a full tool-using turn: narration -> tool_call_start/end -> done.

    Used by the #1471 real-REPL regression below.
    """
    from anteroom.cli.repl import _run_repl

    db = _make_db(tmp_path)
    config = _make_config(tmp_path)
    buf = StringIO()
    captured_console = Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=100,
        highlight=False,
    )

    prompt_calls = 0

    async def fake_prompt(*args: Any, **kwargs: Any) -> str:
        nonlocal prompt_calls
        prompt_calls += 1
        if prompt_calls == 1:
            return "hello"
        await asyncio.sleep(0.2)
        raise EOFError()

    async def fake_agent_loop(**kwargs: Any) -> Any:
        yield AgentEvent(kind="thinking", data={})
        # Narration token (single chunk so its text is easy to count later).
        yield AgentEvent(
            kind="token",
            data={"content": "I'm checking the config file layout first."},
        )
        await asyncio.sleep(0.02)
        # Tool call interrupts the narration.
        yield AgentEvent(
            kind="tool_call_start",
            data={"tool_name": "read_file", "arguments": {"path": "/tmp/x"}},
        )
        yield AgentEvent(
            kind="tool_call_end",
            data={"tool_name": "read_file", "status": "ok", "output": "ok"},
        )
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

    with (
        patch("anteroom.cli.repl.renderer.console", captured_console),
        patch("anteroom.cli.repl.renderer._stdout_console", captured_console),
        patch("anteroom.cli.repl.renderer.render_error", lambda msg: captured_console.print(f"Error: {msg}")),
        patch("anteroom.cli.repl.renderer.render_conversation_recap", lambda *a, **k: None),
        patch("anteroom.cli.repl.renderer.use_stdout_console", lambda: None),
        patch("anteroom.cli.repl._patch_stdout", _noop_patch_stdout, create=True),
        patch("prompt_toolkit.patch_stdout.patch_stdout", _noop_patch_stdout),
        patch("prompt_toolkit.PromptSession") as mock_session_cls,
        patch("anteroom.services.agent_loop.run_agent_loop", side_effect=fake_agent_loop),
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
                working_dir=str(tmp_path),
            )
        except (EOFError, KeyboardInterrupt, SystemExit):
            pass

    return buf.getvalue()


@pytest.mark.asyncio
async def test_narration_then_tool_through_run_repl_single_render(tmp_path: Path) -> None:
    """Regression for #1471 at the real REPL path: a narration token followed
    by a tool call must render the narration prose exactly once, not once
    on the Thinking line and again as permanent prose.
    """
    import re as _re

    raw = await _run_repl_narration_then_tool(tmp_path)
    plain = _re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]", "", raw)
    assert plain.count("I'm checking the config file layout first.") == 1, (
        f"narration printed {plain.count('narration')} times; raw output was:\n{raw!r}"
    )


async def _run_repl_multiline_narration_then_tool(tmp_path: Path) -> str:
    from anteroom.cli.repl import _run_repl

    db = _make_db(tmp_path)
    config = _make_config(tmp_path)
    buf = StringIO()
    captured_console = Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=100,
        highlight=False,
    )

    prompt_calls = 0

    async def fake_prompt(*args: Any, **kwargs: Any) -> str:
        nonlocal prompt_calls
        prompt_calls += 1
        if prompt_calls == 1:
            return "hello"
        await asyncio.sleep(0.2)
        raise EOFError()

    async def fake_agent_loop(**kwargs: Any) -> Any:
        yield AgentEvent(kind="thinking", data={})
        yield AgentEvent(
            kind="token",
            data={"content": "Here is code:\n```text\nalpha\nbeta\ngamma\n```"},
        )
        await asyncio.sleep(0.02)
        yield AgentEvent(
            kind="tool_call_start",
            data={"tool_name": "read_file", "arguments": {"path": "/tmp/x"}},
        )
        yield AgentEvent(
            kind="tool_call_end",
            data={"tool_name": "read_file", "status": "ok", "output": "ok"},
        )
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

    with (
        patch("anteroom.cli.repl.renderer.console", captured_console),
        patch("anteroom.cli.repl.renderer._stdout_console", captured_console),
        patch("anteroom.cli.repl.renderer.render_error", lambda msg: captured_console.print(f"Error: {msg}")),
        patch("anteroom.cli.repl.renderer.render_conversation_recap", lambda *a, **k: None),
        patch("anteroom.cli.repl.renderer.use_stdout_console", lambda: None),
        patch("anteroom.cli.repl._patch_stdout", _noop_patch_stdout, create=True),
        patch("prompt_toolkit.patch_stdout.patch_stdout", _noop_patch_stdout),
        patch("prompt_toolkit.PromptSession") as mock_session_cls,
        patch("anteroom.services.agent_loop.run_agent_loop", side_effect=fake_agent_loop),
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
                working_dir=str(tmp_path),
            )
        except (EOFError, KeyboardInterrupt, SystemExit):
            pass

    return buf.getvalue()


@pytest.mark.asyncio
async def test_multiline_narration_then_tool_through_run_repl_single_render(tmp_path: Path) -> None:
    multiline = "alpha"
    raw = await _run_repl_multiline_narration_then_tool(tmp_path)
    plain = re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]", "", raw)
    assert plain.count(multiline) == 1, (
        f"multiline narration printed {plain.count(multiline)} times; raw output was:\n{raw!r}"
    )


def _tool_schema(name: str) -> dict[str, Any]:
    return {"type": "function", "function": {"name": name, "parameters": {"type": "object", "properties": {}}}}


async def _capture_repl_turn_tool_names(tmp_path: Path, user_text: str, tools: list[dict[str, Any]]) -> set[str]:
    from anteroom.cli.repl import _run_repl

    db = _make_db(tmp_path)
    config = _make_config(tmp_path)
    captured_tools: list[dict[str, Any]] | None = None
    buf = StringIO()
    captured_console = Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=100,
        highlight=False,
    )

    prompt_calls = 0

    async def fake_prompt(*args: Any, **kwargs: Any) -> str:
        nonlocal prompt_calls
        prompt_calls += 1
        if prompt_calls == 1:
            return user_text
        await asyncio.sleep(0.2)
        raise EOFError()

    async def fake_agent_loop(**kwargs: Any) -> Any:
        nonlocal captured_tools
        captured_tools = kwargs.get("tools_openai")
        yield AgentEvent(kind="thinking", data={})
        yield AgentEvent(kind="token", data={"content": "Captured."})
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

    with (
        patch("anteroom.cli.repl.renderer.console", captured_console),
        patch("anteroom.cli.repl.renderer._stdout_console", captured_console),
        patch("anteroom.cli.repl.renderer.render_error", lambda msg: captured_console.print(f"Error: {msg}")),
        patch("anteroom.cli.repl.renderer.render_conversation_recap", lambda *a, **k: None),
        patch("anteroom.cli.repl.renderer.use_stdout_console", lambda: None),
        patch("anteroom.cli.repl._patch_stdout", _noop_patch_stdout, create=True),
        patch("prompt_toolkit.patch_stdout.patch_stdout", _noop_patch_stdout),
        patch("prompt_toolkit.PromptSession") as mock_session_cls,
        patch("anteroom.cli.streaming.Live", _PersistentFrameLive),
        patch("anteroom.services.agent_loop.run_agent_loop", side_effect=fake_agent_loop),
    ):
        mock_session_cls.return_value = mock_session_instance
        try:
            await _run_repl(
                config=config,
                db=db,
                ai_service=mock_ai,
                tool_executor=mock_tool_executor,
                tools_openai=tools,
                extra_system_prompt="",
                all_tool_names=[tool["function"]["name"] for tool in tools],
                working_dir=str(tmp_path),
            )
        except (EOFError, KeyboardInterrupt, SystemExit):
            pass

    assert captured_tools is not None
    return {tool["function"]["name"] for tool in captured_tools}


@pytest.mark.asyncio
async def test_inline_pdf_turn_filters_file_tools_and_subagents(tmp_path: Path) -> None:
    pdf = tmp_path / "ID Card.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake pdf")
    tools = [
        _tool_schema(name)
        for name in (
            "bash",
            "glob_files",
            "grep",
            "read_file",
            "docx",
            "xlsx",
            "pptx",
            "run_agent",
            "ask_user",
            "save_memory",
        )
    ]

    with patch(
        "anteroom.services.document_extractor.extract_text",
        return_value=ExtractionResult(text="PDF text"),
    ):
        names = await _capture_repl_turn_tool_names(tmp_path, f"{pdf} what's in this pdf", tools)

    assert {"ask_user", "save_memory"} <= names
    assert not (
        names
        & {
            "bash",
            "glob_files",
            "grep",
            "read_file",
            "docx",
            "xlsx",
            "pptx",
            "run_agent",
        }
    )


@pytest.mark.asyncio
async def test_non_pdf_turn_preserves_file_tools_and_subagents(tmp_path: Path) -> None:
    tools = [
        _tool_schema(name)
        for name in (
            "bash",
            "glob_files",
            "grep",
            "read_file",
            "docx",
            "xlsx",
            "pptx",
            "run_agent",
            "ask_user",
        )
    ]

    names = await _capture_repl_turn_tool_names(tmp_path, "inspect the repo", tools)

    assert names == {tool["function"]["name"] for tool in tools}
