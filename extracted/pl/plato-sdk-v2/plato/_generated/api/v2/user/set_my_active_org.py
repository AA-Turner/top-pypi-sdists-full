"""Set My Active Org"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SetActiveOrgRequest, UserOrgsResponse


def _build_request_args(
    body: SetActiveOrgRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/user/me/active-org"

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
    body: SetActiveOrgRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> UserOrgsResponse:
    """Switch the current user's active org to another org they are a member of.

    Session principals only: the active org is global account state that
    redirects all org-scoped reads/writes, so a delegated API key must not be
    able to change it."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return UserOrgsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: SetActiveOrgRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> UserOrgsResponse:
    """Switch the current user's active org to another org they are a member of.

    Session principals only: the active org is global account state that
    redirects all org-scoped reads/writes, so a delegated API key must not be
    able to change it."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return UserOrgsResponse.model_validate(response.json())
