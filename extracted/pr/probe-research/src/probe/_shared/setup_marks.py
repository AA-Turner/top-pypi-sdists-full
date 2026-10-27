"""Who holds `wizard.lock`, and which `probe wizard` menu waits on a person (plan C1).

Two small JSON records, `{"pid", "start", "at"}` (`KEYS`: the process, its
kernel start time from `probe.service.procid`, and since when), beside the
lock in the state folder:

    wizard.lock   written into the lock file by whoever takes the lock
                  (`probe.cli.wizard_lock.held`), cleared as it lets go. The
                  Probe service reads how long a setup has held the device
                  from it, and updates past one held for DEFER_LIMIT_S.
    wizard.menu.<pid>
                  one per interactive menu (two open terminals are two menus),
                  written by it before it lets go of the lock to wait on a
                  person, removed when that wizard exits. The menu's process
                  still runs from the CLI's files, so an update that would move
                  them (in place, or the first side-by-side switch) waits for
                  every waiting menu, as for the lock, at most DEFER_LIMIT_S; a
                  side-by-side switch leaves those files where they are and
                  goes on. A menu's own Update passes only its own marker.

A record is its writer's only while that exact process (pid AND start time)
still runs: a holder killed with SIGKILL leaves its record behind, and a reused
pid names another process. One whose start time cannot be read here is
`UNKNOWN`: its process exists, its record may not be its own.

Stdlib only: the Probe service reads these (plan S1), and `probe.cli` must not
be imported there.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

# At import, not in the calls: an update in place replaces these files before
# the updater's last read of a record (updater.py's H8).
from probe.service import procid

LOCK_FILENAME = "wizard.lock"
#: A menu's marker is `MENU_PREFIX + <its pid>`.
MENU_PREFIX = "wizard.menu."
#: A record's keys: its process, that process's kernel start time, and since when.
KEYS = ("pid", "start", "at")

#: `holder`'s answers.
ALIVE = "alive"
GONE = "gone"
UNKNOWN = "unknown"

_own_start: str | None = None


def own_record() -> dict:
    """This process's record, dated now."""
    global _own_start
    if _own_start is None:
        try:
            _own_start = procid.start_time(os.getpid()) or ""
        except Exception:  # noqa: BLE001 -- a record without it reads as UNKNOWN
            _own_start = ""
    pid_key, start_key, at_key = KEYS
    return {pid_key: os.getpid(), start_key: _own_start, at_key: time.time()}


def holder(path: Path) -> tuple[str, float | None, int | None]:
    """`(state, at, pid)` of the record at `path`: ALIVE (its writer still runs:
    `at` is when it wrote it), GONE (no record, an unreadable one, or its
    writer is gone), or UNKNOWN (its pid runs, its start time cannot be told
    here). `at` is None unless ALIVE; a record dated ahead of the clock is
    UNKNOWN."""
    pid_key, start_key, at_key = KEYS
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
        pid, start, at = record[pid_key], record[start_key], record[at_key]
    except (OSError, ValueError, TypeError, KeyError):
        return GONE, None, None
    if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 1:
        return GONE, None, None
    try:
        alive = procid.alive(pid, start) if isinstance(start, str) and start else None
        if alive is None and not procid.exists(pid):
            alive = False
    except Exception:  # noqa: BLE001 -- cannot be told
        alive = None
    if alive is False:
        return GONE, None, pid
    if alive is None or isinstance(at, bool) or not isinstance(at, (int, float)) or at > time.time():
        return UNKNOWN, None, pid
    return ALIVE, float(at), pid


def menu_path(state_dir: Path, pid: int | None = None) -> Path:
    """The marker of the menu in process `pid` (default: this one)."""
    return state_dir / f"{MENU_PREFIX}{os.getpid() if pid is None else pid}"


def _markers(state_dir: Path) -> list[Path]:
    try:
        return [p for p in state_dir.glob(f"{MENU_PREFIX}*") if p.name[len(MENU_PREFIX):].isdigit()]
    except OSError:
        return []


def menu_waiting(state_dir: Path, *, exclude_pid: int | None = None) -> tuple[bool, float | None]:
    """Does a `probe wizard` menu wait on a person (a marker whose process
    still runs, or cannot be told gone), and since when: the latest of them,
    as every one must be past a limit? A marker whose process cannot be told
    is dated by the file itself, so it too counts a day at most; None only
    when not even that reads. The menu of `exclude_pid` (this process's own,
    for its own Update) is not one; every other is."""
    waiting, times = False, []
    for path in _markers(state_dir):
        state, at, pid = holder(path)
        if state == GONE or (exclude_pid is not None and exclude_pid in (pid, int(path.name[len(MENU_PREFIX):]))):
            continue
        if at is None:
            try:
                at = path.stat().st_mtime
            except OSError:
                at = None
        waiting = True
        times.append(at)
    if not waiting:
        return False, None
    return True, None if None in times else max(times)


def mark_menu(state_dir: Path) -> None:
    """This process's menu waits on a person from now: say so in its own
    marker (`menu_waiting`), and clear the markers of menus that are gone.
    Fail-soft."""
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        path = menu_path(state_dir)
        tmp = state_dir / f".{path.name}.tmp"
        tmp.write_text(json.dumps(own_record()), encoding="utf-8")
        os.replace(tmp, path)
    except OSError:
        return
    for other in _markers(state_dir):
        if other != path and holder(other)[0] == GONE:
            try:
                other.unlink()
            except OSError:
                pass


def unmark_menu(state_dir: Path) -> None:
    """This process's wizard exits: its menu marker goes."""
    try:
        menu_path(state_dir).unlink()
    except OSError:
        pass
