"""List every env var / secret that ``pysae-ai-tools`` knows how to resolve.

    pysae-ai-tools env list [--json]

The catalogue is :data:`pysae_ai_tools.env.config.ENV_CONFIG` — the single
source of truth for what ``env resolve`` can produce. For each variable it
prints the description and the ordered resolver chain (where the value comes
from: AWS Secrets Manager, glab, a manual step, …), so a user can
see at a glance which secrets are supported and how they are obtained. Never
prints any secret value.
"""

import json
import sys
from typing import Annotated

import typer

from .config import ENV_CONFIG

app = typer.Typer()


@app.command()
def main(
    as_json: Annotated[
        bool,
        typer.Option("--json", help="Emit the catalogue as JSON instead of a human-readable list."),
    ] = False,
) -> None:
    """List all env vars / secrets supported by pysae-ai-tools and how they resolve."""
    if as_json:
        payload = {
            var: {
                "description": spec.description,
                "cache": spec.cache,
                "resolvers": [r.source_description for r in spec.resolvers],
                "resolved_name": spec.resolved_name or var,
                "environment": spec.environment,
            }
            for var, spec in ENV_CONFIG.items()
        }
        json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return

    for var, spec in ENV_CONFIG.items():
        typer.secho(var, fg=typer.colors.CYAN, bold=True)
        typer.echo(f"  {spec.description}")
        name = spec.resolved_name or var
        alias = f"{name} ({spec.environment})" if spec.environment else name
        typer.echo(f"  resolved name: {alias}")
        for idx, resolver in enumerate(spec.resolvers):
            arrow = "→" if idx == 0 else "↳"
            typer.secho(f"    {arrow} {resolver.source_description}", fg=typer.colors.BRIGHT_BLACK)
        typer.echo("")
    typer.echo(f"{len(ENV_CONFIG)} variable(s) supported", err=True)


if __name__ == "__main__":
    app()
