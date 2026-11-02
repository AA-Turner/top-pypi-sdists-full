"""Pull-request review setup orchestration."""

import os
import sys
from pathlib import Path

from ...state import get_value, is_dry_run, is_safe_dir_segment
from ..subprocess_utils import run_safe
from .config import AzureDevOpsConfig
from .review_branch_sync import _get_current_commit_hash, _refresh_pr_details_for_commit, checkout_and_sync_branch
from .review_issue_lookup import _fetch_and_display_jira_issue
from .review_prompt_formatting import print_review_instructions
from .review_prompt_generation import generate_review_prompts
from .review_prompt_tracking import _detect_unchanged_files, _persist_processing_paths_to_review_state
from .review_setup_threads import _scaffold_threads_for_review


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
    from ..pull_request_details import get_pull_request_details
    from ..workflows.base import _safe_print

    # Read parameters from state
    pr_id_str = get_value("pull_request_id")
    if not pr_id_str:
        _safe_print("ERROR: pull_request_id is required in state.", file=sys.stderr)
        sys.exit(1)
    pull_request_id = int(pr_id_str)

    jira_issue_key = get_value("jira.issue_key")
    copilot_model_id = get_value("copilot.model_id")
    dry_run_val = get_value("dry_run")
    code_hosting_provider = get_value("platform.code_hosting") or get_value("provider") or get_value("github.provider")
    github_repository = get_value("github.repo")
    azure_repository = get_value("azure_devops.repository")
    generic_repository = get_value("repository")
    canonical_repository = get_value("sourceCodeHostingPlatform.pullRequest.repository")

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
        if isinstance(code_hosting_provider, str) and code_hosting_provider.strip():
            set_value("provider", code_hosting_provider)
            set_value("platform.code_hosting", code_hosting_provider)
        if isinstance(github_repository, str) and github_repository.strip():
            set_value("github.repo", github_repository)
        if isinstance(azure_repository, str) and azure_repository.strip():
            set_value("azure_devops.repository", azure_repository)
        if isinstance(generic_repository, str) and generic_repository.strip():
            set_value("repository", generic_repository)
        if isinstance(canonical_repository, str) and canonical_repository.strip():
            set_value("sourceCodeHostingPlatform.pullRequest.repository", canonical_repository)
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
        _safe_print(f"WARNING: bootstrap state init failed: {exc}", file=sys.stderr)

    # Step 1: Fetch Jira issue details if we have a key
    if jira_issue_key:
        _safe_print(f"\nFetching Jira issue details for {jira_issue_key}...")
        jira_fetch_success = _fetch_and_display_jira_issue(jira_issue_key)
        if not jira_fetch_success:
            set_value("review.jira_fetch_failed", "true")
            _safe_print(
                "Warning: Jira issue fetch failed. Review will proceed without acceptance criteria context.",
                file=sys.stderr,
            )
        else:
            delete_value("review.jira_fetch_failed")
    else:
        delete_value("review.jira_fetch_failed")

    # Step 2: Fetch PR details
    _safe_print(f"\nFetching pull request details for PR {pull_request_id}...")
    pr_details = get_pull_request_details(provider=code_hosting_provider or "azure_devops")
    if not isinstance(pr_details, dict):
        _safe_print("ERROR: PR details fetch did not return a valid payload.", file=sys.stderr)
        sys.exit(1)

    # Step 3: Checkout source branch and sync with main
    pr_info = pr_details.get("pullRequest", pr_details)
    resolved_provider = pr_details.get("provider") or code_hosting_provider or get_value("platform.code_hosting")
    is_github_provider = isinstance(resolved_provider, str) and resolved_provider.strip().lower() == "github"

    # Extract and store commit hash short for artifact directory scoping.
    # This must be set before checkout_and_sync_branch() and generate_review_prompts()
    # so that both use the correct directory under pull-request-review/.
    # When commitId is absent, delete any stale value to keep artifact paths deterministic.
    last_merge = pr_info.get("lastMergeSourceCommit")
    if not isinstance(last_merge, dict):
        if last_merge is not None:
            _safe_print(
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
                _safe_print(
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
            _safe_print(
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
        _safe_print(f"\nChecking out source branch '{source_branch}' and syncing with main...")
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
            _safe_print("", file=sys.stderr)
            _safe_print("=" * 60, file=sys.stderr)
            _safe_print("BRANCH CHECKOUT/SYNC ISSUE", file=sys.stderr)
            _safe_print("=" * 60, file=sys.stderr)
            _safe_print("", file=sys.stderr)
            _safe_print(f"Error: {checkout_error}", file=sys.stderr)
            _safe_print("", file=sys.stderr)
            _safe_print("Please resolve this issue and re-run the workflow.", file=sys.stderr)
            _safe_print("", file=sys.stderr)
            sys.exit(1)

        if not is_dry_run() and push_succeeded in (True, None):
            current_commit_hash = _get_current_commit_hash(run_command=run_safe)
            if current_commit_hash and current_commit_hash != source_commit_id:
                commit_hash_short = current_commit_hash[:12]
                set_value("review.commit_hash_short", commit_hash_short)

                refreshed_pr_details = _refresh_pr_details_for_commit(current_commit_hash)
                if refreshed_pr_details is None:
                    _safe_print(
                        "Error: Could not load PR details for the post-sync HEAD commit. "
                        "Please re-run the workflow to refresh review data.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                pr_details = refreshed_pr_details
                pr_info = pr_details.get("pullRequest", pr_details)
            elif current_commit_hash is None and push_succeeded is True:
                _safe_print(
                    "Error: Could not determine the post-sync HEAD commit after "
                    "a rewritten branch was pushed. Artifact scope and API payload "
                    "may be inconsistent. Please re-run the workflow.",
                    file=sys.stderr,
                )
                sys.exit(1)
    else:
        _safe_print("Warning: Could not determine source branch from PR details", file=sys.stderr)

    # Step 4: Generate review prompts
    _safe_print("\nGenerating file review prompts...")
    unchanged_files = _detect_unchanged_files(pull_request_id, pr_details)
    prompts_generated, _, skipped_not_on_branch_count, prompts_dir, skipped_files = generate_review_prompts(
        pull_request_id,
        pr_details,
        files_on_branch,
        unchanged_files,
    )

    # The existing thread scaffolder writes through the Azure DevOps REST API.
    if is_github_provider:
        _safe_print("Skipping Azure DevOps review-thread scaffolding for GitHub pull requests.")
    else:
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
            _safe_print(
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
        _safe_print(
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

        if is_github_provider:
            raw_repository = pr_details.get("repository")
            repository = raw_repository.get("id") if isinstance(raw_repository, dict) else None
            from ...adapters.base import is_valid_github_repository

            if not isinstance(repository, str) or not is_valid_github_repository(repository):
                raise ValueError("GitHub pull-request details must include a normalized owner/repository value")
            pr_url = f"https://github.com/{repository}/pull/{pull_request_id}"
            source_code_platform = "GitHub"
        else:
            config = AzureDevOpsConfig.from_state()
            pr_url = (
                f"{config.organization.rstrip('/')}/{config.project}/_git/"
                f"{config.repository}/pullrequest/{pull_request_id}"
            )
            source_code_platform = "AzureDevOps"

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

        artifact_dir_name = prompts_dir.name
        if not isinstance(artifact_dir_name, str) or not artifact_dir_name:
            artifact_dir_name = ""
        artifact_dir = (Path("pull-request-review") / artifact_dir_name).as_posix()

        workflow_context = {
            "pull_request_id": pull_request_id,
            "jira_issue_key": jira_issue_key or "",
            "pr_title": pr_title,
            "pr_author": pr_author,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "file_count": file_count,
            "pr_url": pr_url,
            "source_code_platform": source_code_platform,
            "repo_review_focus_areas": repo_review_focus_areas or "",
            "review_artifact_dir_name": artifact_dir_name,
            "review_artifact_dir": artifact_dir,
        }

        set_workflow_state(
            name="pull-request-review",
            status="initiated",
            step="initiate",
            context=workflow_context,
        )

        _safe_print("\n" + "=" * 60)
        _safe_print("WORKFLOW INITIALIZED: pull-request-review")
        _safe_print("=" * 60)

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
            "source_code_platform": source_code_platform,
            "review_artifact_dir_name": artifact_dir_name,
            "review_artifact_dir": artifact_dir,
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
        _safe_print(f"ERROR: Could not initialize workflow: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        _safe_print(f"ERROR: Could not initialize workflow: {e}", file=sys.stderr)
        sys.exit(1)
