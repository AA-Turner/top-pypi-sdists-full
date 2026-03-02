"""Rescore Simulator Sessions"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import RescoreResponse


def _build_request_args(
    simulator_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/env/simulators/{simulator_id}/rescore"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    simulator_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RescoreResponse:
    """Rescore all sessions for all test cases in a simulator."""

    request_args = _build_request_args(
        simulator_id=simulator_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return RescoreResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    simulator_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RescoreResponse:
    """Rescore all sessions for all test cases in a simulator."""

    request_args = _build_request_args(
        simulator_id=simulator_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return RescoreResponse.model_validate(response.json())
