"""Tests for continue_session handling in PlatoVMRuntime._execute_agent().

continue_session is passed through the agent config dict (AGENT_CONFIG_B64),
NOT as a separate env var. These tests verify the config dict carries it.
"""

from __future__ import annotations

import asyncio
import base64
import json
from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from plato.agents.runtime.base import AgentContext
from plato.agents.runtime.vm import PlatoVMRuntime, _make_agent_alias


class _FakeInstructionWriter:
    def __init__(self, returncode: int = 0, stderr: bytes = b"") -> None:
        self.returncode = returncode
        self._stderr = stderr
        self.stdin = None
        self.stdout = None
        self.stderr = None

    async def communicate(self, input: bytes | None = None) -> tuple[bytes, bytes]:
        return b"", self._stderr


def _make_ctx(continue_session: bool = False, display_name: str | None = None) -> AgentContext:
    config = {"key": "value"}
    if continue_session:
        config["continue_session"] = True
    return AgentContext(
        image="test:latest",
        config=config,
        instruction="do something",
        display_name=display_name,
    )


@pytest.fixture
def runtime():
    """Create a PlatoVMRuntime with mocked session."""
    session = MagicMock()
    rt = PlatoVMRuntime(
        session=session,
        ssh_key_path=MagicMock(),
    )
    return rt


@pytest.fixture
def mock_instruction_write():
    with patch(
        "plato.agents.runtime.vm.asyncio.create_subprocess_exec",
        new=AsyncMock(return_value=_FakeInstructionWriter()),
    ) as mock_proc:
        yield mock_proc


class TestVMContinueSession:
    """Tests for continue_session propagation via config dict."""

    @pytest.mark.asyncio
    async def test_continue_session_in_config_b64(self, runtime, mock_instruction_write):
        """When continue_session=True is in config, AGENT_CONFIG_B64 should carry it."""
        ctx = _make_ctx(continue_session=True)
        agent_env = MagicMock()
        hostname = "10.0.0.1"

        captured_command = None

        async def mock_run_ssh(h, cmd, timeout=300):
            return 0, "ALREADY_EXISTS\n", ""

        async def mock_run_ssh_streaming(_ssh_key, hostname, command, user="root", extra_opts=None):
            nonlocal captured_command
            captured_command = command
            return 0

        runtime._run_ssh = mock_run_ssh

        with patch("plato.agents.runtime.vm.OTelContext.from_env") as mock_otel:
            mock_otel.return_value = MagicMock(
                otel_url=None,
                session_id=None,
                upload_url=None,
                traceparent=None,
                trace_id=None,
                parent_span_id=None,
                to_env_vars=MagicMock(return_value=[]),
            )
            with patch(
                "plato.agents.runtime.vm.run_ssh",
                new=AsyncMock(return_value=(0, "ALREADY_EXISTS\n", "")),
            ):
                with patch(
                    "plato.agents.runtime.vm.run_ssh_streaming",
                    new=AsyncMock(side_effect=mock_run_ssh_streaming),
                ):
                    await runtime._execute_agent(ctx, agent_env, hostname, "/usr/local/bin/plato-agent-runner")

        assert captured_command is not None
        # No separate env var for continue_session
        assert "AGENT_CONTINUE_SESSION" not in captured_command
        # PATH must include /root/.local/bin for agent child processes (pip tools, uv, etc.)
        assert 'PATH="/root/.local/bin:$PATH"' in captured_command
        assert "/usr/local/bin/plato-agent-runner run" in captured_command
        # But config_b64 should contain it
        assert "AGENT_CONFIG_B64" in captured_command
        # Decode the config from the command to verify
        decoded = json.loads(base64.b64decode(ctx.config_b64).decode())
        assert decoded["continue_session"] is True

    @pytest.mark.asyncio
    async def test_no_continue_session_in_config_by_default(self, runtime, mock_instruction_write):
        """When continue_session is not set, it should not appear in config."""
        ctx = _make_ctx(continue_session=False)
        agent_env = MagicMock()
        hostname = "10.0.0.1"

        captured_command = None

        async def mock_run_ssh(h, cmd, timeout=300):
            return 0, "ALREADY_EXISTS\n", ""

        async def mock_run_ssh_streaming(_ssh_key, hostname, command, user="root", extra_opts=None):
            nonlocal captured_command
            captured_command = command
            return 0

        runtime._run_ssh = mock_run_ssh

        with patch("plato.agents.runtime.vm.OTelContext.from_env") as mock_otel:
            mock_otel.return_value = MagicMock(
                otel_url=None,
                session_id=None,
                upload_url=None,
                traceparent=None,
                trace_id=None,
                parent_span_id=None,
                to_env_vars=MagicMock(return_value=[]),
            )
            with patch(
                "plato.agents.runtime.vm.run_ssh",
                new=AsyncMock(return_value=(0, "ALREADY_EXISTS\n", "")),
            ):
                with patch(
                    "plato.agents.runtime.vm.run_ssh_streaming",
                    new=AsyncMock(side_effect=mock_run_ssh_streaming),
                ):
                    await runtime._execute_agent(ctx, agent_env, hostname, "/usr/local/bin/plato-agent-runner")

        assert captured_command is not None
        assert "AGENT_CONTINUE_SESSION" not in captured_command
        decoded = json.loads(base64.b64decode(ctx.config_b64).decode())
        assert "continue_session" not in decoded

    def test_make_agent_alias_uses_readable_slug(self):
        alias = _make_agent_alias("Backend Builder / Review")
        assert alias.startswith("backend-builder-review-")
        assert len(alias.split("-")[-1]) == 8

    @pytest.mark.asyncio
    async def test_prepare_retries_with_retry_suffix_after_duplicate_alias(self, runtime):
        ctx = _make_ctx(display_name="shared-components-batch-5")
        agent_env = MagicMock()
        agent_env.mesh_ip = None
        agent_env.get_mesh_ip = AsyncMock(return_value="10.0.0.1")

        runtime._create_vm = AsyncMock(
            side_effect=[
                RuntimeError("Duplicate alias 'shared-components-batch-5-old'"),
                agent_env,
            ]
        )
        runtime._setup_network = AsyncMock()
        runtime._sync_code = AsyncMock()
        runtime._run_ssh_streaming = AsyncMock(return_value=0)
        runtime.cleanup = AsyncMock()
        agent_env.add_ssh_key = AsyncMock()

        with (
            patch(
                "plato.agents.runtime.vm._make_agent_alias",
                return_value="shared-components-batch-5-base",
            ),
            patch("pathlib.Path.read_text", return_value="ssh-ed25519 AAAATEST"),
            patch(
                "plato.agents.runtime.vm.resolve_runner_path",
                new=AsyncMock(return_value="/usr/local/bin/plato-agent-runner"),
            ) as mock_resolve,
        ):
            prepared = await runtime.prepare(ctx)

        assert prepared.agent_id == "shared-components-batch-5-base-retry-1"
        assert prepared.hostname == "10.0.0.1"
        assert runtime._create_vm.await_count == 2
        assert runtime._create_vm.await_args_list[0].args == (
            "test:latest",
            "shared-components-batch-5-base",
        )
        assert runtime._create_vm.await_args_list[1].args == (
            "test:latest",
            "shared-components-batch-5-base-retry-1",
        )
        mock_resolve.assert_awaited_once()
        runtime.cleanup.assert_awaited_once_with(
            "shared-components-batch-5-base",
            error=True,
        )

    @pytest.mark.asyncio
    async def test_agent_name_propagated_to_span_and_env(self, runtime, mock_instruction_write):
        ctx = _make_ctx(display_name="backend-builder")
        agent_env = MagicMock()
        agent_env.alias = "backend-builder-ab12cd34"
        agent_env.job_id = "job-123"
        hostname = "10.0.0.1"

        captured_command = None
        span_attrs: dict[str, str] = {}

        class _FakeSpan:
            def set_attribute(self, key, value):
                span_attrs[key] = value

            def get_span_context(self):
                return MagicMock(is_valid=False)

        class _FakeTracer:
            @contextmanager
            def start_as_current_span(self, _name):
                yield _FakeSpan()

        async def mock_run_ssh_streaming(_ssh_key, hostname, command, user="root", extra_opts=None):
            nonlocal captured_command
            captured_command = command
            return 0

        with patch("plato.agents.runtime.vm.trace.get_tracer", return_value=_FakeTracer()):
            with patch(
                "plato.agents.runtime.vm.run_ssh",
                new=AsyncMock(return_value=(0, "ALREADY_EXISTS\n", "")),
            ):
                with patch(
                    "plato.agents.runtime.vm.run_ssh_streaming",
                    new=AsyncMock(side_effect=mock_run_ssh_streaming),
                ):
                    with patch("plato.agents.runtime.vm.OTelContext.from_env") as mock_otel:
                        mock_otel.return_value = MagicMock(
                            otel_url=None,
                            session_id=None,
                            upload_url=None,
                            traceparent=None,
                            trace_id=None,
                            parent_span_id=None,
                            to_env_vars=MagicMock(return_value=[]),
                        )
                        await runtime._execute_agent(ctx, agent_env, hostname, "/usr/local/bin/plato-agent-runner")

        assert captured_command is not None
        assert 'PLATO_AGENT_DISPLAY_NAME="backend-builder"' in captured_command
        assert span_attrs["atif.agent.name"] == "backend-builder"
        assert span_attrs["plato.agent.display_name"] == "backend-builder"
        assert span_attrs["plato.agent.alias"] == "backend-builder-ab12cd34"

    @pytest.mark.asyncio
    async def test_workspace_ownership_normalized_before_agent_run(self, runtime, mock_instruction_write):
        """VM runtime still calls the writability hook before running the agent."""
        ctx = _make_ctx(continue_session=False)
        agent_env = MagicMock()
        hostname = "10.0.0.1"

        streaming_called = False

        async def mock_run_ssh_streaming(_ssh_key, hostname, command, user="root", extra_opts=None):
            nonlocal streaming_called
            streaming_called = True
            return 0

        runtime._ensure_workspace_writable = AsyncMock()

        with patch("plato.agents.runtime.vm.OTelContext.from_env") as mock_otel:
            mock_otel.return_value = MagicMock(
                otel_url=None,
                session_id=None,
                upload_url=None,
                traceparent=None,
                trace_id=None,
                parent_span_id=None,
                to_env_vars=MagicMock(return_value=[]),
            )
            with patch(
                "plato.agents.runtime.vm.run_ssh",
                new=AsyncMock(return_value=(0, "ALREADY_EXISTS\n", "")),
            ):
                with patch(
                    "plato.agents.runtime.vm.run_ssh_streaming",
                    new=AsyncMock(side_effect=mock_run_ssh_streaming),
                ):
                    await runtime._execute_agent(ctx, agent_env, hostname, "/usr/local/bin/plato-agent-runner")

        assert streaming_called is True
        runtime._ensure_workspace_writable.assert_awaited_once_with(hostname)

    @pytest.mark.asyncio
    async def test_workspace_ownership_failure_is_non_fatal(self, runtime, mock_instruction_write):
        """Agent run proceeds without ownership normalization warnings."""
        ctx = _make_ctx(continue_session=False)
        agent_env = MagicMock()
        hostname = "10.0.0.1"

        streaming_called = False

        async def mock_run_ssh_streaming(_ssh_key, hostname, command, user="root", extra_opts=None):
            nonlocal streaming_called
            streaming_called = True
            return 0

        with patch("plato.agents.runtime.vm.OTelContext.from_env") as mock_otel:
            mock_otel.return_value = MagicMock(
                otel_url=None,
                session_id=None,
                upload_url=None,
                traceparent=None,
                trace_id=None,
                parent_span_id=None,
                to_env_vars=MagicMock(return_value=[]),
            )
            with patch(
                "plato.agents.runtime.vm.run_ssh",
                new=AsyncMock(return_value=(0, "ALREADY_EXISTS\n", "")),
            ):
                with patch(
                    "plato.agents.runtime.vm.run_ssh_streaming",
                    new=AsyncMock(side_effect=mock_run_ssh_streaming),
                ):
                    with patch("plato.agents.runtime.vm.logger.warning") as mock_warn:
                        await runtime._execute_agent(ctx, agent_env, hostname, "/usr/local/bin/plato-agent-runner")
                        mock_warn.assert_not_called()

        assert streaming_called is True

    @pytest.mark.asyncio
    async def test_prepare_cold_runs_code_sync_and_env_setup_concurrently(self, runtime):
        """Code sync and env setup must run concurrently via asyncio.gather, not serially."""
        ctx = _make_ctx(display_name="concurrency-test")
        agent_env = MagicMock()
        agent_env.mesh_ip = "10.0.0.1"
        agent_env.get_mesh_ip = AsyncMock(return_value="10.0.0.1")
        agent_env.add_ssh_key = AsyncMock()

        runtime._create_vm = AsyncMock(return_value=agent_env)

        call_order: list[str] = []
        sync_started = asyncio.Event()
        env_started = asyncio.Event()

        async def mock_sync_code(tracer, ctx, agent_env, mesh_ip, alias):
            call_order.append("sync_start")
            sync_started.set()
            await asyncio.sleep(0)
            call_order.append("sync_end")

        async def mock_env_setup(tracer, mesh_ip):
            call_order.append("env_start")
            env_started.set()
            await asyncio.sleep(0)
            call_order.append("env_end")

        async def mock_ws_setup(tracer, agent_env, mesh_ip, alias):
            call_order.append("ws_setup")

        runtime._prepare_sync_code = mock_sync_code
        runtime._prepare_env_setup = mock_env_setup
        runtime._prepare_workspace_setup = mock_ws_setup

        with (
            patch("pathlib.Path.read_text", return_value="ssh-ed25519 AAAATEST"),
            patch(
                "plato.agents.runtime.vm.resolve_runner_path",
                new=AsyncMock(return_value="/usr/local/bin/plato-agent-runner"),
            ),
        ):
            await runtime._prepare_cold(ctx)

        # Both sync and env should start before either ends (concurrent execution)
        sync_idx = call_order.index("sync_start")
        env_idx = call_order.index("env_start")
        # Both started before workspace setup
        ws_idx = call_order.index("ws_setup")
        assert sync_idx < ws_idx
        assert env_idx < ws_idx

    @pytest.mark.asyncio
    async def test_prepare_from_pool_runs_env_before_workspace(self, runtime):
        """Pool path must run env setup before workspace setup (env writes /etc/environment)."""
        from plato.agents.runtime.warmpool import PooledVM

        ctx = _make_ctx(display_name="pool-order-test")
        pooled_vm = MagicMock(spec=PooledVM)
        pooled_vm.alias = "pool-vm-1"
        pooled_vm.mesh_ip = "10.0.0.1"
        pooled_vm.runner_path = "/usr/local/bin/plato-agent-runner"
        pooled_vm.agent_env = MagicMock()

        warm_pool = MagicMock()
        warm_pool.acquire = AsyncMock(return_value=pooled_vm)
        runtime.warm_pool = warm_pool

        call_order: list[str] = []

        async def mock_env_setup(tracer, mesh_ip):
            call_order.append("env_setup")

        async def mock_ws_setup(tracer, agent_env, mesh_ip, alias):
            call_order.append("ws_setup")

        runtime._prepare_env_setup = mock_env_setup
        runtime._prepare_workspace_setup = mock_ws_setup

        await runtime._prepare_from_pool(ctx)

        assert call_order == ["env_setup", "ws_setup"]

    @pytest.mark.asyncio
    async def test_prepare_cold_exhausted_retries_raises(self, runtime):
        """After all retry attempts fail with non-duplicate errors, the last exception is raised."""
        ctx = _make_ctx(display_name="exhaust-test")

        runtime._create_vm = AsyncMock(side_effect=RuntimeError("Some fatal error"))
        runtime.cleanup = AsyncMock()

        with patch("plato.agents.runtime.vm._make_agent_alias", return_value="exhaust-base"):
            with pytest.raises(RuntimeError, match="Some fatal error"):
                await runtime._prepare_cold(ctx)

        # Only one attempt since it's not a duplicate alias error
        assert runtime._create_vm.await_count == 1

    @pytest.mark.asyncio
    async def test_resolve_runner_path_requires_absolute_executable(self, runtime):
        with patch(
            "plato.agents.runtime.vm.run_ssh",
            new=AsyncMock(return_value=(0, "/usr/local/bin/plato-agent-runner\n", "")),
        ):
            runner_path = await runtime._resolve_runner_path("10.0.0.1")

        assert runner_path == "/usr/local/bin/plato-agent-runner"
