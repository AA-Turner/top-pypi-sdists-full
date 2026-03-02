"""Generate Prediction"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import TestCaseGeneratePredictionRequest


def _build_request_args(
    body: TestCaseGeneratePredictionRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/testcases/generate-prediction"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    body: TestCaseGeneratePredictionRequest,
) -> Any:
    """Generate Prediction"""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    body: TestCaseGeneratePredictionRequest,
) -> Any:
    """Generate Prediction"""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
