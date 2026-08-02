"""Show the effective per-repo config (the stable project data).

This is the **config/stable** side of the context, separate from ``detect-context``
(which carries only the *dynamic* branch context). It emits the effective config —
the ``.pysae-ai-tools.yaml`` file merged over schema defaults — and nothing else: the
output mirrors the config file structure exactly, with no synthesised keys. The
``.pysae-ai-tools/`` overlay directory and ``overlay:`` references are resolved at load
time, so what is printed is always the fully-resolved config. YAML by default, JSON
with ``--json``.

    pysae-ai-tools project show [PATH...] [--root DIR | --project PATH [--ref REF] [--local]] [--json]

Optional dotted ``PATH`` arguments narrow the output — a **getter** that replaces
``… --json | jq``:

- one path (``slack.tech_channel_id``, ``release``) → that value: a string verbatim,
  a scalar list one element per line (like ``jq '.x[]'``), any other subtree as YAML/JSON;
- list elements are addressable by index (``project.labels.0``, ``release.tracks.-1``);
- **several paths at once** → one value per line, in request order (so successive
  ``read`` calls capture them without ``jq``); with ``--json``, a ``{path: value}`` object.

Like ``project list``, ``--project`` reads the **canonical** default branch on GitLab by
default — a local checkout may be on a feature branch, dirty, or stale. Pass ``--local`` to
prefer the local clone (reflecting uncommitted edits), falling back to GitLab when uncloned.
"""

import json
from pathlib import Path
from typing import Annotated

import typer
import yaml

from ..common.project_config import (
    ProjectConfig,
    ProjectConfigError,
    config_path,
    load_project_config,
    load_project_config_for,
    load_project_config_from_gitlab,
    local_checkout,
)

app = typer.Typer()


def _narrow(data: object, path: str) -> object:
    """Descend ``data`` along the dotted ``path``; exit 2 on an unknown key/index.

    Dict keys are matched by name; a list is indexed when the segment is a valid
    (possibly negative) integer, so ``project.labels.0`` and ``release.tracks.-1`` work.
    """
    node = data
    for key in path.split("."):
        if isinstance(node, dict) and key in node:
            node = node[key]
            continue
        if isinstance(node, list):
            idx = _list_index(key, node)
            if idx is not None:
                node = node[idx]
                continue
        typer.secho(f"✗ unknown config path: {path}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2)
    return node


def _list_index(key: str, seq: list[object]) -> int | None:
    """Return ``key`` as an in-range list index (negatives allowed), or ``None``."""
    try:
        i = int(key)
    except ValueError:
        return None
    return i if -len(seq) <= i < len(seq) else None


def _emit_one(node: object, *, json_output: bool) -> None:
    """Print a single narrowed value (getter for one path)."""
    if json_output:
        typer.echo(json.dumps(node, ensure_ascii=False, indent=2))
    elif isinstance(node, str):
        if node.strip():
            typer.echo(node)
    elif isinstance(node, list) and all(_is_scalar(el) for el in node):
        # A scalar list prints one element per line, like `jq -r '.x[]'`.
        for el in node:
            typer.echo(el if isinstance(el, str) else json.dumps(el))
    elif node is not None:
        typer.echo(yaml.safe_dump(node, sort_keys=False, allow_unicode=True).rstrip())


def _emit_many(pairs: list[tuple[str, object]], *, json_output: bool) -> None:
    """Print several narrowed values — one per line in order, or a JSON object."""
    if json_output:
        typer.echo(json.dumps(dict(pairs), ensure_ascii=False, indent=2))
        return
    # One physical line per requested path (blank for empty), so a caller can capture
    # them with successive `read` — a jq-free way to pull several scalars at once.
    for _path, node in pairs:
        if isinstance(node, str):
            typer.echo(node)
        elif node is None:
            typer.echo("")
        else:
            typer.echo(json.dumps(node, ensure_ascii=False))


def _is_scalar(value: object) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


@app.command()
def main(
    paths: Annotated[
        list[str] | None,
        typer.Argument(
            help="Dotted key(s) to narrow the output, e.g. slack.tech_channel_id or release. "
            "Pass several to read them at once (one value per line). Omit for the whole config."
        ),
    ] = None,
    root: Annotated[Path, typer.Option("--root", help="Repository root (defaults to current directory).")] = Path("."),
    project: Annotated[
        str | None,
        typer.Option("--project", help="GitLab project (path or ID): canonical default branch; --local for the clone."),
    ] = None,
    ref: Annotated[
        str | None, typer.Option("--ref", help="Git ref for --project (default: project default branch).")
    ] = None,
    local: Annotated[
        bool,
        typer.Option("--local", help="With --project: prefer the local checkout (uncommitted edits), GitLab fallback."),
    ] = False,
    json_output: Annotated[bool, typer.Option("--json", help="Emit JSON instead of YAML (for jq).")] = False,
    refresh: Annotated[
        bool, typer.Option("--refresh", help="Bypass the on-disk cache for --project (re-fetch from GitLab).")
    ] = False,
) -> None:
    """Print the effective config (file + defaults) as YAML, or JSON with ``--json``."""
    try:
        if project is not None:
            fetch = load_project_config_for if local else load_project_config_from_gitlab
            cfg = fetch(project, ref, refresh=refresh)
        else:
            cfg = load_project_config(root)
    except (ProjectConfigError, RuntimeError) as exc:
        typer.secho(f"✗ {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from None
    effective = cfg if cfg is not None else ProjectConfig()
    data = effective.model_dump(mode="json")
    if paths:
        pairs = [(p, _narrow(data, p)) for p in paths]
        if len(pairs) == 1:
            _emit_one(pairs[0][1], json_output=json_output)
        else:
            _emit_many(pairs, json_output=json_output)
        return
    if json_output:
        typer.echo(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if project is not None:
        # Mirror what was actually read: --local reads the clone only when present and no ref
        # is forced (an explicit ref always goes through GitLab); otherwise it's canonical GitLab.
        checkout = local_checkout(project) if local and ref is None else None
        origin = f"local {checkout}" if checkout else f"GitLab {project}"
        source_line = f"# effective config — project {project} ({origin})"
    elif config_path(root):
        source_line = f"# effective config — source: {config_path(root)}"
    else:
        source_line = "# effective config — no file, all defaults"
    typer.echo(source_line)
    typer.echo(yaml.safe_dump(data, sort_keys=False, allow_unicode=True).rstrip())


if __name__ == "__main__":
    app()
