"""Get Session Traces"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import OTelTraceResponse


def _build_request_args(
    session_id: str,
    limit: int | None = 10000,
    cursor: str | None = None,
    offset: int | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/otel/sessions/{session_id}/traces"

    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if cursor is not None:
        params["cursor"] = cursor
    if offset is not None:
        params["offset"] = offset

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    session_id: str,
    limit: int | None = 10000,
    cursor: str | None = None,
    offset: int | None = None,
) -> OTelTraceResponse:
    """Get parsed traces for a session with cursor-based pagination.

    Returns spans parsed from stored OTLP batches, suitable for UI rendering."""

    request_args = _build_request_args(
        session_id=session_id,
        limit=limit,
        cursor=cursor,
        offset=offset,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return OTelTraceResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    limit: int | None = 10000,
    cursor: str | None = None,
    offset: int | None = None,
) -> OTelTraceResponse:
    """Get parsed traces for a session with cursor-based pagination.

    Returns spans parsed from stored OTLP batches, suitable for UI rendering."""

    request_args = _build_request_args(
        session_id=session_id,
        limit=limit,
        cursor=cursor,
        offset=offset,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return OTelTraceResponse.model_validate(response.json())
