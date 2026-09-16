"""
Manages the ``.agdt/.gitignore`` file that prevents runtime state from being
committed on code branches.

The constant ``AGDT_GITIGNORE_ENTRIES`` is the single source of truth for:
1. The entries written to ``.agdt/.gitignore``.
2. The paths unstaged by ``stage_changes()`` in ``cli/git/operations.py``.
"""

import os
from pathlib import Path

# Paths (relative to .agdt/) that must be git-ignored on code branches.
# Used both for writing .agdt/.gitignore and for defense-in-depth unstaging
# in stage_changes().
AGDT_GITIGNORE_ENTRIES = ("runtime-bootstrap.json", "identity.json", "workflows/", "cache/")

AGDT_GITIGNORE_HEADER = (
    "# Managed by agentic-devtools — do not edit manually.\n"
    "# Ignores runtime state; tracked config/scripts remain visible.\n"
)


def ensure_agdt_gitignore(git_root: Path | None) -> bool:
    """Ensure ``.agdt/.gitignore`` contains the managed entries.

    Args:
        git_root: Repository/worktree root.  When ``None`` (not in a git
            repo) the call is a silent no-op.

    Returns:
        ``True`` when the file already matched or was successfully created/updated,
        ``False`` when *git_root* is ``None`` or a read or write error occurred.
    """
    succeeded, _ = ensure_agdt_gitignore_with_mutation(git_root)
    return succeeded


def ensure_agdt_gitignore_with_mutation(git_root: Path | None) -> tuple[bool, bool]:
    """Ensure ``.agdt/.gitignore`` contains the managed entries.

    Args:
        git_root: Repository/worktree root.  When ``None`` (not in a git
            repo) the call is a silent no-op.

    Returns:
        A tuple of ``(succeeded, mutated)``. ``succeeded`` is ``True`` when the
        file already matched or was successfully created/updated. ``mutated`` is
        ``True`` only when the file was created or updated on disk. Both values
        are ``False`` when *git_root* is ``None`` or a read or write error occurred.
    """
    if git_root is None:
        return False, False

    gitignore_path = git_root / ".agdt" / ".gitignore"
    try:
        gitignore_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            existing = gitignore_path.read_bytes()
        except FileNotFoundError:
            existing = None

        newline = os.linesep if existing is None else "\r\n" if b"\r\n" in existing else "\n"
        content = (AGDT_GITIGNORE_HEADER + "\n".join(AGDT_GITIGNORE_ENTRIES) + "\n").replace("\n", newline)
        encoded_content = content.encode("utf-8")
        if existing == encoded_content:
            return True, False
        gitignore_path.write_bytes(encoded_content)
        return True, True
    except OSError:
        return False, False
