"""
Type annotations for pcs service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pcs/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_pcs.type_defs import AccountingRequestTypeDef

    data: AccountingRequestTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AccountingModeType,
    ClusterStatusType,
    ComputeNodeGroupStatusType,
    EndpointTypeType,
    ExecutionPolicyType,
    NetworkTypeType,
    OnErrorType,
    PurchaseOptionType,
    QueueStatusType,
    ScriptCachingPolicyType,
    SizeType,
    SlurmRestModeType,
    SpotAllocationStrategyType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccountingRequestTypeDef",
    "AccountingTypeDef",
    "CgroupCustomSettingTypeDef",
    "ClusterSlurmConfigurationRequestTypeDef",
    "ClusterSlurmConfigurationTypeDef",
    "ClusterSummaryTypeDef",
    "ClusterTypeDef",
    "ComputeNodeGroupConfigurationTypeDef",
    "ComputeNodeGroupSlurmConfigurationRequestTypeDef",
    "ComputeNodeGroupSlurmConfigurationTypeDef",
    "ComputeNodeGroupSummaryTypeDef",
    "ComputeNodeGroupTypeDef",
    "CreateClusterRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateComputeNodeGroupRequestTypeDef",
    "CreateComputeNodeGroupResponseTypeDef",
    "CreateQueueRequestTypeDef",
    "CreateQueueResponseTypeDef",
    "CustomLaunchTemplateTypeDef",
    "DeleteClusterRequestTypeDef",
    "DeleteComputeNodeGroupRequestTypeDef",
    "DeleteQueueRequestTypeDef",
    "EndpointTypeDef",
    "ErrorInfoTypeDef",
    "GetClusterRequestTypeDef",
    "GetClusterResponseTypeDef",
    "GetComputeNodeGroupRequestTypeDef",
    "GetComputeNodeGroupResponseTypeDef",
    "GetQueueRequestTypeDef",
    "GetQueueResponseTypeDef",
    "InstanceConfigTypeDef",
    "JwtAuthTypeDef",
    "JwtKeyTypeDef",
    "ListClustersRequestPaginateTypeDef",
    "ListClustersRequestTypeDef",
    "ListClustersResponseTypeDef",
    "ListComputeNodeGroupsRequestPaginateTypeDef",
    "ListComputeNodeGroupsRequestTypeDef",
    "ListComputeNodeGroupsResponseTypeDef",
    "ListQueuesRequestPaginateTypeDef",
    "ListQueuesRequestTypeDef",
    "ListQueuesResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NetworkingRequestTypeDef",
    "NetworkingTypeDef",
    "NodeLifecycleActionsRequestTypeDef",
    "NodeLifecycleActionsTypeDef",
    "NodeLifecycleScriptOutputTypeDef",
    "NodeLifecycleScriptTypeDef",
    "NodeLifecycleScriptUnionTypeDef",
    "NodeLifecycleStagesOutputTypeDef",
    "NodeLifecycleStagesTypeDef",
    "NodeLifecycleStagesUnionTypeDef",
    "PaginatorConfigTypeDef",
    "QueueSlurmConfigurationRequestTypeDef",
    "QueueSlurmConfigurationTypeDef",
    "QueueSummaryTypeDef",
    "QueueTypeDef",
    "RegisterComputeNodeGroupInstanceRequestTypeDef",
    "RegisterComputeNodeGroupInstanceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "ScalingConfigurationRequestTypeDef",
    "ScalingConfigurationTypeDef",
    "SchedulerRequestTypeDef",
    "SchedulerTypeDef",
    "ScriptSourceTypeDef",
    "SlurmAuthKeyTypeDef",
    "SlurmCustomSettingTypeDef",
    "SlurmRestRequestTypeDef",
    "SlurmRestTypeDef",
    "SlurmdbdCustomSettingTypeDef",
    "SpotOptionsTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAccountingRequestTypeDef",
    "UpdateClusterRequestTypeDef",
    "UpdateClusterResponseTypeDef",
    "UpdateClusterSlurmConfigurationRequestTypeDef",
    "UpdateComputeNodeGroupRequestTypeDef",
    "UpdateComputeNodeGroupResponseTypeDef",
    "UpdateComputeNodeGroupSlurmConfigurationRequestTypeDef",
    "UpdateNodeLifecycleActionsRequestTypeDef",
    "UpdateQueueRequestTypeDef",
    "UpdateQueueResponseTypeDef",
    "UpdateQueueSlurmConfigurationRequestTypeDef",
    "UpdateSchedulerRequestTypeDef",
    "UpdateSlurmRestRequestTypeDef",
)

class AccountingRequestTypeDef(TypedDict):
    mode: AccountingModeType
    defaultPurgeTimeInDays: NotRequired[int]

class AccountingTypeDef(TypedDict):
    mode: AccountingModeType
    defaultPurgeTimeInDays: NotRequired[int]

class CgroupCustomSettingTypeDef(TypedDict):
    parameterName: str
    parameterValue: str

class SlurmCustomSettingTypeDef(TypedDict):
    parameterName: str
    parameterValue: str

class SlurmRestRequestTypeDef(TypedDict):
    mode: SlurmRestModeType

class SlurmdbdCustomSettingTypeDef(TypedDict):
    parameterName: str
    parameterValue: str

class SlurmAuthKeyTypeDef(TypedDict):
    secretArn: str
    secretVersion: str

class SlurmRestTypeDef(TypedDict):
    mode: SlurmRestModeType

ClusterSummaryTypeDef = TypedDict(
    "ClusterSummaryTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "status": ClusterStatusType,
    },
)
EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "type": EndpointTypeType,
        "privateIpAddress": str,
        "port": str,
        "publicIpAddress": NotRequired[str],
        "ipv6Address": NotRequired[str],
    },
)

class ErrorInfoTypeDef(TypedDict):
    code: NotRequired[str]
    message: NotRequired[str]

class NetworkingTypeDef(TypedDict):
    subnetIds: NotRequired[list[str]]
    securityGroupIds: NotRequired[list[str]]
    networkType: NotRequired[NetworkTypeType]

SchedulerTypeDef = TypedDict(
    "SchedulerTypeDef",
    {
        "type": Literal["SLURM"],
        "version": str,
    },
)

class ComputeNodeGroupConfigurationTypeDef(TypedDict):
    computeNodeGroupId: NotRequired[str]

ComputeNodeGroupSummaryTypeDef = TypedDict(
    "ComputeNodeGroupSummaryTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "clusterId": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "status": ComputeNodeGroupStatusType,
    },
)
CustomLaunchTemplateTypeDef = TypedDict(
    "CustomLaunchTemplateTypeDef",
    {
        "id": str,
        "version": str,
    },
)

class InstanceConfigTypeDef(TypedDict):
    instanceType: NotRequired[str]

class ScalingConfigurationTypeDef(TypedDict):
    minInstanceCount: int
    maxInstanceCount: int

class SpotOptionsTypeDef(TypedDict):
    allocationStrategy: NotRequired[SpotAllocationStrategyType]

class NetworkingRequestTypeDef(TypedDict):
    subnetIds: NotRequired[Sequence[str]]
    securityGroupIds: NotRequired[Sequence[str]]
    networkType: NotRequired[NetworkTypeType]

SchedulerRequestTypeDef = TypedDict(
    "SchedulerRequestTypeDef",
    {
        "type": Literal["SLURM"],
        "version": str,
    },
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ScalingConfigurationRequestTypeDef(TypedDict):
    minInstanceCount: int
    maxInstanceCount: int

class DeleteClusterRequestTypeDef(TypedDict):
    clusterIdentifier: str
    clientToken: NotRequired[str]

class DeleteComputeNodeGroupRequestTypeDef(TypedDict):
    clusterIdentifier: str
    computeNodeGroupIdentifier: str
    clientToken: NotRequired[str]

class DeleteQueueRequestTypeDef(TypedDict):
    clusterIdentifier: str
    queueIdentifier: str
    clientToken: NotRequired[str]

class GetClusterRequestTypeDef(TypedDict):
    clusterIdentifier: str

class GetComputeNodeGroupRequestTypeDef(TypedDict):
    clusterIdentifier: str
    computeNodeGroupIdentifier: str

class GetQueueRequestTypeDef(TypedDict):
    clusterIdentifier: str
    queueIdentifier: str

class JwtKeyTypeDef(TypedDict):
    secretArn: str
    secretVersion: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListClustersRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListComputeNodeGroupsRequestTypeDef(TypedDict):
    clusterIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListQueuesRequestTypeDef(TypedDict):
    clusterIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

QueueSummaryTypeDef = TypedDict(
    "QueueSummaryTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "clusterId": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "status": QueueStatusType,
    },
)

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class ScriptSourceTypeDef(TypedDict):
    scriptLocation: str
    s3VersionId: NotRequired[str]
    checksum: NotRequired[str]

class RegisterComputeNodeGroupInstanceRequestTypeDef(TypedDict):
    clusterIdentifier: str
    bootstrapId: str

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateAccountingRequestTypeDef(TypedDict):
    defaultPurgeTimeInDays: NotRequired[int]
    mode: NotRequired[AccountingModeType]

class UpdateSchedulerRequestTypeDef(TypedDict):
    version: str

class UpdateSlurmRestRequestTypeDef(TypedDict):
    mode: NotRequired[SlurmRestModeType]

class ComputeNodeGroupSlurmConfigurationRequestTypeDef(TypedDict):
    scaleDownIdleTimeInSeconds: NotRequired[int]
    slurmCustomSettings: NotRequired[Sequence[SlurmCustomSettingTypeDef]]

class ComputeNodeGroupSlurmConfigurationTypeDef(TypedDict):
    scaleDownIdleTimeInSeconds: NotRequired[int]
    slurmCustomSettings: NotRequired[list[SlurmCustomSettingTypeDef]]

class QueueSlurmConfigurationRequestTypeDef(TypedDict):
    slurmCustomSettings: NotRequired[Sequence[SlurmCustomSettingTypeDef]]

class QueueSlurmConfigurationTypeDef(TypedDict):
    slurmCustomSettings: NotRequired[list[SlurmCustomSettingTypeDef]]

class UpdateComputeNodeGroupSlurmConfigurationRequestTypeDef(TypedDict):
    scaleDownIdleTimeInSeconds: NotRequired[int]
    slurmCustomSettings: NotRequired[Sequence[SlurmCustomSettingTypeDef]]

class UpdateQueueSlurmConfigurationRequestTypeDef(TypedDict):
    slurmCustomSettings: NotRequired[Sequence[SlurmCustomSettingTypeDef]]

class ClusterSlurmConfigurationRequestTypeDef(TypedDict):
    scaleDownIdleTimeInSeconds: NotRequired[int]
    slurmCustomSettings: NotRequired[Sequence[SlurmCustomSettingTypeDef]]
    slurmdbdCustomSettings: NotRequired[Sequence[SlurmdbdCustomSettingTypeDef]]
    cgroupCustomSettings: NotRequired[Sequence[CgroupCustomSettingTypeDef]]
    accounting: NotRequired[AccountingRequestTypeDef]
    slurmRest: NotRequired[SlurmRestRequestTypeDef]

class ListClustersResponseTypeDef(TypedDict):
    clusters: list[ClusterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListComputeNodeGroupsResponseTypeDef(TypedDict):
    computeNodeGroups: list[ComputeNodeGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class JwtAuthTypeDef(TypedDict):
    jwtKey: NotRequired[JwtKeyTypeDef]

class ListClustersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListComputeNodeGroupsRequestPaginateTypeDef(TypedDict):
    clusterIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQueuesRequestPaginateTypeDef(TypedDict):
    clusterIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListQueuesResponseTypeDef(TypedDict):
    queues: list[QueueSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class NodeLifecycleScriptOutputTypeDef(TypedDict):
    name: str
    scriptSource: ScriptSourceTypeDef
    arguments: NotRequired[list[str]]
    onError: NotRequired[OnErrorType]
    executionPolicy: NotRequired[ExecutionPolicyType]

class NodeLifecycleScriptTypeDef(TypedDict):
    name: str
    scriptSource: ScriptSourceTypeDef
    arguments: NotRequired[Sequence[str]]
    onError: NotRequired[OnErrorType]
    executionPolicy: NotRequired[ExecutionPolicyType]

class UpdateClusterSlurmConfigurationRequestTypeDef(TypedDict):
    scaleDownIdleTimeInSeconds: NotRequired[int]
    slurmCustomSettings: NotRequired[Sequence[SlurmCustomSettingTypeDef]]
    slurmdbdCustomSettings: NotRequired[Sequence[SlurmdbdCustomSettingTypeDef]]
    cgroupCustomSettings: NotRequired[Sequence[CgroupCustomSettingTypeDef]]
    accounting: NotRequired[UpdateAccountingRequestTypeDef]
    slurmRest: NotRequired[UpdateSlurmRestRequestTypeDef]

class CreateQueueRequestTypeDef(TypedDict):
    clusterIdentifier: str
    queueName: str
    computeNodeGroupConfigurations: NotRequired[Sequence[ComputeNodeGroupConfigurationTypeDef]]
    slurmConfiguration: NotRequired[QueueSlurmConfigurationRequestTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

QueueTypeDef = TypedDict(
    "QueueTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "clusterId": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "status": QueueStatusType,
        "computeNodeGroupConfigurations": list[ComputeNodeGroupConfigurationTypeDef],
        "slurmConfiguration": NotRequired[QueueSlurmConfigurationTypeDef],
        "errorInfo": NotRequired[list[ErrorInfoTypeDef]],
    },
)

class UpdateQueueRequestTypeDef(TypedDict):
    clusterIdentifier: str
    queueIdentifier: str
    computeNodeGroupConfigurations: NotRequired[Sequence[ComputeNodeGroupConfigurationTypeDef]]
    slurmConfiguration: NotRequired[UpdateQueueSlurmConfigurationRequestTypeDef]
    clientToken: NotRequired[str]

class CreateClusterRequestTypeDef(TypedDict):
    clusterName: str
    scheduler: SchedulerRequestTypeDef
    size: SizeType
    networking: NetworkingRequestTypeDef
    slurmConfiguration: NotRequired[ClusterSlurmConfigurationRequestTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class ClusterSlurmConfigurationTypeDef(TypedDict):
    scaleDownIdleTimeInSeconds: NotRequired[int]
    slurmCustomSettings: NotRequired[list[SlurmCustomSettingTypeDef]]
    slurmdbdCustomSettings: NotRequired[list[SlurmdbdCustomSettingTypeDef]]
    cgroupCustomSettings: NotRequired[list[CgroupCustomSettingTypeDef]]
    authKey: NotRequired[SlurmAuthKeyTypeDef]
    jwtAuth: NotRequired[JwtAuthTypeDef]
    accounting: NotRequired[AccountingTypeDef]
    slurmRest: NotRequired[SlurmRestTypeDef]

class NodeLifecycleStagesOutputTypeDef(TypedDict):
    nodeBootstrapped: NotRequired[list[NodeLifecycleScriptOutputTypeDef]]
    nodeReady: NotRequired[list[NodeLifecycleScriptOutputTypeDef]]

NodeLifecycleScriptUnionTypeDef = Union[
    NodeLifecycleScriptTypeDef, NodeLifecycleScriptOutputTypeDef
]

class UpdateClusterRequestTypeDef(TypedDict):
    clusterIdentifier: str
    clientToken: NotRequired[str]
    slurmConfiguration: NotRequired[UpdateClusterSlurmConfigurationRequestTypeDef]
    scheduler: NotRequired[UpdateSchedulerRequestTypeDef]

class CreateQueueResponseTypeDef(TypedDict):
    queue: QueueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetQueueResponseTypeDef(TypedDict):
    queue: QueueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateQueueResponseTypeDef(TypedDict):
    queue: QueueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "status": ClusterStatusType,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "scheduler": SchedulerTypeDef,
        "size": SizeType,
        "networking": NetworkingTypeDef,
        "slurmConfiguration": NotRequired[ClusterSlurmConfigurationTypeDef],
        "endpoints": NotRequired[list[EndpointTypeDef]],
        "errorInfo": NotRequired[list[ErrorInfoTypeDef]],
    },
)

class NodeLifecycleActionsTypeDef(TypedDict):
    stages: NodeLifecycleStagesOutputTypeDef
    scriptCachingPolicy: NotRequired[ScriptCachingPolicyType]

class NodeLifecycleStagesTypeDef(TypedDict):
    nodeBootstrapped: NotRequired[Sequence[NodeLifecycleScriptUnionTypeDef]]
    nodeReady: NotRequired[Sequence[NodeLifecycleScriptUnionTypeDef]]

class CreateClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ComputeNodeGroupTypeDef = TypedDict(
    "ComputeNodeGroupTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "clusterId": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "status": ComputeNodeGroupStatusType,
        "subnetIds": list[str],
        "customLaunchTemplate": CustomLaunchTemplateTypeDef,
        "iamInstanceProfileArn": str,
        "scalingConfiguration": ScalingConfigurationTypeDef,
        "instanceConfigs": list[InstanceConfigTypeDef],
        "amiId": NotRequired[str],
        "purchaseOption": NotRequired[PurchaseOptionType],
        "spotOptions": NotRequired[SpotOptionsTypeDef],
        "slurmConfiguration": NotRequired[ComputeNodeGroupSlurmConfigurationTypeDef],
        "nodeLifecycleActions": NotRequired[NodeLifecycleActionsTypeDef],
        "errorInfo": NotRequired[list[ErrorInfoTypeDef]],
    },
)

class RegisterComputeNodeGroupInstanceResponseTypeDef(TypedDict):
    nodeID: str
    sharedSecret: str
    endpoints: list[EndpointTypeDef]
    clusterName: str
    computeNodeGroupId: str
    computeNodeGroupName: str
    nodeLifecycleActions: NodeLifecycleActionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

NodeLifecycleStagesUnionTypeDef = Union[
    NodeLifecycleStagesTypeDef, NodeLifecycleStagesOutputTypeDef
]

class CreateComputeNodeGroupResponseTypeDef(TypedDict):
    computeNodeGroup: ComputeNodeGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetComputeNodeGroupResponseTypeDef(TypedDict):
    computeNodeGroup: ComputeNodeGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateComputeNodeGroupResponseTypeDef(TypedDict):
    computeNodeGroup: ComputeNodeGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class NodeLifecycleActionsRequestTypeDef(TypedDict):
    stages: NodeLifecycleStagesUnionTypeDef
    scriptCachingPolicy: NotRequired[ScriptCachingPolicyType]

class UpdateNodeLifecycleActionsRequestTypeDef(TypedDict):
    stages: NodeLifecycleStagesUnionTypeDef
    scriptCachingPolicy: NotRequired[ScriptCachingPolicyType]

class CreateComputeNodeGroupRequestTypeDef(TypedDict):
    clusterIdentifier: str
    computeNodeGroupName: str
    subnetIds: Sequence[str]
    customLaunchTemplate: CustomLaunchTemplateTypeDef
    iamInstanceProfileArn: str
    scalingConfiguration: ScalingConfigurationRequestTypeDef
    instanceConfigs: Sequence[InstanceConfigTypeDef]
    amiId: NotRequired[str]
    purchaseOption: NotRequired[PurchaseOptionType]
    spotOptions: NotRequired[SpotOptionsTypeDef]
    slurmConfiguration: NotRequired[ComputeNodeGroupSlurmConfigurationRequestTypeDef]
    nodeLifecycleActions: NotRequired[NodeLifecycleActionsRequestTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateComputeNodeGroupRequestTypeDef(TypedDict):
    clusterIdentifier: str
    computeNodeGroupIdentifier: str
    amiId: NotRequired[str]
    subnetIds: NotRequired[Sequence[str]]
    customLaunchTemplate: NotRequired[CustomLaunchTemplateTypeDef]
    purchaseOption: NotRequired[PurchaseOptionType]
    spotOptions: NotRequired[SpotOptionsTypeDef]
    scalingConfiguration: NotRequired[ScalingConfigurationRequestTypeDef]
    iamInstanceProfileArn: NotRequired[str]
    slurmConfiguration: NotRequired[UpdateComputeNodeGroupSlurmConfigurationRequestTypeDef]
    nodeLifecycleActions: NotRequired[UpdateNodeLifecycleActionsRequestTypeDef]
    clientToken: NotRequired[str]
