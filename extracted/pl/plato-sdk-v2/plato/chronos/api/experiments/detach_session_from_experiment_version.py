"""Detach Session From Experiment Version"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import ExperimentFileResponse


def _build_request_args(
    public_id: str,
    session_public_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/experiments/versions/{public_id}/sessions/{session_public_id}"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "DELETE",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    public_id: str,
    session_public_id: str,
    x_api_key: str | None = None,
) -> ExperimentFileResponse:
    """Remove a session attachment from an experiment version."""

    request_args = _build_request_args(
        public_id=public_id,
        session_public_id=session_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ExperimentFileResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    session_public_id: str,
    x_api_key: str | None = None,
) -> ExperimentFileResponse:
    """Remove a session attachment from an experiment version."""

    request_args = _build_request_args(
        public_id=public_id,
        session_public_id=session_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ExperimentFileResponse.model_validate(response.json())
