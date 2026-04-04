"""Additional unit tests for small REPL helper functions."""

from __future__ import annotations

import asyncio
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.cli.repl import (
    _build_introspect_instructions_info,
    _build_system_prompt,
    _check_for_update,
    _cleanup_after_turn,
    _detect_project_context,
    _drain_input_to_msg_queue,
    _embed_after_upload,
    _identity_kwargs,
    _load_conversation_messages,
    _parse_bang_command,
    _replace_file_instructions,
    _route_cancel_signal,
    _run_bang_command,
    _run_mcp_startup_live,
    _show_resume_info,
    _show_usage_stats,
)


class _FakeProc:
    def __init__(self, *, stdout: bytes = b"", returncode: int | None = 0) -> None:
        self._stdout = stdout
        self.returncode = returncode
        self.killed = False
        self.waited = False

    async def communicate(self) -> tuple[bytes, bytes]:
        return self._stdout, b""

    def kill(self) -> None:
        self.killed = True

    async def wait(self) -> None:
        self.waited = True


def test_load_conversation_messages_reconstructs_tool_calls() -> None:
    db = MagicMock()
    stored_messages = [
        {"role": "system", "content": "rules"},
        {"role": "user", "content": "hello"},
        {
            "role": "assistant",
            "content": "using tools",
            "tool_calls": [
                {
                    "id": "call_1",
                    "tool_name": "read_file",
                    "input": {"path": "a.txt"},
                    "output": {"content": "A"},
                }
            ],
        },
        {"role": "assistant", "content": "done"},
        {"role": "ignored", "content": "skip me"},
    ]

    with patch("anteroom.cli.repl.storage.list_messages", return_value=stored_messages):
        ai_messages, raw = _load_conversation_messages(db, "conv-1")

    assert raw == stored_messages
    assert ai_messages[0] == {"role": "system", "content": "rules"}
    assert ai_messages[1] == {"role": "user", "content": "hello"}
    assert ai_messages[2]["role"] == "assistant"
    assert ai_messages[2]["tool_calls"][0]["function"]["name"] == "read_file"
    assert ai_messages[3] == {"role": "tool", "tool_call_id": "call_1", "content": '{"content": "A"}'}
    assert ai_messages[4] == {"role": "assistant", "content": "done"}


@pytest.mark.asyncio
async def test_check_for_update_returns_newer_version() -> None:
    proc = _FakeProc(stdout=b"anteroom (9.9.9)\n", returncode=0)

    with patch("anteroom.cli.repl.asyncio.create_subprocess_exec", new=AsyncMock(return_value=proc)):
        assert await _check_for_update("1.0.0") == "9.9.9"


@pytest.mark.asyncio
async def test_check_for_update_cleans_up_on_exception() -> None:
    proc = _FakeProc(returncode=None)

    async def _raise_runtime(awaitable, timeout):
        if hasattr(awaitable, "close"):
            awaitable.close()
        raise RuntimeError("boom")

    with (
        patch("anteroom.cli.repl.asyncio.create_subprocess_exec", new=AsyncMock(return_value=proc)),
        patch("anteroom.cli.repl.asyncio.wait_for", side_effect=_raise_runtime),
    ):
        assert await _check_for_update("1.0.0") is None

    assert proc.killed is True
    assert proc.waited is True


def test_route_cancel_signal_sets_current_event() -> None:
    agent_busy = asyncio.Event()
    agent_busy.set()
    cancel_event = asyncio.Event()

    routed = _route_cancel_signal(agent_busy, [cancel_event])

    assert routed is True
    assert cancel_event.is_set() is True


def test_route_cancel_signal_returns_false_when_idle() -> None:
    assert _route_cancel_signal(asyncio.Event(), [asyncio.Event()]) is False


def test_cleanup_after_turn_backfills_queue_on_cancel() -> None:
    cancel_event = asyncio.Event()
    cancel_event.set()
    agent_busy = asyncio.Event()
    agent_busy.set()
    msg_queue: asyncio.Queue[dict[str, str]] = asyncio.Queue()
    msg_queue.put_nowait({"role": "user", "content": "queued"})
    ai_messages: list[dict[str, str]] = []

    _cleanup_after_turn(cancel_event, agent_busy, msg_queue, ai_messages, has_pending_work=lambda: True)

    assert ai_messages == [{"role": "user", "content": "queued"}]
    assert agent_busy.is_set() is False


def test_cleanup_after_turn_clears_busy_when_no_pending_work() -> None:
    cancel_event = asyncio.Event()
    agent_busy = asyncio.Event()
    agent_busy.set()
    msg_queue: asyncio.Queue[dict[str, str]] = asyncio.Queue()

    _cleanup_after_turn(cancel_event, agent_busy, msg_queue, [], has_pending_work=lambda: False)

    assert agent_busy.is_set() is False


@pytest.mark.asyncio
async def test_drain_input_to_msg_queue_handles_exit_command() -> None:
    input_queue: asyncio.Queue[str] = asyncio.Queue()
    input_queue.put_nowait("/quit")
    msg_queue: asyncio.Queue[dict[str, str]] = asyncio.Queue()
    cancel_event = asyncio.Event()
    exit_flag = asyncio.Event()

    await _drain_input_to_msg_queue(
        input_queue,
        msg_queue,
        "/tmp",
        MagicMock(),
        "conv-1",
        cancel_event,
        exit_flag,
    )

    assert cancel_event.is_set() is True
    assert exit_flag.is_set() is True
    assert msg_queue.empty() is True


@pytest.mark.asyncio
async def test_drain_input_to_msg_queue_warns_on_unknown_command() -> None:
    input_queue: asyncio.Queue[str] = asyncio.Queue()
    input_queue.put_nowait("/unknown stuff")
    msg_queue: asyncio.Queue[dict[str, str]] = asyncio.Queue()
    warn = MagicMock()

    await _drain_input_to_msg_queue(
        input_queue,
        msg_queue,
        "/tmp",
        MagicMock(),
        "conv-1",
        asyncio.Event(),
        asyncio.Event(),
        warn_callback=warn,
    )

    warn.assert_called_once_with("/unknown")
    assert msg_queue.empty() is True


@pytest.mark.asyncio
async def test_drain_input_to_msg_queue_expands_skill_invocation() -> None:
    input_queue: asyncio.Queue[str] = asyncio.Queue()
    input_queue.put_nowait("/skill do thing")
    msg_queue: asyncio.Queue[dict[str, str]] = asyncio.Queue()
    db = MagicMock()
    skill_registry = MagicMock()
    skill_registry.resolve_input.return_value = (True, "expanded prompt")

    with patch("anteroom.cli.repl.storage.create_message") as create_message:
        await _drain_input_to_msg_queue(
            input_queue,
            msg_queue,
            "/tmp",
            db,
            "conv-1",
            asyncio.Event(),
            asyncio.Event(),
            identity_kwargs={"user_id": "u1"},
            skill_registry=skill_registry,
        )

    create_message.assert_called_once()
    assert await msg_queue.get() == {"role": "user", "content": "expanded prompt"}


def test_parse_bang_command_variants() -> None:
    assert _parse_bang_command("!git status") == "git status"
    assert _parse_bang_command("! git status") == "git status"
    assert _parse_bang_command("   !pwd") == "pwd"
    assert _parse_bang_command("!   ") == ""
    assert _parse_bang_command("hello") is None
    assert _parse_bang_command("/help") is None


@pytest.mark.asyncio
async def test_run_bang_command_executes_shell_without_persisting() -> None:
    tool_registry = MagicMock()
    config = SimpleNamespace(safety=SimpleNamespace(bash=SimpleNamespace(timeout=33)))

    with (
        patch("anteroom.cli.repl.renderer") as renderer,
        patch(
            "anteroom.tools.bash.handle",
            new=AsyncMock(return_value={"stdout": "ok\n", "stderr": "warn\n"}),
        ) as handle,
    ):
        handled = await _run_bang_command(
            "! git status",
            working_dir="/tmp/project",
            tool_registry=tool_registry,
            config=config,
        )

    assert handled is True
    assert tool_registry._working_dir == "/tmp/project"
    handle.assert_awaited_once_with(
        command="git status",
        timeout=33,
        _bypass_hard_block=False,
        _sandbox_config=config.safety.bash,
    )
    assert renderer.console.print.call_args_list[0].args == ("ok\n",)
    assert renderer.console.print.call_args_list[0].kwargs == {"end": ""}
    assert renderer.console.print.call_args_list[1].args == ("warn\n",)
    assert renderer.console.print.call_args_list[1].kwargs == {"end": ""}


@pytest.mark.asyncio
async def test_run_bang_command_rejects_empty_shell_escape() -> None:
    tool_registry = MagicMock()
    config = SimpleNamespace(safety=SimpleNamespace(bash=SimpleNamespace(timeout=33)))

    with patch("anteroom.cli.repl.renderer") as renderer:
        handled = await _run_bang_command(
            "!   ",
            working_dir="/tmp/project",
            tool_registry=tool_registry,
            config=config,
        )

    assert handled is True
    renderer.console.print.assert_called_once()


@pytest.mark.asyncio
async def test_drain_input_to_msg_queue_executes_bang_without_queueing() -> None:
    input_queue: asyncio.Queue[str] = asyncio.Queue()
    input_queue.put_nowait("!pwd")
    msg_queue: asyncio.Queue[dict[str, str]] = asyncio.Queue()
    db = MagicMock()
    tool_registry = MagicMock()
    config = SimpleNamespace(safety=SimpleNamespace(bash=SimpleNamespace(timeout=12)))

    with (
        patch("anteroom.cli.repl.storage.create_message") as create_message,
        patch("anteroom.cli.repl.renderer"),
        patch("anteroom.tools.bash.handle", new=AsyncMock(return_value={"stdout": "x\n"})) as handle,
    ):
        await _drain_input_to_msg_queue(
            input_queue,
            msg_queue,
            "/tmp",
            db,
            "conv-1",
            asyncio.Event(),
            asyncio.Event(),
            tool_registry=tool_registry,
            config=config,
        )

    create_message.assert_not_called()
    assert msg_queue.empty() is True
    handle.assert_awaited_once_with(
        command="pwd",
        timeout=12,
        _bypass_hard_block=False,
        _sandbox_config=config.safety.bash,
    )


def test_detect_project_context_reports_markers(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n")
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()

    context = _detect_project_context(str(tmp_path))

    assert "git repository" in context
    assert "Python project (pyproject.toml)" in context
    assert "Key directories: src, tests" in context


def test_build_introspect_instructions_info_collects_sources() -> None:
    with (
        patch(
            "anteroom.cli.instructions.find_global_instructions_path",
            return_value=(Path("/tmp/global.md"), "global text"),
        ),
        patch(
            "anteroom.cli.instructions.find_project_instructions_path",
            return_value=(Path("/tmp/project.md"), "project text"),
        ),
        patch("anteroom.cli.instructions.estimate_tokens", side_effect=[11, 17]),
    ):
        result = _build_introspect_instructions_info("/tmp/project")

    assert result["total_tokens"] == 28
    assert result["sources"] == [
        {"path": "/tmp/global.md", "source": "global", "estimated_tokens": 11},
        {"path": "/tmp/project.md", "source": "project", "estimated_tokens": 17},
    ]


def test_identity_kwargs_with_identity() -> None:
    config = SimpleNamespace(identity=SimpleNamespace(user_id="user-1", display_name="Troy"))
    assert _identity_kwargs(config) == {"user_id": "user-1", "user_display_name": "Troy"}


def test_identity_kwargs_without_identity() -> None:
    assert _identity_kwargs(SimpleNamespace(identity=None)) == {"user_id": None, "user_display_name": None}


@pytest.mark.asyncio
async def test_embed_after_upload_handles_no_worker() -> None:
    get_worker = AsyncMock(return_value=None)
    assert await _embed_after_upload(get_worker, "source-1") is None


@pytest.mark.asyncio
async def test_embed_after_upload_returns_chunk_count() -> None:
    worker = MagicMock()
    worker.embed_source = AsyncMock(return_value=42)
    get_worker = AsyncMock(return_value=worker)

    assert await _embed_after_upload(get_worker, "source-1") == 42


def test_show_resume_info_renders_recap_and_rag_sources() -> None:
    db = MagicMock()
    conv = {"id": "conv-1", "title": "Saved chat"}
    ai_messages = [{"role": "user", "content": "hi"}]
    stored = [
        {"role": "assistant", "content": "answer", "metadata": {"rag_sources": [{"title": "Doc"}]}},
        {"role": "user", "content": "follow-up", "metadata": None},
    ]

    with (
        patch("anteroom.cli.repl.storage.list_messages", return_value=stored),
        patch("anteroom.cli.repl.renderer") as renderer,
    ):
        _show_resume_info(db, conv, ai_messages)

    renderer.render_conversation_recap.assert_called_once_with(stored)
    renderer.render_rag_sources.assert_called_once_with([{"title": "Doc"}])


def test_show_usage_stats_prints_costs_and_model_breakdown() -> None:
    db = MagicMock()
    config = SimpleNamespace(
        cli=SimpleNamespace(
            usage=SimpleNamespace(
                week_days=7,
                month_days=30,
                model_costs={
                    "gpt-a": {"input": 1.0, "output": 2.0},
                    "gpt-b": {"input": 0.5, "output": 1.0},
                },
            )
        )
    )
    stats = [
        {
            "model": "gpt-a",
            "prompt_tokens": 1_000_000,
            "completion_tokens": 500_000,
            "total_tokens": 1_500_000,
            "message_count": 2,
        },
        {
            "model": "gpt-b",
            "prompt_tokens": 0,
            "completion_tokens": 1_000_000,
            "total_tokens": 1_000_000,
            "message_count": 1,
        },
    ]

    with (
        patch("anteroom.cli.repl.storage.get_usage_stats", return_value=stats),
        patch("anteroom.cli.repl.renderer") as renderer,
    ):
        _show_usage_stats(db, config)

    printed = "\n".join(call.args[0] for call in renderer.console.print.call_args_list if call.args)
    assert "Token Usage" in printed
    assert "Est. cost" in printed
    assert "By model" in printed
    assert "gpt-a" in printed
    assert "gpt-b" in printed


@pytest.mark.asyncio
async def test_run_mcp_startup_live_tracks_connected_and_failed_servers() -> None:
    statuses: dict[str, dict[str, object]] = {}
    servers = [SimpleNamespace(name="alpha"), SimpleNamespace(name="beta")]

    async def _startup(*, status_callback) -> None:
        status_callback("alpha", {"status": "connected", "tool_count": 3})
        status_callback("beta", {"status": "error", "error_message": "broken connection to service"})

    mcp_manager = SimpleNamespace(startup=_startup)

    with patch("anteroom.cli.repl.renderer") as renderer:
        renderer.startup_step.return_value = nullcontext()
        await _run_mcp_startup_live(mcp_manager, servers, statuses)

    assert statuses["alpha"]["status"] == "connected"
    assert statuses["beta"]["status"] == "error"
    printed = "\n".join(call.args[0] for call in renderer.console.print.call_args_list if call.args)
    assert "alpha" in printed
    assert "beta" in printed
    assert "MCP:" in printed


class TestReplaceFileInstructions:
    """Tests for _replace_file_instructions (#1302)."""

    def test_in_place_replacement(self) -> None:
        prompt = "before\n<file_instructions>\nold content\n</file_instructions>\nafter"
        result = _replace_file_instructions(prompt, "new content")
        assert "<file_instructions>\nnew content\n</file_instructions>" in result
        assert "before" in result
        assert "after" in result
        assert "old content" not in result

    def test_preserves_boundary(self) -> None:
        prompt = (
            "trusted section\n<file_instructions>\nold\n</file_instructions>\nmore trusted\n--- UNTRUSTED SECTION ---"
        )
        result = _replace_file_instructions(prompt, "new instructions")
        # Untrusted marker stays after the file_instructions block
        fi_pos = result.index("<file_instructions>")
        untrusted_pos = result.index("--- UNTRUSTED SECTION ---")
        assert fi_pos < untrusted_pos

    def test_inserts_when_absent_after_project_context(self) -> None:
        prompt = "<project_context>\nWorking directory: /tmp\n</project_context>\nother stuff"
        result = _replace_file_instructions(prompt, "new instructions")
        assert "<file_instructions>\nnew instructions\n</file_instructions>" in result
        # Inserted after </project_context>
        pc_pos = result.index("</project_context>")
        fi_pos = result.index("<file_instructions>")
        assert fi_pos > pc_pos

    def test_inserts_when_absent_after_space_instructions(self) -> None:
        prompt = (
            "<project_context>\nctx\n</project_context>\n"
            '<space_instructions space="s">\ninstr\n</space_instructions>\n'
            "other"
        )
        result = _replace_file_instructions(prompt, "new")
        assert "<file_instructions>\nnew\n</file_instructions>" in result
        # Prefers space_instructions anchor
        si_pos = result.index("</space_instructions>")
        fi_pos = result.index("<file_instructions>")
        assert fi_pos > si_pos

    def test_removes_when_none(self) -> None:
        prompt = "before\n<file_instructions>\nold\n</file_instructions>\nafter"
        result = _replace_file_instructions(prompt, None)
        assert "file_instructions" not in result
        assert "before" in result
        assert "after" in result

    def test_no_op_when_none_and_absent(self) -> None:
        prompt = "no instructions here"
        result = _replace_file_instructions(prompt, None)
        assert result == prompt

    def test_preserves_other_sections(self) -> None:
        prompt = (
            "<project_context>\nctx\n</project_context>\n"
            '<space_instructions space="s">\nspace\n</space_instructions>\n'
            "<file_instructions>\nold\n</file_instructions>\n"
            '<artifact type="rule" fqn="test">\nrule\n</artifact>'
        )
        result = _replace_file_instructions(prompt, "new")
        assert "space_instructions" in result
        assert "space" in result
        assert "project_context" in result
        assert "artifact" in result
        assert "rule" in result


class TestBuildSystemPromptInstructionsTags:
    """Verify _build_system_prompt wraps instructions in <file_instructions> tags (#1302)."""

    def test_instructions_wrapped_in_tags(self) -> None:
        from anteroom.config import AIConfig, AppConfig, AppSettings, CliConfig, SafetyConfig

        config = AppConfig(
            ai=AIConfig(base_url="http://localhost:1/v1", api_key="k", model="m"),
            app=AppSettings(data_dir=Path("/tmp"), tls=False),
            safety=SafetyConfig(),
            cli=CliConfig(),
        )
        result = _build_system_prompt(config, "/tmp", "# Test Instructions\nHello")
        assert "<file_instructions>" in result
        assert "# Test Instructions\nHello" in result
        assert "</file_instructions>" in result

    def test_no_tags_when_no_instructions(self) -> None:
        from anteroom.config import AIConfig, AppConfig, AppSettings, CliConfig, SafetyConfig

        config = AppConfig(
            ai=AIConfig(base_url="http://localhost:1/v1", api_key="k", model="m"),
            app=AppSettings(data_dir=Path("/tmp"), tls=False),
            safety=SafetyConfig(),
            cli=CliConfig(),
        )
        result = _build_system_prompt(config, "/tmp", None)
        assert "file_instructions" not in result
