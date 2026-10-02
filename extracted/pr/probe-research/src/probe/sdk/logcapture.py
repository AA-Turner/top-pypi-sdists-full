"""Everything a run prints, teed to its terminal and to a capped log file (D17).

Two callers, one mechanism. File descriptors are handed to a HELPER PROCESS
that copies every byte to the real stream and into the log:

* ``probe exec`` owns a CHILD: the child's stdout/stderr are the helper's
  pipes (or ptys, when the exec's own stream is a terminal).
* ``probe.init()`` owns ITSELF: fds 1 and 2 are swapped for the helper's pipes,
  so C-level output (a CUDA abort, a C++ ``terminate called``, faulthandler's
  traceback) is captured too.

WHY A PROCESS, NOT A THREAD. A thread dies with the process it lives in. The
output a hard death writes last -- faulthandler's traceback before SIGSEGV,
libstdc++'s message before abort() -- would sit unread in the pipe, lost from
the TERMINAL as well as the log: the one moment a person most needs to see
stderr. For ``probe exec`` the same holds the other way round: whatever kills
the wrapper (a scheduler's SIGUSR1, ``kill -9``) must not close the child's
stdout, and a background process the command leaves running must keep a
working stdout after ``probe exec`` returns. A separate reader keeps forwarding
until every writer is gone, however anyone died.

THE HELPER IGNORES EVERY SIGNAL IT CAN. It sits in the stream of a program that
never asked for it, so it must be the last thing standing: Ctrl-C, SIGTERM and
SIGHUP reach the whole process group, and Slurm's ``--signal=USR1@90`` /
submitit's USR2 reach every process in a job step. A helper that died of one
would turn the program's next ``print`` into BrokenPipeError. It is told to
stop through a FILE (``<log>.stopped``), never a signal, and exits at EOF.

WHY A PTY WHEN THE STREAM IS A TERMINAL. Swapping a terminal for a pipe changes
the program: ``isatty()`` turns false, so progress bars lose their width,
libraries drop colour, and libc switches C stdout to full buffering. A pty keeps
``isatty()`` true. ``OPOST`` is cleared on it so the line discipline does not
turn ``\\n`` into ``\\r\\n`` -- the terminal and the log get the program's exact
bytes, ``\\r``-redrawn progress bars included.

NOTHING THE PROGRAM COULD SEE MAY CHANGE. stdout and stderr that are the same
file (``> log 2>&1``) share ONE pipe, so their interleaving is kept. A
destination that stops accepting (``| head`` exited) closes the program's end
too, so the program gets EPIPE exactly as it would have. Restoring the streams
leaves alone a descriptor the program itself redirected meanwhile.

LIVE (plan item (h)). When ``<log>.live/`` exists as the helper starts, it
also appends every byte it reads, in order, to ``LIVE_SEGMENT_BYTES`` segment
files there (:class:`LiveSpool`), named by the raw offset of their first byte.
A shipper in the process that owns the tee (:mod:`probe.sdk.logstream`) reads
them, sends complete lines to the server while the run is alive, and deletes
each segment it has sent. The spool never holds more than
``LIVE_UNSHIPPED_BYTES``: past it the OLDEST segment is deleted -- a gap in the
offsets the server records -- and nothing ever waits on the shipper. A spool
that fails (a full disk) stops; the forwarding and the log go on. The final
log above is unchanged by any of this.

STDLIB ONLY, and runnable as a script (``python logcapture.py ...``): the
helper is spawned from this FILE, not the package, so it starts in tens of
milliseconds and never imports httpx beside a training loop.
"""

from __future__ import annotations

import collections
import errno
import json
import os
import select
import selectors
import signal
import subprocess
import sys
import threading
import time

#: The log keeps the first HEAD_BYTES and the last TAIL_BYTES of a run's output.
#: The tail is the larger half on purpose: a run's ending (the traceback, the
#: final eval) is what someone opens the log for.
HEAD_BYTES = 2 * 1024 * 1024
TAIL_BYTES = 8 * 1024 * 1024
#: After a stop, how long the helper waits for stragglers -- a DataLoader worker
#: or a background process that inherited the stream -- before it writes the
#: log as-is and carries on forwarding without it.
DRAIN_GRACE_SECONDS = 0.5
#: How long a stopping caller waits for the helper to finish the log.
FLUSH_WAIT_SECONDS = 2.0
#: How long a starting caller waits for the helper to be signal-proof.
READY_WAIT_SECONDS = 2.0
#: EOF with no stop marker: how long the helper waits to see its parent exit
#: (CUDA teardown takes seconds) before deciding it did not crash.
RECOVERY_WAIT_SECONDS = 60.0
#: What ``subprocess.run`` gives a child after Ctrl-C before killing it.
SIGINT_GRACE_SECONDS = 0.25
_CHUNK = 64 * 1024
#: Live streaming (see LIVE above): one spool segment, and the most the spool
#: may hold that the shipper has not sent (the segment being written included).
LIVE_SEGMENT_BYTES = 1024 * 1024
LIVE_UNSHIPPED_BYTES = 16 * 1024 * 1024
LIVE_SEGMENT_PREFIX = "seg-"
LIVE_SEGMENT_SUFFIX = ".log"
#: Written by the helper when the stream ends, holding its final raw offset.
LIVE_EOF_NAME = "eof"
#: Signals whose default action ends a process and that someone else may send
#: to a whole group or job step. The helper ignores them all.
_IGNORED_SIGNALS = (
    "SIGINT", "SIGTERM", "SIGHUP", "SIGQUIT", "SIGUSR1", "SIGUSR2", "SIGPIPE",
    "SIGALRM", "SIGVTALRM", "SIGPROF", "SIGXCPU", "SIGXFSZ", "SIGIO", "SIGPOLL",
    "SIGPWR", "SIGSTKFLT", "SIGLOST", "SIGINFO", "SIGEMT", "SIGTSTP", "SIGTTIN",
    "SIGTTOU",
)


def omitted_marker(n: int) -> bytes:
    return f"\n[probe: {n:,} bytes of output omitted here]\n".encode()


class CappedLog:
    """A log file holding the first ``head_bytes`` and last ``tail_bytes``.

    The head goes to disk as it arrives, so a reader that dies keeps it; the
    tail is held in memory and written at :meth:`close`. Under the cap the file
    is byte-for-byte what was written -- nothing is inserted unless something
    was dropped.
    """

    def __init__(self, path: str, *, head_bytes: int = HEAD_BYTES, tail_bytes: int = TAIL_BYTES):
        self.path = path
        self.head_bytes = head_bytes
        self.tail_bytes = tail_bytes
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        self._file = os.fdopen(fd, "wb", buffering=0)
        self._head = 0
        self._tail: collections.deque[bytes] = collections.deque()
        self._tail_len = 0
        self.total = 0
        self.omitted = 0
        self.closed = False

    def write(self, data: bytes) -> None:
        if self.closed or not data:
            return
        self.total += len(data)
        room = self.head_bytes - self._head
        if room > 0:
            part = data[:room]
            self._file.write(part)
            self._head += len(part)
            data = data[room:]
        if not data:
            return
        self._tail.append(data)
        self._tail_len += len(data)
        # Drop whole chunks from the left while what remains still covers the
        # cap; the exact cut happens once, at close.
        while self._tail and self._tail_len - len(self._tail[0]) >= self.tail_bytes:
            self._tail_len -= len(self._tail.popleft())

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        tail = b"".join(self._tail)
        self._tail.clear()
        if len(tail) > self.tail_bytes:
            tail = tail[len(tail) - self.tail_bytes :]
        self.omitted = self.total - self._head - len(tail)
        try:
            if self.omitted:
                self._file.write(omitted_marker(self.omitted))
            self._file.write(tail)
        finally:
            self._file.close()

    def stats(self) -> dict:
        return {"total_bytes": self.total, "omitted_bytes": self.omitted}


def live_dir(log_path: str) -> str:
    """The spool directory beside ``log_path``. Its existence when the helper
    starts is what turns live mode on."""
    return log_path + ".live"


def segment_name(start: int) -> str:
    return f"{LIVE_SEGMENT_PREFIX}{start:016d}{LIVE_SEGMENT_SUFFIX}"


def list_segments(directory: str) -> list[tuple[int, str, int]]:
    """``(start offset, path, size)`` of every segment in ``directory``, oldest
    first. A segment deleted while this lists it is left out."""
    found = []
    try:
        entries = list(os.scandir(directory))
    except OSError:
        return []
    for entry in entries:
        name = entry.name
        if not (name.startswith(LIVE_SEGMENT_PREFIX) and name.endswith(LIVE_SEGMENT_SUFFIX)):
            continue
        digits = name[len(LIVE_SEGMENT_PREFIX) : -len(LIVE_SEGMENT_SUFFIX)]
        if not digits.isdigit():
            continue
        try:
            size = entry.stat().st_size
        except OSError:
            continue
        found.append((int(digits), entry.path, size))
    found.sort()
    return found


def read_eof(directory: str) -> int | None:
    """The stream's final raw offset once the helper has ended it, else None."""
    try:
        with open(os.path.join(directory, LIVE_EOF_NAME), encoding="ascii") as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        return None


class LiveSpool:
    """Every byte the helper reads, appended in order to segment files named
    by the raw offset of their first byte (see LIVE in the module docstring).

    Concatenating the segments that exist gives exactly the stream's bytes
    from the oldest one's offset on. The shipper deletes a segment once it has
    sent it; this class counts what is left when it starts a new segment and
    deletes the OLDEST ones while the total would pass ``budget_bytes``. That
    is the only place a byte can be lost, it is visible as a jump in the
    offsets, and it never waits.
    """

    def __init__(
        self,
        directory: str,
        *,
        segment_bytes: int = LIVE_SEGMENT_BYTES,
        budget_bytes: int = LIVE_UNSHIPPED_BYTES,
    ):
        self.dir = directory
        self.segment_bytes = segment_bytes
        self.budget_bytes = budget_bytes
        #: Raw offset of the next byte, i.e. every byte ever written.
        self.offset = 0
        #: Bytes deleted unsent because the budget was full.
        self.dropped = 0
        self.closed = False
        self._fd: int | None = None
        self._segment_len = 0
        self._open_segment()

    def _open_segment(self) -> None:
        path = os.path.join(self.dir, segment_name(self.offset))
        self._fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        self._segment_len = 0

    def write(self, data: bytes) -> None:
        if self.closed or not data:
            return
        view = memoryview(data)
        while view:
            room = self.segment_bytes - self._segment_len
            if room <= 0:
                self._roll()
                continue
            part = view[:room]
            _write_all(self._fd, part)
            self._segment_len += len(part)
            self.offset += len(part)
            view = view[len(part) :]

    def _roll(self) -> None:
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None
        self._enforce_budget()
        self._open_segment()

    def _enforce_budget(self) -> None:
        """Room for the segment about to start: delete the oldest segments
        while what is unsent, plus one full segment, would pass the budget."""
        segments = list_segments(self.dir)
        total = sum(size for _, _, size in segments)
        while segments and total + self.segment_bytes > self.budget_bytes:
            _, path, size = segments.pop(0)
            try:
                os.unlink(path)
                self.dropped += size
            except FileNotFoundError:
                pass  # the shipper sent and deleted it meanwhile
            total -= size

    def close(self) -> None:
        """End the stream: the last segment is complete, and ``eof`` says
        where the stream stopped."""
        if self.closed:
            return
        self.closed = True
        try:
            if self._fd is not None:
                os.close(self._fd)
        finally:
            self._fd = None
            tmp = os.path.join(self.dir, LIVE_EOF_NAME + ".tmp")
            with open(tmp, "w", encoding="ascii") as fh:
                fh.write(str(self.offset))
            os.replace(tmp, os.path.join(self.dir, LIVE_EOF_NAME))


def _write_all(fd: int, data: bytes) -> None:
    view = memoryview(data)
    while view:
        try:
            written = os.write(fd, view)
        except BlockingIOError:
            # A destination someone set O_NONBLOCK on (a shared tty): wait
            # until it takes more, exactly as a blocking write would.
            select.select([], [fd], [], 1.0)
            continue
        view = view[written:]


def pump(pairs, log, *, stop: threading.Event | None = None, on_tick=None) -> None:
    """Copy each ``(src_fd, dst_fd)`` to its destination and into ``log``
    until every source ends (EOF, or EIO from a pty whose writers are gone).
    ``log`` is anything with ``write(bytes)`` (a :class:`CappedLog`), or None.

    A destination that stops accepting (the reader of a pipe exited) closes its
    SOURCE: the writer then gets EPIPE, as it would have writing there itself,
    instead of running on into a stream nobody reads. A log that fails is
    dropped and the forwarding carries on. ``stop`` ends the pump early;
    ``on_tick`` runs between reads, at least every 0.2s.
    """
    selector = selectors.DefaultSelector()
    live: dict[int, int] = {}
    for src, dst in pairs:
        selector.register(src, selectors.EVENT_READ)
        live[src] = dst
    try:
        while live:
            if stop is not None and stop.is_set():
                return
            if on_tick is not None:
                on_tick()
            for key, _ in selector.select(timeout=0.2):
                src = key.fd
                try:
                    data = os.read(src, _CHUNK)
                except OSError as exc:
                    if exc.errno not in (errno.EIO, errno.EBADF):
                        raise
                    data = b""
                if not data:
                    selector.unregister(src)
                    live.pop(src, None)
                    continue
                try:
                    _write_all(live[src], data)
                except OSError:
                    selector.unregister(src)
                    live.pop(src, None)
                    _close(src)
                if log is not None:
                    try:
                        log.write(data)
                    except Exception:  # noqa: BLE001
                        # A full disk under the log must never stop the
                        # forwarding: a reader that stops reading lets the pipe
                        # fill, and the writer -- the training job -- blocks
                        # forever. Drop the log, keep the stream moving.
                        log = None
    finally:
        selector.close()


# -- stream plumbing -------------------------------------------------------------
def _terminal(fd: int) -> bool:
    try:
        return os.isatty(fd)
    except OSError:
        return False


def copy_winsize(src_fd: int, dst_fd: int) -> None:
    try:
        import fcntl
        import termios

        size = fcntl.ioctl(src_fd, termios.TIOCGWINSZ, b"\0" * 8)
        fcntl.ioctl(dst_fd, termios.TIOCSWINSZ, size)
    except Exception:  # noqa: BLE001 -- a window size is cosmetic
        pass


def open_stream(like_fd: int) -> tuple[int, int, bool]:
    """``(read_end, write_end, is_pty)`` standing in for the stream ``like_fd``.

    A pty when ``like_fd`` is a terminal, so the writer keeps seeing one; a
    plain pipe otherwise (a job whose output goes to a file or a pipe already
    sees no terminal, and must keep seeing none).
    """
    if _terminal(like_fd):
        try:
            import pty
            import termios

            master, slave = pty.openpty()
            master, slave = _high(master), _high(slave)
            attrs = termios.tcgetattr(slave)
            attrs[1] &= ~termios.OPOST  # no \n -> \r\n: the bytes pass untouched
            termios.tcsetattr(slave, termios.TCSANOW, attrs)
            copy_winsize(like_fd, master)
            os.set_inheritable(master, False)
            return master, slave, True
        except Exception:  # noqa: BLE001 -- no pty available: a pipe still works
            pass
    read_end, write_end = os.pipe()
    return _high(read_end), _high(write_end), False


def _high(fd: int) -> int:
    """``fd`` moved to 3 or above. With stdin closed (``python train.py <&-``)
    a new descriptor takes number 0, where a child's ``stdin=DEVNULL`` -- or
    the program itself -- would later overwrite it."""
    if fd >= 3:
        return fd
    import fcntl

    moved = fcntl.fcntl(fd, fcntl.F_DUPFD_CLOEXEC, 3)
    os.close(fd)
    return moved


def _dup_high(fd: int) -> int:
    import fcntl

    return fcntl.fcntl(fd, fcntl.F_DUPFD_CLOEXEC, 3)


def _identity(fd: int) -> tuple[int, int] | None:
    try:
        info = os.fstat(fd)
    except OSError:
        return None
    return info.st_dev, info.st_ino


def _close(*fds: int | None) -> None:
    for fd in fds:
        if fd is None:
            continue
        try:
            os.close(fd)
        except OSError:
            pass


class _Tee:
    """Stand-in streams for fds 1 and 2, read by a helper process that forwards
    to the originals and writes the log.

    :meth:`open` starts the helper and fills :attr:`writers` (``{fd: write
    end}``); the caller hands those to whoever writes. :meth:`finish` tells the
    helper to stop and returns the log's stats once it has written them.
    """

    def __init__(
        self, log_path: str, *, recovery_entry: str | None = None, watch_parent: bool = False
    ):
        self.log_path = log_path
        #: The capture record the helper hands to a recovery process if its
        #: parent exits without stopping the tee (see `_helper_main`).
        self.recovery_entry = recovery_entry
        #: 2.2: report the parent's death as soon as it is reparented, not at
        #: EOF. Only for a tee of the WRITER itself (`InProcessTee`): under
        #: `run_teed` the parent is a launcher, whose death says nothing about
        #: the child still writing.
        self.watch_parent = watch_parent
        self.writers: dict[int, int] = {}
        self.saved: dict[int, int] = {}
        self.helper: subprocess.Popen | None = None

    def open(self) -> None:
        _flush_python_streams()
        reads: list[int] = []
        specs: list[str] = []
        try:
            for fd in (1, 2):
                self.saved[fd] = _dup_high(fd)
            same = _identity(1) is not None and _identity(1) == _identity(2)
            for fd in ((1,) if same else (1, 2)):
                read_end, write_end, is_pty = open_stream(self.saved[fd])
                reads.append(read_end)
                self.writers[fd] = write_end
                specs.append(f"{read_end}:{self.saved[fd]}:{1 if is_pty else 0}")
            if same:
                # `> log 2>&1`: one stream, so the order the program wrote in
                # is the order the file and the log keep.
                self.writers[2] = self.writers[1]
            extra = ["--recover", self.recovery_entry] if self.recovery_entry else []
            if os.path.isdir(live_dir(self.log_path)):
                # The owner asked for a live stream (probe.sdk.logstream).
                extra += ["--live", live_dir(self.log_path)]
            if self.recovery_entry and self.watch_parent:
                extra = ["--watch-parent", *extra]
            self.helper = subprocess.Popen(
                [sys.executable, "-I", "-S", os.path.abspath(__file__), *extra, self.log_path, *specs],
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
        proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=tee.writers[1], stderr=tee.writers[2])
    except BaseException:
        tee.close_writers()
        tee.finish()
        raise
    tee.close_writers()  # only the child holds the writing ends now
    try:
        try:
            returncode = proc.wait()
        except KeyboardInterrupt:
            try:
                proc.wait(timeout=SIGINT_GRACE_SECONDS)
            except subprocess.TimeoutExpired:
                pass
            proc.kill()
            proc.wait()
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
        self, log_path: str, *, recovery_entry: str | None = None, watch_parent: bool = False
    ):
        self.log_path = log_path
        self._tee = _Tee(log_path, recovery_entry=recovery_entry, watch_parent=watch_parent)
        self._saved: dict[int, int] = {}
        self._ours: dict[int, tuple[int, int] | None] = {}
        self._active = False
        self._lock = threading.Lock()

    @property
    def helper_pid(self) -> int | None:
        helper = self._tee.helper
        return helper.pid if helper is not None else None

    def start(self) -> None:
        tee = self._tee
        tee.open()
        try:
            # Our own copies for restoring, separate from the helper's
            # destinations, which `_Tee.finish` closes.
            for fd in (1, 2):
                self._saved[fd] = _dup_high(fd)
        except BaseException:
            _close(*self._saved.values())
            self._saved.clear()
            tee.close_writers()
            tee.finish()
            raise
        for fd, write_end in tee.writers.items():
            os.dup2(write_end, fd)
            self._ours[fd] = _identity(fd)
        tee.close_writers()
        self._active = True
        # After `_active`: a helper that dies from here on is seen, and the
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
            if not self._active:
                return
            self._active = False
            _flush_python_streams()
            for fd, saved in self._saved.items():
                # Only a descriptor that is still ours: a program that
                # redirected fd 1 itself after init keeps its redirection.
                if _identity(fd) != self._ours.get(fd):
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
        if self._active:
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


def _meta_path(log_path: str) -> str:
    return log_path + ".meta.json"


def _stopped_path(log_path: str) -> str:
    return log_path + ".stopped"


def _ready_path(log_path: str) -> str:
    return log_path + ".ready"


#: Popen keywords for a child that outlives this process and its Ctrl-C: a new
#: session on POSIX; Windows ignores that one, so a detached new process group
#: there. Inline rather than `probe._shared.oscompat.DETACHED`: this module also
#: runs as a `-I -S` script that cannot import probe.
_DETACHED: dict = (
    {"creationflags": subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP}
    if os.name == "nt"
    else {"start_new_session": True}
)


def _spawn_recovery(entry: str) -> None:
    """The run's process died without closing its capture: hand the record to
    a normal interpreter (this helper runs `-I -S` and cannot import probe),
    detached, with the run's own environment and credentials. It starts in the
    record's own private directory, never the run's folder: `python -m` puts
    the working directory first on sys.path, and a `probe/` folder there would
    be imported instead of the SDK."""
    try:
        subprocess.Popen(
            [sys.executable, "-m", "probe.sdk.outputs", "--recover", entry],
            cwd=os.path.dirname(os.path.abspath(entry)),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **_DETACHED,
            close_fds=True,
        )
    except Exception:  # noqa: BLE001 -- the next capture start retries it
        pass


def _spawn_writer_gone(entry: str) -> None:
    """The run's own process is gone: report it NOW (2.2), from a normal
    interpreter, detached, like `_spawn_recovery`. The reporter claims the
    record once (``ENTRY.gone``), so a second trigger is harmless."""
    try:
        subprocess.Popen(
            [sys.executable, "-m", "probe.sdk.outputs", "--writer-gone", entry],
            cwd=os.path.dirname(os.path.abspath(entry)),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **_DETACHED,
            close_fds=True,
        )
    except Exception:  # noqa: BLE001 -- the reaper still ends the run
        pass


def read_stats(log_path: str) -> dict | None:
    try:
        with open(_meta_path(log_path), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def _write_stats(log: CappedLog) -> None:
    tmp = _meta_path(log.path) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(log.stats(), fh)
    os.replace(tmp, _meta_path(log.path))


def _flush_python_streams() -> None:
    # Not on the SIGTERM close's worker thread: the main thread, parked in the
    # handler, may hold a stream's lock for good (CPython runs a handler inside
    # a buffered flush), and waiting on it spent the whole close budget.
    # `sys.modules`, not an import: this module also runs as a `-I -S` script.
    guard = sys.modules.get("probe.sdk.safe_warn")
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


def _ignore_signals() -> None:
    for name in _IGNORED_SIGNALS:
        signum = getattr(signal, name, None)
        if signum is None:
            continue
        try:
            signal.signal(signum, signal.SIG_IGN)
        except (OSError, ValueError, RuntimeError):
            pass
    low, high = getattr(signal, "SIGRTMIN", 0), getattr(signal, "SIGRTMAX", -1)
    for signum in range(low, high + 1):
        try:
            signal.signal(signum, signal.SIG_IGN)
        except (OSError, ValueError, RuntimeError):
            pass


def _parent_exited(parent: int, stopped: str) -> bool:
    """EOF arrived with no stop marker. Did the parent exit? It is reparented
    away from us the moment it exits -- before anyone reaps it, and while a
    zombie still answers ``kill(pid, 0)``. It may also still be tearing down
    (CUDA teardown takes seconds), so wait a while before deciding it lives."""
    deadline = time.monotonic() + RECOVERY_WAIT_SECONDS
    while True:
        if os.getppid() != parent:
            return True
        if os.path.exists(stopped) or time.monotonic() >= deadline:
            return False
        time.sleep(0.1)


def _helper_main(argv: list[str]) -> int:
    """``logcapture.py [--watch-parent] [--recover ENTRY] [--live DIR] LOG_PATH SRC:DST:PTY ...``
    -- the helper."""
    _ignore_signals()
    recovery_entry = None
    live_path = None
    watch_parent = False
    while argv and argv[0] in ("--watch-parent", "--recover", "--live"):
        if argv[0] == "--watch-parent":
            watch_parent, argv = True, argv[1:]
            continue
        if argv[0] == "--recover":
            recovery_entry = argv[1]
        else:
            live_path = argv[1]
        argv = argv[2:]
    parent = os.getppid()
    log_path, *specs = argv
    try:
        with open(_ready_path(log_path), "w"):
            pass
    except OSError:
        pass
    stopped = _stopped_path(log_path)
    pairs, ptys = [], []
    for spec in specs:
        src, dst, is_pty = (int(part) for part in spec.split(":"))
        pairs.append((src, dst))
        if is_pty:
            ptys.append((dst, src))
    if ptys and hasattr(signal, "SIGWINCH"):

        def _resize(*_):
            for tty, master in ptys:
                copy_winsize(tty, master)

        signal.signal(signal.SIGWINCH, _resize)
    state: dict = {"log": None, "stop_seen": None, "live": None, "gone_reported": False}
    try:
        state["log"] = CappedLog(log_path)
    except OSError:
        pass  # no log (a full disk): forwarding is still the whole job
    if live_path:
        try:
            state["live"] = LiveSpool(live_path)
        except OSError:
            pass  # no spool: the live view goes without, nothing else does

    def _close_live() -> None:
        live, state["live"] = state["live"], None
        if live is None:
            return
        try:
            live.close()
        except Exception:  # noqa: BLE001 -- the live view is best effort
            pass

    def _flush_log() -> None:
        # The spool ends first: once the log's stats exist the owner stops
        # its shipper, which then reads `eof` to know it has everything.
        _close_live()
        log, state["log"] = state["log"], None
        if log is None:
            return
        try:
            log.close()
            _write_stats(log)
        except Exception:  # noqa: BLE001 -- a full disk loses the tail, not the stream
            pass

    def _report_gone() -> None:
        state["gone_reported"] = True
        if recovery_entry:
            _spawn_writer_gone(recovery_entry)

    def _tick() -> None:
        # 2.2: the parent (the run's writer) is gone the moment we are
        # reparented, whether or not anyone still holds the streams -- a
        # grandchild keeping stdout open delays EOF forever. Checked every
        # tick (<= 0.2 s), and never after a stop: a clean close is no death.
        if (
            watch_parent
            and not state["gone_reported"]
            and os.getppid() != parent
            and state["stop_seen"] is None
            and not os.path.exists(stopped)
        ):
            _report_gone()
        if state["log"] is None:
            _close_live()  # a straggler's output after the log was taken is not streamed either
            return
        if state["stop_seen"] is None:
            if os.path.exists(stopped):
                state["stop_seen"] = time.monotonic()
        elif time.monotonic() - state["stop_seen"] >= DRAIN_GRACE_SECONDS:
            # Stopped, but someone still holds a stream: take the log now and
            # keep forwarding for them.
            _flush_log()

    class _Log:
        def write(self, data: bytes) -> None:
            if state["live"] is not None:
                try:
                    state["live"].write(data)
                except Exception:  # noqa: BLE001 -- a full disk ends the spool, not the stream
                    _close_live()
            if state["log"] is None:
                return
            try:
                state["log"].write(data)
            except Exception:  # noqa: BLE001
                _flush_log()

    try:
        pump(pairs, _Log(), on_tick=_tick)
    finally:
        # Before the log is handed back: once it is, the caller may clean up.
        stopped_seen = state["stop_seen"] is not None or os.path.exists(stopped)
        _flush_log()
    # EOF with no stop marker and the parent gone: it died mid-run (a segfault,
    # an abort, the OOM killer, a SIGTERM). Its outputs and this log are still
    # on disk, and nothing else will ever send them.
    if recovery_entry and not stopped_seen and _parent_exited(parent, stopped):
        if watch_parent and not state["gone_reported"]:
            _report_gone()
        _spawn_recovery(recovery_entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(_helper_main(sys.argv[1:]))
