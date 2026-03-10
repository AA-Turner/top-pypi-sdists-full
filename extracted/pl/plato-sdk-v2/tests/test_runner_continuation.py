"""Tests for AgentRunner (.with_continuation, continuation loop) and Workspace.mount_path."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from plato.agents.runner import AgentRunner
from plato.agents.runtime.base import AgentContext, PreparedAgent, Runtime
from plato.worlds.workspace import Workspace

# ---------------------------------------------------------------------------
# Helpers / fakes
# ---------------------------------------------------------------------------


class FakeRuntime(Runtime):
    """Minimal Runtime that records calls for assertions."""

    def __init__(self):
        self.prepare_calls: list[AgentContext] = []
        self.execute_calls: list[AgentContext] = []
        self.cleanup_calls: list[tuple[str, bool]] = []

    async def run(self, ctx: AgentContext) -> str:
        raise NotImplementedError

    async def prepare(self, ctx: AgentContext) -> PreparedAgent:
        self.prepare_calls.append(ctx)
        return PreparedAgent(agent_id="test-agent", hostname="10.0.0.1", runtime=self)

    async def execute(self, prepared: PreparedAgent, ctx: AgentContext) -> None:
        self.execute_calls.append(ctx)

    async def cleanup(self, agent_id: str, error: bool = False) -> None:
        self.cleanup_calls.append((agent_id, error))


def _make_agent_config():
    """Create a minimal AgentConfig-like mock."""
    cfg = MagicMock()
    cfg.image = "test:latest"
    cfg.config = {"key": "value"}
    cfg.runtime = MagicMock()
    cfg.runtime.model_dump.return_value = {"type": "docker"}
    return cfg


# ---------------------------------------------------------------------------
# Tests: Workspace.mount_path
# ---------------------------------------------------------------------------


class TestWorkspaceMountPoint:
    """Test the Workspace.mount_path property."""

    def test_mount_path_returns_explicit_value(self):
        ws = Workspace("code", Path("/workspace/code"), tracked=False, mount_path="/custom/code")
        assert ws.mount_path == "/custom/code"

    def test_mount_path_defaults_to_path_when_none(self):
        ws = Workspace("code", Path("/workspace/code"), tracked=False)
        assert ws.mount_path == "/workspace/code"

    def test_mount_path_defaults_to_data_subdir_when_tracked(self):
        ws = Workspace("code", Path("/workspace/code"), tracked=True)
        assert ws.mount_path == "/workspace/code/data"

    def test_mount_path_overrides_tracked_data_subdir(self):
        ws = Workspace("code", Path("/workspace/code"), tracked=True, mount_path="/workspace/code")
        assert ws.mount_path == "/workspace/code"


# ---------------------------------------------------------------------------
# Tests: with_continuation builder
# ---------------------------------------------------------------------------


class TestWithContinuationBuilder:
    """Test the builder method itself."""

    def test_returns_self(self):
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        async def cond():
            return True

        result = runner.with_continuation(exit_condition=cond)
        assert result is runner

    def test_sets_defaults(self):
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        async def cond():
            return True

        runner.with_continuation(exit_condition=cond)
        assert runner._exit_condition is cond
        assert runner._max_continuations == 2
        assert runner._continuation_instruction == "Continue. Complete all remaining work."

    def test_custom_values(self):
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        async def cond():
            return True

        runner.with_continuation(
            exit_condition=cond,
            max_continuations=5,
            continuation_instruction="Keep going!",
        )
        assert runner._max_continuations == 5
        assert runner._continuation_instruction == "Keep going!"


# ---------------------------------------------------------------------------
# Tests: run() without continuation (baseline behavior preserved)
# ---------------------------------------------------------------------------


class TestRunWithoutContinuation:
    """Ensure run() behaves identically to before when no continuation is set."""

    @pytest.mark.asyncio
    async def test_single_execution(self):
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        await runner.run("do something")

        assert len(runtime.prepare_calls) == 1
        assert len(runtime.execute_calls) == 1
        assert len(runtime.cleanup_calls) == 1
        assert runtime.cleanup_calls[0] == ("test-agent", False)

    @pytest.mark.asyncio
    async def test_instruction_passed_correctly(self):
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        await runner.run("do something specific")

        exec_ctx = runtime.execute_calls[0]
        assert exec_ctx.instruction == "do something specific"
        assert exec_ctx.config.get("continue_session") is not True

    @pytest.mark.asyncio
    async def test_display_name_passed_to_runtime_contexts(self):
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime, display_name="backend-builder")

        await runner.run("do something specific")

        assert runtime.prepare_calls[0].display_name == "backend-builder"
        assert runtime.execute_calls[0].display_name == "backend-builder"

    @pytest.mark.asyncio
    async def test_run_display_name_override_takes_precedence(self):
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime, display_name="default-name")

        await runner.run("do something specific", display_name="override-name")

        assert runtime.prepare_calls[0].display_name == "override-name"
        assert runtime.execute_calls[0].display_name == "override-name"

    @pytest.mark.asyncio
    async def test_cleanup_on_error(self):
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()

        async def failing_execute(prepared, ctx):
            raise RuntimeError("boom")

        runtime.execute = failing_execute
        runner = AgentRunner(agent_cfg, runtime)

        with pytest.raises(RuntimeError, match="boom"):
            await runner.run("do something")

        assert len(runtime.cleanup_calls) == 1
        assert runtime.cleanup_calls[0] == ("test-agent", True)


# ---------------------------------------------------------------------------
# Tests: run() with continuation loop
# ---------------------------------------------------------------------------


class TestRunWithContinuation:
    """Test the continuation loop behavior."""

    @pytest.mark.asyncio
    async def test_exit_condition_met_on_first_attempt(self):
        """When exit condition is True after first run, no continuation."""
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        call_count = 0

        async def always_true():
            nonlocal call_count
            call_count += 1
            return True

        runner.with_continuation(exit_condition=always_true)
        await runner.run("initial task")

        assert len(runtime.execute_calls) == 1
        assert call_count == 1
        # First attempt should NOT have continue_session
        assert runtime.execute_calls[0].config.get("continue_session") is not True
        assert runtime.execute_calls[0].instruction == "initial task"

    @pytest.mark.asyncio
    async def test_exit_condition_met_on_second_attempt(self):
        """Exit condition fails first, succeeds second → 2 executions."""
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        results = iter([False, True])

        async def condition():
            return next(results)

        runner.with_continuation(exit_condition=condition, max_continuations=3)
        await runner.run("initial task")

        assert len(runtime.execute_calls) == 2
        # First: original instruction, no continue
        assert runtime.execute_calls[0].instruction == "initial task"
        assert runtime.execute_calls[0].config.get("continue_session") is not True
        # Second: continuation instruction, with continue
        assert runtime.execute_calls[1].instruction == "Continue. Complete all remaining work."
        assert runtime.execute_calls[1].config.get("continue_session") is True

    @pytest.mark.asyncio
    async def test_max_continuations_exhausted(self):
        """Exit condition never met → runs 1 + max_continuations times."""
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        async def never_true():
            return False

        runner.with_continuation(exit_condition=never_true, max_continuations=2)
        await runner.run("initial task")

        # 1 initial + 2 continuations = 3 total
        assert len(runtime.execute_calls) == 3
        assert runtime.execute_calls[0].config.get("continue_session") is not True
        assert runtime.execute_calls[1].config.get("continue_session") is True
        assert runtime.execute_calls[2].config.get("continue_session") is True

    @pytest.mark.asyncio
    async def test_vm_prepared_once(self):
        """VM should only be prepared once regardless of continuations."""
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        async def never_true():
            return False

        runner.with_continuation(exit_condition=never_true, max_continuations=3)
        await runner.run("initial task")

        assert len(runtime.prepare_calls) == 1
        assert len(runtime.execute_calls) == 4  # 1 + 3
        assert len(runtime.cleanup_calls) == 1

    @pytest.mark.asyncio
    async def test_custom_continuation_instruction(self):
        """Custom continuation instruction should be used for retry attempts."""
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        results = iter([False, True])

        async def condition():
            return next(results)

        runner.with_continuation(
            exit_condition=condition,
            continuation_instruction="Please finish the work.",
        )
        await runner.run("initial task")

        assert runtime.execute_calls[1].instruction == "Please finish the work."

    @pytest.mark.asyncio
    async def test_cleanup_on_error_during_continuation(self):
        """If execute() raises during a continuation, cleanup with error=True."""
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        call_count = 0

        original_execute = runtime.execute

        async def execute_fails_on_second(prepared, ctx):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise RuntimeError("continuation failed")
            await original_execute(prepared, ctx)

        runtime.execute = execute_fails_on_second

        async def never_true():
            return False

        runner = AgentRunner(agent_cfg, runtime)
        runner.with_continuation(exit_condition=never_true, max_continuations=2)

        with pytest.raises(RuntimeError, match="continuation failed"):
            await runner.run("initial task")

        assert len(runtime.cleanup_calls) == 1
        assert runtime.cleanup_calls[0] == ("test-agent", True)

    @pytest.mark.asyncio
    async def test_post_run_hooks_run_after_loop(self):
        """Post-run hooks should execute after the entire continuation loop."""
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        hook_called = False

        async def post_hook(prepared):
            nonlocal hook_called
            hook_called = True
            # Should only be called once, after loop completes
            assert len(runtime.execute_calls) == 2

        results = iter([False, True])

        async def condition():
            return next(results)

        runner.with_continuation(exit_condition=condition)
        runner.on_post_run(post_hook)
        await runner.run("initial task")

        assert hook_called

    @pytest.mark.asyncio
    async def test_prepare_hooks_run_before_loop(self):
        """Prepare hooks should execute before the first execution."""
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        hook_called = False

        async def prep_hook(prepared):
            nonlocal hook_called
            hook_called = True
            assert len(runtime.execute_calls) == 0

        async def always_true():
            return True

        runner.with_continuation(exit_condition=always_true)
        runner.on_prepare(prep_hook)
        await runner.run("initial task")

        assert hook_called

    @pytest.mark.asyncio
    async def test_zero_max_continuations(self):
        """max_continuations=0 means only the initial run, no retries."""
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()
        runner = AgentRunner(agent_cfg, runtime)

        async def never_true():
            return False

        runner.with_continuation(exit_condition=never_true, max_continuations=0)
        await runner.run("initial task")

        assert len(runtime.execute_calls) == 1

    @pytest.mark.asyncio
    async def test_chaining_with_hooks(self):
        """Builder methods should be chainable."""
        agent_cfg = _make_agent_config()
        runtime = FakeRuntime()

        prepare_called = False
        post_called = False

        async def prep(p):
            nonlocal prepare_called
            prepare_called = True

        async def post(p):
            nonlocal post_called
            post_called = True

        async def always_true():
            return True

        runner = (
            AgentRunner(agent_cfg, runtime)
            .on_prepare(prep)
            .with_continuation(exit_condition=always_true)
            .on_post_run(post)
        )
        await runner.run("task")

        assert prepare_called
        assert post_called
        assert len(runtime.execute_calls) == 1
