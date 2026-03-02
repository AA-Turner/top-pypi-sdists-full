"""Update Simulator"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AppApiV1SimulatorRoutesUpdateSimulatorRequest


def _build_request_args(
    simulator_id: int,
    body: AppApiV1SimulatorRoutesUpdateSimulatorRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/simulator/{simulator_id}"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "PUT",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    simulator_id: int,
    body: AppApiV1SimulatorRoutesUpdateSimulatorRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Update simulator fields. Returns the full simulator."""

    request_args = _build_request_args(
        simulator_id=simulator_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    simulator_id: int,
    body: AppApiV1SimulatorRoutesUpdateSimulatorRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Update simulator fields. Returns the full simulator."""

    request_args = _build_request_args(
        simulator_id=simulator_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
