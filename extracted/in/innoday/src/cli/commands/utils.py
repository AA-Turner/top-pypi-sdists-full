"""
InnoDay CLI Utility Commands

Handles utility operations like status, ping, version, etc.
"""

import argparse
import json
from typing import Any, Dict, Optional

from rich.console import Console
from rich.table import Table

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.utils.formatters import (
    OutputFormatter,
    ProgressReporter,
    format_error,
    format_success,
)
from src.version import get_display_version

console = Console()


class UtilityCommands:
    """Utility commands for system status and information."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser, command_name: str) -> None:
        if command_name == "ping":
            parser.add_argument("service", choices=["api"], help="Service to ping")

    @staticmethod
    async def execute(args: argparse.Namespace, config) -> int:
        command = args.command

        if command == "status":
            return await UtilityCommands._handle_status(args, config)
        elif command == "ping":
            return await UtilityCommands._handle_ping(args, config)
        elif command == "health":
            return await UtilityCommands._handle_health(args, config)
        elif command == "version":
            return await UtilityCommands._handle_version(args, config)
        else:
            console.print(format_error(f"Unknown utility command: {command}"))
            return 1

    @staticmethod
    async def _handle_status(args: argparse.Namespace, config) -> int:
        formatter = OutputFormatter(
            format_type=getattr(args, "format", None) or config.get_output_format(),
            color_enabled=config.is_color_enabled(),
        )

        status_data = {
            "api_url": config.get_api_url(),
            "organization": config.get_current_organization(),
        }

        async with InnoDayAPIClient(config) as client:
            try:
                with ProgressReporter("Checking API status..."):
                    await client.ping_api()
                status_data["api_status"] = "healthy"
            except APIError:
                status_data["api_status"] = "unreachable"

        formatter.format_status(status_data)
        return 0

    @staticmethod
    async def _handle_ping(args: argparse.Namespace, config) -> int:
        async with InnoDayAPIClient(config) as client:
            try:
                with ProgressReporter("Pinging API..."):
                    response = await client.ping_api()
                console.print(
                    format_success(f"API is reachable at {config.get_api_url()}")
                )

                if response.get("message"):
                    console.print(f"[dim]{response['message']}[/dim]")

                return 0

            except APIError as e:
                console.print(format_error(f"API is not reachable: {e}"))
                return 1

    @staticmethod
    async def _handle_health(args: argparse.Namespace, config) -> int:
        """Print what `GET /health` actually says.

        `ping` is not this command. It calls `GET /` (`ping_api`), whose
        `status` field is the string literal `"\u2705 Healthy"` -- it cannot
        report a problem. `/health` is the only route that runs `SELECT 1` and
        answers 503 when the database is gone, and until this command existed
        nothing in the CLI called it: `get_api_health()` had zero callers, and
        the three raw-httpx `/health` reads (config, session, init) each keep
        the boolean and discard `database`, `version` and `environment`.

        A 503 is a *verdict*, not a transport failure, so the unhealthy payload
        is printed rather than swallowed into an error string.
        """
        health: Dict[str, Any] = {}
        error: Optional[str] = None

        async with InnoDayAPIClient(config) as client:
            try:
                with ProgressReporter("Checking API health..."):
                    health = await client.get_api_health()
            except APIError as e:
                # 503 is the route's own verdict and carries the same body as
                # 200, so it is displayed rather than raised. Any other status
                # is a transport/auth failure and must not be rendered as a
                # health table full of "unknown".
                if e.status_code == 503 and isinstance(e.response_data, dict):
                    health = e.response_data
                else:
                    error = str(e)

        if error:
            console.print(format_error(f"API health check failed: {error}"))
            return 1

        if getattr(args, "format", None) == "json":
            print(json.dumps(health, indent=2))
            return 0 if health.get("status") == "healthy" else 1

        status = health.get("status", "unknown")
        database = health.get("database", "unknown")
        healthy = status == "healthy"

        console.print(
            f"\n[bold]InnoDay API Health:[/bold] "
            f"{'[green]HEALTHY[/green]' if healthy else f'[red]{status.upper()}[/red]'}"
        )

        table = Table(show_header=True, header_style="bold")
        table.add_column("Check")
        table.add_column("Value")
        table.add_row("URL", config.get_api_url())
        table.add_row(
            "Database",
            f"[green]{database}[/green]"
            if database == "connected"
            else f"[red]{database}[/red]",
        )
        for label, key in (
            ("Version", "version"),
            ("Environment", "environment"),
            ("Port", "port"),
        ):
            value = health.get(key)
            table.add_row(label, str(value) if value is not None else "[dim]-[/dim]")
        console.print(table)

        return 0 if healthy else 1

    @staticmethod
    async def _handle_version(args: argparse.Namespace, config) -> int:
        version = get_display_version()

        console.print(f"[bold blue]InnoDay CLI[/bold blue] {version}")
        console.print()
        console.print("[dim]Configuration:[/dim]")
        console.print(f"  Config file: {config.config_path}")
        console.print(f"  API URL: {config.get_api_url()}")

        current_org = config.get_current_organization()
        if current_org:
            console.print(f"  Organization: {current_org}")
        else:
            console.print("  Organization: [red]Not configured[/red]")

        console.print()
        console.print("[dim]Service Status:[/dim]")

        async with InnoDayAPIClient(config) as client:
            try:
                await client.ping_api()
                console.print("  API: [green]✓ Online[/green]")
            except APIError:
                console.print("  API: [red]✗ Offline[/red]")

        return 0
