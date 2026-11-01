"""verify a bearer token against the API's /v1/me, with bounded accept/reject caches."""

from __future__ import annotations

import asyncio
import hashlib
import time
import weakref
from collections import OrderedDict
from typing import Any
import httpx
from ...sdk.settings.settings import resolve
from ...foundation.tls.tls import ssl_context
from probe.mcp.server.pool import _client_headers_var, _env


_PROTECTED_RESOURCE_PATH = "/.well-known/oauth-protected-resource"


def _oauth_discovery() -> dict | None:
    """OAuth discovery config, or None to disable it (self-host / static bearer).

    Enabled by default so a hosted MCP client can find the authorization server
    and start the OAuth flow. ``PROBE_MCP_OAUTH=0`` turns it off; the resource and
    authorization-server URLs are overridable for self-host."""
    if _env("MCP_OAUTH", "1") != "1":
        return None
    resource = _env("MCP_RESOURCE_URL", "https://mcp.research.prbe.ai").rstrip("/")
    auth_server = _env("MCP_AUTH_SERVER", "https://api.research.prbe.ai").rstrip("/")
    return {"resource": resource, "authorization_servers": [auth_server]}


# Rejections are cached so a client retrying a dead token costs one upstream call
# instead of one per request.
#
# Acceptances are cached too, but on a MUCH shorter clock, and the asymmetry is the
# whole design. Every hosted request pays a /v1/me round trip, and this is the only
# thing standing in front of every tool call, so an uncached accept taxes every
# healthy user on every call. What that buys, and what the short TTL is bounding:
#
#   * A revoked token keeps working for up to _ACCEPT_TTL_SECONDS. It does not get
#     DATA in that window -- the API authenticates every backend call behind this,
#     and this check is a UX affordance, not the security boundary (see
#     _upstream_rejects). It only delays the 401.
#   * That 401 is also what tells the client to re-run its headers helper and heal,
#     so healing is delayed by the same bound. This is the sharper cost of the two.
#
# Rotation is never delayed either way: a new token hashes to a new key.
_REJECT_TTL_SECONDS = 60.0
_ACCEPT_TTL_SECONDS = 15.0
_VERIFY_CACHE_MAX = 512
_verify_cache: OrderedDict[str, float] = OrderedDict()
#: token sha256 -> (expires_monotonic, identity | None). Identity is the parsed
#: /v1/me body, which this call already fetches and used to discard.
_accept_cache: OrderedDict[str, tuple[float, dict | None]] = OrderedDict()


def _remember(cache: OrderedDict, key: str, value: Any) -> None:
    """Insert, evicting the OLDEST single entry when full.

    Deliberately not clear-all. A pod serving more than _VERIFY_CACHE_MAX live tokens
    would wipe on nearly every insert, collapsing the hit rate to zero and releasing a
    synchronised herd of /v1/me calls from every in-flight caller at once -- which is
    the traffic the TTL exists to remove, arriving all at the same instant.
    """
    cache[key] = value
    cache.move_to_end(key)
    while len(cache) > _VERIFY_CACHE_MAX:
        cache.popitem(last=False)


#: One httpx client per event loop rather than one per request: a fresh AsyncClient
#: meant a TCP+TLS handshake in front of every tool call. WEAK-keyed on the loop,
#: matching _limiters_by_loop above: a dead loop and its client are collected together,
#: and the pair can never be assigned out of step the way two module globals could.
_verify_clients: weakref.WeakKeyDictionary[asyncio.AbstractEventLoop, httpx.AsyncClient] = (
    weakref.WeakKeyDictionary()
)

#: Sized so saturation SHEDS instead of stalling. httpx's default Timeout(5.0) also
#: sets the pool-acquire timeout to 5s, so a burst past max_connections would park
#: callers for five seconds and then raise PoolTimeout -- an httpx.HTTPError, which
#: this module's fail-open handler turns into "accepted". A short pool timeout keeps
#: that window small; keepalive_expiry sits above _ACCEPT_TTL_SECONDS so a quiet pod's
#: next verification still reuses the connection instead of re-handshaking.
_VERIFY_LIMITS = httpx.Limits(
    max_connections=64, max_keepalive_connections=16, keepalive_expiry=60.0
)
_VERIFY_TIMEOUT = httpx.Timeout(connect=2.0, read=5.0, write=5.0, pool=1.0)


def _verify_http_client() -> httpx.AsyncClient:
    loop = asyncio.get_running_loop()
    client = _verify_clients.get(loop)
    if client is None or client.is_closed:
        client = httpx.AsyncClient(
            base_url=resolve().base_url,
            timeout=_VERIFY_TIMEOUT,
            limits=_VERIFY_LIMITS,
            verify=ssl_context(),
            # No cookie jar. This client is shared by every tenant on the pod, and
            # /v1 resolves credentials COOKIE-FIRST (auth/dependencies._resolve_principal)
            # -- so a single Set-Cookie landing in a shared jar would make every later
            # verification authenticate as that one user. Nothing sets one today; the
            # sharing is new, so the guard goes in with it.
            cookies=None,
            follow_redirects=False,
        )
        _verify_clients[loop] = client
    return client


def identity_for_token(token: str | None) -> dict | None:
    """The cached /v1/me identity for a token, or None.

    Read-only: population is a side effect of _upstream_rejects, so the signature that
    `with_auth_and_health` injects for tests stays a plain token -> bool.
    """
    if not token:
        return None
    entry = _accept_cache.get(hashlib.sha256(token.encode()).hexdigest())
    if entry is None or entry[0] <= time.monotonic():
        return None
    return entry[1]


def _identity_from_me(body: dict) -> dict | None:
    """A build_batch identity dict from a /v1/me body, or None if it names no user."""
    user_id = body.get("user_id")
    if not user_id:
        return None
    return {
        "distinct_id": str(user_id),
        "customer_id": body.get("customer_id"),
        # Per TOKEN, so no workspace here: the hosted MCP's only workspace scope is
        # the caller's per-REQUEST workspace limit (`X-Probe-Workspace-Limit`,
        # forwarded on its API calls), which `with_auth_and_health` stamps on the
        # request's own copy of this identity. build_batch omits the key when
        # falsy, so None means "not limited / not applicable".
        "workspace_id": None,
        "authenticated": True,
    }


async def _upstream_rejects(token: str) -> bool:
    """Whether the API definitively rejects this token (401/403).

    Only a definitive rejection returns True. A timeout, connection error, or 5xx
    returns False — a transient API blip must not disconnect every MCP client, and the
    edge check is a UX affordance, not the security boundary: the API still
    authenticates the tool call behind it.
    """
    key = hashlib.sha256(token.encode()).hexdigest()
    now = time.monotonic()
    expires = _verify_cache.get(key)
    if expires is not None:
        if expires > now:
            return True
        _verify_cache.pop(key, None)  # pop, not del: a losing racer must not KeyError
    accepted = _accept_cache.get(key)
    if accepted is not None:
        if accepted[0] > now:
            return False
        _accept_cache.pop(key, None)
    try:
        headers = {"Authorization": f"Bearer {token}"}
        headers.update(_client_headers_var.get() or {})
        response = await _verify_http_client().get("/v1/me", headers=headers)
    except httpx.HTTPError:
        # Transient: neither accept nor reject is cached, so the next request asks
        # again rather than inheriting a verdict we never actually got.
        return False
    if response.status_code not in (401, 403):
        # Only a 2xx is an ANSWER. 404/429/5xx and redirects still fail open -- a
        # blip must not disconnect every client -- but they are NOT cached: caching
        # them would turn a transient upstream fault into 15 seconds of "everyone is
        # authenticated", which is a far worse failure than the extra round trip.
        if not (200 <= response.status_code < 300):
            return False
        # The body is the point now, not just the status: it carries the user_id and
        # customer_id that attribution needs, on a call we were making regardless.
        identity: dict | None = None
        try:
            body = response.json()
            if isinstance(body, dict):
                identity = _identity_from_me(body)
        except Exception:  # a 200 we cannot parse is still a valid token
            identity = None
        _remember(_accept_cache, key, (now + _ACCEPT_TTL_SECONDS, identity))
        return False
    _remember(_verify_cache, key, now + _REJECT_TTL_SECONDS)
    return True
