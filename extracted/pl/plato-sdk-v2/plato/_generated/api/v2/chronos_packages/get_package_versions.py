"""Get Package Versions"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import PackageVersionsResponse


def _build_request_args(
    package_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/chronos-packages/{package_name}"

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
    package_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> PackageVersionsResponse:
    """Get all versions of a specific chronos package.

    Args:
        package_name: Name of the package
        principal: Authenticated principal

    Returns:
        All versions of the package owned by the organization

    Raises:
        HTTPException: 404 if package not found"""

    request_args = _build_request_args(
        package_name=package_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return PackageVersionsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    package_name: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> PackageVersionsResponse:
    """Get all versions of a specific chronos package.

    Args:
        package_name: Name of the package
        principal: Authenticated principal

    Returns:
        All versions of the package owned by the organization

    Raises:
        HTTPException: 404 if package not found"""

    request_args = _build_request_args(
        package_name=package_name,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return PackageVersionsResponse.model_validate(response.json())
