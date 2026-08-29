from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock, patch

import pytest
from opentelemetry import baggage, context, trace
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import NonRecordingSpan, SpanContext, TraceFlags
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from temporalio.converter import PayloadConverter

from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.tracing._temporal_tracing_interceptor import (
    MistralWorkflowTracingInterceptor,
    _apply_sample_rate,
    _carrier_has_valid_span,
    _carrier_with_workflow_execution_baggage,
    _deterministic_workflow_traceparent,
    _MistralTracingWorkflowInboundInterceptor,
    _sampled_by_rate,
    _traceparent_is_sampled,
    get_temporal_tracing_interceptors,
    get_trace_context_interceptors,
)
from mistralai.workflows.core.tracing.utils import USER_TRACEPARENT_HEADER
from mistralai.workflows.models import EventAttributes, SearchAttributes

from .utils import create_test_worker

_UNSAMPLED_TRACEPARENT = f"00-{'a' * 31}1-{'b' * 15}1-00"


def _flags(traceparent: str) -> str:
    return traceparent.split("-")[3]


@workflow.define(name="test-missing-trace-header-workflow")
class MissingTraceHeaderWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "ok"


def _trace_id_from_traceparent(traceparent: str) -> str:
    return traceparent.split("-")[1]


@pytest.mark.asyncio
async def test_missing_workflow_trace_header_uses_deterministic_trace_id(
    temporal_env: Any,
    mock_upsert_search_attributes: Any,
) -> None:
    async with create_test_worker(
        temporal_env,
        workflows=[MissingTraceHeaderWorkflow],
        activities=[],
        interceptors=get_temporal_tracing_interceptors(),
    ):
        workflow_def = get_workflow_definition(MissingTraceHeaderWorkflow)
        assert workflow_def is not None

        handle = await temporal_env.client.start_workflow(
            workflow_def.name,
            id="test-missing-trace-header",
            task_queue="test-task-queue",
        )
        await handle.result()
        description = await handle.describe()

    expected_trace_id = _trace_id_from_traceparent(
        _deterministic_workflow_traceparent(description.namespace, description.id, description.run_id)
    )
    upserted_attrs = mock_upsert_search_attributes.call_args.args[0]
    attrs = {pair.key.name: pair.value for pair in upserted_attrs}

    assert attrs[SearchAttributes.otel_trace_id] == expected_trace_id
    assert attrs[SearchAttributes.otel_trace_id] != "00000000000000000000000000000000"


@pytest.mark.parametrize("sample_rate,expected", [(1.0, True), (0.0, False)])
def test_sampled_by_rate_edges(sample_rate: float, expected: bool) -> None:
    assert _sampled_by_rate("a" * 32, sample_rate) is expected


def test_sampled_by_rate_matches_trace_id_ratio_bound() -> None:
    # Mirrors OTel TraceIdRatioBased: the low 64 bits of the trace id below the bound are sampled.
    rate = 0.5
    bound = round(rate * (1 << 64))
    assert _sampled_by_rate(f"{bound - 1:032x}", rate) is True
    assert _sampled_by_rate(f"{bound + 1:032x}", rate) is False


@pytest.mark.parametrize("sample_rate,expected_flag", [(1.0, "01"), (0.0, "00")])
def test_apply_sample_rate_sets_flag_and_keeps_ids(sample_rate: float, expected_flag: str) -> None:
    traceparent = f"00-{'a' * 32}-{'b' * 16}-00"
    result = _apply_sample_rate({"traceparent": traceparent}, sample_rate)
    assert result["traceparent"] == f"00-{'a' * 32}-{'b' * 16}-{expected_flag}"


@pytest.mark.parametrize(
    "carrier",
    [{}, {"traceparent": "malformed"}, {"traceparent": f"00-{'z' * 32}-{'b' * 16}-01"}],
)
def test_apply_sample_rate_ignores_missing_or_malformed(carrier: dict) -> None:
    assert _apply_sample_rate(carrier, 1.0) == carrier


@pytest.mark.parametrize(
    "traceparent,expected",
    [
        (f"00-{'a' * 32}-{'b' * 16}-01", True),
        (f"00-{'a' * 32}-{'b' * 16}-ff", True),
        (f"00-{'a' * 32}-{'b' * 16}-00", False),
        (f"00-{'a' * 32}-{'b' * 16}-fe", False),
        ("malformed", False),
        (f"00-{'a' * 32}-{'b' * 16}-gg", False),
    ],
)
def test_traceparent_is_sampled_reads_the_sampled_bit(traceparent: str, expected: bool) -> None:
    assert _traceparent_is_sampled(traceparent) is expected


def _emit_root_span(traceparent: str) -> Mock:
    interceptor = _make_inbound_interceptor()
    completed_span = Mock()
    interceptor._completed_span = completed_span  # type: ignore[attr-defined]
    info = SimpleNamespace(
        parent=None,
        run_id="run-1",
        first_execution_run_id="run-1",
        workflow_type="wf-type",
        workflow_id="wf",
    )
    with (
        patch("temporalio.workflow.info", return_value=info),
        patch("temporalio.workflow.unsafe.is_replaying", return_value=False),
        patch.object(interceptor, "_load_workflow_context_carrier", return_value={"traceparent": traceparent}),
    ):
        interceptor._maybe_emit_workflow_root_span()
    return completed_span


def test_root_span_not_emitted_when_trace_unsampled() -> None:
    _emit_root_span(_UNSAMPLED_TRACEPARENT).assert_not_called()


def test_root_span_emitted_when_trace_sampled() -> None:
    _emit_root_span(f"00-{'a' * 31}1-{'b' * 15}1-01").assert_called_once()


def _make_inbound_interceptor() -> _MistralTracingWorkflowInboundInterceptor:
    # Build without the contrib __init__ (needs next/root); the carrier method only touches these attrs.
    interceptor = object.__new__(_MistralTracingWorkflowInboundInterceptor)
    interceptor.header_key = "_tracer-data"
    interceptor.text_map_propagator = CompositePropagator(
        [
            TraceContextTextMapPropagator(),
            W3CBaggagePropagator(),
        ]
    )
    interceptor.payload_converter = PayloadConverter.default
    interceptor._workflow_context_carrier = None
    return interceptor


def _fake_info(
    *,
    traceparent: str,
    carrier_extra: dict[str, str] | None = None,
    user_provided: bool = False,
    parent: object | None = None,
    run_id: str = "run-1",
    first_execution_run_id: str = "run-1",
    workflow_id: str = "wf",
) -> SimpleNamespace:
    carrier = {"traceparent": traceparent, **(carrier_extra or {})}
    headers = {"_tracer-data": PayloadConverter.default.to_payloads([carrier])[0]}
    if user_provided:
        headers[USER_TRACEPARENT_HEADER] = PayloadConverter.default.to_payload(True)
    return SimpleNamespace(
        headers=headers,
        parent=parent,
        run_id=run_id,
        first_execution_run_id=first_execution_run_id,
        namespace="ns",
        workflow_id=workflow_id,
    )


def _load_carrier(info: SimpleNamespace) -> dict:
    interceptor = _make_inbound_interceptor()
    with patch("temporalio.workflow.info", return_value=info):
        carrier = interceptor._load_workflow_context_carrier()
    assert carrier is not None
    return carrier


def test_root_first_run_without_user_traceparent_samples_at_full_rate() -> None:
    carrier = _load_carrier(
        _fake_info(
            traceparent=_UNSAMPLED_TRACEPARENT,
            carrier_extra={"x-existing": "kept"},
            workflow_id="workflow-exec-123",
        )
    )
    context = _make_inbound_interceptor().text_map_propagator.extract(carrier)

    assert _flags(carrier["traceparent"]) == "01"
    assert carrier["traceparent"].split("-")[1] == _UNSAMPLED_TRACEPARENT.split("-")[1]
    assert carrier["x-existing"] == "kept"
    assert baggage.get_baggage(EventAttributes.workflow_execution_id.value, context=context) == "workflow-exec-123"


def test_root_first_run_drops_when_sample_rate_zero() -> None:
    with patch("mistralai.workflows.core.tracing._temporal_tracing_interceptor.config") as cfg:
        cfg.common.otel_sample_rate = 0.0
        carrier = _load_carrier(_fake_info(traceparent=f"00-{'a' * 32}-{'b' * 16}-01"))
    assert _flags(carrier["traceparent"]) == "00"
    assert carrier["traceparent"].split("-")[1] == "a" * 32


def test_root_first_run_with_user_traceparent_honors_unsampled_bit() -> None:
    carrier = _load_carrier(_fake_info(traceparent=_UNSAMPLED_TRACEPARENT, user_provided=True))
    assert _flags(carrier["traceparent"]) == "00"


def test_child_workflow_honors_propagated_sampling() -> None:
    carrier = _load_carrier(
        _fake_info(
            traceparent=_UNSAMPLED_TRACEPARENT,
            parent=object(),
            workflow_id="child-workflow-exec",
        )
    )
    context = _make_inbound_interceptor().text_map_propagator.extract(carrier)
    assert _flags(carrier["traceparent"]) == "00"
    assert baggage.get_baggage(EventAttributes.workflow_execution_id.value, context=context) == "child-workflow-exec"


def test_continue_as_new_run_honors_propagated_sampling() -> None:
    carrier = _load_carrier(
        _fake_info(traceparent=_UNSAMPLED_TRACEPARENT, run_id="run-2", first_execution_run_id="run-1")
    )
    assert _flags(carrier["traceparent"]) == "00"


def test_carrier_helpers_ignore_ambient_context() -> None:
    propagator = CompositePropagator(
        [
            W3CBaggagePropagator(),
            TraceContextTextMapPropagator(),
        ]
    )
    carrier_traceparent = f"00-{'a' * 32}-{'b' * 16}-01"
    ambient = baggage.set_baggage("unrelated-key", "should-not-leak")
    ambient = trace.set_span_in_context(
        NonRecordingSpan(
            SpanContext(
                trace_id=int("c" * 32, 16),
                span_id=int("d" * 16, 16),
                is_remote=True,
                trace_flags=TraceFlags(0x01),
            )
        ),
        ambient,
    )

    token = context.attach(ambient)
    try:
        assert not _carrier_has_valid_span(propagator, {})
        result = _carrier_with_workflow_execution_baggage(
            propagator,
            {"traceparent": carrier_traceparent},
            "workflow-exec-123",
        )
        result_without_traceparent = _carrier_with_workflow_execution_baggage(
            propagator,
            {},
            "workflow-exec-123",
        )
    finally:
        context.detach(token)

    isolated = context.Context()
    extracted = propagator.extract(result, context=isolated)
    extracted_without_traceparent = propagator.extract(result_without_traceparent, context=isolated)

    assert result["traceparent"] == carrier_traceparent
    assert "traceparent" not in result_without_traceparent
    assert baggage.get_baggage("unrelated-key", context=extracted) is None
    assert baggage.get_baggage("unrelated-key", context=extracted_without_traceparent) is None
    assert baggage.get_baggage(EventAttributes.workflow_execution_id.value, context=extracted) == "workflow-exec-123"
    assert (
        baggage.get_baggage(EventAttributes.workflow_execution_id.value, context=extracted_without_traceparent)
        == "workflow-exec-123"
    )
    assert not trace.get_current_span(extracted_without_traceparent).get_span_context().is_valid


@activity(name="tracing_probe_activity")
async def tracing_probe_activity() -> str | None:
    return baggage.get_baggage(EventAttributes.workflow_execution_id.value)


@activity(name="tracing_probe_failing_activity", retry_policy_max_attempts=1)
async def tracing_probe_failing_activity() -> str:
    raise ValueError("activity boom")


@workflow.define(name="tracing-probe-workflow")
class TracingProbeWorkflow:
    @workflow.entrypoint
    async def run(self) -> str | None:
        return await tracing_probe_activity()


@workflow.define(name="tracing-probe-failing-workflow")
class TracingProbeFailingWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return await tracing_probe_failing_activity()


@pytest.mark.parametrize(
    ("workflow_cls", "activity_fn", "span_name", "expect_failure"),
    [
        (TracingProbeWorkflow, tracing_probe_activity, "ExecuteActivity:tracing_probe_activity", False),
        (
            TracingProbeFailingWorkflow,
            tracing_probe_failing_activity,
            "ExecuteActivity:tracing_probe_failing_activity",
            True,
        ),
    ],
)
@pytest.mark.asyncio
async def test_activity_span_records_schedule_to_start_and_execution_ms(
    temporal_env: Any,
    workflow_cls: type,
    activity_fn: Any,
    span_name: str,
    expect_failure: bool,
) -> None:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    # Pass the tracer explicitly so spans land in this exporter regardless of the global provider.
    tracer = provider.get_tracer("test-activity-timing")

    async with create_test_worker(
        temporal_env,
        workflows=[workflow_cls],
        activities=[activity_fn],
        interceptors=[*get_trace_context_interceptors(), MistralWorkflowTracingInterceptor(tracer=tracer)],
    ):
        workflow_def = get_workflow_definition(workflow_cls)
        assert workflow_def is not None

        handle = await temporal_env.client.start_workflow(
            workflow_def.name,
            id=f"test-activity-timing-{'fail' if expect_failure else 'ok'}",
            task_queue="test-task-queue",
        )
        if expect_failure:
            with pytest.raises(Exception):
                await handle.result()
        else:
            result = await handle.result()
            assert result == {"result": "test-activity-timing-ok"}

    activity_spans = [s for s in exporter.get_finished_spans() if s.name == span_name]
    assert len(activity_spans) == 1
    attrs = activity_spans[0].attributes
    assert attrs is not None

    schedule_to_start_ms = attrs.get(EventAttributes.activity_schedule_to_start_ms)
    execution_ms = attrs.get(EventAttributes.activity_execution_ms)
    assert isinstance(schedule_to_start_ms, int) and schedule_to_start_ms >= 0
    assert isinstance(execution_ms, int) and execution_ms >= 0
