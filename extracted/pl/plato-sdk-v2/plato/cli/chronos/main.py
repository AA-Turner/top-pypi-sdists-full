"""Plato Chronos CLI - Launch and manage Chronos jobs."""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
from typing import Annotated

import typer

from plato.chronos.sdk import Chronos
from plato.cli.chronos.settings import get_settings
from plato.cli.utils import console

chronos_app = typer.Typer(help="Chronos job management commands.")
logger = logging.getLogger(__name__)
settings = get_settings()


def _require_api_key(api_key: str | None) -> str:
    """Validate API key is provided, exit if not."""
    if not api_key:
        console.print("[red]No API key provided[/red]")
        console.print("Set PLATO_API_KEY environment variable or use --api-key")
        raise typer.Exit(1)
    return api_key


@chronos_app.command()
def launch(
    config: Path = typer.Argument(
        ...,
        help="Path to job config JSON file",
        exists=True,
        readable=True,
    ),
    prerelease: bool = typer.Option(
        False,
        "--prerelease",
        help="Allow prerelease versions (dev, alpha, beta, rc) for packages",
    ),
    chronos_url: str = typer.Option(
        None,
        "--url",
        "-u",
        envvar="CHRONOS_URL",
        help="Chronos API URL",
    ),
    api_key: str = typer.Option(
        None,
        "--api-key",
        "-k",
        envvar="PLATO_API_KEY",
        help="Plato API key for authentication",
    ),
):
    """Launch a Chronos job from a config file.

    Submits the job to Chronos API which:
    - Gets the base image from the world's schema.json
    - Installs the world package via uv at runtime
    - World code is NOT baked into the image

    Package format: "plato-world-name:version" (e.g., plato-world-structured-execution:0.1.0)

    """
    import json

    from pydantic import ValidationError

    from plato.chronos.models import LaunchJobRequest

    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    # Load config file (expand ${VAR} references from environment, same as dev mode)
    try:
        with open(config) as f:
            raw = json.loads(os.path.expandvars(f.read()))
    except Exception as e:
        console.print(f"[red]Invalid config file: {e}[/red]")
        raise typer.Exit(1)

    # Strip non-launch fields
    raw.pop("dev", None)
    raw.pop("session", None)

    # Auto-inject plato_api_key into world.config if not present
    world_cfg = raw.get("world", {})
    if "config" not in world_cfg:
        world_cfg["config"] = {}
    if "plato_api_key" not in world_cfg.get("config", {}):
        world_cfg["config"]["plato_api_key"] = api_key

    if prerelease:
        raw["allow_prerelease"] = True

    # Validate with Pydantic model
    try:
        request = LaunchJobRequest.model_validate(raw)
    except ValidationError as e:
        console.print(f"[red]Invalid config:[/red]\n{e}")
        raise typer.Exit(1)

    console.print("[blue]Launching job via Chronos API...[/blue]")
    console.print(f"   World: {request.world.package}")
    if prerelease:
        console.print("   Prerelease: enabled")

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            resp = client.launch(
                package=request.world.package,
                config=request.world.config,
                tags=request.tags,
                runtime=request.world.runtime.model_dump() if request.world.runtime else None,
                allow_prerelease=request.allow_prerelease or False,
            )

        console.print("\n[green]Job launched successfully![/green]")
        console.print(f"   Session ID: {resp.session_id}")
        console.print(f"   Status: {resp.status}")
        console.print(f"\n[dim]View at: {chronos_url}/sessions/{resp.session_id}[/dim]")

    except Exception as e:
        console.print(f"[red]Failed to launch job: {e}[/red]")
        raise typer.Exit(1)


@chronos_app.command()
def stop(
    session_id: Annotated[str, typer.Argument(help="Session ID to stop")],
    chronos_url: str = typer.Option(
        None,
        "--url",
        "-u",
        envvar="CHRONOS_URL",
        help="Chronos API URL",
    ),
    api_key: str = typer.Option(
        None,
        "--api-key",
        "-k",
        envvar="PLATO_API_KEY",
        help="Plato API key for authentication",
    ),
):
    """Stop a running Chronos session."""
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    console.print(f"[yellow]Stopping session {session_id}...[/yellow]")

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            client.stop(session_id)
        console.print(f"[green]Session {session_id} stopped[/green]")
    except Exception as e:
        console.print(f"[red]Failed to stop session: {e}[/red]")
        raise typer.Exit(1)


@chronos_app.command()
def dev(
    config: Annotated[
        Path,
        typer.Argument(help="Path to dev config JSON file", exists=True, readable=True),
    ],
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Show detailed logs"),
    ] = False,
):
    """Run world + agents on VMs with rsync hot reload."""
    from rich.logging import RichHandler

    from plato.cli.chronos.dev import Config, DevRunner

    # Configure logging with Rich handler for colored output
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False, show_time=verbose)],
    )
    # Always show dev runner and sync logs
    logging.getLogger("plato.cli.chronos.dev.runner").setLevel(logging.INFO)
    logging.getLogger("plato.cli.chronos.dev.sync").setLevel(logging.INFO)
    # Suppress noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    if not os.environ.get("PLATO_API_KEY"):
        console.print("[red]PLATO_API_KEY environment variable required[/red]")
        raise typer.Exit(1)

    try:
        dev_config = Config.from_file(config)
        runner = DevRunner(config=dev_config, config_path=config, verbose=verbose)
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        raise typer.Exit(0)
    except Exception as e:
        if verbose:
            console.print(f"[red]Failed: {e}[/red]")
            logger.exception("Dev mode failed")
        raise typer.Exit(1)
