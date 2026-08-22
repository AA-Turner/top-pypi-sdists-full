"""List Grants"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AuthorizationRole, AuthzGrantsResponse, ResourceType


def _build_request_args(
    role: AuthorizationRole,
    resource_type: ResourceType,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/authz/grants"

    params: dict[str, Any] = {}
    if role is not None:
        params["role"] = getattr(role, "value", role)
    if resource_type is not None:
        params["resource_type"] = getattr(resource_type, "value", resource_type)

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
    role: AuthorizationRole,
    resource_type: ResourceType,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AuthzGrantsResponse:
    """Return all resource IDs the principal can access for a role + resource type."""

    request_args = _build_request_args(
        role=role,
        resource_type=resource_type,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AuthzGrantsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    role: AuthorizationRole,
    resource_type: ResourceType,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AuthzGrantsResponse:
    """Return all resource IDs the principal can access for a role + resource type."""

    request_args = _build_request_args(
        role=role,
        resource_type=resource_type,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AuthzGrantsResponse.model_validate(response.json())
