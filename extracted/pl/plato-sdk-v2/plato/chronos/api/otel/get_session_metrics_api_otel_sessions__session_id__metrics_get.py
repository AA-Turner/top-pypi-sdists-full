"""Get Session Metrics"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionMetricsResponse


def _build_request_args(
    session_id: str,
    env_alias: str | None = None,
    cursor: str | None = None,
    limit: int | None = 100,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/otel/sessions/{session_id}/metrics"

    params: dict[str, Any] = {}
    if env_alias is not None:
        params["env_alias"] = env_alias
    if cursor is not None:
        params["cursor"] = cursor
    if limit is not None:
        params["limit"] = limit

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
    session_id: str,
    env_alias: str | None = None,
    cursor: str | None = None,
    limit: int | None = 100,
    x_api_key: str | None = None,
) -> SessionMetricsResponse:
    """Get stored OTLP metrics for a session.

    Returns raw metric data points, optionally filtered by env_alias.
    Uses cursor-based pagination over metric batches to avoid loading
    all data into memory at once."""

    request_args = _build_request_args(
        session_id=session_id,
        env_alias=env_alias,
        cursor=cursor,
        limit=limit,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionMetricsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    env_alias: str | None = None,
    cursor: str | None = None,
    limit: int | None = 100,
    x_api_key: str | None = None,
) -> SessionMetricsResponse:
    """Get stored OTLP metrics for a session.

    Returns raw metric data points, optionally filtered by env_alias.
    Uses cursor-based pagination over metric batches to avoid loading
    all data into memory at once."""

    request_args = _build_request_args(
        session_id=session_id,
        env_alias=env_alias,
        cursor=cursor,
        limit=limit,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionMetricsResponse.model_validate(response.json())
