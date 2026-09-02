"""
InnoDay CLI Scope Commands

Handles scope document operations including viewing and AI-driven ticket generation.
Follows the pattern established by projects.py and organizations.py.
"""

import argparse

from rich.console import Console
from rich.prompt import Confirm

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.config import CLIConfig
from src.cli.utils.formatters import (
    OutputFormatter,
    describe_error,
    format_error,
    format_info,
    format_success,
    format_warning,
)

console = Console()

# Deprecation notices go to stderr: this command's stdout is the result, and a
# flag that is on its way out should not change what a script parses.
_deprecations = Console(stderr=True)


class ScopeCommands:
    """Scope document and ticket generation commands."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up scope command parser."""
        subparsers = parser.add_subparsers(
            title="Scope Commands",
            dest="scope_command",
            help="Scope operations",
        )

        # scope show
        show_parser = subparsers.add_parser(
            "show",
            help="Show scope document",
            description="Display scope document details for a project",
        )
        show_parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            dest="project_id",
            help="Project ID (resolved from cwd's .innoday/project.yml when omitted)",
        )

        # scope generate
        generate_parser = subparsers.add_parser(
            "generate",
            help="Generate tickets from scope",
            description="Use AI to generate tickets on a board from scope document",
        )
        generate_parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            dest="project_id",
            help="Project ID (resolved from cwd's .innoday/project.yml when omitted)",
        )
        generate_parser.add_argument(
            "--scope-id", dest="scope_id", required=True, help="Scope document ID"
        )
        generate_parser.add_argument(
            "--board", required=True, help="Board registration ID"
        )
        # `--type` selects nothing any more. Its only purpose was choosing
        # which local credential to read for the X-Integration-Token header;
        # the server now resolves the target board's own credential from Vault
        # (#609). It is still *accepted* for one release, and ignored, because
        # it was `required=True` -- deleting it breaks every existing scripted
        # invocation of this command, not just the ones that chose the flag
        # deliberately. Accepting a no-op costs nothing; the deprecation
        # notice below (stderr) is what tells anyone still passing it.
        generate_parser.add_argument(
            "--type",
            help=argparse.SUPPRESS,
        )
        generate_parser.add_argument(
            "--no-epics",
            action="store_true",
            help="Don't create epic tickets",
        )
        generate_parser.add_argument(
            "--no-hierarchy",
            action="store_true",
            help="Don't link stories to epics",
        )
        generate_parser.add_argument(
            "--context",
            help="Additional context for AI (e.g., 'Focus on MVP features')",
        )
        generate_parser.add_argument(
            "--max-tickets",
            type=int,
            default=50,
            help="Maximum tickets to generate (default: 50)",
        )
        generate_parser.add_argument(
            "--confirm",
            action="store_true",
            help="Skip confirmation prompt",
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute scope command."""
        command = getattr(args, "scope_command", None)

        if command == "show":
            return await ScopeCommands._handle_show(args, config)
        elif command == "generate":
            return await ScopeCommands._handle_generate(args, config)
        else:
            console.print(format_error("No scope command specified"))
            console.print(
                format_info(
                    "Available: show, generate — use 'innoday scope --help' for details"
                )
            )
            return 1

    @staticmethod
    async def _handle_show(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle scope show command."""
        try:
            # Verify organization is set
            org_alias = config.get_current_organization()
            if not org_alias:
                console.print(format_error("No organization selected"))
                console.print(
                    format_info(
                        "Run this from a directory with .innoday/project.yml, or pass --organization <alias> explicitly"
                    )
                )
                return 1

            org_id = config.get_organization_id(org_alias)
            if not org_id:
                console.print(
                    format_error(f"Organization ID not found for '{org_alias}'")
                )
                return 1

            project_id = (
                getattr(args, "project_id", None) or config.get_current_project_id()
            )
            if not project_id:
                console.print(format_error("No project specified"))
                console.print(
                    format_info(
                        "Pass --project-id, or run this command from inside "
                        "a project directory (one with .innoday/project.yml)"
                    )
                )
                return 1

            api_client = InnoDayAPIClient(config)
            formatter = OutputFormatter(
                format_type=args.format, color_enabled=not args.no_color
            )

            # Fetch the project's current scope. There is no GET-by-scope-id
            # route (the API exposes only the current-scope GET here and a
            # PUT-by-id), so `show` always resolves the current scope.
            endpoint = f"/organizations/{org_id}/projects/{project_id}/scope"

            response = await api_client.get(endpoint)

            if response.status_code == 404:
                console.print(
                    format_warning(f"No scope found for project {project_id}")
                )
                return 0
            elif response.status_code != 200:
                console.print(
                    format_error(f"Failed to fetch scope: HTTP {response.status_code}")
                )
                return 1

            scope_data = response.json()

            if not scope_data:
                if formatter.format_type == "json":
                    formatter._print_json({})
                    return 0
                console.print(format_warning("No scope document found"))
                return 0

            # Display scope details
            if formatter.format_type == "json":
                formatter._print_json(scope_data)
            else:
                console.print("\n[bold]Scope Document[/bold]")
                console.print(f"ID: {scope_data.get('id', 'N/A')}")
                console.print(f"Version: {scope_data.get('version', 'N/A')}")
                console.print(f"Status: {scope_data.get('status', 'N/A')}")
                console.print(
                    f"Confidence: {scope_data.get('confidence_score', 'N/A')}"
                )
                console.print(
                    f"Estimated Hours: {scope_data.get('estimated_hours', 'N/A')}"
                )
                console.print("\n[bold]Refined Scope:[/bold]")
                console.print(scope_data.get("refined_scope", "N/A"))

                if scope_data.get("deliverables"):
                    console.print("\n[bold]Deliverables:[/bold]")
                    console.print(scope_data.get("deliverables"))

            await api_client.close()
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1

    @staticmethod
    async def _handle_generate(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle scope generate command."""
        try:
            # Verify organization is set
            org_alias = config.get_current_organization()
            if not org_alias:
                console.print(format_error("No organization selected"))
                console.print(
                    format_info(
                        "Run this from a directory with .innoday/project.yml, or pass --organization <alias> explicitly"
                    )
                )
                return 1

            org_id = config.get_organization_id(org_alias)
            if not org_id:
                console.print(
                    format_error(f"Organization ID not found for '{org_alias}'")
                )
                return 1

            project_id = (
                getattr(args, "project_id", None) or config.get_current_project_id()
            )
            if not project_id:
                console.print(format_error("No project specified"))
                console.print(
                    format_info(
                        "Pass --project-id, or run this command from inside "
                        "a project directory (one with .innoday/project.yml)"
                    )
                )
                return 1

            # Confirmation prompt
            if not args.confirm:
                console.print(
                    f"\n[yellow]This will generate tickets on board {args.board} from scope {args.scope_id}[/yellow]"
                )
                if not Confirm.ask("Continue?"):
                    console.print("Generation cancelled")
                    return 0

            # No credential is read from this machine and none is sent: the
            # generate endpoint resolves the target board's own credential
            # from Vault (#609).
            if getattr(args, "type", None):
                # stderr, so a script piping this command's stdout is not
                # handed a line of prose it has to parse around.
                _deprecations.print(
                    format_warning(
                        "--type is deprecated and ignored: the board's own "
                        "credential is resolved server-side from Vault. Drop "
                        "the flag; it will be removed in a future release."
                    )
                )

            api_client = InnoDayAPIClient(config)

            # Build request
            request_data = {
                "board_id": args.board,
                "create_epics": not args.no_epics,
                "create_hierarchy": not args.no_hierarchy,
                "max_tickets": args.max_tickets,
            }

            if args.context:
                request_data["additional_context"] = args.context

            console.print(format_info("Generating tickets with AI..."))

            # Call API
            endpoint = f"/organizations/{org_id}/projects/{project_id}/scope/{args.scope_id}/generate"
            response = await api_client.post(endpoint, json=request_data)

            if response.status_code == 400:
                error_detail = response.json().get("detail", "Unknown error")
                console.print(format_error(f"Generation failed: {error_detail}"))
                return 1
            elif response.status_code != 200:
                console.print(
                    format_error(
                        f"Failed to generate tickets: HTTP {response.status_code}"
                    )
                )
                return 1

            result = response.json()

            # Display results
            console.print(
                format_success(
                    f"✓ Generated {result.get('tickets_generated', 0)} tickets!"
                )
            )
            console.print(f"  Epics: {result.get('epics_created', 0)}")
            console.print(f"  Stories: {result.get('stories_created', 0)}")
            console.print(f"  Tasks: {result.get('tasks_created', 0)}")
            console.print(f"  Generation ID: {result.get('generation_id', 'N/A')}")
            console.print(f"  Board URL: {result.get('board_url', 'N/A')}")

            # Show epic hierarchy
            epic_tickets = result.get("epic_tickets", [])
            if epic_tickets:
                console.print("\n[bold]Epic Hierarchy:[/bold]")
                for epic in epic_tickets:
                    console.print(
                        f"  {epic.get('external_id')}: {epic.get('summary')} ({epic.get('child_count', 0)} stories)"
                    )

            await api_client.close()
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1
