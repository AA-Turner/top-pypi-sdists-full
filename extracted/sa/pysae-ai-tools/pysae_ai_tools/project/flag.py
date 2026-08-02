"""Check a per-repo boolean flag from ``.pysae-ai-tools.yaml`` via exit code.

Skills call this instead of parsing ``project show --json`` with ``jq``: the flag
check is integrated end-to-end, with a clean exit-code contract.

    pysae-ai-tools project flag <dotted.path> [--root DIR]

Exit codes:
    0  the flag is true  (enabled)
    1  the flag is false (disabled)
    2  the path does not exist in the schema

A missing or malformed config degrades to the schema defaults, so each flag keeps
its own default (``issues.enabled`` → enabled, ``release.allow_prerelease`` →
disabled, …). Typical use in a skill:

    pysae-ai-tools project flag issues.enabled || echo "skip — issue creation off"
"""

from pathlib import Path
from typing import Annotated

import typer

from ..common.project_config import (
    ProjectConfig,
    ProjectConfigError,
    flag_enabled,
    load_project_config_for,
)

app = typer.Typer()


@app.command()
def main(
    path: Annotated[str, typer.Argument(help="Dotted flag path, e.g. issues.enabled or slack.notifications.mep.")],
    root: Annotated[Path, typer.Option("--root", help="Repository root (defaults to current directory).")] = Path("."),
    project: Annotated[
        str | None,
        typer.Option("--project", help="GitLab project (path or ID): local checkout first, else GitLab."),
    ] = None,
    ref: Annotated[
        str | None, typer.Option("--ref", help="Git ref for --project (default: project default branch).")
    ] = None,
) -> None:
    """Exit 0 if the dotted flag is true, 1 if false, 2 if the path is unknown."""
    if project is not None:
        try:
            cfg = load_project_config_for(project, ref)
        except (ProjectConfigError, RuntimeError) as exc:
            typer.secho(f"⚠ {exc}; using schema defaults", fg=typer.colors.YELLOW, err=True)
            cfg = None
        cfg = cfg or ProjectConfig()
        try:
            obj: object = cfg
            for attr in path.split("."):
                obj = getattr(obj, attr)
        except AttributeError:
            typer.secho(f"✗ unknown flag path: {path}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=2) from None
        raise typer.Exit(code=0 if bool(obj) else 1)

    try:
        enabled = flag_enabled(root, *path.split("."))
    except AttributeError:
        typer.secho(f"✗ unknown flag path: {path}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from None
    raise typer.Exit(code=0 if enabled else 1)


if __name__ == "__main__":
    app()
