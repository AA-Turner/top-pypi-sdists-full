"""Delete Simulator Screenshot"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SimulatorResponse


def _build_request_args(
    name: str,
    url: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/simulators/{name}/screenshots"

    params: dict[str, Any] = {}
    if url is not None:
        params["url"] = url

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "DELETE",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    name: str,
    url: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SimulatorResponse:
    """Remove a screenshot from the sim. If the URL points at the
    plato-sim-public-assets bucket, the S3 object is deleted too."""

    request_args = _build_request_args(
        name=name,
        url=url,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SimulatorResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    name: str,
    url: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SimulatorResponse:
    """Remove a screenshot from the sim. If the URL points at the
    plato-sim-public-assets bucket, the S3 object is deleted too."""

    request_args = _build_request_args(
        name=name,
        url=url,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SimulatorResponse.model_validate(response.json())
