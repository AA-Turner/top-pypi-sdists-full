"""
Type annotations for simspaceweaver service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_simspaceweaver.type_defs import CloudWatchLogsLogGroupTypeDef

    data: CloudWatchLogsLogGroupTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Union

from .literals import (
    ClockStatusType,
    ClockTargetStatusType,
    LifecycleManagementStrategyType,
    SimulationAppStatusType,
    SimulationAppTargetStatusType,
    SimulationStatusType,
    SimulationTargetStatusType,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "CloudWatchLogsLogGroupTypeDef",
    "CreateSnapshotInputTypeDef",
    "DeleteAppInputTypeDef",
    "DeleteSimulationInputTypeDef",
    "DescribeAppInputTypeDef",
    "DescribeAppOutputTypeDef",
    "DescribeSimulationInputTypeDef",
    "DescribeSimulationOutputTypeDef",
    "DomainTypeDef",
    "LaunchOverridesOutputTypeDef",
    "LaunchOverridesTypeDef",
    "LaunchOverridesUnionTypeDef",
    "ListAppsInputTypeDef",
    "ListAppsOutputTypeDef",
    "ListSimulationsInputTypeDef",
    "ListSimulationsOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "LiveSimulationStateTypeDef",
    "LogDestinationTypeDef",
    "LoggingConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "S3DestinationTypeDef",
    "S3LocationTypeDef",
    "SimulationAppEndpointInfoTypeDef",
    "SimulationAppMetadataTypeDef",
    "SimulationAppPortMappingTypeDef",
    "SimulationClockTypeDef",
    "SimulationMetadataTypeDef",
    "StartAppInputTypeDef",
    "StartAppOutputTypeDef",
    "StartClockInputTypeDef",
    "StartSimulationInputTypeDef",
    "StartSimulationOutputTypeDef",
    "StopAppInputTypeDef",
    "StopClockInputTypeDef",
    "StopSimulationInputTypeDef",
    "TagResourceInputTypeDef",
    "UntagResourceInputTypeDef",
)


class CloudWatchLogsLogGroupTypeDef(TypedDict):
    LogGroupArn: NotRequired[str]


class S3DestinationTypeDef(TypedDict):
    BucketName: str
    ObjectKeyPrefix: NotRequired[str]


class DeleteAppInputTypeDef(TypedDict):
    App: str
    Domain: str
    Simulation: str


class DeleteSimulationInputTypeDef(TypedDict):
    Simulation: str


class DescribeAppInputTypeDef(TypedDict):
    App: str
    Domain: str
    Simulation: str


class LaunchOverridesOutputTypeDef(TypedDict):
    LaunchCommands: NotRequired[List[str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DescribeSimulationInputTypeDef(TypedDict):
    Simulation: str


class S3LocationTypeDef(TypedDict):
    BucketName: str
    ObjectKey: str


class DomainTypeDef(TypedDict):
    Lifecycle: NotRequired[LifecycleManagementStrategyType]
    Name: NotRequired[str]


class LaunchOverridesTypeDef(TypedDict):
    LaunchCommands: NotRequired[Sequence[str]]


class ListAppsInputTypeDef(TypedDict):
    Simulation: str
    Domain: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class SimulationAppMetadataTypeDef(TypedDict):
    Domain: NotRequired[str]
    Name: NotRequired[str]
    Simulation: NotRequired[str]
    Status: NotRequired[SimulationAppStatusType]
    TargetStatus: NotRequired[SimulationAppTargetStatusType]


class ListSimulationsInputTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class SimulationMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreationTime: NotRequired[datetime]
    Name: NotRequired[str]
    Status: NotRequired[SimulationStatusType]
    TargetStatus: NotRequired[SimulationTargetStatusType]


class ListTagsForResourceInputTypeDef(TypedDict):
    ResourceArn: str


class SimulationClockTypeDef(TypedDict):
    Status: NotRequired[ClockStatusType]
    TargetStatus: NotRequired[ClockTargetStatusType]


class SimulationAppPortMappingTypeDef(TypedDict):
    Actual: NotRequired[int]
    Declared: NotRequired[int]


class StartClockInputTypeDef(TypedDict):
    Simulation: str


class StopAppInputTypeDef(TypedDict):
    App: str
    Domain: str
    Simulation: str


class StopClockInputTypeDef(TypedDict):
    Simulation: str


class StopSimulationInputTypeDef(TypedDict):
    Simulation: str


class TagResourceInputTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceInputTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class LogDestinationTypeDef(TypedDict):
    CloudWatchLogsLogGroup: NotRequired[CloudWatchLogsLogGroupTypeDef]


class CreateSnapshotInputTypeDef(TypedDict):
    Destination: S3DestinationTypeDef
    Simulation: str


class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartAppOutputTypeDef(TypedDict):
    Domain: str
    Name: str
    Simulation: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartSimulationOutputTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    ExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartSimulationInputTypeDef(TypedDict):
    Name: str
    RoleArn: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    MaximumDuration: NotRequired[str]
    SchemaS3Location: NotRequired[S3LocationTypeDef]
    SnapshotS3Location: NotRequired[S3LocationTypeDef]
    Tags: NotRequired[Mapping[str, str]]


LaunchOverridesUnionTypeDef = Union[LaunchOverridesTypeDef, LaunchOverridesOutputTypeDef]


class ListAppsOutputTypeDef(TypedDict):
    Apps: List[SimulationAppMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListSimulationsOutputTypeDef(TypedDict):
    Simulations: List[SimulationMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LiveSimulationStateTypeDef(TypedDict):
    Clocks: NotRequired[List[SimulationClockTypeDef]]
    Domains: NotRequired[List[DomainTypeDef]]


class SimulationAppEndpointInfoTypeDef(TypedDict):
    Address: NotRequired[str]
    IngressPortMappings: NotRequired[List[SimulationAppPortMappingTypeDef]]


class LoggingConfigurationTypeDef(TypedDict):
    Destinations: NotRequired[List[LogDestinationTypeDef]]


class StartAppInputTypeDef(TypedDict):
    Domain: str
    Name: str
    Simulation: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    LaunchOverrides: NotRequired[LaunchOverridesUnionTypeDef]


class DescribeAppOutputTypeDef(TypedDict):
    Description: str
    Domain: str
    EndpointInfo: SimulationAppEndpointInfoTypeDef
    LaunchOverrides: LaunchOverridesOutputTypeDef
    Name: str
    Simulation: str
    Status: SimulationAppStatusType
    TargetStatus: SimulationAppTargetStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSimulationOutputTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    Description: str
    ExecutionId: str
    LiveSimulationState: LiveSimulationStateTypeDef
    LoggingConfiguration: LoggingConfigurationTypeDef
    MaximumDuration: str
    Name: str
    RoleArn: str
    SchemaError: str
    SchemaS3Location: S3LocationTypeDef
    SnapshotS3Location: S3LocationTypeDef
    StartError: str
    Status: SimulationStatusType
    TargetStatus: SimulationTargetStatusType
    ResponseMetadata: ResponseMetadataTypeDef
