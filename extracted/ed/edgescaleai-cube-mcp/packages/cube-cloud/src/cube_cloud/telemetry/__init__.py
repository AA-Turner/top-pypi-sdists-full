"""Tool-call analytics telemetry.

`record_tool_call` is the single seam invoked from the cube-cloud `call_tool`
wrapper. It builds the canonical event and fans it out to the configured sinks.
It is guaranteed non-blocking and never-raising: telemetry must never break or
alter a tool call. Sinks:

  - S3 archive (durable analytics system of record) — always, when configured.
  - Groundcover OTLP spans (hot/correlation tier) — wired in a later slice.

Console requests are recorded through the same sinks by `console_events.py`
(imported directly by `main.py`, not re-exported here) under `source="console"`.
"""

from __future__ import annotations

import logging
from typing import Any

from cube_cloud.config import settings
from cube_cloud.telemetry import archive, otlp
from cube_cloud.telemetry.events import ToolCallEvent, build_event

logger = logging.getLogger(__name__)

__all__ = ["record_tool_call", "build_event", "ToolCallEvent"]


def record_tool_call(
    req: Any,
    name: str,
    arguments: dict[str, Any],
    result: str,
    latency_ms: float,
    exception: BaseException | None = None,
) -> None:
    """Build and emit the tool-call event. Never raises."""
    if not settings.telemetry_enabled:
        return
    try:
        event = build_event(req, name, arguments, result, latency_ms, exception)
        # OTLP first so the span's trace_id is stamped onto the event before the
        # S3 record is written — links the durable row to the Groundcover trace.
        otlp.emit_span(event)
        archive.emit(event)
    except BaseException:
        # Airtight: telemetry is invoked from the tool wrapper's `finally`, so an
        # escaping error here would replace the in-flight tool exception. Swallow
        # everything (including non-Exception BaseExceptions) and only log.
        logger.exception("telemetry: record_tool_call failed (swallowed)")
