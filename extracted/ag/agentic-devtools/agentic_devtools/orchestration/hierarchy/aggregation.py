"""Rolling-window SLO aggregation and operator-alert evaluation (NFR-002, NFR-003).

Persists per-run outcome records for two independent production SLOs:

- **Trace completeness** (NFR-002): whether a run's trace reached a
  ``workflow_completed`` event, over a rolling 30-day window with at least
  100 started runs. The denominator includes crashes, hangs, trace
  failures, and runs without ``workflow_completed``; only explicitly
  recorded external cancellations/aborts are excluded.
- **Degradation success** (NFR-003): whether an *eligible* FR-015
  degradation run completed successfully within 10 minutes, over a rolling
  30-day window with at least 100 eligible runs. FR-014-invalid rejections
  are never eligible and are excluded from both numerator and denominator;
  explicit cancellations/aborts are also excluded. Crashes, hangs,
  time-exceeded completions, and failures ARE included in the denominator.

Both aggregations expose an ``evaluate_alert`` helper that returns an
actionable operator alert only once the minimum sample size is met and the
rolling rate falls below 99%.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import IO, cast

from agentic_devtools.file_locking import locked_file
from agentic_devtools.orchestration.hierarchy.protected_storage import (
    ProtectedStorage,
    resolve_authorized_principals,
    resolve_master_key,
)

_ROLLING_WINDOW_DAYS = 30
_MIN_RUNS_FOR_ALERT = 100
_ALERT_THRESHOLD = 0.99
_DEGRADATION_TIME_LIMIT_SECONDS = 10 * 60
_DEGRADATION_STALE_RUN_THRESHOLD = timedelta(seconds=_DEGRADATION_TIME_LIMIT_SECONDS)
# A started run with no terminal record is only classified as a hang/failure
# once it has been in-flight longer than this threshold.  Runs started more
# recently than this are still considered active and are excluded from rate
# calculations to avoid depressing the SLO during concurrent activity.
_STALE_RUN_THRESHOLD = timedelta(hours=4)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _parse_iso(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt


@dataclass(frozen=True)
class TraceCompletenessRecord:
    """One production run's trace-completeness outcome for NFR-002."""

    run_id: str
    timestamp: str
    complete: bool  # True iff workflow_completed was emitted
    explicitly_cancelled: bool = False

    @property
    def counts_toward_denominator(self) -> bool:
        return not self.explicitly_cancelled

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "complete": self.complete,
            "explicitly_cancelled": self.explicitly_cancelled,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> TraceCompletenessRecord:
        run_id = data.get("run_id")
        timestamp = data.get("timestamp")
        complete = data.get("complete")
        explicitly_cancelled = data.get("explicitly_cancelled", False)
        if not isinstance(run_id, str):
            raise ValueError("run_id must be a string")
        if not isinstance(timestamp, str):
            raise ValueError("timestamp must be a string")
        if not isinstance(complete, bool):
            raise ValueError("complete must be a boolean")
        if not isinstance(explicitly_cancelled, bool):
            raise ValueError("explicitly_cancelled must be a boolean")
        return cls(
            run_id=run_id,
            timestamp=timestamp,
            complete=complete,
            explicitly_cancelled=explicitly_cancelled,
        )


@dataclass(frozen=True)
class DegradationRecord:
    """One production run's FR-015 degradation eligibility/outcome for NFR-003."""

    run_id: str
    timestamp: str
    eligible: bool  # False for FR-014-invalid rejections (never counted)
    successful: bool  # crashes/hangs/time-exceeded/failures are NOT successful
    elapsed_seconds: float = 0.0
    explicitly_cancelled: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.elapsed_seconds, bool) or not isinstance(self.elapsed_seconds, (int, float)):
            raise ValueError("elapsed_seconds must be numeric")
        if self.elapsed_seconds < 0:
            raise ValueError("elapsed_seconds must be non-negative")

    @property
    def within_time_limit(self) -> bool:
        return self.elapsed_seconds <= _DEGRADATION_TIME_LIMIT_SECONDS

    @property
    def counts_toward_denominator(self) -> bool:
        return self.eligible and not self.explicitly_cancelled

    @property
    def counts_as_success(self) -> bool:
        return self.counts_toward_denominator and self.successful and self.within_time_limit

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "eligible": self.eligible,
            "successful": self.successful,
            "elapsed_seconds": self.elapsed_seconds,
            "explicitly_cancelled": self.explicitly_cancelled,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> DegradationRecord:
        run_id = data.get("run_id")
        timestamp = data.get("timestamp")
        eligible = data.get("eligible")
        successful = data.get("successful")
        raw_elapsed = data.get("elapsed_seconds", 0.0)
        explicitly_cancelled = data.get("explicitly_cancelled", False)
        if not isinstance(run_id, str):
            raise ValueError("run_id must be a string")
        if not isinstance(timestamp, str):
            raise ValueError("timestamp must be a string")
        if not isinstance(eligible, bool):
            raise ValueError("eligible must be a boolean")
        if not isinstance(successful, bool):
            raise ValueError("successful must be a boolean")
        if isinstance(raw_elapsed, bool) or not isinstance(raw_elapsed, (int, float)):
            raise ValueError("elapsed_seconds must be numeric")
        if not isinstance(explicitly_cancelled, bool):
            raise ValueError("explicitly_cancelled must be a boolean")
        return cls(
            run_id=run_id,
            timestamp=timestamp,
            eligible=eligible,
            successful=successful,
            elapsed_seconds=float(cast(float, raw_elapsed)),
            explicitly_cancelled=explicitly_cancelled,
        )


@dataclass(frozen=True)
class AlertEvaluation:
    """The result of evaluating a rolling-window rate against the 99% SLO threshold."""

    slo_name: str
    sample_size: int
    rate: float | None
    alert: bool
    message: str | None


def _append_record(path: Path, record_dict: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with locked_file(path, mode="a", encoding="utf-8") as handle:
        file_handle = cast(IO[str], handle)
        file_handle.write(json.dumps(record_dict, sort_keys=True) + "\n")


def _read_records(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    with locked_file(path, mode="r", exclusive=False, encoding="utf-8") as handle:
        file_handle = cast(IO[str], handle)
        return _parse_records(file_handle)


def _parse_records(lines: Iterable[str]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        try:
            record = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict) or not isinstance(record.get("timestamp"), str):
            continue
        try:
            _parse_iso(record["timestamp"])
        except (TypeError, ValueError):
            continue
        records.append(record)
    return records


def _within_window(records: Iterable[dict[str, object]], now: datetime) -> list[dict[str, object]]:
    cutoff = now - timedelta(days=_ROLLING_WINDOW_DAYS)
    return [r for r in records if cutoff <= _parse_iso(str(r["timestamp"])) <= now]


def _started_trace_runs(records: Iterable[dict[str, object]]) -> dict[str, tuple[bool, str]]:
    started: dict[str, tuple[bool, str]] = {}
    for record in records:
        if record.get("phase") != "started":
            continue
        run_id = record.get("run_id")
        if not isinstance(run_id, str):
            continue
        timestamp = record.get("timestamp")
        if not isinstance(timestamp, str):
            continue  # pragma: no cover — _read_records pre-validates timestamps
        explicitly_cancelled_val = record.get("explicitly_cancelled", False)
        if not isinstance(explicitly_cancelled_val, bool):
            continue
        started[run_id] = (explicitly_cancelled_val, timestamp)
    return started


def _started_degradation_runs(records: Iterable[dict[str, object]]) -> dict[str, tuple[bool, bool, str]]:
    started: dict[str, tuple[bool, bool, str]] = {}
    for record in records:
        if record.get("phase") != "started":
            continue
        run_id = record.get("run_id")
        if not isinstance(run_id, str):
            continue
        timestamp = record.get("timestamp")
        if not isinstance(timestamp, str):
            continue  # pragma: no cover — _read_records pre-validates timestamps
        eligible_val = record.get("eligible", True)
        if not isinstance(eligible_val, bool):
            continue
        explicitly_cancelled_val = record.get("explicitly_cancelled", False)
        if not isinstance(explicitly_cancelled_val, bool):
            continue
        started[run_id] = (eligible_val, explicitly_cancelled_val, timestamp)
    return started


def _terminal_trace_records_by_run(records: Iterable[dict[str, object]]) -> dict[str, TraceCompletenessRecord]:
    terminal: dict[str, TraceCompletenessRecord] = {}
    for record in records:
        if record.get("phase", "terminal") != "terminal":
            continue
        try:
            parsed = TraceCompletenessRecord.from_dict(record)
        except ValueError:
            continue
        terminal[parsed.run_id] = parsed
    return terminal


def _terminal_degradation_records_by_run(records: Iterable[dict[str, object]]) -> dict[str, DegradationRecord]:
    terminal: dict[str, DegradationRecord] = {}
    for record in records:
        if record.get("phase", "terminal") != "terminal":
            continue
        try:
            parsed = DegradationRecord.from_dict(record)
        except ValueError:
            continue
        terminal[parsed.run_id] = parsed
    return terminal


def append_trace_completeness_started(
    history_path: Path,
    *,
    run_id: str,
    explicitly_cancelled: bool = False,
    timestamp: str | None = None,
) -> None:
    """Persist the start of a production run for NFR-002 lifecycle accounting."""
    _append_record(
        history_path,
        {
            "run_id": run_id,
            "timestamp": timestamp or _now_iso(),
            "phase": "started",
            "explicitly_cancelled": explicitly_cancelled,
        },
    )


def append_trace_completeness_record(
    history_path: Path,
    *,
    run_id: str,
    complete: bool,
    explicitly_cancelled: bool = False,
    timestamp: str | None = None,
) -> None:
    """Persist one run's NFR-002 trace-completeness outcome."""
    record = TraceCompletenessRecord(
        run_id=run_id,
        timestamp=timestamp or _now_iso(),
        complete=complete,
        explicitly_cancelled=explicitly_cancelled,
    )
    _append_record(history_path, record.to_dict())


def rolling_trace_completeness_rate(history_path: Path, *, now: datetime | None = None) -> tuple[float | None, int]:
    """Return ``(rate, denominator_size)`` for the rolling 30-day NFR-002 window."""
    now = now or datetime.now(UTC)
    records_in_window = list(_within_window(_read_records(history_path), now))
    started_runs = _started_trace_runs(records_in_window)
    terminal_by_run = _terminal_trace_records_by_run(records_in_window)
    candidates: list[TraceCompletenessRecord] = []
    for run_id in set(started_runs) | set(terminal_by_run):
        terminal = terminal_by_run.get(run_id)
        if terminal is None:
            # run_id is in started_runs when it has no terminal record (guaranteed by set union logic)
            explicitly_cancelled, start_ts = started_runs[run_id]
            # Only classify an unterminated start as hung/failed after the stale
            # threshold; runs still within it are considered actively running.
            try:
                if (now - _parse_iso(start_ts)) < _STALE_RUN_THRESHOLD:
                    continue
            except (ValueError, TypeError):  # pragma: no cover — _read_records pre-validates timestamps
                pass
            candidates.append(
                TraceCompletenessRecord(
                    run_id=run_id,
                    timestamp=now.isoformat(),
                    complete=False,
                    explicitly_cancelled=explicitly_cancelled,
                )
            )
            continue
        candidates.append(terminal)
    denominator = [record for record in candidates if record.counts_toward_denominator]
    if not denominator:
        return None, 0
    numerator = sum(1 for r in denominator if r.complete)
    return numerator / len(denominator), len(denominator)


def evaluate_trace_completeness_alert(history_path: Path, *, now: datetime | None = None) -> AlertEvaluation:
    """Evaluate the NFR-002 operator alert: rate < 99% over >= 100 started runs."""
    rate, size = rolling_trace_completeness_rate(history_path, now=now)
    if size < _MIN_RUNS_FOR_ALERT or rate is None:
        return AlertEvaluation("trace_completeness", size, rate, alert=False, message=None)
    if rate < _ALERT_THRESHOLD:
        return AlertEvaluation(
            "trace_completeness",
            size,
            rate,
            alert=True,
            message=f"Trace completeness fell to {rate:.4f} over {size} runs (below 99% NFR-002 threshold)",
        )
    return AlertEvaluation("trace_completeness", size, rate, alert=False, message=None)


def append_degradation_record(
    history_path: Path,
    *,
    run_id: str,
    eligible: bool,
    successful: bool,
    elapsed_seconds: float = 0.0,
    explicitly_cancelled: bool = False,
    timestamp: str | None = None,
) -> None:
    """Persist one run's NFR-003 degradation eligibility/outcome."""
    record = DegradationRecord(
        run_id=run_id,
        timestamp=timestamp or _now_iso(),
        eligible=eligible,
        successful=successful,
        elapsed_seconds=elapsed_seconds,
        explicitly_cancelled=explicitly_cancelled,
    )
    _append_record(history_path, record.to_dict())


def append_degradation_started(
    history_path: Path,
    *,
    run_id: str,
    eligible: bool = True,
    explicitly_cancelled: bool = False,
    timestamp: str | None = None,
) -> None:
    """Persist the start of an eligible degradation run for NFR-003 accounting."""
    _append_record(
        history_path,
        {
            "run_id": run_id,
            "timestamp": timestamp or _now_iso(),
            "phase": "started",
            "eligible": eligible,
            "explicitly_cancelled": explicitly_cancelled,
        },
    )


def rolling_degradation_success_rate(history_path: Path, *, now: datetime | None = None) -> tuple[float | None, int]:
    """Return ``(rate, denominator_size)`` for the rolling 30-day NFR-003 window."""
    now = now or datetime.now(UTC)
    records_in_window = list(_within_window(_read_records(history_path), now))
    started_runs = _started_degradation_runs(records_in_window)
    terminal_by_run = _terminal_degradation_records_by_run(records_in_window)
    candidates: list[DegradationRecord] = []
    for run_id in set(started_runs) | set(terminal_by_run):
        terminal = terminal_by_run.get(run_id)
        if terminal is None:
            # run_id is in started_runs when it has no terminal record (guaranteed by set union logic)
            eligible, explicitly_cancelled, start_ts = started_runs[run_id]
            # Only classify an unterminated start as hung/failed after the stale
            # threshold; runs still within it are considered actively running.
            try:
                if (now - _parse_iso(start_ts)) < _DEGRADATION_STALE_RUN_THRESHOLD:
                    continue
            except (ValueError, TypeError):  # pragma: no cover — _read_records pre-validates timestamps
                pass
            candidates.append(
                DegradationRecord(
                    run_id=run_id,
                    timestamp=now.isoformat(),
                    eligible=eligible,
                    successful=False,
                    explicitly_cancelled=explicitly_cancelled,
                )
            )
            continue
        candidates.append(terminal)
    denominator = [record for record in candidates if record.counts_toward_denominator]
    if not denominator:
        return None, 0
    numerator = sum(1 for r in denominator if r.counts_as_success)
    return numerator / len(denominator), len(denominator)


def evaluate_degradation_alert(history_path: Path, *, now: datetime | None = None) -> AlertEvaluation:
    """Evaluate the NFR-003 operator alert: rate < 99% over >= 100 eligible runs."""
    rate, size = rolling_degradation_success_rate(history_path, now=now)
    if size < _MIN_RUNS_FOR_ALERT or rate is None:
        return AlertEvaluation("degradation_success", size, rate, alert=False, message=None)
    if rate < _ALERT_THRESHOLD:
        return AlertEvaluation(
            "degradation_success",
            size,
            rate,
            alert=True,
            message=(
                f"Degradation success rate fell to {rate:.4f} over {size} eligible runs (below 99% NFR-003 threshold)"
            ),
        )
    return AlertEvaluation("degradation_success", size, rate, alert=False, message=None)


def append_retention_record(
    registry_path: Path,
    *,
    run_id: str,
    trace_path: str,
    expires_at: str,
    timestamp: str | None = None,
) -> None:
    """Persist a bounded retention record for a newly created trace (≤30-day deletion policy)."""
    _append_record(
        registry_path,
        {
            "run_id": run_id,
            "trace_path": trace_path,
            "expires_at": expires_at,
            "timestamp": timestamp or _now_iso(),
        },
    )


def _has_existing_symlink_component(path: Path) -> bool:
    """Return True when any existing component of ``path`` is a symlink."""
    return any(component.exists() and component.is_symlink() for component in (path, *path.parents))


def _resolve_canonical_trace_path(registry_path: Path, *, run_id: str, trace_path: str) -> Path | None:
    """Resolve and validate a registry trace path against the canonical layout."""
    hierarchy_dir = registry_path.parent
    if _has_existing_symlink_component(registry_path) or _has_existing_symlink_component(hierarchy_dir):
        return None
    candidate = Path(trace_path)
    if not candidate.is_absolute():
        return None
    expected = hierarchy_dir / run_id / "trace.ndjson"
    try:
        hierarchy_root = hierarchy_dir.resolve(strict=False)
        expected_resolved = expected.resolve(strict=False)
        candidate_resolved = candidate.resolve(strict=False)
    except OSError:
        return None
    try:
        expected_resolved.relative_to(hierarchy_root)
        candidate_resolved.relative_to(hierarchy_root)
    except ValueError:
        return None
    if candidate_resolved != expected_resolved:
        return None
    if _has_existing_symlink_component(candidate) or _has_existing_symlink_component(expected):
        return None
    return expected_resolved


def cleanup_expired_retention(
    registry_path: Path,
    *,
    master_key: bytes,
    authorized_principals: frozenset[str],
    now: datetime | None = None,
) -> tuple[str, ...]:
    """Delete expired trace files and compact the retention registry.

    Scans the retention registry for records whose ``expires_at`` timestamp has
    passed, deletes each expired trace file via ``ProtectedStorage.delete()``,
    removes expired entries from the registry, and returns the ``run_id`` values
    of cleaned-up runs.
    """
    if not registry_path.exists():
        return ()
    current = now or datetime.now(UTC)
    surviving: list[dict[str, object]] = []
    removed_run_ids: list[str] = []
    with locked_file(registry_path, mode="r+", exclusive=True, encoding="utf-8") as handle:
        file_handle = cast(IO[str], handle)
        records = _parse_records(file_handle)
        for record in records:
            expires_at_raw = record.get("expires_at")
            if not isinstance(expires_at_raw, str):
                surviving.append(record)
                continue
            try:
                expires_dt = _parse_iso(expires_at_raw)
            except (ValueError, TypeError):
                surviving.append(record)
                continue
            if current < expires_dt:
                surviving.append(record)
                continue
            run_id_val = record.get("run_id")
            trace_path_str = record.get("trace_path")
            if isinstance(trace_path_str, str):
                if not isinstance(run_id_val, str):
                    surviving.append(record)
                    continue
                trace_file = _resolve_canonical_trace_path(
                    registry_path,
                    run_id=run_id_val,
                    trace_path=trace_path_str,
                )
                if trace_file is None:
                    surviving.append(record)
                    continue
                if trace_file.exists():
                    try:
                        storage = ProtectedStorage(
                            trace_file,
                            master_key=master_key,
                            authorized_principals=authorized_principals,
                        )
                        storage.delete()
                    except Exception:
                        surviving.append(record)
                        continue
            if isinstance(run_id_val, str):
                removed_run_ids.append(run_id_val)
        if len(surviving) < len(records):
            file_handle.seek(0)
            file_handle.write("".join(json.dumps(rec, sort_keys=True) + "\n" for rec in surviving))
            file_handle.truncate()
    return tuple(removed_run_ids)


def cleanup_workflow_retention(
    registry_path: Path,
    *,
    master_key: bytes | None = None,
    authorized_principals: frozenset[str] | None = None,
) -> tuple[str, ...]:
    """Delete retained traces for workflow deletion via protected-storage authorization."""
    if not registry_path.exists():
        return ()
    resolved_master_key = master_key
    resolved_authorized_principals = authorized_principals
    should_remove_registry = False
    removed_run_ids: list[str] = []
    surviving: list[dict[str, object]] = []
    with locked_file(registry_path, mode="r+", exclusive=True, encoding="utf-8") as handle:
        file_handle = cast(IO[str], handle)
        records = _parse_records(file_handle)
        for record in records:
            run_id = record.get("run_id")
            trace_path = record.get("trace_path")
            if isinstance(trace_path, str):
                if not isinstance(run_id, str):
                    surviving.append(record)
                    continue
                trace_file = _resolve_canonical_trace_path(
                    registry_path,
                    run_id=run_id,
                    trace_path=trace_path,
                )
                if trace_file is None:
                    surviving.append(record)
                    continue
                try:
                    if trace_file.exists():
                        if resolved_master_key is None:
                            resolved_master_key = resolve_master_key()
                        if resolved_authorized_principals is None:
                            resolved_authorized_principals = resolve_authorized_principals()
                        storage = ProtectedStorage(
                            trace_file,
                            master_key=resolved_master_key,
                            authorized_principals=resolved_authorized_principals,
                        )
                        storage.delete()
                except Exception:
                    surviving.append(record)
                    continue
            if isinstance(run_id, str):
                removed_run_ids.append(run_id)
        if surviving:
            file_handle.seek(0)
            file_handle.write("".join(json.dumps(rec, sort_keys=True) + "\n" for rec in surviving))
            file_handle.truncate()
        else:
            file_handle.seek(0)
            file_handle.truncate()
            should_remove_registry = True
    if should_remove_registry:
        try:
            registry_path.unlink()
        except FileNotFoundError:
            pass
    return tuple(removed_run_ids)
