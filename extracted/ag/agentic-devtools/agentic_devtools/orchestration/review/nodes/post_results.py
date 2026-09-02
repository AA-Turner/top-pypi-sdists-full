"""``post_results`` node — posts review results to Azure DevOps.

Satisfies FR-007 (posting consolidated review comment and line-anchored
suggestion threads), FR-005 (final review-state.json update), and
NFR-002 (idempotent writes via marker-based recovery for suggestion
threads and consolidated comments).
"""

from __future__ import annotations

import json
import sys
from typing import Any, TypeAlias
from urllib.parse import quote, unquote

SuggestionThreadKey: TypeAlias = tuple[str, int, int, str | None, str]
PostedSuggestion: TypeAlias = tuple[str, int, int, int, int, str, str, bool, str, str | None]


def post_results_node(state: dict[str, Any]) -> dict[str, Any]:
    """Post review results back to Azure DevOps.

    Posts the consolidated review comment with the final verdict and
    per-file findings.  Updates ``review-state.json`` with thread IDs
    and the final overall status.

    Args:
        state: Current ``ReviewGraphState``.

    Returns:
        State update dict confirming completion.
    """
    review_state_path = state.get("review_state_path", "")
    file_results = state.get("file_results", [])
    overall_decision = state.get("overall_decision", "approve")
    summary = state.get("summary", "")
    pr_id = state.get("pr_id")
    organization = state.get("organization", "")
    project = state.get("project", "")
    repo_id = state.get("repo_id", "")

    # Carry forward any errors accumulated by upstream pipeline nodes so that
    # they appear in the final stdout summary (NFR-003) and are not silently
    # dropped.  The `or []` guards against an explicit `None` stored in state
    # (e.g. a node that returns `{"errors": None}`), where `.get()` alone would
    # return `None` and `list(None)` would raise `TypeError`.
    upstream_errors: list[str] = list(state.get("errors", []) or [])
    errors: list[str] = []

    # Update review state with final results
    if pr_id:
        try:
            _update_final_review_state(
                pr_id=int(pr_id),
                file_results=file_results,
                overall_decision=overall_decision,
                summary=summary,
            )
        except Exception as exc:
            print(f"post_results: failed to update review state: {exc}", file=sys.stderr)
            errors.append("post_results: failed to update review state")

    # Post line-anchored suggestion threads first so that when the consolidated
    # comment is rendered it can read the persisted suggestion thread IDs from
    # review-state.json.  The consolidated renderer sources suggestions from the
    # review state, so posting them after the consolidated comment would cause the
    # comment to be rendered without the suggestions.
    if pr_id and organization and project and repo_id:
        try:
            _post_suggestion_threads(
                pr_id=int(pr_id),
                organization=organization,
                project=project,
                repo_id=repo_id,
                file_results=file_results,
            )
        except Exception as exc:
            print(f"post_results: failed to post suggestion threads: {exc}", file=sys.stderr)
            errors.append("post_results: failed to post suggestion threads")

        # Post the consolidated comment after suggestions have been persisted so
        # the renderer sees all suggestion thread IDs in review-state.json.
        try:
            _post_consolidated_comment(
                pr_id=int(pr_id),
                organization=organization,
                project=project,
                repo_id=repo_id,
            )
        except Exception as exc:
            print(f"post_results: failed to post consolidated comment: {exc}", file=sys.stderr)
            errors.append("post_results: failed to post consolidated comment")

    # Write structured output to stdout (NFR-003).  Upstream errors (from
    # fetch_pr_details, scaffold_comments, review_files, etc.) are prepended so
    # that failures in earlier nodes are visible in the final summary even when
    # post_results itself succeeds.
    all_errors = upstream_errors + errors
    output = {
        "status": "completed",
        "decision": overall_decision,
        "summary": summary,
        "files_reviewed": len(file_results),
        "review_state_path": review_state_path,
        "errors": all_errors,
    }
    print(json.dumps(output, indent=2))

    return {"errors": errors}


def _update_final_review_state(
    *,
    pr_id: int,
    file_results: list[Any],
    overall_decision: str,
    summary: str = "",
) -> None:
    """Update review-state.json with the final overall status.

    The base status is derived from the per-file statuses already persisted by
    ``review_files_node``.  The ``overall_decision`` from the policy engine is
    then applied as a one-way tightener: if the policy decided
    ``"request-changes"`` but all files were individually approved, the stored
    status is escalated to ``"needs-work"`` so the consolidated comment and
    status cascade reflect the autonomous decision.  The policy can never
    *loosen* the status — a file-level ``"needs-work"`` is always preserved.
    """
    from agentic_devtools.cli.azure_devops.review_state import (
        ReviewStatus,
        load_review_state,
        save_review_state,
    )
    from agentic_devtools.cli.azure_devops.status_cascade import derive_overall_status

    try:
        review_state = load_review_state(pr_id)
    except FileNotFoundError:
        print("Warning: review-state.json not found, skipping update", file=sys.stderr)
        return

    _apply_effective_model_attribution(review_state, file_results)

    # Derive the overall status from the saved per-file statuses first.
    derived = derive_overall_status(review_state)

    # The policy decision can only *tighten* the status: if the decision engine
    # determined that policy thresholds require "request-changes" but every file
    # was individually approved, escalate the stored status to "needs-work" so
    # the consolidated comment and status cascade reflect the autonomous decision.
    # The policy never *loosens* the status — if any file needs work, that stays.
    if overall_decision == "request-changes" and derived == ReviewStatus.APPROVED.value:
        review_state.overallSummary.status = ReviewStatus.NEEDS_WORK.value
    else:
        review_state.overallSummary.status = derived
    review_state.overallSummary.narrativeSummary = summary

    save_review_state(review_state)


def _apply_effective_model_attribution(review_state: Any, file_results: list[Any]) -> None:
    """Persist a single effective model only when the reviewed files agree on one.

    Per-file routing can legitimately use different models for different files.
    In that case the scaffolded/requested top-level ``modelId`` is preserved
    because there is no single effective attribution to promote globally.
    """

    all_model_ids = [
        result.get("model_id") if isinstance(result, dict) else getattr(result, "model_id", None)
        for result in file_results
    ]
    valid_models = [m.strip() for m in all_model_ids if isinstance(m, str) and m.strip()]
    if len(valid_models) != len(file_results):
        return
    effective_models = set(valid_models)
    if len(effective_models) != 1:
        return

    effective_model = next(iter(effective_models))

    # Migrate the commit registry before updating the top-level modelId.
    # When the effective model (returned by the provider at runtime) differs from
    # the scaffolded/requested model, the CommitComment entry for the current
    # commit still holds a ModelCommentRef keyed by the old model ID.  Renaming
    # it here — before review_state.modelId is written — ensures that the ref in
    # the commit registry stays consistent with the new modelId: subsequent reads
    # of the registry use modelId as the lookup key, so misalignment would cause
    # the same review run to appear as two separate model reviews.
    #
    # Only the entry for the current commit is migrated; walking every historical
    # entry would risk renaming refs from earlier reviews that legitimately used
    # the same requested model with a different effective model.
    old_model_id = getattr(review_state, "modelId", None)
    commit_hash = getattr(review_state, "commitHash", None)
    commit_comments = getattr(review_state, "commitComments", {})
    entry = commit_comments.get(commit_hash) if isinstance(commit_comments, dict) and commit_hash else None
    source_model_id: str | None = None

    if commit_hash:
        sessions = list(reversed(getattr(review_state, "sessions", [])))
        eligible_sessions = [
            session
            for session in sessions
            if getattr(session, "status", None) == "in_progress"
            and ((session_commit := getattr(session, "commitHash", None)) is None or session_commit == commit_hash)
        ]
        if isinstance(old_model_id, str) and old_model_id.strip():
            scaffolded_model = old_model_id.strip()
            if any(getattr(session, "modelId", None) == scaffolded_model for session in eligible_sessions):
                source_model_id = scaffolded_model
            else:
                alias_models: set[str] = set()
                if entry is not None:
                    alias_models = {
                        normalized_model
                        for session in eligible_sessions
                        if isinstance(session_model := getattr(session, "modelId", None), str)
                        and (normalized_model := session_model.strip())
                        and entry.get_model(normalized_model) is not None
                        and normalized_model != scaffolded_model
                    }
                if len(alias_models) == 1:
                    source_model_id = next(iter(alias_models))

    if source_model_id is None and isinstance(old_model_id, str) and old_model_id.strip():
        source_model_id = old_model_id.strip()

    if entry is not None and source_model_id and source_model_id != effective_model:
        source_ref = entry.get_model(source_model_id)
        if source_ref is not None and source_ref.modelId == source_model_id:
            target_ref = entry.get_model(effective_model)
            if target_ref is None:
                source_ref.modelId = effective_model
            else:
                if source_ref.commentId > 0:
                    target_ref.commentId = source_ref.commentId
                seen_continuations = set(target_ref.continuationCommentIds)
                for continuation_id in source_ref.continuationCommentIds:
                    if continuation_id not in seen_continuations:
                        target_ref.continuationCommentIds.append(continuation_id)
                        seen_continuations.add(continuation_id)
                if isinstance(source_ref.status, str) and source_ref.status:
                    target_ref.status = source_ref.status
                if isinstance(source_ref.timestamp, str) and source_ref.timestamp:
                    target_ref.timestamp = source_ref.timestamp
                entry.models = [ref for ref in entry.models if ref is not source_ref]

    review_state.modelId = effective_model
    # Apply the same commit/model scoping as complete_active_session() so that
    # a concurrent or stale in_progress session for a different commit or model
    # is not incorrectly relabelled.
    # When old_model_id is None (no scaffolded model was set), model filtering
    # is intentionally skipped — matching complete_active_session()'s behaviour —
    # and the newest commit-scoped in_progress session is relabelled regardless.
    commit_hash_attr = getattr(review_state, "commitHash", None)
    candidates = list(reversed(getattr(review_state, "sessions", [])))
    if commit_hash_attr:
        candidates = [
            s for s in candidates if getattr(s, "commitHash", None) is None or s.commitHash == commit_hash_attr
        ]
    if old_model_id:
        model_scoped = [
            s
            for s in candidates
            if isinstance(session_model := getattr(s, "modelId", None), str)
            and session_model.strip() == source_model_id
        ]
        candidates = [s for s in model_scoped if getattr(s, "status", None) == "in_progress"]
    for session in candidates:
        if getattr(session, "status", None) == "in_progress":
            session.modelId = effective_model
            break


def _post_consolidated_comment(
    *,
    pr_id: int,
    organization: str,
    project: str,
    repo_id: str,
) -> None:
    """Post or update the consolidated review comment on the PR."""
    from agentic_devtools.cli.azure_devops.auth import get_auth_headers, get_pat
    from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
    from agentic_devtools.cli.azure_devops.review_state import load_review_state
    from agentic_devtools.cli.azure_devops.status_cascade import (
        cascade_overall_summary_update,
        execute_cascade,
    )

    try:
        review_state = load_review_state(pr_id)
    except FileNotFoundError:
        print("Warning: review-state.json not found, skipping cascade", file=sys.stderr)
        return

    project_encoded = _encode_project(project)
    base_url = f"{organization}/{project_encoded}/_apis/git/repositories/{repo_id}/pullRequests/{pr_id}"

    pat = get_pat()
    headers = get_auth_headers(pat)
    config = AzureDevOpsConfig.from_state()

    import requests as requests_module

    ops = cascade_overall_summary_update(review_state, base_url)
    if ops:
        execute_cascade(
            ops,
            requests_module,
            headers,
            config=config,
            repo_id=repo_id,
            pull_request_id=pr_id,
            state=review_state,
        )

    from agentic_devtools.cli.azure_devops.review_state import save_review_state

    save_review_state(review_state)


def _post_suggestion_threads(
    *,
    pr_id: int,
    organization: str,
    project: str,
    repo_id: str,
    file_results: list[Any],
) -> None:
    """Post line-anchored suggestion threads for anchorable findings."""
    from agentic_devtools.cli.azure_devops.auth import get_auth_headers, get_pat

    pat = get_pat()
    headers = get_auth_headers(pat)
    posted_suggestions: list[PostedSuggestion] = []
    existing_threads = _list_existing_suggestion_thread_keys(
        pr_id=pr_id,
        organization=organization,
        project=project,
        repo_id=repo_id,
        headers=headers,
    )

    for result in file_results:
        suggestions = result.get("suggestions", []) if isinstance(result, dict) else getattr(result, "suggestions", [])
        for suggestion in suggestions:
            line = suggestion.get("line") if isinstance(suggestion, dict) else getattr(suggestion, "line", None)
            if not line:
                # Defensive guard: all SuggestionOutput objects carry a required line
                # anchor, so this path should not be reached from validated LLM output.
                # Emit a warning so any malformed suggestion dict is observable rather
                # than silently dropped.
                _fp = result.get("file_path", "") if isinstance(result, dict) else getattr(result, "file_path", "")
                print(
                    f"Warning: post_results: suggestion in {_fp!r} has no line anchor "
                    f"and cannot be posted as an ADO thread; it will not appear in "
                    f"review-state.json",
                    file=sys.stderr,
                )
                continue

            end_line = (
                suggestion.get("endLine") if isinstance(suggestion, dict) else getattr(suggestion, "endLine", None)
            )
            file_path = result.get("file_path", "") if isinstance(result, dict) else getattr(result, "file_path", "")
            content = (
                suggestion.get("content", "") if isinstance(suggestion, dict) else getattr(suggestion, "content", "")
            )
            out_of_scope = (
                suggestion.get("out_of_scope", False)
                if isinstance(suggestion, dict)
                else getattr(suggestion, "out_of_scope", False)
            )
            replacement_code = (
                suggestion.get("replacement_code")
                if isinstance(suggestion, dict)
                else getattr(suggestion, "replacement_code", None)
            )
            severity = (
                suggestion.get("severity") if isinstance(suggestion, dict) else getattr(suggestion, "severity", None)
            )
            thread_key = _build_suggestion_thread_key(
                file_path=file_path,
                line=line,
                end_line=end_line if isinstance(end_line, int) else None,
                severity=severity if isinstance(severity, str) else None,
                content=content,
                replacement_code=replacement_code if isinstance(replacement_code, str) else None,
            )
            if thread_key in existing_threads:
                continue

            # Post line-anchored comment thread
            try:
                thread_id, comment_id = _post_line_comment(
                    pr_id=pr_id,
                    organization=organization,
                    project=project,
                    repo_id=repo_id,
                    headers=headers,
                    file_path=file_path,
                    line=line,
                    end_line=end_line,
                    content=content,
                    replacement_code=replacement_code,
                    severity=severity if isinstance(severity, str) else None,
                )
                existing_threads.add(thread_key)
                posted_suggestions.append(
                    (
                        file_path,
                        thread_id,
                        comment_id,
                        line,
                        end_line if isinstance(end_line, int) else line,
                        severity if isinstance(severity, str) else "",
                        content,
                        bool(out_of_scope),
                        _build_link_text(line, end_line if isinstance(end_line, int) else None),
                        replacement_code if isinstance(replacement_code, str) else None,
                    )
                )
            except Exception as exc:
                print(f"Warning: failed to post suggestion thread: {exc}", file=sys.stderr)

    _persist_posted_suggestions(pr_id=pr_id, posted_suggestions=posted_suggestions)


def _build_link_text(line: int, end_line: int | None) -> str:
    """Return the standard discussion link label for a suggestion."""
    effective_end_line = end_line if isinstance(end_line, int) else line
    if effective_end_line != line:
        return f"lines {line} - {effective_end_line}"
    return f"line {line}"


def _persist_posted_suggestions(*, pr_id: int, posted_suggestions: list[PostedSuggestion]) -> None:
    """Persist successfully posted suggestion thread metadata to review state."""
    if not posted_suggestions:
        return

    from agentic_devtools.cli.azure_devops.review_state import (
        SuggestionEntry,
        add_suggestion_to_file,
        normalize_file_path,
        read_modify_write_review_state,
    )

    with read_modify_write_review_state(pr_id) as review_state:
        for (
            file_path,
            thread_id,
            comment_id,
            line,
            end_line,
            severity,
            content,
            out_of_scope,
            link_text,
            replacement_code,
        ) in posted_suggestions:
            normalized_path = normalize_file_path(file_path)
            file_entry = review_state.files.get(normalized_path)
            if file_entry is None:
                print(
                    f"Warning: could not persist suggestion thread for unknown file {normalized_path!r}",
                    file=sys.stderr,
                )
                continue
            # Remove any draft entry (threadId=0 sentinel from _update_review_state_for_file)
            # that matches this suggestion by line+endLine+content.  The real ADO entry with actual
            # thread/comment IDs is about to be appended; keeping both would duplicate findings.
            file_entry.suggestions = [
                s
                for s in file_entry.suggestions
                if not (s.threadId == 0 and s.line == line and s.endLine == end_line and s.content == content)
            ]
            if any(
                existing.threadId == thread_id and existing.commentId == comment_id
                for existing in file_entry.suggestions
            ):
                continue
            add_suggestion_to_file(
                review_state,
                normalized_path,
                SuggestionEntry(
                    threadId=thread_id,
                    commentId=comment_id,
                    line=line,
                    endLine=end_line,
                    severity=severity,
                    outOfScope=out_of_scope,
                    linkText=link_text,
                    content=content,
                    replacement_code=replacement_code,
                ),
            )


def _list_existing_suggestion_thread_keys(
    *,
    pr_id: int,
    organization: str,
    project: str,
    repo_id: str,
    headers: dict[str, str],
) -> set[SuggestionThreadKey]:
    """Recover existing AGDT suggestion threads for idempotent re-runs."""
    import requests

    from agentic_devtools.cli.azure_devops.marker import parse_marker, strip_marker_line

    project_encoded = _encode_project(project)
    url = (
        f"{organization}/{project_encoded}/_apis/git/repositories/"
        f"{repo_id}/pullRequests/{pr_id}/threads?api-version=7.1-preview.1"
    )
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    payload = response.json()
    threads = payload.get("value", []) if isinstance(payload, dict) else payload
    existing: set[SuggestionThreadKey] = set()
    for thread in threads:
        if not isinstance(thread, dict):
            continue
        comments = thread.get("comments")
        if not isinstance(comments, list) or not comments:
            continue
        first_comment = comments[0]
        if not isinstance(first_comment, dict):
            continue
        content = first_comment.get("content")
        if not isinstance(content, str):
            continue
        marker = parse_marker(content)
        if not marker or marker.get("type") != "suggestion":
            continue
        line_raw = marker.get("line")
        if not line_raw or not line_raw.isdigit():
            continue
        start_line = int(line_raw)
        thread_context = thread.get("threadContext")
        file_path = marker.get("file")
        if not file_path and isinstance(thread_context, dict):
            raw_path = thread_context.get("filePath")
            file_path = raw_path if isinstance(raw_path, str) else None
        if not file_path:
            continue
        end_line = start_line
        if isinstance(thread_context, dict):
            right_file_end = thread_context.get("rightFileEnd")
            if isinstance(right_file_end, dict):
                end_line_raw = right_file_end.get("line")
                if isinstance(end_line_raw, int):
                    end_line = end_line_raw
        existing.add((file_path, start_line, end_line, marker.get("severity"), strip_marker_line(content)))
    return existing


def _post_line_comment(
    *,
    pr_id: int,
    organization: str,
    project: str,
    repo_id: str,
    headers: dict[str, str],
    file_path: str,
    line: int,
    content: str,
    replacement_code: str | None,
    end_line: int | None = None,
    severity: str | None = None,
) -> tuple[int, int]:
    """Post a single line-anchored comment thread to Azure DevOps."""
    import requests

    from agentic_devtools.cli.azure_devops.marker import build_marker
    from agentic_devtools.cli.azure_devops.pr_review_submit_mapper import (
        transform_replacement_code,
    )

    project_encoded = _encode_project(project)
    url = (
        f"{organization}/{project_encoded}/_apis/git/repositories/"
        f"{repo_id}/pullRequests/{pr_id}/threads?api-version=7.1-preview.1"
    )

    marker = build_marker("suggestion", file=file_path, pr=pr_id, line=line, severity=severity)
    comment_body = transform_replacement_code(content, replacement_code)
    comment_content = f"{marker}\n{comment_body}"

    body = {
        "comments": [
            {
                "parentCommentId": 0,
                "content": comment_content,
                "commentType": "text",
            }
        ],
        "status": "active",
        "threadContext": {
            "filePath": file_path,
            "rightFileStart": {"line": line, "offset": 1},
            "rightFileEnd": {"line": end_line or line, "offset": 1},
        },
    }

    response = requests.post(url, json=body, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise RuntimeError("Unexpected Azure DevOps thread response payload type")
    thread_id = payload.get("id")
    comments = payload.get("comments")
    if not isinstance(thread_id, int):
        raise RuntimeError("Azure DevOps thread response did not include an integer thread id")
    if not isinstance(comments, list) or not comments:
        raise RuntimeError("Azure DevOps thread response did not include comments")
    first_comment = comments[0]
    if not isinstance(first_comment, dict):
        raise RuntimeError("Azure DevOps thread response did not include a valid comment object")
    comment_id = first_comment.get("id")
    if not isinstance(comment_id, int):
        raise RuntimeError("Azure DevOps thread response did not include an integer comment id")
    return thread_id, comment_id


def _build_suggestion_thread_key(
    *,
    file_path: str,
    line: int,
    end_line: int | None,
    severity: str | None,
    content: str,
    replacement_code: str | None,
) -> SuggestionThreadKey:
    """Build the deduplication key for a suggestion thread."""
    from agentic_devtools.cli.azure_devops.pr_review_submit_mapper import (
        transform_replacement_code,
    )

    return (
        file_path,
        line,
        end_line if isinstance(end_line, int) else line,
        severity,
        transform_replacement_code(content, replacement_code),
    )


def _encode_project(project: str) -> str:
    """Normalize raw or already-encoded Azure DevOps project names for URLs."""
    return quote(unquote(project), safe="")
