"""
InnoDay CLI Project Commands

Handles project management operations including listing, creating, updating, and viewing details.
"""

import argparse
import json
from typing import Any, Dict, List

from rich.console import Console
from rich.prompt import Confirm, Prompt

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.config import CLIConfig
from src.cli.utils.formatters import (
    OutputFormatter,
    ProgressReporter,
    describe_error,
    format_error,
    format_info,
    format_success,
    format_warning,
)
from src.cli.utils.health_table import health_table
from src.domain.project import ProjectPriority, ProjectStatus

console = Console()

# Choices are derived from the enums so they cannot drift from what the API
# accepts. Every value of both flags previously returned HTTP 422 -- the
# `--status` and `--priority` filters were entirely non-functional:
#
#   innoday projects list --status ACTIVE     -> 422
#   innoday projects list --priority MEDIUM   -> 422
#
# Two independent causes, both fixed here:
#   * case -- the hardcoded lists were UPPERCASE, but `GET /projects` validates
#     against `Optional[ProjectStatus]` / `Optional[ProjectPriority]`, i.e. the
#     enums' lowercase *values*;
#   * values that do not exist -- `ON_HOLD` and `COMPLETED` are absent from
#     ProjectStatus (PLANNING/ACTIVE/ARCHIVED), and `CRITICAL` from
#     ProjectPriority (HIGH/MEDIUM/LOW). argparse accepted them, then the server
#     rejected them, so the error surfaced as far as possible from the cause.
#
# (`innoday tickets list --status IN_PROGRESS` works only because that router
# takes a plain `Optional[str]` and compares it to the stored enum *name*. The
# two routers genuinely disagree about case; the CLI must send what each accepts.)
PROJECT_STATUS_CHOICES = [status.value for status in ProjectStatus]
PROJECT_PRIORITY_CHOICES = [priority.value for priority in ProjectPriority]


def _enum_arg(enum_cls, choices: List[str], label: str):
    """An argparse ``type=`` that maps either casing onto the enum's own value.

    Accepting UPPERCASE matters for compatibility: it is the form the CLI
    advertised the whole time this was broken, and the form the database shows
    (the column stores enum *names*), so it is what anyone would type.
    """

    def convert(value: str) -> str:
        try:
            return enum_cls(value.strip().lower()).value
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"invalid {label} {value!r} (choose from {', '.join(choices)})"
            ) from None

    return convert


project_status = _enum_arg(ProjectStatus, PROJECT_STATUS_CHOICES, "project status")
project_priority = _enum_arg(
    ProjectPriority, PROJECT_PRIORITY_CHOICES, "project priority"
)


def _server_ignored(requested, actual) -> bool:
    """Whether the server disregarded this field, as opposed to normalising it.

    **Normalising is not ignoring, and warning about both is worse than warning
    about neither.** The first version of this compared the two exactly, so
    renaming a project to `blast` -- stored uppercase, like every alias, because
    it doubles as a ticket prefix -- reported:

        alias: BLAST
        ⚠ asked for alias='blast', server has 'BLAST'

    Nothing was wrong. A warning that fires on every tidied value is one people
    learn to scroll past, and the real case -- a field silently dropped, the row
    unchanged, `200` returned -- scrolls past with it.

    Case and surrounding whitespace are the normalisations this API performs. A
    genuinely disregarded field still differs after both are removed: `BLASTOFF`
    is not a tidier `blast`.
    """
    if actual == requested:
        return False
    if isinstance(requested, str) and isinstance(actual, str):
        return requested.strip().casefold() != actual.strip().casefold()
    return True


class ProjectCommands:
    """Project management commands."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up project command parser."""
        subparsers = parser.add_subparsers(
            title="Project Commands",
            dest="project_command",
            help="Project operations",
        )

        # Projects list
        list_parser = subparsers.add_parser(
            "list",
            help="List projects",
            description="List all projects in the current organization",
        )
        list_parser.add_argument(
            "--status",
            choices=PROJECT_STATUS_CHOICES,
            type=project_status,
            help="Filter by status",
        )
        list_parser.add_argument(
            "--priority",
            choices=PROJECT_PRIORITY_CHOICES,
            type=project_priority,
            help="Filter by priority",
        )
        list_parser.add_argument("--tags", help="Filter by tags (comma-separated)")
        list_parser.add_argument(
            "--all",
            action="store_true",
            help="Include archived projects (hidden by default)",
        )

        # Projects show
        show_parser = subparsers.add_parser(
            "show",
            help="Show project details",
            description="Display detailed information about a project",
        )
        show_parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            dest="project_id",
            help="Project ID or alias (resolved from cwd's .innoday/project.yml when omitted)",
        )
        show_parser.add_argument(
            "--overview",
            action="store_true",
            help="Show full overview with repositories and issues",
        )

        # Projects health
        health_parser = subparsers.add_parser(
            "health",
            help="Is this project working — database, boards, credentials",
            description=(
                "One call for the database, every board registered to this "
                "project, and how long ago each really synced. Add --probe to "
                "contact the boards themselves."
            ),
        )
        health_parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            dest="project_id",
            help="Project ID or alias (resolved from cwd's .innoday/project.yml when omitted)",
        )
        health_parser.add_argument(
            "--no-probe",
            action="store_true",
            dest="no_probe",
            help=(
                "Skip contacting the boards. Without this, every active board is "
                "asked — a health check that never leaves the database cannot "
                "answer the question."
            ),
        )

        # Projects create
        create_parser = subparsers.add_parser(
            "create",
            help="Create new project",
            description="Create a new project in the current organization",
        )
        create_parser.add_argument("name", help="Project name")
        create_parser.add_argument(
            "--alias",
            required=True,
            help="Short uppercase ticket prefix, e.g. PF, HS (unique within the org)",
        )
        create_parser.add_argument("--description", help="Project description")
        create_parser.add_argument("--goals", help="Project goals (markdown)")
        create_parser.add_argument("--scope-limitations", help="What's out of scope")
        create_parser.add_argument(
            "--priority",
            choices=PROJECT_PRIORITY_CHOICES,
            type=project_priority,
            default=ProjectPriority.MEDIUM.value,
            help="Project priority (default: medium)",
        )
        create_parser.add_argument(
            "--status",
            choices=PROJECT_STATUS_CHOICES,
            type=project_status,
            default=ProjectStatus.PLANNING.value,
            help="Initial status (default: planning)",
        )
        create_parser.add_argument("--tags", help="Tags (comma-separated)")
        create_parser.add_argument(
            "--interactive",
            "-i",
            action="store_true",
            help="Interactive mode (prompts for all fields)",
        )

        # Projects update
        update_parser = subparsers.add_parser(
            "update",
            help="Update project",
            description="Update an existing project's metadata",
        )
        update_parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            dest="project_id",
            help="Project ID or alias (resolved from cwd's .innoday/project.yml when omitted)",
        )
        update_parser.add_argument("--name", help="New project name")
        update_parser.add_argument(
            "--alias",
            help="New alias. This is the project's ticket prefix AND its GitHub "
            "discovery topic, so renaming changes which repositories are found — "
            "add the new topic to them first.",
        )
        update_parser.add_argument("--description", help="New description")
        update_parser.add_argument("--goals", help="New goals")
        update_parser.add_argument("--scope-limitations", help="New scope limitations")
        update_parser.add_argument(
            "--priority",
            choices=PROJECT_PRIORITY_CHOICES,
            type=project_priority,
            help="New priority",
        )
        update_parser.add_argument(
            "--status",
            choices=PROJECT_STATUS_CHOICES,
            type=project_status,
            help="New status",
        )
        update_parser.add_argument("--tags", help="New tags (comma-separated)")

        # Projects delete -- archives; kept as the command name for
        # compatibility, but every string it prints says "archive".
        delete_parser = subparsers.add_parser(
            "delete",
            help="Archive project (soft; alias stays taken)",
            description=(
                "Archive a project. The project is not removed -- it is set to "
                "status 'archived', keeps its alias, and can be reactivated "
                "with 'projects update --status active'."
            ),
        )
        delete_parser.add_argument(
            # Not required: the cwd is a legitimate way to say which project,
            # and this was the one command that refused it -- archiving being
            # exactly where a person is most likely to be standing in the thing
            # they mean. The confirmation prompt is what guards the action.
            "--project-id",
            default=argparse.SUPPRESS,
            dest="project_id",
            help="Project ID or alias",
        )
        delete_parser.add_argument(
            "--confirm",
            action="store_true",
            help="Skip confirmation prompt",
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute project command."""
        command = getattr(args, "project_command", None)

        if command == "list":
            return await ProjectCommands._handle_list(args, config)
        elif command == "show":
            return await ProjectCommands._handle_show(args, config)
        elif command == "health":
            return await ProjectCommands._handle_health(args, config)
        elif command == "create":
            return await ProjectCommands._handle_create(args, config)
        elif command == "update":
            return await ProjectCommands._handle_update(args, config)
        elif command == "delete":
            return await ProjectCommands._handle_delete(args, config)
        else:
            console.print(format_error("No project command specified"))
            console.print(
                format_info(
                    "Available: list, show, health, create, update, delete — "
                    "use 'innoday projects --help' for details"
                )
            )
            return 1

    @staticmethod
    async def _handle_list(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle projects list command."""
        try:
            # Verify organization is set
            org_alias = config.get_current_organization()
            if not org_alias:
                console.print(format_error("No organization selected"))
                console.print(
                    format_info(
                        "Run this from a directory with .innoday/project.yml, "
                        "or pass --organization <alias> explicitly"
                    )
                )
                return 1

            org_id = config.get_organization_id(org_alias)
            if not org_id:
                console.print(
                    format_error(f"Organization ID not found for '{org_alias}'")
                )
                return 1

            api_client = InnoDayAPIClient(config)
            formatter = OutputFormatter(
                format_type=args.format, color_enabled=not args.no_color
            )

            # Build query parameters
            params = {}
            if args.status:
                params["status"] = args.status
            if args.priority:
                params["priority"] = args.priority
            if args.tags:
                params["tags"] = args.tags

            # Fetch projects
            response = await api_client.get(
                f"/organizations/{org_id}/projects", params=params
            )

            if response.status_code != 200:
                console.print(
                    format_error(
                        f"Failed to fetch projects: HTTP {response.status_code}"
                    )
                )
                return 1

            projects = response.json()

            # Hide archived projects unless asked for. `projects delete`
            # archives rather than deletes, so without this the project the
            # operator just archived stays in the list and the command reads
            # as having silently failed. Filtered client-side so the API's
            # default stays unchanged for other consumers.
            archived_hidden = 0
            if not args.all and not args.status:
                live = [
                    p
                    for p in projects
                    if str(p.get("status", "")).lower() != ProjectStatus.ARCHIVED.value
                ]
                archived_hidden = len(projects) - len(live)
                projects = live

            if not projects:
                if archived_hidden:
                    console.print(
                        format_warning(
                            f"No active projects ({archived_hidden} archived "
                            "-- pass --all to include them)"
                        )
                    )
                else:
                    console.print(format_warning("No projects found"))
                return 0

            # Format and display
            formatter.format_projects(projects)

            if archived_hidden:
                console.print(
                    format_info(
                        f"{archived_hidden} archived project"
                        f"{'s' if archived_hidden != 1 else ''} hidden "
                        "-- pass --all to include them"
                    )
                )

            await api_client.close()
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1

    @staticmethod
    async def _handle_show(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle projects show command."""
        try:
            # Verify organization is set
            org_alias = config.get_current_organization()
            if not org_alias:
                console.print(format_error("No organization selected"))
                console.print(
                    format_info(
                        "Run this from a directory with .innoday/project.yml, "
                        "or pass --organization <alias> explicitly"
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

            # Determine endpoint based on overview flag
            if args.overview:
                endpoint = f"/organizations/{org_id}/projects/{project_id}/overview"
            else:
                endpoint = f"/organizations/{org_id}/projects/{project_id}"

            response = await api_client.get(endpoint)

            if response.status_code == 404:
                console.print(format_error(f"Project '{project_id}' not found"))
                return 1
            elif response.status_code != 200:
                console.print(
                    format_error(
                        f"Failed to fetch project: HTTP {response.status_code}"
                    )
                )
                return 1

            project_data = response.json()

            # Format and display
            formatter = OutputFormatter(
                format_type=args.format, color_enabled=not args.no_color
            )
            formatter.format_project_details(
                project_data, include_overview=args.overview
            )

            await api_client.close()
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1

    @staticmethod
    async def _handle_health(args: argparse.Namespace, config: CLIConfig) -> int:
        """Print the project's composite health.

        `reachable` is three-valued and rendered as such: a dash means the board
        was never contacted (no --probe, inactive, or no credential stored), not
        that it failed. A cross is the board actually saying no.
        """
        try:
            org_alias = config.get_current_organization()
            if not org_alias:
                console.print(format_error("No organization selected"))
                console.print(
                    format_info(
                        "Run this from a directory with .innoday/project.yml, "
                        "or pass --organization <alias> explicitly"
                    )
                )
                return 1

            org_id = config.get_organization_id(org_alias) or org_alias
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
            probe = not getattr(args, "no_probe", False)
            endpoint = f"/organizations/{org_id}/projects/{project_id}/health"
            if not probe:
                endpoint += "?probe=false"

            with ProgressReporter(
                "Probing boards..." if probe else "Checking project health..."
            ):
                response = await api_client.get(endpoint)

            if response.status_code == 404:
                console.print(format_error(f"Project '{project_id}' not found"))
                return 1
            if response.status_code == 403:
                console.print(
                    format_error("Forbidden — this needs the DEVELOPER role or above")
                )
                return 1
            if response.status_code != 200:
                console.print(
                    format_error(
                        f"Failed to get project health: {response.status_code}"
                    )
                )
                return 1

            health = response.json()

            if getattr(args, "format", None) == "json":
                print(json.dumps(health, indent=2))
                return 0 if health.get("status") == "healthy" else 1

            status = health.get("status", "unknown")
            colour = {"healthy": "green", "degraded": "yellow"}.get(status, "red")
            console.print(
                f"\n[bold]Project {health.get('project_alias', project_id)}:[/bold] "
                f"[{colour}]{status.upper()}[/{colour}]"
            )

            console.print(health_table(health))

            if not (health.get("boards") or []):
                console.print("[yellow]No boards registered for this project[/yellow]")
            if not probe:
                console.print(
                    "[dim]Boards not contacted (--no-probe). Reachability is "
                    "unknown, not healthy.[/dim]"
                )

            return 0 if status == "healthy" else 1

        except Exception as e:
            console.print(format_error(f"Failed to get project health: {e}"))
            return 1

    @staticmethod
    async def _handle_create(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle projects create command."""
        try:
            # Verify organization is set
            org_alias = config.get_current_organization()
            if not org_alias:
                console.print(format_error("No organization selected"))
                console.print(
                    format_info(
                        "Run this from a directory with .innoday/project.yml, "
                        "or pass --organization <alias> explicitly"
                    )
                )
                return 1

            org_id = config.get_organization_id(org_alias)
            if not org_id:
                console.print(
                    format_error(f"Organization ID not found for '{org_alias}'")
                )
                return 1

            # Gather project data
            if args.interactive:
                project_data = await ProjectCommands._gather_project_data_interactive()
            else:
                project_data = {
                    "name": args.name,
                    "alias": args.alias.upper(),
                    "description": args.description or "",
                    "goals": args.goals,
                    "scope_limitations": args.scope_limitations,
                    "priority": args.priority,
                    "status": args.status,
                }

                # Parse tags
                if args.tags:
                    project_data["tags"] = [tag.strip() for tag in args.tags.split(",")]

            api_client = InnoDayAPIClient(config)

            # Create project
            response = await api_client.post(
                f"/organizations/{org_id}/projects", json=project_data
            )

            if response.status_code not in [200, 201]:
                error_detail = response.json().get("detail", "Unknown error")
                console.print(format_error(f"Failed to create project: {error_detail}"))
                return 1

            created_project = response.json()

            console.print(format_success(f"Project created: {created_project['name']}"))
            console.print(format_info(f"ID: {created_project['id']}"))
            console.print(format_info(f"Alias: {created_project['alias']}"))
            console.print(format_info(f"Status: {created_project['status']}"))
            console.print(format_info(f"Priority: {created_project['priority']}"))

            await api_client.close()
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1

    @staticmethod
    async def _gather_project_data_interactive() -> Dict[str, Any]:
        """Gather project data interactively."""
        console.print("[bold]Create New Project[/bold]")
        console.print("-" * 40)

        name = Prompt.ask("Project name")
        alias = Prompt.ask(
            "Alias (short uppercase ticket prefix, e.g. PF, HS; unique within the org)"
        )
        description = Prompt.ask("Description", default="")
        goals = Prompt.ask("Goals (optional)", default="")
        scope_limitations = Prompt.ask("Scope limitations (optional)", default="")

        priority = Prompt.ask(
            "Priority",
            choices=PROJECT_PRIORITY_CHOICES,
            type=project_priority,
            default=ProjectPriority.MEDIUM.value,
        )

        status = Prompt.ask(
            "Status",
            choices=PROJECT_STATUS_CHOICES,
            type=project_status,
            default=ProjectStatus.PLANNING.value,
        )

        tags_input = Prompt.ask("Tags (comma-separated, optional)", default="")
        tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

        return {
            "name": name,
            "alias": alias.upper(),
            "description": description,
            "goals": goals or None,
            "scope_limitations": scope_limitations or None,
            "priority": priority,
            "status": status,
            "tags": tags,
        }

    @staticmethod
    async def _handle_update(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle projects update command."""
        try:
            # Verify organization is set
            org_alias = config.get_current_organization()
            if not org_alias:
                console.print(format_error("No organization selected"))
                console.print(
                    format_info(
                        "Run this from a directory with .innoday/project.yml, "
                        "or pass --organization <alias> explicitly"
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

            # Build update data from provided arguments
            update_data = {}
            if args.name:
                update_data["name"] = args.name
            if getattr(args, "alias", None):
                update_data["alias"] = args.alias
            if args.description:
                update_data["description"] = args.description
            if args.goals:
                update_data["goals"] = args.goals
            if args.scope_limitations:
                update_data["scope_limitations"] = args.scope_limitations
            if args.priority:
                update_data["priority"] = args.priority
            if args.status:
                update_data["status"] = args.status
            if args.tags:
                update_data["tags"] = [tag.strip() for tag in args.tags.split(",")]

            if not update_data:
                console.print(format_error("No update fields provided"))
                console.print(
                    format_info(
                        "Use --name, --description, --status, etc. to specify changes"
                    )
                )
                return 1

            api_client = InnoDayAPIClient(config)

            # Update project (router exposes PUT only at this path)
            response = await api_client.put(
                f"/organizations/{org_id}/projects/{project_id}",
                json=update_data,
            )

            if response.status_code == 404:
                console.print(format_error(f"Project '{project_id}' not found"))
                return 1
            elif response.status_code != 200:
                error_detail = response.json().get("detail", "Unknown error")
                console.print(format_error(f"Failed to update project: {error_detail}"))
                return 1

            updated_project = response.json()

            console.print(format_success(f"Project updated: {updated_project['name']}"))

            # **Report the server's answer, not our own request.** This printed
            # `update_data` -- what was *asked for* -- so a field the server
            # silently dropped still read as applied. `alias` was exactly that
            # for as long as it existed on the API model: accepted, answered
            # 200, discarded, and confirmed back to the user as changed.
            #
            # Comparing the two also surfaces the refusal for free.
            for key, requested in update_data.items():
                actual = updated_project.get(key, requested)
                console.print(format_info(f"  {key}: {actual}"))
                if _server_ignored(requested, actual):
                    console.print(
                        format_error(
                            f"  ⚠ asked for {key}={requested!r}, server has {actual!r}"
                        )
                    )

            await api_client.close()
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1

    @staticmethod
    async def _handle_delete(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle projects delete command."""
        try:
            # Verify organization is set
            org_alias = config.get_current_organization()
            if not org_alias:
                console.print(format_error("No organization selected"))
                console.print(
                    format_info(
                        "Run this from a directory with .innoday/project.yml, "
                        "or pass --organization <alias> explicitly"
                    )
                )
                return 1

            org_id = config.get_organization_id(org_alias)
            if not org_id:
                console.print(
                    format_error(f"Organization ID not found for '{org_alias}'")
                )
                return 1

            api_client = InnoDayAPIClient(config)

            # Confirmation prompt. Says "archive" because that is what the
            # server does -- the row is never removed, and the alias stays
            # taken (see ProjectService._normalize_alias). Show what is
            # attached first: a bare yes/no on an id string gives the operator
            # nothing to check the decision against.
            if not args.confirm:
                await ProjectCommands._print_archive_impact(
                    api_client, org_id, args.project_id
                )
                if not Confirm.ask(
                    f"Archive project '{args.project_id}'? "
                    "It keeps its alias and can be reactivated."
                ):
                    console.print("Archive cancelled")
                    await api_client.close()
                    return 0

            # Delete project
            response = await api_client.api_client.delete(
                f"{api_client.api_base_url}/api/v1/organizations/{org_id}/projects/{args.project_id}"
            )

            if response.status_code == 404:
                console.print(format_error(f"Project '{args.project_id}' not found"))
                await api_client.close()
                return 1
            elif response.status_code != 200:
                error_detail = response.json().get("detail", "Unknown error")
                console.print(
                    format_error(f"Failed to archive project: {error_detail}")
                )
                await api_client.close()
                return 1

            # Echo back what the server actually changed, so the result is
            # auditable rather than a fixed string.
            body = response.json() if response.content else {}
            label = body.get("alias") or body.get("id") or args.project_id
            previous = body.get("previous_status")
            detail = f" (was {previous})" if previous else ""
            console.print(format_success(f"Project '{label}' archived{detail}"))
            console.print(
                format_info(
                    "It keeps its alias and no longer appears in "
                    "`projects list`. Reactivate with "
                    f"`innoday projects update --project-id {label} "
                    "--status active`"
                )
            )

            await api_client.close()
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1

    @staticmethod
    async def _print_archive_impact(
        api_client: InnoDayAPIClient, org_id: str, project_ref: str
    ) -> None:
        """Print what is attached to a project before archiving it.

        Best effort: this decorates a confirmation prompt, so failing to fetch
        must not block the archive. Silently skipped when unavailable.
        """
        try:
            response = await api_client.get(
                f"/organizations/{org_id}/projects/{project_ref}/overview"
            )
            if response.status_code != 200:
                return
            overview = response.json()
        except Exception:
            return

        project = overview.get("project") or {}
        repositories = overview.get("repositories") or {}
        board = overview.get("board") or {}
        tickets = board.get("tickets") or {}

        name = project.get("name") or project_ref
        console.print(
            f"\n[bold]{name}[/bold] ([cyan]{project.get('alias', '?')}[/cyan])"
        )
        console.print(f"  Repositories: {repositories.get('total', 0)}")
        if board:
            console.print(
                f"  Board:        {board.get('name', 'unknown')} "
                f"({board.get('type', 'unknown')})"
            )
            console.print(
                f"  Tickets:      {tickets.get('total', 0)} total, "
                f"{tickets.get('open', 0)} open, "
                f"{tickets.get('in_progress', 0)} in progress"
            )
        else:
            console.print("  Board:        none attached")
        console.print("  Nothing is deleted -- these stay attached.\n")
