"""Windows-specific process helpers.

The deferred-command trick: on Windows a running ``.exe`` shim is locked, so
neither ``uv tool uninstall`` nor ``uv tool upgrade`` can overwrite it from the
process that holds the lock. The fix is to spawn a detached ``cmd`` that waits
for our PID to disappear, then runs the real work once the handle is free.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

# Cap the polling loop so a wedged parent never leaves an orphan cmd spinning
# forever.
_MAX_POLLS = 60


def schedule_deferred_cmd(wait_pid: int, script_lines: list[str]) -> Path:
    """Write and launch a detached batch script that runs ``script_lines`` once
    the process ``wait_pid`` has exited, then removes its own scratch directory.

    The generated ``.cmd`` polls ``tasklist`` for ``wait_pid`` (at most
    ``_MAX_POLLS`` one-second iterations), waits a short grace period for the OS
    to release file handles, runs the caller's ``script_lines``, and finally
    deletes the temporary directory it lives in. Returns the path to that
    ``.cmd``.

    Windows only — the caller owns the ``os.name == "nt"`` guard. Propagates
    ``OSError`` when the detached launch fails.
    """
    work_dir = Path(tempfile.mkdtemp(prefix="pysae-deferred-"))
    bat = work_dir / "deferred.cmd"

    lines = [
        "@echo off",
        # UTF-8 codepage so paths with accented characters (e.g. RémiAlvergnat)
        # are interpreted correctly by cmd.
        "chcp 65001 >nul",
        "setlocal enabledelayedexpansion",
        "set /a tries=0",
        # Initial grace period — give the parent shell time to exit cleanly
        # before we start poking at the locked files.
        "timeout /t 3 /nobreak >nul",
        ":wait",
        f'tasklist /FI "PID eq {wait_pid}" 2>nul | find "{wait_pid}" >nul',
        "if errorlevel 1 goto :run",
        "set /a tries+=1",
        f"if !tries! geq {_MAX_POLLS} goto :run",
        "timeout /t 1 /nobreak >nul",
        "goto wait",
        ":run",
        # Extra grace so the OS releases file handles after the process exits.
        "timeout /t 1 /nobreak >nul",
        *script_lines,
        f'rmdir /s /q "{work_dir}" >nul 2>&1',
    ]
    script = "\r\n".join(lines) + "\r\n"
    bat.write_text(script, encoding="utf-8", newline="")

    # CREATE_NO_WINDOW gives the cmd a hidden console; child commands invoked
    # from inside the bat (tasklist, find, uv, rmdir …) inherit that hidden
    # console instead of getting a fresh visible one. With DETACHED_PROCESS the
    # cmd would have *no* console, so Windows would spawn a new visible console
    # for every console-app subcommand — the polling loop alone would flash
    # dozens of cmd windows. CREATE_NEW_PROCESS_GROUP keeps the child alive
    # across a Ctrl-C in the parent shell. stdio is routed to DEVNULL so the
    # child can't latch onto the parent's handles.
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        creationflags = 0
    subprocess.Popen(
        ["cmd", "/c", str(bat)],
        creationflags=creationflags,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
    )
    return bat
