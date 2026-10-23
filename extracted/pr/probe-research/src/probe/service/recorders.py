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
                       its thread waits, and takes over once that one is gone
    the guard          each session's thread restarts after a failure (5 s,
                       doubling to 5 min) while its agent runs: one bad
                       transcript stops one session's recording, never another's
    restarts           `recorders.json` (0600, beside the registry): what to
                       resume when the next service starts -- each session's
                       arguments and the variables a recorder reads (the tap
                       client sends only those, `tap.record_client.TAP_ENV_*`),
                       and the newer tap a session asked for, loaded first
    an owner           only a session whose agent process is known: the
                       recorder keeps no heartbeat of its own, and ends with
                       that process (the tap's own owner check); one without
                       gets `tap watch` as before

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
#: The tap's own floor (`tap.start.MIN_PYTHON`).
MIN_PYTHON = (3, 11)


def _first_retry() -> float:
    try:
        return max(0.05, float(os.environ.get(RETRY_ENV, FIRST_RETRY_S)))
    except ValueError:
        return FIRST_RETRY_S


def _numbers(version: str) -> tuple:
    return tuple(int(p) for p in version.split(".")) if _VERSION.match(version or "") else ()


@dataclass
class Recording:
    sid: str
    params: dict
    controls: Any
    thread: threading.Thread | None = None
    started_at: float = field(default_factory=time.time)
    last: str = ""
    failures: int = 0


class RecorderHost:
    def __init__(
        self,
        *,
        log: Callable[[str], None],
        loop_getter: Callable[[], Any],
        changed: Callable[[], None] = lambda: None,
    ) -> None:
        self.log = log
        self._loop_getter = loop_getter
        self._changed = changed
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
        tap_dir = Path(root) / "tap"
        if not (tap_dir / "hosted.py").is_file() or not (tap_dir / "main.py").is_file():
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
            if not isinstance(value, str) or not value.startswith("/") or len(value) > 4096:
                raise invalid_params(f"{key} must be an absolute path")
        transcript, folder = params.get("transcript"), params.get("transcript_dir")
        if not (isinstance(transcript, str) and transcript.startswith("/")) and not (
            isinstance(folder, str) and folder.startswith("/")
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
        if os.name != "posix":
            return {"recording": False, "reason": "unsupported"}
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
            outcome, detail = self.hosted.record(rec.params, rec.controls)
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
        self._changed()

    def alive(self) -> bool:
        return any(r.thread is not None and r.thread.is_alive() for r in self.recordings.values())

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
        return [
            {"sid": r.sid, "alive": bool(r.thread and r.thread.is_alive()), "started_at": r.started_at,
             "last": r.last, "failures": r.failures}
            for r in self.recordings.values()
        ]

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
        its last pass and FINALIZE (the tap's own owner check). Returns how many."""
        try:
            data = json.loads(self._path().read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return 0
        if not isinstance(data, dict) or data.get("v") != RECORDERS_VERSION:
            return 0
        sessions = [s for s in data.get("sessions") or [] if isinstance(s, dict)]
        wanted = data.get("tap")
        if isinstance(wanted, dict) and isinstance(wanted.get("root"), str) and isinstance(wanted.get("version"), str):
            # The newer tap a session asked for before the restart.
            if not self._load(wanted["root"], wanted["version"]):
                self.unloadable = wanted["version"]
        # Else the newest tap any of them named.
        sessions.sort(key=lambda s: _numbers(str(s.get("tap_version") or "")), reverse=True)
        resumed = 0
        for raw in sessions:
            try:
                session = self._valid(raw)
            except Exception:  # noqa: BLE001 -- a record this version cannot read is dropped
                continue
            if not isinstance(session.get("owner"), dict) or session["sid"] in self.recordings:
                continue
            if not self._load(session["tap_root"], session["tap_version"]):
                continue
            with contextlib.suppress(Exception):
                register(raw)
            self._start(session, delay=random.uniform(0.0, RESUME_SPREAD_S) if resumed else 0.0)
            resumed += 1
        self._save()
        return resumed
