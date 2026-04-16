"""Test Column Transform"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import RunColumnTransformRequest, RunColumnTransformResponse


def _build_request_args(
    body: RunColumnTransformRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/tools/test_column_transform"

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
    body: RunColumnTransformRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RunColumnTransformResponse:
    """Run a transform against a list of test values using the Python re engine."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return RunColumnTransformResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: RunColumnTransformRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RunColumnTransformResponse:
    """Run a transform against a list of test values using the Python re engine."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return RunColumnTransformResponse.model_validate(response.json())
