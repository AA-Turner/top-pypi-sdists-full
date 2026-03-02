"""Set Session Output"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SetOutputRequest, SetOutputResponse


def _build_request_args(
    session_id: str,
    body: SetOutputRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/session/{session_id}/set-output"

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
    session_id: str,
    body: SetOutputRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SetOutputResponse:
    """Attach an output to a session by creating a SystemScoringResult.

    This allows storing extracted outputs for sessions that haven't called evaluate().
    Only works if the session doesn't already have an output attached.

    RESTRICTED TO PLATO ORG ONLY (org_id == 5)."""

    request_args = _build_request_args(
        session_id=session_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SetOutputResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    body: SetOutputRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SetOutputResponse:
    """Attach an output to a session by creating a SystemScoringResult.

    This allows storing extracted outputs for sessions that haven't called evaluate().
    Only works if the session doesn't already have an output attached.

    RESTRICTED TO PLATO ORG ONLY (org_id == 5)."""

    request_args = _build_request_args(
        session_id=session_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SetOutputResponse.model_validate(response.json())
