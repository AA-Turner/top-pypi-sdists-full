"""`innoday timeline` -- a project's curated event history, newest first.

**The timeline had no client at all.** `ProjectTimeline` rows have been written
since PF-102 -- releases, repo attachments, ticket syncs, scrum summaries -- and
the only way to read them was `GET .../timeline` by hand or a psql query. Not the
CLI, not the MCP server, not the `/ui` dashboard. A feed nobody can read is
indistinguishable from a feed nobody writes to, which is exactly how the
"summaries never reached the timeline" bug stayed invisible: there was no surface
on which its absence would have shown.

Read-only on purpose. Entries are written by the mutations they describe (see
`services/project_timeline_writer.py`) so that the entry and the change it
records land in one transaction; a CLI that could append arbitrary rows would
make the feed a place people write notes, which is what `scope`/`updates` are
for.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.markup import escape

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.utils.formatters import ProgressReporter, format_error, format_warning
from src.cli.utils.project_context import load_project_context

console = Console()

#: Event type -> glyph. Keyed on the lowercase value; the column arrives as the
#: enum NAME from Postgres and the value from the API, so both are folded.
EVENT_ICONS: Dict[str, str] = {
    "release": "🚀",
    "release_created": "🚀",
    "release_updated": "🚀",
    "meeting": "🗣",
    "spec_update": "📐",
    "scrum_summary": "📋",
    "repo_added": "📦",
    "repo_removed": "📦",
    "ticket_sync": "🔄",
    "board_attached": "🔗",
}

DEFAULT_LIMIT = 20


def _age(value: Optional[str]) -> str:
    """`2026-08-08T12:07:30+00:00` -> `2h ago`. Never raises on junk.

    Relative rather than absolute because the question a timeline answers is
    "how recently", and a column of ISO timestamps makes the reader do that
    subtraction themselves.
    """
    if not value:
        return ""
    try:
        moment = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return ""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    seconds = int((datetime.now(timezone.utc) - moment).total_seconds())
    if seconds < 0:
        return "just now"
    if seconds < 3600:
        return f"{max(1, seconds // 60)}m ago"
    if seconds < 86400:
        return f"{seconds // 3600}h ago"
    return f"{seconds // 86400}d ago"


def _event_label(event_type: Optional[str]) -> str:
    key = str(event_type or "").lower()
    return f"{EVENT_ICONS.get(key, '•')} {key.replace('_', ' ')}"


def render_timeline(
    entries: List[Dict[str, Any]], *, project_label: str, verbose: bool
) -> str:
    """The rendered feed, as Rich markup. Pure -- everything comes from `entries`."""
    lines: List[str] = [
        f"[bold cyan]Timeline[/bold cyan] · {escape(project_label)}",
        "",
    ]
    if not entries:
        lines.append("  [dim]Nothing on this project's timeline yet.[/dim]")
        return "\n".join(lines)

    for entry in entries:
        when = _age(entry.get("occurred_at"))
        lines.append(
            f"[bold]{_event_label(entry.get('event_type'))}[/bold]  "
            f"{escape(str(entry.get('title') or ''))}"
            f"   [dim]{when}[/dim]"
        )
        summary = str(entry.get("summary") or "").strip()
        if summary:
            for prose in summary.splitlines():
                lines.append(f"    [dim]{escape(prose)}[/dim]")
        by = str(entry.get("created_by") or "")
        if by and by != "system":
            lines.append(f"    [dim]by {escape(by)}[/dim]")
        if verbose and entry.get("metadata"):
            lines.append(f"    [dim]{escape(str(entry['metadata']))}[/dim]")
        lines.append("")
    return "\n".join(lines)


class TimelineCommands:
    """`innoday timeline` — read a project's event history."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--project",
            dest="timeline_project",
            metavar="REF",
            help="Project alias or id (default: resolved from the cwd)",
        )
        parser.add_argument(
            "--event",
            dest="timeline_event",
            metavar="TYPE",
            help="Only this event type, e.g. scrum_summary, release, repo_added",
        )
        parser.add_argument(
            "--limit",
            dest="timeline_limit",
            type=int,
            default=DEFAULT_LIMIT,
            help=f"How many entries to show (default: {DEFAULT_LIMIT}, max 200)",
        )
        parser.add_argument(
            "--verbose",
            dest="timeline_verbose",
            action="store_true",
            help="Also print each entry's structured metadata",
        )
        parser.add_argument(
            "--json",
            dest="timeline_json",
            action="store_true",
            help="Print the raw payload instead of the rendered feed",
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config) -> int:
        import json as _json

        org_alias = config.get_current_organization()
        if not org_alias:
            console.print(
                format_error(
                    "No project in this directory. The organization and "
                    "project come from `.innoday/project.yml` in the working "
                    "directory, so run this from a project workspace, or pass "
                    "--dir <path>.\n"
                    "If you are redirecting output somewhere else, redirect to "
                    "that path rather than changing directory into it."
                )
            )
            return 1
        org_id = config.get_organization_id(org_alias)
        if not org_id:
            console.print(
                format_error(
                    f"Organization '{org_alias}' is not in your local config. "
                    "Run 'innoday orgs list' to refresh."
                )
            )
            return 1

        project_ref = getattr(args, "timeline_project", None) or (
            config.get_current_project_id()
        )
        if not project_ref:
            console.print(
                format_error(
                    "No project. Run this from inside a project directory (one "
                    "with .innoday/project.yml), or pass --project <alias>."
                )
            )
            return 1

        # A UUID in the header tells the reader nothing; the alias lives in the
        # same file the id came from -- so read that file from the directory the
        # caller actually pointed at, and only believe it when it describes the
        # project being shown.
        #
        # Both halves of that were wrong here, and `summary` had already fixed
        # both. Guarding on `--project` catches the subcommand's flag but not the
        # global one, so `innoday --project BPAI timeline` printed BPAI's
        # timeline under PF's name; and reading the cwd ignores `--dir`, so
        # `innoday --dir <bpai> timeline` did the same. Matching on the id
        # closes both, because the label is then only ever the name of the
        # project whose events are on screen.
        project_label = str(project_ref)
        context_dir = getattr(args, "dir", None)
        context = load_project_context(Path(context_dir) if context_dir else None) or {}
        if project_ref and project_ref == context.get("project_id"):
            project_label = (
                context.get("project_alias")
                or context.get("project_name")
                or project_label
            )

        params: Dict[str, Any] = {"limit": max(1, min(200, args.timeline_limit))}
        event = getattr(args, "timeline_event", None)
        if event:
            params["event_type"] = str(event).lower()

        async with InnoDayAPIClient(config) as client:
            try:
                with ProgressReporter("Reading the timeline..."):
                    response = await client.get(
                        f"/organizations/{org_id}/projects/{project_ref}/timeline",
                        params=params,
                    )
            except APIError as exc:
                console.print(format_error(str(exc)))
                return 1

        if response.status_code == 422 and event:
            console.print(
                format_warning(
                    f"'{event}' is not a known event type. Known: "
                    + ", ".join(sorted(EVENT_ICONS))
                )
            )
            return 1
        if response.status_code != 200:
            console.print(
                format_error(
                    f"Could not read the timeline: HTTP {response.status_code} — "
                    f"{response.text[:300]}"
                )
            )
            return 1

        payload = response.json() or {}
        if getattr(args, "timeline_json", False) or (
            getattr(args, "format", None) == "json"
        ):
            print(_json.dumps(payload, indent=2, default=str))
            return 0

        entries = payload.get("entries") or []
        console.print(
            render_timeline(
                entries,
                project_label=project_label,
                verbose=bool(getattr(args, "timeline_verbose", False)),
            )
        )
        if payload.get("next_cursor"):
            console.print(
                "[dim]More entries exist — raise --limit to see further back.[/dim]"
            )
        return 0
