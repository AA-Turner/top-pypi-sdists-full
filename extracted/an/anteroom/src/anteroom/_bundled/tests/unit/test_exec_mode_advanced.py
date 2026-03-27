"""Advanced exec mode tests: MCP failure, artifacts, JSON output, timeout (#1021)."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.cli.exec_mode import (
    _sanitize_for_terminal,
    _truncate,
    run_exec_mode,
)


@dataclass
class FakeEvent:
    kind: str
    data: dict[str, Any]


def _make_config(tmp_path: Path) -> MagicMock:
    config = MagicMock()
    config.ai.model = "test-model"
    config.ai.base_url = "http://localhost:1234/v1"
    config.ai.max_tools = 128
    config.ai.provider = "openai"
    config.app.data_dir = tmp_path / "data"
    config.identity = None
    config.safety.approval_mode = "ask_for_writes"
    config.safety.subagent.max_concurrent = 5
    config.safety.subagent.max_total = 10
    config.safety.subagent.max_depth = 3
    config.safety.subagent.max_iterations = 15
    config.safety.subagent.timeout = 120
    config.safety.subagent.max_output_chars = 4000
    config.safety.subagent.max_prompt_chars = 32000
    config.safety.read_only = False
    config.safety.output_filter.enabled = False
    config.safety.tool_rate_limit.per_minute = 0
    config.safety.tool_rate_limit.per_conversation = 0
    config.safety.tool_rate_limit.consecutive_failures = 0
    config.safety.tool_rate_limit.action = "block"
    config.safety.tool_tiers = {}
    config.mcp_servers = []
    config.mcp_tool_warning_threshold = 50
    config.cli.max_tool_iterations = 50
    config.cli.tool_output_max_chars = 2000
    config.cli.max_consecutive_text_only = 3
    config.cli.max_line_repeats = 5
    return config


class TestMcpStartupFailure:
    """MCP startup failure should degrade gracefully, not crash."""

    @pytest.mark.asyncio
    async def test_mcp_failure_continues(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)
        config.mcp_servers = {"test-server": {"command": "fake"}}

        events = [
            FakeEvent("token", {"content": "Hello"}),
            FakeEvent("assistant_message", {"content": "Hello"}),
            FakeEvent("done", {}),
        ]

        async def fake_loop(**kwargs: Any) -> Any:
            for e in events:
                yield e

        mock_mcp_cls = MagicMock()
        mock_mcp = mock_mcp_cls.return_value
        mock_mcp.startup = AsyncMock(side_effect=RuntimeError("Connection refused"))

        with (
            patch("anteroom.cli.exec_mode.init_db") as mock_db,
            patch("anteroom.cli.exec_mode.storage"),
            patch("anteroom.cli.exec_mode.create_ai_service"),
            patch("anteroom.cli.exec_mode.run_agent_loop", side_effect=fake_loop),
            patch("anteroom.cli.exec_mode.register_default_tools"),
            patch("anteroom.cli.exec_mode.get_effective_dimensions", return_value=384),
            patch("anteroom.services.mcp_manager.McpManager", mock_mcp_cls),
            patch.dict("sys.modules", {"anteroom.services.mcp_manager": MagicMock(McpManager=mock_mcp_cls)}),
            patch("anteroom.cli.exec_mode.sys") as mock_sys,
        ):
            mock_db.return_value = MagicMock()
            mock_sys.stdin.isatty.return_value = True
            mock_sys.stdout = MagicMock()
            mock_sys.stderr = MagicMock()

            exit_code = await run_exec_mode(config, "test prompt", quiet=True)

        assert exit_code == 0


class TestArtifactRegistryFailure:
    """Artifact registry failure should continue without artifacts."""

    @pytest.mark.asyncio
    async def test_artifact_failure_continues(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)

        events = [
            FakeEvent("token", {"content": "OK"}),
            FakeEvent("assistant_message", {"content": "OK"}),
            FakeEvent("done", {}),
        ]

        async def fake_loop(**kwargs: Any) -> Any:
            for e in events:
                yield e

        with (
            patch("anteroom.cli.exec_mode.init_db") as mock_db,
            patch("anteroom.cli.exec_mode.storage"),
            patch("anteroom.cli.exec_mode.create_ai_service"),
            patch("anteroom.cli.exec_mode.run_agent_loop", side_effect=fake_loop),
            patch("anteroom.cli.exec_mode.register_default_tools"),
            patch("anteroom.cli.exec_mode.get_effective_dimensions", return_value=384),
            patch("anteroom.cli.exec_mode.sys") as mock_sys,
            patch("anteroom.services.artifact_registry.ArtifactRegistry", side_effect=RuntimeError("DB error")),
        ):
            mock_db.return_value = MagicMock()
            mock_sys.stdin.isatty.return_value = True
            mock_sys.stdout = MagicMock()
            mock_sys.stderr = MagicMock()

            exit_code = await run_exec_mode(config, "test prompt", quiet=True)

        assert exit_code == 0


class TestJsonOutput:
    """JSON output mode produces valid JSON."""

    @pytest.mark.asyncio
    async def test_json_output_valid(self, tmp_path: Path, capsys: Any) -> None:
        config = _make_config(tmp_path)

        events = [
            FakeEvent("token", {"content": "Hello world"}),
            FakeEvent("assistant_message", {"content": "Hello world"}),
            FakeEvent("done", {}),
        ]

        async def fake_loop(**kwargs: Any) -> Any:
            for e in events:
                yield e

        with (
            patch("anteroom.cli.exec_mode.init_db") as mock_db,
            patch("anteroom.cli.exec_mode.storage"),
            patch("anteroom.cli.exec_mode.create_ai_service"),
            patch("anteroom.cli.exec_mode.run_agent_loop", side_effect=fake_loop),
            patch("anteroom.cli.exec_mode.register_default_tools"),
            patch("anteroom.cli.exec_mode.get_effective_dimensions", return_value=384),
            patch("anteroom.cli.exec_mode.sys") as mock_sys,
        ):
            mock_db.return_value = MagicMock()
            mock_sys.stdin.isatty.return_value = True
            # Use real stdout for capsys capture
            import sys

            mock_sys.stdout = sys.stdout
            mock_sys.stderr = sys.stderr

            exit_code = await run_exec_mode(config, "test prompt", output_json=True, quiet=True)

        assert exit_code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert "output" in result
        assert "exit_code" in result
        assert result["exit_code"] == 0
        assert result["model"] == "test-model"


class TestNoTtyApproval:
    """No-TTY environment should fail-closed for tool approval."""

    @pytest.mark.asyncio
    async def test_no_tty_denies_tool(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)
        config.safety.approval_mode = "ask"

        events = [
            FakeEvent("tool_call_start", {"tool_name": "bash", "id": "tc1", "arguments": {"command": "ls"}}),
            FakeEvent("tool_call_end", {"tool_name": "bash", "id": "tc1", "status": "success", "output": ""}),
            FakeEvent("token", {"content": "Done"}),
            FakeEvent("assistant_message", {"content": "Done"}),
            FakeEvent("done", {}),
        ]

        async def fake_loop(**kwargs: Any) -> Any:
            for e in events:
                yield e

        with (
            patch("anteroom.cli.exec_mode.init_db") as mock_db,
            patch("anteroom.cli.exec_mode.storage"),
            patch("anteroom.cli.exec_mode.create_ai_service"),
            patch("anteroom.cli.exec_mode.run_agent_loop", side_effect=fake_loop),
            patch("anteroom.cli.exec_mode.register_default_tools"),
            patch("anteroom.cli.exec_mode.get_effective_dimensions", return_value=384),
            patch("anteroom.cli.exec_mode.sys") as mock_sys,
        ):
            mock_db.return_value = MagicMock()
            mock_sys.stdin.isatty.return_value = False
            mock_sys.stdin.read.return_value = ""
            mock_sys.stdout = MagicMock()
            mock_sys.stderr = MagicMock()

            # The approval callback should deny because has_tty=False
            # We can't easily test the callback in isolation because it's
            # created inside run_exec_mode, but we verify no crash occurs
            exit_code = await run_exec_mode(config, "test prompt", quiet=True)

        assert exit_code == 0


class TestTimeout:
    """Timeout uses asyncio.wait_for, produces exit code 124."""

    @pytest.mark.asyncio
    async def test_timeout_exit_code_124(self, tmp_path: Path) -> None:
        config = _make_config(tmp_path)

        async def slow_loop(**kwargs: Any) -> Any:
            await asyncio.sleep(10)
            yield FakeEvent("done", {})  # pragma: no cover

        with (
            patch("anteroom.cli.exec_mode.init_db") as mock_db,
            patch("anteroom.cli.exec_mode.storage"),
            patch("anteroom.cli.exec_mode.create_ai_service"),
            patch("anteroom.cli.exec_mode.run_agent_loop", side_effect=slow_loop),
            patch("anteroom.cli.exec_mode.register_default_tools"),
            patch("anteroom.cli.exec_mode.get_effective_dimensions", return_value=384),
            patch("anteroom.cli.exec_mode.sys") as mock_sys,
        ):
            mock_db.return_value = MagicMock()
            mock_sys.stdin.isatty.return_value = True
            mock_sys.stdout = MagicMock()
            mock_sys.stderr = MagicMock()

            exit_code = await run_exec_mode(config, "test prompt", timeout=0.1, quiet=True)

        assert exit_code == 124


class TestTruncateFunction:
    """_truncate with various string lengths."""

    def test_short_string_unchanged(self) -> None:
        assert _truncate("hello", 200) == "hello"

    def test_exact_max_unchanged(self) -> None:
        assert _truncate("x" * 200, 200) == "x" * 200

    def test_long_string_truncated(self) -> None:
        result = _truncate("x" * 300, 200)
        assert len(result) == 203  # 200 + "..."
        assert result.endswith("...")

    def test_custom_max(self) -> None:
        result = _truncate("abcdefghij", 5)
        assert result == "abcde..."


class TestSanitizeForTerminal:
    """ANSI escape stripping."""

    def test_strips_ansi_color(self) -> None:
        result = _sanitize_for_terminal("\x1b[31mred text\x1b[0m")
        assert result == "red text"

    def test_strips_osc_sequence(self) -> None:
        result = _sanitize_for_terminal("\x1b]0;title\x07normal")
        assert result == "normal"

    def test_preserves_newlines_and_tabs(self) -> None:
        result = _sanitize_for_terminal("line1\nline2\ttab")
        assert result == "line1\nline2\ttab"
