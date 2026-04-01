"""Create Test Run"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import CreateTestRunRequest, ExperimentTestRunResponse


def _build_request_args(
    version_public_id: str,
    body: CreateTestRunRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/experiments/versions/{version_public_id}/test-runs"

    headers: dict[str, str] = {}
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
    version_public_id: str,
    body: CreateTestRunRequest,
    x_api_key: str | None = None,
) -> ExperimentTestRunResponse:
    """Register a sub-experiment test run for a specific experiment version."""

    request_args = _build_request_args(
        version_public_id=version_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ExperimentTestRunResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    version_public_id: str,
    body: CreateTestRunRequest,
    x_api_key: str | None = None,
) -> ExperimentTestRunResponse:
    """Register a sub-experiment test run for a specific experiment version."""

    request_args = _build_request_args(
        version_public_id=version_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ExperimentTestRunResponse.model_validate(response.json())
