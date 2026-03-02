"""Get Organization Concurrency Status"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import GetConcurrencyStatusResponse


def _build_request_args(
    organization_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/organization/{organization_id}/concurrency-status"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    organization_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> GetConcurrencyStatusResponse:
    """Get an organization's current concurrency status.

    Returns:
    - Raw Redis counters for debugging (without clamping)
    - Raw reserved token derivation from counters
    - Escrow-aware in-flight estimate range (low/high + midpoint)
    - Assumptions used for rough estimation (overage budget and worker count)

    This is useful for monitoring and debugging concurrency limits."""

    request_args = _build_request_args(
        organization_id=organization_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return GetConcurrencyStatusResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    organization_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> GetConcurrencyStatusResponse:
    """Get an organization's current concurrency status.

    Returns:
    - Raw Redis counters for debugging (without clamping)
    - Raw reserved token derivation from counters
    - Escrow-aware in-flight estimate range (low/high + midpoint)
    - Assumptions used for rough estimation (overage budget and worker count)

    This is useful for monitoring and debugging concurrency limits."""

    request_args = _build_request_args(
        organization_id=organization_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return GetConcurrencyStatusResponse.model_validate(response.json())
