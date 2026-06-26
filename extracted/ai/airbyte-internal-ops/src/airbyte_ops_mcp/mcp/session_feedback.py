# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tool for Devin session feedback reporting.

This module exposes the session feedback operation as an MCP tool for AI agents.
It is a thin wrapper around the shared dispatch function in the human_in_the_loop
module, with hardcoded channel, emoji, and formatting for the feedback use case.

Feedback is structured with categories and fields modeled after standard issue/bug
report templates to ensure actionable, consistent reports.

## MCP reference

.. include:: ../../../docs/mcp-generated/session_feedback.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

import logging
import re
from enum import StrEnum
from typing import Annotated, Literal

import requests
from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.github_actions import (
    WorkflowDispatchResult,
    resolve_default_workflow_branch,
    trigger_workflow_dispatch,
)
from airbyte_ops_mcp.github_api import resolve_ci_trigger_github_token
from airbyte_ops_mcp.human_in_the_loop import dispatch_escalation
from airbyte_ops_mcp.slack_api import SlackAPIError, SlackURLParseError
from airbyte_ops_mcp.slack_posting import parse_slack_thread_url, post_thread_reply

logger = logging.getLogger(__name__)

# Hardcoded settings for the feedback tool — not agent-controllable.
_FEEDBACK_CHANNEL = "C0ACUHRP6B1"
_AJ_STEERS_IDENTIFIER = "U05AKF1BCC9"

# Triage workflow settings
_TRIAGE_REPO_OWNER = "airbytehq"
_TRIAGE_REPO_NAME = "airbyte-ops-mcp"
_TRIAGE_WORKFLOW_FILE = "devin-session-triage.yml"
_TRIAGE_DEFAULT_BRANCH = "main"
_AI_SKILLS_REPO_URL = "https://github.com/airbytehq/ai-skills"
_INTERNAL_SKILLS_URL = (
    "https://internal.airbyte.ai/docs/internal-docs/ai-engineering/skills"
)
_PLAYBOOK_ID_PATTERN = re.compile(r"^[a-z0-9_-]+$")
_SKILL_ID_PATTERN = re.compile(r"^[a-z0-9-]+$")

# --- Category definitions ---

_CATEGORY_DISPLAY: dict[str, str] = {
    "tool_failure": "Tool Failure",
    "missing_guidance": "Missing Guidance",
    "suspected_hallucination": "Suspected Hallucination",
    "bad_approach": "Bad Approach",
    "excessive_iteration": "Excessive Iteration",
    "poor_quality": "Poor Quality",
    "other_concern": "Other Concern",
    "great_results": "Great Results",
    "exceeded_expectations": "Exceeded Expectations",
    "fast_completion": "Fast Completion",
    "good_communication": "Good Communication",
    "other_positive_feedback": "Other Positive Feedback",
}


class FeedbackCategory(StrEnum):
    """Feedback categories for Devin session reports."""

    # Negative categories
    TOOL_FAILURE = "tool_failure"
    MISSING_GUIDANCE = "missing_guidance"
    SUSPECTED_HALLUCINATION = "suspected_hallucination"
    BAD_APPROACH = "bad_approach"
    EXCESSIVE_ITERATION = "excessive_iteration"
    POOR_QUALITY = "poor_quality"
    OTHER_CONCERN = "other_concern"

    # Positive categories
    GREAT_RESULTS = "great_results"
    EXCEEDED_EXPECTATIONS = "exceeded_expectations"
    FAST_COMPLETION = "fast_completion"
    GOOD_COMMUNICATION = "good_communication"
    OTHER_POSITIVE_FEEDBACK = "other_positive_feedback"

    def is_negative(self) -> bool:
        """Return True if this is a negative feedback category."""
        return self in _NEGATIVE_MEMBERS

    def display_name(self) -> str:
        """Return the human-readable display name for this category."""
        return _CATEGORY_DISPLAY.get(self.value, self.value)


_NEGATIVE_MEMBERS = frozenset(
    {
        FeedbackCategory.TOOL_FAILURE,
        FeedbackCategory.MISSING_GUIDANCE,
        FeedbackCategory.SUSPECTED_HALLUCINATION,
        FeedbackCategory.BAD_APPROACH,
        FeedbackCategory.EXCESSIVE_ITERATION,
        FeedbackCategory.POOR_QUALITY,
        FeedbackCategory.OTHER_CONCERN,
    }
)

_SEVERITY_DISPLAY: dict[str, str] = {
    "low": "Low",
    "medium": "Medium",
    "high": "High",
    "critical": "Critical",
}


def _feedback_emoji(feedback_type: str) -> str:
    """Return the header emoji for the given feedback type."""
    return ":tada:" if feedback_type == "positive" else ":warning:"


def _feedback_label(feedback_type: str) -> str:
    """Return the header label for the given feedback type."""
    type_display = "Positive" if feedback_type == "positive" else "Negative"
    return f"Devin Session Feedback ({type_display})"


def _format_playbook_link(playbook_id: str) -> str:
    """Return Slack mrkdwn for a playbook identifier."""
    if playbook_id == "none":
        return "none"
    return f"<{_AI_SKILLS_REPO_URL}/blob/main/devin/playbooks/{playbook_id}.md|{playbook_id}>"


def _format_skill_link(skill_id: str) -> str:
    """Return Slack mrkdwn for a skill identifier."""
    return f"<{_INTERNAL_SKILLS_URL}/#{skill_id}|{skill_id}>"


def _validate_playbook_id(playbook_id: str) -> str | None:
    """Return an error message if `playbook_id` is not a valid playbook identifier."""
    if playbook_id == "none" or _PLAYBOOK_ID_PATTERN.fullmatch(playbook_id):
        return None
    return "session_playbook must be 'none' or a lowercase playbook ID using only letters, numbers, '-' and '_'."


def _validate_skill_id(skill_id: str | None) -> str | None:
    """Return an error message if `skill_id` is not a valid skill identifier."""
    if skill_id is None or _SKILL_ID_PATTERN.fullmatch(skill_id):
        return None
    return "related_skill_name must be a lowercase skill ID using only letters, numbers, and '-'."


def _build_feedback_body(
    *,
    feedback_type: str,
    category: str,
    task_description: str,
    session_playbook: str,
    related_skill_name: str | None,
    expected_behavior: str | None,
    observed_behavior: str | None,
    what_went_well: str | None,
    severity: str | None,
    steps_to_reproduce: str | None,
) -> str:
    """Build a Slack mrkdwn message body from structured feedback fields."""
    lines: list[str] = []

    cat = FeedbackCategory(category)
    lines.append(f"*Category:* {cat.display_name()}")

    if severity:
        sev_display = _SEVERITY_DISPLAY.get(severity, severity)
        lines.append(f"*Severity:* {sev_display}")

    lines.append("")
    lines.append(f"*Task:* {task_description}")
    lines.append(f"*Session Playbook:* {_format_playbook_link(session_playbook)}")
    if related_skill_name:
        lines.append(f"*Related Skill:* {_format_skill_link(related_skill_name)}")

    if feedback_type == "negative":
        if expected_behavior:
            lines.append("")
            lines.append(f"*Expected Behavior:* {expected_behavior}")
        if observed_behavior:
            lines.append("")
            lines.append(f"*Observed Behavior:* {observed_behavior}")
        if steps_to_reproduce:
            lines.append("")
            lines.append(f"*Steps to Reproduce:* {steps_to_reproduce}")
    else:
        if what_went_well:
            lines.append("")
            lines.append(f"*What Went Well:* {what_went_well}")

    if feedback_type == "negative":
        lines.append("")
        lines.append(
            "_Auto-triage: a Devin session with v3 analyze mode will inspect this session._"
        )

    return "\n".join(lines)


def _validate_negative_fields(
    expected_behavior: str | None,
    observed_behavior: str | None,
) -> str | None:
    """Return an error message if required negative feedback fields are missing."""
    missing: list[str] = []
    if not expected_behavior:
        missing.append("expected_behavior")
    if not observed_behavior:
        missing.append("observed_behavior")
    if missing:
        return f"Negative feedback requires: {', '.join(missing)}."
    return None


def _validate_positive_fields(
    what_went_well: str | None,
) -> str | None:
    """Return an error message if required positive feedback fields are missing."""
    if not what_went_well:
        return "Positive feedback requires: what_went_well."
    return None


def _dispatch_triage_workflow(
    session_url: str,
    feedback_context: str,
    reporting_user: str,
    session_playbook: str,
    related_skill_name: str | None = None,
    cc_persons: str = "",
    header_emoji: str = "",
    header_label: str = "",
) -> WorkflowDispatchResult | None:
    """Dispatch the v3 session triage workflow.

    The triage workflow launches a Devin session with v3 analyze mode and
    posts a single Slack notification via the HITL reusable workflow.
    Formatting params (emoji, header, cc) are passed through to the HITL
    notification so the caller doesn't need to post separately.

    Returns the dispatch result, or None if dispatch fails.
    """
    token = resolve_ci_trigger_github_token()
    inputs: dict[str, str] = {
        "session_url": session_url,
        "feedback_context": feedback_context,
        "reporting_user": reporting_user,
        "session_playbook": session_playbook,
    }
    if related_skill_name:
        inputs["related_skill_name"] = related_skill_name
    if cc_persons:
        inputs["cc_persons"] = cc_persons
    if header_emoji:
        inputs["header_emoji"] = header_emoji
    if header_label:
        inputs["header_label"] = header_label
    try:
        return trigger_workflow_dispatch(
            owner=_TRIAGE_REPO_OWNER,
            repo=_TRIAGE_REPO_NAME,
            workflow_file=_TRIAGE_WORKFLOW_FILE,
            ref=resolve_default_workflow_branch(_TRIAGE_DEFAULT_BRANCH),
            inputs=inputs,
            token=token,
        )
    except requests.HTTPError:
        logger.exception("Failed to dispatch triage workflow")
        return None


class SessionFeedbackResponse(BaseModel):
    """Response from the session feedback tool."""

    success: bool = Field(description="Whether the workflow was triggered successfully")
    message: str = Field(description="Human-readable status message")
    workflow_url: str | None = Field(
        default=None,
        description="URL to view the GitHub Actions workflow file",
    )
    run_id: int | None = Field(
        default=None,
        description="GitHub Actions workflow run ID",
    )
    run_url: str | None = Field(
        default=None,
        description="Direct URL to the GitHub Actions workflow run",
    )
    triage_run_url: str | None = Field(
        default=None,
        description="URL to the auto-triage workflow run",
    )


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def devin_session_feedback(
    feedback_type: Annotated[
        Literal["positive", "negative"],
        Field(
            description=(
                "Type of feedback: 'positive' for a good experience or 'negative' for a "
                "bad experience. Use 'positive' when the user expresses satisfaction, "
                "praise, or a success story. Use 'negative' when the user reports a problem, "
                "frustration, or failure."
            ),
        ),
    ],
    category: Annotated[
        FeedbackCategory,
        Field(
            description=(
                "Feedback category. "
                "For NEGATIVE feedback, use one of: "
                "'tool_failure' (a specific tool/integration broke), "
                "'missing_guidance' (Devin lacked instructions or context), "
                "'suspected_hallucination' (Devin fabricated information or made incorrect claims), "
                "'bad_approach' (Devin took a fundamentally wrong strategy), "
                "'excessive_iteration' (too many loops/retries before success), "
                "'poor_quality' (output quality below expectations), "
                "'other_concern'. "
                "For POSITIVE feedback, use one of: "
                "'great_results' (task completed with high quality), "
                "'exceeded_expectations' (went above and beyond), "
                "'fast_completion' (completed quickly and efficiently), "
                "'good_communication' (kept user well-informed), "
                "'other_positive_feedback'."
            ),
        ),
    ],
    task_description: Annotated[
        str,
        Field(
            description=(
                "Brief description of what the user asked Devin to do. "
                "This sets the context for the feedback."
            ),
        ),
    ],
    agent_session_url: Annotated[
        str,
        Field(
            description=(
                "Your agent session URL so the team can view the full context. "
                "Use the session URL from your system prompt."
            ),
        ),
    ],
    reporting_user: Annotated[
        str,
        Field(
            description=(
                "The person providing the feedback. Accepts an email address "
                "(e.g. 'aj@airbyte.io'), a GitHub handle prefixed with @ "
                "(e.g. '@aaronsteers'), or a Slack user ID (e.g. 'U05AKF1BCC9')."
            ),
        ),
    ],
    session_playbook: Annotated[
        str,
        Field(
            description=(
                "ID of the Devin playbook associated with the session (e.g. "
                "'devin_feedback_triage'), or 'none' when no playbook is associated. "
                "Required so feedback can identify whether playbook instructions may need updates."
            ),
        ),
    ],
    related_skill_name: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional skill ID associated with the feedback (e.g. "
                "'delete-declarative-source-def') when a related skill may need updates "
                "or is suspected of having issues."
            ),
        ),
    ],
    expected_behavior: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "What should have happened. REQUIRED for negative feedback. "
                "Describe the expected outcome clearly."
            ),
        ),
    ],
    observed_behavior: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "What actually happened. REQUIRED for negative feedback. "
                "Describe the actual outcome, including any error messages or unexpected results."
            ),
        ),
    ],
    what_went_well: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "What specifically was good about the experience. REQUIRED for positive feedback. "
                "Be specific about what Devin did well."
            ),
        ),
    ],
    severity: Annotated[
        Literal["low", "medium", "high", "critical"] | None,
        Field(
            default=None,
            description=(
                "Severity of the issue. Recommended for negative feedback. "
                "'low' = minor inconvenience, 'medium' = notable impact, "
                "'high' = significant blocker, 'critical' = complete failure."
            ),
        ),
    ],
    steps_to_reproduce: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional steps to reproduce the issue. Helpful for negative feedback "
                "to enable the team to investigate."
            ),
        ),
    ],
    session_to_evaluate: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional Devin session URL to evaluate/triage. Use this when reporting "
                "feedback about a *different* session (not your own). If omitted, "
                "agent_session_url is used as the session to triage (i.e., the reporter "
                "is reporting on itself)."
            ),
        ),
    ],
) -> SessionFeedbackResponse:
    """Report structured feedback about a Devin session experience via Slack.

    Posts a formatted feedback message to the #hydra-feedback Slack channel,
    tagging the reporting user and @AJ Steers. The message includes a clickable
    button for the Devin session link. For negative feedback, a triage workflow
    is automatically dispatched to launch a Devin session with v3 analyze mode
    that can inspect the original session's full conversation history.

    IMPORTANT: This feedback will be logged publicly in Slack. Inform the user
    that their feedback is visible to the team and they may be contacted for
    additional details.

    Use this tool when a user explicitly asks to report a positive or negative
    experience with their Devin session. Before calling this tool, let the user
    know:
    - Their feedback will be posted publicly in the #hydra-feedback Slack channel
    - They may be contacted by the team for more details
    - Both the reporting user and @AJ Steers will be tagged in the message
    - For negative feedback, a triage session will be automatically launched to inspect the reported session

    The Slack message is sent by a GitHub Actions workflow so that Slack
    credentials are never exposed to the calling agent.
    """
    # Validate category matches feedback type.
    cat = FeedbackCategory(category)
    is_negative_feedback = feedback_type == "negative"
    id_validation_error = _validate_playbook_id(session_playbook) or _validate_skill_id(
        related_skill_name
    )
    if id_validation_error:
        return SessionFeedbackResponse(
            success=False,
            message=id_validation_error,
        )

    if cat.is_negative() != is_negative_feedback:
        expected_kind = "negative" if is_negative_feedback else "positive"
        valid = [
            c.value for c in FeedbackCategory if c.is_negative() == is_negative_feedback
        ]
        return SessionFeedbackResponse(
            success=False,
            message=(
                f"Invalid category '{category}' for {feedback_type} feedback. "
                f"Valid {expected_kind} categories: {', '.join(valid)}."
            ),
        )

    # Validate required fields based on feedback type.
    if feedback_type == "negative":
        validation_error = _validate_negative_fields(
            expected_behavior=expected_behavior,
            observed_behavior=observed_behavior,
        )
    else:
        validation_error = _validate_positive_fields(
            what_went_well=what_went_well,
        )

    if validation_error:
        return SessionFeedbackResponse(
            success=False,
            message=validation_error,
        )

    message_body = _build_feedback_body(
        feedback_type=feedback_type,
        category=category,
        task_description=task_description,
        session_playbook=session_playbook,
        related_skill_name=related_skill_name,
        expected_behavior=expected_behavior,
        observed_behavior=observed_behavior,
        what_went_well=what_went_well,
        severity=severity,
        steps_to_reproduce=steps_to_reproduce,
    )

    # For negative feedback, dispatch triage workflow (which also posts to Slack
    # via the HITL reusable workflow — single message with triage button).
    # For positive feedback, dispatch HITL directly (no triage needed).
    if is_negative_feedback:
        triage_session_url = session_to_evaluate or agent_session_url
        # _dispatch_triage_workflow catches exceptions internally and returns None
        triage_result = _dispatch_triage_workflow(
            session_url=triage_session_url,
            feedback_context=message_body,
            reporting_user=reporting_user,
            session_playbook=session_playbook,
            related_skill_name=related_skill_name,
            cc_persons=_AJ_STEERS_IDENTIFIER,
            header_emoji=_feedback_emoji(feedback_type),
            header_label=_feedback_label(feedback_type),
        )
        if triage_result is not None:
            view_url = triage_result.run_url or triage_result.workflow_url
            return SessionFeedbackResponse(
                success=True,
                message=(
                    "Feedback submitted. Auto-triage workflow launched. "
                    "A Slack notification will be posted to #hydra-feedback "
                    "once the triage session starts. "
                    f"View workflow progress at: {view_url}"
                ),
                workflow_url=triage_result.workflow_url,
                run_id=triage_result.run_id,
                run_url=triage_result.run_url,
                triage_run_url=view_url,
            )
        # Triage dispatch failed — fall back to direct HITL notification
        # so negative feedback is still recorded in Slack.
        logger.warning(
            "Triage workflow dispatch failed; falling back to direct HITL dispatch."
        )

    # Positive feedback (or negative feedback fallback): dispatch HITL directly
    result = dispatch_escalation(
        target_person=reporting_user,
        message=message_body,
        agent_session_url=agent_session_url,
        cc=[_AJ_STEERS_IDENTIFIER],
        channel_override=_FEEDBACK_CHANNEL,
        header_emoji=_feedback_emoji(feedback_type),
        header_label=_feedback_label(feedback_type),
    )

    view_url = result.run_url or result.workflow_url
    return SessionFeedbackResponse(
        success=True,
        message=(
            f"Feedback submitted and posted to #hydra-feedback. "
            f"The reporting user and @AJ Steers have been tagged. "
            f"View progress at: {view_url}"
        ),
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


# ---------------------------------------------------------------------------
# Non-interactive thread disclaimer
# ---------------------------------------------------------------------------

_FOLLOWUP_HEADER = "🤖 *Automated Triage Update*"
_FOLLOWUP_FOOTER_TEMPLATE = (
    "_ℹ️ This thread is not monitored by Devin. "
    "Replies here will not be seen by any agent. "
    "For follow-up, use the <{agent_session_url}|linked session> or create a new task._"
)


def _wrap_followup_message(message: str, *, agent_session_url: str) -> str:
    """Wrap a follow-up message with session link and non-interactive disclaimer."""
    footer = _FOLLOWUP_FOOTER_TEMPLATE.format(agent_session_url=agent_session_url)
    return f"{_FOLLOWUP_HEADER}\n\n{message}\n\n{footer}"


# ---------------------------------------------------------------------------
# Feedback follow-up tool
# ---------------------------------------------------------------------------


class SessionFeedbackFollowupResponse(BaseModel):
    """Response from the session feedback follow-up tool."""

    success: bool = Field(description="Whether the follow-up was posted successfully")
    message: str = Field(description="Human-readable status message")
    reply_ts: str | None = Field(
        default=None,
        description="Timestamp of the posted reply (Slack ts format)",
    )


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def devin_session_feedback_followup(
    thread_url: Annotated[
        str,
        Field(
            description=(
                "Slack thread URL from the original feedback post in #hydra-feedback. "
                "This is the thread where follow-up context will be appended. "
                "Example: https://airbytehq-team.slack.com/archives/C0ACUHRP6B1/p1773062711122019"
            ),
        ),
    ],
    message: Annotated[
        str,
        Field(
            description=(
                "Follow-up message text in Slack mrkdwn format. "
                "Typically a triage report or additional context about the "
                "feedback being investigated. "
                "Supports *bold*, _italic_, `code`, ```code blocks```, "
                "> blockquotes, and <url|label> links."
            ),
        ),
    ],
    agent_session_url: Annotated[
        str,
        Field(
            description=(
                "Your agent session URL for audit trail. "
                "Use the session URL from your system prompt."
            ),
        ),
    ],
) -> SessionFeedbackFollowupResponse:
    """Post a follow-up to an existing feedback thread in #hydra-feedback.

    This is the "second call" in the feedback workflow: after
    `devin_session_feedback` creates the initial report, this tool appends
    triage findings or additional context as a threaded reply.

    Each reply is wrapped with a disclaimer clarifying that the thread is
    non-interactive and not monitored by any agent.

    Workspace validation ensures only URLs from the expected Slack
    workspace are accepted.
    """
    try:
        channel_id, thread_ts = parse_slack_thread_url(thread_url)
    except SlackURLParseError as exc:
        return SessionFeedbackFollowupResponse(
            success=False,
            message=str(exc),
        )

    wrapped_message = _wrap_followup_message(
        message, agent_session_url=agent_session_url
    )

    try:
        result = post_thread_reply(
            channel_id=channel_id,
            thread_ts=thread_ts,
            message=wrapped_message,
        )
        reply_ts = result.ts
    except SlackAPIError as exc:
        return SessionFeedbackFollowupResponse(
            success=False,
            message=f"Slack API error: {exc}",
        )

    logger.info(
        "Feedback follow-up posted: channel=%s thread_ts=%s agent=%s",
        channel_id,
        thread_ts,
        agent_session_url,
    )
    return SessionFeedbackFollowupResponse(
        success=True,
        message=f"Follow-up posted to feedback thread in channel {channel_id}.",
        reply_ts=reply_ts,
    )


def register_session_feedback_tools(app: FastMCP) -> None:
    """Register session feedback tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
