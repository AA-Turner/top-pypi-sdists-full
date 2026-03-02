"""Change detection for incremental indexing using git diff."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import git

from ..utils.logger import log


@dataclass
class ChangedFiles:
    """Files changed since last indexing."""

    added: list[Path] = field(default_factory=list)
    modified: list[Path] = field(default_factory=list)
    deleted: list[Path] = field(default_factory=list)

    @property
    def all_to_index(self) -> list[Path]:
        """Get all files that need to be (re)indexed."""
        return self.added + self.modified

    @property
    def total_changes(self) -> int:
        """Total number of changed files."""
        return len(self.added) + len(self.modified) + len(self.deleted)

    def __bool__(self) -> bool:
        """True if there are any changes."""
        return self.total_changes > 0


class ChangeDetector:
    """Detects files changed since last indexing using git diff."""

    def __init__(self, repo: git.Repo, last_indexed_commit: Optional[str] = None):
        """Initialize change detector.

        Args:
            repo: Git repository
            last_indexed_commit: SHA of commit at last index, or None for full index
        """
        self.repo = repo
        self.last_indexed_commit = last_indexed_commit
        self.repo_root = Path(repo.working_dir)

    def get_current_commit(self) -> str:
        """Get current HEAD commit SHA."""
        return self.repo.head.commit.hexsha

    def get_changed_files(self, extensions: list[str] = None) -> ChangedFiles:
        """Find files changed since last index.

        Uses git diff to detect:
        - Added files (A)
        - Modified files (M)
        - Deleted files (D)
        - Renamed files (R) - treated as delete + add

        Args:
            extensions: Optional list of extensions to filter (e.g., ['.py', '.ts'])

        Returns:
            ChangedFiles with categorized changes
        """
        if not self.last_indexed_commit:
            log.info("No previous index commit - full index required")
            return ChangedFiles()

        try:
            # Verify the commit exists
            try:
                old_commit = self.repo.commit(self.last_indexed_commit)
            except git.BadName:
                log.warning(f"Previous commit {self.last_indexed_commit[:8]} not found - full index required")
                return ChangedFiles()

            current_commit = self.repo.head.commit

            # Get diff between last indexed commit and current HEAD
            diff = old_commit.diff(current_commit)

            added = []
            modified = []
            deleted = []

            for change in diff:
                # Handle different change types
                if change.change_type == 'A':  # Added
                    file_path = self.repo_root / change.b_path
                    if self._should_include(file_path, extensions):
                        added.append(file_path)

                elif change.change_type == 'M':  # Modified
                    file_path = self.repo_root / change.b_path
                    if self._should_include(file_path, extensions):
                        modified.append(file_path)

                elif change.change_type == 'D':  # Deleted
                    file_path = self.repo_root / change.a_path
                    if self._should_include(file_path, extensions):
                        deleted.append(file_path)

                elif change.change_type == 'R':  # Renamed
                    # Treat as delete old + add new
                    old_path = self.repo_root / change.a_path
                    new_path = self.repo_root / change.b_path
                    if self._should_include(old_path, extensions):
                        deleted.append(old_path)
                    if self._should_include(new_path, extensions):
                        added.append(new_path)

                elif change.change_type in ('C', 'T'):  # Copied or Type changed
                    file_path = self.repo_root / change.b_path
                    if self._should_include(file_path, extensions):
                        modified.append(file_path)

            result = ChangedFiles(added=added, modified=modified, deleted=deleted)

            log.info(f"Detected changes: {len(added)} added, {len(modified)} modified, {len(deleted)} deleted")

            return result

        except Exception as e:
            log.error(f"Error detecting changes: {e}")
            return ChangedFiles()

    def _should_include(self, file_path: Path, extensions: Optional[list[str]]) -> bool:
        """Check if file should be included based on extension filter.

        Args:
            file_path: Path to file
            extensions: Optional list of extensions to include

        Returns:
            True if file should be included
        """
        if extensions is None:
            return True
        return file_path.suffix.lower() in [ext.lower() for ext in extensions]

    def has_uncommitted_changes(self) -> bool:
        """Check if there are uncommitted changes in the working directory.

        Returns:
            True if there are uncommitted changes
        """
        return self.repo.is_dirty(untracked_files=True)
