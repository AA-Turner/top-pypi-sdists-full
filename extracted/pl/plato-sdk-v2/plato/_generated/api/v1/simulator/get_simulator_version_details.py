"""Get Simulator Version Details"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SimulatorVersionDetails


def _build_request_args(
    simulator_name: str,
    dataset: str,
    version: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/simulator/{simulator_name}/{dataset}/version/{version}"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
    simulator_name: str,
    dataset: str,
    version: str,
) -> SimulatorVersionDetails:
    """Get build artifacts (Docker image, ECS task def, snapshot URI) for a specific simulator version"""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        dataset=dataset,
        version=version,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SimulatorVersionDetails.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    simulator_name: str,
    dataset: str,
    version: str,
) -> SimulatorVersionDetails:
    """Get build artifacts (Docker image, ECS task def, snapshot URI) for a specific simulator version"""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        dataset=dataset,
        version=version,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SimulatorVersionDetails.model_validate(response.json())
