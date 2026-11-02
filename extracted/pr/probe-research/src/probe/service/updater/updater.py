"""The service's updater: the machine's one automatic updater (plan "Updating everything", X1, R2, R3, D3, D4).

    when     after discovery, if the last check is CHECK_EVERY_S old (or there
             never was one); then every CHECK_EVERY_S while the service runs;
             on `update.check_now` (the CLI and the plugin hook, instead of
             spawning an updater of their own); never while automatic updates
             are off (`autoupdate.json` `enabled`, the wizard's setting: on
             for the managed CLI unless a person turned it off, C2)
    cycle    update.started
             1 cli_and_plugins  only on a quiet machine (X1): no run holds a
                                run lock or a `run.hold` (a `probe exec`'s,
                                `runholds.py`), no wizard holds wizard.lock (nor,
                                for an update that moves the CLI's files, waits
                                at its menu: `setup_marks`), no
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
                                action -- each reason its own 24 h -- or by a
                                setup that has held wizard.lock that long (its
                                holder's record says since when, C1), the next
                                cycle updates anyway, in place (the child told,
                                PROBE_UPDATE_FORCED, when that is past a run or
                                a setup), as the updater before the service
                                always did (D7, D33): a machine that is never
                                quiet, or a wizard menu left open, still
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
             2 app              the desktop app's update, at most once per
                                CHECK_EVERY_S. A CLOSED app on macOS (installed,
                                no app connection, no process of it, its
                                instance lock free) is installed by the service
                                itself (`appinstall.py`): the app's own manifest,
                                signature and key, never a downgrade, an atomic
                                bundle swap, no app process started; `installed`
                                (or `current`, `failed`) is the step and the
                                app's check, so its next launch is not due. A
                                skip (`not_writable`, `app_running`,
                                `not_permitted`) records nothing: the app's own
                                updater checks at its next launch. Elsewhere
                                (Linux, Windows) there is no app. The check is
                                handed to an OPEN app: an app
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
                                as failed (due again). The service never
                                launches the app. At its launch
                                the app asks itself (`update.check_now`
                                trigger `app` with `app`): the answer's
                                `app: {due, reason}` hands it the check then.
             3 self             the CLI version a fresh process imports; a new
                                one means this service is old code: it finishes
                                the cycle, says `service.stopping{update}` and
                                exits. The next `ensure` (a tap re-registering,
                                the app reconnecting) starts the new code.
             update.done
    hold     a running cycle keeps the service alive (R3): HOLD_S, and while
             its update child runs, as long as that child may (its time
             limit and stop grace), then HOLD_S again for the rest (B2: a
             keeper-started cycle has no session to keep the service up)
    imports  everything the cycle needs is imported before step 1 replaces
             the files it would import from (R2)

The SDK in researchers' own project environments is never touched (D4).

Stdlib only at import (the start path; plan S1). `probe._shared` (run locks,
the skip record) and `probe.shared.updates.version_policy` (the setting) are light and
imported when a cycle runs.
"""

from __future__ import annotations

import asyncio
import os
import secrets
import time
from collections.abc import Callable
from ...foundation.service_api.vocabularies import (
    APP_RESULT_TIMEOUT_S,
    BusyHolder,
    CheckOutcome,
    DeferReason,
    StepState,
    CheckTrigger,
    Topic,
    UpdateStep)
from ...foundation.compose.compose import compose
from probe.service.updater.app_decision import AppDecisionMixin
from probe.service.updater.child import ChildMixin
from probe.service.updater.cycle import CycleMixin
from probe.service.updater.install_switch import _guard_record
from probe.service.updater.quiet.quiet import Busy, QuietMixin, auto_update_enabled
from probe.service.updater.quiet.workers import WorkersMixin
from probe.service.updater.settings import (
    APP_RESULT_TIMEOUT_ENV,
    CHECK_EVERY_S,
    CHECK_NOW_COOLDOWN_S,
    DEFERRED_RETRY_S,
    DEFER_LIMIT_ENV,
    DEFER_LIMIT_S,
    FOLLOWUP_MAX_AGE_S,
    HOLD_S,
    SESSION_END_RETRY_MAX_S,
    SESSION_END_RETRY_S,
    UPDATE_STOP_GRACE_ENV,
    UPDATE_STOP_GRACE_S,
    UPDATE_TIMEOUT_ENV,
    UPDATE_TIMEOUT_S,
    WORKER_STOP_ENV,
    WORKER_STOP_S,
    _env_seconds,
    _installs_closed_app,
)
from probe.service.updater.state import StateMixin
from probe.service.updater.steps.app import AppStepMixin
from probe.service.updater.steps.cli import CliStepMixin


# -- the updater ---------------------------------------------------------------


@compose
class Updater(
    StateMixin,
    QuietMixin,
    WorkersMixin,
    ChildMixin,
    AppDecisionMixin,
    CycleMixin,
    CliStepMixin,
    AppStepMixin,
):
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
        followup: Callable[[bool], None] = lambda restart: None,
        stop_hosted: Callable[[str], bool] = lambda sid: False,
    ) -> None:
        self.version = version
        #: Stop one session's run in this service's daemon host (`WorkerHost.stop_hosted`):
        #: the D7 hand-over of a hosted worker, whose pid is the host's.
        self.stop_hosted = stop_hosted
        #: An update installed something (a cycle's update child ran, or a
        #: person's Update action did): what open sessions read follows it now
        #: (`followup.py`), told whether this service restarts onto a new CLI
        #: first (then the next one does it: `take_followup`).
        self.followup = followup
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
        #: Called when what holds the service changes (a cycle starts, lets go of the slot, or ends).
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
        #: What the last look found (`_look`): the setup's own time, where it
        #: can be told (`Busy.setup_time`), after the cycle cleared what does
        #: not hold its kind of update off (a menu, side by side).
        self.last_busy: Busy | None = None
        self.app_result_timeout_s = _env_seconds(APP_RESULT_TIMEOUT_ENV, APP_RESULT_TIMEOUT_S)
        self.update_timeout_s = _env_seconds(UPDATE_TIMEOUT_ENV, UPDATE_TIMEOUT_S)
        self.update_stop_grace_s = _env_seconds(UPDATE_STOP_GRACE_ENV, UPDATE_STOP_GRACE_S)
        self.state = self._load()
        self._migrate_app_check()
        self.cycle_id: str | None = None
        self.step: str | None = None
        self.task: asyncio.Task | None = None
        #: True from a cycle's start to the end of its CLI-and-plugins step: the
        #: one mutating slot is the update's (`action.run` queues an action
        #: behind it, and answers an Update busy).
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
        #: The start-time `_recover_closed` (macOS), until it is done.
        self._recovering: asyncio.Task | None = None

    def in_progress(self) -> bool:
        return self.task is not None and not self.task.done()

    def mark_followup(self, cycle_id: str | None) -> None:
        """This service restarts onto a new CLI before it follows the update
        up: the next service, the new code, does it (`take_followup`)."""
        self.state["followup"] = {"at": time.time(), "cycle_id": cycle_id}
        self._save()

    def take_followup(self) -> bool:
        """Is a follow-up of an update left for this service: one the service
        before it marked (`mark_followup`, within FOLLOWUP_MAX_AGE_S), or this
        CLI version has never followed one up (`followed_version`: the first
        start after an update by a service before this code, or by hand)?
        Taken: asked once per mark and per version."""
        def fresh(at: object) -> bool:
            return isinstance(at, (int, float)) and 0 <= time.time() - at < FOLLOWUP_MAX_AGE_S

        record = self.state.pop("followup", None)
        marked = fresh(record.get("at") if isinstance(record, dict) else None)
        followed = self.state.get("followed_version")
        last = self.state.get("last_result")
        to = ((last.get("steps") or {}).get(UpdateStep.SELF) or {}).get("to_version") if isinstance(last, dict) else None
        # A version followed up before this one, or (a service before this
        # code, which recorded none) the cycle that restarted onto this one.
        moved = followed not in (None, self.version) or (
            followed is None and isinstance(last, dict) and bool(last.get("restart")) and to == self.version
            and fresh(last.get("at"))
        )
        if record is None and not moved:
            return False
        self.state["followed_version"] = self.version
        self._save()
        return marked or moved

    def busy_holder(self) -> dict | None:
        if self.slot and self.in_progress():
            return {"kind": BusyHolder.UPDATE, "cycle_id": self.cycle_id}
        return None

    def holding(self) -> bool:
        """Does a running cycle keep the service alive (its hold, R3)?"""
        return self.in_progress() and time.monotonic() < self.hold_until

    def _hold(self, seconds: float) -> None:
        """Hold the service for `seconds` from now; then it looks again at what holds it."""
        self.hold_until = time.monotonic() + seconds
        if self._hold_end is not None:
            self._hold_end.cancel()
        self._hold_end = self._loop.call_later(seconds + 0.05, self.changed)

    def _hold_for_child(self) -> float:
        """The longest an update child runs: its time limit, then the stop's
        grace (a hard cap: past it the child is killed, `children.run_events`)."""
        return self.update_timeout_s + self.update_stop_grace_s

    def public(self) -> dict:
        """`service.status`'s `update`, and `update.status`."""
        return {
            "enabled": auto_update_enabled(self.session_state_dirs()),
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
        if _installs_closed_app() and self._loop is not None:
            # Whether or not a cycle is due; a cycle's app step waits for it (`_sweep_closed`).
            task = self._loop.create_task(self._recover_closed())
            self._recovering = task
            self._side_tasks.add(task)
            task.add_done_callback(self._side_tasks.discard)
        if requested is not None:
            self.check_now(requested)
        elif auto_update_enabled(self.session_state_dirs()) and (self.due() or self.pending is not None):
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
            delay = CHECK_EVERY_S if last is None else max(60.0, last + self.interval() - time.time())
        self._timer = self._loop.call_later(delay, self._tick)

    def _tick(self) -> None:
        self._timer = None
        if not self.in_progress() and auto_update_enabled(self.session_state_dirs()) and (self.due() or self.pending is not None):
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
        if not auto_update_enabled(self.session_state_dirs()):
            self.emit(Topic.UPDATE_DEFERRED, {"cycle_id": None, "reason": DeferReason.AUTO_UPDATE_OFF, "trigger": trigger})
            return {"outcome": CheckOutcome.DEFERRED, "reason": DeferReason.AUTO_UPDATE_OFF}
        last = self.last_check
        # The lifeboat's ask (`keeper`) is never `recent`: it asks only when it
        # saw a newer release than the last check could, at most every
        # half hour, and a service that answers it with no cycle idles out
        # and reads to the lifeboat as one that cannot start.
        if last is not None and 0 <= time.time() - last < CHECK_NOW_COOLDOWN_S and not self.moved_back() \
                and trigger != CheckTrigger.KEEPER:
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
        if trigger is None or self.in_progress() or not auto_update_enabled(self.session_state_dirs()):
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
        self._hold(HOLD_S)
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
