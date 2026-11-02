"""Explicit process-lifetime standard streams with invocation-local assignment bindings."""

import sys
from collections.abc import Iterator
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from contextvars import ContextVar

from labqoat.compute.context_output import ContextOutput
from labqoat.compute.logging_routing import LoggingRouting
from labqoat.compute.run_telemetry import RunTelemetry
from labqoat.run_context import RunContext


class OutputRouting:
    """Install proxies once per physical worker and scope credentials to each executing task."""

    def __init__(self) -> None:
        """Create routing state owned by this worker rather than a process-global singleton."""
        self._sinks: ContextVar[tuple[RunTelemetry, ...]] = ContextVar("labqoat_output", default=())

    @contextmanager
    def installed(self) -> Iterator["OutputRouting"]:
        """Restore original streams even when worker execution is interrupted."""
        with (
            LoggingRouting(self._sinks).installed(),
            redirect_stdout(ContextOutput(self._sinks, sys.stdout)),
            redirect_stderr(ContextOutput(self._sinks, sys.stderr, "stderr")),
        ):
            yield self

    @contextmanager
    def bind(self, contexts: list[RunContext]) -> Iterator[None]:
        """Propagate input ownership through async tasks and asyncio.to_thread calls."""
        sinks = tuple(context._telemetry for context in contexts if context._telemetry is not None)
        token = self._sinks.set(sinks)
        try:
            yield
        finally:
            self._sinks.reset(token)
            for sink in sinks:
                sink.flush_output()
