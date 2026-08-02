"""``pysae-ai-tools issue epic list`` — list open epics as JSON."""

from dataclasses import asdict
from typing import Annotated

import typer

from ...common.issue_tracking.provider import UnsupportedCapability
from ..resolve import print_json, resolve_provider


def main(
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """Print every open epic under the owner namespace as JSON."""
    provider = resolve_provider(project=project or None)
    try:
        epics = provider.list_open_epics()
    except UnsupportedCapability as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    print_json([asdict(e) for e in epics])
