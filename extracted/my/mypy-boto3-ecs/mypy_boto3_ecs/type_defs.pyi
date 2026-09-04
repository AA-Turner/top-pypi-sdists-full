"""
Type annotations for ecs service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_ecs.type_defs import AcceleratorCountRequestTypeDef

    data: AcceleratorCountRequestTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    AcceleratorManufacturerType,
    AcceleratorNameType,
    AcceleratorTypeType,
    AccessTypeType,
    AgentUpdateStatusType,
    ApplicationProtocolType,
    AssignPublicIpType,
    AutoRepairActionsStatusType,
    AvailabilityZoneRebalancingType,
    BareMetalType,
    BurstablePerformanceType,
    CapacityOptionTypeType,
    CapacityProviderStatusType,
    CapacityProviderTypeType,
    CapacityProviderUpdateStatusType,
    CapacityReservationPreferenceType,
    ClusterFieldType,
    CompatibilityType,
    ConnectivityType,
    ContainerConditionType,
    ContainerInstanceFieldType,
    ContainerInstanceStatusType,
    CPUArchitectureType,
    CpuManufacturerType,
    DaemonDeploymentRollbackMonitorsStatusType,
    DaemonDeploymentStatusType,
    DaemonIpcModeType,
    DaemonPidModeType,
    DaemonPropagateTagsType,
    DaemonStatusType,
    DaemonTaskDefinitionStatusFilterType,
    DaemonTaskDefinitionStatusType,
    DeploymentControllerTypeType,
    DeploymentLifecycleHookActionType,
    DeploymentLifecycleHookStageType,
    DeploymentLifecycleHookStatusType,
    DeploymentLifecycleHookTargetTypeType,
    DeploymentRolloutStateType,
    DeploymentStrategyType,
    DesiredStatusType,
    DeviceCgroupPermissionType,
    EFSAuthorizationConfigIAMType,
    EFSTransitEncryptionType,
    ExecuteCommandLoggingType,
    ExpressGatewayServiceScalingMetricType,
    ExpressGatewayServiceStatusCodeType,
    FirelensConfigurationTypeType,
    HealthStatusType,
    InstanceGenerationType,
    InstanceHealthCheckStateType,
    InstanceHealthCheckTypeType,
    IpcModeType,
    LaunchTypeType,
    LocalStorageType,
    LocalStorageTypeType,
    LogDriverType,
    ManagedDrainingType,
    ManagedInstancesMonitoringOptionsType,
    ManagedResourceStatusType,
    ManagedScalingStatusType,
    ManagedTerminationProtectionType,
    NetworkModeType,
    OSFamilyType,
    PidModeType,
    PlacementConstraintTypeType,
    PlacementStrategyTypeType,
    PlatformDeviceTypeType,
    PropagateMITagsType,
    PropagateTagsType,
    ResourceManagementTypeType,
    ResourceTypeType,
    SchedulingStrategyType,
    ScopeType,
    ServiceConnectAccessLoggingFormatType,
    ServiceConnectIncludeQueryParametersType,
    ServiceDeploymentLifecycleStageType,
    ServiceDeploymentRollbackMonitorsStatusType,
    ServiceDeploymentStatusType,
    ServiceRevisionCleanupType,
    SettingNameType,
    SettingTypeType,
    SortOrderType,
    StabilityStatusType,
    StopServiceDeploymentStopTypeType,
    TaskDefinitionFamilyStatusType,
    TaskDefinitionStatusType,
    TaskFilesystemTypeType,
    TaskStopCodeType,
    ThresholdTypeType,
    TransportProtocolType,
    UlimitNameType,
    VersionConsistencyType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceleratorCountRequestTypeDef",
    "AcceleratorTotalMemoryMiBRequestTypeDef",
    "AdvancedConfigurationTypeDef",
    "AttachmentStateChangeTypeDef",
    "AttachmentTypeDef",
    "AttributeTypeDef",
    "AutoRepairConfigurationTypeDef",
    "AutoScalingGroupProviderTypeDef",
    "AutoScalingGroupProviderUpdateTypeDef",
    "AwsVpcConfigurationOutputTypeDef",
    "AwsVpcConfigurationTypeDef",
    "BaselineEbsBandwidthMbpsRequestTypeDef",
    "CanaryConfigurationTypeDef",
    "CapacityProviderStrategyItemTypeDef",
    "CapacityProviderTypeDef",
    "CapacityReservationRequestTypeDef",
    "ClusterConfigurationTypeDef",
    "ClusterServiceConnectDefaultsRequestTypeDef",
    "ClusterServiceConnectDefaultsTypeDef",
    "ClusterSettingTypeDef",
    "ClusterTypeDef",
    "ContainerDefinitionOutputTypeDef",
    "ContainerDefinitionTypeDef",
    "ContainerDefinitionUnionTypeDef",
    "ContainerDependencyTypeDef",
    "ContainerImageTypeDef",
    "ContainerInstanceHealthStatusTypeDef",
    "ContainerInstanceTypeDef",
    "ContainerOverrideOutputTypeDef",
    "ContainerOverrideTypeDef",
    "ContainerRestartPolicyOutputTypeDef",
    "ContainerRestartPolicyTypeDef",
    "ContainerRestartPolicyUnionTypeDef",
    "ContainerStateChangeTypeDef",
    "ContainerTypeDef",
    "ContinueServiceDeploymentRequestTypeDef",
    "ContinueServiceDeploymentResponseTypeDef",
    "CreateCapacityProviderRequestTypeDef",
    "CreateCapacityProviderResponseTypeDef",
    "CreateClusterRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateDaemonRequestTypeDef",
    "CreateDaemonResponseTypeDef",
    "CreateExpressGatewayServiceRequestTypeDef",
    "CreateExpressGatewayServiceResponseTypeDef",
    "CreateManagedInstancesProviderConfigurationTypeDef",
    "CreateServiceRequestTypeDef",
    "CreateServiceResponseTypeDef",
    "CreateTaskSetRequestTypeDef",
    "CreateTaskSetResponseTypeDef",
    "CreatedAtTypeDef",
    "DaemonAlarmConfigurationOutputTypeDef",
    "DaemonAlarmConfigurationTypeDef",
    "DaemonCapacityProviderTypeDef",
    "DaemonCircuitBreakerTypeDef",
    "DaemonContainerDefinitionOutputTypeDef",
    "DaemonContainerDefinitionTypeDef",
    "DaemonContainerDefinitionUnionTypeDef",
    "DaemonContainerImageTypeDef",
    "DaemonDeploymentAlarmsTypeDef",
    "DaemonDeploymentCapacityProviderTypeDef",
    "DaemonDeploymentConfigurationOutputTypeDef",
    "DaemonDeploymentConfigurationTypeDef",
    "DaemonDeploymentConfigurationUnionTypeDef",
    "DaemonDeploymentRevisionDetailTypeDef",
    "DaemonDeploymentSummaryTypeDef",
    "DaemonDeploymentTypeDef",
    "DaemonDetailTypeDef",
    "DaemonLinuxParametersOutputTypeDef",
    "DaemonLinuxParametersTypeDef",
    "DaemonLinuxParametersUnionTypeDef",
    "DaemonRevisionDetailTypeDef",
    "DaemonRevisionTypeDef",
    "DaemonRollbackTypeDef",
    "DaemonSummaryTypeDef",
    "DaemonTaskDefinitionSummaryTypeDef",
    "DaemonTaskDefinitionTypeDef",
    "DaemonVolumeTypeDef",
    "DeleteAccountSettingRequestTypeDef",
    "DeleteAccountSettingResponseTypeDef",
    "DeleteAttributesRequestTypeDef",
    "DeleteAttributesResponseTypeDef",
    "DeleteCapacityProviderRequestTypeDef",
    "DeleteCapacityProviderResponseTypeDef",
    "DeleteClusterRequestTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteDaemonRequestTypeDef",
    "DeleteDaemonResponseTypeDef",
    "DeleteDaemonTaskDefinitionRequestTypeDef",
    "DeleteDaemonTaskDefinitionResponseTypeDef",
    "DeleteExpressGatewayServiceRequestTypeDef",
    "DeleteExpressGatewayServiceResponseTypeDef",
    "DeleteServiceRequestTypeDef",
    "DeleteServiceResponseTypeDef",
    "DeleteTaskDefinitionsRequestTypeDef",
    "DeleteTaskDefinitionsResponseTypeDef",
    "DeleteTaskSetRequestTypeDef",
    "DeleteTaskSetResponseTypeDef",
    "DeploymentAlarmsOutputTypeDef",
    "DeploymentAlarmsTypeDef",
    "DeploymentCircuitBreakerTypeDef",
    "DeploymentConfigurationOutputTypeDef",
    "DeploymentConfigurationTypeDef",
    "DeploymentConfigurationUnionTypeDef",
    "DeploymentControllerTypeDef",
    "DeploymentEarlySuccessCriteriaTypeDef",
    "DeploymentEphemeralStorageTypeDef",
    "DeploymentLifecycleHookDetailTypeDef",
    "DeploymentLifecycleHookOutputTypeDef",
    "DeploymentLifecycleHookTimeoutConfigurationTypeDef",
    "DeploymentLifecycleHookTypeDef",
    "DeploymentTypeDef",
    "DeregisterContainerInstanceRequestTypeDef",
    "DeregisterContainerInstanceResponseTypeDef",
    "DeregisterTaskDefinitionRequestTypeDef",
    "DeregisterTaskDefinitionResponseTypeDef",
    "DescribeCapacityProvidersRequestTypeDef",
    "DescribeCapacityProvidersResponseTypeDef",
    "DescribeClustersRequestTypeDef",
    "DescribeClustersResponseTypeDef",
    "DescribeContainerInstancesRequestTypeDef",
    "DescribeContainerInstancesResponseTypeDef",
    "DescribeDaemonDeploymentsRequestTypeDef",
    "DescribeDaemonDeploymentsRequestWaitExtraTypeDef",
    "DescribeDaemonDeploymentsRequestWaitTypeDef",
    "DescribeDaemonDeploymentsResponseTypeDef",
    "DescribeDaemonRequestTypeDef",
    "DescribeDaemonRequestWaitTypeDef",
    "DescribeDaemonResponseTypeDef",
    "DescribeDaemonRevisionsRequestTypeDef",
    "DescribeDaemonRevisionsResponseTypeDef",
    "DescribeDaemonTaskDefinitionRequestTypeDef",
    "DescribeDaemonTaskDefinitionRequestWaitExtraTypeDef",
    "DescribeDaemonTaskDefinitionRequestWaitTypeDef",
    "DescribeDaemonTaskDefinitionResponseTypeDef",
    "DescribeExpressGatewayServiceRequestTypeDef",
    "DescribeExpressGatewayServiceResponseTypeDef",
    "DescribeServiceDeploymentsRequestTypeDef",
    "DescribeServiceDeploymentsResponseTypeDef",
    "DescribeServiceRevisionsRequestTypeDef",
    "DescribeServiceRevisionsResponseTypeDef",
    "DescribeServicesRequestTypeDef",
    "DescribeServicesRequestWaitExtraTypeDef",
    "DescribeServicesRequestWaitTypeDef",
    "DescribeServicesResponseTypeDef",
    "DescribeTaskDefinitionRequestTypeDef",
    "DescribeTaskDefinitionResponseTypeDef",
    "DescribeTaskSetsRequestTypeDef",
    "DescribeTaskSetsResponseTypeDef",
    "DescribeTasksRequestTypeDef",
    "DescribeTasksRequestWaitExtraTypeDef",
    "DescribeTasksRequestWaitTypeDef",
    "DescribeTasksResponseTypeDef",
    "DeviceOutputTypeDef",
    "DeviceTypeDef",
    "DeviceUnionTypeDef",
    "DiscoverPollEndpointRequestTypeDef",
    "DiscoverPollEndpointResponseTypeDef",
    "DockerVolumeConfigurationOutputTypeDef",
    "DockerVolumeConfigurationTypeDef",
    "DockerVolumeConfigurationUnionTypeDef",
    "EBSTagSpecificationOutputTypeDef",
    "EBSTagSpecificationTypeDef",
    "EBSTagSpecificationUnionTypeDef",
    "ECSExpressGatewayServiceTypeDef",
    "ECSManagedResourcesTypeDef",
    "EFSAuthorizationConfigTypeDef",
    "EFSVolumeConfigurationTypeDef",
    "EnvironmentFileTypeDef",
    "EphemeralStorageTypeDef",
    "ExecuteCommandConfigurationTypeDef",
    "ExecuteCommandLogConfigurationTypeDef",
    "ExecuteCommandRequestTypeDef",
    "ExecuteCommandResponseTypeDef",
    "ExpressGatewayContainerOutputTypeDef",
    "ExpressGatewayContainerTypeDef",
    "ExpressGatewayContainerUnionTypeDef",
    "ExpressGatewayRepositoryCredentialsTypeDef",
    "ExpressGatewayScalingTargetTypeDef",
    "ExpressGatewayServiceAwsLogsConfigurationTypeDef",
    "ExpressGatewayServiceConfigurationTypeDef",
    "ExpressGatewayServiceNetworkConfigurationOutputTypeDef",
    "ExpressGatewayServiceNetworkConfigurationTypeDef",
    "ExpressGatewayServiceNetworkConfigurationUnionTypeDef",
    "ExpressGatewayServiceStatusTypeDef",
    "FSxWindowsFileServerAuthorizationConfigTypeDef",
    "FSxWindowsFileServerVolumeConfigurationTypeDef",
    "FailureTypeDef",
    "FirelensConfigurationOutputTypeDef",
    "FirelensConfigurationTypeDef",
    "FirelensConfigurationUnionTypeDef",
    "GetTaskProtectionRequestTypeDef",
    "GetTaskProtectionResponseTypeDef",
    "HealthCheckOutputTypeDef",
    "HealthCheckTypeDef",
    "HealthCheckUnionTypeDef",
    "HostEntryTypeDef",
    "HostVolumePropertiesTypeDef",
    "InferenceAcceleratorOverrideTypeDef",
    "InferenceAcceleratorTypeDef",
    "InfrastructureOptimizationTypeDef",
    "IngressPathSummaryTypeDef",
    "InstanceHealthCheckResultTypeDef",
    "InstanceLaunchTemplateOutputTypeDef",
    "InstanceLaunchTemplateTypeDef",
    "InstanceLaunchTemplateUnionTypeDef",
    "InstanceLaunchTemplateUpdateTypeDef",
    "InstanceRequirementsRequestOutputTypeDef",
    "InstanceRequirementsRequestTypeDef",
    "InstanceRequirementsRequestUnionTypeDef",
    "KernelCapabilitiesOutputTypeDef",
    "KernelCapabilitiesTypeDef",
    "KernelCapabilitiesUnionTypeDef",
    "KeyValuePairTypeDef",
    "LinearConfigurationTypeDef",
    "LinuxParametersOutputTypeDef",
    "LinuxParametersTypeDef",
    "LinuxParametersUnionTypeDef",
    "ListAccountSettingsRequestPaginateTypeDef",
    "ListAccountSettingsRequestTypeDef",
    "ListAccountSettingsResponseTypeDef",
    "ListAttributesRequestPaginateTypeDef",
    "ListAttributesRequestTypeDef",
    "ListAttributesResponseTypeDef",
    "ListClustersRequestPaginateTypeDef",
    "ListClustersRequestTypeDef",
    "ListClustersResponseTypeDef",
    "ListContainerInstancesRequestPaginateTypeDef",
    "ListContainerInstancesRequestTypeDef",
    "ListContainerInstancesResponseTypeDef",
    "ListDaemonDeploymentsRequestTypeDef",
    "ListDaemonDeploymentsResponseTypeDef",
    "ListDaemonTaskDefinitionsRequestTypeDef",
    "ListDaemonTaskDefinitionsResponseTypeDef",
    "ListDaemonsRequestTypeDef",
    "ListDaemonsResponseTypeDef",
    "ListServiceDeploymentsRequestTypeDef",
    "ListServiceDeploymentsResponseTypeDef",
    "ListServicesByNamespaceRequestPaginateTypeDef",
    "ListServicesByNamespaceRequestTypeDef",
    "ListServicesByNamespaceResponseTypeDef",
    "ListServicesRequestPaginateTypeDef",
    "ListServicesRequestTypeDef",
    "ListServicesResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTaskDefinitionFamiliesRequestPaginateTypeDef",
    "ListTaskDefinitionFamiliesRequestTypeDef",
    "ListTaskDefinitionFamiliesResponseTypeDef",
    "ListTaskDefinitionsRequestPaginateTypeDef",
    "ListTaskDefinitionsRequestTypeDef",
    "ListTaskDefinitionsResponseTypeDef",
    "ListTasksRequestPaginateTypeDef",
    "ListTasksRequestTypeDef",
    "ListTasksResponseTypeDef",
    "LoadBalancerTypeDef",
    "LogConfigurationOutputTypeDef",
    "LogConfigurationTypeDef",
    "LogConfigurationUnionTypeDef",
    "ManagedAgentStateChangeTypeDef",
    "ManagedAgentTypeDef",
    "ManagedApplicationAutoScalingPolicyTypeDef",
    "ManagedAutoScalingTypeDef",
    "ManagedCertificateTypeDef",
    "ManagedIngressPathTypeDef",
    "ManagedInstancesLocalStorageConfigurationTypeDef",
    "ManagedInstancesNetworkConfigurationOutputTypeDef",
    "ManagedInstancesNetworkConfigurationTypeDef",
    "ManagedInstancesNetworkConfigurationUnionTypeDef",
    "ManagedInstancesProviderTypeDef",
    "ManagedInstancesStorageConfigurationTypeDef",
    "ManagedListenerRuleTypeDef",
    "ManagedListenerTypeDef",
    "ManagedLoadBalancerTypeDef",
    "ManagedLogGroupTypeDef",
    "ManagedMetricAlarmTypeDef",
    "ManagedScalableTargetTypeDef",
    "ManagedScalingTypeDef",
    "ManagedSecurityGroupTypeDef",
    "ManagedStorageConfigurationTypeDef",
    "ManagedTargetGroupTypeDef",
    "MemoryGiBPerVCpuRequestTypeDef",
    "MemoryMiBRequestTypeDef",
    "MetricConfigurationOutputTypeDef",
    "MetricConfigurationTypeDef",
    "MonitoringConfigurationOutputTypeDef",
    "MonitoringConfigurationTypeDef",
    "MonitoringConfigurationUnionTypeDef",
    "MountPointTypeDef",
    "NetworkBandwidthGbpsRequestTypeDef",
    "NetworkBindingTypeDef",
    "NetworkConfigurationOutputTypeDef",
    "NetworkConfigurationTypeDef",
    "NetworkConfigurationUnionTypeDef",
    "NetworkInterfaceCountRequestTypeDef",
    "NetworkInterfaceTypeDef",
    "PaginatorConfigTypeDef",
    "PlacementConstraintTypeDef",
    "PlacementStrategyTypeDef",
    "PlatformDeviceTypeDef",
    "PortMappingTypeDef",
    "ProtectedTaskTypeDef",
    "ProxyConfigurationOutputTypeDef",
    "ProxyConfigurationTypeDef",
    "ProxyConfigurationUnionTypeDef",
    "PutAccountSettingDefaultRequestTypeDef",
    "PutAccountSettingDefaultResponseTypeDef",
    "PutAccountSettingRequestTypeDef",
    "PutAccountSettingResponseTypeDef",
    "PutAttributesRequestTypeDef",
    "PutAttributesResponseTypeDef",
    "PutClusterCapacityProvidersRequestTypeDef",
    "PutClusterCapacityProvidersResponseTypeDef",
    "RegisterContainerInstanceRequestTypeDef",
    "RegisterContainerInstanceResponseTypeDef",
    "RegisterDaemonTaskDefinitionRequestTypeDef",
    "RegisterDaemonTaskDefinitionResponseTypeDef",
    "RegisterTaskDefinitionRequestTypeDef",
    "RegisterTaskDefinitionResponseTypeDef",
    "RepositoryCredentialsTypeDef",
    "ResolvedConfigurationTypeDef",
    "ResourceOutputTypeDef",
    "ResourceRequirementTypeDef",
    "ResourceTypeDef",
    "ResourceUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RollbackTypeDef",
    "RunTaskRequestTypeDef",
    "RunTaskResponseTypeDef",
    "RuntimePlatformOverrideTypeDef",
    "RuntimePlatformTypeDef",
    "S3FilesVolumeConfigurationTypeDef",
    "ScaleTypeDef",
    "SecretTypeDef",
    "ServiceConnectAccessLogConfigurationTypeDef",
    "ServiceConnectClientAliasTypeDef",
    "ServiceConnectConfigurationOutputTypeDef",
    "ServiceConnectConfigurationTypeDef",
    "ServiceConnectConfigurationUnionTypeDef",
    "ServiceConnectServiceOutputTypeDef",
    "ServiceConnectServiceResourceTypeDef",
    "ServiceConnectServiceTypeDef",
    "ServiceConnectTestTrafficHeaderMatchRulesTypeDef",
    "ServiceConnectTestTrafficHeaderRulesTypeDef",
    "ServiceConnectTestTrafficRulesTypeDef",
    "ServiceConnectTlsCertificateAuthorityTypeDef",
    "ServiceConnectTlsConfigurationTypeDef",
    "ServiceCurrentRevisionSummaryTypeDef",
    "ServiceDeploymentAlarmsTypeDef",
    "ServiceDeploymentBriefTypeDef",
    "ServiceDeploymentCircuitBreakerTypeDef",
    "ServiceDeploymentTypeDef",
    "ServiceEventTypeDef",
    "ServiceManagedEBSVolumeConfigurationOutputTypeDef",
    "ServiceManagedEBSVolumeConfigurationTypeDef",
    "ServiceManagedEBSVolumeConfigurationUnionTypeDef",
    "ServiceRegistryTypeDef",
    "ServiceRevisionLoadBalancerTypeDef",
    "ServiceRevisionOverridesTypeDef",
    "ServiceRevisionSummaryTypeDef",
    "ServiceRevisionTypeDef",
    "ServiceTypeDef",
    "ServiceVolumeConfigurationOutputTypeDef",
    "ServiceVolumeConfigurationTypeDef",
    "ServiceVolumeConfigurationUnionTypeDef",
    "SessionTypeDef",
    "SettingTypeDef",
    "StartTaskRequestTypeDef",
    "StartTaskResponseTypeDef",
    "StopServiceDeploymentRequestTypeDef",
    "StopServiceDeploymentResponseTypeDef",
    "StopTaskRequestTypeDef",
    "StopTaskResponseTypeDef",
    "SubmitAttachmentStateChangesRequestTypeDef",
    "SubmitAttachmentStateChangesResponseTypeDef",
    "SubmitContainerStateChangeRequestTypeDef",
    "SubmitContainerStateChangeResponseTypeDef",
    "SubmitTaskStateChangeRequestTypeDef",
    "SubmitTaskStateChangeResponseTypeDef",
    "SystemControlTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TaskDefinitionPlacementConstraintTypeDef",
    "TaskDefinitionTypeDef",
    "TaskEphemeralStorageTypeDef",
    "TaskManagedEBSVolumeConfigurationTypeDef",
    "TaskManagedEBSVolumeTerminationPolicyTypeDef",
    "TaskOverrideOutputTypeDef",
    "TaskOverrideTypeDef",
    "TaskOverrideUnionTypeDef",
    "TaskSetTypeDef",
    "TaskTypeDef",
    "TaskVolumeConfigurationTypeDef",
    "ThresholdConfigurationTypeDef",
    "TimeoutConfigurationTypeDef",
    "TimestampTypeDef",
    "TmpfsOutputTypeDef",
    "TmpfsTypeDef",
    "TmpfsUnionTypeDef",
    "TotalLocalStorageGBRequestTypeDef",
    "UlimitTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateCapacityProviderRequestTypeDef",
    "UpdateCapacityProviderResponseTypeDef",
    "UpdateClusterRequestTypeDef",
    "UpdateClusterResponseTypeDef",
    "UpdateClusterSettingsRequestTypeDef",
    "UpdateClusterSettingsResponseTypeDef",
    "UpdateContainerAgentRequestTypeDef",
    "UpdateContainerAgentResponseTypeDef",
    "UpdateContainerInstancesStateRequestTypeDef",
    "UpdateContainerInstancesStateResponseTypeDef",
    "UpdateDaemonRequestTypeDef",
    "UpdateDaemonResponseTypeDef",
    "UpdateExpressGatewayServiceRequestTypeDef",
    "UpdateExpressGatewayServiceResponseTypeDef",
    "UpdateManagedInstancesProviderConfigurationTypeDef",
    "UpdateServicePrimaryTaskSetRequestTypeDef",
    "UpdateServicePrimaryTaskSetResponseTypeDef",
    "UpdateServiceRequestTypeDef",
    "UpdateServiceResponseTypeDef",
    "UpdateTaskProtectionRequestTypeDef",
    "UpdateTaskProtectionResponseTypeDef",
    "UpdateTaskSetRequestTypeDef",
    "UpdateTaskSetResponseTypeDef",
    "UpdatedExpressGatewayServiceTypeDef",
    "VCpuCountRangeRequestTypeDef",
    "VersionInfoTypeDef",
    "VolumeFromTypeDef",
    "VolumeOutputTypeDef",
    "VolumeTypeDef",
    "VolumeUnionTypeDef",
    "VpcLatticeConfigurationTypeDef",
    "WaiterConfigTypeDef",
)

AcceleratorCountRequestTypeDef = TypedDict(
    "AcceleratorCountRequestTypeDef",
    {
        "min": NotRequired[int],
        "max": NotRequired[int],
    },
)
AcceleratorTotalMemoryMiBRequestTypeDef = TypedDict(
    "AcceleratorTotalMemoryMiBRequestTypeDef",
    {
        "min": NotRequired[int],
        "max": NotRequired[int],
    },
)

class AdvancedConfigurationTypeDef(TypedDict):
    alternateTargetGroupArn: NotRequired[str]
    productionListenerRule: NotRequired[str]
    testListenerRule: NotRequired[str]
    roleArn: NotRequired[str]

class AttachmentStateChangeTypeDef(TypedDict):
    attachmentArn: str
    status: str

class KeyValuePairTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]

class AttributeTypeDef(TypedDict):
    name: str
    value: NotRequired[str]
    targetType: NotRequired[Literal["container-instance"]]
    targetId: NotRequired[str]

class AutoRepairConfigurationTypeDef(TypedDict):
    actionsStatus: NotRequired[AutoRepairActionsStatusType]

class ManagedScalingTypeDef(TypedDict):
    status: NotRequired[ManagedScalingStatusType]
    targetCapacity: NotRequired[int]
    minimumScalingStepSize: NotRequired[int]
    maximumScalingStepSize: NotRequired[int]
    instanceWarmupPeriod: NotRequired[int]

class AwsVpcConfigurationOutputTypeDef(TypedDict):
    subnets: list[str]
    securityGroups: NotRequired[list[str]]
    assignPublicIp: NotRequired[AssignPublicIpType]

class AwsVpcConfigurationTypeDef(TypedDict):
    subnets: Sequence[str]
    securityGroups: NotRequired[Sequence[str]]
    assignPublicIp: NotRequired[AssignPublicIpType]

BaselineEbsBandwidthMbpsRequestTypeDef = TypedDict(
    "BaselineEbsBandwidthMbpsRequestTypeDef",
    {
        "min": NotRequired[int],
        "max": NotRequired[int],
    },
)

class CanaryConfigurationTypeDef(TypedDict):
    canaryPercent: NotRequired[float]
    canaryBakeTimeInMinutes: NotRequired[int]

class CapacityProviderStrategyItemTypeDef(TypedDict):
    capacityProvider: str
    weight: NotRequired[int]
    base: NotRequired[int]

class TagTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

class CapacityReservationRequestTypeDef(TypedDict):
    reservationGroupArn: NotRequired[str]
    reservationPreference: NotRequired[CapacityReservationPreferenceType]

class ManagedStorageConfigurationTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]
    fargateEphemeralStorageKmsKeyId: NotRequired[str]

class ClusterServiceConnectDefaultsRequestTypeDef(TypedDict):
    namespace: str

class ClusterServiceConnectDefaultsTypeDef(TypedDict):
    namespace: NotRequired[str]

class ClusterSettingTypeDef(TypedDict):
    name: NotRequired[Literal["containerInsights"]]
    value: NotRequired[str]

class ContainerDependencyTypeDef(TypedDict):
    containerName: str
    condition: ContainerConditionType

class ContainerRestartPolicyOutputTypeDef(TypedDict):
    enabled: bool
    ignoredExitCodes: NotRequired[list[int]]
    restartAttemptPeriod: NotRequired[int]

EnvironmentFileTypeDef = TypedDict(
    "EnvironmentFileTypeDef",
    {
        "value": str,
        "type": Literal["s3"],
    },
)
FirelensConfigurationOutputTypeDef = TypedDict(
    "FirelensConfigurationOutputTypeDef",
    {
        "type": FirelensConfigurationTypeType,
        "options": NotRequired[dict[str, str]],
    },
)

class HealthCheckOutputTypeDef(TypedDict):
    command: list[str]
    interval: NotRequired[int]
    timeout: NotRequired[int]
    retries: NotRequired[int]
    startPeriod: NotRequired[int]

class HostEntryTypeDef(TypedDict):
    hostname: str
    ipAddress: str

class MountPointTypeDef(TypedDict):
    sourceVolume: NotRequired[str]
    containerPath: NotRequired[str]
    readOnly: NotRequired[bool]

class PortMappingTypeDef(TypedDict):
    containerPort: NotRequired[int]
    hostPort: NotRequired[int]
    protocol: NotRequired[TransportProtocolType]
    name: NotRequired[str]
    appProtocol: NotRequired[ApplicationProtocolType]
    containerPortRange: NotRequired[str]

class RepositoryCredentialsTypeDef(TypedDict):
    credentialsParameter: str

ResourceRequirementTypeDef = TypedDict(
    "ResourceRequirementTypeDef",
    {
        "value": str,
        "type": ResourceTypeType,
    },
)

class SecretTypeDef(TypedDict):
    name: str
    valueFrom: str

class SystemControlTypeDef(TypedDict):
    namespace: NotRequired[str]
    value: NotRequired[str]

class UlimitTypeDef(TypedDict):
    name: UlimitNameType
    softLimit: int
    hardLimit: int

class VolumeFromTypeDef(TypedDict):
    sourceContainer: NotRequired[str]
    readOnly: NotRequired[bool]

class ContainerImageTypeDef(TypedDict):
    containerName: NotRequired[str]
    imageDigest: NotRequired[str]
    image: NotRequired[str]

InstanceHealthCheckResultTypeDef = TypedDict(
    "InstanceHealthCheckResultTypeDef",
    {
        "type": NotRequired[InstanceHealthCheckTypeType],
        "status": NotRequired[InstanceHealthCheckStateType],
        "statusReason": NotRequired[str],
        "lastUpdated": NotRequired[datetime],
        "lastStatusChange": NotRequired[datetime],
    },
)
ResourceOutputTypeDef = TypedDict(
    "ResourceOutputTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "doubleValue": NotRequired[float],
        "longValue": NotRequired[int],
        "integerValue": NotRequired[int],
        "stringSetValue": NotRequired[list[str]],
    },
)

class VersionInfoTypeDef(TypedDict):
    agentVersion: NotRequired[str]
    agentHash: NotRequired[str]
    dockerVersion: NotRequired[str]

class ContainerRestartPolicyTypeDef(TypedDict):
    enabled: bool
    ignoredExitCodes: NotRequired[Sequence[int]]
    restartAttemptPeriod: NotRequired[int]

class NetworkBindingTypeDef(TypedDict):
    bindIP: NotRequired[str]
    containerPort: NotRequired[int]
    hostPort: NotRequired[int]
    protocol: NotRequired[TransportProtocolType]
    containerPortRange: NotRequired[str]
    hostPortRange: NotRequired[str]

class ManagedAgentTypeDef(TypedDict):
    lastStartedAt: NotRequired[datetime]
    name: NotRequired[Literal["ExecuteCommandAgent"]]
    reason: NotRequired[str]
    lastStatus: NotRequired[str]

class NetworkInterfaceTypeDef(TypedDict):
    attachmentId: NotRequired[str]
    privateIpv4Address: NotRequired[str]
    ipv6Address: NotRequired[str]

class ContinueServiceDeploymentRequestTypeDef(TypedDict):
    serviceDeploymentArn: str
    hookId: str
    action: NotRequired[DeploymentLifecycleHookActionType]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ExpressGatewayScalingTargetTypeDef(TypedDict):
    minTaskCount: NotRequired[int]
    maxTaskCount: NotRequired[int]
    autoScalingMetric: NotRequired[ExpressGatewayServiceScalingMetricType]
    autoScalingTargetValue: NotRequired[int]

class InfrastructureOptimizationTypeDef(TypedDict):
    scaleInAfter: NotRequired[int]

DeploymentControllerTypeDef = TypedDict(
    "DeploymentControllerTypeDef",
    {
        "type": DeploymentControllerTypeType,
    },
)
PlacementConstraintTypeDef = TypedDict(
    "PlacementConstraintTypeDef",
    {
        "type": NotRequired[PlacementConstraintTypeType],
        "expression": NotRequired[str],
    },
)
PlacementStrategyTypeDef = TypedDict(
    "PlacementStrategyTypeDef",
    {
        "type": NotRequired[PlacementStrategyTypeType],
        "field": NotRequired[str],
    },
)

class ServiceRegistryTypeDef(TypedDict):
    registryArn: NotRequired[str]
    port: NotRequired[int]
    containerName: NotRequired[str]
    containerPort: NotRequired[int]

class VpcLatticeConfigurationTypeDef(TypedDict):
    roleArn: str
    targetGroupArn: str
    portName: str

class ScaleTypeDef(TypedDict):
    value: NotRequired[float]
    unit: NotRequired[Literal["PERCENT"]]

TimestampTypeDef = Union[datetime, str]

class DaemonAlarmConfigurationOutputTypeDef(TypedDict):
    alarmNames: NotRequired[list[str]]
    enable: NotRequired[bool]

class DaemonAlarmConfigurationTypeDef(TypedDict):
    alarmNames: NotRequired[Sequence[str]]
    enable: NotRequired[bool]

class DaemonCapacityProviderTypeDef(TypedDict):
    arn: NotRequired[str]
    runningCount: NotRequired[int]
    withoutDaemonCount: NotRequired[int]

class DaemonCircuitBreakerTypeDef(TypedDict):
    failureCount: NotRequired[int]
    status: NotRequired[DaemonDeploymentRollbackMonitorsStatusType]
    threshold: NotRequired[int]

class DaemonContainerImageTypeDef(TypedDict):
    containerName: NotRequired[str]
    imageDigest: NotRequired[str]
    image: NotRequired[str]

class DaemonDeploymentAlarmsTypeDef(TypedDict):
    status: NotRequired[DaemonDeploymentRollbackMonitorsStatusType]
    alarmNames: NotRequired[list[str]]
    triggeredAlarmNames: NotRequired[list[str]]

class DaemonDeploymentCapacityProviderTypeDef(TypedDict):
    arn: NotRequired[str]
    runningInstanceCount: NotRequired[int]
    withoutDaemonInstanceCount: NotRequired[int]
    drainingInstanceCount: NotRequired[int]

class DaemonDeploymentSummaryTypeDef(TypedDict):
    daemonDeploymentArn: NotRequired[str]
    daemonArn: NotRequired[str]
    clusterArn: NotRequired[str]
    status: NotRequired[DaemonDeploymentStatusType]
    statusReason: NotRequired[str]
    targetDaemonRevisionArn: NotRequired[str]
    createdAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    stoppedAt: NotRequired[datetime]
    finishedAt: NotRequired[datetime]

class DaemonRollbackTypeDef(TypedDict):
    reason: NotRequired[str]
    startedAt: NotRequired[datetime]
    rollbackTargetDaemonRevisionArn: NotRequired[str]
    rollbackCapacityProviders: NotRequired[list[str]]

class DeviceOutputTypeDef(TypedDict):
    hostPath: str
    containerPath: NotRequired[str]
    permissions: NotRequired[list[DeviceCgroupPermissionType]]

class KernelCapabilitiesOutputTypeDef(TypedDict):
    add: NotRequired[list[str]]
    drop: NotRequired[list[str]]

class TmpfsOutputTypeDef(TypedDict):
    containerPath: str
    size: int
    mountOptions: NotRequired[list[str]]

class DaemonSummaryTypeDef(TypedDict):
    daemonArn: NotRequired[str]
    status: NotRequired[DaemonStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class DaemonTaskDefinitionSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    registeredAt: NotRequired[datetime]
    registeredBy: NotRequired[str]
    deleteRequestedAt: NotRequired[datetime]
    status: NotRequired[DaemonTaskDefinitionStatusType]

class HostVolumePropertiesTypeDef(TypedDict):
    sourcePath: NotRequired[str]

class DeleteAccountSettingRequestTypeDef(TypedDict):
    name: SettingNameType
    principalArn: NotRequired[str]

SettingTypeDef = TypedDict(
    "SettingTypeDef",
    {
        "name": NotRequired[SettingNameType],
        "value": NotRequired[str],
        "principalArn": NotRequired[str],
        "type": NotRequired[SettingTypeType],
    },
)

class DeleteCapacityProviderRequestTypeDef(TypedDict):
    capacityProvider: str
    cluster: NotRequired[str]

class DeleteClusterRequestTypeDef(TypedDict):
    cluster: str

class DeleteDaemonRequestTypeDef(TypedDict):
    daemonArn: str

class DeleteDaemonTaskDefinitionRequestTypeDef(TypedDict):
    daemonTaskDefinition: str

class DeleteExpressGatewayServiceRequestTypeDef(TypedDict):
    serviceArn: str

class DeleteServiceRequestTypeDef(TypedDict):
    service: str
    cluster: NotRequired[str]
    force: NotRequired[bool]

class DeleteTaskDefinitionsRequestTypeDef(TypedDict):
    taskDefinitions: Sequence[str]

class FailureTypeDef(TypedDict):
    arn: NotRequired[str]
    reason: NotRequired[str]
    detail: NotRequired[str]

class DeleteTaskSetRequestTypeDef(TypedDict):
    cluster: str
    service: str
    taskSet: str
    force: NotRequired[bool]

class DeploymentAlarmsOutputTypeDef(TypedDict):
    alarmNames: list[str]
    rollback: bool
    enable: bool

class DeploymentAlarmsTypeDef(TypedDict):
    alarmNames: Sequence[str]
    rollback: bool
    enable: bool

ThresholdConfigurationTypeDef = TypedDict(
    "ThresholdConfigurationTypeDef",
    {
        "type": ThresholdTypeType,
        "value": int,
    },
)

class DeploymentEarlySuccessCriteriaTypeDef(TypedDict):
    enable: bool
    healthyPercent: NotRequired[int]
    sourceServiceRevisionCleanup: NotRequired[ServiceRevisionCleanupType]

class LinearConfigurationTypeDef(TypedDict):
    stepPercent: NotRequired[float]
    stepBakeTimeInMinutes: NotRequired[int]

class DeploymentEphemeralStorageTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]

class DeploymentLifecycleHookDetailTypeDef(TypedDict):
    hookId: NotRequired[str]
    targetType: NotRequired[DeploymentLifecycleHookTargetTypeType]
    targetArn: NotRequired[str]
    status: NotRequired[DeploymentLifecycleHookStatusType]
    expiresAt: NotRequired[datetime]
    timeoutAction: NotRequired[DeploymentLifecycleHookActionType]

class DeploymentLifecycleHookTimeoutConfigurationTypeDef(TypedDict):
    timeoutInMinutes: NotRequired[int]
    action: NotRequired[DeploymentLifecycleHookActionType]

class ServiceConnectServiceResourceTypeDef(TypedDict):
    discoveryName: NotRequired[str]
    discoveryArn: NotRequired[str]

class DeregisterContainerInstanceRequestTypeDef(TypedDict):
    containerInstance: str
    cluster: NotRequired[str]
    force: NotRequired[bool]

class DeregisterTaskDefinitionRequestTypeDef(TypedDict):
    taskDefinition: str

class DescribeCapacityProvidersRequestTypeDef(TypedDict):
    capacityProviders: NotRequired[Sequence[str]]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[Literal["TAGS"]]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class DescribeClustersRequestTypeDef(TypedDict):
    clusters: NotRequired[Sequence[str]]
    include: NotRequired[Sequence[ClusterFieldType]]

class DescribeContainerInstancesRequestTypeDef(TypedDict):
    containerInstances: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[ContainerInstanceFieldType]]

class DescribeDaemonDeploymentsRequestTypeDef(TypedDict):
    daemonDeploymentArns: Sequence[str]

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class DescribeDaemonRequestTypeDef(TypedDict):
    daemonArn: str

class DescribeDaemonRevisionsRequestTypeDef(TypedDict):
    daemonRevisionArns: Sequence[str]

class DescribeDaemonTaskDefinitionRequestTypeDef(TypedDict):
    daemonTaskDefinition: str

class DescribeExpressGatewayServiceRequestTypeDef(TypedDict):
    serviceArn: str
    include: NotRequired[Sequence[Literal["TAGS"]]]

class DescribeServiceDeploymentsRequestTypeDef(TypedDict):
    serviceDeploymentArns: Sequence[str]

class DescribeServiceRevisionsRequestTypeDef(TypedDict):
    serviceRevisionArns: Sequence[str]

class DescribeServicesRequestTypeDef(TypedDict):
    services: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[Literal["TAGS"]]]

class DescribeTaskDefinitionRequestTypeDef(TypedDict):
    taskDefinition: str
    include: NotRequired[Sequence[Literal["TAGS"]]]

class DescribeTaskSetsRequestTypeDef(TypedDict):
    cluster: str
    service: str
    taskSets: NotRequired[Sequence[str]]
    include: NotRequired[Sequence[Literal["TAGS"]]]

class DescribeTasksRequestTypeDef(TypedDict):
    tasks: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[Literal["TAGS"]]]

class DeviceTypeDef(TypedDict):
    hostPath: str
    containerPath: NotRequired[str]
    permissions: NotRequired[Sequence[DeviceCgroupPermissionType]]

class DiscoverPollEndpointRequestTypeDef(TypedDict):
    containerInstance: NotRequired[str]
    cluster: NotRequired[str]

class DockerVolumeConfigurationOutputTypeDef(TypedDict):
    scope: NotRequired[ScopeType]
    autoprovision: NotRequired[bool]
    driver: NotRequired[str]
    driverOpts: NotRequired[dict[str, str]]
    labels: NotRequired[dict[str, str]]

class DockerVolumeConfigurationTypeDef(TypedDict):
    scope: NotRequired[ScopeType]
    autoprovision: NotRequired[bool]
    driver: NotRequired[str]
    driverOpts: NotRequired[Mapping[str, str]]
    labels: NotRequired[Mapping[str, str]]

class ExpressGatewayServiceStatusTypeDef(TypedDict):
    statusCode: NotRequired[ExpressGatewayServiceStatusCodeType]
    statusReason: NotRequired[str]

class ManagedLogGroupTypeDef(TypedDict):
    status: ManagedResourceStatusType
    updatedAt: datetime
    logGroupName: str
    arn: NotRequired[str]
    statusReason: NotRequired[str]

class ManagedMetricAlarmTypeDef(TypedDict):
    status: ManagedResourceStatusType
    updatedAt: datetime
    arn: NotRequired[str]
    statusReason: NotRequired[str]

class ManagedSecurityGroupTypeDef(TypedDict):
    status: ManagedResourceStatusType
    updatedAt: datetime
    arn: NotRequired[str]
    statusReason: NotRequired[str]

class EFSAuthorizationConfigTypeDef(TypedDict):
    accessPointId: NotRequired[str]
    iam: NotRequired[EFSAuthorizationConfigIAMType]

class EphemeralStorageTypeDef(TypedDict):
    sizeInGiB: int

class ExecuteCommandLogConfigurationTypeDef(TypedDict):
    cloudWatchLogGroupName: NotRequired[str]
    cloudWatchEncryptionEnabled: NotRequired[bool]
    s3BucketName: NotRequired[str]
    s3EncryptionEnabled: NotRequired[bool]
    s3KeyPrefix: NotRequired[str]

class ExecuteCommandRequestTypeDef(TypedDict):
    command: str
    interactive: bool
    task: str
    cluster: NotRequired[str]
    container: NotRequired[str]

class SessionTypeDef(TypedDict):
    sessionId: NotRequired[str]
    streamUrl: NotRequired[str]
    tokenValue: NotRequired[str]

class ExpressGatewayRepositoryCredentialsTypeDef(TypedDict):
    credentialsParameter: NotRequired[str]

class ExpressGatewayServiceAwsLogsConfigurationTypeDef(TypedDict):
    logGroup: str
    logStreamPrefix: str

class ExpressGatewayServiceNetworkConfigurationOutputTypeDef(TypedDict):
    securityGroups: NotRequired[list[str]]
    subnets: NotRequired[list[str]]

class IngressPathSummaryTypeDef(TypedDict):
    accessType: AccessTypeType
    endpoint: str

class ExpressGatewayServiceNetworkConfigurationTypeDef(TypedDict):
    securityGroups: NotRequired[Sequence[str]]
    subnets: NotRequired[Sequence[str]]

class FSxWindowsFileServerAuthorizationConfigTypeDef(TypedDict):
    credentialsParameter: str
    domain: str

FirelensConfigurationTypeDef = TypedDict(
    "FirelensConfigurationTypeDef",
    {
        "type": FirelensConfigurationTypeType,
        "options": NotRequired[Mapping[str, str]],
    },
)

class GetTaskProtectionRequestTypeDef(TypedDict):
    cluster: str
    tasks: NotRequired[Sequence[str]]

class ProtectedTaskTypeDef(TypedDict):
    taskArn: NotRequired[str]
    protectionEnabled: NotRequired[bool]
    expirationDate: NotRequired[datetime]

class HealthCheckTypeDef(TypedDict):
    command: Sequence[str]
    interval: NotRequired[int]
    timeout: NotRequired[int]
    retries: NotRequired[int]
    startPeriod: NotRequired[int]

class InferenceAcceleratorOverrideTypeDef(TypedDict):
    deviceName: NotRequired[str]
    deviceType: NotRequired[str]

class InferenceAcceleratorTypeDef(TypedDict):
    deviceName: str
    deviceType: str

class ManagedInstancesLocalStorageConfigurationTypeDef(TypedDict):
    useLocalStorage: NotRequired[bool]

class ManagedInstancesNetworkConfigurationOutputTypeDef(TypedDict):
    subnets: NotRequired[list[str]]
    securityGroups: NotRequired[list[str]]

class ManagedInstancesStorageConfigurationTypeDef(TypedDict):
    storageSizeGiB: NotRequired[int]

MemoryGiBPerVCpuRequestTypeDef = TypedDict(
    "MemoryGiBPerVCpuRequestTypeDef",
    {
        "min": NotRequired[float],
        "max": NotRequired[float],
    },
)
MemoryMiBRequestTypeDef = TypedDict(
    "MemoryMiBRequestTypeDef",
    {
        "min": int,
        "max": NotRequired[int],
    },
)
NetworkBandwidthGbpsRequestTypeDef = TypedDict(
    "NetworkBandwidthGbpsRequestTypeDef",
    {
        "min": NotRequired[float],
        "max": NotRequired[float],
    },
)
NetworkInterfaceCountRequestTypeDef = TypedDict(
    "NetworkInterfaceCountRequestTypeDef",
    {
        "min": NotRequired[int],
        "max": NotRequired[int],
    },
)
TotalLocalStorageGBRequestTypeDef = TypedDict(
    "TotalLocalStorageGBRequestTypeDef",
    {
        "min": NotRequired[float],
        "max": NotRequired[float],
    },
)
VCpuCountRangeRequestTypeDef = TypedDict(
    "VCpuCountRangeRequestTypeDef",
    {
        "min": int,
        "max": NotRequired[int],
    },
)

class KernelCapabilitiesTypeDef(TypedDict):
    add: NotRequired[Sequence[str]]
    drop: NotRequired[Sequence[str]]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAccountSettingsRequestTypeDef(TypedDict):
    name: NotRequired[SettingNameType]
    value: NotRequired[str]
    principalArn: NotRequired[str]
    effectiveSettings: NotRequired[bool]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListAttributesRequestTypeDef(TypedDict):
    targetType: Literal["container-instance"]
    cluster: NotRequired[str]
    attributeName: NotRequired[str]
    attributeValue: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListClustersRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

ListContainerInstancesRequestTypeDef = TypedDict(
    "ListContainerInstancesRequestTypeDef",
    {
        "cluster": NotRequired[str],
        "filter": NotRequired[str],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "status": NotRequired[ContainerInstanceStatusType],
    },
)

class ListDaemonTaskDefinitionsRequestTypeDef(TypedDict):
    familyPrefix: NotRequired[str]
    family: NotRequired[str]
    revision: NotRequired[Literal["LAST_REGISTERED"]]
    status: NotRequired[DaemonTaskDefinitionStatusFilterType]
    sort: NotRequired[SortOrderType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDaemonsRequestTypeDef(TypedDict):
    clusterArn: NotRequired[str]
    capacityProviderArns: NotRequired[Sequence[str]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ServiceDeploymentBriefTypeDef(TypedDict):
    serviceDeploymentArn: NotRequired[str]
    serviceArn: NotRequired[str]
    clusterArn: NotRequired[str]
    startedAt: NotRequired[datetime]
    createdAt: NotRequired[datetime]
    finishedAt: NotRequired[datetime]
    targetServiceRevisionArn: NotRequired[str]
    status: NotRequired[ServiceDeploymentStatusType]
    statusReason: NotRequired[str]

class ListServicesByNamespaceRequestTypeDef(TypedDict):
    namespace: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListServicesRequestTypeDef(TypedDict):
    cluster: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    launchType: NotRequired[LaunchTypeType]
    schedulingStrategy: NotRequired[SchedulingStrategyType]
    resourceManagementType: NotRequired[ResourceManagementTypeType]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class ListTaskDefinitionFamiliesRequestTypeDef(TypedDict):
    familyPrefix: NotRequired[str]
    status: NotRequired[TaskDefinitionFamilyStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTaskDefinitionsRequestTypeDef(TypedDict):
    familyPrefix: NotRequired[str]
    status: NotRequired[TaskDefinitionStatusType]
    sort: NotRequired[SortOrderType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTasksRequestTypeDef(TypedDict):
    cluster: NotRequired[str]
    containerInstance: NotRequired[str]
    family: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    startedBy: NotRequired[str]
    serviceName: NotRequired[str]
    desiredStatus: NotRequired[DesiredStatusType]
    launchType: NotRequired[LaunchTypeType]
    daemonName: NotRequired[str]

class ManagedAgentStateChangeTypeDef(TypedDict):
    containerName: str
    managedAgentName: Literal["ExecuteCommandAgent"]
    status: str
    reason: NotRequired[str]

class ManagedApplicationAutoScalingPolicyTypeDef(TypedDict):
    status: ManagedResourceStatusType
    updatedAt: datetime
    policyType: str
    targetValue: float
    metric: str
    arn: NotRequired[str]
    statusReason: NotRequired[str]

class ManagedScalableTargetTypeDef(TypedDict):
    status: ManagedResourceStatusType
    updatedAt: datetime
    minCapacity: int
    maxCapacity: int
    arn: NotRequired[str]
    statusReason: NotRequired[str]

class ManagedCertificateTypeDef(TypedDict):
    status: ManagedResourceStatusType
    updatedAt: datetime
    domainName: str
    arn: NotRequired[str]
    statusReason: NotRequired[str]

class ManagedListenerRuleTypeDef(TypedDict):
    status: ManagedResourceStatusType
    updatedAt: datetime
    arn: NotRequired[str]
    statusReason: NotRequired[str]

class ManagedListenerTypeDef(TypedDict):
    status: ManagedResourceStatusType
    updatedAt: datetime
    arn: NotRequired[str]
    statusReason: NotRequired[str]

class ManagedLoadBalancerTypeDef(TypedDict):
    status: ManagedResourceStatusType
    updatedAt: datetime
    scheme: str
    arn: NotRequired[str]
    statusReason: NotRequired[str]
    subnetIds: NotRequired[list[str]]
    securityGroupIds: NotRequired[list[str]]

class ManagedTargetGroupTypeDef(TypedDict):
    status: ManagedResourceStatusType
    updatedAt: datetime
    healthCheckPath: str
    healthCheckPort: int
    port: int
    arn: NotRequired[str]
    statusReason: NotRequired[str]

class ManagedInstancesNetworkConfigurationTypeDef(TypedDict):
    subnets: NotRequired[Sequence[str]]
    securityGroups: NotRequired[Sequence[str]]

class MetricConfigurationOutputTypeDef(TypedDict):
    metricNames: list[str]
    resolutionSeconds: int

class MetricConfigurationTypeDef(TypedDict):
    metricNames: Sequence[str]
    resolutionSeconds: int

PlatformDeviceTypeDef = TypedDict(
    "PlatformDeviceTypeDef",
    {
        "id": str,
        "type": PlatformDeviceTypeType,
    },
)

class PutAccountSettingDefaultRequestTypeDef(TypedDict):
    name: SettingNameType
    value: str

class PutAccountSettingRequestTypeDef(TypedDict):
    name: SettingNameType
    value: str
    principalArn: NotRequired[str]

class RuntimePlatformTypeDef(TypedDict):
    cpuArchitecture: NotRequired[CPUArchitectureType]
    operatingSystemFamily: NotRequired[OSFamilyType]

TaskDefinitionPlacementConstraintTypeDef = TypedDict(
    "TaskDefinitionPlacementConstraintTypeDef",
    {
        "type": NotRequired[Literal["memberOf"]],
        "expression": NotRequired[str],
    },
)

class ServiceRevisionLoadBalancerTypeDef(TypedDict):
    targetGroupArn: NotRequired[str]
    productionListenerRule: NotRequired[str]

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "doubleValue": NotRequired[float],
        "longValue": NotRequired[int],
        "integerValue": NotRequired[int],
        "stringSetValue": NotRequired[Sequence[str]],
    },
)

class RollbackTypeDef(TypedDict):
    reason: NotRequired[str]
    startedAt: NotRequired[datetime]
    serviceRevisionArn: NotRequired[str]

class RuntimePlatformOverrideTypeDef(TypedDict):
    cpuArchitecture: NotRequired[str]

class S3FilesVolumeConfigurationTypeDef(TypedDict):
    fileSystemArn: str
    rootDirectory: NotRequired[str]
    transitEncryptionPort: NotRequired[int]
    accessPointArn: NotRequired[str]

ServiceConnectAccessLogConfigurationTypeDef = TypedDict(
    "ServiceConnectAccessLogConfigurationTypeDef",
    {
        "format": ServiceConnectAccessLoggingFormatType,
        "includeQueryParameters": NotRequired[ServiceConnectIncludeQueryParametersType],
    },
)

class TimeoutConfigurationTypeDef(TypedDict):
    idleTimeoutSeconds: NotRequired[int]
    perRequestTimeoutSeconds: NotRequired[int]

class ServiceConnectTestTrafficHeaderMatchRulesTypeDef(TypedDict):
    exact: str

class ServiceConnectTlsCertificateAuthorityTypeDef(TypedDict):
    awsPcaAuthorityArn: NotRequired[str]

class ServiceCurrentRevisionSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    requestedTaskCount: NotRequired[int]
    runningTaskCount: NotRequired[int]
    pendingTaskCount: NotRequired[int]

class ServiceDeploymentAlarmsTypeDef(TypedDict):
    status: NotRequired[ServiceDeploymentRollbackMonitorsStatusType]
    alarmNames: NotRequired[list[str]]
    triggeredAlarmNames: NotRequired[list[str]]

class ServiceDeploymentCircuitBreakerTypeDef(TypedDict):
    status: NotRequired[ServiceDeploymentRollbackMonitorsStatusType]
    failureCount: NotRequired[int]
    threshold: NotRequired[int]

class ServiceRevisionSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    requestedTaskCount: NotRequired[int]
    runningTaskCount: NotRequired[int]
    pendingTaskCount: NotRequired[int]
    requestedTestTrafficWeight: NotRequired[float]
    requestedProductionTrafficWeight: NotRequired[float]

ServiceEventTypeDef = TypedDict(
    "ServiceEventTypeDef",
    {
        "id": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "message": NotRequired[str],
    },
)

class StopServiceDeploymentRequestTypeDef(TypedDict):
    serviceDeploymentArn: str
    stopType: NotRequired[StopServiceDeploymentStopTypeType]

class StopTaskRequestTypeDef(TypedDict):
    task: str
    cluster: NotRequired[str]
    reason: NotRequired[str]

class TaskEphemeralStorageTypeDef(TypedDict):
    sizeInGiB: NotRequired[int]
    kmsKeyId: NotRequired[str]

class TaskManagedEBSVolumeTerminationPolicyTypeDef(TypedDict):
    deleteOnTermination: bool

class TmpfsTypeDef(TypedDict):
    containerPath: str
    size: int
    mountOptions: NotRequired[Sequence[str]]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateContainerAgentRequestTypeDef(TypedDict):
    containerInstance: str
    cluster: NotRequired[str]

class UpdateContainerInstancesStateRequestTypeDef(TypedDict):
    containerInstances: Sequence[str]
    status: ContainerInstanceStatusType
    cluster: NotRequired[str]

class UpdateServicePrimaryTaskSetRequestTypeDef(TypedDict):
    cluster: str
    service: str
    primaryTaskSet: str

class UpdateTaskProtectionRequestTypeDef(TypedDict):
    cluster: str
    tasks: Sequence[str]
    protectionEnabled: bool
    expiresInMinutes: NotRequired[int]

class LoadBalancerTypeDef(TypedDict):
    targetGroupArn: NotRequired[str]
    loadBalancerName: NotRequired[str]
    containerName: NotRequired[str]
    containerPort: NotRequired[int]
    advancedConfiguration: NotRequired[AdvancedConfigurationTypeDef]

class SubmitAttachmentStateChangesRequestTypeDef(TypedDict):
    attachments: Sequence[AttachmentStateChangeTypeDef]
    cluster: NotRequired[str]

AttachmentTypeDef = TypedDict(
    "AttachmentTypeDef",
    {
        "id": NotRequired[str],
        "type": NotRequired[str],
        "status": NotRequired[str],
        "details": NotRequired[list[KeyValuePairTypeDef]],
    },
)
ProxyConfigurationOutputTypeDef = TypedDict(
    "ProxyConfigurationOutputTypeDef",
    {
        "containerName": str,
        "type": NotRequired[Literal["APPMESH"]],
        "properties": NotRequired[list[KeyValuePairTypeDef]],
    },
)
ProxyConfigurationTypeDef = TypedDict(
    "ProxyConfigurationTypeDef",
    {
        "containerName": str,
        "type": NotRequired[Literal["APPMESH"]],
        "properties": NotRequired[Sequence[KeyValuePairTypeDef]],
    },
)

class DeleteAttributesRequestTypeDef(TypedDict):
    attributes: Sequence[AttributeTypeDef]
    cluster: NotRequired[str]

class PutAttributesRequestTypeDef(TypedDict):
    attributes: Sequence[AttributeTypeDef]
    cluster: NotRequired[str]

class AutoScalingGroupProviderTypeDef(TypedDict):
    autoScalingGroupArn: str
    managedScaling: NotRequired[ManagedScalingTypeDef]
    managedTerminationProtection: NotRequired[ManagedTerminationProtectionType]
    managedDraining: NotRequired[ManagedDrainingType]

class AutoScalingGroupProviderUpdateTypeDef(TypedDict):
    managedScaling: NotRequired[ManagedScalingTypeDef]
    managedTerminationProtection: NotRequired[ManagedTerminationProtectionType]
    managedDraining: NotRequired[ManagedDrainingType]

class NetworkConfigurationOutputTypeDef(TypedDict):
    awsvpcConfiguration: NotRequired[AwsVpcConfigurationOutputTypeDef]

class NetworkConfigurationTypeDef(TypedDict):
    awsvpcConfiguration: NotRequired[AwsVpcConfigurationTypeDef]

class PutClusterCapacityProvidersRequestTypeDef(TypedDict):
    cluster: str
    capacityProviders: Sequence[str]
    defaultCapacityProviderStrategy: Sequence[CapacityProviderStrategyItemTypeDef]

class EBSTagSpecificationOutputTypeDef(TypedDict):
    resourceType: Literal["volume"]
    tags: NotRequired[list[TagTypeDef]]
    propagateTags: NotRequired[PropagateTagsType]

class EBSTagSpecificationTypeDef(TypedDict):
    resourceType: Literal["volume"]
    tags: NotRequired[Sequence[TagTypeDef]]
    propagateTags: NotRequired[PropagateTagsType]

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]

class UpdateClusterSettingsRequestTypeDef(TypedDict):
    cluster: str
    settings: Sequence[ClusterSettingTypeDef]

class ContainerOverrideOutputTypeDef(TypedDict):
    name: NotRequired[str]
    command: NotRequired[list[str]]
    environment: NotRequired[list[KeyValuePairTypeDef]]
    environmentFiles: NotRequired[list[EnvironmentFileTypeDef]]
    cpu: NotRequired[int]
    memory: NotRequired[int]
    memoryReservation: NotRequired[int]
    resourceRequirements: NotRequired[list[ResourceRequirementTypeDef]]

class ContainerOverrideTypeDef(TypedDict):
    name: NotRequired[str]
    command: NotRequired[Sequence[str]]
    environment: NotRequired[Sequence[KeyValuePairTypeDef]]
    environmentFiles: NotRequired[Sequence[EnvironmentFileTypeDef]]
    cpu: NotRequired[int]
    memory: NotRequired[int]
    memoryReservation: NotRequired[int]
    resourceRequirements: NotRequired[Sequence[ResourceRequirementTypeDef]]

class LogConfigurationOutputTypeDef(TypedDict):
    logDriver: LogDriverType
    options: NotRequired[dict[str, str]]
    secretOptions: NotRequired[list[SecretTypeDef]]

class LogConfigurationTypeDef(TypedDict):
    logDriver: LogDriverType
    options: NotRequired[Mapping[str, str]]
    secretOptions: NotRequired[Sequence[SecretTypeDef]]

class ContainerInstanceHealthStatusTypeDef(TypedDict):
    overallStatus: NotRequired[InstanceHealthCheckStateType]
    details: NotRequired[list[InstanceHealthCheckResultTypeDef]]

ContainerRestartPolicyUnionTypeDef = Union[
    ContainerRestartPolicyTypeDef, ContainerRestartPolicyOutputTypeDef
]

class ContainerStateChangeTypeDef(TypedDict):
    containerName: NotRequired[str]
    imageDigest: NotRequired[str]
    runtimeId: NotRequired[str]
    exitCode: NotRequired[int]
    networkBindings: NotRequired[Sequence[NetworkBindingTypeDef]]
    reason: NotRequired[str]
    status: NotRequired[str]

class SubmitContainerStateChangeRequestTypeDef(TypedDict):
    cluster: NotRequired[str]
    task: NotRequired[str]
    containerName: NotRequired[str]
    runtimeId: NotRequired[str]
    status: NotRequired[str]
    exitCode: NotRequired[int]
    reason: NotRequired[str]
    networkBindings: NotRequired[Sequence[NetworkBindingTypeDef]]

class ContainerTypeDef(TypedDict):
    containerArn: NotRequired[str]
    taskArn: NotRequired[str]
    name: NotRequired[str]
    image: NotRequired[str]
    imageDigest: NotRequired[str]
    runtimeId: NotRequired[str]
    lastStatus: NotRequired[str]
    exitCode: NotRequired[int]
    reason: NotRequired[str]
    networkBindings: NotRequired[list[NetworkBindingTypeDef]]
    networkInterfaces: NotRequired[list[NetworkInterfaceTypeDef]]
    healthStatus: NotRequired[HealthStatusType]
    managedAgents: NotRequired[list[ManagedAgentTypeDef]]
    cpu: NotRequired[str]
    memory: NotRequired[str]
    memoryReservation: NotRequired[str]
    gpuIds: NotRequired[list[str]]
    neuronDeviceIds: NotRequired[list[str]]

class ContinueServiceDeploymentResponseTypeDef(TypedDict):
    serviceDeploymentArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDaemonResponseTypeDef(TypedDict):
    daemonArn: str
    status: DaemonStatusType
    createdAt: datetime
    deploymentArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAttributesResponseTypeDef(TypedDict):
    attributes: list[AttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDaemonResponseTypeDef(TypedDict):
    daemonArn: str
    status: DaemonStatusType
    createdAt: datetime
    updatedAt: datetime
    deploymentArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDaemonTaskDefinitionResponseTypeDef(TypedDict):
    daemonTaskDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DiscoverPollEndpointResponseTypeDef(TypedDict):
    endpoint: str
    telemetryEndpoint: str
    serviceConnectEndpoint: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAttributesResponseTypeDef(TypedDict):
    attributes: list[AttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListClustersResponseTypeDef(TypedDict):
    clusterArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListContainerInstancesResponseTypeDef(TypedDict):
    containerInstanceArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServicesByNamespaceResponseTypeDef(TypedDict):
    serviceArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListServicesResponseTypeDef(TypedDict):
    serviceArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTaskDefinitionFamiliesResponseTypeDef(TypedDict):
    families: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTaskDefinitionsResponseTypeDef(TypedDict):
    taskDefinitionArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTasksResponseTypeDef(TypedDict):
    taskArns: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PutAttributesResponseTypeDef(TypedDict):
    attributes: list[AttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterDaemonTaskDefinitionResponseTypeDef(TypedDict):
    daemonTaskDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopServiceDeploymentResponseTypeDef(TypedDict):
    serviceDeploymentArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class SubmitAttachmentStateChangesResponseTypeDef(TypedDict):
    acknowledgment: str
    ResponseMetadata: ResponseMetadataTypeDef

class SubmitContainerStateChangeResponseTypeDef(TypedDict):
    acknowledgment: str
    ResponseMetadata: ResponseMetadataTypeDef

class SubmitTaskStateChangeResponseTypeDef(TypedDict):
    acknowledgment: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDaemonResponseTypeDef(TypedDict):
    daemonArn: str
    status: DaemonStatusType
    createdAt: datetime
    updatedAt: datetime
    deploymentArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTaskSetRequestTypeDef(TypedDict):
    cluster: str
    service: str
    taskSet: str
    scale: ScaleTypeDef

class CreatedAtTypeDef(TypedDict):
    before: NotRequired[TimestampTypeDef]
    after: NotRequired[TimestampTypeDef]

class DaemonDeploymentConfigurationOutputTypeDef(TypedDict):
    drainPercent: NotRequired[float]
    alarms: NotRequired[DaemonAlarmConfigurationOutputTypeDef]
    bakeTimeInMinutes: NotRequired[int]

class DaemonDeploymentConfigurationTypeDef(TypedDict):
    drainPercent: NotRequired[float]
    alarms: NotRequired[DaemonAlarmConfigurationTypeDef]
    bakeTimeInMinutes: NotRequired[int]

class DaemonRevisionDetailTypeDef(TypedDict):
    arn: NotRequired[str]
    capacityProviders: NotRequired[list[DaemonCapacityProviderTypeDef]]
    totalRunningCount: NotRequired[int]
    totalWithoutDaemonCount: NotRequired[int]

class DaemonRevisionTypeDef(TypedDict):
    daemonRevisionArn: NotRequired[str]
    clusterArn: NotRequired[str]
    daemonArn: NotRequired[str]
    daemonTaskDefinitionArn: NotRequired[str]
    createdAt: NotRequired[datetime]
    containerImages: NotRequired[list[DaemonContainerImageTypeDef]]
    propagateTags: NotRequired[DaemonPropagateTagsType]
    enableECSManagedTags: NotRequired[bool]
    enableExecuteCommand: NotRequired[bool]
    critical: NotRequired[bool]

class DaemonDeploymentRevisionDetailTypeDef(TypedDict):
    arn: NotRequired[str]
    capacityProviders: NotRequired[list[DaemonDeploymentCapacityProviderTypeDef]]
    totalRunningInstanceCount: NotRequired[int]
    totalWithoutDaemonInstanceCount: NotRequired[int]
    totalDrainingInstanceCount: NotRequired[int]

class ListDaemonDeploymentsResponseTypeDef(TypedDict):
    daemonDeployments: list[DaemonDeploymentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DaemonLinuxParametersOutputTypeDef(TypedDict):
    capabilities: NotRequired[KernelCapabilitiesOutputTypeDef]
    devices: NotRequired[list[DeviceOutputTypeDef]]
    initProcessEnabled: NotRequired[bool]
    tmpfs: NotRequired[list[TmpfsOutputTypeDef]]

class LinuxParametersOutputTypeDef(TypedDict):
    capabilities: NotRequired[KernelCapabilitiesOutputTypeDef]
    devices: NotRequired[list[DeviceOutputTypeDef]]
    initProcessEnabled: NotRequired[bool]
    sharedMemorySize: NotRequired[int]
    tmpfs: NotRequired[list[TmpfsOutputTypeDef]]
    maxSwap: NotRequired[int]
    swappiness: NotRequired[int]

class ListDaemonsResponseTypeDef(TypedDict):
    daemonSummariesList: list[DaemonSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDaemonTaskDefinitionsResponseTypeDef(TypedDict):
    daemonTaskDefinitions: list[DaemonTaskDefinitionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DaemonVolumeTypeDef(TypedDict):
    name: NotRequired[str]
    host: NotRequired[HostVolumePropertiesTypeDef]

class DeleteAccountSettingResponseTypeDef(TypedDict):
    setting: SettingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAccountSettingsResponseTypeDef(TypedDict):
    settings: list[SettingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PutAccountSettingDefaultResponseTypeDef(TypedDict):
    setting: SettingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutAccountSettingResponseTypeDef(TypedDict):
    setting: SettingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeploymentCircuitBreakerTypeDef(TypedDict):
    enable: bool
    rollback: bool
    resetOnHealthyTask: NotRequired[bool]
    thresholdConfiguration: NotRequired[ThresholdConfigurationTypeDef]

class DeploymentLifecycleHookOutputTypeDef(TypedDict):
    targetType: NotRequired[DeploymentLifecycleHookTargetTypeType]
    hookTargetArn: NotRequired[str]
    roleArn: NotRequired[str]
    lifecycleStages: NotRequired[list[DeploymentLifecycleHookStageType]]
    hookDetails: NotRequired[dict[str, Any]]
    timeoutConfiguration: NotRequired[DeploymentLifecycleHookTimeoutConfigurationTypeDef]

class DeploymentLifecycleHookTypeDef(TypedDict):
    targetType: NotRequired[DeploymentLifecycleHookTargetTypeType]
    hookTargetArn: NotRequired[str]
    roleArn: NotRequired[str]
    lifecycleStages: NotRequired[Sequence[DeploymentLifecycleHookStageType]]
    hookDetails: NotRequired[Mapping[str, Any]]
    timeoutConfiguration: NotRequired[DeploymentLifecycleHookTimeoutConfigurationTypeDef]

class DescribeDaemonDeploymentsRequestWaitExtraTypeDef(TypedDict):
    daemonDeploymentArns: Sequence[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeDaemonDeploymentsRequestWaitTypeDef(TypedDict):
    daemonDeploymentArns: Sequence[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeDaemonRequestWaitTypeDef(TypedDict):
    daemonArn: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeDaemonTaskDefinitionRequestWaitExtraTypeDef(TypedDict):
    daemonTaskDefinition: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeDaemonTaskDefinitionRequestWaitTypeDef(TypedDict):
    daemonTaskDefinition: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeServicesRequestWaitExtraTypeDef(TypedDict):
    services: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[Literal["TAGS"]]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeServicesRequestWaitTypeDef(TypedDict):
    services: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[Literal["TAGS"]]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeTasksRequestWaitExtraTypeDef(TypedDict):
    tasks: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[Literal["TAGS"]]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeTasksRequestWaitTypeDef(TypedDict):
    tasks: Sequence[str]
    cluster: NotRequired[str]
    include: NotRequired[Sequence[Literal["TAGS"]]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

DeviceUnionTypeDef = Union[DeviceTypeDef, DeviceOutputTypeDef]
DockerVolumeConfigurationUnionTypeDef = Union[
    DockerVolumeConfigurationTypeDef, DockerVolumeConfigurationOutputTypeDef
]

class EFSVolumeConfigurationTypeDef(TypedDict):
    fileSystemId: str
    rootDirectory: NotRequired[str]
    transitEncryption: NotRequired[EFSTransitEncryptionType]
    transitEncryptionPort: NotRequired[int]
    authorizationConfig: NotRequired[EFSAuthorizationConfigTypeDef]

class ExecuteCommandConfigurationTypeDef(TypedDict):
    kmsKeyId: NotRequired[str]
    logging: NotRequired[ExecuteCommandLoggingType]
    logConfiguration: NotRequired[ExecuteCommandLogConfigurationTypeDef]

class ExecuteCommandResponseTypeDef(TypedDict):
    clusterArn: str
    containerArn: str
    containerName: str
    interactive: bool
    session: SessionTypeDef
    taskArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ExpressGatewayContainerOutputTypeDef(TypedDict):
    image: str
    containerPort: NotRequired[int]
    awsLogsConfiguration: NotRequired[ExpressGatewayServiceAwsLogsConfigurationTypeDef]
    repositoryCredentials: NotRequired[ExpressGatewayRepositoryCredentialsTypeDef]
    command: NotRequired[list[str]]
    environment: NotRequired[list[KeyValuePairTypeDef]]
    secrets: NotRequired[list[SecretTypeDef]]

class ExpressGatewayContainerTypeDef(TypedDict):
    image: str
    containerPort: NotRequired[int]
    awsLogsConfiguration: NotRequired[ExpressGatewayServiceAwsLogsConfigurationTypeDef]
    repositoryCredentials: NotRequired[ExpressGatewayRepositoryCredentialsTypeDef]
    command: NotRequired[Sequence[str]]
    environment: NotRequired[Sequence[KeyValuePairTypeDef]]
    secrets: NotRequired[Sequence[SecretTypeDef]]

ExpressGatewayServiceNetworkConfigurationUnionTypeDef = Union[
    ExpressGatewayServiceNetworkConfigurationTypeDef,
    ExpressGatewayServiceNetworkConfigurationOutputTypeDef,
]

class FSxWindowsFileServerVolumeConfigurationTypeDef(TypedDict):
    fileSystemId: str
    rootDirectory: str
    authorizationConfig: FSxWindowsFileServerAuthorizationConfigTypeDef

FirelensConfigurationUnionTypeDef = Union[
    FirelensConfigurationTypeDef, FirelensConfigurationOutputTypeDef
]

class GetTaskProtectionResponseTypeDef(TypedDict):
    protectedTasks: list[ProtectedTaskTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTaskProtectionResponseTypeDef(TypedDict):
    protectedTasks: list[ProtectedTaskTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

HealthCheckUnionTypeDef = Union[HealthCheckTypeDef, HealthCheckOutputTypeDef]

class InstanceRequirementsRequestOutputTypeDef(TypedDict):
    vCpuCount: VCpuCountRangeRequestTypeDef
    memoryMiB: MemoryMiBRequestTypeDef
    cpuManufacturers: NotRequired[list[CpuManufacturerType]]
    memoryGiBPerVCpu: NotRequired[MemoryGiBPerVCpuRequestTypeDef]
    excludedInstanceTypes: NotRequired[list[str]]
    instanceGenerations: NotRequired[list[InstanceGenerationType]]
    spotMaxPricePercentageOverLowestPrice: NotRequired[int]
    onDemandMaxPricePercentageOverLowestPrice: NotRequired[int]
    bareMetal: NotRequired[BareMetalType]
    burstablePerformance: NotRequired[BurstablePerformanceType]
    requireHibernateSupport: NotRequired[bool]
    networkInterfaceCount: NotRequired[NetworkInterfaceCountRequestTypeDef]
    localStorage: NotRequired[LocalStorageType]
    localStorageTypes: NotRequired[list[LocalStorageTypeType]]
    totalLocalStorageGB: NotRequired[TotalLocalStorageGBRequestTypeDef]
    baselineEbsBandwidthMbps: NotRequired[BaselineEbsBandwidthMbpsRequestTypeDef]
    acceleratorTypes: NotRequired[list[AcceleratorTypeType]]
    acceleratorCount: NotRequired[AcceleratorCountRequestTypeDef]
    acceleratorManufacturers: NotRequired[list[AcceleratorManufacturerType]]
    acceleratorNames: NotRequired[list[AcceleratorNameType]]
    acceleratorTotalMemoryMiB: NotRequired[AcceleratorTotalMemoryMiBRequestTypeDef]
    networkBandwidthGbps: NotRequired[NetworkBandwidthGbpsRequestTypeDef]
    allowedInstanceTypes: NotRequired[list[str]]
    maxSpotPriceAsPercentageOfOptimalOnDemandPrice: NotRequired[int]

class InstanceRequirementsRequestTypeDef(TypedDict):
    vCpuCount: VCpuCountRangeRequestTypeDef
    memoryMiB: MemoryMiBRequestTypeDef
    cpuManufacturers: NotRequired[Sequence[CpuManufacturerType]]
    memoryGiBPerVCpu: NotRequired[MemoryGiBPerVCpuRequestTypeDef]
    excludedInstanceTypes: NotRequired[Sequence[str]]
    instanceGenerations: NotRequired[Sequence[InstanceGenerationType]]
    spotMaxPricePercentageOverLowestPrice: NotRequired[int]
    onDemandMaxPricePercentageOverLowestPrice: NotRequired[int]
    bareMetal: NotRequired[BareMetalType]
    burstablePerformance: NotRequired[BurstablePerformanceType]
    requireHibernateSupport: NotRequired[bool]
    networkInterfaceCount: NotRequired[NetworkInterfaceCountRequestTypeDef]
    localStorage: NotRequired[LocalStorageType]
    localStorageTypes: NotRequired[Sequence[LocalStorageTypeType]]
    totalLocalStorageGB: NotRequired[TotalLocalStorageGBRequestTypeDef]
    baselineEbsBandwidthMbps: NotRequired[BaselineEbsBandwidthMbpsRequestTypeDef]
    acceleratorTypes: NotRequired[Sequence[AcceleratorTypeType]]
    acceleratorCount: NotRequired[AcceleratorCountRequestTypeDef]
    acceleratorManufacturers: NotRequired[Sequence[AcceleratorManufacturerType]]
    acceleratorNames: NotRequired[Sequence[AcceleratorNameType]]
    acceleratorTotalMemoryMiB: NotRequired[AcceleratorTotalMemoryMiBRequestTypeDef]
    networkBandwidthGbps: NotRequired[NetworkBandwidthGbpsRequestTypeDef]
    allowedInstanceTypes: NotRequired[Sequence[str]]
    maxSpotPriceAsPercentageOfOptimalOnDemandPrice: NotRequired[int]

KernelCapabilitiesUnionTypeDef = Union[KernelCapabilitiesTypeDef, KernelCapabilitiesOutputTypeDef]

class ListAccountSettingsRequestPaginateTypeDef(TypedDict):
    name: NotRequired[SettingNameType]
    value: NotRequired[str]
    principalArn: NotRequired[str]
    effectiveSettings: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAttributesRequestPaginateTypeDef(TypedDict):
    targetType: Literal["container-instance"]
    cluster: NotRequired[str]
    attributeName: NotRequired[str]
    attributeValue: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClustersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListContainerInstancesRequestPaginateTypeDef = TypedDict(
    "ListContainerInstancesRequestPaginateTypeDef",
    {
        "cluster": NotRequired[str],
        "filter": NotRequired[str],
        "status": NotRequired[ContainerInstanceStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListServicesByNamespaceRequestPaginateTypeDef(TypedDict):
    namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServicesRequestPaginateTypeDef(TypedDict):
    cluster: NotRequired[str]
    launchType: NotRequired[LaunchTypeType]
    schedulingStrategy: NotRequired[SchedulingStrategyType]
    resourceManagementType: NotRequired[ResourceManagementTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTaskDefinitionFamiliesRequestPaginateTypeDef(TypedDict):
    familyPrefix: NotRequired[str]
    status: NotRequired[TaskDefinitionFamilyStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTaskDefinitionsRequestPaginateTypeDef(TypedDict):
    familyPrefix: NotRequired[str]
    status: NotRequired[TaskDefinitionStatusType]
    sort: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTasksRequestPaginateTypeDef(TypedDict):
    cluster: NotRequired[str]
    containerInstance: NotRequired[str]
    family: NotRequired[str]
    startedBy: NotRequired[str]
    serviceName: NotRequired[str]
    desiredStatus: NotRequired[DesiredStatusType]
    launchType: NotRequired[LaunchTypeType]
    daemonName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListServiceDeploymentsResponseTypeDef(TypedDict):
    serviceDeployments: list[ServiceDeploymentBriefTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ManagedAutoScalingTypeDef(TypedDict):
    scalableTarget: NotRequired[ManagedScalableTargetTypeDef]
    applicationAutoScalingPolicies: NotRequired[list[ManagedApplicationAutoScalingPolicyTypeDef]]

class ManagedIngressPathTypeDef(TypedDict):
    accessType: AccessTypeType
    endpoint: str
    loadBalancer: NotRequired[ManagedLoadBalancerTypeDef]
    loadBalancerSecurityGroups: NotRequired[list[ManagedSecurityGroupTypeDef]]
    certificate: NotRequired[ManagedCertificateTypeDef]
    listener: NotRequired[ManagedListenerTypeDef]
    rule: NotRequired[ManagedListenerRuleTypeDef]
    targetGroups: NotRequired[list[ManagedTargetGroupTypeDef]]

ManagedInstancesNetworkConfigurationUnionTypeDef = Union[
    ManagedInstancesNetworkConfigurationTypeDef, ManagedInstancesNetworkConfigurationOutputTypeDef
]

class MonitoringConfigurationOutputTypeDef(TypedDict):
    metricConfigurations: NotRequired[list[MetricConfigurationOutputTypeDef]]

class MonitoringConfigurationTypeDef(TypedDict):
    metricConfigurations: NotRequired[Sequence[MetricConfigurationTypeDef]]

class ResolvedConfigurationTypeDef(TypedDict):
    loadBalancers: NotRequired[list[ServiceRevisionLoadBalancerTypeDef]]

ResourceUnionTypeDef = Union[ResourceTypeDef, ResourceOutputTypeDef]

class ServiceRevisionOverridesTypeDef(TypedDict):
    runtimePlatform: NotRequired[RuntimePlatformOverrideTypeDef]

class ServiceConnectTestTrafficHeaderRulesTypeDef(TypedDict):
    name: str
    value: NotRequired[ServiceConnectTestTrafficHeaderMatchRulesTypeDef]

class ServiceConnectTlsConfigurationTypeDef(TypedDict):
    issuerCertificateAuthority: ServiceConnectTlsCertificateAuthorityTypeDef
    kmsKey: NotRequired[str]
    roleArn: NotRequired[str]

TmpfsUnionTypeDef = Union[TmpfsTypeDef, TmpfsOutputTypeDef]
ProxyConfigurationUnionTypeDef = Union[ProxyConfigurationTypeDef, ProxyConfigurationOutputTypeDef]
TaskSetTypeDef = TypedDict(
    "TaskSetTypeDef",
    {
        "id": NotRequired[str],
        "taskSetArn": NotRequired[str],
        "serviceArn": NotRequired[str],
        "clusterArn": NotRequired[str],
        "startedBy": NotRequired[str],
        "externalId": NotRequired[str],
        "status": NotRequired[str],
        "taskDefinition": NotRequired[str],
        "computedDesiredCount": NotRequired[int],
        "pendingCount": NotRequired[int],
        "runningCount": NotRequired[int],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "launchType": NotRequired[LaunchTypeType],
        "capacityProviderStrategy": NotRequired[list[CapacityProviderStrategyItemTypeDef]],
        "platformVersion": NotRequired[str],
        "platformFamily": NotRequired[str],
        "networkConfiguration": NotRequired[NetworkConfigurationOutputTypeDef],
        "loadBalancers": NotRequired[list[LoadBalancerTypeDef]],
        "serviceRegistries": NotRequired[list[ServiceRegistryTypeDef]],
        "scale": NotRequired[ScaleTypeDef],
        "stabilityStatus": NotRequired[StabilityStatusType],
        "stabilityStatusAt": NotRequired[datetime],
        "tags": NotRequired[list[TagTypeDef]],
        "fargateEphemeralStorage": NotRequired[DeploymentEphemeralStorageTypeDef],
    },
)
NetworkConfigurationUnionTypeDef = Union[
    NetworkConfigurationTypeDef, NetworkConfigurationOutputTypeDef
]

class ServiceManagedEBSVolumeConfigurationOutputTypeDef(TypedDict):
    roleArn: str
    encrypted: NotRequired[bool]
    kmsKeyId: NotRequired[str]
    volumeType: NotRequired[str]
    sizeInGiB: NotRequired[int]
    snapshotId: NotRequired[str]
    volumeInitializationRate: NotRequired[int]
    iops: NotRequired[int]
    throughput: NotRequired[int]
    tagSpecifications: NotRequired[list[EBSTagSpecificationOutputTypeDef]]
    filesystemType: NotRequired[TaskFilesystemTypeType]

EBSTagSpecificationUnionTypeDef = Union[
    EBSTagSpecificationTypeDef, EBSTagSpecificationOutputTypeDef
]

class TaskOverrideOutputTypeDef(TypedDict):
    containerOverrides: NotRequired[list[ContainerOverrideOutputTypeDef]]
    cpu: NotRequired[str]
    inferenceAcceleratorOverrides: NotRequired[list[InferenceAcceleratorOverrideTypeDef]]
    executionRoleArn: NotRequired[str]
    memory: NotRequired[str]
    taskRoleArn: NotRequired[str]
    ephemeralStorage: NotRequired[EphemeralStorageTypeDef]

class TaskOverrideTypeDef(TypedDict):
    containerOverrides: NotRequired[Sequence[ContainerOverrideTypeDef]]
    cpu: NotRequired[str]
    inferenceAcceleratorOverrides: NotRequired[Sequence[InferenceAcceleratorOverrideTypeDef]]
    executionRoleArn: NotRequired[str]
    memory: NotRequired[str]
    taskRoleArn: NotRequired[str]
    ephemeralStorage: NotRequired[EphemeralStorageTypeDef]

LogConfigurationUnionTypeDef = Union[LogConfigurationTypeDef, LogConfigurationOutputTypeDef]

class ContainerInstanceTypeDef(TypedDict):
    containerInstanceArn: NotRequired[str]
    ec2InstanceId: NotRequired[str]
    capacityProviderName: NotRequired[str]
    version: NotRequired[int]
    versionInfo: NotRequired[VersionInfoTypeDef]
    remainingResources: NotRequired[list[ResourceOutputTypeDef]]
    registeredResources: NotRequired[list[ResourceOutputTypeDef]]
    status: NotRequired[str]
    statusReason: NotRequired[str]
    agentConnected: NotRequired[bool]
    runningTasksCount: NotRequired[int]
    pendingTasksCount: NotRequired[int]
    agentUpdateStatus: NotRequired[AgentUpdateStatusType]
    attributes: NotRequired[list[AttributeTypeDef]]
    registeredAt: NotRequired[datetime]
    attachments: NotRequired[list[AttachmentTypeDef]]
    tags: NotRequired[list[TagTypeDef]]
    healthStatus: NotRequired[ContainerInstanceHealthStatusTypeDef]

class SubmitTaskStateChangeRequestTypeDef(TypedDict):
    cluster: NotRequired[str]
    task: NotRequired[str]
    status: NotRequired[str]
    reason: NotRequired[str]
    containers: NotRequired[Sequence[ContainerStateChangeTypeDef]]
    attachments: NotRequired[Sequence[AttachmentStateChangeTypeDef]]
    managedAgents: NotRequired[Sequence[ManagedAgentStateChangeTypeDef]]
    pullStartedAt: NotRequired[TimestampTypeDef]
    pullStoppedAt: NotRequired[TimestampTypeDef]
    executionStoppedAt: NotRequired[TimestampTypeDef]

class ListDaemonDeploymentsRequestTypeDef(TypedDict):
    daemonArn: str
    status: NotRequired[Sequence[DaemonDeploymentStatusType]]
    createdAt: NotRequired[CreatedAtTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListServiceDeploymentsRequestTypeDef(TypedDict):
    service: str
    cluster: NotRequired[str]
    status: NotRequired[Sequence[ServiceDeploymentStatusType]]
    createdAt: NotRequired[CreatedAtTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

DaemonDeploymentConfigurationUnionTypeDef = Union[
    DaemonDeploymentConfigurationTypeDef, DaemonDeploymentConfigurationOutputTypeDef
]

class DaemonDetailTypeDef(TypedDict):
    daemonArn: NotRequired[str]
    clusterArn: NotRequired[str]
    status: NotRequired[DaemonStatusType]
    currentRevisions: NotRequired[list[DaemonRevisionDetailTypeDef]]
    deploymentArn: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class DescribeDaemonRevisionsResponseTypeDef(TypedDict):
    daemonRevisions: list[DaemonRevisionTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DaemonDeploymentTypeDef(TypedDict):
    daemonDeploymentArn: NotRequired[str]
    clusterArn: NotRequired[str]
    status: NotRequired[DaemonDeploymentStatusType]
    statusReason: NotRequired[str]
    targetDaemonRevision: NotRequired[DaemonDeploymentRevisionDetailTypeDef]
    sourceDaemonRevisions: NotRequired[list[DaemonDeploymentRevisionDetailTypeDef]]
    circuitBreaker: NotRequired[DaemonCircuitBreakerTypeDef]
    alarms: NotRequired[DaemonDeploymentAlarmsTypeDef]
    rollback: NotRequired[DaemonRollbackTypeDef]
    deploymentConfiguration: NotRequired[DaemonDeploymentConfigurationOutputTypeDef]
    createdAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    stoppedAt: NotRequired[datetime]
    finishedAt: NotRequired[datetime]

class DaemonContainerDefinitionOutputTypeDef(TypedDict):
    image: str
    name: NotRequired[str]
    memory: NotRequired[int]
    memoryReservation: NotRequired[int]
    repositoryCredentials: NotRequired[RepositoryCredentialsTypeDef]
    healthCheck: NotRequired[HealthCheckOutputTypeDef]
    cpu: NotRequired[int]
    essential: NotRequired[bool]
    entryPoint: NotRequired[list[str]]
    command: NotRequired[list[str]]
    workingDirectory: NotRequired[str]
    environmentFiles: NotRequired[list[EnvironmentFileTypeDef]]
    environment: NotRequired[list[KeyValuePairTypeDef]]
    secrets: NotRequired[list[SecretTypeDef]]
    readonlyRootFilesystem: NotRequired[bool]
    mountPoints: NotRequired[list[MountPointTypeDef]]
    logConfiguration: NotRequired[LogConfigurationOutputTypeDef]
    firelensConfiguration: NotRequired[FirelensConfigurationOutputTypeDef]
    privileged: NotRequired[bool]
    user: NotRequired[str]
    ulimits: NotRequired[list[UlimitTypeDef]]
    linuxParameters: NotRequired[DaemonLinuxParametersOutputTypeDef]
    dependsOn: NotRequired[list[ContainerDependencyTypeDef]]
    startTimeout: NotRequired[int]
    stopTimeout: NotRequired[int]
    systemControls: NotRequired[list[SystemControlTypeDef]]
    interactive: NotRequired[bool]
    pseudoTerminal: NotRequired[bool]
    restartPolicy: NotRequired[ContainerRestartPolicyOutputTypeDef]

class ContainerDefinitionOutputTypeDef(TypedDict):
    name: NotRequired[str]
    image: NotRequired[str]
    repositoryCredentials: NotRequired[RepositoryCredentialsTypeDef]
    cpu: NotRequired[int]
    memory: NotRequired[int]
    memoryReservation: NotRequired[int]
    links: NotRequired[list[str]]
    portMappings: NotRequired[list[PortMappingTypeDef]]
    essential: NotRequired[bool]
    restartPolicy: NotRequired[ContainerRestartPolicyOutputTypeDef]
    entryPoint: NotRequired[list[str]]
    command: NotRequired[list[str]]
    environment: NotRequired[list[KeyValuePairTypeDef]]
    environmentFiles: NotRequired[list[EnvironmentFileTypeDef]]
    mountPoints: NotRequired[list[MountPointTypeDef]]
    volumesFrom: NotRequired[list[VolumeFromTypeDef]]
    linuxParameters: NotRequired[LinuxParametersOutputTypeDef]
    secrets: NotRequired[list[SecretTypeDef]]
    dependsOn: NotRequired[list[ContainerDependencyTypeDef]]
    startTimeout: NotRequired[int]
    stopTimeout: NotRequired[int]
    versionConsistency: NotRequired[VersionConsistencyType]
    hostname: NotRequired[str]
    user: NotRequired[str]
    workingDirectory: NotRequired[str]
    disableNetworking: NotRequired[bool]
    privileged: NotRequired[bool]
    readonlyRootFilesystem: NotRequired[bool]
    dnsServers: NotRequired[list[str]]
    dnsSearchDomains: NotRequired[list[str]]
    extraHosts: NotRequired[list[HostEntryTypeDef]]
    dockerSecurityOptions: NotRequired[list[str]]
    interactive: NotRequired[bool]
    pseudoTerminal: NotRequired[bool]
    dockerLabels: NotRequired[dict[str, str]]
    ulimits: NotRequired[list[UlimitTypeDef]]
    logConfiguration: NotRequired[LogConfigurationOutputTypeDef]
    healthCheck: NotRequired[HealthCheckOutputTypeDef]
    systemControls: NotRequired[list[SystemControlTypeDef]]
    resourceRequirements: NotRequired[list[ResourceRequirementTypeDef]]
    firelensConfiguration: NotRequired[FirelensConfigurationOutputTypeDef]
    credentialSpecs: NotRequired[list[str]]

class DeploymentConfigurationOutputTypeDef(TypedDict):
    deploymentCircuitBreaker: NotRequired[DeploymentCircuitBreakerTypeDef]
    maximumPercent: NotRequired[int]
    minimumHealthyPercent: NotRequired[int]
    alarms: NotRequired[DeploymentAlarmsOutputTypeDef]
    strategy: NotRequired[DeploymentStrategyType]
    bakeTimeInMinutes: NotRequired[int]
    lifecycleHooks: NotRequired[list[DeploymentLifecycleHookOutputTypeDef]]
    linearConfiguration: NotRequired[LinearConfigurationTypeDef]
    canaryConfiguration: NotRequired[CanaryConfigurationTypeDef]
    earlySuccessCriteria: NotRequired[DeploymentEarlySuccessCriteriaTypeDef]

class DeploymentConfigurationTypeDef(TypedDict):
    deploymentCircuitBreaker: NotRequired[DeploymentCircuitBreakerTypeDef]
    maximumPercent: NotRequired[int]
    minimumHealthyPercent: NotRequired[int]
    alarms: NotRequired[DeploymentAlarmsTypeDef]
    strategy: NotRequired[DeploymentStrategyType]
    bakeTimeInMinutes: NotRequired[int]
    lifecycleHooks: NotRequired[Sequence[DeploymentLifecycleHookTypeDef]]
    linearConfiguration: NotRequired[LinearConfigurationTypeDef]
    canaryConfiguration: NotRequired[CanaryConfigurationTypeDef]
    earlySuccessCriteria: NotRequired[DeploymentEarlySuccessCriteriaTypeDef]

class ClusterConfigurationTypeDef(TypedDict):
    executeCommandConfiguration: NotRequired[ExecuteCommandConfigurationTypeDef]
    managedStorageConfiguration: NotRequired[ManagedStorageConfigurationTypeDef]

class ExpressGatewayServiceConfigurationTypeDef(TypedDict):
    serviceRevisionArn: NotRequired[str]
    executionRoleArn: NotRequired[str]
    taskRoleArn: NotRequired[str]
    taskDefinitionArn: NotRequired[str]
    cpu: NotRequired[str]
    memory: NotRequired[str]
    networkConfiguration: NotRequired[ExpressGatewayServiceNetworkConfigurationOutputTypeDef]
    healthCheckPath: NotRequired[str]
    primaryContainer: NotRequired[ExpressGatewayContainerOutputTypeDef]
    scalingTarget: NotRequired[ExpressGatewayScalingTargetTypeDef]
    ingressPaths: NotRequired[list[IngressPathSummaryTypeDef]]
    createdAt: NotRequired[datetime]

ExpressGatewayContainerUnionTypeDef = Union[
    ExpressGatewayContainerTypeDef, ExpressGatewayContainerOutputTypeDef
]

class VolumeOutputTypeDef(TypedDict):
    name: NotRequired[str]
    host: NotRequired[HostVolumePropertiesTypeDef]
    dockerVolumeConfiguration: NotRequired[DockerVolumeConfigurationOutputTypeDef]
    efsVolumeConfiguration: NotRequired[EFSVolumeConfigurationTypeDef]
    s3filesVolumeConfiguration: NotRequired[S3FilesVolumeConfigurationTypeDef]
    fsxWindowsFileServerVolumeConfiguration: NotRequired[
        FSxWindowsFileServerVolumeConfigurationTypeDef
    ]
    configuredAtLaunch: NotRequired[bool]

class VolumeTypeDef(TypedDict):
    name: NotRequired[str]
    host: NotRequired[HostVolumePropertiesTypeDef]
    dockerVolumeConfiguration: NotRequired[DockerVolumeConfigurationUnionTypeDef]
    efsVolumeConfiguration: NotRequired[EFSVolumeConfigurationTypeDef]
    s3filesVolumeConfiguration: NotRequired[S3FilesVolumeConfigurationTypeDef]
    fsxWindowsFileServerVolumeConfiguration: NotRequired[
        FSxWindowsFileServerVolumeConfigurationTypeDef
    ]
    configuredAtLaunch: NotRequired[bool]

class InstanceLaunchTemplateOutputTypeDef(TypedDict):
    ec2InstanceProfileArn: str
    networkConfiguration: ManagedInstancesNetworkConfigurationOutputTypeDef
    storageConfiguration: NotRequired[ManagedInstancesStorageConfigurationTypeDef]
    localStorageConfiguration: NotRequired[ManagedInstancesLocalStorageConfigurationTypeDef]
    monitoring: NotRequired[ManagedInstancesMonitoringOptionsType]
    capacityOptionType: NotRequired[CapacityOptionTypeType]
    instanceMetadataTagsPropagation: NotRequired[bool]
    instanceRequirements: NotRequired[InstanceRequirementsRequestOutputTypeDef]
    fipsEnabled: NotRequired[bool]
    capacityReservations: NotRequired[CapacityReservationRequestTypeDef]

InstanceRequirementsRequestUnionTypeDef = Union[
    InstanceRequirementsRequestTypeDef, InstanceRequirementsRequestOutputTypeDef
]

class ECSManagedResourcesTypeDef(TypedDict):
    ingressPaths: NotRequired[list[ManagedIngressPathTypeDef]]
    autoScaling: NotRequired[ManagedAutoScalingTypeDef]
    metricAlarms: NotRequired[list[ManagedMetricAlarmTypeDef]]
    serviceSecurityGroups: NotRequired[list[ManagedSecurityGroupTypeDef]]
    logGroups: NotRequired[list[ManagedLogGroupTypeDef]]

MonitoringConfigurationUnionTypeDef = Union[
    MonitoringConfigurationTypeDef, MonitoringConfigurationOutputTypeDef
]

class RegisterContainerInstanceRequestTypeDef(TypedDict):
    cluster: NotRequired[str]
    instanceIdentityDocument: NotRequired[str]
    instanceIdentityDocumentSignature: NotRequired[str]
    totalResources: NotRequired[Sequence[ResourceUnionTypeDef]]
    versionInfo: NotRequired[VersionInfoTypeDef]
    containerInstanceArn: NotRequired[str]
    attributes: NotRequired[Sequence[AttributeTypeDef]]
    platformDevices: NotRequired[Sequence[PlatformDeviceTypeDef]]
    tags: NotRequired[Sequence[TagTypeDef]]

class ServiceConnectTestTrafficRulesTypeDef(TypedDict):
    header: ServiceConnectTestTrafficHeaderRulesTypeDef

class DaemonLinuxParametersTypeDef(TypedDict):
    capabilities: NotRequired[KernelCapabilitiesUnionTypeDef]
    devices: NotRequired[Sequence[DeviceUnionTypeDef]]
    initProcessEnabled: NotRequired[bool]
    tmpfs: NotRequired[Sequence[TmpfsUnionTypeDef]]

class LinuxParametersTypeDef(TypedDict):
    capabilities: NotRequired[KernelCapabilitiesUnionTypeDef]
    devices: NotRequired[Sequence[DeviceUnionTypeDef]]
    initProcessEnabled: NotRequired[bool]
    sharedMemorySize: NotRequired[int]
    tmpfs: NotRequired[Sequence[TmpfsUnionTypeDef]]
    maxSwap: NotRequired[int]
    swappiness: NotRequired[int]

class CreateTaskSetResponseTypeDef(TypedDict):
    taskSet: TaskSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteTaskSetResponseTypeDef(TypedDict):
    taskSet: TaskSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTaskSetsResponseTypeDef(TypedDict):
    taskSets: list[TaskSetTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServicePrimaryTaskSetResponseTypeDef(TypedDict):
    taskSet: TaskSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTaskSetResponseTypeDef(TypedDict):
    taskSet: TaskSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTaskSetRequestTypeDef(TypedDict):
    service: str
    cluster: str
    taskDefinition: str
    externalId: NotRequired[str]
    networkConfiguration: NotRequired[NetworkConfigurationUnionTypeDef]
    loadBalancers: NotRequired[Sequence[LoadBalancerTypeDef]]
    serviceRegistries: NotRequired[Sequence[ServiceRegistryTypeDef]]
    launchType: NotRequired[LaunchTypeType]
    capacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    platformVersion: NotRequired[str]
    scale: NotRequired[ScaleTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class ServiceVolumeConfigurationOutputTypeDef(TypedDict):
    name: str
    managedEBSVolume: NotRequired[ServiceManagedEBSVolumeConfigurationOutputTypeDef]

class ServiceManagedEBSVolumeConfigurationTypeDef(TypedDict):
    roleArn: str
    encrypted: NotRequired[bool]
    kmsKeyId: NotRequired[str]
    volumeType: NotRequired[str]
    sizeInGiB: NotRequired[int]
    snapshotId: NotRequired[str]
    volumeInitializationRate: NotRequired[int]
    iops: NotRequired[int]
    throughput: NotRequired[int]
    tagSpecifications: NotRequired[Sequence[EBSTagSpecificationUnionTypeDef]]
    filesystemType: NotRequired[TaskFilesystemTypeType]

class TaskManagedEBSVolumeConfigurationTypeDef(TypedDict):
    roleArn: str
    encrypted: NotRequired[bool]
    kmsKeyId: NotRequired[str]
    volumeType: NotRequired[str]
    sizeInGiB: NotRequired[int]
    snapshotId: NotRequired[str]
    volumeInitializationRate: NotRequired[int]
    iops: NotRequired[int]
    throughput: NotRequired[int]
    tagSpecifications: NotRequired[Sequence[EBSTagSpecificationUnionTypeDef]]
    terminationPolicy: NotRequired[TaskManagedEBSVolumeTerminationPolicyTypeDef]
    filesystemType: NotRequired[TaskFilesystemTypeType]

class TaskTypeDef(TypedDict):
    attachments: NotRequired[list[AttachmentTypeDef]]
    attributes: NotRequired[list[AttributeTypeDef]]
    availabilityZone: NotRequired[str]
    capacityProviderName: NotRequired[str]
    clusterArn: NotRequired[str]
    connectivity: NotRequired[ConnectivityType]
    connectivityAt: NotRequired[datetime]
    containerInstanceArn: NotRequired[str]
    containers: NotRequired[list[ContainerTypeDef]]
    cpu: NotRequired[str]
    createdAt: NotRequired[datetime]
    desiredStatus: NotRequired[str]
    enableExecuteCommand: NotRequired[bool]
    executionStoppedAt: NotRequired[datetime]
    group: NotRequired[str]
    healthStatus: NotRequired[HealthStatusType]
    inferenceAccelerators: NotRequired[list[InferenceAcceleratorTypeDef]]
    lastStatus: NotRequired[str]
    launchType: NotRequired[LaunchTypeType]
    memory: NotRequired[str]
    overrides: NotRequired[TaskOverrideOutputTypeDef]
    platformVersion: NotRequired[str]
    platformFamily: NotRequired[str]
    pullStartedAt: NotRequired[datetime]
    pullStoppedAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    startedBy: NotRequired[str]
    stopCode: NotRequired[TaskStopCodeType]
    stoppedAt: NotRequired[datetime]
    stoppedReason: NotRequired[str]
    stoppingAt: NotRequired[datetime]
    tags: NotRequired[list[TagTypeDef]]
    taskArn: NotRequired[str]
    taskDefinitionArn: NotRequired[str]
    version: NotRequired[int]
    ephemeralStorage: NotRequired[EphemeralStorageTypeDef]
    fargateEphemeralStorage: NotRequired[TaskEphemeralStorageTypeDef]

TaskOverrideUnionTypeDef = Union[TaskOverrideTypeDef, TaskOverrideOutputTypeDef]

class DeregisterContainerInstanceResponseTypeDef(TypedDict):
    containerInstance: ContainerInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeContainerInstancesResponseTypeDef(TypedDict):
    containerInstances: list[ContainerInstanceTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterContainerInstanceResponseTypeDef(TypedDict):
    containerInstance: ContainerInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateContainerAgentResponseTypeDef(TypedDict):
    containerInstance: ContainerInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateContainerInstancesStateResponseTypeDef(TypedDict):
    containerInstances: list[ContainerInstanceTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDaemonRequestTypeDef(TypedDict):
    daemonName: str
    daemonTaskDefinitionArn: str
    capacityProviderArns: Sequence[str]
    clusterArn: NotRequired[str]
    deploymentConfiguration: NotRequired[DaemonDeploymentConfigurationUnionTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    propagateTags: NotRequired[DaemonPropagateTagsType]
    enableECSManagedTags: NotRequired[bool]
    enableExecuteCommand: NotRequired[bool]
    clientToken: NotRequired[str]
    critical: NotRequired[bool]

class UpdateDaemonRequestTypeDef(TypedDict):
    daemonArn: str
    daemonTaskDefinitionArn: str
    capacityProviderArns: Sequence[str]
    deploymentConfiguration: NotRequired[DaemonDeploymentConfigurationUnionTypeDef]
    propagateTags: NotRequired[DaemonPropagateTagsType]
    enableECSManagedTags: NotRequired[bool]
    enableExecuteCommand: NotRequired[bool]
    critical: NotRequired[bool]

class DescribeDaemonResponseTypeDef(TypedDict):
    daemon: DaemonDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeDaemonDeploymentsResponseTypeDef(TypedDict):
    failures: list[FailureTypeDef]
    daemonDeployments: list[DaemonDeploymentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DaemonTaskDefinitionTypeDef(TypedDict):
    daemonTaskDefinitionArn: NotRequired[str]
    family: NotRequired[str]
    revision: NotRequired[int]
    taskRoleArn: NotRequired[str]
    executionRoleArn: NotRequired[str]
    containerDefinitions: NotRequired[list[DaemonContainerDefinitionOutputTypeDef]]
    volumes: NotRequired[list[DaemonVolumeTypeDef]]
    cpu: NotRequired[str]
    memory: NotRequired[str]
    status: NotRequired[DaemonTaskDefinitionStatusType]
    registeredAt: NotRequired[datetime]
    deleteRequestedAt: NotRequired[datetime]
    registeredBy: NotRequired[str]
    pidMode: NotRequired[DaemonPidModeType]
    ipcMode: NotRequired[DaemonIpcModeType]

class ServiceDeploymentTypeDef(TypedDict):
    serviceDeploymentArn: NotRequired[str]
    serviceArn: NotRequired[str]
    clusterArn: NotRequired[str]
    createdAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    finishedAt: NotRequired[datetime]
    stoppedAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    sourceServiceRevisions: NotRequired[list[ServiceRevisionSummaryTypeDef]]
    targetServiceRevision: NotRequired[ServiceRevisionSummaryTypeDef]
    status: NotRequired[ServiceDeploymentStatusType]
    statusReason: NotRequired[str]
    lifecycleStage: NotRequired[ServiceDeploymentLifecycleStageType]
    lifecycleHookDetails: NotRequired[list[DeploymentLifecycleHookDetailTypeDef]]
    deploymentConfiguration: NotRequired[DeploymentConfigurationOutputTypeDef]
    rollback: NotRequired[RollbackTypeDef]
    deploymentCircuitBreaker: NotRequired[ServiceDeploymentCircuitBreakerTypeDef]
    alarms: NotRequired[ServiceDeploymentAlarmsTypeDef]

DeploymentConfigurationUnionTypeDef = Union[
    DeploymentConfigurationTypeDef, DeploymentConfigurationOutputTypeDef
]

class ClusterTypeDef(TypedDict):
    clusterArn: NotRequired[str]
    clusterName: NotRequired[str]
    configuration: NotRequired[ClusterConfigurationTypeDef]
    status: NotRequired[str]
    registeredContainerInstancesCount: NotRequired[int]
    runningTasksCount: NotRequired[int]
    pendingTasksCount: NotRequired[int]
    activeServicesCount: NotRequired[int]
    statistics: NotRequired[list[KeyValuePairTypeDef]]
    tags: NotRequired[list[TagTypeDef]]
    settings: NotRequired[list[ClusterSettingTypeDef]]
    capacityProviders: NotRequired[list[str]]
    defaultCapacityProviderStrategy: NotRequired[list[CapacityProviderStrategyItemTypeDef]]
    attachments: NotRequired[list[AttachmentTypeDef]]
    attachmentsStatus: NotRequired[str]
    serviceConnectDefaults: NotRequired[ClusterServiceConnectDefaultsTypeDef]

class CreateClusterRequestTypeDef(TypedDict):
    clusterName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    settings: NotRequired[Sequence[ClusterSettingTypeDef]]
    configuration: NotRequired[ClusterConfigurationTypeDef]
    capacityProviders: NotRequired[Sequence[str]]
    defaultCapacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    serviceConnectDefaults: NotRequired[ClusterServiceConnectDefaultsRequestTypeDef]

class UpdateClusterRequestTypeDef(TypedDict):
    cluster: str
    settings: NotRequired[Sequence[ClusterSettingTypeDef]]
    configuration: NotRequired[ClusterConfigurationTypeDef]
    serviceConnectDefaults: NotRequired[ClusterServiceConnectDefaultsRequestTypeDef]

class ECSExpressGatewayServiceTypeDef(TypedDict):
    cluster: NotRequired[str]
    serviceName: NotRequired[str]
    serviceArn: NotRequired[str]
    infrastructureRoleArn: NotRequired[str]
    status: NotRequired[ExpressGatewayServiceStatusTypeDef]
    currentDeployment: NotRequired[str]
    activeConfigurations: NotRequired[list[ExpressGatewayServiceConfigurationTypeDef]]
    tags: NotRequired[list[TagTypeDef]]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class UpdatedExpressGatewayServiceTypeDef(TypedDict):
    serviceArn: NotRequired[str]
    cluster: NotRequired[str]
    serviceName: NotRequired[str]
    status: NotRequired[ExpressGatewayServiceStatusTypeDef]
    targetConfiguration: NotRequired[ExpressGatewayServiceConfigurationTypeDef]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class CreateExpressGatewayServiceRequestTypeDef(TypedDict):
    infrastructureRoleArn: str
    executionRoleArn: NotRequired[str]
    serviceName: NotRequired[str]
    cluster: NotRequired[str]
    healthCheckPath: NotRequired[str]
    primaryContainer: NotRequired[ExpressGatewayContainerUnionTypeDef]
    taskRoleArn: NotRequired[str]
    networkConfiguration: NotRequired[ExpressGatewayServiceNetworkConfigurationUnionTypeDef]
    cpu: NotRequired[str]
    memory: NotRequired[str]
    scalingTarget: NotRequired[ExpressGatewayScalingTargetTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    taskDefinitionArn: NotRequired[str]

class UpdateExpressGatewayServiceRequestTypeDef(TypedDict):
    serviceArn: str
    executionRoleArn: NotRequired[str]
    healthCheckPath: NotRequired[str]
    primaryContainer: NotRequired[ExpressGatewayContainerUnionTypeDef]
    taskRoleArn: NotRequired[str]
    networkConfiguration: NotRequired[ExpressGatewayServiceNetworkConfigurationUnionTypeDef]
    cpu: NotRequired[str]
    memory: NotRequired[str]
    scalingTarget: NotRequired[ExpressGatewayScalingTargetTypeDef]
    taskDefinitionArn: NotRequired[str]

class TaskDefinitionTypeDef(TypedDict):
    taskDefinitionArn: NotRequired[str]
    containerDefinitions: NotRequired[list[ContainerDefinitionOutputTypeDef]]
    family: NotRequired[str]
    taskRoleArn: NotRequired[str]
    executionRoleArn: NotRequired[str]
    networkMode: NotRequired[NetworkModeType]
    revision: NotRequired[int]
    volumes: NotRequired[list[VolumeOutputTypeDef]]
    status: NotRequired[TaskDefinitionStatusType]
    requiresAttributes: NotRequired[list[AttributeTypeDef]]
    placementConstraints: NotRequired[list[TaskDefinitionPlacementConstraintTypeDef]]
    compatibilities: NotRequired[list[CompatibilityType]]
    runtimePlatform: NotRequired[RuntimePlatformTypeDef]
    requiresCompatibilities: NotRequired[list[CompatibilityType]]
    cpu: NotRequired[str]
    memory: NotRequired[str]
    inferenceAccelerators: NotRequired[list[InferenceAcceleratorTypeDef]]
    pidMode: NotRequired[PidModeType]
    ipcMode: NotRequired[IpcModeType]
    proxyConfiguration: NotRequired[ProxyConfigurationOutputTypeDef]
    registeredAt: NotRequired[datetime]
    deregisteredAt: NotRequired[datetime]
    deleteRequestedAt: NotRequired[datetime]
    registeredBy: NotRequired[str]
    ephemeralStorage: NotRequired[EphemeralStorageTypeDef]
    enableFaultInjection: NotRequired[bool]

VolumeUnionTypeDef = Union[VolumeTypeDef, VolumeOutputTypeDef]

class ManagedInstancesProviderTypeDef(TypedDict):
    infrastructureRoleArn: NotRequired[str]
    instanceLaunchTemplate: NotRequired[InstanceLaunchTemplateOutputTypeDef]
    propagateTags: NotRequired[PropagateMITagsType]
    infrastructureOptimization: NotRequired[InfrastructureOptimizationTypeDef]
    autoRepairConfiguration: NotRequired[AutoRepairConfigurationTypeDef]

class InstanceLaunchTemplateTypeDef(TypedDict):
    ec2InstanceProfileArn: str
    networkConfiguration: ManagedInstancesNetworkConfigurationUnionTypeDef
    storageConfiguration: NotRequired[ManagedInstancesStorageConfigurationTypeDef]
    localStorageConfiguration: NotRequired[ManagedInstancesLocalStorageConfigurationTypeDef]
    monitoring: NotRequired[ManagedInstancesMonitoringOptionsType]
    capacityOptionType: NotRequired[CapacityOptionTypeType]
    instanceMetadataTagsPropagation: NotRequired[bool]
    instanceRequirements: NotRequired[InstanceRequirementsRequestUnionTypeDef]
    fipsEnabled: NotRequired[bool]
    capacityReservations: NotRequired[CapacityReservationRequestTypeDef]

class InstanceLaunchTemplateUpdateTypeDef(TypedDict):
    ec2InstanceProfileArn: NotRequired[str]
    networkConfiguration: NotRequired[ManagedInstancesNetworkConfigurationUnionTypeDef]
    storageConfiguration: NotRequired[ManagedInstancesStorageConfigurationTypeDef]
    instanceMetadataTagsPropagation: NotRequired[bool]
    localStorageConfiguration: NotRequired[ManagedInstancesLocalStorageConfigurationTypeDef]
    monitoring: NotRequired[ManagedInstancesMonitoringOptionsType]
    instanceRequirements: NotRequired[InstanceRequirementsRequestUnionTypeDef]
    capacityReservations: NotRequired[CapacityReservationRequestTypeDef]

class ServiceConnectClientAliasTypeDef(TypedDict):
    port: int
    dnsName: NotRequired[str]
    testTrafficRules: NotRequired[ServiceConnectTestTrafficRulesTypeDef]

DaemonLinuxParametersUnionTypeDef = Union[
    DaemonLinuxParametersTypeDef, DaemonLinuxParametersOutputTypeDef
]
LinuxParametersUnionTypeDef = Union[LinuxParametersTypeDef, LinuxParametersOutputTypeDef]
ServiceManagedEBSVolumeConfigurationUnionTypeDef = Union[
    ServiceManagedEBSVolumeConfigurationTypeDef, ServiceManagedEBSVolumeConfigurationOutputTypeDef
]

class TaskVolumeConfigurationTypeDef(TypedDict):
    name: str
    managedEBSVolume: NotRequired[TaskManagedEBSVolumeConfigurationTypeDef]

class DescribeTasksResponseTypeDef(TypedDict):
    tasks: list[TaskTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RunTaskResponseTypeDef(TypedDict):
    tasks: list[TaskTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartTaskResponseTypeDef(TypedDict):
    tasks: list[TaskTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StopTaskResponseTypeDef(TypedDict):
    task: TaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeDaemonTaskDefinitionResponseTypeDef(TypedDict):
    daemonTaskDefinition: DaemonTaskDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeServiceDeploymentsResponseTypeDef(TypedDict):
    serviceDeployments: list[ServiceDeploymentTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeClustersResponseTypeDef(TypedDict):
    clusters: list[ClusterTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PutClusterCapacityProvidersResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateClusterResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateClusterSettingsResponseTypeDef(TypedDict):
    cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateExpressGatewayServiceResponseTypeDef(TypedDict):
    service: ECSExpressGatewayServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteExpressGatewayServiceResponseTypeDef(TypedDict):
    service: ECSExpressGatewayServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeExpressGatewayServiceResponseTypeDef(TypedDict):
    service: ECSExpressGatewayServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateExpressGatewayServiceResponseTypeDef(TypedDict):
    service: UpdatedExpressGatewayServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteTaskDefinitionsResponseTypeDef(TypedDict):
    taskDefinitions: list[TaskDefinitionTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeregisterTaskDefinitionResponseTypeDef(TypedDict):
    taskDefinition: TaskDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTaskDefinitionResponseTypeDef(TypedDict):
    taskDefinition: TaskDefinitionTypeDef
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterTaskDefinitionResponseTypeDef(TypedDict):
    taskDefinition: TaskDefinitionTypeDef
    tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

CapacityProviderTypeDef = TypedDict(
    "CapacityProviderTypeDef",
    {
        "capacityProviderArn": NotRequired[str],
        "name": NotRequired[str],
        "cluster": NotRequired[str],
        "status": NotRequired[CapacityProviderStatusType],
        "autoScalingGroupProvider": NotRequired[AutoScalingGroupProviderTypeDef],
        "managedInstancesProvider": NotRequired[ManagedInstancesProviderTypeDef],
        "updateStatus": NotRequired[CapacityProviderUpdateStatusType],
        "updateStatusReason": NotRequired[str],
        "tags": NotRequired[list[TagTypeDef]],
        "type": NotRequired[CapacityProviderTypeType],
    },
)
InstanceLaunchTemplateUnionTypeDef = Union[
    InstanceLaunchTemplateTypeDef, InstanceLaunchTemplateOutputTypeDef
]

class UpdateManagedInstancesProviderConfigurationTypeDef(TypedDict):
    infrastructureRoleArn: str
    instanceLaunchTemplate: InstanceLaunchTemplateUpdateTypeDef
    propagateTags: NotRequired[PropagateMITagsType]
    infrastructureOptimization: NotRequired[InfrastructureOptimizationTypeDef]
    autoRepairConfiguration: NotRequired[AutoRepairConfigurationTypeDef]

class ServiceConnectServiceOutputTypeDef(TypedDict):
    portName: str
    discoveryName: NotRequired[str]
    clientAliases: NotRequired[list[ServiceConnectClientAliasTypeDef]]
    ingressPortOverride: NotRequired[int]
    timeout: NotRequired[TimeoutConfigurationTypeDef]
    tls: NotRequired[ServiceConnectTlsConfigurationTypeDef]

class ServiceConnectServiceTypeDef(TypedDict):
    portName: str
    discoveryName: NotRequired[str]
    clientAliases: NotRequired[Sequence[ServiceConnectClientAliasTypeDef]]
    ingressPortOverride: NotRequired[int]
    timeout: NotRequired[TimeoutConfigurationTypeDef]
    tls: NotRequired[ServiceConnectTlsConfigurationTypeDef]

class DaemonContainerDefinitionTypeDef(TypedDict):
    image: str
    name: NotRequired[str]
    memory: NotRequired[int]
    memoryReservation: NotRequired[int]
    repositoryCredentials: NotRequired[RepositoryCredentialsTypeDef]
    healthCheck: NotRequired[HealthCheckUnionTypeDef]
    cpu: NotRequired[int]
    essential: NotRequired[bool]
    entryPoint: NotRequired[Sequence[str]]
    command: NotRequired[Sequence[str]]
    workingDirectory: NotRequired[str]
    environmentFiles: NotRequired[Sequence[EnvironmentFileTypeDef]]
    environment: NotRequired[Sequence[KeyValuePairTypeDef]]
    secrets: NotRequired[Sequence[SecretTypeDef]]
    readonlyRootFilesystem: NotRequired[bool]
    mountPoints: NotRequired[Sequence[MountPointTypeDef]]
    logConfiguration: NotRequired[LogConfigurationUnionTypeDef]
    firelensConfiguration: NotRequired[FirelensConfigurationUnionTypeDef]
    privileged: NotRequired[bool]
    user: NotRequired[str]
    ulimits: NotRequired[Sequence[UlimitTypeDef]]
    linuxParameters: NotRequired[DaemonLinuxParametersUnionTypeDef]
    dependsOn: NotRequired[Sequence[ContainerDependencyTypeDef]]
    startTimeout: NotRequired[int]
    stopTimeout: NotRequired[int]
    systemControls: NotRequired[Sequence[SystemControlTypeDef]]
    interactive: NotRequired[bool]
    pseudoTerminal: NotRequired[bool]
    restartPolicy: NotRequired[ContainerRestartPolicyUnionTypeDef]

class ContainerDefinitionTypeDef(TypedDict):
    name: NotRequired[str]
    image: NotRequired[str]
    repositoryCredentials: NotRequired[RepositoryCredentialsTypeDef]
    cpu: NotRequired[int]
    memory: NotRequired[int]
    memoryReservation: NotRequired[int]
    links: NotRequired[Sequence[str]]
    portMappings: NotRequired[Sequence[PortMappingTypeDef]]
    essential: NotRequired[bool]
    restartPolicy: NotRequired[ContainerRestartPolicyUnionTypeDef]
    entryPoint: NotRequired[Sequence[str]]
    command: NotRequired[Sequence[str]]
    environment: NotRequired[Sequence[KeyValuePairTypeDef]]
    environmentFiles: NotRequired[Sequence[EnvironmentFileTypeDef]]
    mountPoints: NotRequired[Sequence[MountPointTypeDef]]
    volumesFrom: NotRequired[Sequence[VolumeFromTypeDef]]
    linuxParameters: NotRequired[LinuxParametersUnionTypeDef]
    secrets: NotRequired[Sequence[SecretTypeDef]]
    dependsOn: NotRequired[Sequence[ContainerDependencyTypeDef]]
    startTimeout: NotRequired[int]
    stopTimeout: NotRequired[int]
    versionConsistency: NotRequired[VersionConsistencyType]
    hostname: NotRequired[str]
    user: NotRequired[str]
    workingDirectory: NotRequired[str]
    disableNetworking: NotRequired[bool]
    privileged: NotRequired[bool]
    readonlyRootFilesystem: NotRequired[bool]
    dnsServers: NotRequired[Sequence[str]]
    dnsSearchDomains: NotRequired[Sequence[str]]
    extraHosts: NotRequired[Sequence[HostEntryTypeDef]]
    dockerSecurityOptions: NotRequired[Sequence[str]]
    interactive: NotRequired[bool]
    pseudoTerminal: NotRequired[bool]
    dockerLabels: NotRequired[Mapping[str, str]]
    ulimits: NotRequired[Sequence[UlimitTypeDef]]
    logConfiguration: NotRequired[LogConfigurationUnionTypeDef]
    healthCheck: NotRequired[HealthCheckUnionTypeDef]
    systemControls: NotRequired[Sequence[SystemControlTypeDef]]
    resourceRequirements: NotRequired[Sequence[ResourceRequirementTypeDef]]
    firelensConfiguration: NotRequired[FirelensConfigurationUnionTypeDef]
    credentialSpecs: NotRequired[Sequence[str]]

class ServiceVolumeConfigurationTypeDef(TypedDict):
    name: str
    managedEBSVolume: NotRequired[ServiceManagedEBSVolumeConfigurationUnionTypeDef]

class RunTaskRequestTypeDef(TypedDict):
    taskDefinition: str
    capacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    cluster: NotRequired[str]
    count: NotRequired[int]
    enableECSManagedTags: NotRequired[bool]
    enableExecuteCommand: NotRequired[bool]
    group: NotRequired[str]
    launchType: NotRequired[LaunchTypeType]
    networkConfiguration: NotRequired[NetworkConfigurationUnionTypeDef]
    overrides: NotRequired[TaskOverrideUnionTypeDef]
    placementConstraints: NotRequired[Sequence[PlacementConstraintTypeDef]]
    placementStrategy: NotRequired[Sequence[PlacementStrategyTypeDef]]
    platformVersion: NotRequired[str]
    propagateTags: NotRequired[PropagateTagsType]
    referenceId: NotRequired[str]
    startedBy: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    clientToken: NotRequired[str]
    volumeConfigurations: NotRequired[Sequence[TaskVolumeConfigurationTypeDef]]

class StartTaskRequestTypeDef(TypedDict):
    containerInstances: Sequence[str]
    taskDefinition: str
    cluster: NotRequired[str]
    enableECSManagedTags: NotRequired[bool]
    enableExecuteCommand: NotRequired[bool]
    group: NotRequired[str]
    networkConfiguration: NotRequired[NetworkConfigurationUnionTypeDef]
    overrides: NotRequired[TaskOverrideUnionTypeDef]
    propagateTags: NotRequired[PropagateTagsType]
    referenceId: NotRequired[str]
    startedBy: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    volumeConfigurations: NotRequired[Sequence[TaskVolumeConfigurationTypeDef]]

class CreateCapacityProviderResponseTypeDef(TypedDict):
    capacityProvider: CapacityProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteCapacityProviderResponseTypeDef(TypedDict):
    capacityProvider: CapacityProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeCapacityProvidersResponseTypeDef(TypedDict):
    capacityProviders: list[CapacityProviderTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateCapacityProviderResponseTypeDef(TypedDict):
    capacityProvider: CapacityProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateManagedInstancesProviderConfigurationTypeDef(TypedDict):
    infrastructureRoleArn: str
    instanceLaunchTemplate: InstanceLaunchTemplateUnionTypeDef
    propagateTags: NotRequired[PropagateMITagsType]
    infrastructureOptimization: NotRequired[InfrastructureOptimizationTypeDef]
    autoRepairConfiguration: NotRequired[AutoRepairConfigurationTypeDef]

class UpdateCapacityProviderRequestTypeDef(TypedDict):
    name: str
    cluster: NotRequired[str]
    autoScalingGroupProvider: NotRequired[AutoScalingGroupProviderUpdateTypeDef]
    managedInstancesProvider: NotRequired[UpdateManagedInstancesProviderConfigurationTypeDef]

class ServiceConnectConfigurationOutputTypeDef(TypedDict):
    enabled: bool
    namespace: NotRequired[str]
    services: NotRequired[list[ServiceConnectServiceOutputTypeDef]]
    logConfiguration: NotRequired[LogConfigurationOutputTypeDef]
    accessLogConfiguration: NotRequired[ServiceConnectAccessLogConfigurationTypeDef]

class ServiceConnectConfigurationTypeDef(TypedDict):
    enabled: bool
    namespace: NotRequired[str]
    services: NotRequired[Sequence[ServiceConnectServiceTypeDef]]
    logConfiguration: NotRequired[LogConfigurationTypeDef]
    accessLogConfiguration: NotRequired[ServiceConnectAccessLogConfigurationTypeDef]

DaemonContainerDefinitionUnionTypeDef = Union[
    DaemonContainerDefinitionTypeDef, DaemonContainerDefinitionOutputTypeDef
]
ContainerDefinitionUnionTypeDef = Union[
    ContainerDefinitionTypeDef, ContainerDefinitionOutputTypeDef
]
ServiceVolumeConfigurationUnionTypeDef = Union[
    ServiceVolumeConfigurationTypeDef, ServiceVolumeConfigurationOutputTypeDef
]

class CreateCapacityProviderRequestTypeDef(TypedDict):
    name: str
    cluster: NotRequired[str]
    autoScalingGroupProvider: NotRequired[AutoScalingGroupProviderTypeDef]
    managedInstancesProvider: NotRequired[CreateManagedInstancesProviderConfigurationTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]

DeploymentTypeDef = TypedDict(
    "DeploymentTypeDef",
    {
        "id": NotRequired[str],
        "status": NotRequired[str],
        "taskDefinition": NotRequired[str],
        "desiredCount": NotRequired[int],
        "pendingCount": NotRequired[int],
        "runningCount": NotRequired[int],
        "failedTasks": NotRequired[int],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "capacityProviderStrategy": NotRequired[list[CapacityProviderStrategyItemTypeDef]],
        "launchType": NotRequired[LaunchTypeType],
        "platformVersion": NotRequired[str],
        "platformFamily": NotRequired[str],
        "networkConfiguration": NotRequired[NetworkConfigurationOutputTypeDef],
        "rolloutState": NotRequired[DeploymentRolloutStateType],
        "rolloutStateReason": NotRequired[str],
        "serviceConnectConfiguration": NotRequired[ServiceConnectConfigurationOutputTypeDef],
        "serviceConnectResources": NotRequired[list[ServiceConnectServiceResourceTypeDef]],
        "volumeConfigurations": NotRequired[list[ServiceVolumeConfigurationOutputTypeDef]],
        "fargateEphemeralStorage": NotRequired[DeploymentEphemeralStorageTypeDef],
        "vpcLatticeConfigurations": NotRequired[list[VpcLatticeConfigurationTypeDef]],
    },
)

class ServiceRevisionTypeDef(TypedDict):
    serviceRevisionArn: NotRequired[str]
    serviceArn: NotRequired[str]
    clusterArn: NotRequired[str]
    taskDefinition: NotRequired[str]
    capacityProviderStrategy: NotRequired[list[CapacityProviderStrategyItemTypeDef]]
    launchType: NotRequired[LaunchTypeType]
    platformVersion: NotRequired[str]
    platformFamily: NotRequired[str]
    loadBalancers: NotRequired[list[LoadBalancerTypeDef]]
    serviceRegistries: NotRequired[list[ServiceRegistryTypeDef]]
    networkConfiguration: NotRequired[NetworkConfigurationOutputTypeDef]
    containerImages: NotRequired[list[ContainerImageTypeDef]]
    guardDutyEnabled: NotRequired[bool]
    serviceConnectConfiguration: NotRequired[ServiceConnectConfigurationOutputTypeDef]
    volumeConfigurations: NotRequired[list[ServiceVolumeConfigurationOutputTypeDef]]
    fargateEphemeralStorage: NotRequired[DeploymentEphemeralStorageTypeDef]
    createdAt: NotRequired[datetime]
    vpcLatticeConfigurations: NotRequired[list[VpcLatticeConfigurationTypeDef]]
    resolvedConfiguration: NotRequired[ResolvedConfigurationTypeDef]
    ecsManagedResources: NotRequired[ECSManagedResourcesTypeDef]
    overrides: NotRequired[ServiceRevisionOverridesTypeDef]
    monitoring: NotRequired[MonitoringConfigurationOutputTypeDef]

ServiceConnectConfigurationUnionTypeDef = Union[
    ServiceConnectConfigurationTypeDef, ServiceConnectConfigurationOutputTypeDef
]

class RegisterDaemonTaskDefinitionRequestTypeDef(TypedDict):
    family: str
    containerDefinitions: Sequence[DaemonContainerDefinitionUnionTypeDef]
    taskRoleArn: NotRequired[str]
    executionRoleArn: NotRequired[str]
    cpu: NotRequired[str]
    memory: NotRequired[str]
    volumes: NotRequired[Sequence[DaemonVolumeTypeDef]]
    tags: NotRequired[Sequence[TagTypeDef]]
    pidMode: NotRequired[DaemonPidModeType]
    ipcMode: NotRequired[DaemonIpcModeType]

class RegisterTaskDefinitionRequestTypeDef(TypedDict):
    family: str
    containerDefinitions: Sequence[ContainerDefinitionUnionTypeDef]
    taskRoleArn: NotRequired[str]
    executionRoleArn: NotRequired[str]
    networkMode: NotRequired[NetworkModeType]
    volumes: NotRequired[Sequence[VolumeUnionTypeDef]]
    placementConstraints: NotRequired[Sequence[TaskDefinitionPlacementConstraintTypeDef]]
    requiresCompatibilities: NotRequired[Sequence[CompatibilityType]]
    cpu: NotRequired[str]
    memory: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    pidMode: NotRequired[PidModeType]
    ipcMode: NotRequired[IpcModeType]
    proxyConfiguration: NotRequired[ProxyConfigurationUnionTypeDef]
    inferenceAccelerators: NotRequired[Sequence[InferenceAcceleratorTypeDef]]
    ephemeralStorage: NotRequired[EphemeralStorageTypeDef]
    runtimePlatform: NotRequired[RuntimePlatformTypeDef]
    enableFaultInjection: NotRequired[bool]

class ServiceTypeDef(TypedDict):
    serviceArn: NotRequired[str]
    serviceName: NotRequired[str]
    clusterArn: NotRequired[str]
    loadBalancers: NotRequired[list[LoadBalancerTypeDef]]
    serviceRegistries: NotRequired[list[ServiceRegistryTypeDef]]
    status: NotRequired[str]
    desiredCount: NotRequired[int]
    runningCount: NotRequired[int]
    pendingCount: NotRequired[int]
    launchType: NotRequired[LaunchTypeType]
    capacityProviderStrategy: NotRequired[list[CapacityProviderStrategyItemTypeDef]]
    platformVersion: NotRequired[str]
    platformFamily: NotRequired[str]
    taskDefinition: NotRequired[str]
    deploymentConfiguration: NotRequired[DeploymentConfigurationOutputTypeDef]
    taskSets: NotRequired[list[TaskSetTypeDef]]
    deployments: NotRequired[list[DeploymentTypeDef]]
    roleArn: NotRequired[str]
    events: NotRequired[list[ServiceEventTypeDef]]
    createdAt: NotRequired[datetime]
    currentServiceDeployment: NotRequired[str]
    currentServiceRevisions: NotRequired[list[ServiceCurrentRevisionSummaryTypeDef]]
    placementConstraints: NotRequired[list[PlacementConstraintTypeDef]]
    placementStrategy: NotRequired[list[PlacementStrategyTypeDef]]
    networkConfiguration: NotRequired[NetworkConfigurationOutputTypeDef]
    healthCheckGracePeriodSeconds: NotRequired[int]
    schedulingStrategy: NotRequired[SchedulingStrategyType]
    deploymentController: NotRequired[DeploymentControllerTypeDef]
    tags: NotRequired[list[TagTypeDef]]
    createdBy: NotRequired[str]
    enableECSManagedTags: NotRequired[bool]
    propagateTags: NotRequired[PropagateTagsType]
    enableExecuteCommand: NotRequired[bool]
    availabilityZoneRebalancing: NotRequired[AvailabilityZoneRebalancingType]
    resourceManagementType: NotRequired[ResourceManagementTypeType]

class DescribeServiceRevisionsResponseTypeDef(TypedDict):
    serviceRevisions: list[ServiceRevisionTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateServiceRequestTypeDef(TypedDict):
    serviceName: str
    cluster: NotRequired[str]
    taskDefinition: NotRequired[str]
    availabilityZoneRebalancing: NotRequired[AvailabilityZoneRebalancingType]
    loadBalancers: NotRequired[Sequence[LoadBalancerTypeDef]]
    serviceRegistries: NotRequired[Sequence[ServiceRegistryTypeDef]]
    desiredCount: NotRequired[int]
    clientToken: NotRequired[str]
    launchType: NotRequired[LaunchTypeType]
    capacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    platformVersion: NotRequired[str]
    role: NotRequired[str]
    deploymentConfiguration: NotRequired[DeploymentConfigurationUnionTypeDef]
    placementConstraints: NotRequired[Sequence[PlacementConstraintTypeDef]]
    placementStrategy: NotRequired[Sequence[PlacementStrategyTypeDef]]
    networkConfiguration: NotRequired[NetworkConfigurationUnionTypeDef]
    healthCheckGracePeriodSeconds: NotRequired[int]
    schedulingStrategy: NotRequired[SchedulingStrategyType]
    deploymentController: NotRequired[DeploymentControllerTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    enableECSManagedTags: NotRequired[bool]
    propagateTags: NotRequired[PropagateTagsType]
    enableExecuteCommand: NotRequired[bool]
    serviceConnectConfiguration: NotRequired[ServiceConnectConfigurationUnionTypeDef]
    volumeConfigurations: NotRequired[Sequence[ServiceVolumeConfigurationUnionTypeDef]]
    vpcLatticeConfigurations: NotRequired[Sequence[VpcLatticeConfigurationTypeDef]]
    monitoring: NotRequired[MonitoringConfigurationUnionTypeDef]

class UpdateServiceRequestTypeDef(TypedDict):
    service: str
    cluster: NotRequired[str]
    desiredCount: NotRequired[int]
    taskDefinition: NotRequired[str]
    capacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    deploymentConfiguration: NotRequired[DeploymentConfigurationUnionTypeDef]
    availabilityZoneRebalancing: NotRequired[AvailabilityZoneRebalancingType]
    networkConfiguration: NotRequired[NetworkConfigurationUnionTypeDef]
    placementConstraints: NotRequired[Sequence[PlacementConstraintTypeDef]]
    placementStrategy: NotRequired[Sequence[PlacementStrategyTypeDef]]
    platformVersion: NotRequired[str]
    forceNewDeployment: NotRequired[bool]
    healthCheckGracePeriodSeconds: NotRequired[int]
    deploymentController: NotRequired[DeploymentControllerTypeDef]
    enableExecuteCommand: NotRequired[bool]
    enableECSManagedTags: NotRequired[bool]
    loadBalancers: NotRequired[Sequence[LoadBalancerTypeDef]]
    propagateTags: NotRequired[PropagateTagsType]
    serviceRegistries: NotRequired[Sequence[ServiceRegistryTypeDef]]
    serviceConnectConfiguration: NotRequired[ServiceConnectConfigurationUnionTypeDef]
    volumeConfigurations: NotRequired[Sequence[ServiceVolumeConfigurationUnionTypeDef]]
    vpcLatticeConfigurations: NotRequired[Sequence[VpcLatticeConfigurationTypeDef]]
    monitoring: NotRequired[MonitoringConfigurationUnionTypeDef]

class CreateServiceResponseTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteServiceResponseTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeServicesResponseTypeDef(TypedDict):
    services: list[ServiceTypeDef]
    failures: list[FailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateServiceResponseTypeDef(TypedDict):
    service: ServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
