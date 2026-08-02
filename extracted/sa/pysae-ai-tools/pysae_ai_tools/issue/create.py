"""``pysae-ai-tools issue create`` — create an issue via the resolved provider."""

from pathlib import Path
from typing import Annotated

import typer

from ..common.project_config import flag_enabled
from .resolve import resolve_provider


def main(
    title: Annotated[str, typer.Option("--title", help="Issue title")],
    description: Annotated[str, typer.Option("--description", help="Issue description body")] = "",
    description_file: Annotated[str, typer.Option("--description-file", help="Read the body from this file")] = "",
    label: Annotated[list[str] | None, typer.Option("--label", help="Label (repeatable)")] = None,
    assignee: Annotated[list[str] | None, typer.Option("--assignee", help="Assignee username (repeatable)")] = None,
    weight: Annotated[int | None, typer.Option("--weight", help="Fibonacci weight")] = None,
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """Create an issue and print its URL."""
    # Honour the per-repo creation flag centrally, so every caller is covered.
    if not project and not flag_enabled(Path.cwd(), "issues", "enabled"):
        typer.echo("skipped: issues.enabled is false for this repo — no issue created")
        return
    body = Path(description_file).read_text(encoding="utf-8", errors="replace") if description_file else description
    provider = resolve_provider(project=project or None)
    issue = provider.create_issue(
        title=title,
        description=body,
        labels=label or [],
        assignees=assignee or [],
        weight=weight,
    )
    typer.echo(issue.web_url or issue.iid)
