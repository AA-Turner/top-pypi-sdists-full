"""Get Simulator Id"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SimulatorIdResponse


def _build_request_args(
    simulator_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/simulator/{simulator_name}/id"

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
    simulator_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SimulatorIdResponse:
    """Get the simulator ID for a given simulator name."""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SimulatorIdResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    simulator_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SimulatorIdResponse:
    """Get the simulator ID for a given simulator name."""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SimulatorIdResponse.model_validate(response.json())
