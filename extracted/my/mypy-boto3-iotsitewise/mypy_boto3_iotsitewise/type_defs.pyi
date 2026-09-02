"""
Type annotations for iotsitewise service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_iotsitewise.type_defs import AccessDeniedExceptionTypeDef

    data: AccessDeniedExceptionTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    AggregateTypeType,
    ApplicationStatusType,
    AssetModelStateType,
    AssetModelTypeType,
    AssetModelVersionTypeType,
    AssetStateType,
    AuthModeType,
    BatchEntryCompletionStatusType,
    BatchGetAssetPropertyAggregatesErrorCodeType,
    BatchGetAssetPropertyValueErrorCodeType,
    BatchGetAssetPropertyValueHistoryErrorCodeType,
    BatchPutAssetPropertyValueErrorCodeType,
    CapabilitySyncStatusType,
    ColumnNameType,
    ComputationModelStateType,
    ComputeLocationType,
    ComputeNodeErrorCodeType,
    ComputeNodeExecutionStateType,
    ConfigurationStateType,
    CoreDeviceOperatingSystemType,
    DataSegmentErrorCodeType,
    DatasetEnrichmentStatusType,
    DatasetExportJobFilterType,
    DatasetExportJobStatusType,
    DatasetSourceFormatType,
    DatasetSourceTypeType,
    DatasetStateType,
    DatasetTypeEnumType,
    DetailedErrorCodeType,
    DetailedPipelineErrorCodeType,
    DisassociatedDataStorageStateType,
    EncryptionTypeType,
    EnrichmentJobStatusType,
    EnrichmentStatusType,
    ErrorCodeType,
    ExecutionStateType,
    ExportDataTypeType,
    ForwardingConfigStateType,
    IdentityTypeType,
    JobStatusType,
    ListAssetModelPropertiesFilterType,
    ListAssetPropertiesFilterType,
    ListAssetsFilterType,
    ListBulkImportJobsFilterType,
    ListTimeSeriesTypeType,
    LoggingLevelType,
    MonitorErrorCodeType,
    PermissionType,
    PipelineErrorCodeType,
    PipelineExecutionStateType,
    PortalStateType,
    PortalTypeType,
    ProcessingTypeType,
    ProcessingUnitType,
    PropertyDataTypeType,
    PropertyNotificationStateType,
    QualityType,
    QueryStatusType,
    RawValueTypeType,
    ResourceErrorCodeType,
    ResourceStateType,
    ResourceTypeType,
    ScalarTypeType,
    SearchStatusType,
    SearchTypeType,
    StorageClassType,
    StorageTypeType,
    TargetResourceTypeType,
    TimeOrderingType,
    TraversalDirectionType,
    WarmTierStateType,
    WorkspaceStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccessDeniedExceptionTypeDef",
    "AccessPolicySummaryTypeDef",
    "ActionDefinitionTypeDef",
    "ActionPayloadTypeDef",
    "ActionSummaryTypeDef",
    "AggregatedValueTypeDef",
    "AggregatesTypeDef",
    "AlarmsTypeDef",
    "ApplicationSummaryTypeDef",
    "AssetBindingValueFilterTypeDef",
    "AssetCompositeModelPathSegmentTypeDef",
    "AssetCompositeModelSummaryTypeDef",
    "AssetCompositeModelTypeDef",
    "AssetErrorDetailsTypeDef",
    "AssetHierarchyInfoTypeDef",
    "AssetHierarchyTypeDef",
    "AssetModelBindingValueFilterTypeDef",
    "AssetModelCompositeModelDefinitionTypeDef",
    "AssetModelCompositeModelOutputTypeDef",
    "AssetModelCompositeModelPathSegmentTypeDef",
    "AssetModelCompositeModelSummaryTypeDef",
    "AssetModelCompositeModelTypeDef",
    "AssetModelCompositeModelUnionTypeDef",
    "AssetModelHierarchyDefinitionTypeDef",
    "AssetModelHierarchyTypeDef",
    "AssetModelPropertyBindingValueFilterTypeDef",
    "AssetModelPropertyBindingValueTypeDef",
    "AssetModelPropertyDefinitionTypeDef",
    "AssetModelPropertyOutputTypeDef",
    "AssetModelPropertyPathSegmentTypeDef",
    "AssetModelPropertySummaryTypeDef",
    "AssetModelPropertyTypeDef",
    "AssetModelPropertyUnionTypeDef",
    "AssetModelStatusTypeDef",
    "AssetModelSummaryTypeDef",
    "AssetPropertyBindingValueFilterTypeDef",
    "AssetPropertyBindingValueTypeDef",
    "AssetPropertyPathSegmentTypeDef",
    "AssetPropertySummaryTypeDef",
    "AssetPropertyTypeDef",
    "AssetPropertyValueTypeDef",
    "AssetRelationshipSummaryTypeDef",
    "AssetStatusTypeDef",
    "AssetSummaryTypeDef",
    "AssociateAssetsRequestTypeDef",
    "AssociateDataSegmentEntryTypeDef",
    "AssociateTimeSeriesToAssetPropertyRequestTypeDef",
    "AssociatedAssetsSummaryTypeDef",
    "AttributeTypeDef",
    "BatchAssociateDataSegmentsToDatasetRequestTypeDef",
    "BatchAssociateDataSegmentsToDatasetResponseTypeDef",
    "BatchAssociateProjectAssetsRequestTypeDef",
    "BatchAssociateProjectAssetsResponseTypeDef",
    "BatchDeleteDatasetDataSegmentsRequestTypeDef",
    "BatchDeleteDatasetDataSegmentsResponseTypeDef",
    "BatchDisassociateDataSegmentsFromDatasetRequestTypeDef",
    "BatchDisassociateDataSegmentsFromDatasetResponseTypeDef",
    "BatchDisassociateProjectAssetsRequestTypeDef",
    "BatchDisassociateProjectAssetsResponseTypeDef",
    "BatchGetAssetPropertyAggregatesEntryTypeDef",
    "BatchGetAssetPropertyAggregatesErrorEntryTypeDef",
    "BatchGetAssetPropertyAggregatesErrorInfoTypeDef",
    "BatchGetAssetPropertyAggregatesRequestTypeDef",
    "BatchGetAssetPropertyAggregatesResponseTypeDef",
    "BatchGetAssetPropertyAggregatesSkippedEntryTypeDef",
    "BatchGetAssetPropertyAggregatesSuccessEntryTypeDef",
    "BatchGetAssetPropertyValueEntryTypeDef",
    "BatchGetAssetPropertyValueErrorEntryTypeDef",
    "BatchGetAssetPropertyValueErrorInfoTypeDef",
    "BatchGetAssetPropertyValueHistoryEntryTypeDef",
    "BatchGetAssetPropertyValueHistoryErrorEntryTypeDef",
    "BatchGetAssetPropertyValueHistoryErrorInfoTypeDef",
    "BatchGetAssetPropertyValueHistoryRequestTypeDef",
    "BatchGetAssetPropertyValueHistoryResponseTypeDef",
    "BatchGetAssetPropertyValueHistorySkippedEntryTypeDef",
    "BatchGetAssetPropertyValueHistorySuccessEntryTypeDef",
    "BatchGetAssetPropertyValueRequestTypeDef",
    "BatchGetAssetPropertyValueResponseTypeDef",
    "BatchGetAssetPropertyValueSkippedEntryTypeDef",
    "BatchGetAssetPropertyValueSuccessEntryTypeDef",
    "BatchPutAssetPropertyErrorEntryTypeDef",
    "BatchPutAssetPropertyErrorTypeDef",
    "BatchPutAssetPropertyValueRequestTypeDef",
    "BatchPutAssetPropertyValueResponseTypeDef",
    "BlobTypeDef",
    "CancelEnrichmentJobRequestTypeDef",
    "CancelEnrichmentJobResponseTypeDef",
    "CancelPipelineExecutionRequestTypeDef",
    "CancelPipelineExecutionResponseTypeDef",
    "CancelQueryRequestTypeDef",
    "CancelQueryResponseTypeDef",
    "CitationTypeDef",
    "ColumnInfoTypeDef",
    "ColumnInformationTypeDef",
    "ColumnTypeTypeDef",
    "CompositeModelPropertyTypeDef",
    "CompositionDetailsTypeDef",
    "CompositionRelationshipItemTypeDef",
    "CompositionRelationshipSummaryTypeDef",
    "ComputationModelAnomalyDetectionConfigurationTypeDef",
    "ComputationModelConfigurationTypeDef",
    "ComputationModelDataBindingUsageSummaryTypeDef",
    "ComputationModelDataBindingValueOutputTypeDef",
    "ComputationModelDataBindingValueTypeDef",
    "ComputationModelDataBindingValueUnionTypeDef",
    "ComputationModelResolveToResourceSummaryTypeDef",
    "ComputationModelStatusTypeDef",
    "ComputationModelSummaryTypeDef",
    "ComputeNodeExecutionDetailsTypeDef",
    "ComputeNodeExecutionStateDetailsTypeDef",
    "ComputeNodeExecutionStatusTypeDef",
    "ComputeNodeOutputTypeDef",
    "ComputeNodeTypeDef",
    "ComputeNodeUnionTypeDef",
    "ConfigurationErrorDetailsTypeDef",
    "ConfigurationStatusTypeDef",
    "ConflictingOperationExceptionTypeDef",
    "ContainerTaskConfigurationOutputTypeDef",
    "ContainerTaskConfigurationTypeDef",
    "ContentTypeDef",
    "CreateAccessPolicyRequestTypeDef",
    "CreateAccessPolicyResponseTypeDef",
    "CreateApplicationRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateAssetModelCompositeModelRequestTypeDef",
    "CreateAssetModelCompositeModelResponseTypeDef",
    "CreateAssetModelRequestTypeDef",
    "CreateAssetModelResponseTypeDef",
    "CreateAssetRequestTypeDef",
    "CreateAssetResponseTypeDef",
    "CreateBulkImportJobRequestTypeDef",
    "CreateBulkImportJobResponseTypeDef",
    "CreateComputationModelRequestTypeDef",
    "CreateComputationModelResponseTypeDef",
    "CreateDashboardRequestTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateDatasetExportJobRequestTypeDef",
    "CreateDatasetExportJobResponseTypeDef",
    "CreateDatasetRequestTypeDef",
    "CreateDatasetResponseTypeDef",
    "CreateEnrichmentJobRequestTypeDef",
    "CreateEnrichmentJobResponseTypeDef",
    "CreateGatewayRequestTypeDef",
    "CreateGatewayResponseTypeDef",
    "CreatePipelineRequestTypeDef",
    "CreatePipelineResponseTypeDef",
    "CreatePortalRequestTypeDef",
    "CreatePortalResponseTypeDef",
    "CreateProjectRequestTypeDef",
    "CreateProjectResponseTypeDef",
    "CreateTaskRequestTypeDef",
    "CreateTaskResponseTypeDef",
    "CreateWorkspaceRequestTypeDef",
    "CreateWorkspaceResponseTypeDef",
    "CsvOutputTypeDef",
    "CsvTypeDef",
    "CsvUnionTypeDef",
    "CustomerManagedS3StorageTypeDef",
    "DashboardSummaryTypeDef",
    "DataBindingValueFilterTypeDef",
    "DataBindingValueTypeDef",
    "DataSegmentEnrichmentTypeDef",
    "DataSegmentRelationshipSummaryTypeDef",
    "DataSegmentSummaryTypeDef",
    "DataSetReferenceTypeDef",
    "DatasetConfigTypeDef",
    "DatasetEnrichmentEntryTypeDef",
    "DatasetEnrichmentTypeDef",
    "DatasetItemOutputTypeDef",
    "DatasetItemTypeDef",
    "DatasetSourceTypeDef",
    "DatasetStatusTypeDef",
    "DatasetSummaryTypeDef",
    "DatumPaginatorTypeDef",
    "DatumTypeDef",
    "DeleteAccessPolicyRequestTypeDef",
    "DeleteApplicationRequestTypeDef",
    "DeleteAssetModelCompositeModelRequestTypeDef",
    "DeleteAssetModelCompositeModelResponseTypeDef",
    "DeleteAssetModelInterfaceRelationshipRequestTypeDef",
    "DeleteAssetModelInterfaceRelationshipResponseTypeDef",
    "DeleteAssetModelRequestTypeDef",
    "DeleteAssetModelResponseTypeDef",
    "DeleteAssetRequestTypeDef",
    "DeleteAssetResponseTypeDef",
    "DeleteComputationModelRequestTypeDef",
    "DeleteComputationModelResponseTypeDef",
    "DeleteDashboardRequestTypeDef",
    "DeleteDataSegmentEntryTypeDef",
    "DeleteDatasetRequestTypeDef",
    "DeleteDatasetResponseTypeDef",
    "DeleteGatewayRequestTypeDef",
    "DeletePipelineRequestTypeDef",
    "DeletePipelineResponseTypeDef",
    "DeletePortalRequestTypeDef",
    "DeletePortalResponseTypeDef",
    "DeleteProjectRequestTypeDef",
    "DeleteTaskRequestTypeDef",
    "DeleteTaskResponseTypeDef",
    "DeleteTimeSeriesRequestTypeDef",
    "DeleteWorkspaceRequestTypeDef",
    "DeleteWorkspaceResponseTypeDef",
    "DescribeAccessPolicyRequestTypeDef",
    "DescribeAccessPolicyResponseTypeDef",
    "DescribeActionRequestTypeDef",
    "DescribeActionResponseTypeDef",
    "DescribeApplicationRequestTypeDef",
    "DescribeApplicationResponseTypeDef",
    "DescribeAssetCompositeModelRequestTypeDef",
    "DescribeAssetCompositeModelResponseTypeDef",
    "DescribeAssetModelCompositeModelRequestTypeDef",
    "DescribeAssetModelCompositeModelResponseTypeDef",
    "DescribeAssetModelInterfaceRelationshipRequestTypeDef",
    "DescribeAssetModelInterfaceRelationshipResponseTypeDef",
    "DescribeAssetModelRequestTypeDef",
    "DescribeAssetModelRequestWaitExtraTypeDef",
    "DescribeAssetModelRequestWaitTypeDef",
    "DescribeAssetModelResponseTypeDef",
    "DescribeAssetPropertyRequestTypeDef",
    "DescribeAssetPropertyResponseTypeDef",
    "DescribeAssetRequestTypeDef",
    "DescribeAssetRequestWaitExtraTypeDef",
    "DescribeAssetRequestWaitTypeDef",
    "DescribeAssetResponseTypeDef",
    "DescribeBulkImportJobRequestTypeDef",
    "DescribeBulkImportJobResponseTypeDef",
    "DescribeComputationModelExecutionSummaryRequestTypeDef",
    "DescribeComputationModelExecutionSummaryResponseTypeDef",
    "DescribeComputationModelRequestTypeDef",
    "DescribeComputationModelResponseTypeDef",
    "DescribeDashboardRequestTypeDef",
    "DescribeDashboardResponseTypeDef",
    "DescribeDatasetExportJobRequestTypeDef",
    "DescribeDatasetExportJobResponseTypeDef",
    "DescribeDatasetRequestTypeDef",
    "DescribeDatasetResponseTypeDef",
    "DescribeDefaultEncryptionConfigurationResponseTypeDef",
    "DescribeEnrichmentJobRequestTypeDef",
    "DescribeEnrichmentJobResponseTypeDef",
    "DescribeExecutionRequestTypeDef",
    "DescribeExecutionResponseTypeDef",
    "DescribeGatewayCapabilityConfigurationRequestTypeDef",
    "DescribeGatewayCapabilityConfigurationResponseTypeDef",
    "DescribeGatewayRequestTypeDef",
    "DescribeGatewayResponseTypeDef",
    "DescribeLoggingOptionsRequestTypeDef",
    "DescribeLoggingOptionsResponseTypeDef",
    "DescribePipelineExecutionRequestPaginateTypeDef",
    "DescribePipelineExecutionRequestTypeDef",
    "DescribePipelineExecutionResponseTypeDef",
    "DescribePipelineRequestTypeDef",
    "DescribePipelineResponseTypeDef",
    "DescribePortalRequestTypeDef",
    "DescribePortalRequestWaitExtraTypeDef",
    "DescribePortalRequestWaitTypeDef",
    "DescribePortalResponseTypeDef",
    "DescribeProjectRequestTypeDef",
    "DescribeProjectResponseTypeDef",
    "DescribeQueryRequestTypeDef",
    "DescribeQueryResponseTypeDef",
    "DescribeSearchRequestTypeDef",
    "DescribeSearchResponseTypeDef",
    "DescribeStorageConfigurationResponseTypeDef",
    "DescribeTaskRequestTypeDef",
    "DescribeTaskResponseTypeDef",
    "DescribeTimeSeriesRequestTypeDef",
    "DescribeTimeSeriesResponseTypeDef",
    "DescribeWorkspaceRequestTypeDef",
    "DescribeWorkspaceResponseTypeDef",
    "DetailedErrorTypeDef",
    "DetailedPipelineErrorTypeDef",
    "DisassociateAssetsRequestTypeDef",
    "DisassociateDataSegmentEntryTypeDef",
    "DisassociateTimeSeriesFromAssetPropertyRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnrichmentJobConfigurationTypeDef",
    "EnrichmentJobSummaryTypeDef",
    "EnrichmentTrimSettingsTypeDef",
    "EphemeralStorageConfigurationTypeDef",
    "ErrorDetailsTypeDef",
    "ErrorReportLocationTypeDef",
    "EventDetectionTypeDef",
    "ExecuteActionRequestTypeDef",
    "ExecuteActionResponseTypeDef",
    "ExecuteQueryRequestPaginateTypeDef",
    "ExecuteQueryRequestTypeDef",
    "ExecuteQueryResponsePaginatorTypeDef",
    "ExecuteQueryResponseTypeDef",
    "ExecutionEnvironmentVariablesOutputTypeDef",
    "ExecutionEnvironmentVariablesTypeDef",
    "ExecutionEnvironmentVariablesUnionTypeDef",
    "ExecutionStatusTypeDef",
    "ExecutionSummaryTypeDef",
    "ExportErrorReportLocationTypeDef",
    "ExportJobSummaryTypeDef",
    "ExpressionVariableOutputTypeDef",
    "ExpressionVariableTypeDef",
    "ExpressionVariableUnionTypeDef",
    "FailedDataSegmentAssociationTypeDef",
    "FailedDataSegmentDeletionTypeDef",
    "FailedDataSegmentDisassociationTypeDef",
    "FileFormatOutputTypeDef",
    "FileFormatTypeDef",
    "FileFormatUnionTypeDef",
    "FileOutputTypeDef",
    "FileTypeDef",
    "FileUnionTypeDef",
    "FormatSettingsTypeDef",
    "ForwardingConfigTypeDef",
    "GatewayCapabilitySummaryTypeDef",
    "GatewayPlatformTypeDef",
    "GatewaySummaryTypeDef",
    "GetAssetPropertyAggregatesRequestPaginateTypeDef",
    "GetAssetPropertyAggregatesRequestTypeDef",
    "GetAssetPropertyAggregatesResponseTypeDef",
    "GetAssetPropertyValueHistoryRequestPaginateTypeDef",
    "GetAssetPropertyValueHistoryRequestTypeDef",
    "GetAssetPropertyValueHistoryResponseTypeDef",
    "GetAssetPropertyValueRequestTypeDef",
    "GetAssetPropertyValueResponseTypeDef",
    "GetCaptureDataRequestTypeDef",
    "GetCaptureDataResponseTypeDef",
    "GetInterpolatedAssetPropertyValuesRequestPaginateTypeDef",
    "GetInterpolatedAssetPropertyValuesRequestTypeDef",
    "GetInterpolatedAssetPropertyValuesResponseTypeDef",
    "GetQueryResultsRequestPaginateTypeDef",
    "GetQueryResultsRequestTypeDef",
    "GetQueryResultsResponseTypeDef",
    "GetSearchResultsRequestPaginateTypeDef",
    "GetSearchResultsRequestTypeDef",
    "GetSearchResultsResponseTypeDef",
    "GreengrassTypeDef",
    "GreengrassV2TypeDef",
    "GroupIdentityTypeDef",
    "HierarchyMappingTypeDef",
    "IAMRoleIdentityTypeDef",
    "IAMUserIdentityTypeDef",
    "IdentityTypeDef",
    "ImageFileTypeDef",
    "ImageLocationTypeDef",
    "ImageTypeDef",
    "InterfaceRelationshipSummaryTypeDef",
    "InterfaceRelationshipTypeDef",
    "InterfaceSummaryTypeDef",
    "InternalFailureExceptionTypeDef",
    "InterpolatedAssetPropertyValueTypeDef",
    "InvalidRequestExceptionTypeDef",
    "InvocationOutputTypeDef",
    "InvokeAssistantRequestTypeDef",
    "InvokeAssistantResponseTypeDef",
    "JobConfigurationOutputTypeDef",
    "JobConfigurationTypeDef",
    "JobConfigurationUnionTypeDef",
    "JobSummaryTypeDef",
    "KendraSourceDetailTypeDef",
    "LimitExceededExceptionTypeDef",
    "ListAccessPoliciesRequestPaginateTypeDef",
    "ListAccessPoliciesRequestTypeDef",
    "ListAccessPoliciesResponseTypeDef",
    "ListActionsRequestPaginateTypeDef",
    "ListActionsRequestTypeDef",
    "ListActionsResponseTypeDef",
    "ListApplicationsRequestPaginateTypeDef",
    "ListApplicationsRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListAssetModelCompositeModelsRequestPaginateTypeDef",
    "ListAssetModelCompositeModelsRequestTypeDef",
    "ListAssetModelCompositeModelsResponseTypeDef",
    "ListAssetModelPropertiesRequestPaginateTypeDef",
    "ListAssetModelPropertiesRequestTypeDef",
    "ListAssetModelPropertiesResponseTypeDef",
    "ListAssetModelsRequestPaginateTypeDef",
    "ListAssetModelsRequestTypeDef",
    "ListAssetModelsResponseTypeDef",
    "ListAssetPropertiesRequestPaginateTypeDef",
    "ListAssetPropertiesRequestTypeDef",
    "ListAssetPropertiesResponseTypeDef",
    "ListAssetRelationshipsRequestPaginateTypeDef",
    "ListAssetRelationshipsRequestTypeDef",
    "ListAssetRelationshipsResponseTypeDef",
    "ListAssetsRequestPaginateTypeDef",
    "ListAssetsRequestTypeDef",
    "ListAssetsResponseTypeDef",
    "ListAssociatedAssetsRequestPaginateTypeDef",
    "ListAssociatedAssetsRequestTypeDef",
    "ListAssociatedAssetsResponseTypeDef",
    "ListBulkImportJobsRequestPaginateTypeDef",
    "ListBulkImportJobsRequestTypeDef",
    "ListBulkImportJobsResponseTypeDef",
    "ListCompositionRelationshipsRequestPaginateTypeDef",
    "ListCompositionRelationshipsRequestTypeDef",
    "ListCompositionRelationshipsResponseTypeDef",
    "ListComputationModelDataBindingUsagesRequestPaginateTypeDef",
    "ListComputationModelDataBindingUsagesRequestTypeDef",
    "ListComputationModelDataBindingUsagesResponseTypeDef",
    "ListComputationModelResolveToResourcesRequestPaginateTypeDef",
    "ListComputationModelResolveToResourcesRequestTypeDef",
    "ListComputationModelResolveToResourcesResponseTypeDef",
    "ListComputationModelsRequestPaginateTypeDef",
    "ListComputationModelsRequestTypeDef",
    "ListComputationModelsResponseTypeDef",
    "ListDashboardsRequestPaginateTypeDef",
    "ListDashboardsRequestTypeDef",
    "ListDashboardsResponseTypeDef",
    "ListDatasetDataSegmentRelationshipsRequestPaginateTypeDef",
    "ListDatasetDataSegmentRelationshipsRequestTypeDef",
    "ListDatasetDataSegmentRelationshipsResponseTypeDef",
    "ListDatasetDataSegmentsRequestPaginateTypeDef",
    "ListDatasetDataSegmentsRequestTypeDef",
    "ListDatasetDataSegmentsResponseTypeDef",
    "ListDatasetExportJobsRequestPaginateTypeDef",
    "ListDatasetExportJobsRequestTypeDef",
    "ListDatasetExportJobsResponseTypeDef",
    "ListDatasetsRequestPaginateTypeDef",
    "ListDatasetsRequestTypeDef",
    "ListDatasetsResponseTypeDef",
    "ListEnrichmentJobsRequestPaginateTypeDef",
    "ListEnrichmentJobsRequestTypeDef",
    "ListEnrichmentJobsResponseTypeDef",
    "ListExecutionsRequestPaginateTypeDef",
    "ListExecutionsRequestTypeDef",
    "ListExecutionsResponseTypeDef",
    "ListGatewaysRequestPaginateTypeDef",
    "ListGatewaysRequestTypeDef",
    "ListGatewaysResponseTypeDef",
    "ListInterfaceRelationshipsRequestPaginateTypeDef",
    "ListInterfaceRelationshipsRequestTypeDef",
    "ListInterfaceRelationshipsResponseTypeDef",
    "ListPipelineExecutionsRequestPaginateTypeDef",
    "ListPipelineExecutionsRequestTypeDef",
    "ListPipelineExecutionsResponseTypeDef",
    "ListPipelinesRequestPaginateTypeDef",
    "ListPipelinesRequestTypeDef",
    "ListPipelinesResponseTypeDef",
    "ListPortalsRequestPaginateTypeDef",
    "ListPortalsRequestTypeDef",
    "ListPortalsResponseTypeDef",
    "ListProjectAssetsRequestPaginateTypeDef",
    "ListProjectAssetsRequestTypeDef",
    "ListProjectAssetsResponseTypeDef",
    "ListProjectsRequestPaginateTypeDef",
    "ListProjectsRequestTypeDef",
    "ListProjectsResponseTypeDef",
    "ListQueriesRequestPaginateTypeDef",
    "ListQueriesRequestTypeDef",
    "ListQueriesResponseTypeDef",
    "ListSearchesFiltersTypeDef",
    "ListSearchesRequestPaginateTypeDef",
    "ListSearchesRequestTypeDef",
    "ListSearchesResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTasksRequestPaginateTypeDef",
    "ListTasksRequestTypeDef",
    "ListTasksResponseTypeDef",
    "ListTimeSeriesRequestPaginateTypeDef",
    "ListTimeSeriesRequestTypeDef",
    "ListTimeSeriesResponseTypeDef",
    "ListWorkspacesRequestPaginateTypeDef",
    "ListWorkspacesRequestTypeDef",
    "ListWorkspacesResponseTypeDef",
    "LocationTypeDef",
    "LoggingOptionsTypeDef",
    "MatchedDataBindingTypeDef",
    "MeasurementProcessingConfigTypeDef",
    "MeasurementTypeDef",
    "MetricOutputTypeDef",
    "MetricProcessingConfigTypeDef",
    "MetricTypeDef",
    "MetricUnionTypeDef",
    "MetricWindowTypeDef",
    "MonitorErrorDetailsTypeDef",
    "MountOverridesOutputTypeDef",
    "MountOverridesTypeDef",
    "MountOverridesUnionTypeDef",
    "MountSourceTypeDef",
    "MountTypeDef",
    "MultiLayerStorageTypeDef",
    "PaginatorConfigTypeDef",
    "PipelineExecutionStateDetailsTypeDef",
    "PipelineExecutionStatusTypeDef",
    "PipelineExecutionSummaryTypeDef",
    "PipelineSummaryTypeDef",
    "PortalResourceTypeDef",
    "PortalStatusTypeDef",
    "PortalSummaryTypeDef",
    "PortalTypeEntryOutputTypeDef",
    "PortalTypeEntryTypeDef",
    "PortalTypeEntryUnionTypeDef",
    "ProcessingInputOutputTypeDef",
    "ProcessingInputTypeDef",
    "ProcessingInputUnionTypeDef",
    "ProjectResourceTypeDef",
    "ProjectSummaryTypeDef",
    "PropertyMappingConfigurationTypeDef",
    "PropertyMappingTypeDef",
    "PropertyNotificationTypeDef",
    "PropertyTypeDef",
    "PropertyTypeOutputTypeDef",
    "PropertyTypeTypeDef",
    "PropertyTypeUnionTypeDef",
    "PropertyValueNullValueTypeDef",
    "PutAssetModelInterfaceRelationshipRequestTypeDef",
    "PutAssetModelInterfaceRelationshipResponseTypeDef",
    "PutAssetPropertyValueEntryTypeDef",
    "PutDefaultEncryptionConfigurationRequestTypeDef",
    "PutDefaultEncryptionConfigurationResponseTypeDef",
    "PutLoggingOptionsRequestTypeDef",
    "PutStorageConfigurationRequestTypeDef",
    "PutStorageConfigurationResponseTypeDef",
    "QueryStatisticsTypeDef",
    "QuerySummaryTypeDef",
    "ReferenceTypeDef",
    "ResolveToTypeDef",
    "ResourceErrorTypeDef",
    "ResourceNotFoundExceptionTypeDef",
    "ResourceStatusTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "ResponseStreamTypeDef",
    "RetentionPeriodTypeDef",
    "RowPaginatorTypeDef",
    "RowTypeDef",
    "S3AccessPointSourceTypeDef",
    "SearchFiltersTypeDef",
    "SearchResultTypeDef",
    "SearchSummaryTypeDef",
    "SessionConfigTypeDef",
    "SiemensIETypeDef",
    "SourceDetailTypeDef",
    "SourceTypeDef",
    "StartPipelineExecutionRequestTypeDef",
    "StartPipelineExecutionResponseTypeDef",
    "StartQueryRequestTypeDef",
    "StartQueryResponseTypeDef",
    "StartSearchRequestTypeDef",
    "StartSearchResponseTypeDef",
    "TagResourceRequestTypeDef",
    "TargetResourceTypeDef",
    "TaskConfigurationOutputTypeDef",
    "TaskConfigurationTypeDef",
    "TaskConfigurationUnionTypeDef",
    "TaskSummaryTypeDef",
    "ThrottlingExceptionTypeDef",
    "TimeInNanosTypeDef",
    "TimeIntervalTypeDef",
    "TimeSeriesSummaryTypeDef",
    "TimeseriesItemTypeDef",
    "TimestampTypeDef",
    "TraceTypeDef",
    "TransformOutputTypeDef",
    "TransformProcessingConfigTypeDef",
    "TransformTypeDef",
    "TransformUnionTypeDef",
    "TrimSettingsTypeDef",
    "TumblingWindowTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAccessPolicyRequestTypeDef",
    "UpdateAssetModelCompositeModelRequestTypeDef",
    "UpdateAssetModelCompositeModelResponseTypeDef",
    "UpdateAssetModelRequestTypeDef",
    "UpdateAssetModelResponseTypeDef",
    "UpdateAssetPropertyRequestTypeDef",
    "UpdateAssetRequestTypeDef",
    "UpdateAssetResponseTypeDef",
    "UpdateComputationModelRequestTypeDef",
    "UpdateComputationModelResponseTypeDef",
    "UpdateDashboardRequestTypeDef",
    "UpdateDatasetRequestTypeDef",
    "UpdateDatasetResponseTypeDef",
    "UpdateGatewayCapabilityConfigurationRequestTypeDef",
    "UpdateGatewayCapabilityConfigurationResponseTypeDef",
    "UpdateGatewayRequestTypeDef",
    "UpdatePipelineRequestTypeDef",
    "UpdatePipelineResponseTypeDef",
    "UpdatePortalRequestTypeDef",
    "UpdatePortalResponseTypeDef",
    "UpdateProjectRequestTypeDef",
    "UpdateTaskRequestTypeDef",
    "UpdateTaskResponseTypeDef",
    "UpdateWorkspaceRequestTypeDef",
    "UpdateWorkspaceResponseTypeDef",
    "UserIdentityTypeDef",
    "VariableValueOutputTypeDef",
    "VariableValueTypeDef",
    "VariableValueUnionTypeDef",
    "VariantTypeDef",
    "WaiterConfigTypeDef",
    "WarmTierRetentionPeriodTypeDef",
    "WorkspaceEncryptionConfigurationInfoTypeDef",
    "WorkspaceEncryptionConfigurationTypeDef",
    "WorkspaceErrorDetailsTypeDef",
    "WorkspaceStatusTypeDef",
    "WorkspaceSummaryTypeDef",
)

class AccessDeniedExceptionTypeDef(TypedDict):
    message: NotRequired[str]

class ActionDefinitionTypeDef(TypedDict):
    actionDefinitionId: str
    actionName: str
    actionType: str

class ActionPayloadTypeDef(TypedDict):
    stringValue: str

class ResolveToTypeDef(TypedDict):
    assetId: str

class TargetResourceTypeDef(TypedDict):
    assetId: NotRequired[str]
    computationModelId: NotRequired[str]

AggregatesTypeDef = TypedDict(
    "AggregatesTypeDef",
    {
        "average": NotRequired[float],
        "count": NotRequired[float],
        "maximum": NotRequired[float],
        "minimum": NotRequired[float],
        "sum": NotRequired[float],
        "standardDeviation": NotRequired[float],
    },
)

class AlarmsTypeDef(TypedDict):
    alarmRoleArn: str
    notificationLambdaArn: NotRequired[str]

ApplicationSummaryTypeDef = TypedDict(
    "ApplicationSummaryTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "status": ApplicationStatusType,
        "createdAt": datetime,
        "workspaceName": str,
    },
)

class AssetBindingValueFilterTypeDef(TypedDict):
    assetId: str

AssetCompositeModelPathSegmentTypeDef = TypedDict(
    "AssetCompositeModelPathSegmentTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)

class AssetErrorDetailsTypeDef(TypedDict):
    assetId: str
    code: Literal["INTERNAL_FAILURE"]
    message: str

class AssetHierarchyInfoTypeDef(TypedDict):
    parentAssetId: NotRequired[str]
    childAssetId: NotRequired[str]

AssetHierarchyTypeDef = TypedDict(
    "AssetHierarchyTypeDef",
    {
        "name": str,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)

class AssetModelBindingValueFilterTypeDef(TypedDict):
    assetModelId: str

AssetModelCompositeModelPathSegmentTypeDef = TypedDict(
    "AssetModelCompositeModelPathSegmentTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)
AssetModelHierarchyDefinitionTypeDef = TypedDict(
    "AssetModelHierarchyDefinitionTypeDef",
    {
        "name": str,
        "childAssetModelId": str,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)
AssetModelHierarchyTypeDef = TypedDict(
    "AssetModelHierarchyTypeDef",
    {
        "name": str,
        "childAssetModelId": str,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)

class AssetModelPropertyBindingValueFilterTypeDef(TypedDict):
    assetModelId: str
    propertyId: str

class AssetModelPropertyBindingValueTypeDef(TypedDict):
    assetModelId: str
    propertyId: str

AssetModelPropertyPathSegmentTypeDef = TypedDict(
    "AssetModelPropertyPathSegmentTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)

class InterfaceSummaryTypeDef(TypedDict):
    interfaceAssetModelId: str
    interfaceAssetModelPropertyId: str

class AssetPropertyBindingValueFilterTypeDef(TypedDict):
    assetId: str
    propertyId: str

class AssetPropertyBindingValueTypeDef(TypedDict):
    assetId: str
    propertyId: str

AssetPropertyPathSegmentTypeDef = TypedDict(
    "AssetPropertyPathSegmentTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)

class PropertyNotificationTypeDef(TypedDict):
    topic: str
    state: PropertyNotificationStateType

class TimeInNanosTypeDef(TypedDict):
    timeInSeconds: int
    offsetInNanos: NotRequired[int]

class AssociateAssetsRequestTypeDef(TypedDict):
    assetId: str
    hierarchyId: str
    childAssetId: str
    clientToken: NotRequired[str]

class AssociateTimeSeriesToAssetPropertyRequestTypeDef(TypedDict):
    alias: str
    assetId: str
    propertyId: str
    clientToken: NotRequired[str]

class AttributeTypeDef(TypedDict):
    defaultValue: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BatchAssociateProjectAssetsRequestTypeDef(TypedDict):
    projectId: str
    assetIds: Sequence[str]
    clientToken: NotRequired[str]

class BatchDisassociateProjectAssetsRequestTypeDef(TypedDict):
    projectId: str
    assetIds: Sequence[str]
    clientToken: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class BatchGetAssetPropertyAggregatesErrorEntryTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyAggregatesErrorCodeType
    errorMessage: str
    entryId: str

class BatchGetAssetPropertyAggregatesErrorInfoTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyAggregatesErrorCodeType
    errorTimestamp: datetime

class BatchGetAssetPropertyValueEntryTypeDef(TypedDict):
    entryId: str
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]

class BatchGetAssetPropertyValueErrorEntryTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyValueErrorCodeType
    errorMessage: str
    entryId: str

class BatchGetAssetPropertyValueErrorInfoTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyValueErrorCodeType
    errorTimestamp: datetime

class BatchGetAssetPropertyValueHistoryErrorEntryTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyValueHistoryErrorCodeType
    errorMessage: str
    entryId: str

class BatchGetAssetPropertyValueHistoryErrorInfoTypeDef(TypedDict):
    errorCode: BatchGetAssetPropertyValueHistoryErrorCodeType
    errorTimestamp: datetime

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CancelEnrichmentJobRequestTypeDef(TypedDict):
    workspaceName: str
    jobId: str

class CancelPipelineExecutionRequestTypeDef(TypedDict):
    workspaceName: str
    pipelineName: str
    pipelineExecutionId: str
    reason: NotRequired[str]

class CancelQueryRequestTypeDef(TypedDict):
    workspaceName: str
    queryId: str

class ContentTypeDef(TypedDict):
    text: NotRequired[str]

class ColumnTypeTypeDef(TypedDict):
    scalarType: NotRequired[ScalarTypeType]

ColumnInformationTypeDef = TypedDict(
    "ColumnInformationTypeDef",
    {
        "name": str,
        "type": str,
    },
)
CompositionRelationshipItemTypeDef = TypedDict(
    "CompositionRelationshipItemTypeDef",
    {
        "id": NotRequired[str],
    },
)

class CompositionRelationshipSummaryTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelId: str
    assetModelCompositeModelType: str

class ComputationModelAnomalyDetectionConfigurationTypeDef(TypedDict):
    inputProperties: str
    resultProperty: str

class DetailedPipelineErrorTypeDef(TypedDict):
    code: DetailedPipelineErrorCodeType
    message: str

class ComputeNodeOutputTypeDef(TypedDict):
    computeNodeName: str
    taskName: str
    environmentVariables: NotRequired[dict[str, str]]
    dependsOn: NotRequired[list[str]]

class ComputeNodeTypeDef(TypedDict):
    computeNodeName: str
    taskName: str
    environmentVariables: NotRequired[Mapping[str, str]]
    dependsOn: NotRequired[Sequence[str]]

class ConfigurationErrorDetailsTypeDef(TypedDict):
    code: ErrorCodeType
    message: str

class ConflictingOperationExceptionTypeDef(TypedDict):
    message: str
    resourceId: str
    resourceArn: str

class EphemeralStorageConfigurationTypeDef(TypedDict):
    storageClass: StorageClassType
    storageSizeInGiB: int

class CreateApplicationRequestTypeDef(TypedDict):
    idcInstanceArn: str
    workspaceName: str
    name: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateAssetRequestTypeDef(TypedDict):
    assetName: str
    assetModelId: str
    assetId: NotRequired[str]
    assetExternalId: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    assetDescription: NotRequired[str]

class ErrorReportLocationTypeDef(TypedDict):
    bucket: str
    prefix: str

class CreateDashboardRequestTypeDef(TypedDict):
    projectId: str
    dashboardName: str
    dashboardDefinition: str
    dashboardDescription: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class ExportErrorReportLocationTypeDef(TypedDict):
    s3Uri: str

class CreateProjectRequestTypeDef(TypedDict):
    portalId: str
    projectName: str
    projectDescription: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class WorkspaceEncryptionConfigurationTypeDef(TypedDict):
    encryptionType: EncryptionTypeType
    kmsKeyId: NotRequired[str]

class CsvOutputTypeDef(TypedDict):
    columnNames: list[ColumnNameType]

class CsvTypeDef(TypedDict):
    columnNames: Sequence[ColumnNameType]

class CustomerManagedS3StorageTypeDef(TypedDict):
    s3ResourceArn: str
    roleArn: str

DashboardSummaryTypeDef = TypedDict(
    "DashboardSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "description": NotRequired[str],
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
    },
)

class DataSegmentEnrichmentTypeDef(TypedDict):
    status: EnrichmentStatusType
    lastEnrichedAt: NotRequired[datetime]

class DatasetEnrichmentEntryTypeDef(TypedDict):
    status: DatasetEnrichmentStatusType
    lastEnrichedAt: NotRequired[datetime]

class DatumPaginatorTypeDef(TypedDict):
    scalarValue: NotRequired[str]
    arrayValue: NotRequired[list[dict[str, Any]]]
    rowValue: NotRequired[dict[str, Any]]
    nullValue: NotRequired[bool]

class DatumTypeDef(TypedDict):
    scalarValue: NotRequired[str]
    arrayValue: NotRequired[list[dict[str, Any]]]
    rowValue: NotRequired[dict[str, Any]]
    nullValue: NotRequired[bool]

class DeleteAccessPolicyRequestTypeDef(TypedDict):
    accessPolicyId: str
    clientToken: NotRequired[str]

DeleteApplicationRequestTypeDef = TypedDict(
    "DeleteApplicationRequestTypeDef",
    {
        "workspaceName": str,
        "id": str,
    },
)

class DeleteAssetModelCompositeModelRequestTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelId: str
    clientToken: NotRequired[str]
    ifMatch: NotRequired[str]
    ifNoneMatch: NotRequired[str]
    matchForVersionType: NotRequired[AssetModelVersionTypeType]

class DeleteAssetModelInterfaceRelationshipRequestTypeDef(TypedDict):
    assetModelId: str
    interfaceAssetModelId: str
    clientToken: NotRequired[str]

class DeleteAssetModelRequestTypeDef(TypedDict):
    assetModelId: str
    clientToken: NotRequired[str]
    ifMatch: NotRequired[str]
    ifNoneMatch: NotRequired[str]
    matchForVersionType: NotRequired[AssetModelVersionTypeType]

class DeleteAssetRequestTypeDef(TypedDict):
    assetId: str
    clientToken: NotRequired[str]

class DeleteComputationModelRequestTypeDef(TypedDict):
    computationModelId: str
    clientToken: NotRequired[str]

class DeleteDashboardRequestTypeDef(TypedDict):
    dashboardId: str
    clientToken: NotRequired[str]

class DeleteDatasetRequestTypeDef(TypedDict):
    datasetId: str
    workspaceName: NotRequired[str]
    clientToken: NotRequired[str]

class DeleteGatewayRequestTypeDef(TypedDict):
    gatewayId: str

class DeletePipelineRequestTypeDef(TypedDict):
    workspaceName: str
    pipelineName: str

class DeletePortalRequestTypeDef(TypedDict):
    portalId: str
    clientToken: NotRequired[str]

class DeleteProjectRequestTypeDef(TypedDict):
    projectId: str
    clientToken: NotRequired[str]

class DeleteTaskRequestTypeDef(TypedDict):
    workspaceName: str
    taskName: str

class DeleteTimeSeriesRequestTypeDef(TypedDict):
    alias: NotRequired[str]
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    clientToken: NotRequired[str]
    workspaceName: NotRequired[str]

class DeleteWorkspaceRequestTypeDef(TypedDict):
    workspaceName: str
    clientToken: NotRequired[str]

class DescribeAccessPolicyRequestTypeDef(TypedDict):
    accessPolicyId: str

class DescribeActionRequestTypeDef(TypedDict):
    actionId: str

DescribeApplicationRequestTypeDef = TypedDict(
    "DescribeApplicationRequestTypeDef",
    {
        "workspaceName": str,
        "id": str,
    },
)

class DescribeAssetCompositeModelRequestTypeDef(TypedDict):
    assetId: str
    assetCompositeModelId: str

class DescribeAssetModelCompositeModelRequestTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelId: str
    assetModelVersion: NotRequired[str]

class DescribeAssetModelInterfaceRelationshipRequestTypeDef(TypedDict):
    assetModelId: str
    interfaceAssetModelId: str

class HierarchyMappingTypeDef(TypedDict):
    assetModelHierarchyId: str
    interfaceAssetModelHierarchyId: str

class PropertyMappingTypeDef(TypedDict):
    assetModelPropertyId: str
    interfaceAssetModelPropertyId: str

class DescribeAssetModelRequestTypeDef(TypedDict):
    assetModelId: str
    excludeProperties: NotRequired[bool]
    assetModelVersion: NotRequired[str]

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

InterfaceRelationshipTypeDef = TypedDict(
    "InterfaceRelationshipTypeDef",
    {
        "id": str,
    },
)

class DescribeAssetPropertyRequestTypeDef(TypedDict):
    assetId: str
    propertyId: str

class DescribeAssetRequestTypeDef(TypedDict):
    assetId: str
    excludeProperties: NotRequired[bool]

class DescribeBulkImportJobRequestTypeDef(TypedDict):
    jobId: str
    workspaceName: NotRequired[str]

class DescribeComputationModelExecutionSummaryRequestTypeDef(TypedDict):
    computationModelId: str
    resolveToResourceType: NotRequired[Literal["ASSET"]]
    resolveToResourceId: NotRequired[str]

class DescribeComputationModelRequestTypeDef(TypedDict):
    computationModelId: str
    computationModelVersion: NotRequired[str]

class DescribeDashboardRequestTypeDef(TypedDict):
    dashboardId: str

class DescribeDatasetExportJobRequestTypeDef(TypedDict):
    workspaceName: str
    jobId: str

class DescribeDatasetRequestTypeDef(TypedDict):
    datasetId: str
    workspaceName: NotRequired[str]
    datasetVersion: NotRequired[str]

class DescribeEnrichmentJobRequestTypeDef(TypedDict):
    workspaceName: str
    jobId: str

class DescribeExecutionRequestTypeDef(TypedDict):
    executionId: str

class ExecutionStatusTypeDef(TypedDict):
    state: ExecutionStateType

class DescribeGatewayCapabilityConfigurationRequestTypeDef(TypedDict):
    gatewayId: str
    capabilityNamespace: str

class DescribeGatewayRequestTypeDef(TypedDict):
    gatewayId: str

class GatewayCapabilitySummaryTypeDef(TypedDict):
    capabilityNamespace: str
    capabilitySyncStatus: CapabilitySyncStatusType

class DescribeLoggingOptionsRequestTypeDef(TypedDict):
    workspaceName: NotRequired[str]

class LoggingOptionsTypeDef(TypedDict):
    level: LoggingLevelType

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribePipelineExecutionRequestTypeDef(TypedDict):
    workspaceName: str
    pipelineName: str
    pipelineExecutionId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

ExecutionEnvironmentVariablesOutputTypeDef = TypedDict(
    "ExecutionEnvironmentVariablesOutputTypeDef",
    {
        "global": NotRequired[dict[str, str]],
        "computeNodes": NotRequired[dict[str, dict[str, str]]],
    },
)

class DescribePipelineRequestTypeDef(TypedDict):
    workspaceName: str
    pipelineName: str
    pipelineVersion: NotRequired[str]

class DescribePortalRequestTypeDef(TypedDict):
    portalId: str

ImageLocationTypeDef = TypedDict(
    "ImageLocationTypeDef",
    {
        "id": str,
        "url": str,
    },
)

class PortalTypeEntryOutputTypeDef(TypedDict):
    portalTools: NotRequired[list[str]]

class DescribeProjectRequestTypeDef(TypedDict):
    projectId: str

class DescribeQueryRequestTypeDef(TypedDict):
    workspaceName: str
    queryId: str

class QueryStatisticsTypeDef(TypedDict):
    rowCount: int
    bytesScanned: int
    executionTimeInMillis: int

class DescribeSearchRequestTypeDef(TypedDict):
    workspaceName: str
    searchId: str

class RetentionPeriodTypeDef(TypedDict):
    numberOfDays: NotRequired[int]
    unlimited: NotRequired[bool]

class WarmTierRetentionPeriodTypeDef(TypedDict):
    numberOfDays: NotRequired[int]
    unlimited: NotRequired[bool]

class DescribeTaskRequestTypeDef(TypedDict):
    workspaceName: str
    taskName: str
    taskVersion: NotRequired[str]

class DescribeTimeSeriesRequestTypeDef(TypedDict):
    alias: NotRequired[str]
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    workspaceName: NotRequired[str]

class DescribeWorkspaceRequestTypeDef(TypedDict):
    workspaceName: str

class WorkspaceEncryptionConfigurationInfoTypeDef(TypedDict):
    encryptionType: EncryptionTypeType
    kmsKeyArn: NotRequired[str]

class DetailedErrorTypeDef(TypedDict):
    code: DetailedErrorCodeType
    message: str

class DisassociateAssetsRequestTypeDef(TypedDict):
    assetId: str
    hierarchyId: str
    childAssetId: str
    clientToken: NotRequired[str]

class DisassociateTimeSeriesFromAssetPropertyRequestTypeDef(TypedDict):
    alias: str
    assetId: str
    propertyId: str
    clientToken: NotRequired[str]

class EnrichmentJobSummaryTypeDef(TypedDict):
    jobId: str
    status: EnrichmentJobStatusType
    workspaceName: str
    jobType: Literal["EVENT_DETECTION"]
    datasetId: str
    createdAt: datetime
    propertyAlias: NotRequired[str]
    timeSeriesId: NotRequired[str]
    updatedAt: NotRequired[datetime]

class ExecuteQueryRequestTypeDef(TypedDict):
    queryStatement: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    clientToken: NotRequired[str]

ExecutionEnvironmentVariablesTypeDef = TypedDict(
    "ExecutionEnvironmentVariablesTypeDef",
    {
        "global": NotRequired[Mapping[str, str]],
        "computeNodes": NotRequired[Mapping[str, Mapping[str, str]]],
    },
)

class ExportJobSummaryTypeDef(TypedDict):
    jobId: str
    status: DatasetExportJobStatusType
    startedAt: datetime
    destinationS3Uri: str
    completedAt: NotRequired[datetime]

class FormatSettingsTypeDef(TypedDict):
    framesPerSecond: NotRequired[int]
    widthInPixels: NotRequired[int]
    heightInPixels: NotRequired[int]

class ForwardingConfigTypeDef(TypedDict):
    state: ForwardingConfigStateType

class GreengrassTypeDef(TypedDict):
    groupArn: str

class GreengrassV2TypeDef(TypedDict):
    coreDeviceThingName: str
    coreDeviceOperatingSystem: NotRequired[CoreDeviceOperatingSystemType]

class SiemensIETypeDef(TypedDict):
    iotCoreThingName: str

class GetAssetPropertyValueRequestTypeDef(TypedDict):
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]

GetInterpolatedAssetPropertyValuesRequestTypeDef = TypedDict(
    "GetInterpolatedAssetPropertyValuesRequestTypeDef",
    {
        "startTimeInSeconds": int,
        "endTimeInSeconds": int,
        "quality": QualityType,
        "intervalInSeconds": int,
        "type": str,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "startTimeOffsetInNanos": NotRequired[int],
        "endTimeOffsetInNanos": NotRequired[int],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "intervalWindowInSeconds": NotRequired[int],
    },
)

class GetQueryResultsRequestTypeDef(TypedDict):
    workspaceName: str
    queryId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class GetSearchResultsRequestTypeDef(TypedDict):
    searchId: str
    workspaceName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

GroupIdentityTypeDef = TypedDict(
    "GroupIdentityTypeDef",
    {
        "id": str,
    },
)

class IAMRoleIdentityTypeDef(TypedDict):
    arn: str

class IAMUserIdentityTypeDef(TypedDict):
    arn: str

UserIdentityTypeDef = TypedDict(
    "UserIdentityTypeDef",
    {
        "id": str,
    },
)
InterfaceRelationshipSummaryTypeDef = TypedDict(
    "InterfaceRelationshipSummaryTypeDef",
    {
        "id": str,
    },
)

class InternalFailureExceptionTypeDef(TypedDict):
    message: str

class InvalidRequestExceptionTypeDef(TypedDict):
    message: str

class InvokeAssistantRequestTypeDef(TypedDict):
    message: str
    conversationId: NotRequired[str]
    enableTrace: NotRequired[bool]

JobSummaryTypeDef = TypedDict(
    "JobSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "status": JobStatusType,
    },
)

class KendraSourceDetailTypeDef(TypedDict):
    knowledgeBaseArn: str
    roleArn: str

class LimitExceededExceptionTypeDef(TypedDict):
    message: str

class ListAccessPoliciesRequestTypeDef(TypedDict):
    identityType: NotRequired[IdentityTypeType]
    identityId: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    resourceId: NotRequired[str]
    iamArn: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListActionsRequestTypeDef(TypedDict):
    targetResourceType: TargetResourceTypeType
    targetResourceId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    resolveToResourceType: NotRequired[Literal["ASSET"]]
    resolveToResourceId: NotRequired[str]

class ListApplicationsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAssetModelCompositeModelsRequestTypeDef(TypedDict):
    assetModelId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    assetModelVersion: NotRequired[str]

ListAssetModelPropertiesRequestTypeDef = TypedDict(
    "ListAssetModelPropertiesRequestTypeDef",
    {
        "assetModelId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[ListAssetModelPropertiesFilterType],
        "assetModelVersion": NotRequired[str],
    },
)

class ListAssetModelsRequestTypeDef(TypedDict):
    assetModelTypes: NotRequired[Sequence[AssetModelTypeType]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    assetModelVersion: NotRequired[str]

ListAssetPropertiesRequestTypeDef = TypedDict(
    "ListAssetPropertiesRequestTypeDef",
    {
        "assetId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[ListAssetPropertiesFilterType],
    },
)

class ListAssetRelationshipsRequestTypeDef(TypedDict):
    assetId: str
    traversalType: Literal["PATH_TO_ROOT"]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

ListAssetsRequestTypeDef = TypedDict(
    "ListAssetsRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "assetModelId": NotRequired[str],
        "filter": NotRequired[ListAssetsFilterType],
    },
)

class ListAssociatedAssetsRequestTypeDef(TypedDict):
    assetId: str
    hierarchyId: NotRequired[str]
    traversalDirection: NotRequired[TraversalDirectionType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

ListBulkImportJobsRequestTypeDef = TypedDict(
    "ListBulkImportJobsRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[ListBulkImportJobsFilterType],
        "workspaceName": NotRequired[str],
    },
)

class ListCompositionRelationshipsRequestTypeDef(TypedDict):
    assetModelId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListComputationModelResolveToResourcesRequestTypeDef(TypedDict):
    computationModelId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListComputationModelsRequestTypeDef(TypedDict):
    computationModelType: NotRequired[Literal["ANOMALY_DETECTION"]]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDashboardsRequestTypeDef(TypedDict):
    projectId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListDatasetDataSegmentRelationshipsRequestTypeDef(TypedDict):
    datasetId: str
    workspaceName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDatasetDataSegmentsRequestTypeDef(TypedDict):
    datasetId: str
    workspaceName: str
    datasetVersion: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

ListDatasetExportJobsRequestTypeDef = TypedDict(
    "ListDatasetExportJobsRequestTypeDef",
    {
        "workspaceName": str,
        "filter": NotRequired[DatasetExportJobFilterType],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

class ListDatasetsRequestTypeDef(TypedDict):
    sourceType: DatasetSourceTypeType
    workspaceName: NotRequired[str]
    datasetType: NotRequired[DatasetTypeEnumType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListExecutionsRequestTypeDef(TypedDict):
    targetResourceType: TargetResourceTypeType
    targetResourceId: str
    resolveToResourceType: NotRequired[Literal["ASSET"]]
    resolveToResourceId: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    actionType: NotRequired[str]

class ListGatewaysRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListInterfaceRelationshipsRequestTypeDef(TypedDict):
    interfaceAssetModelId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListPipelinesRequestTypeDef(TypedDict):
    workspaceName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListPortalsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListProjectAssetsRequestTypeDef(TypedDict):
    projectId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListProjectsRequestTypeDef(TypedDict):
    portalId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "description": NotRequired[str],
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
    },
)
ListQueriesRequestTypeDef = TypedDict(
    "ListQueriesRequestTypeDef",
    {
        "workspaceName": str,
        "filter": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

class QuerySummaryTypeDef(TypedDict):
    queryId: str
    status: QueryStatusType
    submittedAt: datetime
    completedAt: NotRequired[datetime]

class SearchSummaryTypeDef(TypedDict):
    searchId: str
    workspaceName: str
    status: SearchStatusType
    queryStatement: str
    searchType: SearchTypeType
    statusReason: NotRequired[str]
    startedAt: NotRequired[datetime]
    groupId: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class ListTasksRequestTypeDef(TypedDict):
    workspaceName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListTimeSeriesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    assetId: NotRequired[str]
    aliasPrefix: NotRequired[str]
    timeSeriesType: NotRequired[ListTimeSeriesTypeType]
    workspaceName: NotRequired[str]

class TimeSeriesSummaryTypeDef(TypedDict):
    timeSeriesId: str
    dataType: PropertyDataTypeType
    timeSeriesCreationDate: datetime
    timeSeriesLastUpdateDate: datetime
    timeSeriesArn: str
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    alias: NotRequired[str]
    dataTypeSpec: NotRequired[str]

class ListWorkspacesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class LocationTypeDef(TypedDict):
    uri: NotRequired[str]

class MetricProcessingConfigTypeDef(TypedDict):
    computeLocation: ComputeLocationType

class TumblingWindowTypeDef(TypedDict):
    interval: str
    offset: NotRequired[str]

class MonitorErrorDetailsTypeDef(TypedDict):
    code: NotRequired[MonitorErrorCodeType]
    message: NotRequired[str]

class S3AccessPointSourceTypeDef(TypedDict):
    accessPointArn: str
    prefix: NotRequired[str]

PortalResourceTypeDef = TypedDict(
    "PortalResourceTypeDef",
    {
        "id": str,
    },
)

class PortalTypeEntryTypeDef(TypedDict):
    portalTools: NotRequired[Sequence[str]]

ProjectResourceTypeDef = TypedDict(
    "ProjectResourceTypeDef",
    {
        "id": str,
    },
)

class PropertyValueNullValueTypeDef(TypedDict):
    valueType: RawValueTypeType

class PutDefaultEncryptionConfigurationRequestTypeDef(TypedDict):
    encryptionType: EncryptionTypeType
    kmsKeyId: NotRequired[str]

class ResourceErrorTypeDef(TypedDict):
    code: NotRequired[ResourceErrorCodeType]
    message: NotRequired[str]

class ResourceNotFoundExceptionTypeDef(TypedDict):
    message: str

class ThrottlingExceptionTypeDef(TypedDict):
    message: str

class TraceTypeDef(TypedDict):
    text: NotRequired[str]

class StartQueryRequestTypeDef(TypedDict):
    workspaceName: str
    queryStatement: str
    clientToken: NotRequired[str]

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateAssetPropertyRequestTypeDef(TypedDict):
    assetId: str
    propertyId: str
    propertyAlias: NotRequired[str]
    propertyNotificationState: NotRequired[PropertyNotificationStateType]
    clientToken: NotRequired[str]
    propertyUnit: NotRequired[str]

class UpdateAssetRequestTypeDef(TypedDict):
    assetId: str
    assetName: str
    assetExternalId: NotRequired[str]
    clientToken: NotRequired[str]
    assetDescription: NotRequired[str]

class UpdateDashboardRequestTypeDef(TypedDict):
    dashboardId: str
    dashboardName: str
    dashboardDefinition: str
    dashboardDescription: NotRequired[str]
    clientToken: NotRequired[str]

class UpdateGatewayCapabilityConfigurationRequestTypeDef(TypedDict):
    gatewayId: str
    capabilityNamespace: str
    capabilityConfiguration: str

class UpdateGatewayRequestTypeDef(TypedDict):
    gatewayId: str
    gatewayName: str

class UpdateProjectRequestTypeDef(TypedDict):
    projectId: str
    projectName: str
    projectDescription: NotRequired[str]
    clientToken: NotRequired[str]

class WorkspaceErrorDetailsTypeDef(TypedDict):
    code: ErrorCodeType
    message: str

class ComputationModelResolveToResourceSummaryTypeDef(TypedDict):
    resolveTo: NotRequired[ResolveToTypeDef]

class ActionSummaryTypeDef(TypedDict):
    actionId: NotRequired[str]
    actionDefinitionId: NotRequired[str]
    targetResource: NotRequired[TargetResourceTypeDef]
    resolveTo: NotRequired[ResolveToTypeDef]

class ExecuteActionRequestTypeDef(TypedDict):
    targetResource: TargetResourceTypeDef
    actionDefinitionId: str
    actionPayload: ActionPayloadTypeDef
    clientToken: NotRequired[str]
    resolveTo: NotRequired[ResolveToTypeDef]

class AggregatedValueTypeDef(TypedDict):
    timestamp: datetime
    value: AggregatesTypeDef
    quality: NotRequired[QualityType]

AssetCompositeModelSummaryTypeDef = TypedDict(
    "AssetCompositeModelSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "type": str,
        "description": str,
        "path": list[AssetCompositeModelPathSegmentTypeDef],
        "externalId": NotRequired[str],
    },
)

class AssetRelationshipSummaryTypeDef(TypedDict):
    relationshipType: Literal["HIERARCHY"]
    hierarchyInfo: NotRequired[AssetHierarchyInfoTypeDef]

AssetModelCompositeModelSummaryTypeDef = TypedDict(
    "AssetModelCompositeModelSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "type": str,
        "externalId": NotRequired[str],
        "description": NotRequired[str],
        "path": NotRequired[list[AssetModelCompositeModelPathSegmentTypeDef]],
    },
)

class VariableValueOutputTypeDef(TypedDict):
    propertyId: NotRequired[str]
    hierarchyId: NotRequired[str]
    propertyPath: NotRequired[list[AssetModelPropertyPathSegmentTypeDef]]

class VariableValueTypeDef(TypedDict):
    propertyId: NotRequired[str]
    hierarchyId: NotRequired[str]
    propertyPath: NotRequired[Sequence[AssetModelPropertyPathSegmentTypeDef]]

class DataBindingValueFilterTypeDef(TypedDict):
    asset: NotRequired[AssetBindingValueFilterTypeDef]
    assetModel: NotRequired[AssetModelBindingValueFilterTypeDef]
    assetProperty: NotRequired[AssetPropertyBindingValueFilterTypeDef]
    assetModelProperty: NotRequired[AssetModelPropertyBindingValueFilterTypeDef]

ComputationModelDataBindingValueOutputTypeDef = TypedDict(
    "ComputationModelDataBindingValueOutputTypeDef",
    {
        "assetModelProperty": NotRequired[AssetModelPropertyBindingValueTypeDef],
        "assetProperty": NotRequired[AssetPropertyBindingValueTypeDef],
        "list": NotRequired[list[dict[str, Any]]],
    },
)
ComputationModelDataBindingValueTypeDef = TypedDict(
    "ComputationModelDataBindingValueTypeDef",
    {
        "assetModelProperty": NotRequired[AssetModelPropertyBindingValueTypeDef],
        "assetProperty": NotRequired[AssetPropertyBindingValueTypeDef],
        "list": NotRequired[Sequence[Mapping[str, Any]]],
    },
)

class DataBindingValueTypeDef(TypedDict):
    assetModelProperty: NotRequired[AssetModelPropertyBindingValueTypeDef]
    assetProperty: NotRequired[AssetPropertyBindingValueTypeDef]

AssetPropertySummaryTypeDef = TypedDict(
    "AssetPropertySummaryTypeDef",
    {
        "id": str,
        "externalId": NotRequired[str],
        "alias": NotRequired[str],
        "unit": NotRequired[str],
        "notification": NotRequired[PropertyNotificationTypeDef],
        "assetCompositeModelId": NotRequired[str],
        "path": NotRequired[list[AssetPropertyPathSegmentTypeDef]],
    },
)
AssetPropertyTypeDef = TypedDict(
    "AssetPropertyTypeDef",
    {
        "id": str,
        "name": str,
        "dataType": PropertyDataTypeType,
        "externalId": NotRequired[str],
        "alias": NotRequired[str],
        "notification": NotRequired[PropertyNotificationTypeDef],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
        "path": NotRequired[list[AssetPropertyPathSegmentTypeDef]],
    },
)

class AssociateDataSegmentEntryTypeDef(TypedDict):
    sourceDatasetId: str
    timeSeriesId: str
    startTimestamp: TimeInNanosTypeDef
    endTimestamp: TimeInNanosTypeDef

class BatchPutAssetPropertyErrorTypeDef(TypedDict):
    errorCode: BatchPutAssetPropertyValueErrorCodeType
    errorMessage: str
    timestamps: list[TimeInNanosTypeDef]

class DataSegmentRelationshipSummaryTypeDef(TypedDict):
    targetDatasetId: str
    sourceDatasetId: str
    timeSeriesId: str
    startTimestamp: TimeInNanosTypeDef
    endTimestamp: TimeInNanosTypeDef

class DeleteDataSegmentEntryTypeDef(TypedDict):
    timeSeriesId: str
    startTimestamp: TimeInNanosTypeDef
    endTimestamp: TimeInNanosTypeDef

class DisassociateDataSegmentEntryTypeDef(TypedDict):
    sourceDatasetId: str
    timeSeriesId: str
    startTimestamp: TimeInNanosTypeDef
    endTimestamp: TimeInNanosTypeDef

class EnrichmentTrimSettingsTypeDef(TypedDict):
    startTime: TimeInNanosTypeDef
    endTime: TimeInNanosTypeDef

class FailedDataSegmentAssociationTypeDef(TypedDict):
    sourceDatasetId: str
    timeSeriesId: str
    startTimestamp: TimeInNanosTypeDef
    endTimestamp: TimeInNanosTypeDef
    errorCode: DataSegmentErrorCodeType
    errorMessage: str

class FailedDataSegmentDeletionTypeDef(TypedDict):
    timeSeriesId: str
    startTimestamp: TimeInNanosTypeDef
    endTimestamp: TimeInNanosTypeDef
    errorCode: DataSegmentErrorCodeType
    errorMessage: str

class FailedDataSegmentDisassociationTypeDef(TypedDict):
    sourceDatasetId: str
    timeSeriesId: str
    startTimestamp: TimeInNanosTypeDef
    endTimestamp: TimeInNanosTypeDef
    errorCode: DataSegmentErrorCodeType
    errorMessage: str

class SearchResultTypeDef(TypedDict):
    searchId: str
    workspaceName: str
    datasetId: str
    timeSeriesId: str
    startTimestamp: TimeInNanosTypeDef
    endTimestamp: TimeInNanosTypeDef
    topTimestamp: TimeInNanosTypeDef
    score: float

class SessionConfigTypeDef(TypedDict):
    sessionStartTimestamp: TimeInNanosTypeDef
    sessionEndTimestamp: TimeInNanosTypeDef

class TimeIntervalTypeDef(TypedDict):
    startTime: TimeInNanosTypeDef
    endTime: TimeInNanosTypeDef

class TrimSettingsTypeDef(TypedDict):
    startTime: TimeInNanosTypeDef
    endTime: TimeInNanosTypeDef

class BatchAssociateProjectAssetsResponseTypeDef(TypedDict):
    errors: list[AssetErrorDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDisassociateProjectAssetsResponseTypeDef(TypedDict):
    errors: list[AssetErrorDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CancelEnrichmentJobResponseTypeDef(TypedDict):
    jobId: str
    status: EnrichmentJobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CancelPipelineExecutionResponseTypeDef(TypedDict):
    state: PipelineExecutionStateType
    ResponseMetadata: ResponseMetadataTypeDef

class CancelQueryResponseTypeDef(TypedDict):
    queryId: str
    status: QueryStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAccessPolicyResponseTypeDef(TypedDict):
    accessPolicyId: str
    accessPolicyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "dnsSubdomain": str,
        "name": str,
        "status": ApplicationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateBulkImportJobResponseTypeDef(TypedDict):
    jobId: str
    jobName: str
    jobStatus: JobStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDashboardResponseTypeDef(TypedDict):
    dashboardId: str
    dashboardArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDatasetExportJobResponseTypeDef(TypedDict):
    jobId: str
    workspaceName: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEnrichmentJobResponseTypeDef(TypedDict):
    jobId: str
    status: EnrichmentJobStatusType
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    gatewayArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProjectResponseTypeDef(TypedDict):
    projectId: str
    projectArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeActionResponseTypeDef(TypedDict):
    actionId: str
    targetResource: TargetResourceTypeDef
    actionDefinitionId: str
    actionPayload: ActionPayloadTypeDef
    executionTime: datetime
    resolveTo: ResolveToTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

DescribeApplicationResponseTypeDef = TypedDict(
    "DescribeApplicationResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "dnsSubdomain": str,
        "description": str,
        "id": str,
        "idcApplicationArn": str,
        "name": str,
        "status": ApplicationStatusType,
        "updatedAt": datetime,
        "workspaceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class DescribeComputationModelExecutionSummaryResponseTypeDef(TypedDict):
    computationModelId: str
    resolveTo: ResolveToTypeDef
    computationModelExecutionSummary: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeDashboardResponseTypeDef(TypedDict):
    dashboardId: str
    dashboardArn: str
    dashboardName: str
    projectId: str
    dashboardDescription: str
    dashboardDefinition: str
    dashboardCreationDate: datetime
    dashboardLastUpdateDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeGatewayCapabilityConfigurationResponseTypeDef(TypedDict):
    gatewayId: str
    capabilityNamespace: str
    capabilityConfiguration: str
    capabilitySyncStatus: CapabilitySyncStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeProjectResponseTypeDef(TypedDict):
    projectId: str
    projectArn: str
    projectName: str
    portalId: str
    projectDescription: str
    projectCreationDate: datetime
    projectLastUpdateDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeSearchResponseTypeDef(TypedDict):
    searchId: str
    workspaceName: str
    status: SearchStatusType
    queryStatement: str
    searchType: SearchTypeType
    statusReason: str
    startedAt: datetime
    groupId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeTimeSeriesResponseTypeDef(TypedDict):
    assetId: str
    propertyId: str
    alias: str
    timeSeriesId: str
    dataType: PropertyDataTypeType
    dataTypeSpec: str
    timeSeriesCreationDate: datetime
    timeSeriesLastUpdateDate: datetime
    timeSeriesArn: str
    workspaceName: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ExecuteActionResponseTypeDef(TypedDict):
    actionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetCaptureDataResponseTypeDef(TypedDict):
    data: bytes
    startTime: TimeInNanosTypeDef
    endTime: TimeInNanosTypeDef
    dataType: Literal["VIDEO-MP4"]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListApplicationsResponseTypeDef(TypedDict):
    applications: list[ApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListProjectAssetsResponseTypeDef(TypedDict):
    assetIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartPipelineExecutionResponseTypeDef(TypedDict):
    pipelineExecutionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartQueryResponseTypeDef(TypedDict):
    queryId: str
    status: QueryStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class StartSearchResponseTypeDef(TypedDict):
    searchId: str
    workspaceName: str
    status: SearchStatusType
    groupId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGatewayCapabilityConfigurationResponseTypeDef(TypedDict):
    capabilityNamespace: str
    capabilitySyncStatus: CapabilitySyncStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetAssetPropertyAggregatesEntryTypeDef(TypedDict):
    entryId: str
    aggregateTypes: Sequence[AggregateTypeType]
    resolution: str
    startDate: TimestampTypeDef
    endDate: TimestampTypeDef
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]

class BatchGetAssetPropertyValueHistoryEntryTypeDef(TypedDict):
    entryId: str
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    startDate: NotRequired[TimestampTypeDef]
    endDate: NotRequired[TimestampTypeDef]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]

class GetAssetPropertyAggregatesRequestTypeDef(TypedDict):
    aggregateTypes: Sequence[AggregateTypeType]
    resolution: str
    startDate: TimestampTypeDef
    endDate: TimestampTypeDef
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class GetAssetPropertyValueHistoryRequestTypeDef(TypedDict):
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    startDate: NotRequired[TimestampTypeDef]
    endDate: NotRequired[TimestampTypeDef]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListEnrichmentJobsRequestTypeDef(TypedDict):
    workspaceName: str
    datasetId: NotRequired[str]
    propertyAlias: NotRequired[str]
    timeSeriesId: NotRequired[str]
    status: NotRequired[EnrichmentJobStatusType]
    jobType: NotRequired[Literal["EVENT_DETECTION"]]
    startDate: NotRequired[TimestampTypeDef]
    endDate: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListPipelineExecutionsRequestTypeDef(TypedDict):
    workspaceName: str
    pipelineName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    state: NotRequired[PipelineExecutionStateType]
    startTimeAfter: NotRequired[TimestampTypeDef]
    startTimeBefore: NotRequired[TimestampTypeDef]
    endTimeAfter: NotRequired[TimestampTypeDef]
    endTimeBefore: NotRequired[TimestampTypeDef]

class ListSearchesFiltersTypeDef(TypedDict):
    statusFilter: NotRequired[Sequence[SearchStatusType]]
    startedAfter: NotRequired[TimestampTypeDef]
    startedBefore: NotRequired[TimestampTypeDef]
    groupIdFilter: NotRequired[Sequence[str]]
    searchTypeFilter: NotRequired[Sequence[SearchTypeType]]

class BatchGetAssetPropertyAggregatesSkippedEntryTypeDef(TypedDict):
    entryId: str
    completionStatus: BatchEntryCompletionStatusType
    errorInfo: NotRequired[BatchGetAssetPropertyAggregatesErrorInfoTypeDef]

class BatchGetAssetPropertyValueRequestTypeDef(TypedDict):
    entries: Sequence[BatchGetAssetPropertyValueEntryTypeDef]
    nextToken: NotRequired[str]

class BatchGetAssetPropertyValueSkippedEntryTypeDef(TypedDict):
    entryId: str
    completionStatus: BatchEntryCompletionStatusType
    errorInfo: NotRequired[BatchGetAssetPropertyValueErrorInfoTypeDef]

class BatchGetAssetPropertyValueHistorySkippedEntryTypeDef(TypedDict):
    entryId: str
    completionStatus: BatchEntryCompletionStatusType
    errorInfo: NotRequired[BatchGetAssetPropertyValueHistoryErrorInfoTypeDef]

ImageFileTypeDef = TypedDict(
    "ImageFileTypeDef",
    {
        "data": BlobTypeDef,
        "type": Literal["PNG"],
    },
)
ColumnInfoTypeDef = TypedDict(
    "ColumnInfoTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[ColumnTypeTypeDef],
    },
)

class GetQueryResultsResponseTypeDef(TypedDict):
    columnInfo: list[ColumnInformationTypeDef]
    rows: list[list[str]]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CompositionDetailsTypeDef(TypedDict):
    compositionRelationship: NotRequired[list[CompositionRelationshipItemTypeDef]]

class ListCompositionRelationshipsResponseTypeDef(TypedDict):
    compositionRelationshipSummaries: list[CompositionRelationshipSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ComputationModelConfigurationTypeDef(TypedDict):
    anomalyDetection: NotRequired[ComputationModelAnomalyDetectionConfigurationTypeDef]

class ComputeNodeExecutionStateDetailsTypeDef(TypedDict):
    code: ComputeNodeErrorCodeType
    message: str
    details: NotRequired[list[DetailedPipelineErrorTypeDef]]

class PipelineExecutionStateDetailsTypeDef(TypedDict):
    message: str
    code: NotRequired[PipelineErrorCodeType]
    details: NotRequired[list[DetailedPipelineErrorTypeDef]]

ComputeNodeUnionTypeDef = Union[ComputeNodeTypeDef, ComputeNodeOutputTypeDef]

class ConfigurationStatusTypeDef(TypedDict):
    state: ConfigurationStateType
    error: NotRequired[ConfigurationErrorDetailsTypeDef]

class CreateWorkspaceRequestTypeDef(TypedDict):
    workspaceName: str
    encryptionConfiguration: WorkspaceEncryptionConfigurationTypeDef
    workspaceDescription: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]

class UpdateWorkspaceRequestTypeDef(TypedDict):
    workspaceName: str
    workspaceDescription: NotRequired[str]
    encryptionConfiguration: NotRequired[WorkspaceEncryptionConfigurationTypeDef]
    clientToken: NotRequired[str]

class FileFormatOutputTypeDef(TypedDict):
    csv: NotRequired[CsvOutputTypeDef]
    parquet: NotRequired[dict[str, Any]]
    mp4: NotRequired[dict[str, Any]]
    annotation: NotRequired[dict[str, Any]]

CsvUnionTypeDef = Union[CsvTypeDef, CsvOutputTypeDef]

class MultiLayerStorageTypeDef(TypedDict):
    customerManagedS3Storage: CustomerManagedS3StorageTypeDef

class ListDashboardsResponseTypeDef(TypedDict):
    dashboardSummaries: list[DashboardSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DataSegmentSummaryTypeDef(TypedDict):
    sourceDatasetId: str
    timeSeriesId: str
    startTimestamp: TimeInNanosTypeDef
    endTimestamp: TimeInNanosTypeDef
    alias: str
    dataType: PropertyDataTypeType
    enrichment: NotRequired[DataSegmentEnrichmentTypeDef]

class DatasetEnrichmentTypeDef(TypedDict):
    video: NotRequired[DatasetEnrichmentEntryTypeDef]

class RowPaginatorTypeDef(TypedDict):
    data: list[DatumPaginatorTypeDef]

class RowTypeDef(TypedDict):
    data: list[DatumTypeDef]

class DescribeAssetModelInterfaceRelationshipResponseTypeDef(TypedDict):
    assetModelId: str
    interfaceAssetModelId: str
    propertyMappings: list[PropertyMappingTypeDef]
    hierarchyMappings: list[HierarchyMappingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PropertyMappingConfigurationTypeDef(TypedDict):
    matchByPropertyName: NotRequired[bool]
    createMissingProperty: NotRequired[bool]
    overrides: NotRequired[Sequence[PropertyMappingTypeDef]]

class DescribeAssetModelRequestWaitExtraTypeDef(TypedDict):
    assetModelId: str
    excludeProperties: NotRequired[bool]
    assetModelVersion: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeAssetModelRequestWaitTypeDef(TypedDict):
    assetModelId: str
    excludeProperties: NotRequired[bool]
    assetModelVersion: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeAssetRequestWaitExtraTypeDef(TypedDict):
    assetId: str
    excludeProperties: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeAssetRequestWaitTypeDef(TypedDict):
    assetId: str
    excludeProperties: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribePortalRequestWaitExtraTypeDef(TypedDict):
    portalId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribePortalRequestWaitTypeDef(TypedDict):
    portalId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class DescribeExecutionResponseTypeDef(TypedDict):
    executionId: str
    actionType: str
    targetResource: TargetResourceTypeDef
    targetResourceVersion: str
    resolveTo: ResolveToTypeDef
    executionStartTime: datetime
    executionEndTime: datetime
    executionStatus: ExecutionStatusTypeDef
    executionResult: dict[str, str]
    executionDetails: dict[str, str]
    executionEntityVersion: str
    ResponseMetadata: ResponseMetadataTypeDef

class ExecutionSummaryTypeDef(TypedDict):
    executionId: str
    targetResource: TargetResourceTypeDef
    targetResourceVersion: str
    executionStartTime: datetime
    executionStatus: ExecutionStatusTypeDef
    actionType: NotRequired[str]
    resolveTo: NotRequired[ResolveToTypeDef]
    executionEndTime: NotRequired[datetime]
    executionEntityVersion: NotRequired[str]

class DescribeLoggingOptionsResponseTypeDef(TypedDict):
    loggingOptions: LoggingOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutLoggingOptionsRequestTypeDef(TypedDict):
    loggingOptions: LoggingOptionsTypeDef
    workspaceName: NotRequired[str]

class DescribePipelineExecutionRequestPaginateTypeDef(TypedDict):
    workspaceName: str
    pipelineName: str
    pipelineExecutionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ExecuteQueryRequestPaginateTypeDef(TypedDict):
    queryStatement: str
    clientToken: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetAssetPropertyAggregatesRequestPaginateTypeDef(TypedDict):
    aggregateTypes: Sequence[AggregateTypeType]
    resolution: str
    startDate: TimestampTypeDef
    endDate: TimestampTypeDef
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetAssetPropertyValueHistoryRequestPaginateTypeDef(TypedDict):
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]
    startDate: NotRequired[TimestampTypeDef]
    endDate: NotRequired[TimestampTypeDef]
    qualities: NotRequired[Sequence[QualityType]]
    timeOrdering: NotRequired[TimeOrderingType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

GetInterpolatedAssetPropertyValuesRequestPaginateTypeDef = TypedDict(
    "GetInterpolatedAssetPropertyValuesRequestPaginateTypeDef",
    {
        "startTimeInSeconds": int,
        "endTimeInSeconds": int,
        "quality": QualityType,
        "intervalInSeconds": int,
        "type": str,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "startTimeOffsetInNanos": NotRequired[int],
        "endTimeOffsetInNanos": NotRequired[int],
        "intervalWindowInSeconds": NotRequired[int],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class GetQueryResultsRequestPaginateTypeDef(TypedDict):
    workspaceName: str
    queryId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetSearchResultsRequestPaginateTypeDef(TypedDict):
    searchId: str
    workspaceName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAccessPoliciesRequestPaginateTypeDef(TypedDict):
    identityType: NotRequired[IdentityTypeType]
    identityId: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    resourceId: NotRequired[str]
    iamArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListActionsRequestPaginateTypeDef(TypedDict):
    targetResourceType: TargetResourceTypeType
    targetResourceId: str
    resolveToResourceType: NotRequired[Literal["ASSET"]]
    resolveToResourceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssetModelCompositeModelsRequestPaginateTypeDef(TypedDict):
    assetModelId: str
    assetModelVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListAssetModelPropertiesRequestPaginateTypeDef = TypedDict(
    "ListAssetModelPropertiesRequestPaginateTypeDef",
    {
        "assetModelId": str,
        "filter": NotRequired[ListAssetModelPropertiesFilterType],
        "assetModelVersion": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListAssetModelsRequestPaginateTypeDef(TypedDict):
    assetModelTypes: NotRequired[Sequence[AssetModelTypeType]]
    assetModelVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListAssetPropertiesRequestPaginateTypeDef = TypedDict(
    "ListAssetPropertiesRequestPaginateTypeDef",
    {
        "assetId": str,
        "filter": NotRequired[ListAssetPropertiesFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListAssetRelationshipsRequestPaginateTypeDef(TypedDict):
    assetId: str
    traversalType: Literal["PATH_TO_ROOT"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListAssetsRequestPaginateTypeDef = TypedDict(
    "ListAssetsRequestPaginateTypeDef",
    {
        "assetModelId": NotRequired[str],
        "filter": NotRequired[ListAssetsFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListAssociatedAssetsRequestPaginateTypeDef(TypedDict):
    assetId: str
    hierarchyId: NotRequired[str]
    traversalDirection: NotRequired[TraversalDirectionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListBulkImportJobsRequestPaginateTypeDef = TypedDict(
    "ListBulkImportJobsRequestPaginateTypeDef",
    {
        "filter": NotRequired[ListBulkImportJobsFilterType],
        "workspaceName": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListCompositionRelationshipsRequestPaginateTypeDef(TypedDict):
    assetModelId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListComputationModelResolveToResourcesRequestPaginateTypeDef(TypedDict):
    computationModelId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListComputationModelsRequestPaginateTypeDef(TypedDict):
    computationModelType: NotRequired[Literal["ANOMALY_DETECTION"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDashboardsRequestPaginateTypeDef(TypedDict):
    projectId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDatasetDataSegmentRelationshipsRequestPaginateTypeDef(TypedDict):
    datasetId: str
    workspaceName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDatasetDataSegmentsRequestPaginateTypeDef(TypedDict):
    datasetId: str
    workspaceName: str
    datasetVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListDatasetExportJobsRequestPaginateTypeDef = TypedDict(
    "ListDatasetExportJobsRequestPaginateTypeDef",
    {
        "workspaceName": str,
        "filter": NotRequired[DatasetExportJobFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListDatasetsRequestPaginateTypeDef(TypedDict):
    sourceType: DatasetSourceTypeType
    workspaceName: NotRequired[str]
    datasetType: NotRequired[DatasetTypeEnumType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnrichmentJobsRequestPaginateTypeDef(TypedDict):
    workspaceName: str
    datasetId: NotRequired[str]
    propertyAlias: NotRequired[str]
    timeSeriesId: NotRequired[str]
    status: NotRequired[EnrichmentJobStatusType]
    jobType: NotRequired[Literal["EVENT_DETECTION"]]
    startDate: NotRequired[TimestampTypeDef]
    endDate: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListExecutionsRequestPaginateTypeDef(TypedDict):
    targetResourceType: TargetResourceTypeType
    targetResourceId: str
    resolveToResourceType: NotRequired[Literal["ASSET"]]
    resolveToResourceId: NotRequired[str]
    actionType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGatewaysRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInterfaceRelationshipsRequestPaginateTypeDef(TypedDict):
    interfaceAssetModelId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPipelineExecutionsRequestPaginateTypeDef(TypedDict):
    workspaceName: str
    pipelineName: str
    state: NotRequired[PipelineExecutionStateType]
    startTimeAfter: NotRequired[TimestampTypeDef]
    startTimeBefore: NotRequired[TimestampTypeDef]
    endTimeAfter: NotRequired[TimestampTypeDef]
    endTimeBefore: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPipelinesRequestPaginateTypeDef(TypedDict):
    workspaceName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPortalsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectAssetsRequestPaginateTypeDef(TypedDict):
    projectId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProjectsRequestPaginateTypeDef(TypedDict):
    portalId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListQueriesRequestPaginateTypeDef = TypedDict(
    "ListQueriesRequestPaginateTypeDef",
    {
        "workspaceName": str,
        "filter": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListTasksRequestPaginateTypeDef(TypedDict):
    workspaceName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTimeSeriesRequestPaginateTypeDef(TypedDict):
    assetId: NotRequired[str]
    aliasPrefix: NotRequired[str]
    timeSeriesType: NotRequired[ListTimeSeriesTypeType]
    workspaceName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorkspacesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class DescribeQueryResponseTypeDef(TypedDict):
    queryId: str
    status: QueryStatusType
    submittedAt: datetime
    completedAt: datetime
    statistics: QueryStatisticsTypeDef
    errorMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class ErrorDetailsTypeDef(TypedDict):
    code: ErrorCodeType
    message: str
    details: NotRequired[list[DetailedErrorTypeDef]]

class ListEnrichmentJobsResponseTypeDef(TypedDict):
    jobs: list[EnrichmentJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ExecutionEnvironmentVariablesUnionTypeDef = Union[
    ExecutionEnvironmentVariablesTypeDef, ExecutionEnvironmentVariablesOutputTypeDef
]

class ListDatasetExportJobsResponseTypeDef(TypedDict):
    jobs: list[ExportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetCaptureDataRequestTypeDef(TypedDict):
    workspaceName: str
    startTime: TimeInNanosTypeDef
    endTime: TimeInNanosTypeDef
    timeSeriesId: NotRequired[str]
    propertyAlias: NotRequired[str]
    formatSettings: NotRequired[FormatSettingsTypeDef]
    nextToken: NotRequired[str]

class MeasurementProcessingConfigTypeDef(TypedDict):
    forwardingConfig: ForwardingConfigTypeDef

class TransformProcessingConfigTypeDef(TypedDict):
    computeLocation: ComputeLocationType
    forwardingConfig: NotRequired[ForwardingConfigTypeDef]

class GatewayPlatformTypeDef(TypedDict):
    greengrass: NotRequired[GreengrassTypeDef]
    greengrassV2: NotRequired[GreengrassV2TypeDef]
    siemensIE: NotRequired[SiemensIETypeDef]

class IdentityTypeDef(TypedDict):
    user: NotRequired[UserIdentityTypeDef]
    group: NotRequired[GroupIdentityTypeDef]
    iamUser: NotRequired[IAMUserIdentityTypeDef]
    iamRole: NotRequired[IAMRoleIdentityTypeDef]

class ListInterfaceRelationshipsResponseTypeDef(TypedDict):
    interfaceRelationshipSummaries: list[InterfaceRelationshipSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBulkImportJobsResponseTypeDef(TypedDict):
    jobSummaries: list[JobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SourceDetailTypeDef(TypedDict):
    kendra: NotRequired[KendraSourceDetailTypeDef]

class ListProjectsResponseTypeDef(TypedDict):
    projectSummaries: list[ProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListQueriesResponseTypeDef(TypedDict):
    queries: list[QuerySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSearchesResponseTypeDef(TypedDict):
    searchSummaries: list[SearchSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTimeSeriesResponseTypeDef(TypedDict):
    TimeSeriesSummaries: list[TimeSeriesSummaryTypeDef]
    workspaceName: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class SourceTypeDef(TypedDict):
    arn: NotRequired[str]
    location: NotRequired[LocationTypeDef]

class MetricWindowTypeDef(TypedDict):
    tumbling: NotRequired[TumblingWindowTypeDef]

class PortalStatusTypeDef(TypedDict):
    state: PortalStateType
    error: NotRequired[MonitorErrorDetailsTypeDef]

class MountSourceTypeDef(TypedDict):
    s3AccessPoint: NotRequired[S3AccessPointSourceTypeDef]

PortalTypeEntryUnionTypeDef = Union[PortalTypeEntryTypeDef, PortalTypeEntryOutputTypeDef]

class ResourceTypeDef(TypedDict):
    portal: NotRequired[PortalResourceTypeDef]
    project: NotRequired[ProjectResourceTypeDef]

class VariantTypeDef(TypedDict):
    stringValue: NotRequired[str]
    integerValue: NotRequired[int]
    doubleValue: NotRequired[float]
    booleanValue: NotRequired[bool]
    nullValue: NotRequired[PropertyValueNullValueTypeDef]

class ResourceStatusTypeDef(TypedDict):
    error: NotRequired[ResourceErrorTypeDef]
    state: NotRequired[ResourceStateType]

class WorkspaceStatusTypeDef(TypedDict):
    state: WorkspaceStateType
    error: NotRequired[WorkspaceErrorDetailsTypeDef]

class ListComputationModelResolveToResourcesResponseTypeDef(TypedDict):
    computationModelResolveToResourceSummaries: list[
        ComputationModelResolveToResourceSummaryTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListActionsResponseTypeDef(TypedDict):
    actionSummaries: list[ActionSummaryTypeDef]
    nextToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetAssetPropertyAggregatesSuccessEntryTypeDef(TypedDict):
    entryId: str
    aggregatedValues: list[AggregatedValueTypeDef]

class GetAssetPropertyAggregatesResponseTypeDef(TypedDict):
    aggregatedValues: list[AggregatedValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAssetRelationshipsResponseTypeDef(TypedDict):
    assetRelationshipSummaries: list[AssetRelationshipSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAssetModelCompositeModelsResponseTypeDef(TypedDict):
    assetModelCompositeModelSummaries: list[AssetModelCompositeModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ExpressionVariableOutputTypeDef(TypedDict):
    name: str
    value: VariableValueOutputTypeDef

VariableValueUnionTypeDef = Union[VariableValueTypeDef, VariableValueOutputTypeDef]

class ListComputationModelDataBindingUsagesRequestPaginateTypeDef(TypedDict):
    dataBindingValueFilter: DataBindingValueFilterTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListComputationModelDataBindingUsagesRequestTypeDef(TypedDict):
    dataBindingValueFilter: DataBindingValueFilterTypeDef
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

ComputationModelDataBindingValueUnionTypeDef = Union[
    ComputationModelDataBindingValueTypeDef, ComputationModelDataBindingValueOutputTypeDef
]

class MatchedDataBindingTypeDef(TypedDict):
    value: DataBindingValueTypeDef

class ListAssetPropertiesResponseTypeDef(TypedDict):
    assetPropertySummaries: list[AssetPropertySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

AssetCompositeModelTypeDef = TypedDict(
    "AssetCompositeModelTypeDef",
    {
        "name": str,
        "type": str,
        "properties": list[AssetPropertyTypeDef],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)

class DescribeAssetCompositeModelResponseTypeDef(TypedDict):
    assetId: str
    assetCompositeModelId: str
    assetCompositeModelExternalId: str
    assetCompositeModelPath: list[AssetCompositeModelPathSegmentTypeDef]
    assetCompositeModelName: str
    assetCompositeModelDescription: str
    assetCompositeModelType: str
    assetCompositeModelProperties: list[AssetPropertyTypeDef]
    assetCompositeModelSummaries: list[AssetCompositeModelSummaryTypeDef]
    actionDefinitions: list[ActionDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchAssociateDataSegmentsToDatasetRequestTypeDef(TypedDict):
    datasetId: str
    workspaceName: str
    associateDataSegmentEntries: Sequence[AssociateDataSegmentEntryTypeDef]
    clientToken: NotRequired[str]

class BatchPutAssetPropertyErrorEntryTypeDef(TypedDict):
    entryId: str
    errors: list[BatchPutAssetPropertyErrorTypeDef]

class ListDatasetDataSegmentRelationshipsResponseTypeDef(TypedDict):
    dataSegmentRelationshipSummaries: list[DataSegmentRelationshipSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchDeleteDatasetDataSegmentsRequestTypeDef(TypedDict):
    datasetId: str
    workspaceName: str
    deleteDataSegmentEntries: Sequence[DeleteDataSegmentEntryTypeDef]
    clientToken: NotRequired[str]

class BatchDisassociateDataSegmentsFromDatasetRequestTypeDef(TypedDict):
    datasetId: str
    workspaceName: str
    disassociateDataSegmentEntries: Sequence[DisassociateDataSegmentEntryTypeDef]
    clientToken: NotRequired[str]

class EventDetectionTypeDef(TypedDict):
    datasetId: str
    trimSettings: EnrichmentTrimSettingsTypeDef
    timeSeriesId: NotRequired[str]
    propertyAlias: NotRequired[str]

class BatchAssociateDataSegmentsToDatasetResponseTypeDef(TypedDict):
    datasetId: str
    datasetVersion: str
    failedAssociations: list[FailedDataSegmentAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeleteDatasetDataSegmentsResponseTypeDef(TypedDict):
    datasetId: str
    datasetVersion: str
    errors: list[FailedDataSegmentDeletionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDisassociateDataSegmentsFromDatasetResponseTypeDef(TypedDict):
    datasetId: str
    datasetVersion: str
    failedDisassociations: list[FailedDataSegmentDisassociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetSearchResultsResponseTypeDef(TypedDict):
    searchResults: list[SearchResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DatasetConfigTypeDef(TypedDict):
    session: NotRequired[SessionConfigTypeDef]

class SearchFiltersTypeDef(TypedDict):
    timeSeriesIds: NotRequired[Sequence[str]]
    datasetIds: NotRequired[Sequence[str]]
    timeIntervals: NotRequired[Sequence[TimeIntervalTypeDef]]

class DatasetItemOutputTypeDef(TypedDict):
    datasetId: str
    trimSettings: NotRequired[TrimSettingsTypeDef]
    exportDataTypes: NotRequired[list[ExportDataTypeType]]

class DatasetItemTypeDef(TypedDict):
    datasetId: str
    trimSettings: NotRequired[TrimSettingsTypeDef]
    exportDataTypes: NotRequired[Sequence[ExportDataTypeType]]

class TimeseriesItemTypeDef(TypedDict):
    timeSeriesId: NotRequired[str]
    propertyAlias: NotRequired[str]
    trimSettings: NotRequired[TrimSettingsTypeDef]
    formatSettings: NotRequired[FormatSettingsTypeDef]

class BatchGetAssetPropertyAggregatesRequestTypeDef(TypedDict):
    entries: Sequence[BatchGetAssetPropertyAggregatesEntryTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class BatchGetAssetPropertyValueHistoryRequestTypeDef(TypedDict):
    entries: Sequence[BatchGetAssetPropertyValueHistoryEntryTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListSearchesRequestPaginateTypeDef(TypedDict):
    workspaceName: str
    listSearchesFilters: NotRequired[ListSearchesFiltersTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSearchesRequestTypeDef(TypedDict):
    workspaceName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    listSearchesFilters: NotRequired[ListSearchesFiltersTypeDef]

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "id": NotRequired[str],
        "file": NotRequired[ImageFileTypeDef],
    },
)

class ComputeNodeExecutionStatusTypeDef(TypedDict):
    state: ComputeNodeExecutionStateType
    stateDetails: NotRequired[ComputeNodeExecutionStateDetailsTypeDef]

class PipelineExecutionStatusTypeDef(TypedDict):
    state: PipelineExecutionStateType
    stateDetails: NotRequired[PipelineExecutionStateDetailsTypeDef]

class CreatePipelineRequestTypeDef(TypedDict):
    workspaceName: str
    pipelineName: str
    computations: Sequence[ComputeNodeUnionTypeDef]
    description: NotRequired[str]
    environmentVariables: NotRequired[Mapping[str, str]]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]

class UpdatePipelineRequestTypeDef(TypedDict):
    workspaceName: str
    pipelineName: str
    description: NotRequired[str]
    environmentVariables: NotRequired[Mapping[str, str]]
    computations: NotRequired[Sequence[ComputeNodeUnionTypeDef]]

class DescribeDefaultEncryptionConfigurationResponseTypeDef(TypedDict):
    encryptionType: EncryptionTypeType
    kmsKeyArn: str
    configurationStatus: ConfigurationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutDefaultEncryptionConfigurationResponseTypeDef(TypedDict):
    encryptionType: EncryptionTypeType
    kmsKeyArn: str
    configurationStatus: ConfigurationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class FileOutputTypeDef(TypedDict):
    bucket: str
    key: str
    versionId: NotRequired[str]
    alias: NotRequired[str]
    startTime: NotRequired[TimeInNanosTypeDef]
    fileFormat: NotRequired[FileFormatOutputTypeDef]

class JobConfigurationOutputTypeDef(TypedDict):
    fileFormat: NotRequired[FileFormatOutputTypeDef]

class FileFormatTypeDef(TypedDict):
    csv: NotRequired[CsvUnionTypeDef]
    parquet: NotRequired[Mapping[str, Any]]
    mp4: NotRequired[Mapping[str, Any]]
    annotation: NotRequired[Mapping[str, Any]]

class DescribeStorageConfigurationResponseTypeDef(TypedDict):
    storageType: StorageTypeType
    multiLayerStorage: MultiLayerStorageTypeDef
    disassociatedDataStorage: DisassociatedDataStorageStateType
    retentionPeriod: RetentionPeriodTypeDef
    configurationStatus: ConfigurationStatusTypeDef
    lastUpdateDate: datetime
    warmTier: WarmTierStateType
    warmTierRetentionPeriod: WarmTierRetentionPeriodTypeDef
    disallowIngestNullNaN: bool
    ResponseMetadata: ResponseMetadataTypeDef

class PutStorageConfigurationRequestTypeDef(TypedDict):
    storageType: StorageTypeType
    multiLayerStorage: NotRequired[MultiLayerStorageTypeDef]
    disassociatedDataStorage: NotRequired[DisassociatedDataStorageStateType]
    retentionPeriod: NotRequired[RetentionPeriodTypeDef]
    warmTier: NotRequired[WarmTierStateType]
    warmTierRetentionPeriod: NotRequired[WarmTierRetentionPeriodTypeDef]
    disallowIngestNullNaN: NotRequired[bool]

class PutStorageConfigurationResponseTypeDef(TypedDict):
    storageType: StorageTypeType
    multiLayerStorage: MultiLayerStorageTypeDef
    disassociatedDataStorage: DisassociatedDataStorageStateType
    retentionPeriod: RetentionPeriodTypeDef
    configurationStatus: ConfigurationStatusTypeDef
    warmTier: WarmTierStateType
    warmTierRetentionPeriod: WarmTierRetentionPeriodTypeDef
    disallowIngestNullNaN: bool
    ResponseMetadata: ResponseMetadataTypeDef

class ListDatasetDataSegmentsResponseTypeDef(TypedDict):
    dataSegments: list[DataSegmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ExecuteQueryResponsePaginatorTypeDef(TypedDict):
    columns: list[ColumnInfoTypeDef]
    rows: list[RowPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ExecuteQueryResponseTypeDef(TypedDict):
    columns: list[ColumnInfoTypeDef]
    rows: list[RowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PutAssetModelInterfaceRelationshipRequestTypeDef(TypedDict):
    assetModelId: str
    interfaceAssetModelId: str
    propertyMappingConfiguration: PropertyMappingConfigurationTypeDef
    clientToken: NotRequired[str]

class ListExecutionsResponseTypeDef(TypedDict):
    executionSummaries: list[ExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AssetModelStatusTypeDef(TypedDict):
    state: AssetModelStateType
    error: NotRequired[ErrorDetailsTypeDef]

class AssetStatusTypeDef(TypedDict):
    state: AssetStateType
    error: NotRequired[ErrorDetailsTypeDef]

class ComputationModelStatusTypeDef(TypedDict):
    state: ComputationModelStateType
    error: NotRequired[ErrorDetailsTypeDef]

class DatasetStatusTypeDef(TypedDict):
    state: DatasetStateType
    error: NotRequired[ErrorDetailsTypeDef]

class MeasurementTypeDef(TypedDict):
    processingConfig: NotRequired[MeasurementProcessingConfigTypeDef]

class CreateGatewayRequestTypeDef(TypedDict):
    gatewayName: str
    gatewayPlatform: GatewayPlatformTypeDef
    gatewayVersion: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class DescribeGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    gatewayName: str
    gatewayArn: str
    gatewayPlatform: GatewayPlatformTypeDef
    gatewayVersion: str
    gatewayCapabilitySummaries: list[GatewayCapabilitySummaryTypeDef]
    creationDate: datetime
    lastUpdateDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GatewaySummaryTypeDef(TypedDict):
    gatewayId: str
    gatewayName: str
    creationDate: datetime
    lastUpdateDate: datetime
    gatewayPlatform: NotRequired[GatewayPlatformTypeDef]
    gatewayVersion: NotRequired[str]
    gatewayCapabilitySummaries: NotRequired[list[GatewayCapabilitySummaryTypeDef]]

class DatasetSourceTypeDef(TypedDict):
    sourceType: DatasetSourceTypeType
    sourceFormat: DatasetSourceFormatType
    sourceDetail: NotRequired[SourceDetailTypeDef]

class DataSetReferenceTypeDef(TypedDict):
    datasetArn: NotRequired[str]
    source: NotRequired[SourceTypeDef]

class CreatePortalResponseTypeDef(TypedDict):
    portalId: str
    portalArn: str
    portalStartUrl: str
    portalStatus: PortalStatusTypeDef
    ssoApplicationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePortalResponseTypeDef(TypedDict):
    portalStatus: PortalStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePortalResponseTypeDef(TypedDict):
    portalId: str
    portalArn: str
    portalName: str
    portalDescription: str
    portalClientId: str
    portalStartUrl: str
    portalContactEmail: str
    portalStatus: PortalStatusTypeDef
    portalCreationDate: datetime
    portalLastUpdateDate: datetime
    portalLogoImageLocation: ImageLocationTypeDef
    roleArn: str
    portalAuthMode: AuthModeType
    notificationSenderEmail: str
    alarms: AlarmsTypeDef
    portalType: PortalTypeType
    portalTypeConfiguration: dict[str, PortalTypeEntryOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

PortalSummaryTypeDef = TypedDict(
    "PortalSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "startUrl": str,
        "status": PortalStatusTypeDef,
        "description": NotRequired[str],
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
        "roleArn": NotRequired[str],
        "portalType": NotRequired[PortalTypeType],
    },
)

class UpdatePortalResponseTypeDef(TypedDict):
    portalStatus: PortalStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class MountTypeDef(TypedDict):
    name: str
    relativePath: str
    source: MountSourceTypeDef
    storageType: Literal["SHARED_STORAGE"]

class CreatePortalRequestTypeDef(TypedDict):
    portalName: str
    portalContactEmail: str
    roleArn: str
    portalDescription: NotRequired[str]
    clientToken: NotRequired[str]
    portalLogoImageFile: NotRequired[ImageFileTypeDef]
    tags: NotRequired[Mapping[str, str]]
    portalAuthMode: NotRequired[AuthModeType]
    notificationSenderEmail: NotRequired[str]
    alarms: NotRequired[AlarmsTypeDef]
    portalType: NotRequired[PortalTypeType]
    portalTypeConfiguration: NotRequired[Mapping[str, PortalTypeEntryUnionTypeDef]]

AccessPolicySummaryTypeDef = TypedDict(
    "AccessPolicySummaryTypeDef",
    {
        "id": str,
        "identity": IdentityTypeDef,
        "resource": ResourceTypeDef,
        "permission": PermissionType,
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
    },
)

class CreateAccessPolicyRequestTypeDef(TypedDict):
    accessPolicyIdentity: IdentityTypeDef
    accessPolicyResource: ResourceTypeDef
    accessPolicyPermission: PermissionType
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class DescribeAccessPolicyResponseTypeDef(TypedDict):
    accessPolicyId: str
    accessPolicyArn: str
    accessPolicyIdentity: IdentityTypeDef
    accessPolicyResource: ResourceTypeDef
    accessPolicyPermission: PermissionType
    accessPolicyCreationDate: datetime
    accessPolicyLastUpdateDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAccessPolicyRequestTypeDef(TypedDict):
    accessPolicyId: str
    accessPolicyIdentity: IdentityTypeDef
    accessPolicyResource: ResourceTypeDef
    accessPolicyPermission: PermissionType
    clientToken: NotRequired[str]

class AssetPropertyValueTypeDef(TypedDict):
    value: VariantTypeDef
    timestamp: TimeInNanosTypeDef
    quality: NotRequired[QualityType]

class InterpolatedAssetPropertyValueTypeDef(TypedDict):
    timestamp: TimeInNanosTypeDef
    value: VariantTypeDef

class CreatePipelineResponseTypeDef(TypedDict):
    pipelineName: str
    pipelineArn: str
    version: str
    status: ResourceStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTaskResponseTypeDef(TypedDict):
    taskName: str
    taskArn: str
    version: str
    status: ResourceStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePipelineResponseTypeDef(TypedDict):
    status: ResourceStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteTaskResponseTypeDef(TypedDict):
    status: ResourceStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribePipelineResponseTypeDef(TypedDict):
    pipelineName: str
    workspaceName: str
    description: str
    pipelineArn: str
    version: str
    environmentVariables: dict[str, str]
    computations: list[ComputeNodeOutputTypeDef]
    status: ResourceStatusTypeDef
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PipelineSummaryTypeDef(TypedDict):
    pipelineName: str
    pipelineArn: str
    version: str
    status: ResourceStatusTypeDef
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]

class TaskSummaryTypeDef(TypedDict):
    taskName: str
    taskArn: str
    version: str
    status: ResourceStatusTypeDef
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]

class UpdatePipelineResponseTypeDef(TypedDict):
    version: str
    status: ResourceStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTaskResponseTypeDef(TypedDict):
    version: str
    status: ResourceStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateWorkspaceResponseTypeDef(TypedDict):
    workspaceName: str
    workspaceArn: str
    workspaceStatus: WorkspaceStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteWorkspaceResponseTypeDef(TypedDict):
    workspaceStatus: WorkspaceStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeWorkspaceResponseTypeDef(TypedDict):
    workspaceArn: str
    workspaceName: str
    workspaceDescription: str
    workspaceStatus: WorkspaceStatusTypeDef
    encryptionConfiguration: WorkspaceEncryptionConfigurationInfoTypeDef
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateWorkspaceResponseTypeDef(TypedDict):
    workspaceStatus: WorkspaceStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class WorkspaceSummaryTypeDef(TypedDict):
    name: str
    arn: str
    status: WorkspaceStatusTypeDef
    createdAt: datetime
    updatedAt: datetime

class BatchGetAssetPropertyAggregatesResponseTypeDef(TypedDict):
    errorEntries: list[BatchGetAssetPropertyAggregatesErrorEntryTypeDef]
    successEntries: list[BatchGetAssetPropertyAggregatesSuccessEntryTypeDef]
    skippedEntries: list[BatchGetAssetPropertyAggregatesSkippedEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class MetricOutputTypeDef(TypedDict):
    window: MetricWindowTypeDef
    expression: NotRequired[str]
    variables: NotRequired[list[ExpressionVariableOutputTypeDef]]
    processingConfig: NotRequired[MetricProcessingConfigTypeDef]

class TransformOutputTypeDef(TypedDict):
    expression: str
    variables: list[ExpressionVariableOutputTypeDef]
    processingConfig: NotRequired[TransformProcessingConfigTypeDef]

class ExpressionVariableTypeDef(TypedDict):
    name: str
    value: VariableValueUnionTypeDef

class CreateComputationModelRequestTypeDef(TypedDict):
    computationModelName: str
    computationModelConfiguration: ComputationModelConfigurationTypeDef
    computationModelDataBinding: Mapping[str, ComputationModelDataBindingValueUnionTypeDef]
    computationModelDescription: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateComputationModelRequestTypeDef(TypedDict):
    computationModelId: str
    computationModelName: str
    computationModelConfiguration: ComputationModelConfigurationTypeDef
    computationModelDataBinding: Mapping[str, ComputationModelDataBindingValueUnionTypeDef]
    computationModelDescription: NotRequired[str]
    clientToken: NotRequired[str]

class ComputationModelDataBindingUsageSummaryTypeDef(TypedDict):
    computationModelIds: list[str]
    matchedDataBinding: MatchedDataBindingTypeDef

class BatchPutAssetPropertyValueResponseTypeDef(TypedDict):
    errorEntries: list[BatchPutAssetPropertyErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class EnrichmentJobConfigurationTypeDef(TypedDict):
    eventDetection: NotRequired[EventDetectionTypeDef]

class StartSearchRequestTypeDef(TypedDict):
    workspaceName: str
    queryStatement: str
    clientToken: NotRequired[str]
    searchType: NotRequired[SearchTypeType]
    searchFilters: NotRequired[SearchFiltersTypeDef]
    groupId: NotRequired[str]

class ProcessingInputOutputTypeDef(TypedDict):
    timeseries: NotRequired[list[TimeseriesItemTypeDef]]
    dataset: NotRequired[DatasetItemOutputTypeDef]

class ProcessingInputTypeDef(TypedDict):
    timeseries: NotRequired[Sequence[TimeseriesItemTypeDef]]
    dataset: NotRequired[DatasetItemTypeDef]

class UpdatePortalRequestTypeDef(TypedDict):
    portalId: str
    portalName: str
    portalContactEmail: str
    roleArn: str
    portalDescription: NotRequired[str]
    portalLogoImage: NotRequired[ImageTypeDef]
    clientToken: NotRequired[str]
    notificationSenderEmail: NotRequired[str]
    alarms: NotRequired[AlarmsTypeDef]
    portalType: NotRequired[PortalTypeType]
    portalTypeConfiguration: NotRequired[Mapping[str, PortalTypeEntryUnionTypeDef]]

class PipelineExecutionSummaryTypeDef(TypedDict):
    pipelineExecutionId: str
    pipelineVersion: str
    status: PipelineExecutionStatusTypeDef
    executionPriority: NotRequired[int]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]

class DescribeBulkImportJobResponseTypeDef(TypedDict):
    jobId: str
    jobName: str
    jobStatus: JobStatusType
    jobRoleArn: str
    files: list[FileOutputTypeDef]
    errorReportLocation: ErrorReportLocationTypeDef
    jobConfiguration: JobConfigurationOutputTypeDef
    jobCreationDate: datetime
    jobLastUpdateDate: datetime
    adaptiveIngestion: bool
    deleteFilesAfterImport: bool
    datasetId: str
    workspaceName: str
    ResponseMetadata: ResponseMetadataTypeDef

FileFormatUnionTypeDef = Union[FileFormatTypeDef, FileFormatOutputTypeDef]

class JobConfigurationTypeDef(TypedDict):
    fileFormat: NotRequired[FileFormatTypeDef]

AssetModelSummaryTypeDef = TypedDict(
    "AssetModelSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetModelStatusTypeDef,
        "externalId": NotRequired[str],
        "assetModelType": NotRequired[AssetModelTypeType],
        "version": NotRequired[str],
    },
)

class CreateAssetModelCompositeModelResponseTypeDef(TypedDict):
    assetModelCompositeModelId: str
    assetModelCompositeModelPath: list[AssetModelCompositeModelPathSegmentTypeDef]
    assetModelStatus: AssetModelStatusTypeDef
    assetModelId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAssetModelResponseTypeDef(TypedDict):
    assetModelId: str
    assetModelArn: str
    assetModelStatus: AssetModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAssetModelCompositeModelResponseTypeDef(TypedDict):
    assetModelStatus: AssetModelStatusTypeDef
    assetModelId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAssetModelInterfaceRelationshipResponseTypeDef(TypedDict):
    assetModelId: str
    interfaceAssetModelId: str
    assetModelArn: str
    assetModelStatus: AssetModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAssetModelResponseTypeDef(TypedDict):
    assetModelId: str
    assetModelStatus: AssetModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutAssetModelInterfaceRelationshipResponseTypeDef(TypedDict):
    assetModelId: str
    interfaceAssetModelId: str
    assetModelArn: str
    assetModelStatus: AssetModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAssetModelCompositeModelResponseTypeDef(TypedDict):
    assetModelCompositeModelPath: list[AssetModelCompositeModelPathSegmentTypeDef]
    assetModelStatus: AssetModelStatusTypeDef
    assetModelId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAssetModelResponseTypeDef(TypedDict):
    assetModelId: str
    assetModelStatus: AssetModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

AssetSummaryTypeDef = TypedDict(
    "AssetSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetStatusTypeDef,
        "hierarchies": list[AssetHierarchyTypeDef],
        "externalId": NotRequired[str],
        "description": NotRequired[str],
    },
)
AssociatedAssetsSummaryTypeDef = TypedDict(
    "AssociatedAssetsSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetStatusTypeDef,
        "hierarchies": list[AssetHierarchyTypeDef],
        "externalId": NotRequired[str],
        "description": NotRequired[str],
    },
)

class CreateAssetResponseTypeDef(TypedDict):
    assetId: str
    assetArn: str
    assetStatus: AssetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAssetResponseTypeDef(TypedDict):
    assetId: str
    assetStatus: AssetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAssetResponseTypeDef(TypedDict):
    assetId: str
    assetExternalId: str
    assetArn: str
    assetName: str
    assetModelId: str
    assetProperties: list[AssetPropertyTypeDef]
    assetHierarchies: list[AssetHierarchyTypeDef]
    assetCompositeModels: list[AssetCompositeModelTypeDef]
    assetCreationDate: datetime
    assetLastUpdateDate: datetime
    assetStatus: AssetStatusTypeDef
    assetDescription: str
    assetCompositeModelSummaries: list[AssetCompositeModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAssetResponseTypeDef(TypedDict):
    assetId: str
    assetStatus: AssetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ComputationModelSummaryTypeDef = TypedDict(
    "ComputationModelSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "type": Literal["ANOMALY_DETECTION"],
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": ComputationModelStatusTypeDef,
        "version": str,
        "description": NotRequired[str],
    },
)

class CreateComputationModelResponseTypeDef(TypedDict):
    computationModelId: str
    computationModelArn: str
    computationModelStatus: ComputationModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteComputationModelResponseTypeDef(TypedDict):
    computationModelStatus: ComputationModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeComputationModelResponseTypeDef(TypedDict):
    computationModelId: str
    computationModelArn: str
    computationModelName: str
    computationModelDescription: str
    computationModelConfiguration: ComputationModelConfigurationTypeDef
    computationModelDataBinding: dict[str, ComputationModelDataBindingValueOutputTypeDef]
    computationModelCreationDate: datetime
    computationModelLastUpdateDate: datetime
    computationModelStatus: ComputationModelStatusTypeDef
    computationModelVersion: str
    actionDefinitions: list[ActionDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateComputationModelResponseTypeDef(TypedDict):
    computationModelStatus: ComputationModelStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDatasetResponseTypeDef(TypedDict):
    datasetId: str
    datasetArn: str
    datasetStatus: DatasetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

DatasetSummaryTypeDef = TypedDict(
    "DatasetSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": DatasetStatusTypeDef,
        "sourceType": NotRequired[DatasetSourceTypeType],
        "datasetType": NotRequired[DatasetTypeEnumType],
        "enrichmentStatus": NotRequired[DatasetEnrichmentTypeDef],
    },
)

class DeleteDatasetResponseTypeDef(TypedDict):
    datasetStatus: DatasetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDatasetResponseTypeDef(TypedDict):
    datasetId: str
    datasetArn: str
    datasetStatus: DatasetStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListGatewaysResponseTypeDef(TypedDict):
    gatewaySummaries: list[GatewaySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateDatasetRequestTypeDef(TypedDict):
    datasetName: str
    datasetSource: DatasetSourceTypeDef
    datasetId: NotRequired[str]
    datasetDescription: NotRequired[str]
    datasetType: NotRequired[DatasetTypeEnumType]
    datasetConfig: NotRequired[DatasetConfigTypeDef]
    workspaceName: NotRequired[str]
    metadata: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class DescribeDatasetResponseTypeDef(TypedDict):
    datasetId: str
    datasetArn: str
    datasetName: str
    datasetDescription: str
    datasetType: DatasetTypeEnumType
    datasetConfig: DatasetConfigTypeDef
    workspaceName: str
    metadata: dict[str, str]
    datasetSource: DatasetSourceTypeDef
    datasetStatus: DatasetStatusTypeDef
    datasetCreationDate: datetime
    datasetLastUpdateDate: datetime
    datasetVersion: str
    enrichmentStatus: DatasetEnrichmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDatasetRequestTypeDef(TypedDict):
    datasetId: str
    datasetName: str
    datasetSource: DatasetSourceTypeDef
    workspaceName: NotRequired[str]
    datasetDescription: NotRequired[str]
    datasetConfig: NotRequired[DatasetConfigTypeDef]
    metadata: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]

class ReferenceTypeDef(TypedDict):
    dataset: NotRequired[DataSetReferenceTypeDef]

class ListPortalsResponseTypeDef(TypedDict):
    portalSummaries: list[PortalSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ComputeNodeExecutionDetailsTypeDef(TypedDict):
    computeNodeName: str
    taskName: str
    taskArn: str
    taskVersion: str
    dependsOn: list[str]
    status: ComputeNodeExecutionStatusTypeDef
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    executionEnvironmentVariables: NotRequired[dict[str, str]]
    executionMounts: NotRequired[list[MountTypeDef]]

class ContainerTaskConfigurationOutputTypeDef(TypedDict):
    ecrUri: str
    taskExecutionRole: str
    processingType: ProcessingTypeType
    processingUnit: ProcessingUnitType
    ephemeralStorageConfiguration: NotRequired[EphemeralStorageConfigurationTypeDef]
    command: NotRequired[list[str]]
    timeoutSeconds: NotRequired[int]
    environmentVariables: NotRequired[dict[str, str]]
    mounts: NotRequired[list[MountTypeDef]]

class ContainerTaskConfigurationTypeDef(TypedDict):
    ecrUri: str
    taskExecutionRole: str
    processingType: ProcessingTypeType
    processingUnit: ProcessingUnitType
    ephemeralStorageConfiguration: NotRequired[EphemeralStorageConfigurationTypeDef]
    command: NotRequired[Sequence[str]]
    timeoutSeconds: NotRequired[int]
    environmentVariables: NotRequired[Mapping[str, str]]
    mounts: NotRequired[Sequence[MountTypeDef]]

class MountOverridesOutputTypeDef(TypedDict):
    computeNodes: dict[str, list[MountTypeDef]]

class MountOverridesTypeDef(TypedDict):
    computeNodes: Mapping[str, Sequence[MountTypeDef]]

class ListAccessPoliciesResponseTypeDef(TypedDict):
    accessPolicySummaries: list[AccessPolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchGetAssetPropertyValueHistorySuccessEntryTypeDef(TypedDict):
    entryId: str
    assetPropertyValueHistory: list[AssetPropertyValueTypeDef]

class BatchGetAssetPropertyValueSuccessEntryTypeDef(TypedDict):
    entryId: str
    assetPropertyValue: NotRequired[AssetPropertyValueTypeDef]

class GetAssetPropertyValueHistoryResponseTypeDef(TypedDict):
    assetPropertyValueHistory: list[AssetPropertyValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetAssetPropertyValueResponseTypeDef(TypedDict):
    propertyValue: AssetPropertyValueTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutAssetPropertyValueEntryTypeDef(TypedDict):
    entryId: str
    propertyValues: Sequence[AssetPropertyValueTypeDef]
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]

class GetInterpolatedAssetPropertyValuesResponseTypeDef(TypedDict):
    interpolatedAssetPropertyValues: list[InterpolatedAssetPropertyValueTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPipelinesResponseTypeDef(TypedDict):
    pipelineSummaries: list[PipelineSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTasksResponseTypeDef(TypedDict):
    taskSummaries: list[TaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorkspacesResponseTypeDef(TypedDict):
    workspaceSummaries: list[WorkspaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PropertyTypeOutputTypeDef(TypedDict):
    attribute: NotRequired[AttributeTypeDef]
    measurement: NotRequired[MeasurementTypeDef]
    transform: NotRequired[TransformOutputTypeDef]
    metric: NotRequired[MetricOutputTypeDef]

ExpressionVariableUnionTypeDef = Union[ExpressionVariableTypeDef, ExpressionVariableOutputTypeDef]

class ListComputationModelDataBindingUsagesResponseTypeDef(TypedDict):
    dataBindingUsageSummaries: list[ComputationModelDataBindingUsageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateEnrichmentJobRequestTypeDef(TypedDict):
    workspaceName: str
    jobConfiguration: EnrichmentJobConfigurationTypeDef
    clientToken: NotRequired[str]

class DescribeEnrichmentJobResponseTypeDef(TypedDict):
    jobId: str
    status: EnrichmentJobStatusType
    workspaceName: str
    jobType: Literal["EVENT_DETECTION"]
    jobConfiguration: EnrichmentJobConfigurationTypeDef
    createdAt: datetime
    updatedAt: datetime
    completedAt: datetime
    cancelledAt: datetime
    failureMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

DescribeDatasetExportJobResponseTypeDef = TypedDict(
    "DescribeDatasetExportJobResponseTypeDef",
    {
        "jobId": str,
        "workspaceName": str,
        "status": DatasetExportJobStatusType,
        "startedAt": datetime,
        "completedAt": datetime,
        "destinationS3Uri": str,
        "errorReportLocation": ExportErrorReportLocationTypeDef,
        "input": ProcessingInputOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ProcessingInputUnionTypeDef = Union[ProcessingInputTypeDef, ProcessingInputOutputTypeDef]

class ListPipelineExecutionsResponseTypeDef(TypedDict):
    pipelineExecutionSummaries: list[PipelineExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class FileTypeDef(TypedDict):
    bucket: str
    key: str
    versionId: NotRequired[str]
    alias: NotRequired[str]
    startTime: NotRequired[TimeInNanosTypeDef]
    fileFormat: NotRequired[FileFormatUnionTypeDef]

JobConfigurationUnionTypeDef = Union[JobConfigurationTypeDef, JobConfigurationOutputTypeDef]

class ListAssetModelsResponseTypeDef(TypedDict):
    assetModelSummaries: list[AssetModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAssetsResponseTypeDef(TypedDict):
    assetSummaries: list[AssetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAssociatedAssetsResponseTypeDef(TypedDict):
    assetSummaries: list[AssociatedAssetsSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListComputationModelsResponseTypeDef(TypedDict):
    computationModelSummaries: list[ComputationModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListDatasetsResponseTypeDef(TypedDict):
    datasetSummaries: list[DatasetSummaryTypeDef]
    workspaceName: str
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CitationTypeDef(TypedDict):
    reference: NotRequired[ReferenceTypeDef]
    content: NotRequired[ContentTypeDef]

class TaskConfigurationOutputTypeDef(TypedDict):
    containerTaskConfiguration: NotRequired[ContainerTaskConfigurationOutputTypeDef]

class TaskConfigurationTypeDef(TypedDict):
    containerTaskConfiguration: NotRequired[ContainerTaskConfigurationTypeDef]

class DescribePipelineExecutionResponseTypeDef(TypedDict):
    pipelineExecutionId: str
    pipelineName: str
    workspaceName: str
    pipelineVersion: str
    status: PipelineExecutionStatusTypeDef
    startTime: datetime
    endTime: datetime
    requestEnvironmentVariables: ExecutionEnvironmentVariablesOutputTypeDef
    requestMountOverrides: MountOverridesOutputTypeDef
    executionPriority: int
    computeNodeExecutionDetails: list[ComputeNodeExecutionDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

MountOverridesUnionTypeDef = Union[MountOverridesTypeDef, MountOverridesOutputTypeDef]

class BatchGetAssetPropertyValueHistoryResponseTypeDef(TypedDict):
    errorEntries: list[BatchGetAssetPropertyValueHistoryErrorEntryTypeDef]
    successEntries: list[BatchGetAssetPropertyValueHistorySuccessEntryTypeDef]
    skippedEntries: list[BatchGetAssetPropertyValueHistorySkippedEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchGetAssetPropertyValueResponseTypeDef(TypedDict):
    errorEntries: list[BatchGetAssetPropertyValueErrorEntryTypeDef]
    successEntries: list[BatchGetAssetPropertyValueSuccessEntryTypeDef]
    skippedEntries: list[BatchGetAssetPropertyValueSkippedEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchPutAssetPropertyValueRequestTypeDef(TypedDict):
    entries: Sequence[PutAssetPropertyValueEntryTypeDef]
    enablePartialEntryProcessing: NotRequired[bool]

AssetModelPropertyOutputTypeDef = TypedDict(
    "AssetModelPropertyOutputTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeOutputTypeDef,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
        "path": NotRequired[list[AssetModelPropertyPathSegmentTypeDef]],
    },
)
AssetModelPropertySummaryTypeDef = TypedDict(
    "AssetModelPropertySummaryTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeOutputTypeDef,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
        "assetModelCompositeModelId": NotRequired[str],
        "path": NotRequired[list[AssetModelPropertyPathSegmentTypeDef]],
        "interfaceSummaries": NotRequired[list[InterfaceSummaryTypeDef]],
    },
)
PropertyTypeDef = TypedDict(
    "PropertyTypeDef",
    {
        "id": str,
        "name": str,
        "dataType": PropertyDataTypeType,
        "externalId": NotRequired[str],
        "alias": NotRequired[str],
        "notification": NotRequired[PropertyNotificationTypeDef],
        "unit": NotRequired[str],
        "type": NotRequired[PropertyTypeOutputTypeDef],
        "path": NotRequired[list[AssetPropertyPathSegmentTypeDef]],
    },
)

class MetricTypeDef(TypedDict):
    window: MetricWindowTypeDef
    expression: NotRequired[str]
    variables: NotRequired[Sequence[ExpressionVariableUnionTypeDef]]
    processingConfig: NotRequired[MetricProcessingConfigTypeDef]

class TransformTypeDef(TypedDict):
    expression: str
    variables: Sequence[ExpressionVariableUnionTypeDef]
    processingConfig: NotRequired[TransformProcessingConfigTypeDef]

CreateDatasetExportJobRequestTypeDef = TypedDict(
    "CreateDatasetExportJobRequestTypeDef",
    {
        "workspaceName": str,
        "destinationS3Uri": str,
        "input": ProcessingInputUnionTypeDef,
        "errorReportLocation": ExportErrorReportLocationTypeDef,
        "clientToken": NotRequired[str],
    },
)
FileUnionTypeDef = Union[FileTypeDef, FileOutputTypeDef]

class InvocationOutputTypeDef(TypedDict):
    message: NotRequired[str]
    citations: NotRequired[list[CitationTypeDef]]

class DescribeTaskResponseTypeDef(TypedDict):
    workspaceName: str
    taskName: str
    description: str
    taskArn: str
    version: str
    taskConfiguration: TaskConfigurationOutputTypeDef
    status: ResourceStatusTypeDef
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

TaskConfigurationUnionTypeDef = Union[TaskConfigurationTypeDef, TaskConfigurationOutputTypeDef]

class StartPipelineExecutionRequestTypeDef(TypedDict):
    workspaceName: str
    pipelineName: str
    executionEnvironmentVariableOverrides: NotRequired[ExecutionEnvironmentVariablesUnionTypeDef]
    executionMountOverrides: NotRequired[MountOverridesUnionTypeDef]
    executionPriority: NotRequired[int]
    clientToken: NotRequired[str]

AssetModelCompositeModelOutputTypeDef = TypedDict(
    "AssetModelCompositeModelOutputTypeDef",
    {
        "name": str,
        "type": str,
        "description": NotRequired[str],
        "properties": NotRequired[list[AssetModelPropertyOutputTypeDef]],
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)

class DescribeAssetModelCompositeModelResponseTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelId: str
    assetModelCompositeModelExternalId: str
    assetModelCompositeModelPath: list[AssetModelCompositeModelPathSegmentTypeDef]
    assetModelCompositeModelName: str
    assetModelCompositeModelDescription: str
    assetModelCompositeModelType: str
    assetModelCompositeModelProperties: list[AssetModelPropertyOutputTypeDef]
    compositionDetails: CompositionDetailsTypeDef
    assetModelCompositeModelSummaries: list[AssetModelCompositeModelSummaryTypeDef]
    actionDefinitions: list[ActionDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssetModelPropertiesResponseTypeDef(TypedDict):
    assetModelPropertySummaries: list[AssetModelPropertySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

CompositeModelPropertyTypeDef = TypedDict(
    "CompositeModelPropertyTypeDef",
    {
        "name": str,
        "type": str,
        "assetProperty": PropertyTypeDef,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)
MetricUnionTypeDef = Union[MetricTypeDef, MetricOutputTypeDef]
TransformUnionTypeDef = Union[TransformTypeDef, TransformOutputTypeDef]

class CreateBulkImportJobRequestTypeDef(TypedDict):
    jobName: str
    jobRoleArn: str
    files: Sequence[FileUnionTypeDef]
    errorReportLocation: ErrorReportLocationTypeDef
    jobConfiguration: NotRequired[JobConfigurationUnionTypeDef]
    adaptiveIngestion: NotRequired[bool]
    deleteFilesAfterImport: NotRequired[bool]
    datasetId: NotRequired[str]
    workspaceName: NotRequired[str]

class ResponseStreamTypeDef(TypedDict):
    trace: NotRequired[TraceTypeDef]
    output: NotRequired[InvocationOutputTypeDef]
    accessDeniedException: NotRequired[AccessDeniedExceptionTypeDef]
    conflictingOperationException: NotRequired[ConflictingOperationExceptionTypeDef]
    internalFailureException: NotRequired[InternalFailureExceptionTypeDef]
    invalidRequestException: NotRequired[InvalidRequestExceptionTypeDef]
    limitExceededException: NotRequired[LimitExceededExceptionTypeDef]
    resourceNotFoundException: NotRequired[ResourceNotFoundExceptionTypeDef]
    throttlingException: NotRequired[ThrottlingExceptionTypeDef]

class CreateTaskRequestTypeDef(TypedDict):
    workspaceName: str
    taskName: str
    taskConfiguration: TaskConfigurationUnionTypeDef
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]

class UpdateTaskRequestTypeDef(TypedDict):
    workspaceName: str
    taskName: str
    description: NotRequired[str]
    taskConfiguration: NotRequired[TaskConfigurationUnionTypeDef]

class DescribeAssetModelResponseTypeDef(TypedDict):
    assetModelId: str
    assetModelExternalId: str
    assetModelArn: str
    assetModelName: str
    assetModelType: AssetModelTypeType
    assetModelDescription: str
    assetModelProperties: list[AssetModelPropertyOutputTypeDef]
    assetModelHierarchies: list[AssetModelHierarchyTypeDef]
    assetModelCompositeModels: list[AssetModelCompositeModelOutputTypeDef]
    assetModelCompositeModelSummaries: list[AssetModelCompositeModelSummaryTypeDef]
    assetModelCreationDate: datetime
    assetModelLastUpdateDate: datetime
    assetModelStatus: AssetModelStatusTypeDef
    assetModelVersion: str
    interfaceDetails: list[InterfaceRelationshipTypeDef]
    eTag: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAssetPropertyResponseTypeDef(TypedDict):
    assetId: str
    assetExternalId: str
    assetName: str
    assetModelId: str
    assetProperty: PropertyTypeDef
    compositeModel: CompositeModelPropertyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PropertyTypeTypeDef(TypedDict):
    attribute: NotRequired[AttributeTypeDef]
    measurement: NotRequired[MeasurementTypeDef]
    transform: NotRequired[TransformUnionTypeDef]
    metric: NotRequired[MetricUnionTypeDef]

class InvokeAssistantResponseTypeDef(TypedDict):
    body: EventStream[ResponseStreamTypeDef]
    conversationId: str
    ResponseMetadata: ResponseMetadataTypeDef

PropertyTypeUnionTypeDef = Union[PropertyTypeTypeDef, PropertyTypeOutputTypeDef]
AssetModelPropertyDefinitionTypeDef = TypedDict(
    "AssetModelPropertyDefinitionTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeUnionTypeDef,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
    },
)
AssetModelPropertyTypeDef = TypedDict(
    "AssetModelPropertyTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeUnionTypeDef,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
        "path": NotRequired[Sequence[AssetModelPropertyPathSegmentTypeDef]],
    },
)
AssetModelCompositeModelDefinitionTypeDef = TypedDict(
    "AssetModelCompositeModelDefinitionTypeDef",
    {
        "name": str,
        "type": str,
        "id": NotRequired[str],
        "externalId": NotRequired[str],
        "description": NotRequired[str],
        "properties": NotRequired[Sequence[AssetModelPropertyDefinitionTypeDef]],
    },
)

class CreateAssetModelCompositeModelRequestTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelName: str
    assetModelCompositeModelType: str
    assetModelCompositeModelExternalId: NotRequired[str]
    parentAssetModelCompositeModelId: NotRequired[str]
    assetModelCompositeModelId: NotRequired[str]
    assetModelCompositeModelDescription: NotRequired[str]
    clientToken: NotRequired[str]
    composedAssetModelId: NotRequired[str]
    assetModelCompositeModelProperties: NotRequired[Sequence[AssetModelPropertyDefinitionTypeDef]]
    ifMatch: NotRequired[str]
    ifNoneMatch: NotRequired[str]
    matchForVersionType: NotRequired[AssetModelVersionTypeType]

AssetModelPropertyUnionTypeDef = Union[AssetModelPropertyTypeDef, AssetModelPropertyOutputTypeDef]

class CreateAssetModelRequestTypeDef(TypedDict):
    assetModelName: str
    assetModelType: NotRequired[AssetModelTypeType]
    assetModelId: NotRequired[str]
    assetModelExternalId: NotRequired[str]
    assetModelDescription: NotRequired[str]
    assetModelProperties: NotRequired[Sequence[AssetModelPropertyDefinitionTypeDef]]
    assetModelHierarchies: NotRequired[Sequence[AssetModelHierarchyDefinitionTypeDef]]
    assetModelCompositeModels: NotRequired[Sequence[AssetModelCompositeModelDefinitionTypeDef]]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

AssetModelCompositeModelTypeDef = TypedDict(
    "AssetModelCompositeModelTypeDef",
    {
        "name": str,
        "type": str,
        "description": NotRequired[str],
        "properties": NotRequired[Sequence[AssetModelPropertyUnionTypeDef]],
        "id": NotRequired[str],
        "externalId": NotRequired[str],
    },
)

class UpdateAssetModelCompositeModelRequestTypeDef(TypedDict):
    assetModelId: str
    assetModelCompositeModelId: str
    assetModelCompositeModelName: str
    assetModelCompositeModelExternalId: NotRequired[str]
    assetModelCompositeModelDescription: NotRequired[str]
    clientToken: NotRequired[str]
    assetModelCompositeModelProperties: NotRequired[Sequence[AssetModelPropertyUnionTypeDef]]
    ifMatch: NotRequired[str]
    ifNoneMatch: NotRequired[str]
    matchForVersionType: NotRequired[AssetModelVersionTypeType]

AssetModelCompositeModelUnionTypeDef = Union[
    AssetModelCompositeModelTypeDef, AssetModelCompositeModelOutputTypeDef
]

class UpdateAssetModelRequestTypeDef(TypedDict):
    assetModelId: str
    assetModelName: str
    assetModelExternalId: NotRequired[str]
    assetModelDescription: NotRequired[str]
    assetModelProperties: NotRequired[Sequence[AssetModelPropertyUnionTypeDef]]
    assetModelHierarchies: NotRequired[Sequence[AssetModelHierarchyTypeDef]]
    assetModelCompositeModels: NotRequired[Sequence[AssetModelCompositeModelUnionTypeDef]]
    clientToken: NotRequired[str]
    ifMatch: NotRequired[str]
    ifNoneMatch: NotRequired[str]
    matchForVersionType: NotRequired[AssetModelVersionTypeType]
