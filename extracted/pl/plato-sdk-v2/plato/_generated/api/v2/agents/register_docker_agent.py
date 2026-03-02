"""Register Docker Agent"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import RegisterDockerAgentRequest, RegisterDockerAgentResponse


def _build_request_args(
    body: RegisterDockerAgentRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/agents/register"

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
    body: RegisterDockerAgentRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RegisterDockerAgentResponse:
    """Register a Docker image agent with optional schema.

    Validation rules:
    1. If agent name exists with different org_id -> reject (403)
    2. If agent name exists with same org_id but different version -> allow (new version)
    3. If agent name + version exists -> reject (409)
    4. If agent name is new -> allow"""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return RegisterDockerAgentResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: RegisterDockerAgentRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RegisterDockerAgentResponse:
    """Register a Docker image agent with optional schema.

    Validation rules:
    1. If agent name exists with different org_id -> reject (403)
    2. If agent name exists with same org_id but different version -> allow (new version)
    3. If agent name + version exists -> reject (409)
    4. If agent name is new -> allow"""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return RegisterDockerAgentResponse.model_validate(response.json())
