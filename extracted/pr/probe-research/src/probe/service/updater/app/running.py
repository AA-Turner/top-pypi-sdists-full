"""is the app running: processes by their executable's current path, and the app's instance lock."""

from __future__ import annotations
import contextlib
import os
import subprocess
import sys
from pathlib import Path
from probe.service.updater.app.bundle_check import BUNDLE_ID
from probe.service.updater.app.errors import InstallError
from probe.service.updater.app.manifest import supported
#: The app's instance lock (prbe-ai/desktop `background_update.rs` INSTANCE_LOCK,
#: in Tauri's `app_data_dir()`: `~/Library/Application Support/<identifier>`).
#: Every app process holds it (flock) for its life.
INSTANCE_LOCK = Path("Library") / "Application Support" / BUNDLE_ID / "instance.lock"


# -- is the app running? -----------------------------------------------------------


_LIBSYSTEM: list = []


def _libsystem():
    """macOS libSystem (proc_pidpath, renamex_np), loaded once."""
    if not _LIBSYSTEM:
        import ctypes

        _LIBSYSTEM.append(ctypes.CDLL("/usr/lib/libSystem.B.dylib", use_errno=True))
    return _LIBSYSTEM[0]


def _darwin_exe_path(pid: int) -> str | None:
    """`proc_pidpath`: where pid's executable is NOW (it follows a rename)."""
    try:
        import ctypes

        buffer = ctypes.create_string_buffer(4096)
        size = _libsystem().proc_pidpath(ctypes.c_int(pid), buffer, ctypes.c_uint32(4096))
    except (OSError, AttributeError):
        return None
    if size <= 0:
        return None
    return buffer.raw[:size].decode("utf-8", "surrogateescape")


def processes() -> list[tuple[int, str]]:
    """`(pid, executable path)` of every process this user can see, as exact as
    the system says: Linux `/proc/<pid>/exe` (follows renames), macOS `ps`'s
    `comm` (every user's; the path it started from) and `proc_pidpath` where it
    answers (the path it runs from now). One process may be listed twice."""
    found: list[tuple[int, str]] = []
    if sys.platform.startswith("linux"):
        with contextlib.suppress(OSError):
            for entry in os.scandir("/proc"):
                if entry.name.isdigit():
                    with contextlib.suppress(OSError):
                        found.append((int(entry.name), os.readlink(f"/proc/{entry.name}/exe")))
        return found
    try:
        done = subprocess.run(
            ["/bin/ps", "-axww", "-o", "pid=,comm="], capture_output=True, text=True, timeout=15,
            stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise InstallError(f"ps could not run: {exc}") from exc
    for line in done.stdout.splitlines():
        pid, _, path = line.strip().partition(" ")
        if pid.isdigit():
            found.append((int(pid), path.strip()))
            if supported():
                exact = _darwin_exe_path(int(pid))
                if exact:
                    found.append((int(pid), exact))
    return found


def _under(path: str, roots: list[str]) -> bool:
    return any(path == r or path.startswith(r.rstrip("/") + "/") for r in roots)


def _roots(*paths: Path) -> list[str]:
    out = []
    for path in paths:
        out.append(str(path))
        with contextlib.suppress(OSError):
            out.append(os.path.realpath(path))
    return sorted(set(out))


def running_from(*bundles: Path, lister=processes) -> list[int]:
    """The pids whose executable is under any of `bundles`."""
    roots = _roots(*bundles)
    return sorted({pid for pid, path in lister() if pid != os.getpid() and _under(path, roots)})


def instance_lock_path(home: Path) -> Path:
    return home / INSTANCE_LOCK


def lock_held(home: Path) -> bool:
    """Does an app process hold its instance lock now? Never creates it."""
    import fcntl

    try:
        fd = os.open(instance_lock_path(home), os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    except OSError:
        return False
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return True
    except OSError:
        return False
    finally:
        os.close(fd)
    return False
