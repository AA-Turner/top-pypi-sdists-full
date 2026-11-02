"""Operation lifecycle, logs, events, and privacy behavior tests."""

import asyncio
import inspect
import logging
from collections.abc import Callable

import pytest
from conftest import SDKHarness, histogram_points, metrics_by_name, point_attributes
from opentelemetry.context import Context
from opentelemetry.sdk.trace import ReadableSpan, Span, SpanProcessor
from opentelemetry.trace import Link, SpanContext, StatusCode, TraceFlags, Tracer, get_current_span

from mistralai.observability.otel import (
    Features,
    InferenceDetails,
    Operation,
    observability,
)
from mistralai.observability.otel import semconv_constants as c
from mistralai.observability.otel.models import (
    ATTR_MISTRAL_OBS_FEATURES_DETECTOR,
    ATTR_MISTRAL_OBS_FEATURES_JUDGE,
    ATTR_MISTRAL_OBS_FEATURES_MODERATION,
)


def test_operation_constructor_hides_sdk_binding() -> None:
    """The internal SDK association should not leak into the public constructor."""
    assert "_observability" not in inspect.signature(Operation).parameters


def test_span_attributes_status_and_exceptions(harness: SDKHarness) -> None:
    """Span attributes, status, and exception recording should be exported."""
    with (
        pytest.raises(RuntimeError, match="boom"),
        harness.observability.operation(
            "chat",
            provider="mistral",
            model="mistral-small",
            attributes={c.ATTR_GEN_AI_REQUEST_MODEL: "override-model"},
        ),
    ):
        message = "boom"
        raise RuntimeError(message)

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    span_attributes = dict(span.attributes or {})
    assert span.name == "chat mistral-small"
    assert span_attributes[c.ATTR_GEN_AI_OPERATION_NAME] == "chat"
    assert span_attributes[c.ATTR_GEN_AI_PROVIDER_NAME] == "mistral"
    assert span_attributes[c.ATTR_GEN_AI_REQUEST_MODEL] == "override-model"
    assert span_attributes["error.type"] == "RuntimeError"
    assert span.status.status_code.name == "ERROR"
    assert span.status.description == "boom"
    assert len(span.events) == 1
    assert span.events[0].name == "exception"


def test_pythonic_convenience_api_records_signals(harness: SDKHarness) -> None:
    """The high-level operation API should emit spans, logs, and metrics."""
    with harness.observability.operation(
        "chat",
        provider="mistral",
        model="mistral-large",
        attributes={"custom.span": "value"},
    ) as operation:
        operation.inference_details(
            output_messages=[{"role": "assistant", "content": "hello"}],
            attributes={"custom.event": "value"},
        )
        operation.evaluation_result("quality", score_value=0.9, score_label="pass")
        operation.token_usage(input_tokens=2, output_tokens=3)

    harness.observability.flush()

    span = harness.span_exporter.get_finished_spans()[0]
    span_attributes = dict(span.attributes or {})
    assert span.name == "chat mistral-large"
    assert span_attributes["custom.span"] == "value"
    assert span_attributes[c.ATTR_GEN_AI_PROVIDER_NAME] == "mistral"
    assert span_attributes[c.ATTR_GEN_AI_REQUEST_MODEL] == "mistral-large"
    assert c.ATTR_GEN_AI_RESPONSE_MODEL not in span_attributes

    logs = harness.log_exporter.get_finished_logs()
    assert [log.log_record.event_name for log in logs] == [
        c.EVENT_INFERENCE_DETAILS,
        c.EVENT_EVALUATION_RESULT,
    ]
    inference_attributes = dict(logs[0].log_record.attributes or {})
    assert inference_attributes["custom.event"] == "value"
    assert inference_attributes[c.ATTR_GEN_AI_OPERATION_NAME] == "chat"
    assert inference_attributes[c.ATTR_GEN_AI_REQUEST_MODEL] == "mistral-large"
    assert inference_attributes[c.ATTR_GEN_AI_OUTPUT_MESSAGES] == ({"role": "assistant", "content": "hello"},)

    collected_metrics = metrics_by_name(harness.metric_reader.get_metrics_data())
    token_points = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_TOKEN_USAGE])
    assert {point_attributes(point)[c.ATTR_GEN_AI_TOKEN_TYPE]: point.sum for point in token_points} == {
        c.TOKEN_TYPE_INPUT: 2,
        c.TOKEN_TYPE_OUTPUT: 3,
    }
    duration_point = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_OPERATION_DURATION])[0]
    assert duration_point.sum > 0


def test_conversation_context_applies_to_operation_spans_and_logs_not_metrics(harness: SDKHarness) -> None:
    """Conversation context should correlate operation spans and logs without touching metric attrs."""
    with harness.observability.conversation("conv_123", compacted=True):
        with harness.observability.operation("chat", provider="mistral", model="mistral-small") as operation:
            operation.log("queued")
            operation.event("mistral.obs.operation.checkpoint", "started")
            operation.inference_details(output_messages=[{"role": "assistant", "content": "hello"}])
            operation.evaluation_result("quality", score_label="pass")
            operation.token_usage(input_tokens=2, output_tokens=3)

        operation.evaluation_result("delayed-quality", score_label="pass")

    harness.observability.flush()

    span = harness.span_exporter.get_finished_spans()[0]
    span_attributes = dict(span.attributes or {})
    assert span_attributes[c.ATTR_GEN_AI_CONVERSATION_ID] == "conv_123"
    assert span_attributes[c.ATTR_GEN_AI_CONVERSATION_COMPACTED] is True

    logs = harness.log_exporter.get_finished_logs()
    assert len(logs) == 5
    for log in logs:
        log_attributes = dict(log.log_record.attributes or {})
        assert log_attributes[c.ATTR_GEN_AI_CONVERSATION_ID] == "conv_123"
        assert log_attributes[c.ATTR_GEN_AI_CONVERSATION_COMPACTED] is True

    collected_metrics = metrics_by_name(harness.metric_reader.get_metrics_data())
    for metric in collected_metrics.values():
        for point in histogram_points(metric):
            attributes = point_attributes(point)
            assert c.ATTR_GEN_AI_CONVERSATION_ID not in attributes
            assert c.ATTR_GEN_AI_CONVERSATION_COMPACTED not in attributes


def test_operation_conversation_overrides_context_and_inherits_to_children(harness: SDKHarness) -> None:
    """Explicit operation conversation fields should win and propagate to child operations."""
    with (
        harness.observability.conversation("context-conv", compacted=True),
        harness.observability.operation(
            "chat",
            conversation_id="explicit-conv",
            conversation_compacted=False,
        ) as parent,
    ):
        with harness.observability.tool("lookup", parent=parent):
            pass

        with harness.observability.operation("chat", parent=parent) as child:
            child.log("child log")

    harness.observability.flush()

    spans = harness.span_exporter.get_finished_spans()
    assert len(spans) == 3
    for span in spans:
        span_attributes = dict(span.attributes or {})
        assert span_attributes[c.ATTR_GEN_AI_CONVERSATION_ID] == "explicit-conv"
        assert span_attributes[c.ATTR_GEN_AI_CONVERSATION_COMPACTED] is False

    log_attributes = dict(harness.log_exporter.get_finished_logs()[0].log_record.attributes or {})
    assert log_attributes[c.ATTR_GEN_AI_CONVERSATION_ID] == "explicit-conv"
    assert log_attributes[c.ATTR_GEN_AI_CONVERSATION_COMPACTED] is False


def test_operation_supports_explicit_start_and_end(harness: SDKHarness) -> None:
    """Operations should support manual start and end lifecycle calls."""
    operation = harness.observability.operation("chat", provider="mistral", model="mistral-large")

    operation.start()
    operation.evaluation_result("quality", score_label="pass")
    operation.end()

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    assert span.context is not None
    assert operation.trace_id == f"{span.context.trace_id:032x}"
    assert operation.span_id == f"{span.context.span_id:016x}"
    log = harness.log_exporter.get_finished_logs()[0].log_record
    assert log.event_name == c.EVENT_EVALUATION_RESULT
    assert log.trace_id == span.context.trace_id
    assert log.span_id == span.context.span_id


def test_start_can_skip_attaching_current_context(harness: SDKHarness) -> None:
    """`set_current_context=False` starts the span without attaching context."""
    operation = harness.observability.operation("chat", provider="mistral", model="mistral-large")

    operation.start(set_current_context=False)
    current = get_current_span().get_span_context()
    operation.end()

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    assert span.context is not None
    assert current.span_id != span.context.span_id
    assert operation.span_id == f"{span.context.span_id:016x}"


def test_start_and_end_can_run_in_separate_tasks(harness: SDKHarness, caplog: pytest.LogCaptureFixture) -> None:
    """Operations started and ended in different asyncio tasks keep explicit parents and detach cleanly."""
    agent = harness.observability.agent("agent")
    tool = harness.observability.tool("search", call_id="call-1")

    async def run(callback: Callable[[], object]) -> None:
        callback()

    async def observe_in_separate_tasks() -> None:
        await asyncio.create_task(run(lambda: agent.start(set_current_context=False)))
        await asyncio.create_task(run(lambda: tool.start(parent=agent, set_current_context=False)))
        await asyncio.create_task(run(tool.end))
        await asyncio.create_task(run(agent.end))

    with caplog.at_level(logging.ERROR, logger="opentelemetry.context"):
        asyncio.run(observe_in_separate_tasks())

    assert [record for record in caplog.records if record.name == "opentelemetry.context"] == []
    harness.observability.flush()
    spans = harness.span_exporter.get_finished_spans()
    assert len(spans) == 2
    tool_span, agent_span = spans
    assert tool_span.context is not None
    assert agent_span.context is not None
    assert tool.span_id == f"{tool_span.context.span_id:016x}"
    assert agent.span_id == f"{agent_span.context.span_id:016x}"
    assert tool_span.parent is not None
    assert tool_span.parent.span_id == agent_span.context.span_id
    assert tool_span.context.trace_id == agent_span.context.trace_id


def test_end_with_error_type_sets_span_status_and_error_type(harness: SDKHarness) -> None:
    """`end(error_type=...)` marks the span errored and labels the duration metric."""
    operation = harness.observability.operation("chat", provider="mistral", model="mistral-large")

    operation.start(set_current_context=False)
    operation.end(error_type="provider")

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    assert span.status.status_code.name == "ERROR"
    assert dict(span.attributes or {})[c.ATTR_ERROR_TYPE] == "provider"
    assert span.status.description is None
    assert not span.events


@pytest.mark.parametrize("error_message", ["Session API rejected agents.spawn (HTTP 403)", ""])
def test_end_records_error_message_without_metric_labels_or_exception_events(
    harness: SDKHarness, error_message: str
) -> None:
    """Payload failures retain their description without inventing an exception or metric label."""
    operation = harness.observability.tool("agents.spawn", call_id="call-1")
    operation.start(set_current_context=False, start_time_unix_nano=1_000_000_000)
    operation.end(
        error_type="session_procedure_rejected",
        error_message=error_message,
        end_time_unix_nano=3_500_000_000,
    )
    operation.end(error_type="ignored", error_message="ignored")

    harness.observability.flush()
    [span] = harness.span_exporter.get_finished_spans()
    assert span.status.status_code is StatusCode.ERROR
    assert span.status.description == error_message
    assert dict(span.attributes or {})[c.ATTR_ERROR_TYPE] == "session_procedure_rejected"
    assert c.ATTR_GEN_AI_TOOL_CALL_RESULT not in dict(span.attributes or {})
    assert not span.events
    assert span.start_time == 1_000_000_000
    assert span.end_time == 3_500_000_000
    metric = metrics_by_name(harness.metric_reader.get_metrics_data())[c.METRIC_GEN_AI_EXECUTE_TOOL_DURATION]
    [point] = histogram_points(metric)
    assert point.count == 1
    assert point.sum == 2.5
    assert dict(point_attributes(point)) == {
        c.ATTR_GEN_AI_TOOL_NAME: "agents.spawn",
        c.ATTR_ERROR_TYPE: "session_procedure_rejected",
    }


def test_end_rejects_error_message_without_error_type(harness: SDKHarness) -> None:
    """A message without an error type leaves the operation open and unmodified."""
    operation = harness.observability.tool("lookup")
    operation.start(set_current_context=False)

    with pytest.raises(ValueError, match="error_message requires error_type"):
        operation.end(error_message="failed")

    assert operation.is_started
    operation.end()
    harness.observability.flush()
    [span] = harness.span_exporter.get_finished_spans()
    assert span.status.status_code is StatusCode.UNSET
    assert span.status.description is None
    assert c.ATTR_ERROR_TYPE not in dict(span.attributes or {})


def test_end_without_active_span_ignores_error_message(harness: SDKHarness) -> None:
    """Inactive operations remain no-ops even with unmatched error arguments."""
    operation = harness.observability.tool("lookup")
    operation.end(error_message="failed")

    harness.observability.flush()
    assert not harness.span_exporter.get_finished_spans()


def test_start_with_explicit_span_id_and_times_reconstructs_a_recorded_operation(harness: SDKHarness) -> None:
    """A recorded operation keeps its stable span id, parent, timing, and duration."""
    parent = Operation(name="invoke_agent", trace_id="a" * 32, span_id="b" * 16)
    operation = harness.observability.tool("search", call_id="call-1", parent=parent)

    operation.start(set_current_context=False, span_id="c" * 16, start_time_unix_nano=1_000_000_000)
    operation.end(error_type="timeout", end_time_unix_nano=3_500_000_000)

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    assert span.context is not None
    assert span.parent is not None
    assert span.context.trace_id == int("a" * 32, 16)
    assert span.context.span_id == int("c" * 16, 16)
    assert span.parent.span_id == int("b" * 16, 16)
    assert span.start_time == 1_000_000_000
    assert span.end_time == 3_500_000_000
    metric = metrics_by_name(harness.metric_reader.get_metrics_data())[c.METRIC_GEN_AI_EXECUTE_TOOL_DURATION]
    point = histogram_points(metric)[0]
    assert point.sum == 2.5
    assert point_attributes(point)[c.ATTR_ERROR_TYPE] == "timeout"


def test_explicit_span_id_does_not_leak_to_child_spans(harness: SDKHarness) -> None:
    """Pinning one span id leaves the ids of later spans random."""
    pinned = harness.observability.operation("chat", provider="mistral", model="mistral-large")
    pinned.start(set_current_context=False, span_id="d" * 16)
    with harness.observability.operation("chat", provider="mistral", model="mistral-large", parent=pinned) as child:
        pass
    pinned.end()

    assert pinned.span_id == "d" * 16
    assert child.span_id != "d" * 16


class _SpanStartingProcessor(SpanProcessor):
    """Start one span from `on_start`, under the same parent as the span being started."""

    def __init__(self, tracer: Tracer) -> None:
        self._tracer = tracer
        self.started: list[ReadableSpan] = []

    def on_start(self, span: Span, parent_context: Context | None = None) -> None:
        if span.name == "processor":
            return
        processor_span = self._tracer.start_span("processor", context=parent_context)
        processor_span.end()
        assert isinstance(processor_span, ReadableSpan)
        self.started.append(processor_span)


@pytest.mark.parametrize(
    "parent",
    [Operation(name="invoke_agent", trace_id="a" * 32, span_id="b" * 16), None],
    ids=["child", "root"],
)
def test_pinned_ids_are_not_reused_by_spans_started_from_on_start(
    harness: SDKHarness, parent: Operation | None
) -> None:
    """A pinned id serves only the requested span, not a span a processor starts while it starts."""
    processor = _SpanStartingProcessor(harness.observability.tracer)
    harness.observability.tracer_provider.add_span_processor(processor)
    operation = harness.observability.tool("search", parent=parent)

    operation.start(set_current_context=False, span_id="c" * 16, trace_id=None if parent else "e" * 32)

    [processor_span] = processor.started
    assert processor_span.context is not None
    assert operation.span_id == "c" * 16
    assert processor_span.context.span_id != int("c" * 16, 16)
    if parent is not None:
        assert operation.trace_id == "a" * 32
        assert processor_span.context.trace_id == int("a" * 32, 16)
    else:
        assert operation.trace_id == "e" * 32
        assert processor_span.context.trace_id != int("e" * 32, 16)


@pytest.mark.parametrize(
    ("span_id", "trace_id", "error"),
    [
        ("0" * 16, None, "span_id must be a non-zero"),
        ("abc", None, "span_id must be 16 hexadecimal"),
        ("z" * 16, None, "span_id must be 16 hexadecimal"),
        (None, "0" * 32, "trace_id must be a non-zero"),
        (None, "abc", "trace_id must be 32 hexadecimal"),
        (None, "z" * 32, "trace_id must be 32 hexadecimal"),
    ],
    ids=["zero-span", "short-span", "non-hex-span", "zero-trace", "short-trace", "non-hex-trace"],
)
def test_start_rejects_invalid_explicit_ids(
    harness: SDKHarness, span_id: str | None, trace_id: str | None, error: str
) -> None:
    """Explicit span and trace ids must be non-zero hexadecimal identifiers of the right length."""
    operation = harness.observability.operation("chat", provider="mistral", model="mistral-large")

    with pytest.raises(ValueError, match=error):
        operation.start(set_current_context=False, span_id=span_id, trace_id=trace_id)


def test_start_rejects_trace_id_with_a_parent(harness: SDKHarness) -> None:
    """A trace id cannot be pinned on a child, so it is rejected rather than silently ignored."""
    parent = Operation(name="invoke_agent", trace_id="a" * 32, span_id="b" * 16)
    operation = harness.observability.tool("search", parent=parent)

    with pytest.raises(ValueError, match="trace_id only applies to a root operation"):
        operation.start(set_current_context=False, trace_id="e" * 32)

    assert not operation.is_started


def test_explicit_trace_id_starts_a_linked_root_inside_a_current_span(harness: SDKHarness) -> None:
    """A pinned trace id starts a root with its links, even when another span is current."""
    linked = SpanContext(
        trace_id=int("1" * 32, 16),
        span_id=int("2" * 16, 16),
        is_remote=True,
        trace_flags=TraceFlags(TraceFlags.SAMPLED),
    )
    with harness.observability.operation("chat", provider="mistral", model="mistral-large"):
        root = harness.observability.agent("assistant")
        root.start(set_current_context=False, trace_id="e" * 32, links=[Link(linked)])
        root.end()

    harness.observability.flush()
    root_span, _current_span = harness.span_exporter.get_finished_spans()
    assert root.trace_id == "e" * 32
    assert root_span.parent is None
    assert [link.context for link in root_span.links] == [linked]


def test_end_rejects_end_time_before_recorded_start(harness: SDKHarness) -> None:
    """A rejected end time leaves the span open and unmodified."""
    operation = harness.observability.operation("chat", provider="mistral", model="mistral-large")
    operation.start(set_current_context=False, start_time_unix_nano=2_000)

    with pytest.raises(ValueError, match="end_time_unix_nano"):
        operation.end(error_type="timeout", end_time_unix_nano=1_000)

    assert operation.is_started
    operation.end(end_time_unix_nano=3_000)
    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    assert span.status.status_code is StatusCode.UNSET
    assert c.ATTR_ERROR_TYPE not in dict(span.attributes or {})


@pytest.mark.parametrize(
    ("start_time_unix_nano", "end_time_unix_nano"),
    [(1_000_000_000, None), (None, 3_000_000_000)],
    ids=["recorded-start-live-end", "live-start-recorded-end"],
)
def test_end_rejects_mixing_recorded_and_live_times(
    harness: SDKHarness, start_time_unix_nano: int | None, end_time_unix_nano: int | None
) -> None:
    """A span and its duration metric only agree when both times come from the same source."""
    operation = harness.observability.operation("chat", provider="mistral", model="mistral-large")
    operation.start(set_current_context=False, start_time_unix_nano=start_time_unix_nano)

    with pytest.raises(ValueError, match="must be given together"):
        operation.end(end_time_unix_nano=end_time_unix_nano)

    assert operation.is_started


def test_tool_result_serializes_structured_payload_after_start(harness: SDKHarness) -> None:
    """`tool_result` records a serialized result known only when the tool finishes."""
    operation = harness.observability.tool("search", call_id="call-1")

    operation.start(set_current_context=False)
    operation.tool_result({"status": "ok", "rows": 2})
    operation.end()

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    assert dict(span.attributes or {})[c.ATTR_GEN_AI_TOOL_CALL_RESULT] == '{"rows":2,"status":"ok"}'


def test_operation_evaluation_result_uses_stored_ids_without_starting_span(harness: SDKHarness) -> None:
    """Stored span identifiers should correlate delayed evaluation logs."""
    operation = Operation(
        name="evaluation",
        trace_id="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        span_id="bbbbbbbbbbbbbbbb",
        request_model="mistral-small",
        provider_name="mistral",
    )

    operation.evaluation_result("quality", score_label="pass")

    harness.observability.flush()
    assert harness.span_exporter.get_finished_spans() == ()
    log = harness.log_exporter.get_finished_logs()[0].log_record
    assert log.event_name == c.EVENT_EVALUATION_RESULT
    assert log.trace_id == int("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 16)
    assert log.span_id == int("bbbbbbbbbbbbbbbb", 16)
    attributes = dict(log.attributes or {})
    assert attributes[c.ATTR_GEN_AI_EVALUATION_NAME] == "quality"


def test_operation_features_become_span_attributes_and_can_be_overridden(harness: SDKHarness) -> None:
    """Feature objects should become span attrs, with explicit attrs merged last."""
    with harness.observability.operation(
        "chat",
        features=Features(sensitive_data=True, moderation=True, judges=["toxicity", "groundedness"]),
        attributes={
            ATTR_MISTRAL_OBS_FEATURES_DETECTOR: False,
            "custom.operation.flag": "enabled",
        },
    ):
        pass

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    span_attributes = dict(span.attributes or {})
    assert span_attributes[ATTR_MISTRAL_OBS_FEATURES_DETECTOR] is False
    assert span_attributes[ATTR_MISTRAL_OBS_FEATURES_JUDGE] == ("toxicity", "groundedness")
    assert span_attributes[ATTR_MISTRAL_OBS_FEATURES_MODERATION] is True
    assert span_attributes["custom.operation.flag"] == "enabled"


@pytest.mark.parametrize("named_event", [False, True])
def test_operation_logs_inherit_context_attributes_and_features(
    harness: SDKHarness,
    *,
    named_event: bool,
) -> None:
    """Operation logs and named events should inherit context and feature attrs."""
    with harness.observability.operation("chat") as operation:
        if named_event:
            operation.event(
                "mistral.obs.operation.checkpoint",
                "moderation queued",
                features=Features(sensitive_data=True, moderation=True, judges=["quality"]),
                attributes={"custom.log": "value"},
            )
        else:
            operation.log(
                "moderation queued",
                features=Features(sensitive_data=True, moderation=True, judges=["quality"]),
                attributes={"custom.log": "value"},
            )

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    assert span.context is not None
    log = harness.log_exporter.get_finished_logs()[0].log_record
    log_attributes = dict(log.attributes or {})
    expected_event_name = "mistral.obs.operation.checkpoint" if named_event else None
    assert log.event_name == expected_event_name
    assert log.body == "moderation queued"
    assert log.trace_id == span.context.trace_id
    assert log.span_id == span.context.span_id
    assert log_attributes[ATTR_MISTRAL_OBS_FEATURES_DETECTOR] is True
    assert log_attributes[ATTR_MISTRAL_OBS_FEATURES_JUDGE] == ("quality",)
    assert log_attributes[ATTR_MISTRAL_OBS_FEATURES_MODERATION] is True
    assert log_attributes["custom.log"] == "value"


def test_inference_details_emits_explicit_content(harness: SDKHarness) -> None:
    """Inference details should emit exactly the explicit content passed."""
    harness.observability.record_inference_details(
        InferenceDetails(
            request_stream=True,
            response_time_to_first_chunk=0.25,
            input_messages=[{"role": "user", "content": "visible"}],
            output_messages=[{"role": "assistant", "content": "shown"}],
            system_instructions=[{"type": "text", "content": "Answer directly."}],
            prompt_variables={"customer": "acme"},
        )
    )

    harness.observability.flush()
    log = harness.log_exporter.get_finished_logs()[0]
    attributes = dict(log.log_record.attributes or {})
    assert attributes[c.ATTR_GEN_AI_REQUEST_STREAM] is True
    assert attributes[c.ATTR_GEN_AI_RESPONSE_TIME_TO_FIRST_CHUNK] == 0.25
    assert attributes[c.ATTR_GEN_AI_INPUT_MESSAGES] == ({"role": "user", "content": "visible"},)
    assert attributes[c.ATTR_GEN_AI_OUTPUT_MESSAGES] == ({"role": "assistant", "content": "shown"},)
    assert attributes[c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS] == ({"type": "text", "content": "Answer directly."},)
    assert attributes[f"{c.ATTR_GEN_AI_PROMPT_VARIABLE}.customer"] == "acme"


def test_operation_completion_omits_content_by_default(harness: SDKHarness) -> None:
    """Completion helpers should omit message content unless opted in."""
    with harness.observability.operation("chat") as operation:
        operation.completion(output_messages=[{"role": "assistant", "content": "hello"}])

    harness.observability.flush()
    assert harness.log_exporter.get_finished_logs() == ()
    span = harness.span_exporter.get_finished_spans()[0]
    span_attributes = dict(span.attributes or {})
    assert c.ATTR_GEN_AI_INPUT_MESSAGES not in span_attributes
    assert c.ATTR_GEN_AI_OUTPUT_MESSAGES not in span_attributes


def test_shutdown_performs_final_flush() -> None:
    """Shutdown should perform a final flush before closing providers."""
    harness = SDKHarness()
    with harness.observability.operation("chat") as operation:
        operation.evaluation_result("quality")

    observability.shutdown()

    assert len(harness.span_exporter.get_finished_spans()) == 1
    assert len(harness.log_exporter.get_finished_logs()) == 1
    assert c.METRIC_GEN_AI_CLIENT_OPERATION_DURATION in metrics_by_name(harness.metric_reader.get_metrics_data())
