from typing import Optional

import click

from vessl.cli._base import vessl_argument, vessl_option
from vessl.cli._util import print_table, truncate_datetime
from vessl.cli.storage import storage_cli
from vessl.storage.file import VolumeFile
from vessl.storage.volume_v2 import (
    copy_volume_file,
    create_volume,
    delete_volume,
    delete_volume_file,
    list_volume_files,
    list_volumes,
)
from vessl.util.fmt import format_size
from vessl.util.prompt import generic_prompter, prompt_confirm
from vessl.volume import parse_volume_url


@storage_cli.vessl_command(name="list-volumes")
@vessl_option(
    "--storage-name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Storage name"),
    help="The name of the storage.",
)
@vessl_option(
    "--keyword",
    type=click.STRING,
    required=False,
    default=None,
    help="Keyword to search for.",
)
@vessl_option(
    "--limit",
    type=click.INT,
    required=False,
    default=None,
)
def list(storage_name: str, keyword: Optional[str], limit: Optional[int]):
    volumes = list_volumes(storage_name=storage_name, keyword=keyword, limit=limit)
    print_table(
        volumes,
        ["Name", "Updated", "Tags"],
        lambda x: [
            x.name,
            truncate_datetime(x.updated_dt),
            [tag.name for tag in x.tags],
        ],
    )


@storage_cli.vessl_command(name="create-volume")
@vessl_argument(
    "name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Volume Name"),
)
@vessl_option(
    "--storage-name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Storage name"),
    help="The name of the storage.",
)
@vessl_option(
    "--tag",
    type=click.STRING,
    required=False,
    default=(),
    multiple=True,
    help="The tag(s) of the volume.",
)
def create(name: str, storage_name: str, tag: tuple[str, ...]):
    create_volume(name=name, storage_name=storage_name, tags=tag)


@storage_cli.vessl_command(name="delete-volume")
@vessl_argument(
    "name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Volume Name"),
)
@vessl_option(
    "--storage-name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Storage name"),
    help="The name of the storage.",
)
def delete(name: str, storage_name: str):
    if not prompt_confirm(f"Are you sure to delete volume `{name}`?"):
        return

    delete_volume(name=name, storage_name=storage_name)


@storage_cli.vessl_command()
@vessl_argument(
    "path",
    type=click.STRING,
    required=True,
)
def list_files(path: str):
    """
    List all files in a volume.

    `PATH` must follow the following format: `volume://{STORAGE_NAME}/{VOLUME_NAME}`
    """
    path_ref = parse_volume_url(path)
    files: list[VolumeFile] = list_volume_files(
        storage_name=path_ref.storage_name,
        volume_name=path_ref.volume_name,
        path=path_ref.volume_path,
    )
    print_table(
        files,
        ["Path", "Size"],
        lambda x: [x.path, format_size(x.size)],
    )


@storage_cli.vessl_command()
@vessl_argument(
    "source",
    type=click.STRING,
    required=True,
)
@vessl_argument(
    "dest",
    type=click.STRING,
    required=True,
)
def copy_file(source: str, dest: str):
    """
    Copy a file from source to dest.

    One of `SOURCE` or `DEST` must follow the format: `volume://{STORAGE_NAME}/{VOLUME_NAME}`.
    The other must be a local file path.
    """
    source_ref = parse_volume_url(source, raise_if_not_exists=True)
    dest_ref = parse_volume_url(dest)

    copy_volume_file(source=source_ref, dest=dest_ref)


@storage_cli.vessl_command()
@vessl_argument(
    "path",
    type=click.STRING,
    required=True,
)
@vessl_option("-r", "--recursive", is_flag=True)
def delete_file(path: str, recursive: bool):
    """
    Delete a file in a volume.

    `PATH` must follow the following format: `volume://{STORAGE_NAME}/{VOLUME_NAME}`.
    """
    if not prompt_confirm(f"Are you sure to delete `{path}`?"):
        return

    path_ref = parse_volume_url(path)

    delete_volume_file(
        storage_name=path_ref.storage_name,
        volume_name=path_ref.volume_name,
        path=path_ref.volume_path,
        recursive=recursive,
    )
