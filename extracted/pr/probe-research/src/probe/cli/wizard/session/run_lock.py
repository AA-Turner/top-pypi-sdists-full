"""the wizard run lock: whether a run may change the device, hold the lock, let it go while the menu waits on a person, take it back for one action, step aside for a forced update."""

from __future__ import annotations

import contextlib
import contextvars
import sys

import typer
from ....sdk import session_marker


def _wizard_changes_device(action: str | None, *, yes: bool, who_records: str | None) -> bool:
    """Whether this wizard run may change the device, so must hold the run lock.

    Read-only runs never wait on (or block) one that writes: a diagnose, a
    headless account, settings or imports listing, a recorder row read without
    `--who-records`. Those report only when nobody can answer their screen."""
    from probe.cli import wizard as wizard
    from probe.cli.wizard.actions.onboarding import Action

    if action in {Action.DIAGNOSE, Action.MANUAL, Action.EXIT}:
        return False
    headless = yes or not wizard.interactive()
    if action in {Action.ACCOUNT, Action.IMPORT_JOBS, Action.DEFAULTS, Action.SETTINGS}:
        return not headless
    if action == Action.RECORDER:
        return who_records is not None or not headless
    return True


#: The hold `_wizard_run_lock` keeps for the block it guards (an ExitStack), so
#: the interactive menu can let go of the lock while it waits on a person and
#: take it again for each action (`_hold_for_action`, plan C1). None outside one.
_RUN_LOCK: contextvars.ContextVar[contextlib.ExitStack | None] = contextvars.ContextVar(
    "probe_wizard_run_lock", default=None
)


@contextlib.contextmanager
def _wizard_run_lock(needed: bool = True, *, command: str = "probe wizard", update_trigger=None):
    """Hold the device's wizard run lock (`wizard_lock`) for the block, or end
    the run at once: a second runner says so and exits `BUSY_EXIT_CODE`,
    having changed nothing. `command` names the runner in what it says; an
    update (`update_trigger`, an `update_report.Trigger`) turned away is also
    recorded as a skip, so `probe doctor` shows why it did not run -- unless
    the Probe service decided to update past a setup that has held the lock
    for a day (`upgrading.forced_past`, C1): that update goes on without it.

    The hold is `_RUN_LOCK` for the block: the interactive menu lets go of it
    while it waits on a person (`_wizard_session`), and marks that it waits
    instead (`_release_for_menu`); the mark goes with the block. An update is
    also turned away by another process's waiting menu, when it would move the
    files that menu runs from (`upgrading.menu_holds_update_off`)."""
    from probe.core import events as json_events
    from probe.cli.wizard.session import lock as wizard_lock

    def turned_away() -> typer.Exit:
        if update_trigger is not None:
            from probe.shared.updates import autoupdate

            autoupdate.record_skip(autoupdate.SKIP_SETUP_RUNNING, trigger=update_trigger.value)
        print(
            f"{command}: {wizard_lock.BUSY_MESSAGE} on this device (a terminal or the "
            "desktop app). Nothing has been changed: run this again when it finishes.",
            file=sys.stderr,
        )
        json_events.error(json_events.ErrorCode.BUSY, wizard_lock.BUSY_MESSAGE)
        return typer.Exit(wizard_lock.BUSY_EXIT_CODE)

    with contextlib.ExitStack() as stack:
        if needed:
            try:
                stack.enter_context(wizard_lock.held())
            except wizard_lock.Busy:
                if update_trigger is None or not _update_forced_past_setup():
                    raise turned_away() from None
            if update_trigger is not None and _menu_holds_update_off():
                raise turned_away()
        token = _RUN_LOCK.set(stack)
        try:
            yield
        finally:
            _RUN_LOCK.reset(token)
            if getattr(stack, "menu_marked", False):
                _unmark_menu()


def _update_forced_past_setup() -> bool:
    """Did the Probe service decide to update past a setup holding the lock (C1)?"""
    from probe.cli.install import upgrade as upgrading
    from probe.foundation.service_api.vocabularies import DeferReason

    return upgrading.forced_past(DeferReason.SETUP_RUNNING)


def _menu_holds_update_off() -> bool:
    """`upgrading.menu_holds_update_off`: another process's menu waits on a
    person, and this update would move the files it runs from."""
    from probe.cli.install import upgrade as upgrading

    return upgrading.menu_holds_update_off()


def _release_for_menu() -> None:
    """The interactive menu waits on a person: let go of the run lock, so a
    menu left open never holds another setup off, nor an update for more than
    a day (C1), and say that it waits (`setup_marks.mark_menu`): the files it
    runs from must not be moved under it (an update in place, or the first
    switch), while a side-by-side switch goes on. Its next action takes the
    lock again (`_hold_for_action`)."""
    stack = _RUN_LOCK.get()
    if stack is None:
        return
    from probe.shared.updates import setup_marks

    # The mark first, then the lock: an updater that looks in between sees one.
    setup_marks.mark_menu(session_marker.state_dir())
    stack.menu_marked = True  # its `_wizard_run_lock` removes the mark at the end
    stack.close()


def _unmark_menu() -> None:
    """The wizard's run ends: its menu, if it had one, waits no more."""
    try:
        from probe.shared.updates import setup_marks

        setup_marks.unmark_menu(session_marker.state_dir())
    except Exception:  # noqa: BLE001 -- a marker left behind names a process that is gone
        pass


def _hold_for_action(action, *, yes: bool, who_records: str | None) -> bool:
    """Take the run lock again for one action the menu chose, when the action
    may change the device (`_wizard_changes_device`). False when another setup
    holds it now -- or, for an Update, another process's menu waits and the
    update may move its files (`_menu_holds_update_off`, looked at before the
    lock is taken): nothing ran, and no lock is held while the page that says
    so waits (an Update turned away is a skip, as ever). Within a hold this
    process has (a run that started with `--action`), a no-op."""
    from probe.cli.wizard.session import lock as wizard_lock
    from probe.cli.wizard.actions import onboarding as actions_mod

    stack = _RUN_LOCK.get()
    if stack is None or not _wizard_changes_device(action, yes=yes, who_records=who_records):
        return True
    update = action == actions_mod.Action.UPDATE
    try:
        if update and _menu_holds_update_off():
            raise wizard_lock.Busy(wizard_lock.BUSY_MESSAGE)
        stack.enter_context(wizard_lock.held())
    except wizard_lock.Busy:
        if update and _update_forced_past_setup():
            return True  # as `_wizard_run_lock`: the service decided (C1)
        stack.close()
        if update:
            from probe.shared.updates import autoupdate

            autoupdate.record_skip(autoupdate.SKIP_SETUP_RUNNING, trigger=_update_action_trigger(yes).value)
        return False
    return True
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.update import _update_action_trigger  # noqa: E402 -- pieces need each other; the front door loads this one first
