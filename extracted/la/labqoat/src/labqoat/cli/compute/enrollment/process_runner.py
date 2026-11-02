"""Run local ssh and docker processes with captured output and bounded duration."""

from __future__ import annotations

import subprocess
from collections.abc import Sequence

from labqoat.cli.compute.enrollment.command_result import CommandResult


class ProcessRunner:
    """Execute argument vectors without a local shell; substitute a fake in tests."""

    def __init__(self, timeout_seconds: float = 1800.0) -> None:
        """Bound each process so an unreachable host cannot hang enrollment forever."""
        self._timeout = timeout_seconds

    def run(self, args: Sequence[str], stdin: bytes | None = None) -> CommandResult:
        """Run one process, feeding optional standard input."""
        completed = subprocess.run(list(args), input=stdin, capture_output=True, check=False, timeout=self._timeout)
        return CommandResult(completed.returncode, completed.stdout, completed.stderr)

    def pipe(self, producer: Sequence[str], consumer: Sequence[str]) -> CommandResult:
        """Stream the producer's output into the consumer, failing if either side fails."""
        with subprocess.Popen(list(producer), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as source:
            with subprocess.Popen(
                list(consumer), stdin=source.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ) as sink:
                if source.stdout is not None:
                    source.stdout.close()
                output, sink_error = sink.communicate(timeout=self._timeout)
            source_error = source.stderr.read() if source.stderr is not None else b""
            source.wait(timeout=self._timeout)
        status = source.returncode or sink.returncode
        return CommandResult(status, output, source_error + sink_error)
