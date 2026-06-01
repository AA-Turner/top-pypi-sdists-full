# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tool for human-in-the-loop escalation.

This module exposes the HITL escalation operation as an MCP tool for AI agents.
It is a thin wrapper around the core dispatch function in human_in_the_loop module.

## MCP reference

.. include:: ../../../docs/mcp-generated/human_in_the_loop.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

from enum import StrEnum
from typing import Annotated

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.human_in_the_loop import dispatch_escalation


class RequestType(StrEnum):
    """Type of escalation request, controlling the Slack header emoji and label."""

    ACTION = "action"
    REVIEW = "review"
    INPUT = "input"
    GUIDANCE = "guidance"
    APPROVAL = "approval"
    BLOCKED = "blocked"


# Maps request_type values to (header_emoji, header_label) tuples.
_REQUEST_TYPE_HEADERS: dict[RequestType, tuple[str, str]] = {
    RequestType.ACTION: ("🔧", "Action Requested"),
    RequestType.REVIEW: ("👀", "Review Requested"),
    RequestType.INPUT: ("❓", "Input Needed"),
    RequestType.GUIDANCE: ("🧭", "Guidance Needed"),
    RequestType.APPROVAL: ("✅", "Approval Requested"),
    RequestType.BLOCKED: ("🚫", "Still Blocked"),
}


class EscalateToHumanResponse(BaseModel):
    """Response from the human-in-the-loop escalation tool."""

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


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def escalate_to_human(
    target_person: Annotated[
        str,
        "Primary person to notify. Accepts an email address (e.g. 'aj@airbyte.io'), "
        "a GitHub handle prefixed with @ (e.g. '@aaronsteers'), "
        "or a Slack user ID (e.g. 'U05AKF1BCC9').",
    ],
    message: Annotated[
        str,
        "The message body to deliver to the human. Format using Slack mrkdwn: "
        "*bold*, _italic_, `code`, ```code blocks```, > blockquotes, "
        "- bullet lists, and <url|label> links. Should clearly explain "
        "what you need help with or what decision is required.",
    ],
    agent_session_url: Annotated[
        str,
        "Your agent session URL so the human can view the full context. "
        "Use the session URL from your system prompt.",
    ],
    cc: Annotated[
        list[str] | None,
        "Optional list of additional people to tag on the message. "
        "Each entry uses the same identifier format as target_person.",
    ] = None,
    pr_url: Annotated[
        str | None,
        "Optional URL to a related pull request for the 'View PR' button.",
    ] = None,
    issue_url: Annotated[
        str | None,
        "Optional URL to a related GitHub issue for the 'View Issue' button.",
    ] = None,
    additional_actions: Annotated[
        dict[str, str] | None,
        "Optional dictionary of label -> URL pairs for extra action buttons. "
        "Example: {'Start Workflow': 'https://github.com/...actions/...'}.",
    ] = None,
    approval_requested: Annotated[
        bool,
        "Set to True to add 'Approve' and 'Reject' buttons that post back to the Slack app. "
        "Each button includes a confirmation dialog (if approval_request_summary is provided). "
        "When either button is clicked, both buttons morph into non-interactive status text "
        "(e.g. ':white_check_mark: Approved by @user' or ':x: Rejected by @user').",
    ] = False,
    approval_request_summary: Annotated[
        str | None,
        "Short description of what the user is approving, shown in a Slack "
        "confirmation dialog before the Approve button fires. Rendered as a "
        "blockquote. MUST be at most 280 characters; over-limit or "
        "unbalanced-backtick inputs are rejected at call time. Keep it to the "
        "minimum info the approver needs to identify what they are approving. "
        "Example: 'Pinning source-hubspot prerelease 4.5.3-preview to workspace for testing'.",
    ] = None,
    approval_request_detail_url: Annotated[
        str | None,
        "Optional URL where the reviewer can read full details of what they are "
        "being asked to approve. Rendered as a 'View Details' button in the Slack message.",
    ] = None,
    connector_name: Annotated[
        str | None,
        "Optional connector name to display prominently in the Slack message. "
        "For example, when combined with request_type='action', the header may be "
        "rendered as '🔧 Action Requested — source-salesloft'. If request_type is omitted, "
        "the header remains the generic '🙋 Human-in-the-loop request' and the connector "
        "name is still included for additional context. Always provide this when the "
        "escalation is about a specific connector.",
    ] = None,
    request_type: Annotated[
        RequestType | None,
        "Type of escalation request. Controls the Slack message header emoji and label. "
        "Accepted values: 'action' (🔧 Action Requested), "
        "'review' (👀 Review Requested), 'input' (❓ Input Needed), "
        "'guidance' (🧭 Guidance Needed), 'approval' (✅ Approval Requested), "
        "'blocked' (🚫 Still Blocked). "
        "When omitted, defaults to the generic 'Human-in-the-loop request' header.",
    ] = None,
) -> EscalateToHumanResponse:
    """Escalate to a human team member via Slack.

    Posts a formatted message to the #human-in-the-loop Slack channel,
    tagging the specified person(s). The message includes clickable buttons
    for the Devin session, PR, and issue links when provided, plus any
    additional freeform action buttons.

    The Slack message is sent by a GitHub Actions workflow so that Slack
    credentials are never exposed to the calling agent. The workflow
    resolves person identifiers (email, GitHub handle, or Slack ID) to
    Slack user IDs using the internal team roster.

    Use this tool when you need human input, approval, or help that you
    cannot resolve on your own.
    """
    # Resolve request_type to header_emoji and header_label
    header_emoji: str | None = None
    header_label: str | None = None
    if request_type is not None:
        header_emoji, header_label = _REQUEST_TYPE_HEADERS[request_type]

    result = dispatch_escalation(
        target_person=target_person,
        message=message,
        agent_session_url=agent_session_url,
        cc=cc,
        pr_url=pr_url,
        issue_url=issue_url,
        additional_actions=additional_actions,
        approval_requested=approval_requested,
        approval_request_summary=approval_request_summary,
        approval_request_detail_url=approval_request_detail_url,
        connector_name=connector_name,
        header_emoji=header_emoji,
        header_label=header_label,
    )

    view_url = result.run_url or result.workflow_url
    return EscalateToHumanResponse(
        success=True,
        message=(
            f"Escalation sent to '{target_person}' via #human-in-the-loop. "
            f"View progress at: {view_url}"
        ),
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


def register_human_in_the_loop_tools(app: FastMCP) -> None:
    """Register human-in-the-loop tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
