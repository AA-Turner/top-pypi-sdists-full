"""``pysae-ai-tools mr update`` — update a merge request's title/body/labels/draft."""

from pathlib import Path
from typing import Annotated

import typer

from .resolve import print_json, resolve_provider

_PROJECT_HELP = "Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL"


def main(
    iid: Annotated[str, typer.Argument(help="Merge request number")],
    title: Annotated[str | None, typer.Option("--title", help="New title")] = None,
    description: Annotated[str | None, typer.Option("--description", help="New description body")] = None,
    description_file: Annotated[str, typer.Option("--description-file", help="Read the body from this file")] = "",
    add_label: Annotated[list[str] | None, typer.Option("--add-label", help="Label to add (repeatable)")] = None,
    remove_label: Annotated[
        list[str] | None, typer.Option("--remove-label", help="Label to remove (repeatable)")
    ] = None,
    draft: Annotated[bool | None, typer.Option("--draft/--ready", help="Set draft or ready state")] = None,
    project: Annotated[str, typer.Option("--project", help=_PROJECT_HELP)] = "",
) -> None:
    """Update a merge request and print the updated record as JSON."""
    body = description
    if description_file:
        body = Path(description_file).read_text(encoding="utf-8", errors="replace")
    provider = resolve_provider(project=project or None)
    mr = provider.update_mr(
        iid,
        title=title,
        description=body,
        add_labels=add_label or None,
        remove_labels=remove_label or None,
        draft=draft,
    )
    print_json({"iid": mr.iid, "web_url": mr.web_url, "labels": mr.labels, "draft": mr.draft})
