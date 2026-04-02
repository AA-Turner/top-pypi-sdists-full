"""Tests for VM agent bootstrap decisions."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from plato.agents.runtime.base import AgentContext
from plato.agents.runtime.vm import install_agent_code_on_vm


def _make_ctx(agent_code_path: Path | None = None) -> AgentContext:
    return AgentContext(
        image="383806609161.dkr.ecr.us-west-1.amazonaws.com/agents/plato/test-agent:1.2.3",
        config={},
        instruction="",
        agent_code_path=agent_code_path,
    )


@pytest.mark.asyncio
async def test_install_agent_code_on_vm_uses_explicit_dev_agent_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sync_dev_code = AsyncMock(return_value=True)
    install_production_agent = AsyncMock()
    monkeypatch.setattr("plato.agents.runtime.vm.sync_dev_code", sync_dev_code)
    monkeypatch.setattr("plato.agents.runtime.vm.install_production_agent", install_production_agent)
    monkeypatch.setattr("plato.agents.runtime.vm.Path.exists", lambda self: str(self) == "/sdk")

    ctx = _make_ctx(Path("/agents/test-agent"))

    await install_agent_code_on_vm(Path("/tmp/key"), "10.0.0.1", ctx)

    sync_dev_code.assert_awaited_once_with(
        Path("/tmp/key"), "10.0.0.1", Path("/agents/test-agent"), "test-agent", "1.2.3"
    )
    install_production_agent.assert_not_awaited()


@pytest.mark.asyncio
async def test_install_agent_code_on_vm_falls_back_when_no_explicit_dev_agent_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sync_dev_code = AsyncMock(return_value=False)
    install_production_agent = AsyncMock()
    monkeypatch.setattr("plato.agents.runtime.vm.sync_dev_code", sync_dev_code)
    monkeypatch.setattr("plato.agents.runtime.vm.install_production_agent", install_production_agent)
    monkeypatch.setattr("plato.agents.runtime.vm.Path.exists", lambda self: str(self) == "/sdk")

    ctx = _make_ctx()

    await install_agent_code_on_vm(Path("/tmp/key"), "10.0.0.1", ctx)

    sync_dev_code.assert_awaited_once_with(Path("/tmp/key"), "10.0.0.1", None, "test-agent", "1.2.3")
    install_production_agent.assert_awaited_once_with(Path("/tmp/key"), "10.0.0.1", "test-agent", "1.2.3")


@pytest.mark.asyncio
async def test_install_agent_code_on_vm_uses_production_install_without_sdk(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sync_dev_code = AsyncMock()
    install_production_agent = AsyncMock()
    monkeypatch.setattr("plato.agents.runtime.vm.sync_dev_code", sync_dev_code)
    monkeypatch.setattr("plato.agents.runtime.vm.install_production_agent", install_production_agent)
    monkeypatch.setattr("plato.agents.runtime.vm.Path.exists", lambda self: False)

    ctx = _make_ctx(Path("/agents/test-agent"))

    await install_agent_code_on_vm(Path("/tmp/key"), "10.0.0.1", ctx)

    sync_dev_code.assert_not_awaited()
    install_production_agent.assert_awaited_once_with(Path("/tmp/key"), "10.0.0.1", "test-agent", "1.2.3")
