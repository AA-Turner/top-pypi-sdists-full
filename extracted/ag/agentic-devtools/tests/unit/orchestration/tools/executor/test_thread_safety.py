"""Tests for thread-safety enforcement."""

import threading
import time
from unittest.mock import patch

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestThreadSafety:
    """Tests for per-tool lock enforcement."""

    def test_thread_unsafe_tool_busy(self):
        """Second concurrent call to thread_safe=False tool gets tool_busy error."""
        barrier = threading.Barrier(2, timeout=5)

        def slow_tool(**kwargs):
            barrier.wait()
            time.sleep(0.5)
            return {"done": True}

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="unsafe",
                description="Not thread safe",
                category="state",
                input_schema={"type": "object", "properties": {}},
                thread_safe=False,
                timeout_seconds=5.0,
            ),
            fn=slow_tool,
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)

        results = [None, None]

        def _call(idx):
            if idx == 0:
                results[idx] = executor.execute("unsafe")
            else:
                barrier.wait()
                time.sleep(0.05)  # Ensure first call has acquired lock
                results[idx] = executor.execute("unsafe")

        t1 = threading.Thread(target=_call, args=(0,))
        t2 = threading.Thread(target=_call, args=(1,))
        t1.start()
        t2.start()
        t1.join(timeout=10)
        t2.join(timeout=10)

        # One should succeed, one should get tool_busy
        successes = [r for r in results if r and r.success]
        failures = [r for r in results if r and not r.success]
        assert len(successes) == 1
        assert len(failures) == 1
        assert failures[0].error_type == "precondition_not_met"
        assert "tool_busy" in failures[0].error_message

    def test_thread_safe_tool_concurrent(self):
        """thread_safe=True tools can execute concurrently."""
        call_count = {"n": 0}
        lock = threading.Lock()

        def counting_tool(**kwargs):
            with lock:
                call_count["n"] += 1
            time.sleep(0.1)
            return {"ok": True}

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="safe",
                description="Thread safe",
                category="testing",
                input_schema={"type": "object", "properties": {}},
                thread_safe=True,
            ),
            fn=counting_tool,
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)

        threads = [threading.Thread(target=lambda: executor.execute("safe")) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10)

        assert call_count["n"] == 3

    def test_thread_unsafe_tool_busy_audit_status(self):
        """tool_busy audit entries use precondition_not_met status."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="unsafe",
                description="Not thread safe",
                category="state",
                input_schema={"type": "object", "properties": {}},
                thread_safe=False,
            ),
            fn=lambda **kwargs: {"done": True},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)

        lock = executor._get_tool_lock("unsafe")
        lock.acquire()
        try:
            with patch("agentic_devtools.orchestration.tools.executor.emit_audit_log") as mock_emit:
                result = executor.execute("unsafe")
        finally:
            lock.release()

        assert result.success is False
        assert result.error_type == "precondition_not_met"
        assert mock_emit.call_args.kwargs["status"] == "precondition_not_met"

    def test_timeout_keeps_non_thread_safe_lock_until_tool_finishes(self):
        """Timed-out non-thread-safe tools stay locked until the worker exits."""

        def slow_tool(**kwargs):
            time.sleep(0.3)
            return {"done": True}

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="unsafe_timeout",
                description="Not thread safe and slow",
                category="state",
                input_schema={"type": "object", "properties": {}},
                thread_safe=False,
                timeout_seconds=0.05,
            ),
            fn=slow_tool,
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)

        first = executor.execute("unsafe_timeout")
        second = executor.execute("unsafe_timeout")
        time.sleep(0.35)
        third = executor.execute("unsafe_timeout")

        assert first.error_type == "timeout"
        assert second.error_type == "precondition_not_met"
        assert third.error_type == "timeout"
