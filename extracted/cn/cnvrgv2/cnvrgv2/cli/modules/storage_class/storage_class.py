import click
from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.cli.utils.helpers import print_generator_in_chunks
from cnvrgv2.config import error_messages
from cnvrgv2.errors import CnvrgError
from cnvrgv2.utils.validators import validate_storage_class_title


@click.group(name='storage-class')
def storage_class_group():
    pass


@storage_class_group.command()
@click.option('-t', '--title', prompt=messages.STORAGE_CLASS_PROMPT_TITLE, help=messages.STORAGE_CLASS_HELP_TITLE)
@click.option('-i', '--host-ip', prompt=messages.STORAGE_CLASS_PROMPT_HOST_IP, help=messages.STORAGE_CLASS_HELP_HOST_IP)
@click.option('-p', '--host-path', prompt=messages.STORAGE_CLASS_PROMPT_HOST_PATH,
              help=messages.STORAGE_CLASS_HELP_HOST_PATH)
@click.option('-c', '--cluster-slug', prompt=messages.STORAGE_CLASS_PROMPT_CLUSTER,
              help=messages.STORAGE_CLASS_HELP_CLUSTER)
@click.option('-w', '--wait', default=False, help=messages.STORAGE_CLASS_WAIT)
@prepare_command()
def create(cnvrg, logger, title=None, host_ip=None, host_path=None, cluster_slug=None, wait=False):
    """
    Create Storage Class
    """
    if not validate_storage_class_title(title):
        logger.log_and_echo(error_messages.INVALID_STORAGE_CLASS_TITLE.format(title), error=True)
    logger.log_and_echo(messages.STORAGE_CLASS_CREATING_MESSAGE)
    new_storage_class = cnvrg.storage_classes.create(title=title, host_ip=host_ip,
                                                     host_path=host_path, cluster=cluster_slug, wait=wait)
    success_message = messages.CREATED_SUCCESSFULLY.format(new_storage_class.title, new_storage_class.slug)
    logger.log_and_echo(success_message)


@storage_class_group.command()
@click.option('-t', '--title', prompt=messages.STORAGE_CLASS_PROMPT_CONNECT_TITLE,
              help=messages.STORAGE_CLASS_HELP_CONNECT_TITLE)
@click.option('-cv', '--connect-volumes', default=False, prompt=messages.STORAGE_CLASS_CONNECT_ALL_VOLUMES_PROMPT,
              help=messages.STORAGE_CLASS_CONNECT_ALL_VOLUMES_HELP)
@click.option('-c', '--cluster-slug', prompt=messages.STORAGE_CLASS_PROMPT_CLUSTER,
              help=messages.STORAGE_CLASS_HELP_CLUSTER)
@click.option('-w', '--wait', default=False, help=messages.STORAGE_CLASS_WAIT)
@prepare_command()
def connect(cnvrg, logger, title=None, connect_volumes=False, cluster_slug=None, wait=False):
    """
    Connect Storage Class
    """
    if not validate_storage_class_title(title):
        logger.log_and_echo(error_messages.INVALID_STORAGE_CLASS_TITLE.format(title), error=True)
    logger.log_and_echo(messages.STORAGE_CLASS_CONNECT_MESSAGE)
    connected_storage_class = cnvrg.storage_classes.connect(title=title, connect_all_volumes=connect_volumes,
                                                            cluster=cluster_slug, wait=wait)
    success_message = messages.CREATED_SUCCESSFULLY.format(connected_storage_class.title, connected_storage_class.slug)
    logger.log_and_echo(success_message)


@storage_class_group.command()
@click.option('-s', '--slug', help=messages.STORAGE_CLASS_HELP_SLUG)
@prepare_command()
def disconnect(cnvrg, logger, slug):
    """
    disconnect a storage_class
    """
    try:
        storage_class = cnvrg.storage_classes.get(slug=slug)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return
    success_message = messages.DISCONNECT_MESSAGE_SUCCESSFULLY.format(storage_class.title, storage_class.slug)
    storage_class.disconnect()
    logger.log_and_echo(success_message)


@storage_class_group.command()
@click.option('-s', '--slug', help=messages.STORAGE_CLASS_HELP_SLUG)
@prepare_command()
def delete(cnvrg, logger, slug):
    """
    Deletes a storage class
    """
    try:
        storage_class = cnvrg.storage_classes.get(slug=slug)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return
    storage_class.delete()
    success_message = messages.DELETE_MESSAGE_SUCCESSFULLY.format(storage_class.title, storage_class.slug)
    logger.log_and_echo(success_message)


@storage_class_group.command(name='get')
@click.option('-s', '--slug', help=messages.STORAGE_CLASS_HELP_SLUG)
@prepare_command()
def get(cnvrg, logger, slug):
    """
    Get a specific storage class by slug
    """
    try:
        storage_class = cnvrg.storage_classes.get(slug=slug)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return
    attributes_field_name = ["Title", "Slug", "Host IP", "Host Path", "Status"]
    attributes = ["title", "slug", "host_ip", "host_path", "status"]
    print_generator_in_chunks(
        generator=iter([storage_class]),
        chunk_size=1,
        limit=1,
        object_attributes=attributes,
        attributes_field_name=attributes_field_name,
    )


@storage_class_group.command(name='list')
@click.option('-p', '--page-size', default=20, help=messages.PAGE_SIZE_HELP)
@click.option('-s', '--sort', default="-id", help=messages.SORT_HELP)
@click.option('-cs', '--chunk-size', default=20, type=int, help='Number of storage classes to display at a time')
@click.option('-l', '--limit', type=int, help='Maximum number of storage classes to display')
@prepare_command()
def list_command(cnvrg, logger, sort, chunk_size, limit, page_size):
    """
    List all storage classes
    """
    try:
        storage_classes = cnvrg.storage_classes.list(sort=sort, page_size=page_size)
    except CnvrgError as error:
        logger.log_and_echo(message=str(error), error=True)
        return
    attributes_field_name = ["Title", "Slug", "Host IP", "Host Path", "Status"]
    attributes = ["title", "slug", "host_ip", "host_path", "status"]
    print_generator_in_chunks(
        generator=storage_classes,
        chunk_size=chunk_size,
        limit=limit,
        object_attributes=attributes,
        attributes_field_name=attributes_field_name,
    )
