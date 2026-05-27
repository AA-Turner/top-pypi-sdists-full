"""List Simulator Artifacts"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ListSimulatorArtifactsResponse


def _build_request_args(
    name: str,
    testcases_only: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/simulators/{name}/artifacts"

    params: dict[str, Any] = {}
    if testcases_only is not None:
        params["testcases_only"] = testcases_only

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
    name: str,
    testcases_only: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ListSimulatorArtifactsResponse:
    """List artifacts for the given simulator.

    When testcases_only=false (default), returns all artifacts for the simulator.
    When testcases_only=true, returns only artifacts that have at least one
    testcase linked via the test_case_artifacts junction table."""

    request_args = _build_request_args(
        name=name,
        testcases_only=testcases_only,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ListSimulatorArtifactsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    name: str,
    testcases_only: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ListSimulatorArtifactsResponse:
    """List artifacts for the given simulator.

    When testcases_only=false (default), returns all artifacts for the simulator.
    When testcases_only=true, returns only artifacts that have at least one
    testcase linked via the test_case_artifacts junction table."""

    request_args = _build_request_args(
        name=name,
        testcases_only=testcases_only,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ListSimulatorArtifactsResponse.model_validate(response.json())
