"""Get Session Cost Summary"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionCostSummaryResponse


def _build_request_args(
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/sessions/cost-summary"

    params: dict[str, Any] = {}
    if tags is not None:
        params["tags"] = tags
    if tags_mode is not None:
        params["tags_mode"] = tags_mode

    headers: dict[str, str] = {}
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
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    x_api_key: str | None = None,
) -> SessionCostSummaryResponse:
    """Return lightweight cost data for all matching sessions (no pagination limit).

    Returns session_id, created_at, total_cost_usd, and tags for each matching
    top-level session.  The frontend uses this to compute totals, per-period
    breakdowns, and per-simulator costs without being capped at 200 rows."""

    request_args = _build_request_args(
        tags=tags,
        tags_mode=tags_mode,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionCostSummaryResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    x_api_key: str | None = None,
) -> SessionCostSummaryResponse:
    """Return lightweight cost data for all matching sessions (no pagination limit).

    Returns session_id, created_at, total_cost_usd, and tags for each matching
    top-level session.  The frontend uses this to compute totals, per-period
    breakdowns, and per-simulator costs without being capped at 200 rows."""

    request_args = _build_request_args(
        tags=tags,
        tags_mode=tags_mode,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionCostSummaryResponse.model_validate(response.json())
