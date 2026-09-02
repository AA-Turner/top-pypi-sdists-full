"""Azure DevOps CI platform provider.

Implements ``parse_event()`` for ADO service hook payloads and
``delete_review_comments()`` for removing agentic-devtools review-scaffolding
comment threads via the Azure DevOps REST API. The remaining action methods are
stubs that raise ``NotImplementedError`` (the GitHub provider is the primary CI
implementation).
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, cast
from urllib.parse import quote, unquote

from agentic_devtools.cli.ci.exceptions import MalformedEventError
from agentic_devtools.cli.ci.models import (
    CheckRunStatus,
    EventPayload,
    FinalizationResult,
    IssueCommentInfo,
    IssueEvent,
    PRMetadata,
    ReviewCommentDeletionResult,
    ReviewCommentInfo,
    ReviewCommentTarget,
    ReviewInfo,
    SquashResult,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider

# Azure DevOps REST API version used for thread/comment operations. The
# connectionData endpoint returns HTTP 400 in some environments, so marker-based
# filtering (not authenticated-user resolution) is the default selection method.
_DELETE_API_VERSION = "7.1-preview.1"
_HTTP_TIMEOUT = 30
_SUCCESS_STATUS_CODES = (200, 204)


class AzureDevOpsProvider(CIPlatformProvider):
    """Azure DevOps CI platform provider implementation.

    Implements ``parse_event()`` for ADO service hook payloads and
    ``delete_review_comments()`` for review-scaffolding cleanup. Remaining
    CI-loop action methods are stubs that raise ``NotImplementedError``.
    """

    def __init__(self, organization: str = "", project: str = "", repository: str = "") -> None:
        """Initialize the Azure DevOps provider.

        Args:
            organization: Azure DevOps organization name or URL
                (e.g. ``"https://dev.azure.com/myorg"``).
            project: Azure DevOps project name.
            repository: Azure DevOps repository name (required by
                :meth:`delete_review_comments`).
        """
        self._organization = organization
        self._project = project
        self._repository = repository

    def parse_event(self, raw_payload: dict, event_name: str) -> EventPayload:
        """Parse an Azure DevOps service hook payload.

        Handles the ADO service hook JSON format for pull request events.

        Args:
            raw_payload: Raw JSON payload from the ADO service hook.
            event_name: Event type (e.g., "git.pullrequest.updated").

        Returns:
            Normalized EventPayload.

        Raises:
            MalformedEventError: If the payload cannot be parsed.
        """
        try:
            resource = raw_payload.get("resource", {})

            # ADO PR events have pullRequestId in the resource
            pr_id = resource.get("pullRequestId", 0)
            if isinstance(pr_id, str):
                pr_id = int(pr_id) if pr_id.isdigit() else 0

            # Extract branch info
            source_branch = resource.get("sourceRefName", "")
            target_branch = resource.get("targetRefName", "")
            # Strip refs/heads/ prefix
            if source_branch.startswith("refs/heads/"):
                source_branch = source_branch[len("refs/heads/") :]
            if target_branch.startswith("refs/heads/"):
                target_branch = target_branch[len("refs/heads/") :]

            # Extract commit SHA
            last_merge_source_commit = resource.get("lastMergeSourceCommit", {})
            head_sha = last_merge_source_commit.get("commitId", "")

            # Extract repository info
            repo_info = resource.get("repository", {})
            repo_name = repo_info.get("name", "")
            project_name = raw_payload.get("resourceContainers", {}).get("project", {}).get("id", "")
            full_name = f"{project_name}/{repo_name}" if project_name and repo_name else ""

            # Detect edit-change metadata for PR update events
            action = event_name
            title_changed = False
            body_changed = False
            base_changed = False
            edit_changes_known = False
            if event_name == "git.pullrequest.updated":
                action = "edited"
                # ADO includes a "changedFields" dict or per-field deltas in resource
                changed_fields = raw_payload.get("changedFields")
                edit_changes_known = isinstance(changed_fields, dict)
                if isinstance(changed_fields, dict):
                    title_changed = "title" in changed_fields or "Title" in changed_fields
                    body_changed = "description" in changed_fields or "Description" in changed_fields
                    base_changed = "targetRefName" in changed_fields or "TargetRefName" in changed_fields

            return EventPayload(
                pr_number=pr_id,
                head_branch=source_branch,
                head_sha=head_sha,
                base_branch=target_branch,
                action=action,
                repository_full_name=full_name,
                title_changed=title_changed,
                body_changed=body_changed,
                base_changed=base_changed,
                edit_changes_known=edit_changes_known,
            )
        except (TypeError, ValueError, AttributeError) as exc:
            raise MalformedEventError(event_name, str(exc)) from exc

    def delete_review_comments(
        self,
        pr_number: int,
        *,
        execute: bool = False,
        author_substring: str | None = None,
    ) -> ReviewCommentDeletionResult:
        """Delete agentic-devtools review-scaffolding comment threads on a PR.

        Lists every comment thread on *pr_number*, selects the deletable comments
        (``commentType == "text"`` carrying an ``agdt-review`` marker, plus an
        optional author-substring fallback), and either reports them (dry-run) or
        deletes them (``execute=True``).

        Args:
            pr_number: Pull request ID.
            execute: When ``False`` (default), perform a dry-run and return the
                comments that *would* be deleted. When ``True``, delete them.
            author_substring: Optional case-insensitive substring matched against
                each comment author's display/unique name as a fallback selector.

        Returns:
            A :class:`ReviewCommentDeletionResult` with the selected comments and,
            in execute mode, each comment's deletion outcome.
        """
        from agentic_devtools.cli.azure_devops.auth import get_auth_headers, get_pat
        from agentic_devtools.cli.azure_devops.helpers import get_repository_id, require_requests

        requests_module = require_requests()
        headers = get_auth_headers(get_pat())
        repo_id = get_repository_id(self._organization, self._project, self._repository)

        threads = self._list_threads(requests_module, headers, repo_id, pr_number)
        targets = _select_deletion_targets(threads, author_substring)

        if not execute:
            return ReviewCommentDeletionResult(executed=False, targets=tuple(targets))

        finalized: list[ReviewCommentTarget] = []
        for target in targets:
            try:
                response = self._delete_comment(requests_module, headers, repo_id, pr_number, target)
            # Continue through per-comment failures (for example network/request
            # exceptions from requests) so execute mode can report a full summary.
            except Exception as exc:  # noqa: BLE001
                finalized.append(replace(target, error=f"{type(exc).__name__}: {exc}"))
                continue
            if response.status_code in _SUCCESS_STATUS_CODES:
                finalized.append(replace(target, deleted=True))
            else:
                detail = (response.text or "").strip()
                error = f"HTTP {response.status_code}: {detail[:160]}" if detail else f"HTTP {response.status_code}"
                finalized.append(replace(target, error=error))
        return ReviewCommentDeletionResult(executed=True, targets=tuple(finalized))

    def _threads_url(self, repo_id: str, pr_number: int) -> str:
        """Build the PR threads collection URL."""
        org = self._organization.rstrip("/")
        project = quote(unquote(self._project), safe="")
        return (
            f"{org}/{project}/_apis/git/repositories/{repo_id}"
            f"/pullRequests/{pr_number}/threads?api-version={_DELETE_API_VERSION}"
        )

    def _comment_url(self, repo_id: str, pr_number: int, thread_id: int, comment_id: int) -> str:
        """Build the URL for a single PR comment."""
        org = self._organization.rstrip("/")
        project = quote(unquote(self._project), safe="")
        return (
            f"{org}/{project}/_apis/git/repositories/{repo_id}"
            f"/pullRequests/{pr_number}/threads/{thread_id}/comments/{comment_id}"
            f"?api-version={_DELETE_API_VERSION}"
        )

    def _list_threads(self, requests_module: Any, headers: dict[str, str], repo_id: str, pr_number: int) -> list[dict]:
        """Return all comment threads on the pull request."""
        response = requests_module.get(self._threads_url(repo_id, pr_number), headers=headers, timeout=_HTTP_TIMEOUT)
        if not 200 <= response.status_code < 300:
            detail = (response.text or "").strip()
            error = f"HTTP {response.status_code}: {detail[:160]}" if detail else f"HTTP {response.status_code}"
            raise RuntimeError(f"Failed to list PR threads for #{pr_number}: {error}")
        return response.json().get("value", []) or []

    def _delete_comment(
        self,
        requests_module: Any,
        headers: dict[str, str],
        repo_id: str,
        pr_number: int,
        target: ReviewCommentTarget,
    ) -> Any:
        """Delete a single PR comment and return the HTTP response."""
        url = self._comment_url(repo_id, pr_number, target.thread_id, target.comment_id)
        return requests_module.delete(url, headers=headers, timeout=_HTTP_TIMEOUT)

    def get_pr_metadata(self, pr_number: int) -> PRMetadata:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.get_pr_metadata() not yet implemented")

    def list_check_runs(self, head_sha: str) -> list[CheckRunStatus]:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.list_check_runs() not yet implemented")

    def list_reviews(self, pr_number: int) -> list[ReviewInfo]:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.list_reviews() not yet implemented")

    def post_comment(self, pr_number: int, body: str) -> int:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.post_comment() not yet implemented")

    def update_comment(self, comment_id: int, body: str) -> None:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.update_comment() not yet implemented")

    def find_comment(self, pr_number: int, marker: str) -> tuple[int, str] | None:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.find_comment() not yet implemented")

    def approve_pr(self, pr_number: int, head_sha: str, body: str) -> bool:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.approve_pr() not yet implemented")

    def merge_pr(self, pr_number: int, head_sha: str, method: str, *, commit_title: str | None = None) -> None:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.merge_pr() not yet implemented")

    def delete_branch(self, branch: str) -> None:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.delete_branch() not yet implemented")

    def publish_pr(self, pr_number: int) -> None:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.publish_pr() not yet implemented")

    def squash_before_publish(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> None:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.squash_before_publish() not yet implemented")

    def request_reviewer(self, pr_number: int, reviewer: str) -> None:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.request_reviewer() not yet implemented")

    def count_unresolved_review_threads(self, pr_number: int) -> int:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.count_unresolved_review_threads() not yet implemented")

    def list_pr_files(self, pr_number: int) -> list[str]:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.list_pr_files() not yet implemented")

    def get_check_annotations(self, check_run_id: int, limit: int) -> list[str]:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.get_check_annotations() not yet implemented")

    def dispatch_repair(
        self,
        pr_number: int,
        head_sha: str,
        repair_type: str,
        failed_checks: list[CheckRunStatus],
        review_comments: list[ReviewCommentInfo],
        review_id: int = 0,
        declared_author_comment_count: int = 0,
        declared_author_comment_counts_by_review: dict[int, int] | None = None,
    ) -> int:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.dispatch_repair() not yet implemented")

    def list_review_comments(self, pr_number: int, review_id: int) -> list[ReviewCommentInfo]:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.list_review_comments() not yet implemented")

    def list_issue_comments(self, pr_number: int) -> list[IssueCommentInfo]:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.list_issue_comments() not yet implemented")

    def finalize_post_repair(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
        review_id: int,
    ) -> FinalizationResult:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.finalize_post_repair() not yet implemented")

    def squash_post_repair(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> SquashResult:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.squash_post_repair() not yet implemented")

    def list_pr_issue_events(self, pr_number: int) -> list[IssueEvent]:
        """ADO does not support the GitHub Issues Events API — returns empty list."""
        return []

    def count_commits_behind(self, *, pr_number: int, base_branch: str, head_branch: str) -> int:
        """ADO stub — returns 0 (not yet implemented)."""
        return 0

    def rebase_onto_base(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> None:
        """Not implemented for ADO stub."""
        raise NotImplementedError("AzureDevOpsProvider.rebase_onto_base() not yet implemented")


def _select_deletion_targets(threads: list[dict], author_substring: str | None) -> list[ReviewCommentTarget]:
    """Select deletable comments from PR threads.

    A comment is selected when it is a non-deleted ``text`` comment AND either
    carries a valid ``agdt-review`` marker (the primary, default mechanism) or its
    author matches *author_substring* (the optional fallback). System, vote, and
    code-change comments cannot be deleted and are skipped.
    """
    from agentic_devtools.cli.azure_devops.marker import is_recognized_marker, parse_marker

    targets: list[ReviewCommentTarget] = []
    for thread in threads:
        if thread.get("isDeleted"):
            continue
        thread_id = cast(int, thread.get("id"))
        for comment in thread.get("comments") or []:
            if comment.get("isDeleted"):
                continue
            comment_type = comment.get("commentType")
            if comment_type != "text":
                continue
            content = comment.get("content") or ""
            parsed = parse_marker(content)
            marker_type = parsed.get("type") if parsed else None
            is_marker = is_recognized_marker(parsed)
            if not (is_marker or _author_matches(comment.get("author"), author_substring)):
                continue
            targets.append(
                ReviewCommentTarget(
                    thread_id=thread_id,
                    comment_id=cast(int, comment.get("id")),
                    comment_type=comment_type,
                    marker_type=marker_type if is_marker else None,
                    snippet=_first_line(content),
                )
            )
    return targets


def _author_matches(author: dict | None, author_substring: str | None) -> bool:
    """Return ``True`` when *author* matches the optional *author_substring* fallback."""
    if not author_substring:
        return False
    author = author or {}
    haystack = f"{author.get('displayName', '')} {author.get('uniqueName', '')}".lower()
    return author_substring.lower() in haystack


def _first_line(content: str) -> str:
    """Return a short, human-readable first line of *content* (marker stripped)."""
    from agentic_devtools.cli.azure_devops.marker import strip_marker_line

    body = strip_marker_line(content or "")
    for line in body.splitlines():
        text = line.strip()
        if text:
            return text[:80]
    return "(empty)"
