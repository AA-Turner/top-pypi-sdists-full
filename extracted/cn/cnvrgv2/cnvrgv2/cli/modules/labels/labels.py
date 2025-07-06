import click

from prettytable import PrettyTable

from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.errors import CnvrgError
from cnvrgv2.cli.utils.helpers import print_generator_in_chunks


@click.group(name='labels')
def labels_group():
    """
    Manage labels in cnvrg
    """
    pass


@labels_group.command()
@click.option('-k', '--kind', help=messages.LABEL_HELP_KIND)
@click.option('-n', '--name', help=messages.LABEL_HELP_NAME)
@click.option('-c', '--color_name', help=messages.LABEL_HELP_COLOR_NAME)
@prepare_command()
def create(cnvrg, logger, kind, name, color_name):
    try:
        label = cnvrg.labels.create(name, kind, color_name)
        logger.log_and_echo(messages.LABEL_CREATE_SUCCESS.format(label.name))
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)


@labels_group.command()
@click.option('-k', '--kind', prompt=messages.LABEL_PROMPT_KIND, help=messages.LABEL_HELP_KIND)
@click.option('-cs', '--chunk-size', default=20, help=messages.DATASET_LIST_FILES_HELP_CHUNK_SIZE)
@click.option('-l', '--limit', type=int, help=messages.DATASET_LIST_FILES_HELP_LIMIT)
@prepare_command()
def list(cnvrg, kind, chunk_size, limit):
    """
    Lists Labels
    """
    labels = cnvrg.labels.list(kind)
    attributes_field_name = ["Name", "Color Name"]
    attributes = ["name", "color_name"]
    print_generator_in_chunks(labels, chunk_size, limit, attributes, attributes_field_name, line_numbers=True)


@labels_group.command()
@click.option('-k', '--kind', help=messages.LABEL_HELP_KIND)
@click.option('-n', '--name', help=messages.LABEL_HELP_NAME)
@prepare_command()
def get(cnvrg, logger, kind, name):
    """
    Retrieves an Label information
    """
    try:
        label = cnvrg.labels.get(name=name, kind=kind)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return

    table = PrettyTable()
    table.field_names = ["Name", "Color Name"]
    table.add_row([label.name, label.color_name])
    click.echo(table)


@labels_group.command()
@click.option('-k', '--kind', help=messages.LABEL_HELP_KIND)
@click.option('-n', '--name', help=messages.LABEL_HELP_NAME)
@prepare_command()
def delete(cnvrg, logger, name, kind):
    """
    Delete an label
    """
    try:
        label = cnvrg.labels.get(name=name, kind=kind)
        label.delete()
        msg = messages.LABEL_DELETE_SUCCESS.format(name)
        logger.log_and_echo(msg)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return
