"""per-event-loop admission and thread limits, with the open-web sub-quota."""

from __future__ import annotations

import asyncio
import weakref

import anyio
import anyio.to_thread
from probe.mcp.server.pool import _env

# Tool execution runs on worker threads (see _tool) so the event loop — which
# serves /healthz and every kubelet probe — is never blocked by a backend
# round-trip (2026-07-30: one slow CallToolRequest starved /healthz and the
# pod was liveness-killed). Admission is bounded and sheds load explicitly:
#   _TOOL_CAPACITY   concurrent threaded tool calls per process (matches
#                    anyio's default thread-pool bound of 40);
#   _QUEUE_TIMEOUT_S a call that cannot get a worker within this raises a
#                    retryable "overloaded" error instead of queueing toward
#                    the ingress's 300s timeout;
#   _QUEUE_WARN_S    waits past this log a saturation breadcrumb, because a
#                    saturated pod otherwise looks healthy to every probe.
# Two limiters on purpose: admission is OURS, so the acquire can be timed and
# shed; the run_sync limiter merely permits the thread and is never contended
# because admission gates entry. anyio primitives bind to the running event
# loop, so both are created lazily per loop (one loop in production; tests
# create one per anyio.run). Weak-keyed by the LOOP OBJECT so a dead loop's
# entry disappears with it — an id()-keyed map handed a recycled id would give
# a new loop limiters bound to dead-loop primitives.
# Default concurrent threaded tool calls per process; PROBE_MCP_TOOL_CAPACITY
# overrides at boot (read in _limiters) so the manifest can co-tune capacity
# with the pod's CPU/memory budget without a code release.
_TOOL_CAPACITY = 40
_QUEUE_TIMEOUT_S = 20.0
_QUEUE_WARN_S = 5.0
# Literature calls can spend up to the backend's Firecrawl timeout on network
# I/O. Bound their share of the worker pool so a burst of paper reads leaves
# capacity for the lab's own records. Keep the existing deployment setting
# PROBE_MCP_WEB_CAPACITY; it now applies only to find_papers.
_WEB_CAPACITY_FRACTION = 4
_WEB_TOOLS = frozenset({"find_papers"})
# The open-web request bounds, mirrored from `app/websearch/schemas.py` so they
# reach the caller as SCHEMA. They were prose in the tool docstrings while the
# enums beside them were `$defs` -- and the docstring was wrong about one of
# them, claiming the deployment "clamps" an over-large `limit` when the endpoint
# 422s it. A bound the caller can see is a bound nobody has to be told twice.
_WEB_QUERY_CHARS = 500
_WEB_MAX_LIMIT = 50
_limiters_by_loop: weakref.WeakKeyDictionary[
    asyncio.AbstractEventLoop, tuple[anyio.CapacityLimiter, anyio.CapacityLimiter]
] = weakref.WeakKeyDictionary()
_web_limiters_by_loop: weakref.WeakKeyDictionary[
    asyncio.AbstractEventLoop, anyio.CapacityLimiter
] = weakref.WeakKeyDictionary()


def _limiters() -> tuple[anyio.CapacityLimiter, anyio.CapacityLimiter]:
    """(admission, thread) limiters for the running event loop, created on
    first use. Only ever called from the loop (inside async wrappers), so the
    lazy init cannot race. Weak-keyed per loop because anyio primitives bind
    to the loop they first await on — production has one loop for the process
    lifetime; each test's asyncio.run gets fresh limiters (and fresh capacity,
    so monkeypatching _TOOL_CAPACITY works per-test)."""
    loop = asyncio.get_running_loop()
    pair = _limiters_by_loop.get(loop)
    if pair is None:
        capacity = int(_env("MCP_TOOL_CAPACITY") or _TOOL_CAPACITY)
        pair = (anyio.CapacityLimiter(capacity), anyio.CapacityLimiter(capacity))
        _limiters_by_loop[loop] = pair
    return pair


def _web_limiter() -> anyio.CapacityLimiter:
    """The open-web sub-quota for this loop. See `_WEB_CAPACITY_FRACTION`.

    Held INSIDE the admission slot, never instead of it, so a web burst is
    bounded twice: once by the pool everyone shares and once by its own share
    of it. At least 1, so a tiny capacity (tests, a one-worker deployment) still
    serves web calls one at a time rather than never.
    """
    loop = asyncio.get_running_loop()
    limiter = _web_limiters_by_loop.get(loop)
    if limiter is None:
        override = _env("MCP_WEB_CAPACITY")
        capacity = int(_env("MCP_TOOL_CAPACITY") or _TOOL_CAPACITY)
        web = int(override) if override else max(1, capacity // _WEB_CAPACITY_FRACTION)
        limiter = anyio.CapacityLimiter(max(1, web))
        _web_limiters_by_loop[loop] = limiter
    return limiter
