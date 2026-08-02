"""List every Pysae repo and its resolved ``.pysae-ai-tools.yaml`` config.

This is the cross-repo counterpart of ``project show`` (one repo). It aggregates the
per-repo configs so nothing has to be regenerated when a project's config changes.

    pysae-ai-tools project list [--json] [--repos a,b,c] [--ref BRANCH] [--refresh]

Without ``--repos`` it discovers every ``pysae`` group project (incl. subgroups) and
keeps those that carry a config. Discovery and the per-repo GitLab config fetches are
**cached** on disk (TTL 5 min, shared with ``project show``) since they are stable
config data — pass ``--refresh`` to bypass. ``--json`` emits ``{path: config}``.
"""

import json
import sys
from typing import Annotated

import typer

from ..common.project_config import aggregate_project_configs, discover_project_paths

app = typer.Typer()


def _resolve_paths(repos: str | None, refresh: bool) -> list[str]:
    if repos:
        return [p.strip() for p in repos.split(",") if p.strip()]
    return discover_project_paths(refresh=refresh)


@app.command()
def main(
    repos: Annotated[
        str | None, typer.Option("--repos", help="Comma-separated repo paths (else: discover the pysae group).")
    ] = None,
    ref: Annotated[
        str | None, typer.Option("--ref", help="Git ref to read configs from (default: each repo's default branch).")
    ] = None,
    local: Annotated[
        bool,
        typer.Option(
            "--local", help="Prefer local checkouts (reflect uncommitted edits), GitLab fallback if uncloned."
        ),
    ] = False,
    as_json: Annotated[bool, typer.Option("--json", help="Emit {path: config} JSON instead of a summary.")] = False,
    refresh: Annotated[bool, typer.Option("--refresh", help="Bypass the on-disk cache and re-fetch.")] = False,
) -> None:
    """Aggregate and print every repo's config from GitLab (canonical); --local for clones."""
    try:
        paths = _resolve_paths(repos, refresh)
    except RuntimeError as exc:
        typer.secho(f"✗ {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from None
    configs = aggregate_project_configs(paths, ref=ref, refresh=refresh, prefer_local=local)
    if as_json:
        json.dump(
            {path: cfg.model_dump(mode="json") for path, cfg in configs.items()},
            sys.stdout,
            indent=2,
            ensure_ascii=False,
        )
        sys.stdout.write("\n")
        return
    for path, cfg in configs.items():
        name = cfg.name_for("en") or "—"
        channel = cfg.slack.tech_channel or "—"
        services = ", ".join(s.name for s in cfg.k8s.services) or "—"
        typer.echo(f"{path}\t{name}\t{channel}\t[{services}]")
    typer.echo(f"\n{len(configs)} repo(s) with a config", err=True)


if __name__ == "__main__":
    app()
