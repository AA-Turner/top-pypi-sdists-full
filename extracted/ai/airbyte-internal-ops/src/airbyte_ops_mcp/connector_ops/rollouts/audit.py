# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Slack audit output for AutoPilot rollout actions."""

from __future__ import annotations

import logging
import os

from airbyte_ops_mcp.connector_ops.rollouts.ci import build_ci_run_url
from airbyte_ops_mcp.connector_ops.rollouts.models import (
    AutopilotAction,
    AutopilotResult,
)
from airbyte_ops_mcp.slack_posting import (
    post_channel_message,
    post_thread_reply,
    resolve_slack_bot_token,
)

logger = logging.getLogger(__name__)

_AUDIT_CHANNEL_ENV = "SLACK_CHANNEL_ROLLOUT_AUDIT"
_AUDIT_CHANNEL_DEFAULT_ID = "C0BRZHL7P41"  # #connector-rollout-updates


def _audit_entries(result: AutopilotResult) -> list[tuple[str, AutopilotAction]]:
    """Return entries that are useful in the rollout audit."""
    return [
        *[("Action", entry) for entry in result.actions],
        *[("Error", entry) for entry in result.errors],
        *[("Warning", entry) for entry in result.warnings],
        *[("Hold", entry) for entry in result.holds],
    ]


def _render_detail_lines(result: AutopilotResult) -> str:
    """Render audit-worthy result entries for a Slack thread."""
    markers = {
        "Action": "✅",
        "Error": "❌",
        "Warning": "⚠️",
        "Hold": "⏸️",
    }
    lines = []
    for category, entry in _audit_entries(result):
        tier = entry.tier or "unknown"
        message = entry.message.replace("\n", " ")
        lines.append(
            f"{markers[category]} *{category}:* `{entry.connector_name}` "
            f"`{entry.rc_version}` ({tier}) — {message}"
        )
    return "\n".join(lines)


def _render_parent_message(result: AutopilotResult) -> str:
    """Render the parent message for an AutoPilot phase."""
    run_url = build_ci_run_url()
    return (
        f"*Rollout AutoPilot: `{result.command}`*\n"
        f"{result.summary}\n"
        f"<{run_url}|View GitHub Actions run>"
    )


def post_autopilot_audit(result: AutopilotResult) -> None:
    """Post audit-worthy AutoPilot output to Slack without affecting the CLI.

    The audit posts to `#connector-rollout-updates` by default; configure
    `SLACK_CHANNEL_ROLLOUT_AUDIT` to override the target channel. A pass must
    take at least one action to be posted; its errors, warnings, and holds are
    included as context, while `skipped` entries are omitted. Dry runs are
    intentionally omitted.
    """
    channel = (
        os.environ.get(_AUDIT_CHANNEL_ENV, "").strip() or _AUDIT_CHANNEL_DEFAULT_ID
    )
    if result.dry_run or not result.actions:
        return

    token = resolve_slack_bot_token()
    if not token:
        return

    try:
        parent = post_channel_message(
            channel,
            _render_parent_message(result),
            token=token,
        )
        details = _render_detail_lines(result)
        if details:
            post_thread_reply(channel, parent.ts, details, token=token)
    except Exception as exc:
        logger.warning(
            "Failed to post AutoPilot audit for %s: %s",
            result.command,
            exc,
        )
