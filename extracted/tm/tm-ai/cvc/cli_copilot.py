"""CLI: `cvc copilot` — manage GitHub Copilot credentials in the pool.

Subcommands:
    cvc copilot login    Device-code OAuth flow → add token to pool
    cvc copilot status   Show pool stats + active credentials
    cvc copilot logout   Remove a credential (or all) from the pool
    cvc copilot add      Add a token directly (gho_/github_pat_/ghu_)
"""
from __future__ import annotations

import sys
import uuid

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group(name="copilot")
def copilot_group() -> None:
    """Manage GitHub Copilot credentials (multi-token pool with rotation)."""


@copilot_group.command("login")
def copilot_login() -> None:
    """Run GitHub OAuth device-code flow and add the token to the pool."""
    from cvc.auth.copilot_auth import (
        copilot_device_code_login,
        validate_copilot_token,
    )
    from cvc.agent.credential_pool import (
        get_pool,
        PooledCredential,
        AUTH_TYPE_OAUTH,
        SOURCE_DEVICE_CODE,
    )

    console.print("[bold cyan]Starting GitHub Copilot device-code login…[/bold cyan]")
    try:
        token = copilot_device_code_login()
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled.[/yellow]")
        sys.exit(1)
    except Exception as exc:
        console.print(f"[bold red]Login failed:[/bold red] {exc}")
        sys.exit(1)

    if not token:
        console.print("[bold red]No token received.[/bold red]")
        sys.exit(1)

    ok, msg = validate_copilot_token(token)
    if not ok:
        console.print(f"[bold red]Token rejected:[/bold red] {msg}")
        sys.exit(1)

    pool = get_pool()
    cred = pool.add(PooledCredential(
        provider="copilot",
        id=uuid.uuid4().hex[:8],
        label=f"oauth-{uuid.uuid4().hex[:4]}",
        auth_type=AUTH_TYPE_OAUTH,
        source=SOURCE_DEVICE_CODE,
        access_token=token,
    ))
    console.print(f"[bold green]✓ Added Copilot credential[/bold green] [dim]id={cred.id} label={cred.label}[/dim]")


@copilot_group.command("status")
def copilot_status() -> None:
    """Show pool stats and Copilot credentials."""
    from cvc.agent.credential_pool import get_pool

    pool = get_pool()
    stats = pool.stats()
    creds = pool.list("copilot")

    console.print(f"[bold]Pool:[/bold] strategy=[cyan]{stats['strategy']}[/cyan] store=[dim]{stats['store_path']}[/dim]")

    if not creds:
        console.print("[yellow]No Copilot credentials in pool.[/yellow]")
        console.print("[dim]Run [bold]cvc copilot login[/bold] or set COPILOT_GITHUB_TOKEN.[/dim]")
        return

    t = Table(title="Copilot credentials", show_header=True, header_style="bold cyan")
    t.add_column("ID")
    t.add_column("Label")
    t.add_column("Source")
    t.add_column("Status")
    t.add_column("Used")
    t.add_column("Token (prefix)")
    for c in creds:
        prefix = (c.access_token or "")[:10] + "…" if c.access_token else "—"
        t.add_row(c.id, c.label, c.source, c.status, str(c.usage_count), prefix)
    console.print(t)


@copilot_group.command("logout")
@click.option("--id", "cred_id", default=None, help="Credential ID to remove (omit + use --all to wipe).")
@click.option("--all", "remove_all", is_flag=True, help="Remove ALL Copilot credentials.")
def copilot_logout(cred_id: str | None, remove_all: bool) -> None:
    """Remove a credential (or all) from the pool."""
    from cvc.agent.credential_pool import get_pool

    pool = get_pool()
    if remove_all:
        creds = pool.list("copilot")
        for c in creds:
            pool.remove("copilot", c.id)
        console.print(f"[bold green]✓ Removed {len(creds)} Copilot credential(s).[/bold green]")
        return

    if not cred_id:
        console.print("[red]Specify --id <id> or --all.[/red]")
        sys.exit(1)

    if pool.remove("copilot", cred_id):
        console.print(f"[bold green]✓ Removed credential[/bold green] [dim]{cred_id}[/dim]")
    else:
        console.print(f"[red]No credential found with id={cred_id}[/red]")
        sys.exit(1)


@copilot_group.command("add")
@click.argument("token")
@click.option("--label", default=None, help="Friendly label.")
def copilot_add(token: str, label: str | None) -> None:
    """Add a GitHub Copilot token directly (gho_/github_pat_/ghu_)."""
    from cvc.auth.copilot_auth import validate_copilot_token
    from cvc.agent.credential_pool import (
        get_pool,
        PooledCredential,
        AUTH_TYPE_PAT,
        AUTH_TYPE_OAUTH,
        SOURCE_USER,
    )

    ok, msg = validate_copilot_token(token)
    if not ok:
        console.print(f"[bold red]Invalid token:[/bold red] {msg}")
        sys.exit(1)

    auth_type = AUTH_TYPE_PAT if token.startswith("github_pat_") else AUTH_TYPE_OAUTH
    cred = get_pool().add(PooledCredential(
        provider="copilot",
        id=uuid.uuid4().hex[:8],
        label=label or f"manual-{uuid.uuid4().hex[:4]}",
        auth_type=auth_type,
        source=SOURCE_USER,
        access_token=token,
    ))
    console.print(f"[bold green]✓ Added Copilot credential[/bold green] [dim]id={cred.id} label={cred.label}[/dim]")
