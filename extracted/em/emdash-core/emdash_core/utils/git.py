"""Git utilities for repository detection and URL handling."""

import subprocess
from pathlib import Path
from typing import Optional


def get_git_remote_url(repo_root: Path) -> Optional[str]:
    """Get the origin remote URL from git.

    Args:
        repo_root: Path to the git repository root

    Returns:
        The remote URL or None if not found
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def normalize_repo_url(url: str) -> str:
    """Normalize git URL to https format for matching.

    Handles various git URL formats:
    - git@github.com:user/repo.git -> https://github.com/user/repo
    - https://github.com/user/repo.git -> https://github.com/user/repo
    - ssh://git@github.com/user/repo.git -> https://github.com/user/repo

    Args:
        url: Git remote URL in any format

    Returns:
        Normalized https URL without .git suffix
    """
    url = url.strip()

    # Remove .git suffix
    if url.endswith(".git"):
        url = url[:-4]

    # Handle SSH format: git@github.com:user/repo
    if url.startswith("git@"):
        # git@github.com:user/repo -> https://github.com/user/repo
        url = url.replace("git@", "https://", 1)
        url = url.replace(":", "/", 1)

    # Handle ssh:// format: ssh://git@github.com/user/repo
    elif url.startswith("ssh://"):
        url = url.replace("ssh://git@", "https://", 1)
        url = url.replace("ssh://", "https://", 1)

    # Ensure https prefix
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    return url


def get_normalized_remote_url(repo_root: Path) -> Optional[str]:
    """Get the normalized origin remote URL.

    Combines get_git_remote_url and normalize_repo_url.

    Args:
        repo_root: Path to the git repository root

    Returns:
        Normalized https URL or None if not found
    """
    remote_url = get_git_remote_url(repo_root)
    if remote_url:
        return normalize_repo_url(remote_url)
    return None


def get_current_branch(repo_root: Path) -> Optional[str]:
    """Get the current git branch name.

    Args:
        repo_root: Path to the git repository root

    Returns:
        The current branch name or None if not found/not in a git repo
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def get_git_status_summary(repo_root: Path) -> Optional[str]:
    """Get a brief summary of git status.

    Args:
        repo_root: Path to the git repository root

    Returns:
        Brief status summary (e.g., "3 modified, 2 untracked") or None
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return None

        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        if not lines:
            return "clean"

        # Count by status type
        modified = 0
        untracked = 0
        staged = 0
        deleted = 0

        for line in lines:
            if not line:
                continue
            status = line[:2]
            if status == "??":
                untracked += 1
            elif status[0] in ("M", "A", "D", "R", "C"):
                staged += 1
            elif status[1] == "M":
                modified += 1
            elif status[1] == "D":
                deleted += 1

        parts = []
        if staged:
            parts.append(f"{staged} staged")
        if modified:
            parts.append(f"{modified} modified")
        if deleted:
            parts.append(f"{deleted} deleted")
        if untracked:
            parts.append(f"{untracked} untracked")

        return ", ".join(parts) if parts else "clean"

    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def get_repo_name(repo_root: Path) -> Optional[str]:
    """Get the repository name from the remote URL or directory name.

    Args:
        repo_root: Path to the git repository root

    Returns:
        Repository name (e.g., "user/repo") or None
    """
    remote_url = get_normalized_remote_url(repo_root)
    if remote_url:
        # Extract user/repo from https://github.com/user/repo
        parts = remote_url.rstrip("/").split("/")
        if len(parts) >= 2:
            return f"{parts[-2]}/{parts[-1]}"
    # Fallback to directory name
    return repo_root.name
