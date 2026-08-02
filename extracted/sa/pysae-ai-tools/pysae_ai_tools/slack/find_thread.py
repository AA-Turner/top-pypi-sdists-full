"""Find a Slack thread parent message by structured metadata or text prefix.

Locates an existing review/release thread before deciding whether to post a
fresh one or update the previous one. Two matching modes, metadata first:

- **Metadata** (robust): with ``--metadata-event-type`` **and** a non-empty
  ``--metadata-match`` JSON, match a top-level message carrying that
  ``event_type`` whose ``event_payload`` contains every key/value in
  ``--metadata-match``. Immune to header-text changes and to humans quoting it.
  An empty match is ignored (it would match any message of the type), falling
  through to the prefix mode.
- **Prefix** (fallback / legacy): match a top-level message whose text
  **starts** with ``--prefix`` and optionally **contains** ``--contains``.
  Used when no metadata is present (messages posted before it existed).

A metadata match wins over a prefix match.

Usage:
    pysae-ai-tools slack find-thread \\
        --channel C0123ABCDEF \\
        --metadata-event-type ai_tools_prerelease_recap \\
        --metadata-match '{"project": "https://gitlab.com/pysae/api", "tag": "v4.9.0"}' \\
        --prefix "*Review pre-release \\`v4.9.0\\` →" \\
        --contains "— \\`pysae/api\\`"

Uses :func:`pysae_ai_tools.slack.common.get_slack_token` for
authentication: the user token locally, the bot token in CI. The
matching token must hold ``channels:history`` (or
``groups:history`` for private channels).

Output (JSON, one line):
    {"ok": true, "ts": "1700000000.000200", "channel": "C..."}
    {"ok": true, "ts": null, "channel": "C..."}   # no match
    {"ok": false, "error": "<slack error code>"}
"""

import json
from collections.abc import Mapping
from typing import Annotated

import typer

from .client import SlackApiError, slack_get
from .common import get_slack_token


def _is_top_level(msg: dict[str, object]) -> bool:
    """Skip thread replies and events without a regular top-level ts."""
    return not (msg.get("thread_ts") and msg.get("thread_ts") != msg.get("ts"))


def _metadata_matches(msg: dict[str, object], event_type: str, match: Mapping[str, object]) -> bool:
    """Whether the message carries ``event_type`` and a payload superset of ``match``."""
    meta = msg.get("metadata")
    if not isinstance(meta, dict) or meta.get("event_type") != event_type:
        return False
    payload = meta.get("event_payload")
    if not isinstance(payload, dict):
        return False
    return all(str(payload.get(k, "")).rstrip("/") == str(v).rstrip("/") for k, v in match.items())


def _prefix_matches(msg: dict[str, object], prefix: str, contains: str) -> bool:
    text = msg.get("text") or ""
    if not isinstance(text, str) or not prefix or not text.startswith(prefix):
        return False
    return not (contains and contains not in text)


def find_thread_ts(
    messages: list[dict[str, object]],
    *,
    event_type: str = "",
    match: Mapping[str, object] | None = None,
    prefix: str = "",
    contains: str = "",
) -> str | None:
    """Return the ts of the matching top-level message: metadata first, prefix fallback.

    Messages are most-recent-first; a metadata match anywhere wins over any prefix
    match, otherwise the most recent prefix match is returned.
    """
    match = match or {}
    # The metadata mode needs at least one payload key: an empty match makes
    # _metadata_matches vacuously true, which would match the most recent message
    # of that event_type regardless of project/version — wrong in a shared channel.
    use_metadata = bool(event_type and match)
    prefix_ts: str | None = None
    for msg in messages:
        if not isinstance(msg, dict) or not _is_top_level(msg):
            continue
        if use_metadata and _metadata_matches(msg, event_type, match):
            return str(msg.get("ts")) if msg.get("ts") is not None else None
        if prefix_ts is None and _prefix_matches(msg, prefix, contains):
            prefix_ts = str(msg.get("ts")) if msg.get("ts") is not None else None
    return prefix_ts


cli = typer.Typer()


@cli.command()
def main(
    channel: Annotated[str, typer.Option("--channel", help="Slack channel ID")],
    prefix: Annotated[
        str,
        typer.Option("--prefix", help="Fallback: match top-level messages whose text starts with this string."),
    ] = "",
    contains: Annotated[
        str,
        typer.Option(
            "--contains",
            help="Optional secondary prefix filter — the matching message must also contain this substring.",
        ),
    ] = "",
    metadata_event_type: Annotated[
        str,
        typer.Option(
            "--metadata-event-type",
            help="Preferred: match a message with this metadata event_type (needs a non-empty --metadata-match).",
        ),
    ] = "",
    metadata_match: Annotated[
        str,
        typer.Option(
            "--metadata-match",
            help="JSON object — the metadata event_payload must contain every key/value (with --metadata-event-type).",
        ),
    ] = "",
    limit: Annotated[
        int,
        typer.Option("--limit", help="Maximum number of recent messages to scan (default 200)."),
    ] = 200,
) -> None:
    """Find the most recent top-level Slack message by metadata (preferred) or --prefix."""
    token = get_slack_token()
    if not token:
        print(json.dumps({"ok": False, "error": "no Slack token available"}))
        raise typer.Exit(code=1)

    match: dict[str, object] = {}
    if metadata_match:
        try:
            parsed_match = json.loads(metadata_match)
        except json.JSONDecodeError as e:
            print(json.dumps({"ok": False, "error": f"invalid --metadata-match JSON: {e}"}))
            raise typer.Exit(code=1) from None
        if not isinstance(parsed_match, dict):
            print(json.dumps({"ok": False, "error": "--metadata-match must be a JSON object"}))
            raise typer.Exit(code=1)
        match = parsed_match

    params = {"channel": channel, "limit": str(limit)}
    if metadata_event_type:
        params["include_all_metadata"] = "true"
    try:
        result = slack_get(token, "conversations.history", params)
    except SlackApiError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        raise typer.Exit(code=1) from None

    messages = result.get("messages")
    if not isinstance(messages, list):
        messages = []

    ts = find_thread_ts(messages, event_type=metadata_event_type, match=match, prefix=prefix, contains=contains)
    print(json.dumps({"ok": True, "ts": ts, "channel": channel}))


if __name__ == "__main__":
    cli()
