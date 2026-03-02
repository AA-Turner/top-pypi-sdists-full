"""Get Simulator Info"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SimulatorInfoResponse


def _build_request_args(
    simulator_name: str,
    dataset: str,
    include_checkpoints: bool | None = False,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/simulator/{simulator_name}/{dataset}/info"

    params: dict[str, Any] = {}
    if include_checkpoints is not None:
        params["include_checkpoints"] = include_checkpoints

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    simulator_name: str,
    dataset: str,
    include_checkpoints: bool | None = False,
) -> SimulatorInfoResponse:
    """Get artifact and tag information for a specific simulator using Postgres"""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        dataset=dataset,
        include_checkpoints=include_checkpoints,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SimulatorInfoResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    simulator_name: str,
    dataset: str,
    include_checkpoints: bool | None = False,
) -> SimulatorInfoResponse:
    """Get artifact and tag information for a specific simulator using Postgres"""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        dataset=dataset,
        include_checkpoints=include_checkpoints,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SimulatorInfoResponse.model_validate(response.json())
