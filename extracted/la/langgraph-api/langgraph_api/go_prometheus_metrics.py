"""Merge Go core Prometheus text into the Python /metrics scrape.

In multi-process mode, queue depth / workers / run lifecycle counters live in
the Go core-server registry. Scrapers always hit Python :8000/metrics; those
handlers call ``merge_go_prometheus_text``, which fetches the registry over the
existing core gRPC channel (same path as PoolStats).

Go's ``PrometheusMetrics`` RPC dumps the isPublic registry only — trust that
filter. ``EXPOSE_INTERNAL_METRICS_PROMETHEUS`` still gates Python's own scrape
partition; wiring it through to also dump Go internals is a follow-up on the
Go side.
"""

from __future__ import annotations

import structlog
from google.protobuf.empty_pb2 import Empty  # ty: ignore[unresolved-import]

from langgraph_api import config

logger = structlog.stdlib.get_logger(__name__)


async def fetch_go_prometheus_text() -> bytes | None:
    """Fetch Go Prometheus exposition text via gRPC, or None on any failure."""
    try:
        from langgraph_api.grpc.client import get_shared_client  # noqa: PLC0415

        client = await get_shared_client()
        response = await client.runs.PrometheusMetrics(Empty())
        body = response.body
        return bytes(body) if body else None
    except Exception as exc:
        await logger.awarning(
            "Failed to fetch Go Prometheus metrics for /metrics merge",
            exc_info=exc,
        )
        return None


async def merge_go_prometheus_text(python_body: bytes) -> bytes:
    """Append Go public registry text when multi-process; else python_body."""
    if config.DISPATCH_MODE != config.DispatchMode.MULTI_PROCESS:
        return python_body

    go_body = await fetch_go_prometheus_text()
    if not go_body:
        return python_body

    if python_body and not python_body.endswith(b"\n"):
        python_body += b"\n"
    return python_body + go_body
