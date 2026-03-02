"""Generate State Mutations Config Route"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    id: int,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/testcases/{id}/generate-state-mutations-config"

    return {
        "method": "POST",
        "url": url,
    }


def sync(
    client: httpx.Client,
    id: int,
) -> Any:
    """Generate State Mutations Config Route"""

    request_args = _build_request_args(
        id=id,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    id: int,
) -> Any:
    """Generate State Mutations Config Route"""

    request_args = _build_request_args(
        id=id,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
