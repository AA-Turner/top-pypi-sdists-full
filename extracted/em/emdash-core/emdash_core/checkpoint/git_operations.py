"""Git operations for checkpoint system."""

import json
from pathlib import Path
from typing import Optional

from git import Repo
from git.exc import GitCommandError

from ..utils.logger import log
from .models import CheckpointMetadata


class GitCheckpointOperations:
    """Handles git operations for checkpoints.

    Creates specially-formatted commits that can be identified
    and parsed as checkpoints.
    """

    CHECKPOINT_PREFIX = "[emdash-checkpoint]"
    METADATA_START = "---EMDASH_METADATA---"
    METADATA_END = "---END_METADATA---"

    def __init__(self, repo_root: Path):
        """Initialize git operations.

        Args:
            repo_root: Root of the git repository
        """
        self.repo_root = repo_root.resolve()
        self.repo = Repo(self.repo_root)

    def has_changes(self) -> bool:
        """Check if there are uncommitted changes.

        Returns:
            True if there are staged, unstaged, or untracked changes
        """
        return self.repo.is_dirty(untracked_files=True)

    def get_modified_files(self) -> list[str]:
        """Get list of modified/added/deleted files.

        Returns:
            List of file paths relative to repo root
        """
        files = set()

        # Staged changes
        for item in self.repo.index.diff("HEAD"):
            files.add(item.a_path)
            if item.b_path:
                files.add(item.b_path)

        # Unstaged changes
        for item in self.repo.index.diff(None):
            files.add(item.a_path)
            if item.b_path:
                files.add(item.b_path)

        # Untracked files
        files.update(self.repo.untracked_files)

        return sorted(files)

    def create_checkpoint_commit(
        self,
        metadata: CheckpointMetadata,
        summary: str,
    ) -> str:
        """Create a checkpoint commit.

        Stages all changes and creates a commit with structured
        metadata in the commit message.

        Args:
            metadata: Checkpoint metadata to include
            summary: Human-readable summary of changes

        Returns:
            Commit SHA

        Raises:
            GitCommandError: If commit fails
        """
        # Stage all changes
        self.repo.git.add("-A")

        # Build commit message
        message = self._build_commit_message(metadata, summary)

        # Create commit
        commit = self.repo.index.commit(message)
        log.info(f"Created checkpoint commit {commit.hexsha[:8]}")

        return commit.hexsha

    def _build_commit_message(
        self,
        metadata: CheckpointMetadata,
        summary: str,
    ) -> str:
        """Build the structured commit message.

        Format:
            [emdash-checkpoint] Auto-checkpoint #{iteration}

            Summary: {summary}

            ---EMDASH_METADATA---
            {json metadata}
            ---END_METADATA---
        """
        # Build metadata dict (excluding commit_sha which isn't set yet)
        meta_dict = {
            "checkpoint_version": "1.0",
            "id": metadata.id,
            "session_id": metadata.session_id,
            "iteration": metadata.iteration,
            "timestamp": metadata.timestamp,
            "tools_used": metadata.tools_used,
            "files_modified": metadata.files_modified,
            "token_usage": metadata.token_usage,
        }

        lines = [
            f"{self.CHECKPOINT_PREFIX} Auto-checkpoint #{metadata.iteration}",
            "",
            f"Summary: {summary}",
            "",
            self.METADATA_START,
            json.dumps(meta_dict, indent=2),
            self.METADATA_END,
        ]

        return "\n".join(lines)

    def parse_checkpoint_commit(self, commit) -> Optional[CheckpointMetadata]:
        """Parse checkpoint metadata from a commit.

        Args:
            commit: Git commit object

        Returns:
            CheckpointMetadata if commit is a checkpoint, None otherwise
        """
        if not commit.message.startswith(self.CHECKPOINT_PREFIX):
            return None

        try:
            # Extract JSON between markers
            message = commit.message
            start_idx = message.find(self.METADATA_START)
            end_idx = message.find(self.METADATA_END)

            if start_idx == -1 or end_idx == -1:
                return None

            json_str = message[start_idx + len(self.METADATA_START):end_idx].strip()
            data = json.loads(json_str)

            return CheckpointMetadata(
                id=data.get("id", ""),
                session_id=data.get("session_id", ""),
                iteration=data.get("iteration", 0),
                timestamp=data.get("timestamp", ""),
                commit_sha=commit.hexsha,
                summary=self._extract_summary(message),
                tools_used=data.get("tools_used", []),
                files_modified=data.get("files_modified", []),
                token_usage=data.get("token_usage", {}),
            )
        except (json.JSONDecodeError, KeyError) as e:
            log.warning(f"Failed to parse checkpoint commit {commit.hexsha[:8]}: {e}")
            return None

    def _extract_summary(self, message: str) -> str:
        """Extract summary line from commit message."""
        for line in message.split("\n"):
            if line.startswith("Summary:"):
                return line[8:].strip()
        return ""

    def list_checkpoint_commits(self, limit: int = 50) -> list[CheckpointMetadata]:
        """List all checkpoint commits.

        Args:
            limit: Maximum number of commits to search

        Returns:
            List of CheckpointMetadata, most recent first
        """
        checkpoints = []

        try:
            for commit in self.repo.iter_commits(max_count=limit * 2):
                metadata = self.parse_checkpoint_commit(commit)
                if metadata:
                    checkpoints.append(metadata)
                    if len(checkpoints) >= limit:
                        break
        except GitCommandError as e:
            log.warning(f"Failed to list checkpoint commits: {e}")

        return checkpoints

    def restore_to_commit(self, commit_sha: str, create_branch: bool = True) -> str:
        """Restore working directory to a specific commit.

        Args:
            commit_sha: SHA of commit to restore to
            create_branch: If True, create a branch at the restored state

        Returns:
            Branch name if created, or commit SHA if detached

        Raises:
            GitCommandError: If restore fails
        """
        # Check for uncommitted changes
        if self.has_changes():
            raise GitCommandError(
                "restore",
                "Cannot restore: uncommitted changes exist. "
                "Please commit or stash your changes first.",
            )

        if create_branch:
            # Create a new branch at the checkpoint
            branch_name = f"emdash/restore-{commit_sha[:8]}"
            self.repo.git.checkout("-b", branch_name, commit_sha)
            log.info(f"Restored to {commit_sha[:8]} on branch {branch_name}")
            return branch_name
        else:
            # Detached HEAD
            self.repo.git.checkout(commit_sha)
            log.info(f"Restored to {commit_sha[:8]} (detached HEAD)")
            return commit_sha

    def get_commit(self, commit_sha: str):
        """Get a commit object by SHA.

        Args:
            commit_sha: Full or partial commit SHA

        Returns:
            Git commit object
        """
        return self.repo.commit(commit_sha)
