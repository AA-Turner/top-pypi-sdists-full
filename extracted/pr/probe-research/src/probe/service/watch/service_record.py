"""the service's own record: how the service before this one ended (crash, kill, reboot), and this one's crash."""

from __future__ import annotations
import contextlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from ...foundation.service_api import paths
from probe.service.watch.bounds import MAX_TRACEBACK
from probe.service.watch.files import read_json, write_json
from probe.service.watch.keeper import WINDOWS
MAX_ONCE = 256
#: The service's record of itself (`last_run`), and of a crash (`record_crash`).
RUN_NAME = "service.run"
LAST_CRASH_NAME = "last-crash.json"
#: Two boot readings within this many seconds are one boot (Windows: from the uptime).
BOOT_SLACK_S = 120.0


# -- the service's own record ---------------------------------------------------


def previous_holder() -> tuple[int, str] | None:
    """`(pid, start)` the lock file names (`server._name_holder`): the service
    before this one. Read BEFORE this one names itself there. Never raises."""
    try:
        text = paths.lock_path().read_text(encoding="utf-8")
    except (OSError, ValueError):
        return None
    pid_s, _, start = text.strip().partition(" ")
    try:
        pid = int(pid_s)
    except ValueError:
        return None
    return (pid, start.strip()) if pid > 1 else None


def boot_id() -> str | None:
    """This boot's id: Linux's `boot_id`, macOS's `kern.boottime`, Windows' boot
    time from the uptime (best effort). None when unknown. Never raises."""
    try:
        if sys.platform.startswith("linux"):
            return Path("/proc/sys/kernel/random/boot_id").read_text(encoding="utf-8").strip() or None
        if sys.platform == "darwin":
            out = subprocess.run(  # noqa: S603 -- a fixed system binary, no shell
                ["/usr/sbin/sysctl", "-n", "kern.boottime"], capture_output=True, text=True, timeout=2, check=False,
            ).stdout
            found = re.search(r"sec\s*=\s*(\d+)", out)
            return f"boottime:{found.group(1)}" if found else None
        if os.name == "nt":
            import ctypes

            tick = ctypes.windll.kernel32.GetTickCount64  # type: ignore[attr-defined]
            tick.restype = ctypes.c_ulonglong
            return f"boottime:{round(time.time() - tick() / 1000.0)}"
    except Exception:  # noqa: BLE001 -- unknown: never called a reboot
        return None
    return None


def same_boot(a: object, b: object) -> bool | None:
    """Do two `boot_id` readings name one boot? None when either is unknown."""
    if not isinstance(a, str) or not isinstance(b, str) or not a or not b:
        return None
    if a.startswith("boottime:") and b.startswith("boottime:"):
        try:
            return abs(float(a[9:]) - float(b[9:])) <= BOOT_SLACK_S
        except ValueError:
            return a == b
    return a == b


def _same_process(pid: object, start: object, other_pid: object, other_start: object) -> bool:
    if not isinstance(pid, int) or pid != other_pid:
        return False
    if start and other_start:
        return str(start) == str(other_start)
    return True


def last_run(previous: tuple[int, str] | None, version: str) -> dict | None:
    """At start, holding the lock: how the service before this one ended, when
    that was a crash -- `{"reason": "crashed" | "unclean_exit", ...facts}` for
    `service_crash` -- else None. Then this one's own record, `service.run`
    (0600: pid, start, boot, version). A crash: `last-crash.json` names it
    (written on the way out, with its traceback), or (not on Windows: WINDOWS)
    it left no stop record (`last-stop.json`, written by every deliberate stop)
    and the boot is the same (a reboot or a shutdown's kill is not a crash; an
    unknown boot is never called a reboot). Never raises."""
    try:
        return _last_run(previous, version)
    except Exception:  # noqa: BLE001 -- the service starts whatever its record says
        return None


def _last_run(previous: tuple[int, str] | None, version: str) -> dict | None:
    from .. import guard
    from ...foundation.service_api import procid

    folder = paths.service_dir()
    run = read_json(folder / RUN_NAME)
    run = run if isinstance(run, dict) else {}
    stop = guard.last_stop() or {}
    crash = read_json(folder / LAST_CRASH_NAME)
    crash = crash if isinstance(crash, dict) else {}
    boot = boot_id()
    own = procid.start_time(os.getpid())
    write_json(folder / RUN_NAME, {"pid": os.getpid(), "start": own, "boot": boot, "version": version, "at": time.time()})
    if previous is None and isinstance(run.get("pid"), int):
        previous = (run["pid"], str(run.get("start") or ""))
    if previous is None:
        return None
    pid, start = previous
    if _same_process(pid, start, os.getpid(), own):
        return None
    prior = run if _same_process(run.get("pid"), run.get("start"), pid, start) else {}
    facts = {
        "previous": {"version": prior.get("version"), "started_at": prior.get("at")},
        "last_stop": {k: stop.get(k) for k in ("reason", "version", "at")} if stop else None,
    }
    if _same_process(crash.get("pid"), crash.get("start"), pid, start):
        with contextlib.suppress(OSError):
            (folder / LAST_CRASH_NAME).unlink()
        return {"reason": "crashed", **facts, "error": crash.get("error"), "traceback": crash.get("traceback"),
                "crashed_at": crash.get("at")}
    if WINDOWS:
        return None  # a logoff ends it with no stop record: that says nothing there
    if stop and _same_process(stop.get("pid"), stop.get("start"), pid, start):
        return None
    if same_boot(prior.get("boot"), boot) is False:
        return None  # a reboot (or the shutdown's kill): no crash
    return {"reason": "unclean_exit", **facts, "boot_known": same_boot(prior.get("boot"), boot) is not None}


def record_crash(error: str, text: str) -> None:
    """The service is exiting on an exception (`run_service`): what the next
    one reports (`last_run`). Never raises."""
    try:
        from ...foundation.service_api import procid

        start = procid.start_time(os.getpid())
    except Exception:  # noqa: BLE001
        start = None
    write_json(paths.service_dir() / LAST_CRASH_NAME, {
        "pid": os.getpid(), "start": start, "error": str(error)[:500], "traceback": (text or "")[-MAX_TRACEBACK:],
        "at": time.time(),
    })
