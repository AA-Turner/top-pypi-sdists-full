import click

from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command_without_context
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.config import Config
from cnvrgv2.cnvrg import Cnvrg


@click.command()
@click.option(
    '-nc',
    '--no-check-certificate',
    'check',
    flag_value=0,
    help=messages.CONFIG_HELP_CHECK_CERTIFICATE.format("Disable")
)
@click.option(
    '-c',
    '--check-certificate',
    'check',
    flag_value=1,
    help=messages.CONFIG_HELP_CHECK_CERTIFICATE.format("Enable")
)
@click.option('-o', '--organization', help=messages.CONFIG_HELP_ORGANIZTION)
@prepare_command_without_context()
def config(logger, check, organization):
    """
    Change configuration values
    """
    if all(arg is None for arg in [check, organization]):
        click.echo(message=config.get_help(click.get_current_context()))
        logger.info(msg=messages.CONFIG_NO_ARGS_LOG)
        return
    config_file = Config()
    old_organization = config_file.organization
    try:
        if check is not None:
            config_file.check_certificate = bool(check)
        if organization:
            config_file.organization = organization
            config_file.save()
            Cnvrg()  # We want to test the connection with the new organization

        logger.log_and_echo(message=messages.CONFIG_UPDATE_SUCCESS)
    except CnvrgArgumentsError as error:
        config_file.organization = old_organization
        config_file.save()
        logger.log_and_echo(message=str(error), error=True)
