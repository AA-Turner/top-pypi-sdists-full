"""one poll (read, settle, renew, maybe a bite) and the idle-aware loop around it."""

from __future__ import annotations
import asyncio
import contextlib
import os
import time
from pathlib import Path
from probe.daemon.session import session as folders
from probe.daemon.host import lease
from probe.shared import mailbox
from probe.shared.mailbox import requests as requests_mod
from probe.daemon.trace import shipper as shipper_mod

POLL_S = 2.0
#: The folder check runs at most this often.
FOLDER_CHECK_S = 30.0
#: How often a running bite looks at the session-end deadline (which a signal
#: can start while it runs).
DEADLINE_POLL_S = 1.0
#: A `.handover` marker older than this was left by a waiter that died.
HANDOVER_FRESH_S = 10.0
#: In the daemon host (plan M2): a run that has seen nothing new for IDLE_AFTER_S
#: polls only every IDLE_POLL_S, and wakes at once when one of its files changes
#: (`Worker.poke`, from the host's watcher). A worker process polls every POLL_S.
IDLE_AFTER_S = 60.0
IDLE_POLL_S = 10.0
#: Test-only overrides of the two (read in the run's environment). Nothing in production sets them.
IDLE_AFTER_ENV = "PROBE_DAEMON_IDLE_AFTER_S"
IDLE_POLL_ENV = "PROBE_DAEMON_IDLE_POLL_S"


def _idle_timings() -> tuple[float, float]:
    def read(name: str, default: float) -> float:
        try:
            value = float(os.environ.get(name) or default)
        except ValueError:
            return default
        return value if value > 0 else default

    return read(IDLE_AFTER_ENV, IDLE_AFTER_S), read(IDLE_POLL_ENV, IDLE_POLL_S)


class TickMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    # -- the loop -------------------------------------------------------------
    async def _check_folders(self, workdirs: list[Path], *, emit: bool = True, force: bool = False) -> None:
        """The folder check, at most every FOLDER_CHECK_S (unless `force`) and off the
        event loop. Its failure is logged, never the bite's. `emit=False` only moves
        the snapshot on: what changed in `read only (daemon)` is never announced.
        While the session ends, a growing file's `changed` line is not waited for
        (`folders.GROWING`)."""
        if not force and self.clock() - self.folders_checked_at < FOLDER_CHECK_S:
            return
        self.folders_checked_at = self.clock()
        try:
            await folders.check_async(self.store, self.session.cwd, self.session.home, workdirs=workdirs, emit=emit,
                                      excluded=self.exclusions.path_excluded, flush=self.stopping)
        except Exception as exc:  # noqa: BLE001
            log.warning("folder check failed: %s: %s", type(exc).__name__, exc)
        self._mark_inline()  # a file the agent changed while it held Probe is its own

    async def tick(self) -> int | None:
        """One poll. An exit code when the worker is done, else None."""
        if self.replay is None and install_replaced():
            # The next read of its own files would fail or be the new version's, in
            # either lane (the reader, which never ends the worker, would only ping
            # "failing"). Leave 0 and the supervisor starts the new install, which
            # takes the session over -- unless the session is ending: then nobody
            # restarts it, and what is still queued waits for the next daemon.
            log.warning("%s; exiting for the new install", REINSTALLED)
            if self.stopping:
                unrecorded = len(self.store.pending())
                if unrecorded:
                    _device_error(f"session {self.session.session_id} ended with {unrecorded} events unrecorded; "
                                  "the next daemon on this machine finishes them")
            else:
                _device_error(f"session {self.session.session_id}: the probe CLI was reinstalled; the daemon "
                              "restarts on the new install")
            self._release(lease.REASON_STOPPED)
            return 0
        if self.replay is None:
            self._keep_mailbox()
        state = lease.session_state(self.session.session_id)
        if self.replay is None:
            if lease.inline(self.session.session_id, state):
                # Manual or confirmed-quota inline stops the daemon as `off` does,
                # at once, with no
                # finishing pass (the agent records from the switch on, and an
                # approval settled now would race it). What came before the switch
                # stays pending for the next worker. The folders are looked at
                # first: an edit made before the switch is stamped before it, and
                # the agent's edits after it become events of their own.
                log.info("Probe is inline: stopping the daemon")
                await self._check_folders(folders.working_folders(self.store, self.session.cwd, self.session.home),
                                          force=True)
                self.fail_requests(requests_mod.REASON_INLINE)
                self._release(lease.REASON_STOPPED)
                return inline_exit_code(self.session.session_id)
            if lease.reads_only(self.session.session_id, state):
                return await self._read_only_tick()
            if state is not None and not lease.records(self.session.session_id, state):
                self.fail_requests(requests_mod.REASON_OFF)
                self._release(lease.REASON_STOPPED)
                return 0
            if state is None:
                code = self._switch_unreadable()
                if code is not None:
                    return code
            else:
                self.switch_unreadable_since = None
        if self.read_only_from is not None and state == STATE_DAEMON:
            await self._end_read_only()
        if not self.stopping and self._parent_gone():
            log.info("capture is gone: finishing what is queued")
            self.begin_stopping()
        self._take_input()
        self._announce_inline()
        self._fail_stuck_requests()
        self.publish_writer_messages()
        if self.audit is not None and not self.stopping:
            self.audit.maybe_start()
        # Renewed first: a yes settled below runs on a fresh lease, not the end of an old one.
        self._renew()
        await self.settle_answers()
        self._renew()
        if self.handing_over():
            log.info("handing over to the resumed session's worker")
            self._release(lease.REASON_HANDOVER)
            return 0
        left = None if self.finish_by is None else self.finish_by - self.clock()
        trigger = self.due() if left is None or left > 0 else None
        blocked = self._bite_blocked() if trigger else None
        if trigger and blocked is None:
            self.not_started = None
            workdirs = folders.working_folders(self.store, self.session.cwd, self.session.home)
            await self._check_folders(workdirs)
            await self.run_bite(trigger, workdirs=workdirs)
            return None
        if blocked is not None and blocked != self.not_started:
            log.info("a bite is due (%s) but none starts: %s", trigger, blocked)
            self.not_started = blocked
        self.requeue_deferred()
        idle = not self.store.pending(limit=1) and not self._carrying_on()
        if self.stopping and idle and (left is None or left > 0) and folders.growing(self.store):
            # A growing file's last `changed` line is owed: one more look makes it,
            # and the next poll records it.
            await self._check_folders(folders.working_folders(self.store, self.session.cwd, self.session.home),
                                      force=True)
            if self.store.pending(limit=1):
                return None
        if self.stopping and (idle or (left is not None and left <= 0)):
            unrecorded = len(self.store.pending())
            if unrecorded:
                _device_error(f"session {self.session.session_id} ended with {unrecorded} events unrecorded; "
                              "the next daemon on this machine finishes them")
            self.fail_requests(requests_mod.REASON_SESSION_END)
            self._release(lease.REASON_STOPPED)
            return 0
        return None

    def _keep_mailbox(self) -> None:
        """Every poll: the mailbox folders' keep files, so an SDK from before
        #3616 never takes them for a dead run's (`mailbox.keep_folders`), and
        this worker's marker again when something removed it."""
        sid = self.session.session_id
        mailbox.keep_folders()
        if not self.marks_requests:
            return
        offered = self.run_alerts.offered if self.run_alerts is not None else None
        try:
            if mailbox.keep_worker_marker(sid, config=offered):
                log.warning("this worker's request marker was gone; written again")
        except OSError as exc:  # the next poll tries again
            log.warning("could not write this worker's request marker again: %s", exc)

    def handing_over(self) -> bool:
        """The session ended, and a resumed session's worker waits for the lock
        (`session_lock` wrote the marker): hand over at the next model round
        instead of finishing the queue -- the new worker carries the same
        conversation on from the shared store."""
        if not self.stopping:
            return False
        try:
            age = time.time() - mailbox.handover_path(self.session.session_id).stat().st_mtime
        except OSError:
            return False
        # The waiter re-touches it every poll: an old one was left by a waiter that died.
        return age < HANDOVER_FRESH_S

    def wake_paths(self) -> list[Path]:
        """What the host's watcher looks at for this run (plan M2): every stream
        it reads (`_end_offsets`: the chat log, its helper agents' logs and their
        folder, the SDK inbox, the reader's claim log), its switch, its asks and
        writer requests, the held questions' answers, its hand-over ask. Anything
        else waits for the next poll. Asked again now and then (`Host.watch`): a
        helper agent's log may start later."""
        sid = self.session.session_id
        files = self.adapter.session_files(self.session.transcript)
        streams = [files.main, *files.subagents, inbox_path(sid), mailbox.claim_log_path(sid)]
        folders_ = sorted({p.parent for p in files.subagents})
        return [*streams, *folders_, lease.sessions_dir() / f"{sid}.state", mailbox.asks_dir(sid),
                mailbox.requests_dir(sid), self.board.root / "answers", mailbox.handover_path(sid)]

    def poke(self) -> None:
        """Something of this run's changed (any thread): an idle wait ends now."""
        loop = self._loop
        if loop is None:
            return
        for event in (self._wake, self._reader_wake):
            if event is not None:
                with contextlib.suppress(RuntimeError):  # its loop has closed
                    loop.call_soon_threadsafe(event.set)

    async def pause(self, seconds: float, event: asyncio.Event | None) -> None:
        """The wait between two polls: `seconds`; in the daemon host, once nothing
        new has come for IDLE_AFTER_S, up to IDLE_POLL_S, ended by a poke."""
        idle_after, idle_poll = _idle_timings()
        if not self.wakeable or event is None or self.stopping or self.clock() - self.changed_at < idle_after:
            await asyncio.sleep(seconds)
            return
        try:
            await asyncio.wait_for(event.wait(), idle_poll)
        except asyncio.TimeoutError:
            return
        # Consumed after the wait, never before it: a poke during the look that
        # follows sets it again, so the next wait ends at once (none is lost). Idle
        # until a look finds something new (`changed_at`), not because of a poke.
        event.clear()

    async def loop(self) -> int:
        self._loop = asyncio.get_running_loop()
        if self.wakeable:
            self._wake, self._reader_wake = asyncio.Event(), asyncio.Event()
        self._renew()
        await folders.baseline(self.store, self.session.cwd, self.session.home,
                               excluded=self.exclusions.path_excluded)
        if self.replay is None and self._inline_unannounced():
            # Back from `/probe inline`: the folders now, before the next edit, so
            # an edit the agent made inside the stretch is not folded into one
            # diff with the next edit (stamped after the stretch, the writer's).
            await self._check_folders(folders.working_folders(self.store, self.session.cwd, self.session.home),
                                      force=True)
        if self.replay is None and mailbox.enabled(source=self.session.source):
            from probe.daemon.lanes.reader import ReaderLane
            from probe.daemon.lanes.run_alerts import RunAlertLane

            self.reader = ReaderLane(self)
            self.reader.start()
            # Its own task, never a step of `tick`: tick returns early in `read
            # only (daemon)` and awaits whole bites, and an alert must not wait
            # behind either.
            self.run_alerts = RunAlertLane(self)
            self.run_alerts.start()
        if self.replay is None:
            from probe.daemon.lanes.audit import AuditLane

            self.audit = AuditLane(self)
        # The session's traces go up beside the loop, never in its way (`shipper.py`).
        uploads = shipper_mod.start(self.session.session_id) if self.replay is None else None
        try:
            while True:
                if self.stopping and self.reader is not None:
                    await self.reader.stop()  # nobody is left to deliver to
                    self.reader = None
                if self.stopping and self.run_alerts is not None:
                    await self.run_alerts.stop()  # nobody is left to tell
                    self.run_alerts = None
                if self.stopping and self.audit is not None:
                    await self.audit.stop()  # cut short before its write: the note stays due
                    self.audit = None
                if self.on_tick is not None:
                    self.on_tick()
                seq, ran = self.store.next_seq(), self.last_run_at
                code = await self.tick()
                if code is not None:
                    return code
                if self.store.next_seq() != seq or self.last_run_at != ran:
                    self.changed_at = self.clock()
                await self.pause(POLL_S, self._wake)
        finally:
            if self.reader is not None:
                await self.reader.stop()
                self.reader = None
            if self.run_alerts is not None:
                await self.run_alerts.stop()
                self.run_alerts = None
            if self.audit is not None:
                await self.audit.stop()
                self.audit = None
            if uploads is not None:
                await uploads.stop()
from probe.daemon.worker.error_log import _device_error  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.files import inbox_path  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.install import install_replaced  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.failures import STATE_DAEMON  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.run_end import REINSTALLED  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.supervisor import inline_exit_code  # noqa: E402 -- pieces need each other; the front door loads this one first
