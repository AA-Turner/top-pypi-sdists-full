"""save what is recorded (recorders.json) and record every session again after the service restarts."""

from __future__ import annotations
import contextlib
import json
import os
import random
import threading
from pathlib import Path
from typing import Callable


from .. import capture_gate
from ....foundation.service_api import paths
from probe.service.sessions.recorders.tap import _numbers, _replacement, installed_tap

RECORDERS_NAME = "recorders.json"
RECORDERS_VERSION = 1
#: Resumed recorders start spread over this long: started at one instant their
#: passes stay in step, and each drains the others' queues too (the tap's
#: shared drain), so in step they post the same batch twice (de-duplicated by
#: the server, but sent twice).
RESUME_SPREAD_S = 20.0


class RestartsMixin:
    """Part of RecorderHost: its methods run with `self` the RecorderHost; compose() folds them into RecorderHost."""

    # -- restarts -------------------------------------------------------------------

    def _path(self) -> Path:
        return paths.service_dir() / RECORDERS_NAME

    def _save(self) -> None:
        data: dict = {"v": RECORDERS_VERSION, "sessions": [dict(r.params) for r in list(self.recordings.values())]}
        if self.wanted is not None:
            data["tap"] = {"root": self.wanted[0], "version": self.wanted[1]}
        target = self._path()
        tmp = target.with_name(f"{target.name}.{os.getpid()}.{threading.get_ident()}.tmp")
        with self._save_lock:
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
        # The newer tap a session asked for before the restart (or an update's
        # follow-up wanted), and the newest one the sessions' agents have
        # installed now: the newest of them that loads, first. One that will
        # not load is not wanted again (`unloadable`).
        # Then the sessions' own: the newest of all of them that loads.
        candidates: list[tuple[str, str, bool]] = []
        wanted = data.get("tap")
        if isinstance(wanted, dict) and isinstance(wanted.get("root"), str) and isinstance(wanted.get("version"), str):
            candidates.append((*(_replacement(wanted["root"]) or (wanted["root"], wanted["version"])), True))
        for _raw, session in sessions:
            found = installed_tap(session)
            if found is not None:
                candidates.append((*found, True))
        sessions.sort(key=lambda pair: _numbers(pair[1]["tap_version"]), reverse=True)
        candidates += [(session["tap_root"], session["tap_version"], False) for _raw, session in sessions]
        # Stable: at one version a wanted or installed folder comes before a named one.
        candidates.sort(key=lambda c: _numbers(c[1]), reverse=True)
        tried: set = set()
        for root, version, wanted_one in candidates:
            if self.hosted is not None:
                break
            if (root, version) in tried:
                continue
            tried.add((root, version))
            if self._load(root, version):
                break
            if wanted_one and (self.unloadable is None or _numbers(version) > _numbers(self.unloadable)):
                self.unloadable = version
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
            # Spread, but never a session that is off (or has a gap to settle):
            # its gap and its claim come at once, and it posts nothing in step.
            held = bool(capture_gate.gaps_of(session)) or self.off(session)
            self._start(session, delay=random.uniform(0.0, RESUME_SPREAD_S) if resumed and not held else 0.0)
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
