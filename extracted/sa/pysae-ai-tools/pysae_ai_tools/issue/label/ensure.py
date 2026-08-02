"""``pysae-ai-tools issue label ensure`` — create an owner-scoped label if absent."""

from typing import Annotated

import typer

from ...common.issue_tracking.provider import UnsupportedCapability
from ..resolve import resolve_provider


def main(
    name: Annotated[str, typer.Argument(help="Label name (e.g. version::v1.2.3)")],
    color: Annotated[str, typer.Option("--color", help="Hex color, e.g. #ff0000")] = "",
    description: Annotated[str, typer.Option("--description", help="Label description")] = "",
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """Ensure an owner-scoped label exists, creating it when missing."""
    provider = resolve_provider(project=project or None)
    try:
        label = provider.ensure_owner_label(name, color=color, description=description)
    except UnsupportedCapability as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(label.name)
