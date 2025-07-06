import click

import os.path
from cnvrgv2.cnvrg import UsersClient
from cnvrgv2.cli.utils import messages
from cnvrgv2.config import Config

from cnvrgv2.errors import CnvrgFileError, CnvrgHttpError
from cnvrgv2.cli.utils.decorators import prepare_command_without_context
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.config import error_messages


@click.command()
@click.option('-d', '--domain', default=None, help=messages.LOGIN_PROMPT_DOMAIN)
@click.option('-e', '--email', default=None, help=messages.LOGIN_PROMPT_EMAIL)
@click.option('-p', '--password', default=None, help=messages.LOGIN_PROMPT_PASSWORD, hide_input=True)
@click.option('-o', '--organization', default=None, help=messages.LOGIN_ORGANIZATION_HELP)
@click.option('-t', '--auth-token', default=None, help=messages.LOGIN_HELP_AUTH_TOKEN)
@prepare_command_without_context()
def login(logger, domain, email, password, organization, auth_token):
    config = Config()
    config_domain = None
    if password is None:
        password = ""

    if domain is None:
        config_domain = config.domain
        domain = config_domain or click.prompt(messages.LOGIN_PROMPT_DOMAIN, type=str)

    # The guideline in this block is to receive both email and pass together from the user or config file.
    if email is None:
        config_email = config.user
        config_token = config.token

        if config_email and config_token and config_domain:
            click.echo(messages.LOGIN_ALREADY_LOGGED_IN)
            return
        else:
            email = click.prompt(messages.LOGIN_PROMPT_EMAIL, type=str)
            if not auth_token:
                password = click.prompt(messages.LOGIN_PROMPT_PASSWORD, type=str, hide_input=True)
    else:
        if not auth_token:
            password = password or click.prompt(messages.LOGIN_PROMPT_PASSWORD, type=str, hide_input=True)

    try:
        uc = UsersClient(domain=domain, token=auth_token)
        config.sso_version = uc.sso_version

        token, default_organization, sso_enabled, _ = uc.login(user=email, password=password, token=auth_token)

        config.domain = domain
        config.organization = organization or default_organization
        config.user = email
        if auth_token is not None and sso_enabled:
            config.token = auth_token
        else:
            config.token = token
        config.check_certificate = False
        config.save()

        logger.log_and_echo(messages.LOGIN_SUCCESS.format(email))

    except CnvrgHttpError:
        logger.log_and_echo(messages.LOGIN_INVALID_CREDENTIALS, error=True)


@click.command()
@prepare_command_without_context()
def logout(logger):
    try:
        config = Config()
        config.remove_config_fields("user", "token")
        logger.log_and_echo(messages.LOGOUT_SUCCESS)

    except CnvrgFileError:
        logger.log_and_echo(messages.LOGOUT_CONFIG_MISSING, error=True)


@click.command()
@prepare_command()
def me(logger):
    """
    Prints the current logged in user details
    """
    try:
        config = Config()
        log_dir = os.path.join(config.global_cnvrg_path, "logs")
        log_path = log_dir + "/cnvrg.log"
        click.echo(messages.ME_SUCCESS_API.format(config.domain))
        click.echo(messages.ME_SUCCESS.format(config.user))
        click.echo(messages.ME_SUCCESS_LOGS.format(log_path))
        logger.info(messages.ME_LOGGER_SUCCESS)

    except CnvrgFileError:
        logger.log_and_echo(error_messages.CREDENTIALS_MISSING, error=True)
