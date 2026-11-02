"""Git branch synchronization for pull-request reviews."""

import json
import re
import sys
import time
from collections.abc import Callable
from typing import Any

from ...state import get_state_dir, get_value, is_dry_run, set_value
from ..subprocess_utils import run_safe
from .helpers import resolve_review_artifact_dir_name

_FULL_COMMIT_HASH_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")
_POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS = 3
_POST_SYNC_PR_DETAILS_REFRESH_DELAY_SECONDS = 1.0


def _try_force_push_after_rebase(dry_run: bool) -> bool | None:
    """Attempt force push after a successful rebase.

    Wraps ``force_push()`` so that a push failure is non-blocking: the rebase
    already succeeded locally and the caller can continue.

    Args:
        dry_run: If True, delegates to ``force_push(dry_run=True)`` which only
            prints what would happen.

    Returns:
        ``True`` if the push succeeded, ``False`` if it failed, or ``None``
        when running in dry-run mode.
    """
    from ..git.operations import force_push

    if dry_run:
        force_push(dry_run=True)
        return None

    try:
        force_push(dry_run=False)
        return True
    except SystemExit:
        print("Warning: Rebase succeeded but push failed. You can manually push with: git push --force-with-lease")
        return False


def _get_current_commit_hash(run_command: Callable[..., Any] | None = None) -> str | None:
    """Return the full SHA for the repository's current HEAD, when valid."""
    if run_command is None:
        run_command = run_safe
    try:
        result = run_command(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError:
        return None

    if result.returncode != 0 or not isinstance(result.stdout, str):
        return None

    commit_hash = result.stdout.strip()
    if not _FULL_COMMIT_HASH_PATTERN.fullmatch(commit_hash):
        return None
    return commit_hash.lower()


def _extract_source_commit_id(pr_details: dict[str, Any]) -> str | None:
    """Return the PR source commit id when present and valid."""
    pr_info = pr_details.get("pullRequest", pr_details)
    if not isinstance(pr_info, dict):
        return None
    source_commit = pr_info.get("lastMergeSourceCommit")
    if not isinstance(source_commit, dict):
        return None
    commit_id = source_commit.get("commitId")
    if not isinstance(commit_id, str):
        return None
    normalized_commit_id = commit_id.strip().lower()
    if not normalized_commit_id:
        return None
    return normalized_commit_id


def _refresh_pr_details_for_commit(
    current_commit_hash: str,
) -> dict[str, Any] | None:
    """Reload PR details until the API commit matches local HEAD or attempts are exhausted."""
    from ..pull_request_details import get_pull_request_details
    from ..workflows.base import _safe_print

    for attempt in range(1, _POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS + 1):
        try:
            refreshed_raw = get_pull_request_details()
        except (OSError, RuntimeError, SystemExit, TypeError, ValueError) as exc:
            _safe_print(
                f"Warning: Could not refresh PR details after sync (attempt "
                f"{attempt}/{_POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS}): {exc}",
                file=sys.stderr,
            )
        else:
            if isinstance(refreshed_raw, dict):
                refreshed_commit_id = _extract_source_commit_id(refreshed_raw)
                if refreshed_commit_id == current_commit_hash:
                    return refreshed_raw
                _safe_print(
                    f"Warning: Refreshed PR details commit "
                    f"({refreshed_commit_id or 'missing'}) did not match local HEAD "
                    f"({current_commit_hash}) on attempt "
                    f"{attempt}/{_POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS}.",
                    file=sys.stderr,
                )
            else:
                _safe_print(
                    f"Warning: Refreshed PR details had unexpected type "
                    f"{type(refreshed_raw).__name__!r} on attempt "
                    f"{attempt}/{_POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS}.",
                    file=sys.stderr,
                )

        if attempt < _POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS:
            time.sleep(_POST_SYNC_PR_DETAILS_REFRESH_DELAY_SECONDS)

    return None


def _checkout_and_prepare_source_branch(source_branch: str, dry_run: bool) -> tuple[bool, str | None]:
    """Checkout, fetch, and reset the source branch before review."""
    from ..git.operations import checkout_branch, fetch_branch, reset_branch_to_origin
    from ..workflows.base import _safe_print

    _safe_print(f"\nChecking out PR source branch: {source_branch}...")
    checkout_result = checkout_branch(source_branch, dry_run=dry_run)
    if not checkout_result.is_success:
        if checkout_result.needs_user_action:
            return (
                False,
                f"\n{'=' * 60}\n"
                f"⚠️  CANNOT CHECKOUT BRANCH\n"
                f"{'=' * 60}\n\n"
                f"{checkout_result.message}\n\n"
                f"After resolving, restart the workflow with:\n"
                f"  agdt-review-pull-request\n"
                f"{'=' * 60}",
            )
        return False, f"Error checking out branch: {checkout_result.message}"  # pragma: no cover

    if not fetch_branch(source_branch, dry_run=dry_run):
        return (
            False,
            f"Failed to fetch origin/{source_branch}. Cannot proceed with review on potentially stale code.",
        )
    if not reset_branch_to_origin(source_branch, dry_run=dry_run):
        return (
            False,
            f"Failed to reset branch to origin/{source_branch}. "
            "See the messages above for details and resolution steps.",
        )
    return True, None


def _sync_source_branch_with_main(dry_run: bool) -> tuple[bool, bool | None]:
    """Fetch main and rebase the source branch when possible."""
    from ..git.operations import fetch_main, rebase_onto_main
    from ..workflows.base import _safe_print

    if not fetch_main(dry_run=dry_run):
        _safe_print("Warning: Could not fetch from origin/main, continuing without rebase...")
        return False, None

    _safe_print("Rebasing onto origin/main...")
    rebase_result = rebase_onto_main(dry_run=dry_run)
    if rebase_result.is_success:
        _safe_print("Branch is synced with main.")
        push_succeeded = _try_force_push_after_rebase(dry_run) if rebase_result.was_rebased else None
        return False, push_succeeded
    if rebase_result.needs_manual_resolution:
        _safe_print(f"\n{'=' * 60}")
        _safe_print("⚠️  REBASE CONFLICTS DETECTED")
        _safe_print("=" * 60)
        _safe_print("The branch has conflicts with main that should be resolved.")
        _safe_print("However, the review can continue with the current branch state.")
        _safe_print("After the review, you may want to resolve conflicts separately.")
        _safe_print("=" * 60 + "\n")
        return True, None
    _safe_print(f"Warning: {rebase_result.message}")
    _safe_print("Continuing with review...")
    return False, None


def _refresh_artifact_commit_hash(
    save_files_on_branch: bool,
    refresh_review_commit_scope: bool,
    dry_run: bool,
    push_succeeded: bool | None,
) -> str | None:
    """Resolve the commit hash used to scope persisted branch artifacts."""
    artifact_commit_hash_short = get_value("review.commit_hash_short") if save_files_on_branch else None
    if refresh_review_commit_scope and not dry_run and push_succeeded in (True, None):
        current_commit_hash = _get_current_commit_hash()
        if current_commit_hash:
            artifact_commit_hash_short = current_commit_hash[:12]
            set_value("review.commit_hash_short", artifact_commit_hash_short)
    return artifact_commit_hash_short


def _get_branch_inventory(
    save_files_on_branch: bool,
) -> tuple[list[str], dict[str, str], dict[str, str], str | None]:
    """Collect branch changes and retain metadata when name-status parsing fails."""
    from ..git.operations import get_branch_change_inventory, get_files_changed_on_branch

    if not save_files_on_branch:
        return get_files_changed_on_branch(), {}, {}, None
    files_on_branch, change_types, rename_sources, diff_ref, inventory_loaded = get_branch_change_inventory()
    if not inventory_loaded:
        files_on_branch = get_files_changed_on_branch()
    return files_on_branch, change_types, rename_sources, diff_ref


def _persist_branch_inventory(
    pull_request_id: int,
    files_set: set[str],
    change_types_on_branch: dict[str, str],
    rename_sources_on_branch: dict[str, str],
    diff_ref: str | None,
    artifact_commit_hash_short: str | None,
) -> None:
    """Write branch file inventory and its diff metadata to review artifacts."""
    from ..workflows.base import _safe_print

    diff_base_ref = None
    if diff_ref is not None:
        diff_base_ref = diff_ref.removesuffix("...HEAD")
        merge_base_proc = run_safe(
            ["git", "merge-base", diff_base_ref, "HEAD"],
            capture_output=True,
            text=True,
            shell=False,
        )
        merge_base = merge_base_proc.stdout.strip()
        if merge_base_proc.returncode == 0 and merge_base:
            diff_base_ref = merge_base
        else:
            print(
                f"Warning: Could not resolve merge-base for '{diff_base_ref}...HEAD'; "
                "persisting diff base ref for recovered-file metadata.",
                file=sys.stderr,
            )

    dir_name = resolve_review_artifact_dir_name(
        pull_request_id,
        artifact_commit_hash_short,
        allow_discovery=False,
    )
    prompts_dir = get_state_dir() / "pull-request-review" / dir_name
    prompts_dir.mkdir(parents=True, exist_ok=True)
    files_on_branch_path = prompts_dir / "files-on-branch.json"
    with open(files_on_branch_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "files": list(files_set),
                "change_types": change_types_on_branch,
                "rename_sources": rename_sources_on_branch,
                "diff_base_ref": diff_base_ref,
            },
            f,
            indent=2,
        )
    _safe_print(f"Saved files on branch to: {files_on_branch_path}")


def checkout_and_sync_branch(
    source_branch: str,
    pull_request_id: int | None = None,
    save_files_on_branch: bool = False,
    dry_run: bool = False,
    refresh_review_commit_scope: bool = False,
) -> tuple[bool, str | None, set[str], bool, bool | None]:
    """
    Checkout the PR source branch, sync it with origin, and rebase onto main.

    This prepares the local working copy for the review by:
    1. Checking out the source branch
    2. Fetching the source branch from origin and hard-resetting to origin/<branch>
       so the local copy reflects the author's latest pushed commits
    3. Fetching the latest from origin/main
    4. Rebasing onto main (continues even if conflicts, with warning)
    5. If rebase rewrote history, force-pushing to update the remote

    Args:
        source_branch: The PR source branch name (without refs/heads/)
        pull_request_id: Optional PR ID for saving files_on_branch to JSON
        save_files_on_branch: Whether to save files_on_branch to JSON file
        dry_run: If True, skip destructive git operations (checkout, fetch,
            reset, rebase) — the function will still compute changed files
            based on the current HEAD.
        refresh_review_commit_scope: When True after live sync advances HEAD,
            including after a rewritten-branch push or reset/fetch advancement
            with no push attempt, refresh ``review.commit_hash_short`` from the
            local HEAD before writing branch inventory artifacts.

    Returns:
        Tuple of (success, error_message, files_on_branch, had_rebase_conflicts, push_succeeded)
        - success: True if checkout succeeded and we can proceed
        - error_message: If success is False, the message to show the user
        - files_on_branch: Set of file paths changed on this branch vs main
        - had_rebase_conflicts: True if rebase conflicts were detected
        - push_succeeded: True if auto-push succeeded, False if it failed,
          None if no push was attempted (no rebase, or dry-run)
    """
    from ..workflows.base import _safe_print

    checkout_success, checkout_error = _checkout_and_prepare_source_branch(source_branch, dry_run)
    if not checkout_success:
        return False, checkout_error, set(), False, None

    had_rebase_conflicts, push_succeeded = _sync_source_branch_with_main(dry_run)
    artifact_commit_hash_short = _refresh_artifact_commit_hash(
        save_files_on_branch,
        refresh_review_commit_scope,
        dry_run,
        push_succeeded,
    )

    _safe_print("\nIdentifying files changed on this branch...")
    files_on_branch, change_types_on_branch, rename_sources_on_branch, diff_ref = _get_branch_inventory(
        save_files_on_branch
    )
    files_set = set(files_on_branch)
    _safe_print(f"Found {len(files_set)} file(s) changed on this branch.")

    if save_files_on_branch and pull_request_id:
        _persist_branch_inventory(
            pull_request_id,
            files_set,
            change_types_on_branch,
            rename_sources_on_branch,
            diff_ref,
            artifact_commit_hash_short,
        )

    return True, None, files_set, had_rebase_conflicts, push_succeeded


def checkout_and_sync_branch_from_state() -> None:
    """Background-task entry point that checks out/syncs the PR source branch."""
    pr_id_raw = get_value("pull_request_id")
    if not pr_id_raw:
        print("Error: pull_request_id is required in state", file=sys.stderr)
        sys.exit(1)

    pull_request_id = int(pr_id_raw)
    details_path = get_state_dir() / "temp-get-pull-request-details-response.json"
    if not details_path.exists():
        print(f"Error: PR details file not found: {details_path}", file=sys.stderr)
        print("Run get_pull_request_details first.", file=sys.stderr)
        sys.exit(1)

    with open(details_path, encoding="utf-8") as f:
        pr_details = json.load(f)

    pr_info = pr_details.get("pullRequest", pr_details)
    source_branch = pr_info.get("sourceRefName", "").replace("refs/heads/", "")
    if not source_branch:
        print("Error: Could not determine source branch from PR details", file=sys.stderr)
        sys.exit(1)

    success, error, _files, _had_conflicts, _push = checkout_and_sync_branch(
        source_branch,
        pull_request_id,
        save_files_on_branch=True,
        dry_run=is_dry_run(),
    )
    if not success:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
