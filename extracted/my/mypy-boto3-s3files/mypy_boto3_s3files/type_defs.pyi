"""
Type annotations for s3files service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3files/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_s3files.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

from .literals import ImportTriggerType, IpAddressTypeType, LifeCycleStateType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CreateAccessPointRequestTypeDef",
    "CreateAccessPointResponseTypeDef",
    "CreateFileSystemRequestTypeDef",
    "CreateFileSystemResponseTypeDef",
    "CreateMountTargetRequestTypeDef",
    "CreateMountTargetResponseTypeDef",
    "CreationPermissionsTypeDef",
    "DeleteAccessPointRequestTypeDef",
    "DeleteFileSystemPolicyRequestTypeDef",
    "DeleteFileSystemRequestTypeDef",
    "DeleteMountTargetRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExpirationDataRuleTypeDef",
    "GetAccessPointRequestTypeDef",
    "GetAccessPointResponseTypeDef",
    "GetFileSystemPolicyRequestTypeDef",
    "GetFileSystemPolicyResponseTypeDef",
    "GetFileSystemRequestTypeDef",
    "GetFileSystemResponseTypeDef",
    "GetMountTargetRequestTypeDef",
    "GetMountTargetResponseTypeDef",
    "GetSynchronizationConfigurationRequestTypeDef",
    "GetSynchronizationConfigurationResponseTypeDef",
    "ImportDataRuleTypeDef",
    "ListAccessPointsDescriptionTypeDef",
    "ListAccessPointsRequestPaginateTypeDef",
    "ListAccessPointsRequestTypeDef",
    "ListAccessPointsResponseTypeDef",
    "ListFileSystemsDescriptionTypeDef",
    "ListFileSystemsRequestPaginateTypeDef",
    "ListFileSystemsRequestTypeDef",
    "ListFileSystemsResponseTypeDef",
    "ListMountTargetsDescriptionTypeDef",
    "ListMountTargetsRequestPaginateTypeDef",
    "ListMountTargetsRequestTypeDef",
    "ListMountTargetsResponseTypeDef",
    "ListTagsForResourceRequestPaginateTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PosixUserOutputTypeDef",
    "PosixUserTypeDef",
    "PosixUserUnionTypeDef",
    "PutFileSystemPolicyRequestTypeDef",
    "PutSynchronizationConfigurationRequestTypeDef",
    "ResponseMetadataTypeDef",
    "RootDirectoryTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateMountTargetRequestTypeDef",
    "UpdateMountTargetResponseTypeDef",
)

class TagTypeDef(TypedDict):
    key: str
    value: str

class PosixUserOutputTypeDef(TypedDict):
    uid: int
    gid: int
    secondaryGids: NotRequired[list[int]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateMountTargetRequestTypeDef(TypedDict):
    fileSystemId: str
    subnetId: str
    ipv4Address: NotRequired[str]
    ipv6Address: NotRequired[str]
    ipAddressType: NotRequired[IpAddressTypeType]
    securityGroups: NotRequired[Sequence[str]]

class CreationPermissionsTypeDef(TypedDict):
    ownerUid: int
    ownerGid: int
    permissions: str

class DeleteAccessPointRequestTypeDef(TypedDict):
    accessPointId: str

class DeleteFileSystemPolicyRequestTypeDef(TypedDict):
    fileSystemId: str

class DeleteFileSystemRequestTypeDef(TypedDict):
    fileSystemId: str
    forceDelete: NotRequired[bool]

class DeleteMountTargetRequestTypeDef(TypedDict):
    mountTargetId: str

class ExpirationDataRuleTypeDef(TypedDict):
    daysAfterLastAccess: int

class GetAccessPointRequestTypeDef(TypedDict):
    accessPointId: str

class GetFileSystemPolicyRequestTypeDef(TypedDict):
    fileSystemId: str

class GetFileSystemRequestTypeDef(TypedDict):
    fileSystemId: str

class GetMountTargetRequestTypeDef(TypedDict):
    mountTargetId: str

class GetSynchronizationConfigurationRequestTypeDef(TypedDict):
    fileSystemId: str

class ImportDataRuleTypeDef(TypedDict):
    prefix: str
    trigger: ImportTriggerType
    sizeLessThan: int

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAccessPointsRequestTypeDef(TypedDict):
    fileSystemId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListFileSystemsDescriptionTypeDef(TypedDict):
    creationTime: datetime
    fileSystemArn: str
    fileSystemId: str
    bucket: str
    status: LifeCycleStateType
    roleArn: str
    ownerId: str
    name: NotRequired[str]
    statusMessage: NotRequired[str]

class ListFileSystemsRequestTypeDef(TypedDict):
    bucket: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListMountTargetsDescriptionTypeDef(TypedDict):
    mountTargetId: str
    ownerId: str
    subnetId: str
    availabilityZoneId: NotRequired[str]
    fileSystemId: NotRequired[str]
    ipv4Address: NotRequired[str]
    ipv6Address: NotRequired[str]
    status: NotRequired[LifeCycleStateType]
    statusMessage: NotRequired[str]
    networkInterfaceId: NotRequired[str]
    vpcId: NotRequired[str]

class ListMountTargetsRequestTypeDef(TypedDict):
    fileSystemId: NotRequired[str]
    accessPointId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class PosixUserTypeDef(TypedDict):
    uid: int
    gid: int
    secondaryGids: NotRequired[Sequence[int]]

class PutFileSystemPolicyRequestTypeDef(TypedDict):
    fileSystemId: str
    policy: str

class UntagResourceRequestTypeDef(TypedDict):
    resourceId: str
    tagKeys: Sequence[str]

class UpdateMountTargetRequestTypeDef(TypedDict):
    mountTargetId: str
    securityGroups: Sequence[str]

class CreateFileSystemRequestTypeDef(TypedDict):
    bucket: str
    roleArn: str
    prefix: NotRequired[str]
    clientToken: NotRequired[str]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    acceptBucketWarning: NotRequired[bool]

class TagResourceRequestTypeDef(TypedDict):
    resourceId: str
    tags: Sequence[TagTypeDef]

class CreateFileSystemResponseTypeDef(TypedDict):
    creationTime: datetime
    fileSystemArn: str
    fileSystemId: str
    bucket: str
    prefix: str
    clientToken: str
    kmsKeyId: str
    status: LifeCycleStateType
    statusMessage: str
    roleArn: str
    ownerId: str
    tags: list[TagTypeDef]
    name: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMountTargetResponseTypeDef(TypedDict):
    availabilityZoneId: str
    ownerId: str
    mountTargetId: str
    fileSystemId: str
    subnetId: str
    ipv4Address: str
    ipv6Address: str
    networkInterfaceId: str
    vpcId: str
    securityGroups: list[str]
    status: LifeCycleStateType
    statusMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetFileSystemPolicyResponseTypeDef(TypedDict):
    fileSystemId: str
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetFileSystemResponseTypeDef(TypedDict):
    creationTime: datetime
    fileSystemArn: str
    fileSystemId: str
    bucket: str
    prefix: str
    clientToken: str
    kmsKeyId: str
    status: LifeCycleStateType
    statusMessage: str
    roleArn: str
    ownerId: str
    tags: list[TagTypeDef]
    name: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetMountTargetResponseTypeDef(TypedDict):
    availabilityZoneId: str
    ownerId: str
    mountTargetId: str
    fileSystemId: str
    subnetId: str
    ipv4Address: str
    ipv6Address: str
    networkInterfaceId: str
    vpcId: str
    securityGroups: list[str]
    status: LifeCycleStateType
    statusMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateMountTargetResponseTypeDef(TypedDict):
    availabilityZoneId: str
    ownerId: str
    mountTargetId: str
    fileSystemId: str
    subnetId: str
    ipv4Address: str
    ipv6Address: str
    networkInterfaceId: str
    vpcId: str
    securityGroups: list[str]
    status: LifeCycleStateType
    statusMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class RootDirectoryTypeDef(TypedDict):
    path: NotRequired[str]
    creationPermissions: NotRequired[CreationPermissionsTypeDef]

class GetSynchronizationConfigurationResponseTypeDef(TypedDict):
    latestVersionNumber: int
    importDataRules: list[ImportDataRuleTypeDef]
    expirationDataRules: list[ExpirationDataRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PutSynchronizationConfigurationRequestTypeDef(TypedDict):
    fileSystemId: str
    importDataRules: Sequence[ImportDataRuleTypeDef]
    expirationDataRules: Sequence[ExpirationDataRuleTypeDef]
    latestVersionNumber: NotRequired[int]

class ListAccessPointsRequestPaginateTypeDef(TypedDict):
    fileSystemId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFileSystemsRequestPaginateTypeDef(TypedDict):
    bucket: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMountTargetsRequestPaginateTypeDef(TypedDict):
    fileSystemId: NotRequired[str]
    accessPointId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsForResourceRequestPaginateTypeDef(TypedDict):
    resourceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFileSystemsResponseTypeDef(TypedDict):
    fileSystems: list[ListFileSystemsDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListMountTargetsResponseTypeDef(TypedDict):
    mountTargets: list[ListMountTargetsDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

PosixUserUnionTypeDef = Union[PosixUserTypeDef, PosixUserOutputTypeDef]

class CreateAccessPointResponseTypeDef(TypedDict):
    accessPointArn: str
    accessPointId: str
    clientToken: str
    fileSystemId: str
    status: LifeCycleStateType
    ownerId: str
    posixUser: PosixUserOutputTypeDef
    rootDirectory: RootDirectoryTypeDef
    tags: list[TagTypeDef]
    name: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAccessPointResponseTypeDef(TypedDict):
    accessPointArn: str
    accessPointId: str
    clientToken: str
    fileSystemId: str
    status: LifeCycleStateType
    ownerId: str
    posixUser: PosixUserOutputTypeDef
    rootDirectory: RootDirectoryTypeDef
    tags: list[TagTypeDef]
    name: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAccessPointsDescriptionTypeDef(TypedDict):
    accessPointArn: str
    accessPointId: str
    fileSystemId: str
    status: LifeCycleStateType
    ownerId: str
    posixUser: NotRequired[PosixUserOutputTypeDef]
    rootDirectory: NotRequired[RootDirectoryTypeDef]
    name: NotRequired[str]

class CreateAccessPointRequestTypeDef(TypedDict):
    fileSystemId: str
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    posixUser: NotRequired[PosixUserUnionTypeDef]
    rootDirectory: NotRequired[RootDirectoryTypeDef]

class ListAccessPointsResponseTypeDef(TypedDict):
    accessPoints: list[ListAccessPointsDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
