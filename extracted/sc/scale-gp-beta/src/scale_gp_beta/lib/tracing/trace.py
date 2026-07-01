import logging
import contextvars
from types import TracebackType
from typing import Type, Optional
from typing_extensions import override

from scale_gp_beta.types import SpanType, SpanStatus

from .span import Span, BaseSpan, NoOpSpan
from .util import generate_trace_id
from .scope import Scope
from .types import SpanInputParam, SpanOutputParam, SpanMetadataParam
from .trace_queue_manager import TraceQueueManager

log: logging.Logger = logging.getLogger(__name__)


class BaseTrace:
    def __init__(
            self,
            queue_manager: Optional[TraceQueueManager],
            root_span: BaseSpan,
            trace_id: str
    ) -> None:
        self._trace_id = trace_id
        self.queue_manager = queue_manager

        self._in_progress = False
        self._contextvar_token: Optional[contextvars.Token[Optional[BaseTrace]]] = None

        self.root_span = root_span

    def start(self) -> None:
        pass

    def end(self) -> None:
        pass

    def flush(self, blocking: bool = True) -> None:
        pass

    @property
    def metadata(self) -> SpanMetadataParam:
        return self.root_span.metadata

    @metadata.setter
    def metadata(self, value: SpanMetadataParam) -> None:
        self.root_span.metadata = value

    @property
    def input(self) -> SpanInputParam:
        return self.root_span.input

    @input.setter
    def input(self, value: SpanInputParam) -> None:
        self.root_span.input = value

    @property
    def output(self) -> SpanOutputParam:
        return self.root_span.output

    @output.setter
    def output(self, value: SpanOutputParam) -> None:
        self.root_span.output = value

    # no setters
    @property
    def name(self) -> Optional[str]:
        return self.root_span.name

    @property
    def span_id(self) -> Optional[str]:
        return self.root_span.span_id

    @property
    def trace_id(self) -> Optional[str]:
        return self._trace_id

    @property
    def group_id(self) -> Optional[str]:
        return self.root_span.group_id

    @property
    def span_type(self) -> SpanType:
        return self.root_span.span_type

    @property
    def status(self) -> SpanStatus:
        return self.root_span.status

    def set_error(
            self,
            error_type: Optional[str] = None,
            error_message: Optional[str] = None,
            exception: Optional[BaseException] = None,
    ) -> None:
        self.root_span.set_error(error_type=error_type, error_message=error_message, exception=exception)

    def __enter__(self) -> "BaseTrace":
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        self.end()

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"trace_id='{self.trace_id}', "
            f"root_span='{repr(self.root_span)}', "
            ")"
        )

    @override
    def __str__(self) -> str:
        return self.__repr__()


class NoOpTrace(BaseTrace):
    def __init__(
            self,
            name: str,
            queue_manager: Optional[TraceQueueManager] = None,
            trace_id: Optional[str] = None,
            span_id: Optional[str] = None,
            group_id: Optional[str] = None,
            span_type: SpanType = "TRACER",
            input: Optional[SpanInputParam] = None,
            output: Optional[SpanOutputParam] = None,
            metadata: Optional[SpanMetadataParam] = None,
    ):
        trace_id = trace_id or generate_trace_id()
        root_span = NoOpSpan(
            name=name,
            span_id=span_id,
            trace_id=trace_id,
            group_id=group_id,
            queue_manager=queue_manager,
            metadata=metadata,
            span_type=span_type,
            input=input,
            output=output,
        )
        super().__init__(queue_manager, root_span, trace_id)

    @override
    def start(self) -> None:
        self.root_span.start()

    @override
    def end(self) -> None:
        self.root_span.end()


class Trace(BaseTrace):
    def __init__(
            self,
            name: str,
            queue_manager: TraceQueueManager,
            trace_id: Optional[str] = None,
            span_id: Optional[str] = None,
            group_id: Optional[str] = None,
            span_type: SpanType = "TRACER",
            input: Optional[SpanInputParam] = None,
            output: Optional[SpanOutputParam] = None,
            metadata: Optional[SpanMetadataParam] = None,
    ):
        trace_id = trace_id or generate_trace_id()
        root_span = Span(
            name=name,
            span_id=span_id,
            trace_id=trace_id,
            group_id=group_id,
            queue_manager=queue_manager,
            metadata=metadata,
            span_type=span_type,
            input=input,
            output=output,
        )
        super().__init__(queue_manager, root_span, trace_id)
        self.queue_manager: TraceQueueManager = queue_manager

    @override
    def start(self) -> None:
        if self._in_progress:
            log.warning(f"Trace already started: {self.trace_id}")
            return

        self._in_progress = True
        self.queue_manager.report_trace_start(self)  # no-op
        self._contextvar_token = Scope.set_current_trace(self)

        self.root_span.start()

    @override
    def end(self) -> None:
        if not self._in_progress:
            log.warning(f"Ending trace which is not active: {self.trace_id}")
            return
        if self._contextvar_token is None:
            log.warning(f"Ending trace which is not active: {self.trace_id}, contextvar_token not set")
            return

        self._in_progress = False
        self.queue_manager.report_trace_end(self)  # no-op
        Scope.reset_current_trace(self._contextvar_token)
        self._contextvar_token = None

        self.root_span.end()

    @override
    def flush(self, blocking: bool = True) -> None:
        self.root_span.flush(blocking=blocking)
