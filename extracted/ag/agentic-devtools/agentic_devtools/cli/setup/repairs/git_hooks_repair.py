"""Git hooks repair for the doctor framework.

Configures ``core.hooksPath`` to ``.githooks`` if inside a git repo.
Non-destructive: an existing ``core.hooksPath`` pointing anywhere other than
``.githooks`` is preserved, and management can be disabled entirely with
``"manage_git_hooks": false`` in ``.agdt/config/project.json``.
Idempotent: if already configured with ``.githooks`` dir present, returns
``False`` (no-op).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..dependency_checker import DependencyStatus
from ..git_hooks_policy import (
    HOOKS_DISABLED_MESSAGE,
    format_preserved_message,
    is_git_hooks_management_enabled,
)


def repair_git_hooks(dep: DependencyStatus) -> bool:
    """Repair missing git hooks configuration.

    Args:
        dep: The ``DependencyStatus`` for the ``git-hooks`` check.

    Returns:
        ``True`` if hooks were configured (applied), ``False`` if already
        configured, preserved, or disabled by project config (no-op).

    Raises:
        RuntimeError: If git is not available, not in a git repo, or the
            configuration command fails.
    """
    # Determine repo root
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except FileNotFoundError:
        raise RuntimeError("git binary not found — cannot configure hooks path")
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("git command timed out — cannot configure hooks path") from exc

    if result.returncode != 0:
        raise RuntimeError("Not inside a git repository — cannot configure hooks path")

    repo_root = Path(result.stdout.strip())

    # Defence in depth: the doctor never dispatches this repair once the checker
    # reports the toggle as non-blocking, but a direct call still must not write.
    if not is_git_hooks_management_enabled(repo_root):
        print(HOOKS_DISABLED_MESSAGE)
        dep.found = True
        return False

    # Check current hooksPath
    try:
        config_result = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except FileNotFoundError:
        raise RuntimeError("git binary not found — cannot configure hooks path")
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("git command timed out — cannot configure hooks path") from exc

    hooks_path_set = config_result.returncode == 0
    current_hooks_path = config_result.stdout.strip() if hooks_path_set else ""

    # If already configured to .githooks and the dir exists → no-op
    if current_hooks_path == ".githooks" and (repo_root / ".githooks").is_dir():
        dep.found = True
        return False

    # A foreign hooks path (including an explicitly-configured empty value) belongs to
    # another tool (Husky, pre-commit, …) → preserve it.
    # Defence in depth, as above: unreachable via the doctor, reachable via a direct call.
    if hooks_path_set and current_hooks_path != ".githooks":
        print(format_preserved_message(current_hooks_path))
        dep.found = True
        return False

    # Call setup_git_hooks() to perform the configuration
    from ..script_generators.required_setup import setup_git_hooks

    try:
        result_msg = setup_git_hooks()
    except FileNotFoundError:
        raise RuntimeError("git binary not found — cannot configure hooks path")

    if result_msg is None:
        raise RuntimeError("No git context — cannot configure hooks path")

    if "Failed to set core.hooksPath" in result_msg:
        raise RuntimeError(result_msg.strip())

    # setup_git_hooks() declined to write (preserved or disabled) — nothing to
    # post-verify, and the ``.githooks`` post-checks below would falsely fail.
    if "core.hooksPath set to '.githooks'" not in result_msg:
        print(result_msg)
        dep.found = True
        return False

    # Post-check: verify .githooks directory exists
    if not (repo_root / ".githooks").is_dir():
        raise RuntimeError(f"Git hooks configured but .githooks directory does not exist at {repo_root / '.githooks'}")

    # Post-check: verify core.hooksPath is actually set to .githooks
    try:
        verify_result = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"Post-verification failed: {exc}") from exc

    actual = verify_result.stdout.strip()
    if actual != ".githooks":
        label = actual if actual else "(not set)"
        raise RuntimeError(f"Post-verification failed: core.hooksPath is {label!r}, expected '.githooks'")

    dep.found = True
    return True
