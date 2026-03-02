"""Batch Create Test Cases"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import BatchCreateTestCasesRequest, BatchCreateTestCasesResponse


def _build_request_args(
    body: BatchCreateTestCasesRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/simulator/test-cases/batch-create"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    body: BatchCreateTestCasesRequest,
) -> BatchCreateTestCasesResponse:
    """Create or update multiple test cases with artifact verification.

    This is an atomic operation - either ALL test cases succeed or ALL fail.
    If any test case fails validation or insertion, the entire batch is rolled back.

    For each test case:
    - Verifies the artifact_id exists in the database
    - Gets the simulator from the artifact
    - Creates or updates the test case (uses public_id to detect existing test cases)
    - Links the test case to the simulator

    Returns results for all test cases on success, or raises HTTPException on any failure."""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return BatchCreateTestCasesResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: BatchCreateTestCasesRequest,
) -> BatchCreateTestCasesResponse:
    """Create or update multiple test cases with artifact verification.

    This is an atomic operation - either ALL test cases succeed or ALL fail.
    If any test case fails validation or insertion, the entire batch is rolled back.

    For each test case:
    - Verifies the artifact_id exists in the database
    - Gets the simulator from the artifact
    - Creates or updates the test case (uses public_id to detect existing test cases)
    - Links the test case to the simulator

    Returns results for all test cases on success, or raises HTTPException on any failure."""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return BatchCreateTestCasesResponse.model_validate(response.json())
