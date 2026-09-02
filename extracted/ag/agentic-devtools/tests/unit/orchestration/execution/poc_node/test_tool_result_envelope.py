"""Tests for poc_node ToolResult envelope unwrapping."""

import json

from agentic_devtools.orchestration.execution.context import ExecutionContext
from agentic_devtools.orchestration.execution.poc_node import create_analysis_node
from agentic_devtools.orchestration.execution.tracing import TraceEvent
from agentic_devtools.orchestration.execution.types import ReasoningResponse


class _MockTracer:
    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    def emit(self, event: TraceEvent) -> None:
        self.events.append(event)


class _MockProvider:
    def invoke(self, prompt, *, tools=None, output_schema=None, model=None):  # noqa: ANN001, ANN003, ANN201
        return ReasoningResponse(
            raw_text=json.dumps({"plan": "ok"}),
            parsed_output={"plan": "ok"},
        )


class TestToolResultEnvelopeUnwrap:
    """Tests for ToolResult envelope failure unwrapping in poc_node."""

    def test_failed_tool_result_envelope_returns_error(self):
        """When tool registry returns a failed ToolResult envelope, node returns error state."""

        class _FailedEnvelopeRegistry:
            def invoke(self, tool_name: str, **kwargs) -> dict:  # noqa: ANN003
                return {
                    "success": False,
                    "error_type": "execution_error",
                    "error_message": "Jira is down",
                    "output": None,
                }

        tracer = _MockTracer()
        ctx = ExecutionContext(
            reasoning=_MockProvider(),
            tools=_FailedEnvelopeRegistry(),
            tracer=tracer,
        )
        node = create_analysis_node(ctx)
        result = node({})

        assert result["status"] == "failed"
        assert "execution_error" in str(result["error"])
        assert "Jira is down" in str(result["error"])

    def test_failed_envelope_emits_trace_event(self):
        """A failed envelope emits a trace event with success=False."""

        class _FailedEnvelopeRegistry:
            def invoke(self, tool_name: str, **kwargs) -> dict:  # noqa: ANN003
                return {
                    "success": False,
                    "error_type": "timeout",
                    "error_message": "Timed out",
                }

        tracer = _MockTracer()
        ctx = ExecutionContext(
            reasoning=_MockProvider(),
            tools=_FailedEnvelopeRegistry(),
            tracer=tracer,
        )
        node = create_analysis_node(ctx)
        node({})

        tool_events = [e for e in tracer.events if e.operation_type == "tool_invocation"]
        assert len(tool_events) >= 1
        failed_events = [e for e in tool_events if not e.success]
        assert len(failed_events) >= 1
        assert "error_type=timeout" in failed_events[0].output_summary

    def test_successful_envelope_extracts_output(self):
        """When registry returns successful envelope, output is extracted."""

        class _SuccessEnvelopeRegistry:
            def invoke(self, tool_name: str, **kwargs) -> dict:  # noqa: ANN003
                return {
                    "success": True,
                    "output": {"issue_key": "PROJ-123", "summary": "Test issue"},
                }

        ctx = ExecutionContext(
            reasoning=_MockProvider(),
            tools=_SuccessEnvelopeRegistry(),
            tracer=_MockTracer(),
        )
        node = create_analysis_node(ctx)
        result = node({})

        assert result["status"] == "completed"

    def test_failed_envelope_with_unknown_error_type(self):
        """Failed envelope with missing error_type defaults to 'unknown'."""

        class _FailedNoTypeRegistry:
            def invoke(self, tool_name: str, **kwargs) -> dict:  # noqa: ANN003
                return {"success": False}

        ctx = ExecutionContext(
            reasoning=_MockProvider(),
            tools=_FailedNoTypeRegistry(),
            tracer=_MockTracer(),
        )
        node = create_analysis_node(ctx)
        result = node({})

        assert result["status"] == "failed"
        assert "unknown" in str(result["error"])

    def test_failed_envelope_uses_fallback_error_keys(self):
        """Failed envelopes surface message, error, and stderr details."""

        class _FailedEnvelopeRegistry:
            def __init__(self, response: dict) -> None:
                self._response = response

            def invoke(self, tool_name: str, **kwargs) -> dict:  # noqa: ANN003
                return self._response

        failure_cases = (
            ({"success": False, "message": "Not a git repository"}, "Not a git repository"),
            ({"success": False, "error": "File not found"}, "File not found"),
            ({"success": False, "stderr": "Pattern is unsafe"}, "Pattern is unsafe"),
        )

        for response, expected in failure_cases:
            ctx = ExecutionContext(
                reasoning=_MockProvider(),
                tools=_FailedEnvelopeRegistry(response),
                tracer=_MockTracer(),
            )
            node = create_analysis_node(ctx)
            result = node({})

            assert result["status"] == "failed"
            assert expected in str(result["error"])
