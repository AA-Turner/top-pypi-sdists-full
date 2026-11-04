"""Get Org Permissions"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import OrgPermissionsResponse


def _build_request_args(
    org_public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/admin/orgs/{org_public_id}/permissions"

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
    org_public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> OrgPermissionsResponse:
    """Return all users who have any policy grant on this org."""

    request_args = _build_request_args(
        org_public_id=org_public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return OrgPermissionsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    org_public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> OrgPermissionsResponse:
    """Return all users who have any policy grant on this org."""

    request_args = _build_request_args(
        org_public_id=org_public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return OrgPermissionsResponse.model_validate(response.json())
