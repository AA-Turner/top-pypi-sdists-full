"""``pysae-ai-tools mr rebase`` — rebase a merge request onto its target (Capability.REBASE)."""

from typing import Annotated

import typer

from ..common.merge_requests.provider import UnsupportedCapability
from .resolve import resolve_provider

_PROJECT_HELP = "Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL"


def main(
    iid: Annotated[str, typer.Argument(help="Merge request number")],
    project: Annotated[str, typer.Option("--project", help=_PROJECT_HELP)] = "",
) -> None:
    """Rebase a merge request onto its target branch (server-side)."""
    provider = resolve_provider(project=project or None)
    try:
        provider.rebase(iid)
    except UnsupportedCapability as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(f"rebased !{iid}")
