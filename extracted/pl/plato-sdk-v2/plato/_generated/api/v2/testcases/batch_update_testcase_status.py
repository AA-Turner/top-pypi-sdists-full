"""Batch Update Testcase Status"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import BatchUpdateStatusRequest, BatchUpdateStatusResponse


def _build_request_args(
    body: BatchUpdateStatusRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/testcases/status/batch"

    return {
        "method": "PUT",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    body: BatchUpdateStatusRequest,
) -> BatchUpdateStatusResponse:
    """Batch update testcase statuses.

    Internal service endpoint used by watchdog to sync review
    decisions into Plato's TestCaseStatus.

    - Testcase not found in Plato: warning (skipped)
    - No work order status for org: error
    - Already at target status: skipped (no-op)
    - Any other transition: updated"""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return BatchUpdateStatusResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: BatchUpdateStatusRequest,
) -> BatchUpdateStatusResponse:
    """Batch update testcase statuses.

    Internal service endpoint used by watchdog to sync review
    decisions into Plato's TestCaseStatus.

    - Testcase not found in Plato: warning (skipped)
    - No work order status for org: error
    - Already at target status: skipped (no-op)
    - Any other transition: updated"""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return BatchUpdateStatusResponse.model_validate(response.json())
