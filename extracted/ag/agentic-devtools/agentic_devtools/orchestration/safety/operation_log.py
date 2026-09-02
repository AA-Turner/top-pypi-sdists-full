"""Operation log for idempotent external mutations (FR-005).

Append-only NDJSON log that tracks every external mutation's lifecycle
(pending → completed/failed/skipped). Provides O(1) lookup by operation_id
within the current run_id scope.
"""

from __future__ import annotations

import dataclasses
import json
import logging
import threading
from pathlib import Path
from typing import Any

from agentic_devtools.file_locking import locked_file

logger = logging.getLogger(__name__)

_LOG_FILENAME = "operation-log.ndjson"


@dataclasses.dataclass(frozen=True)
class OperationLogRecord:
    """A single operation log entry (FR-005).

    Attributes:
        operation_id: Deterministic ID from compute_operation_id().
        run_id: The agdt_run_id scoping this record.
        tool_name: Name of the tool invoked.
        node_name: The graph node that invoked the tool.
        input_hash: SHA-256 prefix of canonical inputs (for debugging).
        execution_timestamp: ISO-8601 timestamp of the operation.
        execution_mode: The mode under which the operation ran.
        status: One of "pending", "completed", "failed", "skipped".
        result_summary: Brief description of the outcome.
        skip_reason: Why the operation was skipped (for skipped records).
        override_reason: Why a safety override was applied.
        result_payload: The full result for replay on duplicate-skip.
        prior_completion_timestamp: Timestamp of the prior completed record
            (present on skipped-duplicate records for audit traceability).
    """

    operation_id: str
    run_id: str
    tool_name: str
    node_name: str = ""
    input_hash: str = ""
    execution_timestamp: str = ""
    execution_mode: str = ""
    status: str = ""
    result_summary: str = ""
    skip_reason: str | None = None
    override_reason: str | None = None
    result_payload: Any = None
    prior_completion_timestamp: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary for NDJSON persistence."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OperationLogRecord:
        """Deserialize from a dictionary."""
        # Only pass known fields to avoid TypeError on extra keys
        known_fields = {f.name for f in dataclasses.fields(cls)}
        filtered = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered)


class OperationLog:
    """NDJSON-backed operation log with in-memory index (FR-005).

    The log file lives at ``<state_dir>/operation-log.ndjson``.
    The in-memory index is scoped to the current ``run_id`` and uses
    last-wins semantics for duplicate operation_ids.
    """

    def __init__(self, state_dir: Path, run_id: str) -> None:
        self._log_path = state_dir / _LOG_FILENAME
        self._run_id = run_id
        self._index: dict[str, OperationLogRecord] = {}
        self._index_lock = threading.Lock()
        self._build_index()

    @property
    def log_path(self) -> Path:
        """Return the path to the operation log file."""
        return self._log_path

    @property
    def run_id(self) -> str:
        """Return the current run ID."""
        return self._run_id

    def lookup(self, operation_id: str) -> OperationLogRecord | None:
        """Look up the latest record for an operation in the current run.

        Returns None if no record exists for this operation_id in the
        current run_id scope.
        """
        with self._index_lock:
            return self._index.get(operation_id)

    def append(self, record: OperationLogRecord) -> None:
        """Append a record to the log file and update the in-memory index.

        Uses file locking for atomic append. Only indexes records matching
        the current run_id.
        """
        self._log_path.parent.mkdir(parents=True, exist_ok=True)

        line = json.dumps(record.to_dict(), separators=(",", ":"), default=str) + "\n"

        # Append mode with exclusive lock
        try:
            with locked_file(self._log_path, mode="a", exclusive=True) as f:
                f.write(line)
        except FileNotFoundError:
            # Parent dir may have been removed between mkdir and open — recreate
            # and append.  Use locked_file (not plain open) to preserve the
            # atomic append-only NDJSON contract (NFR-002).
            self._log_path.parent.mkdir(parents=True, exist_ok=True)
            with locked_file(self._log_path, mode="a", exclusive=True) as f:
                f.write(line)

        # Update in-memory index if this record matches our run_id.
        # Pop before reinserting so that the insertion order reflects last-seen
        # semantics (plain dict assignment does not move an existing key).
        if record.run_id == self._run_id:
            with self._index_lock:
                self._index.pop(record.operation_id, None)
                self._index[record.operation_id] = record

    def all_records(self) -> list[OperationLogRecord]:
        """Return all indexed records for the current run_id."""
        with self._index_lock:
            return list(self._index.values())

    def _build_index(self) -> None:
        """Parse the NDJSON log and build the in-memory index.

        Skips corrupted lines with warnings. Only indexes records
        matching the current run_id (last-wins semantics).
        """
        if not self._log_path.exists():
            return

        try:
            content = self._log_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            logger.warning("Failed to read operation log %s: %s", self._log_path, exc)
            return

        for line_num, line in enumerate(content.splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                record = OperationLogRecord.from_dict(data)
                if record.run_id == self._run_id:
                    # Pop before reinserting so that insertion order reflects
                    # last-seen semantics for each operation_id in the file.
                    with self._index_lock:
                        self._index.pop(record.operation_id, None)
                        self._index[record.operation_id] = record
            except (json.JSONDecodeError, TypeError, KeyError) as exc:
                logger.warning(
                    "Skipping corrupted line %d in operation log: %s",
                    line_num,
                    exc,
                )

    def get_timestamp(self) -> str:
        """Return current ISO-8601 timestamp for record creation."""
        from datetime import datetime, timezone

        return datetime.now(tz=timezone.utc).isoformat()
