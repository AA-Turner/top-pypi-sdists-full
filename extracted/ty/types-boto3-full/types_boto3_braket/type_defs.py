"""
Type annotations for braket service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_braket/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_braket.type_defs import ActionMetadataTypeDef

    data: ActionMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime

from .literals import (
    CancellationStatusType,
    CompressionTypeType,
    DeviceStatusType,
    DeviceTypeType,
    InstanceTypeType,
    JobEventTypeType,
    JobPrimaryStatusType,
    QuantumTaskStatusType,
    QueueNameType,
    QueuePriorityType,
    SearchJobsFilterOperatorType,
    SearchQuantumTasksFilterOperatorType,
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
    "ActionMetadataTypeDef",
    "AlgorithmSpecificationTypeDef",
    "AssociationTypeDef",
    "CancelJobRequestTypeDef",
    "CancelJobResponseTypeDef",
    "CancelQuantumTaskRequestTypeDef",
    "CancelQuantumTaskResponseTypeDef",
    "ContainerImageTypeDef",
    "CreateJobRequestTypeDef",
    "CreateJobResponseTypeDef",
    "CreateQuantumTaskRequestTypeDef",
    "CreateQuantumTaskResponseTypeDef",
    "DataSourceTypeDef",
    "DeviceConfigTypeDef",
    "DeviceQueueInfoTypeDef",
    "DeviceSummaryTypeDef",
    "GetDeviceRequestTypeDef",
    "GetDeviceResponseTypeDef",
    "GetJobRequestTypeDef",
    "GetJobResponseTypeDef",
    "GetQuantumTaskRequestTypeDef",
    "GetQuantumTaskResponseTypeDef",
    "HybridJobQueueInfoTypeDef",
    "InputFileConfigTypeDef",
    "InstanceConfigTypeDef",
    "JobCheckpointConfigTypeDef",
    "JobEventDetailsTypeDef",
    "JobOutputDataConfigTypeDef",
    "JobStoppingConditionTypeDef",
    "JobSummaryTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "QuantumTaskQueueInfoTypeDef",
    "QuantumTaskSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "S3DataSourceTypeDef",
    "ScriptModeConfigTypeDef",
    "SearchDevicesFilterTypeDef",
    "SearchDevicesRequestPaginateTypeDef",
    "SearchDevicesRequestTypeDef",
    "SearchDevicesResponseTypeDef",
    "SearchJobsFilterTypeDef",
    "SearchJobsRequestPaginateTypeDef",
    "SearchJobsRequestTypeDef",
    "SearchJobsResponseTypeDef",
    "SearchQuantumTasksFilterTypeDef",
    "SearchQuantumTasksRequestPaginateTypeDef",
    "SearchQuantumTasksRequestTypeDef",
    "SearchQuantumTasksResponseTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
)


class ActionMetadataTypeDef(TypedDict):
    actionType: str
    programCount: NotRequired[int]
    executableCount: NotRequired[int]


class ContainerImageTypeDef(TypedDict):
    uri: str


class ScriptModeConfigTypeDef(TypedDict):
    entryPoint: str
    s3Uri: str
    compressionType: NotRequired[CompressionTypeType]


AssociationTypeDef = TypedDict(
    "AssociationTypeDef",
    {
        "arn": str,
        "type": Literal["RESERVATION_TIME_WINDOW_ARN"],
    },
)


class CancelJobRequestTypeDef(TypedDict):
    jobArn: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CancelQuantumTaskRequestTypeDef(TypedDict):
    quantumTaskArn: str
    clientToken: str


class DeviceConfigTypeDef(TypedDict):
    device: str


class InstanceConfigTypeDef(TypedDict):
    instanceType: InstanceTypeType
    volumeSizeInGb: int
    instanceCount: NotRequired[int]


class JobCheckpointConfigTypeDef(TypedDict):
    s3Uri: str
    localPath: NotRequired[str]


class JobOutputDataConfigTypeDef(TypedDict):
    s3Path: str
    kmsKeyId: NotRequired[str]


class JobStoppingConditionTypeDef(TypedDict):
    maxRuntimeInSeconds: NotRequired[int]


class S3DataSourceTypeDef(TypedDict):
    s3Uri: str


class DeviceQueueInfoTypeDef(TypedDict):
    queue: QueueNameType
    queueSize: str
    queuePriority: NotRequired[QueuePriorityType]


class DeviceSummaryTypeDef(TypedDict):
    deviceArn: str
    deviceName: str
    providerName: str
    deviceType: DeviceTypeType
    deviceStatus: DeviceStatusType


class GetDeviceRequestTypeDef(TypedDict):
    deviceArn: str


class GetJobRequestTypeDef(TypedDict):
    jobArn: str
    additionalAttributeNames: NotRequired[Sequence[Literal["QueueInfo"]]]


class HybridJobQueueInfoTypeDef(TypedDict):
    queue: QueueNameType
    position: str
    message: NotRequired[str]


class JobEventDetailsTypeDef(TypedDict):
    eventType: NotRequired[JobEventTypeType]
    timeOfEvent: NotRequired[datetime]
    message: NotRequired[str]


class GetQuantumTaskRequestTypeDef(TypedDict):
    quantumTaskArn: str
    additionalAttributeNames: NotRequired[Sequence[Literal["QueueInfo"]]]


class QuantumTaskQueueInfoTypeDef(TypedDict):
    queue: QueueNameType
    position: str
    queuePriority: NotRequired[QueuePriorityType]
    message: NotRequired[str]


class JobSummaryTypeDef(TypedDict):
    status: JobPrimaryStatusType
    jobArn: str
    jobName: str
    device: str
    createdAt: datetime
    startedAt: NotRequired[datetime]
    endedAt: NotRequired[datetime]
    tags: NotRequired[Dict[str, str]]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class QuantumTaskSummaryTypeDef(TypedDict):
    quantumTaskArn: str
    status: QuantumTaskStatusType
    deviceArn: str
    shots: int
    outputS3Bucket: str
    outputS3Directory: str
    createdAt: datetime
    endedAt: NotRequired[datetime]
    tags: NotRequired[Dict[str, str]]


class SearchDevicesFilterTypeDef(TypedDict):
    name: str
    values: Sequence[str]


SearchJobsFilterTypeDef = TypedDict(
    "SearchJobsFilterTypeDef",
    {
        "name": str,
        "values": Sequence[str],
        "operator": SearchJobsFilterOperatorType,
    },
)
SearchQuantumTasksFilterTypeDef = TypedDict(
    "SearchQuantumTasksFilterTypeDef",
    {
        "name": str,
        "values": Sequence[str],
        "operator": SearchQuantumTasksFilterOperatorType,
    },
)


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class AlgorithmSpecificationTypeDef(TypedDict):
    scriptModeConfig: NotRequired[ScriptModeConfigTypeDef]
    containerImage: NotRequired[ContainerImageTypeDef]


class CreateQuantumTaskRequestTypeDef(TypedDict):
    clientToken: str
    deviceArn: str
    shots: int
    outputS3Bucket: str
    outputS3KeyPrefix: str
    action: str
    deviceParameters: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    jobToken: NotRequired[str]
    associations: NotRequired[Sequence[AssociationTypeDef]]


class CancelJobResponseTypeDef(TypedDict):
    jobArn: str
    cancellationStatus: CancellationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CancelQuantumTaskResponseTypeDef(TypedDict):
    quantumTaskArn: str
    cancellationStatus: CancellationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateQuantumTaskResponseTypeDef(TypedDict):
    quantumTaskArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DataSourceTypeDef(TypedDict):
    s3DataSource: S3DataSourceTypeDef


class GetDeviceResponseTypeDef(TypedDict):
    deviceArn: str
    deviceName: str
    providerName: str
    deviceType: DeviceTypeType
    deviceStatus: DeviceStatusType
    deviceCapabilities: str
    deviceQueueInfo: List[DeviceQueueInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SearchDevicesResponseTypeDef(TypedDict):
    devices: List[DeviceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GetQuantumTaskResponseTypeDef(TypedDict):
    quantumTaskArn: str
    status: QuantumTaskStatusType
    failureReason: str
    deviceArn: str
    deviceParameters: str
    shots: int
    outputS3Bucket: str
    outputS3Directory: str
    createdAt: datetime
    endedAt: datetime
    tags: Dict[str, str]
    jobArn: str
    queueInfo: QuantumTaskQueueInfoTypeDef
    associations: List[AssociationTypeDef]
    numSuccessfulShots: int
    actionMetadata: ActionMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchJobsResponseTypeDef(TypedDict):
    jobs: List[JobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchQuantumTasksResponseTypeDef(TypedDict):
    quantumTasks: List[QuantumTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchDevicesRequestPaginateTypeDef(TypedDict):
    filters: Sequence[SearchDevicesFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchDevicesRequestTypeDef(TypedDict):
    filters: Sequence[SearchDevicesFilterTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class SearchJobsRequestPaginateTypeDef(TypedDict):
    filters: Sequence[SearchJobsFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchJobsRequestTypeDef(TypedDict):
    filters: Sequence[SearchJobsFilterTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class SearchQuantumTasksRequestPaginateTypeDef(TypedDict):
    filters: Sequence[SearchQuantumTasksFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchQuantumTasksRequestTypeDef(TypedDict):
    filters: Sequence[SearchQuantumTasksFilterTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class InputFileConfigTypeDef(TypedDict):
    channelName: str
    dataSource: DataSourceTypeDef
    contentType: NotRequired[str]


class CreateJobRequestTypeDef(TypedDict):
    clientToken: str
    algorithmSpecification: AlgorithmSpecificationTypeDef
    outputDataConfig: JobOutputDataConfigTypeDef
    jobName: str
    roleArn: str
    instanceConfig: InstanceConfigTypeDef
    deviceConfig: DeviceConfigTypeDef
    inputDataConfig: NotRequired[Sequence[InputFileConfigTypeDef]]
    checkpointConfig: NotRequired[JobCheckpointConfigTypeDef]
    stoppingCondition: NotRequired[JobStoppingConditionTypeDef]
    hyperParameters: NotRequired[Mapping[str, str]]
    tags: NotRequired[Mapping[str, str]]
    associations: NotRequired[Sequence[AssociationTypeDef]]


class GetJobResponseTypeDef(TypedDict):
    status: JobPrimaryStatusType
    jobArn: str
    roleArn: str
    failureReason: str
    jobName: str
    hyperParameters: Dict[str, str]
    inputDataConfig: List[InputFileConfigTypeDef]
    outputDataConfig: JobOutputDataConfigTypeDef
    stoppingCondition: JobStoppingConditionTypeDef
    checkpointConfig: JobCheckpointConfigTypeDef
    algorithmSpecification: AlgorithmSpecificationTypeDef
    instanceConfig: InstanceConfigTypeDef
    createdAt: datetime
    startedAt: datetime
    endedAt: datetime
    billableDuration: int
    deviceConfig: DeviceConfigTypeDef
    events: List[JobEventDetailsTypeDef]
    tags: Dict[str, str]
    queueInfo: HybridJobQueueInfoTypeDef
    associations: List[AssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
