"""``pysae-ai-tools mr whoami`` — print the authenticated username."""

from typing import Annotated

import typer

from .resolve import resolve_provider

_PROJECT_HELP = "Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL"


def main(
    project: Annotated[str, typer.Option("--project", help=_PROJECT_HELP)] = "",
) -> None:
    """Print the username of the authenticated account."""
    typer.echo(resolve_provider(project=project or None).current_user())
