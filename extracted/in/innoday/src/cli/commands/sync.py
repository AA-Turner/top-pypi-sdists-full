"""
InnoDay CLI Sync Commands

`innoday sync` (bare, or with a subcommand) is the project-scoped cascade:
board tickets, repos, and current release state, in one operation. Run it
from inside a project directory (one with .innoday/project.yml), or point
it elsewhere with the global `--dir <path>` flag (there is no `sync <path>`
positional -- `--dir` already does this exact job for every command, reused
here rather than inventing a second mechanism).
"""

import argparse
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

import httpx
from rich.console import Console
from rich.table import Table

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.utils.formatters import (
    format_error,
    format_info,
    format_success,
    format_warning,
)
from src.utils.time_windows import parse_iso_utc, parse_window

console = Console()


class SyncScope(str, Enum):
    """Which stages of the cascade to run (PF-398).

    The cascade is three independent pulls that happen to be useful together;
    `--scope` is for when only one of them is what you actually wanted. It is
    a filter on the existing stages, not a new command per stage -- `innoday
    sync` stays the thing you type, and `all` stays the default.
    """

    ALL = "all"
    BOARD = "board"
    REPOS = "repos"
    RELEASES = "releases"


DEFAULT_SCOPE = SyncScope.ALL.value


def parse_since(value: Optional[str]) -> Optional[str]:
    """`3d` or `2026-08-01` → an ISO instant the API can filter on.

    Both spellings, because both are what people reach for: a relative window
    when they mean "recently", an absolute date when they mean a specific one.
    Resolved here rather than server-side so the value sent is an unambiguous
    instant -- "3d" evaluated in the server's clock and the user's would be two
    different questions.

    Both grammars come from `src/utils/time_windows.py`, which the summary
    engine also uses. They were declared here a second time, byte-identical,
    in a module the engine does not import -- so `innoday sync --since 3d` and
    a `3d` summary window could have drifted apart with nothing to notice.

    Raises ValueError on anything else rather than guessing; a misread `--since`
    silently syncs the wrong window, which looks like a data problem.
    """
    if not value:
        return None
    try:
        window = parse_window(value)
    except ValueError:
        raise ValueError("--since must cover at least one unit, e.g. '1d'")
    if window is not None:
        return (datetime.now(timezone.utc) - window).isoformat()
    absolute = parse_iso_utc(value)
    if absolute is None:
        raise ValueError(
            f"--since must be a window like '3d'/'12h'/'2w' or an ISO date "
            f"like '2026-08-01'; got {value!r}"
        )
    return absolute.isoformat()


class SyncCommands:
    """Project-scoped sync cascade."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up sync command parser."""
        parser.add_argument(
            "--since",
            metavar="WHEN",
            help="Only re-process board tickets that moved since then — a "
            "window ('3d', '12h', '2w') or an ISO date ('2026-08-01'). "
            "Tickets InnoDay has never seen are still imported.",
        )
        parser.add_argument(
            "--status",
            action="store_true",
            dest="sync_status_only",
            help="Report whether a sync is running and how the last one went. "
            "Read-only: this starts nothing.",
        )
        parser.add_argument(
            "--scope",
            # Derived from the enum, never typed out beside it. `default` is a
            # plain string already in `choices` because argparse does not pass
            # `default` through `type`.
            choices=[scope.value for scope in SyncScope],
            default=DEFAULT_SCOPE,
            help=f"Which stages of the cascade to run (default: {DEFAULT_SCOPE})",
        )

        subparsers = parser.add_subparsers(
            title="Sync Commands",
            dest="sync_command",
            help="Data synchronization operations",
        )

        # Sync a single ticket by its external key
        ticket_parser = subparsers.add_parser(
            "ticket",
            help="Fetch one ticket from the connected board immediately",
        )
        ticket_parser.add_argument(
            "key", help="External ticket key (e.g. PROJ-123, PF-155)"
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config) -> int:
        """Execute sync command."""
        command = getattr(args, "sync_command", None)

        # Check organization is configured
        if not config.get_current_organization():
            console.print(
                format_error(
                    "Organization not configured. Run 'innoday config init' first."
                )
            )
            return 1

        async with InnoDayAPIClient(
            config, timeout=config.get_sync_timeout()
        ) as client:
            try:
                if getattr(args, "sync_status_only", False):
                    # **The only thing that happens.** A status flag that also
                    # syncs is a status flag nobody can safely run, and the
                    # reason to ask is usually that you are not sure it is safe
                    # to start one.
                    return await SyncCommands._handle_status(args, client, config)
                if command == "ticket":
                    return await SyncCommands._handle_ticket_sync(args, client, config)
                elif command is None:
                    return await SyncCommands._handle_cascade(args, client, config)
                else:
                    console.print(format_error(f"Unknown sync command: {command}"))
                    return 1

            except httpx.ReadTimeout:
                # The old message was `Error: ReadTimeout (no message)`, which
                # names neither what timed out nor whether anything happened. A
                # sync that times out has usually done most of its work
                # server-side, so re-running is the right advice and "it broke"
                # is the wrong impression.
                console.print(
                    format_error(
                        f"The sync did not answer within "
                        f"{config.get_sync_timeout():.0f}s and was given up on."
                    )
                )
                console.print(
                    format_info(
                        "The server may well have finished — re-run to see. If it "
                        "keeps timing out, raise the limit with "
                        "`innoday config set api-timeout <seconds>`."
                    )
                )
                return 1
            except APIError as e:
                console.print(format_error(str(e)))
                return 1

    # ------------------------------------------------------------------ status

    @staticmethod
    def _age(started: Optional[str]) -> str:
        """How long ago, in the roughest useful unit."""
        when = parse_iso_utc(started) if started else None
        if when is None:
            return "at an unknown time"
        seconds = max(0, int((datetime.now(timezone.utc) - when).total_seconds()))
        if seconds < 90:
            return f"{seconds}s ago"
        if seconds < 5400:
            return f"{seconds // 60}m ago"
        return f"{seconds // 3600}h ago"

    @staticmethod
    async def _fetch_status(client, org_id: str, project_id: str) -> Optional[dict]:
        """The project's sync state, or None if the server could not answer.

        None is deliberately not the same as "nothing is running" -- the caller
        decides what an unanswerable question means, and for the pre-flight
        below it must not read as permission.
        """
        try:
            response = await client.get(
                f"/organizations/{org_id}/projects/{project_id}/sync/status"
            )
        except (APIError, httpx.HTTPError):
            # **`httpx.HTTPError` matters more than `APIError` here.** A slow
            # status route raises `ReadTimeout`, which is not an `APIError`, so
            # it escaped to the handler that turns any timeout into "the sync
            # did not answer" and returns 1 -- the pre-flight killing the very
            # run it exists to protect. A check that cannot answer must cost the
            # caller nothing.
            return None
        if response.status_code != 200:
            return None
        return response.json()

    @staticmethod
    def _render_status(status: dict) -> None:
        running = status.get("running") or []
        if running:
            console.print(
                format_warning(
                    f"A sync is running now — {len(running)} board(s) in flight."
                )
            )
            for row in running:
                console.print(
                    f"  · board {row.get('board_registration_id')} "
                    f"started {SyncCommands._age(row.get('started_at'))} "
                    f"[dim]({row.get('status')})[/dim]"
                )
        else:
            console.print(format_success("Nothing is running."))

        last = status.get("last_sync")
        if not last:
            console.print("[dim]No completed sync on record for this project.[/dim]")
            return

        freshness = "current" if status.get("is_fresh") else "stale"
        console.print(
            f"[dim]Last finished {SyncCommands._age(last.get('completed_at'))} "
            f"· {last.get('status')} · data is {freshness}[/dim]"
        )
        found = last.get("tickets_found")
        if found is not None:
            console.print(
                f"[dim]  {found} found · {last.get('tickets_created')} created "
                f"· {last.get('tickets_updated')} updated[/dim]"
            )
        if last.get("error_message"):
            console.print(format_warning(f"  {last['error_message']}"))

    @staticmethod
    async def _handle_status(args, client, config) -> int:
        """`innoday sync --status` -- reports, and starts nothing."""
        resolved = SyncCommands._resolve_target(config)
        if resolved is None:
            return 1
        org_id, project_id = resolved

        status = await SyncCommands._fetch_status(client, org_id, project_id)
        if status is None:
            console.print(format_error("Could not read this project's sync state."))
            return 1
        SyncCommands._render_status(status)
        return 0

    @staticmethod
    def _resolve_target(config) -> Optional[tuple]:
        """(org_id, project_id) from the same context every other command reads."""
        org_alias = config.get_current_organization()
        org_id = config.get_organization_id(org_alias)
        if not org_id:
            console.print(
                format_error(
                    f"Organization '{org_alias}' is not in your local config. "
                    "Run 'innoday orgs list' to refresh, or check "
                    ".innoday/project.yml for a stale org reference."
                )
            )
            return None
        project_id = config.get_current_project_id()
        if not project_id:
            console.print(
                format_error(
                    "No project specified. Run this from inside a project "
                    "directory (one with .innoday/project.yml), or pass "
                    "--dir <path>."
                )
            )
            return None
        return org_id, project_id

    @staticmethod
    async def _handle_cascade(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """
        Sync a project's board tickets, repos, and report current release
        state -- one cascading operation, scoped to cwd's (or --dir's)
        .innoday/project.yml.
        """
        resolved = SyncCommands._resolve_target(config)
        if resolved is None:
            return 1
        org_id, project_id = resolved

        # **Ask first, every time.** The board stage refuses a concurrent run
        # server-side, but only once it has been attempted -- so two people, or
        # two agent sessions, discover each other by colliding. Asking up front
        # turns that into a sentence before anything starts.
        #
        # An unanswerable question is **not** permission: a server that cannot
        # report says nothing about whether a sync is running, so it warns and
        # continues rather than either blocking real work or implying a check
        # happened that did not.
        status = await SyncCommands._fetch_status(client, org_id, project_id)
        if status is None:
            console.print(
                format_warning(
                    "Could not check whether a sync is already running — "
                    "continuing anyway."
                )
            )
        elif status.get("is_running"):
            SyncCommands._render_status(status)
            console.print(
                format_info(
                    "Nothing was started. Watch it with `innoday sync --status`."
                )
            )
            return 1

        try:
            since = parse_since(getattr(args, "since", None))
        except ValueError as exc:
            console.print(format_error(str(exc)))
            return 1

        scope = getattr(args, "scope", DEFAULT_SCOPE)

        def wanted(stage: SyncScope) -> bool:
            return scope in (SyncScope.ALL.value, stage.value)

        exit_code = 0

        # --- 1. Board tickets ---
        if wanted(SyncScope.BOARD):
            console.print("[bold cyan]1. Board tickets[/bold cyan]")
            board_result = await SyncCommands._sync_board(
                client, org_id, project_id, config, since=since
            )
            if board_result == 1:
                exit_code = 1

        # --- 2. Repositories ---
        if wanted(SyncScope.REPOS):
            console.print("\n[bold cyan]2. Repositories[/bold cyan]")
            repo_result = await SyncCommands._sync_repos(client, org_id, project_id)
            if repo_result == 1:
                exit_code = 1

        # --- 3. Releases (report current state -- no external source to sync from) ---
        if wanted(SyncScope.RELEASES):
            console.print("\n[bold cyan]3. Releases[/bold cyan]")
            await SyncCommands._report_releases(client, org_id, project_id)

        return exit_code

    @staticmethod
    async def _sync_board(
        client: InnoDayAPIClient,
        org_id: str,
        project_id: str,
        config,
        since: Optional[str] = None,
    ) -> int:
        """Trigger a sync for the project's one board, if it has one."""
        response = await client.get(
            f"/organizations/{org_id}/boards", params={"project_id": project_id}
        )
        if response.status_code != 200:
            console.print(
                format_error(f"Failed to look up board: HTTP {response.status_code}")
            )
            return 1

        boards = response.json()
        if not boards:
            console.print(
                format_info("No board registered for this project -- skipping.")
            )
            return 0

        board = boards[0]
        board_id = board["id"]

        # No credential is read from this machine and none is sent: the
        # server resolves the board's own credential from Vault (#609).
        sync_data = {"full_sync": False, "dry_run": False, "force": False}
        if since:
            sync_data["since"] = since

        response = await client.post(
            f"/organizations/{org_id}/boards/{board_id}/sync",
            json=sync_data,
        )
        if response.status_code in (200, 201):
            data = response.json()
            console.print(
                format_success(
                    f"Board sync queued for {board['board_name']} (sync_id: {data.get('sync_id')})"
                )
            )
            console.print(
                "  [dim]Check status with: "
                f"innoday board sync-status --board-id {board_id}[/dim]"
            )
            return 0
        elif response.status_code == 429:
            # Print what the server said rather than a summary of it: the
            # detail names the blocking run, when it started, and `--force`.
            # The line that stood here dropped all of it (#613).
            #
            # Kept identical to `BoardCommands._handle_sync`'s 429 branch --
            # same refusal, same bug, and this one used to omit the sync-status
            # hint that the success branch nine lines above prints, so the
            # operator with a *wedged* board got less help than the one whose
            # sync queued fine.
            #
            # Exits 1, like every other "I did not do what you asked" in this
            # CLI (#622). It returned 0 until then, so `innoday sync` in a
            # script was indistinguishable from a sync that queued -- and the
            # caller that most needs to know is the automated one, which never
            # reads the warning line.
            try:
                error_detail = response.json() if response.content else {}
            except json.JSONDecodeError:
                # A 429 from a proxy in front of the API is HTML, not JSON.
                # `src/cli/client.py` is where this guard is settled.
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
            return 1
        else:
            console.print(
                format_error(
                    f"Board sync failed: HTTP {response.status_code} -- {response.text}"
                )
            )
            return 1

    @staticmethod
    async def _sync_repos(
        client: InnoDayAPIClient, org_id: str, project_id: str
    ) -> int:
        """Discover/reconcile the project's repos by GitHub topic label."""
        response = await client.post(
            f"/organizations/{org_id}/projects/{project_id}/repositories/discover"
        )
        if response.status_code != 200:
            console.print(
                format_error(
                    f"Repo sync failed: HTTP {response.status_code} -- {response.text}"
                )
            )
            return 1

        result = response.json()
        console.print(
            format_success(
                f"Synced {result['repositories_synced']} repositories "
                f"(topic: {result.get('github_label') or 'unset'})"
            )
        )
        if result.get("new_repositories"):
            for repo in result["new_repositories"]:
                console.print(f"  [green]+[/green] {repo['name']}")
        if result.get("deactivated_repositories"):
            for name in result.get("deactivated_repository_names", []):
                console.print(f"  [yellow]-[/yellow] {name} (lost topic label)")
        return 0

    @staticmethod
    async def _report_releases(
        client: InnoDayAPIClient, org_id: str, project_id: str
    ) -> None:
        """
        Report current release state. There is no external source to sync
        releases *from* (unlike tickets/repos) -- releases are created/updated
        directly via `innoday releases create`/`update`, so this step is a
        status report, not a sync.
        """
        response = await client.get(
            f"/organizations/{org_id}/releases", params={"project_id": project_id}
        )
        if response.status_code != 200:
            console.print(format_warning("Could not fetch current releases."))
            return

        # The endpoint has no limit param -- it returns everything (already
        # newest-first); trim to the 5 most recent for this summary view,
        # matching the CLI's own `releases list` command's client-side trim.
        releases = response.json()
        if not releases:
            console.print(
                format_info(
                    "No releases yet for this project. "
                    "Create one with 'innoday releases create <version>'."
                )
            )
            return

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Version", style="bold")
        table.add_column("Status")
        table.add_column("Released")

        for r in releases[:5]:
            released_at = (r.get("released_at") or "")[:10]
            table.add_row(r.get("version", ""), r.get("status", ""), released_at)

        console.print(table)

    @staticmethod
    async def _handle_ticket_sync(
        args: argparse.Namespace, client: InnoDayAPIClient, config
    ) -> int:
        """Handle sync ticket command — fetch and upsert a single ticket immediately."""
        org_alias = config.get_current_organization()
        org_id = config.get_organization_id(org_alias)

        if not org_id:
            console.print(
                format_error(
                    "Organization ID not found. Please reconfigure with 'innoday config init'."
                )
            )
            return 1

        # Resolve the org's single active board registration
        response = await client.get(f"/organizations/{org_id}/boards")
        if response.status_code != 200:
            console.print(
                format_error(f"Failed to look up board registration: {response}")
            )
            return 1

        boards = response.json()
        if not boards:
            console.print(
                format_error(
                    "No active board registered for this organization. "
                    "Register one with 'innoday board register'."
                )
            )
            return 1

        board = boards[0]
        board_id = board["id"]

        # No credential is read from this machine and none is sent: the
        # server resolves the board's own credential from Vault (#609).
        try:
            response = await client.post(
                f"/organizations/{org_id}/boards/{board_id}/tickets/{args.key}/sync",
            )
        except APIError as e:
            console.print(format_error(f"Sync failed: {str(e)}"))
            return 1

        if response.status_code == 200:
            data = response.json()
            ticket = data["ticket"]
            verb = "Created" if data["was_created"] else "Updated"

            console.print(format_success(f"✅ {verb} ticket {args.key}"))
            console.print(f"  Summary: {ticket['summary']}")
            console.print(f"  Status: {ticket['status']}")
            if ticket.get("url"):
                console.print(f"  URL: {ticket['url']}")

            return 0
        elif response.status_code == 404:
            error_detail = response.json() if response.content else {}
            console.print(
                format_error(
                    error_detail.get("detail", f"Ticket '{args.key}' not found")
                )
            )
            return 1
        else:
            error_msg = response.json() if response.content else str(response)
            console.print(format_error(f"Failed to sync ticket: {error_msg}"))
            return 1
