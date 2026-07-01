"""``cvc trajectory`` CLI commands."""
from __future__ import annotations

import json
from typing import Any, Dict

import click


def _fetch(path: str) -> Dict[str, Any]:
    import urllib.error
    import urllib.request

    base = "http://127.0.0.1:8765"
    try:
        with urllib.request.urlopen(f"{base}{path}", timeout=2.5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise click.ClickException(f"Gateway unreachable at {base}: {exc}") from exc


@click.group("trajectory")
def trajectory_group() -> None:
    """Inspect recorded agent trajectories (JSONL turn logs)."""


@trajectory_group.command("ls")
@click.option("--dir", "dir_path", default=None, help="Directory of trajectory JSONL files.")
def trajectory_ls(dir_path: str | None) -> None:
    """List trajectory files."""
    qs = f"?dir={dir_path}" if dir_path else ""
    data = _fetch(f"/api/trajectory/files{qs}")
    files = data.get("files", [])
    click.echo(f"dir: {data.get('dir')}")
    if not files:
        click.echo("(empty)")
        return
    for f in files:
        click.echo(f"  {f['name']:<48} {f['size_bytes']:>10} B")


@trajectory_group.command("tail")
@click.option("--file", "file_path", default=None, help="JSONL file path.")
@click.option("--limit", default=20, show_default=True)
@click.option("--json", "as_json", is_flag=True)
def trajectory_tail(file_path: str | None, limit: int, as_json: bool) -> None:
    """Tail the last N turns of a trajectory."""
    qs = f"?limit={limit}" + (f"&file={file_path}" if file_path else "")
    data = _fetch(f"/api/trajectory/tail{qs}")
    if as_json:
        click.echo(json.dumps(data, indent=2))
        return
    click.echo(f"file: {data.get('path')}")
    for t in data.get("turns", []):
        click.echo(
            f"  turn={t.get('turn')} model={t.get('provider')}:{t.get('model')} "
            f"p={t.get('prompt_tokens')} c={t.get('completion_tokens')} "
            f"tools={len(t.get('tool_calls') or [])}"
        )


@trajectory_group.command("summary")
@click.option("--file", "file_path", default=None)
def trajectory_summary(file_path: str | None) -> None:
    """Aggregate token totals + model usage."""
    qs = f"?file={file_path}" if file_path else ""
    data = _fetch(f"/api/trajectory/summary{qs}")
    click.echo(json.dumps(data, indent=2))
