"""Git service: the 17 structured git ops over one unary endpoint.

Option-A port of the SSH-stdio git protocol (``plato/git_ops/``): the existing
``GitOpRequest``/``GitOpResult`` models ride ``POST /v1/git/op`` unchanged, and
execution reuses ``git_ops.dispatch.run_request`` verbatim — same ops, same
semantics, different pipe. What the daemon adds over the stdio server:

* An unknown/invalid operation is a typed INVALID_REQUEST, not a dead server.
* Per-``repo_path`` serialization: the stdio server was globally sequential
  (one in-flight request per connection); GitPython on one repo is not
  concurrency-safe, so ops on the SAME repo still serialize — but ops on
  different repos may now overlap.
* Idempotency dedupe: a resent request (same X-Plato-Idempotency-Key) returns
  the cached result instead of re-running the op — the stdio client's
  reconnect-resend was at-least-once. Dedupe covers the WHOLE retry window: a
  resend that lands while the first attempt is still executing awaits the same
  in-flight task (single-flight), and a first attempt that outlives its
  deadline still populates the cache when it completes.
* Deadline enforcement from X-Plato-Deadline. Like the stdio server's
  client-side timeout, an expired op's thread keeps running to completion —
  git work is not cancellable mid-flight — but the caller gets a typed
  DEADLINE_EXCEEDED instead of a torn-down connection.
"""

from __future__ import annotations

import asyncio

from aiohttp import web

from plato.agents.daemon.http_util import error_response, parse_body, request_id_of
from plato.agents.daemon.idempotency import ResultCache
from plato.agents.daemon.state import DaemonContext
from plato.git_ops.dispatch import run_request
from plato.git_ops.models import GitOpRequest
from plato.rpc.protocol import (
    API_PREFIX,
    CAP_GIT,
    HEADER_DEADLINE,
    HEADER_DEDUPED,
    HEADER_IDEMPOTENCY_KEY,
    HEADER_REQUEST_ID,
)


class _RepoLocks:
    def __init__(self) -> None:
        self._locks: dict[str, asyncio.Lock] = {}

    def for_repo(self, repo_path: str) -> asyncio.Lock:
        lock = self._locks.get(repo_path)
        if lock is None:
            lock = asyncio.Lock()
            self._locks[repo_path] = lock
        return lock


# Strong refs to git-op tasks that outlive their request (deadline expired but
# the uncancellable GitPython thread is still running). Prevents GC of the task
# — and thus premature lock release — before the thread finishes.
_inflight: set[asyncio.Task[str]] = set()


def _op_handler(cache: ResultCache, locks: _RepoLocks):
    async def op(request: web.Request) -> web.Response:
        req = await parse_body(request, GitOpRequest)  # unknown op → INVALID_REQUEST

        headers = {HEADER_REQUEST_ID: request_id_of(request)}
        idem_key = request.headers.get(HEADER_IDEMPOTENCY_KEY)
        deadline_raw = request.headers.get(HEADER_DEADLINE)
        timeout = float(deadline_raw) if deadline_raw else None

        def _deadline_response() -> web.Response:
            return error_response(
                request,
                "DEADLINE_EXCEEDED",
                f"git op {req.operation} on {req.repo_path} exceeded {timeout}s",
            )

        fut: asyncio.Future[str] | None = None
        if idem_key:
            cached = cache.get(idem_key)
            if cached is not None:
                return web.json_response(text=cached, headers={**headers, HEADER_DEDUPED: "cache"})
            pending = cache.inflight(idem_key)
            if pending is not None:
                # Resend landed while the first attempt is still executing:
                # await the SAME attempt instead of enqueueing a duplicate
                # behind the repo lock (single-flight — the exactly-once claim
                # must hold across the whole retry window, not just after
                # completion).
                try:
                    payload = await asyncio.wait_for(asyncio.shield(pending), timeout=timeout)
                except TimeoutError:
                    return _deadline_response()
                return web.json_response(text=payload, headers={**headers, HEADER_DEDUPED: "inflight"})
            fut = cache.begin(idem_key)

        lock = locks.for_repo(req.repo_path)

        async def _run_locked() -> str:
            # The lock is acquired AND released inside the task, so it is held
            # for the entire lifetime of the (uncancellable) GitPython thread —
            # even if the request below abandons us on deadline. This is what
            # keeps same-repo ops serialized: a timed-out op still owns the repo
            # until its thread returns. GitPython is blocking, so it runs off
            # the event loop to keep health/job endpoints responsive.
            async with lock:
                result = await asyncio.to_thread(run_request, req)
                return result.model_dump_json()

        task: asyncio.Task[str] = asyncio.ensure_future(_run_locked())
        _inflight.add(task)
        task.add_done_callback(_inflight.discard)
        if idem_key and fut is not None:
            # Resolve the single-flight future (and populate the completed
            # cache) when the TASK finishes — not when this request returns.
            # A timed-out request abandons the task but later resends must
            # still dedupe against its eventual result.
            def _resolve(t: asyncio.Task[str], key: str = idem_key, f: asyncio.Future[str] = fut) -> None:
                exc = None if t.cancelled() else t.exception()
                if t.cancelled():
                    cache.finish(key, f, None, asyncio.CancelledError())
                elif exc is not None:
                    cache.finish(key, f, None, exc)
                else:
                    cache.finish(key, f, t.result(), None)

            task.add_done_callback(_resolve)

        try:
            # shield: on deadline, wait_for cancels the wrapper, NOT the task —
            # the task keeps running (and keeps the lock) to completion.
            payload = await asyncio.wait_for(asyncio.shield(task), timeout=timeout)
        except TimeoutError:
            return _deadline_response()

        return web.json_response(text=payload, headers=headers)

    return op


def register(app: web.Application, ctx: DaemonContext) -> None:
    app.router.add_post(f"{API_PREFIX}/git/op", _op_handler(ResultCache(), _RepoLocks()))
    ctx.capabilities.append(CAP_GIT)
