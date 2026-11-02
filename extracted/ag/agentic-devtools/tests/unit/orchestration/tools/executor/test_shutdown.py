"""Tests for ToolExecutor.shutdown()."""

from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestShutdown:
    """Tests for ToolExecutor.shutdown()."""

    def test_shutdown_waits_by_default(self):
        """shutdown() delegates to the pool with wait=True by default."""
        executor = ToolExecutor(ConcreteToolRegistry())
        mock_pool = MagicMock()
        executor._pool = mock_pool
        executor.shutdown()
        mock_pool.shutdown.assert_called_once_with(wait=True, cancel_futures=False)

    def test_shutdown_no_wait_cancels_futures(self):
        """shutdown(wait=False) passes cancel_futures=True to the pool."""
        executor = ToolExecutor(ConcreteToolRegistry())
        mock_pool = MagicMock()
        executor._pool = mock_pool
        executor.shutdown(wait=False)
        mock_pool.shutdown.assert_called_once_with(wait=False, cancel_futures=True)
