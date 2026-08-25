"""
Type annotations for timestream-influxdb service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_timestream_influxdb/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_timestream_influxdb.type_defs import ClusterConfigurationTypeDef

    data: ClusterConfigurationTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AutomatedDbBackupTypeType,
    ClusterStatusType,
    DataFusionRuntimeTypeType,
    DbBackupStatusType,
    DbBackupTypeType,
    DbInstanceTypeType,
    DbStorageTypeType,
    DeploymentTypeType,
    DurationTypeType,
    EngineTypeType,
    FailoverModeType,
    InstanceModeType,
    LogLevelType,
    NetworkTypeType,
    ResourceDeploymentTypeType,
    ResourceTypeType,
    RestoreModeType,
    StatusType,
    TracingTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "ClusterConfigurationTypeDef",
    "CreateDbBackupInputTypeDef",
    "CreateDbBackupOutputTypeDef",
    "CreateDbClusterInputTypeDef",
    "CreateDbClusterOutputTypeDef",
    "CreateDbInstanceInputTypeDef",
    "CreateDbInstanceOutputTypeDef",
    "CreateDbParameterGroupInputTypeDef",
    "CreateDbParameterGroupOutputTypeDef",
    "DbBackupConfigurationOutputTypeDef",
    "DbBackupConfigurationTypeDef",
    "DbBackupSummaryTypeDef",
    "DbClusterSummaryTypeDef",
    "DbInstanceForClusterSummaryTypeDef",
    "DbInstanceSummaryTypeDef",
    "DbParameterGroupSummaryTypeDef",
    "DeleteDbBackupInputTypeDef",
    "DeleteDbBackupOutputTypeDef",
    "DeleteDbClusterInputTypeDef",
    "DeleteDbClusterOutputTypeDef",
    "DeleteDbInstanceInputTypeDef",
    "DeleteDbInstanceOutputTypeDef",
    "DurationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetDbBackupInputTypeDef",
    "GetDbBackupOutputTypeDef",
    "GetDbClusterInputTypeDef",
    "GetDbClusterOutputTypeDef",
    "GetDbInstanceInputTypeDef",
    "GetDbInstanceOutputTypeDef",
    "GetDbParameterGroupInputTypeDef",
    "GetDbParameterGroupOutputTypeDef",
    "InfluxDBv2ParametersTypeDef",
    "InfluxDBv3CoreParametersTypeDef",
    "InfluxDBv3EnterpriseParametersTypeDef",
    "ListDbBackupsInputPaginateTypeDef",
    "ListDbBackupsInputTypeDef",
    "ListDbBackupsOutputTypeDef",
    "ListDbClustersInputPaginateTypeDef",
    "ListDbClustersInputTypeDef",
    "ListDbClustersOutputTypeDef",
    "ListDbInstancesForClusterInputPaginateTypeDef",
    "ListDbInstancesForClusterInputTypeDef",
    "ListDbInstancesForClusterOutputTypeDef",
    "ListDbInstancesInputPaginateTypeDef",
    "ListDbInstancesInputTypeDef",
    "ListDbInstancesOutputTypeDef",
    "ListDbParameterGroupsInputPaginateTypeDef",
    "ListDbParameterGroupsInputTypeDef",
    "ListDbParameterGroupsOutputTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LogDeliveryConfigurationTypeDef",
    "MaintenanceScheduleTypeDef",
    "PaginatorConfigTypeDef",
    "ParametersTypeDef",
    "PercentOrAbsoluteLongTypeDef",
    "RebootDbClusterInputTypeDef",
    "RebootDbClusterOutputTypeDef",
    "RebootDbInstanceInputTypeDef",
    "RebootDbInstanceOutputTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreFromDbBackupInputTypeDef",
    "RestoreFromDbBackupOutputTypeDef",
    "S3ConfigurationTypeDef",
    "TagResourceRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateDbClusterInputTypeDef",
    "UpdateDbClusterOutputTypeDef",
    "UpdateDbInstanceInputTypeDef",
    "UpdateDbInstanceOutputTypeDef",
)

class ClusterConfigurationTypeDef(TypedDict):
    ingestQueryInstances: NotRequired[int]
    queryOnlyInstances: NotRequired[int]
    dedicatedCompactor: NotRequired[bool]

class CreateDbBackupInputTypeDef(TypedDict):
    name: str
    dbResourceId: str
    retentionDays: NotRequired[int]
    tags: NotRequired[Mapping[str, str]]

class MaintenanceScheduleTypeDef(TypedDict):
    timezone: str
    preferredMaintenanceWindow: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

DbBackupConfigurationTypeDef = TypedDict(
    "DbBackupConfigurationTypeDef",
    {
        "type": AutomatedDbBackupTypeType,
        "retentionDays": int,
        "enabled": bool,
        "customSchedule": NotRequired[str],
    },
)
DbBackupConfigurationOutputTypeDef = TypedDict(
    "DbBackupConfigurationOutputTypeDef",
    {
        "type": AutomatedDbBackupTypeType,
        "retentionDays": int,
        "enabled": bool,
        "customSchedule": NotRequired[str],
        "nextAutomatedBackupTime": NotRequired[datetime],
    },
)
DbBackupSummaryTypeDef = TypedDict(
    "DbBackupSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": NotRequired[str],
        "status": NotRequired[DbBackupStatusType],
        "createdAt": NotRequired[datetime],
        "expiresAfter": NotRequired[str],
        "dbResourceId": NotRequired[str],
        "type": NotRequired[DbBackupTypeType],
        "engineType": NotRequired[EngineTypeType],
        "deploymentType": NotRequired[ResourceDeploymentTypeType],
        "kmsKeyId": NotRequired[str],
    },
)
DbClusterSummaryTypeDef = TypedDict(
    "DbClusterSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": NotRequired[ClusterStatusType],
        "endpoint": NotRequired[str],
        "readerEndpoint": NotRequired[str],
        "port": NotRequired[int],
        "deploymentType": NotRequired[Literal["MULTI_NODE_READ_REPLICAS"]],
        "dbInstanceType": NotRequired[DbInstanceTypeType],
        "networkType": NotRequired[NetworkTypeType],
        "dbStorageType": NotRequired[DbStorageTypeType],
        "allocatedStorage": NotRequired[int],
        "engineType": NotRequired[EngineTypeType],
    },
)
DbInstanceForClusterSummaryTypeDef = TypedDict(
    "DbInstanceForClusterSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": NotRequired[StatusType],
        "endpoint": NotRequired[str],
        "port": NotRequired[int],
        "networkType": NotRequired[NetworkTypeType],
        "dbInstanceType": NotRequired[DbInstanceTypeType],
        "dbStorageType": NotRequired[DbStorageTypeType],
        "allocatedStorage": NotRequired[int],
        "deploymentType": NotRequired[DeploymentTypeType],
        "instanceMode": NotRequired[InstanceModeType],
        "instanceModes": NotRequired[list[InstanceModeType]],
    },
)
DbInstanceSummaryTypeDef = TypedDict(
    "DbInstanceSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": NotRequired[StatusType],
        "endpoint": NotRequired[str],
        "port": NotRequired[int],
        "networkType": NotRequired[NetworkTypeType],
        "dbInstanceType": NotRequired[DbInstanceTypeType],
        "dbStorageType": NotRequired[DbStorageTypeType],
        "allocatedStorage": NotRequired[int],
        "deploymentType": NotRequired[DeploymentTypeType],
    },
)
DbParameterGroupSummaryTypeDef = TypedDict(
    "DbParameterGroupSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "description": NotRequired[str],
    },
)

class DeleteDbBackupInputTypeDef(TypedDict):
    identifier: str

class DeleteDbClusterInputTypeDef(TypedDict):
    dbClusterId: str
    retainAutomatedBackups: NotRequired[bool]

class DeleteDbInstanceInputTypeDef(TypedDict):
    identifier: str
    retainAutomatedBackups: NotRequired[bool]

class DurationTypeDef(TypedDict):
    durationType: DurationTypeType
    value: int

class GetDbBackupInputTypeDef(TypedDict):
    identifier: str

class GetDbClusterInputTypeDef(TypedDict):
    dbClusterId: str

class GetDbInstanceInputTypeDef(TypedDict):
    identifier: str

class GetDbParameterGroupInputTypeDef(TypedDict):
    identifier: str

class PercentOrAbsoluteLongTypeDef(TypedDict):
    percent: NotRequired[str]
    absolute: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListDbBackupsInputTypeDef(TypedDict):
    dbResourceId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDbClustersInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDbInstancesForClusterInputTypeDef(TypedDict):
    dbClusterId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDbInstancesInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDbParameterGroupsInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class S3ConfigurationTypeDef(TypedDict):
    bucketName: str
    enabled: bool

class RebootDbClusterInputTypeDef(TypedDict):
    dbClusterId: str
    instanceIds: NotRequired[Sequence[str]]

class RebootDbInstanceInputTypeDef(TypedDict):
    identifier: str

TimestampTypeDef = Union[datetime, str]

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class CreateDbClusterOutputTypeDef(TypedDict):
    dbClusterId: str
    dbClusterStatus: ClusterStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDbClusterOutputTypeDef(TypedDict):
    dbClusterStatus: ClusterStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class RebootDbClusterOutputTypeDef(TypedDict):
    dbClusterStatus: ClusterStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class RestoreFromDbBackupOutputTypeDef(TypedDict):
    restoredDbResourceId: str
    restoreStatus: Literal["RESTORING"]
    resourceType: ResourceTypeType
    engineType: EngineTypeType
    deploymentType: ResourceDeploymentTypeType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDbClusterOutputTypeDef(TypedDict):
    dbClusterStatus: ClusterStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListDbBackupsOutputTypeDef(TypedDict):
    items: list[DbBackupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDbClustersOutputTypeDef(TypedDict):
    items: list[DbClusterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDbInstancesForClusterOutputTypeDef(TypedDict):
    items: list[DbInstanceForClusterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDbInstancesOutputTypeDef(TypedDict):
    items: list[DbInstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDbParameterGroupsOutputTypeDef(TypedDict):
    items: list[DbParameterGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class InfluxDBv2ParametersTypeDef(TypedDict):
    fluxLogEnabled: NotRequired[bool]
    logLevel: NotRequired[LogLevelType]
    noTasks: NotRequired[bool]
    queryConcurrency: NotRequired[int]
    queryQueueSize: NotRequired[int]
    tracingType: NotRequired[TracingTypeType]
    metricsDisabled: NotRequired[bool]
    httpIdleTimeout: NotRequired[DurationTypeDef]
    httpReadHeaderTimeout: NotRequired[DurationTypeDef]
    httpReadTimeout: NotRequired[DurationTypeDef]
    httpWriteTimeout: NotRequired[DurationTypeDef]
    influxqlMaxSelectBuckets: NotRequired[int]
    influxqlMaxSelectPoint: NotRequired[int]
    influxqlMaxSelectSeries: NotRequired[int]
    pprofDisabled: NotRequired[bool]
    queryInitialMemoryBytes: NotRequired[int]
    queryMaxMemoryBytes: NotRequired[int]
    queryMemoryBytes: NotRequired[int]
    sessionLength: NotRequired[int]
    sessionRenewDisabled: NotRequired[bool]
    storageCacheMaxMemorySize: NotRequired[int]
    storageCacheSnapshotMemorySize: NotRequired[int]
    storageCacheSnapshotWriteColdDuration: NotRequired[DurationTypeDef]
    storageCompactFullWriteColdDuration: NotRequired[DurationTypeDef]
    storageCompactThroughputBurst: NotRequired[int]
    storageMaxConcurrentCompactions: NotRequired[int]
    storageMaxIndexLogFileSize: NotRequired[int]
    storageNoValidateFieldSize: NotRequired[bool]
    storageRetentionCheckInterval: NotRequired[DurationTypeDef]
    storageSeriesFileMaxConcurrentSnapshotCompactions: NotRequired[int]
    storageSeriesIdSetCacheSize: NotRequired[int]
    storageWalMaxConcurrentWrites: NotRequired[int]
    storageWalMaxWriteDelay: NotRequired[DurationTypeDef]
    uiDisabled: NotRequired[bool]

class InfluxDBv3CoreParametersTypeDef(TypedDict):
    queryFileLimit: NotRequired[int]
    queryLogSize: NotRequired[int]
    logFilter: NotRequired[str]
    logFormat: NotRequired[Literal["full"]]
    dataFusionNumThreads: NotRequired[int]
    dataFusionRuntimeType: NotRequired[DataFusionRuntimeTypeType]
    dataFusionRuntimeDisableLifoSlot: NotRequired[bool]
    dataFusionRuntimeEventInterval: NotRequired[int]
    dataFusionRuntimeGlobalQueueInterval: NotRequired[int]
    dataFusionRuntimeMaxBlockingThreads: NotRequired[int]
    dataFusionRuntimeMaxIoEventsPerTick: NotRequired[int]
    dataFusionRuntimeThreadKeepAlive: NotRequired[DurationTypeDef]
    dataFusionRuntimeThreadPriority: NotRequired[int]
    dataFusionMaxParquetFanout: NotRequired[int]
    dataFusionUseCachedParquetLoader: NotRequired[bool]
    dataFusionConfig: NotRequired[str]
    maxHttpRequestSize: NotRequired[int]
    forceSnapshotMemThreshold: NotRequired[PercentOrAbsoluteLongTypeDef]
    walSnapshotSize: NotRequired[int]
    walMaxWriteBufferSize: NotRequired[int]
    snapshottedWalFilesToKeep: NotRequired[int]
    preemptiveCacheAge: NotRequired[DurationTypeDef]
    parquetMemCachePrunePercentage: NotRequired[float]
    parquetMemCachePruneInterval: NotRequired[DurationTypeDef]
    disableParquetMemCache: NotRequired[bool]
    parquetMemCacheQueryPathDuration: NotRequired[DurationTypeDef]
    lastCacheEvictionInterval: NotRequired[DurationTypeDef]
    distinctCacheEvictionInterval: NotRequired[DurationTypeDef]
    gen1Duration: NotRequired[DurationTypeDef]
    execMemPoolBytes: NotRequired[PercentOrAbsoluteLongTypeDef]
    parquetMemCacheSize: NotRequired[PercentOrAbsoluteLongTypeDef]
    walReplayFailOnError: NotRequired[bool]
    walReplayConcurrencyLimit: NotRequired[int]
    tableIndexCacheMaxEntries: NotRequired[int]
    tableIndexCacheConcurrencyLimit: NotRequired[int]
    gen1LookbackDuration: NotRequired[DurationTypeDef]
    retentionCheckInterval: NotRequired[DurationTypeDef]
    deleteGracePeriod: NotRequired[DurationTypeDef]
    hardDeleteDefaultDuration: NotRequired[DurationTypeDef]
    pluginRepositoryUrl: NotRequired[str]
    pluginRepositorySecretArn: NotRequired[str]

class InfluxDBv3EnterpriseParametersTypeDef(TypedDict):
    ingestQueryInstances: int
    queryOnlyInstances: int
    dedicatedCompactor: bool
    queryFileLimit: NotRequired[int]
    queryLogSize: NotRequired[int]
    logFilter: NotRequired[str]
    logFormat: NotRequired[Literal["full"]]
    dataFusionNumThreads: NotRequired[int]
    dataFusionRuntimeType: NotRequired[DataFusionRuntimeTypeType]
    dataFusionRuntimeDisableLifoSlot: NotRequired[bool]
    dataFusionRuntimeEventInterval: NotRequired[int]
    dataFusionRuntimeGlobalQueueInterval: NotRequired[int]
    dataFusionRuntimeMaxBlockingThreads: NotRequired[int]
    dataFusionRuntimeMaxIoEventsPerTick: NotRequired[int]
    dataFusionRuntimeThreadKeepAlive: NotRequired[DurationTypeDef]
    dataFusionRuntimeThreadPriority: NotRequired[int]
    dataFusionMaxParquetFanout: NotRequired[int]
    dataFusionUseCachedParquetLoader: NotRequired[bool]
    dataFusionConfig: NotRequired[str]
    maxHttpRequestSize: NotRequired[int]
    forceSnapshotMemThreshold: NotRequired[PercentOrAbsoluteLongTypeDef]
    walSnapshotSize: NotRequired[int]
    walMaxWriteBufferSize: NotRequired[int]
    snapshottedWalFilesToKeep: NotRequired[int]
    preemptiveCacheAge: NotRequired[DurationTypeDef]
    parquetMemCachePrunePercentage: NotRequired[float]
    parquetMemCachePruneInterval: NotRequired[DurationTypeDef]
    disableParquetMemCache: NotRequired[bool]
    parquetMemCacheQueryPathDuration: NotRequired[DurationTypeDef]
    lastCacheEvictionInterval: NotRequired[DurationTypeDef]
    distinctCacheEvictionInterval: NotRequired[DurationTypeDef]
    gen1Duration: NotRequired[DurationTypeDef]
    execMemPoolBytes: NotRequired[PercentOrAbsoluteLongTypeDef]
    parquetMemCacheSize: NotRequired[PercentOrAbsoluteLongTypeDef]
    walReplayFailOnError: NotRequired[bool]
    walReplayConcurrencyLimit: NotRequired[int]
    tableIndexCacheMaxEntries: NotRequired[int]
    tableIndexCacheConcurrencyLimit: NotRequired[int]
    gen1LookbackDuration: NotRequired[DurationTypeDef]
    retentionCheckInterval: NotRequired[DurationTypeDef]
    deleteGracePeriod: NotRequired[DurationTypeDef]
    hardDeleteDefaultDuration: NotRequired[DurationTypeDef]
    pluginRepositoryUrl: NotRequired[str]
    pluginRepositorySecretArn: NotRequired[str]
    compactionRowLimit: NotRequired[int]
    compactionMaxNumFilesPerPlan: NotRequired[int]
    compactionGen2Duration: NotRequired[DurationTypeDef]
    compactionMultipliers: NotRequired[str]
    compactionCleanupWait: NotRequired[DurationTypeDef]
    compactionCheckInterval: NotRequired[DurationTypeDef]
    lastValueCacheDisableFromHistory: NotRequired[bool]
    distinctValueCacheDisableFromHistory: NotRequired[bool]
    replicationInterval: NotRequired[DurationTypeDef]
    catalogSyncInterval: NotRequired[DurationTypeDef]

class ListDbBackupsInputPaginateTypeDef(TypedDict):
    dbResourceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDbClustersInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDbInstancesForClusterInputPaginateTypeDef(TypedDict):
    dbClusterId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDbInstancesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDbParameterGroupsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class LogDeliveryConfigurationTypeDef(TypedDict):
    s3Configuration: S3ConfigurationTypeDef

class ParametersTypeDef(TypedDict):
    InfluxDBv2: NotRequired[InfluxDBv2ParametersTypeDef]
    InfluxDBv3Core: NotRequired[InfluxDBv3CoreParametersTypeDef]
    InfluxDBv3Enterprise: NotRequired[InfluxDBv3EnterpriseParametersTypeDef]

CreateDbBackupOutputTypeDef = TypedDict(
    "CreateDbBackupOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": DbBackupStatusType,
        "createdAt": datetime,
        "expiresAfter": str,
        "dbResourceId": str,
        "type": DbBackupTypeType,
        "engineType": EngineTypeType,
        "deploymentType": ResourceDeploymentTypeType,
        "kmsKeyId": str,
        "clusterConfiguration": ClusterConfigurationTypeDef,
        "dbParameterGroupId": str,
        "dbInstanceType": DbInstanceTypeType,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "failoverMode": FailoverModeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "vpcSubnetIds": list[str],
        "vpcSecurityGroupIds": list[str],
        "publiclyAccessible": bool,
        "port": int,
        "networkType": NetworkTypeType,
        "influxAuthParametersSecretArn": str,
        "maintenanceSchedule": MaintenanceScheduleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateDbClusterInputTypeDef(TypedDict):
    name: str
    dbInstanceType: DbInstanceTypeType
    vpcSubnetIds: Sequence[str]
    vpcSecurityGroupIds: Sequence[str]
    username: NotRequired[str]
    password: NotRequired[str]
    organization: NotRequired[str]
    bucket: NotRequired[str]
    port: NotRequired[int]
    dbParameterGroupIdentifier: NotRequired[str]
    dbStorageType: NotRequired[DbStorageTypeType]
    allocatedStorage: NotRequired[int]
    networkType: NotRequired[NetworkTypeType]
    publiclyAccessible: NotRequired[bool]
    deploymentType: NotRequired[Literal["MULTI_NODE_READ_REPLICAS"]]
    failoverMode: NotRequired[FailoverModeType]
    logDeliveryConfiguration: NotRequired[LogDeliveryConfigurationTypeDef]
    maintenanceSchedule: NotRequired[MaintenanceScheduleTypeDef]
    dbBackupConfigurations: NotRequired[Sequence[DbBackupConfigurationTypeDef]]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateDbInstanceInputTypeDef(TypedDict):
    name: str
    password: str
    dbInstanceType: DbInstanceTypeType
    vpcSubnetIds: Sequence[str]
    vpcSecurityGroupIds: Sequence[str]
    allocatedStorage: int
    username: NotRequired[str]
    organization: NotRequired[str]
    bucket: NotRequired[str]
    publiclyAccessible: NotRequired[bool]
    dbStorageType: NotRequired[DbStorageTypeType]
    dbParameterGroupIdentifier: NotRequired[str]
    deploymentType: NotRequired[DeploymentTypeType]
    logDeliveryConfiguration: NotRequired[LogDeliveryConfigurationTypeDef]
    maintenanceSchedule: NotRequired[MaintenanceScheduleTypeDef]
    tags: NotRequired[Mapping[str, str]]
    port: NotRequired[int]
    networkType: NotRequired[NetworkTypeType]
    dbBackupConfigurations: NotRequired[Sequence[DbBackupConfigurationTypeDef]]
    kmsKeyId: NotRequired[str]

CreateDbInstanceOutputTypeDef = TypedDict(
    "CreateDbInstanceOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": StatusType,
        "endpoint": str,
        "port": int,
        "networkType": NetworkTypeType,
        "dbInstanceType": DbInstanceTypeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "deploymentType": DeploymentTypeType,
        "vpcSubnetIds": list[str],
        "publiclyAccessible": bool,
        "vpcSecurityGroupIds": list[str],
        "dbParameterGroupIdentifier": str,
        "availabilityZone": str,
        "secondaryAvailabilityZone": str,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "influxAuthParametersSecretArn": str,
        "dbClusterId": str,
        "instanceMode": InstanceModeType,
        "instanceModes": list[InstanceModeType],
        "maintenanceSchedule": MaintenanceScheduleTypeDef,
        "lastMaintenanceTime": datetime,
        "nextMaintenanceTime": datetime,
        "dbBackupConfigurations": list[DbBackupConfigurationOutputTypeDef],
        "kmsKeyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteDbBackupOutputTypeDef = TypedDict(
    "DeleteDbBackupOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": DbBackupStatusType,
        "createdAt": datetime,
        "expiresAfter": str,
        "dbResourceId": str,
        "type": DbBackupTypeType,
        "engineType": EngineTypeType,
        "deploymentType": ResourceDeploymentTypeType,
        "kmsKeyId": str,
        "clusterConfiguration": ClusterConfigurationTypeDef,
        "dbParameterGroupId": str,
        "dbInstanceType": DbInstanceTypeType,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "failoverMode": FailoverModeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "vpcSubnetIds": list[str],
        "vpcSecurityGroupIds": list[str],
        "publiclyAccessible": bool,
        "port": int,
        "networkType": NetworkTypeType,
        "influxAuthParametersSecretArn": str,
        "maintenanceSchedule": MaintenanceScheduleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteDbInstanceOutputTypeDef = TypedDict(
    "DeleteDbInstanceOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": StatusType,
        "endpoint": str,
        "port": int,
        "networkType": NetworkTypeType,
        "dbInstanceType": DbInstanceTypeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "deploymentType": DeploymentTypeType,
        "vpcSubnetIds": list[str],
        "publiclyAccessible": bool,
        "vpcSecurityGroupIds": list[str],
        "dbParameterGroupIdentifier": str,
        "availabilityZone": str,
        "secondaryAvailabilityZone": str,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "influxAuthParametersSecretArn": str,
        "dbClusterId": str,
        "instanceMode": InstanceModeType,
        "instanceModes": list[InstanceModeType],
        "maintenanceSchedule": MaintenanceScheduleTypeDef,
        "lastMaintenanceTime": datetime,
        "nextMaintenanceTime": datetime,
        "dbBackupConfigurations": list[DbBackupConfigurationOutputTypeDef],
        "kmsKeyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDbBackupOutputTypeDef = TypedDict(
    "GetDbBackupOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": DbBackupStatusType,
        "createdAt": datetime,
        "expiresAfter": str,
        "dbResourceId": str,
        "type": DbBackupTypeType,
        "engineType": EngineTypeType,
        "deploymentType": ResourceDeploymentTypeType,
        "kmsKeyId": str,
        "clusterConfiguration": ClusterConfigurationTypeDef,
        "dbParameterGroupId": str,
        "dbInstanceType": DbInstanceTypeType,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "failoverMode": FailoverModeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "vpcSubnetIds": list[str],
        "vpcSecurityGroupIds": list[str],
        "publiclyAccessible": bool,
        "port": int,
        "networkType": NetworkTypeType,
        "influxAuthParametersSecretArn": str,
        "maintenanceSchedule": MaintenanceScheduleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDbClusterOutputTypeDef = TypedDict(
    "GetDbClusterOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": ClusterStatusType,
        "endpoint": str,
        "readerEndpoint": str,
        "port": int,
        "deploymentType": Literal["MULTI_NODE_READ_REPLICAS"],
        "dbInstanceType": DbInstanceTypeType,
        "networkType": NetworkTypeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "engineType": EngineTypeType,
        "publiclyAccessible": bool,
        "dbParameterGroupIdentifier": str,
        "effectiveDbParameterGroupIdentifier": str,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "maintenanceSchedule": MaintenanceScheduleTypeDef,
        "lastMaintenanceTime": datetime,
        "nextMaintenanceTime": datetime,
        "influxAuthParametersSecretArn": str,
        "vpcSubnetIds": list[str],
        "vpcSecurityGroupIds": list[str],
        "failoverMode": FailoverModeType,
        "clusterConfiguration": ClusterConfigurationTypeDef,
        "dbBackupConfigurations": list[DbBackupConfigurationOutputTypeDef],
        "kmsKeyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDbInstanceOutputTypeDef = TypedDict(
    "GetDbInstanceOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": StatusType,
        "endpoint": str,
        "port": int,
        "networkType": NetworkTypeType,
        "dbInstanceType": DbInstanceTypeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "deploymentType": DeploymentTypeType,
        "vpcSubnetIds": list[str],
        "publiclyAccessible": bool,
        "vpcSecurityGroupIds": list[str],
        "dbParameterGroupIdentifier": str,
        "availabilityZone": str,
        "secondaryAvailabilityZone": str,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "influxAuthParametersSecretArn": str,
        "dbClusterId": str,
        "instanceMode": InstanceModeType,
        "instanceModes": list[InstanceModeType],
        "maintenanceSchedule": MaintenanceScheduleTypeDef,
        "lastMaintenanceTime": datetime,
        "nextMaintenanceTime": datetime,
        "dbBackupConfigurations": list[DbBackupConfigurationOutputTypeDef],
        "kmsKeyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RebootDbInstanceOutputTypeDef = TypedDict(
    "RebootDbInstanceOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": StatusType,
        "endpoint": str,
        "port": int,
        "networkType": NetworkTypeType,
        "dbInstanceType": DbInstanceTypeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "deploymentType": DeploymentTypeType,
        "vpcSubnetIds": list[str],
        "publiclyAccessible": bool,
        "vpcSecurityGroupIds": list[str],
        "dbParameterGroupIdentifier": str,
        "availabilityZone": str,
        "secondaryAvailabilityZone": str,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "influxAuthParametersSecretArn": str,
        "dbClusterId": str,
        "instanceMode": InstanceModeType,
        "instanceModes": list[InstanceModeType],
        "maintenanceSchedule": MaintenanceScheduleTypeDef,
        "lastMaintenanceTime": datetime,
        "nextMaintenanceTime": datetime,
        "dbBackupConfigurations": list[DbBackupConfigurationOutputTypeDef],
        "kmsKeyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class RestoreFromDbBackupInputTypeDef(TypedDict):
    name: str
    dbBackupId: str
    restoreToTime: NotRequired[TimestampTypeDef]
    restoreMode: NotRequired[RestoreModeType]
    vpcSubnetIds: NotRequired[Sequence[str]]
    vpcSecurityGroupIds: NotRequired[Sequence[str]]
    publiclyAccessible: NotRequired[bool]
    logDeliveryConfiguration: NotRequired[LogDeliveryConfigurationTypeDef]
    maintenanceSchedule: NotRequired[MaintenanceScheduleTypeDef]
    tags: NotRequired[Mapping[str, str]]
    port: NotRequired[int]
    networkType: NotRequired[NetworkTypeType]
    deploymentType: NotRequired[ResourceDeploymentTypeType]
    dbBackupConfigurations: NotRequired[Sequence[DbBackupConfigurationTypeDef]]
    kmsKeyId: NotRequired[str]

class UpdateDbClusterInputTypeDef(TypedDict):
    dbClusterId: str
    logDeliveryConfiguration: NotRequired[LogDeliveryConfigurationTypeDef]
    dbParameterGroupIdentifier: NotRequired[str]
    port: NotRequired[int]
    dbInstanceType: NotRequired[DbInstanceTypeType]
    failoverMode: NotRequired[FailoverModeType]
    maintenanceSchedule: NotRequired[MaintenanceScheduleTypeDef]
    dbBackupConfigurations: NotRequired[Sequence[DbBackupConfigurationTypeDef]]

class UpdateDbInstanceInputTypeDef(TypedDict):
    identifier: str
    logDeliveryConfiguration: NotRequired[LogDeliveryConfigurationTypeDef]
    dbParameterGroupIdentifier: NotRequired[str]
    port: NotRequired[int]
    dbInstanceType: NotRequired[DbInstanceTypeType]
    deploymentType: NotRequired[DeploymentTypeType]
    dbStorageType: NotRequired[DbStorageTypeType]
    allocatedStorage: NotRequired[int]
    maintenanceSchedule: NotRequired[MaintenanceScheduleTypeDef]
    dbBackupConfigurations: NotRequired[Sequence[DbBackupConfigurationTypeDef]]

UpdateDbInstanceOutputTypeDef = TypedDict(
    "UpdateDbInstanceOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "status": StatusType,
        "endpoint": str,
        "port": int,
        "networkType": NetworkTypeType,
        "dbInstanceType": DbInstanceTypeType,
        "dbStorageType": DbStorageTypeType,
        "allocatedStorage": int,
        "deploymentType": DeploymentTypeType,
        "vpcSubnetIds": list[str],
        "publiclyAccessible": bool,
        "vpcSecurityGroupIds": list[str],
        "dbParameterGroupIdentifier": str,
        "availabilityZone": str,
        "secondaryAvailabilityZone": str,
        "logDeliveryConfiguration": LogDeliveryConfigurationTypeDef,
        "influxAuthParametersSecretArn": str,
        "dbClusterId": str,
        "instanceMode": InstanceModeType,
        "instanceModes": list[InstanceModeType],
        "maintenanceSchedule": MaintenanceScheduleTypeDef,
        "lastMaintenanceTime": datetime,
        "nextMaintenanceTime": datetime,
        "dbBackupConfigurations": list[DbBackupConfigurationOutputTypeDef],
        "kmsKeyId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateDbParameterGroupInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    parameters: NotRequired[ParametersTypeDef]
    tags: NotRequired[Mapping[str, str]]

CreateDbParameterGroupOutputTypeDef = TypedDict(
    "CreateDbParameterGroupOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "description": str,
        "parameters": ParametersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDbParameterGroupOutputTypeDef = TypedDict(
    "GetDbParameterGroupOutputTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "description": str,
        "parameters": ParametersTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
