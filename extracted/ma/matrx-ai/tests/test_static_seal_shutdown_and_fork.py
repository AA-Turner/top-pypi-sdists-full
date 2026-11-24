"""Two process-edge guards for the static seal: no false failure alarm at shutdown, and a forked child
never inherits a held lock. The send path is untouched by both."""

from __future__ import annotations

import os
import subprocess
import sys
import textwrap
import threading
import time

from matrx_ai.providers import final_outbound_snapshot as fos


def test_no_failure_report_once_shutdown_has_begun(monkeypatch) -> None:
    said: list[str] = []
    monkeypatch.setattr(fos.logger, "error", lambda *a, **k: said.append(str(a)))
    monkeypatch.setattr(fos, "_FAILED", set())
    monkeypatch.setattr(fos, "_close_worker_at_exit", fos._close_worker_at_exit)
    # Never kill the run's shared worker: _close_worker_at_exit SIGKILLs _WORKER and leaves the dead
    # handle, so the next seal test in the process found it down and fingerprinted nothing
    # (test_static_seal_worker_process "seal only", red in the full suite since 50b80f96af7).
    monkeypatch.setattr(fos, "_WORKER", None)
    try:
        fos._close_worker_at_exit()  # what atexit runs first: flips the shutdown flag
        fos._say_failure("seal worker", RuntimeError("cut off by exit"))
        assert said == []
    finally:
        fos._SHUTTING_DOWN[0] = False
    fos._say_failure("seal worker", RuntimeError("real failure"))
    assert said, "outside shutdown a failure is still reported"


def test_a_job_in_flight_at_exit_prints_no_alarm() -> None:
    code = textwrap.dedent(
        """
        from matrx_ai.providers import final_outbound_snapshot as fos
        import atexit
        # a dispatcher-style failure arriving after atexit began (worker closed under the job)
        atexit.register(lambda: (fos._close_worker_at_exit(), fos._say_failure("seal worker", RuntimeError("worker closed"))))
        """
    )
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60)
    assert "failed (the send proceeds" not in r.stdout + r.stderr


def test_a_forked_child_gets_fresh_locks_and_takes_them_within_a_second() -> None:
    if not hasattr(os, "fork"):
        return
    held = threading.Event()
    release = threading.Event()

    def holder() -> None:
        with fos._LOCK, fos._DISPATCHER_GUARD, fos._CHECK_LOCK:
            held.set()
            release.wait(10)

    t = threading.Thread(target=holder)
    t.start()
    assert held.wait(5)
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        ok = b"0"
        try:
            deadline = time.monotonic() + 1
            for lock in (fos._LOCK, fos._DISPATCHER_GUARD, fos._CHECK_LOCK):
                if not lock.acquire(timeout=max(0.01, deadline - time.monotonic())):
                    ok = b"1"
                    break
                lock.release()
        finally:
            os.write(w, ok)
            os._exit(0)
    os.close(w)
    got = os.read(r, 1)
    os.waitpid(pid, 0)
    release.set()
    t.join()
    assert got == b"0", "child could not take an inherited lock within 1 s"
