"""Sync User External Access"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ExternalAccessSyncResult


def _build_request_args(
    user_public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/admin/users/{user_public_id}/sync-external-access"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    user_public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ExternalAccessSyncResult:
    """Run the full external-services sync (hub gitea + guacamole) for a user
    now — the "refresh permissions" button.

    Same reconcile a login performs, so an admin can push the current truth to
    a user (including provisioning their hub account for the first time)
    without asking them to log out and back in."""

    request_args = _build_request_args(
        user_public_id=user_public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ExternalAccessSyncResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    user_public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ExternalAccessSyncResult:
    """Run the full external-services sync (hub gitea + guacamole) for a user
    now — the "refresh permissions" button.

    Same reconcile a login performs, so an admin can push the current truth to
    a user (including provisioning their hub account for the first time)
    without asking them to log out and back in."""

    request_args = _build_request_args(
        user_public_id=user_public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ExternalAccessSyncResult.model_validate(response.json())
