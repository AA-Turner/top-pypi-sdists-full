"""Receive Traces"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args() -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/otel/v1/traces"

    return {
        "method": "POST",
        "url": url,
    }


def sync(
    client: httpx.Client,
) -> dict[str, Any]:
    """Receive OTLP trace data (JSON or protobuf) and store as JSON.

    Resource attributes must include:
    - plato.session.id: The Chronos session ID"""

    request_args = _build_request_args()

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
) -> dict[str, Any]:
    """Receive OTLP trace data (JSON or protobuf) and store as JSON.

    Resource attributes must include:
    - plato.session.id: The Chronos session ID"""

    request_args = _build_request_args()

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
