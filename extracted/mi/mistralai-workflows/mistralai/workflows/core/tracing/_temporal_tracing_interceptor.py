from typing import (
    Any,
    Mapping,
    Type,
)

import opentelemetry
import structlog
import temporalio
from opentelemetry.trace import StatusCode
from temporalio.client import Interceptor
from temporalio.contrib.opentelemetry import TracingInterceptor, workflow
from temporalio.contrib.pydantic import PydanticPayloadConverter
from temporalio.converter import PayloadConverter

from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.encoding.trace_encoder import TraceEncoder
from mistralai.workflows.core.tracing.utils import CUSTOM_TRACING_ATTRIBUTES, get_span_attributes
from mistralai.workflows.models import EventAttributes, EventSpanType

logger = structlog.get_logger(__name__)


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
        with self.tracer.start_as_current_span(
            f"ExecuteActivity:{activity_info.activity_type}",
            attributes={
                **get_span_attributes(
                    event_type=activity_info.activity_type,
                    span_type=EventSpanType.activity,
                    custom_attributes=custom_attributes,
                ),
                EventAttributes.arguments: self.trace_serializer.serialize(input.args),
            },
        ) as span:
            try:
                result = await super().execute_activity(input)
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


def get_temporal_tracing_interceptors() -> list[Interceptor]:
    # TracingInterceptor handles trace context propagation from Temporal headers.
    # always_create_workflow_spans=True ensures scheduled workflows get their own trace
    # instead of polluting other workflow traces.
    interceptors: list[Interceptor] = [TracingInterceptor(always_create_workflow_spans=True)]
    if config.common.otel_enabled:
        interceptors.append(MistralWorkflowTracingInterceptor())
    return interceptors
