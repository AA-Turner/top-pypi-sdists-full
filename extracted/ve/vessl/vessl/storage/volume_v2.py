import base64
import os
import time
from typing import Optional

from openapi_client import (
    ProtoTag,
    ResponseVolumeV2FederateInfo,
    ResponseVolumeV2Info,
    StorageGoogleStorageFederationToken,
    StorageS3FederationToken,
    VolumeV2CreateAPIInput,
    VolumeV2FederateAPIInput,
)
from vessl import vessl_api
from vessl.organization import _get_organization_name
from vessl.storage.abstract_volume import AbstractVolume
from vessl.storage.file import VolumeFile
from vessl.storage.gcs import GCSVolume
from vessl.storage.s3 import S3Volume
from vessl.util import constant
from vessl.util.common import safe_cast
from vessl.util.fmt import format_size
from vessl.volume import VolumePathRef, parse_volume_url


def list_volumes(
    storage_name: str, keyword: Optional[str] = None, **kwargs
) -> list[ResponseVolumeV2Info]:
    """List volumes in provided storage name with default organization.
    If you want to override the default organization, then pass `organization_name` as `**kwargs`.

    Args:
        storage_name: name of the storage
        keyword: optional search keyword

    Example:
        ```python
        vessl.storage.list_volumes(storage_name="my-storage")
        ```
    """
    query_keys = {"limit", "offset"}
    query_kwargs = {k: v for k, v in kwargs.items() if k in query_keys}

    return vessl_api.volume_v2_list_api(
        organization_name=_get_organization_name(**kwargs),
        storage_name=storage_name,
        keyword=keyword,
        **query_kwargs,
    ).results


def create_volume(name: str, storage_name: str, tags: tuple[str, ...] = (), **kwargs):
    """Create volume in provided storage name with default organization.
    If you want to override the default organization, then pass `organization_name` as `**kwargs`.

    Args:
        name: The name of the volume.
        storage_name: The name of the storage.
        tags: The tags of the volume.

    Example:
        ```python
        vessl.storage.create_volume(
            name="my-volume",
            storage_name="my-storage",
            tags=("my-tag1", "my-tag2"),
        )
        ```
    """
    vessl_api.volume_v2_create_api(
        organization_name=_get_organization_name(**kwargs),
        storage_name=storage_name,
        volume_v2_create_api_input=VolumeV2CreateAPIInput(
            volume_name=name,
            tags=[ProtoTag(name=tag) for tag in tags],
        ),
    )


def delete_volume(name: str, storage_name: str, **kwargs):
    """Delete volume in provided storage name with default organization.
    If you want to override the default organization, then pass `organization_name` as `**kwargs`.

    Args:
        name: The name of the volume.
        storage_name: The name of the storage.

    Example:
        ```python
        vessl.storage.delete_volume(name="my-volume", storage_name="my-storage")
        ```
    """
    vessl_api.volume_v2_delete_api(
        organization_name=_get_organization_name(**kwargs),
        storage_name=storage_name,
        volume_name=name,
    )


def volume_federate(
    storage_name: str, volume_name: str, federation_type: str, **kwargs
) -> ResponseVolumeV2FederateInfo:
    """
    Get federation information for a Volume.

    Args:
        storage_name (str): Name of the storage.
        volume_name (str): Name of the volume in the storage.

    Example:
        ```python
        vessl.storage.volume_federate(
            storage_name="my-storage-1",
            volume_name="my-volume-1",
        )
        ```
    """

    return vessl_api.volume_v2_federate_api(
        organization_name=_get_organization_name(**kwargs),
        storage_name=storage_name,
        volume_name=volume_name,
        volume_v2_federate_api_input=VolumeV2FederateAPIInput(federation_type=federation_type),
    )


def _get_volume_with_federate(
    source_storage_name: str, source_volume_name: str, federation_type: str
) -> AbstractVolume:
    fed = volume_federate(
        storage_name=source_storage_name,
        volume_name=source_volume_name,
        federation_type=federation_type,
    )

    insecure_skip_tls_verify = safe_cast(os.environ.get('VESSL_INSECURE_SKIP_TLS_VERIFY'), bool, False)
    verify_tls = not insecure_skip_tls_verify

    if fed.type == "s3":
        s3_token: Optional[StorageS3FederationToken] = fed.s3_token
        if s3_token is None:
            return S3Volume(
                bucket_name=fed.bucket_name,
                base_path=fed.path,
                verify_tls=verify_tls,
            )
        else:
            return S3Volume(
                aws_access_key_id=s3_token.access_key_id,
                aws_secret_access_key=s3_token.secret_access_key,
                aws_session_token=s3_token.session_token,
                bucket_name=fed.bucket_name,
                base_path=fed.path,
                region=fed.region,
                endpoint_url=fed.endpoint,
                force_path_style=fed.force_path_style,
                verify_tls=verify_tls,
            )
    elif fed.type == "gcs":
        gcs_token: StorageGoogleStorageFederationToken = fed.gcs_token
        cred_decoded = base64.b64decode(gcs_token.base64_credentials).decode("utf-8")
        return GCSVolume(
            bucket_name=fed.bucket_name,
            base_path=fed.path,
            gcp_api_key_json=cred_decoded,
        )
    else:
        raise NotImplementedError(f"invalid type: {fed.type}")


def copy_volume_file(source: VolumePathRef, dest: VolumePathRef):
    t2t = (source.type, dest.type)
    if t2t == (constant.VOLUME_TYPE_VOLUME, constant.VOLUME_TYPE_LOCAL):
        download_volume_file(
            source_storage_name=source.storage_name,
            source_volume_name=source.volume_name,
            dest_path=dest.local_path,
        )
    elif t2t == (constant.VOLUME_TYPE_LOCAL, constant.VOLUME_TYPE_VOLUME):
        upload_volume_file(
            source_path=source.local_path,
            dest_storage_name=dest.storage_name,
            dest_volume_name=dest.volume_name,
            dest_path=dest.volume_path,
        )
    else:
        raise NotImplementedError(
            "The sv:// scheme for volume operations is deprecated. "
            "For backward compatibility, please use vessl.copy_volume_file() instead of vessl.storage.copy_volume_file()."
        )


def list_volume_files(storage_name: str, volume_name: str, path: str = "") -> list[VolumeFile]:
    """
    List all files in a volume.

    Arguments:
         storage_name (str): Name of the storage.
         volume_name (str): Name of the volume in the storage.
         path (str, optional): Path of directory to list. Defaults to "".

    Example:
        ```python
        vessl.storage.list_volume_files(
            storage_name="my-storage",
            volume_name="my-volume",
        )
        ```
    """
    volume = _get_volume_with_federate(storage_name, volume_name, federation_type="read")
    return volume.list(path)


def download_volume_file(source_storage_name: str, source_volume_name: str, dest_path: str):
    """
    Download a file from a volume.

    Arguments:
         source_storage_name (str): Name of the storage.
         source_volume_name (str): Name of the volume in the storage.
         dest_path (str): Path of local directory to download the file to.

    Examples:
        ```python
        vessl.storage.download_volume_file(
            source_storage_name="my-storage",
            source_volume_name="my-volume",
            dest_path="models"
        )
        ```
    """
    os.makedirs(dest_path, exist_ok=True)

    volume = _get_volume_with_federate(
        source_storage_name, source_volume_name, federation_type="read"
    )

    progress_last_printed = time.time()

    def progress_callback(
        total_file_count,
        current_file_index,
        current_file_size,
        current_file_downloaded,
        total_downloaded,
    ):
        nonlocal progress_last_printed

        now = time.time()
        if now < progress_last_printed + 5.0:
            return
        progress_last_printed = now

        print(
            f"Downloading: {current_file_index:4}/{total_file_count:4} file(s): "
            + f"{format_size(current_file_downloaded)}/{format_size(current_file_size)} "
            + f"({current_file_downloaded/current_file_size*100:5.2f}%), "
            + f"total {format_size(total_downloaded)}"
        )

    volume.download_directory("", destination=dest_path, progress_callback=progress_callback)


def upload_volume_file(
    source_path: str, dest_storage_name: str, dest_volume_name: str, dest_path: str = ""
):
    """
    Upload a file from a volume.

    Arguments:
         source_path (str): Path of local directory or file to upload.
         dest_storage_name (str): Name of the storage.
         dest_volume_name (str): Name of the volume in the storage.
         dest_path (str): Path of volume directory to upload the file to. Defaults to "".

    Examples:
        ```python
        vessl.storage.upload_volume_file(
            source_path="/path/to/file",
            dest_storage_name="my-storage",
            dest_volume_name="my-volume",
        )
        ```
    """
    volume = _get_volume_with_federate(dest_storage_name, dest_volume_name, federation_type="write")

    progress_last_printed = time.time()

    def progress_callback(
        total_file_count,
        current_file_index,
        current_file_size,
        current_file_downloaded,
        total_downloaded,
    ):
        nonlocal progress_last_printed

        now = time.time()
        if now < progress_last_printed + 5.0:
            return
        progress_last_printed = now

        print(
            f"Downloading: {current_file_index:4}/{total_file_count:4} file(s): "
            + f"{format_size(current_file_downloaded)}/{format_size(current_file_size)} "
            + f"({current_file_downloaded/current_file_size*100:5.2f}%), "
            + f"total {format_size(total_downloaded)}"
        )

    if os.path.isdir(source_path):
        volume.upload_directory(
            source_path, destination=dest_path, progress_callback=progress_callback
        )
    else:
        destination = os.path.join(dest_path, os.path.basename(source_path))
        volume.upload_file(source_path, destination=destination)


def delete_volume_file(storage_name: str, volume_name: str, path: str, recursive: bool = False):
    """
    Delete a file from a volume.

    Arguments:
         storage_name (str): Name of the storage.
         volume_name (str): Name of the volume in the storage.
         path (str): Path of directory or file in volume to delete.
         recursive (bool, optional): If true, delete all files in this directory. Defaults to False.

    Examples:
        ```python
        vessl.storage.delete_volume_file(
            storage_name="my-storage",
            volume_name="my-volume",
            path="model.pth"
        )
        ```
    """
    volume = _get_volume_with_federate(storage_name, volume_name, federation_type="write")

    # Even if recursive=True, always call delete_file() to ensure the file is deleted
    # when the input is a file instead of a directory.
    if recursive:
        volume.delete_directory(path)
    volume.delete_file(path)
