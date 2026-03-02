"""Get Agent Versions"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AgentVersionsResponse


def _build_request_args(
    agent_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/agents/{agent_name}/versions"

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
    agent_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AgentVersionsResponse:
    """Get all versions of a specific Docker image agent.

    Args:
        agent_name: Name of the agent

    Returns:
        All versions of the agent owned by the organization

    Raises:
        HTTPException: 404 if agent not found"""

    request_args = _build_request_args(
        agent_name=agent_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AgentVersionsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    agent_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AgentVersionsResponse:
    """Get all versions of a specific Docker image agent.

    Args:
        agent_name: Name of the agent

    Returns:
        All versions of the agent owned by the organization

    Raises:
        HTTPException: 404 if agent not found"""

    request_args = _build_request_args(
        agent_name=agent_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AgentVersionsResponse.model_validate(response.json())
