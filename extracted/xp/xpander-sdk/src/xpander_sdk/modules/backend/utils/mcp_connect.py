"""Preflight connectivity for remote MCP servers.

agno's MCPTools swallows connect failures (the real transport error dies inside
the anyio task group and only "Cancelled via cancel scope" surfaces), so agents
silently run without their MCP tools. Probing with a short-lived session
surfaces the real error and lets the caller heal a stale OAuth token first.
"""

import asyncio
import hashlib
import time
from os import getenv
from typing import Dict, Optional

import httpx

# Hard cap on the preflight probe. A healthy MCP connects in <1s; anything longer
# is a hung/broken server and must not stall child startup. Env-tunable.
PROBE_OVERALL_TIMEOUT = int(getenv("XPANDER_MCP_PROBE_TIMEOUT", "10"))

# Master switch for the cross-task probe reuse cache. When False, every task
# re-probes each MCP server fresh (no healthy/failed marker reuse). Flip to True
# to re-enable the PRO-1951 optimization.
PROBE_CACHE_ENABLED = False

# How long a successful preflight stays trusted for a given (agent, server, token).
# A remote MCP re-connects on every agno run anyway, so this only governs how long
# we skip the *redundant* preflight probe; kept short so a server-side idle timeout
# or a rotated token is re-checked within the window.
PROBE_CACHE_TTL_SECONDS = 30.0

# Process-wide "recently healthy" markers: key -> monotonic expiry. Keyed on the
# auth header too, so a token refresh (new Authorization) is a cache miss and
# re-probes. Only successful probes are recorded.
_probe_ready_until: Dict[str, float] = {}

# Short-TTL "recently failed" markers so a persistently-bad server (timeout/403)
# is skipped fast instead of every task re-paying the full probe timeout.
PROBE_FAIL_TTL_SECONDS = float(getenv("XPANDER_MCP_PROBE_FAIL_TTL", "60"))
_probe_failed_until: Dict[str, float] = {}


def _probe_cache_key(agent_id: str, url: str, headers: Optional[Dict]) -> str:
    """Stable per (agent, server, auth-token) key; token folded into a digest, never stored raw."""
    token = (headers or {}).get("Authorization", "")
    return hashlib.sha256(f"{agent_id}|{url}|{token}".encode()).hexdigest()[:16]


def probe_recently_ok(agent_id: str, url: str, headers: Optional[Dict]) -> bool:
    """True when a prior task already confirmed this exact (agent, server, token) is healthy."""
    if not PROBE_CACHE_ENABLED:
        return False
    if not agent_id:
        return False
    expiry = _probe_ready_until.get(_probe_cache_key(agent_id, url, headers))
    return expiry is not None and expiry > time.monotonic()


def mark_probe_ok(agent_id: str, url: str, headers: Optional[Dict]) -> None:
    """Record a healthy preflight so sibling/subsequent tasks can skip the redundant probe."""
    if not PROBE_CACHE_ENABLED:
        return
    if not agent_id:
        return
    _probe_ready_until[_probe_cache_key(agent_id, url, headers)] = (
        time.monotonic() + PROBE_CACHE_TTL_SECONDS
    )


def probe_recently_failed(agent_id: str, url: str, headers: Optional[Dict]) -> bool:
    """True when a recent task already found this exact (agent, server, token) unreachable."""
    if not PROBE_CACHE_ENABLED:
        return False
    if not agent_id:
        return False
    expiry = _probe_failed_until.get(_probe_cache_key(agent_id, url, headers))
    return expiry is not None and expiry > time.monotonic()


def mark_probe_failed(agent_id: str, url: str, headers: Optional[Dict]) -> None:
    """Record a non-auth preflight failure so sibling/subsequent tasks skip the re-probe."""
    if not PROBE_CACHE_ENABLED:
        return
    if not agent_id:
        return
    _probe_failed_until[_probe_cache_key(agent_id, url, headers)] = (
        time.monotonic() + PROBE_FAIL_TTL_SECONDS
    )


def clear_probe_cache() -> None:
    """Drop all healthy + failed markers (test hook; safe to call anytime)."""
    _probe_ready_until.clear()
    _probe_failed_until.clear()


def extract_real_mcp_error(exc: BaseException) -> BaseException:
    """Unwrap anyio ExceptionGroup noise down to the error that failed the connect."""
    leaves = []

    def _walk(e: BaseException) -> None:
        subs = getattr(
            e, "exceptions", None
        )  # duck-typed: BaseExceptionGroup is py3.11+
        if isinstance(subs, (list, tuple)) and subs:
            for sub in subs:
                _walk(sub)
        else:
            leaves.append(e)

    _walk(exc)
    for leaf in leaves:
        if isinstance(leaf, httpx.HTTPStatusError):
            return leaf
    for leaf in leaves:
        if not isinstance(leaf, (GeneratorExit, asyncio.CancelledError)):
            return leaf
    return exc


def is_mcp_auth_error(exc: BaseException) -> bool:
    """True when the server rejected our credentials (token stale/revoked)."""
    return (
        isinstance(exc, httpx.HTTPStatusError)
        and exc.response is not None
        and exc.response.status_code in (401, 403)
    )


async def probe_mcp_server(
    url: str,
    headers: Optional[Dict] = None,
    transport: str = "streamable-http",
) -> Optional[BaseException]:
    """Open a short-lived MCP session; return the real error on failure, None when healthy."""
    from mcp import ClientSession

    async def _probe() -> None:
        if transport == "sse":
            from mcp.client.sse import sse_client

            ctx = sse_client(url=url, headers=headers or {})
        else:
            from mcp.client.streamable_http import streamablehttp_client

            ctx = streamablehttp_client(url=url, headers=headers or {})

        async with ctx as streams:
            read, write = streams[0], streams[1]
            async with ClientSession(read, write) as session:
                await session.initialize()

    try:
        await asyncio.wait_for(_probe(), timeout=PROBE_OVERALL_TIMEOUT)
        return None
    except BaseException as e:
        return extract_real_mcp_error(e)
