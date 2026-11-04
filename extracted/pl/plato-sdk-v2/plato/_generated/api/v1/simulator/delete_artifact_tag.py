"""Delete Artifact Tag"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ArtifactTagsResponse


def _build_request_args(
    tag_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/simulator/artifact-tags/{tag_name}"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "DELETE",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    tag_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ArtifactTagsResponse:
    """Delete a artifact tag definition (admin only).

    Existing simulator tag pointers with this name are left in place — the
    name simply becomes immutable again."""

    request_args = _build_request_args(
        tag_name=tag_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ArtifactTagsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    tag_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ArtifactTagsResponse:
    """Delete a artifact tag definition (admin only).

    Existing simulator tag pointers with this name are left in place — the
    name simply becomes immutable again."""

    request_args = _build_request_args(
        tag_name=tag_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ArtifactTagsResponse.model_validate(response.json())
