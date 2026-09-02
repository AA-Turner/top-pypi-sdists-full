#!/usr/bin/env python3
"""
InnoDay CLI - Main Entry Point

A comprehensive command-line interface for the InnoDay platform that provides
ticket management, agent interaction, and system utilities.
"""

import argparse
import sys
import traceback
from typing import List, Optional

from colorama import init as colorama_init
from rich.console import Console

from src.cli.commands.auth import AuthCommands
from src.cli.commands.boards import BoardCommands
from src.cli.commands.config import ConfigCommands
from src.cli.commands.git_sync import GitSyncCommands
from src.cli.commands.license import LicenseCommands
from src.cli.commands.organizations import OrganizationCommands
from src.cli.commands.platform import PlatformCommands
from src.cli.commands.platform_admin import PlatformAdminCommands
from src.cli.commands.projects import ProjectCommands
from src.cli.commands.release_proxy import ReleaseProxyCommands
from src.cli.commands.releases import ReleasesCommands
from src.cli.commands.repositories import RepositoryCommands
from src.cli.commands.scheduler import SchedulerCommands
from src.cli.commands.scopes import ScopeCommands
from src.cli.commands.services import ServiceCommands
from src.cli.commands.session import SessionCommands
from src.cli.commands.status import StatusCommands
from src.cli.commands.summary import SummaryCommands
from src.cli.commands.sync import SyncCommands
from src.cli.commands.tickets import TicketCommands
from src.cli.commands.timeline import TimelineCommands
from src.cli.commands.upgrade import UpgradeCommands
from src.cli.commands.utils import UtilityCommands
from src.cli.commands.workspace import WorkspaceCommands
from src.cli.config import CLIConfig
from src.cli.utils.formatters import describe_exception, format_error, format_warning
from src.version import get_display_version


def setup_colorama():
    """Initialize colorama for cross-platform colored output."""
    colorama_init(autoreset=True)


#: Commands that never touch an organization. Priming for these would spend a
#: request to answer a question they do not ask -- and `login` in particular runs
#: before there is anything to authenticate with.
_NO_ORG_COMMANDS = {
    "login",
    "logout",
    "whoami",
    "config",
    "platform",
    "platform-admin",
    "upgrade",
    "ping",
    "version",
    "start",
    "stop",
    "restart",
    "logs",
    "init",
    "join",
}


async def _prime_org_id(config, command) -> None:
    """Cache the resolved organization UUID before dispatch, if it is missing.

    Silent on failure: the commands themselves report an unresolvable
    organization far better than an exception raised here, out of context, would.
    """
    if command in _NO_ORG_COMMANDS:
        return
    alias = config.get_current_organization()
    if not alias or config.get_organization_id(alias):
        return

    from src.cli.client import InnoDayAPIClient
    from src.cli.utils.context import _resolve_org_id

    client = InnoDayAPIClient(config)
    try:
        await _resolve_org_id(config, client, alias)
    except Exception:  # noqa: BLE001 -- see the docstring
        pass
    finally:
        await client.close()


async def _prime_project_id(config, args) -> Optional[str]:
    """Resolve an explicit `--project ALIAS` to a UUID before dispatch.

    The organization half of this was done centrally; the project half was not,
    and the asymmetry shipped a silent wrong answer. `--org` is only ever a
    prefix that `_build_api_url` inserts inside the generic verbs, so resolving
    it there was enough. A project ref is different: commands bake it into a
    `project_id` **query parameter** or into the endpoint string itself, before
    any verb runs. So it has to be resolved here, ahead of dispatch, or each of
    the thirteen command modules has to remember to do it -- and they did not.

    What that cost, measured against the deployed API:

        innoday --org hs --project PF releases list   -> "No releases found"
        innoday --org hs --project PF tickets list    -> "Project 'PF' not found"

    with the same commands returning three releases and 362 tickets when given
    the project's UUID. The first is the worse of the two: `Release.project_id`
    is a UUID column, so filtering it by the alias matches nothing and the route
    answers `HTTP 200` with an empty list. Nothing looks broken.

    Unlike `_prime_org_id` this does **not** fail silently. The ref here was
    typed on the command line this invocation; if it does not name a project the
    caller can reach, saying so beats letting a downstream route answer 404 --
    or, worse, answer nothing at all. Returns an error message to print, or None.

    Costs nothing in a workspace: `.innoday/project.yml` stores the UUID, so the
    ref is already a UUID and this returns before opening a client.
    """
    from src.cli.utils.context import (
        ContextError,
        _resolve_org_id,
        _resolve_project_id,
        looks_like_uuid,
    )

    if args.command in _NO_ORG_COMMANDS:
        return None
    ref = config.get_current_project_id()
    if not ref or looks_like_uuid(ref):
        return None
    org_alias = config.get_current_organization()
    if not org_alias:
        return None

    from src.cli.client import InnoDayAPIClient

    client = InnoDayAPIClient(config)
    try:
        org_id = await _resolve_org_id(config, client, org_alias)
        project_id = await _resolve_project_id(client, org_id, ref)
    except ContextError as exc:
        hint = f" {exc.hint}" if exc.hint else ""
        return f"{exc.message}{hint}"
    except Exception:  # noqa: BLE001 -- a transport failure is the command's to report
        return None
    finally:
        await client.close()

    config.set_project_override(project_id)
    # Modules that read the flag off the namespace rather than through the
    # config (`releases`, `tickets`) would otherwise still hold the alias.
    if getattr(args, "project_id", None):
        args.project_id = project_id
    return None


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the main argument parser."""
    parser = argparse.ArgumentParser(
        prog="innoday",
        description="InnoDay CLI - AI-Powered Team Orchestration Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  innoday login                          # Authenticate the CLI (device flow)
  innoday status                         # Check connectivity, identity, orgs, tickets
  innoday init hs/pf                     # Onboard a project workspace by alias
  innoday join hs                        # Join an org and onboard, in one step
  innoday refresh                        # Re-onboard the current project (cwd)
  innoday platform start                 # Start all services
  innoday platform status                # Check service status
  innoday config init                    # Configure CLI settings only
  innoday tickets list --status TODO     # List TODO tickets
  innoday summary                        # What you did in the last 3 days
  innoday summary --scrum                # ...for the whole team

Version: {get_display_version()}
For more help: innoday <command> --help
        """.strip(),
    )

    # Global options
    parser.add_argument("--config", metavar="PATH", help="Custom config file path")
    parser.add_argument(
        "--profile", metavar="NAME", help="Use a named config profile (e.g. dev, local)"
    )
    # `--org` is canonical; `--organization` stays as an accepted spelling so
    # nothing that already types it breaks. Both take an alias OR a UUID -- the
    # CLI resolves an alias before building the request (see utils/context.py for
    # why passing one through to the API is not safe).
    parser.add_argument(
        "--org",
        "--organization",
        dest="organization",
        metavar="ALIAS|ID",
        help="Organization to act on, by alias or id",
    )
    parser.add_argument(
        "--project",
        "--project-id",
        dest="project_id",
        metavar="ALIAS|ID",
        help="Project to act on, by alias or id (same precedence as --org)",
    )
    parser.add_argument(
        "--dir",
        metavar="PATH",
        help=(
            "Directory to resolve .innoday/project.yml context from "
            "(default: current directory)"
        ),
    )
    parser.add_argument("--api-url", metavar="URL", help="Override API URL")
    parser.add_argument(
        "--format",
        choices=["table", "json", "csv"],
        # No default, so that "the user did not ask for a format" is
        # distinguishable from "the user asked for a table". With `"table"`
        # here, `output.format` in ~/.innoday/config.json was persisted,
        # displayed by `config show`, settable by `config set format` -- and
        # could never take effect, because every consumer saw an explicit
        # "table" on the namespace and had nothing to fall back from.
        default=None,
        help="Output format (default: the profile's output.format, or table)",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress non-essential output"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Detailed output")
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )

    # Custom version action to show banner
    class VersionAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            from src.cli.banner import get_banner_config, show_version_banner

            banner_config = get_banner_config()
            if banner_config["show_banners"] and banner_config["show_on_version"]:
                show_version_banner()
            else:
                print(f"InnoDay CLI {get_display_version()}")
            parser.exit()

    parser.add_argument(
        "--version", action=VersionAction, nargs=0, help="Show version information"
    )

    # Subcommands
    subparsers = parser.add_subparsers(
        title="Commands", dest="command", help="Available commands", metavar="<command>"
    )

    # Init command (auth P4, PF-350): programmatic PROJECT onboarding by alias.
    # This is the pixelfuel-claude `onboard-project` skill moved into InnoDay:
    # resolve <org>/<proj> → clone/refresh repos → write .innoday/project.yml.
    # (The old identity/config wizard's job moved to `innoday login`; the wizard
    # itself remains reachable as `innoday config init`.)
    init_parser = subparsers.add_parser(
        "init",
        help="Onboard a project workspace by alias: innoday init <org>/<proj>",
        description="Resolve an org/project by alias, clone or refresh its repos "
        "into ~/workspaces/<org>/<proj>/, write .innoday/project.yml, and install "
        "the pixelfuel-managed pre-commit hook into each repo (pass --no-hooks to "
        "skip). Run `innoday login` first to authenticate.",
    )
    WorkspaceCommands.setup_init_parser(init_parser)

    # Join an org AND onboard its workspace in one step (auth P4).
    join_parser = subparsers.add_parser(
        "join",
        help="Join an org and onboard its workspace: innoday join <org>[/<proj>]",
        description="Join an organization (self-registration or accepted invite) "
        "and onboard its project workspace in one step. Mimics `init`.",
    )
    WorkspaceCommands.setup_join_parser(join_parser)

    # Re-onboard the CURRENT project (from cwd's .innoday/project.yml) (auth P4).
    refresh_parser = subparsers.add_parser(
        "refresh",
        help="Re-onboard the current project (pull repos, rewrite project.yml)",
        description="Re-run onboarding for the project you're in (reads the cwd's "
        ".innoday/project.yml): pull existing repos, add new, rewrite context.",
    )
    WorkspaceCommands.setup_refresh_parser(refresh_parser)

    # Deprecated top-level service management aliases — moved under `platform`.
    # Excluded from the primary --help listing but still functional; they print
    # a redirect notice and delegate to the same ServiceCommands logic.
    # (help=argparse.SUPPRESS alone doesn't hide subparser choices on this
    # argparse version, so the choice action is dropped explicitly below.)
    # `status` is excluded here — it's reclaimed below for the developer-facing
    # `innoday status` command; the old process-status check now lives only at
    # `innoday platform status`.
    deprecated_service_cmds = ["start", "stop", "restart", "logs"]
    for cmd_name in deprecated_service_cmds:
        cmd_parser = subparsers.add_parser(cmd_name, help=argparse.SUPPRESS)
        ServiceCommands.setup_parser(cmd_parser)
    subparsers._choices_actions = [
        action
        for action in subparsers._choices_actions
        if action.dest not in deprecated_service_cmds
    ]

    # Status command (developer-facing) — connectivity, identity, orgs, projects.
    # Listed first among examples in the epilog below per acceptance criteria.
    status_parser = subparsers.add_parser(
        "status",
        help="Check InnoDay connectivity, identity, orgs, and assigned tickets",
    )
    StatusCommands.setup_parser(status_parser)

    # Session authentication commands (device flow) — top level, gh/railway style.
    login_parser = subparsers.add_parser(
        "login",
        help="Log in to InnoDay via the browser device flow",
        description="Authenticate the CLI against a running InnoDay API using the "
        "OAuth device-authorization flow (or --with-token for CI).",
    )
    SessionCommands.setup_login_parser(login_parser)

    logout_parser = subparsers.add_parser(
        "logout",
        help="Log out and clear stored credentials",
    )
    SessionCommands.setup_logout_parser(logout_parser)

    whoami_parser = subparsers.add_parser(
        "whoami",
        help="Show the currently logged-in identity",
    )
    SessionCommands.setup_whoami_parser(whoami_parser)

    # Configuration commands
    config_parser = subparsers.add_parser(
        "config",
        help="Configuration management",
        description="Manage InnoDay CLI configuration",
    )
    ConfigCommands.setup_parser(config_parser)

    # Authentication commands
    auth_parser = subparsers.add_parser(
        "auth",
        help="Authentication management",
        description="Manage authentication and credentials",
    )
    AuthCommands.setup_parser(auth_parser)

    # Ticket commands
    tickets_parser = subparsers.add_parser(
        "tickets", help="Ticket management", description="Manage tickets and comments"
    )
    TicketCommands.setup_parser(tickets_parser)

    # Board commands
    board_parser = subparsers.add_parser(
        "board",
        help="Board management",
        description="Board management and AI-powered summarization",
    )
    BoardCommands.setup_parser(board_parser)

    # Summary — one command, and the common case takes no flags at all
    # (`innoday summary` = you, last 3 days). Deliberately NOT a group: there
    # is no `summary list|show|ticket|search`. Per-ticket history surfaces
    # through `innoday tickets show`, where someone already is when they want it.
    summary_parser = subparsers.add_parser(
        "summary",
        help="What happened: your work over the last 3 days (--scrum for the team)",
        description="Assemble and render what moved in a window — tickets, "
        "branches and PRs, grouped into active / no-work / unassigned / up-next. "
        "Prose is written by a Claude session (/innoday:summary), never here.",
    )
    SummaryCommands.setup_parser(summary_parser)

    # Timeline — the project's curated event history. Read-only: entries are
    # written by the mutations they describe so the entry and the change land in
    # one transaction (see services/project_timeline_writer.py). Rows have been
    # accumulating since PF-102 with no client at all, which is how "summaries
    # never reached the timeline" stayed invisible.
    timeline_parser = subparsers.add_parser(
        "timeline",
        help="This project's event history — releases, syncs, summaries",
        description="Read a project's curated timeline, newest first. "
        "Entries are written by the events they record; this only reads them.",
    )
    TimelineCommands.setup_parser(timeline_parser)

    # Sync commands
    sync_parser = subparsers.add_parser(
        "sync",
        help="Data synchronization",
        description="Synchronize data with external systems",
    )
    SyncCommands.setup_parser(sync_parser)

    # Scheduler commands
    scheduler_parser = subparsers.add_parser(
        "scheduler",
        help="Background board sync scheduler",
        description="Run a background process that periodically syncs all connected boards",
    )
    SchedulerCommands.setup_parser(scheduler_parser)

    # Git sync commands
    git_parser = subparsers.add_parser(
        "git",
        help="Git platform synchronization",
        description="Manage Git platform integrations (GitHub, GitLab, Jira)",
    )
    GitSyncCommands.setup_parser(git_parser)

    # License commands
    license_parser = subparsers.add_parser(
        "license",
        help="License management",
        description="Manage licenses, usage tracking, and upgrades",
    )
    LicenseCommands.setup_parser(license_parser)

    # Repository commands
    repos_parser = subparsers.add_parser(
        "repos",
        help="Repository management",
        description="Manage repositories and synchronize GitHub issues",
    )
    RepositoryCommands.setup_parser(repos_parser)

    # Organization commands
    orgs_parser = subparsers.add_parser(
        "orgs",
        help="Organization management",
        description="Manage organizations and switch between them",
    )
    OrganizationCommands.setup_parser(orgs_parser)

    # Project commands
    projects_parser = subparsers.add_parser(
        "projects",
        help="Project management",
        description="Manage projects within an organization",
    )
    ProjectCommands.setup_parser(projects_parser)

    # Scope commands
    scope_parser = subparsers.add_parser(
        "scope",
        help="Scope documents and ticket generation",
        description="Manage scope documents and generate tickets with AI",
    )
    ScopeCommands.setup_parser(scope_parser)

    # Releases commands
    releases_parser = subparsers.add_parser(
        "releases",
        help="Release management",
        description="List releases and view release details including summary and changelog",
    )
    ReleasesCommands.setup_parser(releases_parser)

    # `innoday blastoff` -- the deploy command. Drives the blastoff engine with
    # an InnoDay-supplied brief and records the result.
    #
    # **Named after the engine, not "release".** InnoDay has releases as *rows*,
    # planned weeks ahead, so `innoday release` read as though it created one. It
    # does not; it ships the one that already exists. `innoday releases` (plural)
    # is the record API and is a different thing again -- one letter apart, which
    # is exactly the confusion worth removing.
    blastoff_parser = subparsers.add_parser(
        "blastoff",
        help="Deploy: tag repos on GitHub and record the release to InnoDay",
        description="Show what a release would contain, and stop there. Pass "
        "--release to be asked before tagging, --release --yes to tag without "
        "being asked, --hotfix to patch the last released version instead.",
    )
    ReleaseProxyCommands.setup_parser(blastoff_parser, "blastoff")

    # Kept, because they are what people type. `release` is the old name;
    # `hotfix` is the short form of `blastoff --hotfix` and worth keeping on its
    # own merits.
    release_parser = subparsers.add_parser(
        "release",
        help="Alias for `blastoff`",
        description="Alias for `innoday blastoff`.",
    )
    ReleaseProxyCommands.setup_parser(release_parser, "release")

    hotfix_parser = subparsers.add_parser(
        "hotfix",
        help="Alias for `blastoff --hotfix`",
        description="Alias for `innoday blastoff --hotfix`: patch the last "
        "released version rather than cutting the next planned one.",
    )
    ReleaseProxyCommands.setup_parser(hotfix_parser, "hotfix")

    # Platform commands
    platform_parser = subparsers.add_parser(
        "platform",
        help="Platform setup and management",
        description="Setup and manage the InnoDay platform",
    )
    PlatformCommands.setup_parser(platform_parser)

    # Platform Administrator commands
    platform_admin_parser = subparsers.add_parser(
        "platform-admin",
        help="Platform administrator management",
        description="Manage platform administrator/service provider information",
    )
    PlatformAdminCommands.setup_parser(platform_admin_parser)

    # Self-upgrade — reinstall the CLI from PyPI, optionally re-onboard the
    # current project workspace afterward.
    upgrade_parser = subparsers.add_parser(
        "upgrade",
        help="Reinstall the InnoDay CLI from PyPI (optionally refresh the project)",
        description="Self-reinstall the InnoDay CLI via `uv tool install "
        "innoday --reinstall` (latest, or a pinned VERSION), reporting the "
        "installed vs. PyPI-latest version. With --refresh, re-onboard the "
        "current project workspace after a successful reinstall.",
    )
    UpgradeCommands.setup_parser(upgrade_parser)

    # Utility commands (ping, version)
    for cmd_name, cmd_help in [
        ("ping", "Test connectivity"),
        ("health", "API health: status, database, version, environment"),
        ("version", "Show version information"),
    ]:
        cmd_parser = subparsers.add_parser(cmd_name, help=cmd_help)
        UtilityCommands.setup_parser(cmd_parser, cmd_name)

    return parser


async def execute_command(args: argparse.Namespace) -> int:
    """Execute the specified command with the given arguments."""
    try:
        # Load configuration. The upgrade commands (init/join/refresh) regenerate
        # .innoday/project.yml, so they tolerate a legacy/unversioned one. The
        # legacy-tolerant identity/read-only commands (status/whoami/logout) also
        # tolerate it: they still run and display whatever context resolves
        # (status/whoami surface their own `innoday refresh` note) rather than
        # hard-erroring. Every other command hard-errors on a legacy file with a
        # yellow heads-up (see below), prompting `innoday refresh`.
        # `version`/`ping`/`health` are pure diagnostics that never require project
        # context — they must always run (silently, no legacy note) so a user
        # can check their install even inside a workspace with a stale
        # project.yml.
        _upgrade_cmds = {"init", "join", "refresh"}
        _legacy_tolerant = {
            "status",
            "whoami",
            "logout",
            "version",
            "ping",
            "health",
        }
        _legacy_ok = _upgrade_cmds | _legacy_tolerant
        config = CLIConfig(
            config_path=args.config,
            profile=getattr(args, "profile", None),
            organization=args.organization,
            project_id=getattr(args, "project_id", None),
            api_url=args.api_url,
            detect_cwd_context=True,
            allow_legacy_context=args.command in _legacy_ok,
            context_dir=getattr(args, "dir", None),
        )

        # Disable color output if requested
        if args.no_color:
            config.set_color_enabled(False)

        # An outdated .innoday/project.yml in the cwd is a hard stop for every
        # command except the legacy-tolerant ones (`_legacy_ok`: the upgrade
        # commands that regenerate the file, plus status/whoami/logout which
        # display it and warn). Surface the guidance and exit cleanly.
        if config.legacy_context_error and args.command not in _legacy_ok:
            # It's a recoverable one-command-away situation, not a crash — render
            # it as a yellow heads-up, not a red error, and keep the message's own
            # newlines/indentation intact. escape() the message: it embeds the
            # cwd's project.yml path, and a path containing '[' (a dir literally
            # named with brackets) would otherwise be parsed by Rich as a markup
            # tag and garble the output or raise MarkupError.
            from rich.markup import escape

            Console().print(
                f"[yellow]⚠  {escape(str(config.legacy_context_error))}[/yellow]"
            )
            return 1

        # Resolve the organization alias to a UUID once, here, before any
        # command runs.
        #
        # Eight command modules build org-scoped URLs themselves from
        # `config.get_organization_id(alias)`, which is a purely local lookup:
        # the map it reads is written by a workspace, `config init` or
        # `orgs env-setup`, and NOT by `innoday login`. So `--org bp` on a
        # freshly-authenticated machine gave an alias with no id, and 25 call
        # sites each hard-errored (or, worse, emitted an unscoped URL).
        #
        # Priming it centrally fixes all of them without threading a resolver
        # through 25 call sites, and costs one request only when the alias is not
        # already cached -- which, inside a workspace, it always is.
        await _prime_org_id(config, args.command)

        # ...and the project ref likewise, for the reasons in `_prime_project_id`.
        # This one reports rather than swallowing: an unresolvable `--project`
        # otherwise reaches a UUID column as an alias and is answered with an
        # empty list.
        project_error = await _prime_project_id(config, args)
        if project_error:
            Console().print(f"[red]✗ {project_error}[/red]")
            return 1

        # Route to appropriate command handler
        if args.command == "init":
            # auth P4: `init` now onboards a project workspace by alias.
            return await WorkspaceCommands.execute_init(args, config)
        elif args.command == "join":
            return await WorkspaceCommands.execute_join(args, config)
        elif args.command == "refresh":
            return await WorkspaceCommands.execute_refresh(args, config)
        elif args.command in ["start", "stop", "restart", "logs"]:
            # Deprecated top-level service management commands: these spawn
            # processes directly via uv, bypassing containers. `innoday platform
            # start/stop/restart/logs` (docker-compose backed, see
            # PlatformCommands) is now the canonical local run path; `innoday
            # platform status` reports on that process-based service state.
            Console().print(
                format_warning(
                    f"This command has moved to 'innoday platform {args.command}'. "
                    "The old form will be removed in a future release."
                )
            )
            args.service_action = args.command  # Set service action for ServiceCommands
            return await ServiceCommands.execute(args, config)
        elif args.command == "status":
            return await StatusCommands.execute(args, config)
        elif args.command == "login":
            return await SessionCommands.login(args, config)
        elif args.command == "logout":
            return await SessionCommands.logout(args, config)
        elif args.command == "whoami":
            return await SessionCommands.whoami(args, config)
        elif args.command == "config":
            return await ConfigCommands.execute(args, config)
        elif args.command == "auth":
            return await AuthCommands.execute(args, config)
        elif args.command == "tickets":
            return await TicketCommands.execute(args, config)
        elif args.command == "board":
            return await BoardCommands.execute(args, config)
        elif args.command == "summary":
            return await SummaryCommands.execute(args, config)
        elif args.command == "timeline":
            return await TimelineCommands.execute(args, config)
        elif args.command == "sync":
            return await SyncCommands.execute(args, config)
        elif args.command == "scheduler":
            return await SchedulerCommands.execute(args, config)
        elif args.command == "git":
            return await GitSyncCommands.execute(args, config)
        elif args.command == "license":
            return await LicenseCommands.execute(args, config)
        elif args.command == "repos":
            return await RepositoryCommands.execute(args, config)
        elif args.command == "orgs":
            return await OrganizationCommands.execute(args, config)
        elif args.command == "projects":
            return await ProjectCommands.execute(args, config)
        elif args.command == "scope":
            return await ScopeCommands.execute(args, config)
        elif args.command == "releases":
            return await ReleasesCommands.execute(args, config)
        elif args.command in ("blastoff", "release"):
            return await ReleaseProxyCommands.execute_release(args, config)
        elif args.command == "hotfix":
            return await ReleaseProxyCommands.execute_hotfix(args, config)
        elif args.command == "platform":
            return await PlatformCommands.execute(args, config)
        elif args.command == "platform-admin":
            return await PlatformAdminCommands.execute(args, config)
        elif args.command == "upgrade":
            return await UpgradeCommands.execute(args, config)
        elif args.command in ["ping", "health", "version"]:
            return await UtilityCommands.execute(args, config)
        else:
            print(
                format_error("No command specified. Use --help for available commands.")
            )
            return 1

    except KeyboardInterrupt:
        if not args.quiet:
            console = Console()
            console.print("\n[yellow]Operation cancelled by user[/yellow]")
        return 130
    except Exception as e:
        if args.verbose:
            console = Console()
            console.print(format_error(f"Error: {describe_exception(e)}"))
            console.print("[red]Traceback:[/red]")
            traceback.print_exc()
        else:
            console = Console()
            console.print(format_error(f"Error: {describe_exception(e)}"))
            console.print("[yellow]Use --verbose for more details[/yellow]")
        return 1


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    setup_colorama()

    parser = create_parser()
    args = parser.parse_args(argv)

    # Handle case where no command is provided
    if not hasattr(args, "command") or args.command is None:
        parser.print_help()
        return 1

    # Run async command execution
    import asyncio

    return asyncio.run(execute_command(args))


if __name__ == "__main__":
    sys.exit(main())
