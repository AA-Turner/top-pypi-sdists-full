"""Integration tests for status tools with TaskResult contracts (#1316).

These tests exercise the full tool-call path through ToolRegistry.call_tool()
with mocked managers, verifying that TaskResult-shaped data flows correctly
through the tool dispatch and that the LLM trust boundary is enforced.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from anteroom.config import SafetyConfig
from anteroom.tools import ToolRegistry, register_default_tools


def _make_registry() -> ToolRegistry:
    """Build a ToolRegistry with default tools and auto-approval safety."""
    registry = ToolRegistry()
    config = SafetyConfig(approval_mode="auto")
    registry.set_safety_config(config)
    register_default_tools(registry)
    return registry


def _task_result_metadata(
    *,
    status: str = "completed",
    summary: str = "hello world",
    exit_code: int | None = 0,
    error: str | None = None,
    tool_calls: list[str] | None = None,
    output_pointer: str | None = "ptr-123",
    truncated: bool = False,
    duration_seconds: float = 1.5,
) -> dict[str, Any]:
    return {
        "task_result": {
            "status": status,
            "summary": summary,
            "exit_code": exit_code,
            "error": error,
            "tool_calls": tool_calls or [],
            "output_pointer": output_pointer,
            "truncated": truncated,
            "duration_seconds": duration_seconds,
        }
    }


# ---------------------------------------------------------------------------
# bash_background_status via ToolRegistry.call_tool()
# ---------------------------------------------------------------------------


class TestBashBackgroundStatusIntegration:
    """bash_background_status through the full tool dispatch path."""

    @pytest.mark.asyncio
    async def test_returns_task_result_fields(self) -> None:
        registry = _make_registry()
        bg_mgr = MagicMock()
        bg_mgr.get_task.return_value = {
            "id": "task-1",
            "command": "sleep 10",
            "status": "completed",
            "started_at": "2026-04-05T10:00:00",
            "completed_at": "2026-04-05T10:00:11",
            "metadata": _task_result_metadata(
                summary="done sleeping",
                exit_code=0,
                duration_seconds=10.1,
            ),
        }

        result = await registry.call_tool(
            "bash_background_status",
            {"task_id": "task-1"},
            _extra_context={"bg_manager": bg_mgr},
        )

        assert result["status"] == "completed"
        assert result["summary"] == "done sleeping"
        assert result["exit_code"] == 0
        assert result["duration_seconds"] == 10.1
        assert result["truncated"] is False
        assert result["error"] is None
        assert result["task_id"] == "task-1"
        assert result["command"] == "sleep 10"
        # Trust boundary: output_pointer must NOT appear in LLM response
        assert "output_pointer" not in result

    @pytest.mark.asyncio
    async def test_legacy_fallback_without_task_result(self) -> None:
        registry = _make_registry()
        bg_mgr = MagicMock()
        bg_mgr.get_task.return_value = {
            "id": "task-2",
            "command": "echo hi",
            "status": "running",
            "started_at": "2026-04-05T10:00:00",
            "completed_at": None,
            "exit_code": None,
            "stdout_preview": "hi\n",
            "stderr_preview": "",
            "metadata": {},
        }

        result = await registry.call_tool(
            "bash_background_status",
            {"task_id": "task-2"},
            _extra_context={"bg_manager": bg_mgr},
        )

        # Legacy shape: raw fields, no TaskResult keys
        assert result["status"] == "running"
        assert result["task_id"] == "task-2"
        assert result["stdout_preview"] == "hi\n"
        assert "summary" not in result
        assert "duration_seconds" not in result
        assert "output_pointer" not in result

    @pytest.mark.asyncio
    async def test_failed_task_result(self) -> None:
        registry = _make_registry()
        bg_mgr = MagicMock()
        bg_mgr.get_task.return_value = {
            "id": "task-3",
            "command": "false",
            "status": "completed",
            "started_at": "2026-04-05T10:00:00",
            "completed_at": "2026-04-05T10:00:01",
            "metadata": _task_result_metadata(
                status="failed",
                summary="",
                exit_code=1,
                error="Process exited with code 1",
                duration_seconds=0.5,
            ),
        }

        result = await registry.call_tool(
            "bash_background_status",
            {"task_id": "task-3"},
            _extra_context={"bg_manager": bg_mgr},
        )

        assert result["status"] == "failed"
        assert result["exit_code"] == 1
        assert result["error"] == "Process exited with code 1"
        assert "output_pointer" not in result

    @pytest.mark.asyncio
    async def test_no_manager_returns_error(self) -> None:
        registry = _make_registry()

        result = await registry.call_tool(
            "bash_background_status",
            {"task_id": "task-x"},
            _extra_context={},
        )

        assert "error" in result

    @pytest.mark.asyncio
    async def test_task_not_found_returns_error(self) -> None:
        registry = _make_registry()
        bg_mgr = MagicMock()
        bg_mgr.get_task.return_value = None

        result = await registry.call_tool(
            "bash_background_status",
            {"task_id": "task-ghost"},
            _extra_context={"bg_manager": bg_mgr},
        )

        assert "error" in result
        assert "not found" in result["error"]


# ---------------------------------------------------------------------------
# agent_run_status via ToolRegistry.call_tool()
# ---------------------------------------------------------------------------


class TestAgentRunStatusIntegration:
    """agent_run_status through the full tool dispatch path."""

    @pytest.mark.asyncio
    async def test_returns_task_result_fields(self) -> None:
        registry = _make_registry()
        detach_mgr = MagicMock()
        detach_mgr.get_run.return_value = {
            "id": "run-abc",
            "status": "completed",
            "title": "Summarize logs",
            "started_at": "2026-04-05T10:00:00",
            "completed_at": "2026-04-05T10:01:00",
            "duration_ms": 60000,
            "parent_run_id": None,
            "metadata": _task_result_metadata(
                summary="Found 3 errors",
                exit_code=None,
                tool_calls=["grep", "read_file"],
                output_pointer="run-abc",
                duration_seconds=59.5,
            ),
        }

        result = await registry.call_tool(
            "agent_run_status",
            {"run_id": "run-abc"},
            _extra_context={"detach_manager": detach_mgr},
        )

        assert result["status"] == "completed"
        assert result["summary"] == "Found 3 errors"
        assert result["tool_calls"] == ["grep", "read_file"]
        assert result["duration_seconds"] == 59.5
        assert result["run_id"] == "run-abc"
        assert result["title"] == "Summarize logs"
        # Trust boundary
        assert "output_pointer" not in result

    @pytest.mark.asyncio
    async def test_legacy_fallback_without_task_result(self) -> None:
        registry = _make_registry()
        detach_mgr = MagicMock()
        detach_mgr.get_run.return_value = {
            "id": "run-xyz",
            "status": "running",
            "title": "In progress",
            "started_at": "2026-04-05T10:00:00",
            "completed_at": None,
            "duration_ms": None,
            "parent_run_id": None,
            "metadata": {
                "output": "partial output here",
                "tool_calls_made": ["bash"],
            },
        }

        result = await registry.call_tool(
            "agent_run_status",
            {"run_id": "run-xyz"},
            _extra_context={"detach_manager": detach_mgr},
        )

        # Legacy shape
        assert result["status"] == "running"
        assert result["run_id"] == "run-xyz"
        assert result["output"] == "partial output here"
        assert result["tool_calls_made"] == ["bash"]
        assert "summary" not in result
        assert "duration_seconds" not in result
        assert "output_pointer" not in result

    @pytest.mark.asyncio
    async def test_failed_run_with_error(self) -> None:
        registry = _make_registry()
        detach_mgr = MagicMock()
        detach_mgr.get_run.return_value = {
            "id": "run-fail",
            "status": "completed",
            "title": "Broken task",
            "started_at": "2026-04-05T10:00:00",
            "completed_at": "2026-04-05T10:00:30",
            "duration_ms": 30000,
            "parent_run_id": "run-parent",
            "metadata": _task_result_metadata(
                status="failed",
                summary="",
                exit_code=None,
                error="Agent loop timed out",
                tool_calls=["bash", "read_file", "bash"],
                output_pointer="run-fail",
                duration_seconds=30.0,
            ),
        }

        result = await registry.call_tool(
            "agent_run_status",
            {"run_id": "run-fail"},
            _extra_context={"detach_manager": detach_mgr},
        )

        assert result["status"] == "failed"
        assert result["error"] == "Agent loop timed out"
        assert result["tool_calls"] == ["bash", "read_file", "bash"]
        assert result["parent_run_id"] == "run-parent"
        assert "output_pointer" not in result

    @pytest.mark.asyncio
    async def test_no_manager_returns_error(self) -> None:
        registry = _make_registry()

        result = await registry.call_tool(
            "agent_run_status",
            {"run_id": "run-x"},
            _extra_context={},
        )

        assert "error" in result

    @pytest.mark.asyncio
    async def test_run_not_found_returns_error(self) -> None:
        registry = _make_registry()
        detach_mgr = MagicMock()
        detach_mgr.get_run.return_value = None

        result = await registry.call_tool(
            "agent_run_status",
            {"run_id": "run-ghost"},
            _extra_context={"detach_manager": detach_mgr},
        )

        assert "error" in result
        assert "not found" in result["error"]
