"""Worker inbound auth (S2 §2.2) — a thin verifier seam, not a second issuer.

In production the Browser Manager mints scoped ES256 JWTs through the existing
``matrx_connect.ScopedTokenIssuer`` and the worker verifies them with the public
key. That crypto is a host concern; this package must run standalone, so the worker
holds an injected ``TokenVerifier``. The control plane (real or ``StubControlPlane``)
provides the matching issuer.

``InMemoryTokenAuthority`` is the stub's issuer+verifier pair: it mints opaque
capability tokens and verifies audience (``worker:{worker_id}``), operation
(``mtx_op``), expiry, and single-use ``jti`` replay — exactly the claims S2 §2.2
requires — with zero external crypto. It is NOT for production; the real worker is
handed a JWT verifier instead.
"""

from __future__ import annotations

import secrets
import time
from dataclasses import dataclass, field
from typing import Protocol

import jwt

from matrx_scraper.cloud_browser.worker.errors import WorkerProtocolError


@dataclass(frozen=True)
class WorkerCredential:
    """The verified facts of one inbound call's bearer token."""

    worker_id: str
    run_id: str
    profile_id: str
    op: str
    jti: str


class TokenVerifier(Protocol):
    def verify(self, bearer: str, *, worker_id: str, op: str) -> WorkerCredential:
        """Return the verified credential, or raise ``WorkerProtocolError`` with one
        of ``unauthorized_worker_call`` / ``audience_mismatch`` / ``credential_expired``
        / ``credential_replayed``."""
        ...


@dataclass
class Es256WorkerTokenVerifier:
    """Verify short-lived, operation-bound worker calls with a public key."""

    issuer: str
    public_key_pem: str
    _spent_jti: dict[str, float] = field(default_factory=dict)

    def verify(self, bearer: str, *, worker_id: str, op: str) -> WorkerCredential:
        if not bearer:
            raise WorkerProtocolError("unauthorized_worker_call", message="missing token")
        try:
            claims = jwt.decode(
                bearer,
                self.public_key_pem,
                algorithms=["ES256"],
                audience=f"worker:{worker_id}",
                issuer=self.issuer,
                options={"require": ["exp", "aud", "iss", "sub", "jti"]},
            )
        except jwt.ExpiredSignatureError as exc:
            raise WorkerProtocolError("credential_expired", message="token expired") from exc
        except jwt.InvalidAudienceError as exc:
            raise WorkerProtocolError(
                "audience_mismatch", message="token audience mismatch"
            ) from exc
        except jwt.InvalidTokenError as exc:
            raise WorkerProtocolError("unauthorized_worker_call", message="token rejected") from exc

        if claims.get("mtx_op") != op:
            raise WorkerProtocolError(
                "unauthorized_worker_call", message="token operation mismatch"
            )
        run_id = str(claims.get("run_id") or "")
        profile_id = str(claims.get("profile_id") or "")
        if not run_id or not profile_id:
            raise WorkerProtocolError("unauthorized_worker_call", message="token scope incomplete")

        now = time.time()
        self._spent_jti = {key: expiry for key, expiry in self._spent_jti.items() if expiry >= now}
        jti = str(claims["jti"])
        if jti in self._spent_jti:
            raise WorkerProtocolError("credential_replayed", message="token already used")
        self._spent_jti[jti] = float(claims["exp"])
        return WorkerCredential(
            worker_id=worker_id,
            run_id=run_id,
            profile_id=profile_id,
            op=op,
            jti=jti,
        )


@dataclass
class InMemoryTokenAuthority:
    """Stub issuer+verifier. Tokens are random opaque strings mapped to their claims
    in-process; nothing crosses a network. Single-use ``jti`` replay is enforced."""

    default_ttl_s: float = 120.0
    _claims: dict[str, dict[str, object]] = field(default_factory=dict)
    _spent_jti: set[str] = field(default_factory=set)

    def mint(
        self,
        *,
        worker_id: str,
        run_id: str,
        profile_id: str,
        op: str,
        ttl_s: float | None = None,
    ) -> str:
        token = secrets.token_urlsafe(24)
        self._claims[token] = {
            "aud": f"worker:{worker_id}",
            "sub": f"run:{run_id}",
            "profile": profile_id,
            "op": op,
            "jti": secrets.token_hex(8),
            "exp": time.time() + (ttl_s if ttl_s is not None else self.default_ttl_s),
        }
        return token

    def mint_expired(self, *, worker_id: str, run_id: str, profile_id: str, op: str) -> str:
        token = self.mint(
            worker_id=worker_id, run_id=run_id, profile_id=profile_id, op=op, ttl_s=-1
        )
        return token

    def verify(self, bearer: str, *, worker_id: str, op: str) -> WorkerCredential:
        claims = self._claims.get(bearer)
        if claims is None:
            raise WorkerProtocolError(
                "unauthorized_worker_call", message="unknown or missing token"
            )
        if claims["aud"] != f"worker:{worker_id}":
            raise WorkerProtocolError("audience_mismatch", message="token audience mismatch")
        if claims["op"] != op:
            raise WorkerProtocolError(
                "unauthorized_worker_call", message="token operation mismatch"
            )
        if float(claims["exp"]) < time.time():  # type: ignore[arg-type]
            raise WorkerProtocolError("credential_expired", message="token expired")
        jti = str(claims["jti"])
        if jti in self._spent_jti:
            raise WorkerProtocolError("credential_replayed", message="token already used")
        self._spent_jti.add(jti)
        return WorkerCredential(
            worker_id=worker_id,
            run_id=str(claims["sub"]).removeprefix("run:"),
            profile_id=str(claims["profile"]),
            op=op,
            jti=jti,
        )
