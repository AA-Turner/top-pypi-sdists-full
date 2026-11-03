"""List Releases"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ReleaseResponse, ReleaseStatus


def _build_request_args(
    organization_id: int | None = None,
    status: ReleaseStatus | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/releases"

    params: dict[str, Any] = {}
    if organization_id is not None:
        params["organization_id"] = organization_id
    if status is not None:
        params["status"] = status

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
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
    organization_id: int | None = None,
    status: ReleaseStatus | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> list[ReleaseResponse]:
    """Get releases. Admins can filter by org, others see only their org's."""

    request_args = _build_request_args(
        organization_id=organization_id,
        status=status,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    organization_id: int | None = None,
    status: ReleaseStatus | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> list[ReleaseResponse]:
    """Get releases. Admins can filter by org, others see only their org's."""

    request_args = _build_request_args(
        organization_id=organization_id,
        status=status,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
