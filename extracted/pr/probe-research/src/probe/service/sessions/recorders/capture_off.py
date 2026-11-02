"""Probe off (capture_gate): watch each session's switch, hold its recorder while off, settle the gap when it comes back on."""

from __future__ import annotations
import contextlib
import os
import threading
import time
from pathlib import Path
from typing import Any


from .. import capture_gate
from probe.service.sessions.recorders.recording import DEFERRED_KEY, ENDED_STEP, PAUSED_STEP, RECORD_STEP, Recording
from probe.service.sessions.recorders.threads import AFTER_EXIT_TRIES, MAX_RETRY_S, _first_retry
#: A held session's claim (`capture_gate.Claim`) is looked for this soon after
#: a look that found none, doubling to CLAIM_MAX_S, and at once when a `tap
#: watch` offers the session (it lets go of the claim then).
CLAIM_EVERY_S = 1.0
CLAIM_MAX_S = 60.0


class CaptureOffMixin:
    """Part of RecorderHost: its methods run with `self` the RecorderHost; compose() folds them into RecorderHost."""

    # -- Probe off (`capture_gate`) ----------------------------------------------------

    def off(self, params: dict) -> bool:
        """Does this session's switch read `off` now (`session.record`, a resume)?"""
        if not self.gated:
            return False
        return capture_gate.is_off(params)

    def _superseded(self, rec: Recording) -> bool:
        """A newer recording of the session took over (a resume after its end:
        `record` starts a fresh one): this one touches nothing of the session's."""
        return self.recordings.get(rec.sid) is not rec

    @staticmethod
    def _is_off(rec: Recording) -> bool:
        """Held for its switch: an open gap (seen `off`, not on again yet)."""
        return capture_gate.is_open(capture_gate.gaps_of(rec.params))

    def held_off(self, sid: object) -> bool:
        """Is this session recorded here and held because Probe is off for it?"""
        rec = self.recordings.get(sid) if isinstance(sid, str) else None
        return bool(rec is not None and rec.thread is not None and rec.thread.is_alive() and self._is_off(rec))

    def _transcript(self, rec: Recording) -> tuple[Path | None, bool]:
        """`(path, looked)` (`capture_gate.find_transcript`), the path kept once found."""
        if rec.transcript is not None:
            return rec.transcript, True
        path, looked = capture_gate.find_transcript(self._tap(), rec.params)
        rec.transcript = path
        return path, looked

    def _gate(self, rec: Recording, *, first: bool = False, on_loop: bool = False) -> bool:
        """Look at the session's switch: open its gap when it reads `off`,
        close it when it reads anything else. True while it is off. `first`:
        this service has not seen the session before (a new recording, or one
        resumed with no gap): found off, its gap starts at the transcript's
        first byte, so nothing not yet sent is sent (when it turned off is
        not known; a line written on and not yet sent is lost, never one
        written off sent). `on_loop`: called on the service's loop (an RPC): the
        gap file is written later, by the recorder thread or the monitor."""
        if not self.gated or self._superseded(rec):
            return False
        tap = self._tap()
        off = capture_gate.switch(rec.params) == capture_gate.OFF
        # Its gap file, until it has been read once (a read that fails now is
        # tried again at the next look, the session held meanwhile).
        merging = not rec.file_merged
        signature = capture_gate.file_signature(self._sessions_dir(rec), rec.sid) if merging else ()
        from_file = capture_gate.read_gap_file_raw(self._sessions_dir(rec), rec.sid) if merging else []
        # Where the transcript stands, read before the lock (a file read) and
        # only when the switch moved past the session's gaps. None when it
        # cannot be read, or its rollout could not be looked for.
        moved = merging or first or off != capture_gate.is_open(capture_gate.gaps_of(rec.params))
        mark = None
        if moved and not (off and first):
            path, looked = self._transcript(rec)
            mark = capture_gate.mark_now(tap, path) if looked else None
        with self._gate_lock:
            if self._superseded(rec):
                return False
            gaps = capture_gate.gaps_of(rec.params)
            changed = False
            if merging and from_file is not None:
                # What an earlier recording of it left unsettled (its gap file
                # outlives `recorders.json`, a restart and a pruned `.state`).
                merged = capture_gate.normalized(gaps + from_file)
                if merged != gaps:
                    gaps, changed = merged, True
            if moved and off != capture_gate.is_open(gaps):
                if off:
                    # Found off at its first look: from its first byte. An
                    # opening whose mark does not read starts at 0 too.
                    gaps, changed = capture_gate.opened(gaps, 0 if first or mark is None else mark), True
                elif mark is not None:
                    gaps, changed = capture_gate.closed(gaps, mark), True
                # else: its transcript cannot be read now: the gap stays open
                # (it is held) and the next look closes it.
            if changed:
                self._keep_gaps(rec, gaps)
            else:
                capture_gate.unsettled(rec.sid, gaps)
            if merging and from_file is not None:
                # Its record holds all its gaps now, published above: from
                # here its record decides for the drains here, not its file.
                rec.file_merged = True
                rec.file_sig = signature
                capture_gate.live(rec.sid, True)
        if not on_loop:
            self._flush_gap_file(rec)
        elif rec.gap_file_due:
            rec.gate_wake.set()  # its recorder thread (or the monitor) writes it
        if changed:
            what = "off: not captured" if off else "on: captured outside its gaps"
            self.log(f"capture gate: session {rec.sid} is {what}; its gaps (transcript bytes) are {gaps}")
            self._save()
            self._notify()
        return off

    def wake(self, sid: object) -> None:
        """Its session ended (its SessionEnd, or its agent exited): its
        recorder looks now instead of at the end of the wait it is in (up to
        MAX_RETRY_S while the server refuses or cannot be reached), which kept
        the service alive that long after the last session ended. A held one
        (`_hold`) waits on `gate_wake`, a running one between two failed
        passes (`_backoff`) on `wake`. A look decides nothing by itself: the
        recorder still reads whether its session ended, and a finish keeps its
        own pace (`_hold`'s 2 s between its last tries)."""
        rec = self.recordings.get(sid) if isinstance(sid, str) else None
        if rec is not None:
            rec.gate_wake.set()
            rec.wake.set()

    def look(self, sid: object) -> None:
        """`session.recording`'s look at the session's switch, at once (the CLI
        that moved it asks this right after): its gap opens or closes with the
        transcript as it is now, before the agent writes its next line. A
        session that turned off while its loop ran is told to leave."""
        rec = self.recordings.get(sid) if isinstance(sid, str) else None
        if rec is None or rec.thread is None or not rec.thread.is_alive() or rec.controls.stop.is_set():
            return
        try:
            off = self._gate(rec, on_loop=True)
        except Exception:  # noqa: BLE001 -- the recorder's own look comes within POLL_S
            return
        if off and not rec.held and rec.in_record:
            self._ask_hold(rec)
        rec.gate_wake.set()

    def _ask_hold(self, rec: Recording) -> None:
        if rec.hold_asked or rec.controls.pause.is_set() or rec.controls.stop.is_set():
            return
        rec.hold_asked = True
        rec.controls.pause.set()  # its loop leaves at its next check; the guard holds it

    def _notify(self) -> None:
        """From any thread: what keeps the service alive changed."""
        loop = self._loop_getter()
        if loop is not None:
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(self._changed)

    def _ensure_monitor(self) -> None:
        if not self.gated:
            return
        with self._monitor_lock:
            if self._monitor is not None and self._monitor.is_alive():
                return
            self._monitor = threading.Thread(target=self._watch_switches, name="capture-gate", daemon=True)
            self._monitor.start()

    def _watch_switches(self) -> None:
        """Every POLL_S: each recorded session's switch (`_gate`); one that
        turned off while its loop runs is told to leave. Ends with the service,
        or once nothing has been recorded for a minute (`_start` starts it again)."""
        quiet_since = time.monotonic()
        while not self._closing:
            live = [r for r in list(self.recordings.values()) if r.thread is not None and r.thread.is_alive()]
            if live:
                quiet_since = time.monotonic()
            elif time.monotonic() - quiet_since > 60.0:
                with self._monitor_lock:
                    if not any(r.thread is not None and r.thread.is_alive() for r in self.recordings.values()):
                        self._monitor = None
                        return
            for rec in live:
                if rec.hold_asked or rec.controls.stop.is_set() or rec.controls.pause.is_set():
                    continue
                with contextlib.suppress(Exception):
                    # A held one too: one that turns off again while it settles
                    # has its gap opened now (its settle reads the gaps live).
                    if self._gate(rec) and rec.in_record and not rec.held:
                        self._ask_hold(rec)
            time.sleep(capture_gate.POLL_S)

    def _needs_hold(self, rec: Recording) -> bool:
        """Before its loop runs: is the session off, or a gap not settled yet?"""
        if not self.gated:
            return False
        try:
            return self._gate(rec) or bool(capture_gate.gaps_of(rec.params)) or not rec.file_merged
        except Exception:  # noqa: BLE001
            return not rec.file_merged

    def _settled(self, rec: Recording, done: list, *, everything: bool = False) -> None:
        """The gaps `done` (the ones a settle ran with) are settled: the
        server's cursor is past them. A gap opened since, or still open, stays
        (`everything`: the session ended and was finalized, so none does).
        Never for a recording a newer one of the session replaced."""
        with self._gate_lock:
            if self._superseded(rec):
                return
            gaps = capture_gate.gaps_of(rec.params)
            if everything:
                keep: list = []
            else:
                finished = {(g[0], g[1]) for g in done if g[1] is not None}
                keep = [g for g in gaps if g[1] is None or (g[0], g[1]) not in finished]
            rec.settled_gaps.update((g[0], g[1]) for g in gaps if g not in keep)
            self._keep_gaps(rec, keep)
        self._flush_gap_file(rec)
        self._save()

    def _wait_held(self, rec: Recording, seconds: float) -> bool:
        """Wait up to `seconds`, ending early on a wake, the session's stop, or
        the service's: True when the service stops (`close`)."""
        rec.gate_wake.wait(max(0.0, seconds))
        rec.gate_wake.clear()
        return rec.controls.pause.is_set() or self._closing

    def _hold(self, rec: Recording) -> str:
        """Probe is off for this session (or a gap waits to be settled): its
        loop does not run. Returns RECORD once the switch is on again and the
        gaps are settled (the loop records on from there), PAUSED when the
        service stops (the next one holds it again), ENDED when the session
        ended (settled to its end and finalized, or never sent at all: its gap
        file then stays). A session that ends while the server cannot be
        reached is retried here, slowly, and by every later service: never
        given up while it has a gap, unless it is refused for good (no login
        here, or the Probe gateway's own 401/403/404/422: `capture_gate.settle`):
        then it is dropped from `recorders.json` and its gap file stays. A recording a newer one of the session replaced (a
        resume after its end) leaves at once, touching nothing of the session's
        (ENDED)."""
        tap = self._tap()
        claim = capture_gate.Claim(tap, rec.params)
        published = False
        rec.held = True
        rec.last = "off"
        if self._is_off(rec):
            loop = self._loop_getter()
            if loop is not None:
                with contextlib.suppress(RuntimeError):
                    loop.call_soon_threadsafe(self._held, dict(rec.params))
        self._notify()
        retry = _first_retry()
        #: When the next try to settle its gaps is due (a failed one backs off):
        #: until then the loop looks again every HELD_POLL_S, so a session that
        #: ends (or turns off) meanwhile is seen at once, and no wake brings a
        #: try forward.
        settle_at = 0.0
        finals = 0
        claim_at, claim_every = 0.0, CLAIM_EVERY_S
        current = lambda: not self._superseded(rec)  # noqa: E731
        try:
            while True:
                if rec.controls.pause.is_set() or self._closing:
                    return PAUSED_STEP
                if self._superseded(rec):
                    # A resume after its end started a fresh recording, which
                    # carried its gaps over: that one settles and finishes it.
                    rec.last = "ended off: superseded"
                    return ENDED_STEP
                ending = rec.controls.stop.is_set() or self._ending(rec) or self._owner_alive(rec) is False
                off = self._gate(rec)
                gaps = capture_gate.gaps_of(rec.params)
                if not rec.file_merged:
                    # Its gap file could not be read yet: nothing of it is
                    # settled or recorded until it is (it may hold a gap).
                    if self._wait_held(rec, capture_gate.HELD_POLL_S):
                        return PAUSED_STEP
                    continue
                if ending:
                    if not rec.finishing and not rec.deferred:
                        rec.finishing = True
                        self._notify()
                    if published:
                        self._publish(rec, None)
                        published = False
                    claim.release()
                    done = capture_gate.settle(tap, rec.params, gaps, finalize=True, log=self.log, current=current)
                    if self._superseded(rec):
                        continue  # left at the top: nothing of the session's is touched
                    if done == capture_gate.REFUSED:
                        # Refused for good: no service tries again
                        # (`_ended` drops its record); its gap file stays, so
                        # nothing of the stretch is ever sent.
                        rec.dropped = True
                        capture_gate.write_marker(tap, rec.params, None)
                        rec.finishing = False
                        rec.last = "ended off: refused, not tried again"
                        self.log(f"capture gate: session {rec.sid} ended while off and the server refused it; "
                                 "not tried again, what it wrote while off stays unsent")
                        return ENDED_STEP
                    if done in (capture_gate.DONE, capture_gate.DELETED, capture_gate.KEPT):
                        if done != capture_gate.KEPT:
                            self._settled(rec, gaps, everything=True)
                        # KEPT: it never sent anything; its gap file stays, so a
                        # later capture of it skips the stretch too.
                        capture_gate.write_marker(tap, rec.params, None)
                        rec.finishing = False
                        rec.last = f"ended off ({done})"
                        return ENDED_STEP
                    finals += 1
                    if finals >= AFTER_EXIT_TRIES and not rec.deferred:
                        # The server does not answer: tried again here every few
                        # minutes, and by every later service, never given up
                        # (its gaps stay saved); it keeps no service alive.
                        rec.deferred, rec.finishing = True, False
                        rec.params[DEFERRED_KEY] = True  # a later service starts it deferred
                        self._save()
                        rec.last = "ended off: not finished yet"
                        self.log(f"capture gate: session {rec.sid} ended while off and could not be finished yet; "
                                 "tried again later, what it wrote while off stays unsent")
                        self._notify()
                    if not rec.deferred:
                        # 2 s between the last tries, whatever wakes it: one end
                        # wakes it up to three times (its SessionEnd, `session.end`,
                        # its agent's exit), which must not spend the tries at once.
                        if rec.controls.pause.wait(2.0) or self._closing:
                            return PAUSED_STEP
                        rec.gate_wake.clear()
                        continue
                    if self._wait_held(rec, retry):
                        return PAUSED_STEP
                    retry = min(retry * 2, MAX_RETRY_S)
                    continue
                if off:
                    self._own_marker(tap, rec)
                    now = time.monotonic()
                    if not published and (now >= claim_at or rec.claim_now):
                        # A journal holding its row is looked for when it is
                        # offered (a `tap watch` letting go), else less and less
                        # often: a scan of the journal folders.
                        rec.claim_now = False
                        folder = claim.take()
                        if folder is not None:
                            self._publish(rec, folder)
                            published = True
                        else:
                            claim_at, claim_every = now + claim_every, min(claim_every * 2, CLAIM_MAX_S)
                    if self._wait_held(rec, capture_gate.HELD_POLL_S):
                        return PAUSED_STEP
                    continue
                if rec.deferred:
                    # Its agent is back (a new `session.record` for it): live again.
                    rec.deferred = False
                    rec.params.pop(DEFERRED_KEY, None)
                    finals = 0
                    self._save()
                if published:
                    self._publish(rec, None)
                    published = False
                claim.release()
                if not gaps:
                    return RECORD_STEP
                if time.monotonic() < settle_at:
                    if self._wait_held(rec, min(capture_gate.HELD_POLL_S, settle_at - time.monotonic())):
                        return PAUSED_STEP
                    continue
                done = capture_gate.settle(tap, rec.params, gaps, finalize=False, log=self.log, current=current)
                if self._superseded(rec):
                    continue
                if done in (capture_gate.DONE, capture_gate.DELETED):
                    # Then look again: it may have turned off while this ran.
                    self._settled(rec, gaps)
                    retry = _first_retry()
                    settle_at = 0.0
                    continue
                rec.last = "off: settling"
                settle_at = time.monotonic() + retry
                retry = min(retry * 2, MAX_RETRY_S)
        finally:
            if published:
                self._publish(rec, None)
            claim.release()
            rec.held = False
            self._notify()

    def _own_marker(self, tap: Any, rec: Recording) -> None:
        """While it is held off and this service runs, its `.hosted` marker
        names this service, as for any session it records: a service before
        this one wrote the session's agent there when it stopped (`close`)."""
        if self._closing:
            return
        owner = rec.params.get("owner") if isinstance(rec.params.get("owner"), dict) else {}
        pid = owner.get("pid")
        if isinstance(pid, int) and not isinstance(pid, bool) and pid != os.getpid() \
                and capture_gate.marker_names(tap, rec.params) == str(pid):
            capture_gate.write_marker(tap, rec.params, os.getpid())

    @staticmethod
    def _publish(rec: Recording, folder: str | None) -> None:
        """The journal claim a held recorder holds, as its loop publishes one
        (`Controls.claim`): `service.status` says it holds the session."""
        with contextlib.suppress(Exception):
            publish = getattr(rec.controls, "claim", None)
            if callable(publish):
                publish(folder)
