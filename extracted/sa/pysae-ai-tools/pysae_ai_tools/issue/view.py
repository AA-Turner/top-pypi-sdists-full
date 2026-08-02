"""``pysae-ai-tools issue view`` — print an issue as JSON."""

from dataclasses import asdict
from typing import Annotated

import typer

from .resolve import print_json, resolve_provider


def main(
    iid: Annotated[str, typer.Argument(help="Issue number")],
    project: Annotated[
        str,
        typer.Option(
            "--project",
            help="Target another repo relative to the current owner ('op', 'infra/infra-cluster') or a full URL",
        ),
    ] = "",
) -> None:
    """Fetch an issue and print it as JSON."""
    provider = resolve_provider(project=project or None)
    print_json(asdict(provider.get_issue(iid)))
