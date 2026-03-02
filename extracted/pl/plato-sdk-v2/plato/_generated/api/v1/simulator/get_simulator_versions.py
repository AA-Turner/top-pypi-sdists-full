"""Get Simulator Versions"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SimulatorVersionsResponse


def _build_request_args(
    simulator_name: str,
    include_checkpoints: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/simulator/{simulator_name}/versions"

    params: dict[str, Any] = {}
    if include_checkpoints is not None:
        params["include_checkpoints"] = include_checkpoints

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
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
    simulator_name: str,
    include_checkpoints: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SimulatorVersionsResponse:
    """Get all versions for a specific simulator across all datasets"""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        include_checkpoints=include_checkpoints,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SimulatorVersionsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    simulator_name: str,
    include_checkpoints: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SimulatorVersionsResponse:
    """Get all versions for a specific simulator across all datasets"""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        include_checkpoints=include_checkpoints,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SimulatorVersionsResponse.model_validate(response.json())
