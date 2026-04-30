"""Get Global Benchmark Pass Rates"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    model: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/session/public/benchmarks/global/pass-rates"

    params: dict[str, Any] = {}
    if model is not None:
        params["model"] = model

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
    model: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Pass/fail totals for one model across all simulators.
    In local/dev: fetches from prod per-simulator benchmark endpoints.
    In prod: queries the database directly."""

    request_args = _build_request_args(
        model=model,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    model: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Pass/fail totals for one model across all simulators.
    In local/dev: fetches from prod per-simulator benchmark endpoints.
    In prod: queries the database directly."""

    request_args = _build_request_args(
        model=model,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
