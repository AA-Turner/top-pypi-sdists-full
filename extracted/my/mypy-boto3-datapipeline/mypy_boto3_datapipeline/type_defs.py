"""
Type annotations for datapipeline service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datapipeline/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_datapipeline.type_defs import ParameterValueTypeDef

    data: ParameterValueTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

from .literals import OperatorTypeType, TaskStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ActivatePipelineInputTypeDef",
    "AddTagsInputTypeDef",
    "CreatePipelineInputTypeDef",
    "CreatePipelineOutputTypeDef",
    "DeactivatePipelineInputTypeDef",
    "DeletePipelineInputTypeDef",
    "DescribeObjectsInputPaginateTypeDef",
    "DescribeObjectsInputTypeDef",
    "DescribeObjectsOutputTypeDef",
    "DescribePipelinesInputTypeDef",
    "DescribePipelinesOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EvaluateExpressionInputTypeDef",
    "EvaluateExpressionOutputTypeDef",
    "FieldTypeDef",
    "GetPipelineDefinitionInputTypeDef",
    "GetPipelineDefinitionOutputTypeDef",
    "InstanceIdentityTypeDef",
    "ListPipelinesInputPaginateTypeDef",
    "ListPipelinesInputTypeDef",
    "ListPipelinesOutputTypeDef",
    "OperatorTypeDef",
    "PaginatorConfigTypeDef",
    "ParameterAttributeTypeDef",
    "ParameterObjectOutputTypeDef",
    "ParameterObjectTypeDef",
    "ParameterObjectUnionTypeDef",
    "ParameterValueTypeDef",
    "PipelineDescriptionTypeDef",
    "PipelineIdNameTypeDef",
    "PipelineObjectOutputTypeDef",
    "PipelineObjectTypeDef",
    "PipelineObjectUnionTypeDef",
    "PollForTaskInputTypeDef",
    "PollForTaskOutputTypeDef",
    "PutPipelineDefinitionInputTypeDef",
    "PutPipelineDefinitionOutputTypeDef",
    "QueryObjectsInputPaginateTypeDef",
    "QueryObjectsInputTypeDef",
    "QueryObjectsOutputTypeDef",
    "QueryTypeDef",
    "RemoveTagsInputTypeDef",
    "ReportTaskProgressInputTypeDef",
    "ReportTaskProgressOutputTypeDef",
    "ReportTaskRunnerHeartbeatInputTypeDef",
    "ReportTaskRunnerHeartbeatOutputTypeDef",
    "ResponseMetadataTypeDef",
    "SelectorTypeDef",
    "SetStatusInputTypeDef",
    "SetTaskStatusInputTypeDef",
    "TagTypeDef",
    "TaskObjectTypeDef",
    "TimestampTypeDef",
    "ValidatePipelineDefinitionInputTypeDef",
    "ValidatePipelineDefinitionOutputTypeDef",
    "ValidationErrorTypeDef",
    "ValidationWarningTypeDef",
)

ParameterValueTypeDef = TypedDict(
    "ParameterValueTypeDef",
    {
        "id": str,
        "stringValue": str,
    },
)
TimestampTypeDef = Union[datetime, str]


class TagTypeDef(TypedDict):
    key: str
    value: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeactivatePipelineInputTypeDef(TypedDict):
    pipelineId: str
    cancelActive: NotRequired[bool]


class DeletePipelineInputTypeDef(TypedDict):
    pipelineId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeObjectsInputTypeDef(TypedDict):
    pipelineId: str
    objectIds: Sequence[str]
    evaluateExpressions: NotRequired[bool]
    marker: NotRequired[str]


class DescribePipelinesInputTypeDef(TypedDict):
    pipelineIds: Sequence[str]


class EvaluateExpressionInputTypeDef(TypedDict):
    pipelineId: str
    objectId: str
    expression: str


class FieldTypeDef(TypedDict):
    key: str
    stringValue: NotRequired[str]
    refValue: NotRequired[str]


class GetPipelineDefinitionInputTypeDef(TypedDict):
    pipelineId: str
    version: NotRequired[str]


class InstanceIdentityTypeDef(TypedDict):
    document: NotRequired[str]
    signature: NotRequired[str]


class ListPipelinesInputTypeDef(TypedDict):
    marker: NotRequired[str]


PipelineIdNameTypeDef = TypedDict(
    "PipelineIdNameTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)
OperatorTypeDef = TypedDict(
    "OperatorTypeDef",
    {
        "type": NotRequired[OperatorTypeType],
        "values": NotRequired[Sequence[str]],
    },
)


class ParameterAttributeTypeDef(TypedDict):
    key: str
    stringValue: str


ValidationErrorTypeDef = TypedDict(
    "ValidationErrorTypeDef",
    {
        "id": NotRequired[str],
        "errors": NotRequired[list[str]],
    },
)
ValidationWarningTypeDef = TypedDict(
    "ValidationWarningTypeDef",
    {
        "id": NotRequired[str],
        "warnings": NotRequired[list[str]],
    },
)


class RemoveTagsInputTypeDef(TypedDict):
    pipelineId: str
    tagKeys: Sequence[str]


class ReportTaskRunnerHeartbeatInputTypeDef(TypedDict):
    taskrunnerId: str
    workerGroup: NotRequired[str]
    hostname: NotRequired[str]


class SetStatusInputTypeDef(TypedDict):
    pipelineId: str
    objectIds: Sequence[str]
    status: str


class SetTaskStatusInputTypeDef(TypedDict):
    taskId: str
    taskStatus: TaskStatusType
    errorId: NotRequired[str]
    errorMessage: NotRequired[str]
    errorStackTrace: NotRequired[str]


class ActivatePipelineInputTypeDef(TypedDict):
    pipelineId: str
    parameterValues: NotRequired[Sequence[ParameterValueTypeDef]]
    startTimestamp: NotRequired[TimestampTypeDef]


class AddTagsInputTypeDef(TypedDict):
    pipelineId: str
    tags: Sequence[TagTypeDef]


class CreatePipelineInputTypeDef(TypedDict):
    name: str
    uniqueId: str
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreatePipelineOutputTypeDef(TypedDict):
    pipelineId: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class EvaluateExpressionOutputTypeDef(TypedDict):
    evaluatedExpression: str
    ResponseMetadata: ResponseMetadataTypeDef


class QueryObjectsOutputTypeDef(TypedDict):
    ids: list[str]
    marker: str
    hasMoreResults: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ReportTaskProgressOutputTypeDef(TypedDict):
    canceled: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ReportTaskRunnerHeartbeatOutputTypeDef(TypedDict):
    terminate: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeObjectsInputPaginateTypeDef(TypedDict):
    pipelineId: str
    objectIds: Sequence[str]
    evaluateExpressions: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelinesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class PipelineDescriptionTypeDef(TypedDict):
    pipelineId: str
    name: str
    fields: list[FieldTypeDef]
    description: NotRequired[str]
    tags: NotRequired[list[TagTypeDef]]


PipelineObjectOutputTypeDef = TypedDict(
    "PipelineObjectOutputTypeDef",
    {
        "id": str,
        "name": str,
        "fields": list[FieldTypeDef],
    },
)
PipelineObjectTypeDef = TypedDict(
    "PipelineObjectTypeDef",
    {
        "id": str,
        "name": str,
        "fields": Sequence[FieldTypeDef],
    },
)


class ReportTaskProgressInputTypeDef(TypedDict):
    taskId: str
    fields: NotRequired[Sequence[FieldTypeDef]]


class PollForTaskInputTypeDef(TypedDict):
    workerGroup: str
    hostname: NotRequired[str]
    instanceIdentity: NotRequired[InstanceIdentityTypeDef]


class ListPipelinesOutputTypeDef(TypedDict):
    pipelineIdList: list[PipelineIdNameTypeDef]
    marker: str
    hasMoreResults: bool
    ResponseMetadata: ResponseMetadataTypeDef


SelectorTypeDef = TypedDict(
    "SelectorTypeDef",
    {
        "fieldName": NotRequired[str],
        "operator": NotRequired[OperatorTypeDef],
    },
)
ParameterObjectOutputTypeDef = TypedDict(
    "ParameterObjectOutputTypeDef",
    {
        "id": str,
        "attributes": list[ParameterAttributeTypeDef],
    },
)
ParameterObjectTypeDef = TypedDict(
    "ParameterObjectTypeDef",
    {
        "id": str,
        "attributes": Sequence[ParameterAttributeTypeDef],
    },
)


class PutPipelineDefinitionOutputTypeDef(TypedDict):
    validationErrors: list[ValidationErrorTypeDef]
    validationWarnings: list[ValidationWarningTypeDef]
    errored: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ValidatePipelineDefinitionOutputTypeDef(TypedDict):
    validationErrors: list[ValidationErrorTypeDef]
    validationWarnings: list[ValidationWarningTypeDef]
    errored: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePipelinesOutputTypeDef(TypedDict):
    pipelineDescriptionList: list[PipelineDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeObjectsOutputTypeDef(TypedDict):
    pipelineObjects: list[PipelineObjectOutputTypeDef]
    marker: str
    hasMoreResults: bool
    ResponseMetadata: ResponseMetadataTypeDef


class TaskObjectTypeDef(TypedDict):
    taskId: NotRequired[str]
    pipelineId: NotRequired[str]
    attemptId: NotRequired[str]
    objects: NotRequired[dict[str, PipelineObjectOutputTypeDef]]


PipelineObjectUnionTypeDef = Union[PipelineObjectTypeDef, PipelineObjectOutputTypeDef]


class QueryTypeDef(TypedDict):
    selectors: NotRequired[Sequence[SelectorTypeDef]]


class GetPipelineDefinitionOutputTypeDef(TypedDict):
    pipelineObjects: list[PipelineObjectOutputTypeDef]
    parameterObjects: list[ParameterObjectOutputTypeDef]
    parameterValues: list[ParameterValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


ParameterObjectUnionTypeDef = Union[ParameterObjectTypeDef, ParameterObjectOutputTypeDef]


class PollForTaskOutputTypeDef(TypedDict):
    taskObject: TaskObjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class QueryObjectsInputPaginateTypeDef(TypedDict):
    pipelineId: str
    sphere: str
    query: NotRequired[QueryTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class QueryObjectsInputTypeDef(TypedDict):
    pipelineId: str
    sphere: str
    query: NotRequired[QueryTypeDef]
    marker: NotRequired[str]
    limit: NotRequired[int]


class PutPipelineDefinitionInputTypeDef(TypedDict):
    pipelineId: str
    pipelineObjects: Sequence[PipelineObjectUnionTypeDef]
    parameterObjects: NotRequired[Sequence[ParameterObjectUnionTypeDef]]
    parameterValues: NotRequired[Sequence[ParameterValueTypeDef]]


class ValidatePipelineDefinitionInputTypeDef(TypedDict):
    pipelineId: str
    pipelineObjects: Sequence[PipelineObjectUnionTypeDef]
    parameterObjects: NotRequired[Sequence[ParameterObjectUnionTypeDef]]
    parameterValues: NotRequired[Sequence[ParameterValueTypeDef]]
