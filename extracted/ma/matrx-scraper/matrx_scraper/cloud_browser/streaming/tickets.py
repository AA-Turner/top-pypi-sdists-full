"""Stream-ticket mint/verify — a thin, reuse-first wrapper over the platform's
`ScopedTokenIssuer` (matrx-connect), NOT a second JWT signer.

A stream ticket is a scoped, short-lived, single-audience capability credential.
The platform already has exactly that primitive, signing ES256 tokens for the
token broker. We reuse it with our OWN issuer name, OWN audience, and OWN key.
A hand-rolled ticket format is a defect (S4 §0).

`matrx_connect` is a Tier-2 optional dep of this package, so it is imported
lazily inside the constructor — never at module top level of a core file
(package boundary rules). For standalone tests the host passes a locally
generated EC P-256 key; nothing here reads env.

Authority: contracts/S4-stream-tickets.md §0, §3.1.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import (
    SCOPE_AUDIO,
    SCOPE_INPUT,
    SCOPE_VIDEO,
    STREAM_AUDIENCE,
    STREAM_ISSUER_NAME,
    TICKET_MAX_TTL,
    TICKET_TTL_SECONDS,
)
from .errors import STREAM_TICKET_EXPIRED, STREAM_TICKET_INVALID, StreamError


@dataclass(frozen=True)
class TicketClaims:
    """The verified content of a stream ticket — what was ASKED FOR. Never the
    authorization answer itself (that is re-derived at claim, S4 §3.2 B7)."""

    user_id: str
    jti: str
    expires_at: int
    scopes: tuple[str, ...]
    origin: str
    profile_id: str
    run_id: str
    handoff_id: str | None
    control_revision: int | None
    grant_revision: int
    access_level: str
    mode: str
    worker_id: str
    stream_session_id: str

    @property
    def allows_input(self) -> bool:
        return SCOPE_INPUT in self.scopes


class TicketSigner:
    """Mints and verifies browser-stream tickets over ONE ES256 keypair.

    The key is injected (host resolves ``BROWSER_STREAM_TOKEN_SIGNING_KEY``);
    this class never touches env. Unset key is caught upstream in
    :meth:`StreamingConfig.require_signing_key` and 503s the route.
    """

    def __init__(self, *, private_key_pem: str) -> None:
        # Lazy import keeps matrx-connect out of the core import graph.
        from matrx_connect.scoped_tokens import ScopedTokenError, ScopedTokenIssuer

        self._ScopedTokenError = ScopedTokenError
        self._issuer = ScopedTokenIssuer(
            issuer=STREAM_ISSUER_NAME,
            private_key_pem=private_key_pem,
            default_ttl_seconds=TICKET_TTL_SECONDS,
            max_ttl_seconds=TICKET_MAX_TTL,
        )

    @property
    def public_key_pem(self) -> str:
        return self._issuer.public_key_pem

    def mint(
        self,
        *,
        user_id: str,
        origin: str,
        profile_id: str,
        run_id: str,
        handoff_id: str | None,
        control_revision: int | None,
        grant_revision: int,
        access_level: str,
        mode: str,
        worker_id: str,
        stream_session_id: str,
        audio_allowed: bool,
    ) -> tuple[str, int]:
        """Return ``(ticket, expires_at)``. Scopes and the mtx_* extra claims
        follow S4 §3.1 exactly. `tier_policy="none"` is the contract (no model
        is involved), passed explicitly, never a placeholder to remove."""
        scopes: list[str] = [SCOPE_VIDEO]
        if audio_allowed:
            scopes.append(SCOPE_AUDIO)
        if mode == "control":
            scopes.append(SCOPE_INPUT)

        # mtx_-prefixed so a reader tells platform claims from ours. No claim
        # ever carries a worker address/port, profile path, visited site origin,
        # account label, credential ref, or page title (S4 §3.1).
        extra: dict[str, Any] = {
            "mtx_origin": origin,
            "mtx_profile_id": profile_id,
            "mtx_run_id": run_id,
            "mtx_handoff_id": handoff_id,
            "mtx_control_revision": control_revision,
            "mtx_grant_revision": grant_revision,
            "mtx_access_level": access_level,
            "mtx_mode": mode,
            "mtx_worker_id": worker_id,
            "mtx_stream_session_id": stream_session_id,
        }
        return self._issuer.mint(
            user_id=user_id,
            audience=STREAM_AUDIENCE,
            tier_policy="none",
            scopes=tuple(scopes),
            extra_claims=extra,
        )

    def verify(self, token: str) -> TicketClaims:
        """Verify signature, issuer, audience, expiry (B1). Raises StreamError
        with the typed code the gateway surfaces. This does NOT re-derive access
        — B7 does that against the live resolver."""
        try:
            grant = self._issuer.verify(token, audience=STREAM_AUDIENCE)
        except self._ScopedTokenError as exc:
            # jwt.ExpiredSignatureError is wrapped inside ScopedTokenError; the
            # class name is in the message.
            msg = str(exc)
            if "Expired" in msg or "expired" in msg:
                raise StreamError(STREAM_TICKET_EXPIRED, "stream ticket expired") from exc
            raise StreamError(STREAM_TICKET_INVALID, "stream ticket rejected") from exc

        c = grant.claims
        return TicketClaims(
            user_id=grant.user_id,
            jti=grant.token_id,
            expires_at=grant.expires_at,
            scopes=grant.scopes,
            origin=str(c.get("mtx_origin", "")),
            profile_id=str(c.get("mtx_profile_id", "")),
            run_id=str(c.get("mtx_run_id", "")),
            handoff_id=(str(c["mtx_handoff_id"]) if c.get("mtx_handoff_id") else None),
            control_revision=(
                int(c["mtx_control_revision"])
                if c.get("mtx_control_revision") is not None
                else None
            ),
            grant_revision=int(c.get("mtx_grant_revision", -1)),
            access_level=str(c.get("mtx_access_level", "")),
            mode=str(c.get("mtx_mode", "")),
            worker_id=str(c.get("mtx_worker_id", "")),
            stream_session_id=str(c.get("mtx_stream_session_id", "")),
        )
