"""``pysae-ai-tools issue epic create`` — create an epic under the owner namespace."""

from pathlib import Path
from typing import Annotated

import typer

from ...common.issue_tracking.provider import UnsupportedCapability
from ..resolve import print_json, resolve_provider


def main(
    title: Annotated[str, typer.Option("--title", help="Epic title")],
    description: Annotated[str, typer.Option("--description", help="Epic description body")] = "",
    description_file: Annotated[str, typer.Option("--description-file", help="Read the body from this file")] = "",
    label: Annotated[list[str] | None, typer.Option("--label", help="Label (repeatable)")] = None,
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """Create an epic and print it as JSON."""
    body = Path(description_file).read_text(encoding="utf-8", errors="replace") if description_file else description
    provider = resolve_provider(project=project or None)
    try:
        epic = provider.create_epic(title=title, description=body, labels=label or None)
    except UnsupportedCapability as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    print_json({"iid": epic.iid, "web_url": epic.web_url, "title": epic.title})
