"""Merge a git ref into main in a bare repo.

Provides the core merge logic used by both :class:`AgentExecutionManager`
(for automatic post-run merges) and :func:`attach_review_gate` (for
merge-after-review flows).  The caller handles locking, workspace refresh,
checkpointing, and ref cleanup.

Usage::

    result = await merge_ref_to_main(
        bare_repo_path="/path/to/bare.git",
        ref="refs/heads/pr/dashboard",
        squash=True,
        commit_message="Merge dashboard implementation",
    )
    if not result.merged:
        print(f"Conflict: {result.unmerged_files}")
"""

from __future__ import annotations

import asyncio
import logging
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from git import Repo
from git.exc import GitCommandError

from plato.git_ops.repo import AGENT_ACTOR, trust_git_directory

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MergeResult:
    """Result of a merge operation."""

    merged: bool
    """Whether the merge succeeded."""

    commit_sha: str = ""
    """SHA of the merge commit on main (empty on failure)."""

    unmerged_files: list[str] = field(default_factory=list)
    """Paths with unresolved conflicts (empty on success)."""


async def merge_ref_to_main(
    bare_repo_path: str,
    ref: str,
    *,
    squash: bool = False,
    commit_message: str = "",
    max_retries: int = 1,
) -> MergeResult:
    """Merge a published ref into main in the bare repo.

    Clones the bare repo into a temp dir, fetches the ref, merges (or
    squash-merges), and pushes back to main.  Retries on transient push
    failures up to *max_retries* times.

    Args:
        bare_repo_path: Path to the bare git repository.
        ref: Git ref to merge (e.g. ``refs/heads/pr/dashboard``).
        squash: If True, squash-merge (single commit). Otherwise regular merge.
        commit_message: Commit message. Defaults to ``"Merge {ref}"``.
        max_retries: Max attempts (retries on push race, not on conflict).

    Returns:
        :class:`MergeResult` with ``merged=True`` on success or
        ``merged=False`` with ``unmerged_files`` on conflict.
    """
    msg = commit_message or f"Merge {ref}"

    for attempt in range(1, max_retries + 1):
        temp_dir = Path(tempfile.mkdtemp(prefix="merge-"))
        try:
            await asyncio.to_thread(_clone_local, bare_repo_path, temp_dir)
            await asyncio.to_thread(_fetch_local, temp_dir, ref)

            if squash:
                conflicted, unmerged = await asyncio.to_thread(_squash_merge_local, temp_dir, msg)
            else:
                conflicted, unmerged = await asyncio.to_thread(_merge_local, temp_dir, msg)

            if conflicted:
                if attempt < max_retries:
                    logger.warning("Merge conflict for %s (attempt %d/%d), retrying", ref, attempt, max_retries)
                    continue
                return MergeResult(merged=False, unmerged_files=unmerged)

            await asyncio.to_thread(_push_main_local, temp_dir)
            commit_sha = await asyncio.to_thread(_rev_parse_local, temp_dir, "HEAD")
            return MergeResult(merged=True, commit_sha=commit_sha)
        except Exception:
            if attempt == max_retries:
                raise
            logger.warning("Merge attempt %d/%d failed for %s", attempt, max_retries, ref, exc_info=True)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    # Should not reach here, but satisfy type checker
    return MergeResult(merged=False)


async def delete_remote_ref(bare_repo_path: str, ref: str) -> bool:
    """Delete a ref from a bare repo."""
    return await asyncio.to_thread(_delete_ref_local, bare_repo_path, ref)


# ---------------------------------------------------------------------------
# Local git helpers (run in thread pool via asyncio.to_thread)
# ---------------------------------------------------------------------------


def _repo(path: Path | str) -> Repo:
    trust_git_directory(path)
    return Repo(path)


def _clone_local(bare_repo_path: str, temp_dir: Path) -> None:
    trust_git_directory(bare_repo_path)
    trust_git_directory(temp_dir)
    repo = Repo.clone_from(bare_repo_path, temp_dir)
    with repo.config_writer() as config:
        config.set_value("user", "email", AGENT_ACTOR.email)
        config.set_value("user", "name", AGENT_ACTOR.name)


def _fetch_local(temp_dir: Path, ref: str) -> None:
    _repo(temp_dir).remote("origin").fetch(ref)


def _merge_local(temp_dir: Path, commit_message: str) -> tuple[bool, list[str]]:
    """Regular merge. Returns (conflicted, unmerged_files)."""
    repo = _repo(temp_dir)
    try:
        repo.git.merge("FETCH_HEAD", "-m", commit_message)
        return False, []
    except GitCommandError as exc:
        unmerged = _unmerged_files(temp_dir)
        if unmerged:
            return True, unmerged
        raise RuntimeError(exc.stderr.strip() or exc.stdout.strip() or str(exc)) from exc


def _squash_merge_local(temp_dir: Path, commit_message: str) -> tuple[bool, list[str]]:
    """Squash merge. Returns (conflicted, unmerged_files)."""
    repo = _repo(temp_dir)
    try:
        repo.git.merge("FETCH_HEAD", "--squash")
    except GitCommandError as exc:
        unmerged = _unmerged_files(temp_dir)
        if unmerged:
            return True, unmerged
        raise RuntimeError(exc.stderr.strip() or exc.stdout.strip() or str(exc)) from exc
    # Squash merge stages but doesn't commit — commit now
    try:
        repo.git.commit("-m", commit_message)
    except GitCommandError:
        # Nothing to commit (no changes)
        pass
    return False, []


def _unmerged_files(temp_dir: Path) -> list[str]:
    return sorted(str(path) for path in _repo(temp_dir).index.unmerged_blobs().keys())


def _push_main_local(temp_dir: Path) -> None:
    _repo(temp_dir).git.push("--porcelain", "origin", "HEAD:main")


def _rev_parse_local(temp_dir: Path, ref: str) -> str:
    return _repo(temp_dir).commit(ref).hexsha


def _delete_ref_local(bare_repo_path: str, ref: str) -> bool:
    try:
        _repo(bare_repo_path).git.update_ref("-d", ref)
        return True
    except GitCommandError:
        return False
