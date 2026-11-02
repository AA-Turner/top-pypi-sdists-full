"""`pi update` for Probe's pi package, one at a time per machine."""

from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass
# `update_report` is imported HERE, at the top, for the same reason updater.py
# imports its whole call graph eagerly (H8): it runs after `uv tool upgrade` has
# replaced the installed tree, when a first import would read the new files.
from probe.shared.updates import autoupdate
from probe.shared.updates import update_report
from probe.foundation.harness_registry import get_registry


@dataclass(frozen=True)
class _PiUpdate:
    """What the pi step did: its lines, and whether an ATTEMPTED update failed
    (skipped -- not installed, another update holding the lock -- is not a
    failure)."""

    lines: list[str]
    ok: bool = True
    detail: str = ""
    #: `pi update` actually ran (a skip did not).
    ran: bool = False
    #: For the server's update report only: which of the returns below this
    #: is, and the package versions either side of it.
    code: update_report.PiStep | None = None
    before: str | None = None
    after: str | None = None
    #: What open pi sessions need to run the new package, when they cannot
    #: switch by themselves ("" when they can, or nothing moved).
    action: str = ""


@contextmanager
def _pi_update_lock():
    """One `pi update` at a time on this machine: two runs on one clone (two
    Claude Code windows' auto-updates and a pi start) race git and npm. Yields
    whether this run holds it; without `fcntl` (Windows) it always does."""
    try:
        import fcntl
    except ImportError:
        yield True
        return
    from probe.sdk import session_marker

    try:
        path = session_marker.state_dir() / "pi-update.lock"
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = open(path, "a+")  # noqa: SIM115 - held across the yield
    except OSError:
        # A lock that cannot be opened is never worth failing the update over.
        yield True
        return
    with handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            yield False
            return
        try:
            yield True
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _update_pi_package() -> _PiUpdate:
    """`pi update` for Probe's pi package when pi has it installed; nothing
    otherwise. Says the versions it moved between, or how to do it by hand.

    It runs while pi does, as pi's own `pi update` does. It used to wait until
    no pi process was left, and a researcher running pi agents around the
    clock never got the package at all (strand-ai, 2026-10-15). A running pi
    keeps the extension and capture watcher it loaded: in real pi 1.0.0, with
    the package's `node_modules` deleted and then `pi update`d from 0.4.0 to
    0.5.0 under it, turns, `/probe-status`, `/probe-mcp-login` and the watcher
    process carried on, `/new` started a session, and `/reload` loaded 0.5.0
    (a running session's capture watcher keeps its old code until pi restarts).
    Killed mid-`npm install`, the orphaned npm still finished `node_modules`.
    Only a pi STARTED during the second or two in which `pi update` has removed
    `node_modules` fails to load the package, and exits 1."""
    from probe.shared.harness.harnesses import pi as pi_config

    directory = pi_config.installed_package_dir()
    if directory is None or not directory.is_dir():
        autoupdate.mark_pi_update_pending(False)
        return _PiUpdate([], code=update_report.PiStep.NOT_INSTALLED)
    with _pi_update_lock() as held:
        if not held:
            return _PiUpdate(
                ["pi package:", "  another update is updating it now"],
                code=update_report.PiStep.LOCKED,
            )
        before = pi_config.installed_package_version()
        # Owed until it is known to have worked: an updater killed mid-update
        # (it removes and reinstalls `node_modules`) is retried, not forgotten.
        autoupdate.mark_pi_update_pending(True)
        result = pi_config.update_package()
        after = pi_config.installed_package_version()

    def shown(version) -> str:
        return ".".join(str(part) for part in version) if version else "unknown"

    versions_seen = {
        "before": shown(before) if before else None,
        "after": shown(after) if after else None,
    }
    if not result.ok and not getattr(result, "reachable", True):
        # pi itself is gone (uninstalled, its settings still naming us): nothing
        # to update with, which is not an update that failed.
        autoupdate.mark_pi_update_pending(False)
        return _PiUpdate(
            ["pi package:", f"  not updated: {result.detail}"],
            code=update_report.PiStep.UNREACHABLE,
            **versions_seen,
        )
    # A failure stays owed, so pi's next session start tries again.
    autoupdate.mark_pi_update_pending(not result.ok)
    if not result.ok:
        return _PiUpdate(
            ["pi package:", f"  ! not updated ({result.detail}); run `pi update {pi_config.MIRROR_GIT_SOURCE}`"],
            ok=False,
            detail=f"pi package not updated: {result.detail}",
            ran=True,
            code=update_report.PiStep.FAILED,
            **versions_seen,
        )
    # The copy open sessions' shims switch to (kimi/pi update parity P1): made
    # from the clone `pi update` just finished; a package from before the shim
    # makes none.
    from probe.shared.harness.harnesses.pi import pins as pi_pins

    pinned = None
    try:
        pinned = pi_pins.pin_installed()
    except Exception:  # noqa: BLE001 -- no pin: open sessions keep what they run
        pinned = None
    if before != after:
        # One line: the attempt record (`update_owed_pi_package`) and the update
        # report read the last line as what happened.
        harness = _package_harness()
        binary = get_registry().get(harness).binary if harness else None
        follows = bool(pinned is not None and binary and pi_pins.sessions_follow((binary,)))
        if follows:
            follow = "open pi sessions switch to it at their next turn, no restart needed"
        else:
            follow = "run /reload in open pi sessions (or restart them) to apply"
        return _PiUpdate(
            ["pi package:", f"  updated {shown(before)} → {shown(after)} ({follow})"],
            ran=True, code=update_report.PiStep.UPDATED, **versions_seen,
            action="" if follows else "Run /reload in open pi sessions (or restart them) to apply the update.",
        )
    return _PiUpdate(
        ["pi package:", f"  already {shown(after)}"],
        ran=True, code=update_report.PiStep.CURRENT, **versions_seen,
    )
from probe.cli.install.upgrade.package_step import _package_harness  # noqa: E402 -- pieces need each other; the front door loads this one first
