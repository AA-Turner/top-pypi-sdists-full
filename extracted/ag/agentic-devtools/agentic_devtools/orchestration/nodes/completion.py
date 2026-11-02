"""Completion node: post summary comment and finalize workflow.

Builds a completion comment with work summary, PR link, completed
checklist items, and token usage. Posts to the appropriate platform
using structured formatting from ``_comment_formatting``.
"""

from __future__ import annotations

import logging
from typing import Any

from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe
from agentic_devtools.orchestration.nodes._comment_formatting import format_completion_comment
from agentic_devtools.orchestration.nodes._helpers import (
    _to_nonneg_int,
    build_idempotency_registry,
    detect_issue_provider,
    get_run_id,
    normalize_github_issue_number,
    utc_now,
)
from agentic_devtools.orchestration.state_schema import WorkOnIssueState

logger = logging.getLogger(__name__)


def completion_node(state: WorkOnIssueState) -> dict[str, Any]:
    """Post completion comment and mark workflow as done.

    Builds a summary with PR link, checklist results, and token usage.
    Posts to Jira or GitHub depending on the issue provider.

    Fails fast when ``issue_key`` is missing, blank, or not a string so a
    corrupted/resumed checkpoint cannot raise ``AttributeError`` inside
    ``detect_issue_provider()`` or ``normalize_issue_key()``.
    """
    issue_key = state.get("issue_key", "")
    if not isinstance(issue_key, str) or not issue_key.strip():
        return {
            "step": "completion",
            "status": "failed",
            "error": "issue_key is required and must be a non-empty string",
            "completion_comment_posted": False,
            "events": [
                {
                    "event": "completion_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": "missing_issue_key"},
                }
            ],
        }
    issue_key = issue_key.strip()
    raw_issue_provider = state.get("issue_provider")
    issue_provider = (
        raw_issue_provider
        if isinstance(raw_issue_provider, str) and raw_issue_provider in {"jira", "github"}
        else detect_issue_provider(issue_key)
    )
    pr_url = state.get("pr_url", "")
    checklist_items = state.get("checklist_items", [])
    token_usage_prompt = state.get("token_usage_prompt", 0)
    token_usage_completion = state.get("token_usage_completion", 0)
    dry_run = state.get("dry_run") is True

    # Build completion data for formatter
    completion_data = _build_completion_data(
        state,
        pr_url=pr_url if isinstance(pr_url, str) else "",
        checklist_items=checklist_items if isinstance(checklist_items, list) else [],
        token_usage_prompt=_to_nonneg_int(token_usage_prompt),
        token_usage_completion=_to_nonneg_int(token_usage_completion),
    )

    # Format comment using structured formatter
    comment = format_completion_comment(completion_data, issue_provider)

    # Post comment (or skip in dry-run mode)
    completion_comment_posted = False
    dry_run_skipped = False

    if dry_run:
        dry_run_skipped = True
        logger.info("Dry-run: would post completion comment to %s issue %s:\n%s", issue_provider, issue_key, comment)
    else:
        # Post comment to appropriate platform (best-effort)
        run_id = get_run_id()
        if issue_provider == "jira":
            completion_comment_posted = _post_jira_comment(issue_key, comment, run_id=run_id)
        else:
            completion_comment_posted = _post_github_comment(issue_key, comment, run_id=run_id)

    return {
        "step": "completion",
        "status": "completed",
        "completion_comment_posted": completion_comment_posted,
        "dry_run_skipped": dry_run_skipped,
        "events": [
            {
                "event": "completion_completed",
                "timestamp": utc_now(),
                "signals": {"pr_url": pr_url, "completion_comment_posted": completion_comment_posted},
            }
        ],
    }


def _post_jira_comment(issue_key: str, comment: str, *, run_id: str | None = None) -> bool:
    """Post completion comment to Jira.

    Protects against duplicate posts on LangGraph checkpoint replay via the
    ``IdempotencyRegistry`` when ``run_id`` is available.

    Returns True on success or idempotency-cache hit, False on failure.
    """
    tool_name = "jira_add_comment"
    tool_args = {"issue_key": issue_key, "comment": comment}
    registry = build_idempotency_registry(run_id)
    if registry is not None:
        existing = registry.check(tool_name, tool_args, "completion")
        if existing is not None and existing.status == "success":
            logger.info("Idempotency hit: Jira completion comment for %s already posted", issue_key)
            return True
    try:
        from agentic_devtools.orchestration.nodes._issue_retrieval import _build_jira_config
        from agentic_devtools.tools.jira import add_comment

        config = _build_jira_config()
        add_comment(config=config, issue_key=issue_key, comment=comment)
        if registry is not None:
            registry.record(tool_name, tool_args, "completion", result_summary="success")
        return True
    except Exception as exc:
        logger.warning("Failed to post Jira completion comment: %s", exc)
        return False


def _post_github_comment(issue_key: str, comment: str, *, run_id: str | None = None) -> bool:
    """Post completion comment to GitHub.

    Protects against duplicate posts on LangGraph checkpoint replay via the
    ``IdempotencyRegistry`` when ``run_id`` is available.

    Returns True on success or idempotency-cache hit, False on failure.
    """
    tool_name = "github_add_comment"
    tool_args = {"issue_number": issue_key, "comment": comment}
    registry = build_idempotency_registry(run_id)
    if registry is not None:
        existing = registry.check(tool_name, tool_args, "completion")
        if existing is not None and existing.status == "success":
            logger.info("Idempotency hit: GitHub completion comment for %s already posted", issue_key)
            return True
    try:
        repo = resolve_github_repo_safe()
        if not repo:
            logger.warning("Cannot resolve GitHub repo for completion comment")
            return False

        normalized_issue_key = normalize_github_issue_number(issue_key)
        if not normalized_issue_key:
            logger.warning("GitHub issue key is invalid; expected positive integer")
            return False

        from agentic_devtools.adapters.github_adapter import GitHubIssuesAdapter

        adapter = GitHubIssuesAdapter(repo=repo)
        adapter.add_comment(normalized_issue_key, comment)
        if registry is not None:
            registry.record(tool_name, tool_args, "completion", result_summary="success")
        return True
    except Exception as exc:
        logger.warning("Failed to post GitHub completion comment: %s", exc)
        return False


def _build_completion_data(
    state: WorkOnIssueState,
    *,
    pr_url: str,
    checklist_items: list[dict[str, Any]],
    token_usage_prompt: int,
    token_usage_completion: int,
) -> dict[str, Any]:
    """Build formatter input from the workflow's actual state producers."""
    raw_what_was_done = state.get("what_was_done")
    if isinstance(raw_what_was_done, str) and raw_what_was_done.strip():
        what_was_done = raw_what_was_done
    else:
        what_was_done = _derive_work_summary(state, checklist_items)

    raw_quality_gates = state.get("quality_gates")
    quality_gates = (
        raw_quality_gates
        if isinstance(raw_quality_gates, list) and all(isinstance(item, dict) for item in raw_quality_gates)
        else _derive_quality_gates(state)
    )

    return {
        "what_was_done": what_was_done,
        "pr_url": pr_url,
        "quality_gates": quality_gates,
        "checklist_items": checklist_items,
        "token_usage_prompt": token_usage_prompt,
        "token_usage_completion": token_usage_completion,
    }


def _derive_work_summary(state: WorkOnIssueState, checklist_items: list[dict[str, Any]]) -> str:
    """Summarize completed work from checklist items and affected paths."""
    lines: list[str] = []

    completed_descriptions = [
        description.strip()
        for item in checklist_items
        if isinstance(item, dict)
        and item.get("is_complete") is True
        and isinstance((description := item.get("description")), str)
        and description.strip()
    ]
    if completed_descriptions:
        lines.append("Completed checklist items:")
        lines.extend(f"- {description}" for description in completed_descriptions)

    raw_paths = state.get("affected_paths", [])
    if isinstance(raw_paths, list):
        unique_paths: list[str] = []
        for raw_path in raw_paths:
            normalized = raw_path.strip() if isinstance(raw_path, str) else ""
            if normalized and normalized not in unique_paths:
                unique_paths.append(normalized)
        if unique_paths:
            if lines:
                lines.append("")
            lines.append("Affected files:")
            lines.extend(f"- {path}" for path in unique_paths)

    if lines:
        return "\n".join(lines)

    raw_log = state.get("implementation_log", [])
    if isinstance(raw_log, list):
        completed_count = sum(1 for entry in raw_log if isinstance(entry, dict) and entry.get("status") == "completed")
        if completed_count:
            return f"Completed {completed_count} implementation step(s)."
    return ""


def _derive_quality_gates(state: WorkOnIssueState) -> list[dict[str, str]]:
    """Derive a compact quality-gate summary from verification output."""
    raw_output = state.get("verification_output")
    has_output = isinstance(raw_output, str) and bool(raw_output.strip())

    # Check if any verification event was recorded so we can emit a gate entry
    # even when verification produced no textual output.
    raw_events = state.get("events")
    has_verification_event = isinstance(raw_events, list) and any(
        isinstance(e, dict) and e.get("event") in ("verification_passed", "verification_failed") for e in raw_events
    )

    if not has_output and not has_verification_event:
        return []

    status = _derive_quality_gate_status(state)

    details = ""
    if has_output:
        raw_str: str = raw_output  # type: ignore[assignment]
        details = " ".join(part.strip() for part in raw_str.splitlines() if part.strip())
        if len(details) > 200:
            details = f"{details[:197]}..."
    return [{"name": "Targeted checks", "status": status, "details": details}]


def _derive_quality_gate_status(state: WorkOnIssueState) -> str:
    """Derive gate status from recorded verification events."""
    raw_events = state.get("events")
    if not isinstance(raw_events, list):
        return "fail"

    for event in reversed(raw_events):
        if not isinstance(event, dict):
            continue
        event_name = event.get("event")
        if event_name == "verification_failed":
            return "fail"
        if event_name == "verification_passed":
            return "pass"
    return "fail"
