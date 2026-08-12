"""Get Authz Enums"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AuthzEnumsResponse


def _build_request_args(
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/authz/enums"

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
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AuthzEnumsResponse:
    """Roles, resource types, and user permission flags for admin UI pickers.

    Derived from the enums and `UserPermissions` at request time — adding a role
    or flag in Python surfaces it here with no frontend change. Dead roles are
    filtered out so they can't be granted."""

    request_args = _build_request_args(
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AuthzEnumsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AuthzEnumsResponse:
    """Roles, resource types, and user permission flags for admin UI pickers.

    Derived from the enums and `UserPermissions` at request time — adding a role
    or flag in Python surfaces it here with no frontend change. Dead roles are
    filtered out so they can't be granted."""

    request_args = _build_request_args(
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AuthzEnumsResponse.model_validate(response.json())
