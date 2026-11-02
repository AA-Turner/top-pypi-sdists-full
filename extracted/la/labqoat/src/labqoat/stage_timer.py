"""Ordered stage timing evidence for managed Python workload execution."""

from __future__ import annotations

import sys
import time
from contextlib import contextmanager
from collections.abc import Iterator
from typing import TextIO


class StageTimer:
    """Emit one line per named stage with its step and cumulative duration when a stream is bound."""

    def __init__(self, stream: TextIO | None = None) -> None:
        """Bind an optional output stream and start this workload's monotonic origin."""
        self._stream = stream
        self._origin = time.monotonic()
        self._previous = self._origin

    @classmethod
    def stderr(cls) -> StageTimer:
        """Bind the workload's standard error so machine results keep standard output."""
        return cls(sys.stderr)

    @contextmanager
    def span(self, name: str, detail: str = "") -> Iterator[None]:
        """Record one stage, with optional attribution, even when the wrapped operation raises."""
        try:
            yield
        finally:
            self.stage(name, detail)

    def stage(self, name: str, detail: str = "") -> None:
        """Record one completed stage, emitting its step and total milliseconds."""
        now = time.monotonic()
        stream = self._stream
        if stream is not None:
            step = (now - self._previous) * 1000
            total = (now - self._origin) * 1000
            fields = f"stage={name}" if detail == "" else f"stage={name} detail={detail}"
            stream.write(f"LABQOAT_TIMING {fields} step_ms={step:.1f} total_ms={total:.1f}\n")
            stream.flush()
        self._previous = now

    def finish(self) -> None:
        """Record the whole workload after its final stage."""
        self.stage("total")
