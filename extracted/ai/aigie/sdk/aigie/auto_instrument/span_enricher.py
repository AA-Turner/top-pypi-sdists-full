"""
Span Enricher — enriches Kytte spans with OTel infrastructure metadata.

Converts OpenTelemetry spans from library instrumentors (psycopg2, redis, httpx, etc.)
into Aigie TRACE_UPDATE events via the shared EventBuffer.

Threading model:
    - on_start() runs in the CALLER thread (where ContextVars are set)
    - export()  runs in BatchSpanProcessor's BACKGROUND thread
    - We capture Aigie parent info in on_start() as span attributes,
      then read them back in export() — no ContextVar access needed at export time.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

if TYPE_CHECKING:
    from ..buffer import EventBuffer

try:
    from opentelemetry.context import Context as _Context
    from opentelemetry.sdk.trace import SpanProcessor as _SpanProcessor
    from opentelemetry.sdk.trace.export import SpanExporter as _SpanExporter
    from opentelemetry.sdk.trace.export import SpanExportResult as _SpanExportResult
except ImportError:
    _Context = Any  # type: ignore[assignment,misc]
    _SpanProcessor = object  # type: ignore[assignment,misc]
    _SpanExporter = object  # type: ignore[assignment,misc]
    _SpanExportResult = None

logger = logging.getLogger(__name__)

# Thread-safe state
_enricher_lock = threading.Lock()
_enricher_buffer: EventBuffer | None = None
_enricher_initialized: bool = False

# Thread-keyed fallback context for frameworks that dispatch to thread pools.
# Keyed by thread ID so concurrent agents in different threads don't collide.
_thread_traces: dict[int, str] = {}  # thread_id -> trace_id
_thread_spans: dict[int, str] = {}  # thread_id -> span_id
_thread_ctx_lock = threading.Lock()

# Internal attribute keys for Aigie context (stripped before sending to backend)
_AIGIE_TRACE_ID = "aigie.trace_id"
_AIGIE_PARENT_ID = "aigie.parent_id"

# OTel semantic convention attribute keys
_DB_SYSTEM = "db.system"
_DB_STATEMENT = "db.statement"
_DB_NAME = "db.name"
_DB_OPERATION = "db.operation"
_HTTP_METHOD = "http.method"
_HTTP_URL = "http.url"
_HTTP_STATUS_CODE = "http.status_code"
_HTTP_TARGET = "http.target"
_NET_PEER_NAME = "net.peer.name"
_NET_PEER_PORT = "net.peer.port"

# Redis-like systems categorized as "cache"
_CACHE_SYSTEMS = frozenset({"redis", "memcached", "valkey"})

# SQL statement truncation limit
_MAX_DB_STATEMENT_LEN = 2000

# Internal SDK paths — calls to these are filtered from customer telemetry
_INTERNAL_PATHS = (
    "/api/v1/ingestion",
    "/api/v1/spans",
    "/api/v1/traces",
    "/api/v1/gateway",
    "/api/v1/health",
    "/api/v1/mode",
)

# Map OTel db.system values to friendly display names
_DB_SYSTEM_NAMES: dict[str, str] = {
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "sqlite": "SQLite",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "memcached": "Memcached",
    "elasticsearch": "Elasticsearch",
    "mssql": "SQL Server",
    "oracle": "Oracle",
    "cassandra": "Cassandra",
}


def _friendly_db_name(db_system: str) -> str:
    """Get a human-friendly name for a database system."""
    return _DB_SYSTEM_NAMES.get(db_system, db_system)


def _infer_span_type(attributes: Mapping[str, Any]) -> str:
    """Map OTel span attributes to an Aigie span type."""
    db_system = attributes.get(_DB_SYSTEM)
    if db_system:
        if db_system in _CACHE_SYSTEMS:
            return "cache"
        return "database"

    if (
        attributes.get(_HTTP_METHOD)
        or attributes.get(_HTTP_URL)
        or attributes.get("http.request.method")
        or attributes.get("url.full")
    ):
        return "http"

    return "tool"


def _extract_metadata(attributes: Mapping[str, Any]) -> dict[str, Any]:
    """Extract relevant OTel attributes into Aigie metadata format."""
    metadata: dict[str, Any] = {"span_source": "otel_bridge"}

    db_system = attributes.get(_DB_SYSTEM)
    if db_system:
        metadata["db.system"] = db_system
        metadata["db.system_name"] = _friendly_db_name(db_system)
        if _DB_STATEMENT in attributes:
            stmt = str(attributes[_DB_STATEMENT])
            metadata["db.statement"] = (
                stmt[:_MAX_DB_STATEMENT_LEN] if len(stmt) > _MAX_DB_STATEMENT_LEN else stmt
            )
        if _DB_NAME in attributes:
            metadata["db.name"] = attributes[_DB_NAME]
        if _DB_OPERATION in attributes:
            metadata["db.operation"] = attributes[_DB_OPERATION]

    http_method = attributes.get(_HTTP_METHOD) or attributes.get("http.request.method")
    if http_method:
        metadata["http.method"] = http_method
    http_url = attributes.get(_HTTP_URL) or attributes.get("url.full")
    if http_url:
        metadata["http.url"] = str(http_url)
    if _HTTP_TARGET in attributes:
        metadata["http.target"] = str(attributes[_HTTP_TARGET])
    http_status = attributes.get(_HTTP_STATUS_CODE) or attributes.get("http.response.status_code")
    if http_status:
        metadata["http.status_code"] = http_status
    peer_name = attributes.get(_NET_PEER_NAME) or attributes.get("server.address")
    if peer_name:
        metadata["http.host"] = peer_name
    peer_port = attributes.get(_NET_PEER_PORT) or attributes.get("server.port")
    if peer_port:
        metadata["net.peer.port"] = peer_port

    return metadata


def _is_internal_sdk_call(attributes: Mapping[str, Any]) -> bool:
    """Check if this HTTP span is an internal Aigie SDK call."""
    url = str(attributes.get(_HTTP_URL, "") or attributes.get("url.full", ""))
    if not url:
        return False
    return any(path in url for path in _INTERNAL_PATHS)



def _get_buffer() -> EventBuffer | None:
    """Lazily get the shared event buffer from the global Aigie instance."""
    global _enricher_buffer
    with _enricher_lock:
        if _enricher_buffer is not None:
            return _enricher_buffer

        try:
            from ..client import _global_aigie

            if _global_aigie and hasattr(_global_aigie, "_buffer") and _global_aigie._buffer:
                _enricher_buffer = _global_aigie._buffer
                return _enricher_buffer
        except ImportError:
            pass

    return None


def _build_call_info(
    span_type: str,
    metadata: dict[str, Any],
    duration_ms: float | None,
    is_error: bool,
) -> dict[str, Any]:
    """Build the per-call summary dict."""
    call_info: dict[str, Any] = {"type": span_type}
    if span_type == "database":
        call_info["db_system"] = metadata.get("db.system", "")
        call_info["db_name"] = metadata.get("db.system_name", "")
        if "db.operation" in metadata:
            call_info["operation"] = metadata["db.operation"]
    elif span_type == "http":
        call_info["method"] = metadata.get("http.method", "")
        call_info["url"] = metadata.get("http.url", "")
        call_info["status"] = metadata.get("http.status_code", "")
        call_info["host"] = metadata.get("http.host", "")
    elif span_type == "cache":
        call_info["system"] = metadata.get("db.system", "")
    if duration_ms is not None:
        call_info["duration_ms"] = duration_ms
    if is_error:
        call_info["error"] = True
    return call_info


def _process_span(otel_span: Any) -> dict[str, Any] | None:
    """Process one OTel span. Returns entry dict or None if span should be skipped."""
    try:
        attrs = dict(otel_span.attributes) if otel_span.attributes else {}

        trace_id = attrs.pop(_AIGIE_TRACE_ID, None)
        parent_id = attrs.pop(_AIGIE_PARENT_ID, None)

        if not trace_id or not parent_id:
            return None
        if parent_id == trace_id:
            return None

        metadata = _extract_metadata(attrs)
        is_internal = _is_internal_sdk_call(attrs)
        if is_internal:
            metadata["internal_sdk_call"] = True

        span_type = _infer_span_type(attrs)

        is_error = False
        if hasattr(otel_span, "status") and otel_span.status:
            try:
                from opentelemetry.trace import StatusCode

                if otel_span.status.status_code == StatusCode.ERROR:
                    is_error = True
                    if otel_span.status.description:
                        metadata["error.message"] = otel_span.status.description
            except ImportError:
                pass

        duration_ms = None
        if otel_span.start_time and otel_span.end_time:
            duration_ms = round((otel_span.end_time - otel_span.start_time) / 1e6, 1)

        key = f"{parent_id}:{trace_id}"
        call_info = _build_call_info(span_type, metadata, duration_ms, is_error)

        return {
            "trace_id": trace_id,
            "parent_id": parent_id,
            "span_type": span_type,
            "call_info": call_info,
            "is_internal": is_internal,
            "metadata": metadata,
            "key": key,
        }
    except Exception:
        logger.debug(
            "Failed to process OTel span: %s",
            getattr(otel_span, "name", "<unknown>"),
            exc_info=True,
        )
        return None


def _build_http_url_list(http_calls: list[dict[str, Any]]) -> list[str]:
    """Build a deduplicated list of HTTP URL labels."""
    url_counts: dict[str, int] = {}
    for c in http_calls:
        method = c.get("method", "")
        url = c.get("url", "")
        if not url:
            continue
        try:
            parsed = urlparse(url)
            short = f"{parsed.netloc}{'/'.join(parsed.path.split('/')[:3])}"
        except Exception:
            short = url[:80]
        label = f"{method} {short}" if method else short
        url_counts[label] = url_counts.get(label, 0) + 1
    return [
        f"{u} (x{n})" if n > 1 else u
        for u, n in sorted(url_counts.items(), key=lambda x: -x[1])
    ]


def _build_db_op_list(db_calls: list[dict[str, Any]]) -> list[str]:
    """Build a deduplicated list of DB operation labels."""
    op_counts: dict[str, int] = {}
    for c in db_calls:
        op = c.get("operation", "")
        db_name = c.get("db_name", "")
        label = f"{op} {db_name}".strip() if op else db_name
        if label:
            op_counts[label] = op_counts.get(label, 0) + 1
    return [
        f"{o} (x{n})" if n > 1 else o
        for o, n in sorted(op_counts.items(), key=lambda x: -x[1])
    ]


def _build_span_summary(infra_calls: list[dict[str, Any]]) -> dict[str, Any]:
    """Build per-span summary dict from a list of infra call_info dicts."""
    summary: dict[str, Any] = {"call_count": len(infra_calls)}
    http_calls = [c for c in infra_calls if c["type"] == "http"]
    db_calls = [c for c in infra_calls if c["type"] == "database"]
    if http_calls:
        summary["http_urls"] = _build_http_url_list(http_calls)
    if db_calls:
        summary["db_operations"] = _build_db_op_list(db_calls)
    dur = sum(c.get("duration_ms", 0) for c in infra_calls if c.get("duration_ms"))
    if dur:
        summary["duration_ms"] = round(dur, 1)
    return summary


def _aggregate_enrichments(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Group _process_span entries into per-trace structure."""
    trace_data: dict[str, dict[str, Any]] = {}

    for entry in entries:
        trace_id = entry["trace_id"]
        parent_id = entry["parent_id"]
        call_info = entry["call_info"]
        is_internal = entry["is_internal"]

        if trace_id not in trace_data:
            trace_data[trace_id] = {"all_infra": [], "all_sdk": [], "infra_by_span": {}}

        if is_internal:
            trace_data[trace_id]["all_sdk"].append(call_info)
        else:
            trace_data[trace_id]["all_infra"].append(call_info)
            if parent_id != trace_id:
                span_key = parent_id[:8]
                existing = trace_data[trace_id]["infra_by_span"].get(span_key)
                if existing is None:
                    trace_data[trace_id]["infra_by_span"][span_key] = [call_info]
                else:
                    existing.append(call_info)

    # Convert accumulated lists to span summaries
    for trace_id in trace_data:
        by_span = trace_data[trace_id]["infra_by_span"]
        trace_data[trace_id]["infra_by_span"] = {
            k: _build_span_summary(v) for k, v in by_span.items()
        }

    return trace_data


def _build_trace_meta(
    infra_calls: list[dict[str, Any]],
    sdk_calls: list[dict[str, Any]],
    infra_by_span: dict[str, Any],
) -> dict[str, Any]:
    """Build the metadata payload for TRACE_UPDATE."""
    trace_meta: dict[str, Any] = {}

    if infra_calls:
        db_calls = [c for c in infra_calls if c["type"] == "database"]
        http_calls = [c for c in infra_calls if c["type"] == "http"]
        cache_calls = [c for c in infra_calls if c["type"] == "cache"]
        trace_meta["infra_call_count"] = len(infra_calls)
        if db_calls:
            trace_meta["infra_db_calls"] = len(db_calls)
            trace_meta["infra_db_systems"] = list(
                {c.get("db_name", "") for c in db_calls if c.get("db_name")}
            )
        if http_calls:
            trace_meta["infra_http_calls"] = len(http_calls)
            hosts = list({c.get("host", "") for c in http_calls if c.get("host")})
            if hosts:
                trace_meta["infra_http_hosts"] = hosts
        if cache_calls:
            trace_meta["infra_cache_calls"] = len(cache_calls)
        infra_total_ms = sum(c.get("duration_ms", 0) for c in infra_calls if c.get("duration_ms"))
        if infra_total_ms:
            trace_meta["infra_duration_ms"] = round(infra_total_ms, 1)
        infra_errors = sum(1 for c in infra_calls if c.get("error"))
        if infra_errors:
            trace_meta["infra_error_count"] = infra_errors

    if sdk_calls:
        sdk_durations = [c["duration_ms"] for c in sdk_calls if c.get("duration_ms")]
        trace_meta["sdk_call_count"] = len(sdk_calls)
        if sdk_durations:
            trace_meta["sdk_total_latency_ms"] = round(sum(sdk_durations), 1)
            trace_meta["sdk_avg_latency_ms"] = round(sum(sdk_durations) / len(sdk_durations), 1)
            trace_meta["sdk_max_latency_ms"] = round(max(sdk_durations), 1)
        sdk_errors = sum(1 for c in sdk_calls if c.get("error"))
        if sdk_errors:
            trace_meta["sdk_error_count"] = sdk_errors

    if infra_by_span:
        trace_meta["infra_by_span"] = infra_by_span

    return trace_meta


def _flush_to_buffer(buffer: EventBuffer, trace_data: dict[str, dict[str, Any]]) -> None:
    """Build trace meta and schedule TRACE_UPDATE events via buffer."""
    from ..buffer import EventType
    from ..utils.safe import schedule_async

    for trace_id, data in trace_data.items():
        try:
            trace_meta = _build_trace_meta(
                data["all_infra"], data["all_sdk"], data["infra_by_span"]
            )
            if trace_meta:
                schedule_async(
                    buffer.add(
                        EventType.TRACE_UPDATE,
                        {"id": trace_id, "trace_id": trace_id, "metadata": trace_meta},
                    )
                )
        except Exception:
            logger.debug("Failed to send trace enrichment for %s", trace_id, exc_info=True)


def _export_otel_spans(otel_spans: Sequence[Any]) -> None:
    """Thin orchestrator: process spans, aggregate, flush to buffer."""
    buffer = _get_buffer()
    if not buffer:
        return
    entries = [e for s in otel_spans if (e := _process_span(s)) is not None]
    if not entries:
        return
    trace_data = _aggregate_enrichments(entries)
    _flush_to_buffer(buffer, trace_data)


def set_active_trace_id(trace_id: str | None, span_id: str | None = None) -> None:
    """Set the trace/span IDs for the current thread.

    Thread-keyed: concurrent agents in different threads won't collide.
    Called by framework auto-instruments when a trace starts.
    """
    tid = threading.get_ident()
    with _thread_ctx_lock:
        if trace_id:
            _thread_traces[tid] = trace_id
        else:
            _thread_traces.pop(tid, None)
        if span_id:
            _thread_spans[tid] = span_id
        else:
            _thread_spans.pop(tid, None)


def set_active_span_id(span_id: str | None) -> None:
    """Update the current span ID for the current thread."""
    tid = threading.get_ident()
    with _thread_ctx_lock:
        if span_id:
            _thread_spans[tid] = span_id
        else:
            _thread_spans.pop(tid, None)


def _find_aigie_context() -> tuple[str | None, str | None]:
    """Try ContextVar chain, fall back to thread-keyed context.

    Returns (trace_id, parent_id).
    """
    trace_id = None
    parent_id = None

    try:
        from ..context_manager import get_current_span_context, get_current_trace_context

        span_ctx = get_current_span_context()
        trace_ctx = get_current_trace_context()

        if span_ctx:
            parent_id = span_ctx.id
            trace_id = span_ctx.metadata.get("trace_id") or (
                trace_ctx.id if trace_ctx else None
            )
        elif trace_ctx:
            trace_id = trace_ctx.id
    except Exception:
        pass

    if not trace_id:
        try:
            from .trace import get_current_trace

            auto_trace = get_current_trace()
            if auto_trace:
                trace_id = getattr(auto_trace, "id", None)
        except Exception:
            pass

    if not trace_id:
        tid = threading.get_ident()
        with _thread_ctx_lock:
            trace_id = _thread_traces.get(tid)

    if not parent_id and trace_id:
        tid = threading.get_ident()
        with _thread_ctx_lock:
            parent_id = _thread_spans.get(tid) or trace_id

    return trace_id, parent_id


class _KytteContextCapture(_SpanProcessor):  # type: ignore[valid-type,misc]
    """Captures Aigie trace/span context at span creation time.

    on_start() runs in the CALLER's thread where ContextVars are set,
    so we can read the current Aigie trace/span and attach the IDs as
    span attributes. The exporter reads these back later from the
    background thread where ContextVars are NOT available.
    """

    def on_start(self, span: Any, parent_context: _Context | None = None) -> None:
        try:
            trace_id, parent_id = _find_aigie_context()
            if not trace_id:
                return

            logger.debug(
                "span_enricher on_start: span=%s trace=%s parent=%s (parent==trace: %s)",
                getattr(span, "name", "?"),
                trace_id[:8] if trace_id else "None",
                parent_id[:8] if parent_id else "None",
                parent_id == trace_id,
            )

            if hasattr(span, "set_attribute"):
                span.set_attribute(_AIGIE_TRACE_ID, trace_id)
                span.set_attribute(_AIGIE_PARENT_ID, parent_id)
        except Exception:
            pass

    def on_end(self, span: Any) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


class _InfraSpanExporter(_SpanExporter):  # type: ignore[valid-type,misc]
    """Exports OTel spans by converting them to Aigie span events."""

    def export(self, spans: Sequence[Any]) -> Any:
        try:
            _export_otel_spans(spans)
            if _SpanExportResult is not None:
                return _SpanExportResult.SUCCESS
            return None
        except Exception:
            logger.debug("_InfraSpanExporter.export failed", exc_info=True)
            if _SpanExportResult is not None:
                return _SpanExportResult.FAILURE
            return None

    def shutdown(self) -> None:
        logger.debug("_InfraSpanExporter shutting down")

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        buf = _get_buffer()
        if buf is not None and hasattr(buf, "flush"):
            from ..utils.safe import schedule_async

            schedule_async(buf.flush())
        return True


def _setup_span_enricher() -> bool:
    """Set up the OTel TracerProvider with the Kytte span enricher.

    Architecture:
        OTel Instrumentor -> TracerProvider -> _KytteContextCapture (on_start: captures
                                              Aigie parent from ContextVars)
                                           -> BatchSpanProcessor -> _InfraSpanExporter
                                                                           |
                                                                   Enrich OTel span
                                                                   into Aigie events
                                                                           |
                                                                   EventBuffer -> Backend

    Installs two components:
    1. _KytteContextCapture — captures Aigie parent context at span start (caller thread)
    2. _InfraSpanExporter   — converts OTel spans to Aigie events at export time (bg thread)

    Returns True if setup succeeded.
    """
    global _enricher_initialized

    with _enricher_lock:
        if _enricher_initialized:
            return True

        try:
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
        except ImportError:
            logger.debug("opentelemetry-sdk not installed, skipping span enricher setup")
            return False

        context_processor = _KytteContextCapture()
        exporter = _InfraSpanExporter()
        batch_processor = BatchSpanProcessor(
            exporter,
            max_queue_size=512,
            max_export_batch_size=64,
            schedule_delay_millis=5000,
        )

        provider = TracerProvider()
        provider.add_span_processor(context_processor)
        provider.add_span_processor(batch_processor)

        from opentelemetry import trace as otel_trace

        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        if provider_type in ("ProxyTracerProvider", "_DefaultTracerProvider"):
            otel_trace.set_tracer_provider(provider)
        elif hasattr(current_provider, "add_span_processor"):
            current_provider.add_span_processor(context_processor)
            current_provider.add_span_processor(batch_processor)
        else:
            logger.debug(
                "Cannot add enricher processors to existing OTel provider (type=%s), skipping",
                provider_type,
            )
            return False

        _enricher_initialized = True
        logger.debug("Span enricher initialized")
        return True


def _teardown_span_enricher() -> None:
    """Reset enricher state so it can be re-initialized after disable_all()."""
    global _enricher_initialized, _enricher_buffer
    with _enricher_lock:
        _enricher_initialized = False
        _enricher_buffer = None
    with _thread_ctx_lock:
        _thread_traces.clear()
        _thread_spans.clear()
