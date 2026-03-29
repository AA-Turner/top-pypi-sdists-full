"""Get Global Benchmark Pass Rates"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    model: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/session/public/benchmarks/global/pass-rates"

    params: dict[str, Any] = {}
    if model is not None:
        params["model"] = model

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    model: str,
) -> Any:
    """Pass/fail totals for one model across all simulators.
    In local/dev: fetches from prod per-simulator benchmark endpoints.
    In prod: queries the database directly."""

    request_args = _build_request_args(
        model=model,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    model: str,
) -> Any:
    """Pass/fail totals for one model across all simulators.
    In local/dev: fetches from prod per-simulator benchmark endpoints.
    In prod: queries the database directly."""

    request_args = _build_request_args(
        model=model,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
