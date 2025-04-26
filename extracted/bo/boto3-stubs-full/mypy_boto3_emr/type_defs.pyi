"""
Type annotations for emr service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_emr.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Union

from .literals import (
    ActionOnFailureType,
    AdjustmentTypeType,
    AuthModeType,
    AutoScalingPolicyStateChangeReasonCodeType,
    AutoScalingPolicyStateType,
    CancelStepsRequestStatusType,
    ClusterStateChangeReasonCodeType,
    ClusterStateType,
    ComparisonOperatorType,
    ComputeLimitsUnitTypeType,
    IdcUserAssignmentType,
    IdentityTypeType,
    InstanceCollectionTypeType,
    InstanceFleetStateChangeReasonCodeType,
    InstanceFleetStateType,
    InstanceFleetTypeType,
    InstanceGroupStateChangeReasonCodeType,
    InstanceGroupStateType,
    InstanceGroupTypeType,
    InstanceRoleTypeType,
    InstanceStateChangeReasonCodeType,
    InstanceStateType,
    JobFlowExecutionStateType,
    MarketTypeType,
    NotebookExecutionStatusType,
    OnDemandCapacityReservationPreferenceType,
    OnDemandProvisioningAllocationStrategyType,
    PlacementGroupStrategyType,
    ReconfigurationTypeType,
    RepoUpgradeOnBootType,
    ScaleDownBehaviorType,
    ScalingStrategyType,
    SpotProvisioningAllocationStrategyType,
    SpotProvisioningTimeoutActionType,
    StatisticType,
    StepCancellationOptionType,
    StepExecutionStateType,
    StepStateType,
    UnitType,
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
    "AddInstanceFleetInputTypeDef",
    "AddInstanceFleetOutputTypeDef",
    "AddInstanceGroupsInputTypeDef",
    "AddInstanceGroupsOutputTypeDef",
    "AddJobFlowStepsInputTypeDef",
    "AddJobFlowStepsOutputTypeDef",
    "AddTagsInputTypeDef",
    "ApplicationOutputTypeDef",
    "ApplicationTypeDef",
    "ApplicationUnionTypeDef",
    "AutoScalingPolicyDescriptionTypeDef",
    "AutoScalingPolicyStateChangeReasonTypeDef",
    "AutoScalingPolicyStatusTypeDef",
    "AutoScalingPolicyTypeDef",
    "AutoTerminationPolicyTypeDef",
    "BlockPublicAccessConfigurationMetadataTypeDef",
    "BlockPublicAccessConfigurationOutputTypeDef",
    "BlockPublicAccessConfigurationTypeDef",
    "BlockPublicAccessConfigurationUnionTypeDef",
    "BootstrapActionConfigOutputTypeDef",
    "BootstrapActionConfigTypeDef",
    "BootstrapActionConfigUnionTypeDef",
    "BootstrapActionDetailTypeDef",
    "CancelStepsInfoTypeDef",
    "CancelStepsInputTypeDef",
    "CancelStepsOutputTypeDef",
    "CloudWatchAlarmDefinitionOutputTypeDef",
    "CloudWatchAlarmDefinitionTypeDef",
    "CloudWatchAlarmDefinitionUnionTypeDef",
    "ClusterStateChangeReasonTypeDef",
    "ClusterStatusTypeDef",
    "ClusterSummaryTypeDef",
    "ClusterTimelineTypeDef",
    "ClusterTypeDef",
    "CommandTypeDef",
    "ComputeLimitsTypeDef",
    "ConfigurationOutputTypeDef",
    "ConfigurationPaginatorTypeDef",
    "ConfigurationTypeDef",
    "ConfigurationUnionTypeDef",
    "CreateSecurityConfigurationInputTypeDef",
    "CreateSecurityConfigurationOutputTypeDef",
    "CreateStudioInputTypeDef",
    "CreateStudioOutputTypeDef",
    "CreateStudioSessionMappingInputTypeDef",
    "CredentialsTypeDef",
    "DeleteSecurityConfigurationInputTypeDef",
    "DeleteStudioInputTypeDef",
    "DeleteStudioSessionMappingInputTypeDef",
    "DescribeClusterInputTypeDef",
    "DescribeClusterInputWaitExtraTypeDef",
    "DescribeClusterInputWaitTypeDef",
    "DescribeClusterOutputTypeDef",
    "DescribeJobFlowsInputTypeDef",
    "DescribeJobFlowsOutputTypeDef",
    "DescribeNotebookExecutionInputTypeDef",
    "DescribeNotebookExecutionOutputTypeDef",
    "DescribeReleaseLabelInputTypeDef",
    "DescribeReleaseLabelOutputTypeDef",
    "DescribeSecurityConfigurationInputTypeDef",
    "DescribeSecurityConfigurationOutputTypeDef",
    "DescribeStepInputTypeDef",
    "DescribeStepInputWaitTypeDef",
    "DescribeStepOutputTypeDef",
    "DescribeStudioInputTypeDef",
    "DescribeStudioOutputTypeDef",
    "EbsBlockDeviceConfigTypeDef",
    "EbsBlockDeviceTypeDef",
    "EbsConfigurationTypeDef",
    "EbsVolumeTypeDef",
    "Ec2InstanceAttributesTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ErrorDetailTypeDef",
    "ExecutionEngineConfigTypeDef",
    "FailureDetailsTypeDef",
    "GetAutoTerminationPolicyInputTypeDef",
    "GetAutoTerminationPolicyOutputTypeDef",
    "GetBlockPublicAccessConfigurationOutputTypeDef",
    "GetClusterSessionCredentialsInputTypeDef",
    "GetClusterSessionCredentialsOutputTypeDef",
    "GetManagedScalingPolicyInputTypeDef",
    "GetManagedScalingPolicyOutputTypeDef",
    "GetStudioSessionMappingInputTypeDef",
    "GetStudioSessionMappingOutputTypeDef",
    "HadoopJarStepConfigOutputTypeDef",
    "HadoopJarStepConfigTypeDef",
    "HadoopJarStepConfigUnionTypeDef",
    "HadoopStepConfigTypeDef",
    "InstanceFleetConfigTypeDef",
    "InstanceFleetModifyConfigTypeDef",
    "InstanceFleetPaginatorTypeDef",
    "InstanceFleetProvisioningSpecificationsTypeDef",
    "InstanceFleetResizingSpecificationsTypeDef",
    "InstanceFleetStateChangeReasonTypeDef",
    "InstanceFleetStatusTypeDef",
    "InstanceFleetTimelineTypeDef",
    "InstanceFleetTypeDef",
    "InstanceGroupConfigTypeDef",
    "InstanceGroupDetailTypeDef",
    "InstanceGroupModifyConfigTypeDef",
    "InstanceGroupPaginatorTypeDef",
    "InstanceGroupStateChangeReasonTypeDef",
    "InstanceGroupStatusTypeDef",
    "InstanceGroupTimelineTypeDef",
    "InstanceGroupTypeDef",
    "InstanceResizePolicyOutputTypeDef",
    "InstanceResizePolicyTypeDef",
    "InstanceResizePolicyUnionTypeDef",
    "InstanceStateChangeReasonTypeDef",
    "InstanceStatusTypeDef",
    "InstanceTimelineTypeDef",
    "InstanceTypeConfigTypeDef",
    "InstanceTypeDef",
    "InstanceTypeSpecificationPaginatorTypeDef",
    "InstanceTypeSpecificationTypeDef",
    "JobFlowDetailTypeDef",
    "JobFlowExecutionStatusDetailTypeDef",
    "JobFlowInstancesConfigTypeDef",
    "JobFlowInstancesDetailTypeDef",
    "KerberosAttributesTypeDef",
    "KeyValueTypeDef",
    "ListBootstrapActionsInputPaginateTypeDef",
    "ListBootstrapActionsInputTypeDef",
    "ListBootstrapActionsOutputTypeDef",
    "ListClustersInputPaginateTypeDef",
    "ListClustersInputTypeDef",
    "ListClustersOutputTypeDef",
    "ListInstanceFleetsInputPaginateTypeDef",
    "ListInstanceFleetsInputTypeDef",
    "ListInstanceFleetsOutputPaginatorTypeDef",
    "ListInstanceFleetsOutputTypeDef",
    "ListInstanceGroupsInputPaginateTypeDef",
    "ListInstanceGroupsInputTypeDef",
    "ListInstanceGroupsOutputPaginatorTypeDef",
    "ListInstanceGroupsOutputTypeDef",
    "ListInstancesInputPaginateTypeDef",
    "ListInstancesInputTypeDef",
    "ListInstancesOutputTypeDef",
    "ListNotebookExecutionsInputPaginateTypeDef",
    "ListNotebookExecutionsInputTypeDef",
    "ListNotebookExecutionsOutputTypeDef",
    "ListReleaseLabelsInputTypeDef",
    "ListReleaseLabelsOutputTypeDef",
    "ListSecurityConfigurationsInputPaginateTypeDef",
    "ListSecurityConfigurationsInputTypeDef",
    "ListSecurityConfigurationsOutputTypeDef",
    "ListStepsInputPaginateTypeDef",
    "ListStepsInputTypeDef",
    "ListStepsOutputTypeDef",
    "ListStudioSessionMappingsInputPaginateTypeDef",
    "ListStudioSessionMappingsInputTypeDef",
    "ListStudioSessionMappingsOutputTypeDef",
    "ListStudiosInputPaginateTypeDef",
    "ListStudiosInputTypeDef",
    "ListStudiosOutputTypeDef",
    "ListSupportedInstanceTypesInputTypeDef",
    "ListSupportedInstanceTypesOutputTypeDef",
    "ManagedScalingPolicyTypeDef",
    "MetricDimensionTypeDef",
    "ModifyClusterInputTypeDef",
    "ModifyClusterOutputTypeDef",
    "ModifyInstanceFleetInputTypeDef",
    "ModifyInstanceGroupsInputTypeDef",
    "NotebookExecutionSummaryTypeDef",
    "NotebookExecutionTypeDef",
    "NotebookS3LocationForOutputTypeDef",
    "NotebookS3LocationFromInputTypeDef",
    "OSReleaseTypeDef",
    "OnDemandCapacityReservationOptionsTypeDef",
    "OnDemandProvisioningSpecificationTypeDef",
    "OnDemandResizingSpecificationTypeDef",
    "OutputNotebookS3LocationForOutputTypeDef",
    "OutputNotebookS3LocationFromInputTypeDef",
    "PaginatorConfigTypeDef",
    "PlacementGroupConfigTypeDef",
    "PlacementTypeOutputTypeDef",
    "PlacementTypeTypeDef",
    "PlacementTypeUnionTypeDef",
    "PortRangeTypeDef",
    "PutAutoScalingPolicyInputTypeDef",
    "PutAutoScalingPolicyOutputTypeDef",
    "PutAutoTerminationPolicyInputTypeDef",
    "PutBlockPublicAccessConfigurationInputTypeDef",
    "PutManagedScalingPolicyInputTypeDef",
    "ReleaseLabelFilterTypeDef",
    "RemoveAutoScalingPolicyInputTypeDef",
    "RemoveAutoTerminationPolicyInputTypeDef",
    "RemoveManagedScalingPolicyInputTypeDef",
    "RemoveTagsInputTypeDef",
    "ResponseMetadataTypeDef",
    "RunJobFlowInputTypeDef",
    "RunJobFlowOutputTypeDef",
    "ScalingActionTypeDef",
    "ScalingConstraintsTypeDef",
    "ScalingRuleOutputTypeDef",
    "ScalingRuleTypeDef",
    "ScalingRuleUnionTypeDef",
    "ScalingTriggerOutputTypeDef",
    "ScalingTriggerTypeDef",
    "ScalingTriggerUnionTypeDef",
    "ScriptBootstrapActionConfigOutputTypeDef",
    "ScriptBootstrapActionConfigTypeDef",
    "ScriptBootstrapActionConfigUnionTypeDef",
    "SecurityConfigurationSummaryTypeDef",
    "SessionMappingDetailTypeDef",
    "SessionMappingSummaryTypeDef",
    "SetKeepJobFlowAliveWhenNoStepsInputTypeDef",
    "SetTerminationProtectionInputTypeDef",
    "SetUnhealthyNodeReplacementInputTypeDef",
    "SetVisibleToAllUsersInputTypeDef",
    "ShrinkPolicyOutputTypeDef",
    "ShrinkPolicyTypeDef",
    "ShrinkPolicyUnionTypeDef",
    "SimpleScalingPolicyConfigurationTypeDef",
    "SimplifiedApplicationTypeDef",
    "SpotProvisioningSpecificationTypeDef",
    "SpotResizingSpecificationTypeDef",
    "StartNotebookExecutionInputTypeDef",
    "StartNotebookExecutionOutputTypeDef",
    "StepConfigOutputTypeDef",
    "StepConfigTypeDef",
    "StepConfigUnionTypeDef",
    "StepDetailTypeDef",
    "StepExecutionStatusDetailTypeDef",
    "StepStateChangeReasonTypeDef",
    "StepStatusTypeDef",
    "StepSummaryTypeDef",
    "StepTimelineTypeDef",
    "StepTypeDef",
    "StopNotebookExecutionInputTypeDef",
    "StudioSummaryTypeDef",
    "StudioTypeDef",
    "SupportedInstanceTypeTypeDef",
    "SupportedProductConfigTypeDef",
    "TagTypeDef",
    "TerminateJobFlowsInputTypeDef",
    "TimestampTypeDef",
    "UpdateStudioInputTypeDef",
    "UpdateStudioSessionMappingInputTypeDef",
    "UsernamePasswordTypeDef",
    "VolumeSpecificationTypeDef",
    "WaiterConfigTypeDef",
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class ApplicationOutputTypeDef(TypedDict):
    Name: NotRequired[str]
    Version: NotRequired[str]
    Args: NotRequired[List[str]]
    AdditionalInfo: NotRequired[Dict[str, str]]

class ApplicationTypeDef(TypedDict):
    Name: NotRequired[str]
    Version: NotRequired[str]
    Args: NotRequired[Sequence[str]]
    AdditionalInfo: NotRequired[Mapping[str, str]]

class ScalingConstraintsTypeDef(TypedDict):
    MinCapacity: int
    MaxCapacity: int

class AutoScalingPolicyStateChangeReasonTypeDef(TypedDict):
    Code: NotRequired[AutoScalingPolicyStateChangeReasonCodeType]
    Message: NotRequired[str]

class AutoTerminationPolicyTypeDef(TypedDict):
    IdleTimeout: NotRequired[int]

class BlockPublicAccessConfigurationMetadataTypeDef(TypedDict):
    CreationDateTime: datetime
    CreatedByArn: str

class PortRangeTypeDef(TypedDict):
    MinRange: int
    MaxRange: NotRequired[int]

class ScriptBootstrapActionConfigOutputTypeDef(TypedDict):
    Path: str
    Args: NotRequired[List[str]]

class CancelStepsInfoTypeDef(TypedDict):
    StepId: NotRequired[str]
    Status: NotRequired[CancelStepsRequestStatusType]
    Reason: NotRequired[str]

class CancelStepsInputTypeDef(TypedDict):
    ClusterId: str
    StepIds: Sequence[str]
    StepCancellationOption: NotRequired[StepCancellationOptionType]

class MetricDimensionTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class ClusterStateChangeReasonTypeDef(TypedDict):
    Code: NotRequired[ClusterStateChangeReasonCodeType]
    Message: NotRequired[str]

class ClusterTimelineTypeDef(TypedDict):
    CreationDateTime: NotRequired[datetime]
    ReadyDateTime: NotRequired[datetime]
    EndDateTime: NotRequired[datetime]

class ErrorDetailTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorData: NotRequired[List[Dict[str, str]]]
    ErrorMessage: NotRequired[str]

class ConfigurationOutputTypeDef(TypedDict):
    Classification: NotRequired[str]
    Configurations: NotRequired[List[Dict[str, Any]]]
    Properties: NotRequired[Dict[str, str]]

class Ec2InstanceAttributesTypeDef(TypedDict):
    Ec2KeyName: NotRequired[str]
    Ec2SubnetId: NotRequired[str]
    RequestedEc2SubnetIds: NotRequired[List[str]]
    Ec2AvailabilityZone: NotRequired[str]
    RequestedEc2AvailabilityZones: NotRequired[List[str]]
    IamInstanceProfile: NotRequired[str]
    EmrManagedMasterSecurityGroup: NotRequired[str]
    EmrManagedSlaveSecurityGroup: NotRequired[str]
    ServiceAccessSecurityGroup: NotRequired[str]
    AdditionalMasterSecurityGroups: NotRequired[List[str]]
    AdditionalSlaveSecurityGroups: NotRequired[List[str]]

class KerberosAttributesTypeDef(TypedDict):
    Realm: str
    KdcAdminPassword: str
    CrossRealmTrustPrincipalPassword: NotRequired[str]
    ADDomainJoinUser: NotRequired[str]
    ADDomainJoinPassword: NotRequired[str]

class PlacementGroupConfigTypeDef(TypedDict):
    InstanceRole: InstanceRoleTypeType
    PlacementStrategy: NotRequired[PlacementGroupStrategyType]

class CommandTypeDef(TypedDict):
    Name: NotRequired[str]
    ScriptPath: NotRequired[str]
    Args: NotRequired[List[str]]

ComputeLimitsTypeDef = TypedDict(
    "ComputeLimitsTypeDef",
    {
        "UnitType": ComputeLimitsUnitTypeType,
        "MinimumCapacityUnits": int,
        "MaximumCapacityUnits": int,
        "MaximumOnDemandCapacityUnits": NotRequired[int],
        "MaximumCoreCapacityUnits": NotRequired[int],
    },
)

class ConfigurationPaginatorTypeDef(TypedDict):
    Classification: NotRequired[str]
    Configurations: NotRequired[List[Dict[str, Any]]]
    Properties: NotRequired[Dict[str, str]]

class ConfigurationTypeDef(TypedDict):
    Classification: NotRequired[str]
    Configurations: NotRequired[Sequence[Mapping[str, Any]]]
    Properties: NotRequired[Mapping[str, str]]

class CreateSecurityConfigurationInputTypeDef(TypedDict):
    Name: str
    SecurityConfiguration: str

class CreateStudioSessionMappingInputTypeDef(TypedDict):
    StudioId: str
    IdentityType: IdentityTypeType
    SessionPolicyArn: str
    IdentityId: NotRequired[str]
    IdentityName: NotRequired[str]

class UsernamePasswordTypeDef(TypedDict):
    Username: NotRequired[str]
    Password: NotRequired[str]

class DeleteSecurityConfigurationInputTypeDef(TypedDict):
    Name: str

class DeleteStudioInputTypeDef(TypedDict):
    StudioId: str

class DeleteStudioSessionMappingInputTypeDef(TypedDict):
    StudioId: str
    IdentityType: IdentityTypeType
    IdentityId: NotRequired[str]
    IdentityName: NotRequired[str]

class DescribeClusterInputTypeDef(TypedDict):
    ClusterId: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

TimestampTypeDef = Union[datetime, str]

class DescribeNotebookExecutionInputTypeDef(TypedDict):
    NotebookExecutionId: str

class DescribeReleaseLabelInputTypeDef(TypedDict):
    ReleaseLabel: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class OSReleaseTypeDef(TypedDict):
    Label: NotRequired[str]

class SimplifiedApplicationTypeDef(TypedDict):
    Name: NotRequired[str]
    Version: NotRequired[str]

class DescribeSecurityConfigurationInputTypeDef(TypedDict):
    Name: str

class DescribeStepInputTypeDef(TypedDict):
    ClusterId: str
    StepId: str

class DescribeStudioInputTypeDef(TypedDict):
    StudioId: str

class VolumeSpecificationTypeDef(TypedDict):
    VolumeType: str
    SizeInGB: int
    Iops: NotRequired[int]
    Throughput: NotRequired[int]

class EbsVolumeTypeDef(TypedDict):
    Device: NotRequired[str]
    VolumeId: NotRequired[str]

ExecutionEngineConfigTypeDef = TypedDict(
    "ExecutionEngineConfigTypeDef",
    {
        "Id": str,
        "Type": NotRequired[Literal["EMR"]],
        "MasterInstanceSecurityGroupId": NotRequired[str],
        "ExecutionRoleArn": NotRequired[str],
    },
)

class FailureDetailsTypeDef(TypedDict):
    Reason: NotRequired[str]
    Message: NotRequired[str]
    LogFile: NotRequired[str]

class GetAutoTerminationPolicyInputTypeDef(TypedDict):
    ClusterId: str

class GetClusterSessionCredentialsInputTypeDef(TypedDict):
    ClusterId: str
    ExecutionRoleArn: NotRequired[str]

class GetManagedScalingPolicyInputTypeDef(TypedDict):
    ClusterId: str

class GetStudioSessionMappingInputTypeDef(TypedDict):
    StudioId: str
    IdentityType: IdentityTypeType
    IdentityId: NotRequired[str]
    IdentityName: NotRequired[str]

class SessionMappingDetailTypeDef(TypedDict):
    StudioId: NotRequired[str]
    IdentityId: NotRequired[str]
    IdentityName: NotRequired[str]
    IdentityType: NotRequired[IdentityTypeType]
    SessionPolicyArn: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]

class KeyValueTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]

class HadoopStepConfigTypeDef(TypedDict):
    Jar: NotRequired[str]
    Properties: NotRequired[Dict[str, str]]
    MainClass: NotRequired[str]
    Args: NotRequired[List[str]]

class SpotProvisioningSpecificationTypeDef(TypedDict):
    TimeoutDurationMinutes: int
    TimeoutAction: SpotProvisioningTimeoutActionType
    BlockDurationMinutes: NotRequired[int]
    AllocationStrategy: NotRequired[SpotProvisioningAllocationStrategyType]

class SpotResizingSpecificationTypeDef(TypedDict):
    TimeoutDurationMinutes: NotRequired[int]
    AllocationStrategy: NotRequired[SpotProvisioningAllocationStrategyType]

class InstanceFleetStateChangeReasonTypeDef(TypedDict):
    Code: NotRequired[InstanceFleetStateChangeReasonCodeType]
    Message: NotRequired[str]

class InstanceFleetTimelineTypeDef(TypedDict):
    CreationDateTime: NotRequired[datetime]
    ReadyDateTime: NotRequired[datetime]
    EndDateTime: NotRequired[datetime]

class InstanceGroupDetailTypeDef(TypedDict):
    Market: MarketTypeType
    InstanceRole: InstanceRoleTypeType
    InstanceType: str
    InstanceRequestCount: int
    InstanceRunningCount: int
    State: InstanceGroupStateType
    CreationDateTime: datetime
    InstanceGroupId: NotRequired[str]
    Name: NotRequired[str]
    BidPrice: NotRequired[str]
    LastStateChangeReason: NotRequired[str]
    StartDateTime: NotRequired[datetime]
    ReadyDateTime: NotRequired[datetime]
    EndDateTime: NotRequired[datetime]
    CustomAmiId: NotRequired[str]

class InstanceGroupStateChangeReasonTypeDef(TypedDict):
    Code: NotRequired[InstanceGroupStateChangeReasonCodeType]
    Message: NotRequired[str]

class InstanceGroupTimelineTypeDef(TypedDict):
    CreationDateTime: NotRequired[datetime]
    ReadyDateTime: NotRequired[datetime]
    EndDateTime: NotRequired[datetime]

class InstanceResizePolicyOutputTypeDef(TypedDict):
    InstancesToTerminate: NotRequired[List[str]]
    InstancesToProtect: NotRequired[List[str]]
    InstanceTerminationTimeout: NotRequired[int]

class InstanceResizePolicyTypeDef(TypedDict):
    InstancesToTerminate: NotRequired[Sequence[str]]
    InstancesToProtect: NotRequired[Sequence[str]]
    InstanceTerminationTimeout: NotRequired[int]

class InstanceStateChangeReasonTypeDef(TypedDict):
    Code: NotRequired[InstanceStateChangeReasonCodeType]
    Message: NotRequired[str]

class InstanceTimelineTypeDef(TypedDict):
    CreationDateTime: NotRequired[datetime]
    ReadyDateTime: NotRequired[datetime]
    EndDateTime: NotRequired[datetime]

class JobFlowExecutionStatusDetailTypeDef(TypedDict):
    State: JobFlowExecutionStateType
    CreationDateTime: datetime
    StartDateTime: NotRequired[datetime]
    ReadyDateTime: NotRequired[datetime]
    EndDateTime: NotRequired[datetime]
    LastStateChangeReason: NotRequired[str]

class PlacementTypeOutputTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    AvailabilityZones: NotRequired[List[str]]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListBootstrapActionsInputTypeDef(TypedDict):
    ClusterId: str
    Marker: NotRequired[str]

class ListInstanceFleetsInputTypeDef(TypedDict):
    ClusterId: str
    Marker: NotRequired[str]

class ListInstanceGroupsInputTypeDef(TypedDict):
    ClusterId: str
    Marker: NotRequired[str]

class ListInstancesInputTypeDef(TypedDict):
    ClusterId: str
    InstanceGroupId: NotRequired[str]
    InstanceGroupTypes: NotRequired[Sequence[InstanceGroupTypeType]]
    InstanceFleetId: NotRequired[str]
    InstanceFleetType: NotRequired[InstanceFleetTypeType]
    InstanceStates: NotRequired[Sequence[InstanceStateType]]
    Marker: NotRequired[str]

class ReleaseLabelFilterTypeDef(TypedDict):
    Prefix: NotRequired[str]
    Application: NotRequired[str]

class ListSecurityConfigurationsInputTypeDef(TypedDict):
    Marker: NotRequired[str]

class SecurityConfigurationSummaryTypeDef(TypedDict):
    Name: NotRequired[str]
    CreationDateTime: NotRequired[datetime]

class ListStepsInputTypeDef(TypedDict):
    ClusterId: str
    StepStates: NotRequired[Sequence[StepStateType]]
    StepIds: NotRequired[Sequence[str]]
    Marker: NotRequired[str]

class ListStudioSessionMappingsInputTypeDef(TypedDict):
    StudioId: NotRequired[str]
    IdentityType: NotRequired[IdentityTypeType]
    Marker: NotRequired[str]

class SessionMappingSummaryTypeDef(TypedDict):
    StudioId: NotRequired[str]
    IdentityId: NotRequired[str]
    IdentityName: NotRequired[str]
    IdentityType: NotRequired[IdentityTypeType]
    SessionPolicyArn: NotRequired[str]
    CreationTime: NotRequired[datetime]

class ListStudiosInputTypeDef(TypedDict):
    Marker: NotRequired[str]

class StudioSummaryTypeDef(TypedDict):
    StudioId: NotRequired[str]
    Name: NotRequired[str]
    VpcId: NotRequired[str]
    Description: NotRequired[str]
    Url: NotRequired[str]
    AuthMode: NotRequired[AuthModeType]
    CreationTime: NotRequired[datetime]

class ListSupportedInstanceTypesInputTypeDef(TypedDict):
    ReleaseLabel: str
    Marker: NotRequired[str]

SupportedInstanceTypeTypeDef = TypedDict(
    "SupportedInstanceTypeTypeDef",
    {
        "Type": NotRequired[str],
        "MemoryGB": NotRequired[float],
        "StorageGB": NotRequired[int],
        "VCPU": NotRequired[int],
        "Is64BitsOnly": NotRequired[bool],
        "InstanceFamilyId": NotRequired[str],
        "EbsOptimizedAvailable": NotRequired[bool],
        "EbsOptimizedByDefault": NotRequired[bool],
        "NumberOfDisks": NotRequired[int],
        "EbsStorageOnly": NotRequired[bool],
        "Architecture": NotRequired[str],
    },
)

class ModifyClusterInputTypeDef(TypedDict):
    ClusterId: str
    StepConcurrencyLevel: NotRequired[int]

class NotebookS3LocationForOutputTypeDef(TypedDict):
    Bucket: NotRequired[str]
    Key: NotRequired[str]

class OutputNotebookS3LocationForOutputTypeDef(TypedDict):
    Bucket: NotRequired[str]
    Key: NotRequired[str]

class NotebookS3LocationFromInputTypeDef(TypedDict):
    Bucket: NotRequired[str]
    Key: NotRequired[str]

class OnDemandCapacityReservationOptionsTypeDef(TypedDict):
    UsageStrategy: NotRequired[Literal["use-capacity-reservations-first"]]
    CapacityReservationPreference: NotRequired[OnDemandCapacityReservationPreferenceType]
    CapacityReservationResourceGroupArn: NotRequired[str]

class OutputNotebookS3LocationFromInputTypeDef(TypedDict):
    Bucket: NotRequired[str]
    Key: NotRequired[str]

class PlacementTypeTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    AvailabilityZones: NotRequired[Sequence[str]]

class RemoveAutoScalingPolicyInputTypeDef(TypedDict):
    ClusterId: str
    InstanceGroupId: str

class RemoveAutoTerminationPolicyInputTypeDef(TypedDict):
    ClusterId: str

class RemoveManagedScalingPolicyInputTypeDef(TypedDict):
    ClusterId: str

class RemoveTagsInputTypeDef(TypedDict):
    ResourceId: str
    TagKeys: Sequence[str]

class SupportedProductConfigTypeDef(TypedDict):
    Name: NotRequired[str]
    Args: NotRequired[Sequence[str]]

class SimpleScalingPolicyConfigurationTypeDef(TypedDict):
    ScalingAdjustment: int
    AdjustmentType: NotRequired[AdjustmentTypeType]
    CoolDown: NotRequired[int]

class ScriptBootstrapActionConfigTypeDef(TypedDict):
    Path: str
    Args: NotRequired[Sequence[str]]

class SetKeepJobFlowAliveWhenNoStepsInputTypeDef(TypedDict):
    JobFlowIds: Sequence[str]
    KeepJobFlowAliveWhenNoSteps: bool

class SetTerminationProtectionInputTypeDef(TypedDict):
    JobFlowIds: Sequence[str]
    TerminationProtected: bool

class SetUnhealthyNodeReplacementInputTypeDef(TypedDict):
    JobFlowIds: Sequence[str]
    UnhealthyNodeReplacement: bool

class SetVisibleToAllUsersInputTypeDef(TypedDict):
    JobFlowIds: Sequence[str]
    VisibleToAllUsers: bool

class StepExecutionStatusDetailTypeDef(TypedDict):
    State: StepExecutionStateType
    CreationDateTime: datetime
    StartDateTime: NotRequired[datetime]
    EndDateTime: NotRequired[datetime]
    LastStateChangeReason: NotRequired[str]

class StepStateChangeReasonTypeDef(TypedDict):
    Code: NotRequired[Literal["NONE"]]
    Message: NotRequired[str]

class StepTimelineTypeDef(TypedDict):
    CreationDateTime: NotRequired[datetime]
    StartDateTime: NotRequired[datetime]
    EndDateTime: NotRequired[datetime]

class StopNotebookExecutionInputTypeDef(TypedDict):
    NotebookExecutionId: str

class TerminateJobFlowsInputTypeDef(TypedDict):
    JobFlowIds: Sequence[str]

class UpdateStudioInputTypeDef(TypedDict):
    StudioId: str
    Name: NotRequired[str]
    Description: NotRequired[str]
    SubnetIds: NotRequired[Sequence[str]]
    DefaultS3Location: NotRequired[str]
    EncryptionKeyArn: NotRequired[str]

class UpdateStudioSessionMappingInputTypeDef(TypedDict):
    StudioId: str
    IdentityType: IdentityTypeType
    SessionPolicyArn: str
    IdentityId: NotRequired[str]
    IdentityName: NotRequired[str]

class AddInstanceFleetOutputTypeDef(TypedDict):
    ClusterId: str
    InstanceFleetId: str
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class AddInstanceGroupsOutputTypeDef(TypedDict):
    JobFlowId: str
    InstanceGroupIds: List[str]
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class AddJobFlowStepsOutputTypeDef(TypedDict):
    StepIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateSecurityConfigurationOutputTypeDef(TypedDict):
    Name: str
    CreationDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateStudioOutputTypeDef(TypedDict):
    StudioId: str
    Url: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeSecurityConfigurationOutputTypeDef(TypedDict):
    Name: str
    SecurityConfiguration: str
    CreationDateTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListReleaseLabelsOutputTypeDef(TypedDict):
    ReleaseLabels: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ModifyClusterOutputTypeDef(TypedDict):
    StepConcurrencyLevel: int
    ResponseMetadata: ResponseMetadataTypeDef

class RunJobFlowOutputTypeDef(TypedDict):
    JobFlowId: str
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartNotebookExecutionOutputTypeDef(TypedDict):
    NotebookExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class AddTagsInputTypeDef(TypedDict):
    ResourceId: str
    Tags: Sequence[TagTypeDef]

class CreateStudioInputTypeDef(TypedDict):
    Name: str
    AuthMode: AuthModeType
    VpcId: str
    SubnetIds: Sequence[str]
    ServiceRole: str
    WorkspaceSecurityGroupId: str
    EngineSecurityGroupId: str
    DefaultS3Location: str
    Description: NotRequired[str]
    UserRole: NotRequired[str]
    IdpAuthUrl: NotRequired[str]
    IdpRelayStateParameterName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    TrustedIdentityPropagationEnabled: NotRequired[bool]
    IdcUserAssignment: NotRequired[IdcUserAssignmentType]
    IdcInstanceArn: NotRequired[str]
    EncryptionKeyArn: NotRequired[str]

class StudioTypeDef(TypedDict):
    StudioId: NotRequired[str]
    StudioArn: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    AuthMode: NotRequired[AuthModeType]
    VpcId: NotRequired[str]
    SubnetIds: NotRequired[List[str]]
    ServiceRole: NotRequired[str]
    UserRole: NotRequired[str]
    WorkspaceSecurityGroupId: NotRequired[str]
    EngineSecurityGroupId: NotRequired[str]
    Url: NotRequired[str]
    CreationTime: NotRequired[datetime]
    DefaultS3Location: NotRequired[str]
    IdpAuthUrl: NotRequired[str]
    IdpRelayStateParameterName: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]
    IdcInstanceArn: NotRequired[str]
    TrustedIdentityPropagationEnabled: NotRequired[bool]
    IdcUserAssignment: NotRequired[IdcUserAssignmentType]
    EncryptionKeyArn: NotRequired[str]

ApplicationUnionTypeDef = Union[ApplicationTypeDef, ApplicationOutputTypeDef]

class AutoScalingPolicyStatusTypeDef(TypedDict):
    State: NotRequired[AutoScalingPolicyStateType]
    StateChangeReason: NotRequired[AutoScalingPolicyStateChangeReasonTypeDef]

class GetAutoTerminationPolicyOutputTypeDef(TypedDict):
    AutoTerminationPolicy: AutoTerminationPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutAutoTerminationPolicyInputTypeDef(TypedDict):
    ClusterId: str
    AutoTerminationPolicy: NotRequired[AutoTerminationPolicyTypeDef]

class BlockPublicAccessConfigurationOutputTypeDef(TypedDict):
    BlockPublicSecurityGroupRules: bool
    PermittedPublicSecurityGroupRuleRanges: NotRequired[List[PortRangeTypeDef]]

class BlockPublicAccessConfigurationTypeDef(TypedDict):
    BlockPublicSecurityGroupRules: bool
    PermittedPublicSecurityGroupRuleRanges: NotRequired[Sequence[PortRangeTypeDef]]

class BootstrapActionConfigOutputTypeDef(TypedDict):
    Name: str
    ScriptBootstrapAction: ScriptBootstrapActionConfigOutputTypeDef

class CancelStepsOutputTypeDef(TypedDict):
    CancelStepsInfoList: List[CancelStepsInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CloudWatchAlarmDefinitionOutputTypeDef(TypedDict):
    ComparisonOperator: ComparisonOperatorType
    MetricName: str
    Period: int
    Threshold: float
    EvaluationPeriods: NotRequired[int]
    Namespace: NotRequired[str]
    Statistic: NotRequired[StatisticType]
    Unit: NotRequired[UnitType]
    Dimensions: NotRequired[List[MetricDimensionTypeDef]]

class CloudWatchAlarmDefinitionTypeDef(TypedDict):
    ComparisonOperator: ComparisonOperatorType
    MetricName: str
    Period: int
    Threshold: float
    EvaluationPeriods: NotRequired[int]
    Namespace: NotRequired[str]
    Statistic: NotRequired[StatisticType]
    Unit: NotRequired[UnitType]
    Dimensions: NotRequired[Sequence[MetricDimensionTypeDef]]

class ClusterStatusTypeDef(TypedDict):
    State: NotRequired[ClusterStateType]
    StateChangeReason: NotRequired[ClusterStateChangeReasonTypeDef]
    Timeline: NotRequired[ClusterTimelineTypeDef]
    ErrorDetails: NotRequired[List[ErrorDetailTypeDef]]

class ListBootstrapActionsOutputTypeDef(TypedDict):
    BootstrapActions: List[CommandTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class ManagedScalingPolicyTypeDef(TypedDict):
    ComputeLimits: NotRequired[ComputeLimitsTypeDef]
    UtilizationPerformanceIndex: NotRequired[int]
    ScalingStrategy: NotRequired[ScalingStrategyType]

ConfigurationUnionTypeDef = Union[ConfigurationTypeDef, ConfigurationOutputTypeDef]

class CredentialsTypeDef(TypedDict):
    UsernamePassword: NotRequired[UsernamePasswordTypeDef]

class DescribeClusterInputWaitExtraTypeDef(TypedDict):
    ClusterId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeClusterInputWaitTypeDef(TypedDict):
    ClusterId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeStepInputWaitTypeDef(TypedDict):
    ClusterId: str
    StepId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeJobFlowsInputTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    JobFlowIds: NotRequired[Sequence[str]]
    JobFlowStates: NotRequired[Sequence[JobFlowExecutionStateType]]

class ListClustersInputTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    ClusterStates: NotRequired[Sequence[ClusterStateType]]
    Marker: NotRequired[str]

class ListNotebookExecutionsInputTypeDef(TypedDict):
    EditorId: NotRequired[str]
    Status: NotRequired[NotebookExecutionStatusType]
    From: NotRequired[TimestampTypeDef]
    To: NotRequired[TimestampTypeDef]
    Marker: NotRequired[str]
    ExecutionEngineId: NotRequired[str]

class DescribeReleaseLabelOutputTypeDef(TypedDict):
    ReleaseLabel: str
    Applications: List[SimplifiedApplicationTypeDef]
    AvailableOSReleases: List[OSReleaseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class EbsBlockDeviceConfigTypeDef(TypedDict):
    VolumeSpecification: VolumeSpecificationTypeDef
    VolumesPerInstance: NotRequired[int]

class EbsBlockDeviceTypeDef(TypedDict):
    VolumeSpecification: NotRequired[VolumeSpecificationTypeDef]
    Device: NotRequired[str]

class GetStudioSessionMappingOutputTypeDef(TypedDict):
    SessionMapping: SessionMappingDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class HadoopJarStepConfigOutputTypeDef(TypedDict):
    Jar: str
    Properties: NotRequired[List[KeyValueTypeDef]]
    MainClass: NotRequired[str]
    Args: NotRequired[List[str]]

class HadoopJarStepConfigTypeDef(TypedDict):
    Jar: str
    Properties: NotRequired[Sequence[KeyValueTypeDef]]
    MainClass: NotRequired[str]
    Args: NotRequired[Sequence[str]]

class InstanceFleetStatusTypeDef(TypedDict):
    State: NotRequired[InstanceFleetStateType]
    StateChangeReason: NotRequired[InstanceFleetStateChangeReasonTypeDef]
    Timeline: NotRequired[InstanceFleetTimelineTypeDef]

class InstanceGroupStatusTypeDef(TypedDict):
    State: NotRequired[InstanceGroupStateType]
    StateChangeReason: NotRequired[InstanceGroupStateChangeReasonTypeDef]
    Timeline: NotRequired[InstanceGroupTimelineTypeDef]

class ShrinkPolicyOutputTypeDef(TypedDict):
    DecommissionTimeout: NotRequired[int]
    InstanceResizePolicy: NotRequired[InstanceResizePolicyOutputTypeDef]

InstanceResizePolicyUnionTypeDef = Union[
    InstanceResizePolicyTypeDef, InstanceResizePolicyOutputTypeDef
]

class InstanceStatusTypeDef(TypedDict):
    State: NotRequired[InstanceStateType]
    StateChangeReason: NotRequired[InstanceStateChangeReasonTypeDef]
    Timeline: NotRequired[InstanceTimelineTypeDef]

class JobFlowInstancesDetailTypeDef(TypedDict):
    MasterInstanceType: str
    SlaveInstanceType: str
    InstanceCount: int
    MasterPublicDnsName: NotRequired[str]
    MasterInstanceId: NotRequired[str]
    InstanceGroups: NotRequired[List[InstanceGroupDetailTypeDef]]
    NormalizedInstanceHours: NotRequired[int]
    Ec2KeyName: NotRequired[str]
    Ec2SubnetId: NotRequired[str]
    Placement: NotRequired[PlacementTypeOutputTypeDef]
    KeepJobFlowAliveWhenNoSteps: NotRequired[bool]
    TerminationProtected: NotRequired[bool]
    UnhealthyNodeReplacement: NotRequired[bool]
    HadoopVersion: NotRequired[str]

class ListBootstrapActionsInputPaginateTypeDef(TypedDict):
    ClusterId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListClustersInputPaginateTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    ClusterStates: NotRequired[Sequence[ClusterStateType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInstanceFleetsInputPaginateTypeDef(TypedDict):
    ClusterId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInstanceGroupsInputPaginateTypeDef(TypedDict):
    ClusterId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInstancesInputPaginateTypeDef(TypedDict):
    ClusterId: str
    InstanceGroupId: NotRequired[str]
    InstanceGroupTypes: NotRequired[Sequence[InstanceGroupTypeType]]
    InstanceFleetId: NotRequired[str]
    InstanceFleetType: NotRequired[InstanceFleetTypeType]
    InstanceStates: NotRequired[Sequence[InstanceStateType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNotebookExecutionsInputPaginateTypeDef(TypedDict):
    EditorId: NotRequired[str]
    Status: NotRequired[NotebookExecutionStatusType]
    From: NotRequired[TimestampTypeDef]
    To: NotRequired[TimestampTypeDef]
    ExecutionEngineId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSecurityConfigurationsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStepsInputPaginateTypeDef(TypedDict):
    ClusterId: str
    StepStates: NotRequired[Sequence[StepStateType]]
    StepIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStudioSessionMappingsInputPaginateTypeDef(TypedDict):
    StudioId: NotRequired[str]
    IdentityType: NotRequired[IdentityTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListStudiosInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListReleaseLabelsInputTypeDef(TypedDict):
    Filters: NotRequired[ReleaseLabelFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListSecurityConfigurationsOutputTypeDef(TypedDict):
    SecurityConfigurations: List[SecurityConfigurationSummaryTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListStudioSessionMappingsOutputTypeDef(TypedDict):
    SessionMappings: List[SessionMappingSummaryTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListStudiosOutputTypeDef(TypedDict):
    Studios: List[StudioSummaryTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListSupportedInstanceTypesOutputTypeDef(TypedDict):
    SupportedInstanceTypes: List[SupportedInstanceTypeTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class NotebookExecutionSummaryTypeDef(TypedDict):
    NotebookExecutionId: NotRequired[str]
    EditorId: NotRequired[str]
    NotebookExecutionName: NotRequired[str]
    Status: NotRequired[NotebookExecutionStatusType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    NotebookS3Location: NotRequired[NotebookS3LocationForOutputTypeDef]
    ExecutionEngineId: NotRequired[str]

class NotebookExecutionTypeDef(TypedDict):
    NotebookExecutionId: NotRequired[str]
    EditorId: NotRequired[str]
    ExecutionEngine: NotRequired[ExecutionEngineConfigTypeDef]
    NotebookExecutionName: NotRequired[str]
    NotebookParams: NotRequired[str]
    Status: NotRequired[NotebookExecutionStatusType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    Arn: NotRequired[str]
    OutputNotebookURI: NotRequired[str]
    LastStateChangeReason: NotRequired[str]
    NotebookInstanceSecurityGroupId: NotRequired[str]
    Tags: NotRequired[List[TagTypeDef]]
    NotebookS3Location: NotRequired[NotebookS3LocationForOutputTypeDef]
    OutputNotebookS3Location: NotRequired[OutputNotebookS3LocationForOutputTypeDef]
    OutputNotebookFormat: NotRequired[Literal["HTML"]]
    EnvironmentVariables: NotRequired[Dict[str, str]]

class OnDemandProvisioningSpecificationTypeDef(TypedDict):
    AllocationStrategy: OnDemandProvisioningAllocationStrategyType
    CapacityReservationOptions: NotRequired[OnDemandCapacityReservationOptionsTypeDef]

class OnDemandResizingSpecificationTypeDef(TypedDict):
    TimeoutDurationMinutes: NotRequired[int]
    AllocationStrategy: NotRequired[OnDemandProvisioningAllocationStrategyType]
    CapacityReservationOptions: NotRequired[OnDemandCapacityReservationOptionsTypeDef]

class StartNotebookExecutionInputTypeDef(TypedDict):
    ExecutionEngine: ExecutionEngineConfigTypeDef
    ServiceRole: str
    EditorId: NotRequired[str]
    RelativePath: NotRequired[str]
    NotebookExecutionName: NotRequired[str]
    NotebookParams: NotRequired[str]
    NotebookInstanceSecurityGroupId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    NotebookS3Location: NotRequired[NotebookS3LocationFromInputTypeDef]
    OutputNotebookS3Location: NotRequired[OutputNotebookS3LocationFromInputTypeDef]
    OutputNotebookFormat: NotRequired[Literal["HTML"]]
    EnvironmentVariables: NotRequired[Mapping[str, str]]

PlacementTypeUnionTypeDef = Union[PlacementTypeTypeDef, PlacementTypeOutputTypeDef]

class ScalingActionTypeDef(TypedDict):
    SimpleScalingPolicyConfiguration: SimpleScalingPolicyConfigurationTypeDef
    Market: NotRequired[MarketTypeType]

ScriptBootstrapActionConfigUnionTypeDef = Union[
    ScriptBootstrapActionConfigTypeDef, ScriptBootstrapActionConfigOutputTypeDef
]

class StepStatusTypeDef(TypedDict):
    State: NotRequired[StepStateType]
    StateChangeReason: NotRequired[StepStateChangeReasonTypeDef]
    FailureDetails: NotRequired[FailureDetailsTypeDef]
    Timeline: NotRequired[StepTimelineTypeDef]

class DescribeStudioOutputTypeDef(TypedDict):
    Studio: StudioTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetBlockPublicAccessConfigurationOutputTypeDef(TypedDict):
    BlockPublicAccessConfiguration: BlockPublicAccessConfigurationOutputTypeDef
    BlockPublicAccessConfigurationMetadata: BlockPublicAccessConfigurationMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

BlockPublicAccessConfigurationUnionTypeDef = Union[
    BlockPublicAccessConfigurationTypeDef, BlockPublicAccessConfigurationOutputTypeDef
]

class BootstrapActionDetailTypeDef(TypedDict):
    BootstrapActionConfig: NotRequired[BootstrapActionConfigOutputTypeDef]

class ScalingTriggerOutputTypeDef(TypedDict):
    CloudWatchAlarmDefinition: CloudWatchAlarmDefinitionOutputTypeDef

CloudWatchAlarmDefinitionUnionTypeDef = Union[
    CloudWatchAlarmDefinitionTypeDef, CloudWatchAlarmDefinitionOutputTypeDef
]

class ClusterSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[ClusterStatusTypeDef]
    NormalizedInstanceHours: NotRequired[int]
    ClusterArn: NotRequired[str]
    OutpostArn: NotRequired[str]

class ClusterTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[ClusterStatusTypeDef]
    Ec2InstanceAttributes: NotRequired[Ec2InstanceAttributesTypeDef]
    InstanceCollectionType: NotRequired[InstanceCollectionTypeType]
    LogUri: NotRequired[str]
    LogEncryptionKmsKeyId: NotRequired[str]
    RequestedAmiVersion: NotRequired[str]
    RunningAmiVersion: NotRequired[str]
    ReleaseLabel: NotRequired[str]
    AutoTerminate: NotRequired[bool]
    TerminationProtected: NotRequired[bool]
    UnhealthyNodeReplacement: NotRequired[bool]
    VisibleToAllUsers: NotRequired[bool]
    Applications: NotRequired[List[ApplicationOutputTypeDef]]
    Tags: NotRequired[List[TagTypeDef]]
    ServiceRole: NotRequired[str]
    NormalizedInstanceHours: NotRequired[int]
    MasterPublicDnsName: NotRequired[str]
    Configurations: NotRequired[List[ConfigurationOutputTypeDef]]
    SecurityConfiguration: NotRequired[str]
    AutoScalingRole: NotRequired[str]
    ScaleDownBehavior: NotRequired[ScaleDownBehaviorType]
    CustomAmiId: NotRequired[str]
    EbsRootVolumeSize: NotRequired[int]
    RepoUpgradeOnBoot: NotRequired[RepoUpgradeOnBootType]
    KerberosAttributes: NotRequired[KerberosAttributesTypeDef]
    ClusterArn: NotRequired[str]
    OutpostArn: NotRequired[str]
    StepConcurrencyLevel: NotRequired[int]
    PlacementGroups: NotRequired[List[PlacementGroupConfigTypeDef]]
    OSReleaseLabel: NotRequired[str]
    EbsRootVolumeIops: NotRequired[int]
    EbsRootVolumeThroughput: NotRequired[int]

class GetManagedScalingPolicyOutputTypeDef(TypedDict):
    ManagedScalingPolicy: ManagedScalingPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutManagedScalingPolicyInputTypeDef(TypedDict):
    ClusterId: str
    ManagedScalingPolicy: ManagedScalingPolicyTypeDef

class GetClusterSessionCredentialsOutputTypeDef(TypedDict):
    Credentials: CredentialsTypeDef
    ExpiresAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class EbsConfigurationTypeDef(TypedDict):
    EbsBlockDeviceConfigs: NotRequired[Sequence[EbsBlockDeviceConfigTypeDef]]
    EbsOptimized: NotRequired[bool]

class InstanceTypeSpecificationPaginatorTypeDef(TypedDict):
    InstanceType: NotRequired[str]
    WeightedCapacity: NotRequired[int]
    BidPrice: NotRequired[str]
    BidPriceAsPercentageOfOnDemandPrice: NotRequired[float]
    Configurations: NotRequired[List[ConfigurationPaginatorTypeDef]]
    EbsBlockDevices: NotRequired[List[EbsBlockDeviceTypeDef]]
    EbsOptimized: NotRequired[bool]
    CustomAmiId: NotRequired[str]
    Priority: NotRequired[float]

class InstanceTypeSpecificationTypeDef(TypedDict):
    InstanceType: NotRequired[str]
    WeightedCapacity: NotRequired[int]
    BidPrice: NotRequired[str]
    BidPriceAsPercentageOfOnDemandPrice: NotRequired[float]
    Configurations: NotRequired[List[ConfigurationOutputTypeDef]]
    EbsBlockDevices: NotRequired[List[EbsBlockDeviceTypeDef]]
    EbsOptimized: NotRequired[bool]
    CustomAmiId: NotRequired[str]
    Priority: NotRequired[float]

class StepConfigOutputTypeDef(TypedDict):
    Name: str
    HadoopJarStep: HadoopJarStepConfigOutputTypeDef
    ActionOnFailure: NotRequired[ActionOnFailureType]

HadoopJarStepConfigUnionTypeDef = Union[
    HadoopJarStepConfigTypeDef, HadoopJarStepConfigOutputTypeDef
]

class ShrinkPolicyTypeDef(TypedDict):
    DecommissionTimeout: NotRequired[int]
    InstanceResizePolicy: NotRequired[InstanceResizePolicyUnionTypeDef]

class InstanceTypeDef(TypedDict):
    Id: NotRequired[str]
    Ec2InstanceId: NotRequired[str]
    PublicDnsName: NotRequired[str]
    PublicIpAddress: NotRequired[str]
    PrivateDnsName: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    Status: NotRequired[InstanceStatusTypeDef]
    InstanceGroupId: NotRequired[str]
    InstanceFleetId: NotRequired[str]
    Market: NotRequired[MarketTypeType]
    InstanceType: NotRequired[str]
    EbsVolumes: NotRequired[List[EbsVolumeTypeDef]]

class ListNotebookExecutionsOutputTypeDef(TypedDict):
    NotebookExecutions: List[NotebookExecutionSummaryTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeNotebookExecutionOutputTypeDef(TypedDict):
    NotebookExecution: NotebookExecutionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class InstanceFleetProvisioningSpecificationsTypeDef(TypedDict):
    SpotSpecification: NotRequired[SpotProvisioningSpecificationTypeDef]
    OnDemandSpecification: NotRequired[OnDemandProvisioningSpecificationTypeDef]

class InstanceFleetResizingSpecificationsTypeDef(TypedDict):
    SpotResizeSpecification: NotRequired[SpotResizingSpecificationTypeDef]
    OnDemandResizeSpecification: NotRequired[OnDemandResizingSpecificationTypeDef]

class BootstrapActionConfigTypeDef(TypedDict):
    Name: str
    ScriptBootstrapAction: ScriptBootstrapActionConfigUnionTypeDef

class StepSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Config: NotRequired[HadoopStepConfigTypeDef]
    ActionOnFailure: NotRequired[ActionOnFailureType]
    Status: NotRequired[StepStatusTypeDef]

class StepTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Config: NotRequired[HadoopStepConfigTypeDef]
    ActionOnFailure: NotRequired[ActionOnFailureType]
    Status: NotRequired[StepStatusTypeDef]
    ExecutionRoleArn: NotRequired[str]

class PutBlockPublicAccessConfigurationInputTypeDef(TypedDict):
    BlockPublicAccessConfiguration: BlockPublicAccessConfigurationUnionTypeDef

class ScalingRuleOutputTypeDef(TypedDict):
    Name: str
    Action: ScalingActionTypeDef
    Trigger: ScalingTriggerOutputTypeDef
    Description: NotRequired[str]

class ScalingTriggerTypeDef(TypedDict):
    CloudWatchAlarmDefinition: CloudWatchAlarmDefinitionUnionTypeDef

class ListClustersOutputTypeDef(TypedDict):
    Clusters: List[ClusterSummaryTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeClusterOutputTypeDef(TypedDict):
    Cluster: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class InstanceTypeConfigTypeDef(TypedDict):
    InstanceType: str
    WeightedCapacity: NotRequired[int]
    BidPrice: NotRequired[str]
    BidPriceAsPercentageOfOnDemandPrice: NotRequired[float]
    EbsConfiguration: NotRequired[EbsConfigurationTypeDef]
    Configurations: NotRequired[Sequence[ConfigurationUnionTypeDef]]
    CustomAmiId: NotRequired[str]
    Priority: NotRequired[float]

class StepDetailTypeDef(TypedDict):
    StepConfig: StepConfigOutputTypeDef
    ExecutionStatusDetail: StepExecutionStatusDetailTypeDef

class StepConfigTypeDef(TypedDict):
    Name: str
    HadoopJarStep: HadoopJarStepConfigUnionTypeDef
    ActionOnFailure: NotRequired[ActionOnFailureType]

ShrinkPolicyUnionTypeDef = Union[ShrinkPolicyTypeDef, ShrinkPolicyOutputTypeDef]

class ListInstancesOutputTypeDef(TypedDict):
    Instances: List[InstanceTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class InstanceFleetPaginatorTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[InstanceFleetStatusTypeDef]
    InstanceFleetType: NotRequired[InstanceFleetTypeType]
    TargetOnDemandCapacity: NotRequired[int]
    TargetSpotCapacity: NotRequired[int]
    ProvisionedOnDemandCapacity: NotRequired[int]
    ProvisionedSpotCapacity: NotRequired[int]
    InstanceTypeSpecifications: NotRequired[List[InstanceTypeSpecificationPaginatorTypeDef]]
    LaunchSpecifications: NotRequired[InstanceFleetProvisioningSpecificationsTypeDef]
    ResizeSpecifications: NotRequired[InstanceFleetResizingSpecificationsTypeDef]
    Context: NotRequired[str]

class InstanceFleetTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[InstanceFleetStatusTypeDef]
    InstanceFleetType: NotRequired[InstanceFleetTypeType]
    TargetOnDemandCapacity: NotRequired[int]
    TargetSpotCapacity: NotRequired[int]
    ProvisionedOnDemandCapacity: NotRequired[int]
    ProvisionedSpotCapacity: NotRequired[int]
    InstanceTypeSpecifications: NotRequired[List[InstanceTypeSpecificationTypeDef]]
    LaunchSpecifications: NotRequired[InstanceFleetProvisioningSpecificationsTypeDef]
    ResizeSpecifications: NotRequired[InstanceFleetResizingSpecificationsTypeDef]
    Context: NotRequired[str]

BootstrapActionConfigUnionTypeDef = Union[
    BootstrapActionConfigTypeDef, BootstrapActionConfigOutputTypeDef
]

class ListStepsOutputTypeDef(TypedDict):
    Steps: List[StepSummaryTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeStepOutputTypeDef(TypedDict):
    Step: StepTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AutoScalingPolicyDescriptionTypeDef(TypedDict):
    Status: NotRequired[AutoScalingPolicyStatusTypeDef]
    Constraints: NotRequired[ScalingConstraintsTypeDef]
    Rules: NotRequired[List[ScalingRuleOutputTypeDef]]

ScalingTriggerUnionTypeDef = Union[ScalingTriggerTypeDef, ScalingTriggerOutputTypeDef]

class InstanceFleetConfigTypeDef(TypedDict):
    InstanceFleetType: InstanceFleetTypeType
    Name: NotRequired[str]
    TargetOnDemandCapacity: NotRequired[int]
    TargetSpotCapacity: NotRequired[int]
    InstanceTypeConfigs: NotRequired[Sequence[InstanceTypeConfigTypeDef]]
    LaunchSpecifications: NotRequired[InstanceFleetProvisioningSpecificationsTypeDef]
    ResizeSpecifications: NotRequired[InstanceFleetResizingSpecificationsTypeDef]
    Context: NotRequired[str]

class InstanceFleetModifyConfigTypeDef(TypedDict):
    InstanceFleetId: str
    TargetOnDemandCapacity: NotRequired[int]
    TargetSpotCapacity: NotRequired[int]
    ResizeSpecifications: NotRequired[InstanceFleetResizingSpecificationsTypeDef]
    InstanceTypeConfigs: NotRequired[Sequence[InstanceTypeConfigTypeDef]]
    Context: NotRequired[str]

class JobFlowDetailTypeDef(TypedDict):
    JobFlowId: str
    Name: str
    ExecutionStatusDetail: JobFlowExecutionStatusDetailTypeDef
    Instances: JobFlowInstancesDetailTypeDef
    LogUri: NotRequired[str]
    LogEncryptionKmsKeyId: NotRequired[str]
    AmiVersion: NotRequired[str]
    Steps: NotRequired[List[StepDetailTypeDef]]
    BootstrapActions: NotRequired[List[BootstrapActionDetailTypeDef]]
    SupportedProducts: NotRequired[List[str]]
    VisibleToAllUsers: NotRequired[bool]
    JobFlowRole: NotRequired[str]
    ServiceRole: NotRequired[str]
    AutoScalingRole: NotRequired[str]
    ScaleDownBehavior: NotRequired[ScaleDownBehaviorType]

StepConfigUnionTypeDef = Union[StepConfigTypeDef, StepConfigOutputTypeDef]

class InstanceGroupModifyConfigTypeDef(TypedDict):
    InstanceGroupId: str
    InstanceCount: NotRequired[int]
    EC2InstanceIdsToTerminate: NotRequired[Sequence[str]]
    ShrinkPolicy: NotRequired[ShrinkPolicyUnionTypeDef]
    ReconfigurationType: NotRequired[ReconfigurationTypeType]
    Configurations: NotRequired[Sequence[ConfigurationUnionTypeDef]]

class ListInstanceFleetsOutputPaginatorTypeDef(TypedDict):
    InstanceFleets: List[InstanceFleetPaginatorTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListInstanceFleetsOutputTypeDef(TypedDict):
    InstanceFleets: List[InstanceFleetTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class InstanceGroupPaginatorTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Market: NotRequired[MarketTypeType]
    InstanceGroupType: NotRequired[InstanceGroupTypeType]
    BidPrice: NotRequired[str]
    InstanceType: NotRequired[str]
    RequestedInstanceCount: NotRequired[int]
    RunningInstanceCount: NotRequired[int]
    Status: NotRequired[InstanceGroupStatusTypeDef]
    Configurations: NotRequired[List[ConfigurationPaginatorTypeDef]]
    ConfigurationsVersion: NotRequired[int]
    LastSuccessfullyAppliedConfigurations: NotRequired[List[ConfigurationPaginatorTypeDef]]
    LastSuccessfullyAppliedConfigurationsVersion: NotRequired[int]
    EbsBlockDevices: NotRequired[List[EbsBlockDeviceTypeDef]]
    EbsOptimized: NotRequired[bool]
    ShrinkPolicy: NotRequired[ShrinkPolicyOutputTypeDef]
    AutoScalingPolicy: NotRequired[AutoScalingPolicyDescriptionTypeDef]
    CustomAmiId: NotRequired[str]

class InstanceGroupTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    Market: NotRequired[MarketTypeType]
    InstanceGroupType: NotRequired[InstanceGroupTypeType]
    BidPrice: NotRequired[str]
    InstanceType: NotRequired[str]
    RequestedInstanceCount: NotRequired[int]
    RunningInstanceCount: NotRequired[int]
    Status: NotRequired[InstanceGroupStatusTypeDef]
    Configurations: NotRequired[List[ConfigurationOutputTypeDef]]
    ConfigurationsVersion: NotRequired[int]
    LastSuccessfullyAppliedConfigurations: NotRequired[List[ConfigurationOutputTypeDef]]
    LastSuccessfullyAppliedConfigurationsVersion: NotRequired[int]
    EbsBlockDevices: NotRequired[List[EbsBlockDeviceTypeDef]]
    EbsOptimized: NotRequired[bool]
    ShrinkPolicy: NotRequired[ShrinkPolicyOutputTypeDef]
    AutoScalingPolicy: NotRequired[AutoScalingPolicyDescriptionTypeDef]
    CustomAmiId: NotRequired[str]

class PutAutoScalingPolicyOutputTypeDef(TypedDict):
    ClusterId: str
    InstanceGroupId: str
    AutoScalingPolicy: AutoScalingPolicyDescriptionTypeDef
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ScalingRuleTypeDef(TypedDict):
    Name: str
    Action: ScalingActionTypeDef
    Trigger: ScalingTriggerUnionTypeDef
    Description: NotRequired[str]

class AddInstanceFleetInputTypeDef(TypedDict):
    ClusterId: str
    InstanceFleet: InstanceFleetConfigTypeDef

class ModifyInstanceFleetInputTypeDef(TypedDict):
    ClusterId: str
    InstanceFleet: InstanceFleetModifyConfigTypeDef

class DescribeJobFlowsOutputTypeDef(TypedDict):
    JobFlows: List[JobFlowDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AddJobFlowStepsInputTypeDef(TypedDict):
    JobFlowId: str
    Steps: Sequence[StepConfigUnionTypeDef]
    ExecutionRoleArn: NotRequired[str]

class ModifyInstanceGroupsInputTypeDef(TypedDict):
    ClusterId: NotRequired[str]
    InstanceGroups: NotRequired[Sequence[InstanceGroupModifyConfigTypeDef]]

class ListInstanceGroupsOutputPaginatorTypeDef(TypedDict):
    InstanceGroups: List[InstanceGroupPaginatorTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListInstanceGroupsOutputTypeDef(TypedDict):
    InstanceGroups: List[InstanceGroupTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef

ScalingRuleUnionTypeDef = Union[ScalingRuleTypeDef, ScalingRuleOutputTypeDef]

class AutoScalingPolicyTypeDef(TypedDict):
    Constraints: ScalingConstraintsTypeDef
    Rules: Sequence[ScalingRuleUnionTypeDef]

class InstanceGroupConfigTypeDef(TypedDict):
    InstanceRole: InstanceRoleTypeType
    InstanceType: str
    InstanceCount: int
    Name: NotRequired[str]
    Market: NotRequired[MarketTypeType]
    BidPrice: NotRequired[str]
    Configurations: NotRequired[Sequence[ConfigurationUnionTypeDef]]
    EbsConfiguration: NotRequired[EbsConfigurationTypeDef]
    AutoScalingPolicy: NotRequired[AutoScalingPolicyTypeDef]
    CustomAmiId: NotRequired[str]

class PutAutoScalingPolicyInputTypeDef(TypedDict):
    ClusterId: str
    InstanceGroupId: str
    AutoScalingPolicy: AutoScalingPolicyTypeDef

class AddInstanceGroupsInputTypeDef(TypedDict):
    InstanceGroups: Sequence[InstanceGroupConfigTypeDef]
    JobFlowId: str

class JobFlowInstancesConfigTypeDef(TypedDict):
    MasterInstanceType: NotRequired[str]
    SlaveInstanceType: NotRequired[str]
    InstanceCount: NotRequired[int]
    InstanceGroups: NotRequired[Sequence[InstanceGroupConfigTypeDef]]
    InstanceFleets: NotRequired[Sequence[InstanceFleetConfigTypeDef]]
    Ec2KeyName: NotRequired[str]
    Placement: NotRequired[PlacementTypeUnionTypeDef]
    KeepJobFlowAliveWhenNoSteps: NotRequired[bool]
    TerminationProtected: NotRequired[bool]
    UnhealthyNodeReplacement: NotRequired[bool]
    HadoopVersion: NotRequired[str]
    Ec2SubnetId: NotRequired[str]
    Ec2SubnetIds: NotRequired[Sequence[str]]
    EmrManagedMasterSecurityGroup: NotRequired[str]
    EmrManagedSlaveSecurityGroup: NotRequired[str]
    ServiceAccessSecurityGroup: NotRequired[str]
    AdditionalMasterSecurityGroups: NotRequired[Sequence[str]]
    AdditionalSlaveSecurityGroups: NotRequired[Sequence[str]]

class RunJobFlowInputTypeDef(TypedDict):
    Name: str
    Instances: JobFlowInstancesConfigTypeDef
    LogUri: NotRequired[str]
    LogEncryptionKmsKeyId: NotRequired[str]
    AdditionalInfo: NotRequired[str]
    AmiVersion: NotRequired[str]
    ReleaseLabel: NotRequired[str]
    Steps: NotRequired[Sequence[StepConfigUnionTypeDef]]
    BootstrapActions: NotRequired[Sequence[BootstrapActionConfigUnionTypeDef]]
    SupportedProducts: NotRequired[Sequence[str]]
    NewSupportedProducts: NotRequired[Sequence[SupportedProductConfigTypeDef]]
    Applications: NotRequired[Sequence[ApplicationUnionTypeDef]]
    Configurations: NotRequired[Sequence[ConfigurationUnionTypeDef]]
    VisibleToAllUsers: NotRequired[bool]
    JobFlowRole: NotRequired[str]
    ServiceRole: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SecurityConfiguration: NotRequired[str]
    AutoScalingRole: NotRequired[str]
    ScaleDownBehavior: NotRequired[ScaleDownBehaviorType]
    CustomAmiId: NotRequired[str]
    EbsRootVolumeSize: NotRequired[int]
    RepoUpgradeOnBoot: NotRequired[RepoUpgradeOnBootType]
    KerberosAttributes: NotRequired[KerberosAttributesTypeDef]
    StepConcurrencyLevel: NotRequired[int]
    ManagedScalingPolicy: NotRequired[ManagedScalingPolicyTypeDef]
    PlacementGroupConfigs: NotRequired[Sequence[PlacementGroupConfigTypeDef]]
    AutoTerminationPolicy: NotRequired[AutoTerminationPolicyTypeDef]
    OSReleaseLabel: NotRequired[str]
    EbsRootVolumeIops: NotRequired[int]
    EbsRootVolumeThroughput: NotRequired[int]
