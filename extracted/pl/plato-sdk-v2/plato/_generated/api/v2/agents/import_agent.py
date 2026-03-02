"""Import Agent"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ImportAgentRequest, ImportAgentResponse


def _build_request_args(
    body: ImportAgentRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/agents/import"

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
    body: ImportAgentRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ImportAgentResponse:
    """Import an agent from an external registry.

    This endpoint is used by the frontend to import agents discovered
    from the Plato registry into the local backend. Unlike /register,
    this does not enforce version ordering - it allows importing any
    version that doesn't already exist.

    Returns existing artifact if name+version already imported."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ImportAgentResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: ImportAgentRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ImportAgentResponse:
    """Import an agent from an external registry.

    This endpoint is used by the frontend to import agents discovered
    from the Plato registry into the local backend. Unlike /register,
    this does not enforce version ordering - it allows importing any
    version that doesn't already exist.

    Returns existing artifact if name+version already imported."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ImportAgentResponse.model_validate(response.json())
