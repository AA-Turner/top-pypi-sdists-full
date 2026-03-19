"""Auto Verify"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AppApiV2TestcaseRoutesAutoVerifyRequest, AutoVerifyResponse


def _build_request_args(
    body: AppApiV2TestcaseRoutesAutoVerifyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/testcases/auto_verify"

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
    body: AppApiV2TestcaseRoutesAutoVerifyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AutoVerifyResponse:
    """Auto-verify sessions by generating a V2ScoringConfig and validating all sessions against it.

    1. Generates a V2ScoringConfig from the selected generation session(s)
    2. Scores all non-imposter sessions -- they must all pass
    3. Scores all imposter sessions -- they must all fail"""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AutoVerifyResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: AppApiV2TestcaseRoutesAutoVerifyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AutoVerifyResponse:
    """Auto-verify sessions by generating a V2ScoringConfig and validating all sessions against it.

    1. Generates a V2ScoringConfig from the selected generation session(s)
    2. Scores all non-imposter sessions -- they must all pass
    3. Scores all imposter sessions -- they must all fail"""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AutoVerifyResponse.model_validate(response.json())
