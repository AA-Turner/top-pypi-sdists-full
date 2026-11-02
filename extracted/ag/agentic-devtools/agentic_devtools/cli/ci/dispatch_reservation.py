"""Single-writer reservations for concurrent repair dispatches."""

from __future__ import annotations

import json
import re
from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import IO, Literal, Protocol, cast

from agentic_devtools.cli.ci.dispatch_state import MAX_DISPATCHES_PER_SHA
from agentic_devtools.file_locking import locked_file
from agentic_devtools.state import get_state_dir

_OWNER_RE = re.compile(r"^[0-9]+-[0-9]+-[0-9a-f]{8}$")
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_REPO_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*$")
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$")
_RESERVATION_KEYS = frozenset(
    {"repo", "pull_request_id", "sha", "ordinal", "owner", "state", "created_at", "schema_version"}
)
_STORE_KEYS = frozenset({"schema_version", "reservations"})
_RESERVATION_FILENAME = "dispatch-ordinals.json"


class FileOperationsProtocol(Protocol):
    """Filesystem seam used by deterministic reservation tests."""

    def locked_file(self, path: Path) -> AbstractContextManager[IO[str]]:
        """Return an exclusive context manager for *path*."""


@dataclass(frozen=True, slots=True)
class DispatchReservation:
    """The closed, immutable schema for one ordinal reservation."""

    repo: str
    pull_request_id: int
    sha: str
    ordinal: int
    owner: str
    state: Literal["reserved"]
    created_at: str
    schema_version: Literal[1]

    def __post_init__(self) -> None:
        if not isinstance(self.repo, str) or not _REPO_RE.fullmatch(self.repo):
            raise ValueError("repo must be a canonical owner/name repository identifier")
        if (
            isinstance(self.pull_request_id, bool)
            or not isinstance(self.pull_request_id, int)
            or self.pull_request_id <= 0
        ):
            raise ValueError("pull_request_id must be a positive integer")
        if not isinstance(self.sha, str) or not _SHA_RE.fullmatch(self.sha):
            raise ValueError("sha must be a complete lowercase 40-character hexadecimal SHA")
        if (
            isinstance(self.ordinal, bool)
            or not isinstance(self.ordinal, int)
            or not 1 <= self.ordinal <= MAX_DISPATCHES_PER_SHA
        ):
            raise ValueError("ordinal must be one of the three dispatch ordinals")
        if not isinstance(self.owner, str) or not _OWNER_RE.fullmatch(self.owner):
            raise ValueError("owner has an invalid format")
        if self.state != "reserved":
            raise ValueError("state must be reserved")
        if not isinstance(self.created_at, str) or not _TIMESTAMP_RE.fullmatch(self.created_at):
            raise ValueError("created_at must be UTC ISO-8601 with microsecond precision")
        try:
            datetime.fromisoformat(self.created_at[:-1] + "+00:00")
        except ValueError as exc:
            raise ValueError("created_at must be a valid UTC timestamp") from exc
        if (
            not isinstance(self.schema_version, int)
            or isinstance(self.schema_version, bool)
            or self.schema_version != 1
        ):
            raise ValueError("schema_version must be 1")

    def to_dict(self) -> dict[str, object]:
        """Serialize the closed record schema."""
        return {
            "repo": self.repo,
            "pull_request_id": self.pull_request_id,
            "sha": self.sha,
            "ordinal": self.ordinal,
            "owner": self.owner,
            "state": self.state,
            "created_at": self.created_at,
            "schema_version": self.schema_version,
        }

    @classmethod
    def from_dict(cls, value: object) -> DispatchReservation:
        """Validate and deserialize one closed reservation record."""
        if not isinstance(value, dict) or set(value) != _RESERVATION_KEYS:
            raise ValueError("reservation record has an invalid schema")
        return cls(
            repo=cast(str, value["repo"]),
            pull_request_id=cast(int, value["pull_request_id"]),
            sha=cast(str, value["sha"]),
            ordinal=cast(int, value["ordinal"]),
            owner=cast(str, value["owner"]),
            state=cast(Literal["reserved"], value["state"]),
            created_at=cast(str, value["created_at"]),
            schema_version=cast(Literal[1], value["schema_version"]),
        )


@dataclass(frozen=True, slots=True)
class AcquiredResult:
    """Successful reservation acquisition."""

    reservation: DispatchReservation


@dataclass(frozen=True, slots=True)
class LostRaceResult:
    """A contender that must stop before reaching the provider boundary."""

    reason: Literal["already_reserved", "read_back_failed"]


@dataclass(frozen=True, slots=True)
class ExhaustedResult:
    """The requested ordinal is outside the canonical eligibility set."""

    reason: Literal["exhausted"] = "exhausted"


ReservationResult = AcquiredResult | LostRaceResult | ExhaustedResult


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _reservation_path() -> Path:
    return get_state_dir() / _RESERVATION_FILENAME


def _request_key(repo: str, pull_request_id: int, sha: str, ordinal: int) -> str:
    return f"{repo}|{pull_request_id}|{sha}|{ordinal}"


def _decode_store(content: str) -> dict[str, object]:
    if not content.strip():
        return {}
    try:
        raw = json.loads(content, object_pairs_hook=_reject_duplicate_keys)
    except json.JSONDecodeError as exc:
        raise ValueError("reservation store is not valid JSON") from exc
    if (
        not isinstance(raw, dict)
        or set(raw) != _STORE_KEYS
        or not isinstance(raw.get("schema_version"), int)
        or isinstance(raw.get("schema_version"), bool)
        or raw["schema_version"] != 1
    ):
        raise ValueError("reservation store has an invalid schema")
    reservations = raw.get("reservations")
    if not isinstance(reservations, dict):
        raise ValueError("reservations must be an object")
    result: dict[str, object] = {}
    for key, value in reservations.items():
        if not isinstance(value, dict):
            raise ValueError("reservation store contains an invalid record")
        reservation = DispatchReservation.from_dict(value)
        if (
            key != _request_key(reservation.repo, reservation.pull_request_id, reservation.sha, reservation.ordinal)
            or key in result
        ):
            raise ValueError("reservation key does not match its record")
        result[key] = reservation
    return result


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("reservation store contains duplicate keys")
        result[key] = value
    return result


def _encode_store(reservations: dict[str, DispatchReservation]) -> str:
    return (
        json.dumps(
            {
                "schema_version": 1,
                "reservations": {key: reservation.to_dict() for key, reservation in reservations.items()},
            },
            indent=2,
        )
        + "\n"
    )


def _locked(path: Path, file_ops: FileOperationsProtocol | None) -> AbstractContextManager[IO[str]]:
    if file_ops is not None:
        return file_ops.locked_file(path)
    return cast(AbstractContextManager[IO[str]], locked_file(path, "r+", exclusive=True, encoding="utf-8"))


def acquire_reservation(
    repo: str,
    pull_request_id: int,
    sha: str,
    ordinal: int,
    owner: str,
    *,
    file_ops: FileOperationsProtocol | None = None,
) -> ReservationResult:
    """Atomically reserve an eligible dispatch ordinal and verify ownership."""
    if not isinstance(repo, str) or not _REPO_RE.fullmatch(repo):
        raise ValueError("repo must be a canonical owner/name repository identifier")
    if isinstance(ordinal, bool) or not isinstance(ordinal, int) or ordinal < 1 or ordinal > MAX_DISPATCHES_PER_SHA:
        return ExhaustedResult()
    # Constructing the record performs all remaining request validation before any write.
    timestamp = _now()
    reservation = DispatchReservation(repo, pull_request_id, sha, ordinal, owner, "reserved", timestamp, 1)
    key = _request_key(repo, pull_request_id, sha, ordinal)
    with _locked(_reservation_path(), file_ops) as handle:
        handle.seek(0)
        reservations = _decode_store(handle.read())
        existing = cast(DispatchReservation | None, reservations.get(key))
        if existing is not None:
            if existing.owner != owner:
                return LostRaceResult("already_reserved")
            reservation = existing
        else:
            reservations[key] = reservation
            handle.seek(0)
            handle.write(_encode_store(cast(dict[str, DispatchReservation], reservations)))
            handle.truncate()
            handle.flush()
        handle.seek(0)
        try:
            read_back = _decode_store(handle.read()).get(key)
        except ValueError:
            return LostRaceResult("read_back_failed")
        if not isinstance(read_back, DispatchReservation) or read_back.owner != owner:
            return LostRaceResult("read_back_failed")
        return AcquiredResult(read_back)
