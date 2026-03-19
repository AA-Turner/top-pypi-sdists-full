"""List Datasets"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import DatasetResponse


def _build_request_args(
    world_package: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/datasets"

    params: dict[str, Any] = {}
    if world_package is not None:
        params["world_package"] = world_package

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
    world_package: str | None = None,
    x_api_key: str | None = None,
) -> list[DatasetResponse]:
    """List Datasets"""

    request_args = _build_request_args(
        world_package=world_package,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    world_package: str | None = None,
    x_api_key: str | None = None,
) -> list[DatasetResponse]:
    """List Datasets"""

    request_args = _build_request_args(
        world_package=world_package,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
