"""
InnoDay CLI Scheduler

Background sync process that periodically calls the board sync API
for all connected boards in the current organization.
"""

import argparse
import asyncio
import signal
from datetime import datetime, timezone
from typing import Dict, List, Optional

import httpx
from rich.console import Console
from rich.table import Table

console = Console()

DEFAULT_INTERVAL = 30  # minutes


class SchedulerCommands:
    """Board sync scheduler commands."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        subparsers = parser.add_subparsers(
            title="Scheduler Commands",
            dest="scheduler_command",
            help="Background sync scheduler operations",
        )

        start_parser = subparsers.add_parser(
            "start", help="Start the background sync scheduler"
        )
        start_parser.add_argument(
            "--interval",
            type=int,
            default=DEFAULT_INTERVAL,
            metavar="MINUTES",
            help=f"Sync interval in minutes (default: {DEFAULT_INTERVAL})",
        )
        start_parser.add_argument(
            "--api-url",
            default=None,
            metavar="URL",
            help="InnoDay API URL (overrides config)",
        )
        start_parser.add_argument(
            "--org-id",
            default=None,
            metavar="ID",
            help="Organization ID (overrides config)",
        )
        start_parser.add_argument(
            "--run-once",
            action="store_true",
            help="Run a single sync then exit (useful for cron)",
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config) -> int:
        command = getattr(args, "scheduler_command", None)
        if command == "start":
            return await SchedulerCommands._start(args, config)
        console.print(
            "[red]No scheduler command specified. Available: start — "
            "run 'innoday scheduler --help' for details.[/red]"
        )
        return 1

    @staticmethod
    async def _start(args: argparse.Namespace, config) -> int:
        api_url = (getattr(args, "api_url", None) or config.get_api_url()).rstrip("/")
        org_id = getattr(args, "org_id", None)

        if not org_id:
            org_alias = config.get_current_organization()
            if org_alias:
                org_details = config._config.get("organizations", {}).get(org_alias, {})
                org_id = org_details.get("id")

        if not org_id:
            console.print(
                "[red]Organization not configured. Run 'innoday config init' or pass --org-id.[/red]"
            )
            return 1

        interval_minutes = getattr(args, "interval", DEFAULT_INTERVAL)
        run_once = getattr(args, "run_once", False)

        scheduler = _BoardSyncScheduler(
            api_url=api_url,
            org_id=org_id,
            interval_minutes=interval_minutes,
            cli_token=config.get_cli_token(),
            team_secret=config.get_team_secret(),
        )

        if run_once:
            return await scheduler.run_once()
        return await scheduler.run_loop()


class _BoardSyncScheduler:
    """Handles the polling loop and API calls."""

    def __init__(
        self,
        api_url: str,
        org_id: str,
        interval_minutes: int,
        cli_token: Optional[str] = None,
        team_secret: Optional[str] = None,
    ):
        self.api_url = api_url
        self.org_id = org_id
        self.interval_seconds = interval_minutes * 60
        self.cli_token = cli_token
        self.team_secret = team_secret
        self._stop = asyncio.Event()

        # Register SIGINT/SIGTERM so Ctrl+C shuts down cleanly
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                asyncio.get_event_loop().add_signal_handler(sig, self._stop.set)
            except (RuntimeError, NotImplementedError):
                pass

    def _headers(self) -> Dict[str, str]:
        """Identity is the Bearer CLI token, same as src/cli/client.py.

        This used to send `X-User-ID` — a bare, unverified assertion of who the
        caller is. The API no longer accepts it.
        """
        h = {"Content-Type": "application/json"}
        if self.cli_token:
            h["Authorization"] = f"Bearer {self.cli_token}"
        if self.team_secret:
            h["X-Team-Secret"] = self.team_secret
        return h

    async def _list_boards(self, client: httpx.AsyncClient) -> List[Dict]:
        url = f"{self.api_url}/api/v1/organizations/{self.org_id}/boards"
        resp = await client.get(url, headers=self._headers())
        resp.raise_for_status()
        data = resp.json()
        # API may return a list or {"boards": [...]}
        if isinstance(data, list):
            return data
        return data.get("boards", data.get("items", []))

    async def _sync_board(self, client: httpx.AsyncClient, board: Dict) -> Dict:
        board_id = board.get("id")
        url = (
            f"{self.api_url}/api/v1/organizations/{self.org_id}/boards/{board_id}/sync"
        )
        resp = await client.post(url, headers=self._headers(), json={})
        return {
            "board_id": board_id,
            "status_code": resp.status_code,
            "ok": resp.is_success,
        }

    async def _sync_all(self) -> None:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        console.print(f"\n[bold cyan]── Sync run at {now} ──[/bold cyan]")

        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                boards = await self._list_boards(client)
            except Exception as e:
                console.print(f"[red]Failed to list boards: {e}[/red]")
                return

            if not boards:
                console.print("[yellow]No boards found for organization.[/yellow]")
                return

            table = Table(show_header=True, header_style="bold", box=None)
            table.add_column("Board", style="dim")
            table.add_column("Type", style="dim")
            table.add_column("Result")

            tasks = [self._sync_board(client, b) for b in boards]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for board, result in zip(boards, results):
                name = (
                    board.get("board_name") or board.get("name") or board.get("id", "?")
                )
                board_type = board.get("board_type", "")
                if isinstance(result, Exception):
                    table.add_row(name, board_type, f"[red]Error: {result}[/red]")
                elif result["ok"]:
                    table.add_row(name, board_type, "[green]✓ queued[/green]")
                else:
                    table.add_row(
                        name,
                        board_type,
                        f"[yellow]HTTP {result['status_code']}[/yellow]",
                    )

            console.print(table)

    async def run_once(self) -> int:
        console.print(
            f"[bold]InnoDay Sync[/bold] — org [cyan]{self.org_id}[/cyan] → [cyan]{self.api_url}[/cyan]"
        )
        try:
            await self._sync_all()
            return 0
        except Exception as e:
            console.print(f"[red]Sync failed: {e}[/red]")
            return 1

    async def run_loop(self) -> int:
        console.print(
            f"[bold]InnoDay Sync Scheduler[/bold] starting\n"
            f"  org:      [cyan]{self.org_id}[/cyan]\n"
            f"  api:      [cyan]{self.api_url}[/cyan]\n"
            f"  interval: [cyan]{self.interval_seconds // 60}m[/cyan]\n"
            f"  [dim]Press Ctrl+C to stop[/dim]"
        )

        while not self._stop.is_set():
            try:
                await self._sync_all()
            except Exception as e:
                console.print(f"[red]Sync error: {e}[/red]")

            # Wait for interval or stop signal
            try:
                await asyncio.wait_for(
                    self._stop.wait(), timeout=float(self.interval_seconds)
                )
            except asyncio.TimeoutError:
                pass

        console.print("\n[dim]Scheduler stopped.[/dim]")
        return 0
