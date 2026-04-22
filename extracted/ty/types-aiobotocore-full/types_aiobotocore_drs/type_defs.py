"""
Type annotations for drs service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_drs/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_drs.type_defs import AccountTypeDef

    data: AccountTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime

from .literals import (
    DataReplicationErrorStringType,
    DataReplicationInitiationStepNameType,
    DataReplicationInitiationStepStatusType,
    DataReplicationStateType,
    EC2InstanceStateType,
    ExtensionStatusType,
    FailbackLaunchTypeType,
    FailbackReplicationErrorType,
    FailbackStateType,
    InitiatedByType,
    InternetProtocolType,
    JobLogEventType,
    JobStatusType,
    JobTypeType,
    LastLaunchResultType,
    LastLaunchTypeType,
    LaunchActionCategoryType,
    LaunchActionParameterTypeType,
    LaunchActionRunStatusType,
    LaunchActionTypeType,
    LaunchDispositionType,
    LaunchStatusType,
    OriginEnvironmentType,
    PITPolicyRuleUnitsType,
    ProductCodeModeType,
    RecoveryInstanceDataReplicationInitiationStepNameType,
    RecoveryInstanceDataReplicationInitiationStepStatusType,
    RecoveryInstanceDataReplicationStateType,
    RecoveryResultType,
    RecoverySnapshotsOrderType,
    ReplicationConfigurationDataPlaneRoutingType,
    ReplicationConfigurationDefaultLargeStagingDiskTypeType,
    ReplicationConfigurationEbsEncryptionType,
    ReplicationConfigurationReplicatedDiskStagingDiskTypeType,
    ReplicationDirectionType,
    ReplicationStatusType,
    TargetInstanceTypeRightSizingMethodType,
    VolumeStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccountTypeDef",
    "AssociateSourceNetworkStackRequestTypeDef",
    "AssociateSourceNetworkStackResponseTypeDef",
    "CPUTypeDef",
    "ConversionPropertiesTypeDef",
    "CreateExtendedSourceServerRequestTypeDef",
    "CreateExtendedSourceServerResponseTypeDef",
    "CreateLaunchConfigurationTemplateRequestTypeDef",
    "CreateLaunchConfigurationTemplateResponseTypeDef",
    "CreateReplicationConfigurationTemplateRequestTypeDef",
    "CreateSourceNetworkRequestTypeDef",
    "CreateSourceNetworkResponseTypeDef",
    "DataReplicationErrorTypeDef",
    "DataReplicationInfoReplicatedDiskTypeDef",
    "DataReplicationInfoTypeDef",
    "DataReplicationInitiationStepTypeDef",
    "DataReplicationInitiationTypeDef",
    "DeleteJobRequestTypeDef",
    "DeleteLaunchActionRequestTypeDef",
    "DeleteLaunchConfigurationTemplateRequestTypeDef",
    "DeleteRecoveryInstanceRequestTypeDef",
    "DeleteReplicationConfigurationTemplateRequestTypeDef",
    "DeleteSourceNetworkRequestTypeDef",
    "DeleteSourceServerRequestTypeDef",
    "DescribeJobLogItemsRequestPaginateTypeDef",
    "DescribeJobLogItemsRequestTypeDef",
    "DescribeJobLogItemsResponseTypeDef",
    "DescribeJobsRequestFiltersTypeDef",
    "DescribeJobsRequestPaginateTypeDef",
    "DescribeJobsRequestTypeDef",
    "DescribeJobsResponseTypeDef",
    "DescribeLaunchConfigurationTemplatesRequestPaginateTypeDef",
    "DescribeLaunchConfigurationTemplatesRequestTypeDef",
    "DescribeLaunchConfigurationTemplatesResponseTypeDef",
    "DescribeRecoveryInstancesRequestFiltersTypeDef",
    "DescribeRecoveryInstancesRequestPaginateTypeDef",
    "DescribeRecoveryInstancesRequestTypeDef",
    "DescribeRecoveryInstancesResponseTypeDef",
    "DescribeRecoverySnapshotsRequestFiltersTypeDef",
    "DescribeRecoverySnapshotsRequestPaginateTypeDef",
    "DescribeRecoverySnapshotsRequestTypeDef",
    "DescribeRecoverySnapshotsResponseTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestPaginateTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestTypeDef",
    "DescribeReplicationConfigurationTemplatesResponseTypeDef",
    "DescribeSourceNetworksRequestFiltersTypeDef",
    "DescribeSourceNetworksRequestPaginateTypeDef",
    "DescribeSourceNetworksRequestTypeDef",
    "DescribeSourceNetworksResponseTypeDef",
    "DescribeSourceServersRequestFiltersTypeDef",
    "DescribeSourceServersRequestPaginateTypeDef",
    "DescribeSourceServersRequestTypeDef",
    "DescribeSourceServersResponseTypeDef",
    "DisconnectRecoveryInstanceRequestTypeDef",
    "DisconnectSourceServerRequestTypeDef",
    "DiskTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventResourceDataTypeDef",
    "ExportSourceNetworkCfnTemplateRequestTypeDef",
    "ExportSourceNetworkCfnTemplateResponseTypeDef",
    "GetFailbackReplicationConfigurationRequestTypeDef",
    "GetFailbackReplicationConfigurationResponseTypeDef",
    "GetLaunchConfigurationRequestTypeDef",
    "GetReplicationConfigurationRequestTypeDef",
    "IdentificationHintsTypeDef",
    "JobLogEventDataTypeDef",
    "JobLogTypeDef",
    "JobTypeDef",
    "LaunchActionParameterTypeDef",
    "LaunchActionRunTypeDef",
    "LaunchActionTypeDef",
    "LaunchActionsRequestFiltersTypeDef",
    "LaunchActionsStatusTypeDef",
    "LaunchConfigurationTemplateTypeDef",
    "LaunchConfigurationTypeDef",
    "LaunchIntoInstancePropertiesTypeDef",
    "LicensingTypeDef",
    "LifeCycleLastLaunchInitiatedTypeDef",
    "LifeCycleLastLaunchTypeDef",
    "LifeCycleTypeDef",
    "ListExtensibleSourceServersRequestPaginateTypeDef",
    "ListExtensibleSourceServersRequestTypeDef",
    "ListExtensibleSourceServersResponseTypeDef",
    "ListLaunchActionsRequestPaginateTypeDef",
    "ListLaunchActionsRequestTypeDef",
    "ListLaunchActionsResponseTypeDef",
    "ListStagingAccountsRequestPaginateTypeDef",
    "ListStagingAccountsRequestTypeDef",
    "ListStagingAccountsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NetworkInterfaceTypeDef",
    "OSTypeDef",
    "PITPolicyRuleTypeDef",
    "PaginatorConfigTypeDef",
    "ParticipatingResourceIDTypeDef",
    "ParticipatingResourceTypeDef",
    "ParticipatingServerTypeDef",
    "ProductCodeTypeDef",
    "PutLaunchActionRequestTypeDef",
    "PutLaunchActionResponseTypeDef",
    "RecoveryInstanceDataReplicationErrorTypeDef",
    "RecoveryInstanceDataReplicationInfoReplicatedDiskTypeDef",
    "RecoveryInstanceDataReplicationInfoTypeDef",
    "RecoveryInstanceDataReplicationInitiationStepTypeDef",
    "RecoveryInstanceDataReplicationInitiationTypeDef",
    "RecoveryInstanceDiskTypeDef",
    "RecoveryInstanceFailbackTypeDef",
    "RecoveryInstancePropertiesTypeDef",
    "RecoveryInstanceTypeDef",
    "RecoveryLifeCycleTypeDef",
    "RecoverySnapshotTypeDef",
    "ReplicationConfigurationReplicatedDiskTypeDef",
    "ReplicationConfigurationTemplateResponseTypeDef",
    "ReplicationConfigurationTemplateTypeDef",
    "ReplicationConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "RetryDataReplicationRequestTypeDef",
    "ReverseReplicationRequestTypeDef",
    "ReverseReplicationResponseTypeDef",
    "SourceCloudPropertiesTypeDef",
    "SourceNetworkDataTypeDef",
    "SourceNetworkTypeDef",
    "SourcePropertiesTypeDef",
    "SourceServerResponseTypeDef",
    "SourceServerTypeDef",
    "StagingAreaTypeDef",
    "StagingSourceServerTypeDef",
    "StartFailbackLaunchRequestTypeDef",
    "StartFailbackLaunchResponseTypeDef",
    "StartRecoveryRequestSourceServerTypeDef",
    "StartRecoveryRequestTypeDef",
    "StartRecoveryResponseTypeDef",
    "StartReplicationRequestTypeDef",
    "StartReplicationResponseTypeDef",
    "StartSourceNetworkRecoveryRequestNetworkEntryTypeDef",
    "StartSourceNetworkRecoveryRequestTypeDef",
    "StartSourceNetworkRecoveryResponseTypeDef",
    "StartSourceNetworkReplicationRequestTypeDef",
    "StartSourceNetworkReplicationResponseTypeDef",
    "StopFailbackRequestTypeDef",
    "StopReplicationRequestTypeDef",
    "StopReplicationResponseTypeDef",
    "StopSourceNetworkReplicationRequestTypeDef",
    "StopSourceNetworkReplicationResponseTypeDef",
    "TagResourceRequestTypeDef",
    "TerminateRecoveryInstancesRequestTypeDef",
    "TerminateRecoveryInstancesResponseTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateFailbackReplicationConfigurationRequestTypeDef",
    "UpdateLaunchConfigurationRequestTypeDef",
    "UpdateLaunchConfigurationTemplateRequestTypeDef",
    "UpdateLaunchConfigurationTemplateResponseTypeDef",
    "UpdateReplicationConfigurationRequestTypeDef",
    "UpdateReplicationConfigurationTemplateRequestTypeDef",
)


class AccountTypeDef(TypedDict):
    accountID: NotRequired[str]


class AssociateSourceNetworkStackRequestTypeDef(TypedDict):
    sourceNetworkID: str
    cfnStackName: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CPUTypeDef(TypedDict):
    cores: NotRequired[int]
    modelName: NotRequired[str]


class ProductCodeTypeDef(TypedDict):
    productCodeId: NotRequired[str]
    productCodeMode: NotRequired[ProductCodeModeType]


class CreateExtendedSourceServerRequestTypeDef(TypedDict):
    sourceServerArn: str
    tags: NotRequired[Mapping[str, str]]


class LicensingTypeDef(TypedDict):
    osByol: NotRequired[bool]


class PITPolicyRuleTypeDef(TypedDict):
    units: PITPolicyRuleUnitsType
    interval: int
    retentionDuration: int
    ruleID: NotRequired[int]
    enabled: NotRequired[bool]


class CreateSourceNetworkRequestTypeDef(TypedDict):
    vpcID: str
    originAccountID: str
    originRegion: str
    tags: NotRequired[Mapping[str, str]]


class DataReplicationErrorTypeDef(TypedDict):
    error: NotRequired[DataReplicationErrorStringType]
    rawError: NotRequired[str]


class DataReplicationInfoReplicatedDiskTypeDef(TypedDict):
    deviceName: NotRequired[str]
    totalStorageBytes: NotRequired[int]
    replicatedStorageBytes: NotRequired[int]
    rescannedStorageBytes: NotRequired[int]
    backloggedStorageBytes: NotRequired[int]
    volumeStatus: NotRequired[VolumeStatusType]


class DataReplicationInitiationStepTypeDef(TypedDict):
    name: NotRequired[DataReplicationInitiationStepNameType]
    status: NotRequired[DataReplicationInitiationStepStatusType]


class DeleteJobRequestTypeDef(TypedDict):
    jobID: str


class DeleteLaunchActionRequestTypeDef(TypedDict):
    resourceId: str
    actionId: str


class DeleteLaunchConfigurationTemplateRequestTypeDef(TypedDict):
    launchConfigurationTemplateID: str


class DeleteRecoveryInstanceRequestTypeDef(TypedDict):
    recoveryInstanceID: str


class DeleteReplicationConfigurationTemplateRequestTypeDef(TypedDict):
    replicationConfigurationTemplateID: str


class DeleteSourceNetworkRequestTypeDef(TypedDict):
    sourceNetworkID: str


class DeleteSourceServerRequestTypeDef(TypedDict):
    sourceServerID: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeJobLogItemsRequestTypeDef(TypedDict):
    jobID: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeJobsRequestFiltersTypeDef(TypedDict):
    jobIDs: NotRequired[Sequence[str]]
    fromDate: NotRequired[str]
    toDate: NotRequired[str]


class DescribeLaunchConfigurationTemplatesRequestTypeDef(TypedDict):
    launchConfigurationTemplateIDs: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeRecoveryInstancesRequestFiltersTypeDef(TypedDict):
    recoveryInstanceIDs: NotRequired[Sequence[str]]
    sourceServerIDs: NotRequired[Sequence[str]]


class DescribeRecoverySnapshotsRequestFiltersTypeDef(TypedDict):
    fromDateTime: NotRequired[str]
    toDateTime: NotRequired[str]


class RecoverySnapshotTypeDef(TypedDict):
    snapshotID: str
    sourceServerID: str
    expectedTimestamp: str
    timestamp: NotRequired[str]
    ebsSnapshots: NotRequired[list[str]]


class DescribeReplicationConfigurationTemplatesRequestTypeDef(TypedDict):
    replicationConfigurationTemplateIDs: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeSourceNetworksRequestFiltersTypeDef(TypedDict):
    sourceNetworkIDs: NotRequired[Sequence[str]]
    originAccountID: NotRequired[str]
    originRegion: NotRequired[str]


class DescribeSourceServersRequestFiltersTypeDef(TypedDict):
    sourceServerIDs: NotRequired[Sequence[str]]
    hardwareId: NotRequired[str]
    stagingAccountIDs: NotRequired[Sequence[str]]


class DisconnectRecoveryInstanceRequestTypeDef(TypedDict):
    recoveryInstanceID: str


class DisconnectSourceServerRequestTypeDef(TypedDict):
    sourceServerID: str


DiskTypeDef = TypedDict(
    "DiskTypeDef",
    {
        "deviceName": NotRequired[str],
        "bytes": NotRequired[int],
    },
)


class SourceNetworkDataTypeDef(TypedDict):
    sourceNetworkID: NotRequired[str]
    sourceVpc: NotRequired[str]
    targetVpc: NotRequired[str]
    stackName: NotRequired[str]


class ExportSourceNetworkCfnTemplateRequestTypeDef(TypedDict):
    sourceNetworkID: str


class GetFailbackReplicationConfigurationRequestTypeDef(TypedDict):
    recoveryInstanceID: str


class GetLaunchConfigurationRequestTypeDef(TypedDict):
    sourceServerID: str


class GetReplicationConfigurationRequestTypeDef(TypedDict):
    sourceServerID: str


class IdentificationHintsTypeDef(TypedDict):
    fqdn: NotRequired[str]
    hostname: NotRequired[str]
    vmWareUuid: NotRequired[str]
    awsInstanceID: NotRequired[str]


LaunchActionParameterTypeDef = TypedDict(
    "LaunchActionParameterTypeDef",
    {
        "value": NotRequired[str],
        "type": NotRequired[LaunchActionParameterTypeType],
    },
)


class LaunchActionsRequestFiltersTypeDef(TypedDict):
    actionIds: NotRequired[Sequence[str]]


class LaunchIntoInstancePropertiesTypeDef(TypedDict):
    launchIntoEC2InstanceID: NotRequired[str]


LifeCycleLastLaunchInitiatedTypeDef = TypedDict(
    "LifeCycleLastLaunchInitiatedTypeDef",
    {
        "apiCallDateTime": NotRequired[str],
        "jobID": NotRequired[str],
        "type": NotRequired[LastLaunchTypeType],
    },
)


class ListExtensibleSourceServersRequestTypeDef(TypedDict):
    stagingAccountID: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class StagingSourceServerTypeDef(TypedDict):
    hostname: NotRequired[str]
    arn: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class ListStagingAccountsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class NetworkInterfaceTypeDef(TypedDict):
    macAddress: NotRequired[str]
    ips: NotRequired[list[str]]
    isPrimary: NotRequired[bool]


class OSTypeDef(TypedDict):
    fullString: NotRequired[str]


class ParticipatingResourceIDTypeDef(TypedDict):
    sourceNetworkID: NotRequired[str]


class RecoveryInstanceDataReplicationErrorTypeDef(TypedDict):
    error: NotRequired[FailbackReplicationErrorType]
    rawError: NotRequired[str]


class RecoveryInstanceDataReplicationInfoReplicatedDiskTypeDef(TypedDict):
    deviceName: NotRequired[str]
    totalStorageBytes: NotRequired[int]
    replicatedStorageBytes: NotRequired[int]
    rescannedStorageBytes: NotRequired[int]
    backloggedStorageBytes: NotRequired[int]


class RecoveryInstanceDataReplicationInitiationStepTypeDef(TypedDict):
    name: NotRequired[RecoveryInstanceDataReplicationInitiationStepNameType]
    status: NotRequired[RecoveryInstanceDataReplicationInitiationStepStatusType]


RecoveryInstanceDiskTypeDef = TypedDict(
    "RecoveryInstanceDiskTypeDef",
    {
        "internalDeviceName": NotRequired[str],
        "bytes": NotRequired[int],
        "ebsVolumeID": NotRequired[str],
    },
)


class RecoveryInstanceFailbackTypeDef(TypedDict):
    failbackClientID: NotRequired[str]
    failbackJobID: NotRequired[str]
    failbackInitiationTime: NotRequired[str]
    state: NotRequired[FailbackStateType]
    agentLastSeenByServiceDateTime: NotRequired[str]
    failbackClientLastSeenByServiceDateTime: NotRequired[str]
    failbackToOriginalServer: NotRequired[bool]
    firstByteDateTime: NotRequired[str]
    elapsedReplicationDuration: NotRequired[str]
    failbackLaunchType: NotRequired[FailbackLaunchTypeType]


class RecoveryLifeCycleTypeDef(TypedDict):
    apiCallDateTime: NotRequired[datetime]
    jobID: NotRequired[str]
    lastRecoveryResult: NotRequired[RecoveryResultType]


class ReplicationConfigurationReplicatedDiskTypeDef(TypedDict):
    deviceName: NotRequired[str]
    isBootDisk: NotRequired[bool]
    stagingDiskType: NotRequired[ReplicationConfigurationReplicatedDiskStagingDiskTypeType]
    iops: NotRequired[int]
    throughput: NotRequired[int]
    optimizedStagingDiskType: NotRequired[ReplicationConfigurationReplicatedDiskStagingDiskTypeType]


class RetryDataReplicationRequestTypeDef(TypedDict):
    sourceServerID: str


class ReverseReplicationRequestTypeDef(TypedDict):
    recoveryInstanceID: str


class SourceCloudPropertiesTypeDef(TypedDict):
    originAccountID: NotRequired[str]
    originRegion: NotRequired[str]
    originAvailabilityZone: NotRequired[str]
    sourceOutpostArn: NotRequired[str]


class StagingAreaTypeDef(TypedDict):
    status: NotRequired[ExtensionStatusType]
    stagingAccountID: NotRequired[str]
    stagingSourceServerArn: NotRequired[str]
    errorMessage: NotRequired[str]


class StartFailbackLaunchRequestTypeDef(TypedDict):
    recoveryInstanceIDs: Sequence[str]
    tags: NotRequired[Mapping[str, str]]


class StartRecoveryRequestSourceServerTypeDef(TypedDict):
    sourceServerID: str
    recoverySnapshotID: NotRequired[str]


class StartReplicationRequestTypeDef(TypedDict):
    sourceServerID: str


class StartSourceNetworkRecoveryRequestNetworkEntryTypeDef(TypedDict):
    sourceNetworkID: str
    cfnStackName: NotRequired[str]


class StartSourceNetworkReplicationRequestTypeDef(TypedDict):
    sourceNetworkID: str


class StopFailbackRequestTypeDef(TypedDict):
    recoveryInstanceID: str


class StopReplicationRequestTypeDef(TypedDict):
    sourceServerID: str


class StopSourceNetworkReplicationRequestTypeDef(TypedDict):
    sourceNetworkID: str


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class TerminateRecoveryInstancesRequestTypeDef(TypedDict):
    recoveryInstanceIDs: Sequence[str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateFailbackReplicationConfigurationRequestTypeDef(TypedDict):
    recoveryInstanceID: str
    name: NotRequired[str]
    bandwidthThrottling: NotRequired[int]
    usePrivateIP: NotRequired[bool]
    internetProtocol: NotRequired[InternetProtocolType]


class CreateSourceNetworkResponseTypeDef(TypedDict):
    sourceNetworkID: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ExportSourceNetworkCfnTemplateResponseTypeDef(TypedDict):
    s3DestinationUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetFailbackReplicationConfigurationResponseTypeDef(TypedDict):
    recoveryInstanceID: str
    name: str
    bandwidthThrottling: int
    usePrivateIP: bool
    internetProtocol: InternetProtocolType
    ResponseMetadata: ResponseMetadataTypeDef


class ListStagingAccountsResponseTypeDef(TypedDict):
    accounts: list[AccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ReverseReplicationResponseTypeDef(TypedDict):
    reversedDirectionSourceServerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ConversionPropertiesTypeDef(TypedDict):
    volumeToConversionMap: NotRequired[dict[str, dict[str, str]]]
    rootVolumeName: NotRequired[str]
    forceUefi: NotRequired[bool]
    dataTimestamp: NotRequired[str]
    volumeToVolumeSize: NotRequired[dict[str, int]]
    volumeToProductCodes: NotRequired[dict[str, list[ProductCodeTypeDef]]]


class CreateLaunchConfigurationTemplateRequestTypeDef(TypedDict):
    tags: NotRequired[Mapping[str, str]]
    launchDisposition: NotRequired[LaunchDispositionType]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    licensing: NotRequired[LicensingTypeDef]
    exportBucketArn: NotRequired[str]
    postLaunchEnabled: NotRequired[bool]
    launchIntoSourceInstance: NotRequired[bool]


class LaunchConfigurationTemplateTypeDef(TypedDict):
    launchConfigurationTemplateID: NotRequired[str]
    arn: NotRequired[str]
    tags: NotRequired[dict[str, str]]
    launchDisposition: NotRequired[LaunchDispositionType]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    licensing: NotRequired[LicensingTypeDef]
    exportBucketArn: NotRequired[str]
    postLaunchEnabled: NotRequired[bool]
    launchIntoSourceInstance: NotRequired[bool]


class UpdateLaunchConfigurationTemplateRequestTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    launchDisposition: NotRequired[LaunchDispositionType]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    licensing: NotRequired[LicensingTypeDef]
    exportBucketArn: NotRequired[str]
    postLaunchEnabled: NotRequired[bool]
    launchIntoSourceInstance: NotRequired[bool]


class CreateReplicationConfigurationTemplateRequestTypeDef(TypedDict):
    stagingAreaSubnetId: str
    replicationServersSecurityGroupsIDs: Sequence[str]
    ebsEncryption: ReplicationConfigurationEbsEncryptionType
    bandwidthThrottling: int
    stagingAreaTags: Mapping[str, str]
    pitPolicy: Sequence[PITPolicyRuleTypeDef]
    associateDefaultSecurityGroup: NotRequired[bool]
    replicationServerInstanceType: NotRequired[str]
    useDedicatedReplicationServer: NotRequired[bool]
    defaultLargeStagingDiskType: NotRequired[
        ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ]
    ebsEncryptionKeyArn: NotRequired[str]
    dataPlaneRouting: NotRequired[ReplicationConfigurationDataPlaneRoutingType]
    createPublicIP: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]
    autoReplicateNewDisks: NotRequired[bool]
    internetProtocol: NotRequired[InternetProtocolType]


class ReplicationConfigurationTemplateResponseTypeDef(TypedDict):
    replicationConfigurationTemplateID: str
    arn: str
    stagingAreaSubnetId: str
    associateDefaultSecurityGroup: bool
    replicationServersSecurityGroupsIDs: list[str]
    replicationServerInstanceType: str
    useDedicatedReplicationServer: bool
    defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ebsEncryption: ReplicationConfigurationEbsEncryptionType
    ebsEncryptionKeyArn: str
    bandwidthThrottling: int
    dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType
    createPublicIP: bool
    stagingAreaTags: dict[str, str]
    tags: dict[str, str]
    pitPolicy: list[PITPolicyRuleTypeDef]
    autoReplicateNewDisks: bool
    internetProtocol: InternetProtocolType
    ResponseMetadata: ResponseMetadataTypeDef


class ReplicationConfigurationTemplateTypeDef(TypedDict):
    replicationConfigurationTemplateID: str
    arn: NotRequired[str]
    stagingAreaSubnetId: NotRequired[str]
    associateDefaultSecurityGroup: NotRequired[bool]
    replicationServersSecurityGroupsIDs: NotRequired[list[str]]
    replicationServerInstanceType: NotRequired[str]
    useDedicatedReplicationServer: NotRequired[bool]
    defaultLargeStagingDiskType: NotRequired[
        ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ]
    ebsEncryption: NotRequired[ReplicationConfigurationEbsEncryptionType]
    ebsEncryptionKeyArn: NotRequired[str]
    bandwidthThrottling: NotRequired[int]
    dataPlaneRouting: NotRequired[ReplicationConfigurationDataPlaneRoutingType]
    createPublicIP: NotRequired[bool]
    stagingAreaTags: NotRequired[dict[str, str]]
    tags: NotRequired[dict[str, str]]
    pitPolicy: NotRequired[list[PITPolicyRuleTypeDef]]
    autoReplicateNewDisks: NotRequired[bool]
    internetProtocol: NotRequired[InternetProtocolType]


class UpdateReplicationConfigurationTemplateRequestTypeDef(TypedDict):
    replicationConfigurationTemplateID: str
    arn: NotRequired[str]
    stagingAreaSubnetId: NotRequired[str]
    associateDefaultSecurityGroup: NotRequired[bool]
    replicationServersSecurityGroupsIDs: NotRequired[Sequence[str]]
    replicationServerInstanceType: NotRequired[str]
    useDedicatedReplicationServer: NotRequired[bool]
    defaultLargeStagingDiskType: NotRequired[
        ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ]
    ebsEncryption: NotRequired[ReplicationConfigurationEbsEncryptionType]
    ebsEncryptionKeyArn: NotRequired[str]
    bandwidthThrottling: NotRequired[int]
    dataPlaneRouting: NotRequired[ReplicationConfigurationDataPlaneRoutingType]
    createPublicIP: NotRequired[bool]
    stagingAreaTags: NotRequired[Mapping[str, str]]
    pitPolicy: NotRequired[Sequence[PITPolicyRuleTypeDef]]
    autoReplicateNewDisks: NotRequired[bool]
    internetProtocol: NotRequired[InternetProtocolType]


class DataReplicationInitiationTypeDef(TypedDict):
    startDateTime: NotRequired[str]
    nextAttemptDateTime: NotRequired[str]
    steps: NotRequired[list[DataReplicationInitiationStepTypeDef]]


class DescribeJobLogItemsRequestPaginateTypeDef(TypedDict):
    jobID: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLaunchConfigurationTemplatesRequestPaginateTypeDef(TypedDict):
    launchConfigurationTemplateIDs: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReplicationConfigurationTemplatesRequestPaginateTypeDef(TypedDict):
    replicationConfigurationTemplateIDs: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListExtensibleSourceServersRequestPaginateTypeDef(TypedDict):
    stagingAccountID: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStagingAccountsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeJobsRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[DescribeJobsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeJobsRequestTypeDef(TypedDict):
    filters: NotRequired[DescribeJobsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeRecoveryInstancesRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[DescribeRecoveryInstancesRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeRecoveryInstancesRequestTypeDef(TypedDict):
    filters: NotRequired[DescribeRecoveryInstancesRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeRecoverySnapshotsRequestPaginateTypeDef(TypedDict):
    sourceServerID: str
    filters: NotRequired[DescribeRecoverySnapshotsRequestFiltersTypeDef]
    order: NotRequired[RecoverySnapshotsOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeRecoverySnapshotsRequestTypeDef(TypedDict):
    sourceServerID: str
    filters: NotRequired[DescribeRecoverySnapshotsRequestFiltersTypeDef]
    order: NotRequired[RecoverySnapshotsOrderType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeRecoverySnapshotsResponseTypeDef(TypedDict):
    items: list[RecoverySnapshotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DescribeSourceNetworksRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[DescribeSourceNetworksRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSourceNetworksRequestTypeDef(TypedDict):
    filters: NotRequired[DescribeSourceNetworksRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeSourceServersRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[DescribeSourceServersRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSourceServersRequestTypeDef(TypedDict):
    filters: NotRequired[DescribeSourceServersRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class EventResourceDataTypeDef(TypedDict):
    sourceNetworkData: NotRequired[SourceNetworkDataTypeDef]


LaunchActionTypeDef = TypedDict(
    "LaunchActionTypeDef",
    {
        "actionId": NotRequired[str],
        "actionCode": NotRequired[str],
        "type": NotRequired[LaunchActionTypeType],
        "name": NotRequired[str],
        "active": NotRequired[bool],
        "order": NotRequired[int],
        "actionVersion": NotRequired[str],
        "optional": NotRequired[bool],
        "parameters": NotRequired[dict[str, LaunchActionParameterTypeDef]],
        "description": NotRequired[str],
        "category": NotRequired[LaunchActionCategoryType],
    },
)


class PutLaunchActionRequestTypeDef(TypedDict):
    resourceId: str
    actionCode: str
    order: int
    actionId: str
    optional: bool
    active: bool
    name: str
    actionVersion: str
    category: LaunchActionCategoryType
    description: str
    parameters: NotRequired[Mapping[str, LaunchActionParameterTypeDef]]


PutLaunchActionResponseTypeDef = TypedDict(
    "PutLaunchActionResponseTypeDef",
    {
        "resourceId": str,
        "actionId": str,
        "actionCode": str,
        "type": LaunchActionTypeType,
        "name": str,
        "active": bool,
        "order": int,
        "actionVersion": str,
        "optional": bool,
        "parameters": dict[str, LaunchActionParameterTypeDef],
        "description": str,
        "category": LaunchActionCategoryType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListLaunchActionsRequestPaginateTypeDef(TypedDict):
    resourceId: str
    filters: NotRequired[LaunchActionsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLaunchActionsRequestTypeDef(TypedDict):
    resourceId: str
    filters: NotRequired[LaunchActionsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class LaunchConfigurationTypeDef(TypedDict):
    sourceServerID: str
    name: str
    ec2LaunchTemplateID: str
    launchDisposition: LaunchDispositionType
    targetInstanceTypeRightSizingMethod: TargetInstanceTypeRightSizingMethodType
    copyPrivateIp: bool
    copyTags: bool
    licensing: LicensingTypeDef
    postLaunchEnabled: bool
    launchIntoInstanceProperties: LaunchIntoInstancePropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateLaunchConfigurationRequestTypeDef(TypedDict):
    sourceServerID: str
    name: NotRequired[str]
    launchDisposition: NotRequired[LaunchDispositionType]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    licensing: NotRequired[LicensingTypeDef]
    postLaunchEnabled: NotRequired[bool]
    launchIntoInstanceProperties: NotRequired[LaunchIntoInstancePropertiesTypeDef]


class LifeCycleLastLaunchTypeDef(TypedDict):
    initiated: NotRequired[LifeCycleLastLaunchInitiatedTypeDef]
    status: NotRequired[LaunchStatusType]


class ListExtensibleSourceServersResponseTypeDef(TypedDict):
    items: list[StagingSourceServerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SourcePropertiesTypeDef(TypedDict):
    lastUpdatedDateTime: NotRequired[str]
    recommendedInstanceType: NotRequired[str]
    identificationHints: NotRequired[IdentificationHintsTypeDef]
    networkInterfaces: NotRequired[list[NetworkInterfaceTypeDef]]
    disks: NotRequired[list[DiskTypeDef]]
    cpus: NotRequired[list[CPUTypeDef]]
    ramBytes: NotRequired[int]
    os: NotRequired[OSTypeDef]
    supportsNitroInstances: NotRequired[bool]


class ParticipatingResourceTypeDef(TypedDict):
    participatingResourceID: NotRequired[ParticipatingResourceIDTypeDef]
    launchStatus: NotRequired[LaunchStatusType]


class RecoveryInstanceDataReplicationInitiationTypeDef(TypedDict):
    startDateTime: NotRequired[str]
    steps: NotRequired[list[RecoveryInstanceDataReplicationInitiationStepTypeDef]]


class RecoveryInstancePropertiesTypeDef(TypedDict):
    lastUpdatedDateTime: NotRequired[str]
    identificationHints: NotRequired[IdentificationHintsTypeDef]
    networkInterfaces: NotRequired[list[NetworkInterfaceTypeDef]]
    disks: NotRequired[list[RecoveryInstanceDiskTypeDef]]
    cpus: NotRequired[list[CPUTypeDef]]
    ramBytes: NotRequired[int]
    os: NotRequired[OSTypeDef]


class SourceNetworkTypeDef(TypedDict):
    sourceNetworkID: NotRequired[str]
    sourceVpcID: NotRequired[str]
    arn: NotRequired[str]
    tags: NotRequired[dict[str, str]]
    replicationStatus: NotRequired[ReplicationStatusType]
    replicationStatusDetails: NotRequired[str]
    cfnStackName: NotRequired[str]
    sourceRegion: NotRequired[str]
    sourceAccountID: NotRequired[str]
    lastRecovery: NotRequired[RecoveryLifeCycleTypeDef]
    launchedVpcID: NotRequired[str]


class ReplicationConfigurationTypeDef(TypedDict):
    sourceServerID: str
    name: str
    stagingAreaSubnetId: str
    associateDefaultSecurityGroup: bool
    replicationServersSecurityGroupsIDs: list[str]
    replicationServerInstanceType: str
    useDedicatedReplicationServer: bool
    defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType
    replicatedDisks: list[ReplicationConfigurationReplicatedDiskTypeDef]
    ebsEncryption: ReplicationConfigurationEbsEncryptionType
    ebsEncryptionKeyArn: str
    bandwidthThrottling: int
    dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType
    createPublicIP: bool
    stagingAreaTags: dict[str, str]
    pitPolicy: list[PITPolicyRuleTypeDef]
    autoReplicateNewDisks: bool
    internetProtocol: InternetProtocolType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateReplicationConfigurationRequestTypeDef(TypedDict):
    sourceServerID: str
    name: NotRequired[str]
    stagingAreaSubnetId: NotRequired[str]
    associateDefaultSecurityGroup: NotRequired[bool]
    replicationServersSecurityGroupsIDs: NotRequired[Sequence[str]]
    replicationServerInstanceType: NotRequired[str]
    useDedicatedReplicationServer: NotRequired[bool]
    defaultLargeStagingDiskType: NotRequired[
        ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ]
    replicatedDisks: NotRequired[Sequence[ReplicationConfigurationReplicatedDiskTypeDef]]
    ebsEncryption: NotRequired[ReplicationConfigurationEbsEncryptionType]
    ebsEncryptionKeyArn: NotRequired[str]
    bandwidthThrottling: NotRequired[int]
    dataPlaneRouting: NotRequired[ReplicationConfigurationDataPlaneRoutingType]
    createPublicIP: NotRequired[bool]
    stagingAreaTags: NotRequired[Mapping[str, str]]
    pitPolicy: NotRequired[Sequence[PITPolicyRuleTypeDef]]
    autoReplicateNewDisks: NotRequired[bool]
    internetProtocol: NotRequired[InternetProtocolType]


class StartRecoveryRequestTypeDef(TypedDict):
    sourceServers: Sequence[StartRecoveryRequestSourceServerTypeDef]
    isDrill: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]


class StartSourceNetworkRecoveryRequestTypeDef(TypedDict):
    sourceNetworks: Sequence[StartSourceNetworkRecoveryRequestNetworkEntryTypeDef]
    deployAsNew: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]


class CreateLaunchConfigurationTemplateResponseTypeDef(TypedDict):
    launchConfigurationTemplate: LaunchConfigurationTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLaunchConfigurationTemplatesResponseTypeDef(TypedDict):
    items: list[LaunchConfigurationTemplateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateLaunchConfigurationTemplateResponseTypeDef(TypedDict):
    launchConfigurationTemplate: LaunchConfigurationTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReplicationConfigurationTemplatesResponseTypeDef(TypedDict):
    items: list[ReplicationConfigurationTemplateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DataReplicationInfoTypeDef(TypedDict):
    lagDuration: NotRequired[str]
    etaDateTime: NotRequired[str]
    replicatedDisks: NotRequired[list[DataReplicationInfoReplicatedDiskTypeDef]]
    dataReplicationState: NotRequired[DataReplicationStateType]
    dataReplicationInitiation: NotRequired[DataReplicationInitiationTypeDef]
    dataReplicationError: NotRequired[DataReplicationErrorTypeDef]
    stagingAvailabilityZone: NotRequired[str]
    stagingOutpostArn: NotRequired[str]


class JobLogEventDataTypeDef(TypedDict):
    sourceServerID: NotRequired[str]
    conversionServerID: NotRequired[str]
    targetInstanceID: NotRequired[str]
    rawError: NotRequired[str]
    conversionProperties: NotRequired[ConversionPropertiesTypeDef]
    eventResourceData: NotRequired[EventResourceDataTypeDef]
    attemptCount: NotRequired[int]
    maxAttemptsCount: NotRequired[int]


class LaunchActionRunTypeDef(TypedDict):
    action: NotRequired[LaunchActionTypeDef]
    runId: NotRequired[str]
    status: NotRequired[LaunchActionRunStatusType]
    failureReason: NotRequired[str]


class ListLaunchActionsResponseTypeDef(TypedDict):
    items: list[LaunchActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class LifeCycleTypeDef(TypedDict):
    addedToServiceDateTime: NotRequired[str]
    firstByteDateTime: NotRequired[str]
    elapsedReplicationDuration: NotRequired[str]
    lastSeenByServiceDateTime: NotRequired[str]
    lastLaunch: NotRequired[LifeCycleLastLaunchTypeDef]


class RecoveryInstanceDataReplicationInfoTypeDef(TypedDict):
    lagDuration: NotRequired[str]
    etaDateTime: NotRequired[str]
    replicatedDisks: NotRequired[list[RecoveryInstanceDataReplicationInfoReplicatedDiskTypeDef]]
    dataReplicationState: NotRequired[RecoveryInstanceDataReplicationStateType]
    dataReplicationInitiation: NotRequired[RecoveryInstanceDataReplicationInitiationTypeDef]
    dataReplicationError: NotRequired[RecoveryInstanceDataReplicationErrorTypeDef]
    stagingAvailabilityZone: NotRequired[str]
    stagingOutpostArn: NotRequired[str]


class DescribeSourceNetworksResponseTypeDef(TypedDict):
    items: list[SourceNetworkTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartSourceNetworkReplicationResponseTypeDef(TypedDict):
    sourceNetwork: SourceNetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopSourceNetworkReplicationResponseTypeDef(TypedDict):
    sourceNetwork: SourceNetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class JobLogTypeDef(TypedDict):
    logDateTime: NotRequired[str]
    event: NotRequired[JobLogEventType]
    eventData: NotRequired[JobLogEventDataTypeDef]


class LaunchActionsStatusTypeDef(TypedDict):
    ssmAgentDiscoveryDatetime: NotRequired[str]
    runs: NotRequired[list[LaunchActionRunTypeDef]]


class SourceServerResponseTypeDef(TypedDict):
    sourceServerID: str
    arn: str
    tags: dict[str, str]
    recoveryInstanceId: str
    lastLaunchResult: LastLaunchResultType
    dataReplicationInfo: DataReplicationInfoTypeDef
    lifeCycle: LifeCycleTypeDef
    sourceProperties: SourcePropertiesTypeDef
    stagingArea: StagingAreaTypeDef
    sourceCloudProperties: SourceCloudPropertiesTypeDef
    replicationDirection: ReplicationDirectionType
    reversedDirectionSourceServerArn: str
    sourceNetworkID: str
    agentVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class SourceServerTypeDef(TypedDict):
    sourceServerID: NotRequired[str]
    arn: NotRequired[str]
    tags: NotRequired[dict[str, str]]
    recoveryInstanceId: NotRequired[str]
    lastLaunchResult: NotRequired[LastLaunchResultType]
    dataReplicationInfo: NotRequired[DataReplicationInfoTypeDef]
    lifeCycle: NotRequired[LifeCycleTypeDef]
    sourceProperties: NotRequired[SourcePropertiesTypeDef]
    stagingArea: NotRequired[StagingAreaTypeDef]
    sourceCloudProperties: NotRequired[SourceCloudPropertiesTypeDef]
    replicationDirection: NotRequired[ReplicationDirectionType]
    reversedDirectionSourceServerArn: NotRequired[str]
    sourceNetworkID: NotRequired[str]
    agentVersion: NotRequired[str]


class RecoveryInstanceTypeDef(TypedDict):
    ec2InstanceID: NotRequired[str]
    ec2InstanceState: NotRequired[EC2InstanceStateType]
    jobID: NotRequired[str]
    recoveryInstanceID: NotRequired[str]
    sourceServerID: NotRequired[str]
    arn: NotRequired[str]
    tags: NotRequired[dict[str, str]]
    failback: NotRequired[RecoveryInstanceFailbackTypeDef]
    dataReplicationInfo: NotRequired[RecoveryInstanceDataReplicationInfoTypeDef]
    recoveryInstanceProperties: NotRequired[RecoveryInstancePropertiesTypeDef]
    pointInTimeSnapshotDateTime: NotRequired[str]
    isDrill: NotRequired[bool]
    originEnvironment: NotRequired[OriginEnvironmentType]
    originAvailabilityZone: NotRequired[str]
    agentVersion: NotRequired[str]
    sourceOutpostArn: NotRequired[str]


class DescribeJobLogItemsResponseTypeDef(TypedDict):
    items: list[JobLogTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ParticipatingServerTypeDef(TypedDict):
    sourceServerID: NotRequired[str]
    recoveryInstanceID: NotRequired[str]
    launchStatus: NotRequired[LaunchStatusType]
    launchActionsStatus: NotRequired[LaunchActionsStatusTypeDef]


class CreateExtendedSourceServerResponseTypeDef(TypedDict):
    sourceServer: SourceServerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSourceServersResponseTypeDef(TypedDict):
    items: list[SourceServerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartReplicationResponseTypeDef(TypedDict):
    sourceServer: SourceServerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopReplicationResponseTypeDef(TypedDict):
    sourceServer: SourceServerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRecoveryInstancesResponseTypeDef(TypedDict):
    items: list[RecoveryInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "jobID": str,
        "arn": NotRequired[str],
        "type": NotRequired[JobTypeType],
        "initiatedBy": NotRequired[InitiatedByType],
        "creationDateTime": NotRequired[str],
        "endDateTime": NotRequired[str],
        "status": NotRequired[JobStatusType],
        "participatingServers": NotRequired[list[ParticipatingServerTypeDef]],
        "tags": NotRequired[dict[str, str]],
        "participatingResources": NotRequired[list[ParticipatingResourceTypeDef]],
    },
)


class AssociateSourceNetworkStackResponseTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeJobsResponseTypeDef(TypedDict):
    items: list[JobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartFailbackLaunchResponseTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartRecoveryResponseTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartSourceNetworkRecoveryResponseTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TerminateRecoveryInstancesResponseTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
