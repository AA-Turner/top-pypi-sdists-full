"""Get Replay Score Data"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    agent_artifact_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/session/replay-score/{agent_artifact_id}"

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
    agent_artifact_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Replay Score Data"""

    request_args = _build_request_args(
        agent_artifact_id=agent_artifact_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    agent_artifact_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Replay Score Data"""

    request_args = _build_request_args(
        agent_artifact_id=agent_artifact_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
