"""List Invites"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import OrgInviteListResponse


def _build_request_args(
    org_public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/orgs/{org_public_id}/invites"

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
) -> OrgInviteListResponse:
    """Every invite ever minted for the org, newest first, with who redeemed
    each one — the audit trail for how people got in."""

    request_args = _build_request_args(
        org_public_id=org_public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return OrgInviteListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    org_public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> OrgInviteListResponse:
    """Every invite ever minted for the org, newest first, with who redeemed
    each one — the audit trail for how people got in."""

    request_args = _build_request_args(
        org_public_id=org_public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return OrgInviteListResponse.model_validate(response.json())
