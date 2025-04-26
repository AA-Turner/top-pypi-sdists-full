from enum import Enum
from typing import Optional

from openapi_client import (
    ResponseKernelClusterNodeInfo,
    StorageCreateAPIInput,
    StorageValidateConnectionAPIInput,
    V1ClusterHostPathConfig,
    V1ClusterNfsConfig,
    V1Config,
    V1GcsConfig,
    V1S3Config,
)
from vessl import list_clusters, vessl_api
from vessl.organization import _get_organization_name
from vessl.util.exception import (
    NotFoundError,
    StorageConnectionError,
    VesslApiException,
)


class StorageType(Enum):
    GCS = "gcs"
    S3 = "s3"
    NFS = "cluster-nfs"
    HOST_PATH = "cluster-host-path"


def _separate_bucket_path(path: str):
    parts = path.split("/", 1)
    if len(parts) == 1:
        return path, "/"
    return parts


def list_storages(**kwargs):
    """List storages in the default organization. If you want to
    override the default organization, then pass `organization_name` as
    `**kwargs`.

    Example:
        ```python
        vessl.list_storages()
        ```
    """
    query_keys = {"limit", "offset"}
    query_kwargs = {k: v for k, v in kwargs.items() if k in query_keys}

    storage_response = vessl_api.storage_list_api(
        organization_name=_get_organization_name(**kwargs), **query_kwargs
    )

    return [storage_response.managed] + storage_response.external.results


def _get_storage_config(storage_type: StorageType, path: str):
    config = V1Config()

    if storage_type == StorageType.S3:
        bucket, base_path = _separate_bucket_path(path)
        config.s3_config = V1S3Config(
            base_path=base_path,
            bucket_name=bucket,
        )
        return config
    if storage_type == StorageType.GCS:
        bucket, base_path = _separate_bucket_path(path)
        config.gcs_config = V1GcsConfig(
            base_path=base_path,
            bucket_name=bucket,
        )
        return config
    if storage_type == StorageType.NFS:
        host, base_path = path.split(":", 1)
        config.cluster_nfs_config = V1ClusterNfsConfig(
            host=host,
            base_path=base_path,
        )
        return config
    if storage_type == StorageType.HOST_PATH:
        config.cluster_host_path_config = V1ClusterHostPathConfig(
            base_path=path,
        )
        return config


def _test_connection(storage_type: StorageType, path: str, organization_credential_name: str):
    if storage_type in {StorageType.NFS, StorageType.HOST_PATH}:
        return

    try:
        vessl_api.storage_validate_connection_api(
            organization_name=vessl_api.organization.name,
            storage_validate_connection_api_input=StorageValidateConnectionAPIInput(
                organization_credential_name=organization_credential_name,
                storage_type=storage_type.value,
                storage_config=_get_storage_config(storage_type, path),
            ),
        )
    except VesslApiException as e:
        raise StorageConnectionError(
            "Storage connection failed. Please check your bucket status and policy."
        )


def _get_cluster_id(storage_type: StorageType, cluster_name):
    if not storage_type in {StorageType.NFS, StorageType.HOST_PATH}:
        return None

    cluster_list = list_clusters()

    for cluster in cluster_list:
        cluster: ResponseKernelClusterNodeInfo
        if cluster.name == cluster_name:
            return cluster.id

    raise NotFoundError("Cluster name not found")


def create_storage(
    name: str,
    storage_type: StorageType,
    path: str,
    credential_name: Optional[str] = None,
    cluster_name: Optional[str] = None,
):
    """Create storage.

    Args:
        name(str): The name of the storage to create.
        storage_type(StorageType): The type of storage to create. (GCS|S3|CLUSTER_NFS|CLUSTER_HOST_PATH)
        path(str): The path of the storage.
                    - For `s3` : Path must in `{bucket_name}/{path}` (e.g. my-bucket)
                    - For `gcs` : Path must in `{bucket_name}/{path}` (e.g. my-bucket)
                    - For `nfs` : Path must be in `{server}:{path}` format (e.g. 192.168.1.100:/shared/data)
                    - For `host-path` : Path must be an absolute local path (e.g. /data/host-folder)
        credential_name(str): The name of the credential to use. Required if `storage_type` is S3 or GCS
        cluster_name(str): The name of the cluster to use. Required if `storage_type` is NFS or HostPath

    Example:
        ```python
        vessl.create_storage(
            name="my-storage",
            storage_type=vessl.StorageType.S3,
            path="my-bucket",
            credential_name="my-credential",
        )
        ```
    """
    if storage_type in {StorageType.GCS, StorageType.S3} and not credential_name:
        raise NotFoundError("You must provide a credential name when storage type is S3 or GCS")
    if (
        storage_type in {StorageType.NFS, StorageType.HOST_PATH}
        and not cluster_name
    ):
        raise NotFoundError(
            "You must provide a cluster name when storage type is ClusterNFS or ClusterHostPath"
        )

    _test_connection(storage_type, path, credential_name)

    vessl_api.storage_create_api(
        organization_name=vessl_api.organization.name,
        storage_create_api_input=StorageCreateAPIInput(
            name=name,
            cluster_id=_get_cluster_id(storage_type, cluster_name),
            organization_credential_name=credential_name,
            storage_config=_get_storage_config(storage_type, path),
            storage_type=storage_type.value,
        ),
    )


def delete_storage(name: str):
    """Delete storage.

    Args:
        name(str): The name of the storage to delete.

    Example:
        ```python
        vessl.delete_storage(name="my-storage")
        ```
    """
    vessl_api.storage_delete_api(
        organization_name=vessl_api.organization.name,
        storage_name=name,
    )
