"""List Registry Agents"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import RegistryAgentListResponse


def _build_request_args() -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/registry/agents"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
) -> RegistryAgentListResponse:
    """List all agent packages from the PyPI registry."""

    request_args = _build_request_args()

    response = client.request(**request_args)
    raise_for_status(response)
    return RegistryAgentListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
) -> RegistryAgentListResponse:
    """List all agent packages from the PyPI registry."""

    request_args = _build_request_args()

    response = await client.request(**request_args)
    raise_for_status(response)
    return RegistryAgentListResponse.model_validate(response.json())
