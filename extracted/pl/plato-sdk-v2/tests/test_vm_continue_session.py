"""Tests for continue_session handling in PlatoVMRuntime._execute_agent().

continue_session is passed through the agent config dict (AGENT_CONFIG_B64),
NOT as a separate env var. These tests verify the config dict carries it.
"""

from __future__ import annotations

import base64
import json
from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from plato.agents.runtime.base import AgentContext
from plato.agents.runtime.vm import PlatoVMRuntime, _make_agent_alias


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


class TestVMContinueSession:
    """Tests for continue_session propagation via config dict."""

    @pytest.mark.asyncio
    async def test_continue_session_in_config_b64(self, runtime):
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
                    await runtime._execute_agent(ctx, agent_env, hostname)

        assert captured_command is not None
        # No separate env var for continue_session
        assert "AGENT_CONTINUE_SESSION" not in captured_command
        # But config_b64 should contain it
        assert "AGENT_CONFIG_B64" in captured_command
        # Decode the config from the command to verify
        decoded = json.loads(base64.b64decode(ctx.config_b64).decode())
        assert decoded["continue_session"] is True

    @pytest.mark.asyncio
    async def test_no_continue_session_in_config_by_default(self, runtime):
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
                    await runtime._execute_agent(ctx, agent_env, hostname)

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

        with patch(
            "plato.agents.runtime.vm._make_agent_alias",
            return_value="shared-components-batch-5-base",
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
        runtime.cleanup.assert_awaited_once_with(
            "shared-components-batch-5-base",
            error=True,
        )

    @pytest.mark.asyncio
    async def test_agent_name_propagated_to_span_and_env(self, runtime):
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
                        await runtime._execute_agent(ctx, agent_env, hostname)

        assert captured_command is not None
        assert 'PLATO_AGENT_DISPLAY_NAME="backend-builder"' in captured_command
        assert span_attrs["atif.agent.name"] == "backend-builder"
        assert span_attrs["plato.agent.display_name"] == "backend-builder"
        assert span_attrs["plato.agent.alias"] == "backend-builder-ab12cd34"

    @pytest.mark.asyncio
    async def test_workspace_ownership_normalized_before_agent_run(self, runtime):
        """VM runtime normalizes /workspace ownership before running as superman."""
        ctx = _make_ctx(continue_session=False)
        agent_env = MagicMock()
        hostname = "10.0.0.1"

        ssh_commands: list[str] = []
        streaming_called = False

        async def mock_run_ssh(h, cmd, timeout=300):
            ssh_commands.append(cmd)
            return 0, "ALREADY_EXISTS\n", ""

        async def mock_run_ssh_streaming(_ssh_key, hostname, command, user="root", extra_opts=None):
            nonlocal streaming_called
            streaming_called = True
            ownership_cmd = next(c for c in ssh_commands if "chown -R superman:superman /workspace" in c)
            assert "2>/dev/null" not in ownership_cmd
            assert "|| true" not in ownership_cmd
            assert user == "superman"
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
                    await runtime._execute_agent(ctx, agent_env, hostname)

        assert streaming_called is True

    @pytest.mark.asyncio
    async def test_workspace_ownership_failure_is_non_fatal(self, runtime):
        """Agent run proceeds even if ownership normalization command fails."""
        ctx = _make_ctx(continue_session=False)
        agent_env = MagicMock()
        hostname = "10.0.0.1"

        streaming_called = False

        async def mock_run_ssh(h, cmd, timeout=300):
            if "chown -R superman:superman /workspace" in cmd:
                return 1, "", "operation not permitted"
            return 0, "ALREADY_EXISTS\n", ""

        async def mock_run_ssh_streaming(_ssh_key, hostname, command, user="root", extra_opts=None):
            nonlocal streaming_called
            streaming_called = True
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
                    with patch("plato.agents.runtime.vm.logger.warning") as mock_warn:
                        await runtime._execute_agent(ctx, agent_env, hostname)
                        mock_warn.assert_called_once()

        assert streaming_called is True
