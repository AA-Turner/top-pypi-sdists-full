"""Create Experiment File"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import ExperimentFileCreateRequest, ExperimentFileResponse


def _build_request_args(
    body: ExperimentFileCreateRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/experiments/files"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    body: ExperimentFileCreateRequest,
    x_api_key: str | None = None,
) -> ExperimentFileResponse:
    """Create a new experiment file and its initial version."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ExperimentFileResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: ExperimentFileCreateRequest,
    x_api_key: str | None = None,
) -> ExperimentFileResponse:
    """Create a new experiment file and its initial version."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ExperimentFileResponse.model_validate(response.json())
