#!/usr/bin/env python3
"""Audit PR and issue evaluation cleanup automation script.

Posts structured evaluation comments to audit evaluation PRs and related tracking issues,
closes the PRs, deletes remote feature branches, and closes related issues.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
import tempfile
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, urlparse


class AuditCleanupError(Exception):
    """Domain exception raised when an audit cleanup operation fails."""


@dataclass
class AuditCleanupResult:
    """Execution status result of audit cleanup operations."""

    pr_number: int
    pr_commented: bool = False
    pr_closed: bool = False
    branch_deleted: bool = False
    issue_commented: bool = False
    issue_closed: bool = False
    success: bool = True
    error_message: str | None = None


_TRANSIENT_CODE_RE = re.compile(
    r"(?:https?[/ :]|status[: ]|error[: ]|\()\s*(?:code\s*)?(429|502|503|504)\b",
    re.IGNORECASE,
)
_REPOSITORY_OWNER = "swai-factory"
_REPOSITORY_NAME = "agentic-devtools"
_REPOSITORY = f"{_REPOSITORY_OWNER}/{_REPOSITORY_NAME}"
_REPOSITORY_ISSUE_PATH_RE = re.compile(rf"/{_REPOSITORY_OWNER}/{_REPOSITORY_NAME}/issues/(\d+)")
_REPOSITORY_ISSUE_PATH_PREFIX = f"/{_REPOSITORY_OWNER}/{_REPOSITORY_NAME}/issues/"
_TRANSIENT_KEYWORDS = (
    "timeout",
    "timed out",
    "connection reset",
    "econnreset",
    "etimedout",
    "socket hang up",
    "temporary failure",
    "server error",
    "service unavailable",
    "bad gateway",
    "too many requests",
    "rate limit",
)


def _validate_retry_settings(max_retries: int, retry_delay: float) -> None:
    """Validate retry configuration accepted by the public entry points."""
    if max_retries < 0:
        raise ValueError(f"max_retries cannot be negative, got {max_retries}")
    if not math.isfinite(retry_delay) or retry_delay < 0:
        raise ValueError(f"retry_delay must be finite and non-negative, got {retry_delay}")


def is_transient_error(stderr_or_msg: str, returncode: int = 0) -> bool:
    """Check if an error output indicates a transient network or server failure.

    Args:
        stderr_or_msg: Standard error text or exception message.
        returncode: Exit code from process.

    Returns:
        True if the error appears transient and retryable, False otherwise.
    """
    text = stderr_or_msg.lower()
    if _TRANSIENT_CODE_RE.search(text):
        return True
    for kw in _TRANSIENT_KEYWORDS:
        if kw in text:
            return True
    return False


def run_command(
    cmd: Sequence[str],
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> subprocess.CompletedProcess[str]:
    """Execute an external command securely with retry logic on transient errors.

    Args:
        cmd: Command and arguments sequence.
        dry_run: If True, simulate command without execution.
        max_retries: Maximum number of retry attempts for transient errors.
        retry_delay: Initial retry delay in seconds.

    Returns:
        subprocess.CompletedProcess instance.

    Raises:
        AuditCleanupError: If command execution fails after retries or with permanent error.
    """
    _validate_retry_settings(max_retries=max_retries, retry_delay=retry_delay)
    if dry_run:
        return subprocess.CompletedProcess(
            args=list(cmd),
            returncode=0,
            stdout="[DRY-RUN] Command simulated successfully.",
            stderr="",
        )

    attempts = max_retries + 1
    last_error = ""

    for attempt in range(attempts):  # pragma: no branch
        try:
            result = subprocess.run(
                list(cmd),
                capture_output=True,
                text=True,
                shell=False,
                check=False,
            )
            if result.returncode == 0:
                return result

            last_error = result.stderr.strip() or result.stdout.strip() or f"Exit code {result.returncode}"
            if is_transient_error(last_error, result.returncode) and attempt < attempts - 1:
                if retry_delay > 0:
                    time.sleep(retry_delay * (2**attempt))
                continue

            raise AuditCleanupError(f"Command failed ({result.returncode}): {' '.join(cmd)}\n{last_error}")
        except OSError as exc:
            raise AuditCleanupError(f"Command launch error: {' '.join(cmd)}\n{exc}") from exc
        except subprocess.SubprocessError as exc:
            last_error = str(exc)
            if attempt < attempts - 1:
                if retry_delay > 0:
                    time.sleep(retry_delay * (2**attempt))
                continue
            raise AuditCleanupError(f"Process execution error: {' '.join(cmd)}\n{last_error}") from exc

    raise AuditCleanupError(
        f"Command failed after {attempts} attempts: {' '.join(cmd)}\n{last_error}"
    )  # pragma: no cover


def read_comment_content(
    comment_file: str | None = None,
    comment: str | None = None,
) -> str:
    """Resolve and read comment text from a file path or direct string.

    Args:
        comment_file: Optional path to markdown comment file.
        comment: Optional direct string comment.

    Returns:
        Comment string content.

    Raises:
        FileNotFoundError: If comment_file does not exist.
        ValueError: If neither comment_file nor comment is provided or content is empty.
    """
    if comment_file:
        path = Path(comment_file)
        if not path.is_file():
            raise FileNotFoundError(f"Comment file not found: {comment_file}")
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            raise ValueError(f"Comment file is empty: {comment_file}")
        return content

    if comment is not None:
        content = comment.strip()
        if not content:
            raise ValueError("Comment string cannot be empty.")
        return content

    raise ValueError("Either comment_file or comment must be provided.")


def normalize_issue_number(issue_ref: int | str) -> int:
    """Normalize issue reference string or integer into a clean issue number.

    Accepts plain integers, ``#NNN`` strings, and GitHub issue URLs for the
    current repository (``https://github.com/swai-factory/agentic-devtools/issues/<number>``).
    Any other format is rejected to prevent accidental mutation of unrelated issues.

    Args:
        issue_ref: Issue number integer, "#123", or GitHub issue URL.

    Returns:
        Positive integer issue number.

    Raises:
        ValueError: If issue_ref cannot be parsed to a positive integer.
    """
    if isinstance(issue_ref, bool):
        raise ValueError(f"Issue number must be an integer, got bool: {issue_ref}")
    if isinstance(issue_ref, int):
        if issue_ref <= 0:
            raise ValueError(f"Issue number must be positive, got {issue_ref}")
        return issue_ref

    cleaned = str(issue_ref).strip()

    # Accept plain number or #NNN (exact match only)
    m = re.fullmatch(r"#?(\d+)", cleaned)
    if m:
        val = int(m.group(1))
        if val <= 0:
            raise ValueError(f"Issue number must be positive, got {val}")
        return val

    parsed = urlparse(cleaned)
    if parsed.scheme in {"http", "https"}:
        if parsed.netloc.lower() != "github.com":
            raise ValueError(f"Unsupported issue URL host in '{issue_ref}'")
        if not parsed.path.startswith(_REPOSITORY_ISSUE_PATH_PREFIX):
            raise ValueError(f"Unsupported issue URL repository in '{issue_ref}'")
        url_m = _REPOSITORY_ISSUE_PATH_RE.fullmatch(parsed.path)
        if url_m is None:
            raise ValueError(f"Unsupported issue URL path in '{issue_ref}'")
        val = int(url_m.group(1))
        if val <= 0:
            raise ValueError(f"Issue number must be positive, got {val}")
        return val

    raise ValueError(f"Could not parse issue number from '{issue_ref}'")


def get_pr_head_branch(
    pr_number: int,
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> str | None:
    """Retrieve the head branch name for a given pull request.

    Args:
        pr_number: GitHub pull request number.
        dry_run: If True, return synthetic branch name.
        max_retries: Maximum retry attempts for transient errors.
        retry_delay: Initial retry backoff delay in seconds.

    Returns:
        Branch name string, or None if not found.
    """
    if dry_run:
        return "synthetic-branch-dry-run"

    cmd = [
        "gh",
        "pr",
        "view",
        str(pr_number),
        "--repo",
        _REPOSITORY,
        "--json",
        "headRefName,isCrossRepository",
    ]
    result = run_command(
        cmd,
        dry_run=False,
        max_retries=max_retries,
        retry_delay=retry_delay,
    )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AuditCleanupError(
            f"Could not parse PR metadata for PR #{pr_number}: {result.stdout.strip() or '<empty>'}"
        ) from exc
    if not isinstance(payload, dict):
        raise AuditCleanupError(f"Unexpected PR metadata payload for PR #{pr_number}")
    if payload.get("isCrossRepository") is not False:
        raise AuditCleanupError(f"Refusing to delete the head branch for cross-repository PR #{pr_number}")
    branch = payload.get("headRefName")
    if not isinstance(branch, str):
        return None
    branch = branch.strip()
    return branch if branch else None


def _run_comment_command(
    command_prefix: Sequence[str],
    comment: str,
    dry_run: bool = False,
) -> None:
    """Run a ``gh`` comment command with the body stored in a temporary file.

    Comment creation is non-idempotent: retries after an ambiguous response
    (timeout, 502, 503) would post duplicate comments.  Retries are therefore
    disabled unconditionally for all comment commands.

    Args:
        command_prefix: ``gh`` command arguments before the body flag.
        comment: Markdown comment body.
        dry_run: If True, simulate operation.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as handle:
        handle.write(comment)
        body_file = handle.name

    try:
        run_command(
            [*command_prefix, "--body-file", body_file],
            dry_run=dry_run,
            max_retries=0,
            retry_delay=0.0,
        )
    finally:
        Path(body_file).unlink(missing_ok=True)


def _comment_marker_exists(
    thread_number: int,
    marker: str,
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> bool:
    """Return True when an issue/PR discussion already contains ``marker``."""
    if dry_run:
        return False

    result = run_command(
        ["gh", "api", "--paginate", f"repos/{_REPOSITORY}/issues/{thread_number}/comments"],
        dry_run=False,
        max_retries=max_retries,
        retry_delay=retry_delay,
    )
    raw_payload = result.stdout.strip()
    if not raw_payload:
        raise AuditCleanupError(f"Empty response for comments on thread #{thread_number}")
    payload: list[object] = []
    try:
        decoder = json.JSONDecoder()
        idx = 0
        length = len(raw_payload)
        while idx < length:
            while idx < length and raw_payload[idx] in " \t\n\r":
                idx += 1
            if idx >= length:  # pragma: no cover - raw_payload is stripped first
                break
            page, idx = decoder.raw_decode(raw_payload, idx)
            if not isinstance(page, list):
                raise AuditCleanupError(f"Unexpected comments payload for thread #{thread_number}")
            payload.extend(page)
    except json.JSONDecodeError as exc:
        raise AuditCleanupError(
            f"Could not parse existing comments for thread #{thread_number}: {result.stdout.strip() or '<empty>'}"
        ) from exc

    for entry in payload:
        if not isinstance(entry, dict):
            raise AuditCleanupError(f"Unexpected comment entry payload for thread #{thread_number}")
        body = entry.get("body")
        if isinstance(body, str) and marker in body:
            return True
    return False


def post_pr_comment(
    pr_number: int,
    comment: str,
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> bool:
    """Post an evaluation comment on a pull request.

    Comment creation is non-idempotent, so retries are disabled. If a prior
    run already posted the same comment body (identified by a deterministic
    hidden marker), this becomes a no-op instead of posting a duplicate.

    Args:
        pr_number: GitHub pull request number.
        comment: Markdown comment body.
        dry_run: If True, simulate operation.
        max_retries: Maximum retry attempts for the pre-post marker lookup.
        retry_delay: Initial retry backoff delay for the pre-post marker lookup.

    Returns:
        True when a new comment was posted, False when the marker already
        existed and no mutation was performed.
    """
    comment = comment.rstrip()
    marker = f"<!-- audit-pr-cleanup:pr:{pr_number}:{hashlib.sha256(comment.encode('utf-8')).hexdigest()[:16]} -->"
    if _comment_marker_exists(
        pr_number,
        marker=marker,
        dry_run=dry_run,
        max_retries=max_retries,
        retry_delay=retry_delay,
    ):
        return False
    _run_comment_command(
        ["gh", "pr", "comment", str(pr_number), "--repo", _REPOSITORY],
        comment=f"{comment}\n\n{marker}",
        dry_run=dry_run,
    )
    return True


def close_pr(
    pr_number: int,
    delete_branch: bool = False,
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> None:
    """Close a pull request and optionally delete its head branch.

    Args:
        pr_number: GitHub pull request number.
        delete_branch: If True, include --delete-branch flag.
        dry_run: If True, simulate operation.
        max_retries: Maximum retry attempts for transient errors.
        retry_delay: Initial retry backoff delay in seconds.
    """
    cmd = ["gh", "pr", "close", str(pr_number), "--repo", _REPOSITORY]
    if delete_branch:
        cmd.append("--delete-branch")
    try:
        run_command(cmd, dry_run=dry_run, max_retries=max_retries, retry_delay=retry_delay)
    except AuditCleanupError as exc:
        if "already closed" in str(exc).lower() or "not open" in str(exc).lower():
            return
        raise


def delete_remote_branch(
    branch_name: str,
    remote: str = "origin",
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> None:
    """Delete a remote branch from the scoped GitHub repository.

    Args:
        branch_name: Name of remote branch to delete.
        remote: Deprecated compatibility argument; ignored.
        dry_run: If True, simulate operation.
        max_retries: Maximum retry attempts for transient errors.
        retry_delay: Initial retry backoff delay in seconds.
    """
    if not branch_name.strip():
        raise ValueError("Branch name cannot be empty.")
    encoded_branch = quote(branch_name.strip(), safe="")
    cmd = ["gh", "api", "--method", "DELETE", f"repos/{_REPOSITORY}/git/refs/heads/{encoded_branch}"]
    try:
        run_command(cmd, dry_run=dry_run, max_retries=max_retries, retry_delay=retry_delay)
    except AuditCleanupError as exc:
        error_text = str(exc).lower()
        if (
            "remote ref does not exist" in error_text
            or "couldn't find remote ref" in error_text
            or "reference does not exist" in error_text
        ):
            return
        raise


def post_issue_comment(
    issue_number: int | str,
    comment: str,
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> bool:
    """Post an evaluation comment on a tracking issue.

    Comment creation is non-idempotent, so retries are disabled. If a prior
    run already posted the same comment body (identified by a deterministic
    hidden marker), this becomes a no-op instead of posting a duplicate.

    Args:
        issue_number: Tracking issue number or reference.
        comment: Markdown comment body.
        dry_run: If True, simulate operation.
        max_retries: Maximum retry attempts for the pre-post marker lookup.
        retry_delay: Initial retry backoff delay for the pre-post marker lookup.

    Returns:
        True when a new comment was posted, False when the marker already
        existed and no mutation was performed.
    """
    num = normalize_issue_number(issue_number)
    comment = comment.rstrip()
    marker = f"<!-- audit-pr-cleanup:issue:{num}:{hashlib.sha256(comment.encode('utf-8')).hexdigest()[:16]} -->"
    if _comment_marker_exists(
        num,
        marker=marker,
        dry_run=dry_run,
        max_retries=max_retries,
        retry_delay=retry_delay,
    ):
        return False
    _run_comment_command(
        ["gh", "issue", "comment", str(num), "--repo", _REPOSITORY],
        comment=f"{comment}\n\n{marker}",
        dry_run=dry_run,
    )
    return True


def close_issue(
    issue_number: int | str,
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> None:
    """Close a tracking issue.

    Args:
        issue_number: Tracking issue number or reference.
        dry_run: If True, simulate operation.
        max_retries: Maximum retry attempts for transient errors.
        retry_delay: Initial retry backoff delay in seconds.
    """
    num = normalize_issue_number(issue_number)
    cmd = ["gh", "issue", "close", str(num), "--repo", _REPOSITORY]
    try:
        run_command(cmd, dry_run=dry_run, max_retries=max_retries, retry_delay=retry_delay)
    except AuditCleanupError as exc:
        if "already closed" in str(exc).lower():
            return
        raise


def is_pr_closed(
    pr_number: int,
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> bool:
    """Return True when the pull request state is closed.

    In dry-run mode this returns True without remote verification.
    """
    if dry_run:
        return True
    cmd = ["gh", "pr", "view", str(pr_number), "--repo", _REPOSITORY, "--json", "state"]
    result = run_command(cmd, dry_run=False, max_retries=max_retries, retry_delay=retry_delay)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AuditCleanupError(
            f"Could not parse PR state for PR #{pr_number}: {result.stdout.strip() or '<empty>'}"
        ) from exc
    if not isinstance(payload, dict):
        raise AuditCleanupError(f"Unexpected PR state payload for PR #{pr_number}")
    state = payload.get("state")
    return isinstance(state, str) and state.upper() in {"CLOSED", "MERGED"}


def is_issue_closed(
    issue_number: int | str,
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> bool:
    """Return True when the issue state is closed.

    In dry-run mode this returns True without remote verification.
    """
    if dry_run:
        return True
    num = normalize_issue_number(issue_number)
    cmd = ["gh", "issue", "view", str(num), "--repo", _REPOSITORY, "--json", "state"]
    result = run_command(cmd, dry_run=False, max_retries=max_retries, retry_delay=retry_delay)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AuditCleanupError(
            f"Could not parse issue state for issue #{num}: {result.stdout.strip() or '<empty>'}"
        ) from exc
    if not isinstance(payload, dict):
        raise AuditCleanupError(f"Unexpected issue state payload for issue #{num}")
    state = payload.get("state")
    return isinstance(state, str) and state.upper() == "CLOSED"


def branch_exists(
    branch_name: str,
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> bool:
    """Return True when the remote branch still exists in the scoped repository.

    In dry-run mode this returns False without remote verification.
    """
    if dry_run:
        return False
    if not branch_name.strip():
        raise ValueError("Branch name cannot be empty.")
    encoded_branch = quote(branch_name.strip(), safe="")
    cmd = ["gh", "api", f"repos/{_REPOSITORY}/git/ref/heads/{encoded_branch}"]
    try:
        run_command(cmd, dry_run=False, max_retries=max_retries, retry_delay=retry_delay)
    except AuditCleanupError as exc:
        error_text = str(exc).lower()
        if "reference does not exist" in error_text or "no ref found for" in error_text:
            return False
        if "not found" in error_text:
            run_command(
                ["gh", "api", f"repos/{_REPOSITORY}"],
                dry_run=False,
                max_retries=max_retries,
                retry_delay=retry_delay,
            )
            return False
        raise
    return True


def cleanup_audit_pr(
    pr_number: int,
    comment: str,
    related_issue: int | str | None = None,
    issue_comment: str | None = None,
    delete_branch: bool = False,
    dry_run: bool = False,
    max_retries: int = 3,
    retry_delay: float = 0.0,
) -> AuditCleanupResult:
    """Execute end-to-end evaluation cleanup for an audit PR and optional issue.

    Args:
        pr_number: Pull request number.
        comment: Comment body for pull request.
        related_issue: Optional related tracking issue.
        issue_comment: Optional comment body for tracking issue (defaults to PR comment).
        delete_branch: If True, delete the PR's remote head branch.
        dry_run: If True, simulate all operations without making changes.
        max_retries: Maximum retry attempts for network operations.
        retry_delay: Initial backoff delay for retries.

    Returns:
        AuditCleanupResult containing status of each operation.

    Raises:
        ValueError: If pr_number is invalid or comment is empty.
        AuditCleanupError: If any sub-operation fails.
    """
    if not isinstance(pr_number, int) or isinstance(pr_number, bool):
        raise ValueError(f"PR number must be an integer, got {type(pr_number).__name__}")
    if pr_number <= 0:
        raise ValueError(f"PR number must be positive, got {pr_number}")
    if not comment.strip():
        raise ValueError("PR comment text cannot be empty.")
    _validate_retry_settings(max_retries=max_retries, retry_delay=retry_delay)

    normalized_issue: int | None = None
    resolved_issue_comment: str | None = None
    if issue_comment is not None and related_issue is None:
        raise ValueError("issue_comment requires related_issue to be set.")
    if related_issue is not None:
        normalized_issue = normalize_issue_number(related_issue)
        resolved_issue_comment = issue_comment if issue_comment is not None else comment
        if not resolved_issue_comment.strip():
            raise ValueError("issue_comment text cannot be empty or whitespace.")

    result = AuditCleanupResult(pr_number=pr_number)

    # Step 1: Resolve the head branch before mutating the PR when deletion is requested
    head_branch: str | None = None
    if delete_branch:
        head_branch = get_pr_head_branch(
            pr_number,
            dry_run=dry_run,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )
        if head_branch is None:
            result.success = False
            result.error_message = (
                f"PR #{pr_number}: branch deletion requested but head branch name "
                "could not be resolved — refusing to proceed without a verified branch target"
            )
            return result

    # Step 2: Post PR evaluation comment
    result.pr_commented = post_pr_comment(
        pr_number=pr_number,
        comment=comment,
        dry_run=dry_run,
        max_retries=max_retries,
        retry_delay=retry_delay,
    )

    # Step 3: Close the PR
    close_pr(
        pr_number=pr_number,
        dry_run=dry_run,
        max_retries=max_retries,
        retry_delay=retry_delay,
    )
    result.pr_closed = is_pr_closed(
        pr_number=pr_number,
        dry_run=dry_run,
        max_retries=max_retries,
        retry_delay=retry_delay,
    )
    if not result.pr_closed:
        result.success = False
        result.error_message = f"PR #{pr_number} is still open after close attempt"
        return result

    # Step 4: Delete branch explicitly so the flag reflects the actual outcome
    if delete_branch and head_branch:
        delete_remote_branch(
            branch_name=head_branch,
            dry_run=dry_run,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )
        result.branch_deleted = not branch_exists(
            branch_name=head_branch,
            dry_run=dry_run,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )
        if not result.branch_deleted:
            result.success = False
            result.error_message = f"branch '{head_branch}' still exists after delete attempt"
            return result

    # Step 5: Handle related issue if provided
    if normalized_issue is not None and resolved_issue_comment is not None:
        result.issue_commented = post_issue_comment(
            issue_number=normalized_issue,
            comment=resolved_issue_comment,
            dry_run=dry_run,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

        close_issue(
            issue_number=normalized_issue,
            dry_run=dry_run,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )
        result.issue_closed = is_issue_closed(
            issue_number=normalized_issue,
            dry_run=dry_run,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

    failures: list[str] = []
    if normalized_issue is not None and not result.issue_closed:
        failures.append(f"issue #{normalized_issue} is still open after close attempt")
    if failures:
        result.success = False
        result.error_message = "; ".join(failures)

    return result


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for audit PR cleanup.

    Args:
        args: Optional list of CLI argument strings.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Audit PR and issue evaluation cleanup script.",
    )
    parser.add_argument(
        "--pr-number",
        type=int,
        required=True,
        help="Pull request number to evaluate and clean up.",
    )
    comment_group = parser.add_mutually_exclusive_group(required=True)
    comment_group.add_argument(
        "--comment-file",
        type=str,
        default=None,
        help="Path to markdown file containing the PR evaluation comment.",
    )
    comment_group.add_argument(
        "--comment",
        type=str,
        default=None,
        help="Direct comment text for the PR evaluation.",
    )
    parser.add_argument(
        "--related-issue",
        type=str,
        default=None,
        help="Related tracking issue number (e.g. 3881 or #3881).",
    )
    issue_comment_group = parser.add_mutually_exclusive_group(required=False)
    issue_comment_group.add_argument(
        "--issue-comment-file",
        type=str,
        default=None,
        help="Path to markdown file containing the issue evaluation comment.",
    )
    issue_comment_group.add_argument(
        "--issue-comment",
        type=str,
        default=None,
        help="Direct comment text for the issue evaluation.",
    )
    parser.add_argument(
        "--delete-branch",
        action="store_true",
        default=False,
        help="Delete remote head branch when closing PR.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Simulate all operations without performing actual GitHub or Git mutations.",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum retry attempts for transient network errors (default: 3).",
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=1.0,
        help="Initial retry delay in seconds (default: 1.0).",
    )
    parsed = parser.parse_args(args)
    try:
        _validate_retry_settings(max_retries=parsed.max_retries, retry_delay=parsed.retry_delay)
    except ValueError as exc:
        parser.error(str(exc).replace("max_retries", "--max-retries").replace("retry_delay", "--retry-delay"))
    if (parsed.issue_comment_file is not None or parsed.issue_comment is not None) and not parsed.related_issue:
        parser.error("--issue-comment-file and --issue-comment require --related-issue")
    return parsed


def main(args: Sequence[str] | None = None) -> int:
    """Entry point for CLI execution.

    Args:
        args: Optional list of CLI argument strings.

    Returns:
        0 on success, 1 on runtime/cleanup errors. Invalid CLI usage raises
        ``SystemExit(2)`` via ``argparse`` before this function can return.
    """
    try:
        parsed = parse_args(args)
        pr_comment = read_comment_content(
            comment_file=parsed.comment_file,
            comment=parsed.comment,
        )

        issue_comment: str | None = None
        if parsed.related_issue:
            if parsed.issue_comment_file is not None or parsed.issue_comment is not None:
                issue_comment = read_comment_content(
                    comment_file=parsed.issue_comment_file,
                    comment=parsed.issue_comment,
                )
            else:
                issue_comment = pr_comment

        result = cleanup_audit_pr(
            pr_number=parsed.pr_number,
            comment=pr_comment,
            related_issue=parsed.related_issue,
            issue_comment=issue_comment,
            delete_branch=parsed.delete_branch,
            dry_run=parsed.dry_run,
            max_retries=parsed.max_retries,
            retry_delay=parsed.retry_delay,
        )

        mode_str = "[DRY-RUN] " if parsed.dry_run else ""
        issue_display = str(normalize_issue_number(parsed.related_issue)) if parsed.related_issue else ""
        if not result.success:
            print(f"Error: postcondition check failed — {result.error_message}", file=sys.stderr)
            return 1
        print(f"{mode_str}Successfully processed cleanup for PR #{result.pr_number}.")
        if result.pr_commented:
            print(f"{mode_str}- PR #{result.pr_number} comment posted.")
        if result.pr_closed:
            print(f"{mode_str}- PR #{result.pr_number} closed.")
        if result.branch_deleted:
            print(f"{mode_str}- PR #{result.pr_number} branch deleted.")
        if result.issue_commented and parsed.related_issue:
            print(f"{mode_str}- Issue #{issue_display} comment posted.")
        if result.issue_closed and parsed.related_issue:
            print(f"{mode_str}- Issue #{issue_display} closed.")

        return 0

    except Exception as exc:
        print(f"Error during audit cleanup: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
