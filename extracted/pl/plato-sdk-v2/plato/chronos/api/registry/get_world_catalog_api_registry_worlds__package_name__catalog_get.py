"""Get World Catalog"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import WorldCatalogDetailResponse


def _build_request_args(
    package_name: str,
    version: str | None = None,
    allow_prerelease: bool | None = False,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/registry/worlds/{package_name}/catalog"

    params: dict[str, Any] = {}
    if version is not None:
        params["version"] = version
    if allow_prerelease is not None:
        params["allow_prerelease"] = allow_prerelease

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    package_name: str,
    version: str | None = None,
    allow_prerelease: bool | None = False,
) -> WorldCatalogDetailResponse:
    """List all worlds within a package.

    For catalog-format packages (multiple worlds), returns each world entry.
    For single-world packages, returns a list with one entry."""

    request_args = _build_request_args(
        package_name=package_name,
        version=version,
        allow_prerelease=allow_prerelease,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WorldCatalogDetailResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    package_name: str,
    version: str | None = None,
    allow_prerelease: bool | None = False,
) -> WorldCatalogDetailResponse:
    """List all worlds within a package.

    For catalog-format packages (multiple worlds), returns each world entry.
    For single-world packages, returns a list with one entry."""

    request_args = _build_request_args(
        package_name=package_name,
        version=version,
        allow_prerelease=allow_prerelease,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WorldCatalogDetailResponse.model_validate(response.json())
