"""Lookup Agent"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AgentLookupResponse


def _build_request_args(
    name: str,
    version: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/agents/lookup"

    params: dict[str, Any] = {}
    if name is not None:
        params["name"] = name
    if version is not None:
        params["version"] = version

    headers: dict[str, str] = {}
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
    name: str,
    version: str | None = None,
    x_api_key: str | None = None,
) -> AgentLookupResponse:
    """Lookup an agent by name and optional version. Returns the artifact info."""

    request_args = _build_request_args(
        name=name,
        version=version,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AgentLookupResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    name: str,
    version: str | None = None,
    x_api_key: str | None = None,
) -> AgentLookupResponse:
    """Lookup an agent by name and optional version. Returns the artifact info."""

    request_args = _build_request_args(
        name=name,
        version=version,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AgentLookupResponse.model_validate(response.json())
