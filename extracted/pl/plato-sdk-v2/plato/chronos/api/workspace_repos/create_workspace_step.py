"""Create Workspace Step"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import CreateStepRequest, CreateStepResponse


def _build_request_args(
    session_public_id: str,
    body: CreateStepRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/sessions/{session_public_id}/create-step"

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
    session_public_id: str,
    body: CreateStepRequest,
    x_api_key: str | None = None,
) -> CreateStepResponse:
    """Create a new step with files. Works for both empty branches and existing branches.

    If base_ref_public_id is provided, inherits that ref's manifest and overlays the new files.
    Otherwise creates a fresh manifest from scratch."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return CreateStepResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    body: CreateStepRequest,
    x_api_key: str | None = None,
) -> CreateStepResponse:
    """Create a new step with files. Works for both empty branches and existing branches.

    If base_ref_public_id is provided, inherits that ref's manifest and overlays the new files.
    Otherwise creates a fresh manifest from scratch."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return CreateStepResponse.model_validate(response.json())
