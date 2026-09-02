"""Build the changed-file list for the setup-expectations drift gate.

Encapsulates all changed-file resolution so both the standalone script
(``scripts/check_setup_expectations_drift.py``) and the parallel check
runner (``commands.py``) share the exact same logic.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from agentic_devtools.cli.checks.changed_files import DiffUnavailableError, get_changed_files


def _build_drift_file_list(cwd: Path) -> tuple[list[str], list[str]]:
    """Return ``(files, deleted_paths)`` for the drift gate.

    ``files`` contains all changed paths (including deleted/renamed paths)
    suitable for passing to :func:`check_drift`.

    ``deleted_paths`` contains paths that were deleted or renamed away,
    needed by :func:`ensure_placeholder_docs` to avoid re-creating
    intentionally removed placeholders.

    The function reuses :func:`get_changed_files` for the primary
    non-deleted file list, then supplements it with a ``git diff
    --name-status --diff-filter=DR`` call to capture deletions and, for
    renames, both the *old* path (added to ``deleted_paths`` and
    ``extra_paths``) and the *new* path (added to ``extra_paths`` only).
    """
    # 1. Primary: non-deleted changed files (all types, not just *.py)
    try:
        primary = get_changed_files(pattern="*", cwd=cwd)
    except DiffUnavailableError:
        primary = []

    # 2. Supplementary: deletions and renames
    deleted_paths: list[str] = []
    extra_paths: list[str] = []
    _collect_deletions_renames(cwd, deleted_paths, extra_paths)

    # 3. Merge and deduplicate
    combined_set: set[str] = set(primary)
    combined_set.update(extra_paths)
    combined_set.update(deleted_paths)
    files = sorted(combined_set)

    deduped_deleted = sorted(set(deleted_paths))
    return files, deduped_deleted


# Revision-selection fallback ladder matching get_changed_files().
_DIFF_STRATEGIES: list[list[str]] = [
    ["git", "diff", "--name-status", "--find-renames", "--diff-filter=DR", "origin/main...HEAD"],
    ["git", "diff", "--name-status", "--find-renames", "--diff-filter=DR", "HEAD~10..HEAD"],
    ["git", "diff", "--name-status", "--find-renames", "--diff-filter=DR", "HEAD~1..HEAD"],
    [
        "git",
        "diff-tree",
        "--name-status",
        "-r",
        "--find-renames",
        "--diff-filter=DR",
        "HEAD",
    ],
]


def _collect_deletions_renames(
    cwd: Path,
    deleted_paths: list[str],
    extra_paths: list[str],
) -> None:
    """Populate *deleted_paths* and *extra_paths* from ``git diff --name-status``.

    Tries each strategy in :data:`_DIFF_STRATEGIES` until one succeeds.
    On complete failure the lists are left empty (best-effort).
    """
    cwd_str = str(cwd)
    output: str | None = None

    for cmd in _DIFF_STRATEGIES:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd_str)
        except (FileNotFoundError, OSError):
            continue
        if result.returncode == 0:
            output = result.stdout
            break

    if output is None:
        return

    for line in output.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0] if parts else ""
        if status.startswith("D") and len(parts) >= 2:
            deleted_paths.append(parts[1])
            extra_paths.append(parts[1])
        elif status.startswith("R") and len(parts) >= 3:
            old_path = parts[1]
            new_path = parts[2]
            deleted_paths.append(old_path)
            extra_paths.append(old_path)
            extra_paths.append(new_path)
