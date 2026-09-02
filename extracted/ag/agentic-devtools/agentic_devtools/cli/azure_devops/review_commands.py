"""Pull Request Review commands - orchestrates PR review workflow.

This module provides the main entry point for reviewing pull requests,
handling the resolution of PR IDs from Jira issues and vice versa.
"""

import json
import os
import re
import sys
import time
from datetime import UTC
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ...state import delete_value, get_state_dir, get_value, is_dry_run, is_safe_dir_segment, set_value
from ..git import get_diff_lines_info, get_diff_patch, normalize_ref_name
from ..subprocess_utils import run_safe
from .auth import get_auth_headers, get_pat
from .config import AzureDevOpsConfig
from .helpers import parse_bool_from_state_value, require_requests, resolve_review_artifact_dir_name, verify_az_cli

if TYPE_CHECKING:
    from .review_state import FileEntry, SkippedFile

# Import helper modules


def _get_jira_issue_key_from_state() -> str | None:
    """Get Jira issue key from state."""
    return get_value("jira.issue_key")


def _get_pull_request_id_from_state() -> int | None:
    """Get pull request ID from state."""
    value = get_value("pull_request_id")
    if value is not None:
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    return None


def _get_linked_pull_request_from_jira(issue_key: str) -> int | None:
    """
    Fetch Jira issue and extract linked Azure DevOps pull request ID.

    This looks for remote links that point to Azure DevOps pull requests.

    Args:
        issue_key: Jira issue key (e.g., PROJECT-1234)

    Returns:
        Pull request ID if found, None otherwise
    """
    import re

    try:
        import requests as req_module
    except ImportError:
        print("Warning: 'requests' library required for Jira API calls", file=sys.stderr)
        return None

    # Import Jira config
    try:
        from ..jira.config import get_jira_base_url, get_jira_headers
        from ..jira.helpers import _get_ssl_verify
    except ImportError:  # pragma: no cover
        print("Warning: Jira module not available", file=sys.stderr)
        return None

    base_url = get_jira_base_url()
    headers = get_jira_headers()
    ssl_verify = _get_ssl_verify()

    # First, get the issue with remote links
    issue_url = f"{base_url}/rest/api/2/issue/{issue_key}?fields=summary"

    try:
        response = req_module.get(issue_url, headers=headers, verify=ssl_verify, timeout=30)
        if response.status_code != 200:
            return None
    except Exception:
        return None

    # Get remote links for the issue
    remote_links_url = f"{base_url}/rest/api/2/issue/{issue_key}/remotelink"

    try:
        response = req_module.get(remote_links_url, headers=headers, verify=ssl_verify, timeout=30)
        if response.status_code == 200:
            remote_links = response.json()

            # Look for Azure DevOps PR links
            # Pattern: https://dev.azure.com/{org}/{project}/_git/{repo}/pullrequest/{id}
            pr_url_pattern = re.compile(r"pullrequest[s]?/(\d+)", re.IGNORECASE)

            for link in remote_links:
                link_url = link.get("object", {}).get("url", "")
                if "dev.azure.com" in link_url or "visualstudio.com" in link_url:
                    match = pr_url_pattern.search(link_url)
                    if match:
                        return int(match.group(1))
    except Exception:  # pragma: no cover
        pass

    return None


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


_FULL_COMMIT_HASH_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")
_POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS = 3
_POST_SYNC_PR_DETAILS_REFRESH_DELAY_SECONDS = 1.0


def _get_current_commit_hash() -> str | None:
    """Return the full SHA for the repository's current HEAD, when valid."""
    try:
        result = run_safe(
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
    details_path: Path,
    current_commit_hash: str,
) -> dict[str, Any] | None:
    """Reload PR details until the API commit matches local HEAD or attempts are exhausted."""
    from .pull_request_details_commands import get_pull_request_details

    for attempt in range(1, _POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS + 1):
        try:
            get_pull_request_details()
            with open(details_path, encoding="utf-8") as details_file:
                refreshed_raw = json.load(details_file)
        except (OSError, SystemExit, TypeError, ValueError) as exc:
            print(
                f"Warning: Could not refresh PR details after sync (attempt "
                f"{attempt}/{_POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS}): {exc}",
                file=sys.stderr,
            )
        else:
            if isinstance(refreshed_raw, dict):
                refreshed_commit_id = _extract_source_commit_id(refreshed_raw)
                if refreshed_commit_id == current_commit_hash:
                    return refreshed_raw
                print(
                    f"Warning: Refreshed PR details commit "
                    f"({refreshed_commit_id or 'missing'}) did not match local HEAD "
                    f"({current_commit_hash}) on attempt "
                    f"{attempt}/{_POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS}.",
                    file=sys.stderr,
                )
            else:
                print(
                    f"Warning: Refreshed PR details had unexpected type "
                    f"{type(refreshed_raw).__name__!r} on attempt "
                    f"{attempt}/{_POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS}.",
                    file=sys.stderr,
                )

        if attempt < _POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS:
            time.sleep(_POST_SYNC_PR_DETAILS_REFRESH_DELAY_SECONDS)

    return None


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
    from ..git.operations import (
        checkout_branch,
        fetch_branch,
        fetch_main,
        get_branch_change_inventory,
        get_files_changed_on_branch,
        rebase_onto_main,
        reset_branch_to_origin,
    )

    # Step 1: Checkout the source branch
    print(f"\nChecking out PR source branch: {source_branch}...")
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
                set(),
                False,
                None,
            )
        return (  # pragma: no cover
            False,
            f"Error checking out branch: {checkout_result.message}",
            set(),
            False,
            None,
        )

    # Step 1b: Fetch source branch from origin to get latest changes
    if not fetch_branch(source_branch, dry_run=dry_run):
        return (
            False,
            f"Failed to fetch origin/{source_branch}. Cannot proceed with review on potentially stale code.",
            set(),
            False,
            None,
        )

    # Step 1c: Reset local branch to match origin
    if not reset_branch_to_origin(source_branch, dry_run=dry_run):
        return (
            False,
            f"Failed to reset branch to origin/{source_branch}. "
            "See the messages above for details and resolution steps.",
            set(),
            False,
            None,
        )

    # Step 2: Fetch latest from main
    had_rebase_conflicts = False
    push_succeeded: bool | None = None
    fetch_success = fetch_main(dry_run=dry_run)
    if not fetch_success:
        print("Warning: Could not fetch from origin/main, continuing without rebase...")
    else:
        # Step 3: Rebase onto main (continue even on conflicts)
        print("Rebasing onto origin/main...")
        rebase_result = rebase_onto_main(dry_run=dry_run)

        if rebase_result.is_success:
            print("Branch is synced with main.")
            # Step 3b: Auto-push if rebase rewrote history
            if rebase_result.was_rebased:
                push_succeeded = _try_force_push_after_rebase(dry_run)
        elif rebase_result.needs_manual_resolution:
            had_rebase_conflicts = True
            # Continue with review but warn about conflicts
            print(f"\n{'=' * 60}")
            print("⚠️  REBASE CONFLICTS DETECTED")
            print("=" * 60)
            print("The branch has conflicts with main that should be resolved.")
            print("However, the review can continue with the current branch state.")
            print("After the review, you may want to resolve conflicts separately.")
            print("=" * 60 + "\n")
        else:
            print(f"Warning: {rebase_result.message}")
            print("Continuing with review...")

    artifact_commit_hash_short: str | None = None
    if save_files_on_branch:
        artifact_commit_hash_short = get_value("review.commit_hash_short")

    if refresh_review_commit_scope and not dry_run and push_succeeded in (True, None):
        current_commit_hash = _get_current_commit_hash()
        if current_commit_hash:
            artifact_commit_hash_short = current_commit_hash[:12]
            set_value("review.commit_hash_short", artifact_commit_hash_short)

    # Step 4: Get files changed on this branch vs main
    print("\nIdentifying files changed on this branch...")
    diff_ref: str | None = None
    if save_files_on_branch:
        (
            files_on_branch,
            change_types_on_branch,
            rename_sources_on_branch,
            diff_ref,
            inventory_loaded,
        ) = get_branch_change_inventory()
        if not inventory_loaded:
            # Fall back to name-only listing if name-status parsing failed.
            # Keep the resolved diff_ref from inventory even on parse failure:
            # save_files_on_branch uses it to derive/persist diff_base_ref for
            # recovered-file metadata lookup.
            files_on_branch = get_files_changed_on_branch()
    else:
        files_on_branch = get_files_changed_on_branch()
        change_types_on_branch = {}
        rename_sources_on_branch = {}
    files_set = set(files_on_branch)
    print(f"Found {len(files_set)} file(s) changed on this branch.")

    # Optionally save files_on_branch to JSON for async workflows
    if save_files_on_branch and pull_request_id:
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
        temp_dir = get_state_dir()
        prompts_dir = temp_dir / "pull-request-review" / dir_name
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
        print(f"Saved files on branch to: {files_on_branch_path}")

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


def _detect_unchanged_files(
    pull_request_id: int,
    pr_details: dict[str, Any],
) -> set[str]:
    """Return files unchanged since the prior review commit."""
    from .review_helpers import normalize_repo_path
    from .review_state import load_review_state

    current_files: set[str] = set()
    for file_detail in pr_details.get("files", []):
        raw_path = file_detail.get("path", "")
        if not raw_path:
            continue
        normalized = normalize_repo_path(raw_path)
        if normalized:
            current_files.add(normalized)
    if not current_files:
        return set()

    try:
        prior_state = load_review_state(pull_request_id)
    except FileNotFoundError:
        return set()

    prior_commit_hash = prior_state.commitHash
    if not prior_commit_hash:
        return set()

    pr_info = pr_details.get("pullRequest", pr_details)
    last_merge = pr_info.get("lastMergeSourceCommit")
    if not isinstance(last_merge, dict):
        return set()
    current_commit_hash = last_merge.get("commitId")
    if not isinstance(current_commit_hash, str) or not current_commit_hash.strip():
        return set()
    current_commit_hash = current_commit_hash.strip()

    if prior_commit_hash == current_commit_hash:
        return current_files

    diff_proc = run_safe(
        ["git", "diff", "--name-only", f"{prior_commit_hash}..{current_commit_hash}"],
        capture_output=True,
        text=True,
        shell=False,
    )
    if diff_proc.returncode != 0:
        print(
            "Warning: Could not diff prior vs current commit for unchanged-file detection; "
            "treating all files as changed.",
            file=sys.stderr,
        )
        return set()

    changed_files: set[str] = set()
    for path in diff_proc.stdout.splitlines():
        if not path.strip():
            continue
        normalized = normalize_repo_path(path.strip())
        if normalized:
            changed_files.add(normalized)

    return {path for path in current_files if path not in changed_files}


def _normalize_path_for_comparison(path: str) -> str:
    """
    Normalize a file path for comparison.

    Strips leading slashes and normalizes to forward slashes.

    Args:
        path: File path to normalize

    Returns:
        Normalized path for comparison
    """
    if not path:
        return ""
    return path.strip().replace("\\", "/").lstrip("/").lower()


def _fetch_pull_request_basic_info(pull_request_id: int, config: AzureDevOpsConfig) -> dict[str, Any] | None:
    """
    Fetch basic pull request info using az CLI.

    Args:
        pull_request_id: PR ID to fetch
        config: Azure DevOps configuration

    Returns:
        PR data dict or None if failed
    """
    verify_az_cli()
    pat = get_pat()

    env = os.environ.copy()
    env["AZURE_DEVOPS_EXT_PAT"] = pat

    org_arg = (
        config.organization
        if config.organization.startswith("http")
        else f"https://dev.azure.com/{config.organization}"
    )

    result = run_safe(
        [
            "az",
            "repos",
            "pr",
            "show",
            "--id",
            str(pull_request_id),
            "--organization",
            org_arg,
            "--output",
            "json",
        ],
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def _fetch_and_display_jira_issue(issue_key: str) -> bool:
    """
    Fetch and display Jira issue details.

    Args:
        issue_key: Jira issue key

    Returns:
        True if successful, False otherwise
    """
    try:
        from ..jira.get_commands import get_issue
        from ..jira.state_helpers import set_jira_value

        # Set the issue key in state
        set_jira_value("issue_key", issue_key)

        # Call get_issue (this prints details and saves to temp file)
        get_issue()
        return True
    except SystemExit:
        # get_issue calls sys.exit(1) on failure - catch and continue
        print(
            f"Warning: Jira issue {issue_key} could not be fetched. Proceeding with PR review only.",
            file=sys.stderr,
        )
        return False
    except Exception as e:
        print(f"Warning: Failed to fetch Jira issue {issue_key}: {e}", file=sys.stderr)
        return False


def generate_review_prompts(
    pull_request_id: int,
    pr_details: dict | None = None,
    files_on_branch: set[str] | None = None,
    unchanged_files: set[str] | None = None,
) -> tuple[int, int, int, Path, list["SkippedFile"]]:
    """
    Generate file review prompts from PR details.

    This function creates the queue.json manifest and individual file prompts
    for the PR review workflow. All in-scope files are reviewed every run;
    unchanged files receive a simplified prompt when valid prior state exists.

    Args:
        pull_request_id: PR ID
        pr_details: Full PR details payload. If None, loads from temp file.
        files_on_branch: Set of file paths that are actually changed on the branch.
            If None and files-on-branch.json exists, loads from that file.
            If provided, files not in this set will be filtered out (they likely
            came from recently merged PRs). Conversely, any file present in this
            set but missing from ``pr_details["files"]`` (a PR-API/git diff
            discrepancy) is recovered: a synthetic file entry is added so it
            still gets a prompt file and a queue entry, and a warning is
            printed so the recovery is never silent.
        unchanged_files: Set of file paths that have no changes since the last
            review. If None, treated as empty set (all files considered changed).

    Returns:
        Tuple of (prompts_generated, skipped_reviewed_count, skipped_not_on_branch_count,
        prompts_directory, skipped_files)
    """
    from datetime import datetime

    from .review_helpers import (
        filter_threads,
        get_threads_for_file,
        normalize_repo_path,
    )
    from .review_state import (
        PROCESSING_PATH_INHERITED,
        SkippedFile,
        determine_processing_path,
        load_review_state,
    )

    if unchanged_files is None:
        unchanged_files = set()

    temp_dir = get_state_dir()
    details_path = temp_dir / "temp-get-pull-request-details-response.json"
    commit_hash_short = get_value("review.commit_hash_short")
    dir_name = resolve_review_artifact_dir_name(
        pull_request_id,
        commit_hash_short,
        allow_discovery=False,
    )
    prompts_dir = temp_dir / "pull-request-review" / dir_name
    prompts_dir.mkdir(parents=True, exist_ok=True)

    # Load pr_details from temp file if not provided
    if pr_details is None:
        if not details_path.exists():
            raise FileNotFoundError(f"PR details file not found: {details_path}. Run get_pull_request_details first.")
        with open(details_path, encoding="utf-8") as f:
            pr_details = json.load(f)

    # Load files_on_branch metadata from JSON when available.
    branch_file_change_types: dict[str, str] = {}
    branch_rename_sources: dict[str, str] = {}
    branch_diff_base_ref: str | None = None
    files_on_branch_path = prompts_dir / "files-on-branch.json"
    if files_on_branch_path.exists():
        with open(files_on_branch_path, encoding="utf-8") as f:
            files_data = json.load(f)
        if files_on_branch is None:
            files_on_branch = set(files_data.get("files", []))
            print(f"Loaded {len(files_on_branch)} files from files-on-branch.json")
        raw_change_types = files_data.get("change_types", {})
        if isinstance(raw_change_types, dict):
            for raw_path, raw_change_type in raw_change_types.items():
                if not isinstance(raw_path, str) or not isinstance(raw_change_type, str):
                    continue
                normalized_path = raw_path.replace("\\", "/").strip()
                if not normalized_path:
                    continue
                normalized_change_type = raw_change_type.strip().lower()
                if normalized_change_type in {"a", "add"}:
                    branch_file_change_types[normalized_path] = "add"
                elif normalized_change_type in {"d", "delete"}:
                    branch_file_change_types[normalized_path] = "delete"
                elif normalized_change_type.startswith("r"):
                    branch_file_change_types[normalized_path] = "rename"
                elif normalized_change_type in {"m", "edit", "modify"}:
                    branch_file_change_types[normalized_path] = "edit"
        raw_rename_sources = files_data.get("rename_sources", {})
        if isinstance(raw_rename_sources, dict):
            for raw_new_path, raw_old_path in raw_rename_sources.items():
                if not isinstance(raw_new_path, str) or not isinstance(raw_old_path, str):
                    continue
                normalized_new_path = raw_new_path.replace("\\", "/").strip()
                normalized_old_path = raw_old_path.replace("\\", "/").strip()
                if not normalized_new_path or not normalized_old_path:
                    continue
                branch_rename_sources[normalized_new_path] = normalized_old_path
        raw_diff_base_ref = files_data.get("diff_base_ref")
        if isinstance(raw_diff_base_ref, str) and raw_diff_base_ref.strip():
            branch_diff_base_ref = raw_diff_base_ref.strip()

    files_payload = pr_details.get("files", [])
    threads_payload = filter_threads(pr_details.get("threads", []))

    # Normalize files_on_branch for comparison
    normalized_branch_files: set[str] | None = None
    if files_on_branch is not None:
        normalized_branch_files = {_normalize_path_for_comparison(f) for f in files_on_branch}

        # Recover files that git reports as changed on the branch but that are
        # missing from the PR API's file listing. Previously such files were
        # silently dropped from queue.json with no indication anything was
        # skipped (see issue: PR file review queue silently drops files that
        # are present in files-on-branch.json). Append synthetic file entries
        # so they still get a prompt file and a queue entry.
        known_paths: set[str] = set()
        for file_detail in files_payload:
            raw_path = file_detail.get("path", "")
            if not isinstance(raw_path, str):
                print(
                    f"Warning: Skipping PR file record with non-string path: {raw_path!r}",
                    file=sys.stderr,
                )
                continue
            normalized_known_path = _normalize_path_for_comparison(raw_path)
            if normalized_known_path:
                known_paths.add(normalized_known_path)
        missing_normalized = sorted(normalized_branch_files - known_paths)
        if missing_normalized:
            branch_original_by_normalized = {_normalize_path_for_comparison(f): f for f in files_on_branch}
            branch_change_type_by_normalized = {
                _normalize_path_for_comparison(path): change_type
                for path, change_type in branch_file_change_types.items()
            }
            branch_rename_source_by_normalized = {
                _normalize_path_for_comparison(new_path): old_path
                for new_path, old_path in branch_rename_sources.items()
            }
            missing_paths = [branch_original_by_normalized[normalized] for normalized in missing_normalized]
            print(
                f"Warning: {len(missing_paths)} file(s) changed on the branch were missing from the PR "
                f"file listing; adding them to the review queue: {', '.join(missing_paths)}",
                file=sys.stderr,
            )
            if branch_diff_base_ref:
                base_ref = branch_diff_base_ref
            else:
                raw_comparison = pr_details.get("comparison")
                comparison_info = raw_comparison if isinstance(raw_comparison, dict) else {}
                base_branch_raw = comparison_info.get("baseBranch")
                base_branch = normalize_ref_name(base_branch_raw) if isinstance(base_branch_raw, str) else ""
                if not base_branch:
                    base_ref_raw = comparison_info.get("baseRef")
                    base_ref_hint = base_ref_raw if isinstance(base_ref_raw, str) else ""
                    if base_ref_hint.startswith("origin/"):
                        base_branch = base_ref_hint.removeprefix("origin/")
                    elif base_ref_hint.startswith("refs/heads/"):
                        base_branch = base_ref_hint.removeprefix("refs/heads/")
                base_branch = normalize_ref_name(base_branch or "")
                if not base_branch:
                    base_branch = "main"
                    print(
                        "Warning: Could not derive base branch from PR details "
                        "(baseBranch missing and baseRef not a branch ref); "
                        "falling back to origin/main for recovered-file metadata.",
                        file=sys.stderr,
                    )
                base_ref = f"origin/{base_branch}"
            # Always use HEAD as compare_ref for recovered files: files_on_branch
            # is produced from git diff against the current branch HEAD, so any
            # recovered file is definitionally reachable from HEAD.  The
            # compareRef captured in pr_details was snapshotted before branch
            # sync / rebase and may point to a commit that pre-dates the file,
            # causing the diff lookup to return empty metadata.
            compare_ref = "HEAD"
            for missing_path in missing_paths:
                normalized_missing_path = _normalize_path_for_comparison(missing_path)
                # Use the git-derived change type when available so that deleted
                # files are labelled "delete" (not "edit"), renamed files are
                # labelled "rename", and so on.  Falls back to "edit" when the
                # caller supplied files_on_branch directly without change-type
                # metadata (e.g. in unit tests).
                change_type = branch_change_type_by_normalized.get(normalized_missing_path, "edit")
                git_lookup_path = missing_path.replace("\\", "/").lstrip("/")
                original_path = None
                git_lookup_target: str | list[str] = git_lookup_path
                if change_type == "rename":
                    candidate_original_path = branch_rename_source_by_normalized.get(normalized_missing_path)
                    if candidate_original_path:
                        normalized_original_path = candidate_original_path.replace("\\", "/").lstrip("/")
                        if normalized_original_path:
                            original_path = candidate_original_path
                            if normalized_original_path != git_lookup_path:
                                git_lookup_target = [normalized_original_path, git_lookup_path]
                is_binary = False
                added_lines: list[dict[str, Any]] = []
                removed_lines: list[dict[str, Any]] = []
                patch = None
                try:
                    diff_info = get_diff_lines_info(base_ref, compare_ref, git_lookup_target)
                    is_binary = bool(diff_info.added.is_binary or diff_info.removed.is_binary)
                    added_lines = [
                        {"line": line.line_number, "content": line.content} for line in diff_info.added.lines
                    ]
                    removed_lines = [
                        {"line": line.line_number, "content": line.content} for line in diff_info.removed.lines
                    ]
                except Exception as exc:
                    print(
                        f"Warning: Could not load git diff metadata for recovered file '{missing_path}': {exc}",
                        file=sys.stderr,
                    )
                else:
                    if not is_binary:
                        try:
                            patch = get_diff_patch(base_ref, compare_ref, git_lookup_target)
                        except Exception as exc:
                            print(
                                f"Warning: Could not load git patch for recovered file '{missing_path}': {exc}",
                                file=sys.stderr,
                            )
                # Construct a complete synthetic file detail record so that
                # downstream consumers (manifest builder, prompt writer) receive
                # well-formed entries with all expected fields present, rather
                # than having to handle missing keys on code paths that were
                # not designed for partial dicts.
                file_record: dict[str, Any] = {
                    "path": missing_path,
                    "changeType": change_type,
                    "isBinary": is_binary,
                    "addedLineCount": len(added_lines),
                    "addedLines": added_lines,
                    "removedLineCount": len(removed_lines),
                    "removedLines": removed_lines,
                    "patch": patch,
                }
                # Preserve the rename source path so downstream consumers (e.g.
                # source_context.py) can fetch the pre-rename base-side content.
                # Without originalPath a recovered rename would query the
                # destination path at the base commit where it does not exist.
                if original_path:
                    file_record["originalPath"] = original_path
                files_payload.append(file_record)

    # Load prior review state for inheritance checks
    try:
        prior_state = load_review_state(pull_request_id)
    except FileNotFoundError:
        prior_state = None
    prior_commit_hash = prior_state.commitHash if prior_state else None

    # Normalize unchanged_files for comparison
    normalized_unchanged: set[str] = {f.lower() for f in unchanged_files}

    # Save snapshots
    files_snapshot_path = prompts_dir / "pull-request-files.json"
    with open(files_snapshot_path, "w", encoding="utf-8") as f:
        json.dump({"files": files_payload}, f, indent=2)

    threads_snapshot_path = prompts_dir / "pull-request-threads.json"
    with open(threads_snapshot_path, "w", encoding="utf-8") as f:
        json.dump({"threads": threads_payload}, f, indent=2)

    # Copy Jira issue if available
    state_dir = get_state_dir()
    jira_temp_path = state_dir / "temp-get-issue-details-response.json"
    jira_prompt_path = prompts_dir / "pull-request-jira-issue.json"
    if jira_temp_path.exists():  # pragma: no cover
        jira_prompt_path.write_text(jira_temp_path.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        jira_prompt_path.write_text("{}", encoding="utf-8")

    # Generate prompts for each file
    prompts_generated = 0
    skipped_not_on_branch_count = 0
    queue_entries = []
    skipped_files: list[SkippedFile] = []
    filtered_files_payload: list[dict[str, Any]] = []

    for file_detail in files_payload:
        raw_file_path = file_detail.get("path", "")
        file_path = raw_file_path if isinstance(raw_file_path, str) else ""
        normalized_path = normalize_repo_path(file_path) or ""

        # Skip files not actually on the branch (from recently merged PRs)
        if normalized_branch_files is not None:
            normalized_for_comparison = _normalize_path_for_comparison(file_path)
            if normalized_for_comparison not in normalized_branch_files:
                print(f"Skipping file not on branch (likely from merged PR): {file_path}")
                skipped_not_on_branch_count += 1
                skipped_files.append(SkippedFile(path=file_path, reason="not_on_branch"))
                continue

        # Determine processing path for the file
        is_unchanged = bool(normalized_path and normalized_path.lower() in normalized_unchanged)
        prior_entry = prior_state.files.get(normalized_path) if prior_state and normalized_path else None
        processing_path = determine_processing_path(prior_entry, is_unchanged, prior_commit_hash)

        # Route to appropriate prompt writer
        if processing_path == PROCESSING_PATH_INHERITED:
            prompt_path = _write_unchanged_file_prompt(prompts_dir, file_detail, prior_entry)
        else:
            threads_for_file = get_threads_for_file(threads_payload, file_path)
            prompt_path = _write_file_prompt(prompts_dir, file_detail, threads_for_file)

        prompts_generated += 1
        filtered_files_payload.append(file_detail)

        queue_entries.append(
            {
                "path": file_path,
                "normalizedPath": normalized_path,
                "promptFile": prompt_path.name,
                "promptPath": str(prompt_path),
                "status": "pending",
                "processingPath": processing_path,
            }
        )

    # Write queue manifest.
    #
    # NOTE: queue.json is no longer the source of PR-review *progress* counts —
    # those now derive from manifest.json + the answer ledger via
    # pr_review_progress.compute_review_progress. It is retained because the v2
    # setup pipeline still reads it for the manifest prompt-link map
    # (pr_review_manifest.load_queue_entries), to carry reviewDepth alongside the
    # manifest (pr_review_triage._apply_depth_to_queue), and to persist per-file
    # processingPath metadata into review-state.json
    # (_persist_processing_paths_to_review_state).
    queue_payload = {
        "pullRequestId": pull_request_id,
        "generatedUtc": datetime.now(UTC).isoformat(),
        "total": prompts_generated,
        "pending": queue_entries,
        "completed": [],
    }

    queue_path = prompts_dir / "queue.json"
    with open(queue_path, "w", encoding="utf-8") as f:
        json.dump(queue_payload, f, indent=2)

    # Keep pr_details in sync with the in-scope branch-filtered file list so
    # downstream consumers (e.g. manifest builder) generate rows only for files
    # that actually have prompt/queue entries.
    pr_details["files"] = filtered_files_payload
    if details_path.exists():
        temp_details_path = details_path.with_name(f"{details_path.name}.tmp")
        try:
            with open(temp_details_path, "w", encoding="utf-8") as f:
                json.dump(pr_details, f, indent=2)
            os.replace(temp_details_path, details_path)
        except OSError as exc:
            print(
                f"Warning: Could not persist filtered PR details artifact: {exc}",
                file=sys.stderr,
            )
            try:
                temp_details_path.unlink(missing_ok=True)
            except OSError as cleanup_exc:
                print(
                    f"Warning: Could not remove temporary PR details artifact: {cleanup_exc}",
                    file=sys.stderr,
                )

    return prompts_generated, 0, skipped_not_on_branch_count, prompts_dir, skipped_files


def generate_review_prompts_from_state() -> None:
    """Background-task entry point that generates prompts for current PR state."""
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

    unchanged_files = _detect_unchanged_files(pull_request_id, pr_details)
    _prompts_generated, _skipped_reviewed, _skipped_not_on_branch, prompts_dir, _skipped_files = (
        generate_review_prompts(
            pull_request_id,
            pr_details,
            unchanged_files=unchanged_files,
        )
    )
    _persist_processing_paths_to_review_state(pull_request_id, prompts_dir)


def _write_file_prompt(directory: Path, file_detail: dict, threads_for_file: list) -> Path:
    """Write a file review prompt to disk."""
    from .review_helpers import (
        build_full_file_content_section,
        convert_to_prompt_filename,
        resolve_repository_root,
    )

    filename = convert_to_prompt_filename(file_detail.get("path", ""))
    prompt_path = directory / filename

    file_json = json.dumps(file_detail, indent=2, ensure_ascii=False)
    threads_json = json.dumps(threads_for_file, indent=2, ensure_ascii=False) if threads_for_file else "[]"

    lines = [
        f"# File Review: {file_detail.get('path', 'unknown')}",
        "",
        "## File Diff Object",
        "",
        "```json",
        file_json,
        "```",
        "",
        "## Existing Threads",
        "",
        "```json",
        threads_json,
        "```",
    ]

    lines.extend(
        build_full_file_content_section(
            file_path=file_detail.get("path", ""),
            change_type=file_detail.get("changeType", "edit"),
            repo_root=resolve_repository_root(),
        )
    )

    prompt_path.write_text("\n".join(lines), encoding="utf-8")
    return prompt_path


def _write_unchanged_file_prompt(directory: Path, file_detail: dict, prior_entry: "FileEntry | None") -> Path:
    """Write a simplified file review prompt for an unchanged file.

    For files with no changes since the last review and a valid prior state,
    this produces a minimal prompt instructing the AI agent to only submit
    a review if their assessment differs from the prior review.

    Args:
        directory: Directory to write the prompt file.
        file_detail: File detail dictionary from the PR payload.
        prior_entry: The prior FileEntry with review state, or None.

    Returns:
        Path to the written prompt file.
    """
    from .review_helpers import convert_to_prompt_filename

    filename = convert_to_prompt_filename(file_detail.get("path", ""))
    prompt_path = directory / filename

    file_path = file_detail.get("path", "unknown")
    prior_status = prior_entry.status if prior_entry else "unknown"
    prior_summary = prior_entry.summary if prior_entry else None

    lines = [
        f"# File Review: {file_path}",
        "",
        "## Status",
        "",
        "no changes since last review",
        "",
        f"**Prior review status:** {prior_status}",
    ]

    if prior_summary:
        lines.extend(["", f"**Prior review summary:** {prior_summary}"])

    lines.extend(
        [
            "",
            "## Instructions",
            "",
            "This file has not changed since the last review. The prior review outcome is shown above.",
            "Still perform an independent review of this file, but **only submit** a review",
            "(via `agdt-file-review-write`) if your assessment **differs** from the prior review.",
            "If your assessment matches the prior review, skip submission — the file is already correctly reviewed.",
        ]
    )

    prompt_path.write_text("\n".join(lines), encoding="utf-8")
    return prompt_path


def print_review_instructions(
    pull_request_id: int,
    prompts_dir: Path,
    prompts_generated: int,
    skipped_not_on_branch_count: int = 0,
) -> None:
    """Print instructions for the AI agent to follow."""
    print("")
    print("=" * 60)
    print("PULL REQUEST REVIEW WORKFLOW")
    print("=" * 60)
    print("")
    print(f"PR ID: {pull_request_id}")
    print(f"Prompts generated: {prompts_generated}")
    if skipped_not_on_branch_count > 0:
        print(f"Skipped (not on branch, from merged PRs): {skipped_not_on_branch_count}")
    print(f"Prompts directory: {prompts_dir}")
    print("")
    print("=" * 60)
    print("SHARED CONTEXT FOR THIS REVIEW")
    print("=" * 60)
    print("")
    print("Review snapshots are saved in the prompts folder:")
    print("  • pull-request-files.json - All files in the PR diff")
    print("  • pull-request-threads.json - Existing comment threads")
    print("  • pull-request-jira-issue.json - Linked Jira issue details")
    print("")
    print("Keep analysis scoped to one file at a time; use shared artifacts for background context.")
    print("")
    print("=" * 60)
    print("CONSOLE CHECKLIST (for each file)")
    print("=" * 60)
    print("")
    print("1. Open the file prompt and analyze the diff + any existing threads.")
    print("2. Verify repository conventions/invariants for that file and capture concrete feedback.")
    print("3. Post the review with the appropriate command; let the queue advance automatically.")
    print("")
    print("=" * 60)
    print("NEXT STEP: FILE REVIEW DELEGATION")
    print("=" * 60)
    print("")
    print("The file review queue and per-file prompts are ready.")
    print("")
    print("Hand off to the PR review orchestrator to synthesize PR context,")
    print("triage review depth, and delegate each file to a file-reviewer subagent.")
    print("Each file-reviewer records its verdict with the atomic answer write:")
    print("")
    print("    agdt-file-review-write --file-key <fileKey> --answer-file <path-to-draft.json>")
    print("")
    print("=" * 60)
    print("IMPORTANT NOTES")
    print("=" * 60)
    print("")
    print("• After reviewing the final file, the overarching PR comments will be")
    print("  generated automatically. This may take up to 30 seconds.")
    print("• DO NOT RUN ANY COMMANDS after submitting the final file review!")
    print("  Wait for the process to complete.")
    print("• After all files are reviewed, provide a summary of your findings.")
    print("")

    if prompts_generated == 0:
        print("WARNING: No prompts were generated. All files may have been skipped (not on branch).")
    else:
        print("Ready to begin review. Process the queue starting with the first pending file.")


def _persist_processing_paths_to_review_state(pull_request_id: int, prompts_dir: Path) -> None:
    """Best-effort persistence of queue processingPath metadata into review-state.json."""
    queue_path = prompts_dir / "queue.json"
    if not queue_path.exists():
        return

    try:
        with open(queue_path, encoding="utf-8") as f:
            queue_payload = json.load(f)
    except (OSError, ValueError):
        return

    pending_entries = queue_payload.get("pending")
    if not isinstance(pending_entries, list) or not pending_entries:
        return

    from .review_helpers import normalize_repo_path

    processing_by_path: dict[str, str] = {}
    for entry in pending_entries:
        if not isinstance(entry, dict):
            continue
        processing_path = entry.get("processingPath")
        if not isinstance(processing_path, str) or not processing_path:
            continue
        normalized_path = entry.get("normalizedPath")
        if not isinstance(normalized_path, str) or not normalized_path:
            raw_path = entry.get("path")
            normalized_path = normalize_repo_path(raw_path) if isinstance(raw_path, str) else None
        if not normalized_path:
            continue
        processing_by_path[normalized_path] = processing_path

    if not processing_by_path:
        return

    try:
        from .review_state import FileLockError, read_modify_write_review_state

        with read_modify_write_review_state(pull_request_id) as state:
            for path, file_entry in state.files.items():
                file_entry.processingPath = processing_by_path.get(path)
    except (FileNotFoundError, FileLockError, OSError, ValueError) as exc:
        print(
            "Warning: Could not persist processing path metadata to review-state.json; "
            f"continuing without processing-path audit trail: {exc}",
            file=sys.stderr,
        )


def _scaffold_threads_for_review(
    pull_request_id: int,
    pr_details: dict[str, Any],
    pr_info: dict[str, Any],
    files_on_branch: set[str] | None,
    rebase_conflicts: bool = False,
) -> None:
    """Scaffold all review threads for a PR.

    Creates file and overall summary threads upfront. Idempotent:
    skips creation if review-state.json already exists. Errors are caught and
    printed as warnings to avoid breaking the overall review setup flow.

    Args:
        pull_request_id: PR ID.
        pr_details: Full PR details payload (from get_pull_request_details).
        pr_info: PR metadata dict (pullRequest sub-key or top-level).
        files_on_branch: Set of file paths on the source branch for filtering,
            or None to include all PR files.
        rebase_conflicts: True if rebase conflicts were detected during checkout.
    """
    from .review_scaffold import scaffold_review_threads

    try:
        repo_id = pr_info.get("repository", {}).get("id")
        if not repo_id:
            print("Warning: Could not determine repo ID for scaffolding; skipping.", file=sys.stderr)
            return

        file_paths: list = [f.get("path", "") for f in pr_details.get("files", []) if f.get("path")]

        if files_on_branch is not None:
            branch_normalized = {_normalize_path_for_comparison(f) for f in files_on_branch}
            file_paths = [fp for fp in file_paths if _normalize_path_for_comparison(fp) in branch_normalized]

        if not file_paths:
            print("No files to scaffold threads for; skipping.")
            return

        iterations = pr_details.get("iterations") or []
        latest_iteration_id = max((it.get("id", 0) for it in iterations), default=0)

        # Extract commit hash from PR info, guarding against JSON null → None or unexpected types
        last_merge = pr_info.get("lastMergeSourceCommit")
        commit_hash_raw = last_merge.get("commitId") if isinstance(last_merge, dict) else None
        if commit_hash_raw is not None and not isinstance(commit_hash_raw, str):
            print(
                f"Warning: lastMergeSourceCommit.commitId has unexpected type "
                f"{type(commit_hash_raw).__name__!r}; omitting from scaffolding.",
                file=sys.stderr,
            )
            commit_hash_raw = None
        commit_hash = commit_hash_raw

        # Resolve model_id from state (copilot.model_id); defaults to "unknown" if not set
        model_id = get_value("copilot.model_id") or "unknown"

        # Forced re-review overrides the same-commit + same-model skip.
        # Treat as a one-shot flag: clear from state immediately after reading so
        # subsequent resume/review calls do not accidentally re-force a re-review.
        force_rereview = parse_bool_from_state_value(get_value("review.force_rereview"))
        if force_rereview:
            delete_value("review.force_rereview")

        config = AzureDevOpsConfig.from_state()
        dry_run = is_dry_run()

        if dry_run:
            requests_module = None
            auth_headers: dict = {}
        else:
            requests_module = require_requests()
            auth_headers = get_auth_headers(get_pat())

        print(f"\nScaffolding review threads for PR {pull_request_id}...")
        scaffold_review_threads(
            pull_request_id=pull_request_id,
            files=file_paths,
            config=config,
            repo_id=repo_id,
            repo_name=config.repository,
            latest_iteration_id=latest_iteration_id,
            requests_module=requests_module,
            headers=auth_headers,
            dry_run=dry_run,
            commit_hash=commit_hash,
            model_id=model_id,
            rebase_conflicts=rebase_conflicts,
            force_rereview=force_rereview,
        )
    except Exception as e:
        print(f"Warning: Scaffolding failed: {e}", file=sys.stderr)


def setup_pull_request_review() -> None:
    """
    Set up a pull request review workflow (used by initiate_pull_request_review_workflow).

    This is a streamlined version of review_pull_request that assumes the PR ID
    is already resolved and set in state. It performs the following steps:
    1. Optionally fetch Jira issue details
    2. Fetch PR details via get_pull_request_details
    3. Checkout source branch and sync with main
    4. Generate review prompts and queue.json
    5. Scaffold review threads (file/overall summary threads)
    6. Print review instructions
    7. Initialize workflow state

    State keys:
        pull_request_id (required): PR ID
        jira.issue_key (optional): Jira issue key
        copilot.model_id (optional): AI model identifier for the reviewer

    This function runs setup synchronously so workflow state and prompt
    artifacts are finalized before any Copilot session is launched.
    Use setup_pull_request_review_async when background execution is required.
    """
    from ...state import delete_value, set_value
    from .pull_request_details_commands import get_pull_request_details

    # Read parameters from state
    pr_id_str = get_value("pull_request_id")
    if not pr_id_str:
        print("ERROR: pull_request_id is required in state.", file=sys.stderr)
        sys.exit(1)
    pull_request_id = int(pr_id_str)

    jira_issue_key = get_value("jira.issue_key")
    copilot_model_id = get_value("copilot.model_id")
    dry_run_val = get_value("dry_run")

    # Bootstrap identity + worktree_key before fetching PR details / generating
    # artifacts so they land in the identity-scoped directory from the start.
    # Note: get_value() calls above still resolve against the old state dir;
    # the bootstrap call below re-seeds those keys into the scoped state.
    try:
        import uuid

        from ...state import set_bootstrap_state

        # Normalize Jira issue key once and use consistently for scoping and state.
        if isinstance(jira_issue_key, str):
            jira_issue_key_norm = jira_issue_key.strip() or None
        else:
            jira_issue_key_norm = None

        # Ensure all subsequent uses in this function see the normalized value.
        jira_issue_key = jira_issue_key_norm

        worktree_key = jira_issue_key if jira_issue_key else f"PR{pull_request_id}"
        # FR-004: Skip bootstrap modification when AGENTIC_DEVTOOLS_STATE_DIR is set.
        # The env var already pins the state directory; modifying runtime-bootstrap.json
        # would be redundant and could cause a race condition for concurrent commands.
        if not os.environ.get("AGENTIC_DEVTOOLS_STATE_DIR", "").strip():
            set_bootstrap_state(worktree_key=worktree_key)
        else:
            # FR-004: AGENTIC_DEVTOOLS_STATE_DIR is set — skip bootstrap modification.
            # The env var already pins the state directory. Log for debugging.
            import logging

            logging.debug("FR-004: Skipping set_bootstrap_state() — AGENTIC_DEVTOOLS_STATE_DIR is set.")

        # Re-set context keys that were read from the old (_unscoped) state
        # directory.  set_bootstrap_state() may have changed the resolved
        # state dir, so downstream commands (e.g., get_pull_request_details)
        # that call get_value() would find an empty scoped state.json.
        # NOTE: When adding new state keys to this function, they MUST be
        # added to this re-persistence block as well.
        set_value("pull_request_id", str(pull_request_id))
        if jira_issue_key_norm:
            set_value("jira.issue_key", jira_issue_key_norm)
        if copilot_model_id:
            set_value("copilot.model_id", copilot_model_id)
        if dry_run_val is not None:
            set_value("dry_run", str(dry_run_val))

        # Generate agdt_run_id (same pattern as initiate_workflow in base.py)
        # so that persist_if_dirty() can commit workflow state to a -agdt branch.
        run_id = uuid.uuid4().hex[:12]
        set_value("agdt_run_id", run_id)

        # NOTE: versionControl.currentBranch is intentionally NOT set here.
        # This function checks out the PR source branch below (Step 3), so
        # the branch at this point is stale.  persist_if_dirty() resolves the
        # current branch from git when needed.
    except Exception as exc:
        # Bootstrap is best-effort: review proceeds using _unscoped if this
        # fails (e.g., not in a git repo).  Log the error for debugging.
        print(f"WARNING: bootstrap state init failed: {exc}", file=sys.stderr)

    # Step 1: Fetch Jira issue details if we have a key
    if jira_issue_key:
        print(f"\nFetching Jira issue details for {jira_issue_key}...")
        jira_fetch_success = _fetch_and_display_jira_issue(jira_issue_key)
        if not jira_fetch_success:
            set_value("review.jira_fetch_failed", "true")
            print(
                "Warning: Jira issue fetch failed. Review will proceed without acceptance criteria context.",
                file=sys.stderr,
            )
        else:
            delete_value("review.jira_fetch_failed")
    else:
        delete_value("review.jira_fetch_failed")

    # Step 2: Fetch PR details
    print(f"\nFetching pull request details for PR {pull_request_id}...")
    get_pull_request_details()

    # Load the PR details from the temp file
    temp_dir = get_state_dir()
    details_path = temp_dir / "temp-get-pull-request-details-response.json"

    if not details_path.exists():
        print("ERROR: PR details file not found after fetch.", file=sys.stderr)
        sys.exit(1)

    with open(details_path, encoding="utf-8") as f:
        pr_details = json.load(f)

    # Step 3: Checkout source branch and sync with main
    pr_info = pr_details.get("pullRequest", pr_details)

    # Extract and store commit hash short for artifact directory scoping.
    # This must be set before checkout_and_sync_branch() and generate_review_prompts()
    # so that both use the correct directory under pull-request-review/.
    # When commitId is absent, delete any stale value to keep artifact paths deterministic.
    last_merge = pr_info.get("lastMergeSourceCommit")
    if not isinstance(last_merge, dict):
        if last_merge is not None:
            print(
                f"Warning: lastMergeSourceCommit has unexpected type "
                f"{type(last_merge).__name__!r}; review artifacts will be scoped by PR ID.",
                file=sys.stderr,
            )
        source_commit_id = ""
    else:
        source_commit_id = last_merge.get("commitId", "")
        # Treat empty string as "absent", but warn and normalize any other non-string value.
        if not isinstance(source_commit_id, str):
            if source_commit_id != "":  # pragma: no branch
                print(
                    f"Warning: lastMergeSourceCommit.commitId has unexpected type "
                    f"{type(source_commit_id).__name__!r}; review artifacts will be scoped by PR ID.",
                    file=sys.stderr,
                )
            source_commit_id = ""
        else:
            # Normalize leading/trailing whitespace so the derived short hash matches
            # the canonical directory segment used for review artifacts.
            normalized_commit_id = source_commit_id.strip()
            if not normalized_commit_id:
                # If the commit ID was empty or only whitespace, treat it as absent.
                source_commit_id = ""
            else:
                source_commit_id = normalized_commit_id

    commit_hash_short = ""
    if source_commit_id:
        commit_hash_short = source_commit_id[:12]
        # Validate that commit_hash_short is safe to persist and use as a path segment.
        if not is_safe_dir_segment(commit_hash_short):
            print(
                "Warning: Derived commit_hash_short contains unexpected characters; "
                "review artifacts will be scoped by PR ID.",
                file=sys.stderr,
            )
            commit_hash_short = ""

    if commit_hash_short:
        set_value("review.commit_hash_short", commit_hash_short)
    else:
        delete_value("review.commit_hash_short")

    source_branch = pr_info.get("sourceRefName", "").replace("refs/heads/", "")

    files_on_branch: set[str] | None = None
    had_rebase_conflicts = False
    if source_branch:
        print(f"\nChecking out source branch '{source_branch}' and syncing with main...")
        (
            checkout_success,
            checkout_error,
            files_on_branch,
            had_rebase_conflicts,
            push_succeeded,
        ) = checkout_and_sync_branch(
            source_branch,
            pull_request_id,
            save_files_on_branch=True,
            dry_run=is_dry_run(),
            refresh_review_commit_scope=True,
        )

        # Finding 5: Persist rebase conflict status so downstream prompts can
        # include a disclaimer when reviewing files from a conflict-containing tree.
        if had_rebase_conflicts:
            set_value("review.rebase_conflicts_detected", "true")
        else:
            delete_value("review.rebase_conflicts_detected")

        if not checkout_success:
            print("", file=sys.stderr)
            print("=" * 60, file=sys.stderr)
            print("BRANCH CHECKOUT/SYNC ISSUE", file=sys.stderr)
            print("=" * 60, file=sys.stderr)
            print("", file=sys.stderr)
            print(f"Error: {checkout_error}", file=sys.stderr)
            print("", file=sys.stderr)
            print("Please resolve this issue and re-run the workflow.", file=sys.stderr)
            print("", file=sys.stderr)
            sys.exit(1)

        if not is_dry_run() and push_succeeded in (True, None):
            current_commit_hash = _get_current_commit_hash()
            if current_commit_hash and current_commit_hash != source_commit_id:
                commit_hash_short = current_commit_hash[:12]
                set_value("review.commit_hash_short", commit_hash_short)

                refreshed_pr_details = _refresh_pr_details_for_commit(details_path, current_commit_hash)
                if refreshed_pr_details is None:
                    print(
                        "Error: Could not load PR details for the post-sync HEAD commit. "
                        "Please re-run the workflow to refresh review data.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                pr_details = refreshed_pr_details
                pr_info = pr_details.get("pullRequest", pr_details)
            elif current_commit_hash is None and push_succeeded is True:
                print(
                    "Error: Could not determine the post-sync HEAD commit after "
                    "a rewritten branch was pushed. Artifact scope and API payload "
                    "may be inconsistent. Please re-run the workflow.",
                    file=sys.stderr,
                )
                sys.exit(1)
    else:
        print("Warning: Could not determine source branch from PR details", file=sys.stderr)

    # Step 4: Generate review prompts
    print("\nGenerating file review prompts...")
    unchanged_files = _detect_unchanged_files(pull_request_id, pr_details)
    prompts_generated, _, skipped_not_on_branch_count, prompts_dir, skipped_files = generate_review_prompts(
        pull_request_id,
        pr_details,
        files_on_branch,
        unchanged_files,
    )

    # Step 5: Scaffold review threads (all file/folder/overall summary threads upfront)
    _scaffold_threads_for_review(
        pull_request_id, pr_details, pr_info, files_on_branch, rebase_conflicts=had_rebase_conflicts
    )

    # Step 5b: Persist queue processing metadata into review state (informational — never abort setup)
    _persist_processing_paths_to_review_state(pull_request_id, prompts_dir)

    # Step 5c: Persist skipped files into review state (informational — never abort setup)
    if skipped_files:
        try:
            from .review_state import FileLockError, read_modify_write_review_state

            with read_modify_write_review_state(pull_request_id) as state:
                state.skippedFiles = skipped_files
        except (FileNotFoundError, FileLockError, OSError, ValueError) as exc:
            # FileNotFoundError — review-state.json not yet created
            # FileLockError — lock contention
            # OSError — permission or I/O issue
            # ValueError (incl. json.JSONDecodeError) — corrupt state file
            print(
                "Warning: Could not persist skipped files to review-state.json; "
                f"continuing without skipped-file audit trail: {exc}",
                file=sys.stderr,
            )

    # Step 5d: Generate additive v2 review artifacts (manifest + triage + answers).
    # Best-effort and self-contained — never alters the existing review loop.
    try:
        from .pr_review_artifacts import generate_v2_review_artifacts

        generate_v2_review_artifacts(pull_request_id, pr_details, prompts_dir)
    except Exception as exc:
        print(
            f"Warning: v2 review artifact generation failed (setup unaffected): {exc}",
            file=sys.stderr,
        )

    # Step 6: Print instructions
    print_review_instructions(pull_request_id, prompts_dir, prompts_generated, skipped_not_on_branch_count)

    # Step 7: Initialize workflow with PR context
    try:
        from ...prompts.loader import load_and_render_prompt
        from ...state import set_workflow_state

        pr_title = pr_info.get("title", "")
        pr_author = pr_info.get("createdBy", {}).get("displayName", "")
        target_branch = pr_info.get("targetRefName", "").replace("refs/heads/", "")
        file_count = prompts_generated

        config = AzureDevOpsConfig.from_state()
        pr_url = (
            f"{config.organization.rstrip('/')}/{config.project}/_git/{config.repository}/pullrequest/{pull_request_id}"
        )

        # Load repo-specific review focus areas (optional — None if not configured)
        from ...config import load_review_focus_areas

        # Determine repository root for loading .github/agdt-config.json
        try:
            git_root_result = run_safe(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=False,
                shell=False,
            )
            if git_root_result.returncode == 0 and git_root_result.stdout:
                repo_root = git_root_result.stdout.strip()
            else:
                repo_root = str(Path.cwd())
        except Exception:
            repo_root = str(Path.cwd())

        repo_review_focus_areas = load_review_focus_areas(repo_root)

        workflow_context = {
            "pull_request_id": pull_request_id,
            "jira_issue_key": jira_issue_key or "",
            "pr_title": pr_title,
            "pr_author": pr_author,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "file_count": file_count,
            "pr_url": pr_url,
            "source_code_platform": "AzureDevOps",
            "repo_review_focus_areas": repo_review_focus_areas or "",
        }

        set_workflow_state(
            name="pull-request-review",
            status="initiated",
            step="initiate",
            context=workflow_context,
        )

        print("\n" + "=" * 60)
        print("WORKFLOW INITIALIZED: pull-request-review")
        print("=" * 60)

        variables = {
            "pull_request_id": pull_request_id,
            "jira_issue_key": jira_issue_key or "",
            "pr_title": pr_title,
            "pr_author": pr_author,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "file_count": file_count,
            "repo_review_focus_areas": repo_review_focus_areas or "",
            "pr_url": pr_url,
            "source_code_platform": "AzureDevOps",
        }

        load_and_render_prompt(
            workflow_name="pull-request-review",
            step_name="initiate",
            variables=variables,
            save_to_temp=True,
            log_output=True,
        )

    except ImportError as e:  # pragma: no cover
        # Defensive fallback for stripped/broken installs where workflow modules
        # are unavailable at runtime.
        print(f"ERROR: Could not initialize workflow: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Could not initialize workflow: {e}", file=sys.stderr)
        sys.exit(1)
