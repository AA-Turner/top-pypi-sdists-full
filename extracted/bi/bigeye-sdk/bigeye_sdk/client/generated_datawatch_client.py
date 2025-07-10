from __future__ import annotations

import abc
import json

from time import sleep, time
from typing import List, Optional, Union, Dict

from bigeye_sdk.client.enum import Method
from bigeye_sdk.functions.metric_functions import is_same_metric, is_same_column_metric, create_metric_info_list
from bigeye_sdk.functions.urlfuncts import encode_url_params
from bigeye_sdk.generated.com.bigeye.models.generated import (
    TableList,
    ColumnMetricProfileList,
    GetMetricInfoListRequest,
    MetricInfoList,
    SearchMetricConfigurationRequest,
    BatchGetMetricResponse,
    MetricCreationState,
    ThreeLeggedBoolean,
    MetricSortField,
    SortDirection,
    MetricConfiguration,
    MetricBackfillResponse,
    MetricBackfillRequest,
    GetCollectionsResponse,
    GetCollectionResponse,
    Collection,
    EditCollectionResponse,
    EditCollectionRequest,
    GetDeltaApplicableMetricTypesResponse,
    BatchRunMetricsRequest,
    BatchRunMetricsResponse,
    GetSourceListResponse,
    Empty,
    Source,
    CreateSourceRequest,
    BatchMetricConfigRequest,
    BatchMetricConfigResponse,
    Table,
    ComparisonTableInfo,
    GetComparisonTableInfosResponse,
    GetComparisonTableInfosRequest,
    GetIssuesRequest,
    Issue,
    GetIssuesResponse,
    UpdateIssueRequest,
    IssueStatusUpdate,
    IssueStatus,
    MetricRunLabel,
    User,
    UpdateIssueResponse,
    GetTableComparisonMetricGroupInfoRequest,
    GetTableComparisonMetricGroupInfoResponse,
    ComparisonMetricGroup,
    GetPreviewResponse,
    NamedSchedule,
    CreateNamedScheduleRequest,
    GetNamedSchedulesRequest,
    NamedScheduleSortField,
    GetNamedSchedulesResponse,
    SchemaList,
    SchemaSearchRequest,
    DataNodeType,
    CreateDataNodeRequest,
    DataNode,
    CreateLineageRelationshipRequest,
    LineageRelationship,
    CreateCollectionResponse,
    TimeRange,
    NotificationChannel,
    CreateMetricTemplateRequest,
    MetricTemplate,
    MetricTemplateParametersFieldEntry,
    Warehouse,
    CreateMetricTemplateResponse,
    VirtualTableRequest,
    VirtualTable,
    MetricTemplateParameterType,
    FieldType,
    GetMetricTemplateListRequest,
    GetMetricTemplateListResponse,
    MetricTemplateSortField,
    SchemaChangeSortField,
    GetSchemaChangesRequest,
    GetSchemaChangesResponse,
    SchemaChange,
    IntegrationsResponse,
    Integration,
    GetIntegrationEntitiesResponse,
    ConfigValue,
    GetConfigListResponse,
    WorkflowResponse,
    WorkflowStatusResponse,
    GetLineageRelationshipsForNodeResponse,
    WorkspaceListResponse,
    BulkChangeGroupUsersRequest,
    GroupListResponse,
    GetUserListResponse,
    BulkChangeGroupUsersResponse,
    UserInviteRequest,
    GroupUserOperation,
    CreateOrUpdateWorkspaceRequest,
    Workspace,
    CreateOrUpdateGroupRequest,
    Group,
    RoleV2ListResponse,
    RoleOperation,
    BulkResponse,
    GetVirtualTableListRequest,
    GetVirtualTableListResponse,
    IssueMessageUpdate,
    IssueConfigUpdate,
    IssueAssignmentUpdate,
    WorkflowInfo,
    WorkflowProcessingStatus,
    RunDeltaResponse,
    DeltaInfo,
    Delta,
    GetDeltaInfosResponse,
    RelationshipType,
    LineageEdgeV2,
    CreateLineageEdgeV2Request,
    GetColumnListRequest,
    GetColumnListResponse,
    MetricInfo, GetTableListResponse, GetTableListRequest, GetCustomRuleListResponse,
    CreateCustomRuleRequest, CustomRule, MetricSchedule, CustomRulesThresholdType, UpdateCustomRuleRequest,
    CustomRuleInfo, TimeInterval, TimeIntervalType, RebuildSourceRequest, CreatePersonalApiKeyRequest,
    CreatePersonalApiKeyResponse, ListPersonalApiKeyResponse, CreateAgentApiKeyResponse, CreateAgentApiKeyRequest,
    ListAgentApiKeyResponse, GetWorkspaceAccessorsResponse, CreateLineageNodeV2Request, LineageNodeV2,
    LineageSearchResponse, LineageSearchRequest, GetDebugQueriesResponse, ConfigValueType, SourceMetadataOverrides,
    WarehouseType, BulkChangeGroupGrantsRequest, Grant, RoleV2, IdAndDisplayName, BulkChangeGroupGrantsResponse,
    IssuePriorityChangeEvent, TableLineageV2Response, CreateLineageNodeV2BulkRequest, CreateLineageEdgeV2BulkRequest,
    GetMetricObservedColumnBulkRequest, MetricObservedColumnListResponse, MetricObservedColumnRequest,
    MetricObservedColumnResponse, GetCustomRuleListRequest
)

# create logger
from bigeye_sdk.log import get_logger
from bigeye_sdk.model.enums import LineageDirection
from bigeye_sdk.model.protobuf_enum_facade import SimpleFieldType, SimpleMetricTemplateParameterType, \
    SimpleWorkflowProcessingStatus, SimpleTableSortField, SimpleSortDirection, SimpleIssueStatus, SimpleIssuePriority, \
    SimpleIssueSortField

log = get_logger(__file__)


class GeneratedDatawatchClient(abc.ABC):
    """TODO: In future, should be generated and only contain methods generated from protobuf. :)"""

    def _call_datawatch(self, method: Method, url, body: str = None, params: dict = None, timeout: int = None):
        url = url.replace('//', '/')
        return self._call_datawatch_impl(method=method, url=url, body=body, params=params, timeout=timeout)

    @abc.abstractmethod
    def _call_datawatch_impl(self, method: Method, url, body: str = None, params: dict = None, timeout: int = None):
        """Each implementation must override this."""
        pass

    # TODO: Refactor all code to use search_tables below, then deprecate
    def get_tables(self,
                   *,
                   warehouse_id: List[int] = [],
                   schema: List[str] = [],
                   table_name: List[str] = [],
                   ids: List[int] = [],
                   schema_id: List[int] = []) -> TableList:
        url = f"/api/v1/tables{encode_url_params(locals(), remove_keys=['api_conf'])}"
        log.info('Getting warehouse tables.')
        log.info(url)
        response = self._call_datawatch(Method.GET, url)
        tables = TableList().from_dict(response)
        return tables

    def search_tables(self,
                      *,
                      warehouse_id: List[int] = [],
                      schema: List[str] = [],
                      table_name: List[str] = [],
                      ids: List[int] = [],
                      schema_id: List[int] = [],
                      include_favorites: bool = False,
                      ignore_fields: bool = False,
                      include_data_node_ids: bool = True
                      ) -> TableList:
        url = f"/api/v1/tables{encode_url_params(locals(), remove_keys=['api_conf'])}"
        log.info('Getting warehouse tables.')
        log.info(url)
        response = self._call_datawatch(Method.GET, url)
        tables = TableList().from_dict(response)
        return tables

    # TODO: Rename to get_tables when deprecated function is deleted.
    def get_tables_post(self,
                        *,
                        source_ids: List[int] = [],
                        schema_ids: List[int] = [],
                        table_ids: List[int] = [],
                        page_size: int = 0,
                        page_cursor: str = "",
                        sort_field: SimpleTableSortField = SimpleTableSortField.UNSPECIFIED,
                        sort_direction: SimpleSortDirection = SimpleSortDirection.UNSPECIFIED,
                        search: str = "",
                        ignore_fields: bool = True,
                        include_data_node_ids: bool = False) -> GetTableListResponse:

        url = "/api/v1/tables/fetch"
        request = GetTableListRequest()
        request.source_ids = source_ids
        request.schema_ids = schema_ids
        request.table_ids = table_ids
        request.page_size = page_size
        request.page_cursor = page_cursor
        request.sort_field = sort_field.to_datawatch_object()
        request.sort_direction = sort_direction.to_datawatch_object()
        request.search = search
        request.ignore_fields = ignore_fields
        request.include_data_node_ids = include_data_node_ids

        request_dict = request.to_dict()
        request_dict["ignoreFields"] = ignore_fields
        request_json = json.dumps(request_dict)

        response = self._call_datawatch(Method.POST, url=url, body=request_json)

        tlist_current = GetTableListResponse().from_dict(response)
        tlist_total = GetTableListResponse()
        tlist_total.tables.extend(tlist_current.tables)

        while tlist_current.pagination_info.next_cursor:
            request.page_cursor = tlist_current.pagination_info.next_cursor
            request_dict = request.to_dict()
            request_dict["ignoreFields"] = ignore_fields
            request_json = json.dumps(request_dict)

            response = self._call_datawatch(Method.POST, url=url, body=request_json)
            tlist_current = GetTableListResponse().from_dict(response)
            tlist_total.tables.extend(tlist_current.tables)

        return tlist_total

    def get_table_ids(self,
                      warehouse_id: List[int] = [],
                      schemas: List[str] = [],
                      table_name: List[str] = [],
                      ids: List[int] = [],
                      schema_id: List[int] = []) -> List[int]:
        return [t.id for t in self.get_tables(warehouse_id=warehouse_id, schema=schemas, table_name=table_name,
                                              ids=ids, schema_id=schema_id).tables]

    def rebuild(self, warehouse_id: int, schema_name: str = None):
        """
        TODO: switch to returning an object from the protobuf.

        Args:
            warehouse_id:
            schema_name:

        Returns: list of metrics.

        """
        url = f'/dataset/rebuild/{warehouse_id}'

        if schema_name is not None:
            url = url + f'/{schema_name}'

        return self._call_datawatch(Method.GET, url)

    def get_table_profile(self, table_id: int) -> ColumnMetricProfileList:
        url = f'/api/v1/tables/profile/{table_id}'
        return ColumnMetricProfileList().from_dict(self._call_datawatch(Method.GET, url))

    def batch_delete_metrics(self, metric_ids: List[int]):
        body = json.dumps({"metricIds": metric_ids})
        log.info(f'Deleting metrics: {metric_ids}')
        url = f'/statistics'
        return self._call_datawatch(Method.DELETE, url, body)

    def get_metric_configuration(
            self, *, metric_id: int = 0
    ) -> MetricConfiguration:
        """Get metric configuration"""

        url = f'/api/v1/metrics/{metric_id}'

        r = self._call_datawatch(Method.GET, url)
        return MetricConfiguration().from_dict(r)

    def search_metric_configuration(
            self,
            *,
            ids: List[int] = [],
            warehouse_ids: List[int] = [],
            table_ids: List[int] = [],
            table_name: str = "",
            status: str = "",
            muted: bool = False,
    ) -> List[MetricConfiguration]:
        """Search metric configurations"""

        request = SearchMetricConfigurationRequest()
        request.ids = ids
        request.warehouse_ids = warehouse_ids
        request.table_ids = table_ids
        request.table_name = table_name
        request.status = status
        request.muted = muted

        url = f'/api/v1/metrics{encode_url_params(d=request.to_dict())}'

        response = self._call_datawatch(Method.GET, url=url)

        return [MetricConfiguration().from_dict(m) for m in BatchGetMetricResponse(metrics=response).metrics]

    def get_metric_info_batch_post(
            self,
            *,
            metric_ids: List[int] = [],
            warehouse_ids: List[int] = [],
            table_ids: List[int] = [],
            table_name: str = "",
            status: str = "",  # healthy, alerting, unknown
            metric_creation_states: List[MetricCreationState] = [],
            muted: ThreeLeggedBoolean = 0,
            page_size: int = 0,
            page_cursor: str = "",
            sort_field: MetricSortField = 0,
            schema_name: str = "",
            column_ids: List[int] = [],
            search: str = "",
            sort_direction: SortDirection = 0,
    ) -> MetricInfoList:
        """
        Get metric information as batch.
        Args:
            metric_ids: list of metric ids
            warehouse_ids: list of source ids
            table_ids: list of table ids
            table_name: a single table name
            status: healthy, alerting, unknown
            metric_creation_states: a list of metric creation states (enum)
            muted: three-legged true, false, unspecified
            page_size: int
            page_cursor: unique id of the cursor
            sort_field: sort by value MetricSortField (enum)
            schema_name: a single schema name
            column_ids: a list of column ids
            search: a raw search of metric names.
            sort_direction: three-legged ascending, descending, unspecified

        Returns: a list of metric info fitting the argument criteria.

        """

        request = GetMetricInfoListRequest()
        request.metric_ids = metric_ids
        request.warehouse_ids = warehouse_ids
        request.table_ids = table_ids
        request.table_name = table_name
        request.status = status
        request.metric_creation_states = metric_creation_states
        request.muted = muted
        request.page_size = page_size
        request.page_cursor = page_cursor
        request.sort_field = sort_field
        request.schema_name = schema_name
        request.column_ids = column_ids
        request.search = search
        request.sort_direction = sort_direction

        url = '/api/v1/metrics/info'

        if len(request.to_dict()) != 0:
            response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        else:
            response = self._call_datawatch(Method.GET, url=url)

        try:
            mil_current = MetricInfoList().from_dict(response)
        except ValueError as e:
            log.warning(f"Exception handled during response {e}")
            log.info("Some metrics may not be available")
            mil_current = create_metric_info_list(metric_infos=response)

        mil_return = MetricInfoList()
        mil_return.metrics.extend(mil_current.metrics)

        while mil_current.pagination_info.next_cursor:
            request.page_cursor = mil_current.pagination_info.next_cursor
            response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
            try:
                mil_current = MetricInfoList().from_dict(response)
            except ValueError:
                mil_current = create_metric_info_list(metric_infos=response)
            mil_return.metrics.extend(mil_current.metrics)

        return mil_return

    def get_existing_metric(self,
                            warehouse_id: int, table: Table, column_name: str, user_defined_name: str,
                            metric_name: str, group_by: List[str], filters: List[str]):
        """
        Get an existing metric by name and group_by.
        """
        metrics: List[MetricConfiguration] = self.search_metric_configuration(warehouse_ids=[warehouse_id],
                                                                              table_ids=[table.id])

        for m in metrics:
            if is_same_metric(m, metric_name, user_defined_name, group_by, filters) \
                    and is_same_column_metric(m, column_name):
                return m
        return None

    def backfill_metric(
            self,
            *,
            metric_ids: List[int] = [],
            backfill_range: Optional[TimeRange] = None,
            delete_history: Optional[bool] = None
    ) -> MetricBackfillResponse:
        """
        Runs metrics for past data and returns the API response.  Destructive.
        :param metric_ids: list of metric ids to run.
        :param backfill_range: time range for metrics to be run.
        :param delete_history: whether to delete metric run history with backfill.
        :return: MetricBackfillResponse object.
        """

        request = MetricBackfillRequest()
        request.metric_ids = metric_ids
        if backfill_range is not None:
            request.backfill_range = backfill_range
        if delete_history is not None:
            request.delete_history = delete_history

        url = "/api/v1/metrics/backfill"

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())

        return MetricBackfillResponse().from_dict(response)

    def get_collections(self) -> GetCollectionsResponse:
        url = "/api/v1/collections/"
        log.info(url)
        response = self._call_datawatch(Method.GET, url=url)
        return GetCollectionsResponse().from_dict(response)

    def get_collection(self, collection_id: int) -> GetCollectionResponse:
        url = f"/api/v1/collections/{collection_id}"
        log.info(url)
        response = self._call_datawatch(Method.GET, url=url)
        return GetCollectionResponse().from_dict(response)

    def create_collection(
            self,
            *,
            collection_name: str = "",
            description: str = "",
            metric_ids: List[int] = [],
            notification_channels: List[NotificationChannel] = [],
            muted_until_timestamp: int = 0,
    ) -> CreateCollectionResponse:
        """Create collection"""

        url = f"/api/v1/collections"

        request = EditCollectionRequest()
        request.collection_name = collection_name
        request.description = description
        request.metric_ids = metric_ids
        if notification_channels is not None:
            request.notification_channels = notification_channels
        request.muted_until_timestamp = muted_until_timestamp

        log.info(f'Query: {url}; Body: {request.to_json()}')

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())

        return CreateCollectionResponse().from_dict(response)

    def create_collection_dep(self, collection: Collection) -> EditCollectionResponse:
        url = f"/api/v1/collections"

        request: EditCollectionRequest = EditCollectionRequest()
        request.collection_name = collection.name
        request.description = collection.description
        request.metric_ids = collection.metric_ids
        request.notification_channels = collection.notification_channels
        request.muted_until_timestamp = collection.muted_until_timestamp

        log.info(f'Query: {url}; Body: {request.to_json()}')

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())

        return EditCollectionResponse().from_dict(response)

    def update_collection(self, collection: Collection) -> EditCollectionResponse:

        request: EditCollectionRequest = EditCollectionRequest()
        request.collection_name = collection.name
        request.description = collection.description if collection.description else collection.name
        request.metric_ids = collection.metric_ids
        request.notification_channels = collection.notification_channels
        request.muted_until_timestamp = collection.muted_until_timestamp

        url = f"/api/v1/collections/{collection.id}"

        log.info(f'Query: {url}; Body: {request.to_json()}')

        response = self._call_datawatch(Method.PUT, url=url, body=request.to_json())

        return EditCollectionResponse().from_dict(response)

    def upsert_metric_to_collection(self, collection_id: int,
                                    add_metric_ids: Union[int, List[int]]) -> EditCollectionResponse:

        if type(add_metric_ids) == int:
            mids = list(add_metric_ids)
        else:
            mids = add_metric_ids

        collection: Collection = self.get_collection(collection_id=collection_id).collection

        for mid in mids:
            collection.metric_ids.append(mid)

        return self.update_collection(collection=collection)

    def delete_collection(self, collection_id: int):
        url = f"/api/v1/collections/{collection_id}"

        self._call_datawatch(Method.DELETE, url=url)

    def delete_delta(self, *, comparison_table_id: int = 0):
        """Delete a delta"""

        url = f"/api/v1/metrics/comparisons/tables/{comparison_table_id}"

        self._call_datawatch(Method.DELETE, url)

    def get_delta_applicable_metric_types(
            self, *, table_id: int = 0
    ) -> GetDeltaApplicableMetricTypesResponse:
        """
        Get list of metrics applicable for deltas
        Args:
            table_id: source table id

        Returns: list of metrics applicable for deltas.

        """

        url = f"/api/v1/tables/{table_id}/delta-applicable-metric-types"

        response = self._call_datawatch(Method.GET, url)

        return GetDeltaApplicableMetricTypesResponse().from_dict(response)

    def run_a_delta(self, *, delta_id: int, await_results: bool = False) -> Optional[Delta]:
        """
        Args:
            delta_id: Required.  The ID of the delta to run
            await_results: bool. Whether to wait for delta run to complete or not, default False.

        Returns:  Optional[Delta]
        """

        url = f"/api/v1/deltas/run/{delta_id}"
        response = RunDeltaResponse().from_dict(
            self._call_datawatch(Method.GET, url)
        )

        if not await_results:
            log.info(f"Delta run has been queued for {response.delta_info.delta.name}")
            return None

        workflow_response = self.get_workflow_status(
            workflow_id=response.workflow_info.workflow_id
        )

        while (
                workflow_response.status
                == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_QUEUED
                or workflow_response.status
                == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_IN_PROGRESS
        ):
            log.info("Delta run in queue...")
            sleep(10)
            workflow_response = self.get_workflow_status(workflow_id=workflow_response.workflow_id)

        status = SimpleWorkflowProcessingStatus.from_datawatch_object(
            workflow_response.status
        )
        log.info(f"Delta run completed for delta ID: {delta_id} with status {status}")

        delta = self.get_delta_by_id(delta_id=delta_id)

        # TODO - bug with backend that reports completed status before delta is actually complete, once fixed this can
        #  be removed.
        seconds_since_run = time() - delta.last_run_at_epoch_seconds
        while seconds_since_run > 60:
            log.info(f"Reading delta results...")
            sleep(5)
            delta = self.get_delta_by_id(delta_id=delta_id)
            seconds_since_run = time() - delta.last_run_at_epoch_seconds

        return delta

    def get_delta_info(self, delta_id: int) -> DeltaInfo:
        url = f"/api/v1/deltas/{delta_id}"
        response = self._call_datawatch(Method.GET, url)

        return DeltaInfo().from_dict(response)

    def get_delta_by_id(self, delta_id: int) -> Delta:
        return self.get_delta_info(delta_id=delta_id).delta

    def get_delta_information(self, *, delta_ids: List[int],
                              exclude_comparison_metrics: bool = False) -> List[ComparisonTableInfo]:
        """

            Args:
                delta_ids: Required.  The delta ID or IDs.
                exclude_comparison_metrics: Optional. Whether to include the list of ComparisonMetricInfos

            Returns:  List[ComparisonTableInfo]

        """

        url = "/api/v1/metrics/comparisons/tables/info"
        request = GetComparisonTableInfosRequest(delta_ids, exclude_comparison_metrics)
        response = self._call_datawatch(Method.POST, url, request.to_json())

        return GetComparisonTableInfosResponse().from_dict(response).comparison_table_infos

    def get_deltas(self,
                   *,
                   comparison_table_ids: List[int] = [],
                   exclude_comparison_metrics: bool = True,
                   page_size: Optional[int] = 0) -> List[DeltaInfo]:
        """
            Args:
                comparison_table_ids: Optional.  The id or IDs of tables used in deltas.
                exclude_comparison_metrics: Optional. Whether to exclude the list of ComparisonMetricInfos
                page_size: Optional. The number of records to return per search

            Returns:  List[DeltaInfo]
        """

        url = "/api/v1/deltas/fetch"
        request = GetComparisonTableInfosRequest()
        request.comparison_table_ids = comparison_table_ids
        request.exclude_comparison_metrics = exclude_comparison_metrics
        request.page_size = page_size

        response = self._call_datawatch(Method.POST, url, request.to_json())

        dil_current = GetDeltaInfosResponse().from_dict(response)
        dil_return: List[DeltaInfo] = []
        dil_return.extend(dil_current.delta_infos)

        while dil_current.pagination_info.next_cursor:
            request.page_cursor = dil_current.pagination_info.next_cursor
            response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
            dil_current = GetDeltaInfosResponse().from_dict(response)
            dil_return.extend(dil_current.delta_infos)

        return dil_return

    def get_delta_groups_information(self, *, comparison_metric_id: int) -> List[ComparisonMetricGroup]:
        """

            Args:
                comparison_metric_id: Required.  The ID for a delta with grouped by columns.

            Returns:  List[ComparisonMetricGroup]

        """

        url = f"/api/v1/metrics/comparisons/metrics/{comparison_metric_id}/groups/info"
        request = GetTableComparisonMetricGroupInfoRequest(comparison_metric_id)
        response = self._call_datawatch(Method.GET, url, request.to_json())

        return GetTableComparisonMetricGroupInfoResponse().from_dict(response).group_state

    def run_metric_batch(
            self, *, metric_ids: List[int] = []
    ) -> BatchRunMetricsResponse:
        """Batch run metrics"""

        request = BatchRunMetricsRequest()
        request.metric_ids = metric_ids

        url = '/api/v1/metrics/run/batch'

        response = self._call_datawatch(Method.POST, url, request.to_json())

        return BatchRunMetricsResponse().from_dict(response)

    def run_metric_batch_async(
            self, *, metric_ids: List[int] = []
    ) -> List[MetricInfo]:
        """Batch run metrics via queue"""
        url = "/api/v1/metrics/run/batch/queue"

        batch_request = BatchRunMetricsRequest(metric_ids=metric_ids)

        response = WorkflowInfo().from_dict(
            self._call_datawatch(Method.POST, url, batch_request.to_json())
        )

        workflow_response = self.get_workflow_status(workflow_id=response.workflow_id)

        while (workflow_response.status == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_QUEUED or
               workflow_response.status == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_IN_PROGRESS):
            log.info("Batch metric run in queue...")
            sleep(10)
            workflow_response = self.get_workflow_status(workflow_id=response.workflow_id)

        status = SimpleWorkflowProcessingStatus.from_datawatch_object(workflow_response.status)
        log.info(f"Batch metric run completed for metric IDs: {metric_ids} with status {status}")

        # TODO remove this call when backend returns BatchMetricRunResponse in workflow status
        # https://linear.app/torodata/issue/HELP-721/return-batchrunmetricsresponse-with-workflow-response
        return self.get_metric_info_batch_post(metric_ids=metric_ids).metrics

    def get_sources(self) -> GetSourceListResponse:
        """Get sources"""
        url = "/api/v1/sources/fetch"
        request = Empty()

        response = self._call_datawatch(Method.POST, url, request.to_json())

        return GetSourceListResponse().from_dict(response)

    def get_schemas(self, *, warehouse_id: List[int] = []) -> SchemaList:
        request = SchemaSearchRequest()
        request.warehouse_id = warehouse_id

        url = f'/api/v1/schemas{encode_url_params(d=request.to_dict())}'

        response = self._call_datawatch(Method.GET, url)

        return SchemaList().from_dict(response)

    def edit_metric(self, metric_configuration: MetricConfiguration = None) -> BatchMetricConfigResponse:
        """
        TODO: Only supporting 1 metric because of weird defaults and required fields.
        Args:
            metric_configuration:

        Returns:

        """
        url = "/api/v1/metrics/batch"

        request = BatchMetricConfigRequest()
        request.metric_ids = [metric_configuration.id]

        request.metric_configuration = metric_configuration
        request_json = request.to_json()

        response = self._call_datawatch(Method.PUT, url, request_json)

        return BatchMetricConfigResponse().from_dict(response)

    def create_source(self, request: CreateSourceRequest, if_not_exists: bool = False,
                      overwrite: bool = False) -> Source:
        """
        Creates a source in Bigeye.
        :param request: A CreateSourceRequest containing detail for the source to create.
        :param if_not_exists: If true then will not overwrite and return the existing source.  Matches on alias.
        :param overwrite: If true then will overwrite existing source. Matches on aliad.
        :return:
        """

        if if_not_exists and overwrite:
            raise Exception("Cannot create source if not exists and overwrite existing source.. Choose one!")

        if if_not_exists or overwrite:
            existing_sources_ix: Dict[str, Source] = {s.name: s for s in self.get_sources().sources}
            existing = existing_sources_ix.get(request.name, None)
            if existing:
                if if_not_exists:
                    return existing
                if overwrite:
                    self.delete_source(warehouse_id=existing.id)

        url = '/api/v1/sources'

        response = self._call_datawatch(Method.POST, url, request.to_json())
        source = Source().from_dict(value=response['source'])
        log.info(f'Source {source.name} created with warehouse ID: {source.id}')
        return source

    def upsert_source(
            self,
            *,
            source_id: int = 0,
            name: str = "",
            hostname: str = "",
            port: int = 0,
            database_name: str = "",
            database_type: WarehouseType = WarehouseType.DATABASE_TYPE_UNSPECIFIED,
            domain: str = "",
            username: str = "",
            password: str = "",
            private_key_file: str = "",
            query_timeout_seconds: int = 0,
            skip_indexing: bool = False,
            alation_source_id: int = 0,
            atlan_connection_id: str = "",
            temporal_agent_secret: str = "",
            bigquery_query_project_ids: str = "",
            source_metadata_overrides: SourceMetadataOverrides = SourceMetadataOverrides(),
            request: Optional[CreateSourceRequest] = None
    ):

        url = '/api/v1/sources'
        if not request:
            request = CreateSourceRequest()
            request.id = source_id
            request.name = name
            request.hostname = hostname
            request.port = port
            request.database_name = database_name
            request.database_type = database_type
            request.domain = domain
            request.username = username
            request.password = password
            request.private_key_file = private_key_file
            request.query_timeout_seconds = query_timeout_seconds
            request.skip_indexing = skip_indexing
            request.alation_source_id = alation_source_id
            request.atlan_connection_id = atlan_connection_id
            request.temporal_agent_secret = temporal_agent_secret
            request.bigquery_query_project_ids = bigquery_query_project_ids
            request.source_metadata_overrides = source_metadata_overrides

        response = self._call_datawatch(Method.POST, url, request.to_json())
        source = Source().from_dict(value=response['source'])

        if source_id:
            log.info(f"Source {source_id} has been updated.")
        else:
            log.info(f"Source {source.name} created with warehouse ID: {source.id}")
        return source


    def delete_metric(self, metric: Union[int, MetricConfiguration]):
        """
        Deletes an individual metric.
        Args:
            metric: MetricConfiguration

        Warnings: Will log a warning when attempting to delete a metric created by Bigconfig.
        """

        if isinstance(metric, int):
            metric = self.get_metric_configuration(metric_id=metric)

        if metric.metric_creation_state == MetricCreationState.METRIC_CREATION_STATE_SUITE:
            log.warning(f"Cannot delete metric because it was created by Bigconfig.  "
                        f"MetricID: {metric.id}")
        else:
            url = f'/api/v1/metrics/{metric.id}'

            self._call_datawatch(Method.DELETE, url)

    def delete_source(self, warehouse_id: int):

        url = f'/api/v1/sources/{warehouse_id}'

        self._call_datawatch(Method.DELETE, url)
        log.info(f'Begin delete for warehouse ID: {warehouse_id}')

    def get_issues(
            self,
            *,
            current_status: List[SimpleIssueStatus] = [],
            warehouse_ids: List[int] = [],
            schema_ids: List[int] = [],
            metric_ids: List[int] = [],
            collection_ids: List[int] = [],
            issue_ids: List[int] = [],
            schema_names: List[str] = [],
            table_ids: List[int] = [],
            column_ids: List[int] = [],
            related_issue_ids: List[int] = [],
            parent_issue_ids: List[int] = [],
            priority: List[SimpleIssuePriority] = [],
            assignee_ids: List[int] = [],
            page_size: int = 0,
            sort_field: SimpleIssueSortField = SimpleIssueSortField.UNSPECIFIED,
            sort_direction: SimpleSortDirection = SimpleSortDirection.UNSPECIFIED,
            search: str = "") -> List[Issue]:

        url = '/api/v1/issues/fetch'

        # TODO: Will require update when GetIssuesRequest refactors to collection_ids

        request = GetIssuesRequest()
        request.current_status = [status.to_datawatch_object() for status in current_status]
        request.warehouse_ids = warehouse_ids
        request.schema_ids = schema_ids
        request.metric_ids = metric_ids
        request.sla_ids = collection_ids
        request.issue_ids = issue_ids
        request.schema_names = schema_names
        request.table_ids = table_ids
        request.column_ids = column_ids
        request.related_issue_ids = related_issue_ids
        request.parent_issue_ids = parent_issue_ids
        request.sort_field = sort_field.to_datawatch_object()
        request.sort_direction = sort_direction.to_datawatch_object()
        request.page_size = page_size
        request.priority = [p.to_datawatch_object() for p in priority]
        request.assignee_ids = assignee_ids
        request.search = search

        response = GetIssuesResponse().from_dict(
            self._call_datawatch(method=Method.POST, url=url, body=request.to_json())
        )
        issues: List[Issue] = response.issue
        while response.pagination_info.next_cursor:
            request.page_cursor = response.pagination_info.next_cursor
            response = GetIssuesResponse().from_dict(
                self._call_datawatch(method=Method.POST, url=url, body=request.to_json())
            )
            issues.extend(response.issue)
        return issues

    def get_issue(self, issue_id: int) -> Issue:
        url = f'/api/v1/issues/{issue_id}'

        return GetIssuesResponse().from_dict(
            self._call_datawatch(method=Method.GET, url=url)
        ).issue[0]

    def get_issue_by_key(self, issue_key: str) -> Issue:
        url = f'/api/v1/issues/company-issue/{issue_key}'
        response = GetIssuesResponse().from_dict(self._call_datawatch(method=Method.GET, url=url))
        return response.issue[0]

    def update_issue(self,
                     *,
                     issue_id: int,
                     issue_status: str,
                     updated_by: str,
                     update_message: str,
                     closing_label: Optional[str]) -> Issue:

        url = f'/api/v1/issues/{issue_id}'

        status = IssueStatus.from_string(f'ISSUE_STATUS_{issue_status.upper()}')
        isu = IssueStatusUpdate()
        isu.updated_by = User(name=updated_by)
        isu.message = update_message
        isu.new_status = status

        if status == IssueStatus.ISSUE_STATUS_CLOSED or status == IssueStatus.ISSUE_STATUS_MONITORING:
            if closing_label is not None:
                label = MetricRunLabel.from_string(f'METRIC_RUN_LABEL_{closing_label.upper()}')
                isu.closing_label = label

        request = UpdateIssueRequest(status_update=isu)

        response = self._call_datawatch(Method.PUT, url, request.to_json())
        return UpdateIssueResponse().from_dict(response).issue

    def post_comment_to_issue(self, issue_id: int, comment: str) -> Issue:
        url = f'/api/v1/issues/{issue_id}'
        message_update = IssueMessageUpdate(message=comment)
        request = UpdateIssueRequest(message_update=message_update)
        response = self._call_datawatch(Method.PUT, url, request.to_json())
        return UpdateIssueResponse().from_dict(response).issue

    def assign_issue_to_user(self, issue_id: int, user_id: int) -> Issue:
        url = f'/api/v1/issues/{issue_id}'
        assignment_update = IssueAssignmentUpdate(assignee=User(id=user_id))
        request = UpdateIssueRequest(assignment_update=assignment_update)
        response = self._call_datawatch(Method.PUT, url, request.to_json())
        return UpdateIssueResponse().from_dict(response).issue

    def update_issue_summary(self, issue_id: int, summary: str, append: bool = False, is_link: bool = False):
        url = f'/api/v1/issues/{issue_id}'
        summary_text = summary

        if append:
            issue: Issue = self.get_issue(issue_id=issue_id)
            summary_text = (f"{issue.summary}  "
                            f"{summary}")

        summary_update = IssueConfigUpdate(summary=summary_text)
        request = UpdateIssueRequest(config_update=summary_update)
        response = self._call_datawatch(Method.PUT, url, request.to_json())
        return UpdateIssueResponse().from_dict(response).issue

    def update_issue_priority(self, issue_id: int, priority: SimpleIssuePriority) -> Issue:
        url = f'/api/v1/issues/{issue_id}'
        priority_update = IssuePriorityChangeEvent(issue_priority=priority.to_datawatch_object())
        request = UpdateIssueRequest(priority_update=priority_update)
        response = self._call_datawatch(Method.PUT, url, request.to_json())
        return UpdateIssueResponse().from_dict(response).issue

    def get_debug_preview(self, *, metric_id: int = 0) -> GetPreviewResponse:
        """Get sample debug rows for debug page"""

        url = f'/api/v1/metrics/{metric_id}/debug/preview'

        return GetPreviewResponse().from_dict(self._call_datawatch(Method.GET, url))

    def get_debug_and_metric_queries(self, *, metric_id: int = 0, timeout: int = 0) -> GetDebugQueriesResponse:
        """Get queries for debug page"""
        url = f"/api/v1/metrics/{metric_id}/debug/queries"
        return GetDebugQueriesResponse().from_dict(
            self._call_datawatch(Method.GET, url, timeout=timeout)
        )

    def create_named_schedule(
            self, *, id: int = 0, name: str = "", cron: str = ""
    ) -> NamedSchedule:
        """Upsert a named schedule. Pass schedule ID to update."""

        url = "/api/v1/schedules"

        request = CreateNamedScheduleRequest()
        request.id = id
        request.name = name
        request.cron = cron

        r = self._call_datawatch(Method.POST, url, request.to_json())
        return NamedSchedule().from_dict(r)

    def delete_named_schedule(self, *, schedule_id: int = 0) -> Empty:
        """Deleted a named schedule"""

        # delete: "/api/v1/schedules/{schedule_id}"

        url = f"/api/v1/schedules/{schedule_id}"

        return self._call_datawatch(Method.DELETE, url)

    def get_named_schedule(
            self,
            *,
            ids: List[int] = [],
            page_size: int = 0,
            page_cursor: str = "",
            sort_field: NamedScheduleSortField = 0,
            sort_direction: SortDirection = 0,
            search: str = "",
    ) -> GetNamedSchedulesResponse:
        """Get named schedules"""

        # get: "/api/v1/schedules"

        request = GetNamedSchedulesRequest()
        request.ids = ids
        request.page_size = page_size
        request.page_cursor = page_cursor
        request.sort_field = sort_field
        request.sort_direction = sort_direction
        request.search = search

        url = f'/api/v1/schedules{encode_url_params(d=request.to_dict())}'

        response = GetNamedSchedulesResponse().from_dict(self._call_datawatch(Method.GET, url=url))
        schedules: List[NamedSchedule] = []
        schedules.extend(response.named_schedules)

        while response.pagination_info.next_cursor:
            request.page_cursor = response.pagination_info.next_cursor
            url = f'/api/v1/schedules{encode_url_params(d=request.to_dict())}'
            response = self._call_datawatch(Method.GET, url=url)
            schedules.extend(
                GetNamedSchedulesResponse().from_dict(response).named_schedules
            )

        return GetNamedSchedulesResponse(named_schedules=schedules)

    def create_data_node(self, *, node_type: DataNodeType, node_entity_id: int) -> DataNode:
        """Create Data Node for Lineage"""

        request = CreateDataNodeRequest()
        request.node_type = node_type
        request.node_entity_id = node_entity_id

        url = '/api/v1/lineage/nodes'

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())

        return DataNode().from_dict(response)

    def get_data_node_by_id(self, node_id: int) -> DataNode:
        """Get a Data Node by ID"""
        url = f'/api/v1/lineage/nodes/{node_id}'
        response = self._call_datawatch(Method.GET, url=url)

        return DataNode().from_dict(response)

    def get_relationships_for_data_nodes(self, *, data_node_id: int) -> GetLineageRelationshipsForNodeResponse:

        url = f'/api/v1/lineage/nodes/{data_node_id}/relationships'
        return GetLineageRelationshipsForNodeResponse().from_dict(
            self._call_datawatch(Method.GET, url=url)
        )

    def delete_data_node(self, *, data_node_id: int):

        url = f"/api/v1/lineage/nodes/{data_node_id}"
        log.info(f"Deleting data node {data_node_id}")
        self._call_datawatch(Method.DELETE, url=url)

    def create_table_lineage_relationship(self,
                                          *,
                                          upstream_data_node_id: int,
                                          downstream_data_node_id: int) -> LineageRelationship:
        """Create lineage relationship between two tables"""

        request = CreateLineageRelationshipRequest()
        request.upstream_data_node_id = upstream_data_node_id
        request.downstream_data_node_id = downstream_data_node_id

        url = '/api/v1/lineage/relationships'

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return LineageRelationship().from_dict(response)

    def delete_lineage_relationship(self,
                                    *,
                                    relationship_id: int):

        url = f"/api/v1/lineage/relationships/{relationship_id}"
        log.info(f"Deleting lineage relationship with ID: {relationship_id}")
        self._call_datawatch(Method.DELETE, url=url)

    def create_lineage_edge(self,
                            upstream_data_node_id: int,
                            downstream_data_node_id: int,
                            relationship_type: RelationshipType = RelationshipType.RELATIONSHIP_TYPE_LINEAGE) -> LineageEdgeV2:
        """Create lineage relationship between two objects"""

        request = CreateLineageEdgeV2Request()
        request.relationship_type = relationship_type
        request.upstream_data_node_id = upstream_data_node_id
        request.downstream_data_node_id = downstream_data_node_id

        url = '/api/v2/lineage/edges'
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return LineageEdgeV2().from_dict(response)

    def delete_lineage_relationship_for_node(self,
                                             *,
                                             data_node_id: int):

        url = f"/api/v1/lineage/nodes/{data_node_id}/relationships"
        log.info(f"Deleting lineage relationships for data node {data_node_id}")
        self._call_datawatch(Method.DELETE, url=url)

    def create_lineage_node(self,
                            node_name: str,
                            node_type: DataNodeType,
                            node_container_name: Optional[str] = None,
                            icon_url: Optional[str] = None) -> LineageNodeV2:
        url = '/api/v2/lineage/nodes'
        request = CreateLineageNodeV2Request()
        request.node_name = node_name
        request.icon_url = icon_url

        if node_container_name:
            request.node_container_name = node_container_name

        request_dict = request.to_dict()
        request_dict["nodeType"] = node_type
        response = self._call_datawatch(Method.POST, url=url, body=json.dumps(request_dict))
        return LineageNodeV2().from_dict(response)

    def delete_lineage_node(self, node_id: int):
        url = f'/api/v2/lineage/nodes/{node_id}'
        log.info(f"Deleting lineage node with ID: {node_id}")
        return self._call_datawatch(Method.DELETE, url=url)

    def get_lineage_graph_from_data_node(self,
                                         *,
                                         data_node_id: int,
                                         depth: int = 1,
                                         direction: LineageDirection = LineageDirection.ALL,
                                         timeout: Optional[int] = None) -> TableLineageV2Response:
        url = f"/api/v2/lineage/nodes/{data_node_id}/graph?depth={depth}&direction={direction}"
        return TableLineageV2Response().from_dict(
            self._call_datawatch(Method.GET, url=url, timeout=timeout)
        )

    def execute_lineage_workflow(self, source_id: int):
        """Run lineage collection process for a source. For non-cloud warehouse vendors (Snowflake, Bigquery, Redshift)
        this will only create the necessary containment edges (source -> table -> column)"""
        url = f"/api/v1/lineage/sources/{source_id}/lineage/workflow"
        log.info(f"Kicking off lineage workflow for source: {source_id}")
        response: WorkflowStatusResponse = WorkflowStatusResponse().from_dict(
            self._call_datawatch(Method.POST, url=url)
        )

        status_url = f"/api/v1/lineage/status/{response.workflow_id}"
        while response.status == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_QUEUED or \
                response.status == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_IN_PROGRESS:
            log.info(f"Processing source {source_id} for lineage...")
            time.sleep(10)
            wsr: WorkflowStatusResponse = WorkflowStatusResponse().from_dict(
                self._call_datawatch(Method.GET, url=status_url))
            response.status = wsr.status

        log.info(f"Workflow finished with status {response.status}")

        if response.status != WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_COMPLETED:
            err = f"Workflow was not completed. Final status: {response.status.name}"
            raise Exception(err)

    def upsert_metric_template(self,
                               *,
                               id: int,
                               name: str,
                               template: str,
                               return_type: Union[SimpleFieldType.BOOLEAN, SimpleFieldType.NUMERIC],
                               parameters: List[str],
                               source: Optional[Source] = None) -> CreateMetricTemplateResponse:

        metric_template = MetricTemplate()
        request = CreateMetricTemplateRequest()
        params = []

        metric_template.id = id
        metric_template.name = name
        metric_template.template = template
        metric_template.return_type = FieldType.from_string(
            f"{SimpleFieldType.get_protobuf_type_prefix()}_{return_type}")

        for p in parameters:
            kv = p.split("=")
            key = kv[0]
            value = MetricTemplateParameterType.from_string(
                f"{SimpleMetricTemplateParameterType.get_protobuf_type_prefix()}_{kv[1]}"
            )
            temp_param = MetricTemplateParametersFieldEntry(key=key, value=value)
            params.append(temp_param)

        metric_template.parameters = params
        if source:
            metric_template.source = Warehouse(id=source.id, name=source.name, warehouse_vendor=source.database_type)

        request.metric_template = metric_template

        url = "/api/v1/metric-templates"

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return CreateMetricTemplateResponse().from_dict(response)

    def delete_metric_template(self,
                               *,
                               template_id: int):
        url = f"/api/v1/metric-templates/{template_id}"
        log.info(f"Deleting template with ID: {template_id}")
        self._call_datawatch(Method.DELETE, url=url)

    def get_all_metric_templates(self,
                                 *,
                                 page_size: int = 0,
                                 page_cursor: str = "",
                                 sort_field: MetricTemplateSortField = 0,
                                 sort_direction: SortDirection = 0,
                                 search: str = "") -> List[MetricTemplate]:
        request = GetMetricTemplateListRequest()
        request.page_size = page_size
        request.page_cursor = page_cursor
        request.sort_field = sort_field
        request.sort_direction = sort_direction
        request.search = search

        url = "/api/v1/metric-templates/fetch"

        response = GetMetricTemplateListResponse().from_dict(
            self._call_datawatch(method=Method.POST, url=url, body=request.to_json())
        )

        metric_templates: List[MetricTemplate] = response.metric_templates

        while response.pagination_info.next_cursor:
            request.page_cursor = response.pagination_info.next_cursor
            response = GetMetricTemplateListResponse().from_dict(
                self._call_datawatch(method=Method.POST, url=url, body=request.to_json())
            )
            metric_templates.extend(response.metric_templates)

        return metric_templates

    def create_virtual_table(self,
                             *,
                             name: str,
                             sql: str,
                             warehouse_id: int) -> VirtualTable:
        request = VirtualTableRequest(name=name, sql=sql, warehouse_id=warehouse_id)
        url = "/api/v1/virtual-tables"
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return VirtualTable().from_dict(response)

    def update_virtual_table(self,
                             *,
                             id: int,
                             name: str,
                             sql: str,
                             warehouse_id: int):
        update_request = VirtualTableRequest(name=name, sql=sql, warehouse_id=warehouse_id)

        url = f"/api/v1/virtual-tables/{id}"
        self._call_datawatch(Method.PUT, url=url, body=update_request.to_json())

    def delete_virtual_table(self,
                             *,
                             table_id: int):

        url = f"/api/v1/virtual-tables/{table_id}"
        log.info(f"Deleting virtual table with ID: {table_id}")
        self._call_datawatch(Method.DELETE, url=url)

    def get_all_virtual_tables(self) -> List[VirtualTable]:

        url = "/api/v1/virtual-tables"
        # TODO: Change to response from protobuf when available
        response = [VirtualTable(table=Table().from_dict(vt['table']), sql_query=vt['sqlQuery'])
                    for vt in self._call_datawatch(Method.GET, url=url)]
        return response

    def get_virtual_tables(self,
                           *,
                           source_ids: List[int] = (),
                           schema_ids: List[int] = (),
                           tabled_ids: List[int] = (),
                           page_size: int = 0,
                           page_cursor: str = "",
                           search: str = "",
                           ignore_fields: bool = False
                           ) -> List[VirtualTable]:

        url = "/api/v1/virtual-tables/fetch"

        locals().pop("self")
        request = GetVirtualTableListRequest().from_dict(locals())
        response = GetVirtualTableListResponse().from_dict(
            self._call_datawatch(Method.POST, url=url, body=request.to_json())
        )
        virtual_tables: List[VirtualTable] = response.virtual_tables

        while response.pagination_info.next_cursor:
            request.page_cursor = response.pagination_info.next_cursor
            response = GetVirtualTableListResponse().from_dict(
                self._call_datawatch(Method.POST, url=url, body=request.to_json())
            )
            virtual_tables.extend(response.virtual_tables)

        return virtual_tables

    def fetch_schema_changes(self,
                             *,
                             page_size: int = 0,
                             page_cursor: str = "",
                             sort_field: SchemaChangeSortField = 0,
                             sort_direction: SortDirection = 0,
                             search: str = "",
                             source_id: Optional[int] = None,
                             schema_id: Optional[int] = None,
                             table_id: Optional[int] = None,
                             column_id: Optional[int] = None) -> List[SchemaChange]:

        request = GetSchemaChangesRequest()
        request.page_size = page_size
        request.page_cursor = page_cursor
        request.sort_field = sort_field
        request.sort_direction = sort_direction
        request.search = search
        request.source_id = source_id
        request.schema_id = schema_id
        request.table_id = table_id
        request.column_id = column_id

        url = "/api/v1/schema-changes/fetch"

        response = GetSchemaChangesResponse().from_dict(
            self._call_datawatch(Method.POST, url=url, body=request.to_json())
        )

        schema_changes: List[SchemaChange] = response.schema_changes

        while response.pagination_info.next_cursor:
            request.page_cursor = response.pagination_info.next_cursor
            response = GetSchemaChangesResponse().from_dict(
                self._call_datawatch(method=Method.POST, url=url, body=request.to_json())
            )
            schema_changes.extend(response.schema_changes)

        return schema_changes

    def get_integrations(self) -> List[Integration]:

        url = "/api/v1/integrations"
        return IntegrationsResponse().from_dict(
            self._call_datawatch(Method.GET, url=url)
        ).integrations

    def get_integration_entities(self, *, integration_id: int) -> GetIntegrationEntitiesResponse:
        url = f"/api/v1/integrations/{integration_id}/entities"
        return GetIntegrationEntitiesResponse().from_dict(
            self._call_datawatch(Method.GET, url=url)
        )

    def get_advanced_configs(self) -> List[ConfigValue]:
        url = "/api/v1/configs/fetch"
        return GetConfigListResponse().from_dict(
            self._call_datawatch(Method.POST, url=url)
        ).advanced_configs

    def update_advanced_configs(
            self, *, key: str = "", value: Union[str, int, bool] = "", config_values: Optional[List[dict]] = None
    ):
        url = "/api/v1/configs/"
        if not config_values:
            config_values = {"key": key}
            if isinstance(value, str):
                config_values.update(
                    {"stringValue": value, "type": ConfigValueType.VALUE_TYPE_STRING.name}
                )
            elif isinstance(value, bool):
                config_values.update(
                    {"booleanValue": value, "type": ConfigValueType.VALUE_TYPE_BOOL.name}
                )
            else:
                config_values.update(
                    {"numberValue": value, "type": ConfigValueType.VALUE_TYPE_INTEGER.name}
                )

        update_request = {"advancedConfigs": [config_values]}
        self._call_datawatch(Method.PUT, url=url, body=json.dumps(update_request))

    def rebuild_schema(self, schema_id: int) -> WorkflowResponse:
        url = f"/api/v1/rebuilds/schemas/{schema_id}"
        return WorkflowResponse().from_dict(
            self._call_datawatch(method=Method.POST, url=url)
        )

    def rebuild_source(self, source_id: int, priority: int = 1) -> WorkflowResponse:
        url = f"/api/v1/rebuilds/sources/{source_id}"
        request = RebuildSourceRequest(priority=priority)
        return WorkflowResponse().from_dict(
            self._call_datawatch(method=Method.POST, url=url, body=request.to_json())
        )

    def get_workflow_status(self, workflow_id: int) -> WorkflowStatusResponse:
        url = f"/api/v1/workflows/{workflow_id}/status"
        return WorkflowStatusResponse().from_dict(
            self._call_datawatch(method=Method.GET, url=url)
        )

    def get_workspaces(self) -> WorkspaceListResponse:
        url = '/api/v1/workspaces'
        response = self._call_datawatch(Method.GET, url=url)
        return WorkspaceListResponse().from_dict(response)

    def get_workspace(self, *, workspace_id: int) -> Workspace:
        url = f'/api/v1/workspaces/{workspace_id}'
        response = self._call_datawatch(Method.GET, url=url)
        return Workspace().from_dict(response)

    def create_workspace(self, workspace_name: str) -> Workspace:
        url = '/api/v1/workspaces'
        request = CreateOrUpdateWorkspaceRequest(name=workspace_name)
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return Workspace().from_dict(response)

    def update_workspace(self, workspace_name: str, workspace_id: int) -> Workspace:
        url = f'/api/v1/workspaces/{workspace_id}'
        request = CreateOrUpdateWorkspaceRequest(name=workspace_name)
        response = self._call_datawatch(Method.PUT, url=url, body=request.to_json())
        return Workspace().from_dict(response)

    def delete_workspace(self, workspace_id: int):
        url = f'/api/v1/workspaces/{workspace_id}'
        return self._call_datawatch(Method.DELETE, url=url)

    def get_workspace_accessors(self, *, workspace_id: int) -> GetWorkspaceAccessorsResponse:
        url = f"/api/v1/workspaces/{workspace_id}/accessors"
        return GetWorkspaceAccessorsResponse().from_dict(
            self._call_datawatch(Method.GET, url=url)
        )

    def get_users(self) -> GetUserListResponse:
        url = '/user'
        response = self._call_datawatch(Method.GET, url=url)
        return GetUserListResponse().from_dict(response)

    def invite_user(self, user_name: str, user_email: str, group_ids: List[int]):
        url = '/api/v1/users'
        request = UserInviteRequest(name=user_name, email=user_email, group_ids=group_ids)
        return User().from_dict(self._call_datawatch(Method.POST, url=url, body=request.to_json()))

    def delete_user(self, user_id: int):
        url = f'/user/{user_id}'
        return self._call_datawatch(Method.DELETE, url=url)

    def edit_users_groups(self, user_ids: List[int], group_ids: List[int],
                          operation: GroupUserOperation) -> BulkChangeGroupUsersResponse:
        url = '/api/v1/groups/users'
        request = BulkChangeGroupUsersRequest(user_ids=user_ids,
                                              group_ids=group_ids,
                                              operation=operation)
        response = self._call_datawatch(Method.PUT, url=url, body=request.to_json())
        return BulkChangeGroupUsersResponse().from_dict(response)

    def get_groups(self) -> GroupListResponse:
        url = '/api/v1/groups'
        response = self._call_datawatch(Method.GET, url=url)
        return GroupListResponse().from_dict(response)

    def create_group(self, group_name: str) -> Group:
        url = '/api/v1/groups'
        request = CreateOrUpdateGroupRequest(name=group_name)
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return Group().from_dict(response)

    def update_group(self, group_name: str, group_id: int) -> Group:
        url = f'/api/v1/groups/{group_id}'
        request = CreateOrUpdateGroupRequest(name=group_name)
        response = self._call_datawatch(Method.PUT, url=url, body=request.to_json())
        return Group().from_dict(response)

    def delete_group(self, group_id: int):
        url = f'/api/v1/groups/{group_id}'
        return self._call_datawatch(Method.DELETE, url=url)

    def get_roles(self) -> RoleV2ListResponse:
        url = '/api/v1/roles'
        response = self._call_datawatch(Method.GET, url=url)
        return RoleV2ListResponse().from_dict(response)

    def edit_group_roles(self, group: Group, role: RoleV2, workspace_ids: List[int], operation: RoleOperation) -> BulkChangeGroupGrantsResponse:
        url = '/api/v1/groups/grants'
        grants: List[Grant] = []

        if operation == RoleOperation.ROLE_OPERATION_GRANT:
            for wid in workspace_ids:
                grants.append(Grant(
                    role=role,
                    group=IdAndDisplayName(id=group.id, display_name=group.name),
                    workspace=IdAndDisplayName(id=wid)
                ))
        elif operation == RoleOperation.ROLE_OPERATION_REVOKE:
            for grant in group.grants:
                if grant.workspace.id in workspace_ids:
                    grants.append(grant)
        else:
            raise Exception(f'Role operation {operation} not supported.')

        request = BulkChangeGroupGrantsRequest(
            operation=operation,
            requests=grants
        )
        response = self._call_datawatch(Method.PUT, url=url, body=request.to_json())
        return BulkChangeGroupGrantsResponse().from_dict(response)

    def get_columns(self, table_ids: List[int] = [], column_ids: List[int] = []) -> GetColumnListResponse:
        url = '/api/v1/columns/fetch'
        request = GetColumnListRequest(table_ids=table_ids, column_ids=column_ids)
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return GetColumnListResponse().from_dict(response)

    def create_custom_rule(self,
                           warehouse_id: int,
                           name: str,
                           sql: str,
                           threshold_type: CustomRulesThresholdType = None,
                           upper_threshold: Optional[float] = None,
                           lower_threshold: Optional[float] = None,
                           collection_ids: Optional[List[int]] = None,
                           schedule: Optional[MetricSchedule] = None,
                           owner_id: Optional[int] = None) -> CustomRuleInfo:
        """Create a new custom rule."""
        url = '/api/v1/custom-rules'
        rule = CustomRule()
        rule.warehouse_id = warehouse_id
        rule.name = name
        rule.sql = sql
        rule.threshold_type = threshold_type
        rule.upper_threshold = upper_threshold
        rule.lower_threshold = lower_threshold
        rule.collection_ids = collection_ids or []

        if not schedule:
            rule.metric_schedule = MetricSchedule(
                schedule_frequency=TimeInterval(
                    interval_type=TimeIntervalType.HOURS_TIME_INTERVAL_TYPE,
                    interval_value=24
                )
            )
        else:
            rule.metric_schedule = schedule

        if owner_id:
            owner = [u for u in self.get_users().users if u.id == owner_id][0]
            rule.owner = owner

        request = CreateCustomRuleRequest()
        request.custom_rule = rule

        # this is done so that default 0 values are not removed when converting to json
        request_dict = request.to_dict()
        request_dict["customRule"]["upperThreshold"] = upper_threshold
        request_dict["customRule"]["lowerThreshold"] = lower_threshold
        request_json = json.dumps(request_dict)

        response = self._call_datawatch(Method.POST, url=url, body=request_json)
        return CustomRuleInfo().from_dict(response)

    def edit_custom_rule(self,
                         custom_rule: CustomRule,
                         rule_id: int) -> CustomRuleInfo:
        """Edit an existing custom rule."""
        url = f'/api/v1/custom-rules/{rule_id}'
        request = UpdateCustomRuleRequest()
        request.custom_rule = custom_rule
        request.id = rule_id

        # this is done so that default 0 values are not removed when converting to json
        request_dict = request.to_dict()
        request_dict["customRule"]["upperThreshold"] = request.custom_rule.upper_threshold
        request_dict["customRule"]["lowerThreshold"] = request.custom_rule.lower_threshold
        request_json = json.dumps(request_dict)

        response = self._call_datawatch(Method.PUT, url=url, body=request_json)
        return CustomRuleInfo().from_dict(response)

    def get_rule_by_id(self, rule_id: int) -> CustomRuleInfo:
        """Get a single rule by ID."""
        url = f'/api/v1/custom-rules/{rule_id}'
        response = self._call_datawatch(Method.GET, url=url)
        return CustomRuleInfo().from_dict(response)

    def get_rules_for_collection(self, collection_id: int) -> GetCustomRuleListResponse:
        """Get all rules for a given collection."""
        url = f'/api/v1/custom-rules/collection/{collection_id}'
        response = self._call_datawatch(Method.GET, url=url)

        rlist_current = GetCustomRuleListResponse().from_dict(response)
        rlist_total = GetCustomRuleListResponse()
        rlist_total.custom_rules.extend(rlist_current.custom_rules)

        while rlist_current.pagination_info.next_cursor:
            response.page_cursor = rlist_current.pagination_info.next_cursor
            response = self._call_datawatch(Method.POST, url=url, body=response.to_json())
            rlist_current = GetCustomRuleListResponse().from_dict(response)
            rlist_total.custom_rules.extend(rlist_current.custom_rules)

        return rlist_total

    def get_rules_for_source(self, warehouse_id: int) -> GetCustomRuleListResponse:
        """Get all rules for a given warehouse"""
        url = f'/api/v1/custom-rules/warehouse/{warehouse_id}'
        response = self._call_datawatch(Method.GET, url=url)

        rlist_current = GetCustomRuleListResponse().from_dict(response)
        rlist_total = GetCustomRuleListResponse()
        rlist_total.custom_rules.extend(rlist_current.custom_rules)

        while rlist_current.pagination_info.next_cursor:
            response.page_cursor = rlist_current.pagination_info.next_cursor
            response = self._call_datawatch(Method.POST, url=url, body=response.to_json())
            rlist_current = GetCustomRuleListResponse().from_dict(response)
            rlist_total.custom_rules.extend(rlist_current.custom_rules)

        return rlist_total

    def delete_custom_rule(self, id: int):
        """Delete a custom rule."""
        url = f'/api/v1/custom-rules/{id}'
        return self._call_datawatch(Method.DELETE, url=url)

    def get_custom_rule_list(self,
                             *,
                             search: str = "",
                             page_size: int = 0,
                             source_id: int = 0,
                             schema_id: int = 0,
                             table_id: int = 0,
                             column_id: int = 0,
                             collection_id: int = 0,
                             join_id: int = 0):
        url = "/api/v1/custom-rules/fetch"
        request = GetCustomRuleListRequest(
            search=search,
            page_size=page_size,
            source_id=source_id,
            schema_id=schema_id,
            table_id=table_id,
            column_id=column_id,
            collection_id=collection_id,
            join_id=join_id
        )

        rlist_current = GetCustomRuleListResponse().from_dict(
            self._call_datawatch(method=Method.POST, url=url, body=request.to_json())
        )
        rlist_total = GetCustomRuleListResponse()
        rlist_total.custom_rules.extend(rlist_current.custom_rules)

        while rlist_current.pagination_info.next_cursor:
            rlist_current.page_cursor = rlist_current.pagination_info.next_cursor
            response = self._call_datawatch(Method.POST, url=url, body=rlist_current.to_json())
            rlist_current = GetCustomRuleListResponse().from_dict(response)
            rlist_total.custom_rules.extend(rlist_current.custom_rules)

        return rlist_total

    def get_personal_api_keys(self) -> ListPersonalApiKeyResponse:
        url = "/api/v1/personal-api-keys"
        return ListPersonalApiKeyResponse().from_dict(
            self._call_datawatch(Method.GET, url=url)
        )

    def create_personal_api_key(self, *, name: str, description: Optional[str] = "") -> CreatePersonalApiKeyResponse:
        url = "/api/v1/personal-api-keys"
        request = CreatePersonalApiKeyRequest()
        request.name = name
        request.description = description
        return CreatePersonalApiKeyResponse().from_dict(
            self._call_datawatch(Method.POST, url=url, body=request.to_json())
        )

    def delete_personal_api_key(self, *, id: int):
        url = f"/api/v1/personal-api-keys/{id}"
        self._call_datawatch(Method.DELETE, url=url)

    def get_agent_api_keys(self) -> ListAgentApiKeyResponse:
        url = "/api/v1/agent-api-keys"
        return ListAgentApiKeyResponse().from_dict(
            self._call_datawatch(Method.GET, url=url)
        )

    def create_agent_api_key(self, *, name: str, description: Optional[str] = "") -> CreateAgentApiKeyResponse:
        url = "/api/v1/agent-api-keys"
        request = CreateAgentApiKeyRequest()
        request.name = name
        request.description = description
        return CreateAgentApiKeyResponse().from_dict(
            self._call_datawatch(Method.POST, url=url, body=request.to_json())
        )

    def delete_agent_api_key(self, *, id: int):
        url = f"/api/v1/agent-api-keys/{id}"
        self._call_datawatch(Method.DELETE, url=url)

    def bulk_create_lineage_nodes(self, nodes: List[CreateLineageNodeV2Request]):
        url = "/api/v2/lineage/nodes/bulk"
        request = CreateLineageNodeV2BulkRequest()
        request.nodes = nodes
        return self._call_datawatch(Method.POST, url=url, body=request.to_json())

    def bulk_create_lineage_edges(self, edges: List[CreateLineageEdgeV2Request]):
        url = "/api/v2/lineage/edges/bulk"
        request = CreateLineageEdgeV2BulkRequest()
        request.edges = edges
        return self._call_datawatch(Method.POST, url=url, body=request.to_json())

    def get_bulk_metric_observed_column(
            self,
            *,
            metric_ids: List[int] = [],
            column_ids: List[int] = [],
            table_ids: List[int] = [],
            schema_ids: List[int] = [],
            source_ids: List[int] = [],
            is_for_custom_rule: bool = False,
            remove_duplicate_metrics: bool = False
    ) -> MetricObservedColumnListResponse:
        url = "/api/v1/metric-observed-column/bulk-list"
        request = GetMetricObservedColumnBulkRequest(
            metric_ids=metric_ids,
            column_ids=column_ids,
            table_ids=table_ids,
            schema_ids=schema_ids,
            source_ids=source_ids,
        ).to_dict()

        request.update({"isForCustomRule": is_for_custom_rule, "removeDuplicateMetrics": remove_duplicate_metrics})
        return MetricObservedColumnListResponse().from_dict(
            self._call_datawatch(method=Method.POST, url=url, body=json.dumps(request))
        )

    def create_metric_observed_column(
            self, *, column_id: int, metric_id: int, comments: Optional[str] = None
    ) -> MetricObservedColumnResponse:
        url = "/api/v1/metric-observed-column"
        request = MetricObservedColumnRequest(column_id=column_id, metric_id=metric_id, comments=comments)
        return MetricObservedColumnResponse().from_dict(
            self._call_datawatch(method=Method.POST, url=url, body=request.to_json())
        )

    def get_metric_observed_column_for_metric(self, *, metric_id: int) -> MetricObservedColumnListResponse:
        url = f"/api/v1/metric-observed-column/metric/{metric_id}"
        return MetricObservedColumnListResponse().from_dict(
            self._call_datawatch(method=Method.GET, url=url)
        )

    def get_metric_observed_column_for_column(self, *, column_id: int) -> MetricObservedColumnListResponse:
        url = f"/api/v1/metric-observed-column/column/{column_id}"
        return MetricObservedColumnListResponse().from_dict(
            self._call_datawatch(method=Method.GET, url=url)
        )
