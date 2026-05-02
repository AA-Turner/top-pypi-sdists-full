"""Git operations module for SAGE DevOps.

This module provides git-related operations including:
- Branch management
- Commit operations
- Status checking
- Diff generation

NOTE: This is a stub implementation. Full functionality coming soon.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from sage.devops.models import GitCommit, GitResult, GitStatus


class GitOps:
    """Git operations handler.

    Provides safe git operations for SAGE workflows.
    """

    def __init__(self, repo_path: Path | str | None = None):
        """Initialize GitOps.

        Args:
            repo_path: Path to the git repository. If None, uses current directory.
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.is_repo = self._check_is_repo()

    def _check_is_repo(self) -> bool:
        """Check if the path is a git repository."""
        try:
            git_dir = self.repo_path / ".git"
            if git_dir.exists():
                return True
            # Try to find git root
            result = self._run_git(
                ["rev-parse", "--is-inside-work-tree"],
                check=False,
                stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError, Exception):
            return False

    def _validate_repo(self) -> None:
        """Validate that the path is a git repository (legacy)."""
        if not self.is_repo:
            raise ValueError(f"Not a git repository: {self.repo_path}")

    def _run_git(
        self,
        args: list[str],
        check: bool = True,
        capture_output: bool = True,
        stderr: Any = None,
        timeout: int = 30,
    ) -> subprocess.CompletedProcess:
        """Run a git command."""
        cmd = ["git"] + args
        return subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=capture_output,
            text=True,
            check=check,
            stderr=stderr,
            timeout=timeout,
        )

    def status(self) -> GitStatus:
        """Alias for get_status() for backward compatibility."""
        if not self.is_repo:
            return GitStatus(branch="none", is_clean=True, staged_files=[], modified_files=[], untracked_files=[])
        return self.get_status()

    def add_all(self) -> GitResult:
        """Stage all changes."""
        if not self.is_repo:
            return GitResult(success=True)  # No-op in non-git repo
        try:
            self.stage_files(["."])
            return GitResult(success=True)
        except Exception as e:
            return GitResult(success=False, error=str(e))

    def get_status(self) -> GitStatus:
        """Get current git status."""
        if not self.is_repo:
            return GitStatus(branch="none", is_clean=True, staged_files=[], modified_files=[], untracked_files=[])
        result = self._run_git(["status", "--porcelain", "-b"])
        lines = result.stdout.strip().split("\n")

        # Parse branch and ahead/behind from first line
        branch = "unknown"
        ahead = 0
        behind = 0
        if lines and lines[0].startswith("##"):
            branch_info = lines[0][3:]
            if "..." in branch_info:
                branch = branch_info.split("...")[0]
                # Check for [ahead X, behind Y]
                import re

                match = re.search(r"\[ahead (\d+)(?:, behind (\d+))?\]", branch_info)
                if match:
                    ahead = int(match.group(1))
                    if match.group(2):
                        behind = int(match.group(2))
                else:
                    match = re.search(r"\[behind (\d+)\]", branch_info)
                    if match:
                        behind = int(match.group(1))
            else:
                branch = branch_info
            lines = lines[1:]

        staged = []
        modified = []
        untracked = []

        for line in lines:
            if not line:
                continue
            status = line[:2]
            filepath = line[3:]

            if status[0] in "MADRC":
                staged.append(filepath)
            if status[1] in "MD":
                modified.append(filepath)
            if status == "??":
                untracked.append(filepath)

        return GitStatus(
            branch=branch,
            is_clean=len(staged) == 0 and len(modified) == 0,
            staged_files=staged,
            modified_files=modified,
            untracked_files=untracked,
            ahead=ahead,
            behind=behind,
        )

    def get_current_branch(self) -> str:
        """Get current branch name."""
        if not self.is_repo:
            return "none"
        result = self._run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        return str(result.stdout).strip()

    def get_diff(self, staged: bool = False) -> str:
        """Get diff of changes.

        Args:
            staged: If True, show staged changes. Otherwise show unstaged.
        """
        if not self.is_repo:
            return ""
        args = ["diff"]
        if staged:
            args.append("--staged")
        result = self._run_git(args)
        return str(result.stdout)

    def get_log(self, count: int = 10) -> list[GitCommit]:
        """Get recent commits."""
        if not self.is_repo:
            return []
        result = self._run_git(
            [
                "log",
                f"-{count}",
                "--format=%H|%s|%an|%ai",
            ]
        )

        commits = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|")
            if len(parts) >= 4:
                commits.append(
                    GitCommit(
                        sha=parts[0],
                        message=parts[1],
                        author=parts[2],
                        date=parts[3],
                    )
                )

        return commits

    def stage_files(self, files: list[str]) -> None:
        """Stage files for commit."""
        if not self.is_repo:
            return
        if files:
            self._run_git(["add"] + files)

    def commit(self, message: str) -> GitResult:
        """Create a commit.

        Returns:
            GitResult containing the commit SHA if successful.
        """
        if not self.is_repo:
            return GitResult(success=True, data="none")
        try:
            self._run_git(["commit", "-m", message])
            result = self._run_git(["rev-parse", "HEAD"])
            sha = str(result.stdout).strip()
            return GitResult(success=True, data=sha)
        except Exception as e:
            return GitResult(success=False, error=str(e))

    def create_branch(self, name: str, checkout: bool = True) -> None:
        """Create a new branch."""
        if not self.is_repo:
            return
        self._run_git(["branch", name])
        if checkout:
            self._run_git(["checkout", name])

    def checkout(self, ref: str) -> None:
        """Checkout a branch or commit."""
        if not self.is_repo:
            return
        self._run_git(["checkout", ref])

    def pull(self, remote: str = "origin", branch: str | None = None) -> None:
        """Pull from remote."""
        if not self.is_repo:
            return
        args = ["pull", remote]
        if branch:
            args.append(branch)
        self._run_git(args)

    def push(
        self,
        remote: str = "origin",
        branch: str | None = None,
        set_upstream: bool = False,
        force_with_lease: bool = False,
    ) -> GitResult:
        """Push to remote."""
        if not self.is_repo:
            return GitResult(success=True)
        args = ["push", remote]
        if set_upstream:
            args.append("-u")
        if force_with_lease:
            args.append("--force-with-lease")
        if branch:
            args.append(branch)

        try:
            result = self._run_git(args)
            return GitResult(success=True, output=result.stdout)
        except Exception as e:
            return GitResult(success=False, error=str(e))

    def stash(self, message: str | None = None) -> None:
        """Stash current changes."""
        if not self.is_repo:
            return
        args = ["stash", "push"]
        if message:
            args.extend(["-m", message])
        self._run_git(args)

    def stash_pop(self) -> None:
        """Pop stashed changes."""
        if not self.is_repo:
            return
        self._run_git(["stash", "pop"])
