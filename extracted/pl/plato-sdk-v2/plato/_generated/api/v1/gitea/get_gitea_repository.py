"""Get Gitea Repository"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import RepositoryResponse


def _build_request_args(
    owner: str,
    repo: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/gitea/repositories/{owner}/{repo}"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    owner: str,
    repo: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RepositoryResponse:
    """Get a specific Gitea repository"""

    request_args = _build_request_args(
        owner=owner,
        repo=repo,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return RepositoryResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    owner: str,
    repo: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RepositoryResponse:
    """Get a specific Gitea repository"""

    request_args = _build_request_args(
        owner=owner,
        repo=repo,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return RepositoryResponse.model_validate(response.json())
