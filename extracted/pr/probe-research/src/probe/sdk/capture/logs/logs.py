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

ONE TEE PER PROCESS, MANY RUNS (run-logs plan T14/T15). ``import probe`` may
start the helper before any run exists (``--held``: :mod:`.early`); the run a
``probe.init()`` opens takes it over (``<log>.adopt``: the recovery record and
the live stream, acked by ``<log>.adopted``), and its close asks for
``<log>.rotate``: the helper finishes the current file as that run's log
(``<log>.meta.json`` is the ack), empties its buffers and goes on teeing into
the file the request names, held for whatever comes next. ``<log>.discard``
drops a held file no run took. A held file nobody asked to keep is deleted at
EOF. Every byte lands in exactly one file.

THE SAVED FILE COLLAPSES REDRAWS (T20): a line a ``\\r`` progress bar redrew
is kept as its last frame (:func:`keep_last_frames`, the live stream's rule
too) BEFORE the cap counts it; the terminal still gets the exact bytes.

LIVE (plan item (h)). When ``<log>.live/`` exists as the helper starts (or a
run's adoption asks for it), it also appends every byte it reads, in order, to
``LIVE_SEGMENT_BYTES`` segment files there (:class:`LiveSpool`), named by the
raw offset of their first byte.
A shipper in the process that owns the tee (:mod:`probe.sdk.capture.logs.stream`) reads
them, sends complete lines to the server while the run is alive, and deletes
each segment it has sent. The spool never holds more than
``LIVE_UNSHIPPED_BYTES``: past it the OLDEST segment is deleted -- a gap in the
offsets the server records -- and nothing ever waits on the shipper. A spool
that fails (a full disk) stops; the forwarding and the log go on. The final
log above is unchanged by any of this.

STDLIB ONLY, and runnable as a script (``python logs.py ...``): the
helper is spawned from this FILE, not the package, so it starts in tens of
milliseconds and never imports httpx beside a training loop. The owner's side
(swapping the streams, starting this file, asking it things) is tee.py; its
names are still served here (:func:`__getattr__`).
"""

from __future__ import annotations

import collections
import contextlib
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
#: A spool a run's adoption starts begins with the newest output held before it, at most this.
LIVE_SEED_BYTES = 1024 * 1024
#: The saved log holds a line still being drawn as its last frame, at most this; past it the
#: line goes to the log as it is (a progress bar with no newline, a minified dump).
MAX_HELD_LINE_BYTES = 64 * 1024
#: After a rotate request the helper reads what the writers had already written (a pty's line
#: discipline may lag) until nothing comes for ROTATE_QUIET_SECONDS, at most ROTATE_DRAIN_SECONDS:
#: a writer that never pauses must not hold the rotate past its owner's wait.
ROTATE_QUIET_SECONDS = 0.05
ROTATE_DRAIN_SECONDS = 0.25
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


def keep_last_frames(text):
    """Each line as a terminal left it: the last frame a ``\\r`` redraw drew (``str`` or ``bytes``).
    A text that ends in a redraw keeps that ``\\r``: the next piece's first frame then replaces
    this one where the pieces are joined, instead of being appended to it. THE one redraw rule:
    the live stream (stream.py) and the saved log (:class:`RedrawCollapse`) both use it."""
    cr, lf = ("\r", "\n") if isinstance(text, str) else (b"\r", b"\n")
    empty = text[:0]
    lines = text.replace(cr + lf, lf).split(lf)
    for index, line in enumerate(lines):
        if cr in line:
            frames = [frame for frame in line.split(cr) if frame.strip()]
            redraw = cr if index == len(lines) - 1 and line.endswith(cr) else empty
            lines[index] = (frames[-1] if frames else empty) + redraw
    return lf.join(lines)


class RedrawCollapse:
    """:func:`keep_last_frames` fed the stream piece by piece, for the saved log: complete lines
    go out collapsed; the line still being drawn is held as its last frame, at most
    ``MAX_HELD_LINE_BYTES`` (past it, it goes out as it is)."""

    def __init__(self) -> None:
        self._line = b""

    def push(self, data: bytes) -> bytes:
        pending = self._line + data
        end = pending.rfind(b"\n") + 1
        if b"\r" not in pending:
            done, self._line = pending[:end], pending[end:]
        else:
            done = keep_last_frames(pending[:end]) if end else b""
            # The frame after the last redraw is still being drawn: kept as it is, never judged blank yet.
            drawn, cr, drawing = pending[end:].rpartition(b"\r")
            self._line = (keep_last_frames(drawn + cr) if cr else b"") + drawing
        if len(self._line) > MAX_HELD_LINE_BYTES:
            done, self._line = done + self._line, b""
        return done

    def flush(self) -> bytes:
        """The line still held: the stream (or this file of it) ends here."""
        line, self._line = self._line, b""
        return line


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
        # Read too: a live stream a run starts later begins with what is held (`read_recent`).
        fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0o600)
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

    def read_recent(self, limit: int) -> bytes:
        """The newest ``limit`` bytes held, contiguous: the tail, and the head's end when
        nothing was dropped between them."""
        tail = b"".join(self._tail)
        if len(tail) >= limit:
            return tail[-limit:]
        if self.closed or self.total > self._head + len(tail):
            return tail
        want = min(limit - len(tail), self._head)
        head = os.pread(self._file.fileno(), want, self._head - want) if want else b""
        return head + tail

    def discard(self) -> None:
        """No one keeps this log: close it and delete the file."""
        if self.closed:
            return
        self.closed = True
        self._tail.clear()
        try:
            self._file.close()
        finally:
            with contextlib.suppress(OSError):
                os.unlink(self.path)


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


class Pump:
    """Copy each ``(src_fd, dst_fd)`` to its destination and into ``log``
    until every source ends (EOF, or EIO from a pty whose writers are gone).
    ``log`` is anything with ``write(bytes)`` (a :class:`CappedLog`), or None.

    A destination that stops accepting (the reader of a pipe exited) closes its
    SOURCE: the writer then gets EPIPE, as it would have writing there itself,
    instead of running on into a stream nobody reads. A log that fails is
    dropped and the forwarding carries on. ``stop`` ends the pump early;
    ``on_tick`` runs between reads, at least every 0.2s, and may call
    :meth:`drain` to take in what the writers have written by then.
    """

    def __init__(self, pairs, log, *, stop: threading.Event | None = None, on_tick=None):
        self.log = log
        self._stop = stop
        self._on_tick = on_tick
        self._selector = selectors.DefaultSelector()
        self._live: dict[int, int] = {}
        for src, dst in pairs:
            self._selector.register(src, selectors.EVENT_READ)
            self._live[src] = dst

    def run(self) -> None:
        try:
            while self._live:
                if self._stop is not None and self._stop.is_set():
                    return
                if self._on_tick is not None:
                    self._on_tick()
                self._step(0.2)
        finally:
            self._selector.close()

    def drain(self, quiet: float = ROTATE_QUIET_SECONDS, longest: float = ROTATE_DRAIN_SECONDS) -> None:
        """Read until nothing more arrives for ``quiet`` seconds, at most ``longest``: what the
        writers wrote before asking."""
        deadline = time.monotonic() + longest
        while self._live and time.monotonic() < deadline and self._step(quiet):
            pass

    def _step(self, timeout: float) -> bool:
        """One wait for input; True when something was read."""
        has_read = False
        for key, _ in self._selector.select(timeout=timeout):
            has_read = True
            src = key.fd
            try:
                data = os.read(src, _CHUNK)
            except OSError as exc:
                if exc.errno not in (errno.EIO, errno.EBADF):
                    raise
                data = b""
            if not data:
                self._selector.unregister(src)
                self._live.pop(src, None)
                continue
            try:
                _write_all(self._live[src], data)
            except OSError:
                self._selector.unregister(src)
                self._live.pop(src, None)
                _close(src)
            if self.log is not None:
                try:
                    self.log.write(data)
                except Exception:  # noqa: BLE001
                    # A full disk under the log must never stop the
                    # forwarding: a reader that stops reading lets the pipe
                    # fill, and the writer -- the training job -- blocks
                    # forever. Drop the log, keep the stream moving.
                    self.log = None
        return has_read


def pump(pairs, log, *, stop: threading.Event | None = None, on_tick=None) -> None:
    """:class:`Pump` run to the end."""
    Pump(pairs, log, stop=stop, on_tick=on_tick).run()


def copy_winsize(src_fd: int, dst_fd: int) -> None:
    try:
        import fcntl
        import termios

        size = fcntl.ioctl(src_fd, termios.TIOCGWINSZ, b"\0" * 8)
        fcntl.ioctl(dst_fd, termios.TIOCSWINSZ, size)
    except Exception:  # noqa: BLE001 -- a window size is cosmetic
        pass


def _close(*fds: int | None) -> None:
    for fd in fds:
        if fd is None:
            continue
        try:
            os.close(fd)
        except OSError:
            pass


def _meta_path(log_path: str) -> str:
    return log_path + ".meta.json"


def _stopped_path(log_path: str) -> str:
    return log_path + ".stopped"


def _ready_path(log_path: str) -> str:
    return log_path + ".ready"


def _adopt_path(log_path: str) -> str:
    return log_path + ".adopt"


def _get_adopted_path(log_path: str) -> str:
    return log_path + ".adopted"


def _rotate_path(log_path: str) -> str:
    return log_path + ".rotate"


def _discard_path(log_path: str) -> str:
    return log_path + ".discard"


def write_request(path: str, body: dict) -> None:
    """A control file, whole or not at all: the helper never reads half of one."""
    partial = path + ".partial"
    with open(partial, "w", encoding="utf-8") as fh:
        json.dump(body, fh)
    os.replace(partial, path)


def get_late_path(log_path: str) -> str:
    """The request a close leaves when the helper had not finished the log (T21)."""
    return log_path + ".late"


def _read_request(path: str) -> dict | None:
    """A control file's body, or None when there is none (or it was withdrawn meanwhile)."""
    try:
        with open(path, encoding="utf-8") as fh:
            body = json.load(fh)
    except (OSError, ValueError):
        return None
    with contextlib.suppress(OSError):
        os.unlink(path)
    return body if isinstance(body, dict) else {}


#: Popen keywords for a child that outlives this process and its Ctrl-C: a new
#: session on POSIX; Windows ignores that one, so a detached new process group
#: there. Inline rather than `probe.foundation.os_backend.os_backend.DETACHED`: this module also
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


def spawn_late_log(request: str) -> None:
    """The log a close sent unfinished is complete now: send the whole of it, from a normal
    interpreter, detached, like `_spawn_recovery` (`recovery.send_late_log`, which claims the
    request once)."""
    try:
        subprocess.Popen(
            [sys.executable, "-m", "probe.sdk.outputs", "--late-log", request],
            cwd=os.path.dirname(os.path.abspath(request)),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **_DETACHED,
            close_fds=True,
        )
    except Exception:  # noqa: BLE001 -- the head is still the run's log
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
    """``logs.py [--held] [--watch-parent] [--recover ENTRY] [--live DIR] LOG_PATH SRC:DST:PTY ...``
    -- the helper."""
    _ignore_signals()
    recovery_entry = None
    live_path = None
    flags: set[str] = set()
    while argv and argv[0] in ("--held", "--watch-parent", "--recover", "--live"):
        if argv[0] in ("--held", "--watch-parent"):
            flags.add(argv[0])
            argv = argv[1:]
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
    # `path`: the file being written now (a rotate moves it on). `held`: no run owns it yet, so
    # nobody asked to keep it. `recover` / `watch`: the record of the run that does own it.
    state: dict = {
        "path": log_path,
        "held": "--held" in flags,
        "recover": recovery_entry,
        "watch": "--watch-parent" in flags,
        "log": None,
        "collapse": RedrawCollapse(),
        "stop_seen": None,
        "live": None,
        "gone_reported": False,
    }
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
            log.write(state["collapse"].flush())
            log.close()
            _write_stats(log)
        except Exception:  # noqa: BLE001 -- a full disk loses the tail, not the stream
            return
        if os.path.exists(get_late_path(log.path)):
            spawn_late_log(get_late_path(log.path))  # its run's close sent only the head (T21)

    def _discard() -> None:
        _close_live()
        log, state["log"] = state["log"], None
        path = state["path"]
        if log is not None:
            with contextlib.suppress(Exception):
                log.discard()
        for marker in (_discard_path(path), _ready_path(path), _adopt_path(path), _stopped_path(path)):
            with contextlib.suppress(OSError):
                os.unlink(marker)

    def _adopt() -> None:
        path = state["path"]
        request = _read_request(_adopt_path(path))
        if request is None:
            return
        state["held"] = False
        state["recover"] = request.get("recover") or None
        state["watch"] = bool(request.get("watch_parent")) and bool(state["recover"])
        if request.get("live") and state["live"] is None and os.path.isdir(live_dir(path)):
            try:
                spool = LiveSpool(live_dir(path))
                if state["log"] is not None:
                    # The run's live view starts with the newest output held before it, at a line.
                    seed = state["log"].read_recent(LIVE_SEED_BYTES)
                    if state["log"].total > len(seed) and b"\n" in seed:
                        seed = seed[seed.index(b"\n") + 1 :]
                    spool.write(seed)
                state["live"] = spool
            except OSError:
                pass  # no spool: the live view goes without
        with contextlib.suppress(OSError):
            with open(_get_adopted_path(path), "w"):
                pass

    def _rotate(the_pump: "Pump") -> None:
        path = state["path"]
        request = _read_request(_rotate_path(path))
        if request is None or not request.get("next"):
            return
        # What the writers wrote before they asked belongs to the log being finished.
        the_pump.drain()
        _flush_log()  # its stats are the owner's ack
        state.update(
            path=str(request["next"]),
            held=True,
            recover=None,
            watch=False,
            collapse=RedrawCollapse(),
            stop_seen=None,
            gone_reported=False,
        )
        try:
            state["log"] = CappedLog(state["path"])
        except OSError:
            pass  # no log for what comes next; forwarding goes on

    def _report_gone() -> None:
        state["gone_reported"] = True
        if state["recover"]:
            _spawn_writer_gone(state["recover"])

    def _tick() -> None:
        path = state["path"]
        stopped = _stopped_path(path)
        # 2.2: the parent (the run's writer) is gone the moment we are
        # reparented, whether or not anyone still holds the streams -- a
        # grandchild keeping stdout open delays EOF forever. Checked every
        # tick (<= 0.2 s), and never after a stop: a clean close is no death.
        if (
            state["watch"]
            and not state["gone_reported"]
            and os.getppid() != parent
            and state["stop_seen"] is None
            and not os.path.exists(stopped)
        ):
            _report_gone()
        if state["held"] and os.path.exists(_adopt_path(path)):
            _adopt()
        if state["log"] is None:
            _close_live()  # a straggler's output after the log was taken is not streamed either
            return
        if os.path.exists(_discard_path(path)):
            _discard()
            return
        if state["stop_seen"] is None:
            if os.path.exists(stopped):
                state["stop_seen"] = time.monotonic()
            elif os.path.exists(_rotate_path(path)):
                _rotate(the_pump)
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
                state["log"].write(state["collapse"].push(data))
            except Exception:  # noqa: BLE001
                _flush_log()

    the_pump = Pump(pairs, _Log(), on_tick=_tick)
    try:
        the_pump.run()
    finally:
        # Before the log is handed back: once it is, the caller may clean up.
        path = state["path"]
        stopped_seen = state["stop_seen"] is not None or os.path.exists(_stopped_path(path))
        if state["held"] and os.path.exists(_adopt_path(path)):
            _adopt()  # a run took it as the writers went: it is that run's
        if os.path.exists(_discard_path(path)) or (state["held"] and not stopped_seen):
            _discard()  # no run took it, and nobody asked to keep it
        else:
            _flush_log()
    # EOF with no stop marker and the parent gone: it died mid-run (a segfault,
    # an abort, the OOM killer, a SIGTERM). Its outputs and this log are still
    # on disk, and nothing else will ever send them.
    recovery_entry = state["recover"]
    if recovery_entry and not stopped_seen and _parent_exited(parent, _stopped_path(path)):
        if state["watch"] and not state["gone_reported"]:
            _report_gone()
        _spawn_recovery(recovery_entry)
    return 0


#: Names that moved to tee.py (the owner's side), still read here by older callers and the old
#: `probe.sdk.logcapture` path.
_OWNER_SIDE = frozenset({"InProcessTee", "run_teed", "open_stream", "_Tee", "_flush_python_streams", "_flush_c_streams"})


def __getattr__(name: str):
    if name in _OWNER_SIDE:
        from . import tee  # never when run as the helper script: nothing there reads these

        return getattr(tee, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    raise SystemExit(_helper_main(sys.argv[1:]))
