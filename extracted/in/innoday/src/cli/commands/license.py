"""
InnoDay CLI License Commands

Handles license management operations including viewing license info,
usage tracking, license upgrades, and license validation.
"""

import argparse
from typing import Optional

from rich.console import Console

from src.cli.config import CLIConfig
from src.cli.utils.formatters import format_error, format_warning

console = Console()


class LicenseCommands:
    """License management commands."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up license command parser."""
        subparsers = parser.add_subparsers(
            title="License Commands", dest="license_command", help="License operations"
        )

        # License info
        subparsers.add_parser(
            "info", help="Show current license information and usage summary"
        )

        # License usage
        usage_parser = subparsers.add_parser(
            "usage", help="Show usage metrics and limits"
        )
        usage_parser.add_argument(
            "--period",
            choices=["today", "week", "month"],
            default="month",
            help="Usage period to display (default: month)",
        )
        usage_parser.add_argument(
            "--detailed", action="store_true", help="Show detailed usage breakdown"
        )

        # License upgrade
        upgrade_parser = subparsers.add_parser(
            "upgrade", help="Upgrade license to a different tier"
        )
        upgrade_parser.add_argument(
            "tier",
            choices=["guidance", "spark", "sprint", "velocity"],
            help="Target license tier",
        )
        upgrade_parser.add_argument("--reason", help="Reason for the license change")
        upgrade_parser.add_argument(
            "--confirm", action="store_true", help="Skip confirmation prompt"
        )

        # License check
        check_parser = subparsers.add_parser(
            "check", help="Check if an action is allowed under current license"
        )
        check_parser.add_argument(
            "--action",
            choices=["create_ticket", "add_user", "add_board"],
            required=True,
            help="Action to validate",
        )

        # License history
        history_parser = subparsers.add_parser(
            "history", help="Show license change history"
        )
        history_parser.add_argument(
            "--limit",
            type=int,
            default=10,
            help="Number of history entries to show (default: 10)",
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute license command."""
        if not args.license_command:
            console.print(
                format_error(
                    "No license command specified. Available: info, usage, upgrade, "
                    "check, history — run 'innoday license --help' for details."
                )
            )
            return 1

        # Validate organization configuration
        organization = config.get_current_organization()
        if not organization:
            console.print(
                format_error(
                    "No organization configured. Run 'innoday config init' first."
                )
            )
            return 1

        try:
            if args.license_command == "info":
                return await LicenseCommands._show_license_info(organization, config)
            elif args.license_command == "usage":
                period_days = {"today": 1, "week": 7, "month": 30}[args.period]
                return await LicenseCommands._show_usage_metrics(
                    organization, config, period_days, args.detailed
                )
            elif args.license_command == "upgrade":
                user_id = config.get_user_id()
                if not user_id:
                    console.print(
                        format_error(
                            # `config set` takes {api-url,api-timeout,format,color,team-secret};
                            # there has never been a `user-id` key. Identity is
                            # created by the init wizard.
                            "No user configured. Run 'innoday init' first."
                        )
                    )
                    return 1
                return await LicenseCommands._upgrade_license(
                    organization, user_id, config, args.tier, args.reason, args.confirm
                )
            elif args.license_command == "check":
                user_id = config.get_user_id()
                return await LicenseCommands._check_license_action(
                    organization, user_id, config, args.action
                )
            elif args.license_command == "history":
                console.print(
                    format_warning("License history command not yet implemented.")
                )
                console.print("This feature will be available in a future release.")
                return 0
            else:
                console.print(
                    format_error(f"Unknown license command: {args.license_command}")
                )
                return 1

        except Exception as e:
            console.print(format_error(f"License command failed: {str(e)}"))
            return 1

    @staticmethod
    async def _show_license_info(organization: str, config: CLIConfig) -> int:
        """Show detailed license information"""
        console.print(format_warning("License info command not yet implemented."))
        console.print("This feature will be available in a future release.")
        return 0

    @staticmethod
    async def _show_usage_metrics(
        organization: str, config: CLIConfig, period_days: int, detailed: bool
    ) -> int:
        """Show usage metrics for the specified period"""
        console.print(format_warning("License usage command not yet implemented."))
        console.print("This feature will be available in a future release.")
        return 0

    @staticmethod
    async def _upgrade_license(
        organization: str,
        user_id: str,
        config: CLIConfig,
        tier: str,
        reason: Optional[str],
        confirm: bool,
    ) -> int:
        """Upgrade license to specified tier"""
        console.print(
            format_warning("License upgrade functionality not yet implemented.")
        )
        console.print("This feature will be available in a future release.")
        return 0

    @staticmethod
    async def _check_license_action(
        organization: str, user_id: Optional[str], config: CLIConfig, action: str
    ) -> int:
        """Check if a specific action is allowed under current license"""
        console.print(format_warning("License check command not yet implemented."))
        console.print("This feature will be available in a future release.")
        return 0
