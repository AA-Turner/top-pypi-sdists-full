"""
Type annotations for dsql service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dsql/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_dsql.type_defs import ClusterSummaryTypeDef

    data: ClusterSummaryTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    ClusterStatusType,
    EncryptionStatusType,
    EncryptionTypeType,
    StreamFailureErrorCodeType,
    StreamStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "ClusterSummaryTypeDef",
    "CreateClusterInputTypeDef",
    "CreateClusterOutputTypeDef",
    "CreateStreamInputTypeDef",
    "CreateStreamOutputTypeDef",
    "DeleteClusterInputTypeDef",
    "DeleteClusterOutputTypeDef",
    "DeleteClusterPolicyInputTypeDef",
    "DeleteClusterPolicyOutputTypeDef",
    "DeleteStreamInputTypeDef",
    "DeleteStreamOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionDetailsTypeDef",
    "GetClusterInputTypeDef",
    "GetClusterInputWaitExtraTypeDef",
    "GetClusterInputWaitTypeDef",
    "GetClusterOutputTypeDef",
    "GetClusterPolicyInputTypeDef",
    "GetClusterPolicyOutputTypeDef",
    "GetStreamInputTypeDef",
    "GetStreamInputWaitExtraTypeDef",
    "GetStreamInputWaitTypeDef",
    "GetStreamOutputTypeDef",
    "GetVpcEndpointServiceNameInputTypeDef",
    "GetVpcEndpointServiceNameOutputTypeDef",
    "KinesisTargetDefinitionTypeDef",
    "ListClustersInputPaginateTypeDef",
    "ListClustersInputTypeDef",
    "ListClustersOutputTypeDef",
    "ListStreamsInputPaginateTypeDef",
    "ListStreamsInputTypeDef",
    "ListStreamsOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "MultiRegionPropertiesOutputTypeDef",
    "MultiRegionPropertiesTypeDef",
    "MultiRegionPropertiesUnionTypeDef",
    "PaginatorConfigTypeDef",
    "PutClusterPolicyInputTypeDef",
    "PutClusterPolicyOutputTypeDef",
    "ResponseMetadataTypeDef",
    "StatusReasonTypeDef",
    "StreamSummaryTypeDef",
    "TagResourceInputTypeDef",
    "TargetDefinitionTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateClusterInputTypeDef",
    "UpdateClusterOutputTypeDef",
    "WaiterConfigTypeDef",
)


class ClusterSummaryTypeDef(TypedDict):
    identifier: str
    arn: str


class EncryptionDetailsTypeDef(TypedDict):
    encryptionType: EncryptionTypeType
    encryptionStatus: EncryptionStatusType
    kmsKeyArn: NotRequired[str]


class MultiRegionPropertiesOutputTypeDef(TypedDict):
    witnessRegion: NotRequired[str]
    clusters: NotRequired[list[str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteClusterInputTypeDef(TypedDict):
    identifier: str
    clientToken: NotRequired[str]


class DeleteClusterPolicyInputTypeDef(TypedDict):
    identifier: str
    expectedPolicyVersion: NotRequired[str]
    clientToken: NotRequired[str]


class DeleteStreamInputTypeDef(TypedDict):
    clusterIdentifier: str
    streamIdentifier: str
    clientToken: NotRequired[str]


class GetClusterInputTypeDef(TypedDict):
    identifier: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class GetClusterPolicyInputTypeDef(TypedDict):
    identifier: str


class GetStreamInputTypeDef(TypedDict):
    clusterIdentifier: str
    streamIdentifier: str


class StatusReasonTypeDef(TypedDict):
    error: StreamFailureErrorCodeType
    updatedAt: datetime


class GetVpcEndpointServiceNameInputTypeDef(TypedDict):
    identifier: str


class KinesisTargetDefinitionTypeDef(TypedDict):
    streamArn: str
    roleArn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListClustersInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListStreamsInputTypeDef(TypedDict):
    clusterIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class StreamSummaryTypeDef(TypedDict):
    clusterIdentifier: str
    streamIdentifier: str
    arn: str
    creationTime: datetime
    status: StreamStatusType


class ListTagsForResourceInputTypeDef(TypedDict):
    resourceArn: str


class MultiRegionPropertiesTypeDef(TypedDict):
    witnessRegion: NotRequired[str]
    clusters: NotRequired[Sequence[str]]


class PutClusterPolicyInputTypeDef(TypedDict):
    identifier: str
    policy: str
    bypassPolicyLockoutSafetyCheck: NotRequired[bool]
    expectedPolicyVersion: NotRequired[str]
    clientToken: NotRequired[str]


class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class CreateClusterOutputTypeDef(TypedDict):
    identifier: str
    arn: str
    status: ClusterStatusType
    creationTime: datetime
    multiRegionProperties: MultiRegionPropertiesOutputTypeDef
    encryptionDetails: EncryptionDetailsTypeDef
    deletionProtectionEnabled: bool
    endpoint: str
    ResponseMetadata: ResponseMetadataTypeDef


CreateStreamOutputTypeDef = TypedDict(
    "CreateStreamOutputTypeDef",
    {
        "clusterIdentifier": str,
        "streamIdentifier": str,
        "arn": str,
        "status": StreamStatusType,
        "creationTime": datetime,
        "ordering": Literal["UNORDERED"],
        "format": Literal["JSON"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DeleteClusterOutputTypeDef(TypedDict):
    identifier: str
    arn: str
    status: ClusterStatusType
    creationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClusterPolicyOutputTypeDef(TypedDict):
    policyVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteStreamOutputTypeDef(TypedDict):
    clusterIdentifier: str
    streamIdentifier: str
    arn: str
    status: StreamStatusType
    creationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetClusterOutputTypeDef(TypedDict):
    identifier: str
    arn: str
    status: ClusterStatusType
    creationTime: datetime
    deletionProtectionEnabled: bool
    multiRegionProperties: MultiRegionPropertiesOutputTypeDef
    tags: dict[str, str]
    encryptionDetails: EncryptionDetailsTypeDef
    endpoint: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetClusterPolicyOutputTypeDef(TypedDict):
    policy: str
    policyVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetVpcEndpointServiceNameOutputTypeDef(TypedDict):
    serviceName: str
    clusterVpcEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListClustersOutputTypeDef(TypedDict):
    clusters: list[ClusterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutClusterPolicyOutputTypeDef(TypedDict):
    policyVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterOutputTypeDef(TypedDict):
    identifier: str
    arn: str
    status: ClusterStatusType
    creationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetClusterInputWaitExtraTypeDef(TypedDict):
    identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetClusterInputWaitTypeDef(TypedDict):
    identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetStreamInputWaitExtraTypeDef(TypedDict):
    clusterIdentifier: str
    streamIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetStreamInputWaitTypeDef(TypedDict):
    clusterIdentifier: str
    streamIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class TargetDefinitionTypeDef(TypedDict):
    kinesis: NotRequired[KinesisTargetDefinitionTypeDef]


class ListClustersInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamsInputPaginateTypeDef(TypedDict):
    clusterIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamsOutputTypeDef(TypedDict):
    streams: list[StreamSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


MultiRegionPropertiesUnionTypeDef = Union[
    MultiRegionPropertiesTypeDef, MultiRegionPropertiesOutputTypeDef
]
CreateStreamInputTypeDef = TypedDict(
    "CreateStreamInputTypeDef",
    {
        "clusterIdentifier": str,
        "targetDefinition": TargetDefinitionTypeDef,
        "ordering": Literal["UNORDERED"],
        "format": Literal["JSON"],
        "tags": NotRequired[Mapping[str, str]],
        "clientToken": NotRequired[str],
    },
)
GetStreamOutputTypeDef = TypedDict(
    "GetStreamOutputTypeDef",
    {
        "clusterIdentifier": str,
        "streamIdentifier": str,
        "arn": str,
        "status": StreamStatusType,
        "creationTime": datetime,
        "ordering": Literal["UNORDERED"],
        "format": Literal["JSON"],
        "targetDefinition": TargetDefinitionTypeDef,
        "statusReason": StatusReasonTypeDef,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateClusterInputTypeDef(TypedDict):
    deletionProtectionEnabled: NotRequired[bool]
    kmsEncryptionKey: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]
    multiRegionProperties: NotRequired[MultiRegionPropertiesUnionTypeDef]
    policy: NotRequired[str]
    bypassPolicyLockoutSafetyCheck: NotRequired[bool]


class UpdateClusterInputTypeDef(TypedDict):
    identifier: str
    deletionProtectionEnabled: NotRequired[bool]
    kmsEncryptionKey: NotRequired[str]
    clientToken: NotRequired[str]
    multiRegionProperties: NotRequired[MultiRegionPropertiesUnionTypeDef]
