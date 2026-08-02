"""``pysae-ai-tools mr view`` — print a merge request as JSON."""

from dataclasses import asdict
from typing import Annotated

import typer

from .resolve import print_json, resolve_provider

_PROJECT_HELP = "Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL"


def main(
    iid: Annotated[str, typer.Argument(help="Merge request number")],
    project: Annotated[str, typer.Option("--project", help=_PROJECT_HELP)] = "",
) -> None:
    """Fetch a merge request and print it as JSON."""
    provider = resolve_provider(project=project or None)
    print_json(asdict(provider.get_mr(iid)))
