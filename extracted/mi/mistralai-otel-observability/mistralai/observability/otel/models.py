"""Data models and semantic-convention mapping for GenAI telemetry."""

from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from contextvars import Token
from dataclasses import dataclass, field
from types import TracebackType
from typing import TYPE_CHECKING, Literal, Protocol, Self

from opentelemetry import context as context_api
from opentelemetry.context import Context
from opentelemetry.trace import (
    Link,
    NonRecordingSpan,
    Span,
    SpanContext,
    SpanKind,
    Status,
    StatusCode,
    TraceFlags,
    TraceState,
    set_span_in_context,
)
from opentelemetry.util.types import AttributeValue

from . import semconv_constants as c
from ._ids import parse_otel_id
from .attributes import normalize_otel_attribute, normalize_otel_attributes
from .hooks import OperationDataTransformers, OperationDataValue

if TYPE_CHECKING:
    from opentelemetry.sdk.trace.sampling import Sampler

    from .sdk import Clock, ObservabilitySDK, StreamingTimer

ATTR_MISTRAL_OBS_FEATURES_DETECTOR = "mistral.obs.features.detector"
ATTR_MISTRAL_OBS_FEATURES_JUDGE = "mistral.obs.features.judge"
ATTR_MISTRAL_OBS_FEATURES_MODERATION = "mistral.obs.features.moderation"

Attributes = Mapping[str, AttributeValue]
type EventAttributeValue = OperationDataValue
ExtendedAttributes = Mapping[str, EventAttributeValue]
GenAiMessage = Mapping[str, EventAttributeValue]
OtlpProtocol = Literal["http/protobuf", "grpc"]
OperationDurationMetric = Literal["client_operation", "invoke_agent", "execute_tool", "none"]

_STRUCTURED_OPERATION_SPAN_FIELDS = frozenset(
    {
        c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS,
        c.ATTR_GEN_AI_TOOL_DEFINITIONS,
        c.ATTR_GEN_AI_TOOL_CALL_ARGUMENTS,
        c.ATTR_GEN_AI_TOOL_CALL_RESULT,
    }
)

DEFAULT_METRIC_HISTOGRAM_BOUNDARIES = (
    0.001,
    0.005,
    0.01,
    0.025,
    0.05,
    0.1,
    0.25,
    0.5,
    1.0,
    2.5,
    5.0,
    10.0,
    30.0,
    60.0,
)


class CommonGenAiAttributes(Protocol):
    """Shared attributes used by spans, logs, and metrics."""

    @property
    def provider_name(self) -> str | None:
        """GenAI provider name, such as `mistral_ai`, when known."""
        ...

    @property
    def request_model(self) -> str | None:
        """Model requested by the caller, when the operation has one."""
        ...

    @property
    def response_model(self) -> str | None:
        """Model reported by the provider response, when available."""
        ...


class ChatCompletionAdapter(Protocol):
    """Completion payload interface consumed by `record_completion`.

    Implementations expose completion response fields in the SDK's generic
    GenAI shape so the operation can enrich spans and token metrics without
    importing every provider SDK in the core package.
    """

    @property
    def response_model(self) -> str | None:
        """Model reported by the chat-completion response."""
        ...

    @property
    def response_id(self) -> str | None:
        """Provider response identifier."""
        ...

    @property
    def input_messages(self) -> Sequence[GenAiMessage] | None:
        """Request messages converted to GenAI message format, if provided."""
        ...

    @property
    def output_messages(self) -> Sequence[GenAiMessage] | None:
        """Response messages converted to GenAI message format, if provided."""
        ...

    @property
    def finish_reasons(self) -> Sequence[str] | None:
        """Provider finish reasons for returned choices."""
        ...

    @property
    def input_tokens(self) -> int | None:
        """Prompt or input token count reported by the provider."""
        ...

    @property
    def output_tokens(self) -> int | None:
        """Completion or output token count reported by the provider."""
        ...


def _empty_attributes() -> dict[str, AttributeValue]:
    return {}


def _empty_extended_attributes() -> dict[str, EventAttributeValue]:
    return {}


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatCompletionDetails:
    """Generic completion details consumed by `record_completion`."""

    response_model: str | None = None
    response_id: str | None = None
    input_messages: Sequence[GenAiMessage] | None = None
    output_messages: Sequence[GenAiMessage] | None = None
    finish_reasons: Sequence[str] | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Features:
    """Mistral observability features requested for an operation or log.

    `sensitive_data` intentionally maps to the existing detector telemetry
    attribute because the downstream feature is still implemented by the
    detector pipeline. The Python name describes the product-level capability
    callers enable, while the emitted OTLP key stays stable.
    """

    sensitive_data: bool | None = None
    moderation: bool | None = None
    # NOTE(OBS-2326): `judges` carries scorer slugs. The worker resolves each slug
    # first-match (workspace, then shared), so two pipeline configs sharing a slug
    # with different mappings can't be disambiguated from here (unlike the selector
    # and live paths, which now resolve by snapshot id). Pinning the mapping would
    # need either a pipeline_config_id (but emit-time callers usually don't know
    # pipelines) or an inline mapping per slug (but a scorer not referenced by any
    # enabled pipeline isn't in the worker snapshot and won't resolve). Open contract
    # question; effectively unused today, so revisit before relying on it (OBS-2338).
    judges: Sequence[str] | None = None


@dataclass(frozen=True, kw_only=True)
class ObservabilityConfig:
    """Configuration for isolated OpenTelemetry providers and exporters."""

    service_name: str = "mistralai-otel-observability"
    service_version: str | None = None
    endpoint: str | None = None
    protocol: OtlpProtocol = "http/protobuf"
    headers: Mapping[str, str] | None = None
    timeout: float | None = None
    export_interval_millis: int = 5_000
    insecure: bool | None = None
    resource_attributes: Attributes = field(default_factory=_empty_attributes)
    metric_histogram_boundaries: Sequence[float] = DEFAULT_METRIC_HISTOGRAM_BOUNDARIES
    sampler: "Sampler | None" = None


@dataclass(kw_only=True)
class Operation:
    """User-facing GenAI operation that owns or references a span.

    An operation can be started as a real span, used as a context manager, or
    created with stored trace/span identifiers for delayed logs and evaluations.
    The fields mirror GenAI semantic-convention attributes; high-level helpers
    fill the common subset while advanced callers can set the full shape.
    """

    name: str
    parent: "Operation | None" = None
    context: Context | None = None
    trace_id: str | int | None = None
    span_id: str | int | None = None
    span_name: str | None = None
    kind: SpanKind = SpanKind.CLIENT
    provider_name: str | None = None
    request_model: str | None = None
    request_max_tokens: int | None = None
    request_choice_count: int | None = None
    request_temperature: float | None = None
    request_top_p: float | None = None
    request_top_k: int | None = None
    request_stop_sequences: Sequence[str] | None = None
    request_frequency_penalty: float | None = None
    request_presence_penalty: float | None = None
    request_seed: int | None = None
    request_stream: bool | None = None
    request_reasoning_level: str | None = None
    response_model: str | None = None
    response_id: str | None = None
    response_time_to_first_chunk: float | None = None
    input_tokens: int | None = None
    cache_read_input_tokens: int | None = None
    cache_creation_input_tokens: int | None = None
    output_tokens: int | None = None
    reasoning_output_tokens: int | None = None
    finish_reasons: Sequence[str] | None = None
    output_type: str | None = None
    conversation_id: str | None = None
    conversation_compacted: bool | None = None
    prompt_name: str | None = None
    prompt_version: str | None = None
    prompt_variables: Mapping[str, str] | None = None
    agent_id: str | None = None
    agent_name: str | None = None
    agent_description: str | None = None
    agent_version: str | None = None
    tool_name: str | None = None
    tool_call_id: str | None = None
    tool_description: str | None = None
    tool_type: str | None = None
    tool_call_arguments: EventAttributeValue | None = None
    tool_call_result: EventAttributeValue | None = None
    system_instructions: EventAttributeValue | None = None
    tool_definitions: EventAttributeValue | None = None
    server_address: str | None = None
    server_port: int | None = None
    duration_metric: OperationDurationMetric = "client_operation"
    include_content: bool = False
    attributes: Attributes = field(default_factory=_empty_attributes)
    _observability: "ObservabilitySDK | None" = field(default=None, init=False, repr=False, compare=False)
    _span: Span | None = field(default=None, init=False, repr=False, compare=False)
    _span_context: Context | None = field(default=None, init=False, repr=False, compare=False)
    _context_token: Token[Context] | None = field(default=None, init=False, repr=False, compare=False)
    _started_at: float | None = field(default=None, init=False, repr=False, compare=False)
    _start_time_unix_nano: int | None = field(default=None, init=False, repr=False, compare=False)
    _duration_recorded: bool = field(default=False, init=False, repr=False, compare=False)

    def _sdk(self) -> "ObservabilitySDK":
        """Return the SDK that created this operation, or the configured facade SDK."""
        return self._observability or _sdk()

    def _active_span(self) -> Span:
        """Return the active span or fail if the operation was not started."""
        if self._span is None:
            message = "operation has not been started"
            raise RuntimeError(message)
        return self._span

    @contextmanager
    def span(
        self,
        name: str,
        *,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> Generator[Span]:
        """Start a non-GenAI child span scoped to this operation."""
        with self._sdk().span(
            name,
            parent=self,
            kind=kind,
            attributes=attributes,
        ) as span:
            yield span

    @property
    def otel_context(self) -> Context:
        """Return an OTel context for active spans or stored span references."""
        if self._span_context is not None:
            return self._span_context
        elif self.trace_id is not None and self.span_id is not None:
            return _span_context(trace_id=self.trace_id, span_id=self.span_id)
        else:
            message = "operation has no active span or trace_id/span_id"
            raise RuntimeError(message)

    @property
    def is_started(self) -> bool:
        """Report whether this operation currently has an active span."""
        return self._span is not None

    @property
    def started_at(self) -> float:
        """Return the monotonic start timestamp used for duration metrics."""
        if self._started_at is None:
            message = "operation has not been started"
            raise RuntimeError(message)
        return self._started_at

    @property
    def duration_recorded(self) -> bool:
        """Report whether this operation already emitted its duration metric."""
        return self._duration_recorded

    def start(
        self,
        *,
        context: Context | None = None,
        parent: "Operation | None" = None,
        set_current_context: bool = True,
        span_id: str | int | None = None,
        start_time_unix_nano: int | None = None,
        trace_id: str | int | None = None,
        links: Sequence[Link] | None = None,
    ) -> Self:
        """Start the span represented by this operation.

        Starting attaches the span to the current OpenTelemetry context so logs,
        metrics, and child operations recorded inside the block inherit the same
        trace/span context. Operations created only with trace/span ids can skip
        `start()` and still emit correlated logs.

        Set `set_current_context=False` when `start()` and `end()` run in
        different execution contexts (for example separate asyncio tasks), where
        attaching here would leave a context token that cannot be detached in the
        other task. Parenting still works through explicit `parent`/`context`.

        `span_id` and `start_time_unix_nano` let a host that reconstructs an
        operation from durable records emit it with a stable identity and its
        original timing, so repeated emission exports the same span id.
        `trace_id` pins the trace of a root operation, and `links` records span
        links, for example to the application span that caused an isolated trace.
        """
        if self._span is not None:
            message = "operation has already been started"
            raise RuntimeError(message)

        sdk = self._sdk()
        operation_context = _operation_context(
            context if context is not None else self.context,
            parent if parent is not None else self.parent,
        )
        span_name = sdk.operation_data_transformers.transform(
            operation_span_name(self),
            operation_name=self.name,
            signal="span",
            field="span.name",
        )
        if not isinstance(span_name, str):
            span_name = c.FALLBACK_OPERATION_SPAN_NAME
        span = sdk.start_operation_span(
            span_name,
            context=operation_context,
            kind=self.kind,
            attributes=operation_attributes(self, transformers=sdk.operation_data_transformers),
            span_id=span_id,
            start_time_unix_nano=start_time_unix_nano,
            trace_id=trace_id,
            links=links,
        )
        span_context = span.get_span_context()
        self.trace_id = f"{span_context.trace_id:032x}"
        self.span_id = f"{span_context.span_id:016x}"
        self._span = span
        self._span_context = set_span_in_context(span)
        if set_current_context:
            self._context_token = context_api.attach(self._span_context)
        self._started_at = sdk.clock()
        self._start_time_unix_nano = start_time_unix_nano
        self._duration_recorded = False
        return self

    def end(
        self,
        *,
        error_type: str | None = None,
        error_message: str | None = None,
        end_time_unix_nano: int | None = None,
    ) -> None:
        """End the active span and record its matching duration metric.

        When `error_type` is given, the span is marked `ERROR` with an
        `error.type` attribute and the duration metric is labelled with the same
        value, so a failed operation is recorded consistently on both the span
        and the metric. Use this for terminal failures that are not raised
        exceptions, such as a provider error or an outcome carried in a payload;
        exceptions raised inside the context manager are recorded separately.

        `error_message` requires `error_type` and sets the span status description
        after the configured operation-data transformations. A dropped or
        non-string transformed value leaves the description unset. The message
        is never added to metrics, and returned failures do not create exception
        events.

        The metric emitted depends on the operation kind: normal client
        operations use `gen_ai.client.operation.duration`, in-process agents use
        `gen_ai.invoke_agent.duration`, tools use `gen_ai.execute_tool.duration`,
        and plan spans intentionally skip a duration metric.

        `end_time_unix_nano` closes the span at a recorded time, and the
        duration metric uses the difference between both recorded timestamps
        instead of the local clock. It is required when the span was started at
        a recorded time, and rejected otherwise.
        """
        if self._span is None:
            return

        if error_message is not None and error_type is None:
            message = "error_message requires error_type"
            raise ValueError(message)
        if (end_time_unix_nano is None) != (self._start_time_unix_nano is None):
            message = "start_time_unix_nano and end_time_unix_nano must be given together"
            raise ValueError(message)
        _check_end_time(self._start_time_unix_nano, end_time_unix_nano)
        if error_type is not None:
            description = None
            if error_message is not None:
                transformed = self._sdk().operation_data_transformers.transform(
                    error_message,
                    operation_name=self.name,
                    signal="span",
                    field="status.description",
                )
                if isinstance(transformed, str):
                    description = transformed
            self._span.set_status(Status(StatusCode.ERROR, description))
            self.set_attribute(c.ATTR_ERROR_TYPE, error_type)
        self._finish(error_type=error_type, end_time_unix_nano=end_time_unix_nano)

    def _finish(self, *, error_type: str | None, end_time_unix_nano: int | None = None) -> None:
        """Record the duration metric, detach the context, and end the span.

        The span status is left untouched so a richer status already set by the
        caller (such as the redacted description from a recorded exception) is
        preserved; `error_type` only labels the duration metric here.
        """
        if self._span is None:
            return

        duration_s = None
        if end_time_unix_nano is not None and self._start_time_unix_nano is not None:
            duration_s = (end_time_unix_nano - self._start_time_unix_nano) / 1_000_000_000
        self.operation_duration(duration_s, error_type=error_type)
        if self._context_token is not None:
            context_api.detach(self._context_token)
            self._context_token = None
        self._span.end(end_time=end_time_unix_nano)
        self._span = None

    def __enter__(self) -> Self:
        """Start the operation span when entering a `with` block."""
        return self.start()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Record exceptions and end the operation span on block exit."""
        if exc is not None and self._span is not None:
            self._sdk().record_operation_exception(self._active_span(), exc, operation_name=self.name)
            self._finish(error_type=exc_type.__name__ if exc_type is not None else type(exc).__name__)
        else:
            self.end()

    def set_attribute(self, key: str, value: AttributeValue) -> None:
        """Set one attribute on the active span."""
        self._set_attribute(key, value, already_transformed=False)

    def _set_attribute(self, key: str, value: AttributeValue, *, already_transformed: bool) -> None:
        transformed = value
        if not already_transformed:
            transformed = self._sdk().operation_data_transformers.transform(
                value,
                operation_name=self.name,
                signal="span",
                field=key,
            )
        attribute = normalize_otel_attribute(transformed)
        if attribute is not None:
            self._active_span().set_attribute(key, attribute)

    def set_attributes(self, attributes: Mapping[str, AttributeValue]) -> None:
        """Set multiple attributes on the active span."""
        self._set_transformed_attributes(attributes)

    def _set_transformed_attributes(
        self,
        attributes: Mapping[str, AttributeValue],
        *,
        already_transformed: frozenset[str] = frozenset(),
    ) -> None:
        for key, value in attributes.items():
            self._set_attribute(key, value, already_transformed=key in already_transformed)

    def tool_result(
        self,
        result: EventAttributeValue,
        *,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> None:
        """Record the tool call result on the active span.

        The result is serialized and passed through the data transformers, the
        same structured path tool arguments use at operation start. Use this for
        results that are only known when the tool finishes.
        """
        span_attributes: dict[str, AttributeValue] = {}
        _set_operation_structured_span_attribute(
            span_attributes,
            self,
            c.ATTR_GEN_AI_TOOL_CALL_RESULT,
            result,
            self._sdk().operation_data_transformers,
            overrides=attributes,
        )
        if attributes is not None:
            span_attributes.update(attributes)
        self._set_transformed_attributes(
            span_attributes,
            already_transformed=frozenset({c.ATTR_GEN_AI_TOOL_CALL_RESULT} - (attributes or {}).keys()),
        )

    def log(
        self,
        body: EventAttributeValue,
        *,
        features: Features | None = None,
        attributes: ExtendedAttributes | None = None,
    ) -> None:
        """Emit an operation-scoped log without an OTel event name.

        The log is correlated with this operation's active or stored span
        context. Use this for application breadcrumbs; use `event()` when the
        log needs a stable event name.
        """
        self._sdk().record_log(
            body,
            context=self.otel_context,
            attributes=_operation_log_attributes(
                attributes,
                operation=self,
                features=features,
            ),
            operation=self,
        )

    def event(
        self,
        event_name: str,
        body: EventAttributeValue | None = None,
        *,
        features: Features | None = None,
        attributes: ExtendedAttributes | None = None,
    ) -> None:
        """Emit an operation-scoped named log event.

        This is the log-based replacement for span events. It keeps the
        operation trace/span context while giving downstream processors a stable
        `event_name` to route on.
        """
        self._sdk().record_event(
            event_name,
            body=body,
            context=self.otel_context,
            attributes=_operation_log_attributes(
                attributes,
                operation=self,
                features=features,
            ),
            operation=self,
        )

    def inference_details(
        self,
        *,
        response_model: str | None = None,
        response_id: str | None = None,
        input_messages: Sequence[GenAiMessage] | None = None,
        output_messages: Sequence[GenAiMessage] | None = None,
        prompt: str | None = None,
        completion: str | None = None,
        finish_reasons: Sequence[str] | None = None,
        attributes: ExtendedAttributes | None = None,
    ) -> None:
        """Emit the GenAI inference-detail log for explicitly supplied content.

        This method is not gated by `include_content`: if callers pass messages,
        prompts, or completions here, the SDK sends them. Completion adapters do
        not call this automatically so privacy decisions stay explicit.
        """
        self._sdk().record_inference_details(
            InferenceDetails(
                operation_name=self.name,
                provider_name=self.provider_name,
                request_model=self.request_model,
                request_max_tokens=self.request_max_tokens,
                request_choice_count=self.request_choice_count,
                request_temperature=self.request_temperature,
                request_top_p=self.request_top_p,
                request_top_k=self.request_top_k,
                request_stop_sequences=self.request_stop_sequences,
                request_frequency_penalty=self.request_frequency_penalty,
                request_presence_penalty=self.request_presence_penalty,
                request_seed=self.request_seed,
                request_stream=self.request_stream,
                request_reasoning_level=self.request_reasoning_level,
                response_model=response_model or self.response_model,
                response_id=response_id or self.response_id,
                response_time_to_first_chunk=self.response_time_to_first_chunk,
                input_tokens=self.input_tokens,
                cache_read_input_tokens=self.cache_read_input_tokens,
                cache_creation_input_tokens=self.cache_creation_input_tokens,
                output_tokens=self.output_tokens,
                reasoning_output_tokens=self.reasoning_output_tokens,
                input_messages=input_messages,
                output_messages=output_messages,
                prompt=prompt,
                completion=completion,
                finish_reasons=finish_reasons or self.finish_reasons,
                output_type=self.output_type,
                conversation_id=self.conversation_id,
                conversation_compacted=self.conversation_compacted,
                prompt_name=self.prompt_name,
                prompt_version=self.prompt_version,
                prompt_variables=self.prompt_variables,
                agent_id=self.agent_id,
                agent_name=self.agent_name,
                agent_description=self.agent_description,
                agent_version=self.agent_version,
                system_instructions=self.system_instructions,
                tool_definitions=self.tool_definitions,
                server_address=self.server_address,
                server_port=self.server_port,
                attributes=_extended_attributes(attributes),
            ),
            context=self.otel_context,
            operation=self,
        )

    def evaluation_result(
        self,
        name: str,
        *,
        score_value: float | None = None,
        score_label: str | None = None,
        explanation: str | None = None,
        response_id: str | None = None,
        attributes: ExtendedAttributes | None = None,
    ) -> None:
        """Emit a GenAI evaluation-result log correlated to this operation.

        Evaluations can be recorded while the span is active or later from an
        `Operation` that only carries trace/span identifiers. Include
        `response_id` when the evaluation applies to a specific model response.
        """
        self._sdk().record_evaluation_result(
            EvaluationResult(
                name=name,
                score_value=score_value,
                score_label=score_label,
                explanation=explanation,
                response_id=response_id,
                attributes=_operation_log_attributes(
                    attributes,
                    operation=self,
                    features=None,
                ),
            ),
            context=self.otel_context,
            operation=self,
        )

    def token_usage(
        self,
        *,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        response_model: str | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> None:
        """Record input/output token usage for this operation.

        The SDK emits one histogram datapoint per provided token direction using
        `gen_ai.token.type` to distinguish input from output.
        """
        self._sdk().record_token_usage(
            TokenUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                operation_name=self.name,
                provider_name=self.provider_name,
                request_model=self.request_model,
                response_model=response_model if response_model is not None else self.response_model,
                attributes=_otel_attributes(attributes),
            ),
            context=self.otel_context,
            operation=self,
        )

    def operation_duration(
        self,
        duration_s: float | None = None,
        *,
        response_model: str | None = None,
        server_address: str | None = None,
        server_port: int | None = None,
        error_type: str | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> None:
        """Record this operation's duration metric once.

        `end()` calls this automatically. Manual calls are useful when a caller
        wants to provide an externally measured duration; subsequent calls are
        ignored so the operation does not double-count.
        """
        if self._duration_recorded:
            return

        sdk = self._sdk()
        if duration_s is None:
            duration_s = sdk.clock() - self.started_at
        sdk.record_operation_duration(
            OperationDuration(
                duration_s=duration_s,
                operation_name=self.name,
                provider_name=self.provider_name,
                request_model=self.request_model,
                response_model=response_model if response_model is not None else self.response_model,
                server_address=server_address if server_address is not None else self.server_address,
                server_port=server_port if server_port is not None else self.server_port,
                error_type=error_type,
                duration_metric=self.duration_metric,
                agent_name=self.agent_name,
                tool_name=self.tool_name,
                tool_type=self.tool_type,
                attributes=_otel_attributes(attributes),
            ),
            context=self.otel_context,
            operation=self,
        )
        self._duration_recorded = True

    def start_streaming_timer(
        self,
        *,
        response_model: str | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
        clock: "Clock | None" = None,
    ) -> "StreamingTimer":
        """Create a streaming timer scoped to this operation."""
        return self._sdk().start_streaming_timer(
            StreamingChunk(
                operation_name=self.name,
                provider_name=self.provider_name,
                request_model=self.request_model,
                response_model=response_model or self.response_model,
                attributes=_otel_attributes(attributes),
            ),
            context=self.otel_context,
            clock=clock,
            operation=self,
        )

    def mistral_completion(
        self,
        response: object,
        *,
        messages: Sequence[object] | None = None,
    ) -> None:
        """Record telemetry from a Mistral chat-completion response.

        The optional Mistral adapter extracts response id/model, finish reasons,
        token usage, and output messages. Input messages must be supplied by the
        caller because the Mistral response does not echo the request.
        """
        from .mistral import MistralChatCompletionAdapter

        self._sdk().record_completion(self, MistralChatCompletionAdapter(response, input_messages=messages))

    def completion(
        self,
        *,
        response_model: str | None = None,
        response_id: str | None = None,
        input_messages: Sequence[GenAiMessage] | None = None,
        output_messages: Sequence[GenAiMessage] | None = None,
        finish_reasons: Sequence[str] | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        attributes: Mapping[str, AttributeValue] | None = None,
    ) -> None:
        """Record completion metadata on this operation.

        This method is the span/metric counterpart to `inference_details(...)`:
        it enriches the operation span with response metadata and usage, records
        token metrics, and only copies supplied content to the span when
        `include_content=True`.
        """
        resolved_response_model = response_model if response_model is not None else self.response_model
        resolved_response_id = response_id if response_id is not None else self.response_id
        resolved_finish_reasons = finish_reasons if finish_reasons is not None else self.finish_reasons

        self._sdk().record_completion(
            self,
            ChatCompletionDetails(
                response_model=resolved_response_model,
                response_id=resolved_response_id,
                input_messages=input_messages,
                output_messages=output_messages,
                finish_reasons=resolved_finish_reasons,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            ),
            attributes=attributes,
        )


@dataclass(frozen=True, kw_only=True)
class InferenceDetails:
    """Payload for the GenAI inference details log event."""

    operation_name: str | None = None
    provider_name: str | None = None
    request_model: str | None = None
    request_max_tokens: int | None = None
    request_choice_count: int | None = None
    request_temperature: float | None = None
    request_top_p: float | None = None
    request_top_k: int | None = None
    request_stop_sequences: Sequence[str] | None = None
    request_frequency_penalty: float | None = None
    request_presence_penalty: float | None = None
    request_seed: int | None = None
    request_stream: bool | None = None
    request_reasoning_level: str | None = None
    response_model: str | None = None
    response_id: str | None = None
    response_time_to_first_chunk: float | None = None
    input_tokens: int | None = None
    cache_read_input_tokens: int | None = None
    cache_creation_input_tokens: int | None = None
    output_tokens: int | None = None
    reasoning_output_tokens: int | None = None
    input_messages: Sequence[GenAiMessage] | None = None
    output_messages: Sequence[GenAiMessage] | None = None
    prompt: str | None = None
    completion: str | None = None
    finish_reasons: Sequence[str] | None = None
    output_type: str | None = None
    conversation_id: str | None = None
    conversation_compacted: bool | None = None
    prompt_name: str | None = None
    prompt_version: str | None = None
    prompt_variables: Mapping[str, str] | None = None
    agent_id: str | None = None
    agent_name: str | None = None
    agent_description: str | None = None
    agent_version: str | None = None
    system_instructions: EventAttributeValue | None = None
    tool_definitions: EventAttributeValue | None = None
    server_address: str | None = None
    server_port: int | None = None
    attributes: ExtendedAttributes = field(default_factory=_empty_extended_attributes)


@dataclass(frozen=True, kw_only=True)
class EvaluationResult:
    """Payload for a GenAI evaluation result log event."""

    name: str
    score_value: float | None = None
    score_label: str | None = None
    explanation: str | None = None
    response_id: str | None = None
    attributes: ExtendedAttributes = field(default_factory=_empty_extended_attributes)


@dataclass(frozen=True, kw_only=True)
class TokenUsage:
    """Metric payload for GenAI input and output token usage."""

    input_tokens: int | None = None
    output_tokens: int | None = None
    operation_name: str | None = None
    provider_name: str | None = None
    request_model: str | None = None
    response_model: str | None = None
    attributes: Attributes = field(default_factory=_empty_attributes)


@dataclass(frozen=True, kw_only=True)
class OperationDuration:
    """Metric payload for operation, agent, and tool duration histograms."""

    duration_s: float
    operation_name: str | None = None
    provider_name: str | None = None
    request_model: str | None = None
    response_model: str | None = None
    server_address: str | None = None
    server_port: int | None = None
    error_type: str | None = None
    duration_metric: OperationDurationMetric = "client_operation"
    agent_name: str | None = None
    tool_name: str | None = None
    tool_type: str | None = None
    attributes: Attributes = field(default_factory=_empty_attributes)


@dataclass(frozen=True, kw_only=True)
class StreamingChunk:
    """Metric payload for streaming first-chunk and per-chunk timings."""

    operation_name: str | None = None
    provider_name: str | None = None
    request_model: str | None = None
    response_model: str | None = None
    attributes: Attributes = field(default_factory=_empty_attributes)


def operation_span_name(operation: Operation) -> str:
    """Return the semconv span name for the given operation."""
    if operation.span_name:
        return operation.span_name
    elif operation.name == c.OPERATION_NAME_CREATE_AGENT:
        if operation.agent_name:
            return f"{c.OPERATION_NAME_CREATE_AGENT} {operation.agent_name}"
        else:
            return c.OPERATION_NAME_CREATE_AGENT
    elif operation.name == c.OPERATION_NAME_INVOKE_AGENT:
        if operation.agent_name:
            return f"{c.OPERATION_NAME_INVOKE_AGENT} {operation.agent_name}"
        else:
            return c.OPERATION_NAME_INVOKE_AGENT
    elif operation.name == c.OPERATION_NAME_EXECUTE_TOOL and operation.tool_name:
        return f"{c.OPERATION_NAME_EXECUTE_TOOL} {operation.tool_name}"
    elif operation.name == c.OPERATION_NAME_PLAN:
        if operation.agent_name:
            return f"{c.OPERATION_NAME_PLAN} {operation.agent_name}"
        else:
            return c.OPERATION_NAME_PLAN
    elif operation.request_model:
        return f"{operation.name} {operation.request_model}"
    else:
        return operation.name


def operation_attributes(
    operation: Operation,
    *,
    transformers: OperationDataTransformers | None = None,
) -> dict[str, AttributeValue]:
    """Build span attributes for an operation from semconv fields."""
    attributes: dict[str, AttributeValue] = {
        c.ATTR_GEN_AI_OPERATION_NAME: operation.name,
    }
    attributes.update(_common_gen_ai_attributes(operation))
    _set_inference_span_attributes(attributes, operation)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_RESPONSE_ID, operation.response_id)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_USAGE_INPUT_TOKENS, operation.input_tokens)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_USAGE_CACHE_READ_INPUT_TOKENS, operation.cache_read_input_tokens)
    _set_if_not_none(
        attributes,
        c.ATTR_GEN_AI_USAGE_CACHE_CREATION_INPUT_TOKENS,
        operation.cache_creation_input_tokens,
    )
    _set_if_not_none(attributes, c.ATTR_GEN_AI_USAGE_OUTPUT_TOKENS, operation.output_tokens)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_USAGE_REASONING_OUTPUT_TOKENS, operation.reasoning_output_tokens)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_RESPONSE_FINISH_REASONS, operation.finish_reasons)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_RESPONSE_TIME_TO_FIRST_CHUNK, operation.response_time_to_first_chunk)
    _set_if_not_none(attributes, c.ATTR_SERVER_ADDRESS, operation.server_address)
    _set_if_not_none(attributes, c.ATTR_SERVER_PORT, operation.server_port)
    _set_operation_structured_span_attribute(
        attributes,
        operation,
        c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS,
        operation.system_instructions,
        transformers,
        overrides=operation.attributes,
    )
    _set_operation_structured_span_attribute(
        attributes,
        operation,
        c.ATTR_GEN_AI_TOOL_DEFINITIONS,
        operation.tool_definitions,
        transformers,
        overrides=operation.attributes,
    )
    _set_prompt_variable_attributes(attributes, operation.prompt_variables)
    _set_agent_span_attributes(attributes, operation)
    _set_tool_span_attributes(attributes, operation, transformers)
    attributes.update(operation.attributes)
    if transformers is not None:
        transformed = transformers.transform_attributes(
            attributes,
            operation_name=operation.name,
            signal="span",
            # Generated structured values are serialized only after their one
            # transformation. User overrides skipped generation and still need
            # to pass through the chain here.
            already_transformed=_STRUCTURED_OPERATION_SPAN_FIELDS - operation.attributes.keys(),
        )
        return normalize_otel_attributes(transformed)
    return attributes


def completion_span_attributes(
    operation: Operation,
    completion: ChatCompletionAdapter,
    *,
    attributes: Mapping[str, AttributeValue] | None = None,
    transformers: OperationDataTransformers | None = None,
) -> dict[str, AttributeValue]:
    """Build span attributes for a chat completion payload."""
    span_attributes: dict[str, AttributeValue] = {}
    _set_if_not_none(span_attributes, c.ATTR_GEN_AI_RESPONSE_MODEL, operation.response_model)
    _set_if_not_none(span_attributes, c.ATTR_GEN_AI_RESPONSE_ID, operation.response_id)
    _set_if_not_none(span_attributes, c.ATTR_GEN_AI_RESPONSE_FINISH_REASONS, operation.finish_reasons)
    _set_if_not_none(span_attributes, c.ATTR_GEN_AI_USAGE_INPUT_TOKENS, completion.input_tokens)
    _set_if_not_none(span_attributes, c.ATTR_GEN_AI_USAGE_OUTPUT_TOKENS, completion.output_tokens)
    if operation.include_content:
        _set_operation_structured_span_attribute(
            span_attributes,
            operation,
            c.ATTR_GEN_AI_INPUT_MESSAGES,
            completion.input_messages,
            transformers,
            overrides=attributes,
        )
        _set_operation_structured_span_attribute(
            span_attributes,
            operation,
            c.ATTR_GEN_AI_OUTPUT_MESSAGES,
            completion.output_messages,
            transformers,
            overrides=attributes,
        )
    span_attributes.update(attributes or {})
    return span_attributes


def inference_attributes(details: InferenceDetails) -> dict[str, EventAttributeValue]:
    """Build log attributes for a GenAI inference details event."""
    attributes: dict[str, EventAttributeValue] = {}
    _set_if_not_none(attributes, c.ATTR_GEN_AI_OPERATION_NAME, details.operation_name)
    attributes.update(_common_gen_ai_attributes(details))
    _set_inference_event_attributes(attributes, details)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_RESPONSE_ID, details.response_id)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_RESPONSE_FINISH_REASONS, details.finish_reasons)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_RESPONSE_TIME_TO_FIRST_CHUNK, details.response_time_to_first_chunk)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_USAGE_INPUT_TOKENS, details.input_tokens)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_USAGE_CACHE_READ_INPUT_TOKENS, details.cache_read_input_tokens)
    _set_if_not_none(
        attributes,
        c.ATTR_GEN_AI_USAGE_CACHE_CREATION_INPUT_TOKENS,
        details.cache_creation_input_tokens,
    )
    _set_if_not_none(attributes, c.ATTR_GEN_AI_USAGE_OUTPUT_TOKENS, details.output_tokens)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_USAGE_REASONING_OUTPUT_TOKENS, details.reasoning_output_tokens)
    _set_if_not_none(attributes, c.ATTR_SERVER_ADDRESS, details.server_address)
    _set_if_not_none(attributes, c.ATTR_SERVER_PORT, details.server_port)

    _set_if_not_none(attributes, c.ATTR_GEN_AI_INPUT_MESSAGES, _input_messages(details))
    _set_if_not_none(attributes, c.ATTR_GEN_AI_OUTPUT_MESSAGES, _output_messages(details))
    _set_if_not_none(attributes, c.ATTR_GEN_AI_SYSTEM_INSTRUCTIONS, details.system_instructions)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_TOOL_DEFINITIONS, details.tool_definitions)
    _set_prompt_variable_attributes(attributes, details.prompt_variables)
    _set_agent_event_attributes(attributes, details)

    attributes.update(details.attributes)
    return attributes


def evaluation_attributes(result: EvaluationResult) -> dict[str, EventAttributeValue]:
    """Build log attributes for a GenAI evaluation result event."""
    attributes: dict[str, EventAttributeValue] = {c.ATTR_GEN_AI_EVALUATION_NAME: result.name}
    _set_if_not_none(attributes, c.ATTR_GEN_AI_EVALUATION_SCORE_VALUE, result.score_value)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_EVALUATION_SCORE_LABEL, result.score_label)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_EVALUATION_EXPLANATION, result.explanation)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_RESPONSE_ID, result.response_id)
    attributes.update(result.attributes)
    return attributes


def token_usage_metric_attributes(usage: TokenUsage, token_type: str) -> dict[str, AttributeValue]:
    """Build metric attributes for one token usage datapoint."""
    attributes = _common_gen_ai_attributes(usage)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_OPERATION_NAME, usage.operation_name)
    attributes[c.ATTR_GEN_AI_TOKEN_TYPE] = token_type
    attributes.update(usage.attributes)
    return attributes


def operation_duration_metric_attributes(duration: OperationDuration) -> dict[str, AttributeValue]:
    """Build metric attributes for the duration metric selected by an operation."""
    if duration.duration_metric == "invoke_agent":
        attributes: dict[str, AttributeValue] = {}
        _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_MODEL, duration.request_model)
        _set_if_not_none(attributes, c.ATTR_GEN_AI_AGENT_NAME, duration.agent_name)
        _set_if_not_none(attributes, c.ATTR_ERROR_TYPE, duration.error_type)
    elif duration.duration_metric == "execute_tool":
        attributes = {}
        _set_if_not_none(attributes, c.ATTR_GEN_AI_AGENT_NAME, duration.agent_name)
        _set_if_not_none(attributes, c.ATTR_GEN_AI_TOOL_NAME, duration.tool_name)
        _set_if_not_none(attributes, c.ATTR_GEN_AI_TOOL_TYPE, duration.tool_type)
        _set_if_not_none(attributes, c.ATTR_ERROR_TYPE, duration.error_type)
    else:
        attributes = _common_gen_ai_attributes(duration)
        _set_if_not_none(attributes, c.ATTR_GEN_AI_OPERATION_NAME, duration.operation_name)
        _set_if_not_none(attributes, c.ATTR_SERVER_ADDRESS, duration.server_address)
        _set_if_not_none(attributes, c.ATTR_SERVER_PORT, duration.server_port)
        _set_if_not_none(attributes, c.ATTR_ERROR_TYPE, duration.error_type)
    attributes.update(duration.attributes)
    return attributes


def streaming_chunk_metric_attributes(chunk: StreamingChunk) -> dict[str, AttributeValue]:
    """Build metric attributes for streaming chunk timing datapoints."""
    attributes = _common_gen_ai_attributes(chunk)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_OPERATION_NAME, chunk.operation_name)
    attributes.update(chunk.attributes)
    return attributes


def _common_gen_ai_attributes(obj: CommonGenAiAttributes) -> dict[str, AttributeValue]:
    attributes: dict[str, AttributeValue] = {}
    _set_if_not_none(attributes, c.ATTR_GEN_AI_PROVIDER_NAME, obj.provider_name)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_MODEL, obj.request_model)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_RESPONSE_MODEL, obj.response_model)
    return attributes


def _set_inference_span_attributes(attributes: dict[str, AttributeValue], obj: Operation | InferenceDetails) -> None:
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_MAX_TOKENS, obj.request_max_tokens)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_CHOICE_COUNT, obj.request_choice_count)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_TEMPERATURE, obj.request_temperature)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_TOP_P, obj.request_top_p)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_TOP_K, obj.request_top_k)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_STOP_SEQUENCES, obj.request_stop_sequences)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_FREQUENCY_PENALTY, obj.request_frequency_penalty)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_PRESENCE_PENALTY, obj.request_presence_penalty)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_SEED, obj.request_seed)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_STREAM, obj.request_stream)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_REASONING_LEVEL, obj.request_reasoning_level)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_OUTPUT_TYPE, obj.output_type)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_CONVERSATION_ID, obj.conversation_id)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_CONVERSATION_COMPACTED, obj.conversation_compacted)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_PROMPT_NAME, obj.prompt_name)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_PROMPT_VERSION, obj.prompt_version)


def _set_inference_event_attributes(
    attributes: dict[str, EventAttributeValue],
    obj: Operation | InferenceDetails,
) -> None:
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_MAX_TOKENS, obj.request_max_tokens)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_CHOICE_COUNT, obj.request_choice_count)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_TEMPERATURE, obj.request_temperature)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_TOP_P, obj.request_top_p)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_TOP_K, obj.request_top_k)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_STOP_SEQUENCES, obj.request_stop_sequences)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_FREQUENCY_PENALTY, obj.request_frequency_penalty)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_PRESENCE_PENALTY, obj.request_presence_penalty)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_SEED, obj.request_seed)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_STREAM, obj.request_stream)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_REQUEST_REASONING_LEVEL, obj.request_reasoning_level)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_OUTPUT_TYPE, obj.output_type)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_CONVERSATION_ID, obj.conversation_id)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_CONVERSATION_COMPACTED, obj.conversation_compacted)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_PROMPT_NAME, obj.prompt_name)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_PROMPT_VERSION, obj.prompt_version)


def _set_agent_span_attributes(attributes: dict[str, AttributeValue], obj: Operation) -> None:
    _set_if_not_none(attributes, c.ATTR_GEN_AI_AGENT_ID, obj.agent_id)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_AGENT_NAME, obj.agent_name)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_AGENT_DESCRIPTION, obj.agent_description)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_AGENT_VERSION, obj.agent_version)


def _set_agent_event_attributes(attributes: dict[str, EventAttributeValue], obj: InferenceDetails) -> None:
    _set_if_not_none(attributes, c.ATTR_GEN_AI_AGENT_ID, obj.agent_id)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_AGENT_NAME, obj.agent_name)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_AGENT_DESCRIPTION, obj.agent_description)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_AGENT_VERSION, obj.agent_version)


def _set_tool_span_attributes(
    attributes: dict[str, AttributeValue],
    obj: Operation,
    transformers: OperationDataTransformers | None,
) -> None:
    _set_if_not_none(attributes, c.ATTR_GEN_AI_TOOL_NAME, obj.tool_name)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_TOOL_CALL_ID, obj.tool_call_id)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_TOOL_DESCRIPTION, obj.tool_description)
    _set_if_not_none(attributes, c.ATTR_GEN_AI_TOOL_TYPE, obj.tool_type)
    _set_operation_structured_span_attribute(
        attributes,
        obj,
        c.ATTR_GEN_AI_TOOL_CALL_ARGUMENTS,
        obj.tool_call_arguments,
        transformers,
        overrides=obj.attributes,
    )
    _set_operation_structured_span_attribute(
        attributes,
        obj,
        c.ATTR_GEN_AI_TOOL_CALL_RESULT,
        obj.tool_call_result,
        transformers,
        overrides=obj.attributes,
    )


def _set_operation_structured_span_attribute(
    attributes: dict[str, AttributeValue],
    operation: Operation,
    field: str,
    value: EventAttributeValue | None,
    transformers: OperationDataTransformers | None,
    *,
    overrides: Mapping[str, AttributeValue] | None,
) -> None:
    if overrides is not None and field in overrides:
        return
    _set_if_not_none(
        attributes,
        field,
        _operation_structured_span_attribute(operation, field, value, transformers),
    )


def _operation_structured_span_attribute(
    operation: Operation,
    field: str,
    value: EventAttributeValue | None,
    transformers: OperationDataTransformers | None,
) -> AttributeValue | None:
    if transformers is not None:
        value = transformers.transform(value, operation_name=operation.name, signal="span", field=field)
    return normalize_otel_attribute(value, structured_document=True)


def _set_prompt_variable_attributes[AttributeT](
    attributes: dict[str, AttributeT],
    prompt_variables: Mapping[str, AttributeT] | None,
) -> None:
    if prompt_variables is None:
        return

    for name, value in prompt_variables.items():
        attributes[f"{c.ATTR_GEN_AI_PROMPT_VARIABLE}.{name}"] = value


def _input_messages(details: InferenceDetails) -> Sequence[GenAiMessage] | None:
    if details.input_messages is not None:
        return details.input_messages
    elif details.prompt is not None:
        return ({"role": "user", "parts": ({"type": "text", "content": details.prompt},)},)
    else:
        return None


def _output_messages(details: InferenceDetails) -> Sequence[GenAiMessage] | None:
    if details.output_messages is not None:
        return details.output_messages
    elif details.completion is not None:
        return ({"role": "assistant", "parts": ({"type": "text", "content": details.completion},)},)
    else:
        return None


def _set_if_not_none[SetValue](attributes: dict[str, SetValue], key: str, value: SetValue | None) -> None:
    if value is None:
        return
    attributes[key] = value


def _sdk() -> "ObservabilitySDK":
    from .sdk import require_configured

    return require_configured()


def _operation_context(context: Context | None, parent: Operation | None) -> Context | None:
    if context is not None and parent is not None:
        message = "context cannot be combined with parent"
        raise ValueError(message)
    elif parent is not None:
        return parent.otel_context
    else:
        return context


def _otel_attributes(attributes: Mapping[str, AttributeValue] | None) -> Mapping[str, AttributeValue]:
    if attributes is None:
        return {}
    return attributes


def _extended_attributes(attributes: ExtendedAttributes | None) -> ExtendedAttributes:
    if attributes is None:
        return {}
    return attributes


def _log_attributes(
    attributes: ExtendedAttributes | None,
    *,
    features: Features | None,
) -> ExtendedAttributes:
    resolved_attributes: dict[str, EventAttributeValue] = dict(feature_attributes(features))
    resolved_attributes.update(_extended_attributes(attributes))
    return resolved_attributes


def feature_attributes(features: Features | None) -> dict[str, AttributeValue]:
    """Map requested Mistral observability features to stable OTLP attributes."""
    attributes: dict[str, AttributeValue] = {}
    if features is None:
        return attributes
    if features.sensitive_data is not None:
        attributes[ATTR_MISTRAL_OBS_FEATURES_DETECTOR] = features.sensitive_data
    if features.moderation is not None:
        attributes[ATTR_MISTRAL_OBS_FEATURES_MODERATION] = features.moderation
    if features.judges is not None:
        attributes[ATTR_MISTRAL_OBS_FEATURES_JUDGE] = tuple(features.judges)
    return attributes


def _operation_log_attributes(
    attributes: ExtendedAttributes | None,
    *,
    operation: Operation,
    features: Features | None,
) -> ExtendedAttributes:
    resolved_attributes: dict[str, EventAttributeValue] = {}
    _set_if_not_none(resolved_attributes, c.ATTR_GEN_AI_CONVERSATION_ID, operation.conversation_id)
    _set_if_not_none(resolved_attributes, c.ATTR_GEN_AI_CONVERSATION_COMPACTED, operation.conversation_compacted)
    resolved_attributes.update(_log_attributes(attributes, features=features))
    return resolved_attributes


def _check_end_time(start_time_unix_nano: int | None, end_time_unix_nano: int | None) -> None:
    if start_time_unix_nano is None or end_time_unix_nano is None:
        return
    if end_time_unix_nano < start_time_unix_nano:
        message = "end_time_unix_nano must not precede start_time_unix_nano"
        raise ValueError(message)


def _span_context(*, trace_id: str | int, span_id: str | int) -> Context:
    span = NonRecordingSpan(
        SpanContext(
            trace_id=parse_otel_id(trace_id, name="trace_id", hex_digits=32),
            span_id=parse_otel_id(span_id, name="span_id", hex_digits=16),
            is_remote=True,
            trace_flags=TraceFlags(TraceFlags.SAMPLED),
            trace_state=TraceState(),
        )
    )
    return set_span_in_context(span)
