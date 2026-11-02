"""What child processes and native code write to a worker's standard descriptors, as the input's own output."""

import codecs
import os
import select
from collections.abc import Iterator
from contextlib import contextmanager
from threading import Event, Thread
from typing import ClassVar

from labqoat.compute.output_buffer import OutputBuffer
from labqoat.run_context import RunContext


class DescriptorOutput:
    """Carry one standard descriptor into an input's output while the input runs, and drain it before it ends.

    Python's own streams are routed per input already. A child process or a native library writes to the
    descriptor itself, which reaches the run by a slower path that stops counting the moment the input is
    released, so the last lines before a failure were lost. A process the input leaves behind keeps the pipe
    open; once the input has ended, a quiet moment or the longest drain ends the wait for it.
    """

    QUIET_SECONDS: ClassVar[float] = 0.05
    DRAIN_SECONDS: ClassVar[float] = 2.0

    def __init__(self, descriptor: int, sink: OutputBuffer) -> None:
        """Name the descriptor to carry and the buffer that owns its lines."""
        self._descriptor = descriptor
        self._sink = sink
        self._ended = Event()

    @classmethod
    @contextmanager
    def captured(cls, context: RunContext) -> Iterator[None]:
        """Carry standard output and standard error for an input that has output of its own."""
        telemetry = context._telemetry
        if telemetry is None:
            yield
            return
        with cls(1, telemetry.output).installed(), cls(2, telemetry.error_output).installed():
            yield

    @contextmanager
    def installed(self) -> Iterator[None]:
        """Point the descriptor at a pipe this worker reads, then restore it and take what the pipe still holds."""
        original = os.dup(self._descriptor)
        reader, writer = os.pipe()
        os.dup2(writer, self._descriptor)
        os.close(writer)
        pump = Thread(target=self._pump, args=(reader,), daemon=True)
        pump.start()
        try:
            yield
        finally:
            os.dup2(original, self._descriptor)
            os.close(original)
            self._ended.set()
            pump.join(self.DRAIN_SECONDS)

    def _pump(self, reader: int) -> None:
        """Decode what arrives into the input's buffer until every writer is gone or the input's share is in."""
        decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        while self._readable(reader):
            chunk = os.read(reader, 65536)
            if not chunk:
                break
            self._sink.write(decoder.decode(chunk))
        os.close(reader)

    def _readable(self, reader: int) -> bool:
        """Wait for output; after the input has ended, a quiet moment means whoever holds the pipe is not it."""
        while not select.select([reader], [], [], self.QUIET_SECONDS)[0]:
            if self._ended.is_set():
                return False
        return True
