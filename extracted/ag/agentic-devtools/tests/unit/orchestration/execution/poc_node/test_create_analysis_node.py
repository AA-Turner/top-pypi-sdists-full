"""Tests for create_analysis_node PoC factory.

Covers: successful reasoning, tool invocation, retry, timeout,
schema validation, trace emission, model selection, and missing provider.
"""

import json
import time

import pytest

from agentic_devtools.orchestration.execution.context import ExecutionContext
from agentic_devtools.orchestration.execution.exceptions import (
    ReasoningTimeoutError,
    ToolInvocationError,
)
from agentic_devtools.orchestration.execution.poc_node import create_analysis_node
from agentic_devtools.orchestration.execution.tracing import TraceEvent
from agentic_devtools.orchestration.execution.types import ReasoningResponse, TokenUsage

# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


class _MockTracer:
    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    def emit(self, event: TraceEvent) -> None:
        self.events.append(event)


class _RaisingTracer:
    """Tracer that always raises on emit — used to verify best-effort semantics."""

    def emit(self, event: TraceEvent) -> None:  # noqa: ARG002
        raise RuntimeError("tracer intentionally broken")


class _MockRegistry:
    def __init__(self, return_value=None) -> None:  # noqa: ANN001
        self.calls: list[tuple[str, dict]] = []
        self._return = return_value or "issue context data"

    def invoke(self, tool_name: str, **kwargs) -> str:  # noqa: ANN003
        self.calls.append((tool_name, kwargs))
        return self._return


class _MockProvider:
    def __init__(self, responses=None, raises=None) -> None:  # noqa: ANN001
        self._responses = list(responses or [])
        self._raises = raises
        self.call_count = 0

    def invoke(self, prompt, *, tools=None, output_schema=None, model=None):  # noqa: ANN001, ANN003, ANN201
        self.call_count += 1
        if self._raises:
            raise self._raises
        if self._responses:
            return self._responses.pop(0)
        return ReasoningResponse(
            raw_text=json.dumps({"plan": "do something"}),
            parsed_output={"plan": "do something"},
        )


def _make_ctx(
    provider=None,  # noqa: ANN001
    registry=None,  # noqa: ANN001
    tracer=None,  # noqa: ANN001
    config=None,  # noqa: ANN001
) -> ExecutionContext:
    return ExecutionContext(
        reasoning=provider or _MockProvider(),
        tools=registry or _MockRegistry(),
        tracer=tracer or _MockTracer(),
        config=config or {},
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestCreateAnalysisNode:
    def test_successful_reasoning(self) -> None:
        """US1 scenario 1: valid LLM response → correct state update."""
        ctx = _make_ctx()
        node = create_analysis_node(ctx)
        result = node({})
        assert result["status"] == "completed"
        assert result["error"] is None
        assert result["analysis_result"] == {"plan": "do something"}

    def test_deterministic_with_mock(self) -> None:
        """US1 scenario 2: mocked LLM produces identical output."""
        provider = _MockProvider()
        ctx = _make_ctx(provider=provider)
        node = create_analysis_node(ctx)
        result1 = node({})
        # Reset provider
        provider.call_count = 0
        result2 = node({})
        assert result1["analysis_result"] == result2["analysis_result"]

    def test_malformed_response_raises_validation_error(self) -> None:
        """US1 scenario 3: invalid JSON → structured validation error."""
        provider = _MockProvider(responses=[ReasoningResponse(raw_text="not json at all")])
        ctx = _make_ctx(provider=provider)
        node = create_analysis_node(ctx, max_retries=0)
        result = node({})
        assert result["status"] == "failed"
        error_msg = str(result["error"])
        assert "Malformed LLM response" in error_msg or "failed" in error_msg

    def test_timeout_handling(self) -> None:
        """US1 scenario: provider raises ReasoningTimeoutError."""
        provider = _MockProvider(raises=ReasoningTimeoutError("timeout"))
        ctx = _make_ctx(provider=provider)
        node = create_analysis_node(ctx, max_retries=0)
        result = node({})
        assert result["status"] == "failed"

    def test_trace_events_emitted_for_reasoning(self) -> None:
        """US1: trace events emitted for reasoning calls."""
        tracer = _MockTracer()
        ctx = _make_ctx(tracer=tracer)
        node = create_analysis_node(ctx)
        node({})
        # Should have at least one tool event and one reasoning event
        op_types = {e.operation_type for e in tracer.events}
        assert "reasoning" in op_types
        assert "tool_invocation" in op_types

    def test_per_node_model_selection(self) -> None:
        """US1: model identifier forwarded to provider."""
        provider = _MockProvider()
        tracer = _MockTracer()
        ctx = _make_ctx(provider=provider, tracer=tracer)
        node = create_analysis_node(ctx, model="claude-3")
        node({})
        reasoning_events = [e for e in tracer.events if e.operation_type == "reasoning"]
        assert len(reasoning_events) >= 1
        assert reasoning_events[0].model_id == "claude-3"

    def test_provider_not_configured(self) -> None:
        """US1: factory fails fast when provider is None."""
        with pytest.raises(ValueError, match="not configured"):
            create_analysis_node(
                ExecutionContext(
                    reasoning=None,  # type: ignore[arg-type]
                    tools=_MockRegistry(),
                    tracer=_MockTracer(),
                )
            )

    def test_successful_tool_invocation(self) -> None:
        """US2 scenario 1: mock tool called with correct args."""
        registry = _MockRegistry(return_value="context from tool")
        ctx = _make_ctx(registry=registry)
        node = create_analysis_node(ctx)
        node({})
        assert len(registry.calls) == 1
        assert registry.calls[0][0] == "get_issue_context"

    def test_failed_tool_invocation(self) -> None:
        """US2 scenario 2: tool raises ToolInvocationError."""

        class _FailingRegistry:
            def invoke(self, tool_name: str, **kwargs) -> None:  # noqa: ANN003
                raise ToolInvocationError("tool broken", tool_name=tool_name)

        ctx = _make_ctx(registry=_FailingRegistry())
        node = create_analysis_node(ctx)
        result = node({})
        assert result["status"] == "failed"
        assert "Tool invocation failed" in str(result["error"])

    def test_unexpected_registry_exception_caught(self) -> None:
        """Unexpected exceptions from registry are caught and returned as failed state."""

        class _BrokenRegistry:
            def invoke(self, tool_name: str, **kwargs) -> None:  # noqa: ANN003
                raise KeyError("unexpected registry failure")

        ctx = _make_ctx(registry=_BrokenRegistry())
        node = create_analysis_node(ctx)
        result = node({})
        assert result["status"] == "failed"
        assert "Tool invocation failed" in str(result["error"])

    def test_tool_failure_trace_does_not_log_exception_message(self) -> None:
        """Failure trace event uses safe type-name summary, not raw exception message."""
        tracer = _MockTracer()

        class _FailingRegistry:
            def invoke(self, tool_name: str, **kwargs) -> None:  # noqa: ANN003
                raise ToolInvocationError("secret_token=abc123", tool_name=tool_name)

        ctx = _make_ctx(registry=_FailingRegistry(), tracer=tracer)
        node = create_analysis_node(ctx)
        node({})
        fail_events = [e for e in tracer.events if e.operation_type == "tool_invocation" and not e.success]
        assert fail_events
        assert "secret_token" not in fail_events[0].output_summary
        assert "error_type=" in fail_events[0].output_summary

    def test_trace_does_not_log_tool_output_content(self) -> None:
        tracer = _MockTracer()
        registry = _MockRegistry(return_value={"token": "secret", "message": "hello"})
        ctx = _make_ctx(registry=registry, tracer=tracer)
        node = create_analysis_node(ctx)
        node({})
        tool_events = [e for e in tracer.events if e.operation_type == "tool_invocation" and e.success]
        assert tool_events
        assert "secret" not in tool_events[0].output_summary
        assert tool_events[0].output_summary == "dict(keys=2)"

    def test_trace_tool_summary_for_list_output(self) -> None:
        tracer = _MockTracer()
        registry = _MockRegistry(return_value=["a", "b", "c"])
        ctx = _make_ctx(registry=registry, tracer=tracer)
        node = create_analysis_node(ctx)
        node({})
        tool_events = [e for e in tracer.events if e.operation_type == "tool_invocation" and e.success]
        assert tool_events[0].output_summary == "list(items=3)"

    def test_trace_tool_summary_for_scalar_output(self) -> None:
        tracer = _MockTracer()
        registry = _MockRegistry(return_value=123)
        ctx = _make_ctx(registry=registry, tracer=tracer)
        node = create_analysis_node(ctx)
        node({})
        tool_events = [e for e in tracer.events if e.operation_type == "tool_invocation" and e.success]
        assert tool_events[0].output_summary == "int"

    def test_trace_events_for_tool_invocation(self) -> None:
        """US2: trace events emitted for tool invocations."""
        tracer = _MockTracer()
        ctx = _make_ctx(tracer=tracer)
        node = create_analysis_node(ctx)
        node({})
        tool_events = [e for e in tracer.events if e.operation_type == "tool_invocation"]
        assert len(tool_events) >= 1
        assert tool_events[0].tool_name == "get_issue_context"

    def test_node_uses_registry_not_direct_imports(self) -> None:
        """US2: node does NOT import tool implementations directly."""
        registry = _MockRegistry()
        ctx = _make_ctx(registry=registry)
        node = create_analysis_node(ctx)
        node({})
        # If node used direct imports, registry would have no calls
        assert len(registry.calls) > 0

    def test_retry_on_failure_then_success(self) -> None:
        """US3: first call invalid, second valid → success."""
        responses = [
            ReasoningResponse(raw_text="not json"),
            ReasoningResponse(
                raw_text=json.dumps({"plan": "retry worked"}),
                parsed_output={"plan": "retry worked"},
            ),
        ]
        provider = _MockProvider(responses=responses)
        ctx = _make_ctx(provider=provider)
        node = create_analysis_node(ctx, max_retries=2)
        result = node({})
        assert result["status"] == "completed"
        assert result["analysis_result"] == {"plan": "retry worked"}

    def test_retry_exhaustion(self) -> None:
        """US3: all attempts fail → error state."""
        provider = _MockProvider(
            responses=[
                ReasoningResponse(raw_text="bad1"),
                ReasoningResponse(raw_text="bad2"),
                ReasoningResponse(raw_text="bad3"),
            ]
        )
        ctx = _make_ctx(provider=provider)
        node = create_analysis_node(ctx, max_retries=2)
        result = node({})
        assert result["status"] == "failed"
        assert result["retry_count"] == 3

    def test_trace_does_not_log_prompt_or_raw_output_content(self) -> None:
        tracer = _MockTracer()
        provider = _MockProvider(
            responses=[
                ReasoningResponse(
                    raw_text="MODEL RAW SECRET",
                    parsed_output={"result": "ok"},
                )
            ]
        )
        registry = _MockRegistry(return_value="CONTEXT SECRET")
        ctx = _make_ctx(provider=provider, registry=registry, tracer=tracer)
        node = create_analysis_node(ctx)
        node({})
        reasoning_events = [e for e in tracer.events if e.operation_type == "reasoning" and e.success]
        assert reasoning_events
        reasoning_event = reasoning_events[0]
        assert "CONTEXT SECRET" not in reasoning_event.input_summary
        assert "MODEL RAW SECRET" not in reasoning_event.output_summary
        assert "prompt_chars=" in reasoning_event.input_summary
        assert "raw_text_chars=" in reasoning_event.output_summary

    def test_integration_full_pipeline(self) -> None:
        """SC-006 scenario 1: full reasoning→acting→state pipeline."""
        start = time.time()
        provider = _MockProvider(
            responses=[
                ReasoningResponse(
                    raw_text=json.dumps({"analysis": "complete"}),
                    parsed_output={"analysis": "complete"},
                    usage=TokenUsage(
                        prompt_tokens=100,
                        completion_tokens=50,
                        total_tokens=150,
                    ),
                )
            ]
        )
        tracer = _MockTracer()
        registry = _MockRegistry()
        ctx = _make_ctx(provider=provider, registry=registry, tracer=tracer)
        node = create_analysis_node(ctx, model="gpt-4")
        result = node({})
        elapsed = time.time() - start

        assert result["status"] == "completed"
        assert result["analysis_result"] == {"analysis": "complete"}
        assert len(registry.calls) == 1
        assert len(tracer.events) >= 2
        assert elapsed < 3.0

    def test_faulty_tracer_does_not_break_tool_success_path(self) -> None:
        """Best-effort emit: faulty tracer must not prevent a successful node run."""
        ctx = _make_ctx(tracer=_RaisingTracer())
        node = create_analysis_node(ctx)
        result = node({})
        assert result["status"] == "completed"

    def test_faulty_tracer_does_not_break_tool_failure_path(self) -> None:
        """Best-effort emit: faulty tracer must not mask the tool-failure return."""

        class _FailingRegistry:
            def invoke(self, tool_name: str, **kwargs) -> None:  # noqa: ANN003
                raise ToolInvocationError("boom", tool_name=tool_name)

        ctx = _make_ctx(registry=_FailingRegistry(), tracer=_RaisingTracer())
        node = create_analysis_node(ctx)
        result = node({})
        assert result["status"] == "failed"
        assert "Tool invocation failed" in str(result["error"])

    def test_faulty_tracer_does_not_break_reasoning_success_path(self) -> None:
        """Best-effort emit: faulty tracer must not prevent reasoning from succeeding."""
        provider = _MockProvider(
            responses=[
                ReasoningResponse(
                    raw_text=json.dumps({"plan": "ok"}),
                    parsed_output={"plan": "ok"},
                )
            ]
        )
        ctx = _make_ctx(provider=provider, tracer=_RaisingTracer())
        node = create_analysis_node(ctx)
        result = node({})
        assert result["status"] == "completed"
        assert result["analysis_result"] == {"plan": "ok"}

    def test_faulty_tracer_does_not_break_reasoning_timeout_path(self) -> None:
        """Best-effort emit: faulty tracer must not interfere with timeout→retry flow."""
        # First call times out, second succeeds — verifies retry continues after tracer failure.
        call_count = 0
        original_responses = [
            ReasoningResponse(
                raw_text=json.dumps({"plan": "after timeout"}),
                parsed_output={"plan": "after timeout"},
            )
        ]

        class _TimeoutThenSuccessProvider:
            def invoke(self, prompt, *, tools=None, output_schema=None, model=None):  # noqa: ANN001, ANN003, ANN201
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    raise ReasoningTimeoutError("timeout")
                return original_responses.pop(0)

        ctx = _make_ctx(provider=_TimeoutThenSuccessProvider(), tracer=_RaisingTracer())
        node = create_analysis_node(ctx, max_retries=2)
        result = node({})
        assert result["status"] == "completed"
        assert result["analysis_result"] == {"plan": "after timeout"}

    def test_integration_tool_end_to_end(self) -> None:
        """SC-006 scenario 2: tool invocation end-to-end."""
        start = time.time()
        registry = _MockRegistry(return_value={"files": ["a.py", "b.py"]})
        tracer = _MockTracer()
        ctx = _make_ctx(registry=registry, tracer=tracer)
        node = create_analysis_node(ctx)
        result = node({})
        elapsed = time.time() - start

        assert result["status"] == "completed"
        assert registry.calls[0][0] == "get_issue_context"
        assert elapsed < 3.0

    def test_emit_best_effort_logs_only_exception_type_not_message(self, capsys) -> None:  # noqa: ANN001
        """_emit_best_effort must not leak exception message to stderr."""
        sensitive_message = "api_key=super_secret_abc123"

        class _SensitiveFailingTracer:
            def emit(self, event: TraceEvent) -> None:  # noqa: ARG002
                raise RuntimeError(sensitive_message)

        ctx = _make_ctx(tracer=_SensitiveFailingTracer())
        node = create_analysis_node(ctx)
        node({})
        captured = capsys.readouterr()
        assert sensitive_message not in captured.err
        assert "RuntimeError" in captured.err

    def test_non_string_default_model_raises(self) -> None:
        """create_analysis_node must raise ValueError when default_model is not a string."""
        ctx = _make_ctx(config={"default_model": 42})
        with pytest.raises(ValueError, match="default_model.*must be a string"):
            create_analysis_node(ctx)

    def test_none_default_model_raises(self) -> None:
        """create_analysis_node must raise ValueError when default_model is None (not a string)."""
        ctx = _make_ctx(config={"default_model": None})
        with pytest.raises(ValueError, match="default_model.*must be a string"):
            create_analysis_node(ctx)

    def test_string_default_model_accepted(self) -> None:
        """create_analysis_node accepts a valid string default_model config value."""
        ctx = _make_ctx(config={"default_model": "gpt-4"})
        node = create_analysis_node(ctx)
        result = node({})
        assert result["status"] == "completed"

    def test_negative_max_retries_raises(self) -> None:
        """create_analysis_node must reject negative max_retries at factory time."""
        ctx = _make_ctx()
        with pytest.raises(ValueError, match="max_retries must be >= 0"):
            create_analysis_node(ctx, max_retries=-1)

    def test_tool_failure_error_field_does_not_contain_exception_message(self) -> None:
        """Tool invocation error field must not embed the exception message (metadata-only)."""

        class _FailingRegistry:
            def invoke(self, tool_name: str, **kwargs) -> None:  # noqa: ANN003
                raise ToolInvocationError("secret_token=abc123", tool_name=tool_name)

        ctx = _make_ctx(registry=_FailingRegistry())
        node = create_analysis_node(ctx)
        result = node({})
        assert result["status"] == "failed"
        error_str = str(result["error"])
        assert "secret_token" not in error_str
        assert "abc123" not in error_str
        assert "tool=get_issue_context" in error_str
        assert "error_type=ToolInvocationError" in error_str

    def test_reasoning_failure_error_field_does_not_contain_exception_message(self) -> None:
        """Reasoning failure error field must not embed the exception message (metadata-only)."""
        sensitive_message = "Authorization: ******"
        provider = _MockProvider(raises=ValueError(sensitive_message))
        ctx = _make_ctx(provider=provider)
        node = create_analysis_node(ctx, max_retries=0)
        result = node({})
        assert result["status"] == "failed"
        error_str = str(result["error"])
        assert sensitive_message not in error_str
        assert "error_type=" in error_str

    def test_malformed_response_emits_only_failure_trace_not_success_then_failure(self) -> None:
        """When raw JSON parsing fails, only one failure trace is emitted — no preceding success trace."""
        tracer = _MockTracer()
        provider = _MockProvider(responses=[ReasoningResponse(raw_text="not json at all")])
        ctx = _make_ctx(provider=provider, tracer=tracer)
        node = create_analysis_node(ctx, max_retries=0)
        node({})
        reasoning_events = [e for e in tracer.events if e.operation_type == "reasoning"]
        assert len(reasoning_events) == 1, (
            f"Expected exactly 1 reasoning trace event, got {len(reasoning_events)}: "
            f"{[(e.success, e.output_summary) for e in reasoning_events]}"
        )
        assert not reasoning_events[0].success

    def test_unexpected_provider_exception_emits_single_failure_trace(self) -> None:
        """Unexpected provider exceptions (not timeout, not parse failure) emit exactly one failure trace."""
        tracer = _MockTracer()
        provider = _MockProvider(raises=ConnectionError("network unreachable"))
        ctx = _make_ctx(provider=provider, tracer=tracer)
        node = create_analysis_node(ctx, max_retries=0)
        node({})
        reasoning_events = [e for e in tracer.events if e.operation_type == "reasoning"]
        assert len(reasoning_events) == 1, (
            f"Expected exactly 1 reasoning trace event, got {len(reasoning_events)}: "
            f"{[(e.success, e.output_summary) for e in reasoning_events]}"
        )
        assert not reasoning_events[0].success
        assert "error_type=ConnectionError" in reasoning_events[0].output_summary

    def test_unexpected_provider_exception_does_not_double_emit_after_parse_failure(self) -> None:
        """Parse failure already traces; the catch-all handler must not emit a second trace."""
        tracer = _MockTracer()
        # raw_text is invalid JSON → triggers the parse-failure path which sets _failure_already_traced
        provider = _MockProvider(responses=[ReasoningResponse(raw_text="not valid json")])
        ctx = _make_ctx(provider=provider, tracer=tracer)
        node = create_analysis_node(ctx, max_retries=0)
        node({})
        reasoning_events = [e for e in tracer.events if e.operation_type == "reasoning"]
        # Must still be exactly one — the parse-failure trace, not a second catch-all trace
        assert len(reasoning_events) == 1
        assert not reasoning_events[0].success

    def test_retry_augmented_prompt_does_not_include_failure_messages(self) -> None:
        """Retry augmented prompt must not embed raw exception messages from prior attempts."""
        sensitive_error_message = "api_key=SECRET_KEY_12345"
        recorded_prompts: list[str] = []
        call_count = 0
        success_response = ReasoningResponse(
            raw_text=json.dumps({"plan": "ok"}),
            parsed_output={"plan": "ok"},
        )

        class _FailThenSucceedProvider:
            def invoke(self, prompt, *, tools=None, output_schema=None, model=None):  # noqa: ANN001, ANN003, ANN201
                nonlocal call_count
                call_count += 1
                recorded_prompts.append(prompt)
                if call_count == 1:
                    raise ValueError(sensitive_error_message)
                return success_response

        ctx = _make_ctx(provider=_FailThenSucceedProvider())
        node = create_analysis_node(ctx, max_retries=2)
        result = node({})
        assert result["status"] == "completed"
        assert len(recorded_prompts) == 2
        # The retry prompt must NOT contain the sensitive error message
        assert sensitive_error_message not in recorded_prompts[1]
        # It should contain attempt metadata
        assert "retry attempt" in recorded_prompts[1]
