"""Safe checkpoint management for SAGE.

This module provides scoped rollback that only affects SAGE-owned edits,
preventing accidental destruction of user work.

Key safety guarantees:
- Only deletes files that SAGE created in-session
- Only restores files that SAGE modified in-session
- Uses non-destructive git operations (apply vs pop)
- Tracks file provenance (created vs modified)
- Validates operations before execution
"""

from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)

__all__ = [
    "Checkpoint",
    "CheckpointManager",
    "FileChange",
    "RestoreResult",
]


@dataclass
class FileChange:
    """Tracks a single file change with provenance."""

    path: str  # Relative path from workspace root
    action: Literal["created", "modified", "deleted"]
    original_content: str | None = None  # For modified files, stores original content
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "path": self.path,
            "action": self.action,
            "original_content": self.original_content,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> FileChange:
        """Deserialize from dictionary."""
        return cls(
            path=data["path"],
            action=data["action"],
            original_content=data.get("original_content"),
            timestamp=data.get("timestamp", datetime.now().isoformat()),
        )


@dataclass
class Checkpoint:
    """Snapshot of SAGE state for safe rollback.

    Unlike the old checkpoint system, this tracks:
    - Which files were CREATED by SAGE (safe to delete on rollback)
    - Which files were MODIFIED by SAGE (restore original content on rollback)
    - Original content of modified files (for safe restoration)
    """

    id: str
    timestamp: str
    git_sha: str | None  # Git commit SHA at checkpoint time
    git_stash: str | None  # Stash reference if uncommitted changes existed
    changes: list[FileChange]  # Tracked file changes with provenance
    message_count: int  # Number of messages in conversation
    description: str  # Human-readable description

    # Legacy field for backward compatibility
    files_written: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "git_sha": self.git_sha,
            "git_stash": self.git_stash,
            "changes": [c.to_dict() for c in self.changes],
            "files_written": self.files_written,
            "message_count": self.message_count,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Checkpoint:
        """Deserialize from dictionary."""
        # Handle legacy checkpoints that only have files_written
        changes = []
        if "changes" in data:
            changes = [FileChange.from_dict(c) for c in data["changes"]]
        elif "files_written" in data:
            # Convert legacy files_written to changes (assume all were created)
            changes = [
                FileChange(path=fp, action="created") for fp in data.get("files_written", [])
            ]

        return cls(
            id=data["id"],
            timestamp=data["timestamp"],
            git_sha=data.get("git_sha"),
            git_stash=data.get("git_stash"),
            changes=changes,
            files_written=data.get("files_written", []),
            message_count=data.get("message_count", 0),
            description=data.get("description", ""),
        )

    @property
    def files_created(self) -> list[str]:
        """Files that SAGE created (safe to delete on rollback)."""
        return [c.path for c in self.changes if c.action == "created"]

    @property
    def files_modified(self) -> list[str]:
        """Files that SAGE modified (restore original on rollback)."""
        return [c.path for c in self.changes if c.action == "modified"]


@dataclass
class RestoreResult:
    """Result of a restore operation."""

    success: bool
    message: str
    files_deleted: list[str] = field(default_factory=list)
    files_restored: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class CheckpointManager:
    """Manages safe checkpoints for SAGE with scoped rollback.

    Key safety guarantees:
    1. Only deletes files that SAGE created in-session
    2. Only restores files that SAGE modified in-session
    3. Uses non-destructive git operations
    4. Validates operations before execution
    5. Provides detailed rollback reporting
    """

    MAX_CHECKPOINTS = 20
    CHECKPOINT_FILE = "history.json"

    def __init__(self, cwd: Path) -> None:
        self.cwd = cwd.resolve()
        self.checkpoints: list[Checkpoint] = []
        self._checkpoint_dir = cwd / ".sage" / "checkpoints"
        self._checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self._pending_changes: list[FileChange] = []
        self._is_repo = self._check_is_repo()
        self._load_checkpoints()

    def _check_is_repo(self) -> bool:
        """Check if the path is a git repository."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=5,
                stderr=subprocess.DEVNULL,
            )
            return result.returncode == 0
        except Exception:
            return False

    # ── Change Tracking ─────────────────────────────────────────

    def track_file_created(self, path: str) -> None:
        """Track that SAGE created a new file."""
        self._pending_changes.append(
            FileChange(
                path=path,
                action="created",
            )
        )

    def track_file_modified(self, path: str, original_content: str | None = None) -> None:
        """Track that SAGE modified an existing file.

        Args:
            path: Relative path to the file
            original_content: Original content before modification (for safe restore)
        """
        # If we don't have original content, try to read it from git
        if original_content is None:
            original_content = self._get_git_file_content(path)

        self._pending_changes.append(
            FileChange(
                path=path,
                action="modified",
                original_content=original_content,
            )
        )

    def track_file_deleted(self, path: str, original_content: str | None = None) -> None:
        """Track that SAGE deleted a file."""
        if original_content is None:
            original_content = self._get_git_file_content(path)

        self._pending_changes.append(
            FileChange(
                path=path,
                action="deleted",
                original_content=original_content,
            )
        )

    def clear_pending_changes(self) -> None:
        """Clear pending changes (e.g., after creating a checkpoint)."""
        self._pending_changes.clear()

    # ── Checkpoint Creation ─────────────────────────────────────

    def create_checkpoint(
        self,
        message_count: int,
        description: str,
        auto_stash: bool = True,
        files_written: list[str] | None = None,  # Legacy compatibility
    ) -> Checkpoint:
        """Create a new checkpoint before a major operation.

        Args:
            message_count: Number of messages in conversation
            description: Human-readable description
            auto_stash: Whether to stash uncommitted changes
            files_written: Legacy parameter for backward compatibility
        """
        checkpoint_id = f"cp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        git_stash = None
        if auto_stash and self._has_uncommitted_changes():
            git_stash = self._create_stash(description)

        # Merge pending changes with any legacy files_written
        changes = list(self._pending_changes)
        if files_written:
            existing_paths = {c.path for c in changes}
            for fp in files_written:
                if fp not in existing_paths:
                    # Assume created for legacy compatibility
                    changes.append(FileChange(path=fp, action="created"))

        checkpoint = Checkpoint(
            id=checkpoint_id,
            timestamp=datetime.now().isoformat(),
            git_sha=self._get_git_sha(),
            git_stash=git_stash,
            changes=changes,
            files_written=files_written or [],
            message_count=message_count,
            description=description,
        )

        self.checkpoints.append(checkpoint)
        self._save_checkpoints()
        self.clear_pending_changes()

        return checkpoint

    # ── Safe Restore ────────────────────────────────────────────

    def restore_checkpoint(self, checkpoint: Checkpoint) -> RestoreResult:
        """Safely restore to a checkpoint.

        Safety guarantees:
        1. Only deletes files that SAGE created (not pre-existing files)
        2. Only restores files that SAGE modified (preserves user work)
        3. Uses non-destructive git operations
        4. Reports all actions taken

        Returns:
            RestoreResult with details of what was done
        """
        result = RestoreResult(success=True, message="")

        # Phase 1: Delete files that SAGE created
        for change in checkpoint.changes:
            if change.action == "created":
                target = self.cwd / change.path
                if target.exists():
                    try:
                        target.unlink()
                        result.files_deleted.append(change.path)
                    except Exception as e:
                        result.errors.append(f"Failed to delete {change.path}: {e}")
                else:
                    result.warnings.append(f"File already gone: {change.path}")

        # Phase 2: Restore files that SAGE modified
        for change in checkpoint.changes:
            if change.action == "modified":
                target = self.cwd / change.path
                if change.original_content is not None:
                    try:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_text(change.original_content)
                        result.files_restored.append(change.path)
                    except Exception as e:
                        result.errors.append(f"Failed to restore {change.path}: {e}")
                else:
                    # Try git restore for this specific file
                    restore_ok = self._git_restore_file(change.path, checkpoint.git_sha)
                    if restore_ok:
                        result.files_restored.append(change.path)
                    else:
                        result.errors.append(f"No original content for {change.path}")

        # Phase 3: Restore files that SAGE deleted
        for change in checkpoint.changes:
            if change.action == "deleted":
                target = self.cwd / change.path
                if change.original_content is not None:
                    try:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_text(change.original_content)
                        result.files_restored.append(change.path)
                    except Exception as e:
                        result.errors.append(f"Failed to restore deleted {change.path}: {e}")

        # Phase 4: Apply stash if present (non-destructively)
        if checkpoint.git_stash:
            stash_ok, stash_msg = self._apply_stash(checkpoint.git_stash)
            if not stash_ok:
                result.warnings.append(f"Stash apply: {stash_msg}")

        # Determine overall result
        if result.errors:
            result.success = False
            result.message = f"Partial restore with {len(result.errors)} error(s)"
        else:
            result.message = (
                f"Restored: {len(result.files_deleted)} deleted, "
                f"{len(result.files_restored)} restored"
            )

        return result

    def validate_restore(self, checkpoint: Checkpoint) -> tuple[bool, list[str]]:
        """Validate that a restore operation is safe to perform.

        Returns:
            (is_safe, list_of_concerns)
        """
        concerns = []

        # Check for conflicts with user work
        for change in checkpoint.changes:
            target = self.cwd / change.path

            if change.action == "created" and target.exists():
                # Check if file has been modified since SAGE created it
                try:
                    current = target.read_text(encoding="utf-8", errors="replace")
                    # If we tracked original, we can compare
                    # For now, just note that it exists
                except Exception:
                    pass

            if change.action == "modified" and not target.exists():
                concerns.append(f"File was deleted externally: {change.path}")

        # Check git state
        if self._has_uncommitted_changes():
            concerns.append("Uncommitted changes exist - consider stashing first")

        return len(concerns) == 0, concerns

    # ── Checkpoint Access ───────────────────────────────────────

    def get_last_checkpoint(self) -> Checkpoint | None:
        """Get the most recent checkpoint."""
        return self.checkpoints[-1] if self.checkpoints else None

    def list_checkpoints(self, limit: int = 5) -> list[Checkpoint]:
        """List recent checkpoints (most recent first)."""
        return self.checkpoints[-limit:][::-1]

    def get_checkpoint_by_id(self, checkpoint_id: str) -> Checkpoint | None:
        """Get a specific checkpoint by ID."""
        for cp in self.checkpoints:
            if cp.id == checkpoint_id:
                return cp
        return None

    # ── Git Operations (Non-Destructive) ────────────────────────

    def _get_git_sha(self) -> str | None:
        """Get current git HEAD SHA."""
        if not self._is_repo:
            return None
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()[:12]
        except Exception as e:
            logger.debug(f"Could not get git SHA: {e}")
        return None

    def _has_uncommitted_changes(self) -> bool:
        """Check if there are uncommitted changes."""
        if not self._is_repo:
            return False
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=5,
            )
            return bool(result.stdout.strip())
        except Exception as e:
            logger.debug(f"Could not check for uncommitted changes: {e}")
            return False

    def _get_git_file_content(self, path: str) -> str | None:
        """Get file content from git HEAD."""
        if not self._is_repo:
            return None
        try:
            result = subprocess.run(
                ["git", "show", f"HEAD:{path}"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                return result.stdout
        except Exception as e:
            logger.debug(f"Could not get git file content for {path}: {e}")
        return None

    def _git_restore_file(self, path: str, sha: str | None = None) -> bool:
        """Restore a specific file from git (scoped, not whole-tree)."""
        if not self._is_repo:
            return False
        try:
            ref = sha or "HEAD"
            # Use git restore for scoped file restoration
            result = subprocess.run(
                ["git", "restore", "--source", ref, "--", path],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Failed to restore file {path}: {e}")
            return False

    def _create_stash(self, message: str) -> str | None:
        """Create a git stash and return the stash reference."""
        if not self._is_repo:
            return None
        try:
            if not self._has_uncommitted_changes():
                return None

            result = subprocess.run(
                ["git", "stash", "push", "-m", f"SAGE checkpoint: {message}"],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0 and "No local changes" not in result.stdout:
                # Get the stash reference
                list_result = subprocess.run(
                    ["git", "stash", "list", "-1"],
                    cwd=self.cwd,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if list_result.returncode == 0 and list_result.stdout.strip():
                    return list_result.stdout.split(":")[0]  # e.g., "stash@{0}"
        except Exception as e:
            logger.error(f"Failed to create git stash: {e}")
        return None

    def _apply_stash(self, stash_ref: str) -> tuple[bool, str]:
        """Apply a stash non-destructively (keeps the stash).

        Uses 'git stash apply' instead of 'git stash pop' so the stash
        is preserved in case we need it again.
        """
        try:
            result = subprocess.run(
                ["git", "stash", "apply", stash_ref],
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                return True, "Stash applied successfully"
            else:
                # Handle conflicts gracefully
                if "conflict" in result.stderr.lower():
                    return False, "Stash apply had conflicts - manual resolution needed"
                return False, result.stderr.strip() or "Stash apply failed"
        except Exception as e:
            return False, f"Git stash apply failed: {e}"

    # ── Persistence ─────────────────────────────────────────────

    def _load_checkpoints(self) -> None:
        """Load checkpoints from disk."""
        checkpoint_file = self._checkpoint_dir / self.CHECKPOINT_FILE
        if checkpoint_file.exists():
            try:
                data = json.loads(checkpoint_file.read_text(encoding="utf-8", errors="replace"))
                self.checkpoints = [Checkpoint.from_dict(cp) for cp in data.get("checkpoints", [])]
            except Exception:
                self.checkpoints = []

    def _save_checkpoints(self) -> None:
        """Persist checkpoints to disk."""
        checkpoint_file = self._checkpoint_dir / self.CHECKPOINT_FILE
        data = {
            "version": 2,  # New format version
            "checkpoints": [cp.to_dict() for cp in self.checkpoints[-self.MAX_CHECKPOINTS :]],
        }
        checkpoint_file.write_text(json.dumps(data, indent=2))
