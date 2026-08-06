from __future__ import annotations

import logging
from copy import deepcopy
from typing import TYPE_CHECKING, Type, Optional, cast
from threading import RLock
from typing_extensions import override

from scale_gp_beta.types import SpanType, SpanStatus
from scale_gp_beta.types.span_create_param import SpanCreateParam as SpanCreateRequest

from .util import iso_timestamp, generate_span_id
from .scope import Scope
from .types import ErrorCategory, SpanInputParam, SpanOutputParam, SpanMetadataParam
from .exceptions import CategorizedError, ParamsCreationError

if TYPE_CHECKING:
    import contextvars
    from types import TracebackType

    from .trace_queue_manager import TraceQueueManager

log: logging.Logger = logging.getLogger(__name__)

_ERROR_CATEGORIES = frozenset({"application", "platform", "unknown"})


def _normalize_error_category(value: object) -> ErrorCategory:
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in _ERROR_CATEGORIES:
            return cast(ErrorCategory, normalized)
    return "unknown"


class BaseSpan:
    """Base class for all span types, providing common attributes and context management.

    A span represents a single unit of work or operation within a trace. This base
    class defines the core interface and properties for spans, such as name, IDs,
    timestamps, and methods for starting and ending the span's lifecycle.

    It is intended to be subclassed by concrete span implementations like `Span`
    (for active tracing) and `NoOpSpan` (for when tracing is disabled).

    Attributes:
        name (str): The human-readable name of the span.
        trace_id (str): The ID of the trace this span belongs to.
        span_id (str): The unique ID of this span.
        parent_span_id (Optional[str]): The ID of the parent span, if this is a child span.
        start_time (Optional[str]): ISO 8601 timestamp of when the span started.
                                     Set by the `start()` method.
        end_time (Optional[str]): ISO 8601 timestamp of when the span ended.
                                   Set by the `end()` method.
        input (Optional[dict[str, Any]]): Input data or parameters for the span's operation.
        output (Optional[dict[str, Any]]): Output data or results from the span's operation.
        metadata (Optional[dict[str, Any]]): Additional arbitrary key-value metadata for the span.
        _contextvar_token (Optional[contextvars.Token]): Token for managing the span's presence
                                                        in the current execution context.
    """

    def __init__(
        self,
        name: str,
        trace_id: Optional[str] = None,
        queue_manager: Optional[TraceQueueManager] = None,
        span_id: Optional[str] = None,
        parent_span_id: Optional[str] = None,
        group_id: Optional[str] = None,
        input: Optional[SpanInputParam] = None,
        output: Optional[SpanOutputParam] = None,
        metadata: Optional[SpanMetadataParam] = None,
        span_type: SpanType = "STANDALONE"
    ):
        self._name = name
        self._trace_id: str = trace_id or "no_trace_id"
        self._group_id = group_id
        self._span_id: str = span_id or generate_span_id()
        self._parent_span_id = parent_span_id
        self._start_time: Optional[str] = None
        self._end_time: Optional[str] = None
        self._input: SpanInputParam = input or {}
        self._output: SpanOutputParam = output or {}
        self._metadata: SpanMetadataParam = metadata or {}
        self._span_type: SpanType = span_type
        self._status: SpanStatus = "SUCCESS"
        self._queue_manager = queue_manager

        self._contextvar_token: Optional[contextvars.Token[Optional[BaseSpan]]] = None
        self._lock = RLock()

    def start(self) -> None:
        pass

    def end(self) -> None:
        pass

    def flush(self, blocking: bool = True) -> None:
        pass

    @property
    def name(self) -> str:
        return self._name

    @property
    def trace_id(self) -> str:
        return self._trace_id

    @property
    def group_id(self) -> Optional[str]:
        return self._group_id

    @property
    def span_id(self) -> str:
        return self._span_id

    @property
    def parent_span_id(self) -> Optional[str]:
        return self._parent_span_id

    @property
    def status(self) -> SpanStatus:
        return self._status

    @property
    def span_type(self) -> SpanType:
        return self._span_type

    # with setters
    @property
    def start_time(self) -> Optional[str]:
        return self._start_time

    @start_time.setter
    def start_time(self, value: Optional[str]) -> None:
        with self._lock:
            self._start_time = value

    @property
    def end_time(self) -> Optional[str]:
        return self._end_time

    @end_time.setter
    def end_time(self, value: Optional[str]) -> None:
        with self._lock:
            self._end_time = value

    @property
    def metadata(self) -> SpanMetadataParam:
        return self._metadata

    @metadata.setter
    def metadata(self, value: SpanMetadataParam) -> None:
        # this does not protect against span.metadata["foo"] = "bar" which uses the getter, ditto input and output
        with self._lock:
            self._metadata = value

    @property
    def input(self) -> SpanInputParam:
        return self._input

    @input.setter
    def input(self, value: SpanInputParam) -> None:
        with self._lock:
            self._input = value

    @property
    def output(self) -> SpanOutputParam:
        return self._output

    @output.setter
    def output(self, value: SpanOutputParam) -> None:
        with self._lock:
            self._output = value

    def set_error(
            self,
            error_type: Optional[str] = None,
            error_message: Optional[str] = None,
            exception: Optional[BaseException] = None,
            error_category: Optional[ErrorCategory] = None,
    ) -> None:
        # Naively record details in metadata for now, note that error capture only supported in context manager
        with self._lock:
            exception_type = type(exception).__name__ if exception else None
            exception_message = str(exception) if exception else None
            category = error_category
            if category is None and isinstance(exception, CategorizedError):
                category = exception.error_category
            self._status = "ERROR"
            self.metadata["error"] = True
            self.metadata["error_type"] = error_type or exception_type
            self.metadata["error_message"] = error_message or exception_message
            self.metadata["error_category"] = _normalize_error_category(category)

    def __enter__(self) -> BaseSpan:
        self.start()
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> None:
        # TODO: support error observations when using direct span.start() and span.end()
        if exc_type is not None:
            self.set_error(exception=exc_val)
        self.end()

    def to_request_params(self) -> SpanCreateRequest:
        with self._lock:
            if self.start_time is None:
                raise ParamsCreationError("No start time specified")

            request_data = SpanCreateRequest(
                name=self.name,
                id=self.span_id,
                trace_id=self.trace_id,
                start_timestamp=self.start_time,
                input=self.input,
                output=self.output,
                metadata=self.metadata,
                status=self.status,
                type=self.span_type
            )

            if self.end_time is not None:
                request_data["end_timestamp"] = self.end_time

            # parent_span_id is optional (root spans)
            if self.parent_span_id is not None:
                request_data["parent_id"] = self.parent_span_id

            if self.group_id is not None:
                request_data["group_id"] = self.group_id

            # ensure no future changes to metadata, input or output changes request_data, full isolation
            request_data = deepcopy(request_data)
            return request_data

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"span_id='{self.span_id}', "
            f"trace_id='{self.trace_id}', "
            f"parent_span_id='{self.parent_span_id}', "
            f"group_id='{self.group_id}', "
            f"start_time='{self.start_time}', "
            f"end_time='{self.end_time}', "
            f"input='{self.input}', "
            f"output='{self.output}', "
            f"metadata='{self.metadata}', "
            f"span_type='{self.span_type}', "
            f"status='{self.status}'"
            ")"
        )

    @override
    def __str__(self) -> str:
        return self.__repr__()


class NoOpSpan(BaseSpan):
    @override
    def start(self) -> None:
        if self.start_time is not None:
            log.warning(f"Span {self.name}: {self.span_id} has already started at {self.start_time}")
            return

        self.start_time = iso_timestamp()
        self._contextvar_token = Scope.set_current_span(self)

    @override
    def end(self) -> None:
        if self.end_time is not None:
            log.warning(f"Span {self.name}: {self.span_id} has already ended at {self.end_time}")
            return

        if self._contextvar_token is None:
            log.warning(f"Span {self.name}: {self.span_id} has not started yet.")
            return

        self.end_time = iso_timestamp()
        Scope.reset_current_span(self._contextvar_token)
        self._contextvar_token = None


class Span(BaseSpan):
    """An operational span implementation that records and reports tracing data.

    `Span` instances represent actual units of work that are part of an active trace.
    They record timestamps, manage their context in `Scope`, and interact with the
    `TraceQueueManager` to report their start and end events for later export.
    """

    def __init__(
        self,
        name: str,
        trace_id: str,
        queue_manager: TraceQueueManager,
        span_id: Optional[str] = None,
        parent_span_id: Optional[str] = None,
        group_id: Optional[str] = None,
        input: Optional[SpanInputParam] = None,
        output: Optional[SpanOutputParam] = None,
        metadata: Optional[SpanMetadataParam] = None,
        span_type: SpanType = "STANDALONE",
    ):
        super().__init__(name, trace_id, queue_manager, span_id, parent_span_id, group_id, input, output, metadata, span_type)
        self._queue_manager: TraceQueueManager = queue_manager
        self._trace_id: str = trace_id

    @override
    def flush(self, blocking: bool = True) -> None:
        """Export span. Defaults to in-thread and will block until the request is complete.

        With `blocking=False`, this method will enqueue the request for the background worker.
        The background worker batches and sends asynchronously.
        :param blocking:
        """
        if blocking:
            self._queue_manager.export_now(self)
        else:
            self._queue_manager.enqueue(self)

    @override
    def start(self) -> None:
        """Starts the operational Span.

        Sets the `start_time`, reports the span start to the `TraceQueueManager`
        , and registers this span as the current span.
        """
        with self._lock:
            if self.start_time is not None:
                log.warning(f"Span {self.name}: {self.span_id} has already started at {self.start_time}")
                return

            self.start_time = iso_timestamp()
            self._queue_manager.report_span_start(self)
            self._contextvar_token = Scope.set_current_span(self)

    @override
    def end(self) -> None:
        """Ends the operational Span.

        Sets the `end_time`, reports the span end (with its complete data) to the
        `TraceQueueManager` for queuing and export, and resets this span from the
        `Scope`.
        """
        with self._lock:
            if self.end_time is not None:
                log.warning(f"Span {self.name}: {self.span_id} has already ended at {self.end_time}")
                return
            if self._contextvar_token is None:
                log.warning(
                    (
                        f"Span {self.name}: {self.span_id} attempting to end without a valid context token. "
                        "Was start() called and completed successfully?"
                    )
                )
                return

            self.end_time = iso_timestamp()
            self._queue_manager.report_span_end(self)
            Scope.reset_current_span(self._contextvar_token)
            self._contextvar_token = None
