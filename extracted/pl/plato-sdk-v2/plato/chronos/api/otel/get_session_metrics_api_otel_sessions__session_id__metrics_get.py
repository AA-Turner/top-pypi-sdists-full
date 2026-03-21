"""Get Session Metrics"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionMetricsResponse


def _build_request_args(
    session_id: str,
    env_alias: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/otel/sessions/{session_id}/metrics"

    params: dict[str, Any] = {}
    if env_alias is not None:
        params["env_alias"] = env_alias

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
    x_api_key: str | None = None,
) -> SessionMetricsResponse:
    """Get stored OTLP metrics for a session.

    Returns raw metric data points, optionally filtered by env_alias."""

    request_args = _build_request_args(
        session_id=session_id,
        env_alias=env_alias,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionMetricsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    env_alias: str | None = None,
    x_api_key: str | None = None,
) -> SessionMetricsResponse:
    """Get stored OTLP metrics for a session.

    Returns raw metric data points, optionally filtered by env_alias."""

    request_args = _build_request_args(
        session_id=session_id,
        env_alias=env_alias,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionMetricsResponse.model_validate(response.json())
