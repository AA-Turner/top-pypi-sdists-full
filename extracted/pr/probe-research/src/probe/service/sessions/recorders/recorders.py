"""Every session's recorder, as a thread of the service (plan A2, D2, D3, D39).

    session.record     a session's SessionStart (and each prompt) asks the
                       service to record it (`tap record`): registered as
                       `session.register` would, then recorded on a thread of
                       this process running the installed tap package's
                       `tap.hosted.record` (one recorder codebase, two hosts:
                       `tap watch` where the service cannot run)
    session.recording  is it recorded here now?
    session.finish     its SessionEnd: finish it (last pass, FINALIZE) and say
                       whether that happened within `wait`

    the tap            imported once, from the newest tap plugin folder a
                       session named. A session that names a NEWER one than is
                       loaded gets `restart`: the service restarts (its
                       recorders pause, then resume from their saved progress
                       in the next service, which loads the newer tap). After
                       an update the newest tap the sessions' agents have
                       INSTALLED is wanted the same way (`follow_installed`:
                       Claude Code's install ledger names it, Codex keeps the
                       one version folder), and every service start loads the
                       newest installed one that loads (`installed_tap`), so a
                       session left open across an update records on the new
                       tap without asking for it (plan C9)
    one at a time      the tap journal's live claim: a session whose own
                       `tap watch` still runs is never recorded twice (D39);
                       its thread waits, and takes over once that one is gone.
                       A `tap watch` that started because no service answered
                       asks `session.record` itself once one does, then lets
                       go of the claim (the tap's `tap/handback.py`)
    the guard          each session's thread restarts after a failure (5 s,
                       doubling to 5 min) while its agent runs: one bad
                       transcript stops one session's recording, never another's
    restarts           `recorders.json` (0600, beside the registry): what to
                       resume when the next service starts -- each session's
                       arguments and the variables a recorder reads (the tap
                       client sends only those, `tap.record_client.TAP_ENV_*`),
                       and the newer tap a session asked for, loaded first.
                       A saved tap folder may be gone by then: Codex replaces
                       a plugin's version folder when it updates it, and an
                       update cycle does that just before it restarts this
                       service. Such a session resumes from the version folder
                       that replaced it (`_replacement`), and one session's
                       missing folder never keeps it from the tap another's
                       loaded; one that still cannot resume is said by sid
    an owner           only a session whose agent process is known: the
                       recorder keeps no heartbeat of its own, and ends with
                       that process (the tap's own owner check); one without
                       gets `tap watch` as before
    its worker         each recording's controls carry a `workers.Link`: a tap
                       that knows it hands the session's daemon worker to the
                       service's own supervisor (`workers.py`); its loop's end
                       releases it, and so does the recording's end here
    Probe off          a session whose switch reads `off` is not captured
                       here (`capture_gate`): its recorder is held (its loop
                       does not run) and keeps the stretch as a gap (in its
                       record and its gap file); once the switch is on again
                       it settles the gap (the lines in it go as nothing, so
                       they are never sent) and records on. A held session
                       never keeps the service alive, and the service accepts
                       one (`session.record`) so that no `tap watch` records
                       it instead

    its copy           the tap is imported from a copy of its package this
                       service makes and owns (`_pin`, in its machine folder),
                       never from the agent's plugin cache it came from: Codex
                       deletes a plugin's version folder when it installs the
                       next, and the tap still imports modules and reads data
                       files of its own long after it loaded (plan C7)

Stdlib only at import (the start path; plan S1). The tap is imported when the
first session is recorded.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import threading
import time
from pathlib import Path
from typing import Any, Callable


from .. import capture_gate
from ....foundation.compose.compose import compose
from probe.service.sessions.recorders.capture_off import CaptureOffMixin
from probe.service.sessions.recorders.gaps import GapsMixin
from probe.service.sessions.recorders.recording import Recording
from probe.service.sessions.recorders.restarts import RestartsMixin
from probe.service.sessions.recorders.tap import TapMixin, _numbers, installed_tap
from probe.service.sessions.recorders.threads import ThreadsMixin
#: How long a stopping service waits for its recorders to pause, all together.
PAUSE_JOIN_S = 5.0


@compose
class RecorderHost(
    TapMixin,
    GapsMixin,
    CaptureOffMixin,
    ThreadsMixin,
    RestartsMixin,
):
    def __init__(
        self,
        *,
        log: Callable[[str], None],
        loop_getter: Callable[[], Any],
        changed: Callable[[], None] = lambda: None,
        workers: Any = None,
        incident: Callable[..., None] = lambda *args, **kwargs: None,
        claimed: Callable[[str], None] = lambda sid: None,
        held: Callable[[dict], None] = lambda params: None,
    ) -> None:
        self.log = log
        #: Told a session's id, on its recorder's thread, each time its loop
        #: takes or lets go of the session's claim (what `hints.followed`
        #: reads): the service's hint lane looks again then.
        self._claimed = claimed
        #: Told a session's record (on the loop) when its switch turns it off
        #: while it was recorded: the service registers it as `off` (its tap's
        #: own registration ended with its loop).
        self._held = held
        #: The service stops (`close`): a held recorder leaves, never records.
        self._closing = False
        #: The capture gate works with the loaded tap (`capture_gate.install`);
        #: False for a tap without what it needs: nothing is held then.
        self.gated = False
        self._tapns: Any = None
        self._gate_lock = threading.Lock()
        #: Held while a gap file is written (an fsync): never `_gate_lock`,
        #: which every session's gate and the service's loop take.
        self._gap_file_lock = threading.Lock()
        self._save_lock = threading.Lock()
        self._monitor: threading.Thread | None = None
        self._monitor_lock = threading.Lock()
        #: The service's watch (`watch.Watch.note`): a failing recorder, a tap
        #: that will not load (crash-report plan B2).
        self.incident = incident
        self._loop_getter = loop_getter
        self._changed = changed
        #: The service's worker supervisor (`workers.WorkerHost`), or None.
        self.workers = workers
        self.recordings: dict[str, Recording] = {}
        self.tap_root: str | None = None
        self.tap_copy: str | None = None
        self.tap_version: str | None = None
        self.hosted = None  # the `tap.hosted` module, once imported
        #: A newer tap than is loaded, which a session named: `(root, version)`.
        #: The service restarts and its next copy loads this one first.
        self.wanted: tuple[str, str] | None = None
        #: The newer tap this service was restarted onto and could not load: no
        #: session restarts it onto that version again (a restart on purpose is
        #: no start to back off from, `client.forget_start`, so nothing else
        #: would end that loop); the session's own tap records it.
        self.unloadable: str | None = None
        #: The last `follow_installed` saw a newer installed tap folder its agent
        #: may still be writing (`_settled`): its caller asks again soon.
        self.settling = False

    def check(self, params: dict) -> dict | None:
        """Can `session.record` record this session here? None when it can,
        else its answer (the caller then registers nothing)."""
        session = self._valid(params)
        if not isinstance(session.get("owner"), dict):
            return {"recording": False, "reason": "no_owner"}
        if self.hosted is not None and _numbers(session["tap_version"]) > _numbers(self.tap_version or ""):
            if self.unloadable is not None and _numbers(session["tap_version"]) <= _numbers(self.unloadable):
                return {"recording": False, "reason": "tap_unloadable"}
            # A newer tap than the one loaded: restart onto it, as for a CLI update.
            if self.wanted is None or _numbers(session["tap_version"]) > _numbers(self.wanted[1]):
                self.wanted = (session["tap_root"], session["tap_version"])
                self._save()
            return {"recording": False, "restart": True}
        if not self._load(session["tap_root"], session["tap_version"]):
            return {"recording": False, "reason": "no_tap"}
        return None

    def record(self, params: dict) -> dict:
        """`session.record`'s recorder half, after `check` (and the caller
        registered the session).

        A recorder that is FINISHING is never kept for the session asked
        again: its `stop` is set (its SessionEnd, or its loop saw the session's
        shutdown sentinel: the tap sets it then, from 0.10.17). A resume right
        after the session's end (pi `--continue` after a quit) gets a fresh
        recorder, which takes the session over once the finishing one lets go
        of it (D39): kept, the finishing one would FINALIZE and end, and
        nothing would record the resumed session. (A tap before 0.10.17 says
        nothing when its loop sees the sentinel, and every caller removes the
        sentinel before it asks, so nothing here can tell; such a caller's
        newer tap restarts the service onto it, which ends that case.)"""
        session = self._valid(params)
        current = self.recordings.get(session["sid"])
        if current is not None and current.thread is not None and current.thread.is_alive() \
                and not current.controls.stop.is_set():
            with self._gate_lock:
                # Its off stretches belong to the session, not to one request.
                self._carry_gaps(current, session)
                current.params = session
            self._save()
            if not current.in_record and current.last.startswith(str(getattr(self.hosted, "STOPPED", "stopped"))):
                current.wake.set()  # it stepped back for another recorder: look again now
            current.claim_now = True  # held: a `tap watch` offering it may let go of its claim now
            self.look(session["sid"])
            return self._answer(current, started=False)
        if current is not None and current.thread is not None and current.thread.is_alive():
            # Finishing (its SessionEnd came first, then this resume): the new
            # thread takes the session over once that one lets go of it (D39).
            pass
        rec = self._start(session)
        self._save()
        return self._answer(rec, started=True)

    def _answer(self, rec: Recording, *, started: bool) -> dict:
        """`session.record`'s answer. For a session that is off, `off: true`
        too: it is taken (so no `tap watch` records it instead) and held. The
        pid is this service's while it runs, as for any session; once it
        stops holding the session, `close` writes the session's own agent into
        its `.hosted` marker instead (`capture_gate.write_marker`)."""
        answer = {"recording": True, "started": started, "pid": os.getpid()}
        if self._is_off(rec):
            answer["off"] = True
        return answer

    def recording(self, sid: object) -> bool:
        current = self.recordings.get(sid) if isinstance(sid, str) else None
        return bool(current and current.thread and current.thread.is_alive())

    def follow_installed(self) -> tuple[str, str] | None:
        """After an update: the newest tap the recorded sessions' agents have
        installed (`installed_tap`), when it is newer than the one loaded and
        not one this service could not load. Wanted (saved, so the next
        service loads it first, as for a session that names a newer tap); the
        caller restarts the service onto it. None when the loaded tap is the
        newest installed, or nothing is recorded here."""
        self.settling = False
        if self.hosted is None:
            return None
        best: tuple[str, str] | None = None
        unsettled: list = []
        for rec in list(self.recordings.values()):
            if rec.thread is None or not rec.thread.is_alive() or rec.controls.stop.is_set() or self._is_off(rec):
                continue  # a session held off records nothing: no reason to restart for it
            found = installed_tap(rec.params, unsettled)
            if found is not None and (best is None or _numbers(found[1]) > _numbers(best[1])):
                best = found
        # A newer folder Codex may still be writing: the caller asks again soon.
        self.settling = any(_numbers(Path(p).name) > _numbers(self.tap_version or "") for p in unsettled)
        if best is None or _numbers(best[1]) <= _numbers(self.tap_version or ""):
            return None
        if self.unloadable is not None and _numbers(best[1]) <= _numbers(self.unloadable):
            return None
        if self.wanted is None or _numbers(best[1]) > _numbers(self.wanted[1]):
            self.wanted = best
            self._save()
        return self.wanted

    def contexts(self) -> list[dict]:
        """The live recorded sessions' environments and harnesses, for the
        update's follow-up (`followup.contexts`, `notes.sync`'s `rules_for`)."""
        return [
            {"env": rec.params.get("env"), "harness": rec.params.get("harness")}
            for rec in list(self.recordings.values())
            if rec.thread is not None and rec.thread.is_alive() and not rec.controls.stop.is_set()
            and not self._is_off(rec)  # Probe off: no follow-up work for it
        ]

    def live(self, sid: object) -> bool:
        """Recorded here and not finishing: its daemon worker is a live session's."""
        current = self.recordings.get(sid) if isinstance(sid, str) else None
        return bool(
            current and current.thread and current.thread.is_alive()
            and not current.controls.stop.is_set() and not current.controls.pause.is_set()
        )

    async def finish(self, params: dict) -> dict:
        sid = params.get("sid")
        wait = params.get("wait", 0)
        wait = float(wait) if isinstance(wait, (int, float)) and not isinstance(wait, bool) else 0.0
        current = self.recordings.get(sid) if isinstance(sid, str) else None
        if current is None or current.thread is None or not current.thread.is_alive():
            return {"recording": False, "finished": False}
        current.controls.stop.set()
        current.gate_wake.set()  # a held recorder waits on this, not on `stop`
        await asyncio.to_thread(current.thread.join, max(0.0, min(wait, 60.0)))
        return {"recording": True, "finished": not current.thread.is_alive()}

    async def finish_harness(self, harness: str, wait: float, harness_of: Callable[[str], str | None]) -> dict:
        """`recorders.finish` (`probe capture off` for one agent): every
        recorder of `harness` finishes as `finish` does (its killswitch, set
        first by the CLI, makes its last pass ship nothing). Its harness is the
        one its `session.record` named, else its registration's. Waits up to
        `wait` for all of them together. `{finished: [sid], unfinished: [sid]}`."""
        targets = []
        for rec in list(self.recordings.values()):
            if rec.thread is None or not rec.thread.is_alive():
                continue
            named = rec.params.get("harness")
            if (named if isinstance(named, str) and named else harness_of(rec.sid)) == harness:
                targets.append(rec)
        for rec in targets:
            rec.controls.stop.set()
            rec.gate_wake.set()
        deadline = time.monotonic() + max(0.0, min(wait, 60.0))
        for rec in targets:
            await asyncio.to_thread(rec.thread.join, max(0.0, deadline - time.monotonic()))
        return {
            "finished": [r.sid for r in targets if not r.thread.is_alive()],
            "unfinished": [r.sid for r in targets if r.thread.is_alive()],
        }

    def alive(self) -> bool:
        """Does a recorder keep the service alive? One held because its session
        is off never does (`capture_gate`): Probe off starts nothing and keeps
        nothing running."""
        return any(
            r.thread is not None and r.thread.is_alive()
            and not (r.held and not r.finishing and (r.deferred or self._is_off(r)))
            for r in list(self.recordings.values())
        )

    def claims(self) -> dict:
        """`{sid: journal folder}` for each session recorded here whose
        recorder holds its live claim now: published by the tap's loop as it
        takes and lets go of the claim (`tap.hosted.Controls.claim`, tap 0.10.6;
        an older tap publishes nothing). Where `session.list` reads receipts."""
        out = {}
        for rec in list(self.recordings.values()):
            folder = getattr(rec.controls, "claimed", None)
            if isinstance(folder, str) and folder and rec.thread is not None and rec.thread.is_alive():
                out[rec.sid] = folder
        return out

    async def close(self) -> None:
        """The service stops: every recorder pauses (resumed by the next one),
        and its daemon worker is asked to hand over to the next one's. A
        session finishing (its SessionEnd came) is not paused: it finishes
        within the same wait, or the next service resumes it (its shutdown
        sentinel still there) and finishes it."""
        self._closing = True
        self._save()
        for rec in self.recordings.values():
            if rec.controls.stop.is_set():
                continue
            if not rec.held:
                self._hand_over(rec)
            rec.controls.pause.set()
            rec.gate_wake.set()
        deadline = time.monotonic() + PAUSE_JOIN_S
        for rec in list(self.recordings.values()):
            if rec.thread is not None:
                await asyncio.to_thread(rec.thread.join, max(0.0, deadline - time.monotonic()))
        still = [r.sid for r in self.recordings.values() if r.thread is not None and r.thread.is_alive()]
        if still:
            self.log(f"recorder: {len(still)} session(s) still pausing at exit; resumed from saved progress")
        for rec in list(self.recordings.values()):
            # A gap a look on the loop opened or closed just before the stop,
            # its file not written yet (`_flush_gap_file`): written now, so it
            # outlives this service even if `recorders.json` does not.
            if self.gated:
                with contextlib.suppress(Exception):
                    await asyncio.to_thread(self._flush_gap_file, rec)
        for rec in list(self.recordings.values()):
            if rec.controls.stop.is_set() or not self._is_off(rec) or self._tapns is None:
                continue
            # No service runs for a session that is off: its own agent stands in
            # its `.hosted` marker (`capture_gate.write_marker`), so a tap's hooks
            # start neither a service nor a `tap watch` for it every prompt.
            owner = rec.params.get("owner") if isinstance(rec.params.get("owner"), dict) else {}
            pid = owner.get("pid")
            if isinstance(pid, int) and not isinstance(pid, bool) and pid > 1:
                capture_gate.write_marker(self._tapns, rec.params, pid)

    def public(self) -> list:
        """`service.status`'s `recorders`. `alive`: the session's thread runs
        (also while it waits to try again); `recording`: its loop holds the
        session's journal claim now, so it is the one recording the session
        (false in a retry wait, or while another recorder -- the session's own
        `tap watch` -- holds it; None from a tap that cannot say, before 0.10.5);
        `tap_version`: the tap this service loaded, which every recorder here
        runs, whatever tap its session named (the update report's "still runs
        an older tap")."""
        return [
            {"sid": r.sid, "alive": bool(r.thread and r.thread.is_alive()),
             "recording": self._holds(r), "started_at": r.started_at,
             "last": r.last, "failures": r.failures, "tap_version": self.tap_version,
             # The agent its `session.record` named (`finish_harness` reads it
             # first), so a reader can match a recorder whose registration went.
             "harness": r.params.get("harness") if isinstance(r.params.get("harness"), str) else None,
             # Probe is off for it: nothing of it is captured (`capture_gate`).
             # `recording` may still say it holds the session's claim (so an
             # older tap's `tap watch` hands it over): readers read `off` first.
             "off": bool(self._is_off(r))}
            for r in list(self.recordings.values())
        ]
