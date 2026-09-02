"""Cache management commands for Runlayer CLI."""

import shutil

import typer

from runlayer_cli.oauth import default_cache_dir

app = typer.Typer(help="Manage Runlayer CLI OAuth client cache")


@app.callback(invoke_without_command=True)
def cache_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command(name="clear")
def clear():
    """Remove the OAuth client cache directory."""
    cache_dir = default_cache_dir()
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        typer.echo(f"Removed cache directory: {cache_dir}")
    else:
        typer.echo("Cache directory does not exist, nothing to clear.")
