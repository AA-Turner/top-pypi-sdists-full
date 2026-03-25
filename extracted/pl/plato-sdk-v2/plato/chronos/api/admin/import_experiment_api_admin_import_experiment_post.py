"""Import Experiment"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    experiment_id: str,
    source_url: str | None = "https://chronos.plato.so",
    force: bool | None = False,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/admin/import-experiment"

    params: dict[str, Any] = {}
    if experiment_id is not None:
        params["experiment_id"] = experiment_id
    if source_url is not None:
        params["source_url"] = source_url
    if force is not None:
        params["force"] = force

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
    experiment_id: str,
    source_url: str | None = "https://chronos.plato.so",
    force: bool | None = False,
    x_api_key: str | None = None,
) -> Any:
    """Import an experiment file (with all versions, linked sessions, and configs) via SSE."""

    request_args = _build_request_args(
        experiment_id=experiment_id,
        source_url=source_url,
        force=force,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    experiment_id: str,
    source_url: str | None = "https://chronos.plato.so",
    force: bool | None = False,
    x_api_key: str | None = None,
) -> Any:
    """Import an experiment file (with all versions, linked sessions, and configs) via SSE."""

    request_args = _build_request_args(
        experiment_id=experiment_id,
        source_url=source_url,
        force=force,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
