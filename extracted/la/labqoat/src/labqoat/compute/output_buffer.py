"""Bounded line assembly for assignment-owned standard output."""

import re
from threading import RLock
from datetime import UTC, datetime
from typing import ClassVar, Literal

from labqoat.training.worker_experiment_sink import WorkerExperimentSink
from labqoat.training.run_log_record import RunLogRecord


class OutputBuffer:
    """Queue complete lines promptly and flush partial lines before finalization."""

    LIMIT: ClassVar[int] = 16_000

    def __init__(self, sink: WorkerExperimentSink, stream: Literal["stdout", "stderr"] = "stdout") -> None:
        """Share the assignment's ordered log sequence with framework telemetry."""
        self._sink = sink
        self._pending = ""
        self._lock = RLock()
        self._stream = stream
        self._produced_at: datetime | None = None

    def write(self, text: str) -> None:
        """Keep each line whole up to ``LIMIT`` characters, under the server's 16,384; split only longer ones."""
        with self._lock:
            for index, part in enumerate(re.split(r"[\r\n]", text)):
                if index:
                    self.flush()
                self._append(part)

    def _append(self, part: str) -> None:
        """Add a piece of one line, publishing a full record whenever the line reaches the limit."""
        while part:
            if not self._pending:
                self._produced_at = datetime.now(UTC)
            room = self.LIMIT - len(self._pending)
            self._pending += part[:room]
            part = part[room:]
            if len(self._pending) >= self.LIMIT:
                self.flush()

    def flush(self) -> None:
        """Publish nonempty fragments under a single ordered assignment-owned sink."""
        with self._lock:
            if self._pending.strip():
                self._sink.log_record(RunLogRecord(self._pending, stream=self._stream, produced_at=self._produced_at))
            self._pending = ""
            self._produced_at = None
