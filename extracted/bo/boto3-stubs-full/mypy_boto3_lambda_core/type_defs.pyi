"""
Type annotations for lambda-core service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_lambda_core.type_defs import CompatibilityTypeDef

    data: CompatibilityTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    CompatibilityPolicyType,
    ComputeResourceTypeType,
    NetworkConnectorLastUpdateStatusReasonCodeType,
    NetworkConnectorLastUpdateStatusType,
    NetworkConnectorStateReasonCodeType,
    NetworkConnectorStateType,
    NetworkProtocolType,
    RuntimeAliasStateType,
    RuntimeArchitectureType,
    RuntimeReleaseStateType,
    RuntimeStateType,
    RuntimeVersionStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "CompatibilityTypeDef",
    "CreateNetworkConnectorRequestTypeDef",
    "CreateNetworkConnectorResponseTypeDef",
    "CreateRuntimeAliasRequestTypeDef",
    "CreateRuntimeAliasResponseTypeDef",
    "CreateRuntimeRequestTypeDef",
    "CreateRuntimeResponseTypeDef",
    "CreateRuntimeVersionRequestTypeDef",
    "CreateRuntimeVersionResponseTypeDef",
    "DeleteNetworkConnectorRequestTypeDef",
    "DeleteNetworkConnectorResponseTypeDef",
    "DeleteRuntimeAliasRequestTypeDef",
    "DeleteRuntimeRequestTypeDef",
    "DeleteRuntimeVersionRequestTypeDef",
    "GetNetworkConnectorRequestTypeDef",
    "GetNetworkConnectorResponseTypeDef",
    "GetRuntimeAliasRequestTypeDef",
    "GetRuntimeAliasRequestWaitTypeDef",
    "GetRuntimeAliasResponseTypeDef",
    "GetRuntimeRequestTypeDef",
    "GetRuntimeResponseTypeDef",
    "GetRuntimeVersionRequestTypeDef",
    "GetRuntimeVersionRequestWaitTypeDef",
    "GetRuntimeVersionResponseTypeDef",
    "ListNetworkConnectorVersionsRequestPaginateTypeDef",
    "ListNetworkConnectorVersionsRequestTypeDef",
    "ListNetworkConnectorVersionsResponseTypeDef",
    "ListNetworkConnectorsRequestPaginateTypeDef",
    "ListNetworkConnectorsRequestTypeDef",
    "ListNetworkConnectorsResponseTypeDef",
    "ListRuntimeAliasesRequestPaginateTypeDef",
    "ListRuntimeAliasesRequestTypeDef",
    "ListRuntimeAliasesResponseTypeDef",
    "ListRuntimeVersionsRequestPaginateTypeDef",
    "ListRuntimeVersionsRequestTypeDef",
    "ListRuntimeVersionsResponseTypeDef",
    "ListRuntimesRequestPaginateTypeDef",
    "ListRuntimesRequestTypeDef",
    "ListRuntimesResponseTypeDef",
    "NetworkConnectorConfigurationOutputTypeDef",
    "NetworkConnectorConfigurationTypeDef",
    "NetworkConnectorConfigurationUnionTypeDef",
    "NetworkConnectorSummaryTypeDef",
    "NetworkConnectorVersionSummaryTypeDef",
    "NetworkConnectorVpcEgressConfigurationOutputTypeDef",
    "NetworkConnectorVpcEgressConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PlatformTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreRuntimeRequestTypeDef",
    "RestoreRuntimeResponseTypeDef",
    "RuntimeAliasInfoTypeDef",
    "RuntimeInfoTypeDef",
    "RuntimeReleaseLifecycleTypeDef",
    "RuntimeVersionInfoTypeDef",
    "UpdateNetworkConnectorRequestTypeDef",
    "UpdateNetworkConnectorResponseTypeDef",
    "UpdateRuntimeAliasRequestTypeDef",
    "UpdateRuntimeAliasResponseTypeDef",
    "UpdateRuntimeRequestTypeDef",
    "UpdateRuntimeResponseTypeDef",
    "UpdateRuntimeVersionRequestTypeDef",
    "UpdateRuntimeVersionResponseTypeDef",
    "WaiterConfigTypeDef",
)

class CompatibilityTypeDef(TypedDict):
    IntegrationModels: NotRequired[list[Literal["RuntimeAPI"]]]
    Architectures: NotRequired[list[RuntimeArchitectureType]]
    ManagedInstances: NotRequired[CompatibilityPolicyType]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class RuntimeReleaseLifecycleTypeDef(TypedDict):
    ReleaseState: NotRequired[RuntimeReleaseStateType]
    DeprecationDate: NotRequired[str]
    FunctionCreateBlockDate: NotRequired[str]
    FunctionUpdateBlockDate: NotRequired[str]

class CreateRuntimeVersionRequestTypeDef(TypedDict):
    RuntimeName: str
    ImageUri: str
    Name: str
    ReleaseNotes: NotRequired[str]
    DryRun: NotRequired[bool]

class PlatformTypeDef(TypedDict):
    Architecture: str
    Os: str
    Digest: str

class DeleteNetworkConnectorRequestTypeDef(TypedDict):
    Identifier: str

class DeleteRuntimeAliasRequestTypeDef(TypedDict):
    RuntimeName: str
    Name: str
    RecoveryWindowInDays: NotRequired[int]

class DeleteRuntimeRequestTypeDef(TypedDict):
    RuntimeName: str
    RecoveryWindowInDays: NotRequired[int]

class DeleteRuntimeVersionRequestTypeDef(TypedDict):
    RuntimeName: str
    Name: str
    RecoveryWindowInDays: NotRequired[int]

class GetNetworkConnectorRequestTypeDef(TypedDict):
    Identifier: str

class GetRuntimeAliasRequestTypeDef(TypedDict):
    RuntimeName: str
    Name: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetRuntimeRequestTypeDef(TypedDict):
    RuntimeName: str

class GetRuntimeVersionRequestTypeDef(TypedDict):
    RuntimeName: str
    Name: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListNetworkConnectorVersionsRequestTypeDef(TypedDict):
    Identifier: str
    State: NotRequired[NetworkConnectorStateType]
    Marker: NotRequired[str]
    MaxItems: NotRequired[int]

class NetworkConnectorVersionSummaryTypeDef(TypedDict):
    Arn: str
    VersionArn: str
    Name: str
    Id: str
    Version: int
    State: NetworkConnectorStateType
    StateReason: NotRequired[str]
    StateReasonCode: NotRequired[NetworkConnectorStateReasonCodeType]
    LastModified: NotRequired[datetime]

class ListNetworkConnectorsRequestTypeDef(TypedDict):
    State: NotRequired[NetworkConnectorStateType]
    Marker: NotRequired[str]
    MaxItems: NotRequired[int]

NetworkConnectorSummaryTypeDef = TypedDict(
    "NetworkConnectorSummaryTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Id": str,
        "Type": Literal["VPC_EGRESS"],
        "State": NotRequired[NetworkConnectorStateType],
        "LastModified": NotRequired[datetime],
        "LatestVersionArn": NotRequired[str],
        "LatestVersion": NotRequired[int],
    },
)

class ListRuntimeAliasesRequestTypeDef(TypedDict):
    RuntimeName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListRuntimeVersionsRequestTypeDef(TypedDict):
    RuntimeName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListRuntimesRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class NetworkConnectorVpcEgressConfigurationOutputTypeDef(TypedDict):
    SubnetIds: NotRequired[list[str]]
    SecurityGroupIds: NotRequired[list[str]]
    NetworkProtocol: NotRequired[NetworkProtocolType]
    AssociatedComputeResourceTypes: NotRequired[list[ComputeResourceTypeType]]

class NetworkConnectorVpcEgressConfigurationTypeDef(TypedDict):
    SubnetIds: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]
    NetworkProtocol: NotRequired[NetworkProtocolType]
    AssociatedComputeResourceTypes: NotRequired[Sequence[ComputeResourceTypeType]]

class RestoreRuntimeRequestTypeDef(TypedDict):
    RuntimeName: str
    RuntimeVersion: NotRequired[str]
    RuntimeAlias: NotRequired[str]

class UpdateRuntimeVersionRequestTypeDef(TypedDict):
    RuntimeName: str
    Name: str
    ReleaseNotes: str

class RuntimeVersionInfoTypeDef(TypedDict):
    Name: str
    Arn: str
    ResolvedUri: str
    State: RuntimeVersionStateType
    Created: str
    LastModified: str
    PendingDeletionAt: NotRequired[str]
    ReleaseNotes: NotRequired[str]
    Compatibility: NotRequired[CompatibilityTypeDef]

class RestoreRuntimeResponseTypeDef(TypedDict):
    RuntimeName: str
    RuntimeVersion: str
    RuntimeAlias: str
    Arn: str
    State: RuntimeStateType
    LastModified: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRuntimeAliasRequestTypeDef(TypedDict):
    RuntimeName: str
    RuntimeVersion: str
    Name: str
    Description: NotRequired[str]
    ReleaseLifecycle: NotRequired[RuntimeReleaseLifecycleTypeDef]

class CreateRuntimeAliasResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    RuntimeVersion: str
    RuntimeVersionArn: str
    State: RuntimeAliasStateType
    Description: str
    ReleaseLifecycle: RuntimeReleaseLifecycleTypeDef
    Created: str
    LastModified: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRuntimeRequestTypeDef(TypedDict):
    Name: str
    Tags: NotRequired[Mapping[str, str]]
    Description: NotRequired[str]
    LicenseInfo: NotRequired[str]
    ReleaseLifecycle: NotRequired[RuntimeReleaseLifecycleTypeDef]

class CreateRuntimeResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    LicenseInfo: str
    ReleaseLifecycle: RuntimeReleaseLifecycleTypeDef
    Created: str
    LastModified: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRuntimeAliasResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    RuntimeVersion: str
    RuntimeVersionArn: str
    State: RuntimeAliasStateType
    PendingDeletionAt: str
    Description: str
    Compatibility: CompatibilityTypeDef
    ReleaseLifecycle: RuntimeReleaseLifecycleTypeDef
    Created: str
    LastModified: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRuntimeResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    LicenseInfo: str
    ReleaseLifecycle: RuntimeReleaseLifecycleTypeDef
    State: RuntimeStateType
    PendingDeletionAt: str
    Created: str
    LastModified: str
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef

class RuntimeAliasInfoTypeDef(TypedDict):
    Name: str
    Arn: str
    RuntimeVersion: str
    RuntimeVersionArn: str
    State: RuntimeAliasStateType
    Created: str
    LastModified: str
    PendingDeletionAt: NotRequired[str]
    Description: NotRequired[str]
    Compatibility: NotRequired[CompatibilityTypeDef]
    ReleaseLifecycle: NotRequired[RuntimeReleaseLifecycleTypeDef]

class RuntimeInfoTypeDef(TypedDict):
    Arn: str
    Name: str
    Created: str
    LastModified: str
    Description: NotRequired[str]
    LicenseInfo: NotRequired[str]
    ReleaseLifecycle: NotRequired[RuntimeReleaseLifecycleTypeDef]
    State: NotRequired[RuntimeStateType]
    PendingDeletionAt: NotRequired[str]

class UpdateRuntimeAliasRequestTypeDef(TypedDict):
    RuntimeName: str
    Name: str
    RuntimeVersion: str
    Description: NotRequired[str]
    ReleaseLifecycle: NotRequired[RuntimeReleaseLifecycleTypeDef]

class UpdateRuntimeAliasResponseTypeDef(TypedDict):
    RuntimeName: str
    Name: str
    Arn: str
    RuntimeVersion: str
    RuntimeVersionArn: str
    State: RuntimeAliasStateType
    Description: str
    Compatibility: CompatibilityTypeDef
    ReleaseLifecycle: RuntimeReleaseLifecycleTypeDef
    Created: str
    LastModified: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRuntimeRequestTypeDef(TypedDict):
    RuntimeName: str
    Description: NotRequired[str]
    LicenseInfo: NotRequired[str]
    ReleaseLifecycle: NotRequired[RuntimeReleaseLifecycleTypeDef]

class UpdateRuntimeResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Description: str
    LicenseInfo: str
    ReleaseLifecycle: RuntimeReleaseLifecycleTypeDef
    Created: str
    LastModified: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRuntimeVersionResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    ResolvedUri: str
    State: RuntimeVersionStateType
    ReleaseNotes: str
    Platforms: list[PlatformTypeDef]
    Compatibility: CompatibilityTypeDef
    Created: str
    LastModified: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRuntimeVersionResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    ResolvedUri: str
    State: RuntimeVersionStateType
    PendingDeletionAt: str
    ReleaseNotes: str
    Platforms: list[PlatformTypeDef]
    Compatibility: CompatibilityTypeDef
    Created: str
    LastModified: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRuntimeVersionResponseTypeDef(TypedDict):
    Name: str
    Arn: str
    ResolvedUri: str
    State: RuntimeVersionStateType
    ReleaseNotes: str
    Platforms: list[PlatformTypeDef]
    Compatibility: CompatibilityTypeDef
    Created: str
    LastModified: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRuntimeAliasRequestWaitTypeDef(TypedDict):
    RuntimeName: str
    Name: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetRuntimeVersionRequestWaitTypeDef(TypedDict):
    RuntimeName: str
    Name: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class ListNetworkConnectorVersionsRequestPaginateTypeDef(TypedDict):
    Identifier: str
    State: NotRequired[NetworkConnectorStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNetworkConnectorsRequestPaginateTypeDef(TypedDict):
    State: NotRequired[NetworkConnectorStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRuntimeAliasesRequestPaginateTypeDef(TypedDict):
    RuntimeName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRuntimeVersionsRequestPaginateTypeDef(TypedDict):
    RuntimeName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRuntimesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNetworkConnectorVersionsResponseTypeDef(TypedDict):
    NetworkConnectorVersions: list[NetworkConnectorVersionSummaryTypeDef]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListNetworkConnectorsResponseTypeDef(TypedDict):
    NetworkConnectors: list[NetworkConnectorSummaryTypeDef]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef

class NetworkConnectorConfigurationOutputTypeDef(TypedDict):
    VpcEgressConfiguration: NotRequired[NetworkConnectorVpcEgressConfigurationOutputTypeDef]

class NetworkConnectorConfigurationTypeDef(TypedDict):
    VpcEgressConfiguration: NotRequired[NetworkConnectorVpcEgressConfigurationTypeDef]

class ListRuntimeVersionsResponseTypeDef(TypedDict):
    Items: list[RuntimeVersionInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRuntimeAliasesResponseTypeDef(TypedDict):
    Items: list[RuntimeAliasInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRuntimesResponseTypeDef(TypedDict):
    Items: list[RuntimeInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateNetworkConnectorResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Id: str
    VersionArn: str
    Version: int
    Configuration: NetworkConnectorConfigurationOutputTypeDef
    OperatorRole: str
    State: NetworkConnectorStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteNetworkConnectorResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Id: str
    VersionArn: str
    Version: int
    Configuration: NetworkConnectorConfigurationOutputTypeDef
    OperatorRole: str
    State: NetworkConnectorStateType
    ResponseMetadata: ResponseMetadataTypeDef

class GetNetworkConnectorResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Id: str
    VersionArn: str
    Version: int
    LatestVersionArn: str
    LatestVersion: int
    Configuration: NetworkConnectorConfigurationOutputTypeDef
    OperatorRole: str
    State: NetworkConnectorStateType
    StateReason: str
    StateReasonCode: NetworkConnectorStateReasonCodeType
    LastUpdateStatus: NetworkConnectorLastUpdateStatusType
    LastUpdateStatusReason: str
    LastUpdateStatusReasonCode: NetworkConnectorLastUpdateStatusReasonCodeType
    LastModified: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateNetworkConnectorResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Id: str
    VersionArn: str
    Version: int
    OperatorRole: str
    Configuration: NetworkConnectorConfigurationOutputTypeDef
    State: NetworkConnectorStateType
    LastUpdateStatus: NetworkConnectorLastUpdateStatusType
    LastUpdateStatusReason: str
    LastModified: datetime
    ResponseMetadata: ResponseMetadataTypeDef

NetworkConnectorConfigurationUnionTypeDef = Union[
    NetworkConnectorConfigurationTypeDef, NetworkConnectorConfigurationOutputTypeDef
]

class CreateNetworkConnectorRequestTypeDef(TypedDict):
    Name: str
    Configuration: NetworkConnectorConfigurationUnionTypeDef
    OperatorRole: NotRequired[str]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class UpdateNetworkConnectorRequestTypeDef(TypedDict):
    Identifier: str
    Configuration: NotRequired[NetworkConnectorConfigurationUnionTypeDef]
    OperatorRole: NotRequired[str]
    ClientToken: NotRequired[str]
