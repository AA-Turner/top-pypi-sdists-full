"""Scaffold Azure DevOps review threads during review setup."""

import sys
from typing import Any

from ...state import delete_value, get_value, is_dry_run
from .auth import get_auth_headers, get_pat
from .config import AzureDevOpsConfig
from .helpers import parse_bool_from_state_value, require_requests
from .review_prompt_tracking import _normalize_path_for_comparison


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
    from ..workflows.base import _safe_print
    from .review_scaffold_orchestration import scaffold_review_threads

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
        _safe_print(f"Warning: Scaffolding failed: {e}", file=sys.stderr)
