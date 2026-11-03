"""Get Repository Contents"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    owner: str,
    repo: str,
    path: str | None = "",
    ref: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/gitea/repositories/{owner}/{repo}/contents"

    params: dict[str, Any] = {}
    if path is not None:
        params["path"] = path
    if ref is not None:
        params["ref"] = ref

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
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
    owner: str,
    repo: str,
    path: str | None = "",
    ref: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> list[dict[str, Any]]:
    """Get contents of a repository directory or file"""

    request_args = _build_request_args(
        owner=owner,
        repo=repo,
        path=path,
        ref=ref,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    owner: str,
    repo: str,
    path: str | None = "",
    ref: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> list[dict[str, Any]]:
    """Get contents of a repository directory or file"""

    request_args = _build_request_args(
        owner=owner,
        repo=repo,
        path=path,
        ref=ref,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
