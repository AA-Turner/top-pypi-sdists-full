"""
Type annotations for mgn service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mgn/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_mgn.type_defs import ApplicationAggregatedStatusTypeDef

    data: ApplicationAggregatedStatusTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from typing import Union

from .literals import (
    ActionCategoryType,
    ApplicationHealthStatusType,
    ApplicationProgressStatusType,
    BootModeType,
    ChangeServerLifeCycleStateSourceServerLifecycleStateType,
    DataReplicationErrorStringType,
    DataReplicationInitiationStepNameType,
    DataReplicationInitiationStepStatusType,
    DataReplicationStateType,
    ExportStatusType,
    FirstBootType,
    ImportErrorTypeType,
    ImportStatusType,
    InitiatedByType,
    InternetProtocolType,
    JobLogEventType,
    JobStatusType,
    JobTypeType,
    LaunchDispositionType,
    LaunchStatusType,
    LifeCycleStateType,
    PostLaunchActionExecutionStatusType,
    PostLaunchActionsDeploymentTypeType,
    ReplicationConfigurationDataPlaneRoutingType,
    ReplicationConfigurationDefaultLargeStagingDiskTypeType,
    ReplicationConfigurationEbsEncryptionType,
    ReplicationConfigurationReplicatedDiskStagingDiskTypeType,
    ReplicationTypeType,
    SsmDocumentTypeType,
    SsmParameterStoreParameterTypeType,
    TargetInstanceTypeRightSizingMethodType,
    VolumeTypeType,
    WaveHealthStatusType,
    WaveProgressStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ApplicationAggregatedStatusTypeDef",
    "ApplicationResponseTypeDef",
    "ApplicationTypeDef",
    "ArchiveApplicationRequestTypeDef",
    "ArchiveWaveRequestTypeDef",
    "AssociateApplicationsRequestTypeDef",
    "AssociateSourceServersRequestTypeDef",
    "CPUTypeDef",
    "ChangeServerLifeCycleStateRequestTypeDef",
    "ChangeServerLifeCycleStateSourceServerLifecycleTypeDef",
    "ConnectorResponseTypeDef",
    "ConnectorSsmCommandConfigTypeDef",
    "ConnectorTypeDef",
    "CreateApplicationRequestTypeDef",
    "CreateConnectorRequestTypeDef",
    "CreateLaunchConfigurationTemplateRequestTypeDef",
    "CreateReplicationConfigurationTemplateRequestTypeDef",
    "CreateWaveRequestTypeDef",
    "DataReplicationErrorTypeDef",
    "DataReplicationInfoReplicatedDiskTypeDef",
    "DataReplicationInfoTypeDef",
    "DataReplicationInitiationStepTypeDef",
    "DataReplicationInitiationTypeDef",
    "DeleteApplicationRequestTypeDef",
    "DeleteConnectorRequestTypeDef",
    "DeleteJobRequestTypeDef",
    "DeleteLaunchConfigurationTemplateRequestTypeDef",
    "DeleteReplicationConfigurationTemplateRequestTypeDef",
    "DeleteSourceServerRequestTypeDef",
    "DeleteVcenterClientRequestTypeDef",
    "DeleteWaveRequestTypeDef",
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
    "DescribeReplicationConfigurationTemplatesRequestPaginateTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestTypeDef",
    "DescribeReplicationConfigurationTemplatesResponseTypeDef",
    "DescribeSourceServersRequestFiltersTypeDef",
    "DescribeSourceServersRequestPaginateTypeDef",
    "DescribeSourceServersRequestTypeDef",
    "DescribeSourceServersResponseTypeDef",
    "DescribeVcenterClientsRequestPaginateTypeDef",
    "DescribeVcenterClientsRequestTypeDef",
    "DescribeVcenterClientsResponseTypeDef",
    "DisassociateApplicationsRequestTypeDef",
    "DisassociateSourceServersRequestTypeDef",
    "DisconnectFromServiceRequestTypeDef",
    "DiskTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportErrorDataTypeDef",
    "ExportTaskErrorTypeDef",
    "ExportTaskSummaryTypeDef",
    "ExportTaskTypeDef",
    "FinalizeCutoverRequestTypeDef",
    "GetLaunchConfigurationRequestTypeDef",
    "GetReplicationConfigurationRequestTypeDef",
    "IdentificationHintsTypeDef",
    "ImportErrorDataTypeDef",
    "ImportTaskErrorTypeDef",
    "ImportTaskSummaryApplicationsTypeDef",
    "ImportTaskSummaryServersTypeDef",
    "ImportTaskSummaryTypeDef",
    "ImportTaskSummaryWavesTypeDef",
    "ImportTaskTypeDef",
    "JobLogEventDataTypeDef",
    "JobLogTypeDef",
    "JobPostLaunchActionsLaunchStatusTypeDef",
    "JobTypeDef",
    "LaunchConfigurationTemplateResponseTypeDef",
    "LaunchConfigurationTemplateTypeDef",
    "LaunchConfigurationTypeDef",
    "LaunchTemplateDiskConfTypeDef",
    "LaunchedInstanceTypeDef",
    "LicensingTypeDef",
    "LifeCycleLastCutoverFinalizedTypeDef",
    "LifeCycleLastCutoverInitiatedTypeDef",
    "LifeCycleLastCutoverRevertedTypeDef",
    "LifeCycleLastCutoverTypeDef",
    "LifeCycleLastTestFinalizedTypeDef",
    "LifeCycleLastTestInitiatedTypeDef",
    "LifeCycleLastTestRevertedTypeDef",
    "LifeCycleLastTestTypeDef",
    "LifeCycleTypeDef",
    "ListApplicationsRequestFiltersTypeDef",
    "ListApplicationsRequestPaginateTypeDef",
    "ListApplicationsRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListConnectorsRequestFiltersTypeDef",
    "ListConnectorsRequestPaginateTypeDef",
    "ListConnectorsRequestTypeDef",
    "ListConnectorsResponseTypeDef",
    "ListExportErrorsRequestPaginateTypeDef",
    "ListExportErrorsRequestTypeDef",
    "ListExportErrorsResponseTypeDef",
    "ListExportsRequestFiltersTypeDef",
    "ListExportsRequestPaginateTypeDef",
    "ListExportsRequestTypeDef",
    "ListExportsResponseTypeDef",
    "ListImportErrorsRequestPaginateTypeDef",
    "ListImportErrorsRequestTypeDef",
    "ListImportErrorsResponseTypeDef",
    "ListImportsRequestFiltersTypeDef",
    "ListImportsRequestPaginateTypeDef",
    "ListImportsRequestTypeDef",
    "ListImportsResponseTypeDef",
    "ListManagedAccountsRequestPaginateTypeDef",
    "ListManagedAccountsRequestTypeDef",
    "ListManagedAccountsResponseTypeDef",
    "ListSourceServerActionsRequestPaginateTypeDef",
    "ListSourceServerActionsRequestTypeDef",
    "ListSourceServerActionsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTemplateActionsRequestPaginateTypeDef",
    "ListTemplateActionsRequestTypeDef",
    "ListTemplateActionsResponseTypeDef",
    "ListWavesRequestFiltersTypeDef",
    "ListWavesRequestPaginateTypeDef",
    "ListWavesRequestTypeDef",
    "ListWavesResponseTypeDef",
    "ManagedAccountTypeDef",
    "MarkAsArchivedRequestTypeDef",
    "NetworkInterfaceTypeDef",
    "OSTypeDef",
    "PaginatorConfigTypeDef",
    "ParticipatingServerTypeDef",
    "PauseReplicationRequestTypeDef",
    "PostLaunchActionsOutputTypeDef",
    "PostLaunchActionsStatusTypeDef",
    "PostLaunchActionsTypeDef",
    "PostLaunchActionsUnionTypeDef",
    "PutSourceServerActionRequestTypeDef",
    "PutTemplateActionRequestTypeDef",
    "RemoveSourceServerActionRequestTypeDef",
    "RemoveTemplateActionRequestTypeDef",
    "ReplicationConfigurationReplicatedDiskTypeDef",
    "ReplicationConfigurationTemplateResponseTypeDef",
    "ReplicationConfigurationTemplateTypeDef",
    "ReplicationConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "ResumeReplicationRequestTypeDef",
    "RetryDataReplicationRequestTypeDef",
    "S3BucketSourceTypeDef",
    "SourcePropertiesTypeDef",
    "SourceServerActionDocumentResponseTypeDef",
    "SourceServerActionDocumentTypeDef",
    "SourceServerActionsRequestFiltersTypeDef",
    "SourceServerConnectorActionTypeDef",
    "SourceServerResponseTypeDef",
    "SourceServerTypeDef",
    "SsmDocumentOutputTypeDef",
    "SsmDocumentTypeDef",
    "SsmExternalParameterTypeDef",
    "SsmParameterStoreParameterTypeDef",
    "StartCutoverRequestTypeDef",
    "StartCutoverResponseTypeDef",
    "StartExportRequestTypeDef",
    "StartExportResponseTypeDef",
    "StartImportRequestTypeDef",
    "StartImportResponseTypeDef",
    "StartReplicationRequestTypeDef",
    "StartTestRequestTypeDef",
    "StartTestResponseTypeDef",
    "StopReplicationRequestTypeDef",
    "TagResourceRequestTypeDef",
    "TemplateActionDocumentResponseTypeDef",
    "TemplateActionDocumentTypeDef",
    "TemplateActionsRequestFiltersTypeDef",
    "TerminateTargetInstancesRequestTypeDef",
    "TerminateTargetInstancesResponseTypeDef",
    "UnarchiveApplicationRequestTypeDef",
    "UnarchiveWaveRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateApplicationRequestTypeDef",
    "UpdateConnectorRequestTypeDef",
    "UpdateLaunchConfigurationRequestTypeDef",
    "UpdateLaunchConfigurationTemplateRequestTypeDef",
    "UpdateReplicationConfigurationRequestTypeDef",
    "UpdateReplicationConfigurationTemplateRequestTypeDef",
    "UpdateSourceServerReplicationTypeRequestTypeDef",
    "UpdateSourceServerRequestTypeDef",
    "UpdateWaveRequestTypeDef",
    "VcenterClientTypeDef",
    "WaveAggregatedStatusTypeDef",
    "WaveResponseTypeDef",
    "WaveTypeDef",
)


class ApplicationAggregatedStatusTypeDef(TypedDict):
    lastUpdateDateTime: NotRequired[str]
    healthStatus: NotRequired[ApplicationHealthStatusType]
    progressStatus: NotRequired[ApplicationProgressStatusType]
    totalSourceServers: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ArchiveApplicationRequestTypeDef(TypedDict):
    applicationID: str
    accountID: NotRequired[str]


class ArchiveWaveRequestTypeDef(TypedDict):
    waveID: str
    accountID: NotRequired[str]


class AssociateApplicationsRequestTypeDef(TypedDict):
    waveID: str
    applicationIDs: Sequence[str]
    accountID: NotRequired[str]


class AssociateSourceServersRequestTypeDef(TypedDict):
    applicationID: str
    sourceServerIDs: Sequence[str]
    accountID: NotRequired[str]


class CPUTypeDef(TypedDict):
    cores: NotRequired[int]
    modelName: NotRequired[str]


class ChangeServerLifeCycleStateSourceServerLifecycleTypeDef(TypedDict):
    state: ChangeServerLifeCycleStateSourceServerLifecycleStateType


class ConnectorSsmCommandConfigTypeDef(TypedDict):
    s3OutputEnabled: bool
    cloudWatchOutputEnabled: bool
    outputS3BucketName: NotRequired[str]
    cloudWatchLogGroupName: NotRequired[str]


class CreateApplicationRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    accountID: NotRequired[str]


class LaunchTemplateDiskConfTypeDef(TypedDict):
    volumeType: NotRequired[VolumeTypeType]
    iops: NotRequired[int]
    throughput: NotRequired[int]


class LicensingTypeDef(TypedDict):
    osByol: NotRequired[bool]


class CreateReplicationConfigurationTemplateRequestTypeDef(TypedDict):
    stagingAreaSubnetId: str
    associateDefaultSecurityGroup: bool
    replicationServersSecurityGroupsIDs: Sequence[str]
    replicationServerInstanceType: str
    useDedicatedReplicationServer: bool
    defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ebsEncryption: ReplicationConfigurationEbsEncryptionType
    bandwidthThrottling: int
    dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType
    createPublicIP: bool
    stagingAreaTags: Mapping[str, str]
    ebsEncryptionKeyArn: NotRequired[str]
    useFipsEndpoint: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]
    internetProtocol: NotRequired[InternetProtocolType]


class CreateWaveRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    accountID: NotRequired[str]


class DataReplicationErrorTypeDef(TypedDict):
    error: NotRequired[DataReplicationErrorStringType]
    rawError: NotRequired[str]


class DataReplicationInfoReplicatedDiskTypeDef(TypedDict):
    deviceName: NotRequired[str]
    totalStorageBytes: NotRequired[int]
    replicatedStorageBytes: NotRequired[int]
    rescannedStorageBytes: NotRequired[int]
    backloggedStorageBytes: NotRequired[int]


class DataReplicationInitiationStepTypeDef(TypedDict):
    name: NotRequired[DataReplicationInitiationStepNameType]
    status: NotRequired[DataReplicationInitiationStepStatusType]


class DeleteApplicationRequestTypeDef(TypedDict):
    applicationID: str
    accountID: NotRequired[str]


class DeleteConnectorRequestTypeDef(TypedDict):
    connectorID: str


class DeleteJobRequestTypeDef(TypedDict):
    jobID: str
    accountID: NotRequired[str]


class DeleteLaunchConfigurationTemplateRequestTypeDef(TypedDict):
    launchConfigurationTemplateID: str


class DeleteReplicationConfigurationTemplateRequestTypeDef(TypedDict):
    replicationConfigurationTemplateID: str


class DeleteSourceServerRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class DeleteVcenterClientRequestTypeDef(TypedDict):
    vcenterClientID: str


class DeleteWaveRequestTypeDef(TypedDict):
    waveID: str
    accountID: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeJobLogItemsRequestTypeDef(TypedDict):
    jobID: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    accountID: NotRequired[str]


class DescribeJobsRequestFiltersTypeDef(TypedDict):
    jobIDs: NotRequired[Sequence[str]]
    fromDate: NotRequired[str]
    toDate: NotRequired[str]


class DescribeLaunchConfigurationTemplatesRequestTypeDef(TypedDict):
    launchConfigurationTemplateIDs: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeReplicationConfigurationTemplatesRequestTypeDef(TypedDict):
    replicationConfigurationTemplateIDs: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


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
    useFipsEndpoint: NotRequired[bool]
    tags: NotRequired[dict[str, str]]
    internetProtocol: NotRequired[InternetProtocolType]


class DescribeSourceServersRequestFiltersTypeDef(TypedDict):
    sourceServerIDs: NotRequired[Sequence[str]]
    isArchived: NotRequired[bool]
    replicationTypes: NotRequired[Sequence[ReplicationTypeType]]
    lifeCycleStates: NotRequired[Sequence[LifeCycleStateType]]
    applicationIDs: NotRequired[Sequence[str]]


class DescribeVcenterClientsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class VcenterClientTypeDef(TypedDict):
    vcenterClientID: NotRequired[str]
    arn: NotRequired[str]
    hostname: NotRequired[str]
    vcenterUUID: NotRequired[str]
    datacenterName: NotRequired[str]
    lastSeenDatetime: NotRequired[str]
    sourceServerTags: NotRequired[dict[str, str]]
    tags: NotRequired[dict[str, str]]


class DisassociateApplicationsRequestTypeDef(TypedDict):
    waveID: str
    applicationIDs: Sequence[str]
    accountID: NotRequired[str]


class DisassociateSourceServersRequestTypeDef(TypedDict):
    applicationID: str
    sourceServerIDs: Sequence[str]
    accountID: NotRequired[str]


class DisconnectFromServiceRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


DiskTypeDef = TypedDict(
    "DiskTypeDef",
    {
        "deviceName": NotRequired[str],
        "bytes": NotRequired[int],
    },
)


class ExportErrorDataTypeDef(TypedDict):
    rawError: NotRequired[str]


class ExportTaskSummaryTypeDef(TypedDict):
    serversCount: NotRequired[int]
    applicationsCount: NotRequired[int]
    wavesCount: NotRequired[int]


class FinalizeCutoverRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class GetLaunchConfigurationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class GetReplicationConfigurationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class IdentificationHintsTypeDef(TypedDict):
    fqdn: NotRequired[str]
    hostname: NotRequired[str]
    vmWareUuid: NotRequired[str]
    awsInstanceID: NotRequired[str]
    vmPath: NotRequired[str]


class ImportErrorDataTypeDef(TypedDict):
    sourceServerID: NotRequired[str]
    applicationID: NotRequired[str]
    waveID: NotRequired[str]
    ec2LaunchTemplateID: NotRequired[str]
    rowNumber: NotRequired[int]
    rawError: NotRequired[str]
    accountID: NotRequired[str]


class ImportTaskSummaryApplicationsTypeDef(TypedDict):
    createdCount: NotRequired[int]
    modifiedCount: NotRequired[int]


class ImportTaskSummaryServersTypeDef(TypedDict):
    createdCount: NotRequired[int]
    modifiedCount: NotRequired[int]


class ImportTaskSummaryWavesTypeDef(TypedDict):
    createdCount: NotRequired[int]
    modifiedCount: NotRequired[int]


class S3BucketSourceTypeDef(TypedDict):
    s3Bucket: str
    s3Key: str
    s3BucketOwner: NotRequired[str]


class JobLogEventDataTypeDef(TypedDict):
    sourceServerID: NotRequired[str]
    conversionServerID: NotRequired[str]
    targetInstanceID: NotRequired[str]
    rawError: NotRequired[str]
    attemptCount: NotRequired[int]
    maxAttemptsCount: NotRequired[int]


class LaunchedInstanceTypeDef(TypedDict):
    ec2InstanceID: NotRequired[str]
    jobID: NotRequired[str]
    firstBoot: NotRequired[FirstBootType]


class LifeCycleLastCutoverFinalizedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]


class LifeCycleLastCutoverInitiatedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]
    jobID: NotRequired[str]


class LifeCycleLastCutoverRevertedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]


class LifeCycleLastTestFinalizedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]


class LifeCycleLastTestInitiatedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]
    jobID: NotRequired[str]


class LifeCycleLastTestRevertedTypeDef(TypedDict):
    apiCallDateTime: NotRequired[str]


class ListApplicationsRequestFiltersTypeDef(TypedDict):
    applicationIDs: NotRequired[Sequence[str]]
    isArchived: NotRequired[bool]
    waveIDs: NotRequired[Sequence[str]]


class ListConnectorsRequestFiltersTypeDef(TypedDict):
    connectorIDs: NotRequired[Sequence[str]]


class ListExportErrorsRequestTypeDef(TypedDict):
    exportID: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListExportsRequestFiltersTypeDef(TypedDict):
    exportIDs: NotRequired[Sequence[str]]


class ListImportErrorsRequestTypeDef(TypedDict):
    importID: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListImportsRequestFiltersTypeDef(TypedDict):
    importIDs: NotRequired[Sequence[str]]


class ListManagedAccountsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ManagedAccountTypeDef(TypedDict):
    accountId: NotRequired[str]


class SourceServerActionsRequestFiltersTypeDef(TypedDict):
    actionIDs: NotRequired[Sequence[str]]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class TemplateActionsRequestFiltersTypeDef(TypedDict):
    actionIDs: NotRequired[Sequence[str]]


class ListWavesRequestFiltersTypeDef(TypedDict):
    waveIDs: NotRequired[Sequence[str]]
    isArchived: NotRequired[bool]


class MarkAsArchivedRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class NetworkInterfaceTypeDef(TypedDict):
    macAddress: NotRequired[str]
    ips: NotRequired[list[str]]
    isPrimary: NotRequired[bool]


class OSTypeDef(TypedDict):
    fullString: NotRequired[str]


class PauseReplicationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class SsmExternalParameterTypeDef(TypedDict):
    dynamicPath: NotRequired[str]


class SsmParameterStoreParameterTypeDef(TypedDict):
    parameterType: SsmParameterStoreParameterTypeType
    parameterName: str


class RemoveSourceServerActionRequestTypeDef(TypedDict):
    sourceServerID: str
    actionID: str
    accountID: NotRequired[str]


class RemoveTemplateActionRequestTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    actionID: str


class ReplicationConfigurationReplicatedDiskTypeDef(TypedDict):
    deviceName: NotRequired[str]
    isBootDisk: NotRequired[bool]
    stagingDiskType: NotRequired[ReplicationConfigurationReplicatedDiskStagingDiskTypeType]
    iops: NotRequired[int]
    throughput: NotRequired[int]


class ResumeReplicationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class RetryDataReplicationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class SourceServerConnectorActionTypeDef(TypedDict):
    credentialsSecretArn: NotRequired[str]
    connectorArn: NotRequired[str]


class StartCutoverRequestTypeDef(TypedDict):
    sourceServerIDs: Sequence[str]
    tags: NotRequired[Mapping[str, str]]
    accountID: NotRequired[str]


class StartExportRequestTypeDef(TypedDict):
    s3Bucket: str
    s3Key: str
    s3BucketOwner: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class StartReplicationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class StartTestRequestTypeDef(TypedDict):
    sourceServerIDs: Sequence[str]
    tags: NotRequired[Mapping[str, str]]
    accountID: NotRequired[str]


class StopReplicationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class TerminateTargetInstancesRequestTypeDef(TypedDict):
    sourceServerIDs: Sequence[str]
    tags: NotRequired[Mapping[str, str]]
    accountID: NotRequired[str]


class UnarchiveApplicationRequestTypeDef(TypedDict):
    applicationID: str
    accountID: NotRequired[str]


class UnarchiveWaveRequestTypeDef(TypedDict):
    waveID: str
    accountID: NotRequired[str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateApplicationRequestTypeDef(TypedDict):
    applicationID: str
    name: NotRequired[str]
    description: NotRequired[str]
    accountID: NotRequired[str]


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
    useFipsEndpoint: NotRequired[bool]
    internetProtocol: NotRequired[InternetProtocolType]


class UpdateSourceServerReplicationTypeRequestTypeDef(TypedDict):
    sourceServerID: str
    replicationType: ReplicationTypeType
    accountID: NotRequired[str]


class UpdateWaveRequestTypeDef(TypedDict):
    waveID: str
    name: NotRequired[str]
    description: NotRequired[str]
    accountID: NotRequired[str]


class WaveAggregatedStatusTypeDef(TypedDict):
    lastUpdateDateTime: NotRequired[str]
    replicationStartedDateTime: NotRequired[str]
    healthStatus: NotRequired[WaveHealthStatusType]
    progressStatus: NotRequired[WaveProgressStatusType]
    totalApplications: NotRequired[int]


class ApplicationTypeDef(TypedDict):
    applicationID: NotRequired[str]
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    isArchived: NotRequired[bool]
    applicationAggregatedStatus: NotRequired[ApplicationAggregatedStatusTypeDef]
    creationDateTime: NotRequired[str]
    lastModifiedDateTime: NotRequired[str]
    tags: NotRequired[dict[str, str]]
    waveID: NotRequired[str]


class ApplicationResponseTypeDef(TypedDict):
    applicationID: str
    arn: str
    name: str
    description: str
    isArchived: bool
    applicationAggregatedStatus: ApplicationAggregatedStatusTypeDef
    creationDateTime: str
    lastModifiedDateTime: str
    tags: dict[str, str]
    waveID: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


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
    useFipsEndpoint: bool
    tags: dict[str, str]
    internetProtocol: InternetProtocolType
    ResponseMetadata: ResponseMetadataTypeDef


class ChangeServerLifeCycleStateRequestTypeDef(TypedDict):
    sourceServerID: str
    lifeCycle: ChangeServerLifeCycleStateSourceServerLifecycleTypeDef
    accountID: NotRequired[str]


class ConnectorResponseTypeDef(TypedDict):
    connectorID: str
    name: str
    ssmInstanceID: str
    arn: str
    tags: dict[str, str]
    ssmCommandConfig: ConnectorSsmCommandConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ConnectorTypeDef(TypedDict):
    connectorID: NotRequired[str]
    name: NotRequired[str]
    ssmInstanceID: NotRequired[str]
    arn: NotRequired[str]
    tags: NotRequired[dict[str, str]]
    ssmCommandConfig: NotRequired[ConnectorSsmCommandConfigTypeDef]


class CreateConnectorRequestTypeDef(TypedDict):
    name: str
    ssmInstanceID: str
    tags: NotRequired[Mapping[str, str]]
    ssmCommandConfig: NotRequired[ConnectorSsmCommandConfigTypeDef]


class UpdateConnectorRequestTypeDef(TypedDict):
    connectorID: str
    name: NotRequired[str]
    ssmCommandConfig: NotRequired[ConnectorSsmCommandConfigTypeDef]


class DataReplicationInitiationTypeDef(TypedDict):
    startDateTime: NotRequired[str]
    nextAttemptDateTime: NotRequired[str]
    steps: NotRequired[list[DataReplicationInitiationStepTypeDef]]


class DescribeJobLogItemsRequestPaginateTypeDef(TypedDict):
    jobID: str
    accountID: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLaunchConfigurationTemplatesRequestPaginateTypeDef(TypedDict):
    launchConfigurationTemplateIDs: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReplicationConfigurationTemplatesRequestPaginateTypeDef(TypedDict):
    replicationConfigurationTemplateIDs: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVcenterClientsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListExportErrorsRequestPaginateTypeDef(TypedDict):
    exportID: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImportErrorsRequestPaginateTypeDef(TypedDict):
    importID: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListManagedAccountsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeJobsRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[DescribeJobsRequestFiltersTypeDef]
    accountID: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeJobsRequestTypeDef(TypedDict):
    filters: NotRequired[DescribeJobsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    accountID: NotRequired[str]


class DescribeReplicationConfigurationTemplatesResponseTypeDef(TypedDict):
    items: list[ReplicationConfigurationTemplateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DescribeSourceServersRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[DescribeSourceServersRequestFiltersTypeDef]
    accountID: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSourceServersRequestTypeDef(TypedDict):
    filters: NotRequired[DescribeSourceServersRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    accountID: NotRequired[str]


class DescribeVcenterClientsResponseTypeDef(TypedDict):
    items: list[VcenterClientTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ExportTaskErrorTypeDef(TypedDict):
    errorDateTime: NotRequired[str]
    errorData: NotRequired[ExportErrorDataTypeDef]


class ExportTaskTypeDef(TypedDict):
    exportID: NotRequired[str]
    arn: NotRequired[str]
    s3Bucket: NotRequired[str]
    s3Key: NotRequired[str]
    s3BucketOwner: NotRequired[str]
    creationDateTime: NotRequired[str]
    endDateTime: NotRequired[str]
    status: NotRequired[ExportStatusType]
    progressPercentage: NotRequired[float]
    summary: NotRequired[ExportTaskSummaryTypeDef]
    tags: NotRequired[dict[str, str]]


class ImportTaskErrorTypeDef(TypedDict):
    errorDateTime: NotRequired[str]
    errorType: NotRequired[ImportErrorTypeType]
    errorData: NotRequired[ImportErrorDataTypeDef]


class ImportTaskSummaryTypeDef(TypedDict):
    waves: NotRequired[ImportTaskSummaryWavesTypeDef]
    applications: NotRequired[ImportTaskSummaryApplicationsTypeDef]
    servers: NotRequired[ImportTaskSummaryServersTypeDef]


class StartImportRequestTypeDef(TypedDict):
    s3BucketSource: S3BucketSourceTypeDef
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class JobLogTypeDef(TypedDict):
    logDateTime: NotRequired[str]
    event: NotRequired[JobLogEventType]
    eventData: NotRequired[JobLogEventDataTypeDef]


class LifeCycleLastCutoverTypeDef(TypedDict):
    initiated: NotRequired[LifeCycleLastCutoverInitiatedTypeDef]
    reverted: NotRequired[LifeCycleLastCutoverRevertedTypeDef]
    finalized: NotRequired[LifeCycleLastCutoverFinalizedTypeDef]


class LifeCycleLastTestTypeDef(TypedDict):
    initiated: NotRequired[LifeCycleLastTestInitiatedTypeDef]
    reverted: NotRequired[LifeCycleLastTestRevertedTypeDef]
    finalized: NotRequired[LifeCycleLastTestFinalizedTypeDef]


class ListApplicationsRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[ListApplicationsRequestFiltersTypeDef]
    accountID: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListApplicationsRequestTypeDef(TypedDict):
    filters: NotRequired[ListApplicationsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    accountID: NotRequired[str]


class ListConnectorsRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[ListConnectorsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListConnectorsRequestTypeDef(TypedDict):
    filters: NotRequired[ListConnectorsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListExportsRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[ListExportsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListExportsRequestTypeDef(TypedDict):
    filters: NotRequired[ListExportsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListImportsRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[ListImportsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImportsRequestTypeDef(TypedDict):
    filters: NotRequired[ListImportsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListManagedAccountsResponseTypeDef(TypedDict):
    items: list[ManagedAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSourceServerActionsRequestPaginateTypeDef(TypedDict):
    sourceServerID: str
    filters: NotRequired[SourceServerActionsRequestFiltersTypeDef]
    accountID: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSourceServerActionsRequestTypeDef(TypedDict):
    sourceServerID: str
    filters: NotRequired[SourceServerActionsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    accountID: NotRequired[str]


class ListTemplateActionsRequestPaginateTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    filters: NotRequired[TemplateActionsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTemplateActionsRequestTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    filters: NotRequired[TemplateActionsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListWavesRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[ListWavesRequestFiltersTypeDef]
    accountID: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWavesRequestTypeDef(TypedDict):
    filters: NotRequired[ListWavesRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    accountID: NotRequired[str]


class SourcePropertiesTypeDef(TypedDict):
    lastUpdatedDateTime: NotRequired[str]
    recommendedInstanceType: NotRequired[str]
    identificationHints: NotRequired[IdentificationHintsTypeDef]
    networkInterfaces: NotRequired[list[NetworkInterfaceTypeDef]]
    disks: NotRequired[list[DiskTypeDef]]
    cpus: NotRequired[list[CPUTypeDef]]
    ramBytes: NotRequired[int]
    os: NotRequired[OSTypeDef]


class PutSourceServerActionRequestTypeDef(TypedDict):
    sourceServerID: str
    actionName: str
    documentIdentifier: str
    order: int
    actionID: str
    documentVersion: NotRequired[str]
    active: NotRequired[bool]
    timeoutSeconds: NotRequired[int]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]]]
    externalParameters: NotRequired[Mapping[str, SsmExternalParameterTypeDef]]
    description: NotRequired[str]
    category: NotRequired[ActionCategoryType]
    accountID: NotRequired[str]


class PutTemplateActionRequestTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    actionName: str
    documentIdentifier: str
    order: int
    actionID: str
    documentVersion: NotRequired[str]
    active: NotRequired[bool]
    timeoutSeconds: NotRequired[int]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]]]
    operatingSystem: NotRequired[str]
    externalParameters: NotRequired[Mapping[str, SsmExternalParameterTypeDef]]
    description: NotRequired[str]
    category: NotRequired[ActionCategoryType]


class SourceServerActionDocumentResponseTypeDef(TypedDict):
    actionID: str
    actionName: str
    documentIdentifier: str
    order: int
    documentVersion: str
    active: bool
    timeoutSeconds: int
    mustSucceedForCutover: bool
    parameters: dict[str, list[SsmParameterStoreParameterTypeDef]]
    externalParameters: dict[str, SsmExternalParameterTypeDef]
    description: str
    category: ActionCategoryType
    ResponseMetadata: ResponseMetadataTypeDef


class SourceServerActionDocumentTypeDef(TypedDict):
    actionID: NotRequired[str]
    actionName: NotRequired[str]
    documentIdentifier: NotRequired[str]
    order: NotRequired[int]
    documentVersion: NotRequired[str]
    active: NotRequired[bool]
    timeoutSeconds: NotRequired[int]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[dict[str, list[SsmParameterStoreParameterTypeDef]]]
    externalParameters: NotRequired[dict[str, SsmExternalParameterTypeDef]]
    description: NotRequired[str]
    category: NotRequired[ActionCategoryType]


class SsmDocumentOutputTypeDef(TypedDict):
    actionName: str
    ssmDocumentName: str
    timeoutSeconds: NotRequired[int]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[dict[str, list[SsmParameterStoreParameterTypeDef]]]
    externalParameters: NotRequired[dict[str, SsmExternalParameterTypeDef]]


class SsmDocumentTypeDef(TypedDict):
    actionName: str
    ssmDocumentName: str
    timeoutSeconds: NotRequired[int]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]]]
    externalParameters: NotRequired[Mapping[str, SsmExternalParameterTypeDef]]


class TemplateActionDocumentResponseTypeDef(TypedDict):
    actionID: str
    actionName: str
    documentIdentifier: str
    order: int
    documentVersion: str
    active: bool
    timeoutSeconds: int
    mustSucceedForCutover: bool
    parameters: dict[str, list[SsmParameterStoreParameterTypeDef]]
    operatingSystem: str
    externalParameters: dict[str, SsmExternalParameterTypeDef]
    description: str
    category: ActionCategoryType
    ResponseMetadata: ResponseMetadataTypeDef


class TemplateActionDocumentTypeDef(TypedDict):
    actionID: NotRequired[str]
    actionName: NotRequired[str]
    documentIdentifier: NotRequired[str]
    order: NotRequired[int]
    documentVersion: NotRequired[str]
    active: NotRequired[bool]
    timeoutSeconds: NotRequired[int]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[dict[str, list[SsmParameterStoreParameterTypeDef]]]
    operatingSystem: NotRequired[str]
    externalParameters: NotRequired[dict[str, SsmExternalParameterTypeDef]]
    description: NotRequired[str]
    category: NotRequired[ActionCategoryType]


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
    useFipsEndpoint: bool
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
    useFipsEndpoint: NotRequired[bool]
    accountID: NotRequired[str]
    internetProtocol: NotRequired[InternetProtocolType]


class UpdateSourceServerRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]
    connectorAction: NotRequired[SourceServerConnectorActionTypeDef]


class WaveResponseTypeDef(TypedDict):
    waveID: str
    arn: str
    name: str
    description: str
    isArchived: bool
    waveAggregatedStatus: WaveAggregatedStatusTypeDef
    creationDateTime: str
    lastModifiedDateTime: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class WaveTypeDef(TypedDict):
    waveID: NotRequired[str]
    arn: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    isArchived: NotRequired[bool]
    waveAggregatedStatus: NotRequired[WaveAggregatedStatusTypeDef]
    creationDateTime: NotRequired[str]
    lastModifiedDateTime: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class ListApplicationsResponseTypeDef(TypedDict):
    items: list[ApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListConnectorsResponseTypeDef(TypedDict):
    items: list[ConnectorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DataReplicationInfoTypeDef(TypedDict):
    lagDuration: NotRequired[str]
    etaDateTime: NotRequired[str]
    replicatedDisks: NotRequired[list[DataReplicationInfoReplicatedDiskTypeDef]]
    dataReplicationState: NotRequired[DataReplicationStateType]
    dataReplicationInitiation: NotRequired[DataReplicationInitiationTypeDef]
    dataReplicationError: NotRequired[DataReplicationErrorTypeDef]
    lastSnapshotDateTime: NotRequired[str]
    replicatorId: NotRequired[str]


class ListExportErrorsResponseTypeDef(TypedDict):
    items: list[ExportTaskErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListExportsResponseTypeDef(TypedDict):
    items: list[ExportTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartExportResponseTypeDef(TypedDict):
    exportTask: ExportTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListImportErrorsResponseTypeDef(TypedDict):
    items: list[ImportTaskErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ImportTaskTypeDef(TypedDict):
    importID: NotRequired[str]
    arn: NotRequired[str]
    s3BucketSource: NotRequired[S3BucketSourceTypeDef]
    creationDateTime: NotRequired[str]
    endDateTime: NotRequired[str]
    status: NotRequired[ImportStatusType]
    progressPercentage: NotRequired[float]
    summary: NotRequired[ImportTaskSummaryTypeDef]
    tags: NotRequired[dict[str, str]]


class DescribeJobLogItemsResponseTypeDef(TypedDict):
    items: list[JobLogTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class LifeCycleTypeDef(TypedDict):
    addedToServiceDateTime: NotRequired[str]
    firstByteDateTime: NotRequired[str]
    elapsedReplicationDuration: NotRequired[str]
    lastSeenByServiceDateTime: NotRequired[str]
    lastTest: NotRequired[LifeCycleLastTestTypeDef]
    lastCutover: NotRequired[LifeCycleLastCutoverTypeDef]
    state: NotRequired[LifeCycleStateType]


class ListSourceServerActionsResponseTypeDef(TypedDict):
    items: list[SourceServerActionDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class JobPostLaunchActionsLaunchStatusTypeDef(TypedDict):
    ssmDocument: NotRequired[SsmDocumentOutputTypeDef]
    ssmDocumentType: NotRequired[SsmDocumentTypeType]
    executionID: NotRequired[str]
    executionStatus: NotRequired[PostLaunchActionExecutionStatusType]
    failureReason: NotRequired[str]


class PostLaunchActionsOutputTypeDef(TypedDict):
    deployment: NotRequired[PostLaunchActionsDeploymentTypeType]
    s3LogBucket: NotRequired[str]
    s3OutputKeyPrefix: NotRequired[str]
    cloudWatchLogGroupName: NotRequired[str]
    ssmDocuments: NotRequired[list[SsmDocumentOutputTypeDef]]


class PostLaunchActionsTypeDef(TypedDict):
    deployment: NotRequired[PostLaunchActionsDeploymentTypeType]
    s3LogBucket: NotRequired[str]
    s3OutputKeyPrefix: NotRequired[str]
    cloudWatchLogGroupName: NotRequired[str]
    ssmDocuments: NotRequired[Sequence[SsmDocumentTypeDef]]


class ListTemplateActionsResponseTypeDef(TypedDict):
    items: list[TemplateActionDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListWavesResponseTypeDef(TypedDict):
    items: list[WaveTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListImportsResponseTypeDef(TypedDict):
    items: list[ImportTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartImportResponseTypeDef(TypedDict):
    importTask: ImportTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SourceServerResponseTypeDef(TypedDict):
    sourceServerID: str
    arn: str
    isArchived: bool
    tags: dict[str, str]
    launchedInstance: LaunchedInstanceTypeDef
    dataReplicationInfo: DataReplicationInfoTypeDef
    lifeCycle: LifeCycleTypeDef
    sourceProperties: SourcePropertiesTypeDef
    replicationType: ReplicationTypeType
    vcenterClientID: str
    applicationID: str
    userProvidedID: str
    fqdnForActionFramework: str
    connectorAction: SourceServerConnectorActionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SourceServerTypeDef(TypedDict):
    sourceServerID: NotRequired[str]
    arn: NotRequired[str]
    isArchived: NotRequired[bool]
    tags: NotRequired[dict[str, str]]
    launchedInstance: NotRequired[LaunchedInstanceTypeDef]
    dataReplicationInfo: NotRequired[DataReplicationInfoTypeDef]
    lifeCycle: NotRequired[LifeCycleTypeDef]
    sourceProperties: NotRequired[SourcePropertiesTypeDef]
    replicationType: NotRequired[ReplicationTypeType]
    vcenterClientID: NotRequired[str]
    applicationID: NotRequired[str]
    userProvidedID: NotRequired[str]
    fqdnForActionFramework: NotRequired[str]
    connectorAction: NotRequired[SourceServerConnectorActionTypeDef]


class PostLaunchActionsStatusTypeDef(TypedDict):
    ssmAgentDiscoveryDatetime: NotRequired[str]
    postLaunchActionsLaunchStatusList: NotRequired[list[JobPostLaunchActionsLaunchStatusTypeDef]]


class LaunchConfigurationTemplateResponseTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    arn: str
    postLaunchActions: PostLaunchActionsOutputTypeDef
    enableMapAutoTagging: bool
    mapAutoTaggingMpeID: str
    tags: dict[str, str]
    ec2LaunchTemplateID: str
    launchDisposition: LaunchDispositionType
    targetInstanceTypeRightSizingMethod: TargetInstanceTypeRightSizingMethodType
    copyPrivateIp: bool
    associatePublicIpAddress: bool
    copyTags: bool
    licensing: LicensingTypeDef
    bootMode: BootModeType
    smallVolumeMaxSize: int
    smallVolumeConf: LaunchTemplateDiskConfTypeDef
    largeVolumeConf: LaunchTemplateDiskConfTypeDef
    enableParametersEncryption: bool
    parametersEncryptionKey: str
    ResponseMetadata: ResponseMetadataTypeDef


class LaunchConfigurationTemplateTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    arn: NotRequired[str]
    postLaunchActions: NotRequired[PostLaunchActionsOutputTypeDef]
    enableMapAutoTagging: NotRequired[bool]
    mapAutoTaggingMpeID: NotRequired[str]
    tags: NotRequired[dict[str, str]]
    ec2LaunchTemplateID: NotRequired[str]
    launchDisposition: NotRequired[LaunchDispositionType]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]
    copyPrivateIp: NotRequired[bool]
    associatePublicIpAddress: NotRequired[bool]
    copyTags: NotRequired[bool]
    licensing: NotRequired[LicensingTypeDef]
    bootMode: NotRequired[BootModeType]
    smallVolumeMaxSize: NotRequired[int]
    smallVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    largeVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    enableParametersEncryption: NotRequired[bool]
    parametersEncryptionKey: NotRequired[str]


class LaunchConfigurationTypeDef(TypedDict):
    sourceServerID: str
    name: str
    ec2LaunchTemplateID: str
    launchDisposition: LaunchDispositionType
    targetInstanceTypeRightSizingMethod: TargetInstanceTypeRightSizingMethodType
    copyPrivateIp: bool
    copyTags: bool
    licensing: LicensingTypeDef
    bootMode: BootModeType
    postLaunchActions: PostLaunchActionsOutputTypeDef
    enableMapAutoTagging: bool
    mapAutoTaggingMpeID: str
    ResponseMetadata: ResponseMetadataTypeDef


PostLaunchActionsUnionTypeDef = Union[PostLaunchActionsTypeDef, PostLaunchActionsOutputTypeDef]


class DescribeSourceServersResponseTypeDef(TypedDict):
    items: list[SourceServerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ParticipatingServerTypeDef(TypedDict):
    sourceServerID: str
    launchStatus: NotRequired[LaunchStatusType]
    launchedEc2InstanceID: NotRequired[str]
    postLaunchActionsStatus: NotRequired[PostLaunchActionsStatusTypeDef]


class DescribeLaunchConfigurationTemplatesResponseTypeDef(TypedDict):
    items: list[LaunchConfigurationTemplateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateLaunchConfigurationTemplateRequestTypeDef(TypedDict):
    postLaunchActions: NotRequired[PostLaunchActionsUnionTypeDef]
    enableMapAutoTagging: NotRequired[bool]
    mapAutoTaggingMpeID: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    launchDisposition: NotRequired[LaunchDispositionType]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]
    copyPrivateIp: NotRequired[bool]
    associatePublicIpAddress: NotRequired[bool]
    copyTags: NotRequired[bool]
    licensing: NotRequired[LicensingTypeDef]
    bootMode: NotRequired[BootModeType]
    smallVolumeMaxSize: NotRequired[int]
    smallVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    largeVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    enableParametersEncryption: NotRequired[bool]
    parametersEncryptionKey: NotRequired[str]


class UpdateLaunchConfigurationRequestTypeDef(TypedDict):
    sourceServerID: str
    name: NotRequired[str]
    launchDisposition: NotRequired[LaunchDispositionType]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    licensing: NotRequired[LicensingTypeDef]
    bootMode: NotRequired[BootModeType]
    postLaunchActions: NotRequired[PostLaunchActionsUnionTypeDef]
    enableMapAutoTagging: NotRequired[bool]
    mapAutoTaggingMpeID: NotRequired[str]
    accountID: NotRequired[str]


class UpdateLaunchConfigurationTemplateRequestTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    postLaunchActions: NotRequired[PostLaunchActionsUnionTypeDef]
    enableMapAutoTagging: NotRequired[bool]
    mapAutoTaggingMpeID: NotRequired[str]
    launchDisposition: NotRequired[LaunchDispositionType]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]
    copyPrivateIp: NotRequired[bool]
    associatePublicIpAddress: NotRequired[bool]
    copyTags: NotRequired[bool]
    licensing: NotRequired[LicensingTypeDef]
    bootMode: NotRequired[BootModeType]
    smallVolumeMaxSize: NotRequired[int]
    smallVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    largeVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    enableParametersEncryption: NotRequired[bool]
    parametersEncryptionKey: NotRequired[str]


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
    },
)


class DescribeJobsResponseTypeDef(TypedDict):
    items: list[JobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartCutoverResponseTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartTestResponseTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TerminateTargetInstancesResponseTypeDef(TypedDict):
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
