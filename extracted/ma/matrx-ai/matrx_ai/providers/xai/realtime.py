"""xAI Realtime wire boundary.

This module owns xAI's provider-facing realtime URLs and the request that
creates a browser-safe client secret.  Callers retain their own authorization,
capability, and credential-envelope policy; this layer only performs the
provider wire operation.
"""

from __future__ import annotations

import httpx

CLIENT_SECRETS_URL = "https://api.x.ai/v1/realtime/client_secrets"
REALTIME_WSS_URL = "wss://api.x.ai/v1/realtime"


async def create_realtime_client_secret(
    api_key: str,
    *,
    expires_after_seconds: int,
    timeout_seconds: float,
) -> httpx.Response:
    """Create an xAI Realtime ephemeral secret without retaining the key."""
    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        return await client.post(
            CLIENT_SECRETS_URL,
            json={"expires_after": {"seconds": expires_after_seconds}},
            headers={"Authorization": f"Bearer {api_key}"},
        )
