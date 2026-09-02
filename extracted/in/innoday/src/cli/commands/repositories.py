"""Repository management CLI commands."""

import argparse
from datetime import datetime
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.table import Table

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.config import CLIConfig
from src.cli.utils.formatters import (
    advisory_console,
    format_datetime,
    format_error,
    format_info,
    format_success,
    format_warning,
)
from src.domain.project import RepositoryLayer


class RepositoryCommands:
    """CLI commands for repository management and issue synchronization"""

    def __init__(self, config: CLIConfig):
        self.config = config
        self.console = Console()

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Add repository command parser to the main parser"""
        subparsers = parser.add_subparsers(
            title="Repository Commands",
            dest="repos_action",
            help="Repository operations",
        )

        # repos list command
        repos_list_parser = subparsers.add_parser("list", help="List repositories")
        repos_list_parser.add_argument(
            "--all-projects",
            dest="all_projects",
            action="store_true",
            help=(
                "List every repository in the organization. Without this the "
                "list is scoped to the current project (--project, or the "
                "cwd's .innoday/project.yml)"
            ),
        )

        # repos set-primary command
        set_primary_parser = subparsers.add_parser(
            "set-primary",
            help="Make the current project this repository's primary project",
            description=(
                "A repository's own GitHub Releases are imported as releases of "
                "its PRIMARY project only, so a repo shared between projects "
                "does not push its package version into all of them. Run this "
                "from the workspace of the project that should own the repo's "
                "release path, or pass --project."
            ),
        )
        set_primary_parser.add_argument(
            "name",
            help="Repository name (e.g. innoday-blastoff) or its id",
        )

        # repos set-layer command
        set_layer_parser = subparsers.add_parser(
            "set-layer",
            help="Classify a repository's layer within the current project",
            description=(
                "A repository's layer says what kind of thing it is. It is a "
                "per-project classification, so the same repo can be a UI in "
                "one project and a demo in another. DESIGN is the one layer "
                "that changes how a release reads: a design repository is "
                "still tagged, but its work is narrated in its own section "
                "rather than mixed into what shipped to customers."
            ),
        )
        set_layer_parser.add_argument(
            "name",
            help="Repository name (e.g. bps-ui-demo) or its id",
        )
        set_layer_parser.add_argument(
            "--layer",
            required=True,
            # Derived from the enum rather than typed out: a hand-written list
            # drifts the moment a member is added, and argparse would then
            # reject a layer the server accepts.
            choices=[member.value for member in RepositoryLayer],
            help="The layer to set",
        )

        # repos sync-issues command
        sync_issues_parser = subparsers.add_parser(
            "sync-issues", help="Synchronize GitHub issues for a repository"
        )
        sync_issues_parser.add_argument(
            "--repository-id",
            dest="repository_id",
            required=True,
            help="Repository ID to sync issues for",
        )
        sync_issues_parser.add_argument(
            "--token", required=True, help="GitHub access token"
        )
        sync_issues_parser.add_argument(
            "--state",
            choices=["open", "closed", "all"],
            default="all",
            help="Issue state filter (default: all)",
        )
        sync_issues_parser.add_argument(
            "--since", help="Only sync issues updated after this date (ISO format)"
        )
        sync_issues_parser.add_argument(
            "--dry-run", action="store_true", help="Preview sync without making changes"
        )

        # repos issues command
        issues_parser = subparsers.add_parser("issues", help="List repository issues")
        issues_parser.add_argument(
            "--repository-id",
            dest="repository_id",
            required=True,
            help="Repository ID to list issues for",
        )
        issues_parser.add_argument(
            "--state", choices=["open", "closed"], help="Filter by issue state"
        )
        issues_parser.add_argument("--search", help="Search in issue title and body")
        issues_parser.add_argument(
            "--format",
            choices=["table", "json", "csv"],
            default="table",
            help="Output format (default: table)",
        )

        # repos issues show command
        issue_show_parser = subparsers.add_parser(
            "issue", help="Show specific repository issue"
        )
        issue_show_parser.add_argument(
            "--repository-id",
            dest="repository_id",
            required=True,
            help="Repository ID",
        )
        issue_show_parser.add_argument("issue_id", type=int, help="GitHub issue ID")

        # repos sync-history command
        history_parser = subparsers.add_parser(
            "sync-history", help="Show issue synchronization statistics"
        )
        history_parser.add_argument(
            "--repository-id",
            dest="repository_id",
            required=True,
            help="Repository ID to show sync history for",
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute repository commands"""
        repo_commands = RepositoryCommands(config)
        try:
            return await repo_commands.handle_repositories_command(args)
        except Exception as e:
            console = Console()
            console.print(format_error(f"Repository command failed: {str(e)}"))
            return 1

    async def handle_repositories_command(self, args: argparse.Namespace) -> int:
        """Handle repository commands"""
        try:
            if args.repos_action == "list":
                await self.list_repositories(args)
            elif args.repos_action == "sync-issues":
                await self.sync_repository_issues(args)
            elif args.repos_action == "issues":
                await self.list_repository_issues(args)
            elif args.repos_action == "issue":
                await self.show_repository_issue(args)
            elif args.repos_action == "sync-history":
                await self.show_sync_history(args)
            elif args.repos_action == "set-primary":
                return await self.set_primary_project(args)
            elif args.repos_action == "set-layer":
                return await self.set_layer(args)
            else:
                self.console.print(format_error("No repos action specified"))
                self.console.print(
                    "[dim]Available: list, sync-issues, issues, issue, "
                    "sync-history, set-primary, set-layer — run "
                    "'innoday repos --help' for details[/dim]"
                )
                return 1
        except Exception as e:
            self.console.print(format_error(f"Repository command failed: {str(e)}"))
            return 1

        return 0

    async def _linked_repo(
        self, client: InnoDayAPIClient, name: str, why: str
    ) -> Optional[Dict[str, Any]]:
        """The project-linked repository called `name`, or None with a reason printed.

        Resolving by name rather than by id, because the id is GitHub's numeric
        one and nobody has it to hand. `why` is appended when nothing matches --
        the caller knows what the repo was needed *for*, and "not linked to this
        project" on its own leaves somebody guessing whether that is even the
        problem.
        """
        response = await client.get(
            f"/organizations/{client.organization_id}"
            f"/projects/{client.project_id}/repositories"
        )
        if response.status_code != 200:
            self.console.print(
                format_error(
                    f"Could not list the project's repositories: {response.status_code}"
                )
            )
            return None

        repos = response.json() or []
        wanted = name.strip().lower()
        match = next(
            (
                r
                for r in repos
                if str(r.get("id")) == name
                or (r.get("name") or "").lower() == wanted
                or (r.get("full_name") or "").lower().endswith("/" + wanted)
            ),
            None,
        )
        if match is None:
            self.console.print(
                format_error(f"'{name}' is not linked to this project. {why}")
            )
            if repos:
                names = ", ".join(sorted(r.get("name") or "?" for r in repos))
                self.console.print(f"[dim]Linked here: {names}[/dim]")
            return None
        return match

    async def _require_project(self, client: InnoDayAPIClient, why: str) -> bool:
        """True when an org and a project are both in context, else prints why not."""
        if not client.validate_organization_id():
            self.console.print(format_error("Organization ID is required."))
            return False
        if not client.project_id:
            self.console.print(
                format_error(
                    "No project in context. Run from a project workspace or pass "
                    f"--project: {why}"
                )
            )
            return False
        return True

    async def set_layer(self, args: argparse.Namespace) -> int:
        """Classify a repository's layer within the project in context.

        The layer lives on the project<->repository link, not on the repository,
        so this is a statement about what the repo is *to this project*.

        DESIGN is the member worth knowing about. A design repository -- a demo,
        a prototype -- is still part of the release and still gets tagged; what
        changes is that a release summary gives its work a section of its own
        instead of folding layout experiments into the customer-facing story.
        Before this existed the only way to keep a demo out of the notes was to
        unlink it, which also dropped it from the tag set: one release covered
        six repositories instead of seven and said nothing.
        """
        client = InnoDayAPIClient(self.config)

        if not await self._require_project(
            client, "a layer is a per-project classification."
        ):
            return 1

        match = await self._linked_repo(
            client,
            args.name,
            "A repo must belong to a project before it can be classified in it.",
        )
        if match is None:
            return 1

        update = await client.put(
            f"/organizations/{client.organization_id}/projects/"
            f"{client.project_id}/repositories/{match['id']}",
            json={"layer": args.layer},
        )
        if update.status_code != 200:
            self.console.print(
                format_error(
                    f"Failed to set the layer: {update.status_code} "
                    f"{getattr(update, 'text', '')}"
                )
            )
            return 1

        self.console.print(
            format_success(f"{match.get('name')} is now layer '{args.layer}'.")
        )
        if args.layer == RepositoryLayer.DESIGN.value:
            self.console.print(
                "[dim]It is still tagged by releases. Its work will appear in "
                "the release summary's design section rather than among the "
                "shipped features.[/dim]"
            )
            self.console.print(
                "[dim]Add a 'layer-design' topic on GitHub so repository "
                "rediscovery re-derives this instead of resetting it. "
                "(A topic cannot contain a colon, so 'layer:design' is "
                "rejected by GitHub.)[/dim]"
            )
        return 0

    async def set_primary_project(self, args: argparse.Namespace) -> int:
        """Make the project in context this repository's primary project.

        The primary project owns the repo's release path: `_discover_releases`
        imports a repo's published GitHub Releases only into that project. Without
        it, a repo shared between projects pushes its own package version into all
        of them -- which is how blastoff v0.3.0 became a PF platform release and
        collapsed that release's changelog window.

        Resolving by name rather than requiring an id, because the id is GitHub's
        numeric one and nobody has it to hand.
        """
        client = InnoDayAPIClient(self.config)

        if not client.validate_organization_id():
            self.console.print(format_error("Organization ID is required."))
            return 1
        if not client.project_id:
            self.console.print(
                format_error(
                    "No project in context. Run from a project workspace or pass "
                    "--project: this command decides which project owns the "
                    "repo's releases, so it cannot be inferred."
                )
            )
            return 1

        match = await self._linked_repo(
            client,
            args.name,
            "A repo must belong to a project before it can be its primary.",
        )
        if match is None:
            return 1

        update = await client.put(
            f"/organizations/{client.organization_id}/projects/"
            f"{client.project_id}/repositories/{match['id']}",
            json={"is_primary_project": True},
        )
        if update.status_code != 200:
            self.console.print(
                format_error(
                    f"Failed to set the primary project: {update.status_code} "
                    f"{getattr(update, 'text', '')}"
                )
            )
            return 1

        self.console.print(
            format_success(
                f"{match.get('name')} releases now belong to project "
                f"{client.project_id}."
            )
        )
        self.console.print(
            "[dim]Its GitHub Releases will no longer be imported as releases of "
            "any other project it belongs to.[/dim]"
        )
        return 0

    async def list_repositories(self, args: argparse.Namespace) -> None:
        """List repositories"""
        client = InnoDayAPIClient(self.config)

        try:
            if not client.validate_organization_id():
                raise APIError("Organization ID is required for repository operations")

            # Follow the project in context, like tickets list. Without this
            # `repos list` inside a project workspace answered with every repo
            # in the organization, which reads as the project's own list.
            all_projects = getattr(args, "all_projects", False)
            scoped = bool(client.project_id) and not all_projects

            if scoped:
                response = await client.get(
                    f"/organizations/{client.organization_id}"
                    f"/projects/{client.project_id}/repositories"
                )
            else:
                response = await client.get("repositories")

            if response.status_code != 200:
                self.console.print(
                    format_error(f"Failed to list repositories: {response.status_code}")
                )
                return

            repos = response.json()
            if not repos:
                self.console.print("[yellow]No repositories found.[/yellow]")
                return

            if scoped:
                advisory_console.print(
                    format_info(
                        f"Scoped to project {client.project_id} "
                        "-- pass --all-projects for the whole organization"
                    )
                )

            table = Table(title="Repositories")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="white")
            table.add_column("Language", style="green")
            table.add_column("Layer", style="blue")
            table.add_column("Active", style="magenta")

            for repo in repos:
                table.add_row(
                    str(repo["id"]),
                    repo["name"],
                    repo.get("language") or "N/A",
                    repo.get("layer") or "N/A",
                    "Yes" if repo["is_active"] else "No",
                )

            self.console.print(table)

        except APIError as e:
            self.console.print(format_error(str(e)))
        except Exception as e:
            self.console.print(format_error(f"Failed to list repositories: {str(e)}"))

    async def sync_repository_issues(self, args: argparse.Namespace) -> None:
        """Synchronize GitHub issues for a repository"""
        client = InnoDayAPIClient(self.config)

        try:
            if not client.validate_organization_id():
                raise APIError("Organization ID is required for repository operations")

            # Parse since date if provided
            since_date = None
            if args.since:
                try:
                    since_date = datetime.fromisoformat(args.since)
                except ValueError:
                    self.console.print(
                        format_error(
                            f"Invalid date format: {args.since}. Use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
                        )
                    )
                    return

            # Prepare sync request
            sync_data = {"state_filter": args.state, "dry_run": args.dry_run}
            if since_date:
                sync_data["since"] = since_date.isoformat()

            self.console.print(
                f"🔄 Syncing GitHub issues for repository {args.repository_id}..."
            )
            if args.dry_run:
                self.console.print(
                    "[yellow]📋 DRY RUN MODE - No changes will be saved[/yellow]"
                )

            # Make API request
            http_response = await client.post(
                f"repositories/{args.repository_id}/sync-issues",
                json=sync_data,
                headers={"X-GitHub-Token": args.token},
            )
            if http_response.status_code != 200:
                self.console.print(
                    format_error(f"Failed to sync issues: {http_response.status_code}")
                )
                return

            response = http_response.json()

            if response.get("success"):
                stats = response["statistics"]
                self.console.print(
                    format_success("✅ Issue sync completed successfully!")
                )

                # Display statistics
                table = Table(title="Sync Statistics")
                table.add_column("Metric", style="cyan")
                table.add_column("Count", style="green")

                table.add_row("Issues Fetched", str(stats["total_fetched"]))
                table.add_row("Issues Created", str(stats["issues_created"]))
                table.add_row("Issues Updated", str(stats["issues_updated"]))
                table.add_row("Issues Skipped", str(stats["issues_skipped"]))

                if response.get("duration_seconds"):
                    table.add_row("Duration", f"{response['duration_seconds']:.2f}s")

                self.console.print(table)

                # Show errors if any
                if response.get("errors"):
                    self.console.print("\n[yellow]⚠️ Warnings/Errors:[/yellow]")
                    for error in response["errors"]:
                        self.console.print(f"  • {error}")
            else:
                self.console.print(format_error("❌ Issue sync failed"))
                if response.get("errors"):
                    for error in response["errors"]:
                        self.console.print(format_error(f"  • {error}"))

        except APIError as e:
            self.console.print(format_error(str(e)))
        except Exception as e:
            self.console.print(format_error(f"Failed to sync issues: {str(e)}"))

    async def list_repository_issues(self, args: argparse.Namespace) -> None:
        """List repository issues"""
        client = InnoDayAPIClient(self.config)

        try:
            if not client.validate_organization_id():
                raise APIError("Organization ID is required for repository operations")

            # Build query parameters
            params = {}
            if args.state:
                params["state"] = args.state
            if args.search:
                params["search"] = args.search

            http_response = await client.get(
                f"repositories/{args.repository_id}/issues", params=params
            )
            if http_response.status_code != 200:
                self.console.print(
                    format_error(f"Failed to list issues: {http_response.status_code}")
                )
                return

            # The router returns a bare JSON array (response_model=List[...]),
            # not a {"issues": [...]} wrapper.
            issues = http_response.json()

            if not issues:
                self.console.print(
                    f"[yellow]No issues found for repository {args.repository_id}[/yellow]"
                )
                return

            if args.format == "json":
                import json

                print(json.dumps(issues, indent=2, default=str))
            elif args.format == "csv":
                self._print_issues_csv(issues)
            else:
                self._print_issues_table(issues)

        except APIError as e:
            self.console.print(format_error(str(e)))
        except Exception as e:
            self.console.print(format_error(f"Failed to list issues: {str(e)}"))

    async def show_repository_issue(self, args: argparse.Namespace) -> None:
        """Show detailed information for a specific repository issue"""
        # No single-issue-by-id endpoint exists in the API (only the list
        # endpoint, .../repositories/{repository_id}/issues) -- stub rather
        # than call a route that doesn't exist. If this is ever implemented
        # for real, restore the `client.validate_organization_id()` guard
        # used by every other (non-stub) handler in this class.
        self.console.print(
            format_warning("Showing a single repository issue is not yet implemented.")
        )
        self.console.print(
            "This feature will be available in a future release. "
            "Use 'innoday repos issues --repository-id <id>' to list issues instead."
        )

    async def show_sync_history(self, args: argparse.Namespace) -> None:
        """Show synchronization statistics for a repository"""
        # No issue-sync-history endpoint exists in the API -- stub rather
        # than call a route that doesn't exist. If this is ever implemented
        # for real, restore the `client.validate_organization_id()` guard
        # used by every other (non-stub) handler in this class.
        self.console.print(
            format_warning("Repository sync history is not yet implemented.")
        )
        self.console.print("This feature will be available in a future release.")

    def _print_issues_table(self, issues: List[Dict]) -> None:
        """Print issues in table format"""
        table = Table(title="Repository Issues")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="white", max_width=50)
        table.add_column("State", style="green")
        table.add_column("Updated", style="blue")

        for issue in issues:
            state = "🟢 Open" if issue["is_open"] else "🔴 Closed"
            updated = format_datetime(issue["github_updated_at"])

            table.add_row(str(issue["github_issue_id"]), issue["title"], state, updated)

        self.console.print(table)

    def _print_issues_csv(self, issues: List[Dict]) -> None:
        """Print issues in CSV format"""
        import csv
        import sys

        writer = csv.writer(sys.stdout)
        writer.writerow(["ID", "Title", "State", "GitHub URL", "Created", "Updated"])

        for issue in issues:
            writer.writerow(
                [
                    issue["github_issue_id"],
                    issue["title"],
                    "open" if issue["is_open"] else "closed",
                    issue["github_url"],
                    issue["github_created_at"],
                    issue["github_updated_at"],
                ]
            )
