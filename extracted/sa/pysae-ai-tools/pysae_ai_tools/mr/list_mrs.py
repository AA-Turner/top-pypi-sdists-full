"""``pysae-ai-tools mr list`` — list merge requests as JSON."""

from dataclasses import asdict
from typing import Annotated

import typer

from .resolve import print_json, resolve_provider

_PROJECT_HELP = "Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL"


def main(
    search: Annotated[str, typer.Option("--search", help="Full-text search")] = "",
    author: Annotated[str, typer.Option("--author", help="Filter by author username")] = "",
    assignee: Annotated[str, typer.Option("--assignee", help="Filter by assignee username")] = "",
    label: Annotated[list[str] | None, typer.Option("--label", help="Filter by label (repeatable)")] = None,
    state: Annotated[str, typer.Option("--state", help="opened / closed / all")] = "opened",
    project: Annotated[str, typer.Option("--project", help=_PROJECT_HELP)] = "",
) -> None:
    """List merge requests (optionally filtered) and print them as JSON."""
    provider = resolve_provider(project=project or None)
    mrs = provider.list_mrs(
        search=search or None,
        author=author or None,
        assignee=assignee or None,
        labels=label or None,
        state=state,
    )
    print_json([asdict(m) for m in mrs])
