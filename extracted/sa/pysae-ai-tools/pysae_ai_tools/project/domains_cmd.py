"""List the domain-label vocabulary — the union of every repo's **primary** domain label
(``project.labels[0]``; secondary labels like Scheduling/Security/Test are excluded).

ai-tools holds no hardcoded domain-label list: the vocabulary is whatever the per-repo
``.pysae-ai-tools.yaml`` configs declare, aggregated live (cached).

    pysae-ai-tools project domains [--json] [--refresh]
"""

import json
import sys
from typing import Annotated

import typer

from ..common.project_config import domain_labels

app = typer.Typer()


@app.command()
def main(
    as_json: Annotated[bool, typer.Option("--json", help="Emit a JSON array instead of one per line.")] = False,
    refresh: Annotated[bool, typer.Option("--refresh", help="Bypass the on-disk cache and re-aggregate.")] = False,
) -> None:
    """Print the domain labels declared across all repo configs."""
    labels = domain_labels(refresh=refresh)
    if as_json:
        json.dump(labels, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return
    for label in labels:
        typer.echo(label)


if __name__ == "__main__":
    app()
