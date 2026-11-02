"""OpenTelemetry provider ownership, exporting, and SDK facade."""

import os
import time
import traceback
from collections.abc import Generator, Mapping, Sequence
from contextlib import ExitStack, contextmanager
from contextvars import ContextVar
from importlib.metadata import PackageNotFoundError, version
from typing import Protocol
from urllib.parse import urlsplit, urlunsplit

from opentelemetry import context as context_api
from opentelemetry.context import Context
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, LogRecordExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import MetricExporter, MetricReader, PeriodicExportingMetricReader
from opentelemetry.sdk.metrics.view import ExplicitBucketHistogramAggregation, View
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import SpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter
from opentelemetry.sdk.trace.id_generator import IdGenerator, RandomIdGenerator
from opentelemetry.trace import (
    Link,
    Span,
    SpanKind,
    Status,
    StatusCode,
    get_current_span,
)
from opentelemetry.util.types import AttributeValue

from . import semconv_constants as c
from ._ids import parse_otel_id
from .attributes import normalize_otel_attributes
from .hooks import OperationDataTransformer, OperationDataTransformers
from .models import (
    DEFAULT_METRIC_HISTOGRAM_BOUNDARIES,
    ChatCompletionAdapter,
    EvaluationResult,
    EventAttributeValue,
    ExtendedAttributes,
    Features,
    InferenceDetails,
    ObservabilityConfig,
    Operation,
    OperationDuration,
    StreamingChunk,
    TokenUsage,
    completion_span_attributes,
    evaluation_attributes,
    feature_attributes,
    inference_attributes,
    operation_duration_metric_attributes,
    streaming_chunk_metric_attributes,
    token_usage_metric_attributes,
)
from .redaction import RegexRedactionPolicy

PACKAGE_NAME = "mistralai-otel-observability"
INSTRUMENTATION_NAME = "mistralai.observability.otel"
MISTRAL_TELEMETRY_ENDPOINT = "https://api.mistral.ai/telemetry"
MISTRAL_API_KEY_ENV = "MISTRAL_API_KEY"


def _instrumentation_version() -> str | None:
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:
        return None


INSTRUMENTATION_VERSION = _instrumentation_version()


class _OperationIdGenerator(IdGenerator):
    """Random ids, except for one span or trace id pinned for the current task.

    A pin is consumed by the first id it serves, so a span that a processor
    starts from `on_start` while the pinned span is starting gets a random id.
    """

    def __init__(self) -> None:
        self._random = RandomIdGenerator()
        self._pinned_trace_id: ContextVar[int | None] = ContextVar(
            "mistralai_observability_pinned_trace_id",
            default=None,
        )
        self._pinned_span_id: ContextVar[int | None] = ContextVar(
            "mistralai_observability_pinned_span_id",
            default=None,
        )

    @contextmanager
    def pin_span_id(self, span_id: int) -> Generator[None]:
        token = self._pinned_span_id.set(span_id)
        try:
            yield
        finally:
            self._pinned_span_id.reset(token)

    @contextmanager
    def pin_trace_id(self, trace_id: int) -> Generator[None]:
        token = self._pinned_trace_id.set(trace_id)
        try:
            yield
        finally:
            self._pinned_trace_id.reset(token)

    def generate_span_id(self) -> int:
        span_id = self._pinned_span_id.get()
        if span_id is None:
            return self._random.generate_span_id()
        self._pinned_span_id.set(None)
        return span_id

    def generate_trace_id(self) -> int:
        trace_id = self._pinned_trace_id.get()
        if trace_id is None:
            return self._random.generate_trace_id()
        self._pinned_trace_id.set(None)
        return trace_id


class Clock(Protocol):
    """Monotonic clock interface used by duration helpers."""

    def __call__(self) -> float:
        """Return the current monotonic timestamp in seconds."""
        ...


_configured: "ObservabilitySDK | None" = None
_conversation_context: ContextVar[tuple[str, bool | None] | None] = ContextVar(
    "mistralai_observability_conversation_context",
    default=None,
)


def require_configured() -> "ObservabilitySDK":
    """Return the configured SDK or raise a clear setup error."""
    if _configured is None:
        message = "mistralai.observability.otel.observability.configure() must be called before recording telemetry"
        raise RuntimeError(message)
    return _configured


class Observability:
    """Process-wide facade used by applications to configure and record telemetry."""

    @contextmanager
    def conversation(
        self,
        conversation_id: str,
        *,
        compacted: bool | None = None,
    ) -> Generator[None]:
        """Set default GenAI conversation attributes for operations in this context.

        Use this when the application or provider already has a stable session,
        thread, or conversation identifier. The SDK never generates fallback
        conversation ids because semconv reserves this field for real
        conversation identity across traces.
        """
        with _conversation_scope(conversation_id, compacted=compacted):
            yield

    def configure(
        self,
        config: ObservabilityConfig | None = None,
        *,
        operation_data_transformers: Sequence[OperationDataTransformer] | None = None,
        span_exporter: SpanExporter | None = None,
        span_processors: Sequence[SpanProcessor] | None = None,
        metric_reader: MetricReader | None = None,
        metric_exporter: MetricExporter | None = None,
        log_exporter: LogRecordExporter | None = None,
    ) -> None:
        """Configure the process-wide observability SDK instance.

        The configured instance owns isolated OpenTelemetry trace, metric, and
        log providers. Reconfiguring shuts down the previous owned providers
        first, which keeps tests and short-lived scripts deterministic without
        installing any OpenTelemetry globals. The default regex policy redacts
        known secrets and PII; pass an empty sequence to disable redaction.
        ``span_processors`` are invoked in the given order at both span start
        and end. They run before the SDK's export processor.
        """
        global _configured

        if _configured is not None:
            _configured.shutdown()
        _configured = ObservabilitySDK(
            config,
            operation_data_transformers=operation_data_transformers,
            span_exporter=span_exporter,
            span_processors=span_processors,
            metric_reader=metric_reader,
            metric_exporter=metric_exporter,
            log_exporter=log_exporter,
        )

    def configure_mistral(
        self,
        *,
        service_name: str,
        service_version: str | None = None,
        api_key: str | None = None,
        endpoint: str = MISTRAL_TELEMETRY_ENDPOINT,
        timeout: float | None = None,
        export_interval_millis: int = 5_000,
        resource_attributes: Mapping[str, AttributeValue] | None = None,
        metric_histogram_boundaries: Sequence[float] | None = None,
        operation_data_transformers: Sequence[OperationDataTransformer] | None = None,
    ) -> None:
        """Configure OTLP export for Mistral's telemetry endpoint.

        This is the production-friendly shortcut for sending all three OTLP
        signals to `api.mistral.ai/telemetry`. It resolves authorization from
        the explicit `api_key` or the `MISTRAL_API_KEY` environment variable.
        The default regex policy redacts known secrets and PII; pass an empty
        sequence to disable redaction.
        """
        self.configure(
            ObservabilityConfig(
                service_name=service_name,
                service_version=service_version,
                endpoint=endpoint,
                protocol="http/protobuf",
                headers=_mistral_headers(api_key),
                timeout=timeout,
                export_interval_millis=export_interval_millis,
                resource_attributes=resource_attributes or {},
                metric_histogram_boundaries=metric_histogram_boundaries
                if metric_histogram_boundaries is not None
                else DEFAULT_METRIC_HISTOGRAM_BOUNDARIES,
            ),
            operation_data_transformers=operation_data_transformers,
        )

    def operation(
        self,
        name: str,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        model: str | None = None,
        provider: str | None = None,
        conversation_id: str | None = None,
        conversation_compacted: bool | None = None,
        include_content: bool = False,
        features: Features | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Operation:
        """Create a GenAI operation object without starting its span yet.

        Use the returned `Operation` as a context manager, or call `start()` and
        `end()` explicitly. The operation can also be used as a reference object
        with stored trace/span ids for delayed logs and evaluations.
        """
        return require_configured().operation(
            name,
            context=context,
            parent=parent,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            model=model,
            provider=provider,
            conversation_id=conversation_id,
            conversation_compacted=conversation_compacted,
            include_content=include_content,
            features=features,
            attributes=attributes,
        )

    @contextmanager
    def span(
        self,
        name: str,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Generator[Span]:
        """Start an arbitrary span through the SDK's isolated tracer.

        Use this for local work that is useful in traces but has no GenAI
        semantic-convention shape, such as cache lookups, serialization, or
        provider response parsing. The span is still exported by this SDK's
        private pipeline and can parent or be parented by GenAI operations.
        """
        with require_configured().span(
            name,
            context=context,
            parent=parent,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            kind=kind,
            attributes=attributes,
        ) as span:
            yield span

    def create_agent(
        self,
        name: str | None = None,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        agent_id: str | None = None,
        description: str | None = None,
        version: str | None = None,
        model: str | None = None,
        provider: str | None = None,
        conversation_id: str | None = None,
        conversation_compacted: bool | None = None,
        system_instructions: EventAttributeValue | None = None,
        server_address: str | None = None,
        server_port: int | None = None,
        features: Features | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Operation:
        """Create a span-ready operation for provisioning a hosted GenAI agent.

        This helper represents the semconv `create_agent` client boundary: the
        call that creates or updates an agent resource in a remote service. It
        returns a normal `Operation`, so callers can use it as a context manager
        and attach logs, evaluations, and custom attributes just like chat spans.
        """
        return require_configured().create_agent(
            name,
            context=context,
            parent=parent,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            agent_id=agent_id,
            description=description,
            version=version,
            model=model,
            provider=provider,
            conversation_id=conversation_id,
            conversation_compacted=conversation_compacted,
            system_instructions=system_instructions,
            server_address=server_address,
            server_port=server_port,
            features=features,
            attributes=attributes,
        )

    def agent(
        self,
        name: str | None = None,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        agent_id: str | None = None,
        description: str | None = None,
        version: str | None = None,
        model: str | None = None,
        provider: str | None = None,
        conversation_id: str | None = None,
        conversation_compacted: bool | None = None,
        remote: bool = False,
        features: Features | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Operation:
        """Create a span-ready operation for invoking an agent.

        Agent invocation is distinct from a single model call: it can include
        planning, model calls, tool execution, and intermediate logs. By default
        this records an internal `invoke_agent` span for in-process frameworks;
        pass `remote=True` when the boundary is a remote hosted agent service.
        """
        return require_configured().agent(
            name,
            context=context,
            parent=parent,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            agent_id=agent_id,
            description=description,
            version=version,
            model=model,
            provider=provider,
            conversation_id=conversation_id,
            conversation_compacted=conversation_compacted,
            remote=remote,
            features=features,
            attributes=attributes,
        )

    def tool(
        self,
        name: str,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        call_id: str | None = None,
        description: str | None = None,
        tool_type: str | None = None,
        arguments: EventAttributeValue | None = None,
        result: EventAttributeValue | None = None,
        agent_name: str | None = None,
        conversation_id: str | None = None,
        conversation_compacted: bool | None = None,
        features: Features | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Operation:
        """Create a span-ready operation for executing one tool call.

        Tool execution is modeled as an internal `execute_tool` span and should
        usually be parented to the chat or agent operation that requested it.
        Arguments and result may contain sensitive data, so pass only the fields
        that are appropriate for the configured telemetry destination.
        """
        return require_configured().tool(
            name,
            context=context,
            parent=parent,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            call_id=call_id,
            description=description,
            tool_type=tool_type,
            arguments=arguments,
            result=result,
            agent_name=agent_name,
            conversation_id=conversation_id,
            conversation_compacted=conversation_compacted,
            features=features,
            attributes=attributes,
        )

    def plan(
        self,
        agent_name: str | None = None,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        conversation_id: str | None = None,
        conversation_compacted: bool | None = None,
        features: Features | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Operation:
        """Create a span-ready operation for an agent planning phase.

        A plan span captures task decomposition or strategy selection before
        child model/tool operations run. The GenAI semantic conventions define a
        plan span but no plan duration metric, so ending this operation exports
        the span without recording a synthetic duration metric.
        """
        return require_configured().plan(
            agent_name,
            context=context,
            parent=parent,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            conversation_id=conversation_id,
            conversation_compacted=conversation_compacted,
            features=features,
            attributes=attributes,
        )

    def flush(self, timeout_millis: int = 30_000) -> bool:
        """Flush all owned span, metric, and log pipelines."""
        return require_configured().flush(timeout_millis=timeout_millis)

    def shutdown(self, timeout_millis: int = 30_000) -> None:
        """Flush and close the configured SDK instance if one exists."""
        global _configured

        if _configured is None:
            return
        _configured.shutdown(timeout_millis=timeout_millis)
        _configured = None


observability = Observability()


class ObservabilitySDK:
    """Configured SDK instance that owns isolated OTel providers."""

    def __init__(
        self,
        config: ObservabilityConfig | None = None,
        *,
        operation_data_transformers: Sequence[OperationDataTransformer] | None = None,
        span_exporter: SpanExporter | None = None,
        span_processors: Sequence[SpanProcessor] | None = None,
        metric_reader: MetricReader | None = None,
        metric_exporter: MetricExporter | None = None,
        log_exporter: LogRecordExporter | None = None,
    ) -> None:
        """Create isolated trace, metric, and log pipelines for one configuration."""
        self.config = config or ObservabilityConfig()
        self.clock = time.perf_counter
        configured_transformers = (
            (RegexRedactionPolicy(),) if operation_data_transformers is None else tuple(operation_data_transformers)
        )
        self.operation_data_transformers = OperationDataTransformers(transformers=configured_transformers)
        self._resource = self._build_resource(self.config)

        self._id_generator = _OperationIdGenerator()
        self.tracer_provider = TracerProvider(
            resource=self._resource,
            shutdown_on_exit=False,
            sampler=self.config.sampler,
            id_generator=self._id_generator,
        )
        for span_processor in span_processors or ():
            self.tracer_provider.add_span_processor(span_processor)
        self.tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter or self._build_span_exporter()))
        self.tracer = self.tracer_provider.get_tracer(INSTRUMENTATION_NAME, INSTRUMENTATION_VERSION)

        resolved_metric_reader = metric_reader or PeriodicExportingMetricReader(
            metric_exporter or self._build_metric_exporter(),
            export_interval_millis=self.config.export_interval_millis,
        )
        self.meter_provider = MeterProvider(
            resource=self._resource,
            metric_readers=[resolved_metric_reader],
            shutdown_on_exit=False,
            views=self._build_metric_views(self.config),
        )
        self.meter = self.meter_provider.get_meter(INSTRUMENTATION_NAME, INSTRUMENTATION_VERSION)
        self._operation_duration = self.meter.create_histogram(
            c.METRIC_GEN_AI_CLIENT_OPERATION_DURATION,
            unit="s",
            description="Duration of GenAI client operations.",
        )
        self._token_usage = self.meter.create_histogram(
            c.METRIC_GEN_AI_CLIENT_TOKEN_USAGE,
            unit="{token}",
            description="Token usage for GenAI client operations.",
        )
        self._time_to_first_chunk = self.meter.create_histogram(
            c.METRIC_GEN_AI_CLIENT_OPERATION_TIME_TO_FIRST_CHUNK,
            unit="s",
            description="Time from operation start to first output chunk.",
        )
        self._time_per_output_chunk = self.meter.create_histogram(
            c.METRIC_GEN_AI_CLIENT_OPERATION_TIME_PER_OUTPUT_CHUNK,
            unit="s",
            description="Time between output chunks.",
        )
        self._invoke_agent_duration = self.meter.create_histogram(
            c.METRIC_GEN_AI_INVOKE_AGENT_DURATION,
            unit="s",
            description="Duration of in-process GenAI agent invocations.",
        )
        self._execute_tool_duration = self.meter.create_histogram(
            c.METRIC_GEN_AI_EXECUTE_TOOL_DURATION,
            unit="s",
            description="Duration of GenAI tool executions.",
        )

        self.logger_provider = LoggerProvider(resource=self._resource, shutdown_on_exit=False)
        self.logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(log_exporter or self._build_log_exporter())
        )
        self.logger = self.logger_provider.get_logger(INSTRUMENTATION_NAME, INSTRUMENTATION_VERSION)
        self._shutdown = False

    @contextmanager
    def conversation(
        self,
        conversation_id: str,
        *,
        compacted: bool | None = None,
    ) -> Generator[None]:
        """Set default GenAI conversation attributes for operations in this context."""
        with _conversation_scope(conversation_id, compacted=compacted):
            yield

    def _bind_operation(self, operation: Operation) -> Operation:
        """Associate an SDK-created operation without exposing it in the constructor."""
        operation._observability = self  # pyright: ignore[reportPrivateUsage]
        return operation

    def start_operation_span(
        self,
        name: str,
        *,
        context: Context | None,
        kind: SpanKind,
        attributes: Mapping[str, AttributeValue],
        span_id: str | int | None = None,
        start_time_unix_nano: int | None = None,
        trace_id: str | int | None = None,
        links: Sequence[Link] | None = None,
    ) -> Span:
        """Start an operation span, optionally with caller-owned ids, start time, and links.

        A pinned `trace_id` only applies when the span is a root, so it is
        rejected when `context` carries a parent span. Without a `context`, a
        pinned `trace_id` starts a root span instead of joining the current span.
        """
        if trace_id is not None and context is None:
            context = Context()
        elif trace_id is not None and get_current_span(context).get_span_context().is_valid:
            message = "trace_id only applies to a root operation"
            raise ValueError(message)
        with ExitStack() as stack:
            if span_id is not None:
                stack.enter_context(
                    self._id_generator.pin_span_id(parse_otel_id(span_id, name="span_id", hex_digits=16))
                )
            if trace_id is not None:
                stack.enter_context(
                    self._id_generator.pin_trace_id(parse_otel_id(trace_id, name="trace_id", hex_digits=32))
                )
            return self.tracer.start_span(
                name,
                context=context,
                kind=kind,
                attributes=attributes,
                links=links,
                start_time=start_time_unix_nano,
            )

    def operation(
        self,
        name: str,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        model: str | None = None,
        provider: str | None = None,
        conversation_id: str | None = None,
        conversation_compacted: bool | None = None,
        include_content: bool = False,
        features: Features | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Operation:
        """Create an unstarted operation using this configured SDK."""
        return self.create_operation(
            name,
            context=context,
            parent=parent,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            model=model,
            provider=provider,
            conversation_id=conversation_id,
            conversation_compacted=conversation_compacted,
            include_content=include_content,
            features=features,
            attributes=attributes,
        )

    def create_operation(
        self,
        name: str,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        model: str | None = None,
        provider: str | None = None,
        conversation_id: str | None = None,
        conversation_compacted: bool | None = None,
        include_content: bool = False,
        features: Features | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Operation:
        """Build a generic GenAI operation with common high-level fields."""
        resolved_parent = _operation_parent(parent, trace_id, parent_span_id)
        operation = Operation(
            name=name,
            context=context,
            parent=resolved_parent,
            provider_name=provider,
            request_model=model,
            conversation_id=_resolve_conversation_id(conversation_id, resolved_parent),
            conversation_compacted=_resolve_conversation_compacted(conversation_compacted, resolved_parent),
            include_content=include_content,
            attributes=_operation_attributes(
                attributes,
                features=features,
            ),
        )
        return self._bind_operation(operation)

    def create_agent(
        self,
        name: str | None = None,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        agent_id: str | None = None,
        description: str | None = None,
        version: str | None = None,
        model: str | None = None,
        provider: str | None = None,
        conversation_id: str | None = None,
        conversation_compacted: bool | None = None,
        system_instructions: EventAttributeValue | None = None,
        server_address: str | None = None,
        server_port: int | None = None,
        features: Features | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Operation:
        """Build a `create_agent` operation backed by this configured SDK."""
        resolved_parent = _operation_parent(parent, trace_id, parent_span_id)
        operation = Operation(
            name=c.OPERATION_NAME_CREATE_AGENT,
            context=context,
            parent=resolved_parent,
            kind=SpanKind.CLIENT,
            provider_name=provider,
            request_model=model,
            conversation_id=_resolve_conversation_id(conversation_id, resolved_parent),
            conversation_compacted=_resolve_conversation_compacted(conversation_compacted, resolved_parent),
            agent_id=agent_id,
            agent_name=name,
            agent_description=description,
            agent_version=version,
            system_instructions=system_instructions,
            server_address=server_address,
            server_port=server_port,
            duration_metric="client_operation",
            attributes=_operation_attributes(
                attributes,
                features=features,
            ),
        )
        return self._bind_operation(operation)

    def agent(
        self,
        name: str | None = None,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        agent_id: str | None = None,
        description: str | None = None,
        version: str | None = None,
        model: str | None = None,
        provider: str | None = None,
        conversation_id: str | None = None,
        conversation_compacted: bool | None = None,
        remote: bool = False,
        features: Features | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Operation:
        """Build an `invoke_agent` operation backed by this configured SDK."""
        resolved_parent = _operation_parent(parent, trace_id, parent_span_id)
        operation = Operation(
            name=c.OPERATION_NAME_INVOKE_AGENT,
            context=context,
            parent=resolved_parent,
            kind=SpanKind.CLIENT if remote else SpanKind.INTERNAL,
            provider_name=provider,
            request_model=model,
            conversation_id=_resolve_conversation_id(conversation_id, resolved_parent),
            conversation_compacted=_resolve_conversation_compacted(conversation_compacted, resolved_parent),
            agent_id=agent_id,
            agent_name=name,
            agent_description=description,
            agent_version=version,
            duration_metric="client_operation" if remote else "invoke_agent",
            attributes=_operation_attributes(
                attributes,
                features=features,
            ),
        )
        return self._bind_operation(operation)

    def tool(
        self,
        name: str,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        call_id: str | None = None,
        description: str | None = None,
        tool_type: str | None = None,
        arguments: EventAttributeValue | None = None,
        result: EventAttributeValue | None = None,
        agent_name: str | None = None,
        conversation_id: str | None = None,
        conversation_compacted: bool | None = None,
        features: Features | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Operation:
        """Build an `execute_tool` operation backed by this configured SDK."""
        resolved_parent = _operation_parent(parent, trace_id, parent_span_id)
        operation = Operation(
            name=c.OPERATION_NAME_EXECUTE_TOOL,
            context=context,
            parent=resolved_parent,
            kind=SpanKind.INTERNAL,
            agent_name=agent_name,
            conversation_id=_resolve_conversation_id(conversation_id, resolved_parent),
            conversation_compacted=_resolve_conversation_compacted(conversation_compacted, resolved_parent),
            tool_name=name,
            tool_call_id=call_id,
            tool_description=description,
            tool_type=tool_type,
            tool_call_arguments=arguments,
            tool_call_result=result,
            duration_metric="execute_tool",
            attributes=_operation_attributes(
                attributes,
                features=features,
            ),
        )
        return self._bind_operation(operation)

    def plan(
        self,
        agent_name: str | None = None,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        conversation_id: str | None = None,
        conversation_compacted: bool | None = None,
        features: Features | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Operation:
        """Build a `plan` operation backed by this configured SDK."""
        resolved_parent = _operation_parent(parent, trace_id, parent_span_id)
        operation = Operation(
            name=c.OPERATION_NAME_PLAN,
            context=context,
            parent=resolved_parent,
            kind=SpanKind.INTERNAL,
            agent_name=agent_name,
            conversation_id=_resolve_conversation_id(conversation_id, resolved_parent),
            conversation_compacted=_resolve_conversation_compacted(conversation_compacted, resolved_parent),
            duration_metric="none",
            attributes=_operation_attributes(
                attributes,
                features=features,
            ),
        )
        return self._bind_operation(operation)

    @contextmanager
    def span(
        self,
        name: str,
        *,
        context: Context | None = None,
        parent: Operation | None = None,
        trace_id: str | int | None = None,
        parent_span_id: str | int | None = None,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Generator[Span]:
        """Start a non-GenAI span exported by this SDK's tracer provider.

        This is the low-level escape hatch for intermediate work that should be
        visible in traces without pretending to be a GenAI operation. When no
        explicit parent or context is supplied, OpenTelemetry's current context
        is used, so spans created inside an active operation become children of
        that operation.
        """
        resolved_parent = _operation_parent(parent, trace_id, parent_span_id)
        span_context = _span_parent_context(context, resolved_parent)
        transform_context = (parent.name, self.operation_data_transformers) if parent is not None else None
        resolved_name = name
        resolved_attributes = dict(attributes or {})
        if transform_context is not None:
            operation_name, transformers = transform_context
            transformed_name = transformers.transform(
                name,
                operation_name=operation_name,
                signal="span",
                field="span.name",
            )
            resolved_name = transformed_name if isinstance(transformed_name, str) else c.FALLBACK_CHILD_SPAN_NAME
            resolved_attributes = normalize_otel_attributes(
                transformers.transform_attributes(
                    resolved_attributes,
                    operation_name=operation_name,
                    signal="span",
                )
            )
        with self.tracer.start_as_current_span(
            resolved_name,
            context=span_context,
            kind=kind,
            attributes=resolved_attributes,
            record_exception=False,
            set_status_on_exception=False,
        ) as span:
            try:
                yield span
            except Exception as exc:
                if transform_context is None:
                    self.record_span_exception(span, exc)
                else:
                    operation_name, transformers = transform_context
                    self._record_transformed_exception(
                        span,
                        exc,
                        operation_name=operation_name,
                        transformers=transformers,
                    )
                raise

    def record_span_exception(self, span: Span, exc: BaseException) -> None:
        """Record exception status and attributes on a span."""
        span.record_exception(exc)
        span.set_status(Status(StatusCode.ERROR, str(exc)))
        span.set_attribute(c.ATTR_ERROR_TYPE, type(exc).__name__)

    def record_operation_exception(self, span: Span, exc: BaseException, *, operation_name: str) -> None:
        """Record a transformed exception on an operation span."""
        self._record_transformed_exception(
            span,
            exc,
            operation_name=operation_name,
            transformers=self.operation_data_transformers,
        )

    def _record_transformed_exception(
        self,
        span: Span,
        exc: BaseException,
        *,
        operation_name: str,
        transformers: OperationDataTransformers,
    ) -> None:
        exception_attributes = transformers.transform_attributes(
            {
                c.ATTR_EXCEPTION_TYPE: type(exc).__name__,
                c.ATTR_EXCEPTION_MESSAGE: str(exc),
                c.ATTR_EXCEPTION_STACKTRACE: "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
            },
            operation_name=operation_name,
            signal="span",
        )
        span.add_event("exception", attributes=normalize_otel_attributes(exception_attributes))
        description = transformers.transform(
            str(exc),
            operation_name=operation_name,
            signal="span",
            field="status.description",
        )
        span.set_status(Status(StatusCode.ERROR, description if isinstance(description, str) else None))
        span.set_attribute(c.ATTR_ERROR_TYPE, type(exc).__name__)

    def _transform_log_attributes(
        self,
        operation: Operation,
        attributes: ExtendedAttributes,
    ) -> dict[str, EventAttributeValue]:
        return self.operation_data_transformers.transform_attributes(
            attributes,
            operation_name=operation.name,
            signal="log",
        )

    def _transform_metric_attributes(
        self,
        operation: Operation,
        attributes: Mapping[str, AttributeValue],
    ) -> dict[str, AttributeValue]:
        return normalize_otel_attributes(
            self.operation_data_transformers.transform_attributes(
                attributes,
                operation_name=operation.name,
                signal="metric",
            )
        )

    def record_inference_details(
        self,
        details: InferenceDetails,
        context: Context | None = None,
        *,
        operation: Operation | None = None,
    ) -> None:
        """Emit a GenAI inference-details event log from a dataclass payload."""
        attributes = inference_attributes(details)
        if operation is not None:
            attributes = self._transform_log_attributes(operation, attributes)
        self._emit_event_log(
            c.EVENT_INFERENCE_DETAILS,
            body=None,
            attributes=attributes,
            context=context,
        )

    def record_evaluation_result(
        self,
        result: EvaluationResult,
        context: Context | None = None,
        *,
        operation: Operation | None = None,
    ) -> None:
        """Emit a GenAI evaluation-result event log from a dataclass payload."""
        attributes = evaluation_attributes(result)
        if operation is not None:
            attributes = self._transform_log_attributes(operation, attributes)
        self._emit_event_log(
            c.EVENT_EVALUATION_RESULT,
            body=None,
            attributes=attributes,
            context=context,
        )

    def record_completion(
        self,
        operation: Operation,
        completion: ChatCompletionAdapter,
        *,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> None:
        """Record completion metadata from a normalized adapter payload."""
        response_model = (
            completion.response_model if completion.response_model is not None else operation.response_model
        )
        response_id = completion.response_id if completion.response_id is not None else operation.response_id
        finish_reasons = (
            completion.finish_reasons if completion.finish_reasons is not None else operation.finish_reasons
        )
        input_tokens = completion.input_tokens
        output_tokens = completion.output_tokens

        operation.response_model = response_model
        operation.response_id = response_id
        if input_tokens is not None:
            operation.input_tokens = input_tokens
        if output_tokens is not None:
            operation.output_tokens = output_tokens
        operation.finish_reasons = finish_reasons
        operation._set_transformed_attributes(  # pyright: ignore[reportPrivateUsage]
            completion_span_attributes(
                operation,
                completion,
                attributes=attributes,
                transformers=self.operation_data_transformers,
            ),
            already_transformed=frozenset(
                {
                    c.ATTR_GEN_AI_INPUT_MESSAGES,
                    c.ATTR_GEN_AI_OUTPUT_MESSAGES,
                }
                - (attributes or {}).keys()
            ),
        )
        self.record_token_usage(
            TokenUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                operation_name=operation.name,
                provider_name=operation.provider_name,
                request_model=operation.request_model,
                response_model=response_model,
            ),
            context=operation.otel_context,
            operation=operation,
        )

    def record_token_usage(
        self,
        usage: TokenUsage,
        context: Context | None = None,
        *,
        operation: Operation | None = None,
    ) -> None:
        """Record token usage metrics from a dataclass payload."""
        records = (
            (c.TOKEN_TYPE_INPUT, usage.input_tokens),
            (c.TOKEN_TYPE_OUTPUT, usage.output_tokens),
        )
        for token_type, value in records:
            if value is None:
                continue
            attributes = token_usage_metric_attributes(usage, token_type)
            if operation is not None:
                attributes = self._transform_metric_attributes(operation, attributes)
            self._token_usage.record(value, attributes, context=context)

    def record_operation_duration(
        self,
        duration: OperationDuration,
        context: Context | None = None,
        *,
        operation: Operation | None = None,
    ) -> None:
        """Record the duration metric selected by the payload."""
        attributes = operation_duration_metric_attributes(duration)
        if operation is not None:
            attributes = self._transform_metric_attributes(operation, attributes)
        if duration.duration_metric == "client_operation":
            self._operation_duration.record(duration.duration_s, attributes, context=context)
        elif duration.duration_metric == "invoke_agent":
            self._invoke_agent_duration.record(duration.duration_s, attributes, context=context)
        elif duration.duration_metric == "execute_tool":
            self._execute_tool_duration.record(duration.duration_s, attributes, context=context)
        else:
            return

    def start_streaming_timer(
        self,
        chunk: StreamingChunk | None = None,
        *,
        context: Context | None = None,
        clock: Clock | None = None,
        operation: Operation | None = None,
    ) -> "StreamingTimer":
        """Create a timer that records first-chunk and per-chunk metrics."""
        return StreamingTimer(
            observability=self,
            default_chunk=chunk or StreamingChunk(),
            context=context,
            clock=clock or time.perf_counter,
            operation=operation,
        )

    def flush(self, timeout_millis: int = 30_000) -> bool:
        """Force-flush owned span, metric, and log providers."""
        trace_flushed = self.tracer_provider.force_flush(timeout_millis=timeout_millis)
        metric_flushed = self.meter_provider.force_flush(timeout_millis=timeout_millis)
        log_flushed = self.logger_provider.force_flush(timeout_millis=timeout_millis)
        return bool(trace_flushed and metric_flushed and log_flushed)

    def shutdown(self, timeout_millis: int = 30_000) -> None:
        """Flush and shut down all owned OpenTelemetry providers once."""
        if self._shutdown:
            return
        self._shutdown = True
        self.flush(timeout_millis=timeout_millis)
        self.tracer_provider.shutdown()
        self.meter_provider.shutdown()
        self.logger_provider.shutdown()

    def record_streaming_chunk(
        self,
        elapsed_s: float,
        *,
        is_first_chunk: bool,
        chunk: StreamingChunk,
        context: Context | None,
        operation: Operation | None = None,
    ) -> None:
        """Record one streaming chunk timing datapoint."""
        histogram = self._time_to_first_chunk if is_first_chunk else self._time_per_output_chunk
        attributes = streaming_chunk_metric_attributes(chunk)
        if operation is not None:
            attributes = self._transform_metric_attributes(operation, attributes)
        histogram.record(elapsed_s, attributes, context=context)

    def record_log(
        self,
        body: EventAttributeValue,
        *,
        context: Context | None = None,
        attributes: ExtendedAttributes | None = None,
        operation: Operation | None = None,
    ) -> None:
        """Emit a plain log record through the owned logger provider."""
        resolved_body = body
        resolved_attributes = _extended_attributes(attributes)
        if operation is not None:
            resolved_body = self.operation_data_transformers.transform(
                body,
                operation_name=operation.name,
                signal="log",
                field="body",
            )
            resolved_attributes = self._transform_log_attributes(operation, resolved_attributes)
        self._emit_log(
            resolved_body,
            attributes=resolved_attributes,
            context=context,
        )

    def record_event(
        self,
        event_name: str,
        body: EventAttributeValue | None = None,
        *,
        context: Context | None = None,
        attributes: ExtendedAttributes | None = None,
        operation: Operation | None = None,
    ) -> None:
        """Emit a named log event through the owned logger provider."""
        resolved_event_name = event_name
        resolved_body = body
        resolved_attributes = _extended_attributes(attributes)
        if operation is not None:
            transformed_event_name = self.operation_data_transformers.transform(
                event_name,
                operation_name=operation.name,
                signal="log",
                field="event.name",
            )
            resolved_event_name = (
                transformed_event_name if isinstance(transformed_event_name, str) else c.FALLBACK_OPERATION_EVENT_NAME
            )
            resolved_body = self.operation_data_transformers.transform(
                body,
                operation_name=operation.name,
                signal="log",
                field="body",
            )
            resolved_attributes = self._transform_log_attributes(operation, resolved_attributes)
        self._emit_event_log(
            resolved_event_name,
            body=resolved_body,
            attributes=resolved_attributes,
            context=context,
        )

    def _emit_log(
        self,
        body: EventAttributeValue | None,
        *,
        attributes: ExtendedAttributes,
        context: Context | None,
    ) -> None:
        self.logger.emit(
            context=context or context_api.get_current(),
            body=body,
            attributes=dict(attributes),
        )

    def _emit_event_log(
        self,
        event_name: str,
        *,
        body: EventAttributeValue | None = None,
        attributes: ExtendedAttributes,
        context: Context | None,
    ) -> None:
        self.logger.emit(
            context=context or context_api.get_current(),
            body=event_name if body is None else body,
            event_name=event_name,
            attributes=dict(attributes),
        )

    def _build_span_exporter(self) -> SpanExporter:
        if self.config.protocol == "grpc":
            try:
                from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (  # pyright: ignore[reportMissingImports]
                    OTLPSpanExporter as GrpcOTLPSpanExporter,  # pyright: ignore[reportUnknownVariableType]
                )
            except ModuleNotFoundError as exc:
                message = "gRPC OTLP export requires installing mistralai-otel-observability[grpc]"
                raise RuntimeError(message) from exc

            return GrpcOTLPSpanExporter(  # pyright: ignore[reportUnknownVariableType]
                endpoint=self.config.endpoint,
                headers=dict(self.config.headers) if self.config.headers is not None else None,
                timeout=self.config.timeout,
                insecure=self.config.insecure,
            )
        else:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as HttpOTLPSpanExporter

            return HttpOTLPSpanExporter(
                endpoint=_http_signal_endpoint(self.config.endpoint, "traces"),
                headers=dict(self.config.headers) if self.config.headers is not None else None,
                timeout=self.config.timeout,
            )

    def _build_metric_exporter(self) -> MetricExporter:
        if self.config.protocol == "grpc":
            try:
                from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (  # pyright: ignore[reportMissingImports]
                    OTLPMetricExporter as GrpcOTLPMetricExporter,  # pyright: ignore[reportUnknownVariableType]
                )
            except ModuleNotFoundError as exc:
                message = "gRPC OTLP export requires installing mistralai-otel-observability[grpc]"
                raise RuntimeError(message) from exc

            return GrpcOTLPMetricExporter(  # pyright: ignore[reportUnknownVariableType]
                endpoint=self.config.endpoint,
                headers=dict(self.config.headers) if self.config.headers is not None else None,
                timeout=self.config.timeout,
                insecure=self.config.insecure,
            )
        else:
            from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
                OTLPMetricExporter as HttpOTLPMetricExporter,
            )

            return HttpOTLPMetricExporter(
                endpoint=_http_signal_endpoint(self.config.endpoint, "metrics"),
                headers=dict(self.config.headers) if self.config.headers is not None else None,
                timeout=self.config.timeout,
            )

    def _build_log_exporter(self) -> LogRecordExporter:
        if self.config.protocol == "grpc":
            try:
                from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (  # pyright: ignore[reportMissingImports]
                    OTLPLogExporter as GrpcOTLPLogExporter,  # pyright: ignore[reportUnknownVariableType]
                )
            except ModuleNotFoundError as exc:
                message = "gRPC OTLP export requires installing mistralai-otel-observability[grpc]"
                raise RuntimeError(message) from exc

            return GrpcOTLPLogExporter(  # pyright: ignore[reportUnknownVariableType]
                endpoint=self.config.endpoint,
                headers=dict(self.config.headers) if self.config.headers is not None else None,
                timeout=self.config.timeout,
                insecure=self.config.insecure,
            )
        else:
            from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter as HttpOTLPLogExporter

            return HttpOTLPLogExporter(
                endpoint=_http_signal_endpoint(self.config.endpoint, "logs"),
                headers=dict(self.config.headers) if self.config.headers is not None else None,
                timeout=self.config.timeout,
            )

    @staticmethod
    def _build_resource(config: ObservabilityConfig) -> Resource:
        attributes: dict[str, AttributeValue] = {"service.name": config.service_name}
        if config.service_version is not None:
            attributes["service.version"] = config.service_version
        attributes.update(config.resource_attributes)
        return Resource.create(attributes)

    @staticmethod
    def _build_metric_views(config: ObservabilityConfig) -> list[View]:
        duration_aggregation = ExplicitBucketHistogramAggregation(config.metric_histogram_boundaries)
        token_aggregation = ExplicitBucketHistogramAggregation((1, 4, 16, 64, 256, 1_024, 4_096, 16_384, 65_536))
        return [
            View(instrument_name=c.METRIC_GEN_AI_CLIENT_OPERATION_DURATION, aggregation=duration_aggregation),
            View(
                instrument_name=c.METRIC_GEN_AI_CLIENT_OPERATION_TIME_TO_FIRST_CHUNK,
                aggregation=duration_aggregation,
            ),
            View(
                instrument_name=c.METRIC_GEN_AI_CLIENT_OPERATION_TIME_PER_OUTPUT_CHUNK,
                aggregation=duration_aggregation,
            ),
            View(instrument_name=c.METRIC_GEN_AI_INVOKE_AGENT_DURATION, aggregation=duration_aggregation),
            View(instrument_name=c.METRIC_GEN_AI_EXECUTE_TOOL_DURATION, aggregation=duration_aggregation),
            View(instrument_name=c.METRIC_GEN_AI_CLIENT_TOKEN_USAGE, aggregation=token_aggregation),
        ]


class StreamingTimer:
    """Helper that turns streaming chunk arrivals into duration metrics."""

    def __init__(
        self,
        *,
        observability: ObservabilitySDK,
        default_chunk: StreamingChunk,
        context: Context | None,
        clock: Clock,
        operation: Operation | None,
    ) -> None:
        """Create a timer bound to a configured SDK and default chunk attrs."""
        self._observability = observability
        self._default_chunk = default_chunk
        self._context = context
        self._clock = clock
        self._operation = operation
        self._started_at = clock()
        self._last_chunk_at: float | None = None

    def record_chunk(self, chunk: StreamingChunk | None = None) -> float:
        """Record the next chunk interval and return the measured seconds."""
        now = self._clock()
        if self._last_chunk_at is None:
            elapsed_s = now - self._started_at
            is_first_chunk = True
        else:
            elapsed_s = now - self._last_chunk_at
            is_first_chunk = False

        self._last_chunk_at = now
        self._observability.record_streaming_chunk(
            elapsed_s,
            is_first_chunk=is_first_chunk,
            chunk=chunk or self._default_chunk,
            context=self._context,
            operation=self._operation,
        )
        return elapsed_s


def _http_signal_endpoint(endpoint: str | None, signal: str) -> str | None:
    if endpoint is None:
        return None

    parts = urlsplit(endpoint)
    path = parts.path.rstrip("/")
    path = f"{path}/v1/{signal}"
    return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))


@contextmanager
def _conversation_scope(
    conversation_id: str,
    *,
    compacted: bool | None,
) -> Generator[None]:
    token = _conversation_context.set((conversation_id, compacted))
    try:
        yield
    finally:
        _conversation_context.reset(token)


def _resolve_conversation_id(
    conversation_id: str | None,
    parent: Operation | None,
) -> str | None:
    if conversation_id is not None:
        return conversation_id
    elif parent is not None and parent.conversation_id is not None:
        return parent.conversation_id
    else:
        current = _conversation_context.get()
        if current is None:
            return None
        return current[0]


def _resolve_conversation_compacted(
    conversation_compacted: bool | None,
    parent: Operation | None,
) -> bool | None:
    if conversation_compacted is not None:
        return conversation_compacted
    elif parent is not None and parent.conversation_compacted is not None:
        return parent.conversation_compacted
    else:
        current = _conversation_context.get()
        if current is None:
            return None
        return current[1]


def _operation_parent(
    parent: Operation | None,
    trace_id: str | int | None,
    parent_span_id: str | int | None,
) -> Operation | None:
    if parent is not None and (trace_id is not None or parent_span_id is not None):
        message = "parent cannot be combined with trace_id or parent_span_id"
        raise ValueError(message)
    elif trace_id is None and parent_span_id is None:
        return parent
    elif trace_id is None or parent_span_id is None:
        message = "trace_id and parent_span_id must be provided together"
        raise ValueError(message)
    else:
        return Operation(name="parent", trace_id=trace_id, span_id=parent_span_id)


def _span_parent_context(context: Context | None, parent: Operation | None) -> Context | None:
    if context is not None and parent is not None:
        message = "context cannot be combined with parent, trace_id, or parent_span_id"
        raise ValueError(message)
    elif parent is not None:
        return parent.otel_context
    else:
        return context


def _otel_attributes(attributes: Mapping[str, AttributeValue] | None) -> Mapping[str, AttributeValue]:
    if attributes is None:
        return {}
    return attributes


def _operation_attributes(
    attributes: Mapping[str, AttributeValue] | None,
    *,
    features: Features | None,
) -> Mapping[str, AttributeValue]:
    resolved_attributes: dict[str, AttributeValue] = dict(feature_attributes(features))
    resolved_attributes.update(_otel_attributes(attributes))
    return resolved_attributes


def _extended_attributes(attributes: ExtendedAttributes | None) -> ExtendedAttributes:
    if attributes is None:
        return {}
    return attributes


def _mistral_headers(api_key: str | None) -> dict[str, str]:
    resolved_api_key = api_key or os.getenv(MISTRAL_API_KEY_ENV)
    if not resolved_api_key:
        message = f"{MISTRAL_API_KEY_ENV} must be set unless api_key is provided"
        raise ValueError(message)

    return {"Authorization": f"Bearer {resolved_api_key}"}
