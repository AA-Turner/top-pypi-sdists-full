"""Manage named organization API keys stored in CLI config."""

from typing import Optional

import typer

from runlayer_cli.cli_persistence import save_config_or_exit
from runlayer_cli.config import (
    load_config,
    resolve_host,
)

app = typer.Typer(help="Manage stored organization API keys")


@app.callback(invoke_without_command=True)
def org_api_key_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command()
def add(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Name to reference this key by"),
    secret: str = typer.Option(
        ...,
        "--secret",
        "-s",
        prompt="Org API key",
        hide_input=True,
        help="The org API key value (rl_org_...)",
    ),
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        help="Host to store the key for (defaults to current host)",
    ),
) -> None:
    """Store a named org API key for the current host."""
    config = load_config()
    effective_host = resolve_host(ctx, host, config.default_host)
    try:
        config.set_org_api_key(effective_host, name, secret)
    except ValueError as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1) from None
    # Org keys live only in config.yaml; aiwatch runtime never writes it, so the
    # key would not be persisted (it only lived in the in-memory Config).
    save_config_or_exit(config, subject=f"org API key '{name}'", host=effective_host)
    typer.secho(
        f"Org API key '{name}' saved for {effective_host}.",
        fg=typer.colors.GREEN,
        err=True,
    )


@app.command()
def remove(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Name of the key to remove"),
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        help="Host to remove the key from (defaults to current host)",
    ),
) -> None:
    """Remove a stored org API key."""
    config = load_config()
    effective_host = resolve_host(ctx, host, config.default_host)
    if config.remove_org_api_key(effective_host, name):
        # Org keys live only in config.yaml; aiwatch runtime never writes it, so
        # the removal would not be persisted (it only mutated the in-memory
        # Config) — error instead of falsely reporting success.
        save_config_or_exit(
            config, subject=f"org API key '{name}' removal", host=effective_host
        )
        typer.secho(
            f"Org API key '{name}' removed for {effective_host}.",
            fg=typer.colors.GREEN,
            err=True,
        )
    else:
        typer.secho(
            f"No org API key '{name}' found for {effective_host}.",
            fg=typer.colors.YELLOW,
            err=True,
        )


@app.command(name="list")
def list_keys(
    ctx: typer.Context,
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        help="Host to list keys for (defaults to current host)",
    ),
) -> None:
    """List stored org API key names for the current host."""
    config = load_config()
    effective_host = resolve_host(ctx, host, config.default_host)
    keys = config.list_org_api_keys(effective_host)
    if not keys:
        typer.echo(f"No org API keys stored for {effective_host}.", err=True)
        return
    typer.echo(f"Org API keys for {effective_host}:", err=True)
    for name, prefix in keys.items():
        typer.echo(f"  {name}: {prefix}", err=True)
