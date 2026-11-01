"""one ResearchReadService per caller token: acquire, lease for a call, park on eviction, close quietly."""

from __future__ import annotations
import contextvars
import hashlib
import logging
import os
import threading
import warnings
from collections import OrderedDict
from collections.abc import Iterator
from contextlib import contextmanager

from ... import __version__
from ...foundation.request_identity.request_identity import client_version_headers
from ...sdk.client.client import Client
from ...sdk.settings.settings import Settings, load_context, resolve
from ...foundation.request_identity.surface import Surface
from ...sdk.delivery.transport.transport import Transport
from ..tools.tools import ResearchReadService
from ..source.source import ResearchOSSource

# Per-request caller token (set by the HTTP auth middleware; None under stdio).
_token_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "probe_mcp_token", default=None
)
# Validated telemetry from the current hosted MCP request.  It is separate from
# the token because it is untrusted, optional, and never participates in auth.
_client_headers_var: contextvars.ContextVar[dict[str, str] | None] = contextvars.ContextVar(
    "probe_mcp_client_headers",
    default=None,
)

# Reuse a client AND a source per distinct token: the client so we do not open
# an httpx client per call, the source because it carries the /v1/search
# capability-probe cache — a fresh source per call would re-probe (a full
# search fan-out) on every tool call, including unrelated reads. Both maps are
# LRU-bounded together (hosted multi-tenant mode must not pin one client+source
# per distinct token forever). Eviction: an IDLE evictee's httpx client is
# closed immediately; a BUSY one (in-flight lease below) is parked and closed
# by its last lease release. An evicted token re-creates on its next request.
_MAX_CACHED_TOKENS = 256
_clients: OrderedDict[str | None, Client] = OrderedDict()
_sources: OrderedDict[str | None, ResearchOSSource] = OrderedDict()
_factory_lock = threading.Lock()

# In-flight leases: with tool bodies on worker threads (_tool), LRU eviction
# can race a call that is mid-request on the evicted client. A lease pins the
# source for the duration of one tool call; eviction closes idle sources
# immediately but PARKS busy ones, and the last lease release closes them.
# Keyed by the SOURCE INSTANCE (id of a strongly-held object), never the
# token: one token can cycle through several client generations, and two
# generations must never share a slot. Guarded by _factory_lock; close()
# always happens outside the lock.
_in_flight: dict[int, int] = {}
_parked: dict[int, ResearchOSSource] = {}
# Retries on the MCP surface only (SDK default stays 3): agents retry their
# own tool calls, so the server retrying too just multiplies worker-pin time.
_MCP_MAX_RETRIES = 1

_logger = logging.getLogger("probe.mcp.server")  # the old module's name (agent:17): log filters keep matching


def _env(name: str, default: str | None = None) -> str | None:
    """Read ``PROBE_<name>``, falling back to the legacy ``ROS_<name>`` spelling
    (deprecated in the #14/#15 rename; the fallback keeps old deployments working)."""
    value = os.environ.get(f"PROBE_{name}")
    if value is not None:
        return value
    legacy = os.environ.get(f"ROS_{name}")
    if legacy is not None:
        warnings.warn(f"ROS_{name} is deprecated; set PROBE_{name} instead", stacklevel=2)
        return legacy
    return default


def _acquire_service(
    *, lease: bool
) -> tuple[ResearchReadService, ResearchOSSource, list[ResearchOSSource]]:
    """Resolve (and memoize) the per-token client+source, optionally taking an
    in-flight lease on the source, and run LRU eviction — all under ONE lock
    acquisition, so a source can never be evicted between resolution and its
    lease. Returns the sources to close; the CALLER closes them outside the
    lock (close() does network-adjacent teardown and must not hold it)."""
    token = _token_var.get() or _env("MCP_TOKEN") or load_context().get("mcp_token")
    to_close: list[ResearchOSSource] = []
    with _factory_lock:
        source = _sources.get(token)
        if source is None:
            client = _clients.get(token)
            if client is None:
                # Pass settings explicitly rather than Client(token=token): with
                # token=None, Client's resolve() would fall back to PROBE_TOKEN /
                # the context's `token` — the WRITE credential — and hand it to an
                # MCP client. The read-only boundary is the whole reason mcp_token
                # is a separate credential, so a missing one must stay missing and
                # surface as an auth error, never silently upgrade to write scope.
                #
                # Custom Transport with max_retries=1: the SDK default (3) lets
                # one tool call pin a worker thread ~130s exactly when the
                # backend is slow — and MCP callers are agents that retry
                # anyway, so server-side persistence buys latency, not
                # reliability. Worst-case pin drops to ~62s, which the
                # manifest's grace budget covers with room.
                #
                # The client identity here is THIS process's package version,
                # which is the truth under stdio: the local server ships in the
                # same distribution as the CLI, so its version is what the user
                # has installed. Without it, `surface=mcp` traffic reached the
                # backend anonymous and an MCP-only user reported no version at
                # all. Hosted, the ASGI wrapper overrides it per request with
                # the CALLER's forwarded pair, so this value never escapes as
                # somebody else's.
                #
                # The workspace limit: under stdio, this computer's own (the
                # config's). Hosted, every request binds the CALLER's forwarded
                # one (`workspace_limit.forwarded_scope`, `{}` when they sent
                # none), which the transport reads first, so a pod's own never
                # reaches anyone's request.
                ambient = resolve()
                mcp_settings = Settings(
                    base_url=ambient.base_url, token=token, workspace_limit=ambient.workspace_limit
                )
                client = Client(
                    settings=mcp_settings,
                    transport=Transport(
                        mcp_settings,
                        max_retries=_MCP_MAX_RETRIES,
                        surface=Surface.MCP.value,
                        client_headers=client_version_headers("cli", __version__),
                    ),
                    fail_open=False,
                    surface=Surface.MCP.value,
                )
                _clients[token] = client
            source = ResearchOSSource(client)
            _sources[token] = source
        # LRU: refresh both maps' recency together, then evict the stalest
        # pair(s) beyond the cap. Idle evictees are closed (by the caller);
        # busy ones are parked and closed by their last lease release.
        _clients.move_to_end(token)
        _sources.move_to_end(token)
        if lease:
            _in_flight[id(source)] = _in_flight.get(id(source), 0) + 1
        while len(_sources) > _MAX_CACHED_TOKENS:
            stale_token, stale_source = _sources.popitem(last=False)
            _clients.pop(stale_token, None)
            if _in_flight.get(id(stale_source), 0) > 0:
                _parked[id(stale_source)] = stale_source
            else:
                to_close.append(stale_source)
    return ResearchReadService(source), source, to_close


def _close_quietly(source: ResearchOSSource) -> None:
    """Teardown must never poison the caller's request or abort sibling
    closes: a failing httpx close is logged and swallowed. Anything stronger
    turns one tenant's teardown hiccup into another tenant's tool error —
    or, worse, a permanently leaked lease."""
    try:
        source.close()
    except Exception:
        _logger.warning("closing an evicted client failed (leaked socket at worst)", exc_info=True)


def _release_lease(source: ResearchOSSource) -> None:
    """Drop one in-flight lease; the last release of a PARKED (evicted while
    busy) source closes it — outside the lock."""
    close_me: ResearchOSSource | None = None
    with _factory_lock:
        key = id(source)
        remaining = _in_flight.get(key, 1) - 1
        if remaining > 0:
            _in_flight[key] = remaining
        else:
            _in_flight.pop(key, None)
            close_me = _parked.pop(key, None)
    if close_me is not None:
        _close_quietly(close_me)


def _service_from_token() -> ResearchReadService:
    """TEST SEAM — production traffic goes through ``_leased_service``.

    Build a read service bound to the current request's token (HTTP) or the
    ``PROBE_MCP_TOKEN`` (stdio), falling back to the ``mcp_token`` that
    the wizard stores. Client and source are memoized per token
    (the service itself is a stateless wrapper); the lock only guards the maps —
    a racing double-probe inside the source is idempotent and accepted.

    WARNING: the returned service holds NO lease — another thread's eviction
    can close its client mid-call. That is exactly the race `_leased_service`
    exists to prevent, so any new production caller must use that instead."""
    service, _source, to_close = _acquire_service(lease=False)
    for stale in to_close:
        _close_quietly(stale)  # closes the underlying httpx client
    return service


@contextmanager
def _leased_service() -> Iterator[ResearchReadService]:
    """`_service_from_token` plus an in-flight lease held for the duration of
    one tool call — the guard that makes LRU eviction safe under threads.

    The try/finally starts BEFORE the evictee closes: the lease was already
    taken inside `_acquire_service`, so a raising close must not skip
    `_release_lease` (that would park the leased source forever)."""
    service, source, to_close = _acquire_service(lease=True)
    try:
        for stale in to_close:
            _close_quietly(stale)
        yield service
    finally:
        _release_lease(source)


def _token_fingerprint() -> str:
    """A loggable, non-reversible handle for the current caller's token, so
    saturation and shed events are attributable to a tenant without ever
    logging the credential. None (stdio / env-token mode) logs as "local"."""
    token = _token_var.get()
    if not token:
        return "local"
    return hashlib.sha256(token.encode()).hexdigest()[:8]
