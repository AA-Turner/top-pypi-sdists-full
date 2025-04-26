import click

import vessl.volume
from vessl.cli._base import VesslGroup, vessl_argument, vessl_option
from vessl.cli._util import print_volume_files
from vessl.storage.volume_v2 import copy_volume_file as copy_volume_file_v2
from vessl.util import constant
from vessl.util.echo import print_success
from vessl.util.prompt import generic_prompter
from vessl.volume import copy_volume_file, delete_volume_file, list_volume_files


@click.command(name="volume", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@vessl_argument(
    "id",
    type=click.INT,
    required=True,
    prompter=generic_prompter("Volume ID", click.INT),
)
@click.option("-p", "--path", type=click.Path(), default="", help="Defaults to root.")
@click.option("-r", "--recursive", is_flag=True)
def list(id: int, path: str, recursive: bool):
    files = list_volume_files(
        volume_id=id,
        path=path,
        need_download_url=False,
        recursive=recursive,
    )
    print_volume_files(files)


@cli.vessl_command()
@vessl_argument(
    "id",
    type=click.INT,
    required=True,
    prompter=generic_prompter("Volume ID", click.INT),
)
@click.option("-p", "--path", type=click.Path(), required=True)
def delete(id: int, path: str):
    delete_volume_file(volume_id=id, path=path)
    print_success(f"Deleted {path}.")


@cli.vessl_command()
@vessl_option(
    "--source-id",
    type=click.INT,
    prompter=generic_prompter("Source volume ID", click.INT),
    help="If not specified, source is assumed to be local.",
)
@vessl_option(
    "--source-path",
    type=click.Path(),
    required=True,
    prompter=generic_prompter("Source path"),
)
@vessl_option(
    "--dest-id",
    type=click.INT,
    prompter=generic_prompter("Destination volume ID", click.INT),
    help="If not specified, destination is assumed to be local.",
)
@vessl_option(
    "--dest-path",
    type=click.Path(),
    required=True,
    prompter=generic_prompter("Destination path"),
)
def copy(
    source_id: int,
    source_path: str,
    dest_id: int,
    dest_path: str,
):
    copy_volume_file(
        source_volume_id=source_id,
        source_path=source_path,
        dest_volume_id=dest_id,
        dest_path=dest_path,
    )


@cli.vessl_command(hidden=True)
@click.argument(
    "source",
    type=click.STRING,
    required=True,
)
@click.argument(
    "dest",
    type=click.STRING,
    required=True,
)
def cp(source: str, dest: str):
    """Volume copy method used in backend"""

    source_ref = vessl.volume.parse_volume_url(source, raise_if_not_exists=True)
    dest_ref = vessl.volume.parse_volume_url(dest)

    if source_ref.type == constant.VOLUME_TYPE_SV or dest_ref.type == constant.VOLUME_TYPE_SV:
        # Fallback to legacy volume API.
        # If a volume is not a "sv://", then sv_id == 0; however, we want None instead.
        copy_volume_file(
            source_ref.sv_id or None,
            source_ref.sv_path or source_ref.local_path,
            dest_ref.sv_id or None,
            dest_ref.sv_path or dest_ref.local_path,
        )
    else:
        copy_volume_file_v2(source_ref, dest_ref)


@cli.vessl_command(hidden=True)
@click.argument("storage", type=click.STRING, required=True)
@click.argument("volume", type=click.STRING, required=True)
@click.argument("path", type=click.STRING, required=True)
def create_run_execution_volume(storage: str, volume: str, path: str):
    """Create run execution volume from workload."""
    vessl.volume.create_run_execution_volume_v2(storage, volume, path)
