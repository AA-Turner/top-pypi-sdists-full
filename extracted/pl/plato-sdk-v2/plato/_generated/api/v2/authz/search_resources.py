"""Search Resources"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ResourceSearchResponse, ResourceType


def _build_request_args(
    resource_type: ResourceType,
    q: str | None = "",
    include_wildcard: bool | None = True,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/authz/resources"

    params: dict[str, Any] = {}
    if resource_type is not None:
        params["resource_type"] = getattr(resource_type, "value", resource_type)
    if q is not None:
        params["q"] = q
    if include_wildcard is not None:
        params["include_wildcard"] = include_wildcard

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
    resource_type: ResourceType,
    q: str | None = "",
    include_wildcard: bool | None = True,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ResourceSearchResponse:
    """Search grantable resources by name, for the grant composer's picker.

    Admin-only: it enumerates resources across every org, which is what an
    admin granting access needs and what nobody else should see."""

    request_args = _build_request_args(
        resource_type=resource_type,
        q=q,
        include_wildcard=include_wildcard,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ResourceSearchResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    resource_type: ResourceType,
    q: str | None = "",
    include_wildcard: bool | None = True,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ResourceSearchResponse:
    """Search grantable resources by name, for the grant composer's picker.

    Admin-only: it enumerates resources across every org, which is what an
    admin granting access needs and what nobody else should see."""

    request_args = _build_request_args(
        resource_type=resource_type,
        q=q,
        include_wildcard=include_wildcard,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ResourceSearchResponse.model_validate(response.json())
