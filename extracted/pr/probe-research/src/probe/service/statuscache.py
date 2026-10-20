"""`status.get`: `probe status --json`'s object, from a child, cached (plan X7).

`python -m probe.core.run status` runs in a child (it reads setup, plugin and
doctor code the service must not import), at most once per TTL_S for one
context, and again after anything that changes what it would say: an action
ending, a session starting or ending (`invalidate`). `refresh: true` always runs
a child, with the slow checks (`probe status --refresh`); its answer is cached
like any other. `max_age` (seconds) takes a cached answer only that young:
`max_age: 0` always runs a fresh local child, without the slow checks.

One cache entry per request context (plan X2: a client with its own
`PROBE_CONFIG_PATH` or `CLAUDE_CONFIG_DIR` sees its own files), a few at most.
Concurrent callers of one context share one child.

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import asyncio
import json
import time

from . import children
from .protocol import ErrorCode, RefusedReason, RpcError

TTL_S = 30.0
TIMEOUT_S = 60.0
#: Contexts remembered at once; the least recently used goes first.
MAX_ENTRIES = 8


class StatusCache:
    def __init__(self, *, ttl: float = TTL_S, timeout: float = TIMEOUT_S) -> None:
        self.ttl = ttl
        self.timeout = timeout
        #: Bumped by `invalidate`: an entry from an older generation is stale.
        self.generation = 0
        self._entries: dict[str, tuple[float, int, dict]] = {}
        #: (context, refresh, generation) -> the child answering it: a caller after
        #: an `invalidate` never joins a child that started before it.
        self._inflight: dict[tuple[str, bool, int], asyncio.Future] = {}
        #: Children run so far (`service.status` shows it; the tests read it).
        self.children = 0

    def invalidate(self) -> None:
        self.generation += 1

    @staticmethod
    def key(env_extra: dict) -> str:
        return json.dumps(sorted(env_extra.items()))

    async def get(self, env_extra: dict, *, refresh: bool, max_age: float | None = None) -> dict:
        key = self.key(env_extra)
        entry = self._entries.get(key)
        limit = self.ttl if max_age is None else min(self.ttl, float(max_age))
        if (
            not refresh
            and limit > 0
            and entry is not None
            and entry[1] == self.generation
            and time.monotonic() - entry[0] <= limit
        ):
            return entry[2]
        slot = (key, refresh, self.generation)
        flight = self._inflight.get(slot)
        if flight is None or flight.done():
            for old in [k for k, f in self._inflight.items() if f.done()]:
                del self._inflight[old]
            flight = asyncio.ensure_future(self._run(key, env_extra, refresh))
            self._inflight[slot] = flight
        return await asyncio.shield(flight)

    async def _run(self, key: str, env_extra: dict, refresh: bool) -> dict:
        generation = self.generation
        self.children += 1
        try:
            code, snapshot = await children.run_read(
                "status", {"refresh": True} if refresh else {}, env_extra=env_extra, timeout=self.timeout
            )
        except OSError as exc:
            raise RpcError(
                ErrorCode.REFUSED, f"probe status could not start: {exc}", {"reason": RefusedReason.STATUS_UNAVAILABLE}
            ) from None
        if code is None:
            raise RpcError(ErrorCode.REFUSED, "probe status timed out", {"reason": RefusedReason.STATUS_UNAVAILABLE})
        if not isinstance(snapshot, dict):
            raise RpcError(
                ErrorCode.REFUSED,
                f"probe status gave no JSON object (exit {code})",
                {"reason": RefusedReason.STATUS_UNAVAILABLE},
            )
        self._entries.pop(key, None)
        self._entries[key] = (time.monotonic(), generation, snapshot)
        while len(self._entries) > MAX_ENTRIES:
            self._entries.pop(next(iter(self._entries)))
        return snapshot
