"""Clear Single Cache"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import CacheClearResponse, CacheName


def _build_request_args(
    cache_name: CacheName,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/admin/cache/clear/{cache_name}"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    cache_name: CacheName,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> CacheClearResponse:
    """Clear a specific cache by name.

    This clears the cache on the current worker and publishes an event
    to clear the cache on all other workers in the cluster.

    Requires admin privileges."""

    request_args = _build_request_args(
        cache_name=cache_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return CacheClearResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    cache_name: CacheName,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> CacheClearResponse:
    """Clear a specific cache by name.

    This clears the cache on the current worker and publishes an event
    to clear the cache on all other workers in the cluster.

    Requires admin privileges."""

    request_args = _build_request_args(
        cache_name=cache_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return CacheClearResponse.model_validate(response.json())
