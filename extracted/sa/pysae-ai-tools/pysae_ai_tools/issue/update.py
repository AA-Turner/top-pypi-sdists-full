"""``pysae-ai-tools issue update`` — update an issue's title/body/labels."""

from pathlib import Path
from typing import Annotated

import typer

from .resolve import print_json, resolve_provider


def main(
    iid: Annotated[str, typer.Argument(help="Issue number")],
    title: Annotated[str | None, typer.Option("--title", help="New title")] = None,
    description: Annotated[str | None, typer.Option("--description", help="New description body")] = None,
    description_file: Annotated[str, typer.Option("--description-file", help="Read the body from this file")] = "",
    add_label: Annotated[list[str] | None, typer.Option("--add-label", help="Label to add (repeatable)")] = None,
    remove_label: Annotated[
        list[str] | None, typer.Option("--remove-label", help="Label to remove (repeatable)")
    ] = None,
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """Update an issue and print the updated record as JSON."""
    body = description
    if description_file:
        body = Path(description_file).read_text(encoding="utf-8", errors="replace")
    provider = resolve_provider(project=project or None)
    issue = provider.update_issue(
        iid,
        title=title,
        description=body,
        add_labels=add_label or None,
        remove_labels=remove_label or None,
    )
    print_json({"iid": issue.iid, "web_url": issue.web_url, "labels": issue.labels})
