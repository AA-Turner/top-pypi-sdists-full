"""THE STATIC SEAL'S ONE WORKER PROCESS — fingerprint work never runs in the server process.

Why a process (2026-11-13): fingerprinting in server worker THREADS stalled the event loop
160-240 ms under load — ``json.loads`` of large bodies triggered full garbage collections that froze
every thread, plus interpreter-lock contention. A child process has its own interpreter lock and its
own garbage collector: nothing it does can pause the server's event loop.

What the child runs: ``final_outbound_snapshot.worker_job`` — pure functions over plain data (the
body bytes, the seal stamp, the parse limit, the residual check's known texts and patterns). It never
touches the server's state; the parent compares the returned short hashes (``check_and_remember``).

What the child imports: the stdlib, ``matrx_ai.providers.final_outbound_snapshot`` (stdlib only at
import), ``matrx_ai.providers.residual_check`` (stdlib only) and, for an xAI job only, the request's
proto module. Never the server app: it is started with ``python -c`` (no ``__main__`` re-import, unlike
``multiprocessing``'s spawn, which would re-run ``run.py``'s top level in the child).

Protocol: length-prefixed pickles over the child's stdin/stdout, one job at a time. The child runs at a
lowest CPU priority (Linux ``SCHED_IDLE``, else ``nice`` 19), in its own session (a terminal Ctrl-C never reaches it), and exits
when its stdin closes (the server process ended). Anything it prints goes to stderr.
"""

from __future__ import annotations

import os
import pickle
import select
import struct
import subprocess
import sys
import time
from typing import Any

_HEADER = struct.Struct("!Q")
_READ_CHUNK = 1 << 20

#: Started with ``python -c``: reads the parent's ``sys.path`` (first frame), then serves.
_BOOT = (
    "import pickle, struct, sys\n"
    "_n = struct.unpack('!Q', sys.stdin.buffer.read(8))[0]\n"
    "sys.path[:] = pickle.loads(sys.stdin.buffer.read(_n))\n"
    "from matrx_ai.providers.seal_worker import serve\n"
    "serve()\n"
)


class WorkerGone(Exception):
    """The worker process died, closed its pipe, or did not answer in time."""


# ---------------------------------------------------------------------------
# Child side
# ---------------------------------------------------------------------------


def _yield_the_cpu() -> None:
    """The worker runs only on CPU time the server is not using: Linux ``SCHED_IDLE`` (it never
    preempts a server thread), else ``nice`` 19. A courtesy: failure changes nothing else."""
    try:
        os.sched_setscheduler(0, os.SCHED_IDLE, os.sched_param(0))  # type: ignore[attr-defined]
        return
    except Exception:  # noqa: BLE001
        pass
    try:
        os.nice(19)
    except Exception:  # noqa: BLE001
        pass


def serve() -> None:
    """The child's loop: read a job, run it, write the result. Returns on EOF (the parent is gone)."""
    import signal

    try:
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    except Exception:  # noqa: BLE001
        pass
    _yield_the_cpu()
    inp = sys.stdin.buffer
    out = sys.stdout.buffer
    sys.stdout = sys.stderr  # a stray print never corrupts the channel
    job_fn = None
    while True:
        header = inp.read(_HEADER.size)
        if len(header) < _HEADER.size:
            return
        (size,) = _HEADER.unpack(header)
        data = inp.read(size)
        if len(data) < size:
            return
        try:
            if job_fn is None:
                from matrx_ai.providers.final_outbound_snapshot import worker_job

                job_fn = worker_job
            result: Any = job_fn(pickle.loads(data))
        except BaseException as exc:  # noqa: BLE001 — a failed job is an answer, never a dead worker
            result = {"error": f"{type(exc).__name__}: {exc}"}
        del data
        try:
            payload = pickle.dumps(result, protocol=pickle.HIGHEST_PROTOCOL)
        except BaseException as exc:  # noqa: BLE001
            payload = pickle.dumps({"error": f"result not picklable: {type(exc).__name__}"})
        out.write(_HEADER.pack(len(payload)))
        out.write(payload)
        out.flush()


# ---------------------------------------------------------------------------
# Parent side
# ---------------------------------------------------------------------------


def _ready(fd: int, event: int, timeout: float) -> bool:
    """Wait for ``fd`` with ``poll`` (``select.select`` refuses descriptors numbered 1024 and up, and a
    busy server holds thousands of sockets). A hang-up or error counts as ready: the read or write
    that follows reports it."""
    poller = select.poll()
    poller.register(fd, event)
    return bool(poller.poll(max(timeout, 0.0) * 1000.0))


def _widen_pipe(fd: int) -> None:
    """Linux: a pipe as large as allowed (up to 1 MB), so a typical body crosses in ONE write — each
    wake-up of the dispatcher thread is an interpreter-lock hand-off the event loop may wait on."""
    try:
        import fcntl

        size = 1 << 20
        try:
            with open("/proc/sys/fs/pipe-max-size") as limit:
                size = min(size, int(limit.read().strip()))
        except Exception:  # noqa: BLE001
            pass
        fcntl.fcntl(fd, fcntl.F_SETPIPE_SZ, size)
    except Exception:  # noqa: BLE001 — a smaller pipe only costs more wake-ups
        pass


class WorkerProcess:
    """One child process. ``call`` is used from ONE server thread at a time (the seal dispatcher)."""

    def __init__(self) -> None:
        self.proc = subprocess.Popen(  # noqa: S603 — our own interpreter, our own boot code
            [sys.executable, "-c", _BOOT],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
            bufsize=0,
            close_fds=True,
            start_new_session=True,
        )
        try:
            assert self.proc.stdin is not None and self.proc.stdout is not None
            self._in = self.proc.stdin.fileno()
            self._out = self.proc.stdout.fileno()
            for fd in (self._in, self._out):
                _widen_pipe(fd)
            os.set_blocking(self._in, False)
            path = pickle.dumps([p for p in sys.path if isinstance(p, str)])
            self._write(_HEADER.pack(len(path)), time.monotonic() + 30)
            self._write(path, time.monotonic() + 30)
        except BaseException:
            self.close()  # never leave the child behind (one per restart window)
            raise

    @property
    def pid(self) -> int:
        return int(self.proc.pid)

    def alive(self) -> bool:
        return self.proc.poll() is None

    def call(self, job: Any, timeout: float) -> Any:
        """Send one job, wait for its answer. Raises ``WorkerGone`` on death, EOF or timeout."""
        deadline = time.monotonic() + timeout
        data = pickle.dumps(job, protocol=pickle.HIGHEST_PROTOCOL)
        self._write(_HEADER.pack(len(data)), deadline)
        self._write(data, deadline)
        del data
        (size,) = _HEADER.unpack(self._read(_HEADER.size, deadline))
        return pickle.loads(self._read(size, deadline))

    def _write(self, data: bytes, deadline: float) -> None:
        view = memoryview(data)
        while view:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise WorkerGone("timed out writing a job")
            if not _ready(self._in, select.POLLOUT, remaining):
                continue
            try:
                written = os.write(self._in, view)
            except BlockingIOError:
                continue
            except OSError as exc:  # BrokenPipeError: the child is gone
                raise WorkerGone(f"pipe closed: {exc}") from exc
            view = view[written:]

    def _read(self, size: int, deadline: float) -> bytes:
        buf = bytearray()
        while len(buf) < size:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise WorkerGone("timed out waiting for a result")
            if not _ready(self._out, select.POLLIN, remaining):
                continue
            chunk = os.read(self._out, min(size - len(buf), _READ_CHUNK))
            if not chunk:
                raise WorkerGone(f"worker exited (code {self.proc.poll()})")
            buf += chunk
        return bytes(buf)

    def close(self) -> None:
        """Stop the child (never raises, never waits long)."""
        try:
            self.proc.kill()
        except Exception:  # noqa: BLE001
            pass
        for stream in (self.proc.stdin, self.proc.stdout):
            try:
                if stream is not None:
                    stream.close()
            except Exception:  # noqa: BLE001
                pass
        try:
            self.proc.wait(timeout=2)
        except Exception:  # noqa: BLE001
            pass


__all__ = ["WorkerGone", "WorkerProcess", "serve"]
