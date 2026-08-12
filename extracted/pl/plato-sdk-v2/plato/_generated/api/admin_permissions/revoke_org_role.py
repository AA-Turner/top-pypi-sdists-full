"""Revoke Org Role"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import OrgPermissionUser


def _build_request_args(
    org_public_id: str,
    user_public_id: str,
    role: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/admin/orgs/{org_public_id}/users/{user_public_id}/roles/{role}"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "DELETE",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    org_public_id: str,
    user_public_id: str,
    role: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> OrgPermissionUser:
    """Revoke an org-level capability role from a user.

    Revoking the user's *last* role in an org ends their membership there, so
    this path upholds the same invariants as `remove_user_from_org`: it refuses
    when that org is their only one, and re-points the active org when the
    membership it pointed at is the one going away."""

    request_args = _build_request_args(
        org_public_id=org_public_id,
        user_public_id=user_public_id,
        role=role,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return OrgPermissionUser.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    org_public_id: str,
    user_public_id: str,
    role: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> OrgPermissionUser:
    """Revoke an org-level capability role from a user.

    Revoking the user's *last* role in an org ends their membership there, so
    this path upholds the same invariants as `remove_user_from_org`: it refuses
    when that org is their only one, and re-points the active org when the
    membership it pointed at is the one going away."""

    request_args = _build_request_args(
        org_public_id=org_public_id,
        user_public_id=user_public_id,
        role=role,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return OrgPermissionUser.model_validate(response.json())
