"""Staleness detection for backfill audits.

Detects whether review observations reference files that no longer exist
at HEAD, indicating the feedback may be outdated and should not drive
instruction updates.
"""

from __future__ import annotations

from pathlib import Path, PureWindowsPath

from agentic_devtools.cli.audit.models import ReviewObservation


def check_file_exists_at_head(file_path: str, repo_root: str) -> bool:
    """Check whether a file exists in the repository at HEAD.

    Args:
        file_path: Repo-relative file path to check.
        repo_root: Absolute path to the repository root.

    Returns:
        True if the file exists, False otherwise.
    """
    if not file_path:
        return False
    normalized = file_path.replace("\\", "/")
    if normalized.startswith("/"):
        normalized = normalized.lstrip("/")
    relative_path = Path(normalized)
    repo_root_path = Path(repo_root).resolve()

    if relative_path.is_absolute() or PureWindowsPath(normalized).is_absolute():
        return False
    if ".." in relative_path.parts:
        return False

    candidate = (repo_root_path / relative_path).resolve()
    if not candidate.is_relative_to(repo_root_path):
        return False

    return candidate.is_file()


def detect_stale_comments(
    observations: list[ReviewObservation],
    repo_root: str,
) -> list[ReviewObservation]:
    """Annotate observations whose referenced files no longer exist.

    For each observation, checks whether the file path still exists at HEAD.
    Returns a new list with ``is_stale=True`` for observations referencing
    deleted files.

    Args:
        observations: List of review observations to check.
        repo_root: Absolute path to the repository root.

    Returns:
        New list of observations with staleness annotations applied.
    """
    result: list[ReviewObservation] = []
    for obs in observations:
        if obs.file_path and not check_file_exists_at_head(obs.file_path, repo_root):
            # Create a new frozen instance with is_stale=True
            stale_obs = ReviewObservation(
                file_path=obs.file_path,
                line=obs.line,
                body=obs.body,
                diff_hunk=obs.diff_hunk,
                resolved=obs.resolved,
                reviewer=obs.reviewer,
                primary_category=obs.primary_category,
                secondary_category=obs.secondary_category,
                is_stale=True,
                pr_number=obs.pr_number,
            )
            result.append(stale_obs)
        else:
            result.append(obs)
    return result
