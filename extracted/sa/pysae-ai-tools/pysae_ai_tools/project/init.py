"""Create a ``.pysae-ai-tools.yaml`` at the repo root from the bundled template.

The template is fully commented (every key at its default), so the generated file
documents the available knobs without changing behaviour. The maintainer uncomments and
fills the repo-specific values (domain ``labels``, Slack ``tech_channel``, deploy
topology, …) — ai-tools holds no per-repo defaults to pre-fill.

    pysae-ai-tools project init [--root DIR] [--force]

Idempotent: refuses to overwrite an existing file unless ``--force`` is passed.
"""

from pathlib import Path
from typing import Annotated

import typer

from .template import get_template

app = typer.Typer()


@app.command()
def main(
    root: Annotated[Path, typer.Option("--root", help="Repository root (defaults to current directory).")] = Path("."),
    force: Annotated[bool, typer.Option("--force", help="Overwrite an existing file.")] = False,
) -> None:
    """Create ``.pysae-ai-tools.yaml`` at ``root`` from the bundled template."""
    target = root / ".pysae-ai-tools.yaml"
    if target.exists() and not force:
        typer.secho(f"✗ {target} already exists (use --force to overwrite).", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    target.write_text(get_template(), encoding="utf-8")
    typer.echo(f"✓ wrote {target}")


if __name__ == "__main__":
    app()
