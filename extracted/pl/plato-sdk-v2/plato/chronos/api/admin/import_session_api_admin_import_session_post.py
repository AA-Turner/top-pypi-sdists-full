"""Import Session"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    session_id: str,
    source_url: str | None = "https://chronos.plato.so",
    force: bool | None = False,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/admin/import-session"

    params: dict[str, Any] = {}
    if session_id is not None:
        params["session_id"] = session_id
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
    session_id: str,
    source_url: str | None = "https://chronos.plato.so",
    force: bool | None = False,
    x_api_key: str | None = None,
) -> Any:
    """Import a session via SSE with progress updates."""

    request_args = _build_request_args(
        session_id=session_id,
        source_url=source_url,
        force=force,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    source_url: str | None = "https://chronos.plato.so",
    force: bool | None = False,
    x_api_key: str | None = None,
) -> Any:
    """Import a session via SSE with progress updates."""

    request_args = _build_request_args(
        session_id=session_id,
        source_url=source_url,
        force=force,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
