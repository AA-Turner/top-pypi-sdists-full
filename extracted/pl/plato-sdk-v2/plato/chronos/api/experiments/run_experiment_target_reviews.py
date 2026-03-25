"""Run Target Reviews"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import RunReviewsResponse


def _build_request_args(
    public_id: str,
    session_public_id: str,
    spec_index: int | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/experiments/files/{public_id}/run-reviews/{session_public_id}"

    params: dict[str, Any] = {}
    if spec_index is not None:
        params["spec_index"] = spec_index

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    public_id: str,
    session_public_id: str,
    spec_index: int | None = None,
    x_api_key: str | None = None,
) -> RunReviewsResponse:
    """Launch target review sessions for a linked experiment session.

    For each target review spec on the experiment file (or a single one if
    spec_index is provided), launches a review session with the
    target_session_id set to the given session."""

    request_args = _build_request_args(
        public_id=public_id,
        session_public_id=session_public_id,
        spec_index=spec_index,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return RunReviewsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    session_public_id: str,
    spec_index: int | None = None,
    x_api_key: str | None = None,
) -> RunReviewsResponse:
    """Launch target review sessions for a linked experiment session.

    For each target review spec on the experiment file (or a single one if
    spec_index is provided), launches a review session with the
    target_session_id set to the given session."""

    request_args = _build_request_args(
        public_id=public_id,
        session_public_id=session_public_id,
        spec_index=spec_index,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return RunReviewsResponse.model_validate(response.json())
