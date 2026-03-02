"""Get Agent Ecr Token"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import EcrTokenResponse


def _build_request_args(
    agent_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/agents/ecr-token"

    params: dict[str, Any] = {}
    if agent_name is not None:
        params["agent_name"] = agent_name

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    agent_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> EcrTokenResponse:
    """Get ECR push token for agent image.

    Returns token for pushing to agents/{org}/{agent_name} repository.
    Creates the repository if it doesn't exist."""

    request_args = _build_request_args(
        agent_name=agent_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return EcrTokenResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    agent_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> EcrTokenResponse:
    """Get ECR push token for agent image.

    Returns token for pushing to agents/{org}/{agent_name} repository.
    Creates the repository if it doesn't exist."""

    request_args = _build_request_args(
        agent_name=agent_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return EcrTokenResponse.model_validate(response.json())
