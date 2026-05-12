from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from typing import Any, Callable, MutableMapping

from .clients.capsule import SaveSessionDataRequest
from .session import (
    session_data_base_checksum,
    session_data_checksum,
    session_data_payload_json,
    session_data_revision,
    session_data_json,
)


class SessionDataCommitError(RuntimeError):
    """Raised when a session data commit is not durably accepted."""


@dataclass
class SessionDataCommit:
    data: dict[str, Any]
    data_json: str
    revision: int
    checksum: str


def session_data_snapshot(data: MutableMapping[str, Any]) -> dict[str, Any]:
    """Return a JSON-safe snapshot, preserving server-owned metadata."""
    return _object_from_json(session_data_json(data))


def _object_from_json(data_json: str) -> dict[str, Any]:
    try:
        parsed = json.loads(data_json or "{}")
    except (TypeError, json.JSONDecodeError) as exc:
        raise SessionDataCommitError(f"invalid session data JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SessionDataCommitError("session data must be a JSON object")
    return parsed


def _payload_object(data: MutableMapping[str, Any]) -> dict[str, Any]:
    return _object_from_json(session_data_payload_json(data))


def _merge_transaction(
    base_snapshot: MutableMapping[str, Any],
    desired_payload: MutableMapping[str, Any],
    current_snapshot: MutableMapping[str, Any],
) -> dict[str, Any]:
    """Apply this transaction's top-level changes to the current server snapshot."""
    base_payload = _payload_object(base_snapshot)
    merged = dict(current_snapshot)
    for key in set(base_payload) | set(desired_payload):
        same_value = desired_payload.get(key) == base_payload.get(key)
        same_presence = (key in desired_payload) == (key in base_payload)
        if same_value and same_presence:
            continue
        if key in desired_payload:
            merged[str(key)] = desired_payload[key]
        else:
            merged.pop(str(key), None)
    return merged


def _build_request(
    session_id: str,
    data: MutableMapping[str, Any],
    base_snapshot: MutableMapping[str, Any],
) -> SaveSessionDataRequest:
    payload = session_data_payload_json(data)
    payload_data = _object_from_json(payload)
    return SaveSessionDataRequest(
        session_id=session_id,
        data_json=payload,
        base_revision=session_data_revision(base_snapshot),
        base_checksum=session_data_base_checksum(base_snapshot),
        nonce=str(uuid.uuid4()),
        checksum=session_data_checksum(payload_data),
    )


def commit_session_data(
    *,
    session_id: str,
    data: MutableMapping[str, Any],
    base_snapshot: MutableMapping[str, Any],
    save_session_data: Callable[[SaveSessionDataRequest], Any],
    max_conflicts: int = 1,
) -> SessionDataCommit:
    """Commit one session-data transaction.

    Success means the server returned an accepted snapshot. Anything else is a
    hard failure so callers cannot silently clear dirty state.
    """
    working = session_data_snapshot(data)
    base = session_data_snapshot(base_snapshot)

    for attempt in range(max_conflicts + 1):
        request = _build_request(session_id, working, base)
        response = save_session_data(request)
        if response is None:
            raise SessionDataCommitError("session data save returned no response")

        data_json = getattr(response, "data_json", "") or ""
        if getattr(response, "ok", False):
            if not data_json:
                raise SessionDataCommitError("session data save succeeded without snapshot")
            accepted = _object_from_json(data_json)
            return SessionDataCommit(
                data=accepted,
                data_json=data_json,
                revision=session_data_revision(accepted),
                checksum=session_data_base_checksum(accepted),
            )

        if getattr(response, "conflict", False) and data_json and attempt < max_conflicts:
            current = _object_from_json(data_json)
            desired = _payload_object(working)
            working = _merge_transaction(base, desired, current)
            base = current
            continue

        if getattr(response, "conflict", False):
            raise SessionDataCommitError("session data CAS conflict was not accepted")
        raise SessionDataCommitError("session data save was rejected")

    raise SessionDataCommitError("session data save exceeded retry limit")
