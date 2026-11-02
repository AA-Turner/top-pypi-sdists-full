"""is the machine quiet (X1): no setup, worker or run in the way; how long each reason has deferred, and when to update past it."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from pathlib import Path
from ....foundation.service_api.vocabularies import (
    DeferReason,
    REPORT_FOR_CHECK)
from probe.service.updater.quiet.workers import _flock_held, live_workers, state_dirs
from probe.service.updater.settings import LIMITED, WIZARD_LOCK_NAME, _SKIPS


# -- is the machine quiet? (plan X1) -----------------------------------------


def setup_running(extra_dirs=()) -> bool:
    """Does a Probe setup hold the device now: a `probe wizard`, `probe update`
    or `probe uninstall` (run from a terminal or anywhere else), by its
    `wizard.lock` in any state folder this service knows of (`state_dirs`)?
    What writes Codex's config beside it waits (`codextrust`)."""
    return any(_flock_held(state / WIZARD_LOCK_NAME) for state in state_dirs(extra_dirs))


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
    #: A setup holds wizard.lock ...
    setup: bool = False
    #: ... since then (the latest of their records), or None: not known.
    setup_since: float | None = None
    #: A `probe wizard` menu waits on a person (`setup_marks.menu_waiting`): a
    #: setup only for an update that moves the files it runs from (not side by
    #: side: the cycle clears it then) ...
    menu: bool = False
    #: ... since then, or None: not known.
    menu_since: float | None = None

    def setup_time(self) -> float | None:
        """Since when the setups found (`setup`, `menu`) have held the device:
        the latest, as every one must be past the limit; None when one's time
        cannot be told, or none was found."""
        times = ([self.setup_since] if self.setup else []) + ([self.menu_since] if self.menu else [])
        if not times or None in times:
            return None
        return max(times)

    def blocking(self) -> str | None:
        """Why nothing may update, live sessions' workers aside (they are asked
        to stop). A worker finishing an ended session's queue blocks."""
        if self.action:
            return DeferReason.ACTION_RUNNING
        if self.unseen_daemon or self.workers is None or any(w.draining for w in self.workers):
            return DeferReason.DAEMON_RECORDING
        if self.run:
            return DeferReason.RUN_IN_FLIGHT
        if self.setup or self.menu:
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
        if self.setup or self.menu:
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
    exclude_pid: int | None = None,
) -> Busy:
    """The quiet check (X1), in the default state folder and every live
    session's own (D13). `run_held`: a `probe exec` holds a run here
    (`run.hold`); the run locks are still looked for, for the runs no hold
    names (the SDK's, a `probe exec` from before the hold, or one that found
    no service). `exclude_pid`: a process looking for itself's sake (an
    update a wizard menu started, in the same process after the hand-off's
    exec): its own menu marker, and a wizard.lock its record says it holds,
    are no setup to wait for."""
    dirs = state_dirs(extra_dirs)
    busy = Busy(action=action_running, unseen_daemon=unseen_daemon, workers=live_workers(dirs))
    if run_held:
        busy.run = True
    else:
        try:
            from probe.foundation.durable import run_lock

            busy.run = any(run_lock.any_live(state / run_lock.RUNS_DIRNAME) for state in dirs)
        except Exception:  # noqa: BLE001 -- unknown reads as a live run, as run_lock itself does
            busy.run = True
    held = [
        state / WIZARD_LOCK_NAME for state in dirs
        if _flock_held(state / WIZARD_LOCK_NAME) and not _held_by(state / WIZARD_LOCK_NAME, exclude_pid)
    ]
    busy.setup = bool(held)
    if held:
        since = [setup_held_since(lock) for lock in held]
        busy.setup_since = None if None in since else max(since)
    menus = [menu for menu in (_menu_waiting(state, exclude_pid) for state in dirs) if menu[0]]
    busy.menu = bool(menus)
    if menus:
        since = [at for _, at in menus]
        busy.menu_since = None if None in since else max(since)
    return busy


def setup_held_since(lock: Path) -> float | None:
    """When the setup holding `lock` (a wizard.lock found held) took it: the
    record its holder wrote (`setup_marks.holder`), while that exact process
    (pid and start time) still runs. None when it cannot be told: a holder from
    before the record (the file then holds nothing, or a record whose writer is
    gone), a record dated ahead of the clock, or one that does not read."""
    try:
        from probe.shared.updates import setup_marks

        state, at, _pid = setup_marks.holder(lock)
    except Exception:  # noqa: BLE001 -- cannot be told
        return None
    return at if state == setup_marks.ALIVE else None


def _held_by(lock: Path, pid: int | None) -> bool:
    """Does `lock`'s holder record name `pid`, its writer still running?"""
    if pid is None:
        return False
    try:
        from probe.shared.updates import setup_marks

        state, _at, holder_pid = setup_marks.holder(lock)
    except Exception:  # noqa: BLE001
        return False
    return state == setup_marks.ALIVE and holder_pid == pid


def _menu_waiting(state: Path, exclude_pid: int | None = None) -> tuple[bool, float | None]:
    """`setup_marks.menu_waiting` for one state folder; one that cannot be
    read is no menu (the lock still guards every write the menu makes)."""
    try:
        from probe.shared.updates import setup_marks

        return setup_marks.menu_waiting(state, exclude_pid=exclude_pid)
    except Exception:  # noqa: BLE001
        return False, None


def busy_reason(*, action_running: bool, daemon_session: bool = False) -> str | None:
    """Why the CLI env cannot be updated right now (a DeferReason), or None:
    the quiet check before D7, workers included (`probe doctor`'s view).

    `daemon_session`: a live daemon-mode session whose worker's lock may sit
    out of sight (registered without its state folder)."""
    return look(action_running=action_running, unseen_daemon=daemon_session).reason()


def auto_update_enabled(extra_dirs=()) -> bool:
    """The wizard's setting (`autoupdate.json`), read the way every updater
    reads it: on unless a person turned it off, for the managed CLI this
    service runs from; opt-in for any other install (`version_policy.autoupdate_state`, C2).
    A `false` in any state folder this service knows of is off: its own, and
    every live session's (`extra_dirs`, D13), where a person who runs with
    XDG_STATE_HOME saved it."""
    try:
        from probe.shared.updates import version_policy

        return version_policy.autoupdate_enabled(extra_dirs=extra_dirs)
    except Exception:  # noqa: BLE001 -- version_policy never raises; a broken import updates nothing
        return False


def record_skip(reason: str, trigger: str) -> None:
    """The deferral, in the record `probe doctor` prints (under the server's
    report word for `trigger`). Never raises."""
    name = _SKIPS.get(reason)
    if name is None:
        return
    try:
        from probe.shared.updates import autoupdate

        report = REPORT_FOR_CHECK.get(trigger, "cli")
        autoupdate.record_skip(getattr(autoupdate, name), trigger=autoupdate.Trigger(report))
    except Exception:  # noqa: BLE001 -- a diagnostic
        pass


class QuietMixin:
    """Part of Updater: its methods run with `self` the Updater; compose() folds them into Updater."""

    def _look(self) -> Busy:
        busy = look(
            action_running=self.action_running(),
            unseen_daemon=self.daemon_session(),
            extra_dirs=self.session_state_dirs(),
            run_held=self.run_held(),
        )
        self.last_busy = busy
        return busy

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
        self.last_busy = busy
        return busy

    def _streaks(self) -> dict:
        """`{reason: since}`: how long each reason has deferred without a break."""
        value = self.state.get("deferred_since")
        if not isinstance(value, dict):
            return {}
        return {k: float(v) for k, v in value.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}

    def _deferred_since(self, reason: str | None = None) -> float | None:
        held = self.last_busy.setup_time() if self.last_busy is not None else None
        if reason == DeferReason.SETUP_RUNNING and held is not None:
            # How long the lock has been held (or the menu has waited), not how
            # long this service has deferred on it (C1): a wizard left open for
            # days before this service started is past the limit at its first look.
            return held
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
