"""Delete Key"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import CacheKeyDeleteResponse, CacheName


def _build_request_args(
    cache_name: CacheName,
    key: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/admin/cache/key/{cache_name}/{key}"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "DELETE",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    cache_name: CacheName,
    key: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> CacheKeyDeleteResponse:
    """Delete a specific key from a cache.

    Note: This only deletes from the current worker. For distributed
    invalidation of a specific key, consider clearing the entire cache.

    Requires admin privileges."""

    request_args = _build_request_args(
        cache_name=cache_name,
        key=key,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return CacheKeyDeleteResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    cache_name: CacheName,
    key: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> CacheKeyDeleteResponse:
    """Delete a specific key from a cache.

    Note: This only deletes from the current worker. For distributed
    invalidation of a specific key, consider clearing the entire cache.

    Requires admin privileges."""

    request_args = _build_request_args(
        cache_name=cache_name,
        key=key,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return CacheKeyDeleteResponse.model_validate(response.json())
