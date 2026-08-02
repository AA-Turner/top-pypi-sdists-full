"""Show the GitLab group ai-tools operates on, and where it was resolved from.

The group is resolved generically (see ``common.group``): explicit ``--group`` →
current repo's origin namespace → ``$PYSAE_AI_TOOLS_GROUP`` → ``"pysae"`` default. This
command surfaces the resolved path, its ``source``, and the numeric ID (live via glab).

    pysae-ai-tools project group [--group PATH] [--json] [--refresh]
"""

import json
from pathlib import Path
from typing import Annotated

import typer

from ..common.group import resolve_group_id, resolve_group_identity

app = typer.Typer()


@app.command()
def main(
    group: Annotated[
        str | None, typer.Option("--group", help="Force a group path (else: derived from origin / env / default).")
    ] = None,
    root: Annotated[Path, typer.Option("--root", help="Repository root used to derive the group from origin.")] = Path(
        "."
    ),
    json_output: Annotated[bool, typer.Option("--json", help="Emit JSON instead of text.")] = False,
    refresh: Annotated[
        bool, typer.Option("--refresh", help="Bypass the on-disk cache for the group ID lookup.")
    ] = False,
) -> None:
    """Print the resolved group path, its source, and numeric ID."""
    identity = resolve_group_identity(explicit=group, root=root)
    group_id: int | None
    try:
        group_id = resolve_group_id(identity.path, refresh=refresh)
    except RuntimeError:
        group_id = None  # glab unavailable — still report the path/source
    if json_output:
        typer.echo(json.dumps({"path": identity.path, "id": group_id, "source": identity.source}, ensure_ascii=False))
        return
    typer.echo(f"path:   {identity.path}")
    typer.echo(f"id:     {group_id if group_id is not None else '— (glab unavailable)'}")
    typer.echo(f"source: {identity.source}")


if __name__ == "__main__":
    app()
