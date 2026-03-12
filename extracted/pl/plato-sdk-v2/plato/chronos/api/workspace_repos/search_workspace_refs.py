"""Search Workspace Refs"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import WorkspaceRefSearchResponse


def _build_request_args(
    q: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/workspace-repos/search"

    params: dict[str, Any] = {}
    if q is not None:
        params["q"] = q

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
    q: str,
    x_api_key: str | None = None,
) -> WorkspaceRefSearchResponse:
    """Search for workspace refs by session:step format or free text."""

    request_args = _build_request_args(
        q=q,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WorkspaceRefSearchResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    q: str,
    x_api_key: str | None = None,
) -> WorkspaceRefSearchResponse:
    """Search for workspace refs by session:step format or free text."""

    request_args = _build_request_args(
        q=q,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WorkspaceRefSearchResponse.model_validate(response.json())
