"""Verifier runner - discovers and runs Plato verifiers."""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(
    name="plato-verifier-runner",
    help="Run Plato verifiers against completed sessions",
    no_args_is_help=True,
)

logger = logging.getLogger(__name__)


@app.command()
def run(
    verifier: Annotated[str, typer.Option("--verifier", "-V", help="Verifier name to run")],
    config: Annotated[Path, typer.Option("--config", "-c", help="Path to config JSON file")],
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose logging")] = False,
) -> None:
    """Run a verifier against a session."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)

    if not config.exists():
        typer.echo(f"Error: Config file not found: {config}", err=True)
        raise typer.Exit(1)

    from .registry import discover_verifiers, get_registered_verifiers, get_verifier

    discover_verifiers()

    verifier_cls = get_verifier(verifier)
    if verifier_cls is None:
        available = list(get_registered_verifiers().keys())
        typer.echo(f"Error: Verifier '{verifier}' not found. Available: {available}", err=True)
        raise typer.Exit(1)

    with open(config) as f:
        config_json = json.load(f)

    config_class = verifier_cls.get_config_class()
    verifier_config = config_class.model_validate(config_json)

    instance = verifier_cls()

    try:
        result = asyncio.run(instance.run(verifier_config))
        typer.echo(f"Verifier completed: {result.signal.value} — {result.summary}")
    except KeyboardInterrupt:
        logger.info("Verifier interrupted")
    except Exception as e:
        logger.exception(f"Verifier execution failed: {e}")
        raise typer.Exit(1)


@app.command("list")
def list_verifiers(
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose logging")] = False,
) -> None:
    """List available verifiers."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    from .registry import discover_verifiers, get_registered_verifiers

    discover_verifiers()

    verifiers = get_registered_verifiers()
    if not verifiers:
        typer.echo("No verifiers found.")
        return

    typer.echo("Available verifiers:")
    for name, cls in verifiers.items():
        desc = getattr(cls, "description", "") or ""
        typer.echo(f"  {name}: {desc}")


def main() -> None:
    """CLI entry point."""
    app()


if __name__ == "__main__":
    main()
