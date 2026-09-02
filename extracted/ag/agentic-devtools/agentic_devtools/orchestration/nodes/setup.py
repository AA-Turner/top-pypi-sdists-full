"""Setup node: validate context and create/resume the issue worktree and branch.

Replaces the legacy branch-only stub with real worktree management (feature
#1900). The node:

1. Validates the issue key.
2. Runs a pre-flight context check (FR-003) — refuses to operate inside a
   *different* issue's worktree.
3. Fetches ``origin`` (FR-001) — a fetch failure is a transient ``BlockedState``.
4. Detects an existing worktree (FR-002) — resume, or a structured corruption
   error (FR-010).
5. Otherwise creates a fresh worktree anchored to the freshly-fetched
   ``origin/main`` (FR-001), or a worktree tracking a matching remote branch.

All Git operations call Python functions directly (FR-007); no ``agdt-*``
subprocesses. Outcomes are returned as a :class:`SetupResult` embedded in the
graph state under ``setup_result`` (plus legacy ``setup_complete``/``error``
fields for checkpoint compatibility). ``SystemExit`` raised by ``core.py``
helpers is never allowed to escape the node boundary.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from agentic_devtools.cli.git.branch_naming import build_branch_name, normalize_issue_key
from agentic_devtools.cli.git.core import GitError, run_git_safe
from agentic_devtools.cli.git.worktree import create_worktree, detect_existing_worktree
from agentic_devtools.cli.workflows.preflight import get_current_git_branch, get_git_repo_root
from agentic_devtools.cli.workflows.worktree_setup import get_main_repo_root, is_in_worktree
from agentic_devtools.models.git_results import BlockedCategory, BlockedState, SetupResult
from agentic_devtools.orchestration.nodes._helpers import utc_now
from agentic_devtools.orchestration.state_schema import WorkOnIssueState

_MAIN_BRANCH = "main"

# Auth-failure patterns for git fetch stderr classification.
_FETCH_AUTH_PATTERNS = re.compile(
    r"authentication failed|permission denied|could not read Username|"
    r"Repository not found|403|fatal: could not read",
    re.IGNORECASE,
)


def _segment_matches(text: str, normalized_key: str, sep: str) -> bool:
    """Return whether ``normalized_key`` is an exact ``sep``-delimited segment of ``text``."""
    target = normalized_key.lower()
    return any(segment and segment.lower() == target for segment in text.split(sep))


def _preflight_context_error(normalized_key: str) -> BlockedState | None:
    """Validate the current directory/branch context (FR-003).

    Returns ``None`` when it is safe to proceed (context matches the issue, or we
    are in the repository root and will create a worktree). Returns a
    ``context_mismatch`` :class:`BlockedState` when the current context is a
    linked worktree whose branch or folder does not match the issue (either
    alone being set is insufficient inside a linked worktree).
    """
    branch = get_current_git_branch() or ""
    repo_root = get_git_repo_root() or ""

    # Normalize path separators so the check works on Windows (backslash paths).
    normalized_root = repo_root.replace(os.sep, "/") if os.sep != "/" else repo_root

    branch_ok = bool(branch) and _segment_matches(branch, normalized_key, "/")
    folder_ok = bool(normalized_root) and _segment_matches(normalized_root, normalized_key, "/")

    # Inside a linked worktree both the folder and the branch must reference the
    # issue — matching only one is insufficient (e.g. /repos/42 checked out on
    # ``main`` would satisfy folder_ok but must not proceed).  Outside a worktree
    # (main checkout) a single match is enough: the node will create/switch into
    # the correct worktree/branch.
    in_worktree = is_in_worktree()
    if in_worktree:
        if branch_ok and folder_ok:
            return None
    else:
        if branch_ok or folder_ok:
            return None

    # Context does not reference this issue. If we are inside some *other*
    # worktree, refuse to operate there. If we are in the main repo root, it is
    # safe to create/switch into the issue worktree.
    if in_worktree:
        return BlockedState(
            category="context_mismatch",
            message=(
                f"Current context (branch={branch or '<none>'}, root={repo_root or '<none>'}) "
                f"is a different worktree and does not match issue {normalized_key}; "
                f"refusing to run Git operations in the wrong context"
            ),
        )
    return None


def _find_remote_branch(main_root: str, normalized_key: str) -> str | None:
    """Return a remote branch name whose issue segment matches, or ``None``.

    Scans ``git ls-remote --heads origin`` for a ``refs/heads/<name>`` whose
    slash-delimited segments contain an exact match for ``normalized_key``.

    Raises:
        GitError: When ``ls-remote`` itself fails (transient network/auth error).
            The caller must classify this as ``auth`` or ``transient`` based on
            stderr patterns; ``None`` is reserved for a successful scan with no
            matching branch.
    """
    result = run_git_safe(["ls-remote", "--heads", "origin"], cwd=main_root)
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        ref = parts[1]
        if not ref.startswith("refs/heads/"):
            continue
        name = ref[len("refs/heads/") :]
        if _segment_matches(name, normalized_key, "/"):
            return name
    return None


def _resolve_description(state: WorkOnIssueState) -> str:
    """Derive a branch description from the issue summary, if available."""
    issue_data = state.get("issue_data", {})
    if isinstance(issue_data, dict):
        summary = issue_data.get("summary", "")
        if isinstance(summary, str) and summary.strip():
            return summary
    return "implementation"


def _resume_result_dict(result: SetupResult) -> dict[str, Any]:
    """Build the success state-update dict for a resume/create outcome."""
    return {
        "step": "setup",
        "error": None,
        "setup_complete": True,
        "setup_result": result,
        "source_branch": result.branch_name,
        "events": [
            {
                "event": "setup_completed",
                "timestamp": utc_now(),
                "signals": {
                    "mode": result.mode,
                    "branch": result.branch_name,
                    "worktree_path": result.worktree_path,
                },
            }
        ],
    }


def _blocked_result_dict(result: SetupResult) -> dict[str, Any]:
    """Build the blocked state-update dict for a failed setup outcome."""
    if result.error is None:  # defensive: callers pass error results
        raise ValueError("_blocked_result_dict requires a SetupResult with a non-None error")
    return {
        "step": "setup",
        "status": "blocked",
        "error": result.error.message,
        "setup_complete": False,
        "setup_result": result,
        "events": [
            {
                "event": "setup_failed",
                "timestamp": utc_now(),
                "signals": {"category": result.error.category, "error": result.error.message},
            }
        ],
    }


def setup_node(state: WorkOnIssueState) -> dict[str, Any]:
    """Create or resume the issue worktree and branch.

    See the module docstring for the full flow. Returns a LangGraph state-update
    dict containing a :class:`SetupResult` under ``setup_result``.
    """
    issue_key = state.get("issue_key", "")
    if not isinstance(issue_key, str) or not issue_key.strip():
        return _blocked_result_dict(
            SetupResult(
                error=BlockedState(
                    category="context_mismatch",
                    message="issue_key is required and must be a non-empty string",
                )
            )
        )

    try:
        normalized_key = normalize_issue_key(issue_key)
    except ValueError as exc:
        return _blocked_result_dict(SetupResult(error=BlockedState(category="context_mismatch", message=str(exc))))

    # Pre-flight context validation (FR-003).
    context_error = _preflight_context_error(normalized_key)
    if context_error is not None:
        return _blocked_result_dict(SetupResult(error=context_error))

    # Resolve the main repository root (worktrees are its siblings).
    main_root = get_main_repo_root() or get_git_repo_root()
    if not main_root:
        return _blocked_result_dict(
            SetupResult(
                error=BlockedState(
                    category="context_mismatch",
                    message="Could not determine the git repository root",
                )
            )
        )

    # Dry-run: return a simulated successful SetupResult without executing any mutating
    # git operation (fetch, create, or track a remote branch).
    if state.get("dry_run"):
        simulated_key = normalized_key
        description = _resolve_description(state)
        simulated_branch = build_branch_name(simulated_key, description)
        simulated_path = str(Path(main_root).parent / simulated_key)
        return _resume_result_dict(
            SetupResult(worktree_path=simulated_path, branch_name=simulated_branch, mode="created")
        )

    # Fetch origin so the new branch starts from the latest origin/main (FR-001).
    try:
        run_git_safe(["fetch", "origin"], cwd=main_root)
    except GitError as exc:
        exc_str = str(exc)
        category: BlockedCategory = "auth" if _FETCH_AUTH_PATTERNS.search(exc_str) else "transient"
        return _blocked_result_dict(
            SetupResult(error=BlockedState(category=category, message=f"git fetch origin failed: {exc_str}"))
        )

    # Detect an existing worktree (FR-002 / FR-010).
    try:
        detection = detect_existing_worktree(issue_key, main_root)
    except GitError as exc:
        return _blocked_result_dict(
            SetupResult(error=BlockedState(category="transient", message=f"Worktree detection failed: {exc}"))
        )

    if detection.status == "corrupt":
        return _blocked_result_dict(
            SetupResult(
                error=BlockedState(
                    category="corruption",
                    message=(
                        f"Worktree path {detection.path!r} exists but is not a valid git worktree; "
                        f"manual cleanup required before resuming issue {normalized_key}"
                    ),
                )
            )
        )

    if detection.status == "resume":
        branch = detection.branch
        if branch is None and detection.path:
            # Conventional-path match without a porcelain branch — look it up.
            try:
                branch_result = run_git_safe(["rev-parse", "--abbrev-ref", "HEAD"], cwd=detection.path)
                branch = branch_result.stdout.strip() or None
            except GitError:
                branch = None
        # A detached HEAD (abbrev-ref returns the literal "HEAD") or a failed
        # branch lookup means the worktree is not in a named-branch context;
        # resuming here would lead to a detached commit that push/PR creation
        # cannot target, so treat it as a context error.
        if not branch or branch == "HEAD":
            return _blocked_result_dict(
                SetupResult(
                    error=BlockedState(
                        category="context_mismatch",
                        message=(
                            f"Worktree at {detection.path!r} is in a detached HEAD state "
                            f"or has no named branch; attach it to a named branch before "
                            f"resuming issue {normalized_key}"
                        ),
                    )
                )
            )
        # Guard against resuming a worktree whose branch is unrelated to the issue
        # (e.g. a folder named after the issue that is currently checked out on main).
        if not _segment_matches(branch, normalized_key, "/"):
            return _blocked_result_dict(
                SetupResult(
                    error=BlockedState(
                        category="context_mismatch",
                        message=(
                            f"Worktree at {detection.path!r} is on branch {branch!r} which "
                            f"does not contain issue key {normalized_key}; refusing to resume "
                            f"on an unrelated branch"
                        ),
                    )
                )
            )
        return _resume_result_dict(SetupResult(worktree_path=detection.path, branch_name=branch, mode="resumed"))

    # Not found locally — check the remote for a matching branch to track.
    description = _resolve_description(state)
    try:
        remote_branch = _find_remote_branch(main_root, normalized_key)
    except GitError as exc:
        exc_str = str(exc)
        category = "auth" if _FETCH_AUTH_PATTERNS.search(exc_str) else "transient"
        return _blocked_result_dict(
            SetupResult(error=BlockedState(category=category, message=f"git ls-remote failed: {exc_str}"))
        )
    if remote_branch is not None:
        result = create_worktree(
            issue_key,
            description,
            branch_name=remote_branch,
            use_existing_branch=True,
        )
        if result.error is not None:
            return _blocked_result_dict(result)
        result.mode = "resumed"
        return _resume_result_dict(result)

    # Fresh creation anchored to the freshly-fetched origin/main (FR-001).
    result = create_worktree(
        issue_key,
        description,
        start_point=f"origin/{_MAIN_BRANCH}",
    )
    if result.error is not None:
        return _blocked_result_dict(result)
    # build_branch_name is deterministic; ensure branch_name is set for the PR node.
    if not result.branch_name:
        result.branch_name = build_branch_name(issue_key, description)
    return _resume_result_dict(result)
