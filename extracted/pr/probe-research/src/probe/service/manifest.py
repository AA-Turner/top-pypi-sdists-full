"""`manifest.refresh`: the release manifest, refreshed by the service for the CLI.

A CLI command that finds its cached manifest (`version-check.json`) stale used
to spawn a detached `python -m probe.cli.version_refresh` of its own on every
such call. Where a service answers, it asks the service instead and goes on at
once: the service runs ONE `probe.core.run version {"refresh": true}` child,
which is that refresher's work (the same fetch, TLS trust and back-off, written
to the same cache, then the update reports still waiting), with the caller's
context: its proxy, CA bundle, config and cache folders (`protocol.CONTEXT_ENV`).

    one at a time   per context: a caller while one runs gets `running`
    recent          a context refreshed less than COOLDOWN_S ago answers that
                    refresh (`recent`) instead of fetching again; the CLI reads
                    that as "it did not land" and refreshes itself
    bounded         at most MAX_ENTRIES refreshes at once; past that, `busy`
    wait            a caller may wait up to `wait` seconds for the answer; the
                    CLI's every-command path never does (it must not make, or
                    wait for, a network call)
    holds           a refresh in flight keeps the service up (at most TIMEOUT_S)

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Callable

from . import children
from .protocol import CheckOutcome, ErrorCode, RpcError

#: A refresh child past this is killed (its fetch alone is bounded at 3 s).
TIMEOUT_S = 60.0
#: A context refreshed this recently answers that refresh, not a new fetch.
COOLDOWN_S = 60.0
#: Contexts remembered at once; the least recently refreshed goes first.
MAX_ENTRIES = 8


class ManifestRefresher:
    def __init__(self, *, changed: Callable[[], None] = lambda: None, timeout: float = TIMEOUT_S) -> None:
        self._changed = changed
        self.timeout = timeout
        self._inflight: dict[str, asyncio.Future] = {}
        #: context key -> (monotonic time it finished, its answer)
        self._last: dict[str, tuple[float, dict]] = {}
        #: Children run so far (the tests read it).
        self.children = 0

    @staticmethod
    def key(env_extra: dict) -> str:
        return json.dumps(sorted(env_extra.items()))

    def in_flight(self) -> bool:
        return any(not f.done() for f in self._inflight.values())

    async def refresh(self, env_extra: dict, *, wait: float = 0.0) -> dict:
        """`{outcome, done, result}`: `outcome` is started | running | recent;
        `result` the finished refresh's answer once `done`."""
        key = self.key(env_extra)
        flight = self._inflight.get(key)
        if flight is None or flight.done():
            last = self._last.get(key)
            if last is not None and 0 <= time.monotonic() - last[0] < COOLDOWN_S:
                return {"outcome": CheckOutcome.RECENT, "done": True, "result": last[1]}
            if sum(1 for f in self._inflight.values() if not f.done()) >= MAX_ENTRIES:
                # The caller refreshes it itself (the CLI's own detached child).
                raise RpcError(ErrorCode.BUSY, "busy: too many manifest refreshes at once")
            flight = asyncio.ensure_future(self._run(key, env_extra))
            self._inflight[key] = flight
            outcome = CheckOutcome.STARTED
            self._changed()
        else:
            outcome = CheckOutcome.RUNNING
        if wait > 0 and not flight.done():
            try:
                await asyncio.wait_for(asyncio.shield(flight), wait)
            except asyncio.TimeoutError:
                pass
        done = flight.done() and not flight.cancelled() and flight.exception() is None
        return {"outcome": outcome, "done": done, "result": flight.result() if done else None}

    async def _run(self, key: str, env_extra: dict) -> dict:
        self.children += 1
        try:
            try:
                code, value = await children.run_read(
                    "version", {"refresh": True}, env_extra=env_extra, timeout=self.timeout
                )
            except Exception as exc:  # noqa: BLE001 -- recorded for the cooldown, never raised unread
                code, value = None, None
                if isinstance(exc, OSError):
                    error = f"the refresh could not start: {exc}"
                else:
                    error = f"the refresh failed: {exc!r}"
            else:
                error = None if code is not None else "the refresh timed out"
            answer = value if isinstance(value, dict) else {}
            ok = answer.get("ok")
            fetched = answer.get("fetched_at")
            latest = answer.get("cli_latest")
            result = {
                "ok": ok if isinstance(ok, bool) else False,
                "fetched_at": fetched if isinstance(fetched, (int, float)) and not isinstance(fetched, bool) else None,
                "cli_latest": latest if isinstance(latest, str) else None,
                "exit_code": code,
            }
            if error is None and (code != 0 or not answer):
                error = f"the refresh gave no answer (exit {code})"
            if error is not None:
                result["error"] = error
            self._last.pop(key, None)
            self._last[key] = (time.monotonic(), result)
            while len(self._last) > MAX_ENTRIES:
                self._last.pop(next(iter(self._last)))
            return result
        finally:
            self._inflight.pop(key, None)
            asyncio.get_running_loop().call_soon(self._changed)
