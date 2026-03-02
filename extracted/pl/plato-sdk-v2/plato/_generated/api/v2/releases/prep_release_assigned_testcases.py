"""Prep Release Assigned Testcases"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import PrepAssignedTestcasesRequest, ReleaseResponse


def _build_request_args(
    public_id: str,
    body: PrepAssignedTestcasesRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/releases/{public_id}/prep/assigned_testcases"

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
    body: PrepAssignedTestcasesRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ReleaseResponse:
    """Prep a release with testcases assigned to the given org that don't exist on tenant.

    1. Gets all testcases in Plato assigned to this org
    2. Calls tenant to get existing testcase IDs
    3. Finds testcases that don't exist on tenant
    4. Collects linked testcase_artifacts, artifacts, and simulators
    5. Adds all to manifest and returns updated release

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
    body: PrepAssignedTestcasesRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ReleaseResponse:
    """Prep a release with testcases assigned to the given org that don't exist on tenant.

    1. Gets all testcases in Plato assigned to this org
    2. Calls tenant to get existing testcase IDs
    3. Finds testcases that don't exist on tenant
    4. Collects linked testcase_artifacts, artifacts, and simulators
    5. Adds all to manifest and returns updated release

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
