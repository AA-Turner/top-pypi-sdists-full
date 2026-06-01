# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""CI-side script for the Slack notification dispatch workflow.

This module runs inside GitHub Actions to resolve person identifiers to
Slack user IDs (using the roster artifact) and post a formatted Block Kit
message to a Slack channel.

It is invoked by the `human-in-the-loop.yml` workflow and should NOT be
imported at MCP runtime. The Slack token (`SLACK_BOT_TOKEN_HITL`) is only
available in CI.

The module supports customizable message headers, emojis, and channels so
that multiple MCP tools (e.g. escalate_to_human, devin_session_feedback)
can share the same workflow with different presentation.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse

import requests

_SLACK_ID_PATTERN = re.compile(r"^U[A-Z0-9]{8,}$")


def _load_roster(roster_file: str) -> list[dict[str, str | int | None]]:
    """Load the roster JSON file.

    Handles both the raw list format and the `{"members": [...]}` wrapper.
    """
    with open(roster_file) as f:
        data = json.load(f)

    if isinstance(data, dict) and "members" in data:
        return data["members"]
    if isinstance(data, list):
        return data
    return []


def _resolve_to_slack_id(
    identifier: str,
    roster: list[dict[str, str | int | None]],
) -> str | None:
    """Resolve a person identifier to a Slack user ID using the roster.

    Tries matching against email, GitHub handle, and Slack ID fields.

    Returns:
        Slack user ID string if found, None otherwise.
    """
    identifier = identifier.strip()
    if identifier.startswith("@"):
        identifier = identifier[1:]
        if not identifier:
            return None

    if _SLACK_ID_PATTERN.match(identifier):
        return identifier

    identifier_lower = identifier.lower()

    for person in roster:
        slack_email = person.get("slack_email")
        if (
            slack_email
            and isinstance(slack_email, str)
            and slack_email.lower() == identifier_lower
        ):
            slack_id = person.get("slack_id")
            if slack_id and isinstance(slack_id, str):
                return slack_id

        github_handle = person.get("github_handle")
        if (
            github_handle
            and isinstance(github_handle, str)
            and github_handle.lower() == identifier_lower
        ):
            slack_id = person.get("slack_id")
            if slack_id and isinstance(slack_id, str):
                return slack_id

        github_email = person.get("github_public_email")
        if (
            github_email
            and isinstance(github_email, str)
            and github_email.lower() == identifier_lower
        ):
            slack_id = person.get("slack_id")
            if slack_id and isinstance(slack_id, str):
                return slack_id

    return None


def _format_mention(identifier: str, slack_id: str | None) -> str:
    """Format a person as a Slack mention or fallback plain text."""
    if slack_id:
        return f"<@{slack_id}>"
    return f"`{identifier}` (could not resolve to Slack)"


def _extract_short_session_token(agent_session_url: str, length: int = 8) -> str | None:
    """Extract a short token from the session ID in the URL.

    For `https://app.devin.ai/sessions/7b60ceb6abab46c19cbe689ebdfed874`
    returns `7b60ceb6` (first *length* hex characters).

    Returns None if no session ID segment is found.
    """
    path = urlparse(agent_session_url).path.rstrip("/")
    segment = path.rsplit("/", 1)[-1] if "/" in path else ""
    if segment and len(segment) >= length and re.fullmatch(r"[0-9a-fA-F-]+", segment):
        return segment[:length]
    return None


def _extract_number_from_url(url: str) -> str | None:
    """Extract the trailing numeric identifier from a GitHub PR or issue URL.

    For `https://github.com/owner/repo/pull/365` returns `365`.
    For `https://github.com/owner/repo/issues/11103` returns `11103`.
    """
    match = re.search(r"/(pull|issues)/([0-9]+)(?:/|$)", url)
    if match:
        return match.group(2)
    return None


def _derive_agent_name(agent_session_url: str) -> str:
    """Derive an agent display name from the session URL.

    For `https://app.devin.ai/sessions/...` returns `Devin.ai`.
    Falls back to the full hostname if the domain has fewer than two parts.
    """
    hostname = urlparse(agent_session_url).hostname or ""
    parts = hostname.rsplit(".", 2)
    if len(parts) >= 2:
        base = f"{parts[-2]}.{parts[-1]}"
        return base[0].upper() + base[1:]
    return hostname.capitalize() if hostname else "Agent"


def _build_slack_blocks(
    target_person: str,
    target_slack_id: str | None,
    cc_mentions: list[str],
    message: str,
    agent_session_url: str,
    pr_url: str | None,
    issue_url: str | None,
    additional_actions: dict[str, str] | None,
    approval_requested: bool = False,
    approval_request_summary: str | None = None,
    approval_request_detail_url: str | None = None,
    approval_metadata: dict[str, str] | None = None,
    sender_name: str = "Agent (No-Reply)",
    header_emoji: str = "🙋",
    header_label: str = "Human-in-the-loop request",
    context_footer: str | None = None,
    connector_name: str | None = None,
) -> list[dict]:
    """Build Slack Block Kit blocks for the notification message."""
    blocks: list[dict] = []

    # -- Header: plain_text header block (renders large and bold in Slack) --
    # When a connector_name is provided, include it in the header for prominence.
    # Slack header blocks are plain_text only (no mrkdwn), so monospace is not
    # possible here, but the large bold rendering keeps it scannable.
    if connector_name:
        header_text = f"{header_emoji} {header_label} — {connector_name}"
    else:
        header_text = f"{header_emoji} {header_label}"
    blocks.append(
        {
            "type": "header",
            "text": {"type": "plain_text", "text": header_text, "emoji": True},
        }
    )

    # -- To / CC line --
    target_mention = _format_mention(target_person, target_slack_id)
    to_line = f"*To:* {target_mention}"
    if cc_mentions:
        to_line += f"  |  *CC:* {', '.join(cc_mentions)}"

    blocks.append(
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": to_line}],
        }
    )

    blocks.append({"type": "divider"})

    # -- Message body (mrkdwn — supports bold, italic, lists, code, links) --
    blocks.append(
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": message},
        }
    )

    blocks.append({"type": "divider"})

    # -- Action buttons --
    # Approval buttons (Approve/Reject) are built first so they appear
    # as the leftmost buttons in the actions bar.  Link buttons (View PR,
    # View Issue, etc.) follow after.
    buttons: list[dict] = []
    if approval_requested:
        button_payload: dict[str, str | dict[str, str]] = {
            "session_url": agent_session_url,
        }
        if approval_metadata:
            button_payload["approval_metadata"] = approval_metadata
        approve_value = json.dumps(button_payload)
        approve_button: dict = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Approve",
                "emoji": True,
            },
            "style": "primary",
            "value": approve_value,
            "action_id": "approve_request",
        }
        if approval_request_summary:
            approve_button["confirm"] = {
                "title": {
                    "type": "plain_text",
                    "text": "Confirm Approval",
                },
                "text": {
                    "type": "mrkdwn",
                    "text": f"> {approval_request_summary}"[:300],
                },
                "confirm": {
                    "type": "plain_text",
                    "text": "Yes, Approve",
                },
                "deny": {
                    "type": "plain_text",
                    "text": "Cancel",
                },
            }
        buttons.append(approve_button)

        reject_button: dict = {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Reject",
                "emoji": True,
            },
            "style": "danger",
            "value": approve_value,
            "action_id": "reject_request",
        }
        if approval_request_summary:
            reject_button["confirm"] = {
                "title": {
                    "type": "plain_text",
                    "text": "Confirm Rejection",
                },
                "text": {
                    "type": "mrkdwn",
                    "text": f"> {approval_request_summary}"[:300],
                },
                "confirm": {
                    "type": "plain_text",
                    "text": "Yes, Reject",
                },
                "deny": {
                    "type": "plain_text",
                    "text": "Cancel",
                },
            }
        buttons.append(reject_button)

    if approval_request_detail_url:
        buttons.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "View Details", "emoji": True},
                "url": approval_request_detail_url,
                "action_id": "view_approval_details",
            }
        )

    if pr_url:
        pr_number = _extract_number_from_url(pr_url)
        pr_label = f"View PR #{pr_number}" if pr_number else "View PR"
        buttons.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": pr_label, "emoji": True},
                "url": pr_url,
                "action_id": "view_pr",
            }
        )
    if issue_url:
        issue_number = _extract_number_from_url(issue_url)
        issue_label = f"View Issue #{issue_number}" if issue_number else "View Issue"
        buttons.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": issue_label, "emoji": True},
                "url": issue_url,
                "action_id": "view_issue",
            }
        )
    if additional_actions:
        for label, url in additional_actions.items():
            buttons.append(
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": label[:75],
                        "emoji": True,
                    },
                    "url": url,
                    "action_id": f"extra_{label[:50]}",
                }
            )

    # Always add a "View Session" button
    session_token = _extract_short_session_token(agent_session_url)
    session_label = (
        f"View Session ({session_token})" if session_token else "View Session"
    )
    buttons.append(
        {
            "type": "button",
            "text": {"type": "plain_text", "text": session_label, "emoji": True},
            "url": agent_session_url,
            "action_id": "view_session",
        }
    )

    if buttons:
        # Set primary style on first button only if no approval buttons
        # already set their own styles.
        if not approval_requested:
            buttons[0]["style"] = "primary"
        blocks.append({"type": "actions", "elements": buttons})

    # -- Footer --
    footer_parts = [
        f"Sent by *{sender_name}*. Please respond in the linked session or PR, not in this thread."
    ]
    if context_footer:
        footer_parts.append(context_footer)

    blocks.append(
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "\n".join(footer_parts),
                }
            ],
        }
    )

    return blocks


def _post_slack_message(
    token: str,
    channel: str,
    blocks: list[dict],
    fallback_text: str,
    username: str | None = None,
) -> dict[str, str]:
    """Post a message to Slack using the Web API.

    Returns:
        Dict with `channel` and `ts` from the Slack API response.
    """
    payload: dict = {
        "channel": channel,
        "blocks": blocks,
        "text": fallback_text,
        "unfurl_links": False,
        "unfurl_media": False,
    }
    if username:
        payload["username"] = username
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data.get('error', 'unknown')}")

    result_channel = data.get("channel", channel)
    result_ts = data.get("ts", "")
    print(
        f"Message posted to #{result_channel} successfully (ts={result_ts}).",
        file=sys.stderr,
    )
    return {"channel": result_channel, "ts": result_ts}


def main() -> None:
    """CLI entrypoint for the CI-side HITL script."""
    parser = argparse.ArgumentParser(
        description="Resolve person identifiers and post HITL escalation to Slack."
    )
    parser.add_argument(
        "--roster-file", required=True, help="Path to roster JSON file."
    )
    parser.add_argument(
        "--target-person",
        required=True,
        help="Primary person identifier (email, GitHub handle, or Slack ID).",
    )
    parser.add_argument("--message", required=True, help="Message body.")
    parser.add_argument("--agent-session-url", required=True, help="Agent session URL.")
    parser.add_argument(
        "--cc-persons",
        default="",
        help="Comma-separated additional person identifiers.",
    )
    parser.add_argument("--pr-url", default=None, help="Optional PR URL.")
    parser.add_argument("--issue-url", default=None, help="Optional issue URL.")
    parser.add_argument(
        "--additional-actions",
        default=None,
        help="JSON object of label -> URL pairs for extra action buttons.",
    )
    parser.add_argument(
        "--approval-requested",
        action="store_true",
        default=False,
        help="Add an Approve button that posts back to the Slack app with confirmation dialog.",
    )
    parser.add_argument(
        "--approval-request-summary",
        default=None,
        help="Short description of what the user is approving. Shown in the confirmation dialog.",
    )
    parser.add_argument(
        "--channel-override",
        default=None,
        help="Slack channel ID to post to instead of the default.",
    )
    parser.add_argument(
        "--header-emoji",
        default="🙋",
        help="Emoji for the message header. Defaults to '🙋'.",
    )
    parser.add_argument(
        "--header-label",
        default="Human-in-the-loop request",
        help="Label for the message header. Defaults to 'Human-in-the-loop request'.",
    )
    parser.add_argument(
        "--context-footer",
        default=None,
        help="Additional text appended to the context footer block.",
    )
    parser.add_argument(
        "--approval-request-detail-url",
        default=None,
        help="Optional URL where the reviewer can read full details of the approval request.",
    )
    parser.add_argument(
        "--approval-metadata",
        default=None,
        help="JSON object of key-value pairs to embed in approval buttons and echo in approval records.",
    )
    parser.add_argument(
        "--connector-name",
        default=None,
        help="Optional connector name to include in the header (e.g. '🔧 Action Requested — source-postgres').",
    )

    args = parser.parse_args()

    slack_token = os.environ.get("SLACK_BOT_TOKEN_HITL")
    if not slack_token:
        print(
            "Error: SLACK_BOT_TOKEN_HITL environment variable is required.",
            file=sys.stderr,
        )
        sys.exit(1)

    channel = args.channel_override or os.environ.get(
        "SLACK_CHANNEL_HITL", "human-in-the-loop"
    )

    roster = _load_roster(args.roster_file)
    print(f"Loaded roster with {len(roster)} members.", file=sys.stderr)

    target_slack_id = _resolve_to_slack_id(args.target_person, roster)
    if target_slack_id:
        print(
            f"Resolved target '{args.target_person}' -> Slack ID {target_slack_id}",
            file=sys.stderr,
        )
    else:
        print(
            f"Warning: Could not resolve '{args.target_person}' to a Slack ID.",
            file=sys.stderr,
        )

    cc_mentions: list[str] = []
    if args.cc_persons:
        for person in args.cc_persons.split(","):
            person = person.strip()
            if not person:
                continue
            cc_slack_id = _resolve_to_slack_id(person, roster)
            cc_mentions.append(_format_mention(person, cc_slack_id))

    extra_actions: dict[str, str] | None = None
    if args.additional_actions:
        extra_actions = json.loads(args.additional_actions)

    agent_name = _derive_agent_name(args.agent_session_url)
    print(f"Derived agent name: {agent_name}", file=sys.stderr)

    sender_name = f"{agent_name} (No-Reply)"

    approval_meta: dict[str, str] | None = None
    if args.approval_metadata:
        approval_meta = json.loads(args.approval_metadata)

    blocks = _build_slack_blocks(
        target_person=args.target_person,
        target_slack_id=target_slack_id,
        cc_mentions=cc_mentions,
        message=args.message,
        agent_session_url=args.agent_session_url,
        pr_url=args.pr_url,
        issue_url=args.issue_url,
        additional_actions=extra_actions,
        approval_requested=args.approval_requested,
        approval_request_summary=args.approval_request_summary,
        approval_request_detail_url=args.approval_request_detail_url,
        approval_metadata=approval_meta,
        sender_name=sender_name,
        header_emoji=args.header_emoji,
        header_label=args.header_label,
        context_footer=args.context_footer,
        connector_name=args.connector_name,
    )

    target_mention = _format_mention(args.target_person, target_slack_id)
    fallback_text = f"{args.header_label} for {target_mention}: {args.message}"

    result = _post_slack_message(
        slack_token, channel, blocks, fallback_text, username=sender_name
    )

    # Emit GitHub Actions outputs so callers can access the posted message
    # coordinates (channel + ts) for thread replies.
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"message_channel={result['channel']}\n")
            f.write(f"message_ts={result['ts']}\n")
            # Build a Slack permalink for convenience
            ts_digits = result["ts"].replace(".", "")
            thread_url = (
                f"https://airbytehq-team.slack.com/archives/"
                f"{result['channel']}/p{ts_digits}"
            )
            f.write(f"thread_url={thread_url}\n")
        print(
            f"GitHub Actions outputs set: message_channel={result['channel']}, "
            f"message_ts={result['ts']}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
