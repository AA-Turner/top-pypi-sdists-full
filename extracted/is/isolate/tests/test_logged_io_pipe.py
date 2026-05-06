"""Regression tests for the pipe wiring used by `logged_io`.

Background: `_unblocked_pipe()` is consumed by `logged_io()`, where the
*read* end is drained from a reader thread (`_io_observer`) using
`select()` + `os.read()`. Only the read end needs to be non-blocking
(so the post-`select` read can never hang on a partial-line edge case).

Historically both ends were marked non-blocking. That makes the *write*
end raise `BlockingIOError` (errno EAGAIN) the moment the kernel pipe
buffer (~64 KB on Linux) fills up before the reader thread drains it —
which is exactly what happens when a worker emits a chunky traceback.
With a blocking write end, writers apply backpressure instead.
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading

import pytest
from isolate.backends.common import _unblocked_pipe, logged_io


def test_unblocked_pipe_write_end_is_blocking():
    """The write end must be blocking so that worker stdout/stderr applies
    backpressure instead of raising BlockingIOError when the pipe buffer fills."""
    read_fd, write_fd = _unblocked_pipe()
    try:
        assert not os.get_blocking(read_fd), "read end must be non-blocking"
        assert os.get_blocking(write_fd), (
            "write end must be blocking so the worker gets backpressure "
            "instead of BlockingIOError when the pipe buffer fills up"
        )
    finally:
        os.close(read_fd)
        os.close(write_fd)


def test_writing_more_than_pipe_buffer_does_not_raise_blocking_io_error():
    """Direct reproducer: write more than the kernel pipe buffer (64 KB on
    Linux) through a Python BufferedWriter on top of the pipe's write end,
    while a reader thread drains it slowly. With a non-blocking write end
    this raises `BlockingIOError`; with a blocking write end the writer
    transparently waits for the reader to make room.
    """
    read_fd, write_fd = _unblocked_pipe()
    drained = bytearray()
    drain_done = threading.Event()

    def drain():
        # Slow reader: read in small chunks with a `select` loop, mimicking
        # `_io_observer`'s pattern but slower so the pipe buffer fills up.
        import select as _select

        while not drain_done.is_set():
            ready, _, _ = _select.select([read_fd], [], [], 0.05)
            if read_fd in ready:
                try:
                    chunk = os.read(read_fd, 4096)
                except BlockingIOError:
                    continue
                if not chunk:
                    return
                drained.extend(chunk)

    reader = threading.Thread(target=drain)
    reader.start()
    try:
        # 512 KB is well past the 64 KB pipe buffer on Linux.
        payload = b"x" * (512 * 1024)
        with open(write_fd, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
        # Give the reader a moment to catch up.
        deadline_loops = 50
        while len(drained) < len(payload) and deadline_loops > 0:
            deadline_loops -= 1
            drain_done.wait(0.05)
    finally:
        drain_done.set()
        os.close(write_fd)
        reader.join(timeout=2)
        os.close(read_fd)

    assert len(drained) == len(
        payload
    ), f"reader only drained {len(drained)} of {len(payload)} bytes"


@pytest.mark.skipif(sys.platform == "win32", reason="pipes / pass_fds are POSIX-y")
def test_logged_io_subprocess_emitting_large_output_does_not_crash():
    """End-to-end reproducer mirroring how `logged_io` is used in
    `isolate.connections._local._base`: a child process writes a chunky
    payload (~256 KB) to stdout. With a non-blocking write end the child's
    Python runtime raises `BlockingIOError` when flushing stdout; with
    backpressure the child completes cleanly and the parent receives
    every line."""

    captured: list[str] = []
    lock = threading.Lock()

    def record(line: str) -> None:
        with lock:
            captured.append(line)

    n_lines = 4000
    line_template = "trace-{idx:08d}-" + ("y" * 50)
    child_script = (
        "import sys\n"
        f"for i in range({n_lines}):\n"
        f"    sys.stdout.write({line_template!r}.format(idx=i) + '\\n')\n"
        "sys.stdout.flush()\n"
    )

    with logged_io(record) as (stdout, stderr, log_fd):
        proc = subprocess.run(
            [sys.executable, "-u", "-c", child_script],
            stdout=stdout,
            stderr=stderr,
            pass_fds=(log_fd,),
            text=True,
            check=False,
        )

    assert proc.returncode == 0, (
        f"child exited with {proc.returncode}; with a non-blocking write end "
        "Python's stdout buffer raises BlockingIOError on large flushes"
    )
    # All `n_lines` should have been captured by the observer thread.
    assert len(captured) == n_lines, f"expected {n_lines} lines, got {len(captured)}"
