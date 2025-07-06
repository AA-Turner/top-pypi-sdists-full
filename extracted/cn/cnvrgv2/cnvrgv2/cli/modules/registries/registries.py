import click

from prettytable import PrettyTable

from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.errors import CnvrgError
from cnvrgv2.modules.registries import RegistryTypes


@click.group(name='registry')
def registry_group():
    """
    Manage images in cnvrg
    """
    pass


@registry_group.command()
@click.option('-t', '--title', prompt=messages.REGISTRY_PROMPT_TITLE, help=messages.REGISTRY_HELP_TITLE)
@click.option('-u', '--url', prompt=messages.REGISTRY_PROMPT_URL, help=messages.REGISTRY_HELP_URL)
@click.option('-rt', '--type', default=RegistryTypes.OTHER, help=messages.REGISTRY_HELP_TYPE)
@click.option('-us', '--username', default=None, help=messages.REGISTRY_HELP_USERNAME)
@click.option('-ps', '--password', default=None, help=messages.REGISTRY_HELP_PASSWORD)
@prepare_command()
def create(cnvrg, logger, title, url, type, username, password):
    """
    Creates a new registry
    """

    registry = cnvrg.registries.create(
        url=url,
        type=type,
        title=title,
        username=username,
        password=password
    )

    logger.log_and_echo(messages.REGISTRY_CREATE_SUCCESS.format(registry.title))


@registry_group.command()
@prepare_command()
def list(cnvrg):
    """
    Lists cnvrg registries
    """

    table = PrettyTable()
    table.field_names = ["Slug", "Title", "URL", "Private", "Username", "Type"]
    for field in table.field_names:
        table.align[field] = "l"

    for reg in cnvrg.registries.list():
        table.add_row([reg.slug, reg.title, reg.url, reg.private, reg.username, reg.registry_type])

    click.echo(table)


@registry_group.command()
@click.option('-s', '--slug', help=messages.REGISTRY_HELP_SLUG)
@prepare_command()
def get(cnvrg, logger, slug):
    """
    Retrieves a registry data
    """

    try:
        reg = cnvrg.registries.get(slug=slug)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return

    table = PrettyTable()
    table.field_names = ["Slug", "Title", "URL", "Private", "Username", "Type"]
    for field in table.field_names:
        table.align[field] = "l"

    table.add_row([reg.slug, reg.title, reg.url, reg.private, reg.username, reg.registry_type])
    click.echo(table)


@registry_group.command()
@click.option('-s', '--slug', prompt=messages.IMAGE_PROMPT_SLUG, help=messages.IMAGE_HELP_SLUG)
@click.option('-t', '--title', default=None, help=messages.REGISTRY_HELP_TITLE)
@click.option('-u', '--url', default=None, help=messages.REGISTRY_HELP_URL)
@click.option('-us', '--username', default=None, help=messages.REGISTRY_HELP_USERNAME)
@click.option('-ps', '--password', default=None, help=messages.REGISTRY_HELP_PASSWORD)
@prepare_command()
def update(cnvrg, slug, title, url, username, password):
    """
    Updates a registry
    """

    cnvrg.registries.get(slug=slug).update(title=title, url=url, username=username, password=password)


@registry_group.command()
@click.option('-s', '--slug', help=messages.REGISTRY_HELP_SLUG)
@prepare_command()
def delete(cnvrg, logger, slug):
    """
    Deletes a registry
    """

    try:
        reg = cnvrg.registries.get(slug=slug)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return

    reg.delete()
