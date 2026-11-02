"""Tests for NodeExecutionEvent serialization."""

from agentic_devtools.orchestration.observability_events import (
    LLMCallEvent,
    NodeExecutionEvent,
    ObservabilityEvent,
    ToolCallEvent,
)


class TestObservabilityEvent:
    """Tests for the base ObservabilityEvent dataclass."""

    def test_to_dict_contains_all_envelope_fields(self) -> None:
        event = ObservabilityEvent(
            version=1,
            event_seq=1,
            type="node",
            run_id="abc123",
            timestamp="2024-01-01T00:00:00+00:00",
        )
        d = event.to_dict()
        assert d["version"] == 1
        assert d["event_seq"] == 1
        assert d["type"] == "node"
        assert d["run_id"] == "abc123"
        assert d["timestamp"] == "2024-01-01T00:00:00+00:00"

    def test_frozen_immutable(self) -> None:
        event = ObservabilityEvent(version=1, event_seq=1, type="node", run_id="x", timestamp="t")
        try:
            event.version = 2  # type: ignore[misc]
            assert False, "Should have raised"  # noqa: B011
        except AttributeError:
            pass


class TestNodeExecutionEvent:
    """Tests for NodeExecutionEvent serialization."""

    def test_success_event_serialization(self) -> None:
        event = NodeExecutionEvent(
            version=1,
            event_seq=1,
            type="node",
            run_id="run-1",
            timestamp="2024-01-01T00:00:01+00:00",
            node_name="fetch_issue",
            status="success",
            start_time="2024-01-01T00:00:00+00:00",
            end_time="2024-01-01T00:00:01+00:00",
            duration_ms=1000,
            input_summary={"key": "value"},
            output_summary="result data",
        )
        d = event.to_dict()
        assert d["type"] == "node"
        assert d["node_name"] == "fetch_issue"
        assert d["status"] == "success"
        assert d["duration_ms"] == 1000
        assert d["error_class"] is None
        assert d["retryable"] is None

    def test_failure_event_serialization(self) -> None:
        event = NodeExecutionEvent(
            version=1,
            event_seq=2,
            type="node",
            run_id="run-1",
            timestamp="2024-01-01T00:00:02+00:00",
            node_name="analyze",
            status="failure",
            start_time="2024-01-01T00:00:01+00:00",
            end_time="2024-01-01T00:00:02+00:00",
            duration_ms=500,
            error_class="transient",
            retryable=True,
            error_message="Connection timeout",
        )
        d = event.to_dict()
        assert d["status"] == "failure"
        assert d["error_class"] == "transient"
        assert d["retryable"] is True
        assert d["error_message"] == "Connection timeout"

    def test_skipped_event_serialization(self) -> None:
        event = NodeExecutionEvent(
            version=1,
            event_seq=3,
            type="node",
            run_id="run-1",
            timestamp="2024-01-01T00:00:00+00:00",
            node_name="optional_step",
            status="skipped",
            start_time="2024-01-01T00:00:00+00:00",
            end_time="2024-01-01T00:00:00+00:00",
            duration_ms=0,
            input_summary=None,
            output_summary=None,
        )
        d = event.to_dict()
        assert d["status"] == "skipped"
        assert d["duration_ms"] == 0
        assert d["input_summary"] is None
        assert d["output_summary"] is None


class TestLLMCallEvent:
    """Tests for LLMCallEvent serialization."""

    def test_full_event_serialization(self) -> None:
        event = LLMCallEvent(
            version=1,
            event_seq=1,
            type="llm_call",
            run_id="run-1",
            timestamp="2024-01-01T00:00:00+00:00",
            node_name="analyze",
            node_type="review",
            model="gpt-4o",
            input_tokens=1000,
            output_tokens=500,
            latency_ms=2500,
            validation_result="pass",
            estimated_cost_usd=0.0075,
        )
        d = event.to_dict()
        assert d["type"] == "llm_call"
        assert d["model"] == "gpt-4o"
        assert d["input_tokens"] == 1000
        assert d["estimated_cost_usd"] == 0.0075

    def test_null_tokens_serialization(self) -> None:
        event = LLMCallEvent(
            version=1,
            event_seq=1,
            type="llm_call",
            run_id="run-1",
            timestamp="2024-01-01T00:00:00+00:00",
            node_name="analyze",
            node_type="review",
            model="unknown-model",
            input_tokens=None,
            output_tokens=None,
            latency_ms=1000,
            validation_result="pass",
            estimated_cost_usd=None,
        )
        d = event.to_dict()
        assert d["input_tokens"] is None
        assert d["output_tokens"] is None
        assert d["estimated_cost_usd"] is None


class TestToolCallEvent:
    """Tests for ToolCallEvent serialization."""

    def test_successful_tool_call(self) -> None:
        event = ToolCallEvent(
            version=1,
            event_seq=1,
            type="tool_call",
            run_id="run-1",
            timestamp="2024-01-01T00:00:00+00:00",
            node_name="commit",
            tool_name="git_commit",
            input_params={"message": "feat: add feature"},
            duration_ms=150.5,
            success=True,
            dry_run=False,
            mutating=True,
            tool_result_summary="Committed abc123",
        )
        d = event.to_dict()
        assert d["type"] == "tool_call"
        assert d["tool_name"] == "git_commit"
        assert d["success"] is True
        assert d["mutating"] is True
        assert d["dry_run"] is False

    def test_failed_tool_call(self) -> None:
        event = ToolCallEvent(
            version=1,
            event_seq=1,
            type="tool_call",
            run_id="run-1",
            timestamp="2024-01-01T00:00:00+00:00",
            node_name="commit",
            tool_name="jira_add_comment",
            input_params={},
            duration_ms=500.0,
            success=False,
            dry_run=False,
            mutating=True,
            error_class="tool",
        )
        d = event.to_dict()
        assert d["success"] is False
        assert d["error_class"] == "tool"
