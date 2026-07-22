"""Tests for the non-blocking stdout log writer.

The env server logs synchronously from its asyncio event loop. If stdout stops
draining (a node whose containerd has stopped reading the log FIFO), a plain
write() blocks and freezes the whole pod. _NonBlockingStreamWriter moves that
blocking off the caller and onto a drain thread, dropping under backpressure.
These tests exercise the actual class (not a copy) and the structlog wiring.
"""

import io
import threading
import time

from openreward.log_utils import _NonBlockingStreamWriter


class _BlockingStream:
    """A stream whose write() blocks until released -- a full pipe with no reader."""

    def __init__(self):
        self._gate = threading.Event()
        self.writes = []

    def write(self, s):
        self._gate.wait()
        self.writes.append(s)

    def flush(self):
        pass

    def release(self):
        self._gate.set()


def _drain(writer, timeout=5.0):
    deadline = time.monotonic() + timeout
    while writer._q.qsize() > 0 and time.monotonic() < deadline:
        time.sleep(0.02)
    time.sleep(0.1)


def test_writer_is_nonblocking_under_a_stalled_stream():
    # The core guarantee: the caller (the event loop, in prod) never blocks even
    # when the underlying stream is wedged forever.
    stream = _BlockingStream()
    w = _NonBlockingStreamWriter(stream, maxsize=100)
    t0 = time.monotonic()
    for i in range(5000):
        w.write(f"line {i}\n")
    elapsed = time.monotonic() - t0
    assert elapsed < 1.0, f"writes blocked ({elapsed:.2f}s): non-blocking guarantee failed"
    # Bounded queue: excess is dropped, not buffered unboundedly.
    assert w._dropped > 0
    stream.release()


def test_writer_is_lossless_and_ordered_when_healthy():
    buf = io.StringIO()
    w = _NonBlockingStreamWriter(buf, maxsize=10000)
    for i in range(2000):
        w.write(f"L{i}\n")
    _drain(w)
    lines = [ln for ln in buf.getvalue().splitlines() if ln.startswith("L")]
    assert len(lines) == 2000, f"lost lines: {len(lines)}/2000"
    assert lines[0] == "L0" and lines[-1] == "L1999", "lines out of order"
    assert w._dropped == 0


def test_writer_reports_drops_after_recovery():
    stream = _BlockingStream()
    w = _NonBlockingStreamWriter(stream, maxsize=50)
    for i in range(500):
        w.write(f"x{i}\n")
    assert w._dropped > 0
    stream.release()
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        if any("dropped" in s for s in stream.writes):
            break
        time.sleep(0.05)
    assert any("dropped" in s for s in stream.writes), "drop count not surfaced after recovery"


def test_structlog_printlogger_routes_through_the_writer():
    # log_utils wires structlog.PrintLogger(_stdout_sink()); confirm that call
    # site actually reaches the stream through the writer.
    import structlog

    buf = io.StringIO()
    w = _NonBlockingStreamWriter(buf, maxsize=10000)
    logger = structlog.PrintLogger(w)
    logger.msg("hello-from-printlogger")
    deadline = time.monotonic() + 3
    while "hello-from-printlogger" not in buf.getvalue() and time.monotonic() < deadline:
        time.sleep(0.02)
    assert "hello-from-printlogger" in buf.getvalue()
