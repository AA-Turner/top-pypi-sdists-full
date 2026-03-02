"""Auto Verify Testcase"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AutoVerifyRequest


def _build_request_args(
    body: AutoVerifyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/testcases/auto-verify"

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
    body: AutoVerifyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Auto-verify a testcase by comparing scoring results between correct sessions and imposter sessions.

    This endpoint:
    1. Generates (or uses provided) scoring config from non-imposter sessions
    2. Validates all non-imposter sessions pass with that config
    3. Validates all imposter sessions FAIL with that config
    4. Returns the scoring config + ignore table used during generation

    RESTRICTED TO PLATO ORG ONLY (org_id == 5)."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    body: AutoVerifyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Auto-verify a testcase by comparing scoring results between correct sessions and imposter sessions.

    This endpoint:
    1. Generates (or uses provided) scoring config from non-imposter sessions
    2. Validates all non-imposter sessions pass with that config
    3. Validates all imposter sessions FAIL with that config
    4. Returns the scoring config + ignore table used during generation

    RESTRICTED TO PLATO ORG ONLY (org_id == 5)."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
