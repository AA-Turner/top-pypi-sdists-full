"""Tests for TraceEmitter protocol conformance."""

from agentic_devtools.orchestration.execution.protocols import TraceEmitter
from agentic_devtools.orchestration.execution.tracing import TraceEvent


class _MockTraceEmitter:
    """A concrete class satisfying the TraceEmitter protocol."""

    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    def emit(self, event: TraceEvent) -> None:
        self.events.append(event)


class TestTraceEmitter:
    def test_mock_satisfies_protocol(self) -> None:
        emitter = _MockTraceEmitter()
        assert isinstance(emitter, TraceEmitter)

    def test_emit_records_event(self) -> None:
        emitter = _MockTraceEmitter()
        event = TraceEvent(
            timestamp=1234.0,
            node_name="test_node",
            operation_type="reasoning",
        )
        emitter.emit(event)
        assert len(emitter.events) == 1
        assert emitter.events[0].node_name == "test_node"

    def test_emit_multiple_events(self) -> None:
        emitter = _MockTraceEmitter()
        for i in range(3):
            emitter.emit(
                TraceEvent(
                    timestamp=float(i),
                    node_name=f"node_{i}",
                    operation_type="tool_invocation",
                )
            )
        assert len(emitter.events) == 3
