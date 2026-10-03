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

import contextlib
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
)


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


def pid_file(session_id: str, source: str) -> Path:
    return Path("/tmp") / f"{watcher_prefix(source)}-watcher-{session_id}.pid"


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
      * `probe-research-pi/src/core/daemon.ts::isDaemonAlive` -- matches that exact
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


def _halted(source: str) -> bool:
    """Whether the daemon is sitting in the 401 halt latch.

    Read the same way `tap status` reports it (`tap/status.py`): halted while
    a `last_401_at` stamp exists AND the fingerprint of the REJECTED
    credential still matches the current one. A changed token clears the
    latch, so reporting it afterwards would name a condition the next daemon
    start will not hit. An old daemon that stamped no fingerprint at all still
    reads as halted -- same as `tap status`.

    THE TAP IS OPTIONAL HERE. It is a separately pip-installable package
    living in the coding agent's plugin cache, and on most machines it is not
    importable from the probe CLI's environment at all. Every failure in this
    function degrades to "not halted": `probe session status` must keep
    working, and an unaskable question is not evidence of a halt.

    The state db is addressed through `tap_plugin_dir(source)` rather than
    `tap.config.state_db_path()` on purpose: `tap.config` resolves its
    directory from `PROBE_TAP_SOURCE`, which the CLI's own process does not
    set, so it would answer for claude_code while the rest of
    `session_capture_state` answered for `source`. It is also read-only --
    `Storage.__init__` creates directories and a schema, so a missing db is
    checked first rather than conjured by a status read.
    """
    try:
        from tap.outbox import token_fingerprint  # noqa: PLC0415 - optional dependency
        from tap.storage import Storage  # noqa: PLC0415
    except Exception:  # noqa: BLE001 - absent OR broken tap both mean "cannot tell"
        return False

    db = tap_plugin_dir(source) / "state.db"
    if not db.exists():
        return False
    credential = resolved_capture_credential(source)
    if credential is None:
        return False
    token = credential[0]

    try:
        storage = Storage(db)
    except Exception:  # noqa: BLE001 - a locked or corrupt db is not a halt
        return False
    try:
        if not storage.get_meta("last_401_at"):
            return False
        rejected = storage.get_meta("last_401_token_sha256")
        return not rejected or rejected == token_fingerprint(token)
    except Exception:  # noqa: BLE001
        return False
    finally:
        with contextlib.suppress(Exception):
            storage.close()


def session_capture_state(session_id: str, source: str | None = None) -> CaptureState:
    """The one answer every surface renders."""
    source = source or agent_source()
    plugin_dir = tap_plugin_dir(source)

    if not plugin_dir.exists():
        return CaptureState(False, None, "not installed")
    if (plugin_dir / ".disabled").exists():
        return CaptureState(False, None, "killswitch")
    if _halted(source):
        return CaptureState(False, None, "halted")

    try:
        raw = pid_file(session_id, source).read_text(encoding="utf-8").strip()
        pid = int(raw)
    except (OSError, ValueError):
        return CaptureState(False, None, "not started")

    if pid <= 0:
        return CaptureState(False, None, "not started")
    try:
        os.kill(pid, 0)
    except OSError:
        return CaptureState(False, None, "not started")
    if not _looks_like_the_uploader(pid):
        return CaptureState(False, None, "not started")
    return CaptureState(True, pid, "running")


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

    state = session_capture_state(session_id, source)
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
