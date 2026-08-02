"""Rewrite the ``*Status* : …`` line of an existing Slack message.

Fetches the message text via ``conversations.history`` (single-message
window via ``latest=ts&inclusive=true&limit=1``), regex-replaces the
line starting with ``*Status* :`` with the new value, then calls
``chat.update`` with the full updated text. The rest of the message
body is preserved verbatim.

Designed for the pre-release review header lifecycle (en cours de
validation → validé, déploiement en cours → déployé en production,
etc.) but generic enough to update any Slack message that follows the
``*Status* : <…>`` convention on a single line.

Usage:
    pysae-ai-tools slack set-status-line \\
        --channel C0123ABCDEF \\
        --ts 1700000000.000200 \\
        --status ":rocket: validé, déploiement en cours"

Uses :func:`pysae_ai_tools.slack.common.get_slack_token` for
authentication. The token must hold ``channels:history`` (read) and
``chat:write`` (update), and the actual update is constrained by Slack
to the original author of the message.

Output (JSON, one line):
    {"ok": true, "ts": "1700000000.000200", "channel": "C..."}
    {"ok": false, "error": "<slack error code or message>"}
"""

import json
import re
from typing import Annotated

import typer

from .client import SlackApiError, slack_get, slack_post
from .common import get_slack_token

_STATUS_LINE_RE = re.compile(r"^\*Status\* :.*$", re.MULTILINE)


def fetch_message_text(token: str, channel: str, ts: str) -> str | None:
    """Return the text of the single message at ``ts`` in ``channel``, or None."""
    parsed = slack_get(
        token, "conversations.history", {"channel": channel, "latest": ts, "inclusive": "true", "limit": "1"}
    )
    messages = parsed.get("messages")
    if not isinstance(messages, list) or not messages:
        return None
    first = messages[0]
    if not isinstance(first, dict):
        return None
    if first.get("ts") != ts:
        return None
    text = first.get("text")
    return text if isinstance(text, str) else None


def update_message(token: str, channel: str, ts: str, text: str) -> dict[str, object]:
    """Call chat.update with the rewritten text."""
    return slack_post(token, "chat.update", {"channel": channel, "ts": ts, "text": text})


cli = typer.Typer()


@cli.command()
def main(
    channel: Annotated[str, typer.Option("--channel", help="Slack channel ID")],
    ts: Annotated[str, typer.Option("--ts", help="Timestamp of the message to update")],
    status: Annotated[
        str,
        typer.Option(
            "--status",
            help="New status content (emoji + text). Inserted after `*Status* : `.",
        ),
    ],
) -> None:
    """Rewrite the *Status* line of a Slack message in place."""
    token = get_slack_token()
    if not token:
        print(json.dumps({"ok": False, "error": "no Slack token available"}))
        raise typer.Exit(code=1)

    try:
        body = fetch_message_text(token, channel, ts)
    except SlackApiError as e:
        print(json.dumps({"ok": False, "error": f"fetch failed: {e}"}))
        raise typer.Exit(code=1) from None

    if body is None:
        print(json.dumps({"ok": False, "error": "message not found at given ts"}))
        raise typer.Exit(code=1)

    new_line = f"*Status* : {status}"
    if _STATUS_LINE_RE.search(body):
        new_body = _STATUS_LINE_RE.sub(new_line, body, count=1)
    else:
        # No existing line — append at the end of the body so the message still carries the info.
        new_body = body.rstrip() + "\n\n" + new_line

    if new_body == body:
        print(json.dumps({"ok": True, "ts": ts, "channel": channel, "noop": True}))
        return

    try:
        result = update_message(token, channel, ts, new_body)
    except SlackApiError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        raise typer.Exit(code=1) from None

    print(json.dumps({"ok": True, "ts": result.get("ts"), "channel": result.get("channel")}))


if __name__ == "__main__":
    cli()
