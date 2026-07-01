from __future__ import annotations

import contextlib
import json
import os
import threading
import typing as t
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import IO

from loguru import logger
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

from dreadnode.tracing.constants import (
    AGENT_ATTRIBUTE_SESSION_ID,
    SPAN_ATTRIBUTE_RUN_ID,
    SPAN_ATTRIBUTE_SESSION_ID,
)

TraceBackend = t.Literal["local", "remote"]
"""Controls remote OTLP streaming.

- ``"local"`` — local JSONL only. No OTLP streaming.
- ``"remote"`` — local JSONL and OTLP streaming.
- ``None`` (default) — Auto-detect: stream if credentials exist.

Local JSONL is **always** populated regardless of this setting.
"""

# Default MCP server port - can be overridden via MCP_SERVER_PORT env var
DEFAULT_MCP_PORT = int(os.environ.get("MCP_SERVER_PORT", "8787"))

if t.TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    from opentelemetry.sdk.trace import ReadableSpan

    from dreadnode.storage import Storage

try:
    import websockets
    import websockets.sync.client

    HAS_WEBSOCKETS = True
except ImportError:
    HAS_WEBSOCKETS = False


@dataclass
class TraceExportConfig:
    """Configuration for trace exports to Storage.

    Used by log_artifact() to write artifact metadata to JSONL.
    """

    storage: Storage
    run_id: str
    _artifacts_file: IO[str] | None = field(default=None, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def get_path(self, signal: str, ext: str = "jsonl") -> Path:
        """Get the file path for a specific signal type."""
        return self.storage.trace_path(self.run_id, f"{signal}.{ext}")

    def write_artifact(self, artifact: dict[str, t.Any]) -> None:
        """Write artifact metadata to artifacts.jsonl."""
        with self._lock:
            if self._artifacts_file is None:
                self._artifacts_file = self.get_path("artifacts").open("a")
            self._artifacts_file.write(json.dumps(artifact, default=str) + "\n")
            self._artifacts_file.flush()

    def shutdown(self) -> None:
        """Close any open file handles."""
        with self._lock:
            if self._artifacts_file is not None:
                self._artifacts_file.close()
                self._artifacts_file = None


def span_to_flat_dict(span: ReadableSpan) -> dict:
    """Convert an OTEL ReadableSpan to a flat dict for JSON serialization.

    This is the canonical span serialization used by all local exporters
    (JSONL, WebSocket).
    """
    parent_span_id = None
    if span.parent is not None:
        parent_span_id = format(span.parent.span_id, "016x")

    return {
        "trace_id": format(span.context.trace_id, "032x") if span.context else None,
        "span_id": format(span.context.span_id, "016x") if span.context else None,
        "parent_id": parent_span_id,
        "name": span.name,
        "kind": span.kind.name if span.kind else None,
        "status": span.status.status_code.name if span.status else None,
        "start_time": datetime.fromtimestamp(span.start_time / 1e9, tz=UTC).isoformat()
        if span.start_time
        else None,
        "end_time": datetime.fromtimestamp(span.end_time / 1e9, tz=UTC).isoformat()
        if span.end_time
        else None,
        "attributes": dict(span.attributes) if span.attributes else {},
        "events": [
            {
                "name": e.name,
                "timestamp": datetime.fromtimestamp(e.timestamp / 1e9, tz=UTC).isoformat()
                if e.timestamp
                else None,
                "attributes": dict(e.attributes) if e.attributes else {},
            }
            for e in (span.events or [])
        ],
        "resource": dict(span.resource.attributes) if span.resource else {},
    }


def _get_span_attribute(span: ReadableSpan, key: str) -> str | None:
    """Read a string-valued attribute from a span."""
    if not span.attributes:
        return None
    value = span.attributes.get(key)
    return value if isinstance(value, str) and value else None


class JsonlSpanExporter(SpanExporter):
    """SpanExporter that writes spans to session or run-scoped JSONL files."""

    def __init__(self, storage: Storage) -> None:
        self._storage = storage
        self._files: dict[str, IO[str]] = {}
        self._lock = threading.Lock()

    def _get_span_path(self, span: ReadableSpan) -> Path | None:
        session_id = _get_span_attribute(span, SPAN_ATTRIBUTE_SESSION_ID) or _get_span_attribute(
            span, AGENT_ATTRIBUTE_SESSION_ID
        )
        if session_id is not None:
            return self._storage.session_spans_path(session_id, ext="jsonl")

        run_id = _get_span_attribute(span, SPAN_ATTRIBUTE_RUN_ID)
        if run_id is not None:
            return self._storage.trace_path(run_id, "spans.jsonl")

        return None

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        try:
            with self._lock:
                for span in spans:
                    path = self._get_span_path(span)
                    if path is None:
                        continue

                    path_str = str(path)
                    if path_str not in self._files:
                        self._files[path_str] = path.open("a", encoding="utf-8")

                    self._files[path_str].write(
                        json.dumps(span_to_flat_dict(span), default=str) + "\n"
                    )
                    self._files[path_str].flush()
        except Exception as e:
            logger.debug(f"Failed to export spans to JSONL: {e}")
            return SpanExportResult.FAILURE
        return SpanExportResult.SUCCESS

    def force_flush(self, timeout_millis: int = 30_000) -> bool:  # noqa: ARG002
        return True

    def shutdown(self) -> None:
        with self._lock:
            for file in self._files.values():
                file.close()
            self._files.clear()


class LocalStorageSpanExporter(SpanExporter):
    """SpanExporter that writes spans to local JSONL files."""

    def __init__(self, storage: Storage) -> None:
        self._jsonl_exporter = JsonlSpanExporter(storage)

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        return self._jsonl_exporter.export(spans)

    def force_flush(self, timeout_millis: int = 30_000) -> bool:
        return self._jsonl_exporter.force_flush(timeout_millis)

    def shutdown(self) -> None:
        self._jsonl_exporter.shutdown()


class WebSocketSpanExporter(SpanExporter):
    """SpanExporter that sends spans to dreadnode serve via WebSocket.

    Used by agents to stream spans in real-time to the serve endpoint
    for immediate visibility in Armada.
    """

    def __init__(
        self,
        run_id: str,
        host: str = "127.0.0.1",
        port: int = DEFAULT_MCP_PORT,
        *,
        auto_start: bool = True,
    ):
        """Create a WebSocket span exporter.

        Args:
            run_id: The run identifier.
            host: Server host address.
            port: Server port (default from MCP_SERVER_PORT env var or 8787).
            auto_start: Whether to auto-start the server if not running.
        """
        if not HAS_WEBSOCKETS:
            raise ImportError("websockets package required for WebSocketSpanExporter")

        self.run_id = run_id
        self.url = f"ws://{host}:{port}/ws/spans/{run_id}"
        self.auto_start = auto_start
        self.host = host
        self.port = port
        self._ws: t.Any = None
        self._lock = threading.Lock()

    def _ensure_connection(self) -> bool:
        """Ensure WebSocket connection is established."""
        if self._ws is not None:
            return True

        # Auto-start server if configured
        if self.auto_start:
            from dreadnode.integrations.serve.client import ServeClient

            client = ServeClient(host=self.host, port=self.port)
            if not client.ensure_running():
                logger.warning("Failed to start dreadnode serve")
                return False

        try:
            self._ws = websockets.sync.client.connect(self.url)
        except Exception as e:
            logger.debug(f"Failed to connect to WebSocket: {e}")
            return False
        else:
            return True

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        """Export spans to WebSocket server."""
        with self._lock:
            if not self._ensure_connection():
                return SpanExportResult.FAILURE
            try:
                for span in spans:
                    self._ws.send(json.dumps(span_to_flat_dict(span)))
            except Exception as e:
                logger.debug(f"Failed to export spans via WebSocket: {e}")
                self._ws = None  # Reset connection on failure
                return SpanExportResult.FAILURE
            else:
                return SpanExportResult.SUCCESS

    def force_flush(self, timeout_millis: int = 30_000) -> bool:  # noqa: ARG002
        """Force flush any pending spans."""
        return True

    def shutdown(self) -> None:
        """Close the WebSocket connection."""
        with self._lock:
            if self._ws is not None:
                with contextlib.suppress(Exception):
                    self._ws.close()
                self._ws = None
