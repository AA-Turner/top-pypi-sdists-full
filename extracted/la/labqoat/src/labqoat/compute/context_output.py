"""Context-local output routing for concurrent worker tasks and their input threads."""

from contextvars import ContextVar
from io import TextIOBase
from typing import TextIO, Literal

from labqoat.compute.run_telemetry import RunTelemetry


class ContextOutput(TextIOBase):
    """Use task-local assignment sinks while leaving unassigned runtime output on its original stream."""

    def __init__(
        self,
        sinks: ContextVar[tuple[RunTelemetry, ...]],
        fallback: TextIO,
        stream: Literal["stdout", "stderr"] = "stdout",
    ) -> None:
        """Retain an explicit routing context shared by the worker's stdout and stderr proxies."""
        self._sinks = sinks
        self._fallback = fallback
        self._stream = stream

    def write(self, text: str) -> int:
        """Attribute a shared batch message separately through every participating input's authority."""
        sinks = self._sinks.get()
        if not sinks:
            return self._fallback.write(text)
        for sink in sinks:
            output = sink.error_output if self._stream == "stderr" else sink.output
            output.write(text)
        return len(text)

    def flush(self) -> None:
        """Flush active assignment fragments or the ordinary process stream."""
        sinks = self._sinks.get()
        if not sinks:
            self._fallback.flush()
        for sink in sinks:
            output = sink.error_output if self._stream == "stderr" else sink.output
            output.flush()

    def fileno(self) -> int:
        """The process's own descriptor, which libraries such as vLLM redirect; the worker captures what it gets."""
        return self._fallback.fileno()

    def isatty(self) -> bool:
        """Whether the process's own stream is a terminal."""
        return self._fallback.isatty()
