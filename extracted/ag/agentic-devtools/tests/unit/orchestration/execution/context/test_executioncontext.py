"""Tests for ExecutionContext dataclass construction."""

from agentic_devtools.orchestration.execution.context import ExecutionContext
from agentic_devtools.orchestration.execution.tracing import LoggingTraceEmitter, TraceEvent
from agentic_devtools.orchestration.execution.types import ReasoningResponse


class _StubProvider:
    def invoke(self, prompt, *, tools=None, output_schema=None, model=None):  # noqa: ANN001, ANN003, ANN201
        return ReasoningResponse(raw_text="stub")


class _StubRegistry:
    def invoke(self, tool_name, **kwargs):  # noqa: ANN001, ANN003, ANN201
        return None


class _StubEmitter:
    def emit(self, event: TraceEvent) -> None:
        pass


class TestExecutionContext:
    def test_construction(self) -> None:
        ctx = ExecutionContext(
            reasoning=_StubProvider(),
            tools=_StubRegistry(),
            tracer=_StubEmitter(),
        )
        assert ctx.reasoning is not None
        assert ctx.tools is not None
        assert ctx.tracer is not None

    def test_config_defaults_empty(self) -> None:
        ctx = ExecutionContext(
            reasoning=_StubProvider(),
            tools=_StubRegistry(),
            tracer=_StubEmitter(),
        )
        assert ctx.config == {}

    def test_config_populated(self) -> None:
        ctx = ExecutionContext(
            reasoning=_StubProvider(),
            tools=_StubRegistry(),
            tracer=_StubEmitter(),
            config={"default_model": "gpt-4", "max_retries": 3},
        )
        assert ctx.config["default_model"] == "gpt-4"
        assert ctx.config["max_retries"] == 3

    def test_is_frozen(self) -> None:
        ctx = ExecutionContext(
            reasoning=_StubProvider(),
            tools=_StubRegistry(),
            tracer=_StubEmitter(),
        )
        try:
            ctx.reasoning = _StubProvider()  # type: ignore[misc]
            raise AssertionError("Expected FrozenInstanceError")
        except AttributeError:
            pass

    def test_with_logging_emitter(self) -> None:
        ctx = ExecutionContext(
            reasoning=_StubProvider(),
            tools=_StubRegistry(),
            tracer=LoggingTraceEmitter(),
        )
        assert isinstance(ctx.tracer, LoggingTraceEmitter)
