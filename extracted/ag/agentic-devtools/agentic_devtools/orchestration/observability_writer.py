"""Thread-safe JSONL event writer for observability logs.

Writes one JSON object per line to an append-mode file under
``<state_dir>/observability/run-{run_id}.jsonl``.  Failures during
initialization or writing are swallowed with a stderr warning —
observability never crashes the workflow.

Event sequencing is managed by ``WorkflowRun``; this writer only handles
serialization and file I/O.
"""

from __future__ import annotations

import json
import sys
import threading
from pathlib import Path
from typing import IO, Any

from agentic_devtools.orchestration.execution.run_id import validate_run_id


class EventWriter:
    """Thread-safe append-mode JSONL writer.

    On init failure (invalid run_id, permission error, etc.) the writer
    degrades to no-op mode with a warning on stderr.  Write-time errors
    are also caught and reported via stderr without re-raising.
    """

    def __init__(self, run_id: str, state_dir: str | Path) -> None:
        self._lock = threading.Lock()
        self._file: IO[str] | None = None
        self._log_path: Path | None = None
        self._degraded = False

        try:
            validated_id = validate_run_id(run_id)
            obs_dir = Path(state_dir) / "observability"
            obs_dir.mkdir(parents=True, exist_ok=True)
            self._log_path = obs_dir / f"run-{validated_id}.jsonl"
            self._file = open(self._log_path, "a", encoding="utf-8")  # noqa: SIM115
        except Exception as exc:  # noqa: BLE001
            self._degraded = True
            print(
                f"[observability] WARNING: Failed to initialize log writer: {exc}",
                file=sys.stderr,
            )

    @property
    def log_path(self) -> Path | None:
        """Return the resolved log file path, if one was computed."""
        return self._log_path

    @property
    def degraded(self) -> bool:
        """Return True if the writer is in no-op mode."""
        return self._degraded

    def write(self, event: dict[str, Any]) -> None:
        """Serialize and append an event as a single JSON line.

        All errors (serialization and I/O) are caught and reported
        via stderr without propagating to the caller.  After the first
        write failure the writer permanently degrades to no-op mode
        to prevent repeated stderr spam and stale file-handle retries.
        """
        with self._lock:
            if self._degraded or self._file is None:
                return
            try:
                line = json.dumps(event, default=str)
                self._file.write(line + "\n")
                self._file.flush()
            except Exception as exc:  # noqa: BLE001
                print(
                    f"[observability] WARNING: Failed to write event: {exc}",
                    file=sys.stderr,
                )
                # Degrade permanently so subsequent calls are silent no-ops.
                self._degraded = True
                try:
                    self._file.close()
                except Exception:  # noqa: BLE001
                    pass
                self._file = None

    def close(self) -> None:
        """Idempotently close the underlying file handle."""
        with self._lock:
            if self._file is not None:
                try:
                    self._file.close()
                except Exception:  # noqa: BLE001
                    pass
                self._file = None
