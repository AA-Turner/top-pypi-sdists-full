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


from . import capture_gate, paths, procid
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
#: Kimi Code's folder of one tap version (`probe.cli.kimi_config`): `managed/<id>@<version>`.
_KIMI_TAP = re.compile(r"^probe-research-tap@(\d+(\.\d+)+)$")
KIMI_MANAGED = "managed"
KIMI_LIST = "installed.json"
#: The tap's own floor (`tap.start.MIN_PYTHON`).
MIN_PYTHON = (3, 11)
#: A held session's claim (`capture_gate.Claim`) is looked for this soon after
#: a look that found none, doubling to CLAIM_MAX_S, and at once when a `tap
#: watch` offers the session (it lets go of the claim then).
CLAIM_EVERY_S = 1.0
CLAIM_MAX_S = 60.0
#: A session's record says it ended while off and is not finished yet.
DEFERRED_KEY = "capture_deferred"
#: `RecorderHost._hold`'s answers.
RECORD_STEP = "record"
PAUSED_STEP = "paused"
ENDED_STEP = "ended"


def _first_retry() -> float:
    try:
        return max(0.05, float(os.environ.get(RETRY_ENV, FIRST_RETRY_S)))
    except ValueError:
        return FIRST_RETRY_S


def _numbers(version: str) -> tuple:
    return tuple(int(p) for p in version.split(".")) if _VERSION.match(version or "") else ()


def _codex_cache(env: dict) -> Path:
    """Codex's plugin cache for a session's environment (as the hooks'
    `dispatch._codex_cache` reads it)."""
    home = (env.get("CODEX_HOME") or "").strip()
    base = Path(os.path.expanduser(home)) if home else Path(env.get("HOME") or os.path.expanduser("~")) / ".codex"
    return base / "plugins" / "cache"


#: A Codex version folder written within this long (its own, `tap/`'s or
#: `hooks/`'s time) may still be being written by Codex: not taken as the
#: installed tap yet (the tap hooks' rule, `installed-tap.sh` TAP_SETTLE_S).
SETTLE_S = 5.0


def _settled(folder: Path, now: float | None = None) -> bool:
    """Were `folder`, its `tap/` and its `hooks/` (those that exist) last
    written at least SETTLE_S ago? False when one cannot be read."""
    now = time.time() if now is None else now
    try:
        for part in (folder, folder / "tap", folder / "hooks"):
            if part.exists() and now - part.stat().st_mtime < SETTLE_S:
                return False
    except (OSError, ValueError):
        return False
    return True


def installed_tap(session: dict, unsettled: list | None = None) -> tuple[str, str] | None:
    """`(root, version)` of the tap folder the session's coding agent has
    installed NOW, beside the version folder the session named (its plugin
    cache's `<marketplace>/<plugin>/<version>/`); None when there is none to
    tell or it cannot be told.

    Claude Code: the one folder its install ledger keeps under the plugin's
    `<plugin>@<marketplace>` (`followup.read_ledger`), never another copy:
    it follows a rollback too. Codex, which records no install and keeps only
    the version folder it installed: the highest version-shaped sibling that
    carries a tap, inside Codex's own cache, and that Codex has stopped
    writing (`_settled`: it picks by listing, and the newest folder may be one
    Codex is still copying; each one skipped for that goes in `unsettled`).
    Kimi Code: the one tap folder its plugin list (`installed.json`) records,
    beside the `managed/probe-research-tap@<version>` folder the session named
    (`_kimi_installed`). A folder elsewhere (a developer's checkout, pi's own
    copy): None."""
    from . import followup

    try:
        here = Path(session["tap_root"]).resolve()
    except (KeyError, TypeError, ValueError, OSError):
        return None
    if _KIMI_TAP.match(here.name):
        return _kimi_installed(here)
    if not _SIBLING.match(here.name):
        return None
    plugin = here.parent
    env = session.get("env") if isinstance(session.get("env"), dict) else {}
    plugins = followup.read_ledger(env)
    key = f"{plugin.name}@{plugin.parent.name}"
    if plugins is not None and key in plugins:
        listed = followup.installed_paths(plugins.get(key))
        if listed is None or len(listed) != 1:
            return None
        target = listed.pop()
        if target.parent != plugin or not _SIBLING.match(target.name) or not _has_tap(target):
            return None
        return str(target), target.name
    try:
        if plugin.parent.parent != _codex_cache(env).resolve():
            return None
        found = [(_numbers(p.name), p) for p in plugin.iterdir() if _SIBLING.match(p.name) and _has_tap(p)]
    except (OSError, ValueError):
        return None
    fresh = [p for _key, p in found if not _settled(p)]
    if unsettled is not None:
        unsettled.extend(str(p) for p in fresh)
    found = [(key, p) for key, p in found if p not in fresh]
    if not found:
        return None
    best = max(found)[1]
    return str(best), best.name


def _kimi_installed(here: Path) -> tuple[str, str] | None:
    """`(root, version)` of the tap Kimi's plugin list records, when it is a
    whole tap folder beside `here` in Kimi's `managed/`; None otherwise (no
    list, none or several recorded, another folder, a tap still incomplete)."""
    managed = here.parent
    if managed.name != KIMI_MANAGED:
        return None
    try:
        records = json.loads((managed.parent / KIMI_LIST).read_text(encoding="utf-8"))["plugins"]
        roots = {Path(r["root"]).resolve() for r in records
                 if isinstance(r, dict) and r.get("id") == "probe-research-tap" and isinstance(r.get("root"), str)}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None
    if len(roots) != 1:
        return None
    target = roots.pop()
    found = _KIMI_TAP.match(target.name)
    if target.parent != managed or found is None or not _has_tap(target):
        return None
    return str(target), found.group(1)


def _has_tap(root: Path) -> bool:
    """Does `root` hold a tap? False for a folder that cannot be read, or a
    saved path no filesystem call accepts (a NUL byte): one session's bad root
    must never stop another's resume."""
    tap_dir = root / "tap"
    try:
        return (tap_dir / "hosted.py").is_file() and (tap_dir / "main.py").is_file()
    except (OSError, ValueError):
        return False


#: The service's own copies of the taps it loaded (`_pin`), in its machine folder.
TAPS_NAME = "taps"

def _pin(root: str, version: str) -> Path:
    """A copy of the tap package at `root` that only this service writes or
    removes, to import from instead of `root` (plan C7): `<machine folder>/taps/
    <version>-<fingerprint>/tap/`. Raises OSError (the caller loads in place).

    The service imports the tap once and keeps running it for hours or days,
    and the tap reads its own files long after that import: modules it imports
    only when first needed (`from tap import ...` inside functions), data files
    beside them (`harnesses.json`, the companion's rules). A coding agent's
    plugin cache is not the service's to rely on for that long: Codex keeps one
    version folder of a plugin and deletes it when it installs the next
    (audit #14), Claude Code removes old version folders some time after an
    update, Probe prunes Kimi's. Under a tap imported from such a folder, the
    first lazy import after the update failed. A copy is made once per tap
    version and files (a later load of the same files reuses it); old copies are
    removed at a later load, never the one in use (`probe._shared.pins`)."""
    from probe._shared import pins  # noqa: PLC0415 -- only when a tap loads: the start path stays the service's

    store = paths.service_dir() / TAPS_NAME
    target = pins.make(store, version if _VERSION.match(version or "") else None, {"tap": Path(root) / "tap"},
                       default="tap", meta={"from": root})
    pins.prune(store, keep={target})
    return target


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
    #: Set by a `session.record` for this session while its recorder waits
    #: after stepping back (another recorder held the claim): it tries again
    #: at once instead of after STOPPED_RETRIES first waits (a `tap watch`
    #: that has just let go of the session: `hooks/tap_handover.py`).
    wake: threading.Event = field(default_factory=threading.Event)
    #: Its switch reads `off` (or a gap waits to be settled): its tap loop does
    #: not run, the gate holds it (`RecorderHost._hold`).
    held: bool = False
    #: The switch was seen `off` while its loop ran: the loop was told to leave
    #: (`controls.pause`), and the guard holds the session instead of pausing it.
    hold_asked: bool = False
    #: Wakes a held recorder at once (`session.recording` saw the switch move).
    gate_wake: threading.Event = field(default_factory=threading.Event)
    #: A held session that ended is being finished (settled to its end and
    #: finalized): the service stays up for that, as for any recorder's end.
    finishing: bool = False
    #: Its transcript file, once known (a Codex session names only a folder).
    transcript: Path | None = None
    #: A held session that ended could not be finished (the server did not
    #: answer): it is retried, slowly, by this service and every later one, and
    #: keeps no service alive meanwhile.
    deferred: bool = False
    #: A `session.record` came for it (a `tap watch` offering it): a held
    #: recorder looks for the session's claim again at once.
    claim_now: bool = False
    #: Its gap file is behind its record: written off the shared lock and off
    #: the service's loop, by its recorder thread or the monitor
    #: (`RecorderHost._flush_gap_file`).
    gap_file_due: bool = False
    #: It ended while off and was refused for good (no login here, or the
    #: Probe gateway's own 401/403/404/422): no later service retries it; its
    #: gap file stays.
    dropped: bool = False
    #: Its gap file was read and merged into its record (`_gate`). Until then
    #: it is held, its gap file decides for every drain here (it is not `live`),
    #: and its gap file is never rewritten from its record.
    file_merged: bool = False
    #: Its gap file could not be written: said once, and once it can again.
    gap_file_failing: bool = False
    #: Its gap file's signature when this recording last wrote or read it
    #: (`()`: not yet). One that differs was written by another writer since
    #: (from tap 0.10.19 a `tap watch` of the session records its own off
    #: stretches there): merged into the record before it is written again.
    file_sig: Any = ()
    #: The gaps this recording settled (dropped from its record): never taken
    #: back from a gap file another writer wrote before it saw them go.
    settled_gaps: set = field(default_factory=set)


class RecorderHost:
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

    # -- the tap -----------------------------------------------------------------

    def _load(self, root: str, version: str) -> bool:
        """Import `tap` from `root` (once), through the service's own copy of it
        (`_pin`): a plugin cache that deletes the folder later never takes the
        tap's lazy imports and data files with it. False when it cannot be."""
        if self.hosted is not None:
            return True
        if not _has_tap(Path(root)):
            return False
        if sys.version_info < MIN_PYTHON:
            # The tap needs 3.11 (StrEnum); the CLI, and so this service, runs on
            # 3.10 too. `tap watch` then records, on the system python3.
            return False
        source = root
        try:
            root = str(_pin(source, version))
        except (OSError, ValueError) as exc:
            # Loaded in place, as before the copy: a folder that stays works.
            self.log(f"recorder: cannot copy the tap from {source}, loading it in place: {exc!r}")
        if root not in sys.path:
            sys.path.insert(0, root)
        try:
            import importlib

            module = importlib.import_module("tap.hosted")
            importlib.import_module("tap.main")  # the recorder itself: what fails, fails here
            import tap  # noqa: F401

            loaded = getattr(sys.modules.get("tap"), "__version__", "")
        except Exception as exc:  # noqa: BLE001
            self.log(f"cannot load the tap from {source}: {exc!r}")
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
        self.hosted, self.tap_root, self.tap_version = module, source, loaded or version
        #: Where it was imported from: the service's copy (`_pin`), or `source` itself.
        self.tap_copy = root
        self.log(f"recorder: tap {self.tap_version} loaded from {source}" + (f" (its copy {root})" if root != source else ""))
        try:
            self.gated = capture_gate.install(self._tap(), self.log)
        except Exception as exc:  # noqa: BLE001 -- a tap without the gate's modules records as before
            self.gated = False
            self.log(f"capture gate: not with tap {self.tap_version} ({type(exc).__name__}: {str(exc)[:200]})")
        try:
            # A refused key stamped where the status line and doctor read it.
            from . import keylatch

            keylatch.install(self._tap(), self.log)
        except Exception as exc:  # noqa: BLE001 -- never a reason not to record
            self.log(f"key latch: not with tap {self.tap_version} ({type(exc).__name__}: {str(exc)[:200]})")
        return True

    def _tap(self) -> Any:
        """The loaded tap's modules the capture gate works with."""
        if self._tapns is None:
            import importlib
            import types

            names = ("session_journal", "reconcile", "config", "threadenv", "main", "session_identity",
                     "record_client")
            space = types.SimpleNamespace(**{n: importlib.import_module(f"tap.{n}") for n in names})
            try:
                # The tap's own gate, from 0.10.19 (`capture_gate.native`).
                space.capture_gate = importlib.import_module("tap.capture_gate")
            except ImportError:
                space.capture_gate = None
            self._tapns = space
        return self._tapns

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
        gaps = capture_gate.gaps_of(params)
        if gaps:
            # Its off stretches (`capture_gate`), kept across restarts.
            session[capture_gate.GAPS_KEY] = gaps
        if params.get(DEFERRED_KEY) is True:
            # Ended while off, not finished yet: a later service retries it slowly.
            session[DEFERRED_KEY] = True
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

    # -- Probe off (`capture_gate`) ----------------------------------------------------

    def off(self, params: dict) -> bool:
        """Does this session's switch read `off` now (`session.record`, a resume)?"""
        if not self.gated:
            return False
        return capture_gate.is_off(params)

    @staticmethod
    def _sessions_dir(rec: Recording) -> Path:
        """Where the session's switch and gap file are (its registrant's state folder)."""
        env = rec.params.get("env") if isinstance(rec.params.get("env"), dict) else {}
        return capture_gate.sessions_dir_for(env, rec.params.get("state_dir"))

    def _keep_gaps(self, rec: Recording, gaps: list) -> None:
        """The session's gaps in its record (saved with `recorders.json`) and
        for the drains of this process, at once; its gap file next, off this
        lock and off the loop (`_flush_gap_file`). Under `_gate_lock`."""
        rec.params[capture_gate.GAPS_KEY] = gaps
        if gaps:
            capture_gate.unsettled(rec.sid, gaps)
        else:
            capture_gate.settled(rec.sid)
            rec.params.pop(capture_gate.GAPS_KEY, None)
        rec.gap_file_due = True

    def _flush_gap_file(self, rec: Recording) -> None:
        """Write the session's gap file when it is behind its record (or holds
        gaps its record does not: a removal that failed). Under the session's
        gap-file lock (`capture_gate.locked`), which every writer takes: what
        another writer (a `tap watch` of the session, tap 0.10.19) put there
        since this recording last wrote or read it is merged into its record
        first, never written over. Never for a recording a newer one of the
        session replaced. Not on the loop."""
        if self._superseded(rec) or not rec.file_merged:
            return  # never a gap only the file holds, before the record took it in
        sessions = self._sessions_dir(rec)
        merged: list = []
        with self._gap_file_lock:  # one writer at a time, so the last one written is the newest
            try:
                with capture_gate.locked(sessions, rec.sid):
                    written = self._write_gap_file(rec, sessions, merged)
            except OSError:
                written = False  # the lock could not be had now: tried again at the next look
            if merged:
                self.log(f"capture gate: session {rec.sid}'s gap file holds gaps another recorder wrote; "
                         f"its gaps (transcript bytes) are {merged[0]}")
                self._save()
                self._notify()
            if written is None:
                return
            if not written:
                rec.gap_file_due = True
                if not rec.gap_file_failing:
                    rec.gap_file_failing = True
                    self.log(f"capture gate: session {rec.sid}'s gap file could not be written; "
                             "tried again at each look")
            elif rec.gap_file_failing:
                rec.gap_file_failing = False
                self.log(f"capture gate: session {rec.sid}'s gap file is written again")

    def _write_gap_file(self, rec: Recording, sessions: Path, merged: list) -> bool | None:
        """`_flush_gap_file`'s write, under the session's gap-file lock: True
        written, False not (tried again later), None nothing to write. What it
        merged from another writer goes in `merged`."""
        signature = capture_gate.file_signature(sessions, rec.sid)
        if signature != rec.file_sig:
            # Written by another writer since this recording last saw it.
            raw = capture_gate.read_gap_file_raw(sessions, rec.sid)
            if raw is None:
                return False  # cannot be read now: never written over unread
            joined = self._merge_from_file(rec, raw)
            if joined is not None:
                merged.append(joined)
            rec.file_sig = signature
        on_file = capture_gate.read_gap_file(sessions, rec.sid)
        with self._gate_lock:
            if self._superseded(rec):
                return None
            gaps = capture_gate.gaps_of(rec.params)
            due = rec.gap_file_due or on_file != capture_gate.normalized(gaps)
            rec.gap_file_due = False
        if not due:
            return None
        if not capture_gate.write_gap_file(sessions, rec.sid, gaps, rec.transcript):
            return False
        rec.file_sig = capture_gate.file_signature(sessions, rec.sid)
        return True

    def _merge_from_file(self, rec: Recording, on_file: list) -> list | None:
        """Gaps another writer put in the session's gap file join its record:
        all but the ones this recording settled, and an open gap this record
        already closed (the same start: its own, from before it saw it close).
        The record's gaps after, or None when nothing joined."""
        with self._gate_lock:
            if self._superseded(rec):
                return None
            gaps = capture_gate.gaps_of(rec.params)
            closed_at = {g[0] for g in gaps if g[1] is not None}
            extra = [g for g in on_file if (g[0], g[1]) not in rec.settled_gaps
                     and not (g[1] is None and g[0] in closed_at)]
            merged = capture_gate.normalized(gaps + extra)
            if merged == capture_gate.normalized(gaps):
                return None
            self._keep_gaps(rec, merged)
            return merged

    @staticmethod
    def _carry_gaps(previous: Recording, session: dict) -> None:
        """A session's off stretches go on in its new record. Under `_gate_lock`."""
        if capture_gate.GAPS_KEY in previous.params:
            session[capture_gate.GAPS_KEY] = previous.params[capture_gate.GAPS_KEY]

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
