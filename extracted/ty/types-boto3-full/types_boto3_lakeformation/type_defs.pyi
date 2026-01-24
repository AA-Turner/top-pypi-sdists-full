"""
Type annotations for lakeformation service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lakeformation/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_lakeformation.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from botocore.response import StreamingBody

from .literals import (
    ApplicationStatusType,
    ComparisonOperatorType,
    CredentialsScopeType,
    DataLakeResourceTypeType,
    EnableStatusType,
    FieldNameStringType,
    OptimizerTypeType,
    PermissionType,
    PermissionTypeType,
    QueryStateStringType,
    ResourceShareTypeType,
    ResourceTypeType,
    ServiceAuthorizationType,
    TransactionStatusFilterType,
    TransactionStatusType,
    TransactionTypeType,
    VerificationStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AddLFTagsToResourceRequestTypeDef",
    "AddLFTagsToResourceResponseTypeDef",
    "AddObjectInputTypeDef",
    "AssumeDecoratedRoleWithSAMLRequestTypeDef",
    "AssumeDecoratedRoleWithSAMLResponseTypeDef",
    "AuditContextTypeDef",
    "BatchGrantPermissionsRequestTypeDef",
    "BatchGrantPermissionsResponseTypeDef",
    "BatchPermissionsFailureEntryTypeDef",
    "BatchPermissionsRequestEntryOutputTypeDef",
    "BatchPermissionsRequestEntryTypeDef",
    "BatchPermissionsRequestEntryUnionTypeDef",
    "BatchRevokePermissionsRequestTypeDef",
    "BatchRevokePermissionsResponseTypeDef",
    "CancelTransactionRequestTypeDef",
    "CatalogResourceTypeDef",
    "ColumnLFTagTypeDef",
    "ColumnWildcardOutputTypeDef",
    "ColumnWildcardTypeDef",
    "ColumnWildcardUnionTypeDef",
    "CommitTransactionRequestTypeDef",
    "CommitTransactionResponseTypeDef",
    "ConditionTypeDef",
    "CreateDataCellsFilterRequestTypeDef",
    "CreateLFTagExpressionRequestTypeDef",
    "CreateLFTagRequestTypeDef",
    "CreateLakeFormationIdentityCenterConfigurationRequestTypeDef",
    "CreateLakeFormationIdentityCenterConfigurationResponseTypeDef",
    "CreateLakeFormationOptInRequestTypeDef",
    "DataCellsFilterOutputTypeDef",
    "DataCellsFilterResourceTypeDef",
    "DataCellsFilterTypeDef",
    "DataCellsFilterUnionTypeDef",
    "DataLakePrincipalTypeDef",
    "DataLakeSettingsOutputTypeDef",
    "DataLakeSettingsTypeDef",
    "DataLakeSettingsUnionTypeDef",
    "DataLocationResourceTypeDef",
    "DatabaseResourceTypeDef",
    "DeleteDataCellsFilterRequestTypeDef",
    "DeleteLFTagExpressionRequestTypeDef",
    "DeleteLFTagRequestTypeDef",
    "DeleteLakeFormationIdentityCenterConfigurationRequestTypeDef",
    "DeleteLakeFormationOptInRequestTypeDef",
    "DeleteObjectInputTypeDef",
    "DeleteObjectsOnCancelRequestTypeDef",
    "DeregisterResourceRequestTypeDef",
    "DescribeLakeFormationIdentityCenterConfigurationRequestTypeDef",
    "DescribeLakeFormationIdentityCenterConfigurationResponseTypeDef",
    "DescribeResourceRequestTypeDef",
    "DescribeResourceResponseTypeDef",
    "DescribeTransactionRequestTypeDef",
    "DescribeTransactionResponseTypeDef",
    "DetailsMapTypeDef",
    "ErrorDetailTypeDef",
    "ExecutionStatisticsTypeDef",
    "ExtendTransactionRequestTypeDef",
    "ExternalFilteringConfigurationOutputTypeDef",
    "ExternalFilteringConfigurationTypeDef",
    "ExternalFilteringConfigurationUnionTypeDef",
    "FilterConditionTypeDef",
    "GetDataCellsFilterRequestTypeDef",
    "GetDataCellsFilterResponseTypeDef",
    "GetDataLakePrincipalResponseTypeDef",
    "GetDataLakeSettingsRequestTypeDef",
    "GetDataLakeSettingsResponseTypeDef",
    "GetEffectivePermissionsForPathRequestTypeDef",
    "GetEffectivePermissionsForPathResponseTypeDef",
    "GetLFTagExpressionRequestTypeDef",
    "GetLFTagExpressionResponseTypeDef",
    "GetLFTagRequestTypeDef",
    "GetLFTagResponseTypeDef",
    "GetQueryStateRequestTypeDef",
    "GetQueryStateResponseTypeDef",
    "GetQueryStatisticsRequestTypeDef",
    "GetQueryStatisticsResponseTypeDef",
    "GetResourceLFTagsRequestTypeDef",
    "GetResourceLFTagsResponseTypeDef",
    "GetTableObjectsRequestTypeDef",
    "GetTableObjectsResponseTypeDef",
    "GetTemporaryDataLocationCredentialsRequestTypeDef",
    "GetTemporaryDataLocationCredentialsResponseTypeDef",
    "GetTemporaryGluePartitionCredentialsRequestTypeDef",
    "GetTemporaryGluePartitionCredentialsResponseTypeDef",
    "GetTemporaryGlueTableCredentialsRequestTypeDef",
    "GetTemporaryGlueTableCredentialsResponseTypeDef",
    "GetWorkUnitResultsRequestTypeDef",
    "GetWorkUnitResultsResponseTypeDef",
    "GetWorkUnitsRequestPaginateTypeDef",
    "GetWorkUnitsRequestTypeDef",
    "GetWorkUnitsResponseTypeDef",
    "GrantPermissionsRequestTypeDef",
    "LFTagErrorTypeDef",
    "LFTagExpressionResourceTypeDef",
    "LFTagExpressionTypeDef",
    "LFTagKeyResourceOutputTypeDef",
    "LFTagKeyResourceTypeDef",
    "LFTagKeyResourceUnionTypeDef",
    "LFTagOutputTypeDef",
    "LFTagPairOutputTypeDef",
    "LFTagPairTypeDef",
    "LFTagPairUnionTypeDef",
    "LFTagPolicyResourceOutputTypeDef",
    "LFTagPolicyResourceTypeDef",
    "LFTagPolicyResourceUnionTypeDef",
    "LFTagTypeDef",
    "LFTagUnionTypeDef",
    "LakeFormationOptInsInfoTypeDef",
    "ListDataCellsFilterRequestPaginateTypeDef",
    "ListDataCellsFilterRequestTypeDef",
    "ListDataCellsFilterResponseTypeDef",
    "ListLFTagExpressionsRequestPaginateTypeDef",
    "ListLFTagExpressionsRequestTypeDef",
    "ListLFTagExpressionsResponseTypeDef",
    "ListLFTagsRequestPaginateTypeDef",
    "ListLFTagsRequestTypeDef",
    "ListLFTagsResponseTypeDef",
    "ListLakeFormationOptInsRequestTypeDef",
    "ListLakeFormationOptInsResponseTypeDef",
    "ListPermissionsRequestTypeDef",
    "ListPermissionsResponseTypeDef",
    "ListResourcesRequestTypeDef",
    "ListResourcesResponseTypeDef",
    "ListTableStorageOptimizersRequestTypeDef",
    "ListTableStorageOptimizersResponseTypeDef",
    "ListTransactionsRequestTypeDef",
    "ListTransactionsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PartitionObjectsTypeDef",
    "PartitionValueListTypeDef",
    "PlanningStatisticsTypeDef",
    "PrincipalPermissionsOutputTypeDef",
    "PrincipalPermissionsTypeDef",
    "PrincipalResourcePermissionsTypeDef",
    "PutDataLakeSettingsRequestTypeDef",
    "QueryPlanningContextTypeDef",
    "QuerySessionContextTypeDef",
    "RedshiftConnectTypeDef",
    "RedshiftScopeUnionTypeDef",
    "RegisterResourceRequestTypeDef",
    "RemoveLFTagsFromResourceRequestTypeDef",
    "RemoveLFTagsFromResourceResponseTypeDef",
    "ResourceInfoTypeDef",
    "ResourceOutputTypeDef",
    "ResourceTypeDef",
    "ResourceUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RevokePermissionsRequestTypeDef",
    "RowFilterOutputTypeDef",
    "RowFilterTypeDef",
    "SearchDatabasesByLFTagsRequestPaginateTypeDef",
    "SearchDatabasesByLFTagsRequestTypeDef",
    "SearchDatabasesByLFTagsResponseTypeDef",
    "SearchTablesByLFTagsRequestPaginateTypeDef",
    "SearchTablesByLFTagsRequestTypeDef",
    "SearchTablesByLFTagsResponseTypeDef",
    "ServiceIntegrationUnionOutputTypeDef",
    "ServiceIntegrationUnionTypeDef",
    "ServiceIntegrationUnionUnionTypeDef",
    "StartQueryPlanningRequestTypeDef",
    "StartQueryPlanningResponseTypeDef",
    "StartTransactionRequestTypeDef",
    "StartTransactionResponseTypeDef",
    "StorageOptimizerTypeDef",
    "TableObjectTypeDef",
    "TableResourceOutputTypeDef",
    "TableResourceTypeDef",
    "TableResourceUnionTypeDef",
    "TableWithColumnsResourceOutputTypeDef",
    "TableWithColumnsResourceTypeDef",
    "TableWithColumnsResourceUnionTypeDef",
    "TaggedDatabaseTypeDef",
    "TaggedTableTypeDef",
    "TemporaryCredentialsTypeDef",
    "TimestampTypeDef",
    "TransactionDescriptionTypeDef",
    "UpdateDataCellsFilterRequestTypeDef",
    "UpdateLFTagExpressionRequestTypeDef",
    "UpdateLFTagRequestTypeDef",
    "UpdateLakeFormationIdentityCenterConfigurationRequestTypeDef",
    "UpdateResourceRequestTypeDef",
    "UpdateTableObjectsRequestTypeDef",
    "UpdateTableStorageOptimizerRequestTypeDef",
    "UpdateTableStorageOptimizerResponseTypeDef",
    "VirtualObjectTypeDef",
    "WorkUnitRangeTypeDef",
    "WriteOperationTypeDef",
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AddObjectInputTypeDef(TypedDict):
    Uri: str
    ETag: str
    Size: int
    PartitionValues: NotRequired[Sequence[str]]

class AssumeDecoratedRoleWithSAMLRequestTypeDef(TypedDict):
    SAMLAssertion: str
    RoleArn: str
    PrincipalArn: str
    DurationSeconds: NotRequired[int]

class AuditContextTypeDef(TypedDict):
    AdditionalAuditContext: NotRequired[str]

class ErrorDetailTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]

class ConditionTypeDef(TypedDict):
    Expression: NotRequired[str]

class DataLakePrincipalTypeDef(TypedDict):
    DataLakePrincipalIdentifier: NotRequired[str]

class CancelTransactionRequestTypeDef(TypedDict):
    TransactionId: str

class CatalogResourceTypeDef(TypedDict):
    Id: NotRequired[str]

class LFTagPairOutputTypeDef(TypedDict):
    TagKey: str
    TagValues: list[str]
    CatalogId: NotRequired[str]

class ColumnWildcardOutputTypeDef(TypedDict):
    ExcludedColumnNames: NotRequired[list[str]]

class ColumnWildcardTypeDef(TypedDict):
    ExcludedColumnNames: NotRequired[Sequence[str]]

class CommitTransactionRequestTypeDef(TypedDict):
    TransactionId: str

class CreateLFTagRequestTypeDef(TypedDict):
    TagKey: str
    TagValues: Sequence[str]
    CatalogId: NotRequired[str]

class RowFilterOutputTypeDef(TypedDict):
    FilterExpression: NotRequired[str]
    AllRowsWildcard: NotRequired[dict[str, Any]]

class DataCellsFilterResourceTypeDef(TypedDict):
    TableCatalogId: NotRequired[str]
    DatabaseName: NotRequired[str]
    TableName: NotRequired[str]
    Name: NotRequired[str]

class RowFilterTypeDef(TypedDict):
    FilterExpression: NotRequired[str]
    AllRowsWildcard: NotRequired[Mapping[str, Any]]

class DataLocationResourceTypeDef(TypedDict):
    ResourceArn: str
    CatalogId: NotRequired[str]

class DatabaseResourceTypeDef(TypedDict):
    Name: str
    CatalogId: NotRequired[str]

class DeleteDataCellsFilterRequestTypeDef(TypedDict):
    TableCatalogId: NotRequired[str]
    DatabaseName: NotRequired[str]
    TableName: NotRequired[str]
    Name: NotRequired[str]

class DeleteLFTagExpressionRequestTypeDef(TypedDict):
    Name: str
    CatalogId: NotRequired[str]

class DeleteLFTagRequestTypeDef(TypedDict):
    TagKey: str
    CatalogId: NotRequired[str]

class DeleteLakeFormationIdentityCenterConfigurationRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]

class DeleteObjectInputTypeDef(TypedDict):
    Uri: str
    ETag: NotRequired[str]
    PartitionValues: NotRequired[Sequence[str]]

class VirtualObjectTypeDef(TypedDict):
    Uri: str
    ETag: NotRequired[str]

class DeregisterResourceRequestTypeDef(TypedDict):
    ResourceArn: str

class DescribeLakeFormationIdentityCenterConfigurationRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]

class ExternalFilteringConfigurationOutputTypeDef(TypedDict):
    Status: EnableStatusType
    AuthorizedTargets: list[str]

class DescribeResourceRequestTypeDef(TypedDict):
    ResourceArn: str

class ResourceInfoTypeDef(TypedDict):
    ResourceArn: NotRequired[str]
    RoleArn: NotRequired[str]
    LastModified: NotRequired[datetime]
    WithFederation: NotRequired[bool]
    HybridAccessEnabled: NotRequired[bool]
    WithPrivilegedAccess: NotRequired[bool]
    VerificationStatus: NotRequired[VerificationStatusType]
    ExpectedResourceOwnerAccount: NotRequired[str]

class DescribeTransactionRequestTypeDef(TypedDict):
    TransactionId: str

class TransactionDescriptionTypeDef(TypedDict):
    TransactionId: NotRequired[str]
    TransactionStatus: NotRequired[TransactionStatusType]
    TransactionStartTime: NotRequired[datetime]
    TransactionEndTime: NotRequired[datetime]

class DetailsMapTypeDef(TypedDict):
    ResourceShare: NotRequired[list[str]]

class ExecutionStatisticsTypeDef(TypedDict):
    AverageExecutionTimeMillis: NotRequired[int]
    DataScannedBytes: NotRequired[int]
    WorkUnitsExecutedCount: NotRequired[int]

class ExtendTransactionRequestTypeDef(TypedDict):
    TransactionId: NotRequired[str]

class ExternalFilteringConfigurationTypeDef(TypedDict):
    Status: EnableStatusType
    AuthorizedTargets: Sequence[str]

class FilterConditionTypeDef(TypedDict):
    Field: NotRequired[FieldNameStringType]
    ComparisonOperator: NotRequired[ComparisonOperatorType]
    StringValueList: NotRequired[Sequence[str]]

class GetDataCellsFilterRequestTypeDef(TypedDict):
    TableCatalogId: str
    DatabaseName: str
    TableName: str
    Name: str

class GetDataLakeSettingsRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]

class GetEffectivePermissionsForPathRequestTypeDef(TypedDict):
    ResourceArn: str
    CatalogId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class GetLFTagExpressionRequestTypeDef(TypedDict):
    Name: str
    CatalogId: NotRequired[str]

class LFTagOutputTypeDef(TypedDict):
    TagKey: str
    TagValues: list[str]

class GetLFTagRequestTypeDef(TypedDict):
    TagKey: str
    CatalogId: NotRequired[str]

class GetQueryStateRequestTypeDef(TypedDict):
    QueryId: str

class GetQueryStatisticsRequestTypeDef(TypedDict):
    QueryId: str

class PlanningStatisticsTypeDef(TypedDict):
    EstimatedDataToScanBytes: NotRequired[int]
    PlanningTimeMillis: NotRequired[int]
    QueueTimeMillis: NotRequired[int]
    WorkUnitsGeneratedCount: NotRequired[int]

TimestampTypeDef = Union[datetime, str]

class TemporaryCredentialsTypeDef(TypedDict):
    AccessKeyId: NotRequired[str]
    SecretAccessKey: NotRequired[str]
    SessionToken: NotRequired[str]
    Expiration: NotRequired[datetime]

class PartitionValueListTypeDef(TypedDict):
    Values: Sequence[str]

class GetWorkUnitResultsRequestTypeDef(TypedDict):
    QueryId: str
    WorkUnitId: int
    WorkUnitToken: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetWorkUnitsRequestTypeDef(TypedDict):
    QueryId: str
    NextToken: NotRequired[str]
    PageSize: NotRequired[int]

class WorkUnitRangeTypeDef(TypedDict):
    WorkUnitIdMax: int
    WorkUnitIdMin: int
    WorkUnitToken: str

class LFTagExpressionResourceTypeDef(TypedDict):
    Name: str
    CatalogId: NotRequired[str]

class LFTagKeyResourceOutputTypeDef(TypedDict):
    TagKey: str
    TagValues: list[str]
    CatalogId: NotRequired[str]

class LFTagKeyResourceTypeDef(TypedDict):
    TagKey: str
    TagValues: Sequence[str]
    CatalogId: NotRequired[str]

class LFTagPairTypeDef(TypedDict):
    TagKey: str
    TagValues: Sequence[str]
    CatalogId: NotRequired[str]

class LFTagTypeDef(TypedDict):
    TagKey: str
    TagValues: Sequence[str]

class ListLFTagExpressionsRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListLFTagsRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    ResourceShareType: NotRequired[ResourceShareTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTableStorageOptimizersRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    CatalogId: NotRequired[str]
    StorageOptimizerType: NotRequired[OptimizerTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class StorageOptimizerTypeDef(TypedDict):
    StorageOptimizerType: NotRequired[OptimizerTypeType]
    Config: NotRequired[dict[str, str]]
    ErrorMessage: NotRequired[str]
    Warnings: NotRequired[str]
    LastRunDetails: NotRequired[str]

class ListTransactionsRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    StatusFilter: NotRequired[TransactionStatusFilterType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class TableObjectTypeDef(TypedDict):
    Uri: NotRequired[str]
    ETag: NotRequired[str]
    Size: NotRequired[int]

class RedshiftConnectTypeDef(TypedDict):
    Authorization: ServiceAuthorizationType

class RegisterResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    UseServiceLinkedRole: NotRequired[bool]
    RoleArn: NotRequired[str]
    WithFederation: NotRequired[bool]
    HybridAccessEnabled: NotRequired[bool]
    WithPrivilegedAccess: NotRequired[bool]
    ExpectedResourceOwnerAccount: NotRequired[str]

class TableResourceOutputTypeDef(TypedDict):
    DatabaseName: str
    CatalogId: NotRequired[str]
    Name: NotRequired[str]
    TableWildcard: NotRequired[dict[str, Any]]

class StartTransactionRequestTypeDef(TypedDict):
    TransactionType: NotRequired[TransactionTypeType]

class TableResourceTypeDef(TypedDict):
    DatabaseName: str
    CatalogId: NotRequired[str]
    Name: NotRequired[str]
    TableWildcard: NotRequired[Mapping[str, Any]]

class UpdateLFTagRequestTypeDef(TypedDict):
    TagKey: str
    CatalogId: NotRequired[str]
    TagValuesToDelete: NotRequired[Sequence[str]]
    TagValuesToAdd: NotRequired[Sequence[str]]

class UpdateResourceRequestTypeDef(TypedDict):
    RoleArn: str
    ResourceArn: str
    WithFederation: NotRequired[bool]
    HybridAccessEnabled: NotRequired[bool]
    ExpectedResourceOwnerAccount: NotRequired[str]

class UpdateTableStorageOptimizerRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    StorageOptimizerConfig: Mapping[OptimizerTypeType, Mapping[str, str]]
    CatalogId: NotRequired[str]

class AssumeDecoratedRoleWithSAMLResponseTypeDef(TypedDict):
    AccessKeyId: str
    SecretAccessKey: str
    SessionToken: str
    Expiration: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CommitTransactionResponseTypeDef(TypedDict):
    TransactionStatus: TransactionStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLakeFormationIdentityCenterConfigurationResponseTypeDef(TypedDict):
    ApplicationArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetDataLakePrincipalResponseTypeDef(TypedDict):
    Identity: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetLFTagResponseTypeDef(TypedDict):
    CatalogId: str
    TagKey: str
    TagValues: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetQueryStateResponseTypeDef(TypedDict):
    Error: str
    State: QueryStateStringType
    ResponseMetadata: ResponseMetadataTypeDef

class GetTemporaryGluePartitionCredentialsResponseTypeDef(TypedDict):
    AccessKeyId: str
    SecretAccessKey: str
    SessionToken: str
    Expiration: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetTemporaryGlueTableCredentialsResponseTypeDef(TypedDict):
    AccessKeyId: str
    SecretAccessKey: str
    SessionToken: str
    Expiration: datetime
    VendedS3Path: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetWorkUnitResultsResponseTypeDef(TypedDict):
    ResultStream: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class StartQueryPlanningResponseTypeDef(TypedDict):
    QueryId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartTransactionResponseTypeDef(TypedDict):
    TransactionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTableStorageOptimizerResponseTypeDef(TypedDict):
    Result: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetTemporaryDataLocationCredentialsRequestTypeDef(TypedDict):
    DurationSeconds: NotRequired[int]
    AuditContext: NotRequired[AuditContextTypeDef]
    DataLocations: NotRequired[Sequence[str]]
    CredentialsScope: NotRequired[CredentialsScopeType]

class PrincipalPermissionsOutputTypeDef(TypedDict):
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Permissions: NotRequired[list[PermissionType]]

class PrincipalPermissionsTypeDef(TypedDict):
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Permissions: NotRequired[Sequence[PermissionType]]

class ColumnLFTagTypeDef(TypedDict):
    Name: NotRequired[str]
    LFTags: NotRequired[list[LFTagPairOutputTypeDef]]

class LFTagErrorTypeDef(TypedDict):
    LFTag: NotRequired[LFTagPairOutputTypeDef]
    Error: NotRequired[ErrorDetailTypeDef]

class ListLFTagsResponseTypeDef(TypedDict):
    LFTags: list[LFTagPairOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TableWithColumnsResourceOutputTypeDef(TypedDict):
    DatabaseName: str
    Name: str
    CatalogId: NotRequired[str]
    ColumnNames: NotRequired[list[str]]
    ColumnWildcard: NotRequired[ColumnWildcardOutputTypeDef]

ColumnWildcardUnionTypeDef = Union[ColumnWildcardTypeDef, ColumnWildcardOutputTypeDef]

class DataCellsFilterOutputTypeDef(TypedDict):
    TableCatalogId: str
    DatabaseName: str
    TableName: str
    Name: str
    RowFilter: NotRequired[RowFilterOutputTypeDef]
    ColumnNames: NotRequired[list[str]]
    ColumnWildcard: NotRequired[ColumnWildcardOutputTypeDef]
    VersionId: NotRequired[str]

class DataCellsFilterTypeDef(TypedDict):
    TableCatalogId: str
    DatabaseName: str
    TableName: str
    Name: str
    RowFilter: NotRequired[RowFilterTypeDef]
    ColumnNames: NotRequired[Sequence[str]]
    ColumnWildcard: NotRequired[ColumnWildcardTypeDef]
    VersionId: NotRequired[str]

class TaggedDatabaseTypeDef(TypedDict):
    Database: NotRequired[DatabaseResourceTypeDef]
    LFTags: NotRequired[list[LFTagPairOutputTypeDef]]

class WriteOperationTypeDef(TypedDict):
    AddObject: NotRequired[AddObjectInputTypeDef]
    DeleteObject: NotRequired[DeleteObjectInputTypeDef]

class DeleteObjectsOnCancelRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    TransactionId: str
    Objects: Sequence[VirtualObjectTypeDef]
    CatalogId: NotRequired[str]

class DescribeResourceResponseTypeDef(TypedDict):
    ResourceInfo: ResourceInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListResourcesResponseTypeDef(TypedDict):
    ResourceInfoList: list[ResourceInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DescribeTransactionResponseTypeDef(TypedDict):
    TransactionDescription: TransactionDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListTransactionsResponseTypeDef(TypedDict):
    Transactions: list[TransactionDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

ExternalFilteringConfigurationUnionTypeDef = Union[
    ExternalFilteringConfigurationTypeDef, ExternalFilteringConfigurationOutputTypeDef
]

class ListResourcesRequestTypeDef(TypedDict):
    FilterConditionList: NotRequired[Sequence[FilterConditionTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class GetLFTagExpressionResponseTypeDef(TypedDict):
    Name: str
    Description: str
    CatalogId: str
    Expression: list[LFTagOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class LFTagExpressionTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    CatalogId: NotRequired[str]
    Expression: NotRequired[list[LFTagOutputTypeDef]]

class LFTagPolicyResourceOutputTypeDef(TypedDict):
    ResourceType: ResourceTypeType
    CatalogId: NotRequired[str]
    Expression: NotRequired[list[LFTagOutputTypeDef]]
    ExpressionName: NotRequired[str]

class GetQueryStatisticsResponseTypeDef(TypedDict):
    ExecutionStatistics: ExecutionStatisticsTypeDef
    PlanningStatistics: PlanningStatisticsTypeDef
    QuerySubmissionTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetTableObjectsRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    CatalogId: NotRequired[str]
    TransactionId: NotRequired[str]
    QueryAsOfTime: NotRequired[TimestampTypeDef]
    PartitionPredicate: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class QueryPlanningContextTypeDef(TypedDict):
    DatabaseName: str
    CatalogId: NotRequired[str]
    QueryAsOfTime: NotRequired[TimestampTypeDef]
    QueryParameters: NotRequired[Mapping[str, str]]
    TransactionId: NotRequired[str]

class QuerySessionContextTypeDef(TypedDict):
    QueryId: NotRequired[str]
    QueryStartTime: NotRequired[TimestampTypeDef]
    ClusterId: NotRequired[str]
    QueryAuthorizationId: NotRequired[str]
    AdditionalContext: NotRequired[Mapping[str, str]]

class GetTemporaryDataLocationCredentialsResponseTypeDef(TypedDict):
    Credentials: TemporaryCredentialsTypeDef
    AccessibleDataLocations: list[str]
    CredentialsScope: CredentialsScopeType
    ResponseMetadata: ResponseMetadataTypeDef

class GetTemporaryGluePartitionCredentialsRequestTypeDef(TypedDict):
    TableArn: str
    Partition: PartitionValueListTypeDef
    Permissions: NotRequired[Sequence[PermissionType]]
    DurationSeconds: NotRequired[int]
    AuditContext: NotRequired[AuditContextTypeDef]
    SupportedPermissionTypes: NotRequired[Sequence[PermissionTypeType]]

class GetWorkUnitsRequestPaginateTypeDef(TypedDict):
    QueryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLFTagExpressionsRequestPaginateTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListLFTagsRequestPaginateTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    ResourceShareType: NotRequired[ResourceShareTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetWorkUnitsResponseTypeDef(TypedDict):
    QueryId: str
    WorkUnitRanges: list[WorkUnitRangeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

LFTagKeyResourceUnionTypeDef = Union[LFTagKeyResourceTypeDef, LFTagKeyResourceOutputTypeDef]
LFTagPairUnionTypeDef = Union[LFTagPairTypeDef, LFTagPairOutputTypeDef]
LFTagUnionTypeDef = Union[LFTagTypeDef, LFTagOutputTypeDef]

class ListTableStorageOptimizersResponseTypeDef(TypedDict):
    StorageOptimizerList: list[StorageOptimizerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class PartitionObjectsTypeDef(TypedDict):
    PartitionValues: NotRequired[list[str]]
    Objects: NotRequired[list[TableObjectTypeDef]]

class RedshiftScopeUnionTypeDef(TypedDict):
    RedshiftConnect: NotRequired[RedshiftConnectTypeDef]

TableResourceUnionTypeDef = Union[TableResourceTypeDef, TableResourceOutputTypeDef]

class DataLakeSettingsOutputTypeDef(TypedDict):
    DataLakeAdmins: NotRequired[list[DataLakePrincipalTypeDef]]
    ReadOnlyAdmins: NotRequired[list[DataLakePrincipalTypeDef]]
    CreateDatabaseDefaultPermissions: NotRequired[list[PrincipalPermissionsOutputTypeDef]]
    CreateTableDefaultPermissions: NotRequired[list[PrincipalPermissionsOutputTypeDef]]
    Parameters: NotRequired[dict[str, str]]
    TrustedResourceOwners: NotRequired[list[str]]
    AllowExternalDataFiltering: NotRequired[bool]
    AllowFullTableExternalDataAccess: NotRequired[bool]
    ExternalDataFilteringAllowList: NotRequired[list[DataLakePrincipalTypeDef]]
    AuthorizedSessionTagValueList: NotRequired[list[str]]

class DataLakeSettingsTypeDef(TypedDict):
    DataLakeAdmins: NotRequired[Sequence[DataLakePrincipalTypeDef]]
    ReadOnlyAdmins: NotRequired[Sequence[DataLakePrincipalTypeDef]]
    CreateDatabaseDefaultPermissions: NotRequired[Sequence[PrincipalPermissionsTypeDef]]
    CreateTableDefaultPermissions: NotRequired[Sequence[PrincipalPermissionsTypeDef]]
    Parameters: NotRequired[Mapping[str, str]]
    TrustedResourceOwners: NotRequired[Sequence[str]]
    AllowExternalDataFiltering: NotRequired[bool]
    AllowFullTableExternalDataAccess: NotRequired[bool]
    ExternalDataFilteringAllowList: NotRequired[Sequence[DataLakePrincipalTypeDef]]
    AuthorizedSessionTagValueList: NotRequired[Sequence[str]]

class GetResourceLFTagsResponseTypeDef(TypedDict):
    LFTagOnDatabase: list[LFTagPairOutputTypeDef]
    LFTagsOnTable: list[LFTagPairOutputTypeDef]
    LFTagsOnColumns: list[ColumnLFTagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TaggedTableTypeDef(TypedDict):
    Table: NotRequired[TableResourceOutputTypeDef]
    LFTagOnDatabase: NotRequired[list[LFTagPairOutputTypeDef]]
    LFTagsOnTable: NotRequired[list[LFTagPairOutputTypeDef]]
    LFTagsOnColumns: NotRequired[list[ColumnLFTagTypeDef]]

class AddLFTagsToResourceResponseTypeDef(TypedDict):
    Failures: list[LFTagErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RemoveLFTagsFromResourceResponseTypeDef(TypedDict):
    Failures: list[LFTagErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TableWithColumnsResourceTypeDef(TypedDict):
    DatabaseName: str
    Name: str
    CatalogId: NotRequired[str]
    ColumnNames: NotRequired[Sequence[str]]
    ColumnWildcard: NotRequired[ColumnWildcardUnionTypeDef]

class GetDataCellsFilterResponseTypeDef(TypedDict):
    DataCellsFilter: DataCellsFilterOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDataCellsFilterResponseTypeDef(TypedDict):
    DataCellsFilters: list[DataCellsFilterOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

DataCellsFilterUnionTypeDef = Union[DataCellsFilterTypeDef, DataCellsFilterOutputTypeDef]

class SearchDatabasesByLFTagsResponseTypeDef(TypedDict):
    DatabaseList: list[TaggedDatabaseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class UpdateTableObjectsRequestTypeDef(TypedDict):
    DatabaseName: str
    TableName: str
    WriteOperations: Sequence[WriteOperationTypeDef]
    CatalogId: NotRequired[str]
    TransactionId: NotRequired[str]

class ListLFTagExpressionsResponseTypeDef(TypedDict):
    LFTagExpressions: list[LFTagExpressionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ResourceOutputTypeDef(TypedDict):
    Catalog: NotRequired[CatalogResourceTypeDef]
    Database: NotRequired[DatabaseResourceTypeDef]
    Table: NotRequired[TableResourceOutputTypeDef]
    TableWithColumns: NotRequired[TableWithColumnsResourceOutputTypeDef]
    DataLocation: NotRequired[DataLocationResourceTypeDef]
    DataCellsFilter: NotRequired[DataCellsFilterResourceTypeDef]
    LFTag: NotRequired[LFTagKeyResourceOutputTypeDef]
    LFTagPolicy: NotRequired[LFTagPolicyResourceOutputTypeDef]
    LFTagExpression: NotRequired[LFTagExpressionResourceTypeDef]

class StartQueryPlanningRequestTypeDef(TypedDict):
    QueryPlanningContext: QueryPlanningContextTypeDef
    QueryString: str

class GetTemporaryGlueTableCredentialsRequestTypeDef(TypedDict):
    TableArn: str
    Permissions: NotRequired[Sequence[PermissionType]]
    DurationSeconds: NotRequired[int]
    AuditContext: NotRequired[AuditContextTypeDef]
    SupportedPermissionTypes: NotRequired[Sequence[PermissionTypeType]]
    S3Path: NotRequired[str]
    QuerySessionContext: NotRequired[QuerySessionContextTypeDef]

class CreateLFTagExpressionRequestTypeDef(TypedDict):
    Name: str
    Expression: Sequence[LFTagUnionTypeDef]
    Description: NotRequired[str]
    CatalogId: NotRequired[str]

class LFTagPolicyResourceTypeDef(TypedDict):
    ResourceType: ResourceTypeType
    CatalogId: NotRequired[str]
    Expression: NotRequired[Sequence[LFTagUnionTypeDef]]
    ExpressionName: NotRequired[str]

class SearchDatabasesByLFTagsRequestPaginateTypeDef(TypedDict):
    Expression: Sequence[LFTagUnionTypeDef]
    CatalogId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchDatabasesByLFTagsRequestTypeDef(TypedDict):
    Expression: Sequence[LFTagUnionTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CatalogId: NotRequired[str]

class SearchTablesByLFTagsRequestPaginateTypeDef(TypedDict):
    Expression: Sequence[LFTagUnionTypeDef]
    CatalogId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class SearchTablesByLFTagsRequestTypeDef(TypedDict):
    Expression: Sequence[LFTagUnionTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CatalogId: NotRequired[str]

class UpdateLFTagExpressionRequestTypeDef(TypedDict):
    Name: str
    Expression: Sequence[LFTagUnionTypeDef]
    Description: NotRequired[str]
    CatalogId: NotRequired[str]

class GetTableObjectsResponseTypeDef(TypedDict):
    Objects: list[PartitionObjectsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ServiceIntegrationUnionOutputTypeDef(TypedDict):
    Redshift: NotRequired[list[RedshiftScopeUnionTypeDef]]

class ServiceIntegrationUnionTypeDef(TypedDict):
    Redshift: NotRequired[Sequence[RedshiftScopeUnionTypeDef]]

class ListDataCellsFilterRequestPaginateTypeDef(TypedDict):
    Table: NotRequired[TableResourceUnionTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDataCellsFilterRequestTypeDef(TypedDict):
    Table: NotRequired[TableResourceUnionTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]

class GetDataLakeSettingsResponseTypeDef(TypedDict):
    DataLakeSettings: DataLakeSettingsOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

DataLakeSettingsUnionTypeDef = Union[DataLakeSettingsTypeDef, DataLakeSettingsOutputTypeDef]

class SearchTablesByLFTagsResponseTypeDef(TypedDict):
    TableList: list[TaggedTableTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

TableWithColumnsResourceUnionTypeDef = Union[
    TableWithColumnsResourceTypeDef, TableWithColumnsResourceOutputTypeDef
]

class CreateDataCellsFilterRequestTypeDef(TypedDict):
    TableData: DataCellsFilterUnionTypeDef

class UpdateDataCellsFilterRequestTypeDef(TypedDict):
    TableData: DataCellsFilterUnionTypeDef

class BatchPermissionsRequestEntryOutputTypeDef(TypedDict):
    Id: str
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Resource: NotRequired[ResourceOutputTypeDef]
    Permissions: NotRequired[list[PermissionType]]
    Condition: NotRequired[ConditionTypeDef]
    PermissionsWithGrantOption: NotRequired[list[PermissionType]]

class LakeFormationOptInsInfoTypeDef(TypedDict):
    Resource: NotRequired[ResourceOutputTypeDef]
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Condition: NotRequired[ConditionTypeDef]
    LastModified: NotRequired[datetime]
    LastUpdatedBy: NotRequired[str]

class PrincipalResourcePermissionsTypeDef(TypedDict):
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Resource: NotRequired[ResourceOutputTypeDef]
    Condition: NotRequired[ConditionTypeDef]
    Permissions: NotRequired[list[PermissionType]]
    PermissionsWithGrantOption: NotRequired[list[PermissionType]]
    AdditionalDetails: NotRequired[DetailsMapTypeDef]
    LastUpdated: NotRequired[datetime]
    LastUpdatedBy: NotRequired[str]

LFTagPolicyResourceUnionTypeDef = Union[
    LFTagPolicyResourceTypeDef, LFTagPolicyResourceOutputTypeDef
]

class DescribeLakeFormationIdentityCenterConfigurationResponseTypeDef(TypedDict):
    CatalogId: str
    InstanceArn: str
    ApplicationArn: str
    ExternalFiltering: ExternalFilteringConfigurationOutputTypeDef
    ShareRecipients: list[DataLakePrincipalTypeDef]
    ServiceIntegrations: list[ServiceIntegrationUnionOutputTypeDef]
    ResourceShare: str
    ResponseMetadata: ResponseMetadataTypeDef

ServiceIntegrationUnionUnionTypeDef = Union[
    ServiceIntegrationUnionTypeDef, ServiceIntegrationUnionOutputTypeDef
]

class PutDataLakeSettingsRequestTypeDef(TypedDict):
    DataLakeSettings: DataLakeSettingsUnionTypeDef
    CatalogId: NotRequired[str]

class BatchPermissionsFailureEntryTypeDef(TypedDict):
    RequestEntry: NotRequired[BatchPermissionsRequestEntryOutputTypeDef]
    Error: NotRequired[ErrorDetailTypeDef]

class ListLakeFormationOptInsResponseTypeDef(TypedDict):
    LakeFormationOptInsInfoList: list[LakeFormationOptInsInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetEffectivePermissionsForPathResponseTypeDef(TypedDict):
    Permissions: list[PrincipalResourcePermissionsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListPermissionsResponseTypeDef(TypedDict):
    PrincipalResourcePermissions: list[PrincipalResourcePermissionsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ResourceTypeDef(TypedDict):
    Catalog: NotRequired[CatalogResourceTypeDef]
    Database: NotRequired[DatabaseResourceTypeDef]
    Table: NotRequired[TableResourceUnionTypeDef]
    TableWithColumns: NotRequired[TableWithColumnsResourceUnionTypeDef]
    DataLocation: NotRequired[DataLocationResourceTypeDef]
    DataCellsFilter: NotRequired[DataCellsFilterResourceTypeDef]
    LFTag: NotRequired[LFTagKeyResourceUnionTypeDef]
    LFTagPolicy: NotRequired[LFTagPolicyResourceUnionTypeDef]
    LFTagExpression: NotRequired[LFTagExpressionResourceTypeDef]

class CreateLakeFormationIdentityCenterConfigurationRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    InstanceArn: NotRequired[str]
    ExternalFiltering: NotRequired[ExternalFilteringConfigurationUnionTypeDef]
    ShareRecipients: NotRequired[Sequence[DataLakePrincipalTypeDef]]
    ServiceIntegrations: NotRequired[Sequence[ServiceIntegrationUnionUnionTypeDef]]

class UpdateLakeFormationIdentityCenterConfigurationRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    ShareRecipients: NotRequired[Sequence[DataLakePrincipalTypeDef]]
    ServiceIntegrations: NotRequired[Sequence[ServiceIntegrationUnionUnionTypeDef]]
    ApplicationStatus: NotRequired[ApplicationStatusType]
    ExternalFiltering: NotRequired[ExternalFilteringConfigurationUnionTypeDef]

class BatchGrantPermissionsResponseTypeDef(TypedDict):
    Failures: list[BatchPermissionsFailureEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchRevokePermissionsResponseTypeDef(TypedDict):
    Failures: list[BatchPermissionsFailureEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

ResourceUnionTypeDef = Union[ResourceTypeDef, ResourceOutputTypeDef]

class AddLFTagsToResourceRequestTypeDef(TypedDict):
    Resource: ResourceUnionTypeDef
    LFTags: Sequence[LFTagPairUnionTypeDef]
    CatalogId: NotRequired[str]

class BatchPermissionsRequestEntryTypeDef(TypedDict):
    Id: str
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Resource: NotRequired[ResourceUnionTypeDef]
    Permissions: NotRequired[Sequence[PermissionType]]
    Condition: NotRequired[ConditionTypeDef]
    PermissionsWithGrantOption: NotRequired[Sequence[PermissionType]]

class CreateLakeFormationOptInRequestTypeDef(TypedDict):
    Principal: DataLakePrincipalTypeDef
    Resource: ResourceUnionTypeDef
    Condition: NotRequired[ConditionTypeDef]

class DeleteLakeFormationOptInRequestTypeDef(TypedDict):
    Principal: DataLakePrincipalTypeDef
    Resource: ResourceUnionTypeDef
    Condition: NotRequired[ConditionTypeDef]

class GetResourceLFTagsRequestTypeDef(TypedDict):
    Resource: ResourceUnionTypeDef
    CatalogId: NotRequired[str]
    ShowAssignedLFTags: NotRequired[bool]

class GrantPermissionsRequestTypeDef(TypedDict):
    Principal: DataLakePrincipalTypeDef
    Resource: ResourceUnionTypeDef
    Permissions: Sequence[PermissionType]
    CatalogId: NotRequired[str]
    Condition: NotRequired[ConditionTypeDef]
    PermissionsWithGrantOption: NotRequired[Sequence[PermissionType]]

class ListLakeFormationOptInsRequestTypeDef(TypedDict):
    Principal: NotRequired[DataLakePrincipalTypeDef]
    Resource: NotRequired[ResourceUnionTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListPermissionsRequestTypeDef(TypedDict):
    CatalogId: NotRequired[str]
    Principal: NotRequired[DataLakePrincipalTypeDef]
    ResourceType: NotRequired[DataLakeResourceTypeType]
    Resource: NotRequired[ResourceUnionTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    IncludeRelated: NotRequired[str]

class RemoveLFTagsFromResourceRequestTypeDef(TypedDict):
    Resource: ResourceUnionTypeDef
    LFTags: Sequence[LFTagPairUnionTypeDef]
    CatalogId: NotRequired[str]

class RevokePermissionsRequestTypeDef(TypedDict):
    Principal: DataLakePrincipalTypeDef
    Resource: ResourceUnionTypeDef
    Permissions: Sequence[PermissionType]
    CatalogId: NotRequired[str]
    Condition: NotRequired[ConditionTypeDef]
    PermissionsWithGrantOption: NotRequired[Sequence[PermissionType]]

BatchPermissionsRequestEntryUnionTypeDef = Union[
    BatchPermissionsRequestEntryTypeDef, BatchPermissionsRequestEntryOutputTypeDef
]

class BatchGrantPermissionsRequestTypeDef(TypedDict):
    Entries: Sequence[BatchPermissionsRequestEntryUnionTypeDef]
    CatalogId: NotRequired[str]

class BatchRevokePermissionsRequestTypeDef(TypedDict):
    Entries: Sequence[BatchPermissionsRequestEntryUnionTypeDef]
    CatalogId: NotRequired[str]
