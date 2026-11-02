"""run the bundle's same-team swap program (probe-swap) as its own responsible process and read its answer."""

from __future__ import annotations
import contextlib
import json
import os
import shutil
import stat
import subprocess
import time
from pathlib import Path

from . import locate as appupdate
from probe.service.updater.app.bundle_check import bundle_info
from probe.service.updater.app.errors import InstallError
from probe.service.updater.app.manifest import supported
from probe.service.updater.app.running import _libsystem
#: The release's update helper (prbe-ai/desktop `src-tauri/src/bin/probe-swap.rs`)
#: and the Info.plist key that says a release has it (`ProbeSwapHelper` = 1).
HELPER_NAME = "probe-swap"
HELPER_KEY = "ProbeSwapHelper"
#: Beside the app while the helper's two renames are under way (`recover`);
#: desktop `probe-swap.rs` `JOURNAL_NAME`.
HELPER_JOURNAL_NAME = f".{appupdate.APP_NAME}.probe-swap.json"
#: A folder the helper's `--remove` renamed before deleting it (`DELETING_SUFFIX`):
#: what is left of it is the installed app's helper's to delete (`sweep`).
HELPER_DELETING_SUFFIX = ".deleting"
#: Its codesign checks of two bundles, the swap and `gktool scan` (60 s), at most.
HELPER_TIMEOUT_S = 5 * 60.0
#: <spawn.h> POSIX_SPAWN_CLOEXEC_DEFAULT (Apple): only the descriptors the file
#: actions name reach the helper.
_POSIX_SPAWN_CLOEXEC_DEFAULT = 0x4000


# -- the same-team helper (prbe-ai/desktop `src-tauri/src/bin/probe-swap.rs`) -------

#: The helper's `result` words (desktop `probe-swap.rs` `Outcome::word`); its
#: exit codes 0, 0, 3, 4, 5, 1. Each answer also carries a machine `reason`
#: (`Reason::word`) and, after an exchange, `old`: where the old bundle is.
HELPER_SWAPPED = "swapped"
HELPER_REMOVED = "removed"
HELPER_APP_RUNNING = "app_running"
HELPER_REFUSED = "refused"
HELPER_NOT_PERMITTED = "not_permitted"
HELPER_ERROR = "error"
HELPER_RESULTS = (HELPER_SWAPPED, HELPER_REMOVED, HELPER_APP_RUNNING, HELPER_REFUSED, HELPER_NOT_PERMITTED, HELPER_ERROR)
#: This side's own reasons for an `error` answer: the helper did not start or answer.
REASON_NO_DISCLAIM = "no_disclaim"
REASON_NOT_STARTED = "not_started"
REASON_NO_ANSWER = "no_answer"
#: The helper's reason when an old copy started from the old bundle during the swap.
REASON_APP_STARTED = "app_started"
#: An answer that is not `swapped`, with the new release already the app, counts
#: as installed only for these: the answer was lost (or the helper never ran and
#: something else put it there), or the helper could not swap back from under an
#: old copy that started (the new app was verified before the swap). Never for
#: `verify_failed` or `changed`: that new app is not the one checked.
INSTALLED_ANYWAY = frozenset({REASON_NO_ANSWER, REASON_NOT_STARTED, REASON_APP_STARTED})
#: The helper's reasons for an app that failed its checks after the swap; with
#: `undo_failed` that app may be the app now (`Updater`'s `app_install_broken`).
UNTRUSTED_AFTER_SWAP = frozenset({"verify_failed", "changed"})
#: The helper's `refused` reasons that stay the same for the same release: the
#: release is not tried again for REFUSED_BACKOFF_S unless another release is
#: the latest (`Outcome.REFUSED_RELEASE`).
PERMANENT_REFUSALS = frozenset({"unsigned", "not_newer", "not_probe", "quarantined"})


def helper_of(bundle: Path) -> Path | None:
    """The bundle's `Contents/MacOS/probe-swap`, when its Info.plist says it
    has one (`ProbeSwapHelper` = 1) and it is an executable file; else None."""
    try:
        info = bundle_info(bundle)
    except InstallError:
        return None
    flag = info.get(HELPER_KEY)
    if isinstance(flag, bool) or flag != 1:
        return None
    path = bundle / "Contents" / "MacOS" / HELPER_NAME
    try:
        mode = os.lstat(path).st_mode
    except OSError:
        return None
    return path if stat.S_ISREG(mode) and mode & 0o100 else None


def _helper_env() -> dict:
    # The helper reads nothing from its environment (its home comes from the
    # user database); a fixed PATH for the system tools it runs.
    return {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C"}


def _answer(code: int, out: str, err: str) -> dict:
    for line in reversed(out.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            with contextlib.suppress(ValueError):
                data = json.loads(line)
                if isinstance(data, dict):
                    return data
    detail = err.strip()[-300:] or f"the update helper exited {code} and said nothing"
    return {"result": HELPER_ERROR, "reason": REASON_NO_ANSWER, "detail": detail}


def _wait(pid: int, timeout: float) -> int:
    import signal

    deadline = time.monotonic() + timeout
    while True:
        done, status = os.waitpid(pid, os.WNOHANG)
        if done == pid:
            return os.waitstatus_to_exitcode(status)
        if time.monotonic() >= deadline:
            with contextlib.suppress(OSError):
                os.kill(pid, signal.SIGKILL)
            _, status = os.waitpid(pid, 0)
            return os.waitstatus_to_exitcode(status)
        time.sleep(0.05)


def _disclaim_available() -> bool:
    try:
        return hasattr(_libsystem(), "responsibility_spawnattrs_setdisclaim")
    except OSError:
        return False


def _spawn_disclaimed(argv: list[str], timeout: float) -> tuple[int, str, str]:
    """posix_spawn the helper as its OWN responsible process
    (`responsibility_spawnattrs_setdisclaim`, looked up at run time as LLDB
    does): macOS then judges the change to the app by the helper's signature
    (the Probe team), not by this Python's. Only stdin/stdout/stderr reach it
    (POSIX_SPAWN_CLOEXEC_DEFAULT)."""
    import ctypes
    import tempfile

    libc = _libsystem()
    work = tempfile.mkdtemp(prefix="probe-swap-")
    out_path, err_path = os.path.join(work, "out"), os.path.join(work, "err")
    attr, actions = ctypes.c_void_p(), ctypes.c_void_p()
    pid = ctypes.c_int()
    try:
        if libc.posix_spawnattr_init(ctypes.byref(attr)) != 0:
            raise OSError("posix_spawnattr_init failed")
        try:
            if libc.posix_spawn_file_actions_init(ctypes.byref(actions)) != 0:
                raise OSError("posix_spawn_file_actions_init failed")
            try:
                if libc.responsibility_spawnattrs_setdisclaim(ctypes.byref(attr), ctypes.c_int(1)) != 0:
                    raise OSError("responsibility_spawnattrs_setdisclaim failed")
                if libc.posix_spawnattr_setflags(ctypes.byref(attr), ctypes.c_short(_POSIX_SPAWN_CLOEXEC_DEFAULT)) != 0:
                    raise OSError("posix_spawnattr_setflags failed")
                for fd, path, flags in (
                    (0, b"/dev/null", os.O_RDONLY),
                    (1, os.fsencode(out_path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC),
                    (2, os.fsencode(err_path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC),
                ):
                    if libc.posix_spawn_file_actions_addopen(
                        ctypes.byref(actions), ctypes.c_int(fd), path, ctypes.c_int(flags), ctypes.c_int(0o600)
                    ) != 0:
                        raise OSError("posix_spawn_file_actions_addopen failed")
                args = [os.fsencode(a) for a in argv]
                argv_c = (ctypes.c_char_p * (len(args) + 1))(*args, None)
                env = [f"{k}={v}".encode() for k, v in _helper_env().items()]
                envp = (ctypes.c_char_p * (len(env) + 1))(*env, None)
                rc = libc.posix_spawn(
                    ctypes.byref(pid), argv_c[0], ctypes.byref(actions), ctypes.byref(attr), argv_c, envp
                )
                if rc != 0:
                    raise OSError(rc, f"posix_spawn: {os.strerror(rc)}")
            finally:
                libc.posix_spawn_file_actions_destroy(ctypes.byref(actions))
        finally:
            libc.posix_spawnattr_destroy(ctypes.byref(attr))
        code = _wait(pid.value, timeout)
        out = Path(out_path).read_text(encoding="utf-8", errors="replace")
        err = Path(err_path).read_text(encoding="utf-8", errors="replace")
        return code, out, err
    finally:
        shutil.rmtree(work, ignore_errors=True)


def _spawn_plain(argv: list[str], timeout: float) -> tuple[int, str, str]:
    """Elsewhere (no desktop app; the tests): a plain child."""
    try:
        done = subprocess.run(
            argv, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL, env=_helper_env()
        )
    except subprocess.TimeoutExpired:
        return -9, "", f"the update helper did not finish within {timeout:g} s"
    return done.returncode, done.stdout, done.stderr


def run_helper(argv: list[str], *, timeout: float = HELPER_TIMEOUT_S) -> tuple[int, dict]:
    """Run a bundle's update helper; `(exit code, its JSON answer)`. On macOS
    only as its own responsible process (posix_spawn with the disclaim
    attribute): without it the helper is not run at all, since macOS would
    judge its change by this Python and refuse it with a notification."""
    try:
        if supported():
            if not _disclaim_available():
                return -1, {"result": HELPER_ERROR, "reason": REASON_NO_DISCLAIM,
                            "detail": "this macOS cannot start the update helper as its own process"}
            code, out, err = _spawn_disclaimed(argv, timeout)
        else:
            code, out, err = _spawn_plain(argv, timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        return -1, {"result": HELPER_ERROR, "reason": REASON_NOT_STARTED,
                    "detail": f"the update helper could not start: {exc}"}
    return code, _answer(code, out, err)
