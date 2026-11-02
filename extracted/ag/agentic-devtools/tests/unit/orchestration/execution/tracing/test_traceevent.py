"""Tests for TraceEvent dataclass construction."""

from agentic_devtools.orchestration.execution.tracing import TraceEvent


class TestTraceEvent:
    def test_construction_minimal(self) -> None:
        event = TraceEvent(
            timestamp=1234.0,
            node_name="test_node",
            operation_type="reasoning",
        )
        assert event.timestamp == 1234.0
        assert event.node_name == "test_node"
        assert event.operation_type == "reasoning"

    def test_default_values(self) -> None:
        event = TraceEvent(
            timestamp=0.0,
            node_name="n",
            operation_type="tool_invocation",
        )
        assert event.model_id == ""
        assert event.tool_name == ""
        assert event.input_summary == ""
        assert event.output_summary == ""
        assert event.duration_ms == 0.0
        assert event.success is True
        assert event.usage == {}

    def test_all_fields(self) -> None:
        event = TraceEvent(
            timestamp=9999.0,
            node_name="analysis",
            operation_type="reasoning",
            model_id="gpt-4",
            tool_name="",
            input_summary="prompt...",
            output_summary="result...",
            duration_ms=150.5,
            success=True,
            usage={"prompt_tokens": 100, "completion_tokens": 50},
        )
        assert event.model_id == "gpt-4"
        assert event.duration_ms == 150.5
        assert event.usage["prompt_tokens"] == 100

    def test_is_frozen(self) -> None:
        event = TraceEvent(timestamp=0.0, node_name="n", operation_type="r")
        try:
            event.node_name = "changed"  # type: ignore[misc]
            raise AssertionError("Expected FrozenInstanceError")
        except AttributeError:
            pass
