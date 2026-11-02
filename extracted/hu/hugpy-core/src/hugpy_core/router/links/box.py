"""Box links — the router's live view of each box.

A link keeps one `Box` snapshot current through the wrapper's own API:
`GET /v1/telemetry/state?wait=N&since=K` with the box key. The wrapper answers when
it next writes (long-poll), so one open request per box keeps the snapshot current
with no timer anywhere. (0.0.1 also read a local box's store file and polled SQLite's
data_version every 0.5 s; removed in 0.0.2 — the wrapper is reached through its API
only, the same way core reaches it through this router.)

Routing requires a recent coherent telemetry response; `/health` alone cannot
renew an expired snapshot.
"""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Optional
from urllib.parse import urlencode

import aiohttp

from hugpy_core.router.core.types import Box, Resident
from hugpy_core.router.imports import constants as C

log = logging.getLogger("hugpy_core.router.links")


def box_from_state(name: str, state: dict, pool: str = "", blocked: bool = False,
                   online: bool = True, last_picked: float = 0.0,
                   wildcard: bool = False) -> Box:
    """A Box from the wrapper's state tables (residents, models, gpu_state)."""
    residents = []
    for r in state.get("residents") or []:
        if not r.get("key"):
            continue
        st = r.get("state") or ("serving" if r.get("busy") else "idle")
        residents.append(Resident(key=r["key"], state=st,
                                  healthy=bool(r.get("healthy", True)) and bool(r.get("alive", True)),
                                  busy=bool(r.get("busy")), last_used=float(r.get("last_used") or 0)))
    models = frozenset(m["key"] for m in (state.get("models") or []) if m.get("key"))
    frees = [int(g["free"]) for g in (state.get("gpu_state") or []) if g.get("free") is not None]
    observation = state.get('observation') or {}
    identity = ((observation['store_id'], observation['epoch'])
                if observation.get('store_id') and observation.get('epoch') else None)
    return Box(name=name, online=online, pool=pool, blocked=blocked, wildcard=wildcard, residents=tuple(residents),
               models=models, room_gpu=max(frees) if frees else None, last_picked=last_picked,
               observation_identity=identity, observation_generation=observation.get('generation'))


class BoxLink:
    def __init__(self, name: str, url: str, key: Optional[str] = None, pool: str = "",
                 store: Optional[str] = None, blocked: bool = False, wildcard: bool = False):
        self.name, self.url, self.key, self.pool = name, url.rstrip("/"), key, pool
        self.store_path, self.blocked, self.wildcard = store, blocked, wildcard
        self.state: dict = {}
        self.online = False
        self.last_ok = 0.0
        self.last_picked = 0.0
        self.mode = "api"                     # `store` (0.0.1's local file link) is accepted and ignored
        self._changes = -1
        self._received_at = None
        self._task: Optional[asyncio.Task] = None
        # EVENT-DRIVEN (operator 2026-10-14): the wrapper's long-poll answers when its
        # store changed; ``changed`` is set exactly then (never on a mere timeout
        # answer), with ``version`` counting the box's changes seen. A consumer
        # (the core's collector) awaits it instead of running a timer.
        self.changed: asyncio.Event = asyncio.Event()
        self.version: int = 0
        self.on_change: list = []             # callbacks(link) on every change seen (central's queue kicks)

    # the snapshot
    def box(self) -> Box:
        fresh = (self._received_at is not None
                 and time.monotonic() - self._received_at <= C.OFFLINE_AFTER_S
                 and (self.state.get('observation') or {}).get('consistent', True) is True)
        return box_from_state(self.name, self.state, self.pool, self.blocked,
                              online=self.online and bool(self.state) and fresh, last_picked=self.last_picked,
                              wildcard=self.wildcard)

    def accept_state(self, state):
        """Accept a full telemetry response; health alone cannot refresh it."""
        if not isinstance(state, dict):
            raise ValueError('worker telemetry must be an object')
        observation = state.get('observation')
        if observation is not None:
            if (not isinstance(observation, dict)
                    or observation.get('schema') != 'hugpy.worker-observation'
                    or observation.get('version') != 1
                    or not isinstance(observation.get('epoch'), str) or not observation['epoch']
                    or not observation.get('store_id')
                    or observation['store_id'] != state.get('store_id')
                    or type(observation.get('generation')) is not int
                    or observation['generation'] != state.get('changes')
                    or type(observation.get('consistent')) is not bool):
                raise ValueError('invalid worker observation envelope')
        changes = int(state.get('changes') or 0)
        old = self.state.get('observation') or {}
        new = observation or {}
        if (old and new and (old.get('store_id'), old.get('epoch'))
                == (new.get('store_id'), new.get('epoch')) and changes < self._changes):
            raise ValueError('worker observation generation regressed within one epoch')
        moved = (changes != self._changes or not self.state
                 or (old.get('store_id'), old.get('epoch'), old.get('consistent'))
                 != (new.get('store_id'), new.get('epoch'), new.get('consistent')))
        self.state, self._changes = state, changes
        self._received_at = time.monotonic()
        self.online, self.last_ok = True, time.time()
        return moved

    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.key}"} if self.key else {}

    # running
    def start(self, session: aiohttp.ClientSession) -> None:
        self._task = asyncio.ensure_future(self._run(session))

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except (asyncio.CancelledError, Exception):  # noqa: BLE001
                pass

    async def _health(self, session) -> bool:
        try:
            async with session.get(self.url + "/health", timeout=aiohttp.ClientTimeout(total=5)) as r:
                ok = r.status == 200
        except Exception:  # noqa: BLE001
            ok = False
        now = time.time()
        if ok:
            self.last_ok = now
        self.online = ok or (now - self.last_ok < C.OFFLINE_AFTER_S and self.last_ok > 0)
        return ok

    async def _run(self, session) -> None:
        while True:
            try:
                await self._run_remote(session)
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 — a link never dies
                log.warning("link %s: %s", self.name, exc)
                await asyncio.sleep(2)

    async def _run_remote(self, session) -> None:
        await self._health(session)
        query = {'wait': C.WAIT_S, 'since': self._changes}
        epoch = (self.state.get('observation') or {}).get('epoch')
        if epoch:
            query['epoch'] = epoch
        url = f"{self.url}/v1/telemetry/state?{urlencode(query)}"
        try:
            async with session.get(url, headers=self.headers(),
                                   timeout=aiohttp.ClientTimeout(total=C.WAIT_S + 15)) as r:
                if r.status != 200:
                    log.warning("link %s: state answered %s", self.name, r.status)
                    await asyncio.sleep(5)
                    return
                state = await r.json()
                moved = self.accept_state(state)
                if moved:
                    self.version += 1
                    self.changed.set()
                    for cb in list(self.on_change):
                        try:
                            cb(self)
                        except Exception:  # noqa: BLE001 — a consumer's error never stops the link
                            log.warning("link %s: on_change callback failed", self.name, exc_info=True)
        except (aiohttp.ClientError, asyncio.TimeoutError):
            await asyncio.sleep(2)
