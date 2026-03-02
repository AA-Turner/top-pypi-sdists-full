"""Git worktree management for isolated agent changes.

This module provides worktree management for running agents in isolated
git worktrees, allowing changes to be reviewed before merging to the
main branch.

Usage:
    # Enable worktree mode via environment variable
    export EMDASH_USE_WORKTREE=true

    # Or via API options
    options.use_worktree = True

Flow:
    1. User sends message to agent
    2. If use_worktree=True, create worktree: .emdash-worktrees/{session-id}/
    3. Agent makes changes in the worktree
    4. When done, user can apply or discard changes via API
"""

import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from git import Repo

from ..utils.logger import log


@dataclass
class WorktreeInfo:
    """Information about a created worktree."""
    path: Path
    branch: str
    base_branch: str
    task_slug: str
    created_at: str
    status: str  # pending, active, completed, failed


class WorktreeError(Exception):
    """Error during worktree operations."""
    pass


class WorktreeManager:
    """Manages Git worktrees for parallel agent execution.

    Creates isolated worktrees under .emdash-worktrees/{task-slug}/
    with unique branches for each parallel task.

    Example:
        manager = WorktreeManager(repo_root=Path("."))

        # Create worktree for a task
        info = manager.create_worktree("add-user-auth", base_branch="main")
        # -> .emdash-worktrees/add-user-auth/
        # -> branch: emdash/task-add-user-auth

        # Clean up when done
        manager.remove_worktree("add-user-auth")
    """

    WORKTREE_DIR = ".emdash-worktrees"
    BRANCH_PREFIX = "emdash/task-"

    def __init__(self, repo_root: Path):
        """Initialize worktree manager.

        Args:
            repo_root: Root of the main git repository
        """
        self.repo_root = repo_root.resolve()
        self.repo = Repo(self.repo_root)
        self.worktrees_base = self.repo_root / self.WORKTREE_DIR

    def slugify(self, text: str) -> str:
        """Convert text to URL-safe slug."""
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[-\s]+", "-", text)
        return text[:50]

    def _get_default_branch(self) -> str:
        """Get the default branch name for this repo.

        Tries HEAD, then common names (main, master), then first available branch.
        """
        # Try current HEAD branch
        try:
            if not self.repo.head.is_detached:
                return self.repo.active_branch.name
        except Exception:
            pass

        # Try common branch names
        branch_names = [h.name for h in self.repo.heads]
        for name in ["main", "master", "develop"]:
            if name in branch_names:
                return name

        # Use first available branch
        if branch_names:
            return branch_names[0]

        # Fallback to HEAD
        return "HEAD"

    def create_worktree(
        self,
        task_name: str,
        base_branch: str | None = None,
        force: bool = False,
    ) -> WorktreeInfo:
        """Create a new worktree for a task.

        Args:
            task_name: Human-readable task name or slug
            base_branch: Branch to base the worktree on (auto-detected if None)
            force: If True, remove existing worktree first

        Returns:
            WorktreeInfo with worktree details

        Raises:
            WorktreeError: If worktree creation fails
        """
        slug = self.slugify(task_name)
        worktree_path = self.worktrees_base / slug
        branch_name = f"{self.BRANCH_PREFIX}{slug}"

        # Auto-detect base branch if not provided
        if base_branch is None:
            base_branch = self._get_default_branch()
        log.debug(f"Using base branch: {base_branch}")

        # Handle existing worktree
        if worktree_path.exists():
            if force:
                self.remove_worktree(slug)
            else:
                raise WorktreeError(f"Worktree already exists: {worktree_path}")

        # Ensure base directory exists
        self.worktrees_base.mkdir(parents=True, exist_ok=True)

        # Fetch latest if remote exists
        try:
            if self.repo.remotes:
                self.repo.remotes.origin.fetch()
        except Exception:
            pass  # No remote or fetch failed, continue with local

        # Delete branch if it exists (from previous run)
        if branch_name in [h.name for h in self.repo.heads]:
            self.repo.delete_head(branch_name, force=True)

        # Create worktree with new branch using git command
        cmd = [
            "git", "worktree", "add",
            "-b", branch_name,
            str(worktree_path),
            base_branch,
        ]
        result = subprocess.run(
            cmd,
            cwd=str(self.repo_root),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise WorktreeError(f"Failed to create worktree: {result.stderr}")

        log.info(f"Created worktree at {worktree_path} on branch {branch_name}")

        return WorktreeInfo(
            path=worktree_path,
            branch=branch_name,
            base_branch=base_branch,
            task_slug=slug,
            created_at=datetime.now().isoformat(),
            status="pending",
        )

    def remove_worktree(self, slug_or_path: str | Path) -> bool:
        """Remove a worktree and optionally its branch.

        Args:
            slug_or_path: Task slug or full worktree path

        Returns:
            True if removed successfully
        """
        if isinstance(slug_or_path, Path):
            worktree_path = slug_or_path
            slug = worktree_path.name
        else:
            slug = slug_or_path
            worktree_path = self.worktrees_base / slug

        branch_name = f"{self.BRANCH_PREFIX}{slug}"

        # Remove worktree
        if worktree_path.exists():
            cmd = ["git", "worktree", "remove", str(worktree_path), "--force"]
            subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True)

            # If git worktree remove fails, force delete
            if worktree_path.exists():
                shutil.rmtree(worktree_path)

        # Prune worktree metadata
        subprocess.run(
            ["git", "worktree", "prune"],
            cwd=str(self.repo_root),
            capture_output=True,
        )

        # Delete the branch
        try:
            if branch_name in [h.name for h in self.repo.heads]:
                self.repo.delete_head(branch_name, force=True)
        except Exception:
            pass  # Branch may not exist

        log.info(f"Removed worktree {slug}")
        return True

    def list_worktrees(self) -> list[WorktreeInfo]:
        """List all active emdash worktrees."""
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            cwd=str(self.repo_root),
            capture_output=True,
            text=True,
        )

        worktrees = []
        current: dict = {}

        for line in result.stdout.strip().split("\n"):
            if line.startswith("worktree "):
                current["path"] = Path(line[9:])
            elif line.startswith("branch refs/heads/"):
                current["branch"] = line[18:]
            elif line == "":
                path = current.get("path")
                if path and str(self.worktrees_base) in str(path):
                    worktrees.append(WorktreeInfo(
                        path=path,
                        branch=current.get("branch", ""),
                        base_branch="main",
                        task_slug=path.name,
                        created_at="",
                        status="active",
                    ))
                current = {}

        return worktrees

    def cleanup_all(self) -> int:
        """Remove all emdash worktrees.

        Returns:
            Number of worktrees removed
        """
        worktrees = self.list_worktrees()
        for wt in worktrees:
            self.remove_worktree(wt.task_slug)

        # Also clean up the base directory
        if self.worktrees_base.exists():
            shutil.rmtree(self.worktrees_base)

        return len(worktrees)

    def get_worktree(self, slug: str) -> Optional[WorktreeInfo]:
        """Get info for a specific worktree by slug."""
        worktree_path = self.worktrees_base / slug
        if not worktree_path.exists():
            return None

        branch_name = f"{self.BRANCH_PREFIX}{slug}"
        return WorktreeInfo(
            path=worktree_path,
            branch=branch_name,
            base_branch="main",
            task_slug=slug,
            created_at="",
            status="active",
        )
