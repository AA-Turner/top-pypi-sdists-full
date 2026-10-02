"""Tracing processor for OpenAI Agents SDK integration with Bitfab."""

from __future__ import annotations

import contextlib
import logging
import uuid
from typing import TYPE_CHECKING, Any, Callable, TypedDict

from bitfab import subtree
from bitfab.constants import DEFAULT_SERVICE_URL
from bitfab.http import HttpClient
from bitfab.processor_payload import finalize_span_payload, finalize_trace_payload
from bitfab.serialize import to_json_safe
from bitfab.span_origin import make_span_origin

if TYPE_CHECKING:
    from agents import Span, Trace, TracingProcessor
else:
    try:
        from agents import TracingProcessor
    except ImportError:
        TracingProcessor = object

logger = logging.getLogger(__name__)


class ActiveSpanContext(TypedDict):
    trace_id: str
    span_id: str


class BitfabOpenAITracingProcessor(TracingProcessor):
    """Tracing processor for OpenAI Agents SDK that sends traces to Bitfab.

    This processor captures traces and spans from the OpenAI Agents SDK and sends
    them to the Bitfab API for storage and analysis.

    Args:
        api_key: Bitfab API key for authentication
        service_url: Base URL for the Bitfab service (default: https://bitfab.ai)
    """

    def __init__(
        self,
        api_key: str,
        service_url: str | None = None,
        get_active_span_context: Callable[[], ActiveSpanContext | None] | None = None,
        *,
        _http_client: HttpClient | None = None,
        _should_record: Callable[[], bool] | None = None,
    ):
        """Initialize the Bitfab tracing processor.

        Args:
            api_key: Bitfab API key
            service_url: Base URL for Bitfab service (default: production URL)
            get_active_span_context: Optional callback that returns the active
                withSpan context or ``None``. Used to link OpenAI traces into
                an existing withSpan trace.
        """
        self._owns_http_client = _http_client is None
        self._http_client = _http_client or HttpClient(
            api_key=api_key, service_url=service_url or DEFAULT_SERVICE_URL
        )
        self._active_traces: dict[str, Trace] = {}
        self._active_spans: dict[str, Span] = {}
        self._ended_traces: set[str] = set()
        self._get_active_span_context = get_active_span_context
        self._should_record = _should_record or (
            lambda: (self._http_client._resolve_api_key() or "").strip() != ""
        )
        self._active_span_mappings: dict[str, ActiveSpanContext] = {}
        self._canonical_trace_ids: dict[str, str] = {}
        self._subtree_entries: dict[str, Any] = {}

    def _get_canonical_trace_id(self, source_trace_id: str) -> str:
        existing = self._canonical_trace_ids.get(source_trace_id)
        if existing is not None:
            return existing

        created = str(uuid.uuid4())
        self._canonical_trace_ids[source_trace_id] = created
        return created

    @property
    def api_key(self) -> str:
        """Get the API key."""
        return self._http_client._resolve_api_key() or ""

    @property
    def service_url(self) -> str:
        """Get the service URL."""
        return self._http_client.service_url

    def on_trace_start(self, trace: Trace) -> None:
        """Called when a trace starts.

        If there's an active withSpan context, the trace ID is remapped to the
        outer trace and sent to pre-create the external_traces row on the server.

        Args:
            trace: The trace that started
        """
        try:
            self._active_traces[trace.trace_id] = trace

            active_context = (
                self._get_active_span_context()
                if self._get_active_span_context is not None
                else None
            )
            if active_context is not None:
                self._active_span_mappings[trace.trace_id] = active_context

            canonical_trace_id = (
                active_context["trace_id"]
                if active_context is not None
                else self._get_canonical_trace_id(trace.trace_id)
            )
            self._canonical_trace_ids[trace.trace_id] = canonical_trace_id
            self._http_client.trace_completion.hold(
                active_context["trace_id"] if active_context else trace.trace_id,
                f"openai:{trace.trace_id}",
            )

            self._send_external_trace(
                trace,
                canonical_trace_id=canonical_trace_id,
                source_trace_id_override=(
                    active_context["trace_id"] if active_context else None
                ),
            )
        except Exception:
            pass

    def on_trace_end(self, trace: Trace) -> None:
        """Called when a trace ends.

        If mapped to a withSpan trace, sends with remapped ID and completed=False
        since the parent withSpan handles completion.

        Args:
            trace: The trace that ended
        """
        try:
            mapping = self._active_span_mappings.get(trace.trace_id)

            self._send_external_trace(
                trace,
                completed=mapping is None,
                canonical_trace_id=(
                    mapping["trace_id"]
                    if mapping is not None
                    else self._get_canonical_trace_id(trace.trace_id)
                ),
                source_trace_id_override=(mapping["trace_id"] if mapping else None),
            )

            self._ended_traces.add(trace.trace_id)
            self._http_client.trace_completion.end(
                mapping["trace_id"] if mapping else trace.trace_id,
                f"openai:{trace.trace_id}",
            )
            self._cleanup_trace(trace.trace_id)
        except Exception:
            pass

    def _cleanup_trace(self, trace_id: str) -> None:
        if trace_id not in self._ended_traces or any(
            span.trace_id == trace_id for span in self._active_spans.values()
        ):
            return
        self._ended_traces.discard(trace_id)
        self._active_span_mappings.pop(trace_id, None)
        self._canonical_trace_ids.pop(trace_id, None)
        self._active_traces.pop(trace_id, None)

    def on_span_start(self, span: Span) -> None:
        """Called when a span starts.

        Args:
            span: The span that started
        """
        with contextlib.suppress(Exception):
            self._active_spans[span.span_id] = span
            mapping = self._active_span_mappings.get(span.trace_id)
            trace_id = mapping["trace_id"] if mapping else span.trace_id
            self._http_client.trace_completion.start(trace_id, span.span_id)
            if mapping is not None and self._should_record():
                entry = subtree.enter_framework_span(mapping["trace_id"], span.span_id)
                if entry is not None:
                    self._subtree_entries[span.span_id] = entry

    def on_span_end(self, span: Span) -> None:
        """Called when a span ends.

        Args:
            span: The span that ended
        """
        with contextlib.suppress(Exception):
            entry = self._subtree_entries.pop(span.span_id, None)
            if entry is not None:
                subtree.exit_framework_span(entry)
        try:
            mapping = self._active_span_mappings.get(span.trace_id)
            trace_id = mapping["trace_id"] if mapping else span.trace_id
            try:
                self._send_external_span(span)
            finally:
                self._http_client.trace_completion.end(trace_id, span.span_id)
                self._active_spans.pop(span.span_id, None)
                self._cleanup_trace(span.trace_id)
        except Exception:
            pass

    def _send_external_trace(
        self,
        trace: Trace,
        completed: bool = False,
        canonical_trace_id: str | None = None,
        source_trace_id_override: str | None = None,
    ) -> None:
        """Send external trace to Bitfab API (fire-and-forget).

        When trace_id_override is provided, the trace ID is remapped to link
        the OpenAI trace into an outer withSpan trace.

        Args:
            trace: The trace to send
            completed: If True, marks the trace as completed
            canonical_trace_id: Internal trace ID requested from Bitfab
            source_trace_id_override: If set, overrides the external trace ID
        """
        if not self._should_record():
            return
        try:
            external_trace = trace.export()
            if source_trace_id_override is not None:
                external_trace["id"] = source_trace_id_override

            trace_data: dict[str, Any] = {
                "type": "openai",
                "source": "python-sdk-openai-tracing",
                "externalTrace": external_trace,
                "completed": completed,
            }
            if canonical_trace_id is not None:
                trace_data["id"] = canonical_trace_id

            # Sanitize the whole payload (not just input/response) so a
            # non-serializable value anywhere in the export (e.g. a model in
            # trace metadata) is recursed/dumped rather than dropping the entire
            # trace, warning when the capture was lossy. The HTTP boundary stays
            # as the final net. Mirrors the TypeScript processor (no pre-gate).
            trace_data = finalize_trace_payload(trace_data, logger)

            self._http_client.send_external_trace(trace_data)
        except Exception as e:
            logger.error(f"Failed to send external trace to Bitfab: {e}", exc_info=True)

    def _serialize_value(self, value: Any) -> Any:
        """Serialize a value to a JSON-serializable format.

        Delegates to the shared ``to_json_safe`` so the recurse-the-dump logic
        lives in exactly one place (see bitfab/serialize.py)."""
        return to_json_safe(value)

    def _export_span(self, span: Span, errors: list[dict[str, str]]) -> dict[str, Any]:
        """Export span to dict, collecting any errors."""
        try:
            serialized_span = span.export()
            if not isinstance(serialized_span, dict):
                errors.append(
                    {
                        "step": "span.export()",
                        "error": f"Returned non-dict type: {type(serialized_span)}",
                    }
                )
                serialized_span = {}
        except Exception as e:
            errors.append({"step": "span.export()", "error": str(e)})
            serialized_span = {}

        if "span_data" not in serialized_span:
            serialized_span["span_data"] = {}

        return serialized_span

    def _extract_span_input_response(
        self,
        span: Span,
        serialized_span: dict[str, Any],
    ) -> None:
        """Pull input/response onto a response span's serialized payload.

        Only ``ResponseSpanData`` drops its content from ``export()`` (which emits
        just ``response_id``/``usage``), so we recover ``input``/``response`` from
        the live span_data. Every other span type (function, agent, custom, and
        the newer task/turn spans) already carries its data via ``export()``, so
        writing here would clobber a real input with an empty ``[]`` or stamp a
        spurious ``response: None``. Gate strictly to response spans, and only set
        a field when a value is actually present.

        Assign the raw values: sanitization (and lossy-capture reporting) happens
        once in ``finalize_span_payload``. Pre-stubbing input/response here would
        turn a lossy value into a plain placeholder string before the reporting
        pass runs, so its loss would never be marked non-replayable. This runs at
        span end (send time), so there is no snapshot window to guard against."""
        if getattr(span.span_data, "type", None) != "response":
            return

        input_value = getattr(span.span_data, "input", None)
        if input_value is not None:
            serialized_span["span_data"]["input"] = input_value

        response_value = getattr(span.span_data, "response", None)
        if response_value is not None:
            serialized_span["span_data"]["response"] = response_value

    def _apply_span_overrides(
        self, serialized_span: dict[str, Any], trace_id: str
    ) -> None:
        """If the span's trace is mapped to a withSpan trace, rewrite trace_id and parent_id."""
        mapping = self._active_span_mappings.get(trace_id)
        if mapping is not None:
            serialized_span["trace_id"] = mapping["trace_id"]
            if not serialized_span.get("parent_id"):
                serialized_span["parent_id"] = mapping["span_id"]

    def _build_span_payload(
        self,
        serialized_span: dict[str, Any],
        errors: list[dict[str, str]],
    ) -> dict[str, Any]:
        """Build the span payload, sanitizing the whole span for JSON safety.

        Runs the entire payload through ``finalize_span_payload`` so a
        non-serializable value in any span_data field (output, model_config,
        tools, ...) is recursed/dumped rather than gutting the span down to
        id + trace_id, and a lossy capture is marked rather than shipped
        silently. The HTTP boundary stays as the final net. Mirrors the
        TypeScript processor, which has no destructive pre-gate."""
        serialized_span["span_origin"] = make_span_origin("openai-agents")
        span_data: dict[str, Any] = {
            "id": str(uuid.uuid4()),
            "type": "openai",
            "source": "python-sdk-openai-tracing",
            "sourceTraceId": serialized_span.get("trace_id", "unknown"),
            "rawSpan": serialized_span,
        }

        if errors:
            span_data["errors"] = errors

        return finalize_span_payload(span_data)

    def _send_external_span(self, span: Span) -> None:
        """Send external span to Bitfab API (fire-and-forget).

        If the span belongs to a trace mapped to a withSpan trace, the trace_id
        and parent_id are rewritten to link the span into the withSpan tree.

        Args:
            span: The span to send
        """
        if not self._should_record():
            return
        errors: list[dict[str, str]] = []
        serialized_span = self._export_span(span, errors)
        self._extract_span_input_response(span, serialized_span)
        self._apply_span_overrides(serialized_span, span.trace_id)

        span_payload = self._build_span_payload(serialized_span, errors)
        span_payload["traceId"] = self._get_canonical_trace_id(span.trace_id)

        try:
            self._http_client.send_external_span(span_payload)
        except Exception as e:
            logger.error(f"Failed to send external span to Bitfab: {e}", exc_info=True)

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Force flush any buffered traces/spans.

        Args:
            timeout_millis: Maximum time to wait for flush in milliseconds

        Returns:
            True if flush succeeded, False otherwise
        """
        return self._http_client.wait_for_pending_requests(
            timeout=max(timeout_millis, 0) / 1000
        )

    def shutdown(self, timeout_millis: int = 30000) -> bool:
        """Shutdown the tracing processor.

        Args:
            timeout_millis: Maximum time to wait for shutdown in milliseconds

        Returns:
            True if shutdown succeeded, False otherwise
        """
        try:
            if self._owns_http_client:
                return self._http_client.close(max(timeout_millis, 0) / 1000)
            return self.force_flush(timeout_millis)
        finally:
            self._active_traces.clear()
            self._active_spans.clear()
            self._active_span_mappings.clear()
            self._canonical_trace_ids.clear()
            self._subtree_entries.clear()

    def __enter__(self) -> BitfabOpenAITracingProcessor:
        """Enter context manager."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager and shutdown."""
        self.shutdown()
