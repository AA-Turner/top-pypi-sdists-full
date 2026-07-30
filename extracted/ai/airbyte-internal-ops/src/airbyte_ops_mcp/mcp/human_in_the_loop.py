# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for human-in-the-loop workflows: escalation to a human, team-roster lookup, and Slack newsletter posting.

## MCP reference

.. include:: ../../../docs/mcp-generated/human_in_the_loop.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

import json
import logging
from enum import Enum, StrEnum
from typing import Annotated, Literal

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.github_actions import (
    WorkflowDispatchResult,
    WorkflowRunStatus,
    resolve_default_workflow_branch,
    trigger_workflow_dispatch,
    wait_for_workflow_completion,
)
from airbyte_ops_mcp.github_api import resolve_ci_trigger_github_token
from airbyte_ops_mcp.human_in_the_loop import (
    HITL_SLACK_CHANNEL_URL,
    dispatch_escalation,
)
from airbyte_ops_mcp.internal_team_roster import fetch_roster, search_roster
from airbyte_ops_mcp.slack_api import lookup_slack_usergroup as find_slack_usergroups
from airbyte_ops_mcp.slack_ops.blocks import (
    build_blocks,
    validate_message,
)


class PersonRecord(BaseModel):
    """A person in the internal team roster."""

    slack_id: str | None = Field(default=None, description="Slack user ID")
    slack_display_name: str | None = Field(
        default=None, description="Slack display name"
    )
    slack_email: str | None = Field(
        default=None, description="Email address from Slack profile"
    )
    github_id: int | None = Field(default=None, description="GitHub numeric user ID")
    github_handle: str | None = Field(default=None, description="GitHub username")
    github_public_email: str | None = Field(
        default=None, description="Public email from GitHub profile"
    )


class PeopleLookupResponse(BaseModel):
    """Response from a people lookup query."""

    query: str = Field(description="The search query that was used")
    total_matches: int = Field(description="Number of matching records")
    matches: list[PersonRecord] = Field(description="Matching person records")


class RosterListResponse(BaseModel):
    """Response listing the full internal team roster."""

    total_members: int = Field(description="Total number of members in the roster")
    members: list[PersonRecord] = Field(description="All person records in the roster")


class SlackUsergroupRecord(BaseModel):
    """A Slack usergroup and its mention metadata."""

    id: str = Field(description="Slack usergroup ID used in <!subteam^ID|@handle>")
    handle: str = Field(description="Slack usergroup handle without the leading @")
    name: str = Field(description="Slack usergroup display name")
    description: str = Field(description="Slack usergroup description")
    user_count: int = Field(description="Number of members in the usergroup")


class SlackUsergroupLookupResponse(BaseModel):
    """Response from a Slack usergroup lookup."""

    id_or_handle: str = Field(description="The usergroup ID or handle/name lookup")
    total_matches: int = Field(description="Number of matching usergroups")
    matches: list[SlackUsergroupRecord] = Field(description="Matching Slack usergroups")


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def lookup_person(
    query: Annotated[
        str,
        Field(
            description=(
                "Search query to match against any field: email address, "
                "Slack display name, Slack user ID, GitHub handle, or GitHub user ID. "
                "Case-insensitive partial matching for strings, exact match for numeric IDs."
            )
        ),
    ],
) -> PeopleLookupResponse:
    """Look up a person in the Airbyte internal team roster.

    Searches the daily-generated roster artifact by any field value.
    The roster is built from Slack and GitHub org membership data,
    cross-referenced by email address.

    Use this to find someone's Slack ID for messaging, GitHub handle
    for code review, or to cross-reference identities across platforms.
    """
    roster = fetch_roster()
    matches = search_roster(roster, query)
    return PeopleLookupResponse(
        query=query,
        total_matches=len(matches),
        matches=[PersonRecord.model_validate(person) for person in matches],
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def list_team_roster() -> RosterListResponse:
    """List the full Airbyte internal team roster.

    Returns all members from the daily-generated roster artifact.
    The roster is sorted by Slack display name for easy scanning.
    Use lookup_person for targeted searches instead of scanning the full list.
    """
    roster = fetch_roster()
    return RosterListResponse(
        total_members=len(roster),
        members=[PersonRecord.model_validate(person) for person in roster],
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def lookup_slack_usergroup(
    id_or_handle: Annotated[
        str,
        Field(
            description=(
                "Required Slack usergroup handle/name or S-prefixed usergroup ID. "
                "Handle/name matching is "
                "case-insensitive and partial; a leading @ is ignored. "
                "S-prefixed IDs are matched exactly."
            )
        ),
    ],
) -> SlackUsergroupLookupResponse:
    """Resolve Slack usergroups to IDs for usergroup mentions.

    Pass a handle or name to resolve oncall aliases such as `@oc-apis`, or
    pass an S-prefixed usergroup ID for the corresponding handle and name.
    Results include the ID and metadata needed for the
    `<!subteam^ID|@alias>` mention syntax used by Slack messages.
    """
    usergroups = find_slack_usergroups(id_or_handle)
    return SlackUsergroupLookupResponse(
        id_or_handle=id_or_handle,
        total_matches=len(usergroups),
        matches=[
            SlackUsergroupRecord(
                id=usergroup.id,
                handle=usergroup.handle,
                name=usergroup.name,
                description=usergroup.description,
                user_count=usergroup.user_count,
            )
            for usergroup in usergroups
        ],
    )


class RequestType(StrEnum):
    """Type of escalation request, controlling the Slack header emoji and label."""

    ACTION = "action"
    REVIEW = "review"
    INPUT = "input"
    GUIDANCE = "guidance"
    APPROVAL = "approval"
    BLOCKED = "blocked"


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
    slack_channel_url: str = Field(
        default=HITL_SLACK_CHANNEL_URL,
        description="Direct URL to the #human-in-the-loop Slack channel",
    )
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
        "a Slack user ID (e.g. 'U05AKF1BCC9'), or a Slack usergroup ID "
        "(e.g. 'S0BKR63VAN5' for @oc-internal-ai). Slack usergroup handles "
        "such as '@oc-internal-ai' are not resolvable; use the ID form.",
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
        "Optional list of additional people or Slack usergroups to tag on the "
        "message. Each entry uses the same identifier format as target_person. "
        "For usergroups, use the S-prefixed ID (e.g. 'S0BKR63VAN5' for "
        "@oc-internal-ai), not the handle.",
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
    """Escalate to a human or Slack usergroup via Slack.

    Posts a formatted message to the #human-in-the-loop Slack channel,
    tagging the specified person(s) or usergroup(s). The message includes
    clickable buttons for the Devin session, PR, and issue links when provided,
    plus any additional freeform action buttons.

    The Slack message is sent by a GitHub Actions workflow so that Slack
    credentials are never exposed to the calling agent. The workflow
    resolves person identifiers (email, GitHub handle, or Slack ID) to Slack
    user IDs using the internal team roster. S-prefixed Slack usergroup IDs
    bypass roster resolution and render as usergroup mentions.

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
            f"Escalation sent to '{target_person}' via #human-in-the-loop "
            f"({HITL_SLACK_CHANNEL_URL}). "
            f"View progress at: {view_url}"
        ),
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


logger = logging.getLogger(__name__)

_NEWSLETTER_CHANNELS: dict[str, tuple[str, str]] = {
    "DR": ("C0AH48172M6", "#daily-newsletters"),
    "Internal AI": ("C0AH48172M6", "#daily-newsletters"),
    "AJ": ("C0BLUPJ0X0R", "#aj-release-notes"),
}

_REPO_OWNER = "airbytehq"

_REPO_NAME = "airbyte-ops-mcp"

_WORKFLOW_FILE = "slack-post-message.yml"

_DEFAULT_BRANCH = "main"

_DRY_RUN_CHANNEL = "C0AEN317Z7T"


class DryRunMode(str, Enum):
    """Controls how dry-run behaves."""

    off = "off"
    """Normal mode — post to the real channel."""

    local = "local"
    """Local-only preview. Builds Block Kit JSON and returns both the
    blocks JSON (for agent-side rendering) and a Block Kit Builder URL.
    No workflow is triggered."""

    slack_test_channel = "slack_test_channel"
    """Triggers the real workflow but posts to a test channel instead of
    the production newsletter channel."""


class PostToSlackChannelResponse(BaseModel):
    """Response from the post_slack_newsletter tool."""

    success: bool = Field(description="Whether the operation completed successfully")
    message: str = Field(description="Human-readable status message")
    blocks_json: str | None = Field(
        default=None,
        description=(
            "Serialised JSON array of Block Kit blocks. "
            "Populated in 'local' dry-run mode so the agent can "
            "render or inspect the blocks directly."
        ),
    )
    workflow_url: str | None = Field(
        default=None,
        description="URL to view the GitHub Actions workflow file",
    )
    run_id: int | None = Field(
        default=None,
        description="GitHub Actions workflow run ID",
    )
    channel_name: str | None = Field(
        default=None,
        description="Human-readable Slack channel name (e.g. '#daily-newsletters')",
    )
    run_url: str | None = Field(
        default=None,
        description="Direct URL to the GitHub Actions workflow run",
    )


def _format_failure_details(run_status: WorkflowRunStatus) -> str:
    """Build a human-readable summary of failed jobs from a workflow run."""
    if not run_status.jobs:
        return ""
    failed_jobs = [j for j in run_status.jobs if j.conclusion == "failure"]
    if not failed_jobs:
        return ""
    job_summaries = [f"  - {j.name} (job_id={j.job_id})" for j in failed_jobs]
    return " Failed jobs:\n" + "\n".join(job_summaries)


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def post_slack_newsletter(
    message_text: Annotated[
        str,
        "The formatted message to post, using Slack mrkdwn syntax: "
        "*bold*, _italic_, `code`, ```code blocks```, > blockquotes, "
        "- bullet lists, and <url|label> links. "
        "Use ## for section headers (translated to Block Kit header blocks) "
        "and ### for sub-headers (translated to bold text). "
        "Double newlines (\\n\\n) split the text into separate visual "
        "sections in the Slack message. "
        "Do NOT include markdown tables — they will be rejected.",
    ],
    newsletter_name: Annotated[
        Literal["DR", "Internal AI", "AJ"],
        "Name of the newsletter to post to. "
        "Determines which Slack channel receives the message. "
        "DR and Internal AI both post to #daily-newsletters; AJ posts to "
        "#aj-release-notes. "
        "Ignored when dry_run is 'slack_test_channel'.",
    ],
    dry_run: Annotated[
        str,
        "Controls dry-run behaviour. "
        "'off' (default): post to the real channel. "
        "'local': build blocks locally and return blocks JSON plus a "
        "Block Kit Builder URL — no workflow is triggered. "
        "'slack_test_channel': trigger the workflow but post to a test "
        "channel instead of the production newsletter channel.",
    ] = "off",
) -> PostToSlackChannelResponse:
    """Post a formatted newsletter digest to a Slack channel.

    Converts Slack mrkdwn text into Block Kit blocks locally (with
    validation), then dispatches them to a GitHub Actions workflow for
    posting.  The workflow receives finished Block Kit JSON — it does
    not perform any markdown conversion.

    Dry-run modes:
    - `local`: returns blocks JSON for local rendering — no workflow triggered
    - `slack_test_channel`: posts to a test channel for formatting verification
    """
    try:
        mode = DryRunMode(dry_run)
    except ValueError:
        allowed_values = ", ".join(m.value for m in DryRunMode)
        return PostToSlackChannelResponse(
            success=False,
            message=(
                f"Invalid dry_run value {dry_run!r}. "
                f"Allowed values are: {allowed_values}."
            ),
        )

    # --- Validate input ---
    try:
        validate_message(message_text)
    except ValueError as exc:
        return PostToSlackChannelResponse(
            success=False,
            message=str(exc),
        )

    # --- Build Block Kit blocks locally ---
    blocks_dict = build_blocks(message_text)
    blocks_json = json.dumps(blocks_dict)

    # --- Local mode: return blocks JSON, no dispatch ---
    if mode is DryRunMode.local:
        return PostToSlackChannelResponse(
            success=True,
            message=(
                "Local preview generated. Use the blocks_json field to "
                "render the message locally."
            ),
            blocks_json=blocks_json,
        )

    # --- Resolve target channel ---
    if mode is DryRunMode.slack_test_channel:
        resolved_channel = _DRY_RUN_CHANNEL
        resolved_channel_name = "#slackbot-testing-channel--ignore-plz"
    else:
        resolved_channel, resolved_channel_name = _NEWSLETTER_CHANNELS[newsletter_name]

    resolved_fallback = message_text[:120].replace("\n", " ")

    # --- Dispatch to GitHub Actions ---
    token = resolve_ci_trigger_github_token()
    result: WorkflowDispatchResult = trigger_workflow_dispatch(
        owner=_REPO_OWNER,
        repo=_REPO_NAME,
        workflow_file=_WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(_DEFAULT_BRANCH),
        inputs={
            "channel_id": resolved_channel,
            "blocks_json": blocks_json,
            "fallback_text": resolved_fallback,
        },
        token=token,
    )

    view_url = result.run_url or result.workflow_url
    mode_label = (
        " (dry run — test channel)" if mode is DryRunMode.slack_test_channel else ""
    )

    # --- Guard: if we couldn't discover the run, return early ---
    if result.run_id is None:
        return PostToSlackChannelResponse(
            success=False,
            message=(
                f"Workflow dispatched to {resolved_channel_name}{mode_label} "
                f"but could not discover the run ID to verify completion. "
                f"Check manually: {view_url}"
            ),
            channel_name=resolved_channel_name,
            workflow_url=result.workflow_url,
        )

    # --- Wait for workflow completion and report failures ---
    run_status: WorkflowRunStatus = wait_for_workflow_completion(
        owner=_REPO_OWNER,
        repo=_REPO_NAME,
        run_id=result.run_id,
        token=token,
        poll_interval_seconds=5.0,
        max_wait_seconds=120.0,
    )

    if run_status.failed:
        failure_details = _format_failure_details(run_status)
        return PostToSlackChannelResponse(
            success=False,
            message=(
                f"Workflow run FAILED (conclusion={run_status.conclusion}) "
                f"for {resolved_channel_name}{mode_label}. "
                f"Run: {run_status.run_url or view_url}"
                f"{failure_details}"
            ),
            channel_name=resolved_channel_name,
            workflow_url=result.workflow_url,
            run_id=result.run_id,
            run_url=run_status.run_url or result.run_url,
        )

    if not run_status.succeeded:
        return PostToSlackChannelResponse(
            success=False,
            message=(
                f"Workflow run did not complete within 120s "
                f"(status={run_status.status}, "
                f"conclusion={run_status.conclusion}){mode_label}. "
                f"Run: {run_status.run_url or view_url}"
            ),
            channel_name=resolved_channel_name,
            workflow_url=result.workflow_url,
            run_id=result.run_id,
            run_url=run_status.run_url or result.run_url,
        )

    return PostToSlackChannelResponse(
        success=True,
        message=(
            f"Message posted to {resolved_channel_name} "
            f"({resolved_channel}){mode_label}. "
            f"Run: {view_url}"
        ),
        channel_name=resolved_channel_name,
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


def register_human_in_the_loop_tools(app: FastMCP) -> None:
    """Register human-in-the-loop tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
