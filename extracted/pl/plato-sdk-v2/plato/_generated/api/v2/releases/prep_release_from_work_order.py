"""Prep Release From Work Order"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import PrepFromWorkOrderRequest, ReleaseResponse


def _build_request_args(
    public_id: str,
    body: PrepFromWorkOrderRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/releases/{public_id}/prep/work_order"

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
    public_id: str,
    body: PrepFromWorkOrderRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ReleaseResponse:
    """Prep a release with selected testcases from a work order.

    Allows granular selection of individual testcases to include in the release.
    Collects linked testcase_artifacts, artifacts, and simulators automatically.

    Admin only."""

    request_args = _build_request_args(
        public_id=public_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ReleaseResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    body: PrepFromWorkOrderRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ReleaseResponse:
    """Prep a release with selected testcases from a work order.

    Allows granular selection of individual testcases to include in the release.
    Collects linked testcase_artifacts, artifacts, and simulators automatically.

    Admin only."""

    request_args = _build_request_args(
        public_id=public_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ReleaseResponse.model_validate(response.json())
