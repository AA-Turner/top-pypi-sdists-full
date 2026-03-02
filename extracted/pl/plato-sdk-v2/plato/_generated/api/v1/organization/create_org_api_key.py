"""Create Org Api Key"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import CreateOrgApiKeyRequest, CreateOrgApiKeyResponse


def _build_request_args(
    org_id: str,
    body: CreateOrgApiKeyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/organization/{org_id}/api-keys"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    org_id: str,
    body: CreateOrgApiKeyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> CreateOrgApiKeyResponse:
    """Create an API key for an organization. Use 'me' for current org, or org ID (admin only)."""

    request_args = _build_request_args(
        org_id=org_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return CreateOrgApiKeyResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    org_id: str,
    body: CreateOrgApiKeyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> CreateOrgApiKeyResponse:
    """Create an API key for an organization. Use 'me' for current org, or org ID (admin only)."""

    request_args = _build_request_args(
        org_id=org_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return CreateOrgApiKeyResponse.model_validate(response.json())
