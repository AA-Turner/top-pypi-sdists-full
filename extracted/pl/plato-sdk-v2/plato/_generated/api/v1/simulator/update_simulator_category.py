"""Update Simulator Category"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SimulatorCategoryInfo, UpdateSimulatorCategoryRequest


def _build_request_args(
    category_id: int,
    body: UpdateSimulatorCategoryRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/simulator/categories/{category_id}"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "PUT",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    category_id: int,
    body: UpdateSimulatorCategoryRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SimulatorCategoryInfo:
    """Rename a category or change its description (admin only)."""

    request_args = _build_request_args(
        category_id=category_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SimulatorCategoryInfo.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    category_id: int,
    body: UpdateSimulatorCategoryRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SimulatorCategoryInfo:
    """Rename a category or change its description (admin only)."""

    request_args = _build_request_args(
        category_id=category_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SimulatorCategoryInfo.model_validate(response.json())
