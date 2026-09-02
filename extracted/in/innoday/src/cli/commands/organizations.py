"""
InnoDay CLI Organization Commands

Handles organization management operations including listing and viewing details.
Org context itself is resolved from cwd's .innoday/project.yml (or an explicit
--organization flag) -- see CLIConfig._apply_cwd_project_context. There is no
persistent "switch" command; org selection is always request-scoped or
directory-scoped, never sticky state a later command can silently inherit.
"""

import argparse
from pathlib import Path
from urllib.parse import quote

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.config import CLIConfig
from src.cli.utils.formatters import (
    OutputFormatter,
    describe_error,
    format_error,
    format_info,
    format_success,
    format_warning,
)
from src.domain.user_identity import IdentityPlatform

console = Console()


class OrganizationCommands:
    """Organization management commands."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up organization command parser."""
        subparsers = parser.add_subparsers(
            title="Organization Commands",
            dest="org_command",
            help="Organization operations",
        )

        # Orgs list
        list_parser = subparsers.add_parser(
            "list",
            help="List all organizations",
            description="List all organizations the user has access to",
        )
        list_parser.add_argument(
            "--show-members",
            action="store_true",
            help="Include member count for each organization",
        )

        # Orgs show
        show_parser = subparsers.add_parser(
            "show",
            help="Show organization details",
            description="Display detailed information about an organization",
        )
        show_parser.add_argument(
            "org_slug",
            nargs="?",
            help="Organization alias (defaults to current organization)",
        )
        show_parser.add_argument(
            "--stats", action="store_true", help="Include statistics"
        )

        # Orgs current
        subparsers.add_parser(
            "current",
            help="Show current organization",
            description="Display the currently active organization",
        )

        # Orgs env-setup
        env_setup_parser = subparsers.add_parser(
            "env-setup",
            help="Create or update org env file (env/orgs/<alias>)",
            description=(
                "Interactive wizard to create env/orgs/<alias> with board "
                "credentials. File is gitignored — safe to store API tokens."
            ),
        )
        env_setup_parser.add_argument(
            "alias",
            nargs="?",
            help="Org alias (e.g. acme). Omit to be prompted.",
        )
        env_setup_parser.add_argument(
            "--update",
            action="store_true",
            help="Update an existing env file (default: warn before overwriting).",
        )

        # Orgs members — list, or add someone by email
        members_parser = subparsers.add_parser(
            "members",
            help="List an organization's members, add one, or change a role",
            description=(
                "List members, add one with --add, or change an existing "
                "member's role with --set-role. Membership is not cosmetic: "
                "IdentityResolutionService will not match a board assignee to a "
                "user who is not an active member of the org, on either the "
                "email or the handle path — so an unmapped assignee is often a "
                "missing membership rather than a missing handle. Nor is the "
                "role: releases, board sync and ticket writes all require "
                "DEVELOPER or higher, so a MEMBER can read everything and "
                "change nothing."
            ),
        )
        members_parser.add_argument(
            "--add",
            dest="member_add",
            metavar="EMAIL_OR_ID",
            help="Add this person. An email is resolved to their user id.",
        )
        members_parser.add_argument(
            "--set-role",
            dest="member_set_role",
            metavar="EMAIL_OR_ID",
            help=(
                "Change this existing member's role to --role. --add refuses an "
                "existing member (409, treated as idempotent), so before this "
                "there was no way to change a role from the CLI at all."
            ),
        )
        members_parser.add_argument(
            "--role",
            dest="member_role",
            default="DEVELOPER",
            choices=["MEMBER", "DEVELOPER", "ADMIN", "OWNER"],
            help=(
                "Role for --add or --set-role (default: DEVELOPER — can sync "
                "boards, write tickets and cut releases). Pass MEMBER for "
                "someone who should only read."
            ),
        )

        # Orgs identities — who a board or commit handle belongs to
        identities_parser = subparsers.add_parser(
            "identities",
            help="List handle mappings, or map/unmap one (admin)",
            description=(
                "Say who a board or commit handle belongs to. Mapping used to be "
                "possible only from the Team page, so it could not be scripted, "
                "could not happen during onboarding, and could not be done by an "
                "agent — a GitHub login resolving to nobody had to be fixed by "
                "writing to the database by hand. A wrong mapping reattributes "
                "somebody else's work in every summary that follows, so --unmap "
                "is as easy as --map."
            ),
        )
        identities_parser.add_argument(
            "--map",
            dest="identity_map",
            metavar="HANDLE",
            help="Map this handle. Requires --user and --platform.",
        )
        identities_parser.add_argument(
            "--unmap",
            dest="identity_unmap",
            metavar="HANDLE",
            help="Remove this handle's mapping. Requires --platform.",
        )
        identities_parser.add_argument(
            "--user",
            dest="identity_user",
            metavar="EMAIL",
            help=(
                "Who the handle is, by email — an admin knows the address, not "
                "the uuid."
            ),
        )
        identities_parser.add_argument(
            "--platform",
            dest="identity_platform",
            # Derived, never hand-listed: a copy of an enum's values drifts from
            # it silently, and this repo has been bitten by exactly that.
            choices=[p.value for p in IdentityPlatform],
            help="Which system the handle comes from.",
        )
        identities_parser.add_argument(
            "--project",
            dest="identity_project",
            metavar="PROJECT_ID",
            help=(
                "Scope a board handle to one project, shadowing any global row. "
                "Ignored for github, which is one login per person."
            ),
        )
        identities_parser.add_argument(
            "--unmapped",
            dest="identity_unmapped",
            action="store_true",
            help=(
                "List the handles that resolve to nobody instead of the "
                "mappings that exist — where onboarding actually starts."
            ),
        )

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute organization command."""
        command = getattr(args, "org_command", None)

        if command == "list":
            return await OrganizationCommands._handle_list(args, config)
        elif command == "show":
            return await OrganizationCommands._handle_show(args, config)
        elif command == "current":
            return await OrganizationCommands._handle_current(args, config)
        elif command == "env-setup":
            return await OrganizationCommands._handle_env_setup(args, config)
        elif command == "identities":
            return await OrganizationCommands._handle_identities(args, config)
        elif command == "members":
            return await OrganizationCommands._handle_members(args, config)
        else:
            console.print(format_error("No organization command specified"))
            console.print(
                format_info(
                    "Available: list, show, current, members, env-setup — "
                    "use 'innoday orgs --help' for details"
                )
            )
            return 1

    @staticmethod
    async def _handle_list(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle orgs list command."""
        try:
            api_client = InnoDayAPIClient(config)
            formatter = OutputFormatter(
                format_type=args.format, color_enabled=not args.no_color
            )

            # Fetch organizations
            response = await api_client.get("/organizations")

            if response.status_code != 200:
                console.print(
                    format_error(
                        f"Failed to fetch organizations: HTTP {response.status_code}"
                    )
                )
                return 1

            organizations = response.json()

            if not organizations:
                console.print(format_warning("No organizations found"))
                return 0

            # Get current organization for highlighting
            current_org_alias = config.get_current_organization()

            # Add current indicator
            for org in organizations:
                org["is_current"] = org.get("alias") == current_org_alias

            # Format and display
            formatter.format_organizations(
                organizations, show_members=args.show_members
            )

            await api_client.close()
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1

    @staticmethod
    async def _handle_show(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle orgs show command."""
        try:
            # Determine which organization to show (by alias)
            org_alias = args.org_slug or config.get_current_organization()

            if not org_alias:
                console.print(format_error("No organization selected"))
                console.print(
                    format_info(
                        "Run this from a directory with .innoday/project.yml, "
                        "or pass --organization <alias> explicitly (or an org "
                        "alias positional here)"
                    )
                )
                return 1

            # Get organization ID from alias
            org_id = config.get_organization_id(org_alias)
            if not org_id:
                # Try to fetch from API by alias
                api_client = InnoDayAPIClient(config)
                response = await api_client.get("/organizations")

                if response.status_code != 200:
                    console.print(
                        format_error(
                            f"Failed to fetch organizations: HTTP {response.status_code}"
                        )
                    )
                    return 1

                orgs = response.json()
                org_match = next((o for o in orgs if o.get("alias") == org_alias), None)

                if not org_match:
                    console.print(format_error(f"Organization '{org_alias}' not found"))
                    return 1

                org_id = org_match["id"]
                await api_client.close()

            # Fetch organization details
            api_client = InnoDayAPIClient(config)
            endpoint = f"/organizations/{org_id}"
            if args.stats:
                endpoint += "?include_stats=true"

            response = await api_client.get(endpoint)

            if response.status_code == 404:
                console.print(format_error(f"Organization '{org_alias}' not found"))
                return 1
            elif response.status_code != 200:
                console.print(
                    format_error(
                        f"Failed to fetch organization: HTTP {response.status_code}"
                    )
                )
                return 1

            org_data = response.json()

            # Format and display
            formatter = OutputFormatter(
                format_type=args.format, color_enabled=not args.no_color
            )
            formatter.format_organization_details(org_data, include_stats=args.stats)

            await api_client.close()
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1

    @staticmethod
    async def _handle_identities(args: argparse.Namespace, config: CLIConfig) -> int:
        """List handle mappings, or map/unmap one.

        `--user` takes an **email** for the same reason `members --add` does: it is
        what a board reports and what a person knows, and the uuid it resolves to
        is an implementation detail.

        The listing shows *where* each mapping is stored, because there are two
        places and the difference is load-bearing: a GitHub login lives on
        `users.github_username`, a board handle in `user_identity`. Resolution
        consults both (#569) — before it did, mapping a commit handle silenced the
        Team page's unmapped list without making the author resolvable anywhere.

        `--unmapped` inverts the listing, and is where onboarding starts: without
        it the only way to find out *which* handles need mapping was to open the
        Team page in a browser, which is the dependency this command exists to
        remove. It reads the same server-side capability that page's panel does,
        so a script and the page cannot disagree about who still needs mapping.
        """
        org_alias = config.get_current_organization()
        if not org_alias:
            console.print(format_error("No organization selected"))
            console.print(
                format_info(
                    "Run this from a directory with .innoday/project.yml, or "
                    "pass --organization <alias>"
                )
            )
            return 1
        org_id = config.get_organization_id(org_alias)
        if not org_id:
            console.print(
                format_error(f"Organization '{org_alias}' is not in your local config")
            )
            return 1

        to_map = getattr(args, "identity_map", None)
        to_unmap = getattr(args, "identity_unmap", None)
        platform = getattr(args, "identity_platform", None)
        who = getattr(args, "identity_user", None)
        want_unmapped = bool(getattr(args, "identity_unmapped", False))

        if to_map and to_unmap:
            console.print(format_error("Pass --map or --unmap, not both."))
            return 1
        if want_unmapped and (to_map or to_unmap):
            console.print(
                format_error("--unmapped lists; it cannot be combined with a write.")
            )
            return 1
        if want_unmapped and platform:
            # Caught here rather than by the 422, so the explanation arrives
            # without a round trip. Same reason either way: an unmapped board
            # handle carries no platform, so the filter could only be honoured
            # by guessing one.
            console.print(
                format_error(
                    "--platform cannot be combined with --unmapped: an unmapped "
                    "board handle has no platform recorded."
                )
            )
            return 1
        if (to_map or to_unmap) and not platform:
            console.print(
                format_error("--platform is required with --map and --unmap.")
            )
            return 1
        if to_map and not who:
            console.print(format_error("--map needs --user <email>."))
            return 1

        async with InnoDayAPIClient(config) as client:
            try:
                if to_map:
                    payload = {
                        "user": who,
                        "platform": platform,
                        "handle": to_map,
                    }
                    project = getattr(args, "identity_project", None)
                    if project:
                        payload["project_id"] = project
                    response = await client.post(
                        f"/organizations/{org_id}/identities", json=payload
                    )
                    if response.status_code == 409:
                        # Named without naming the current owner -- echoing that
                        # would turn this into a way to enumerate the board's
                        # people by guessing display names.
                        console.print(format_error(response.json().get("detail", "")))
                        return 1
                    if response.status_code not in (200, 201):
                        console.print(
                            format_error(
                                f"Could not map {to_map!r}: HTTP "
                                f"{response.status_code} — {response.text[:200]}"
                            )
                        )
                        return 1
                    body = response.json()
                    console.print(
                        format_success(
                            f"{to_map} is now {body.get('user_email')} "
                            f"({platform}, stored as {body.get('stored_as')})."
                        )
                    )
                    # Board tickets keep a *persisted* `assigned_to`, unlike a
                    # GitHub login, which every summary re-resolves live. So say
                    # what happened to the ones already synced, rather than
                    # leaving the caller to assume a mapping fixed history it
                    # did not touch.
                    moved = body.get("tickets_reattributed") or 0
                    if moved:
                        console.print(
                            format_info(
                                f"{moved} already-synced ticket(s) now show as theirs."
                            )
                        )
                    elif body.get("stored_as") == "user_identity":
                        console.print(
                            format_info(
                                "No already-synced ticket carries that handle; "
                                "the next board sync will use the mapping."
                            )
                        )
                    return 0

                if to_unmap:
                    response = await client.delete(
                        f"/organizations/{org_id}/identities"
                        f"?platform={platform}&handle={quote(to_unmap)}"
                    )
                    if response.status_code not in (200, 204):
                        console.print(
                            format_error(
                                f"Could not unmap {to_unmap!r}: HTTP "
                                f"{response.status_code} — {response.text[:200]}"
                            )
                        )
                        return 1
                    console.print(
                        format_success(f"{to_unmap} is no longer mapped ({platform}).")
                    )
                    if platform == IdentityPlatform.GITHUB.value:
                        # There is one GitHub login per person, on
                        # `users.github_username`, and it is not only a mapping:
                        # the profile page shows it and their open-pull-request
                        # panel is keyed on it. Unmapping empties both, which is
                        # not obvious from the word "unmap".
                        console.print(
                            format_warning(
                                "That was their only GitHub login, so their "
                                "profile and open-PR list are now empty too — "
                                "re-map it, or they can set it on their profile "
                                "page."
                            )
                        )
                    return 0

                if want_unmapped:
                    query = "?unmapped=true"
                elif platform:
                    query = f"?platform={platform}"
                else:
                    query = ""
                response = await client.get(
                    f"/organizations/{org_id}/identities{query}"
                )
                if response.status_code != 200:
                    console.print(
                        format_error(
                            f"Could not list mappings: HTTP "
                            f"{response.status_code} — {response.text[:200]}"
                        )
                    )
                    return 1
                rows = response.json() or []

                if want_unmapped:
                    if not rows:
                        console.print("[green]Nothing is unmapped.[/green]")
                        return 0
                    table = Table(show_header=True, header_style="bold magenta")
                    table.add_column("Kind", style="cyan")
                    table.add_column("Handle", style="white")
                    table.add_column("Behind it", style="dim")
                    for row in rows:
                        table.add_row(
                            str(row.get("kind") or ""),
                            str(row.get("handle") or ""),
                            str(row.get("detail") or ""),
                        )
                    console.print(table)
                    # The most common cause is not a missing handle. Resolution
                    # refuses a non-member on every path, so an unmapped name is
                    # often somebody who was never added to the org -- and no
                    # amount of mapping fixes that.
                    console.print(
                        format_info(
                            "Map one with --map <handle> --user <email> "
                            "--platform <platform>. If the person should "
                            "already resolve, check `innoday orgs members` "
                            "first — resolution refuses a non-member."
                        )
                    )
                    return 0

                if not rows:
                    console.print("[yellow]No handle mappings.[/yellow]")
                    console.print(
                        format_info(
                            "An unmapped board assignee is often a missing "
                            "membership rather than a missing handle — check "
                            "`innoday orgs members` first."
                        )
                    )
                    return 0
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Platform", style="cyan")
                table.add_column("Handle", style="white")
                table.add_column("Person", style="white")
                table.add_column("Scope", style="dim")
                table.add_column("Stored as", style="dim")
                for row in rows:
                    table.add_row(
                        str(row.get("platform") or ""),
                        str(row.get("handle") or ""),
                        str(row.get("user_email") or ""),
                        "project" if row.get("project_id") else "global",
                        str(row.get("stored_as") or ""),
                    )
                console.print(table)
                return 0
            except Exception as exc:  # noqa: BLE001
                console.print(
                    format_error(f"Unexpected error -- {describe_error(exc)}")
                )
                return 1

    @staticmethod
    async def _handle_members(args: argparse.Namespace, config: CLIConfig) -> int:
        """List an org's members, or add one by email.

        **Why the CLI needs this at all.** `POST /organizations/{id}/members`
        has existed and been ADMIN-gated for a long time, with no CLI or MCP
        caller — so the only ways to add a member were the invite email flow
        (which needs the recipient to click a link) or a hand-written API call,
        which this repo forbids. That gap is not cosmetic: board-assignee
        resolution refuses to match a user who is not an active member of the
        org, on *both* the email and handle paths, so "6 assignees unmapped" on
        a project usually means six missing memberships and no amount of handle
        mapping fixes it.

        `--add` takes an **email**, because that is what a board reports and what
        a person knows; the user id it resolves to is an implementation detail.
        """
        org_alias = config.get_current_organization()
        if not org_alias:
            console.print(format_error("No organization selected"))
            console.print(
                format_info(
                    "Run this from a directory with .innoday/project.yml, or "
                    "pass --organization <alias>"
                )
            )
            return 1
        org_id = config.get_organization_id(org_alias)
        if not org_id:
            console.print(
                format_error(f"Organization '{org_alias}' is not in your local config")
            )
            return 1

        target = getattr(args, "member_add", None)
        set_role_target = getattr(args, "member_set_role", None)

        if target and set_role_target:
            console.print(format_error("Pass --add or --set-role, not both."))
            return 1

        if set_role_target:
            return await OrganizationCommands._set_member_role(
                config, org_id, org_alias, set_role_target, args.member_role
            )

        async with InnoDayAPIClient(config) as client:
            try:
                if not target:
                    response = await client.get(f"/organizations/{org_id}/members")
                    if response.status_code != 200:
                        console.print(
                            format_error(
                                f"Could not list members: HTTP "
                                f"{response.status_code} — {response.text[:200]}"
                            )
                        )
                        return 1
                    members = response.json() or []
                    if not members:
                        console.print("[yellow]No members.[/yellow]")
                        return 0
                    table = Table(show_header=True, header_style="bold magenta")
                    table.add_column("Email", style="cyan")
                    table.add_column("Name", style="white")
                    table.add_column("Role", style="white")
                    table.add_column("Active", style="dim")
                    for m in members:
                        user = m.get("user") or {}
                        table.add_row(
                            str(user.get("email") or ""),
                            str(user.get("full_name") or ""),
                            str(m.get("role") or ""),
                            "yes" if m.get("is_active") else "no",
                        )
                    console.print(table)
                    return 0

                user_id = target
                if "@" in target:
                    user_id = await OrganizationCommands._user_id_for_email(
                        client, target
                    )
                    if not user_id:
                        console.print(
                            format_error(f"No InnoDay user has the email {target}")
                        )
                        console.print(
                            format_info(
                                "Seed one first — see 'Seeding platform users' in "
                                "CLAUDE.md (scripts/bootstrap_cli.py seed-user)."
                            )
                        )
                        return 1

                response = await client.post(
                    f"/organizations/{org_id}/members",
                    json={"user_id": user_id, "role": args.member_role},
                )
            except APIError as exc:
                console.print(format_error(f"Failed to reach InnoDay: {exc}"))
                return 1

        if response.status_code in (200, 201):
            console.print(
                format_success(f"{target} is now a {args.member_role} of {org_alias}.")
            )
            return 0
        if response.status_code == 409:
            # Already a member is the desired end state, so this is not a
            # failure -- it is idempotency, and reporting it as an error makes
            # the command unusable in a loop over a list of people.
            console.print(format_info(f"{target} is already a member of {org_alias}."))
            return 0
        detail = response.text[:200]
        try:
            detail = str((response.json() or {}).get("detail") or detail)
        except ValueError:
            pass
        console.print(
            format_error(
                f"Could not add {target} (HTTP {response.status_code}): {detail}"
            )
        )
        return 1

    @staticmethod
    async def _set_member_role(
        config: CLIConfig, org_id: str, org_alias: str, target: str, role: str
    ) -> int:
        """Change an existing member's role.

        `--add` cannot do this: the route 409s on an active member, and the CLI
        (correctly) treats that as idempotent success, so re-adding someone with
        a different role silently changes nothing. `PUT .../members/{user_id}`
        has existed and been ADMIN-gated for a long time with no CLI caller,
        which is why a role could be set once at add-time and never afterwards.

        That gap has teeth. MEMBER is the add default, and releases, board sync
        and ticket writes all require DEVELOPER or higher — so the common outcome
        is a colleague who can read everything, and whose first `innoday release`
        tags every repo and then fails to record the release.
        """
        async with InnoDayAPIClient(config) as client:
            try:
                user_id = target
                if "@" in target:
                    user_id = await OrganizationCommands._user_id_for_email(
                        client, target
                    )
                    if not user_id:
                        console.print(
                            format_error(f"No InnoDay user has the email {target}")
                        )
                        return 1

                response = await client.put(
                    f"/organizations/{org_id}/members/{user_id}",
                    json={"role": role},
                )
            except APIError as exc:
                console.print(format_error(f"Failed to reach InnoDay: {exc}"))
                return 1

        if response.status_code == 200:
            console.print(format_success(f"{target} is now a {role} of {org_alias}."))
            return 0
        if response.status_code == 404:
            console.print(format_error(f"{target} is not a member of {org_alias}."))
            console.print(
                format_info(f"Add them first: innoday orgs members --add {target}")
            )
            return 1
        detail = response.text[:200]
        try:
            detail = str((response.json() or {}).get("detail") or detail)
        except ValueError:
            pass
        console.print(
            format_error(
                f"Could not change {target}'s role (HTTP {response.status_code}): "
                f"{detail}"
            )
        )
        return 1

    @staticmethod
    async def _user_id_for_email(client: InnoDayAPIClient, email: str):
        """An email -> user id, paging `GET /users` until it is found.

        There is no lookup-by-email route, so this pages rather than guessing a
        query parameter that does not exist. Bounded: a platform with more users
        than this needs the route, not a bigger loop here.
        """
        offset = 0
        for _ in range(20):
            response = await client.get(
                "/users", params={"limit": 100, "offset": offset}
            )
            if response.status_code != 200:
                return None
            users = response.json() or []
            if not isinstance(users, list) or not users:
                return None
            for user in users:
                if (
                    isinstance(user, dict)
                    and str(user.get("email") or "").lower() == email.lower()
                ):
                    return user.get("id")
            if len(users) < 100:
                return None
            offset += 100
        return None

    @staticmethod
    async def _handle_current(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle orgs current command."""
        try:
            formatter = OutputFormatter(
                format_type=args.format, color_enabled=not args.no_color
            )

            current_org_alias = config.get_current_organization()

            if not current_org_alias:
                if formatter.format_type == "json":
                    formatter._print_json({})
                    return 0
                console.print(format_warning("No organization currently selected"))
                console.print(
                    format_info(
                        "Run this from a directory with .innoday/project.yml, "
                        "or pass --organization <alias> explicitly"
                    )
                )
                return 0

            # Get organization details from config
            org_details = config.get_organization_details(current_org_alias)
            org_name = (
                org_details.get("name", current_org_alias)
                if org_details
                else current_org_alias
            )
            org_id = org_details.get("id", "Unknown") if org_details else "Unknown"

            if formatter.format_type == "json":
                formatter._print_json(
                    {
                        "name": org_name,
                        "alias": current_org_alias,
                        "id": org_id,
                    }
                )
                return 0

            if org_details:
                console.print(format_success("Current Organization:"))
                console.print(f"  Name: {org_name}")
                console.print(f"  Alias: {current_org_alias}")
                console.print(f"  ID: {org_id}")
            else:
                # Fallback if not in config
                console.print(
                    format_success(f"Current Organization: {current_org_alias}")
                )

            return 0

        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1

    @staticmethod
    async def _handle_env_setup(args: argparse.Namespace, config: CLIConfig) -> int:
        """Interactive wizard to create env/orgs/<alias> and register org/project/board via API."""
        try:
            user_id = config.get_user_id()
            if not user_id:
                console.print(
                    # `innoday platform setup` has never existed -- `platform`
                    # takes {init,health,start,stop,restart,logs,status}. `init`
                    # is the wizard that creates the identity this is missing.
                    format_error("Not logged in. Run 'innoday init' first.")
                )
                return 1

            console.print(format_info("Organization setup wizard"))
            console.print("")

            # --- Collect inputs ---
            alias = args.alias or Prompt.ask("  Org alias (e.g. acme)")
            alias = alias.strip().lower()

            org_name = Prompt.ask("  Org name (e.g. Acme Corp)")
            project_name = Prompt.ask("  Project name")

            console.print("")
            console.print("  Board type options: jira, linear, trello, notion, github")
            board_type_input = Prompt.ask("  Board type", default="skip")
            board_type_input = board_type_input.strip().lower()
            skip_board = board_type_input == "skip"

            board_url = ""
            board_token = ""
            board_email = ""
            board_name = ""

            if not skip_board:
                board_url = Prompt.ask("  Board URL")
                board_name = Prompt.ask("  Board display name", default=project_name)
                board_token = Prompt.ask("  Board API token", password=True)
                if board_type_input == "jira":
                    board_email = Prompt.ask("  Board API email (Jira only)")

            # --- Confirmation ---
            console.print("")
            console.print(format_info("Summary:"))
            console.print(f"  Alias:        {alias}")
            console.print(f"  Org name:     {org_name}")
            console.print(f"  Project:      {project_name}")
            if not skip_board:
                console.print(f"  Board type:   {board_type_input}")
                console.print(f"  Board URL:    {board_url}")
            console.print("")

            if not Confirm.ask("  Create organization and write env file?"):
                console.print(format_warning("Cancelled."))
                return 0

            # --- Check if env file already exists ---
            env_dir = Path("env") / "orgs"
            env_file = env_dir / alias
            if env_file.exists() and not getattr(args, "update", False):
                console.print(
                    format_warning(
                        f"File {env_file} already exists. Use --update to overwrite."
                    )
                )
                return 1

            api_client = InnoDayAPIClient(config)

            # --- Create organization ---
            console.print(format_info("Creating organization..."))
            org_response = await api_client.post(
                "/organizations",
                json={"name": org_name, "alias": alias},
            )

            if org_response.status_code not in (200, 201):
                console.print(
                    format_error(
                        f"Failed to create organization: HTTP {org_response.status_code} — {org_response.text}"
                    )
                )
                await api_client.close()
                return 1

            org_data = org_response.json()
            org_id = org_data["id"]
            console.print(format_success(f"  Organization created: {org_id}"))

            # --- Create project ---
            console.print(format_info("Creating project..."))
            project_response = await api_client.post(
                f"/organizations/{org_id}/projects",
                json={"name": project_name, "description": project_name},
            )

            if project_response.status_code not in (200, 201):
                console.print(
                    format_error(
                        f"Failed to create project: HTTP {project_response.status_code} — {project_response.text}"
                    )
                )
                await api_client.close()
                return 1

            project_data = project_response.json()
            project_id = project_data["id"]
            console.print(format_success(f"  Project created: {project_id}"))

            # --- Connect board (optional) ---
            board_id = None
            if not skip_board:
                console.print(format_info("Connecting board..."))
                integration_token = (
                    f"{board_email}:{board_token}"
                    if board_type_input == "jira" and board_email
                    else board_token
                )
                board_response = await api_client.post(
                    f"/organizations/{org_id}/boards",
                    json={
                        "board_url": board_url,
                        "board_name": board_name,
                        "board_type": board_type_input,
                    },
                    headers={"X-Integration-Token": integration_token},
                )

                if board_response.status_code not in (200, 201):
                    console.print(
                        format_warning(
                            f"Board connect failed: HTTP {board_response.status_code} — {board_response.text}"
                        )
                    )
                    console.print(format_info("  Continuing without board connection."))
                else:
                    board_data = board_response.json()
                    board_id = board_data.get("id")
                    console.print(format_success(f"  Board connected: {board_id}"))

            # --- Write env file ---
            env_dir.mkdir(parents=True, exist_ok=True)
            lines = [
                f"ORG_ALIAS={alias}",
                f"ORG_NAME={org_name}",
                "GITHUB_ORG=",
                f"GITHUB_TOPIC={alias}",
            ]
            if not skip_board:
                lines += [
                    f"BOARD_TYPE={board_type_input}",
                    f"BOARD_URL={board_url}",
                    f"BOARD_API_TOKEN={board_token}",
                ]
                if board_type_input == "jira":
                    lines.append(f"BOARD_API_EMAIL={board_email}")
            else:
                lines += [
                    "BOARD_TYPE=",
                    "BOARD_URL=",
                    "BOARD_API_TOKEN=",
                    "BOARD_API_EMAIL=",
                ]

            env_file.write_text("\n".join(lines) + "\n")
            console.print(format_success(f"  Wrote {env_file}"))

            # --- Update CLI config ---
            # Record the org's alias -> {id, name} lookup entry. We do NOT set
            # a "current organization" here: which org is current is resolved
            # per-invocation from cwd's .innoday/project.yml, never persisted to
            # the shared config file.
            if alias not in config._config.get("organizations", {}):
                config._config.setdefault("organizations", {})[alias] = {
                    "name": org_name,
                    "id": org_id,
                }
            config.save()

            # --- Done ---
            console.print("")
            console.print(format_success("Setup complete!"))
            console.print(f"  Org ID:     {org_id}")
            console.print(f"  Project ID: {project_id}")
            if board_id:
                console.print(f"  Board ID:   {board_id}")
            console.print(f"  Env file:   {env_file}")
            console.print(
                "  Org context is resolved from .innoday/project.yml when you "
                "run commands from a project directory."
            )

            await api_client.close()
            return 0

        except APIError as e:
            console.print(format_error(f"API error: {str(e)}"))
            return 1
        except Exception as e:
            console.print(format_error(f"Unexpected error -- {describe_error(e)}"))
            return 1
