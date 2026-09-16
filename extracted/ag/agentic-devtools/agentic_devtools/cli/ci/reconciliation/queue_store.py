"""Repository-backed queue-state persistence."""

from __future__ import annotations

import base64
import hashlib
import json
import logging
import re
from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import asdict, replace
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Protocol
from uuid import uuid4

from agentic_devtools.cli.ci.credential_roles import require_default_repo_workflow_token
from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.reconciliation.models import (
    QuarantineRecord,
    QueueState,
    _history_digest,
    _legacy_digest,
    queue_state_from_dict,
    validate_queue_state,
)
from agentic_devtools.state import deserialize_queue_document, serialize_queue_document

logger = logging.getLogger(__name__)
_HTTP_STATUS_TOKEN_TEMPLATE = r"(?<!\d){code}(?!\d)"


def _decode_queue_document(raw: bytes) -> dict[str, Any]:
    """Reject duplicate keys before the legacy decoder can discard history."""

    def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate queue-document key: {key}")
            result[key] = value
        return result

    json.loads(raw, object_pairs_hook=unique_pairs)
    return deserialize_queue_document(raw)


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


class MigrationRequiredError(QueueStoreError):
    """Raised when a write crosses an unproved activation boundary."""


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

        token = require_default_repo_workflow_token("access AI PR loop queue-state repository contents")
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
            data = queue_state_from_dict(_decode_queue_document(raw))
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
                current_revision = queue_state_from_dict(_decode_queue_document(raw)).revision
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

        token = require_default_repo_workflow_token("create the AI PR loop queue-state branch")
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
        current = self.load()
        if current.revision != expected_revision or state.revision != expected_revision:
            raise ConcurrentModificationError("Queue revision changed before transition")
        self._validate_transition(current, state)
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

    @staticmethod
    def _validate_transition(current: QueueState, updated: QueueState) -> None:
        """Protect activation and append-only authority even for legacy save callers."""
        old_mode, new_mode = current.migration_status, updated.migration_status
        if old_mode == "preactivation":
            if new_mode == "preactivation":
                return
            migration = updated.migration
            history = replace(
                updated,
                evidence={
                    key: value
                    for key, value in updated.evidence.items()
                    if migration is None or key != migration.evidence_id
                },
            )
            if (
                new_mode != "prepared"
                or migration is None
                or migration.source_revision != current.revision
                or migration.source_digest != _legacy_digest(current)
                or _legacy_digest(updated) != _legacy_digest(current)
                or migration.history_digest != _history_digest(history)
            ):
                raise MigrationRequiredError("migration must bind the exact legacy source and full history")
            return
        if current.migration != updated.migration:
            raise MigrationRequiredError("migration provenance is immutable")
        if old_mode == "prepared":
            if new_mode == "prepared":
                # Legacy reconciliation remains available, but makes activation stale.
                for name in ("pr_envelopes", "obligations", "findings", "rounds", "attempts", "evidence"):
                    if getattr(current, name) != getattr(updated, name):
                        raise MigrationRequiredError("prepared history is immutable")
                return
            migration = current.migration
            assert migration is not None
            if (
                new_mode != "active"
                or current.revision != migration.prepared_revision
                or _legacy_digest(current) != migration.source_digest
                or replace(updated, migration_status="prepared") != current
            ):
                raise MigrationRequiredError("activation requires unchanged persisted preparation")
            return
        if new_mode != "active" or current.control_epoch != updated.control_epoch:
            raise MigrationRequiredError("active foundation cannot revert or change epoch through a legacy save")
        if _legacy_digest(current) != _legacy_digest(updated):
            raise MigrationRequiredError("legacy writes are disabled only after explicit activation")
        for name in ("evidence", "findings"):
            for key, value in getattr(current, name).items():
                if getattr(updated, name).get(key) != value:
                    raise ValueError(f"immutable {name} history changed")
        for pr, envelope in current.pr_envelopes.items():
            new = updated.pr_envelopes.get(pr)
            if (
                new is None
                or new.round_ids[: len(envelope.round_ids)] != envelope.round_ids
                or new.obligation_ids[: len(envelope.obligation_ids)] != envelope.obligation_ids
                or new.history_evidence_id != envelope.history_evidence_id
            ):
                raise ValueError("PR lifetime ownership/history cannot reset")
        for key, obligation in current.obligations.items():
            new_obligation = updated.obligations.get(key)
            if (
                new_obligation is None
                or new_obligation.problem_hash != obligation.problem_hash
                or new_obligation.pr_number != obligation.pr_number
                or new_obligation.finding_ids[: len(obligation.finding_ids)] != obligation.finding_ids
                or new_obligation.attempt_ids[: len(obligation.attempt_ids)] != obligation.attempt_ids
                or (
                    obligation.remediation_id is not None and new_obligation.remediation_id != obligation.remediation_id
                )
            ):
                raise ValueError("semantic problem history cannot reset")
        for key, batch in current.rounds.items():
            new_batch = updated.rounds.get(key)
            if (
                new_batch is None
                or replace(
                    new_batch,
                    phase=batch.phase,
                    publication_id=batch.publication_id,
                    review_id=batch.review_id,
                )
                != batch
            ):
                raise ValueError("immutable batch identity changed")
            transitions = {
                "prepublication": {"prepublication", "published", "invalidated"},
                "published": {"published", "reviewed", "invalidated"},
                "reviewed": {"reviewed"},
                "invalidated": {"invalidated"},
            }
            if (
                new_batch.phase not in transitions[batch.phase]
                or (batch.publication_id is not None and new_batch.publication_id != batch.publication_id)
                or (batch.review_id is not None and new_batch.review_id != batch.review_id)
            ):
                raise ValueError("batch boundary cannot rewind")
        for key, attempt in current.attempts.items():
            new_attempt = updated.attempts.get(key)
            if (
                new_attempt is None
                or replace(
                    new_attempt,
                    batch_id=attempt.batch_id,
                    observation_id=attempt.observation_id,
                    status=attempt.status,
                    acceptance_id=attempt.acceptance_id,
                    outcome_id=attempt.outcome_id,
                )
                != attempt
            ):
                raise ValueError("immutable attempt identity changed")
            if (new_attempt.batch_id, new_attempt.observation_id) != (attempt.batch_id, attempt.observation_id):
                old_envelope = current.pr_envelopes[attempt.pr_number]
                envelope = updated.pr_envelopes[attempt.pr_number]
                old_batch = current.rounds[attempt.batch_id]
                new_batch = updated.rounds[new_attempt.batch_id]
                old_input = current.evidence[attempt.observation_id]
                authority = updated.evidence[new_attempt.observation_id]
                if (
                    attempt.status != "authorized"
                    or new_attempt.status != "authorized"
                    or attempt.acceptance_id is not None
                    or old_envelope.active_batch_id != attempt.batch_id
                    or envelope.active_batch_id != new_attempt.batch_id
                    or old_envelope.observation_id != new_attempt.observation_id
                    or envelope.observation_id != new_attempt.observation_id
                    or old_envelope.hold != "none"
                    or envelope.hold != "none"
                    or new_batch.phase != "prepublication"
                    or authority.observed_at < old_input.observed_at
                    or current.obligations[attempt.obligation_id].attempt_ids[-1] != key
                ):
                    raise ValueError("only unaccepted authorized work can be rebound")
                same_scope = (old_input.head_sha, old_input.base_sha, old_input.policy_version) == (
                    authority.head_sha,
                    authority.base_sha,
                    authority.policy_version,
                )
                if new_attempt.batch_id == attempt.batch_id:
                    if old_batch.phase != "prepublication" or not same_scope:
                        raise ValueError("renewal requires active unchanged prepublication input")
                elif (
                    old_batch.phase != "invalidated"
                    or same_scope
                    or new_batch.batch_id in current.rounds
                    or new_batch.reason != "replan"
                    or new_batch.authorization_id != old_batch.batch_id
                    or new_batch.round_number != old_envelope.rounds_used + 1
                ):
                    raise ValueError("replan requires a new bounded batch replacing invalidated input")
            transitions = {
                "authorized": {"authorized", "unknown"},
                "unknown": {"unknown", "authorized", "accepted"},
                "accepted": {"accepted", "failed", "succeeded"},
                "failed": {"failed"},
                "succeeded": {"succeeded"},
            }
            if (
                new_attempt.status not in transitions[attempt.status]
                or (attempt.acceptance_id is not None and new_attempt.acceptance_id != attempt.acceptance_id)
                or (attempt.outcome_id is not None and new_attempt.outcome_id != attempt.outcome_id)
            ):
                raise ValueError("accepted work/outcome cannot rewind")
            if attempt.status == "unknown" and new_attempt.status == "authorized":
                if not any(
                    proof.kind == "absence"
                    and proof.subject == key
                    and proof.pr_number == attempt.pr_number
                    and proof.related_id == attempt.observation_id
                    and proof.after == "not_accepted"
                    and proof.evidence_id not in current.evidence
                    for proof in updated.evidence.values()
                ):
                    raise ValueError("dispatch uncertainty requires new independently verified absence")
        for key, attempt in updated.attempts.items():
            if key not in current.attempts and attempt.status != "authorized":
                raise ValueError("persist attempt authorization before acceptance")
        for key, batch in updated.rounds.items():
            if key not in current.rounds and (
                batch.phase != "prepublication" or batch.publication_id or batch.review_id
            ):
                raise ValueError("persist round admission before publication/review")
            if key not in current.rounds and batch.reason == "replan":
                if not any(
                    attempt_id in current.attempts
                    and current.attempts[attempt_id].batch_id == batch.authorization_id
                    and attempt.batch_id == key
                    for attempt_id, attempt in updated.attempts.items()
                ):
                    raise ValueError("replan requires retained known-unaccepted work")
        if updated.global_epoch not in {current.global_epoch, current.global_epoch + 1}:
            raise ValueError("global admission epoch cannot revert or skip")
        if updated.global_epoch == current.global_epoch + 1:
            if f"epoch:{updated.global_epoch}" not in updated.audit_refs:
                raise ValueError("global admission epoch requires advance_epoch")
            for pr, controller in current.controllers.items():
                replacement = updated.controllers.get(pr)
                if replacement is None or replacement.global_epoch != updated.global_epoch:
                    raise ValueError("epoch advancement must refresh controller projections")
        if not set(current.permit_requests).issubset(updated.permit_requests):
            raise ValueError("permit request history cannot be deleted")
        for key, request in current.permit_requests.items():
            new_request = updated.permit_requests.get(key)
            if new_request is None or (
                new_request.request_id,
                new_request.repo,
                new_request.pr_number,
                new_request.obligation_id,
                new_request.batch_id,
                new_request.worker_id,
                new_request.provider,
                new_request.model,
                new_request.owner_epoch,
                new_request.queue_position,
                new_request.requested_at,
                new_request.deadline_at,
            ) != (
                request.request_id,
                request.repo,
                request.pr_number,
                request.obligation_id,
                request.batch_id,
                request.worker_id,
                request.provider,
                request.model,
                request.owner_epoch,
                request.queue_position,
                request.requested_at,
                request.deadline_at,
            ):
                raise ValueError("immutable permit request identity changed")
            transitions = {
                "queued": {"queued", "reserved", "cancelled"},
                "reserved": {"reserved", "unknown", "cancelled"},
                "unknown": {"unknown", "accepted", "released"},
                "accepted": {"accepted", "released"},
                "released": {"released"},
                "cancelled": {"cancelled"},
            }
            if new_request.status not in transitions[request.status]:
                raise ValueError("permit request cannot rewind")
            if (
                request.terminal_evidence_id is not None
                and new_request.terminal_evidence_id != request.terminal_evidence_id
            ):
                raise ValueError("request terminal evidence is immutable")
            if new_request.status == "released":
                if (
                    new_request.terminal_evidence_id is None
                    or new_request.terminal_evidence_id not in updated.evidence
                    or new_request.permit_id is None
                    or new_request.permit_id not in updated.active_permits
                    or new_request.terminal_evidence_id
                    != updated.active_permits[new_request.permit_id].terminal_evidence_id
                ):
                    raise ValueError("released request requires authoritative terminal evidence")
        for key, request in updated.permit_requests.items():
            if key not in current.permit_requests and request.status != "queued":
                raise ValueError("new permit request must be queued before admission")
        for key, permit in current.active_permits.items():
            new_permit = updated.active_permits.get(key)
            if new_permit is None or replace(
                new_permit,
                status=permit.status,
                remote_task_id=permit.remote_task_id,
                remote_session_id=permit.remote_session_id,
                acceptance_evidence_id=None,
                terminal_evidence_id=None,
            ) != replace(
                permit,
                status=permit.status,
                remote_task_id=permit.remote_task_id,
                remote_session_id=permit.remote_session_id,
                acceptance_evidence_id=None,
                terminal_evidence_id=None,
            ):
                raise ValueError("immutable permit identity changed")
            transitions = {
                "reserved": {"reserved", "unknown", "cancelled"},
                "unknown": {"unknown", "accepted", "released"},
                "accepted": {"accepted", "released"},
                "released": {"released"},
                "cancelled": {"cancelled"},
            }
            if new_permit.status not in transitions[permit.status]:
                raise ValueError("permit cannot rewind")
            if permit.remote_task_id is not None and new_permit.remote_task_id != permit.remote_task_id:
                raise ValueError("accepted remote task identity changed")
            if permit.remote_session_id is not None and new_permit.remote_session_id != permit.remote_session_id:
                raise ValueError("accepted remote session identity changed")
            if (
                permit.acceptance_evidence_id is not None
                and new_permit.acceptance_evidence_id != permit.acceptance_evidence_id
            ):
                raise ValueError("acceptance evidence is immutable")
            if (
                permit.terminal_evidence_id is not None
                and new_permit.terminal_evidence_id != permit.terminal_evidence_id
            ):
                raise ValueError("permit terminal evidence is immutable")
            if new_permit.status == "accepted" and (
                new_permit.acceptance_evidence_id is None
                or new_permit.acceptance_evidence_id not in updated.evidence
                or updated.evidence[new_permit.acceptance_evidence_id].kind != "acceptance"
                or updated.evidence[new_permit.acceptance_evidence_id].after != permit.model
            ):
                raise ValueError("accepted permit requires authoritative acceptance evidence")
            if new_permit.status == "released":
                if new_permit.terminal_evidence_id is None or new_permit.terminal_evidence_id not in updated.evidence:
                    raise ValueError("released permit requires authoritative terminal evidence")
                evidence = updated.evidence[new_permit.terminal_evidence_id]
                if (
                    evidence.subject != permit.request_id
                    or evidence.related_id != permit.permit_id
                    or (permit.status == "unknown" and (evidence.kind != "absence" or evidence.after != "not_accepted"))
                    or (
                        permit.status == "accepted"
                        and (evidence.kind not in {"failure", "success"} or evidence.before != "terminal")
                    )
                ):
                    raise ValueError("released permit requires bound terminal evidence")
        for key, permit in updated.active_permits.items():
            if key not in current.active_permits and permit.status != "reserved":
                raise ValueError("persist reservation before worker acceptance")
        if not set(current.effects).issubset(updated.effects):
            raise ValueError("effect history cannot be deleted")
        for key, effect in current.effects.items():
            new_effect = updated.effects.get(key)
            if new_effect is None or (
                new_effect.repo,
                new_effect.pr_number,
                new_effect.kind,
                new_effect.payload_digest,
            ) != (effect.repo, effect.pr_number, effect.kind, effect.payload_digest):
                raise ValueError("immutable effect intent changed")
            if effect.status != new_effect.status and effect.status != "intent":
                raise ValueError("effect history cannot rewind")
        for key, effect in updated.effects.items():
            if key not in current.effects and effect.status != "intent":
                raise ValueError("persist effect intent before settlement")

    def transact(
        self,
        transition: Callable[[QueueState], QueueState],
        *,
        expected_revision: int | None = None,
    ) -> QueueState:
        """Apply one deterministic transition through the single-document CAS boundary."""
        state = self.load()
        revision = state.revision if expected_revision is None else expected_revision
        if revision != state.revision:
            raise ConcurrentModificationError(f"Revision mismatch: expected {revision}, got {state.revision}")
        updated = transition(deepcopy(state))
        if not isinstance(updated, QueueState):
            raise TypeError(f"Queue transition must return QueueState, got {type(updated).__name__}")
        return self.save(updated, expected_revision=revision)

    def recovery_token(self) -> str | None:
        """Return an opaque CAS token without decoding persisted state."""
        return self._backing.recovery_token(self._key())

    def save_recovery(self, state: QueueState, expected_token: str) -> QueueState:
        """Persist an authoritative replacement while retaining corruption evidence."""
        validate_queue_state(state, expected_repo=self._repo, expected_state_ref=self._state_ref)
        if state.migration_status != "preactivation":
            raise MigrationRequiredError("corrupt recovery cannot assert known new-mode budgets")
        try:
            existing = self._backing.load_entry(self._key())
        except (StateDecodeError, StateTooLargeError):
            existing = None
        if existing is not None and existing[1].migration_status != "preactivation":
            raise MigrationRequiredError("legacy recovery cannot erase a readable foundation history")
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
        current = self.load()
        if current.revision != state.revision:
            raise ConcurrentModificationError("Queue state changed before quarantine")
        self._validate_transition(current, state)
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
