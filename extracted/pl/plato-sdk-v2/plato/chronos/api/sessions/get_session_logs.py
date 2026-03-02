"""Get Session Logs"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionLogsResponse


def _build_request_args(
    public_id: str,
    limit: int | None = 10000,
    cursor: str | None = None,
    offset: int | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{public_id}/logs"

    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if cursor is not None:
        params["cursor"] = cursor
    if offset is not None:
        params["offset"] = offset

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    public_id: str,
    limit: int | None = 10000,
    cursor: str | None = None,
    offset: int | None = None,
    x_api_key: str | None = None,
) -> SessionLogsResponse:
    """Get logs/events for a session with cursor-based pagination.

    Pass the cursor from the previous response to load the next page.
    On the first call, omit cursor to load from the beginning."""

    request_args = _build_request_args(
        public_id=public_id,
        limit=limit,
        cursor=cursor,
        offset=offset,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionLogsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    limit: int | None = 10000,
    cursor: str | None = None,
    offset: int | None = None,
    x_api_key: str | None = None,
) -> SessionLogsResponse:
    """Get logs/events for a session with cursor-based pagination.

    Pass the cursor from the previous response to load the next page.
    On the first call, omit cursor to load from the beginning."""

    request_args = _build_request_args(
        public_id=public_id,
        limit=limit,
        cursor=cursor,
        offset=offset,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionLogsResponse.model_validate(response.json())
