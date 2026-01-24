"""
Type annotations for scheduler service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_scheduler.type_defs import AwsVpcConfigurationOutputTypeDef

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
    AssignPublicIp: NotRequired[AssignPublicIpType]
    SecurityGroups: NotRequired[list[str]]


class AwsVpcConfigurationTypeDef(TypedDict):
    Subnets: Sequence[str]
    AssignPublicIp: NotRequired[AssignPublicIpType]
    SecurityGroups: NotRequired[Sequence[str]]


class CapacityProviderStrategyItemTypeDef(TypedDict):
    capacityProvider: str
    base: NotRequired[int]
    weight: NotRequired[int]


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
    ClientToken: NotRequired[str]
    GroupName: NotRequired[str]


PlacementConstraintTypeDef = TypedDict(
    "PlacementConstraintTypeDef",
    {
        "expression": NotRequired[str],
        "type": NotRequired[PlacementConstraintTypeType],
    },
)
PlacementStrategyTypeDef = TypedDict(
    "PlacementStrategyTypeDef",
    {
        "field": NotRequired[str],
        "type": NotRequired[PlacementStrategyTypeType],
    },
)


class EventBridgeParametersTypeDef(TypedDict):
    DetailType: str
    Source: str


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
    MaxResults: NotRequired[int]
    NamePrefix: NotRequired[str]
    NextToken: NotRequired[str]


class ScheduleGroupSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreationDate: NotRequired[datetime]
    LastModificationDate: NotRequired[datetime]
    Name: NotRequired[str]
    State: NotRequired[ScheduleGroupStateType]


class ListSchedulesInputTypeDef(TypedDict):
    GroupName: NotRequired[str]
    MaxResults: NotRequired[int]
    NamePrefix: NotRequired[str]
    NextToken: NotRequired[str]
    State: NotRequired[ScheduleStateType]


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
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


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
    CreationDate: datetime
    LastModificationDate: datetime
    Name: str
    State: ScheduleGroupStateType
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
    CreationDate: NotRequired[datetime]
    GroupName: NotRequired[str]
    LastModificationDate: NotRequired[datetime]
    Name: NotRequired[str]
    State: NotRequired[ScheduleStateType]
    Target: NotRequired[TargetSummaryTypeDef]


class EcsParametersOutputTypeDef(TypedDict):
    TaskDefinitionArn: str
    CapacityProviderStrategy: NotRequired[list[CapacityProviderStrategyItemTypeDef]]
    EnableECSManagedTags: NotRequired[bool]
    EnableExecuteCommand: NotRequired[bool]
    Group: NotRequired[str]
    LaunchType: NotRequired[LaunchTypeType]
    NetworkConfiguration: NotRequired[NetworkConfigurationOutputTypeDef]
    PlacementConstraints: NotRequired[list[PlacementConstraintTypeDef]]
    PlacementStrategy: NotRequired[list[PlacementStrategyTypeDef]]
    PlatformVersion: NotRequired[str]
    PropagateTags: NotRequired[Literal["TASK_DEFINITION"]]
    ReferenceId: NotRequired[str]
    Tags: NotRequired[list[dict[str, str]]]
    TaskCount: NotRequired[int]


class EcsParametersTypeDef(TypedDict):
    TaskDefinitionArn: str
    CapacityProviderStrategy: NotRequired[Sequence[CapacityProviderStrategyItemTypeDef]]
    EnableECSManagedTags: NotRequired[bool]
    EnableExecuteCommand: NotRequired[bool]
    Group: NotRequired[str]
    LaunchType: NotRequired[LaunchTypeType]
    NetworkConfiguration: NotRequired[NetworkConfigurationTypeDef]
    PlacementConstraints: NotRequired[Sequence[PlacementConstraintTypeDef]]
    PlacementStrategy: NotRequired[Sequence[PlacementStrategyTypeDef]]
    PlatformVersion: NotRequired[str]
    PropagateTags: NotRequired[Literal["TASK_DEFINITION"]]
    ReferenceId: NotRequired[str]
    Tags: NotRequired[Sequence[Mapping[str, str]]]
    TaskCount: NotRequired[int]


class ListSchedulesOutputTypeDef(TypedDict):
    Schedules: list[ScheduleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TargetOutputTypeDef(TypedDict):
    Arn: str
    RoleArn: str
    DeadLetterConfig: NotRequired[DeadLetterConfigTypeDef]
    EcsParameters: NotRequired[EcsParametersOutputTypeDef]
    EventBridgeParameters: NotRequired[EventBridgeParametersTypeDef]
    Input: NotRequired[str]
    KinesisParameters: NotRequired[KinesisParametersTypeDef]
    RetryPolicy: NotRequired[RetryPolicyTypeDef]
    SageMakerPipelineParameters: NotRequired[SageMakerPipelineParametersOutputTypeDef]
    SqsParameters: NotRequired[SqsParametersTypeDef]


class TargetTypeDef(TypedDict):
    Arn: str
    RoleArn: str
    DeadLetterConfig: NotRequired[DeadLetterConfigTypeDef]
    EcsParameters: NotRequired[EcsParametersTypeDef]
    EventBridgeParameters: NotRequired[EventBridgeParametersTypeDef]
    Input: NotRequired[str]
    KinesisParameters: NotRequired[KinesisParametersTypeDef]
    RetryPolicy: NotRequired[RetryPolicyTypeDef]
    SageMakerPipelineParameters: NotRequired[SageMakerPipelineParametersTypeDef]
    SqsParameters: NotRequired[SqsParametersTypeDef]


class GetScheduleOutputTypeDef(TypedDict):
    ActionAfterCompletion: ActionAfterCompletionType
    Arn: str
    CreationDate: datetime
    Description: str
    EndDate: datetime
    FlexibleTimeWindow: FlexibleTimeWindowTypeDef
    GroupName: str
    KmsKeyArn: str
    LastModificationDate: datetime
    Name: str
    ScheduleExpression: str
    ScheduleExpressionTimezone: str
    StartDate: datetime
    State: ScheduleStateType
    Target: TargetOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


TargetUnionTypeDef = Union[TargetTypeDef, TargetOutputTypeDef]


class CreateScheduleInputTypeDef(TypedDict):
    FlexibleTimeWindow: FlexibleTimeWindowTypeDef
    Name: str
    ScheduleExpression: str
    Target: TargetUnionTypeDef
    ActionAfterCompletion: NotRequired[ActionAfterCompletionType]
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    EndDate: NotRequired[TimestampTypeDef]
    GroupName: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    ScheduleExpressionTimezone: NotRequired[str]
    StartDate: NotRequired[TimestampTypeDef]
    State: NotRequired[ScheduleStateType]


class UpdateScheduleInputTypeDef(TypedDict):
    FlexibleTimeWindow: FlexibleTimeWindowTypeDef
    Name: str
    ScheduleExpression: str
    Target: TargetUnionTypeDef
    ActionAfterCompletion: NotRequired[ActionAfterCompletionType]
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    EndDate: NotRequired[TimestampTypeDef]
    GroupName: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    ScheduleExpressionTimezone: NotRequired[str]
    StartDate: NotRequired[TimestampTypeDef]
    State: NotRequired[ScheduleStateType]
