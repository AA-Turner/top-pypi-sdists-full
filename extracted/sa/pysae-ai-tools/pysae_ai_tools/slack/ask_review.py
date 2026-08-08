"""Find an existing review request message in a Slack channel.

Usage:
    pysae-ai-tools slack ask-review \
        --channel C0123ABCDEF \
        --project-url https://gitlab.com/pysae/api \
        --mr-iid 42

Calls the Slack conversations.history API directly (requires SLACK_BOT_TOKEN).
Searches the last 30 days for the message our tooling posted for this MR,
identified by the structured ``ai_tools_review_request`` metadata (project +
mr_iid) stamped at post time — so a human's message merely quoting the same MR
link is never mistaken for the review request. Falls back, for messages posted
before the metadata existed, to a URL scan scoped to our own messages (those
carrying the ai-footer marker).

Output (JSON, one line):
    {"found": true, "ts": "...", "thread_ts": "...", "text": "...", "user": "U..."}
    {"found": false}
"""

import json
import re
import time
from dataclasses import dataclass
from typing import Annotated

import typer

from .client import SlackApiError, slack_paginate
from .common import AI_TOOLS_FOOTER_MARKERS, REVIEW_METADATA_EVENT_TYPE, get_slack_token

SEARCH_WINDOW_DAYS = 30
PAGE_LIMIT = 200


@dataclass
class MatchResult:
    found: bool
    ts: str = ""
    thread_ts: str = ""
    text: str = ""
    user: str = ""
    blocks: list[dict[str, object]] | None = None

    def to_json(self) -> str:
        if not self.found:
            return json.dumps({"found": False})
        return json.dumps(
            {
                "found": True,
                "ts": self.ts,
                "thread_ts": self.thread_ts or self.ts,
                "text": self.text,
                "user": self.user,
            }
        )


def build_mr_url(project_url: str, mr_iid: int) -> str:
    """Build the full GitLab MR URL from project URL and IID."""
    return f"{project_url.rstrip('/')}/-/merge_requests/{mr_iid}"


def _build_pattern(mr_url: str) -> re.Pattern[str]:
    """Build a regex that matches the full MR URL in message text.

    Slack wraps URLs in <url> or <url|label>, so the URL may appear
    inside angle brackets or followed by a pipe. The escaped URL
    handles this naturally since we just need a substring match.
    """
    return re.compile(re.escape(mr_url) + r"(?!\d)")


def _block_text(msg: dict[str, object]) -> str:
    """Concatenate the text of every block element (section text + context elements)."""
    parts: list[str] = []
    blocks = msg.get("blocks")
    if isinstance(blocks, list):
        for block in blocks:
            if not isinstance(block, dict):
                continue
            text_obj = block.get("text")
            if isinstance(text_obj, dict):
                parts.append(str(text_obj.get("text", "")))
            elements = block.get("elements")
            if isinstance(elements, list):
                for el in elements:
                    if isinstance(el, dict):
                        parts.append(str(el.get("text", "")))
    return " ".join(parts)


def _extract_text(msg: dict[str, object]) -> str:
    """Extract all searchable text from a Slack message (text + attachments + blocks)."""
    parts = [str(msg.get("text", ""))]
    attachments = msg.get("attachments")
    if isinstance(attachments, list):
        for att in attachments:
            if isinstance(att, dict):
                parts.append(str(att.get("text", "")))
                parts.append(str(att.get("fallback", "")))
    parts.append(_block_text(msg))
    return " ".join(parts)


def _as_int(value: object) -> int | None:
    """Coerce a metadata value (JSON int or str) to int, or None when not numeric."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def _metadata_matches(msg: dict[str, object], project_url: str, mr_iid: int) -> bool:
    """Whether the message carries our review metadata for exactly this (project, MR).

    This is the robust identity check: only messages our tooling posted carry the
    ``ai_tools_review_request`` event, so a human's message merely quoting the same
    MR link never matches.
    """
    meta = msg.get("metadata")
    if not isinstance(meta, dict) or meta.get("event_type") != REVIEW_METADATA_EVENT_TYPE:
        return False
    payload = meta.get("event_payload")
    if not isinstance(payload, dict):
        return False
    project = payload.get("project")
    return (
        isinstance(project, str)
        and project.rstrip("/") == project_url.rstrip("/")
        and _as_int(payload.get("mr_iid")) == mr_iid
    )


def _is_ai_tools_message(msg: dict[str, object]) -> bool:
    """Whether the message was posted by our tooling (carries an ai-footer marker).

    Any known marker counts: messages posted before the registry migration carry
    the PyPI-link footer, newer ones the GitLab one.
    """
    text = _extract_text(msg)
    return any(marker in text for marker in AI_TOOLS_FOOTER_MARKERS)


def _to_match(msg: dict[str, object]) -> MatchResult:
    ts = str(msg.get("ts", ""))
    raw_blocks = msg.get("blocks")
    return MatchResult(
        found=True,
        ts=ts,
        thread_ts=str(msg.get("thread_ts", "") or ts),
        text=str(msg.get("text", "")),
        user=str(msg.get("user", "")),
        blocks=raw_blocks if isinstance(raw_blocks, list) else None,
    )


def _metadata_match(messages: list[dict[str, object]], project_url: str, mr_iid: int) -> MatchResult | None:
    """First message (most-recent-first) carrying our review metadata for (project, MR)."""
    for msg in messages:
        if isinstance(msg, dict) and _metadata_matches(msg, project_url, mr_iid):
            return _to_match(msg)
    return None


def _fallback_match(messages: list[dict[str, object]], mr_url: str) -> MatchResult | None:
    """Legacy fallback: first *own* message (ai-footer marker) containing the MR URL.

    Scoped to messages we posted so the URL scan never matches a human's message
    that merely cites the same link — the failure mode the metadata path fixes.
    Retained for messages posted before the metadata existed; can be dropped once
    the search window (30 days) has rolled past the migration.
    """
    pattern = _build_pattern(mr_url)
    for msg in messages:
        if isinstance(msg, dict) and _is_ai_tools_message(msg) and pattern.search(_extract_text(msg)):
            return _to_match(msg)
    return None


def find_in_messages(messages: list[dict[str, object]], mr_url: str, project_url: str, mr_iid: int) -> MatchResult:
    """Find the review message: by structured metadata first, then the footer-scoped
    URL fallback. Useful for testing without hitting the Slack API.
    """
    return (
        _metadata_match(messages, project_url, mr_iid) or _fallback_match(messages, mr_url) or MatchResult(found=False)
    )


def fetch_and_search(token: str, channel: str, project_url: str, mr_iid: int) -> MatchResult:
    """Paginate channel history; return the metadata-matched message if any, else the
    most recent footer-scoped URL match.

    Metadata wins over any fallback: the first metadata match (newest-first) is
    returned immediately; only when no message carries our metadata do we settle for
    the first footer-scoped URL match seen.
    """
    mr_url = build_mr_url(project_url, mr_iid)
    oldest = str(int(time.time()) - SEARCH_WINDOW_DAYS * 86400)
    params = {
        "channel": channel,
        "oldest": oldest,
        "limit": str(PAGE_LIMIT),
        "inclusive": "true",
        "include_all_metadata": "true",
    }
    pattern = _build_pattern(mr_url)
    fallback: MatchResult | None = None
    for msg in slack_paginate(token, "conversations.history", params, items_key="messages"):
        if _metadata_matches(msg, project_url, mr_iid):
            return _to_match(msg)
        if fallback is None and _is_ai_tools_message(msg) and pattern.search(_extract_text(msg)):
            fallback = _to_match(msg)
    return fallback or MatchResult(found=False)


cli = typer.Typer()


@cli.command()
def main(
    channel: Annotated[str, typer.Option("--channel", help="Slack channel ID")],
    project_url: Annotated[
        str, typer.Option("--project-url", help="GitLab project URL (e.g. https://gitlab.com/pysae/api)")
    ],
    mr_iid: Annotated[int, typer.Option("--mr-iid", help="GitLab MR IID")],
) -> None:
    """Find the Slack review-request message for a GitLab MR."""
    token = get_slack_token()
    if not token:
        print(json.dumps({"found": False, "error": "no Slack token available"}))
        raise typer.Exit(code=1)

    try:
        result = fetch_and_search(token, channel, project_url, mr_iid)
    except SlackApiError as e:
        print(json.dumps({"found": False, "error": str(e)}))
        raise typer.Exit(code=1) from None

    print(result.to_json())


if __name__ == "__main__":
    cli()
