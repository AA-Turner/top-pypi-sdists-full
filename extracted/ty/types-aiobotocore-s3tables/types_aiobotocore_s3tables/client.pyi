"""
Type annotations for s3tables service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_s3tables.client import S3TablesClient

    session = get_session()
    async with session.create_client("s3tables") as client:
        client: S3TablesClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListNamespacesPaginator, ListTableBucketsPaginator, ListTablesPaginator
from .type_defs import (
    CreateNamespaceRequestTypeDef,
    CreateNamespaceResponseTypeDef,
    CreateTableBucketRequestTypeDef,
    CreateTableBucketResponseTypeDef,
    CreateTableRequestTypeDef,
    CreateTableResponseTypeDef,
    DeleteNamespaceRequestTypeDef,
    DeleteTableBucketEncryptionRequestTypeDef,
    DeleteTableBucketMetricsConfigurationRequestTypeDef,
    DeleteTableBucketPolicyRequestTypeDef,
    DeleteTableBucketReplicationRequestTypeDef,
    DeleteTableBucketRequestTypeDef,
    DeleteTablePolicyRequestTypeDef,
    DeleteTableReplicationRequestTypeDef,
    DeleteTableRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetNamespaceRequestTypeDef,
    GetNamespaceResponseTypeDef,
    GetTableBucketEncryptionRequestTypeDef,
    GetTableBucketEncryptionResponseTypeDef,
    GetTableBucketMaintenanceConfigurationRequestTypeDef,
    GetTableBucketMaintenanceConfigurationResponseTypeDef,
    GetTableBucketMetricsConfigurationRequestTypeDef,
    GetTableBucketMetricsConfigurationResponseTypeDef,
    GetTableBucketPolicyRequestTypeDef,
    GetTableBucketPolicyResponseTypeDef,
    GetTableBucketReplicationRequestTypeDef,
    GetTableBucketReplicationResponseTypeDef,
    GetTableBucketRequestTypeDef,
    GetTableBucketResponseTypeDef,
    GetTableBucketStorageClassRequestTypeDef,
    GetTableBucketStorageClassResponseTypeDef,
    GetTableEncryptionRequestTypeDef,
    GetTableEncryptionResponseTypeDef,
    GetTableMaintenanceConfigurationRequestTypeDef,
    GetTableMaintenanceConfigurationResponseTypeDef,
    GetTableMaintenanceJobStatusRequestTypeDef,
    GetTableMaintenanceJobStatusResponseTypeDef,
    GetTableMetadataLocationRequestTypeDef,
    GetTableMetadataLocationResponseTypeDef,
    GetTablePolicyRequestTypeDef,
    GetTablePolicyResponseTypeDef,
    GetTableRecordExpirationConfigurationRequestTypeDef,
    GetTableRecordExpirationConfigurationResponseTypeDef,
    GetTableRecordExpirationJobStatusRequestTypeDef,
    GetTableRecordExpirationJobStatusResponseTypeDef,
    GetTableReplicationRequestTypeDef,
    GetTableReplicationResponseTypeDef,
    GetTableReplicationStatusRequestTypeDef,
    GetTableReplicationStatusResponseTypeDef,
    GetTableRequestTypeDef,
    GetTableResponseTypeDef,
    GetTableStorageClassRequestTypeDef,
    GetTableStorageClassResponseTypeDef,
    ListNamespacesRequestTypeDef,
    ListNamespacesResponseTypeDef,
    ListTableBucketsRequestTypeDef,
    ListTableBucketsResponseTypeDef,
    ListTablesRequestTypeDef,
    ListTablesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutTableBucketEncryptionRequestTypeDef,
    PutTableBucketMaintenanceConfigurationRequestTypeDef,
    PutTableBucketMetricsConfigurationRequestTypeDef,
    PutTableBucketPolicyRequestTypeDef,
    PutTableBucketReplicationRequestTypeDef,
    PutTableBucketReplicationResponseTypeDef,
    PutTableBucketStorageClassRequestTypeDef,
    PutTableMaintenanceConfigurationRequestTypeDef,
    PutTablePolicyRequestTypeDef,
    PutTableRecordExpirationConfigurationRequestTypeDef,
    PutTableReplicationRequestTypeDef,
    PutTableReplicationResponseTypeDef,
    RenameTableRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateTableMetadataLocationRequestTypeDef,
    UpdateTableMetadataLocationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("S3TablesClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    BadRequestException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    ForbiddenException: type[BotocoreClientError]
    InternalServerErrorException: type[BotocoreClientError]
    MethodNotAllowedException: type[BotocoreClientError]
    NotFoundException: type[BotocoreClientError]
    TooManyRequestsException: type[BotocoreClientError]

class S3TablesClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables.html#S3Tables.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        S3TablesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables.html#S3Tables.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#generate_presigned_url)
        """

    async def create_namespace(
        self, **kwargs: Unpack[CreateNamespaceRequestTypeDef]
    ) -> CreateNamespaceResponseTypeDef:
        """
        Creates a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/create_namespace.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#create_namespace)
        """

    async def create_table(
        self, **kwargs: Unpack[CreateTableRequestTypeDef]
    ) -> CreateTableResponseTypeDef:
        """
        Creates a new table associated with the given namespace in a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/create_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#create_table)
        """

    async def create_table_bucket(
        self, **kwargs: Unpack[CreateTableBucketRequestTypeDef]
    ) -> CreateTableBucketResponseTypeDef:
        """
        Creates a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/create_table_bucket.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#create_table_bucket)
        """

    async def delete_namespace(
        self, **kwargs: Unpack[DeleteNamespaceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_namespace.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#delete_namespace)
        """

    async def delete_table(
        self, **kwargs: Unpack[DeleteTableRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#delete_table)
        """

    async def delete_table_bucket(
        self, **kwargs: Unpack[DeleteTableBucketRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table_bucket.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#delete_table_bucket)
        """

    async def delete_table_bucket_encryption(
        self, **kwargs: Unpack[DeleteTableBucketEncryptionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the encryption configuration for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table_bucket_encryption.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#delete_table_bucket_encryption)
        """

    async def delete_table_bucket_metrics_configuration(
        self, **kwargs: Unpack[DeleteTableBucketMetricsConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the metrics configuration for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table_bucket_metrics_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#delete_table_bucket_metrics_configuration)
        """

    async def delete_table_bucket_policy(
        self, **kwargs: Unpack[DeleteTableBucketPolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a table bucket policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table_bucket_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#delete_table_bucket_policy)
        """

    async def delete_table_bucket_replication(
        self, **kwargs: Unpack[DeleteTableBucketReplicationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the replication configuration for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table_bucket_replication.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#delete_table_bucket_replication)
        """

    async def delete_table_policy(
        self, **kwargs: Unpack[DeleteTablePolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a table policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#delete_table_policy)
        """

    async def delete_table_replication(
        self, **kwargs: Unpack[DeleteTableReplicationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the replication configuration for a specific table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table_replication.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#delete_table_replication)
        """

    async def get_namespace(
        self, **kwargs: Unpack[GetNamespaceRequestTypeDef]
    ) -> GetNamespaceResponseTypeDef:
        """
        Gets details about a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_namespace.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_namespace)
        """

    async def get_table(self, **kwargs: Unpack[GetTableRequestTypeDef]) -> GetTableResponseTypeDef:
        """
        Gets details about a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table)
        """

    async def get_table_bucket(
        self, **kwargs: Unpack[GetTableBucketRequestTypeDef]
    ) -> GetTableBucketResponseTypeDef:
        """
        Gets details on a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_bucket.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_bucket)
        """

    async def get_table_bucket_encryption(
        self, **kwargs: Unpack[GetTableBucketEncryptionRequestTypeDef]
    ) -> GetTableBucketEncryptionResponseTypeDef:
        """
        Gets the encryption configuration for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_bucket_encryption.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_bucket_encryption)
        """

    async def get_table_bucket_maintenance_configuration(
        self, **kwargs: Unpack[GetTableBucketMaintenanceConfigurationRequestTypeDef]
    ) -> GetTableBucketMaintenanceConfigurationResponseTypeDef:
        """
        Gets details about a maintenance configuration for a given table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_bucket_maintenance_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_bucket_maintenance_configuration)
        """

    async def get_table_bucket_metrics_configuration(
        self, **kwargs: Unpack[GetTableBucketMetricsConfigurationRequestTypeDef]
    ) -> GetTableBucketMetricsConfigurationResponseTypeDef:
        """
        Gets the metrics configuration for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_bucket_metrics_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_bucket_metrics_configuration)
        """

    async def get_table_bucket_policy(
        self, **kwargs: Unpack[GetTableBucketPolicyRequestTypeDef]
    ) -> GetTableBucketPolicyResponseTypeDef:
        """
        Gets details about a table bucket policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_bucket_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_bucket_policy)
        """

    async def get_table_bucket_replication(
        self, **kwargs: Unpack[GetTableBucketReplicationRequestTypeDef]
    ) -> GetTableBucketReplicationResponseTypeDef:
        """
        Retrieves the replication configuration for a table bucket.This operation
        returns the IAM role, <code>versionToken</code>, and replication rules that
        define how tables in this bucket are replicated to other buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_bucket_replication.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_bucket_replication)
        """

    async def get_table_bucket_storage_class(
        self, **kwargs: Unpack[GetTableBucketStorageClassRequestTypeDef]
    ) -> GetTableBucketStorageClassResponseTypeDef:
        """
        Retrieves the storage class configuration for a specific table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_bucket_storage_class.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_bucket_storage_class)
        """

    async def get_table_encryption(
        self, **kwargs: Unpack[GetTableEncryptionRequestTypeDef]
    ) -> GetTableEncryptionResponseTypeDef:
        """
        Gets the encryption configuration for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_encryption.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_encryption)
        """

    async def get_table_maintenance_configuration(
        self, **kwargs: Unpack[GetTableMaintenanceConfigurationRequestTypeDef]
    ) -> GetTableMaintenanceConfigurationResponseTypeDef:
        """
        Gets details about the maintenance configuration of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_maintenance_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_maintenance_configuration)
        """

    async def get_table_maintenance_job_status(
        self, **kwargs: Unpack[GetTableMaintenanceJobStatusRequestTypeDef]
    ) -> GetTableMaintenanceJobStatusResponseTypeDef:
        """
        Gets the status of a maintenance job for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_maintenance_job_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_maintenance_job_status)
        """

    async def get_table_metadata_location(
        self, **kwargs: Unpack[GetTableMetadataLocationRequestTypeDef]
    ) -> GetTableMetadataLocationResponseTypeDef:
        """
        Gets the location of the table metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_metadata_location.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_metadata_location)
        """

    async def get_table_policy(
        self, **kwargs: Unpack[GetTablePolicyRequestTypeDef]
    ) -> GetTablePolicyResponseTypeDef:
        """
        Gets details about a table policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_policy)
        """

    async def get_table_record_expiration_configuration(
        self, **kwargs: Unpack[GetTableRecordExpirationConfigurationRequestTypeDef]
    ) -> GetTableRecordExpirationConfigurationResponseTypeDef:
        """
        Retrieves the expiration configuration settings for records in a table, and the
        status of the configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_record_expiration_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_record_expiration_configuration)
        """

    async def get_table_record_expiration_job_status(
        self, **kwargs: Unpack[GetTableRecordExpirationJobStatusRequestTypeDef]
    ) -> GetTableRecordExpirationJobStatusResponseTypeDef:
        """
        Retrieves the status, metrics, and details of the latest record expiration job
        for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_record_expiration_job_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_record_expiration_job_status)
        """

    async def get_table_replication(
        self, **kwargs: Unpack[GetTableReplicationRequestTypeDef]
    ) -> GetTableReplicationResponseTypeDef:
        """
        Retrieves the replication configuration for a specific table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_replication.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_replication)
        """

    async def get_table_replication_status(
        self, **kwargs: Unpack[GetTableReplicationStatusRequestTypeDef]
    ) -> GetTableReplicationStatusResponseTypeDef:
        """
        Retrieves the replication status for a table, including the status of
        replication to each destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_replication_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_replication_status)
        """

    async def get_table_storage_class(
        self, **kwargs: Unpack[GetTableStorageClassRequestTypeDef]
    ) -> GetTableStorageClassResponseTypeDef:
        """
        Retrieves the storage class configuration for a specific table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_storage_class.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_table_storage_class)
        """

    async def list_namespaces(
        self, **kwargs: Unpack[ListNamespacesRequestTypeDef]
    ) -> ListNamespacesResponseTypeDef:
        """
        Lists the namespaces within a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/list_namespaces.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#list_namespaces)
        """

    async def list_table_buckets(
        self, **kwargs: Unpack[ListTableBucketsRequestTypeDef]
    ) -> ListTableBucketsResponseTypeDef:
        """
        Lists table buckets for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/list_table_buckets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#list_table_buckets)
        """

    async def list_tables(
        self, **kwargs: Unpack[ListTablesRequestTypeDef]
    ) -> ListTablesResponseTypeDef:
        """
        List tables in the given table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/list_tables.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#list_tables)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all of the tags applied to a specified Amazon S3 Tables resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#list_tags_for_resource)
        """

    async def put_table_bucket_encryption(
        self, **kwargs: Unpack[PutTableBucketEncryptionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the encryption configuration for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_bucket_encryption.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#put_table_bucket_encryption)
        """

    async def put_table_bucket_maintenance_configuration(
        self, **kwargs: Unpack[PutTableBucketMaintenanceConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new maintenance configuration or replaces an existing maintenance
        configuration for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_bucket_maintenance_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#put_table_bucket_maintenance_configuration)
        """

    async def put_table_bucket_metrics_configuration(
        self, **kwargs: Unpack[PutTableBucketMetricsConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the metrics configuration for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_bucket_metrics_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#put_table_bucket_metrics_configuration)
        """

    async def put_table_bucket_policy(
        self, **kwargs: Unpack[PutTableBucketPolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new table bucket policy or replaces an existing table bucket policy
        for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_bucket_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#put_table_bucket_policy)
        """

    async def put_table_bucket_replication(
        self, **kwargs: Unpack[PutTableBucketReplicationRequestTypeDef]
    ) -> PutTableBucketReplicationResponseTypeDef:
        """
        Creates or updates the replication configuration for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_bucket_replication.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#put_table_bucket_replication)
        """

    async def put_table_bucket_storage_class(
        self, **kwargs: Unpack[PutTableBucketStorageClassRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets or updates the storage class configuration for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_bucket_storage_class.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#put_table_bucket_storage_class)
        """

    async def put_table_maintenance_configuration(
        self, **kwargs: Unpack[PutTableMaintenanceConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new maintenance configuration or replaces an existing maintenance
        configuration for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_maintenance_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#put_table_maintenance_configuration)
        """

    async def put_table_policy(
        self, **kwargs: Unpack[PutTablePolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new table policy or replaces an existing table policy for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#put_table_policy)
        """

    async def put_table_record_expiration_configuration(
        self, **kwargs: Unpack[PutTableRecordExpirationConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates the expiration configuration settings for records in a
        table, including the status of the configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_record_expiration_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#put_table_record_expiration_configuration)
        """

    async def put_table_replication(
        self, **kwargs: Unpack[PutTableReplicationRequestTypeDef]
    ) -> PutTableReplicationResponseTypeDef:
        """
        Creates or updates the replication configuration for a specific table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_replication.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#put_table_replication)
        """

    async def rename_table(
        self, **kwargs: Unpack[RenameTableRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Renames a table or a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/rename_table.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#rename_table)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Applies one or more user-defined tags to an Amazon S3 Tables resource or
        updates existing tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes the specified user-defined tags from an Amazon S3 Tables resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#untag_resource)
        """

    async def update_table_metadata_location(
        self, **kwargs: Unpack[UpdateTableMetadataLocationRequestTypeDef]
    ) -> UpdateTableMetadataLocationResponseTypeDef:
        """
        Updates the metadata location for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/update_table_metadata_location.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#update_table_metadata_location)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_namespaces"]
    ) -> ListNamespacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_table_buckets"]
    ) -> ListTableBucketsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tables"]
    ) -> ListTablesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables.html#S3Tables.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables.html#S3Tables.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3tables/client/)
        """
