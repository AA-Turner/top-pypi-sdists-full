"""``cvc team`` CLI commands."""
from __future__ import annotations

import json

import click


def _fetch(path: str, method: str = "GET"):
    import urllib.error
    import urllib.request

    base = "http://127.0.0.1:8765"
    req = urllib.request.Request(f"{base}{path}", method=method)
    try:
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise click.ClickException(f"Gateway unreachable at {base}: {exc}") from exc


@click.group("team")
def team_group() -> None:
    """The Core 4 — Sofia, Tina, Samantha, Robin."""


@team_group.command("list")
@click.option("--json", "as_json", is_flag=True)
def team_list(as_json: bool) -> None:
    data = _fetch("/api/team")
    if as_json:
        click.echo(json.dumps(data, indent=2))
        return
    for a in data.get("team", []):
        click.echo(
            f"  {a.get('agent_id'):<10} {a.get('name'):<10} "
            f"{a.get('role'):<14} {a.get('rank'):<10} {a.get('squad')}"
        )
    click.echo(f"Total: {data.get('total')}")


@team_group.command("ensure")
def team_ensure() -> None:
    """Idempotently register the canonical Core 4."""
    data = _fetch("/api/team/ensure", method="POST")
    click.echo(json.dumps(data, indent=2))
