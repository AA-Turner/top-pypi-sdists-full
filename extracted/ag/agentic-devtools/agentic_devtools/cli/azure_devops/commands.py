"""Azure DevOps CLI commands.

These are action commands that read state from the JSON file and execute.
They are parameterless for easy auto-approval.
"""

import dataclasses
import os
import re
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC
from typing import Any, Literal
from urllib.parse import unquote

from ...adapters.pull_request_approval import _sanitize_diagnostic
from ...state import (
    delete_value,
    get_pull_request_id,
    get_thread_id,
    get_value,
    is_dry_run,
    set_value,
    should_resolve_thread,
)
from ..subprocess_utils import run_safe
from .auth import get_auth_headers, get_pat
from .config import AzureDevOpsConfig
from .helpers import (
    PrCommentResolveFailedError,
    build_approval_idempotency_key,
    build_thread_context,
    convert_to_pull_request_title,
    get_repository_id,
    parse_bool_from_state_value,
    parse_json_response,
    patch_comment,
    post_pr_comment,
    print_threads,
    require_requests,
    resolve_thread_by_id,
    verify_az_cli,
)
from .marker import build_marker
from .pull_request_details_commands import (
    _get_pull_request_iterations,
    get_change_tracking_id_for_file,
)
from .review_state import (
    OverallSummary,
    ReviewState,
    load_review_state,
    save_review_state,
    sync_review_state_from_threads,
)
from .review_templates import render_overall_summary


class PullRequestCreationPostSubmitError(RuntimeError):
    """The Azure CLI accepted PR creation but a post-submit operation failed."""


def _extract_issue_key_from_branch(branch_name: str) -> str | None:
    """
    Extract a Jira issue key from a branch name.

    Searches for patterns like "PROJECT-1234" in the branch name.
    Returns the first match found (case-insensitive, returned in uppercase).

    Args:
        branch_name: The branch name to search (e.g., "feature/PROJECT-1234/my-feature")

    Returns:
        The extracted issue key (e.g., "PROJECT-1234") or None if not found.
    """
    # Match Jira issue key pattern: PROJECT-NUMBER
    # Common patterns: PROJECT-1234, ABC-12, PROJECT-99999
    match = re.search(r"([A-Z]{2,10}-\d+)", branch_name, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return None  # pragma: no cover


def parse_bool_from_state(key: str, default: bool = False) -> bool:
    """
    Parse a boolean value from state, handling various string representations.

    Args:
        key: The state key to read.
        default: Default value if key is not set.

    Returns:
        Boolean value parsed from state.
    """
    raw_value = get_value(key)
    return parse_bool_from_state_value(raw_value, default)


def require_content() -> str:
    """Get content from state, exiting if not available."""
    content = get_value("content")
    if not content:
        print(
            'Error: No content found. Use: agdt-set content "your message"',
            file=sys.stderr,
        )
        sys.exit(1)
    return content


def reply_to_pull_request_thread() -> None:
    """
    Reply to an existing pull request comment thread.

    Reads from state:
    - pull_request_id (required): Pull request ID
    - thread_id (required): Thread ID to reply to
    - content (required): Reply content (supports multiline)
    - resolve_thread (optional): Whether to resolve after replying
    - dry_run (optional): Preview without making API calls

    Usage:
        agdt-set pull_request_id 23046
        agdt-set thread_id 139474
        agdt-set content "Thanks for the feedback!

        I've made the changes you suggested."
        agdt-reply-to-pull-request-thread
    """
    requests = require_requests()

    # Get required values from state
    pull_request_id = get_pull_request_id(required=True)
    thread_id = get_thread_id(required=True)
    content = require_content()

    resolve_thread_flag = should_resolve_thread()
    dry_run = is_dry_run()
    config = AzureDevOpsConfig.from_state()

    if dry_run:
        print(f"[DRY RUN] Would reply to thread {thread_id} on PR {pull_request_id}")
        print(f"Content:\n{content}")
        if resolve_thread_flag:
            print("[DRY RUN] Would also resolve the thread")
        return

    # Get auth and repo info
    pat = get_pat()
    headers = get_auth_headers(pat)

    print(f"Resolving repository ID for '{config.repository}'...")
    repo_id = get_repository_id(config.organization, config.project, config.repository)

    # Add comment to thread
    comment_url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "threads", thread_id, "comments")

    comment_body = {
        "content": content,
        "commentType": "text",
    }

    print(f"Adding reply to thread {thread_id} on PR {pull_request_id}...")
    response = requests.post(comment_url, headers=headers, json=comment_body, timeout=30)
    response.raise_for_status()

    result = response.json()
    print(f"Reply added successfully (comment ID: {result.get('id')})")

    # Optionally resolve thread
    if resolve_thread_flag:
        print(f"Resolving thread {thread_id}...")
        resolve_thread_by_id(
            requests,
            headers,
            config,
            repo_id,
            pull_request_id,
            thread_id,
            status="fixed",
        )
        print(f"Thread {thread_id} resolved")


def update_review_narrative(
    pull_request_id: int,
    content: str,
    config: AzureDevOpsConfig | None = None,
) -> None:
    """Update the Review Narrative in the existing overall PR summary comment in-place.

    Loads the review state for ``pull_request_id``, sets ``narrativeSummary`` to
    ``content``, re-renders the overall summary, and PATCHes the existing summary
    comment. Saves the updated state on success. When ``config`` is explicitly
    provided, the repository ID is always resolved from it (never from the stored
    review state's ``repoId``), so an explicit ``--repo`` override cannot be
    silently ignored in favor of a stale stored repository. When ``config`` is
    omitted, the stored ``repoId`` is preferred and global state is only
    consulted as a fallback.

    Raises:
        ReviewStateNotFoundError: When review-state.json does not exist for the PR.
        Exception: For any API or state I/O failure (caller should handle).
    """
    from .helpers import build_pr_base_url

    requests = require_requests()
    config_explicitly_provided = config is not None
    config = config or AzureDevOpsConfig.from_state()
    pat = get_pat()
    headers = get_auth_headers(pat)

    try:
        review_state = load_review_state(
            pull_request_id,
            delete_on_pr_mismatch=not config_explicitly_provided,
        )
    except FileNotFoundError as exc:
        raise ReviewStateNotFoundError(str(exc)) from exc
    if review_state.overallSummary.threadId <= 0 or review_state.overallSummary.commentId <= 0:
        raise ValueError("Review state has no existing overall summary comment to update")
    if config_explicitly_provided:
        stored_repository = (
            unquote(getattr(review_state, "organization", "")).rstrip("/").casefold(),
            unquote(getattr(review_state, "project", "")).casefold(),
            unquote(getattr(review_state, "repoName", "")).casefold(),
        )
        requested_repository = (
            unquote(config.organization).rstrip("/").casefold(),
            unquote(config.project).casefold(),
            unquote(config.repository).casefold(),
        )
        if stored_repository != requested_repository:
            raise ReviewStateRepositoryMismatchError(
                "Explicit Azure DevOps repository does not match the repository in review state "
                f"(stored={stored_repository!r}, requested={requested_repository!r})"
            )

    repo_id = None if config_explicitly_provided else getattr(review_state, "repoId", None)
    if repo_id:
        print(f"Using repository ID from review state: {repo_id}")
    else:
        print(f"Resolving repository ID for '{config.repository}'...")
        repo_id = get_repository_id(config.organization, config.project, config.repository)

    review_state.overallSummary.narrativeSummary = content
    base_url = build_pr_base_url(config, pull_request_id)
    summary_marker = build_marker("overall-summary", pr=pull_request_id)
    new_content = f"{summary_marker}\n{render_overall_summary(review_state, base_url)}"

    thread_id = review_state.overallSummary.threadId
    comment_id = review_state.overallSummary.commentId
    print(f"Updating overall PR summary comment (thread {thread_id}, comment {comment_id})...")
    patch_comment(
        requests,
        headers,
        config,
        repo_id,
        pull_request_id,
        thread_id,
        comment_id,
        new_content,
        reply_on_forbidden=True,
    )
    save_review_state(review_state)
    print("Review Narrative updated successfully.")


def _escape_for_cmd(value: str) -> str:
    """Escape cmd.exe metacharacters for safe use in Windows arguments.

    Note: create_pull_request executes `az` via `shell=True` on Windows, and passes
    args as a list. Avoid embedding literal quote characters into individual args;
    instead use cmd-native escaping (caret) plus percent doubling.
    """
    if sys.platform != "win32":
        return value

    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    single_line = " ".join(part for part in normalized.split("\n") if part)

    escaped = single_line.replace("^", "^^").replace("%", "%%")
    for ch in ("&", "|", "<", ">"):
        escaped = escaped.replace(ch, f"^{ch}")
    escaped = escaped.replace('"', '^"')
    return escaped


def add_pull_request_comment() -> None:
    """
    Add a new comment to a pull request.

    Reads from state:
    - pull_request_id (required): Pull request ID
    - content (required): Comment content (supports multiline)
    - path (optional): File path for file-level comment
    - line (optional): Line number for line-level comment
    - end_line (optional): End line for multi-line comment
    - leave_thread_active (optional): Whether to keep thread active (default: resolve after posting)
    - dry_run (optional): Preview without making API calls

    Usage:
        agdt-set pull_request_id 23046
        agdt-set content "Great work on this PR!"
        agdt-add-pull-request-comment

        # For file-level comment
        agdt-set path "src/main.py"
        agdt-set line 42
        agdt-add-pull-request-comment
    """
    requests = require_requests()

    pull_request_id = get_pull_request_id(required=True)
    content = require_content()

    dry_run = is_dry_run()
    leave_thread_active = parse_bool_from_state("leave_thread_active", default=False)

    # Optional file context
    path = get_value("path")
    line = get_value("line")
    end_line = get_value("end_line")

    config = AzureDevOpsConfig.from_state()

    if dry_run:
        print(f"[DRY RUN] Would add comment to PR {pull_request_id}")
        if path:
            line_info = f", Line: {line}" if line else ""
            end_line_info = f"-{end_line}" if end_line else ""
            print(f"[DRY RUN] File: {path}{line_info}{end_line_info}")
        if not leave_thread_active:
            print("[DRY RUN] Would also resolve the thread after posting")
        print(f"Content:\n{content}")
        return

    pat = get_pat()
    headers = get_auth_headers(pat)

    print(f"Resolving repository ID for '{config.repository}'...")
    repo_id = get_repository_id(config.organization, config.project, config.repository)

    # Build thread context for file-level comments
    thread_context = build_thread_context(path, line, end_line)

    # Get latest iteration ID and changeTrackingId for file-level comments
    # to avoid "file no longer exists" issue
    latest_iteration_id = None
    change_tracking_id = None
    if thread_context and path:
        iterations = _get_pull_request_iterations(
            config.organization, config.project, repo_id, pull_request_id, headers
        )
        if iterations:  # pragma: no cover
            latest_iteration_id = max(it.get("id", 0) for it in iterations)
            if latest_iteration_id:
                print(f"Using iteration {latest_iteration_id} for file context")
                # Get the changeTrackingId for this specific file
                change_tracking_id = get_change_tracking_id_for_file(
                    config.organization,
                    config.project,
                    repo_id,
                    pull_request_id,
                    latest_iteration_id,
                    path,
                    headers,
                )
                if change_tracking_id:
                    print(f"Found changeTrackingId {change_tracking_id} for file '{path}'")
                else:
                    print(f"Warning: Could not find changeTrackingId for '{path}'")

    # Create thread with comment
    thread_url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "threads")

    thread_body: dict[str, Any] = {
        "comments": [
            {
                "content": content,
                "commentType": "text",
            }
        ],
        "status": "active",
    }

    if thread_context:
        thread_body["threadContext"] = thread_context
        # Add iteration context so comments are anchored to correct iteration
        if latest_iteration_id and change_tracking_id:  # pragma: no cover
            thread_body["pullRequestThreadContext"] = {
                "iterationContext": {
                    "firstComparingIteration": 1,
                    "secondComparingIteration": latest_iteration_id,
                },
                "changeTrackingId": change_tracking_id,
            }

    print(f"Adding comment to PR {pull_request_id}...")
    response = requests.post(thread_url, headers=headers, json=thread_body, timeout=30)
    response.raise_for_status()

    result = response.json()
    thread_id = result.get("id")
    print(f"Comment added successfully (thread ID: {thread_id})")

    # Optionally resolve thread (default behavior unless leave_thread_active is True)
    if not leave_thread_active and thread_id:
        print(f"Resolving thread {thread_id}...")
        resolve_thread_by_id(
            requests,
            headers,
            config,
            repo_id,
            pull_request_id,
            thread_id,
            status="closed",
        )
        print(f"Thread {thread_id} resolved")


def create_pull_request(
    *,
    timeout: float | None = None,
    source_branch: str | None = None,
    title: str | None = None,
    title_is_rendered: bool = False,
    description: str | None = None,
    target_branch: str | None = None,
    draft: bool | None = None,
    reviewers: str | None = None,
    dry_run: bool | None = None,
    on_pull_request_created: Callable[[int], None] | None = None,
) -> str | None:
    """
    Create a pull request from the current branch.

    Reads from state:
    - source_branch (required): Source branch name
    - title (required): PR title (Markdown links will be stripped)
    - target_branch (optional): Target branch, defaults to 'main'
    - draft (optional): Whether to create as draft, defaults to True
    - reviewers (optional): Comma-separated list of reviewer emails or IDs
    - description (optional): Overrides the resolved PR body when set
    - dry_run (optional): Preview without making API calls

    Args:
        timeout: Optional per-subprocess bound (in seconds) applied separately
            to each Azure CLI call: the two verification probes and the
            ``az repos pr create`` call. A request may therefore take up to
            roughly three timeout periods, excluding other overhead. ``None``
            (the default, used by the parameterless CLI entry point) waits
            indefinitely, matching prior behavior. Callers that hold a lock
            across this call (e.g. the provider-neutral adapter bridge) should
            account for the combined wait when choosing a bounded value.
        source_branch: Optional source branch override; otherwise read from state.
        title: Optional title override. When provided, it replaces the
            ``title`` state value.
        title_is_rendered: Whether ``title`` is already rendered and should
            bypass PR-title template resolution.
        description: Optional description override; otherwise resolve from state
            or the shared PR body template.
        target_branch: Optional target branch override; otherwise read from state.
        draft: Optional draft-mode override; otherwise read from state.
        reviewers: Optional comma-separated reviewer override; otherwise read from
            state.
        dry_run: Optional dry-run override; otherwise read from state.
        on_pull_request_created: Optional callback that receives the created
            PR ID instead of persisting it immediately. Callers can use this
            to defer state migration until request processing finishes.

    The PR title is resolved from the explicit ``title`` override when supplied;
    otherwise ``.agdt/config/pr-title-template.j2`` is used if it exists and
    renders successfully, with a fallback to stripping Markdown links from the
    ``title`` state key.

    The PR description defaults to the shared PR body template
    (``resolve_pr_body()``): if ``.agdt/config/pull-request-template.j2``
    exists it is used as the template, otherwise the raw commit message is
    used as the body. Setting the ``description`` state key overrides this
    resolution entirely and is used verbatim instead.

    Usage:
        agdt-set source_branch "feature/PROJECT-1234/my-feature"
        agdt-set title "feature([PROJECT-1234](https://jira.swica.ch/browse/PROJECT-1234)): add feature"
        agdt-create-pull-request
    """
    if timeout is not None and timeout < 0:
        raise ValueError("timeout must be non-negative")

    # Get required values from state
    source_branch = source_branch if source_branch is not None else get_value("source_branch")
    if not source_branch:
        print(
            'Error: No source_branch found. Use: agdt-set source_branch "branch-name"',
            file=sys.stderr,
        )
        sys.exit(1)

    title_override_supplied = title is not None
    title = title if title_override_supplied else get_value("title")
    if not title:
        print('Error: No title found. Use: agdt-set title "PR title"', file=sys.stderr)
        sys.exit(1)

    # Resolve PR title: try template first, fall back to link-stripping
    from ..pr_template import resolve_pr_title

    if not title_is_rendered:
        rendered_title = resolve_pr_title(title) if title_override_supplied else resolve_pr_title()
        title = rendered_title if rendered_title else convert_to_pull_request_title(title)

    # Get optional values
    from ..pr_template import resolve_pr_body

    description_override = description if description is not None else get_value("description")
    if description_override is None:
        description = resolve_pr_body()
    elif isinstance(description_override, str):
        description = description_override
    else:
        print("Error: description must be a string", file=sys.stderr)
        sys.exit(1)
    target_branch_value = target_branch if target_branch is not None else get_value("target_branch")
    if target_branch_value is None or target_branch_value == "":
        target_branch = "main"
    elif isinstance(target_branch_value, str):
        target_branch = target_branch_value
    else:
        print("Error: target_branch must be a string", file=sys.stderr)
        sys.exit(1)

    # Draft mode defaults to True (opt-out via draft=false)
    # If draft is explicitly set to false/0/no, then draft=False; otherwise draft=True
    draft_raw = draft if draft is not None else get_value("draft")
    if draft_raw is None:
        draft = True
    elif isinstance(draft_raw, bool):
        draft = draft_raw
    else:
        draft = str(draft_raw).lower() not in ("0", "false", "no")

    reviewers_raw = reviewers if reviewers is not None else get_value("reviewers")
    if reviewers_raw is None:
        parsed_reviewers: list[str] = []
    elif isinstance(reviewers_raw, str):
        parsed_reviewers = [item.strip() for item in reviewers_raw.split(",") if item.strip()]
    else:
        print("Error: reviewers must be a comma-separated string", file=sys.stderr)
        sys.exit(1)

    dry_run = is_dry_run() if dry_run is None else dry_run
    config = AzureDevOpsConfig.from_state()

    if dry_run:
        print("[DRY RUN] Would create PR:")
        print(f"  Source Branch: {source_branch}")
        print(f"  Target Branch: {target_branch}")
        print(f"  Title: {title}")
        print(f"  Draft Mode: {draft}")
        if description:
            print(f"  Description: {description}")
        if parsed_reviewers:
            print(f"  Reviewers: {', '.join(parsed_reviewers)}")
        print(f"  Org/Project: {config.organization} / {config.project}")
        print(f"  Repository: {config.repository}")
        return None

    # Verify Azure CLI is available
    try:
        verify_az_cli(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Azure CLI verification timed out before pull-request creation") from exc

    # Set PAT for az CLI
    pat = get_pat()
    env = os.environ.copy()
    env["AZURE_DEVOPS_EXT_PAT"] = pat

    print(f"Creating pull request for '{source_branch}' -> '{target_branch}'...")

    safe_source_branch = _escape_for_cmd(source_branch)
    safe_target_branch = _escape_for_cmd(target_branch)
    safe_title = _escape_for_cmd(title)
    safe_organization = _escape_for_cmd(config.organization)
    safe_project = _escape_for_cmd(config.project)
    safe_repository = _escape_for_cmd(config.repository)

    # Build az repos pr create command
    cmd = [
        "az",
        "repos",
        "pr",
        "create",
        "--source-branch",
        safe_source_branch,
        "--target-branch",
        safe_target_branch,
        "--title",
        safe_title,
        "--organization",
        safe_organization,
        "--project",
        safe_project,
        "--repository",
        safe_repository,
        "--output",
        "json",
    ]

    if draft:
        cmd.append("--draft")

    if parsed_reviewers:
        cmd.append("--reviewers")
        cmd.extend(_escape_for_cmd(reviewer) for reviewer in parsed_reviewers)

    desc_temp_file_path = None
    if description:
        if sys.platform == "win32":
            # Use @filepath on Windows to avoid cmd.exe truncating multiline
            # values when az is executed via shell=True for .cmd scripts.
            import tempfile

            try:
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    suffix=".md",
                    prefix="agdt-pr-desc-",
                    delete=False,
                    encoding="utf-8",
                ) as desc_temp_file:
                    desc_temp_file_path = desc_temp_file.name
                    desc_temp_file.write(description)

                cmd.extend(["--description", _escape_for_cmd(f"@{desc_temp_file_path}")])
            except Exception:
                if desc_temp_file_path is not None:
                    try:
                        os.unlink(desc_temp_file_path)
                    except OSError:
                        pass
                    else:
                        desc_temp_file_path = None
                raise
        else:
            cmd.extend(["--description", description])

    try:
        result = run_safe(cmd, capture_output=True, text=True, env=env, timeout=timeout)
    finally:
        if desc_temp_file_path is not None:
            try:
                os.unlink(desc_temp_file_path)
            except OSError as exc:  # pragma: no cover
                print(
                    f"Warning: Could not delete temporary PR description file {desc_temp_file_path}: {exc}",
                    file=sys.stderr,
                )

    if result.returncode != 0:
        print(f"Error creating PR: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        pr_data = parse_json_response(result.stdout, "PR response")
        if (
            not isinstance(pr_data, dict)
            or isinstance(pr_data.get("pullRequestId"), bool)
            or not isinstance(pr_data.get("pullRequestId"), int)
            or pr_data["pullRequestId"] <= 0
        ):
            raise ValueError("response did not contain a valid pullRequestId")
        repository = pr_data.get("repository", {})
        if not isinstance(repository, dict):
            raise ValueError("response contained an invalid repository object")
        if "webUrl" in repository and not isinstance(repository["webUrl"], str):
            raise ValueError("response contained an invalid repository webUrl")
    except (SystemExit, TypeError, ValueError) as exc:
        raise PullRequestCreationPostSubmitError(
            f"Azure DevOps pull-request creation outcome is indeterminate: response is malformed ({exc})"
        ) from exc

    pull_request_id: int = pr_data["pullRequestId"]
    print("Pull request created successfully.")
    print(f"PR ID: {pull_request_id}")

    # Construct and display the UI URL
    repo_web_url = repository.get("webUrl", "")
    pr_ui_url = ""
    if repo_web_url:
        pr_ui_url = f"{repo_web_url}/pullrequest/{pull_request_id}"
        print(f"PR URL: {pr_ui_url}")

    # Store the PR ID in state for subsequent commands. The remote PR already
    # exists, so a persistence failure must not look like a retryable create
    # failure.
    try:
        if on_pull_request_created is None:
            set_value("pull_request_id", pull_request_id)
        else:
            on_pull_request_created(pull_request_id)
    except Exception as exc:
        raise PullRequestCreationPostSubmitError(
            f"Azure DevOps pull-request creation outcome is indeterminate: state persistence failed ({exc})"
        ) from exc
    if on_pull_request_created is None:
        print(f"(PR ID {pull_request_id} saved to state for subsequent commands)")

    # Try to advance workflow if applicable
    try:
        from ..workflows.advancement import try_advance_workflow_after_pr_creation

        try_advance_workflow_after_pr_creation(pull_request_id, pr_ui_url)
    except ImportError:  # pragma: no cover
        pass  # Workflows module not available
    except Exception as exc:
        raise PullRequestCreationPostSubmitError(
            f"Azure DevOps pull-request creation outcome is indeterminate: workflow advancement failed ({exc})"
        ) from exc

    return pr_ui_url or None


def resolve_thread() -> Any:
    """
    Resolve (close) a pull request comment thread.

    Delegates to the provider-agnostic implementation in
    ``agentic_devtools.cli.pull_request_threads`` with the Azure DevOps
    provider pre-selected, preserving the immutable request snapshot and
    structured result contract of the new implementation.

    Reads from state:
    - pull_request_id (required): Pull request ID
    - thread_id (required): Thread ID to resolve
    - dry_run (optional): Preview without making API calls

    Usage:
        agdt-set pull_request_id 23046
        agdt-set thread_id 139474
        agdt-resolve-thread
    """
    from agentic_devtools.cli.pull_request_threads import resolve_thread as _new_resolve

    return _new_resolve(provider="azure_devops")


def get_pull_request_threads(
    pull_request_id: int | None = None,
    repository: str | None = None,
    organization: str | None = None,
    project: str | None = None,
) -> None:
    """
    Get all comment threads for a pull request.

    Reads from state:
    - pull_request_id (required): Pull request ID
    - repository (optional): Repository override for provider-neutral callers
    - organization, project (optional): Azure DevOps coordinate overrides
    - dry_run (optional): Preview without making API calls
    - sync_review_state (optional): If true, reconcile local review-state.json
      with marker-identified threads from Azure DevOps.

    Outputs thread information including:
    - Thread ID
    - Status (active, fixed, closed, etc.)
    - File path (if file-level comment)
    - Comments with author and content

    Usage:
        agdt-set pull_request_id 23046
        agdt-get-pull-request-threads
    """
    requests = require_requests()

    if pull_request_id is None:
        pull_request_id = get_pull_request_id(required=True)
    elif not isinstance(pull_request_id, int) or isinstance(pull_request_id, bool) or pull_request_id <= 0:
        raise ValueError("pull_request_id must be a positive integer")
    dry_run = is_dry_run()
    sync_flag = parse_bool_from_state("sync_review_state")
    if repository is not None:
        if not isinstance(repository, str) or not repository.strip():
            raise ValueError("repository must be a non-empty string")
        repository = repository.strip()
    for name, value in (("organization", organization), ("project", project)):
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"{name} must be a non-empty string")
    config = AzureDevOpsConfig.from_state()
    config = dataclasses.replace(
        config,
        organization=organization.strip() if organization is not None else config.organization,
        project=project.strip() if project is not None else config.project,
        repository=repository.strip() if repository is not None else config.repository,
    )

    if dry_run:
        print(f"[DRY RUN] Would get threads for PR {pull_request_id}")
        print(f"Repository: {config.repository} | Org/Project: {config.organization} / {config.project}")
        return

    pat = get_pat()
    headers = get_auth_headers(pat)

    print(f"Resolving repository ID for '{config.repository}'...")
    repo_id = get_repository_id(config.organization, config.project, config.repository)

    threads_url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "threads")

    print(f"Fetching threads for PR {pull_request_id}...")
    response = requests.get(threads_url, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    threads = data.get("value", [])

    if not threads:
        print("No comment threads found.")
        return

    print_threads(threads)

    if sync_flag:
        try:
            review_state = load_review_state(pull_request_id)
        except FileNotFoundError:
            from datetime import datetime

            review_state = ReviewState(
                prId=pull_request_id,
                repoId=repo_id,
                repoName=config.repository,
                project=config.project,
                organization=config.organization,
                latestIterationId=0,
                scaffoldedUtc=datetime.now(UTC).isoformat(),
                overallSummary=OverallSummary(threadId=0, commentId=0),
            )
            print("No review-state.json found; bootstrapping from marker-identified threads.", file=sys.stderr)
        sync_review_state_from_threads(pull_request_id, threads, review_state)
        save_review_state(review_state)
        print("Review state synced with marker-identified threads.")


@dataclass(frozen=True)
class AzureApprovalOutcome:
    """Structured outcome of :func:`approve_pull_request`.

    ``resolved`` is ``True`` when the approval mutation is fully complete:
    either the Review Narrative was updated in place, or the fallback comment
    thread was posted *and* successfully marked resolved. It is ``False`` when
    the fallback comment was posted but the thread could not be resolved, so
    the documented "resolved approval comment" state was not reached even
    though no mutation needs to be retried. ``operation_kind`` explicitly
    identifies a narrative update or fallback comment; ``thread_id`` is the
    fallback comment's thread ID.
    """

    resolved: bool
    thread_id: int | None = None
    operation_kind: Literal["narrative_update", "fallback_comment"] | None = None


class ReviewStateRepositoryMismatchError(ValueError):
    """Raised when explicit Azure repo input disagrees with the stored review state."""


class ReviewStateNotFoundError(FileNotFoundError):
    """Raised when the expected review-state artifact does not exist for the PR."""


def approve_pull_request(
    pull_request_id: int | None = None,
    content: str | None = None,
    dry_run: bool | None = None,
    config: AzureDevOpsConfig | None = None,
) -> AzureApprovalOutcome | None:
    """
    Approve a pull request by updating the Review Narrative in the overall summary comment.

    Attempts to update the ``narrativeSummary`` field in the existing overall PR summary
    comment in-place via ``update_review_narrative()``.  Falls back to creating a new
    PR-level comment thread when review-state.json is unavailable or the update fails.

    Reads from state when the corresponding explicit argument is omitted:
    - pull_request_id (required): Pull request ID
    - content (required): Approval comment content
    - dry_run (optional): Preview without making API calls

    Usage:
        agdt-set pull_request_id 23046
        agdt-set content "LGTM! All acceptance criteria met."
        agdt-approve-pull-request

    Returns:
        ``None`` in dry-run mode. Otherwise an :class:`AzureApprovalOutcome`
        describing whether the approval mutation fully completed (narrative
        update, or fallback comment posted and resolved) or only partially
        completed (fallback comment posted but left active because resolving
        it failed).
    """
    resolved_pull_request_id = get_pull_request_id(required=True) if pull_request_id is None else pull_request_id
    resolved_content = require_content() if content is None else content
    resolved_dry_run = is_dry_run() if dry_run is None else dry_run
    if (
        isinstance(resolved_pull_request_id, bool)
        or not isinstance(resolved_pull_request_id, int)
        or resolved_pull_request_id <= 0
    ):
        raise ValueError("pull_request_id must be a positive integer")
    if not isinstance(resolved_content, str) or not resolved_content.strip():
        raise ValueError("content is required")
    if not isinstance(resolved_dry_run, bool):
        raise ValueError("dry_run must be a boolean")
    resolved_config = config or AzureDevOpsConfig.from_state()

    if resolved_dry_run:
        print(f"[DRY RUN] Would update Review Narrative for PR {resolved_pull_request_id}")
        print(f"Content:\n{resolved_content}")
        return None

    if pull_request_id is None and content is None and dry_run is None and config is None:
        # Clear stale file context so fallback add_pull_request_comment posts as PR-level
        delete_value("path")
        delete_value("line")
        delete_value("end_line")

    def _post_fallback_comment(reason: str) -> AzureApprovalOutcome:
        print(
            f"Warning: Could not update Review Narrative ({_sanitize_diagnostic(reason)}); "
            "falling back to new comment.",
            file=sys.stderr,
        )
        # A deterministic key derived from the PR ID/repository lets
        # `post_pr_comment` find and reuse an already-posted fallback thread on
        # retries/reruns, instead of creating another resolved comment each
        # time (see #4025 idempotency). The key intentionally excludes
        # `content` so wording changes reconcile the existing thread instead
        # of producing a new marker/duplicate thread.
        try:
            thread_id = post_pr_comment(
                resolved_pull_request_id,
                resolved_content,
                config=resolved_config,
                idempotency_key=build_approval_idempotency_key(
                    resolved_pull_request_id,
                    resolved_config.repository,
                ),
            )
        except PrCommentResolveFailedError as resolve_exc:
            print(
                f"Warning: {_sanitize_diagnostic(resolve_exc)}. Leaving the thread active.",
                file=sys.stderr,
            )
            return AzureApprovalOutcome(
                resolved=False,
                thread_id=resolve_exc.thread_id,
                operation_kind="fallback_comment",
            )
        return AzureApprovalOutcome(resolved=True, thread_id=thread_id, operation_kind="fallback_comment")

    try:
        update_review_narrative(
            resolved_pull_request_id,
            resolved_content,
            config=resolved_config,
        )
    except Exception as exc:
        return _post_fallback_comment(str(exc))

    return AzureApprovalOutcome(resolved=True, operation_kind="narrative_update")


def mark_pull_request_draft(
    pull_request_id: int | None = None,
    *,
    exit_on_error: bool = True,
    organization: str | None = None,
    project: str | None = None,
    dry_run: bool | None = None,
) -> None:
    """
    Mark a pull request as draft.

    Args:
        pull_request_id: Pull request ID. Falls back to state's ``pull_request_id``
            (required) when not supplied explicitly.
        exit_on_error: When ``True`` (default), failures (missing Azure CLI,
            failed ``az`` invocation, unparseable response) call ``sys.exit(1)``.
            When ``False``, those failures raise ``RuntimeError`` instead so
            programmatic callers can handle them without a process exit.
        organization: Overrides the Azure DevOps organization from
            ``AzureDevOpsConfig.from_state()`` when supplied.
        project: Overrides the Azure DevOps project from
            ``AzureDevOpsConfig.from_state()`` when supplied.
        dry_run: Preview without making API calls. When ``None`` (default),
            falls back to state's ``dry_run`` value; an explicit ``True``/``False``
            overrides state.

    Reads from state:
    - pull_request_id (required unless the parameter is supplied)
    - dry_run (optional): used only when the ``dry_run`` parameter is ``None``

    Usage:
        agdt-set pull_request_id 23046
        agdt-mark-pull-request-draft
    """
    resolved_pull_request_id = pull_request_id if pull_request_id is not None else get_pull_request_id(required=True)
    if (
        not isinstance(resolved_pull_request_id, int)
        or isinstance(resolved_pull_request_id, bool)
        or resolved_pull_request_id <= 0
    ):
        raise ValueError("pull_request_id must be a positive integer")
    if dry_run is not None and not isinstance(dry_run, bool):
        raise ValueError("dry_run must be a boolean")
    if organization is not None and (not isinstance(organization, str) or not organization.strip()):
        raise ValueError("organization must be a non-empty string")
    if project is not None and (not isinstance(project, str) or not project.strip()):
        raise ValueError("project must be a non-empty string")
    resolved_dry_run = is_dry_run() if dry_run is None else dry_run
    config = AzureDevOpsConfig.from_state()
    if organization is not None or project is not None:
        config = dataclasses.replace(
            config,
            organization=organization if organization is not None else config.organization,
            project=project if project is not None else config.project,
        )

    if resolved_dry_run:
        print(f"[DRY RUN] Would mark PR {resolved_pull_request_id} as draft")
        print(f"Org/Project: {config.organization} / {config.project}")
        return

    # Verify Azure CLI is available
    try:
        verify_az_cli()
    except SystemExit as exc:
        if exit_on_error:
            raise
        raise RuntimeError("Azure CLI (az) or the azure-devops extension is not available.") from exc

    # Set PAT for az CLI
    pat = get_pat()
    env = os.environ.copy()
    env["AZURE_DEVOPS_EXT_PAT"] = pat

    print(f"Marking PR {resolved_pull_request_id} as draft...")

    cmd = [
        "az",
        "repos",
        "pr",
        "update",
        "--id",
        str(resolved_pull_request_id),
        "--organization",
        config.organization,
        "--project",
        config.project,
        "--draft",
        "true",
        "--output",
        "json",
    ]

    result = run_safe(cmd, capture_output=True, text=True, env=env)

    if result.returncode != 0:
        print(f"Error marking PR as draft: {result.stderr}", file=sys.stderr)
        if exit_on_error:
            sys.exit(1)
        raise RuntimeError((result.stderr or "Failed to mark PR as draft").strip())

    try:
        pr_data = parse_json_response(result.stdout, "PR response")
    except SystemExit as exc:
        if exit_on_error:
            raise
        raise RuntimeError("Failed to parse PR response as JSON.") from exc
    print(f"PR {resolved_pull_request_id} marked as draft successfully.")

    # Display the PR URL
    repo_web_url = pr_data.get("repository", {}).get("webUrl", "")
    if repo_web_url:
        pull_request_ui_url = f"{repo_web_url}/pullrequest/{resolved_pull_request_id}"
        print(f"PR URL: {pull_request_ui_url}")


def publish_pull_request(
    dry_run: bool | None = None,
    pull_request_id: int | None = None,
    skip_auto_complete: bool | None = None,
) -> None:
    """
    Publish a pull request (remove draft status) and optionally enable auto-complete.

    Args:
        dry_run: When provided, overrides the state-derived dry-run flag. When ``None``,
            the command reads ``dry_run`` from state.
        pull_request_id: When provided, publishes that pull request instead of reading
            ``pull_request_id`` from state.
        skip_auto_complete: When provided, overrides the state-derived auto-complete option.

    Reads from state:
    - pull_request_id (required): Pull request ID when ``pull_request_id`` is ``None``
    - skip_auto_complete (optional): If true, don't enable auto-complete (default: false)
    - dry_run (optional): Preview without making API calls when ``dry_run`` is ``None``

    Usage:
        agdt-set pull_request_id 23046
        agdt-publish-pull-request

        # To skip auto-complete:
        agdt-set skip_auto_complete true
        agdt-publish-pull-request
    """
    if pull_request_id is None:
        pull_request_id = get_pull_request_id(required=True)
    elif not isinstance(pull_request_id, int) or isinstance(pull_request_id, bool) or pull_request_id <= 0:
        raise ValueError("pull_request_id must be a positive integer")
    if dry_run is None:
        dry_run = is_dry_run()
    elif not isinstance(dry_run, bool):
        raise ValueError("dry_run must be a boolean")
    if skip_auto_complete is None:
        skip_auto_complete = parse_bool_from_state("skip_auto_complete", default=False)
    elif not isinstance(skip_auto_complete, bool):
        raise ValueError("skip_auto_complete must be a boolean")
    config = AzureDevOpsConfig.from_state()

    if dry_run:
        print(f"[DRY RUN] Would publish PR {pull_request_id}")
        print(f"Org/Project: {config.organization} / {config.project}")
        if skip_auto_complete:
            print("[DRY RUN] Auto-complete: Skipped")
        else:
            print("[DRY RUN] Auto-complete: Will be enabled")
        return

    # Verify Azure CLI is available
    verify_az_cli()

    # Set PAT for az CLI
    pat = get_pat()
    env = os.environ.copy()
    env["AZURE_DEVOPS_EXT_PAT"] = pat

    print(f"Publishing PR {pull_request_id}...")

    # Remove draft status
    cmd = [
        "az",
        "repos",
        "pr",
        "update",
        "--id",
        str(pull_request_id),
        "--organization",
        config.organization,
        "--project",
        config.project,
        "--draft",
        "false",
        "--output",
        "json",
    ]

    result = run_safe(cmd, capture_output=True, text=True, env=env)

    if result.returncode != 0:
        print(f"Error publishing PR: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    pr_data = parse_json_response(result.stdout, "PR response")
    print(f"PR {pull_request_id} published successfully.")

    # Enable auto-complete unless skipped
    if not skip_auto_complete:
        print(f"Setting auto-complete on PR {pull_request_id}...")

        auto_complete_cmd = [
            "az",
            "repos",
            "pr",
            "update",
            "--id",
            str(pull_request_id),
            "--organization",
            config.organization,
            "--project",
            config.project,
            "--auto-complete",
            "true",
            "--output",
            "json",
        ]

        auto_result = run_safe(auto_complete_cmd, capture_output=True, text=True, env=env)

        if auto_result.returncode != 0:
            print(
                "Warning: Failed to set auto-complete. PR is published but auto-complete not enabled.",
                file=sys.stderr,
            )
            print(f"Error: {auto_result.stderr}", file=sys.stderr)
        else:
            print(f"Auto-complete enabled on PR {pull_request_id}.")

    # Display the PR URL
    repo_web_url = pr_data.get("repository", {}).get("webUrl", "")
    if repo_web_url:
        pull_request_ui_url = f"{repo_web_url}/pullrequest/{pull_request_id}"
        print(f"PR URL: {pull_request_ui_url}")
