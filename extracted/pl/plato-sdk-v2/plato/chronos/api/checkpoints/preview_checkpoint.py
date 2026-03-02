"""Preview Checkpoint"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import PreviewResponse


def _build_request_args(
    checkpoint_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/checkpoints/{checkpoint_id}/preview"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    checkpoint_id: str,
    x_api_key: str | None = None,
) -> PreviewResponse:
    """Launch a preview session from a checkpoint.

    Creates an ephemeral Plato session using the checkpoint's artifact IDs.
    Returns serialized session data that can be used with Session.load()
    to send heartbeats and eventually close the session.

    The frontend should:
    1. Call this endpoint to get the serialized session
    2. Use Session.load(serialized_session) to restore the session
    3. Call session.start_heartbeat() to keep envs alive
    4. Display env URLs/job IDs in a modal
    5. Call session.stop_heartbeat() and session.close() when done"""

    request_args = _build_request_args(
        checkpoint_id=checkpoint_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return PreviewResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    checkpoint_id: str,
    x_api_key: str | None = None,
) -> PreviewResponse:
    """Launch a preview session from a checkpoint.

    Creates an ephemeral Plato session using the checkpoint's artifact IDs.
    Returns serialized session data that can be used with Session.load()
    to send heartbeats and eventually close the session.

    The frontend should:
    1. Call this endpoint to get the serialized session
    2. Use Session.load(serialized_session) to restore the session
    3. Call session.start_heartbeat() to keep envs alive
    4. Display env URLs/job IDs in a modal
    5. Call session.stop_heartbeat() and session.close() when done"""

    request_args = _build_request_args(
        checkpoint_id=checkpoint_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return PreviewResponse.model_validate(response.json())
