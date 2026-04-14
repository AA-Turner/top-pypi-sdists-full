"""Execute computer actions (mouse, keyboard, screenshot)"""

from __future__ import annotations

from typing import Any

import httpx

from ...errors import raise_for_status
from ...models import ComputerRequest, ToolResult


def _build_request_args(
    body: ComputerRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/computer"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True) if hasattr(body, "model_dump") else body,
    }


def sync(
    client: httpx.Client,
    body: ComputerRequest,
) -> ToolResult:
    """Execute computer actions (mouse, keyboard, screenshot)"""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ToolResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: ComputerRequest,
) -> ToolResult:
    """Execute computer actions (mouse, keyboard, screenshot)"""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ToolResult.model_validate(response.json())
