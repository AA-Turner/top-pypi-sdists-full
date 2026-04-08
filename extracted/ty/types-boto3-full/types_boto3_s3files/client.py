"""
Type annotations for s3files service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_s3files.client import S3FilesClient

    session = Session()
    client: S3FilesClient = session.client("s3files")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListAccessPointsPaginator,
    ListFileSystemsPaginator,
    ListMountTargetsPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    CreateAccessPointRequestTypeDef,
    CreateAccessPointResponseTypeDef,
    CreateFileSystemRequestTypeDef,
    CreateFileSystemResponseTypeDef,
    CreateMountTargetRequestTypeDef,
    CreateMountTargetResponseTypeDef,
    DeleteAccessPointRequestTypeDef,
    DeleteFileSystemPolicyRequestTypeDef,
    DeleteFileSystemRequestTypeDef,
    DeleteMountTargetRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAccessPointRequestTypeDef,
    GetAccessPointResponseTypeDef,
    GetFileSystemPolicyRequestTypeDef,
    GetFileSystemPolicyResponseTypeDef,
    GetFileSystemRequestTypeDef,
    GetFileSystemResponseTypeDef,
    GetMountTargetRequestTypeDef,
    GetMountTargetResponseTypeDef,
    GetSynchronizationConfigurationRequestTypeDef,
    GetSynchronizationConfigurationResponseTypeDef,
    ListAccessPointsRequestTypeDef,
    ListAccessPointsResponseTypeDef,
    ListFileSystemsRequestTypeDef,
    ListFileSystemsResponseTypeDef,
    ListMountTargetsRequestTypeDef,
    ListMountTargetsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutFileSystemPolicyRequestTypeDef,
    PutSynchronizationConfigurationRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateMountTargetRequestTypeDef,
    UpdateMountTargetResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("S3FilesClient",)


class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class S3FilesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files.html#S3Files.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        S3FilesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files.html#S3Files.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#generate_presigned_url)
        """

    def create_access_point(
        self, **kwargs: Unpack[CreateAccessPointRequestTypeDef]
    ) -> CreateAccessPointResponseTypeDef:
        """
        Creates an S3 File System Access Point for application-specific access with
        POSIX user identity and root directory enforcement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/create_access_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#create_access_point)
        """

    def create_file_system(
        self, **kwargs: Unpack[CreateFileSystemRequestTypeDef]
    ) -> CreateFileSystemResponseTypeDef:
        """
        Creates an S3 File System resource scoped to a bucket or prefix within a
        bucket, enabling file system access to S3 data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/create_file_system.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#create_file_system)
        """

    def create_mount_target(
        self, **kwargs: Unpack[CreateMountTargetRequestTypeDef]
    ) -> CreateMountTargetResponseTypeDef:
        """
        Creates a mount target resource as an endpoint for mounting the S3 File System
        from compute resources in a specific Availability Zone and VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/create_mount_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#create_mount_target)
        """

    def delete_access_point(
        self, **kwargs: Unpack[DeleteAccessPointRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an S3 File System Access Point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/delete_access_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#delete_access_point)
        """

    def delete_file_system(
        self, **kwargs: Unpack[DeleteFileSystemRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an S3 File System.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/delete_file_system.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#delete_file_system)
        """

    def delete_file_system_policy(
        self, **kwargs: Unpack[DeleteFileSystemPolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the IAM resource policy of an S3 File System.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/delete_file_system_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#delete_file_system_policy)
        """

    def delete_mount_target(
        self, **kwargs: Unpack[DeleteMountTargetRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified mount target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/delete_mount_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#delete_mount_target)
        """

    def get_access_point(
        self, **kwargs: Unpack[GetAccessPointRequestTypeDef]
    ) -> GetAccessPointResponseTypeDef:
        """
        Returns resource information for an S3 File System Access Point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/get_access_point.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#get_access_point)
        """

    def get_file_system(
        self, **kwargs: Unpack[GetFileSystemRequestTypeDef]
    ) -> GetFileSystemResponseTypeDef:
        """
        Returns resource information for the specified S3 File System including status,
        configuration, and metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/get_file_system.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#get_file_system)
        """

    def get_file_system_policy(
        self, **kwargs: Unpack[GetFileSystemPolicyRequestTypeDef]
    ) -> GetFileSystemPolicyResponseTypeDef:
        """
        Returns the IAM resource policy of an S3 File System.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/get_file_system_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#get_file_system_policy)
        """

    def get_mount_target(
        self, **kwargs: Unpack[GetMountTargetRequestTypeDef]
    ) -> GetMountTargetResponseTypeDef:
        """
        Returns detailed resource information for the specified mount target including
        network configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/get_mount_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#get_mount_target)
        """

    def get_synchronization_configuration(
        self, **kwargs: Unpack[GetSynchronizationConfigurationRequestTypeDef]
    ) -> GetSynchronizationConfigurationResponseTypeDef:
        """
        Returns the synchronization configuration for the specified S3 File System,
        including import data rules and expiration data rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/get_synchronization_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#get_synchronization_configuration)
        """

    def list_access_points(
        self, **kwargs: Unpack[ListAccessPointsRequestTypeDef]
    ) -> ListAccessPointsResponseTypeDef:
        """
        Returns resource information for all S3 File System Access Points associated
        with the specified S3 File System.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/list_access_points.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#list_access_points)
        """

    def list_file_systems(
        self, **kwargs: Unpack[ListFileSystemsRequestTypeDef]
    ) -> ListFileSystemsResponseTypeDef:
        """
        Returns a list of all S3 File Systems owned by the account with optional
        filtering by bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/list_file_systems.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#list_file_systems)
        """

    def list_mount_targets(
        self, **kwargs: Unpack[ListMountTargetsRequestTypeDef]
    ) -> ListMountTargetsResponseTypeDef:
        """
        Returns resource information for all mount targets with optional filtering by
        file system, access point, and VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/list_mount_targets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#list_mount_targets)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags for S3 Files resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#list_tags_for_resource)
        """

    def put_file_system_policy(
        self, **kwargs: Unpack[PutFileSystemPolicyRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Creates or replaces the IAM resource policy for an S3 File System to control
        access permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/put_file_system_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#put_file_system_policy)
        """

    def put_synchronization_configuration(
        self, **kwargs: Unpack[PutSynchronizationConfigurationRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Creates or updates the synchronization configuration for the specified S3 File
        System, including import data rules and expiration data rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/put_synchronization_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#put_synchronization_configuration)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates tags for S3 Files resources using standard Amazon Web Services tagging
        APIs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from S3 Files resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#untag_resource)
        """

    def update_mount_target(
        self, **kwargs: Unpack[UpdateMountTargetRequestTypeDef]
    ) -> UpdateMountTargetResponseTypeDef:
        """
        Updates the mount target resource, specifically security group configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/update_mount_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#update_mount_target)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_access_points"]
    ) -> ListAccessPointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_file_systems"]
    ) -> ListFileSystemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_mount_targets"]
    ) -> ListMountTargetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3files/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/client/#get_paginator)
        """
