"""Get Agent Versions"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AgentVersionsResponse


def _build_request_args(
    name: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/agents/by-name/{name}/versions"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    name: str,
    x_api_key: str | None = None,
) -> AgentVersionsResponse:
    """Get all versions of an agent by name."""

    request_args = _build_request_args(
        name=name,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AgentVersionsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    name: str,
    x_api_key: str | None = None,
) -> AgentVersionsResponse:
    """Get all versions of an agent by name."""

    request_args = _build_request_args(
        name=name,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AgentVersionsResponse.model_validate(response.json())
