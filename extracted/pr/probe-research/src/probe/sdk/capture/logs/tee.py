"""The owner's side of the console tee: swap fds 1/2 (`InProcessTee`) or a child's streams (`run_teed`) for streams
the helper (logs.py, started from its file) reads, and ask it things through control files. Split out of logs.py,
which stays the stdlib-only helper script; logs.py still serves these names (`logs.__getattr__`)."""

from __future__ import annotations

import contextlib
import os
import subprocess
import sys
import threading
import time

from . import logs as _helper
from .logs import (
    DRAIN_GRACE_SECONDS,
    FLUSH_WAIT_SECONDS,
    READY_WAIT_SECONDS,
    SIGINT_GRACE_SECONDS,
    _adopt_path,
    _close,
    _discard_path,
    _get_adopted_path,
    _meta_path,
    _ready_path,
    _rotate_path,
    _stopped_path,
    copy_winsize,
    get_late_path,
    live_dir,
    read_stats,
    write_request,
)


# -- stream plumbing -------------------------------------------------------------
def _is_terminal(fd: int) -> bool:
    try:
        return os.isatty(fd)
    except OSError:
        return False


def open_stream(like_fd: int) -> tuple[int, int, bool]:
    """``(read_end, write_end, is_pty)`` standing in for the stream ``like_fd``.

    A pty when ``like_fd`` is a terminal, so the writer keeps seeing one; a
    plain pipe otherwise (a job whose output goes to a file or a pipe already
    sees no terminal, and must keep seeing none).
    """
    if _is_terminal(like_fd):
        try:
            import pty
            import termios

            master, slave = pty.openpty()
            master, slave = _move_high(master), _move_high(slave)
            attrs = termios.tcgetattr(slave)
            attrs[1] &= ~termios.OPOST  # no \n -> \r\n: the bytes pass untouched
            termios.tcsetattr(slave, termios.TCSANOW, attrs)
            copy_winsize(like_fd, master)
            os.set_inheritable(master, False)
            return master, slave, True
        except Exception:  # noqa: BLE001 -- no pty available: a pipe still works
            pass
    read_end, write_end = os.pipe()
    return _move_high(read_end), _move_high(write_end), False


def _move_high(fd: int) -> int:
    """``fd`` moved to 3 or above. With stdin closed (``python train.py <&-``)
    a new descriptor takes number 0, where a child's ``stdin=DEVNULL`` -- or
    the program itself -- would later overwrite it."""
    if fd >= 3:
        return fd
    import fcntl

    moved = fcntl.fcntl(fd, fcntl.F_DUPFD_CLOEXEC, 3)
    os.close(fd)
    return moved


def _copy_high(fd: int) -> int:
    import fcntl

    return fcntl.fcntl(fd, fcntl.F_DUPFD_CLOEXEC, 3)


def _get_identity(fd: int) -> tuple[int, int] | None:
    try:
        info = os.fstat(fd)
    except OSError:
        return None
    return info.st_dev, info.st_ino


def _clear_markers(log_path: str) -> None:
    """Control files an earlier owner of this name left: each would act on the new log."""
    for stale in (
        _stopped_path(log_path),
        _meta_path(log_path),
        _ready_path(log_path),
        _adopt_path(log_path),
        _get_adopted_path(log_path),
        _rotate_path(log_path),
        _discard_path(log_path),
        get_late_path(log_path),
    ):
        with contextlib.suppress(OSError):
            os.unlink(stale)


class _Tee:
    """Stand-in streams for fds 1 and 2, read by a helper process that forwards
    to the originals and writes the log.

    :meth:`open` starts the helper and fills :attr:`writers` (``{fd: write
    end}``); the caller hands those to whoever writes. :meth:`finish` tells the
    helper to stop and returns the log's stats once it has written them.
    """

    def __init__(
        self,
        log_path: str,
        *,
        recovery_entry: str | None = None,
        should_watch_parent: bool = False,
        is_held: bool = False,
    ):
        self.log_path = log_path
        #: The capture record the helper hands to a recovery process if its
        #: parent exits without stopping the tee (see `_helper_main`).
        self.recovery_entry = recovery_entry
        #: 2.2: report the parent's death as soon as it is reparented, not at
        #: EOF. Only for a tee of the WRITER itself (`InProcessTee`): under
        #: `run_teed` the parent is a launcher, whose death says nothing about
        #: the child still writing.
        self.should_watch_parent = should_watch_parent
        #: The log is held for a run not open yet (`early`): dropped at EOF unless a run took it.
        self.is_held = is_held
        self.writers: dict[int, int] = {}
        self.saved: dict[int, int] = {}
        self.helper: subprocess.Popen | None = None

    def open(self) -> None:
        _flush_python_streams()
        # A name is reused once its owner dropped the log, but not its stop marker: left
        # there, that marker cut this log at the helper's first tick (#4240's DDP ranks).
        _clear_markers(self.log_path)
        reads: list[int] = []
        specs: list[str] = []
        try:
            for fd in (1, 2):
                self.saved[fd] = _copy_high(fd)
            is_one_stream = _get_identity(1) is not None and _get_identity(1) == _get_identity(2)
            for fd in ((1,) if is_one_stream else (1, 2)):
                read_end, write_end, is_pty = open_stream(self.saved[fd])
                reads.append(read_end)
                self.writers[fd] = write_end
                specs.append(f"{read_end}:{self.saved[fd]}:{1 if is_pty else 0}")
            if is_one_stream:
                # `> log 2>&1`: one stream, so the order the program wrote in
                # is the order the file and the log keep.
                self.writers[2] = self.writers[1]
            extra = ["--recover", self.recovery_entry] if self.recovery_entry else []
            if os.path.isdir(live_dir(self.log_path)):
                # The owner asked for a live stream (probe.sdk.capture.logs.stream).
                extra += ["--live", live_dir(self.log_path)]
            if self.recovery_entry and self.should_watch_parent:
                extra = ["--watch-parent", *extra]
            if self.is_held:
                extra = ["--held", *extra]
            # The helper is logs.py run by path (`-I -S`: stdlib only, tens of milliseconds).
            self.helper = subprocess.Popen(
                [sys.executable, "-I", "-S", os.path.abspath(_helper.__file__), *extra, self.log_path, *specs],
                pass_fds=[*reads, *self.saved.values()],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=self.saved[2],
                close_fds=True,
            )
        except BaseException:
            _close(*reads, *set(self.writers.values()), *self.saved.values())
            self.writers.clear()
            self.saved.clear()
            raise
        _close(*reads)
        # Until the helper has set its signals aside, a signal to the group
        # would kill it: wait (tens of milliseconds) for it to say so. A
        # helper that died starting (an interpreter that cannot run `-I -S`)
        # must never be handed the program's output: nothing would read it.
        deadline = time.monotonic() + READY_WAIT_SECONDS
        while time.monotonic() < deadline:
            if os.path.exists(_ready_path(self.log_path)):
                break
            if self.helper.poll() is not None:
                break
            time.sleep(0.005)
        if self.helper.poll() is not None:
            self.close_writers()
            _close(*self.saved.values())
            self.saved = {}
            raise OSError("the output helper exited as it started")

    def close_writers(self) -> None:
        _close(*set(self.writers.values()))
        self.writers = {}

    def finish(self) -> dict | None:
        """Tell the helper to stop and wait, briefly, for the log.

        The helper exits at EOF. If a straggler still holds a stream, it writes
        the log ``DRAIN_GRACE_SECONDS`` after the stop marker and keeps
        forwarding without it. Returns the log's stats, or None when no
        complete log exists yet."""
        try:
            with open(_stopped_path(self.log_path), "w"):
                pass
        except OSError:
            pass
        _close(*self.saved.values())
        self.saved = {}
        helper = self.helper
        if helper is None:
            return None
        deadline = time.monotonic() + DRAIN_GRACE_SECONDS + FLUSH_WAIT_SECONDS
        while time.monotonic() < deadline:
            if helper.poll() is not None or os.path.exists(_meta_path(self.log_path)):
                break
            time.sleep(0.02)
        return read_stats(self.log_path)


# -- probe exec: tee a child -----------------------------------------------------
def run_teed(
    argv,
    *,
    cwd=None,
    env=None,
    log_path: str,
    recovery_entry: str | None = None,
    on_helper=None,
    teed_env: dict | None = None,
):
    """Run ``argv`` like ``subprocess.run(argv, check=False)``, teeing its
    stdout and stderr to this process's own and to ``log_path``.

    Returns ``(CompletedProcess, stats)``. stdin is inherited untouched, so an
    interactive child reads the real terminal. Signals are not intercepted:
    SIGTERM, SIGUSR1 ... reach this process and the child exactly as before.
    Ctrl-C behaves as ``subprocess.run`` does: the child gets
    ``SIGINT_GRACE_SECONDS`` to exit, is then killed, and KeyboardInterrupt
    propagates. When the tee cannot be set up the command runs untouched and
    ``stats`` is None. ``on_helper(pid)`` learns the helper's pid; ``teed_env``
    is added to the child's environment only once the tee is live.
    """
    tee = _Tee(log_path, recovery_entry=recovery_entry)
    try:
        tee.open()
    except Exception:  # noqa: BLE001 -- capture is never a reason not to run the command
        return subprocess.run(argv, cwd=cwd, env=env, check=False), None
    if teed_env:
        env = {**(os.environ if env is None else env), **teed_env}
    if on_helper is not None and tee.helper is not None:
        try:
            on_helper(tee.helper.pid)
        except Exception:  # noqa: BLE001
            pass
    try:
        from ...run.launch.program import start_program

        # Here, or by the `probe` shim when this runs in the service (T42).
        child = start_program(argv, cwd=cwd, env=env, stdout=tee.writers[1], stderr=tee.writers[2])
    except BaseException:
        tee.close_writers()
        tee.finish()
        raise
    tee.close_writers()  # only the child holds the writing ends now
    try:
        try:
            returncode = child.wait()
        except KeyboardInterrupt:
            try:
                child.wait(timeout=SIGINT_GRACE_SECONDS)
            except subprocess.TimeoutExpired:
                pass
            child.kill()
            child.wait()
            raise
    finally:
        stats = tee.finish()
    return subprocess.CompletedProcess(argv, returncode), stats


# -- probe.init(): tee this process ----------------------------------------------
class InProcessTee:
    """Swap fds 1 and 2 for streams a helper process tees to the originals and
    to a capped log. :meth:`stop` puts the originals back and returns the stats.

    A watcher thread restores the originals if the helper ever dies first (it
    ignores every signal it can, so only SIGKILL or the OOM killer can do that).
    """

    def __init__(
        self,
        log_path: str,
        *,
        recovery_entry: str | None = None,
        should_watch_parent: bool = False,
        is_held: bool = False,
    ):
        self.log_path = log_path
        self._tee = _Tee(
            log_path, recovery_entry=recovery_entry, should_watch_parent=should_watch_parent, is_held=is_held
        )
        self._saved: dict[int, int] = {}
        self._ours: dict[int, tuple[int, int] | None] = {}
        self._is_teeing = False
        self._lock = threading.Lock()

    @property
    def helper_pid(self) -> int | None:
        helper = self._tee.helper
        return helper.pid if helper is not None else None

    @property
    def is_active(self) -> bool:
        """fds 1/2 still go to the helper (not stopped, and the helper has not died)."""
        return self._is_teeing

    def get_identity(self) -> str | None:
        """``dev:inode`` of the stream fd 1 now is, while it is the helper's: what a child that
        inherited it compares its own fd 1 with (`early.TEED_ENV`)."""
        found = self._ours.get(1)
        return f"{found[0]}:{found[1]}" if self._is_teeing and found else None

    def adopt(self, *, recovery_entry: str | None, should_watch_parent: bool, is_live: bool) -> bool:
        """A run takes the held log (``<log>.adopt``): from now on the helper hands this
        record to a recovery if the process dies, and spools ``<log>.live/`` when ``is_live``.
        True once the helper acked (``<log>.adopted``), within ``READY_WAIT_SECONDS``."""
        path = self.log_path
        write_request(
            _adopt_path(path), {"recover": recovery_entry, "watch_parent": should_watch_parent, "live": is_live}
        )
        if self._wait_for(_get_adopted_path(path), READY_WAIT_SECONDS):
            return True
        with contextlib.suppress(OSError):
            os.unlink(_adopt_path(path))
        return False

    def rotate(self, next_path: str) -> dict | None:
        """Finish the current log as complete and go on teeing into ``next_path``, held
        (``<log>.rotate``). The finished log's stats, or None when the helper did not do it
        within ``FLUSH_WAIT_SECONDS``: the caller then stops the tee instead."""
        _flush_c_streams()
        path = self.log_path
        _clear_markers(next_path)
        write_request(_rotate_path(path), {"next": next_path})
        self._wait_for(_meta_path(path), FLUSH_WAIT_SECONDS)
        stats = read_stats(path)
        if stats is None:
            # Withdrawn, so a late helper does not rotate under the stop that follows; one that
            # already did leaves the stats the stop then reads.
            with contextlib.suppress(OSError):
                os.unlink(_rotate_path(path))
            return None
        self.log_path = self._tee.log_path = next_path
        return stats

    def discard(self) -> None:
        """The held log has no run: the helper drops it (``<log>.discard``). Never waits."""
        write_request(_discard_path(self.log_path), {})

    def _wait_for(self, marker: str, seconds: float) -> bool:
        helper = self._tee.helper
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if os.path.exists(marker):
                return True
            if helper is None or helper.poll() is not None:
                break
            time.sleep(0.005)
        return os.path.exists(marker)

    def start(self) -> None:
        tee = self._tee
        tee.open()
        try:
            # Our own copies for restoring, separate from the helper's
            # destinations, which `_Tee.finish` closes.
            for fd in (1, 2):
                self._saved[fd] = _copy_high(fd)
        except BaseException:
            _close(*self._saved.values())
            self._saved.clear()
            tee.close_writers()
            tee.finish()
            raise
        for fd, write_end in tee.writers.items():
            os.dup2(write_end, fd)
            self._ours[fd] = _get_identity(fd)
        tee.close_writers()
        self._is_teeing = True
        # After `_is_teeing`: a helper that dies from here on is seen, and the
        # original streams go back.
        try:
            threading.Thread(target=self._watch, name="probe-log-watch", daemon=True).start()
        except BaseException:
            self._restore()
            _close(*self._saved.values())
            self._saved = {}
            tee.finish()
            raise

    def _restore(self) -> None:
        with self._lock:
            if not self._is_teeing:
                return
            self._is_teeing = False
            _flush_python_streams()
            for fd, saved in self._saved.items():
                # Only a descriptor that is still ours: a program that
                # redirected fd 1 itself after init keeps its redirection.
                if _get_identity(fd) != self._ours.get(fd):
                    continue
                try:
                    os.dup2(saved, fd)
                except OSError:
                    pass

    def _watch(self) -> None:
        helper = self._tee.helper
        if helper is None:
            return
        helper.wait()
        if self._is_teeing:
            self._restore()
            try:
                os.write(
                    self._saved.get(2, 2),
                    b"probe: output capture stopped (its helper exited); "
                    b"output is no longer being logged\n",
                )
            except OSError:
                pass

    def stop(self) -> dict | None:
        """Restore the originals; wait briefly for the helper to finish the
        log. Returns the log's stats, or None when no complete log exists."""
        _flush_c_streams()
        # The marker goes down BEFORE the streams close: the helper reads EOF
        # right after, and a missing marker at that moment is how it tells a
        # crash from a stop.
        try:
            with open(_stopped_path(self.log_path), "w"):
                pass
        except OSError:
            pass
        self._restore()
        _close(*self._saved.values())
        self._saved = {}
        return self._tee.finish()


def _flush_python_streams() -> None:
    # Not on the SIGTERM close's worker thread: the main thread, parked in the
    # handler, may hold a stream's lock for good (CPython runs a handler inside
    # a buffered flush), and waiting on it spent the whole close budget.
    # `sys.modules`, not an import: never load the warning module just to ask it.
    guard = sys.modules.get("probe.foundation.safe_warn.safe_warn")
    if guard is not None and not guard.streams_allowed():
        return
    for stream in (sys.stdout, sys.stderr, sys.__stdout__, sys.__stderr__):
        try:
            if stream is not None:
                stream.flush()
        except Exception:  # noqa: BLE001
            pass


def _flush_c_streams() -> None:
    """``fflush(NULL)``: C stdio buffered in this process lands in the capture
    rather than after it."""
    _flush_python_streams()
    try:
        import ctypes

        ctypes.CDLL(None).fflush(None)
    except Exception:  # noqa: BLE001 -- no libc symbol table: skip
        pass
