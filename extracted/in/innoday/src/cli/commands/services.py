"""
Service Management Commands

CLI commands for managing InnoDay services (start, stop, restart, status, logs).
Implements the unified service management interface requested in issue #24.
"""

import argparse
import asyncio
import json
import os
from typing import Dict

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from src.cli.config import CLIConfig
from src.config.schema import ServiceStatus
from src.services.manager import InnoServiceManager


class ServiceCommands:
    """Service management command handlers."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up service management command parsers."""
        # Determine which command we're setting up based on parser's prog name
        command_name = parser.prog.split()[-1] if " " in parser.prog else parser.prog

        if command_name in ["start", "stop", "restart"]:
            parser.add_argument(
                "services",
                nargs="*",
                choices=["api", "all"],
                default=["all"],
                help=f"Services to {command_name} (default: all)",
            )
        if command_name in ["start", "restart"]:
            parser.add_argument(
                "--environment",
                choices=["local", "dev", "development", "production"],
                help="Environment to pass to the service (sets ENVIRONMENT before spawning)",
            )
        elif command_name == "status":
            parser.add_argument(
                "--json", action="store_true", help="Output status as JSON"
            )
            parser.add_argument(
                "--watch", action="store_true", help="Continuously monitor status"
            )
        elif command_name == "logs":
            parser.add_argument(
                "service",
                choices=["api"],
                help="Service to view logs for",
            )
            parser.add_argument(
                "--lines",
                "-n",
                type=int,
                default=50,
                help="Number of lines to show (default: 50)",
            )
            parser.add_argument(
                "--follow",
                "-f",
                action="store_true",
                help="Follow log output (not implemented yet)",
            )

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute service management commands."""
        try:
            service_manager = InnoServiceManager()

            if args.service_action == "start":
                return await ServiceCommands._handle_start(args, service_manager)
            elif args.service_action == "stop":
                return await ServiceCommands._handle_stop(args, service_manager)
            elif args.service_action == "restart":
                return await ServiceCommands._handle_restart(args, service_manager)
            elif args.service_action == "status":
                return await ServiceCommands._handle_status(args, service_manager)
            elif args.service_action == "logs":
                return await ServiceCommands._handle_logs(args, service_manager)
            else:
                print("No service action specified")
                return 1

        except Exception as e:
            print(f"Error: {e}")
            return 1

    @staticmethod
    async def _handle_start(
        args: argparse.Namespace, manager: InnoServiceManager
    ) -> int:
        """Handle start command."""
        from src.cli.utils.banner import show_welcome_banner

        if getattr(args, "environment", None):
            os.environ["ENVIRONMENT"] = args.environment

        # Show welcome banner
        show_welcome_banner(title="InnoDay Services")

        services = args.services

        if "all" in services:
            success = await manager.start_all()
            return 0 if success else 1

        # Start specific services
        results = {}
        for service in services:
            results[service] = await manager.start_service(service)

        success_count = sum(results.values())
        if success_count == len(services):
            return 0
        else:
            print(
                f"Warning: {success_count}/{len(services)} services started successfully"
            )
            return 1

    @staticmethod
    async def _handle_stop(
        args: argparse.Namespace, manager: InnoServiceManager
    ) -> int:
        """Handle stop command."""
        services = args.services

        if "all" in services:
            success = await manager.stop_all()
            return 0 if success else 1

        # Stop specific services
        results = {}
        for service in services:
            results[service] = await manager.stop_service(service)

        success_count = sum(results.values())
        if success_count == len(services):
            return 0
        else:
            print(
                f"Warning: {success_count}/{len(services)} services stopped successfully"
            )
            return 1

    @staticmethod
    async def _handle_restart(
        args: argparse.Namespace, manager: InnoServiceManager
    ) -> int:
        """Handle restart command."""
        if getattr(args, "environment", None):
            os.environ["ENVIRONMENT"] = args.environment

        services = args.services

        if "all" in services:
            success = await manager.restart_all()
            return 0 if success else 1

        # Restart specific services
        results = {}
        for service in services:
            results[service] = await manager.restart_service(service)

        success_count = sum(results.values())
        if success_count == len(services):
            return 0
        else:
            print(
                f"Warning: {success_count}/{len(services)} services restarted successfully"
            )
            return 1

    @staticmethod
    async def _handle_status(
        args: argparse.Namespace, manager: InnoServiceManager
    ) -> int:
        """Handle status command."""
        if args.watch:
            return await ServiceCommands._handle_status_watch(manager)

        status = await manager.get_all_status()

        if args.json:
            # Output as JSON
            json_output = {name: svc.to_dict() for name, svc in status.items()}
            print(json.dumps(json_output, indent=2))
        else:
            # Output as formatted table
            ServiceCommands._display_status_table(status)

        return 0

    @staticmethod
    async def _handle_status_watch(manager: InnoServiceManager) -> int:
        """Handle status command with continuous monitoring."""
        console = Console()

        try:
            with Live(console=console, refresh_per_second=2) as live:
                while True:
                    status = await manager.get_all_status()
                    table = ServiceCommands._create_status_table(status)
                    panel = Panel(table, title="InnoDay Services Status", expand=False)
                    live.update(panel)
                    await asyncio.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[yellow]Status monitoring stopped[/yellow]")
            return 0

    @staticmethod
    def _display_status_table(status: Dict[str, ServiceStatus]) -> None:
        """Display service status as a formatted table."""
        console = Console()
        table = ServiceCommands._create_status_table(status)
        console.print(table)

    @staticmethod
    def _create_status_table(status: Dict[str, ServiceStatus]) -> Table:
        """Create a rich table for service status."""
        table = Table(title="InnoDay Services")

        table.add_column("Service", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("PID", justify="right")
        table.add_column("Port", justify="right")
        table.add_column("Uptime", justify="right")
        table.add_column("Memory", justify="right")
        table.add_column("CPU %", justify="right")

        for name, svc in status.items():
            # Color-code status
            if svc.running:
                status_text = f"[green]{svc.status_text}[/green]"
            elif svc.enabled:
                status_text = f"[red]{svc.status_text}[/red]"
            else:
                status_text = f"[dim]{svc.status_text}[/dim]"

            table.add_row(
                svc.display_name,
                status_text,
                str(svc.pid) if svc.pid else "-",
                str(svc.port) if svc.port else "-",
                svc.uptime_text,
                svc.memory_text,
                f"{svc.cpu_percent:.1f}" if svc.cpu_percent else "-",
            )

        return table

    @staticmethod
    async def _handle_logs(
        args: argparse.Namespace, manager: InnoServiceManager
    ) -> int:
        """Handle logs command."""
        service = args.service
        lines = args.lines
        follow = args.follow

        if follow:
            print("Follow mode not implemented yet")
            return 1

        logs = await manager.get_logs(service, lines)

        if logs is None:
            print(f"No logs available for service: {service}")
            return 1

        if not logs.strip():
            print(f"Log file is empty for service: {service}")
            return 0

        print(logs)
        return 0
