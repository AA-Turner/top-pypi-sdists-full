"""Health check and display info"""

from __future__ import annotations

from typing import Any

import httpx

from ...errors import raise_for_status
from ...models import StatusResponse


def _build_request_args() -> dict[str, Any]:
    """Build request arguments."""
    url = "/status"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
) -> StatusResponse:
    """Health check and display info"""

    request_args = _build_request_args()

    response = client.request(**request_args)
    raise_for_status(response)
    return StatusResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
) -> StatusResponse:
    """Health check and display info"""

    request_args = _build_request_args()

    response = await client.request(**request_args)
    raise_for_status(response)
    return StatusResponse.model_validate(response.json())
