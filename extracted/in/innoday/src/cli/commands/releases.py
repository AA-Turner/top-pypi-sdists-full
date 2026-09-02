"""
InnoDay CLI Releases Commands

Handles release management operations: listing releases and viewing release details.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.config import CLIConfig
from src.cli.utils.formatters import (
    describe_error,
    format_error,
    format_info,
    format_success,
    format_warning,
)
from src.cli.utils.project_context import load_project_context
from src.cli.utils.release_view import (
    header_lines,
    prose_lines,
    summary_table,
    unnarrated_notice,
)
from src.domain.release import ReleaseVerdict

console = Console()


class ReleasesCommands:
    """Release management commands."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up releases command parser."""
        subparsers = parser.add_subparsers(
            title="Releases Commands",
            dest="releases_command",
            help="Release operations",
        )

        # releases list
        list_parser = subparsers.add_parser(
            "list",
            help="List releases",
            description="List releases for the current organization",
        )
        # **No default limit.** It used to be 10, on top of a server-side sort
        # that ordered versions as strings -- so "v1.9.0" outranked "v1.12.0",
        # "v1.11.0" and "v1.10.0", and the three newest releases fell off the
        # page. A project cutting v1.11.0 looked like it had last shipped v1.9.0.
        # The sort is fixed server-side; listing everything by default means the
        # answer no longer depends on a truncation nobody asked for. Filter to
        # narrow, rather than being narrowed silently.
        list_parser.add_argument(
            "--limit",
            type=int,
            default=None,
            metavar="N",
            help="Show at most N releases (default: all)",
        )
        list_parser.add_argument(
            "--status",
            choices=["planned", "in_progress", "released", "archived"],
            help="Only releases with this status. 'in_progress' is the version "
            "being cut; 'planned' is what is queued behind it.",
        )
        list_parser.add_argument(
            "--current",
            action="store_true",
            help="Show only the release being cut now -- the one blastoff will "
            "tag. Equivalent to --status in_progress, without needing to know "
            "which status that is.",
        )
        list_parser.add_argument(
            "--org-id",
            default=argparse.SUPPRESS,
            metavar="ORG_ID",
            help="Override organization ID (default: from config)",
        )
        list_parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            metavar="PROJECT_ID",
            help="Filter to releases for this project only",
        )

        # releases summarize
        summarize_parser = subparsers.add_parser(
            "summarize",
            help="Assemble the release summary: what moved, and who moved it",
            description=(
                "The release being cut, assembled as a team summary -- the same "
                "payload 'innoday summary --release' returns, and what the "
                "/innoday:summary skill narrates. Prose is written by a Claude "
                "session, never here."
            ),
        )
        summarize_parser.add_argument(
            "version",
            nargs="?",
            default=None,
            # Optional, defaulting to the release being cut, because that is the
            # release anyone typing this means. Requiring it made the command
            # unusable without first running `releases list` to look up a number
            # the project already knows -- while `releases content` next door had
            # the default right all along.
            help="Release version to summarise (e.g. v1.11.0). Omitted means "
            "the release this project is currently cutting",
        )
        summarize_parser.add_argument(
            "--table",
            action="store_true",
            help="Render as a table -- ticket, summary, people, PRs, verdict -- "
            "instead of prose. The same rows either way; the table is for "
            "checking coverage, the prose for catching up",
        )
        summarize_parser.add_argument(
            "--json",
            dest="summary_json",
            action="store_true",
            help="Print the raw assembled payload instead of the rendered summary",
        )
        # No `--org-id` here any more. It selected the organization for a
        # direct release-row fetch; the summary path resolves the org from config
        # the way every other read does, so the flag could only be accepted and
        # ignored. The entrypoint's `--organization` is the way to point
        # elsewhere, and `--dir` to point at another workspace.
        summarize_parser.add_argument(
            "--project-id",
            dest="project_id",
            default=argparse.SUPPRESS,
            metavar="PROJECT_ID",
            help="Project this version belongs to (version strings are unique "
            "per project; resolved from cwd's .innoday/project.yml when omitted)",
        )

        # releases content
        content_parser = subparsers.add_parser(
            "content",
            help="What a release contains: tickets, their pull requests, and gaps",
            description=(
                "The release assembled server-side, as tickets rather than as "
                "repositories. Each ticket carries the pull requests that "
                "delivered it, whether they merged, who worked on it, and what "
                "is missing. This is what a release summary is written from -- "
                "the narration happens in a Claude session, never here."
            ),
        )
        content_parser.add_argument(
            "version",
            nargs="?",
            help=(
                "Release version to scope tickets to (e.g. v1.11.0). Omitted "
                "means the release this project is currently cutting"
            ),
        )
        content_parser.add_argument(
            "--since",
            help=(
                "Override the window's start (ISO timestamp). Normally leave "
                "this alone: the boundary is derived from the last shipped "
                "release, and a hand-typed one that is wrong produces a "
                "confident, wrong report"
            ),
        )
        content_parser.add_argument(
            "--window-label",
            dest="window_label",
            help="Human phrase for the window, echoed into the payload",
        )

        # releases create
        create_parser = subparsers.add_parser(
            "create",
            help="Create a release record",
            description="Create a release record. Version must be unique per project.",
        )
        create_parser.add_argument(
            "version", help="Release version string (e.g. v1.4.0)"
        )
        create_parser.add_argument(
            "--org-id",
            default=argparse.SUPPRESS,
            metavar="ORG_ID",
            help="Override organization ID (default: from config)",
        )
        create_parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            metavar="PROJECT_ID",
            help="Project this release belongs to (resolved from cwd's "
            ".innoday/project.yml when omitted)",
        )
        create_parser.add_argument("--name", metavar="NAME", help="Release name")
        create_parser.add_argument(
            "--status",
            choices=["planned", "in_progress", "released", "archived"],
            default="planned",
            help="Release status (default: planned)",
        )
        create_parser.add_argument(
            "--target-date",
            metavar="YYYY-MM-DD",
            help="Calendar day this release is aimed at. Distinct from "
            "--released-at, which records when it actually shipped.",
        )
        create_parser.add_argument(
            "--released-at",
            metavar="ISO_DATETIME",
            help="When the release shipped (ISO 8601). Auto-set if --status "
            "released and omitted.",
        )
        create_parser.add_argument("--notes", metavar="TEXT", help="Release notes")
        create_parser.add_argument(
            "--summary", metavar="TEXT", help="Human-readable summary"
        )
        create_parser.add_argument(
            "--changelog-json",
            metavar="JSON",
            help="Structured changelog as a JSON string: "
            '[{"repo": "...", "prs": [{"number": 1, "title": "...", "author": "..."}]}]',
        )
        create_parser.add_argument(
            "--if-exists",
            choices=["fail", "update"],
            default="fail",
            help="What to do if a release with this version already exists for "
            "the project (default: fail with 409). 'update' PATCHes the "
            "existing release with the fields given here instead.",
        )

        # releases delete
        delete_parser = subparsers.add_parser(
            "delete",
            help="Withdraw a release record, freeing its version",
            description="Withdraw a release by version. The record is hidden "
            "rather than destroyed, and its version becomes available to cut "
            "again. Does NOT remove tags or GitHub Releases -- those are named "
            "so you can remove them yourself.",
        )
        delete_parser.add_argument(
            "version", help="Release version string (e.g. v1.4.0)"
        )
        delete_parser.add_argument(
            "--org-id",
            default=argparse.SUPPRESS,
            metavar="ORG_ID",
            help="Override organization ID (default: from config)",
        )
        delete_parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            metavar="PROJECT_ID",
            help="Project this version belongs to (resolved from cwd's "
            ".innoday/project.yml when omitted)",
        )
        delete_parser.add_argument(
            "--yes",
            action="store_true",
            help="Skip the confirmation prompt",
        )

        # releases update
        update_parser = subparsers.add_parser(
            "update",
            help="Update a release record",
            description="Update a release by version. Use --status released to "
            "mark it shipped (auto-sets released_at, rotates the pipeline, and "
            "records what was planned in). Tickets are left alone -- shipping a "
            "version does not close the work on it.",
        )
        update_parser.add_argument(
            "version", help="Release version string (e.g. v1.4.0)"
        )
        update_parser.add_argument(
            "--org-id",
            default=argparse.SUPPRESS,
            metavar="ORG_ID",
            help="Override organization ID (default: from config)",
        )
        update_parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            metavar="PROJECT_ID",
            help="Project this version belongs to (resolved from cwd's "
            ".innoday/project.yml when omitted)",
        )
        update_parser.add_argument("--name", metavar="NAME", help="Release name")
        update_parser.add_argument(
            "--status",
            choices=["planned", "in_progress", "released", "archived"],
            help="New release status",
        )
        # The version itself is deliberately NOT updatable here: it is the
        # positional key this command looks the release up by, and it is also the
        # free-text value every planned-in ticket carries. Changing it has to
        # rewrite those tickets in the same transaction (`release_pipeline._rename`
        # does that) -- a rename, not a field edit.
        update_parser.add_argument(
            "--target-date",
            metavar="YYYY-MM-DD",
            help="Calendar day this release is aimed at (empty string clears it). "
            "Distinct from --released-at, which records when it actually shipped.",
        )
        update_parser.add_argument(
            "--released-at",
            metavar="ISO_DATETIME",
            help="When the release shipped (ISO 8601)",
        )
        update_parser.add_argument("--notes", metavar="TEXT", help="Release notes")
        update_parser.add_argument(
            "--summary", metavar="TEXT", help="Human-readable summary"
        )
        update_parser.add_argument(
            "--changelog-json",
            metavar="JSON",
            help="Structured changelog as a JSON string",
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute releases command."""
        command = getattr(args, "releases_command", None)

        if command == "list":
            return await ReleasesCommands._handle_list(args, config)
        elif command == "summarize":
            return await ReleasesCommands._handle_summarize(args, config)
        elif command == "content":
            return await ReleasesCommands._handle_content(args, config)
        elif command == "create":
            return await ReleasesCommands._handle_create(args, config)
        elif command == "update":
            return await ReleasesCommands._handle_update(args, config)
        elif command == "delete":
            return await ReleasesCommands._handle_delete(args, config)
        else:
            console.print(format_error("No releases command specified"))
            console.print(
                format_info(
                    "Available: list, summarize, content, create, update — "
                    "use 'innoday releases --help' for details"
                )
            )
            return 1

    @staticmethod
    async def _resolve_org_id_async(
        args: argparse.Namespace, config: CLIConfig, client
    ) -> Optional[str]:
        """Organization id from args or context, resolving an alias if needed.

        These routes filter on `Release.organization_id == org_id` using the raw
        path parameter, so an alias reaching the URL produces `HTTP 200` with an
        **empty list** rather than an error -- the worst possible answer. The
        alias is therefore resolved here, before the URL is built.
        """
        from src.cli.utils.context import ContextError, _resolve_org_id

        ref = getattr(args, "org_id", None) or config.get_current_organization()
        if not ref:
            return None
        try:
            return await _resolve_org_id(config, client, ref)
        except ContextError:
            return None

    @staticmethod
    def _resolve_org_id(args: argparse.Namespace, config: CLIConfig) -> Optional[str]:
        """Synchronous form, kept for callers that already hold a resolved id."""
        if getattr(args, "org_id", None):
            return args.org_id

        org_alias = config.get_current_organization()
        if not org_alias:
            return None

        return config.get_organization_id(org_alias)

    @staticmethod
    def _resolve_project_id(
        args: argparse.Namespace, config: CLIConfig
    ) -> Optional[str]:
        """Resolve project ID from args or cwd's .innoday/project.yml."""
        return getattr(args, "project_id", None) or config.get_current_project_id()

    @staticmethod
    def _build_release_body(args: argparse.Namespace) -> Dict[str, Any]:
        """Build the shared request body fields for create/update from CLI args."""
        body: Dict[str, Any] = {}
        if getattr(args, "name", None) is not None:
            body["name"] = args.name
        if getattr(args, "status", None) is not None:
            body["status"] = args.status
        # `is not None`, not truthiness: `--target-date ""` is how you clear a
        # date, and an empty string is exactly the value truthiness would drop.
        if getattr(args, "target_date", None) is not None:
            body["target_date"] = args.target_date or None
        if getattr(args, "released_at", None) is not None:
            body["released_at"] = args.released_at
        if getattr(args, "notes", None) is not None:
            body["notes"] = args.notes
        if getattr(args, "summary", None) is not None:
            body["summary"] = args.summary
        if getattr(args, "changelog_json", None) is not None:
            try:
                body["changelog"] = json.loads(args.changelog_json)
            except json.JSONDecodeError as e:
                raise ValueError(f"--changelog-json is not valid JSON: {e}")
        return body

    @staticmethod
    async def _handle_list(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle releases list command."""
        try:
            api_client = InnoDayAPIClient(config)
            org_id = await ReleasesCommands._resolve_org_id_async(
                args, config, api_client
            )
            if not org_id:
                console.print(
                    format_error(
                        "No organization resolved. Run this from a directory "
                        "with .innoday/project.yml, or pass "
                        "--org <alias|id> --project <alias|id>."
                    )
                )
                return 1

            limit = getattr(args, "limit", None)
            # --current is sugar for --status in_progress: the two-slot pipeline
            # has exactly one in-progress release, and that is the one blastoff
            # cuts. Asking for "the current release" should not require knowing
            # which status word means current.
            status_filter = getattr(args, "status", None)
            if getattr(args, "current", False):
                status_filter = "in_progress"
            # Through the shared resolver, so this falls back to the cwd's
            # project like every other command in this file. Reading args alone
            # meant a bare `innoday releases list` inside a project workspace
            # answered with the whole **organization** while presenting as that
            # project's releases -- so PF's listing showed S4C's and BLASTOFF's
            # rows, and the phantom "duplicate v0.2.0" and "second in_progress"
            # they produced were diagnosed twice as real corruption of PF's
            # release pipeline. Pass --org-id with no project for the org view.
            project_id = ReleasesCommands._resolve_project_id(args, config)

            params: Dict[str, Any] = {}
            if limit is not None:
                params["limit"] = limit
            if status_filter:
                params["status"] = status_filter
            if project_id:
                params["project_id"] = project_id
            try:
                response = await api_client.get(
                    f"/organizations/{org_id}/releases",
                    params=params,
                )
            finally:
                await api_client.close()

            if response.status_code != 200:
                console.print(
                    format_error(
                        f"Failed to fetch releases: HTTP {response.status_code}"
                    )
                )
                return 1

            releases: List[Dict[str, Any]] = response.json()

            # The API returns newest-first (semver-ordered) but enforces no
            # limit of its own, so the trim stays here -- only when one was
            # actually asked for. It used to default to 10 and silently hide
            # whatever came after.
            if limit is not None:
                releases = releases[:limit]

            if getattr(args, "format", "table") == "json":
                print(json.dumps(releases, indent=2))
                return 0

            if not releases:
                console.print(format_warning("No releases found"))
                return 0

            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Version", style="bold")
            table.add_column("Status")
            table.add_column("Released")
            table.add_column("Name")

            for r in releases:
                released_at = r.get("released_at") or ""
                if released_at:
                    released_at = released_at[:10]  # date portion only

                table.add_row(
                    r.get("version", ""),
                    r.get("status", ""),
                    released_at,
                    r.get("name") or "",
                )

            console.print(table)
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1

    @staticmethod
    async def _handle_content(args: argparse.Namespace, config: CLIConfig) -> int:
        """What a release contains, as tickets, for a summary to be written from.

        **JSON on stdout, always.** The consumer is a Claude session writing a
        release summary, not a person reading a table -- the platform assembles
        and judges, and narration happens in the session. Anything a person
        needs goes to stderr.
        """
        api_client = InnoDayAPIClient(config)
        try:
            return await ReleasesCommands._content(args, config, api_client)
        finally:
            await api_client.close()

    @staticmethod
    async def _content(args, config: CLIConfig, api_client) -> int:
        payload = await ReleasesCommands._content_payload(args, config, api_client)
        if payload is None:
            return 1
        print(json.dumps(payload, indent=2, default=str))
        return 0

    @staticmethod
    async def _content_payload(args, config: CLIConfig, api_client):
        """The assembled release, or `None` having already said why not.

        Shared by `releases content` (which prints it as JSON for a narrator to
        write from) and `releases summarize` (which renders it for a person to
        read). **One fetch, deliberately**: the rendered path used to read
        `summary-data` while the JSON path read `release/content`, and the two
        payloads disagree about whether anything merged -- so the same release,
        asked for two ways, came back as two different releases.
        """
        org_id = await ReleasesCommands._resolve_org_id_async(args, config, api_client)
        if not org_id:
            console.print(
                format_error(
                    "No organization resolved. Run this from a directory with "
                    ".innoday/project.yml, or pass --org <alias|id>."
                )
            )
            return None
        project_id = (
            getattr(args, "project_id", None) or config.get_current_project_id()
        )
        if not project_id:
            console.print(
                format_error(
                    "No project resolved. Run this from a project directory, "
                    "or pass --project <alias|id>."
                )
            )
            return None

        params = {
            k: v
            for k, v in (
                ("since", getattr(args, "since", None)),
                ("window_label", getattr(args, "window_label", None)),
                ("version", getattr(args, "version", None)),
            )
            if v
        }
        try:
            response = await api_client.get(
                f"/organizations/{org_id}/projects/{project_id}/release/content",
                params=params,
            )
        except APIError as exc:
            console.print(format_error(str(exc)))
            return None

        if response.status_code == 409:
            # A missing credential is a setup problem, not an empty release,
            # and the two must never render the same.
            console.print(format_error(response.json().get("detail", "")))
            return None
        if response.status_code != 200:
            console.print(
                format_error(f"Could not assemble the release: {response.status_code}")
            )
            return None

        return response.json()

    @staticmethod
    async def _handle_summarize(args: argparse.Namespace, config: CLIConfig) -> int:
        """`releases summarize` -- the release, rendered for a person to read.

        **The same payload `releases content` returns, and the same one the
        `/innoday:summary` skill narrates from.** It used to proxy to
        `innoday summary --release`, which assembles the stand-up slice: that
        payload sees at most one pull request URL per ticket, so it could not
        say whether anything had merged -- the single most important thing a
        release summary reports. One assembly path now, two renderings of it.

        Prose is still never written here. `narrative` is whatever a Claude
        session wrote and saved; where none exists the ticket's title stands in
        and the footer says how many lines that is.
        """
        api_client = InnoDayAPIClient(config)
        try:
            payload = await ReleasesCommands._content_payload(args, config, api_client)
        finally:
            await api_client.close()
        if payload is None:
            return 1

        if (
            getattr(args, "summary_json", False)
            or getattr(args, "format", None) == "json"
        ):
            print(json.dumps(payload, indent=2, default=str))
            return 0

        items = payload.get("items") or []
        project_label = ReleasesCommands._project_label(args, config)
        for line in header_lines(payload, str(project_label)):
            console.print(line)

        if getattr(args, "table", False):
            console.print(summary_table(items))
        elif items:
            for line in prose_lines(items):
                console.print(line)
        else:
            console.print("  [dim]No tickets are on this release.[/dim]")

        ReleasesCommands._render_attention(payload)

        notice = unnarrated_notice(items)
        if notice:
            console.print(f"[dim]{notice}[/dim]")
        return 0

    @staticmethod
    def _project_label(args, config: CLIConfig) -> str:
        """`BPAI`, not the project's UUID.

        Resolved from the directory the caller pointed at rather than the
        process's own cwd, because `--dir` is how somebody summarises another
        workspace -- and without honouring it the header names whichever project
        this terminal happens to be sitting in.
        """
        project_ref = (
            getattr(args, "project_id", None) or config.get_current_project_id()
        )
        context_dir = getattr(args, "dir", None)
        context = load_project_context(Path(context_dir) if context_dir else None) or {}
        if project_ref and project_ref == context.get("project_id"):
            return str(
                context.get("project_alias")
                or context.get("project_name")
                or project_ref
            )
        return str(project_ref or "")

    @staticmethod
    def _render_attention(payload: Dict[str, Any]) -> None:
        """Work this release is carrying that nobody has accounted for.

        Three shapes, and they are the same problem seen from different sides:
        a ticket shipped without being tagged, and a merged pull request naming
        no ticket. Both are going out in this release either way -- the release
        does not wait for the paperwork -- so leaving them out of the summary
        does not make them not ship, it makes them ship unmentioned.
        """
        off_release = payload.get("off_release") or []
        shipped_untagged = [
            row
            for row in off_release
            if row.get("state") == ReleaseVerdict.SHIPPED_UNTAGGED.value
        ]
        # **Work in flight against a ticket on no release.** Split out of
        # `started_untagged` once open pull requests were attached, and rendered
        # nowhere at all until now -- so the loudest thing after "this shipped
        # untagged" reached no terminal reader.
        candidates = [
            row
            for row in off_release
            if row.get("state") == ReleaseVerdict.RELEASE_CANDIDATE.value
        ]
        conflicts = payload.get("conflicts") or []
        unticketed = payload.get("unticketed") or []
        if not (shipped_untagged or candidates or conflicts or unticketed):
            return

        console.print("[bold]Needs attention[/bold]")
        console.print("")
        # **`prose_lines`, not a third copy of the line.** This block built the
        # line by hand -- unfiltered, so an off-release ticket whose pull request
        # authors do not resolve printed `BPAI-407 ·  · bps-api#611 · shipped, on
        # no release`, the dangling separator the skill calls damage -- and
        # un-bold, fifteen lines below the same row rendered correctly by the
        # same command. An `off_release` row carries the same fields as an item,
        # so it goes through the same renderer.
        for line in prose_lines(shipped_untagged):
            console.print(line)
        for line in prose_lines(candidates):
            console.print(line)
        if conflicts:
            # A ticket unfinished on a version that already went out. Reported
            # with its own detail rather than through `prose_lines`, because the
            # thing worth reading is which release left it behind.
            count = len(conflicts)
            noun = "ticket" if count == 1 else "tickets"
            console.print(
                f"  [dim]Left behind by a release that shipped — {count} {noun}[/dim]"
            )
            for row in conflicts:
                console.print(
                    f"    {escape(str(row.get('ref')))}  "
                    f"[dim]{escape(str(row.get('detail') or ''))}[/dim]"
                )
            console.print("")
        if unticketed:
            count = len(unticketed)
            noun = "pull request" if count == 1 else "pull requests"
            console.print(
                f"  [dim]Shipping with no ticket — {count} merged {noun}[/dim]"
            )
            for pr in unticketed:
                console.print(
                    f"    {escape(str(pr.get('repo')))}#{pr.get('number')}  "
                    f"[dim]{escape(str(pr.get('title') or ''))}[/dim]"
                )
            console.print("")

    @staticmethod
    async def _handle_create(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle releases create command."""
        try:
            api_client = InnoDayAPIClient(config)
            org_id = await ReleasesCommands._resolve_org_id_async(
                args, config, api_client
            )
            if not org_id:
                console.print(
                    format_error(
                        "No organization resolved. Run this from a directory "
                        "with .innoday/project.yml, or pass "
                        "--org <alias|id> --project <alias|id>."
                    )
                )
                return 1

            project_id = ReleasesCommands._resolve_project_id(args, config)
            if not project_id:
                console.print(format_error("No project specified"))
                console.print(
                    format_info(
                        "Pass --project-id, or run this command from inside "
                        "a project directory (one with .innoday/project.yml)."
                    )
                )
                return 1

            body = ReleasesCommands._build_release_body(args)
            body["version"] = args.version
            body["project_id"] = project_id
            body.setdefault("status", "planned")
            try:
                response = await api_client.post(
                    f"/organizations/{org_id}/releases", json=body
                )

                if response.status_code == 409 and args.if_exists == "update":
                    lookup = await api_client.get(
                        f"/organizations/{org_id}/releases/by-version/{args.version}",
                        params={"project_id": project_id},
                    )
                    if lookup.status_code != 200:
                        console.print(
                            format_error(
                                f"Release exists but could not be looked up for update: "
                                f"HTTP {lookup.status_code}"
                            )
                        )
                        return 1
                    release_id = lookup.json()["id"]
                    update_body = {k: v for k, v in body.items() if k != "project_id"}
                    response = await api_client.patch(
                        f"/organizations/{org_id}/releases/{release_id}",
                        json=update_body,
                    )
            finally:
                await api_client.close()

            if response.status_code == 409:
                console.print(
                    format_error(
                        f"Release '{args.version}' already exists for this project. "
                        "Pass --if-exists update to update it instead."
                    )
                )
                return 1

            if response.status_code not in (200, 201):
                console.print(
                    format_error(
                        f"Failed to create release: HTTP {response.status_code} -- {response.text}"
                    )
                )
                return 1

            r = response.json()
            if getattr(args, "format", "table") == "json":
                print(json.dumps(r, indent=2))
            else:
                console.print(
                    format_success(f"Release {r['version']} ({r['status']}) saved.")
                )
            return 0

        except ValueError as e:
            console.print(format_error(str(e)))
            return 1
        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1

    @staticmethod
    async def _handle_delete(args: argparse.Namespace, config: CLIConfig) -> int:
        """Withdraw a release, then check it actually went.

        The check is the point. A delete that frees a version is only useful if
        the version really is free, and the caller finds out here rather than
        the next time they try to cut it.

        What this does **not** do is touch GitHub. If the release was really
        cut, its tags and GitHub Releases still exist, and blastoff skips a repo
        whose release already exists -- so re-cutting silently does nothing
        until they are gone. Removing them automatically is destructive,
        irreversible and partial across repos in the same way tagging already
        is, so this names them and leaves the decision with a person.
        """
        api_client = InnoDayAPIClient(config)
        try:
            org_id = await ReleasesCommands._resolve_org_id_async(
                args, config, api_client
            )
            if not org_id:
                console.print(
                    format_error(
                        "No organization resolved. Run this from a directory "
                        "with .innoday/project.yml, or pass "
                        "--org <alias|id> --project <alias|id>."
                    )
                )
                return 1

            project_id = ReleasesCommands._resolve_project_id(args, config)
            if not project_id:
                console.print(format_error("No project specified"))
                return 1

            lookup = await api_client.get(
                f"/organizations/{org_id}/releases/by-version/{args.version}",
                params={"project_id": project_id},
            )
            if lookup.status_code == 404:
                console.print(format_error(f"Release '{args.version}' not found."))
                return 1
            if lookup.status_code != 200:
                console.print(
                    format_error(
                        f"Failed to look up release: HTTP {lookup.status_code}"
                    )
                )
                return 1

            looked_up = lookup.json()
            if looked_up.get("status") == "unregistered":
                console.print(format_error(f"Release '{args.version}' not found."))
                return 1

            release_id = looked_up["id"]
            status = looked_up.get("status")

            if not getattr(args, "yes", False):
                console.print(
                    format_warning(
                        f"Withdraw release {args.version} (status: {status})? "
                        "Its version becomes available to cut again."
                    )
                )
                if status == "released":
                    console.print(
                        format_warning(
                            "This one was actually released -- its tags and "
                            "GitHub Releases will still exist afterwards."
                        )
                    )
                if input("Type the version to confirm: ").strip() != args.version:
                    console.print(format_info("Nothing was changed."))
                    return 1

            response = await api_client.delete(
                f"/organizations/{org_id}/releases/{release_id}"
            )
            if response.status_code not in (200, 204):
                console.print(
                    format_error(
                        f"Failed to withdraw release: HTTP {response.status_code} "
                        f"-- {response.text}"
                    )
                )
                return 1

            # Verify, rather than trust the status code. The whole reason to
            # withdraw a release is to free the version; saying so without
            # checking is how the archive path misled people in the first place.
            recheck = await api_client.get(
                f"/organizations/{org_id}/releases/by-version/{args.version}",
                params={"project_id": project_id},
            )
            still_there = (
                recheck.status_code == 200
                and recheck.json().get("status") != "unregistered"
            )
            if still_there:
                console.print(
                    format_error(
                        f"Reported success, but {args.version} is still "
                        "resolvable on this project. The version is NOT free. "
                        "Do not assume it was withdrawn."
                    )
                )
                return 1

            console.print(
                format_success(
                    f"Release {args.version} withdrawn. That version is free to "
                    "cut again."
                )
            )
            if status == "released":
                console.print(
                    format_warning(
                        "Tags and GitHub Releases were NOT removed. Until they "
                        "are, re-cutting this version will skip those repos as "
                        "'already exists' rather than tagging them:"
                    )
                )
                console.print(
                    format_info(
                        f"  gh release list --repo <org>/<repo> | grep {args.version}\n"
                        f"  gh release delete {args.version} --repo <org>/<repo> --cleanup-tag"
                    )
                )
            return 0
        finally:
            await api_client.close()

    @staticmethod
    async def _handle_update(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle releases update command. Looks up the release by version, then PATCHes it."""
        try:
            api_client = InnoDayAPIClient(config)
            org_id = await ReleasesCommands._resolve_org_id_async(
                args, config, api_client
            )
            if not org_id:
                console.print(
                    format_error(
                        "No organization resolved. Run this from a directory "
                        "with .innoday/project.yml, or pass "
                        "--org <alias|id> --project <alias|id>."
                    )
                )
                return 1

            project_id = ReleasesCommands._resolve_project_id(args, config)
            if not project_id:
                console.print(format_error("No project specified"))
                console.print(
                    format_info(
                        "Pass --project-id, or run this command from inside "
                        "a project directory (one with .innoday/project.yml)."
                    )
                )
                return 1

            body = ReleasesCommands._build_release_body(args)
            if not body:
                console.print(
                    format_error(
                        "No fields to update -- pass at least one of "
                        "--name/--status/--released-at/--notes/--summary/--changelog-json"
                    )
                )
                return 1
            try:
                lookup = await api_client.get(
                    f"/organizations/{org_id}/releases/by-version/{args.version}",
                    params={"project_id": project_id},
                )
                if lookup.status_code == 404:
                    console.print(format_error(f"Release '{args.version}' not found."))
                    return 1
                if lookup.status_code != 200:
                    console.print(
                        format_error(
                            f"Failed to look up release: HTTP {lookup.status_code}"
                        )
                    )
                    return 1

                looked_up = lookup.json()
                if (
                    looked_up.get("status") == "unregistered"
                    and looked_up.get("ticket_count", 0) == 0
                ):
                    console.print(format_error(f"Release '{args.version}' not found."))
                    return 1

                release_id = looked_up["id"]
                response = await api_client.patch(
                    f"/organizations/{org_id}/releases/{release_id}", json=body
                )
            finally:
                await api_client.close()

            if response.status_code != 200:
                console.print(
                    format_error(
                        f"Failed to update release: HTTP {response.status_code} -- {response.text}"
                    )
                )
                return 1

            r = response.json()
            if getattr(args, "format", "table") == "json":
                print(json.dumps(r, indent=2))
            else:
                console.print(
                    format_success(f"Release {r['version']} ({r['status']}) updated.")
                )
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1
