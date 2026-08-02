"""``pysae-ai-tools issue epic view`` — print an epic as JSON."""

from dataclasses import asdict
from typing import Annotated

import typer

from ...common.issue_tracking.provider import UnsupportedCapability
from ..resolve import print_json, resolve_provider


def main(
    iid: Annotated[str, typer.Argument(help="Epic number")],
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """Fetch an epic and print it as JSON."""
    provider = resolve_provider(project=project or None)
    try:
        epic = provider.get_epic(iid)
    except UnsupportedCapability as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    print_json(asdict(epic))
