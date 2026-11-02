"""when an update may run: forced past a setup, a menu waiting on a person, its wait and lock, the service stopped on Windows."""

from __future__ import annotations
import contextlib
import os
import time
from contextlib import ExitStack, contextmanager

from probe import __version__
# `update_report` is imported HERE, at the top, for the same reason updater.py
# imports its whole call graph eagerly (H8): it runs after `uv tool upgrade` has
# replaced the installed tree, when a first import would read the new files.
from probe.shared.updates import autoupdate
from probe.cli.install import updater
from probe.cli.wizard.session import lock as wizard_lock
from probe.shared.updates import update_report
from probe.shared.updates import step as update_step


#: Set by the Probe service (`probe.service.updater.settings.SKIP_CLI_ENV`) when the CLI
#: is current and daemon workers run from its env: plugins only.
SKIP_CLI_ENV = update_step.SKIP_CLI_ENV
#: Set by the Probe service (`probe.service.updater.settings.FORCED_ENV`) when it updates
#: past what deferred it for DEFER_LIMIT_S: those reasons, comma separated
#: (`forced_past`). Past a live run the run-lock check is skipped (D33); past a
#: setup holding wizard.lock for a day, the update runs without that lock (C1).
FORCED_ENV = update_step.FORCED_ENV


def forced_past(reason: str) -> bool:
    """Did the Probe service decide to update past `reason` (a
    `probe.foundation.service_api.vocabularies.DeferReason`), naming it in FORCED_ENV?"""
    return reason in os.environ.get(FORCED_ENV, "").split(",")


def menu_holds_update_off() -> bool:
    """Does a `probe wizard` menu in another process wait on a person
    (`setup_marks.menu_waiting`) -- for less than a day -- while this update
    may move the files that menu runs from? The menu lets go of wizard.lock
    while it waits (C1), so this marker is what stops an update from replacing
    files under it mid-write: as the lock, for a day at most, and never once
    the Probe service decided to go past a setup (FORCED_ENV).

    Only an update bound to go beside the running version passes it: the
    Probe service's, which says so (REQUIRE_SIDE_BY_SIDE_ENV) and then never
    falls back to in place. Any other may: a side-by-side machine still updates
    in place with IN_PLACE_ENV, a receipt it cannot restate, or no target
    version known (`updater.upgrade_side_by_side`), so it waits. Never raises:
    unknown reads as no."""
    try:
        from probe.shared.updates import setup_marks
        from probe.sdk import session_marker
        from probe.foundation.service_api.vocabularies import DeferReason

        if (
            forced_past(DeferReason.SETUP_RUNNING)
            or os.environ.get(updater.REQUIRE_SIDE_BY_SIDE_ENV) == "1"
            # Plugins only (the service's, or what follows an adopt's switch):
            # the CLI's files stay where they are.
            or os.environ.get(SKIP_CLI_ENV) == "1"
        ):
            return False
        waiting, since = setup_marks.menu_waiting(session_marker.state_dir(), exclude_pid=os.getpid())
        if not waiting:
            return False
        from probe.service.updater.settings import DEFER_LIMIT_S

        return since is None or time.time() - since < DEFER_LIMIT_S
    except Exception:  # noqa: BLE001
        return False


@contextlib.contextmanager
def _service_stopped_on_windows(install):
    """Windows (R3): the Probe service runs from the CLI's own uv tool env, and
    Windows cannot replace a file a running process holds. Stop it (its
    recorders pause, saved) for the upgrade, and start it again after (they
    resume). Yields False when it would not stop: the upgrade waits for the
    next try rather than half-replace an env in use. Elsewhere, and for any
    other install, nothing (True).

    Held through the upgrade: `start.lock`, so no hook, tap or keeper starts
    one meanwhile (`client.ensure` finds it taken and starts none), and
    `service.lock`, so one started just before exits as a duplicate."""
    if os.name != "nt" or install.method != updater.Method.UV_TOOL:
        yield True
        return
    from probe.foundation import service_api as client
    from probe.foundation.service_api import paths
    from probe.foundation.service_api.wire import Method

    held: list[int] = []
    is_asked = False
    is_stopped = True
    try:
        paths.ensure_dirs()
        with contextlib.suppress(Exception):  # none runs, or it cannot be asked
            client.call(Method.STOP, {}, client="cli", client_version=__version__, timeout=5.0)
            is_asked = True
        for path in (paths.start_lock_path(), paths.lock_path()):
            fd = os.open(path, os.O_RDWR | os.O_CREAT)
            deadline = time.monotonic() + (15.0 if is_asked else 2.0)
            while not paths.try_lock(fd):
                if time.monotonic() >= deadline:
                    os.close(fd)
                    is_stopped = False
                    break
                time.sleep(0.2)
            else:
                held.append(fd)
            if not is_stopped:
                break
    except OSError:
        pass  # no folder for it: none runs
    try:
        yield is_stopped
    finally:
        for fd in reversed(held):
            with contextlib.suppress(OSError):
                paths.unlock(fd)
            with contextlib.suppress(OSError):
                os.close(fd)
        if is_asked:
            with contextlib.suppress(Exception):
                client.ensure()


@contextmanager
def _update_turn(manifest: dict | None, trigger: update_report.Trigger):
    """The wait and the lock an update takes before it changes anything."""
    # WAIT FOR THE PROCESS THAT SPAWNED US, if it named itself.
    #
    # Only the detached auto-update path sets this; the wizard's interactive
    # Update action has no parent to outlive and skips the wait. Replacing the
    # installed tree while the triggering command is still lazily importing from
    # it is how you get a ModuleNotFoundError out of a command that has worked
    # for a year (see autoupdate.wait_for_pid_exit).
    parent = os.environ.get(autoupdate.WAIT_FOR_PID_ENV)
    if parent:
        try:
            autoupdate.wait_for_pid_exit(int(parent))
        except (TypeError, ValueError):
            pass

    # ONE SETUP AT A TIME (`wizard_lock`), and only after the wait: the process
    # that spawned us can be a `probe wizard`, which holds the lock until it
    # exits. The wizard's own Update action holds it already and goes through.
    # So does an update the Probe service runs past a setup that has held the
    # lock for a day (C1): without it, beside that setup, as the service decided.
    # A menu waiting on a person holds no lock: its marker holds an update off
    # that would move its files (`menu_holds_update_off`).
    from probe.foundation.service_api.vocabularies import DeferReason  # loaded already, by `updater`

    with ExitStack() as stack:
        try:
            stack.enter_context(wizard_lock.held())
            if menu_holds_update_off():
                raise wizard_lock.Busy(wizard_lock.BUSY_MESSAGE)
        except wizard_lock.Busy:
            if not forced_past(DeferReason.SETUP_RUNNING):
                autoupdate.record_skip(
                    autoupdate.SKIP_SETUP_RUNNING,
                    available=updater.cli_latest(manifest) if manifest else None,
                    trigger=trigger.value,
                )
                raise
        yield
