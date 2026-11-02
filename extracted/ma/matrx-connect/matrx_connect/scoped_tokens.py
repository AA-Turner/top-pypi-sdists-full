"""Scoped capability tokens — the mint/verify primitive for brokered access.

A *scoped token* is a short-lived, first-party JWT that grants a narrow
capability (an ``audience``) to one user, optionally constrained by
``scopes`` and carrying an explicit model-tier policy. It is the credential
a host's token broker hands to clients / desktop apps when they need
temporary privileged reach — the host's long-lived provider keys never
leave the server.

**This is NOT `AuthMiddleware` auth and must never be.** The middleware
accepts ONLY Supabase-signed user JWTs (see the auth contract in this
package's CLAUDE.md). Scoped tokens are verified per-route, exactly like
``service_auth`` — a gateway route that accepts them applies
``ScopedTokenIssuer.verify`` (or the ``require_scoped_token`` dependency)
explicitly. A scoped token grants access to its audience's routes and
nothing else; it is worthless on any normal API route.

Key material is injected by the host (constructor arg — never read env
here, per package rules). ES256 only: asymmetric, so a future edge data
plane (e.g. a Cloudflare Worker gateway) can verify with the public key /
JWKS without ever holding the signing key.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any

import jwt

__all__ = [
    "BoundScopedGrant",
    "ScopedGrant",
    "ScopedTokenError",
    "ScopedTokenIssuer",
]

_ALGORITHM = "ES256"


def _b64url_int(n: int) -> str:
    import base64

    return base64.urlsafe_b64encode(n.to_bytes(32, "big")).rstrip(b"=").decode("ascii")


def public_jwk_from_pem(public_key_pem: str) -> dict[str, str]:
    """The JWK (RFC 7517) of an EC P-256 public key, ``kid`` = its RFC 7638 thumbprint.

    What an out-of-process verifier (a JWKS endpoint, PowerSync) needs. The ``kid`` is stable
    for a key and changes when the key rotates, and every token this issuer mints carries it
    in its header, so a verifier holding several keys picks the right one.
    """
    import base64
    import hashlib

    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec

    key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
    if not isinstance(key, ec.EllipticCurvePublicKey) or key.curve.name != "secp256r1":
        raise ValueError("scoped-token keys are EC P-256")
    nums = key.public_numbers()
    x, y = _b64url_int(nums.x), _b64url_int(nums.y)
    thumb = hashlib.sha256(f'{{"crv":"P-256","kty":"EC","x":"{x}","y":"{y}"}}'.encode()).digest()
    kid = base64.urlsafe_b64encode(thumb).rstrip(b"=").decode("ascii")
    return {"kty": "EC", "crv": "P-256", "x": x, "y": y, "alg": _ALGORITHM, "use": "sig", "kid": kid}


class ScopedTokenError(Exception):
    """A scoped token failed verification (bad signature, wrong audience,
    expired, malformed). The message is safe to surface in a 401 detail."""


@dataclass(frozen=True)
class BoundScopedGrant:
    """A verified issuer grant retaining exact signed timestamp claims."""

    user_id: str
    issuer: str
    audience: str
    tier_policy: str
    scopes: tuple[str, ...]
    issued_at: int
    expires_at: int
    token_id: str
    claims: dict[str, Any]


@dataclass(frozen=True)
class ScopedGrant:
    """The verified content of a scoped token."""

    user_id: str
    issuer: str
    audience: str
    # Explicit model-tier fallback policy: "none" | "guest" | "mid".
    # Always present and always explicit — minting requires it with no
    # default (an unstated tier policy is a bug, not a lenient grant).
    tier_policy: str
    scopes: tuple[str, ...]
    expires_at: int  # unix seconds
    token_id: str
    claims: dict[str, Any] = field(default_factory=dict)


class ScopedTokenIssuer:
    """Mints and verifies scoped capability tokens with one ES256 keypair.

    Parameters
    ----------
    issuer : str
        The ``iss`` claim stamped on every token (e.g. ``"matrx-broker"``).
        Hosts should also pass this to ``AuthMiddleware(passthrough_issuers=...)``
        so scoped tokens fall through the global middleware silently.
    private_key_pem : str
        PEM-encoded EC P-256 private key. The host resolves it (env var,
        secret store) and injects it here.
    default_ttl_seconds / max_ttl_seconds : int
        TTL applied when the mint call doesn't specify one, and the hard
        ceiling a caller-supplied TTL is clamped to. Short by design —
        expiry IS the revocation mechanism.
    """

    def __init__(
        self,
        *,
        issuer: str,
        private_key_pem: str,
        default_ttl_seconds: int = 600,
        max_ttl_seconds: int = 3600,
    ) -> None:
        if not issuer:
            raise ValueError("ScopedTokenIssuer requires a non-empty issuer")
        if not private_key_pem:
            raise ValueError("ScopedTokenIssuer requires a private key PEM")
        self._issuer = issuer
        self._private_key_pem = private_key_pem
        self._default_ttl = int(default_ttl_seconds)
        self._max_ttl = int(max_ttl_seconds)
        # Derive the public key once — verification never touches the
        # private half again, and `public_key_pem` is what a remote data
        # plane (edge worker) would be provisioned with.
        from cryptography.hazmat.primitives import serialization

        key = serialization.load_pem_private_key(
            private_key_pem.encode("utf-8"), password=None
        )
        self._public_key_pem = (
            key.public_key()
            .public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            .decode("utf-8")
        )
        self._public_jwk = public_jwk_from_pem(self._public_key_pem)

    @property
    def issuer(self) -> str:
        return self._issuer

    @property
    def public_jwk(self) -> dict[str, str]:
        """This issuer's public key as a JWK; ``kid`` matches every minted token's header."""
        return dict(self._public_jwk)

    @property
    def public_key_pem(self) -> str:
        """PEM public key — hand this to any out-of-process verifier."""
        return self._public_key_pem

    def mint(
        self,
        *,
        user_id: str,
        audience: str,
        tier_policy: str,
        scopes: tuple[str, ...] = (),
        ttl_seconds: int | None = None,
        extra_claims: dict[str, Any] | None = None,
    ) -> tuple[str, int]:
        """Mint a scoped token. Returns ``(token, expires_at_unix)``.

        ``tier_policy`` is REQUIRED and has no default by design: the
        caller must state explicitly whether model-tier fallback applies
        ("guest" | "mid") or explicitly does not ("none").
        """
        if not user_id:
            raise ValueError("scoped token requires a user_id")
        if not audience:
            raise ValueError("scoped token requires an audience")
        if tier_policy not in ("none", "guest", "mid"):
            raise ValueError(
                f"tier_policy must be explicit — 'none' | 'guest' | 'mid', got {tier_policy!r}"
            )
        ttl = self._default_ttl if ttl_seconds is None else int(ttl_seconds)
        ttl = max(1, min(ttl, self._max_ttl))
        now = int(time.time())
        expires_at = now + ttl
        payload: dict[str, Any] = {
            "iss": self._issuer,
            "aud": audience,
            "sub": user_id,
            "iat": now,
            "exp": expires_at,
            "jti": uuid.uuid4().hex,
            "tier_policy": tier_policy,
            "scopes": list(scopes),
        }
        if extra_claims:
            # Registered claims win — extra claims can never override
            # identity, audience, or expiry.
            payload = {**extra_claims, **payload}
        token = jwt.encode(
            payload,
            self._private_key_pem,
            algorithm=_ALGORITHM,
            headers={"kid": self._public_jwk["kid"]},
        )
        return token, expires_at

    def mint_bound(
        self,
        *,
        user_id: str,
        audience: str,
        tier_policy: str,
        scopes: tuple[str, ...],
        issued_at_ms: int,
        deadline_ms: int,
        jti: str,
        extra_claims: dict[str, Any],
    ) -> str:
        """Sign a replayable, server-persisted authority with exact times.

        This is an issuer primitive only; it does not expose an HTTP mint path.
        """
        if not user_id or not audience:
            raise ValueError("bound token requires user_id and audience")
        if tier_policy not in ("none", "guest", "mid"):
            raise ValueError("bound token tier policy")
        values = (issued_at_ms, deadline_ms)
        if any(
            isinstance(value, bool) or not isinstance(value, int) or value < 0
            for value in values
        ):
            raise ValueError("bound token timestamps")
        try:
            canonical_jti = str(uuid.UUID(jti))
        except (TypeError, ValueError, AttributeError) as exc:
            raise ValueError("bound token jti") from exc
        if canonical_jti != jti:
            raise ValueError("bound token jti")
        now_ms = int(time.time() * 1000)
        if deadline_ms <= now_ms or issued_at_ms > now_ms + 5_000:
            raise ValueError("bound token current time")
        iat, exp = issued_at_ms // 1000, deadline_ms // 1000
        if exp <= iat or exp - iat > self._max_ttl:
            raise ValueError("bound token lifetime")
        reserved = {"iss", "aud", "sub", "iat", "exp", "jti", "tier_policy", "scopes"}
        if reserved & set(extra_claims):
            raise ValueError("bound token reserved claim")
        payload: dict[str, Any] = {
            "iss": self._issuer,
            "aud": audience,
            "sub": user_id,
            "iat": iat,
            "exp": exp,
            "jti": jti,
            "tier_policy": tier_policy,
            "scopes": list(scopes),
            **extra_claims,
        }
        return jwt.encode(
            payload,
            self._private_key_pem,
            algorithm=_ALGORITHM,
            headers={"kid": self._public_jwk["kid"]},
        )

    def verify_bound(self, token: str, *, audience: str) -> BoundScopedGrant:
        """Verify exact bound authority with expiry strict and iat skew <=5s."""
        try:
            decoded = jwt.decode(
                token,
                self._public_key_pem,
                algorithms=[_ALGORITHM],
                audience=audience,
                issuer=self._issuer,
                options={
                    "require": ["exp", "aud", "iss", "sub", "iat", "jti"],
                    "verify_iat": False,
                },
            )
        except jwt.InvalidTokenError as exc:
            raise ScopedTokenError("bound token rejected") from exc
        try:
            iat, exp = decoded["iat"], decoded["exp"]
            if any(
                isinstance(value, bool) or not isinstance(value, int)
                for value in (iat, exp)
            ):
                raise ValueError
            if exp <= iat or exp - iat > self._max_ttl or iat > int(time.time()) + 5:
                raise ValueError
            token_id = str(uuid.UUID(decoded["jti"]))
            if token_id != decoded["jti"]:
                raise ValueError
            tier_policy = decoded["tier_policy"]
            if tier_policy not in ("none", "guest", "mid") or not isinstance(
                decoded.get("scopes"), list
            ):
                raise ValueError
            scopes = tuple(
                scope for scope in decoded["scopes"] if isinstance(scope, str)
            )
            if len(scopes) != len(decoded["scopes"]):
                raise ValueError
        except (KeyError, TypeError, ValueError, AttributeError) as exc:
            raise ScopedTokenError("bound token rejected") from exc
        return BoundScopedGrant(
            str(decoded["sub"]),
            self._issuer,
            audience,
            tier_policy,
            scopes,
            iat,
            exp,
            token_id,
            dict(decoded),
        )

    def verify_bound_receipt(self, token: str, *, audience: str) -> BoundScopedGrant:
        """Verify a persisted receipt token without granting current authority.

        This deliberately differs from :meth:`verify_bound` only in expiry
        enforcement.  Callers must reconstruct and compare the complete
        persisted receipt and separately check current actor access; this API
        must never be used to authorize a transition or mint a new lease.
        """
        try:
            decoded = jwt.decode(
                token,
                self._public_key_pem,
                algorithms=[_ALGORITHM],
                audience=audience,
                issuer=self._issuer,
                options={
                    "require": ["exp", "aud", "iss", "sub", "iat", "jti"],
                    "verify_iat": False,
                    "verify_exp": False,
                },
            )
        except jwt.InvalidTokenError as exc:
            raise ScopedTokenError("bound receipt rejected") from exc
        try:
            iat, exp = decoded["iat"], decoded["exp"]
            if any(isinstance(value, bool) or not isinstance(value, int) for value in (iat, exp)):
                raise ValueError
            if exp <= iat or exp - iat > self._max_ttl or iat > int(time.time()) + 5:
                raise ValueError
            token_id = str(uuid.UUID(decoded["jti"]))
            if token_id != decoded["jti"]:
                raise ValueError
            tier_policy = decoded["tier_policy"]
            if tier_policy not in ("none", "guest", "mid") or not isinstance(decoded.get("scopes"), list):
                raise ValueError
            scopes = tuple(scope for scope in decoded["scopes"] if isinstance(scope, str))
            if len(scopes) != len(decoded["scopes"]):
                raise ValueError
        except (KeyError, TypeError, ValueError, AttributeError) as exc:
            raise ScopedTokenError("bound receipt rejected") from exc
        return BoundScopedGrant(
            str(decoded["sub"]), self._issuer, audience, tier_policy, scopes,
            iat, exp, token_id, dict(decoded),
        )

    def verify(self, token: str, *, audience: str) -> ScopedGrant:
        """Verify a scoped token for one exact audience. Raises
        ``ScopedTokenError`` on any failure — never returns a partial grant."""
        try:
            decoded = jwt.decode(
                token,
                self._public_key_pem,
                algorithms=[_ALGORITHM],
                audience=audience,
                issuer=self._issuer,
                options={"require": ["exp", "aud", "iss", "sub"]},
            )
        except jwt.InvalidTokenError as exc:
            raise ScopedTokenError(
                f"scoped token rejected: {type(exc).__name__}: {exc}"
            ) from exc

        tier_policy = decoded.get("tier_policy")
        if tier_policy not in ("none", "guest", "mid"):
            raise ScopedTokenError(
                f"scoped token rejected: missing/invalid tier_policy {tier_policy!r}"
            )
        raw_scopes = decoded.get("scopes")
        scopes = (
            tuple(s for s in raw_scopes if isinstance(s, str))
            if isinstance(raw_scopes, list)
            else ()
        )
        return ScopedGrant(
            user_id=str(decoded["sub"]),
            issuer=self._issuer,
            audience=audience,
            tier_policy=tier_policy,
            scopes=scopes,
            expires_at=int(decoded["exp"]),
            token_id=str(decoded.get("jti", "")),
            claims={
                k: v
                for k, v in decoded.items()
                if k not in ("iat", "exp", "nbf", "jti", "iss", "sub", "aud")
            },
        )

    def bearer_grant(self, authorization: str | None, *, audience: str) -> ScopedGrant:
        """Verify an ``Authorization: Bearer <scoped token>`` header value.
        Raises ``ScopedTokenError`` on a missing/malformed header too, so
        route code has exactly one failure type to map to 401."""
        if not authorization:
            raise ScopedTokenError("missing Authorization header")
        parts = authorization.split(None, 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise ScopedTokenError("Authorization header is not a Bearer token")
        return self.verify(parts[1].strip(), audience=audience)
