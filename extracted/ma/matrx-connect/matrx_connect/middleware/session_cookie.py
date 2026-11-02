"""The browser file-session cookie — the auth lane behind durable render URLs.

Why this exists (Arman's ruling, 2026-08-21/26): **nothing returns a signed
URL.** Private files are addressed by ``file_id`` and rendered through the
durable route ``GET /files/{id}/download?inline=1``. But an ``<img>``/
``<video>`` tag cannot send ``Authorization`` headers — so the browser needs
exactly one credential it sends automatically: an HttpOnly session cookie.

Contract:

- ``POST /files/session`` (any host mounting the files router) is called by
  an ALREADY-AUTHENTICATED client (Bearer JWT or guest fingerprint, with
  ``credentials: 'include'``). It responds with ``Set-Cookie`` carrying an
  HMAC-signed value binding the resolved ``user_id`` with an expiry — in
  TWO shapes, classic and CHIPS ``Partitioned`` (``session_cookie_headers``),
  because from the app origin this is a THIRD-PARTY cookie and browsers
  that block those keep only the partitioned copy (2026-09-16 class).
- ``AuthMiddleware`` accepts the cookie as an auth source **only** for GET
  requests on byte-serving routes (see ``COOKIE_AUTH_PATH_RE``). It can
  never authorize a mutation, an API read, or an admin surface — which is
  what makes the CSRF surface zero: the worst a cross-site ``<img>`` can do
  is render bytes the user could already see, and cross-origin pixel reads
  stay blocked by canvas tainting.
- The cookie value is ``v1.<user_id>.<exp_epoch>.<hex hmac>`` signed with
  the middleware's existing server secret (domain-separated from the guest
  fingerprint signature). No DB row, no session table — verification is a
  pure HMAC check.

The frontend re-calls ``POST /files/session`` on auth bootstrap and from an
``onError`` retry when a render 401s (cookie expired) — replacing the four
signed-URL re-mint subsystems with one cookie refresh.
"""

from __future__ import annotations

import hashlib
import hmac
import re
import time

# Cookie the browser stores for the files host. One name everywhere.
SESSION_COOKIE_NAME = "mx_files_session"

# Default lifetime: 7 days. The FE refreshes on bootstrap and on 401, so a
# shorter value only adds refresh traffic, never security (the cookie is
# HttpOnly + Secure + HMAC-bound to the user id).
SESSION_COOKIE_TTL_SECONDS = 7 * 24 * 3600

# The ONLY routes cookie auth may satisfy: GET byte-serving lanes.
#   /files/{id}/download          durable render/download route
#   /media/{id}/v/{vision_class}  vision-variant byte stream
COOKIE_AUTH_PATH_RE = re.compile(r"^/(?:files/[^/]+/download|media/[^/]+/v/[^/]+)/?$")

_DOMAIN = b"files-session|"


def mint_session_cookie_value(
    user_id: str,
    secret: bytes,
    *,
    ttl_seconds: int = SESSION_COOKIE_TTL_SECONDS,
    now: float | None = None,
) -> str:
    """Build the signed cookie value for ``user_id``."""
    if not user_id:
        raise ValueError("mint_session_cookie_value: user_id is required")
    exp = int((now if now is not None else time.time()) + ttl_seconds)
    msg = _DOMAIN + f"{user_id}|{exp}".encode()
    sig = hmac.new(secret, msg, hashlib.sha256).hexdigest()
    return f"v1.{user_id}.{exp}.{sig}"


def classify_session_cookie_value(
    value: str | None,
    secret: bytes,
    *,
    now: float | None = None,
) -> tuple[str | None, str]:
    """Verify a cookie value and say WHY it failed: ``(user_id, reason)``.

    ``reason`` is one of:

    - ``"ok"`` — valid, unexpired, signature verified; ``user_id`` is set.
    - ``"absent"`` — no cookie value at all.
    - ``"malformed"`` — not the ``v1.<user>.<exp>.<sig>`` shape.
    - ``"expired"`` — well-formed but past its expiry (routine churn; also
      reported for expired foreign cookies — an expired cookie is never
      worth an alarm regardless of who signed it).
    - ``"signature_mismatch"`` — PRESENT, structurally valid, UNEXPIRED,
      but the HMAC does not verify. That combination is exactly secret
      drift across processes/containers (the 2026-08-30 private-file
      outage class) or tampering — never a normal anonymous request.
      Callers on the auth lane must scream, not shrug.

    Never raises.
    """
    if not value:
        return None, "absent"
    parts = value.split(".")
    if len(parts) != 4 or parts[0] != "v1":
        return None, "malformed"
    _, user_id, exp_s, sig = parts
    try:
        exp = int(exp_s)
    except ValueError:
        return None, "malformed"
    if exp < (now if now is not None else time.time()):
        return None, "expired"
    msg = _DOMAIN + f"{user_id}|{exp}".encode()
    expected = hmac.new(secret, msg, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        return None, "signature_mismatch"
    return user_id, "ok"


def verify_session_cookie_value(
    value: str | None,
    secret: bytes,
    *,
    now: float | None = None,
) -> str | None:
    """Return the ``user_id`` for a valid, unexpired cookie value, else None.

    Never raises — a malformed or expired cookie is an anonymous request,
    not an error. Auth-lane callers that must distinguish secret drift from
    routine churn use ``classify_session_cookie_value`` instead.
    """
    user_id, _ = classify_session_cookie_value(value, secret, now=now)
    return user_id


def session_cookie_header(
    value: str,
    *,
    ttl_seconds: int = SESSION_COOKIE_TTL_SECONDS,
    partitioned: bool = False,
) -> str:
    """One ``Set-Cookie`` header value for the minted cookie.

    ``SameSite=None; Secure`` because the app origin (aimatrx.com) and the
    files hosts (server.app.matrxserver.com / files.matrxserver.com) are
    cross-site — the browser only attaches the cookie to ``<img>``/fetch
    requests under exactly this combination. HttpOnly keeps it out of JS.

    ``partitioned=True`` adds the CHIPS ``Partitioned`` attribute: the cookie
    is then stored under the embedding top-level site (aimatrx.com) and is
    the ONLY kind of cross-site cookie a browser that blocks third-party
    cookies will keep. See ``session_cookie_headers`` for why both shapes
    are sent.
    """
    header = (
        f"{SESSION_COOKIE_NAME}={value}; Max-Age={ttl_seconds}; Path=/; "
        "HttpOnly; Secure; SameSite=None"
    )
    return f"{header}; Partitioned" if partitioned else header


def session_cookie_headers(
    value: str, *, ttl_seconds: int = SESSION_COOKIE_TTL_SECONDS
) -> list[str]:
    """EVERY ``Set-Cookie`` header the mint route must emit — append each.

    The lane is, by construction, a third-party cookie: set on the files host
    from the app origin. Any browser mode that blocks third-party cookies
    (Chrome with the setting on, Chrome Incognito, Safari always, Brave
    always) silently discards the unpartitioned ``Set-Cookie`` while the
    mint still answers 200 — so the client believes it has a session and
    every private ``<img>`` 401s forever, with nothing reaching telemetry
    (Arman's Chrome, 2026-09-16: mint 200, render 401, re-mint 200, render
    401 — "Image unavailable"; every agent browser allowed third-party
    cookies, so every prior fix verified green and died in his).

    Two shapes, same name and value:

    - unpartitioned — top-level opens of a byte URL and engines that ignore
      ``Partitioned`` (they treat the second header as an overwrite of the
      first: harmless);
    - ``Partitioned`` — CHIPS (Chrome 114+, Firefox 131+, Safari 18.4+):
      stored and sent for cross-site ``<img>``/fetch even when third-party
      cookies are blocked.

    The verifier reads ``SESSION_COOKIE_NAME`` either way; there is one
    signature and one identity.
    """
    return [
        session_cookie_header(value, ttl_seconds=ttl_seconds),
        session_cookie_header(value, ttl_seconds=ttl_seconds, partitioned=True),
    ]


# ---------------------------------------------------------------------------
# Process-wide secret registration.
#
# The AuthMiddleware owns the server secret (it already holds one for the
# guest-fingerprint signature). It registers it here at construction so the
# session-mint route (mounted by matrx-files' router factory) can sign
# cookies without a second secret or a config back-channel.
# ---------------------------------------------------------------------------

_registered_secret: bytes | None = None
# Whether the registered secret is a per-process random fallback (True) or a
# host-injected stable value (False). Rides beside the secret so the mint
# route can tell clients the truth via ``secret_source`` — a client seeing
# "ephemeral" knows its cookie dies at the next restart / other container
# and can scream client-side instead of failing silently.
_registered_secret_is_ephemeral: bool = False


def register_session_cookie_secret(secret: bytes, *, ephemeral: bool = False) -> None:
    """Register the process-wide cookie-signing secret.

    🚨 STABLE WINS. An EPHEMERAL (per-process random) registration must NEVER
    overwrite a STABLE (host-injected) one. The 2026-08-30 production outage's
    final root cause was exactly this clobber: the app's AuthMiddleware
    registered the stable secret, then a second bare middleware instance
    (aidream's out-of-band token verifier) constructed without a secret and
    silently replaced it with its own random — different random per container,
    every private file render 401'd. Last-writer-wins is the wrong semantic
    for a process-wide secret; the honest one is:

    - stable registration always applies (idempotent; a DIFFERENT stable value
      than the current stable one logs CRITICAL — two configured sources
      disagreeing is a host misconfiguration, and the newest wins so behavior
      stays predictable);
    - ephemeral registration applies only when nothing stable is registered,
      and is REFUSED (with a warning naming this rule) when it would clobber
      a stable secret.
    """
    global _registered_secret, _registered_secret_is_ephemeral
    if ephemeral and _registered_secret is not None and not _registered_secret_is_ephemeral:
        import logging

        logging.getLogger("matrx_connect.auth").warning(
            "register_session_cookie_secret: REFUSED an ephemeral secret that "
            "would have replaced the registered STABLE secret (a second "
            "AuthMiddleware constructed without guest_fingerprint_secret). "
            "Keeping the stable secret. Pass the same stable secret to every "
            "AuthMiddleware construction to silence this."
        )
        return
    if (
        not ephemeral
        and _registered_secret is not None
        and not _registered_secret_is_ephemeral
        and _registered_secret != secret
    ):
        import logging

        logging.getLogger("matrx_connect.auth").critical(
            "register_session_cookie_secret: TWO DIFFERENT STABLE secrets "
            "registered in one process — host misconfiguration (two "
            "middlewares configured from different sources). The newest wins, "
            "but cookies minted under the previous secret are now invalid. "
            "Unify the configuration."
        )
    _registered_secret = secret
    _registered_secret_is_ephemeral = bool(ephemeral)


def get_session_cookie_secret() -> bytes:
    if _registered_secret is None:
        raise RuntimeError(
            "Session-cookie secret not registered. AuthMiddleware registers it at "
            "construction — mount the auth middleware before the files router, or "
            "call register_session_cookie_secret() explicitly in tests."
        )
    return _registered_secret


def get_session_cookie_secret_source() -> str:
    """``"stable"`` (host-injected) or ``"ephemeral"`` (per-process random
    fallback) for the registered secret. Raises like
    ``get_session_cookie_secret`` when nothing is registered."""
    if _registered_secret is None:
        raise RuntimeError(
            "Session-cookie secret not registered. AuthMiddleware registers it at "
            "construction — mount the auth middleware before the files router, or "
            "call register_session_cookie_secret() explicitly in tests."
        )
    return "ephemeral" if _registered_secret_is_ephemeral else "stable"


__all__ = [
    "SESSION_COOKIE_NAME",
    "SESSION_COOKIE_TTL_SECONDS",
    "COOKIE_AUTH_PATH_RE",
    "mint_session_cookie_value",
    "classify_session_cookie_value",
    "verify_session_cookie_value",
    "session_cookie_header",
    "session_cookie_headers",
    "register_session_cookie_secret",
    "get_session_cookie_secret",
    "get_session_cookie_secret_source",
]
