"""List Session Creators"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import CreatorsListResponse


def _build_request_args(
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/sessions/creators"

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
) -> CreatorsListResponse:
    """List distinct users who have created sessions in this org."""

    request_args = _build_request_args(
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return CreatorsListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    x_api_key: str | None = None,
) -> CreatorsListResponse:
    """List distinct users who have created sessions in this org."""

    request_args = _build_request_args(
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return CreatorsListResponse.model_validate(response.json())
