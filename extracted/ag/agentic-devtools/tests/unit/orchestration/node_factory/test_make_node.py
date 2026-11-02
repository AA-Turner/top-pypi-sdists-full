"""Tests for make_node() factory wrapper."""

from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.orchestration.execution.context import ExecutionContext
from agentic_devtools.orchestration.execution.exceptions import RetryExhaustedError
from agentic_devtools.orchestration.execution.tracing import LoggingTraceEmitter
from agentic_devtools.orchestration.node_factory import make_node


def _make_context() -> ExecutionContext:
    """Create a minimal ExecutionContext with mocks."""
    reasoning = MagicMock()
    tools = MagicMock()
    tracer = LoggingTraceEmitter()
    return ExecutionContext(reasoning=reasoning, tools=tools, tracer=tracer)


class TestMakeNode:
    """Tests for the make_node() wrapper."""

    def test_wraps_function_and_calls_with_context(self) -> None:
        """Wrapped function receives state and context."""
        called_with: dict = {}

        def my_node(state, *, context):
            called_with["state"] = state
            called_with["context"] = context
            return {"status": "ok"}

        ctx = _make_context()
        wrapped = make_node(my_node, ctx)
        result = wrapped({"key": "value"})

        assert result == {"status": "ok"}
        assert called_with["state"] == {"key": "value"}
        assert called_with["context"] is ctx

    def test_emits_trace_events(self) -> None:
        """Wrapped function emits start and end trace events."""
        events: list = []
        tracer = MagicMock()
        tracer.emit = lambda event: events.append(event)

        ctx = ExecutionContext(
            reasoning=MagicMock(),
            tools=MagicMock(),
            tracer=tracer,
        )

        def my_node(state, *, context):
            return {"status": "done"}

        wrapped = make_node(my_node, ctx)
        wrapped({"x": 1})

        assert len(events) == 2
        assert events[0].operation_type == "node_start"
        assert events[1].operation_type == "node_end"
        assert events[1].success is True

    def test_emits_trace_with_success_false_on_failed_status(self) -> None:
        """node_end trace has success=False when result status is 'failed'."""
        events: list = []
        tracer = MagicMock()
        tracer.emit = lambda event: events.append(event)

        ctx = ExecutionContext(
            reasoning=MagicMock(),
            tools=MagicMock(),
            tracer=tracer,
        )

        def failing_node(state, *, context):
            return {"status": "failed", "error": {"type": "some_error", "message": "oops"}}

        wrapped = make_node(failing_node, ctx)
        result = wrapped({})

        assert result["status"] == "failed"
        assert events[1].operation_type == "node_end"
        assert events[1].success is False

    def test_retry_exhausted_returns_failed_state(self) -> None:
        """RetryExhaustedError returns failed status dict."""
        ctx = _make_context()

        def failing_node(state, *, context):
            raise RetryExhaustedError("all retries done", attempts=3, last_error="timeout")

        wrapped = make_node(failing_node, ctx)
        result = wrapped({})

        assert result["status"] == "failed"
        assert result["error"]["type"] == "retry_exhausted"
        assert result["error"]["attempts"] == 3

    def test_unexpected_exception_returns_failed_state(self) -> None:
        """Unexpected exceptions return failed status dict."""
        ctx = _make_context()

        def crashing_node(state, *, context):
            raise ValueError("something broke")

        wrapped = make_node(crashing_node, ctx)
        result = wrapped({})

        assert result["status"] == "failed"
        assert result["error"]["type"] == "ValueError"
        assert "something broke" in result["error"]["message"]

    def test_preserves_function_name(self) -> None:
        """Wrapped function preserves the original name."""
        ctx = _make_context()

        def review_file_node(state, *, context):
            return {}

        wrapped = make_node(review_file_node, ctx)
        assert wrapped.__name__ == "review_file_node"
