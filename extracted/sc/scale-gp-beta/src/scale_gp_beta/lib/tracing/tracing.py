import logging
from typing import Optional

from scale_gp_beta.types import SpanType

from .span import Span, BaseSpan, NoOpSpan
from .util import is_disabled
from .scope import Scope
from .trace import Trace, BaseTrace, NoOpTrace
from .types import SpanInputParam, SpanOutputParam, SpanMetadataParam
from .trace_queue_manager import TraceQueueManager, tracing_queue_manager

log: logging.Logger = logging.getLogger(__name__)


def current_span() -> Optional[BaseSpan]:
    """Retrieves the currently active span from the execution context.

    This function relies on `contextvars` to manage the active span in
    a context-local manner, making it safe for concurrent execution
    environments (e.g., threads, asyncio tasks).

    Returns:
        Optional[BaseSpan]: The current BaseSpan instance if one is active,
                            otherwise None. This could be a 'Span' or 'NoOpSpan'.
    """
    return Scope.get_current_span()


def current_trace() -> Optional[BaseTrace]:
    """Retrieves the currently active trace from the execution context.

    Similarly, to `current_span()`, this uses `contextvars` for context-local
    trace management.

    Returns:
        Optional[BaseTrace]: The current BaseTrace instance if one is active,
                             otherwise None. This could be a 'Trace' or 'NoOpTrace'.
    """
    return Scope.get_current_trace()


def flush_queue() -> None:
    """
    Blocking flush of all requests in the queue.

    Useful for distributed applications to ensure spans have been committed before continuing.
    :return:
    """
    queue_manager = tracing_queue_manager()
    queue_manager.flush_queue()


def create_trace(
        name: str,
        span_type: SpanType = "TRACER",
        input: Optional[SpanInputParam] = None,
        output: Optional[SpanOutputParam] = None,
        metadata: Optional[SpanMetadataParam] = None,
        span_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        group_id: Optional[str] = None,
        queue_manager: Optional[TraceQueueManager] = None,
) -> BaseTrace:
    """Creates a new trace and root span instance.

    A trace represents a single, logical operation or workflow. It groups multiple
    spans together. If tracing is disabled (via the 'DISABLE_SCALE_TRACING'
    environment variable), a `NoOpTrace` instance is returned which performs no
    actual tracing operations.

    When a trace is started (e.g., by using it as a context manager or calling its
    `start()` method), it becomes the `current_trace()` in the active scope.
    Similarly, the root span instance becomes the `current_span()` in the active
    scope.

    Args:
        name: The name of the trace.
        span_type (Optional[SpanType]): Type of root span.
        input (Optional[SpanInputParam]): Input of root span.
        output (Optional[SpanOutputParam]): Output of root span.
        metadata (Optional[SpanMetadataParam]): An optional, user-defined metadata.
        span_id (Optional[str]): An optional, user-defined ID for the root span.
                                 Max length is 38 characters.
        trace_id (Optional[str]): An optional, user-defined ID for the trace.
                                  If None, a unique trace ID will be generated.
                                  Max length is 38 characters.
        group_id (Optional[str]): An optional, id to group traces.
        queue_manager (Optional[TraceQueueManager], optional): An optional `TraceQueueManager`.
            Useful for when you need explicit control of flushing and client behavior.

    Returns:
        BaseTrace: A `Trace` instance if tracing is enabled, or a `NoOpTrace`
                   instance if tracing is disabled.
    """
    impl_input: SpanInputParam = input or {}
    impl_output: SpanOutputParam = output or {}
    impl_metadata: SpanMetadataParam = metadata or {}

    if is_disabled():
        log.debug(f"Tracing is disabled. Not creating a new trace.")
        return NoOpTrace(
            name=name,
            trace_id=trace_id,
            span_id=span_id,
            group_id=group_id,
            span_type=span_type,
            input=impl_input,
            output=impl_output,
            metadata=impl_metadata,
        )

    active_trace = current_trace()
    if active_trace is not None:
        log.warning(f"Trace with id {active_trace.trace_id} is already active. Creating a new trace anyways.")

    queue_manager = queue_manager or tracing_queue_manager()
    trace = Trace(
        name=name,
        trace_id=trace_id,
        span_id=span_id,
        group_id=group_id,
        queue_manager=queue_manager,
        span_type=span_type,
        input=impl_input,
        output=impl_output,
        metadata=impl_metadata,
    )
    log.debug(f"Created new trace: {trace.trace_id}")

    return trace


def create_span(
    name: str,
    span_type: SpanType = "STANDALONE",
    input: Optional[SpanInputParam] = None,
    output: Optional[SpanOutputParam] = None,
    metadata: Optional[SpanMetadataParam] = None,
    span_id: Optional[str] = None,
    parent_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    group_id: Optional[str] = None,
    queue_manager: Optional[TraceQueueManager] = None,
) -> BaseSpan:
    """Creates a new span instance.

    A span represents a single unit of work or operation within a trace. Spans
    can be nested to form a hierarchy.

    If tracing is disabled (via 'DISABLE_SCALE_TRACING' environment variable),
    a `NoOpSpan` is returned. Additionally, if no explicit `parent` (Trace or Span)
    is provided and there is no `current_trace()` active in the scope, a `NoOpSpan`
    will also be returned to prevent orphaned spans.

    When a span is started (e.g., via context manager or `start()`), it becomes
    the `current_span()` in the active scope.

    If explicitly setting 'parent_id' and 'trace_id', ensure that the parent span
    has the same 'trace_id'.

    Args:
        name (str): A descriptive name for the span (e.g., "database_query",
                    "http_request").
        span_type (SpanType): The type of the span.
        input (Optional[SpanInputParam], optional): A dictionary containing
            input data or parameters relevant to this span's operation. Defaults to None.
        output (Optional[SpanOutputParam], optional): A dictionary containing
            output data or results from this span's operation. Defaults to None.
        metadata (Optional[SpanMetadataParam], optional):
            A dictionary for arbitrary key-value pairs providing additional
            context or annotations for the span. Values should be simple types.
            Defaults to None.
        span_id (Optional[str]): An optional, user-defined ID for the span.
        parent_id (Optional[str], optional): A `Span` id. Used for explicit control.
        Defaults to span id fetched from the active scope.
        trace_id (Optional[str], optional): A `Trace` id. Used for explicit control.
            Default to trace id fetched from the active scope.
        group_id (Optional[str]): An optional, id to group traces.
        queue_manager (Optional[TraceQueueManager], optional): An optional `TraceQueueManager`.
            Useful for when you need explicit control of flushing and client behavior.

    Returns:
        BaseSpan: A `Span` instance if tracing is enabled and a valid trace context
                  exists, or a `NoOpSpan` otherwise.
    """
    impl_input: SpanInputParam = input or {}
    impl_output: SpanOutputParam = output or {}
    impl_metadata: SpanMetadataParam = metadata or {}

    scoped_trace = current_trace()
    scoped_trace_id = scoped_trace.trace_id if scoped_trace else None
    scoped_group_id = scoped_trace.group_id if scoped_trace else None
    scoped_span = current_span()
    scoped_span_id = scoped_span.span_id if scoped_span else None

    parent_span_id: Optional[str] = parent_id or scoped_span_id
    # TODO: preference should be trace_id -> trace_id from parent span if parent_id present -> scoped_trace_id
    # group_id -> group_id from trace if trace_id specified -> group_id from span if span_id -> scoped_group_id
    impl_trace_id: Optional[str] = trace_id or scoped_trace_id
    impl_group_id: Optional[str] = group_id or scoped_group_id

    # TODO: do a check to ensure trace_id of parent_span matches trace_id (when trace_id is specified)

    noop_span = NoOpSpan(
        name=name,
        span_id=span_id,
        parent_span_id=parent_span_id,
        trace_id=impl_trace_id,
        group_id=impl_group_id,
        input=impl_input,
        output=impl_output,
        metadata=impl_metadata,
        span_type=span_type,
    )

    if is_disabled():
        return noop_span

    if impl_trace_id is None:
        log.debug(f"Attempting to create a span with no trace")
        return noop_span

    queue_manager = queue_manager or tracing_queue_manager()
    span = Span(
        name=name,
        span_id=span_id,
        parent_span_id=parent_span_id,
        trace_id=impl_trace_id,
        group_id=impl_group_id,
        input=impl_input,
        output=impl_output,
        metadata=impl_metadata,
        queue_manager=queue_manager,
        span_type=span_type,
    )
    log.debug(f"Created new span: {span.span_id}")

    return span
