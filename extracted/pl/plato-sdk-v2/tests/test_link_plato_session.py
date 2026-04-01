"""Tests for _link_plato_session in dev and test runners."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from plato.cli.chronos.dev.runner import DevRunner
from plato.cli.chronos.test.runner import TestRunner


@pytest.fixture
def dev_runner() -> DevRunner:
    """Create a DevRunner with minimal mocked config."""
    config = MagicMock()
    config.dev.world = None
    config.dev.agents = {}
    config.dev.extra_sync = {}
    config.dev.sync_sdk = False
    config.session.session_id = "chronos-session-123"
    with patch.dict(os.environ, {"PLATO_API_KEY": "test-key"}):
        return DevRunner(config=config, config_path=Path("/tmp/fake.json"))


@pytest.fixture
def test_runner() -> TestRunner:
    """Create a TestRunner with minimal mocked config."""
    config = MagicMock()
    config.tags = []
    config.world.package = "plato-world-test"
    config.test.pass_env = []
    config.test.env = {}
    runner = TestRunner(
        config=config,
        config_path=Path("/tmp/fake.json"),
        api_key="test-key",
        phase_filter="all",
        pytest_args=None,
        artifacts_dir=None,
        verbose=False,
    )
    runner.session_id = "chronos-session-456"
    return runner


@pytest.mark.asyncio
async def test_dev_runner_link_uses_config_session_id(dev_runner: DevRunner) -> None:
    """DevRunner._link_plato_session must use self.config.session.session_id, not self.session_id."""
    with patch(
        "plato.cli.chronos.dev.runner.link_plato_session.asyncio",
        new_callable=AsyncMock,
    ) as mock_link:
        await dev_runner._link_plato_session("plato-session-abc")

        mock_link.assert_called_once()
        call_kwargs = mock_link.call_args
        assert call_kwargs.kwargs["public_id"] == "chronos-session-123"
        assert call_kwargs.kwargs["body"].plato_session_id == "plato-session-abc"


@pytest.mark.asyncio
async def test_dev_runner_link_skips_when_no_session_id(dev_runner: DevRunner) -> None:
    """DevRunner._link_plato_session should no-op when session_id is not set."""
    dev_runner.config.session.session_id = None
    with patch(
        "plato.cli.chronos.dev.runner.link_plato_session.asyncio",
        new_callable=AsyncMock,
    ) as mock_link:
        await dev_runner._link_plato_session("plato-session-abc")
        mock_link.assert_not_called()


@pytest.mark.asyncio
async def test_test_runner_link_uses_session_id(test_runner: TestRunner) -> None:
    """TestRunner._link_plato_session must use self.session_id."""
    with patch(
        "plato.cli.chronos.test.runner.link_plato_session.asyncio",
        new_callable=AsyncMock,
    ) as mock_link:
        await test_runner._link_plato_session("plato-session-xyz")

        mock_link.assert_called_once()
        call_kwargs = mock_link.call_args
        assert call_kwargs.kwargs["public_id"] == "chronos-session-456"
        assert call_kwargs.kwargs["body"].plato_session_id == "plato-session-xyz"


@pytest.mark.asyncio
async def test_test_runner_link_skips_when_no_session_id(test_runner: TestRunner) -> None:
    """TestRunner._link_plato_session should no-op when session_id is empty."""
    test_runner.session_id = ""
    with patch(
        "plato.cli.chronos.test.runner.link_plato_session.asyncio",
        new_callable=AsyncMock,
    ) as mock_link:
        await test_runner._link_plato_session("plato-session-xyz")
        mock_link.assert_not_called()


@pytest.mark.asyncio
async def test_dev_runner_link_swallows_errors(dev_runner: DevRunner) -> None:
    """DevRunner._link_plato_session should not raise on API errors."""
    with patch(
        "plato.cli.chronos.dev.runner.link_plato_session.asyncio",
        new_callable=AsyncMock,
        side_effect=RuntimeError("connection refused"),
    ):
        # Should not raise
        await dev_runner._link_plato_session("plato-session-abc")


@pytest.mark.asyncio
async def test_test_runner_link_swallows_errors(test_runner: TestRunner) -> None:
    """TestRunner._link_plato_session should not raise on API errors."""
    with patch(
        "plato.cli.chronos.test.runner.link_plato_session.asyncio",
        new_callable=AsyncMock,
        side_effect=RuntimeError("connection refused"),
    ):
        # Should not raise
        await test_runner._link_plato_session("plato-session-xyz")
