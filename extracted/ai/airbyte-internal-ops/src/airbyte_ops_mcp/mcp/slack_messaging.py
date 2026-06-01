# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for Slack messaging operations.

This module exposes the newsletter posting tool for AI agents.

**Newsletter posting** — Converts Slack mrkdwn text into Block Kit blocks
and dispatches them via a GitHub Actions workflow to a newsletter channel.

## MCP reference

.. include:: ../../../docs/mcp-generated/slack_messaging.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

import json
import logging
from enum import Enum
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
from airbyte_ops_mcp.slack_ops.blocks import (
    build_blocks,
    validate_message,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Newsletter constants
# ---------------------------------------------------------------------------

# Newsletter name → (channel_id, human-readable channel name)
_NEWSLETTER_CHANNELS: dict[str, tuple[str, str]] = {
    "Hydra": ("C0AH48172M6", "#daily-newsletters"),
}

# Workflow dispatch constants
_REPO_OWNER = "airbytehq"
_REPO_NAME = "airbyte-ops-mcp"
_WORKFLOW_FILE = "slack-post-message.yml"
_DEFAULT_BRANCH = "main"

# Test channel for dry-run posts (#slackbot-testing-channel--ignore-plz)
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


# ---------------------------------------------------------------------------
# Newsletter tool
# ---------------------------------------------------------------------------


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
        Literal["Hydra"],
        "Name of the newsletter to post to. "
        "Determines which Slack channel receives the message. "
        "Currently only 'Hydra' is supported (posts to #daily-newsletters). "
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


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def register_slack_messaging_tools(app: FastMCP) -> None:
    """Register all Slack messaging tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
