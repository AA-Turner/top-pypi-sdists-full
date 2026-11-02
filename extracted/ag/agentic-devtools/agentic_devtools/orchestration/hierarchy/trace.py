"""FR-012 trace event schema and append-only NDJSON persistence.

Provides the twelve normative ``TraceEventType`` values, conditional
``event_detail`` validation for each event type, and validated append-only
UTF-8 NDJSON persistence for the orchestration workflow trace file.

Traces are the diagnostic backbone of User Story 4: every discovery,
spawn, injection, handoff, review, violation, failure, degradation,
conflict, and completion event must be reconstructable from the trace
file alone.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, cast

from agentic_devtools.file_locking import locked_file

from .scopes import AgentScopeLevel

if TYPE_CHECKING:
    from .protected_storage import ProtectedStorage

_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
_SAFE_RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class TraceValidationError(ValueError):
    """Raised when a trace event fails FR-012 schema validation."""


class TraceEventType:
    """The twelve normative FR-012 event types."""

    HIERARCHY_DISCOVERY = "hierarchy_discovery"
    AGENT_CREATED = "agent_created"
    FILE_BOUNDARY_ESTABLISHED = "file_boundary_established"
    CONTEXT_INJECTED = "context_injected"
    HANDOFF = "handoff"
    REVIEW_DECISION = "review_decision"
    SCOPE_VIOLATION = "scope_violation"
    AGENT_FAILURE = "agent_failure"
    DEGRADATION = "degradation"
    CONFLICT_DETECTED = "conflict_detected"
    CONFLICT_RESOLVED = "conflict_resolved"
    WORKFLOW_COMPLETED = "workflow_completed"

    ALL: frozenset[str] = frozenset(
        {
            HIERARCHY_DISCOVERY,
            AGENT_CREATED,
            FILE_BOUNDARY_ESTABLISHED,
            CONTEXT_INJECTED,
            HANDOFF,
            REVIEW_DECISION,
            SCOPE_VIOLATION,
            AGENT_FAILURE,
            DEGRADATION,
            CONFLICT_DETECTED,
            CONFLICT_RESOLVED,
            WORKFLOW_COMPLETED,
        }
    )


_VALID_SCOPES = {level.value for level in AgentScopeLevel}


def utc_timestamp() -> str:
    """Return the current time as an FR-012-compliant ISO-8601 UTC timestamp."""
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _require_no_newlines(value: Any, field_name: str) -> None:
    if isinstance(value, str) and ("\n" in value or "\r" in value):
        msg = f"Field '{field_name}' must not contain literal newline characters"
        raise TraceValidationError(msg)


def _require_keys(detail: dict[str, Any], keys: set[str], event_type: str) -> None:
    missing = keys - detail.keys()
    if missing:
        msg = f"event_detail for '{event_type}' is missing required keys: {sorted(missing)}"
        raise TraceValidationError(msg)


def _validate_hierarchy_discovery(detail: dict[str, Any]) -> None:
    _require_keys(detail, {"outcome", "levels_found", "error"}, TraceEventType.HIERARCHY_DISCOVERY)
    if detail["outcome"] not in ("success", "partial", "failed"):
        raise TraceValidationError("hierarchy_discovery.outcome must be success|partial|failed")
    if not isinstance(detail["levels_found"], list):
        raise TraceValidationError("hierarchy_discovery.levels_found must be a list")
    if detail["error"] is not None and not isinstance(detail["error"], str):
        raise TraceValidationError("hierarchy_discovery.error must be a string or null")


_CLASSIFICATION_SOURCES = {
    "planning_artifact",
    "secondary_issue_or_diff",
    "discovery_candidate_list",
    "exhausted_sources",
    "not_applicable",
}
_CLASSIFICATION_OUTCOMES = {"classified", "discovery_only_unclassified", "not_applicable"}
_SPECIALIZATION_STATUSES = {
    "specialized_supported",
    "general_unsupported_or_binary",
    "general_discovery_unclassified",
    "not_applicable",
}


def _validate_agent_created(detail: dict[str, Any]) -> None:
    required = {
        "agent_id",
        "scope_level",
        "file_boundary",
        "classification_source",
        "classification_outcome",
        "discovery_only",
        "specialization_status",
    }
    _require_keys(detail, required, TraceEventType.AGENT_CREATED)
    if detail["scope_level"] not in ("epic", "feature", "subtask"):
        raise TraceValidationError("agent_created.scope_level must be epic|feature|subtask")
    if not isinstance(detail["file_boundary"], list):
        raise TraceValidationError("agent_created.file_boundary must be a list")
    if detail["classification_source"] not in _CLASSIFICATION_SOURCES:
        raise TraceValidationError("agent_created.classification_source is invalid")
    if detail["classification_outcome"] not in _CLASSIFICATION_OUTCOMES:
        raise TraceValidationError("agent_created.classification_outcome is invalid")
    if not isinstance(detail["discovery_only"], bool):
        raise TraceValidationError("agent_created.discovery_only must be a boolean")
    if detail["specialization_status"] not in _SPECIALIZATION_STATUSES:
        raise TraceValidationError("agent_created.specialization_status is invalid")

    scope_level = detail["scope_level"]
    if scope_level in ("epic", "feature"):
        if detail["classification_source"] != "not_applicable" or detail["classification_outcome"] != "not_applicable":
            raise TraceValidationError(
                "agent_created: epic/feature scopes must use not_applicable classification fields"
            )
        if detail["discovery_only"] is not False:
            raise TraceValidationError("agent_created: epic/feature scopes must have discovery_only=false")
        if detail["specialization_status"] != "not_applicable":
            raise TraceValidationError(
                "agent_created: epic/feature scopes must have specialization_status=not_applicable"
            )
    else:  # subtask
        if detail["classification_source"] == "not_applicable" or detail["classification_outcome"] == "not_applicable":
            raise TraceValidationError(
                "agent_created: subtask scopes must not use not_applicable classification fields"
            )
        if detail["specialization_status"] == "not_applicable":
            raise TraceValidationError(
                "agent_created: subtask scopes must not use not_applicable specialization_status"
            )
        expected_discovery_only = detail["classification_outcome"] == "discovery_only_unclassified"
        if detail["discovery_only"] != expected_discovery_only:
            raise TraceValidationError(
                "agent_created.discovery_only must be true iff classification_outcome is discovery_only_unclassified"
            )
        if detail["classification_outcome"] == "discovery_only_unclassified":
            if detail["classification_source"] != "exhausted_sources":
                raise TraceValidationError(
                    "agent_created: discovery_only_unclassified requires classification_source=exhausted_sources"
                )
            if detail["specialization_status"] != "general_discovery_unclassified":
                raise TraceValidationError(
                    "agent_created: discovery_only_unclassified requires "
                    "specialization_status=general_discovery_unclassified"
                )


def _validate_file_boundary_established(detail: dict[str, Any]) -> None:
    required = {"agent_id", "source_discovery_agent_id", "previous_boundary", "granted_paths"}
    _require_keys(detail, required, TraceEventType.FILE_BOUNDARY_ESTABLISHED)
    if detail["previous_boundary"] != []:
        raise TraceValidationError("file_boundary_established.previous_boundary must be []")
    if not isinstance(detail["granted_paths"], list) or not detail["granted_paths"]:
        raise TraceValidationError("file_boundary_established.granted_paths must be a non-empty list")


def _validate_context_injected(detail: dict[str, Any]) -> None:
    required = {"agent_id", "fields_injected", "field_content_refs", "trusted"}
    _require_keys(detail, required, TraceEventType.CONTEXT_INJECTED)
    if detail["trusted"] is not False:
        raise TraceValidationError("context_injected.trusted must be false")
    if not isinstance(detail["fields_injected"], list):
        raise TraceValidationError("context_injected.fields_injected must be a list")
    refs = detail["field_content_refs"]
    if not isinstance(refs, dict):
        raise TraceValidationError("context_injected.field_content_refs must be an object")
    if set(refs.keys()) != set(detail["fields_injected"]):
        raise TraceValidationError("context_injected.field_content_refs keys must match fields_injected exactly")
    for field_name, ref in refs.items():
        if not isinstance(ref, dict) or "content_sha256" not in ref:
            raise TraceValidationError(f"context_injected field ref for '{field_name}' missing content_sha256")
        snapshot_ref = ref.get("snapshot_ref")
        locator_type = ref.get("locator_type")
        locator_value = ref.get("locator_value")
        if snapshot_ref is None:
            if locator_type is None or locator_value is None:
                raise TraceValidationError(
                    f"context_injected field ref for '{field_name}': "
                    "locator_type/value required when snapshot_ref is null"
                )


def _validate_handoff(detail: dict[str, Any]) -> None:
    _require_keys(detail, {"from_agent_id", "to_agent_id", "outcome"}, TraceEventType.HANDOFF)
    for field_name in ("from_agent_id", "to_agent_id", "outcome"):
        value = detail[field_name]
        if not isinstance(value, str) or not value:
            raise TraceValidationError(f"handoff.{field_name} must be a non-empty string; got {value!r}")


def _validate_review_decision(detail: dict[str, Any]) -> None:
    required = {"agent_id", "verdict", "requirement_ref", "violation_ref", "corrective_action"}
    _require_keys(detail, required, TraceEventType.REVIEW_DECISION)
    if detail["verdict"] not in ("approved", "rejected", "revision_requested"):
        raise TraceValidationError("review_decision.verdict is invalid")
    if detail["verdict"] in ("rejected", "revision_requested"):
        if detail["violation_ref"] is None or detail["corrective_action"] is None:
            raise TraceValidationError(
                "review_decision: violation_ref and corrective_action are required for rejected/revision_requested"
            )


def _validate_scope_violation(detail: dict[str, Any]) -> None:
    _require_keys(detail, {"agent_id", "attempted_path", "enforcement"}, TraceEventType.SCOPE_VIOLATION)
    if detail["enforcement"] != "blocked":
        raise TraceValidationError("scope_violation.enforcement must be 'blocked'")


_FAILURE_PHASES = {"initial", "retry", "post_retry"}
_ATTEMPT_OUTCOMES = {"failed", "recovered"}
_RECOVERY_MODES = {"checkpoint_restore", "persisted_checkpoint_resume", None}


def _validate_agent_failure(detail: dict[str, Any]) -> None:
    required = {
        "agent_id",
        "failure_reason",
        "retry_attempt",
        "failure_phase",
        "attempt_outcome",
        "recovery_mode",
        "recovered",
        "terminal_cleanup",
        "disposition",
    }
    _require_keys(detail, required, TraceEventType.AGENT_FAILURE)
    if detail["retry_attempt"] not in (0, 1):
        raise TraceValidationError("agent_failure.retry_attempt must be 0 or 1")
    if detail["failure_phase"] not in _FAILURE_PHASES:
        raise TraceValidationError("agent_failure.failure_phase is invalid")
    if detail["attempt_outcome"] not in _ATTEMPT_OUTCOMES:
        raise TraceValidationError("agent_failure.attempt_outcome is invalid")
    if detail["recovery_mode"] not in _RECOVERY_MODES:
        raise TraceValidationError("agent_failure.recovery_mode is invalid")
    if not isinstance(detail["recovered"], bool):
        raise TraceValidationError("agent_failure.recovered must be a boolean")
    cleanup = detail["terminal_cleanup"]
    if cleanup is not None:
        if not isinstance(cleanup, dict) or "action" not in cleanup or "outcome" not in cleanup:
            raise TraceValidationError("agent_failure.terminal_cleanup is malformed")
        if cleanup["action"] not in ("checkpoint_restore", "discard_unverified_state"):
            raise TraceValidationError("agent_failure.terminal_cleanup.action is invalid")
        if cleanup["outcome"] not in ("success", "failed"):
            raise TraceValidationError("agent_failure.terminal_cleanup.outcome is invalid")
        if cleanup["outcome"] == "failed" and detail["disposition"] is not None:
            raise TraceValidationError(
                "agent_failure.disposition must be null when terminal_cleanup outcome is 'failed'"
            )


def _validate_degradation(detail: dict[str, Any]) -> None:
    _require_keys(detail, {"reason", "missing_level", "resulting_topology"}, TraceEventType.DEGRADATION)
    if not isinstance(detail["resulting_topology"], list):
        raise TraceValidationError("degradation.resulting_topology must be a list")


def _validate_conflict_detected(detail: dict[str, Any]) -> None:
    required = {"conflicting_agent_ids", "contested_paths", "proposed_edit_summaries"}
    _require_keys(detail, required, TraceEventType.CONFLICT_DETECTED)
    if not isinstance(detail["conflicting_agent_ids"], list):
        raise TraceValidationError("conflict_detected.conflicting_agent_ids must be a list")
    if not isinstance(detail["contested_paths"], list):
        raise TraceValidationError("conflict_detected.contested_paths must be a list")
    if not isinstance(detail["proposed_edit_summaries"], dict):
        raise TraceValidationError("conflict_detected.proposed_edit_summaries must be an object")


def _validate_conflict_resolved(detail: dict[str, Any]) -> None:
    required = {"resolution_authority", "contested_paths", "granted_paths", "resolution_decision"}
    _require_keys(detail, required, TraceEventType.CONFLICT_RESOLVED)
    if not isinstance(detail["granted_paths"], dict):
        raise TraceValidationError("conflict_resolved.granted_paths must be an object")
    contested = set(detail["contested_paths"])
    seen: set[str] = set()
    for agent_id, paths in detail["granted_paths"].items():
        if not isinstance(paths, list):
            raise TraceValidationError(f"conflict_resolved.granted_paths['{agent_id}'] must be a list")
        for path in paths:
            if path in seen:
                raise TraceValidationError(f"conflict_resolved: path '{path}' granted to more than one agent")
            seen.add(path)
    if contested and contested != seen:
        raise TraceValidationError("conflict_resolved: every contested_path must be granted to exactly one agent")


def _validate_workflow_completed(detail: dict[str, Any]) -> None:
    required = {"outcome", "agents_completed", "agents_skipped", "final_disposition"}
    _require_keys(detail, required, TraceEventType.WORKFLOW_COMPLETED)
    if detail["outcome"] not in ("success", "partial", "failed"):
        raise TraceValidationError("workflow_completed.outcome must be success|partial|failed")
    if not isinstance(detail["agents_completed"], list) or not isinstance(detail["agents_skipped"], list):
        raise TraceValidationError("workflow_completed agent lists must be lists")


_VALIDATORS = {
    TraceEventType.HIERARCHY_DISCOVERY: _validate_hierarchy_discovery,
    TraceEventType.AGENT_CREATED: _validate_agent_created,
    TraceEventType.FILE_BOUNDARY_ESTABLISHED: _validate_file_boundary_established,
    TraceEventType.CONTEXT_INJECTED: _validate_context_injected,
    TraceEventType.HANDOFF: _validate_handoff,
    TraceEventType.REVIEW_DECISION: _validate_review_decision,
    TraceEventType.SCOPE_VIOLATION: _validate_scope_violation,
    TraceEventType.AGENT_FAILURE: _validate_agent_failure,
    TraceEventType.DEGRADATION: _validate_degradation,
    TraceEventType.CONFLICT_DETECTED: _validate_conflict_detected,
    TraceEventType.CONFLICT_RESOLVED: _validate_conflict_resolved,
    TraceEventType.WORKFLOW_COMPLETED: _validate_workflow_completed,
}


@dataclass(frozen=True)
class TraceEvent:
    """A single FR-012 trace event.

    Attributes:
        event_type: One of ``TraceEventType.ALL``.
        agent_scope: One of ``epic``, ``feature``, ``subtask``, ``orchestrator``.
        event_detail: Event-type-specific structured payload.
        timestamp: ISO-8601 UTC timestamp; generated automatically when omitted.
    """

    event_type: str
    agent_scope: str
    event_detail: dict[str, Any]
    timestamp: str = ""
    _timestamp_auto_assigned: bool = field(init=False, repr=False, compare=False, default=False)

    def __post_init__(self) -> None:
        if self.event_type not in TraceEventType.ALL:
            msg = f"Unknown event_type: {self.event_type!r}"
            raise TraceValidationError(msg)
        if self.agent_scope not in _VALID_SCOPES:
            msg = f"Unknown agent_scope: {self.agent_scope!r}"
            raise TraceValidationError(msg)
        auto_assigned = not self.timestamp
        timestamp = self.timestamp or utc_timestamp()
        object.__setattr__(self, "timestamp", timestamp)
        object.__setattr__(self, "_timestamp_auto_assigned", auto_assigned)
        if not timestamp:  # pragma: no cover - utc_timestamp() never returns empty
            raise TraceValidationError("timestamp must not be empty")
        if not _TIMESTAMP_RE.match(timestamp):
            msg = f"timestamp is not valid ISO-8601 with UTC offset: {timestamp!r}"
            raise TraceValidationError(msg)
        try:
            _parse_event_timestamp(timestamp)
        except ValueError as exc:
            msg = f"timestamp is not valid ISO-8601 with UTC offset: {timestamp!r}"
            raise TraceValidationError(msg) from exc
        if self.event_detail is None:
            raise TraceValidationError("event_detail MUST NOT be null")
        if not isinstance(self.event_detail, dict):
            msg = f"event_detail MUST be an object/dict, got {type(self.event_detail).__name__!r}"
            raise TraceValidationError(msg)
        if self.event_type == TraceEventType.FILE_BOUNDARY_ESTABLISHED and self.agent_scope != "orchestrator":
            raise TraceValidationError("file_boundary_established events MUST use agent_scope='orchestrator'")
        _VALIDATORS[self.event_type](self.event_detail)
        _scan_for_newlines(self.event_detail)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to the JSON-safe dict written to the NDJSON trace file."""
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "agent_scope": self.agent_scope,
            "event_detail": self.event_detail,
        }


def _scan_for_newlines(value: Any) -> None:
    if isinstance(value, str):
        _require_no_newlines(value, "event_detail")
    elif isinstance(value, dict):
        for v in value.values():
            _scan_for_newlines(v)
    elif isinstance(value, list):
        for v in value:
            _scan_for_newlines(v)


def serialize_event(event: TraceEvent) -> str:
    """Serialize a ``TraceEvent`` to a single NDJSON line (no trailing newline)."""
    return json.dumps(event.to_dict(), ensure_ascii=False, sort_keys=False, separators=(",", ":"))


def _serialize_event_with_timestamp(event: TraceEvent, timestamp: str) -> str:
    event_dict = event.to_dict()
    event_dict["timestamp"] = timestamp
    return json.dumps(event_dict, ensure_ascii=False, sort_keys=False, separators=(",", ":"))


def _last_event_timestamp(content: str) -> datetime | None:
    """Return the timestamp of the last valid NDJSON event in *content*, or ``None``."""
    for line in reversed(content.splitlines()):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            event = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        ts = event.get("timestamp")
        if isinstance(ts, str):
            try:
                dt = datetime.fromisoformat(ts)
                return dt if dt.tzinfo is not None else dt.replace(tzinfo=UTC)
            except ValueError:
                continue
    return None


def _parse_event_timestamp(timestamp: str) -> datetime:
    parsed = datetime.fromisoformat(timestamp)
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


def _format_trace_timestamp(timestamp: datetime) -> str:
    return timestamp.astimezone(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _effective_timestamp_for_append(event: TraceEvent, last_timestamp: datetime | None) -> str:
    """Return a lock-safe timestamp for this append.

    Explicit caller-provided timestamps are validated strictly. Auto-assigned
    timestamps may be advanced under lock to preserve monotonic ordering across
    concurrent appenders.
    """
    if last_timestamp is None:
        return event.timestamp

    new_timestamp = _parse_event_timestamp(event.timestamp)
    if new_timestamp >= last_timestamp:
        return event.timestamp

    if not event._timestamp_auto_assigned:
        msg = (
            f"out-of-order trace event: {event.timestamp!r} precedes last recorded timestamp "
            f"{last_timestamp.isoformat()!r}"
        )
        raise TraceValidationError(msg)

    assigned = datetime.now(UTC)
    minimum_next = last_timestamp + timedelta(milliseconds=1)
    if assigned < minimum_next:
        assigned = minimum_next
    return _format_trace_timestamp(assigned)


def _truncate_malformed_trailing_record(file_handle: IO[str], content: str) -> str:
    """Drop a malformed final non-blank NDJSON record from in-memory *content* and file."""
    lines = content.splitlines(keepends=True)
    if not lines:
        return content

    last_non_blank_index: int | None = None
    for index in range(len(lines) - 1, -1, -1):
        if lines[index].strip():
            last_non_blank_index = index
            break
    if last_non_blank_index is None:
        return content

    candidate = lines[last_non_blank_index].strip()
    try:
        json.loads(candidate)
        return content
    except json.JSONDecodeError:
        file_handle.seek(0)
        for _ in range(last_non_blank_index):
            file_handle.readline()
        truncate_pos = file_handle.tell()
        file_handle.seek(truncate_pos)
        file_handle.truncate()
        return "".join(lines[:last_non_blank_index])


def append_event(
    trace_path: Path,
    event: TraceEvent,
    *,
    protected_storage: ProtectedStorage | None = None,
) -> None:
    """Append a validated trace event to the NDJSON trace file.

    Uses an exclusive file lock so concurrent agent activity cannot
    interleave partial writes. While holding the lock the function reads
    the last valid event in the file and enforces FR-012 ascending
    timestamps. Explicit caller-provided out-of-order timestamps are
    rejected; auto-generated timestamps are advanced under lock when needed
    to preserve monotonic ordering across concurrent appenders.

    A malformed final non-blank plaintext NDJSON line (for example from an
    interrupted prior write) is truncated under lock before appending so it
    cannot become malformed mid-file data.

    For the ``protected_storage`` path the same FR-012 ordering check runs
    inside the append transaction via ``ProtectedStorage.append``'s
    ``before_append`` callback, so the check and encrypted write share the
    same exclusive lock and cannot race.
    """
    line = serialize_event(event)
    if protected_storage is not None:

        def _validate_last_timestamp(last_plaintext: bytes | None) -> bytes | None:
            if last_plaintext is None:
                return None
            last_ts = _last_event_timestamp(last_plaintext.decode("utf-8"))
            effective_timestamp = _effective_timestamp_for_append(event, last_ts)
            if effective_timestamp != event.timestamp:
                return (_serialize_event_with_timestamp(event, effective_timestamp) + "\n").encode("utf-8")
            return None

        protected_storage.append((line + "\n").encode("utf-8"), before_append=_validate_last_timestamp)
        return
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with locked_file(trace_path, mode="r+", include_created=True) as (file_handle, _created):
        file_handle_io = cast(IO[str], file_handle)
        content = file_handle_io.read()
        content = _truncate_malformed_trailing_record(file_handle_io, content)
        last_ts = _last_event_timestamp(content)
        effective_timestamp = _effective_timestamp_for_append(event, last_ts)
        line_to_append = (
            line
            if effective_timestamp == event.timestamp
            else _serialize_event_with_timestamp(event, effective_timestamp)
        )
        file_handle_io.seek(0, 2)  # seek to end of file
        file_handle_io.write(line_to_append + "\n")


def read_events(
    trace_path: Path,
    *,
    protected_storage: ProtectedStorage | None = None,
) -> list[dict[str, Any]]:
    """Read and parse all NDJSON trace events from ``trace_path``.

    A malformed *final* non-blank line is skipped (to tolerate interrupted
    final writes), but malformed non-final lines raise ``JSONDecodeError``
    because they indicate mid-file corruption.
    """
    if protected_storage is not None:
        encrypted_events: list[dict[str, Any]] = []
        for plaintext in protected_storage.read_all():
            encrypted_events.append(json.loads(plaintext.decode("utf-8")))
        return encrypted_events
    if not trace_path.exists():
        return []
    events: list[dict[str, Any]] = []
    with locked_file(trace_path, mode="r", exclusive=False, encoding="utf-8") as handle:
        file_handle = cast(IO[str], handle)
        non_blank_lines = [line.strip() for line in file_handle if line.strip()]
    for i, stripped in enumerate(non_blank_lines):
        is_last = i == len(non_blank_lines) - 1
        try:
            events.append(json.loads(stripped))
        except json.JSONDecodeError:
            if is_last:
                # The final non-blank line may be a partially written record; tolerate it.
                continue
            raise
    return events


def trace_path_for(state_dir: Path, run_id: str) -> Path:
    """Return the canonical NDJSON trace path for a hierarchy orchestration run."""
    if not _SAFE_RUN_ID_RE.fullmatch(run_id):
        raise ValueError("run_id must be a single safe filesystem path segment")
    return state_dir / "orchestration" / "hierarchy" / run_id / "trace.ndjson"


def attach_provenance_to_event(event_detail: dict[str, Any], provenance: str) -> dict[str, Any]:
    """Return a copy of ``event_detail`` with a ``context_provenance`` field attached.

    Every relevant trace event type (``context_injected``, ``review_decision``,
    ``degradation``) MAY carry a ``context_provenance`` status
    (``"verified" | "unavailable" | "inferred"``) so that a maintainer
    inspecting the trace can tell whether the event was produced from
    verified, unavailable, or inferred hierarchy context (NFR-005). This is
    an additive extension field; it never replaces or narrows any of the
    event's required FR-012 keys.
    """
    if provenance not in ("verified", "unavailable", "inferred"):
        msg = f"Invalid context_provenance value: {provenance!r}"
        raise TraceValidationError(msg)
    updated = dict(event_detail)
    updated["context_provenance"] = provenance
    return updated
