"""World runner - discovers and runs Plato worlds."""

from __future__ import annotations

import asyncio
import json
import logging
import signal
from pathlib import Path
from typing import Annotated

import typer
from pydantic import TypeAdapter

from plato.runtime import RuntimeConfig, VMRuntimeConfig
from plato.worlds.config import DevConfig, RunConfig, SessionConfig

_RuntimeConfigAdapter = TypeAdapter(VMRuntimeConfig)

app = typer.Typer(
    name="plato-world-runner",
    help="Run Plato worlds",
    no_args_is_help=True,
)

logger = logging.getLogger(__name__)


def discover_worlds() -> None:
    """Discover and load installed world packages via entry points.

    World packages declare entry points in pyproject.toml:
        [project.entry-points."plato.worlds"]
        code = "code_world:CodeWorld"

    This function loads all such entry points, triggering registration.
    """
    from plato.utils.discovery import discover_plugins

    discover_plugins("plato.worlds", logger)


async def run_world(
    world_name: str,
    config: RunConfig,
    session: SessionConfig | None = None,
    dev: DevConfig | None = None,
    runtime: RuntimeConfig | None = None,
) -> None:
    """Run a world by name with the given configuration.

    Args:
        world_name: Name of the world to run
        config: World-specific configuration
        session: Session and telemetry configuration
        dev: Dev mode configuration
        runtime: Runtime configuration

    Raises:
        ValueError: If world not found
    """
    discover_worlds()

    from plato.worlds.base import get_registered_worlds, get_world

    world_cls = get_world(world_name)
    if world_cls is None:
        available = list(get_registered_worlds().keys())
        raise ValueError(f"World '{world_name}' not found. Available: {available}")

    world = world_cls()
    await world.run(config, session=session, dev=dev, runtime=runtime)


@app.command()
def run(
    world: Annotated[str, typer.Option("--world", "-w", help="World name to run")],
    config: Annotated[Path, typer.Option("--config", "-c", help="Path to config JSON file")],
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose logging")] = False,
) -> None:
    """Run a world with the given configuration."""
    # Setup logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    # Silence noisy httpx logs
    logging.getLogger("httpx").setLevel(logging.WARNING)

    if not config.exists():
        typer.echo(f"Error: Config file not found: {config}", err=True)
        raise typer.Exit(1)

    # Discover worlds first to get config class
    discover_worlds()

    from plato.worlds.base import get_registered_worlds, get_world

    world_cls = get_world(world)
    if world_cls is None:
        available = list(get_registered_worlds().keys())
        typer.echo(f"Error: World '{world}' not found. Available: {available}", err=True)
        raise typer.Exit(1)

    # Load full config JSON
    with open(config) as f:
        full_config = json.load(f)

    # Extract session, dev, runtime from their locations
    session = SessionConfig.model_validate(full_config.get("session", {}))
    dev = DevConfig.model_validate(full_config.get("dev", {}))

    # Runtime is at world.runtime
    world_block = full_config.get("world", {})
    runtime_data = world_block.get("runtime", {})
    runtime = _RuntimeConfigAdapter.validate_python(runtime_data) if runtime_data else VMRuntimeConfig()

    # Load world config using the world's typed config class (reads from world.config)
    config_class = world_cls.get_config_class()
    run_config = config_class.from_file(config)

    # Convert SIGTERM/SIGHUP to KeyboardInterrupt so asyncio.run() triggers
    # graceful shutdown (close() cleans up agents, tailscale, etc.)
    def _graceful_shutdown(signum: int, frame: object) -> None:
        sig_name = signal.Signals(signum).name
        logger.info(f"Received {sig_name}, shutting down gracefully...")
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, _graceful_shutdown)
    signal.signal(signal.SIGHUP, _graceful_shutdown)

    try:
        world_instance = world_cls()
        asyncio.run(world_instance.run(run_config, session=session, dev=dev, runtime=runtime))
    except KeyboardInterrupt:
        logger.info("World interrupted, cleanup complete")
    except Exception as e:
        logger.exception(f"World execution failed: {e}")
        raise typer.Exit(1)


@app.command("list")
def list_worlds(
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose logging")] = False,
) -> None:
    """List available worlds."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    discover_worlds()

    from plato.worlds.base import get_registered_worlds

    worlds = get_registered_worlds()
    if not worlds:
        typer.echo("No worlds found.")
        return

    typer.echo("Available worlds:")
    for name, cls in worlds.items():
        desc = getattr(cls, "description", "") or ""
        version = cls.get_version()
        typer.echo(f"  {name} (v{version}): {desc}")


def main() -> None:
    """CLI entry point."""
    app()


if __name__ == "__main__":
    main()
