"""Get Session Trajectory"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionTrajectory


def _build_request_args(
    public_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{public_id}/trajectory"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    public_id: str,
    x_api_key: str | None = None,
) -> SessionTrajectory:
    """Return live ATIF trajectory from OTel spans received so far.

    Loads all spans (up to MAX_BATCHES cap) without offset/limit because
    spans_to_trajectories needs the full span tree (root world spans, agent
    spans, etc.) to construct the trajectory correctly."""

    request_args = _build_request_args(
        public_id=public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionTrajectory.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    x_api_key: str | None = None,
) -> SessionTrajectory:
    """Return live ATIF trajectory from OTel spans received so far.

    Loads all spans (up to MAX_BATCHES cap) without offset/limit because
    spans_to_trajectories needs the full span tree (root world spans, agent
    spans, etc.) to construct the trajectory correctly."""

    request_args = _build_request_args(
        public_id=public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionTrajectory.model_validate(response.json())
