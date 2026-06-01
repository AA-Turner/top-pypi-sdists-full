"""Git integration for codrninja — auto-checkpoint, patches, and rollback."""

import os
import subprocess
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

from .sessions import SessionManager


class GitCheckpoint:
    """Manages git checkpoints for safe file changes."""

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = project_root or os.getcwd()

    def _run_git(self, *args: str, cwd: Optional[str] = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git"] + list(args),
            cwd=cwd or self.project_root,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def is_git_repo(self) -> bool:
        """Check if the project root is inside a git repository."""
        result = self._run_git("rev-parse", "--is-inside-work-tree")
        return result.returncode == 0

    def get_branch(self) -> Optional[str]:
        """Get current git branch name."""
        result = self._run_git("rev-parse", "--abbrev-ref", "HEAD")
        if result.returncode == 0:
            return result.stdout.strip()
        return None

    def get_status(self) -> Dict[str, Any]:
        """Get git status summary."""
        if not self.is_git_repo():
            return {"is_repo": False}

        branch = self.get_branch()
        short = self._run_git("status", "--porcelain")
        files_changed = []
        if short.returncode == 0:
            for line in short.stdout.strip().split("\n"):
                if line.strip():
                    status = line[:2].strip()
                    filepath = line[3:].strip()
                    files_changed.append({"status": status, "path": filepath})

        return {
            "is_repo": True,
            "branch": branch,
            "files_changed": files_changed,
            "clean": len(files_changed) == 0,
        }

    def get_diff(self, paths: Optional[List[str]] = None) -> str:
        """Get unified diff of unstaged changes."""
        args = ["diff"]
        if paths:
            args += ["--"] + paths
        result = self._run_git(*args)
        return result.stdout if result.returncode == 0 else ""

    def get_diff_staged(self) -> str:
        """Get unified diff of staged changes."""
        result = self._run_git("diff", "--cached")
        return result.stdout if result.returncode == 0 else ""

    def checkpoint(self, session_name: str, message: Optional[str] = None) -> Dict[str, Any]:
        """Create a git checkpoint (stash or commit) before agent makes changes.

        Returns info about the checkpoint for rollback purposes.
        """
        if not self.is_git_repo():
            return {"success": False, "error": "Not a git repository"}

        status = self.get_status()
        if status.get("clean", True):
            return {"success": True, "message": "Working tree clean, no checkpoint needed", "hash": None}

        # Use git stash for checkpoint — non-destructive, reversible
        msg = message or f"codrninja checkpoint: {session_name} {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        result = self._run_git("stash", "push", "-m", msg)
        if result.returncode != 0:
            # Fallback: try to create a temporary commit
            self._run_git("add", "-A")
            self._run_git("commit", "-m", msg)
            head = self._run_git("rev-parse", "HEAD")
            return {
                "success": True,
                "method": "commit",
                "hash": head.stdout.strip() if head.returncode == 0 else None,
                "message": msg,
            }

        # Get stash hash
        stash_list = self._run_git("stash", "list")
        stash_hash = ""
        if stash_list.returncode == 0 and stash_list.stdout.strip():
            first_line = stash_list.stdout.strip().split("\n")[0]
            stash_hash = first_line.split(":")[0]

        return {
            "success": True,
            "method": "stash",
            "hash": stash_hash,
            "message": msg,
        }

    def rollback(self, method: str = "stash", hash_ref: Optional[str] = None) -> Dict[str, Any]:
        """Rollback to the last checkpoint.

        Args:
            method: 'stash' to pop stash, 'commit' to reset to commit
            hash_ref: Specific commit hash to reset to (for commit method)
        """
        if method == "stash":
            result = self._run_git("stash", "pop")
            if result.returncode == 0:
                return {"success": True, "method": "stash_pop"}
            return {"success": False, "error": result.stderr.strip()}

        if method == "commit" and hash_ref:
            # Reset to the checkpoint commit, keeping working tree changes
            result = self._run_git("reset", "--soft", hash_ref)
            if result.returncode == 0:
                return {"success": True, "method": "soft_reset", "hash": hash_ref}
            return {"success": False, "error": result.stderr.strip()}

        return {"success": False, "error": f"Unknown rollback method: {method}"}

    def save_patch(self, session_manager: SessionManager, session_name: str,
                   label: str = "auto") -> Dict[str, Any]:
        """Save current diff as a patch file in the session directory."""
        diff = self.get_diff()
        if not diff:
            staged = self.get_diff_staged()
            diff = staged

        if not diff:
            return {"success": True, "message": "No changes to patch", "patch_id": None}

        return session_manager.save_patch(session_name, diff, label=label)

    def get_log(self, count: int = 10) -> List[Dict[str, str]]:
        """Get recent git log entries."""
        result = self._run_git(
            "log", f"-{count}", "--pretty=format:%H|%an|%ae|%ai|%s", "--no-color"
        )
        if result.returncode != 0:
            return []

        entries = []
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("|", 4)
            if len(parts) >= 5:
                entries.append({
                    "hash": parts[0],
                    "author": parts[1],
                    "email": parts[2],
                    "date": parts[3],
                    "message": parts[4],
                })
        return entries