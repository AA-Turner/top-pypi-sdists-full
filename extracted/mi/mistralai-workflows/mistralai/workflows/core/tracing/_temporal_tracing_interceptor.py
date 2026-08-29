import hashlib
import time
from typing import (
    Any,
    Mapping,
    Type,
)

import opentelemetry
import opentelemetry.baggage
import opentelemetry.context
import opentelemetry.trace
import structlog
import temporalio
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
from opentelemetry.trace import StatusCode
from temporalio.client import Interceptor
from temporalio.contrib.opentelemetry import TracingInterceptor, TracingWorkflowInboundInterceptor, workflow
from temporalio.contrib.pydantic import PydanticPayloadConverter
from temporalio.converter import PayloadConverter

from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.encoding.trace_encoder import TraceEncoder
from mistralai.workflows.core.tracing._otel_config import (
    FORCE_SPAN_ID_ATTRIBUTE,
    FORCE_TRACE_ID_ATTRIBUTE,
    WORKFLOW_ROOT_ID_GENERATOR,
)
from mistralai.workflows.core.tracing.utils import (
    CUSTOM_TRACING_ATTRIBUTES,
    USER_TRACEPARENT_HEADER,
    WORKFLOW_EXECUTION_ID_ATTRIBUTE,
    get_span_attributes,
    workflow_execution_span_attributes,
)
from mistralai.workflows.models import EventAttributes, EventSpanType

logger = structlog.get_logger(__name__)


def _non_zero_hex(value: bytes, width: int) -> str:
    return f"{int.from_bytes(value, byteorder='big') or 1:0{width}x}"


def _deterministic_workflow_traceparent(namespace: str, workflow_id: str, run_id: str) -> str:
    digest = hashlib.sha256(f"{namespace}:{workflow_id}:{run_id}".encode("utf-8")).digest()
    trace_id = _non_zero_hex(digest[:16], 32)
    span_id = _non_zero_hex(digest[16:24], 16)
    return f"00-{trace_id}-{span_id}-01"


def _carrier_has_valid_span(
    propagator: Any,
    carrier: Mapping[str, Any],
) -> bool:
    context = propagator.extract(carrier, context=opentelemetry.context.Context())
    return opentelemetry.trace.get_current_span(context).get_span_context().is_valid


def _traceparent_flags(traceparent: str) -> int | None:
    parts = traceparent.split("-")
    if len(parts) != 4 or len(parts[3]) != 2:
        return None
    try:
        return int(parts[3], 16)
    except ValueError:
        return None


def _sampled_by_rate(trace_id_hex: str, sample_rate: float) -> bool:
    # Reuse OTel's own sampler (the same class the provider's ParentBasedTraceIdRatio uses for root
    # spans) so this decision cannot drift from what the root span's sampler computes for the same id.
    result = TraceIdRatioBased(sample_rate).should_sample(None, int(trace_id_hex, 16), "")
    return bool(result.decision.is_sampled())


def _apply_sample_rate(carrier: dict[str, Any], sample_rate: float) -> dict[str, Any]:
    # The single trace-level sampling decision: set the carrier flag from the rate so children (via
    # ParentBased) and the forced root (via the emit gate + WorkflowSampler) all follow this one flag.
    traceparent = carrier.get("traceparent")
    if not traceparent:
        return carrier
    parts = traceparent.split("-")
    if len(parts) != 4:
        return carrier
    try:
        sampled = _sampled_by_rate(parts[1], sample_rate)
    except ValueError:
        return carrier
    parts[3] = "01" if sampled else "00"
    return {**carrier, "traceparent": "-".join(parts)}


def _traceparent_is_sampled(traceparent: str) -> bool:
    flags = _traceparent_flags(traceparent)
    return flags is not None and bool(flags & 0x01)


def _carrier_with_workflow_execution_baggage(
    propagator: Any,
    carrier: Mapping[str, Any],
    execution_id: str | None,
) -> dict[str, Any]:
    if not execution_id:
        return dict(carrier)

    context = propagator.extract(carrier, context=opentelemetry.context.Context())
    context = opentelemetry.baggage.set_baggage(
        WORKFLOW_EXECUTION_ID_ATTRIBUTE,
        execution_id,
        context=context,
    )
    enriched_carrier = dict(carrier)
    propagator.inject(enriched_carrier, context=context)
    return enriched_carrier


class _MistralTracingWorkflowInboundInterceptor(TracingWorkflowInboundInterceptor):
    def _load_workflow_context_carrier(self) -> dict[str, Any] | None:
        carrier = super()._load_workflow_context_carrier()
        info = temporalio.workflow.info()
        if carrier and _carrier_has_valid_span(self.text_map_propagator, carrier):
            # Only the top-level workflow's first run decides sampling; children and
            # continue-as-new/reset runs honor the propagated decision to avoid partial traces.
            is_root_first_run = info.parent is None and info.run_id == info.first_execution_run_id
            user_provided = USER_TRACEPARENT_HEADER in info.headers
            if is_root_first_run and not user_provided:
                carrier = _apply_sample_rate(carrier, config.common.otel_sample_rate)
        else:
            carrier = _apply_sample_rate(
                {
                    **(carrier or {}),
                    "traceparent": _deterministic_workflow_traceparent(info.namespace, info.workflow_id, info.run_id),
                },
                config.common.otel_sample_rate,
            )

        carrier = _carrier_with_workflow_execution_baggage(
            self.text_map_propagator,
            carrier,
            info.workflow_id,
        )
        self._workflow_context_carrier = carrier
        return carrier

    async def execute_workflow(self, input: temporalio.worker.ExecuteWorkflowInput) -> Any:
        self._maybe_emit_workflow_root_span()
        return await super().execute_workflow(input)

    def _maybe_emit_workflow_root_span(self) -> None:
        # Emit once, from the first run of the chain; continue-as-new/reset runs inherit it via propagation.
        # This runs inside Temporal's deterministic sandbox, which can't create real OTel spans, so we
        # use _completed_span() (a sandbox-safe recording) and pass the desired ids as attributes.
        # They're picked up on the host side by _completed_workflow_span().
        info = temporalio.workflow.info()
        if (
            temporalio.workflow.unsafe.is_replaying()
            or info.parent is not None
            or info.run_id != info.first_execution_run_id
        ):
            return
        carrier = self._load_workflow_context_carrier()
        traceparent = carrier.get("traceparent") if carrier else None
        if not traceparent:
            return
        parts = traceparent.split("-")
        if len(parts) < 4:
            return
        # Skip the forced root when the trace is unsampled; children are dropped, so it would be an orphan.
        if not _traceparent_is_sampled(traceparent):
            return
        trace_id_hex, span_id_hex = parts[1], parts[2]
        # Attach an empty OTel context so the span has no parent (making it a true root). The FORCE_*
        # attributes carry the desired ids across the sandbox boundary; the workflow id lets dora scope it.
        token = opentelemetry.context.attach(opentelemetry.context.Context())
        try:
            self._completed_span(
                f"StartWorkflow:{info.workflow_type}",
                additional_attributes={
                    FORCE_TRACE_ID_ATTRIBUTE: trace_id_hex,
                    FORCE_SPAN_ID_ATTRIBUTE: span_id_hex,
                    **workflow_execution_span_attributes(info.workflow_id),
                    "temporalRunID": info.run_id,
                },
                kind=opentelemetry.trace.SpanKind.SERVER,
            )
        finally:
            opentelemetry.context.detach(token)


class MistralTemporalTracingInterceptor(TracingInterceptor):
    def workflow_interceptor_class(
        self, input: temporalio.worker.WorkflowInterceptorClassInput
    ) -> type[TracingWorkflowInboundInterceptor]:
        super().workflow_interceptor_class(input)
        return _MistralTracingWorkflowInboundInterceptor

    def _completed_workflow_span(self, params: Any) -> Any:
        # This runs on the host side, outside Temporal's sandbox, where real OTel spans are created.
        # If the sandbox side (_maybe_emit_workflow_root_span) smuggled forced ids via attributes, we
        # pop them here and prime the id generator so the next span OTel creates gets exactly those ids.
        # Only StartWorkflow spans carry the FORCE_* attributes; all others pass through to super() with
        # random ids.
        attributes = params.attributes or {}
        span_id_hex = attributes.pop(FORCE_SPAN_ID_ATTRIBUTE, None)
        trace_id_hex = attributes.pop(FORCE_TRACE_ID_ATTRIBUTE, None)
        if span_id_hex is None:
            return super()._completed_workflow_span(params)
        WORKFLOW_ROOT_ID_GENERATOR.prime(
            trace_id=int(trace_id_hex, 16) if trace_id_hex else None,
            span_id=int(span_id_hex, 16),
        )
        try:
            return super()._completed_workflow_span(params)
        finally:
            WORKFLOW_ROOT_ID_GENERATOR.clear()


class TraceDataSerializer:
    MAX_ARG_TRACE_SIZE = 1024 * 512

    _converter = PydanticPayloadConverter()
    _trace_encoder: TraceEncoder | None = None

    @classmethod
    def _get_trace_encoder(cls) -> TraceEncoder:
        if cls._trace_encoder is None:
            cls._trace_encoder = TraceEncoder(encryption_config=config.worker.temporal_payload_encryption)
        return cls._trace_encoder

    def serialize(self, obj: Any) -> str:
        converted = self._converter.to_payload(obj)
        serialized = self._get_trace_encoder().encode_trace_data(converted.data.decode())
        if len(serialized) > TraceDataSerializer.MAX_ARG_TRACE_SIZE:
            return serialized[: TraceDataSerializer.MAX_ARG_TRACE_SIZE] + "..."

        return serialized


def _get_custom_attributes_from_memo() -> dict[str, str] | None:
    """Extract custom tracing attributes either from memo, or headers if we're in a sub-workflow
    Inject them into input headers
    """
    workflow_memo = temporalio.workflow.memo()
    if custom_attrs := workflow_memo.get(CUSTOM_TRACING_ATTRIBUTES):
        return PayloadConverter.default.from_payload(custom_attrs, dict[str, str])
    return None


class _TracingWorkflowInboundInterceptor(temporalio.worker.WorkflowInboundInterceptor):
    """Tracing for workflow results including all the workflow param & duration
    Rely on workflow.completed_span provided by the official OTeL implementation to ensure temporal compliance
    regarding determinism to not break the replay.
    """

    def __init__(self, next: temporalio.worker.WorkflowInboundInterceptor) -> None:
        super().__init__(next)
        self.tracer = opentelemetry.trace.get_tracer(__name__)
        self.trace_serializer = TraceDataSerializer()

    def init(self, outbound: temporalio.worker.WorkflowOutboundInterceptor) -> None:
        self.next.init(_TracingWorkflowOutboundInterceptor(outbound))

    async def execute_workflow(self, input: temporalio.worker.ExecuteWorkflowInput) -> Any:
        result: Any = None
        exc: Exception | None = None
        start_ns = temporalio.workflow.time_ns()
        workflow_info = temporalio.workflow.info()

        custom_attributes = _get_custom_attributes_from_memo()

        workflow.completed_span(
            f"WorkflowInit:{workflow_info.workflow_type}",
            attributes={
                **get_span_attributes(
                    event_type=workflow_info.workflow_type,
                    span_type=EventSpanType.workflow_init,
                    custom_attributes=custom_attributes,
                ),
                EventAttributes.arguments: self.trace_serializer.serialize(input.args),
                EventAttributes.workflow_max_attempts: config.worker.retry_policy_max_attempts,
            },
            exception=exc,
        )

        try:
            result = await super().execute_workflow(input)
            return result
        except Exception as e:
            exc = e
            raise
        finally:
            workflow_info = temporalio.workflow.info()
            duration_ms = (temporalio.workflow.time_ns() - start_ns) // 1_000_000
            attributes = {
                EventAttributes.workflow_duration_ms: duration_ms,
                EventAttributes.arguments: self.trace_serializer.serialize(input.args),
                EventAttributes.workflow_attempt: workflow_info.attempt,
                EventAttributes.workflow_max_attempts: config.worker.retry_policy_max_attempts,
                **get_span_attributes(
                    event_type=workflow_info.workflow_type,
                    span_type=EventSpanType.workflow_report,
                    custom_attributes=custom_attributes,
                ),
            }
            if exc is None:
                attributes[EventAttributes.result] = self.trace_serializer.serialize(result)
            workflow.completed_span(
                f"WorkflowReport:{workflow_info.workflow_type}", attributes=attributes, exception=exc
            )

    async def handle_signal(self, input: temporalio.worker.HandleSignalInput) -> None:
        custom_attributes = _get_custom_attributes_from_memo()
        with self.tracer.start_as_current_span(
            f"ExecuteSignal:{input.signal}",
            attributes={
                **get_span_attributes(
                    event_type=input.signal,
                    span_type=EventSpanType.signal,
                    custom_attributes=custom_attributes,
                ),
                EventAttributes.arguments: self.trace_serializer.serialize(input.args),
            },
        ) as span:
            try:
                await super().handle_signal(input)
                span.set_status(StatusCode.OK)
            except Exception as e:
                span.record_exception(e)
                span.set_status(StatusCode.ERROR)
                raise

    async def handle_query(self, input: temporalio.worker.HandleQueryInput) -> Any:
        custom_attributes = _get_custom_attributes_from_memo()
        with self.tracer.start_as_current_span(
            f"ExecuteQuery:{input.query}",
            attributes={
                **get_span_attributes(
                    event_type=input.query,
                    span_type=EventSpanType.query,
                    custom_attributes=custom_attributes,
                ),
                EventAttributes.arguments: self.trace_serializer.serialize(input.args),
            },
        ) as span:
            try:
                result = await super().handle_query(input)
                span.set_attribute(EventAttributes.result, self.trace_serializer.serialize(result))
                span.set_status(StatusCode.OK)
            except Exception as e:
                span.record_exception(e)
                span.set_status(StatusCode.ERROR)
                raise

        return result

    def handle_update_validator(self, input: temporalio.worker.HandleUpdateInput) -> None:
        super().handle_update_validator(input)

    async def handle_update_handler(self, input: temporalio.worker.HandleUpdateInput) -> Any:
        custom_attributes = _get_custom_attributes_from_memo()
        with self.tracer.start_as_current_span(
            f"ExecuteUpdate:{input.update}",
            attributes={
                **get_span_attributes(
                    event_type=input.update,
                    span_type=EventSpanType.update,
                    custom_attributes=custom_attributes,
                ),
                EventAttributes.arguments: self.trace_serializer.serialize(input.args),
            },
        ) as span:
            try:
                result = await super().handle_update_handler(input)
                span.set_attribute(EventAttributes.result, self.trace_serializer.serialize(result))
                span.set_status(StatusCode.OK)
            except Exception as e:
                span.record_exception(e)
                span.set_status(StatusCode.ERROR)
                raise

        return result


class _TracingWorkflowOutboundInterceptor(temporalio.worker.WorkflowOutboundInterceptor):
    """Inject custom tracing attributes in headers of activity subcall (as they can't access the memo)
    & forward tracing attributes memo to child workflows
    """

    def _enrich_headers_custom_tracing_attrs(self, headers: Mapping[str, Any]) -> Mapping[str, Any]:
        custom_attributes = _get_custom_attributes_from_memo()
        if custom_attributes is not None:
            encoded_custom_attrs = PayloadConverter.default.to_payload(custom_attributes)
            return {CUSTOM_TRACING_ATTRIBUTES: encoded_custom_attrs, **headers}
        return headers

    def start_activity(self, input: temporalio.worker.StartActivityInput) -> temporalio.workflow.ActivityHandle:
        input.headers = self._enrich_headers_custom_tracing_attrs(input.headers)
        return self.next.start_activity(input)

    def start_local_activity(
        self, input: temporalio.worker.StartLocalActivityInput
    ) -> temporalio.workflow.ActivityHandle:
        input.headers = self._enrich_headers_custom_tracing_attrs(input.headers)
        return self.next.start_local_activity(input)

    async def start_child_workflow(
        self, input: temporalio.worker.StartChildWorkflowInput
    ) -> temporalio.workflow.ChildWorkflowHandle:
        # Forward memo to child workflow
        custom_attributes = _get_custom_attributes_from_memo()
        if custom_attributes:
            input.memo = {
                **(input.memo or {}),
                CUSTOM_TRACING_ATTRIBUTES: PayloadConverter.default.to_payload(custom_attributes),
            }
        return await self.next.start_child_workflow(input)


class _TracingActivityInboundInterceptor(temporalio.worker.ActivityInboundInterceptor):
    def __init__(self, next: temporalio.worker.ActivityInboundInterceptor, tracer: opentelemetry.trace.Tracer) -> None:
        super().__init__(next)
        self.tracer = tracer
        self.trace_serializer = TraceDataSerializer()

    def _extract_custom_attributes_from_headers(self, headers: Mapping[str, Any]) -> dict[str, str] | None:
        custom_attributes: dict[str, str] | None = None
        if CUSTOM_TRACING_ATTRIBUTES in headers:
            custom_attributes = PayloadConverter.default.from_payload(headers[CUSTOM_TRACING_ATTRIBUTES])
        return custom_attributes

    async def execute_activity(self, input: temporalio.worker.ExecuteActivityInput) -> Any:
        activity_info = temporalio.activity.info()
        custom_attributes = self._extract_custom_attributes_from_headers(input.headers)
        schedule_to_start_ms = max(
            0,
            int((activity_info.started_time - activity_info.current_attempt_scheduled_time).total_seconds() * 1000),
        )
        with self.tracer.start_as_current_span(
            f"ExecuteActivity:{activity_info.activity_type}",
            attributes={
                **get_span_attributes(
                    event_type=activity_info.activity_type,
                    span_type=EventSpanType.activity,
                    custom_attributes=custom_attributes,
                ),
                EventAttributes.arguments: self.trace_serializer.serialize(input.args),
                EventAttributes.activity_schedule_to_start_ms: schedule_to_start_ms,
            },
        ) as span:
            start_ns = time.monotonic_ns()
            try:
                # Time only the activity call; the inner finally excludes result serialization below.
                try:
                    result = await super().execute_activity(input)
                finally:
                    span.set_attribute(
                        EventAttributes.activity_execution_ms, (time.monotonic_ns() - start_ns) // 1_000_000
                    )
                span.set_attribute(EventAttributes.result, self.trace_serializer.serialize(result))
                span.set_status(StatusCode.OK)
                return result
            except Exception as e:
                span.record_exception(e)
                span.set_status(StatusCode.ERROR)
                raise


class MistralWorkflowTracingInterceptor(temporalio.client.Interceptor, temporalio.worker.Interceptor):
    def __init__(self, tracer: opentelemetry.trace.Tracer | None = None) -> None:
        self.tracer = tracer or opentelemetry.trace.get_tracer(__name__)

    def intercept_client(self, next: temporalio.client.OutboundInterceptor) -> temporalio.client.OutboundInterceptor:
        return next

    def intercept_activity(
        self, next: temporalio.worker.ActivityInboundInterceptor
    ) -> temporalio.worker.ActivityInboundInterceptor:
        return _TracingActivityInboundInterceptor(next, tracer=self.tracer)

    def workflow_interceptor_class(
        self, input: temporalio.worker.WorkflowInterceptorClassInput
    ) -> Type[_TracingWorkflowInboundInterceptor]:
        return _TracingWorkflowInboundInterceptor


def get_trace_context_interceptors() -> list[Interceptor]:
    # Must wrap EventInterceptor so internal local activities inherit the workflow trace.
    return [MistralTemporalTracingInterceptor(always_create_workflow_spans=True)]


def get_span_recording_interceptors() -> list[Interceptor]:
    # Innermost: serializes args after they are unwrapped and offload-restored.
    if config.common.otel_enabled:
        return [MistralWorkflowTracingInterceptor()]
    return []


def get_temporal_tracing_interceptors() -> list[Interceptor]:
    return [*get_trace_context_interceptors(), *get_span_recording_interceptors()]
