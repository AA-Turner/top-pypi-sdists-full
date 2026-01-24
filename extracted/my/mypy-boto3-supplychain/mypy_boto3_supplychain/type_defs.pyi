"""
Type annotations for supplychain service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_supplychain.type_defs import BillOfMaterialsImportJobTypeDef

    data: BillOfMaterialsImportJobTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    ConfigurationJobStatusType,
    DataIntegrationEventDatasetLoadStatusType,
    DataIntegrationEventDatasetOperationTypeType,
    DataIntegrationEventTypeType,
    DataIntegrationFlowExecutionStatusType,
    DataIntegrationFlowFieldPriorityDedupeSortOrderType,
    DataIntegrationFlowFileTypeType,
    DataIntegrationFlowLoadTypeType,
    DataIntegrationFlowSourceTypeType,
    DataIntegrationFlowTargetTypeType,
    DataIntegrationFlowTransformationTypeType,
    DataLakeDatasetPartitionTransformTypeType,
    DataLakeDatasetSchemaFieldTypeType,
    InstanceStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "BillOfMaterialsImportJobTypeDef",
    "CreateBillOfMaterialsImportJobRequestTypeDef",
    "CreateBillOfMaterialsImportJobResponseTypeDef",
    "CreateDataIntegrationFlowRequestTypeDef",
    "CreateDataIntegrationFlowResponseTypeDef",
    "CreateDataLakeDatasetRequestTypeDef",
    "CreateDataLakeDatasetResponseTypeDef",
    "CreateDataLakeNamespaceRequestTypeDef",
    "CreateDataLakeNamespaceResponseTypeDef",
    "CreateInstanceRequestTypeDef",
    "CreateInstanceResponseTypeDef",
    "DataIntegrationEventDatasetLoadExecutionDetailsTypeDef",
    "DataIntegrationEventDatasetTargetConfigurationTypeDef",
    "DataIntegrationEventDatasetTargetDetailsTypeDef",
    "DataIntegrationEventTypeDef",
    "DataIntegrationFlowDatasetOptionsOutputTypeDef",
    "DataIntegrationFlowDatasetOptionsTypeDef",
    "DataIntegrationFlowDatasetOptionsUnionTypeDef",
    "DataIntegrationFlowDatasetSourceConfigurationOutputTypeDef",
    "DataIntegrationFlowDatasetSourceConfigurationTypeDef",
    "DataIntegrationFlowDatasetSourceConfigurationUnionTypeDef",
    "DataIntegrationFlowDatasetSourceTypeDef",
    "DataIntegrationFlowDatasetTargetConfigurationOutputTypeDef",
    "DataIntegrationFlowDatasetTargetConfigurationTypeDef",
    "DataIntegrationFlowDedupeStrategyOutputTypeDef",
    "DataIntegrationFlowDedupeStrategyTypeDef",
    "DataIntegrationFlowDedupeStrategyUnionTypeDef",
    "DataIntegrationFlowExecutionOutputMetadataTypeDef",
    "DataIntegrationFlowExecutionSourceInfoTypeDef",
    "DataIntegrationFlowExecutionTypeDef",
    "DataIntegrationFlowFieldPriorityDedupeFieldTypeDef",
    "DataIntegrationFlowFieldPriorityDedupeStrategyConfigurationOutputTypeDef",
    "DataIntegrationFlowFieldPriorityDedupeStrategyConfigurationTypeDef",
    "DataIntegrationFlowFieldPriorityDedupeStrategyConfigurationUnionTypeDef",
    "DataIntegrationFlowS3OptionsTypeDef",
    "DataIntegrationFlowS3SourceConfigurationTypeDef",
    "DataIntegrationFlowS3SourceTypeDef",
    "DataIntegrationFlowS3TargetConfigurationTypeDef",
    "DataIntegrationFlowSQLTransformationConfigurationTypeDef",
    "DataIntegrationFlowSourceOutputTypeDef",
    "DataIntegrationFlowSourceTypeDef",
    "DataIntegrationFlowSourceUnionTypeDef",
    "DataIntegrationFlowTargetOutputTypeDef",
    "DataIntegrationFlowTargetTypeDef",
    "DataIntegrationFlowTargetUnionTypeDef",
    "DataIntegrationFlowTransformationTypeDef",
    "DataIntegrationFlowTypeDef",
    "DataLakeDatasetPartitionFieldTransformTypeDef",
    "DataLakeDatasetPartitionFieldTypeDef",
    "DataLakeDatasetPartitionSpecOutputTypeDef",
    "DataLakeDatasetPartitionSpecTypeDef",
    "DataLakeDatasetPartitionSpecUnionTypeDef",
    "DataLakeDatasetPrimaryKeyFieldTypeDef",
    "DataLakeDatasetSchemaFieldTypeDef",
    "DataLakeDatasetSchemaOutputTypeDef",
    "DataLakeDatasetSchemaTypeDef",
    "DataLakeDatasetSchemaUnionTypeDef",
    "DataLakeDatasetTypeDef",
    "DataLakeNamespaceTypeDef",
    "DeleteDataIntegrationFlowRequestTypeDef",
    "DeleteDataIntegrationFlowResponseTypeDef",
    "DeleteDataLakeDatasetRequestTypeDef",
    "DeleteDataLakeDatasetResponseTypeDef",
    "DeleteDataLakeNamespaceRequestTypeDef",
    "DeleteDataLakeNamespaceResponseTypeDef",
    "DeleteInstanceRequestTypeDef",
    "DeleteInstanceResponseTypeDef",
    "GetBillOfMaterialsImportJobRequestTypeDef",
    "GetBillOfMaterialsImportJobResponseTypeDef",
    "GetDataIntegrationEventRequestTypeDef",
    "GetDataIntegrationEventResponseTypeDef",
    "GetDataIntegrationFlowExecutionRequestTypeDef",
    "GetDataIntegrationFlowExecutionResponseTypeDef",
    "GetDataIntegrationFlowRequestTypeDef",
    "GetDataIntegrationFlowResponseTypeDef",
    "GetDataLakeDatasetRequestTypeDef",
    "GetDataLakeDatasetResponseTypeDef",
    "GetDataLakeNamespaceRequestTypeDef",
    "GetDataLakeNamespaceResponseTypeDef",
    "GetInstanceRequestTypeDef",
    "GetInstanceResponseTypeDef",
    "InstanceTypeDef",
    "ListDataIntegrationEventsRequestPaginateTypeDef",
    "ListDataIntegrationEventsRequestTypeDef",
    "ListDataIntegrationEventsResponseTypeDef",
    "ListDataIntegrationFlowExecutionsRequestPaginateTypeDef",
    "ListDataIntegrationFlowExecutionsRequestTypeDef",
    "ListDataIntegrationFlowExecutionsResponseTypeDef",
    "ListDataIntegrationFlowsRequestPaginateTypeDef",
    "ListDataIntegrationFlowsRequestTypeDef",
    "ListDataIntegrationFlowsResponseTypeDef",
    "ListDataLakeDatasetsRequestPaginateTypeDef",
    "ListDataLakeDatasetsRequestTypeDef",
    "ListDataLakeDatasetsResponseTypeDef",
    "ListDataLakeNamespacesRequestPaginateTypeDef",
    "ListDataLakeNamespacesRequestTypeDef",
    "ListDataLakeNamespacesResponseTypeDef",
    "ListInstancesRequestPaginateTypeDef",
    "ListInstancesRequestTypeDef",
    "ListInstancesResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SendDataIntegrationEventRequestTypeDef",
    "SendDataIntegrationEventResponseTypeDef",
    "TagResourceRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateDataIntegrationFlowRequestTypeDef",
    "UpdateDataIntegrationFlowResponseTypeDef",
    "UpdateDataLakeDatasetRequestTypeDef",
    "UpdateDataLakeDatasetResponseTypeDef",
    "UpdateDataLakeNamespaceRequestTypeDef",
    "UpdateDataLakeNamespaceResponseTypeDef",
    "UpdateInstanceRequestTypeDef",
    "UpdateInstanceResponseTypeDef",
)

class BillOfMaterialsImportJobTypeDef(TypedDict):
    instanceId: str
    jobId: str
    status: ConfigurationJobStatusType
    s3uri: str
    message: NotRequired[str]

class CreateBillOfMaterialsImportJobRequestTypeDef(TypedDict):
    instanceId: str
    s3uri: str
    clientToken: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateDataLakeNamespaceRequestTypeDef(TypedDict):
    instanceId: str
    name: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class DataLakeNamespaceTypeDef(TypedDict):
    instanceId: str
    name: str
    arn: str
    createdTime: datetime
    lastModifiedTime: datetime
    description: NotRequired[str]

class CreateInstanceRequestTypeDef(TypedDict):
    instanceName: NotRequired[str]
    instanceDescription: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    webAppDnsDomain: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]

class InstanceTypeDef(TypedDict):
    instanceId: str
    awsAccountId: str
    state: InstanceStateType
    errorMessage: NotRequired[str]
    webAppDnsDomain: NotRequired[str]
    createdTime: NotRequired[datetime]
    lastModifiedTime: NotRequired[datetime]
    instanceName: NotRequired[str]
    instanceDescription: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    versionNumber: NotRequired[float]

class DataIntegrationEventDatasetLoadExecutionDetailsTypeDef(TypedDict):
    status: DataIntegrationEventDatasetLoadStatusType
    message: NotRequired[str]

class DataIntegrationEventDatasetTargetConfigurationTypeDef(TypedDict):
    datasetIdentifier: str
    operationType: DataIntegrationEventDatasetOperationTypeType

class DataIntegrationFlowDatasetSourceTypeDef(TypedDict):
    datasetIdentifier: str

class DataIntegrationFlowExecutionOutputMetadataTypeDef(TypedDict):
    diagnosticReportsRootS3URI: NotRequired[str]

class DataIntegrationFlowS3SourceTypeDef(TypedDict):
    bucketName: str
    key: str

class DataIntegrationFlowFieldPriorityDedupeFieldTypeDef(TypedDict):
    name: str
    sortOrder: DataIntegrationFlowFieldPriorityDedupeSortOrderType

class DataIntegrationFlowS3OptionsTypeDef(TypedDict):
    fileType: NotRequired[DataIntegrationFlowFileTypeType]

class DataIntegrationFlowSQLTransformationConfigurationTypeDef(TypedDict):
    query: str

DataLakeDatasetPartitionFieldTransformTypeDef = TypedDict(
    "DataLakeDatasetPartitionFieldTransformTypeDef",
    {
        "type": DataLakeDatasetPartitionTransformTypeType,
    },
)

class DataLakeDatasetPrimaryKeyFieldTypeDef(TypedDict):
    name: str

DataLakeDatasetSchemaFieldTypeDef = TypedDict(
    "DataLakeDatasetSchemaFieldTypeDef",
    {
        "name": str,
        "type": DataLakeDatasetSchemaFieldTypeType,
        "isRequired": bool,
    },
)

class DeleteDataIntegrationFlowRequestTypeDef(TypedDict):
    instanceId: str
    name: str

class DeleteDataLakeDatasetRequestTypeDef(TypedDict):
    instanceId: str
    namespace: str
    name: str

class DeleteDataLakeNamespaceRequestTypeDef(TypedDict):
    instanceId: str
    name: str

class DeleteInstanceRequestTypeDef(TypedDict):
    instanceId: str

class GetBillOfMaterialsImportJobRequestTypeDef(TypedDict):
    instanceId: str
    jobId: str

class GetDataIntegrationEventRequestTypeDef(TypedDict):
    instanceId: str
    eventId: str

class GetDataIntegrationFlowExecutionRequestTypeDef(TypedDict):
    instanceId: str
    flowName: str
    executionId: str

class GetDataIntegrationFlowRequestTypeDef(TypedDict):
    instanceId: str
    name: str

class GetDataLakeDatasetRequestTypeDef(TypedDict):
    instanceId: str
    namespace: str
    name: str

class GetDataLakeNamespaceRequestTypeDef(TypedDict):
    instanceId: str
    name: str

class GetInstanceRequestTypeDef(TypedDict):
    instanceId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListDataIntegrationEventsRequestTypeDef(TypedDict):
    instanceId: str
    eventType: NotRequired[DataIntegrationEventTypeType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDataIntegrationFlowExecutionsRequestTypeDef(TypedDict):
    instanceId: str
    flowName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDataIntegrationFlowsRequestTypeDef(TypedDict):
    instanceId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDataLakeDatasetsRequestTypeDef(TypedDict):
    instanceId: str
    namespace: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDataLakeNamespacesRequestTypeDef(TypedDict):
    instanceId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListInstancesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    instanceNameFilter: NotRequired[Sequence[str]]
    instanceStateFilter: NotRequired[Sequence[InstanceStateType]]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

TimestampTypeDef = Union[datetime, str]

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateDataLakeDatasetRequestTypeDef(TypedDict):
    instanceId: str
    namespace: str
    name: str
    description: NotRequired[str]

class UpdateDataLakeNamespaceRequestTypeDef(TypedDict):
    instanceId: str
    name: str
    description: NotRequired[str]

class UpdateInstanceRequestTypeDef(TypedDict):
    instanceId: str
    instanceName: NotRequired[str]
    instanceDescription: NotRequired[str]

class CreateBillOfMaterialsImportJobResponseTypeDef(TypedDict):
    jobId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDataIntegrationFlowResponseTypeDef(TypedDict):
    instanceId: str
    name: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDataIntegrationFlowResponseTypeDef(TypedDict):
    instanceId: str
    name: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDataLakeDatasetResponseTypeDef(TypedDict):
    instanceId: str
    namespace: str
    name: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDataLakeNamespaceResponseTypeDef(TypedDict):
    instanceId: str
    name: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetBillOfMaterialsImportJobResponseTypeDef(TypedDict):
    job: BillOfMaterialsImportJobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class SendDataIntegrationEventResponseTypeDef(TypedDict):
    eventId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDataLakeNamespaceResponseTypeDef(TypedDict):
    namespace: DataLakeNamespaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDataLakeNamespaceResponseTypeDef(TypedDict):
    namespace: DataLakeNamespaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDataLakeNamespacesResponseTypeDef(TypedDict):
    namespaces: list[DataLakeNamespaceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateDataLakeNamespaceResponseTypeDef(TypedDict):
    namespace: DataLakeNamespaceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInstanceResponseTypeDef(TypedDict):
    instance: InstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteInstanceResponseTypeDef(TypedDict):
    instance: InstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetInstanceResponseTypeDef(TypedDict):
    instance: InstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListInstancesResponseTypeDef(TypedDict):
    instances: list[InstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateInstanceResponseTypeDef(TypedDict):
    instance: InstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DataIntegrationEventDatasetTargetDetailsTypeDef(TypedDict):
    datasetIdentifier: str
    operationType: DataIntegrationEventDatasetOperationTypeType
    datasetLoadExecution: DataIntegrationEventDatasetLoadExecutionDetailsTypeDef

class DataIntegrationFlowExecutionSourceInfoTypeDef(TypedDict):
    sourceType: DataIntegrationFlowSourceTypeType
    s3Source: NotRequired[DataIntegrationFlowS3SourceTypeDef]
    datasetSource: NotRequired[DataIntegrationFlowDatasetSourceTypeDef]

class DataIntegrationFlowFieldPriorityDedupeStrategyConfigurationOutputTypeDef(TypedDict):
    fields: list[DataIntegrationFlowFieldPriorityDedupeFieldTypeDef]

class DataIntegrationFlowFieldPriorityDedupeStrategyConfigurationTypeDef(TypedDict):
    fields: Sequence[DataIntegrationFlowFieldPriorityDedupeFieldTypeDef]

class DataIntegrationFlowS3SourceConfigurationTypeDef(TypedDict):
    bucketName: str
    prefix: str
    options: NotRequired[DataIntegrationFlowS3OptionsTypeDef]

class DataIntegrationFlowS3TargetConfigurationTypeDef(TypedDict):
    bucketName: str
    prefix: str
    options: NotRequired[DataIntegrationFlowS3OptionsTypeDef]

class DataIntegrationFlowTransformationTypeDef(TypedDict):
    transformationType: DataIntegrationFlowTransformationTypeType
    sqlTransformation: NotRequired[DataIntegrationFlowSQLTransformationConfigurationTypeDef]

class DataLakeDatasetPartitionFieldTypeDef(TypedDict):
    name: str
    transform: DataLakeDatasetPartitionFieldTransformTypeDef

class DataLakeDatasetSchemaOutputTypeDef(TypedDict):
    name: str
    fields: list[DataLakeDatasetSchemaFieldTypeDef]
    primaryKeys: NotRequired[list[DataLakeDatasetPrimaryKeyFieldTypeDef]]

class DataLakeDatasetSchemaTypeDef(TypedDict):
    name: str
    fields: Sequence[DataLakeDatasetSchemaFieldTypeDef]
    primaryKeys: NotRequired[Sequence[DataLakeDatasetPrimaryKeyFieldTypeDef]]

class ListDataIntegrationEventsRequestPaginateTypeDef(TypedDict):
    instanceId: str
    eventType: NotRequired[DataIntegrationEventTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataIntegrationFlowExecutionsRequestPaginateTypeDef(TypedDict):
    instanceId: str
    flowName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataIntegrationFlowsRequestPaginateTypeDef(TypedDict):
    instanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataLakeDatasetsRequestPaginateTypeDef(TypedDict):
    instanceId: str
    namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataLakeNamespacesRequestPaginateTypeDef(TypedDict):
    instanceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInstancesRequestPaginateTypeDef(TypedDict):
    instanceNameFilter: NotRequired[Sequence[str]]
    instanceStateFilter: NotRequired[Sequence[InstanceStateType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SendDataIntegrationEventRequestTypeDef(TypedDict):
    instanceId: str
    eventType: DataIntegrationEventTypeType
    data: str
    eventGroupId: str
    eventTimestamp: NotRequired[TimestampTypeDef]
    clientToken: NotRequired[str]
    datasetTarget: NotRequired[DataIntegrationEventDatasetTargetConfigurationTypeDef]

class DataIntegrationEventTypeDef(TypedDict):
    instanceId: str
    eventId: str
    eventType: DataIntegrationEventTypeType
    eventGroupId: str
    eventTimestamp: datetime
    datasetTargetDetails: NotRequired[DataIntegrationEventDatasetTargetDetailsTypeDef]

class DataIntegrationFlowExecutionTypeDef(TypedDict):
    instanceId: str
    flowName: str
    executionId: str
    status: NotRequired[DataIntegrationFlowExecutionStatusType]
    sourceInfo: NotRequired[DataIntegrationFlowExecutionSourceInfoTypeDef]
    message: NotRequired[str]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    outputMetadata: NotRequired[DataIntegrationFlowExecutionOutputMetadataTypeDef]

DataIntegrationFlowDedupeStrategyOutputTypeDef = TypedDict(
    "DataIntegrationFlowDedupeStrategyOutputTypeDef",
    {
        "type": Literal["FIELD_PRIORITY"],
        "fieldPriority": NotRequired[
            DataIntegrationFlowFieldPriorityDedupeStrategyConfigurationOutputTypeDef
        ],
    },
)
DataIntegrationFlowFieldPriorityDedupeStrategyConfigurationUnionTypeDef = Union[
    DataIntegrationFlowFieldPriorityDedupeStrategyConfigurationTypeDef,
    DataIntegrationFlowFieldPriorityDedupeStrategyConfigurationOutputTypeDef,
]

class DataLakeDatasetPartitionSpecOutputTypeDef(TypedDict):
    fields: list[DataLakeDatasetPartitionFieldTypeDef]

class DataLakeDatasetPartitionSpecTypeDef(TypedDict):
    fields: Sequence[DataLakeDatasetPartitionFieldTypeDef]

DataLakeDatasetSchemaUnionTypeDef = Union[
    DataLakeDatasetSchemaTypeDef, DataLakeDatasetSchemaOutputTypeDef
]

class GetDataIntegrationEventResponseTypeDef(TypedDict):
    event: DataIntegrationEventTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDataIntegrationEventsResponseTypeDef(TypedDict):
    events: list[DataIntegrationEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetDataIntegrationFlowExecutionResponseTypeDef(TypedDict):
    flowExecution: DataIntegrationFlowExecutionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDataIntegrationFlowExecutionsResponseTypeDef(TypedDict):
    flowExecutions: list[DataIntegrationFlowExecutionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DataIntegrationFlowDatasetOptionsOutputTypeDef(TypedDict):
    loadType: NotRequired[DataIntegrationFlowLoadTypeType]
    dedupeRecords: NotRequired[bool]
    dedupeStrategy: NotRequired[DataIntegrationFlowDedupeStrategyOutputTypeDef]

DataIntegrationFlowDedupeStrategyTypeDef = TypedDict(
    "DataIntegrationFlowDedupeStrategyTypeDef",
    {
        "type": Literal["FIELD_PRIORITY"],
        "fieldPriority": NotRequired[
            DataIntegrationFlowFieldPriorityDedupeStrategyConfigurationUnionTypeDef
        ],
    },
)

class DataLakeDatasetTypeDef(TypedDict):
    instanceId: str
    namespace: str
    name: str
    arn: str
    schema: DataLakeDatasetSchemaOutputTypeDef
    createdTime: datetime
    lastModifiedTime: datetime
    description: NotRequired[str]
    partitionSpec: NotRequired[DataLakeDatasetPartitionSpecOutputTypeDef]

DataLakeDatasetPartitionSpecUnionTypeDef = Union[
    DataLakeDatasetPartitionSpecTypeDef, DataLakeDatasetPartitionSpecOutputTypeDef
]

class DataIntegrationFlowDatasetSourceConfigurationOutputTypeDef(TypedDict):
    datasetIdentifier: str
    options: NotRequired[DataIntegrationFlowDatasetOptionsOutputTypeDef]

class DataIntegrationFlowDatasetTargetConfigurationOutputTypeDef(TypedDict):
    datasetIdentifier: str
    options: NotRequired[DataIntegrationFlowDatasetOptionsOutputTypeDef]

DataIntegrationFlowDedupeStrategyUnionTypeDef = Union[
    DataIntegrationFlowDedupeStrategyTypeDef, DataIntegrationFlowDedupeStrategyOutputTypeDef
]

class CreateDataLakeDatasetResponseTypeDef(TypedDict):
    dataset: DataLakeDatasetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDataLakeDatasetResponseTypeDef(TypedDict):
    dataset: DataLakeDatasetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDataLakeDatasetsResponseTypeDef(TypedDict):
    datasets: list[DataLakeDatasetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateDataLakeDatasetResponseTypeDef(TypedDict):
    dataset: DataLakeDatasetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDataLakeDatasetRequestTypeDef(TypedDict):
    instanceId: str
    namespace: str
    name: str
    schema: NotRequired[DataLakeDatasetSchemaUnionTypeDef]
    description: NotRequired[str]
    partitionSpec: NotRequired[DataLakeDatasetPartitionSpecUnionTypeDef]
    tags: NotRequired[Mapping[str, str]]

class DataIntegrationFlowSourceOutputTypeDef(TypedDict):
    sourceType: DataIntegrationFlowSourceTypeType
    sourceName: str
    s3Source: NotRequired[DataIntegrationFlowS3SourceConfigurationTypeDef]
    datasetSource: NotRequired[DataIntegrationFlowDatasetSourceConfigurationOutputTypeDef]

class DataIntegrationFlowTargetOutputTypeDef(TypedDict):
    targetType: DataIntegrationFlowTargetTypeType
    s3Target: NotRequired[DataIntegrationFlowS3TargetConfigurationTypeDef]
    datasetTarget: NotRequired[DataIntegrationFlowDatasetTargetConfigurationOutputTypeDef]

class DataIntegrationFlowDatasetOptionsTypeDef(TypedDict):
    loadType: NotRequired[DataIntegrationFlowLoadTypeType]
    dedupeRecords: NotRequired[bool]
    dedupeStrategy: NotRequired[DataIntegrationFlowDedupeStrategyUnionTypeDef]

class DataIntegrationFlowTypeDef(TypedDict):
    instanceId: str
    name: str
    sources: list[DataIntegrationFlowSourceOutputTypeDef]
    transformation: DataIntegrationFlowTransformationTypeDef
    target: DataIntegrationFlowTargetOutputTypeDef
    createdTime: datetime
    lastModifiedTime: datetime

DataIntegrationFlowDatasetOptionsUnionTypeDef = Union[
    DataIntegrationFlowDatasetOptionsTypeDef, DataIntegrationFlowDatasetOptionsOutputTypeDef
]

class DataIntegrationFlowDatasetTargetConfigurationTypeDef(TypedDict):
    datasetIdentifier: str
    options: NotRequired[DataIntegrationFlowDatasetOptionsTypeDef]

class GetDataIntegrationFlowResponseTypeDef(TypedDict):
    flow: DataIntegrationFlowTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDataIntegrationFlowsResponseTypeDef(TypedDict):
    flows: list[DataIntegrationFlowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateDataIntegrationFlowResponseTypeDef(TypedDict):
    flow: DataIntegrationFlowTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DataIntegrationFlowDatasetSourceConfigurationTypeDef(TypedDict):
    datasetIdentifier: str
    options: NotRequired[DataIntegrationFlowDatasetOptionsUnionTypeDef]

class DataIntegrationFlowTargetTypeDef(TypedDict):
    targetType: DataIntegrationFlowTargetTypeType
    s3Target: NotRequired[DataIntegrationFlowS3TargetConfigurationTypeDef]
    datasetTarget: NotRequired[DataIntegrationFlowDatasetTargetConfigurationTypeDef]

DataIntegrationFlowDatasetSourceConfigurationUnionTypeDef = Union[
    DataIntegrationFlowDatasetSourceConfigurationTypeDef,
    DataIntegrationFlowDatasetSourceConfigurationOutputTypeDef,
]
DataIntegrationFlowTargetUnionTypeDef = Union[
    DataIntegrationFlowTargetTypeDef, DataIntegrationFlowTargetOutputTypeDef
]

class DataIntegrationFlowSourceTypeDef(TypedDict):
    sourceType: DataIntegrationFlowSourceTypeType
    sourceName: str
    s3Source: NotRequired[DataIntegrationFlowS3SourceConfigurationTypeDef]
    datasetSource: NotRequired[DataIntegrationFlowDatasetSourceConfigurationUnionTypeDef]

DataIntegrationFlowSourceUnionTypeDef = Union[
    DataIntegrationFlowSourceTypeDef, DataIntegrationFlowSourceOutputTypeDef
]

class CreateDataIntegrationFlowRequestTypeDef(TypedDict):
    instanceId: str
    name: str
    sources: Sequence[DataIntegrationFlowSourceUnionTypeDef]
    transformation: DataIntegrationFlowTransformationTypeDef
    target: DataIntegrationFlowTargetUnionTypeDef
    tags: NotRequired[Mapping[str, str]]

class UpdateDataIntegrationFlowRequestTypeDef(TypedDict):
    instanceId: str
    name: str
    sources: NotRequired[Sequence[DataIntegrationFlowSourceUnionTypeDef]]
    transformation: NotRequired[DataIntegrationFlowTransformationTypeDef]
    target: NotRequired[DataIntegrationFlowTargetUnionTypeDef]
