"""
Type annotations for gamelift service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_gamelift.type_defs import AcceptMatchInputTypeDef

    data: AcceptMatchInputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    AcceptanceTypeType,
    BackfillModeType,
    BalancingStrategyType,
    BuildStatusType,
    CertificateTypeType,
    ComparisonOperatorTypeType,
    ComputeStatusType,
    ComputeTypeType,
    ContainerDependencyConditionType,
    ContainerFleetBillingTypeType,
    ContainerFleetLocationStatusType,
    ContainerFleetStatusType,
    ContainerGroupDefinitionStatusType,
    ContainerGroupTypeType,
    ContainerMountPointAccessLevelType,
    DeploymentImpairmentStrategyType,
    DeploymentProtectionStrategyType,
    DeploymentStatusType,
    EC2InstanceTypeType,
    EventCodeType,
    FilterInstanceStatusType,
    FleetStatusType,
    FleetTypeType,
    FlexMatchModeType,
    GameServerGroupDeleteOptionType,
    GameServerGroupInstanceTypeType,
    GameServerGroupStatusType,
    GameServerInstanceStatusType,
    GameServerProtectionPolicyType,
    GameServerUtilizationStatusType,
    GameSessionPlacementStateType,
    GameSessionStatusReasonType,
    GameSessionStatusType,
    InstanceStatusType,
    IpProtocolType,
    ListComputeInputStatusType,
    LocationFilterType,
    LogDestinationType,
    MatchmakingConfigurationStatusType,
    MetricNameType,
    OperatingSystemType,
    PlacementFallbackStrategyType,
    PlayerSessionCreationPolicyType,
    PlayerSessionStatusType,
    PolicyTypeType,
    PriorityTypeType,
    ProtectionPolicyType,
    RoutingStrategyTypeType,
    ScalingAdjustmentTypeType,
    ScalingStatusTypeType,
    SortOrderType,
    TerminationModeType,
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
    "AcceptMatchInputTypeDef",
    "AliasTypeDef",
    "AnywhereConfigurationTypeDef",
    "AttributeValueOutputTypeDef",
    "AttributeValueTypeDef",
    "AttributeValueUnionTypeDef",
    "AwsCredentialsTypeDef",
    "BlobTypeDef",
    "BuildTypeDef",
    "CertificateConfigurationTypeDef",
    "ClaimFilterOptionTypeDef",
    "ClaimGameServerInputTypeDef",
    "ClaimGameServerOutputTypeDef",
    "ComputeTypeDef",
    "ConnectionPortRangeTypeDef",
    "ContainerAttributeTypeDef",
    "ContainerDependencyTypeDef",
    "ContainerEnvironmentTypeDef",
    "ContainerFleetLocationAttributesTypeDef",
    "ContainerFleetTypeDef",
    "ContainerGroupDefinitionTypeDef",
    "ContainerHealthCheckOutputTypeDef",
    "ContainerHealthCheckTypeDef",
    "ContainerHealthCheckUnionTypeDef",
    "ContainerIdentifierTypeDef",
    "ContainerMountPointTypeDef",
    "ContainerPortConfigurationOutputTypeDef",
    "ContainerPortConfigurationTypeDef",
    "ContainerPortConfigurationUnionTypeDef",
    "ContainerPortRangeTypeDef",
    "CreateAliasInputTypeDef",
    "CreateAliasOutputTypeDef",
    "CreateBuildInputTypeDef",
    "CreateBuildOutputTypeDef",
    "CreateContainerFleetInputTypeDef",
    "CreateContainerFleetOutputTypeDef",
    "CreateContainerGroupDefinitionInputTypeDef",
    "CreateContainerGroupDefinitionOutputTypeDef",
    "CreateFleetInputTypeDef",
    "CreateFleetLocationsInputTypeDef",
    "CreateFleetLocationsOutputTypeDef",
    "CreateFleetOutputTypeDef",
    "CreateGameServerGroupInputTypeDef",
    "CreateGameServerGroupOutputTypeDef",
    "CreateGameSessionInputTypeDef",
    "CreateGameSessionOutputTypeDef",
    "CreateGameSessionQueueInputTypeDef",
    "CreateGameSessionQueueOutputTypeDef",
    "CreateLocationInputTypeDef",
    "CreateLocationOutputTypeDef",
    "CreateMatchmakingConfigurationInputTypeDef",
    "CreateMatchmakingConfigurationOutputTypeDef",
    "CreateMatchmakingRuleSetInputTypeDef",
    "CreateMatchmakingRuleSetOutputTypeDef",
    "CreatePlayerSessionInputTypeDef",
    "CreatePlayerSessionOutputTypeDef",
    "CreatePlayerSessionsInputTypeDef",
    "CreatePlayerSessionsOutputTypeDef",
    "CreateScriptInputTypeDef",
    "CreateScriptOutputTypeDef",
    "CreateVpcPeeringAuthorizationInputTypeDef",
    "CreateVpcPeeringAuthorizationOutputTypeDef",
    "CreateVpcPeeringConnectionInputTypeDef",
    "DeleteAliasInputTypeDef",
    "DeleteBuildInputTypeDef",
    "DeleteContainerFleetInputTypeDef",
    "DeleteContainerGroupDefinitionInputTypeDef",
    "DeleteFleetInputTypeDef",
    "DeleteFleetLocationsInputTypeDef",
    "DeleteFleetLocationsOutputTypeDef",
    "DeleteGameServerGroupInputTypeDef",
    "DeleteGameServerGroupOutputTypeDef",
    "DeleteGameSessionQueueInputTypeDef",
    "DeleteLocationInputTypeDef",
    "DeleteMatchmakingConfigurationInputTypeDef",
    "DeleteMatchmakingRuleSetInputTypeDef",
    "DeleteScalingPolicyInputTypeDef",
    "DeleteScriptInputTypeDef",
    "DeleteVpcPeeringAuthorizationInputTypeDef",
    "DeleteVpcPeeringConnectionInputTypeDef",
    "DeploymentConfigurationTypeDef",
    "DeploymentDetailsTypeDef",
    "DeregisterComputeInputTypeDef",
    "DeregisterGameServerInputTypeDef",
    "DescribeAliasInputTypeDef",
    "DescribeAliasOutputTypeDef",
    "DescribeBuildInputTypeDef",
    "DescribeBuildOutputTypeDef",
    "DescribeComputeInputTypeDef",
    "DescribeComputeOutputTypeDef",
    "DescribeContainerFleetInputTypeDef",
    "DescribeContainerFleetOutputTypeDef",
    "DescribeContainerGroupDefinitionInputTypeDef",
    "DescribeContainerGroupDefinitionOutputTypeDef",
    "DescribeEC2InstanceLimitsInputTypeDef",
    "DescribeEC2InstanceLimitsOutputTypeDef",
    "DescribeFleetAttributesInputPaginateTypeDef",
    "DescribeFleetAttributesInputTypeDef",
    "DescribeFleetAttributesOutputTypeDef",
    "DescribeFleetCapacityInputPaginateTypeDef",
    "DescribeFleetCapacityInputTypeDef",
    "DescribeFleetCapacityOutputTypeDef",
    "DescribeFleetDeploymentInputTypeDef",
    "DescribeFleetDeploymentOutputTypeDef",
    "DescribeFleetEventsInputPaginateTypeDef",
    "DescribeFleetEventsInputTypeDef",
    "DescribeFleetEventsOutputTypeDef",
    "DescribeFleetLocationAttributesInputTypeDef",
    "DescribeFleetLocationAttributesOutputTypeDef",
    "DescribeFleetLocationCapacityInputTypeDef",
    "DescribeFleetLocationCapacityOutputTypeDef",
    "DescribeFleetLocationUtilizationInputTypeDef",
    "DescribeFleetLocationUtilizationOutputTypeDef",
    "DescribeFleetPortSettingsInputTypeDef",
    "DescribeFleetPortSettingsOutputTypeDef",
    "DescribeFleetUtilizationInputPaginateTypeDef",
    "DescribeFleetUtilizationInputTypeDef",
    "DescribeFleetUtilizationOutputTypeDef",
    "DescribeGameServerGroupInputTypeDef",
    "DescribeGameServerGroupOutputTypeDef",
    "DescribeGameServerInputTypeDef",
    "DescribeGameServerInstancesInputPaginateTypeDef",
    "DescribeGameServerInstancesInputTypeDef",
    "DescribeGameServerInstancesOutputTypeDef",
    "DescribeGameServerOutputTypeDef",
    "DescribeGameSessionDetailsInputPaginateTypeDef",
    "DescribeGameSessionDetailsInputTypeDef",
    "DescribeGameSessionDetailsOutputTypeDef",
    "DescribeGameSessionPlacementInputTypeDef",
    "DescribeGameSessionPlacementOutputTypeDef",
    "DescribeGameSessionQueuesInputPaginateTypeDef",
    "DescribeGameSessionQueuesInputTypeDef",
    "DescribeGameSessionQueuesOutputTypeDef",
    "DescribeGameSessionsInputPaginateTypeDef",
    "DescribeGameSessionsInputTypeDef",
    "DescribeGameSessionsOutputTypeDef",
    "DescribeInstancesInputPaginateTypeDef",
    "DescribeInstancesInputTypeDef",
    "DescribeInstancesOutputTypeDef",
    "DescribeMatchmakingConfigurationsInputPaginateTypeDef",
    "DescribeMatchmakingConfigurationsInputTypeDef",
    "DescribeMatchmakingConfigurationsOutputTypeDef",
    "DescribeMatchmakingInputTypeDef",
    "DescribeMatchmakingOutputTypeDef",
    "DescribeMatchmakingRuleSetsInputPaginateTypeDef",
    "DescribeMatchmakingRuleSetsInputTypeDef",
    "DescribeMatchmakingRuleSetsOutputTypeDef",
    "DescribePlayerSessionsInputPaginateTypeDef",
    "DescribePlayerSessionsInputTypeDef",
    "DescribePlayerSessionsOutputTypeDef",
    "DescribeRuntimeConfigurationInputTypeDef",
    "DescribeRuntimeConfigurationOutputTypeDef",
    "DescribeScalingPoliciesInputPaginateTypeDef",
    "DescribeScalingPoliciesInputTypeDef",
    "DescribeScalingPoliciesOutputTypeDef",
    "DescribeScriptInputTypeDef",
    "DescribeScriptOutputTypeDef",
    "DescribeVpcPeeringAuthorizationsOutputTypeDef",
    "DescribeVpcPeeringConnectionsInputTypeDef",
    "DescribeVpcPeeringConnectionsOutputTypeDef",
    "DesiredPlayerSessionTypeDef",
    "EC2InstanceCountsTypeDef",
    "EC2InstanceLimitTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventTypeDef",
    "FilterConfigurationOutputTypeDef",
    "FilterConfigurationTypeDef",
    "FilterConfigurationUnionTypeDef",
    "FleetAttributesTypeDef",
    "FleetCapacityTypeDef",
    "FleetDeploymentTypeDef",
    "FleetUtilizationTypeDef",
    "GamePropertyTypeDef",
    "GameServerContainerDefinitionInputTypeDef",
    "GameServerContainerDefinitionTypeDef",
    "GameServerContainerGroupCountsTypeDef",
    "GameServerGroupAutoScalingPolicyTypeDef",
    "GameServerGroupTypeDef",
    "GameServerInstanceTypeDef",
    "GameServerTypeDef",
    "GameSessionConnectionInfoTypeDef",
    "GameSessionCreationLimitPolicyTypeDef",
    "GameSessionDetailTypeDef",
    "GameSessionPlacementTypeDef",
    "GameSessionQueueDestinationTypeDef",
    "GameSessionQueueTypeDef",
    "GameSessionTypeDef",
    "GetComputeAccessInputTypeDef",
    "GetComputeAccessOutputTypeDef",
    "GetComputeAuthTokenInputTypeDef",
    "GetComputeAuthTokenOutputTypeDef",
    "GetGameSessionLogUrlInputTypeDef",
    "GetGameSessionLogUrlOutputTypeDef",
    "GetInstanceAccessInputTypeDef",
    "GetInstanceAccessOutputTypeDef",
    "InstanceAccessTypeDef",
    "InstanceCredentialsTypeDef",
    "InstanceDefinitionTypeDef",
    "InstanceTypeDef",
    "IpPermissionTypeDef",
    "LaunchTemplateSpecificationTypeDef",
    "ListAliasesInputPaginateTypeDef",
    "ListAliasesInputTypeDef",
    "ListAliasesOutputTypeDef",
    "ListBuildsInputPaginateTypeDef",
    "ListBuildsInputTypeDef",
    "ListBuildsOutputTypeDef",
    "ListComputeInputPaginateTypeDef",
    "ListComputeInputTypeDef",
    "ListComputeOutputTypeDef",
    "ListContainerFleetsInputPaginateTypeDef",
    "ListContainerFleetsInputTypeDef",
    "ListContainerFleetsOutputTypeDef",
    "ListContainerGroupDefinitionVersionsInputPaginateTypeDef",
    "ListContainerGroupDefinitionVersionsInputTypeDef",
    "ListContainerGroupDefinitionVersionsOutputTypeDef",
    "ListContainerGroupDefinitionsInputPaginateTypeDef",
    "ListContainerGroupDefinitionsInputTypeDef",
    "ListContainerGroupDefinitionsOutputTypeDef",
    "ListFleetDeploymentsInputPaginateTypeDef",
    "ListFleetDeploymentsInputTypeDef",
    "ListFleetDeploymentsOutputTypeDef",
    "ListFleetsInputPaginateTypeDef",
    "ListFleetsInputTypeDef",
    "ListFleetsOutputTypeDef",
    "ListGameServerGroupsInputPaginateTypeDef",
    "ListGameServerGroupsInputTypeDef",
    "ListGameServerGroupsOutputTypeDef",
    "ListGameServersInputPaginateTypeDef",
    "ListGameServersInputTypeDef",
    "ListGameServersOutputTypeDef",
    "ListLocationsInputPaginateTypeDef",
    "ListLocationsInputTypeDef",
    "ListLocationsOutputTypeDef",
    "ListScriptsInputPaginateTypeDef",
    "ListScriptsInputTypeDef",
    "ListScriptsOutputTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LocationAttributesTypeDef",
    "LocationConfigurationTypeDef",
    "LocationModelTypeDef",
    "LocationStateTypeDef",
    "LocationalDeploymentTypeDef",
    "LogConfigurationTypeDef",
    "MatchedPlayerSessionTypeDef",
    "MatchmakingConfigurationTypeDef",
    "MatchmakingRuleSetTypeDef",
    "MatchmakingTicketTypeDef",
    "PaginatorConfigTypeDef",
    "PlacedPlayerSessionTypeDef",
    "PlayerLatencyPolicyTypeDef",
    "PlayerLatencyTypeDef",
    "PlayerOutputTypeDef",
    "PlayerSessionTypeDef",
    "PlayerTypeDef",
    "PlayerUnionTypeDef",
    "PriorityConfigurationOutputTypeDef",
    "PriorityConfigurationOverrideOutputTypeDef",
    "PriorityConfigurationOverrideTypeDef",
    "PriorityConfigurationOverrideUnionTypeDef",
    "PriorityConfigurationTypeDef",
    "PriorityConfigurationUnionTypeDef",
    "PutScalingPolicyInputTypeDef",
    "PutScalingPolicyOutputTypeDef",
    "RegisterComputeInputTypeDef",
    "RegisterComputeOutputTypeDef",
    "RegisterGameServerInputTypeDef",
    "RegisterGameServerOutputTypeDef",
    "RequestUploadCredentialsInputTypeDef",
    "RequestUploadCredentialsOutputTypeDef",
    "ResolveAliasInputTypeDef",
    "ResolveAliasOutputTypeDef",
    "ResourceCreationLimitPolicyTypeDef",
    "ResponseMetadataTypeDef",
    "ResumeGameServerGroupInputTypeDef",
    "ResumeGameServerGroupOutputTypeDef",
    "RoutingStrategyTypeDef",
    "RuntimeConfigurationOutputTypeDef",
    "RuntimeConfigurationTypeDef",
    "RuntimeConfigurationUnionTypeDef",
    "S3LocationTypeDef",
    "ScalingPolicyTypeDef",
    "ScriptTypeDef",
    "SearchGameSessionsInputPaginateTypeDef",
    "SearchGameSessionsInputTypeDef",
    "SearchGameSessionsOutputTypeDef",
    "ServerProcessTypeDef",
    "StartFleetActionsInputTypeDef",
    "StartFleetActionsOutputTypeDef",
    "StartGameSessionPlacementInputTypeDef",
    "StartGameSessionPlacementOutputTypeDef",
    "StartMatchBackfillInputTypeDef",
    "StartMatchBackfillOutputTypeDef",
    "StartMatchmakingInputTypeDef",
    "StartMatchmakingOutputTypeDef",
    "StopFleetActionsInputTypeDef",
    "StopFleetActionsOutputTypeDef",
    "StopGameSessionPlacementInputTypeDef",
    "StopGameSessionPlacementOutputTypeDef",
    "StopMatchmakingInputTypeDef",
    "SupportContainerDefinitionInputTypeDef",
    "SupportContainerDefinitionTypeDef",
    "SuspendGameServerGroupInputTypeDef",
    "SuspendGameServerGroupOutputTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TargetConfigurationTypeDef",
    "TargetTrackingConfigurationTypeDef",
    "TerminateGameSessionInputTypeDef",
    "TerminateGameSessionOutputTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAliasInputTypeDef",
    "UpdateAliasOutputTypeDef",
    "UpdateBuildInputTypeDef",
    "UpdateBuildOutputTypeDef",
    "UpdateContainerFleetInputTypeDef",
    "UpdateContainerFleetOutputTypeDef",
    "UpdateContainerGroupDefinitionInputTypeDef",
    "UpdateContainerGroupDefinitionOutputTypeDef",
    "UpdateFleetAttributesInputTypeDef",
    "UpdateFleetAttributesOutputTypeDef",
    "UpdateFleetCapacityInputTypeDef",
    "UpdateFleetCapacityOutputTypeDef",
    "UpdateFleetPortSettingsInputTypeDef",
    "UpdateFleetPortSettingsOutputTypeDef",
    "UpdateGameServerGroupInputTypeDef",
    "UpdateGameServerGroupOutputTypeDef",
    "UpdateGameServerInputTypeDef",
    "UpdateGameServerOutputTypeDef",
    "UpdateGameSessionInputTypeDef",
    "UpdateGameSessionOutputTypeDef",
    "UpdateGameSessionQueueInputTypeDef",
    "UpdateGameSessionQueueOutputTypeDef",
    "UpdateMatchmakingConfigurationInputTypeDef",
    "UpdateMatchmakingConfigurationOutputTypeDef",
    "UpdateRuntimeConfigurationInputTypeDef",
    "UpdateRuntimeConfigurationOutputTypeDef",
    "UpdateScriptInputTypeDef",
    "UpdateScriptOutputTypeDef",
    "ValidateMatchmakingRuleSetInputTypeDef",
    "ValidateMatchmakingRuleSetOutputTypeDef",
    "VpcPeeringAuthorizationTypeDef",
    "VpcPeeringConnectionStatusTypeDef",
    "VpcPeeringConnectionTypeDef",
)

class AcceptMatchInputTypeDef(TypedDict):
    TicketId: str
    PlayerIds: Sequence[str]
    AcceptanceType: AcceptanceTypeType

RoutingStrategyTypeDef = TypedDict(
    "RoutingStrategyTypeDef",
    {
        "Type": NotRequired[RoutingStrategyTypeType],
        "FleetId": NotRequired[str],
        "Message": NotRequired[str],
    },
)

class AnywhereConfigurationTypeDef(TypedDict):
    Cost: str

class AttributeValueOutputTypeDef(TypedDict):
    S: NotRequired[str]
    N: NotRequired[float]
    SL: NotRequired[List[str]]
    SDM: NotRequired[Dict[str, float]]

class AttributeValueTypeDef(TypedDict):
    S: NotRequired[str]
    N: NotRequired[float]
    SL: NotRequired[Sequence[str]]
    SDM: NotRequired[Mapping[str, float]]

class AwsCredentialsTypeDef(TypedDict):
    AccessKeyId: NotRequired[str]
    SecretAccessKey: NotRequired[str]
    SessionToken: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class BuildTypeDef(TypedDict):
    BuildId: NotRequired[str]
    BuildArn: NotRequired[str]
    Name: NotRequired[str]
    Version: NotRequired[str]
    Status: NotRequired[BuildStatusType]
    SizeOnDisk: NotRequired[int]
    OperatingSystem: NotRequired[OperatingSystemType]
    CreationTime: NotRequired[datetime]
    ServerSdkVersion: NotRequired[str]

class CertificateConfigurationTypeDef(TypedDict):
    CertificateType: CertificateTypeType

class ClaimFilterOptionTypeDef(TypedDict):
    InstanceStatuses: NotRequired[Sequence[FilterInstanceStatusType]]

class GameServerTypeDef(TypedDict):
    GameServerGroupName: NotRequired[str]
    GameServerGroupArn: NotRequired[str]
    GameServerId: NotRequired[str]
    InstanceId: NotRequired[str]
    ConnectionInfo: NotRequired[str]
    GameServerData: NotRequired[str]
    ClaimStatus: NotRequired[Literal["CLAIMED"]]
    UtilizationStatus: NotRequired[GameServerUtilizationStatusType]
    RegistrationTime: NotRequired[datetime]
    LastClaimTime: NotRequired[datetime]
    LastHealthCheckTime: NotRequired[datetime]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ContainerAttributeTypeDef(TypedDict):
    ContainerName: NotRequired[str]
    ContainerRuntimeId: NotRequired[str]

class ConnectionPortRangeTypeDef(TypedDict):
    FromPort: int
    ToPort: int

class ContainerDependencyTypeDef(TypedDict):
    ContainerName: str
    Condition: ContainerDependencyConditionType

class ContainerEnvironmentTypeDef(TypedDict):
    Name: str
    Value: str

class ContainerFleetLocationAttributesTypeDef(TypedDict):
    Location: NotRequired[str]
    Status: NotRequired[ContainerFleetLocationStatusType]

class DeploymentDetailsTypeDef(TypedDict):
    LatestDeploymentId: NotRequired[str]

class GameSessionCreationLimitPolicyTypeDef(TypedDict):
    NewGameSessionsPerCreator: NotRequired[int]
    PolicyPeriodInMinutes: NotRequired[int]

IpPermissionTypeDef = TypedDict(
    "IpPermissionTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
        "IpRange": str,
        "Protocol": IpProtocolType,
    },
)

class LogConfigurationTypeDef(TypedDict):
    LogDestination: NotRequired[LogDestinationType]
    S3BucketName: NotRequired[str]
    LogGroupArn: NotRequired[str]

class ContainerHealthCheckOutputTypeDef(TypedDict):
    Command: List[str]
    Interval: NotRequired[int]
    Retries: NotRequired[int]
    StartPeriod: NotRequired[int]
    Timeout: NotRequired[int]

class ContainerHealthCheckTypeDef(TypedDict):
    Command: Sequence[str]
    Interval: NotRequired[int]
    Retries: NotRequired[int]
    StartPeriod: NotRequired[int]
    Timeout: NotRequired[int]

class ContainerIdentifierTypeDef(TypedDict):
    ContainerName: NotRequired[str]
    ContainerRuntimeId: NotRequired[str]

class ContainerMountPointTypeDef(TypedDict):
    InstancePath: str
    ContainerPath: NotRequired[str]
    AccessLevel: NotRequired[ContainerMountPointAccessLevelType]

ContainerPortRangeTypeDef = TypedDict(
    "ContainerPortRangeTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
        "Protocol": IpProtocolType,
    },
)

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class S3LocationTypeDef(TypedDict):
    Bucket: NotRequired[str]
    Key: NotRequired[str]
    RoleArn: NotRequired[str]
    ObjectVersion: NotRequired[str]

class LocationConfigurationTypeDef(TypedDict):
    Location: str

class ResourceCreationLimitPolicyTypeDef(TypedDict):
    NewGameSessionsPerCreator: NotRequired[int]
    PolicyPeriodInMinutes: NotRequired[int]

class LocationStateTypeDef(TypedDict):
    Location: NotRequired[str]
    Status: NotRequired[FleetStatusType]

class InstanceDefinitionTypeDef(TypedDict):
    InstanceType: GameServerGroupInstanceTypeType
    WeightedCapacity: NotRequired[str]

class LaunchTemplateSpecificationTypeDef(TypedDict):
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    Version: NotRequired[str]

class GamePropertyTypeDef(TypedDict):
    Key: str
    Value: str

class GameSessionQueueDestinationTypeDef(TypedDict):
    DestinationArn: NotRequired[str]

class PlayerLatencyPolicyTypeDef(TypedDict):
    MaximumIndividualPlayerLatencyMilliseconds: NotRequired[int]
    PolicyDurationSeconds: NotRequired[int]

class LocationModelTypeDef(TypedDict):
    LocationName: NotRequired[str]
    LocationArn: NotRequired[str]

class MatchmakingRuleSetTypeDef(TypedDict):
    RuleSetBody: str
    RuleSetName: NotRequired[str]
    RuleSetArn: NotRequired[str]
    CreationTime: NotRequired[datetime]

class CreatePlayerSessionInputTypeDef(TypedDict):
    GameSessionId: str
    PlayerId: str
    PlayerData: NotRequired[str]

class PlayerSessionTypeDef(TypedDict):
    PlayerSessionId: NotRequired[str]
    PlayerId: NotRequired[str]
    GameSessionId: NotRequired[str]
    FleetId: NotRequired[str]
    FleetArn: NotRequired[str]
    CreationTime: NotRequired[datetime]
    TerminationTime: NotRequired[datetime]
    Status: NotRequired[PlayerSessionStatusType]
    IpAddress: NotRequired[str]
    DnsName: NotRequired[str]
    Port: NotRequired[int]
    PlayerData: NotRequired[str]

class CreatePlayerSessionsInputTypeDef(TypedDict):
    GameSessionId: str
    PlayerIds: Sequence[str]
    PlayerDataMap: NotRequired[Mapping[str, str]]

class CreateVpcPeeringAuthorizationInputTypeDef(TypedDict):
    GameLiftAwsAccountId: str
    PeerVpcId: str

class VpcPeeringAuthorizationTypeDef(TypedDict):
    GameLiftAwsAccountId: NotRequired[str]
    PeerVpcAwsAccountId: NotRequired[str]
    PeerVpcId: NotRequired[str]
    CreationTime: NotRequired[datetime]
    ExpirationTime: NotRequired[datetime]

class CreateVpcPeeringConnectionInputTypeDef(TypedDict):
    FleetId: str
    PeerVpcAwsAccountId: str
    PeerVpcId: str

class DeleteAliasInputTypeDef(TypedDict):
    AliasId: str

class DeleteBuildInputTypeDef(TypedDict):
    BuildId: str

class DeleteContainerFleetInputTypeDef(TypedDict):
    FleetId: str

class DeleteContainerGroupDefinitionInputTypeDef(TypedDict):
    Name: str
    VersionNumber: NotRequired[int]
    VersionCountToRetain: NotRequired[int]

class DeleteFleetInputTypeDef(TypedDict):
    FleetId: str

class DeleteFleetLocationsInputTypeDef(TypedDict):
    FleetId: str
    Locations: Sequence[str]

class DeleteGameServerGroupInputTypeDef(TypedDict):
    GameServerGroupName: str
    DeleteOption: NotRequired[GameServerGroupDeleteOptionType]

class DeleteGameSessionQueueInputTypeDef(TypedDict):
    Name: str

class DeleteLocationInputTypeDef(TypedDict):
    LocationName: str

class DeleteMatchmakingConfigurationInputTypeDef(TypedDict):
    Name: str

class DeleteMatchmakingRuleSetInputTypeDef(TypedDict):
    Name: str

class DeleteScalingPolicyInputTypeDef(TypedDict):
    Name: str
    FleetId: str

class DeleteScriptInputTypeDef(TypedDict):
    ScriptId: str

class DeleteVpcPeeringAuthorizationInputTypeDef(TypedDict):
    GameLiftAwsAccountId: str
    PeerVpcId: str

class DeleteVpcPeeringConnectionInputTypeDef(TypedDict):
    FleetId: str
    VpcPeeringConnectionId: str

class DeploymentConfigurationTypeDef(TypedDict):
    ProtectionStrategy: NotRequired[DeploymentProtectionStrategyType]
    MinimumHealthyPercentage: NotRequired[int]
    ImpairmentStrategy: NotRequired[DeploymentImpairmentStrategyType]

class DeregisterComputeInputTypeDef(TypedDict):
    FleetId: str
    ComputeName: str

class DeregisterGameServerInputTypeDef(TypedDict):
    GameServerGroupName: str
    GameServerId: str

class DescribeAliasInputTypeDef(TypedDict):
    AliasId: str

class DescribeBuildInputTypeDef(TypedDict):
    BuildId: str

class DescribeComputeInputTypeDef(TypedDict):
    FleetId: str
    ComputeName: str

class DescribeContainerFleetInputTypeDef(TypedDict):
    FleetId: str

class DescribeContainerGroupDefinitionInputTypeDef(TypedDict):
    Name: str
    VersionNumber: NotRequired[int]

class DescribeEC2InstanceLimitsInputTypeDef(TypedDict):
    EC2InstanceType: NotRequired[EC2InstanceTypeType]
    Location: NotRequired[str]

class EC2InstanceLimitTypeDef(TypedDict):
    EC2InstanceType: NotRequired[EC2InstanceTypeType]
    CurrentInstances: NotRequired[int]
    InstanceLimit: NotRequired[int]
    Location: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeFleetAttributesInputTypeDef(TypedDict):
    FleetIds: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeFleetCapacityInputTypeDef(TypedDict):
    FleetIds: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeFleetDeploymentInputTypeDef(TypedDict):
    FleetId: str
    DeploymentId: NotRequired[str]

class LocationalDeploymentTypeDef(TypedDict):
    DeploymentStatus: NotRequired[DeploymentStatusType]

TimestampTypeDef = Union[datetime, str]

class EventTypeDef(TypedDict):
    EventId: NotRequired[str]
    ResourceId: NotRequired[str]
    EventCode: NotRequired[EventCodeType]
    Message: NotRequired[str]
    EventTime: NotRequired[datetime]
    PreSignedLogUrl: NotRequired[str]
    Count: NotRequired[int]

class DescribeFleetLocationAttributesInputTypeDef(TypedDict):
    FleetId: str
    Locations: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeFleetLocationCapacityInputTypeDef(TypedDict):
    FleetId: str
    Location: str

class DescribeFleetLocationUtilizationInputTypeDef(TypedDict):
    FleetId: str
    Location: str

class FleetUtilizationTypeDef(TypedDict):
    FleetId: NotRequired[str]
    FleetArn: NotRequired[str]
    ActiveServerProcessCount: NotRequired[int]
    ActiveGameSessionCount: NotRequired[int]
    CurrentPlayerSessionCount: NotRequired[int]
    MaximumPlayerSessionCount: NotRequired[int]
    Location: NotRequired[str]

class DescribeFleetPortSettingsInputTypeDef(TypedDict):
    FleetId: str
    Location: NotRequired[str]

class DescribeFleetUtilizationInputTypeDef(TypedDict):
    FleetIds: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeGameServerGroupInputTypeDef(TypedDict):
    GameServerGroupName: str

class DescribeGameServerInputTypeDef(TypedDict):
    GameServerGroupName: str
    GameServerId: str

class DescribeGameServerInstancesInputTypeDef(TypedDict):
    GameServerGroupName: str
    InstanceIds: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class GameServerInstanceTypeDef(TypedDict):
    GameServerGroupName: NotRequired[str]
    GameServerGroupArn: NotRequired[str]
    InstanceId: NotRequired[str]
    InstanceStatus: NotRequired[GameServerInstanceStatusType]

class DescribeGameSessionDetailsInputTypeDef(TypedDict):
    FleetId: NotRequired[str]
    GameSessionId: NotRequired[str]
    AliasId: NotRequired[str]
    Location: NotRequired[str]
    StatusFilter: NotRequired[str]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeGameSessionPlacementInputTypeDef(TypedDict):
    PlacementId: str

class DescribeGameSessionQueuesInputTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeGameSessionsInputTypeDef(TypedDict):
    FleetId: NotRequired[str]
    GameSessionId: NotRequired[str]
    AliasId: NotRequired[str]
    Location: NotRequired[str]
    StatusFilter: NotRequired[str]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeInstancesInputTypeDef(TypedDict):
    FleetId: str
    InstanceId: NotRequired[str]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]
    Location: NotRequired[str]

InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "FleetId": NotRequired[str],
        "FleetArn": NotRequired[str],
        "InstanceId": NotRequired[str],
        "IpAddress": NotRequired[str],
        "DnsName": NotRequired[str],
        "OperatingSystem": NotRequired[OperatingSystemType],
        "Type": NotRequired[EC2InstanceTypeType],
        "Status": NotRequired[InstanceStatusType],
        "CreationTime": NotRequired[datetime],
        "Location": NotRequired[str],
    },
)

class DescribeMatchmakingConfigurationsInputTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    RuleSetName: NotRequired[str]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeMatchmakingInputTypeDef(TypedDict):
    TicketIds: Sequence[str]

class DescribeMatchmakingRuleSetsInputTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class DescribePlayerSessionsInputTypeDef(TypedDict):
    GameSessionId: NotRequired[str]
    PlayerId: NotRequired[str]
    PlayerSessionId: NotRequired[str]
    PlayerSessionStatusFilter: NotRequired[str]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeRuntimeConfigurationInputTypeDef(TypedDict):
    FleetId: str

class DescribeScalingPoliciesInputTypeDef(TypedDict):
    FleetId: str
    StatusFilter: NotRequired[ScalingStatusTypeType]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]
    Location: NotRequired[str]

class DescribeScriptInputTypeDef(TypedDict):
    ScriptId: str

class DescribeVpcPeeringConnectionsInputTypeDef(TypedDict):
    FleetId: NotRequired[str]

class DesiredPlayerSessionTypeDef(TypedDict):
    PlayerId: NotRequired[str]
    PlayerData: NotRequired[str]

class EC2InstanceCountsTypeDef(TypedDict):
    DESIRED: NotRequired[int]
    MINIMUM: NotRequired[int]
    MAXIMUM: NotRequired[int]
    PENDING: NotRequired[int]
    ACTIVE: NotRequired[int]
    IDLE: NotRequired[int]
    TERMINATING: NotRequired[int]

class FilterConfigurationOutputTypeDef(TypedDict):
    AllowedLocations: NotRequired[List[str]]

class FilterConfigurationTypeDef(TypedDict):
    AllowedLocations: NotRequired[Sequence[str]]

class GameServerContainerGroupCountsTypeDef(TypedDict):
    PENDING: NotRequired[int]
    ACTIVE: NotRequired[int]
    IDLE: NotRequired[int]
    TERMINATING: NotRequired[int]

class TargetTrackingConfigurationTypeDef(TypedDict):
    TargetValue: float

class MatchedPlayerSessionTypeDef(TypedDict):
    PlayerId: NotRequired[str]
    PlayerSessionId: NotRequired[str]

class PlacedPlayerSessionTypeDef(TypedDict):
    PlayerId: NotRequired[str]
    PlayerSessionId: NotRequired[str]

class PlayerLatencyTypeDef(TypedDict):
    PlayerId: NotRequired[str]
    RegionIdentifier: NotRequired[str]
    LatencyInMilliseconds: NotRequired[float]

class PriorityConfigurationOverrideOutputTypeDef(TypedDict):
    LocationOrder: List[str]
    PlacementFallbackStrategy: NotRequired[PlacementFallbackStrategyType]

class PriorityConfigurationOutputTypeDef(TypedDict):
    PriorityOrder: NotRequired[List[PriorityTypeType]]
    LocationOrder: NotRequired[List[str]]

class GetComputeAccessInputTypeDef(TypedDict):
    FleetId: str
    ComputeName: str

class GetComputeAuthTokenInputTypeDef(TypedDict):
    FleetId: str
    ComputeName: str

class GetGameSessionLogUrlInputTypeDef(TypedDict):
    GameSessionId: str

class GetInstanceAccessInputTypeDef(TypedDict):
    FleetId: str
    InstanceId: str

class InstanceCredentialsTypeDef(TypedDict):
    UserName: NotRequired[str]
    Secret: NotRequired[str]

class ListAliasesInputTypeDef(TypedDict):
    RoutingStrategyType: NotRequired[RoutingStrategyTypeType]
    Name: NotRequired[str]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListBuildsInputTypeDef(TypedDict):
    Status: NotRequired[BuildStatusType]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListComputeInputTypeDef(TypedDict):
    FleetId: str
    Location: NotRequired[str]
    ContainerGroupDefinitionName: NotRequired[str]
    ComputeStatus: NotRequired[ListComputeInputStatusType]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListContainerFleetsInputTypeDef(TypedDict):
    ContainerGroupDefinitionName: NotRequired[str]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListContainerGroupDefinitionVersionsInputTypeDef(TypedDict):
    Name: str
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListContainerGroupDefinitionsInputTypeDef(TypedDict):
    ContainerGroupType: NotRequired[ContainerGroupTypeType]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListFleetDeploymentsInputTypeDef(TypedDict):
    FleetId: NotRequired[str]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListFleetsInputTypeDef(TypedDict):
    BuildId: NotRequired[str]
    ScriptId: NotRequired[str]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListGameServerGroupsInputTypeDef(TypedDict):
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListGameServersInputTypeDef(TypedDict):
    GameServerGroupName: str
    SortOrder: NotRequired[SortOrderType]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListLocationsInputTypeDef(TypedDict):
    Filters: NotRequired[Sequence[LocationFilterType]]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListScriptsInputTypeDef(TypedDict):
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceARN: str

class PriorityConfigurationOverrideTypeDef(TypedDict):
    LocationOrder: Sequence[str]
    PlacementFallbackStrategy: NotRequired[PlacementFallbackStrategyType]

class PriorityConfigurationTypeDef(TypedDict):
    PriorityOrder: NotRequired[Sequence[PriorityTypeType]]
    LocationOrder: NotRequired[Sequence[str]]

class TargetConfigurationTypeDef(TypedDict):
    TargetValue: float

class RegisterComputeInputTypeDef(TypedDict):
    FleetId: str
    ComputeName: str
    CertificatePath: NotRequired[str]
    DnsName: NotRequired[str]
    IpAddress: NotRequired[str]
    Location: NotRequired[str]

class RegisterGameServerInputTypeDef(TypedDict):
    GameServerGroupName: str
    GameServerId: str
    InstanceId: str
    ConnectionInfo: NotRequired[str]
    GameServerData: NotRequired[str]

class RequestUploadCredentialsInputTypeDef(TypedDict):
    BuildId: str

class ResolveAliasInputTypeDef(TypedDict):
    AliasId: str

class ResumeGameServerGroupInputTypeDef(TypedDict):
    GameServerGroupName: str
    ResumeActions: Sequence[Literal["REPLACE_INSTANCE_TYPES"]]

class ServerProcessTypeDef(TypedDict):
    LaunchPath: str
    ConcurrentExecutions: int
    Parameters: NotRequired[str]

class SearchGameSessionsInputTypeDef(TypedDict):
    FleetId: NotRequired[str]
    AliasId: NotRequired[str]
    Location: NotRequired[str]
    FilterExpression: NotRequired[str]
    SortExpression: NotRequired[str]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class StartFleetActionsInputTypeDef(TypedDict):
    FleetId: str
    Actions: Sequence[Literal["AUTO_SCALING"]]
    Location: NotRequired[str]

class StopFleetActionsInputTypeDef(TypedDict):
    FleetId: str
    Actions: Sequence[Literal["AUTO_SCALING"]]
    Location: NotRequired[str]

class StopGameSessionPlacementInputTypeDef(TypedDict):
    PlacementId: str

class StopMatchmakingInputTypeDef(TypedDict):
    TicketId: str

class SuspendGameServerGroupInputTypeDef(TypedDict):
    GameServerGroupName: str
    SuspendActions: Sequence[Literal["REPLACE_INSTANCE_TYPES"]]

class TerminateGameSessionInputTypeDef(TypedDict):
    GameSessionId: str
    TerminationMode: TerminationModeType

class UntagResourceRequestTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]

class UpdateBuildInputTypeDef(TypedDict):
    BuildId: str
    Name: NotRequired[str]
    Version: NotRequired[str]

class UpdateFleetCapacityInputTypeDef(TypedDict):
    FleetId: str
    DesiredInstances: NotRequired[int]
    MinSize: NotRequired[int]
    MaxSize: NotRequired[int]
    Location: NotRequired[str]

class UpdateGameServerInputTypeDef(TypedDict):
    GameServerGroupName: str
    GameServerId: str
    GameServerData: NotRequired[str]
    UtilizationStatus: NotRequired[GameServerUtilizationStatusType]
    HealthCheck: NotRequired[Literal["HEALTHY"]]

class ValidateMatchmakingRuleSetInputTypeDef(TypedDict):
    RuleSetBody: str

class VpcPeeringConnectionStatusTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]

class AliasTypeDef(TypedDict):
    AliasId: NotRequired[str]
    Name: NotRequired[str]
    AliasArn: NotRequired[str]
    Description: NotRequired[str]
    RoutingStrategy: NotRequired[RoutingStrategyTypeDef]
    CreationTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]

class UpdateAliasInputTypeDef(TypedDict):
    AliasId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    RoutingStrategy: NotRequired[RoutingStrategyTypeDef]

class PlayerOutputTypeDef(TypedDict):
    PlayerId: NotRequired[str]
    PlayerAttributes: NotRequired[Dict[str, AttributeValueOutputTypeDef]]
    Team: NotRequired[str]
    LatencyInMs: NotRequired[Dict[str, int]]

AttributeValueUnionTypeDef = Union[AttributeValueTypeDef, AttributeValueOutputTypeDef]

class ClaimGameServerInputTypeDef(TypedDict):
    GameServerGroupName: str
    GameServerId: NotRequired[str]
    GameServerData: NotRequired[str]
    FilterOption: NotRequired[ClaimFilterOptionTypeDef]

class ClaimGameServerOutputTypeDef(TypedDict):
    GameServer: GameServerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeBuildOutputTypeDef(TypedDict):
    Build: BuildTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeGameServerOutputTypeDef(TypedDict):
    GameServer: GameServerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetComputeAuthTokenOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    ComputeName: str
    ComputeArn: str
    AuthToken: str
    ExpirationTimestamp: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetGameSessionLogUrlOutputTypeDef(TypedDict):
    PreSignedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListBuildsOutputTypeDef(TypedDict):
    Builds: List[BuildTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListFleetsOutputTypeDef(TypedDict):
    FleetIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListGameServersOutputTypeDef(TypedDict):
    GameServers: List[GameServerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PutScalingPolicyOutputTypeDef(TypedDict):
    Name: str
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterGameServerOutputTypeDef(TypedDict):
    GameServer: GameServerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ResolveAliasOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartFleetActionsOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class StopFleetActionsOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBuildOutputTypeDef(TypedDict):
    Build: BuildTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFleetAttributesOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFleetCapacityOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFleetPortSettingsOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGameServerOutputTypeDef(TypedDict):
    GameServer: GameServerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ValidateMatchmakingRuleSetOutputTypeDef(TypedDict):
    Valid: bool
    ResponseMetadata: ResponseMetadataTypeDef

ComputeTypeDef = TypedDict(
    "ComputeTypeDef",
    {
        "FleetId": NotRequired[str],
        "FleetArn": NotRequired[str],
        "ComputeName": NotRequired[str],
        "ComputeArn": NotRequired[str],
        "IpAddress": NotRequired[str],
        "DnsName": NotRequired[str],
        "ComputeStatus": NotRequired[ComputeStatusType],
        "Location": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "OperatingSystem": NotRequired[OperatingSystemType],
        "Type": NotRequired[EC2InstanceTypeType],
        "GameLiftServiceSdkEndpoint": NotRequired[str],
        "GameLiftAgentEndpoint": NotRequired[str],
        "InstanceId": NotRequired[str],
        "ContainerAttributes": NotRequired[List[ContainerAttributeTypeDef]],
        "GameServerContainerGroupDefinitionArn": NotRequired[str],
    },
)

class DescribeFleetPortSettingsOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    InboundPermissions: List[IpPermissionTypeDef]
    UpdateStatus: Literal["PENDING_UPDATE"]
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateFleetPortSettingsInputTypeDef(TypedDict):
    FleetId: str
    InboundPermissionAuthorizations: NotRequired[Sequence[IpPermissionTypeDef]]
    InboundPermissionRevocations: NotRequired[Sequence[IpPermissionTypeDef]]

class ContainerFleetTypeDef(TypedDict):
    FleetId: NotRequired[str]
    FleetArn: NotRequired[str]
    FleetRoleArn: NotRequired[str]
    GameServerContainerGroupDefinitionName: NotRequired[str]
    GameServerContainerGroupDefinitionArn: NotRequired[str]
    PerInstanceContainerGroupDefinitionName: NotRequired[str]
    PerInstanceContainerGroupDefinitionArn: NotRequired[str]
    InstanceConnectionPortRange: NotRequired[ConnectionPortRangeTypeDef]
    InstanceInboundPermissions: NotRequired[List[IpPermissionTypeDef]]
    GameServerContainerGroupsPerInstance: NotRequired[int]
    MaximumGameServerContainerGroupsPerInstance: NotRequired[int]
    InstanceType: NotRequired[str]
    BillingType: NotRequired[ContainerFleetBillingTypeType]
    Description: NotRequired[str]
    CreationTime: NotRequired[datetime]
    MetricGroups: NotRequired[List[str]]
    NewGameSessionProtectionPolicy: NotRequired[ProtectionPolicyType]
    GameSessionCreationLimitPolicy: NotRequired[GameSessionCreationLimitPolicyTypeDef]
    Status: NotRequired[ContainerFleetStatusType]
    DeploymentDetails: NotRequired[DeploymentDetailsTypeDef]
    LogConfiguration: NotRequired[LogConfigurationTypeDef]
    LocationAttributes: NotRequired[List[ContainerFleetLocationAttributesTypeDef]]

ContainerHealthCheckUnionTypeDef = Union[
    ContainerHealthCheckTypeDef, ContainerHealthCheckOutputTypeDef
]

class GetComputeAccessOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    ComputeName: str
    ComputeArn: str
    Credentials: AwsCredentialsTypeDef
    Target: str
    ContainerIdentifiers: List[ContainerIdentifierTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ContainerPortConfigurationOutputTypeDef(TypedDict):
    ContainerPortRanges: List[ContainerPortRangeTypeDef]

class ContainerPortConfigurationTypeDef(TypedDict):
    ContainerPortRanges: Sequence[ContainerPortRangeTypeDef]

class CreateAliasInputTypeDef(TypedDict):
    Name: str
    RoutingStrategy: RoutingStrategyTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateLocationInputTypeDef(TypedDict):
    LocationName: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateMatchmakingRuleSetInputTypeDef(TypedDict):
    Name: str
    RuleSetBody: str
    Tags: NotRequired[Sequence[TagTypeDef]]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestTypeDef(TypedDict):
    ResourceARN: str
    Tags: Sequence[TagTypeDef]

class CreateBuildInputTypeDef(TypedDict):
    Name: NotRequired[str]
    Version: NotRequired[str]
    StorageLocation: NotRequired[S3LocationTypeDef]
    OperatingSystem: NotRequired[OperatingSystemType]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ServerSdkVersion: NotRequired[str]

class CreateBuildOutputTypeDef(TypedDict):
    Build: BuildTypeDef
    UploadCredentials: AwsCredentialsTypeDef
    StorageLocation: S3LocationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateScriptInputTypeDef(TypedDict):
    Name: NotRequired[str]
    Version: NotRequired[str]
    StorageLocation: NotRequired[S3LocationTypeDef]
    ZipFile: NotRequired[BlobTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class RequestUploadCredentialsOutputTypeDef(TypedDict):
    UploadCredentials: AwsCredentialsTypeDef
    StorageLocation: S3LocationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ScriptTypeDef(TypedDict):
    ScriptId: NotRequired[str]
    ScriptArn: NotRequired[str]
    Name: NotRequired[str]
    Version: NotRequired[str]
    SizeOnDisk: NotRequired[int]
    CreationTime: NotRequired[datetime]
    StorageLocation: NotRequired[S3LocationTypeDef]

class UpdateScriptInputTypeDef(TypedDict):
    ScriptId: str
    Name: NotRequired[str]
    Version: NotRequired[str]
    StorageLocation: NotRequired[S3LocationTypeDef]
    ZipFile: NotRequired[BlobTypeDef]

class CreateContainerFleetInputTypeDef(TypedDict):
    FleetRoleArn: str
    Description: NotRequired[str]
    GameServerContainerGroupDefinitionName: NotRequired[str]
    PerInstanceContainerGroupDefinitionName: NotRequired[str]
    InstanceConnectionPortRange: NotRequired[ConnectionPortRangeTypeDef]
    InstanceInboundPermissions: NotRequired[Sequence[IpPermissionTypeDef]]
    GameServerContainerGroupsPerInstance: NotRequired[int]
    InstanceType: NotRequired[str]
    BillingType: NotRequired[ContainerFleetBillingTypeType]
    Locations: NotRequired[Sequence[LocationConfigurationTypeDef]]
    MetricGroups: NotRequired[Sequence[str]]
    NewGameSessionProtectionPolicy: NotRequired[ProtectionPolicyType]
    GameSessionCreationLimitPolicy: NotRequired[GameSessionCreationLimitPolicyTypeDef]
    LogConfiguration: NotRequired[LogConfigurationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]

class CreateFleetLocationsInputTypeDef(TypedDict):
    FleetId: str
    Locations: Sequence[LocationConfigurationTypeDef]

class FleetAttributesTypeDef(TypedDict):
    FleetId: NotRequired[str]
    FleetArn: NotRequired[str]
    FleetType: NotRequired[FleetTypeType]
    InstanceType: NotRequired[EC2InstanceTypeType]
    Description: NotRequired[str]
    Name: NotRequired[str]
    CreationTime: NotRequired[datetime]
    TerminationTime: NotRequired[datetime]
    Status: NotRequired[FleetStatusType]
    BuildId: NotRequired[str]
    BuildArn: NotRequired[str]
    ScriptId: NotRequired[str]
    ScriptArn: NotRequired[str]
    ServerLaunchPath: NotRequired[str]
    ServerLaunchParameters: NotRequired[str]
    LogPaths: NotRequired[List[str]]
    NewGameSessionProtectionPolicy: NotRequired[ProtectionPolicyType]
    OperatingSystem: NotRequired[OperatingSystemType]
    ResourceCreationLimitPolicy: NotRequired[ResourceCreationLimitPolicyTypeDef]
    MetricGroups: NotRequired[List[str]]
    StoppedActions: NotRequired[List[Literal["AUTO_SCALING"]]]
    InstanceRoleArn: NotRequired[str]
    CertificateConfiguration: NotRequired[CertificateConfigurationTypeDef]
    ComputeType: NotRequired[ComputeTypeType]
    AnywhereConfiguration: NotRequired[AnywhereConfigurationTypeDef]
    InstanceRoleCredentialsProvider: NotRequired[Literal["SHARED_CREDENTIAL_FILE"]]

class UpdateFleetAttributesInputTypeDef(TypedDict):
    FleetId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    NewGameSessionProtectionPolicy: NotRequired[ProtectionPolicyType]
    ResourceCreationLimitPolicy: NotRequired[ResourceCreationLimitPolicyTypeDef]
    MetricGroups: NotRequired[Sequence[str]]
    AnywhereConfiguration: NotRequired[AnywhereConfigurationTypeDef]

class CreateFleetLocationsOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    LocationStates: List[LocationStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteFleetLocationsOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    LocationStates: List[LocationStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class LocationAttributesTypeDef(TypedDict):
    LocationState: NotRequired[LocationStateTypeDef]
    StoppedActions: NotRequired[List[Literal["AUTO_SCALING"]]]
    UpdateStatus: NotRequired[Literal["PENDING_UPDATE"]]

class GameServerGroupTypeDef(TypedDict):
    GameServerGroupName: NotRequired[str]
    GameServerGroupArn: NotRequired[str]
    RoleArn: NotRequired[str]
    InstanceDefinitions: NotRequired[List[InstanceDefinitionTypeDef]]
    BalancingStrategy: NotRequired[BalancingStrategyType]
    GameServerProtectionPolicy: NotRequired[GameServerProtectionPolicyType]
    AutoScalingGroupArn: NotRequired[str]
    Status: NotRequired[GameServerGroupStatusType]
    StatusReason: NotRequired[str]
    SuspendedActions: NotRequired[List[Literal["REPLACE_INSTANCE_TYPES"]]]
    CreationTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]

class UpdateGameServerGroupInputTypeDef(TypedDict):
    GameServerGroupName: str
    RoleArn: NotRequired[str]
    InstanceDefinitions: NotRequired[Sequence[InstanceDefinitionTypeDef]]
    GameServerProtectionPolicy: NotRequired[GameServerProtectionPolicyType]
    BalancingStrategy: NotRequired[BalancingStrategyType]

class CreateGameSessionInputTypeDef(TypedDict):
    MaximumPlayerSessionCount: int
    FleetId: NotRequired[str]
    AliasId: NotRequired[str]
    Name: NotRequired[str]
    GameProperties: NotRequired[Sequence[GamePropertyTypeDef]]
    CreatorId: NotRequired[str]
    GameSessionId: NotRequired[str]
    IdempotencyToken: NotRequired[str]
    GameSessionData: NotRequired[str]
    Location: NotRequired[str]

class CreateMatchmakingConfigurationInputTypeDef(TypedDict):
    Name: str
    RequestTimeoutSeconds: int
    AcceptanceRequired: bool
    RuleSetName: str
    Description: NotRequired[str]
    GameSessionQueueArns: NotRequired[Sequence[str]]
    AcceptanceTimeoutSeconds: NotRequired[int]
    NotificationTarget: NotRequired[str]
    AdditionalPlayerCount: NotRequired[int]
    CustomEventData: NotRequired[str]
    GameProperties: NotRequired[Sequence[GamePropertyTypeDef]]
    GameSessionData: NotRequired[str]
    BackfillMode: NotRequired[BackfillModeType]
    FlexMatchMode: NotRequired[FlexMatchModeType]
    Tags: NotRequired[Sequence[TagTypeDef]]

class GameSessionTypeDef(TypedDict):
    GameSessionId: NotRequired[str]
    Name: NotRequired[str]
    FleetId: NotRequired[str]
    FleetArn: NotRequired[str]
    CreationTime: NotRequired[datetime]
    TerminationTime: NotRequired[datetime]
    CurrentPlayerSessionCount: NotRequired[int]
    MaximumPlayerSessionCount: NotRequired[int]
    Status: NotRequired[GameSessionStatusType]
    StatusReason: NotRequired[GameSessionStatusReasonType]
    GameProperties: NotRequired[List[GamePropertyTypeDef]]
    IpAddress: NotRequired[str]
    DnsName: NotRequired[str]
    Port: NotRequired[int]
    PlayerSessionCreationPolicy: NotRequired[PlayerSessionCreationPolicyType]
    CreatorId: NotRequired[str]
    GameSessionData: NotRequired[str]
    MatchmakerData: NotRequired[str]
    Location: NotRequired[str]

class MatchmakingConfigurationTypeDef(TypedDict):
    Name: NotRequired[str]
    ConfigurationArn: NotRequired[str]
    Description: NotRequired[str]
    GameSessionQueueArns: NotRequired[List[str]]
    RequestTimeoutSeconds: NotRequired[int]
    AcceptanceTimeoutSeconds: NotRequired[int]
    AcceptanceRequired: NotRequired[bool]
    RuleSetName: NotRequired[str]
    RuleSetArn: NotRequired[str]
    NotificationTarget: NotRequired[str]
    AdditionalPlayerCount: NotRequired[int]
    CustomEventData: NotRequired[str]
    CreationTime: NotRequired[datetime]
    GameProperties: NotRequired[List[GamePropertyTypeDef]]
    GameSessionData: NotRequired[str]
    BackfillMode: NotRequired[BackfillModeType]
    FlexMatchMode: NotRequired[FlexMatchModeType]

class UpdateGameSessionInputTypeDef(TypedDict):
    GameSessionId: str
    MaximumPlayerSessionCount: NotRequired[int]
    Name: NotRequired[str]
    PlayerSessionCreationPolicy: NotRequired[PlayerSessionCreationPolicyType]
    ProtectionPolicy: NotRequired[ProtectionPolicyType]
    GameProperties: NotRequired[Sequence[GamePropertyTypeDef]]

class UpdateMatchmakingConfigurationInputTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    GameSessionQueueArns: NotRequired[Sequence[str]]
    RequestTimeoutSeconds: NotRequired[int]
    AcceptanceTimeoutSeconds: NotRequired[int]
    AcceptanceRequired: NotRequired[bool]
    RuleSetName: NotRequired[str]
    NotificationTarget: NotRequired[str]
    AdditionalPlayerCount: NotRequired[int]
    CustomEventData: NotRequired[str]
    GameProperties: NotRequired[Sequence[GamePropertyTypeDef]]
    GameSessionData: NotRequired[str]
    BackfillMode: NotRequired[BackfillModeType]
    FlexMatchMode: NotRequired[FlexMatchModeType]

class CreateLocationOutputTypeDef(TypedDict):
    Location: LocationModelTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListLocationsOutputTypeDef(TypedDict):
    Locations: List[LocationModelTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateMatchmakingRuleSetOutputTypeDef(TypedDict):
    RuleSet: MatchmakingRuleSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeMatchmakingRuleSetsOutputTypeDef(TypedDict):
    RuleSets: List[MatchmakingRuleSetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreatePlayerSessionOutputTypeDef(TypedDict):
    PlayerSession: PlayerSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePlayerSessionsOutputTypeDef(TypedDict):
    PlayerSessions: List[PlayerSessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePlayerSessionsOutputTypeDef(TypedDict):
    PlayerSessions: List[PlayerSessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateVpcPeeringAuthorizationOutputTypeDef(TypedDict):
    VpcPeeringAuthorization: VpcPeeringAuthorizationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeVpcPeeringAuthorizationsOutputTypeDef(TypedDict):
    VpcPeeringAuthorizations: List[VpcPeeringAuthorizationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class FleetDeploymentTypeDef(TypedDict):
    DeploymentId: NotRequired[str]
    FleetId: NotRequired[str]
    GameServerBinaryArn: NotRequired[str]
    RollbackGameServerBinaryArn: NotRequired[str]
    PerInstanceBinaryArn: NotRequired[str]
    RollbackPerInstanceBinaryArn: NotRequired[str]
    DeploymentStatus: NotRequired[DeploymentStatusType]
    DeploymentConfiguration: NotRequired[DeploymentConfigurationTypeDef]
    CreationTime: NotRequired[datetime]

class UpdateContainerFleetInputTypeDef(TypedDict):
    FleetId: str
    GameServerContainerGroupDefinitionName: NotRequired[str]
    PerInstanceContainerGroupDefinitionName: NotRequired[str]
    GameServerContainerGroupsPerInstance: NotRequired[int]
    InstanceConnectionPortRange: NotRequired[ConnectionPortRangeTypeDef]
    InstanceInboundPermissionAuthorizations: NotRequired[Sequence[IpPermissionTypeDef]]
    InstanceInboundPermissionRevocations: NotRequired[Sequence[IpPermissionTypeDef]]
    DeploymentConfiguration: NotRequired[DeploymentConfigurationTypeDef]
    Description: NotRequired[str]
    MetricGroups: NotRequired[Sequence[str]]
    NewGameSessionProtectionPolicy: NotRequired[ProtectionPolicyType]
    GameSessionCreationLimitPolicy: NotRequired[GameSessionCreationLimitPolicyTypeDef]
    LogConfiguration: NotRequired[LogConfigurationTypeDef]
    RemoveAttributes: NotRequired[Sequence[Literal["PER_INSTANCE_CONTAINER_GROUP_DEFINITION"]]]

class DescribeEC2InstanceLimitsOutputTypeDef(TypedDict):
    EC2InstanceLimits: List[EC2InstanceLimitTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeFleetAttributesInputPaginateTypeDef(TypedDict):
    FleetIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeFleetCapacityInputPaginateTypeDef(TypedDict):
    FleetIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeFleetUtilizationInputPaginateTypeDef(TypedDict):
    FleetIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeGameServerInstancesInputPaginateTypeDef(TypedDict):
    GameServerGroupName: str
    InstanceIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeGameSessionDetailsInputPaginateTypeDef(TypedDict):
    FleetId: NotRequired[str]
    GameSessionId: NotRequired[str]
    AliasId: NotRequired[str]
    Location: NotRequired[str]
    StatusFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeGameSessionQueuesInputPaginateTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeGameSessionsInputPaginateTypeDef(TypedDict):
    FleetId: NotRequired[str]
    GameSessionId: NotRequired[str]
    AliasId: NotRequired[str]
    Location: NotRequired[str]
    StatusFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeInstancesInputPaginateTypeDef(TypedDict):
    FleetId: str
    InstanceId: NotRequired[str]
    Location: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeMatchmakingConfigurationsInputPaginateTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    RuleSetName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeMatchmakingRuleSetsInputPaginateTypeDef(TypedDict):
    Names: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribePlayerSessionsInputPaginateTypeDef(TypedDict):
    GameSessionId: NotRequired[str]
    PlayerId: NotRequired[str]
    PlayerSessionId: NotRequired[str]
    PlayerSessionStatusFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeScalingPoliciesInputPaginateTypeDef(TypedDict):
    FleetId: str
    StatusFilter: NotRequired[ScalingStatusTypeType]
    Location: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAliasesInputPaginateTypeDef(TypedDict):
    RoutingStrategyType: NotRequired[RoutingStrategyTypeType]
    Name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListBuildsInputPaginateTypeDef(TypedDict):
    Status: NotRequired[BuildStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListComputeInputPaginateTypeDef(TypedDict):
    FleetId: str
    Location: NotRequired[str]
    ContainerGroupDefinitionName: NotRequired[str]
    ComputeStatus: NotRequired[ListComputeInputStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListContainerFleetsInputPaginateTypeDef(TypedDict):
    ContainerGroupDefinitionName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListContainerGroupDefinitionVersionsInputPaginateTypeDef(TypedDict):
    Name: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListContainerGroupDefinitionsInputPaginateTypeDef(TypedDict):
    ContainerGroupType: NotRequired[ContainerGroupTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFleetDeploymentsInputPaginateTypeDef(TypedDict):
    FleetId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFleetsInputPaginateTypeDef(TypedDict):
    BuildId: NotRequired[str]
    ScriptId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGameServerGroupsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGameServersInputPaginateTypeDef(TypedDict):
    GameServerGroupName: str
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLocationsInputPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[LocationFilterType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListScriptsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchGameSessionsInputPaginateTypeDef(TypedDict):
    FleetId: NotRequired[str]
    AliasId: NotRequired[str]
    Location: NotRequired[str]
    FilterExpression: NotRequired[str]
    SortExpression: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeFleetEventsInputPaginateTypeDef(TypedDict):
    FleetId: str
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeFleetEventsInputTypeDef(TypedDict):
    FleetId: str
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Limit: NotRequired[int]
    NextToken: NotRequired[str]

class DescribeFleetEventsOutputTypeDef(TypedDict):
    Events: List[EventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeFleetLocationUtilizationOutputTypeDef(TypedDict):
    FleetUtilization: FleetUtilizationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeFleetUtilizationOutputTypeDef(TypedDict):
    FleetUtilization: List[FleetUtilizationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeGameServerInstancesOutputTypeDef(TypedDict):
    GameServerInstances: List[GameServerInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeInstancesOutputTypeDef(TypedDict):
    Instances: List[InstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

FilterConfigurationUnionTypeDef = Union[
    FilterConfigurationTypeDef, FilterConfigurationOutputTypeDef
]

class FleetCapacityTypeDef(TypedDict):
    FleetId: NotRequired[str]
    FleetArn: NotRequired[str]
    InstanceType: NotRequired[EC2InstanceTypeType]
    InstanceCounts: NotRequired[EC2InstanceCountsTypeDef]
    Location: NotRequired[str]
    GameServerContainerGroupCounts: NotRequired[GameServerContainerGroupCountsTypeDef]

class GameServerGroupAutoScalingPolicyTypeDef(TypedDict):
    TargetTrackingConfiguration: TargetTrackingConfigurationTypeDef
    EstimatedInstanceWarmup: NotRequired[int]

class GameSessionConnectionInfoTypeDef(TypedDict):
    GameSessionArn: NotRequired[str]
    IpAddress: NotRequired[str]
    DnsName: NotRequired[str]
    Port: NotRequired[int]
    MatchedPlayerSessions: NotRequired[List[MatchedPlayerSessionTypeDef]]

class GameSessionPlacementTypeDef(TypedDict):
    PlacementId: NotRequired[str]
    GameSessionQueueName: NotRequired[str]
    Status: NotRequired[GameSessionPlacementStateType]
    GameProperties: NotRequired[List[GamePropertyTypeDef]]
    MaximumPlayerSessionCount: NotRequired[int]
    GameSessionName: NotRequired[str]
    GameSessionId: NotRequired[str]
    GameSessionArn: NotRequired[str]
    GameSessionRegion: NotRequired[str]
    PlayerLatencies: NotRequired[List[PlayerLatencyTypeDef]]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    IpAddress: NotRequired[str]
    DnsName: NotRequired[str]
    Port: NotRequired[int]
    PlacedPlayerSessions: NotRequired[List[PlacedPlayerSessionTypeDef]]
    GameSessionData: NotRequired[str]
    MatchmakerData: NotRequired[str]
    PriorityConfigurationOverride: NotRequired[PriorityConfigurationOverrideOutputTypeDef]

class GameSessionQueueTypeDef(TypedDict):
    Name: NotRequired[str]
    GameSessionQueueArn: NotRequired[str]
    TimeoutInSeconds: NotRequired[int]
    PlayerLatencyPolicies: NotRequired[List[PlayerLatencyPolicyTypeDef]]
    Destinations: NotRequired[List[GameSessionQueueDestinationTypeDef]]
    FilterConfiguration: NotRequired[FilterConfigurationOutputTypeDef]
    PriorityConfiguration: NotRequired[PriorityConfigurationOutputTypeDef]
    CustomEventData: NotRequired[str]
    NotificationTarget: NotRequired[str]

class InstanceAccessTypeDef(TypedDict):
    FleetId: NotRequired[str]
    InstanceId: NotRequired[str]
    IpAddress: NotRequired[str]
    OperatingSystem: NotRequired[OperatingSystemType]
    Credentials: NotRequired[InstanceCredentialsTypeDef]

PriorityConfigurationOverrideUnionTypeDef = Union[
    PriorityConfigurationOverrideTypeDef, PriorityConfigurationOverrideOutputTypeDef
]
PriorityConfigurationUnionTypeDef = Union[
    PriorityConfigurationTypeDef, PriorityConfigurationOutputTypeDef
]

class PutScalingPolicyInputTypeDef(TypedDict):
    Name: str
    FleetId: str
    MetricName: MetricNameType
    ScalingAdjustment: NotRequired[int]
    ScalingAdjustmentType: NotRequired[ScalingAdjustmentTypeType]
    Threshold: NotRequired[float]
    ComparisonOperator: NotRequired[ComparisonOperatorTypeType]
    EvaluationPeriods: NotRequired[int]
    PolicyType: NotRequired[PolicyTypeType]
    TargetConfiguration: NotRequired[TargetConfigurationTypeDef]

class ScalingPolicyTypeDef(TypedDict):
    FleetId: NotRequired[str]
    FleetArn: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[ScalingStatusTypeType]
    ScalingAdjustment: NotRequired[int]
    ScalingAdjustmentType: NotRequired[ScalingAdjustmentTypeType]
    ComparisonOperator: NotRequired[ComparisonOperatorTypeType]
    Threshold: NotRequired[float]
    EvaluationPeriods: NotRequired[int]
    MetricName: NotRequired[MetricNameType]
    PolicyType: NotRequired[PolicyTypeType]
    TargetConfiguration: NotRequired[TargetConfigurationTypeDef]
    UpdateStatus: NotRequired[Literal["PENDING_UPDATE"]]
    Location: NotRequired[str]

class RuntimeConfigurationOutputTypeDef(TypedDict):
    ServerProcesses: NotRequired[List[ServerProcessTypeDef]]
    MaxConcurrentGameSessionActivations: NotRequired[int]
    GameSessionActivationTimeoutSeconds: NotRequired[int]

class RuntimeConfigurationTypeDef(TypedDict):
    ServerProcesses: NotRequired[Sequence[ServerProcessTypeDef]]
    MaxConcurrentGameSessionActivations: NotRequired[int]
    GameSessionActivationTimeoutSeconds: NotRequired[int]

class VpcPeeringConnectionTypeDef(TypedDict):
    FleetId: NotRequired[str]
    FleetArn: NotRequired[str]
    IpV4CidrBlock: NotRequired[str]
    VpcPeeringConnectionId: NotRequired[str]
    Status: NotRequired[VpcPeeringConnectionStatusTypeDef]
    PeerVpcId: NotRequired[str]
    GameLiftVpcId: NotRequired[str]

class CreateAliasOutputTypeDef(TypedDict):
    Alias: AliasTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAliasOutputTypeDef(TypedDict):
    Alias: AliasTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListAliasesOutputTypeDef(TypedDict):
    Aliases: List[AliasTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateAliasOutputTypeDef(TypedDict):
    Alias: AliasTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PlayerTypeDef(TypedDict):
    PlayerId: NotRequired[str]
    PlayerAttributes: NotRequired[Mapping[str, AttributeValueUnionTypeDef]]
    Team: NotRequired[str]
    LatencyInMs: NotRequired[Mapping[str, int]]

class DescribeComputeOutputTypeDef(TypedDict):
    Compute: ComputeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListComputeOutputTypeDef(TypedDict):
    ComputeList: List[ComputeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RegisterComputeOutputTypeDef(TypedDict):
    Compute: ComputeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateContainerFleetOutputTypeDef(TypedDict):
    ContainerFleet: ContainerFleetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeContainerFleetOutputTypeDef(TypedDict):
    ContainerFleet: ContainerFleetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListContainerFleetsOutputTypeDef(TypedDict):
    ContainerFleets: List[ContainerFleetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateContainerFleetOutputTypeDef(TypedDict):
    ContainerFleet: ContainerFleetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GameServerContainerDefinitionTypeDef(TypedDict):
    ContainerName: NotRequired[str]
    DependsOn: NotRequired[List[ContainerDependencyTypeDef]]
    MountPoints: NotRequired[List[ContainerMountPointTypeDef]]
    EnvironmentOverride: NotRequired[List[ContainerEnvironmentTypeDef]]
    ImageUri: NotRequired[str]
    PortConfiguration: NotRequired[ContainerPortConfigurationOutputTypeDef]
    ResolvedImageDigest: NotRequired[str]
    ServerSdkVersion: NotRequired[str]

class SupportContainerDefinitionTypeDef(TypedDict):
    ContainerName: NotRequired[str]
    DependsOn: NotRequired[List[ContainerDependencyTypeDef]]
    MountPoints: NotRequired[List[ContainerMountPointTypeDef]]
    EnvironmentOverride: NotRequired[List[ContainerEnvironmentTypeDef]]
    Essential: NotRequired[bool]
    HealthCheck: NotRequired[ContainerHealthCheckOutputTypeDef]
    ImageUri: NotRequired[str]
    MemoryHardLimitMebibytes: NotRequired[int]
    PortConfiguration: NotRequired[ContainerPortConfigurationOutputTypeDef]
    ResolvedImageDigest: NotRequired[str]
    Vcpu: NotRequired[float]

ContainerPortConfigurationUnionTypeDef = Union[
    ContainerPortConfigurationTypeDef, ContainerPortConfigurationOutputTypeDef
]

class CreateScriptOutputTypeDef(TypedDict):
    Script: ScriptTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeScriptOutputTypeDef(TypedDict):
    Script: ScriptTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListScriptsOutputTypeDef(TypedDict):
    Scripts: List[ScriptTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateScriptOutputTypeDef(TypedDict):
    Script: ScriptTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFleetOutputTypeDef(TypedDict):
    FleetAttributes: FleetAttributesTypeDef
    LocationStates: List[LocationStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeFleetAttributesOutputTypeDef(TypedDict):
    FleetAttributes: List[FleetAttributesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeFleetLocationAttributesOutputTypeDef(TypedDict):
    FleetId: str
    FleetArn: str
    LocationAttributes: List[LocationAttributesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateGameServerGroupOutputTypeDef(TypedDict):
    GameServerGroup: GameServerGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteGameServerGroupOutputTypeDef(TypedDict):
    GameServerGroup: GameServerGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeGameServerGroupOutputTypeDef(TypedDict):
    GameServerGroup: GameServerGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListGameServerGroupsOutputTypeDef(TypedDict):
    GameServerGroups: List[GameServerGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ResumeGameServerGroupOutputTypeDef(TypedDict):
    GameServerGroup: GameServerGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SuspendGameServerGroupOutputTypeDef(TypedDict):
    GameServerGroup: GameServerGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGameServerGroupOutputTypeDef(TypedDict):
    GameServerGroup: GameServerGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateGameSessionOutputTypeDef(TypedDict):
    GameSession: GameSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeGameSessionsOutputTypeDef(TypedDict):
    GameSessions: List[GameSessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GameSessionDetailTypeDef(TypedDict):
    GameSession: NotRequired[GameSessionTypeDef]
    ProtectionPolicy: NotRequired[ProtectionPolicyType]

class SearchGameSessionsOutputTypeDef(TypedDict):
    GameSessions: List[GameSessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TerminateGameSessionOutputTypeDef(TypedDict):
    GameSession: GameSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGameSessionOutputTypeDef(TypedDict):
    GameSession: GameSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMatchmakingConfigurationOutputTypeDef(TypedDict):
    Configuration: MatchmakingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeMatchmakingConfigurationsOutputTypeDef(TypedDict):
    Configurations: List[MatchmakingConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateMatchmakingConfigurationOutputTypeDef(TypedDict):
    Configuration: MatchmakingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeFleetDeploymentOutputTypeDef(TypedDict):
    FleetDeployment: FleetDeploymentTypeDef
    LocationalDeployments: Dict[str, LocationalDeploymentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListFleetDeploymentsOutputTypeDef(TypedDict):
    FleetDeployments: List[FleetDeploymentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeFleetCapacityOutputTypeDef(TypedDict):
    FleetCapacity: List[FleetCapacityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeFleetLocationCapacityOutputTypeDef(TypedDict):
    FleetCapacity: FleetCapacityTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateGameServerGroupInputTypeDef(TypedDict):
    GameServerGroupName: str
    RoleArn: str
    MinSize: int
    MaxSize: int
    LaunchTemplate: LaunchTemplateSpecificationTypeDef
    InstanceDefinitions: Sequence[InstanceDefinitionTypeDef]
    AutoScalingPolicy: NotRequired[GameServerGroupAutoScalingPolicyTypeDef]
    BalancingStrategy: NotRequired[BalancingStrategyType]
    GameServerProtectionPolicy: NotRequired[GameServerProtectionPolicyType]
    VpcSubnets: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]

class MatchmakingTicketTypeDef(TypedDict):
    TicketId: NotRequired[str]
    ConfigurationName: NotRequired[str]
    ConfigurationArn: NotRequired[str]
    Status: NotRequired[MatchmakingConfigurationStatusType]
    StatusReason: NotRequired[str]
    StatusMessage: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    Players: NotRequired[List[PlayerOutputTypeDef]]
    GameSessionConnectionInfo: NotRequired[GameSessionConnectionInfoTypeDef]
    EstimatedWaitTime: NotRequired[int]

class DescribeGameSessionPlacementOutputTypeDef(TypedDict):
    GameSessionPlacement: GameSessionPlacementTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartGameSessionPlacementOutputTypeDef(TypedDict):
    GameSessionPlacement: GameSessionPlacementTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StopGameSessionPlacementOutputTypeDef(TypedDict):
    GameSessionPlacement: GameSessionPlacementTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateGameSessionQueueOutputTypeDef(TypedDict):
    GameSessionQueue: GameSessionQueueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeGameSessionQueuesOutputTypeDef(TypedDict):
    GameSessionQueues: List[GameSessionQueueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateGameSessionQueueOutputTypeDef(TypedDict):
    GameSessionQueue: GameSessionQueueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetInstanceAccessOutputTypeDef(TypedDict):
    InstanceAccess: InstanceAccessTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartGameSessionPlacementInputTypeDef(TypedDict):
    PlacementId: str
    GameSessionQueueName: str
    MaximumPlayerSessionCount: int
    GameProperties: NotRequired[Sequence[GamePropertyTypeDef]]
    GameSessionName: NotRequired[str]
    PlayerLatencies: NotRequired[Sequence[PlayerLatencyTypeDef]]
    DesiredPlayerSessions: NotRequired[Sequence[DesiredPlayerSessionTypeDef]]
    GameSessionData: NotRequired[str]
    PriorityConfigurationOverride: NotRequired[PriorityConfigurationOverrideUnionTypeDef]

class CreateGameSessionQueueInputTypeDef(TypedDict):
    Name: str
    TimeoutInSeconds: NotRequired[int]
    PlayerLatencyPolicies: NotRequired[Sequence[PlayerLatencyPolicyTypeDef]]
    Destinations: NotRequired[Sequence[GameSessionQueueDestinationTypeDef]]
    FilterConfiguration: NotRequired[FilterConfigurationUnionTypeDef]
    PriorityConfiguration: NotRequired[PriorityConfigurationUnionTypeDef]
    CustomEventData: NotRequired[str]
    NotificationTarget: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class UpdateGameSessionQueueInputTypeDef(TypedDict):
    Name: str
    TimeoutInSeconds: NotRequired[int]
    PlayerLatencyPolicies: NotRequired[Sequence[PlayerLatencyPolicyTypeDef]]
    Destinations: NotRequired[Sequence[GameSessionQueueDestinationTypeDef]]
    FilterConfiguration: NotRequired[FilterConfigurationUnionTypeDef]
    PriorityConfiguration: NotRequired[PriorityConfigurationUnionTypeDef]
    CustomEventData: NotRequired[str]
    NotificationTarget: NotRequired[str]

class DescribeScalingPoliciesOutputTypeDef(TypedDict):
    ScalingPolicies: List[ScalingPolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeRuntimeConfigurationOutputTypeDef(TypedDict):
    RuntimeConfiguration: RuntimeConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRuntimeConfigurationOutputTypeDef(TypedDict):
    RuntimeConfiguration: RuntimeConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

RuntimeConfigurationUnionTypeDef = Union[
    RuntimeConfigurationTypeDef, RuntimeConfigurationOutputTypeDef
]

class DescribeVpcPeeringConnectionsOutputTypeDef(TypedDict):
    VpcPeeringConnections: List[VpcPeeringConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

PlayerUnionTypeDef = Union[PlayerTypeDef, PlayerOutputTypeDef]

class ContainerGroupDefinitionTypeDef(TypedDict):
    Name: str
    ContainerGroupDefinitionArn: NotRequired[str]
    CreationTime: NotRequired[datetime]
    OperatingSystem: NotRequired[Literal["AMAZON_LINUX_2023"]]
    ContainerGroupType: NotRequired[ContainerGroupTypeType]
    TotalMemoryLimitMebibytes: NotRequired[int]
    TotalVcpuLimit: NotRequired[float]
    GameServerContainerDefinition: NotRequired[GameServerContainerDefinitionTypeDef]
    SupportContainerDefinitions: NotRequired[List[SupportContainerDefinitionTypeDef]]
    VersionNumber: NotRequired[int]
    VersionDescription: NotRequired[str]
    Status: NotRequired[ContainerGroupDefinitionStatusType]
    StatusReason: NotRequired[str]

class GameServerContainerDefinitionInputTypeDef(TypedDict):
    ContainerName: str
    ImageUri: str
    PortConfiguration: ContainerPortConfigurationUnionTypeDef
    ServerSdkVersion: str
    DependsOn: NotRequired[Sequence[ContainerDependencyTypeDef]]
    MountPoints: NotRequired[Sequence[ContainerMountPointTypeDef]]
    EnvironmentOverride: NotRequired[Sequence[ContainerEnvironmentTypeDef]]

class SupportContainerDefinitionInputTypeDef(TypedDict):
    ContainerName: str
    ImageUri: str
    DependsOn: NotRequired[Sequence[ContainerDependencyTypeDef]]
    MountPoints: NotRequired[Sequence[ContainerMountPointTypeDef]]
    EnvironmentOverride: NotRequired[Sequence[ContainerEnvironmentTypeDef]]
    Essential: NotRequired[bool]
    HealthCheck: NotRequired[ContainerHealthCheckUnionTypeDef]
    MemoryHardLimitMebibytes: NotRequired[int]
    PortConfiguration: NotRequired[ContainerPortConfigurationUnionTypeDef]
    Vcpu: NotRequired[float]

class DescribeGameSessionDetailsOutputTypeDef(TypedDict):
    GameSessionDetails: List[GameSessionDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeMatchmakingOutputTypeDef(TypedDict):
    TicketList: List[MatchmakingTicketTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartMatchBackfillOutputTypeDef(TypedDict):
    MatchmakingTicket: MatchmakingTicketTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartMatchmakingOutputTypeDef(TypedDict):
    MatchmakingTicket: MatchmakingTicketTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFleetInputTypeDef(TypedDict):
    Name: str
    Description: NotRequired[str]
    BuildId: NotRequired[str]
    ScriptId: NotRequired[str]
    ServerLaunchPath: NotRequired[str]
    ServerLaunchParameters: NotRequired[str]
    LogPaths: NotRequired[Sequence[str]]
    EC2InstanceType: NotRequired[EC2InstanceTypeType]
    EC2InboundPermissions: NotRequired[Sequence[IpPermissionTypeDef]]
    NewGameSessionProtectionPolicy: NotRequired[ProtectionPolicyType]
    RuntimeConfiguration: NotRequired[RuntimeConfigurationUnionTypeDef]
    ResourceCreationLimitPolicy: NotRequired[ResourceCreationLimitPolicyTypeDef]
    MetricGroups: NotRequired[Sequence[str]]
    PeerVpcAwsAccountId: NotRequired[str]
    PeerVpcId: NotRequired[str]
    FleetType: NotRequired[FleetTypeType]
    InstanceRoleArn: NotRequired[str]
    CertificateConfiguration: NotRequired[CertificateConfigurationTypeDef]
    Locations: NotRequired[Sequence[LocationConfigurationTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ComputeType: NotRequired[ComputeTypeType]
    AnywhereConfiguration: NotRequired[AnywhereConfigurationTypeDef]
    InstanceRoleCredentialsProvider: NotRequired[Literal["SHARED_CREDENTIAL_FILE"]]

class UpdateRuntimeConfigurationInputTypeDef(TypedDict):
    FleetId: str
    RuntimeConfiguration: RuntimeConfigurationUnionTypeDef

class StartMatchBackfillInputTypeDef(TypedDict):
    ConfigurationName: str
    Players: Sequence[PlayerUnionTypeDef]
    TicketId: NotRequired[str]
    GameSessionArn: NotRequired[str]

class StartMatchmakingInputTypeDef(TypedDict):
    ConfigurationName: str
    Players: Sequence[PlayerUnionTypeDef]
    TicketId: NotRequired[str]

class CreateContainerGroupDefinitionOutputTypeDef(TypedDict):
    ContainerGroupDefinition: ContainerGroupDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeContainerGroupDefinitionOutputTypeDef(TypedDict):
    ContainerGroupDefinition: ContainerGroupDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListContainerGroupDefinitionVersionsOutputTypeDef(TypedDict):
    ContainerGroupDefinitions: List[ContainerGroupDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListContainerGroupDefinitionsOutputTypeDef(TypedDict):
    ContainerGroupDefinitions: List[ContainerGroupDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateContainerGroupDefinitionOutputTypeDef(TypedDict):
    ContainerGroupDefinition: ContainerGroupDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateContainerGroupDefinitionInputTypeDef(TypedDict):
    Name: str
    TotalMemoryLimitMebibytes: int
    TotalVcpuLimit: float
    OperatingSystem: Literal["AMAZON_LINUX_2023"]
    ContainerGroupType: NotRequired[ContainerGroupTypeType]
    GameServerContainerDefinition: NotRequired[GameServerContainerDefinitionInputTypeDef]
    SupportContainerDefinitions: NotRequired[Sequence[SupportContainerDefinitionInputTypeDef]]
    VersionDescription: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]

class UpdateContainerGroupDefinitionInputTypeDef(TypedDict):
    Name: str
    GameServerContainerDefinition: NotRequired[GameServerContainerDefinitionInputTypeDef]
    SupportContainerDefinitions: NotRequired[Sequence[SupportContainerDefinitionInputTypeDef]]
    TotalMemoryLimitMebibytes: NotRequired[int]
    TotalVcpuLimit: NotRequired[float]
    VersionDescription: NotRequired[str]
    SourceVersionNumber: NotRequired[int]
    OperatingSystem: NotRequired[Literal["AMAZON_LINUX_2023"]]
