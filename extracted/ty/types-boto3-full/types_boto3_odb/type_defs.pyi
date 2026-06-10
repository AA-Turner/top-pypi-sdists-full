"""
Type annotations for odb service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_odb/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_odb.type_defs import AcceptMarketplaceRegistrationInputTypeDef

    data: AcceptMarketplaceRegistrationInputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AccessType,
    AutonomousDatabaseBackupStatusType,
    AutonomousDatabaseBackupTypeType,
    AutonomousDatabaseResourceStatusType,
    AutonomousDatabaseWalletStatusType,
    AutonomousMaintenanceScheduleTypeType,
    CharacterSetTypeType,
    CloneTypeType,
    ComputeModelType,
    DatabaseEditionType,
    DatabaseManagementStatusType,
    DatabaseTypeType,
    DataGuardRoleType,
    DataSafeStatusType,
    DayOfWeekNameType,
    DbNodeResourceStatusType,
    DbServerPatchingStatusType,
    DbWorkloadType,
    DisasterRecoveryTypeType,
    DiskRedundancyType,
    EncryptionKeyProviderInputType,
    EncryptionKeyProviderType,
    ExternalIdTypeType,
    IamRoleStatusType,
    IormLifecycleStateType,
    LicenseModelType,
    ManagedResourceStatusType,
    MonthNameType,
    NetServicesArchitectureType,
    ObjectiveType,
    OciOnboardingStatusType,
    OpenModeType,
    OperationsInsightsStatusType,
    PatchingModeTypeType,
    PermissionLevelType,
    PreferenceTypeType,
    RefreshableModeType,
    RefreshableStatusType,
    RepeatCadenceType,
    ResourceStatusType,
    ShapeTypeType,
    SourceTypeType,
    StandbyAllowlistedIpsSourceType,
    WalletTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceptMarketplaceRegistrationInputTypeDef",
    "AssociateIamRoleToResourceInputTypeDef",
    "AutonomousDatabaseApexTypeDef",
    "AutonomousDatabaseBackupSummaryTypeDef",
    "AutonomousDatabaseBackupTypeDef",
    "AutonomousDatabaseCharacterSetSummaryTypeDef",
    "AutonomousDatabaseConnectionStringsTypeDef",
    "AutonomousDatabaseConnectionUrlsTypeDef",
    "AutonomousDatabasePeerSummaryTypeDef",
    "AutonomousDatabaseSummaryTypeDef",
    "AutonomousDatabaseTypeDef",
    "AutonomousDatabaseVersionSummaryTypeDef",
    "AutonomousDatabaseWalletDetailsTypeDef",
    "AutonomousVirtualMachineSummaryTypeDef",
    "AwsEncryptionKeyConfigurationInputTypeDef",
    "AwsEncryptionKeyConfigurationTypeDef",
    "CloneToRefreshableConfigurationTypeDef",
    "CloudAutonomousVmClusterResourceDetailsTypeDef",
    "CloudAutonomousVmClusterSummaryTypeDef",
    "CloudAutonomousVmClusterTypeDef",
    "CloudExadataInfrastructureSummaryTypeDef",
    "CloudExadataInfrastructureTypeDef",
    "CloudExadataInfrastructureUnallocatedResourcesTypeDef",
    "CloudVmClusterSummaryTypeDef",
    "CloudVmClusterTypeDef",
    "CreateAutonomousDatabaseBackupInputTypeDef",
    "CreateAutonomousDatabaseBackupOutputTypeDef",
    "CreateAutonomousDatabaseInputTypeDef",
    "CreateAutonomousDatabaseOutputTypeDef",
    "CreateAutonomousDatabaseWalletInputTypeDef",
    "CreateAutonomousDatabaseWalletOutputTypeDef",
    "CreateCloudAutonomousVmClusterInputTypeDef",
    "CreateCloudAutonomousVmClusterOutputTypeDef",
    "CreateCloudExadataInfrastructureInputTypeDef",
    "CreateCloudExadataInfrastructureOutputTypeDef",
    "CreateCloudVmClusterInputTypeDef",
    "CreateCloudVmClusterOutputTypeDef",
    "CreateOdbNetworkInputTypeDef",
    "CreateOdbNetworkOutputTypeDef",
    "CreateOdbPeeringConnectionInputTypeDef",
    "CreateOdbPeeringConnectionOutputTypeDef",
    "CrossRegionDataGuardConfigurationTypeDef",
    "CrossRegionDisasterRecoveryConfigurationTypeDef",
    "CrossRegionS3RestoreSourcesAccessTypeDef",
    "CustomerContactTypeDef",
    "DataCollectionOptionsTypeDef",
    "DatabaseCloneConfigurationTypeDef",
    "DatabaseConnectionStringProfileTypeDef",
    "DatabaseStandbySummaryTypeDef",
    "DatabaseToolTypeDef",
    "DayOfWeekTypeDef",
    "DbIormConfigTypeDef",
    "DbNodeSummaryTypeDef",
    "DbNodeTypeDef",
    "DbServerPatchingDetailsTypeDef",
    "DbServerSummaryTypeDef",
    "DbServerTypeDef",
    "DbSystemShapeSummaryTypeDef",
    "DeleteAutonomousDatabaseBackupInputTypeDef",
    "DeleteAutonomousDatabaseInputTypeDef",
    "DeleteCloudAutonomousVmClusterInputTypeDef",
    "DeleteCloudExadataInfrastructureInputTypeDef",
    "DeleteCloudVmClusterInputTypeDef",
    "DeleteOdbNetworkInputTypeDef",
    "DeleteOdbPeeringConnectionInputTypeDef",
    "DisassociateIamRoleFromResourceInputTypeDef",
    "DisasterRecoveryConfigurationTypeDef",
    "EncryptionKeyConfigurationInputTypeDef",
    "EncryptionKeyConfigurationTypeDef",
    "EncryptionSummaryTypeDef",
    "ExadataIormConfigTypeDef",
    "FailoverAutonomousDatabaseInputTypeDef",
    "FailoverAutonomousDatabaseOutputTypeDef",
    "GetAutonomousDatabaseBackupInputTypeDef",
    "GetAutonomousDatabaseBackupOutputTypeDef",
    "GetAutonomousDatabaseInputTypeDef",
    "GetAutonomousDatabaseOutputTypeDef",
    "GetAutonomousDatabaseWalletDetailsInputTypeDef",
    "GetAutonomousDatabaseWalletDetailsOutputTypeDef",
    "GetCloudAutonomousVmClusterInputTypeDef",
    "GetCloudAutonomousVmClusterOutputTypeDef",
    "GetCloudExadataInfrastructureInputTypeDef",
    "GetCloudExadataInfrastructureOutputTypeDef",
    "GetCloudExadataInfrastructureUnallocatedResourcesInputTypeDef",
    "GetCloudExadataInfrastructureUnallocatedResourcesOutputTypeDef",
    "GetCloudVmClusterInputTypeDef",
    "GetCloudVmClusterOutputTypeDef",
    "GetDbNodeInputTypeDef",
    "GetDbNodeOutputTypeDef",
    "GetDbServerInputTypeDef",
    "GetDbServerOutputTypeDef",
    "GetOciOnboardingStatusOutputTypeDef",
    "GetOdbNetworkInputTypeDef",
    "GetOdbNetworkOutputTypeDef",
    "GetOdbPeeringConnectionInputTypeDef",
    "GetOdbPeeringConnectionOutputTypeDef",
    "GiVersionSummaryTypeDef",
    "IamRoleTypeDef",
    "InitializeServiceInputTypeDef",
    "KmsAccessTypeDef",
    "ListAutonomousDatabaseBackupsInputPaginateTypeDef",
    "ListAutonomousDatabaseBackupsInputTypeDef",
    "ListAutonomousDatabaseBackupsOutputTypeDef",
    "ListAutonomousDatabaseCharacterSetsInputPaginateTypeDef",
    "ListAutonomousDatabaseCharacterSetsInputTypeDef",
    "ListAutonomousDatabaseCharacterSetsOutputTypeDef",
    "ListAutonomousDatabaseClonesInputPaginateTypeDef",
    "ListAutonomousDatabaseClonesInputTypeDef",
    "ListAutonomousDatabaseClonesOutputTypeDef",
    "ListAutonomousDatabasePeersInputPaginateTypeDef",
    "ListAutonomousDatabasePeersInputTypeDef",
    "ListAutonomousDatabasePeersOutputTypeDef",
    "ListAutonomousDatabaseVersionsInputPaginateTypeDef",
    "ListAutonomousDatabaseVersionsInputTypeDef",
    "ListAutonomousDatabaseVersionsOutputTypeDef",
    "ListAutonomousDatabasesInputPaginateTypeDef",
    "ListAutonomousDatabasesInputTypeDef",
    "ListAutonomousDatabasesOutputTypeDef",
    "ListAutonomousVirtualMachinesInputPaginateTypeDef",
    "ListAutonomousVirtualMachinesInputTypeDef",
    "ListAutonomousVirtualMachinesOutputTypeDef",
    "ListCloudAutonomousVmClustersInputPaginateTypeDef",
    "ListCloudAutonomousVmClustersInputTypeDef",
    "ListCloudAutonomousVmClustersOutputTypeDef",
    "ListCloudExadataInfrastructuresInputPaginateTypeDef",
    "ListCloudExadataInfrastructuresInputTypeDef",
    "ListCloudExadataInfrastructuresOutputTypeDef",
    "ListCloudVmClustersInputPaginateTypeDef",
    "ListCloudVmClustersInputTypeDef",
    "ListCloudVmClustersOutputTypeDef",
    "ListDbNodesInputPaginateTypeDef",
    "ListDbNodesInputTypeDef",
    "ListDbNodesOutputTypeDef",
    "ListDbServersInputPaginateTypeDef",
    "ListDbServersInputTypeDef",
    "ListDbServersOutputTypeDef",
    "ListDbSystemShapesInputPaginateTypeDef",
    "ListDbSystemShapesInputTypeDef",
    "ListDbSystemShapesOutputTypeDef",
    "ListGiVersionsInputPaginateTypeDef",
    "ListGiVersionsInputTypeDef",
    "ListGiVersionsOutputTypeDef",
    "ListOdbNetworksInputPaginateTypeDef",
    "ListOdbNetworksInputTypeDef",
    "ListOdbNetworksOutputTypeDef",
    "ListOdbPeeringConnectionsInputPaginateTypeDef",
    "ListOdbPeeringConnectionsInputTypeDef",
    "ListOdbPeeringConnectionsOutputTypeDef",
    "ListSystemVersionsInputPaginateTypeDef",
    "ListSystemVersionsInputTypeDef",
    "ListSystemVersionsOutputTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LongTermBackupScheduleOutputTypeDef",
    "LongTermBackupScheduleTypeDef",
    "LongTermBackupScheduleUnionTypeDef",
    "MaintenanceWindowOutputTypeDef",
    "MaintenanceWindowTypeDef",
    "MaintenanceWindowUnionTypeDef",
    "ManagedS3BackupAccessTypeDef",
    "ManagedServicesTypeDef",
    "MonthTypeDef",
    "OciDnsForwardingConfigTypeDef",
    "OciEncryptionKeyConfigurationTypeDef",
    "OciIamRoleTypeDef",
    "OciIdentityDomainTypeDef",
    "OdbNetworkSummaryTypeDef",
    "OdbNetworkTypeDef",
    "OdbPeeringConnectionSummaryTypeDef",
    "OdbPeeringConnectionTypeDef",
    "OkvEncryptionKeyConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PointInTimeRestoreConfigurationTypeDef",
    "RebootAutonomousDatabaseInputTypeDef",
    "RebootAutonomousDatabaseOutputTypeDef",
    "RebootDbNodeInputTypeDef",
    "RebootDbNodeOutputTypeDef",
    "ResourcePoolSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreAutonomousDatabaseInputTypeDef",
    "RestoreAutonomousDatabaseOutputTypeDef",
    "RestoreFromBackupConfigurationTypeDef",
    "S3AccessTypeDef",
    "ScheduledOperationDetailsTypeDef",
    "ServiceNetworkEndpointTypeDef",
    "ShrinkAutonomousDatabaseInputTypeDef",
    "ShrinkAutonomousDatabaseOutputTypeDef",
    "SourceConfigurationTypeDef",
    "StartAutonomousDatabaseInputTypeDef",
    "StartAutonomousDatabaseOutputTypeDef",
    "StartDbNodeInputTypeDef",
    "StartDbNodeOutputTypeDef",
    "StopAutonomousDatabaseInputTypeDef",
    "StopAutonomousDatabaseOutputTypeDef",
    "StopDbNodeInputTypeDef",
    "StopDbNodeOutputTypeDef",
    "StsAccessTypeDef",
    "SubscriptionErrorTypeDef",
    "SwitchoverAutonomousDatabaseInputTypeDef",
    "SwitchoverAutonomousDatabaseOutputTypeDef",
    "SystemVersionSummaryTypeDef",
    "TagResourceRequestTypeDef",
    "TimestampTypeDef",
    "TransportableTablespaceTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAutonomousDatabaseBackupInputTypeDef",
    "UpdateAutonomousDatabaseBackupOutputTypeDef",
    "UpdateAutonomousDatabaseInputTypeDef",
    "UpdateAutonomousDatabaseOutputTypeDef",
    "UpdateCloudExadataInfrastructureInputTypeDef",
    "UpdateCloudExadataInfrastructureOutputTypeDef",
    "UpdateOdbNetworkInputTypeDef",
    "UpdateOdbNetworkOutputTypeDef",
    "UpdateOdbPeeringConnectionInputTypeDef",
    "UpdateOdbPeeringConnectionOutputTypeDef",
    "ZeroEtlAccessTypeDef",
)

class AcceptMarketplaceRegistrationInputTypeDef(TypedDict):
    marketplaceRegistrationToken: str

class AssociateIamRoleToResourceInputTypeDef(TypedDict):
    iamRoleArn: str
    awsIntegration: Literal["KmsTde"]
    resourceArn: str

class AutonomousDatabaseApexTypeDef(TypedDict):
    apexVersion: NotRequired[str]
    ordsVersion: NotRequired[str]

AutonomousDatabaseBackupSummaryTypeDef = TypedDict(
    "AutonomousDatabaseBackupSummaryTypeDef",
    {
        "autonomousDatabaseBackupId": NotRequired[str],
        "autonomousDatabaseBackupArn": NotRequired[str],
        "autonomousDatabaseId": NotRequired[str],
        "ocid": NotRequired[str],
        "displayName": NotRequired[str],
        "dbVersion": NotRequired[str],
        "status": NotRequired[AutonomousDatabaseBackupStatusType],
        "statusReason": NotRequired[str],
        "isAutomatic": NotRequired[bool],
        "retentionPeriodInDays": NotRequired[int],
        "sizeInTBs": NotRequired[float],
        "timeAvailableTill": NotRequired[datetime],
        "timeStarted": NotRequired[datetime],
        "timeEnded": NotRequired[datetime],
        "type": NotRequired[AutonomousDatabaseBackupTypeType],
    },
)
AutonomousDatabaseBackupTypeDef = TypedDict(
    "AutonomousDatabaseBackupTypeDef",
    {
        "autonomousDatabaseBackupId": NotRequired[str],
        "autonomousDatabaseBackupArn": NotRequired[str],
        "autonomousDatabaseId": NotRequired[str],
        "ocid": NotRequired[str],
        "displayName": NotRequired[str],
        "dbVersion": NotRequired[str],
        "status": NotRequired[AutonomousDatabaseBackupStatusType],
        "statusReason": NotRequired[str],
        "isAutomatic": NotRequired[bool],
        "retentionPeriodInDays": NotRequired[int],
        "sizeInTBs": NotRequired[float],
        "timeAvailableTill": NotRequired[datetime],
        "timeStarted": NotRequired[datetime],
        "timeEnded": NotRequired[datetime],
        "type": NotRequired[AutonomousDatabaseBackupTypeType],
    },
)

class AutonomousDatabaseCharacterSetSummaryTypeDef(TypedDict):
    characterSet: NotRequired[str]

class DatabaseConnectionStringProfileTypeDef(TypedDict):
    consumerGroup: NotRequired[str]
    displayName: NotRequired[str]
    hostFormat: NotRequired[str]
    isRegional: NotRequired[bool]
    protocol: NotRequired[str]
    sessionMode: NotRequired[str]
    syntaxFormat: NotRequired[str]
    tlsAuthentication: NotRequired[str]
    value: NotRequired[str]

class AutonomousDatabaseConnectionUrlsTypeDef(TypedDict):
    apexUrl: NotRequired[str]
    databaseTransformsUrl: NotRequired[str]
    graphStudioUrl: NotRequired[str]
    machineLearningNotebookUrl: NotRequired[str]
    machineLearningUserManagementUrl: NotRequired[str]
    mongoDbUrl: NotRequired[str]
    ordsUrl: NotRequired[str]
    spatialStudioUrl: NotRequired[str]
    sqlDevWebUrl: NotRequired[str]

class AutonomousDatabasePeerSummaryTypeDef(TypedDict):
    autonomousDatabaseId: NotRequired[str]
    autonomousDatabaseArn: NotRequired[str]
    ocid: NotRequired[str]
    region: NotRequired[str]

class CustomerContactTypeDef(TypedDict):
    email: NotRequired[str]

class DatabaseStandbySummaryTypeDef(TypedDict):
    availabilityDomain: NotRequired[str]
    lagTimeInSeconds: NotRequired[int]
    status: NotRequired[AutonomousDatabaseResourceStatusType]
    statusReason: NotRequired[str]
    maintenanceTargetComponent: NotRequired[str]
    timeDataGuardRoleChanged: NotRequired[datetime]
    timeDisasterRecoveryRoleChanged: NotRequired[datetime]
    timeMaintenanceBegin: NotRequired[datetime]
    timeMaintenanceEnd: NotRequired[datetime]

class DatabaseToolTypeDef(TypedDict):
    isEnabled: NotRequired[bool]
    name: NotRequired[str]
    computeCount: NotRequired[float]
    maxIdleTimeInMinutes: NotRequired[int]

class DisasterRecoveryConfigurationTypeDef(TypedDict):
    disasterRecoveryType: NotRequired[DisasterRecoveryTypeType]
    isReplicateAutomaticBackups: NotRequired[bool]
    isSnapshotStandby: NotRequired[bool]
    timeSnapshotStandbyEnabledTill: NotRequired[datetime]

class LongTermBackupScheduleOutputTypeDef(TypedDict):
    isDisabled: NotRequired[bool]
    repeatCadence: NotRequired[RepeatCadenceType]
    retentionPeriodInDays: NotRequired[int]
    timeOfBackup: NotRequired[datetime]

class ResourcePoolSummaryTypeDef(TypedDict):
    isDisabled: NotRequired[bool]
    poolSize: NotRequired[int]
    poolStorageSizeInTBs: NotRequired[int]
    availableStorageCapacityInTBs: NotRequired[float]
    totalComputeCapacity: NotRequired[int]
    availableComputeCapacity: NotRequired[int]

class AutonomousDatabaseVersionSummaryTypeDef(TypedDict):
    dbWorkload: NotRequired[DbWorkloadType]
    details: NotRequired[str]
    version: NotRequired[str]

class AutonomousDatabaseWalletDetailsTypeDef(TypedDict):
    status: NotRequired[AutonomousDatabaseWalletStatusType]
    timeRotated: NotRequired[datetime]

class AutonomousVirtualMachineSummaryTypeDef(TypedDict):
    autonomousVirtualMachineId: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    vmName: NotRequired[str]
    dbServerId: NotRequired[str]
    dbServerDisplayName: NotRequired[str]
    cpuCoreCount: NotRequired[int]
    memorySizeInGBs: NotRequired[int]
    dbNodeStorageSizeInGBs: NotRequired[int]
    clientIpAddress: NotRequired[str]
    cloudAutonomousVmClusterId: NotRequired[str]
    ocid: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]

class AwsEncryptionKeyConfigurationInputTypeDef(TypedDict):
    iamRoleArn: NotRequired[str]
    externalIdType: NotRequired[ExternalIdTypeType]
    kmsKeyId: NotRequired[str]

class AwsEncryptionKeyConfigurationTypeDef(TypedDict):
    iamRoleArn: NotRequired[str]
    externalIdType: NotRequired[ExternalIdTypeType]
    kmsKeyId: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class CloudAutonomousVmClusterResourceDetailsTypeDef(TypedDict):
    cloudAutonomousVmClusterId: NotRequired[str]
    unallocatedAdbStorageInTBs: NotRequired[float]

class IamRoleTypeDef(TypedDict):
    iamRoleArn: NotRequired[str]
    status: NotRequired[IamRoleStatusType]
    statusReason: NotRequired[str]
    awsIntegration: NotRequired[Literal["KmsTde"]]

class DataCollectionOptionsTypeDef(TypedDict):
    isDiagnosticsEventsEnabled: NotRequired[bool]
    isHealthMonitoringEnabled: NotRequired[bool]
    isIncidentLogsEnabled: NotRequired[bool]

class CreateAutonomousDatabaseBackupInputTypeDef(TypedDict):
    autonomousDatabaseId: str
    displayName: NotRequired[str]
    retentionPeriodInDays: NotRequired[int]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class TransportableTablespaceTypeDef(TypedDict):
    ttsBundleUrl: NotRequired[str]

class CreateAutonomousDatabaseWalletInputTypeDef(TypedDict):
    autonomousDatabaseId: str
    password: str
    walletType: NotRequired[WalletTypeType]
    clientToken: NotRequired[str]

class CreateOdbNetworkInputTypeDef(TypedDict):
    displayName: str
    clientSubnetCidr: str
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    backupSubnetCidr: NotRequired[str]
    customDomainName: NotRequired[str]
    defaultDnsPrefix: NotRequired[str]
    clientToken: NotRequired[str]
    s3Access: NotRequired[AccessType]
    zeroEtlAccess: NotRequired[AccessType]
    stsAccess: NotRequired[AccessType]
    kmsAccess: NotRequired[AccessType]
    s3PolicyDocument: NotRequired[str]
    stsPolicyDocument: NotRequired[str]
    kmsPolicyDocument: NotRequired[str]
    crossRegionS3RestoreSourcesToEnable: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]

class CreateOdbPeeringConnectionInputTypeDef(TypedDict):
    odbNetworkId: str
    peerNetworkId: str
    displayName: NotRequired[str]
    peerNetworkCidrsToBeAdded: NotRequired[Sequence[str]]
    peerNetworkRouteTableIds: NotRequired[Sequence[str]]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CrossRegionDataGuardConfigurationTypeDef(TypedDict):
    sourceAutonomousDatabaseArn: str

class CrossRegionDisasterRecoveryConfigurationTypeDef(TypedDict):
    sourceAutonomousDatabaseArn: str
    remoteDisasterRecoveryType: DisasterRecoveryTypeType
    isReplicateAutomaticBackups: NotRequired[bool]

class CrossRegionS3RestoreSourcesAccessTypeDef(TypedDict):
    region: NotRequired[str]
    ipv4Addresses: NotRequired[list[str]]
    status: NotRequired[ManagedResourceStatusType]

class DatabaseCloneConfigurationTypeDef(TypedDict):
    sourceAutonomousDatabaseId: str
    cloneType: CloneTypeType

class DayOfWeekTypeDef(TypedDict):
    name: NotRequired[DayOfWeekNameType]

class DbIormConfigTypeDef(TypedDict):
    dbName: NotRequired[str]
    flashCacheLimit: NotRequired[str]
    share: NotRequired[int]

class DbNodeSummaryTypeDef(TypedDict):
    dbNodeId: NotRequired[str]
    dbNodeArn: NotRequired[str]
    status: NotRequired[DbNodeResourceStatusType]
    statusReason: NotRequired[str]
    additionalDetails: NotRequired[str]
    backupIpId: NotRequired[str]
    backupVnic2Id: NotRequired[str]
    backupVnicId: NotRequired[str]
    cpuCoreCount: NotRequired[int]
    dbNodeStorageSizeInGBs: NotRequired[int]
    dbServerId: NotRequired[str]
    dbSystemId: NotRequired[str]
    faultDomain: NotRequired[str]
    hostIpId: NotRequired[str]
    hostname: NotRequired[str]
    ocid: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    maintenanceType: NotRequired[Literal["VMDB_REBOOT_MIGRATION"]]
    memorySizeInGBs: NotRequired[int]
    softwareStorageSizeInGB: NotRequired[int]
    createdAt: NotRequired[datetime]
    timeMaintenanceWindowEnd: NotRequired[str]
    timeMaintenanceWindowStart: NotRequired[str]
    totalCpuCoreCount: NotRequired[int]
    vnic2Id: NotRequired[str]
    vnicId: NotRequired[str]

class DbNodeTypeDef(TypedDict):
    dbNodeId: NotRequired[str]
    dbNodeArn: NotRequired[str]
    status: NotRequired[DbNodeResourceStatusType]
    statusReason: NotRequired[str]
    additionalDetails: NotRequired[str]
    backupIpId: NotRequired[str]
    backupVnic2Id: NotRequired[str]
    backupVnicId: NotRequired[str]
    cpuCoreCount: NotRequired[int]
    dbNodeStorageSizeInGBs: NotRequired[int]
    dbServerId: NotRequired[str]
    dbSystemId: NotRequired[str]
    faultDomain: NotRequired[str]
    hostIpId: NotRequired[str]
    hostname: NotRequired[str]
    ocid: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    maintenanceType: NotRequired[Literal["VMDB_REBOOT_MIGRATION"]]
    memorySizeInGBs: NotRequired[int]
    softwareStorageSizeInGB: NotRequired[int]
    createdAt: NotRequired[datetime]
    timeMaintenanceWindowEnd: NotRequired[str]
    timeMaintenanceWindowStart: NotRequired[str]
    totalCpuCoreCount: NotRequired[int]
    vnic2Id: NotRequired[str]
    vnicId: NotRequired[str]
    privateIpAddress: NotRequired[str]
    floatingIpAddress: NotRequired[str]

class DbServerPatchingDetailsTypeDef(TypedDict):
    estimatedPatchDuration: NotRequired[int]
    patchingStatus: NotRequired[DbServerPatchingStatusType]
    timePatchingEnded: NotRequired[str]
    timePatchingStarted: NotRequired[str]

class DbSystemShapeSummaryTypeDef(TypedDict):
    availableCoreCount: NotRequired[int]
    availableCoreCountPerNode: NotRequired[int]
    availableDataStorageInTBs: NotRequired[int]
    availableDataStoragePerServerInTBs: NotRequired[int]
    availableDbNodePerNodeInGBs: NotRequired[int]
    availableDbNodeStorageInGBs: NotRequired[int]
    availableMemoryInGBs: NotRequired[int]
    availableMemoryPerNodeInGBs: NotRequired[int]
    coreCountIncrement: NotRequired[int]
    maxStorageCount: NotRequired[int]
    maximumNodeCount: NotRequired[int]
    minCoreCountPerNode: NotRequired[int]
    minDataStorageInTBs: NotRequired[int]
    minDbNodeStoragePerNodeInGBs: NotRequired[int]
    minMemoryPerNodeInGBs: NotRequired[int]
    minStorageCount: NotRequired[int]
    minimumCoreCount: NotRequired[int]
    minimumNodeCount: NotRequired[int]
    runtimeMinimumCoreCount: NotRequired[int]
    shapeFamily: NotRequired[str]
    shapeType: NotRequired[ShapeTypeType]
    name: NotRequired[str]
    computeModel: NotRequired[ComputeModelType]
    areServerTypesSupported: NotRequired[bool]

class DeleteAutonomousDatabaseBackupInputTypeDef(TypedDict):
    autonomousDatabaseBackupId: str

class DeleteAutonomousDatabaseInputTypeDef(TypedDict):
    autonomousDatabaseId: str

class DeleteCloudAutonomousVmClusterInputTypeDef(TypedDict):
    cloudAutonomousVmClusterId: str

class DeleteCloudExadataInfrastructureInputTypeDef(TypedDict):
    cloudExadataInfrastructureId: str

class DeleteCloudVmClusterInputTypeDef(TypedDict):
    cloudVmClusterId: str

class DeleteOdbNetworkInputTypeDef(TypedDict):
    odbNetworkId: str
    deleteAssociatedResources: bool

class DeleteOdbPeeringConnectionInputTypeDef(TypedDict):
    odbPeeringConnectionId: str

class DisassociateIamRoleFromResourceInputTypeDef(TypedDict):
    iamRoleArn: str
    awsIntegration: Literal["KmsTde"]
    resourceArn: str

class OciEncryptionKeyConfigurationTypeDef(TypedDict):
    kmsKeyId: str
    vaultId: str

class OkvEncryptionKeyConfigurationTypeDef(TypedDict):
    certificateDirectoryName: str
    directoryName: str
    okvKmsKey: str
    okvUri: str
    certificateId: NotRequired[str]

class FailoverAutonomousDatabaseInputTypeDef(TypedDict):
    autonomousDatabaseId: str
    peerDbArn: NotRequired[str]

class GetAutonomousDatabaseBackupInputTypeDef(TypedDict):
    autonomousDatabaseBackupId: str

class GetAutonomousDatabaseInputTypeDef(TypedDict):
    autonomousDatabaseId: str

class GetAutonomousDatabaseWalletDetailsInputTypeDef(TypedDict):
    autonomousDatabaseId: str

class GetCloudAutonomousVmClusterInputTypeDef(TypedDict):
    cloudAutonomousVmClusterId: str

class GetCloudExadataInfrastructureInputTypeDef(TypedDict):
    cloudExadataInfrastructureId: str

class GetCloudExadataInfrastructureUnallocatedResourcesInputTypeDef(TypedDict):
    cloudExadataInfrastructureId: str
    dbServers: NotRequired[Sequence[str]]

class GetCloudVmClusterInputTypeDef(TypedDict):
    cloudVmClusterId: str

class GetDbNodeInputTypeDef(TypedDict):
    cloudVmClusterId: str
    dbNodeId: str

class GetDbServerInputTypeDef(TypedDict):
    cloudExadataInfrastructureId: str
    dbServerId: str

class OciIamRoleTypeDef(TypedDict):
    iamRoleArn: NotRequired[str]
    awsIntegration: NotRequired[Literal["KmsTde"]]

class OciIdentityDomainTypeDef(TypedDict):
    ociIdentityDomainId: NotRequired[str]
    ociIdentityDomainResourceUrl: NotRequired[str]
    ociIdentityDomainUrl: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    accountSetupCloudFormationUrl: NotRequired[str]

class SubscriptionErrorTypeDef(TypedDict):
    errorMessage: NotRequired[str]

class GetOdbNetworkInputTypeDef(TypedDict):
    odbNetworkId: str

class GetOdbPeeringConnectionInputTypeDef(TypedDict):
    odbPeeringConnectionId: str

class OdbPeeringConnectionTypeDef(TypedDict):
    odbPeeringConnectionId: str
    displayName: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    odbPeeringConnectionArn: NotRequired[str]
    odbNetworkArn: NotRequired[str]
    peerNetworkArn: NotRequired[str]
    odbPeeringConnectionType: NotRequired[str]
    peerNetworkCidrs: NotRequired[list[str]]
    createdAt: NotRequired[datetime]
    percentProgress: NotRequired[float]

class GiVersionSummaryTypeDef(TypedDict):
    version: NotRequired[str]

class InitializeServiceInputTypeDef(TypedDict):
    ociIdentityDomain: NotRequired[bool]

class KmsAccessTypeDef(TypedDict):
    status: NotRequired[ManagedResourceStatusType]
    ipv4Addresses: NotRequired[list[str]]
    domainName: NotRequired[str]
    kmsPolicyDocument: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

ListAutonomousDatabaseBackupsInputTypeDef = TypedDict(
    "ListAutonomousDatabaseBackupsInputTypeDef",
    {
        "autonomousDatabaseId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "status": NotRequired[AutonomousDatabaseBackupStatusType],
        "type": NotRequired[AutonomousDatabaseBackupTypeType],
    },
)

class ListAutonomousDatabaseCharacterSetsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    characterSetType: NotRequired[CharacterSetTypeType]

class ListAutonomousDatabaseClonesInputTypeDef(TypedDict):
    autonomousDatabaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAutonomousDatabasePeersInputTypeDef(TypedDict):
    autonomousDatabaseId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAutonomousDatabaseVersionsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    dbWorkload: NotRequired[DbWorkloadType]

class ListAutonomousDatabasesInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAutonomousVirtualMachinesInputTypeDef(TypedDict):
    cloudAutonomousVmClusterId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListCloudAutonomousVmClustersInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    cloudExadataInfrastructureId: NotRequired[str]

class ListCloudExadataInfrastructuresInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListCloudVmClustersInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    cloudExadataInfrastructureId: NotRequired[str]

class ListDbNodesInputTypeDef(TypedDict):
    cloudVmClusterId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDbServersInputTypeDef(TypedDict):
    cloudExadataInfrastructureId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDbSystemShapesInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]

class ListGiVersionsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    shape: NotRequired[str]

class ListOdbNetworksInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListOdbPeeringConnectionsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    odbNetworkId: NotRequired[str]

class OdbPeeringConnectionSummaryTypeDef(TypedDict):
    odbPeeringConnectionId: str
    displayName: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    odbPeeringConnectionArn: NotRequired[str]
    odbNetworkArn: NotRequired[str]
    peerNetworkArn: NotRequired[str]
    odbPeeringConnectionType: NotRequired[str]
    peerNetworkCidrs: NotRequired[list[str]]
    createdAt: NotRequired[datetime]
    percentProgress: NotRequired[float]

class ListSystemVersionsInputTypeDef(TypedDict):
    giVersion: str
    shape: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SystemVersionSummaryTypeDef(TypedDict):
    giVersion: NotRequired[str]
    shape: NotRequired[str]
    systemVersions: NotRequired[list[str]]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class MonthTypeDef(TypedDict):
    name: NotRequired[MonthNameType]

class ManagedS3BackupAccessTypeDef(TypedDict):
    status: NotRequired[ManagedResourceStatusType]
    ipv4Addresses: NotRequired[list[str]]

class S3AccessTypeDef(TypedDict):
    status: NotRequired[ManagedResourceStatusType]
    ipv4Addresses: NotRequired[list[str]]
    domainName: NotRequired[str]
    s3PolicyDocument: NotRequired[str]

class ServiceNetworkEndpointTypeDef(TypedDict):
    vpcEndpointId: NotRequired[str]
    vpcEndpointType: NotRequired[Literal["SERVICENETWORK"]]

class StsAccessTypeDef(TypedDict):
    status: NotRequired[ManagedResourceStatusType]
    ipv4Addresses: NotRequired[list[str]]
    domainName: NotRequired[str]
    stsPolicyDocument: NotRequired[str]

class ZeroEtlAccessTypeDef(TypedDict):
    status: NotRequired[ManagedResourceStatusType]
    cidr: NotRequired[str]

class OciDnsForwardingConfigTypeDef(TypedDict):
    domainName: NotRequired[str]
    ociDnsListenerIp: NotRequired[str]

class RebootAutonomousDatabaseInputTypeDef(TypedDict):
    autonomousDatabaseId: str
    isOnlineReboot: NotRequired[bool]

class RebootDbNodeInputTypeDef(TypedDict):
    cloudVmClusterId: str
    dbNodeId: str

class RestoreFromBackupConfigurationTypeDef(TypedDict):
    autonomousDatabaseBackupId: str
    cloneType: CloneTypeType
    cloneTableSpaceList: NotRequired[Sequence[int]]

class ShrinkAutonomousDatabaseInputTypeDef(TypedDict):
    autonomousDatabaseId: str

class StartAutonomousDatabaseInputTypeDef(TypedDict):
    autonomousDatabaseId: str

class StartDbNodeInputTypeDef(TypedDict):
    cloudVmClusterId: str
    dbNodeId: str

class StopAutonomousDatabaseInputTypeDef(TypedDict):
    autonomousDatabaseId: str

class StopDbNodeInputTypeDef(TypedDict):
    cloudVmClusterId: str
    dbNodeId: str

class SwitchoverAutonomousDatabaseInputTypeDef(TypedDict):
    autonomousDatabaseId: str
    peerDbArn: NotRequired[str]

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateAutonomousDatabaseBackupInputTypeDef(TypedDict):
    autonomousDatabaseBackupId: str
    retentionPeriodInDays: NotRequired[int]

class UpdateOdbNetworkInputTypeDef(TypedDict):
    odbNetworkId: str
    displayName: NotRequired[str]
    peeredCidrsToBeAdded: NotRequired[Sequence[str]]
    peeredCidrsToBeRemoved: NotRequired[Sequence[str]]
    s3Access: NotRequired[AccessType]
    zeroEtlAccess: NotRequired[AccessType]
    stsAccess: NotRequired[AccessType]
    kmsAccess: NotRequired[AccessType]
    s3PolicyDocument: NotRequired[str]
    stsPolicyDocument: NotRequired[str]
    kmsPolicyDocument: NotRequired[str]
    crossRegionS3RestoreSourcesToEnable: NotRequired[Sequence[str]]
    crossRegionS3RestoreSourcesToDisable: NotRequired[Sequence[str]]

class UpdateOdbPeeringConnectionInputTypeDef(TypedDict):
    odbPeeringConnectionId: str
    displayName: NotRequired[str]
    peerNetworkCidrsToBeAdded: NotRequired[Sequence[str]]
    peerNetworkCidrsToBeRemoved: NotRequired[Sequence[str]]

class AutonomousDatabaseConnectionStringsTypeDef(TypedDict):
    allConnectionStrings: NotRequired[dict[str, str]]
    dedicated: NotRequired[str]
    high: NotRequired[str]
    medium: NotRequired[str]
    low: NotRequired[str]
    profiles: NotRequired[list[DatabaseConnectionStringProfileTypeDef]]

class EncryptionKeyConfigurationInputTypeDef(TypedDict):
    awsEncryptionKey: NotRequired[AwsEncryptionKeyConfigurationInputTypeDef]

class CloneToRefreshableConfigurationTypeDef(TypedDict):
    sourceAutonomousDatabaseId: str
    refreshableMode: NotRequired[RefreshableModeType]
    autoRefreshFrequencyInSeconds: NotRequired[int]
    autoRefreshPointLagInSeconds: NotRequired[int]
    timeOfAutoRefreshStart: NotRequired[TimestampTypeDef]
    openMode: NotRequired[OpenModeType]
    cloneType: NotRequired[CloneTypeType]

class LongTermBackupScheduleTypeDef(TypedDict):
    isDisabled: NotRequired[bool]
    repeatCadence: NotRequired[RepeatCadenceType]
    retentionPeriodInDays: NotRequired[int]
    timeOfBackup: NotRequired[TimestampTypeDef]

class PointInTimeRestoreConfigurationTypeDef(TypedDict):
    sourceAutonomousDatabaseId: str
    cloneType: CloneTypeType
    timestamp: NotRequired[TimestampTypeDef]
    useLatestAvailableBackupTimestamp: NotRequired[bool]
    cloneTableSpaceList: NotRequired[Sequence[int]]

class RestoreAutonomousDatabaseInputTypeDef(TypedDict):
    autonomousDatabaseId: str
    timestamp: TimestampTypeDef

class CloudExadataInfrastructureUnallocatedResourcesTypeDef(TypedDict):
    cloudAutonomousVmClusters: NotRequired[list[CloudAutonomousVmClusterResourceDetailsTypeDef]]
    cloudExadataInfrastructureDisplayName: NotRequired[str]
    exadataStorageInTBs: NotRequired[float]
    cloudExadataInfrastructureId: NotRequired[str]
    localStorageInGBs: NotRequired[int]
    memoryInGBs: NotRequired[int]
    ocpus: NotRequired[int]

class CreateCloudVmClusterInputTypeDef(TypedDict):
    cloudExadataInfrastructureId: str
    cpuCoreCount: int
    displayName: str
    giVersion: str
    hostname: str
    sshPublicKeys: Sequence[str]
    odbNetworkId: str
    clusterName: NotRequired[str]
    dataCollectionOptions: NotRequired[DataCollectionOptionsTypeDef]
    dataStorageSizeInTBs: NotRequired[float]
    dbNodeStorageSizeInGBs: NotRequired[int]
    dbServers: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]
    isLocalBackupEnabled: NotRequired[bool]
    isSparseDiskgroupEnabled: NotRequired[bool]
    licenseModel: NotRequired[LicenseModelType]
    memorySizeInGBs: NotRequired[int]
    systemVersion: NotRequired[str]
    timeZone: NotRequired[str]
    clientToken: NotRequired[str]
    scanListenerPortTcp: NotRequired[int]

class CreateAutonomousDatabaseBackupOutputTypeDef(TypedDict):
    displayName: str
    status: ResourceStatusType
    statusReason: str
    autonomousDatabaseBackupId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAutonomousDatabaseOutputTypeDef(TypedDict):
    autonomousDatabaseId: str
    displayName: str
    status: AutonomousDatabaseResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAutonomousDatabaseWalletOutputTypeDef(TypedDict):
    autonomousDatabaseWalletFile: bytes
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCloudAutonomousVmClusterOutputTypeDef(TypedDict):
    displayName: str
    status: ResourceStatusType
    statusReason: str
    cloudAutonomousVmClusterId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCloudExadataInfrastructureOutputTypeDef(TypedDict):
    displayName: str
    status: ResourceStatusType
    statusReason: str
    cloudExadataInfrastructureId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCloudVmClusterOutputTypeDef(TypedDict):
    displayName: str
    status: ResourceStatusType
    statusReason: str
    cloudVmClusterId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateOdbNetworkOutputTypeDef(TypedDict):
    displayName: str
    status: ResourceStatusType
    statusReason: str
    odbNetworkId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateOdbPeeringConnectionOutputTypeDef(TypedDict):
    displayName: str
    status: ResourceStatusType
    statusReason: str
    odbPeeringConnectionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class FailoverAutonomousDatabaseOutputTypeDef(TypedDict):
    autonomousDatabaseId: str
    displayName: str
    status: AutonomousDatabaseResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAutonomousDatabaseBackupOutputTypeDef(TypedDict):
    autonomousDatabaseBackup: AutonomousDatabaseBackupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetAutonomousDatabaseWalletDetailsOutputTypeDef(TypedDict):
    autonomousDatabaseWalletDetails: AutonomousDatabaseWalletDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAutonomousDatabaseBackupsOutputTypeDef(TypedDict):
    autonomousDatabaseBackups: list[AutonomousDatabaseBackupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAutonomousDatabaseCharacterSetsOutputTypeDef(TypedDict):
    autonomousDatabaseCharacterSets: list[AutonomousDatabaseCharacterSetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAutonomousDatabasePeersOutputTypeDef(TypedDict):
    autonomousDatabasePeers: list[AutonomousDatabasePeerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAutonomousDatabaseVersionsOutputTypeDef(TypedDict):
    autonomousDatabaseVersions: list[AutonomousDatabaseVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAutonomousVirtualMachinesOutputTypeDef(TypedDict):
    autonomousVirtualMachines: list[AutonomousVirtualMachineSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class RebootAutonomousDatabaseOutputTypeDef(TypedDict):
    autonomousDatabaseId: str
    displayName: str
    status: AutonomousDatabaseResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class RebootDbNodeOutputTypeDef(TypedDict):
    dbNodeId: str
    status: DbNodeResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class RestoreAutonomousDatabaseOutputTypeDef(TypedDict):
    autonomousDatabaseId: str
    displayName: str
    status: AutonomousDatabaseResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class ShrinkAutonomousDatabaseOutputTypeDef(TypedDict):
    autonomousDatabaseId: str
    displayName: str
    status: AutonomousDatabaseResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartAutonomousDatabaseOutputTypeDef(TypedDict):
    autonomousDatabaseId: str
    displayName: str
    status: AutonomousDatabaseResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartDbNodeOutputTypeDef(TypedDict):
    dbNodeId: str
    status: DbNodeResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopAutonomousDatabaseOutputTypeDef(TypedDict):
    autonomousDatabaseId: str
    displayName: str
    status: AutonomousDatabaseResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopDbNodeOutputTypeDef(TypedDict):
    dbNodeId: str
    status: DbNodeResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class SwitchoverAutonomousDatabaseOutputTypeDef(TypedDict):
    autonomousDatabaseId: str
    displayName: str
    status: AutonomousDatabaseResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAutonomousDatabaseBackupOutputTypeDef(TypedDict):
    displayName: str
    status: ResourceStatusType
    statusReason: str
    autonomousDatabaseBackupId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAutonomousDatabaseOutputTypeDef(TypedDict):
    autonomousDatabaseId: str
    displayName: str
    status: AutonomousDatabaseResourceStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCloudExadataInfrastructureOutputTypeDef(TypedDict):
    displayName: str
    status: ResourceStatusType
    statusReason: str
    cloudExadataInfrastructureId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateOdbNetworkOutputTypeDef(TypedDict):
    displayName: str
    status: ResourceStatusType
    statusReason: str
    odbNetworkId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateOdbPeeringConnectionOutputTypeDef(TypedDict):
    displayName: str
    status: ResourceStatusType
    statusReason: str
    odbPeeringConnectionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ScheduledOperationDetailsTypeDef(TypedDict):
    dayOfWeek: DayOfWeekTypeDef
    scheduledStartTime: NotRequired[str]
    scheduledStopTime: NotRequired[str]

class ExadataIormConfigTypeDef(TypedDict):
    dbPlans: NotRequired[list[DbIormConfigTypeDef]]
    lifecycleDetails: NotRequired[str]
    lifecycleState: NotRequired[IormLifecycleStateType]
    objective: NotRequired[ObjectiveType]

class ListDbNodesOutputTypeDef(TypedDict):
    dbNodes: list[DbNodeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetDbNodeOutputTypeDef(TypedDict):
    dbNode: DbNodeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DbServerSummaryTypeDef(TypedDict):
    dbServerId: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    cpuCoreCount: NotRequired[int]
    dbNodeStorageSizeInGBs: NotRequired[int]
    dbServerPatchingDetails: NotRequired[DbServerPatchingDetailsTypeDef]
    displayName: NotRequired[str]
    exadataInfrastructureId: NotRequired[str]
    ocid: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    maxCpuCount: NotRequired[int]
    maxDbNodeStorageInGBs: NotRequired[int]
    maxMemoryInGBs: NotRequired[int]
    memorySizeInGBs: NotRequired[int]
    shape: NotRequired[str]
    createdAt: NotRequired[datetime]
    vmClusterIds: NotRequired[list[str]]
    computeModel: NotRequired[ComputeModelType]
    autonomousVmClusterIds: NotRequired[list[str]]
    autonomousVirtualMachineIds: NotRequired[list[str]]

class DbServerTypeDef(TypedDict):
    dbServerId: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    cpuCoreCount: NotRequired[int]
    dbNodeStorageSizeInGBs: NotRequired[int]
    dbServerPatchingDetails: NotRequired[DbServerPatchingDetailsTypeDef]
    displayName: NotRequired[str]
    exadataInfrastructureId: NotRequired[str]
    ocid: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    maxCpuCount: NotRequired[int]
    maxDbNodeStorageInGBs: NotRequired[int]
    maxMemoryInGBs: NotRequired[int]
    memorySizeInGBs: NotRequired[int]
    shape: NotRequired[str]
    createdAt: NotRequired[datetime]
    vmClusterIds: NotRequired[list[str]]
    computeModel: NotRequired[ComputeModelType]
    autonomousVmClusterIds: NotRequired[list[str]]
    autonomousVirtualMachineIds: NotRequired[list[str]]

class ListDbSystemShapesOutputTypeDef(TypedDict):
    dbSystemShapes: list[DbSystemShapeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class EncryptionKeyConfigurationTypeDef(TypedDict):
    awsEncryptionKey: NotRequired[AwsEncryptionKeyConfigurationTypeDef]
    ociEncryptionKey: NotRequired[OciEncryptionKeyConfigurationTypeDef]
    okvEncryptionKey: NotRequired[OkvEncryptionKeyConfigurationTypeDef]

class GetOciOnboardingStatusOutputTypeDef(TypedDict):
    status: OciOnboardingStatusType
    existingTenancyActivationLink: str
    newTenancyActivationLink: str
    ociIdentityDomain: OciIdentityDomainTypeDef
    autonomousDatabaseOciIntegrationIamRoles: list[OciIamRoleTypeDef]
    linkedOciTenancyId: str
    linkedOciCompartmentId: str
    subscriptionErrors: list[SubscriptionErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetOdbPeeringConnectionOutputTypeDef(TypedDict):
    odbPeeringConnection: OdbPeeringConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListGiVersionsOutputTypeDef(TypedDict):
    giVersions: list[GiVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ListAutonomousDatabaseBackupsInputPaginateTypeDef = TypedDict(
    "ListAutonomousDatabaseBackupsInputPaginateTypeDef",
    {
        "autonomousDatabaseId": str,
        "status": NotRequired[AutonomousDatabaseBackupStatusType],
        "type": NotRequired[AutonomousDatabaseBackupTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListAutonomousDatabaseCharacterSetsInputPaginateTypeDef(TypedDict):
    characterSetType: NotRequired[CharacterSetTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAutonomousDatabaseClonesInputPaginateTypeDef(TypedDict):
    autonomousDatabaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAutonomousDatabasePeersInputPaginateTypeDef(TypedDict):
    autonomousDatabaseId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAutonomousDatabaseVersionsInputPaginateTypeDef(TypedDict):
    dbWorkload: NotRequired[DbWorkloadType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAutonomousDatabasesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAutonomousVirtualMachinesInputPaginateTypeDef(TypedDict):
    cloudAutonomousVmClusterId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCloudAutonomousVmClustersInputPaginateTypeDef(TypedDict):
    cloudExadataInfrastructureId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCloudExadataInfrastructuresInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCloudVmClustersInputPaginateTypeDef(TypedDict):
    cloudExadataInfrastructureId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDbNodesInputPaginateTypeDef(TypedDict):
    cloudVmClusterId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDbServersInputPaginateTypeDef(TypedDict):
    cloudExadataInfrastructureId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDbSystemShapesInputPaginateTypeDef(TypedDict):
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGiVersionsInputPaginateTypeDef(TypedDict):
    shape: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOdbNetworksInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOdbPeeringConnectionsInputPaginateTypeDef(TypedDict):
    odbNetworkId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSystemVersionsInputPaginateTypeDef(TypedDict):
    giVersion: str
    shape: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOdbPeeringConnectionsOutputTypeDef(TypedDict):
    odbPeeringConnections: list[OdbPeeringConnectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSystemVersionsOutputTypeDef(TypedDict):
    systemVersions: list[SystemVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class MaintenanceWindowOutputTypeDef(TypedDict):
    customActionTimeoutInMins: NotRequired[int]
    daysOfWeek: NotRequired[list[DayOfWeekTypeDef]]
    hoursOfDay: NotRequired[list[int]]
    isCustomActionTimeoutEnabled: NotRequired[bool]
    leadTimeInWeeks: NotRequired[int]
    months: NotRequired[list[MonthTypeDef]]
    patchingMode: NotRequired[PatchingModeTypeType]
    preference: NotRequired[PreferenceTypeType]
    skipRu: NotRequired[bool]
    weeksOfMonth: NotRequired[list[int]]

class MaintenanceWindowTypeDef(TypedDict):
    customActionTimeoutInMins: NotRequired[int]
    daysOfWeek: NotRequired[Sequence[DayOfWeekTypeDef]]
    hoursOfDay: NotRequired[Sequence[int]]
    isCustomActionTimeoutEnabled: NotRequired[bool]
    leadTimeInWeeks: NotRequired[int]
    months: NotRequired[Sequence[MonthTypeDef]]
    patchingMode: NotRequired[PatchingModeTypeType]
    preference: NotRequired[PreferenceTypeType]
    skipRu: NotRequired[bool]
    weeksOfMonth: NotRequired[Sequence[int]]

class ManagedServicesTypeDef(TypedDict):
    serviceNetworkArn: NotRequired[str]
    resourceGatewayArn: NotRequired[str]
    managedServicesIpv4Cidrs: NotRequired[list[str]]
    serviceNetworkEndpoint: NotRequired[ServiceNetworkEndpointTypeDef]
    managedS3BackupAccess: NotRequired[ManagedS3BackupAccessTypeDef]
    zeroEtlAccess: NotRequired[ZeroEtlAccessTypeDef]
    s3Access: NotRequired[S3AccessTypeDef]
    stsAccess: NotRequired[StsAccessTypeDef]
    kmsAccess: NotRequired[KmsAccessTypeDef]
    crossRegionS3RestoreSourcesAccess: NotRequired[list[CrossRegionS3RestoreSourcesAccessTypeDef]]

LongTermBackupScheduleUnionTypeDef = Union[
    LongTermBackupScheduleTypeDef, LongTermBackupScheduleOutputTypeDef
]

class SourceConfigurationTypeDef(TypedDict):
    databaseClone: NotRequired[DatabaseCloneConfigurationTypeDef]
    restoreFromBackup: NotRequired[RestoreFromBackupConfigurationTypeDef]
    pointInTimeRestore: NotRequired[PointInTimeRestoreConfigurationTypeDef]
    crossRegionDataGuard: NotRequired[CrossRegionDataGuardConfigurationTypeDef]
    crossRegionDisasterRecovery: NotRequired[CrossRegionDisasterRecoveryConfigurationTypeDef]
    cloneToRefreshable: NotRequired[CloneToRefreshableConfigurationTypeDef]

class GetCloudExadataInfrastructureUnallocatedResourcesOutputTypeDef(TypedDict):
    cloudExadataInfrastructureUnallocatedResources: (
        CloudExadataInfrastructureUnallocatedResourcesTypeDef
    )
    ResponseMetadata: ResponseMetadataTypeDef

class CloudVmClusterSummaryTypeDef(TypedDict):
    cloudVmClusterId: str
    displayName: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    cloudVmClusterArn: NotRequired[str]
    cloudExadataInfrastructureId: NotRequired[str]
    cloudExadataInfrastructureArn: NotRequired[str]
    clusterName: NotRequired[str]
    cpuCoreCount: NotRequired[int]
    dataCollectionOptions: NotRequired[DataCollectionOptionsTypeDef]
    dataStorageSizeInTBs: NotRequired[float]
    dbNodeStorageSizeInGBs: NotRequired[int]
    dbServers: NotRequired[list[str]]
    diskRedundancy: NotRequired[DiskRedundancyType]
    giVersion: NotRequired[str]
    hostname: NotRequired[str]
    iormConfigCache: NotRequired[ExadataIormConfigTypeDef]
    isLocalBackupEnabled: NotRequired[bool]
    isSparseDiskgroupEnabled: NotRequired[bool]
    lastUpdateHistoryEntryId: NotRequired[str]
    licenseModel: NotRequired[LicenseModelType]
    listenerPort: NotRequired[int]
    memorySizeInGBs: NotRequired[int]
    nodeCount: NotRequired[int]
    ocid: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    ociUrl: NotRequired[str]
    domain: NotRequired[str]
    scanDnsName: NotRequired[str]
    scanDnsRecordId: NotRequired[str]
    scanIpIds: NotRequired[list[str]]
    shape: NotRequired[str]
    sshPublicKeys: NotRequired[list[str]]
    storageSizeInGBs: NotRequired[int]
    systemVersion: NotRequired[str]
    createdAt: NotRequired[datetime]
    timeZone: NotRequired[str]
    vipIds: NotRequired[list[str]]
    odbNetworkId: NotRequired[str]
    odbNetworkArn: NotRequired[str]
    percentProgress: NotRequired[float]
    computeModel: NotRequired[ComputeModelType]
    iamRoles: NotRequired[list[IamRoleTypeDef]]

class CloudVmClusterTypeDef(TypedDict):
    cloudVmClusterId: str
    displayName: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    cloudVmClusterArn: NotRequired[str]
    cloudExadataInfrastructureId: NotRequired[str]
    cloudExadataInfrastructureArn: NotRequired[str]
    clusterName: NotRequired[str]
    cpuCoreCount: NotRequired[int]
    dataCollectionOptions: NotRequired[DataCollectionOptionsTypeDef]
    dataStorageSizeInTBs: NotRequired[float]
    dbNodeStorageSizeInGBs: NotRequired[int]
    dbServers: NotRequired[list[str]]
    diskRedundancy: NotRequired[DiskRedundancyType]
    giVersion: NotRequired[str]
    hostname: NotRequired[str]
    iormConfigCache: NotRequired[ExadataIormConfigTypeDef]
    isLocalBackupEnabled: NotRequired[bool]
    isSparseDiskgroupEnabled: NotRequired[bool]
    lastUpdateHistoryEntryId: NotRequired[str]
    licenseModel: NotRequired[LicenseModelType]
    listenerPort: NotRequired[int]
    memorySizeInGBs: NotRequired[int]
    nodeCount: NotRequired[int]
    ocid: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    ociUrl: NotRequired[str]
    domain: NotRequired[str]
    scanDnsName: NotRequired[str]
    scanDnsRecordId: NotRequired[str]
    scanIpIds: NotRequired[list[str]]
    shape: NotRequired[str]
    sshPublicKeys: NotRequired[list[str]]
    storageSizeInGBs: NotRequired[int]
    systemVersion: NotRequired[str]
    createdAt: NotRequired[datetime]
    timeZone: NotRequired[str]
    vipIds: NotRequired[list[str]]
    odbNetworkId: NotRequired[str]
    odbNetworkArn: NotRequired[str]
    percentProgress: NotRequired[float]
    computeModel: NotRequired[ComputeModelType]
    iamRoles: NotRequired[list[IamRoleTypeDef]]

class ListDbServersOutputTypeDef(TypedDict):
    dbServers: list[DbServerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetDbServerOutputTypeDef(TypedDict):
    dbServer: DbServerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EncryptionSummaryTypeDef(TypedDict):
    encryptionKeyProvider: NotRequired[EncryptionKeyProviderType]
    encryptionKeyConfiguration: NotRequired[EncryptionKeyConfigurationTypeDef]

class CloudAutonomousVmClusterSummaryTypeDef(TypedDict):
    cloudAutonomousVmClusterId: str
    cloudAutonomousVmClusterArn: NotRequired[str]
    odbNetworkId: NotRequired[str]
    odbNetworkArn: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    percentProgress: NotRequired[float]
    displayName: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    cloudExadataInfrastructureId: NotRequired[str]
    cloudExadataInfrastructureArn: NotRequired[str]
    autonomousDataStoragePercentage: NotRequired[float]
    autonomousDataStorageSizeInTBs: NotRequired[float]
    availableAutonomousDataStorageSizeInTBs: NotRequired[float]
    availableContainerDatabases: NotRequired[int]
    availableCpus: NotRequired[float]
    computeModel: NotRequired[ComputeModelType]
    cpuCoreCount: NotRequired[int]
    cpuCoreCountPerNode: NotRequired[int]
    cpuPercentage: NotRequired[float]
    dataStorageSizeInGBs: NotRequired[float]
    dataStorageSizeInTBs: NotRequired[float]
    dbNodeStorageSizeInGBs: NotRequired[int]
    dbServers: NotRequired[list[str]]
    description: NotRequired[str]
    domain: NotRequired[str]
    exadataStorageInTBsLowestScaledValue: NotRequired[float]
    hostname: NotRequired[str]
    ocid: NotRequired[str]
    ociUrl: NotRequired[str]
    isMtlsEnabledVmCluster: NotRequired[bool]
    licenseModel: NotRequired[LicenseModelType]
    maintenanceWindow: NotRequired[MaintenanceWindowOutputTypeDef]
    maxAcdsLowestScaledValue: NotRequired[int]
    memoryPerOracleComputeUnitInGBs: NotRequired[int]
    memorySizeInGBs: NotRequired[int]
    nodeCount: NotRequired[int]
    nonProvisionableAutonomousContainerDatabases: NotRequired[int]
    provisionableAutonomousContainerDatabases: NotRequired[int]
    provisionedAutonomousContainerDatabases: NotRequired[int]
    provisionedCpus: NotRequired[float]
    reclaimableCpus: NotRequired[float]
    reservedCpus: NotRequired[float]
    scanListenerPortNonTls: NotRequired[int]
    scanListenerPortTls: NotRequired[int]
    shape: NotRequired[str]
    createdAt: NotRequired[datetime]
    timeDatabaseSslCertificateExpires: NotRequired[datetime]
    timeOrdsCertificateExpires: NotRequired[datetime]
    timeZone: NotRequired[str]
    totalContainerDatabases: NotRequired[int]
    iamRoles: NotRequired[list[IamRoleTypeDef]]

class CloudAutonomousVmClusterTypeDef(TypedDict):
    cloudAutonomousVmClusterId: str
    cloudAutonomousVmClusterArn: NotRequired[str]
    odbNetworkId: NotRequired[str]
    odbNetworkArn: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    percentProgress: NotRequired[float]
    displayName: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    cloudExadataInfrastructureId: NotRequired[str]
    cloudExadataInfrastructureArn: NotRequired[str]
    autonomousDataStoragePercentage: NotRequired[float]
    autonomousDataStorageSizeInTBs: NotRequired[float]
    availableAutonomousDataStorageSizeInTBs: NotRequired[float]
    availableContainerDatabases: NotRequired[int]
    availableCpus: NotRequired[float]
    computeModel: NotRequired[ComputeModelType]
    cpuCoreCount: NotRequired[int]
    cpuCoreCountPerNode: NotRequired[int]
    cpuPercentage: NotRequired[float]
    dataStorageSizeInGBs: NotRequired[float]
    dataStorageSizeInTBs: NotRequired[float]
    dbNodeStorageSizeInGBs: NotRequired[int]
    dbServers: NotRequired[list[str]]
    description: NotRequired[str]
    domain: NotRequired[str]
    exadataStorageInTBsLowestScaledValue: NotRequired[float]
    hostname: NotRequired[str]
    ocid: NotRequired[str]
    ociUrl: NotRequired[str]
    isMtlsEnabledVmCluster: NotRequired[bool]
    licenseModel: NotRequired[LicenseModelType]
    maintenanceWindow: NotRequired[MaintenanceWindowOutputTypeDef]
    maxAcdsLowestScaledValue: NotRequired[int]
    memoryPerOracleComputeUnitInGBs: NotRequired[int]
    memorySizeInGBs: NotRequired[int]
    nodeCount: NotRequired[int]
    nonProvisionableAutonomousContainerDatabases: NotRequired[int]
    provisionableAutonomousContainerDatabases: NotRequired[int]
    provisionedAutonomousContainerDatabases: NotRequired[int]
    provisionedCpus: NotRequired[float]
    reclaimableCpus: NotRequired[float]
    reservedCpus: NotRequired[float]
    scanListenerPortNonTls: NotRequired[int]
    scanListenerPortTls: NotRequired[int]
    shape: NotRequired[str]
    createdAt: NotRequired[datetime]
    timeDatabaseSslCertificateExpires: NotRequired[datetime]
    timeOrdsCertificateExpires: NotRequired[datetime]
    timeZone: NotRequired[str]
    totalContainerDatabases: NotRequired[int]
    iamRoles: NotRequired[list[IamRoleTypeDef]]

class CloudExadataInfrastructureSummaryTypeDef(TypedDict):
    cloudExadataInfrastructureId: str
    displayName: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    cloudExadataInfrastructureArn: NotRequired[str]
    activatedStorageCount: NotRequired[int]
    additionalStorageCount: NotRequired[int]
    availableStorageSizeInGBs: NotRequired[int]
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    computeCount: NotRequired[int]
    cpuCount: NotRequired[int]
    customerContactsToSendToOCI: NotRequired[list[CustomerContactTypeDef]]
    dataStorageSizeInTBs: NotRequired[float]
    dbNodeStorageSizeInGBs: NotRequired[int]
    dbServerVersion: NotRequired[str]
    lastMaintenanceRunId: NotRequired[str]
    maintenanceWindow: NotRequired[MaintenanceWindowOutputTypeDef]
    maxCpuCount: NotRequired[int]
    maxDataStorageInTBs: NotRequired[float]
    maxDbNodeStorageSizeInGBs: NotRequired[int]
    maxMemoryInGBs: NotRequired[int]
    memorySizeInGBs: NotRequired[int]
    monthlyDbServerVersion: NotRequired[str]
    monthlyStorageServerVersion: NotRequired[str]
    nextMaintenanceRunId: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    ociUrl: NotRequired[str]
    ocid: NotRequired[str]
    shape: NotRequired[str]
    storageCount: NotRequired[int]
    storageServerVersion: NotRequired[str]
    createdAt: NotRequired[datetime]
    totalStorageSizeInGBs: NotRequired[int]
    percentProgress: NotRequired[float]
    databaseServerType: NotRequired[str]
    storageServerType: NotRequired[str]
    computeModel: NotRequired[ComputeModelType]

class CloudExadataInfrastructureTypeDef(TypedDict):
    cloudExadataInfrastructureId: str
    displayName: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    cloudExadataInfrastructureArn: NotRequired[str]
    activatedStorageCount: NotRequired[int]
    additionalStorageCount: NotRequired[int]
    availableStorageSizeInGBs: NotRequired[int]
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    computeCount: NotRequired[int]
    cpuCount: NotRequired[int]
    customerContactsToSendToOCI: NotRequired[list[CustomerContactTypeDef]]
    dataStorageSizeInTBs: NotRequired[float]
    dbNodeStorageSizeInGBs: NotRequired[int]
    dbServerVersion: NotRequired[str]
    lastMaintenanceRunId: NotRequired[str]
    maintenanceWindow: NotRequired[MaintenanceWindowOutputTypeDef]
    maxCpuCount: NotRequired[int]
    maxDataStorageInTBs: NotRequired[float]
    maxDbNodeStorageSizeInGBs: NotRequired[int]
    maxMemoryInGBs: NotRequired[int]
    memorySizeInGBs: NotRequired[int]
    monthlyDbServerVersion: NotRequired[str]
    monthlyStorageServerVersion: NotRequired[str]
    nextMaintenanceRunId: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    ociUrl: NotRequired[str]
    ocid: NotRequired[str]
    shape: NotRequired[str]
    storageCount: NotRequired[int]
    storageServerVersion: NotRequired[str]
    createdAt: NotRequired[datetime]
    totalStorageSizeInGBs: NotRequired[int]
    percentProgress: NotRequired[float]
    databaseServerType: NotRequired[str]
    storageServerType: NotRequired[str]
    computeModel: NotRequired[ComputeModelType]

MaintenanceWindowUnionTypeDef = Union[MaintenanceWindowTypeDef, MaintenanceWindowOutputTypeDef]

class OdbNetworkSummaryTypeDef(TypedDict):
    odbNetworkId: str
    displayName: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    odbNetworkArn: NotRequired[str]
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    clientSubnetCidr: NotRequired[str]
    backupSubnetCidr: NotRequired[str]
    customDomainName: NotRequired[str]
    defaultDnsPrefix: NotRequired[str]
    peeredCidrs: NotRequired[list[str]]
    ociNetworkAnchorId: NotRequired[str]
    ociNetworkAnchorUrl: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    ociVcnId: NotRequired[str]
    ociVcnUrl: NotRequired[str]
    ociDnsForwardingConfigs: NotRequired[list[OciDnsForwardingConfigTypeDef]]
    createdAt: NotRequired[datetime]
    percentProgress: NotRequired[float]
    managedServices: NotRequired[ManagedServicesTypeDef]
    ec2PlacementGroupIds: NotRequired[list[str]]

class OdbNetworkTypeDef(TypedDict):
    odbNetworkId: str
    displayName: NotRequired[str]
    status: NotRequired[ResourceStatusType]
    statusReason: NotRequired[str]
    odbNetworkArn: NotRequired[str]
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    clientSubnetCidr: NotRequired[str]
    backupSubnetCidr: NotRequired[str]
    customDomainName: NotRequired[str]
    defaultDnsPrefix: NotRequired[str]
    peeredCidrs: NotRequired[list[str]]
    ociNetworkAnchorId: NotRequired[str]
    ociNetworkAnchorUrl: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    ociVcnId: NotRequired[str]
    ociVcnUrl: NotRequired[str]
    ociDnsForwardingConfigs: NotRequired[list[OciDnsForwardingConfigTypeDef]]
    createdAt: NotRequired[datetime]
    percentProgress: NotRequired[float]
    managedServices: NotRequired[ManagedServicesTypeDef]
    ec2PlacementGroupIds: NotRequired[list[str]]

class UpdateAutonomousDatabaseInputTypeDef(TypedDict):
    autonomousDatabaseId: str
    adminPassword: NotRequired[str]
    computeCount: NotRequired[float]
    cpuCoreCount: NotRequired[int]
    dataStorageSizeInTBs: NotRequired[int]
    dataStorageSizeInGBs: NotRequired[int]
    displayName: NotRequired[str]
    dbName: NotRequired[str]
    dbVersion: NotRequired[str]
    dbWorkload: NotRequired[DbWorkloadType]
    dbToolsDetails: NotRequired[Sequence[DatabaseToolTypeDef]]
    databaseEdition: NotRequired[DatabaseEditionType]
    licenseModel: NotRequired[LicenseModelType]
    isAutoScalingEnabled: NotRequired[bool]
    isAutoScalingForStorageEnabled: NotRequired[bool]
    isBackupRetentionLocked: NotRequired[bool]
    isLocalDataGuardEnabled: NotRequired[bool]
    isMtlsConnectionRequired: NotRequired[bool]
    isRefreshableClone: NotRequired[bool]
    isDisconnectPeer: NotRequired[bool]
    backupRetentionPeriodInDays: NotRequired[int]
    byolComputeCountLimit: NotRequired[float]
    localAdgAutoFailoverMaxDataLossLimit: NotRequired[int]
    autonomousMaintenanceScheduleType: NotRequired[AutonomousMaintenanceScheduleTypeType]
    customerContactsToSendToOCI: NotRequired[Sequence[CustomerContactTypeDef]]
    scheduledOperations: NotRequired[Sequence[ScheduledOperationDetailsTypeDef]]
    longTermBackupSchedule: NotRequired[LongTermBackupScheduleUnionTypeDef]
    openMode: NotRequired[OpenModeType]
    permissionLevel: NotRequired[PermissionLevelType]
    refreshableMode: NotRequired[RefreshableModeType]
    privateEndpointIp: NotRequired[str]
    privateEndpointLabel: NotRequired[str]
    peerDbId: NotRequired[str]
    resourcePoolLeaderId: NotRequired[str]
    resourcePoolSummary: NotRequired[ResourcePoolSummaryTypeDef]
    standbyAllowlistedIpsSource: NotRequired[StandbyAllowlistedIpsSourceType]
    standbyAllowlistedIps: NotRequired[Sequence[str]]
    allowlistedIps: NotRequired[Sequence[str]]
    autoRefreshFrequencyInSeconds: NotRequired[int]
    autoRefreshPointLagInSeconds: NotRequired[int]
    timeOfAutoRefreshStart: NotRequired[TimestampTypeDef]
    encryptionKeyProvider: NotRequired[EncryptionKeyProviderInputType]
    encryptionKeyConfiguration: NotRequired[EncryptionKeyConfigurationInputTypeDef]

class CreateAutonomousDatabaseInputTypeDef(TypedDict):
    odbNetworkId: NotRequired[str]
    displayName: NotRequired[str]
    dbName: NotRequired[str]
    adminPassword: NotRequired[str]
    computeCount: NotRequired[float]
    dataStorageSizeInTBs: NotRequired[int]
    dataStorageSizeInGBs: NotRequired[int]
    dbWorkload: NotRequired[DbWorkloadType]
    isAutoScalingEnabled: NotRequired[bool]
    isAutoScalingForStorageEnabled: NotRequired[bool]
    licenseModel: NotRequired[LicenseModelType]
    characterSet: NotRequired[str]
    ncharacterSet: NotRequired[str]
    dbVersion: NotRequired[str]
    databaseEdition: NotRequired[DatabaseEditionType]
    standbyAllowlistedIpsSource: NotRequired[StandbyAllowlistedIpsSourceType]
    autonomousMaintenanceScheduleType: NotRequired[AutonomousMaintenanceScheduleTypeType]
    backupRetentionPeriodInDays: NotRequired[int]
    byolComputeCountLimit: NotRequired[float]
    cpuCoreCount: NotRequired[int]
    customerContactsToSendToOCI: NotRequired[Sequence[CustomerContactTypeDef]]
    privateEndpointIp: NotRequired[str]
    privateEndpointLabel: NotRequired[str]
    resourcePoolLeaderId: NotRequired[str]
    resourcePoolSummary: NotRequired[ResourcePoolSummaryTypeDef]
    scheduledOperations: NotRequired[Sequence[ScheduledOperationDetailsTypeDef]]
    standbyAllowlistedIps: NotRequired[Sequence[str]]
    allowlistedIps: NotRequired[Sequence[str]]
    transportableTablespace: NotRequired[TransportableTablespaceTypeDef]
    isBackupRetentionLocked: NotRequired[bool]
    isLocalDataGuardEnabled: NotRequired[bool]
    isMtlsConnectionRequired: NotRequired[bool]
    dbToolsDetails: NotRequired[Sequence[DatabaseToolTypeDef]]
    source: NotRequired[SourceTypeType]
    sourceConfiguration: NotRequired[SourceConfigurationTypeDef]
    encryptionKeyProvider: NotRequired[EncryptionKeyProviderInputType]
    encryptionKeyConfiguration: NotRequired[EncryptionKeyConfigurationInputTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class ListCloudVmClustersOutputTypeDef(TypedDict):
    cloudVmClusters: list[CloudVmClusterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetCloudVmClusterOutputTypeDef(TypedDict):
    cloudVmCluster: CloudVmClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AutonomousDatabaseSummaryTypeDef(TypedDict):
    autonomousDatabaseId: NotRequired[str]
    autonomousDatabaseArn: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    percentProgress: NotRequired[float]
    ocid: NotRequired[str]
    ociUrl: NotRequired[str]
    displayName: NotRequired[str]
    dbName: NotRequired[str]
    sourceId: NotRequired[str]
    status: NotRequired[AutonomousDatabaseResourceStatusType]
    statusReason: NotRequired[str]
    databaseType: NotRequired[DatabaseTypeType]
    dbVersion: NotRequired[str]
    dbWorkload: NotRequired[DbWorkloadType]
    characterSet: NotRequired[str]
    ncharacterSet: NotRequired[str]
    databaseEdition: NotRequired[DatabaseEditionType]
    licenseModel: NotRequired[LicenseModelType]
    openMode: NotRequired[OpenModeType]
    permissionLevel: NotRequired[PermissionLevelType]
    isMtlsConnectionRequired: NotRequired[bool]
    autonomousMaintenanceScheduleType: NotRequired[AutonomousMaintenanceScheduleTypeType]
    netServicesArchitecture: NotRequired[NetServicesArchitectureType]
    availableUpgradeVersions: NotRequired[list[str]]
    byolComputeCountLimit: NotRequired[int]
    connectionStringDetails: NotRequired[AutonomousDatabaseConnectionStringsTypeDef]
    serviceConsoleUrl: NotRequired[str]
    sqlWebDeveloperUrl: NotRequired[str]
    customerContacts: NotRequired[list[CustomerContactTypeDef]]
    apexDetails: NotRequired[AutonomousDatabaseApexTypeDef]
    standbyDb: NotRequired[DatabaseStandbySummaryTypeDef]
    localStandbyDb: NotRequired[DatabaseStandbySummaryTypeDef]
    dataSafeStatus: NotRequired[DataSafeStatusType]
    databaseManagementStatus: NotRequired[DatabaseManagementStatusType]
    operationsInsightsStatus: NotRequired[OperationsInsightsStatusType]
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    maintenanceTargetComponent: NotRequired[str]
    connectionUrls: NotRequired[AutonomousDatabaseConnectionUrlsTypeDef]
    dbToolsDetails: NotRequired[list[DatabaseToolTypeDef]]
    scheduledOperations: NotRequired[list[ScheduledOperationDetailsTypeDef]]
    resourcePoolLeaderId: NotRequired[str]
    computeCount: NotRequired[float]
    computeModel: NotRequired[ComputeModelType]
    cpuCoreCount: NotRequired[int]
    memoryPerOracleComputeUnitInGBs: NotRequired[int]
    provisionableCpus: NotRequired[list[int]]
    isAutoScalingEnabled: NotRequired[bool]
    dataStorageSizeInTBs: NotRequired[float]
    dataStorageSizeInGBs: NotRequired[int]
    usedDataStorageSizeInTBs: NotRequired[float]
    usedDataStorageSizeInGBs: NotRequired[int]
    actualUsedDataStorageSizeInTBs: NotRequired[float]
    allocatedStorageSizeInTBs: NotRequired[float]
    inMemoryAreaInGBs: NotRequired[int]
    isAutoScalingForStorageEnabled: NotRequired[bool]
    odbNetworkId: NotRequired[str]
    odbNetworkArn: NotRequired[str]
    privateEndpoint: NotRequired[str]
    privateEndpointIp: NotRequired[str]
    privateEndpointLabel: NotRequired[str]
    allowlistedIps: NotRequired[list[str]]
    standbyAllowlistedIps: NotRequired[list[str]]
    standbyAllowlistedIpsSource: NotRequired[StandbyAllowlistedIpsSourceType]
    isLocalDataGuardEnabled: NotRequired[bool]
    isRemoteDataGuardEnabled: NotRequired[bool]
    localDisasterRecoveryType: NotRequired[DisasterRecoveryTypeType]
    role: NotRequired[DataGuardRoleType]
    peerDbIds: NotRequired[list[str]]
    failedDataRecoveryInSeconds: NotRequired[int]
    localAdgAutoFailoverMaxDataLossLimit: NotRequired[int]
    remoteDisasterRecoveryConfiguration: NotRequired[DisasterRecoveryConfigurationTypeDef]
    isRefreshableClone: NotRequired[bool]
    refreshableMode: NotRequired[RefreshableModeType]
    refreshableStatus: NotRequired[RefreshableStatusType]
    autoRefreshFrequencyInSeconds: NotRequired[int]
    autoRefreshPointLagInSeconds: NotRequired[int]
    isReconnectCloneEnabled: NotRequired[bool]
    cloneTableSpaceList: NotRequired[list[int]]
    backupRetentionPeriodInDays: NotRequired[int]
    longTermBackupSchedule: NotRequired[LongTermBackupScheduleOutputTypeDef]
    isBackupRetentionLocked: NotRequired[bool]
    totalBackupStorageSizeInGBs: NotRequired[float]
    resourcePoolSummary: NotRequired[ResourcePoolSummaryTypeDef]
    encryptionSummary: NotRequired[EncryptionSummaryTypeDef]
    createdAt: NotRequired[datetime]
    timeOfLastBackup: NotRequired[datetime]
    timeMaintenanceBegin: NotRequired[datetime]
    timeMaintenanceEnd: NotRequired[datetime]
    timeLocalDataGuardEnabled: NotRequired[datetime]
    timeDataGuardRoleChanged: NotRequired[datetime]
    timeOfLastSwitchover: NotRequired[datetime]
    timeOfLastFailover: NotRequired[datetime]
    timeOfLastRefresh: NotRequired[datetime]
    timeOfLastRefreshPoint: NotRequired[datetime]
    timeOfNextRefresh: NotRequired[datetime]
    timeOfAutoRefreshStart: NotRequired[datetime]
    timeDeletionOfFreeAutonomousDatabase: NotRequired[datetime]
    timeReclamationOfFreeAutonomousDatabase: NotRequired[datetime]
    timeDisasterRecoveryRoleChanged: NotRequired[datetime]
    timeUntilReconnectCloneEnabled: NotRequired[datetime]
    nextLongTermBackupTimeStamp: NotRequired[datetime]
    timeUndeleted: NotRequired[datetime]

class AutonomousDatabaseTypeDef(TypedDict):
    autonomousDatabaseId: NotRequired[str]
    autonomousDatabaseArn: NotRequired[str]
    ociResourceAnchorName: NotRequired[str]
    percentProgress: NotRequired[float]
    ocid: NotRequired[str]
    ociUrl: NotRequired[str]
    displayName: NotRequired[str]
    dbName: NotRequired[str]
    sourceId: NotRequired[str]
    status: NotRequired[AutonomousDatabaseResourceStatusType]
    statusReason: NotRequired[str]
    databaseType: NotRequired[DatabaseTypeType]
    dbVersion: NotRequired[str]
    dbWorkload: NotRequired[DbWorkloadType]
    characterSet: NotRequired[str]
    ncharacterSet: NotRequired[str]
    databaseEdition: NotRequired[DatabaseEditionType]
    licenseModel: NotRequired[LicenseModelType]
    openMode: NotRequired[OpenModeType]
    permissionLevel: NotRequired[PermissionLevelType]
    isMtlsConnectionRequired: NotRequired[bool]
    autonomousMaintenanceScheduleType: NotRequired[AutonomousMaintenanceScheduleTypeType]
    netServicesArchitecture: NotRequired[NetServicesArchitectureType]
    availableUpgradeVersions: NotRequired[list[str]]
    byolComputeCountLimit: NotRequired[int]
    connectionStringDetails: NotRequired[AutonomousDatabaseConnectionStringsTypeDef]
    serviceConsoleUrl: NotRequired[str]
    sqlWebDeveloperUrl: NotRequired[str]
    customerContacts: NotRequired[list[CustomerContactTypeDef]]
    apexDetails: NotRequired[AutonomousDatabaseApexTypeDef]
    standbyDb: NotRequired[DatabaseStandbySummaryTypeDef]
    localStandbyDb: NotRequired[DatabaseStandbySummaryTypeDef]
    dataSafeStatus: NotRequired[DataSafeStatusType]
    databaseManagementStatus: NotRequired[DatabaseManagementStatusType]
    operationsInsightsStatus: NotRequired[OperationsInsightsStatusType]
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    maintenanceTargetComponent: NotRequired[str]
    connectionUrls: NotRequired[AutonomousDatabaseConnectionUrlsTypeDef]
    dbToolsDetails: NotRequired[list[DatabaseToolTypeDef]]
    scheduledOperations: NotRequired[list[ScheduledOperationDetailsTypeDef]]
    resourcePoolLeaderId: NotRequired[str]
    computeCount: NotRequired[float]
    computeModel: NotRequired[ComputeModelType]
    cpuCoreCount: NotRequired[int]
    memoryPerOracleComputeUnitInGBs: NotRequired[int]
    provisionableCpus: NotRequired[list[int]]
    isAutoScalingEnabled: NotRequired[bool]
    dataStorageSizeInTBs: NotRequired[float]
    dataStorageSizeInGBs: NotRequired[int]
    usedDataStorageSizeInTBs: NotRequired[float]
    usedDataStorageSizeInGBs: NotRequired[int]
    actualUsedDataStorageSizeInTBs: NotRequired[float]
    allocatedStorageSizeInTBs: NotRequired[float]
    inMemoryAreaInGBs: NotRequired[int]
    isAutoScalingForStorageEnabled: NotRequired[bool]
    odbNetworkId: NotRequired[str]
    odbNetworkArn: NotRequired[str]
    privateEndpoint: NotRequired[str]
    privateEndpointIp: NotRequired[str]
    privateEndpointLabel: NotRequired[str]
    allowlistedIps: NotRequired[list[str]]
    standbyAllowlistedIps: NotRequired[list[str]]
    standbyAllowlistedIpsSource: NotRequired[StandbyAllowlistedIpsSourceType]
    isLocalDataGuardEnabled: NotRequired[bool]
    isRemoteDataGuardEnabled: NotRequired[bool]
    localDisasterRecoveryType: NotRequired[DisasterRecoveryTypeType]
    role: NotRequired[DataGuardRoleType]
    peerDbIds: NotRequired[list[str]]
    failedDataRecoveryInSeconds: NotRequired[int]
    localAdgAutoFailoverMaxDataLossLimit: NotRequired[int]
    remoteDisasterRecoveryConfiguration: NotRequired[DisasterRecoveryConfigurationTypeDef]
    isRefreshableClone: NotRequired[bool]
    refreshableMode: NotRequired[RefreshableModeType]
    refreshableStatus: NotRequired[RefreshableStatusType]
    autoRefreshFrequencyInSeconds: NotRequired[int]
    autoRefreshPointLagInSeconds: NotRequired[int]
    isReconnectCloneEnabled: NotRequired[bool]
    cloneTableSpaceList: NotRequired[list[int]]
    backupRetentionPeriodInDays: NotRequired[int]
    longTermBackupSchedule: NotRequired[LongTermBackupScheduleOutputTypeDef]
    isBackupRetentionLocked: NotRequired[bool]
    totalBackupStorageSizeInGBs: NotRequired[float]
    resourcePoolSummary: NotRequired[ResourcePoolSummaryTypeDef]
    encryptionSummary: NotRequired[EncryptionSummaryTypeDef]
    createdAt: NotRequired[datetime]
    timeOfLastBackup: NotRequired[datetime]
    timeMaintenanceBegin: NotRequired[datetime]
    timeMaintenanceEnd: NotRequired[datetime]
    timeLocalDataGuardEnabled: NotRequired[datetime]
    timeDataGuardRoleChanged: NotRequired[datetime]
    timeOfLastSwitchover: NotRequired[datetime]
    timeOfLastFailover: NotRequired[datetime]
    timeOfLastRefresh: NotRequired[datetime]
    timeOfLastRefreshPoint: NotRequired[datetime]
    timeOfNextRefresh: NotRequired[datetime]
    timeOfAutoRefreshStart: NotRequired[datetime]
    timeDeletionOfFreeAutonomousDatabase: NotRequired[datetime]
    timeReclamationOfFreeAutonomousDatabase: NotRequired[datetime]
    timeDisasterRecoveryRoleChanged: NotRequired[datetime]
    timeUntilReconnectCloneEnabled: NotRequired[datetime]
    nextLongTermBackupTimeStamp: NotRequired[datetime]
    timeUndeleted: NotRequired[datetime]

class ListCloudAutonomousVmClustersOutputTypeDef(TypedDict):
    cloudAutonomousVmClusters: list[CloudAutonomousVmClusterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetCloudAutonomousVmClusterOutputTypeDef(TypedDict):
    cloudAutonomousVmCluster: CloudAutonomousVmClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCloudExadataInfrastructuresOutputTypeDef(TypedDict):
    cloudExadataInfrastructures: list[CloudExadataInfrastructureSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetCloudExadataInfrastructureOutputTypeDef(TypedDict):
    cloudExadataInfrastructure: CloudExadataInfrastructureTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCloudAutonomousVmClusterInputTypeDef(TypedDict):
    cloudExadataInfrastructureId: str
    odbNetworkId: str
    displayName: str
    autonomousDataStorageSizeInTBs: float
    cpuCoreCountPerNode: int
    memoryPerOracleComputeUnitInGBs: int
    totalContainerDatabases: int
    clientToken: NotRequired[str]
    dbServers: NotRequired[Sequence[str]]
    description: NotRequired[str]
    isMtlsEnabledVmCluster: NotRequired[bool]
    licenseModel: NotRequired[LicenseModelType]
    maintenanceWindow: NotRequired[MaintenanceWindowUnionTypeDef]
    scanListenerPortNonTls: NotRequired[int]
    scanListenerPortTls: NotRequired[int]
    tags: NotRequired[Mapping[str, str]]
    timeZone: NotRequired[str]

class CreateCloudExadataInfrastructureInputTypeDef(TypedDict):
    displayName: str
    shape: str
    computeCount: int
    storageCount: int
    availabilityZone: NotRequired[str]
    availabilityZoneId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    customerContactsToSendToOCI: NotRequired[Sequence[CustomerContactTypeDef]]
    maintenanceWindow: NotRequired[MaintenanceWindowUnionTypeDef]
    clientToken: NotRequired[str]
    databaseServerType: NotRequired[str]
    storageServerType: NotRequired[str]

class UpdateCloudExadataInfrastructureInputTypeDef(TypedDict):
    cloudExadataInfrastructureId: str
    maintenanceWindow: NotRequired[MaintenanceWindowUnionTypeDef]

class ListOdbNetworksOutputTypeDef(TypedDict):
    odbNetworks: list[OdbNetworkSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetOdbNetworkOutputTypeDef(TypedDict):
    odbNetwork: OdbNetworkTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAutonomousDatabaseClonesOutputTypeDef(TypedDict):
    autonomousDatabaseClones: list[AutonomousDatabaseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAutonomousDatabasesOutputTypeDef(TypedDict):
    autonomousDatabases: list[AutonomousDatabaseSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetAutonomousDatabaseOutputTypeDef(TypedDict):
    autonomousDatabase: AutonomousDatabaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
