from __future__ import annotations

import base64
import binascii
import json
import math
import os
import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, NamedTuple, Optional

WEB_IDENTITY_TOKEN_FILE_ENV_VAR = "CHALK_WEB_IDENTITY_TOKEN_FILE"

# Bounds how long a token read from the file is reused. Re-reading on every call
# would be wasteful, since credentials are resolved many times per client;
# caching indefinitely would miss rotations.
_MAX_TOKEN_CACHE_TTL_SECONDS = 60.0 * 60.0

# Floors the computed TTL, which shrinks toward zero as a token nears and passes
# its expiry, leaving every caller to re-read. The read happens under a
# process-wide lock and the gRPC interceptor resolves a token on every RPC, so a
# producer that falls behind would serialize the whole client on one lock held
# across a file read. The cost is that a token can be served up to a second past
# its `exp`; the clients invalidate and retry once on 401/403 or UNAUTHENTICATED.
_MIN_TOKEN_CACHE_TTL_SECONDS = 1.0


class WebIdentityTokenError(ValueError):
    """Raised when a Chalk web identity token file cannot be used."""


@dataclass(frozen=True)
class WebIdentityToken:
    """A directly usable Chalk JWT and the claims we need from it."""

    value: str
    environment_id: Optional[str]
    """The token's own environment, when it is scoped to one. User- and team-scoped
    tokens carry no `environment_id` claim and pick an environment per request."""
    expires_at: Optional[float]


class _CacheEntry(NamedTuple):
    """One memoized token and the deadline past which it stops being served."""

    token: WebIdentityToken
    serve_until: float
    """Unix seconds. Cache bookkeeping, not the JWT's ``exp``: it is the read time
    plus `_cache_ttl_seconds`, so it always falls at or before the token expires."""


def web_identity_token_file_from_env() -> Optional[str]:
    """Return the configured token file path, or None if rotating auth is not in use."""
    path = os.environ.get(WEB_IDENTITY_TOKEN_FILE_ENV_VAR)
    if path is None:
        return None
    path = path.strip()
    return path or None


def read_web_identity_token(path: str) -> WebIdentityToken:
    """Read and validate the JWT at ``path``, always hitting disk.

    Raises:
        WebIdentityTokenError: if the file is missing, empty, or does not contain
            a well-formed JWT.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            token = f.read().strip()
    except (OSError, UnicodeError) as e:
        raise WebIdentityTokenError(f"Unable to read {WEB_IDENTITY_TOKEN_FILE_ENV_VAR} file {path!r}: {e}") from e

    if not token:
        raise WebIdentityTokenError(f"{WEB_IDENTITY_TOKEN_FILE_ENV_VAR} file {path!r} is empty")

    claims = _decode_jwt_claims(token, path=path)

    # A default, not a requirement: every explicit environment outranks it in
    # `load_token`, and user- and team-scoped tokens carry no such claim. Demanding
    # one here would reject those tokens even when the caller named an environment.
    environment_id = claims.get("environment_id")
    if not isinstance(environment_id, str) or not environment_id:
        environment_id = None

    return WebIdentityToken(
        value=token,
        environment_id=environment_id,
        expires_at=_expiry_from_claims(claims, path=path),
    )


def get_web_identity_token(path: str) -> WebIdentityToken:
    """Return the current token for ``path``, re-reading once the cache deadline passes."""
    now = time.time()
    with _cache_lock:
        entry = _cache.get(path)
        if entry is not None and now < entry.serve_until:
            return entry.token

        # Read under the lock so a fan-out of threads hitting a cold cache results
        # in one file read rather than one per thread. Nothing is cached on failure.
        token = read_web_identity_token(path)

        read_at = time.time()
        _cache[path] = _CacheEntry(token, read_at + _cache_ttl_seconds(token.expires_at, read_at))
        return token


def invalidate_web_identity_token(path: str) -> None:
    with _cache_lock:
        _cache.pop(path, None)


def clear_web_identity_token_cache() -> None:
    """Drop every memoized token. For tests that exercise rotation against a stable path."""
    with _cache_lock:
        _cache.clear()


def _cache_ttl_seconds(expires_at: Optional[float], now: float) -> float:
    """Half the token's remaining life, capped at an hour and floored at a second.

    The floor covers the whole tail, not just an expired token: a fraction of a
    second of remaining life halves to a TTL short enough to re-read on nearly
    every call.
    """
    if expires_at is None:
        return _MAX_TOKEN_CACHE_TTL_SECONDS
    return max(_MIN_TOKEN_CACHE_TTL_SECONDS, min(_MAX_TOKEN_CACHE_TTL_SECONDS, (expires_at - now) / 2.0))


def _decode_jwt_claims(token: str, *, path: str) -> Dict[str, Any]:
    """Return a JWT's payload claims without verifying its signature."""
    parts = token.split(".")
    if len(parts) != 3 or not all(parts):
        raise WebIdentityTokenError(f"The JWT in {WEB_IDENTITY_TOKEN_FILE_ENV_VAR} file {path!r} is malformed")

    # JWTs use unpadded base64url, but tolerate padding rather than rejecting a
    # token a producer padded for us.
    payload = parts[1]
    try:
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        claims = json.loads(decoded)
    except (binascii.Error, ValueError) as e:
        raise WebIdentityTokenError(
            f"The JWT in {WEB_IDENTITY_TOKEN_FILE_ENV_VAR} file {path!r} has an invalid payload"
        ) from e

    if not isinstance(claims, dict):
        raise WebIdentityTokenError(
            f"The JWT in {WEB_IDENTITY_TOKEN_FILE_ENV_VAR} file {path!r} does not contain an object payload"
        )
    return claims


def _expiry_from_claims(claims: Dict[str, Any], *, path: str) -> Optional[float]:
    """Read the optional ``exp`` claim.

    Absent is fine and means the caller falls back to the maximum cache TTL.
    Present but not a finite number means the producer emitted something we
    should not silently ignore.
    """
    expiration = claims.get("exp")
    if expiration is None:
        return None
    # `isinstance(True, int)` is True in Python, so booleans must be excluded
    # explicitly rather than coerced to 1.0.
    if isinstance(expiration, bool) or not isinstance(expiration, (int, float)) or not math.isfinite(expiration):
        raise WebIdentityTokenError(
            f"The JWT in {WEB_IDENTITY_TOKEN_FILE_ENV_VAR} file {path!r} has an invalid exp claim"
        )
    return float(expiration)


# Memoized at module scope rather than per client: chalkpy builds a separate
# ChalkGRPCClient (and token refresher) per environment, and the async client is
# separate again, so a per-client cache would mean several independent reads per
# TTL window and several divergent views of "the current token". The token file
# is process-wide state, and every client reading the same path should agree.
_cache_lock = threading.Lock()
_cache: Dict[str, _CacheEntry] = {}
