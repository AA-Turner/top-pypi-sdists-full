"""Tests for make_trace_event convenience factory."""

import time

from agentic_devtools.orchestration.execution.tracing import TraceEvent, make_trace_event
from agentic_devtools.orchestration.execution.types import JSONValue


class TestMakeTraceEvent:
    def test_returns_trace_event(self) -> None:
        event = make_trace_event(node_name="test_node", operation_type="reasoning")
        assert isinstance(event, TraceEvent)

    def test_auto_sets_timestamp(self) -> None:
        before = time.time()
        event = make_trace_event(node_name="n", operation_type="reasoning")
        after = time.time()
        assert before <= event.timestamp <= after

    def test_default_values(self) -> None:
        event = make_trace_event(node_name="n", operation_type="tool_invocation")
        assert event.model_id == ""
        assert event.tool_name == ""
        assert event.input_summary == ""
        assert event.output_summary == ""
        assert event.duration_ms == 0.0
        assert event.success is True
        assert event.usage == {}

    def test_all_fields(self) -> None:
        usage: dict[str, JSONValue] = {"prompt_tokens": 10}
        event = make_trace_event(
            node_name="analysis",
            operation_type="reasoning",
            model_id="gpt-4",
            tool_name="get_context",
            input_summary="prompt text",
            output_summary="response text",
            duration_ms=123.4,
            success=False,
            usage=usage,
        )
        assert event.node_name == "analysis"
        assert event.operation_type == "reasoning"
        assert event.model_id == "gpt-4"
        assert event.tool_name == "get_context"
        assert event.input_summary == "prompt text"
        assert event.output_summary == "response text"
        assert event.duration_ms == 123.4
        assert event.success is False
        assert event.usage == {"prompt_tokens": 10}

    def test_usage_none_becomes_empty_dict(self) -> None:
        event = make_trace_event(node_name="n", operation_type="r", usage=None)
        assert event.usage == {}
