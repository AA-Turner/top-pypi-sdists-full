import json

import click
from click.core import Context as ClickContext
from loguru import logger

from gable.cli.helpers.auth import (
    format_npmrc_credentials,
    set_pip_config_credentials,
    write_npm_credentials,
)
from gable.cli.options import global_options


@click.group()
def auth():
    """View configured Gable authentication information"""


@auth.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
)
@global_options()
@click.pass_context
def key(ctx: ClickContext):
    """Print the API Key gable is currently configured to use"""
    api_key = ctx.obj.client.api_key
    if api_key:
        logger.info(f"API Key in use: {api_key}")
        logger.info("To see your account's API Keys, visit your /settings page.")
    else:
        logger.info("No API Key configured.")
        logger.info("To see your account's API Keys, visit your /settings page.")
        logger.info(
            "Then you can use that key by setting the GABLE_API_KEY env var or using the --api-key flag."
        )


@auth.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["npmrc", "json"]),
    default="npmrc",
    help="Format of the output. Options are: npmrc (default), which you can echo directly into your .npmrc file, or json",
)
@click.option(
    "-w",
    "--write",
    is_flag=True,
    default=False,
    help="If specified, adds entry to an existing .npmrc file, default is ~/.npmrc. If the file already contains a Gable NPM entry, it will be updated. If not, a new entry will be added.",
)
@click.option(
    "-f",
    "--file",
    type=str,
    default="~/.npmrc",
    help="The .npmrc file to write to if --write flag is set. Default is ~/.npmrc. The file must exist, or an error will be thrown.",
)
@global_options()
@click.pass_context
def npm(ctx: ClickContext, output: str, write: bool, file: str):
    """Retrieve temporary credentials for Gable's NPM repository"""
    npm_credentials = ctx.obj.client.get_auth_npm()
    if write:
        write_npm_credentials(npm_credentials, file)
        logger.info(f"Credentials written to {file}")
    elif output == "json":
        logger.info(json.dumps(npm_credentials.dict(), indent=4))
    else:
        logger.info(format_npmrc_credentials(npm_credentials))


@auth.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["conf", "json"]),
    default="conf",
    help="Format of the output. Options are: conf (default), which you can echo directly into your pip.conf file, or json",
)
@click.option(
    "-w",
    "--write",
    is_flag=True,
    default=True,
    help="If specified, writes credentials to ~/.gable/.env file. Default is True.",
)
@click.option(
    "-f",
    "--file",
    type=str,
    default="~/.gable/.env",
    help="The file to write credentials to if --write flag is set. Default is ~/.gable/.env.",
)
@global_options()
@click.pass_context
def pip(ctx: ClickContext, output: str, write: bool, file: str):
    """Retrieve temporary credentials for Gable's Python package repository"""
    pip_credentials = ctx.obj.client.get_auth_pip()
    if write:
        set_pip_config_credentials(pip_credentials, file)
    else:
        # Only set environment variables but don't write to file
        set_pip_config_credentials(pip_credentials)

    if output == "json":
        logger.info(json.dumps(pip_credentials.dict(), indent=4))
    else:
        logger.info(
            f"PIP configuration with index URL: {pip_credentials.repositoryEndpoint}"
        )
        logger.info("Environment variables set for the current session.")
