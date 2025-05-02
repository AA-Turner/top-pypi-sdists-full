"""
Type annotations for mgn service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_mgn/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_mgn.type_defs import ApplicationAggregatedStatusTypeDef

    data: ApplicationAggregatedStatusTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
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
    TargetInstanceTypeRightSizingMethodType,
    VolumeTypeType,
    WaveHealthStatusType,
    WaveProgressStatusType,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


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
    healthStatus: NotRequired[ApplicationHealthStatusType]
    lastUpdateDateTime: NotRequired[str]
    progressStatus: NotRequired[ApplicationProgressStatusType]
    totalSourceServers: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ArchiveApplicationRequestTypeDef(TypedDict):
    applicationID: str
    accountID: NotRequired[str]


class ArchiveWaveRequestTypeDef(TypedDict):
    waveID: str
    accountID: NotRequired[str]


class AssociateApplicationsRequestTypeDef(TypedDict):
    applicationIDs: Sequence[str]
    waveID: str
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
    cloudWatchOutputEnabled: bool
    s3OutputEnabled: bool
    cloudWatchLogGroupName: NotRequired[str]
    outputS3BucketName: NotRequired[str]


class CreateApplicationRequestTypeDef(TypedDict):
    name: str
    accountID: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class LaunchTemplateDiskConfTypeDef(TypedDict):
    iops: NotRequired[int]
    throughput: NotRequired[int]
    volumeType: NotRequired[VolumeTypeType]


class LicensingTypeDef(TypedDict):
    osByol: NotRequired[bool]


class CreateReplicationConfigurationTemplateRequestTypeDef(TypedDict):
    associateDefaultSecurityGroup: bool
    bandwidthThrottling: int
    createPublicIP: bool
    dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType
    defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ebsEncryption: ReplicationConfigurationEbsEncryptionType
    replicationServerInstanceType: str
    replicationServersSecurityGroupsIDs: Sequence[str]
    stagingAreaSubnetId: str
    stagingAreaTags: Mapping[str, str]
    useDedicatedReplicationServer: bool
    ebsEncryptionKeyArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    useFipsEndpoint: NotRequired[bool]


class CreateWaveRequestTypeDef(TypedDict):
    name: str
    accountID: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class DataReplicationErrorTypeDef(TypedDict):
    error: NotRequired[DataReplicationErrorStringType]
    rawError: NotRequired[str]


class DataReplicationInfoReplicatedDiskTypeDef(TypedDict):
    backloggedStorageBytes: NotRequired[int]
    deviceName: NotRequired[str]
    replicatedStorageBytes: NotRequired[int]
    rescannedStorageBytes: NotRequired[int]
    totalStorageBytes: NotRequired[int]


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
    accountID: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeJobsRequestFiltersTypeDef(TypedDict):
    fromDate: NotRequired[str]
    jobIDs: NotRequired[Sequence[str]]
    toDate: NotRequired[str]


class DescribeLaunchConfigurationTemplatesRequestTypeDef(TypedDict):
    launchConfigurationTemplateIDs: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeReplicationConfigurationTemplatesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    replicationConfigurationTemplateIDs: NotRequired[Sequence[str]]


class ReplicationConfigurationTemplateTypeDef(TypedDict):
    replicationConfigurationTemplateID: str
    arn: NotRequired[str]
    associateDefaultSecurityGroup: NotRequired[bool]
    bandwidthThrottling: NotRequired[int]
    createPublicIP: NotRequired[bool]
    dataPlaneRouting: NotRequired[ReplicationConfigurationDataPlaneRoutingType]
    defaultLargeStagingDiskType: NotRequired[
        ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ]
    ebsEncryption: NotRequired[ReplicationConfigurationEbsEncryptionType]
    ebsEncryptionKeyArn: NotRequired[str]
    replicationServerInstanceType: NotRequired[str]
    replicationServersSecurityGroupsIDs: NotRequired[List[str]]
    stagingAreaSubnetId: NotRequired[str]
    stagingAreaTags: NotRequired[Dict[str, str]]
    tags: NotRequired[Dict[str, str]]
    useDedicatedReplicationServer: NotRequired[bool]
    useFipsEndpoint: NotRequired[bool]


class DescribeSourceServersRequestFiltersTypeDef(TypedDict):
    applicationIDs: NotRequired[Sequence[str]]
    isArchived: NotRequired[bool]
    lifeCycleStates: NotRequired[Sequence[LifeCycleStateType]]
    replicationTypes: NotRequired[Sequence[ReplicationTypeType]]
    sourceServerIDs: NotRequired[Sequence[str]]


class DescribeVcenterClientsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class VcenterClientTypeDef(TypedDict):
    arn: NotRequired[str]
    datacenterName: NotRequired[str]
    hostname: NotRequired[str]
    lastSeenDatetime: NotRequired[str]
    sourceServerTags: NotRequired[Dict[str, str]]
    tags: NotRequired[Dict[str, str]]
    vcenterClientID: NotRequired[str]
    vcenterUUID: NotRequired[str]


class DisassociateApplicationsRequestTypeDef(TypedDict):
    applicationIDs: Sequence[str]
    waveID: str
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
        "bytes": NotRequired[int],
        "deviceName": NotRequired[str],
    },
)


class ExportErrorDataTypeDef(TypedDict):
    rawError: NotRequired[str]


class ExportTaskSummaryTypeDef(TypedDict):
    applicationsCount: NotRequired[int]
    serversCount: NotRequired[int]
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
    awsInstanceID: NotRequired[str]
    fqdn: NotRequired[str]
    hostname: NotRequired[str]
    vmPath: NotRequired[str]
    vmWareUuid: NotRequired[str]


class ImportErrorDataTypeDef(TypedDict):
    accountID: NotRequired[str]
    applicationID: NotRequired[str]
    ec2LaunchTemplateID: NotRequired[str]
    rawError: NotRequired[str]
    rowNumber: NotRequired[int]
    sourceServerID: NotRequired[str]
    waveID: NotRequired[str]


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
    conversionServerID: NotRequired[str]
    rawError: NotRequired[str]
    sourceServerID: NotRequired[str]
    targetInstanceID: NotRequired[str]


class LaunchedInstanceTypeDef(TypedDict):
    ec2InstanceID: NotRequired[str]
    firstBoot: NotRequired[FirstBootType]
    jobID: NotRequired[str]


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
    isArchived: NotRequired[bool]
    waveIDs: NotRequired[Sequence[str]]


class MarkAsArchivedRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class NetworkInterfaceTypeDef(TypedDict):
    ips: NotRequired[List[str]]
    isPrimary: NotRequired[bool]
    macAddress: NotRequired[str]


class OSTypeDef(TypedDict):
    fullString: NotRequired[str]


class PauseReplicationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class SsmExternalParameterTypeDef(TypedDict):
    dynamicPath: NotRequired[str]


class SsmParameterStoreParameterTypeDef(TypedDict):
    parameterName: str
    parameterType: Literal["STRING"]


class RemoveSourceServerActionRequestTypeDef(TypedDict):
    actionID: str
    sourceServerID: str
    accountID: NotRequired[str]


class RemoveTemplateActionRequestTypeDef(TypedDict):
    actionID: str
    launchConfigurationTemplateID: str


class ReplicationConfigurationReplicatedDiskTypeDef(TypedDict):
    deviceName: NotRequired[str]
    iops: NotRequired[int]
    isBootDisk: NotRequired[bool]
    stagingDiskType: NotRequired[ReplicationConfigurationReplicatedDiskStagingDiskTypeType]
    throughput: NotRequired[int]


class ResumeReplicationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class RetryDataReplicationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class SourceServerConnectorActionTypeDef(TypedDict):
    connectorArn: NotRequired[str]
    credentialsSecretArn: NotRequired[str]


class StartCutoverRequestTypeDef(TypedDict):
    sourceServerIDs: Sequence[str]
    accountID: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class StartExportRequestTypeDef(TypedDict):
    s3Bucket: str
    s3Key: str
    s3BucketOwner: NotRequired[str]


class StartReplicationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class StartTestRequestTypeDef(TypedDict):
    sourceServerIDs: Sequence[str]
    accountID: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class StopReplicationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class TerminateTargetInstancesRequestTypeDef(TypedDict):
    sourceServerIDs: Sequence[str]
    accountID: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


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
    accountID: NotRequired[str]
    description: NotRequired[str]
    name: NotRequired[str]


class UpdateReplicationConfigurationTemplateRequestTypeDef(TypedDict):
    replicationConfigurationTemplateID: str
    arn: NotRequired[str]
    associateDefaultSecurityGroup: NotRequired[bool]
    bandwidthThrottling: NotRequired[int]
    createPublicIP: NotRequired[bool]
    dataPlaneRouting: NotRequired[ReplicationConfigurationDataPlaneRoutingType]
    defaultLargeStagingDiskType: NotRequired[
        ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ]
    ebsEncryption: NotRequired[ReplicationConfigurationEbsEncryptionType]
    ebsEncryptionKeyArn: NotRequired[str]
    replicationServerInstanceType: NotRequired[str]
    replicationServersSecurityGroupsIDs: NotRequired[Sequence[str]]
    stagingAreaSubnetId: NotRequired[str]
    stagingAreaTags: NotRequired[Mapping[str, str]]
    useDedicatedReplicationServer: NotRequired[bool]
    useFipsEndpoint: NotRequired[bool]


class UpdateSourceServerReplicationTypeRequestTypeDef(TypedDict):
    replicationType: ReplicationTypeType
    sourceServerID: str
    accountID: NotRequired[str]


class UpdateWaveRequestTypeDef(TypedDict):
    waveID: str
    accountID: NotRequired[str]
    description: NotRequired[str]
    name: NotRequired[str]


class WaveAggregatedStatusTypeDef(TypedDict):
    healthStatus: NotRequired[WaveHealthStatusType]
    lastUpdateDateTime: NotRequired[str]
    progressStatus: NotRequired[WaveProgressStatusType]
    replicationStartedDateTime: NotRequired[str]
    totalApplications: NotRequired[int]


class ApplicationTypeDef(TypedDict):
    applicationAggregatedStatus: NotRequired[ApplicationAggregatedStatusTypeDef]
    applicationID: NotRequired[str]
    arn: NotRequired[str]
    creationDateTime: NotRequired[str]
    description: NotRequired[str]
    isArchived: NotRequired[bool]
    lastModifiedDateTime: NotRequired[str]
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    waveID: NotRequired[str]


class ApplicationResponseTypeDef(TypedDict):
    applicationAggregatedStatus: ApplicationAggregatedStatusTypeDef
    applicationID: str
    arn: str
    creationDateTime: str
    description: str
    isArchived: bool
    lastModifiedDateTime: str
    name: str
    tags: Dict[str, str]
    waveID: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ReplicationConfigurationTemplateResponseTypeDef(TypedDict):
    arn: str
    associateDefaultSecurityGroup: bool
    bandwidthThrottling: int
    createPublicIP: bool
    dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType
    defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ebsEncryption: ReplicationConfigurationEbsEncryptionType
    ebsEncryptionKeyArn: str
    replicationConfigurationTemplateID: str
    replicationServerInstanceType: str
    replicationServersSecurityGroupsIDs: List[str]
    stagingAreaSubnetId: str
    stagingAreaTags: Dict[str, str]
    tags: Dict[str, str]
    useDedicatedReplicationServer: bool
    useFipsEndpoint: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ChangeServerLifeCycleStateRequestTypeDef(TypedDict):
    lifeCycle: ChangeServerLifeCycleStateSourceServerLifecycleTypeDef
    sourceServerID: str
    accountID: NotRequired[str]


class ConnectorResponseTypeDef(TypedDict):
    arn: str
    connectorID: str
    name: str
    ssmCommandConfig: ConnectorSsmCommandConfigTypeDef
    ssmInstanceID: str
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ConnectorTypeDef(TypedDict):
    arn: NotRequired[str]
    connectorID: NotRequired[str]
    name: NotRequired[str]
    ssmCommandConfig: NotRequired[ConnectorSsmCommandConfigTypeDef]
    ssmInstanceID: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class CreateConnectorRequestTypeDef(TypedDict):
    name: str
    ssmInstanceID: str
    ssmCommandConfig: NotRequired[ConnectorSsmCommandConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]


class UpdateConnectorRequestTypeDef(TypedDict):
    connectorID: str
    name: NotRequired[str]
    ssmCommandConfig: NotRequired[ConnectorSsmCommandConfigTypeDef]


class DataReplicationInitiationTypeDef(TypedDict):
    nextAttemptDateTime: NotRequired[str]
    startDateTime: NotRequired[str]
    steps: NotRequired[List[DataReplicationInitiationStepTypeDef]]


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
    accountID: NotRequired[str]
    filters: NotRequired[DescribeJobsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeJobsRequestTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[DescribeJobsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeReplicationConfigurationTemplatesResponseTypeDef(TypedDict):
    items: List[ReplicationConfigurationTemplateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DescribeSourceServersRequestPaginateTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[DescribeSourceServersRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSourceServersRequestTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[DescribeSourceServersRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescribeVcenterClientsResponseTypeDef(TypedDict):
    items: List[VcenterClientTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ExportTaskErrorTypeDef(TypedDict):
    errorData: NotRequired[ExportErrorDataTypeDef]
    errorDateTime: NotRequired[str]


class ExportTaskTypeDef(TypedDict):
    creationDateTime: NotRequired[str]
    endDateTime: NotRequired[str]
    exportID: NotRequired[str]
    progressPercentage: NotRequired[float]
    s3Bucket: NotRequired[str]
    s3BucketOwner: NotRequired[str]
    s3Key: NotRequired[str]
    status: NotRequired[ExportStatusType]
    summary: NotRequired[ExportTaskSummaryTypeDef]


class ImportTaskErrorTypeDef(TypedDict):
    errorData: NotRequired[ImportErrorDataTypeDef]
    errorDateTime: NotRequired[str]
    errorType: NotRequired[ImportErrorTypeType]


class ImportTaskSummaryTypeDef(TypedDict):
    applications: NotRequired[ImportTaskSummaryApplicationsTypeDef]
    servers: NotRequired[ImportTaskSummaryServersTypeDef]
    waves: NotRequired[ImportTaskSummaryWavesTypeDef]


class StartImportRequestTypeDef(TypedDict):
    s3BucketSource: S3BucketSourceTypeDef
    clientToken: NotRequired[str]


class JobLogTypeDef(TypedDict):
    event: NotRequired[JobLogEventType]
    eventData: NotRequired[JobLogEventDataTypeDef]
    logDateTime: NotRequired[str]


class LifeCycleLastCutoverTypeDef(TypedDict):
    finalized: NotRequired[LifeCycleLastCutoverFinalizedTypeDef]
    initiated: NotRequired[LifeCycleLastCutoverInitiatedTypeDef]
    reverted: NotRequired[LifeCycleLastCutoverRevertedTypeDef]


class LifeCycleLastTestTypeDef(TypedDict):
    finalized: NotRequired[LifeCycleLastTestFinalizedTypeDef]
    initiated: NotRequired[LifeCycleLastTestInitiatedTypeDef]
    reverted: NotRequired[LifeCycleLastTestRevertedTypeDef]


class ListApplicationsRequestPaginateTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[ListApplicationsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListApplicationsRequestTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[ListApplicationsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


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
    items: List[ManagedAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSourceServerActionsRequestPaginateTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]
    filters: NotRequired[SourceServerActionsRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSourceServerActionsRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]
    filters: NotRequired[SourceServerActionsRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


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
    accountID: NotRequired[str]
    filters: NotRequired[ListWavesRequestFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWavesRequestTypeDef(TypedDict):
    accountID: NotRequired[str]
    filters: NotRequired[ListWavesRequestFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SourcePropertiesTypeDef(TypedDict):
    cpus: NotRequired[List[CPUTypeDef]]
    disks: NotRequired[List[DiskTypeDef]]
    identificationHints: NotRequired[IdentificationHintsTypeDef]
    lastUpdatedDateTime: NotRequired[str]
    networkInterfaces: NotRequired[List[NetworkInterfaceTypeDef]]
    os: NotRequired[OSTypeDef]
    ramBytes: NotRequired[int]
    recommendedInstanceType: NotRequired[str]


class PutSourceServerActionRequestTypeDef(TypedDict):
    actionID: str
    actionName: str
    documentIdentifier: str
    order: int
    sourceServerID: str
    accountID: NotRequired[str]
    active: NotRequired[bool]
    category: NotRequired[ActionCategoryType]
    description: NotRequired[str]
    documentVersion: NotRequired[str]
    externalParameters: NotRequired[Mapping[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]


class PutTemplateActionRequestTypeDef(TypedDict):
    actionID: str
    actionName: str
    documentIdentifier: str
    launchConfigurationTemplateID: str
    order: int
    active: NotRequired[bool]
    category: NotRequired[ActionCategoryType]
    description: NotRequired[str]
    documentVersion: NotRequired[str]
    externalParameters: NotRequired[Mapping[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    operatingSystem: NotRequired[str]
    parameters: NotRequired[Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]


class SourceServerActionDocumentResponseTypeDef(TypedDict):
    actionID: str
    actionName: str
    active: bool
    category: ActionCategoryType
    description: str
    documentIdentifier: str
    documentVersion: str
    externalParameters: Dict[str, SsmExternalParameterTypeDef]
    mustSucceedForCutover: bool
    order: int
    parameters: Dict[str, List[SsmParameterStoreParameterTypeDef]]
    timeoutSeconds: int
    ResponseMetadata: ResponseMetadataTypeDef


class SourceServerActionDocumentTypeDef(TypedDict):
    actionID: NotRequired[str]
    actionName: NotRequired[str]
    active: NotRequired[bool]
    category: NotRequired[ActionCategoryType]
    description: NotRequired[str]
    documentIdentifier: NotRequired[str]
    documentVersion: NotRequired[str]
    externalParameters: NotRequired[Dict[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    order: NotRequired[int]
    parameters: NotRequired[Dict[str, List[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]


class SsmDocumentOutputTypeDef(TypedDict):
    actionName: str
    ssmDocumentName: str
    externalParameters: NotRequired[Dict[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[Dict[str, List[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]


class SsmDocumentTypeDef(TypedDict):
    actionName: str
    ssmDocumentName: str
    externalParameters: NotRequired[Mapping[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    parameters: NotRequired[Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]


class TemplateActionDocumentResponseTypeDef(TypedDict):
    actionID: str
    actionName: str
    active: bool
    category: ActionCategoryType
    description: str
    documentIdentifier: str
    documentVersion: str
    externalParameters: Dict[str, SsmExternalParameterTypeDef]
    mustSucceedForCutover: bool
    operatingSystem: str
    order: int
    parameters: Dict[str, List[SsmParameterStoreParameterTypeDef]]
    timeoutSeconds: int
    ResponseMetadata: ResponseMetadataTypeDef


class TemplateActionDocumentTypeDef(TypedDict):
    actionID: NotRequired[str]
    actionName: NotRequired[str]
    active: NotRequired[bool]
    category: NotRequired[ActionCategoryType]
    description: NotRequired[str]
    documentIdentifier: NotRequired[str]
    documentVersion: NotRequired[str]
    externalParameters: NotRequired[Dict[str, SsmExternalParameterTypeDef]]
    mustSucceedForCutover: NotRequired[bool]
    operatingSystem: NotRequired[str]
    order: NotRequired[int]
    parameters: NotRequired[Dict[str, List[SsmParameterStoreParameterTypeDef]]]
    timeoutSeconds: NotRequired[int]


class ReplicationConfigurationTypeDef(TypedDict):
    associateDefaultSecurityGroup: bool
    bandwidthThrottling: int
    createPublicIP: bool
    dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType
    defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ebsEncryption: ReplicationConfigurationEbsEncryptionType
    ebsEncryptionKeyArn: str
    name: str
    replicatedDisks: List[ReplicationConfigurationReplicatedDiskTypeDef]
    replicationServerInstanceType: str
    replicationServersSecurityGroupsIDs: List[str]
    sourceServerID: str
    stagingAreaSubnetId: str
    stagingAreaTags: Dict[str, str]
    useDedicatedReplicationServer: bool
    useFipsEndpoint: bool
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateReplicationConfigurationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]
    associateDefaultSecurityGroup: NotRequired[bool]
    bandwidthThrottling: NotRequired[int]
    createPublicIP: NotRequired[bool]
    dataPlaneRouting: NotRequired[ReplicationConfigurationDataPlaneRoutingType]
    defaultLargeStagingDiskType: NotRequired[
        ReplicationConfigurationDefaultLargeStagingDiskTypeType
    ]
    ebsEncryption: NotRequired[ReplicationConfigurationEbsEncryptionType]
    ebsEncryptionKeyArn: NotRequired[str]
    name: NotRequired[str]
    replicatedDisks: NotRequired[Sequence[ReplicationConfigurationReplicatedDiskTypeDef]]
    replicationServerInstanceType: NotRequired[str]
    replicationServersSecurityGroupsIDs: NotRequired[Sequence[str]]
    stagingAreaSubnetId: NotRequired[str]
    stagingAreaTags: NotRequired[Mapping[str, str]]
    useDedicatedReplicationServer: NotRequired[bool]
    useFipsEndpoint: NotRequired[bool]


class UpdateSourceServerRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]
    connectorAction: NotRequired[SourceServerConnectorActionTypeDef]


class WaveResponseTypeDef(TypedDict):
    arn: str
    creationDateTime: str
    description: str
    isArchived: bool
    lastModifiedDateTime: str
    name: str
    tags: Dict[str, str]
    waveAggregatedStatus: WaveAggregatedStatusTypeDef
    waveID: str
    ResponseMetadata: ResponseMetadataTypeDef


class WaveTypeDef(TypedDict):
    arn: NotRequired[str]
    creationDateTime: NotRequired[str]
    description: NotRequired[str]
    isArchived: NotRequired[bool]
    lastModifiedDateTime: NotRequired[str]
    name: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    waveAggregatedStatus: NotRequired[WaveAggregatedStatusTypeDef]
    waveID: NotRequired[str]


class ListApplicationsResponseTypeDef(TypedDict):
    items: List[ApplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListConnectorsResponseTypeDef(TypedDict):
    items: List[ConnectorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DataReplicationInfoTypeDef(TypedDict):
    dataReplicationError: NotRequired[DataReplicationErrorTypeDef]
    dataReplicationInitiation: NotRequired[DataReplicationInitiationTypeDef]
    dataReplicationState: NotRequired[DataReplicationStateType]
    etaDateTime: NotRequired[str]
    lagDuration: NotRequired[str]
    lastSnapshotDateTime: NotRequired[str]
    replicatedDisks: NotRequired[List[DataReplicationInfoReplicatedDiskTypeDef]]


class ListExportErrorsResponseTypeDef(TypedDict):
    items: List[ExportTaskErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListExportsResponseTypeDef(TypedDict):
    items: List[ExportTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartExportResponseTypeDef(TypedDict):
    exportTask: ExportTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListImportErrorsResponseTypeDef(TypedDict):
    items: List[ImportTaskErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ImportTaskTypeDef(TypedDict):
    creationDateTime: NotRequired[str]
    endDateTime: NotRequired[str]
    importID: NotRequired[str]
    progressPercentage: NotRequired[float]
    s3BucketSource: NotRequired[S3BucketSourceTypeDef]
    status: NotRequired[ImportStatusType]
    summary: NotRequired[ImportTaskSummaryTypeDef]


class DescribeJobLogItemsResponseTypeDef(TypedDict):
    items: List[JobLogTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class LifeCycleTypeDef(TypedDict):
    addedToServiceDateTime: NotRequired[str]
    elapsedReplicationDuration: NotRequired[str]
    firstByteDateTime: NotRequired[str]
    lastCutover: NotRequired[LifeCycleLastCutoverTypeDef]
    lastSeenByServiceDateTime: NotRequired[str]
    lastTest: NotRequired[LifeCycleLastTestTypeDef]
    state: NotRequired[LifeCycleStateType]


class ListSourceServerActionsResponseTypeDef(TypedDict):
    items: List[SourceServerActionDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class JobPostLaunchActionsLaunchStatusTypeDef(TypedDict):
    executionID: NotRequired[str]
    executionStatus: NotRequired[PostLaunchActionExecutionStatusType]
    failureReason: NotRequired[str]
    ssmDocument: NotRequired[SsmDocumentOutputTypeDef]
    ssmDocumentType: NotRequired[SsmDocumentTypeType]


class PostLaunchActionsOutputTypeDef(TypedDict):
    cloudWatchLogGroupName: NotRequired[str]
    deployment: NotRequired[PostLaunchActionsDeploymentTypeType]
    s3LogBucket: NotRequired[str]
    s3OutputKeyPrefix: NotRequired[str]
    ssmDocuments: NotRequired[List[SsmDocumentOutputTypeDef]]


class PostLaunchActionsTypeDef(TypedDict):
    cloudWatchLogGroupName: NotRequired[str]
    deployment: NotRequired[PostLaunchActionsDeploymentTypeType]
    s3LogBucket: NotRequired[str]
    s3OutputKeyPrefix: NotRequired[str]
    ssmDocuments: NotRequired[Sequence[SsmDocumentTypeDef]]


class ListTemplateActionsResponseTypeDef(TypedDict):
    items: List[TemplateActionDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListWavesResponseTypeDef(TypedDict):
    items: List[WaveTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListImportsResponseTypeDef(TypedDict):
    items: List[ImportTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class StartImportResponseTypeDef(TypedDict):
    importTask: ImportTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SourceServerResponseTypeDef(TypedDict):
    applicationID: str
    arn: str
    connectorAction: SourceServerConnectorActionTypeDef
    dataReplicationInfo: DataReplicationInfoTypeDef
    fqdnForActionFramework: str
    isArchived: bool
    launchedInstance: LaunchedInstanceTypeDef
    lifeCycle: LifeCycleTypeDef
    replicationType: ReplicationTypeType
    sourceProperties: SourcePropertiesTypeDef
    sourceServerID: str
    tags: Dict[str, str]
    userProvidedID: str
    vcenterClientID: str
    ResponseMetadata: ResponseMetadataTypeDef


class SourceServerTypeDef(TypedDict):
    applicationID: NotRequired[str]
    arn: NotRequired[str]
    connectorAction: NotRequired[SourceServerConnectorActionTypeDef]
    dataReplicationInfo: NotRequired[DataReplicationInfoTypeDef]
    fqdnForActionFramework: NotRequired[str]
    isArchived: NotRequired[bool]
    launchedInstance: NotRequired[LaunchedInstanceTypeDef]
    lifeCycle: NotRequired[LifeCycleTypeDef]
    replicationType: NotRequired[ReplicationTypeType]
    sourceProperties: NotRequired[SourcePropertiesTypeDef]
    sourceServerID: NotRequired[str]
    tags: NotRequired[Dict[str, str]]
    userProvidedID: NotRequired[str]
    vcenterClientID: NotRequired[str]


class PostLaunchActionsStatusTypeDef(TypedDict):
    postLaunchActionsLaunchStatusList: NotRequired[List[JobPostLaunchActionsLaunchStatusTypeDef]]
    ssmAgentDiscoveryDatetime: NotRequired[str]


class LaunchConfigurationTemplateResponseTypeDef(TypedDict):
    arn: str
    associatePublicIpAddress: bool
    bootMode: BootModeType
    copyPrivateIp: bool
    copyTags: bool
    ec2LaunchTemplateID: str
    enableMapAutoTagging: bool
    largeVolumeConf: LaunchTemplateDiskConfTypeDef
    launchConfigurationTemplateID: str
    launchDisposition: LaunchDispositionType
    licensing: LicensingTypeDef
    mapAutoTaggingMpeID: str
    postLaunchActions: PostLaunchActionsOutputTypeDef
    smallVolumeConf: LaunchTemplateDiskConfTypeDef
    smallVolumeMaxSize: int
    tags: Dict[str, str]
    targetInstanceTypeRightSizingMethod: TargetInstanceTypeRightSizingMethodType
    ResponseMetadata: ResponseMetadataTypeDef


class LaunchConfigurationTemplateTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    arn: NotRequired[str]
    associatePublicIpAddress: NotRequired[bool]
    bootMode: NotRequired[BootModeType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    ec2LaunchTemplateID: NotRequired[str]
    enableMapAutoTagging: NotRequired[bool]
    largeVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    launchDisposition: NotRequired[LaunchDispositionType]
    licensing: NotRequired[LicensingTypeDef]
    mapAutoTaggingMpeID: NotRequired[str]
    postLaunchActions: NotRequired[PostLaunchActionsOutputTypeDef]
    smallVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    smallVolumeMaxSize: NotRequired[int]
    tags: NotRequired[Dict[str, str]]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]


class LaunchConfigurationTypeDef(TypedDict):
    bootMode: BootModeType
    copyPrivateIp: bool
    copyTags: bool
    ec2LaunchTemplateID: str
    enableMapAutoTagging: bool
    launchDisposition: LaunchDispositionType
    licensing: LicensingTypeDef
    mapAutoTaggingMpeID: str
    name: str
    postLaunchActions: PostLaunchActionsOutputTypeDef
    sourceServerID: str
    targetInstanceTypeRightSizingMethod: TargetInstanceTypeRightSizingMethodType
    ResponseMetadata: ResponseMetadataTypeDef


PostLaunchActionsUnionTypeDef = Union[PostLaunchActionsTypeDef, PostLaunchActionsOutputTypeDef]


class DescribeSourceServersResponseTypeDef(TypedDict):
    items: List[SourceServerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ParticipatingServerTypeDef(TypedDict):
    sourceServerID: str
    launchStatus: NotRequired[LaunchStatusType]
    launchedEc2InstanceID: NotRequired[str]
    postLaunchActionsStatus: NotRequired[PostLaunchActionsStatusTypeDef]


class DescribeLaunchConfigurationTemplatesResponseTypeDef(TypedDict):
    items: List[LaunchConfigurationTemplateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateLaunchConfigurationTemplateRequestTypeDef(TypedDict):
    associatePublicIpAddress: NotRequired[bool]
    bootMode: NotRequired[BootModeType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    enableMapAutoTagging: NotRequired[bool]
    largeVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    launchDisposition: NotRequired[LaunchDispositionType]
    licensing: NotRequired[LicensingTypeDef]
    mapAutoTaggingMpeID: NotRequired[str]
    postLaunchActions: NotRequired[PostLaunchActionsUnionTypeDef]
    smallVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    smallVolumeMaxSize: NotRequired[int]
    tags: NotRequired[Mapping[str, str]]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]


class UpdateLaunchConfigurationRequestTypeDef(TypedDict):
    sourceServerID: str
    accountID: NotRequired[str]
    bootMode: NotRequired[BootModeType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    enableMapAutoTagging: NotRequired[bool]
    launchDisposition: NotRequired[LaunchDispositionType]
    licensing: NotRequired[LicensingTypeDef]
    mapAutoTaggingMpeID: NotRequired[str]
    name: NotRequired[str]
    postLaunchActions: NotRequired[PostLaunchActionsUnionTypeDef]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]


class UpdateLaunchConfigurationTemplateRequestTypeDef(TypedDict):
    launchConfigurationTemplateID: str
    associatePublicIpAddress: NotRequired[bool]
    bootMode: NotRequired[BootModeType]
    copyPrivateIp: NotRequired[bool]
    copyTags: NotRequired[bool]
    enableMapAutoTagging: NotRequired[bool]
    largeVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    launchDisposition: NotRequired[LaunchDispositionType]
    licensing: NotRequired[LicensingTypeDef]
    mapAutoTaggingMpeID: NotRequired[str]
    postLaunchActions: NotRequired[PostLaunchActionsUnionTypeDef]
    smallVolumeConf: NotRequired[LaunchTemplateDiskConfTypeDef]
    smallVolumeMaxSize: NotRequired[int]
    targetInstanceTypeRightSizingMethod: NotRequired[TargetInstanceTypeRightSizingMethodType]


JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "jobID": str,
        "arn": NotRequired[str],
        "creationDateTime": NotRequired[str],
        "endDateTime": NotRequired[str],
        "initiatedBy": NotRequired[InitiatedByType],
        "participatingServers": NotRequired[List[ParticipatingServerTypeDef]],
        "status": NotRequired[JobStatusType],
        "tags": NotRequired[Dict[str, str]],
        "type": NotRequired[JobTypeType],
    },
)


class DescribeJobsResponseTypeDef(TypedDict):
    items: List[JobTypeDef]
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
