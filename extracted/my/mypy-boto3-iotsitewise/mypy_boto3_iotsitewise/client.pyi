"""
Type annotations for iotsitewise service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotsitewise.client import IoTSiteWiseClient

    session = Session()
    client: IoTSiteWiseClient = session.client("iotsitewise")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribePipelineExecutionPaginator,
    ExecuteQueryPaginator,
    GetAssetPropertyAggregatesPaginator,
    GetAssetPropertyValueHistoryPaginator,
    GetInterpolatedAssetPropertyValuesPaginator,
    GetQueryResultsPaginator,
    GetSearchResultsPaginator,
    ListAccessPoliciesPaginator,
    ListActionsPaginator,
    ListApplicationsPaginator,
    ListAssetModelCompositeModelsPaginator,
    ListAssetModelPropertiesPaginator,
    ListAssetModelsPaginator,
    ListAssetPropertiesPaginator,
    ListAssetRelationshipsPaginator,
    ListAssetsPaginator,
    ListAssociatedAssetsPaginator,
    ListBulkImportJobsPaginator,
    ListCompositionRelationshipsPaginator,
    ListComputationModelDataBindingUsagesPaginator,
    ListComputationModelResolveToResourcesPaginator,
    ListComputationModelsPaginator,
    ListDashboardsPaginator,
    ListDatasetDataSegmentRelationshipsPaginator,
    ListDatasetDataSegmentsPaginator,
    ListDatasetExportJobsPaginator,
    ListDatasetsPaginator,
    ListEnrichmentJobsPaginator,
    ListExecutionsPaginator,
    ListGatewaysPaginator,
    ListInterfaceRelationshipsPaginator,
    ListPipelineExecutionsPaginator,
    ListPipelinesPaginator,
    ListPortalsPaginator,
    ListProjectAssetsPaginator,
    ListProjectsPaginator,
    ListQueriesPaginator,
    ListSearchesPaginator,
    ListTasksPaginator,
    ListTimeSeriesPaginator,
    ListWorkspacesPaginator,
)
from .type_defs import (
    AssociateAssetsRequestTypeDef,
    AssociateTimeSeriesToAssetPropertyRequestTypeDef,
    BatchAssociateDataSegmentsToDatasetRequestTypeDef,
    BatchAssociateDataSegmentsToDatasetResponseTypeDef,
    BatchAssociateProjectAssetsRequestTypeDef,
    BatchAssociateProjectAssetsResponseTypeDef,
    BatchDeleteDatasetDataSegmentsRequestTypeDef,
    BatchDeleteDatasetDataSegmentsResponseTypeDef,
    BatchDisassociateDataSegmentsFromDatasetRequestTypeDef,
    BatchDisassociateDataSegmentsFromDatasetResponseTypeDef,
    BatchDisassociateProjectAssetsRequestTypeDef,
    BatchDisassociateProjectAssetsResponseTypeDef,
    BatchGetAssetPropertyAggregatesRequestTypeDef,
    BatchGetAssetPropertyAggregatesResponseTypeDef,
    BatchGetAssetPropertyValueHistoryRequestTypeDef,
    BatchGetAssetPropertyValueHistoryResponseTypeDef,
    BatchGetAssetPropertyValueRequestTypeDef,
    BatchGetAssetPropertyValueResponseTypeDef,
    BatchPutAssetPropertyValueRequestTypeDef,
    BatchPutAssetPropertyValueResponseTypeDef,
    CancelEnrichmentJobRequestTypeDef,
    CancelEnrichmentJobResponseTypeDef,
    CancelPipelineExecutionRequestTypeDef,
    CancelPipelineExecutionResponseTypeDef,
    CancelQueryRequestTypeDef,
    CancelQueryResponseTypeDef,
    CreateAccessPolicyRequestTypeDef,
    CreateAccessPolicyResponseTypeDef,
    CreateApplicationRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateAssetModelCompositeModelRequestTypeDef,
    CreateAssetModelCompositeModelResponseTypeDef,
    CreateAssetModelRequestTypeDef,
    CreateAssetModelResponseTypeDef,
    CreateAssetRequestTypeDef,
    CreateAssetResponseTypeDef,
    CreateBulkImportJobRequestTypeDef,
    CreateBulkImportJobResponseTypeDef,
    CreateComputationModelRequestTypeDef,
    CreateComputationModelResponseTypeDef,
    CreateDashboardRequestTypeDef,
    CreateDashboardResponseTypeDef,
    CreateDatasetExportJobRequestTypeDef,
    CreateDatasetExportJobResponseTypeDef,
    CreateDatasetRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateEnrichmentJobRequestTypeDef,
    CreateEnrichmentJobResponseTypeDef,
    CreateGatewayRequestTypeDef,
    CreateGatewayResponseTypeDef,
    CreatePipelineRequestTypeDef,
    CreatePipelineResponseTypeDef,
    CreatePortalRequestTypeDef,
    CreatePortalResponseTypeDef,
    CreateProjectRequestTypeDef,
    CreateProjectResponseTypeDef,
    CreateTaskRequestTypeDef,
    CreateTaskResponseTypeDef,
    CreateWorkspaceRequestTypeDef,
    CreateWorkspaceResponseTypeDef,
    DeleteAccessPolicyRequestTypeDef,
    DeleteApplicationRequestTypeDef,
    DeleteAssetModelCompositeModelRequestTypeDef,
    DeleteAssetModelCompositeModelResponseTypeDef,
    DeleteAssetModelInterfaceRelationshipRequestTypeDef,
    DeleteAssetModelInterfaceRelationshipResponseTypeDef,
    DeleteAssetModelRequestTypeDef,
    DeleteAssetModelResponseTypeDef,
    DeleteAssetRequestTypeDef,
    DeleteAssetResponseTypeDef,
    DeleteComputationModelRequestTypeDef,
    DeleteComputationModelResponseTypeDef,
    DeleteDashboardRequestTypeDef,
    DeleteDatasetRequestTypeDef,
    DeleteDatasetResponseTypeDef,
    DeleteGatewayRequestTypeDef,
    DeletePipelineRequestTypeDef,
    DeletePipelineResponseTypeDef,
    DeletePortalRequestTypeDef,
    DeletePortalResponseTypeDef,
    DeleteProjectRequestTypeDef,
    DeleteTaskRequestTypeDef,
    DeleteTaskResponseTypeDef,
    DeleteTimeSeriesRequestTypeDef,
    DeleteWorkspaceRequestTypeDef,
    DeleteWorkspaceResponseTypeDef,
    DescribeAccessPolicyRequestTypeDef,
    DescribeAccessPolicyResponseTypeDef,
    DescribeActionRequestTypeDef,
    DescribeActionResponseTypeDef,
    DescribeApplicationRequestTypeDef,
    DescribeApplicationResponseTypeDef,
    DescribeAssetCompositeModelRequestTypeDef,
    DescribeAssetCompositeModelResponseTypeDef,
    DescribeAssetModelCompositeModelRequestTypeDef,
    DescribeAssetModelCompositeModelResponseTypeDef,
    DescribeAssetModelInterfaceRelationshipRequestTypeDef,
    DescribeAssetModelInterfaceRelationshipResponseTypeDef,
    DescribeAssetModelRequestTypeDef,
    DescribeAssetModelResponseTypeDef,
    DescribeAssetPropertyRequestTypeDef,
    DescribeAssetPropertyResponseTypeDef,
    DescribeAssetRequestTypeDef,
    DescribeAssetResponseTypeDef,
    DescribeBulkImportJobRequestTypeDef,
    DescribeBulkImportJobResponseTypeDef,
    DescribeComputationModelExecutionSummaryRequestTypeDef,
    DescribeComputationModelExecutionSummaryResponseTypeDef,
    DescribeComputationModelRequestTypeDef,
    DescribeComputationModelResponseTypeDef,
    DescribeDashboardRequestTypeDef,
    DescribeDashboardResponseTypeDef,
    DescribeDatasetExportJobRequestTypeDef,
    DescribeDatasetExportJobResponseTypeDef,
    DescribeDatasetRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeDefaultEncryptionConfigurationResponseTypeDef,
    DescribeEnrichmentJobRequestTypeDef,
    DescribeEnrichmentJobResponseTypeDef,
    DescribeExecutionRequestTypeDef,
    DescribeExecutionResponseTypeDef,
    DescribeGatewayCapabilityConfigurationRequestTypeDef,
    DescribeGatewayCapabilityConfigurationResponseTypeDef,
    DescribeGatewayRequestTypeDef,
    DescribeGatewayResponseTypeDef,
    DescribeLoggingOptionsRequestTypeDef,
    DescribeLoggingOptionsResponseTypeDef,
    DescribePipelineExecutionRequestTypeDef,
    DescribePipelineExecutionResponseTypeDef,
    DescribePipelineRequestTypeDef,
    DescribePipelineResponseTypeDef,
    DescribePortalRequestTypeDef,
    DescribePortalResponseTypeDef,
    DescribeProjectRequestTypeDef,
    DescribeProjectResponseTypeDef,
    DescribeQueryRequestTypeDef,
    DescribeQueryResponseTypeDef,
    DescribeSearchRequestTypeDef,
    DescribeSearchResponseTypeDef,
    DescribeStorageConfigurationResponseTypeDef,
    DescribeTaskRequestTypeDef,
    DescribeTaskResponseTypeDef,
    DescribeTimeSeriesRequestTypeDef,
    DescribeTimeSeriesResponseTypeDef,
    DescribeWorkspaceRequestTypeDef,
    DescribeWorkspaceResponseTypeDef,
    DisassociateAssetsRequestTypeDef,
    DisassociateTimeSeriesFromAssetPropertyRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    ExecuteActionRequestTypeDef,
    ExecuteActionResponseTypeDef,
    ExecuteQueryRequestTypeDef,
    ExecuteQueryResponseTypeDef,
    GetAssetPropertyAggregatesRequestTypeDef,
    GetAssetPropertyAggregatesResponseTypeDef,
    GetAssetPropertyValueHistoryRequestTypeDef,
    GetAssetPropertyValueHistoryResponseTypeDef,
    GetAssetPropertyValueRequestTypeDef,
    GetAssetPropertyValueResponseTypeDef,
    GetCaptureDataRequestTypeDef,
    GetCaptureDataResponseTypeDef,
    GetInterpolatedAssetPropertyValuesRequestTypeDef,
    GetInterpolatedAssetPropertyValuesResponseTypeDef,
    GetQueryResultsRequestTypeDef,
    GetQueryResultsResponseTypeDef,
    GetSearchResultsRequestTypeDef,
    GetSearchResultsResponseTypeDef,
    InvokeAssistantRequestTypeDef,
    InvokeAssistantResponseTypeDef,
    ListAccessPoliciesRequestTypeDef,
    ListAccessPoliciesResponseTypeDef,
    ListActionsRequestTypeDef,
    ListActionsResponseTypeDef,
    ListApplicationsRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListAssetModelCompositeModelsRequestTypeDef,
    ListAssetModelCompositeModelsResponseTypeDef,
    ListAssetModelPropertiesRequestTypeDef,
    ListAssetModelPropertiesResponseTypeDef,
    ListAssetModelsRequestTypeDef,
    ListAssetModelsResponseTypeDef,
    ListAssetPropertiesRequestTypeDef,
    ListAssetPropertiesResponseTypeDef,
    ListAssetRelationshipsRequestTypeDef,
    ListAssetRelationshipsResponseTypeDef,
    ListAssetsRequestTypeDef,
    ListAssetsResponseTypeDef,
    ListAssociatedAssetsRequestTypeDef,
    ListAssociatedAssetsResponseTypeDef,
    ListBulkImportJobsRequestTypeDef,
    ListBulkImportJobsResponseTypeDef,
    ListCompositionRelationshipsRequestTypeDef,
    ListCompositionRelationshipsResponseTypeDef,
    ListComputationModelDataBindingUsagesRequestTypeDef,
    ListComputationModelDataBindingUsagesResponseTypeDef,
    ListComputationModelResolveToResourcesRequestTypeDef,
    ListComputationModelResolveToResourcesResponseTypeDef,
    ListComputationModelsRequestTypeDef,
    ListComputationModelsResponseTypeDef,
    ListDashboardsRequestTypeDef,
    ListDashboardsResponseTypeDef,
    ListDatasetDataSegmentRelationshipsRequestTypeDef,
    ListDatasetDataSegmentRelationshipsResponseTypeDef,
    ListDatasetDataSegmentsRequestTypeDef,
    ListDatasetDataSegmentsResponseTypeDef,
    ListDatasetExportJobsRequestTypeDef,
    ListDatasetExportJobsResponseTypeDef,
    ListDatasetsRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListEnrichmentJobsRequestTypeDef,
    ListEnrichmentJobsResponseTypeDef,
    ListExecutionsRequestTypeDef,
    ListExecutionsResponseTypeDef,
    ListGatewaysRequestTypeDef,
    ListGatewaysResponseTypeDef,
    ListInterfaceRelationshipsRequestTypeDef,
    ListInterfaceRelationshipsResponseTypeDef,
    ListPipelineExecutionsRequestTypeDef,
    ListPipelineExecutionsResponseTypeDef,
    ListPipelinesRequestTypeDef,
    ListPipelinesResponseTypeDef,
    ListPortalsRequestTypeDef,
    ListPortalsResponseTypeDef,
    ListProjectAssetsRequestTypeDef,
    ListProjectAssetsResponseTypeDef,
    ListProjectsRequestTypeDef,
    ListProjectsResponseTypeDef,
    ListQueriesRequestTypeDef,
    ListQueriesResponseTypeDef,
    ListSearchesRequestTypeDef,
    ListSearchesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTasksRequestTypeDef,
    ListTasksResponseTypeDef,
    ListTimeSeriesRequestTypeDef,
    ListTimeSeriesResponseTypeDef,
    ListWorkspacesRequestTypeDef,
    ListWorkspacesResponseTypeDef,
    PutAssetModelInterfaceRelationshipRequestTypeDef,
    PutAssetModelInterfaceRelationshipResponseTypeDef,
    PutDefaultEncryptionConfigurationRequestTypeDef,
    PutDefaultEncryptionConfigurationResponseTypeDef,
    PutLoggingOptionsRequestTypeDef,
    PutStorageConfigurationRequestTypeDef,
    PutStorageConfigurationResponseTypeDef,
    StartPipelineExecutionRequestTypeDef,
    StartPipelineExecutionResponseTypeDef,
    StartQueryRequestTypeDef,
    StartQueryResponseTypeDef,
    StartSearchRequestTypeDef,
    StartSearchResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAccessPolicyRequestTypeDef,
    UpdateAssetModelCompositeModelRequestTypeDef,
    UpdateAssetModelCompositeModelResponseTypeDef,
    UpdateAssetModelRequestTypeDef,
    UpdateAssetModelResponseTypeDef,
    UpdateAssetPropertyRequestTypeDef,
    UpdateAssetRequestTypeDef,
    UpdateAssetResponseTypeDef,
    UpdateComputationModelRequestTypeDef,
    UpdateComputationModelResponseTypeDef,
    UpdateDashboardRequestTypeDef,
    UpdateDatasetRequestTypeDef,
    UpdateDatasetResponseTypeDef,
    UpdateGatewayCapabilityConfigurationRequestTypeDef,
    UpdateGatewayCapabilityConfigurationResponseTypeDef,
    UpdateGatewayRequestTypeDef,
    UpdatePipelineRequestTypeDef,
    UpdatePipelineResponseTypeDef,
    UpdatePortalRequestTypeDef,
    UpdatePortalResponseTypeDef,
    UpdateProjectRequestTypeDef,
    UpdateTaskRequestTypeDef,
    UpdateTaskResponseTypeDef,
    UpdateWorkspaceRequestTypeDef,
    UpdateWorkspaceResponseTypeDef,
)
from .waiter import (
    AssetActiveWaiter,
    AssetModelActiveWaiter,
    AssetModelNotExistsWaiter,
    AssetNotExistsWaiter,
    PortalActiveWaiter,
    PortalNotExistsWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("IoTSiteWiseClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictingOperationException: type[BotocoreClientError]
    InternalFailureException: type[BotocoreClientError]
    InvalidRequestException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    PreconditionFailedException: type[BotocoreClientError]
    QueryTimeoutException: type[BotocoreClientError]
    ResourceAlreadyExistsException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceUnavailableException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    TooManyTagsException: type[BotocoreClientError]
    UnauthorizedException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class IoTSiteWiseClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTSiteWiseClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/can_paginate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/generate_presigned_url.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#generate_presigned_url)
        """

    def associate_assets(
        self, **kwargs: Unpack[AssociateAssetsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates a child asset with the given parent asset through a hierarchy
        defined in the parent asset's model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/associate_assets.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#associate_assets)
        """

    def associate_time_series_to_asset_property(
        self, **kwargs: Unpack[AssociateTimeSeriesToAssetPropertyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates a time series (data stream) with an asset property.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/associate_time_series_to_asset_property.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#associate_time_series_to_asset_property)
        """

    def batch_associate_data_segments_to_dataset(
        self, **kwargs: Unpack[BatchAssociateDataSegmentsToDatasetRequestTypeDef]
    ) -> BatchAssociateDataSegmentsToDatasetResponseTypeDef:
        """
        Associates a batch of data segments with a curated dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/batch_associate_data_segments_to_dataset.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#batch_associate_data_segments_to_dataset)
        """

    def batch_associate_project_assets(
        self, **kwargs: Unpack[BatchAssociateProjectAssetsRequestTypeDef]
    ) -> BatchAssociateProjectAssetsResponseTypeDef:
        """
        The IoT SiteWise Monitor feature will no longer be open to new customers
        starting November 7, 2025.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/batch_associate_project_assets.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#batch_associate_project_assets)
        """

    def batch_delete_dataset_data_segments(
        self, **kwargs: Unpack[BatchDeleteDatasetDataSegmentsRequestTypeDef]
    ) -> BatchDeleteDatasetDataSegmentsResponseTypeDef:
        """
        Deletes a batch of data segments from a session dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/batch_delete_dataset_data_segments.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#batch_delete_dataset_data_segments)
        """

    def batch_disassociate_data_segments_from_dataset(
        self, **kwargs: Unpack[BatchDisassociateDataSegmentsFromDatasetRequestTypeDef]
    ) -> BatchDisassociateDataSegmentsFromDatasetResponseTypeDef:
        """
        Disassociates a batch of data segments from a curated dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/batch_disassociate_data_segments_from_dataset.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#batch_disassociate_data_segments_from_dataset)
        """

    def batch_disassociate_project_assets(
        self, **kwargs: Unpack[BatchDisassociateProjectAssetsRequestTypeDef]
    ) -> BatchDisassociateProjectAssetsResponseTypeDef:
        """
        Disassociates a group (batch) of assets from an IoT SiteWise Monitor project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/batch_disassociate_project_assets.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#batch_disassociate_project_assets)
        """

    def batch_get_asset_property_aggregates(
        self, **kwargs: Unpack[BatchGetAssetPropertyAggregatesRequestTypeDef]
    ) -> BatchGetAssetPropertyAggregatesResponseTypeDef:
        """
        Gets aggregated values (for example, average, minimum, and maximum) for one or
        more asset properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/batch_get_asset_property_aggregates.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#batch_get_asset_property_aggregates)
        """

    def batch_get_asset_property_value(
        self, **kwargs: Unpack[BatchGetAssetPropertyValueRequestTypeDef]
    ) -> BatchGetAssetPropertyValueResponseTypeDef:
        """
        Gets the current value for one or more asset properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/batch_get_asset_property_value.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#batch_get_asset_property_value)
        """

    def batch_get_asset_property_value_history(
        self, **kwargs: Unpack[BatchGetAssetPropertyValueHistoryRequestTypeDef]
    ) -> BatchGetAssetPropertyValueHistoryResponseTypeDef:
        """
        Gets the historical values for one or more asset properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/batch_get_asset_property_value_history.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#batch_get_asset_property_value_history)
        """

    def batch_put_asset_property_value(
        self, **kwargs: Unpack[BatchPutAssetPropertyValueRequestTypeDef]
    ) -> BatchPutAssetPropertyValueResponseTypeDef:
        """
        Sends a list of asset property values to IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/batch_put_asset_property_value.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#batch_put_asset_property_value)
        """

    def cancel_enrichment_job(
        self, **kwargs: Unpack[CancelEnrichmentJobRequestTypeDef]
    ) -> CancelEnrichmentJobResponseTypeDef:
        """
        Cancels a running or pending enrichment job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/cancel_enrichment_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#cancel_enrichment_job)
        """

    def cancel_pipeline_execution(
        self, **kwargs: Unpack[CancelPipelineExecutionRequestTypeDef]
    ) -> CancelPipelineExecutionResponseTypeDef:
        """
        Cancels a pipeline execution in the specified workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/cancel_pipeline_execution.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#cancel_pipeline_execution)
        """

    def cancel_query(
        self, **kwargs: Unpack[CancelQueryRequestTypeDef]
    ) -> CancelQueryResponseTypeDef:
        """
        Cancels a running query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/cancel_query.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#cancel_query)
        """

    def create_access_policy(
        self, **kwargs: Unpack[CreateAccessPolicyRequestTypeDef]
    ) -> CreateAccessPolicyResponseTypeDef:
        """
        The IoT SiteWise Monitor feature will no longer be open to new customers
        starting November 7, 2025.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_access_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_access_policy)
        """

    def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestTypeDef]
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates a new application for the workspace and IdC application provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_application.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_application)
        """

    def create_asset(
        self, **kwargs: Unpack[CreateAssetRequestTypeDef]
    ) -> CreateAssetResponseTypeDef:
        """
        Creates an asset from an existing asset model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_asset.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_asset)
        """

    def create_asset_model(
        self, **kwargs: Unpack[CreateAssetModelRequestTypeDef]
    ) -> CreateAssetModelResponseTypeDef:
        """
        Creates an asset model from specified property and hierarchy definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_asset_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_asset_model)
        """

    def create_asset_model_composite_model(
        self, **kwargs: Unpack[CreateAssetModelCompositeModelRequestTypeDef]
    ) -> CreateAssetModelCompositeModelResponseTypeDef:
        """
        Creates a custom composite model from specified property and hierarchy
        definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_asset_model_composite_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_asset_model_composite_model)
        """

    def create_bulk_import_job(
        self, **kwargs: Unpack[CreateBulkImportJobRequestTypeDef]
    ) -> CreateBulkImportJobResponseTypeDef:
        """
        Defines a job to ingest data to IoT SiteWise from Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_bulk_import_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_bulk_import_job)
        """

    def create_computation_model(
        self, **kwargs: Unpack[CreateComputationModelRequestTypeDef]
    ) -> CreateComputationModelResponseTypeDef:
        """
        Create a computation model with a configuration and data binding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_computation_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_computation_model)
        """

    def create_dashboard(
        self, **kwargs: Unpack[CreateDashboardRequestTypeDef]
    ) -> CreateDashboardResponseTypeDef:
        """
        The IoT SiteWise Monitor feature will no longer be open to new customers
        starting November 7, 2025.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_dashboard.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_dashboard)
        """

    def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_dataset.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_dataset)
        """

    def create_dataset_export_job(
        self, **kwargs: Unpack[CreateDatasetExportJobRequestTypeDef]
    ) -> CreateDatasetExportJobResponseTypeDef:
        """
        Starts an asynchronous job that exports dataset and time-series data from a
        workspace to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_dataset_export_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_dataset_export_job)
        """

    def create_enrichment_job(
        self, **kwargs: Unpack[CreateEnrichmentJobRequestTypeDef]
    ) -> CreateEnrichmentJobResponseTypeDef:
        """
        Creates an asynchronous enrichment job to analyze time-series sensor data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_enrichment_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_enrichment_job)
        """

    def create_gateway(
        self, **kwargs: Unpack[CreateGatewayRequestTypeDef]
    ) -> CreateGatewayResponseTypeDef:
        """
        Creates a gateway, which is a virtual or edge device that delivers industrial
        data streams from local servers to IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_gateway.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_gateway)
        """

    def create_pipeline(
        self, **kwargs: Unpack[CreatePipelineRequestTypeDef]
    ) -> CreatePipelineResponseTypeDef:
        """
        Creates a new pipeline in the specified workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_pipeline.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_pipeline)
        """

    def create_portal(
        self, **kwargs: Unpack[CreatePortalRequestTypeDef]
    ) -> CreatePortalResponseTypeDef:
        """
        The IoT SiteWise Monitor feature will no longer be open to new customers
        starting November 7, 2025.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_portal.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_portal)
        """

    def create_project(
        self, **kwargs: Unpack[CreateProjectRequestTypeDef]
    ) -> CreateProjectResponseTypeDef:
        """
        The IoT SiteWise Monitor feature will no longer be open to new customers
        starting November 7, 2025.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_project.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_project)
        """

    def create_task(self, **kwargs: Unpack[CreateTaskRequestTypeDef]) -> CreateTaskResponseTypeDef:
        """
        Creates a new task in the specified workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_task.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_task)
        """

    def create_workspace(
        self, **kwargs: Unpack[CreateWorkspaceRequestTypeDef]
    ) -> CreateWorkspaceResponseTypeDef:
        """
        Creates a workspace in IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/create_workspace.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#create_workspace)
        """

    def delete_access_policy(
        self, **kwargs: Unpack[DeleteAccessPolicyRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an access policy that grants the specified identity access to the
        specified IoT SiteWise Monitor resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_access_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_access_policy)
        """

    def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an application by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_application.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_application)
        """

    def delete_asset(
        self, **kwargs: Unpack[DeleteAssetRequestTypeDef]
    ) -> DeleteAssetResponseTypeDef:
        """
        Deletes an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_asset.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_asset)
        """

    def delete_asset_model(
        self, **kwargs: Unpack[DeleteAssetModelRequestTypeDef]
    ) -> DeleteAssetModelResponseTypeDef:
        """
        Deletes an asset model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_asset_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_asset_model)
        """

    def delete_asset_model_composite_model(
        self, **kwargs: Unpack[DeleteAssetModelCompositeModelRequestTypeDef]
    ) -> DeleteAssetModelCompositeModelResponseTypeDef:
        """
        Deletes a composite model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_asset_model_composite_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_asset_model_composite_model)
        """

    def delete_asset_model_interface_relationship(
        self, **kwargs: Unpack[DeleteAssetModelInterfaceRelationshipRequestTypeDef]
    ) -> DeleteAssetModelInterfaceRelationshipResponseTypeDef:
        """
        Deletes an interface relationship between an asset model and an interface asset
        model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_asset_model_interface_relationship.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_asset_model_interface_relationship)
        """

    def delete_computation_model(
        self, **kwargs: Unpack[DeleteComputationModelRequestTypeDef]
    ) -> DeleteComputationModelResponseTypeDef:
        """
        Deletes a computation model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_computation_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_computation_model)
        """

    def delete_dashboard(self, **kwargs: Unpack[DeleteDashboardRequestTypeDef]) -> dict[str, Any]:
        """
        Deletes a dashboard from IoT SiteWise Monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_dashboard.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_dashboard)
        """

    def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestTypeDef]
    ) -> DeleteDatasetResponseTypeDef:
        """
        Deletes a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_dataset.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_dataset)
        """

    def delete_gateway(
        self, **kwargs: Unpack[DeleteGatewayRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a gateway from IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_gateway.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_gateway)
        """

    def delete_pipeline(
        self, **kwargs: Unpack[DeletePipelineRequestTypeDef]
    ) -> DeletePipelineResponseTypeDef:
        """
        Deletes a pipeline from the specified workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_pipeline.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_pipeline)
        """

    def delete_portal(
        self, **kwargs: Unpack[DeletePortalRequestTypeDef]
    ) -> DeletePortalResponseTypeDef:
        """
        Deletes a portal from IoT SiteWise Monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_portal.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_portal)
        """

    def delete_project(self, **kwargs: Unpack[DeleteProjectRequestTypeDef]) -> dict[str, Any]:
        """
        Deletes a project from IoT SiteWise Monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_project.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_project)
        """

    def delete_task(self, **kwargs: Unpack[DeleteTaskRequestTypeDef]) -> DeleteTaskResponseTypeDef:
        """
        Deletes a task from the specified workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_task.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_task)
        """

    def delete_time_series(
        self, **kwargs: Unpack[DeleteTimeSeriesRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a time series (data stream).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_time_series.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_time_series)
        """

    def delete_workspace(
        self, **kwargs: Unpack[DeleteWorkspaceRequestTypeDef]
    ) -> DeleteWorkspaceResponseTypeDef:
        """
        Deletes a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/delete_workspace.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#delete_workspace)
        """

    def describe_access_policy(
        self, **kwargs: Unpack[DescribeAccessPolicyRequestTypeDef]
    ) -> DescribeAccessPolicyResponseTypeDef:
        """
        Describes an access policy, which specifies an identity's access to an IoT
        SiteWise Monitor portal or project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_access_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_access_policy)
        """

    def describe_action(
        self, **kwargs: Unpack[DescribeActionRequestTypeDef]
    ) -> DescribeActionResponseTypeDef:
        """
        Retrieves information about an action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_action.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_action)
        """

    def describe_application(
        self, **kwargs: Unpack[DescribeApplicationRequestTypeDef]
    ) -> DescribeApplicationResponseTypeDef:
        """
        Retrieves Application details based on the ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_application.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_application)
        """

    def describe_asset(
        self, **kwargs: Unpack[DescribeAssetRequestTypeDef]
    ) -> DescribeAssetResponseTypeDef:
        """
        Retrieves information about an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_asset.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_asset)
        """

    def describe_asset_composite_model(
        self, **kwargs: Unpack[DescribeAssetCompositeModelRequestTypeDef]
    ) -> DescribeAssetCompositeModelResponseTypeDef:
        """
        Retrieves information about an asset composite model (also known as an asset
        component).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_asset_composite_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_asset_composite_model)
        """

    def describe_asset_model(
        self, **kwargs: Unpack[DescribeAssetModelRequestTypeDef]
    ) -> DescribeAssetModelResponseTypeDef:
        """
        Retrieves information about an asset model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_asset_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_asset_model)
        """

    def describe_asset_model_composite_model(
        self, **kwargs: Unpack[DescribeAssetModelCompositeModelRequestTypeDef]
    ) -> DescribeAssetModelCompositeModelResponseTypeDef:
        """
        Retrieves information about an asset model composite model (also known as an
        asset model component).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_asset_model_composite_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_asset_model_composite_model)
        """

    def describe_asset_model_interface_relationship(
        self, **kwargs: Unpack[DescribeAssetModelInterfaceRelationshipRequestTypeDef]
    ) -> DescribeAssetModelInterfaceRelationshipResponseTypeDef:
        """
        Retrieves information about an interface relationship between an asset model
        and an interface asset model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_asset_model_interface_relationship.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_asset_model_interface_relationship)
        """

    def describe_asset_property(
        self, **kwargs: Unpack[DescribeAssetPropertyRequestTypeDef]
    ) -> DescribeAssetPropertyResponseTypeDef:
        """
        Retrieves information about an asset property.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_asset_property.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_asset_property)
        """

    def describe_bulk_import_job(
        self, **kwargs: Unpack[DescribeBulkImportJobRequestTypeDef]
    ) -> DescribeBulkImportJobResponseTypeDef:
        """
        Retrieves information about a bulk import job request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_bulk_import_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_bulk_import_job)
        """

    def describe_computation_model(
        self, **kwargs: Unpack[DescribeComputationModelRequestTypeDef]
    ) -> DescribeComputationModelResponseTypeDef:
        """
        Retrieves information about a computation model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_computation_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_computation_model)
        """

    def describe_computation_model_execution_summary(
        self, **kwargs: Unpack[DescribeComputationModelExecutionSummaryRequestTypeDef]
    ) -> DescribeComputationModelExecutionSummaryResponseTypeDef:
        """
        Retrieves information about the execution summary of a computation model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_computation_model_execution_summary.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_computation_model_execution_summary)
        """

    def describe_dashboard(
        self, **kwargs: Unpack[DescribeDashboardRequestTypeDef]
    ) -> DescribeDashboardResponseTypeDef:
        """
        Retrieves information about a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_dashboard.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_dashboard)
        """

    def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        Retrieves information about a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_dataset.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_dataset)
        """

    def describe_dataset_export_job(
        self, **kwargs: Unpack[DescribeDatasetExportJobRequestTypeDef]
    ) -> DescribeDatasetExportJobResponseTypeDef:
        """
        Retrieves information about a dataset export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_dataset_export_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_dataset_export_job)
        """

    def describe_default_encryption_configuration(
        self,
    ) -> DescribeDefaultEncryptionConfigurationResponseTypeDef:
        """
        Retrieves information about the default encryption configuration for the Amazon
        Web Services account in the default or specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_default_encryption_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_default_encryption_configuration)
        """

    def describe_enrichment_job(
        self, **kwargs: Unpack[DescribeEnrichmentJobRequestTypeDef]
    ) -> DescribeEnrichmentJobResponseTypeDef:
        """
        Retrieves detailed information about a specific enrichment job, including its
        current status, configuration, and timestamps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_enrichment_job.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_enrichment_job)
        """

    def describe_execution(
        self, **kwargs: Unpack[DescribeExecutionRequestTypeDef]
    ) -> DescribeExecutionResponseTypeDef:
        """
        Retrieves information about the execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_execution.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_execution)
        """

    def describe_gateway(
        self, **kwargs: Unpack[DescribeGatewayRequestTypeDef]
    ) -> DescribeGatewayResponseTypeDef:
        """
        Retrieves information about a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_gateway.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_gateway)
        """

    def describe_gateway_capability_configuration(
        self, **kwargs: Unpack[DescribeGatewayCapabilityConfigurationRequestTypeDef]
    ) -> DescribeGatewayCapabilityConfigurationResponseTypeDef:
        """
        Each gateway capability defines data sources for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_gateway_capability_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_gateway_capability_configuration)
        """

    def describe_logging_options(
        self, **kwargs: Unpack[DescribeLoggingOptionsRequestTypeDef]
    ) -> DescribeLoggingOptionsResponseTypeDef:
        """
        Retrieves the current IoT SiteWise logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_logging_options.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_logging_options)
        """

    def describe_pipeline(
        self, **kwargs: Unpack[DescribePipelineRequestTypeDef]
    ) -> DescribePipelineResponseTypeDef:
        """
        Retrieves detailed information about a specific pipeline in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_pipeline.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_pipeline)
        """

    def describe_pipeline_execution(
        self, **kwargs: Unpack[DescribePipelineExecutionRequestTypeDef]
    ) -> DescribePipelineExecutionResponseTypeDef:
        """
        Retrieves detailed information about a specific pipeline execution, including
        the overall execution status and the status of each individual compute node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_pipeline_execution.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_pipeline_execution)
        """

    def describe_portal(
        self, **kwargs: Unpack[DescribePortalRequestTypeDef]
    ) -> DescribePortalResponseTypeDef:
        """
        Retrieves information about a portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_portal.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_portal)
        """

    def describe_project(
        self, **kwargs: Unpack[DescribeProjectRequestTypeDef]
    ) -> DescribeProjectResponseTypeDef:
        """
        Retrieves information about a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_project.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_project)
        """

    def describe_query(
        self, **kwargs: Unpack[DescribeQueryRequestTypeDef]
    ) -> DescribeQueryResponseTypeDef:
        """
        Retrieves information about a query, including its status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_query.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_query)
        """

    def describe_search(
        self, **kwargs: Unpack[DescribeSearchRequestTypeDef]
    ) -> DescribeSearchResponseTypeDef:
        """
        Returns the current status and metadata of a single search, including the query
        that was submitted, the search type, and — when the search has failed — the
        reason.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_search.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_search)
        """

    def describe_storage_configuration(self) -> DescribeStorageConfigurationResponseTypeDef:
        """
        Retrieves information about the storage configuration for IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_storage_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_storage_configuration)
        """

    def describe_task(
        self, **kwargs: Unpack[DescribeTaskRequestTypeDef]
    ) -> DescribeTaskResponseTypeDef:
        """
        Retrieves detailed information about a specific task in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_task.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_task)
        """

    def describe_time_series(
        self, **kwargs: Unpack[DescribeTimeSeriesRequestTypeDef]
    ) -> DescribeTimeSeriesResponseTypeDef:
        """
        Retrieves information about a time series (data stream).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_time_series.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_time_series)
        """

    def describe_workspace(
        self, **kwargs: Unpack[DescribeWorkspaceRequestTypeDef]
    ) -> DescribeWorkspaceResponseTypeDef:
        """
        Retrieves information about a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/describe_workspace.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#describe_workspace)
        """

    def disassociate_assets(
        self, **kwargs: Unpack[DisassociateAssetsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates a child asset from the given parent asset through a hierarchy
        defined in the parent asset's model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/disassociate_assets.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#disassociate_assets)
        """

    def disassociate_time_series_from_asset_property(
        self, **kwargs: Unpack[DisassociateTimeSeriesFromAssetPropertyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates a time series (data stream) from an asset property.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/disassociate_time_series_from_asset_property.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#disassociate_time_series_from_asset_property)
        """

    def execute_action(
        self, **kwargs: Unpack[ExecuteActionRequestTypeDef]
    ) -> ExecuteActionResponseTypeDef:
        """
        Executes an action on a target resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/execute_action.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#execute_action)
        """

    def execute_query(
        self, **kwargs: Unpack[ExecuteQueryRequestTypeDef]
    ) -> ExecuteQueryResponseTypeDef:
        """
        Run SQL queries to retrieve metadata and time-series data from asset models,
        assets, measurements, metrics, transforms, and aggregates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/execute_query.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#execute_query)
        """

    def get_asset_property_aggregates(
        self, **kwargs: Unpack[GetAssetPropertyAggregatesRequestTypeDef]
    ) -> GetAssetPropertyAggregatesResponseTypeDef:
        """
        Gets aggregated values for an asset property.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_asset_property_aggregates.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_asset_property_aggregates)
        """

    def get_asset_property_value(
        self, **kwargs: Unpack[GetAssetPropertyValueRequestTypeDef]
    ) -> GetAssetPropertyValueResponseTypeDef:
        """
        Gets an asset property's current value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_asset_property_value.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_asset_property_value)
        """

    def get_asset_property_value_history(
        self, **kwargs: Unpack[GetAssetPropertyValueHistoryRequestTypeDef]
    ) -> GetAssetPropertyValueHistoryResponseTypeDef:
        """
        Gets the history of an asset property's values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_asset_property_value_history.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_asset_property_value_history)
        """

    def get_capture_data(
        self, **kwargs: Unpack[GetCaptureDataRequestTypeDef]
    ) -> GetCaptureDataResponseTypeDef:
        """
        Retrieves video data for a specific time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_capture_data.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_capture_data)
        """

    def get_interpolated_asset_property_values(
        self, **kwargs: Unpack[GetInterpolatedAssetPropertyValuesRequestTypeDef]
    ) -> GetInterpolatedAssetPropertyValuesResponseTypeDef:
        """
        Get interpolated values for an asset property for a specified time interval,
        during a period of time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_interpolated_asset_property_values.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_interpolated_asset_property_values)
        """

    def get_query_results(
        self, **kwargs: Unpack[GetQueryResultsRequestTypeDef]
    ) -> GetQueryResultsResponseTypeDef:
        """
        Retrieves the paginated results of a query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_query_results.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_query_results)
        """

    def get_search_results(
        self, **kwargs: Unpack[GetSearchResultsRequestTypeDef]
    ) -> GetSearchResultsResponseTypeDef:
        """
        Retrieves the ranked results of a search, ordered by descending relevance score.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_search_results.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_search_results)
        """

    def invoke_assistant(
        self, **kwargs: Unpack[InvokeAssistantRequestTypeDef]
    ) -> InvokeAssistantResponseTypeDef:
        """
        Invokes SiteWise Assistant to start or continue a conversation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/invoke_assistant.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#invoke_assistant)
        """

    def list_access_policies(
        self, **kwargs: Unpack[ListAccessPoliciesRequestTypeDef]
    ) -> ListAccessPoliciesResponseTypeDef:
        """
        Retrieves a paginated list of access policies for an identity (an IAM Identity
        Center user, an IAM Identity Center group, or an IAM user) or an IoT SiteWise
        Monitor resource (a portal or project).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_access_policies.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_access_policies)
        """

    def list_actions(
        self, **kwargs: Unpack[ListActionsRequestTypeDef]
    ) -> ListActionsResponseTypeDef:
        """
        Retrieves a paginated list of actions for a specific target resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_actions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_actions)
        """

    def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Retrieves a paginated list of existing applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_applications.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_applications)
        """

    def list_asset_model_composite_models(
        self, **kwargs: Unpack[ListAssetModelCompositeModelsRequestTypeDef]
    ) -> ListAssetModelCompositeModelsResponseTypeDef:
        """
        Retrieves a paginated list of composite models associated with the asset model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_asset_model_composite_models.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_asset_model_composite_models)
        """

    def list_asset_model_properties(
        self, **kwargs: Unpack[ListAssetModelPropertiesRequestTypeDef]
    ) -> ListAssetModelPropertiesResponseTypeDef:
        """
        Retrieves a paginated list of properties associated with an asset model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_asset_model_properties.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_asset_model_properties)
        """

    def list_asset_models(
        self, **kwargs: Unpack[ListAssetModelsRequestTypeDef]
    ) -> ListAssetModelsResponseTypeDef:
        """
        Retrieves a paginated list of summaries of all asset models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_asset_models.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_asset_models)
        """

    def list_asset_properties(
        self, **kwargs: Unpack[ListAssetPropertiesRequestTypeDef]
    ) -> ListAssetPropertiesResponseTypeDef:
        """
        Retrieves a paginated list of properties associated with an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_asset_properties.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_asset_properties)
        """

    def list_asset_relationships(
        self, **kwargs: Unpack[ListAssetRelationshipsRequestTypeDef]
    ) -> ListAssetRelationshipsResponseTypeDef:
        """
        Retrieves a paginated list of asset relationships for an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_asset_relationships.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_asset_relationships)
        """

    def list_assets(self, **kwargs: Unpack[ListAssetsRequestTypeDef]) -> ListAssetsResponseTypeDef:
        """
        Retrieves a paginated list of asset summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_assets.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_assets)
        """

    def list_associated_assets(
        self, **kwargs: Unpack[ListAssociatedAssetsRequestTypeDef]
    ) -> ListAssociatedAssetsResponseTypeDef:
        """
        Retrieves a paginated list of associated assets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_associated_assets.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_associated_assets)
        """

    def list_bulk_import_jobs(
        self, **kwargs: Unpack[ListBulkImportJobsRequestTypeDef]
    ) -> ListBulkImportJobsResponseTypeDef:
        """
        Retrieves a paginated list of bulk import job requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_bulk_import_jobs.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_bulk_import_jobs)
        """

    def list_composition_relationships(
        self, **kwargs: Unpack[ListCompositionRelationshipsRequestTypeDef]
    ) -> ListCompositionRelationshipsResponseTypeDef:
        """
        Retrieves a paginated list of composition relationships for an asset model of
        type <code>COMPONENT_MODEL</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_composition_relationships.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_composition_relationships)
        """

    def list_computation_model_data_binding_usages(
        self, **kwargs: Unpack[ListComputationModelDataBindingUsagesRequestTypeDef]
    ) -> ListComputationModelDataBindingUsagesResponseTypeDef:
        """
        Lists all data binding usages for computation models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_computation_model_data_binding_usages.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_computation_model_data_binding_usages)
        """

    def list_computation_model_resolve_to_resources(
        self, **kwargs: Unpack[ListComputationModelResolveToResourcesRequestTypeDef]
    ) -> ListComputationModelResolveToResourcesResponseTypeDef:
        """
        Lists all distinct resources that are resolved from the executed actions of the
        computation model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_computation_model_resolve_to_resources.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_computation_model_resolve_to_resources)
        """

    def list_computation_models(
        self, **kwargs: Unpack[ListComputationModelsRequestTypeDef]
    ) -> ListComputationModelsResponseTypeDef:
        """
        Retrieves a paginated list of summaries of all computation models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_computation_models.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_computation_models)
        """

    def list_dashboards(
        self, **kwargs: Unpack[ListDashboardsRequestTypeDef]
    ) -> ListDashboardsResponseTypeDef:
        """
        Retrieves a paginated list of dashboards for an IoT SiteWise Monitor project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_dashboards.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_dashboards)
        """

    def list_dataset_data_segment_relationships(
        self, **kwargs: Unpack[ListDatasetDataSegmentRelationshipsRequestTypeDef]
    ) -> ListDatasetDataSegmentRelationshipsResponseTypeDef:
        """
        Retrieves a paginated list of data segment relationships for a session dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_dataset_data_segment_relationships.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_dataset_data_segment_relationships)
        """

    def list_dataset_data_segments(
        self, **kwargs: Unpack[ListDatasetDataSegmentsRequestTypeDef]
    ) -> ListDatasetDataSegmentsResponseTypeDef:
        """
        Retrieves a paginated list of data segments associated with a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_dataset_data_segments.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_dataset_data_segments)
        """

    def list_dataset_export_jobs(
        self, **kwargs: Unpack[ListDatasetExportJobsRequestTypeDef]
    ) -> ListDatasetExportJobsResponseTypeDef:
        """
        Retrieves a paginated list of dataset export jobs for a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_dataset_export_jobs.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_dataset_export_jobs)
        """

    def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Retrieves a paginated list of datasets for a specific target resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_datasets.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_datasets)
        """

    def list_enrichment_jobs(
        self, **kwargs: Unpack[ListEnrichmentJobsRequestTypeDef]
    ) -> ListEnrichmentJobsResponseTypeDef:
        """
        Lists enrichment jobs within a workspace with optional filtering and pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_enrichment_jobs.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_enrichment_jobs)
        """

    def list_executions(
        self, **kwargs: Unpack[ListExecutionsRequestTypeDef]
    ) -> ListExecutionsResponseTypeDef:
        """
        Retrieves a paginated list of summaries of all executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_executions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_executions)
        """

    def list_gateways(
        self, **kwargs: Unpack[ListGatewaysRequestTypeDef]
    ) -> ListGatewaysResponseTypeDef:
        """
        Retrieves a paginated list of gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_gateways.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_gateways)
        """

    def list_interface_relationships(
        self, **kwargs: Unpack[ListInterfaceRelationshipsRequestTypeDef]
    ) -> ListInterfaceRelationshipsResponseTypeDef:
        """
        Retrieves a paginated list of asset models that have a specific interface asset
        model applied to them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_interface_relationships.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_interface_relationships)
        """

    def list_pipeline_executions(
        self, **kwargs: Unpack[ListPipelineExecutionsRequestTypeDef]
    ) -> ListPipelineExecutionsResponseTypeDef:
        """
        Lists pipeline executions for a specific pipeline in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_pipeline_executions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_pipeline_executions)
        """

    def list_pipelines(
        self, **kwargs: Unpack[ListPipelinesRequestTypeDef]
    ) -> ListPipelinesResponseTypeDef:
        """
        Lists pipelines in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_pipelines.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_pipelines)
        """

    def list_portals(
        self, **kwargs: Unpack[ListPortalsRequestTypeDef]
    ) -> ListPortalsResponseTypeDef:
        """
        Retrieves a paginated list of IoT SiteWise Monitor portals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_portals.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_portals)
        """

    def list_project_assets(
        self, **kwargs: Unpack[ListProjectAssetsRequestTypeDef]
    ) -> ListProjectAssetsResponseTypeDef:
        """
        Retrieves a paginated list of assets associated with an IoT SiteWise Monitor
        project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_project_assets.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_project_assets)
        """

    def list_projects(
        self, **kwargs: Unpack[ListProjectsRequestTypeDef]
    ) -> ListProjectsResponseTypeDef:
        """
        Retrieves a paginated list of projects for an IoT SiteWise Monitor portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_projects.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_projects)
        """

    def list_queries(
        self, **kwargs: Unpack[ListQueriesRequestTypeDef]
    ) -> ListQueriesResponseTypeDef:
        """
        Retrieves a paginated list of queries for a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_queries.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_queries)
        """

    def list_searches(
        self, **kwargs: Unpack[ListSearchesRequestTypeDef]
    ) -> ListSearchesResponseTypeDef:
        """
        Lists the searches in a workspace, most recently started first.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_searches.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_searches)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of tags for an IoT SiteWise resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_tags_for_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_tags_for_resource)
        """

    def list_tasks(self, **kwargs: Unpack[ListTasksRequestTypeDef]) -> ListTasksResponseTypeDef:
        """
        Lists tasks in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_tasks.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_tasks)
        """

    def list_time_series(
        self, **kwargs: Unpack[ListTimeSeriesRequestTypeDef]
    ) -> ListTimeSeriesResponseTypeDef:
        """
        Retrieves a paginated list of time series (data streams).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_time_series.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_time_series)
        """

    def list_workspaces(
        self, **kwargs: Unpack[ListWorkspacesRequestTypeDef]
    ) -> ListWorkspacesResponseTypeDef:
        """
        Retrieves a paginated list of workspaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/list_workspaces.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#list_workspaces)
        """

    def put_asset_model_interface_relationship(
        self, **kwargs: Unpack[PutAssetModelInterfaceRelationshipRequestTypeDef]
    ) -> PutAssetModelInterfaceRelationshipResponseTypeDef:
        """
        Creates or updates an interface relationship between an asset model and an
        interface asset model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/put_asset_model_interface_relationship.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#put_asset_model_interface_relationship)
        """

    def put_default_encryption_configuration(
        self, **kwargs: Unpack[PutDefaultEncryptionConfigurationRequestTypeDef]
    ) -> PutDefaultEncryptionConfigurationResponseTypeDef:
        """
        Sets the default encryption configuration for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/put_default_encryption_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#put_default_encryption_configuration)
        """

    def put_logging_options(
        self, **kwargs: Unpack[PutLoggingOptionsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Sets logging options for IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/put_logging_options.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#put_logging_options)
        """

    def put_storage_configuration(
        self, **kwargs: Unpack[PutStorageConfigurationRequestTypeDef]
    ) -> PutStorageConfigurationResponseTypeDef:
        """
        Configures storage settings for IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/put_storage_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#put_storage_configuration)
        """

    def start_pipeline_execution(
        self, **kwargs: Unpack[StartPipelineExecutionRequestTypeDef]
    ) -> StartPipelineExecutionResponseTypeDef:
        """
        Starts execution of a pipeline in the specified workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/start_pipeline_execution.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#start_pipeline_execution)
        """

    def start_query(self, **kwargs: Unpack[StartQueryRequestTypeDef]) -> StartQueryResponseTypeDef:
        """
        Starts an asynchronous SQL query against workspace telemetry, annotations, data
        segment, and dataset data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/start_query.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#start_query)
        """

    def start_search(
        self, **kwargs: Unpack[StartSearchRequestTypeDef]
    ) -> StartSearchResponseTypeDef:
        """
        Starts an asynchronous search over the data in a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/start_search.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#start_search)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Adds tags to an IoT SiteWise resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/tag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes a tag from an IoT SiteWise resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/untag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#untag_resource)
        """

    def update_access_policy(
        self, **kwargs: Unpack[UpdateAccessPolicyRequestTypeDef]
    ) -> dict[str, Any]:
        """
        The IoT SiteWise Monitor feature will no longer be open to new customers
        starting November 7, 2025.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_access_policy.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_access_policy)
        """

    def update_asset(
        self, **kwargs: Unpack[UpdateAssetRequestTypeDef]
    ) -> UpdateAssetResponseTypeDef:
        """
        Updates an asset's name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_asset.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_asset)
        """

    def update_asset_model(
        self, **kwargs: Unpack[UpdateAssetModelRequestTypeDef]
    ) -> UpdateAssetModelResponseTypeDef:
        """
        Updates an asset model and all of the assets that were created from the model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_asset_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_asset_model)
        """

    def update_asset_model_composite_model(
        self, **kwargs: Unpack[UpdateAssetModelCompositeModelRequestTypeDef]
    ) -> UpdateAssetModelCompositeModelResponseTypeDef:
        """
        Updates a composite model and all of the assets that were created from the
        model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_asset_model_composite_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_asset_model_composite_model)
        """

    def update_asset_property(
        self, **kwargs: Unpack[UpdateAssetPropertyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an asset property's alias and notification state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_asset_property.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_asset_property)
        """

    def update_computation_model(
        self, **kwargs: Unpack[UpdateComputationModelRequestTypeDef]
    ) -> UpdateComputationModelResponseTypeDef:
        """
        Updates the computation model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_computation_model.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_computation_model)
        """

    def update_dashboard(self, **kwargs: Unpack[UpdateDashboardRequestTypeDef]) -> dict[str, Any]:
        """
        The IoT SiteWise Monitor feature will no longer be open to new customers
        starting November 7, 2025.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_dashboard.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_dashboard)
        """

    def update_dataset(
        self, **kwargs: Unpack[UpdateDatasetRequestTypeDef]
    ) -> UpdateDatasetResponseTypeDef:
        """
        Updates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_dataset.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_dataset)
        """

    def update_gateway(
        self, **kwargs: Unpack[UpdateGatewayRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a gateway's name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_gateway.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_gateway)
        """

    def update_gateway_capability_configuration(
        self, **kwargs: Unpack[UpdateGatewayCapabilityConfigurationRequestTypeDef]
    ) -> UpdateGatewayCapabilityConfigurationResponseTypeDef:
        """
        Updates a gateway capability configuration or defines a new capability
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_gateway_capability_configuration.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_gateway_capability_configuration)
        """

    def update_pipeline(
        self, **kwargs: Unpack[UpdatePipelineRequestTypeDef]
    ) -> UpdatePipelineResponseTypeDef:
        """
        Updates an existing pipeline in the specified workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_pipeline.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_pipeline)
        """

    def update_portal(
        self, **kwargs: Unpack[UpdatePortalRequestTypeDef]
    ) -> UpdatePortalResponseTypeDef:
        """
        The IoT SiteWise Monitor feature will no longer be open to new customers
        starting November 7, 2025.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_portal.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_portal)
        """

    def update_project(self, **kwargs: Unpack[UpdateProjectRequestTypeDef]) -> dict[str, Any]:
        """
        The IoT SiteWise Monitor feature will no longer be open to new customers
        starting November 7, 2025.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_project.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_project)
        """

    def update_task(self, **kwargs: Unpack[UpdateTaskRequestTypeDef]) -> UpdateTaskResponseTypeDef:
        """
        Updates an existing task in the specified workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_task.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_task)
        """

    def update_workspace(
        self, **kwargs: Unpack[UpdateWorkspaceRequestTypeDef]
    ) -> UpdateWorkspaceResponseTypeDef:
        """
        Updates a workspace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/update_workspace.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#update_workspace)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_pipeline_execution"]
    ) -> DescribePipelineExecutionPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["execute_query"]
    ) -> ExecuteQueryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_asset_property_aggregates"]
    ) -> GetAssetPropertyAggregatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_asset_property_value_history"]
    ) -> GetAssetPropertyValueHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_interpolated_asset_property_values"]
    ) -> GetInterpolatedAssetPropertyValuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_query_results"]
    ) -> GetQueryResultsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_search_results"]
    ) -> GetSearchResultsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_access_policies"]
    ) -> ListAccessPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_actions"]
    ) -> ListActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_asset_model_composite_models"]
    ) -> ListAssetModelCompositeModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_asset_model_properties"]
    ) -> ListAssetModelPropertiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_asset_models"]
    ) -> ListAssetModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_asset_properties"]
    ) -> ListAssetPropertiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_asset_relationships"]
    ) -> ListAssetRelationshipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_assets"]
    ) -> ListAssetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_associated_assets"]
    ) -> ListAssociatedAssetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_bulk_import_jobs"]
    ) -> ListBulkImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_composition_relationships"]
    ) -> ListCompositionRelationshipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_computation_model_data_binding_usages"]
    ) -> ListComputationModelDataBindingUsagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_computation_model_resolve_to_resources"]
    ) -> ListComputationModelResolveToResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_computation_models"]
    ) -> ListComputationModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dashboards"]
    ) -> ListDashboardsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dataset_data_segment_relationships"]
    ) -> ListDatasetDataSegmentRelationshipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dataset_data_segments"]
    ) -> ListDatasetDataSegmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dataset_export_jobs"]
    ) -> ListDatasetExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_datasets"]
    ) -> ListDatasetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_enrichment_jobs"]
    ) -> ListEnrichmentJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_executions"]
    ) -> ListExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_gateways"]
    ) -> ListGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_interface_relationships"]
    ) -> ListInterfaceRelationshipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_pipeline_executions"]
    ) -> ListPipelineExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_pipelines"]
    ) -> ListPipelinesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_portals"]
    ) -> ListPortalsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_project_assets"]
    ) -> ListProjectAssetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_projects"]
    ) -> ListProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_queries"]
    ) -> ListQueriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_searches"]
    ) -> ListSearchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tasks"]
    ) -> ListTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_time_series"]
    ) -> ListTimeSeriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_workspaces"]
    ) -> ListWorkspacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["asset_active"]
    ) -> AssetActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_waiter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["asset_model_active"]
    ) -> AssetModelActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_waiter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["asset_model_not_exists"]
    ) -> AssetModelNotExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_waiter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["asset_not_exists"]
    ) -> AssetNotExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_waiter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["portal_active"]
    ) -> PortalActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_waiter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["portal_not_exists"]
    ) -> PortalNotExistsWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/client/get_waiter.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/client/#get_waiter)
        """
