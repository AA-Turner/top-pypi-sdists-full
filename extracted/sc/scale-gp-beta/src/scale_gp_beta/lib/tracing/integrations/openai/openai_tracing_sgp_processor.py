# The following `type: ignore` is necessary because this file provides an optional
# integration for the 'openai-agents' library. The linter will report missing
# imports if the library isn't installed in the development environment, but the
# code handles this gracefully at runtime with a try/except block.
# type: ignore
import logging
from typing import TYPE_CHECKING, Any, Dict, Optional

from scale_gp_beta.lib.tracing.span import BaseSpan
from scale_gp_beta.lib.tracing.tracing import create_span, flush_queue, create_trace, tracing_queue_manager
from scale_gp_beta.lib.tracing.trace_queue_manager import TraceQueueManager

from .utils import sgp_span_name, parse_metadata, extract_response, parse_input_output
from .openai_span_type_map import openai_span_type_map

log: logging.Logger = logging.getLogger(__name__)

try:
    from agents.tracing import (
        Span as OpenAISpan,
        Trace as OpenAITrace,
        SpanData as OpenAISpanData,
        ResponseSpanData as OpenAIResponseSpanData,
        TracingProcessor,
    )

    _openai_agents_installed = True
except ImportError:
    _openai_agents_installed = False
    TracingProcessor = object
    class _Fallback:
        pass

    OpenAISpan = _Fallback
    OpenAITrace = _Fallback
    OpenAISpanData = _Fallback
    OpenAIResponseSpanData = _Fallback

    if TYPE_CHECKING:
        OpenAISpan = Any
        OpenAITrace = Any
        OpenAISpanData = Any
        OpenAIResponseSpanData = Any


class OpenAITracingSGPProcessor(TracingProcessor):
    """
    An SGP tracing processor that integrates with OpenAI Agents SDK.

    This processor requires the 'openai-agents' library to be installed.
    It will raise an ImportError on initialization if the library is not found.
    """

    def __init__(
            self,
            *,
            queue_manager: Optional[TraceQueueManager] = None,
    ):
        """
        Initializes the processor.

        Args:
            queue_manager: An optional custom trace queue manager.

        Raises:
            ImportError: If the 'openai-agents' package is not installed.
        """
        # This runtime check is the gatekeeper. If 'openai-agents' isn't
        # installed, no instance of this class can be created.
        if not _openai_agents_installed:
            raise ImportError(
                "The 'openai-agents' package is required to use the OpenAITracingSGPProcessor. "
                "Please install it with: pip install 'openai-agents'"
            )

        self._queue_manager = queue_manager or tracing_queue_manager()
        self._spans: Dict[str, BaseSpan] = {}

    def on_trace_start(self, openai_trace: "OpenAITrace") -> None:
        sgp_trace = create_trace(
            name=openai_trace.name or "Agent Workflow",
            span_type="AGENT_WORKFLOW",
            group_id=openai_trace.group_id,
            trace_id=openai_trace.trace_id,
            metadata={"openai_metadata": openai_trace.metadata or {}},
        )
        sgp_trace.start()
        self._spans[openai_trace.trace_id] = sgp_trace.root_span

    def on_trace_end(self, openai_trace: "OpenAITrace") -> None:
        root_span = self._spans.pop(openai_trace.trace_id, None)
        if root_span is None:
            log.warning(f"No root span found for trace_id: {openai_trace.trace_id}")
            return
        root_span.end()

    def on_span_start(self, openai_span: "OpenAISpan") -> None:
        _spans_key = openai_span.parent_id or openai_span.trace_id
        parent_span = self._spans.get(_spans_key)
        span_data = openai_span.span_data

        if not parent_span:
            log.warning(f"No parent span found for span_id: {openai_span.span_id}")
            return

        name = sgp_span_name(openai_span)
        sgp_span_type = openai_span_type_map(span_data.type if span_data else None)

        new_span = create_span(
            name=name,
            span_type=sgp_span_type,
            span_id=openai_span.span_id,
            trace_id=parent_span.trace_id,
            parent_id=parent_span.span_id,
        )
        new_span.start()
        self._spans[openai_span.span_id] = new_span

    def on_span_end(self, openai_span: "OpenAISpan") -> None:
        sgp_span = self._spans.pop(openai_span.span_id, None)
        if sgp_span is None:
            log.warning(f"No existing span found for span_id: {openai_span.span_id}")
            return

        # special case response type, if there are more like this we should change arch to support this
        if isinstance(openai_span.span_data, OpenAIResponseSpanData):
            response = extract_response(openai_span)
            sgp_span.input = {"input": openai_span.span_data.input}
            sgp_span.output = {"output": response.get("output", None) if response else None }
        else:
            sgp_span.output = parse_input_output(openai_span, "output")
            sgp_span.input = parse_input_output(openai_span, "input")

        sgp_span.metadata = parse_metadata(openai_span)

        if openai_span.error:
            sgp_span.set_error(error_message=str(openai_span.error))
        sgp_span.end()

    def shutdown(self) -> None:
        self._queue_manager.shutdown()

    def force_flush(self) -> None:
        flush_queue()
