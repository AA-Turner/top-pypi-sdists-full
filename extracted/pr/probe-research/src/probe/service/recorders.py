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
                       in the next service, which loads the newer tap)
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

Stdlib only at import (the start path; plan S1). The tap is imported when the
first session is recorded.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import random
import re
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from . import paths, procid
from .watch import Family

RECORDERS_NAME = "recorders.json"
RECORDERS_VERSION = 1
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
#: How long a stopping service waits for its recorders to pause, all together.
PAUSE_JOIN_S = 5.0
#: A paused session's daemon worker (the service was its parent) is asked to
#: hand over, dated this far ahead: it sees its parent gone within seconds, and
#: without the ask it would end its session (fail the writer requests waiting,
#: release its lease); the next service's worker takes the lock and clears it.
HANDOVER_AHEAD_S = 180.0
#: An attempt that ran this long before it failed resets the wait to the first.
HEALTHY_RUN_S = 600.0
#: Resumed recorders start spread over this long: started at one instant their
#: passes stay in step, and each drains the others' queues too (the tap's
#: shared drain), so in step they post the same batch twice (de-duplicated by
#: the server, but sent twice).
RESUME_SPREAD_S = 20.0
MAX_ENV = 200
_VERSION = re.compile(r"^\d+(\.\d+)*$")
#: A plugin cache's version folder name (the hooks' `[0-9]*.[0-9]*`, stricter).
_SIBLING = re.compile(r"^\d+(\.\d+)+$")
#: The tap's own floor (`tap.start.MIN_PYTHON`).
MIN_PYTHON = (3, 11)


def _first_retry() -> float:
    try:
        return max(0.05, float(os.environ.get(RETRY_ENV, FIRST_RETRY_S)))
    except ValueError:
        return FIRST_RETRY_S


def _numbers(version: str) -> tuple:
    return tuple(int(p) for p in version.split(".")) if _VERSION.match(version or "") else ()


def _has_tap(root: Path) -> bool:
    """Does `root` hold a tap? False for a folder that cannot be read, or a
    saved path no filesystem call accepts (a NUL byte): one session's bad root
    must never stop another's resume."""
    tap_dir = root / "tap"
    try:
        return (tap_dir / "hosted.py").is_file() and (tap_dir / "main.py").is_file()
    except (OSError, ValueError):
        return False


def _replacement(root: str) -> tuple[str, str] | None:
    """`(root, version)` of the tap folder that replaced `root`, when `root` is
    a version folder that no longer carries a tap: Codex installs a plugin at
    `<cache>/<marketplace>/<plugin>/<version>/` and REMOVES the old version
    folder when it installs a new one (tests/test_codex_stale_plugin_root.py).
    The highest-numbered version-shaped sibling that carries a tap. (The Codex
    hooks re-resolve their own `$PLUGIN_ROOT` to the newest-modified sibling;
    with the one version folder Codex keeps, both pick the same.) Only
    version-shaped siblings, so a plugin folder beside other plugins is never
    scanned. None otherwise."""
    path = Path(root)
    if not _SIBLING.match(path.name) or _has_tap(path):
        return None
    try:
        found = [(_numbers(p.name), p) for p in path.parent.iterdir() if _SIBLING.match(p.name) and _has_tap(p)]
    except (OSError, ValueError):
        return None
    if not found:
        return None
    best = max(found)[1]
    return str(best), best.name


@dataclass
class Recording:
    sid: str
    params: dict
    controls: Any
    thread: threading.Thread | None = None
    started_at: float = field(default_factory=time.time)
    last: str = ""
    failures: int = 0
    #: Inside `hosted.record` now (not waiting to try again), since this
    #: (monotonic): a beat older than its start is a previous run's (the
    #: watch's `stalled`, crash-report plan B2).
    in_record: bool = False
    record_since: float = 0.0


class RecorderHost:
    def __init__(
        self,
        *,
        log: Callable[[str], None],
        loop_getter: Callable[[], Any],
        changed: Callable[[], None] = lambda: None,
        workers: Any = None,
        incident: Callable[..., None] = lambda *args, **kwargs: None,
    ) -> None:
        self.log = log
        #: The service's watch (`watch.Watch.note`): a failing recorder, a tap
        #: that will not load (crash-report plan B2).
        self.incident = incident
        self._loop_getter = loop_getter
        self._changed = changed
        #: The service's worker supervisor (`workers.WorkerHost`), or None.
        self.workers = workers
        self.recordings: dict[str, Recording] = {}
        self.tap_root: str | None = None
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

    # -- the tap -----------------------------------------------------------------

    def _load(self, root: str, version: str) -> bool:
        """Import `tap` from `root` (once). False when it cannot be."""
        if self.hosted is not None:
            return True
        if not _has_tap(Path(root)):
            return False
        if sys.version_info < MIN_PYTHON:
            # The tap needs 3.11 (StrEnum); the CLI, and so this service, runs on
            # 3.10 too. `tap watch` then records, on the system python3.
            return False
        if root not in sys.path:
            sys.path.insert(0, root)
        try:
            import importlib

            module = importlib.import_module("tap.hosted")
            importlib.import_module("tap.main")  # the recorder itself: what fails, fails here
            import tap  # noqa: F401

            loaded = getattr(sys.modules.get("tap"), "__version__", "")
        except Exception as exc:  # noqa: BLE001
            self.log(f"cannot load the tap from {root}: {exc!r}")
            # A `tap_load` report, once per tap version (plan B2): its sessions
            # are recorded by their own `tap watch` meanwhile.
            self.incident(Family.TAP_LOAD, "import_failed", None, {"tap_version": version, "error": repr(exc)[:500]},
                          once=f"tap_load:{version}")
            with contextlib.suppress(ValueError):
                sys.path.remove(root)
            # What it imported before failing stays cached otherwise, and the
            # next load (another tap folder) would get this broken one.
            for name in [n for n in sys.modules if n == "tap" or n.startswith("tap.")]:
                sys.modules.pop(name, None)
            return False
        self.hosted, self.tap_root, self.tap_version = module, root, loaded or version
        self.log(f"recorder: tap {self.tap_version} loaded from {root}")
        return True

    # -- requests -----------------------------------------------------------------

    def _valid(self, params: dict) -> dict:
        from .protocol import invalid_params

        sid = params.get("sid")
        if not isinstance(sid, str) or not sid or len(sid) > 128 or "/" in sid:
            raise invalid_params("sid must be a session id")
        for key in ("cwd", "tap_root"):
            value = params.get(key)
            if not isinstance(value, str) or not os.path.isabs(value) or len(value) > 4096:
                raise invalid_params(f"{key} must be an absolute path")
        transcript, folder = params.get("transcript"), params.get("transcript_dir")
        if not (isinstance(transcript, str) and os.path.isabs(transcript)) and not (
            isinstance(folder, str) and os.path.isabs(folder)
        ):
            raise invalid_params("transcript or transcript_dir must be an absolute path")
        env = params.get("env")
        if not isinstance(env, dict) or len(env) > MAX_ENV or not all(
            isinstance(k, str) and isinstance(v, str) and len(v) <= 8192 and "\0" not in v for k, v in env.items()
        ):
            raise invalid_params("env must be an object of at most 200 string variables")
        version = params.get("tap_version")
        if not isinstance(version, str) or not _VERSION.match(version):
            raise invalid_params("tap_version must be a version")
        session = {
            "sid": sid, "cwd": params["cwd"], "transcript": transcript if isinstance(transcript, str) else None,
            "transcript_dir": folder if isinstance(folder, str) else None, "tap_root": params["tap_root"],
            "tap_version": version, "env": dict(env), "owner": params.get("owner"),
        }
        # What `session.register` reads (checked there), kept to register it
        # again after a restart.
        for key in ("harness", "mode", "generation", "state_dir"):
            if key in params:
                session[key] = params[key]
        return session

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
        registered the session)."""
        session = self._valid(params)
        current = self.recordings.get(session["sid"])
        if current is not None and current.thread is not None and current.thread.is_alive() \
                and not current.controls.stop.is_set():
            current.params = session
            self._save()
            return {"recording": True, "started": False, "pid": os.getpid()}
        if current is not None and current.thread is not None and current.thread.is_alive():
            # Finishing (its SessionEnd came first, then this resume): the new
            # thread takes the session over once that one lets go of it (D39).
            pass
        self._start(session)
        self._save()
        return {"recording": True, "started": True, "pid": os.getpid()}

    def recording(self, sid: object) -> bool:
        current = self.recordings.get(sid) if isinstance(sid, str) else None
        return bool(current and current.thread and current.thread.is_alive())

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
        deadline = time.monotonic() + max(0.0, min(wait, 60.0))
        for rec in targets:
            await asyncio.to_thread(rec.thread.join, max(0.0, deadline - time.monotonic()))
        return {
            "finished": [r.sid for r in targets if not r.thread.is_alive()],
            "unfinished": [r.sid for r in targets if r.thread.is_alive()],
        }

    # -- threads -------------------------------------------------------------------

    def _start(self, session: dict, *, delay: float = 0.0) -> None:
        controls = self.hosted.Controls()
        if self.workers is not None:
            # A tap that knows it hands its worker over (`workers.Link`); an
            # older one never reads it and supervises its own.
            with contextlib.suppress(Exception):
                controls.workers = self.workers.link(session["sid"])
        rec = Recording(session["sid"], session, controls)
        rec.thread = threading.Thread(target=self._guard, args=(rec, delay), name=f"recorder-{session['sid'][:12]}",
                                      daemon=True)
        self.recordings[session["sid"]] = rec
        rec.thread.start()
        self.log(f"recorder: session {session['sid']} recorded here")

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
            began = time.monotonic()
            rec.record_since, rec.in_record = began, True
            try:
                outcome, detail = self.hosted.record(rec.params, rec.controls)
            finally:
                rec.in_record = False
            rec.last = f"{outcome}{': ' + detail if detail else ''}"
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

    @staticmethod
    def _backoff(rec: Recording, seconds: float) -> bool:
        """Wait `seconds`, ending early when the session's stop comes (its last
        pass runs then, not after the wait). True when paused instead."""
        until = time.monotonic() + seconds
        while time.monotonic() < until:
            if rec.controls.pause.wait(min(0.2, max(0.0, until - time.monotonic()))):
                return True
            if rec.controls.stop.is_set():
                return False
        return False

    def _ended(self, rec: Recording) -> None:
        if self.recordings.get(rec.sid) is rec and (rec.controls.stop.is_set() or not rec.controls.pause.is_set()):
            del self.recordings[rec.sid]
            self.log(f"recorder: session {rec.sid} done ({rec.last})")
            self._save()
        if rec.controls.stop.is_set() or not rec.controls.pause.is_set():
            # Its tap released the worker on the way out; this covers a loop
            # that never got that far. A newer recording's claim is kept.
            link = getattr(rec.controls, "workers", None)
            if link is not None:
                link.release()
        self._changed()

    def alive(self) -> bool:
        return any(r.thread is not None and r.thread.is_alive() for r in self.recordings.values())

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
            from . import updater

            if not lock.exists() or not updater._flock_held(lock):
                return
            marker = lock.with_suffix(".handover")
            marker.touch()
            ahead = time.time() + HANDOVER_AHEAD_S
            os.utime(marker, (ahead, ahead))
        except Exception:  # noqa: BLE001 -- the worker ends its session as before
            pass

    async def close(self) -> None:
        """The service stops: every recorder pauses (resumed by the next one),
        and its daemon worker is asked to hand over to the next one's. A
        session finishing (its SessionEnd came) is not paused: it finishes
        within the same wait, or the next service resumes it (its shutdown
        sentinel still there) and finishes it."""
        self._save()
        for rec in self.recordings.values():
            if rec.controls.stop.is_set():
                continue
            self._hand_over(rec)
            rec.controls.pause.set()
        deadline = time.monotonic() + PAUSE_JOIN_S
        for rec in list(self.recordings.values()):
            if rec.thread is not None:
                await asyncio.to_thread(rec.thread.join, max(0.0, deadline - time.monotonic()))
        still = [r.sid for r in self.recordings.values() if r.thread is not None and r.thread.is_alive()]
        if still:
            self.log(f"recorder: {len(still)} session(s) still pausing at exit; resumed from saved progress")

    def public(self) -> list:
        """`service.status`'s `recorders`. `alive`: the session's thread runs
        (also while it waits to try again); `recording`: its loop holds the
        session's journal claim now, so it is the one recording the session
        (false in a retry wait, or while another recorder -- the session's own
        `tap watch` -- holds it; None from a tap that cannot say, before 0.10.5)."""
        return [
            {"sid": r.sid, "alive": bool(r.thread and r.thread.is_alive()),
             "recording": self._holds(r), "started_at": r.started_at,
             "last": r.last, "failures": r.failures,
             # The agent its `session.record` named (`finish_harness` reads it
             # first), so a reader can match a recorder whose registration went.
             "harness": r.params.get("harness") if isinstance(r.params.get("harness"), str) else None}
            for r in self.recordings.values()
        ]

    @staticmethod
    def _holds(rec: Recording) -> bool | None:
        """Whether this recorder holds the session's journal claim now: the
        folder its loop published (`Controls.claim`), which a thread alive in
        its retry wait does not. None from a tap that publishes none."""
        if not hasattr(rec.controls, "claimed"):
            return None
        return rec.controls.claimed is not None

    # -- restarts -------------------------------------------------------------------

    def _path(self) -> Path:
        return paths.service_dir() / RECORDERS_NAME

    def _save(self) -> None:
        data: dict = {"v": RECORDERS_VERSION, "sessions": [r.params for r in self.recordings.values()]}
        if self.wanted is not None:
            data["tap"] = {"root": self.wanted[0], "version": self.wanted[1]}
        target = self._path()
        tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
        try:
            with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
                json.dump(data, handle)
            os.replace(tmp, target)
        except OSError:
            pass
        finally:
            with contextlib.suppress(OSError):
                os.unlink(tmp)

    def resume(self, register: Callable[[dict], None]) -> int:
        """At start: record again every session a previous service recorded
        (each from its saved progress). One whose agent exited meanwhile gets
        its last pass and FINALIZE (the tap's own owner check). Returns how many.

        One tap records them all (`_load` imports once), so the tap is chosen
        first and every session then resumes on it: a session's own folder
        decides nothing past that choice, and a folder the plugin's update
        removed moves to the version folder that replaced it (`_replacement`).
        One that cannot resume is said by sid and left out of `recorders.json`:
        its agent's next prompt asks `session.record` again, with the folder its
        hook resolved."""
        try:
            data = json.loads(self._path().read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return 0
        if not isinstance(data, dict) or data.get("v") != RECORDERS_VERSION:
            return 0
        sessions: list[tuple[dict, dict]] = []
        for raw in data.get("sessions") or []:
            if not isinstance(raw, dict):
                continue
            try:
                session = self._valid(raw)
            except Exception as exc:  # noqa: BLE001 -- a record this version cannot read is dropped
                self.log(f"recorder: session {str(raw.get('sid'))[:128]} not resumed: its saved record does not read "
                         f"({getattr(exc, 'message', None) or type(exc).__name__})")
                continue
            if not isinstance(session.get("owner"), dict):
                self.log(f"recorder: session {session['sid']} not resumed: its agent is not known")
                continue
            moved = _replacement(session["tap_root"])
            if moved is not None:
                self.log(f"recorder: session {session['sid']}'s tap folder {session['tap_root']} is gone; "
                         f"resuming from {moved[0]}")
                session = self._moved(session, *moved)
            sessions.append((raw, session))
        wanted = data.get("tap")
        if isinstance(wanted, dict) and isinstance(wanted.get("root"), str) and isinstance(wanted.get("version"), str):
            # The newer tap a session asked for before the restart.
            root, version = _replacement(wanted["root"]) or (wanted["root"], wanted["version"])
            if not self._load(root, version):
                self.unloadable = version
        # Else the newest tap any of them named that loads.
        sessions.sort(key=lambda pair: _numbers(pair[1]["tap_version"]), reverse=True)
        for _raw, session in sessions:
            if self._load(session["tap_root"], session["tap_version"]):
                break
        resumed = 0
        for raw, session in sessions:
            if session["sid"] in self.recordings:
                continue
            if self.hosted is None:
                self.log(f"recorder: session {session['sid']} not resumed: no tap loads "
                         f"(its own: {session['tap_root']})")
                continue
            if _numbers(session["tap_version"]) > _numbers(self.tap_version or ""):
                # Its own tap would not load: recorded on the older one rather
                # than not at all (the journal reads older taps' writes).
                self.log(f"recorder: session {session['sid']} resumed on tap {self.tap_version} "
                         f"(its own {session['tap_version']} did not load)")
            with contextlib.suppress(Exception):
                register(raw)
            self._start(session, delay=random.uniform(0.0, RESUME_SPREAD_S) if resumed else 0.0)
            resumed += 1
        self._save()
        return resumed

    @staticmethod
    def _moved(session: dict, root: str, version: str) -> dict:
        """The session recorded from `root` instead: its saved folder and
        version, and its `PLUGIN_ROOT` where that named the old folder (as the
        hook's own fallback exports it)."""
        env = dict(session["env"])
        if env.get("PLUGIN_ROOT", "").rstrip("/") == session["tap_root"].rstrip("/"):
            env["PLUGIN_ROOT"] = root
        return {**session, "tap_root": root, "tap_version": version, "env": env}
