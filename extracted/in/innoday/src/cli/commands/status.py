"""
InnoDay CLI Status Command

Developer-facing `innoday status`: "am I OK, and is this project OK?"

Step 1 is you -- identity, whether your sign-in token is still good, how many
organizations you reach. When a project resolves (the cwd's
.innoday/project.yml, or --org/--project) step 2 is that project: its GitHub
account and repositories, every board with its last sync, and the tickets
assigned to you. Without one, step 2 is the cross-project table.

The project half reads the existing project-health route (with a live probe)
and each board's sync history; it replaced `projects health` and
`board sync-status`, which answered halves of the same question separately.
Distinct from `innoday platform status`, which reports on the local
process/service state of the API and UI the CLI itself started.
"""

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
from rich.markup import escape
from rich.table import Table

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.commands.boards import render_sync_record
from src.cli.config import CLIConfig
from src.cli.utils import guidance
from src.cli.utils.context import ContextError, resolve_context
from src.cli.utils.formatters import ProgressReporter, format_datetime, format_error
from src.cli.utils.presentation import (
    make_console,
    print_command_header,
    print_step,
)
from src.cli.utils.project_context import (
    LegacyProjectFileError,
    load_project_context,
)

console = make_console()

#: What a failed board sync tells you to run next. Printed, so it must parse --
#: `tests/test_printed_commands_parse.py` checks every such line.
RETRY_BOARD_SYNC = "innoday sync --scope board"

#: How many assigned tickets to list under the project; the count is always shown.
_TICKETS_SHOWN = 5


def reach_mark(reachable: Optional[bool]) -> str:
    """`✓` / `✗` / `—`, and the dash is not a failure.

    Three-valued throughout the health payload: `None` means nothing was proved
    -- probing was skipped, no credential is stored, the budget ran out --
    which is a different thing from asked-and-did-not-answer. Collapsing the two
    reports a working board as broken.
    """
    if reachable is None:
        return "[muted]—[/muted]"
    return "[good]✓[/good]" if reachable else "[bad]✗[/bad]"


def sync_age(seconds: Optional[int]) -> str:
    """`8d ago`, or `never` in yellow.

    Never-synced is the one age worth colouring: every other value is a number
    whose staleness is the reader's policy, because a board synced hourly and
    one synced weekly are both correct and this cannot tell which it is.
    """
    if seconds is None:
        return "[warn]never[/warn]"
    if seconds < 3600:
        return f"{seconds // 60}m ago"
    if seconds < 86400:
        return f"{seconds // 3600}h ago"
    return f"{seconds // 86400}d ago"


def _normalised(status: Optional[str]) -> str:
    return str(status or "").upper().replace(" ", "_")


class StatusCommands:
    """Developer status command handler."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up the `innoday status` command parser."""
        parser.add_argument("--json", action="store_true", help="Output status as JSON")

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute the `innoday status` command.

        Reports, defensively (never crashing outside a project dir or when
        not logged in): current project resolved from cwd's
        .innoday/project.yml, resolved org/project, logged-in identity, CLI
        token presence + expiry, and API health.
        """
        print_command_header(args, config, "status", show_workspace=True)

        api_url = config.get_api_url()
        user_info = config.get_user_info()
        has_token = bool(config.get_cli_token())

        # Current project/org context resolved from cwd. An outdated project.yml
        # is reported (not crashed on) so `status` still runs and tells the user
        # to refresh.
        # Reuse the context config already resolved at construction time — it
        # honours --dir and records any legacy-file error (config is built with
        # allow_legacy_context for status). Re-calling load_project_context()
        # here would ignore --dir (it defaults to the process cwd) and miss the
        # legacy note entirely.
        legacy_context_note = (
            str(config.legacy_context_error) if config.legacy_context_error else None
        )
        project_context = None
        if not legacy_context_note:
            _dir = getattr(args, "dir", None)
            try:
                project_context = load_project_context(Path(_dir) if _dir else None)
            except LegacyProjectFileError as exc:
                legacy_context_note = str(exc)
        context_block = {
            "source": project_context["source_path"] if project_context else None,
            "org_alias": config.get_current_organization(),
            "org_name": (project_context or {}).get("org_name"),
            "project_id": config.get_current_project_id(),
            "legacy_project_file": legacy_context_note,
        }

        # Fall back gracefully if neither an identity nor a token is present.
        if not user_info.get("id") and not has_token:
            message = (
                "No identity configured. Run 'innoday login' (or 'innoday init') "
                "to get started."
            )
            if args.json:
                print(json.dumps({"error": message, "project": context_block}))
            else:
                console.print(format_error(message))
                StatusCommands._display_context(context_block, token=None)
            return 1

        with ProgressReporter("Connecting to InnoDay…"):
            api_result = await StatusCommands._check_api(api_url)

        if not api_result["connected"]:
            message = (
                f"Cannot reach InnoDay at {api_url}. "
                "Run 'innoday platform status' to check if the server is running."
            )
            if args.json:
                print(json.dumps({"error": message, "api": api_result}))
            else:
                console.print(format_error(message))
            return 1

        # A token but no stored identity -- e.g. right after a fresh config,
        # which is what a set-aside unreadable one leaves (PF-466). Ask the API
        # who the token is, as `whoami` does, instead of showing "None <None>"
        # and empty tables (PF-468).
        if has_token and not user_info.get("id"):
            from src.cli.commands.session import _fetch_me, _persist_user

            with ProgressReporter("Checking who you are…"):
                me = await _fetch_me(
                    api_url, config.get_cli_token(), config.get_team_secret()
                )
            if me:
                _persist_user(config, me)
                user_info = config.get_user_info()
            else:
                message = guidance.SIGN_IN_REJECTED
                if args.json:
                    print(json.dumps({"error": message, "project": context_block}))
                else:
                    console.print(format_error(message))
                return 1

        # Best-effort: which stored CLI token is active, and when it expires.
        with ProgressReporter("Checking your sign-in…"):
            token_block = await StatusCommands._token_info(api_url, config)

        # A project resolved from the cwd (or --org/--project) turns step 2 into
        # that project's integrations; otherwise it is the cross-project table.
        project_mode = bool(
            config.get_current_organization() and config.get_current_project_id()
        )
        orgs: List[Dict[str, Any]] = []
        project_status: Optional[Dict[str, Any]] = None
        context_error: Optional[ContextError] = None
        if user_info.get("id"):
            try:
                async with InnoDayAPIClient(config) as client:
                    if project_mode:
                        with ProgressReporter("Loading your organizations…"):
                            orgs = await StatusCommands._get_orgs(client)
                        try:
                            with ProgressReporter("Checking this project…"):
                                project_status = await StatusCommands._project_status(
                                    config, client, orgs, user_info["id"]
                                )
                        except ContextError as exc:
                            context_error = exc
                    else:
                        with ProgressReporter(
                            "Loading your organizations and projects…"
                        ):
                            orgs = await StatusCommands._get_orgs_with_projects(client)
            except (APIError, httpx.HTTPError):
                pass

        current_profile = config.get_current_profile()
        default_profile = config.get_default_profile()

        result = {
            "api": {
                "url": api_url,
                "connected": True,
                "latency_ms": api_result["latency_ms"],
            },
            "identity": {
                "name": user_info.get("name"),
                "email": user_info.get("email"),
                "user_id": user_info.get("id"),
            },
            "token": token_block,
            "project": context_block,
            "profile": {
                "current": current_profile,
                "default": default_profile,
            },
            "org_count": len(orgs),
            "orgs": [
                {"id": o["id"], "name": o["name"], "role": o.get("role")} for o in orgs
            ],
            # The cross-project table is the no-project answer only; with a
            # project, the per-project detail replaces it.
            "projects": (
                None
                if project_mode
                else [p for o in orgs for p in o.get("projects", [])]
            ),
            "project_status": project_status,
        }
        if context_error is not None:
            result["project_error"] = context_error.message

        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            StatusCommands._display_you(result)
            console.print()
            if context_error is not None:
                print_step(2, "Project")
                context_error.print(console)
            elif project_status is not None:
                StatusCommands._display_project(project_status)
            else:
                StatusCommands._display_projects(result["projects"] or [])

        return 1 if context_error is not None else 0

    @staticmethod
    async def _token_info(api_url: str, config: CLIConfig) -> Dict[str, Any]:
        """Report CLI token presence and, best-effort, its server-side expiry.

        Never raises — a missing token, an unauthenticated route, or a network
        error all resolve to a plain present/absent answer.
        """
        token = config.get_cli_token()
        if not token:
            return {"present": False, "valid": None, "expires_at": None, "name": None}

        info: Dict[str, Any] = {
            "present": True,
            "valid": None,
            "expires_at": None,
            "name": None,
        }
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                response = await client.get(
                    f"{api_url.rstrip('/')}/api/v1/auth/tokens",
                    headers={"Authorization": f"Bearer {token}"},
                )
            # `valid` is three-valued like `reachable`: a 401 is a verdict, a
            # 5xx or a network error proves nothing either way.
            if response.status_code == 401:
                info["valid"] = False
            if response.status_code == 200:
                info["valid"] = True
                tokens = response.json() or []
                # We only hold the raw token, not its id, so we can't match a
                # specific row; if there's exactly one, surface its expiry.
                if len(tokens) == 1:
                    info["expires_at"] = tokens[0].get("expires_at")
                    info["name"] = tokens[0].get("name")
        except httpx.HTTPError:
            pass
        return info

    @staticmethod
    def _display_context(context_block: Dict[str, Any], token) -> None:
        """Render the project/token context lines (used in the no-identity path too)."""
        org = context_block.get("org_alias") or "—"
        project = context_block.get("project_id") or "—"
        source = context_block.get("source") or "—"
        console.print(f"  [muted]context[/muted] org={org} project={project}")
        console.print(f"[muted]    resolved from {source}[/muted]")
        legacy = context_block.get("legacy_project_file")
        if legacy:
            # An out-of-date project.yml is an actionable error, not a soft
            # warning — surface it in red with the refresh instruction.
            console.print(f"  [bad]✗ {legacy}[/bad]")
            console.print(
                "[bad]    Run `innoday refresh` to update this workspace.[/bad]"
            )
        if token is not None:
            present = "yes" if token.get("present") else "no"
            console.print(f"[bold]CLI token:[/bold] {present}")

    @staticmethod
    async def _check_api(api_url: str) -> Dict[str, Any]:
        """Check API connectivity against the unauthenticated public status endpoint."""
        start = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as http_client:
                response = await http_client.get(
                    f"{api_url.rstrip('/')}/api/v1/public/status"
                )
            latency_ms = round((time.monotonic() - start) * 1000, 1)
            return {"connected": response.is_success, "latency_ms": latency_ms}
        except (httpx.ConnectError, httpx.TimeoutException):
            return {"connected": False, "latency_ms": None}

    @staticmethod
    async def _get_orgs_with_projects(client: InnoDayAPIClient) -> List[Dict[str, Any]]:
        """Fetch orgs with role, and per-project assigned-ticket counts for each."""
        user_id = client.user_id
        orgs = await StatusCommands._get_orgs(client)

        result = []
        for org in orgs:
            org_id = org["id"]
            projects: List[Dict[str, Any]] = []
            try:
                projects_response = await client.get(
                    f"/organizations/{org_id}/projects"
                )
                projects_response.raise_for_status()
                for project in projects_response.json():
                    count = await StatusCommands._count_assigned_tickets(
                        client, org_id, project["id"], user_id
                    )
                    projects.append(
                        {
                            "id": project["id"],
                            "name": project["name"],
                            "assigned_ticket_count": count,
                        }
                    )
            except (APIError, httpx.HTTPStatusError):
                projects = []

            result.append(
                {
                    "id": org_id,
                    "name": org["name"],
                    "role": org.get("role"),
                    "projects": projects,
                }
            )

        return result

    @staticmethod
    async def _get_orgs(client: InnoDayAPIClient) -> List[Dict[str, Any]]:
        """The organizations the caller belongs to, with their role."""
        response = await client.get("/organizations")
        response.raise_for_status()
        return response.json() or []

    @staticmethod
    async def _project_status(
        config: CLIConfig,
        client: InnoDayAPIClient,
        orgs: List[Dict[str, Any]],
        user_id: str,
    ) -> Dict[str, Any]:
        """Everything step 2 shows for one project, from existing routes only.

        Health (with a live probe) gives GitHub reachability, discovery age and
        every board's reachability and last real sync; each board's
        sync-history row gives what that last run did, or the error it hit.
        Every read past the context is best-effort: a route that fails leaves
        its part blank rather than blanking the whole report.
        """
        ctx = await resolve_context(config, client)
        org = next((o for o in orgs if o.get("id") == ctx.org_id), {})
        project: Dict[str, Any] = {}
        try:
            response = await client.get(f"/organizations/{ctx.org_id}/projects")
            if response.status_code == 200:
                project = next(
                    (p for p in response.json() or [] if p.get("id") == ctx.project_id),
                    {},
                )
        except (APIError, httpx.HTTPError):
            pass

        base = f"/organizations/{ctx.org_id}/projects/{ctx.project_id}"
        health: Dict[str, Any] = {}
        health_error: Optional[str] = None
        try:
            response = await client.get(f"{base}/health", params={"probe": "true"})
            if response.status_code == 200:
                health = response.json() or {}
            elif response.status_code == 403:
                health_error = "Integration health needs the DEVELOPER role or above"
            else:
                health_error = (
                    f"Integration health unavailable (HTTP {response.status_code})"
                )
        except (APIError, httpx.HTTPError) as exc:
            health_error = f"Integration health unavailable: {exc}"

        repository_count: Optional[int] = None
        try:
            response = await client.get(f"{base}/repositories")
            if response.status_code == 200:
                repository_count = len(response.json() or [])
        except (APIError, httpx.HTTPError):
            pass

        boards = []
        for board in health.get("boards") or []:
            last_sync = None
            try:
                response = await client.get(
                    f"/organizations/{ctx.org_id}/boards/{board.get('id')}/sync-history",
                    params={"limit": 1},
                )
                if response.status_code == 200:
                    entries = response.json() or []
                    last_sync = entries[0] if entries else None
            except (APIError, httpx.HTTPError):
                pass
            boards.append({**board, "last_sync": last_sync})

        tickets = await StatusCommands._assigned_tickets(
            client, ctx.org_id, ctx.project_id, user_id
        )

        return {
            "org": {
                "id": ctx.org_id,
                "alias": org.get("alias") or ctx.org_ref,
                "name": org.get("name"),
            },
            "project": {
                "id": ctx.project_id,
                "alias": project.get("alias") or ctx.project_ref,
                "name": project.get("name") or ctx.project_ref,
            },
            "status": health.get("status"),
            "error": health_error,
            "github": (
                {**(health.get("github") or {}), "repository_count": repository_count}
                if health
                else {"repository_count": repository_count}
            ),
            "boards": boards,
            "assigned_tickets": [
                {
                    "id": t.get("id"),
                    "external_ticket_id": t.get("external_ticket_id"),
                    "summary": t.get("summary"),
                    "status": t.get("status"),
                }
                for t in tickets
            ],
        }

    @staticmethod
    async def _assigned_tickets(
        client: InnoDayAPIClient, org_id: str, project_id: str, user_id: str
    ) -> List[Dict[str, Any]]:
        """Tickets assigned to the current user within a project; [] on error.

        `assigned_to`, not `assignee`: the latter matches the board's own
        display-name string, so a user id sent there matches nothing at all
        and every project silently reports zero.
        """
        try:
            response = await client.get(
                f"/organizations/{org_id}/projects/{project_id}/tickets",
                params={"assigned_to": user_id},
            )
            response.raise_for_status()
            return response.json() or []
        except (APIError, httpx.HTTPStatusError):
            return []

    @staticmethod
    async def _count_assigned_tickets(
        client: InnoDayAPIClient, org_id: str, project_id: str, user_id: str
    ) -> int:
        """Count tickets assigned to the current user within a project."""
        return len(
            await StatusCommands._assigned_tickets(client, org_id, project_id, user_id)
        )

    @staticmethod
    def _display_you(result: Dict[str, Any]) -> None:
        """Step 1: who you are, whether your sign-in holds, what you can reach."""
        api = result["api"]
        console.print()
        print_step(1, "You")
        identity = result["identity"]
        console.print(
            f"  [good]✓[/good] {escape(str(identity['name']))} "
            f"[muted]<{escape(str(identity['email']))}>[/muted]"
        )
        console.print(f"[muted]    {identity['user_id']}[/muted]")

        token = result.get("token") or {}
        expiry = format_datetime(token["expires_at"]) if token.get("expires_at") else ""
        expiry_note = f" [muted]· expires {expiry}[/muted]" if expiry else ""
        if not token.get("present"):
            console.print(
                "  [warn]⚠[/warn] no CLI token [muted]· run 'innoday login'[/muted]"
            )
        elif token.get("valid") is False:
            console.print(
                "  [bad]✗[/bad] CLI token rejected [muted]· run 'innoday login'[/muted]"
            )
        elif token.get("valid"):
            console.print(f"  [good]✓[/good] CLI token valid{expiry_note}")
        else:
            console.print(f"  [good]✓[/good] CLI token present{expiry_note}")

        orgs = result.get("orgs") or []
        count = len(orgs)
        names = ", ".join(escape(str(o["name"])) for o in orgs)
        mark = "[good]✓[/good]" if count else "[warn]⚠[/warn]"
        console.print(
            f"  {mark} {count} organization{'' if count == 1 else 's'}"
            + (f" [muted]· {names}[/muted]" if names else "")
        )
        console.print(
            f"  [muted]connected[/muted] {escape(str(api['url']))} "
            f"[muted]· {api['latency_ms']}ms[/muted]"
        )

        context_block = result.get("project") or {}
        legacy = context_block.get("legacy_project_file")
        if legacy:
            # An out-of-date project.yml is an actionable error, not a soft
            # warning — surface it in red with the refresh instruction.
            console.print(f"  [bad]✗ {escape(str(legacy))}[/bad]")
            console.print(
                "[bad]    Run `innoday refresh` to update this workspace.[/bad]"
            )

        profile = result["profile"]
        current = profile["current"]
        default = profile["default"]
        if default is None or default == current:
            console.print(f"  [muted]profile[/muted] {current} (default)")
        else:
            console.print(
                f"  [muted]profile[/muted] {current} "
                f"[muted](current, default is: {default})[/muted]"
            )

    @staticmethod
    def _display_project(detail: Dict[str, Any]) -> None:
        """Step 2 with a project: GitHub, each board, and your tickets."""
        org = detail["org"]
        project = detail["project"]
        print_step(2, f"{project['name']} ({org['alias']}/{project['alias']})")

        if detail.get("error"):
            console.print(f"  [bad]✗ {escape(detail['error'])}[/bad]")

        github = detail.get("github") or {}
        parts = [escape(str(github.get("github_org") or "GitHub"))]
        repos = github.get("repository_count")
        if repos is not None:
            parts.append(f"{repos} repo{'' if repos == 1 else 's'}")
        age = github.get("last_sync_age_seconds")
        parts.append(
            f"discovered {sync_age(age)}"
            if age is not None
            else "[warn]never discovered[/warn]"
        )
        reachable = github.get("reachable")
        if reachable is not True and github.get("detail"):
            style = "bad" if reachable is False else "muted"
            parts.append(f"[{style}]{escape(str(github['detail']))}[/{style}]")
        console.print(f"  {reach_mark(reachable)} GitHub  " + " · ".join(parts))

        boards = detail.get("boards") or []
        if not boards and not detail.get("error"):
            console.print("  [warn]⚠[/warn] no board registered for this project")
        for board in boards:
            StatusCommands._display_board(board)

        tickets = detail.get("assigned_tickets") or []
        count = len(tickets)
        console.print(
            f"  [muted]•[/muted] {count} ticket{'' if count == 1 else 's'} "
            "assigned to you"
        )
        for ticket in tickets[:_TICKETS_SHOWN]:
            key = ticket.get("external_ticket_id") or str(ticket.get("id") or "")[:8]
            console.print(
                f"      {escape(str(key))}  [muted]{escape(str(ticket.get('status') or ''))}"
                f"[/muted]  {escape(str(ticket.get('summary') or ''))}"
            )
        if count > _TICKETS_SHOWN:
            console.print(
                f"      [muted]… and {count - _TICKETS_SHOWN} more · "
                "innoday tickets list[/muted]"
            )

    @staticmethod
    def _display_board(board: Dict[str, Any]) -> None:
        """One board: name, type, last sync age and result, tickets found.

        The age is health's last *real* sync (dry runs excluded); the result and
        counts are the latest sync-history row, which is what a retry acts on.
        """
        record = board.get("last_sync") or {}
        status = _normalised(record.get("sync_status") or board.get("last_sync_status"))
        if status == "COMPLETED":
            mark = "[good]✓[/good]"
        elif status == "FAILED":
            mark = "[bad]✗[/bad]"
        elif status in ("PENDING", "IN_PROGRESS"):
            mark = "[warn]…[/warn]"
        else:
            mark = "[muted]—[/muted]"

        parts = [
            f"{escape(str(board.get('name') or '-'))} · "
            f"{escape(str(board.get('board_type') or '-'))}"
        ]
        age = board.get("last_sync_age_seconds")
        parts.append(
            f"synced {sync_age(age)}"
            if age is not None
            else "[warn]never synced[/warn]"
        )
        if status == "FAILED":
            parts.append("[bad]last sync failed[/bad]")
        elif status in ("PENDING", "IN_PROGRESS"):
            parts.append("[warn]sync in progress[/warn]")
        if record.get("tickets_found") is not None:
            parts.append(f"{record['tickets_found']} tickets found")
        if board.get("reachable") is False:
            parts.append(
                f"[bad]unreachable: {escape(str(board.get('detail') or 'refused'))}[/bad]"
            )
        elif board.get("is_active") is False:
            parts.append("[muted]inactive[/muted]")
        console.print(f"  {mark} " + " · ".join(parts))

        if status == "FAILED" and record:
            render_sync_record(record, indent=6)
            console.print(
                f"      Retry: {RETRY_BOARD_SYNC}  [muted](re-syncs every board in this project)[/muted]"
            )

    @staticmethod
    def _display_projects(projects: List[Dict[str, Any]]) -> None:
        """Step 2 without a project: every project and your tickets in each."""
        print_step(2, "Projects")
        projects_table = Table(header_style="muted")
        projects_table.add_column("Name", style="header")
        projects_table.add_column("Assigned Tickets", justify="right")
        for project in projects:
            projects_table.add_row(
                escape(str(project["name"])), str(project["assigned_ticket_count"])
            )
        console.print(projects_table)
        console.print(
            "[muted]  Run from a project workspace (or pass --org/--project) "
            "to see its GitHub and board integrations.[/muted]"
        )
