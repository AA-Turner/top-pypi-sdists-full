"""Tests for continue_session handling in PlatoVMRuntime._execute_agent().

continue_session is passed through the agent config dict (AGENT_CONFIG_B64),
NOT as a separate env var. These tests verify the config dict carries it.
"""

from __future__ import annotations

import base64
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from plato.agents.runtime.base import AgentContext
from plato.agents.runtime.vm import PlatoVMRuntime


def _make_ctx(continue_session: bool = False) -> AgentContext:
    config = {"key": "value"}
    if continue_session:
        config["continue_session"] = True
    return AgentContext(
        image="test:latest",
        config=config,
        instruction="do something",
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
