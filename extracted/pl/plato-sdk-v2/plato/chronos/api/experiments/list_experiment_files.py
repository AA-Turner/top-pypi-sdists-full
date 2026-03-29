"""List Experiment Files"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import ExperimentFileListResponse


def _build_request_args(
    created_by: str | None = None,
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    folder: str | None = None,
    exclude_hillclimb: bool | None = False,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/experiments/files"

    params: dict[str, Any] = {}
    if created_by is not None:
        params["created_by"] = created_by
    if tags is not None:
        params["tags"] = tags
    if tags_mode is not None:
        params["tags_mode"] = tags_mode
    if folder is not None:
        params["folder"] = folder
    if exclude_hillclimb is not None:
        params["exclude_hillclimb"] = exclude_hillclimb

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
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    folder: str | None = None,
    exclude_hillclimb: bool | None = False,
    x_api_key: str | None = None,
) -> ExperimentFileListResponse:
    """List versioned experiment files for the current org."""

    request_args = _build_request_args(
        created_by=created_by,
        tags=tags,
        tags_mode=tags_mode,
        folder=folder,
        exclude_hillclimb=exclude_hillclimb,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ExperimentFileListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    created_by: str | None = None,
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    folder: str | None = None,
    exclude_hillclimb: bool | None = False,
    x_api_key: str | None = None,
) -> ExperimentFileListResponse:
    """List versioned experiment files for the current org."""

    request_args = _build_request_args(
        created_by=created_by,
        tags=tags,
        tags_mode=tags_mode,
        folder=folder,
        exclude_hillclimb=exclude_hillclimb,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ExperimentFileListResponse.model_validate(response.json())
