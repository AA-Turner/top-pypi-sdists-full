"""Shared utilities for Plato CLI commands."""

import asyncio
import os
from pathlib import Path

import httpx
import typer
import yaml
from rich.console import Console

# Initialize Rich console - shared across all CLI modules
console = Console()

SANDBOX_FILE = ".sandbox.yaml"


def get_sandbox_state(working_dir: Path | str | None = None) -> dict | None:
    """Read sandbox state from .sandbox.yaml.

    Args:
        working_dir: Directory containing .sandbox.yaml. If None, uses cwd.
    """
    base_dir = Path(working_dir) if working_dir else Path.cwd()
    sandbox_file = base_dir / SANDBOX_FILE
    if not sandbox_file.exists():
        return None
    with open(sandbox_file) as f:
        return yaml.safe_load(f)


def save_sandbox_state(state: dict, working_dir: Path | str | None = None) -> None:
    """Save sandbox state to .sandbox.yaml.

    Args:
        state: State dict to save.
        working_dir: Directory to save .sandbox.yaml in. If None, uses cwd.
    """
    base_dir = Path(working_dir) if working_dir else Path.cwd()
    sandbox_file = base_dir / SANDBOX_FILE
    with open(sandbox_file, "w") as f:
        yaml.dump(state, f, default_flow_style=False)


def remove_sandbox_state(working_dir: Path | str | None = None) -> None:
    """Remove .sandbox.yaml.

    Args:
        working_dir: Directory containing .sandbox.yaml. If None, uses cwd.
    """
    base_dir = Path(working_dir) if working_dir else Path.cwd()
    sandbox_file = base_dir / SANDBOX_FILE
    if sandbox_file.exists():
        sandbox_file.unlink()


def require_sandbox_state(working_dir: Path | str | None = None) -> dict:
    """Get sandbox state or exit with error.

    Args:
        working_dir: Directory containing .sandbox.yaml. If None, uses cwd.
    """
    state = get_sandbox_state(working_dir)
    if not state:
        console.print("[red]No sandbox found in current directory[/red]")
        console.print("\n[yellow]Start a sandbox with:[/yellow]")
        console.print("  plato sandbox start --from-config")
        console.print("  plato sandbox start --simulator <name>")
        console.print("  plato sandbox start --artifact-id <id>")
        raise typer.Exit(1)
    return state


def require_sandbox_field(state: dict, field: str, hint: str | None = None) -> str:
    """Get a required field from sandbox state or exit with error."""
    value = state.get(field)
    if not value:
        console.print(f"[red]❌ No {field} found in .sandbox.yaml[/red]")
        if hint:
            console.print(f"\n[yellow]{hint}[/yellow]")
        raise typer.Exit(1)
    return value


def read_plato_config(config_path: str | Path) -> dict:
    """Read plato-config.yml file or exit with error."""
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]❌ Error reading plato-config.yml: {e}[/red]")
        raise typer.Exit(1) from e


def require_plato_config_field(config: dict, field: str) -> str:
    """Get a required field from plato config or exit with error."""
    value = config.get(field)
    if not value:
        console.print(f"[red]❌ No {field} in plato-config.yml[/red]")
        raise typer.Exit(1)
    return value


def require_api_key() -> str:
    """Get API key or exit with error."""
    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        console.print("[red]PLATO_API_KEY environment variable not set[/red]")
        console.print("\n[yellow]Set your API key:[/yellow]")
        console.print("  export PLATO_API_KEY='your-api-key-here'")
        raise typer.Exit(1)
    return api_key


def get_http_client() -> httpx.Client:
    """Get configured httpx client."""
    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so")
    # Strip trailing /api if present (to match v2 SDK behavior)
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    base_url = base_url.rstrip("/")
    return httpx.Client(base_url=base_url, timeout=httpx.Timeout(600.0))


def handle_async(coro):
    """Helper to run async functions with proper error handling."""
    try:
        return asyncio.run(coro)
    except KeyboardInterrupt:
        console.print("\n[red]🛑 Operation cancelled by user.[/red]")
        raise typer.Exit(1) from None
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        if "401" in str(e) or "Unauthorized" in str(e):
            console.print("💡 [yellow]Hint: Make sure PLATO_API_KEY is set in your environment[/yellow]")
        raise typer.Exit(1) from e
