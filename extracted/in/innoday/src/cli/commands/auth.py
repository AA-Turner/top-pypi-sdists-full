"""
InnoDay CLI Authentication Commands

Handles authentication and credential management.
"""

import argparse

import httpx
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

from src.cli.config import CLIConfig
from src.cli.utils.formatters import (
    format_datetime,
    format_error,
    format_success,
    format_warning,
)

console = Console()


class AuthCommands:
    """Authentication and credential management commands."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up authentication command parser."""
        subparsers = parser.add_subparsers(
            title="Authentication Commands",
            dest="auth_command",
            help="Authentication operations",
        )

        # Auth status
        subparsers.add_parser("status", help="Show authentication status")

        # Auth logout -- clears the *legacy* unscoped keyring entries only.
        # Kept so anyone who ran the removed `auth login` can still clean up
        # after it; there is no `--service` because there is nothing left that
        # writes per-service entries.
        logout_parser = subparsers.add_parser(
            "logout", help="Remove leftover legacy board credentials"
        )
        logout_parser.add_argument(
            "--confirm", action="store_true", help="Skip confirmation prompt"
        )

        # Auth tokens — manage CLI (device-flow) auth tokens on the server
        tokens_parser = subparsers.add_parser(
            "tokens", help="List and revoke your InnoDay CLI auth tokens"
        )
        tokens_parser.add_argument(
            "--revoke",
            metavar="ID",
            help="Revoke a token by id (from the list)",
        )

        # Auth identity — which name the board calls you, per project
        identity_parser = subparsers.add_parser(
            "identity",
            help="Show or set the board handle that means you on a project",
        )
        identity_parser.add_argument(
            "--set",
            dest="identity_handle",
            metavar="HANDLE",
            help="The name the board (or GitHub) uses for you, e.g. your login",
        )
        identity_parser.add_argument(
            "--platform",
            default="github",
            help=(
                "Which system HANDLE belongs to (default: github — the one the "
                "summary engine matches commits on)"
            ),
        )
        identity_parser.add_argument(
            "--project",
            dest="identity_project",
            metavar="REF",
            help="Project alias or id (default: resolved from the cwd)",
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute authentication command."""
        command = getattr(args, "auth_command", None)

        if command == "status":
            return await AuthCommands._handle_status(args, config)
        elif command == "logout":
            return await AuthCommands._handle_logout(args, config)
        elif command == "tokens":
            return await AuthCommands._handle_tokens(args, config)
        elif command == "identity":
            return await AuthCommands._handle_identity(args, config)
        else:
            console.print(format_error("No authentication command specified"))
            console.print(
                "[dim]Available: status, logout, tokens, identity — "
                "run 'innoday auth --help' for details[/dim]"
            )
            return 1

    @staticmethod
    async def _handle_status(args: argparse.Namespace, config: CLIConfig) -> int:
        """What InnoDay knows about who you are.

        **This used to report on board credentials nothing reads.** It printed
        "Trello ✓ Configured" / "Jira ✗ Not configured" from unscoped keyring
        entries written by the old `auth login`, while every path that actually
        authenticates to a board -- sync, registration, `board set-cred` --
        resolves per-board credentials from Vault or the org-scoped config.
        Someone debugging a failing Jira sync saw a green tick and ruled out
        credentials that sync had never looked at. A status line that reports on
        something the system does not use is worse than no status line.

        What it answers now is only what it can: who you are logged in as, and
        whether this machine holds a CLI token. Board credentials are per board
        -- `innoday board list` is where their state belongs.
        """
        token = config.get_cli_token()
        user = config.get_user_info() or {}
        org_alias = config.get_current_organization()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("", style="cyan")
        table.add_column("", style="white")
        table.add_row(
            "CLI token",
            (
                "[green]✓ present[/green]"
                if token
                else "[red]✗ none — run `innoday login`[/red]"
            ),
        )
        table.add_row("Identity", str(user.get("email") or "—"))
        table.add_row("Organization", str(org_alias or "— (resolved from cwd)"))
        table.add_row("API", config.get_api_url())

        console.print(
            Panel(
                table,
                title="[bold blue]Authentication[/bold blue]",
                border_style="blue",
            )
        )
        console.print(
            "[dim]Board credentials are per board and live server-side — "
            "see `innoday board list`.[/dim]"
        )
        return 0

    @staticmethod
    async def _handle_logout(args: argparse.Namespace, config: CLIConfig) -> int:
        """Clear the leftover *legacy* board credentials from the keyring.

        Kept, narrowed, and deliberately not deleted with `auth login`: anyone
        who ran that command still has entries on their machine, and removing
        the only way to clear them would strand secrets in a keyring with no
        tool that admits they exist. There is no `--service` any more because
        nothing writes per-service entries.

        This does **not** touch the CLI token (`innoday logout` does that) or
        any board credential the platform actually uses -- those live in Vault,
        per board.
        """
        legacy_keys = [
            "trello_api_key",
            "trello_token",
            "jira_url",
            "jira_email",
            "jira_token",
        ]
        present = [key for key in legacy_keys if config.get_credential(key)]
        if not present:
            console.print("[dim]No legacy board credentials stored.[/dim]")
            return 0

        console.print(
            f"[dim]Found {len(present)} legacy entr"
            f"{'y' if len(present) == 1 else 'ies'}: {', '.join(present)}[/dim]"
        )
        if not args.confirm and not Confirm.ask("Remove them?"):
            console.print("Cancelled")
            return 0

        for key in present:
            try:
                config.delete_credential(key)
            except Exception as exc:  # noqa: BLE001 - best effort per key
                console.print(format_warning(f"Could not remove {key}: {exc}"))
        console.print(
            format_success(
                f"Removed {len(present)} legacy entr"
                f"{'y' if len(present) == 1 else 'ies'}"
            )
        )
        return 0

    @staticmethod
    async def _handle_tokens(args: argparse.Namespace, config: CLIConfig) -> int:
        """List (or revoke) the caller's InnoDay CLI auth tokens.

        Talks to the token-management endpoints with the stored Bearer token.
        Requires an active login (`innoday login`) since these routes are
        authenticated.
        """
        token = config.get_cli_token()
        if not token:
            console.print(format_warning("Not logged in — run `innoday login` first."))
            return 1

        base_url = config.get_api_url().rstrip("/")
        headers = {"Authorization": f"Bearer {token}"}
        revoke_id = getattr(args, "revoke", None)

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as client:
                if revoke_id:
                    response = await client.delete(
                        f"{base_url}/api/v1/auth/tokens/{revoke_id}",
                        headers=headers,
                    )
                    if response.status_code in (200, 204):
                        console.print(format_success(f"Revoked token {revoke_id}"))
                        return 0
                    console.print(
                        format_error(
                            f"Could not revoke token (HTTP {response.status_code}): "
                            f"{response.text[:200]}"
                        )
                    )
                    return 1

                response = await client.get(
                    f"{base_url}/api/v1/auth/tokens", headers=headers
                )
        except httpx.HTTPError as exc:
            console.print(format_error(f"Failed to reach InnoDay: {exc}"))
            return 1

        if response.status_code != 200:
            console.print(
                format_error(
                    f"Failed to list tokens (HTTP {response.status_code}): "
                    f"{response.text[:200]}"
                )
            )
            return 1

        tokens = response.json() or []
        if not tokens:
            console.print("[yellow]No CLI tokens found.[/yellow]")
            return 0

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Last Used", style="dim")
        table.add_column("Expires", style="dim")

        for tok in tokens:
            table.add_row(
                str(tok.get("id", "")),
                tok.get("name") or "-",
                format_datetime(tok.get("last_used_at")),
                format_datetime(tok.get("expires_at")),
            )

        console.print(table)
        return 0

    @staticmethod
    async def _handle_identity(args: argparse.Namespace, config: CLIConfig) -> int:
        """Show, or claim, the board handle that means "you" on a project.

        This is the fix `innoday summary` prints when a personal summary comes
        back empty because InnoDay cannot recognise the caller. Until this
        existed the only way to apply that fix was the `/ui/{org}/profile`
        form — so the CLI printed an instruction it had no way to carry out,
        and a personal summary was unreachable from a terminal.

        With no `--set`, it lists what is already mapped, which is the question
        you actually have when a summary comes back empty.
        """
        token = config.get_cli_token()
        if not token:
            console.print(format_warning("Not logged in — run `innoday login` first."))
            return 1

        base_url = config.get_api_url().rstrip("/")
        headers = {"Authorization": f"Bearer {token}"}
        team_secret = config.get_team_secret()
        if team_secret:
            headers["X-Team-Secret"] = team_secret

        handle = getattr(args, "identity_handle", None)

        if not handle:
            try:
                async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as client:
                    response = await client.get(
                        f"{base_url}/api/v1/auth/me", headers=headers
                    )
            except httpx.HTTPError as exc:
                console.print(format_error(f"Failed to reach InnoDay: {exc}"))
                return 1
            if response.status_code != 200:
                console.print(
                    format_error(
                        f"Could not read your profile (HTTP {response.status_code}): "
                        f"{response.text[:200]}"
                    )
                )
                return 1
            identities = (response.json() or {}).get("identities") or []
            if not identities:
                console.print(
                    "[yellow]No board identities mapped.[/yellow]\n"
                    "[dim]Set one with: innoday auth identity "
                    "--set <your-github-login>[/dim]"
                )
                return 0
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Platform", style="cyan")
            table.add_column("Handle", style="white")
            table.add_column("Project", style="dim")
            table.add_column("Scope", style="dim")
            for row in identities:
                table.add_row(
                    str(row.get("platform") or ""),
                    str(row.get("handle") or ""),
                    str(row.get("project") or "—"),
                    str(row.get("scope") or ""),
                )
            console.print(table)
            return 0

        project_ref = getattr(args, "identity_project", None) or (
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

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as client:
                response = await client.put(
                    f"{base_url}/api/v1/auth/me/identities",
                    headers=headers,
                    json={
                        "project_id": project_ref,
                        "platform": getattr(args, "platform", "github"),
                        "handle": handle,
                    },
                )
        except httpx.HTTPError as exc:
            console.print(format_error(f"Failed to reach InnoDay: {exc}"))
            return 1

        if response.status_code != 200:
            detail = response.text[:200]
            try:
                detail = str((response.json() or {}).get("detail") or detail)
            except ValueError:
                pass
            console.print(
                format_error(
                    f"Could not map that handle (HTTP {response.status_code}): {detail}"
                )
            )
            return 1

        console.print(
            format_success(
                f"On {project_ref}, {getattr(args, 'platform', 'github')} "
                f"handle {handle!r} is you."
            )
        )
        return 0
