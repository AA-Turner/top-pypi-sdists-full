"""
cvc.agent.git_integration — Git integration for the CVC agent.

Auto-detects Git repositories, shows uncommitted changes on startup,
offers to create Git commits alongside CVC commits, and provides
git status information via /git command.
"""

from __future__ import annotations

import logging
import subprocess
from cvc._subprocess_compat import HIDDEN_KW
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.agent.git_integration")


def is_git_repo(workspace: Path) -> bool:
    """Check if the workspace is inside a Git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(workspace),
            timeout=5,
                    **HIDDEN_KW,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def git_status(workspace: Path) -> dict[str, Any]:
    """
    Get the current Git status.
    Returns dict with branch, modified files, untracked files, etc.
    """
    result: dict[str, Any] = {
        "is_git": False,
        "branch": "",
        "staged": [],
        "modified": [],
        "untracked": [],
        "ahead": 0,
        "behind": 0,
        "clean": True,
    }

    if not is_git_repo(workspace):
        return result

    result["is_git"] = True

    try:
        # Current branch
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(workspace), timeout=5,
                    **HIDDEN_KW,
        )
        result["branch"] = branch_result.stdout.strip()

        # Status --porcelain
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(workspace), timeout=5,
                    **HIDDEN_KW,
        )

        for line in status_result.stdout.splitlines():
            if not line.strip():
                continue
            status_code = line[:2]
            filepath = line[3:].strip()

            if status_code[0] in ("M", "A", "D", "R"):
                result["staged"].append(filepath)
            if status_code[1] == "M":
                result["modified"].append(filepath)
            elif status_code[1] == "D":
                result["modified"].append(filepath)
            elif status_code == "??":
                result["untracked"].append(filepath)

        result["clean"] = not (result["staged"] or result["modified"] or result["untracked"])

        # Ahead/behind
        try:
            ab_result = subprocess.run(
                ["git", "rev-list", "--left-right", "--count", f"HEAD...@{{upstream}}"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(workspace), timeout=5,
                            **HIDDEN_KW,
            )
            if ab_result.returncode == 0:
                parts = ab_result.stdout.strip().split()
                if len(parts) == 2:
                    result["ahead"] = int(parts[0])
                    result["behind"] = int(parts[1])
        except Exception:
            pass

    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.warning("Git status failed: %s", e)

    return result


def git_diff_summary(workspace: Path) -> str:
    """Get a summary of uncommitted Git changes."""
    try:
        # Staged changes
        staged = subprocess.run(
            ["git", "diff", "--cached", "--stat"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(workspace), timeout=10,
                    **HIDDEN_KW,
        )
        # Unstaged changes
        unstaged = subprocess.run(
            ["git", "diff", "--stat"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(workspace), timeout=10,
                    **HIDDEN_KW,
        )

        parts = []
        if staged.stdout.strip():
            parts.append(f"Staged changes:\n{staged.stdout.strip()}")
        if unstaged.stdout.strip():
            parts.append(f"Unstaged changes:\n{unstaged.stdout.strip()}")

        return "\n\n".join(parts) if parts else "Working tree clean"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "Could not read Git diff"


def git_commit(workspace: Path, message: str, add_all: bool = True) -> tuple[bool, str]:
    """
    Create a Git commit.
    Returns (success, message_or_hash).
    """
    try:
        if add_all:
            subprocess.run(
                ["git", "add", "-A"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(workspace), timeout=10,
                            **HIDDEN_KW,
            )

        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(workspace), timeout=10,
                    **HIDDEN_KW,
        )

        if result.returncode == 0:
            # Get the commit hash
            hash_result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(workspace), timeout=5,
                            **HIDDEN_KW,
            )
            commit_hash = hash_result.stdout.strip()
            return True, commit_hash
        else:
            error = result.stderr.strip() or result.stdout.strip()
            if "nothing to commit" in error.lower():
                return False, "Nothing to commit — working tree clean"
            return False, error

    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return False, str(e)


def git_log(workspace: Path, limit: int = 10) -> list[dict[str, str]]:
    """Get recent Git commit log."""
    try:
        result = subprocess.run(
            ["git", "log", f"--max-count={limit}", "--pretty=format:%h|%s|%an|%ar"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(workspace), timeout=10,
                    **HIDDEN_KW,
        )

        commits = []
        for line in result.stdout.splitlines():
            parts = line.split("|", 3)
            if len(parts) == 4:
                commits.append({
                    "hash": parts[0],
                    "message": parts[1],
                    "author": parts[2],
                    "time": parts[3],
                })
        return commits
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []


def format_git_status(status: dict[str, Any]) -> str:
    """Format git status for display."""
    if not status.get("is_git"):
        return "Not a Git repository"

    lines = [f"Git branch: {status['branch']}"]

    if status["ahead"]:
        lines.append(f"  ↑ {status['ahead']} ahead")
    if status["behind"]:
        lines.append(f"  ↓ {status['behind']} behind")

    if status["staged"]:
        lines.append(f"  Staged ({len(status['staged'])}): {', '.join(status['staged'][:5])}")
    if status["modified"]:
        lines.append(f"  Modified ({len(status['modified'])}): {', '.join(status['modified'][:5])}")
    if status["untracked"]:
        lines.append(f"  Untracked ({len(status['untracked'])}): {', '.join(status['untracked'][:5])}")

    if status["clean"]:
        lines.append("  Working tree clean ✓")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Sync — shared CLI ↔ dashboard logic (single source of truth)
# ---------------------------------------------------------------------------

import re as _re

_BRANCH_NAME_RE = _re.compile(r"^[A-Za-z0-9._/\-]{1,200}$")


def _run_git_raw(
    args: list[str], cwd: Path, timeout: float = 8.0
) -> tuple[int, str, str]:
    """Run ``git`` and return (rc, stdout, stderr). Never raises for git errors."""
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
                    **HIDDEN_KW,
        )
        return (
            proc.returncode,
            (proc.stdout or "").strip(),
            (proc.stderr or "").strip(),
        )
    except FileNotFoundError:
        return (127, "", "git executable not found on PATH")
    except subprocess.TimeoutExpired:
        return (124, "", f"git {' '.join(args)} timed out")


def _validate_remote_name(name: str) -> str | None:
    name = (name or "").strip()
    if not name:
        return None
    if name.startswith("-") or ".." in name or name.endswith("/") or name.endswith(".lock"):
        return None
    if not _BRANCH_NAME_RE.match(name):
        return None
    return name


def git_sync(
    workspace: Path,
    remote: str = "origin",
    push: bool = True,
    rebase: bool = False,
) -> dict[str, Any]:
    """Sync the workspace with its tracked remote — fetch + ff-pull + push.

    Single source of truth for both the gateway HTTP endpoint and the CLI
    ``/sync`` command. Returns a structured dict the caller can render.

    Returns:
        {
          "status": "ok" | "diverged" | "dirty" | "no_upstream" | "error",
          "branch": str,
          "remote": str,
          "fetched": bool,
          "pulled": int,
          "pushed": int,
          "ahead": int,
          "behind": int,
          "head": str,
          "message": str,
        }
    """
    base = {
        "branch": "",
        "remote": remote,
        "fetched": False,
        "pulled": 0,
        "pushed": 0,
        "ahead": 0,
        "behind": 0,
        "head": "",
    }

    if not is_git_repo(workspace):
        return {**base, "status": "error", "message": "Not a git repository."}

    safe_remote = _validate_remote_name(remote)
    if not safe_remote:
        return {**base, "status": "error", "message": f"Invalid remote name: {remote!r}"}
    remote = safe_remote
    base["remote"] = remote

    rc_b, branch, _ = _run_git_raw(["rev-parse", "--abbrev-ref", "HEAD"], workspace)
    if rc_b != 0 or not branch or branch == "HEAD":
        return {
            **base,
            "status": "error",
            "message": "Detached HEAD — checkout a branch before syncing.",
        }
    base["branch"] = branch

    rc_s, status_out, _ = _run_git_raw(["status", "--porcelain"], workspace)
    if rc_s == 0 and status_out:
        return {
            **base,
            "status": "dirty",
            "message": "Working tree has uncommitted changes — commit or stash before syncing.",
        }

    rc_u, upstream, _ = _run_git_raw(
        ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], workspace
    )
    if rc_u != 0 or not upstream:
        return {
            **base,
            "status": "no_upstream",
            "message": f"Branch '{branch}' has no upstream. Run `git push -u {remote} {branch}` once to set it.",
        }

    rc_f, out_f, err_f = _run_git_raw(["fetch", remote], workspace, timeout=30.0)
    if rc_f != 0:
        return {
            **base,
            "status": "error",
            "message": f"git fetch failed: {(err_f or out_f or '').strip()}",
        }
    base["fetched"] = True

    def _counts() -> tuple[int, int]:
        rc, out, _ = _run_git_raw(
            ["rev-list", "--left-right", "--count", "HEAD...@{u}"], workspace
        )
        if rc != 0 or not out:
            return (0, 0)
        try:
            a, b = out.split()
            return (int(a), int(b))
        except Exception:
            return (0, 0)

    ahead, behind = _counts()
    pulled = 0
    pushed = 0

    if behind > 0:
        pull_args = (
            ["pull", "--rebase", remote, branch]
            if rebase
            else ["pull", "--ff-only", remote, branch]
        )
        rc_p, out_p, err_p = _run_git_raw(pull_args, workspace, timeout=60.0)
        if rc_p != 0:
            return {
                **base,
                "ahead": ahead,
                "behind": behind,
                "status": "diverged",
                "message": (err_p or out_p or "").strip()
                or "History has diverged from remote — resolve manually (merge or rebase).",
            }
        pulled = behind

    ahead, behind = _counts()

    if push and ahead > 0:
        rc_pu, out_pu, err_pu = _run_git_raw(
            ["push", remote, branch], workspace, timeout=60.0
        )
        if rc_pu != 0:
            return {
                **base,
                "pulled": pulled,
                "ahead": ahead,
                "behind": behind,
                "status": "diverged",
                "message": (err_pu or out_pu or "").strip() or "git push failed.",
            }
        pushed = ahead
        ahead, behind = _counts()

    _, head, _ = _run_git_raw(["rev-parse", "--short", "HEAD"], workspace)

    if pulled == 0 and pushed == 0:
        msg = "Already up to date."
    else:
        parts = []
        if pulled:
            parts.append(f"pulled {pulled}")
        if pushed:
            parts.append(f"pushed {pushed}")
        msg = "Synced — " + ", ".join(parts) + "."

    return {
        **base,
        "pulled": pulled,
        "pushed": pushed,
        "ahead": ahead,
        "behind": behind,
        "head": head,
        "status": "ok",
        "message": msg,
    }
