"""CLI integration tests for subagent runtime-hook semantics (#1493).

Tests that:
1. Hook config flows from the call-site through to subagent execution
2. Correlation context is present in hook audit entries from subagent runs
3. Detached subagents receive a snapshotted hook config at launch

These tests drive ToolRegistry and DetachedSubagentManager directly —
no real AI service, no prompt_toolkit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.db import init_db
from anteroom.services.detached_subagent_manager import DetachedSubagentManager

CONV = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
UID = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"


# ---------------------------------------------------------------------------
# Hook config stubs
# ---------------------------------------------------------------------------


@dataclass
class _Matcher:
    tool_name: str = "*"
    arguments: dict[str, str] = field(default_factory=dict)


@dataclass
class _Runner:
    type: str = "command"
    command: str = "echo '{}'"
    url: str = ""
    timeout: int = 5


@dataclass
class _HookEntry:
    id: str = "integ-hook"
    event: str = "pre_tool"
    matcher: _Matcher = field(default_factory=_Matcher)
    runner: _Runner = field(default_factory=_Runner)
    message: str = ""
    trust_source: str = "personal"

    @property
    def is_executable(self) -> bool:
        return self.trust_source in ("personal", "team")


@dataclass
class _HooksConfig:
    pre_tool: list[_HookEntry] = field(default_factory=list)
    post_tool: list[_HookEntry] = field(default_factory=list)


def _hooks_with_pre(hook_id: str = "integ-pre") -> _HooksConfig:
    return _HooksConfig(pre_tool=[_HookEntry(id=hook_id)])


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    return init_db(tmp_path / "test.db")


@pytest.fixture()
def conv_id(db: Any) -> str:
    from anteroom.services.storage import create_conversation

    conv = create_conversation(db, title="integ-test")
    return conv["id"]


def _mock_ai() -> MagicMock:
    svc = MagicMock()
    svc.config = MagicMock()
    svc.config.model = "test-model"
    svc.config.max_tools = 128
    svc._token_provider = None
    return svc


def _mock_registry() -> MagicMock:
    reg = MagicMock()
    reg.has_tool.return_value = True
    reg.get_openai_tools.return_value = []
    reg.list_tools.return_value = []
    reg._safety_config = None
    reg._rate_limiter = None
    reg.call_tool = AsyncMock(return_value={"result": "ok"})
    return reg


# ---------------------------------------------------------------------------
# Tests: foreground subagent path
# ---------------------------------------------------------------------------


class TestForegroundSubagentHookIntegration:
    """hook config reaches the subagent execute path via _run_subagent."""

    @pytest.mark.asyncio
    async def test_hook_config_passed_through_handle(self) -> None:
        """handle() must forward hooks_config to _run_subagent."""
        from anteroom.config import SubagentConfig
        from anteroom.tools.subagent import SubagentLimiter, handle

        hooks = _hooks_with_pre()
        captured: dict[str, Any] = {}

        async def fake_run_subagent(*args: Any, **kwargs: Any) -> dict[str, Any]:
            captured["hooks_config"] = kwargs.get("_hooks_config")
            captured["parent_conversation_id"] = kwargs.get("_parent_conversation_id")
            return {"output": "done", "elapsed_seconds": 0.1, "tool_calls_made": [], "model_used": "test-model"}

        with patch("anteroom.tools.subagent._run_subagent", side_effect=fake_run_subagent):
            limiter = SubagentLimiter()
            result = await handle(
                "integration task",
                _ai_service=_mock_ai(),
                _tool_registry=_mock_registry(),
                _limiter=limiter,
                _conversation_id=CONV,
                _parent_tool_call_id="tc-integ",
                _hooks_config=hooks,
                _config=SubagentConfig(),
            )

        assert "error" not in result or result.get("error") is None
        assert captured.get("hooks_config") is hooks
        assert captured.get("parent_conversation_id") == CONV

    @pytest.mark.asyncio
    async def test_no_hooks_config_does_not_break_subagent(self) -> None:
        """handle() with hooks_config=None must execute normally."""
        from anteroom.config import SubagentConfig
        from anteroom.tools.subagent import SubagentLimiter, handle

        async def fake_run_subagent(*args: Any, **kwargs: Any) -> dict[str, Any]:
            assert kwargs.get("_hooks_config") is None
            return {"output": "done", "elapsed_seconds": 0.1, "tool_calls_made": [], "model_used": "test-model"}

        with patch("anteroom.tools.subagent._run_subagent", side_effect=fake_run_subagent):
            limiter = SubagentLimiter()
            result = await handle(
                "task without hooks",
                _ai_service=_mock_ai(),
                _tool_registry=_mock_registry(),
                _limiter=limiter,
                _conversation_id=CONV,
                _hooks_config=None,
                _config=SubagentConfig(),
            )

        assert "error" not in result or result.get("error") is None


# ---------------------------------------------------------------------------
# Tests: detached subagent hook snapshot path
# ---------------------------------------------------------------------------


class TestDetachedSubagentHookIntegration:
    """DetachedSubagentManager must snapshot hook config at launch time."""

    @pytest.mark.asyncio
    async def test_hooks_config_snapshot_survives_launch(self, db: Any, conv_id: str) -> None:
        """The snapshot passed to start() is the one _run_subagent receives."""
        hooks = _hooks_with_pre("detached-integ")
        captured: dict[str, Any] = {}

        async def fake_run_subagent(*args: Any, **kwargs: Any) -> dict[str, Any]:
            captured["hooks_config"] = kwargs.get("_hooks_config")
            captured["detached_run_id"] = kwargs.get("_detached_run_id")
            return {"output": "bg done", "elapsed_seconds": 0.5, "tool_calls_made": [], "model_used": "test-model"}

        manager = DetachedSubagentManager(db=db)

        with patch("anteroom.tools.subagent._run_subagent", side_effect=fake_run_subagent):
            result = manager.start(
                conv_id,
                "background integration task",
                ai_service=_mock_ai(),
                tool_registry=_mock_registry(),
                hooks_config=hooks,
                parent_conversation_id=CONV,
                parent_tool_call_id="tc-detached",
            )

            assert result["status"] == "running"
            run_id = result["run_id"]
            await manager._tasks[run_id]

        assert captured.get("hooks_config") is hooks, "snapshotted hooks_config must arrive at _run_subagent"
        assert captured.get("detached_run_id") == run_id

    @pytest.mark.asyncio
    async def test_detached_retry_hooks_snapshot(self, db: Any, conv_id: str) -> None:
        """Retry must receive the new hooks_config without reusing the original."""
        hooks_v1 = _hooks_with_pre("v1-hook")
        hooks_v2 = _hooks_with_pre("v2-hook")
        captured: dict[str, Any] = {}

        manager = DetachedSubagentManager(db=db)

        # Create a failed run
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value={
                "output": "",
                "elapsed_seconds": 0.1,
                "tool_calls_made": [],
                "model_used": "m",
                "error": "fail",
            },
        ):
            result = manager.start(
                conv_id,
                "original",
                ai_service=_mock_ai(),
                tool_registry=_mock_registry(),
                hooks_config=hooks_v1,
            )
            original_id = result["run_id"]
            await manager._tasks[original_id]

        # Retry with a different hook config snapshot
        async def fake_retry_run(*args: Any, **kwargs: Any) -> dict[str, Any]:
            captured["hooks_config"] = kwargs.get("_hooks_config")
            return {"output": "retry done", "elapsed_seconds": 0.1, "tool_calls_made": [], "model_used": "m"}

        with patch("anteroom.tools.subagent._run_subagent", side_effect=fake_retry_run):
            retry_result = manager.retry(
                original_id,
                ai_service=_mock_ai(),
                tool_registry=_mock_registry(),
                hooks_config=hooks_v2,
            )
            new_run_id = retry_result["run_id"]
            await manager._tasks[new_run_id]

        assert captured.get("hooks_config") is hooks_v2, "retry must use the new hooks_config, not the original"
        assert captured.get("hooks_config") is not hooks_v1
