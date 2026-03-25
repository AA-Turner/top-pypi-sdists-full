"""Upsert Iteration Session"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import IterationSessionResponse, UpsertIterationSessionRequest


def _build_request_args(
    public_id: str,
    iteration_num: int,
    body: UpsertIterationSessionRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/hillclimb-runs/{public_id}/iterations/{iteration_num}/sessions"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "PUT",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    public_id: str,
    iteration_num: int,
    body: UpsertIterationSessionRequest,
    x_api_key: str | None = None,
) -> IterationSessionResponse:
    """Upsert a session linked to an iteration. Keyed by (iteration_id, session_id)."""

    request_args = _build_request_args(
        public_id=public_id,
        iteration_num=iteration_num,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return IterationSessionResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    iteration_num: int,
    body: UpsertIterationSessionRequest,
    x_api_key: str | None = None,
) -> IterationSessionResponse:
    """Upsert a session linked to an iteration. Keyed by (iteration_id, session_id)."""

    request_args = _build_request_args(
        public_id=public_id,
        iteration_num=iteration_num,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return IterationSessionResponse.model_validate(response.json())
