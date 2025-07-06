import click
from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.cli.utils.helpers import print_generator_in_chunks
from cnvrgv2.config import error_messages
from cnvrgv2.errors import CnvrgError
from cnvrgv2.utils.validators import validate_volume_title


@click.group(name='volume')
def volume_group():
    pass


@volume_group.command()
@click.option('-t', '--title', prompt=messages.VOLUME_TITLE_PROMPT, help=messages.VOLUME_HELP_TITLE)
@click.option('-si', '--size', prompt=messages.VOLUME_SIZE_PROMPT, help=messages.VOLUME_HELP_SIZE)
@click.option('-c', '--cluster', prompt=messages.CLUSTER_SLUG_PROMPT, help=messages.VOLUME_HELP_CLUSTER_SLUG)
@click.option('-sc', '--storage-class-slug', prompt=messages.STORAGE_CLASS_PROMPT_SLUG,
              help=messages.STORAGE_CLASS_HELP_SLUG)
@click.option('-rwm', '--read-write-many', prompt=messages.READ_WRITE_MANY_PROMPT, default=True,
              help=messages.VOLUME_HELP_RWM)
@prepare_command()
def create(cnvrg, logger, title=None, size=None, cluster=None, storage_class_slug=None, read_write_many=True):
    """
    Create volume
    """
    if not validate_volume_title(title):
        logger.log_and_echo(error_messages.INVALID_VOLUME_TITLE.format(title), error=True)
    logger.log_and_echo(messages.VOLUME_CREATING_MESSAGE)
    new_volume = cnvrg.volumes.create(title=title, size=size, cluster=cluster, storage_class=storage_class_slug,
                                      read_write_many=read_write_many)
    success_message = messages.VOLUME_CREATED_SUCCESSFULLY.format(new_volume.title, new_volume.slug)
    logger.log_and_echo(success_message)


@volume_group.command()
@click.option('-t', '--title', prompt=messages.VOLUME_TITLE_PROMPT, help=messages.VOLUME_HELP_TITLE)
@click.option('-pvc', '--pvc-name', prompt=messages.PVC_CLAIM_NAME_PROMPT_TITLE,
              help=messages.PVC_CLAIM_NAME_PROMPT_TITLE)
@click.option('-sc', '--storage-class-slug', prompt=messages.STORAGE_CLASS_PROMPT_SLUG,
              help=messages.STORAGE_CLASS_HELP_SLUG)
@prepare_command()
def connect(cnvrg, logger, title=None, pvc_name=None, storage_class_slug=None):
    """
    Connect Storage Class
    """
    if not validate_volume_title(title):
        logger.log_and_echo(error_messages.INVALID_VOLUME_TITLE.format(title), error=True)

    logger.log_and_echo(messages.VOLUME_CONNECT_MESSAGE)
    connected_volume = cnvrg.volumes.connect(title=title, pvc_name=pvc_name, storage_class=storage_class_slug)
    success_message = messages.VOLUME_CONNECT_SUCCESSFULLY.format(connected_volume.title, connected_volume.slug)
    logger.log_and_echo(success_message)


@volume_group.command()
@click.option('-s', '--slug', help=messages.VOLUME_HELP_SLUG)
@prepare_command()
def disconnect(cnvrg, logger, slug):
    """
    discconect a volume
    """
    try:
        volume = cnvrg.volumes.get(slug=slug)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return
    success_message = messages.VOLUME_DISCONNECTED_MESSAGE_SUCCESSFULLY.format(volume.title)
    volume.disconnect()
    logger.log_and_echo(success_message)


@volume_group.command()
@click.option('-s', '--slug', help=messages.VOLUME_HELP_SLUG)
@prepare_command()
def delete(cnvrg, logger, slug):
    """
    Deletes a volume
    """
    try:
        volume = cnvrg.volumes.get(slug=slug)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return
    success_message = messages.VOLUME_DELETE_MESSAGE_SUCCESSFULLY.format(volume.title)
    volume.delete()
    logger.log_and_echo(success_message)


@volume_group.command(name='list')
@click.option('-p', '--page-size', default=20, help=messages.PAGE_SIZE_HELP)
@click.option('-s', '--sort', default="-id", help=messages.SORT_HELP)
@click.option('-cs', '--chunk-size', default=20, type=int, help='Number of volumes to display at a time')
@click.option('-l', '--limit', type=int, help='Maximum number of volumes to display')
@prepare_command()
def list_command(cnvrg, logger, sort, limit, chunk_size, page_size):
    """
    List all volumes
    """
    try:
        volumes = cnvrg.volumes.list(sort=sort, page_size=page_size)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return
    attributes_field_name = ["Title", "Volume Slug", "Size", "Storage Class Slug", "Access Mode", "Status"]
    attributes = ["title", "slug", "total_space", "storage_class_slug", "access_mode", "status"]
    print_generator_in_chunks(
        generator=volumes,
        chunk_size=chunk_size,
        limit=limit,
        object_attributes=attributes,
        attributes_field_name=attributes_field_name,
        callback=volume_row_callback
    )


def volume_row_callback(row):
    """
    Custom callback to format the size from KB to GB
    """
    size_in_bytes = row[2]
    size_in_gb = size_in_bytes / (1024 ** 3)
    row[2] = f"{size_in_gb:.2f} GB"
    return row


@volume_group.command(name='get')
@click.option('-s', '--slug', help=messages.VOLUME_HELP_SLUG)
@prepare_command()
def get(cnvrg, logger, slug):
    """
    Get a specific volume by slug
    """
    try:
        volume = cnvrg.volumes.get(slug=slug)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return

    attributes_field_name = ["Title", "Volume Slug", "Size", "Storage Class Slug", "Access Mode", "Status"]
    attributes = ["title", "slug", "total_space", "storage_class_slug", "access_mode", "status"]
    print_generator_in_chunks(
        generator=iter([volume]),
        chunk_size=1,
        limit=1,
        object_attributes=attributes,
        attributes_field_name=attributes_field_name,
        callback=volume_row_callback
    )
