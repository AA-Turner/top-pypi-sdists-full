"""The MCP `events` tool: one long-poll of the live pods' poll route, awaited on the event loop and never in the
16 threaded tool slots, under its own cap per process, so idle waits never block other tools (twin: app/live)."""

from __future__ import annotations

import asyncio
import os
import weakref
from http.cookiejar import CookieJar, DefaultCookiePolicy
from collections.abc import Sequence
from typing import Any

import anyio
import anyio.to_thread
import httpx
from mcp.server.fastmcp.exceptions import ToolError
from mcp.types import CallToolResult, TextContent

from ...foundation.request_identity.surface import tool_scope
from ...foundation.token_budget.token_budget import Budget, serialize
from ...generated.live import LiveEvent, LivePoll
from ...sdk.delivery.transport.transport import Transport
from ...sdk.events.query import make_poll_query, make_query, to_query_parameters
from ..delivery import accounting

#: The live long-poll route (CONTRACT.md "Live events").
POLL_PATH = "/v1/live/events/poll"
#: Waits one process holds at once; past it a call is refused at once. `CAPACITY_ENV` overrides it.
EVENTS_CAPACITY = 64
CAPACITY_ENV = "PROBE_MCP_EVENTS_CAPACITY"
#: The hosted MCP's in-cluster address of the live pods (agent/deploy/mcp/k8s.yaml).
LIVE_BASE_URL_ENV = "PROBE_LIVE_BASE_URL"
#: The answer may take this much longer than the wait it asked for.
WAIT_MARGIN_S = 10.0
CONNECT_TIMEOUT_S = 5.0
TOOL_NAME = "events"

_waits_by_loop: weakref.WeakKeyDictionary[asyncio.AbstractEventLoop, _Waits] = weakref.WeakKeyDictionary()


class _Waits:
    """One event loop's cap and HTTP clients, one per live address (anyio and httpx objects bind to the loop
    they first run on)."""

    def __init__(self, capacity: int) -> None:
        self.slots = anyio.CapacityLimiter(capacity)
        self.clients: dict[str, httpx.AsyncClient] = {}

    def get_client(self, base_url: str) -> httpx.AsyncClient:
        client = self.clients.get(base_url)
        if client is None:
            client = self.clients[base_url] = make_http_client(base_url)
        return client


def make_http_client(base_url: str) -> httpx.AsyncClient:
    """The client the waits to one address share, every caller's (a test swaps it for a mock transport). It keeps
    no cookies: a cookie one caller's answer set must never ride another caller's request."""
    from ...foundation.tls.tls import ssl_context

    no_cookies = CookieJar(policy=DefaultCookiePolicy(allowed_domains=[]))
    return httpx.AsyncClient(base_url=base_url, verify=ssl_context(), cookies=no_cookies)


def get_live_base_url(transport: Transport) -> str:
    """Where the live pods answer: `PROBE_LIVE_BASE_URL` (the hosted MCP's in-cluster `research-os-live`
    Service), else the API's address (its ingress sends `/v1/live` to them)."""
    return (os.environ.get(LIVE_BASE_URL_ENV) or transport.settings.base_url).rstrip("/")


async def follow_events(
    transport: Transport,
    *,
    run: str,
    project: str,
    experiment: str,
    kinds: Sequence[str] | None,
    since: int | None,
    wait: float,
    limit: int,
    token_budget: int,
) -> CallToolResult:
    """The events after `since` (at once if any wait, else the first within `wait` seconds), as much as fits
    the token budget, and where to continue."""
    accounting.note_tool(TOOL_NAME)
    try:
        query = make_poll_query(make_query(run=run, project=project, experiment=experiment, kinds=kinds),
                                since=since, wait=wait, limit=limit)
    except ValueError as exc:
        raise ToolError(f"events: {exc}") from None
    waits = _get_waits()
    try:
        waits.slots.acquire_nowait()
    except anyio.WouldBlock:
        raise ToolError(f"events: this server already holds {int(waits.slots.total_tokens)} event waits; "
                        "retry in a few seconds. Other Probe tools are unaffected.") from None
    try:
        http = waits.get_client(get_live_base_url(transport))
        poll = await _fetch_poll(http, transport, to_query_parameters(query), wait)
    finally:
        waits.slots.release()
    answer = await anyio.to_thread.run_sync(build_answer, poll, since, Budget(token_budget))
    return CallToolResult(content=[TextContent(type="text", text=serialize(answer))])


async def _fetch_poll(
    http: httpx.AsyncClient, transport: Transport, parameters: dict[str, Any], wait: float
) -> LivePoll:
    def make_headers() -> dict[str, str]:
        with tool_scope(TOOL_NAME):
            return transport.make_headers("GET", POLL_PATH)

    # Off the loop: a workspace limit named by slug is looked up once with a request of its own.
    headers = await anyio.to_thread.run_sync(make_headers)
    timeout = httpx.Timeout(wait + WAIT_MARGIN_S, connect=CONNECT_TIMEOUT_S)
    try:
        response = await http.get(POLL_PATH, params=parameters, headers=headers, timeout=timeout)
    except httpx.HTTPError as exc:
        raise ToolError(f"events: the live events server could not be reached ({type(exc).__name__}); "
                        "retry shortly") from None
    transport.check_answer(response)
    return LivePoll.model_validate_json(response.content)


def build_answer(poll: LivePoll, since: int | None, budget: Budget) -> dict[str, Any]:
    """`{events, next_since, has_more}` within the budget: events past it wait for the next call (has_more),
    and an event too big alone loses its `data`, so the cursor always moves."""
    events = [_drop_empty_parts(event) for event in poll.events]

    def make(count: int) -> dict[str, Any]:
        if count == len(events):
            return {"events": events, "next_since": poll.cursor, "has_more": poll.has_more}
        return {"events": events[:count], "next_since": poll.events[count - 1].seq if count else since,
                "has_more": True}

    if budget.fits(make(len(events))):
        return make(len(events))
    low, high = 0, len(events)  # make(low) fits, make(high) does not
    while high - low > 1:
        middle = (low + high) // 2
        low, high = (middle, high) if budget.fits(make(middle)) else (low, middle)
    if low:
        return make(low)
    first = {**events[0], "data": {}, "data_omitted": "over the token budget: read it from its route"}
    return {"events": [first], "next_since": poll.events[0].seq, "has_more": len(events) > 1 or poll.has_more}


def _drop_empty_parts(event: LiveEvent) -> dict[str, Any]:
    """The event without empty parts: refs that are null, data that is empty."""
    shaped: dict[str, Any] = {"seq": event.seq, "at": event.at.isoformat(), "kind": event.kind}
    refs = {name: str(value) for name, value in event.refs if value is not None}
    if refs:
        shaped["refs"] = refs
    if event.data:
        shaped["data"] = event.data
    return shaped


def _get_waits() -> _Waits:
    loop = asyncio.get_running_loop()
    waits = _waits_by_loop.get(loop)
    if waits is None:
        waits = _waits_by_loop[loop] = _Waits(int(os.environ.get(CAPACITY_ENV) or EVENTS_CAPACITY))
    return waits
