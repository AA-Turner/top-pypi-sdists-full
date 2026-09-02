"""
InnoDay CLI Status Command

Developer-facing `innoday status`: reports API connectivity, identity,
org memberships (with role), and per-project assigned-ticket counts in
one call. Distinct from `innoday platform status`, which reports on the
local process/service state of the API and UI the CLI itself started.
"""

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, List

import httpx
from rich.console import Console
from rich.table import Table

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.config import CLIConfig
from src.cli.utils.formatters import format_datetime, format_error
from src.cli.utils.project_context import (
    LegacyProjectFileError,
    load_project_context,
)

console = Console()


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

        # Best-effort: which stored CLI token is active, and when it expires.
        token_block = await StatusCommands._token_info(api_url, config)

        orgs = []
        if user_info.get("id"):
            try:
                async with InnoDayAPIClient(config) as client:
                    orgs = await StatusCommands._get_orgs_with_projects(client)
            except (APIError, httpx.HTTPError):
                orgs = []

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
            "orgs": [
                {"id": o["id"], "name": o["name"], "role": o.get("role")} for o in orgs
            ],
            "projects": [p for o in orgs for p in o["projects"]],
        }

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            StatusCommands._display_table(result)

        return 0

    @staticmethod
    async def _token_info(api_url: str, config: CLIConfig) -> Dict[str, Any]:
        """Report CLI token presence and, best-effort, its server-side expiry.

        Never raises — a missing token, an unauthenticated route, or a network
        error all resolve to a plain present/absent answer.
        """
        token = config.get_cli_token()
        if not token:
            return {"present": False, "expires_at": None, "name": None}

        info: Dict[str, Any] = {"present": True, "expires_at": None, "name": None}
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                response = await client.get(
                    f"{api_url.rstrip('/')}/api/v1/auth/tokens",
                    headers={"Authorization": f"Bearer {token}"},
                )
            if response.status_code == 200:
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
        console.print(f"[bold]Project context:[/bold] org={org} project={project}")
        console.print(f"[dim]  resolved from:[/dim] {source}")
        legacy = context_block.get("legacy_project_file")
        if legacy:
            # An out-of-date project.yml is an actionable error, not a soft
            # warning — surface it in red with the refresh instruction.
            console.print(f"[red]  ✗ {legacy}[/red]")
            console.print(
                "[red]    Run `innoday refresh` to update this workspace.[/red]"
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
        orgs_response = await client.get("/organizations")
        orgs_response.raise_for_status()
        orgs = orgs_response.json()

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
    async def _count_assigned_tickets(
        client: InnoDayAPIClient, org_id: str, project_id: str, user_id: str
    ) -> int:
        """Count tickets assigned to the current user within a project.

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
            return len(response.json())
        except (APIError, httpx.HTTPStatusError):
            return 0

    @staticmethod
    def _display_table(result: Dict[str, Any]) -> None:
        """Render status as rich tables, sectioned API/Identity/Orgs/Projects."""
        api = result["api"]
        console.print(
            f"[bold]API:[/bold] [green]✓ connected[/green] "
            f"({api['url']}, {api['latency_ms']}ms)"
        )

        identity = result["identity"]
        console.print(
            f"[bold]Identity:[/bold] {identity['name']} <{identity['email']}> "
            f"({identity['user_id']})"
        )

        token = result.get("token") or {}
        if token.get("present"):
            expiry = (
                format_datetime(token["expires_at"]) if token.get("expires_at") else "—"
            )
            console.print(
                f"[bold]CLI token:[/bold] [green]present[/green] (expires: {expiry})"
            )
        else:
            console.print(
                "[bold]CLI token:[/bold] [yellow]none[/yellow] (run 'innoday login')"
            )

        context_block = result.get("project") or {}
        org = context_block.get("org_alias") or "—"
        project = context_block.get("project_id") or "—"
        source = context_block.get("source") or "—"
        console.print(f"[bold]Project context:[/bold] org={org} project={project}")
        console.print(f"[dim]  resolved from:[/dim] {source}")
        legacy = context_block.get("legacy_project_file")
        if legacy:
            # An out-of-date project.yml is an actionable error, not a soft
            # warning — surface it in red with the refresh instruction.
            console.print(f"[red]  ✗ {legacy}[/red]")
            console.print(
                "[red]    Run `innoday refresh` to update this workspace.[/red]"
            )

        profile = result["profile"]
        current = profile["current"]
        default = profile["default"]
        if default is None or default == current:
            console.print(f"[bold]Profile:[/bold] {current} (default)")
        else:
            console.print(
                f"[bold]Profile:[/bold] {current} (current, default is: {default})"
            )

        orgs_table = Table(title="Orgs")
        orgs_table.add_column("Name", style="cyan")
        orgs_table.add_column("Role")
        for org in result["orgs"]:
            orgs_table.add_row(org["name"], org.get("role") or "-")
        console.print(orgs_table)

        projects_table = Table(title="Projects")
        projects_table.add_column("Name", style="cyan")
        projects_table.add_column("Assigned Tickets", justify="right")
        for project in result["projects"]:
            projects_table.add_row(
                project["name"], str(project["assigned_ticket_count"])
            )
        console.print(projects_table)
