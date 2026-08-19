# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""CI-side CLI entrypoint for the Slack HITL notification workflow.

This module runs inside GitHub Actions to resolve person identifiers to
Slack user IDs (using the roster artifact), preserve Slack usergroup IDs,
and post a formatted Block Kit message to a Slack channel.

It is invoked by the `human-in-the-loop.yml` workflow. The core logic lives
in `slack_posting.send_hitl_notification()`; this module only adds CLI
argument parsing, roster file loading, and GitHub Actions output emission.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from airbyte_ops_mcp.slack_posting import SlackPostResult, send_hitl_notification


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


def _write_github_outputs(result: SlackPostResult) -> None:
    """Emit GitHub Actions outputs for downstream steps."""
    github_output = os.environ.get("GITHUB_OUTPUT")
    if not github_output:
        return

    with open(github_output, "a") as f:
        f.write(f"message_channel={result.channel_id}\n")
        f.write(f"message_ts={result.ts}\n")
        f.write(f"thread_url={result.permalink}\n")

    print(
        f"GitHub Actions outputs set: message_channel={result.channel_id}, "
        f"message_ts={result.ts}",
        file=sys.stderr,
    )


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
        help="Primary identifier (email, GitHub handle, Slack ID, usergroup handle, or pasted Slack mention).",
    )
    parser.add_argument("--message", required=True, help="Message body.")
    parser.add_argument("--agent-session-url", required=True, help="Agent session URL.")
    parser.add_argument(
        "--cc-persons",
        default="",
        help="Comma-separated person or usergroup handles, IDs, or pasted Slack mentions.",
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
        default="\U0001f64b",
        help="Emoji for the message header. Defaults to '\U0001f64b'.",
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
        help="Optional connector name to include in the header.",
    )

    args = parser.parse_args()

    # -- CLI-specific guard: agent-session-url is required for this path --
    if not args.agent_session_url:
        print(
            "Error: --agent-session-url is required for CI HITL notifications.",
            file=sys.stderr,
        )
        sys.exit(1)

    # -- Load roster from file (CI-specific; the Python API uses fetch_roster) --
    roster = _load_roster(args.roster_file)
    print(f"Loaded roster with {len(roster)} members.", file=sys.stderr)

    # -- Parse composite CLI args --
    cc_persons: list[str] | None = None
    if args.cc_persons:
        cc_persons = [p.strip() for p in args.cc_persons.split(",") if p.strip()]

    extra_actions: dict[str, str] | None = None
    if args.additional_actions:
        extra_actions = json.loads(args.additional_actions)

    approval_meta: dict[str, str] | None = None
    if args.approval_metadata:
        approval_meta = json.loads(args.approval_metadata)

    # -- Delegate to the shared function --
    result = send_hitl_notification(
        target_person=args.target_person,
        message=args.message,
        agent_session_url=args.agent_session_url,
        connector_name=args.connector_name,
        header_emoji=args.header_emoji,
        header_label=args.header_label,
        cc_persons=cc_persons,
        pr_url=args.pr_url,
        issue_url=args.issue_url,
        additional_actions=extra_actions,
        approval_requested=args.approval_requested,
        approval_request_summary=args.approval_request_summary,
        approval_request_detail_url=args.approval_request_detail_url,
        approval_metadata=approval_meta,
        channel_override=args.channel_override,
        context_footer=args.context_footer,
        roster=roster,
    )

    print(
        f"Message posted to #{result.channel_id} successfully (ts={result.ts}).",
        file=sys.stderr,
    )

    # -- Emit GitHub Actions outputs --
    _write_github_outputs(result)


if __name__ == "__main__":
    main()
