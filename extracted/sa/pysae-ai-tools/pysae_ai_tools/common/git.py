"""Shared low-level git helpers used by ``glab.clone_group`` and ``code.ensure_repo``.

The two callers have different high-level pull semantics:

- ``clone_group`` does ``git pull --rebase`` in batch mode across many repos
- ``ensure_repo`` does ``git pull --ff-only`` on a single repo, with branch
  switch and stash-or-discard handling

So the **per-pull workflow** stays in each module. What's shared here is
the small set of read-only or single-shot git operations both modules
need: detect default/current/tracking branches, check for local changes,
manage remote URL, resolve ``origin/HEAD``.
"""

import subprocess
from pathlib import Path


def run_git(
    repo_dir: Path,
    *args: str,
    timeout: int = 60,
) -> subprocess.CompletedProcess[str]:
    """Run ``git -C <repo_dir> <args...>`` capturing stdout/stderr as text."""
    return subprocess.run(
        ["git", "-C", str(repo_dir), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def current_branch(repo_dir: Path) -> str | None:
    """Get the current branch name, or None if in detached HEAD."""
    result = run_git(repo_dir, "branch", "--show-current", timeout=10)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return None


def default_branch(repo_dir: Path) -> str | None:
    """Get the default branch name from ``origin/HEAD`` (e.g. ``main`` or ``master``).

    Falls back to ``git remote set-head origin --auto`` then retries when
    ``origin/HEAD`` is not yet set in the local clone.
    """
    result = run_git(repo_dir, "symbolic-ref", "refs/remotes/origin/HEAD", timeout=10)
    if result.returncode == 0:
        return result.stdout.strip().removeprefix("refs/remotes/origin/")
    run_git(repo_dir, "remote", "set-head", "origin", "--auto", timeout=30)
    result = run_git(repo_dir, "symbolic-ref", "refs/remotes/origin/HEAD", timeout=10)
    if result.returncode == 0:
        return result.stdout.strip().removeprefix("refs/remotes/origin/")
    return None


def tracking_branch(repo_dir: Path) -> str | None:
    """Get the upstream tracking branch (e.g. ``origin/main``), or None."""
    result = run_git(
        repo_dir,
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{u}",
        timeout=10,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def remote_branch_exists(repo_dir: Path, branch: str) -> bool:
    """Check if ``origin/<branch>`` exists locally (after a fetch)."""
    result = run_git(repo_dir, "rev-parse", "--verify", f"refs/remotes/origin/{branch}", timeout=10)
    return result.returncode == 0


def has_local_changes(repo_dir: Path) -> bool:
    """Check if the working tree has uncommitted changes (staged, unstaged, or untracked)."""
    result = run_git(repo_dir, "status", "--porcelain", timeout=10)
    return bool(result.stdout.strip())


def get_remote_url(repo_dir: Path, remote: str = "origin") -> str | None:
    """Get the URL of a git remote, or None if not found."""
    try:
        result = run_git(repo_dir, "remote", "get-url", remote, timeout=10)
        if result.returncode == 0:
            return result.stdout.strip()
    except subprocess.TimeoutExpired:
        pass
    return None


def set_remote_url(repo_dir: Path, url: str, remote: str = "origin") -> bool:
    """Set the URL of a git remote. Returns True on success."""
    result = run_git(repo_dir, "remote", "set-url", remote, url, timeout=10)
    return result.returncode == 0


def normalize_url(url: str) -> str:
    """Normalize a git URL for comparison (strip trailing .git and slashes)."""
    return url.rstrip("/").removesuffix(".git")
