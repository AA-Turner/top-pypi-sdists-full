"""Planning node: generate implementation plan via LLM.

Calls the configured LLM provider to analyze the issue and generate
a structured implementation plan. Includes blocked detection for
ambiguous or under-specified issues.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from agentic_devtools.orchestration.execution.context_factory import _run_async
from agentic_devtools.orchestration.nodes._comment_formatting import format_planning_comment
from agentic_devtools.orchestration.nodes._helpers import (
    _to_nonneg_int,
    build_idempotency_registry,
    detect_issue_provider,
    utc_now,
)
from agentic_devtools.orchestration.state_schema import WorkOnIssueState

_MIN_SUMMARY_LENGTH = 5
_MIN_DESCRIPTION_LENGTH = 20
logger = logging.getLogger(__name__)


def planning_node(state: WorkOnIssueState) -> dict[str, Any]:
    """Generate implementation plan using LLM.

    Builds a system prompt with issue context, calls the LLM for
    structured output, and evaluates whether the issue is clear enough
    to proceed. If blocked, sets ``blocked_reason`` and routes to error.
    Fails fast when ``issue_key`` is absent, blank, or not a string.
    """
    raw_issue_key = state.get("issue_key")
    if not isinstance(raw_issue_key, str) or not raw_issue_key.strip():
        return {
            "step": "planning",
            "error": "issue_key is missing or blank; cannot generate implementation plan.",
            "events": [
                {
                    "event": "planning_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": "issue_key is missing or blank"},
                }
            ],
        }
    issue_key: str = raw_issue_key.strip()
    issue_data = state.get("issue_data", {})
    issue_data_dict = issue_data if isinstance(issue_data, dict) else {}

    # Build context for LLM; coerce to str so _check_blocked can safely call
    # .strip() even when issue_data carries None or an ADF dict (Jira Cloud).
    raw_summary = issue_data_dict.get("summary")
    raw_description = issue_data_dict.get("description")
    summary = raw_summary if isinstance(raw_summary, str) else ""
    description = raw_description if isinstance(raw_description, str) else ""

    # Check for obviously blocked issues (empty or trivial)
    blocked_reason = _check_blocked(summary, description)
    if blocked_reason:
        return {
            "step": "planning",
            "status": "blocked",
            "error": blocked_reason,
            "blocked_reason": blocked_reason,
            "plan_posted": False,
            "events": [
                {
                    "event": "planning_blocked",
                    "timestamp": utc_now(),
                    "signals": {"blocked_reason": blocked_reason},
                }
            ],
        }

    # Call LLM for plan generation
    try:
        plan_result = _generate_plan(issue_key, issue_data_dict)
    except Exception as exc:
        return {
            "step": "planning",
            "error": f"Plan generation failed: {exc}",
            "events": [
                {
                    "event": "planning_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": str(exc)},
                }
            ],
        }

    # Check if LLM detected blocked state
    if plan_result.get("is_blocked") is True:
        raw_blocked = plan_result.get("blocked_reason", "")
        blocked_reason = (
            raw_blocked
            if isinstance(raw_blocked, str) and raw_blocked.strip()
            else "Issue is too ambiguous for autonomous implementation"
        )
        return {
            "step": "planning",
            "status": "blocked",
            "error": blocked_reason,
            "blocked_reason": blocked_reason,
            "plan_posted": False,
            "events": [
                {
                    "event": "planning_blocked",
                    "timestamp": utc_now(),
                    "signals": {"blocked_reason": blocked_reason},
                }
            ],
        }

    raw_plan = plan_result.get("plan", "")
    plan_text = raw_plan if isinstance(raw_plan, str) else ""
    raw_token_usage = plan_result.get("token_usage", {})
    token_usage = raw_token_usage if isinstance(raw_token_usage, dict) else {}
    issue_provider = _resolve_issue_provider(state, issue_key)
    tasks, affected_files, risks = _extract_planning_sections(plan_result)

    # Post planning comment to issue tracker (best-effort).
    # plan_posted reports actual comment delivery per spec: False in dry-run
    # (see dry_run_skipped) and False on best-effort failure. Workflow routing
    # is driven by ``error`` (see route_after_plan), so a failed or skipped
    # post never halts the workflow.
    dry_run = state.get("dry_run") is True
    planning_comment_posted = False
    dry_run_skipped = False

    if dry_run:
        dry_run_skipped = True
        comment = format_planning_comment(
            plan_text,
            issue_provider,
            utc_now(),
            tasks=tasks,
            affected_files=affected_files,
            risks=risks,
        )
        logger.info("Dry-run: would post planning comment to %s issue %s:\n%s", issue_provider, issue_key, comment)
    else:
        planning_comment_posted = _post_planning_comment(
            issue_key,
            plan_text,
            state,
            tasks=tasks,
            affected_files=affected_files,
            risks=risks,
        )

    return {
        "step": "planning",
        "status": "active",
        "error": None,
        "blocked_reason": None,
        "plan": plan_text,
        "plan_posted": planning_comment_posted,
        "dry_run_skipped": dry_run_skipped,
        "token_usage_prompt": _to_nonneg_int(state.get("token_usage_prompt"))
        + _to_nonneg_int(token_usage.get("prompt_tokens")),
        "token_usage_completion": _to_nonneg_int(state.get("token_usage_completion"))
        + _to_nonneg_int(token_usage.get("completion_tokens")),
        "events": [
            {
                "event": "planning_completed",
                "timestamp": utc_now(),
                "signals": {"planning_comment_posted": planning_comment_posted},
            }
        ],
    }


def _post_planning_comment(
    issue_key: str,
    plan_text: str,
    state: WorkOnIssueState,
    *,
    tasks: list[str] | None = None,
    affected_files: list[str] | None = None,
    risks: list[str] | None = None,
) -> bool:
    """Post formatted planning comment to the issue tracker (best-effort).

    Protects against duplicate posts on LangGraph checkpoint replay by
    recording each successful invocation in the ``IdempotencyRegistry`` keyed
    by (tool_id, args_hash, node_name, run_id).  When ``run_id`` is
    unavailable (e.g. outside a LangGraph context) the call proceeds without
    idempotency protection.

    Returns True on success or idempotency-cache hit, False on failure (logs a
    warning).
    """
    from agentic_devtools.orchestration.nodes._helpers import (
        detect_issue_provider,
        get_run_id,
        normalize_github_issue_number,
    )

    raw_issue_provider = state.get("issue_provider")
    issue_provider = (
        raw_issue_provider
        if isinstance(raw_issue_provider, str) and raw_issue_provider in {"jira", "github"}
        else detect_issue_provider(issue_key)
    )

    timestamp = utc_now()
    comment = format_planning_comment(
        plan_text,
        issue_provider,
        timestamp,
        tasks=tasks,
        affected_files=affected_files,
        risks=risks,
    )

    tool_name = "jira_add_comment" if issue_provider == "jira" else "github_add_comment"
    normalized_issue_number: str | None = None
    if issue_provider == "github":
        normalized_issue_number = normalize_github_issue_number(issue_key)
        if not normalized_issue_number:
            logger.warning("GitHub issue key is invalid; expected positive integer")
            return False
    idempotency_args = (
        {"issue_key": issue_key} if issue_provider == "jira" else {"issue_number": normalized_issue_number}
    )

    registry = build_idempotency_registry(get_run_id())
    if registry is not None:
        existing = registry.check(tool_name, idempotency_args, "planning")
        if existing is not None and existing.status == "success":
            logger.info("Idempotency hit: planning comment for %s already posted", issue_key)
            return True

    try:
        if issue_provider == "jira":
            from agentic_devtools.orchestration.nodes._issue_retrieval import _build_jira_config
            from agentic_devtools.tools.jira import add_comment

            config = _build_jira_config()
            add_comment(config=config, issue_key=issue_key, comment=comment)
        else:
            from agentic_devtools.adapters.github_adapter import GitHubIssuesAdapter
            from agentic_devtools.cli.github.repo_resolution import resolve_github_repo_safe

            repo = resolve_github_repo_safe()
            if not repo:
                logger.warning("Cannot resolve GitHub repo for planning comment")
                return False
            assert normalized_issue_number is not None
            adapter = GitHubIssuesAdapter(repo=repo)
            adapter.add_comment(normalized_issue_number, comment)

        if registry is not None:
            registry.record(tool_name, idempotency_args, "planning", result_summary="success")
        return True
    except Exception as exc:
        logger.warning("Failed to post planning comment: %s", exc)
        return False


def _check_blocked(summary: str, description: str) -> str | None:
    """Check for obviously under-specified issues.

    Returns a blocked reason string if the issue lacks sufficient detail,
    or None if the issue appears actionable.
    """
    if not summary or len(summary.strip()) < _MIN_SUMMARY_LENGTH:
        return "Issue summary is empty or too short (less than 5 characters). Cannot generate implementation plan."

    if not description or len(description.strip()) < _MIN_DESCRIPTION_LENGTH:
        return (
            "Issue description is empty or too brief (less than 20 characters). "
            "Insufficient context for autonomous implementation."
        )

    return None


def _generate_plan(issue_key: str, issue_data: dict[str, Any]) -> dict[str, Any]:
    """Generate implementation plan via LLM provider.

    Returns dict with keys: plan, is_blocked, blocked_reason, token_usage.
    """
    from agentic_devtools.orchestration.llm.factory import ProviderFactory

    factory = ProviderFactory()
    provider = factory.get_provider("planning", "work_on_issue")

    raw_summary = issue_data.get("summary")
    raw_description = issue_data.get("description")
    summary = raw_summary if isinstance(raw_summary, str) else ""
    description = raw_description if isinstance(raw_description, str) else ""

    system_prompt = (
        "You are an implementation planning assistant. Given an issue description, "
        "generate a structured implementation plan. If the issue is too vague or "
        "contradictory to implement autonomously, respond with is_blocked=true.\n\n"
        "Respond with a JSON object containing:\n"
        '- "is_blocked": boolean (true if issue is too ambiguous)\n'
        '- "blocked_reason": string (explanation if blocked, empty otherwise)\n'
        '- "missing_information": list of strings (what info is needed if blocked)\n'
        '- "plan": string (implementation plan if not blocked)\n'
        '- "tasks": list of task descriptions\n'
        '- "affected_files": list of file paths expected to change\n'
        '- "risks": list of risks or concerns for the implementation\n'
    )

    user_prompt = f"Issue Key: {issue_key}\nSummary: {summary}\n\nDescription:\n{description}"

    async def _call_llm():
        from agentic_devtools.orchestration.llm.types import LLMMessage

        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt),
        ]
        response = await provider.complete(messages)
        return response

    response = _run_async(_call_llm())

    # Parse response
    token_usage = {}
    if response.usage:
        token_usage = {
            "prompt_tokens": response.usage.input_tokens,
            "completion_tokens": response.usage.output_tokens,
        }

    # Try to parse structured response
    try:
        parsed = json.loads(response.text)
        if isinstance(parsed, dict):
            return {
                "plan": parsed.get("plan", response.text),
                "is_blocked": parsed.get("is_blocked", False),
                "blocked_reason": parsed.get("blocked_reason", ""),
                "tasks": parsed.get("tasks", []),
                "risks": parsed.get("risks", []),
                "affected_files": parsed.get("affected_files", []),
                "token_usage": token_usage,
            }
    except (json.JSONDecodeError, TypeError):
        pass
    # If response isn't valid JSON, or parsed to a non-dict type, treat it as the plan text
    return {
        "plan": response.text,
        "is_blocked": False,
        "blocked_reason": "",
        "tasks": [],
        "risks": [],
        "affected_files": [],
        "token_usage": token_usage,
    }


def _resolve_issue_provider(state: WorkOnIssueState, issue_key: str) -> str:
    """Resolve issue provider from state or the issue key format."""
    raw_issue_provider = state.get("issue_provider")
    if isinstance(raw_issue_provider, str) and raw_issue_provider in {"jira", "github"}:
        return raw_issue_provider
    return detect_issue_provider(issue_key)


def _extract_planning_sections(plan_result: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    """Extract formatter-ready sections from the structured plan result."""
    tasks: list[str] = []
    affected_files: list[str] = []
    risks: list[str] = []

    raw_tasks = plan_result.get("tasks", [])
    if isinstance(raw_tasks, list):
        for raw_task in raw_tasks:
            if isinstance(raw_task, str):
                task = raw_task.strip()
                if task:
                    tasks.append(task)
                continue
            if not isinstance(raw_task, dict):
                continue

            description = raw_task.get("description")
            if isinstance(description, str) and description.strip():
                tasks.append(description.strip())

            raw_task_files = raw_task.get("affected_files", [])
            if isinstance(raw_task_files, list):
                for raw_file in raw_task_files:
                    normalized = raw_file.strip() if isinstance(raw_file, str) else ""
                    if normalized and normalized not in affected_files:
                        affected_files.append(normalized)

    raw_affected_files = plan_result.get("affected_files", [])
    if isinstance(raw_affected_files, list):
        for raw_file in raw_affected_files:
            normalized = raw_file.strip() if isinstance(raw_file, str) else ""
            if normalized and normalized not in affected_files:
                affected_files.append(normalized)

    raw_risks = plan_result.get("risks", [])
    if isinstance(raw_risks, list):
        for raw_risk in raw_risks:
            if isinstance(raw_risk, str):
                risk = raw_risk.strip()
                if risk:
                    risks.append(risk)
                continue
            if not isinstance(raw_risk, dict):
                continue

            description = raw_risk.get("description")
            if not isinstance(description, str) or not description.strip():
                continue
            risk = description.strip()
            mitigation = raw_risk.get("mitigation")
            if isinstance(mitigation, str) and mitigation.strip():
                risk = f"{risk} (Mitigation: {mitigation.strip()})"
            risks.append(risk)

    return tasks, affected_files, risks
