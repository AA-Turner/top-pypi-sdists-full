"""Launch Job"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import LaunchRequest, LaunchResponse


def _build_request_args(
    body: LaunchRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/chronos/launch"

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
    body: LaunchRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> LaunchResponse:
    """Launch a chronos job with world, agent artifact, and encrypted secrets.

    Creates a Plato session with the specified world package and agent artifact,
    encrypting any secrets with the organization's key."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LaunchResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: LaunchRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> LaunchResponse:
    """Launch a chronos job with world, agent artifact, and encrypted secrets.

    Creates a Plato session with the specified world package and agent artifact,
    encrypting any secrets with the organization's key."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LaunchResponse.model_validate(response.json())
