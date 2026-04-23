"""Versioned backup and restore history for personal config.

Creates timestamped snapshots of ``~/.anteroom/config.yaml`` before every
managed write and on startup when an external edit is detected.  Snapshots are
stored as plain YAML files under ``~/.anteroom/backups/config/`` and indexed
by an append-only JSONL manifest.

Scope: personal config only (V1).  Project and space configs are intentionally
excluded — if those are ever added the manifest design must become path-keyed.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import logging
import os
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import IO

try:
    import fcntl as _fcntl
except ImportError:  # Windows
    _fcntl = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

_MANIFEST_NAME = "history.jsonl"
_BACKUP_DIR_MODE = 0o700
_BACKUP_FILE_MODE = 0o600


@dataclass
class ConfigHistoryEntry:
    id: str
    timestamp: str  # ISO 8601, UTC
    source: str
    sha256: str
    path: str  # relative to backup_dir


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _lock(f: "IO[str]") -> None:  # noqa: F821
    if _fcntl is not None:
        _fcntl.flock(f, _fcntl.LOCK_EX)


def _unlock(f: "IO[str]") -> None:  # noqa: F821
    if _fcntl is not None:
        _fcntl.flock(f, _fcntl.LOCK_UN)


# ---------------------------------------------------------------------------
# Public service
# ---------------------------------------------------------------------------


def get_backup_dir(anteroom_dir: Path) -> Path:
    """Return ``anteroom_dir/backups/config``."""
    return anteroom_dir / "backups" / "config"


class ConfigHistoryService:
    """Snapshot-based history for a single personal config file."""

    def __init__(self, backup_dir: Path) -> None:
        self._backup_dir = backup_dir
        self._manifest = backup_dir / _MANIFEST_NAME
        backup_dir.mkdir(parents=True, exist_ok=True)
        try:
            backup_dir.chmod(_BACKUP_DIR_MODE)
        except OSError:
            pass

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def snapshot(self, config_path: Path, source: str) -> ConfigHistoryEntry | None:
        """Snapshot *config_path* into history.

        Skips the write if the file hash matches the most recent entry (dedup).
        Returns ``None`` if *config_path* does not exist.
        """
        if not config_path.exists():
            return None

        current_hash = _sha256(config_path)

        # Dedup: skip if same content as last snapshot
        last = self._last_entry()
        if last and last.sha256 == current_hash:
            return last

        now = datetime.now(timezone.utc)
        ts = now.strftime("%Y%m%dT%H%M%SZ")
        entry_id = f"{ts}-{current_hash[:8]}"
        backup_name = f"config-{entry_id}.yaml"
        backup_path = self._backup_dir / backup_name

        shutil.copyfile(config_path, backup_path)  # data only, no metadata/permission inheritance
        try:
            backup_path.chmod(_BACKUP_FILE_MODE)
        except OSError:
            pass

        entry = ConfigHistoryEntry(
            id=entry_id,
            timestamp=now.isoformat(),
            source=source,
            sha256=current_hash,
            path=backup_name,
        )
        self._append_entry(entry)
        return entry

    def list_versions(self) -> list[ConfigHistoryEntry]:
        """Return all history entries, newest first."""
        entries = self._read_manifest()
        return list(reversed(entries))

    def diff(self, version_id: str, current_path: Path) -> str:
        """Return a unified diff between *version_id* backup and *current_path*."""
        entry = self._find_entry(version_id)
        backup_path = self._resolve_backup_path(entry)
        backup_lines = backup_path.read_text(encoding="utf-8").splitlines(keepends=True)
        current_lines = (
            current_path.read_text(encoding="utf-8").splitlines(keepends=True) if current_path.exists() else []
        )
        return "".join(
            difflib.unified_diff(
                backup_lines,
                current_lines,
                fromfile=f"backup/{entry.id}",
                tofile="current",
            )
        )

    def restore(self, version_id: str, target_path: Path) -> None:
        """Restore *version_id* to *target_path*.

        Snapshots the current state first so the restore itself is undoable.
        """
        entry = self._find_entry(version_id)
        backup_path = self._resolve_backup_path(entry)

        # Make the current state undoable
        self.snapshot(target_path, source="pre-restore")

        # Atomic copy
        target_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path_str = tempfile.mkstemp(dir=target_path.parent, suffix=".tmp")
        tmp = Path(tmp_path_str)
        try:
            os.close(fd)
            shutil.copyfile(backup_path, tmp)  # data only, no metadata/permission inheritance
            try:
                tmp.chmod(_BACKUP_FILE_MODE)
            except OSError:
                pass
            os.replace(tmp_path_str, target_path)
        except BaseException:
            tmp.unlink(missing_ok=True)
            raise

    def detect_and_snapshot_external_edit(self, config_path: Path) -> bool:
        """Snapshot if *config_path* differs from the last recorded hash.

        Called at startup to capture edits made while Anteroom was not running.
        Returns ``True`` if a new snapshot was created.

        Uses source ``"external"`` when a prior entry exists (true external
        edit) and ``"initial"`` when the manifest is empty — a first-seen
        config cannot have been edited externally because Anteroom has no
        prior record of it.
        """
        if not config_path.exists():
            return False
        current_hash = _sha256(config_path)
        last = self._last_entry()
        if last and last.sha256 == current_hash:
            return False
        source = "external" if last is not None else "initial"
        result = self.snapshot(config_path, source=source)
        return result is not None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read_manifest(self) -> list[ConfigHistoryEntry]:
        if not self._manifest.exists():
            return []
        entries: list[ConfigHistoryEntry] = []
        with open(self._manifest, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    if not isinstance(d, dict):
                        raise TypeError("manifest entry is not an object")
                    entries.append(
                        ConfigHistoryEntry(
                            id=d["id"],
                            timestamp=d["timestamp"],
                            source=d["source"],
                            sha256=d["sha256"],
                            path=d["path"],
                        )
                    )
                except (KeyError, TypeError, json.JSONDecodeError):
                    logger.warning("Skipping malformed config history entry: %r", line)
        return entries

    def _last_entry(self) -> ConfigHistoryEntry | None:
        entries = self._read_manifest()
        return entries[-1] if entries else None

    def _find_entry(self, version_id: str) -> ConfigHistoryEntry:
        for entry in self._read_manifest():
            if entry.id == version_id:
                return entry
        raise KeyError(f"Config history version not found: {version_id!r}")

    def _resolve_backup_path(self, entry: ConfigHistoryEntry) -> Path:
        """Return the resolved backup path, raising ValueError if outside backup_dir."""
        resolved = (self._backup_dir / entry.path).resolve()
        if not resolved.is_relative_to(self._backup_dir.resolve()):
            raise ValueError(f"Unsafe backup path in manifest: {entry.path!r}")
        return resolved

    def _append_entry(self, entry: ConfigHistoryEntry) -> None:
        row = json.dumps(
            {
                "id": entry.id,
                "timestamp": entry.timestamp,
                "source": entry.source,
                "sha256": entry.sha256,
                "path": entry.path,
            }
        )
        self._manifest.parent.mkdir(parents=True, exist_ok=True)
        with open(self._manifest, "a", encoding="utf-8") as f:
            _lock(f)
            try:
                f.write(row + "\n")
                f.flush()
                os.fsync(f.fileno())
            finally:
                _unlock(f)
