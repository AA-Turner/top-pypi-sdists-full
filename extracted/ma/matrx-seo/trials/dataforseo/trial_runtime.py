"""Shared Click-Play plumbing for DataForSEO trials — credentials + live execute + print."""

from __future__ import annotations

import os
from typing import Any

import rich
from matrx_utils import vcprint

from matrx_seo.providers.dataforseo.client import DataForSeoClient
from matrx_seo.providers.dataforseo.contracts import (
    DataForSeoOperationName,
    DataForSeoOperationRequest,
    DataForSeoWorkflow,
)
from matrx_seo.providers.dataforseo.transport import AsyncHttpTransport


def credentials() -> tuple[str, str]:
    email = os.environ.get("DATA_FOR_SEO_EMAIL", "").strip()
    password = os.environ.get("DATA_FOR_SEO_PASSWORD", "").strip()
    if not email or not password:
        raise RuntimeError(
            "DATA_FOR_SEO_EMAIL and DATA_FOR_SEO_PASSWORD must be set in aidream/.env"
        )
    return email, password


async def run_live(
    *,
    operation: DataForSeoOperationName,
    endpoint_label: str,
    task: dict[str, Any],
) -> dict[str, Any]:
    email, password = credentials()
    transport = AsyncHttpTransport(username=email, password=password, max_attempts=2)
    client = DataForSeoClient(transport)
    try:
        vcprint(f"\n[DATAFORSEO] {endpoint_label}", color="cyan")
        rich.print(task)
        response = await client.execute(
            DataForSeoOperationRequest(
                operation=operation,
                workflow=DataForSeoWorkflow.LIVE,
                tasks=[task],
            )
        )
        result = {
            "reported_cost": (
                str(response.reported_cost) if response.reported_cost is not None else None
            ),
            "external_task_id": response.external_task_id,
            "error": response.error,
            "raw": response.raw,
        }
        rich.print(result)
        return result
    finally:
        await transport.aclose()
