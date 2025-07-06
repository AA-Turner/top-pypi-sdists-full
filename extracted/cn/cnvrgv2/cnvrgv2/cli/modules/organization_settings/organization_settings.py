import re
import click
from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from functools import wraps


def shared_options(**kwargs):
    def inner_decorator(func):
        @click.option('-mdw', '--max-duration-workspaces', type=int, default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_MAX_DURATION_WORKSPACES, **kwargs)
        @click.option('-mde', '--max-duration-experiments', type=int, default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_MAX_DURATION_EXPERIMENTS, **kwargs)
        @click.option('-mde', '--max-duration-endpoints', type=int, default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_MAX_DURATION_ENDPOINTS, **kwargs)
        @click.option('-mdw', '--max-duration-webapps', type=int, default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_MAX_DURATION_WEBAPPS, **kwargs)
        @click.option('-accc', '--automatically-clear-cached-commits', type=int, default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_AUTOMATICALLY_CLEAR_CACHED_COMMITS, **kwargs)
        @click.option('-swu', '--slack-webhook-url', type=str, default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_SLACK_WEBHOOK_URL, **kwargs)
        @click.option('-qcwt', '--queued-compute-wait-time', type=int, default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_QUEUED_COMPUTE_WAIT_TIME, **kwargs)
        @click.option('-cpu', '--custom-pypi-url', type=str, default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_CUSTOM_PYPI_URL, **kwargs)
        @click.option('-dt', '--debug-time', type=int, default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_DEBUG_TIME, **kwargs)
        @click.option('-it', '--idle-time', type=int, default=None, help=messages.ORGANIZATION_SETTINGS_HELP_IDLE_TIME,
                      **kwargs)
        @click.option('-ie', '--idle-enabled', default=None, help=messages.ORGANIZATION_SETTINGS_HELP_IDLE_ENABLED,
                      is_flag=True)
        @click.option('-dte', '--debug-time-enabled', default=None, help=messages.ORGANIZATION_SETTINGS_HELP_DEBUG_TIME,
                      is_flag=True)
        @click.option('-eoe', '--email-on-error', default=None, help=messages.ORGANIZATION_SETTINGS_HELP_EMAIL_ON_ERROR,
                      is_flag=True)
        @click.option('-eos', '--email-on-success', default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_EMAIL_ON_SUCCESS, is_flag=True)
        @click.option('-cpe', '--custom-pypi-enabled', default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_CUSTOM_PYPI_ENABLED, is_flag=True)
        @click.option('-id', '--install-dependencies', default=None,
                      help=messages.ORGANIZATION_SETTINGS_HELP_INSTALL_DEPENDENCIES, is_flag=True)
        @wraps(func)
        def wrapper(*args, **_kwargs):
            return func(*args, **_kwargs)

        return wrapper

    return inner_decorator


@click.group(name="settings")
def organization_settings_group():
    pass


@organization_settings_group.command()
@prepare_command()
def show(cnvrg, logger):
    click.echo("Current settings for organization:")
    cnvrg.settings.reload()
    for prop, value in cnvrg.settings.values().items():
        click.echo(prop + ": " + str(value))


@organization_settings_group.command(name="set")
@shared_options()
@click.option('-dc', '--default-computes', type=str, default=None,
              help=messages.ORGANIZATION_SETTINGS_HELP_DEFAULT_COMPUTES)
@prepare_command()
def set_settings(cnvrg, logger, default_computes, **kwargs):
    if default_computes is not None:
        cnvrg.settings.update(default_computes=re.split(r'\s*,\s*', default_computes))
        return

    cnvrg.settings.update(**{k: v for k, v in kwargs.items() if v is not None})


@organization_settings_group.command(name="unset")
@shared_options(is_flag=True)
@prepare_command()
def unset_settings(
        cnvrg,
        logger,
        **kwargs
):
    cnvrg.settings.update(**{k: None for k, v in kwargs.items() if v is not None})
