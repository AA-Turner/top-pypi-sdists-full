"""
Azure DevOps helper functions.

Pure utility functions that don't read state directly.
"""

import json
import os
import re
import reprlib
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote

from ...state import get_state_dir, is_safe_dir_segment, read_modify_write_state
from ..subprocess_utils import run_safe
from .auth import get_auth_headers, get_pat
from .config import (
    API_VERSION,
    DEFAULT_ORGANIZATION,
    DEFAULT_PROJECT,
    DEFAULT_REPOSITORY,
    PR_ITERATION_CHANGES_API_VERSION,
    AzureDevOpsConfig,
)


def _escape_for_cmd(value: str) -> str:
    """Escape cmd.exe metacharacters for safe use in Windows ``az`` CLI arguments.

    On Windows, ``run_safe`` uses ``shell=True`` for the ``az`` CLI (a
    ``.cmd`` batch script).  ``cmd.exe`` interprets ``%VAR%`` patterns and
    shell operators such as ``&``, ``|``, ``<``, ``>``, ``^``, and ``"``
    inside arguments.  This function neutralises all of them so that
    user-controlled project and repository names are passed literally.
    On non-Windows platforms this is a no-op.
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


def build_pr_base_url(config: AzureDevOpsConfig, pull_request_id: int) -> str:
    """Build the PR web URL for building discussion links.

    Args:
        config: Azure DevOps configuration.
        pull_request_id: Pull request ID.

    Returns:
        PR web URL string.
    """
    org = config.organization.rstrip("/")
    if not org.startswith(("http://", "https://")):
        org = f"https://dev.azure.com/{org.lstrip('/')}"
    encoded_project = quote(config.project, safe="")
    encoded_repo = quote(config.repository, safe="")
    return f"{org}/{encoded_project}/_git/{encoded_repo}/pullrequest/{pull_request_id}"


def _get_repository_id_via_rest(
    organization: str,
    project: str,
    repository: str,
) -> str:
    """Resolve the repository ID via Azure DevOps REST API using PAT auth."""
    requests = require_requests()

    headers = get_auth_headers(get_pat())
    # Normalize to avoid double-encoding values that may already be
    # percent-encoded (e.g. from a git remote URL).
    project_encoded = quote(unquote(project), safe="")
    repository_encoded = quote(unquote(repository), safe="")
    url = (
        f"{organization.rstrip('/')}/{project_encoded}/_apis/git/repositories/"
        f"{repository_encoded}?api-version={API_VERSION}"
    )

    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(f"REST API returned {response.status_code}: {response.text.strip() or 'No response body'}")

    data = response.json()
    repo_id = (data.get("id") or "").strip()
    if not repo_id:
        raise RuntimeError("REST API response did not include a repository id")

    return repo_id


def parse_bool_from_state_value(raw_value, default: bool = False) -> bool:
    """
    Parse a boolean value from a raw state value.

    Args:
        raw_value: The value from state (could be None, bool, or str).
        default: Default value if raw_value is None.

    Returns:
        Boolean value parsed from input.
    """
    if raw_value is None:
        return default
    if isinstance(raw_value, bool):
        return raw_value
    return str(raw_value).lower() in ("1", "true", "yes")


def require_requests():
    """Import and return requests module, exiting if not available."""
    try:
        import requests

        return requests
    except ImportError:
        print(
            "Error: requests library required. Install with: pip install requests",
            file=sys.stderr,
        )
        sys.exit(1)


def get_repository_id(
    organization: str = DEFAULT_ORGANIZATION,
    project: str = DEFAULT_PROJECT,
    repository: str = DEFAULT_REPOSITORY,
) -> str:
    """Get the repository ID, preferring REST and falling back to Azure CLI."""
    rest_error_message: str | None = None
    try:
        return _get_repository_id_via_rest(
            organization=organization,
            project=project,
            repository=repository,
        )
    except Exception as rest_error:
        rest_error_message = f"REST lookup failed for '{repository}': {rest_error}"

    # Azure CLI expects human-readable names; values derived from remotes may
    # already be percent-encoded (e.g. "My%20Project").  On Windows, az is a
    # .cmd batch script so run_safe uses shell=True, allowing cmd.exe to expand
    # %VAR% patterns in arguments.  Double every % to neutralise expansion.
    organization_for_cli = _escape_for_cmd(organization)
    project_for_cli = _escape_for_cmd(unquote(project))
    repository_for_cli = _escape_for_cmd(unquote(repository))

    cmd = [
        "az",
        "repos",
        "show",
        "--organization",
        organization_for_cli,
        "--project",
        project_for_cli,
        "--repository",
        repository_for_cli,
        "--query",
        "id",
        "--output",
        "tsv",
    ]

    cli_env = os.environ.copy()
    try:
        cli_env["AZURE_DEVOPS_EXT_PAT"] = get_pat()
    except OSError as pat_err:
        raise RuntimeError(
            f"{rest_error_message}\nAzure CLI fallback failed: PAT not available ({pat_err})"
        ) from pat_err
    try:
        result = run_safe(cmd, capture_output=True, text=True, env=cli_env)
    except FileNotFoundError as cli_missing_err:
        raise RuntimeError(
            f"{rest_error_message}\nAzure CLI fallback failed: Azure CLI not found ({cli_missing_err})"
        ) from cli_missing_err

    if result.returncode == 0:
        repo_id = result.stdout.strip()
        if repo_id:
            return repo_id
        cli_error = f"Empty repository ID returned for '{repository}'"
    else:
        cli_error = f"Failed to get repository ID for '{repository}': {result.stderr}"

    raise RuntimeError(f"{rest_error_message}\nAzure CLI fallback failed: {cli_error}")


def resolve_thread_by_id(
    requests_module,
    headers: dict[str, str],
    config: AzureDevOpsConfig,
    repo_id: str,
    pull_request_id: int,
    thread_id: int,
    status: str = "closed",
) -> None:
    """
    Resolve a pull request thread by setting its status.

    Args:
        requests_module: The requests module.
        headers: Auth headers for API calls.
        config: Azure DevOps configuration.
        repo_id: Repository ID.
        pull_request_id: Pull request ID.
        thread_id: Thread ID to resolve.
        status: Status to set ("closed", "fixed", etc.).
    """
    resolve_url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "threads", thread_id)
    response = requests_module.patch(resolve_url, headers=headers, json={"status": status})
    response.raise_for_status()


def post_pr_comment(
    pull_request_id: int,
    content: str,
    config: AzureDevOpsConfig | None = None,
    dry_run: bool = False,
    leave_thread_active: bool = False,
) -> int | None:
    """Post a general (non-file-anchored) comment thread on a pull request.

    Unlike the state-reading CLI layer (``add_pull_request_comment()``), this
    function does **not** write to global agent state.  When ``config`` is
    omitted it calls ``AzureDevOpsConfig.from_state()`` to resolve connection
    settings (a read-only access to state); pass an explicit ``config`` when
    you need a fully state-independent call.

    Args:
        pull_request_id: Pull request ID.
        content: Comment text.
        config: Azure DevOps config.  When ``None``, resolved via
            ``AzureDevOpsConfig.from_state()`` (reads—but does not write—state).
        dry_run: When True, prints what would happen without making API calls.
        leave_thread_active: When True, keep the new thread in ``"active"`` status.
            When False (default), the thread is immediately resolved (``"closed"``)
            after posting.

    Returns:
        The numeric thread ID on success, or ``None`` in dry-run mode.

    Raises:
        RuntimeError: When the API call fails, the repository cannot be resolved,
            or the API response does not contain a positive integer thread ID.
    """
    if config is None:
        config = AzureDevOpsConfig.from_state()

    if dry_run:
        print(f"[DRY RUN] Would add comment to PR {pull_request_id}")
        if not leave_thread_active:
            print("[DRY RUN] Would also resolve the thread after posting")
        print(f"Content:\n{content}")
        return None

    requests = require_requests()
    pat = get_pat()
    headers = get_auth_headers(pat)

    repo_id = get_repository_id(config.organization, config.project, config.repository)

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

    print(f"Adding comment to PR {pull_request_id}...")
    response = requests.post(thread_url, headers=headers, json=thread_body, timeout=30)
    response.raise_for_status()

    result = response.json()
    thread_id_raw = result.get("id")
    if not isinstance(thread_id_raw, int) or thread_id_raw <= 0:
        raise RuntimeError(f"Unexpected API response: 'id' is missing or not a positive integer. Response: {result!r}")
    thread_id: int = thread_id_raw
    print(f"Comment added successfully (thread ID: {thread_id})")

    if not leave_thread_active:
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

    return thread_id


class CrossIdentityForbiddenError(Exception):
    """Raised when a PATCH fails with 403 due to cross-identity ownership.

    This indicates the comment is owned by a different Azure DevOps identity
    and cannot be edited by the current PAT user.
    """

    def __init__(self, thread_id: int, comment_id: int, message: str = "") -> None:
        self.thread_id = thread_id
        self.comment_id = comment_id
        default_msg = f"403 Forbidden: cannot PATCH comment {comment_id} on thread {thread_id} (cross-identity)"
        super().__init__(message or default_msg)


_PATCH_MAX_RETRIES = 3


def build_cross_identity_reply_content(content: str) -> str:
    """Prefix scaffold content for a cross-identity reply fallback."""
    marker = "<!-- agdt-review:v1 mode:cross-identity-update -->"
    return f"{marker}\n**[Cross-identity update]**\n\n{content}"


def post_thread_reply(
    requests_module,
    headers: dict[str, str],
    config: AzureDevOpsConfig,
    repo_id: str,
    pull_request_id: int,
    thread_id: int,
    content: str,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Post a reply to an existing thread."""
    if dry_run:
        print(f"[DRY RUN] Would post reply to thread {thread_id}, PR {pull_request_id}")
        return {}

    url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "threads", thread_id, "comments")
    response = requests_module.post(url, headers=headers, json={"content": content, "commentType": "text"}, timeout=30)
    response.raise_for_status()
    return response.json()


def post_cross_identity_reply(
    requests_module,
    headers: dict[str, str],
    config: AzureDevOpsConfig,
    repo_id: str,
    pull_request_id: int,
    thread_id: int,
    content: str,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Post a reply carrying updated content when the main comment cannot be patched."""
    return post_thread_reply(
        requests_module=requests_module,
        headers=headers,
        config=config,
        repo_id=repo_id,
        pull_request_id=pull_request_id,
        thread_id=thread_id,
        content=build_cross_identity_reply_content(content),
        dry_run=dry_run,
    )


def patch_comment(
    requests_module,
    headers: dict[str, str],
    config: AzureDevOpsConfig,
    repo_id: str,
    pull_request_id: int,
    thread_id: int,
    comment_id: int,
    new_content: str,
    dry_run: bool = False,
    cross_identity: bool = False,
    reply_on_forbidden: bool = False,
) -> dict[str, Any]:
    """
    Edit an existing comment's content via PATCH.

    Args:
        requests_module: The requests module.
        headers: Auth headers for API calls.
        config: Azure DevOps configuration.
        repo_id: Repository ID.
        pull_request_id: Pull request ID.
        thread_id: Thread ID containing the comment.
        comment_id: Comment ID to edit.
        new_content: New markdown content for the comment.
        dry_run: If True, skip the API call and return {}.
        cross_identity: If True, skip PATCH and post a cross-identity reply directly.
        reply_on_forbidden: If True, post a cross-identity reply instead of raising on 403.

    Returns:
        Parsed JSON response dict from the API, or {} in dry_run mode.
    """
    if thread_id <= 0:
        # A thread_id of 0 means "no thread" — e.g. a file whose status/summary is
        # rendered inline in the single consolidated review comment rather than in
        # its own thread. There is nothing to patch, so this is a no-op.
        return {}

    if dry_run:
        print(f"[DRY RUN] Would patch comment {comment_id} on thread {thread_id}, PR {pull_request_id}")
        return {}

    if cross_identity:
        return post_cross_identity_reply(
            requests_module=requests_module,
            headers=headers,
            config=config,
            repo_id=repo_id,
            pull_request_id=pull_request_id,
            thread_id=thread_id,
            content=new_content,
        )

    url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "threads", thread_id, "comments", comment_id)

    for attempt in range(_PATCH_MAX_RETRIES):  # pragma: no branch
        response = requests_module.patch(url, headers=headers, json={"content": new_content}, timeout=30)
        if response.status_code == 429 and attempt < _PATCH_MAX_RETRIES - 1:
            retry_after_header = response.headers.get("Retry-After")
            retry_after = 60
            if retry_after_header is not None:
                try:
                    parsed = int(retry_after_header)
                except (TypeError, ValueError):
                    parsed = -1
                if parsed >= 0:
                    retry_after = parsed
            time.sleep(retry_after)
            continue
        if response.status_code == 403:
            if reply_on_forbidden:
                return post_cross_identity_reply(
                    requests_module=requests_module,
                    headers=headers,
                    config=config,
                    repo_id=repo_id,
                    pull_request_id=pull_request_id,
                    thread_id=thread_id,
                    content=new_content,
                )
            raise CrossIdentityForbiddenError(thread_id, comment_id)
        response.raise_for_status()
        return response.json()


def patch_thread_status(
    requests_module,
    headers: dict[str, str],
    config: AzureDevOpsConfig,
    repo_id: str,
    pull_request_id: int,
    thread_id: int,
    status: str,
    dry_run: bool = False,
) -> dict[str, Any]:
    """
    Change a pull request thread's status via PATCH.

    Args:
        requests_module: The requests module.
        headers: Auth headers for API calls.
        config: Azure DevOps configuration.
        repo_id: Repository ID.
        pull_request_id: Pull request ID.
        thread_id: Thread ID to update.
        status: New status value (e.g. "active" or "closed").
        dry_run: If True, skip the API call and return {}.

    Returns:
        Parsed JSON response dict from the API, or {} in dry_run mode.
    """
    if thread_id <= 0:
        # A thread_id of 0 means "no thread" (a file rendered inline in the single
        # consolidated review comment); there is no thread status to change.
        return {}

    if dry_run:
        print(f"[DRY RUN] Would set thread {thread_id} status to '{status}' on PR {pull_request_id}")
        return {}

    url = config.build_api_url(repo_id, "pullRequests", pull_request_id, "threads", thread_id)

    for attempt in range(_PATCH_MAX_RETRIES):  # pragma: no branch
        response = requests_module.patch(url, headers=headers, json={"status": status}, timeout=30)
        if response.status_code == 429 and attempt < _PATCH_MAX_RETRIES - 1:
            header_value = response.headers.get("Retry-After")
            retry_after = 60
            if header_value is not None:
                try:
                    parsed = int(header_value)
                except (TypeError, ValueError):
                    parsed = -1
                if parsed >= 0:
                    retry_after = parsed
            time.sleep(retry_after)
            continue
        response.raise_for_status()
        return response.json()


def convert_to_pull_request_title(title: str) -> str:
    """
    Strip Markdown links from a title to match pull request title convention.

    Transforms commit-style titles with Markdown links to clean PR titles:
    - feature([PROJECT-1234](link)): summary -> feature(PROJECT-1234): summary
    - feature([PROJECT-1234](link) / [PROJECT-5678](link)): summary -> feature(PROJECT-1234/PROJECT-5678): summary

    Args:
        title: The title string potentially containing Markdown links.

    Returns:
        String with Markdown links stripped.
    """
    # Remove (link) parts: [text](link) -> [text]
    result = re.sub(r"\]\([^)]+\)", "]", title)
    # Remove brackets: [text] -> text
    result = re.sub(r"\[([^\]]+)\]", r"\1", result)
    # Remove spaces around slash: text / text -> text/text
    result = re.sub(r"\s*/\s*", "/", result)
    return result


def build_thread_context(
    path: str | None,
    line: int | None,
    end_line: int | None,
) -> dict[str, Any] | None:
    """
    Build thread context for file-level PR comments.

    Args:
        path: File path for the comment.
        line: Start line number.
        end_line: End line number (defaults to line if not specified).

    Returns:
        Thread context dict or None if no path specified.
    """
    if not path:
        return None

    thread_context: dict[str, Any] = {"filePath": path}

    if line is not None:
        # For line comments, we need right-side positioning (after changes)
        thread_context["rightFileStart"] = {"line": int(line), "offset": 1}
        end = int(end_line) if end_line is not None else int(line)
        thread_context["rightFileEnd"] = {"line": end, "offset": 1}

    return thread_context


def verify_az_cli() -> None:
    """Verify Azure CLI and azure-devops extension are installed."""
    try:
        run_safe(["az", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Azure CLI (az) is not installed or not in PATH.", file=sys.stderr)
        print(
            "Install it from: https://learn.microsoft.com/cli/azure/install-azure-cli",
            file=sys.stderr,
        )
        sys.exit(1)

    # Check for azure-devops extension
    result = run_safe(
        [
            "az",
            "extension",
            "list",
            "--output",
            "tsv",
            "--query",
            "[?name=='azure-devops'].name",
        ],
        capture_output=True,
        text=True,
    )
    if not result.stdout.strip():
        print(
            "Error: Azure CLI extension 'azure-devops' is not installed.",
            file=sys.stderr,
        )
        print("Run: az extension add --name azure-devops", file=sys.stderr)
        sys.exit(1)


def parse_json_response(response_text: str, context: str) -> dict[str, Any]:
    """Parse JSON response, exiting with error on failure."""
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        print(f"Error parsing {context}: {response_text}", file=sys.stderr)
        sys.exit(1)


def print_threads(threads: list[dict[str, Any]]) -> None:
    """Format and print PR threads."""
    print(f"\nFound {len(threads)} thread(s):\n")

    for thread in threads:
        thread_id = thread.get("id")
        status = thread.get("status", "unknown")
        thread_context = thread.get("threadContext") or {}
        file_path = thread_context.get("filePath", "(general comment)")

        print(f"--- Thread {thread_id} [{status}] ---")
        print(f"File: {file_path}")

        comments = thread.get("comments", [])
        for comment in comments:
            author = (comment.get("author") or {}).get("displayName", "Unknown")
            content = comment.get("content", "(no content)")
            comment_id = comment.get("id")
            # Truncate long content
            content_preview = content[:100] + "..." if len(content) > 100 else content
            print(f"  [{comment_id}] {author}: {content_preview}")

        print()


def find_pull_request_by_issue_key(
    issue_key: str,
    config: AzureDevOpsConfig | None = None,
    headers: dict[str, str] | None = None,
    status: str = "active",
) -> dict[str, Any] | None:
    """
    Find a pull request by Jira issue key in the source branch, title, or description.

    This searches Azure DevOps for active PRs (including drafts) where the issue key
    appears in the source branch name, PR title, or PR description.

    Args:
        issue_key: Jira issue key (e.g., "PROJECT-1234")
        config: Azure DevOps configuration (defaults to from_state)
        headers: Auth headers (defaults to get_auth_headers)
        status: PR status filter ("active", "completed", "abandoned", "all")

    Returns:
        Pull request data dict if found, None otherwise.
        If multiple PRs match, returns the most recently created one.
    """
    requests = require_requests()

    if config is None:
        config = AzureDevOpsConfig.from_state()

    if headers is None:
        pat = get_pat()  # pragma: no cover
        headers = get_auth_headers(pat)  # pragma: no cover

    # Get repository ID using config values
    try:
        repo_id = get_repository_id(
            organization=config.organization,
            project=config.project,
            repository=config.repository,
        )
    except RuntimeError as e:  # pragma: no cover
        print(f"Error: {e}", file=sys.stderr)
        return None

    # Build search URL - search by status only, we'll filter locally
    project_encoded = config.project.replace(" ", "%20")
    url = (
        f"{config.organization}/{project_encoded}/_apis/git/repositories/"
        f"{repo_id}/pullrequests?searchCriteria.status={status}&api-version=7.0"
    )

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"Error: Failed to search PRs: {response.status_code}", file=sys.stderr)
            return None

        data = response.json()
        pull_requests = data.get("value", [])

        # Filter PRs by issue key in source branch, title, or description (case-insensitive)
        issue_key_lower = issue_key.lower()
        matching_prs = []

        for pr in pull_requests:
            # Check source branch
            source_ref = pr.get("sourceRefName", "")
            branch_name = source_ref.replace("refs/heads/", "")

            # Check title
            title = pr.get("title", "")

            # Check description
            description = pr.get("description", "") or ""

            # Match if issue key appears in any of these fields
            if (
                issue_key_lower in branch_name.lower()
                or issue_key_lower in title.lower()
                or issue_key_lower in description.lower()
            ):
                matching_prs.append(pr)

        if not matching_prs:
            return None

        # If multiple matches, return the most recently created
        if len(matching_prs) > 1:
            # Sort by creation date descending
            matching_prs.sort(
                key=lambda x: x.get("creationDate", ""),
                reverse=True,
            )
            print(
                f"Found {len(matching_prs)} PRs matching '{issue_key}', "
                f"using most recent: #{matching_prs[0].get('pullRequestId')}",
            )

        return matching_prs[0]

    except Exception as e:  # pragma: no cover
        print(f"Error searching for PRs: {e}", file=sys.stderr)
        return None


def get_pull_request_details(
    pull_request_id: int,
    config: AzureDevOpsConfig | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any] | None:
    """
    Get full details for a pull request.

    Args:
        pull_request_id: Pull request ID
        config: Azure DevOps configuration (defaults to from_state)
        headers: Auth headers (defaults to get_auth_headers)

    Returns:
        Pull request data dict if found, None otherwise.
    """
    requests = require_requests()

    if config is None:
        config = AzureDevOpsConfig.from_state()

    if headers is None:
        pat = get_pat()  # pragma: no cover
        headers = get_auth_headers(pat)  # pragma: no cover

    # Get repository ID using config values
    try:
        repo_id = get_repository_id(
            organization=config.organization,
            project=config.project,
            repository=config.repository,
        )
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

    # Build URL to get PR details
    project_encoded = config.project.replace(" ", "%20")
    url = (
        f"{config.organization}/{project_encoded}/_apis/git/repositories/"
        f"{repo_id}/pullrequests/{pull_request_id}?api-version=7.0"
    )

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"Error: Failed to get PR #{pull_request_id}: {response.status_code}", file=sys.stderr)
            return None

        return response.json()

    except Exception as e:
        print(f"Error getting PR details: {e}", file=sys.stderr)
        return None


def get_pull_request_changed_files(
    pull_request_id: int,
    config: AzureDevOpsConfig | None = None,
    headers: dict[str, str] | None = None,
) -> list[str] | None:
    """Get changed file paths for a pull request from the latest iteration."""
    requests = require_requests()

    if config is None:
        config = AzureDevOpsConfig.from_state()

    if headers is None:
        pat = get_pat()  # pragma: no cover
        headers = get_auth_headers(pat)  # pragma: no cover

    try:
        repo_id = get_repository_id(
            organization=config.organization,
            project=config.project,
            repository=config.repository,
        )
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

    organization = config.organization.rstrip("/")
    project_encoded = quote(unquote(config.project), safe="")
    iterations_url = (
        f"{organization}/{project_encoded}/_apis/git/repositories/"
        f"{repo_id}/pullrequests/{pull_request_id}/iterations?api-version={API_VERSION}"
    )

    try:
        iterations_response = requests.get(iterations_url, headers=headers, timeout=30)
        if iterations_response.status_code != 200:
            print(
                f"Error: Failed to get PR #{pull_request_id} iterations: {iterations_response.status_code}",
                file=sys.stderr,
            )
            return None

        iterations = iterations_response.json().get("value", [])
        if not iterations:
            return []

        latest_iteration_id = max((it.get("id", 0) for it in iterations), default=0)
        if latest_iteration_id <= 0:
            return []

        changes_url = (
            f"{organization}/{project_encoded}/_apis/git/repositories/{repo_id}/pullrequests/"
            f"{pull_request_id}/iterations/{latest_iteration_id}/changes"
            f"?api-version={PR_ITERATION_CHANGES_API_VERSION}"
        )
        changes_response = requests.get(changes_url, headers=headers, timeout=30)
        if changes_response.status_code != 200:
            print(
                (
                    f"Error: Failed to get PR #{pull_request_id} iteration "
                    f"{latest_iteration_id} changes: {changes_response.status_code}"
                ),
                file=sys.stderr,
            )
            return None

        change_entries = changes_response.json().get("changeEntries", [])
        changed_paths: list[str] = []
        for entry in change_entries:
            if not isinstance(entry, dict):
                continue
            path = entry.get("item", {}).get("path", "")
            if path:
                changed_paths.append(path)
        return changed_paths
    except Exception as e:
        print(f"Error getting PR changed files: {e}", file=sys.stderr)
        return None


def get_pull_request_source_branch(
    pull_request_id: int,
    config: AzureDevOpsConfig | None = None,
    headers: dict[str, str] | None = None,
) -> str | None:
    """
    Get the source branch name for a pull request.

    Args:
        pull_request_id: Pull request ID
        config: Azure DevOps configuration (defaults to from_state)
        headers: Auth headers (defaults to get_auth_headers)

    Returns:
        Source branch name (without refs/heads/ prefix) if found, None otherwise.
    """
    # Use get_pull_request_details to fetch full PR data
    data = get_pull_request_details(pull_request_id, config, headers)
    if not data:
        return None

    source_ref = data.get("sourceRefName", "")

    # Strip refs/heads/ prefix if present
    if source_ref.startswith("refs/heads/"):
        return source_ref[len("refs/heads/") :]

    return source_ref if source_ref else None


def find_jira_issue_from_pr(
    pull_request_id: int,
    config: AzureDevOpsConfig | None = None,
    headers: dict[str, str] | None = None,
) -> str | None:
    """
    Find Jira issue key from a pull request.

    Searches for Jira issue key in:
    1. PR source branch name (e.g., feature/PROJ-1234/my-feature)
    2. PR title
    3. PR description

    Args:
        pull_request_id: Pull request ID
        config: Azure DevOps configuration (defaults to from_state)
        headers: Auth headers (defaults to get_auth_headers)

    Returns:
        Jira issue key (e.g., "PROJ-1234") if found, None otherwise.
    """
    from agentic_devtools.cli.jira.config import build_jira_issue_pattern, get_jira_project_keys

    # Pattern to match Jira issue keys - built from configured project keys
    jira_pattern = build_jira_issue_pattern(get_jira_project_keys())

    # Get full PR details
    pr_details = get_pull_request_details(pull_request_id, config, headers)
    if not pr_details:
        return None

    # 1. Check source branch first (most reliable)
    source_ref = pr_details.get("sourceRefName", "")
    branch_name = source_ref.replace("refs/heads/", "")
    if branch_name:
        match = jira_pattern.search(branch_name)
        if match:
            return match.group(1).upper()

    # 2. Check PR title
    title = pr_details.get("title", "")
    if title:
        match = jira_pattern.search(title)
        if match:
            return match.group(1).upper()

    # 3. Check PR description
    description = pr_details.get("description", "") or ""
    if description:
        match = jira_pattern.search(description)
        if match:
            return match.group(1).upper()

    return None


def find_pr_from_jira_issue(
    issue_key: str,
    config: AzureDevOpsConfig | None = None,
    headers: dict[str, str] | None = None,
    verbose: bool = False,
) -> int | None:
    """
    Find active PR from a Jira issue key.

    Searches multiple sources in order of reliability:
    1. Jira Development panel (most reliable - official Azure DevOps integration)
    2. Azure DevOps PRs where issue key appears in branch/title/description
    3. Jira issue comments/description for PR links (least reliable - text patterns)

    Args:
        issue_key: Jira issue key (e.g., "PROJ-1234")
        config: Azure DevOps configuration (defaults to from_state)
        headers: Auth headers (defaults to get_auth_headers)
        verbose: Whether to print debug output

    Returns:
        PR ID as integer if found, None otherwise.
    """
    # 1. First, try Jira Development panel (most reliable - official integration)
    try:
        from .review_jira import get_pr_from_development_panel

        dev_panel_pr_id = get_pr_from_development_panel(issue_key, verbose=verbose)
        if dev_panel_pr_id:
            if verbose:  # pragma: no cover
                print(f"Found PR #{dev_panel_pr_id} in Jira Development panel")
            return dev_panel_pr_id
    except Exception:
        # Development panel lookup failed, continue to ADO search
        pass

    # 2. Second, search Azure DevOps for PR with issue key in branch/title/description
    pr_data = find_pull_request_by_issue_key(issue_key, config, headers)
    if pr_data:
        pr_id = pr_data.get("pullRequestId")
        if pr_id:
            if verbose:  # pragma: no cover
                print(f"Found PR #{pr_id} via Azure DevOps search")
            return int(pr_id)

    # 3. Last resort: text pattern matching in Jira comments/description
    try:
        from .review_jira import get_linked_pull_request_from_jira

        jira_pr_id = get_linked_pull_request_from_jira(issue_key, verbose=verbose)
        if jira_pr_id:
            if verbose:  # pragma: no cover
                print(f"Found PR #{jira_pr_id} via text pattern in Jira")
            return jira_pr_id
    except Exception:  # pragma: no cover
        # Jira lookup failed
        pass

    return None


_SHORT_COMMIT_HASH_PATTERN = re.compile(r"^[0-9a-f]{12}$")
_REVIEW_ARTIFACT_DISCOVERY_MARKERS = ("manifest.json", "queue.json")


def _parse_pull_request_id_from_artifact_file(path: Path) -> int | None:
    """Return ``pullRequestId`` from a JSON artifact file when present and valid."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, UnicodeDecodeError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    raw_pr_id = payload.get("pullRequestId")
    if isinstance(raw_pr_id, bool) or not isinstance(raw_pr_id, int):
        return None
    return raw_pr_id


def _artifact_dir_matches_pull_request(entry: Path, pull_request_id: int) -> bool:
    """Return whether an artifact directory can be verified for ``pull_request_id`` ownership.

    Reads every readable ownership marker (``manifest.json``, ``queue.json``).  Returns
    ``True`` only when at least one marker is readable **and** every readable marker belongs
    to ``pull_request_id``.  Returns ``False`` when any readable marker belongs to a
    different PR, or when no marker is readable.
    """
    verified = False
    for artifact_name in _REVIEW_ARTIFACT_DISCOVERY_MARKERS:
        candidate_pr_id = _parse_pull_request_id_from_artifact_file(entry / artifact_name)
        if candidate_pr_id is None:
            continue
        if candidate_pr_id != pull_request_id:
            return False
        verified = True
    return verified


def _discover_commit_hash_short_fallback(pull_request_id: int, state_dir: Path) -> str | None:
    """Best-effort fallback discovery for absent/empty ``review.commit_hash_short``.

    Tier 1: delegates to :func:`~.review_state.derive_commit_hash_short`, which
    reads ``review-state.json`` under a shared sidecar lock.  Tier 2: scans
    committed artifact directories when tier 1 returns an empty string.
    """
    from .review_state import derive_commit_hash_short

    derived = derive_commit_hash_short(pull_request_id)
    if derived:
        return derived

    artifacts_root = state_dir / "pull-request-review"
    try:
        subdirs = list(artifacts_root.iterdir())
    except OSError:
        return None

    candidates: list[tuple[float, str]] = []
    for entry in subdirs:
        if not entry.is_dir():
            continue
        name = entry.name
        if not (is_safe_dir_segment(name) and _SHORT_COMMIT_HASH_PATTERN.fullmatch(name)):
            continue
        if not any((entry / marker).exists() for marker in _REVIEW_ARTIFACT_DISCOVERY_MARKERS):
            continue
        if not _artifact_dir_matches_pull_request(entry, pull_request_id):
            continue
        try:
            candidates.append((entry.stat().st_mtime, name))
        except OSError:
            continue

    if not candidates:
        return None
    candidates.sort(key=lambda pair: pair[0], reverse=True)
    return candidates[0][1]


def resolve_review_artifact_dir_name(
    pull_request_id: int,
    commit_hash_short: Any | None,
    warn: bool = True,
    allow_discovery: bool = True,
    backfill: bool = True,
) -> str:
    """Return a safe, ``str``-typed directory-name segment for scoping review artifacts.

    Reads *commit_hash_short* (already retrieved from state by the caller) and
    validates it with :func:`is_safe_dir_segment`. ``None`` and ``""`` are
    treated as absent before coercion; other values are coerced to ``str`` and
    a whitespace-only result is treated as absent. In absent cases, optionally
    attempts best-effort recovery from local review artifacts
    (``review-state.json`` and existing commit-scoped artifact directories) and
    backfills ``review.commit_hash_short`` in state.
    Falls back to ``'PR<pull_request_id>'`` (printing a warning to stderr when
    *warn* is ``True``) when no usable fallback can be discovered, when the
    explicit value is unsafe, or when it cannot be coerced to a plain ``str``.

    Pass ``warn=False`` from high-frequency callers (e.g. ``_get_queue_path``)
    to avoid spamming stderr on every queue operation when the key is absent.
    Pass ``allow_discovery=False`` for scaffold/setup paths that must avoid
    reusing stale prior-round artifact directories when ``commit_hash_short`` is
    absent.
    Pass ``backfill=False`` from dry-run callers to allow discovery (returning
    the candidate directory name) while suppressing the state-write side-effect
    that would mutate state even when no files are written.

    The returned value is always a plain :class:`str`, safe for direct use as a
    single :class:`pathlib.Path` segment without further coercion or validation.
    """
    fallback = f"PR{pull_request_id}"

    def _safe_repr(obj: Any) -> str:
        """Return a bounded, exception-safe repr for use in warning paths."""
        try:
            return reprlib.repr(obj)
        except Exception:
            return f"<unrepr:{type(obj).__name__}>"

    def _resolve_absent_hash() -> str:
        if not allow_discovery:
            if warn:
                print(
                    f"Warning: review.commit_hash_short not set; using {fallback!r} as artifact directory.",
                    file=sys.stderr,
                )
            return fallback
        candidate = _discover_commit_hash_short_fallback(pull_request_id, get_state_dir())
        if candidate is not None:
            resolved = candidate
            if backfill:
                try:
                    with read_modify_write_state() as _s:
                        review_state = _s.get("review")
                        if isinstance(review_state, dict):
                            raw_existing = review_state.get("commit_hash_short")
                            existing = raw_existing.strip() if isinstance(raw_existing, str) else ""
                            if existing and is_safe_dir_segment(existing):
                                resolved = existing
                                return resolved
                        else:
                            _s["review"] = {}
                        _s["review"]["commit_hash_short"] = candidate
                except Exception:
                    pass
            return resolved
        if warn:
            print(
                f"Warning: review.commit_hash_short not set; using {fallback!r} as artifact directory.",
                file=sys.stderr,
            )
        return fallback

    if commit_hash_short is None or commit_hash_short == "":
        return _resolve_absent_hash()
    try:
        as_str = str(commit_hash_short).strip()
    except Exception:
        if warn:
            print(
                "Warning: review.commit_hash_short "
                f"{_safe_repr(commit_hash_short)} could not be coerced to str; "
                f"using {fallback!r} as artifact directory.",
                file=sys.stderr,
            )
        return fallback
    if as_str == "":
        return _resolve_absent_hash()
    if not is_safe_dir_segment(as_str):
        if warn:
            print(
                "Warning: review.commit_hash_short "
                f"{_safe_repr(commit_hash_short)} is unsafe; "
                f"using {fallback!r} as artifact directory.",
                file=sys.stderr,
            )
        return fallback
    return as_str
