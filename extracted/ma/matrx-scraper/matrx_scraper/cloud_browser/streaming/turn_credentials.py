"""coTURN short-lived REST credentials (S4 §8).

    turn_username   = "<unix_expiry>:<stream_session_id>"
    turn_credential = base64(HMAC-<digest>(<turn_shared_secret>, turn_username))
    turn_expires_at = now + TURN_CREDENTIAL_TTL_SECONDS   # 120

Rules that are load-bearing, not incidental:

- The shared secret lives ONLY on the gateway and the coTURN host. It is never in
  a ticket, a client bundle, or the worker.
- The username embeds ``stream_session_id`` (not a user id or origin) so TURN
  allocation logs correlate to a session without leaking identity.
- 120 s covers ICE gathering with margin; it is NOT the session's lifetime.
- **TURN is not a revocation surface.** Expiring a credential does not stop an
  established relay. Revocation is worker-input-kill + media teardown + gateway
  session close (S4 §6). Never rely on TURN expiry for security.

OPEN(turn-rest-hash): coTURN's classic REST mechanism uses HMAC-SHA1; if the
deployed build supports a stronger digest for this mechanism, set
``StreamingConfig.turn_rest_digest`` and it is used here. WS-4 pins the answer
from the deployed version in the runbook.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
from dataclasses import dataclass

from .config import TURN_CREDENTIAL_TTL_SECONDS, StreamingConfig


@dataclass(frozen=True)
class TurnCredential:
    username: str
    credential: str
    expires_at: int
    stun_urls: tuple[str, ...]
    turn_urls: tuple[str, ...]


def mint_turn_credential(
    cfg: StreamingConfig, *, stream_session_id: str, now: float | None = None
) -> TurnCredential:
    if not cfg.turn_shared_secret:
        # No TURN configured: return STUN-only. A restrictive NAT path then fails
        # loudly at ICE rather than silently; that is a deployment gap, not a
        # security fallback.
        return TurnCredential(
            username="",
            credential="",
            expires_at=int((now or time.time())),
            stun_urls=cfg.stun_urls,
            turn_urls=(),
        )
    expiry = int((now or time.time())) + TURN_CREDENTIAL_TTL_SECONDS
    username = f"{expiry}:{stream_session_id}"
    digest = _digest_for(cfg.turn_rest_digest)
    mac = hmac.new(
        cfg.turn_shared_secret.encode("utf-8"), username.encode("utf-8"), digest
    ).digest()
    credential = base64.b64encode(mac).decode("ascii")
    return TurnCredential(
        username=username,
        credential=credential,
        expires_at=expiry,
        stun_urls=cfg.stun_urls,
        turn_urls=cfg.turn_urls,
    )


def _digest_for(name: str):
    name = (name or "sha1").lower()
    if name == "sha1":
        return hashlib.sha1
    if name == "sha256":
        return hashlib.sha256
    raise ValueError(f"unsupported TURN REST digest {name!r}; coTURN REST is sha1 or sha256")
