from typing import Optional

import click

from openapi_client import ResponseStorageV2Info
from vessl.cli._base import (
    VesslGroup,
    vessl_argument,
    vessl_conditional_option,
    vessl_option,
)
from vessl.cli._util import print_table, truncate_datetime
from vessl.storage import StorageType, create_storage, delete_storage, list_storages
from vessl.util.prompt import generic_prompter, prompt_confirm


@click.command(name="storage", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@vessl_option(
    "--limit",
    type=click.INT,
    required=False,
    default=None,
)
def list(limit: Optional[int]):
    storages = list_storages(limit=limit)
    print_table(
        storages,
        ["Name", "IsVESSLManaged", "Path", "Created", "Updated"],
        lambda x: [
            x.name,
            x.is_vessl_managed,
            _get_storage_path(x),
            truncate_datetime(x.created_dt),
            truncate_datetime(x.updated_dt),
        ],
    )


def _get_storage_path(storage: ResponseStorageV2Info):
    if storage.is_vessl_managed:
        return ""
    if storage.type == StorageType.GCS.value:
        return f"gs://{storage.config.gcs_config.bucket_name}"
    if storage.type == StorageType.S3.value:
        return f"s3://{storage.config.s3_config.bucket_name}"
    if storage.type == StorageType.NFS.value:
        return f"nfs://{storage.config.cluster_nfs_config.host}:{storage.config.cluster_nfs_config.base_path}"
    if storage.type == StorageType.HOST_PATH.value:
        return f"host-path:{storage.config.cluster_host_path_config.base_path}"


def _storage_type_callback(ctx: click.Context, param: click.Parameter, value: str) -> StorageType:
    if value == "gcs":
        return StorageType.GCS
    if value == "s3":
        return StorageType.S3
    if value == "nfs":
        return StorageType.NFS
    if value == "host-path":
        return StorageType.HOST_PATH
    raise click.BadParameter("Unknown storage type")


@cli.vessl_command()
@vessl_argument(
    "name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Storage name"),
)
@vessl_option(
    "--storage-type",
    type=click.Choice(["gcs", "s3", "nfs", "host-path"]),
    prompter=generic_prompter("Storage type; gcs|s3|nfs|host-path"),
    help="\n".join(
        [
            "\b",
            "Specify the storage type. Supported values:",
            "- `gcs`       : Google Cloud Storage",
            "- `s3`        : Amazon S3 storage",
            "- `nfs`       : NFS storage",
            "- `host-path` : host-based local storage",
        ]
    ),
    required=True,
    callback=_storage_type_callback,
)
@vessl_option(
    "--path",
    prompt="Storage path",
    prompter=generic_prompter("Storage path"),
    help="\n".join(
        [
            "\b",
            "Specify the path for the operation. The path format must match the selected storage type:",
            "- For `gcs`       : Path must in `{bucket_name}/{path}` (e.g. my-bucket)",
            "- For `s3`        : Path must in `{bucket_name}/{path}` (e.g. my-bucket)",
            "- For `nfs`       : Path must be in `{server}:{path}` format (e.g. 192.168.1.100:/shared/data)",
            "- For `host-path` : Path must be an absolute local path (e.g. /data/host-folder)",
        ]
    ),
    required=True,
)
@vessl_conditional_option(
    "--credential-name",
    prompt="Credentials name",
    prompter=generic_prompter("Credentials name"),
    condition=("storage_type", [StorageType.GCS.value, StorageType.S3.value]),
    help="Specify the credential name of the storage. This option is required when Storage Type (`--storage-type`) is gcs|s3.",
)
@vessl_conditional_option(
    "--cluster-name",
    prompt="Cluster name",
    condition=(
        "storage_type",
        [StorageType.NFS.value, StorageType.HOST_PATH.value],
    ),
    help="Specify the name of the cluster. This option is required when Storage type (`--storage-type`) is nfs|host-path",
)
def create(
    name: str,
    storage_type: StorageType,
    path: str,
    credential_name: Optional[str],
    cluster_name: Optional[str],
):
    create_storage(name, storage_type, path, credential_name, cluster_name)


@cli.vessl_command()
@vessl_argument(
    "name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Storage name"),
)
def delete(name: str):
    if not prompt_confirm(f"Are you sure to delete external storage `{name}`?"):
        return

    delete_storage(name)
