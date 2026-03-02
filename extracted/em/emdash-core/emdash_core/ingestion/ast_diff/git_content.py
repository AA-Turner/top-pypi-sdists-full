"""Extract file content at a git ref for AST parsing."""

from typing import Optional

import git


def get_file_at_ref(repo: git.Repo, file_path: str, ref: str) -> Optional[str]:
    """Get file content at a specific git ref.

    Args:
        repo: Git repository.
        file_path: Relative path within the repo.
        ref: Git ref (commit SHA, branch, tag, HEAD~1, etc.).

    Returns:
        File content as string, or None if file doesn't exist at that ref.
    """
    try:
        commit = repo.commit(ref)
        blob = commit.tree / file_path
        return blob.data_stream.read().decode("utf-8", errors="replace")
    except (KeyError, git.BadName, git.GitCommandError):
        return None


def get_changed_file_paths(repo: git.Repo, base_ref: str, head_ref: str) -> dict[str, str]:
    """Get paths of files changed between two refs with their change type.

    Args:
        repo: Git repository.
        base_ref: Base git ref.
        head_ref: Head git ref.

    Returns:
        Dict mapping file path to change type ('A', 'M', 'D', 'R').
    """
    try:
        base_commit = repo.commit(base_ref)
        head_commit = repo.commit(head_ref)
        diff = base_commit.diff(head_commit)
    except (git.BadName, git.GitCommandError):
        return {}

    changed: dict[str, str] = {}
    for change in diff:
        if change.change_type == "A":
            changed[change.b_path] = "A"
        elif change.change_type == "D":
            changed[change.a_path] = "D"
        elif change.change_type == "M":
            changed[change.b_path] = "M"
        elif change.change_type == "R":
            changed[change.a_path] = "D"
            changed[change.b_path] = "A"
        elif change.change_type in ("C", "T"):
            changed[change.b_path] = "M"

    return changed
