"""One `probe wizard` that changes this device at a time.

The terminal wizard and the desktop app are two front ends over ONE Probe
install: the same config file, the same agents' settings and instruction files.
Two runs at once would interleave their writes to all of them, and most of
those files have no lock of their own. So every wizard action that changes the
device holds this lock for the whole run, and a second one leaves with
`BUSY_EXIT_CODE` after `CONTENTION_GRACE_S` instead of waiting for it (a
terminal menu can stay open for hours). A desktop workspace save opts into
a longer, bounded wait so a post-install update can finish first.

An OS advisory lock (`flock`) on a file that is never deleted: the kernel
releases it the moment its holder exits, however it exits, so a run killed with
SIGKILL leaves nothing to clean up and there is no pid to judge stale.

A holder writes into the file who it is and since when (`{"pid", "start",
"at"}`, `probe._shared.setup_marks`), and clears it as it lets go: the Probe
service reads it to tell how long a setup has held the device, and updates
past one held for a day (plan C1, `probe.service.updater.LIMITED`). The
interactive menu lets go of the lock while it waits on a person, and says so
in a marker of its own instead (`setup_marks.MENU_PREFIX`,
`main._wizard_session`).

The other ways in to the same writes hold it too: `probe login`, `probe
logout`, `probe update`, and the auto-updater (`upgrading.perform_update`,
once it has waited out the process that spawned it). An update turned away is
recorded as a skip, which `probe doctor` shows.
"""

from __future__ import annotations

import json
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from probe._shared import setup_marks

LOCK_FILENAME = setup_marks.LOCK_FILENAME
#: EX_TEMPFAIL: try again later. Distinct from 1 (failed) and 2 (usage).
BUSY_EXIT_CODE = 75
BUSY_MESSAGE = "another Probe setup is running"
#: How long a run waits out contention before calling it busy. A real holder
#: keeps the lock for its whole run, seconds at least; `running()` (`probe
#: status`, which the desktop app calls on every focus) holds it for
#: microseconds, and must never be what turns a terminal wizard away.
CONTENTION_GRACE_S = 0.25
_RETRY_EVERY_S = 0.01


class Busy(Exception):
    """Another wizard run holds the lock."""


#: This process's open lock file while it holds the lock. Re-entrant within the
#: process: a holder that reaches another entry point (the wizard's Update
#: action runs `perform_update`, which takes the lock too) must not be turned
#: away by itself -- two `flock`s from one process on two open files conflict.
_held = None


def lock_path() -> Path:
    from probe.sdk import session_marker

    return session_marker.state_dir() / LOCK_FILENAME


@contextmanager
def held(*, wait_s: float | None = None) -> Iterator[None]:
    """Hold the lock for the block, or raise `Busy` once another holder has
    kept it for `CONTENTION_GRACE_S`, or the caller's explicit `wait_s`
    (a `running()` probe holds it for an instant; a real run, for the whole run).

    Fail-open on anything but contention: a state folder that cannot be
    written, or a filesystem without locks, runs unlocked as every run did
    before this lock existed, rather than refusing to set Probe up at all.
    Re-entrant: inside a block this process already holds, it holds nothing
    more, and the outer block releases the lock.
    """
    from probe._shared import oscompat

    global _held
    if _held is not None and not _held.closed:
        yield
        return
    handle = None
    try:
        path = lock_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = open(path, "a+")  # noqa: SIM115 - held for the block, closed below
        deadline = time.monotonic() + (CONTENTION_GRACE_S if wait_s is None else wait_s)
        while True:
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(_RETRY_EVERY_S)
    except BlockingIOError:
        if handle is not None:
            handle.close()
        raise Busy(BUSY_MESSAGE) from None
    except OSError:
        if handle is not None:
            handle.close()
        handle = None
    _held = handle  # cleared by the close below: a closed handle holds nothing
    if handle is not None:
        _write_holder(handle, setup_marks.own_record())
    try:
        yield
    finally:
        if handle is not None:
            # Cleared before letting go: a holder from before the record that
            # takes the lock next must not inherit this one's date.
            _write_holder(handle, None)
            handle.close()  # releases the lock


def _write_holder(handle, record: dict | None) -> None:
    """Say in the lock file who holds it and since when (`setup_marks`), over
    whatever the last holder wrote; or nothing, as the holder lets go.
    Fail-soft: a record that cannot be written only means the service cannot
    tell how long this hold has lasted, and measures it by its own deferrals."""
    try:
        handle.truncate(0)  # opened "a+": what follows is written at 0
        if record is not None:
            handle.write(json.dumps(record))
        handle.flush()
    except (OSError, ValueError):
        pass


def running() -> bool | None:
    """Whether a wizard run holds the lock right now: True, False, or None when
    it cannot be told (the probe failed for any reason but contention).

    A non-blocking SHARED `flock` on the existing file, released at once:
    shared, so two probes at once (the desktop app's, a second `probe status`)
    never see each other as a setup -- only a run's exclusive lock conflicts
    with it. Nothing is created, so a status read on a device no wizard ever
    ran on writes nothing. A file opened read-only can carry an `flock`, so this
    needs no write access.
    """
    from probe._shared import oscompat

    try:
        handle = open(lock_path(), "rb")  # noqa: SIM115 - closed below
    except FileNotFoundError:
        return False
    except OSError:
        return None
    try:
        oscompat.flock(handle.fileno(), oscompat.LOCK_SH | oscompat.LOCK_NB)
    except BlockingIOError:
        return True
    except OSError:
        return None
    else:
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
        except OSError:
            pass
        return False
    finally:
        handle.close()
