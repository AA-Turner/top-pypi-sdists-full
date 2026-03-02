"""Get Session Workspace Upload Url"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    public_id: str,
    name: str | None = "workspace",
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{public_id}/workspace-upload-url"

    params: dict[str, Any] = {}
    if name is not None:
        params["name"] = name

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
    public_id: str,
    name: str | None = "workspace",
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Get a presigned PUT URL for uploading a workspace tarball."""

    request_args = _build_request_args(
        public_id=public_id,
        name=name,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    name: str | None = "workspace",
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Get a presigned PUT URL for uploading a workspace tarball."""

    request_args = _build_request_args(
        public_id=public_id,
        name=name,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
