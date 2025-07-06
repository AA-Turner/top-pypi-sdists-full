import os
import click

from prettytable import PrettyTable

from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.errors import CnvrgError


@click.group(name='image')
def image_group():
    """
    Manage images in cnvrg
    """
    pass


@image_group.command()
@click.option('-n', '--name', prompt=messages.IMAGE_PROMPT_NAME, help=messages.IMAGE_HELP_NAME)
@click.option('-t', '--tag', prompt=messages.IMAGE_PROMPT_TAG, help=messages.IMAGE_HELP_TAG)
@click.option('-r', '--registry', default='local', help=messages.IMAGE_HELP_REGISTRY)
@click.option('-l', '--logo', default='', help=messages.IMAGE_HELP_LOGO)
@click.option('-c', '--custom', is_flag=True, default=False, help=messages.IMAGE_HELP_CUSTOM)
@click.option('-rd', '--readme', default='', help=messages.IMAGE_HELP_README)
@click.option('-df', '--dockerfile', default='', help=messages.IMAGE_HELP_DOCKERFILE)
@prepare_command()
def create(cnvrg, logger, name, tag, registry, logo, custom, readme, dockerfile):
    """
    Creates a new image
    """

    # Init readme content
    if readme:
        if not os.path.exists(readme):
            logger.log_and_echo(messages.IMAGE_INVALID_README, error=True)
            return
        with open(readme) as f:
            readme_content = f.read()
    else:
        readme_content = ""

    # Init dockerfile content
    if custom:
        if not dockerfile or not os.path.exists(dockerfile):
            logger.log_and_echo(messages.IMAGE_INVALID_DOCKERFILE, error=True)
            return
        with open(dockerfile) as f:
            dockerfile_content = f.read()
    else:
        dockerfile_content = ""

    new_image = cnvrg.images.create(
        tag=tag,
        name=name,
        logo=logo,
        custom=custom,
        readme=readme_content,
        registry=registry,
        dockerfile=dockerfile_content
    )

    logger.log_and_echo(messages.IMAGE_CREATE_SUCCESS.format(new_image.name))


@image_group.command()
@prepare_command()
def list(cnvrg):
    """
    Lists cnvrg images
    """

    table = PrettyTable()
    table.field_names = ["Slug", "Name", "Tag", "Status", "Registry URL", "Created by"]
    for field in table.field_names:
        table.align[field] = "l"

    for image in cnvrg.images.list():
        created_by = image.created_by or "cnvrg"
        table.add_row([image.slug, image.name, image.tag, image.status, image.registry_url, created_by])

    click.echo(table)


@image_group.command()
@click.option('-s', '--slug', help=messages.IMAGE_HELP_SLUG)
@click.option('-n', '--name', help=messages.IMAGE_HELP_NAME)
@click.option('-t', '--tag', help=messages.IMAGE_HELP_TAG)
@prepare_command()
def get(cnvrg, logger, slug, name, tag):
    """
    Retrieves an image data
    """

    try:
        image = cnvrg.images.get(slug=slug, name=name, tag=tag)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return

    table = PrettyTable()
    table.field_names = ["Slug", "Name", "Tag", "Status", "Registry URL", "Created by"]
    for field in table.field_names:
        table.align[field] = "l"

    created_by = image.created_by or "cnvrg"
    table.add_row([image.slug, image.name, image.tag, image.status, image.registry_url, created_by])

    click.echo(table)


@image_group.command()
@click.option('-s', '--slug', prompt=messages.IMAGE_PROMPT_SLUG, help=messages.IMAGE_HELP_SLUG)
@click.option('-l', '--logo', default=None, help=messages.IMAGE_HELP_LOGO)
@click.option('-rd', '--readme', default=None, help=messages.IMAGE_HELP_README)
@prepare_command()
def update(cnvrg, logger, slug, logo, readme):
    """
    Updates an image
    """

    # Init readme content
    if readme:
        if not os.path.exists(readme):
            logger.log_and_echo(messages.IMAGE_INVALID_README, error=True)
            return
        with open(readme) as f:
            readme_content = f.read()
    else:
        readme_content = ""

    cnvrg.images.get(slug=slug).update(logo=logo, readme=readme_content)


@image_group.command()
@click.option('-s', '--slug', help=messages.IMAGE_HELP_SLUG)
@click.option('-n', '--name', help=messages.IMAGE_HELP_NAME)
@click.option('-t', '--tag', help=messages.IMAGE_HELP_TAG)
@prepare_command()
def delete(cnvrg, logger, slug, name, tag):
    """
    Deletes an image
    """

    try:
        image = cnvrg.images.get(slug=slug, name=name, tag=tag)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return

    image.delete()
