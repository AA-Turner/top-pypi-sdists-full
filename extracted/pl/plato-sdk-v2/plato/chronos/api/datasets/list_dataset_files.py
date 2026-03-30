"""List Dataset Files"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import DatasetFileListResponse


def _build_request_args(
    created_by: str | None = None,
    folder: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/datasets/files"

    params: dict[str, Any] = {}
    if created_by is not None:
        params["created_by"] = created_by
    if folder is not None:
        params["folder"] = folder

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
    created_by: str | None = None,
    folder: str | None = None,
    x_api_key: str | None = None,
) -> DatasetFileListResponse:
    """List dataset files for the current org."""

    request_args = _build_request_args(
        created_by=created_by,
        folder=folder,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return DatasetFileListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    created_by: str | None = None,
    folder: str | None = None,
    x_api_key: str | None = None,
) -> DatasetFileListResponse:
    """List dataset files for the current org."""

    request_args = _build_request_args(
        created_by=created_by,
        folder=folder,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return DatasetFileListResponse.model_validate(response.json())
