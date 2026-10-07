"""List Chain Events"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import ChainEventListResponse


def _build_request_args(
    chain_id: str,
    event_type: str | None = None,
    latest_per_type: bool | None = False,
    limit: int | None = 100,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/handlers/chains/{chain_id}/events"

    params: dict[str, Any] = {}
    if event_type is not None:
        params["event_type"] = event_type
    if latest_per_type is not None:
        params["latest_per_type"] = latest_per_type
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
    chain_id: str,
    event_type: str | None = None,
    latest_per_type: bool | None = False,
    limit: int | None = 100,
    x_api_key: str | None = None,
) -> ChainEventListResponse:
    """A chain's event log, newest first, with the total count alongside.

    "The current X" reads: ``event_type=X&limit=1`` for one type, or
    ``latest_per_type=true`` for every type's newest event at once —
    computed server-side so it stays correct however deep the log grows
    (``latest_per_type`` ignores ``event_type`` and ``limit``). ``limit`` is
    deliberately unclamped: the log itself is unbounded, so the whole of it
    must be readable. A chain with no events reads as empty rather than 404,
    like the chain view — the org scope already guarantees you only see your
    own."""

    request_args = _build_request_args(
        chain_id=chain_id,
        event_type=event_type,
        latest_per_type=latest_per_type,
        limit=limit,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ChainEventListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    chain_id: str,
    event_type: str | None = None,
    latest_per_type: bool | None = False,
    limit: int | None = 100,
    x_api_key: str | None = None,
) -> ChainEventListResponse:
    """A chain's event log, newest first, with the total count alongside.

    "The current X" reads: ``event_type=X&limit=1`` for one type, or
    ``latest_per_type=true`` for every type's newest event at once —
    computed server-side so it stays correct however deep the log grows
    (``latest_per_type`` ignores ``event_type`` and ``limit``). ``limit`` is
    deliberately unclamped: the log itself is unbounded, so the whole of it
    must be readable. A chain with no events reads as empty rather than 404,
    like the chain view — the org scope already guarantees you only see your
    own."""

    request_args = _build_request_args(
        chain_id=chain_id,
        event_type=event_type,
        latest_per_type=latest_per_type,
        limit=limit,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ChainEventListResponse.model_validate(response.json())
