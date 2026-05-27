"""Retag Package Image"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import RetagPackageImageRequest, RetagPackageImageResponse


def _build_request_args(
    repo: str,
    body: RetagPackageImageRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/pypi/{repo}/retag"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    repo: str,
    body: RetagPackageImageRequest,
) -> RetagPackageImageResponse:
    """Retag a package rootfs image after a package publish."""

    request_args = _build_request_args(
        repo=repo,
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return RetagPackageImageResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    repo: str,
    body: RetagPackageImageRequest,
) -> RetagPackageImageResponse:
    """Retag a package rootfs image after a package publish."""

    request_args = _build_request_args(
        repo=repo,
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return RetagPackageImageResponse.model_validate(response.json())
