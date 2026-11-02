"""Provider-neutral pull-request details retrieval."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, cast

from agentic_devtools.adapters.base import is_valid_github_repository
from agentic_devtools.cli.ci.credential_roles import (
    DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,
    require_default_repo_workflow_token,
)
from agentic_devtools.cli.ci.github_provider import (
    _SYNTHETIC_THREAD_KEY_PREFIX,
    GitHubActionsProvider,
    _gh_api,
    _parse_paginated_json,
)
from agentic_devtools.cli.ci.retry import RetryableError, retry_with_backoff

_PROVIDERS = frozenset({"azure_devops", "github"})
_GITHUB_PR_DIFF_FILE_LIMIT = 300


def _state_value(state: Mapping[str, Any] | None, *keys: str) -> object:
    for key in keys:
        current: object = state
        for part in key.split("."):
            if not isinstance(current, Mapping):
                current = None
                break
            current = current.get(part)
        if current is not None:
            return current
    return None


def _deep_merge_state(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """Recursively merge ``override`` onto ``base`` without discarding sibling nested keys."""
    merged: dict[str, Any] = dict(base)
    for key, value in override.items():
        existing = merged.get(key)
        if isinstance(value, Mapping) and isinstance(existing, Mapping):
            merged[key] = _deep_merge_state(existing, value)
        else:
            merged[key] = value
    return merged


def detect_provider(
    explicit: str | None = None,
    state: Mapping[str, Any] | None = None,
    repository: str | None = None,
    *,
    allow_remote: bool = True,
) -> str:
    """Resolve provider from explicit input, configured context, or the checkout remote."""
    selected = (
        explicit
        if explicit is not None
        else _state_value(state, "platform.code_hosting", "provider", "github.provider")
    )
    if selected is not None:
        if not isinstance(selected, str) or selected.strip().lower() not in _PROVIDERS:
            raise ValueError(
                "Provider must be 'azure_devops' or 'github'; configure a provider or use a supported origin remote"
            )
        return selected.strip().lower()

    if isinstance(repository, str) and is_valid_github_repository(repository):
        return "github"

    organization = _state_value(state, "organization", "azure_devops.organization")
    project = _state_value(state, "project", "azure_devops.project")
    has_azure_context = (
        isinstance(organization, str)
        and bool(organization.strip())
        and isinstance(project, str)
        and bool(project.strip())
    )
    github_repository = _state_value(state, "github.repo")
    has_github_context = isinstance(github_repository, str) and is_valid_github_repository(github_repository)
    if has_azure_context and not has_github_context:
        return "azure_devops"
    if has_github_context and not has_azure_context:
        return "github"

    if allow_remote:
        from agentic_devtools.cli.azure_devops.config import get_azure_devops_context_from_git_remote

        if get_azure_devops_context_from_git_remote() is not None:
            return "azure_devops"

        from agentic_devtools.cli.github.repo_resolution import _resolve_repo_from_git_remote

        if _resolve_repo_from_git_remote() is not None:
            return "github"

    raise ValueError("Provider must be configured or inferable from a GitHub/Azure DevOps context or origin remote")


def _github_api_json(endpoint: str, *, paginate: bool = False) -> Any:
    token = require_default_repo_workflow_token("retrieve pull request details")
    if not paginate:

        @retry_with_backoff()
        def _fetch_raw() -> str:
            return _gh_api(
                endpoint,
                paginate=False,
                include_headers=False,
                token=token,
                credential_identity=DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,
            )

        raw = _fetch_raw()
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"GitHub returned invalid JSON for {endpoint}") from exc

    # Paginated endpoints share a single retry budget across the raw transport
    # fetch and the JSON parse: a persistent transient failure should exhaust
    # at most one set of backoff attempts, not one set per layer.
    @retry_with_backoff()
    def _fetch_and_parse_paginated() -> Any:
        raw = _gh_api(
            endpoint,
            paginate=True,
            include_headers=False,
            token=token,
            credential_identity=DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,
        )
        try:
            return _parse_paginated_json(raw)
        except json.JSONDecodeError as exc:
            raise RetryableError(f"GitHub returned invalid JSON for {endpoint}") from exc

    try:
        return _fetch_and_parse_paginated()
    except RetryableError as exc:
        raise RuntimeError(str(exc)) from exc


def _json_value(value: Any) -> Any:
    return asdict(cast(Any, value)) if is_dataclass(value) else value


_HUNK_HEADER_RE = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def _parse_github_patch(patch: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Parse a GitHub per-file unified-diff ``patch`` into added/removed line entries.

    Mirrors the ``{"line": <int>, "content": <str>}`` shape produced by the Azure
    DevOps adapter (``pull_request_details_commands.py``) so downstream consumers
    such as ``_added_text_lines()`` in the manifest builder work identically
    regardless of provider. Unlike a full ``git diff``, GitHub's per-file patch has
    no ``diff --git``/``---``/``+++`` header lines — it starts directly with hunk
    headers — so every line is either a hunk header or hunk content.
    """
    added: list[dict[str, Any]] = []
    removed: list[dict[str, Any]] = []
    old_line = 0
    new_line = 0
    for raw_line in patch.split("\n"):
        match = _HUNK_HEADER_RE.match(raw_line)
        if match:
            old_line = int(match.group(1))
            new_line = int(match.group(2))
            continue
        if raw_line.startswith("+"):
            added.append({"line": new_line, "content": raw_line[1:]})
            new_line += 1
        elif raw_line.startswith("-"):
            removed.append({"line": old_line, "content": raw_line[1:]})
            old_line += 1
        elif raw_line.startswith("\\"):
            # e.g. "\ No newline at end of file" — not a real diff line.
            continue
        elif raw_line.startswith(" "):
            old_line += 1
            new_line += 1
    return added, removed


def _github_change_type(status: str) -> str:
    lowered_status = status.lower()
    if lowered_status in {"added", "copied"}:
        return "add"
    if lowered_status == "removed":
        return "delete"
    if lowered_status == "renamed":
        return "rename"
    return "edit"


def _github_details(pull_request_id: int, repository: str) -> dict[str, Any]:
    """Build normalized GitHub PR details.

    ``githubThreadNodeId`` preserves the opaque GraphQL thread ID as a string;
    it is distinct from REST comment database IDs.
    """
    token = require_default_repo_workflow_token("retrieve pull request details")
    provider = GitHubActionsProvider(repo=repository, token=token)
    metadata = _github_api_json(f"/repos/{repository}/pulls/{pull_request_id}")
    commits = _github_api_json(f"/repos/{repository}/pulls/{pull_request_id}/commits", paginate=True)
    files = _github_api_json(f"/repos/{repository}/pulls/{pull_request_id}/files", paginate=True)
    if not isinstance(commits, list):
        raise RuntimeError(
            f"GitHub returned an invalid commits response for pull request {pull_request_id}: "
            f"expected a list, got {type(commits).__name__}"
        )
    if not isinstance(files, list):
        raise RuntimeError(
            f"GitHub returned an invalid files response for pull request {pull_request_id}: "
            f"expected a list, got {type(files).__name__}"
        )
    if isinstance(metadata, Mapping):
        raw_commit_count = metadata.get("commits")
        if (
            isinstance(raw_commit_count, int)
            and not isinstance(raw_commit_count, bool)
            and len(commits) < raw_commit_count
        ):
            # GitHub's pull-request commits endpoint caps responses at 250 commits
            # regardless of pagination, so a short list would produce incomplete
            # review metadata.
            raise RuntimeError(
                f"GitHub reported {raw_commit_count} commit(s) for pull request {pull_request_id} but "
                f"the commits endpoint returned only {len(commits)}; refusing to persist an incomplete commit list"
            )
    if isinstance(metadata, Mapping):
        raw_changed_files = metadata.get("changed_files")
        if (
            isinstance(raw_changed_files, int)
            and not isinstance(raw_changed_files, bool)
            and len(files) < raw_changed_files
        ):
            # GitHub's /pulls/{id}/files endpoint caps responses at 3000 files
            # regardless of pagination, so a short list here means the manifest
            # would silently omit changed files. Fail explicitly rather than
            # persist an incomplete artifact that downstream review tooling
            # would treat as the full changeset.
            raise RuntimeError(
                f"GitHub reported {raw_changed_files} changed file(s) for pull request {pull_request_id} but "
                f"the files endpoint returned only {len(files)}; refusing to persist an incomplete file list"
            )
    diff_complete = len(files) <= _GITHUB_PR_DIFF_FILE_LIMIT
    reviews = [_json_value(review) for review in provider.list_reviews(pull_request_id)]
    all_comments = provider.list_all_review_comments(pull_request_id)
    comments_by_id = {comment.id: comment for comment in all_comments}
    emitted_comment_ids: set[int] = set()
    threads = provider.list_review_threads_by_thread_id(pull_request_id)
    thread_states = {key: {"resolved": value[0], "commentIds": list(value[1])} for key, value in threads.items()}
    normalized_threads: list[dict[str, Any]] = []
    for thread_id, state in thread_states.items():
        resolved = bool(state.get("resolved"))
        comment_ids = cast(list[Any], state.get("commentIds", []))
        comments: list[dict[str, Any]] = []
        for comment_id in comment_ids:
            comment = comments_by_id.get(comment_id)
            if comment is None:
                continue
            emitted_comment_ids.add(comment_id)
            comment_entry = {
                "id": comment.id,
                "content": comment.body,
                "isDeleted": False,
                "path": comment.path,
                "line": comment.line,
                "startLine": comment.start_line,
                "commitId": comment.commit_id,
                "originalCommitId": comment.original_commit_id,
                "htmlUrl": getattr(comment, "html_url", ""),
                "inReplyToId": getattr(comment, "in_reply_to_id", None),
                "createdAt": getattr(comment, "created_at", ""),
                "author": {
                    "displayName": comment.author_login,
                    "uniqueName": comment.author_login,
                },
            }
            if comment.path:
                comment_entry["threadContext"] = {"filePath": comment.path}
                comment_entry["pullRequestThreadContext"] = {"filePath": comment.path}
            comments.append(comment_entry)
        if not comments:
            continue
        thread_path = next((comment_entry["path"] for comment_entry in comments if comment_entry.get("path")), None)
        normalized_thread = {
            "id": thread_id,
            "isDeleted": False,
            "status": "fixed" if resolved else "active",
            "comments": comments,
        }
        if not thread_id.startswith(_SYNTHETIC_THREAD_KEY_PREFIX):
            normalized_thread["githubThreadNodeId"] = thread_id
        if thread_path:
            normalized_thread["threadContext"] = {"filePath": thread_path}
            normalized_thread["pullRequestThreadContext"] = {"filePath": thread_path}
        normalized_threads.append(normalized_thread)
    for comment in all_comments:
        if comment.id in emitted_comment_ids:
            continue
        comment_entry = {
            "id": comment.id,
            "content": comment.body,
            "isDeleted": False,
            "path": comment.path,
            "line": comment.line,
            "startLine": comment.start_line,
            "commitId": comment.commit_id,
            "originalCommitId": comment.original_commit_id,
            "htmlUrl": getattr(comment, "html_url", ""),
            "inReplyToId": getattr(comment, "in_reply_to_id", None),
            "createdAt": getattr(comment, "created_at", ""),
            "author": {
                "displayName": comment.author_login,
                "uniqueName": comment.author_login,
            },
        }
        normalized_thread = {
            "id": f"comment-{comment.id}",
            "isDeleted": False,
            "status": "active",
            "comments": [comment_entry],
        }
        if comment.path:
            comment_entry["threadContext"] = {"filePath": comment.path}
            comment_entry["pullRequestThreadContext"] = {"filePath": comment.path}
            normalized_thread["threadContext"] = {"filePath": comment.path}
            normalized_thread["pullRequestThreadContext"] = {"filePath": comment.path}
        normalized_threads.append(normalized_thread)
    # PR conversation comments (from /issues/{pr}/comments) are distinct from
    # inline review comments: they carry no file path and live in a separate
    # id namespace, so they cannot collide with the review-comment threads
    # built above. Surface them as pathless threads so general author/reviewer
    # feedback is not dropped from the persisted manifest.
    for issue_comment in provider.list_issue_comments(pull_request_id):
        normalized_threads.append(
            {
                "id": f"issue-comment-{issue_comment.id}",
                "isDeleted": False,
                "status": "active",
                "comments": [
                    {
                        "id": issue_comment.id,
                        "content": issue_comment.body,
                        "isDeleted": False,
                        "path": None,
                        "createdAt": issue_comment.created_at,
                        "htmlUrl": getattr(issue_comment, "html_url", ""),
                        "author": {
                            "displayName": issue_comment.author,
                            "uniqueName": issue_comment.author,
                        },
                    }
                ],
            }
        )
    normalized_files: list[dict[str, Any]] = []
    for index, file_detail in enumerate(files):
        if not isinstance(file_detail, Mapping):
            raise RuntimeError(
                f"GitHub returned malformed file entry at index {index} for pull request {pull_request_id}: "
                "expected an object"
            )
        path = file_detail.get("filename")
        if not isinstance(path, str) or not path.strip():
            raise RuntimeError(
                f"GitHub returned malformed file entry at index {index} for pull request {pull_request_id}: "
                "expected a non-blank string 'filename'"
            )
        raw_status = file_detail.get("status")
        status = raw_status if isinstance(raw_status, str) else ""
        normalized_file = dict(file_detail)
        normalized_file.update(
            {
                "path": path,
                "status": status,
                "changeType": _github_change_type(status),
            }
        )
        raw_additions = file_detail.get("additions", 0)
        raw_deletions = file_detail.get("deletions", 0)
        if (
            isinstance(raw_additions, bool)
            or not isinstance(raw_additions, int)
            or raw_additions < 0
            or isinstance(raw_deletions, bool)
            or not isinstance(raw_deletions, int)
            or raw_deletions < 0
        ):
            raise RuntimeError(
                f"GitHub returned invalid additions/deletions for file {path!r} "
                f"in pull request {pull_request_id}: expected non-negative integers"
            )
        normalized_file["addedLineCount"] = raw_additions
        normalized_file["removedLineCount"] = raw_deletions
        # GitHub omits "patch" for files it could not diff as text (typically
        # binary content, but also files too large to diff). Only assert
        # isBinary=False when GitHub actually produced a textual diff — that is
        # a reliable positive signal. Leave "isBinary" unset when the patch is
        # missing instead of asserting True, so the downstream detector's
        # extension-based fallback (file_retriever.is_binary_file) still runs
        # for files this signal can't confirm, rather than misclassifying a
        # large text file as binary.
        patch = file_detail.get("patch")
        if isinstance(patch, str) and patch.rstrip().splitlines()[-1:] != ["..."]:
            normalized_file["isBinary"] = False
            added_lines, removed_lines = _parse_github_patch(patch)
            if len(added_lines) == raw_additions and len(removed_lines) == raw_deletions:
                normalized_file["addedLines"] = added_lines
                normalized_file["removedLines"] = removed_lines
        previous_filename = file_detail.get("previous_filename")
        if isinstance(previous_filename, str) and previous_filename:
            normalized_file["originalPath"] = previous_filename
        normalized_files.append(normalized_file)
    head = metadata.get("head") if isinstance(metadata, Mapping) else {}
    base = metadata.get("base") if isinstance(metadata, Mapping) else {}
    head_ref = head.get("ref") if isinstance(head, Mapping) else ""
    raw_head_sha = head.get("sha") if isinstance(head, Mapping) else None
    head_sha = raw_head_sha if isinstance(raw_head_sha, str) and raw_head_sha.strip() else ""
    head_available = bool(head_sha)
    base_ref = base.get("ref") if isinstance(base, Mapping) else ""
    base_sha = base.get("sha") if isinstance(base, Mapping) else ""
    base_ref_value = base_sha if isinstance(base_sha, str) and base_sha else ""
    if not base_ref_value:
        base_ref_value = f"origin/{base_ref}" if isinstance(base_ref, str) and base_ref else "origin/main"
    compare_ref_value = head_sha
    if not compare_ref_value:
        compare_ref_value = ""
    raw_number = metadata.get("number") if isinstance(metadata, Mapping) else pull_request_id
    number = raw_number if isinstance(raw_number, int) and not isinstance(raw_number, bool) else pull_request_id
    is_merged = isinstance(metadata, Mapping) and metadata.get("merged") is True
    raw_state = metadata.get("state") if isinstance(metadata, Mapping) else None
    if raw_state == "closed":
        pr_status = "completed" if is_merged else "abandoned"
    elif raw_state == "open":
        pr_status = "active"
    else:
        raise RuntimeError(f"GitHub returned unsupported pull request state {raw_state!r}")
    author = metadata.get("user") if isinstance(metadata, Mapping) else None
    raw_author_login = author.get("login") if isinstance(author, Mapping) else None
    author_login = raw_author_login if isinstance(raw_author_login, str) else ""
    raw_title = metadata.get("title") if isinstance(metadata, Mapping) else None
    raw_body = metadata.get("body") if isinstance(metadata, Mapping) else None
    raw_html_url = metadata.get("html_url") if isinstance(metadata, Mapping) else None
    normalized_repository = {
        "id": repository,
        "name": repository.split("/", maxsplit=1)[1],
        "project": {"name": repository.split("/", maxsplit=1)[0]},
    }
    normalized_pr = {
        "pullRequestId": number,
        "number": number,
        "url": raw_html_url if isinstance(raw_html_url, str) else "",
        "title": raw_title if isinstance(raw_title, str) else "",
        # GitHub's PR body maps to the normalized `description` field consumed by
        # the manifest builder for `meta.prSummary`.
        "description": raw_body if isinstance(raw_body, str) else "",
        "isDraft": bool(metadata.get("draft", False)) if isinstance(metadata, Mapping) else False,
        "status": pr_status,
        "createdBy": {
            "displayName": author_login,
            "uniqueName": author_login,
        },
        "sourceRefName": f"refs/heads/{head_ref}" if isinstance(head_ref, str) and head_ref else "",
        "targetRefName": f"refs/heads/{base_ref}" if isinstance(base_ref, str) and base_ref else "",
        "lastMergeSourceCommit": {"commitId": head_sha} if isinstance(head_sha, str) else {"commitId": ""},
        "lastMergeTargetCommit": {"commitId": base_sha} if isinstance(base_sha, str) else {"commitId": ""},
        "repository": normalized_repository,
        "head_sha": head_sha if isinstance(head_sha, str) else "",
        "head_branch": head_ref if isinstance(head_ref, str) else "",
        "base_branch": base_ref if isinstance(base_ref, str) else "",
    }
    diff = provider.get_pr_diff(pull_request_id) if diff_complete and head_available else None
    if head_available:
        latest_metadata = _github_api_json(f"/repos/{repository}/pulls/{pull_request_id}")
        latest_head = latest_metadata.get("head") if isinstance(latest_metadata, Mapping) else None
        latest_head_sha = latest_head.get("sha") if isinstance(latest_head, Mapping) else None
        if not isinstance(latest_head_sha, str) or not latest_head_sha:
            raise RuntimeError(
                f"GitHub did not return a valid head SHA for pull request {pull_request_id} "
                "after collecting details; retry the command"
            )
        if latest_head_sha != head_sha:
            raise RuntimeError(
                f"GitHub pull request {pull_request_id} head changed while collecting details; retry the command"
            )
    warnings = [
        {"capability": "iterations", "message": "GitHub does not expose Azure DevOps-style PR iterations."},
        {"capability": "reviewedFiles", "message": "GitHub does not expose Azure DevOps-style viewed-file state."},
    ]
    if not head_available:
        warnings.append(
            {
                "capability": "head",
                "message": (
                    "GitHub did not provide a valid pull-request head SHA; "
                    "head comparison and diff data are unavailable."
                ),
            }
        )
    return {
        "schemaVersion": 1,
        "provider": "github",
        "pullRequest": normalized_pr,
        "repository": normalized_repository,
        "providerData": {"repository": repository},
        "comparison": {
            "baseRef": base_ref_value,
            "compareRef": compare_ref_value,
            "baseCommit": base_sha if isinstance(base_sha, str) else "",
            "compareCommit": head_sha,
            "baseBranch": base_ref if isinstance(base_ref, str) else "",
            "compareBranch": head_ref if isinstance(head_ref, str) else "",
        },
        "commits": commits if isinstance(commits, list) else [],
        "files": normalized_files,
        "diff": diff,
        "diffComplete": diff_complete and head_available,
        "threads": normalized_threads,
        "iterations": {"status": "unsupported", "items": []},
        "reviewer": {
            "reviews": reviews,
            "threadStates": thread_states,
            "reviewedFiles": {"status": "unsupported", "files": []},
        },
        "capabilities": {
            "iterations": "unsupported",
            "reviewedFiles": "unsupported",
            "reviews": "available",
            "reviewThreads": "available",
        },
        "warnings": warnings,
    }


def get_pull_request_details(
    provider: str | None = None,
    pull_request_id: int | None = None,
    repository: str | None = None,
    *,
    state: Mapping[str, Any] | None = None,
    output_file: Path | None = None,
    dry_run: bool | None = None,
    state_snapshot: bool = False,
) -> dict[str, Any] | None:
    """Retrieve details using Azure DevOps' existing command or GitHub APIs."""
    selected = detect_provider(provider, state, repository)
    if selected == "azure_devops":
        from agentic_devtools.cli.azure_devops.pull_request_details_commands import (
            get_pull_request_details as ado_command,
        )

        # Force the resolved provider into the delegated state so the Azure
        # command cannot switch providers based on conflicting injected values.
        delegated_state = _deep_merge_state(
            state or {},
            {"provider": selected, "platform": {"code_hosting": selected}},
        )
        state_provider = _state_value(state, "platform.code_hosting", "provider", "github.provider")
        if isinstance(state_provider, str) and state_provider.strip().lower() != selected:
            delegated_state.pop("repository", None)

            source_hosting = delegated_state.get("sourceCodeHostingPlatform")
            if isinstance(source_hosting, Mapping):
                source_hosting = dict(source_hosting)
                pull_request = source_hosting.get("pullRequest")
                if isinstance(pull_request, Mapping):
                    pull_request = dict(pull_request)
                    pull_request.pop("repository", None)
                    source_hosting["pullRequest"] = pull_request
                delegated_state["sourceCodeHostingPlatform"] = source_hosting

            github_state = delegated_state.get("github")
            if isinstance(github_state, Mapping):
                github_state = dict(github_state)
                github_state.pop("repo", None)
                delegated_state["github"] = github_state

        delegated_kwargs: dict[str, Any] = {
            "pull_request_id": pull_request_id,
            "repository": repository,
            "state": delegated_state,
        }
        if output_file is not None:
            delegated_kwargs["output_file"] = output_file
        if dry_run is not None:
            delegated_kwargs["dry_run"] = dry_run
        if state_snapshot:
            delegated_kwargs["state_snapshot"] = True
        ado_command(**delegated_kwargs)
        return None
    if not isinstance(pull_request_id, int) or isinstance(pull_request_id, bool) or pull_request_id <= 0:
        raise ValueError("pull_request_id must be a positive integer")
    if not isinstance(repository, str) or not is_valid_github_repository(repository):
        raise ValueError("GitHub repository must be in owner/repo form")
    return _github_details(pull_request_id, repository)


fetch_pull_request_details = get_pull_request_details
