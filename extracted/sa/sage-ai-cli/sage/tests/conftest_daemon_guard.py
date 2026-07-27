"""Stale-daemon reaper + hard teardown for the session-scoped backend fixture.

WHY THIS EXISTS
---------------
`sage/tests/conftest.py` starts a real uvicorn backend and a
`native_call_handler.py` daemon in a session-scoped autouse fixture. Its
teardown after the `yield` is correct -- terminate, wait, kill on timeout.

But that teardown only runs when pytest exits CLEANLY. If the run is SIGKILLed,
a worker crashes, the terminal closes, or CI cancels the job, the generator
never resumes past the `yield` and both children are orphaned.

On this machine that produced 15 leaked daemons, the oldest alive for 3 days
22 hours. They are not harmless: each holds a port and memory, and one was
observed asynchronously `pip install`ing an older pytest into the host
environment mid-run, breaking pytest-asyncio and making results unreliable.

FIX
---
Two independent layers, because the failure mode is specifically "the clean
path did not run":

1. `reap_stale_daemons()` -- called at fixture SETUP. Kills leftovers from
   previous runs before starting new ones. This is what makes the system
   self-healing after an unclean exit: the *next* run cleans up the *previous*
   run's mess.

2. `register_hard_teardown()` -- installs `atexit` and SIGTERM/SIGINT handlers
   so the children die on the paths pytest's own teardown misses. It cannot
   cover SIGKILL (nothing can), which is exactly why layer 1 is required.

Deliberately does NOT use psutil -- that is not a declared dependency, and a
test-infrastructure guard must not itself introduce an import that can fail.

PORTABILITY NOTE (this bit was a real bug, caught by testing the guard itself)
-----------------------------------------------------------------------------
The first version asked `ps` for `etimes` (elapsed seconds). That is a
procps/Linux keyword. macOS BSD `ps` rejects it outright --

    $ ps -Ao pid=,etimes=,command=
    ps: etimes: keyword not found

-- and the reaper silently matched nothing while daemons were plainly running.
So we now try `etimes` first and fall back to BSD `etime`, whose format is
`[[DD-]HH:]MM:SS` and must be parsed. Both paths are exercised by
`_parse_etime`'s unit tests.
"""

from __future__ import annotations

import atexit
import os
import re
import signal
import subprocess
import sys
from typing import Iterable

# Command-line fragments identifying a daemon started by this fixture.
# Kept narrow on purpose: a broader match risks killing a developer's own server.
_DAEMON_PATTERNS = (
    r"-m uvicorn backend\.app:app",
    r"native_call_handler\.py",
)

_MIN_AGE_SECONDS = 120  # never touch something a concurrent run just started


def _parse_etime(value: str) -> int | None:
    """Parse elapsed time into seconds.

    Accepts either a bare seconds count (Linux `etimes`) or BSD/macOS `etime`
    in `[[DD-]HH:]MM:SS` form. Returns None if unparseable, so a surprising
    format makes us skip the process rather than mis-age it and kill something
    that is only seconds old.

    >>> _parse_etime("42")
    42
    >>> _parse_etime("01:30")
    90
    >>> _parse_etime("01:00:00")
    3600
    >>> _parse_etime("3-04:45:49")
    276349
    """
    value = value.strip()
    if not value:
        return None
    if value.isdigit():
        return int(value)

    days = 0
    if "-" in value:
        day_part, _, value = value.partition("-")
        if not day_part.isdigit():
            return None
        days = int(day_part)

    parts = value.split(":")
    if not all(p.isdigit() for p in parts) or not 1 <= len(parts) <= 3:
        return None
    parts = [int(p) for p in parts]
    while len(parts) < 3:
        parts.insert(0, 0)
    hours, minutes, seconds = parts
    return days * 86400 + hours * 3600 + minutes * 60 + seconds


def _ps_lines() -> list[str]:
    """Return `ps` output as `pid etime command`, trying Linux then BSD keywords."""
    for keyword in ("etimes", "etime"):
        try:
            res = subprocess.run(
                ["ps", "-Ao", f"pid=,ppid=,{keyword}=,command="],
                capture_output=True, text=True, timeout=10,
            )
        except Exception:
            return []
        # BSD ps writes "ps: etimes: keyword not found" to stderr AND still
        # exits 0 while emitting the remaining columns, so checking returncode
        # alone is not enough -- inspect stderr too.
        if "keyword not found" in (res.stderr or ""):
            continue
        if res.stdout:
            return res.stdout.splitlines()
    return []


def _iter_candidate_pids() -> Iterable[tuple[int, int, str]]:
    """Yield (pid, ppid, age_seconds, command) for processes matching our daemons."""
    me = os.getpid()
    for line in _ps_lines():
        parts = line.strip().split(None, 3)
        if len(parts) < 4:
            continue
        pid_s, ppid_s, etime_s, cmd = parts
        if not (pid_s.isdigit() and ppid_s.isdigit()):
            continue
        pid, ppid = int(pid_s), int(ppid_s)
        age = _parse_etime(etime_s)
        if age is None or pid == me:
            continue
        if any(re.search(p, cmd) for p in _DAEMON_PATTERNS):
            yield pid, ppid, age, cmd


def reap_stale_daemons(min_age_seconds: int = _MIN_AGE_SECONDS) -> list[int]:
    """Kill daemons left behind by a previous, uncleanly-terminated run.

    Only processes older than `min_age_seconds` are touched, so a concurrently
    starting run is never killed. Returns the pids reaped.
    """
    reaped: list[int] = []
    for pid, ppid, age, _cmd in _iter_candidate_pids():
        # ORPHANED is the precise definition of "leaked": the pytest session that
        # spawned this daemon is gone, so init/launchd (pid 1) adopted it. Age
        # alone is the wrong signal -- a legitimately long-running concurrent
        # test session has old daemons too, and reaping those would have one run
        # silently kill another run's backend.
        if ppid != 1:
            continue
        if age < min_age_seconds:
            continue
        try:
            os.kill(pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            continue
        except Exception:
            continue
        reaped.append(pid)

    if reaped:
        # Give SIGTERM a moment, then SIGKILL whatever ignored it.
        import time as _time
        _time.sleep(0.5)
        for pid in reaped:
            try:
                os.kill(pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
            except Exception:
                pass
        print(
            f"[conftest] reaped {len(reaped)} stale backend daemon(s) left by a "
            f"previous run: {reaped}",
            file=sys.stderr,
        )
    return reaped


def register_hard_teardown(*procs: subprocess.Popen) -> None:
    """Kill `procs` on interpreter exit and on SIGTERM/SIGINT.

    Complements -- does not replace -- the fixture's post-yield teardown, which
    remains the normal path. This covers abrupt exits where the generator never
    resumes. SIGKILL is uncatchable by design; `reap_stale_daemons()` on the
    next run is the backstop for that case.
    """
    live = [p for p in procs if p is not None]

    def _kill_all() -> None:
        for p in live:
            if p.poll() is not None:
                continue
            try:
                p.terminate()
                p.wait(timeout=3)
            except subprocess.TimeoutExpired:
                try:
                    p.kill()
                    p.wait(timeout=3)
                except Exception:
                    pass
            except Exception:
                pass

    atexit.register(_kill_all)

    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            previous = signal.getsignal(sig)

            def _handler(signum, frame, _prev=previous):
                _kill_all()
                if callable(_prev):
                    _prev(signum, frame)
                else:
                    signal.signal(signum, signal.SIG_DFL)
                    os.kill(os.getpid(), signum)

            signal.signal(sig, _handler)
        except (ValueError, OSError):
            # Not on the main thread (e.g. under xdist workers) -- atexit still applies.
            pass
