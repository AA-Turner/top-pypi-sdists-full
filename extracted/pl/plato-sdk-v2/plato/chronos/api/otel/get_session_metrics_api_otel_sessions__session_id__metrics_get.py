"""Get Session Metrics"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    session_id: str,
    env_alias: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/otel/sessions/{session_id}/metrics"

    params: dict[str, Any] = {}
    if env_alias is not None:
        params["env_alias"] = env_alias

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    session_id: str,
    env_alias: str | None = None,
) -> dict[str, Any]:
    """Get stored OTLP metrics for a session.

    Returns raw metric data points, optionally filtered by env_alias."""

    request_args = _build_request_args(
        session_id=session_id,
        env_alias=env_alias,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    env_alias: str | None = None,
) -> dict[str, Any]:
    """Get stored OTLP metrics for a session.

    Returns raw metric data points, optionally filtered by env_alias."""

    request_args = _build_request_args(
        session_id=session_id,
        env_alias=env_alias,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
