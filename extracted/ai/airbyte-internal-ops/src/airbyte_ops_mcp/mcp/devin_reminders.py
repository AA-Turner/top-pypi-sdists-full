# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for scheduling and cancelling Devin agent reminders.

This module exposes reminder scheduling and cancellation as MCP tools for AI agents.
It is a thin wrapper around the core dispatch functions in the devin_reminders module.

## MCP reference

.. include:: ../../../docs/mcp-generated/devin_reminders.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

from typing import Annotated

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.devin_reminders import dispatch_cancel_reminder, dispatch_reminder


class SetDevinReminderResponse(BaseModel):
    """Response from the set_devin_reminder tool."""

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
def set_devin_reminder(
    reminder_message: Annotated[
        str,
        "The reminder message to deliver. Should clearly describe what "
        "you need to be reminded about.",
    ],
    agent_session_url: Annotated[
        str,
        "Your Devin session URL so the reminder can be injected back into "
        "your session. Use the session URL from your system prompt.",
    ],
    delay_minutes: Annotated[
        int | None,
        "Number of minutes until the reminder fires. Must be a positive "
        "multiple of 30, up to 10080 (7 days). Examples: 30, 60, 120, 1440. "
        "Mutually exclusive with remind_at_local_time.",
    ] = None,
    remind_at_local_time: Annotated[
        str | None,
        "Date-time in local time when the reminder should fire. "
        "At Airbyte, local time is always Pacific (America/Los_Angeles). "
        "Accepts '2026-04-02 09:00' (24-hour), "
        "'2026-04-02 9:00 AM' (12-hour), or ISO-like 'YYYY-MM-DDTHH:MM'. "
        "Must be in the future and within 7 days. "
        "Mutually exclusive with delay_minutes. "
        "PREFERRED — use this instead of delay_minutes to avoid "
        "timezone-conversion errors.",
    ] = None,
    slack_users_cc: Annotated[
        str | None,
        "Optional comma-delimited list of Slack user tags to CC on the "
        "reminder notification. Example: '<@U12345>, <@U67890>'.",
    ] = None,
) -> SetDevinReminderResponse:
    """Schedule a reminder that fires at a specified time or after a delay.

    Creates a reminder that will be delivered back to your Devin session
    and posted to the #devin-reminders Slack channel when the time arrives.
    Reminders are checked every 30 minutes via a cron schedule.

    Exactly one of `delay_minutes` or `remind_at_local_time` must be provided.
    Prefer `remind_at_local_time` (Pacific local time) over `delay_minutes`
    to avoid timezone-conversion mistakes — unless the user explicitly
    asks for a reminder in N minutes.

    The reminder is stored as a GitHub Actions artifact and processed by
    the devin-reminders-action. When the reminder is due, it injects a
    message into the originating Devin session and sends a Slack notification.

    Use this tool when you need to schedule a follow-up action, check on
    a long-running process, or remind yourself about a task.
    """
    try:
        result = dispatch_reminder(
            delay_minutes=delay_minutes,
            remind_at_local_time=remind_at_local_time,
            reminder_message=reminder_message,
            agent_session_url=agent_session_url,
            slack_users_cc=slack_users_cc,
        )
    except ValueError as e:
        return SetDevinReminderResponse(
            success=False,
            message=f"Invalid input: {e}",
        )

    if remind_at_local_time:
        time_desc = f"at {remind_at_local_time} Pacific"
    else:
        time_desc = f"in {delay_minutes} minutes"

    view_url = result.run_url or result.workflow_url
    return SetDevinReminderResponse(
        success=True,
        message=(
            f"Reminder scheduled to fire {time_desc}. "
            f"View progress at: {view_url}\n\n"
            f"To cancel pending reminders for this session, use the "
            f"`cancel_devin_reminder` tool."
        ),
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


class CancelDevinReminderResponse(BaseModel):
    """Response from the cancel_devin_reminder tool."""

    success: bool = Field(
        description="Whether the cancel workflow was triggered successfully"
    )
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
def cancel_devin_reminder(
    agent_session_url: Annotated[
        str,
        "Your Devin session URL. Use the session URL from your system prompt. "
        "Required together with cancel_guids.",
    ],
    cancel_guids: Annotated[
        list[str],
        "List of reminder GUIDs to cancel. You can get GUIDs from "
        "the reminder creation response or from the reminders list.",
    ],
) -> CancelDevinReminderResponse:
    """Cancel pending Devin reminders by session URL and specific GUIDs.

    Removes matching reminders so they will not fire. Use this when instructed
    to stop reminders, or when a reminder is no longer needed.

    Both agent_session_url and cancel_guids are required. Only reminders
    matching the session URL AND present in the GUID list are cancelled.
    """
    try:
        result = dispatch_cancel_reminder(
            agent_session_url=agent_session_url,
            cancel_guids=cancel_guids,
        )
    except ValueError as e:
        return CancelDevinReminderResponse(
            success=False,
            message=f"Invalid input: {e}",
        )

    view_url = result.run_url or result.workflow_url
    guid_list = ", ".join(cancel_guids)
    return CancelDevinReminderResponse(
        success=True,
        message=(
            f"Cancel workflow triggered for GUIDs [{guid_list}] "
            f"in session {agent_session_url}. View progress at: {view_url}"
        ),
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


def register_devin_reminder_tools(app: FastMCP) -> None:
    """Register Devin reminder tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
