"""Platform setup and initialization CLI commands."""

import argparse
from typing import Optional

from rich.console import Console
from rich.table import Table

from src.cli.client import InnoDayAPIClient
from src.cli.commands.services import ServiceCommands
from src.cli.config import CLIConfig
from src.cli.utils import compose
from src.cli.utils.formatters import (
    format_error,
    format_success,
)


class PlatformCommands:
    """CLI commands for platform setup and management"""

    def __init__(self, config: CLIConfig):
        self.config = config
        self.console = Console()
        self.keyring_service = "innoday-platform"

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Add platform command parser to the main parser"""
        subparsers = parser.add_subparsers(
            title="Platform Commands",
            dest="platform_action",
            help="Platform setup and management operations",
        )

        # platform:health command
        health_parser = subparsers.add_parser(
            "health", help="Check platform health and integrations"
        )
        health_parser.add_argument(
            "--detailed", action="store_true", help="Show detailed health information"
        )

        # platform:start command — persists config AND runs docker-compose up
        start_parser = subparsers.add_parser(
            "start", help="Start InnoDay via docker-compose (and persist config)"
        )
        start_parser.add_argument(
            "--env",
            choices=sorted(compose.VALID_ENVS),
            required=True,
            help="Environment to run (local, dev, or test — see README.md 'Configuration')",
        )

        # platform:stop command (docker-compose wrapper)
        subparsers.add_parser("stop", help="Stop InnoDay (docker-compose down)")

        # platform:restart command (docker-compose wrapper)
        subparsers.add_parser(
            "restart", help="Restart InnoDay (docker-compose restart)"
        )

        # platform:logs command (docker-compose wrapper)
        logs_parser = subparsers.add_parser(
            "logs", help="Tail InnoDay logs (docker-compose logs -f)"
        )
        logs_parser.add_argument(
            "--service", default=None, help="Specific service to tail (optional)"
        )

        # platform:status command — docker-compose doesn't expose a process-level
        # status view, so this still delegates to the process-based
        # ServiceCommands status check (ports/PIDs/health), same as pre-#220.
        status_parser = subparsers.add_parser(
            "status", help="Show running services, ports, and health"
        )
        ServiceCommands.setup_parser(status_parser)

    @staticmethod
    async def execute(
        args: argparse.Namespace, config: Optional[CLIConfig] = None
    ) -> int:
        """Execute platform commands"""
        if not config:
            config = CLIConfig()

        commands = PlatformCommands(config)

        if args.platform_action == "start":
            return await commands.start_platform(args)
        elif args.platform_action == "stop":
            return commands.compose_stop()
        elif args.platform_action == "restart":
            return commands.compose_restart()
        elif args.platform_action == "logs":
            return commands.compose_logs(getattr(args, "service", None))
        elif args.platform_action == "health":
            return await commands.check_health(args)
        elif args.platform_action == "status":
            # docker-compose has no process-level status view; delegate to the
            # process-based ServiceCommands status check (ports/PIDs/health).
            args.service_action = args.platform_action
            return await ServiceCommands.execute(args, config)
        else:
            commands.console.print(format_error("No platform action specified"))
            commands.console.print(
                "[dim]Available: health, start, stop, restart, logs, status — "
                "run 'innoday platform --help' for details[/dim]"
            )
            return 1

    async def start_platform(self, args: argparse.Namespace) -> int:
        """Run docker-compose up against the matching .env.<env> file.

        This used to write a `platform_server` block into
        ~/.innoday/config.json first (PF-127), on the plan that `platform
        start` would later read its environment and ports back out. PF-128
        shipped the compose wrapper below instead, which re-derives the env
        file from `args.env`, never passes the project name to docker, and
        takes its ports from `docker-compose.yml` -- so the block was written
        on every start and read by nothing, and three of its fields were
        written back as their own current values. #729 deleted the block; the
        compose call is unchanged.
        """
        env_file = f".env.{args.env}"

        self.console.print(
            format_success(
                f"Platform server configured for '{args.env}' (env file: {env_file})"
            )
        )

        # --- Step 2: bring up docker-compose (PF-128) ---
        return compose.run_compose("up", env=args.env, follow=False)

    def compose_stop(self) -> int:
        """Stop InnoDay via `docker compose down`."""
        return compose.run_compose("down")

    def compose_restart(self) -> int:
        """Restart InnoDay via `docker compose restart`."""
        return compose.run_compose("restart")

    def compose_logs(self, service: Optional[str]) -> int:
        """Tail InnoDay logs via `docker compose logs -f`."""
        return compose.run_compose("logs", follow=True, service=service)

    async def check_health(self, args: argparse.Namespace) -> int:
        """Check platform health and integrations"""
        try:
            async with InnoDayAPIClient(self.config) as client:
                response = await client.get("/platform/health")

                if response.status_code == 200:
                    health = response.json()

                    # Overall status
                    status_icon = "✅" if health["status"] == "healthy" else "⚠️"
                    self.console.print(
                        f"\n[bold]Platform Health: {status_icon} {health['status'].upper()}[/bold]"
                    )

                    # The checks come back only for a platform admin (PF-459);
                    # anyone else gets the status alone.
                    if "checks" not in health:
                        self.console.print(
                            "[dim]Platform checks are shown to platform admins only.[/dim]"
                        )
                        return 0 if health["status"] == "healthy" else 1

                    # Health checks table
                    table = Table(title="Health Checks")
                    table.add_column("Check", style="cyan")
                    table.add_column("Status", justify="center")

                    for check, passed in health["checks"].items():
                        status = "✅" if passed else "❌"
                        check_name = check.replace("_", " ").title()
                        table.add_row(check_name, status)

                    self.console.print(table)

                    if args.detailed and "integrations" in health:
                        # Detailed integration status
                        int_table = Table(title="Integration Health")
                        int_table.add_column("Integration", style="cyan")
                        int_table.add_column("Status", justify="center")
                        int_table.add_column("Details")

                        for integration, details in health["integrations"].items():
                            # Three-valued, like the server's: None means the
                            # integration was never contacted, which is neither
                            # a pass nor a failure. Rendering it as ❌ would
                            # report a working integration as broken.
                            healthy = details.get("healthy")
                            if healthy is None:
                                status = "[dim]—[/dim]"
                            else:
                                status = "✅" if healthy else "❌"
                            message = details.get("message", "")
                            int_table.add_row(integration.title(), status, message)

                        self.console.print(int_table)

                    return 0 if health["status"] == "healthy" else 1
                else:
                    self.console.print(format_error("Failed to check platform health"))
                    return 1

        except Exception as e:
            self.console.print(format_error(f"Error: {str(e)}"))
            return 1
