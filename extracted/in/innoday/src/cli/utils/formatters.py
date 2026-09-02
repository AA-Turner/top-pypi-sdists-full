"""
InnoDay CLI Output Formatters

Beautiful terminal output formatting using Rich library.
"""

import csv
import io
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text


def format_error(message: str) -> str:
    """Format error message with color."""
    return f"[red]✗ {message}[/red]"


def describe_error(exc: BaseException) -> str:
    """An exception as something a person can act on. Never an empty string.

    ``str(exc)`` is empty for a whole family of exceptions, and the CLI printed it
    raw in sixteen places -- so a timed-out sync reported:

        ✗ Unexpected error:

    ...with nothing after the colon, on a command that had usually **succeeded**
    server-side. Diagnosing that needed `--verbose` to discover the class name was
    the entire message.

    So: fall back to the class when there is no text, and say what a timeout
    actually means, because the useful advice is not "it failed" but "it may not
    have".
    """
    text = str(exc).strip()
    name = type(exc).__name__

    # httpx's timeouts are the common case here and the ones that mislead: the
    # request kept going after the client stopped waiting. Matched by name rather
    # than by import so this module stays free of an HTTP dependency, and so it
    # also covers the equivalents from any other client.
    if "Timeout" in name:
        detail = f"{name}: {text}" if text else name
        return (
            f"the request timed out ({detail}). The server may have completed it "
            "anyway -- check the result before retrying."
        )

    if not text:
        return f"{name} (no message)"
    return f"{name}: {text}" if name not in text else text


def enum_key(value: str) -> str:
    """Normalise an enum value or name to the form used as a style-map key.

    Domain enums are ``str, Enum`` with **lowercase values**, while Postgres
    stores the enum **name**, so the same status reaches the CLI as either
    ``"in progress"`` (from the API) or ``"IN_PROGRESS"`` (read from the
    database). Some values also contain a space where the name has an
    underscore -- ``TicketStatus.IN_PROGRESS`` is literally ``"in progress"`` --
    so upper-casing alone is not enough: ``"in progress".upper()`` is
    ``"IN PROGRESS"``, which matched no key and silently fell through to the
    default style. `in progress` and `in review`, the two most common working
    states, therefore rendered unstyled.
    """
    return str(value).strip().upper().replace(" ", "_").replace("-", "_")


def describe_exception(exc: BaseException) -> str:
    """A never-empty, single-line description of `exc`.

    Plain ``str(exc)`` is empty for any exception raised without arguments, and
    for several stdlib and httpx exceptions whose message lives only in the type.
    Interpolating that into an error template produces output like::

        ✗ Error:
        Use --verbose for more details

    -- observed from `innoday board sync-status`, where the exception type was
    the only actionable detail and it was reachable solely via ``--verbose``.
    Nothing here should ever leave the reader with no information at all.
    """
    message = str(exc).strip()
    name = type(exc).__name__
    if not message:
        return f"{name} (no message)"
    # Keep the type when the message alone would be ambiguous about *what* failed.
    status = getattr(exc, "status_code", None)
    if status:
        return f"{message} (HTTP {status})"
    return message


def format_success(message: str) -> str:
    """Format success message with color."""
    return f"[green]✓ {message}[/green]"


def format_warning(message: str) -> str:
    """Format warning message with color."""
    return f"[yellow]⚠ {message}[/yellow]"


def format_info(message: str) -> str:
    """Format info message with color."""
    return f"[cyan]ℹ {message}[/cyan]"


def format_datetime(dt_str: Union[str, datetime, None]) -> str:
    """Format datetime string for display."""
    if not dt_str:
        return "N/A"

    try:
        if isinstance(dt_str, str):
            # Parse ISO format datetime
            dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        elif isinstance(dt_str, datetime):
            dt = dt_str
        else:
            return str(dt_str)

        # Format as relative time if recent, absolute time if older
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now(timezone.utc)
        delta = now - dt

        if delta.days == 0:
            if delta.seconds < 3600:  # Less than 1 hour
                minutes = delta.seconds // 60
                return f"{minutes}m ago"
            else:
                hours = delta.seconds // 3600
                return f"{hours}h ago"
        elif delta.days == 1:
            return "Yesterday"
        elif delta.days < 7:
            return f"{delta.days}d ago"
        else:
            return dt.strftime("%Y-%m-%d")

    except (ValueError, AttributeError):
        return str(dt_str)


#: Where advisories go: notes about scope, warnings, "nothing found" prose --
#: anything a person needs and a script must not receive.
#:
#: **stdout belongs to the machine.** A scope note printed to stdout lands
#: immediately before `--format json` output and makes the whole stream
#: unparseable, which is exactly how the JSON contract broke. rich sends this to
#: stderr, so a human still sees it in the terminal and `| jq` never does.
advisory_console = Console(stderr=True)


class OutputFormatter:
    """Formats output in various formats (table, json, csv)."""

    def __init__(self, format_type: str = "table", color_enabled: bool = True):
        """Initialize formatter with type and color settings.

        A falsy `format_type` means "nobody chose one" -- the global
        `--format` carries no default now, so a command that passes
        `args.format` straight through gets `None` when the flag was not
        given. Those sites render a table, as they did when argparse supplied
        the "table" itself; the two that consult the profile's
        `output.format` do so before calling this.
        """
        self.format_type = format_type or "table"
        self.color_enabled = color_enabled
        self.console = Console(color_system="auto" if color_enabled else None)

    def format_tickets(self, tickets: List[Dict[str, Any]]) -> None:
        """Format and display tickets."""
        if not tickets:
            # An empty answer is still an answer, and in JSON it has to be
            # spelled `[]`. Printing prose here meant a caller parsing the
            # output crashed on "no tickets found" rather than reading zero
            # tickets -- the failure mode looked like a broken CLI.
            if self.format_type == "json":
                self._print_json([])
                return
            self.console.print("[yellow]No tickets found[/yellow]")
            return

        if self.format_type == "json":
            self._print_json(tickets)
        elif self.format_type == "csv":
            self._print_csv(
                tickets, ["id", "summary", "status", "assignee", "created_at"]
            )
        else:  # table
            self._print_tickets_table(tickets)

    def format_ticket(
        self, ticket: Dict[str, Any], with_comments: bool = False
    ) -> None:
        """Format and display a single ticket with details."""
        if self.format_type == "json":
            self._print_json(ticket)
            return

        # Rich table format for single ticket
        self._print_ticket_details(ticket, with_comments)

    def format_comments(self, comments: List[Dict[str, Any]]) -> None:
        """Format and display ticket comments."""
        if not comments:
            if self.format_type == "json":
                self._print_json([])
                return
            self.console.print("[yellow]No comments found[/yellow]")
            return

        if self.format_type == "json":
            self._print_json(comments)
        elif self.format_type == "csv":
            self._print_csv(comments, ["id", "author", "content", "created_at"])
        else:  # table
            self._print_comments_table(comments)

    def format_status(self, status_data: Dict[str, Any]) -> None:
        """Format and display system status."""
        if self.format_type == "json":
            self._print_json(status_data)
            return

        self._print_status_panel(status_data)

    def format_config(self, config_data: Dict[str, Any]) -> None:
        """Format and display configuration."""
        if self.format_type == "json":
            self._print_json(config_data)
            return

        # Config is already handled by CLIConfig.display_config()

    def _print_json(self, data: Union[Dict, List]) -> None:
        """Print data as JSON, to stdout, with nothing else in it.

        **Never through rich.** This used to render the JSON as a highlighted
        `Syntax` block whenever colour was on, and rich pads every line out to
        the console width and wraps anything longer. The result was not JSON:
        `json.loads` failed on it, so `--format json` -- the whole point of
        which is to be read by something other than a person -- could not be
        parsed by a script unless the caller happened to force the terminal
        width wide enough to avoid a wrap.

        Colour would be a nice thing to have and is not worth a broken
        contract. Anyone who wants highlighting has `| jq`, which also gets the
        indentation right.
        """
        print(json.dumps(data, indent=2, default=str))

    def _print_csv(self, data: List[Dict[str, Any]], fields: List[str]) -> None:
        """Print data as CSV."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()

        for item in data:
            # Convert datetime objects to strings
            row = {}
            for field in fields:
                value = item.get(field, "")
                if isinstance(value, datetime):
                    value = value.isoformat()
                row[field] = value
            writer.writerow(row)

        print(output.getvalue().strip())

    def _print_tickets_table(self, tickets: List[Dict[str, Any]]) -> None:
        """Print tickets as a Rich table."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", width=8)
        table.add_column("Title", style="white", min_width=30)
        table.add_column("Status", style="yellow", width=12)
        table.add_column("Assignee", style="green", width=15)
        table.add_column("Created", style="blue", width=12)

        for ticket in tickets:
            # Format status with color
            status = ticket.get("status", "UNKNOWN")
            status_style = self._get_status_style(status)

            # Format creation date
            created_at = ticket.get("created_at", "")
            if isinstance(created_at, str) and created_at:
                try:
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    created_display = dt.strftime("%Y-%m-%d")
                except Exception:
                    created_display = created_at[:10]
            else:
                created_display = "Unknown"

            # API field is "summary", not "title" (Ticket.summary in the
            # domain model) -- this table was reading a field that never
            # existed on the response, always rendering an empty column.
            title = ticket.get("summary") or ""
            table.add_row(
                str(ticket.get("id", "")),
                title[:50] + ("..." if len(title) > 50 else ""),
                f"[{status_style}]{status}[/{status_style}]",
                ticket.get("assignee") or "Unassigned",
                created_display,
            )

        self.console.print(table)
        self.console.print(f"\n[dim]Total: {len(tickets)} tickets[/dim]")

    def _print_ticket_details(
        self, ticket: Dict[str, Any], with_comments: bool = False
    ) -> None:
        """Print detailed ticket information."""
        # Main ticket panel -- API field is "summary", not "title"
        title = ticket.get("summary") or "Untitled"
        status = ticket.get("status", "UNKNOWN")
        status_style = self._get_status_style(status)

        # Create ticket info table
        info_table = Table.grid(padding=1)
        info_table.add_column(style="bold cyan", justify="right")
        info_table.add_column(style="white")

        info_table.add_row("ID:", str(ticket.get("id", "")))
        # The board's own key (BPAI-402) alongside InnoDay's integer id. Both are
        # "the ticket id" in conversation, only one of them is what `--ticket-id`
        # takes, and the panel used to show just the integer -- so the key you had
        # in front of you was never the one on screen.
        if ticket.get("external_ticket_id"):
            info_table.add_row("Key:", str(ticket["external_ticket_id"]))
        info_table.add_row("Status:", f"[{status_style}]{status}[/{status_style}]")
        # Which release this ticket is planned into. Absent from this panel until
        # now, which made the field effectively invisible from the CLI: you could
        # set it with `tickets update --release` and had no way to read it back.
        info_table.add_row("Release:", ticket.get("release") or "Not planned")
        info_table.add_row("Assignee:", ticket.get("assignee") or "Unassigned")
        info_table.add_row("Created:", self._format_datetime(ticket.get("created_at")))
        info_table.add_row("Updated:", self._format_datetime(ticket.get("updated_at")))

        if ticket.get("url"):
            info_table.add_row("URL:", ticket["url"])

        # Description
        description = ticket.get("description") or "No description"

        # **A Rich renderable cannot be interpolated into a string.** The f-string
        # this replaces called `str()` on the Table, so every `tickets show` and
        # every `tickets create` printed a literal
        # "<rich.table.Table object at 0x...>" where the ticket's fields belonged.
        # Group composes renderables; formatting is Rich's job, not str()'s.
        panel_content = Group(
            info_table,
            Text(""),
            Text.from_markup("[bold]Description:[/bold]"),
            Text(str(description)),
        )

        panel = Panel(
            panel_content,
            title=f"[bold white]{title}[/bold white]",
            border_style="blue",
        )

        self.console.print(panel)

        # Comments if requested
        if with_comments and ticket.get("comments"):
            self._print_comments_section(ticket["comments"])

    def _print_comments_table(self, comments: List[Dict[str, Any]]) -> None:
        """Print comments as a Rich table."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Author", style="cyan", width=15)
        table.add_column("Comment", style="white", min_width=40)
        table.add_column("Date", style="blue", width=12)

        for comment in comments:
            content = comment.get("content", "")
            # Truncate long comments
            if len(content) > 60:
                content = content[:57] + "..."

            table.add_row(
                comment.get("author", "Unknown"),
                content,
                self._format_datetime(comment.get("created_at")),
            )

        self.console.print(table)

    def _print_comments_section(self, comments: List[Dict[str, Any]]) -> None:
        """Print comments section for ticket details."""
        if not comments:
            self.console.print("\n[dim]No comments[/dim]")
            return

        self.console.print(f"\n[bold]Comments ({len(comments)}):[/bold]")

        for i, comment in enumerate(comments):
            author = comment.get("author", "Unknown")
            content = comment.get("content", "")
            created = self._format_datetime(comment.get("created_at"))

            comment_panel = Panel(
                content,
                title=f"[bold]{author}[/bold] - {created}",
                border_style="dim",
                padding=(0, 1),
            )
            self.console.print(comment_panel)

    def _print_status_panel(self, status_data: Dict[str, Any]) -> None:
        """Print system status as a Rich panel."""
        table = Table.grid(padding=1)
        table.add_column(style="bold cyan", justify="right")
        table.add_column(style="white")

        # API Status
        api_status = status_data.get("api_status", "unknown")
        api_style = "green" if api_status == "healthy" else "red"
        table.add_row("API Status:", f"[{api_style}]{api_status.upper()}[/{api_style}]")

        # URLs
        if status_data.get("api_url"):
            table.add_row("API URL:", status_data["api_url"])

        # Client ID
        if status_data.get("client_id"):
            table.add_row("Client ID:", status_data["client_id"])

        panel = Panel(
            table,
            title="[bold blue]InnoDay System Status[/bold blue]",
            border_style="blue",
        )

        self.console.print(panel)

    def _get_status_style(self, status: str) -> str:
        """Get Rich style for ticket status."""
        status_styles = {
            "DRAFT": "dim",
            "BACKLOG": "dim",
            "TODO": "blue",
            "IN_PROGRESS": "yellow",
            "IN_REVIEW": "magenta",
            "DONE": "green",
            "CANCELLED": "red",
        }
        return status_styles.get(enum_key(status), "white")

    def _format_datetime(self, dt_str: Optional[str]) -> str:
        """Format datetime string for display."""
        if not dt_str:
            return "Unknown"

        try:
            dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M")
        # `Exception`, not a narrower tuple: this was a bare `except:`, which also
        # swallowed KeyboardInterrupt -- Ctrl-C did nothing inside the display
        # loops that call this. Excluding BaseException fixes that. Narrowing to
        # (ValueError, TypeError) would additionally change which ordinary
        # failures are tolerated: `dt_str` is never type-checked, so a non-string
        # raises AttributeError here, which used to be caught.
        except Exception:
            return dt_str[:16] if len(dt_str) > 16 else dt_str

    def format_organizations(
        self, organizations: List[Dict[str, Any]], show_members: bool = False
    ) -> None:
        """Format and display organizations."""
        if not organizations:
            # An empty answer is still an answer, and in JSON it is spelled
            # `[]`. Prose here made a caller parsing the output crash rather
            # than read zero rows -- a working CLI looking broken. The skills
            # that shell out to `--format json` hit this on a fresh account.
            if self.format_type == "json":
                self._print_json([])
                return
            self.console.print("[yellow]No organizations found[/yellow]")
            return

        if self.format_type == "json":
            self._print_json(organizations)
        elif self.format_type == "csv":
            fields = ["id", "name", "alias", "created_at"]
            if show_members:
                fields.append("member_count")
            self._print_csv(organizations, fields)
        else:  # table
            self._print_organizations_table(organizations, show_members)

    def _print_organizations_table(
        self, organizations: List[Dict[str, Any]], show_members: bool = False
    ) -> None:
        """Print organizations as a Rich table."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name", style="white", min_width=20)
        table.add_column("Slug", style="cyan", width=20)
        if show_members:
            table.add_column("Members", style="blue", width=8, justify="right")
        table.add_column("Created", style="dim", width=12)
        table.add_column("Current", style="green", width=8, justify="center")

        for org in organizations:
            is_current = org.get("is_current", False)
            current_marker = "✓" if is_current else ""

            name = org.get("name", "")
            slug = org.get("alias", "")

            # Highlight current organization
            if is_current:
                name = f"[bold green]{name}[/bold green]"
                slug = f"[bold green]{slug}[/bold green]"

            created_at = org.get("created_at", "")
            if isinstance(created_at, str) and created_at:
                try:
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    created_display = dt.strftime("%Y-%m-%d")
                except Exception:
                    created_display = created_at[:10]
            else:
                created_display = "Unknown"

            row = [name, slug]
            if show_members:
                row.append(str(org.get("member_count", "N/A")))
            row.extend([created_display, current_marker])

            table.add_row(*row)

        self.console.print(table)
        self.console.print(f"\n[dim]Total: {len(organizations)} organizations[/dim]")

    def format_organization_details(
        self, org_data: Dict[str, Any], include_stats: bool = False
    ) -> None:
        """Format and display detailed organization information."""
        if self.format_type == "json":
            self._print_json(org_data)
            return

        # Create organization info table
        info_table = Table.grid(padding=1)
        info_table.add_column(style="bold cyan", justify="right")
        info_table.add_column(style="white")

        info_table.add_row("Name:", org_data.get("name", "Unknown"))
        info_table.add_row("Alias:", org_data.get("alias", "Unknown"))
        info_table.add_row("ID:", org_data.get("id", "Unknown"))

        if org_data.get("description"):
            info_table.add_row("Description:", org_data["description"])

        if org_data.get("website"):
            info_table.add_row("Website:", org_data["website"])

        if org_data.get("jira_url"):
            info_table.add_row("Jira:", org_data["jira_url"])

        if org_data.get("github_url"):
            info_table.add_row("GitHub:", org_data["github_url"])

        if org_data.get("trello_url"):
            info_table.add_row("Trello:", org_data["trello_url"])

        info_table.add_row(
            "Created:", self._format_datetime(org_data.get("created_at"))
        )
        info_table.add_row(
            "Updated:", self._format_datetime(org_data.get("updated_at"))
        )

        # Add statistics if requested
        if include_stats and org_data.get("stats"):
            stats = org_data["stats"]
            info_table.add_row("", "")  # Spacer
            info_table.add_row("[bold]Statistics:[/bold]", "")
            info_table.add_row("  Members:", str(stats.get("member_count", 0)))
            info_table.add_row("  Projects:", str(stats.get("project_count", 0)))
            info_table.add_row("  Repositories:", str(stats.get("repository_count", 0)))
            info_table.add_row("  Tickets:", str(stats.get("ticket_count", 0)))

        panel = Panel(
            info_table,
            title=f"[bold white]Organization: {org_data.get('name', 'Unknown')}[/bold white]",
            border_style="blue",
        )

        self.console.print(panel)

    def format_projects(self, projects: List[Dict[str, Any]]) -> None:
        """Format and display projects."""
        if not projects:
            if self.format_type == "json":
                self._print_json([])
                return
            self.console.print("[yellow]No projects found[/yellow]")
            return

        if self.format_type == "json":
            self._print_json(projects)
        elif self.format_type == "csv":
            self._print_csv(
                projects,
                ["id", "name", "alias", "status", "priority", "created_at"],
            )
        else:  # table
            self._print_projects_table(projects)

    def _print_projects_table(self, projects: List[Dict[str, Any]]) -> None:
        """Print projects as a Rich table."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name", style="white", min_width=25)
        table.add_column("Alias", style="cyan", width=20)
        table.add_column("Status", style="yellow", width=12)
        table.add_column("Priority", style="blue", width=10)
        table.add_column("Tags", style="dim", width=20)
        table.add_column("Created", style="dim", width=12)

        for project in projects:
            # Format status with color
            status = project.get("status", "UNKNOWN")
            status_style = self._get_project_status_style(status)

            # Format priority with color
            priority = project.get("priority", "MEDIUM")
            priority_style = self._get_priority_style(priority)

            # Format tags
            tags = project.get("tags", [])
            tags_display = ", ".join(tags[:3]) if tags else ""
            if len(tags) > 3:
                tags_display += "..."

            # Format creation date
            created_at = project.get("created_at", "")
            if isinstance(created_at, str) and created_at:
                try:
                    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    created_display = dt.strftime("%Y-%m-%d")
                except Exception:
                    created_display = created_at[:10]
            else:
                created_display = "Unknown"

            table.add_row(
                project.get("name", "")[:35]
                + ("..." if len(project.get("name", "")) > 35 else ""),
                project.get("alias", ""),
                f"[{status_style}]{status}[/{status_style}]",
                f"[{priority_style}]{priority}[/{priority_style}]",
                tags_display,
                created_display,
            )

        self.console.print(table)
        self.console.print(f"\n[dim]Total: {len(projects)} projects[/dim]")

    def format_project_details(
        self, project_data: Dict[str, Any], include_overview: bool = False
    ) -> None:
        """Format and display detailed project information.

        Accepts either shape returned by the API:

        * ``GET .../projects/{id}`` -- a flat project object.
        * ``GET .../projects/{id}/overview`` -- ``{"project": {...},
          "repositories": {"total", "by_layer", "primary"}, "board": {...}}``.

        The overview shape nests the project and makes ``repositories`` a
        summary dict rather than a list. Reading it as if it were flat printed
        every field as "Unknown", reported ``len()`` of a 3-key dict as the
        repository count, and then crashed iterating that dict as if its keys
        were repository records.
        """
        if self.format_type == "json":
            self._print_json(project_data)
            return

        # Unwrap the overview envelope, keeping the summary sections aside.
        project = project_data.get("project")
        if isinstance(project, dict):
            repositories = project_data.get("repositories")
            board = project_data.get("board")
        else:
            project = project_data
            repositories = project_data.get("repositories")
            board = None

        # Create project info table
        info_table = Table.grid(padding=1)
        info_table.add_column(style="bold cyan", justify="right")
        info_table.add_column(style="white")

        info_table.add_row("Name:", project.get("name", "Unknown"))
        info_table.add_row("Alias:", project.get("alias", "Unknown"))
        info_table.add_row("ID:", project.get("id", "Unknown"))

        # Status and Priority
        status = project.get("status", "UNKNOWN")
        status_style = self._get_project_status_style(status)
        priority = project.get("priority", "MEDIUM")
        priority_style = self._get_priority_style(priority)

        info_table.add_row("Status:", f"[{status_style}]{status}[/{status_style}]")
        info_table.add_row(
            "Priority:", f"[{priority_style}]{priority}[/{priority_style}]"
        )

        # Description
        if project.get("description"):
            info_table.add_row("Description:", project["description"])

        # Goals
        if project.get("goals"):
            info_table.add_row("", "")  # Spacer
            info_table.add_row("[bold]Goals:[/bold]", "")
            # Truncate long goals for table display
            goals = project["goals"]
            if len(goals) > 200:
                goals = goals[:197] + "..."
            info_table.add_row("", goals)

        # Scope limitations
        if project.get("scope_limitations"):
            info_table.add_row("", "")  # Spacer
            info_table.add_row("[bold]Out of Scope:[/bold]", "")
            limitations = project["scope_limitations"]
            if len(limitations) > 200:
                limitations = limitations[:197] + "..."
            info_table.add_row("", limitations)

        # Tags
        if project.get("tags"):
            tags = ", ".join(project["tags"])
            info_table.add_row("Tags:", tags)

        # Timestamps
        info_table.add_row("", "")  # Spacer
        info_table.add_row("Created:", self._format_datetime(project.get("created_at")))
        info_table.add_row("Updated:", self._format_datetime(project.get("updated_at")))

        # Overview data. `repositories` is a summary dict from the overview
        # endpoint; a list only if some future caller passes one.
        if include_overview and repositories:
            repo_count = (
                repositories.get("total", 0)
                if isinstance(repositories, dict)
                else len(repositories)
            )
            info_table.add_row("", "")  # Spacer
            info_table.add_row("[bold]Repositories:[/bold]", str(repo_count))
            if isinstance(repositories, dict):
                primary = repositories.get("primary")
                if primary:
                    info_table.add_row("Primary:", primary.get("name", "Unknown"))

        if include_overview and board:
            tickets = board.get("tickets") or {}
            info_table.add_row("", "")  # Spacer
            info_table.add_row(
                "[bold]Board:[/bold]",
                f"{board.get('name', 'Unknown')} ({board.get('type', 'unknown')})",
            )
            if tickets:
                info_table.add_row(
                    "Tickets:",
                    f"{tickets.get('total', 0)} total · "
                    f"{tickets.get('open', 0)} open · "
                    f"{tickets.get('in_progress', 0)} in progress · "
                    f"{tickets.get('completed', 0)} done",
                )

        panel = Panel(
            info_table,
            title=f"[bold white]Project: {project.get('name', 'Unknown')}[/bold white]",
            border_style="blue",
        )

        self.console.print(panel)

        # Per-layer breakdown, when the overview supplied one.
        if include_overview and isinstance(repositories, dict):
            self._print_repositories_by_layer(repositories.get("by_layer") or {})
        elif include_overview and isinstance(repositories, list) and repositories:
            self._print_project_repositories(repositories)

    def _print_repositories_by_layer(self, by_layer: Dict[str, Any]) -> None:
        """Print the overview's per-layer repository/issue breakdown."""
        if not by_layer:
            return

        self.console.print("\n[bold]Repositories by layer:[/bold]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Layer", style="yellow", width=14)
        table.add_column("Repos", style="cyan", width=7, justify="right")
        table.add_column("Issues", style="white", width=8, justify="right")
        table.add_column("Open", style="green", width=7, justify="right")

        for layer, stats in by_layer.items():
            table.add_row(
                layer,
                str(stats.get("repositories", 0)),
                str(stats.get("total_issues", 0)),
                str(stats.get("open_issues", 0)),
            )

        self.console.print(table)

    def _print_project_repositories(self, repositories: List[Dict[str, Any]]) -> None:
        """Print project repositories table."""
        self.console.print("\n[bold]Repositories:[/bold]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Repository", style="cyan", min_width=30)
        table.add_column("Layer", style="yellow", width=12)
        table.add_column("Primary", style="green", width=8, justify="center")

        for repo in repositories:
            primary_marker = "✓" if repo.get("is_primary") else ""

            table.add_row(
                repo.get("name", repo.get("repository_url", "Unknown")),
                repo.get("layer", "UNASSIGNED"),
                primary_marker,
            )

        self.console.print(table)

    def _get_project_status_style(self, status: str) -> str:
        """Get Rich style for project status."""
        status_styles = {
            # Keys mirror ProjectStatus (PLANNING/ACTIVE/ARCHIVED). ON_HOLD and
            # COMPLETED were listed here but are not members of the enum, so they
            # could never match -- removed rather than left implying support.
            "PLANNING": "cyan",
            "ACTIVE": "green",
            "ARCHIVED": "dim",
        }
        return status_styles.get(enum_key(status), "white")

    def _get_priority_style(self, priority: str) -> str:
        """Get Rich style for project priority."""
        priority_styles = {
            # Mirrors ProjectPriority (HIGH/MEDIUM/LOW). CRITICAL is not a
            # member; it was unreachable and is gone for the same reason.
            "LOW": "dim",
            "MEDIUM": "blue",
            "HIGH": "yellow",
        }
        return priority_styles.get(enum_key(priority), "white")


class ProgressReporter:
    """Progress reporting for long-running operations."""

    def __init__(self, description: str):
        self.description = description
        self.progress = None
        self.task = None

    def __enter__(self):
        """Start progress reporting."""
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            # **stderr.** A spinner on stdout lands in the middle of the payload:
            # `--format json` came back with "Loading tickets..." in front of the
            # opening bracket, so parsing it failed before the JSON was even
            # reached. Progress is for the person watching, never for the caller
            # reading the output.
            console=advisory_console,
        )
        self.progress.start()
        self.task = self.progress.add_task(self.description, total=None)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop progress reporting."""
        self.stop()

    def stop(self) -> None:
        """Stop the spinner now, and tolerate being called again.

        A caller that spans the whole command needs to put the spinner away
        before it starts printing -- a live animation over a report is noise,
        and over an interactive prompt it is worse than noise. The `with` block
        still exits afterwards, so this has to be safe twice.
        """
        if self.progress is not None:
            self.progress.stop()
            self.progress = None
            self.task = None

    def update(self, description: str):
        """Update progress description."""
        if self.progress and self.task:
            self.progress.update(self.task, description=description)
