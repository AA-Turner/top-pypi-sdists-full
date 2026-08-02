"""``pysae-ai-tools issue list`` — list issues as JSON."""

from dataclasses import asdict
from typing import Annotated

import typer

from .resolve import print_json, resolve_provider


def main(
    search: Annotated[str, typer.Option("--search", help="Full-text search")] = "",
    assignee: Annotated[str, typer.Option("--assignee", help="Filter by assignee username")] = "",
    label: Annotated[list[str] | None, typer.Option("--label", help="Filter by label (repeatable)")] = None,
    state: Annotated[str, typer.Option("--state", help="opened / closed / all")] = "opened",
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """List issues (optionally filtered) and print them as JSON."""
    provider = resolve_provider(project=project or None)
    issues = provider.list_issues(
        search=search or None,
        assignee=assignee or None,
        labels=label or None,
        state=state,
    )
    print_json([asdict(i) for i in issues])
