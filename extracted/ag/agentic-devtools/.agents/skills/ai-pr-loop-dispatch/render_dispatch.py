"""Render a CCR review body with the repository's AI PR Loop comment builder."""

from __future__ import annotations

import argparse
import asyncio
import base64
import difflib
import importlib
import json
import os
import re
import subprocess
import sys
import time
from collections.abc import Callable, Mapping
from dataclasses import replace
from html import escape
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast
from urllib.parse import quote

_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from agentic_devtools.cli.ci.evaluator.diff_heuristic import check_lines_modified  # noqa: E402
from agentic_devtools.cli.ci.review_thread_state import fetch_review_thread_states  # noqa: E402

_REVIEW_URL_PATTERN = re.compile(
    r"^https://github\.com/(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)"
    r"/pull/(?P<pr>\d+)#pullrequestreview-(?P<review>\d+)$"
)
_SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")
_TASK_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
_TERMINAL_TASK_STATES = frozenset({"completed", "failed", "timed_out", "cancelled"})
_TASK_FINAL_RESPONSE_MARKER = re.compile(r"[^\r\n]* End subagent:[^\n]*\n")
_TASK_COMMENT_ID_PATTERN = re.compile(r"\b(?:replied to|reply to|comment)\s+`?(\d+)`?", re.IGNORECASE)
_SUPPRESSED_THREAD_MARKER = "<!-- ai-pr-loop-dispatch-suppressed:{review_id}:{ordinal} -->"
_FOLLOW_UP_MARKER = "<!-- ai-pr-loop:follow-up-issue -->"
_DO_NOT_RESOLVE_MARKER = "AI_PR_LOOP_DO_NOT_RESOLVE"
_RESOLVE_MARKER = "AI_PR_LOOP_RESOLVE"
_SDK_ADJUDICATION_ATTEMPTS = 3
_SDK_RETRY_DELAYS_SECONDS = (1.0, 2.0)
_MAX_TASK_RETRIES = 1
_MAX_RETRY_SESSION_POLLS = 3
_PUSH_FAILURE_MARKERS = (
    "push_blocked",
    "push was blocked",
    "push failed",
    "failed to push",
    "push rejected",
    "non-fast-forward",
    "cannot update this protected ref",
    "repository rule violations",
)
_NO_CODE_CHANGE_MARKERS = (
    "no code changes",
    "no changes were made",
    "no changes needed",
    "no change was needed",
    "nothing to change",
)
_PR_COMMIT_CACHE: dict[tuple[str, str, int], tuple[str, ...]] = {}


class _AgentTasksPayloadTransport:
    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        json_body: Mapping[str, Any] | None,
        timeout: float,
    ) -> Any:
        from agentic_devtools.ai_providers import build_agent_tasks_payload

        body = json_body
        if method == "POST" and isinstance(json_body, Mapping):
            metadata = json_body.get("metadata")
            if isinstance(metadata, Mapping):
                body = build_agent_tasks_payload(
                    prompt=cast(str, json_body["prompt"]),
                    model=cast(str, json_body["model"]),
                    base_ref=cast(str, metadata["base_ref"]),
                    head_ref=cast(str, metadata["head_ref"]),
                )
        return self._transport.request(
            method,
            url,
            headers=headers,
            json_body=body,
            timeout=timeout,
        )


def _parse_review_url(value: str) -> tuple[str, str, int, int]:
    match = _REVIEW_URL_PATTERN.fullmatch(value.strip())
    if match is None:
        raise ValueError("review URL must look like https://github.com/owner/repo/pull/123#pullrequestreview-456")
    return (
        match.group("owner"),
        match.group("repo"),
        int(match.group("pr")),
        int(match.group("review")),
    )


def _gh_value(endpoint: str, jq: str) -> str:
    try:
        result = subprocess.run(
            ["gh", "api", endpoint, "--jq", jq],
            capture_output=True,
            check=True,
            encoding="utf-8",
            shell=False,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("GitHub CLI 'gh' is required for link-only input.") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "GitHub CLI request failed").strip()
        raise RuntimeError(detail) from exc
    value = result.stdout.strip()
    if not value or value == "null":
        raise RuntimeError(f"GitHub API returned no value for {endpoint} ({jq}).")
    return value


def _load_token() -> str:
    for name in ("COPILOT_GITHUB_TOKEN", "SPECKIT_PR_TOKEN", "GH_TOKEN", "GITHUB_TOKEN"):
        token = os.environ.get(name, "").strip()
        if token:
            return token
    raise RuntimeError(
        "No Agent Tasks token found. Set COPILOT_GITHUB_TOKEN, SPECKIT_PR_TOKEN, GH_TOKEN, or GITHUB_TOKEN."
    )


def _strip_copilot_tag(prompt: str) -> str:
    return re.sub(r"^@copilot\b\s*(?:-\s*)?", "", prompt, count=1, flags=re.IGNORECASE)


def _load_review_body(
    *,
    content_file: Path | None,
    owner: str,
    repo: str,
    pr_number: int,
    review_id: int,
) -> str:
    if content_file is not None:
        try:
            body = content_file.read_text(encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(f"Could not read review content file {content_file!s}: {exc}") from exc
    else:
        body = _gh_value(f"repos/{owner}/{repo}/pulls/{pr_number}/reviews/{review_id}", ".body")
    if not body.strip():
        raise RuntimeError("The review body is empty; provide the CCR Markdown content instead.")
    return body


def _load_head_sha(*, owner: str, repo: str, pr_number: int, supplied: str | None) -> str:
    head_sha = supplied.strip() if supplied else _gh_value(f"repos/{owner}/{repo}/pulls/{pr_number}", ".head.sha")
    if not _SHA_PATTERN.fullmatch(head_sha):
        raise ValueError("head SHA must be exactly 40 hexadecimal characters")
    return head_sha


def _load_pr_ref(*, owner: str, repo: str, pr_number: int, jq: str, supplied: str | None) -> str:
    value = supplied.strip() if supplied else _gh_value(f"repos/{owner}/{repo}/pulls/{pr_number}", jq)
    if not value:
        raise ValueError(f"{jq} must be a non-empty string")
    return value


def _load_remote_file_content(*, owner: str, repo: str, path: str, ref: str) -> str:
    """Read a text file from a repository ref, returning an empty value when unavailable."""
    endpoint = f"repos/{owner}/{repo}/contents/{quote(path, safe='')}?ref={quote(ref, safe='')}"
    encoded = _gh_value(endpoint, ".content")
    try:
        return base64.b64decode(encoded).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"Could not decode repository file {path!r} at {ref!r}") from exc


def _copilot_task_provider(*, owner: str, repo: str) -> Any:
    from agentic_devtools.ai_providers import (
        CopilotProvider,
        CopilotProviderConfig,
        ModelDiscovery,
        RequestsHttpTransport,
        get_agent_tasks_headers,
    )

    return CopilotProvider(
        CopilotProviderConfig(
            owner=owner,
            repo=repo,
            base_url="https://api.github.com",
            api_version="2026-03-10",
            timeout_seconds=30.0,
            transport=_AgentTasksPayloadTransport(RequestsHttpTransport()),
            model_discovery=cast(ModelDiscovery, SimpleNamespace(discover_models=lambda: [])),
            auth_header_factory=lambda: get_agent_tasks_headers(_load_token()),
        )
    )


def _dispatch_agent_task(
    *,
    prompt: str,
    owner: str,
    repo: str,
    model: str,
    base_ref: str,
    head_ref: str,
) -> tuple[str, str]:
    from agentic_devtools.ai_providers import TaskRequest

    task = _copilot_task_provider(owner=owner, repo=repo).create_task(
        TaskRequest(
            model_id=model,
            prompt=_strip_copilot_tag(prompt),
            context=f"base_ref={base_ref}; head_ref={head_ref}",
            parameters={},
            metadata={"base_ref": base_ref, "head_ref": head_ref},
        )
    )
    if task.failure is not None:
        raise RuntimeError(task.failure.message)
    task_id = task.task_id
    if task_id is None:
        raise RuntimeError("Copilot provider returned no task ID")
    task_url = f"https://github.com/{owner}/{repo}/tasks/{task_id}"
    return task_id, task_url


def _normalize_task_status(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        return "unknown"
    normalized = value.strip().lower()
    return {"requested": "queued", "running": "in_progress", "waiting": "waiting_for_user"}.get(normalized, normalized)


def _task_snapshot(*, owner: str, repo: str, task_id: str) -> dict[str, Any]:
    task_state = _copilot_task_provider(owner=owner, repo=repo).get_task(task_id)
    if task_state.state is None and task_state.failure is not None:
        raise RuntimeError(task_state.failure.message)
    snapshot = dict(task_state.metadata)
    snapshot.setdefault("state", task_state.state)
    return snapshot


def _task_session_id(snapshot: dict[str, Any]) -> str:
    sessions = snapshot.get("sessions")
    if isinstance(sessions, list):
        for session in reversed(cast(list[Any], sessions)):
            if isinstance(session, dict):
                session_id = cast(dict[str, Any], session).get("id")
                if isinstance(session_id, str) and session_id.strip():
                    return session_id.strip()
    session_id = snapshot.get("session_id")
    return session_id.strip() if isinstance(session_id, str) else ""


def _task_status_from_snapshot(snapshot: dict[str, Any]) -> str:
    sessions = snapshot.get("sessions")
    if isinstance(sessions, list):
        for session in reversed(cast(list[Any], sessions)):
            if isinstance(session, dict):
                session_state = cast(dict[str, Any], session).get("state")
                if isinstance(session_state, str) and session_state.strip():
                    return _normalize_task_status(session_state)
    return _normalize_task_status(snapshot.get("status", snapshot.get("state")))


def _load_task_log(*, owner: str, repo: str, session_id: str) -> str | None:
    if not session_id:
        return None
    cli_environment = os.environ.copy()
    for token_name in ("COPILOT_GITHUB_TOKEN", "SPECKIT_PR_TOKEN", "GH_TOKEN", "GITHUB_TOKEN"):
        cli_environment.pop(token_name, None)
    try:
        result = subprocess.run(
            ["gh", "agent-task", "view", session_id, "--repo", f"{owner}/{repo}", "--log"],
            capture_output=True,
            check=False,
            encoding="utf-8",
            env=cli_environment,
            shell=False,
            text=True,
        )
    except (FileNotFoundError, OSError):
        return None
    output = "\n".join(value for value in (result.stdout, result.stderr) if value)
    return output if output else None


def _extract_task_text(log: str) -> str:
    matches = list(_TASK_FINAL_RESPONSE_MARKER.finditer(log))
    if not matches:
        return ""
    normalized: list[str] = []
    for raw_line in log[matches[-1].end() :].splitlines():
        line = raw_line.strip()
        if not line:
            if normalized and normalized[-1] != "":
                normalized.append("")
            continue
        if line.startswith("• "):
            line = "- " + line[2:]
        if normalized and normalized[-1] and not line.startswith(("- ", "# ")):
            normalized[-1] += " " + line
        else:
            normalized.append(line)
    while normalized and normalized[-1] == "":
        normalized.pop()
    return "\n".join(normalized)


def _terminal_task_text(snapshot: dict[str, Any]) -> str:
    for key in ("result", "output", "message", "error"):
        value = snapshot.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "Agent Task reached a terminal state, but no session log was available."


def _commit_touches_file(*, owner: str, repo: str, commit_sha: str, file_path: str) -> bool:
    if not re.fullmatch(r"[0-9a-fA-F]{7,40}", commit_sha) or not file_path:
        return False
    try:
        paths = _gh_value(
            f"repos/{owner}/{repo}/commits/{commit_sha}",
            ".files[].filename",
        )
    except RuntimeError:
        return False
    return file_path in paths.splitlines()


def _push_verification_status(
    *,
    owner: str,
    repo: str,
    pr_number: int,
    record: dict[str, Any],
    task_text: str,
    agent_comment_text: str,
) -> str:
    evidence_text = f"{task_text}\n{agent_comment_text}".lower()
    no_code_change = any(marker in evidence_text for marker in _NO_CODE_CHANGE_MARKERS)
    reported = _reported_commit_shas(task_text, agent_comment_text)
    reachable = _reachable_reported_commits(
        owner=owner,
        repo=repo,
        pr_number=pr_number,
        reported=reported,
    )
    record["reported_commits"] = reported
    record["reachable_reported_commits"] = reachable
    if no_code_change and not reported and not any(marker in evidence_text for marker in _PUSH_FAILURE_MARKERS):
        return "not_required"
    if not reachable:
        return "unverified"
    file_path = record.get("file_path")
    if isinstance(file_path, str) and file_path:
        if not any(
            _commit_touches_file(owner=owner, repo=repo, commit_sha=commit_sha, file_path=file_path)
            for commit_sha in reachable
        ):
            return "unverified"
    return "verified"


def _build_task_retry_comment(
    *,
    branch: str,
    record: dict[str, Any],
    reason: str,
    task_text: str,
) -> str:
    task_id = record.get("task_id", "unknown")
    file_path = record.get("file_path", "unknown")
    excerpt = task_text[-4000:] if task_text else "No final task text was available."
    return (
        "@copilot - Please continue the existing repair task for this PR in a new session and recover the "
        "unfinished push. Do not create a duplicate task or treat an unrelated commit at the branch tip as "
        "evidence that this finding was fixed.\n\n"
        f"Existing Agent Task ID: {task_id}\n"
        f"Assigned file: {file_path}\n"
        f"Target branch: {branch}\n"
        f"Retry reason: {reason}\n\n"
        "Inspect the existing worktree and commit, then inspect the current remote branch. If the remote has "
        "advanced, fetch it and rebase your local work onto it before pushing. Resolve conflicts while keeping "
        "the assigned fix, rerun targeted checks, and push a new commit with a plain `git push`. Do not amend "
        "or force-push. If the server reports a protected ref or repository-rule violation, capture the complete "
        "error and stop.\n\n"
        "Before reporting success, verify that the remote branch SHA equals your local HEAD SHA and that the "
        "remote commit actually changes the assigned file.\n\n"
        "Previous task result:\n"
        f"```text\n{excerpt}\n```"
    )


def _request_task_retry(
    *,
    owner: str,
    repo: str,
    provider: Any,
    pr_number: int,
    branch: str,
    record: dict[str, Any],
    reason: str,
    task_text: str,
) -> int:
    retry_count = record.get("retry_count", 0)
    if not isinstance(retry_count, int) or retry_count >= _MAX_TASK_RETRIES:
        raise RuntimeError("Maximum Agent Task retry count reached")
    post_comment = getattr(provider, "post_comment_as_pr_token", None)
    if not callable(post_comment):
        raise RuntimeError("Provider cannot post a Copilot retry steering comment")
    comment_id = post_comment(
        pr_number,
        _build_task_retry_comment(branch=branch, record=record, reason=reason, task_text=task_text),
    )
    if not isinstance(comment_id, int) or comment_id <= 0:
        raise RuntimeError("Copilot retry steering comment returned an invalid comment ID")
    _PR_COMMIT_CACHE.pop((owner, repo, pr_number), None)
    record["retry_count"] = retry_count + 1
    record["retry_status"] = "requested"
    record["retry_poll_count"] = 0
    record["retry_comment_id"] = comment_id
    record["retry_reason"] = reason
    record["status"] = "retry_requested"
    record["agent_comment"] = "🔃"
    record["agent_task_text"] = "🔃"
    record["agent_comment_text"] = ""
    record["resolution_decision"] = "-"
    record["resolution_text"] = "🔃 Push verification retry requested."
    return comment_id


def _advance_task_retry(record: dict[str, Any], snapshot: dict[str, Any]) -> bool:
    if record.get("retry_status") != "requested":
        return True
    latest_session_id = _task_session_id(snapshot)
    if latest_session_id and latest_session_id != record.get("session_id"):
        record["session_id"] = latest_session_id
        session_ids = record.setdefault("session_ids", [])
        if isinstance(session_ids, list) and latest_session_id not in session_ids:
            session_ids.append(latest_session_id)
        record["retry_status"] = "running"
        record["status"] = _task_status_from_snapshot(snapshot)
        record["agent_comment"] = "🔃"
        record["agent_task_text"] = "🔃"
        record["resolution_decision"] = "-"
        record["resolution_text"] = "-"
        record["thread_resolved"] = False
        return True
    poll_count = record.get("retry_poll_count", 0)
    record["retry_poll_count"] = poll_count + 1 if isinstance(poll_count, int) else 1
    if record["retry_poll_count"] >= _MAX_RETRY_SESSION_POLLS:
        record["retry_status"] = "exhausted"
        record["status"] = "failed"
        record["agent_comment"] = "None"
        record["agent_task_text"] = "Retry session did not start."
        record["push_verification"] = "unverified"
        record["resolution_decision"] = "do_not_resolve"
        record["resolution_basis"] = "retry session was not observed"
        record["resolution_text"] = "Agent Task retry did not start a new session; thread left unresolved."
    return False


def _comment_metadata(comment: Any, review_url: str) -> dict[str, Any]:
    path = comment.path
    line_range = "None"
    start_line = comment.start_line if isinstance(comment.start_line, int) else None
    end_line = comment.line if isinstance(comment.line, int) else None
    if comment.line is not None:
        start = start_line if start_line is not None else comment.line
        line_range = str(start) if start == comment.line else f"{start}–{comment.line}"
    else:
        match = re.match(r"^(?P<path>.+):(?P<line>\d+(?:[-–]\d+)?)$", path)
        if match:
            path = match.group("path")
            line_range = match.group("line")
            bounds = line_range.replace("–", "-").split("-", 1)
            start_line = int(bounds[0])
            end_line = int(bounds[-1])
    suppressed = comment.is_suppressed and not comment.html_url
    return {
        "is_suppressed": suppressed,
        "comment_id": comment.id if comment.id > 0 else None,
        "file_path": path,
        "line_range": line_range,
        "start_line": start_line,
        "end_line": end_line,
        "original_comment": f"[CCR review]({review_url}) (within body)"
        if suppressed
        else f"[Original comment]({comment.html_url})"
        if comment.html_url
        else "None",
        "comment_type": "suppressed" if suppressed else "inline",
    }


def _filter_unresolved_review_comments(*, provider: Any, pr_number: int, comments: list[Any]) -> list[Any]:
    """Discard comments whose review thread is already resolved.

    Suppressed findings use synthetic negative IDs until a thread is created, so they
    remain eligible for dispatch. Providers without thread-state support retain the
    previous behavior and return the recovered comments unchanged.
    """
    result = fetch_review_thread_states(provider, pr_number)
    if result.degraded:
        return comments
    thread_states = result.states
    return [
        comment
        for comment in comments
        if not isinstance(getattr(comment, "id", None), int)
        or comment.id < 0
        or not thread_states.get(comment.id, (False, False))[0]
    ]


def _parse_follow_up_issue(task_text: str) -> dict[str, Any] | None:
    """Parse the exact structured option-four issue block emitted by the repair agent."""
    marker_index = task_text.find(_FOLLOW_UP_MARKER)
    if marker_index < 0:
        return None
    fenced = re.search(r"```json\s*(.*?)\s*```", task_text[marker_index:], flags=re.DOTALL)
    if fenced is None:
        return None
    try:
        candidate = json.loads(fenced.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(candidate, dict):
        return None
    candidate = cast(dict[str, Any], candidate)
    title = candidate.get("title")
    body = candidate.get("body")
    raw_labels: Any = candidate.get("labels", [])
    issue_type = candidate.get("type")
    if not isinstance(raw_labels, list):
        return None
    labels: list[str] = []
    for raw_label in raw_labels:
        if not isinstance(raw_label, str) or raw_label not in {"bug", "enhancement", "documentation"}:
            return None
        labels.append(raw_label)
    if (
        not isinstance(title, str)
        or not title.strip()
        or not isinstance(body, str)
        or not body.strip()
        or issue_type is not None
        and (not isinstance(issue_type, str) or issue_type not in {"Bug", "Feature", "Task"})
    ):
        return None
    return {
        "title": title.strip(),
        "labels": labels,
        "type": issue_type,
        "body": body.strip(),
    }


def _create_follow_up_issue(*, owner: str, repo: str, issue: dict[str, Any]) -> tuple[int, str]:
    """Create a structured GitHub follow-up issue and return its number and URL."""
    from agentic_devtools.ai_providers import RequestsHttpTransport, get_agent_tasks_headers

    payload: dict[str, Any] = {
        "title": issue["title"],
        "body": issue["body"],
        "labels": issue["labels"],
    }
    if issue.get("type") is not None:
        payload["type"] = issue["type"]
    response = RequestsHttpTransport().request(
        "POST",
        f"https://api.github.com/repos/{owner}/{repo}/issues",
        headers={**get_agent_tasks_headers(_load_token()), "Content-Type": "application/json"},
        json_body=payload,
        timeout=30.0,
    )
    if response.status_code != 201 or not isinstance(response.body, dict):
        raise RuntimeError(f"Follow-up issue creation failed (HTTP {response.status_code})")
    response_body = cast(dict[str, Any], getattr(response, "body", {}))
    number = response_body.get("number")
    html_url = response_body.get("html_url")
    if not isinstance(number, int) or number <= 0 or not isinstance(html_url, str) or not html_url:
        raise RuntimeError("Follow-up issue response did not contain a valid number and URL")
    return number, html_url


def _post_follow_up_reply(*, owner: str, repo: str, pr_number: int, comment_id: int, issue_number: int) -> None:
    """Tell the review thread which follow-up issue was created."""
    from agentic_devtools.ai_providers import RequestsHttpTransport, get_agent_tasks_headers

    response = RequestsHttpTransport().request(
        "POST",
        f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies",
        headers={**get_agent_tasks_headers(_load_token()), "Content-Type": "application/json"},
        json_body={"body": f"Follow-up issue created: #{issue_number} - before resolving it."},
        timeout=30.0,
    )
    if response.status_code != 201:
        raise RuntimeError(f"Follow-up issue reply failed (HTTP {response.status_code})")


def _build_suppressed_review_comment_payload(*, comment: Any, head_sha: str, marker: str) -> dict[str, Any]:
    """Build an unresolved GitHub review-comment payload for a suppressed finding."""
    path = getattr(comment, "path", "")
    body = getattr(comment, "body", "")
    if not isinstance(path, str) or not path or not isinstance(body, str):
        raise ValueError("suppressed review comment must have a non-empty path and string body")
    line = getattr(comment, "line", None)
    start_line = getattr(comment, "start_line", None)
    if line is not None and (not isinstance(line, int) or line <= 0):
        raise ValueError("suppressed review comment line must be a positive integer or None")
    if start_line is not None and (not isinstance(start_line, int) or start_line <= 0):
        raise ValueError("suppressed review comment start_line must be a positive integer or None")
    if line is not None:
        path_value = path
        line_value = str(start_line or line) if start_line != line else str(line)
    else:
        match = re.match(r"^(?P<path>.+):(?P<line>\d+(?:[-–]\d+)?)$", path)
        path_value = match.group("path") if match else path
        line_value = match.group("line") if match else "None"
    payload: dict[str, Any] = {
        "body": f"{marker}\n\n{body}",
        "commit_id": head_sha,
        "path": path_value,
    }
    line_match = re.fullmatch(r"(?P<start>\d+)(?:[-–](?P<end>\d+))?", line_value)
    if line_match is None:
        payload["subject_type"] = "file"
        return payload
    start = int(line_match.group("start"))
    end = int(line_match.group("end") or start)
    payload.update({"line": end, "side": "RIGHT"})
    if start != end:
        payload.update({"start_line": start, "start_side": "RIGHT"})
    return payload


def _post_suppressed_review_comment(
    *,
    owner: str,
    repo: str,
    pr_number: int,
    comment: Any,
    head_sha: str,
    marker: str,
) -> tuple[int, str]:
    """Create one unresolved review-comment root and return its ID and URL."""
    from agentic_devtools.ai_providers import RequestsHttpTransport, get_agent_tasks_headers

    transport = RequestsHttpTransport()
    endpoint = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/comments"
    headers = {**get_agent_tasks_headers(_load_token()), "Content-Type": "application/json"}
    payload = _build_suppressed_review_comment_payload(comment=comment, head_sha=head_sha, marker=marker)
    response = transport.request(
        "POST",
        endpoint,
        headers=headers,
        json_body=payload,
        timeout=30.0,
    )
    if response.status_code == 422 and payload.get("subject_type") != "file":
        payload = {
            key: value for key, value in payload.items() if key not in {"line", "side", "start_line", "start_side"}
        }
        payload["subject_type"] = "file"
        response = transport.request(
            "POST",
            endpoint,
            headers=headers,
            json_body=payload,
            timeout=30.0,
        )
    if response.status_code != 201 or not isinstance(response.body, dict):
        raise RuntimeError(f"Could not create suppressed review thread (HTTP {response.status_code})")
    raw_response_body: Any = getattr(response, "body", None)
    if not isinstance(raw_response_body, dict):
        raise RuntimeError("Suppressed review thread response body was not an object")
    response_body: dict[str, Any] = {str(key): value for key, value in cast(dict[Any, Any], raw_response_body).items()}
    comment_id = response_body.get("id")
    html_url = response_body.get("html_url")
    if not isinstance(comment_id, int) or comment_id <= 0 or not isinstance(html_url, str) or not html_url:
        raise RuntimeError("Suppressed review thread response did not contain a valid ID and URL")
    return comment_id, html_url


def _ensure_suppressed_review_thread(
    *,
    owner: str,
    repo: str,
    pr_number: int,
    comment: Any,
    head_sha: str,
    marker: str,
    provider: Any,
) -> tuple[int, str]:
    """Reuse a marked suppressed thread or create one when none exists."""
    try:
        existing = [item for item in provider.list_all_review_comments(pr_number) if marker in item.body]
    except Exception:
        existing = []
    for item in existing:
        if isinstance(item.id, int) and item.id > 0 and item.html_url:
            return item.id, item.html_url
    return _post_suppressed_review_comment(
        owner=owner,
        repo=repo,
        pr_number=pr_number,
        comment=comment,
        head_sha=head_sha,
        marker=marker,
    )


def _table_cell(value: object) -> str:
    if value is None:
        return "None"
    return str(value).replace("|", "\\|").replace("\r\n", "<br>").replace("\n", "<br>")


def _collapsible_task_text_cell(value: object, *, summary: str = "View full task text") -> str:
    if value is None:
        return _table_cell(value)
    if value in ("-", "🔃"):
        return f"<details>\n<summary>{escape(summary)}</summary>\n\n{_table_cell(value)}\n\n</details>"
    return f"<details><summary>{escape(summary)}</summary><br><pre>{escape(str(value))}</pre></details>"


def _unique_link_label(value: object, *, fallback: str = "-") -> str:
    if not isinstance(value, str):
        return fallback
    url_match = re.search(r"https?://[^\s)]+", value)
    if url_match is None:
        return fallback
    url = url_match.group(0)
    discussion_match = re.search(r"#discussion_r(\d+)", url)
    if discussion_match is not None:
        return discussion_match.group(1)
    task_match = re.search(r"/tasks/([^/?#]+)", url)
    if task_match is not None:
        return task_match.group(1)
    return fallback


def _unique_markdown_link(value: object, *, fallback: str = "-") -> str:
    if not isinstance(value, str):
        return _table_cell(value)
    url_match = re.search(r"https?://[^\s)]+", value)
    if url_match is None:
        return _table_cell(value)
    url = url_match.group(0)
    return f"[{_unique_link_label(url, fallback=fallback)}]({url})"


def _status_marker(record: dict[str, Any]) -> str:
    if record["status"] == "completed":
        return "✅"
    if record["status"] in {"failed", "timed_out", "cancelled"}:
        return "❌"
    return "🔃"


def _find_agent_comment_url(
    *,
    provider: Any,
    pr_number: int,
    record: dict[str, Any],
    task_text: str,
) -> tuple[str | None, bool]:
    models = importlib.import_module("agentic_devtools.cli.ci.models")
    is_copilot_login = cast(Callable[[object], bool], getattr(models, "is_copilot_login"))
    is_agent_login = cast(Callable[[object], bool], getattr(models, "is_cloud_coding_agent_login"))
    referenced_ids = {int(value) for value in _TASK_COMMENT_ID_PATTERN.findall(task_text)}
    comment_id = record.get("comment_id")
    if isinstance(comment_id, int) and comment_id > 0:
        referenced_ids.add(comment_id)
    try:
        comments = provider.list_all_review_comments(pr_number)
    except Exception:
        return None, False
    candidates = [
        comment
        for comment in comments
        if comment.id in referenced_ids
        and comment.id != comment_id
        and comment.html_url
        and (is_agent_login(comment.author_login) or is_copilot_login(comment.author_login))
    ]
    if not candidates and isinstance(comment_id, int) and comment_id > 0:
        candidates = [
            comment
            for comment in comments
            if comment.in_reply_to_id == comment_id
            and comment.html_url
            and (is_agent_login(comment.author_login) or is_copilot_login(comment.author_login))
        ]
    candidates.sort(key=lambda comment: comment.id, reverse=True)
    for candidate in candidates:
        return candidate.html_url, True
    return None, True


def _find_agent_comment_text(*, provider: Any, pr_number: int, record: dict[str, Any]) -> str:
    """Return the full correlated Copilot reply body when it is available."""
    agent_url = record.get("agent_comment")
    if not isinstance(agent_url, str) or not agent_url.startswith(("https://", "http://")):
        return ""
    try:
        comments = provider.list_all_review_comments(pr_number)
    except Exception:
        return ""
    for comment in comments:
        if comment.html_url == agent_url and isinstance(comment.body, str):
            return comment.body
    return ""


def _build_resolution_adjudication_prompt(
    *,
    record: dict[str, Any],
    task_text: str,
    file_diff: str,
    deterministic_basis: str | None = None,
    reachable_commits: list[str] | None = None,
) -> str:
    """Build the bounded evidence prompt used to decide whether a thread is resolvable."""
    evidence: dict[str, Any] = {
        "comment_type": record.get("comment_type"),
        "file_path": record.get("file_path"),
        "line_range": record.get("line_range"),
        "original_comment": record.get("original_comment"),
        "agent_comment": record.get("agent_comment_text") or record.get("agent_comment"),
        "agent_task_text": task_text,
        "agent_task_status": record.get("status"),
        "pre_to_post_file_diff": file_diff,
        "deterministic_post_dispatch_evidence": deterministic_basis,
        "reachable_reported_commits": reachable_commits or [],
        "follow_up_issue": record.get("follow_up_issue"),
    }
    return (
        "Decide whether the assigned GitHub review comment should be resolved. Default to resolving it. "
        "The absolute first characters of the response must be exactly AI_PR_LOOP_RESOLVE or "
        "AI_PR_LOOP_DO_NOT_RESOLVE. The parser scans the entire raw response and the first "
        "occurrence of either marker wins. "
        "Treat deterministic post-dispatch evidence as supporting context, not as automatic proof "
        "that the thread is resolved. "
        "Use AI_PR_LOOP_DO_NOT_RESOLVE only when the code change clearly does not address the comment "
        "or the task clearly failed. Do not veto because the cloud agent "
        "could not post, resolve, or push through a protected branch; those are infrastructure limitations, "
        "not evidence that the code change is incorrect. Explain your decision after the marker.\n\n"
        + json.dumps(evidence, indent=2, ensure_ascii=False)
    )


def _build_file_change_evidence(*, owner: str, repo: str, record: dict[str, Any]) -> str:
    """Build a bounded before/after diff for the finding's file."""
    initial_ref = record.get("initial_head_sha")
    if not isinstance(initial_ref, str) or not initial_ref:
        return "unavailable: initial HEAD SHA was not recorded"
    try:
        current_ref = _gh_value(f"repos/{owner}/{repo}/pulls/{record['pr_number']}", ".head.sha")
        before = _load_remote_file_content(
            owner=owner,
            repo=repo,
            path=str(record["file_path"]),
            ref=initial_ref,
        )
        after = _load_remote_file_content(
            owner=owner,
            repo=repo,
            path=str(record["file_path"]),
            ref=current_ref,
        )
    except (RuntimeError, KeyError, TypeError) as exc:
        return f"unavailable: {exc}"
    diff = difflib.unified_diff(
        before.splitlines(),
        after.splitlines(),
        fromfile=f"before/{record['file_path']}",
        tofile=f"after/{record['file_path']}",
        lineterm="",
    )
    return "\n".join(diff) or "no file changes"


def _load_post_task_diff(*, owner: str, repo: str, provider: Any, record: dict[str, Any]) -> str:
    """Load the unified diff between the dispatch HEAD and current PR HEAD."""
    initial_ref = record.get("initial_head_sha")
    pr_number = record.get("pr_number")
    if not isinstance(initial_ref, str) or not initial_ref or not isinstance(pr_number, int):
        return ""
    try:
        current_ref = _gh_value(f"repos/{owner}/{repo}/pulls/{pr_number}", ".head.sha")
        if current_ref == initial_ref:
            return ""
        get_diff = getattr(provider, "get_commit_range_diff", None)
        if not callable(get_diff):
            return ""
        diff = get_diff(initial_ref, current_ref)
        return diff if isinstance(diff, str) else ""
    except Exception:
        return ""


def _run_single_copilot_adjudication(prompt: str, *, model: str = "gpt-5.6-luna") -> str:
    """Run one read-only Copilot SDK adjudication attempt and return its text."""

    async def _complete() -> str:
        from copilot import CopilotClient, PermissionHandler

        async with CopilotClient() as client:
            async with await client.create_session(
                on_permission_request=PermissionHandler.approve_all,
                model=model,
                tools=[],
            ) as session:
                response = await session.send_and_wait(prompt)
                content = getattr(getattr(response, "data", None), "content", "")
                return content if isinstance(content, str) else ""

    return asyncio.run(_complete())


def _contains_resolution_marker(text: str) -> bool:
    return _RESOLVE_MARKER in text or _DO_NOT_RESOLVE_MARKER in text


def _run_copilot_adjudication(prompt: str, *, model: str = "gpt-5.6-luna") -> str:
    """Retry SDK failures and markerless responses, returning the final attempt text."""
    last_text = ""
    for attempt in range(_SDK_ADJUDICATION_ATTEMPTS):
        try:
            last_text = _run_single_copilot_adjudication(prompt, model=model)
        except Exception as exc:
            last_text = f"Copilot SDK attempt {attempt + 1} failed: {exc}"
        if _contains_resolution_marker(last_text) or attempt == _SDK_ADJUDICATION_ATTEMPTS - 1:
            return last_text
        time.sleep(_SDK_RETRY_DELAYS_SECONDS[attempt])
    return last_text


def _first_resolution_marker(text: str) -> str | None:
    """Return whichever resolution marker occurs first anywhere in *text*."""
    matches = [
        (position, marker)
        for marker in (_RESOLVE_MARKER, _DO_NOT_RESOLVE_MARKER)
        if (position := text.find(marker)) >= 0
    ]
    return min(matches)[1] if matches else None


def _should_resolve_comment(record: dict[str, Any], prompt: str) -> bool:
    """Resolve only when the first resolution marker is affirmative."""
    if record.get("status") != "completed":
        return False
    decision, _resolution_text = _adjudicate_resolution(record, prompt)
    return decision == "resolve"


def _adjudicate_resolution(record: dict[str, Any], prompt: str) -> tuple[str, str]:
    """Return a resolution decision and preserve the complete SDK response text."""
    if record.get("status") != "completed":
        return "do_not_resolve", "Agent Task did not complete successfully; thread left unresolved."
    resolution_text = _run_copilot_adjudication(prompt)
    marker = _first_resolution_marker(resolution_text)
    if marker == _DO_NOT_RESOLVE_MARKER:
        return "do_not_resolve", resolution_text or _DO_NOT_RESOLVE_MARKER
    if marker is None:
        fallback = "Copilot SDK returned no decision marker after three attempts; thread left unresolved."
        return "do_not_resolve", f"{resolution_text}\n\n{fallback}".strip()
    return "resolve", resolution_text


def _deterministic_resolution_basis(diff_text: str, record: dict[str, Any]) -> str | None:
    """Return deterministic diff proof for a finding, or ``None`` when ambiguous."""
    path = record.get("file_path")
    if not isinstance(path, str) or not path:
        return None
    start_line = record.get("start_line")
    end_line = record.get("end_line")
    if isinstance(start_line, int) and start_line > 0:
        if check_lines_modified(diff_text, path, start_line, end_line if isinstance(end_line, int) else start_line):
            return "deterministic line diff"
        return None
    if re.search(rf"^diff --git a/{re.escape(path)} b/{re.escape(path)}$", diff_text, flags=re.MULTILINE):
        return "deterministic file diff"
    return None


def _reported_commit_shas(*texts: str) -> list[str]:
    """Extract plausible full or abbreviated commit SHAs from task evidence."""
    found: list[str] = []
    for text in texts:
        for candidate in re.findall(r"\b[0-9a-fA-F]{7,40}\b", text):
            normalized = candidate.lower()
            if normalized not in found:
                found.append(normalized)
    return found


def _reachable_reported_commits(*, owner: str, repo: str, pr_number: int, reported: list[str]) -> list[str]:
    """Return reported commit prefixes that are reachable from the current PR."""
    if not reported:
        return []
    cache_key = (owner, repo, pr_number)
    reachable = _PR_COMMIT_CACHE.get(cache_key)
    if reachable is None:
        try:
            result = subprocess.run(
                ["gh", "api", f"repos/{owner}/{repo}/pulls/{pr_number}/commits", "--paginate", "--jq", ".[].sha"],
                capture_output=True,
                check=True,
                encoding="utf-8",
                shell=False,
                text=True,
            )
            reachable = tuple(line.strip().lower() for line in result.stdout.splitlines() if line.strip())
        except (FileNotFoundError, OSError, subprocess.CalledProcessError):
            reachable = ()
        _PR_COMMIT_CACHE[cache_key] = reachable
    return [reported_sha for reported_sha in reported if any(sha.startswith(reported_sha) for sha in reachable)]


def _finalize_task_record(
    *,
    owner: str,
    repo: str,
    pr_number: int,
    provider: Any,
    record: dict[str, Any],
    snapshot: dict[str, Any],
) -> None:
    session_id = _task_session_id(snapshot)
    if session_id:
        record["session_id"] = session_id
        session_ids = record.setdefault("session_ids", [])
        if isinstance(session_ids, list) and session_id not in session_ids:
            session_ids.append(session_id)

    if record["agent_task_text"] == "🔃":
        log = _load_task_log(owner=owner, repo=repo, session_id=record["session_id"])
        if log is not None:
            record["agent_task_text"] = _extract_task_text(log) or None
        if record["agent_task_text"] == "🔃":
            record["agent_task_text"] = _terminal_task_text(snapshot)

    if record["agent_comment"] == "🔃":
        task_text = record["agent_task_text"] if isinstance(record["agent_task_text"], str) else ""
        comment_url, lookup_succeeded = _find_agent_comment_url(
            provider=provider,
            pr_number=pr_number,
            record=record,
            task_text=task_text,
        )
        if lookup_succeeded:
            record["agent_comment"] = comment_url
    if record.get("resolution_decision", "-") == "-" and record.get("agent_comment_text") in (None, ""):
        record["agent_comment_text"] = _find_agent_comment_text(
            provider=provider,
            pr_number=pr_number,
            record=record,
        )

    task_text = record["agent_task_text"] if isinstance(record["agent_task_text"], str) else ""
    agent_comment_text = record.get("agent_comment_text")
    if not isinstance(agent_comment_text, str):
        agent_comment_text = ""
    record["push_verification"] = _push_verification_status(
        owner=owner,
        repo=repo,
        pr_number=pr_number,
        record=record,
        task_text=task_text,
        agent_comment_text=agent_comment_text,
    )
    if (
        record["push_verification"] not in {"verified", "not_required"}
        and record.get("retry_count", 0) < _MAX_TASK_RETRIES
    ):
        branch = record.get("head_ref")
        if not isinstance(branch, str) or not branch:
            branch = "the current PR branch"
        try:
            _request_task_retry(
                owner=owner,
                repo=repo,
                provider=provider,
                pr_number=pr_number,
                branch=branch,
                record=record,
                reason="the task's commit could not be verified on the remote PR branch",
                task_text=task_text,
            )
        except RuntimeError as exc:
            record["retry_status"] = "unavailable"
            record["retry_error"] = str(exc)
            record["status"] = "failed"
        else:
            return

    if record.get("follow_up_issue", "-") == "-":
        follow_up = _parse_follow_up_issue(task_text)
        if follow_up is None:
            record["follow_up_issue"] = "None"
        else:
            try:
                issue_number, issue_url = _create_follow_up_issue(owner=owner, repo=repo, issue=follow_up)
                record["follow_up_issue"] = f"#{issue_number}"
                record["follow_up_issue_url"] = issue_url
                comment_id = record.get("comment_id")
                if isinstance(comment_id, int) and comment_id > 0:
                    _post_follow_up_reply(
                        owner=owner,
                        repo=repo,
                        pr_number=pr_number,
                        comment_id=comment_id,
                        issue_number=issue_number,
                    )
            except Exception as exc:
                record["follow_up_issue"] = "None"
                record["follow_up_issue_error"] = str(exc)

    if record.get("resolution_decision", "-") == "-":
        record["pr_number"] = pr_number
        reported_commits = _reported_commit_shas(task_text, agent_comment_text)
        reachable_commits = _reachable_reported_commits(
            owner=owner,
            repo=repo,
            pr_number=pr_number,
            reported=reported_commits,
        )
        record["reported_commits"] = reported_commits
        record["reachable_reported_commits"] = reachable_commits
        if record.get("follow_up_issue_error"):
            record["resolution_decision"] = "do_not_resolve"
            record["resolution_text"] = f"Follow-up issue creation failed: {record['follow_up_issue_error']}"
            record["resolution_basis"] = "follow-up issue creation failure"
        elif record.get("push_verification") not in {"verified", "not_required"}:
            record["resolution_decision"] = "do_not_resolve"
            record["resolution_text"] = "The task's changes could not be verified on the remote PR branch."
            record["resolution_basis"] = "remote push verification failure"
        else:
            post_task_diff = _load_post_task_diff(owner=owner, repo=repo, provider=provider, record=record)
            deterministic_basis = _deterministic_resolution_basis(post_task_diff, record)
            record["resolution_basis"] = (
                f"Copilot SDK adjudication ({deterministic_basis})"
                if deterministic_basis is not None
                else "Copilot SDK adjudication"
            )
            file_diff = _build_file_change_evidence(owner=owner, repo=repo, record=record)
            adjudication_prompt = _build_resolution_adjudication_prompt(
                record=record,
                task_text=task_text,
                file_diff=file_diff,
                deterministic_basis=deterministic_basis,
                reachable_commits=reachable_commits,
            )
            decision, resolution_text = _adjudicate_resolution(record, adjudication_prompt)
            record["resolution_decision"] = decision
            record["resolution_text"] = resolution_text
            if _first_resolution_marker(resolution_text) is None:
                record["resolution_basis"] = "Copilot SDK adjudication failure after three attempts"

    if record.get("resolution_decision") == "resolve" and not record["thread_resolved"]:
        try:
            _resolve_completed_inline_comment(
                owner=owner,
                repo=repo,
                pr_number=pr_number,
                record=record,
            )
        except RuntimeError as exc:
            record["resolution_error"] = str(exc)


def _build_task_result_comment(*, review_url: str, ordinal: int, record: dict[str, Any]) -> str:
    """Build the compact tracking reply for one dispatched finding."""
    agent_comment = record.get("agent_comment")
    if isinstance(agent_comment, str) and agent_comment.startswith(("https://", "http://")):
        agent_comment = _unique_markdown_link(agent_comment)
    original_comment = _unique_markdown_link(record.get("original_comment"))
    task_url = record.get("task_url")
    task_link = (
        f"[{_unique_link_label(task_url)}]({task_url})"
        if isinstance(task_url, str) and task_url.startswith(("https://", "http://"))
        else "-"
    )
    follow_up = record.get("follow_up_issue", "-")
    if record.get("follow_up_issue_url"):
        follow_up = f"[{follow_up}]({record['follow_up_issue_url']})"
    resolution_decision = {"resolve": "Resolve", "do_not_resolve": "Do not resolve"}.get(
        str(record.get("resolution_decision", "-")), "-"
    )
    status_details = f"{_status_marker(record)} {record.get('status', '-')}"
    file_path_details = f"`{record.get('file_path', '-')}`"
    first_table = [
        "| Field | Details |",
        "|---|---|",
        f"| Comment # | {_table_cell(ordinal)} |",
        f"| Agent task | {task_link} |",
        f"| Agent task status | {_table_cell(status_details)} |",
        f"| Push verification | {_table_cell(record.get('push_verification', '-'))} |",
        f"| Retry status | {_table_cell(record.get('retry_status', 'none'))} |",
        f"| File path | {_table_cell(file_path_details)} |",
        f"| Line range | {_table_cell(record.get('line_range', '-'))} |",
        f"| Original comment | {original_comment} |",
        f"| Comment type | {_table_cell(record.get('comment_type', '-'))} |",
        f"| Agent reply to original comment | {agent_comment or '-'} |",
        "",
        _collapsible_task_text_cell(record.get("agent_task_text", "🔃"), summary="Agent task text"),
        "",
        "| Field | Details |",
        "|---|---|",
        f"| Follow-up issue | {follow_up} |",
        f"| Resolution decision | {_table_cell(resolution_decision)} |",
        f"| Resolution basis | {_table_cell(record.get('resolution_basis', '-'))} |",
        "",
        _collapsible_task_text_cell(record.get("resolution_text", "-"), summary="Resolution text"),
        "",
        f"[CCR review]({review_url})",
    ]
    return "\n".join(first_table)


def _post_task_result_reply(
    *,
    owner: str,
    repo: str,
    pr_number: int,
    comment_id: int,
    body: str,
) -> tuple[int, str]:
    """Post one tracking reply to the assigned review comment."""
    from agentic_devtools.ai_providers import RequestsHttpTransport, get_agent_tasks_headers

    response = RequestsHttpTransport().request(
        "POST",
        f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies",
        headers={**get_agent_tasks_headers(_load_token()), "Content-Type": "application/json"},
        json_body={"body": body},
        timeout=30.0,
    )
    if response.status_code != 201:
        raise RuntimeError(f"Tracking reply failed (HTTP {response.status_code})")
    response_body: Any = getattr(response, "body", {})
    if not isinstance(response_body, dict):
        raise RuntimeError("Tracking reply response body was not an object")
    reply_id = response_body.get("id")
    reply_url = response_body.get("html_url")
    if not isinstance(reply_id, int) or reply_id <= 0 or not isinstance(reply_url, str) or not reply_url:
        raise RuntimeError("Tracking reply response did not contain a valid ID and URL")
    return reply_id, reply_url


def _update_task_result_reply(*, owner: str, repo: str, comment_id: int, body: str) -> None:
    """Update one existing tracking reply in place."""
    from agentic_devtools.ai_providers import RequestsHttpTransport, get_agent_tasks_headers

    response = RequestsHttpTransport().request(
        "PATCH",
        f"https://api.github.com/repos/{owner}/{repo}/pulls/comments/{comment_id}",
        headers={**get_agent_tasks_headers(_load_token()), "Content-Type": "application/json"},
        json_body={"body": body},
        timeout=30.0,
    )
    if not 200 <= response.status_code < 300:
        raise RuntimeError(f"Tracking reply update failed (HTTP {response.status_code})")


def _sync_task_result_reply(*, owner: str, repo: str, pr_number: int, review_url: str, record: dict[str, Any]) -> None:
    """Create or update the tracking reply for one task."""
    body = _build_task_result_comment(review_url=review_url, ordinal=int(record["ordinal"]), record=record)
    tracking_id = record.get("tracking_comment_id")
    if isinstance(tracking_id, int) and tracking_id > 0:
        _update_task_result_reply(owner=owner, repo=repo, comment_id=tracking_id, body=body)
        return
    comment_id = record.get("comment_id")
    if not isinstance(comment_id, int) or comment_id <= 0:
        raise RuntimeError("Cannot create a tracking reply without an assigned review comment ID")
    reply_id, reply_url = _post_task_result_reply(
        owner=owner,
        repo=repo,
        pr_number=pr_number,
        comment_id=comment_id,
        body=body,
    )
    record["tracking_comment_id"] = reply_id
    record["tracking_comment_url"] = reply_url


def _resolve_completed_inline_comment(*, owner: str, repo: str, pr_number: int, record: dict[str, Any]) -> None:
    if record["thread_resolved"]:
        return
    comment_id = record["comment_id"]
    if not isinstance(comment_id, int) or comment_id <= 0:
        return
    resolver_module = importlib.import_module("agentic_devtools.cli.github.resolve_review_threads")
    resolve_review_threads = cast(Callable[..., dict[str, Any]], getattr(resolver_module, "resolve_review_threads"))
    result: Any = resolve_review_threads(pr_number, f"{owner}/{repo}", comment_ids=[comment_id])
    if not result.get("verified"):
        raise RuntimeError(f"Review thread resolution was not verified for comment {comment_id}")
    record["thread_resolved"] = True


def _tasks_ready_for_takeover(task_records: list[dict[str, Any]]) -> bool:
    """Return whether every task completed, was delivered, and its thread resolved."""
    return bool(task_records) and all(
        record.get("status") == "completed"
        and record.get("thread_resolved") is True
        and record.get("push_verification") in {"verified", "not_required"}
        for record in task_records
    )


def _run_takeover_after_monitor(*, owner: str, repo: str, pr_number: int, provider: Any) -> None:
    """Run the repository's real takeover action after dispatch completion."""
    from agentic_devtools.cli.ci.pipeline.actions.takeover import TakeOverAutomationCommitAction
    from agentic_devtools.cli.ci.pipeline.models import ActionDecision
    from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, build_pr_state_snapshot

    snapshot = build_pr_state_snapshot(provider, pr_number)
    action = TakeOverAutomationCommitAction()
    derived = DerivedState(snapshot)
    evaluation = action.evaluate(snapshot, derived)
    print(f"takeover_decision={evaluation.decision.value}")
    if evaluation.decision != ActionDecision.EXECUTE:
        print(f"takeover_details={evaluation.details}")
        return
    result = action.execute(provider, snapshot, derived)
    print(f"takeover_result={result.decision.value}")
    if result.decision == ActionDecision.FAILED:
        raise RuntimeError(result.error or "Takeover action failed")


def _state_path(output_dir: Path, pr_number: int, review_id: int) -> Path:
    return output_dir / f"ai-pr-loop-dispatch-{pr_number}-{review_id}-state.json"


def _load_monitor_records(
    *,
    path: Path,
    owner: str,
    repo: str,
    pr_number: int,
    review_id: int,
) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(payload, dict):
        return []
    if (
        payload.get("owner") != owner
        or payload.get("repo") != repo
        or payload.get("pr_number") != pr_number
        or payload.get("review_id") != review_id
    ):
        return []
    records = payload.get("records")
    if not isinstance(records, list):
        return []
    return [record for record in records if isinstance(record, dict) and record.get("task_id")]


def _record_is_complete(record: dict[str, Any]) -> bool:
    return (
        isinstance(record.get("task_id"), str)
        and record.get("status") in _TERMINAL_TASK_STATES
        and record.get("resolution_decision") != "-"
        and record.get("push_verification") in {"verified", "not_required"}
        and (
            record.get("status") != "completed"
            or record.get("thread_resolved") is True
            or record.get("resolution_decision") == "do_not_resolve"
        )
    )


def _find_resume_record(records: list[dict[str, Any]], record: dict[str, Any]) -> dict[str, Any] | None:
    comment_id = record.get("comment_id")
    if not isinstance(comment_id, int) or comment_id <= 0:
        return None
    return next(
        (
            existing
            for existing in records
            if existing.get("comment_id") == comment_id and isinstance(existing.get("task_id"), str)
        ),
        None,
    )


def _write_monitor_state(
    *,
    path: Path,
    owner: str,
    repo: str,
    pr_number: int,
    review_id: int,
    records: list[dict[str, Any]],
) -> None:
    state: dict[str, Any] = {
        "owner": owner,
        "repo": repo,
        "pr_number": pr_number,
        "review_id": review_id,
        "records": records,
    }
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _monitor_tasks(
    *,
    owner: str,
    repo: str,
    pr_number: int,
    review_id: int,
    review_url: str,
    records: list[dict[str, Any]],
    state_path: Path,
    poll_interval_seconds: float,
    provider: Any,
    completion_records: list[dict[str, Any]] | None = None,
) -> None:
    active_records = completion_records if completion_records is not None else records
    while True:
        if poll_interval_seconds > 0:
            time.sleep(poll_interval_seconds)
        for record in active_records:
            if record.get("retry_status") == "requested":
                retry_snapshot = _task_snapshot(owner=owner, repo=repo, task_id=record["task_id"])
                if not _advance_task_retry(record, retry_snapshot):
                    continue
            if record["status"] not in _TERMINAL_TASK_STATES:
                snapshot = _task_snapshot(owner=owner, repo=repo, task_id=record["task_id"])
                record["status"] = _task_status_from_snapshot(snapshot)
                if record["status"] == "unknown":
                    raise RuntimeError(f"Agent Tasks API returned no status for {record['task_id']!r}")
            else:
                snapshot = None
            if record["status"] in _TERMINAL_TASK_STATES:
                if snapshot is None:
                    snapshot = _task_snapshot(owner=owner, repo=repo, task_id=record["task_id"])
                _finalize_task_record(
                    owner=owner,
                    repo=repo,
                    pr_number=pr_number,
                    provider=provider,
                    record=record,
                    snapshot=snapshot,
                )
        for record in records:
            try:
                _sync_task_result_reply(
                    owner=owner,
                    repo=repo,
                    pr_number=pr_number,
                    review_url=review_url,
                    record=record,
                )
            except RuntimeError as exc:
                record["tracking_comment_error"] = str(exc)
        _write_monitor_state(
            path=state_path,
            owner=owner,
            repo=repo,
            pr_number=pr_number,
            review_id=review_id,
            records=records,
        )
        if all(record["status"] in _TERMINAL_TASK_STATES for record in active_records) and all(
            record["agent_comment"] != "🔃"
            and record["agent_task_text"] != "🔃"
            and record.get("tracking_comment_id")
            and record.get("resolution_decision") != "-"
            and (
                record.get("push_verification") in {"verified", "not_required"}
                or record.get("retry_status") in {"exhausted", "unavailable"}
            )
            and (
                record["status"] != "completed"
                or record["thread_resolved"]
                or record.get("resolution_decision") == "do_not_resolve"
            )
            for record in records
        ):
            return


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-url", required=True)
    parser.add_argument("--content-file", type=Path)
    parser.add_argument("--head-sha")
    parser.add_argument("--base-ref")
    parser.add_argument("--head-ref")
    parser.add_argument("--model", default=None)
    parser.add_argument("--dispatch-task", action="store_true")
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Dispatch all recovered comments before monitoring them; sequential dispatch is the default.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reuse the existing monitor state and skip comments whose task is already complete.",
    )
    parser.add_argument("--post-task-link", action="store_true")
    parser.add_argument("--monitor", action="store_true")
    parser.add_argument("--poll-interval-seconds", type=float, default=300.0)
    parser.add_argument("--output-dir", type=Path, default=Path(".agdt-temp"))
    return parser


def main() -> int:
    github_provider = importlib.import_module("agentic_devtools.cli.ci.github_provider")
    GitHubActionsProvider = getattr(github_provider, "GitHubActionsProvider")
    _build_repair_comment = cast(Callable[..., str], getattr(github_provider, "_build_repair_comment"))
    _deduplicate_review_comments = cast(
        Callable[[list[Any], list[Any]], list[Any]], getattr(github_provider, "_deduplicate_review_comments")
    )
    _parse_suppressed_from_review_body = cast(
        Callable[..., list[Any]], getattr(github_provider, "_parse_suppressed_from_review_body")
    )

    args = _build_parser().parse_args()
    owner, repo, pr_number, review_id = _parse_review_url(args.review_url)
    if args.post_task_link and not args.dispatch_task:
        raise ValueError("--post-task-link requires --dispatch-task")
    if args.monitor and not args.post_task_link:
        raise ValueError("--monitor requires --post-task-link")
    if args.resume and not args.post_task_link:
        raise ValueError("--resume requires --post-task-link")
    if args.poll_interval_seconds < 0:
        raise ValueError("--poll-interval-seconds must be non-negative")
    review_body = _load_review_body(
        content_file=args.content_file,
        owner=owner,
        repo=repo,
        pr_number=pr_number,
        review_id=review_id,
    )
    suppressed_comments = _parse_suppressed_from_review_body(review_body, source_review_id=review_id)
    provider = GitHubActionsProvider(f"{owner}/{repo}")

    def _fresh_provider() -> Any:
        return GitHubActionsProvider(f"{owner}/{repo}")

    review_comments = provider.list_review_comments(pr_number, review_id)
    review_comments = _deduplicate_review_comments(review_comments, suppressed_comments)
    review_comments.sort(key=lambda comment: not (comment.is_suppressed and not comment.html_url))
    if not review_comments:
        raise RuntimeError("No inline or suppressed CCR findings were recovered from the review.")
    review_comments = _filter_unresolved_review_comments(
        provider=provider,
        pr_number=pr_number,
        comments=review_comments,
    )
    if not review_comments:
        return 0
    head_sha = _load_head_sha(
        owner=owner,
        repo=repo,
        pr_number=pr_number,
        supplied=args.head_sha,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    dispatch_config: tuple[str, str, str] | None = None
    if args.dispatch_task:
        base_ref = _load_pr_ref(
            owner=owner,
            repo=repo,
            pr_number=pr_number,
            jq=".base.ref",
            supplied=args.base_ref,
        )
        head_ref = _load_pr_ref(
            owner=owner,
            repo=repo,
            pr_number=pr_number,
            jq=".head.ref",
            supplied=args.head_ref,
        )
        model = (args.model or os.environ.get("COPILOT_MODEL") or "gpt-5.6-luna").strip()
        if not model:
            raise ValueError("model must be a non-empty string")
        dispatch_config = (base_ref, head_ref, model)
    task_records: list[dict[str, Any]] = []
    state_path = _state_path(args.output_dir, pr_number, review_id)
    resume_records = (
        _load_monitor_records(
            path=state_path,
            owner=owner,
            repo=repo,
            pr_number=pr_number,
            review_id=review_id,
        )
        if args.resume
        else []
    )
    prepared_comments: list[tuple[Any, dict[str, Any]]] = []
    for ordinal, comment in enumerate(review_comments, start=1):
        record = _comment_metadata(comment, args.review_url.strip())
        dispatch_comment = comment
        if record["is_suppressed"] and dispatch_config is not None:
            marker = _SUPPRESSED_THREAD_MARKER.format(review_id=review_id, ordinal=ordinal)
            comment_id, html_url = _ensure_suppressed_review_thread(
                owner=owner,
                repo=repo,
                pr_number=pr_number,
                comment=comment,
                head_sha=head_sha,
                marker=marker,
                provider=provider,
            )
            thread_states = fetch_review_thread_states(_fresh_provider(), pr_number)
            if not thread_states.degraded and thread_states.states.get(comment_id, (False, False))[0]:
                continue
            dispatch_comment = replace(comment, id=comment_id, html_url=html_url, is_suppressed=False)
            record.update(
                {
                    "comment_id": comment_id,
                    "original_comment": f"[Original comment]({html_url})",
                    "comment_type": "suppressed",
                }
            )
        prepared_comments.append((dispatch_comment, record))

    def _render_and_dispatch(ordinal: int, comment: Any, record: dict[str, Any]) -> bool:
        if dispatch_config is not None:
            thread_states = fetch_review_thread_states(_fresh_provider(), pr_number)
            if (
                not thread_states.degraded
                and isinstance(getattr(comment, "id", None), int)
                and comment.id >= 0
                and thread_states.states.get(comment.id, (False, False))[0]
            ):
                return False
        body = _build_repair_comment(
            head_sha=head_sha,
            repair_type="review",
            failed_checks=[],
            review_comments=[comment],
            repository_full_name=f"{owner}/{repo}",
            pr_number=pr_number,
            review_id=review_id,
        )
        output_path = args.output_dir / f"ai-pr-loop-dispatch-{pr_number}-{review_id}-comment-{ordinal}.md"
        output_path.write_text(body, encoding="utf-8")
        print(f"dispatch_file={output_path.as_posix()}")
        if dispatch_config is not None:
            base_ref, head_ref, model = dispatch_config
            task_id, task_url = _dispatch_agent_task(
                prompt=body,
                owner=owner,
                repo=repo,
                model=model,
                base_ref=base_ref,
                head_ref=head_ref,
            )
            print(f"task_id={task_id}")
            print(f"task_url={task_url}")
            record.update(
                {
                    "ordinal": ordinal,
                    "task_id": task_id,
                    "task_url": task_url,
                    "status": "queued",
                    "agent_comment": "🔃",
                    "agent_task_text": "🔃",
                    "session_id": "",
                    "thread_resolved": False,
                    "follow_up_issue": "-",
                    "resolution_decision": "-",
                    "resolution_text": "-",
                    "initial_head_sha": head_sha,
                    "pr_number": pr_number,
                    "head_ref": head_ref,
                }
            )
            task_records.append(record)
        return True

    def _write_initial_state() -> Path:
        state_path = _state_path(args.output_dir, pr_number, review_id)
        _write_monitor_state(
            path=state_path,
            owner=owner,
            repo=repo,
            pr_number=pr_number,
            review_id=review_id,
            records=task_records,
        )
        print(f"monitor_state={state_path.as_posix()}")
        return state_path

    if args.dispatch_task and not args.parallel:
        for ordinal, (comment, prepared_record) in enumerate(prepared_comments, start=1):
            resume_record = _find_resume_record(resume_records, prepared_record) if args.resume else None
            if resume_record is None:
                record = prepared_record
                if not _render_and_dispatch(ordinal, comment, record):
                    continue
            else:
                record = resume_record
                record["ordinal"] = ordinal
                task_records.append(record)
            if _record_is_complete(record):
                continue
            if args.post_task_link:
                try:
                    _sync_task_result_reply(
                        owner=owner,
                        repo=repo,
                        pr_number=pr_number,
                        review_url=args.review_url.strip(),
                        record=record,
                    )
                except RuntimeError as exc:
                    record["tracking_comment_error"] = str(exc)
                state_path = _write_initial_state()
                if args.monitor:
                    _monitor_tasks(
                        owner=owner,
                        repo=repo,
                        pr_number=pr_number,
                        review_id=review_id,
                        review_url=args.review_url.strip(),
                        records=task_records,
                        state_path=state_path,
                        poll_interval_seconds=args.poll_interval_seconds,
                        provider=provider,
                        completion_records=[record],
                    )
        if args.monitor and _tasks_ready_for_takeover(task_records):
            _run_takeover_after_monitor(owner=owner, repo=repo, pr_number=pr_number, provider=_fresh_provider())
    else:
        for ordinal, (comment, prepared_record) in enumerate(prepared_comments, start=1):
            resume_record = _find_resume_record(resume_records, prepared_record) if args.resume else None
            if resume_record is None:
                _render_and_dispatch(ordinal, comment, prepared_record)
            else:
                record = resume_record
                record["ordinal"] = ordinal
                task_records.append(record)
    if args.post_task_link and not (args.dispatch_task and not args.parallel):
        for record in task_records:
            try:
                _sync_task_result_reply(
                    owner=owner,
                    repo=repo,
                    pr_number=pr_number,
                    review_url=args.review_url.strip(),
                    record=record,
                )
            except RuntimeError as exc:
                record["tracking_comment_error"] = str(exc)
        state_path = _state_path(args.output_dir, pr_number, review_id)
        _write_monitor_state(
            path=state_path,
            owner=owner,
            repo=repo,
            pr_number=pr_number,
            review_id=review_id,
            records=task_records,
        )
        print(f"monitor_state={state_path.as_posix()}")
        if args.monitor:
            _monitor_tasks(
                owner=owner,
                repo=repo,
                pr_number=pr_number,
                review_id=review_id,
                review_url=args.review_url.strip(),
                records=task_records,
                state_path=state_path,
                poll_interval_seconds=args.poll_interval_seconds,
                provider=provider,
            )
            if _tasks_ready_for_takeover(task_records):
                _run_takeover_after_monitor(owner=owner, repo=repo, pr_number=pr_number, provider=_fresh_provider())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
