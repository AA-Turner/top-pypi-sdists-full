"""Gemini Live ephemeral tokens (``auth_tokens``) — the direct-browser-session credential.

A browser holding one of these connects straight to
``BidiGenerateContentConstrained?access_token=<name>``. The token is single-use
(``uses=1``), must be spent on a NEW session within ``new_session_ttl`` seconds,
and LOCKS the model and the whole connect config server-side
(``live_connect_constraints``): the browser cannot swap the model, drop the
system instruction or add tools. The platform key never leaves the server.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from google import genai
from google.genai import types

#: The websocket a token is spent on (v1beta; ``?access_token=<token>`` is appended by the client).
LIVE_CONSTRAINED_WSS_URL = (
    "wss://generativelanguage.googleapis.com/ws/"
    "google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContentConstrained"
)


@dataclass(frozen=True)
class LiveAuthToken:
    token: str
    expires_at: int  # unix seconds — the session itself (resumable within it)
    new_session_expires_at: int


async def create_live_auth_token(
    api_key: str,
    *,
    model: str,
    config: types.LiveConnectConfig,
    ttl_seconds: int,
    new_session_ttl_seconds: int,
) -> LiveAuthToken:
    """Mint one single-use token locked to ``model`` + ``config``.

    ``new_session_ttl_seconds`` is how long the token may wait for its session to open; the host
    supplies it (aidream reads the ``token_broker.google_live`` knob) — this package holds no default."""
    now = dt.datetime.now(tz=dt.UTC)
    expires = now + dt.timedelta(seconds=ttl_seconds)
    new_session = now + dt.timedelta(seconds=new_session_ttl_seconds)
    client = genai.Client(api_key=api_key, http_options={"api_version": "v1beta"})
    created = await client.aio.auth_tokens.create(
        config=types.CreateAuthTokenConfig(
            uses=1,
            expire_time=expires,
            new_session_expire_time=new_session,
            live_connect_constraints=types.LiveConnectConstraints(model=model, config=config),
        )
    )
    if not created.name:
        raise RuntimeError("Google returned no ephemeral token name")
    return LiveAuthToken(
        token=created.name,
        expires_at=int(expires.timestamp()),
        new_session_expires_at=int(new_session.timestamp()),
    )


def client_connect_url() -> str:
    """The endpoint the BROKERED CLIENT opens with a minted credential (handed out with the credential).

    The platform sends nothing there itself; the provider layer still owns the address."""
    return LIVE_CONSTRAINED_WSS_URL
