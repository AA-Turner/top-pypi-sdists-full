"""Is a transcript daemon live for this session, and if not, why.

A NEW MODULE, not an addition to `capture.py`. That file is about turning
capture OFF as a verified postcondition; this is about whether it is ON, and
the two have opposite failure directions -- `capture.py` must never claim off
while something is still running, this must never claim on while nothing is.

The reason vocabulary is CLOSED and rendered verbatim by every surface. A
free-text reason would be four different sentences in four renderers.

(`CaptureState` here is unrelated to the harbor ledger's `probe.CaptureState`
StrEnum. Nothing in this module is re-exported at the package top level.)
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from probe.cli.capabilities import agent_source, resolved_capture_credential, tap_plugin_dir

REASONS = (
    "running",
    "not started",
    "not installed",
    "not paired",
    "killswitch",
    "disabled path",
    "no session file",
    "interpreter too old",
    "halted",
    # The Probe service has a live recorder for the session that does not hold
    # it now: its server does not answer, it waits to try again, or another
    # recorder (the session's own `tap watch`) still holds it. Not a fault of
    # the session's start, so never `not started`.
    "not recording",
    # The session's switch reads `off`: Probe off means the session is NOT
    # captured (`probe.service.capture_gate`). Nothing to fix: the switch.
    "Probe is off",
)
#: The reason for a session whose switch reads `off` (rendered verbatim:
#: `not capturing session transcript: Probe is off`).
OFF_REASON = "Probe is off"


@dataclass(frozen=True)
class CaptureState:
    running: bool
    pid: int | None
    reason: str


def watcher_prefix(source: str) -> str:
    """The `/tmp` prefix this agent's watcher files share: the registry row's
    `capture.watcher_prefix`, which `tap.config.watcher_prefix` reads from the
    tap's own copy of the registry."""
    from probe.harness import get_registry

    capture = get_registry().get(source).capture
    if capture is None:
        raise ValueError(f"{source!r} has no capture tap")
    return capture.watcher_prefix


#: Mirrors `tap.config.WATCHER_DIR_ENV`: on Windows, the folder Git Bash maps
#: the hooks' `/tmp` to (`cygpath -w /tmp`), which session-start.sh exports for
#: everything it starts. The temp folder Python finds there need not be it.
WATCHER_DIR_ENV = "PROBE_TAP_WATCHER_DIR"
#: ... and keeps in the tap's state folder (session-start.sh), for what it does
#: not start: this CLI, and the status line's refresh, run without that variable.
WATCHER_DIR_FILE = ".watcher_dir"


def _watcher_dir(source: str | None = None) -> Path:
    """Where the tap's hooks keep a session's watcher files: `/tmp`, or the
    folder WATCHER_DIR_ENV names (every OS, as the tap from 0.10.19). On
    Windows the folder Git Bash's `/tmp` is: the one session-start.sh recorded
    in `source`'s tap state folder (WATCHER_DIR_FILE), else WATCHER_DIR_ENV (a
    process the hook started), else the user's temp folder."""
    if os.name != "nt":
        given = os.environ.get(WATCHER_DIR_ENV, "")
        return Path(given) if given and os.path.isabs(given) else Path("/tmp")
    if os.name == "nt":
        if source:
            try:
                saved = (tap_plugin_dir(source) / WATCHER_DIR_FILE).read_text(encoding="utf-8").strip()
            except (OSError, ValueError):
                saved = ""
            if saved and os.path.isabs(saved):
                return Path(saved)
        given = os.environ.get(WATCHER_DIR_ENV, "")
        if given and os.path.isabs(given):
            return Path(given)
        import tempfile

        return Path(tempfile.gettempdir())
    return Path("/tmp")


def pid_file(session_id: str, source: str) -> Path:
    return _watcher_dir(source) / f"{watcher_prefix(source)}-watcher-{session_id}.pid"


def hosted_file(session_id: str, source: str) -> Path:
    """Mirrors `tap.config.hosted_file`: the Probe service records the session
    itself (plan A2), and this names its pid."""
    return _watcher_dir(source) / f"{watcher_prefix(source)}-watcher-{session_id}.hosted"


def _hosted_pid(session_id: str, source: str) -> int | None:
    """The service's pid when it records `session_id` (`tap.record_client.hosted_pid`)."""
    from probe.service import procid

    path = hosted_file(session_id, source)
    try:
        if hasattr(os, "getuid") and path.lstat().st_uid != os.getuid():
            return None
        pid = int(path.read_text(encoding="utf-8").strip())
        if pid <= 1 or not procid.exists(pid):
            return None
    except (OSError, ValueError):
        return None
    if os.name == "nt":
        # No other process's command line to read: the service named itself
        # in its lock file (`server._name_holder`).
        from probe.service import paths

        try:
            pid_s, _, start = paths.lock_path().read_text(encoding="utf-8").strip().partition(" ")
        except OSError:
            return None
        return pid if pid_s == str(pid) and start and procid.alive(pid, start) is True else None
    try:
        completed = subprocess.run(  # noqa: S603 - fixed binary, no shell
            ["/bin/ps", "-ww", "-p", str(pid), "-o", "command="],
            capture_output=True, text=True, timeout=5, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return pid if "probe.service" in completed.stdout else None


def heal_marker(session_id: str, source: str) -> Path:
    """Mirrors `tap.config.heal_marker`; shared with `hooks/ensure-daemon.sh`."""
    return tap_plugin_dir(source) / "heal" / session_id


def _looks_like_the_uploader(pid: int) -> bool:
    """Ask the OS what the process IS before believing a `/tmp` filename.

    A LOCAL COPY, deliberately not `probe.cli.capture._looks_like_the_uploader`,
    and the difference is the whole point. Three places now answer "is a daemon
    alive for this session" and they must give the SAME answer:

      * `tap/start.py::daemon_state` -- the SPAWNER. A live pid whose `/bin/ps
        -ww -p <pid> -o command=` output does not contain the substring `tap` is
        classified `stale`, not `running`, and the spawner then starts one.
      * `probe-research-pi/src/core/daemon.ts::isWatcherAlive` -- matches that exact
        substring form, and says in its own comment why matching matters more
        than being strict.
      * this function.

    `capture.py`'s version is STRICTER: the plugin name, or `tap` as a whole
    WORD. That strictness is right there -- it decides whether to aim SIGTERM
    at a pid, so a false positive is a signal sent to an unrelated process.
    Here the consequence is inverted. A false NEGATIVE would have a surface
    print "tracked, not capturing session transcript" while a daemon is
    genuinely running, which is exactly the class of lie this feature exists
    to remove; a false
    positive costs nothing worse than the spawner's own next check.

    So this mirrors the SPAWNER's loose substring form, verbatim. Any change to
    `tap/start.py::_looks_like_the_uploader` is a change to this function.

    `-ww` is load-bearing in all four copies. Without it `ps` cuts the line to
    `$COLUMNS` when that is set, and the wrapper's script text runs ~550
    characters before the first `tap`, so any caller whose environment sets
    `COLUMNS` (pytest did) read a live daemon as `not started` (2026-09-28).
    """
    try:
        completed = subprocess.run(  # noqa: S603 - fixed binary, no shell
            ["/bin/ps", "-ww", "-p", str(pid), "-o", "command="],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return "tap" in completed.stdout


#: How long a status read waits on the tap's state db: a daemon mid-write
#: holds it for milliseconds, and a status read never waits longer than this.
_STATE_DB_TIMEOUT_S = 0.05


def _state_meta(db: Path, *keys: str) -> dict[str, str] | None:
    """`keys` out of the tap's state db `meta` table, read-only, or None when
    it cannot be read (missing, locked past a moment, corrupt, an older
    schema). Stdlib sqlite3 on a `mode=ro` URI: a status read never creates
    the file, its folder or its schema, as the tap's own `Storage` would."""
    import sqlite3  # noqa: PLC0415 - only a machine with a tap state db pays for it

    try:
        conn = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True, timeout=_STATE_DB_TIMEOUT_S)
    except (sqlite3.Error, OSError, ValueError):
        return None
    try:
        marks = ",".join("?" for _ in keys)
        rows = conn.execute(f"SELECT k, v FROM meta WHERE k IN ({marks})", keys).fetchall()  # noqa: S608
    except sqlite3.Error:
        return None
    finally:
        conn.close()
    return {str(k): str(v) for k, v in rows if v is not None}


def _token_fingerprint(token: str) -> str:
    """`tap.outbox.token_fingerprint`, which the tap stamps beside its 401
    latch: sha256 of the token, hex. A copy, because the tap is not importable
    here (see `_halted`)."""
    import hashlib  # noqa: PLC0415

    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _halted(source: str) -> bool:
    """Whether the daemon is sitting in the 401 halt latch.

    Read the same way `tap status` reports it (`tap/status.py`): halted while
    a `last_401_at` stamp exists AND the fingerprint of the REJECTED
    credential still matches the current one. A changed token clears the
    latch, so reporting it afterwards would name a condition the next daemon
    start will not hit. An old daemon that stamped no fingerprint at all still
    reads as halted -- same as `tap status`.

    THE TAP IS NOT IMPORTED. It is a separately pip-installable package living
    in the coding agent's plugin cache, and on most machines it is not
    importable from the probe CLI's environment at all: importing it made
    `probe session status` and `probe doctor` never say halted there. Its
    state db is read directly instead (`_state_meta`), and its fingerprint
    computed here (`_token_fingerprint`). Every failure degrades to "not
    halted": `probe session status` must keep working, and an unaskable
    question is not evidence of a halt.

    The state db is addressed through `tap_plugin_dir(source)` rather than
    `tap.config.state_db_path()` on purpose: `tap.config` resolves its
    directory from `PROBE_TAP_SOURCE`, which the CLI's own process does not
    set, so it would answer for claude_code while the rest of
    `session_capture_state` answered for `source`.
    """
    db = tap_plugin_dir(source) / "state.db"
    if not db.is_file():
        return False
    meta = _state_meta(db, "last_401_at", "last_401_token_sha256")
    if not meta or not meta.get("last_401_at"):
        return False
    credential = resolved_capture_credential(source)
    if credential is None:
        return False
    rejected = meta.get("last_401_token_sha256")
    return not rejected or rejected == _token_fingerprint(credential[0])


def _watcher_pid(session_id: str, source: str) -> int | None:
    """The pid in the session's pid file when it is a live uploader, else None
    (no file, not a number, a dead pid, a live pid that is not the tap)."""
    try:
        pid = int(pid_file(session_id, source).read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None
    if pid <= 0:
        return None
    try:
        from probe._shared import oscompat  # os.kill(pid, 0) answers nothing on Windows

        oscompat.probe_pid(pid)
    except (OSError, OverflowError):
        return None
    return pid if _looks_like_the_uploader(pid) else None


def _recorder_reading(session_id: str) -> str | None:
    """What the Probe service's recorder of `session_id` does now, in REASONS
    words: `running` (it holds the session), `not recording` (a live recorder
    that does not: its server does not answer, it waits to try again, or the
    session's own `tap watch` still holds it), `not started` (the service
    answered and records no such session, or its recorder ended).

    A `.hosted` marker naming a live service says the service took the
    session, not that its recorder records: the tap's loop returns at once for
    a `.disabled_paths` folder or no token, or fails every pass, and the thread
    lives on. `service.status` says which (`recorders[].recording`, the
    session's journal claim). None when it cannot say -- no service answer in
    time, one from before its recorders, a tap before 0.10.5 that publishes no
    claim -- and the caller reads the marker as before: a status read is
    bounded and fails open, and an unaskable question is not evidence."""
    from probe.cli import service_calls  # noqa: PLC0415 - only a hosted session asks

    rows = service_calls.recorders()
    if rows is None:
        return None
    for row in rows:
        if row.get("sid") != session_id:
            continue
        if row.get("alive") is False:
            return "not started"
        if row.get("off") is True:
            return OFF_REASON  # held: Probe is off for it, nothing of it is captured
        claim = row.get("recording")
        if claim is None:
            return None
        return "running" if claim else "not recording"
    return "not started"


def session_capture_state(session_id: str, source: str | None = None, *, ask_service: bool = True) -> CaptureState:
    """The one answer every surface renders.

    A live uploader in the session's pid file answers first. A pid file that
    names no live uploader (a wrapper that gave up, was killed, or whose pid
    was reused) is stale, not an answer: the session may have moved to the
    Probe service since, which leaves a `.hosted` marker beside it. That
    marker counts when it names a live service, and then the service is asked
    what its recorder does (`_recorder_reading`), unless `ask_service` is
    False: the self-heal (`ensure_capture`, before every `probe` command in pi)
    asks only whether a recorder exists, never makes a service round trip, and
    never starts a second one beside a recorder waiting for its server."""
    source = source or agent_source()
    plugin_dir = tap_plugin_dir(source)

    if switched_off(session_id):
        # Probe off: the session is not captured. A `tap watch` an older tap
        # started for it records it until it hands it to the Probe service, so
        # a live one still reads `running`: that much is true.
        pid = _watcher_pid(session_id, source) if plugin_dir.exists() else None
        if pid is not None:
            return CaptureState(True, pid, "running")
        return CaptureState(False, None, OFF_REASON)
    if not plugin_dir.exists():
        return CaptureState(False, None, "not installed")
    if (plugin_dir / ".disabled").exists():
        return CaptureState(False, None, "killswitch")
    if _halted(source):
        return CaptureState(False, None, "halted")

    pid = _watcher_pid(session_id, source)
    if pid is not None:
        return CaptureState(True, pid, "running")
    hosted = _hosted_pid(session_id, source)
    if hosted is None:
        return CaptureState(False, None, "not started")
    reading = _recorder_reading(session_id) if ask_service else None
    if reading in (None, "running"):
        return CaptureState(True, hosted, "running")
    return CaptureState(False, None, reading)


def switched_off(session_id: str) -> bool:
    """Does the session's switch read `off` (its own state, else this machine's
    default), as the Probe service reads it before it records a line?"""
    from probe.sdk import session_marker  # noqa: PLC0415

    try:
        state = session_marker.session_state(session_id)
        if state is None:
            state, _source = session_marker.resolve_state_default(None)
    except Exception:  # noqa: BLE001 -- unreadable: never `off` on a guess
        return False
    return state == session_marker.STATE_OFF


# --- the self-heal ---------------------------------------------------------

HEAL_RETRY_SECONDS = 600


@dataclass(frozen=True)
class HealResult:
    started: bool
    reason: str


def _tracking_is_on(session_id: str, cwd: Path) -> bool:
    # `probe.sdk.session_marker`, not `probe.cli` -- the marker moved to the
    # SDK so the hooks (which cannot import `cli/`) can read it too.
    from probe.sdk import session_marker  # noqa: PLC0415 - import cost off the hot path

    signal = session_marker.tracking_signal(session_id)
    if signal is not None:
        return session_marker.is_tracking(signal)
    on, _source = session_marker.resolve_tracking_default(str(cwd))
    return on


def _capture_installed(cwd: Path) -> bool:
    from probe.cli import pi_config  # noqa: PLC0415

    # The session's cwd, so a PROJECT-scope `packages` entry counts as consent
    # exactly as a global one does. A broken explicit PROBE_PI_PACKAGE_ROOT
    # answers False there ("cannot tell, so do not claim yes"), and this
    # refuses to heal rather than spawning off a half-resolved identity.
    return pi_config.package_entry_installed(cwd=cwd)


def _tap_runtime() -> tuple[str, str | None] | None:
    """`(interpreter, tap_root)`, mirroring all THREE of `tapRuntime.ts`'s branches.

    Branch 3 -- a bare interpreter with `tap` already importable -- is the real
    distribution path for a pip-installed `probe-research-tap`, and dropping
    it would refuse to heal on exactly the installs customers have.
    """
    override = os.environ.get("PROBE_PI_TAP_ROOT", "").strip()
    if override and (Path(override) / "tap" / "__init__.py").exists():
        return (sys.executable, override)

    from probe.cli import pi_config  # noqa: PLC0415

    try:
        root = pi_config.local_package_root()
    except Exception:  # noqa: BLE001 - a broken override must not block the heal
        root = None
    if root is not None:
        sibling = root.parent / "probe-research-tap"
        if (sibling / "tap" / "__init__.py").exists():
            return (sys.executable, str(sibling))

    try:
        import tap  # noqa: PLC0415, F401
    except ImportError:
        return None
    return (sys.executable, None)


def _run(argv: list[str], env: dict[str, str]) -> int:
    completed = subprocess.run(  # noqa: S603 - argv is ours, no shell
        argv, capture_output=True, text=True, timeout=30, check=False, env=env
    )
    return completed.returncode


#: `tap start`'s exit codes, translated into the closed REASONS vocabulary.
#: Any change to `tap/start.py`'s EXIT_* constants is a change to this table.
_EXIT_REASONS = {
    2: "not paired",
    3: "killswitch",
    4: "disabled path",
    5: "no session file",
    6: "interpreter too old",
}


def ensure_capture(session_id: str, cwd: Path | str, source: str | None = None) -> HealResult:
    """Start a daemon when tracking says one should exist, on pi only.

    THE ORDER IS THE POLICY. Each gate answers a question whose "no" is a
    reason a surface can render, and the first no wins.

    Deliberately NOT called from `probe session initialize`: that command is
    the pi extension's own bridge, called before the extension's own spawn.
    Healing there would take the spawn from the extension on every healthy
    session and fire the announcement on all of them.
    """
    source = source or agent_source()
    if source != "pi":
        # Claude Code and Codex spawn from the tap plugin's own hooks.
        return HealResult(False, "not applicable")

    cwd = Path(cwd)
    if not _tracking_is_on(session_id, cwd):
        return HealResult(False, "off")
    if not _capture_installed(cwd):
        return HealResult(False, "not installed")

    transcript = os.environ.get("PI_SESSION_FILE", "").strip()
    if not transcript:
        return HealResult(False, "no session file")

    runtime = _tap_runtime()
    if runtime is None:
        return HealResult(False, "not installed")

    # The marker alone (`ask_service=False`): a recorder the service runs is
    # left to it, whether or not it holds the session at this moment.
    state = session_capture_state(session_id, source, ask_service=False)
    # `not installed` joins the stop list for the same reason `killswitch`
    # does: it is a fact about this machine, not a daemon that failed to
    # start. The tap's state directory is absent, so nothing was ever paired
    # here and `tap start` would refuse anyway -- but pressing on would ALSO
    # conjure that directory below, via the heal marker's own mkdir, and the
    # directory's absence is exactly what `session_capture_state` reads to
    # answer `not installed`. Healing here would erase the evidence for the
    # answer. Found by the live matrix, not by a unit test.
    if state.running or state.reason in ("halted", "killswitch", "not installed"):
        return HealResult(False, state.reason)

    marker = heal_marker(session_id, source)
    try:
        if time.time() - marker.stat().st_mtime < HEAL_RETRY_SECONDS:
            return HealResult(False, "not started")
    except OSError:
        pass

    python, tap_root = runtime
    env = {**os.environ, "PROBE_TAP_SOURCE": "pi"}
    if tap_root:
        env["PYTHONPATH"] = os.pathsep.join(
            p for p in (tap_root, os.environ.get("PYTHONPATH")) if p
        )

    # Stamped BEFORE the spawn, not after: a `tap start` that hangs until its
    # 30s timeout must still cost one attempt, or every surface in the next
    # ten minutes pays that timeout again.
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch()
    except OSError:
        pass

    code = _run(
        [
            python,
            "-m",
            "tap",
            "start",
            "--session-id",
            session_id,
            "--cwd",
            str(cwd),
            "--transcript",
            transcript,
        ],
        env,
    )
    if code != 0:
        return HealResult(False, _EXIT_REASONS.get(code, "not started"))

    print("probe: started transcript capture for this session", file=sys.stderr)
    return HealResult(True, "running")
