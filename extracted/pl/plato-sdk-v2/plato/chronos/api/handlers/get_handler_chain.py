"""Get Handler Chain"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import ChainViewResponse


def _build_request_args(
    chain_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/handlers/chains/{chain_id}"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    chain_id: str,
    x_api_key: str | None = None,
) -> ChainViewResponse:
    """Everything sharing one chain_id: sessions, assignments, invocations."""

    request_args = _build_request_args(
        chain_id=chain_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ChainViewResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    chain_id: str,
    x_api_key: str | None = None,
) -> ChainViewResponse:
    """Everything sharing one chain_id: sessions, assignments, invocations."""

    request_args = _build_request_args(
        chain_id=chain_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ChainViewResponse.model_validate(response.json())
