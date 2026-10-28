"""The uninstall barrier, as every installer reads it (plan clean-uninstall-reinstall, Build contract).

`probe uninstall` writes `S/uninstall/barrier.json` (S = `probe.service.paths.state_dir()`,
`~/.local/state/probe`, never moved by XDG) before it stops or removes anything,
atomically (a temporary file, fsync, rename). The uninstall takes
`<versions root>/install.lock` before it writes the barrier, and holds it to
the end:

    {"v": 1, "pid", "start" (`probe.service.procid` start time), "at",
     "plan": "S/uninstall/plan.json",
     "phase": "planned|stopping|draining|server|integrations|state|finishing",
     "host" (`socket.gethostname()`), "machine_key" (`probe.service.paths`)}

    An owner on ANOTHER machine (a shared home: its `machine_key` differs from
    this one's; `host` only for a record without a key) counts as running: its
    pid means nothing here, so it is never cleared, resumed or finished from
    this machine.

    LIVE   its owner (pid + start) still runs, OR its phase is anything but
           "planned", "stopping" or "draining" (an unknown or missing phase
           included): past those the job must be finished, never undone. A
           file that cannot be read or parsed is LIVE while its mtime is
           younger than UNREADABLE_LIVE_S (60 min), STALE after.
    STALE  its owner is gone and its phase is "planned", "stopping" or
           "draining": an install, `probe repair` or `probe uninstall` may
           clear it (logged)

While it is LIVE, nothing installs over it. The install entries a person runs
(`npx probe-research`, the wizard's install and update, `probe repair`, `probe
daemon install`) FINISH an uninstall whose owner is gone first, the way `probe
uninstall` resumes it (`probe.cli.install_pipeline.gate`), then install afresh;
one whose owner runs, or that they cannot finish, they refuse with one clear
line (`refusal`). Everything else refuses while it is LIVE: every other wizard
action, `npx probe-research backfill`, `probe service start`, the updater, and
the side-by-side install and switch (`probe._shared.installs`, which the
update, the hand-off's adopt and the guard's switch back all go through).

This module only READS the barrier and clears a stale one. Its writer is the
uninstall's (lane U); the two meet only in the file's shape above, so this
reader must stay byte-compatible with it. Stdlib only (the service and the
installs module import it); `probe.service` is imported lazily, for the state
folder and the process identity.
"""

from __future__ import annotations

import contextlib
import json
import os
import time
from pathlib import Path

DIRNAME = "uninstall"
NAME = "barrier.json"
SCHEMA = 1
#: In the order an uninstall goes through them.
PHASES = ("planned", "stopping", "draining", "server", "integrations", "state", "finishing")
#: The only phases a barrier whose owner is gone may be cleared at: nothing
#: irreversible has happened yet. Any other phase, an unknown or a missing one
#: included, is LIVE whoever wrote it.
REVERSIBLE = ("planned", "stopping", "draining")
#: The first phase past REVERSIBLE: the server was told.
NO_RETURN = "server"
#: A barrier file that cannot be read or parsed is LIVE this long after its
#: mtime (its writer renames a complete file into place: a torn one is not its).
UNREADABLE_LIVE_S = 60 * 60
#: `read`'s mark on a file it could not read or parse, with that file's mtime.
_UNREADABLE = "_unreadable"
#: The uninstall's stdlib finisher, copied beside the barrier at its "finishing" phase.
_FINISHER = "finisher.py"


class State:
    ABSENT = "absent"
    LIVE = "live"
    STALE = "stale"


class UninstallRunning(RuntimeError):
    """An uninstall is running, or must be finished first: nothing installs now."""


def path() -> Path:
    """`~/.local/state/probe/uninstall/barrier.json` (`paths.state_dir()`'s rule)."""
    try:
        from probe.service import paths

        state = paths.state_dir()
    except Exception:  # noqa: BLE001 -- the same rule, spelled out
        state = Path.home() / ".local" / "state" / "probe"
    return state / DIRNAME / NAME


def _unreadable(target: Path) -> dict:
    try:
        mtime = target.stat().st_mtime
    except OSError:
        mtime = None
    return {_UNREADABLE: True, "mtime": mtime}


def read(at: Path | None = None) -> dict | None:
    """The barrier's record; None when there is none. A file that cannot be
    read or parsed reads as `{"_unreadable": True, "mtime": <its mtime>}`."""
    target = at or path()
    try:
        raw = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except OSError:
        return _unreadable(target)
    try:
        data = json.loads(raw)
    except ValueError:
        return _unreadable(target)
    return data if isinstance(data, dict) else _unreadable(target)


def _other_machine(data: dict) -> bool:
    """Was it written on another machine sharing this home? Its `machine_key`
    against this machine's (a hostname changes with the network on macOS: never
    the test while there is a key); its `host` only for a record with no key.
    Where this machine's key cannot be read (the tap's copy, without
    `probe.service`), no machine rule applies: the pid check decides."""
    try:
        from probe.service import paths

        mine = paths.machine_key()
    except Exception:  # noqa: BLE001
        return False
    key = data.get("machine_key")
    if isinstance(key, str) and key:
        return key != mine
    host = data.get("host")
    if isinstance(host, str) and host:
        import socket

        try:
            return host != socket.gethostname()
        except OSError:
            return False
    return False


def _owner_runs(data: dict) -> bool:
    """Does the process that wrote it still run (pid AND start time)? An
    owner on another machine (`_other_machine`) does, as far as this one can
    tell. Unknown reads as yes: never cleared on a guess."""
    if _other_machine(data):
        return True
    pid, start = data.get("pid"), data.get("start")
    if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 1:
        return False
    if not isinstance(start, str) or not start:
        # No start time to tell a reused pid by: the pid alone.
        try:
            from probe.service import procid

            return procid.exists(pid)
        except Exception:  # noqa: BLE001
            return True
    try:
        from probe.service import procid

        alive = procid.alive(pid, start)
    except Exception:  # noqa: BLE001
        return True
    return alive is not False


def _past_no_return(data: dict) -> bool:
    """Is its phase anything but a reversible one (an unknown or missing phase
    included)?"""
    return data.get("phase") not in REVERSIBLE


def state(data: dict | None = None, *, at: Path | None = None) -> str:
    """`State.ABSENT`, `State.LIVE` or `State.STALE` (see the module docstring).
    A record of another schema is LIVE."""
    if data is None:
        data = read(at)
    if data is None:
        return State.ABSENT
    if data.get(_UNREADABLE):
        mtime = data.get("mtime")
        if not isinstance(mtime, (int, float)) or time.time() - mtime < UNREADABLE_LIVE_S:
            return State.LIVE
        return State.STALE
    if data.get("v") != SCHEMA:
        return State.LIVE
    if _owner_runs(data) or _past_no_return(data):
        return State.LIVE
    return State.STALE


def live(*, at: Path | None = None) -> bool:
    return state(at=at) == State.LIVE


def refusal(data: dict | None = None, *, at: Path | None = None) -> str | None:
    """The one line an installer prints when it refuses, or None when nothing
    stops it (no barrier, or a stale one)."""
    if data is None:
        data = read(at)
    if state(data) != State.LIVE:
        return None
    if data.get(_UNREADABLE):
        return (f"an uninstall of Probe is in progress ({at or path()} cannot be read yet); finish it with "
                "`probe uninstall`, then install again")
    phase = data.get("phase")
    if _past_no_return(data) and not _owner_runs(data):
        step = f"at its '{phase}' step" if isinstance(phase, str) and phase else "past its point of no return"
        how = "run `probe uninstall`"
        # The finisher is copied in only at "finishing": named only when it is there.
        finisher = (at or path()).parent / _FINISHER
        if finisher.is_file():
            plan = data.get("plan")
            if not isinstance(plan, str) or not plan:
                plan = str(finisher.parent / "plan.json")
            how += f" (or, without the CLI, `python3 {finisher} --plan {plan}`)"
        return f"an uninstall of Probe stopped {step} and must be finished first: {how}, then install again"
    owner = data.get("pid")
    if isinstance(owner, int) and _owner_runs(data):
        return (f"an uninstall of Probe is running (pid {owner}); nothing is installed while it does. "
                "Wait for it to finish, then install again")
    return f"an uninstall of Probe is in progress ({at or path()}); finish it with `probe uninstall`, then install again"


def check() -> None:
    """Raise UninstallRunning when the barrier is LIVE."""
    said = refusal()
    if said:
        raise UninstallRunning(said)


def clear_stale(*, at: Path | None = None) -> str | None:
    """Remove a STALE barrier (only the barrier: the plan beside it is the
    uninstall's, which a later `probe uninstall` writes afresh). Returns the
    line to log when it did, else None. Never raises."""
    target = at or path()
    data = read(target)
    if data is None or state(data) != State.STALE:
        return None
    # Read again right before the unlink, with nothing (no process lookup) in
    # between: a new uninstall may have written its own barrier since. Callers
    # hold the install lock, which an uninstall takes before it writes the
    # barrier, so the same record now is the record judged STALE above.
    again = read(target)
    if again != data:
        return None
    try:
        target.unlink()
    except FileNotFoundError:
        return None
    except OSError as exc:
        return f"could not clear a stale uninstall barrier ({target}): {exc}"
    with contextlib.suppress(OSError):
        os.rmdir(target.parent)  # only when nothing else is in it
    if data.get(_UNREADABLE):
        return f"cleared a stale uninstall barrier ({target}: unreadable, untouched for over an hour)"
    return (f"cleared a stale uninstall barrier (its uninstall, pid {data.get('pid')}, stopped at "
            f"'{data.get('phase')}' before reaching the server)")
