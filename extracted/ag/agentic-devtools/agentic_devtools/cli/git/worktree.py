"""Worktree detection and creation helpers for the setup node.

Implements FR-001, FR-002, and FR-010 of the worktree setup feature:

- Parse ``git worktree list --porcelain`` output into structured entries.
- Detect an existing worktree for a normalized issue key using both a porcelain
  scan (branch issue-key segment match) and the conventional filesystem path
  ``../{normalized-issue-key}/``.
- Distinguish a valid resume from a corrupt/stale directory (FR-010).
- Create a worktree by thin-wrapping
  :func:`agentic_devtools.cli.workflows.worktree_setup.create_worktree` (no
  duplicated ``git worktree add`` logic — FR-001/FR-007).

All git interaction goes through :func:`run_git_safe`, which raises
:class:`GitError` instead of calling ``sys.exit`` so the setup node can convert
failures into structured ``BlockedState`` results.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from agentic_devtools.cli.git.branch_naming import build_branch_name, normalize_issue_key
from agentic_devtools.cli.git.core import GitError, run_git_capture, run_git_safe
from agentic_devtools.cli.workflows.worktree_setup import create_worktree as _cli_create_worktree
from agentic_devtools.models.git_results import BlockedCategory, BlockedState, SetupResult


@dataclass
class WorktreeEntry:
    """A single entry parsed from ``git worktree list --porcelain``.

    Attributes:
        path: The absolute worktree path.
        branch: The branch name (``refs/heads/`` stripped), or ``None`` for a
            detached-HEAD worktree.
    """

    path: str
    branch: str | None


@dataclass
class WorktreeMatch:
    """A porcelain worktree entry that matched the target issue key."""

    path: str
    branch: str


@dataclass
class DetectionResult:
    """Outcome of :func:`detect_existing_worktree`.

    ``status`` values:

    - ``"resume"``: a valid existing worktree was found (``path``/``branch`` set
      when available).
    - ``"corrupt"``: the conventional path exists but is not a valid worktree and
      no porcelain match was found (FR-010).
    - ``"not_found"``: no existing worktree for this issue key.
    """

    status: Literal["resume", "corrupt", "not_found"]
    path: str | None = None
    branch: str | None = None


def parse_worktree_list_porcelain(output: str) -> list[WorktreeEntry]:
    """Parse ``git worktree list --porcelain`` output into :class:`WorktreeEntry` items.

    Porcelain format groups lines per worktree, separated by blank lines::

        worktree /path/to/wt
        HEAD <sha>
        branch refs/heads/feature/PROJ-42/impl

    A ``detached`` line (instead of ``branch``) marks a detached-HEAD worktree, in
    which case ``branch`` is ``None``.

    Args:
        output: Raw porcelain output.

    Returns:
        A list of parsed entries (in input order).
    """
    entries: list[WorktreeEntry] = []
    current_path: str | None = None
    current_branch: str | None = None
    have_worktree = False

    def _flush() -> None:
        nonlocal current_path, current_branch, have_worktree
        if have_worktree and current_path is not None:
            entries.append(WorktreeEntry(path=current_path, branch=current_branch))
        current_path = None
        current_branch = None
        have_worktree = False

    for raw_line in output.splitlines():
        line = raw_line.rstrip()
        if not line:
            _flush()
            continue
        if line.startswith("worktree "):
            # New record boundary — flush any in-progress record first.
            _flush()
            current_path = line[len("worktree ") :].strip()
            have_worktree = True
        elif line.startswith("branch "):
            ref = line[len("branch ") :].strip()
            if ref.startswith("refs/heads/"):
                ref = ref[len("refs/heads/") :]
            current_branch = ref
        elif line == "detached":
            current_branch = None

    _flush()
    return entries


def _branch_issue_segment_matches(branch: str, normalized_key: str) -> bool:
    """Return whether any slash-delimited branch segment exactly matches the key.

    The match is case-insensitive and requires an exact segment match (not a
    substring), per FR-002. Branch names with no ``/`` are treated as a single
    candidate segment.
    """
    target = normalized_key.lower()
    for segment in branch.split("/"):
        if segment and segment.lower() == target:
            return True
    return False


def find_issue_worktree(
    issue_key: str,
    worktree_entries: list[WorktreeEntry],
    *,
    repo_root: str | None = None,
) -> WorktreeMatch | None:
    """Find the first porcelain worktree whose branch targets the issue key.

    Args:
        issue_key: Raw issue key (normalized internally via
            :func:`normalize_issue_key`).
        worktree_entries: Parsed porcelain entries.
        repo_root: When provided, the primary checkout (whose resolved path
            equals ``repo_root``) is excluded so that the main repository
            itself is never returned as a matching issue worktree, even when
            it is currently on a branch that contains the issue key as a
            segment.

    Returns:
        A :class:`WorktreeMatch` for the first branch whose issue-key path segment
        exactly matches the normalized key, or ``None`` when no entry matches.
        Detached-HEAD entries (``branch is None``) are ignored.
    """
    normalized_key = normalize_issue_key(issue_key)
    repo_root_resolved = Path(repo_root).resolve() if repo_root is not None else None
    for entry in worktree_entries:
        if repo_root_resolved is not None and Path(entry.path).resolve() == repo_root_resolved:
            continue
        if entry.branch is None:
            continue
        if _branch_issue_segment_matches(entry.branch, normalized_key):
            return WorktreeMatch(path=entry.path, branch=entry.branch)
    return None


def check_conventional_path(repo_root: str, issue_key: str) -> Path | None:
    """Return the conventional ``../{normalized-issue-key}/`` path if it exists.

    Args:
        repo_root: The main repository root directory.
        issue_key: Raw issue key (normalized internally).

    Returns:
        The resolved conventional worktree :class:`~pathlib.Path` when it exists on
        disk, otherwise ``None``.
    """
    normalized_key = normalize_issue_key(issue_key)
    candidate = Path(repo_root).parent / normalized_key
    if candidate.exists():
        return candidate
    return None


def _is_valid_worktree_dir(path: Path, repo_root: str) -> bool:
    """Return whether ``path`` is a valid git worktree belonging to ``repo_root``.

    A valid linked worktree has a ``.git`` file (pointing at the main repo's
    ``.git/worktrees/<name>``); a main checkout has a ``.git`` directory. A
    stale/broken ``.git`` file left by a removed linked worktree still passes
    the existence check but causes ``git rev-parse --git-dir`` to fail — so
    we use that as the authoritative validation rather than just checking for
    the presence of the ``.git`` entry.

    The candidate's ``--git-common-dir`` is resolved and compared against the
    main repository's ``--git-common-dir``. This rejects a conventional-path
    directory that happens to be a valid git repository but belongs to a
    *different* repo (preventing commits to an unrelated origin).

    Returns:
        True when the ``.git`` entry exists, git considers the directory a
        valid git repository/worktree, and the candidate shares the same common
        git directory as ``repo_root``.
    """
    if not (path / ".git").exists():
        return False
    result = run_git_capture(["rev-parse", "--git-dir"], cwd=str(path))
    if result.returncode != 0:
        return False
    candidate_common = run_git_capture(["rev-parse", "--git-common-dir"], cwd=str(path))
    main_common = run_git_capture(["rev-parse", "--git-common-dir"], cwd=repo_root)
    if candidate_common.returncode != 0 or main_common.returncode != 0:
        return False
    candidate_abs = (path / candidate_common.stdout.strip()).resolve()
    main_abs = (Path(repo_root) / main_common.stdout.strip()).resolve()
    return candidate_abs == main_abs


def detect_existing_worktree(issue_key: str, repo_root: str) -> DetectionResult:
    """Detect an existing worktree for ``issue_key`` (FR-002, FR-010).

    Combines the porcelain scan and the conventional-path check. A valid porcelain
    match takes precedence over a stale conventional directory (so a leftover
    ``../{issue}/`` directory next to a valid worktree registered elsewhere does NOT
    trigger the corruption error).

    Args:
        issue_key: Raw issue key (normalized internally).
        repo_root: The main repository root directory.

    Returns:
        A :class:`DetectionResult` describing resume / corrupt / not_found.
    """
    # 1. Porcelain scan (authoritative — takes precedence over the filesystem path).
    porcelain = run_git_safe(["worktree", "list", "--porcelain"], cwd=repo_root)
    entries = parse_worktree_list_porcelain(porcelain.stdout)
    match = find_issue_worktree(issue_key, entries, repo_root=repo_root)
    if match is not None:
        # Validate the registered path exactly like the conventional-path fallback: a
        # porcelain entry whose path no longer exists on disk (stale/prunable) or whose
        # git-common-dir no longer belongs to this repository is corrupt, not resumable.
        match_path = Path(match.path)
        if not match_path.exists() or not _is_valid_worktree_dir(match_path, repo_root=repo_root):
            return DetectionResult(status="corrupt", path=match.path)
        return DetectionResult(status="resume", path=match.path, branch=match.branch)

    # 2. Conventional filesystem path fallback.
    conventional = check_conventional_path(repo_root, issue_key)
    if conventional is not None:
        # Never treat the primary checkout itself as a resumable issue worktree,
        # even when it lives at ../{issue-key}.
        if conventional.resolve() == Path(repo_root).resolve():
            return DetectionResult(status="not_found")
        if _is_valid_worktree_dir(conventional, repo_root=repo_root):
            return DetectionResult(status="resume", path=str(conventional), branch=None)
        # Path exists but is not a valid worktree and no porcelain match → corruption.
        return DetectionResult(status="corrupt", path=str(conventional))

    return DetectionResult(status="not_found")


def create_worktree(
    issue_key: str,
    description: str,
    *,
    start_point: str | None = None,
    branch_name: str | None = None,
    use_existing_branch: bool = False,
) -> SetupResult:
    """Create a worktree for ``issue_key`` (thin wrapper — FR-001/FR-007).

    Delegates to
    :func:`agentic_devtools.cli.workflows.worktree_setup.create_worktree` (no
    duplicated ``git worktree add`` logic) and adapts the result into a
    :class:`SetupResult`.

    Args:
        issue_key: Raw issue key (normalized internally for the worktree directory
            name and branch).
        description: Free-form description used to build the branch name via
            :func:`build_branch_name` (ignored when ``branch_name`` is provided).
        start_point: Optional git ref anchoring the new branch tip (e.g. a
            freshly-fetched ``origin/main``). Forwarded to the underlying
            ``git worktree add ... <start_point>``.
        branch_name: Exact branch name to use (for remote-tracking resume). When
            provided, ``description`` is not used to build a branch name.
        use_existing_branch: When True (with ``branch_name``), track the existing
            remote branch instead of creating a new one.

    Returns:
        A :class:`SetupResult`; on git failure ``error`` carries a
        ``BlockedState``.
    """
    normalized_key = normalize_issue_key(issue_key)
    resolved_branch = branch_name or build_branch_name(issue_key, description)

    try:
        cli_result = _cli_create_worktree(
            normalized_key,
            branch_name=resolved_branch,
            use_existing_branch=use_existing_branch,
            start_point=start_point,
        )
    except SystemExit as exc:
        code = exc.code if exc.code is not None else "<unknown>"
        return SetupResult(
            error=BlockedState(
                category="transient",
                message=f"Worktree creation helper called sys.exit({code}); treating as transient failure",
            )
        )
    except (GitError, OSError) as exc:  # pragma: no cover - defensive
        return SetupResult(error=BlockedState(category="transient", message=f"Worktree creation failed: {exc}"))

    if not cli_result.success:
        error_msg = cli_result.error_message or "Worktree creation failed"
        # Reserve "corruption" for the case where the worktree path exists on disk
        # but is not a valid git worktree — those require manual cleanup.
        # "branch already exists" and similar local-branch conflicts require manual
        # cleanup of the stale local branch and cannot be resolved by retrying, so
        # classify them as context_mismatch (permanent).
        # Other failures (lock contention, temporary git errors, OS errors) are
        # transient and safe to retry.
        is_corrupt = "not a git worktree" in error_msg
        is_permanent = is_corrupt or re.search(
            r"already exists|A branch named|branch .* already exists",
            error_msg,
            re.IGNORECASE,
        )
        if is_corrupt:
            category: BlockedCategory = "corruption"
        elif is_permanent:
            category = "context_mismatch"
        else:
            category = "transient"
        return SetupResult(
            worktree_path=cli_result.worktree_path or None,
            branch_name=cli_result.branch_name or None,
            error=BlockedState(
                category=category,
                message=error_msg,
            ),
        )

    return SetupResult(
        worktree_path=cli_result.worktree_path,
        branch_name=cli_result.branch_name,
        mode="created",
    )
