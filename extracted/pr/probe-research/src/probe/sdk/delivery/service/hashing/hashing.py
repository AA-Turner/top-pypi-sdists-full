"""HashPool: `files.hash` jobs (plan D20) run by at most 2 hashing children per machine (D24), each nice
10 and ionice best-effort 7 (`child.py`); the rest wait in one FIFO. A child takes a job's fds over a
socketpair and lives while jobs come, then exits after IDLE_S. Its slots are its own: hooks and
commands never wait behind a checkpoint's hash."""

from __future__ import annotations

import concurrent.futures
import contextlib
import json
import queue
import socket
import subprocess
import sys
import threading
import time
from collections.abc import Callable

from probe.foundation.service_api.start import build_module_argv, get_package_dir
from .job import HashJob

#: Hashing children per machine, at most (plan D24).
MAX_CHILDREN = 2
#: A child with no job this long exits (its thread with it).
IDLE_S = 60.0
CHILD_MODULE = "probe.sdk.delivery.service.hashing.child"
#: A child's answer is one line of at most this many bytes.
MAX_ANSWER_BYTES = 4 << 20


class HashPool:
    def __init__(self, *, log: Callable[[str], None] = lambda message: None, max_children: int = MAX_CHILDREN) -> None:
        self.log = log
        self.max_children = max_children
        self._jobs: queue.Queue = queue.Queue()
        self._lock = threading.Lock()
        self._threads: list[threading.Thread] = []
        self._busy = 0
        #: The live children's pids (`public`).
        self._pids: set[int] = set()
        self.hashed = self.expired = self.failed = 0
        self._is_closed = False

    def submit(self, job: HashJob) -> concurrent.futures.Future:
        """Queue `job`; its future answers `{results: [...]}` (per file: `sha256`/`edges`, `cut`
        or `error`), or `{expired: true}` when its deadline passed while it waited."""
        future: concurrent.futures.Future = concurrent.futures.Future()
        with self._lock:
            if self._is_closed:
                job.close()
                future.set_result({"expired": True})
                return future
            self._jobs.put((job, future))
            self._threads = [t for t in self._threads if t.is_alive()]
            if len(self._threads) < self.max_children and self._jobs.qsize() > self._count_idle_threads():
                thread = threading.Thread(target=self._run_worker, name=f"probe-hash-{len(self._threads)}", daemon=True)
                self._threads.append(thread)
                thread.start()
        return future

    def count_in_flight(self) -> int:
        """Jobs running or queued."""
        with self._lock:
            return self._busy + self._jobs.qsize()

    def _count_idle_threads(self) -> int:
        return len(self._threads) - self._busy

    def public(self) -> dict:
        with self._lock:
            return {"children": sorted(self._pids), "busy": self._busy,
                    "queued": self._jobs.qsize(), "hashed": self.hashed, "expired": self.expired,
                    "failed": self.failed}

    def close(self) -> None:
        with self._lock:
            self._is_closed = True
            threads = list(self._threads)
        for _ in threads:
            self._jobs.put(None)

    # -- one child's thread ----------------------------------------------------

    def _run_worker(self) -> None:
        child: _Child | None = None
        try:
            while True:
                try:
                    item = self._jobs.get(timeout=IDLE_S)
                except queue.Empty:
                    # M7: leave the pool under its lock first, so a job queued now either is seen
                    # here (and taken) or finds this thread gone (and starts another).
                    with self._lock:
                        if not self._jobs.empty():
                            continue
                        self._leave()
                    return
                if item is None:
                    return
                job, future = item
                if not future.set_running_or_notify_cancel():
                    job.close()  # its caller stopped waiting (the handler's timeout): skipped
                    continue
                with self._lock:
                    self._busy += 1
                try:
                    if time.monotonic() >= job.deadline:
                        job.close()
                        with self._lock:
                            self.expired += 1
                        future.set_result({"expired": True})
                        continue
                    if child is None or not child.is_alive():
                        if child is not None:
                            self._forget(child)
                        child = _Child.start()
                        with self._lock:
                            self._pids.add(child.popen.pid if hasattr(child, "popen") else id(child))
                    future.set_result({"results": child.run(job)})
                    with self._lock:
                        self.hashed += 1
                except Exception as exc:  # noqa: BLE001 -- one job's failure is its answer
                    job.close()
                    with self._lock:
                        self.failed += 1
                    self.log(f"hashing: a job failed: {type(exc).__name__}: {exc}")
                    if child is not None:
                        self._forget(child)
                        child.stop()
                        child = None
                    if not future.done():
                        future.set_result({"error": f"{type(exc).__name__}"})
                finally:
                    with self._lock:
                        self._busy -= 1
        finally:
            with self._lock:
                self._leave()
            if child is not None:
                self._forget(child)
                child.stop()

    def _leave(self) -> None:
        """This thread is no longer one of the pool's (call under the lock)."""
        current = threading.current_thread()
        self._threads = [t for t in self._threads if t is not current]

    def _forget(self, child) -> None:
        with self._lock:
            self._pids.discard(child.popen.pid if hasattr(child, "popen") else id(child))


class _Child:
    """One hashing child and this service's end of its socketpair."""

    def __init__(self, popen: subprocess.Popen, sock: socket.socket) -> None:
        self.popen = popen
        self.sock = sock
        self._buffer = b""

    @classmethod
    def start(cls) -> _Child:
        ours, theirs = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            # The service's own interpreter and code, `-I`: nothing of the caller's runs here.
            popen = subprocess.Popen(  # noqa: S603 -- our interpreter, our module
                build_module_argv(sys.executable, CHILD_MODULE, [str(theirs.fileno())], get_package_dir()),
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                pass_fds=(theirs.fileno(),), close_fds=True, start_new_session=True,
            )
        except BaseException:
            ours.close()
            raise
        finally:
            theirs.close()
        return cls(popen, ours)

    def is_alive(self) -> bool:
        return self.popen.poll() is None

    def run(self, job: HashJob) -> list[dict]:
        """Send `job` with its fds (closed here once sent: the child holds its own) and wait for
        its answer, at most until the job's deadline and a little more for the answer to come."""
        try:
            message = json.dumps({"files": job.files, "timeout": max(0.0, job.deadline - time.monotonic())})
            socket.send_fds(self.sock, [message.encode("utf-8")], job.fds)
        finally:
            job.close()
        self.sock.settimeout(max(1.0, job.deadline - time.monotonic()) + 10.0)
        while b"\n" not in self._buffer:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise ConnectionError("the hashing child exited")
            self._buffer += chunk
            if len(self._buffer) > MAX_ANSWER_BYTES:
                raise ConnectionError("the hashing child's answer is too long")
        line, self._buffer = self._buffer.split(b"\n", 1)
        answer = json.loads(line)
        if "error" in answer:
            raise ValueError(answer["error"])
        return answer["results"]

    def stop(self) -> None:
        with contextlib.suppress(OSError):
            self.sock.close()
        try:
            self.popen.wait(2.0)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(OSError):
                self.popen.kill()
            with contextlib.suppress(subprocess.TimeoutExpired):
                self.popen.wait(2.0)
