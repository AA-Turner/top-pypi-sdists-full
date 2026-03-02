"""Get Agent Schema"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import RegistryAgentSchemaResponse


def _build_request_args(
    agent_name: str,
    version: str | None = None,
    allow_prerelease: bool | None = False,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/registry/agents/{agent_name}/schema"

    params: dict[str, Any] = {}
    if version is not None:
        params["version"] = version
    if allow_prerelease is not None:
        params["allow_prerelease"] = allow_prerelease

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    agent_name: str,
    version: str | None = None,
    allow_prerelease: bool | None = False,
) -> RegistryAgentSchemaResponse:
    """Get schema for an agent package from the PyPI registry.

    Extracts schema.json from the wheel file."""

    request_args = _build_request_args(
        agent_name=agent_name,
        version=version,
        allow_prerelease=allow_prerelease,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return RegistryAgentSchemaResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    agent_name: str,
    version: str | None = None,
    allow_prerelease: bool | None = False,
) -> RegistryAgentSchemaResponse:
    """Get schema for an agent package from the PyPI registry.

    Extracts schema.json from the wheel file."""

    request_args = _build_request_args(
        agent_name=agent_name,
        version=version,
        allow_prerelease=allow_prerelease,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return RegistryAgentSchemaResponse.model_validate(response.json())
