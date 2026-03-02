"""List Jobs"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import JobListResponse


def _build_request_args(
    service: str | None = None,
    version: str | None = None,
    organization_id: int | None = None,
    page: int | None = 1,
    page_size: int | None = 50,
    authorization: str | None = None,
    x_internal_service: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/jobs/list"

    params: dict[str, Any] = {}
    if service is not None:
        params["service"] = service
    if version is not None:
        params["version"] = version
    if organization_id is not None:
        params["organization_id"] = organization_id
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_internal_service is not None:
        headers["X-Internal-Service"] = x_internal_service
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
    service: str | None = None,
    version: str | None = None,
    organization_id: int | None = None,
    page: int | None = 1,
    page_size: int | None = 50,
    authorization: str | None = None,
    x_internal_service: str | None = None,
    x_api_key: str | None = None,
) -> JobListResponse:
    """Get a paginated list of jobs filtered by service, version, and organization ID"""

    request_args = _build_request_args(
        service=service,
        version=version,
        organization_id=organization_id,
        page=page,
        page_size=page_size,
        authorization=authorization,
        x_internal_service=x_internal_service,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return JobListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    service: str | None = None,
    version: str | None = None,
    organization_id: int | None = None,
    page: int | None = 1,
    page_size: int | None = 50,
    authorization: str | None = None,
    x_internal_service: str | None = None,
    x_api_key: str | None = None,
) -> JobListResponse:
    """Get a paginated list of jobs filtered by service, version, and organization ID"""

    request_args = _build_request_args(
        service=service,
        version=version,
        organization_id=organization_id,
        page=page,
        page_size=page_size,
        authorization=authorization,
        x_internal_service=x_internal_service,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return JobListResponse.model_validate(response.json())
