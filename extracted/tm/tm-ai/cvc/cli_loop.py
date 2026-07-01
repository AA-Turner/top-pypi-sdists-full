"""``cvc loop`` CLI commands — inspect agentic loop state."""
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


@click.group("loop")
def loop_group() -> None:
    """Inspect the live agentic loop (budget, guardrails, compression)."""


@loop_group.command("state")
@click.option("--json", "as_json", is_flag=True, help="Emit raw JSON.")
def loop_state_cmd(as_json: bool) -> None:
    """Show current loop state."""
    snap = _fetch("/api/loop/state")
    if as_json:
        click.echo(json.dumps(snap, indent=2))
        return

    b = snap.get("budget", {})
    g = snap.get("guardrails", {})
    c = snap.get("compressor", {})
    r = snap.get("recorder", {})

    click.secho("Iteration budget", fg="cyan", bold=True)
    click.echo(
        f"  active={b.get('active')} used={b.get('used')}/{b.get('max')} "
        f"remaining={b.get('remaining')} exhausted={b.get('exhausted')}"
    )
    click.secho("Guardrails", fg="cyan", bold=True)
    click.echo(
        f"  active={g.get('active')} calls_this_turn={g.get('calls_this_turn')} "
        f"max_identical={g.get('max_identical_per_turn')} "
        f"max_total={g.get('max_total_per_turn')}"
    )
    click.secho("Compression", fg="cyan", bold=True)
    click.echo(
        f"  active={c.get('active')} trigger_tokens={c.get('trigger_tokens')} "
        f"keep_recent={c.get('keep_recent')}"
    )
    click.secho("Trajectory", fg="cyan", bold=True)
    click.echo(
        f"  active={r.get('active')} enabled={r.get('enabled')} path={r.get('path')}"
    )


@loop_group.command("config")
def loop_config_cmd() -> None:
    """Show default loop configuration."""
    cfg = _fetch("/api/loop/config")
    click.echo(json.dumps(cfg, indent=2))
