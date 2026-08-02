"""Update an existing Slack message via ``chat.update``.

Usage:
    pysae-ai-tools slack update-message \\
        --channel C0123ABCDEF \\
        --ts 1700000000.000200 \\
        --text "Updated content"

    # Multiline text via stdin (--text -)
    pysae-ai-tools slack update-message --channel C... --ts 1700... --text - <<EOF
    line 1
    line 2
    EOF

Both ``--channel`` and ``--ts`` are required — ``chat.update`` needs the
exact message coordinates. Use the values returned by ``post-message``.

Uses :func:`pysae_ai_tools.slack.common.get_slack_token` for authentication:
the user token locally, the bot token in CI.

Output (JSON, one line):
    {"ok": true, "ts": "1700000000.000200", "channel": "C0123ABCDEF"}
    {"ok": false, "error": "<slack error code or message>"}
"""

import json
import sys
from collections.abc import Mapping
from typing import Annotated

import typer

from .client import SlackApiError, slack_post
from .common import get_slack_token


def update_message(token: str, payload: Mapping[str, object]) -> dict[str, object]:
    """Call chat.update (JSON body) and return the parsed response.

    ``payload`` carries ``channel`` + ``ts`` and the new content. Pass ``blocks``
    (a list) alongside ``text`` when the message uses blocks — sending ``text``
    alone on a block message drops the blocks and flattens the rendering.
    """
    return slack_post(token, "chat.update", dict(payload))


cli = typer.Typer()


@cli.command()
def main(
    channel: Annotated[str, typer.Option("--channel", help="Slack channel ID")],
    ts: Annotated[str, typer.Option("--ts", help="Timestamp of the message to update")],
    text: Annotated[
        str,
        typer.Option(
            "--text",
            help="New message text (mrkdwn). Use '-' to read from stdin.",
        ),
    ],
) -> None:
    """Edit a previously-posted Slack message via chat.update."""
    body = sys.stdin.read() if text == "-" else text
    if not body.strip():
        print(json.dumps({"ok": False, "error": "empty message body"}))
        raise typer.Exit(code=1)

    token = get_slack_token()
    if not token:
        print(json.dumps({"ok": False, "error": "no Slack token available"}))
        raise typer.Exit(code=1)

    payload: dict[str, str] = {"channel": channel, "ts": ts, "text": body}

    try:
        result = update_message(token, payload)
    except SlackApiError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        raise typer.Exit(code=1) from None

    print(json.dumps({"ok": True, "ts": result.get("ts"), "channel": result.get("channel")}))


if __name__ == "__main__":
    cli()
