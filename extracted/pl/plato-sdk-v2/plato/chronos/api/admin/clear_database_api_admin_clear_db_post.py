"""Clear Database"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import ClearDbResult


def _build_request_args(
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/admin/clear-db"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    x_api_key: str | None = None,
) -> ClearDbResult:
    """Clear ALL data from the database. Only available in local environment."""

    request_args = _build_request_args(
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ClearDbResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    x_api_key: str | None = None,
) -> ClearDbResult:
    """Clear ALL data from the database. Only available in local environment."""

    request_args = _build_request_args(
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ClearDbResult.model_validate(response.json())
