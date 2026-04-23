"""Tests for runtime-hook semantics with subagents and detached agents (#1493).

Covers:
- Foreground subagents inherit resolved hook config from parent (no reload)
- Detached subagents snapshot hook config at launch time
- Subagent tool calls carry parent/child correlation context in hook dispatch
- Detached retries are correlated via parent_run_id without pretending to be
  the original run
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.config import SubagentConfig
from anteroom.services.agent_loop import AgentEvent
from anteroom.tools.subagent import SubagentLimiter, _run_subagent, handle

# ---------------------------------------------------------------------------
# Minimal config stubs — avoid importing the full AppConfig graph
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
class _Entry:
    id: str = "test-hook"
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
    pre_tool: list[_Entry] = field(default_factory=list)
    post_tool: list[_Entry] = field(default_factory=list)


def _empty_hooks() -> _HooksConfig:
    return _HooksConfig()


def _hooks_with_pre(hook_id: str = "pre-hook") -> _HooksConfig:
    return _HooksConfig(pre_tool=[_Entry(id=hook_id)])


def _hooks_with_post(hook_id: str = "post-hook") -> _HooksConfig:
    return _HooksConfig(post_tool=[_Entry(id=hook_id, event="post_tool")])


# ---------------------------------------------------------------------------
# AI / registry helpers
# ---------------------------------------------------------------------------


def _mock_ai_service() -> MagicMock:
    """Mock AIService that bypasses egress validation."""
    svc = MagicMock()
    svc.config = MagicMock()
    svc.config.model = "gpt-4"
    svc.config.max_tools = 128
    svc._token_provider = None
    return svc


def _mock_registry(*, has_tool: bool = True) -> MagicMock:
    reg = MagicMock()
    reg.has_tool.return_value = has_tool
    reg.get_openai_tools.return_value = []
    reg.list_tools.return_value = []
    reg._safety_config = None
    reg._rate_limiter = None
    reg.call_tool = AsyncMock(return_value={"result": "ok"})
    return reg


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


@pytest.fixture()
def conv_id(db: Any) -> str:
    from anteroom.services.storage import create_conversation

    conv = create_conversation(db, title="test")
    return conv["id"]


# ---------------------------------------------------------------------------
# Tests: hook config inheritance for foreground subagents
# ---------------------------------------------------------------------------


class TestForegroundHookInheritance:
    """Foreground subagents must receive the parent's resolved hook config."""

    @pytest.mark.asyncio
    async def test_hooks_config_passed_to_call_tool(self) -> None:
        """child_tool_executor must forward _hooks_config to call_tool."""
        hooks = _hooks_with_pre()
        registry = _mock_registry()
        captured: dict[str, Any] = {}

        async def fake_call_tool(
            tool_name: str,
            arguments: dict[str, Any],
            confirm_callback: Any = None,
            *,
            _hooks_config: Any = None,
            _audit_writer: Any = None,
            _extra_context: Any = None,
            **_kw: Any,
        ) -> dict[str, Any]:
            captured["hooks_config"] = _hooks_config
            captured["extra_context"] = _extra_context
            return {"result": "ok"}

        registry.call_tool = fake_call_tool

        # Use side_effect so the mock captures call kwargs and forwards tool_executor
        with (
            patch("anteroom.tools.subagent.AIService") as mock_ai_cls,
            patch("anteroom.tools.subagent.run_agent_loop") as mock_loop,
        ):
            mock_child_ai = MagicMock()
            mock_child_ai.client = AsyncMock()
            mock_ai_cls.return_value = mock_child_ai

            async def _loop_side_effect(**kwargs: Any) -> Any:
                tool_exec = kwargs.get("tool_executor")
                if tool_exec:
                    await tool_exec("read_file", {"path": "/tmp/x"})
                if False:
                    yield AgentEvent(kind="token", data={"content": "done"})

            mock_loop.side_effect = _loop_side_effect

            limiter = SubagentLimiter()
            await _run_subagent(
                prompt="do something",
                model=None,
                _ai_service=_mock_ai_service(),
                _tool_registry=registry,
                _cancel_event=asyncio.Event(),
                _depth=0,
                _event_sink=None,
                _agent_id="child-1",
                _parent_tool_call_id="tc-parent",
                _limiter=limiter,
                _hooks_config=hooks,
                _parent_conversation_id="conv-parent",
            )

        assert captured.get("hooks_config") is hooks, "hooks_config must be the parent's resolved config"

    @pytest.mark.asyncio
    async def test_correlation_context_passed_to_call_tool(self) -> None:
        """child_tool_executor must pass parent/child correlation IDs in extra_context."""
        registry = _mock_registry()
        captured: dict[str, Any] = {}

        async def fake_call_tool(
            tool_name: str,
            arguments: dict[str, Any],
            confirm_callback: Any = None,
            *,
            _hooks_config: Any = None,
            _audit_writer: Any = None,
            _extra_context: Any = None,
            **_kw: Any,
        ) -> dict[str, Any]:
            captured["extra_context"] = _extra_context
            return {"result": "ok"}

        registry.call_tool = fake_call_tool

        with (
            patch("anteroom.tools.subagent.AIService") as mock_ai_cls,
            patch("anteroom.tools.subagent.run_agent_loop") as mock_loop,
        ):
            mock_child_ai = MagicMock()
            mock_child_ai.client = AsyncMock()
            mock_ai_cls.return_value = mock_child_ai

            async def _loop_side_effect(**kwargs: Any) -> Any:
                tool_exec = kwargs.get("tool_executor")
                if tool_exec:
                    await tool_exec("read_file", {"path": "/tmp/x"})
                if False:
                    yield AgentEvent(kind="token", data={"content": ""})

            mock_loop.side_effect = _loop_side_effect

            limiter = SubagentLimiter()
            await _run_subagent(
                prompt="task",
                model=None,
                _ai_service=_mock_ai_service(),
                _tool_registry=registry,
                _cancel_event=asyncio.Event(),
                _depth=0,
                _event_sink=None,
                _agent_id="child-abc",
                _parent_tool_call_id="tc-999",
                _limiter=limiter,
                _hooks_config=_empty_hooks(),
                _parent_conversation_id="conv-xyz",
            )

        ctx = captured.get("extra_context") or {}
        assert ctx.get("parent_conversation_id") == "conv-xyz"
        assert ctx.get("parent_tool_call_id") == "tc-999"
        assert ctx.get("child_agent_id") == "child-abc"

    @pytest.mark.asyncio
    async def test_no_hooks_config_call_tool_still_works(self) -> None:
        """When hooks_config is None, child_tool_executor must not error."""
        registry = _mock_registry()

        with (
            patch("anteroom.tools.subagent.AIService") as mock_ai_cls,
            patch("anteroom.tools.subagent.run_agent_loop") as mock_loop,
        ):
            mock_child_ai = MagicMock()
            mock_child_ai.client = AsyncMock()
            mock_ai_cls.return_value = mock_child_ai

            async def _loop_side_effect(**kwargs: Any) -> Any:
                tool_exec = kwargs.get("tool_executor")
                if tool_exec:
                    await tool_exec("read_file", {"path": "/tmp/x"})
                if False:
                    yield AgentEvent(kind="token", data={"content": ""})

            mock_loop.side_effect = _loop_side_effect

            limiter = SubagentLimiter()
            result = await _run_subagent(
                prompt="task",
                model=None,
                _ai_service=_mock_ai_service(),
                _tool_registry=registry,
                _cancel_event=asyncio.Event(),
                _depth=0,
                _event_sink=None,
                _agent_id="child-1",
                _parent_tool_call_id="",
                _limiter=limiter,
                _hooks_config=None,
            )

        assert "error" not in result or result.get("error") is None

    @pytest.mark.asyncio
    async def test_nested_run_agent_inherits_hooks(self) -> None:
        """Nested run_agent calls inside a subagent must receive the same hooks_config."""
        hooks = _hooks_with_pre("parent-hook")
        registry = _mock_registry()
        captured_args: list[dict[str, Any]] = []

        async def fake_call_tool(
            tool_name: str,
            arguments: dict[str, Any],
            confirm_callback: Any = None,
            *,
            _hooks_config: Any = None,
            _audit_writer: Any = None,
            _extra_context: Any = None,
            **_kw: Any,
        ) -> dict[str, Any]:
            if tool_name == "run_agent":
                captured_args.append(
                    {
                        "hooks_config": arguments.get("_hooks_config"),
                        "audit_writer": arguments.get("_audit_writer"),
                    }
                )
            return {"output": "nested done", "elapsed_seconds": 0.1, "tool_calls_made": [], "model_used": "gpt-4"}

        registry.call_tool = fake_call_tool
        registry.has_tool.return_value = True

        with (
            patch("anteroom.tools.subagent.AIService") as mock_ai_cls,
            patch("anteroom.tools.subagent.run_agent_loop") as mock_loop,
        ):
            mock_child_ai = MagicMock()
            mock_child_ai.client = AsyncMock()
            mock_ai_cls.return_value = mock_child_ai

            async def _loop_side_effect(**kwargs: Any) -> Any:
                tool_exec = kwargs.get("tool_executor")
                if tool_exec:
                    await tool_exec("run_agent", {"prompt": "nested task"})
                if False:
                    yield AgentEvent(kind="token", data={"content": ""})

            mock_loop.side_effect = _loop_side_effect

            limiter = SubagentLimiter()
            await _run_subagent(
                prompt="parent task",
                model=None,
                _ai_service=_mock_ai_service(),
                _tool_registry=registry,
                _cancel_event=asyncio.Event(),
                _depth=0,
                _event_sink=None,
                _agent_id="parent",
                _parent_tool_call_id="tc-root",
                _limiter=limiter,
                _hooks_config=hooks,
                _parent_conversation_id="conv-root",
            )

        assert len(captured_args) == 1, "nested run_agent should have been called once"
        assert captured_args[0]["hooks_config"] is hooks, "nested subagent must inherit the same hooks_config"


# ---------------------------------------------------------------------------
# Tests: hook config snapshotting for detached subagents
# ---------------------------------------------------------------------------


class TestDetachedHookSnapshot:
    """Detached subagents must snapshot hook config at launch time."""

    @pytest.mark.asyncio
    async def test_hooks_config_snapshot_passed_to_run_subagent(self, db: Any, conv_id: str) -> None:
        """DetachedSubagentManager.start must pass hooks_config to _run_subagent."""
        from anteroom.services.detached_subagent_manager import DetachedSubagentManager

        hooks = _hooks_with_pre("detached-hook")
        captured: dict[str, Any] = {}

        async def fake_run_subagent(*args: Any, **kwargs: Any) -> dict[str, Any]:
            captured["hooks_config"] = kwargs.get("_hooks_config")
            captured["detached_run_id"] = kwargs.get("_detached_run_id")
            captured["parent_conversation_id"] = kwargs.get("_parent_conversation_id")
            captured["parent_tool_call_id"] = kwargs.get("_parent_tool_call_id")
            return {"output": "done", "elapsed_seconds": 0.1, "tool_calls_made": [], "model_used": "gpt-4"}

        manager = DetachedSubagentManager(db=db)

        with patch("anteroom.tools.subagent._run_subagent", side_effect=fake_run_subagent):
            result = manager.start(
                conv_id,
                "do background work",
                ai_service=_mock_ai_service(),
                tool_registry=_mock_registry(),
                hooks_config=hooks,
                parent_conversation_id="conv-parent",
                parent_tool_call_id="tc-launch",
            )
            assert result["status"] == "running"
            collector = manager._tasks[result["run_id"]]
            await collector

        assert captured.get("hooks_config") is hooks, "snapshot must be the config passed at launch"
        assert captured.get("detached_run_id") == result["run_id"], "detached_run_id must be set"
        assert captured.get("parent_conversation_id") == "conv-parent"
        assert captured.get("parent_tool_call_id") == "tc-launch"

    @pytest.mark.asyncio
    async def test_hooks_config_none_is_forwarded(self, db: Any, conv_id: str) -> None:
        """When hooks_config=None at launch, _run_subagent receives None."""
        from anteroom.services.detached_subagent_manager import DetachedSubagentManager

        captured: dict[str, Any] = {}

        async def fake_run_subagent(*args: Any, **kwargs: Any) -> dict[str, Any]:
            captured["hooks_config"] = kwargs.get("_hooks_config")
            return {"output": "done", "elapsed_seconds": 0.1, "tool_calls_made": [], "model_used": "gpt-4"}

        manager = DetachedSubagentManager(db=db)

        with patch("anteroom.tools.subagent._run_subagent", side_effect=fake_run_subagent):
            result = manager.start(
                conv_id,
                "task",
                ai_service=_mock_ai_service(),
                tool_registry=_mock_registry(),
                hooks_config=None,
            )
            collector = manager._tasks[result["run_id"]]
            await collector

        assert captured.get("hooks_config") is None

    @pytest.mark.asyncio
    async def test_retry_passes_hooks_config(self, db: Any, conv_id: str) -> None:
        """DetachedSubagentManager.retry must forward hooks_config snapshot."""
        from anteroom.services.detached_subagent_manager import DetachedSubagentManager

        hooks = _hooks_with_post("retry-hook")
        captured: dict[str, Any] = {}

        async def fake_run_subagent(*args: Any, **kwargs: Any) -> dict[str, Any]:
            captured["hooks_config"] = kwargs.get("_hooks_config")
            captured["detached_run_id"] = kwargs.get("_detached_run_id")
            return {"output": "retried", "elapsed_seconds": 0.1, "tool_calls_made": [], "model_used": "gpt-4"}

        manager = DetachedSubagentManager(db=db)

        # Create a real failed run to retry
        with patch("anteroom.tools.subagent._run_subagent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = {
                "output": "",
                "elapsed_seconds": 0.1,
                "tool_calls_made": [],
                "model_used": "gpt-4",
                "error": "initial failure",
            }
            result = manager.start(
                conv_id,
                "original task",
                ai_service=_mock_ai_service(),
                tool_registry=_mock_registry(),
            )
            original_run_id = result["run_id"]
            collector = manager._tasks[original_run_id]
            await collector

        # Now retry with hooks_config
        with patch("anteroom.tools.subagent._run_subagent", side_effect=fake_run_subagent):
            retry_result = manager.retry(
                original_run_id,
                ai_service=_mock_ai_service(),
                tool_registry=_mock_registry(),
                hooks_config=hooks,
            )
            assert retry_result["status"] == "running"
            new_run_id = retry_result["run_id"]
            collector = manager._tasks[new_run_id]
            await collector

        assert captured.get("hooks_config") is hooks, "retry must forward hooks_config snapshot"
        assert captured.get("detached_run_id") == new_run_id, "retry run uses its own new run_id"


# ---------------------------------------------------------------------------
# Tests: handle() — public entry point hook wiring
# ---------------------------------------------------------------------------


class TestHandleHookWiring:
    @pytest.mark.asyncio
    async def test_detached_start_receives_hooks_config(self) -> None:
        """handle() with detach=True must pass hooks_config to detach_manager.start."""
        hooks = _hooks_with_pre()
        captured: dict[str, Any] = {}

        detach_manager = MagicMock()

        def fake_start(
            conv_id: str,
            prompt: str,
            *,
            hooks_config: Any = None,
            parent_conversation_id: str = "",
            parent_tool_call_id: str = "",
            **_kw: Any,
        ) -> dict[str, Any]:
            captured["hooks_config"] = hooks_config
            captured["parent_conversation_id"] = parent_conversation_id
            captured["parent_tool_call_id"] = parent_tool_call_id
            return {"run_id": "run-detached", "status": "running", "prompt": prompt[:80]}

        detach_manager.start = fake_start

        result = await handle(
            "fire-and-forget work",
            _ai_service=_mock_ai_service(),
            _tool_registry=_mock_registry(),
            _detach=True,
            _detach_manager=detach_manager,
            _conversation_id="conv-abc",
            _parent_tool_call_id="tc-launch",
            _hooks_config=hooks,
        )

        assert result.get("run_id") == "run-detached"
        assert captured.get("hooks_config") is hooks
        assert captured.get("parent_tool_call_id") == "tc-launch"
        assert captured.get("parent_conversation_id") == "conv-abc"

    @pytest.mark.asyncio
    async def test_foreground_subagent_hooks_config_forwarded(self) -> None:
        """handle() foreground path must forward _hooks_config to _run_subagent."""
        hooks = _hooks_with_pre()
        registry = _mock_registry()
        captured: dict[str, Any] = {}

        with patch("anteroom.tools.subagent._run_subagent") as mock_run:

            async def fake_run(*args: Any, **kwargs: Any) -> dict[str, Any]:
                captured["hooks_config"] = kwargs.get("_hooks_config")
                captured["parent_conversation_id"] = kwargs.get("_parent_conversation_id")
                return {"output": "done", "elapsed_seconds": 0.1, "tool_calls_made": [], "model_used": "gpt-4"}

            mock_run.side_effect = fake_run

            limiter = SubagentLimiter()
            await handle(
                "foreground task",
                _ai_service=_mock_ai_service(),
                _tool_registry=registry,
                _limiter=limiter,
                _conversation_id="conv-fg",
                _parent_tool_call_id="tc-fg",
                _hooks_config=hooks,
                _config=SubagentConfig(),
            )

        assert captured.get("hooks_config") is hooks
        assert captured.get("parent_conversation_id") == "conv-fg"


# ---------------------------------------------------------------------------
# Tests: correlation IDs in hook dispatch
# ---------------------------------------------------------------------------


class TestHookCorrelationContext:
    @pytest.mark.asyncio
    async def test_run_pre_tool_hooks_passes_correlation_fields(self) -> None:
        """run_pre_tool_hooks must forward subagent correlation fields to _run_single_hook."""
        from anteroom.services.hooks import run_pre_tool_hooks

        hooks_cfg = _hooks_with_pre("corr-hook")
        captured: dict[str, Any] = {}

        with patch("anteroom.services.hooks._run_single_hook") as mock_single:
            from anteroom.services.hooks import _ALLOW

            async def fake_single(entry: Any, *args: Any, **kwargs: Any) -> Any:
                captured.update(kwargs)
                return _ALLOW

            mock_single.side_effect = fake_single

            await run_pre_tool_hooks(
                hooks_cfg,
                "read_file",
                {"path": "/tmp/x"},
                parent_conversation_id="conv-parent",
                parent_tool_call_id="tc-parent",
                child_agent_id="child-1",
                detached_run_id="run-det-1",
            )

        assert captured.get("parent_conversation_id") == "conv-parent"
        assert captured.get("parent_tool_call_id") == "tc-parent"
        assert captured.get("child_agent_id") == "child-1"
        assert captured.get("detached_run_id") == "run-det-1"

    @pytest.mark.asyncio
    async def test_run_post_tool_hooks_passes_correlation_fields(self) -> None:
        """run_post_tool_hooks must forward subagent correlation fields to _run_single_hook."""
        from anteroom.services.hooks import run_post_tool_hooks

        hooks_cfg = _hooks_with_post("corr-post-hook")
        captured: dict[str, Any] = {}

        with patch("anteroom.services.hooks._run_single_hook") as mock_single:
            from anteroom.services.hooks import _ALLOW

            async def fake_single(entry: Any, *args: Any, **kwargs: Any) -> Any:
                captured.update(kwargs)
                return _ALLOW

            mock_single.side_effect = fake_single

            await run_post_tool_hooks(
                hooks_cfg,
                "write_file",
                {"path": "/tmp/out", "content": "hello"},
                {"result": "ok"},
                parent_conversation_id="conv-p",
                parent_tool_call_id="tc-p",
                child_agent_id="child-2",
                detached_run_id="run-det-2",
            )

        assert captured.get("parent_conversation_id") == "conv-p"
        assert captured.get("parent_tool_call_id") == "tc-p"
        assert captured.get("child_agent_id") == "child-2"
        assert captured.get("detached_run_id") == "run-det-2"

    def test_build_hook_env_includes_correlation_fields(self) -> None:
        """_build_hook_env must include subagent correlation env vars when set."""
        from anteroom.services.hooks import _build_hook_env

        env = _build_hook_env(
            "pre_tool",
            "bash",
            {"command": "ls"},
            parent_conversation_id="conv-x",
            parent_tool_call_id="tc-x",
            child_agent_id="child-x",
            detached_run_id="run-x",
        )

        assert env["ANTEROOM_HOOK_PARENT_CONVERSATION_ID"] == "conv-x"
        assert env["ANTEROOM_HOOK_PARENT_TOOL_CALL_ID"] == "tc-x"
        assert env["ANTEROOM_HOOK_CHILD_AGENT_ID"] == "child-x"
        assert env["ANTEROOM_HOOK_DETACHED_RUN_ID"] == "run-x"

    def test_build_hook_env_omits_empty_correlation_fields(self) -> None:
        """_build_hook_env must not include correlation env vars when empty."""
        from anteroom.services.hooks import _build_hook_env

        env = _build_hook_env("pre_tool", "bash", {"command": "ls"})

        assert "ANTEROOM_HOOK_PARENT_CONVERSATION_ID" not in env
        assert "ANTEROOM_HOOK_PARENT_TOOL_CALL_ID" not in env
        assert "ANTEROOM_HOOK_CHILD_AGENT_ID" not in env
        assert "ANTEROOM_HOOK_DETACHED_RUN_ID" not in env

    def test_build_hook_payload_includes_correlation_fields(self) -> None:
        """_build_hook_payload must include subagent correlation fields when set."""
        from anteroom.services.hooks import _build_hook_payload

        payload = _build_hook_payload(
            "post_tool",
            "write_file",
            {"path": "/tmp/f"},
            {"result": "ok"},
            parent_conversation_id="conv-y",
            child_agent_id="child-y",
            detached_run_id="run-y",
        )

        assert payload["parent_conversation_id"] == "conv-y"
        assert payload["child_agent_id"] == "child-y"
        assert payload["detached_run_id"] == "run-y"

    def test_build_hook_payload_omits_empty_correlation_fields(self) -> None:
        """_build_hook_payload must not include correlation fields when empty."""
        from anteroom.services.hooks import _build_hook_payload

        payload = _build_hook_payload("pre_tool", "read_file", {"path": "/tmp/f"})

        assert "parent_conversation_id" not in payload
        assert "parent_tool_call_id" not in payload
        assert "child_agent_id" not in payload
        assert "detached_run_id" not in payload

    @pytest.mark.asyncio
    async def test_detached_run_id_in_hook_audit(self) -> None:
        """Hook audit entries from a detached run must include detached_run_id."""
        from anteroom.services.lineage import emit_hook_lifecycle

        audit_writer = MagicMock()
        emitted: list[Any] = []
        audit_writer.is_event_enabled.return_value = True
        audit_writer.emit = lambda entry: emitted.append(entry)

        emit_hook_lifecycle(
            audit_writer,
            "completed",
            hook_id="h-1",
            hook_event="pre_tool",
            tool_name="bash",
            outcome="allow",
            details={"detached_run_id": "run-det", "child_agent_id": "child-det"},
        )

        assert len(emitted) == 1
        details = emitted[0].details
        assert details.get("detached_run_id") == "run-det"
        assert details.get("child_agent_id") == "child-det"


# ---------------------------------------------------------------------------
# Tests: MCP hook 'ask' outcome blocks in subagent (no approval channel)
# ---------------------------------------------------------------------------


class TestMcpHookAskOutcomeInSubagent:
    """MCP pre-tool hook returning 'ask' must block rather than silently allow
    in subagent context where no confirm_callback is available (#1493)."""

    @pytest.mark.asyncio
    async def test_mcp_pre_hook_ask_blocks_when_no_callback(self) -> None:
        """When a pre-tool hook returns 'ask' for an MCP tool in a subagent,
        the call must be blocked — not silently allowed."""
        from anteroom.services.hooks import HookDecision

        hooks = _HooksConfig(pre_tool=[_Entry(id="ask-hook")])
        # Registry has no MCP-named tool; has_tool returns False for the MCP tool.
        # check_safety returns None so the safety gate auto-allows (we test hook path).
        registry = _mock_registry(has_tool=False)
        registry.check_safety.return_value = None
        mcp_manager = MagicMock()
        mcp_manager.call_tool = AsyncMock(return_value={"result": "mcp-ok"})

        captured_result: dict[str, Any] = {}

        with (
            patch("anteroom.tools.subagent.AIService") as mock_ai_cls,
            patch("anteroom.tools.subagent.run_agent_loop") as mock_loop,
            patch("anteroom.services.hooks.run_pre_tool_hooks", new=AsyncMock()) as mock_pre,
        ):
            mock_child_ai = MagicMock()
            mock_child_ai.client = AsyncMock()
            mock_ai_cls.return_value = mock_child_ai

            # Hook returns 'ask'
            mock_pre.return_value = HookDecision(outcome="ask", message="human review needed", hook_id="ask-hook")

            async def _loop_side_effect(**kwargs: Any) -> Any:
                tool_exec = kwargs.get("tool_executor")
                if tool_exec:
                    result = await tool_exec("some_mcp_tool", {"param": "value"})
                    captured_result.update(result)
                if False:
                    yield AgentEvent(kind="token", data={"content": ""})

            mock_loop.side_effect = _loop_side_effect

            limiter = SubagentLimiter()
            await _run_subagent(
                prompt="task",
                model=None,
                _ai_service=_mock_ai_service(),
                _tool_registry=registry,
                _mcp_manager=mcp_manager,
                _cancel_event=asyncio.Event(),
                _depth=0,
                _event_sink=None,
                _agent_id="child-ask",
                _parent_tool_call_id="tc-ask",
                _limiter=limiter,
                _hooks_config=hooks,
                _confirm_callback=None,
            )

        # The MCP tool must NOT have been called
        mcp_manager.call_tool.assert_not_awaited()
        # The result must indicate the tool was blocked
        assert captured_result.get("hook_blocked") is True, (
            "MCP hook 'ask' with no confirm_callback must return hook_blocked=True"
        )

    @pytest.mark.asyncio
    async def test_mcp_pre_hook_deny_blocks(self) -> None:
        """Sanity: MCP pre-tool hook returning 'deny' must block the tool."""
        from anteroom.services.hooks import HookDecision

        hooks = _HooksConfig(pre_tool=[_Entry(id="deny-hook")])
        registry = _mock_registry(has_tool=False)
        registry.check_safety.return_value = None
        mcp_manager = MagicMock()
        mcp_manager.call_tool = AsyncMock(return_value={"result": "mcp-ok"})

        captured_result: dict[str, Any] = {}

        with (
            patch("anteroom.tools.subagent.AIService") as mock_ai_cls,
            patch("anteroom.tools.subagent.run_agent_loop") as mock_loop,
            patch("anteroom.services.hooks.run_pre_tool_hooks", new=AsyncMock()) as mock_pre,
        ):
            mock_child_ai = MagicMock()
            mock_child_ai.client = AsyncMock()
            mock_ai_cls.return_value = mock_child_ai

            mock_pre.return_value = HookDecision(outcome="deny", message="blocked by hook", hook_id="deny-hook")

            async def _loop_side_effect(**kwargs: Any) -> Any:
                tool_exec = kwargs.get("tool_executor")
                if tool_exec:
                    result = await tool_exec("some_mcp_tool", {"param": "value"})
                    captured_result.update(result)
                if False:
                    yield AgentEvent(kind="token", data={"content": ""})

            mock_loop.side_effect = _loop_side_effect

            limiter = SubagentLimiter()
            await _run_subagent(
                prompt="task",
                model=None,
                _ai_service=_mock_ai_service(),
                _tool_registry=registry,
                _mcp_manager=mcp_manager,
                _cancel_event=asyncio.Event(),
                _depth=0,
                _event_sink=None,
                _agent_id="child-deny",
                _parent_tool_call_id="",
                _limiter=limiter,
                _hooks_config=hooks,
                _confirm_callback=None,
            )

        mcp_manager.call_tool.assert_not_awaited()
        assert captured_result.get("hook_blocked") is True
