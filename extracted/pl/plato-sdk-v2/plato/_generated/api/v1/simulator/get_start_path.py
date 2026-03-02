"""Get Start Path"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import StartPathRequest, StartPathResponse


def _build_request_args(
    body: StartPathRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/simulator/start-path"

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
    body: StartPathRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> StartPathResponse:
    """Get the start path for a test case and simulator combination.

    Checks in order:
    1. Test case start_path field (if test_case_public_id is provided)
    2. Simulator config default_start_path field

    Returns the first available start path or None if neither exists."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return StartPathResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: StartPathRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> StartPathResponse:
    """Get the start path for a test case and simulator combination.

    Checks in order:
    1. Test case start_path field (if test_case_public_id is provided)
    2. Simulator config default_start_path field

    Returns the first available start path or None if neither exists."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return StartPathResponse.model_validate(response.json())
