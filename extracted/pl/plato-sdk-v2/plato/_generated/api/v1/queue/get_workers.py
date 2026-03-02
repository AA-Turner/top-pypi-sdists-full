"""Get Workers"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import WorkerStatus


def _build_request_args(
    state: str | None = None,
    stale_only: bool | None = False,
    stale_threshold_seconds: int | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/queue/workers"

    params: dict[str, Any] = {}
    if state is not None:
        params["state"] = state
    if stale_only is not None:
        params["stale_only"] = stale_only
    if stale_threshold_seconds is not None:
        params["stale_threshold_seconds"] = stale_threshold_seconds

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    state: str | None = None,
    stale_only: bool | None = False,
    stale_threshold_seconds: int | None = None,
) -> list[WorkerStatus]:
    """Get list of workers/dispatchers with optional filtering.

    Args:
        state: Filter by worker state
        stale_only: Only return workers with stale heartbeats
        stale_threshold_seconds: Threshold for considering a heartbeat stale (defaults to worker_heartbeat_timeout from settings)

    Returns:
        List of worker status objects matching the filters"""

    request_args = _build_request_args(
        state=state,
        stale_only=stale_only,
        stale_threshold_seconds=stale_threshold_seconds,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    state: str | None = None,
    stale_only: bool | None = False,
    stale_threshold_seconds: int | None = None,
) -> list[WorkerStatus]:
    """Get list of workers/dispatchers with optional filtering.

    Args:
        state: Filter by worker state
        stale_only: Only return workers with stale heartbeats
        stale_threshold_seconds: Threshold for considering a heartbeat stale (defaults to worker_heartbeat_timeout from settings)

    Returns:
        List of worker status objects matching the filters"""

    request_args = _build_request_args(
        state=state,
        stale_only=stale_only,
        stale_threshold_seconds=stale_threshold_seconds,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
