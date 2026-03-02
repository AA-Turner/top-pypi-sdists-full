"""Download Package"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    repo: str,
    package_name: str,
    version: str,
    filename: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/pypi/{repo}/packages/{package_name}/{version}/{filename}"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
    repo: str,
    package_name: str,
    version: str,
    filename: str,
) -> Any:
    """Download a specific package file (wheel or sdist)."""

    request_args = _build_request_args(
        repo=repo,
        package_name=package_name,
        version=version,
        filename=filename,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    repo: str,
    package_name: str,
    version: str,
    filename: str,
) -> Any:
    """Download a specific package file (wheel or sdist)."""

    request_args = _build_request_args(
        repo=repo,
        package_name=package_name,
        version=version,
        filename=filename,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
