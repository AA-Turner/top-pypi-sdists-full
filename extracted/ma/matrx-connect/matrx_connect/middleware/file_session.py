"""Source-bound file credentials. Verification of the signature is not admission.

Hosts must check the signed source's current authority before serving bytes.
This codec deliberately does not extend the legacy v1 cookie verifier.
"""

from __future__ import annotations

import hashlib
import hmac
import math
import re
import time
from dataclasses import dataclass
from typing import Literal, cast
from uuid import UUID

from matrx_connect.context.app_context import AppContext

from .session_cookie import SESSION_COOKIE_TTL_SECONDS

FileSessionSource = Literal["login", "api_key", "guest"]
_DOMAIN = b"files-session-v2|"
_KEY_ID = re.compile(r"[A-Za-z0-9_-]{1,128}\Z", re.ASCII)
_SIGNATURE = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
_EXPIRY = re.compile(r"[1-9][0-9]{0,18}\Z", re.ASCII)
_MAX_VALUE_BYTES = 512


def _uuid(value: str) -> bool:
    return isinstance(value, str) and str(UUID(value)) == value


def _within_lifetime(expiry: int, current: float) -> bool:
    return current < expiry <= current + SESSION_COOKIE_TTL_SECONDS


@dataclass(frozen=True)
class FileSessionCredential:
    """Exact source selectors only; no JWT, API secret or raw fingerprint."""

    user_id: str
    source_kind: FileSessionSource
    source_id: str
    expires_at: int

    def __post_init__(self) -> None:
        if (
            not _uuid(self.user_id)
            or self.source_kind not in {"login", "api_key", "guest"}
            or not isinstance(self.source_id, str)
            or not (
                _KEY_ID.fullmatch(self.source_id)
                if self.source_kind == "api_key"
                else _uuid(self.source_id)
            )
            or type(self.expires_at) is not int
            or not 0 < self.expires_at < 10**19
        ):
            raise ValueError("Invalid file-session source binding")

    def _payload(self) -> str:
        return f"{self.user_id}|{self.source_kind}|{self.source_id}|{self.expires_at}"


def mint_bound_file_session_value(
    credential: FileSessionCredential, secret: bytes, *, now: float | None = None
) -> str:
    """Sign a future binding; the caller owns checking its current source."""
    current = time.time() if now is None else now
    if (
        not secret
        or not math.isfinite(current)
        or not _within_lifetime(credential.expires_at, current)
    ):
        raise ValueError("Cannot mint a file-session binding outside its lifetime bound")
    signature = hmac.new(
        secret, _DOMAIN + credential._payload().encode(), hashlib.sha256
    ).hexdigest()
    return (
        f"v2.{credential.user_id}.{credential.source_kind}."
        f"{credential.source_id}.{credential.expires_at}.{signature}"
    )


def classify_bound_file_session_value(
    value: str | None, secret: bytes, *, now: float | None = None
) -> tuple[FileSessionCredential | None, str]:
    """Check bounded syntax, expiry and HMAC; no live-source decision is made."""
    if not value:
        return None, "absent"
    if not isinstance(value, str) or len(value) > _MAX_VALUE_BYTES or not value.isascii():
        return None, "malformed"
    parts = value.split(".")
    if len(parts) != 6 or parts[0] != "v2":
        return None, "malformed"
    _, user, kind, source, expiry, signature = parts
    if not _EXPIRY.fullmatch(expiry) or not _SIGNATURE.fullmatch(signature) or not secret:
        return None, "malformed"
    if kind not in {"login", "api_key", "guest"}:
        return None, "malformed"
    try:
        credential = FileSessionCredential(user, cast(FileSessionSource, kind), source, int(expiry))
    except (ValueError, TypeError, AttributeError):
        return None, "malformed"
    current = time.time() if now is None else now
    if not math.isfinite(current):
        return None, "malformed"
    if credential.expires_at <= current:
        return None, "expired"
    if not _within_lifetime(credential.expires_at, current):
        return None, "malformed"
    expected = hmac.new(
        secret, _DOMAIN + credential._payload().encode(), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, signature):
        return None, "signature_mismatch"
    return credential, "ok"


def file_session_source_from_context(
    ctx: AppContext, *, ttl_seconds: int = SESSION_COOKIE_TTL_SECONDS, now: float | None = None
) -> FileSessionCredential:
    """Extract provenance carried by admission, refusing identity-only contexts.

    Guest hosts must first supply the verified guest registry row UUID in
    guest_execution_id; the raw fingerprint must never become source_id.
    The caller must still freshly check the resulting source before minting.
    """
    current = time.time() if now is None else now
    if type(ttl_seconds) is not int or ttl_seconds <= 0 or not math.isfinite(current):
        raise ValueError("Invalid file-session lifetime")
    deadline = int(current + min(ttl_seconds, SESSION_COOKIE_TTL_SECONDS))
    if ctx.auth_type == "token" and ctx.is_authenticated:
        claims = ctx.metadata.get("jwt_claims")
        if not isinstance(claims, dict):
            raise ValueError("File session needs verified login provenance")
        kind: FileSessionSource = "login"
        source = claims.get("session_id")
        expiry = ctx.metadata.get("jwt_expires_at")
        if type(expiry) is not int:
            raise ValueError("File session needs verified login expiry")
        deadline = min(deadline, expiry)
    elif ctx.auth_type == "api_key" and ctx.is_authenticated:
        kind = "api_key"
        source = ctx.metadata.get("api_key_id")
        if "api_key_expires_at" not in ctx.metadata:
            raise ValueError("File session needs resolved API-key expiry")
        expiry = ctx.metadata["api_key_expires_at"]
        if expiry is not None:
            if type(expiry) is not int:
                raise ValueError("Invalid resolved API-key expiry")
            deadline = min(deadline, expiry)
    elif ctx.auth_type == "fingerprint":
        kind = "guest"
        source = ctx.metadata.get("guest_execution_id")
    else:
        raise ValueError("File session needs admitted source provenance")
    if not isinstance(source, str) or deadline <= current:
        raise ValueError("Missing or expired file-session source")
    return FileSessionCredential(ctx.user_id, kind, source, deadline)
