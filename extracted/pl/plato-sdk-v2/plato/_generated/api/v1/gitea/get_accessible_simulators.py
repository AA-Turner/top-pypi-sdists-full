"""Get Accessible Simulators"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AppSchemasGiteaResponsesSimulatorListItemResponse


def _build_request_args(
    authorization: str | None = None,
    x_internal_service: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/gitea/simulators"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_internal_service is not None:
        headers["X-Internal-Service"] = x_internal_service
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    authorization: str | None = None,
    x_internal_service: str | None = None,
    x_api_key: str | None = None,
) -> list[AppSchemasGiteaResponsesSimulatorListItemResponse]:
    """Get simulators that user has access to view repos for"""

    request_args = _build_request_args(
        authorization=authorization,
        x_internal_service=x_internal_service,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    authorization: str | None = None,
    x_internal_service: str | None = None,
    x_api_key: str | None = None,
) -> list[AppSchemasGiteaResponsesSimulatorListItemResponse]:
    """Get simulators that user has access to view repos for"""

    request_args = _build_request_args(
        authorization=authorization,
        x_internal_service=x_internal_service,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
