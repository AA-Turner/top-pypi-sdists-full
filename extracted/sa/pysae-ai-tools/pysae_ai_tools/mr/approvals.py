"""``pysae-ai-tools mr approvals`` — print the current approval count (Capability.APPROVALS)."""

from typing import Annotated

import typer

from ..common.merge_requests.provider import UnsupportedCapability
from .resolve import resolve_provider

_PROJECT_HELP = "Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL"


def main(
    iid: Annotated[str, typer.Argument(help="Merge request number")],
    project: Annotated[str, typer.Option("--project", help=_PROJECT_HELP)] = "",
) -> None:
    """Print the number of current approvals on a merge request."""
    provider = resolve_provider(project=project or None)
    try:
        typer.echo(str(provider.approvals_count(iid)))
    except UnsupportedCapability as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
