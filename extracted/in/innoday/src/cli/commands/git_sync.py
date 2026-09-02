"""
InnoDay CLI Git Commands

Provides the `innoday git sync` command: auto-discover and attach/reconcile
repositories for a project by GitHub topic label. This is the only way repos
are attached to a project -- there is no manual link command.
"""

import argparse

from rich.console import Console
from rich.table import Table

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.config import CLIConfig
from src.cli.utils.formatters import describe_error, format_error, format_success

console = Console()


class GitSyncCommands:
    """Git repository discovery/sync commands."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up git command parser."""
        subparsers = parser.add_subparsers(
            title="Git Commands",
            dest="git_command",
            help="Git repository operations",
        )

        sync_parser = subparsers.add_parser(
            "sync",
            help=(
                "Auto-discover and reconcile a project's repositories by "
                "GitHub topic label. This is the only way repos are attached "
                "to a project -- there is no manual link command."
            ),
        )
        sync_parser.add_argument(
            "--org",
            default=argparse.SUPPRESS,
            help="InnoDay organization by alias or id (defaults to the cwd's "
            ".innoday/project.yml). Same as the global --org.",
        )
        sync_parser.add_argument(
            "--project-id",
            default=argparse.SUPPRESS,
            dest="project_id",
            help="Project ID to sync repos for (defaults to cwd's current project)",
        )
        sync_parser.add_argument(
            "--label",
            dest="github_label",
            help=(
                "GitHub topic to search for. Defaults to the project's alias (lowercased) "
                "(the standing convention) if omitted."
            ),
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute git commands."""
        client = InnoDayAPIClient(config)
        try:
            if args.git_command == "sync":
                return await GitSyncCommands.sync_repos(args, client)
            else:
                console.print(format_error("No git command specified"))
                console.print(
                    "[dim]Available: sync -- run 'innoday git --help' for details[/dim]"
                )
                return 1
        except APIError as e:
            console.print(format_error(str(e)))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            if getattr(args, "verbose", False):
                raise
            return 1
        finally:
            await client.close()

    @staticmethod
    async def sync_repos(args: argparse.Namespace, client: InnoDayAPIClient) -> int:
        """
        Auto-discover and reconcile repositories for a project by GitHub topic label.

        Requires GitHub credentials to already be connected for the organization
        (see `innoday integrations github connect`).
        """
        config = client.config

        org_alias = args.org or config.get_current_organization()
        if not org_alias:
            console.print(
                format_error(
                    "No organization selected. Run this from a directory with "
                    ".innoday/project.yml, or pass --org."
                )
            )
            return 1
        org_id = config.get_organization_id(org_alias)
        if not org_id:
            console.print(
                format_error(
                    f"Organization '{org_alias}' is not in your local config. "
                    "Run 'innoday orgs list' to refresh, or check "
                    ".innoday/project.yml for a stale org reference."
                )
            )
            return 1

        project_id = args.project_id or config.get_current_project_id()
        if not project_id:
            console.print(
                format_error(
                    "No project specified. Pass --project-id, or run this "
                    "command from inside a project directory (one with "
                    ".innoday/project.yml)."
                )
            )
            return 1

        label_note = f" (topic: {args.github_label})" if args.github_label else ""
        console.print(f"[cyan]Syncing repositories for project{label_note}...[/cyan]")

        endpoint = (
            f"/organizations/{org_id}/projects/{project_id}/repositories/discover"
        )
        if args.github_label:
            from urllib.parse import urlencode

            endpoint += f"?{urlencode({'github_label': args.github_label})}"

        response = await client.post(endpoint)

        if response.status_code != 200:
            console.print(
                format_error(
                    f"Sync failed: HTTP {response.status_code} -- {response.text}"
                )
            )
            return 1

        result = response.json()
        new_repos = result.get("new_repositories", [])
        console.print(
            format_success(
                f"Synced {result['repositories_synced']} repositories "
                f"(topic: {result.get('github_label') or 'unset'})"
            )
        )

        if new_repos:
            table = Table(title="Newly Attached Repositories")
            table.add_column("Repository", style="cyan")
            table.add_column("Layer", style="yellow")
            table.add_column("URL", style="dim")

            for repo in new_repos:
                table.add_row(repo["name"], repo["layer"], repo["url"])

            console.print(table)
        else:
            console.print("[dim]No new repositories attached.[/dim]")

        if result.get("reactivated_repositories"):
            console.print(
                f"[dim]{result['reactivated_repositories']} repositories reactivated "
                "(regained the topic label).[/dim]"
            )

        if result.get("updated_repositories"):
            console.print(
                f"[dim]{result['updated_repositories']} existing repositories updated.[/dim]"
            )

        if result.get("deactivated_repositories"):
            names = ", ".join(result.get("deactivated_repository_names", []))
            console.print(
                f"[yellow]{result['deactivated_repositories']} repositories lost the "
                f"topic label and were deactivated: {names}[/yellow]"
            )

        return 0
