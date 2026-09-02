"""
Developer init command for InnoDay CLI.

Assumes a running API server (started separately via `innoday platform start`
or `innoday platform init`). This wizard only sets up the developer's identity
and connects to that API — it never bootstraps the platform itself.
"""

import httpx
from rich.console import Console
from rich.prompt import Prompt

from src.cli.commands.config import ConfigCommands
from src.cli.config import DEFAULT_API_URL, CLIConfig, is_local_api_url
from src.cli.utils.banner import show_welcome_banner
from src.cli.utils.formatters import format_error, format_info, format_success

__all__ = ["DEFAULT_API_URL", "InitCommand"]


class InitCommand:
    """Developer setup wizard — identity and org selection only."""

    def __init__(self, config: CLIConfig = None):
        self.console = Console()
        self.config = config if config is not None else CLIConfig()

    async def execute(
        self,
        api_url: str = DEFAULT_API_URL,
        team_secret: str = None,
        default: bool = False,
    ):
        """Execute the developer init process."""
        try:
            self._show_welcome_banner()

            if not await self._api_reachable(api_url):
                self.console.print(
                    format_error(
                        f"Cannot reach InnoDay at {api_url}. Is the server running? "
                        "Try 'innoday platform start'."
                    )
                )
                return 1

            # Team secret precedence for a non-local target:
            #   1. An explicit --team-secret always wins (set + save below).
            #   2. Otherwise, if one is already stored, reuse it silently --
            #      re-running init must NOT make re-entry look mandatory.
            #   3. Only prompt on a true first-time setup (nothing stored, no
            #      flag). A local target never prompts and never requires one.
            if not is_local_api_url(api_url) and not team_secret:
                if self.config.get_team_secret():
                    self.console.print(
                        format_info("Reusing existing team access secret")
                    )
                else:
                    team_secret = Prompt.ask(
                        "Team access secret (required for the shared dev/deployed API)",
                        password=True,
                        default="",
                    )

            # An empty prompt/flag is a no-op -- it must never clear a stored
            # secret (the `if team_secret:` guard preserves that).
            if team_secret:
                self.config.set_team_secret(team_secret)
                self.config.save()
                self.console.print(format_success("Team access secret configured"))

            config_args = type(
                "Args",
                (),
                {"config_command": "init", "force": False, "no_banner": True},
            )()

            config_result = await ConfigCommands.execute(config_args, self.config)
            if config_result != 0:
                self.console.print(format_error("Configuration failed"))
                return 1

            if default:
                self.config.set_default_profile(self.config.get_current_profile())
                self.console.print(
                    format_success(
                        f"Profile '{self.config.get_current_profile()}' set as default"
                    )
                )

            return 0

        except KeyboardInterrupt:
            self.console.print("\n" + format_error("Init cancelled by user"))
            return 130
        except Exception as e:
            self.console.print(format_error(f"Init failed: {e}"))
            return 1

    def _show_welcome_banner(self):
        show_welcome_banner(self.console, "InnoDay Setup")

    async def _api_reachable(self, api_url: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{api_url.rstrip('/')}/health", timeout=5.0
                )
                return response.status_code == 200
        except Exception:
            return False


class InitCommands:
    """Init command integration for CLI."""

    @staticmethod
    def setup_parser(parser):
        parser.add_argument(
            "--api-url",
            default=DEFAULT_API_URL,
            help=f"API server URL (default: {DEFAULT_API_URL})",
        )
        parser.add_argument(
            "--team-secret",
            default=None,
            help="Team access secret for the shared dev/deployed API (sent as "
            "X-Team-Secret). Prompted for interactively if not passed and the "
            "target isn't local.",
        )
        parser.add_argument(
            "--default",
            action="store_true",
            help="Persist this profile as the default used when no --profile is "
            "given (including for non-interactive/MCP invocations).",
        )
        parser.set_defaults(func=InitCommands.execute)

    @staticmethod
    async def execute(args):
        cmd = InitCommand()
        return await cmd.execute(
            api_url=args.api_url,
            team_secret=args.team_secret,
            default=getattr(args, "default", False),
        )
