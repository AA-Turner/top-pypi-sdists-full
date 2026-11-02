"""Tests for timeout enforcement."""

import concurrent.futures
import time
from unittest.mock import MagicMock

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestTimeout:
    """Tests for timeout enforcement in ToolExecutor."""

    def test_timeout_fires(self):
        """Tool that exceeds timeout returns timeout error."""

        def slow_tool(**kwargs):
            time.sleep(1)
            return {"done": True}

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="slow",
                description="Slow tool",
                category="testing",
                input_schema={"type": "object", "properties": {}},
                timeout_seconds=0.5,
            ),
            fn=slow_tool,
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        start = time.perf_counter()
        result = executor.execute("slow")
        elapsed = time.perf_counter() - start
        assert result.success is False
        assert result.error_type == "timeout"
        assert result.duration_ms >= 400  # At least 0.4s
        assert elapsed >= 0.4
        assert elapsed < 2.0

    def test_fast_tool_succeeds(self):
        """Tool that completes within timeout succeeds."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="fast",
                description="Fast tool",
                category="testing",
                input_schema={"type": "object", "properties": {}},
                timeout_seconds=5.0,
            ),
            fn=lambda: {"done": True},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.execute("fast")
        assert result.success is True

    def test_timeout_releases_lock_immediately_when_future_is_already_done(self):
        """Timed-out calls release a held lock immediately when the future is done."""
        registry = ConcreteToolRegistry()
        definition = ToolDefinition(
            name="slow",
            description="Slow tool",
            category="testing",
            input_schema={"type": "object", "properties": {}},
            timeout_seconds=0.5,
            thread_safe=False,
        )
        registry.register(definition, fn=lambda: {"done": True})
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)

        future = MagicMock()
        future.result.side_effect = concurrent.futures.TimeoutError
        future.done.return_value = True

        executor._pool = MagicMock()
        executor._pool.submit.return_value = future

        release_lock = MagicMock()

        result = executor._execute_with_timeout(
            definition,
            "slow",
            {},
            time.time(),
            release_lock=release_lock,
        )

        assert result.error_type == "timeout"
        release_lock.assert_called_once_with()
        # With the shared pool the pool is NOT shut down on timeout.
        executor._pool.shutdown.assert_not_called()

    def test_submit_failure_returns_execution_error(self):
        """Executor returns execution_error when pool.submit raises."""
        registry = ConcreteToolRegistry()
        definition = ToolDefinition(
            name="submit_fail",
            description="Submit failure",
            category="testing",
            input_schema={"type": "object", "properties": {}},
        )
        registry.register(definition, fn=lambda: {"done": True})
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)

        executor._pool = MagicMock()
        executor._pool.submit.side_effect = RuntimeError("submit failed")

        result = executor.execute("submit_fail")

        assert result.success is False
        assert result.error_type == "execution_error"
        assert "submit failed" in result.error_message
        # The shared pool is never shut down on a submit error.
        executor._pool.shutdown.assert_not_called()
