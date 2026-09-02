"""Locked dispatch ordinal ledger and deterministic reconciliation policy."""

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from ..file_locking import locked_file
from ..state import get_state_dir

MAX_DISPATCHES_PER_SHA = 3
LEDGER_SCHEMA_VERSION = 1
_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$|^[0-9a-f]{64}$")
_SLUG_COMPONENT = r"[A-Za-z0-9._-]+"
_SLUG_PATTERN = re.compile(rf"^{_SLUG_COMPONENT}/{_SLUG_COMPONENT}$")
_MARKER_PATTERN = re.compile(
    rf"^<!-- agdt:agent-task-dispatch:v1 repo=(?P<repo>{_SLUG_COMPONENT}/{_SLUG_COMPONENT}) pr=(?P<pr>[1-9][0-9]*) "
    r"sha=(?P<sha>[0-9a-f]{40}|[0-9a-f]{64}) ordinal=(?P<ordinal>[1-3]) -->$"
)


class DispatchPolicyError(ValueError):
    """Base class for dispatch-policy validation and state errors."""


class DispatchInputError(DispatchPolicyError):
    """Raised when a dispatch identity or ordinal is invalid."""


class DispatchStateError(DispatchPolicyError):
    """Raised when the dispatch ledger is corrupt or cannot be reconciled."""


class DispatchLimitReached(DispatchPolicyError):
    """Raised when all dispatch ordinals for a SHA are consumed."""


class ReconciliationRequired(DispatchPolicyError):
    """Raised when an earlier reservation must be reconciled first."""


DispatchLimitError = DispatchLimitReached
DispatchReconciliationRequired = ReconciliationRequired


@dataclass(frozen=True)
class DispatchMarker:
    repo: str
    pull_request_id: int
    sha: str
    ordinal: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "repo": self.repo,
            "pull_request_id": self.pull_request_id,
            "sha": self.sha,
            "ordinal": self.ordinal,
        }


def _canonical_repo(repo: str) -> str:
    if not isinstance(repo, str):
        raise DispatchInputError("repo must be a non-empty owner/repo identifier")
    return repo.lower()


def _validate_identity(repo: str, pull_request_id: int, sha: str) -> None:
    if not isinstance(repo, str) or not _SLUG_PATTERN.fullmatch(repo):
        raise DispatchInputError("repo must be a non-empty owner/repo identifier")
    if isinstance(pull_request_id, bool) or not isinstance(pull_request_id, int) or pull_request_id <= 0:
        raise DispatchInputError("pull_request_id must be a positive integer")
    if not isinstance(sha, str) or not _SHA_PATTERN.fullmatch(sha):
        raise DispatchInputError("sha must be lowercase hexadecimal")


def _validate_ordinal(ordinal: int) -> None:
    if isinstance(ordinal, bool) or not isinstance(ordinal, int) or not 1 <= ordinal <= MAX_DISPATCHES_PER_SHA:
        raise DispatchInputError("ordinal must be an integer from 1 through 3")


def _validate_optional_field(value: str | None, field_name: str) -> None:
    if value is not None and not isinstance(value, str):
        raise DispatchInputError(f"{field_name} must be a string when provided")


def build_dispatch_marker(repo: str, pull_request_id: int, sha: str, ordinal: int) -> str:
    """Build the byte-stable marker used to identify one reservation."""
    repo = _canonical_repo(repo)
    _validate_identity(repo, pull_request_id, sha)
    _validate_ordinal(ordinal)
    return f"<!-- agdt:agent-task-dispatch:v1 repo={repo} pr={pull_request_id} sha={sha} ordinal={ordinal} -->"


def parse_dispatch_marker(marker: str) -> DispatchMarker:
    """Parse and strictly validate a dispatch marker."""
    if not isinstance(marker, str):
        raise DispatchInputError("marker must be a string")
    match = _MARKER_PATTERN.fullmatch(marker)
    if match is None:
        raise DispatchInputError("invalid dispatch marker")
    repo = _canonical_repo(match.group("repo"))
    pull_request_id = int(match.group("pr"))
    sha = match.group("sha")
    ordinal = int(match.group("ordinal"))
    _validate_identity(repo, pull_request_id, sha)
    _validate_ordinal(ordinal)
    return DispatchMarker(repo, pull_request_id, sha, ordinal)


def _ledger_key(repo: str, pull_request_id: int, sha: str) -> str:
    repo = _canonical_repo(repo)
    identity = json.dumps([repo, pull_request_id, sha], separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def _git_common_dir() -> Path | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-common-dir"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise DispatchStateError(f"git rev-parse --git-common-dir failed with OS error: {exc}") from exc
    if result.returncode != 0:
        if "not a git repository" in result.stderr.lower():
            return None
        raise DispatchStateError(
            f"git rev-parse --git-common-dir failed (rc={result.returncode}): {result.stderr.strip()}"
        )
    if not result.stdout.strip():
        return None
    common_dir = Path(result.stdout.strip())
    if common_dir.is_absolute():
        return common_dir
    return (Path.cwd() / common_dir).resolve()


def _ledger_path(ledger_path: Path | None) -> Path:
    if ledger_path is not None:
        return ledger_path
    common_dir = _git_common_dir()
    if common_dir is not None:
        return common_dir / "agdt" / "dispatch-policy" / "dispatch-ledger.json"
    return get_state_dir() / "dispatch-policy" / "dispatch-ledger.json"


def _is_non_bool_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _read_ledger(handle: Any, *, created: bool) -> dict[str, Any]:
    handle.seek(0)
    raw = handle.read()
    if not raw:
        if created:
            return {"schemaVersion": LEDGER_SCHEMA_VERSION, "scopes": {}}
        raise DispatchStateError("dispatch ledger is empty")
    try:
        ledger = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as exc:
        raise DispatchStateError("dispatch ledger contains malformed JSON") from exc
    schema_version = ledger.get("schemaVersion") if isinstance(ledger, dict) else None
    if not isinstance(ledger, dict) or not _is_non_bool_int(schema_version) or schema_version != LEDGER_SCHEMA_VERSION:
        raise DispatchStateError("dispatch ledger schema drift")
    scopes = ledger.get("scopes")
    if not isinstance(scopes, dict):
        raise DispatchStateError("dispatch ledger scopes must be an object")
    return ledger


def _scope(ledger: dict[str, Any], repo: str, pull_request_id: int, sha: str) -> dict[str, Any] | None:
    scope = ledger["scopes"].get(_ledger_key(repo, pull_request_id, sha))
    if scope is None:
        return None
    if not isinstance(scope, dict):
        raise DispatchStateError("dispatch ledger identity mismatch")
    scope_repo = scope.get("repo")
    if isinstance(scope_repo, str):
        scope_repo = _canonical_repo(scope_repo)
    scope_pull_request_id = scope.get("pull_request_id")
    if (
        scope_repo != repo
        or not _is_non_bool_int(scope_pull_request_id)
        or scope_pull_request_id != pull_request_id
        or scope.get("sha") != sha
        or not isinstance(scope.get("ordinals"), dict)
    ):
        raise DispatchStateError("dispatch ledger identity mismatch")
    return scope


def _write_ledger(handle: Any, ledger: dict[str, Any]) -> None:
    handle.seek(0)
    handle.write(json.dumps(ledger, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    handle.truncate()
    handle.flush()


def claim_dispatch_ordinal(
    repo: str,
    pull_request_id: int,
    sha: str,
    *,
    ledger_path: Path | None = None,
    model_id: str | None = None,
    cost: str | None = None,
    task_id: str | None = None,
) -> int:
    """Atomically reserve the first available ordinal for an identity."""
    repo = _canonical_repo(repo)
    _validate_identity(repo, pull_request_id, sha)
    _validate_optional_field(model_id, "model_id")
    _validate_optional_field(cost, "cost")
    _validate_optional_field(task_id, "task_id")
    path = _ledger_path(ledger_path)
    with locked_file(path, mode="r+", exclusive=True, encoding="utf-8", include_created=True) as locked:
        handle, created = cast(tuple[Any, bool], locked)
        ledger = _read_ledger(handle, created=created)
        scope = _scope(ledger, repo, pull_request_id, sha)
        if scope is None:
            scope = {
                "repo": repo,
                "pull_request_id": pull_request_id,
                "sha": sha,
                "ordinals": {},
            }
            ledger["scopes"][_ledger_key(repo, pull_request_id, sha)] = scope
        ordinals = scope["ordinals"]
        for ordinal_text, record in ordinals.items():
            if ordinal_text not in {"1", "2", "3"}:
                raise DispatchStateError("dispatch ledger contains an invalid ordinal")
            if not isinstance(record, dict) or record.get("status") not in {"reserved", "consumed", "released"}:
                raise DispatchStateError("dispatch ledger contains an invalid record")
            if record.get("marker") != build_dispatch_marker(repo, pull_request_id, sha, int(ordinal_text)):
                raise DispatchStateError("dispatch ledger marker does not match identity")
            if record.get("status") == "reserved":
                raise ReconciliationRequired("reconcile the earlier dispatch reservation first")
        for ordinal in range(1, MAX_DISPATCHES_PER_SHA + 1):
            record = ordinals.get(str(ordinal))
            if record is None or record.get("status") == "released":
                entry: dict[str, Any] = {
                    "status": "reserved",
                    "marker": build_dispatch_marker(repo, pull_request_id, sha, ordinal),
                }
                if model_id is not None:
                    entry["model_id"] = model_id
                if cost is not None:
                    entry["cost"] = cost
                if task_id is not None:
                    entry["task_id"] = task_id
                ordinals[str(ordinal)] = entry
                _write_ledger(handle, ledger)
                return ordinal
        raise DispatchLimitReached("maximum dispatches for this SHA have been consumed")


def reconcile_dispatch_state(
    repo: str,
    pull_request_id: int,
    sha: str,
    ordinal: int,
    *,
    marker_found: bool | None,
    task_found: bool | None,
    ledger_path: Path | None = None,
    marker: str | None = None,
) -> str:
    """Reconcile one reservation and return its resulting status."""
    repo = _canonical_repo(repo)
    _validate_identity(repo, pull_request_id, sha)
    _validate_ordinal(ordinal)
    if (marker_found is not None and not isinstance(marker_found, bool)) or (
        task_found is not None and not isinstance(task_found, bool)
    ):
        raise DispatchInputError("marker_found and task_found must be boolean or None")
    if marker is not None:
        parsed = parse_dispatch_marker(marker)
        if parsed != DispatchMarker(repo, pull_request_id, sha, ordinal):
            raise DispatchStateError("observation marker does not match reservation")
        if marker_found is False:
            raise DispatchInputError("marker_found cannot be False when a matching marker is supplied")
    path = _ledger_path(ledger_path)
    with locked_file(path, mode="r+", exclusive=True, encoding="utf-8", include_created=True) as locked:
        handle, created = cast(tuple[Any, bool], locked)
        ledger = _read_ledger(handle, created=created)
        scope = _scope(ledger, repo, pull_request_id, sha)
        if scope is None or str(ordinal) not in scope["ordinals"]:
            if created:
                _write_ledger(handle, ledger)
            raise DispatchStateError("dispatch ordinal has no reservation")
        record = scope["ordinals"][str(ordinal)]
        if not isinstance(record, dict):
            raise DispatchStateError("dispatch ledger contains an invalid record")
        expected_marker = build_dispatch_marker(repo, pull_request_id, sha, ordinal)
        if record.get("marker") != expected_marker:
            raise DispatchStateError("dispatch ledger marker does not match identity")
        current_status = record.get("status")
        observed_terminal_status = None
        if task_found is True:
            observed_terminal_status = "consumed"
        elif marker_found is False and task_found is False:
            observed_terminal_status = "released"
        if current_status in {"consumed", "released"}:
            if observed_terminal_status == current_status:
                return current_status
            raise DispatchStateError(
                f"dispatch ordinal {ordinal} is already terminal ({current_status}) and cannot be reconciled"
            )
        if current_status != "reserved":
            raise DispatchStateError("dispatch ordinal must be in reserved state to reconcile")
        if task_found is True:
            status = "consumed"
            if marker_found is False:
                record["anomaly"] = "task_without_marker"
        elif marker_found is None or task_found is None:
            status = "reserved"
        elif marker_found and not task_found:
            status = "reserved"
            record["marker_only"] = True
        else:
            status = "released"
        record["status"] = status
        _write_ledger(handle, ledger)
        return status


__all__ = [
    "DispatchInputError",
    "DispatchLimitError",
    "DispatchLimitReached",
    "DispatchMarker",
    "DispatchPolicyError",
    "DispatchReconciliationRequired",
    "ReconciliationRequired",
    "DispatchStateError",
    "MAX_DISPATCHES_PER_SHA",
    "build_dispatch_marker",
    "claim_dispatch_ordinal",
    "parse_dispatch_marker",
    "reconcile_dispatch_state",
]
