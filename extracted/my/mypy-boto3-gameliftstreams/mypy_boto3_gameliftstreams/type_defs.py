"""
Type annotations for gameliftstreams service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gameliftstreams/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_gameliftstreams.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime

from .literals import (
    ApplicationStatusReasonType,
    ApplicationStatusType,
    ExportFilesStatusType,
    ReplicationStatusTypeType,
    RevocationModeType,
    RuntimeEnvironmentTypeType,
    ShaderCacheStatusType,
    StreamClassType,
    StreamGroupLocationStatusType,
    StreamGroupStatusReasonType,
    StreamGroupStatusType,
    StreamSessionStatusReasonType,
    StreamSessionStatusType,
    StreamUrlStatusReasonType,
    StreamUrlStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AddStreamGroupLocationsInputTypeDef",
    "AddStreamGroupLocationsOutputTypeDef",
    "ApplicationSummaryTypeDef",
    "AssociateApplicationsInputTypeDef",
    "AssociateApplicationsOutputTypeDef",
    "CreateApplicationInputTypeDef",
    "CreateApplicationOutputTypeDef",
    "CreateStreamGroupInputTypeDef",
    "CreateStreamGroupOutputTypeDef",
    "CreateStreamSessionAdminShellInputTypeDef",
    "CreateStreamSessionAdminShellOutputTypeDef",
    "CreateStreamSessionConnectionInputTypeDef",
    "CreateStreamSessionConnectionOutputTypeDef",
    "CreateStreamUrlInputTypeDef",
    "CreateStreamUrlOutputTypeDef",
    "DefaultApplicationTypeDef",
    "DeleteApplicationInputTypeDef",
    "DeleteStreamGroupInputTypeDef",
    "DisassociateApplicationsInputTypeDef",
    "DisassociateApplicationsOutputTypeDef",
    "DisplayConfigurationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportFilesMetadataTypeDef",
    "ExportStreamSessionFilesInputTypeDef",
    "GetApplicationInputTypeDef",
    "GetApplicationInputWaitExtraTypeDef",
    "GetApplicationInputWaitTypeDef",
    "GetApplicationOutputTypeDef",
    "GetStreamGroupInputTypeDef",
    "GetStreamGroupInputWaitExtraTypeDef",
    "GetStreamGroupInputWaitTypeDef",
    "GetStreamGroupOutputTypeDef",
    "GetStreamSessionInputTypeDef",
    "GetStreamSessionInputWaitTypeDef",
    "GetStreamSessionOutputTypeDef",
    "GetStreamUrlInputTypeDef",
    "GetStreamUrlOutputTypeDef",
    "ListApplicationShaderCachesInputTypeDef",
    "ListApplicationShaderCachesOutputTypeDef",
    "ListApplicationsInputPaginateTypeDef",
    "ListApplicationsInputTypeDef",
    "ListApplicationsOutputTypeDef",
    "ListStreamGroupsInputPaginateTypeDef",
    "ListStreamGroupsInputTypeDef",
    "ListStreamGroupsOutputTypeDef",
    "ListStreamSessionsByAccountInputPaginateTypeDef",
    "ListStreamSessionsByAccountInputTypeDef",
    "ListStreamSessionsByAccountOutputTypeDef",
    "ListStreamSessionsInputPaginateTypeDef",
    "ListStreamSessionsInputTypeDef",
    "ListStreamSessionsOutputTypeDef",
    "ListStreamUrlsInputPaginateTypeDef",
    "ListStreamUrlsInputTypeDef",
    "ListStreamUrlsOutputTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LocationConfigurationTypeDef",
    "LocationStateTypeDef",
    "PaginatorConfigTypeDef",
    "PerformanceStatsConfigurationTypeDef",
    "RemoveStreamGroupLocationsInputTypeDef",
    "ReplicationStatusTypeDef",
    "ResolutionTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeStreamUrlInputTypeDef",
    "RuntimeEnvironmentTypeDef",
    "ShaderCacheSummaryTypeDef",
    "StartStreamSessionInputTypeDef",
    "StartStreamSessionOutputTypeDef",
    "StreamGroupSummaryTypeDef",
    "StreamSessionSummaryTypeDef",
    "StreamUrlSummaryTypeDef",
    "TagResourceRequestTypeDef",
    "TerminateStreamSessionInputTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateApplicationInputTypeDef",
    "UpdateApplicationOutputTypeDef",
    "UpdateStreamGroupInputTypeDef",
    "UpdateStreamGroupOutputTypeDef",
    "VpcTransitConfigurationResponseTypeDef",
    "VpcTransitConfigurationTypeDef",
    "WaiterConfigTypeDef",
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


RuntimeEnvironmentTypeDef = TypedDict(
    "RuntimeEnvironmentTypeDef",
    {
        "Type": RuntimeEnvironmentTypeType,
        "Version": str,
    },
)


class AssociateApplicationsInputTypeDef(TypedDict):
    Identifier: str
    ApplicationIdentifiers: Sequence[str]


class ReplicationStatusTypeDef(TypedDict):
    Location: NotRequired[str]
    Status: NotRequired[ReplicationStatusTypeType]


class DefaultApplicationTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]


class CreateStreamSessionAdminShellInputTypeDef(TypedDict):
    Identifier: str
    StreamSessionIdentifier: str


class CreateStreamSessionConnectionInputTypeDef(TypedDict):
    Identifier: str
    StreamSessionIdentifier: str
    SignalRequest: str
    ClientToken: NotRequired[str]


class DeleteApplicationInputTypeDef(TypedDict):
    Identifier: str


class DeleteStreamGroupInputTypeDef(TypedDict):
    Identifier: str


class DisassociateApplicationsInputTypeDef(TypedDict):
    Identifier: str
    ApplicationIdentifiers: Sequence[str]


class ResolutionTypeDef(TypedDict):
    Width: int
    Height: int


class ExportFilesMetadataTypeDef(TypedDict):
    Status: NotRequired[ExportFilesStatusType]
    StatusReason: NotRequired[str]
    OutputUri: NotRequired[str]


class ExportStreamSessionFilesInputTypeDef(TypedDict):
    Identifier: str
    StreamSessionIdentifier: str
    OutputUri: str


class GetApplicationInputTypeDef(TypedDict):
    Identifier: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class GetStreamGroupInputTypeDef(TypedDict):
    Identifier: str


class GetStreamSessionInputTypeDef(TypedDict):
    Identifier: str
    StreamSessionIdentifier: str


class PerformanceStatsConfigurationTypeDef(TypedDict):
    SharedWithClient: NotRequired[bool]


class GetStreamUrlInputTypeDef(TypedDict):
    Identifier: str
    StreamUrlIdentifier: str


class ListApplicationShaderCachesInputTypeDef(TypedDict):
    Identifier: str


class ShaderCacheSummaryTypeDef(TypedDict):
    Identifier: str
    ApplicationArn: str
    Status: NotRequired[ShaderCacheStatusType]
    LastUpdatedAt: NotRequired[datetime]
    StorageBytes: NotRequired[int]
    AssociatedStreamGroups: NotRequired[list[str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListApplicationsInputTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListStreamGroupsInputTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListStreamSessionsByAccountInputTypeDef(TypedDict):
    Status: NotRequired[StreamSessionStatusType]
    ExportFilesStatus: NotRequired[ExportFilesStatusType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListStreamSessionsInputTypeDef(TypedDict):
    Identifier: str
    Status: NotRequired[StreamSessionStatusType]
    ExportFilesStatus: NotRequired[ExportFilesStatusType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListStreamUrlsInputTypeDef(TypedDict):
    Status: NotRequired[StreamUrlStatusType]
    StreamGroupIdentifier: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class StreamUrlSummaryTypeDef(TypedDict):
    Arn: str
    StreamUrlId: NotRequired[str]
    StreamUrl: NotRequired[str]
    Status: NotRequired[StreamUrlStatusType]
    StatusReason: NotRequired[StreamUrlStatusReasonType]
    ExpiresAt: NotRequired[datetime]
    CreatedAt: NotRequired[datetime]
    UsageLimit: NotRequired[int]
    RemainingUses: NotRequired[int]
    StreamGroupArn: NotRequired[str]
    ApplicationArn: NotRequired[str]
    SessionLengthSeconds: NotRequired[int]
    Description: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str


class VpcTransitConfigurationTypeDef(TypedDict):
    VpcId: str
    Ipv4CidrBlocks: Sequence[str]


class VpcTransitConfigurationResponseTypeDef(TypedDict):
    VpcId: NotRequired[str]
    Ipv4CidrBlocks: NotRequired[list[str]]
    TransitGatewayId: NotRequired[str]
    TransitGatewayResourceShareArn: NotRequired[str]


class RemoveStreamGroupLocationsInputTypeDef(TypedDict):
    Identifier: str
    Locations: Sequence[str]


class RevokeStreamUrlInputTypeDef(TypedDict):
    Identifier: str
    StreamUrlIdentifier: str
    RevocationMode: NotRequired[RevocationModeType]


class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class TerminateStreamSessionInputTypeDef(TypedDict):
    Identifier: str
    StreamSessionIdentifier: str


class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateApplicationInputTypeDef(TypedDict):
    Identifier: str
    Description: NotRequired[str]
    ApplicationLogPaths: NotRequired[Sequence[str]]
    ApplicationLogOutputUri: NotRequired[str]


class AssociateApplicationsOutputTypeDef(TypedDict):
    Arn: str
    ApplicationArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStreamSessionAdminShellOutputTypeDef(TypedDict):
    SessionId: str
    StreamUrl: str
    TokenValue: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStreamSessionConnectionOutputTypeDef(TypedDict):
    SignalResponse: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateApplicationsOutputTypeDef(TypedDict):
    Arn: str
    ApplicationArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ApplicationSummaryTypeDef(TypedDict):
    Arn: str
    Id: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[ApplicationStatusType]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    RuntimeEnvironment: NotRequired[RuntimeEnvironmentTypeDef]


class CreateApplicationInputTypeDef(TypedDict):
    Description: str
    RuntimeEnvironment: RuntimeEnvironmentTypeDef
    ExecutablePath: str
    ApplicationSourceUri: str
    ApplicationLogPaths: NotRequired[Sequence[str]]
    ApplicationLogOutputUri: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]


class CreateApplicationOutputTypeDef(TypedDict):
    Arn: str
    Description: str
    RuntimeEnvironment: RuntimeEnvironmentTypeDef
    ExecutablePath: str
    ApplicationLogPaths: list[str]
    ApplicationLogOutputUri: str
    ApplicationSourceUri: str
    Id: str
    Status: ApplicationStatusType
    StatusReason: ApplicationStatusReasonType
    ReplicationStatuses: list[ReplicationStatusTypeDef]
    CreatedAt: datetime
    LastUpdatedAt: datetime
    AssociatedStreamGroups: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetApplicationOutputTypeDef(TypedDict):
    Arn: str
    Description: str
    RuntimeEnvironment: RuntimeEnvironmentTypeDef
    ExecutablePath: str
    ApplicationLogPaths: list[str]
    ApplicationLogOutputUri: str
    ApplicationSourceUri: str
    Id: str
    Status: ApplicationStatusType
    StatusReason: ApplicationStatusReasonType
    ReplicationStatuses: list[ReplicationStatusTypeDef]
    CreatedAt: datetime
    LastUpdatedAt: datetime
    AssociatedStreamGroups: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApplicationOutputTypeDef(TypedDict):
    Arn: str
    Description: str
    RuntimeEnvironment: RuntimeEnvironmentTypeDef
    ExecutablePath: str
    ApplicationLogPaths: list[str]
    ApplicationLogOutputUri: str
    ApplicationSourceUri: str
    Id: str
    Status: ApplicationStatusType
    StatusReason: ApplicationStatusReasonType
    ReplicationStatuses: list[ReplicationStatusTypeDef]
    CreatedAt: datetime
    LastUpdatedAt: datetime
    AssociatedStreamGroups: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class StreamGroupSummaryTypeDef(TypedDict):
    Arn: str
    Id: NotRequired[str]
    Description: NotRequired[str]
    DefaultApplication: NotRequired[DefaultApplicationTypeDef]
    StreamClass: NotRequired[StreamClassType]
    Status: NotRequired[StreamGroupStatusType]
    CreatedAt: NotRequired[datetime]
    LastUpdatedAt: NotRequired[datetime]
    ExpiresAt: NotRequired[datetime]


class DisplayConfigurationTypeDef(TypedDict):
    Resolution: NotRequired[ResolutionTypeDef]


StreamSessionSummaryTypeDef = TypedDict(
    "StreamSessionSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "UserId": NotRequired[str],
        "Status": NotRequired[StreamSessionStatusType],
        "StatusReason": NotRequired[StreamSessionStatusReasonType],
        "Protocol": NotRequired[Literal["WebRTC"]],
        "LastUpdatedAt": NotRequired[datetime],
        "CreatedAt": NotRequired[datetime],
        "ApplicationArn": NotRequired[str],
        "ExportFilesMetadata": NotRequired[ExportFilesMetadataTypeDef],
        "Location": NotRequired[str],
        "RoleArn": NotRequired[str],
    },
)


class GetApplicationInputWaitExtraTypeDef(TypedDict):
    Identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetApplicationInputWaitTypeDef(TypedDict):
    Identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetStreamGroupInputWaitExtraTypeDef(TypedDict):
    Identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetStreamGroupInputWaitTypeDef(TypedDict):
    Identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetStreamSessionInputWaitTypeDef(TypedDict):
    Identifier: str
    StreamSessionIdentifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class ListApplicationShaderCachesOutputTypeDef(TypedDict):
    Items: list[ShaderCacheSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListApplicationsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamGroupsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamSessionsByAccountInputPaginateTypeDef(TypedDict):
    Status: NotRequired[StreamSessionStatusType]
    ExportFilesStatus: NotRequired[ExportFilesStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamSessionsInputPaginateTypeDef(TypedDict):
    Identifier: str
    Status: NotRequired[StreamSessionStatusType]
    ExportFilesStatus: NotRequired[ExportFilesStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamUrlsInputPaginateTypeDef(TypedDict):
    Status: NotRequired[StreamUrlStatusType]
    StreamGroupIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamUrlsOutputTypeDef(TypedDict):
    Items: list[StreamUrlSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LocationConfigurationTypeDef(TypedDict):
    LocationName: str
    AlwaysOnCapacity: NotRequired[int]
    OnDemandCapacity: NotRequired[int]
    TargetIdleCapacity: NotRequired[int]
    MaximumCapacity: NotRequired[int]
    VpcTransitConfiguration: NotRequired[VpcTransitConfigurationTypeDef]


class LocationStateTypeDef(TypedDict):
    LocationName: NotRequired[str]
    Status: NotRequired[StreamGroupLocationStatusType]
    AlwaysOnCapacity: NotRequired[int]
    OnDemandCapacity: NotRequired[int]
    TargetIdleCapacity: NotRequired[int]
    MaximumCapacity: NotRequired[int]
    RequestedCapacity: NotRequired[int]
    AllocatedCapacity: NotRequired[int]
    IdleCapacity: NotRequired[int]
    InternalVpcIpv4CidrBlock: NotRequired[str]
    VpcTransitConfiguration: NotRequired[VpcTransitConfigurationResponseTypeDef]


class ListApplicationsOutputTypeDef(TypedDict):
    Items: list[ApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListStreamGroupsOutputTypeDef(TypedDict):
    Items: list[StreamGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


CreateStreamUrlInputTypeDef = TypedDict(
    "CreateStreamUrlInputTypeDef",
    {
        "Identifier": str,
        "ApplicationIdentifier": str,
        "Protocol": Literal["WebRTC"],
        "UrlExpiresAfterMinutes": int,
        "Locations": Sequence[str],
        "UsageLimit": NotRequired[int],
        "Description": NotRequired[str],
        "SessionLengthSeconds": NotRequired[int],
        "AdditionalLaunchArgs": NotRequired[Sequence[str]],
        "AdditionalEnvironmentVariables": NotRequired[Mapping[str, str]],
        "RoleArn": NotRequired[str],
        "DisplayConfiguration": NotRequired[DisplayConfigurationTypeDef],
        "ClientToken": NotRequired[str],
    },
)
CreateStreamUrlOutputTypeDef = TypedDict(
    "CreateStreamUrlOutputTypeDef",
    {
        "Arn": str,
        "StreamUrlId": str,
        "StreamUrl": str,
        "Status": StreamUrlStatusType,
        "StatusReason": StreamUrlStatusReasonType,
        "ExpiresAt": datetime,
        "CreatedAt": datetime,
        "UsageLimit": int,
        "RemainingUses": int,
        "StreamGroupArn": str,
        "ApplicationArn": str,
        "Protocol": Literal["WebRTC"],
        "Locations": list[str],
        "SessionLengthSeconds": int,
        "Description": str,
        "AdditionalLaunchArgs": list[str],
        "AdditionalEnvironmentVariables": dict[str, str],
        "RoleArn": str,
        "DisplayConfiguration": DisplayConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStreamSessionOutputTypeDef = TypedDict(
    "GetStreamSessionOutputTypeDef",
    {
        "Arn": str,
        "Description": str,
        "StreamGroupId": str,
        "UserId": str,
        "Status": StreamSessionStatusType,
        "StatusReason": StreamSessionStatusReasonType,
        "Protocol": Literal["WebRTC"],
        "Location": str,
        "SignalRequest": str,
        "SignalResponse": str,
        "ConnectionTimeoutSeconds": int,
        "SessionLengthSeconds": int,
        "AdditionalLaunchArgs": list[str],
        "AdditionalEnvironmentVariables": dict[str, str],
        "PerformanceStatsConfiguration": PerformanceStatsConfigurationTypeDef,
        "LogFileLocationUri": str,
        "WebSdkProtocolUrl": str,
        "LastUpdatedAt": datetime,
        "CreatedAt": datetime,
        "ApplicationArn": str,
        "ExportFilesMetadata": ExportFilesMetadataTypeDef,
        "RoleArn": str,
        "DisplayConfiguration": DisplayConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartStreamSessionInputTypeDef = TypedDict(
    "StartStreamSessionInputTypeDef",
    {
        "Identifier": str,
        "Protocol": Literal["WebRTC"],
        "SignalRequest": str,
        "ApplicationIdentifier": str,
        "ClientToken": NotRequired[str],
        "Description": NotRequired[str],
        "UserId": NotRequired[str],
        "Locations": NotRequired[Sequence[str]],
        "ConnectionTimeoutSeconds": NotRequired[int],
        "SessionLengthSeconds": NotRequired[int],
        "AdditionalLaunchArgs": NotRequired[Sequence[str]],
        "AdditionalEnvironmentVariables": NotRequired[Mapping[str, str]],
        "PerformanceStatsConfiguration": NotRequired[PerformanceStatsConfigurationTypeDef],
        "RoleArn": NotRequired[str],
        "DisplayConfiguration": NotRequired[DisplayConfigurationTypeDef],
    },
)
StartStreamSessionOutputTypeDef = TypedDict(
    "StartStreamSessionOutputTypeDef",
    {
        "Arn": str,
        "Description": str,
        "StreamGroupId": str,
        "UserId": str,
        "Status": StreamSessionStatusType,
        "StatusReason": StreamSessionStatusReasonType,
        "Protocol": Literal["WebRTC"],
        "Location": str,
        "SignalRequest": str,
        "SignalResponse": str,
        "ConnectionTimeoutSeconds": int,
        "SessionLengthSeconds": int,
        "AdditionalLaunchArgs": list[str],
        "AdditionalEnvironmentVariables": dict[str, str],
        "PerformanceStatsConfiguration": PerformanceStatsConfigurationTypeDef,
        "LogFileLocationUri": str,
        "WebSdkProtocolUrl": str,
        "LastUpdatedAt": datetime,
        "CreatedAt": datetime,
        "ApplicationArn": str,
        "ExportFilesMetadata": ExportFilesMetadataTypeDef,
        "RoleArn": str,
        "DisplayConfiguration": DisplayConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStreamUrlOutputTypeDef = TypedDict(
    "GetStreamUrlOutputTypeDef",
    {
        "Arn": str,
        "StreamUrlId": str,
        "StreamUrl": str,
        "Status": StreamUrlStatusType,
        "StatusReason": StreamUrlStatusReasonType,
        "ExpiresAt": datetime,
        "CreatedAt": datetime,
        "UsageLimit": int,
        "RemainingUses": int,
        "StreamGroupArn": str,
        "ApplicationArn": str,
        "Protocol": Literal["WebRTC"],
        "Locations": list[str],
        "SessionLengthSeconds": int,
        "Description": str,
        "AdditionalLaunchArgs": list[str],
        "AdditionalEnvironmentVariables": dict[str, str],
        "RoleArn": str,
        "DisplayConfiguration": DisplayConfigurationTypeDef,
        "StreamSessions": list[StreamSessionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListStreamSessionsByAccountOutputTypeDef(TypedDict):
    Items: list[StreamSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListStreamSessionsOutputTypeDef(TypedDict):
    Items: list[StreamSessionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AddStreamGroupLocationsInputTypeDef(TypedDict):
    Identifier: str
    LocationConfigurations: Sequence[LocationConfigurationTypeDef]


class CreateStreamGroupInputTypeDef(TypedDict):
    Description: str
    StreamClass: StreamClassType
    DefaultApplicationIdentifier: NotRequired[str]
    LocationConfigurations: NotRequired[Sequence[LocationConfigurationTypeDef]]
    Tags: NotRequired[Mapping[str, str]]
    ClientToken: NotRequired[str]


class UpdateStreamGroupInputTypeDef(TypedDict):
    Identifier: str
    LocationConfigurations: NotRequired[Sequence[LocationConfigurationTypeDef]]
    Description: NotRequired[str]
    DefaultApplicationIdentifier: NotRequired[str]


class AddStreamGroupLocationsOutputTypeDef(TypedDict):
    Identifier: str
    Locations: list[LocationStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStreamGroupOutputTypeDef(TypedDict):
    Arn: str
    Description: str
    DefaultApplication: DefaultApplicationTypeDef
    LocationStates: list[LocationStateTypeDef]
    StreamClass: StreamClassType
    Id: str
    Status: StreamGroupStatusType
    StatusReason: StreamGroupStatusReasonType
    LastUpdatedAt: datetime
    CreatedAt: datetime
    ExpiresAt: datetime
    AssociatedApplications: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetStreamGroupOutputTypeDef(TypedDict):
    Arn: str
    Description: str
    DefaultApplication: DefaultApplicationTypeDef
    LocationStates: list[LocationStateTypeDef]
    StreamClass: StreamClassType
    Id: str
    Status: StreamGroupStatusType
    StatusReason: StreamGroupStatusReasonType
    LastUpdatedAt: datetime
    CreatedAt: datetime
    ExpiresAt: datetime
    AssociatedApplications: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateStreamGroupOutputTypeDef(TypedDict):
    Arn: str
    Description: str
    DefaultApplication: DefaultApplicationTypeDef
    LocationStates: list[LocationStateTypeDef]
    StreamClass: StreamClassType
    Id: str
    Status: StreamGroupStatusType
    StatusReason: StreamGroupStatusReasonType
    LastUpdatedAt: datetime
    CreatedAt: datetime
    ExpiresAt: datetime
    AssociatedApplications: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
