"""The server's ingest queue, as a queued write sees it (infra I15d; twin: app/runs/telemetry/ingest_queue).
A queued /metrics or /steps/batch POST asks for an async ack; a close held for queued data is waiting."""

from __future__ import annotations

from typing import Any

#: Sent on a queued metrics or steps-batch POST: the server may answer 202 (durable in its queue,
#: stored later), which deletes the op file as any 2xx does; `finish()` then waits for the store.
ASYNC_ACK_HEADER = "X-Probe-Async-Ack"
#: The server feature that says it gives a 202 only where every close waits for the data.
ASYNC_ACK_FEATURE = "ingest_async_ack"
#: A close's 503 `detail.code` while the run's queued data is not all stored: waiting, not failing.
DATA_PENDING_CODE = "data_pending"


def is_async_ack_declared(client: Any) -> bool | None:
    """What ``client`` already knows of its server's `ASYNC_ACK_FEATURE` (its features cache), or
    None when it never asked. Never asks: a question per drain pass would be a request per pass."""
    cached = getattr(client, "_server_features_cache", None)
    return ASYNC_ACK_FEATURE in cached if isinstance(cached, frozenset) else None


def get_async_ack_headers(client: Any) -> dict[str, str] | None:
    """The header for a queued telemetry POST through ``client``: sent unless the client knows its
    server does not declare `ASYNC_ACK_FEATURE`. A server without the ingest queue ignores it, and
    only one with the queue (whose closes wait for the data, I15d) answers 202."""
    return None if is_async_ack_declared(client) is False else {ASYNC_ACK_HEADER: "1"}


def build_async_ack_kwargs(client: Any) -> dict[str, Any]:
    """`get_async_ack_headers` as `transport.request` keyword arguments: none at all when the header
    is not sent, so a transport that takes no `extra_headers` (an injected one) is called as before."""
    headers = get_async_ack_headers(client)
    return {} if headers is None else {"extra_headers": headers}


def get_data_pending_points(exc: BaseException) -> int | None:
    """The run's pending points when ``exc`` is a close the server held for its queued data (503
    `data_pending`), else None."""
    detail = getattr(exc, "detail", None)
    if getattr(exc, "status", None) != 503 or not isinstance(detail, dict):
        return None
    if detail.get("code") != DATA_PENDING_CODE:
        return None
    points = detail.get("pending_points")
    return points if isinstance(points, int) and points >= 0 else 0
