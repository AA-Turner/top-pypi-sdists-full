"""Repository-backed queue-state persistence."""

from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import re
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import asdict, replace
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Protocol
from uuid import uuid4

from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.reconciliation.models import (
    QuarantineRecord,
    QueueState,
    queue_state_from_dict,
    validate_queue_state,
)
from agentic_devtools.state import deserialize_queue_document, serialize_queue_document

logger = logging.getLogger(__name__)
_HTTP_STATUS_TOKEN_TEMPLATE = r"(?<!\d){code}(?!\d)"


def _state_to_dict(state: QueueState) -> dict[str, Any]:
    """Serialize queue state while converting immutable metric attributes."""
    payload = asdict(replace(state, metric_events=[]))
    payload["metric_events"] = [
        {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "repo": event.repo,
            "recorded_at": event.recorded_at,
            "attributes": _thaw_metric_attributes(event.attributes),
        }
        for event in state.metric_events
    ]
    return payload


def _thaw_metric_attributes(value: Any) -> Any:
    """Convert nested immutable metric attributes to JSON-compatible containers."""
    if isinstance(value, Mapping):
        return {str(key): _thaw_metric_attributes(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_thaw_metric_attributes(item) for item in value]
    return value


class QueueStoreError(Exception):
    """Base exception for queue store errors."""


class ConcurrentModificationError(QueueStoreError):
    """Raised when a save is attempted with a stale revision."""


class StateDecodeError(QueueStoreError):
    """Raised when persisted queue state cannot be decoded safely."""


class StateTooLargeError(QueueStoreError):
    """Raised when serialized state exceeds MAX_STATE_SIZE_BYTES."""


class StateTooStaleError(QueueStoreError):
    """Raised when state is older than MAX_STATE_AGE_SECONDS."""


class QuarantineActiveError(QueueStoreError):
    """Raised when a mutation is attempted on a quarantined state."""


class BackingStore(Protocol):
    """Storage protocol for durable queue-state entries."""

    def load_entry(self, key: tuple[str, str]) -> tuple[int, QueueState] | None: ...  # pragma: no cover

    def save_entry(
        self, key: tuple[str, str], expected_revision: int, updated: QueueState
    ) -> None: ...  # pragma: no cover

    def recovery_token(self, key: tuple[str, str]) -> str | None: ...  # pragma: no cover

    def save_recovery_entry(
        self, key: tuple[str, str], expected_token: str, updated: QueueState
    ) -> None: ...  # pragma: no cover


class InMemoryBackingStore:
    """Backing store that keeps queue-state entries in process memory."""

    def __init__(self) -> None:
        self._store: dict[tuple[str, str], tuple[int, QueueState]] = {}

    def load_entry(self, key: tuple[str, str]) -> tuple[int, QueueState] | None:
        """Return a deep-copied entry when present."""
        entry = self._store.get(key)
        if entry is None:
            return None
        revision, state = entry
        return revision, deepcopy(state)

    def save_entry(self, key: tuple[str, str], expected_revision: int, updated: QueueState) -> None:
        """Persist *updated* when the expected revision still matches."""
        current_revision = self._store[key][0] if key in self._store else 0
        if current_revision != expected_revision:
            raise ConcurrentModificationError(
                f"Revision mismatch: expected {expected_revision}, got {current_revision}"
            )
        self._store[key] = (updated.revision, deepcopy(updated))

    def recovery_token(self, key: tuple[str, str]) -> str | None:
        entry = self._store.get(key)
        return str(entry[0]) if entry is not None else None

    def save_recovery_entry(self, key: tuple[str, str], expected_token: str, updated: QueueState) -> None:
        entry = self._store.get(key)
        current_token = str(entry[0]) if entry is not None else None
        if current_token != expected_token:
            raise ConcurrentModificationError("Queue state changed during recovery")
        self._store[key] = (updated.revision, deepcopy(updated))


class GitHubVariableBackingStore:
    """Backing store that persists queue state as a file on a repository ref."""

    def __init__(self, repo: str, state_ref: str = "ai-pr-loop-state") -> None:
        self._repo = repo
        self._state_ref = state_ref

    _PATH = ".agdt/ai-pr-loop-state.json"

    @staticmethod
    def _api(
        endpoint: str,
        *,
        method: str = "GET",
        body: dict[str, Any] | None = None,
    ) -> str:
        """Call GitHub with the dedicated state-writer credential when configured."""
        from agentic_devtools.cli.ci.github_provider import _gh_api

        token = os.environ.get("REPO_VARIABLE_WRITER_PAT", "").strip() or None
        return _gh_api(endpoint, method=method, body=body, token=token)

    def load_entry(self, key: tuple[str, str]) -> tuple[int, QueueState] | None:
        """Load queue state from the configured repository ref."""
        repo, state_ref = key
        endpoint = f"/repos/{repo}/contents/{self._PATH}?ref={state_ref}"
        try:
            response = self._api(endpoint)
        except RuntimeError as exc:
            if _is_not_found_error(exc):
                return None
            raise
        try:
            metadata = json.loads(response)
            encoded = metadata["content"].replace("\n", "")
            raw = base64.b64decode(encoded, validate=True)
            if len(raw) > config.MAX_STATE_SIZE_BYTES:
                raise StateTooLargeError(f"State size exceeds {config.MAX_STATE_SIZE_BYTES} bytes")
            data = queue_state_from_dict(deserialize_queue_document(raw))
        except (TypeError, ValueError, KeyError) as exc:
            raise StateDecodeError(f"Failed to decode queue state from GitHub ref {state_ref!r}: {exc}") from exc
        if not isinstance(metadata.get("sha"), str) or not metadata["sha"]:
            raise StateDecodeError("GitHub queue document did not include a blob SHA")
        return data.revision, data

    def save_entry(self, key: tuple[str, str], expected_revision: int, updated: QueueState) -> None:
        """Persist queue state using the blob SHA as a compare-and-swap token."""
        repo, state_ref = key
        endpoint = f"/repos/{repo}/contents/{self._PATH}?ref={state_ref}"
        try:
            metadata = json.loads(self._api(endpoint))
        except RuntimeError as exc:
            if _is_not_found_error(exc):
                metadata = None
            else:
                raise
        if metadata is None:
            current_revision = 0
            sha = None
        else:
            try:
                raw = base64.b64decode(metadata["content"].replace("\n", ""), validate=True)
                if len(raw) > config.MAX_STATE_SIZE_BYTES:
                    raise StateTooLargeError(f"State size exceeds {config.MAX_STATE_SIZE_BYTES} bytes")
                current_revision = queue_state_from_dict(deserialize_queue_document(raw)).revision
                sha = metadata["sha"]
            except (TypeError, ValueError, KeyError) as exc:
                raise StateDecodeError(f"Failed to decode queue state from GitHub ref {state_ref!r}: {exc}") from exc
        if current_revision != expected_revision:
            raise ConcurrentModificationError(
                f"Revision mismatch: expected {expected_revision}, got {current_revision}"
            )
        body = {
            "message": "chore: update ai-pr-loop reconciliation state",
            "content": base64.b64encode(serialize_queue_document(_state_to_dict(updated))).decode("ascii"),
            "branch": state_ref,
        }
        if sha is not None:
            body["sha"] = sha
        try:
            self._api(f"/repos/{repo}/contents/{self._PATH}", method="PUT", body=body)
        except RuntimeError as exc:
            if sha is None and _is_not_found_error(exc):
                self._create_state_ref(repo, state_ref)
                self._api(f"/repos/{repo}/contents/{self._PATH}", method="PUT", body=body)
                return
            if _is_conflict_error(exc):
                raise ConcurrentModificationError("Queue state changed during save") from exc
            raise

    def recovery_token(self, key: tuple[str, str]) -> str | None:
        """Return the current blob SHA without decoding its content."""
        repo, state_ref = key
        endpoint = f"/repos/{repo}/contents/{self._PATH}?ref={state_ref}"
        try:
            metadata = json.loads(self._api(endpoint))
        except RuntimeError as exc:
            if _is_not_found_error(exc):
                return None
            raise
        token = metadata.get("sha") if isinstance(metadata, dict) else None
        if not isinstance(token, str) or not token:
            raise StateDecodeError("GitHub queue document did not include a blob SHA")
        return token

    def save_recovery_entry(self, key: tuple[str, str], expected_token: str, updated: QueueState) -> None:
        """Replace corrupt content using its previously observed blob SHA."""
        repo, state_ref = key
        body = {
            "message": "chore: recover ai-pr-loop reconciliation state",
            "content": base64.b64encode(serialize_queue_document(_state_to_dict(updated))).decode("ascii"),
            "branch": state_ref,
            "sha": expected_token,
        }
        try:
            self._api(f"/repos/{repo}/contents/{self._PATH}", method="PUT", body=body)
        except RuntimeError as exc:
            if _is_conflict_error(exc):
                raise ConcurrentModificationError("Queue state changed during recovery") from exc
            raise

    @staticmethod
    def _create_state_ref(repo: str, state_ref: str) -> None:
        from agentic_devtools.cli.ci.github_provider import _gh_api

        token = os.environ.get("REPO_VARIABLE_WRITER_PAT", "").strip() or None
        repository = json.loads(_gh_api(f"/repos/{repo}", token=token))
        default_branch = repository.get("default_branch") if isinstance(repository, dict) else None
        if not isinstance(default_branch, str) or not default_branch:
            raise StateDecodeError("GitHub repository did not include a default branch")
        ref_data = json.loads(_gh_api(f"/repos/{repo}/git/ref/heads/{default_branch}", token=token))
        default_sha = ref_data.get("object", {}).get("sha") if isinstance(ref_data, dict) else None
        if not isinstance(default_sha, str) or not default_sha:
            raise StateDecodeError("GitHub default branch did not include a commit SHA")
        try:
            _gh_api(
                f"/repos/{repo}/git/refs",
                method="POST",
                body={"ref": f"refs/heads/{state_ref}", "sha": default_sha},
                token=token,
            )
        except RuntimeError as exc:
            if "422" not in str(exc) and "already exists" not in str(exc).lower():
                raise


class QueueStore:
    """Queue-state store with pluggable durable backing."""

    def __init__(self, repo: str, state_ref: str = "ai-pr-loop-state", backing: BackingStore | None = None) -> None:
        self._repo = repo
        self._state_ref = state_ref
        self._backing = backing or GitHubVariableBackingStore(repo, state_ref)

    @property
    def _store(self) -> dict[tuple[str, str], tuple[int, QueueState]]:
        if isinstance(self._backing, InMemoryBackingStore):
            return self._backing._store
        return {}

    def _key(self) -> tuple[str, str]:
        return (self._repo, self._state_ref)

    def ensure_state_ref(self) -> None:
        """Ensure the dedicated repository ref exists before the first load."""
        if isinstance(self._backing, GitHubVariableBackingStore):
            self._backing._create_state_ref(self._repo, self._state_ref)

    def load(self) -> QueueState:
        """Load queue state from the backing store."""
        entry = self._backing.load_entry(self._key())
        if entry is None:
            return QueueState(
                repo=self._repo,
                revision=0,
                items={},
                records=[],
                quarantines=[],
                state_ref=self._state_ref,
            )
        revision, state = entry
        self._validate_loaded_entry(revision, state)
        if state.last_updated_at is not None:
            now = datetime.now(UTC)
            age = (now - state.last_updated_at).total_seconds()
            if age > config.MAX_STATE_AGE_SECONDS:
                logger.warning(
                    "Queue state is stale (%0.fs old, max %ss); allowing recovery processing",
                    age,
                    config.MAX_STATE_AGE_SECONDS,
                )
        return deepcopy(state)

    def _check_size(self, state: QueueState) -> None:
        """Raise StateTooLargeError if the serialized state is too large."""
        payload = serialize_queue_document(_state_to_dict(state))
        if len(payload) > config.MAX_STATE_SIZE_BYTES:
            raise StateTooLargeError(f"State size exceeds {config.MAX_STATE_SIZE_BYTES} bytes")

    def save(self, state: QueueState, expected_revision: int) -> QueueState:
        """Save state with compare-and-swap on revision."""
        validate_queue_state(
            state,
            expected_repo=self._repo,
            expected_state_ref=self._state_ref,
        )
        if self.is_quarantined(state):
            raise QuarantineActiveError("State is quarantined; mutations are blocked")
        updated = _replace_state(
            state,
            revision=expected_revision + 1,
            last_updated_at=datetime.now(UTC),
        )
        validate_queue_state(
            updated,
            expected_repo=self._repo,
            expected_state_ref=self._state_ref,
        )
        self._check_size(updated)
        self._backing.save_entry(self._key(), expected_revision, updated)
        return deepcopy(updated)

    def recovery_token(self) -> str | None:
        """Return an opaque CAS token without decoding persisted state."""
        return self._backing.recovery_token(self._key())

    def save_recovery(self, state: QueueState, expected_token: str) -> QueueState:
        """Persist an authoritative replacement while retaining corruption evidence."""
        validate_queue_state(state, expected_repo=self._repo, expected_state_ref=self._state_ref)
        updated = _replace_state(state, last_updated_at=datetime.now(UTC))
        self._check_size(updated)
        self._backing.save_recovery_entry(self._key(), expected_token, updated)
        return deepcopy(updated)

    def quarantine(
        self,
        state: QueueState,
        reason: str,
        evidence: str,
    ) -> QuarantineRecord:
        """Create a quarantine record and persist it with compare-and-swap semantics."""
        validate_queue_state(
            state,
            expected_repo=self._repo,
            expected_state_ref=self._state_ref,
        )
        record = QuarantineRecord(
            quarantine_id=str(uuid4()),
            repo=self._repo,
            reason=reason,
            evidence_digest=hashlib.sha256(evidence.encode("utf-8")).hexdigest(),
            evidence=evidence,
            quarantined_at=datetime.now(UTC),
            recovery_epoch=state.recovery_epoch,
        )
        updated = _replace_state(
            state,
            quarantines=[*state.quarantines, record],
            revision=state.revision + 1,
            last_updated_at=datetime.now(UTC),
        )
        validate_queue_state(
            updated,
            expected_repo=self._repo,
            expected_state_ref=self._state_ref,
        )
        self._check_size(updated)
        self._backing.save_entry(self._key(), state.revision, updated)
        logger.warning("State quarantined: %s", reason)
        return record

    def is_quarantined(self, state: QueueState) -> bool:
        """Return True if there are active quarantine records."""
        return any(record.recovery_epoch >= state.recovery_epoch for record in state.quarantines)

    def _validate_loaded_entry(self, revision: int, state: QueueState) -> None:
        if not isinstance(revision, int) or isinstance(revision, bool):
            raise StateDecodeError(f"Persisted revision must be an int, got {type(revision).__name__}")
        if not isinstance(state, QueueState):
            raise StateDecodeError(f"Persisted queue state must be a QueueState, got {type(state).__name__}")
        if state.revision != revision:
            raise StateDecodeError(f"Persisted revision {revision} does not match QueueState.revision {state.revision}")
        try:
            validate_queue_state(
                state,
                expected_repo=self._repo,
                expected_state_ref=self._state_ref,
            )
        except ValueError as exc:
            raise StateDecodeError(f"Loaded queue state is invalid: {exc}") from exc


def _json_default(value: Any) -> Any:
    """Serialize legacy queue values for callers that import this helper."""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _is_not_found_error(exc: RuntimeError) -> bool:
    text = str(exc)
    return _contains_status_code(text, 404) or "not found" in text.lower()


def _is_conflict_error(exc: RuntimeError) -> bool:
    text = str(exc)
    return _contains_status_code(text, 409) or "does not match" in text.lower()


def _contains_status_code(text: str, code: int) -> bool:
    return re.search(_HTTP_STATUS_TOKEN_TEMPLATE.format(code=code), text) is not None


def _replace_state(state: QueueState, **kwargs: Any) -> QueueState:
    """Return a new QueueState with updated fields."""
    return replace(state, **kwargs)
