"""Get Current User"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import UserResponse


def _build_request_args(
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/user/me"

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
) -> UserResponse:
    """Get current user info.

    Accepts authentication via:
    - Authorization: Bearer <jwt_token>
    - X-API-Key: <api_key>

    Returns user info for the authenticated principal."""

    request_args = _build_request_args(
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return UserResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> UserResponse:
    """Get current user info.

    Accepts authentication via:
    - Authorization: Bearer <jwt_token>
    - X-API-Key: <api_key>

    Returns user info for the authenticated principal."""

    request_args = _build_request_args(
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return UserResponse.model_validate(response.json())
