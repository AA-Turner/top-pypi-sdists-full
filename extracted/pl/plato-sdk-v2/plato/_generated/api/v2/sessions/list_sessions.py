"""List Sessions"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    page: int | None = 1,
    page_size: int | None = 50,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/sessions"

    params: dict[str, Any] = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    page: int | None = 1,
    page_size: int | None = 50,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """List all sessions for the authenticated user or organization."""

    request_args = _build_request_args(
        page=page,
        page_size=page_size,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    page: int | None = 1,
    page_size: int | None = 50,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """List all sessions for the authenticated user or organization."""

    request_args = _build_request_args(
        page=page,
        page_size=page_size,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
