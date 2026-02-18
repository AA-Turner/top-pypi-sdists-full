import json
import sys

import click

from exponent.commands.common import (
    redirect_to_login,
    refresh_api_key_task,
    run_until_complete,
    set_login_complete,
)
from exponent.commands.settings import use_settings
from exponent.commands.types import exponent_cli_group
from exponent.core.config import Settings
from exponent.core.graphql.client import GraphQLClient
from exponent.utils.version import (
    get_installed_metadata,
    get_installed_version,
    get_installer,
    get_python_path,
    get_sys_executable,
)

CURRENT_USER_QUERY = """
    query CurrentUser {
        currentUser {
            userUuid
        }
    }
"""


@exponent_cli_group()
def config_cli() -> None:
    """Manage Indent configuration settings."""
    pass  # pragma: no cover


@config_cli.command(hidden=True)
@use_settings
def debug(
    settings: Settings,
) -> None:
    click.echo("Settings:")
    click.echo(settings)
    click.echo("\nInstalled Version:")
    click.echo(get_installed_version())
    click.echo("\nPython Version:")
    click.echo(sys.version)
    click.echo("\nPython Path:")
    click.echo(get_python_path())
    click.echo("\nSys Executable Path:")
    click.echo(get_sys_executable())
    click.echo("\nInstaller:")
    click.echo(get_installer())
    click.echo("\nInstalled Metadata:")
    click.echo(get_installed_metadata())


@config_cli.command(hidden=True)
@click.option(
    "--set-git-warning-disabled",
    is_flag=True,
    help="Disable the git warning for running Indent from a non-git repository",
)
@click.option(
    "--set-git-warning-enabled",
    is_flag=True,
    help="Enable the git warning for running Indent from a non-git repository",
)
@click.option(
    "--set-auto-upgrade-enabled",
    is_flag=True,
    help="Enable automatic upgrades",
)
@click.option(
    "--set-auto-upgrade-disabled",
    is_flag=True,
    help="Disable automatic upgrades",
)
@click.option(
    "--set-base-api-url-override",
    required=False,
    hidden=True,
    help="Override base API URL",
)
@click.option(
    "--clear-base-api-url-override",
    is_flag=True,
    hidden=True,
    help="Clear base API URL override",
)
@click.option(
    "--set-base-ws-url-override",
    required=False,
    hidden=True,
    help="Override base WS URL",
)
@click.option(
    "--clear-base-ws-url-override",
    is_flag=True,
    hidden=True,
    help="Clear base WS URL override",
)
@click.option(
    "--set-use-default-colors",
    is_flag=True,
    help="Use default colors",
)
@click.option(
    "--clear-use-default-colors",
    is_flag=True,
    help="Clear use default colors",
)
@use_settings
def config(  # noqa: PLR0913
    settings: Settings,
    set_git_warning_disabled: bool,
    set_git_warning_enabled: bool,
    set_auto_upgrade_enabled: bool,
    set_auto_upgrade_disabled: bool,
    clear_base_api_url_override: bool,
    clear_base_ws_url_override: bool,
    set_use_default_colors: bool,
    clear_use_default_colors: bool,
    set_base_api_url_override: str | None = None,
    set_base_ws_url_override: str | None = None,
) -> None:
    """Display current Indent configuration."""

    num_options_set = sum(
        [
            set_git_warning_disabled,
            set_git_warning_enabled,
            set_auto_upgrade_enabled,
            set_auto_upgrade_disabled,
            clear_base_ws_url_override,
            clear_base_api_url_override,
            set_base_api_url_override is not None,
            set_base_ws_url_override is not None,
            set_use_default_colors,
            clear_use_default_colors,
        ]
    )
    if num_options_set == 0:
        click.secho(
            json.dumps(settings.get_config_file_settings(), indent=2),
            fg="green",
        )
        return

    if num_options_set > 1:
        click.secho("Cannot set multiple options at the same time.", fg="red")
        return

    if set_git_warning_enabled:
        settings.options.git_warning_disabled = False
        settings.write_settings_to_config_file()

        click.secho(
            "Git warning enabled. Indent will now check for a git repository.\n",
            fg="yellow",
        )

    if set_git_warning_disabled:
        settings.options.git_warning_disabled = True
        settings.write_settings_to_config_file()

        click.secho(
            "Git warning disabled. Indent will no longer check for a git repository.\n",
            fg="yellow",
        )

    if set_auto_upgrade_enabled:
        settings.options.auto_upgrade = True
        settings.write_settings_to_config_file()

        click.secho(
            "Automatic upgrades enabled. Indent will now check for updates.\n",
            fg="yellow",
        )

    if set_auto_upgrade_disabled:
        settings.options.auto_upgrade = False
        settings.write_settings_to_config_file()

        click.secho(
            "Automatic upgrades disabled. Indent will no longer check for updates.\n",
            fg="yellow",
        )

    if clear_base_api_url_override:
        settings.options.base_api_url_override = None
        settings.write_settings_to_config_file()

        click.secho(
            "API URL override cleared.",
            fg="yellow",
        )

    if clear_base_ws_url_override:
        settings.options.base_ws_url_override = None
        settings.write_settings_to_config_file()

        click.secho(
            "WS URL override cleared.",
            fg="yellow",
        )

    if set_base_api_url_override:
        settings.options.base_api_url_override = set_base_api_url_override
        settings.write_settings_to_config_file()

        click.secho(
            "API URL override set.",
            fg="yellow",
        )

    if set_base_ws_url_override:
        settings.options.base_ws_url_override = set_base_ws_url_override
        settings.write_settings_to_config_file()

        click.secho(
            "WS URL override set.",
            fg="yellow",
        )

    if set_use_default_colors:
        settings.options.use_default_colors = True
        settings.write_settings_to_config_file()

        click.secho(
            "Use default colors set.",
            fg="yellow",
        )

    if clear_use_default_colors:
        settings.options.use_default_colors = False
        settings.write_settings_to_config_file()


@config_cli.command()
@click.option("--key", help="Your Indent API Key")
@use_settings
def login(settings: Settings, key: str) -> None:
    """Log in to Indent."""

    if not key:
        redirect_to_login(settings, "provided")
        return

    click.echo("Verifying API key...")
    run_until_complete(set_login_complete(key, settings.get_base_api_url(), settings.get_base_ws_url()))
    click.secho("Success!", fg="green")

    click.echo(f"Saving API Key to {settings.config_file_path}")

    if settings.api_key and settings.api_key != key:
        click.confirm("Detected existing API Key, continue? ", default=True, abort=True)

    settings.update_api_key(key)
    settings.write_settings_to_config_file()

    click.echo("API Key saved.")


@config_cli.command(hidden=True)
@use_settings
def get_chats(
    settings: Settings,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        get_chats_task(
            api_key=settings.api_key,
            base_api_url=settings.get_base_api_url(),
            base_ws_url=settings.get_base_ws_url(),
        )
    )


@config_cli.command(hidden=True)
@use_settings
def get_authenticated_user(
    settings: Settings,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        get_authenticated_user_task(
            api_key=settings.api_key,
            base_api_url=settings.get_base_api_url(),
            base_ws_url=settings.get_base_ws_url(),
        )
    )


async def get_chats_task(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    result = await graphql_client.get_chats()

    click.echo(f"Found {len(result.organization_chats_page.chats)} chats:")
    for chat in result.organization_chats_page.chats:
        click.echo(f"  - {chat.name or 'Untitled'} ({chat.chat_uuid})")


async def get_authenticated_user_task(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    result = await graphql_client.execute(CURRENT_USER_QUERY)
    click.echo(result)


@config_cli.command(hidden=True)
@use_settings
def refresh_key(settings: Settings) -> None:
    """Refresh your API key."""
    if not settings.api_key:
        redirect_to_login(settings)
        return

    click.echo("Refreshing API key...")
    run_until_complete(
        refresh_api_key_task(
            api_key=settings.api_key,
            base_api_url=settings.get_base_api_url(),
            base_ws_url=settings.get_base_ws_url(),
        )
    )
