"""List Worlds"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import WorldListResponse


def _build_request_args(
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/worlds"

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
    x_api_key: str | None = None,
) -> WorldListResponse:
    """List all worlds for the org."""

    request_args = _build_request_args(
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WorldListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    x_api_key: str | None = None,
) -> WorldListResponse:
    """List all worlds for the org."""

    request_args = _build_request_args(
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WorldListResponse.model_validate(response.json())
