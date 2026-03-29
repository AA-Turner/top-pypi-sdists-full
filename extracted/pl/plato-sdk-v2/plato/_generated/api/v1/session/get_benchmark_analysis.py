"""Get Benchmark Analysis"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    simulator_name: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/session/public/benchmarks/{simulator_name}/analysis"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
    simulator_name: str,
) -> Any:
    """Return the pre-computed benchmark failure analysis JSON for a simulator."""

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
    """Return the pre-computed benchmark failure analysis JSON for a simulator."""

    request_args = _build_request_args(
        simulator_name=simulator_name,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
