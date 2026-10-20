"""The service's updater: the machine's one automatic updater (plan "Updating everything", X1, R2, R3, D3, D4).

    when     after discovery, if the last check is CHECK_EVERY_S old (or there
             never was one); then every CHECK_EVERY_S while the service runs;
             on `update.check_now` (the CLI and the plugin hook, instead of
             spawning an updater of their own); never while automatic updates
             are off (`autoupdate.json` `enabled`, the wizard's setting)
    cycle    update.started
             1 cli_and_plugins  only on a quiet machine (X1): no daemon worker
                                holds its session lock, no run holds a run lock,
                                no wizard holds wizard.lock, no action of ours
                                runs. Then the barrier (`barrier.py`), a settle,
                                the same check again, and `python -m
                                probe.core.run update`: the wizard's Update, which
                                moves the CLI's uv tool env (CLI, daemon, SDK) and
                                every coding agent's plugins and pi's package in
                                one run. Not quiet: update.deferred, a skip in
                                `autoupdate.json` (`probe doctor` shows it), and a
                                retry when a session ends or at the next cycle.
             2 app              the desktop app's own updater (`appupdate.py`),
                                at most once per CHECK_EVERY_S
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
import sys
import time
from collections.abc import Callable
from pathlib import Path

from . import appupdate, barrier, children, paths
from .protocol import (
    BusyHolder,
    CheckOutcome,
    DeferReason,
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
UPDATE_LOG_NAME = "update.log"
#: `probe.cli.update_report.TRIGGER_ENV`: what asked, for the server's report.
TRIGGER_ENV = "PROBE_AUTOUPDATE_TRIGGER"
#: `probe.cli.wizard_lock.LOCK_FILENAME`, under the default state dir.
WIZARD_LOCK_NAME = "wizard.lock"
#: `probe.cli.wizard_lock.BUSY_EXIT_CODE`: the update child found a setup running.
WIZARD_BUSY_EXIT = 75

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
    import fcntl

    try:
        handle = open(path, "rb")  # noqa: SIM115 -- closed below
    except FileNotFoundError:
        return False
    except OSError:
        return True
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
    except BlockingIOError:
        return True
    except OSError:
        return True
    else:
        with contextlib.suppress(OSError):
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        return False
    finally:
        handle.close()


def daemon_worker_running() -> bool:
    """A daemon worker holds `<state>/daemon/<sid>.lock` for its whole life."""
    try:
        locks = list((paths.state_dir() / "daemon").glob("*.lock"))
    except OSError:
        return True
    return any(_flock_held(lock) for lock in locks)


def busy_reason(*, action_running: bool, daemon_session: bool = False) -> str | None:
    """Why the CLI env cannot be updated right now (a DeferReason), or None.

    `daemon_session`: a live session registered in daemon mode. Its worker's
    lock is looked for under `~/.local/state/probe` only, but a session run
    with XDG_STATE_HOME keeps it under that instead, out of this service's
    sight (the service's own state never moves, plan X2): the registration
    says what the lock cannot."""
    if action_running:
        return DeferReason.ACTION_RUNNING
    if daemon_session or daemon_worker_running():
        return DeferReason.DAEMON_RECORDING
    try:
        from probe._shared import run_lock

        if run_lock.any_live():
            return DeferReason.RUN_IN_FLIGHT
    except Exception:  # noqa: BLE001 -- unknown reads as a live run, as run_lock itself does
        return DeferReason.RUN_IN_FLIGHT
    if _flock_held(paths.state_dir() / WIZARD_LOCK_NAME):
        return DeferReason.SETUP_RUNNING
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
    import fcntl  # noqa: F401
    import plistlib  # noqa: F401
    import subprocess  # noqa: F401

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
    ) -> None:
        self.version = version
        self.emit = emit
        #: Called when what holds the service changes (a cycle starts or ends).
        self.changed = changed
        self.stop = stop
        self.action_running = action_running
        self.discovering = discovering
        self.daemon_session = daemon_session
        self.state = self._load()
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
        self._side_tasks: set = set()

    # -- state -----------------------------------------------------------------

    def _load(self) -> dict:
        try:
            data = json.loads(paths.update_state_path().read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = None
        if not isinstance(data, dict) or data.get("v") != STATE_VERSION:
            data = {"v": STATE_VERSION}
        return data

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

    def _busy(self) -> str | None:
        return busy_reason(action_running=self.action_running(), daemon_session=self.daemon_session())

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
        }

    # -- scheduling --------------------------------------------------------------

    def attach(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    def after_discovery(self) -> None:
        """The service's discovery window is over: start a cycle when one is
        due (or was asked for meanwhile), and arm the schedule."""
        requested, self.requested = self.requested, None
        if requested is not None:
            self.check_now(requested)
        elif auto_update_enabled() and (self.due() or self.pending is not None):
            self.start(self.pending or CheckTrigger.SCHEDULE)
        self._arm()

    def _arm(self) -> None:
        if self._loop is None:
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

    def check_now(self, trigger: str) -> dict:
        """`update.check_now`: `{outcome, ...}` (CheckOutcome)."""
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
        if self._busy() is None:
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
        for handle in (self._timer, self._retry, self._hold_end):
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
            steps[UpdateStep.APP] = await self._app(cycle_id)
            if core["state"] in (StepState.DONE, StepState.FAILED):
                steps[UpdateStep.SELF], restart = await self._self(cycle_id)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 -- a bug costs this cycle, never the service
            log(f"cycle {cycle_id} failed: {exc!r}")
            steps["error"] = repr(exc)[:500]
        now = time.time()
        ok = deferred is None and all(
            isinstance(s, dict) and s.get("state") != StepState.FAILED for s in steps.values()
        ) and "error" not in steps
        result = {"cycle_id": cycle_id, "at": now, "trigger": trigger, "ok": ok, "steps": steps, "restart": restart}
        if deferred is None:
            self.state["last_check"] = now
            self.state["last_result"] = result
            self.pending = None
        else:
            self.state["last_deferred"] = {"at": now, "reason": deferred, "trigger": trigger}
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
            self._loop.call_soon(self.stop, StopReason.UPDATE)

    async def _core(self, cycle_id: str, trigger: str) -> dict:
        """Step 1: the CLI's env and the plugins, on a quiet machine only."""
        step = UpdateStep.CLI_AND_PLUGINS
        reason = self._busy()
        if reason is not None:
            self._step(cycle_id, step, StepState.DEFERRED, reason=reason)
            return {"state": StepState.DEFERRED, "reason": reason}
        token = secrets.token_hex(16)
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
            reason = self._busy()
            if reason is not None:
                self._step(cycle_id, step, StepState.DEFERRED, reason=reason)
                return {"state": StepState.DEFERRED, "reason": reason}
            self._step(cycle_id, step, StepState.STARTED)
            done: dict = {}

            def on_event(event: dict) -> None:
                if event.get("event") == "done":
                    done.update(event)
                self.emit(Topic.UPDATE_STEP, {"cycle_id": cycle_id, "step": step, "event": event})

            log_path = paths.service_dir() / UPDATE_LOG_NAME
            with contextlib.suppress(OSError):
                if log_path.stat().st_size > MAX_LOG_BYTES:
                    log_path.unlink()
            try:
                code = await children.run_events(
                    "update",
                    {},
                    env_extra={TRIGGER_ENV: REPORT_FOR_CHECK.get(trigger, "cli"), barrier.TOKEN_ENV: token},
                    on_event=on_event,
                    on_start=started,
                    log_path=log_path,
                )
            except OSError as exc:
                self._step(cycle_id, step, StepState.FAILED, detail=f"the update could not start: {exc}")
                return {"state": StepState.FAILED, "detail": f"the update could not start: {exc}"}
            except asyncio.CancelledError:
                # The service stops while the update still runs: the barrier stays
                # (it names the child), and the next service finds the child's
                # wizard.lock and defers.
                lower = not child or child[0].poll() is not None
                raise
        finally:
            if lower:
                barrier.lower(token)
        code = 128 - code if code < 0 else code
        outcome = {"exit_code": code, "ok": done.get("ok"), "complete": done.get("complete")}
        if code == WIZARD_BUSY_EXIT:
            # The child found a setup holding wizard.lock and recorded the skip itself.
            self._step(cycle_id, step, StepState.DEFERRED, reason=DeferReason.SETUP_RUNNING, exit_code=code)
            return {"state": StepState.DEFERRED, "reason": DeferReason.SETUP_RUNNING, **outcome}
        # A child that wrote no `done` (killed before its first event, say) did
        # not finish: failed, whatever its exit status.
        state = StepState.DONE if code == 0 and done and done.get("ok") is not False else StepState.FAILED
        self._step(cycle_id, step, state, exit_code=code, ok=done.get("ok"), complete=done.get("complete"))
        return {"state": state, **outcome}

    async def _app(self, cycle_id: str) -> dict:
        """Step 2: the desktop app, through its own updater, once per CHECK_EVERY_S."""
        step = UpdateStep.APP
        last = self._number("last_app_check")
        now = time.time()
        if last is not None and 0 <= now - last < CHECK_EVERY_S:
            self._step(cycle_id, step, StepState.SKIPPED, outcome="checked_recently")
            return {"state": StepState.SKIPPED, "outcome": "checked_recently"}
        self._step(cycle_id, step, StepState.STARTED)
        result = await appupdate.update()
        outcome = result.get("outcome")
        if outcome not in (appupdate.Outcome.RUNNING,):
            # A running app is asked again next cycle; anything else waits CHECK_EVERY_S.
            self.state["last_app_check"] = now
        if outcome in (appupdate.Outcome.UPDATED, appupdate.Outcome.CURRENT):
            state = StepState.DONE
        elif outcome in (appupdate.Outcome.FAILED, appupdate.Outcome.TIMEOUT):
            state = StepState.FAILED
        else:
            state = StepState.SKIPPED
        self._step(cycle_id, step, state, **result)
        return {"state": state, **result}

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
            self.stop(StopReason.UPDATE)

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
