"""Trace context parenting and propagation tests."""

from conftest import SDKHarness
from opentelemetry import context as context_api
from opentelemetry import propagate, trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import NonRecordingSpan, SpanContext, TraceFlags, TraceState

from mistralai.observability.otel import Operation
from mistralai.observability.otel import semconv_constants as c


def test_current_otel_context_parents_operation_without_using_context_provider_exporter(harness: SDKHarness) -> None:
    """Current OTel context should parent SDK spans while exporters stay isolated."""
    monitoring_span_exporter = InMemorySpanExporter()
    monitoring_provider = TracerProvider()
    monitoring_provider.add_span_processor(SimpleSpanProcessor(monitoring_span_exporter))
    monitoring_tracer = monitoring_provider.get_tracer("monitoring")

    try:
        with monitoring_tracer.start_as_current_span("monitoring-request") as monitoring_span:
            monitoring_context = monitoring_span.get_span_context()
            with harness.observability.operation("chat") as operation:
                operation.log("owned by mistralai observability")

        harness.observability.flush()
        monitoring_provider.force_flush()

        sdk_span = harness.span_exporter.get_finished_spans()[0]
        assert sdk_span.context is not None
        assert sdk_span.parent is not None
        assert operation.trace_id == f"{monitoring_context.trace_id:032x}"
        assert f"{sdk_span.context.trace_id:032x}" == f"{monitoring_context.trace_id:032x}"
        assert sdk_span.parent.span_id == monitoring_context.span_id
        assert [span.name for span in monitoring_span_exporter.get_finished_spans()] == ["monitoring-request"]
        assert [log.log_record.body for log in harness.log_exporter.get_finished_logs()] == [
            "owned by mistralai observability"
        ]
    finally:
        monitoring_provider.shutdown()


def test_operation_accepts_explicit_otel_context_even_when_another_context_is_current(harness: SDKHarness) -> None:
    """High-level operations should parent to explicit context over current context."""
    current_context = trace.set_span_in_context(
        NonRecordingSpan(
            SpanContext(
                trace_id=int("11111111111111111111111111111111", 16),
                span_id=int("2222222222222222", 16),
                is_remote=True,
                trace_flags=TraceFlags(TraceFlags.SAMPLED),
                trace_state=TraceState(),
            )
        )
    )
    explicit_context = trace.set_span_in_context(
        NonRecordingSpan(
            SpanContext(
                trace_id=int("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 16),
                span_id=int("bbbbbbbbbbbbbbbb", 16),
                is_remote=True,
                trace_flags=TraceFlags(TraceFlags.SAMPLED),
                trace_state=TraceState(),
            )
        )
    )

    token = context_api.attach(current_context)
    try:
        with harness.observability.operation("chat", context=explicit_context):
            pass
    finally:
        context_api.detach(token)

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    assert span.context is not None
    assert f"{span.context.trace_id:032x}" == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert span.parent is not None
    assert f"{span.parent.span_id:016x}" == "bbbbbbbbbbbbbbbb"


def test_operation_can_start_from_parent_operation_identity(harness: SDKHarness) -> None:
    """A stored parent operation should create a child span in the same trace."""
    parent = Operation(
        name="chat",
        trace_id="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        span_id="bbbbbbbbbbbbbbbb",
        request_model="mistral-small",
        provider_name="mistral",
    )

    with harness.observability.operation(
        "evaluation",
        parent=parent,
        model="mistral-small",
        provider="mistral",
    ) as operation:
        child_trace_id = operation.trace_id
        child_span_id = operation.span_id
        operation.evaluation_result(
            "moderation",
            score_label="pass",
            response_id="cmpl_123",
        )
        operation.log("evaluated asynchronously")

    harness.observability.flush()

    span = harness.span_exporter.get_finished_spans()[0]
    assert span.context is not None
    assert f"{span.context.trace_id:032x}" == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert child_trace_id == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert child_span_id == f"{span.context.span_id:016x}"
    assert span.parent is not None
    assert f"{span.parent.span_id:016x}" == "bbbbbbbbbbbbbbbb"
    logs = harness.log_exporter.get_finished_logs()
    assert len(logs) == 2
    assert {log.log_record.trace_id for log in logs} == {int("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 16)}
    assert {log.log_record.span_id for log in logs} == {span.context.span_id}
    evaluation_attributes = dict(logs[0].log_record.attributes or {})
    assert logs[0].log_record.event_name == c.EVENT_EVALUATION_RESULT
    assert evaluation_attributes[c.ATTR_GEN_AI_EVALUATION_NAME] == "moderation"
    assert evaluation_attributes[c.ATTR_GEN_AI_RESPONSE_ID] == "cmpl_123"


def test_arbitrary_span_uses_current_operation_context_without_genai_attributes(harness: SDKHarness) -> None:
    """Low-level spans should reveal local work without adding GenAI semantics."""
    with (
        harness.observability.operation("chat") as operation,
        operation.span("cache.lookup", attributes={"cache.hit": True}) as cache_span,
    ):
        cache_span.set_attribute("cache.backend", "memory")

    harness.observability.flush()

    spans = {span.name: span for span in harness.span_exporter.get_finished_spans()}
    operation_span = spans["chat"]
    cache_lookup_span = spans["cache.lookup"]
    assert operation_span.context is not None
    assert cache_lookup_span.context is not None
    assert cache_lookup_span.parent is not None
    assert cache_lookup_span.context.trace_id == operation_span.context.trace_id
    assert cache_lookup_span.parent.span_id == operation_span.context.span_id
    assert operation.trace_id == f"{operation_span.context.trace_id:032x}"

    cache_attributes = dict(cache_lookup_span.attributes or {})
    assert cache_attributes == {"cache.hit": True, "cache.backend": "memory"}
    assert c.ATTR_GEN_AI_OPERATION_NAME not in cache_attributes


def test_arbitrary_span_can_parent_to_stored_operation_identity(harness: SDKHarness) -> None:
    """Low-level spans should also work when only the parent span ids remain."""
    parent = Operation(
        name="chat",
        trace_id="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        span_id="bbbbbbbbbbbbbbbb",
    )

    with parent.span("cache.rehydrate", attributes={"cache.hit": False}):
        pass

    harness.observability.flush()
    span = harness.span_exporter.get_finished_spans()[0]
    assert span.context is not None
    assert f"{span.context.trace_id:032x}" == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert span.parent is not None
    assert f"{span.parent.span_id:016x}" == "bbbbbbbbbbbbbbbb"
    assert dict(span.attributes or {}) == {"cache.hit": False}


def test_inject_round_trips_current_context(harness: SDKHarness) -> None:
    """Standard OTel propagation should see operation spans in current context."""
    with harness.observability.operation("chat"):
        carrier: dict[str, str] = {}
        propagate.inject(carrier)

    assert "traceparent" in carrier
    assert carrier["traceparent"].startswith("00-")
