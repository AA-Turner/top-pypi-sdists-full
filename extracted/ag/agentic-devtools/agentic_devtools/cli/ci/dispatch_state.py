"""Durable state for safe Agent Tasks repair dispatches."""

from __future__ import annotations

import json
import os
import re
import secrets
import tempfile
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from hmac import compare_digest
from pathlib import Path
from typing import Any

from agentic_devtools.file_locking import locked_file

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_REPO_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
_TASK_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_CAPABILITY_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
_MAX_EVIDENCE_BYTES = 4096
_MAX_EVIDENCE_DEPTH = 8
_MAX_REASON_CHARS = 512
MAX_DISPATCHES_PER_SHA = 3
_IMMUTABLE_RECORD_FIELDS = frozenset({"repo", "pull_request_id", "sha", "ordinal", "token", "created_at"})
_EVIDENCE_CYCLE_PLACEHOLDER = "[CYCLE]"
_EVIDENCE_DEPTH_PLACEHOLDER = "[DEPTH_LIMIT]"
_EVIDENCE_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?i)\bauthorization\s*:\s*(?:bearer|basic)\s+\S+"),
    re.compile(r"(?i)\b(?:bearer|basic)\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"(?i)\b(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{20,}\b"),
)
_EVIDENCE_SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)(?P<key>"
    r"\"(?:api[_-]?key|token|password|passwd|secret|credential(?:s)?|access[_-]?token|refresh[_-]?token|authorization|auth|pat|private[_-]?key)\""
    r"|'(?:api[_-]?key|token|password|passwd|secret|credential(?:s)?|access[_-]?token|refresh[_-]?token|authorization|auth|pat|private[_-]?key)'"
    r"|api[_-]?key|token|password|passwd|secret|credential(?:s)?|access[_-]?token|refresh[_-]?token|authorization|auth|pat|private[_-]?key"
    r")(?P<separator>\s*[:=]\s*)(?P<value>\"[^\"]*\"|'[^']*'|[^\s,;]+)"
)


class DispatchState(StrEnum):
    """The closed set of persisted dispatch states."""

    INTENT = "intent"
    RESERVED = "reserved"
    CREATING = "creating"
    CREATED = "created"
    LINKED = "linked"
    SUCCEEDED = "succeeded"
    NEEDS_RECONCILIATION = "needs_reconciliation"
    ABANDONED = "abandoned"
    ABORTED_AFTER_FINAL_DISPATCH = "aborted_after_final_dispatch"


TERMINAL_STATES = frozenset(
    {
        DispatchState.SUCCEEDED,
        DispatchState.ABANDONED,
        DispatchState.ABORTED_AFTER_FINAL_DISPATCH,
    }
)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _validate_repo(repo: object) -> str:
    if not isinstance(repo, str) or not _REPO_RE.fullmatch(repo):
        raise ValueError("repo must be a repository name, not an owner/repository path")
    return repo.lower()


def _attempt_capability_digest(capability: object) -> str:
    if not isinstance(capability, str) or not capability:
        raise ValueError("attempt_capability must be a non-empty string")
    return sha256(capability.encode("utf-8")).hexdigest()


def _redact_secrets(value: str) -> str:
    redacted = value
    for pattern in _EVIDENCE_SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    redacted = _EVIDENCE_SECRET_ASSIGNMENT_PATTERN.sub(
        lambda match: f"{match.group('key')}{match.group('separator')}[REDACTED]",
        redacted,
    )
    return redacted


def _bounded_reason(reason: str | None) -> str | None:
    if reason is None:
        return None
    if not isinstance(reason, str):
        raise ValueError("reason must be a string when provided")
    return _redact_secrets(reason)[:_MAX_REASON_CHARS]


@dataclass(frozen=True)
class DispatchIdentity:
    """Immutable identity used to correlate one ordinal dispatch."""

    repo: str
    pull_request_id: int
    sha: str
    ordinal: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "repo", _validate_repo(self.repo))
        _positive_int(self.pull_request_id, "pull_request_id")
        if not isinstance(self.sha, str) or not _SHA_RE.fullmatch(self.sha):
            raise ValueError("sha must be a complete lowercase 40-character hexadecimal SHA")
        _positive_int(self.ordinal, "ordinal")

    @property
    def key(self) -> str:
        """Return a stable JSON-map key for this identity."""
        return f"{self.repo}:{self.pull_request_id}:{self.sha}:{self.ordinal}"

    @property
    def token(self) -> str:
        """Return the exact remote correlation token."""
        return f"agdt-dispatch-{self.repo}-{self.pull_request_id}-{self.sha}-{self.ordinal}"


DispatchKey = DispatchIdentity


@dataclass(frozen=True)
class DispatchRecord:
    """A validated, serializable dispatch state-machine record."""

    repo: str
    pull_request_id: int
    sha: str
    ordinal: int
    token: str
    state: DispatchState
    created_at: str
    updated_at: str
    attempt_capability: str | None = field(default=None, compare=False)
    attempt_capability_digest: str | None = None
    retry_count: int = 0
    marker_comment_id: int | None = None
    task_id: str | None = None
    reason: str | None = None
    evidence: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def new(cls, identity: DispatchIdentity) -> DispatchRecord:
        """Create the initial intent record without performing a remote write."""
        now = _now()
        return cls(
            repo=identity.repo,
            pull_request_id=identity.pull_request_id,
            sha=identity.sha,
            ordinal=identity.ordinal,
            token=identity.token,
            state=DispatchState.INTENT,
            created_at=now,
            updated_at=now,
        )

    @property
    def identity(self) -> DispatchIdentity:
        return DispatchIdentity(self.repo, self.pull_request_id, self.sha, self.ordinal)

    def validate(self) -> DispatchRecord:
        """Validate all fields and state-specific requirements."""
        if self.repo != _validate_repo(self.repo):
            raise ValueError("repo must be a lowercase canonical repository name")
        identity = self.identity
        if identity.ordinal > MAX_DISPATCHES_PER_SHA:
            raise ValueError("at most three dispatches are allowed for one SHA")
        if self.token != identity.token:
            raise ValueError("record token does not match its immutable identity")
        if not isinstance(self.state, DispatchState):
            raise ValueError("record state is not one of the legal dispatch states")
        if not isinstance(self.created_at, str) or not self.created_at:
            raise ValueError("created_at is required")
        if not isinstance(self.updated_at, str) or not self.updated_at:
            raise ValueError("updated_at is required")
        if self.attempt_capability is not None:
            _attempt_capability_digest(self.attempt_capability)
        if self.attempt_capability_digest is not None and (
            not isinstance(self.attempt_capability_digest, str)
            or not _CAPABILITY_DIGEST_RE.fullmatch(self.attempt_capability_digest)
        ):
            raise ValueError("attempt_capability_digest must be a lowercase SHA-256 hex digest")
        if isinstance(self.retry_count, bool) or not isinstance(self.retry_count, int) or self.retry_count < 0:
            raise ValueError("retry_count must be a non-negative integer")
        if self.retry_count > 4:
            raise ValueError("retry_count cannot exceed the pre-write terminal budget")
        if self.retry_count == 4 and self.state is not DispatchState.ABANDONED:
            raise ValueError("retry_count=4 is only valid in the abandoned terminal state")
        if self.marker_comment_id is not None:
            _positive_int(self.marker_comment_id, "marker_comment_id")
        if self.task_id is not None and (not isinstance(self.task_id, str) or not _TASK_ID_RE.fullmatch(self.task_id)):
            raise ValueError("task_id must be a non-empty safe identifier")
        if _bounded_reason(self.reason) != self.reason:
            raise ValueError("reason must already be bounded and redacted")
        if not isinstance(self.evidence, dict):
            raise ValueError("evidence must be an object")
        if _bounded_evidence(self.evidence) != self.evidence:
            raise ValueError("evidence must already be bounded and redacted")
        if self.state is DispatchState.INTENT and (self.marker_comment_id is not None or self.task_id is not None):
            raise ValueError("intent cannot contain remote identifiers")
        if self.state is not DispatchState.CREATING and self.attempt_capability_digest is not None:
            raise ValueError("attempt_capability_digest is only valid while a task POST is pending")
        if self.state in {DispatchState.RESERVED, DispatchState.CREATING, DispatchState.NEEDS_RECONCILIATION}:
            if self.task_id is not None:
                raise ValueError(f"task_id is not allowed in {self.state.value}")
        if self.state in {
            DispatchState.RESERVED,
            DispatchState.CREATING,
            DispatchState.CREATED,
            DispatchState.LINKED,
            DispatchState.SUCCEEDED,
            DispatchState.ABORTED_AFTER_FINAL_DISPATCH,
        }:
            if self.marker_comment_id is None:
                raise ValueError(f"marker_comment_id is required in {self.state.value}")
        if self.state in {
            DispatchState.CREATED,
            DispatchState.LINKED,
            DispatchState.SUCCEEDED,
            DispatchState.ABORTED_AFTER_FINAL_DISPATCH,
        }:
            if self.task_id is None:
                raise ValueError(f"task_id is required in {self.state.value}")
        if self.state in {DispatchState.NEEDS_RECONCILIATION, DispatchState.ABANDONED}:
            if not self.reason or not self.evidence:
                raise ValueError(f"reason and evidence are required in {self.state.value}")
        if self.state is DispatchState.NEEDS_RECONCILIATION:
            operation = self.evidence.get("operation")
            if operation not in {"marker", "task"}:
                raise ValueError("needs_reconciliation evidence.operation must be 'marker' or 'task'")
            if operation == "marker" and self.marker_comment_id is not None:
                raise ValueError("marker reconciliation cannot persist marker_comment_id before confirmation")
            if operation == "task" and self.marker_comment_id is None:
                raise ValueError("task reconciliation requires the persisted marker_comment_id")
        if self.state is DispatchState.ABORTED_AFTER_FINAL_DISPATCH and self.ordinal != MAX_DISPATCHES_PER_SHA:
            raise ValueError("aborted_after_final_dispatch is only valid for the third dispatch ordinal")
        return self

    def to_dict(self) -> dict[str, Any]:
        """Serialize this record after validating it."""
        self.validate()
        return {
            "repo": self.repo,
            "pull_request_id": self.pull_request_id,
            "sha": self.sha,
            "ordinal": self.ordinal,
            "token": self.token,
            "state": self.state.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "attempt_capability_digest": self.attempt_capability_digest,
            "retry_count": self.retry_count,
            "marker_comment_id": self.marker_comment_id,
            "task_id": self.task_id,
            "reason": self.reason,
            "evidence": self.evidence,
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> DispatchRecord:
        """Deserialize and validate an untrusted JSON object."""
        if not isinstance(raw, dict):
            raise ValueError("dispatch record must be an object")
        try:
            state = DispatchState(raw["state"])
            record = cls(
                repo=raw["repo"],
                pull_request_id=raw["pull_request_id"],
                sha=raw["sha"],
                ordinal=raw["ordinal"],
                token=raw["token"],
                state=state,
                created_at=raw["created_at"],
                updated_at=raw["updated_at"],
                attempt_capability_digest=raw.get("attempt_capability_digest"),
                retry_count=raw.get("retry_count", 0),
                marker_comment_id=raw.get("marker_comment_id"),
                task_id=raw.get("task_id"),
                reason=raw.get("reason"),
                evidence=raw.get("evidence", {}),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("invalid dispatch record") from exc
        return record.validate()

    def with_state(self, state: str | DispatchState, **changes: Any) -> DispatchRecord:
        """Return a validated copy with a state-machine update."""
        immutable_changes = sorted(_IMMUTABLE_RECORD_FIELDS.intersection(changes))
        if immutable_changes:
            names = ", ".join(immutable_changes)
            raise ValueError(f"with_state cannot modify immutable fields: {names}")
        for remote_id_field in ("marker_comment_id", "task_id"):
            current = getattr(self, remote_id_field)
            if current is not None and remote_id_field in changes and changes[remote_id_field] != current:
                raise ValueError(f"{remote_id_field} cannot change once set")
        if "reason" in changes:
            changes["reason"] = _bounded_reason(changes["reason"])
        next_state = DispatchState(state)
        if next_state is DispatchState.CREATING:
            capability = changes.get("attempt_capability")
            if capability is not None and "attempt_capability_digest" not in changes:
                changes["attempt_capability_digest"] = _attempt_capability_digest(capability)
        else:
            changes.setdefault("attempt_capability", None)
            changes.setdefault("attempt_capability_digest", None)
        evidence = changes.get("evidence", self.evidence)
        if evidence is not self.evidence:
            changes["evidence"] = _bounded_evidence(evidence)
        updated = replace(self, state=next_state, updated_at=_now(), **changes)
        return updated.validate()


def _normalize_evidence_key(key: object) -> str:
    text = re.sub(r"(?<!^)(?=[A-Z])", "_", str(key))
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def _is_sensitive_evidence_key(key: object) -> bool:
    normalized = _normalize_evidence_key(key)
    if normalized in {"apikey", "authorization", "header", "headers", "prompt", "body"}:
        return True
    tokens = {token for token in normalized.split("_") if token}
    if tokens & {
        "token",
        "secret",
        "password",
        "passwd",
        "cookie",
        "pat",
        "auth",
        "credential",
        "credentials",
        "authorization",
        "header",
        "headers",
        "prompt",
        "body",
    }:
        return True
    return "key" in tokens


def _bounded_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(evidence, dict):
        raise ValueError("evidence must be an object")

    def clean(value: Any, depth: int, active_ids: set[int]) -> Any:
        if depth >= _MAX_EVIDENCE_DEPTH:
            return _EVIDENCE_DEPTH_PLACEHOLDER
        if isinstance(value, dict):
            value_id = id(value)
            if value_id in active_ids:
                return _EVIDENCE_CYCLE_PLACEHOLDER
            active_ids.add(value_id)
            try:
                return {
                    str(key): clean(item, depth + 1, active_ids)
                    for key, item in value.items()
                    if not _is_sensitive_evidence_key(key)
                }
            finally:
                active_ids.remove(value_id)
        if isinstance(value, (list, tuple)):
            value_id = id(value)
            if value_id in active_ids:
                return _EVIDENCE_CYCLE_PLACEHOLDER
            active_ids.add(value_id)
            try:
                return [clean(item, depth + 1, active_ids) for item in value[:32]]
            finally:
                active_ids.remove(value_id)
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value if not isinstance(value, str) else _redact_secrets(value)[:512]
        return _redact_secrets(str(value))[:128]

    result = clean(evidence, 0, set())
    if len(json.dumps(result, ensure_ascii=False).encode("utf-8")) > _MAX_EVIDENCE_BYTES:
        raise ValueError("evidence exceeds the bounded storage limit")
    return result


def _read_store(content: str) -> dict[str, dict[str, Any]]:
    if not content.strip():
        raise ValueError("dispatch state file is blank")
    try:
        raw = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("dispatch state is not valid JSON") from exc
    if not isinstance(raw, dict):
        records = None
    elif "version" in raw or "records" in raw:
        version = raw.get("version")
        if isinstance(version, bool) or not isinstance(version, int) or version != 1:
            raise ValueError("dispatch state version is unsupported")
        records = raw.get("records")
    else:
        records = raw
    if not isinstance(records, dict):
        raise ValueError("dispatch state records must be an object")
    validated: dict[str, dict[str, Any]] = {}
    scoped_records: dict[tuple[str, int, str], list[DispatchRecord]] = {}
    for key, raw_record in records.items():
        try:
            record = DispatchRecord.from_dict(raw_record)
        except ValueError as exc:
            raise ValueError("dispatch state contains an invalid record") from exc
        if key != record.identity.key:
            raise ValueError("dispatch state record key does not match record identity")
        validated[key] = record.to_dict()
        scope = (record.repo, record.pull_request_id, record.sha)
        scoped_records.setdefault(scope, []).append(record)
    for ordered_scope_records in scoped_records.values():
        ordered_scope_records.sort(key=lambda item: item.ordinal)
        expected_ordinal = 1
        unresolved_count = 0
        latest_unresolved_ordinal: int | None = None
        for scoped_record in ordered_scope_records:
            if scoped_record.ordinal != expected_ordinal:
                raise ValueError("dispatch state ordinals must be contiguous per scope")
            expected_ordinal += 1
            if scoped_record.state not in TERMINAL_STATES:
                unresolved_count += 1
                latest_unresolved_ordinal = scoped_record.ordinal
        if unresolved_count > 1:
            raise ValueError("dispatch state must include a single unresolved record per scope")
        if latest_unresolved_ordinal is not None and latest_unresolved_ordinal != ordered_scope_records[-1].ordinal:
            raise ValueError("dispatch state unresolved record must be the latest ordinal per scope")
    return validated


def _dispatch_lock_path(path: Path) -> Path:
    return path.with_name(f"{path.name}.lock")


def _load_store(path: Path) -> dict[str, dict[str, Any]]:
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    return _read_store(content)


def _fsync_directory(path: Path) -> None:
    if os.name == "nt" and not hasattr(os, "O_DIRECTORY"):
        return
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    try:
        directory_fd = os.open(path, flags)
    except OSError as exc:
        raise OSError(f"failed to fsync directory {path}") from exc
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def _write_store(path: Path, records: dict[str, dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({"version": 1, "records": records}, indent=2, ensure_ascii=False) + "\n"
    file_descriptor, temp_path = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(file_descriptor, "wb") as handle:
            handle.write(payload.encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        _fsync_directory(path.parent)
    except BaseException:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def load_dispatch_record(path: Path, identity: DispatchIdentity) -> DispatchRecord | None:
    """Load one record under the repository's exclusive file lock."""
    identity = DispatchIdentity(identity.repo, identity.pull_request_id, identity.sha, identity.ordinal)
    with locked_file(_dispatch_lock_path(path), "a+", exclusive=True, encoding="utf-8"):
        records = _load_store(path)
    raw = records.get(identity.key)
    return DispatchRecord.from_dict(raw) if raw is not None else None


def save_dispatch_record_atomic(path: Path, record: DispatchRecord) -> None:
    """Persist one validated record while holding the state-file lock."""
    record.validate()
    with locked_file(_dispatch_lock_path(path), "a+", exclusive=True, encoding="utf-8"):
        records = _load_store(path)
        existing_raw = records.get(record.identity.key)
        if existing_raw is None:
            if record.state is not DispatchState.INTENT:
                raise ValueError("new records must start in intent state")
            scoped = [
                DispatchRecord.from_dict(raw)
                for raw in records.values()
                if raw.get("repo") == record.repo
                and raw.get("pull_request_id") == record.pull_request_id
                and raw.get("sha") == record.sha
            ]
            if any(item.state not in TERMINAL_STATES for item in scoped):
                raise ValueError("an unresolved dispatch blocks a new ordinal claim")
            expected_ordinal = len(scoped) + 1
            if record.ordinal != expected_ordinal:
                raise ValueError("dispatch ordinals must be claimed in order")
        else:
            existing = DispatchRecord.from_dict(existing_raw)
            if existing.marker_comment_id is not None and record.marker_comment_id != existing.marker_comment_id:
                raise ValueError("marker_comment_id cannot change once set")
            if existing.task_id is not None and record.task_id != existing.task_id:
                raise ValueError("task_id cannot change once set")
            if record.to_dict() != existing.to_dict():
                candidate_changes: dict[str, Any] = {}
                for name in (
                    "attempt_capability_digest",
                    "retry_count",
                    "marker_comment_id",
                    "task_id",
                    "reason",
                    "evidence",
                ):
                    existing_value = getattr(existing, name)
                    new_value = getattr(record, name)
                    if new_value != existing_value:
                        candidate_changes[name] = new_value
                expected = {key: value for key, value in record.to_dict().items() if key != "updated_at"}
                has_legal_transition = False
                for (source, event), target in _EVENT_TARGETS.items():
                    if source is not existing.state or target is not record.state:
                        continue
                    try:
                        transitioned = transition_record(existing, event, **candidate_changes)
                    except ValueError:
                        continue
                    transitioned_payload = {
                        key: value for key, value in transitioned.to_dict().items() if key != "updated_at"
                    }
                    if transitioned_payload == expected:
                        has_legal_transition = True
                        break
                if not has_legal_transition:
                    if record.state is existing.state:
                        raise ValueError("cannot persist a stale same-state dispatch record")
                    raise ValueError("cannot persist an illegal state transition for an existing dispatch record")
        records[record.identity.key] = record.to_dict()
        _write_store(path, records)


def create_intent(path: Path, identity: DispatchIdentity) -> DispatchRecord:
    """Persist an intent, fail-closing any replayed intent before another marker POST."""
    identity = DispatchIdentity(identity.repo, identity.pull_request_id, identity.sha, identity.ordinal)
    if identity.ordinal > MAX_DISPATCHES_PER_SHA:
        raise ValueError("at most three dispatches are allowed for one SHA")
    with locked_file(_dispatch_lock_path(path), "a+", exclusive=True, encoding="utf-8"):
        records = _load_store(path)
        existing = records.get(identity.key)
        if existing is not None:
            existing_record = DispatchRecord.from_dict(existing)
            if existing_record.state is DispatchState.INTENT:
                existing_record = transition_record(
                    existing_record,
                    "marker_uncertain",
                    reason="replayed intent requires marker reconciliation",
                    evidence={"operation": "marker", "source": "create_intent_replay"},
                )
                records[identity.key] = existing_record.to_dict()
                _write_store(path, records)
            return existing_record
        scoped = [
            DispatchRecord.from_dict(raw)
            for raw in records.values()
            if raw.get("repo") == identity.repo
            and raw.get("pull_request_id") == identity.pull_request_id
            and raw.get("sha") == identity.sha
        ]
        if any(item.state not in TERMINAL_STATES for item in scoped):
            raise ValueError("an unresolved dispatch blocks a new ordinal claim")
        expected_ordinal = len(scoped) + 1
        if identity.ordinal != expected_ordinal:
            raise ValueError("dispatch ordinals must be claimed in order")
        record = DispatchRecord.new(identity)
        records[identity.key] = record.to_dict()
        _write_store(path, records)
        return record


_EVENT_TARGETS: dict[tuple[DispatchState, str], DispatchState] = {
    (DispatchState.INTENT, "pre_write_failure"): DispatchState.INTENT,
    (DispatchState.INTENT, "marker_succeeded"): DispatchState.RESERVED,
    (DispatchState.INTENT, "marker_success"): DispatchState.RESERVED,
    (DispatchState.INTENT, "marker_uncertain"): DispatchState.NEEDS_RECONCILIATION,
    (DispatchState.RESERVED, "preparation_succeeded"): DispatchState.CREATING,
    (DispatchState.RESERVED, "pre_write_failure"): DispatchState.RESERVED,
    (DispatchState.RESERVED, "abandon"): DispatchState.ABANDONED,
    (DispatchState.CREATING, "pre_write_failure"): DispatchState.RESERVED,
    (DispatchState.CREATING, "task_created"): DispatchState.CREATED,
    (DispatchState.CREATING, "task_success"): DispatchState.CREATED,
    (DispatchState.CREATING, "task_uncertain"): DispatchState.NEEDS_RECONCILIATION,
    (DispatchState.CREATED, "link_succeeded"): DispatchState.LINKED,
    (DispatchState.CREATED, "link_success"): DispatchState.LINKED,
    (DispatchState.CREATED, "link_exists"): DispatchState.LINKED,
    (DispatchState.CREATED, "link_failed"): DispatchState.CREATED,
    (DispatchState.LINKED, "downstream_succeeded"): DispatchState.SUCCEEDED,
    (DispatchState.LINKED, "downstream_success"): DispatchState.SUCCEEDED,
    (DispatchState.LINKED, "final_dispatch"): DispatchState.ABORTED_AFTER_FINAL_DISPATCH,
    (DispatchState.LINKED, "final_dispatch_closed"): DispatchState.ABORTED_AFTER_FINAL_DISPATCH,
    (DispatchState.NEEDS_RECONCILIATION, "reconcile_marker_unique"): DispatchState.RESERVED,
    (DispatchState.NEEDS_RECONCILIATION, "reconcile_marker_miss"): DispatchState.INTENT,
    (DispatchState.NEEDS_RECONCILIATION, "reconcile_task_unique"): DispatchState.CREATED,
    (DispatchState.NEEDS_RECONCILIATION, "reconcile_task_miss"): DispatchState.RESERVED,
    (DispatchState.NEEDS_RECONCILIATION, "reconcile_ambiguous"): DispatchState.NEEDS_RECONCILIATION,
    (DispatchState.NEEDS_RECONCILIATION, "reconcile_incomplete"): DispatchState.NEEDS_RECONCILIATION,
}

for _state in (
    DispatchState.INTENT,
    DispatchState.RESERVED,
    DispatchState.CREATING,
    DispatchState.CREATED,
    DispatchState.LINKED,
    DispatchState.NEEDS_RECONCILIATION,
):
    _EVENT_TARGETS[(_state, "abandon")] = DispatchState.ABANDONED


def _reconciliation_operation(record: DispatchRecord, changes: dict[str, Any]) -> str | None:
    persisted_operation = record.evidence.get("operation")
    if record.state is DispatchState.NEEDS_RECONCILIATION and persisted_operation in {"marker", "task"}:
        supplied_evidence = changes.get("evidence")
        if isinstance(supplied_evidence, dict):
            supplied_operation = supplied_evidence.get("operation")
            if supplied_operation is not None and supplied_operation != persisted_operation:
                raise ValueError(
                    f"reconciliation evidence operation {supplied_operation!r} "
                    f"does not match the persisted uncertain operation {persisted_operation!r}"
                )
        return persisted_operation
    evidence = changes.get("evidence", record.evidence)
    if isinstance(evidence, dict):
        operation = evidence.get("operation")
        if operation in {"marker", "task"}:
            return operation
    if record.marker_comment_id is None and record.task_id is None:
        return "marker"
    if record.marker_comment_id is not None:
        return "task"
    return None


def _normalize_reconciliation_event(record: DispatchRecord, event: str, changes: dict[str, Any]) -> str:
    if record.state is not DispatchState.NEEDS_RECONCILIATION:
        return event
    operation = _reconciliation_operation(record, changes)
    if operation is None:
        raise ValueError("reconciliation evidence must identify whether the uncertain write was marker or task")
    if event in {"reconcile_marker_unique", "reconcile_marker_miss", "reconcile_task_unique", "reconcile_task_miss"}:
        if not event.startswith(f"reconcile_{operation}_"):
            raise ValueError(f"{event} does not match the persisted uncertain operation {operation!r}")
        return event
    if event not in {"reconcile_unique", "reconcile_miss"}:
        return event
    suffix = "unique" if event == "reconcile_unique" else "miss"
    return f"reconcile_{operation}_{suffix}"


def transition_record(record: DispatchRecord, event: str, **changes: Any) -> DispatchRecord:
    """Apply one legal transition without performing a remote side effect."""
    record.validate()
    supplied_retry_count = changes.get("retry_count")
    if supplied_retry_count is not None and event != "pre_write_failure":
        if type(supplied_retry_count) is not int or supplied_retry_count != record.retry_count:
            raise ValueError("retry_count cannot be changed by transition arguments outside pre_write_failure")
        changes.pop("retry_count", None)
    uncertain_operation = {
        "marker_uncertain": "marker",
        "task_uncertain": "task",
    }.get(event)
    if uncertain_operation is not None:
        evidence = changes.get("evidence")
        if isinstance(evidence, dict):
            supplied_operation = evidence.get("operation")
            if supplied_operation is not None and supplied_operation != uncertain_operation:
                raise ValueError(
                    f"{event} evidence operation {supplied_operation!r} "
                    f"does not match the uncertain operation {uncertain_operation!r}"
                )
    event = _normalize_reconciliation_event(record, event, changes)
    target = _EVENT_TARGETS.get((record.state, event))
    if target is None:
        if event == "replay" or event == record.state.value:
            if any(getattr(record, key, object()) != value for key, value in changes.items()):
                raise ValueError(f"{event} cannot include state changes")
            return record
        raise ValueError(f"event {event!r} is not valid from {record.state.value!r}")
    if (
        record.state is DispatchState.CREATING
        and event in {"task_created", "task_success", "task_uncertain"}
        and record.attempt_capability_digest is not None
    ):
        raise ValueError("task results are not valid before task creation capability consumption")
    if event == "pre_write_failure":
        if record.state is DispatchState.CREATING and record.attempt_capability_digest is None:
            raise ValueError("pre_write_failure is not valid after task creation capability consumption")
        retry_count = record.retry_count + 1
        changes["retry_count"] = retry_count
        if retry_count >= 4:
            target = DispatchState.ABANDONED
            changes.setdefault("reason", "pre-write retry exhaustion")
            changes.setdefault("evidence", {"operation": "pre-write", "retry_count": retry_count})
    if event in {"reconcile_marker_miss", "reconcile_task_miss"}:
        changes["retry_count"] = 0
    if target is DispatchState.NEEDS_RECONCILIATION:
        if not changes.get("reason") or not changes.get("evidence"):
            raise ValueError("reconciliation transitions require reason and evidence")
        operation = _reconciliation_operation(record, changes)
        evidence = changes["evidence"]
        if operation is not None and isinstance(evidence, dict) and "operation" not in evidence:
            changes["evidence"] = {**evidence, "operation": operation}
    if record.state is DispatchState.CREATING and target is not DispatchState.CREATING:
        changes.setdefault("attempt_capability", None)
        changes.setdefault("attempt_capability_digest", None)
    if (
        target
        in {
            DispatchState.CREATED,
            DispatchState.LINKED,
            DispatchState.SUCCEEDED,
            DispatchState.ABORTED_AFTER_FINAL_DISPATCH,
        }
        and changes.get("task_id") is None
    ):
        changes["task_id"] = record.task_id
    if target is DispatchState.ABANDONED:
        if not changes.get("reason") or not changes.get("evidence"):
            raise ValueError("abandonment requires reason and evidence")
        for remote_id_field in ("marker_comment_id", "task_id"):
            current = getattr(record, remote_id_field)
            supplied = changes.get(remote_id_field, current)
            if supplied != current:
                raise ValueError(f"abandonment cannot introduce or change {remote_id_field}")
    if target is DispatchState.CREATING:
        capability = changes.get("attempt_capability")
        capability_digest = changes.get("attempt_capability_digest")
        if capability is None and capability_digest is None:
            capability = secrets.token_urlsafe(18)
            changes["attempt_capability"] = capability
        if capability is not None:
            changes["attempt_capability_digest"] = _attempt_capability_digest(capability)
    return record.with_state(target, **changes)


def transition_dispatch(path: Path, identity: DispatchIdentity, event: str, **changes: Any) -> DispatchRecord:
    """Atomically apply a transition and persist it before returning."""
    with locked_file(_dispatch_lock_path(path), "a+", exclusive=True, encoding="utf-8"):
        records = _load_store(path)
        raw = records.get(identity.key)
        if raw is None:
            raise ValueError("dispatch record does not exist")
        record = transition_record(DispatchRecord.from_dict(raw), event, **changes)
        records[identity.key] = record.to_dict()
        _write_store(path, records)
        return record


def consume_task_creation_capability(path: Path, record: DispatchRecord) -> DispatchRecord:
    """Atomically consume the persisted one-shot capability for a creating record."""
    record.validate()
    digest = _attempt_capability_digest(record.attempt_capability)
    with locked_file(_dispatch_lock_path(path), "a+", exclusive=True, encoding="utf-8"):
        records = _load_store(path)
        raw = records.get(record.identity.key)
        if raw is None:
            raise ValueError("task creation requires a durably persisted creating marker")
        persisted = DispatchRecord.from_dict(raw)
        if (
            persisted.to_dict() != record.to_dict()
            or persisted.state is not DispatchState.CREATING
            or persisted.marker_comment_id is None
            or persisted.attempt_capability_digest is None
            or not compare_digest(persisted.attempt_capability_digest, digest)
        ):
            raise ValueError("task creation requires a durably persisted creating marker")
        consumed = replace(persisted, updated_at=_now(), attempt_capability_digest=None)
        consumed.validate()
        records[record.identity.key] = consumed.to_dict()
        _write_store(path, records)
        return consumed


def record_remote_evidence(
    path: Path,
    identity: DispatchIdentity,
    *,
    reason: str,
    evidence: dict[str, Any],
    event: str | None = None,
) -> DispatchRecord:
    """Persist reconciliation evidence without repeating an uncertain write."""
    if event is None:
        current = load_dispatch_record(path, identity)
        if current is None:
            raise ValueError("dispatch record does not exist")
        event = "marker_uncertain" if current.state is DispatchState.INTENT else "task_uncertain"
    return transition_dispatch(path, identity, event, reason=reason, evidence=evidence)


def validate_dispatch_record(record: DispatchRecord) -> DispatchRecord:
    """Validate and return a complete dispatch record."""
    return record.validate()
