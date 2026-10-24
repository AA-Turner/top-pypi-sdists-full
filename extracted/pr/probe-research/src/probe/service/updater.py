"""The service's updater: the machine's one automatic updater (plan "Updating everything", X1, R2, R3, D3, D4).

    when     after discovery, if the last check is CHECK_EVERY_S old (or there
             never was one); then every CHECK_EVERY_S while the service runs;
             on `update.check_now` (the CLI and the plugin hook, instead of
             spawning an updater of their own); never while automatic updates
             are off (`autoupdate.json` `enabled`, the wizard's setting)
    cycle    update.started
             1 cli_and_plugins  only on a quiet machine (X1): no run holds a
                                run lock or a `run.hold` (a `probe exec`'s,
                                `runholds.py`), no wizard holds wizard.lock, no
                                action of ours runs. Daemon workers do not wait for
                                their sessions to end (D7): when the manifest
                                names a newer CLI, new worker starts are held
                                (`barrier.hold_workers`), each live session's
                                worker is asked to hand over at its next safe
                                point (its `.handover` marker, then SIGTERM:
                                the worker finishes the model round it is in
                                and exits; its queue stays in its store), and
                                the update goes on once they are gone; their
                                supervisor (this service's own for a session
                                recorded here, `workers.py`, which starts none
                                while starts are held; else the tap's) starts
                                them again, on the new code, once the barrier
                                is down. With the CLI current
                                the child updates the plugins only and the
                                workers run on. A worker whose `tap watch` is
                                gone is finishing an ended session's queue:
                                waited for, never cut short. Then the barrier
                                (`barrier.py`), a settle, the same check again,
                                and `python -m probe.core.run update` (the
                                wizard's Update, which moves the CLI's uv tool
                                env -- CLI, daemon, SDK -- and every coding
                                agent's plugins and pi's package in one run),
                                with the login shell's PATH and proxy, CA and
                                index settings (`loginenv.py`, D11, D14). Not
                                quiet: update.deferred, a skip in
                                `autoupdate.json` (`probe doctor` shows it), and
                                a retry when a session ends or at the next cycle.
                                Deferred continuously for DEFER_LIMIT_S (24 h)
                                by workers that would not stop, a run or an
                                action -- each reason its own 24 h -- the next
                                cycle updates anyway, in place (the child told,
                                PROBE_UPDATE_FORCED, when that is past a run),
                                as the updater before the service always did
                                (D7, D33): a machine that is never quiet still
                                updates within a day.
                                Locks are looked for in the default state
                                folder and in every live session's own, which
                                its registration names (D13).
                                The child runs UPDATE_TIMEOUT_S (30 min) at
                                most: past it, it is stopped (SIGTERM to its
                                group, then SIGKILL) and the step failed. One a
                                service before this one left running past it
                                -- the barrier names it -- is stopped the same
                                way before the quiet check (`overrun_update`).
             2 app              the desktop app's update check, at most once per
                                CHECK_EVERY_S, handed to the OPEN app: an app
                                subscribed to `app.check` is sent one and the
                                step is `delegated` (one app connection, the
                                newest, gets it and owns it: closed before a
                                report, the check is failed); its own signed updater
                                checks (installing on quit, or offering its
                                "Restart to update" banner) and reports
                                `update.app_result`, recorded as this step
                                (`ready`: downloaded, installs at quit; no
                                second check while it waits, and the next
                                launch's version settles it if the app never
                                said).
                                No report within APP_RESULT_TIMEOUT_S reads
                                as failed (due again). A closed app is
                                `skipped: app_closed` with `last_app_check`
                                left alone, so its next launch is due: the
                                service never launches the app. At its launch
                                the app asks itself (`update.check_now`
                                trigger `app` with `app`): the answer's
                                `app: {due, reason}` hands it the check then.
             3 self             the CLI version a fresh process imports; a new
                                one means this service is old code: it finishes
                                the cycle, says `service.stopping{update}` and
                                exits. The next `ensure` (a tap re-registering,
                                the app reconnecting) starts the new code.
             update.done
    hold     a running cycle keeps the service alive, at most HOLD_S (R3)
    imports  everything the cycle needs is imported before step 1 replaces
             the files it would import from (R2)

The SDK in researchers' own project environments is never touched (D4).

Stdlib only at import (the start path; plan S1). `probe._shared` (run locks,
the skip record) and `probe.version_policy` (the setting) are light and
imported when a cycle runs.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import secrets
import signal
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field, replace
from pathlib import Path

from . import appupdate, barrier, children, loginenv, paths
from .protocol import (
    APP_RESULT_TIMEOUT_S,
    AppCheckReason,
    AppReportIgnored,
    AppResult,
    AppStepOutcome,
    BusyHolder,
    CheckOutcome,
    DeferReason,
    Method,
    StepState,
    CHECK_TRIGGERS,
    REPORT_FOR_CHECK,
    CheckTrigger,
    StopReason,
    Topic,
    UpdateStep,
)

CHECK_EVERY_S = 6 * 3600
#: How long a running cycle may keep an otherwise idle service alive (plan R3).
HOLD_S = 10 * 60
#: `update.check_now` within this of a finished cycle answers `recent`: the
#: manifest cache's own TTL, and the bound on a sweep of runs each ending
#: with a check.
CHECK_NOW_COOLDOWN_S = 15 * 60
#: Between raising the barrier and checking again: a `probe` that passed the
#: barrier's stat a moment before it existed has taken its lock by then.
BARRIER_SETTLE_S = 1.0
#: A deferred update is retried this soon after a session ends (its worker lets
#: go of its lock as it exits), within the service's own idle grace ...
SESSION_END_RETRY_S = 2.0
#: ... and again, twice as long after each busy look, up to this: a worker
#: drains its queue for a while after its session ended, holding its lock.
SESSION_END_RETRY_MAX_S = 15 * 60
#: While an update is deferred, the schedule looks again this often (not every
#: minute, which a last check older than CHECK_EVERY_S would otherwise give).
DEFERRED_RETRY_S = 15 * 60
VERSION_TIMEOUT_S = 30.0
STATE_VERSION = 1
#: The update child's stderr; cut back at a cycle's start past this.
MAX_LOG_BYTES = 1024 * 1024
#: How long the running daemon workers get to hand over before an update (D7):
#: each finishes the model round it is in. Past it, the update is deferred.
WORKER_STOP_S = 10 * 60
#: While waiting, a stopping worker's `.handover` marker is touched this often
#: (the worker trusts only one younger than 10 s: `worker.HANDOVER_FRESH_S`).
HANDOVER_TOUCH_S = 2.0
WORKER_POLL_S = 0.25
#: Deferred this long without a break by workers, a run or an action: the next
#: cycle updates anyway (D7, D33).
DEFER_LIMIT_S = 24 * 3600
#: Told to the update child when DEFER_LIMIT_S ran out (its reason): the child
#: then updates past a live run too (`probe.cli.upgrading.FORCED_ENV`), as
#: this cycle decided, instead of deferring again by itself (D33).
FORCED_ENV = "PROBE_UPDATE_FORCED"
#: Told to the update child when the CLI is current and daemon workers run
#: from its env: plugins only (`probe.cli.upgrading.SKIP_CLI_ENV`, D7).
SKIP_CLI_ENV = "PROBE_UPDATE_SKIP_CLI"
#: Told to the update child when it must update the CLI beside the running
#: version or not at all (`probe.cli.updater.REQUIRE_SIDE_BY_SIDE_ENV`): the
#: service did not wait for runs and workers, because nothing they run from is
#: replaced (D6, D33).
SIDE_BY_SIDE_ENV = "PROBE_UPDATE_SIDE_BY_SIDE"
#: The update child's wall time, at most. Past it the child is stopped (SIGTERM
#: to its process group, SIGKILL after UPDATE_STOP_GRACE_S) and the step is
#: failed, so the next cycle can run: a child that never returned used to keep
#: the cycle in progress for good, every `update.check_now` answering
#: `running`, and the next service deferring on its `wizard.lock` (never
#: overridden) for good. What a normal update takes: 11-28 s for each of the 19
#: cycles in one devbox's service.log (2026-10-22/23); 24 s from start to report
#: for the last update of a machine that then ran none for 29 h. The longest
#: step the child bounds itself is the CLI env's install, 300 s
#: (`probe.cli.updater._UPGRADE_TIMEOUT_S`, `bootstrap._INSTALL_TIMEOUT_S`), and
#: this code already reads an update older than 15 min as a crashed one (the
#: barrier's MAX_AGE_S; the hold of R3 is 10 min). Twice that, six times the
#: longest step and sixty times the slowest update seen: a child still running
#: then is stuck outside its own bounds, not slow.
UPDATE_TIMEOUT_S = 30 * 60
#: SIGTERM to SIGKILL. The child's SIGTERM handler (`probe.core.events`) ends
#: the run through its `finally` blocks: its locks let go, its records and its
#: update report written (the send is bounded at 3 s,
#: `probe.cli.update_report.SEND_TIMEOUT_S`), the command it was running killed.
UPDATE_STOP_GRACE_S = 30.0
#: Test-only overrides of the two (API v1, "Lifecycle"). Nothing in production sets them.
WORKER_STOP_ENV = "PROBE_SERVICE_WORKER_STOP_S"
DEFER_LIMIT_ENV = "PROBE_SERVICE_DEFER_LIMIT_S"
#: And of APP_RESULT_TIMEOUT_S (a delegated app check that never reports).
APP_RESULT_TIMEOUT_ENV = "PROBE_SERVICE_APP_RESULT_TIMEOUT_S"
#: And of UPDATE_TIMEOUT_S and UPDATE_STOP_GRACE_S.
UPDATE_TIMEOUT_ENV = "PROBE_SERVICE_UPDATE_TIMEOUT_S"
UPDATE_STOP_GRACE_ENV = "PROBE_SERVICE_UPDATE_STOP_GRACE_S"
UPDATE_LOG_NAME = "update.log"
#: `probe.cli.update_report.TRIGGER_ENV`: what asked, for the server's report.
TRIGGER_ENV = "PROBE_AUTOUPDATE_TRIGGER"
#: `probe.cli.wizard_lock.LOCK_FILENAME`, under the default state dir.
WIZARD_LOCK_NAME = "wizard.lock"
#: `probe.cli.wizard_lock.BUSY_EXIT_CODE`: the update child found a setup running.
WIZARD_BUSY_EXIT = 75

#: The deferrals DEFER_LIMIT_S ends. A setup (`wizard.lock`) is never overridden:
#: the update child takes that lock itself and would only find it held. (An
#: update child a service before this one started, still running past
#: UPDATE_TIMEOUT_S, is stopped first: `overrun_update`. That is the one holder
#: of the lock ever ended, and only once it is proven to be that child.)
LIMITED = frozenset({DeferReason.DAEMON_RECORDING, DeferReason.RUN_IN_FLIGHT, DeferReason.ACTION_RUNNING})

#: Deferrals as `autoupdate` skip reasons (what `probe doctor` and the server read).
_SKIPS = {
    DeferReason.RUN_IN_FLIGHT: "SKIP_RUN_IN_FLIGHT",
    DeferReason.SETUP_RUNNING: "SKIP_SETUP_RUNNING",
    DeferReason.ACTION_RUNNING: "SKIP_SETUP_RUNNING",
    DeferReason.DAEMON_RECORDING: "SKIP_DAEMON_RECORDING",
}


def log(message: str) -> None:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with contextlib.suppress(OSError, ValueError):
        sys.stderr.write(f"[{stamp}] probe-service[{os.getpid()}]: update: {message}\n")
        sys.stderr.flush()


# -- is the machine quiet? (plan X1) -----------------------------------------


def _flock_held(path: Path) -> bool:
    """Is this lock file held by anyone? Absent: no. Unknown: yes (fail closed).

    A shared, non-blocking probe released at once (as `wizard_lock.running`):
    it conflicts only with a holder's exclusive lock, and creates nothing."""
    try:
        handle = open(path, "rb")  # noqa: SIM115 -- closed below
    except FileNotFoundError:
        return False
    except OSError:
        return True
    try:
        if not paths.try_lock(handle.fileno(), shared=True):
            return True
        paths.unlock(handle.fileno())
        return False
    finally:
        handle.close()


def _env_seconds(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    return value if value >= 0 else default


@dataclass(frozen=True)
class Worker:
    """A daemon worker holding its session's lock (`<state>/daemon/<sid>.lock`)."""

    sid: str
    lock: Path
    #: From its `.worker.json` marker (`probe.daemon.mailbox.mark_worker_accepts`),
    #: checked to be that worker's process; None when it cannot be told.
    pid: int | None
    #: Its session is not a live one: the worker is finishing the queue of a
    #: session that ended, and a hand-over would leave that tail unrecorded
    #: (no successor ever starts). It is waited for, never asked to stop.
    draining: bool = False

    @property
    def handover(self) -> Path:
        """`probe.daemon.mailbox.handover_path`: the worker hands over at its
        next model round while this is fresh."""
        return self.lock.with_suffix(".handover")


def _is_worker(pid: int, sid: str) -> bool:
    """Is `pid` a running `probe daemon worker` for `sid` (never a reused pid)?"""
    try:
        argv = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
        words = [a.decode("utf-8", "replace") for a in argv]
    except OSError:
        try:
            import subprocess

            out = subprocess.run(
                ["ps", "-ww", "-o", "args=", "-p", str(pid)], capture_output=True, text=True, timeout=5, check=False
            ).stdout
        except (OSError, subprocess.SubprocessError):
            return False
        words = out.split()
    joined = " ".join(words)
    return "daemon" in words and "worker" in words and sid in joined


def _worker_pid(state: Path, sid: str) -> int | None:
    try:
        data = json.loads((state / "reads" / "requests" / sid / ".worker.json").read_text(encoding="utf-8"))
        pid = int(data.get("pid"))
    except (OSError, ValueError, TypeError, AttributeError):
        return None
    return pid if pid > 1 and _is_worker(pid, sid) else None


def state_dirs(extra: set | frozenset = frozenset()) -> list[Path]:
    """The default state folder, then every other one a live session named (D13)."""
    out = [paths.state_dir()]
    for raw in sorted(extra):
        path = Path(raw)
        if path not in out:
            out.append(path)
    return out


def _args(pid: int) -> list[str] | None:
    """`pid`'s command line, or None when it cannot be read."""
    try:
        return [a.decode("utf-8", "replace") for a in Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")]
    except OSError:
        pass
    try:
        import subprocess

        out = subprocess.run(
            ["ps", "-ww", "-o", "args=", "-p", str(pid)], capture_output=True, text=True, timeout=5, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.split() if out.returncode == 0 and out.stdout.strip() else None


#: Set by the service when it records sessions itself (`recorders.RecorderHost.live`):
#: is this session recorded here now (not finishing)? A worker the service's own
#: recorder started has the service as its parent.
_hosted_live: Callable[[str], bool] | None = None


def set_hosted(live: Callable[[str], bool] | None) -> None:
    global _hosted_live
    _hosted_live = live


def _session_ended(pid: int | None, sid: str | None = None) -> bool:
    """Is this worker finishing the queue of a session that ended? Its
    supervisor (`tap watch`, or this service for a session it records:
    `workers.py`, or the tap's own on the recorder's thread) stops it with
    SIGTERM when the session ends, so a worker whose parent is no
    longer a `tap ... watch` -- or, under this service, whose session is no
    longer recorded here -- is draining. Unknown (the parent cannot be read)
    counts as live, as before this check."""
    if pid is None:
        return False
    from . import procid

    info = procid.proc(pid)
    if info is None:
        return False
    if info.ppid <= 1:
        return True
    if info.ppid == os.getpid():
        live = _hosted_live
        try:
            return not (live is not None and sid is not None and live(sid))
        except Exception:  # noqa: BLE001 -- unknown counts as live
            return False
    parent = _args(info.ppid)
    if parent is None:
        return False
    return not ("watch" in parent and any("tap" in word for word in parent))


def live_workers(dirs: list[Path]) -> list[Worker] | None:
    """Every daemon worker holding its lock under `dirs`, each marked
    `draining` when its session ended; None when a folder cannot be listed
    (unknown: busy)."""
    found: list[Worker] = []
    for state in dirs:
        try:
            locks = sorted((state / "daemon").glob("*.lock"))
        except OSError:
            return None
        for lock in locks:
            if _flock_held(lock):
                pid = _worker_pid(state, lock.stem)
                found.append(Worker(lock.stem, lock, pid, _session_ended(pid, lock.stem)))
    return found


def daemon_worker_running() -> bool:
    """A daemon worker holds `<state>/daemon/<sid>.lock` for its whole life."""
    workers = live_workers([paths.state_dir()])
    return workers is None or bool(workers)


def _numbers(version: str) -> tuple | None:
    parts = version.split("+", 1)[0].split(".")
    if not parts or not all(p.isdigit() for p in parts):
        return None
    return tuple(int(p) for p in parts)


def behind(installed: object, latest: object) -> bool | None:
    """Is `installed` older than `latest`? None when either is unknown."""
    if not isinstance(installed, str) or not isinstance(latest, str):
        return None
    a, b = _numbers(installed), _numbers(latest)
    if a is None or b is None:
        return None
    return a < b


@dataclass
class Busy:
    """What the quiet check found (X1, D7, D13)."""

    action: bool = False
    #: A live daemon-mode session registered without its state folder: its
    #: worker may be where no lock can be looked for (an older registrant).
    unseen_daemon: bool = False
    #: Running workers (stoppable when every one has a pid), or None: unknown.
    workers: list | None = field(default_factory=list)
    run: bool = False
    setup: bool = False

    def blocking(self) -> str | None:
        """Why nothing may update, live sessions' workers aside (they are asked
        to stop). A worker finishing an ended session's queue blocks."""
        if self.action:
            return DeferReason.ACTION_RUNNING
        if self.unseen_daemon or self.workers is None or any(w.draining for w in self.workers):
            return DeferReason.DAEMON_RECORDING
        if self.run:
            return DeferReason.RUN_IN_FLIGHT
        if self.setup:
            return DeferReason.SETUP_RUNNING
        return None

    def stoppable(self) -> bool:
        """Can every running worker be asked to hand over (each has a pid)?"""
        return self.workers is not None and all(w.pid is not None for w in self.workers)

    def reasons(self) -> list[str]:
        """Every reason nothing may update, in order. A live session's worker
        is one only when it cannot be asked to hand over (no pid to tell: a
        worker from before D7); the others are asked to stop."""
        out = []
        if self.action:
            out.append(DeferReason.ACTION_RUNNING)
        if (
            self.unseen_daemon
            or self.workers is None
            or any(w.draining or w.pid is None for w in self.workers)
        ):
            out.append(DeferReason.DAEMON_RECORDING)
        if self.run:
            out.append(DeferReason.RUN_IN_FLIGHT)
        if self.setup:
            out.append(DeferReason.SETUP_RUNNING)
        return out

    def reason(self) -> str | None:
        """The first reason, workers included, as the quiet check reported it before D7."""
        if self.action:
            return DeferReason.ACTION_RUNNING
        if self.unseen_daemon or self.workers is None or self.workers:
            return DeferReason.DAEMON_RECORDING
        return self.blocking()


def look(
    *,
    action_running: bool,
    unseen_daemon: bool = False,
    extra_dirs: set | frozenset = frozenset(),
    run_held: bool = False,
) -> Busy:
    """The quiet check (X1), in the default state folder and every live
    session's own (D13). `run_held`: a `probe exec` holds a run here
    (`run.hold`); the run locks are still looked for, for the runs no hold
    names (the SDK's, a `probe exec` from before the hold, or one that found
    no service)."""
    dirs = state_dirs(extra_dirs)
    busy = Busy(action=action_running, unseen_daemon=unseen_daemon, workers=live_workers(dirs))
    if run_held:
        busy.run = True
    else:
        try:
            from probe._shared import run_lock

            busy.run = any(run_lock.any_live(state / run_lock.RUNS_DIRNAME) for state in dirs)
        except Exception:  # noqa: BLE001 -- unknown reads as a live run, as run_lock itself does
            busy.run = True
    busy.setup = any(_flock_held(state / WIZARD_LOCK_NAME) for state in dirs)
    return busy


def side_by_side() -> bool:
    """Will this update install the CLI beside the running one (D6)? Then a
    run or a daemon worker keeps its version, and nothing waits for them.
    Not the first switch, which moves the folder every running process reads
    its files through (`installs.needs_migration`): that one waits for a quiet
    machine, as an in-place update does. Unknown reads as no: the update waits
    as before."""
    try:
        from probe._shared import installs

        return installs.usable() and not installs.needs_migration()
    except Exception:  # noqa: BLE001
        return False


def _switched() -> bool:
    """Does the tool path name a version env now (a side-by-side switch)?"""
    try:
        from probe._shared import installs

        return installs.active() is not None
    except Exception:  # noqa: BLE001
        return False


def hand_over_workers(dirs: list[Path]) -> int:
    """After a side-by-side switch, ask every live session's running worker to
    hand over at its next safe point; its supervisor starts it again through
    `probe` (the tap's) or runtime.json's interpreter (the service's), which
    is the new version now. A worker finishing an ended
    session's queue finishes it on its own version. Returns how many were
    asked. Never raises."""
    asked = 0
    # This service exits right after: nobody re-touches the marker as the D7
    # wait does (`_stop_workers`), and a worker reaches its next safe point
    # after its model round, which can outlast the marker's 10 s. So the marker
    # is dated ahead, by the stop window: fresh until then (the next worker
    # removes it when it takes the session's lock).
    ahead = time.time() + _env_seconds(WORKER_STOP_ENV, WORKER_STOP_S)
    for worker in live_workers(dirs) or []:
        if worker.draining or worker.pid is None or not _is_worker(worker.pid, worker.sid):
            continue
        with contextlib.suppress(OSError):
            worker.handover.touch()
            os.utime(worker.handover, (ahead, ahead))
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.kill(worker.pid, signal.SIGTERM)
            asked += 1
    return asked


def busy_reason(*, action_running: bool, daemon_session: bool = False) -> str | None:
    """Why the CLI env cannot be updated right now (a DeferReason), or None:
    the quiet check before D7, workers included (`probe doctor`'s view).

    `daemon_session`: a live daemon-mode session whose worker's lock may sit
    out of sight (registered without its state folder)."""
    return look(action_running=action_running, unseen_daemon=daemon_session).reason()


def _guard_record() -> dict | None:
    """What the last switch's guard found (D5), or None."""
    try:
        from . import guard

        return guard.read()
    except Exception:  # noqa: BLE001
        return None


def auto_update_enabled() -> bool:
    """The wizard's setting (`autoupdate.json`), read the way every updater reads it."""
    try:
        from probe import version_policy

        return version_policy.autoupdate_enabled()
    except Exception:  # noqa: BLE001 -- unreadable reads as off, as version_policy itself does
        return False


def preload() -> None:
    """Import, now, every module the rest of a cycle (and the service after
    it) would otherwise import later -- from files `uv tool upgrade` is about
    to replace (plan R2). The service exits after a cycle that changed its
    version, so nothing loads from the new files into the old process."""
    import calendar  # noqa: F401
    import plistlib  # noqa: F401
    if os.name != "nt":
        import fcntl  # noqa: F401
    import subprocess  # noqa: F401

    from . import guard, loginenv  # noqa: F401  -- the switch's guard; the update child's environment
    from probe._shared import installs  # noqa: F401  -- side-by-side installs (D6)

    from probe import version_policy  # noqa: F401
    from probe._shared import autoupdate, oscompat, run_lock  # noqa: F401
    from probe.core import requests  # noqa: F401  -- action.run checks its params with it
    from probe.harness import registry  # noqa: F401  -- a request context's session variables

    from .server import session_env_names

    session_env_names()

    from . import procid  # noqa: F401


def record_skip(reason: str, trigger: str) -> None:
    """The deferral, in the record `probe doctor` prints (under the server's
    report word for `trigger`). Never raises."""
    name = _SKIPS.get(reason)
    if name is None:
        return
    try:
        from probe._shared import autoupdate

        report = REPORT_FOR_CHECK.get(trigger, "cli")
        autoupdate.record_skip(getattr(autoupdate, name), trigger=autoupdate.Trigger(report))
    except Exception:  # noqa: BLE001 -- a diagnostic
        pass


# -- an update child past UPDATE_TIMEOUT_S -----------------------------------------


def span(seconds: float) -> str:
    """`30 min`, `90 s`: a time limit as a person reads it."""
    return f"{seconds / 60:.0f} min" if seconds >= 120 else f"{seconds:g} s"


#: `record_stopped`, off the loop, waited for this long at most.
RECORD_WAIT_S = 10.0


def record_stopped(detail: str, *, version: str, since: float) -> bool:
    """A stopped update child, in the record `probe doctor` prints
    (`last_attempt`): failed, `detail` its reason. What the child recorded
    itself since `since` (its start) is kept, failed with this detail: the
    agents it finished, or its own account of the stop. Read and written under
    one hold of the record's lock, never waited for (`amend_attempt`): a child
    that would not stop may hold it. Whether it was written. Blocking (file
    I/O): off the loop. Never raises."""
    try:
        from probe._shared import autoupdate

        now = int(time.time())

        def failed(prior):
            if prior is not None and prior.at >= int(since):
                return replace(prior, at=now, ok=False, detail=detail)
            return autoupdate.Attempt(at=now, ok=False, detail=detail, from_version=version)

        return autoupdate.amend_attempt(failed, wait=False)
    except Exception:  # noqa: BLE001 -- a diagnostic
        return False


async def record_stopped_off_loop(detail: str, *, version: str, since: float) -> None:
    """`record_stopped` in a thread, waited for RECORD_WAIT_S at most."""
    try:
        written = await asyncio.wait_for(
            asyncio.to_thread(record_stopped, detail, version=version, since=since), RECORD_WAIT_S
        )
    except asyncio.TimeoutError:
        written = False
    if not written:
        log("could not write the stopped update into autoupdate.json (its lock is held)")


@dataclass(frozen=True)
class Overrun:
    """An update child a service before this one started, still running past
    the limit: the process (pid, kernel start time) the barrier names."""

    pid: int
    start: str
    #: When it started (the barrier's `created_at`, written as it started).
    since: float


def _is_update_child(pid: int) -> bool:
    """Is `pid`'s command line `<python> -I -m probe.core.run update`?"""
    words = _args(pid)
    if not words:
        return False
    words = [w for w in words if w]
    return any(
        words[i] == "-m" and words[i + 1 : i + 3] == [children.CORE_MODULE, "update"] and i + 3 == len(words)
        for i in range(len(words) - 2)
    )


def overrun_update(limit_s: float, now: float | None = None) -> Overrun | None:
    """The update child a service before this one started and left running
    (`Updater._apply`: the barrier names the child once it runs, and stays up
    while it does), when it is still running `limit_s` after its start. Only
    that child, proven three ways: the barrier names it, (pid, kernel start
    time) is still that exact process (a reused pid has another start time:
    `procid.alive`), and its command line is `probe.core.run update`. A person's
    `probe wizard`, the app's Update action (an action, which raises no barrier)
    or anything else holding `wizard.lock` is never named here. Unknown (the
    start time cannot be read) is no. Blocking (`ps` off Linux): off the loop."""
    data = barrier.read()
    if data is None:
        return None
    try:
        pid = int(data.get("pid", 0))
        start = str(data.get("start_time") or "")
        since = float(data.get("created_at"))
    except (TypeError, ValueError):
        return None
    now = time.time() if now is None else now
    if pid <= 1 or pid == os.getpid() or not start or not now - since >= limit_s:
        return None  # not past the limit (a clock set back reads as not past)
    from . import procid

    if procid.alive(pid, start) is not True or not _is_update_child(pid):
        return None
    return Overrun(pid, start, since)


#: How `stop_process` (and the stop of this service's own child) ended.
Stopped = children.Stopped


async def stop_process(pid: int, start: str, grace: float) -> str:
    """Stop the process (pid, start) as `children.run_events` stops its own
    child at the limit (`children.stop`): SIGTERM, then SIGKILL past `grace`,
    to the process group it leads (an update child of this version: what is
    left of the group once it is gone too, while the group is provably still
    its own) or else to it alone (one an older service started in that
    service's group, which other processes share). The process is signalled
    only while (pid, start) is still that process, read off the loop each
    time. How it ended (`Stopped`). Never raises; cancelled, it sends nothing
    more."""
    from . import procid

    async def leader() -> bool:
        return await asyncio.to_thread(procid.alive, pid, start) is True

    group = None
    if os.name != "nt":
        with contextlib.suppress(OSError):
            if await leader() and os.getpgid(pid) == pid:
                group = pid

    def send(sig: int) -> None:
        os.kill(pid, sig)  # it alone: a group it leads is signalled by `children.stop`

    return await children.stop(leader=leader, send=send, group=group, grace=grace)


# -- the updater ---------------------------------------------------------------


class Updater:
    def __init__(
        self,
        *,
        version: str,
        emit: Callable[[str, dict], None],
        changed: Callable[[], None],
        stop: Callable[[str], None],
        action_running: Callable[[], bool],
        discovering: Callable[[], bool],
        daemon_session: Callable[[], bool] = lambda: False,
        state_dirs: Callable[[], set] = set,
        run_held: Callable[[], bool] = lambda: False,
        app_connected: Callable[[], int] = lambda: 0,
        app_listeners: Callable[[], int] = lambda: 0,
        app_target: Callable[[], int | None] = lambda: None,
        send_app_check: Callable[[int, dict], bool] = lambda serial, payload: False,
        app_alive: Callable[[int], bool] = lambda serial: False,
    ) -> None:
        self.version = version
        self.emit = emit
        #: How many desktop app connections are open (`service.hello` client
        #: `app`), and how many of them take `app.check` (a newer build).
        self.app_connected = app_connected
        self.app_listeners = app_listeners
        #: The one app connection a hand-off goes to (the newest that takes
        #: `app.check`), by its serial, and the send to it alone.
        self.app_target = app_target
        self.send_app_check = send_app_check
        #: Is that app connection still open?
        self.app_alive = app_alive
        #: Called when what holds the service changes (a cycle starts or ends).
        self.changed = changed
        self.stop = stop
        self.action_running = action_running
        self.discovering = discovering
        #: A live daemon-mode session registered without its state folder.
        self.daemon_session = daemon_session
        #: Every live session's state folder (D13).
        self.session_state_dirs = state_dirs
        #: Does a `probe exec` hold a run here (`run.hold`)?
        self.run_held = run_held
        #: An in-place update child is starting or running: no new run hold is
        #: admitted (`Service._run_hold`); the run's lock and the barrier are
        #: what that `probe exec` has then, as without the service.
        self.applying = False
        #: This cycle updates side by side (D6): set by `_core`.
        self.beside = False
        #: The version a side-by-side cycle switched to: the guard watches it (D5).
        self.guard_pending: str | None = None
        self.worker_stop_s = _env_seconds(WORKER_STOP_ENV, WORKER_STOP_S)
        self.defer_limit_s = _env_seconds(DEFER_LIMIT_ENV, DEFER_LIMIT_S)
        self.app_result_timeout_s = _env_seconds(APP_RESULT_TIMEOUT_ENV, APP_RESULT_TIMEOUT_S)
        self.update_timeout_s = _env_seconds(UPDATE_TIMEOUT_ENV, UPDATE_TIMEOUT_S)
        self.update_stop_grace_s = _env_seconds(UPDATE_STOP_GRACE_ENV, UPDATE_STOP_GRACE_S)
        self.state = self._load()
        self._migrate_app_check()
        self.cycle_id: str | None = None
        self.step: str | None = None
        self.task: asyncio.Task | None = None
        #: True from a cycle's start to the end of its CLI-and-plugins step: the
        #: one mutating slot is the update's (`action.run` answers busy).
        self.slot = False
        self.hold_until = 0.0  # monotonic
        #: A check_now that came while discovering: its trigger.
        self.requested: str | None = None
        #: The trigger of the last deferred cycle, retried when a session ends
        #: (and after discovery, by a service that restarted meanwhile).
        self.pending: str | None = self._pending_on_disk()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._timer: asyncio.TimerHandle | None = None
        self._retry: asyncio.TimerHandle | None = None
        self._hold_end: asyncio.TimerHandle | None = None
        #: Fires when a delegated app check has had APP_RESULT_TIMEOUT_S.
        self._app_timer: asyncio.TimerHandle | None = None
        self._side_tasks: set = set()

    # -- state -----------------------------------------------------------------

    def _load(self) -> dict:
        try:
            data = json.loads(paths.update_state_path().read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = None
        if data is None:
            # The first start in this machine's folder (plan D8): what the
            # service before the machine key recorded, so the schedule goes on
            # instead of starting a cycle at once.
            try:
                data = json.loads((paths.root_dir() / paths.UPDATE_STATE_NAME).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                data = None
        if not isinstance(data, dict) or data.get("v") != STATE_VERSION:
            data = {"v": STATE_VERSION}
        return data

    def _migrate_app_check(self) -> None:
        """A `last_app_check` the service before this one recorded (no `app`
        record beside it) counts only when that check found the app current
        or updated it: it was also written for an app it never checked
        (quarantined, not installed, not capable, a failed launch, no result
        in time), and read as a recent check those would hold the app's next
        launch check off for 6 h. The outcome is the last cycle's `app` step;
        anything else (or unknown) drops it, so the next launch is due."""
        if "app" in self.state or self._number("last_app_check") is None:
            return
        last = self.state.get("last_result")
        steps = last.get("steps") if isinstance(last, dict) else None
        step = steps.get(UpdateStep.APP) if isinstance(steps, dict) else None
        outcome = step.get("outcome") if isinstance(step, dict) else None
        if outcome not in (AppResult.UPDATED, AppResult.CURRENT):
            self.state.pop("last_app_check", None)
            return
        at = self._number("last_app_check")
        self.state["app"] = {
            "state": StepState.DONE,
            "delegated_at": None,
            "cycle_id": None,
            "trigger": None,
            "via": "background_update",  # the older service's hidden launch
            "version": step.get("version_before"),
            "at": at,
            "reported_at": at,
            "result": outcome,
            "version_before": step.get("version_before"),
            "version_after": step.get("version_after"),
            "error": None,
        }

    def _save(self) -> None:
        target = paths.update_state_path()
        tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
        try:
            with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
                json.dump(self.state, handle)
            os.replace(tmp, target)
        except OSError:
            pass
        finally:
            with contextlib.suppress(OSError):
                os.unlink(tmp)

    def _pending_on_disk(self) -> str | None:
        deferred = self.state.get("last_deferred")
        if not isinstance(deferred, dict):
            return None
        at, last = deferred.get("at"), self._number("last_check")
        if not isinstance(at, (int, float)) or (last is not None and at <= last):
            return None
        trigger = deferred.get("trigger")
        return trigger if trigger in CHECK_TRIGGERS else None

    def _number(self, key: str) -> float | None:
        value = self.state.get(key)
        return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None

    @property
    def last_check(self) -> float | None:
        return self._number("last_check")

    def next_check(self) -> float | None:
        if self.in_progress():
            return None
        last = self.last_check
        return time.time() if last is None else last + CHECK_EVERY_S

    def due(self, now: float | None = None) -> bool:
        last = self.last_check
        now = time.time() if now is None else now
        return last is None or now - last >= CHECK_EVERY_S or now < last

    def _look(self) -> Busy:
        return look(
            action_running=self.action_running(),
            unseen_daemon=self.daemon_session(),
            extra_dirs=self.session_state_dirs(),
            run_held=self.run_held(),
        )

    async def _look_off_loop(self) -> Busy:
        """`_look`, with the registry and the run holds read here on the loop
        (they are the loop's to change) and only the file probes and `ps` in a
        thread."""
        action, unseen, dirs = self.action_running(), self.daemon_session(), set(self.session_state_dirs())
        held = self.run_held()
        busy = await asyncio.to_thread(
            look, action_running=action, unseen_daemon=unseen, extra_dirs=dirs, run_held=held
        )
        # A `probe exec` may have taken a hold while the scan ran: read them
        # again, after the last await (`_apply` spawns with no await after it).
        if self.run_held():
            busy.run = True
        return busy

    def _streaks(self) -> dict:
        """`{reason: since}`: how long each reason has deferred without a break."""
        value = self.state.get("deferred_since")
        if not isinstance(value, dict):
            return {}
        return {k: float(v) for k, v in value.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}

    def _deferred_since(self, reason: str | None = None) -> float | None:
        streaks = self._streaks()
        if reason is not None:
            return streaks.get(reason)
        return min(streaks.values()) if streaks else None

    def _forced(self, reasons: list[str]) -> list[str] | None:
        """The reasons to update past, or None to defer: every reason present
        must be a LIMITED one and past its own DEFER_LIMIT_S (D7, D33)."""
        if not reasons:
            return []
        if all(self._past_limit(r) for r in reasons):
            return list(reasons)
        return None

    def _past_limit(self, reason: str | None, now: float | None = None) -> bool:
        """Has THIS reason deferred for DEFER_LIMIT_S without a break (D7, D33)?
        A run that started a minute ago is not overridden by a day of workers."""
        if reason not in LIMITED:
            return False
        since = self._deferred_since(reason)
        now = time.time() if now is None else now
        return since is not None and 0 <= now - since and now - since >= self.defer_limit_s

    def in_progress(self) -> bool:
        return self.task is not None and not self.task.done()

    def busy_holder(self) -> dict | None:
        if self.slot and self.in_progress():
            return {"kind": BusyHolder.UPDATE, "cycle_id": self.cycle_id}
        return None

    def holding(self) -> bool:
        """Does a running cycle keep the service alive (at most HOLD_S, R3)?"""
        return self.in_progress() and time.monotonic() < self.hold_until

    def public(self) -> dict:
        """`service.status`'s `update`, and `update.status`."""
        return {
            "enabled": auto_update_enabled(),
            "last_check": self.last_check,
            "last_result": self.state.get("last_result"),
            "next_check": self.next_check(),
            "in_progress": self.in_progress(),
            "cycle_id": self.cycle_id,
            "step": self.step,
            "deferred": self.state.get("last_deferred") if self.pending else None,
            "deferred_since": self._deferred_since() if self.pending else None,
            "guard": _guard_record(),
            "app": self.app_public(),
        }

    # -- the desktop app's check (the service decides, the app's updater acts) --

    def _app_record(self, now: float | None = None) -> dict | None:
        """The last app check handed to the app (or reported by it), as it
        reads now: a delegation with no report past the timeout is failed."""
        record = self.state.get("app")
        if not isinstance(record, dict):
            return None
        out = dict(record)
        if out.get("state") == StepState.DELEGATED:
            at = out.get("delegated_at")
            now = time.time() if now is None else now
            if not isinstance(at, (int, float)) or not 0 <= now - at < self.app_result_timeout_s:
                out.update(self._timed_out(at))
        return out

    def _timed_out(self, delegated_at: object) -> dict:
        at = delegated_at if isinstance(delegated_at, (int, float)) else time.time()
        return {
            "state": StepState.FAILED,
            "result": AppResult.FAILED,
            "error": f"no result from the app within {int(self.app_result_timeout_s)} s",
            "timed_out": True,
            "at": at + self.app_result_timeout_s,
        }

    def app_decision(self, *, force: bool = False, now: float | None = None) -> dict:
        """`{due, reason}` (AppCheckReason): should the app check for its
        update now? Due when none was handed over within CHECK_EVERY_S, the
        last one failed (or never reported), or the app forces it."""
        now = time.time() if now is None else now
        record = self._app_record(now)
        if record is not None and record.get("state") in (StepState.DELEGATED, StepState.READY):
            # One check at a time, forced or not: this one has not reported
            # yet, or its downloaded update waits for the app to quit.
            return {"due": False, "reason": AppCheckReason.IN_PROGRESS}
        if force:
            return {"due": True, "reason": AppCheckReason.FORCED}
        if not auto_update_enabled():
            return {"due": False, "reason": AppCheckReason.AUTO_UPDATE_OFF}
        last = self._number("last_app_check")
        if last is None:
            return {"due": True, "reason": AppCheckReason.NEVER_CHECKED}
        if record is not None and record.get("state") == StepState.FAILED:
            return {"due": True, "reason": AppCheckReason.LAST_FAILED}
        if not 0 <= now - last < CHECK_EVERY_S:
            return {"due": True, "reason": AppCheckReason.INTERVAL_PASSED}
        return {"due": False, "reason": AppCheckReason.CHECKED_RECENTLY}

    def app_public(self) -> dict:
        """`update.status`'s `app`: the decision as it stands, when a check was
        last handed over, how many open apps take `app.check`, and the last
        check's record (`last`: a delegation, or the app's report)."""
        now = time.time()
        return {
            **self.app_decision(now=now),
            "last_check": self._number("last_app_check"),
            "listening": self.app_listeners(),
            "last": self._app_record(now),
        }

    def _delegate(
        self, *, cycle_id: str | None, trigger: str, via: str, version: str | None = None, owner: int | None = None
    ) -> dict:
        """Hand the app its check: recorded (`last_app_check` too) before the
        app is told, so a check is never handed over unrecorded. `owner`: the
        app connection `app.check` goes to (None: the app's launch check,
        asked on a connection of its own; only the timeout bounds it)."""
        now = time.time()
        record = {
            "state": StepState.DELEGATED,
            "delegated_at": now,
            "cycle_id": cycle_id,
            "trigger": trigger,
            "via": via,
            "version": version,
            "owner": owner,
            #: Connections are numbered per service process: the owner is this one's.
            "owner_pid": os.getpid() if owner is not None else None,
        }
        self.state["app"] = record
        self.state["last_app_check"] = now
        self._save()
        self._arm_app_timeout(now)
        log(f"app check handed to the app ({via}, cycle {cycle_id})")
        return record

    def _arm_app_timeout(self, delegated_at: float) -> None:
        if self._loop is None:
            return
        if self._app_timer is not None:
            self._app_timer.cancel()
        delay = max(0.0, delegated_at + self.app_result_timeout_s - time.time())
        self._app_timer = self._loop.call_later(delay, self._app_timed_out, delegated_at)

    def app_gone(self, serial: int) -> None:
        """An app connection closed: the check it owned and never reported is
        failed (due again at the next ask; a late report still counts)."""
        record = self.state.get("app")
        if not isinstance(record, dict) or record.get("state") != StepState.DELEGATED:
            return  # a `ready` check stays ready: the app quit to install it
        if record.get("owner") is None or record.get("owner") != serial or record.get("owner_pid") != os.getpid():
            return
        log("the app connection that had the update check closed before it reported")
        self._settle_app({**record, **self._owner_gone()})

    def _owner_left_with_the_old_service(self) -> None:
        """At start: a check sent to a connection of the service before this
        one, still unreported, lost that connection with it."""
        record = self.state.get("app")
        if (
            isinstance(record, dict)
            and record.get("state") == StepState.DELEGATED
            and record.get("owner") is not None
            and record.get("owner_pid") != os.getpid()
        ):
            self._settle_app({**record, **self._owner_gone()})

    def _owner_alive(self, record: dict) -> bool:
        owner = record.get("owner")
        return owner is not None and record.get("owner_pid") == os.getpid() and self.app_alive(owner)

    def _settle_ready_at_launch(self, version: str | None) -> None:
        """The app's launch check, with a downloaded update waiting (`ready`)
        and the app that downloaded it gone (it quit to install it): running
        the downloaded version, it was updated; anything else, the install did
        not happen, and the check is failed (due again). While that app is
        still open, nothing changes: it installs when it quits."""
        record = self.state.get("app")
        if not isinstance(record, dict) or record.get("state") != StepState.READY or self._owner_alive(record):
            return
        now = time.time()
        ready = record.get("version_after")
        settled = {**record, "at": now, "reported_at": now, "settled_at_launch": True}
        if version is not None and version == ready:
            settled.update(state=StepState.DONE, result=AppResult.UPDATED, version_after=version, error=None)
            log(f"the app runs the downloaded {version}: updated")
        else:
            settled.update(
                state=StepState.FAILED,
                result=AppResult.FAILED,
                error=f"the app started at {version}, not the downloaded {ready}",
            )
            log(f"the app started at {version}, not the downloaded {ready}: due again")
        self._settle_app(settled)

    @staticmethod
    def _owner_gone() -> dict:
        return {
            "state": StepState.FAILED,
            "result": AppResult.FAILED,
            "error": "the app connection it was sent to closed before it reported",
            "owner_gone": True,
            "at": time.time(),
        }

    def _app_timed_out(self, delegated_at: float) -> None:
        """No report for this delegation: recorded as failed (due again)."""
        self._app_timer = None
        record = self.state.get("app")
        if not isinstance(record, dict) or record.get("state") != StepState.DELEGATED:
            return
        if record.get("delegated_at") != delegated_at:
            return
        record = {**record, **self._timed_out(delegated_at)}
        log(f"the app did not report its update check within {int(self.app_result_timeout_s)} s")
        self._settle_app(record)

    @staticmethod
    def _app_step(record: dict, outcome: str = AppStepOutcome.ALREADY_DELEGATED) -> dict:
        """A cycle's `app` step from the record: `{state, outcome, ...}`."""
        state = record.get("state")
        out: dict = {"state": state, "delegated_at": record.get("delegated_at")}
        if state == StepState.DELEGATED:
            out["outcome"] = outcome
            return out
        out["outcome"] = record.get("result")
        for key in ("version_before", "version_after", "error", "timed_out", "owner_gone"):
            if record.get(key) is not None:
                out[key] = record[key]
        return out

    def _settle_app(self, record: dict) -> None:
        """The app check's result (reported, or timed out): into the state
        file, the last cycle's `app` step when that was this delegation, and
        an `update.step` like every other step's. The check is over: its
        timeout no longer runs."""
        if self._app_timer is not None:
            self._app_timer.cancel()
            self._app_timer = None
        self.state["app"] = record
        last = self.state.get("last_result")
        steps = last.get("steps") if isinstance(last, dict) else None
        app = steps.get(UpdateStep.APP) if isinstance(steps, dict) else None
        delegated_at = record.get("delegated_at")
        if isinstance(app, dict) and delegated_at is not None and app.get("delegated_at") == delegated_at:
            steps[UpdateStep.APP] = self._app_step(record)
            last["ok"] = "error" not in steps and all(
                isinstance(s, dict) and s.get("state") != StepState.FAILED for s in steps.values()
            )
        self._save()
        step = self._app_step(record)
        self._step(record.get("cycle_id"), UpdateStep.APP, step.pop("state"), **step)

    def app_result(self, report: dict) -> dict:
        """`update.app_result` (`protocol.need_app_result`): what the app's
        own updater did, for the check its `cycle_id` names (none: the check
        in the app's hands now, as an older build reports). It answers that
        check while it has no report of its own: in the app's hands, timed
        out, or lost with its connection (a late report still counts). A
        `cycle_id` of an earlier check, or a second report of one, changes
        nothing (`recorded: false`, AppReportIgnored). `ready` (downloaded,
        installs at quit) stops the check's timeout and keeps it open for one
        final `updated` or `failed`. A report with no check at all (none was
        ever handed over here) is recorded as one made now."""
        now = time.time()
        record = self.state.get("app")
        record = record if isinstance(record, dict) else None
        cycle_id = report.get("cycle_id")
        ignored = None
        if record is not None and cycle_id is not None and cycle_id != record.get("cycle_id"):
            ignored = AppReportIgnored.STALE
        elif record is not None and record.get("reported_at") is not None:
            ignored = AppReportIgnored.DUPLICATE
        elif (
            record is not None
            and record.get("state") == StepState.READY
            and report["result"] not in (AppResult.UPDATED, AppResult.FAILED)
        ):
            ignored = AppReportIgnored.DUPLICATE  # after `ready`: one final updated or failed
        if ignored is not None:
            log(f"the app reported {report['result']}, not recorded ({ignored})")
            return {"recorded": False, "reason": ignored, "app": self.app_public()}
        if record is not None and (record.get("delegated_at") is not None or record.get("state") == StepState.READY):
            record = {k: v for k, v in record.items() if k not in ("timed_out", "owner_gone")}
        else:
            record = {
                "delegated_at": None,
                "cycle_id": cycle_id,
                "trigger": None,
                "via": None,
                "version": report.get("version_before"),
                "owner": None,
            }
            self.state["last_app_check"] = now
        result = report["result"]
        versions = {
            key: report[key] if report.get(key) is not None else record.get(key)
            for key in ("version_before", "version_after")
        }
        if result == AppResult.READY:
            # Downloaded and verified: no timeout now, and the check stays open
            # for one final report (no `reported_at` yet).
            record.update(state=StepState.READY, at=now, ready_at=now, result=result, error=None, **versions)
        else:
            failed = result == AppResult.FAILED
            record.update(
                state=StepState.FAILED if failed else StepState.DONE,
                at=now,
                reported_at=now,
                result=result,
                error=report.get("error"),
                **versions,
            )
        log(f"the app reported its update check: {result}")
        self._settle_app(record)
        return {"recorded": True, "app": self.app_public()}

    def _launch_check(self, app: dict, answer: dict) -> dict:
        """`update.check_now`'s `app` answer (the app's launch check):
        `{due, reason, cycle_id}`. Due: the check is the app's now, recorded
        as handed over (with the cycle this ask started or joined)."""
        self._settle_ready_at_launch(app.get("version"))
        decision = self.app_decision(force=bool(app.get("force")))
        cycle_id = answer.get("cycle_id") if answer.get("outcome") in (CheckOutcome.STARTED, CheckOutcome.RUNNING) else None
        if not decision["due"]:
            return {**decision, "cycle_id": None}
        self._delegate(cycle_id=cycle_id, trigger=CheckTrigger.APP, via=Method.UPDATE_CHECK_NOW, version=app.get("version"))
        return {**decision, "cycle_id": cycle_id}

    # -- scheduling --------------------------------------------------------------

    def attach(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop
        record = self.state.get("app")
        if isinstance(record, dict) and record.get("state") == StepState.DELEGATED:
            at = record.get("delegated_at")
            if record.get("owner") is not None:
                # Sent to a connection of the service before this one: gone with it.
                loop.call_soon(self._owner_left_with_the_old_service)
            elif isinstance(at, (int, float)):
                # The app's launch check, from before this service started: its timeout still runs.
                self._arm_app_timeout(at)
            else:
                self._app_timer = loop.call_soon(self._app_timed_out, at)

    def after_discovery(self) -> None:
        """The service's discovery window is over: start a cycle when one is
        due (or was asked for meanwhile), and arm the schedule."""
        requested, self.requested = self.requested, None
        if os.name == "nt":
            return  # the CLI updates itself on Windows (`check_now`)
        if requested is not None:
            self.check_now(requested)
        elif auto_update_enabled() and (self.due() or self.pending is not None):
            self.start(self.pending or CheckTrigger.SCHEDULE)
        self._arm()

    def _arm(self) -> None:
        if self._loop is None or os.name == "nt":
            return
        if self._timer is not None:
            self._timer.cancel()
        last = self.last_check
        if self.pending is not None:
            delay = DEFERRED_RETRY_S
        else:
            delay = CHECK_EVERY_S if last is None else max(60.0, last + CHECK_EVERY_S - time.time())
        self._timer = self._loop.call_later(delay, self._tick)

    def _tick(self) -> None:
        self._timer = None
        if not self.in_progress() and auto_update_enabled() and (self.due() or self.pending is not None):
            self.start(self.pending or CheckTrigger.SCHEDULE)
        self._arm()

    def check_now(self, trigger: str, app: dict | None = None) -> dict:
        """`update.check_now`: `{outcome, ...}` (CheckOutcome), and, when the
        desktop app asked with `app` (`protocol.need_app_check`), `app: {due,
        reason, cycle_id}` for its own update check. An ask without `app` (an
        older app, the CLI, a hook) gets no `app` and hands nothing over."""
        answer = self._check_cycle(trigger)
        if app is not None:
            answer["app"] = self._launch_check(app, answer)
        return answer

    def _check_cycle(self, trigger: str) -> dict:
        if os.name == "nt":
            # Windows (R3): a running CLI's files can be neither replaced nor
            # moved, so the CLI keeps its own updater there (`_service_owns_updates`).
            return {"outcome": CheckOutcome.DEFERRED, "reason": DeferReason.UNSUPPORTED}
        if self.discovering():
            self.requested = trigger
            return {"outcome": CheckOutcome.SCHEDULED}
        if self.in_progress():
            return {"outcome": CheckOutcome.RUNNING, "cycle_id": self.cycle_id}
        if not auto_update_enabled():
            self.emit(Topic.UPDATE_DEFERRED, {"cycle_id": None, "reason": DeferReason.AUTO_UPDATE_OFF, "trigger": trigger})
            return {"outcome": CheckOutcome.DEFERRED, "reason": DeferReason.AUTO_UPDATE_OFF}
        last = self.last_check
        if last is not None and 0 <= time.time() - last < CHECK_NOW_COOLDOWN_S:
            return {"outcome": CheckOutcome.RECENT, "last_check": last}
        return {"outcome": CheckOutcome.STARTED, "cycle_id": self.start(trigger)}

    def session_ended(self) -> None:
        """A deferred update gets another try once a session is gone."""
        if self.pending is None or self.in_progress() or self._loop is None:
            return
        if self._retry is not None:
            self._retry.cancel()
        self._retry = self._loop.call_later(SESSION_END_RETRY_S, self._retry_pending, SESSION_END_RETRY_S)

    def _retry_pending(self, delay: float = SESSION_END_RETRY_S) -> None:
        self._retry = None
        trigger = self.pending
        if trigger is None or self.in_progress() or not auto_update_enabled():
            return
        busy = self._look()
        if self._forced(busy.reasons()) is not None:
            self.start(trigger)
        elif self._loop is not None and delay < SESSION_END_RETRY_MAX_S:
            # Still busy: most often the ended session's worker, draining its
            # queue under its lock. Look again, less often each time.
            later = min(delay * 2, SESSION_END_RETRY_MAX_S)
            self._retry = self._loop.call_later(later, self._retry_pending, later)

    def start(self, trigger: str) -> str:
        """Start a cycle (the caller checked it may); its cycle id."""
        assert self._loop is not None
        cycle_id = secrets.token_hex(6)
        self.cycle_id = cycle_id
        self.slot = True
        self.hold_until = time.monotonic() + HOLD_S
        if self._hold_end is not None:
            self._hold_end.cancel()
        # When the hold runs out, the service looks again at what holds it.
        self._hold_end = self._loop.call_later(HOLD_S + 0.05, self.changed)
        self.task = self._loop.create_task(self._cycle(cycle_id, trigger))
        self.changed()
        return cycle_id

    def close(self) -> None:
        for handle in (self._timer, self._retry, self._hold_end, self._app_timer):
            if handle is not None:
                handle.cancel()
        if self.task is not None and not self.task.done():
            self.task.cancel()
        for task in list(self._side_tasks):
            task.cancel()

    # -- the cycle ---------------------------------------------------------------

    def _step(self, cycle_id: str, step: str, state: str, **detail: object) -> None:
        self.step = step if state == StepState.STARTED else self.step
        self.emit(Topic.UPDATE_STEP, {"cycle_id": cycle_id, "step": step, "state": state, **detail})

    async def _cycle(self, cycle_id: str, trigger: str) -> None:
        log(f"cycle {cycle_id} started ({trigger})")
        self.emit(Topic.UPDATE_STARTED, {"cycle_id": cycle_id, "trigger": trigger})
        steps: dict = {}
        deferred: str | None = None
        restart = False
        try:
            preload()
            try:
                core = await self._core(cycle_id, trigger)
            finally:
                self.slot = False
            steps[UpdateStep.CLI_AND_PLUGINS] = core
            if core["state"] == StepState.DEFERRED:
                deferred = str(core["reason"])
                self.emit(Topic.UPDATE_DEFERRED, {"cycle_id": cycle_id, "reason": deferred, "trigger": trigger})
            steps[UpdateStep.APP] = await self._app(cycle_id, trigger)
            if core["state"] in (StepState.DONE, StepState.FAILED):
                steps[UpdateStep.SELF], restart = await self._self(cycle_id)
                if restart and (self.beside or await asyncio.to_thread(_switched)):
                    # Watched by the guard (D5), which moves live sessions'
                    # workers once the new version runs: a rejected one keeps
                    # them where they are. The first switch too (it waited for
                    # a quiet machine, so it was not `beside`).
                    to_version = steps[UpdateStep.SELF].get("to_version")
                    if isinstance(to_version, str):
                        self.guard_pending = to_version
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 -- a bug costs this cycle, never the service
            log(f"cycle {cycle_id} failed: {exc!r}")
            steps["error"] = repr(exc)[:500]
        app = steps.get(UpdateStep.APP)
        record = self.state.get("app")
        if (
            isinstance(app, dict)
            and app.get("state") == StepState.DELEGATED
            and isinstance(record, dict)
            and record.get("state") != StepState.DELEGATED
            and record.get("delegated_at") == app.get("delegated_at")
        ):
            # The app reported while the cycle's later steps ran: its result is the step.
            steps[UpdateStep.APP] = self._app_step(record)
        now = time.time()
        ok = deferred is None and all(
            isinstance(s, dict) and s.get("state") != StepState.FAILED for s in steps.values()
        ) and "error" not in steps
        result = {"cycle_id": cycle_id, "at": now, "trigger": trigger, "ok": ok, "steps": steps, "restart": restart}
        if deferred is None:
            self.state["last_check"] = now
            self.state["last_result"] = result
            # Cycles in a row that ended not ok: the watch's `update_failed` (plan B2).
            streak = self.state.get("failed_in_a_row")
            self.state["failed_in_a_row"] = 0 if ok else (streak if isinstance(streak, int) else 0) + 1
            self.state.pop("deferred_since", None)
            self.pending = None
        else:
            self.state["last_deferred"] = {"at": now, "reason": deferred, "trigger": trigger}
            # The streaks DEFER_LIMIT_S is counted from (D7, D33), per reason:
            # every reason this look saw goes on (or starts); one it did not see
            # has ended.
            core_step = steps.get(UpdateStep.CLI_AND_PLUGINS)
            seen = core_step.get("reasons") if isinstance(core_step, dict) else None
            seen = seen if isinstance(seen, list) else [deferred]
            streaks = self._streaks()
            self.state["deferred_since"] = {r: streaks.get(r, now) for r in seen if r in LIMITED}
            self.pending = trigger
            record_skip(deferred, trigger)
        self._save()
        self.cycle_id = None
        self.step = None
        self.emit(Topic.UPDATE_DONE, {**result, "deferred": deferred})
        log(f"cycle {cycle_id} done (ok {ok}, deferred {deferred}, restart {restart})")
        self._arm()
        # `task` is still this one until it returns: clear the hold first.
        self.hold_until = 0.0
        self._loop.call_soon(self.changed)
        if restart:
            # The guard starts when this service really stops (`before_exit`),
            # which waits for a running action: started now, it would watch a
            # service still serving and read it as one that will not go.
            self._loop.call_soon(self.stop, StopReason.UPDATE)

    def before_exit(self, reason: str) -> None:
        """The service is stopping: after a switch (its own restart, or a stop
        for another reason before that came), start the switch's guard now (D5)."""
        if self.guard_pending:  # whatever stops it now, the next one is the new version
            to_version, self.guard_pending = self.guard_pending, None
            self._spawn_guard(to_version)

    def _defer(self, cycle_id: str, reason: str, reasons: list | None = None) -> dict:
        """A deferral, with every reason the look saw (each one's streak goes on)."""
        self._step(cycle_id, UpdateStep.CLI_AND_PLUGINS, StepState.DEFERRED, reason=reason)
        return {"state": StepState.DEFERRED, "reason": reason, "reasons": list(reasons or [reason])}

    async def _stop_workers(self, workers: list) -> list:
        """Ask each running worker to hand over at its next safe point (D7):
        its `.handover` marker, kept fresh, then SIGTERM. Returns the ones
        still holding their lock after `worker_stop_s`."""
        def touch(found: list) -> None:
            for worker in found:
                with contextlib.suppress(OSError):
                    worker.handover.touch()

        touch(workers)
        for worker in workers:
            if worker.pid is not None and _is_worker(worker.pid, worker.sid):
                with contextlib.suppress(ProcessLookupError, PermissionError):
                    os.kill(worker.pid, signal.SIGTERM)
                    log(f"asked daemon worker {worker.pid} ({worker.sid}) to hand over for the update")
        deadline = time.monotonic() + self.worker_stop_s
        touched = time.monotonic()
        while True:
            live = [w for w in workers if _flock_held(w.lock)]
            if not live or time.monotonic() >= deadline:
                break
            if time.monotonic() - touched >= HANDOVER_TOUCH_S:
                touch(live)
                touched = time.monotonic()
            await asyncio.sleep(WORKER_POLL_S)
        for worker in workers:
            # Never leave one behind: a later session end must drain, not hand over.
            with contextlib.suppress(OSError):
                worker.handover.unlink()
        return live

    async def _cli_behind(self, login: dict) -> bool | None:
        """Is the installed CLI older than the newest release (the manifest
        itself, through the login shell's proxy)? None: unknown."""
        try:
            code, value = await children.run_read(
                "version", {"latest": True}, env_extra=login, timeout=VERSION_TIMEOUT_S
            )
        except OSError:
            return None
        if code != 0 or not isinstance(value, dict):
            return None
        return behind(value.get("cli_version"), value.get("cli_latest"))

    async def _stop_previous(self, cycle_id: str) -> dict | None:
        """Before the quiet check: the update child a service before this one
        left running, past `update_timeout_s` (`overrun_update`), is stopped
        as this service stops its own at the limit (its `wizard.lock` would
        otherwise defer every cycle for good: a setup is never overridden).
        What was done, for the step's record, or None (no such child)."""
        found = await asyncio.to_thread(overrun_update, self.update_timeout_s)
        if found is None:
            return None
        past = f"the update a service before this one started ran past {span(self.update_timeout_s)}"
        log(f"{past} (pid {found.pid}, {(time.time() - found.since) / 60:.0f} min old): stopping it")
        self._step(cycle_id, UpdateStep.CLI_AND_PLUGINS, StepState.STARTED, stopping_previous=found.pid)
        how = await stop_process(found.pid, found.start, self.update_stop_grace_s)
        if how == Stopped.GONE:
            log(f"the previous update child {found.pid} exited by itself meanwhile")
            return None
        detail = f"{past} and would not stop" if how == Stopped.RUNNING else f"{past} and was stopped"
        log(f"{detail} ({how})")
        await record_stopped_off_loop(detail, version=self.version, since=found.since)
        return {"detail": detail, "pid": found.pid, "started_at": found.since, "stopped_by": how}

    async def _core(self, cycle_id: str, trigger: str) -> dict:
        """Step 1: the CLI's env and the plugins, on a quiet machine only."""
        previous = await self._stop_previous(cycle_id)
        out = await self._core_step(cycle_id, trigger)
        if previous is not None:
            out["stopped_previous"] = previous
        return out

    async def _core_step(self, cycle_id: str, trigger: str) -> dict:
        step = UpdateStep.CLI_AND_PLUGINS
        busy = await self._look_off_loop()
        # `uv tool dir` is a child process: off the loop.
        self.beside = await asyncio.to_thread(side_by_side)
        if self.beside:
            # Nothing a run or a worker runs from is replaced (D6): they keep
            # their version (one finishing an ended session's queue too), and
            # live sessions' workers move after the switch (`_cycle`).
            busy.run = False
            busy.workers = [] if busy.workers is not None else None
            busy.unseen_daemon = False
        reasons = busy.reasons()
        forced = self._forced(reasons)
        if forced is None:
            first = next(r for r in reasons if not self._past_limit(r))
            return self._defer(cycle_id, first, reasons)
        token = secrets.token_hex(16)
        held = False
        skip_cli = False
        login: dict | None = None
        # Only live sessions' workers are ever asked to stop: one finishing an
        # ended session's queue is waited for (`reasons`), or, past the limit,
        # updated around as before D7.
        # (A worker that cannot be asked, with no pid, is in `reasons`: waited
        # for as before D7, at most DEFER_LIMIT_S.)
        running = [w for w in busy.workers or [] if not w.draining and w.pid is not None]
        daemon = DeferReason.DAEMON_RECORDING
        try:
            if running:
                # The login shell's PATH and settings (D11, D14), for the manifest
                # read and the update child, never stored. Before the barrier: a
                # profile that runs `probe` would wait on it.
                login = await loginenv.child_env(vars=True)
                newer = await self._cli_behind(login)
                if newer is False:
                    # Nothing new for the CLI env the workers run from: leave
                    # them be and update the plugins only (D7).
                    skip_cli = True
                elif newer is None and not self._past_limit(daemon):
                    # Not known whether stopping them would buy anything: wait
                    # (at most DEFER_LIMIT_S), never stop them for nothing.
                    return self._defer(cycle_id, daemon, reasons + [daemon])
                else:
                    try:
                        barrier.hold_workers(token)
                        held = True
                    except OSError as exc:
                        log(f"cannot hold new daemon workers: {exc}")
                        if not self._past_limit(daemon):
                            return self._defer(cycle_id, daemon, reasons + [daemon])
                        forced.append(daemon)
                    if held:
                        self._step(cycle_id, step, StepState.STARTED, stopping_workers=len(running))
                        # A person's action is not refused as busy while the
                        # workers finish their rounds: the slot is the update's
                        # again only once they are gone.
                        self.slot = False
                        left = await self._stop_workers(running)
                        self.slot = True
                        if left:
                            log(f"{len(left)} daemon worker(s) did not hand over within {self.worker_stop_s:.0f} s")
                            if not self._past_limit(daemon):
                                return self._defer(cycle_id, daemon, reasons + [daemon])
                            forced.append(daemon)
                        if self.action_running():
                            # One of a person's actions started meanwhile.
                            action = DeferReason.ACTION_RUNNING
                            return self._defer(cycle_id, action, reasons + [action])
            if login is None:
                login = await loginenv.child_env(vars=True)
            return await self._apply(cycle_id, trigger, token, forced, login, skip_cli, held)
        finally:
            if held:
                barrier.release_workers(token)

    async def _apply(
        self, cycle_id: str, trigger: str, token: str, forced: list, login: dict, skip_cli: bool, held: bool
    ) -> dict:
        """The barrier, the second look, and the update child."""
        step = UpdateStep.CLI_AND_PLUGINS
        try:
            barrier.raise_barrier(token)
        except OSError as exc:
            self._step(cycle_id, step, StepState.FAILED, detail=f"cannot raise the update barrier: {exc}")
            return {"state": StepState.FAILED, "detail": f"cannot raise the update barrier: {exc}"}
        child: list = []

        def started(process) -> None:
            # From here the barrier is the update child's: it stays up while the
            # child runs even if this service stops under it (a signal, the end
            # of its hold), and goes stale once the child is gone.
            child.append(process)
            with contextlib.suppress(OSError):
                barrier.raise_barrier(token, pid=process.pid)

        lower = True
        try:
            await asyncio.sleep(BARRIER_SETTLE_S)
            again = await self._look_off_loop()
            if self.beside:
                again.run, again.unseen_daemon = False, False
                again.workers = [] if again.workers is not None else None
            seen = again.reasons()
            if not (skip_cli or held) and any(not w.draining for w in again.workers or []):
                # A live session's worker started after the first look (none ran
                # then, so none was asked to stop): not under it.
                seen.append(DeferReason.DAEMON_RECORDING)
            for reason in seen:
                if reason not in forced and not self._past_limit(reason):
                    # Something new since the first look (a run just started, a
                    # setup took wizard.lock): never updated under, unless it too
                    # has deferred for DEFER_LIMIT_S.
                    return self._defer(cycle_id, reason, seen)
            forced = sorted(set(forced) | set(seen))
            label = ",".join(forced)
            if forced:
                since = min((self._deferred_since(r) or time.time()) for r in forced)
                hours = (time.time() - since) / 3600
                log(f"updating although {label} (deferred {hours:.1f} h, past the {self.defer_limit_s / 3600:.0f} h limit)")
            self._step(cycle_id, step, StepState.STARTED, **({"forced": label} if forced else {}))
            done: dict = {}

            def on_event(event: dict) -> None:
                if event.get("event") == "done":
                    done.update(event)
                self.emit(Topic.UPDATE_STEP, {"cycle_id": cycle_id, "step": step, "event": event})

            log_path = paths.service_dir() / UPDATE_LOG_NAME
            with contextlib.suppress(OSError):
                if log_path.stat().st_size > MAX_LOG_BYTES:
                    log_path.unlink()
            # From the last look to the child's start nothing here awaits, so no
            # hold is admitted in between; from now on `run.hold` refuses one
            # (an in-place update would replace what that run imports from).
            self.applying = not self.beside
            started_at = time.time()
            overran: children.Overran | None = None
            try:
                code = await children.run_events(
                    "update",
                    {},
                    env_extra={
                        **login,
                        TRIGGER_ENV: REPORT_FOR_CHECK.get(trigger, "cli"),
                        barrier.TOKEN_ENV: token,
                        # Only a run past its own limit lets the child skip its
                        # run check: a run that just started never is (D33).
                        **({FORCED_ENV: DeferReason.RUN_IN_FLIGHT} if DeferReason.RUN_IN_FLIGHT in forced else {}),
                        **({SKIP_CLI_ENV: "1"} if skip_cli else {}),
                        **({SIDE_BY_SIDE_ENV: "1"} if self.beside else {}),
                    },
                    on_event=on_event,
                    on_start=started,
                    log_path=log_path,
                    # Past it the child is stopped (its group: SIGTERM, then
                    # SIGKILL past the grace) and this step fails, so the next
                    # cycle can run (UPDATE_TIMEOUT_S).
                    timeout=self.update_timeout_s,
                    grace=self.update_stop_grace_s,
                )
            except children.Overran as exc:
                overran = exc
            except OSError as exc:
                self._step(cycle_id, step, StepState.FAILED, detail=f"the update could not start: {exc}")
                return {"state": StepState.FAILED, "detail": f"the update could not start: {exc}"}
            except asyncio.CancelledError:
                # The service stops while the update still runs: the barrier stays
                # (it names the child), and the next service finds the child's
                # wizard.lock and defers -- until the child is past the time
                # limit, when the next service stops it (`overrun_update`).
                lower = not child or child[0].poll() is not None
                raise
        finally:
            self.applying = False
            if lower:
                barrier.lower(token)
        if overran is not None:
            return await self._overran(cycle_id, overran, done, started_at, forced=label if forced else None)
        code = 128 - code if code < 0 else code
        outcome = {"exit_code": code, "ok": done.get("ok"), "complete": done.get("complete")}
        if forced:
            outcome["forced"] = label
        if skip_cli:
            outcome["cli"] = "left as it is: daemon workers run from it"
        if code == WIZARD_BUSY_EXIT:
            # The child found a setup holding wizard.lock and recorded the skip itself.
            self._step(cycle_id, step, StepState.DEFERRED, reason=DeferReason.SETUP_RUNNING, exit_code=code)
            return {"state": StepState.DEFERRED, "reason": DeferReason.SETUP_RUNNING, **outcome}
        # A child that wrote no `done` (killed before its first event, say) did
        # not finish: failed, whatever its exit status.
        state = StepState.DONE if code == 0 and done and done.get("ok") is not False else StepState.FAILED
        self._step(cycle_id, step, state, exit_code=code, ok=done.get("ok"), complete=done.get("complete"))
        return {"state": state, **outcome}

    async def _overran(
        self, cycle_id: str, overran: children.Overran, done: dict, started_at: float, *, forced: str | None
    ) -> dict:
        """The update child ran past `update_timeout_s` and was stopped: the
        step failed, saying so where people look -- this step (`update.status`,
        `probe doctor`'s Updates row) and the attempt `probe doctor` prints
        (`record_stopped`). The child's own report to the server says it was
        stopped (`probe.cli.update_report.merged_run`)."""
        limit = span(self.update_timeout_s)
        code = overran.code
        how = overran.how
        detail = f"the update ran past {limit} and " + ("would not stop" if how == Stopped.RUNNING else "was stopped")
        log(f"{detail} ({how})")
        await record_stopped_off_loop(detail, version=self.version, since=started_at)
        outcome: dict = {
            "detail": detail,
            "stopped_by": how,
            "exit_code": None if code is None else 128 - code if code < 0 else code,
            "ok": done.get("ok"),
            "complete": done.get("complete"),
        }
        if forced:
            outcome["forced"] = forced
        self._step(cycle_id, UpdateStep.CLI_AND_PLUGINS, StepState.FAILED, **outcome)
        return {"state": StepState.FAILED, **outcome}

    async def _app(self, cycle_id: str, trigger: str) -> dict:
        """Step 2: the desktop app's update check, at most once per
        CHECK_EVERY_S, handed to the open app (`app.check`). Never launches
        the app: closed, it is checked at its next launch."""
        step = UpdateStep.APP
        record = self._app_record()
        if record is not None and record.get("delegated_at") is not None and record.get("cycle_id") == cycle_id:
            # The app's launch check started this cycle and has its check already.
            out = self._app_step(record)
        else:
            decision = self.app_decision()
            if record is not None and record.get("state") == StepState.READY:
                # A downloaded update waits for the app to quit: no second check.
                out = {
                    "state": StepState.SKIPPED,
                    "outcome": AppStepOutcome.READY_WAITING,
                    **({"version_after": record["version_after"]} if record.get("version_after") else {}),
                }
            elif decision["reason"] == AppCheckReason.IN_PROGRESS and record is not None:
                out = self._app_step(record)
            elif not decision["due"]:
                out = {"state": StepState.SKIPPED, "outcome": decision["reason"]}
            elif (target := self.app_target()) is not None:
                # One app connection gets it (the newest) and owns it.
                record = self._delegate(cycle_id=cycle_id, trigger=trigger, via=Topic.APP_CHECK, owner=target)
                if self.send_app_check(target, {"cycle_id": cycle_id}):
                    out = self._app_step(record, AppStepOutcome.APP_CHECK_SENT)
                else:
                    self.app_gone(target)
                    out = self._app_step(self.state["app"])
            elif self.app_connected() > 0:
                # An older app build: it checks for its own update at its launch.
                out = {"state": StepState.SKIPPED, "outcome": AppStepOutcome.APP_NOT_LISTENING}
            else:
                found = await asyncio.to_thread(appupdate.installed)
                out = {
                    "state": StepState.SKIPPED,
                    "outcome": AppStepOutcome.APP_CLOSED if found else AppStepOutcome.NOT_INSTALLED,
                    **({"version": found["version"]} if found and found.get("version") else {}),
                }
        detail = {k: v for k, v in out.items() if k != "state"}
        self._step(cycle_id, step, out["state"], **detail)
        return out

    def after_update_action(self) -> None:
        """A person's Update (`action.run update`) ran outside a cycle: read
        the CLI version a fresh process imports and, when it moved, restart
        as a cycle's self step would. This service is old code then, and
        anything it imported later would come from the new files."""
        if self._loop is None:
            return
        task = self._loop.create_task(self._after_update_action())
        self._side_tasks.add(task)
        task.add_done_callback(self._side_tasks.discard)

    async def _after_update_action(self) -> None:
        try:
            code, value = await children.run_read("version", {}, timeout=VERSION_TIMEOUT_S)
        except OSError as exc:
            log(f"version check after the update action could not start: {exc}")
            return
        installed = value.get("cli_version") if isinstance(value, dict) else None
        if code == 0 and isinstance(installed, str) and installed and installed != self.version:
            log(f"the update action installed {installed} (this service is {self.version}): restarting")
            # Watched like a cycle's switch (D5) when it was one.
            with contextlib.suppress(Exception):
                from probe._shared import installs

                if installs.active() is not None:
                    self.guard_pending = installed
            self.stop(StopReason.UPDATE)

    def _spawn_guard(self, to_version: str) -> None:
        """Before this service exits for `to_version`, start the guard (D5)
        from THIS version's interpreter: it starts the new service, watches it,
        and switches back when it will not run. The interpreter of the version
        it would return to: this one's version env, or after the first switch
        (this service still runs through the moved folder's old path) the
        moved folder itself (`probe._shared.installs.previous`). Never raises."""
        try:
            from probe._shared import installs

            from . import procid

            python = sys.executable
            if not installs.running_from_versions(sys.prefix):
                prior = installs.previous()
                if prior is None:
                    log("no guard: no version to switch back to")
                    return
                python = str(installs.env_python(prior))
            import subprocess

            log_fd = os.open(paths.log_path(), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
            try:
                subprocess.Popen(  # noqa: S603 -- the previous version's interpreter, our own module
                    [python, "-I", "-m", "probe.service.guard", "--from", self.version,
                     "--to", to_version, "--old-python", python, "--old-pid", str(os.getpid()),
                     "--old-start", procid.start_time(os.getpid()) or ""],
                    stdin=subprocess.DEVNULL,
                    stdout=log_fd,
                    stderr=log_fd,
                    cwd=str(paths.service_dir()),
                    env=dict(os.environ),
                    start_new_session=True,
                    close_fds=True,
                )
            finally:
                os.close(log_fd)
            log(f"guard started for {to_version}")
        except Exception as exc:  # noqa: BLE001 -- the update stands; it is only unwatched
            log(f"could not start the guard: {exc!r}")

    async def _self(self, cycle_id: str) -> tuple[dict, bool]:
        """Step 3: did step 1 install a new CLI? Then this service is old code."""
        step = UpdateStep.SELF
        try:
            code, value = await children.run_read("version", {}, timeout=VERSION_TIMEOUT_S)
        except OSError as exc:
            code, value = None, None
            log(f"version check could not start: {exc}")
        installed = value.get("cli_version") if isinstance(value, dict) else None
        if code != 0 or not isinstance(installed, str) or not installed:
            self._step(cycle_id, step, StepState.FAILED, detail="could not read the installed CLI version")
            return {"state": StepState.FAILED, "detail": "could not read the installed CLI version"}, False
        restart = installed != self.version
        detail = {"from_version": self.version, "to_version": installed, "restart": restart}
        self._step(cycle_id, step, StepState.DONE, **detail)
        return {"state": StepState.DONE, **detail}, restart
