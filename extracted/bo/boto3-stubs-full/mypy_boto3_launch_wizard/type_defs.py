"""
Type annotations for launch-wizard service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_launch_wizard/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_launch_wizard.type_defs import CreateDeploymentInputTypeDef

    data: CreateDeploymentInputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime

from .literals import (
    DeploymentFilterKeyType,
    DeploymentStatusType,
    EventStatusType,
    WorkloadDeploymentPatternStatusType,
    WorkloadStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "CreateDeploymentInputTypeDef",
    "CreateDeploymentOutputTypeDef",
    "DeleteDeploymentInputTypeDef",
    "DeleteDeploymentOutputTypeDef",
    "DeploymentConditionalFieldTypeDef",
    "DeploymentDataSummaryTypeDef",
    "DeploymentDataTypeDef",
    "DeploymentEventDataSummaryTypeDef",
    "DeploymentFilterTypeDef",
    "DeploymentPatternVersionDataSummaryTypeDef",
    "DeploymentPatternVersionFilterTypeDef",
    "DeploymentSpecificationsFieldTypeDef",
    "GetDeploymentInputTypeDef",
    "GetDeploymentOutputTypeDef",
    "GetDeploymentPatternVersionInputTypeDef",
    "GetDeploymentPatternVersionOutputTypeDef",
    "GetWorkloadDeploymentPatternInputTypeDef",
    "GetWorkloadDeploymentPatternOutputTypeDef",
    "GetWorkloadInputTypeDef",
    "GetWorkloadOutputTypeDef",
    "ListDeploymentEventsInputPaginateTypeDef",
    "ListDeploymentEventsInputTypeDef",
    "ListDeploymentEventsOutputTypeDef",
    "ListDeploymentPatternVersionsInputPaginateTypeDef",
    "ListDeploymentPatternVersionsInputTypeDef",
    "ListDeploymentPatternVersionsOutputTypeDef",
    "ListDeploymentsInputPaginateTypeDef",
    "ListDeploymentsInputTypeDef",
    "ListDeploymentsOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListWorkloadDeploymentPatternsInputPaginateTypeDef",
    "ListWorkloadDeploymentPatternsInputTypeDef",
    "ListWorkloadDeploymentPatternsOutputTypeDef",
    "ListWorkloadsInputPaginateTypeDef",
    "ListWorkloadsInputTypeDef",
    "ListWorkloadsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceInputTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateDeploymentInputTypeDef",
    "UpdateDeploymentOutputTypeDef",
    "WorkloadDataSummaryTypeDef",
    "WorkloadDataTypeDef",
    "WorkloadDeploymentPatternDataSummaryTypeDef",
    "WorkloadDeploymentPatternDataTypeDef",
)


class CreateDeploymentInputTypeDef(TypedDict):
    workloadName: str
    deploymentPatternName: str
    name: str
    specifications: Mapping[str, str]
    dryRun: NotRequired[bool]
    tags: NotRequired[Mapping[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteDeploymentInputTypeDef(TypedDict):
    deploymentId: str


class DeploymentConditionalFieldTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]
    comparator: NotRequired[str]


DeploymentDataSummaryTypeDef = TypedDict(
    "DeploymentDataSummaryTypeDef",
    {
        "name": NotRequired[str],
        "id": NotRequired[str],
        "workloadName": NotRequired[str],
        "patternName": NotRequired[str],
        "status": NotRequired[DeploymentStatusType],
        "createdAt": NotRequired[datetime],
        "modifiedAt": NotRequired[datetime],
    },
)
DeploymentDataTypeDef = TypedDict(
    "DeploymentDataTypeDef",
    {
        "name": NotRequired[str],
        "id": NotRequired[str],
        "workloadName": NotRequired[str],
        "patternName": NotRequired[str],
        "status": NotRequired[DeploymentStatusType],
        "createdAt": NotRequired[datetime],
        "modifiedAt": NotRequired[datetime],
        "specifications": NotRequired[dict[str, str]],
        "resourceGroup": NotRequired[str],
        "deletedAt": NotRequired[datetime],
        "tags": NotRequired[dict[str, str]],
        "deploymentArn": NotRequired[str],
    },
)


class DeploymentEventDataSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[EventStatusType]
    statusReason: NotRequired[str]
    timestamp: NotRequired[datetime]


class DeploymentFilterTypeDef(TypedDict):
    name: NotRequired[DeploymentFilterKeyType]
    values: NotRequired[Sequence[str]]


class DeploymentPatternVersionDataSummaryTypeDef(TypedDict):
    deploymentPatternVersionName: NotRequired[str]
    description: NotRequired[str]
    documentationUrl: NotRequired[str]
    workloadName: NotRequired[str]
    deploymentPatternName: NotRequired[str]


class DeploymentPatternVersionFilterTypeDef(TypedDict):
    name: Literal["updateFromVersion"]
    values: Sequence[str]


class GetDeploymentInputTypeDef(TypedDict):
    deploymentId: str


class GetDeploymentPatternVersionInputTypeDef(TypedDict):
    workloadName: str
    deploymentPatternName: str
    deploymentPatternVersionName: str


class GetWorkloadDeploymentPatternInputTypeDef(TypedDict):
    workloadName: str
    deploymentPatternName: str


class GetWorkloadInputTypeDef(TypedDict):
    workloadName: str


class WorkloadDataTypeDef(TypedDict):
    workloadName: NotRequired[str]
    displayName: NotRequired[str]
    status: NotRequired[WorkloadStatusType]
    description: NotRequired[str]
    documentationUrl: NotRequired[str]
    iconUrl: NotRequired[str]
    statusMessage: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListDeploymentEventsInputTypeDef(TypedDict):
    deploymentId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceInputTypeDef(TypedDict):
    resourceArn: str


class ListWorkloadDeploymentPatternsInputTypeDef(TypedDict):
    workloadName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class WorkloadDeploymentPatternDataSummaryTypeDef(TypedDict):
    workloadName: NotRequired[str]
    deploymentPatternName: NotRequired[str]
    workloadVersionName: NotRequired[str]
    deploymentPatternVersionName: NotRequired[str]
    displayName: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[WorkloadDeploymentPatternStatusType]
    statusMessage: NotRequired[str]


class ListWorkloadsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class WorkloadDataSummaryTypeDef(TypedDict):
    workloadName: NotRequired[str]
    displayName: NotRequired[str]
    status: NotRequired[WorkloadStatusType]


class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateDeploymentInputTypeDef(TypedDict):
    deploymentId: str
    specifications: Mapping[str, str]
    workloadVersionName: NotRequired[str]
    deploymentPatternVersionName: NotRequired[str]
    dryRun: NotRequired[bool]
    force: NotRequired[bool]


class CreateDeploymentOutputTypeDef(TypedDict):
    deploymentId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDeploymentOutputTypeDef(TypedDict):
    status: DeploymentStatusType
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DeploymentSpecificationsFieldTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    allowedValues: NotRequired[list[str]]
    required: NotRequired[str]
    conditionals: NotRequired[list[DeploymentConditionalFieldTypeDef]]


class ListDeploymentsOutputTypeDef(TypedDict):
    deployments: list[DeploymentDataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateDeploymentOutputTypeDef(TypedDict):
    deployment: DeploymentDataSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDeploymentOutputTypeDef(TypedDict):
    deployment: DeploymentDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDeploymentEventsOutputTypeDef(TypedDict):
    deploymentEvents: list[DeploymentEventDataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDeploymentsInputTypeDef(TypedDict):
    filters: NotRequired[Sequence[DeploymentFilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class GetDeploymentPatternVersionOutputTypeDef(TypedDict):
    deploymentPatternVersion: DeploymentPatternVersionDataSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDeploymentPatternVersionsOutputTypeDef(TypedDict):
    deploymentPatternVersions: list[DeploymentPatternVersionDataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDeploymentPatternVersionsInputTypeDef(TypedDict):
    workloadName: str
    deploymentPatternName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    filters: NotRequired[Sequence[DeploymentPatternVersionFilterTypeDef]]


class GetWorkloadOutputTypeDef(TypedDict):
    workload: WorkloadDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDeploymentEventsInputPaginateTypeDef(TypedDict):
    deploymentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDeploymentPatternVersionsInputPaginateTypeDef(TypedDict):
    workloadName: str
    deploymentPatternName: str
    filters: NotRequired[Sequence[DeploymentPatternVersionFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDeploymentsInputPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[DeploymentFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkloadDeploymentPatternsInputPaginateTypeDef(TypedDict):
    workloadName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkloadsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkloadDeploymentPatternsOutputTypeDef(TypedDict):
    workloadDeploymentPatterns: list[WorkloadDeploymentPatternDataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListWorkloadsOutputTypeDef(TypedDict):
    workloads: list[WorkloadDataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class WorkloadDeploymentPatternDataTypeDef(TypedDict):
    workloadName: NotRequired[str]
    deploymentPatternName: NotRequired[str]
    workloadVersionName: NotRequired[str]
    deploymentPatternVersionName: NotRequired[str]
    displayName: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[WorkloadDeploymentPatternStatusType]
    statusMessage: NotRequired[str]
    specifications: NotRequired[list[DeploymentSpecificationsFieldTypeDef]]


class GetWorkloadDeploymentPatternOutputTypeDef(TypedDict):
    workloadDeploymentPattern: WorkloadDeploymentPatternDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
