"""List Handler Chains"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import ChainListResponse


def _build_request_args(
    limit: int | None = 200,
    offset: int | None = None,
    archived: str | None = "exclude",
    tag: list[str] | None = None,
    tags_mode: str | None = "or",
    q: str | None = None,
    sim: str | None = None,
    failed_only: bool | None = False,
    kind: str | None = None,
    handler: str | None = None,
    sort: str | None = "last_activity",
    order: str | None = "desc",
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/handlers/chains"

    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if archived is not None:
        params["archived"] = archived
    if tag is not None:
        params["tag"] = tag
    if tags_mode is not None:
        params["tags_mode"] = tags_mode
    if q is not None:
        params["q"] = q
    if sim is not None:
        params["sim"] = sim
    if failed_only is not None:
        params["failed_only"] = failed_only
    if kind is not None:
        params["kind"] = kind
    if handler is not None:
        params["handler"] = handler
    if sort is not None:
        params["sort"] = sort
    if order is not None:
        params["order"] = order

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
    limit: int | None = 200,
    offset: int | None = None,
    archived: str | None = "exclude",
    tag: list[str] | None = None,
    tags_mode: str | None = "or",
    q: str | None = None,
    sim: str | None = None,
    failed_only: bool | None = False,
    kind: str | None = None,
    handler: str | None = None,
    sort: str | None = "last_activity",
    order: str | None = "desc",
    x_api_key: str | None = None,
) -> ChainListResponse:
    """List the org's chains, aggregated across sessions/assignments/invocations,
    most recently active first, one ``limit``/``offset`` page at a time.

    Every filter is applied here rather than in the client, for the same
    reason: they decide which chains are candidates at all, so they have to
    run BEFORE the page is cut. A client-side filter silently misses any
    matching chain outside the loaded page, which looks identical to "no such
    chain".

    ``tag`` is repeatable; ``tags_mode`` selects ANY (default) or ALL, the same
    contract as the sessions list. Tags go through the service-wide
    ``normalize_tag`` on both write and query, so no chain-specific matching
    exists here."""

    request_args = _build_request_args(
        limit=limit,
        offset=offset,
        archived=archived,
        tag=tag,
        tags_mode=tags_mode,
        q=q,
        sim=sim,
        failed_only=failed_only,
        kind=kind,
        handler=handler,
        sort=sort,
        order=order,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ChainListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    limit: int | None = 200,
    offset: int | None = None,
    archived: str | None = "exclude",
    tag: list[str] | None = None,
    tags_mode: str | None = "or",
    q: str | None = None,
    sim: str | None = None,
    failed_only: bool | None = False,
    kind: str | None = None,
    handler: str | None = None,
    sort: str | None = "last_activity",
    order: str | None = "desc",
    x_api_key: str | None = None,
) -> ChainListResponse:
    """List the org's chains, aggregated across sessions/assignments/invocations,
    most recently active first, one ``limit``/``offset`` page at a time.

    Every filter is applied here rather than in the client, for the same
    reason: they decide which chains are candidates at all, so they have to
    run BEFORE the page is cut. A client-side filter silently misses any
    matching chain outside the loaded page, which looks identical to "no such
    chain".

    ``tag`` is repeatable; ``tags_mode`` selects ANY (default) or ALL, the same
    contract as the sessions list. Tags go through the service-wide
    ``normalize_tag`` on both write and query, so no chain-specific matching
    exists here."""

    request_args = _build_request_args(
        limit=limit,
        offset=offset,
        archived=archived,
        tag=tag,
        tags_mode=tags_mode,
        q=q,
        sim=sim,
        failed_only=failed_only,
        kind=kind,
        handler=handler,
        sort=sort,
        order=order,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ChainListResponse.model_validate(response.json())
