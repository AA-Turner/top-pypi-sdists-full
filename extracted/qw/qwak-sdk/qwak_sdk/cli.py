from typing import Optional

import click
from packaging import version
from qwak.inner.di_configuration import UserAccountConfiguration
from qwak.inner.di_configuration.account import UserAccount
from qwak.inner.tool.auth import FrogMLAuthClient

from qwak_sdk import __version__ as sdk_version
from qwak_sdk.commands.admin.admin_commands_group import admin_commands_group
from qwak_sdk.commands.alerts.alerts_commnad_group import alerts_commands_group
from qwak_sdk.commands.audience.audience_commands_group import audience_commands_group
from qwak_sdk.commands.automations.automations_commands_group import (
    automations_commands_group,
)
from qwak_sdk.commands.feature_store.feature_store_command_group import (
    feature_store_commands_group,
)
from qwak_sdk.commands.models.models_command_group import models_command_group
from qwak_sdk.commands.projects.projects_command_group import projects_command_group
from qwak_sdk.commands.secrets.secrets_commands_group import secrets_commands_group
from qwak_sdk.commands.workspaces.workspaces_commands_group import (
    workspaces_commands_group,
)
from qwak_sdk.inner.tools.cli_tools import profile_setter_wrapper
from qwak_sdk.inner.tools.logger import setup_qwak_logger

version_option_kwargs = {}
if version.parse(click.__version__) >= version.parse("8.0.0"):
    version_option_kwargs["package_name"] = "qwak-sdk"
    version_option_kwargs["version"] = sdk_version


def create_qwak_cli():
    setup_qwak_logger()

    @click.group()
    @click.version_option(**version_option_kwargs)
    def qwak_cli():
        # This class is intentionally empty
        pass

    @qwak_cli.command("configure", short_help="Configure the Qwak environment")
    @click.option(
        "--api-key",
        metavar="QWAK_API_KEY",
        required=False,
        help="Qwak assigned API key",
    )
    @click.option(
        "--url", metavar="BASE_URL", required=False, help="Artifactory base url"
    )
    @click.option(
        "--username", metavar="USERNAME", required=False, help="The user's username"
    )
    @click.option(
        "--password", metavar="PASSWORD", required=False, help="The user's password"
    )
    @click.option(
        "--token",
        metavar="TOKEN",
        required=False,
        help="Access token to authenticate",
    )
    @click.option(
        "--interactive",
        metavar="INTERACTIVE",
        required=False,
        help="Login with interactive flow",
        default=False,
    )
    @click.option(
        "--environment",
        metavar="ENVIRONMENT",
        default="default",
        required=False,
        is_eager=True,
        help="Qwak environment's name",
    )
    @click.option(
        "--type",
        metavar="TYPE",
        default="qwak",
        required=False,
        type=click.Choice(["qwak", "jfrog"], case_sensitive=False),
        is_eager=True,
        help="Login type (qwak/jfrog)",
    )
    @profile_setter_wrapper
    def set_configuration(
        api_key: Optional[str],
        url: Optional[str],
        username: Optional[str],
        password: Optional[str],
        token: Optional[str],
        interactive: bool,
        environment: str,
        type: str,
        **_,
    ):
        if type.lower() == "jfrog":
            account_config = UserAccountConfiguration(auth_client=FrogMLAuthClient)
            account_config.configure_user(
                UserAccount(
                    url=url,
                    username=username,
                    password=password,
                    api_key=token,
                    anonymous=False,
                    is_interactive=interactive,
                )
            )
        elif type.lower() == "qwak":
            if api_key is None:
                api_key = click.prompt("Please enter your API key", type=str)

            account_config = UserAccountConfiguration()
            account_config.configure_user(UserAccount(api_key=api_key))
            print(f"User successfully configured for the '{environment}' environment")

    qwak_cli.add_command(projects_command_group)
    qwak_cli.add_command(models_command_group)
    qwak_cli.add_command(secrets_commands_group)
    qwak_cli.add_command(automations_commands_group)
    qwak_cli.add_command(admin_commands_group)
    qwak_cli.add_command(feature_store_commands_group)
    qwak_cli.add_command(audience_commands_group)
    qwak_cli.add_command(alerts_commands_group)
    qwak_cli.add_command(workspaces_commands_group)
    return qwak_cli
