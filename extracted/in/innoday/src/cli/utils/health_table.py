"""Everything a project depends on, in one table.

`projects health` printed the database as a dim suffix on the status line, the
GitHub credential as a sentence, and only the boards as a table -- so a project
with one board showed a paragraph above a single row, and the two dependencies
that were *not* boards did not line up with the one that was. Whether GitHub is
reachable and whether Linear is reachable are the same question asked twice, and
they were answered in two different shapes.

They are rows now, above the boards, in the order a project fails in: without
the database nothing else means anything, without GitHub no code can be read,
and a board is the last thing to go. The first column has no header because the
rows are not all boards and no single word covers them -- "Dependency" is
management English for a column whose contents are self-evident.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from rich.markup import escape
from rich.table import Table


def reach_mark(reachable: Optional[bool]) -> str:
    """`✅` / `❌` / `—`, and the dash is not a failure.

    Three-valued throughout the health payload: `None` means nothing was proved
    -- probing was skipped, no credential is stored, the budget ran out --
    which is a different thing from asked-and-did-not-answer. Collapsing the two
    reports a working board as broken.
    """
    if reachable is None:
        return "[dim]—[/dim]"
    return "[green]✅[/green]" if reachable else "[red]❌[/red]"


def sync_age(seconds: Optional[int]) -> str:
    """`8d ago`, or `never` in yellow.

    Never-synced is the one age worth colouring: every other value is a number
    whose staleness is the reader's policy, because a board synced hourly and
    one synced weekly are both correct and this cannot tell which it is.
    """
    if seconds is None:
        return "[yellow]never[/yellow]"
    if seconds < 3600:
        return f"{seconds // 60}m ago"
    if seconds < 86400:
        return f"{seconds // 3600}h ago"
    return f"{seconds // 86400}d ago"


def _github_row(github: Dict[str, Any]) -> List[str]:
    """GitHub as a row rather than a sentence, carrying the same two numbers.

    `detail` is only shown when it says something a mark cannot: the reason a
    credential was refused, or the reason nothing was checked. On the happy path
    the organisation name is the useful half and the rest was decoration.
    """
    reachable = github.get("reachable")
    detail = str(github.get("detail") or "")
    org = str(github.get("github_org") or "")
    if reachable is None:
        kind = f"[dim]{escape(detail or 'not checked')}[/dim]"
    elif reachable:
        kind = escape(org) if org else "github"
    else:
        kind = f"[red]{escape(detail or 'rejected')}[/red]"
    # **Both numbers are real here.** The probe has always timed its own round
    # trip and repository discovery has always recorded when it last ran; this
    # row printed a dash over each. A dash beside a row showing `1203ms` reads
    # as "not applicable to GitHub", which is a stronger claim than "nobody
    # looked" -- and it was not even that, since both had been measured.
    latency = github.get("latency_ms")
    return [
        "GitHub",
        kind,
        reach_mark(reachable),
        f"{latency}ms" if latency is not None else "[dim]—[/dim]",
        sync_age(github.get("last_sync_age_seconds")),
    ]


def health_table(health: Dict[str, Any]) -> Table:
    """The database, the GitHub credential, and every board, in failure order."""
    table = Table(show_header=True, header_style="bold")
    # No header on the first column: the rows are a database, a credential and
    # some boards, and there is no honest one-word name for that set.
    table.add_column("")
    table.add_column("Type")
    table.add_column("Reachable", justify="center")
    table.add_column("Latency", justify="right")
    table.add_column("Last real sync")

    connected = health.get("database") == "connected"
    db_latency = health.get("database_latency_ms")
    table.add_row(
        "Database",
        "[dim]innoday[/dim]",
        reach_mark(connected),
        f"{db_latency}ms" if db_latency is not None else "[dim]—[/dim]",
        # A database is not synced, so this one stays blank on purpose -- it is
        # the only dash in the column that means "not a thing" rather than
        # "not measured".
        "[dim]—[/dim]",
    )
    table.add_row(*_github_row(health.get("github") or {}))

    for board in health.get("boards") or []:
        latency = board.get("latency_ms")
        table.add_row(
            escape(str(board.get("name") or "-")),
            escape(str(board.get("board_type") or "-")),
            reach_mark(board.get("reachable")),
            f"{latency}ms" if latency is not None else "[dim]—[/dim]",
            sync_age(board.get("last_sync_age_seconds")),
        )
    return table
