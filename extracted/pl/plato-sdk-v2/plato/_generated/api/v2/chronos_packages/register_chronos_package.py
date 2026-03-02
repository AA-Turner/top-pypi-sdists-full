"""Register Chronos Package"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import RegisterPackageRequest, RegisterPackageResponse


def _build_request_args(
    body: RegisterPackageRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/chronos-packages/register"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    body: RegisterPackageRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RegisterPackageResponse:
    """Register a deployed chronos package in the artifacts database.

    Validation rules:
    1. If package_name exists with different org_id -> reject (403)
    2. If package_name exists with same org_id but different version -> allow (new version)
    3. If package_name + version exists -> reject (409)
    4. If package_name is new -> allow

    Args:
        request: Package registration details
        principal: Authenticated principal

    Returns:
        Registration confirmation with artifact ID

    Raises:
        HTTPException: 403 if package owned by different org, 409 if version exists"""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return RegisterPackageResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: RegisterPackageRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RegisterPackageResponse:
    """Register a deployed chronos package in the artifacts database.

    Validation rules:
    1. If package_name exists with different org_id -> reject (403)
    2. If package_name exists with same org_id but different version -> allow (new version)
    3. If package_name + version exists -> reject (409)
    4. If package_name is new -> allow

    Args:
        request: Package registration details
        principal: Authenticated principal

    Returns:
        Registration confirmation with artifact ID

    Raises:
        HTTPException: 403 if package owned by different org, 409 if version exists"""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return RegisterPackageResponse.model_validate(response.json())
