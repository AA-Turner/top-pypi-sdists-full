"""Platform Administrator CLI commands."""

import argparse

from rich.console import Console

from src.cli.config import CLIConfig
from src.cli.utils.formatters import format_error, format_warning


class PlatformAdminCommands:
    """CLI commands for platform administrator management"""

    def __init__(self, config: CLIConfig):
        self.config = config
        self.console = Console()

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Add platform administrator command parser to the main parser"""
        subparsers = parser.add_subparsers(
            title="Platform Administrator Commands",
            dest="platform_admin_action",
            help="Platform administrator operations",
        )

        # platform-admin show command
        show_parser = subparsers.add_parser(
            "show", help="Show current platform administrator information"
        )
        show_parser.add_argument(
            "--public", action="store_true", help="Show only public information"
        )

        # platform-admin setup command
        setup_parser = subparsers.add_parser(
            "setup", help="Interactive setup of platform administrator information"
        )
        setup_parser.add_argument(
            "--quick", action="store_true", help="Quick setup with minimal questions"
        )

        # platform-admin update command
        update_parser = subparsers.add_parser(
            "update", help="Update specific platform administrator fields"
        )
        update_parser.add_argument("--company-name", help="Company name")
        update_parser.add_argument("--contact-email", help="Contact email")
        update_parser.add_argument("--contact-person", help="Contact person name")
        update_parser.add_argument("--phone", help="Phone number")
        update_parser.add_argument("--website", help="Website URL")
        update_parser.add_argument("--description", help="Service description")
        update_parser.add_argument("--business-hours", help="Business hours")
        update_parser.add_argument("--development-rate", help="Development rate info")
        update_parser.add_argument(
            "--offers-development",
            choices=["true", "false"],
            help="Whether development services are offered",
        )

        # platform-admin status command
        subparsers.add_parser(
            "status", help="Check platform administrator configuration status"
        )

        # platform-admin reset command
        reset_parser = subparsers.add_parser(
            "reset", help="Reset platform administrator to default values"
        )
        reset_parser.add_argument(
            "--confirm", action="store_true", help="Skip confirmation prompt"
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute platform administrator commands"""
        admin_commands = PlatformAdminCommands(config)
        try:
            return await admin_commands.handle_platform_admin_command(args)
        except Exception as e:
            console = Console()
            console.print(format_error(f"Platform admin command failed: {str(e)}"))
            return 1

    async def handle_platform_admin_command(self, args: argparse.Namespace) -> int:
        """Handle platform administrator commands"""
        try:
            if args.platform_admin_action == "show":
                await self.show_platform_admin_info(args)
            elif args.platform_admin_action == "setup":
                await self.setup_platform_admin(args)
            elif args.platform_admin_action == "update":
                await self.update_platform_admin(args)
            elif args.platform_admin_action == "status":
                await self.show_platform_admin_status()
            elif args.platform_admin_action == "reset":
                await self.reset_platform_admin(args)
            else:
                self.console.print(format_error("No platform-admin action specified"))
                self.console.print(
                    "[dim]Available: show, setup, update, status, reset — "
                    "run 'innoday platform-admin --help' for details[/dim]"
                )
                return 1
        except Exception as e:
            self.console.print(format_error(f"Platform admin command failed: {str(e)}"))
            return 1

        # Platform administrator commands are not yet backed by a real API --
        # every subcommand above is a stub, so this always exits non-zero.
        return 1

    async def show_platform_admin_info(self, args: argparse.Namespace) -> None:
        """Show platform administrator information"""
        self.console.print(
            format_warning("Platform administrator commands are not yet implemented.")
        )
        self.console.print("This feature will be available in a future release.")

    async def setup_platform_admin(self, args: argparse.Namespace) -> None:
        """Interactive setup of platform administrator information"""
        self.console.print(
            format_warning("Platform administrator setup is not yet implemented.")
        )
        self.console.print("This feature will be available in a future release.")

    async def update_platform_admin(self, args: argparse.Namespace) -> None:
        """Update specific platform administrator fields"""
        self.console.print(
            format_warning("Platform administrator update is not yet implemented.")
        )
        self.console.print("This feature will be available in a future release.")

    async def show_platform_admin_status(self) -> None:
        """Show platform administrator configuration status"""
        self.console.print(
            format_warning("Platform administrator status is not yet implemented.")
        )
        self.console.print("This feature will be available in a future release.")

    async def reset_platform_admin(self, args: argparse.Namespace) -> None:
        """Reset platform administrator to default values"""
        self.console.print(
            format_warning("Platform administrator reset is not yet implemented.")
        )
        self.console.print("This feature will be available in a future release.")
