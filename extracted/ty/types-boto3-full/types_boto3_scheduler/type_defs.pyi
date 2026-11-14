"""
Type annotations for scheduler service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_scheduler/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_scheduler.type_defs import AwsVpcConfigurationOutputTypeDef

    data: AwsVpcConfigurationOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    ActionAfterCompletionType,
    AssignPublicIpType,
    FlexibleTimeWindowModeType,
    LaunchTypeType,
    PlacementConstraintTypeType,
    PlacementStrategyTypeType,
    ScheduleGroupStateType,
    ScheduleStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AwsVpcConfigurationOutputTypeDef",
    "AwsVpcConfigurationTypeDef",
    "CapacityProviderStrategyItemTypeDef",
    "CreateScheduleGroupInputTypeDef",
    "CreateScheduleGroupOutputTypeDef",
    "CreateScheduleInputTypeDef",
    "CreateScheduleOutputTypeDef",
    "DeadLetterConfigTypeDef",
    "DeleteScheduleGroupInputTypeDef",
    "DeleteScheduleInputTypeDef",
    "EcsParametersOutputTypeDef",
    "EcsParametersTypeDef",
    "EventBridgeParametersTypeDef",
    "EventBridgePutEventsV2ParametersTypeDef",
    "EventBridgePutRawEventsParametersOutputTypeDef",
    "EventBridgePutRawEventsParametersTypeDef",
    "FlexibleTimeWindowTypeDef",
    "GetScheduleGroupInputTypeDef",
    "GetScheduleGroupOutputTypeDef",
    "GetScheduleInputTypeDef",
    "GetScheduleOutputTypeDef",
    "KinesisParametersTypeDef",
    "ListScheduleGroupsInputPaginateTypeDef",
    "ListScheduleGroupsInputTypeDef",
    "ListScheduleGroupsOutputTypeDef",
    "ListSchedulesInputPaginateTypeDef",
    "ListSchedulesInputTypeDef",
    "ListSchedulesOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "NetworkConfigurationOutputTypeDef",
    "NetworkConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PlacementConstraintTypeDef",
    "PlacementStrategyTypeDef",
    "ResponseMetadataTypeDef",
    "RetryPolicyTypeDef",
    "SageMakerPipelineParameterTypeDef",
    "SageMakerPipelineParametersOutputTypeDef",
    "SageMakerPipelineParametersTypeDef",
    "ScheduleGroupSummaryTypeDef",
    "ScheduleSummaryTypeDef",
    "SqsParametersTypeDef",
    "TagResourceInputTypeDef",
    "TagTypeDef",
    "TargetOutputTypeDef",
    "TargetSummaryTypeDef",
    "TargetTypeDef",
    "TargetUnionTypeDef",
    "TimestampTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateScheduleInputTypeDef",
    "UpdateScheduleOutputTypeDef",
)

class AwsVpcConfigurationOutputTypeDef(TypedDict):
    Subnets: list[str]
    SecurityGroups: NotRequired[list[str]]
    AssignPublicIp: NotRequired[AssignPublicIpType]

class AwsVpcConfigurationTypeDef(TypedDict):
    Subnets: Sequence[str]
    SecurityGroups: NotRequired[Sequence[str]]
    AssignPublicIp: NotRequired[AssignPublicIpType]

class CapacityProviderStrategyItemTypeDef(TypedDict):
    capacityProvider: str
    weight: NotRequired[int]
    base: NotRequired[int]

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class FlexibleTimeWindowTypeDef(TypedDict):
    Mode: FlexibleTimeWindowModeType
    MaximumWindowInMinutes: NotRequired[int]

TimestampTypeDef = Union[datetime, str]

class DeadLetterConfigTypeDef(TypedDict):
    Arn: NotRequired[str]

class DeleteScheduleGroupInputTypeDef(TypedDict):
    Name: str
    ClientToken: NotRequired[str]

class DeleteScheduleInputTypeDef(TypedDict):
    Name: str
    GroupName: NotRequired[str]
    ClientToken: NotRequired[str]

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

class EventBridgeParametersTypeDef(TypedDict):
    DetailType: str
    Source: str

class EventBridgePutEventsV2ParametersTypeDef(TypedDict):
    DetailType: str
    Source: str

class EventBridgePutRawEventsParametersOutputTypeDef(TypedDict):
    Metadata: NotRequired[dict[str, str]]

class EventBridgePutRawEventsParametersTypeDef(TypedDict):
    Metadata: NotRequired[Mapping[str, str]]

class GetScheduleGroupInputTypeDef(TypedDict):
    Name: str

class GetScheduleInputTypeDef(TypedDict):
    Name: str
    GroupName: NotRequired[str]

class KinesisParametersTypeDef(TypedDict):
    PartitionKey: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListScheduleGroupsInputTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ScheduleGroupSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    State: NotRequired[ScheduleGroupStateType]
    CreationDate: NotRequired[datetime]
    LastModificationDate: NotRequired[datetime]

class ListSchedulesInputTypeDef(TypedDict):
    GroupName: NotRequired[str]
    NamePrefix: NotRequired[str]
    State: NotRequired[ScheduleStateType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class ListTagsForResourceInputTypeDef(TypedDict):
    ResourceArn: str

class RetryPolicyTypeDef(TypedDict):
    MaximumEventAgeInSeconds: NotRequired[int]
    MaximumRetryAttempts: NotRequired[int]

class SageMakerPipelineParameterTypeDef(TypedDict):
    Name: str
    Value: str

class TargetSummaryTypeDef(TypedDict):
    Arn: str

class SqsParametersTypeDef(TypedDict):
    MessageGroupId: NotRequired[str]

class UntagResourceInputTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class NetworkConfigurationOutputTypeDef(TypedDict):
    awsvpcConfiguration: NotRequired[AwsVpcConfigurationOutputTypeDef]

class NetworkConfigurationTypeDef(TypedDict):
    awsvpcConfiguration: NotRequired[AwsVpcConfigurationTypeDef]

class CreateScheduleGroupInputTypeDef(TypedDict):
    Name: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    ClientToken: NotRequired[str]

class TagResourceInputTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]

class CreateScheduleGroupOutputTypeDef(TypedDict):
    ScheduleGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateScheduleOutputTypeDef(TypedDict):
    ScheduleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetScheduleGroupOutputTypeDef(TypedDict):
    Arn: str
    Name: str
    State: ScheduleGroupStateType
    CreationDate: datetime
    LastModificationDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateScheduleOutputTypeDef(TypedDict):
    ScheduleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListScheduleGroupsInputPaginateTypeDef(TypedDict):
    NamePrefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSchedulesInputPaginateTypeDef(TypedDict):
    GroupName: NotRequired[str]
    NamePrefix: NotRequired[str]
    State: NotRequired[ScheduleStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListScheduleGroupsOutputTypeDef(TypedDict):
    ScheduleGroups: list[ScheduleGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class SageMakerPipelineParametersOutputTypeDef(TypedDict):
    PipelineParameterList: NotRequired[list[SageMakerPipelineParameterTypeDef]]

class SageMakerPipelineParametersTypeDef(TypedDict):
    PipelineParameterList: NotRequired[Sequence[SageMakerPipelineParameterTypeDef]]

class ScheduleSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    GroupName: NotRequired[str]
    State: NotRequired[ScheduleStateType]
    CreationDate: NotRequired[datetime]
    LastModificationDate: NotRequired[datetime]
    Target: NotRequired[TargetSummaryTypeDef]

class EcsParametersOutputTypeDef(TypedDict):
    TaskDefinitionArn: str
    TaskCount: NotRequired[int]
    LaunchType: NotRequired[LaunchTypeType]
    NetworkConfiguration: NotRequired[NetworkConfigurationOutputTypeDef]
    PlatformVersion: NotRequired[str]
    Group: NotRequired[str]
    CapacityProviderStrategy: NotRequired[list[CapacityProviderStrategyItemTypeDef]]
    EnableECSManagedTags: NotRequired[bool]
    EnableExecuteCommand: NotRequired[bool]
    PlacementConstraints: NotRequired[list[PlacementConstraintTypeDef]]
    PlacementStrategy: NotRequired[list[PlacementStrategyTypeDef]]
    PropagateTags: NotRequired[Literal["TASK_DEFINITION"]]
    ReferenceId: NotRequired[str]
    Tags: NotRequired[list[dict[str, str]]]

class EcsParametersTypeDef(TypedDict):
    TaskDefinitionArn: str
    TaskCount: NotRequired[int]
    LaunchType: NotRequired[LaunchTypeType]
    NetworkConfiguration: NotRequired[NetworkConfigurationTypeDef]
    PlatformVersion: NotRequired[str]
    Group: NotRequired[str]
    CapacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    EnableECSManagedTags: NotRequired[bool]
    EnableExecuteCommand: NotRequired[bool]
    PlacementConstraints: NotRequired[Sequence[PlacementConstraintTypeDef]]
    PlacementStrategy: NotRequired[Sequence[PlacementStrategyTypeDef]]
    PropagateTags: NotRequired[Literal["TASK_DEFINITION"]]
    ReferenceId: NotRequired[str]
    Tags: NotRequired[Sequence[Mapping[str, str]]]

class ListSchedulesOutputTypeDef(TypedDict):
    Schedules: list[ScheduleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TargetOutputTypeDef(TypedDict):
    Arn: str
    RoleArn: str
    DeadLetterConfig: NotRequired[DeadLetterConfigTypeDef]
    RetryPolicy: NotRequired[RetryPolicyTypeDef]
    Input: NotRequired[str]
    EcsParameters: NotRequired[EcsParametersOutputTypeDef]
    EventBridgeParameters: NotRequired[EventBridgeParametersTypeDef]
    EventBridgePutEventsV2Parameters: NotRequired[EventBridgePutEventsV2ParametersTypeDef]
    EventBridgePutRawEventsParameters: NotRequired[EventBridgePutRawEventsParametersOutputTypeDef]
    KinesisParameters: NotRequired[KinesisParametersTypeDef]
    SageMakerPipelineParameters: NotRequired[SageMakerPipelineParametersOutputTypeDef]
    SqsParameters: NotRequired[SqsParametersTypeDef]

class TargetTypeDef(TypedDict):
    Arn: str
    RoleArn: str
    DeadLetterConfig: NotRequired[DeadLetterConfigTypeDef]
    RetryPolicy: NotRequired[RetryPolicyTypeDef]
    Input: NotRequired[str]
    EcsParameters: NotRequired[EcsParametersTypeDef]
    EventBridgeParameters: NotRequired[EventBridgeParametersTypeDef]
    EventBridgePutEventsV2Parameters: NotRequired[EventBridgePutEventsV2ParametersTypeDef]
    EventBridgePutRawEventsParameters: NotRequired[EventBridgePutRawEventsParametersTypeDef]
    KinesisParameters: NotRequired[KinesisParametersTypeDef]
    SageMakerPipelineParameters: NotRequired[SageMakerPipelineParametersTypeDef]
    SqsParameters: NotRequired[SqsParametersTypeDef]

class GetScheduleOutputTypeDef(TypedDict):
    Arn: str
    GroupName: str
    Name: str
    ScheduleExpression: str
    StartDate: datetime
    EndDate: datetime
    Description: str
    ScheduleExpressionTimezone: str
    State: ScheduleStateType
    CreationDate: datetime
    LastModificationDate: datetime
    KmsKeyArn: str
    Target: TargetOutputTypeDef
    FlexibleTimeWindow: FlexibleTimeWindowTypeDef
    ActionAfterCompletion: ActionAfterCompletionType
    ResponseMetadata: ResponseMetadataTypeDef

TargetUnionTypeDef = Union[TargetTypeDef, TargetOutputTypeDef]

class CreateScheduleInputTypeDef(TypedDict):
    Name: str
    ScheduleExpression: str
    Target: TargetUnionTypeDef
    FlexibleTimeWindow: FlexibleTimeWindowTypeDef
    GroupName: NotRequired[str]
    StartDate: NotRequired[TimestampTypeDef]
    EndDate: NotRequired[TimestampTypeDef]
    Description: NotRequired[str]
    ScheduleExpressionTimezone: NotRequired[str]
    State: NotRequired[ScheduleStateType]
    KmsKeyArn: NotRequired[str]
    ClientToken: NotRequired[str]
    ActionAfterCompletion: NotRequired[ActionAfterCompletionType]

class UpdateScheduleInputTypeDef(TypedDict):
    Name: str
    ScheduleExpression: str
    Target: TargetUnionTypeDef
    FlexibleTimeWindow: FlexibleTimeWindowTypeDef
    GroupName: NotRequired[str]
    StartDate: NotRequired[TimestampTypeDef]
    EndDate: NotRequired[TimestampTypeDef]
    Description: NotRequired[str]
    ScheduleExpressionTimezone: NotRequired[str]
    State: NotRequired[ScheduleStateType]
    KmsKeyArn: NotRequired[str]
    ClientToken: NotRequired[str]
    ActionAfterCompletion: NotRequired[ActionAfterCompletionType]
