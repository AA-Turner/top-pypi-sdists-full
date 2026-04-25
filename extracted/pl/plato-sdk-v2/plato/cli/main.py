"""Plato CLI - Main entry point."""

import os
import platform
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote

import typer
from dotenv import load_dotenv

from plato.cli.agent import agent_app
from plato.cli.chronos import chronos_app
from plato.cli.compose import app as compose_app
from plato.cli.db_tunnel import db_tunnel_app
from plato.cli.hillclimb import hillclimb_app
from plato.cli.pm import pm_app
from plato.cli.sandbox import sandbox_app
from plato.cli.segmentation import segmentation_app
from plato.cli.session import app as session_app
from plato.cli.utils import console, get_http_client, require_api_key
from plato.cli.world import world_app


def _find_bundled_cli() -> str | None:
    """
    Find the Plato Go CLI binary.

    Returns:
        Path to the CLI binary if found, None otherwise.
    """
    # Check locations in order of preference
    search_paths = []

    # 1. Bundled in package (plato-cli) - go up from cli/ to v1/
    binary_name = "plato-cli.exe" if platform.system().lower() == "windows" else "plato-cli"
    package_dir = Path(__file__).resolve().parent.parent  # v1/
    bin_dir = package_dir / "bin"
    search_paths.append(bin_dir / binary_name)

    # 2. plato-client/cli/bin/plato (development location)
    # Navigate from python-sdk/plato/cli/main.py to plato-client/cli/bin/plato
    plato_client_dir = package_dir.parent.parent  # Go up to plato-client
    go_binary_name = "plato.exe" if platform.system().lower() == "windows" else "plato"
    search_paths.append(plato_client_dir / "cli" / "bin" / go_binary_name)

    # 3. Check PATH for 'plato-cli' only (not 'plato' to avoid finding Python entry point)
    which_result = shutil.which(binary_name)
    if which_result:
        search_paths.append(Path(which_result))

    # Return first found executable that is NOT the Python entry point
    python_entry_point = shutil.which("plato")  # This is the Python CLI
    for path in search_paths:
        if path.exists() and os.access(path, os.X_OK):
            # Skip if this is the Python entry point (would cause infinite recursion)
            if python_entry_point and str(path.resolve()) == str(Path(python_entry_point).resolve()):
                continue
            return str(path)

    return None


# Load environment variables
load_dotenv()
load_dotenv(dotenv_path=os.path.join(os.path.expanduser("~"), ".env"))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


# =============================================================================
# MAIN APP
# =============================================================================


def _version_callback(value: bool) -> None:
    if value:
        from importlib.metadata import version

        console.print(version("plato-sdk-v2"))
        raise typer.Exit()


app = typer.Typer(help="[bold blue]Plato CLI[/bold blue] - Manage Plato environments and simulators.")


@app.callback()
def _app_callback(
    version: bool = typer.Option(
        False, "--version", "-V", help="Show version and exit.", callback=_version_callback, is_eager=True
    ),
) -> None:
    """Plato CLI - Manage Plato environments and simulators."""


# Register sub-apps
app.add_typer(db_tunnel_app, name="db-tunnel")
app.add_typer(sandbox_app, name="sandbox")
app.add_typer(session_app, name="session")
app.add_typer(compose_app, name="compose")
app.add_typer(pm_app, name="pm")
app.add_typer(agent_app, name="agent")
app.add_typer(world_app, name="world")
app.add_typer(chronos_app, name="chronos")
app.add_typer(hillclimb_app, name="hillclimb")
app.add_typer(segmentation_app, name="segmentation")


# =============================================================================
# TOP-LEVEL COMMANDS
# =============================================================================


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def hub(
    ctx: typer.Context,
):
    """Launch the Plato Hub CLI (interactive TUI for managing simulators).

    Opens the Go-based Plato CLI which provides an interactive terminal UI for
    browsing simulators, launching environments, and managing VMs. Any additional
    arguments are passed through to the Go CLI.

    Common subcommands: 'clone <service>', 'credentials', or no args for interactive mode.
    """
    # Find the bundled CLI binary
    plato_bin = _find_bundled_cli()

    if not plato_bin:
        console.print("[red]❌ Plato CLI binary not found in package[/red]")
        console.print("\n[yellow]The bundled CLI binary was not found in this installation.[/yellow]")
        console.print("This indicates an installation issue with the plato-sdk package.")
        console.print("\n[yellow]💡 Try reinstalling the package:[/yellow]")
        console.print("   pip install --upgrade --force-reinstall plato-sdk")
        console.print("\n[dim]If the issue persists, please report it at:[/dim]")
        console.print("[dim]https://github.com/plato-app/plato-client/issues[/dim]")
        raise typer.Exit(1)

    # Get any additional arguments passed after 'hub'
    args = ctx.args if hasattr(ctx, "args") else []

    try:
        # Launch the Go CLI, passing through all arguments
        # Use execvp to replace the current process so the TUI works properly
        os.execvp(plato_bin, [plato_bin] + args)
    except Exception as e:
        console.print(f"[red]❌ Failed to launch Plato Hub: {e}[/red]")
        raise typer.Exit(1) from e


@app.command()
def clone(
    service: str = typer.Argument(..., help="Service name to clone (e.g., espocrm)"),
    directory: str = typer.Argument(None, help="Target directory (defaults to service name)"),
):
    """Clone a service repository from Plato Hub (Gitea).

    Clones the simulator source code to your local machine for development or review.

    Arguments:
        service: Service name to clone (e.g., 'espocrm', 'gitea')
        directory: Target directory (defaults to service name)
    """
    from plato._generated.api.v1.gitea import (
        create_simulator_repository,
        get_accessible_simulators,
        get_gitea_credentials,
        get_simulator_repository,
    )

    api_key = require_api_key()
    client = get_http_client()

    # Get Gitea credentials
    try:
        creds = get_gitea_credentials.sync(client=client, x_api_key=api_key)
    except Exception as e:
        console.print(f"[red]Failed to get Gitea credentials: {e}[/red]")
        raise typer.Exit(1) from e

    # Find simulator
    try:
        simulators = get_accessible_simulators.sync(client=client, x_api_key=api_key)
    except Exception as e:
        console.print(f"[red]Failed to list simulators: {e}[/red]")
        raise typer.Exit(1) from e

    simulator = None
    for sim in simulators:
        sim_name = sim.get("name") if isinstance(sim, dict) else getattr(sim, "name", None)
        if sim_name and sim_name.lower() == service.lower():
            simulator = sim
            break

    if not simulator:
        console.print(f"[red]Simulator '{service}' not found[/red]")
        available = [(s.get("name") if isinstance(s, dict) else getattr(s, "name", "?")) for s in simulators]
        if available:
            console.print(f"[yellow]Available: {', '.join(sorted(available))}[/yellow]")
        raise typer.Exit(1)

    # Get or create repo
    sim_id = simulator.get("id") if isinstance(simulator, dict) else getattr(simulator, "id", None)
    has_repo = simulator.get("has_repo") if isinstance(simulator, dict) else getattr(simulator, "has_repo", False)

    if sim_id is None:
        console.print(f"[red]Simulator '{service}' has no ID[/red]")
        raise typer.Exit(1)

    try:
        if has_repo:
            repo = get_simulator_repository.sync(client=client, simulator_id=sim_id, x_api_key=api_key)
        else:
            repo = create_simulator_repository.sync(client=client, simulator_id=sim_id, x_api_key=api_key)
    except Exception as e:
        console.print(f"[red]Failed to get repository: {e}[/red]")
        raise typer.Exit(1) from e

    clone_url = repo.clone_url
    if not clone_url:
        console.print("[red]No clone URL available for repository[/red]")
        raise typer.Exit(1)

    # Build authenticated URL
    encoded_username = quote(creds.username, safe="")
    encoded_password = quote(creds.password, safe="")
    auth_clone_url = clone_url.replace("https://", f"https://{encoded_username}:{encoded_password}@", 1)

    # Clone locally
    target_dir = directory or service
    git_env = os.environ.copy()
    git_env["GIT_TERMINAL_PROMPT"] = "0"
    git_env["GIT_ASKPASS"] = ""

    console.print(f"Cloning [bold]{service}[/bold] into [bold]{target_dir}[/bold]...")
    result = subprocess.run(
        ["git", "clone", auth_clone_url, target_dir],
        env=git_env,
    )
    if result.returncode != 0:
        console.print(f"[red]Clone failed (exit {result.returncode})[/red]")
        raise typer.Exit(1)

    console.print(f"[green]Cloned {service} into {target_dir}[/green]")


@app.command()
def credentials():
    """Display your Plato Hub (Gitea) credentials.

    Shows the username and password needed to access Plato's Gitea repositories
    for cloning and pushing simulator code.
    """
    plato_bin = _find_bundled_cli()
    if not plato_bin:
        console.print("[red]❌ Plato CLI binary not found[/red]")
        console.print("[yellow]Cannot show credentials without the Go CLI binary.[/yellow]")
        raise typer.Exit(1)

    try:
        os.execvp(plato_bin, [plato_bin, "credentials"])
    except Exception as e:
        console.print(f"[red]❌ Failed to get credentials: {e}[/red]")
        raise typer.Exit(1) from e


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help="Explore simulation APIs (list, info, endpoints, spec)",
)
def sims(ctx: typer.Context):
    """Explore simulation APIs - list sims, view endpoints, get OpenAPI specs."""
    from plato.sims import cli as sims_cli

    # Pass all arguments to the sims CLI
    sims_cli.main(ctx.args)


# =============================================================================
# ENTRY POINT
# =============================================================================

# force bump to v36
# TEST/MOCK: This comment marks test-related code. Used for verification in release workflow.


def main():
    """Main entry point for the Plato CLI."""
    app()


# Backward compatibility
cli = main

if __name__ == "__main__":
    main()
