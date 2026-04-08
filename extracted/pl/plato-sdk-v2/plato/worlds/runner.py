"""World runner - discovers and runs Plato worlds."""

from __future__ import annotations

import asyncio
import importlib.metadata
import json
import logging
import signal
from pathlib import Path
from typing import Annotated

import typer

from plato.runtimes.base import RuntimeInfo
from plato.worlds.config import ChronosConfig, DevConfig, RunConfig

app = typer.Typer(
    name="plato-world-runner",
    help="Run Plato worlds",
    no_args_is_help=True,
)

logger = logging.getLogger(__name__)


def _report_crash_to_chronos(
    config_path: Path,
    error_message: str,
) -> None:
    """Best-effort report of a world crash to Chronos.

    Called when the world runner fails before BaseWorld.run() can report
    completion itself (e.g., import errors, world-not-found, startup crashes).
    Uses the Chronos SDK to properly mark the session as failed.
    """
    import os

    try:
        with open(config_path) as f:
            full_config = json.load(f)
        session_cfg = full_config.get("session", {})
        session_id = session_cfg.get("session_id")
        chronos_url = session_cfg.get("chronos_url")
        if not session_id or not chronos_url:
            return

        api_key = os.environ.get("PLATO_API_KEY", "")

        from plato.chronos.sdk import Chronos

        client = Chronos(base_url=chronos_url, api_key=api_key)
        client.complete(
            session_id=session_id,
            status="failed",
            error_message=error_message[:8000],
        )
        logger.info("Reported crash to Chronos for session %s", session_id)
    except Exception as e:
        logger.warning("Failed to report crash to Chronos: %s", e)


def discover_worlds() -> None:
    """Discover and load installed world packages via entry points.

    World packages declare entry points in pyproject.toml:
        [project.entry-points."plato.worlds"]
        code = "code_world:CodeWorld"

    This function loads all such entry points, triggering registration.
    """
    from plato.utils.discovery import discover_plugins

    discover_plugins("plato.worlds", logger)


def discover_world(world_name: str) -> None:
    """Discover and load a single installed world package by entry point."""
    from plato.worlds.base import get_world

    if get_world(world_name) is not None:
        return

    try:
        entry_points = importlib.metadata.entry_points(group="plato.worlds")
    except TypeError:
        entry_points = importlib.metadata.entry_points().get("plato.worlds", [])

    for entry_point in entry_points:
        if entry_point.name != world_name:
            continue
        try:
            entry_point.load()
            logger.debug("Loaded plugin: %s", entry_point.name)
        except Exception as exc:
            logger.warning("Failed to load plugin '%s': %s", entry_point.name, exc)
        return


async def run_world(
    world_name: str,
    config: RunConfig,
    chronos: ChronosConfig,
    dev: DevConfig | None = None,
    runtime_info: RuntimeInfo | None = None,
) -> None:
    """Run a world by name with the given configuration.

    Args:
        world_name: Name of the world to run
        config: World-specific configuration
        chronos: Chronos session and telemetry configuration
        dev: Dev mode configuration
        runtime_info: Runtime environment info (hostname, SSH key, etc.)

    Raises:
        ValueError: If world not found
    """
    discover_world(world_name)

    from plato.worlds.base import get_registered_worlds, get_world

    world_cls = get_world(world_name)
    if world_cls is None:
        available = list(get_registered_worlds().keys())
        raise ValueError(f"World '{world_name}' not found. Available: {available}")

    world = world_cls()
    await world.run(config, chronos=chronos, dev=dev, runtime_info=runtime_info)


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

    # Discover just the requested world entry point.
    discover_world(world)

    from plato.worlds.base import get_registered_worlds, get_world

    world_cls = get_world(world)
    if world_cls is None:
        available = list(get_registered_worlds().keys())
        error_msg = f"World '{world}' not found. Available: {available}"
        typer.echo(f"Error: {error_msg}", err=True)
        _report_crash_to_chronos(config, error_message=error_msg)
        raise typer.Exit(1)
    # Load full config JSON
    with open(config) as f:
        full_config = json.load(f)

    # Extract chronos, dev, runtime from their locations
    session_data = full_config.get("session", {})
    chronos = ChronosConfig.model_validate(session_data)
    dev = DevConfig.model_validate(full_config.get("dev", {}))

    # Runtime info is at world.runtime_info (optional, set by WorldLauncher)
    # or reconstructed from session.plato_session (set by Chronos backend)
    world_block = full_config.get("world", {})
    runtime_info_data = world_block.get("runtime_info")
    runtime_info = RuntimeInfo.model_validate(runtime_info_data) if runtime_info_data else None

    # Chronos backend passes plato_session in session config — bridge it to runtime_info
    # so the world can restore the Plato v2 session for agent VM management.
    plato_session_data = session_data.get("plato_session")
    if plato_session_data:
        if runtime_info is None:
            runtime_info = RuntimeInfo(
                runtime_id="runtime",
                hostname="localhost",
                serialized_session=plato_session_data,
            )
        elif runtime_info.serialized_session is None:
            runtime_info = runtime_info.model_copy(update={"serialized_session": plato_session_data})

    # Ensure the world VM has an SSH keypair for accessing agent VMs.
    # Generate one if missing — the public key gets registered with the Plato
    # session later when VMRuntime.start() calls env.add_ssh_key().
    if runtime_info is not None and runtime_info.ssh_key_path is None:
        from plato.utils.ssh import generate_ssh_key

        key_path = generate_ssh_key()
        runtime_info = runtime_info.model_copy(update={"ssh_key_path": key_path})

    # Load world config using the world's typed config class (reads from world.config)
    config_class = world_cls.get_config_class()
    run_config = config_class.from_file(config)

    # Convert SIGTERM/SIGHUP to KeyboardInterrupt so asyncio.run() triggers
    # graceful shutdown (close() cleans up agents, etc.)
    def _graceful_shutdown(signum: int, frame: object) -> None:
        sig_name = signal.Signals(signum).name
        logger.info(f"Received {sig_name}, shutting down gracefully...")
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, _graceful_shutdown)
    signal.signal(signal.SIGHUP, _graceful_shutdown)

    world_instance = world_cls()
    try:
        asyncio.run(world_instance.run(run_config, chronos=chronos, dev=dev, runtime_info=runtime_info))
    except KeyboardInterrupt:
        logger.info("World interrupted, cleanup complete")
    except Exception as e:
        logger.exception(f"World execution failed: {e}")
        if not getattr(world_instance, "_chronos_completed", False):
            import traceback

            _report_crash_to_chronos(
                config,
                error_message=f"{type(e).__name__}: {e}\n{traceback.format_exc()}",
            )
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
