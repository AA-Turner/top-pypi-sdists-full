"""``pysae-ai-tools issue note`` — post a comment on an issue."""

from pathlib import Path
from typing import Annotated

import typer

from .resolve import resolve_provider


def main(
    iid: Annotated[str, typer.Argument(help="Issue number")],
    message: Annotated[str, typer.Option("--message", help="Comment body")] = "",
    message_file: Annotated[str, typer.Option("--message-file", help="Read the body from this file")] = "",
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """Post a comment on an issue."""
    body = Path(message_file).read_text(encoding="utf-8", errors="replace") if message_file else message
    if not body:
        typer.echo("a comment body is required (--message or --message-file)", err=True)
        raise typer.Exit(code=1)
    resolve_provider(project=project or None).add_note(iid, body)
