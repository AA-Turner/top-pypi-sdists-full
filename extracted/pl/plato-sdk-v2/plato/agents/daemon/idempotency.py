"""Idempotency-key result dedupe, shared by all mutating daemon endpoints.

The client retries a mutating POST exactly once after a transport failure iff
it carries ``X-Plato-Idempotency-Key``. That retry is only safe if the daemon
returns the SAME result for a key it has already seen, instead of re-running
the operation — a lost *response* must not become a second *execution*.

Two layers make that true across the whole retry window:

* a TTL'd LRU of COMPLETED results (``ResultCache``), replayed on late resends;
* a SINGLE-FLIGHT map of in-flight futures — a resend that lands while the
  first attempt is still executing (deadline blip, dropped connection; aiohttp
  does not cancel handlers on disconnect) awaits the SAME future and gets the
  identical payload, instead of racing a concurrent second execution.

One ``ResultCache`` per endpoint, wired via ``with_idempotency``.
"""

from __future__ import annotations

import asyncio
import time
from collections import OrderedDict
from collections.abc import Awaitable, Callable

from aiohttp import web
from pydantic import BaseModel

from plato.agents.daemon.http_util import request_id_of
from plato.rpc.protocol import HEADER_DEDUPED, HEADER_IDEMPOTENCY_KEY, HEADER_REQUEST_ID

_TTL_S = 300.0
_MAX_ENTRIES = 256


class ResultCache:
    """Completed-result LRU + in-flight single-flight registry, per endpoint."""

    def __init__(self) -> None:
        self._entries: OrderedDict[str, tuple[float, str]] = OrderedDict()
        self._inflight: dict[str, asyncio.Future[str]] = {}

    def get(self, key: str) -> str | None:
        entry = self._entries.get(key)
        if entry is None:
            return None
        ts, payload = entry
        if time.monotonic() - ts > _TTL_S:
            del self._entries[key]
            return None
        self._entries.move_to_end(key)
        return payload

    def put(self, key: str, payload: str) -> None:
        self._entries[key] = (time.monotonic(), payload)
        self._entries.move_to_end(key)
        while len(self._entries) > _MAX_ENTRIES:
            self._entries.popitem(last=False)

    def inflight(self, key: str) -> asyncio.Future[str] | None:
        """The future of a currently-executing attempt for ``key``, if any."""
        return self._inflight.get(key)

    def begin(self, key: str) -> asyncio.Future[str]:
        """Register ``key`` as in-flight. Caller MUST resolve via ``finish``."""
        fut: asyncio.Future[str] = asyncio.get_running_loop().create_future()
        self._inflight[key] = fut
        return fut

    def finish(self, key: str, fut: asyncio.Future[str], payload: str | None, exc: BaseException | None) -> None:
        """Resolve and deregister an in-flight attempt.

        Success caches the payload; failure propagates to waiters but is NOT
        cached — a later retry re-executes, matching the SSH-era semantics of
        retrying genuine failures.
        """
        self._inflight.pop(key, None)
        if payload is not None:
            self.put(key, payload)
            fut.set_result(payload)
        else:
            assert exc is not None
            fut.set_exception(exc)
            # Waiter may or may not exist; don't let "exception never
            # retrieved" warnings fire for the no-duplicate common case.
            _ = fut.exception()


async def with_idempotency(
    request: web.Request,
    cache: ResultCache,
    produce: Callable[[], Awaitable[BaseModel]],
) -> web.Response:
    """Run ``produce`` once per idempotency key — completed keys replay the
    cached JSON, in-flight keys await the first attempt's future. Requests
    without a key are executed unconditionally."""
    headers = {HEADER_REQUEST_ID: request_id_of(request)}
    key = request.headers.get(HEADER_IDEMPOTENCY_KEY)
    if not key:
        model = await produce()
        return web.json_response(text=model.model_dump_json(), headers=headers)

    cached = cache.get(key)
    if cached is not None:
        return web.json_response(text=cached, headers={**headers, HEADER_DEDUPED: "cache"})
    pending = cache.inflight(key)
    if pending is not None:
        # Duplicate landed mid-execution: share the first attempt's outcome.
        # shield() so THIS request's cancellation cannot cancel the shared
        # future out from under the original attempt's other waiters.
        payload = await asyncio.shield(pending)
        return web.json_response(text=payload, headers={**headers, HEADER_DEDUPED: "inflight"})

    fut = cache.begin(key)
    try:
        model = await produce()
    except BaseException as exc:
        cache.finish(key, fut, None, exc)
        raise
    payload = model.model_dump_json()
    cache.finish(key, fut, payload, None)
    return web.json_response(text=payload, headers=headers)
