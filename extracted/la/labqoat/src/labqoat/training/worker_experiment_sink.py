"""Durable platform telemetry for an authenticated training assignment."""

import json
from threading import Lock

from labqoat.json_document import JsonValue
from labqoat.training.metric_batch import MetricBatch
from labqoat.training.run_log_record import RunLogRecord
from labqoat.training.telemetry_unavailable_error import TelemetryUnavailableError
from labqoat.worker import WorkerApi
from labqoat.worker.worker_api_error import WorkerApiError


class WorkerExperimentSink:
    """Store step metrics and retain hyperparameters in the run's log evidence."""

    def __init__(self, api: WorkerApi) -> None:
        """Bind telemetry to one explicit assignment API."""
        self._api = api
        self._sequence = 0
        self._log_lock = Lock()

    def log_hyperparameters(self, parameters: tuple[tuple[str, str], ...]) -> None:
        """Retain the exact parameters that the framework actually logged."""
        self._log("training.hyperparameters=" + json.dumps(dict(parameters), separators=(",", ":"), sort_keys=True))

    def log_metrics(self, batch: MetricBatch) -> None:
        """Queue immutable metrics under their original optimizer or epoch step."""
        entries: list[JsonValue] = [{"step": batch.step, "name": name, "value": value} for name, value in batch.metrics]
        try:
            self._api.buffer_telemetry("metrics", entries)
        except WorkerApiError as error:
            if error.status is not None and error.status < 500 and error.status not in {408, 429}:
                raise
            raise TelemetryUnavailableError("Training metric delivery failed") from error

    @property
    def sequence(self) -> int:
        """The number the next log of this assignment gets."""
        return self._sequence

    def resume_from(self, sequence: int) -> None:
        """Number logs after those an earlier sink of the same assignment already delivered."""
        with self._log_lock:
            self._sequence = max(self._sequence, sequence)

    def finalize(self, status: str) -> None:
        """Retain framework completion without changing the platform run state."""
        self._log(f"training.framework.finalized status={status}")
        self.flush()

    def flush(self) -> None:
        """Confirm every accepted log and metric before a caller crosses a delivery barrier."""
        self._api.flush_telemetry()

    def _log(self, content: str) -> None:
        """Queue ordered log evidence with replay-stable sequence numbers."""
        self.log_text(content)

    def log_text(self, content: str) -> None:
        """Serialize framework and standard-output evidence using one assignment sequence."""
        self.log_record(RunLogRecord(content))

    def log_record(self, record: RunLogRecord) -> None:
        """Freeze producer metadata before transport retries and share the assignment sequence."""
        entry = record.to_dict()
        with self._log_lock:
            entry["seq"] = self._sequence
            self._api.buffer_telemetry("logs", [entry])
            self._sequence += 1
