import sys

import click
import questionary
from pycarlo.core import Session

import montecarlodata.settings as settings
from montecarlodata.agent_traces.commands import agent_traces
from montecarlodata.agents.commands import agents
from montecarlodata.collector.commands import collectors
from montecarlodata.common.user import UserService
from montecarlodata.config import ConfigManager
from montecarlodata.data_exports.commands import export
from montecarlodata.dataimport.commands import import_subcommand
from montecarlodata.discovery.commands import discovery
from montecarlodata.iac.commands import monitors
from montecarlodata.insights.commands import insights
from montecarlodata.integrations.commands import integrations
from montecarlodata.keys.commands import keys
from montecarlodata.management.commands import management
from montecarlodata.mcp.commands import mcp
from montecarlodata.platform.commands import platform
from montecarlodata.secrets.commands import secrets
from montecarlodata.tools import dump_help

# CLI authentication types (for `configure`).
AUTH_TYPE_API_KEY = "api-key"
AUTH_TYPE_OAUTH = "oauth"


def _stdin_is_tty() -> bool:
    """Whether stdin is an interactive terminal. The questionary picker can only render on a
    real TTY; scripted runs (CI, scheduled jobs piping prompt answers) must not reach it."""
    return sys.stdin is not None and sys.stdin.isatty()


def _validate_instance_id(value: str) -> str:
    """Validate an instance id via the SDK (the single source of truth), re-raising as a UsageError
    so the flag/prompt re-asks on invalid input.

    Used both for the --mcd-instance-id flag and as a click prompt value_proc.
    """
    try:
        return Session.validate_instance_id(value)
    except ValueError as e:
        raise click.UsageError(str(e)) from e


@click.group(help="Monte Carlo's CLI.")
@click.option(
    "--profile",
    default=settings.DEFAULT_PROFILE_NAME,
    help="Specify an MCD profile name. Uses default otherwise.",
)
@click.option(
    "--config-path",
    default=settings.DEFAULT_CONFIG_PATH,
    type=click.Path(dir_okay=True),
    help=(
        "Specify path where to look for config file. Uses "
        f"{settings.DEFAULT_CONFIG_PATH} otherwise."
    ),
)
@click.version_option()
@click.pass_context
def entry_point(ctx, profile, config_path):
    """
    Entry point for all subcommands and options. Reads configuration and sets as context,
    except when configuring or getting help.
    """
    if (
        ctx.invoked_subcommand != settings.CONFIG_SUB_COMMAND
        and settings.HELP_FLAG not in sys.argv[1:]
    ):
        config = ConfigManager(profile_name=profile, base_path=config_path).read()
        if not config:
            ctx.abort()
        ctx.obj = {"config": config}


@click.command(
    help=(
        "Configure the CLI. Without a terminal (e.g. CI or scripted runs), API key auth is used "
        "unless --oauth or --api-key is passed."
    )
)
@click.option(
    "--profile-name",
    required=False,
    help="Specify a profile name for configuration.",
    default=settings.DEFAULT_PROFILE_NAME,
)
@click.option(
    "--config-path",
    required=False,
    help="Specify path where to look for config file.",
    default=settings.DEFAULT_CONFIG_PATH,
    type=click.Path(dir_okay=True),
)
@click.option(
    "--oauth",
    is_flag=True,
    default=False,
    help=(
        "Configure using OAuth client credentials. "
        "Required in non-interactive environments, which default to API key auth."
    ),
)
@click.option(
    "--api-key",
    "api_key",
    is_flag=True,
    default=False,
    help="Configure using an API key.",
)
@click.option("--mcd-id", default=None, help="Monte Carlo token user ID (API key auth).")
@click.option("--mcd-token", default=None, help="Monte Carlo token value (API key auth).")
@click.option(
    "--mcd-oauth-client-id", default=None, help="Monte Carlo OAuth client ID (OAuth auth)."
)
@click.option(
    "--mcd-oauth-client-secret",
    default=None,
    help="Monte Carlo OAuth client secret (OAuth auth).",
)
@click.option(
    "--mcd-instance-id",
    default=None,
    help="Monte Carlo deployment instance ID, e.g. us1, eu1 (OAuth auth).",
)
def configure(
    profile_name,
    config_path,
    oauth,
    api_key,
    mcd_id,
    mcd_token,
    mcd_oauth_client_id,
    mcd_oauth_client_secret,
    mcd_instance_id,
):
    """
    Special subcommand for configuring the CLI
    """
    if oauth and api_key:
        raise click.UsageError("Specify only one of --oauth or --api-key.")

    # --oauth / --api-key select the auth type non-interactively; otherwise ask (arrow-key picker).
    # Without a TTY the picker cannot render, so scripted runs fall back to api-key auth — the
    # pre-picker behavior, where prompt answers can be piped via stdin.
    if oauth:
        auth_type = AUTH_TYPE_OAUTH
    elif api_key:
        auth_type = AUTH_TYPE_API_KEY
    elif not _stdin_is_tty():
        click.echo(
            "No terminal detected — defaulting to API key auth. Pass --oauth to use OAuth.",
            err=True,
        )
        auth_type = AUTH_TYPE_API_KEY
    else:
        auth_type = questionary.select(
            "Authentication type",
            choices=[AUTH_TYPE_API_KEY, AUTH_TYPE_OAUTH],
            default=AUTH_TYPE_API_KEY,
        ).ask()
        if auth_type is None:  # user cancelled (e.g. Ctrl-C)
            raise click.Abort()

    config_manager = ConfigManager(profile_name=profile_name, base_path=config_path)
    if auth_type == AUTH_TYPE_OAUTH:
        # Reconfiguring is authoritative: drop any prior API-key credentials so a switched-over
        # profile doesn't keep stale (and live) secrets on disk.
        config_manager.remove_options(ConfigManager.API_KEY_OPTIONS)
        config_manager.write(
            mcd_oauth_client_id=mcd_oauth_client_id or click.prompt("Client ID"),
            mcd_oauth_client_secret=(
                mcd_oauth_client_secret or click.prompt("Client Secret", hide_input=True)
            ),
            mcd_instance_id=(
                _validate_instance_id(mcd_instance_id)
                if mcd_instance_id
                else click.prompt(
                    "Instance ID (e.g. us1, eu1; see Account Information -> Instance ID)",
                    value_proc=_validate_instance_id,
                )
            ),
        )
    else:
        # Drop any prior OAuth credentials so the switched-over profile is authoritative and OAuth
        # (which wins in Config.read) doesn't keep overriding the new API key.
        config_manager.remove_options(ConfigManager.OAUTH_OPTIONS)
        config_manager.write(
            mcd_id=mcd_id or click.prompt("Key ID"),
            mcd_token=mcd_token or click.prompt("Secret", hide_input=True),
        )


@click.command(help="Validate that the CLI can Connect to Monte Carlo.")
@click.pass_obj
def validate(ctx):
    """
    Special subcommand for validating the CLI was correctly configured
    """
    first_name = UserService(
        config=ctx["config"],
        command_name="validate",
    ).user.first_name
    click.echo(f"Hi, {first_name}! All is well.")


@entry_point.command(help="Echo all help text.", name="help")
def echo_help():
    """
    Special subcommand to echo all help text.
    """
    dump_help(entry_point)


entry_point.add_command(integrations)
entry_point.add_command(configure)
entry_point.add_command(validate)
entry_point.add_command(collectors)
entry_point.add_command(discovery)
entry_point.add_command(monitors)
entry_point.add_command(import_subcommand)
entry_point.add_command(insights)
entry_point.add_command(management)
entry_point.add_command(agents)
entry_point.add_command(agent_traces)
entry_point.add_command(keys)
entry_point.add_command(secrets)
entry_point.add_command(platform)
entry_point.add_command(export)
entry_point.add_command(mcp)

# to allow this to be run as a script within an IDE (for debugging)
if __name__ == "__main__":
    entry_point()
