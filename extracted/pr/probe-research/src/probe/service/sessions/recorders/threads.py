"""each session's recorder thread: run it, retry with backoff while its agent runs, hand over to the worker at the end."""

from __future__ import annotations
import contextlib
import os
import threading
import time
from pathlib import Path
from typing import Callable


from .. import capture_gate
from ....foundation.service_api import procid
from ...watch.incident import Family
from probe.service.sessions.recorders.recording import DEFERRED_KEY, RECORD_STEP, Recording
#: The first wait after a recorder failed (doubling to MAX_RETRY_S); tests shorten it.
RETRY_ENV = "PROBE_SERVICE_RECORDER_RETRY_S"
FIRST_RETRY_S = 5.0
MAX_RETRY_S = 300.0
#: A recorder that ended for another reason (another recorder holds the
#: session, a killswitch, no token yet) looks again this many first waits
#: later (15 s) while its agent runs.
STOPPED_RETRIES = 3
#: After its agent exited, a recorder that failed is tried this many times more
#: (its last pass and FINALIZE are what is left to do).
AFTER_EXIT_TRIES = 3
#: A paused session's daemon worker (the service was its parent) is asked to
#: hand over, dated this far ahead: it sees its parent gone within seconds, and
#: without the ask it would end its session (fail the writer requests waiting,
#: release its lease); the next service's worker takes the lock and clears it.
HANDOVER_AHEAD_S = 180.0
#: An attempt that ran this long before it failed resets the wait to the first.
HEALTHY_RUN_S = 600.0


def _first_retry() -> float:
    try:
        return max(0.05, float(os.environ.get(RETRY_ENV, FIRST_RETRY_S)))
    except ValueError:
        return FIRST_RETRY_S


class ThreadsMixin:
    """Part of RecorderHost: its methods run with `self` the RecorderHost; compose() folds them into RecorderHost."""

    # -- threads -------------------------------------------------------------------

    def _start(self, session: dict, *, delay: float = 0.0) -> Recording:
        controls = self.hosted.Controls()
        publish = getattr(controls, "claim", None)
        if callable(publish):
            # The tap's loop publishes its claim through this (`Controls.claim`,
            # tap 0.10.6): heard here too, at once (`claimed`). A tap that
            # publishes none is read by the hint lane without it.
            sid = session["sid"]

            def claim(folder: str | None, _publish: Callable = publish, _sid: str = sid) -> None:
                _publish(folder)
                with contextlib.suppress(Exception):
                    self._claimed(_sid)

            with contextlib.suppress(Exception):
                controls.claim = claim
        if self.workers is not None:
            # A tap that knows it hands its worker over (`workers.Link`); an
            # older one never reads it and supervises its own.
            with contextlib.suppress(Exception):
                controls.workers = self.workers.link(session["sid"])
        rec = Recording(session["sid"], session, controls)
        rec.thread = threading.Thread(target=self._guard, args=(rec, delay), name=f"recorder-{session['sid'][:12]}",
                                      daemon=True)
        with self._gate_lock:
            # The one it replaces (finishing: a resume after the session's
            # end) touches nothing of the session's from here (`_superseded`);
            # its gaps go on with this one.
            previous = self.recordings.get(session["sid"])
            if previous is not None:
                self._carry_gaps(previous, session)
            self.recordings[session["sid"]] = rec
            # Its gaps for the drains here before anything else; its gap file
            # decides for them too until its first look merged it (`_gate`).
            capture_gate.unsettled(rec.sid, capture_gate.gaps_of(session))
            capture_gate.live(rec.sid, False)
        rec.deferred = session.get(DEFERRED_KEY) is True
        with contextlib.suppress(Exception):
            # Its switch first: an off session's gap opens now, before anything
            # could stage it (`capture_gate`), and the drains here leave it alone.
            self._gate(rec, first=True, on_loop=True)
        rec.thread.start()
        self._ensure_monitor()
        self.log(f"recorder: session {session['sid']} recorded here{' (off: held)' if self._is_off(rec) else ''}")
        return rec

    def _owner_alive(self, rec: Recording) -> bool | None:
        owner = rec.params.get("owner")
        if not isinstance(owner, dict):
            return None
        try:
            return procid.alive(int(owner["pid"]), str(owner["start_time"]))
        except (KeyError, TypeError, ValueError):
            return None

    def _guard(self, rec: Recording, start_after: float = 0.0) -> None:
        """The session's thread: its recorder, again after a failure, while its agent runs."""
        delay = _first_retry()
        finals = 0
        until = time.monotonic() + start_after
        while time.monotonic() < until and not rec.controls.stop.is_set():
            if rec.controls.pause.wait(min(0.2, max(0.0, until - time.monotonic()))):
                return  # the service stops before it began: the next one resumes it
        while True:
            if self._needs_hold(rec):
                # Probe is off for it (or a gap waits to be settled): nothing of
                # it is captured until the switch is on again (`capture_gate`).
                if self._hold(rec) != RECORD_STEP:
                    break
            began = time.monotonic()
            rec.record_since, rec.in_record = began, True
            try:
                outcome, detail = self.hosted.record(rec.params, rec.controls)
            finally:
                rec.in_record = False
            rec.last = f"{outcome}{': ' + detail if detail else ''}"
            if rec.hold_asked:
                # Its loop left because the switch turned off, not for a restart:
                # held from here (its stop too, if it came: the hold finalizes).
                rec.hold_asked = False
                if not self._closing:
                    rec.controls.pause.clear()
                    continue
            if outcome in (self.hosted.ENDED, self.hosted.PAUSED) or rec.controls.pause.is_set():
                break
            if rec.controls.stop.is_set():
                # Its last pass failed: tried again a few times, FINALIZE is what is left.
                if outcome != self.hosted.FAILED or finals >= AFTER_EXIT_TRIES:
                    break
                finals += 1
                rec.failures += 1
                self.log(f"recorder: session {rec.sid}'s last pass failed ({detail}); again in 2 s")
                if rec.controls.pause.wait(2.0):
                    break
                continue
            if time.monotonic() - began >= HEALTHY_RUN_S:
                delay = _first_retry()
            if self._owner_alive(rec) is False and (outcome != self.hosted.FAILED or rec.failures >= AFTER_EXIT_TRIES):
                break  # the agent is gone and its recorder did what it could
            if outcome == self.hosted.FAILED and self._owner_alive(rec) is False:
                # Its agent is gone: its last tries 2 s apart, as after its stop,
                # never the back-off (up to MAX_RETRY_S, holding the service).
                rec.failures += 1
                self.log(f"recorder: session {rec.sid} failed after its agent exited ({detail}); again in 2 s")
                if rec.controls.pause.wait(2.0):
                    break
                continue
            if outcome == self.hosted.FAILED:
                rec.failures += 1
                self.log(f"recorder: session {rec.sid} failed ({detail}); again in {delay:.0f} s")
                if self._owner_alive(rec) is not False:
                    # While its agent runs: one event of `recorder` (3 in 15 min
                    # are a report, plan B2), with its consent its own.
                    self.incident(Family.RECORDER, "failing", rec.sid, {
                        "detail": str(detail)[:300], "failures": rec.failures, "tap_version": self.tap_version,
                    }, env=rec.params.get("env"))
                wait = delay
                delay = min(delay * 2, MAX_RETRY_S)
            else:
                wait = _first_retry() * STOPPED_RETRIES
            if self._backoff(rec, wait):
                break  # paused: the next service resumes it
            # Waited out, or its SessionEnd came meanwhile: once more (with
            # `stop` set the loop makes its last pass and FINALIZE).
        loop = self._loop_getter()
        if loop is not None:
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(self._ended, rec)

    def _backoff(self, rec: Recording, seconds: float) -> bool:
        """Wait `seconds`, ending early when the session's stop comes (its last
        pass runs then, not after the wait), or its switch turns off (it is
        held from then). True when paused instead."""
        until = time.monotonic() + seconds
        while time.monotonic() < until:
            if rec.controls.pause.wait(min(0.2, max(0.0, until - time.monotonic()))):
                if rec.hold_asked and not self._closing:
                    rec.hold_asked = False
                    rec.controls.pause.clear()
                    return False
                return True
            if rec.controls.stop.is_set():
                return False
            if rec.wake.is_set():
                rec.wake.clear()
                return False
            if self.gated and self._is_off(rec):
                return False
        return False

    def _ended(self, rec: Recording) -> None:
        # A session that ended while off and was not finished before this
        # service stopped stays saved: the next service finishes it.
        # One the server refused for good is dropped whatever (`_hold`).
        unfinished = self._closing and bool(capture_gate.gaps_of(rec.params)) and not rec.dropped
        if self.recordings.get(rec.sid) is rec and not unfinished and (
                rec.controls.stop.is_set() or not rec.controls.pause.is_set() or rec.dropped):
            del self.recordings[rec.sid]
            capture_gate.live(rec.sid, False)
            self.log(f"recorder: session {rec.sid} done ({rec.last})")
            self._save()
            # What it wrote while off stays out of every drain here while it
            # has a gap (in memory and in its gap file).
        if rec.controls.stop.is_set() or not rec.controls.pause.is_set():
            # Its tap released the worker on the way out; this covers a loop
            # that never got that far. A newer recording's claim is kept.
            link = getattr(rec.controls, "workers", None)
            if link is not None:
                link.release()
        self._changed()

    def _ending(self, rec: Recording) -> bool:
        """Did its SessionEnd come (the tap's own check: its shutdown sentinel,
        also for a `/clear`, which never asks the service to finish it)?"""
        ending = getattr(self.hosted, "ending", None)
        if ending is None:
            return False
        try:
            return bool(ending(rec.params))
        except Exception:  # noqa: BLE001
            return False

    def _hand_over(self, rec: Recording) -> None:
        """Ask the session's running daemon worker to hand over (see HANDOVER_AHEAD_S).
        Never for a session that is ending: there is no next worker to take
        its queue, so it finishes it itself."""
        if self._ending(rec):
            return
        state = rec.params.get("state_dir")
        if not isinstance(state, str) or not state:
            return
        lock = Path(state) / "daemon" / f"{rec.sid}.lock"
        try:
            from ... import updater

            if not lock.exists() or not updater._flock_held(lock):
                return
            marker = lock.with_suffix(".handover")
            marker.touch()
            ahead = time.time() + HANDOVER_AHEAD_S
            os.utime(marker, (ahead, ahead))
        except Exception:  # noqa: BLE001 -- the worker ends its session as before
            pass

    @staticmethod
    def _holds(rec: Recording) -> bool | None:
        """Whether this recorder holds the session's journal claim now: the
        folder its loop published (`Controls.claim`), which a thread alive in
        its retry wait does not. None from a tap that publishes none."""
        if not hasattr(rec.controls, "claimed"):
            return None
        return rec.controls.claimed is not None
