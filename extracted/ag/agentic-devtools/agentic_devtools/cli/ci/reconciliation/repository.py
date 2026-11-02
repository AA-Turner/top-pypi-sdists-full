"""Durable reconciliation manifest repository with CAS and archive shards."""

from __future__ import annotations

import json
import re
from contextlib import contextmanager
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from types import ModuleType
from typing import Any

from agentic_devtools.cli.ci.reconciliation.config import MAX_STATE_SIZE_BYTES

_fcntl_module: ModuleType | None
try:
    import fcntl as _fcntl_module
except ImportError:  # pragma: no cover - Windows uses the atomic replacement fallback
    _fcntl_module = None  # type: ignore[assignment]

_ACTIVE_HISTORY_LIMITS = {
    "observations": 32,
    "decisions": 32,
    "invalidations": 32,
    "leases": 16,
}
_MAX_ENTRY_BYTES = 16_384
_MAX_FREE_TEXT_BYTES = 4_096
_SHARD_MAX_BYTES = 262_144


class ManifestConflictError(RuntimeError):
    """Raised when saving with a stale revision."""


class ManifestOverflowError(RuntimeError):
    """Raised when immutable history cannot fit policy constraints."""


class MissingArchiveShardError(RuntimeError):
    """Raised when manifest pointers reference missing shard content."""


@dataclass(frozen=True)
class TruncationAudit:
    """Metadata describing deterministic truncation."""

    field_name: str
    original_bytes: int
    discarded_sha256: str


@dataclass(frozen=True)
class ArchiveShardPointer:
    """Pointer metadata for one append-only archive shard."""

    shard_id: str
    entry_count: int
    content_sha256: str
    size_bytes: int


@dataclass
class ReconciliationManifest:
    """Active reconciliation manifest persisted with CAS semantics."""

    repo: str
    revision: int
    inventory: dict[str, dict[str, Any]] = field(default_factory=dict)
    ledgers: dict[str, dict[str, Any]] = field(default_factory=dict)
    archive_pointers: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    overflow_alerts: list[str] = field(default_factory=list)


class FileBackedReconciliationRepository:
    """File-backed durable store for trusted reconciliation state."""

    def __init__(self, root: Path, *, repo: str) -> None:
        self._root = root
        self._repo = repo
        self._manifest_path = root / "manifest.json"
        self._archive_dir = root / "archive"

    def load(self) -> ReconciliationManifest:
        """Load manifest from disk or return an empty one."""
        if not self._manifest_path.exists():
            return ReconciliationManifest(repo=self._repo, revision=0)
        data = json.loads(self._manifest_path.read_text(encoding="utf-8"))
        manifest = ReconciliationManifest(
            repo=data.get("repo", self._repo),
            revision=int(data.get("revision", 0)),
            inventory=dict(data.get("inventory", {})),
            ledgers=dict(data.get("ledgers", {})),
            archive_pointers={key: list(value) for key, value in dict(data.get("archive_pointers", {})).items()},
            overflow_alerts=list(data.get("overflow_alerts", [])),
        )
        self.assert_archive_integrity(manifest)
        return manifest

    def save(self, manifest: ReconciliationManifest, *, expected_revision: int) -> ReconciliationManifest:
        """Save manifest using revision-based compare-and-swap semantics."""
        with self._exclusive_lock():
            current = self.load()
            if current.revision != expected_revision:
                raise ManifestConflictError(f"revision mismatch: expected {expected_revision}, got {current.revision}")
            updated = ReconciliationManifest(
                repo=manifest.repo,
                revision=expected_revision + 1,
                inventory=manifest.inventory,
                ledgers=manifest.ledgers,
                archive_pointers=manifest.archive_pointers,
                overflow_alerts=manifest.overflow_alerts,
            )
            serialized = _serialize_manifest(updated)
            if len(serialized.encode("utf-8")) > MAX_STATE_SIZE_BYTES:
                raise ManifestOverflowError("manifest exceeds MAX_STATE_SIZE_BYTES")
            self._manifest_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = self._manifest_path.with_suffix(".json.new")
            temp_path.write_text(serialized, encoding="utf-8")
            temp_path.replace(self._manifest_path)
            return updated

    @contextmanager
    def _exclusive_lock(self):
        """Serialize manifest read/check/write sequences across reconciliation processes."""
        self._manifest_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self._manifest_path.with_suffix(".lock")
        with lock_path.open("a+", encoding="utf-8") as lock_file:
            if _fcntl_module is not None:  # pragma: no branch
                _fcntl_module.flock(lock_file.fileno(), _fcntl_module.LOCK_EX)
            try:
                yield
            finally:
                if _fcntl_module is not None:  # pragma: no branch
                    _fcntl_module.flock(lock_file.fileno(), _fcntl_module.LOCK_UN)

    def append_immutable_entry(
        self,
        *,
        manifest: ReconciliationManifest,
        record_id: str,
        channel: str,
        entry: dict[str, Any],
    ) -> ReconciliationManifest:
        """Append immutable history and roll old entries into archive shards."""
        if channel not in _ACTIVE_HISTORY_LIMITS:
            raise ValueError(f"unsupported channel: {channel}")
        self.assert_archive_integrity(manifest)
        normalized_entry = normalize_immutable_entry(entry)
        if len(_serialize_json(normalized_entry).encode("utf-8")) > _MAX_ENTRY_BYTES:
            raise ManifestOverflowError("normalized immutable entry exceeds size cap")

        next_manifest = ReconciliationManifest(
            repo=manifest.repo,
            revision=manifest.revision,
            inventory=dict(manifest.inventory),
            ledgers=json.loads(json.dumps(manifest.ledgers)),
            archive_pointers={k: list(v) for k, v in manifest.archive_pointers.items()},
            overflow_alerts=list(manifest.overflow_alerts),
        )
        ledger = dict(next_manifest.ledgers.get(record_id, {}))
        history = list(ledger.get(channel, []))
        history.append(normalized_entry)

        while len(history) > _ACTIVE_HISTORY_LIMITS[channel]:
            oldest = history.pop(0)
            pointer = self._write_archive_shard(record_id=record_id, entries=[oldest])
            next_manifest.archive_pointers.setdefault(record_id, []).append(pointer)

        ledger[channel] = history
        next_manifest.ledgers[record_id] = ledger

        payload = _serialize_manifest(next_manifest)
        if len(payload.encode("utf-8")) > int(MAX_STATE_SIZE_BYTES * 0.75):
            while history:
                pointer = self._write_archive_shard(record_id=record_id, entries=[history.pop(0)])
                next_manifest.archive_pointers.setdefault(record_id, []).append(pointer)
                ledger[channel] = history
                payload = _serialize_manifest(next_manifest)
                if len(payload.encode("utf-8")) <= int(MAX_STATE_SIZE_BYTES * 0.75):
                    break
            if len(payload.encode("utf-8")) > MAX_STATE_SIZE_BYTES:
                raise ManifestOverflowError("manifest cannot fit after archive rollover")
        return next_manifest

    def assert_archive_integrity(self, manifest: ReconciliationManifest) -> None:
        """Fail closed when any manifest pointer references missing shard content."""
        for pointers in manifest.archive_pointers.values():
            for pointer in pointers:
                if not isinstance(pointer, dict):
                    raise MissingArchiveShardError("invalid archive shard pointer")
                shard_id = pointer.get("shard_id")
                if not isinstance(shard_id, str) or re.fullmatch(r"[0-9a-f]{24}", shard_id) is None:
                    raise MissingArchiveShardError("invalid archive shard identifier")
                shard_path = self._archive_dir / f"{shard_id}.json"
                if not shard_path.exists():
                    raise MissingArchiveShardError(f"missing archive shard: {shard_id}")
                payload_bytes = shard_path.read_bytes()
                if pointer.get("size_bytes") != len(payload_bytes):
                    raise MissingArchiveShardError(f"archive shard size mismatch: {shard_id}")
                if pointer.get("content_sha256") != sha256(payload_bytes).hexdigest():
                    raise MissingArchiveShardError(f"archive shard digest mismatch: {shard_id}")
                try:
                    entries = json.loads(payload_bytes)
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise MissingArchiveShardError(f"invalid archive shard: {shard_id}") from exc
                if not isinstance(entries, list) or pointer.get("entry_count") != len(entries):
                    raise MissingArchiveShardError(f"archive shard entry-count mismatch: {shard_id}")

    def _write_archive_shard(self, *, record_id: str, entries: list[dict[str, Any]]) -> dict[str, Any]:
        payload = _serialize_json(entries)
        payload_bytes = payload.encode("utf-8")
        if len(payload_bytes) > _SHARD_MAX_BYTES:
            raise ManifestOverflowError("archive shard exceeds size cap")
        digest = sha256(payload_bytes).hexdigest()
        shard_id = sha256(f"{record_id}:{digest}".encode()).hexdigest()[:24]
        self._archive_dir.mkdir(parents=True, exist_ok=True)
        shard_path = self._archive_dir / f"{shard_id}.json"
        if not shard_path.exists():
            shard_path.write_text(payload, encoding="utf-8")
        return {
            "shard_id": shard_id,
            "entry_count": len(entries),
            "content_sha256": digest,
            "size_bytes": len(payload_bytes),
        }


def normalize_immutable_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """Normalize immutable entries with deterministic truncation metadata."""
    normalized = dict(entry)
    truncation_audits: list[dict[str, Any]] = []
    for key, value in list(normalized.items()):
        if isinstance(value, str):
            raw = value.encode("utf-8")
            if len(raw) > _MAX_FREE_TEXT_BYTES:
                value_text = raw[:_MAX_FREE_TEXT_BYTES].decode("utf-8", errors="ignore")
                normalized[key] = value_text
                truncation_audits.append(
                    {
                        "field_name": key,
                        "original_bytes": len(raw),
                        "discarded_sha256": sha256(raw).hexdigest(),
                    }
                )
    if truncation_audits:
        normalized["_truncation"] = truncation_audits
    return normalized


def _serialize_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _serialize_manifest(manifest: ReconciliationManifest) -> str:
    return _serialize_json(
        {
            "repo": manifest.repo,
            "revision": manifest.revision,
            "inventory": manifest.inventory,
            "ledgers": manifest.ledgers,
            "archive_pointers": manifest.archive_pointers,
            "overflow_alerts": manifest.overflow_alerts,
        }
    )
