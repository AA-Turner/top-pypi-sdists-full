"""Upload a file to a Slack channel (or thread) via the modern external upload flow.

Low-level counterpart to ``slack release-file``: it takes an explicit ``--channel`` (and
optional ``--thread-ts``) instead of resolving a release thread from (app, version). Both
share the upload mechanics in :mod:`pysae_ai_tools.slack.upload`.

Usage:
    # Post a file to a channel
    pysae-ai-tools slack upload-file --channel C0123ABCDEF --file ./report.pdf

    # Attach a file to an existing thread, with a title and a leading comment
    pysae-ai-tools slack upload-file --channel mep --thread-ts 1700000000.000100 \\
        --file build/app-prod.apk --title "Driver prod" --comment ":package: APK prod"

Uses :func:`pysae_ai_tools.slack.common.get_slack_token` for authentication (user token
locally, bot token in CI); the token must hold the ``files:write`` scope.

Output (JSON, one line):
    {"ok": true, "file_id": "F0123456789", "channel": "C0123ABCDEF"}
    {"ok": false, "error": "<slack error code or message>"}
"""

import json
import urllib.error
from pathlib import Path
from typing import Annotated

import typer

from .common import get_slack_token, resolve_channel
from .upload import upload_file

cli = typer.Typer()


@cli.command()
def main(
    channel: Annotated[
        str,
        typer.Option("--channel", help="Slack channel ID, or a known name (e.g. 'mep')."),
    ],
    file: Annotated[
        Path,
        typer.Option("--file", help="Path to the file to upload.", exists=True, dir_okay=False, readable=True),
    ],
    thread_ts: Annotated[
        str,
        typer.Option("--thread-ts", help="Parent message ts — upload the file as a thread reply."),
    ] = "",
    filename: Annotated[
        str,
        typer.Option("--filename", help="Override the filename shown in Slack (defaults to the file's basename)."),
    ] = "",
    title: Annotated[
        str,
        typer.Option("--title", help="File title shown in Slack (defaults to the filename)."),
    ] = "",
    comment: Annotated[
        str,
        typer.Option("--comment", help="Optional message text posted alongside the file (initial_comment)."),
    ] = "",
    join: Annotated[
        bool,
        typer.Option(
            "--join",
            help="Self-join the (public) channel on 'not_in_channel' and retry — needs the channels:join scope.",
        ),
    ] = False,
) -> None:
    """Upload a file to a Slack channel (or thread) via files.completeUploadExternal."""
    token = get_slack_token()
    if not token:
        print(json.dumps({"ok": False, "error": "no Slack token available"}))
        raise typer.Exit(code=1)

    chan = resolve_channel(channel)
    try:
        result = upload_file(
            token,
            file,
            channel=chan,
            filename=filename,
            title=title,
            initial_comment=comment,
            thread_ts=thread_ts,
            join=join,
        )
    except (RuntimeError, urllib.error.URLError, OSError) as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        raise typer.Exit(code=1) from None

    print(json.dumps({"ok": True, "file_id": result.get("file_id"), "channel": chan}))


if __name__ == "__main__":
    cli()
