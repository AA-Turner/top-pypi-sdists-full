"""Get Benchmark Model Errors"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    simulator_name: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/session/public/benchmarks/{simulator_name}/model-errors"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
    simulator_name: str,
) -> Any:
    """Return model-fault sessions with sub-grouping for a simulator."""

    request_args = _build_request_args(
        simulator_name=simulator_name,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    simulator_name: str,
) -> Any:
    """Return model-fault sessions with sub-grouping for a simulator."""

    request_args = _build_request_args(
        simulator_name=simulator_name,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
