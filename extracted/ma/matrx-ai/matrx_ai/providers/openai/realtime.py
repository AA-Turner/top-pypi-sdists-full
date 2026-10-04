"""OpenAI Realtime wire boundary.

The broker owns authorization and tier selection.  This module owns the
provider request that turns the selected session configuration into an
ephemeral client secret.
"""

from __future__ import annotations

from typing import Any

import httpx

CLIENT_SECRETS_URL = "https://api.openai.com/v1/realtime/client_secrets"
REALTIME_CALLS_URL = "https://api.openai.com/v1/realtime/calls"


async def create_realtime_client_secret(
    api_key: str,
    *,
    model: str,
    expires_after_seconds: int,
    timeout_seconds: float,
    session: dict[str, Any] | None = None,
) -> httpx.Response:
    """Create an OpenAI Realtime ephemeral secret for an already-approved model.

    ``session`` is the TRANSLATED session config (``translate_session_settings``
    output) — merged under the fixed ``type``/``model`` so a setting can never
    replace the approved model.
    """
    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        return await client.post(
            CLIENT_SECRETS_URL,
            json={
                "expires_after": {
                    "anchor": "created_at",
                    "seconds": expires_after_seconds,
                },
                "session": {**(session or {}), "type": "realtime", "model": model},
            },
            headers={"Authorization": f"Bearer {api_key}"},
        )
