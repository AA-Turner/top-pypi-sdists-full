"""Create Dataset File"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import DatasetFileCreateRequest, DatasetFileResponse


def _build_request_args(
    body: DatasetFileCreateRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/datasets/files"

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
    body: DatasetFileCreateRequest,
    x_api_key: str | None = None,
) -> DatasetFileResponse:
    """Create a new dataset file with an initial version."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return DatasetFileResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: DatasetFileCreateRequest,
    x_api_key: str | None = None,
) -> DatasetFileResponse:
    """Create a new dataset file with an initial version."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return DatasetFileResponse.model_validate(response.json())
