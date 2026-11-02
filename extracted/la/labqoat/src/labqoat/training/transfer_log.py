"""Milestone lines for the byte transfers a worker performs on a run's behalf."""

import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Literal

from labqoat.json_document import JsonValue
from labqoat.training.run_log_record import RunLogRecord
from labqoat.training.worker_experiment_sink import WorkerExperimentSink
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass(frozen=True)
class TransferLog:
    """Show what a quiet run is moving, how much and how fast, without ever failing the transfer itself."""

    sink: WorkerExperimentSink | None = None
    announce_bytes: int = 8 * 1024 * 1024
    announce_seconds: float = 2.0

    def note(
        self,
        message: str,
        facts: dict[str, JsonValue] | None = None,
        level: Literal["progress", "warning"] = "progress",
    ) -> None:
        """Add one line that the default run console shows."""
        if self.sink is None:
            return
        record = RunLogRecord(message[:16000], level=level, stream="milestone", data={"transfer": dict(facts or {})})
        try:
            self.sink.log_record(record)
        except WorkerApiError:
            return

    @contextmanager
    def upload(self, subject: str, byte_size: int) -> Iterator[None]:
        """Announce large uploads when they start and report every large or slow one with its rate."""
        size = self.size(byte_size)
        if byte_size >= self.announce_bytes:
            self.note(f"uploading {subject} ({size})", {"subject": subject, "bytes": byte_size, "state": "started"})
        started = time.monotonic()
        try:
            yield
        except BaseException:
            seconds = time.monotonic() - started
            facts: dict[str, JsonValue] = {"subject": subject, "bytes": byte_size, "state": "failed"}
            message = f"upload of {subject} ({size}) failed after {seconds:.1f}s"
            self.note(message, facts | {"seconds": seconds}, "warning")
            raise
        seconds = time.monotonic() - started
        if byte_size >= self.announce_bytes or seconds >= self.announce_seconds:
            facts = {"subject": subject, "bytes": byte_size, "state": "finished", "seconds": seconds}
            self.note(f"uploaded {subject} ({size}) in {seconds:.1f}s{self.rate(byte_size, seconds)}", facts)

    @staticmethod
    def size(byte_size: int) -> str:
        """Human units with one decimal below ten, matching how people read file sizes."""
        value = float(byte_size)
        for unit in ("B", "KiB", "MiB"):
            if value < 1024:
                return f"{value:.0f} {unit}" if unit == "B" or value >= 10 else f"{value:.1f} {unit}"
            value /= 1024
        return f"{value:.0f} GiB" if value >= 10 else f"{value:.1f} GiB"

    @staticmethod
    def rate(byte_size: int, seconds: float) -> str:
        """A transfer rate only where the duration is long enough to measure one."""
        if seconds < 0.5 or byte_size <= 0:
            return ""
        return f", {byte_size / 1_048_576 / seconds:.1f} MiB/s"
