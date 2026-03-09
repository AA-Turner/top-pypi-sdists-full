"""Delete Saved Filter"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    filter_id: int,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/saved-filters/{filter_id}"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "DELETE",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    filter_id: int,
    x_api_key: str | None = None,
) -> Any:
    """Delete a saved filter preset (must belong to current user)."""

    request_args = _build_request_args(
        filter_id=filter_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    filter_id: int,
    x_api_key: str | None = None,
) -> Any:
    """Delete a saved filter preset (must belong to current user)."""

    request_args = _build_request_args(
        filter_id=filter_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
