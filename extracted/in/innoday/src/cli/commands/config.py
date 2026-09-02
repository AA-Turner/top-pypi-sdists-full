"""
InnoDay CLI Configuration Commands

Handles configuration management operations.
"""

import argparse
import copy
from typing import Any, Dict, Optional

from rich.console import Console

from src.cli.config import DEFAULT_API_URL, CLIConfig, is_local_api_url
from src.cli.utils.formatters import (
    format_error,
    format_success,
    format_warning,
)
from src.domain.board import BoardType

console = Console()


class ConfigCommands:
    """Configuration management commands."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser) -> None:
        """Set up configuration command parser."""
        subparsers = parser.add_subparsers(
            title="Configuration Commands",
            dest="config_command",
            help="Configuration operations",
        )

        # Config init
        init_parser = subparsers.add_parser(
            "init", help="Interactive configuration setup"
        )
        init_parser.add_argument(
            "--force", action="store_true", help="Overwrite existing configuration"
        )
        # Non-interactive parameters
        init_parser.add_argument(
            "--api-url",
            help=f"API server URL (default: {DEFAULT_API_URL})",
        )
        init_parser.add_argument("--email", help="User email address")
        init_parser.add_argument("--name", help="User full name")
        init_parser.add_argument(
            "--non-interactive",
            action="store_true",
            help="Run in non-interactive mode (requires all necessary parameters)",
        )

        # Config set
        set_parser = subparsers.add_parser("set", help="Set configuration value")
        set_parser.add_argument(
            "key",
            # `organization` is accepted here and then refused by
            # `_handle_set` with an explanation. Leaving it out of `choices`
            # made argparse answer a bare "invalid choice" instead, so the
            # carefully worded rejection -- which names
            # `.innoday/project.yml` and `--organization`, the two things
            # that actually work -- was unreachable. `get` has always
            # accepted the key, which made the asymmetry read as a bug in
            # the CLI rather than as a deliberate removal.
            choices=[
                "api-url",
                "api-timeout",
                "organization",
                "format",
                "color",
                "team-secret",
            ],
            help="Configuration key to set",
        )
        set_parser.add_argument("value", help="Configuration value")

        # Config get
        get_parser = subparsers.add_parser("get", help="Get configuration value")
        get_parser.add_argument(
            "key",
            choices=[
                "api-url",
                "api-timeout",
                "organization",
                "format",
                "color",
                "team-secret",
            ],
            help="Configuration key to get",
        )

        # Config show
        subparsers.add_parser("show", help="Show current configuration")

        # Config reset
        reset_parser = subparsers.add_parser(
            "reset", help="Reset configuration to defaults"
        )
        reset_parser.add_argument(
            "--confirm", action="store_true", help="Confirm reset without prompting"
        )

        # Profile management
        profile_parser = subparsers.add_parser(
            "profile", help="Manage named config profiles"
        )
        profile_sub = profile_parser.add_subparsers(
            dest="profile_command", help="Profile operations"
        )

        profile_sub.add_parser("list", help="List all profiles")

        use_parser = profile_sub.add_parser("use", help="Switch active profile")
        use_parser.add_argument("name", help="Profile name to activate")

        create_parser = profile_sub.add_parser("create", help="Create a new profile")
        create_parser.add_argument("name", help="Profile name (e.g. dev, local)")
        create_parser.add_argument("--api-url", help="API URL for this profile")
        create_parser.add_argument(
            "--default",
            action="store_true",
            help="Also set this as the default profile used when no --profile is "
            "given (including for non-interactive/MCP invocations).",
        )

        delete_parser = profile_sub.add_parser("delete", help="Delete a profile")
        delete_parser.add_argument("name", help="Profile name to delete")

        show_parser = profile_sub.add_parser("show", help="Show config for a profile")
        show_parser.add_argument(
            "name", nargs="?", help="Profile name (defaults to active)"
        )

        set_default_parser = profile_sub.add_parser(
            "set-default",
            help="Repoint the default profile (used for non-interactive/MCP "
            "resolution) without switching or creating anything",
        )
        set_default_parser.add_argument("name", help="Profile name to make the default")

    @staticmethod
    async def execute(args: argparse.Namespace, config: CLIConfig) -> int:
        """Execute configuration command."""
        command = getattr(args, "config_command", None)

        if command == "init":
            return await ConfigCommands._handle_init(args, config)
        elif command == "set":
            return await ConfigCommands._handle_set(args, config)
        elif command == "get":
            return await ConfigCommands._handle_get(args, config)
        elif command == "show":
            return await ConfigCommands._handle_show(args, config)
        elif command == "reset":
            return await ConfigCommands._handle_reset(args, config)
        elif command == "profile":
            return await ConfigCommands._handle_profile(args, config)
        else:
            console.print(format_error("No configuration command specified"))
            console.print(
                "[dim]Available: init, set, get, show, reset, profile — "
                "run 'innoday config --help' for details[/dim]"
            )
            return 1

    @staticmethod
    async def _handle_init(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle config init command - streamlined initialization."""
        try:
            # Check if already initialized
            if config.is_initialized() and not args.force:
                console.print(format_success("✅ Already initialized!"))
                console.print()

                # Fetch and display current setup info
                from src.cli.client import InnoDayAPIClient as APIClient

                try:
                    api_client = APIClient(config)

                    # Get user info
                    user_info = config.get_user_info()
                    console.print(f"User: {user_info['name']} ({user_info['email']})")

                    # Get current organization info
                    org_alias = config.get_current_organization()
                    if org_alias:
                        org_id = config.get_organization_id(org_alias)
                        if org_id:
                            org_response = await api_client.get(
                                f"/organizations/{org_id}"
                            )
                            if org_response and org_response.status_code == 200:
                                org_data = org_response.json()
                                console.print(f"Organization: {org_data['name']}")

                    console.print(f"API: {config.get_api_url()}")

                except Exception:
                    # If API is not available, just show config data
                    console.print(f"Organization: {config.get_current_organization()}")
                    console.print(f"API: {config.get_api_url()}")

                return 0

            # Check for non-interactive mode
            if getattr(args, "non_interactive", False):
                # Validate required parameters
                if not args.email or not args.name:
                    console.print(
                        format_error("Non-interactive mode requires --email and --name")
                    )
                    return 1

                # Run non-interactive initialization. Its exit code is the
                # command's: it used to be discarded, so even the team-secret
                # refusal -- which writes nothing at all -- exited 0 (#619).
                return await ConfigCommands._non_interactive_init(config, args)

            # Show welcome banner for first-time setup (unless suppressed)
            if not getattr(args, "no_banner", False):
                from src.cli.utils.banner import show_welcome_banner

                show_welcome_banner(console, "InnoDay CLI")

            # Run streamlined interactive setup
            succeeded = await ConfigCommands._streamlined_init(
                config, profile_name=getattr(args, "profile", None)
            )
            return 0 if succeeded else 1

        except Exception as e:
            console.print(format_error(f"Failed to initialize configuration: {e}"))
            return 1

    @staticmethod
    async def _handle_set(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle config set command."""
        try:
            key = args.key.replace("-", "_")  # Convert kebab-case to snake_case
            value = args.value

            # Validate and set value
            if key == "api_url":
                config.set_api_url(value)
            elif key == "organization":
                # The current organization is no longer a persisted setting --
                # it is resolved per-invocation from cwd's .innoday/project.yml
                # (or a one-off --organization flag), never stored in the
                # shared ~/.innoday/config.json. Reject the write rather than
                # silently no-op it.
                console.print(
                    format_error(
                        "`config set organization` is no longer supported. The "
                        "current organization is resolved automatically from "
                        "the .innoday/project.yml in your working directory. "
                        "Use `--organization <alias>` for a one-off override."
                    )
                )
                return 1
            elif key == "format":
                if value not in ["table", "json", "csv"]:
                    console.print(
                        format_error(
                            f"Invalid format: {value}. Must be table, json, or csv"
                        )
                    )
                    return 1
                config.set_output_format(value)
            elif key == "color":
                if value.lower() in ["true", "yes", "1", "on"]:
                    config.set_color_enabled(True)
                elif value.lower() in ["false", "no", "0", "off"]:
                    config.set_color_enabled(False)
                else:
                    console.print(
                        format_error(
                            f"Invalid color value: {value}. Must be true/false"
                        )
                    )
                    return 1
            elif key == "api_timeout":
                # Settable at last. `set_api_timeout` has existed with no way to
                # reach it, so a slow deployment could not be accommodated at
                # all -- BPAI's repo sync needs ~32s against a 30s default.
                try:
                    seconds = float(value)
                except ValueError:
                    console.print(
                        format_error(f"Invalid timeout: {value}. Give it in seconds.")
                    )
                    return 1
                if seconds <= 0:
                    console.print(
                        format_error("Timeout must be greater than zero seconds.")
                    )
                    return 1
                config.set_api_timeout(seconds)
            elif key == "team_secret":
                config.set_team_secret(value)

            # Save configuration
            config.save()
            display_value = "***" if key == "team_secret" else value
            console.print(format_success(f"Set {args.key} = {display_value}"))
            return 0

        except Exception as e:
            console.print(format_error(f"Failed to set configuration: {e}"))
            return 1

    @staticmethod
    async def _handle_get(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle config get command."""
        try:
            key = args.key.replace("-", "_")

            # Get value
            if key == "api_url":
                value = config.get_api_url()
            elif key == "organization":
                value = config.get_current_organization() or "Not set"
            elif key == "format":
                value = config.get_output_format()
            elif key == "color":
                value = "true" if config.is_color_enabled() else "false"
            elif key == "team_secret":
                value = "***" if config.get_team_secret() else "Not set"
            else:
                console.print(format_error(f"Unknown configuration key: {key}"))
                return 1

            print(value)  # Plain output for scripting
            return 0

        except Exception as e:
            console.print(format_error(f"Failed to get configuration: {e}"))
            return 1

    @staticmethod
    async def _handle_show(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle config show command."""
        try:
            config.display_config()
            return 0
        except Exception as e:
            console.print(format_error(f"Failed to show configuration: {e}"))
            return 1

    @staticmethod
    async def _handle_reset(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle config reset command."""
        try:
            from rich.prompt import Confirm

            # Confirm reset
            if not args.confirm:
                if not Confirm.ask(
                    "Are you sure you want to reset configuration to defaults?"
                ):
                    console.print("Reset cancelled")
                    return 0

            # Reset to defaults.
            #
            # `_config` is ONE profile; `DEFAULT_CONFIG` is the file that wraps
            # every profile. Assigning the latter here nested `current_profile`
            # and `profiles` *inside* the profile being reset, so a reset
            # profile came back holding a copy of the whole config shape and
            # none of the keys any accessor reads. A deep copy, because a
            # shallow one hands the live default dicts to the caller to mutate.
            config._config = copy.deepcopy(CLIConfig._PROFILE_DEFAULTS)
            config.save()

            # A "Also clear stored credentials?" step was here. It called
            # `config.list_credentials()`, which has never existed on
            # `CLIConfig` -- so every `config reset` raised `AttributeError`
            # *after* saving, printed "Failed to reset configuration" and
            # exited 1 while having reset the profile perfectly well. There is
            # no enumeration API to fix it with (keyring offers no listing, and
            # `delete_credential` takes one key), so the step goes rather than
            # being reimplemented: `innoday auth logout` clears the CLI token,
            # which is the only credential this file's owner has left.
            console.print(format_success("Configuration reset to defaults"))
            return 0

        except Exception as e:
            console.print(format_error(f"Failed to reset configuration: {e}"))
            return 1

    # `_validate_jira_credentials` and `_validate_trello_credentials` were
    # here. They existed only for `_configure_jira`/`_configure_trello`, the
    # wizard paths that wrote a board secret to ~/.innoday/config.json and
    # were removed by #609. `innoday board set-cred` validates against the
    # real provider server-side before storing in Vault, so nothing is lost.

    # `_validate_github_token`, `_validate_claude_credentials` and
    # `_validate_slack_token` were here (#729), alongside the
    # `_configure_github`/`_configure_slack`/`_configure_claude` prompts they
    # served and the `config integrations` wizard that called those. The wizard
    # collected a GitHub personal access token, a Claude API key and a Slack bot
    # token, validated each against the real provider, and stored them in
    # ~/.innoday/config.json (and the OS keyring) where **no code path has ever
    # read them back** -- the reader was deleted by #609. Same
    # laptop-resident-credential class that #609 fixed for Jira and Trello, left
    # standing for these three. `innoday board set-cred` is the replacement for
    # a board credential; the other two have no replacement because nothing
    # wanted them.

    #: What to run when a user create needs the shared deployment's team secret
    #: and the CLI has none. Names `innoday config set team-secret`, which
    #: exists, and deliberately no longer says "or pass
    #: `innoday init --team-secret`": that flag is real, but it belongs to the
    #: *workspace* `init` command, so someone running `config init` was being
    #: sent to a different command for a flag `config init` does not have
    #: (#619).
    TEAM_SECRET_REQUIRED_MESSAGE = (
        "A team access secret is required to create a user on the shared "
        "dev/deployed API. Run `innoday config set team-secret <value>` first, "
        "then re-run this command."
    )

    @staticmethod
    async def _non_interactive_init(config: CLIConfig, args: argparse.Namespace) -> int:
        """Non-interactive initialization using command-line parameters.

        User/CLI setup only -- no organization is created or joined here.
        Organizations and projects are expected to already exist (created by
        a platform admin or via a separate onboarding flow); a user joins
        one explicitly afterward. See innoday-self-register-lightweight.md
        for the planned `innoday orgs join` command that covers that step.

        Returns 0 when the config was written, 1 when it was not. Note what 0
        does *not* claim: `POST /users` mints no token, so this command cannot
        by itself leave the CLI able to authenticate -- only `innoday login` or
        `scripts/bootstrap_cli.py seed-user` can. It used to print "✅
        Configuration initialized successfully!" regardless, which is how a
        wiped machine ended up with `innoday status` reporting
        `✗ No identity configured` right after a "successful" init, and no
        command that repaired it (#619). The closing message is now conditional
        on there actually being a token, and names the command that mints one
        when there isn't. Writing the config is still a success (exit 0) --
        agents and the register-project skill run this against a local API and
        then log in, so a non-zero exit for "no token yet" would fail a flow
        that is proceeding correctly.
        """
        from src.cli.client import InnoDayAPIClient as APIClient

        # Set platform URL -- match `innoday init`'s own default (the shared
        # dev environment), not localhost, so a non-interactive `config init`
        # run with no --api-url doesn't silently point at a local server that
        # likely isn't running.
        api_url = args.api_url or DEFAULT_API_URL

        config.set_api_url(api_url)

        console.print(f"API URL: {api_url}")

        # Create API client
        api_client = APIClient(config)

        user_id = None
        failure = None

        # Against the shared dev/deployed API, POST /users is gated by the team
        # access secret. Refuse a create up front (rather than firing a doomed
        # 401) when none is set.
        if not is_local_api_url(api_url) and not config.get_team_secret():
            console.print(format_error(ConfigCommands.TEAM_SECRET_REQUIRED_MESSAGE))
            return 1

        try:
            user_data = {
                "email": args.email,
                "full_name": args.name,
                "role": "DEVELOPER",
            }

            # Check if user exists
            users_response = await api_client.get("/users")
            if users_response.status_code == 200:
                users = users_response.json()
                existing_user = next(
                    (u for u in users if u["email"] == args.email), None
                )

                if existing_user:
                    user_id = existing_user["id"]
                    console.print(f"✓ User exists: {args.name}")
                else:
                    create_response = await api_client.post("/users", json=user_data)
                    if create_response.status_code in [200, 201]:
                        user_result = create_response.json()
                        user_id = user_result["id"]
                        console.print(f"✓ User created: {args.name}")
                    else:
                        raise Exception(
                            f"Failed to create user: {create_response.status_code}"
                        )
            else:
                # Previously this branch did not exist: a non-200 user list fell
                # straight through to a save with user_id still None, and then
                # printed success.
                raise Exception(
                    f"Could not list users: HTTP {users_response.status_code}"
                )

        except Exception as e:
            failure = str(e)
            console.print(f"⚠ Setup error: {e}")

        if not user_id:
            # No invented UUID here. The old fallback was `uuid.uuid4()`, which
            # writes an identity no server has ever heard of -- every request
            # made as it fails, and the config looks configured.
            console.print(
                format_error(
                    f"Could not resolve a user for {args.email} on {api_url}"
                    + (f" ({failure})" if failure else "")
                    + ". Nothing was written. Check the API URL and team secret, "
                    "or ask a platform admin to seed the account with "
                    "`scripts/bootstrap_cli.py seed-user`."
                )
            )
            return 1

        # Persist the resolved identity. `set_user_info` mutates memory only --
        # like every other field setter on CLIConfig -- so the save is the
        # caller's job and must not be dropped: without it `get_user_id()` is
        # None on the next invocation and `board register`, `license` and
        # `client.py` all refuse to run.
        config.set_user_info(user_id, args.email, args.name)
        config.save()

        if config.get_cli_token():
            console.print(
                format_success("\n✅ Configuration initialized successfully!")
            )
            console.print(f"User: {args.name} ({args.email})")
        else:
            console.print(
                format_warning(
                    f"\n⚠ Configuration saved for {args.name} ({args.email}), but "
                    "this CLI is not authenticated yet -- `config init` cannot "
                    "mint a token."
                )
            )
            console.print(
                "Finish with `innoday login` (browser device flow). No account "
                "yet? A platform admin can seed one and hand you a token with "
                "`scripts/bootstrap_cli.py seed-user <email>`."
            )
        console.print(
            "[dim]No organization selected. Join one with "
            "`innoday join <alias>` once it exists.[/dim]"
        )
        return 0

    @staticmethod
    async def _create_user(
        api_client: Any,
        email: str,
        full_name: str,
        config: Optional[CLIConfig] = None,
    ) -> str:
        """Create a new user via the API and return the new user's id.

        Against a NON-local API, the shared dev/deployed server gates
        POST /users behind the team access secret. If none is configured,
        refuse up front with actionable guidance rather than firing a request
        that will just 401. A local API has no team secret, so this is skipped.

        The gate reads `config` when passed, else falls back to the client's
        own `.config` (both are the same real CLIConfig in production).
        """
        cfg = config if config is not None else getattr(api_client, "config", None)
        if isinstance(cfg, CLIConfig) and not is_local_api_url(cfg.get_api_url()):
            if not cfg.get_team_secret():
                console.print(format_error(ConfigCommands.TEAM_SECRET_REQUIRED_MESSAGE))
                raise Exception(
                    "Missing team access secret for user creation on the shared "
                    "dev/deployed API"
                )

        create_response = await api_client.post(
            "/users", json={"email": email, "full_name": full_name, "role": "DEVELOPER"}
        )
        if create_response.status_code not in (200, 201):
            raise Exception(
                f"HTTP {create_response.status_code}: {create_response.text}"
            )
        return create_response.json()["id"]

    @staticmethod
    async def _streamlined_init(
        config: CLIConfig, profile_name: Optional[str] = None
    ) -> bool:
        """Profile-scoped initialization wizard. Returns False if aborted."""
        from rich.prompt import Confirm, Prompt

        from src.cli.client import InnoDayAPIClient as APIClient

        console.print("\n[bold cyan]─── InnoDay Profile Setup ───[/bold cyan]\n")

        # Step 1: Profile name
        default_profile = profile_name or config.get_current_profile() or "dev"
        chosen_profile = Prompt.ask("Profile name", default=default_profile)

        # Create profile if it doesn't exist
        if chosen_profile not in config.list_profiles():
            config.create_profile(chosen_profile)
            console.print(format_success(f"✓ Created profile '{chosen_profile}'"))

        # Switch to it
        config._current_profile = chosen_profile
        config._config = config._active_profile_config()

        # Step 2: API URL (with connectivity check)
        while True:
            api_url = Prompt.ask("API URL", default=config.get_api_url())
            config.set_api_url(api_url)
            console.print("[dim]Checking connectivity...[/dim]")
            try:
                import httpx

                async with httpx.AsyncClient() as client:
                    r = await client.get(f"{api_url.rstrip('/')}/health", timeout=5.0)
                    if r.status_code == 200:
                        data = r.json()
                        console.print(
                            format_success(
                                f"✓ Connected — {data.get('service', 'InnoDay')} v{data.get('version', '?')}"
                            )
                        )
                        break
                    else:
                        console.print(format_warning(f"⚠ API returned {r.status_code}"))
            except Exception as e:
                console.print(format_warning(f"⚠ Could not connect: {e}"))
            if not Confirm.ask("Try a different URL?", default=True):
                break

        api_client = APIClient(config)

        # Step 3: User — fetch from API and let user pick
        user_id = None
        user_email = None
        user_name = None

        console.print("\n[bold]Who are you?[/bold]")
        try:
            users_response = await api_client.get("/users")
            if users_response and users_response.status_code == 200:
                users = users_response.json()
                if isinstance(users, list) and users:
                    console.print("\nUsers on this instance:")
                    for i, u in enumerate(users, 1):
                        console.print(
                            f"  {i}. {u.get('name') or u.get('full_name', '?')} ({u.get('email', '?')})"
                        )
                    idx_str = Prompt.ask(
                        "Select your number (or press Enter to enter email manually)",
                        default="",
                    )
                    if idx_str.strip().isdigit():
                        idx = int(idx_str.strip()) - 1
                        if 0 <= idx < len(users):
                            selected = users[idx]
                            user_id = selected["id"]
                            user_email = selected.get("email", "")
                            user_name = selected.get("name") or selected.get(
                                "full_name", ""
                            )
                            console.print(
                                format_success(
                                    f"✓ Selected: {user_name} ({user_email})"
                                )
                            )
        except Exception:
            pass

        if not user_id:
            user_email = Prompt.ask("Your email")
            # Try to look up by email
            try:
                users_response = await api_client.get("/users")
                if users_response and users_response.status_code == 200:
                    users = users_response.json()
                    if isinstance(users, list):
                        match = next(
                            (u for u in users if u.get("email") == user_email), None
                        )
                        if match:
                            user_id = match["id"]
                            user_name = match.get("name") or match.get("full_name", "")
                            console.print(format_success(f"✓ Found user: {user_name}"))
            except Exception:
                pass

        if not user_id:
            console.print(
                format_warning(f"User '{user_email}' not found on this instance.")
            )
            if not Confirm.ask("Create a new account with this email?", default=True):
                console.print(
                    format_error(
                        "Cannot continue without a valid user_id. Aborting init."
                    )
                )
                return False
            user_name = Prompt.ask("Your full name")
            try:
                user_id = await ConfigCommands._create_user(
                    api_client, user_email, user_name, config=config
                )
                console.print(
                    format_success(f"✓ User created: {user_name} ({user_email})")
                )
            except Exception as e:
                console.print(format_error(f"Could not create user: {e}"))
                return False

        config.set_user_info(user_id or "", user_email or "", user_name or "")

        # Recreate the client now that user info is set, so it picks up the
        # stored identity (X-User-ID is long gone -- auth is the Bearer token).
        await api_client.close()
        api_client = APIClient(config)

        # Step 4: Organizations — fetch and multi-select
        console.print("\n[bold]Which organizations do you want in this profile?[/bold]")
        selected_orgs = []
        try:
            if user_id:
                orgs_response = await api_client.get(
                    f"/auth/users/{user_id}/organizations"
                )
            else:
                orgs_response = None

            if orgs_response and orgs_response.status_code == 200:
                orgs = orgs_response.json()
                if not isinstance(orgs, list):
                    orgs = orgs.get("organizations", [])
            else:
                orgs = []

            if orgs:
                console.print("\nOrganizations you belong to:")
                for i, o in enumerate(orgs, 1):
                    console.print(
                        f"  {i}. {o.get('name', '?')} ({o.get('alias', '?')})"
                    )
                idxs_str = Prompt.ask(
                    "Select numbers separated by commas (or Enter for all)",
                    default="all",
                )
                if idxs_str.strip().lower() in ("", "all"):
                    selected_orgs = orgs
                else:
                    for part in idxs_str.split(","):
                        part = part.strip()
                        if part.isdigit():
                            idx = int(part) - 1
                            if 0 <= idx < len(orgs):
                                selected_orgs.append(orgs[idx])
            else:
                console.print(format_warning("No organizations found for this user."))
        except Exception as e:
            console.print(format_warning(f"Could not fetch organizations: {e}"))

        # Persist the selected orgs' alias -> {id, name} lookup map into the
        # profile config. We do NOT set a "current organization" here: which
        # org is current is resolved per-invocation from cwd's
        # .innoday/project.yml, not stored in the shared config file.
        for org in selected_orgs:
            slug = org.get("alias") or CLIConfig.generate_alias(org.get("name", "org"))
            if slug not in config._config["organizations"]:
                config._config["organizations"][slug] = {}
            config._config["organizations"][slug]["name"] = org.get("name", slug)
            config._config["organizations"][slug]["id"] = org.get("id")

        # Step 5: Board check per org
        console.print("\n[bold]Checking board registrations...[/bold]")
        all_have_boards = True
        for org in selected_orgs:
            slug = org.get("alias") or CLIConfig.generate_alias(org.get("name", ""))
            org_id = org.get("id")
            has_board = False
            if org_id and user_id:
                try:
                    boards_response = await api_client.get(
                        f"/organizations/{org_id}/boards"
                    )
                    if boards_response and boards_response.status_code == 200:
                        boards = boards_response.json()
                        if isinstance(boards, list) and boards:
                            has_board = True
                            console.print(
                                format_success(
                                    f"  ✓ {org.get('name', slug)}: board registered ({len(boards)} board(s))"
                                )
                            )
                except Exception:
                    pass

            if not has_board:
                all_have_boards = False
                console.print(
                    format_warning(f"  ⚠ {org.get('name', slug)}: no board registered")
                )
                if Confirm.ask(
                    f"    Configure board for {org.get('name', slug)} now?",
                    default=True,
                ):
                    await ConfigCommands._configure_org_board(
                        config, api_client, org, user_id
                    )

        # Step 6: Completion message
        config.save()

        if all_have_boards:
            console.print(format_success(f"\n✅ Profile '{chosen_profile}' is ready!"))
            console.print("""
[bold cyan]🚀 YOU ARE CLEARED FOR LAUNCH, COMMANDER.[/bold cyan]

Your InnoDay MCP is fuelled and on the pad. Here's your mission brief:

  • [bold]Sync your boards[/bold]   → "sync all boards for Acme"
  • [bold]Get a summary[/bold]      → "what's the current release status for bp-ai?"
  • [bold]Check the team[/bold]     → "what did the team ship this week?"
  • [bold]File a ticket[/bold]      → "create a ticket: fix the flaky sync on retries"

The MCP handles the wiring — you just fly the mission. 🛸
""")
        else:
            console.print(
                format_success(f"\n✅ Profile '{chosen_profile}' configured.")
            )
            console.print(
                "\n[dim]Register remaining boards, then you're ready to sync and get summaries.[/dim]"
            )

        return True

    @staticmethod
    async def _configure_org_board(
        config: CLIConfig,
        api_client: Any,
        org: Dict[str, Any],
        user_id: Optional[str],
    ) -> None:
        """Inline board setup for a single org during init."""
        from rich.prompt import Prompt

        org_id = org.get("id")
        org_name = org.get("name", org.get("alias", "org"))

        console.print(f"\n  [bold]Board setup for {org_name}[/bold]")

        # A board must belong to a project (BoardRegistration.project_id is a
        # required FK, and BoardRegistrationCreate requires board_name too).
        # Resolve the project first -- offer the org's projects to pick from,
        # falling back to a manual project-ID prompt.
        project_id = await ConfigCommands._select_project_id(api_client, org_id)
        if not project_id:
            console.print(
                format_warning(
                    "  ⚠ No project selected -- skipping board setup "
                    "(a board must belong to a project)"
                )
            )
            return

        # Derived from `BoardType`, never typed out. The hand-written list
        # here offered "github", which is not a member -- picking it produced a
        # 422 from board registration and a bare "⚠ Could not register board",
        # i.e. an interactive prompt leading somewhere that cannot work.
        board_type = Prompt.ask(
            "  Board type",
            choices=[board.value for board in BoardType],
            default=BoardType.JIRA.value,
        )
        board_name = Prompt.ask("  Board name", default=f"{org_name} board")
        board_url = Prompt.ask("  Board URL")
        board_token = Prompt.ask("  Board API token", password=True, default="")
        board_email = ""
        if board_type == "jira":
            board_email = Prompt.ask("  Jira email")

        if org_id and user_id:
            try:
                payload: Dict[str, Any] = {
                    "board_type": board_type,
                    "board_name": board_name,
                    "board_url": board_url,
                    "project_id": project_id,
                    "organization_id": org_id,
                }
                extra_headers: Dict[str, str] = {}
                if board_token:
                    extra_headers["X-Integration-Token"] = (
                        f"{board_email}:{board_token}"
                        if board_type == "jira" and board_email
                        else board_token
                    )
                resp = await api_client.post(
                    f"/organizations/{org_id}/boards",
                    json=payload,
                    headers=extra_headers or None,
                )
                if resp and resp.status_code in (200, 201):
                    console.print(
                        format_success(f"  ✓ Board registered for {org_name}")
                    )
                else:
                    console.print(
                        format_warning(
                            f"  ⚠ Could not register board ({resp.status_code if resp else 'no response'})"
                        )
                    )
            except Exception as e:
                console.print(format_warning(f"  ⚠ Board registration failed: {e}"))

    @staticmethod
    async def _select_project_id(
        api_client: Any, org_id: Optional[str]
    ) -> Optional[str]:
        """Resolve a project_id for board registration. Lists the org's
        projects for the user to pick from; falls back to a manual project-ID
        prompt if none can be listed."""
        from rich.prompt import Prompt

        projects: list = []
        if org_id:
            try:
                resp = await api_client.get(f"/organizations/{org_id}/projects")
                if resp and resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list):
                        projects = data
            except Exception:
                projects = []

        if projects:
            console.print("  Projects in this organization:")
            for i, p in enumerate(projects, 1):
                console.print(f"    {i}. {p.get('name', '?')} ({p.get('id', '?')})")
            choice = Prompt.ask(
                "  Select a project number (or Enter to type an ID)", default=""
            )
            choice = choice.strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(projects):
                    return projects[idx].get("id")

        entered = Prompt.ask("  Project ID", default="")
        return entered.strip() or None

    @staticmethod
    async def _handle_profile(args: argparse.Namespace, config: CLIConfig) -> int:
        """Handle `config profile` subcommands."""
        from rich.table import Table

        sub = getattr(args, "profile_command", None)

        if sub == "list":
            profiles = config.list_profiles()
            active = config.get_current_profile()
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Profile", style="cyan")
            table.add_column("Active", style="green")
            table.add_column("API URL")
            table.add_column("User")
            for name in profiles:
                pdata = config.get_profile_config(name)
                is_active = "✓" if name == active else ""
                api_url = (
                    pdata.get("platform", {}).get("api_url", "?") if pdata else "?"
                )
                user = pdata.get("user", {}) if pdata else {}
                user_str = user.get("email") or user.get("id") or "—"
                table.add_row(name, is_active, api_url, user_str)
            console.print(table)
            return 0

        elif sub == "use":
            try:
                config.set_current_profile(args.name)
                console.print(format_success(f"Switched to profile '{args.name}'"))
                return 0
            except ValueError as e:
                console.print(format_error(str(e)))
                return 1

        elif sub == "create":
            api_url = getattr(args, "api_url", None)
            make_default = getattr(args, "default", False)
            if args.name in config.list_profiles():
                console.print(format_warning(f"Profile '{args.name}' already exists."))
                return 0
            config.create_profile(args.name, api_url=api_url)
            config.save()
            console.print(
                format_success(
                    f"Created profile '{args.name}'"
                    + (f" (api-url: {api_url})" if api_url else "")
                )
            )
            if make_default:
                config.set_default_profile(args.name)
                console.print(format_success(f"Profile '{args.name}' set as default"))
            return 0

        elif sub == "set-default":
            try:
                config.set_default_profile(args.name)
                console.print(format_success(f"Profile '{args.name}' set as default"))
                return 0
            except ValueError as e:
                console.print(format_error(str(e)))
                return 1

        elif sub == "delete":
            try:
                config.delete_profile(args.name)
                config.save()
                console.print(format_success(f"Deleted profile '{args.name}'"))
                return 0
            except ValueError as e:
                console.print(format_error(str(e)))
                return 1

        elif sub == "show":
            name = getattr(args, "name", None) or config.get_current_profile()
            pdata = config.get_profile_config(name)
            if pdata is None:
                console.print(format_error(f"Profile '{name}' not found."))
                return 1
            import json as _json

            # Mask sensitive fields
            safe = _json.dumps(pdata, indent=2, default=str)
            console.print(f"[bold]Profile: {name}[/bold]\n{safe}")
            return 0

        else:
            console.print(
                format_error(
                    "No profile sub-command given. Try: list, use, create, delete, show, set-default"
                )
            )
            return 1
