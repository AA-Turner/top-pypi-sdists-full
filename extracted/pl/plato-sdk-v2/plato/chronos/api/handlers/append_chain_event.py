"""Append Chain Event"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import ChainEventResponse, CreateChainEventBody


def _build_request_args(
    chain_id: str,
    body: CreateChainEventBody,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/handlers/chains/{chain_id}/events"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    chain_id: str,
    body: CreateChainEventBody,
    x_api_key: str | None = None,
) -> ChainEventResponse:
    """Append one event to a chain's log.

    This is the door for chain state that comes from OUTSIDE the flow: an
    external system (e.g. an exploration graph) pushes its current ref here
    whenever it advances, and readers derive "the latest X" from the newest
    event of that type. Append-only, so external writers and the flow's own
    ``chain_metadata`` propagation can never clobber each other.

    Deliberately open to any authenticated principal in the org, unlike the
    admin-only mutations on this router: the intended writers are external
    services holding an org API key, appending executes no code, and — unlike
    archiving — it hides nothing from anyone. The log is unbounded in count;
    only the per-event payload size is capped (16 KiB, in the body model)."""

    request_args = _build_request_args(
        chain_id=chain_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ChainEventResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    chain_id: str,
    body: CreateChainEventBody,
    x_api_key: str | None = None,
) -> ChainEventResponse:
    """Append one event to a chain's log.

    This is the door for chain state that comes from OUTSIDE the flow: an
    external system (e.g. an exploration graph) pushes its current ref here
    whenever it advances, and readers derive "the latest X" from the newest
    event of that type. Append-only, so external writers and the flow's own
    ``chain_metadata`` propagation can never clobber each other.

    Deliberately open to any authenticated principal in the org, unlike the
    admin-only mutations on this router: the intended writers are external
    services holding an org API key, appending executes no code, and — unlike
    archiving — it hides nothing from anyone. The log is unbounded in count;
    only the per-event payload size is capped (16 KiB, in the body model)."""

    request_args = _build_request_args(
        chain_id=chain_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ChainEventResponse.model_validate(response.json())
