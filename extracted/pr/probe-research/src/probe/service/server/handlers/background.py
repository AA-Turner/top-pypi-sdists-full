"""outbox.drain, box.watch, telemetry.send: the caller checks before BackgroundHost starts a child (plan Q5)."""

from __future__ import annotations

import asyncio

from ...actions import caller
from ...jobs.background.background import is_other_network
from ....foundation.service_api.vocabularies import BackgroundRefusal
from ....foundation.service_api.params import need_background, need_telemetry
from probe.service.server.connections.connections import Connection
from probe.service.server.outbox import _is_base_url_allowed

#: `outbox.drain` / `box.watch` checks and child starts (a stat, a sandbox
#: read, a fork) on their own threads, at most this many taken in at once, and
#: what a caller is answered within (the SDK gives up well before: its budget
#: is `client.HANDOFF_BUDGET_S`).
BACKGROUND_THREADS = 2
MAX_PENDING_BACKGROUND = 8
BACKGROUND_WAIT_S = 2.0


class BackgroundHandlersMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""
    async def _outbox_drain(self, conn: Connection, params: dict) -> dict:
        """`outbox.drain` (plan Q5): the drainer of the outbox folder `dir`, as
        the service's child on the caller's interpreter and environment
        (`jobs/background/background.py`). `{accepted: true, state}` (started, or this
        service's child for it runs), else `{accepted: false, reason}` and the
        caller forks its own drainer, as before."""
        return await self._background_start(conn, need_background(params, directory=True), self.background.drain)

    async def _box_watch(self, conn: Connection, params: dict) -> dict:
        """`box.watch` (plan Q5): this box's watcher (`probe.box`), likewise."""
        return await self._background_start(conn, need_background(params, directory=False), self.background.watch_box)

    async def _background_start(self, conn: Connection, request: dict, start) -> dict:
        """The caller checks, then `start(request)`, on a thread: a caller in
        a sandbox is refused (its child would run outside it), and so is a
        `PROBE_BASE_URL` the CLI config does not name (plan D10: the stored
        login follows that variable). An answer not ready within
        BACKGROUND_WAIT_S reads `busy`; the start still completes, and the
        caller's own drainer and this one share the outbox's lease."""
        if self.stop_reason is not None:
            return {"accepted": False, "reason": BackgroundRefusal.STOPPING}
        peer = conn.peer_pid

        def checked() -> dict:
            # A caller cut off from the network is confined too: its uploads
            # would go out on this service's.
            if caller.sandboxed(peer) or is_other_network(peer):
                return {"accepted": False, "reason": BackgroundRefusal.SANDBOXED}
            if not _is_base_url_allowed(request["env"]):
                return {"accepted": False, "reason": BackgroundRefusal.UNKNOWN_ENDPOINT}
            return start(request)

        done, answer = await self._offload(
            "_background_starts", BACKGROUND_THREADS, self._background_slots, BackgroundRefusal.BUSY,
            BACKGROUND_WAIT_S, checked,
        )
        if not done or "refused" in answer:
            return {"accepted": False, "reason": BackgroundRefusal.BUSY}
        return answer

    async def _telemetry_send(self, conn: Connection, params: dict) -> dict:
        """`telemetry.send` (plan Q5): one batch the caller built, POSTed from
        the service's telemetry thread. Never for a caller in a sandbox (its
        network would be this service's)."""
        entries, batch_id = need_telemetry(params)
        peer = conn.peer_pid
        if await asyncio.to_thread(lambda: caller.sandboxed(peer) or is_other_network(peer)):
            return {"accepted": False, "reason": BackgroundRefusal.SANDBOXED}
        return self.background.send_telemetry(entries, batch_id)
