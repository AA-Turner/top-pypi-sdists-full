"""Per-message file history for SmartChat rollback."""

from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import shutil
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from abstra_internals.logger import AbstraLogger
from abstra_internals.settings import Settings

MAX_SNAPSHOTS = 50
BACKUP_DIRNAME = "backups"
STATE_FILENAME = "state.json"
ROOT_DIRNAME = ".abstra/file-history"

_BACKUP_FILENAME_RE = re.compile(r"^[0-9a-f]{16}@v\d+$")


@dataclass(frozen=True)
class FileHistoryBackup:
    backup_filename: str | None
    version: int
    backup_time: str
    # backup_filename=None has two meanings disambiguated by pre_existed:
    #   pre_existed=False -> file did not exist (rewind unlinks creations)
    #   pre_existed=True  -> backup copy failed (rewind must NOT touch the file)
    pre_existed: bool = False

    def to_dict(self) -> dict:
        return {
            "backupFilename": self.backup_filename,
            "version": self.version,
            "backupTime": self.backup_time,
            "preExisted": self.pre_existed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> FileHistoryBackup:
        return cls(
            backup_filename=data.get("backupFilename"),
            version=int(data.get("version", 1)),
            backup_time=data.get("backupTime")
            or datetime.now(timezone.utc).isoformat(),
            pre_existed=bool(data.get("preExisted", False)),
        )


@dataclass(frozen=True)
class FileHistoryRewindFailure:
    path: str
    reason: str

    def to_dict(self) -> dict:
        return {"path": self.path, "reason": self.reason}


class FileHistoryRewindError(Exception):
    def __init__(
        self,
        message_id: str,
        files_restored: list[Path],
        failures: list[FileHistoryRewindFailure],
    ) -> None:
        super().__init__(f"File rewind partially failed for message_id={message_id}")
        self.message_id = message_id
        self.files_restored = files_restored
        self.failures = failures


@dataclass
class FileHistorySnapshot:
    message_id: str
    timestamp: str
    tracked_file_backups: dict[str, FileHistoryBackup] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "messageId": self.message_id,
            "timestamp": self.timestamp,
            "trackedFileBackups": {
                path: backup.to_dict()
                for path, backup in self.tracked_file_backups.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> FileHistorySnapshot:
        return cls(
            message_id=data["messageId"],
            timestamp=data["timestamp"],
            tracked_file_backups={
                path: FileHistoryBackup.from_dict(value)
                for path, value in data.get("trackedFileBackups", {}).items()
            },
        )


@dataclass
class FileHistoryState:
    snapshots: list[FileHistorySnapshot] = field(default_factory=list)
    tracked_files: set[str] = field(default_factory=set)
    snapshot_sequence: int = 0

    def to_dict(self) -> dict:
        return {
            "snapshots": [snap.to_dict() for snap in self.snapshots],
            "trackedFiles": sorted(self.tracked_files),
            "snapshotSequence": self.snapshot_sequence,
        }

    @classmethod
    def from_dict(cls, data: dict) -> FileHistoryState:
        return cls(
            snapshots=[
                FileHistorySnapshot.from_dict(s) for s in data.get("snapshots", [])
            ],
            tracked_files=set(data.get("trackedFiles", [])),
            snapshot_sequence=int(data.get("snapshotSequence", 0)),
        )


class FileHistoryService:
    _state: FileHistoryState | None = None
    _state_root: Path | None = None
    _lock = threading.RLock()

    @classmethod
    def _root(cls) -> Path:
        return Path(Settings.root_path)

    @classmethod
    def _dir(cls) -> Path:
        return cls._root() / ROOT_DIRNAME

    @classmethod
    def _backup_dir(cls) -> Path:
        return cls._dir() / BACKUP_DIRNAME

    @classmethod
    def _state_path(cls) -> Path:
        return cls._dir() / STATE_FILENAME

    @classmethod
    def _get_state(cls) -> FileHistoryState:
        with cls._lock:
            current = cls._root()
            state = cls._state
            if state is None or cls._state_root != current:
                state = cls._load_state()
                cls._state = state
                cls._state_root = current
            return state

    @classmethod
    def reset_for_tests(cls) -> None:
        with cls._lock:
            cls._state = None
            cls._state_root = None

    @classmethod
    def clear(cls) -> None:
        with cls._lock:
            try:
                if cls._dir().exists():
                    shutil.rmtree(cls._dir(), ignore_errors=True)
            except Exception as e:  # noqa: BLE001
                AbstraLogger.warning(f"file-history: failed to clear directory: {e}")
            cls._state = FileHistoryState()
            cls._state_root = cls._root()

    @classmethod
    def make_snapshot(cls, message_id: str) -> None:
        with cls._lock:
            cls._make_snapshot_locked(message_id)

    @classmethod
    def track_edit(cls, message_id: str, file_path: Path) -> None:
        try:
            tracking_path = cls._tracking_path(file_path)
        except ValueError:
            return

        with cls._lock:
            state = cls._get_state()
            current_idx = cls._snapshot_index(message_id)
            if current_idx is None:
                cls._make_snapshot_locked(message_id)
                current_idx = cls._snapshot_index(message_id)
                if current_idx is None:
                    return
            current = state.snapshots[current_idx]
            if tracking_path in current.tracked_file_backups:
                return
            next_version = cls._next_version_for(tracking_path)
            backup = cls._create_backup(file_path, next_version)
            current.tracked_file_backups[tracking_path] = backup
            state.tracked_files.add(tracking_path)
            cls._persist()

    @classmethod
    def rewind(cls, message_id: str) -> list[Path]:
        with cls._lock:
            state = cls._get_state()
            target_idx = cls._snapshot_index(message_id)
            if target_idx is None:
                raise FileNotFoundError(
                    f"No file-history snapshot for message_id={message_id}"
                )
            target = state.snapshots[target_idx]
            tracked_files = set(state.tracked_files)
            effective_backups = cls._resolve_effective_backups(target, tracked_files)

        files_changed: list[Path] = []
        failures: list[FileHistoryRewindFailure] = []
        for tracking_path in tracked_files:
            try:
                file_path = cls._safe_absolute_path(tracking_path)
                if file_path is None:
                    failures.append(
                        FileHistoryRewindFailure(tracking_path, "Unsafe tracking path")
                    )
                    AbstraLogger.warning(
                        f"file-history: refusing rewind for unsafe tracking path {tracking_path!r}"
                    )
                    continue

                effective_backup = effective_backups.get(tracking_path)
                backup_filename = (
                    effective_backup.backup_filename
                    if effective_backup is not None
                    else None
                )

                if backup_filename is None:
                    if effective_backup is not None and effective_backup.pre_existed:
                        failures.append(
                            FileHistoryRewindFailure(
                                tracking_path, "Backup write previously failed"
                            )
                        )
                        AbstraLogger.warning(
                            f"file-history: skipping rewind for {tracking_path}: "
                            "backup write previously failed; user file preserved"
                        )
                        continue
                    if not file_path.exists():
                        continue
                    file_path.unlink(missing_ok=True)
                    files_changed.append(file_path)
                    continue

                if not _is_safe_backup_filename(backup_filename):
                    failures.append(
                        FileHistoryRewindFailure(
                            tracking_path, "Unsafe backup filename"
                        )
                    )
                    AbstraLogger.warning(
                        f"file-history: refusing rewind for unsafe backup filename "
                        f"{backup_filename!r} on {tracking_path}"
                    )
                    continue

                backup_path = cls._backup_dir() / backup_filename
                if not backup_path.exists():
                    failures.append(
                        FileHistoryRewindFailure(tracking_path, "Backup file missing")
                    )
                    AbstraLogger.warning(
                        f"file-history: backup missing for {tracking_path} ({backup_filename})"
                    )
                    continue
                if file_path.exists() and cls._files_equal(file_path, backup_path):
                    continue

                file_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup_path, file_path)
                os.chmod(file_path, backup_path.stat().st_mode)
                files_changed.append(file_path)
            except Exception as e:  # noqa: BLE001
                failures.append(FileHistoryRewindFailure(tracking_path, str(e)))
                AbstraLogger.warning(
                    f"file-history: rewind failed for {tracking_path}: {e}"
                )
        if failures:
            raise FileHistoryRewindError(message_id, files_changed, failures)
        cls._discard_snapshots_after(message_id)
        return files_changed

    @classmethod
    def can_restore(cls, message_id: str) -> bool:
        with cls._lock:
            return cls._snapshot_index(message_id) is not None

    @classmethod
    def has_any_changes(cls, message_id: str) -> bool:
        with cls._lock:
            state = cls._get_state()
            target_idx = cls._snapshot_index(message_id)
            if target_idx is None:
                return False
            target = state.snapshots[target_idx]
            tracked_files = set(state.tracked_files)
            effective_backups = cls._resolve_effective_backups(target, tracked_files)

        for tracking_path in tracked_files:
            try:
                file_path = cls._safe_absolute_path(tracking_path)
                if file_path is None:
                    continue
                effective_backup = effective_backups.get(tracking_path)
                backup_filename = (
                    effective_backup.backup_filename
                    if effective_backup is not None
                    else None
                )
                if backup_filename is None:
                    if effective_backup is not None and effective_backup.pre_existed:
                        continue
                    if file_path.exists():
                        return True
                    continue
                if not _is_safe_backup_filename(backup_filename):
                    continue
                backup_path = cls._backup_dir() / backup_filename
                if not file_path.exists() and backup_path.exists():
                    return True
                if file_path.exists() and not cls._files_equal(file_path, backup_path):
                    return True
            except Exception as e:  # noqa: BLE001
                AbstraLogger.warning(
                    f"file-history: has_any_changes failed for {tracking_path}: {e}"
                )
        return False

    @classmethod
    def get_diff_stats(cls, message_id: str) -> dict | None:
        with cls._lock:
            state = cls._get_state()
            target_idx = cls._snapshot_index(message_id)
            if target_idx is None:
                return None
            target = state.snapshots[target_idx]
            tracked_files = set(state.tracked_files)
            effective_backups = cls._resolve_effective_backups(target, tracked_files)

        files_changed: list[str] = []
        insertions = 0
        deletions = 0

        for tracking_path in tracked_files:
            try:
                file_path = cls._safe_absolute_path(tracking_path)
                if file_path is None:
                    continue
                effective_backup = effective_backups.get(tracking_path)
                if (
                    effective_backup is not None
                    and effective_backup.backup_filename is None
                    and effective_backup.pre_existed
                ):
                    continue
                backup_filename = (
                    effective_backup.backup_filename
                    if effective_backup is not None
                    else None
                )
                if backup_filename is not None and not _is_safe_backup_filename(
                    backup_filename
                ):
                    backup_filename = None

                current_content = (
                    file_path.read_text(encoding="utf-8", errors="replace")
                    if file_path.exists()
                    else ""
                )
                backup_content = (
                    (cls._backup_dir() / backup_filename).read_text(
                        encoding="utf-8", errors="replace"
                    )
                    if backup_filename
                    and (cls._backup_dir() / backup_filename).exists()
                    else ""
                )

                if current_content == backup_content:
                    continue

                files_changed.append(tracking_path)
                ins, dels = _line_diff_counts(current_content, backup_content)
                insertions += ins
                deletions += dels
            except Exception as e:  # noqa: BLE001
                AbstraLogger.warning(
                    f"file-history: get_diff_stats failed for {tracking_path}: {e}"
                )

        return {
            "filesChanged": files_changed,
            "insertions": insertions,
            "deletions": deletions,
        }

    @classmethod
    def list_checkpoints(cls) -> list[dict]:
        with cls._lock:
            snapshots = list(cls._get_state().snapshots)

        out: list[dict] = []
        for snap in snapshots:
            stats = cls.get_diff_stats(snap.message_id) or {
                "filesChanged": [],
                "insertions": 0,
                "deletions": 0,
            }
            out.append(
                {
                    "messageId": snap.message_id,
                    "timestamp": snap.timestamp,
                    "diffStats": stats,
                }
            )
        return out

    @classmethod
    def _make_snapshot_locked(cls, message_id: str) -> None:
        if cls._snapshot_index(message_id) is not None:
            return
        state = cls._get_state()
        now = datetime.now(timezone.utc).isoformat()
        state.snapshots.append(
            FileHistorySnapshot(
                message_id=message_id,
                timestamp=now,
                tracked_file_backups=cls._current_tracked_backups_locked(),
            )
        )
        state.snapshot_sequence += 1
        cls._evict_if_needed()
        cls._persist()

    @classmethod
    def _current_tracked_backups_locked(cls) -> dict[str, FileHistoryBackup]:
        tracked_backups: dict[str, FileHistoryBackup] = {}
        for tracking_path in sorted(cls._get_state().tracked_files):
            tracked_backups[tracking_path] = cls._backup_for_current_state(
                tracking_path
            )
        return tracked_backups

    @classmethod
    def _backup_for_current_state(cls, tracking_path: str) -> FileHistoryBackup:
        file_path = cls._absolute_path(tracking_path)
        latest = cls._latest_backup_for(tracking_path)
        if latest is not None and cls._backup_matches_current_state(file_path, latest):
            return latest
        return cls._create_backup(file_path, cls._next_version_for(tracking_path))

    @classmethod
    def _snapshot_index(cls, message_id: str) -> int | None:
        state = cls._get_state()
        for i in range(len(state.snapshots) - 1, -1, -1):
            if state.snapshots[i].message_id == message_id:
                return i
        return None

    @classmethod
    def _next_version_for(cls, tracking_path: str) -> int:
        latest = 0
        for snap in cls._get_state().snapshots:
            backup = snap.tracked_file_backups.get(tracking_path)
            if backup is not None and backup.version > latest:
                latest = backup.version
        return latest + 1

    @classmethod
    def _first_version_backup(cls, tracking_path: str) -> FileHistoryBackup | None:
        """CALLER MUST HOLD ``cls._lock``."""
        for snap in cls._get_state().snapshots:
            backup = snap.tracked_file_backups.get(tracking_path)
            if backup is not None and backup.version == 1:
                return backup
        return None

    @classmethod
    def _resolve_effective_backups(
        cls,
        target: FileHistorySnapshot,
        tracked_files: set[str],
    ) -> dict[str, FileHistoryBackup | None]:
        """CALLER MUST HOLD ``cls._lock``."""
        return {
            path: target.tracked_file_backups.get(path)
            or cls._first_version_backup(path)
            for path in tracked_files
        }

    @classmethod
    def _latest_backup_for(cls, tracking_path: str) -> FileHistoryBackup | None:
        for snap in reversed(cls._get_state().snapshots):
            backup = snap.tracked_file_backups.get(tracking_path)
            if backup is not None:
                return backup
        return None

    @classmethod
    def _create_backup(cls, file_path: Path, version: int) -> FileHistoryBackup:
        now = datetime.now(timezone.utc).isoformat()
        if not file_path.exists():
            return FileHistoryBackup(
                backup_filename=None,
                version=version,
                backup_time=now,
                pre_existed=False,
            )

        try:
            tracking_path = cls._tracking_path(file_path)
        except ValueError:
            return FileHistoryBackup(
                backup_filename=None,
                version=version,
                backup_time=now,
                pre_existed=False,
            )

        backup_filename = _backup_filename(tracking_path, version)
        backup_path = cls._backup_dir() / backup_filename

        if backup_path.exists() and cls._files_equal(file_path, backup_path):
            return FileHistoryBackup(
                backup_filename=backup_filename,
                version=version,
                backup_time=now,
                pre_existed=True,
            )

        try:
            cls._backup_dir().mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, backup_path)
            os.chmod(backup_path, file_path.stat().st_mode)
        except Exception as e:  # noqa: BLE001
            AbstraLogger.warning(
                f"file-history: failed to write backup {backup_filename}: {e}"
            )
            # File existed but copy failed: pre_existed=True so rewind skips
            # instead of treating the None filename as ENOENT and unlinking.
            return FileHistoryBackup(
                backup_filename=None,
                version=version,
                backup_time=now,
                pre_existed=True,
            )

        return FileHistoryBackup(
            backup_filename=backup_filename,
            version=version,
            backup_time=now,
            pre_existed=True,
        )

    @classmethod
    def _evict_if_needed(cls) -> None:
        state = cls._get_state()
        if len(state.snapshots) <= MAX_SNAPSHOTS:
            return
        evicted = state.snapshots[:-MAX_SNAPSHOTS]
        state.snapshots = state.snapshots[-MAX_SNAPSHOTS:]
        cls._cleanup_orphans(evicted)

    @classmethod
    def _cleanup_orphans(cls, evicted: list[FileHistorySnapshot]) -> None:
        survivors: set[str] = set()
        for snap in cls._get_state().snapshots:
            for backup in snap.tracked_file_backups.values():
                if backup.backup_filename:
                    survivors.add(backup.backup_filename)
        for snap in evicted:
            for backup in snap.tracked_file_backups.values():
                name = backup.backup_filename
                if name and name not in survivors:
                    try:
                        (cls._backup_dir() / name).unlink(missing_ok=True)
                    except Exception as e:  # noqa: BLE001
                        AbstraLogger.warning(
                            f"file-history: failed to delete orphan backup {name}: {e}"
                        )

    @classmethod
    def _discard_snapshots_after(cls, message_id: str) -> None:
        with cls._lock:
            state = cls._get_state()
            target_idx = cls._snapshot_index(message_id)
            if target_idx is None:
                return
            evicted = state.snapshots[target_idx + 1 :]
            if not evicted:
                return
            state.snapshots = state.snapshots[: target_idx + 1]
            state.tracked_files = {
                path
                for snap in state.snapshots
                for path in snap.tracked_file_backups.keys()
            }
            cls._cleanup_orphans(evicted)
            cls._persist()

    @classmethod
    def _tracking_path(cls, file_path: Path) -> str:
        absolute = Path(file_path).resolve()
        try:
            return str(absolute.relative_to(cls._root().resolve()))
        except ValueError as exc:
            raise ValueError(
                f"file-history: path {absolute} is outside project root {cls._root()}"
            ) from exc

    @classmethod
    def _absolute_path(cls, tracking_path: str) -> Path:
        return cls._root() / tracking_path

    @classmethod
    def _safe_absolute_path(cls, tracking_path: str) -> Path | None:
        """Returns the CANONICAL resolved path (not the candidate) so downstream
        file ops operate on the same path that was validated against the root.
        """
        if not _is_safe_tracking_path(tracking_path):
            return None
        candidate = cls._root() / tracking_path
        try:
            resolved = candidate.resolve()
            root_resolved = cls._root().resolve()
        except OSError:
            return None
        try:
            resolved.relative_to(root_resolved)
        except ValueError:
            return None
        return resolved

    @classmethod
    def _files_equal(cls, a: Path, b: Path) -> bool:
        try:
            sa = a.stat()
            sb = b.stat()
        except FileNotFoundError:
            return False
        if sa.st_size != sb.st_size:
            return False
        return a.read_bytes() == b.read_bytes()

    @classmethod
    def _backup_matches_current_state(
        cls, file_path: Path, backup: FileHistoryBackup
    ) -> bool:
        if backup.backup_filename is None:
            return not file_path.exists()
        backup_path = cls._backup_dir() / backup.backup_filename
        return (
            file_path.exists()
            and backup_path.exists()
            and cls._files_equal(file_path, backup_path)
        )

    @classmethod
    def _load_state(cls) -> FileHistoryState:
        if not cls._state_path().exists():
            return FileHistoryState()
        try:
            data = json.loads(cls._state_path().read_text(encoding="utf-8"))
            state = FileHistoryState.from_dict(data)
        except (json.JSONDecodeError, OSError, KeyError) as e:
            AbstraLogger.warning(
                f"file-history: corrupted state.json, reinitializing: {e}"
            )
            return FileHistoryState()
        return cls._sanitize_loaded_state(state)

    @classmethod
    def _sanitize_loaded_state(cls, state: FileHistoryState) -> FileHistoryState:
        safe_tracked: set[str] = set()
        for path in state.tracked_files:
            if not _is_safe_tracking_path(path):
                AbstraLogger.warning(
                    f"file-history: dropping unsafe tracked path {path!r} from state"
                )
                continue
            safe_tracked.add(path)

        safe_snapshots: list[FileHistorySnapshot] = []
        for snap in state.snapshots:
            sanitized_backups: dict[str, FileHistoryBackup] = {}
            for path, backup in snap.tracked_file_backups.items():
                if not _is_safe_tracking_path(path):
                    AbstraLogger.warning(
                        f"file-history: dropping unsafe path {path!r} "
                        f"from snapshot {snap.message_id}"
                    )
                    continue
                if backup.backup_filename is not None and not _is_safe_backup_filename(
                    backup.backup_filename
                ):
                    AbstraLogger.warning(
                        f"file-history: dropping unsafe backup filename "
                        f"{backup.backup_filename!r} on {path}"
                    )
                    continue
                sanitized_backups[path] = backup
            safe_snapshots.append(
                FileHistorySnapshot(
                    message_id=snap.message_id,
                    timestamp=snap.timestamp,
                    tracked_file_backups=sanitized_backups,
                )
            )
        return FileHistoryState(
            snapshots=safe_snapshots,
            tracked_files=safe_tracked,
            snapshot_sequence=state.snapshot_sequence,
        )

    @classmethod
    def _persist(cls) -> None:
        try:
            cls._dir().mkdir(parents=True, exist_ok=True)
            tmp = cls._state_path().with_suffix(".tmp")
            tmp.write_text(
                json.dumps(cls._get_state().to_dict(), indent=2), encoding="utf-8"
            )
            os.replace(str(tmp), str(cls._state_path()))
        except Exception as e:  # noqa: BLE001
            AbstraLogger.warning(f"file-history: failed to persist state: {e}")


def _backup_filename(tracking_path: str, version: int) -> str:
    digest = hashlib.sha256(tracking_path.encode("utf-8")).hexdigest()[:16]
    return f"{digest}@v{version}"


def _is_safe_tracking_path(tracking_path: str) -> bool:
    if not isinstance(tracking_path, str) or not tracking_path:
        return False
    p = Path(tracking_path)
    if p.is_absolute():
        return False
    if any(part == ".." for part in p.parts):
        return False
    return True


def _is_safe_backup_filename(name: str | None) -> bool:
    return bool(name) and bool(_BACKUP_FILENAME_RE.fullmatch(name))


def _line_diff_counts(current: str, target: str) -> tuple[int, int]:
    if current == target:
        return 0, 0
    cur_lines = current.splitlines()
    tgt_lines = target.splitlines()
    insertions = 0
    deletions = 0
    matcher = difflib.SequenceMatcher(a=cur_lines, b=tgt_lines, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "insert":
            insertions += j2 - j1
        elif tag == "delete":
            deletions += i2 - i1
        elif tag == "replace":
            deletions += i2 - i1
            insertions += j2 - j1
    return insertions, deletions


def safe_track_edit(file_path: Path) -> None:
    from abstra_internals.services.mcp_context import current_message_id

    message_id = current_message_id()
    if not message_id:
        return
    try:
        FileHistoryService.track_edit(message_id, file_path)
    except Exception as e:  # noqa: BLE001
        AbstraLogger.warning(f"file-history: track_edit failed for {file_path}: {e}")


def safe_make_snapshot() -> None:
    from abstra_internals.services.mcp_context import current_message_id

    message_id = current_message_id()
    if not message_id:
        return
    try:
        FileHistoryService.make_snapshot(message_id)
    except Exception as e:  # noqa: BLE001
        AbstraLogger.warning(f"file-history: make_snapshot failed: {e}")
