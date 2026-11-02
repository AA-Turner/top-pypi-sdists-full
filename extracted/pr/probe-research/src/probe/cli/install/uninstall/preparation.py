"""before any phase: the scope, the confirmation (Keep first), server ids, the install lock, the plan."""

from __future__ import annotations
#: How long a fresh uninstall waits for an update that holds the install lock.
LOCK_WAIT_S = 30.0


# -- scope (U-T2) -------------------------------------------------------------------------


def _scope(run: Run) -> None:
    from probe.cli.install.uninstall import processes as uninstall_procs
    from probe.core import events

    force = run.options.force
    here = uninstall_procs.recorded_session_here()
    if here is not None:
        # Never with --force either: an agent must not uninstall Probe from
        # under the session it runs in. A person does it, outside any session.
        _step(events.Step.UNINSTALL_SCOPE, events.Status.FAILED, "inside a recorded agent session")
        raise Stop(EXIT_REFUSED, (
            f"probe uninstall: this runs inside an agent session Probe records ({here}), which uninstalling would "
            "tear down under it. Nothing was changed. Run `probe uninstall` yourself, in a terminal outside "
            "any agent session."), Reason.IN_SESSION, {"session": here})
    users = uninstall_procs.live_users()
    if users and not force:
        listed = "\n".join(f"  - {u.label}" for u in users)
        _step(events.Step.UNINSTALL_SCOPE, events.Status.FAILED, f"{len(users)} live user(s) of this install")
        raise Stop(EXIT_REFUSED, (
            f"probe uninstall: Probe is still in use on this computer:\n{listed}\n"
            "Nothing was changed. End them, or run `probe uninstall --force` to stop them all and go on."),
            Reason.LIVE_USERS, {"users": [u.as_json() for u in users]})
    _step(events.Step.UNINSTALL_SCOPE, events.Status.DONE,
          f"{len(users)} live user(s), stopped by --force" if users else "nothing else uses this install")


def _confirm(run: Run) -> None:
    """Interactive only: what is about to happen, Keep first."""
    if not run.options.interactive:
        return
    from probe.cli import wizard as wizard
    from probe.cli.wizard import terminal as tui

    with tui.window(enabled=True):
        tui.clear()
        answer = wizard.confirm_removal(tuple(run.agents), offline=run.options.offline)
    tui.leave_window()
    if answer is not True:
        _telemetry_declined(run)
        raise Stop(EXIT_REFUSED, "probe uninstall: nothing was changed.", Reason.CANCELLED)


# -- planning ------------------------------------------------------------------------------


def _server_ids(run: Run) -> dict | None:
    from probe.cli.install.uninstall import plan as uninstall_plan

    if run.options.offline:
        return None
    try:
        return uninstall_plan.server_ids()
    except uninstall_plan.Offline as exc:
        if run.resumed:
            raise Stop(EXIT_REFUSED, _offline_resumed(exc), Reason.OFFLINE, {"error": str(exc)}) from None
        raise Stop(EXIT_REFUSED, (
            f"probe uninstall: cannot reach Probe's server ({exc}), so this computer's sign-in could not be "
            "revoked. Nothing was changed. Try again when online, or run `probe uninstall --offline` to remove "
            "Probe from this computer only and revoke its keys yourself in the dashboard."),
            Reason.OFFLINE, {"error": str(exc)}) from None


def _take_lock(run: Run) -> None:
    from probe.shared.updates import handoff
    from probe.cli.install.uninstall import plan as uninstall_plan

    root = uninstall_plan.primary_versions_root()
    if handoff.holds(root):
        return  # this process holds it already (an installer finishing an uninstall)
    if handoff.fcntl is None:
        return  # Windows: no install lock exists there, for any installer
    try:
        fd = handoff.take_lock(root, wait_s=LOCK_WAIT_S)
    except OSError as exc:
        # Never on without it: an install could switch the CLI under this run.
        raise Stop(EXIT_REFUSED, f"probe uninstall: the install lock ({handoff.lock_path(root)}) cannot be taken "
                                 f"({exc}); nothing was changed. Fix that, then run it again.",
                   Reason.BUSY, {"error": str(exc)}) from None
    if fd is None:
        if run.resumed:
            raise Stop(EXIT_REFUSED, "probe uninstall: another Probe update or uninstall is running; try again "
                                     "when it ends.", Reason.BUSY)
        raise Stop(EXIT_REFUSED, "probe uninstall: another Probe update or uninstall is running; nothing was "
                                 "changed. Try again when it ends.", Reason.BUSY)
    run.lock_fd = fd


def _plan(run: Run, server: dict | None) -> None:
    from probe.cli.install.uninstall import plan as uninstall_plan
    from probe.core import events

    run.plan = uninstall_plan.compute(server=server)
    run.wrote_plan = True  # from here the folder holds this run's plan (a call-off takes it)
    uninstall_plan.write(run.plan)
    gens = len(run.plan.get("env_generations", []))
    agents = len(run.plan.get("agent_edits", []))
    _step(events.Step.UNINSTALL_PLAN, events.Status.DONE,
          f"{len(run.plan['paths'])} path(s), {gens} CLI env(s), {agents} coding agent(s)")
from probe.cli.install.uninstall.phases.server import _offline_resumed  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.state import Reason, Run, Stop, _step  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.telemetry import _telemetry_declined  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.uninstall import EXIT_REFUSED, run  # noqa: E402 -- pieces need each other; the front door loads this one first
