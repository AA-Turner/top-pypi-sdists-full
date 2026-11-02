"""the loop side: scan every SCAN_S, run each WatchCondition, turn a condition failing on two scans into an incident."""

from __future__ import annotations

import asyncio
import contextlib
import threading
from collections.abc import Callable, Mapping
from probe.service.watch.conditions.capture import capture_conditions
from probe.service.watch.conditions.lease import lease_condition
from probe.service.watch.incident import Family
from probe.service.watch.settings import (
    CAPTURE_MAX_SESSIONS,
    DEDUPE_S,
    GONE_S,
    KEPT_WHILE_UPDATING,
    MAX_PENDING,
    SLOW_CHECK_S,
    STALL_S,
    WAKE_GAP_S,
    WAKE_GRACE_S,
    WAKE_SLACK_S,
    WINDOW_S,
)


#: A slow check's read that did not answer (timed out, or still stuck).
_UNREAD = object()


async def _on_daemon_thread(work: Callable[[], object], timeout: float) -> object:
    """`work()` on a daemon thread of its own, waited for at most `timeout`
    (asyncio.TimeoutError past it): a call stuck on a slow server is left
    behind, and neither the loop nor a stopping service waits for it (the
    default executor's threads are joined at exit; `receipts.ReceiptCache`'s rule)."""
    loop = asyncio.get_running_loop()
    result: asyncio.Future = loop.create_future()

    def run() -> None:
        try:
            value, error = work(), None
        except Exception as exc:  # noqa: BLE001 -- handed to the waiter
            value, error = None, exc

        def settle() -> None:
            if result.done():
                return
            if error is not None:
                result.set_exception(error)
            else:
                result.set_result(value)

        with contextlib.suppress(RuntimeError):  # the loop is closed: the service went first
            loop.call_soon_threadsafe(settle)

    threading.Thread(target=run, name="probe-watch-check", daemon=True).start()
    return await asyncio.wait_for(result, timeout)


class LoopSideMixin:
    """Part of Watch: its methods run with `self` the Watch; compose() folds them into Watch."""

    # -- the loop side -----------------------------------------------------------

    def start(self) -> None:
        """Arm the scan (the service calls it once it serves), having read what
        a note must know from the first: the once-ever record (never read under
        the lock on the loop later) and the barrier (else unknown until the
        first scan, SCAN_S away)."""
        if not self.enabled:
            return
        with self._lock:
            self._load_state()
        try:
            self._barrier = bool(self.barrier_up())
        except Exception:  # noqa: BLE001 -- unknown: not up
            self._barrier = False
        self._arm()

    def _arm(self) -> None:
        loop = self._loop_getter()
        if loop is None or self._closed:
            return
        self._timer = loop.call_later(self.scan_s, self._tick_scan)

    def _tick_scan(self) -> None:
        self._timer = None
        self._spawn(self._scan())

    def _spawn(self, coro) -> None:
        task = asyncio.ensure_future(coro)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    def _kick(self) -> None:
        """From any thread: on the loop's next turn, the new incident's
        sessions are taken (`_triage`) -- whatever the report slot is doing
        meanwhile (a child running, a login shell asked) -- and a send is tried."""
        loop = self._loop_getter()
        if loop is None or loop.is_closed() or self._closed:
            return
        with contextlib.suppress(RuntimeError):
            loop.call_soon_threadsafe(self._kicked)

    def _kicked(self) -> None:
        self._triage()
        self._spawn(self._send_next())

    def _triage(self) -> None:
        """On the loop: each new incident gets the sessions whose agent runs
        NOW, the moment it is looked at (its consent is theirs and its own
        environment's). While discovering too, marked `partial`: those are
        joined, when it is decided, by the sessions back by then."""
        with self._lock:
            fresh, self._fresh = self._fresh, []
        if not fresh:
            return
        voters = list(self.voters())
        partial = bool(self.discovering())
        for incident in fresh:
            if incident.family not in KEPT_WHILE_UPDATING and self._quiet():
                continue  # an update began before it was looked at
            incident.voters, incident.partial = voters, partial
            with self._lock:
                self._pending.pop(incident.key, None)
                self._pending[incident.key] = incident
                while len(self._pending) > MAX_PENDING:
                    self._pending.pop(next(iter(self._pending)))

    def _sense_wake(self) -> None:
        """Wall time ran ahead of monotonic time since the last scan (a sleep,
        which monotonic time does not count), or the scans were far apart:
        every condition measured in time starts again, after WAKE_GRACE_S."""
        wall, mono = self.clock(), self.monotonic()
        if self._tick is not None:
            last_wall, last_mono = self._tick
            if (wall - last_wall) - (mono - last_mono) > WAKE_SLACK_S or mono - last_mono > max(
                WAKE_GAP_S, 4 * self.scan_s
            ):
                self._woke_at = mono
                self._cond_last = {}
                self.log("watch: the machine slept (or the scans stalled): what is measured in time waits "
                         f"{WAKE_GRACE_S:.0f} s")
        self._tick = (wall, mono)

    def _timed(self) -> bool:
        """May a condition measured in time count now (not just after a wake)?"""
        return self._woke_at is None or self.monotonic() - self._woke_at >= WAKE_GRACE_S

    def _prune(self) -> None:
        """Counts past their window and reports past their dedupe window go."""
        mono, wall = self.monotonic(), self.clock()
        with self._lock:
            for key, seen in list(self._seen.items()):
                while seen and mono - seen[0][0] > WINDOW_S:
                    seen.popleft()
                if not seen:
                    del self._seen[key]
            for key, at in list(self._settled.items()):
                if wall - at >= DEDUPE_S:
                    del self._settled[key]

    async def _scan(self) -> None:
        try:
            self._last_scan = self.clock()
            self._sense_wake()
            self._prune()
            try:
                self._barrier = bool(await asyncio.to_thread(self.barrier_up))
            except Exception:  # noqa: BLE001 -- unknown: not up
                self._barrier = False
            if self.discovering() or self._quiet():
                return
            sessions = list(self.sessions())
            daemon = [
                (s.sid, s.state_dir) for s in sessions
                if getattr(s, "mode", None) == "daemon" and getattr(s, "state_dir", None) and not self.supervised(s.sid)
            ]
            # A `tap watch` session (its own recorder, not this service's): its
            # link's registration is its heartbeat; only with an agent that runs.
            heartbeats = [
                (s.sid, s.heartbeat_at) for s in sessions
                if getattr(s, "owner", None) is not None and getattr(s, "owner_live", False)
                and self.hosted_env(s.sid) is None and isinstance(getattr(s, "heartbeat_at", None), (int, float))
            ]
            beats = list(self.recorders())
            leases, stalled, record = await asyncio.to_thread(self._look, daemon, beats)
            self._conditions(leases, stalled, heartbeats)
            self._guard(record)
            await self._slow_checks()
            await self._send_next()
        except Exception as exc:  # noqa: BLE001 -- one bad scan never stops the next
            self.log(f"watch: scan failed: {exc!r}")
        finally:
            self._arm()

    def _look(self, daemon: list, beats: list) -> tuple[dict, dict, dict | None]:
        """On a thread (a session's state folder may be a slow mount, an
        owner's check runs `ps` on macOS): each unsupervised daemon session's
        lease condition, each hosted recorder stalled while its agent runs,
        and guard.json."""
        from .. import guard
        from ...foundation.service_api import procid

        now = self.clock()
        leases = {}
        for sid, state_dir in daemon:
            found = lease_condition(state_dir, sid, now)
            if found is not None:
                leases[sid] = found
        stalled = {}
        for beat in beats:
            age, owner = beat.get("beat_age_s"), beat.get("owner")
            if not isinstance(age, (int, float)) or age <= STALL_S or not isinstance(owner, dict):
                continue
            try:
                running = procid.alive(int(owner["pid"]), str(owner["start_time"])) is not False
            except (KeyError, TypeError, ValueError):
                running = False
            if running:
                stalled[beat["sid"]] = {"beat_s": round(age)}
        return leases, stalled, guard.read()

    def _conditions(self, leases: dict, stalled: dict, heartbeats: list) -> None:
        """A failing condition on two scans in a row: one event (its family's
        threshold met). A condition measured in time waits out a wake."""
        timed = self._timed()
        found: dict = {}
        for sid, (cond, facts) in leases.items():
            if cond in ("hung", "not_running") and not timed:
                continue
            found[(Family.WORKER, sid)] = (cond, {**facts, "source": "lease"})
        if timed:
            for sid, facts in stalled.items():
                found[(Family.RECORDER, sid)] = ("stalled", facts)
            now = self.clock()
            for sid, heartbeat_at in heartbeats:
                if now - heartbeat_at > GONE_S:
                    # Once per registration: a session its next service did not
                    # resume stays gone, unchanged, until its agent's next prompt
                    # registers it again, which may be hours away.
                    found[(Family.RECORDER, sid)] = ("gone", {"heartbeat_s": round(now - heartbeat_at)},
                                                     f"recorder_gone:{sid}:{heartbeat_at!r}")
        last, self._cond_last = self._cond_last, {key: cond for key, (cond, *_) in found.items()}
        for (family, sid), (cond, facts, *once) in found.items():
            if last.get((family, sid)) == cond:
                self.note(family, cond, sid, facts, once=once[0] if once else None, threshold=1)

    async def _slow_checks(self) -> None:
        """Every SLOW_CHECK_S (and on the first scan): the outbox and each live
        session's receipts, a condition on two runs in a row making one event;
        every CREDENTIAL_CHECK_S, each key the CLI config holds. Measured in
        time, so never just after a wake."""
        mono = self.monotonic()
        if self._slow_at is not None and mono - self._slow_at < SLOW_CHECK_S:
            return
        self._slow_at = mono
        if not self._timed():
            self._slow_last = {}
            return
        now = self.clock()
        found: dict = {}
        #: The families whose read this time answered (a read given up on is
        #: no news either way: nothing it waits on is dropped).
        read: set = set()
        stuck = await self._read_outbox(now)
        if stuck is not _UNREAD:
            read.add(Family.OUTBOX_STUCK)
            if stuck is not None:
                found[(Family.OUTBOX_STUCK, None)] = stuck
        try:
            receipts = await self.receipts()
        except Exception as exc:  # noqa: BLE001 -- no receipts this time: nothing said about them
            self.log(f"watch: reading receipts failed: {exc!r}")
            receipts = None
        if isinstance(receipts, Mapping):
            read.add(Family.CAPTURE_STALLED)
        # Unread: nothing said about them, and what `still` saw is kept (an
        # empty read would forget it, and the next one age from scratch).
        stalled = (capture_conditions(receipts, now, self._capture_still)
                   if isinstance(receipts, Mapping) else {})
        if stalled:
            # One report for the machine, naming its sessions: an hour-long
            # stall of the server's ingestion stalls every session at once,
            # and that is one report per machine, not one per session.
            oldest = sorted(stalled, key=lambda sid: -stalled[sid]["received_h"])
            found[(Family.CAPTURE_STALLED, None)] = ("waiting", {
                "count": len(stalled), "sessions": {sid: stalled[sid] for sid in oldest[:CAPTURE_MAX_SESSIONS]}})
        last, self._slow_last = self._slow_last, {key: reason for key, (reason, _) in found.items()}
        for (family, sid), (reason, facts) in found.items():
            if last.get((family, sid)) == reason:
                self.note(family, reason, sid, facts, threshold=1)
        self._drop_cleared(found, read)
        if self._credential_task is None or self._credential_task.done():
            # Beside the scan, never in it: a server trickling its answer holds
            # this check (CREDENTIAL_DEADLINE_S at most), never the next scan.
            self._credential_task = asyncio.ensure_future(self._credential_check(now))
            self._tasks.add(self._credential_task)
            self._credential_task.add_done_callback(self._tasks.discard)

    def _drop_cleared(self, found: dict, read: set) -> None:
        """An outbox or capture incident still waiting (a retry) whose
        condition this check read and no longer sees is no longer news: it
        goes."""
        with self._lock:
            cleared = [key for key in self._pending
                       if key[0] in (Family.OUTBOX_STUCK, Family.CAPTURE_STALLED) and key[0] in read
                       and key not in found]
            for key in cleared:
                del self._pending[key]
        for family, _ in cleared:
            self.log(f"watch: {family} cleared before it was reported; dropped")
