"""
InnoDay CLI Board Commands

Handles board management and summarization operations.
"""

import argparse
import json
from typing import Any, Dict, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.utils.formatters import (
    ProgressReporter,
    advisory_console,
    format_error,
    format_info,
    format_success,
    format_warning,
)

console = Console()


def format_sync_status(raw_status: Optional[str], *, dry_run: bool = False) -> str:
    """Render a board's sync status, matching either casing it arrives in.

    Case-insensitive deliberately. ``SyncStatus`` is a ``str`` Enum whose
    *values* are lowercase (``"completed"``), which is what the API serialises,
    while the database column stores the enum *name* (``"COMPLETED"``) -- so the
    same status is seen in either case depending on where it is read.

    Matching only the uppercase form meant none of the branches ever fired: a
    failed sync printed the bare, unstyled ``Status: failed`` rather than
    ``❌ Last sync failed``. Kept out of the handler so it can be tested against
    real inputs instead of a copy of this logic.
    """
    display = raw_status or "unknown"
    status = str(display).upper().replace(" ", "_")
    if status in ("PENDING", "IN_PROGRESS"):
        label = status.lower().replace("_", " ")
        return format_warning(f"🔄 Dry run {label}" if dry_run else f"🔄 Sync {label}")
    if status == "COMPLETED":
        # **Never in the past tense for a preview.** A dry run used to print
        # "Last sync completed successfully" over counts of tickets it had not
        # touched, which is how a stale board came to look freshly synced.
        if dry_run:
            return format_warning(
                "🔍 Last run was a DRY RUN — nothing was written. "
                "The counts below are what it would have done."
            )
        return format_success("✅ Last sync completed successfully")
    if status == "FAILED":
        return format_error("❌ Last sync failed")
    return f"Status: {display}"


class BoardCommands:
    """Board management and summarization commands."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up board command parser."""
        subparsers = parser.add_subparsers(
            title="Board Commands",
            dest="board_command",
            help="Board management and summarization operations",
        )

        # Summarize board
        summarize_parser = subparsers.add_parser(
            "summarize", help="Generate AI-powered summary of board tickets"
        )
        summarize_parser.add_argument(
            "--board-id", dest="board_id", required=True, help="Board registration ID"
        )
        summarize_parser.add_argument(
            "--type",
            choices=["status", "daily", "sprint", "weekly", "custom"],
            default="status",
            help="Type of summary to generate (default: status)",
        )
        summarize_parser.add_argument(
            "--time-window",
            type=int,
            default=24,
            help="Time window in hours for recent items (default: 24)",
        )
        summarize_parser.add_argument(
            "--format",
            choices=["table", "json", "markdown"],
            default="markdown",
            help="Output format (default: markdown)",
        )

        # Get summaries
        summaries_parser = subparsers.add_parser(
            "summaries", help="Get historical summaries for a board"
        )
        summaries_parser.add_argument(
            "--board-id", dest="board_id", required=True, help="Board registration ID"
        )
        summaries_parser.add_argument(
            "--limit",
            type=int,
            default=5,
            help="Maximum number of summaries to retrieve (default: 5)",
        )
        summaries_parser.add_argument(
            "--type",
            choices=["status", "daily", "sprint", "weekly", "custom"],
            help="Filter by summary type",
        )
        summaries_parser.add_argument(
            "--format",
            choices=["table", "json"],
            default="table",
            help="Output format (default: table)",
        )

        # Get latest summary
        latest_parser = subparsers.add_parser(
            "summary-latest", help="Get the most recent summary for a board"
        )
        latest_parser.add_argument(
            "--board-id", dest="board_id", required=True, help="Board registration ID"
        )
        latest_parser.add_argument(
            "--format",
            choices=["table", "json", "markdown"],
            default="markdown",
            help="Output format (default: markdown)",
        )

        # List boards
        list_parser = subparsers.add_parser("list", help="List registered boards")
        list_parser.add_argument(
            "--active-only",
            action="store_true",
            help="Show only active boards",
        )
        list_parser.add_argument(
            "--all-projects",
            dest="all_projects",
            action="store_true",
            help=(
                "List every board in the organization. Without this the list "
                "is scoped to the current project (--project, or the cwd's "
                ".innoday/project.yml)"
            ),
        )
        list_parser.add_argument(
            "--format",
            choices=["table", "json"],
            default="table",
            help="Output format (default: table)",
        )

        # Register board
        register_parser = subparsers.add_parser(
            "register", help="Register a new board for synchronization"
        )
        register_parser.add_argument(
            "board_url", help="Full URL to the board (Trello/Jira/Linear/Notion)"
        )
        register_parser.add_argument("board_name", help="Display name for the board")
        register_parser.add_argument(
            "--type",
            choices=["linear", "jira", "trello", "notion"],
            required=True,
            help="Type of board",
        )
        register_parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            dest="project_id",
            help="Project this board belongs to (required -- resolved from "
            "cwd's .innoday/project.yml when omitted)",
        )
        register_parser.add_argument(
            "--sync",
            action="store_true",
            help="Immediately sync the board after registering (leaves the "
            "board registered if the sync fails)",
        )
        BoardCommands._add_credential_arguments(register_parser)

        # Sync board
        sync_parser = subparsers.add_parser(
            "sync", help="Sync tickets from a registered board"
        )
        sync_parser.add_argument(
            "--board-id",
            dest="board_id",
            required=False,
            default=None,
            help="Board registration ID to sync. Optional: when omitted, the "
            "board is resolved from the current project (cwd's "
            ".innoday/project.yml) if it has exactly one board.",
        )
        sync_parser.add_argument(
            "--full",
            action="store_true",
            help="Perform full sync instead of incremental",
        )
        sync_parser.add_argument(
            "--force",
            action="store_true",
            help=(
                "Start even if a run is recorded as still in progress. An "
                "interrupted sync leaves that record behind and blocks every "
                "later one; this is the way out."
            ),
        )
        sync_parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview changes without applying them",
        )

        # Clear board tickets
        clear_parser = subparsers.add_parser(
            "clear",
            help="Logically delete all tickets synced from a board (reversible "
            "via re-sync; the board stays registered)",
        )
        clear_parser.add_argument("board_id", help="Board registration ID to clear")
        clear_parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report how many tickets would be cleared, without clearing",
        )
        clear_parser.add_argument(
            "--yes",
            action="store_true",
            help="Skip the confirmation prompt",
        )

        # Delete board registration (InnoDay-only soft-delete)
        delete_parser = subparsers.add_parser(
            "delete",
            help="Logically delete a board registration in InnoDay (soft-delete: "
            "the board row and its tickets are preserved for audit; the external "
            "board is never touched). Frees the project for a new board.",
        )
        delete_parser.add_argument("board_id", help="Board registration ID to delete")
        delete_parser.add_argument(
            "--yes",
            action="store_true",
            help="Skip the confirmation prompt",
        )

        # Sync status
        sync_status_parser = subparsers.add_parser(
            "sync-status", help="Check sync status for a board"
        )
        sync_status_parser.add_argument(
            "--board-id",
            dest="board_id",
            required=False,
            default=None,
            help="Board registration ID. Optional: when omitted, resolved from "
            "the current project (cwd's .innoday/project.yml) if it has "
            "exactly one board.",
        )

        # Set/rotate credential. `set-credential` stays registered as an alias:
        # it is the name in the docs and in anyone's shell history, and an
        # argparse alias costs nothing next to a command that silently vanished.
        for name, aliases in (("set-cred", ["set-credential"]),):
            set_credential_parser = subparsers.add_parser(
                name,
                aliases=aliases,
                help="Set or rotate the stored credential for this project's board",
            )
            # Both optional now. A project has exactly one board (the common
            # case), the cwd already says which project, and the board record
            # already knows its own type -- so requiring the operator to restate
            # a UUID and a board type they cannot be wrong about was asking for
            # a copy-paste error during a credential rotation, which is exactly
            # when you least want one.
            set_credential_parser.add_argument(
                "--board-id",
                dest="board_id",
                help="Board registration ID (default: the cwd project's board)",
            )
            set_credential_parser.add_argument(
                "--type",
                choices=["linear", "jira", "trello", "notion"],
                help="Board type (default: read from the resolved board)",
            )
            BoardCommands._add_credential_arguments(set_credential_parser)

    @staticmethod
    async def execute(args: argparse.Namespace, config) -> int:
        """Execute board command."""
        command = getattr(args, "board_command", None)

        # Check organization is configured
        if not config.get_current_organization():
            console.print(
                format_error(
                    "Organization not configured. Run 'innoday config init' first."
                )
            )
            return 1

        async with InnoDayAPIClient(config) as client:
            try:
                if command == "summarize":
                    return await BoardCommands._handle_summarize(args, client, config)
                elif command == "summaries":
                    return await BoardCommands._handle_summaries(args, client, config)
                elif command == "summary-latest":
                    return await BoardCommands._handle_latest(args, client, config)
                elif command == "list":
                    return await BoardCommands._handle_list(args, client, config)
                elif command == "register":
                    return await BoardCommands._handle_register(args, client, config)
                elif command == "sync":
                    return await BoardCommands._handle_sync(args, client, config)
                elif command == "clear":
                    return await BoardCommands._handle_clear(args, client, config)
                elif command == "delete":
                    return await BoardCommands._handle_delete(args, client, config)
                elif command == "sync-status":
                    return await BoardCommands._handle_sync_status(args, client, config)
                elif command in ("set-cred", "set-credential"):
                    return await BoardCommands._handle_set_credential(
                        args, client, config
                    )
                else:
                    console.print(format_error("No board command specified"))
                    console.print(
                        "[dim]Available: summarize, summaries, summary-latest, list, "
                        "register, sync, clear, sync-status, set-credential — run "
                        "'innoday board --help' for details[/dim]"
                    )
                    return 1

            except APIError as e:
                console.print(format_error(str(e)))
                return 1

    @staticmethod
    async def _handle_summarize(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """Handle board summarize command.

        HS-297: this no longer generates an AI-written summary server-side
        (that used to call Anthropic directly with a per-org CLAUDE_API_KEY).
        A bare CLI invocation has no Claude Code session attached to write
        prose from the data, so this command now only fetches and displays
        the same raw structured data (tickets, stats) that the MCP
        `get_board_summary_data` tool returns to an interactive session.
        Output is clearly labeled as structured data, not a summary.
        """
        # Get organization ID from config
        org_alias = config.get_current_organization()
        org_id = config.get_organization_id(org_alias)

        if not org_id:
            console.print(
                format_error(
                    "Organization ID not found. Please reconfigure with 'innoday config init'."
                )
            )
            return 1

        with ProgressReporter(
            f"Fetching {args.type} summary data for board {args.board_id}..."
        ):
            response = await client.get(
                f"/organizations/{org_id}/boards/{args.board_id}/summary-data",
                params={"summary_type": args.type},
            )

        if response.status_code == 200:
            data = response.json()

            # Format output based on requested format
            if args.format == "json":
                print(json.dumps(data, indent=2))
            elif args.format == "markdown":
                console.print(
                    format_success(
                        "Structured data for summary (no AI-written summary -- "
                        "run this via Claude Code/MCP to get prose)"
                    )
                )
                console.print(
                    Panel(
                        f"Board: {data.get('board_name', args.board_id)}\n"
                        f"Ticket count: {data.get('ticket_count', 'unknown')}",
                        title=f"📊 {args.type.upper()} Summary Data",
                        border_style="green",
                    )
                )

                # Display stats with custom organization
                if data.get("stats"):
                    stats_table = Table(title="📈 Statistics", show_edge=True)
                    stats_table.add_column("Metric", style="cyan")
                    stats_table.add_column("Value", style="yellow", justify="right")

                    stats = data["stats"]

                    # Completed tickets section (at top)
                    stats_table.add_row(
                        "Completed (24h)", str(stats.get("completed_24h", 0))
                    )
                    stats_table.add_row(
                        "Completed (48h)", str(stats.get("completed_48h", 0))
                    )
                    stats_table.add_row(
                        "Completed (7d)", str(stats.get("completed_7d", 0))
                    )

                    # Add separator row
                    stats_table.add_row("", "")

                    # Active tickets section with indented sub-items
                    stats_table.add_row(
                        "Active Tickets", str(stats.get("active_tickets", 0))
                    )
                    stats_table.add_row(
                        "  In Progress", str(stats.get("in_progress", 0))
                    )
                    stats_table.add_row("  In Review", str(stats.get("in_review", 0)))
                    stats_table.add_row(
                        "  Todo (Assigned)", str(stats.get("todo_assigned", 0))
                    )
                    stats_table.add_row("  Blocked", str(stats.get("blocked", 0)))

                    # Backlog
                    stats_table.add_row("Backlog", str(stats.get("backlog", 0)))

                    # Add separator row
                    stats_table.add_row("", "")

                    # Total tickets at bottom
                    stats_table.add_row(
                        "[bold]Total Tickets[/bold]",
                        f"[bold]{stats.get('total_tickets', 0)}[/bold]",
                    )

                    console.print(stats_table)

                # Display recent completions
                if data.get("recent_completions"):
                    from collections import defaultdict
                    from datetime import date, datetime

                    # Group tickets by date
                    tickets_by_date = defaultdict(list)
                    today = date.today()

                    for ticket in data["recent_completions"]:
                        if ticket.get("completed_date"):
                            # Parse the date from the ticket
                            try:
                                completed_date = datetime.fromisoformat(
                                    ticket["completed_date"].replace("Z", "+00:00")
                                ).date()
                            except Exception:
                                completed_date = today
                            tickets_by_date[completed_date].append(ticket)

                    # Sort dates in descending order (most recent first)
                    sorted_dates = sorted(tickets_by_date.keys(), reverse=True)

                    # Count total tickets
                    total_count = sum(
                        len(tickets) for tickets in tickets_by_date.values()
                    )
                    console.print(
                        f"\n[bold cyan]Tickets Completed in Last 7 Days ({total_count} total)[/bold cyan]\n"
                    )

                    # Display grouped by date
                    ticket_num = 1
                    for date_key in sorted_dates:
                        # Calculate days ago
                        days_diff = (today - date_key).days

                        # Format date header
                        if days_diff == 0:
                            date_header = f"Today ({date_key.strftime('%B %d, %Y')})"
                        elif days_diff == 1:
                            date_header = (
                                f"Yesterday ({date_key.strftime('%B %d, %Y')})"
                            )
                        else:
                            date_header = f"{days_diff} Days Ago ({date_key.strftime('%B %d, %Y')})"

                        console.print(f"  [bold]{date_header}:[/bold]")

                        # Display tickets for this date
                        for ticket in tickets_by_date[date_key]:
                            release_text = (
                                f" ({ticket['release']})"
                                if ticket.get("release")
                                else " (No release)"
                            )
                            summary = (
                                ticket["summary"][:80]
                                if len(ticket["summary"]) > 80
                                else ticket["summary"]
                            )
                            console.print(
                                f"  {ticket_num}. {ticket['key']}: {summary}{release_text}"
                            )
                            ticket_num += 1

                        console.print()  # Add blank line between date groups
            else:
                # Table format
                table = Table(title=f"Board Summary Data - {args.type.upper()}")
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="white")

                table.add_row("Board", str(data.get("board_name", args.board_id)))
                table.add_row("Type", str(data.get("summary_type", args.type)))
                table.add_row("Generated At", str(data.get("generated_at", "")))
                table.add_row("Ticket Count", str(data.get("ticket_count", 0)))

                console.print(table)

            console.print(
                format_success(
                    "Structured data fetched successfully! (No AI summary was "
                    "written -- use this data via Claude Code/MCP to get one.)"
                )
            )
            return 0
        else:
            error_msg = "Failed to fetch summary data"
            if response.content:
                try:
                    error_data = response.json()
                    error_msg = (
                        f"{error_msg}: {error_data.get('detail', 'Unknown error')}"
                    )
                except Exception:
                    error_msg = f"{error_msg}: HTTP {response.status_code}"
            console.print(format_error(error_msg))
            return 1

    @staticmethod
    async def _handle_summaries(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """Handle board summaries command."""
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
                format_error(
                    "Organization ID not found. Please reconfigure with 'innoday config init'."
                )
            )
            return 1

        params = {"limit": args.limit}
        if args.type:
            params["summary_type"] = args.type

        response = await client.get(
            f"/organizations/{org_id}/boards/{args.board_id}/summaries", params=params
        )

        if response.status_code == 200:
            data = response.json()
            summaries = data.get("summaries", [])

            if not summaries:
                if args.format == "json":
                    print(json.dumps([], indent=2))
                    return 0
                console.print(format_warning("No summaries found for this board"))
                return 0

            # Display message. To stderr: it lands immediately before the JSON
            # payload below, and a line of prose in front of it is enough to
            # make the whole stream unparseable.
            advisory_console.print(f"\n💬 {data.get('message', '')}\n")

            if args.format == "json":
                print(json.dumps(summaries, indent=2))
            else:
                # Table format
                table = Table(title=f"Board Summaries ({len(summaries)} found)")
                table.add_column("ID", style="cyan", no_wrap=True)
                table.add_column("Type", style="yellow")
                table.add_column("Created", style="green")
                table.add_column("Stats", style="white")
                table.add_column("Motivational", style="magenta", max_width=30)

                for summary in summaries:
                    stats_str = f"📊 {summary['stats'].get('total_tickets', 0)} tickets"
                    table.add_row(
                        summary["id"][:8] + "...",
                        summary["summary_type"],
                        summary["created_at"][:19],
                        stats_str,
                        summary.get("motivational_message", "")[:30] + "...",
                    )

                console.print(table)

            return 0
        else:
            console.print(format_error(f"Failed to get summaries: {response}"))
            return 1

    @staticmethod
    async def _handle_latest(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """Handle board summary-latest command."""
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
                format_error(
                    "Organization ID not found. Please reconfigure with 'innoday config init'."
                )
            )
            return 1

        response = await client.get(
            f"/organizations/{org_id}/boards/{args.board_id}/summaries/latest"
        )

        if response.status_code == 200:
            data = response.json()

            # Display message with motivational quote. To stderr -- see above:
            # stdout carries the payload and nothing else.
            advisory_console.print(f"\n💬 {data.get('message', '')}\n")

            if args.format == "json":
                print(json.dumps(data, indent=2))
            elif args.format == "markdown":
                # Display as formatted markdown
                console.print(
                    Panel(
                        Markdown(data["summary"]),
                        title=f"📊 Latest {data['summary_type'].upper()} Summary",
                        subtitle=f"Generated: {data['created_at']}",
                        border_style="green",
                    )
                )

                # Display stats if present
                if data.get("stats"):
                    console.print("\n[bold]Statistics:[/bold]")
                    for key, value in data["stats"].items():
                        console.print(f"  • {key.replace('_', ' ').title()}: {value}")
            else:
                # Table format
                table = Table(title="Latest Board Summary")
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="white")

                table.add_row("Summary ID", data["id"])
                table.add_row("Type", data["summary_type"])
                table.add_row("Created At", data["created_at"])
                table.add_row("Motivational", data.get("motivational_message", ""))

                console.print(table)
                console.print(f"\n[bold]Summary:[/bold]\n{data['summary']}")

            return 0
        else:
            console.print(format_error(f"Failed to get latest summary: {response}"))
            return 1

    @staticmethod
    async def _handle_list(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """Handle board list command."""
        # Get organization ID from config
        org_alias = config.get_current_organization()
        org_id = config.get_organization_id(org_alias)

        if not org_id:
            console.print(
                format_error(
                    "Organization ID not found. Please reconfigure with 'innoday config init'."
                )
            )
            return 1

        params = {}
        if hasattr(args, "active_only") and args.active_only:
            params["active_only"] = True

        # Get boards for the organization
        response = await client.get(f"/organizations/{org_id}/boards", params=params)

        if response.status_code == 200:
            boards = response.json()

            # Follow the project in context, like tickets and repos. There is
            # no project-scoped board route (the project board endpoint is
            # POST-only), and BoardRegistrationResponse carries project_id, so
            # filter here rather than add an endpoint for one field.
            all_projects = getattr(args, "all_projects", False)
            scoped = bool(client.project_id) and not all_projects
            if scoped:
                boards = [b for b in boards if b.get("project_id") == client.project_id]

            if not boards:
                if args.format == "json":
                    print(json.dumps([], indent=2))
                    return 0
                if scoped:
                    console.print(
                        format_warning(
                            "No board registered for this project "
                            "-- pass --all-projects to see the organization's"
                        )
                    )
                else:
                    console.print(
                        format_warning("No boards registered for this organization")
                    )
                return 0

            if scoped:
                advisory_console.print(
                    format_info(
                        f"Scoped to project {client.project_id} "
                        "-- pass --all-projects for the whole organization"
                    )
                )

            if args.format == "json":
                print(json.dumps(boards, indent=2))
            else:
                # Table format
                table = Table(title=f"Registered Boards ({len(boards)} found)")
                table.add_column("ID", style="cyan", no_wrap=True)
                table.add_column("Name", style="yellow")
                table.add_column("Type", style="green")
                table.add_column("Active", style="white")
                table.add_column("Last Sync", style="magenta")

                for board in boards:
                    table.add_row(
                        board["id"][:8] + "...",
                        board["board_name"],
                        board["board_type"],
                        "✅" if board["is_active"] else "❌",
                        (
                            board.get("last_sync_at", "Never")[:19]
                            if board.get("last_sync_at")
                            else "Never"
                        ),
                    )

                console.print(table)

            return 0
        else:
            console.print(format_error(f"Failed to list boards: {response}"))
            return 1

    # Which flags a given board type needs, phrased for an error message.
    # Single source of truth for `register` and `set-cred`, which supply a
    # credential the same way and must not drift apart.
    REQUIRED_CREDENTIAL_FLAGS = {
        "jira": "--email and --api-token",
        "trello": "--api-key and --token",
        "linear": "--token",
        "notion": "--token",
    }

    @staticmethod
    def _add_credential_arguments(parser: argparse.ArgumentParser) -> None:
        """Register the explicit credential flags on a subparser.

        A credential reaches InnoDay only by being typed, never by being
        found: `register` used to read `~/.innoday/config.json` for whatever
        the operator happened to have saved (#609).
        """
        parser.add_argument("--email", help="Jira account email")
        parser.add_argument("--api-token", help="Jira API token")
        parser.add_argument("--api-key", help="Trello API key")
        parser.add_argument("--token", help="Trello/Linear/Notion token")

    @staticmethod
    def _integration_token_from_args(
        board_type: str, args: argparse.Namespace
    ) -> Optional[str]:
        """Build the X-Integration-Token value from the credential flags."""
        return BoardCommands._build_integration_token_header(
            board_type,
            {
                "email": getattr(args, "email", None),
                "api_token": getattr(args, "api_token", None),
                "api_key": getattr(args, "api_key", None),
                "token": getattr(args, "token", None),
            },
        )

    @staticmethod
    def _missing_credential_error(board_type: str) -> str:
        return (
            f"Missing required credential fields for a {board_type} board "
            f"(need {BoardCommands.REQUIRED_CREDENTIAL_FLAGS[board_type]})"
        )

    @staticmethod
    def _build_integration_token_header(
        board_type: str, source: Dict[str, Any]
    ) -> Optional[str]:
        """Build the X-Integration-Token string from a dict of credential
        fields. Jira/Trello take a colon-joined pair; Linear/Notion take the
        raw token -- matches the shapes validate_board_access
        (src/routers/boards.py) already expects. Returns None if the
        required fields for the given board_type aren't present in source."""
        if board_type == "jira" and source.get("email") and source.get("api_token"):
            return f"{source['email']}:{source['api_token']}"
        elif board_type == "trello" and source.get("api_key") and source.get("token"):
            return f"{source['api_key']}:{source['token']}"
        elif board_type in ("linear", "notion") and source.get("token"):
            return source["token"]
        return None

    @staticmethod
    async def _handle_register(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """Handle board registration command."""
        # Get user ID from config
        user_id = config.get_user_id()
        if not user_id:
            console.print(
                format_error("User ID not configured. Run 'innoday config init' first.")
            )
            return 1

        # Get organization ID
        org_alias = config.get_current_organization()
        org_id = config.get_organization_id(org_alias)

        if not org_id:
            console.print(
                format_error(
                    "Organization ID not found. Please reconfigure with 'innoday config init'."
                )
            )
            return 1

        # A board must belong to a project (BoardRegistration.project_id is a
        # required FK) -- resolve from --project-id, falling back to cwd's
        # .innoday/project.yml, and fail clearly if neither resolves.
        project_id = (
            getattr(args, "project_id", None) or config.get_current_project_id()
        )
        if not project_id:
            console.print(
                format_error(
                    "No project specified. Pass --project-id, or run this "
                    "command from inside a project directory (one with "
                    ".innoday/project.yml)."
                )
            )
            return 1

        # Registration is the one legitimate moment a credential is supplied
        # -- it is how one reaches Vault, where every later sync resolves it
        # from. It must be typed, not found: this used to read whatever
        # `~/.innoday/config.json` held for this board type (#609).
        token = BoardCommands._integration_token_from_args(args.type, args)
        if not token:
            console.print(
                format_error(BoardCommands._missing_credential_error(args.type))
            )
            return 1
        headers = {"X-Integration-Token": token}

        # Build registration data
        board_data = {
            "organization_id": org_id,
            "project_id": project_id,
            "board_url": args.board_url,
            "board_name": args.board_name,
            "board_type": args.type,
        }

        with ProgressReporter(f"Registering {args.type} board...") as progress:
            try:
                # Call the real registration endpoint -- this previously
                # posted to /users/{user_id}/board-registrations, which does
                # not exist anywhere in the API (confirmed against the live
                # OpenAPI schema); innoday board register has never worked.
                response = await client.post(
                    f"/organizations/{org_id}/boards",
                    json=board_data,
                    headers=headers,
                )

                # Parse JSON from response
                if response.status_code == 200 or response.status_code == 201:
                    data = response.json()
                else:
                    data = None

                if data and "id" in data:
                    progress.update("Board registered successfully")

                    # Display registration info
                    console.print(format_success(f"✅ Board registered: {data['id']}"))
                    console.print(f"  Name: {data.get('board_name', 'Unknown')}")
                    console.print(f"  Type: {data.get('board_type', 'Unknown')}")
                    console.print(f"  URL: {data.get('board_url', 'Unknown')}")
                    console.print(f"  Active: {data.get('is_active', False)}")
                    console.print()
                    console.print(
                        "Now you can sync with: "
                        f"innoday board sync --board-id {data['id']}"
                    )

                    if getattr(args, "sync", False):
                        console.print()
                        console.print("Running initial sync...")
                        sync_args = argparse.Namespace(
                            board_command="sync",
                            board_id=data["id"],
                            full=False,
                            dry_run=False,
                        )
                        sync_rc = await BoardCommands._handle_sync(
                            sync_args, client, config
                        )
                        if sync_rc != 0:
                            console.print(
                                format_error(
                                    "Board registered, but the initial sync "
                                    "failed. Retry: "
                                    f"innoday board sync --board-id {data['id']}"
                                )
                            )
                        # Exit 0 regardless: `register` was asked to create the
                        # board, and it did -- the board is live and is not
                        # rolled back on a sync failure. `--sync` is a
                        # convenience that runs afterwards; reporting its
                        # outcome as the *registration's* exit code tells a
                        # script the board does not exist, and the obvious
                        # response to that lie is to register again, which
                        # duplicates it. What went wrong is on the line above,
                        # with the command that retries just the sync.
                        #
                        # Since #622 this mattered for a refusal too: a 429
                        # ("a sync is already running") now exits 1, so a
                        # successful registration inherited a failure from a
                        # server response that means the system is working.
                        return 0

                    return 0
                else:
                    console.print(format_error(f"Failed to register board: {response}"))
                    return 1

            except APIError as e:
                console.print(format_error(f"Registration failed: {str(e)}"))
                return 1

    @staticmethod
    async def _resolve_board(
        args: argparse.Namespace,
        client: InnoDayAPIClient,
        config,
        org_id: str,
    ) -> Optional[dict]:
        """Return the board **record** to operate on.

        If --board-id was passed, use it -- but still look the record up, so
        callers get the board's type without asking the operator to restate it.
        A board id from outside the current project still works: the id is
        honoured even when the lookup cannot see it, so nothing that worked
        before stops working.

        Otherwise resolve the current project from cwd's .innoday/project.yml
        and look at the boards registered to it: exactly one -> use it; zero or
        many -> print a clear message and return None so the caller aborts.
        This mirrors how `board list` / `board register` already scope to the
        cwd project, so a developer standing in a project workspace can just
        run `innoday board sync` with no arguments.
        """
        explicit = getattr(args, "board_id", None)
        if explicit:
            return {"id": explicit}

        project_id = config.get_current_project_id()
        if not project_id:
            console.print(
                format_error(
                    "No --board-id given and no current project to resolve one from."
                )
            )
            console.print(
                format_info(
                    "Run this from inside a project directory (one with "
                    ".innoday/project.yml), or pass --board-id explicitly."
                )
            )
            return None

        response = await client.get(f"/organizations/{org_id}/boards")
        if response.status_code != 200:
            console.print(
                format_error(f"Could not list boards to resolve one: {response}")
            )
            return None

        boards = [
            b for b in (response.json() or []) if b.get("project_id") == project_id
        ]

        if not boards:
            console.print(
                format_error("No board is registered for the current project.")
            )
            console.print(
                format_info(
                    "Register one with `innoday board register`, or pass "
                    "--board-id to sync a board from another project."
                )
            )
            return None

        if len(boards) > 1:
            console.print(
                format_error(
                    f"The current project has {len(boards)} boards — "
                    "pass --board-id to choose one:"
                )
            )
            for b in boards:
                console.print(
                    format_info(
                        f"  {b.get('id')}  {b.get('board_name')} "
                        f"({b.get('board_type')})"
                    )
                )
            return None

        board = boards[0]
        console.print(
            format_info(
                f"Using board {board.get('board_name')} "
                f"({board.get('board_type')}) for the current project."
            )
        )
        return board

    @staticmethod
    async def _resolve_board_id(
        args: argparse.Namespace,
        client: InnoDayAPIClient,
        config,
        org_id: str,
    ) -> Optional[str]:
        """Just the id, for callers that need nothing but the id.

        An explicit `--board-id` costs **no request** here, which
        `tests/cli/commands/test_boards.py` pins deliberately: `board sync
        --board-id X` should not pay for a board listing it will not read.
        `set-cred` uses `_resolve_board_record` instead, because it genuinely
        needs the board's type and one extra GET during a credential rotation
        is a fair price for not making the operator restate it.
        """
        board = await BoardCommands._resolve_board(args, client, config, org_id)
        return None if board is None else board.get("id")

    @staticmethod
    async def _resolve_board_record(
        args: argparse.Namespace,
        client: InnoDayAPIClient,
        config,
        org_id: str,
    ) -> Optional[dict]:
        """The board record, looking an explicit `--board-id` up as well.

        Only `set-cred` wants this: it needs `board_type`, and a record with
        just an id would send it back to demanding `--type`. A board id from
        outside the current project still works -- the id is honoured even when
        the listing cannot see it, so nothing that worked before stops working.
        """
        board = await BoardCommands._resolve_board(args, client, config, org_id)
        if board is None:
            return None
        if board.get("board_type"):
            return board
        try:
            response = await client.get(f"/organizations/{org_id}/boards")
            if response.status_code == 200:
                listing = response.json()
                # Shape-checked rather than assumed. This is an enrichment
                # lookup for a value we can live without, so anything other than
                # a list of objects means "no type available" -- never a crash
                # partway through a credential rotation.
                if isinstance(listing, list):
                    for candidate in listing:
                        if isinstance(candidate, dict) and candidate.get(
                            "id"
                        ) == board.get("id"):
                            return candidate
        except APIError:
            pass
        return board

    @staticmethod
    async def _handle_sync(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """Handle board sync command."""

        # No credential is sent, and none is read from this machine: the
        # server resolves the board's own credential from Vault (#609). What
        # stood here read `~/.innoday/config.json` for the FIRST of
        # linear/jira/trello/notion that happened to be configured and sent
        # it regardless of the board's actual type -- so a saved Jira
        # credential would be forwarded to api.linear.app when syncing a
        # Linear board, the shape of #562.
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
                format_error(
                    "Organization ID not found. Please reconfigure with 'innoday config init'."
                )
            )
            return 1

        board_id = await BoardCommands._resolve_board_id(args, client, config, org_id)
        if not board_id:
            return 1

        # Build sync request
        sync_data = {
            "full_sync": args.full if hasattr(args, "full") else False,
            "dry_run": args.dry_run if hasattr(args, "dry_run") else False,
            # An interrupted sync leaves a PENDING row that blocks every later
            # one. Before this flag existed the only way out was editing that row
            # by hand, which is what happened on Atomic the night before its
            # release.
            "force": args.force if hasattr(args, "force") else False,
        }

        with ProgressReporter("Syncing board tickets...") as progress:
            try:
                # Call sync endpoint
                response = await client.post(
                    f"/organizations/{org_id}/boards/{board_id}/sync",
                    json=sync_data,
                )

                # Parse JSON from response
                if response.status_code == 200 or response.status_code == 201:
                    data = response.json()
                else:
                    data = None

                if data and "sync_id" in data:
                    progress.update("Board sync initiated")

                    # Display sync info
                    console.print(format_success(f"✅ Sync started: {data['sync_id']}"))
                    console.print(f"  Status: {data.get('status', 'PENDING')}")
                    console.print(
                        f"  Message: {data.get('message', 'Sync in progress')}"
                    )

                    if data.get("tickets_found") is not None:
                        console.print(f"  Tickets found: {data['tickets_found']}")

                    console.print()
                    console.print(
                        "💡 Tip: Check sync status with: "
                        f"innoday board sync-status --board-id {board_id}"
                    )

                    return 0
                elif response.status_code == 429:
                    # The server's detail names the blocking run and the way
                    # past it; this line used to say "please wait", the wrong
                    # advice when the blocker is a row a dead process left
                    # behind (#613).
                    #
                    # Kept identical to `SyncCommands._sync_board`'s 429 branch,
                    # down to the fallback wording: the same refusal reached the
                    # operator two different ways, and the two were fixed twice
                    # and came out disagreeing about whether to print the
                    # sync-status hint at all.
                    try:
                        error_detail = response.json() if response.content else {}
                    except json.JSONDecodeError:
                        # A 429 from a proxy in front of the API is HTML, not
                        # JSON. `src/cli/client.py` is where this guard is
                        # settled; a bare `.json()` here would traceback.
                        error_detail = {}
                    console.print(
                        format_warning(
                            error_detail.get(
                                "detail", "Sync already in progress for this board."
                            )
                        )
                    )
                    console.print(
                        "  [dim]Check status with: "
                        f"innoday board sync-status --board-id {board_id}[/dim]"
                    )
                    # Exits 1: the sync did not happen. See the twin in
                    # `SyncCommands._sync_board` (#622).
                    return 1
                else:
                    error_msg = response.json() if response.content else str(response)
                    console.print(format_error(f"Failed to sync board: {error_msg}"))
                    return 1

            except APIError as e:
                console.print(format_error(f"Sync failed: {str(e)}"))
                return 1

    @staticmethod
    async def _handle_clear(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """Handle board clear -- logically delete a board's tickets."""
        org_alias = config.get_current_organization()
        org_id = config.get_organization_id(org_alias)
        if not org_id:
            console.print(format_error("Organization not configured."))
            return 1

        query = "?dry_run=true" if args.dry_run else ""
        if not args.dry_run and not getattr(args, "yes", False):
            confirmed = Confirm.ask(
                f"Logically delete all tickets synced from board {args.board_id}? "
                "(reversible via re-sync)"
            )
            if not confirmed:
                console.print("Aborted.")
                return 0

        with ProgressReporter("Clearing board...") as progress:
            response = await client.post(
                f"/organizations/{org_id}/boards/{args.board_id}/clear{query}",
                json={},
            )
            if response.status_code == 200:
                cleared = response.json().get("cleared", 0)
                verb = "Would clear" if args.dry_run else "Cleared"
                progress.update("Done")
                console.print(format_success(f"✅ {verb} {cleared} ticket(s)"))
                return 0
            console.print(format_error(f"Failed to clear board: {response}"))
            return 1

    @staticmethod
    async def _handle_delete(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """Handle board delete -- logically delete a board registration in
        InnoDay (soft-delete). Calls DELETE /boards/{id}, which sets the board's
        deleted_at + is_active=False and cascade-clears its tickets. This is an
        InnoDay-only operation: the external board (Jira/Linear/Trello) is never
        touched. Frees the board's project so a new board can be registered.
        """
        org_alias = config.get_current_organization()
        org_id = config.get_organization_id(org_alias)
        if not org_id:
            console.print(format_error("Organization not configured."))
            return 1

        if not getattr(args, "yes", False):
            confirmed = Confirm.ask(
                f"Logically delete board registration {args.board_id} in InnoDay? "
                "(soft-delete -- board and tickets preserved for audit; the "
                "external board is not touched)"
            )
            if not confirmed:
                console.print("Aborted.")
                return 0

        with ProgressReporter("Deleting board registration...") as progress:
            response = await client.delete(
                f"/organizations/{org_id}/boards/{args.board_id}"
            )
            if response.status_code == 200:
                cleared = response.json().get("cleared", 0)
                progress.update("Done")
                console.print(
                    format_success(
                        f"✅ Board registration deleted (soft) -- {cleared} "
                        "ticket(s) cleared, all rows preserved."
                    )
                )
                return 0
            console.print(format_error(f"Failed to delete board: {response}"))
            return 1

    @staticmethod
    async def _handle_sync_status(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """Handle board sync status command."""
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
                format_error(
                    "Organization ID not found. Please reconfigure with 'innoday config init'."
                )
            )
            return 1

        board_id = await BoardCommands._resolve_board_id(args, client, config, org_id)
        if not board_id:
            return 1

        try:
            # Call sync status endpoint -- GET .../sync-history returns a
            # JSON array of records ordered newest-first (response_model
            # List[Dict] in src/routers/boards.py::get_sync_history), not a
            # single status object. With limit=1 the most recent record is
            # entries[0]. Field names also come straight from
            # BoardSyncHistory (sync_status/tickets_found/...), not the
            # status/tickets_processed names this used to assume.
            response = await client.get(
                f"/organizations/{org_id}/boards/{board_id}/sync-history",
                params={"limit": 1},
            )

            if response.status_code == 200:
                entries = response.json()

                if not entries:
                    console.print(
                        format_warning("⚠️  Board has never been synchronized")
                    )
                    return 0

                data = entries[0]

                preview = bool(data.get("dry_run"))
                console.print(
                    format_sync_status(data.get("sync_status"), dry_run=preview)
                )
                verb = "would create" if preview else "created"
                verb_u = "would update" if preview else "updated"

                if data.get("started_at"):
                    console.print(f"  Started: {data['started_at']}")
                if data.get("completed_at"):
                    console.print(f"  Completed: {data['completed_at']}")
                if data.get("tickets_found") is not None:
                    console.print(f"  Tickets found: {data['tickets_found']}")
                if data.get("tickets_created") is not None:
                    console.print(f"  Tickets {verb}: {data['tickets_created']}")
                if data.get("tickets_updated") is not None:
                    console.print(f"  Tickets {verb_u}: {data['tickets_updated']}")
                if data.get("tickets_skipped") is not None:
                    console.print(f"  Tickets skipped: {data['tickets_skipped']}")
                if data.get("duration_seconds") is not None:
                    console.print(f"  Duration: {data['duration_seconds']} seconds")
                if data.get("error_message"):
                    console.print(f"  Error: {data['error_message']}")

                return 0
            else:
                error_msg = response.json() if response.content else str(response)
                console.print(format_error(f"Failed to get sync status: {error_msg}"))
                return 1

        except APIError as e:
            console.print(format_error(f"Failed to get sync status: {str(e)}"))
            return 1

    @staticmethod
    async def _handle_set_credential(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """Set or rotate a board's Vault-stored credential via PATCH
        .../boards/{board_id}/credential. Covers both rotating an existing
        credential and setting one for a pre-Vault board that never had one
        stored.

        Neither --board-id nor --type is required: the cwd names the project,
        the project has one board, and the board record carries its own type.
        """
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
                format_error(
                    "Organization ID not found. Please reconfigure with 'innoday config init'."
                )
            )
            return 1

        board = await BoardCommands._resolve_board_record(args, client, config, org_id)
        if board is None:
            return 1
        board_id = board.get("id")

        # An explicit --type wins (it is the escape hatch for a board whose
        # record could not be read); otherwise take the board's own.
        board_type = getattr(args, "type", None) or board.get("board_type") or ""
        board_type = str(board_type).lower()
        if board_type not in ("linear", "jira", "trello", "notion"):
            console.print(
                format_error(
                    "Could not determine the board type — pass --type explicitly."
                )
            )
            return 1

        token = BoardCommands._integration_token_from_args(board_type, args)
        if not token:
            console.print(
                format_error(BoardCommands._missing_credential_error(board_type))
            )
            return 1

        try:
            response = await client.patch(
                f"/organizations/{org_id}/boards/{board_id}/credential",
                headers={"X-Integration-Token": token},
            )

            if response.status_code == 200:
                data = response.json()
                console.print(
                    format_success(f"✅ Credential updated for board {board_id}")
                )
                console.print(f"  Type: {data.get('board_type', board_type)}")
                console.print(f"  Updated: {data.get('updated_at', 'unknown')}")
                console.print()
                console.print(
                    f"💡 Tip: Verify with: innoday board sync --board-id {board_id}"
                )
                return 0
            elif response.status_code == 403:
                error_detail = response.json() if response.content else {}
                console.print(
                    format_error(
                        error_detail.get(
                            "detail", "Cannot access board with provided token"
                        )
                    )
                )
                return 1
            elif response.status_code == 404:
                console.print(format_error(f"Board {board_id} not found"))
                return 1
            else:
                error_msg = response.json() if response.content else str(response)
                console.print(format_error(f"Failed to update credential: {error_msg}"))
                return 1

        except APIError as e:
            console.print(format_error(f"Failed to update credential: {str(e)}"))
            return 1
