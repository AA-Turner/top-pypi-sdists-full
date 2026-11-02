"""Worktree setup capability helpers."""

from __future__ import annotations

import os
import platform
import re
import signal
import subprocess
import sys

from agentic_devtools.cli.git.core import GitError

from . import worktree_setup_repository as _m_worktree_setup_repository
from .worktree_setup_repository import WorktreeSetupResult


def _sanitize_worktree_setup_diagnostic(value: object) -> str:
    """Redact credentials and bound untrusted setup-script diagnostics."""
    from agentic_devtools.cli.setup.log_sanitizer import sanitize as _log_sanitize  # noqa: PLC0415

    from .worktree_setup import (
        _SETUP_DIAGNOSTIC_BEARER_PATTERN,
        _SETUP_DIAGNOSTIC_CREDENTIAL_PATTERN,
        _SETUP_DIAGNOSTIC_TOKEN_PATTERN,
        _SETUP_STDERR_READ_LIMIT,
    )

    text = str(value)
    text = "".join(" " if ord(char) < 32 or ord(char) == 127 else char for char in text)
    text = re.sub(r"\s+", " ", text).strip()
    # Value-based redaction first (catches raw env-var secrets without labels).
    text = _log_sanitize(text)
    text = _SETUP_DIAGNOSTIC_CREDENTIAL_PATTERN.sub("<redacted>", text)
    text = _SETUP_DIAGNOSTIC_BEARER_PATTERN.sub("<redacted>", text)
    text = _SETUP_DIAGNOSTIC_TOKEN_PATTERN.sub("<redacted>", text)
    return text[:_SETUP_STDERR_READ_LIMIT]


def _get_worktree_setup_stderr_capture_limit() -> int:
    """Return a bounded stderr capture size that still guarantees secret redaction."""
    from .worktree_setup import _SETUP_STDERR_READ_LIMIT, _SETUP_STDERR_SANITIZE_OVERLAP

    overlap = _SETUP_STDERR_SANITIZE_OVERLAP
    for env_var in ("AZURE_DEV_OPS_COPILOT_PAT", "GITHUB_TOKEN", "JIRA_COPILOT_PAT"):
        overlap = max(overlap, len(os.environ.get(env_var, "")))
    return _SETUP_STDERR_READ_LIMIT + overlap


def _terminate_worktree_setup_process_tree(proc: subprocess.Popen[str]) -> None:
    """Best-effort terminate the setup-script process tree within a bounded wait."""
    from .worktree_setup import _SETUP_SCRIPT_KILL_WAIT_SECONDS

    def _kill_process() -> None:
        try:
            proc.kill()
        except OSError:
            pass

    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                shell=False,
                timeout=_SETUP_SCRIPT_KILL_WAIT_SECONDS,
            )
            if result.returncode != 0:
                _kill_process()
        except subprocess.TimeoutExpired:
            _kill_process()
        except OSError:
            _kill_process()
    else:
        try:
            os.killpg(proc.pid, signal.SIGKILL)  # type: ignore[attr-defined]
        except ProcessLookupError, PermissionError, OSError:
            _kill_process()

    try:
        proc.wait(timeout=_SETUP_SCRIPT_KILL_WAIT_SECONDS)
    except subprocess.TimeoutExpired:
        pass


def _wait_for_worktree_removal(worktree_path: str) -> bool:
    """Wait briefly for a timed-out worktree removal to finish asynchronously."""
    import time

    from .worktree_setup import _SETUP_CLEANUP_CONFIRMATION_POLL_SECONDS, _SETUP_CLEANUP_CONFIRMATION_TIMEOUT_SECONDS

    deadline = time.monotonic() + _SETUP_CLEANUP_CONFIRMATION_TIMEOUT_SECONDS
    while os.path.exists(worktree_path) and time.monotonic() < deadline:
        time.sleep(_SETUP_CLEANUP_CONFIRMATION_POLL_SECONDS)
    return not os.path.exists(worktree_path)


def _remove_invocation_trust_if_worktree_gone(result: WorktreeSetupResult) -> None:
    """Remove trust only when this invocation added it and the path is gone."""
    if result.copilot_trust_added and not os.path.exists(result.worktree_path):
        from ..copilot.trust import remove_trusted_folder

        remove_trusted_folder(result.worktree_path)


def _cleanup_failed_worktree_setup(
    result: WorktreeSetupResult,
    *,
    failure_context: str = "the original target setup script failure",
) -> None:
    """Best-effort cleanup of invocation-owned worktree and created local branch."""
    from .worktree_setup import _SETUP_CLEANUP_TIMEOUT_SECONDS

    if not result.created_worktree:
        return

    try:
        try:
            cleanup_result = subprocess.run(
                ["git", "worktree", "remove", "--force", result.worktree_path],
                cwd=_m_worktree_setup_repository.get_main_repo_root(),
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                shell=False,
                timeout=_SETUP_CLEANUP_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as exc:
            print(
                f"Cleanup failed; retain {failure_context}. "
                f"Manual recovery may be required for worktree {result.worktree_path}: "
                f"{' '.join(str(a) for a in exc.cmd) if exc.cmd else 'git worktree remove'} "
                f"timed out after {_SETUP_CLEANUP_TIMEOUT_SECONDS}s",
                file=sys.stderr,
            )
            if result.copilot_trust_added and _wait_for_worktree_removal(result.worktree_path):
                _remove_invocation_trust_if_worktree_gone(result)
            return
        if cleanup_result.returncode == 0:
            print(
                f"Cleanup attempted for worktree created by this setup: {result.worktree_path} "
                f"(branch: {result.branch_name})"
            )
            if os.path.exists(result.worktree_path):
                print(
                    f"Cleanup failed; retain {failure_context}. "
                    f"Manual recovery may be required for worktree {result.worktree_path}: "
                    "git worktree remove reported success but path still exists",
                    file=sys.stderr,
                )
                return
            _remove_invocation_trust_if_worktree_gone(result)
            if result.created_branch:
                try:
                    branch_cleanup = subprocess.run(
                        ["git", "branch", "-D", result.branch_name],
                        cwd=_m_worktree_setup_repository.get_main_repo_root(),
                        capture_output=True,
                        encoding="utf-8",
                        errors="replace",
                        check=False,
                        shell=False,
                        timeout=_SETUP_CLEANUP_TIMEOUT_SECONDS,
                    )
                except subprocess.TimeoutExpired as exc:
                    print(
                        f"Cleanup failed; retain {failure_context}. "
                        f"Manual recovery may be required for branch {result.branch_name}: "
                        f"{' '.join(str(a) for a in exc.cmd) if exc.cmd else 'git branch -D'} "
                        f"timed out after {_SETUP_CLEANUP_TIMEOUT_SECONDS}s",
                        file=sys.stderr,
                    )
                    return
                if branch_cleanup.returncode != 0:
                    diagnostic = (
                        _sanitize_worktree_setup_diagnostic(branch_cleanup.stderr or "") or "git branch cleanup failed"
                    )
                    print(
                        f"Cleanup failed; retain {failure_context}. "
                        f"Manual recovery may be required for branch {result.branch_name}: {diagnostic}",
                        file=sys.stderr,
                    )
        else:
            diagnostic = (
                _sanitize_worktree_setup_diagnostic(cleanup_result.stderr or "") or "git worktree remove failed"
            )
            print(
                f"Cleanup failed; retain {failure_context}. "
                f"Manual recovery may be required for worktree {result.worktree_path}: {diagnostic}",
                file=sys.stderr,
            )
    except (FileNotFoundError, OSError) as exc:
        print(
            f"Cleanup failed; retain {failure_context}. "
            f"Manual recovery may be required for worktree {result.worktree_path}: "
            f"{_sanitize_worktree_setup_diagnostic(exc)}",
            file=sys.stderr,
        )


def check_worktree_exists(
    issue_key: str,
    *,
    require_registered: bool = False,
    expected_path: str | None = None,
) -> str | None:
    """
    Check if a worktree for the given issue key already exists.

    Args:
        issue_key: The issue key to check for
        require_registered: If True, require an explicit Git porcelain registration
            instead of accepting the conventional filesystem fallback.
        expected_path: When requiring registration, optionally match the exact
            expected path in Git porcelain rather than the branch name.

    Returns:
        The worktree path if it exists, None otherwise
    """
    main_repo_root = _m_worktree_setup_repository.get_main_repo_root()
    if not main_repo_root:
        raise GitError(
            1,
            "unable to resolve main repository root",
            ["rev-parse", "--git-common-dir"],
        )

    try:
        from ..git.worktree import detect_existing_worktree

        detection = detect_existing_worktree(
            issue_key,
            main_repo_root,
            require_porcelain=require_registered,
            expected_path=expected_path,
        )
    except GitError as exc:
        raise GitError(
            exc.returncode,
            _sanitize_worktree_setup_diagnostic(exc.stderr),
            exc.args_list,
        ) from exc

    if detection.status == "resume":
        return detection.path
    if detection.status == "corrupt":
        raise GitError(
            1,
            _sanitize_worktree_setup_diagnostic(f"git worktree candidate {detection.path} is invalid"),
            ["worktree", "list", "--porcelain"],
        )
    return None
