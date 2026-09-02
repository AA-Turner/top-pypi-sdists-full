"""
InnoDay CLI Ticket Commands

Handles ticket management operations.
"""

import argparse
import sys
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.prompt import Confirm, Prompt

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.utils.formatters import (
    OutputFormatter,
    ProgressReporter,
    advisory_console,
    format_error,
    format_info,
    format_success,
    format_warning,
)
from src.domain.ticket import TicketStatus
from src.services.release_planning import OUTSTANDING_STATUSES, semver_key
from src.services.ticket_release import CURRENT_RELEASE

console = Console()

#: The status vocabulary, derived from the enum rather than restated (GH #630).
#:
#: **The names and the values are spelled differently, and both spellings were in
#: circulation.** `TicketStatus.IN_PROGRESS` is named `IN_PROGRESS` and valued
#: `"in progress"` -- a space, not an underscore -- and every hand-written list of
#: choices in this file and in the MCP tool descriptions was written from the
#: names. The API validates values. So `create_ticket`'s own default of `"TODO"`
#: was rejected by its own API, which is the simplest call the tool has.
#:
#: Deriving the list removes the class of bug rather than one instance: a member
#: added or renamed on the enum cannot leave these behind. Both spellings are
#: offered because scripts and skills already pass the uppercase names, and the
#: API now accepts either (see `TicketStatus._missing_`).
STATUS_CHOICES = [status.name for status in TicketStatus] + [
    status.value for status in TicketStatus if status.value != status.name
]

#: What to print when listing them for a human -- the names, which is what the
#: help text has always shown and what callers type.
STATUS_NAMES = ", ".join(status.name for status in TicketStatus)


def _add_deprecated_ticket_id_flag(parser: argparse.ArgumentParser) -> None:
    """Keep `--ticket-id` working, hidden, alongside the positional.

    The id used to be a *required flag* on six of these subcommands while
    `cancel`/`delete` took it positionally -- an inconsistency with no recorded
    reason, and it made the obvious form (`innoday tickets show 1416`) fail with a
    usage error. The positional is now the documented way.

    The flag stays, suppressed from help rather than removed, because scripts and
    skills in other repos already pass it and a rename that breaks them buys
    nothing. `dest` differs from the positional's so the handler can tell which
    was used.
    """
    parser.add_argument("--ticket-id", dest="ticket_id_flag", help=argparse.SUPPRESS)


#: Which release statuses the picker offers, and in what order -- derived from
#: `OUTSTANDING_STATUSES` rather than typed, so a fifth `ReleaseStatus` member
#: cannot be silently absent here while `release_planning` includes it. Keyed by
#: the enum *value*, because that is what the releases endpoint serialises
#: (`r.status.value`).
_OUTSTANDING_RANK: Dict[str, int] = {
    status.value: rank for rank, status in enumerate(OUTSTANDING_STATUSES)
}


class TicketCommands:
    """Ticket management commands."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up ticket command parser."""
        subparsers = parser.add_subparsers(
            title="Ticket Commands", dest="ticket_command", help="Ticket operations"
        )

        # Tickets list
        list_parser = subparsers.add_parser("list", help="List tickets")
        list_parser.add_argument(
            "--status",
            choices=STATUS_CHOICES,
            metavar="STATUS",
            help=f"Filter by status: {STATUS_NAMES}",
        )
        list_parser.add_argument("--assignee", help="Filter by assignee")
        list_parser.add_argument(
            "--all-projects",
            dest="all_projects",
            action="store_true",
            help=(
                "List every ticket in the organization. Without this the list "
                "is scoped to the current project (--project, or the cwd's "
                ".innoday/project.yml)"
            ),
        )

        # Tickets show
        show_parser = subparsers.add_parser("show", help="Show ticket details")
        show_parser.add_argument(
            "ticket",
            nargs="?",
            metavar="TICKET",
            help="Ticket to act on: InnoDay's numeric id (1380) or the "
            "board's own key (BPAI-402, case-insensitive)",
        )
        _add_deprecated_ticket_id_flag(show_parser)
        show_parser.add_argument(
            "--with-comments", action="store_true", help="Include comments"
        )
        # A ticket's summary history lives here rather than behind a
        # `summary ticket <id>` verb (PF-398): "what have the standups said
        # about this?" is asked while looking at the ticket, so it belongs on
        # the command someone is already running, not in a second place they
        # have to know exists.
        show_parser.add_argument(
            "--with-summaries",
            action="store_true",
            help="Include the summary lines that have mentioned this ticket",
        )

        # Tickets create
        create_parser = subparsers.add_parser("create", help="Create new ticket")
        create_parser.add_argument("title", help="Ticket title")
        create_parser.add_argument("--description", help="Ticket description")
        create_parser.add_argument("--assignee", help="Assign to user")
        create_parser.add_argument(
            "--project",
            help="Project ID to attach this ticket to (defaults to the "
            "project resolved from cwd's .innoday/project.yml, if any)",
        )
        create_parser.add_argument(
            "--status",
            choices=STATUS_CHOICES,
            metavar="STATUS",
            default="TODO",
            help=f"Initial status: {STATUS_NAMES} (default: TODO)",
        )
        # No argparse `choices`: the vocabulary is live data. A list built at
        # parser-construction time runs before any org or project is resolved and
        # before a single HTTP call, so it could only ever be a hardcoded guess at
        # another project's release names. The check is in the handler, against
        # the releases endpoint. (This also sidesteps the `default=` bypasses
        # `type=` trap -- there is no default.)
        create_parser.add_argument(
            "--release",
            metavar="VERSION",
            help="Plan this ticket into one of the project's outstanding "
            "releases, or 'current' for the version being cut",
        )
        create_parser.add_argument(
            "--from-file",
            metavar="FILE",
            help="Create tickets from file (one per line)",
        )
        create_parser.add_argument(
            "--from-stdin",
            action="store_true",
            help="Create tickets from stdin (one per line)",
        )

        # Tickets update
        update_parser = subparsers.add_parser("update", help="Update existing ticket")
        update_parser.add_argument(
            "ticket",
            nargs="?",
            metavar="TICKET",
            help="Ticket to act on: InnoDay's numeric id (1380) or the "
            "board's own key (BPAI-402, case-insensitive)",
        )
        _add_deprecated_ticket_id_flag(update_parser)
        update_parser.add_argument("--title", help="New title")
        update_parser.add_argument("--description", help="New description")
        update_parser.add_argument("--assignee", help="New assignee")
        update_parser.add_argument(
            "--project", help="New project ID to attach this ticket to"
        )
        update_parser.add_argument(
            "--status",
            choices=STATUS_CHOICES,
            metavar="STATUS",
            help=f"New status: {STATUS_NAMES}",
        )
        update_parser.add_argument(
            "--release",
            metavar="VERSION",
            help="Move this ticket to one of the project's outstanding releases, "
            "or 'current' for the version being cut",
        )

        # Tickets assign (convenience command)
        assign_parser = subparsers.add_parser("assign", help="Assign ticket to user")
        assign_parser.add_argument(
            "ticket",
            nargs="?",
            metavar="TICKET",
            help="Ticket to act on: InnoDay's numeric id (1380) or the "
            "board's own key (BPAI-402, case-insensitive)",
        )
        _add_deprecated_ticket_id_flag(assign_parser)
        assign_parser.add_argument("assignee", help="User to assign to")

        # Tickets close (convenience command)
        close_parser = subparsers.add_parser("close", help="Mark ticket as done")
        close_parser.add_argument(
            "ticket",
            nargs="?",
            metavar="TICKET",
            help="Ticket to act on: InnoDay's numeric id (1380) or the "
            "board's own key (BPAI-402, case-insensitive)",
        )
        _add_deprecated_ticket_id_flag(close_parser)

        # Tickets cancel (soft-cancel; "delete" is kept as an alias since
        # tickets are never hard-deleted -- see GH #291)
        for cmd_name, cmd_help in (
            ("cancel", "Cancel ticket (soft -- sets status to CANCELLED)"),
            ("delete", "Alias for 'cancel' -- tickets are never hard-deleted"),
        ):
            cancel_parser = subparsers.add_parser(cmd_name, help=cmd_help)
            cancel_parser.add_argument("ticket_id", help="Ticket ID")
            cancel_parser.add_argument(
                "--note",
                help="Reason for cancelling (required -- prompted if omitted)",
            )
            cancel_parser.add_argument(
                "--confirm", action="store_true", help="Skip confirmation prompt"
            )

        # Tickets comment
        # tickets attach-pr / detach-pr
        attach_parser = subparsers.add_parser(
            "attach-pr",
            help="Attach a pull request to a ticket by hand",
            description=(
                "Record that a pull request delivered a ticket, when the pull "
                "request does not say so itself. Every other link is derived "
                "from the branch, the title, then the description -- this is "
                "for the work that names its ticket in none of them. A release "
                "summary proposes the match; this is where your agreement is "
                "written down."
            ),
        )
        attach_parser.add_argument(
            "--ticket",
            required=True,
            metavar="REF",
            help="Ticket reference as the summary printed it, e.g. BPAI-417",
        )
        attach_parser.add_argument(
            "--repo", required=True, help="Repository name, e.g. bps-api"
        )
        attach_parser.add_argument(
            "--pr",
            required=True,
            type=int,
            metavar="NUMBER",
            help="Pull request number",
        )

        detach_parser = subparsers.add_parser(
            "detach-pr",
            help="Undo a hand-made pull request attachment",
            description=(
                "Clears the manual link only. A pull request whose branch names "
                "its ticket goes on matching afterwards."
            ),
        )
        detach_parser.add_argument("--repo", required=True, help="Repository name")
        detach_parser.add_argument("--pr", required=True, type=int, metavar="NUMBER")

        comment_parser = subparsers.add_parser("comment", help="Add comment to ticket")
        comment_parser.add_argument(
            "ticket",
            nargs="?",
            metavar="TICKET",
            help="Ticket to act on: InnoDay's numeric id (1380) or the "
            "board's own key (BPAI-402, case-insensitive)",
        )
        _add_deprecated_ticket_id_flag(comment_parser)
        comment_parser.add_argument("comment", help="Comment text")
        comment_parser.add_argument(
            "--author",
            help="Commenter user ID (default: current configured user's ID)",
        )

        # Tickets comments
        comments_parser = subparsers.add_parser("comments", help="List ticket comments")
        comments_parser.add_argument(
            "ticket",
            nargs="?",
            metavar="TICKET",
            help="Ticket to act on: InnoDay's numeric id (1380) or the "
            "board's own key (BPAI-402, case-insensitive)",
        )
        _add_deprecated_ticket_id_flag(comments_parser)

    @staticmethod
    async def execute(args: argparse.Namespace, config) -> int:
        """Execute ticket command."""
        command = getattr(args, "ticket_command", None)

        # One place resolves "which ticket", so no handler has to know that the id
        # arrives two ways. The positional wins when both are given; the
        # deprecated `--ticket-id` still works. Handlers keep reading
        # `args.ticket_id`, so this is the whole of the change for them.
        #
        # A board key (BPAI-402) is passed through untouched -- the API resolves
        # it, so every client gets the same vocabulary rather than each one
        # growing its own lookup.
        ticket_ref = getattr(args, "ticket", None) or getattr(
            args, "ticket_id_flag", None
        )
        if ticket_ref:
            args.ticket_id = ticket_ref
        elif hasattr(args, "ticket") or hasattr(args, "ticket_id_flag"):
            console.print(
                format_error(
                    "No ticket given. Pass the ticket as the first argument -- "
                    "its InnoDay id (1380) or its board key (BPAI-402)."
                )
            )
            return 1

        # Check organization is configured
        if not config.get_current_organization():
            console.print(
                format_error(
                    "Organization not configured. Run 'innoday config init' first."
                )
            )
            return 1

        # Create formatter
        formatter = OutputFormatter(
            format_type=getattr(args, "format", None) or config.get_output_format(),
            color_enabled=config.is_color_enabled(),
        )

        # Execute command
        async with InnoDayAPIClient(config) as client:
            try:
                if command == "list":
                    return await TicketCommands._handle_list(args, client, formatter)
                elif command == "show":
                    return await TicketCommands._handle_show(args, client, formatter)
                elif command == "create":
                    return await TicketCommands._handle_create(args, client, formatter)
                elif command == "update":
                    return await TicketCommands._handle_update(args, client, formatter)
                elif command == "assign":
                    return await TicketCommands._handle_assign(args, client, formatter)
                elif command == "close":
                    return await TicketCommands._handle_close(args, client, formatter)
                elif command in ("cancel", "delete"):
                    return await TicketCommands._handle_cancel(args, client, formatter)
                elif command == "comment":
                    return await TicketCommands._handle_comment(args, client, formatter)
                elif command == "comments":
                    return await TicketCommands._handle_comments(
                        args, client, formatter
                    )
                elif command in ("attach-pr", "detach-pr"):
                    return await TicketCommands._handle_pr_link(
                        args, client, attach=command == "attach-pr"
                    )
                else:
                    console.print(format_error("No ticket command specified"))
                    console.print(
                        "[dim]Available: list, show, create, update, assign, close, "
                        "cancel, comment, comments, attach-pr, detach-pr — "
                        "run 'innoday tickets "
                        "--help' for details[/dim]"
                    )
                    return 1

            except APIError as e:
                console.print(format_error(str(e)))
                return 1

    @staticmethod
    async def _handle_pr_link(args, client, *, attach: bool) -> int:
        """Attach or detach one pull request, by hand.

        The counterpart to a release summary's proposal. The summary works out
        which ticket an unlinked pull request probably delivered and prints the
        command; running it is the confirmation, and nothing is written until
        somebody does.
        """
        org_id = client.organization_id
        project_id = client.project_id
        if not org_id or not project_id:
            console.print(
                format_error(
                    "No project in context. Run from a project workspace, or "
                    "pass --project: a pull request is attached to a ticket on "
                    "one project."
                )
            )
            return 1

        path = (
            f"/organizations/{org_id}/projects/{project_id}"
            f"/pull-requests/{args.repo}/{args.pr}/ticket"
        )
        try:
            if attach:
                response = await client.put(path, json={"ticket_ref": args.ticket})
            else:
                response = await client.delete(path)
        except APIError as exc:
            console.print(format_error(str(exc)))
            return 1

        if response.status_code not in (200, 201):
            detail = ""
            try:
                detail = response.json().get("detail", "")
            except Exception:  # noqa: BLE001
                detail = getattr(response, "text", "")
            console.print(format_error(detail or f"HTTP {response.status_code}"))
            return 1

        body = response.json()
        if attach:
            console.print(
                format_success(
                    f"{body['repo']}#{body['number']} → {body['ticket_ref']} "
                    f"({body.get('title') or ''})"
                )
            )
            console.print(
                "[dim]It will appear under that ticket in the next release "
                "summary. Undo with `innoday tickets detach-pr`.[/dim]"
            )
        else:
            console.print(format_success(f"{body['repo']}#{body['number']} detached."))
            console.print(
                "[dim]Derivation takes over again: if its branch names a "
                "ticket, it still matches.[/dim]"
            )
        return 0

    @staticmethod
    async def _handle_list(
        args: argparse.Namespace, client: InnoDayAPIClient, formatter: OutputFormatter
    ) -> int:
        """Handle tickets list command."""
        all_projects = getattr(args, "all_projects", False)

        with ProgressReporter("Loading tickets..."):
            tickets = await client.list_tickets(
                status=getattr(args, "status", None),
                assignee=getattr(args, "assignee", None),
                all_projects=all_projects,
            )

        # Say which scope produced the list. Silence here is what let an
        # org-wide answer pass for a project-scoped one.
        if client.project_id and not all_projects:
            advisory_console.print(
                format_info(
                    f"Scoped to project {client.project_id} "
                    "-- pass --all-projects for the whole organization"
                )
            )

        formatter.format_tickets(tickets)
        return 0

    @staticmethod
    async def _handle_show(
        args: argparse.Namespace, client: InnoDayAPIClient, formatter: OutputFormatter
    ) -> int:
        """Handle tickets show command."""
        with ProgressReporter(f"Loading ticket {args.ticket_id}..."):
            ticket = await client.get_ticket(args.ticket_id)

            # Load comments if requested
            if args.with_comments:
                comments = await client.get_comments(args.ticket_id)
                ticket["comments"] = comments

        formatter.format_ticket(ticket, with_comments=args.with_comments)

        if getattr(args, "with_summaries", False):
            # Not under `--format json`. This prints free text, and it ran
            # *after* `format_ticket` had already emitted a complete JSON
            # document -- so the output was valid JSON followed by prose, which
            # no parser will accept. A person still gets it in table mode.
            if formatter.format_type == "json":
                advisory_console.print(
                    format_info(
                        "--with-summaries prints prose and is omitted under "
                        "--format json; run without --format json to read it"
                    )
                )
            else:
                await TicketCommands._print_summary_history(args.ticket_id, client)
        return 0

    @staticmethod
    async def _print_summary_history(ticket_id, client: InnoDayAPIClient) -> None:
        """Every summary line that has mentioned this ticket, newest first.

        Best-effort: a ticket's own detail is the thing that was asked for, so
        a failure to fetch its narration history prints a note and leaves the
        ticket on screen rather than failing the command.
        """
        from rich.markup import escape

        organization_id = client.organization_id
        if not organization_id:
            return
        try:
            response = await client.get(
                f"/organizations/{organization_id}/tickets/{ticket_id}/summary-items"
            )
        except APIError as exc:
            console.print(format_warning(f"Could not load summary history: {exc}"))
            return
        if response.status_code != 200:
            console.print(
                format_warning(
                    f"Could not load summary history (HTTP {response.status_code})."
                )
            )
            return

        items = (response.json() or {}).get("items") or []
        if not items:
            console.print("\n[dim]No summary has mentioned this ticket yet.[/dim]")
            return

        console.print("\n[bold]Summary history[/bold]")
        for item in items:
            when = str(item.get("summary_created_at") or "")[:16].replace("T", " ")
            window = item.get("window_spec") or ""
            kind = item.get("summary_type") or ""
            console.print(
                f"  [dim]{escape(when)} · {escape(str(kind))}"
                f"{' · ' + escape(str(window)) if window else ''}[/dim]"
            )
            body = item.get("body_markdown")
            if body:
                for prose in str(body).strip().splitlines():
                    console.print(f"    {escape(prose)}")

    @staticmethod
    async def _outstanding_releases(
        client: InnoDayAPIClient, project_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """The project's outstanding releases, best-first, or ``None`` if unread.

        One call to the existing releases endpoint -- there is no
        `outstanding=true` filter and this does not need one. What it *does* need
        is a **re-sort**: the endpoint orders by `Release.version DESC`, a *string*
        sort, which puts `v1.10.0` before `v1.9.0`. That is the exact bug
        `semver_key` exists to fix, so the list is reordered here rather than
        printed in the wrong order.

        ``None`` (rather than an empty list) when the list could not be read, so
        the caller can tell "nothing is outstanding" from "we do not know" and let
        the API be the judge instead of blocking a write on a picker fetch.
        """
        try:
            response = await client.get(
                f"/organizations/{client.organization_id}/releases",
                params={"project_id": project_id},
            )
        except Exception:  # noqa: BLE001 -- a picker fetch must not fail a write
            return None
        if response.status_code != 200:
            return None
        try:
            rows = response.json()
        except ValueError:
            return None

        outstanding = [row for row in rows if row.get("status") in _OUTSTANDING_RANK]
        outstanding.sort(
            key=lambda row: (
                _OUTSTANDING_RANK[row["status"]],
                semver_key(str(row.get("version", ""))),
            )
        )
        return outstanding

    @staticmethod
    def _print_release_options(options: List[Dict[str, Any]]) -> None:
        console.print("\n[bold]Outstanding releases:[/bold]")
        for row in options:
            note = (
                "  (cutting now)"
                if row["status"] == OUTSTANDING_STATUSES[0].value
                else ""
            )
            console.print(f"  {row['version']}   {row['status']}{note}")

    @staticmethod
    async def _resolve_release(
        client: InnoDayAPIClient, project_id: str, requested: str
    ) -> Optional[str]:
        """The version to send, or ``None`` meaning "stop, write nothing".

        A pre-flight, not a second implementation of the rule: the API validates
        this too, and its answer is authoritative. What the pre-flight buys is the
        *list* -- a bare 422 tells someone their version is wrong, this tells them
        which versions are right, before anything has been created.
        """
        # The API strips before matching, so strip here too -- otherwise
        # `--release " v1.11.0 "` fails the pre-flight against an option list that
        # does not contain the padded form, while the API would have accepted it.
        requested = requested.strip()

        if requested == CURRENT_RELEASE:
            # Resolved server-side, by the same helper the `?release=` filter
            # uses. Reimplementing it here is how the two come to disagree.
            return requested

        options = await TicketCommands._outstanding_releases(client, project_id)
        if options is None:
            # Could not read the list. Send it and let the API answer -- failing
            # the write on a failed picker fetch would be worse than a 422.
            return requested

        if any(row["version"] == requested for row in options):
            return requested

        if not options:
            console.print(
                format_error(
                    "This project has no outstanding releases to assign a ticket to"
                )
            )
            console.print(
                format_info("Create one first:  innoday releases create <version>")
            )
            return None

        console.print(
            format_error(
                f"'{requested}' is not an outstanding release for this project"
            )
        )
        TicketCommands._print_release_options(options)

        if not sys.stdin.isatty():
            # Non-interactive: print and stop, so a script fails loudly rather
            # than quietly creating a ticket on the wrong version.
            console.print(
                format_info(
                    f"Pass one of those, --release {CURRENT_RELEASE} for the "
                    "version being cut, or create a new release first:  "
                    f"innoday releases create {requested}"
                )
            )
            return None

        console.print()
        choice = Prompt.ask(
            "Pick a release",
            choices=[row["version"] for row in options] + ["cancel"],
            default=options[0]["version"],
        )
        return None if choice == "cancel" else choice

    @staticmethod
    async def _handle_create(
        args: argparse.Namespace, client: InnoDayAPIClient, formatter: OutputFormatter
    ) -> int:
        """Handle tickets create command."""
        tickets_to_create = []

        # Handle different input sources
        if args.from_file:
            try:
                with open(args.from_file, "r") as f:
                    tickets_to_create = [line.strip() for line in f if line.strip()]
            except IOError as e:
                console.print(
                    format_error(f"Could not read file {args.from_file}: {e}")
                )
                return 1

        elif args.from_stdin:
            console.print(
                "[dim]Enter ticket titles (one per line), Ctrl+D when done:[/dim]"
            )
            try:
                tickets_to_create = [line.strip() for line in sys.stdin if line.strip()]
            except KeyboardInterrupt:
                console.print("\nCancelled")
                return 0

        else:
            # Single ticket from arguments
            tickets_to_create = [args.title]

        if not tickets_to_create:
            console.print(format_warning("No tickets to create"))
            return 0

        # Create tickets
        created_tickets = []

        project_id = getattr(args, "project", None) or client.project_id
        if not project_id:
            console.print(format_error("No project specified"))
            console.print(
                format_info(
                    "Pass --project, or run this command from inside "
                    "a project directory (one with .innoday/project.yml) "
                    "-- a ticket must belong to a project"
                )
            )
            return 1

        # Checked once, before the loop: `--from-file` creates many tickets and
        # they all carry the same release, so an invalid value must not create the
        # first ninety-nine and then fail.
        release = None
        if getattr(args, "release", None):
            release = await TicketCommands._resolve_release(
                client, project_id, args.release
            )
            if release is None:
                return 1

        for title in tickets_to_create:
            ticket_data = {
                "summary": title,
                "description": args.description or "",
                "status": args.status,
                "assignee": args.assignee,
                "project_id": project_id,
                "release": release,
            }

            # Remove None values
            ticket_data = {k: v for k, v in ticket_data.items() if v is not None}

            try:
                with ProgressReporter(f"Creating ticket: {title[:30]}..."):
                    ticket = await client.create_ticket(ticket_data)
                    created_tickets.append(ticket)

            except APIError as e:
                console.print(format_error(f"Failed to create ticket '{title}': {e}"))
                continue

        # Display results
        if created_tickets:
            console.print(format_success(f"Created {len(created_tickets)} ticket(s)"))
            if len(created_tickets) == 1:
                formatter.format_ticket(created_tickets[0])
            else:
                formatter.format_tickets(created_tickets)

        return 0 if created_tickets else 1

    @staticmethod
    async def _handle_update(
        args: argparse.Namespace, client: InnoDayAPIClient, formatter: OutputFormatter
    ) -> int:
        """Handle tickets update command."""
        # Build update data
        update_data = {}
        if args.title:
            update_data["summary"] = args.title
        if args.description:
            update_data["description"] = args.description
        if args.assignee:
            update_data["assignee"] = args.assignee
        if args.status:
            update_data["status"] = args.status
        if getattr(args, "project", None):
            update_data["project_id"] = args.project
        if args.release is not None and not args.release.strip():
            # `--release ""` clears the field. Guarding on truthiness instead of
            # `is not None` swallowed this: argparse defaults to None, so the two
            # differ for the empty string ONLY -- every other invocation is
            # unaffected. The API and MCP both accept "" as a clear, so a CLI that
            # cannot express it is the odd one out. Not validated, deliberately:
            # removing a ticket from a release must not require naming a valid one.
            update_data["release"] = ""
        elif args.release:
            # Validate against the project the ticket will belong to AFTER this
            # call: an explicit --project (a move) wins, otherwise the ticket's
            # OWN project -- deliberately not the cwd's.
            #
            # This used to read `args.project or client.project_id`, which was
            # wrong in two directions at once: updating a ticket that lives in
            # project B while standing in project A's directory rejected a legal
            # version and printed *A's* option list, and running outside any
            # project directory refused the write entirely -- a command that
            # worked before --release existed.
            project_id = getattr(args, "project", None)
            if not project_id:
                try:
                    ticket = await client.get_ticket(args.ticket_id)
                    project_id = (ticket or {}).get("project_id")
                except Exception:
                    project_id = None

            if not project_id:
                # Could not learn the ticket's project. Send it and let the API's
                # 422 be authoritative -- same call the failed-picker-fetch branch
                # in _resolve_release makes. A false rejection is worse than a
                # round trip, and the server validates this regardless.
                update_data["release"] = args.release.strip()
            else:
                release = await TicketCommands._resolve_release(
                    client, project_id, args.release
                )
                if release is None:
                    return 1
                update_data["release"] = release

        if not update_data:
            console.print(format_warning("No updates specified"))
            return 0

        with ProgressReporter(f"Updating ticket {args.ticket_id}..."):
            ticket = await client.update_ticket(args.ticket_id, update_data)

        console.print(format_success(f"Updated ticket {args.ticket_id}"))
        formatter.format_ticket(ticket)
        return 0

    @staticmethod
    async def _handle_assign(
        args: argparse.Namespace, client: InnoDayAPIClient, formatter: OutputFormatter
    ) -> int:
        """Handle tickets assign command."""
        update_data = {"assignee": args.assignee}

        with ProgressReporter(
            f"Assigning ticket {args.ticket_id} to {args.assignee}..."
        ):
            await client.update_ticket(args.ticket_id, update_data)

        console.print(
            format_success(f"Assigned ticket {args.ticket_id} to {args.assignee}")
        )
        return 0

    @staticmethod
    async def _handle_close(
        args: argparse.Namespace, client: InnoDayAPIClient, formatter: OutputFormatter
    ) -> int:
        """Handle tickets close command."""
        update_data = {"status": "DONE"}

        with ProgressReporter(f"Closing ticket {args.ticket_id}..."):
            await client.update_ticket(args.ticket_id, update_data)

        console.print(format_success(f"Closed ticket {args.ticket_id}"))
        return 0

    @staticmethod
    async def _handle_cancel(
        args: argparse.Namespace, client: InnoDayAPIClient, formatter: OutputFormatter
    ) -> int:
        """Handle tickets cancel command (soft-cancel; 'delete' is an alias).

        A note is mandatory -- prompted interactively if not passed via
        --note, and rejected if left blank. Tickets are never hard-deleted,
        only marked CANCELLED with the note recorded as a comment (GH #291).
        """
        note = args.note
        if not note:
            note = Prompt.ask(f"Reason for cancelling ticket {args.ticket_id}")
        note = (note or "").strip()
        if not note:
            console.print(format_error("A note is required to cancel a ticket"))
            return 1

        if not args.confirm:
            if not Confirm.ask(f"Cancel ticket {args.ticket_id}?"):
                console.print("Cancellation aborted")
                return 0

        with ProgressReporter(f"Cancelling ticket {args.ticket_id}..."):
            await client.cancel_ticket(args.ticket_id, note)

        console.print(format_success(f"Cancelled ticket {args.ticket_id}"))
        return 0

    @staticmethod
    async def _handle_comment(
        args: argparse.Namespace, client: InnoDayAPIClient, formatter: OutputFormatter
    ) -> int:
        """Handle tickets comment command."""
        # API's CommentCreate model requires comment/commenter_id (not
        # content/author -- these field names must match exactly, see
        # src/routers/tickets.py's CommentCreate). commenter_id defaults to
        # the resolved current user, matching the server's own fallback to
        # current_user.id when it's omitted -- --author lets a caller
        # attribute the comment to a different user id explicitly.
        commenter_id = args.author or client.user_id
        if not commenter_id:
            console.print(
                format_error(
                    "No commenter identity available — pass --author <user-id> "
                    "or configure a current user (innoday init)"
                )
            )
            return 1

        comment_data = {"comment": args.comment, "commenter_id": commenter_id}

        with ProgressReporter(f"Adding comment to ticket {args.ticket_id}..."):
            await client.add_comment(args.ticket_id, comment_data)

        console.print(format_success(f"Added comment to ticket {args.ticket_id}"))
        return 0

    @staticmethod
    async def _handle_comments(
        args: argparse.Namespace, client: InnoDayAPIClient, formatter: OutputFormatter
    ) -> int:
        """Handle tickets comments command."""
        with ProgressReporter(f"Loading comments for ticket {args.ticket_id}..."):
            comments = await client.get_comments(args.ticket_id)

        formatter.format_comments(comments)
        return 0
