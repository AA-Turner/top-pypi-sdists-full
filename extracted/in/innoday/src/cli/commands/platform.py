"""Platform setup and initialization CLI commands."""

import argparse
from typing import Optional

import keyring
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from src.cli.client import InnoDayAPIClient
from src.cli.commands.services import ServiceCommands
from src.cli.config import CLIConfig
from src.cli.utils import compose
from src.cli.utils.formatters import (
    format_error,
    format_success,
    format_warning,
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

        # platform:init command
        init_parser = subparsers.add_parser(
            "init", help="Interactive platform setup wizard"
        )
        init_parser.add_argument(
            "--quick",
            action="store_true",
            help="Quick setup with minimal configuration",
        )
        init_parser.add_argument(
            # No default. A default here overrides the global --api-url, so
            # `innoday --api-url https://www.inno.day platform init` posted to
            # localhost -- the same shadowing bug as the --project one, in a
            # place where it silently targets the wrong deployment.
            "--api-url",
            default=argparse.SUPPRESS,
            help="API server URL (default: the configured api-url)",
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

        if args.platform_action == "init":
            return await commands.init_platform(args)
        elif args.platform_action == "start":
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
                "[dim]Available: init, health, start, stop, restart, logs, status — "
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

    async def init_platform(self, args: argparse.Namespace) -> int:
        """Interactive platform setup wizard"""
        self.console.print(
            Panel.fit(
                "[bold cyan]Welcome to InnoDay Platform Setup Wizard[/bold cyan]\n"
                "This wizard will help you configure your InnoDay platform with all necessary integrations.",
                title="🚀 Platform Setup",
                border_style="cyan",
            )
        )

        # Collect platform information
        self.console.print("\n[bold]Step 1: Platform Configuration[/bold]")
        platform_name = Prompt.ask("Platform name", default="InnoDay Platform")

        # Collect admin information
        self.console.print("\n[bold]Step 2: Administrator Account[/bold]")
        admin_email = Prompt.ask("Admin email")
        admin_name = Prompt.ask("Admin full name")

        # Collect integration tokens (optional in quick mode)
        integrations = {}

        if not args.quick:
            self.console.print("\n[bold]Step 3: Integration Configuration[/bold]")
            self.console.print("[yellow]Leave blank to skip any integration[/yellow]")

            # GitHub
            if Confirm.ask("\nConfigure GitHub integration?", default=True):
                github_token = Prompt.ask("GitHub personal access token", password=True)
                if github_token:
                    integrations["github_token"] = github_token
                    # Store in keyring
                    keyring.set_password(
                        self.keyring_service, "github_token", github_token
                    )
                    self.console.print(format_success("GitHub token stored securely"))

            # Jira
            if Confirm.ask("\nConfigure Jira integration?", default=False):
                jira_url = Prompt.ask("Jira URL (e.g., https://company.atlassian.net)")
                jira_email = Prompt.ask("Jira email")
                jira_token = Prompt.ask("Jira API token", password=True)
                if jira_token:
                    integrations["jira_url"] = jira_url
                    integrations["jira_email"] = jira_email
                    integrations["jira_token"] = jira_token
                    # Store in keyring
                    keyring.set_password(self.keyring_service, "jira_token", jira_token)
                    keyring.set_password(self.keyring_service, "jira_email", jira_email)
                    keyring.set_password(self.keyring_service, "jira_url", jira_url)
                    self.console.print(
                        format_success("Jira credentials stored securely")
                    )

            # Trello
            if Confirm.ask("\nConfigure Trello integration?", default=False):
                trello_api_key = Prompt.ask("Trello API key", password=True)
                trello_token = Prompt.ask("Trello token", password=True)
                if trello_api_key and trello_token:
                    integrations["trello_api_key"] = trello_api_key
                    integrations["trello_token"] = trello_token
                    # Store in keyring
                    keyring.set_password(
                        self.keyring_service, "trello_api_key", trello_api_key
                    )
                    keyring.set_password(
                        self.keyring_service, "trello_token", trello_token
                    )
                    self.console.print(
                        format_success("Trello credentials stored securely")
                    )

            # Claude AI
            if Confirm.ask("\nConfigure Claude AI integration?", default=True):
                claude_api_key = Prompt.ask("Claude API key", password=True)
                if claude_api_key:
                    integrations["claude_api_key"] = claude_api_key
                    # Store in keyring
                    keyring.set_password(
                        self.keyring_service, "claude_api_key", claude_api_key
                    )
                    self.console.print(format_success("Claude API key stored securely"))

            # Platform settings
            self.console.print("\n[bold]Step 4: Platform Settings (Optional)[/bold]")
            support_email = Prompt.ask("Support email", default=admin_email)
            billing_email = Prompt.ask("Billing email", default=admin_email)
            website = Prompt.ask("Website URL", default="")

            if support_email:
                integrations["support_email"] = support_email
            if billing_email:
                integrations["billing_email"] = billing_email
            if website:
                integrations["website"] = website

        # Call platform setup API
        self.console.print("\n[bold]Setting up platform...[/bold]")

        setup_data = {
            "platform_name": platform_name,
            "admin_email": admin_email,
            "admin_name": admin_name,
            **integrations,
        }

        try:
            async with InnoDayAPIClient(self.config) as client:
                client.base_url = args.api_url  # Use specified API URL

                response = await client.post("/platform/setup", json=setup_data)

                if response.status_code == 200:
                    result = response.json()

                    # Save configuration
                    self.config.set("platform.api_url", args.api_url)
                    self.config.set("user.id", result["admin_user_id"])
                    self.config.set("user.email", admin_email)
                    self.config.set("user.name", admin_name)
                    self.config.set("platform.organization_id", result["platform_id"])
                    self.config.save()

                    # Display success summary
                    self.console.print(
                        "\n" + format_success("✅ Platform setup complete!")
                    )

                    table = Table(
                        title="Platform Configuration Summary", show_header=False
                    )
                    table.add_column("Setting", style="cyan")
                    table.add_column("Value", style="green")

                    table.add_row("Platform Name", result["platform_name"])
                    table.add_row("Platform ID", result["platform_id"])
                    table.add_row("Admin User ID", result["admin_user_id"])
                    table.add_row(
                        "API Key",
                        (
                            result["api_key"][:8] + "..."
                            if len(result["api_key"]) > 8
                            else result["api_key"]
                        ),
                    )

                    # Show integration status
                    for integration, configured in result[
                        "integrations_configured"
                    ].items():
                        status = "✅ Configured" if configured else "❌ Not configured"
                        table.add_row(f"{integration.title()} Integration", status)

                    self.console.print(table)

                    # Next steps
                    self.console.print("\n[bold]Next Steps:[/bold]")
                    self.console.print(
                        "1. Start the API server: [cyan]innoday platform start[/cyan]"
                    )
                    self.console.print(
                        "2. Create an organization: [cyan]innoday orgs create[/cyan]"
                    )
                    self.console.print(
                        "3. Import repositories: [cyan]innoday repos sync-issues[/cyan]"
                    )
                    self.console.print(
                        "4. Check platform health: [cyan]innoday platform health[/cyan]"
                    )

                    return 0
                else:
                    error_detail = response.json().get("detail", "Unknown error")
                    self.console.print(format_error(f"Setup failed: {error_detail}"))
                    return 1

        except Exception as e:
            self.console.print(format_error(f"Failed to complete setup: {str(e)}"))
            self.console.print(
                format_warning("Make sure the API server is running at " + args.api_url)
            )
            return 1

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
