"""List Tags"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import TagsListResponse


def _build_request_args(
    q: str | None = None,
    limit: int | None = 10,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/sessions/tags"

    params: dict[str, Any] = {}
    if q is not None:
        params["q"] = q
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
    q: str | None = None,
    limit: int | None = 10,
    x_api_key: str | None = None,
) -> TagsListResponse:
    """Search unique tags for the org with ltree hierarchical matching.

    Uses ltree for hierarchical tags with '.' separator.
    Search matches tags containing the query as a substring or ancestor/descendant."""

    request_args = _build_request_args(
        q=q,
        limit=limit,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return TagsListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    q: str | None = None,
    limit: int | None = 10,
    x_api_key: str | None = None,
) -> TagsListResponse:
    """Search unique tags for the org with ltree hierarchical matching.

    Uses ltree for hierarchical tags with '.' separator.
    Search matches tags containing the query as a substring or ancestor/descendant."""

    request_args = _build_request_args(
        q=q,
        limit=limit,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return TagsListResponse.model_validate(response.json())
