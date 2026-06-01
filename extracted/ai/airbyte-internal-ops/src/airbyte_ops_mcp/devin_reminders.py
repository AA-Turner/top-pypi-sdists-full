# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Devin reminders: workflow dispatch for scheduling and cancelling agent reminders.

This module provides the core logic for the `set_devin_reminder` and
`cancel_devin_reminder` MCP tools. It dispatches the `devin-reminders.yml`
workflow with `action=put` or `action=cancel`, which manages reminders
stored as GitHub Actions artifacts and posts notifications to
`#devin-reminders` in Slack.

The reminder fires on the next cron cycle (every 30 minutes) after the
scheduled time, injecting a message back into the originating Devin session
via the `devin-reminders-action`.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone

from airbyte_cdk.utils.datetime_helpers import ab_datetime_parse
from zoneinfo import ZoneInfo

from airbyte_ops_mcp.github_actions import (
    WorkflowDispatchResult,
    resolve_default_workflow_branch,
    trigger_workflow_dispatch,
)
from airbyte_ops_mcp.github_api import resolve_ci_trigger_github_token

logger = logging.getLogger(__name__)

REMINDERS_REPO_OWNER = "airbytehq"
REMINDERS_REPO_NAME = "airbyte-ops-mcp"
REMINDERS_WORKFLOW_FILE = "devin-reminders.yml"
REMINDERS_DEFAULT_BRANCH = "main"


MAX_DELAY_MINUTES = 7 * 24 * 60
CRON_INTERVAL_MINUTES = 30
PACIFIC_TZ = ZoneInfo("America/Los_Angeles")


def validate_delay_minutes(delay_minutes: int) -> None:
    """Validate that delay_minutes is a supported 30-minute interval.

    Args:
        delay_minutes: Number of minutes until the reminder fires.

    Raises:
        ValueError: If delay_minutes is not a positive multiple of 30,
            or exceeds the 7-day maximum.
    """
    if delay_minutes <= 0:
        raise ValueError(f"delay_minutes must be positive, got {delay_minutes}")
    if delay_minutes % CRON_INTERVAL_MINUTES != 0:
        raise ValueError(
            f"delay_minutes must be a multiple of {CRON_INTERVAL_MINUTES}, "
            f"got {delay_minutes}"
        )
    if delay_minutes > MAX_DELAY_MINUTES:
        raise ValueError(
            f"delay_minutes must be at most {MAX_DELAY_MINUTES} (7 days), "
            f"got {delay_minutes}"
        )


def compute_remind_at(
    delay_minutes: int | None = None,
    remind_at_local_time: str | None = None,
) -> str:
    """Resolve reminder timing into an ISO 8601 UTC timestamp.

    Exactly one of `delay_minutes` or `remind_at_local_time` must be provided.

    When `delay_minutes` is given, the timestamp is computed as now + delay.
    When `remind_at_local_time` is given, the string is parsed with
    `ab_datetime_parse` from the Airbyte CDK and reinterpreted as Pacific
    time (`America/Los_Angeles`).

    Args:
        delay_minutes: Minutes from now until the reminder fires. Must be a
            positive multiple of 30, up to 10080 (7 days).
        remind_at_local_time: Date-time string in Pacific time
            (`America/Los_Angeles`), e.g. `2026-04-02 09:00` or
            `2026-04-02 9:00 AM`. Must be in the future and within 7 days.
            Inputs with explicit timezone offsets (e.g. `Z`, `+05:00`,
            `+0530`) are rejected to avoid misinterpreting non-Pacific
            times.

    Returns:
        ISO 8601 timestamp string with UTC timezone offset
        (e.g. `2026-02-20T17:00:00+00:00`).

    Raises:
        ValueError: If neither or both params are given, if the input
            contains an explicit timezone/offset, or if the resolved time
            is invalid (negative, not a multiple of 30, in the past,
            or beyond the 7-day maximum).
    """
    if delay_minutes is not None and remind_at_local_time is not None:
        raise ValueError(
            "Provide exactly one of delay_minutes or remind_at_local_time, not both."
        )
    if delay_minutes is None and remind_at_local_time is None:
        raise ValueError(
            "Provide exactly one of delay_minutes or remind_at_local_time."
        )

    now_utc = datetime.now(tz=timezone.utc)

    if delay_minutes is not None:
        validate_delay_minutes(delay_minutes)
        return (now_utc + timedelta(minutes=delay_minutes)).isoformat()

    assert remind_at_local_time is not None  # for type narrowing
    stripped = remind_at_local_time.strip()

    parsed = ab_datetime_parse(stripped)

    # ab_datetime_parse sets tzinfo to datetime.timezone.utc for naive inputs.
    # Any other tzinfo type (tzlocal for Z, tzoffset for +HH:MM, etc.) means
    # the input contained an explicit timezone — reject it to avoid silently
    # reinterpreting non-Pacific times via the .replace() below.
    if type(parsed.tzinfo) is not timezone:
        raise ValueError(
            "remind_at_local_time must not include a timezone or offset; "
            "provide a local Pacific time like '2026-04-02 09:00'."
        )

    # Reinterpret as Pacific local time.
    pacific_dt = parsed.replace(tzinfo=PACIFIC_TZ)
    utc_dt = pacific_dt.astimezone(timezone.utc)

    if utc_dt <= now_utc:
        raise ValueError(
            f"remind_at_local_time must be in the future. "
            f"Parsed {remind_at_local_time!r} as {utc_dt.isoformat()} UTC, "
            f"which is not after now ({now_utc.isoformat()} UTC)."
        )

    delta_minutes = (utc_dt - now_utc).total_seconds() / 60
    if delta_minutes > MAX_DELAY_MINUTES:
        raise ValueError(
            f"remind_at_local_time must be at most {MAX_DELAY_MINUTES} minutes "
            f"({MAX_DELAY_MINUTES // (24 * 60)} days) in the future. "
            f"'{remind_at_local_time}' is ~{int(delta_minutes)} minutes away."
        )

    return utc_dt.isoformat()


def dispatch_reminder(
    reminder_message: str,
    agent_session_url: str,
    delay_minutes: int | None = None,
    remind_at_local_time: str | None = None,
    slack_users_cc: str | None = None,
) -> WorkflowDispatchResult:
    """Dispatch a Devin reminder via the devin-reminders-command workflow.

    Triggers the `devin-reminders.yml` workflow with `action=put`.
    The workflow stores the reminder as a GitHub Actions artifact and posts
    a confirmation to `#devin-reminders`.

    Exactly one of `delay_minutes` or `remind_at_local_time` must be provided.

    Args:
        reminder_message: The reminder message to deliver.
        agent_session_url: Devin session URL to inject the reminder into.
        delay_minutes: Minutes until the reminder fires. Must be a positive
            multiple of 30, up to 10080 (7 days). Mutually exclusive with
            `remind_at_local_time`.
        remind_at_local_time: A date-time string in Pacific time
            (`America/Los_Angeles`), e.g. `2026-04-02 09:00` or
            `2026-04-02 9:00 AM`. Mutually exclusive with
            `delay_minutes`.
        slack_users_cc: Optional comma-delimited Slack user tags to CC.

    Returns:
        WorkflowDispatchResult with workflow URL and optionally run ID/URL.

    Raises:
        ValueError: If neither or both time params are given, values are
            invalid, or no GitHub token is found.
        requests.HTTPError: If the workflow dispatch API call fails.
    """
    remind_at = compute_remind_at(
        delay_minutes=delay_minutes,
        remind_at_local_time=remind_at_local_time,
    )
    token = resolve_ci_trigger_github_token()

    workflow_inputs: dict[str, str] = {
        "action": "put",
        "reminder_message": reminder_message,
        "remind_at": remind_at,
        "agent_session_url": agent_session_url,
    }

    if slack_users_cc:
        workflow_inputs["slack_users_cc"] = slack_users_cc

    return trigger_workflow_dispatch(
        owner=REMINDERS_REPO_OWNER,
        repo=REMINDERS_REPO_NAME,
        workflow_file=REMINDERS_WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(REMINDERS_DEFAULT_BRANCH),
        inputs=workflow_inputs,
        token=token,
    )


def dispatch_cancel_reminder(
    agent_session_url: str,
    cancel_guids: list[str],
) -> WorkflowDispatchResult:
    """Cancel pending Devin reminders via the devin-reminders workflow.

    Triggers the `devin-reminders.yml` workflow with `action=cancel`.
    The workflow removes matching reminders from the GitHub Actions artifact
    and posts a confirmation to `#devin-reminders`.

    Both `agent_session_url` and `cancel_guids` are required. The action
    filters by both the session URL and the provided GUIDs.

    Args:
        agent_session_url: Devin session URL that owns the reminders.
        cancel_guids: List of specific reminder GUIDs to cancel.

    Returns:
        WorkflowDispatchResult with workflow URL and optionally run ID/URL.

    Raises:
        ValueError: If agent_session_url or cancel_guids is empty,
            or if no GitHub token is found.
        requests.HTTPError: If the workflow dispatch API call fails.
    """
    if not agent_session_url:
        raise ValueError("agent_session_url is required for cancel.")
    if not cancel_guids:
        raise ValueError("cancel_guids is required for cancel.")

    token = resolve_ci_trigger_github_token()

    workflow_inputs: dict[str, str] = {
        "action": "cancel",
        "agent_session_url": agent_session_url,
        "cancel_guids": json.dumps(cancel_guids),
    }

    return trigger_workflow_dispatch(
        owner=REMINDERS_REPO_OWNER,
        repo=REMINDERS_REPO_NAME,
        workflow_file=REMINDERS_WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(REMINDERS_DEFAULT_BRANCH),
        inputs=workflow_inputs,
        token=token,
    )
