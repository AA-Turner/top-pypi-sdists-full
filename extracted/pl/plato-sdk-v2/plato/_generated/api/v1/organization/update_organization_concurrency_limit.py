"""Update Organization Concurrency Limit"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import UpdateConcurrencyLimitRequest, UpdateConcurrencyLimitResponse


def _build_request_args(
    organization_id: int,
    body: UpdateConcurrencyLimitRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/organization/{organization_id}/concurrency-limit"

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
    organization_id: int,
    body: UpdateConcurrencyLimitRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> UpdateConcurrencyLimitResponse:
    """Update an organization's concurrency limit (admin only).

    This endpoint allows admins to update the max_concurrent_runs value
    in an organization's plan, which controls how many simultaneous sessions
    the organization can run.

    After updating the limit, Redis-backed concurrency counters are synced
    for the v2 local limiter."""

    request_args = _build_request_args(
        organization_id=organization_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return UpdateConcurrencyLimitResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    organization_id: int,
    body: UpdateConcurrencyLimitRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> UpdateConcurrencyLimitResponse:
    """Update an organization's concurrency limit (admin only).

    This endpoint allows admins to update the max_concurrent_runs value
    in an organization's plan, which controls how many simultaneous sessions
    the organization can run.

    After updating the limit, Redis-backed concurrency counters are synced
    for the v2 local limiter."""

    request_args = _build_request_args(
        organization_id=organization_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return UpdateConcurrencyLimitResponse.model_validate(response.json())
