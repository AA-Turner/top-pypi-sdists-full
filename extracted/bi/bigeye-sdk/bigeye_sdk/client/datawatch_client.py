from __future__ import annotations

import json
import os
import time
from abc import ABC
from json import JSONDecodeError
from typing import List, Optional, Dict, Tuple, Union

from requests.auth import HTTPBasicAuth

from bigeye_sdk.exceptions import InvalidConfigurationException
from typing_extensions import deprecated

import requests

from bigeye_sdk.authentication.api_authentication import BasicAPIAuth, BrowserAPIAuth, ApiAuth, APIKeyAuth
from bigeye_sdk.bigconfig_validation.big_config_reports import MetricSuiteReport, ProcessStage
from bigeye_sdk.client.base_client import BaseApiClient
from bigeye_sdk.client.enum import Method
from bigeye_sdk.authentication.config import WorkspaceConfig
from bigeye_sdk.client.generated_datawatch_client import GeneratedDatawatchClient
from bigeye_sdk.exceptions.exceptions import NoSourcesFoundException, TableNotFoundException, \
    BigconfigIncompleteException, WorkspaceNotSetException, AuthenticationFailedException, CollectionNotFoundException
from bigeye_sdk.functions.delta_functions import infer_column_mappings, build_ccm
from bigeye_sdk.functions.metric_functions import set_default_model_type_for_threshold, is_freshness_metric
from bigeye_sdk.functions.table_functions import get_table_column_priority_first, table_has_metric_time, \
    fully_qualified_table_to_elements
from bigeye_sdk.generated.com.bigeye.models._generated_root import TagItem, WorkflowV2Id, WorkflowV2StatusResponse, \
    BulkWorkflowV2StatusRequest, BulkWorkflowV2StatusResponse
from bigeye_sdk.generated.com.bigeye.models.generated import (
    MetricConfiguration,
    MetricType,
    CreateComparisonTableResponse,
    CreateComparisonTableRequest,
    ComparisonTableConfiguration,
    IdAndDisplayName,
    ComparisonColumnMapping,
    ColumnNamePair,
    Table,
    GetDebugQueriesResponse,
    Schema,
    Source,
    MetricSuite,
    MetricSuiteResponse,
    MetricNamesResponse,
    WorkflowStatusResponse,
    WorkflowProcessingStatus,
    UserAuth,
    BigconfigWorkflowStatusResponse,
    MetricCreationState,
    LookbackType,
    TimeInterval,
    MetricParameter,
    NotificationChannel,
    Threshold,
    CatalogAttribute,
    SetCatalogAttributeRequest,
    CatalogAttributeResponse,
    GetCatalogAttributeRequest,
    UpsertDeltaRequest,
    Delta,
    UpsertDeltaResponse,
    OwnableType,
    SetObjectOwnerRequest,
    TableLineageV2Response,
    ObjectOwnerResponse, SendDbtCoreRunInfoResponse, SendDbtCoreRunInfoRequest, CustomRuleBulkRequest, BulkResponse,
    CustomRulesThresholdType, MetricSchedule, CustomRuleInfo,
    SearchResponse, SearchRequest, DataNodeType,
    GetCustomRuleListResponse, Workspace, User, BigconfigWorkflowV2StatusResponse, IssueAssignmentUpdate,
    UpdateIssueRequest, UpdateIssueResponse, Issue, CustomIntegrationType, GetCustomIntegrationTypesResponse,
    CustomRepository, GetCustomRepositoriesResponse, CustomNodeType, BulkCreateCustomNodeTypesRequest,
    GetCustomNodeTypesResponse, LineageNodeV2, CreateLineageNodeV2Request, CreateLineageNodeV2BulkRequest,
    CustomRepositorySyncRequest, CustomRepositorySyncResponse,
    ExternalMonitorRunRequest, MetricInfo,
    IntegrationType, GetCatalogEntityChildrenResponse, GetCatalogEntityChildrenRequest, Tag, TagRequest, TagResponse,
    UntagRequest, UntagResponse, CreateOrUpdateTagRequest, CreateOrUpdateTagResponse, DeleteTagResponse,
    GetAllTagsRequest, GetAllTagsResponse, GetTagItemResponse, GetMetricRunsRequest, GetMetricRunsResponse,
    GetMetricRunsBulkRequest, GetMetricRunsBulkResponse, MetricIdentifier, Collection
)

from bigeye_sdk.log import get_logger
from bigeye_sdk.model.delta_facade import SimpleDeltaConfiguration
from bigeye_sdk.model.integration_facade import SimpleCustomIntegration, CustomIntegrationDeploymentResult
from bigeye_sdk.model.metric_facade import SimpleUpsertMetricRequest
from bigeye_sdk.model.protobuf_enum_facade import SimpleCatalogEntityType
from bigeye_sdk.model.protobuf_extensions import MetricDebugQueries

log = get_logger(__name__)


def datawatch_client_factory(auth: ApiAuth, workspace_config: WorkspaceConfig = None, workspace_id: int = None):
    if isinstance(auth, (BasicAPIAuth, BrowserAPIAuth, APIKeyAuth)):
        if workspace_config:
            client = DatawatchClient(auth=auth, workspace_config=workspace_config)
        elif workspace_id:
            client = DatawatchClient(auth=auth, workspace_config=WorkspaceConfig(workspace_id=workspace_id))
        else:
            accessible_workspaces = get_user_auth(auth).workspaces
            if len(accessible_workspaces) == 1:
                # User has access to only 1 workspace, fallback to that
                log.info(f"No workspace provided, defaulting to only valid workspace: {accessible_workspaces[0].name}")
                workspace_config = WorkspaceConfig(workspace_id=accessible_workspaces[0].id)
                client = DatawatchClient(auth=auth, workspace_config=workspace_config)
            elif len(accessible_workspaces) > 1:
                # User has access to more than 1 workspace, need to confirm correct one
                raise WorkspaceNotSetException(f'Expected either workspace_config or workspace_id args to be passed.')
            else:
                # User has access to no workspaces - throw an error to let them know
                raise WorkspaceNotSetException(f'No workspace access detected. Please check with your Bigeye '
                                               'administrators to obtain access to a workspace.')
    else:
        raise Exception('Auth type not supported.')
    return client


def get_user_auth(auth: ApiAuth) -> UserAuth:
    url = '/auth'
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}
    if isinstance(auth, BasicAPIAuth):
        # basic auth not supported for /auth endpoint
        # need to get cookies by first posting login request in session
        session = requests.Session()
        login = {"basic-email": (None, auth.user),
                 "basic-password": (None, auth.password)}
        session.post(url=f'{auth.base_url}/ajaxsignin',
                     files=login)
        response = session.get(
            url=f'{auth.base_url}{url}',
            headers=headers)
    elif isinstance(auth, BrowserAPIAuth):
        response = requests.get(
            url=f'{auth.base_url}{url}',
            cookies=auth.auth_factory().get_cookies(),
            headers=headers)
    # API key not supported for /auth or /ajaxsignin
    elif isinstance(auth, APIKeyAuth):
        raise WorkspaceNotSetException("Workspace ID is required when using API key authentication.")

    if response.status_code < 200 or response.status_code >= 300:
        log.error("Error trying to retrieve workspaces.")
        if response.status_code == 401:
            raise AuthenticationFailedException(
                "Authentication failed. Verify credentials or that you are logged in to Bigeye via a supported browser."
            )
        raise Exception(f'Error returned from datawatch: {response.status_code} - {response.reason}')

    return UserAuth().from_dict(response.json())


def __get_all_workspace_client(cred: ApiAuth) -> DatawatchClient:
    return datawatch_client_factory(
        auth=cred, workspace_config=WorkspaceConfig(workspace_id=0)
    )


def create_api_key_for_configuration(cred: ApiAuth, name: str, description: Optional[str] = "") -> str:
    return __get_all_workspace_client(cred=cred).create_personal_api_key(name=name, description=description).api_key


def create_agent_api_key(cred: ApiAuth, name: str, description: Optional[str] = "") -> str:
    return __get_all_workspace_client(cred=cred).create_agent_api_key(name=name, description=description).api_key


def create_integration_api_key(cred: ApiAuth, name: str, description: Optional[str] = "") -> str:
    return __get_all_workspace_client(cred=cred).create_integration_api_key(name=name, description=description).api_key


def get_all_workspaces_for_login(cred: ApiAuth) -> List[Workspace]:
    return __get_all_workspace_client(cred=cred).get_workspaces().workspaces


def get_all_users_for_login(cred: ApiAuth) -> List[User]:
    return __get_all_workspace_client(cred=cred).get_users().users


def get_allowed_emails_for_workspace(cred: ApiAuth, workspace_id: int) -> List[str]:
    return [user.email.lower() for user in
            __get_all_workspace_client(cred=cred).get_workspace_accessors(workspace_id=workspace_id).users
            ]


def verify_agent_api_key(base_url: str, agent_api_key: str) -> bool:
    response = requests.get(url=f"{base_url}/api/v1/agent-api-keys/verify",
                            headers={"Authorization": f"apikey {agent_api_key}"})
    return True if response.status_code == 204 else False


def verify_personal_api_key(base_url: str, personal_api_key: str) -> bool:
    response = requests.get(url=f"{base_url}/api/v1/personal-api-keys/verify",
                            headers={"Authorization": f"apikey {personal_api_key}"})
    return True if response.status_code == 204 else False


class DatawatchClient(BaseApiClient, GeneratedDatawatchClient, ABC):

    def __init__(self, auth: BasicAPIAuth | BrowserAPIAuth | APIKeyAuth, workspace_config: WorkspaceConfig):
        super().__init__(base_url=auth.base_url)
        self._auth = auth
        self.config = workspace_config

    def _call_datawatch_impl(
            self,
            method: Method,
            url,
            body: str = None,
            params: dict = None,
            timeout: int = None,
            proxies: dict = {}):
        try:
            fq_url = f'{self._base_url}{url}'
            log.info(f'Request Type: {method.name}; URL: {fq_url}; Body: {body}')
            headers = {"Content-Type": "application/json",
                       "Accept": "application/json",
                       "x-bigeye-workspace-id": f'{self.config.workspace_id}'}

            kwargs = {
                'url': fq_url,
                'headers': headers,
                'data': body,
                'params': params,
                'timeout': timeout,
                'proxies': proxies
            }

            # Update headers with authentication
            headers.update(self._auth.get_auth_headers())
            # Add support for custom proxy authentication if configured.
            proxy_user = os.environ.get('BIGEYE_PROXY_AUTH_USER', None)
            proxy_pass = os.environ.get('BIGEYE_PROXY_AUTH_PASSWORD', None)
            custom_auth_header_key = os.environ.get('BIGEYE_AUTH_HEADER_KEY', None)

            # Validate proxy configuration - ensure custom header key is set to avoid conflicts
            if (proxy_user or proxy_pass) and not custom_auth_header_key:
                raise InvalidConfigurationException(
                    "ERROR: When using proxy authentication (BIGEYE_PROXY_AUTH_USER/BIGEYE_PROXY_AUTH_PASSWORD), "
                    "you must also set BIGEYE_AUTH_HEADER_KEY to avoid conflicts with the proxy auth header. "
                    "Example: export BIGEYE_AUTH_HEADER_KEY='x-vendor-auth'"
                )

            if proxy_user and proxy_pass:
                kwargs['auth'] = HTTPBasicAuth(proxy_user, proxy_pass)

            if method == Method.GET:
                response = requests.get(**kwargs)
            elif method == Method.POST:
                response = requests.post(**kwargs)
            elif method == Method.PUT:
                response = requests.put(**kwargs)
            elif method == Method.DELETE:
                response = requests.delete(**kwargs)
            else:
                raise Exception(f'Unsupported http method {method}')
        except Exception as e:
            log.error(f'Exception calling datawatch: {str(e)}')
            raise e
        else:
            log.info(f'Return Code: {response.status_code}')
            if response.status_code < 200 or response.status_code >= 300:
                if response.status_code == 401:
                    raise AuthenticationFailedException(
                        "API returned 401 unauthorized. Verify the auth method being used is correct."
                    )
                log.error(f'Error code returned from datawatch: {response.status_code} - {response.reason}')
                raise Exception(response.text)
            else:
                # Not empty response
                if response.status_code != 204:
                    try:
                        return response.json()
                    except JSONDecodeError as e:
                        log.info(f'Cannot decode response.  {response}')
                        return ''

    def delete_metrics(self, metrics: List[MetricConfiguration] = None):
        """
        Deletes multiple metrics.
        Args:
            metrics: List of metric configurations to delete.
        Warnings: Will log a warning when attempting to delete a metric created by Bigconfig.
        """

        for m in metrics:
            self.delete_metric(m)

    def get_table_level_metrics(self) -> MetricNamesResponse:
        return MetricNamesResponse().from_dict(self.get_table_level_metrics_raw())

    def get_table_level_metrics_raw(self) -> dict:
        url = '/api/v1/metrics/table-level-metric-names'
        return self._call_datawatch(Method.GET, url=url)

    def get_datawatch_json_response(self,
                                    method: Method,
                                    url: str,
                                    body: Optional[str],
                                    params: Optional[dict] = None,
                                    timeout: Optional[int] = None,
                                    proxies: Optional[dict] = {}
                                    ) -> dict:
        return self._call_datawatch(method, url, body=body, params=params, timeout=timeout, proxies=proxies)

    def get_sources_by_name(self, source_names: List[str] = None) -> Dict[str, Source]:
        """
        Creates a source index keyed by name and optionally limited by a list of names passed in.
        Args:
            source_names: names used to limit the index returned

        Returns: an index of sources that is keyed by name.

        """
        if not source_names:
            return {s.name: s for s in self.get_sources().sources}
        else:
            source_names = {s.name: s for s in self.get_sources().sources if s.name in source_names}
            if not source_names:
                raise Exception(f"No sources can be found for given source names. Please verify names and try again.")

            return source_names

    def get_schemas_by_fq_name(self, fq_schema_names: List[str]) -> Dict[str, Schema]:
        """
        Get schemas by fully qualified name.
        :param fq_schema_names: List of fully qualified schema names.  e.g. some_source.some_schema
        :return: Dictionary of schemas keyed by fully qualified schema name.
        """
        r: Dict[str, Schema] = {}
        for sn in fq_schema_names:
            split = sn.split('.')
            if len(split) != 3:
                raise Exception(f"Erroneous input.  Should be a fully qualified schema name.  Received: {sn}")

            warehouse_name, schema_name = split[0], '.'.join(split[-2:])
            source = self.get_sources_by_name(source_names=[warehouse_name])[warehouse_name]

            r[sn] = self.get_schemas_by_name(warehouse_id=source.id, schema_names=[schema_name])[schema_name]

        return r

    def get_schemas_by_name(self, warehouse_id: int, schema_names: List[str]) -> Dict[str, Schema]:
        """
        Builds a dictionary of schemas keyed by name.
        :param warehouse_id:
        :param schema_names:
        :return: Dict[schema_name:str, Schema]
        """
        schemas = self.get_schemas(warehouse_id=[warehouse_id])
        return {s.name: s for s in schemas.schemas if s.name in schema_names}

    def set_table_metric_time(self,
                              column_id: int):
        """
        Sets metric time by column id for a particular table.
        :param column_id: column id
        :return:
        """
        url = f'/dataset/loadedDate/{column_id}'
        self._call_datawatch(method=Method.PUT, url=url, body=None)

    def unset_table_metric_time(self,
                                table: Table):
        """
        Sets metric time by column id for a particular table.
        :param table: Table object
        :return:
        """

        if table_has_metric_time(table):
            url = f'/dataset/loadedDate/{table.metric_time_column.id}'
            log.info(f'Removing metric time from table: {table.database_name}.{table.schema_name}.{table.name}')
            self._call_datawatch(method=Method.DELETE, url=url, body=None)
        else:
            log.info(f'Table has no metric time set: {table.database_name}.{table.schema_name}.{table.name}')

    def _set_table_metric_times(self,
                                column_names: List[str],
                                tables: List[Table],
                                replace: bool = False
                                ):
        """Sets metric times on tables if a column matches, by order priority, and column name in the list of column
        names.  If replace is true then it will reset metric time on tables then it will do a backfill of all metrics
        in that table."""
        for t in tables:
            has_metric_time = table_has_metric_time(t)
            if not has_metric_time or replace:
                c = get_table_column_priority_first(table=t, column_names=column_names)
                if c:
                    log.info(f'Setting column {c.name} in table {t.database_name}.{t.schema_name}.{t.name} '
                             f'as metric time.')
                    self.set_table_metric_time(c.id)

                    if has_metric_time and replace:
                        mcs = self.search_metric_configuration(table_ids=[t.id])
                        mids = [mc.id for mc in mcs]
                        log.info(f'Backfilling metrics after replace.  Metric IDs: {mids}')
                        self.backfill_metric(metric_ids=mids)
                else:
                    log.info(f'No column name provided can be identified in table '
                             f'{t.database_name}.{t.schema_name}.{t.name}')

    def set_table_metric_times(self,
                               column_names: List[str],
                               table_ids: List[int],
                               replace: bool = False):
        """
        Accepts a list of column_names that are acceptable metric time columns and applies for a list of tables.
        :param replace: replace metric time if exists.
        :param column_names: names of columns that would be acceptable metric time columns.
        :param table_ids: the tables to apply metric times on.
        :return:
        """
        tables = self.get_tables(ids=table_ids).tables
        self._set_table_metric_times(tables=tables, column_names=column_names, replace=replace)

    def set_source_metric_times(self,
                                column_names: List[str],
                                wid: int,
                                sid: int,
                                replace: bool = False):
        """
        Accepts a list of column_names that are acceptable metric time columns and applies for the whole source.
        :param replace: replace metric time if exists.
        :param column_names: names of columns that would be acceptable metric time columns.
        :param wid: the wid to apply metric times on.
        :param sid: the Schema ID to apply metric times on.
        :return:
        """
        tables = self.get_tables(warehouse_id=[wid], schema_id=[sid]).tables
        self._set_table_metric_times(tables=tables, column_names=column_names, replace=replace)

    def unset_table_metric_times(self,
                                 table_ids: List[int]):
        """
        Unsets metric time for specified table ids.
        :param table_ids: table ids.
        :return:
        """
        tables = self.get_tables(ids=table_ids).tables
        for t in tables:
            self.unset_table_metric_time(t)

    def unset_source_metric_times(self,
                                  wid: int):
        """
        Unsets metric time for all tables in warehouse.
        :param wid: warehouse id.
        :return:
        """
        tables = self.get_tables(warehouse_id=[wid]).tables
        for t in tables:
            self.unset_table_metric_time(t)

    def delete_deltas_by_name(self, delta_names: List[str]):
        """
        Deletes deltas by string name.
        :param delta_names: list of delta names
        :return:
        """

        existing_delta_ids = [d.comparison_table_configuration.id
                              for d in self.get_delta_information(delta_ids=[], exclude_comparison_metrics=True)
                              if d.comparison_table_configuration.name in delta_names]
        for deltaid in existing_delta_ids:
            self.delete_delta(comparison_table_id=deltaid)

    def create_deltas_from_simple_conf(self, sdcl: List[SimpleDeltaConfiguration]) -> List[Delta]:
        """
        Creates Deltas from a SimpleDeltaConfigurationList.

        :param sdcl: Instance of SimpleDeltaConfigurationList

        :return: Resulting ComparisonTableConfiguration
        """

        # Delete if already exist.
        self.delete_deltas_by_name(delta_names=[sdc.delta_name for sdc in sdcl])

        responses = []

        for sdc in sdcl:
            table_names = []
            schemas = []
            table_ids = []
            source_schema: str
            target_schema: str
            source_tbl: str = ""
            source_table = Table()
            comparisons = []
            warehouses = []

            if sdc.fq_source_table_name:
                swh, source_schema, source_tbl = fully_qualified_table_to_elements(sdc.fq_source_table_name)
                schemas.append(source_schema)
                warehouses.append(swh)
                table_names.append(source_tbl)

            if sdc.source_table_id:
                table_ids.append(sdc.source_table_id)

            targets = sdc.target_table_comparisons

            target_comparisons = {}
            target_ids = []
            target_names = []
            fq_target_names = []

            for t in targets:

                if t.fq_target_table_name:
                    twh, target_schema, target_tbl = fully_qualified_table_to_elements(t.fq_target_table_name)
                    schemas.append(target_schema)
                    target_names.append(target_tbl)
                    warehouses.append(twh)
                    fq_target_names.append(t.fq_target_table_name.lower())

                if t.target_table_id:
                    target_ids.append(t.target_table_id)

            source_ids = [s.id for s in self.get_sources_by_name(source_names=warehouses).values()]

            tables_ix = {t.id: t for t in self.get_tables(ids=table_ids + target_ids,
                                                          schema=schemas,
                                                          table_name=table_names + target_names,
                                                          warehouse_id=source_ids).tables}

            tables = list(tables_ix.values())

            if len(tables) == 1 and len(targets) == 1:
                t = tables[0]
                source_table = t
                targets[0].target_table_id = t.id
                target_comparisons[t.id] = targets[0]
            elif len(tables) == 1 and len(targets) == 2:
                t = tables[0]
                source_table = t
                for i, target in enumerate(targets):
                    target.target_table_id = t.id
                    target_comparisons[f"{i}.{t.id}"] = target
            elif len(tables) != 1:
                for t in tables:
                    fq_table_name = f"{t.warehouse_name}.{t.schema.name}.{t.name}".lower()
                    if t.id in target_ids or fq_table_name in fq_target_names:
                        for i, target in enumerate(targets):
                            if t.id == target.target_table_id:
                                target_comparisons[f"{i}.{t.id}"] = target
                            elif (f"{t.warehouse_name}.{t.schema.name}.{t.name}".lower()
                                  == target.fq_target_table_name.lower()):
                                target.target_table_id = t.id
                                target_comparisons[f"{i}.{t.id}"] = target
                    elif t.id == sdc.source_table_id or t.name == source_tbl or fq_table_name not in fq_target_names:
                        source_table = t
                    else:
                        raise TableNotFoundException(f"Erroneous table id returned: {t.id}")
            else:

                raise TableNotFoundException(f"Cannot find table ids.")

            for target_compare in target_comparisons.values():
                target_table = tables_ix[target_compare.target_table_id]
                response_as_ctc = ComparisonTableConfiguration(name=sdc.delta_name, source_table_id=source_table.id,
                                                               target_table_id=target_compare.target_table_id)

                if target_compare.delta_column_mapping:
                    """
                    If mappings are declared then metrics will be taken from those mappings and no defaults will be applied.
                    """
                    response_as_ctc.column_mappings = [
                        build_ccm(scm=cm, source_table=source_table, target_table=target_table)
                        for cm in target_compare.delta_column_mapping]
                else:
                    """
                    If no mappings are declared then column mappings will be inferred and metrics will be defaulted.
                    """
                    source_metric_types = self.get_delta_applicable_metric_types(table_id=source_table.id).metric_types
                    target_metric_types = self.get_delta_applicable_metric_types(table_id=target_table.id).metric_types
                    response_as_ctc.column_mappings = infer_column_mappings(source_metric_types=source_metric_types,
                                                                            target_metric_types=target_metric_types)

                if target_compare.all_column_metrics:
                    all_column_metrics = [m.to_datawatch_object() for m in target_compare.all_column_metrics]
                    """If SDC has defined all_column_metrics then the each columns metrics wil lbe extended with the metrics
                    defined in all_column_metrics."""
                    for m in response_as_ctc.column_mappings:
                        m.metrics.extend(all_column_metrics)

                response_as_ctc.group_bys = [gb.to_datawatch_object() for gb in target_compare.group_bys]
                response_as_ctc.source_filters = target_compare.source_filters
                response_as_ctc.target_filters = target_compare.target_filters
                response_as_ctc.tolerance = target_compare.tolerance

                comparisons.append(response_as_ctc)

            named_schedule = IdAndDisplayName()
            if sdc.cron_schedule:
                schedules = self.get_named_schedule(search=sdc.cron_schedule.name).named_schedules
                for s in schedules:
                    """Matches on cron value."""
                    if s.cron == sdc.cron_schedule.cron or s.name == sdc.cron_schedule.name:
                        named_schedule = IdAndDisplayName(id=s.id, display_name=s.name)
                        break
                    else:
                        try:
                            schedule = self.create_named_schedule(name=sdc.cron_schedule.name,
                                                                  cron=sdc.cron_schedule.cron)
                            named_schedule = IdAndDisplayName(id=schedule.id, display_name=schedule.name)
                            break
                        except:
                            log.warning("Failed to create cron schedule. Verify you have access.")
                            log.info("The delta will be created without a schedule.")
                            break

            delta = Delta(
                name=sdc.delta_name,
                source_table=IdAndDisplayName(id=source_table.id, display_name=source_table.name),
                named_schedule=named_schedule,
                comparison_table_configurations=comparisons,
                notification_channels=[
                    nc.to_datawatch_object() for nc in sdc.notification_channels
                ]

            )

            response = self.upsert_delta(delta=delta)

            responses.append(response.delta)

        return responses

    def create_delta(
            self,
            name: str = None,
            source_table_id: int = None,
            target_table_id: int = None,
            metrics_to_enable: List[MetricType] = [],
            column_mappings: List[ComparisonColumnMapping] = [],
            named_schedule: IdAndDisplayName = None,
            group_bys: List[ColumnNamePair] = [],
            source_filters: List[str] = [],
            target_filters: List[str] = [],
            comparison_table_configuration: Optional["ComparisonTableConfiguration"] = None,
    ) -> CreateComparisonTableResponse:
        """

        Args:
            name: Required.  Name of delta
            source_table_id:  Required.  table id for source table
            target_table_id: Required. Table id for target table
            metrics_to_enable: Optional.
            column_mappings: Optional. If not exists then will infer from applicable table mappings based on column name.
            named_schedule: Optional.  No schedule if not exists
            group_bys: Optional.  No group bys if not exists
            source_filters: Optional.  No filters if not exists
            target_filters: Optional.  No filters if not exists
            comparison_table_configuration: Optional.

        Returns:  CreateComparisonTableResponse

        """

        if metrics_to_enable and column_mappings:
            raise Exception('Column mappings defines the enabled metrics by column map.  Either define column mappings '
                            'OR metrics to enable -- not both.')

        url = '/api/v1/metrics/comparisons/tables'

        request = CreateComparisonTableRequest()
        if comparison_table_configuration:
            request.comparison_table_configuration = comparison_table_configuration
        elif name and source_table_id and target_table_id:
            request.comparison_table_configuration.name = name
            request.comparison_table_configuration.source_table_id = source_table_id
            request.comparison_table_configuration.target_table_id = target_table_id
            request.comparison_table_configuration.column_mappings = column_mappings
            if named_schedule:
                request.comparison_table_configuration.named_schedule = named_schedule
            request.comparison_table_configuration.group_bys = group_bys
            request.comparison_table_configuration.source_filters = source_filters
            request.comparison_table_configuration.target_filters = target_filters
            request.comparison_table_configuration.target_table_id = target_table_id
        else:
            raise Exception('Must supply either a ComparisonMetricConfiguration OR a name, '
                            'source table id, and target table id.')

        if not request.comparison_table_configuration.column_mappings:
            source_metric_types = self.get_delta_applicable_metric_types(
                table_id=request.comparison_table_configuration.source_table_id
            ).metric_types
            target_metric_types = self.get_delta_applicable_metric_types(
                table_id=request.comparison_table_configuration.target_table_id
            ).metric_types
            request.comparison_table_configuration.column_mappings = infer_column_mappings(
                source_metric_types=source_metric_types,
                target_metric_types=target_metric_types
            )
            if metrics_to_enable:
                for m in request.comparison_table_configuration.column_mappings:
                    m.metrics = metrics_to_enable

        response = self._call_datawatch(Method.POST, url, request.to_json())

        return CreateComparisonTableResponse().from_dict(response)

    def upsert_delta(self, delta: Delta):

        url = "/api/v1/deltas"
        request = UpsertDeltaRequest(delta=delta)
        response = self._call_datawatch(Method.POST, url, request.to_json())
        return UpsertDeltaResponse().from_dict(response)

    def purge_metric_suites(self,
                            source_names: List[str],
                            purge_all_sources: bool = False,
                            apply: bool = False,
                            namespace: Optional[str] = None
                            ) -> List[MetricSuiteReport]:
        """
        Purges metric suites for all warehouse_ids.
        Args:
            source_names: one or more source names
            purge_all_sources: If true will purge all sources in workspace.
            apply: whether to apply the change
            namespace: the namespace to purge

        return: list of metric suite responses.

        Raises:
            NoSourcesFoundException: If no sources are identified based on parameters.
        """

        sources_by_name_ix: Dict[str, Source] = self.get_sources_by_name(source_names)
        source_name_id_tuples: List[Tuple[int, str]] = []
        if purge_all_sources:
            source_name_id_tuples.extend([(s.id, s.name) for s in sources_by_name_ix.values()])
        elif source_names:
            for source_name in source_names:
                source = sources_by_name_ix.get(source_name)
                if source:
                    source_name_id_tuples.append((source.id, source_name))

        reports: List[MetricSuiteReport] = []

        if source_name_id_tuples:
            process_stage = ProcessStage.APPLY if apply else ProcessStage.PLAN
            for source_id, source_name in source_name_id_tuples:
                metric_suite = MetricSuite(source_id=source_id, namespace=namespace)
                response = self.post_bigconfig(metric_suite=metric_suite, apply=apply)
                reports.append(MetricSuiteReport.from_datawatch_object(obj=response,
                                                                       source_name=source_name,
                                                                       process_stage=process_stage))

            return reports

        else:
            raise NoSourcesFoundException('No sources identified for purge.')

    @deprecated("Use post_bigconfig with an empty MetricSuite for the source")
    def purge_warehouse(self, source_id: int) -> BulkResponse:
        url = f"/api/v1/metric-suites/purge/warehouse/{source_id}"
        return BulkResponse().from_dict(self._call_datawatch(Method.GET, url=url))

    @deprecated("Use post_bigconfig")
    def post_metric_suite(self, metric_suite: MetricSuite, apply: bool = False) -> MetricSuiteResponse:
        mc_url = "/api/v1/metric-suites"
        if apply:
            url = mc_url
        else:
            url = f"{mc_url}/dry-run"

        return MetricSuiteResponse().from_dict(
            self._call_datawatch(Method.POST, url=url, body=metric_suite.to_json())
        )

    @deprecated("Use post_bigconfig")
    def post_metric_suite_queue(self, metric_suite: MetricSuite, apply: bool = False) -> MetricSuiteResponse:
        if apply:
            url = "/api/v1/metric-suites/queue"
        else:
            url = f"/api/v1/metric-suites/dry-run/queue"

        response: WorkflowStatusResponse = WorkflowStatusResponse().from_dict(
            self._call_datawatch(Method.POST, url=url, body=metric_suite.to_json())
        )

        status_url = f"/api/v1/metric-suites/status/{response.workflow_id}"
        while response.status == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_QUEUED or \
                response.status == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_IN_PROGRESS:
            log.info(f"Bigconfig in queue...")
            time.sleep(10)
            bwsr: BigconfigWorkflowStatusResponse = BigconfigWorkflowStatusResponse().from_dict(
                self._call_datawatch(Method.GET, url=status_url))
            response.status = bwsr.workflow_status_response.status

        log.info(f"Queuing complete. Workflow finished with status {response.status.name}")

        if response.status != WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_COMPLETED:
            err = f"Bigconfig workflow was not completed. Final status: {response.status.name}"
            raise BigconfigIncompleteException(err)

        return bwsr.metric_suite_response

    def post_bigconfig(self, metric_suite: MetricSuite, apply: bool = False) -> MetricSuiteResponse:
        bc_url = "/api/v1/bigconfig"
        if apply:
            url = f"{bc_url}/apply"
        else:
            url = f"{bc_url}/plan"

        response: BigconfigWorkflowV2StatusResponse = BigconfigWorkflowV2StatusResponse().from_dict(
            self._call_datawatch(Method.POST, url=url, body=metric_suite.to_json())
        )

        status_url = f"{bc_url}/status/{response.status_response.workflow_v2_id.workflow_id}"
        while response.status_response.status == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_QUEUED or \
                response.status_response.status == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_IN_PROGRESS:
            log.info(f"Bigconfig in queue...")
            time.sleep(10)
            response: BigconfigWorkflowV2StatusResponse = BigconfigWorkflowV2StatusResponse().from_dict(
                self._call_datawatch(Method.GET, url=status_url)
            )

        log.info(f"Queuing complete. Workflow finished with status {response.status_response.status.name}")

        if response.status_response.status != WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_COMPLETED:
            err = f"Bigconfig workflow was not completed. Final status: {response.status_response.status.name}"
            raise BigconfigIncompleteException(err)

        return response.bigconfig_response

    def upsert_metric(
            self,
            *,
            id: int = 0,
            schedule_frequency: Optional[TimeInterval] = None,
            filters: List[str] = [],
            group_bys: List[str] = [],
            thresholds: List[Threshold] = [],
            notification_channels: List[NotificationChannel] = [],
            warehouse_id: int = 0,
            dataset_id: int = 0,
            metric_type: Optional[MetricType] = None,
            parameters: List[MetricParameter] = [],
            lookback: Optional[TimeInterval] = None,
            lookback_type: LookbackType = 0,
            metric_creation_state: MetricCreationState = 0,
            grain_seconds: int = 0,
            muted_until_epoch_seconds: int = 0,
            name: str = "",
            description: str = "",
            rct_override: Optional[str] = None,
            metric_configuration: MetricConfiguration = None
    ) -> MetricConfiguration:
        """Create or update metric"""

        if metric_configuration:
            request = metric_configuration
        else:
            request = MetricConfiguration()
            request.id = id
            if schedule_frequency is not None:
                request.schedule_frequency = schedule_frequency
            request.filters = filters
            request.group_bys = group_bys
            if thresholds is not None:
                request.thresholds = set_default_model_type_for_threshold(thresholds)
            if notification_channels is not None:
                request.notification_channels = notification_channels
            request.warehouse_id = warehouse_id
            request.dataset_id = dataset_id
            if metric_type is not None:
                request.metric_type = metric_type
            if parameters is not None:
                request.parameters = parameters
            if lookback is not None:
                request.lookback = lookback
            if rct_override:
                request.rct_override = rct_override
            request.lookback_type = lookback_type
            request.metric_creation_state = metric_creation_state
            request.grain_seconds = grain_seconds
            request.muted_until_epoch_seconds = muted_until_epoch_seconds
            request.name = name
            request.description = description

        set_default_model_type_for_threshold(request.thresholds)

        url = "/api/v1/metrics"

        # this is done so that default 0 values are not removed when converting to json
        request_dict = request.to_dict()
        if request_dict["thresholds"][0] == {}:
            request_dict["thresholds"] = [{"noneThreshold": {}}]

        # if both schedule and name schedule are provided the named schedule should be used.
        if request_dict.get("scheduleFrequency", None) and request_dict.get("metricSchedule", None):
            request_dict.pop('scheduleFrequency', None)

        request_json = json.dumps(request_dict)

        response = self._call_datawatch(Method.POST, url=url, body=request_json)

        return MetricConfiguration().from_dict(response)

    def upsert_metric_from_simple_template(
            self,
            sumr: SimpleUpsertMetricRequest,
            existing_metric_id: int = None
    ) -> int:
        """
        Takes a warehouse id and a SimpleUpsertMetricRequest, fills in reasonable defaults, and upserts a metric.

        :param sumr: SimpleUpsertMetricRequest object
        :param existing_metric_id: An existing metric ID on which to base the upsert

        :return: Id of the resulting metric.
        """
        # TODO Consider moving warehouse_id into sumr
        if sumr.metric_name is None:
            raise Exception("Metric name must be present in configuration", sumr)

        tables = self.get_tables(warehouse_id=[sumr.warehouse_id], schema=[sumr.schema_name],
                                 table_name=[sumr.table_name]).tables

        if not tables:
            raise Exception(f"Could not find table: {sumr.schema_name}.{sumr.table_name}")
        elif len(tables) > 1:
            p = [f"Warehouse ID: {t.warehouse_id}.  FQ Table Name: " \
                 f"{t.database_name}.{t.schema_name}.{t.name}" for t in tables]
            raise Exception(f"Found multiple tables. {p}")
        else:
            table = tables[0]

        if existing_metric_id:
            existing_metric = self.get_metric_configuration(metric_id=existing_metric_id)
        else:
            existing_metric = self.get_existing_metric(
                warehouse_id=sumr.warehouse_id,
                table=table,
                column_name=sumr.column_name,
                user_defined_name=sumr.user_defined_metric_name,
                metric_name=sumr.metric_name,
                group_by=sumr.group_by,
                filters=sumr.filters)

        metric = sumr.to_datawatch_object(target_table=table, existing_metric=existing_metric)

        should_backfill = False
        if metric.id is None and not is_freshness_metric(sumr.metric_name):
            should_backfill = True

        result = self.upsert_metric(metric_configuration=metric)

        log.info("Create result: %s", result.to_json())
        if should_backfill and result.id is not None and table_has_metric_time(table):
            self.backfill_metric(metric_ids=[result.id])

        return result.id

    def create_external_monitor(self, metric: MetricConfiguration) -> MetricConfiguration:
        """
        Create an external monitor.
        External monitors allow submitting metric results from external systems.

        Args:
            metric: MetricConfiguration object defining the external monitor

        Returns:
            MetricConfiguration object for the created external monitor
        """
        url = "/api/v1/monitors/external"
        response = self._call_datawatch(Method.POST, url=url, body=metric.to_json())
        return MetricConfiguration().from_dict(response)

    def submit_external_monitor_run(
        self,
        monitor_id: int,
        run_request: ExternalMonitorRunRequest
    ) -> MetricInfo:
        """
        Submit a run result for an external monitor.
        Args:
            monitor_id: ID of the external monitor
            run_request: ExternalMonitorRunRequest containing the run data

        Returns:
            MetricInfo object containing the result of the monitor run
        """
        url = f"/api/v1/monitors/external/{monitor_id}/runs"

        # Manually construct JSON body to ensure observed_value is always included
        # (betterproto omits fields with default values, and 0.0 is the default for doubles)
        body_dict = {
            "observedValue": run_request.observed_value,
            "runAtEpochSeconds": str(run_request.run_at_epoch_seconds)
        }
        body_json = json.dumps(body_dict)

        response = self._call_datawatch(Method.POST, url=url, body=body_json)
        return MetricInfo().from_dict(response)

    def get_metric_runs(
        self,
        metric_id: int,
        days_of_history: Optional[int] = None,
        start_epoch_seconds: Optional[int] = None,
        end_epoch_seconds: Optional[int] = None
    ) -> GetMetricRunsResponse:
        """
        Get metric runs for a single metric.

        Args:
            metric_id: ID of the metric
            days_of_history: Optional number of days of history to fetch
            start_epoch_seconds: Optional start time filter (epoch seconds)
            end_epoch_seconds: Optional end time filter (epoch seconds)

        Returns:
            GetMetricRunsResponse containing the metric runs
        """
        url = "/api/v1/metrics/runs"
        request = GetMetricRunsRequest()
        request.metric_identifier = MetricIdentifier(metric_id=metric_id)

        if days_of_history is not None:
            request.days_of_history = days_of_history
        if start_epoch_seconds is not None:
            request.start_epoch_seconds = start_epoch_seconds
        if end_epoch_seconds is not None:
            request.end_epoch_seconds = end_epoch_seconds

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return GetMetricRunsResponse().from_dict(response)

    def get_metric_runs_bulk(
        self,
        metric_ids: List[int],
        days_of_history: Optional[int] = None,
        start_epoch_seconds: Optional[int] = None,
        end_epoch_seconds: Optional[int] = None
    ) -> GetMetricRunsBulkResponse:
        """
        Get metric runs for multiple metrics in a single request.

        Args:
            metric_ids: List of metric IDs
            days_of_history: Optional number of days of history to fetch
            start_epoch_seconds: Optional start time filter (epoch seconds)
            end_epoch_seconds: Optional end time filter (epoch seconds)

        Returns:
            GetMetricRunsBulkResponse containing metric runs for all requested metrics
        """
        url = "/api/v1/metrics/runs/bulk"
        request = GetMetricRunsBulkRequest()
        request.metric_identifier = [MetricIdentifier(metric_id=mid) for mid in metric_ids]

        if days_of_history is not None:
            request.days_of_history = days_of_history
        if start_epoch_seconds is not None:
            request.start_epoch_seconds = start_epoch_seconds
        if end_epoch_seconds is not None:
            request.end_epoch_seconds = end_epoch_seconds

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return GetMetricRunsBulkResponse().from_dict(response)

    def regen_autometrics(self, table_id: int):
        url = f'/statistics/suggestions/{table_id}/queue'
        log.info(url)
        response = self._call_datawatch(Method.GET, url=url)

    def backfill_autothresholds(self,
                                metric_ids: List[int] = []):
        """
        Runs posthoc autothresholds for existing metric runs.  Does not run metrics for past data.  Not destructive.
        Will run sync.
        :param metric_ids: list of metric ids
        :return: none.
        """
        for metric_id in metric_ids:
            log.info(f"Backfilling autothreshold: {metric_id}")
            url = f"/statistics/backfillAutoThresholds/{metric_id}"
            response = self._call_datawatch(Method.GET, url=url)

    def get_debug_queries(self, *, metric_ids: List[int], timeout: int = None) -> List[MetricDebugQueries]:
        """
        Get queries for debug page
        :param metric_ids: List of metric ids for which to retrieve debug queries.
        :param timeout: The time in seconds to wait for a response from Bigeye.
        :return: a dictionary of
        """
        r: List[MetricDebugQueries] = []

        for metric_id in metric_ids:
            url = f'/api/v1/metrics/{metric_id}/debug/queries'
            response = self._call_datawatch(Method.GET, url, timeout=timeout)
            i = MetricDebugQueries(
                metric_id=metric_id,
                debug_queries=GetDebugQueriesResponse().from_dict(response)
            )
            r.append(i)

        return r

    def get_attributes(
            self, entity_type: SimpleCatalogEntityType, entity_id: int
    ) -> CatalogAttributeResponse:
        url = "/api/v1/catalog-attributes/get"
        request = GetCatalogAttributeRequest(
            entity_type=entity_type.to_datawatch_object(), entity_id=entity_id
        )
        return CatalogAttributeResponse().from_dict(
            self._call_datawatch_impl(method=Method.POST, url=url, body=request.to_json())
        )

    def set_attributes(
            self, entity_type: SimpleCatalogEntityType, entity_id: int, attributes: dict
    ):
        url = "/api/v1/catalog-attributes/set"
        attrs = [CatalogAttribute(key=k, value=v) for k, v in attributes.items()]
        request = SetCatalogAttributeRequest(
            entity_type=entity_type.to_datawatch_object(),
            entity_id=entity_id,
            attributes=attrs,
        )

        return CatalogAttributeResponse().from_dict(
            self._call_datawatch_impl(method=Method.POST, url=url, body=request.to_json())
        )

    def set_object_owner(self, object_type: OwnableType, object_id: int, owner: int):
        url = "/api/v1/object-owners"
        request = SetObjectOwnerRequest(
            ownable_type=object_type,
            ownable_id=object_id,
            owner=owner
        )

        return ObjectOwnerResponse().from_dict(
            self._call_datawatch_impl(method=Method.POST, url=url, body=request.to_json())
        )

    def batch_run_metrics(self, *, metric_ids: List[int], queue: bool):
        """Use to run a batch of metrics and submit it to the queue or not"""
        if queue:
            self.run_metric_batch_async(metric_ids=metric_ids)
        else:
            r = self.run_metric_batch(metric_ids=metric_ids)
            log.info(r.to_json())

    def send_dbt_core_job_info(self,
                               *,
                               project_name: Optional[str] = None,
                               job_name: Optional[str] = None,
                               job_run_id: Optional[str] = None,
                               manifest_json: str = None,
                               run_results_json: str = None,
                               project_url: Optional[str] = None,
                               job_url: Optional[str] = None,
                               job_run_url: Optional[str] = None) -> SendDbtCoreRunInfoResponse:

        url = "/api/v1/integrations/dbt/job-run"
        request = SendDbtCoreRunInfoRequest()
        request.project_name = project_name
        request.job_name = job_name
        request.job_run_id = job_run_id
        request.manifest_json = manifest_json
        request.run_results_json = run_results_json
        request.project_url = project_url
        request.job_url = job_url
        request.job_run_url = job_run_url

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return SendDbtCoreRunInfoResponse().from_dict(response)

    def bulk_run_rules(self, rule_ids: List[int]) -> BulkResponse:
        """Run a list of rules"""
        url = '/api/v1/custom-rules/bulk'
        request = CustomRuleBulkRequest()
        request.is_run = True
        request.where.ids = rule_ids

        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return BulkResponse().from_dict(response)

    def upsert_custom_rule(self,
                           rule_id: Optional[int] = None,
                           warehouse_id: Optional[int] = None,
                           name: Optional[str] = None,
                           sql: Optional[str] = None,
                           threshold_type: Optional[CustomRulesThresholdType] = None,
                           upper_threshold: Optional[float] = None,
                           lower_threshold: Optional[float] = None,
                           collection_ids: Optional[List[int]] = None,
                           schedule: Optional[MetricSchedule] = None,
                           owner_id: Optional[int] = None) -> CustomRuleInfo:
        """Upsert a custom rule."""
        if not rule_id or rule_id == 0:
            if not warehouse_id or not name or not sql or not threshold_type:
                raise Exception("For new rules, the warehouse_id, name, sql, and threshold_type fields are required.")

            return self.create_custom_rule(
                warehouse_id=warehouse_id,
                name=name,
                sql=sql,
                threshold_type=threshold_type,
                upper_threshold=upper_threshold,
                lower_threshold=lower_threshold,
                collection_ids=collection_ids,
                schedule=schedule,
                owner_id=owner_id
            )

        else:
            custom_rule = self.get_rule_by_id(rule_id=rule_id).custom_rule

            if name is not None:
                custom_rule.name = name
            if sql is not None:
                custom_rule.sql = sql
            if threshold_type is not None:
                custom_rule.threshold_type = threshold_type
            if upper_threshold is not None:
                custom_rule.upper_threshold = upper_threshold
            if lower_threshold is not None:
                custom_rule.lower_threshold = lower_threshold
            if collection_ids is not None:
                custom_rule.collection_ids = collection_ids
            if schedule is not None:
                custom_rule.metric_schedule = schedule
            if owner_id is not None:
                owner = [u for u in self.get_users().users if u.id == owner_id][0]
                custom_rule.owner = owner

            return self.edit_custom_rule(
                custom_rule=custom_rule,
                rule_id=rule_id
            )

    def get_rules(self, warehouse_id: int = None, collection_id: int = None) -> GetCustomRuleListResponse:
        """Get all rules for a given warehouse or collection. Either the warehouse ID or collection ID is required."""
        if not warehouse_id and not collection_id:
            raise Exception(f"Either the warehouse ID or collection ID are required.")
        elif warehouse_id and not collection_id:
            return self.get_rules_for_source(warehouse_id=warehouse_id)
        elif collection_id and not warehouse_id:
            return self.get_rules_for_collection(collection_id=collection_id)
        elif warehouse_id and collection_id:
            rules = self.get_rules_for_source(warehouse_id=warehouse_id)
            rules_filtered = []
            for r in rules.custom_rules:
                for c in r.collections:
                    if c.id == collection_id:
                        rules_filtered.append(r)
            rules.custom_rules = rules_filtered
            return rules

    def get_upstream_nodes(self, node_id: int, depth: Optional[int] = None) -> TableLineageV2Response:
        url = f"/api/v2/lineage/nodes/{node_id}/graph?direction=upstream"
        if depth:
            url += f"&depth={depth}"
        return TableLineageV2Response().from_dict(
            self._call_datawatch_impl(method=Method.GET, url=url)
        )

    def get_downstream_nodes(self, node_id: int, depth: Optional[int] = None) -> TableLineageV2Response:
        url = f"/api/v2/lineage/nodes/{node_id}/graph?direction=downstream"
        if depth:
            url += f"&depth={depth}"
        response = self._call_datawatch_impl(method=Method.GET, url=url)
        return TableLineageV2Response(**response)

    def search_lineage(self, search: str, search_type: Optional[DataNodeType] = None,
                       limit: Optional[int] = 100) -> SearchResponse:
        url = f"/api/v1/search"
        request = SearchRequest()
        request.search = search
        request.limit = limit

        # properly set the search types
        request_dict = request.to_dict()
        if search_type is not None:
            search_types_dict = {"dataNodeType": search_type.name}
            request_dict["types"] = [search_types_dict]

        response = self._call_datawatch(Method.POST, url=url, body=json.dumps(request_dict))
        return SearchResponse().from_dict(response)

    def unassign_issue(self, issue_id: int) -> Issue:
        url = f"/api/v1/issues/{issue_id}"
        unassigned = User(id=0, name="", email="", groups=[], idp_groups=[], last_login_at=0, picture_url="")
        assignment_update = IssueAssignmentUpdate(id=0, assignee=unassigned)
        request = UpdateIssueRequest(assignment_update=assignment_update)
        response = self._call_datawatch(Method.PUT, url, request.to_json())
        return UpdateIssueResponse().from_dict(response).issue

    def get_current_workspace(self) -> Workspace:
        return Workspace().from_dict(
            self._call_datawatch(Method.GET, url=f"/api/v1/workspaces/{self.config.workspace_id}")
        )

    # Custom Integration Types
    def create_custom_integration_type(self, name: str, type: IntegrationType,
                                       description: Optional[str] = None,
                                       icon_url: Optional[str] = None) -> CustomIntegrationType:
        """
        Create a custom integration type.

        Args:
            name: Display name for the integration type
            type: Category of integration (IntegrationType enum - e.g., INTEGRATION_TYPE_DATABASE, INTEGRATION_TYPE_BI_TOOL)
            description: Optional description of the integration type
            icon_url: Optional URL to an icon image (.png, .svg, .jpg, .jpeg, .gif, .webp)

        Returns:
            CustomIntegrationType object containing id, name, description, type, and icon_url
        """
        url = "/api/v2/lineage/custom-integration-types"
        integration_type = CustomIntegrationType(
            name=name,
            type=type,
            description=description or "",
            icon_url=icon_url or ""
        )
        response = self._call_datawatch(Method.POST, url=url, body=integration_type.to_json())
        return CustomIntegrationType().from_dict(response)

    def get_custom_integration_types(self) -> GetCustomIntegrationTypesResponse:
        """
        Get all custom integration types.

        Returns:
            GetCustomIntegrationTypesResponse containing list of CustomIntegrationType objects
        """
        url = "/api/v2/lineage/custom-integration-types"
        response = self._call_datawatch(Method.GET, url=url)
        return GetCustomIntegrationTypesResponse().from_dict(response)

    def update_custom_integration_type(self, integration_type_id: int, name: Optional[str] = None,
                                       type: Optional[IntegrationType] = None,
                                       description: Optional[str] = None,
                                       icon_url: Optional[str] = None) -> CustomIntegrationType:
        """
        Update a custom integration type.

        Args:
            integration_type_id: ID of the integration type to update
            name: Display name for the integration type
            type: Category of integration (IntegrationType enum)
            description: Optional description of the integration type
            icon_url: Optional URL to an icon image

        Returns:
            CustomIntegrationType object with updated values
        """
        url = f"/api/v2/lineage/custom-integration-types/{integration_type_id}"
        # First get the existing integration type
        existing = self.get_custom_integration_types()
        current = next((t for t in existing.types if t.id == integration_type_id), None)
        if not current:
            raise Exception(f"Integration type with id {integration_type_id} not found")

        # Update only provided fields
        updated = CustomIntegrationType(
            id=integration_type_id,
            name=name if name is not None else current.name,
            type=type if type is not None else current.type,
            description=description if description is not None else current.description,
            icon_url=icon_url if icon_url is not None else current.icon_url
        )
        response = self._call_datawatch(Method.PUT, url=url, body=updated.to_json())
        return CustomIntegrationType().from_dict(response)

    def delete_custom_integration_type(self, integration_type_id: int) -> None:
        """
        Delete a custom integration type.

        Args:
            integration_type_id: ID of the integration type to delete
        """
        url = f"/api/v2/lineage/custom-integration-types/{integration_type_id}"
        self._call_datawatch(Method.DELETE, url=url)

    # Custom Repositories
    def create_custom_repository(self, name: str, integration_type_id: int) -> CustomRepository:
        """
        Create a custom repository.

        Args:
            name: Display name for the repository
            integration_type_id: The ID of the custom integration type

        Returns:
            CustomRepository object containing id, name, workspace_id and integration_type
        """
        url = "/api/v2/lineage/custom-repositories"
        repository = CustomRepository(
            name=name,
            integration_type=CustomIntegrationType(id=integration_type_id),
            workspace_id=self.config.workspace_id
        )
        response = self._call_datawatch(Method.POST, url=url, body=repository.to_json())
        return CustomRepository().from_dict(response)

    def get_custom_repositories(self) -> GetCustomRepositoriesResponse:
        """
        Get all custom repositories.

        Returns:
            GetCustomRepositoriesResponse containing list of CustomRepository objects
        """
        url = "/api/v2/lineage/custom-repositories"
        response = self._call_datawatch(Method.GET, url=url)
        return GetCustomRepositoriesResponse().from_dict(response)

    def update_custom_repository(self, repository_id: int, name: Optional[str] = None,
                                 integration_type_id: Optional[int] = None) -> CustomRepository:
        """
        Update a custom repository.

        Args:
            repository_id: ID of the repository to update
            name: Display name for the repository
            integration_type_id: The ID of the custom integration type

        Returns:
            CustomRepository object with updated values
        """
        url = f"/api/v2/lineage/custom-repositories/{repository_id}"
        # Get existing repository
        existing = self.get_custom_repositories()
        current = next((r for r in existing.repositories if r.id == repository_id), None)
        if not current:
            raise Exception(f"Repository with id {repository_id} not found")

        # Update only provided fields
        updated = CustomRepository(
            id=repository_id,
            name=name if name is not None else current.name,
            integration_type=CustomIntegrationType(id=integration_type_id) if integration_type_id is not None else current.integration_type,
            workspace_id=current.workspace_id
        )
        response = self._call_datawatch(Method.PUT, url=url, body=updated.to_json())
        return CustomRepository().from_dict(response)

    def delete_custom_repository(self, repository_id: int) -> None:
        """
        Delete a custom repository.

        Args:
            repository_id: ID of the repository to delete
        """
        url = f"/api/v2/lineage/custom-repositories/{repository_id}"
        self._call_datawatch(Method.DELETE, url=url)

    def sync_custom_repository(self, request: CustomRepositorySyncRequest) -> CustomRepositorySyncResponse:
        """
        Sync a custom repository (declarative sync).

        This endpoint allows you to declaratively define the desired state of a
        custom repository including all its nodes and edges. The API will compute
        the differences and perform create/update/delete operations automatically.

        Returns:
            CustomRepositorySyncResponse with workflow_v2_id for tracking the sync
        """
        url = "/api/v2/lineage/custom-repositories/sync"
        response_dict = self._call_datawatch(
            method=Method.POST,
            url=url,
            body=request.to_json()
        )
        return CustomRepositorySyncResponse().from_dict(response_dict)

    # Custom Node Types
    def create_custom_node_types_bulk(self, types: List[CustomNodeType]) -> BulkResponse:
        """
        Create custom node types in bulk.

        Args:
            types: List of CustomNodeType objects. Each should contain:
                - name: Singular display name for the node type
                - name_plural: Plural display name for the node type
                - integration_type: CustomIntegrationType with id
                - allowed_parent_types: Optional list of CustomNodeType objects with id or name

        Returns:
            BulkResponse with successful_ids and failed_updates

        Example:
            types = [
                CustomNodeType(
                    name="Schema",
                    name_plural="Schemas",
                    integration_type=CustomIntegrationType(id=1)
                ),
                CustomNodeType(
                    name="Table",
                    name_plural="Tables",
                    integration_type=CustomIntegrationType(id=1),
                    allowed_parent_types=[CustomNodeType(name="Schema")]
                )
            ]
        """
        url = "/api/v2/lineage/custom-node-types/bulk"
        request = BulkCreateCustomNodeTypesRequest(types=types)
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return BulkResponse().from_dict(response)

    def get_custom_node_types(self) -> GetCustomNodeTypesResponse:
        """
        Get all custom node types.

        Returns:
            GetCustomNodeTypesResponse containing list of CustomNodeType objects
        """
        url = "/api/v2/lineage/custom-node-types"
        response = self._call_datawatch(Method.GET, url=url)
        return GetCustomNodeTypesResponse().from_dict(response)

    def update_custom_node_type(self, node_type_id: int, name: Optional[str] = None,
                                name_plural: Optional[str] = None,
                                allowed_parent_types: Optional[List[CustomNodeType]] = None) -> CustomNodeType:
        """
        Update a custom node type.

        Args:
            node_type_id: ID of the node type to update
            name: Singular display name for the node type
            name_plural: Plural display name for the node type
            allowed_parent_types: Optional list of CustomNodeType objects with id or name

        Returns:
            CustomNodeType object with updated values
        """
        url = f"/api/v2/lineage/custom-node-types/{node_type_id}"
        # Get existing node type
        existing = self.get_custom_node_types()
        current = next((t for t in existing.types if t.id == node_type_id), None)
        if not current:
            raise Exception(f"Node type with id {node_type_id} not found")

        # Update only provided fields
        updated = CustomNodeType(
            id=node_type_id,
            name=name if name is not None else current.name,
            name_plural=name_plural if name_plural is not None else current.name_plural,
            integration_type=current.integration_type,
            allowed_parent_types=allowed_parent_types if allowed_parent_types is not None else current.allowed_parent_types
        )
        response = self._call_datawatch(Method.PUT, url=url, body=updated.to_json())
        return CustomNodeType().from_dict(response)

    def delete_custom_node_type(self, node_type_id: int) -> None:
        """
        Delete a custom node type.

        Args:
            node_type_id: ID of the node type to delete
        """
        url = f"/api/v2/lineage/custom-node-types/{node_type_id}"
        self._call_datawatch(Method.DELETE, url=url)

    # Nodes
    def create_custom_lineage_node(self, node_name: str, node_type: DataNodeType, node_container_name: str,
                                   custom_repository_id: int, custom_node_type_id: int,
                                   node_container_entity_id: Optional[int] = None,
                                   icon_url: Optional[str] = None) -> LineageNodeV2:
        """
        Create a custom lineage node.

        Args:
            node_name: Name of the node (e.g., "users", "public")
            node_type: DataNodeType enum - use DATA_NODE_TYPE_CUSTOM for custom nodes or DATA_NODE_TYPE_CUSTOM_ENTRY for leaf nodes
            node_container_name: Name of the parent container. For root nodes, use the repository name
            custom_repository_id: The ID of the custom repository
            custom_node_type_id: The ID of the custom node type
            node_container_entity_id: Entity ID of the parent node. Required for child nodes, omit for root-level
            icon_url: Optional icon URL for this specific node

        Returns:
            LineageNodeV2 object containing id, node_entity_id, node_name, etc.
        """
        url = "/api/v2/lineage/nodes"
        request = CreateLineageNodeV2Request(
            node_name=node_name,
            node_type=node_type,
            node_container_name=node_container_name,
            workspace_id=self.config.workspace_id,
            custom_repository_id=custom_repository_id,
            custom_node_type_id=custom_node_type_id,
            node_container_entity_id=node_container_entity_id or 0,
            icon_url=icon_url or ""
        )
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return LineageNodeV2().from_dict(response)

    def get_lineage_node(self, node_id: int) -> LineageNodeV2:
        """
        Get a specific lineage node by ID.

        Args:
            node_id: ID of the node to retrieve

        Returns:
            LineageNodeV2 object containing the node details
        """
        url = f"/api/v2/lineage/nodes/{node_id}"
        response = self._call_datawatch(Method.GET, url=url)
        return LineageNodeV2().from_dict(response)

    def bulk_create_custom_lineage_nodes(self, nodes: List[CreateLineageNodeV2Request]) -> BulkResponse:
        """
        Create multiple custom lineage nodes in bulk.

        Args:
            nodes: List of CreateLineageNodeV2Request objects

        Returns:
            BulkResponse with successful_ids and failed_updates
        """
        url = "/api/v2/lineage/nodes/bulk"

        # Ensure workspace ID is set on each node
        for node in nodes:
            if node.workspace_id == 0:
                node.workspace_id = self.config.workspace_id

        request = CreateLineageNodeV2BulkRequest(nodes=nodes)
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return BulkResponse().from_dict(response)

    def upsert_custom_integration(self, integration: 'SimpleCustomIntegration') -> 'CustomIntegrationDeploymentResult':
        """
        Upsert a complete custom integration including integration type, node types, and repositories.

        This method orchestrates the creation/update of all components of a custom integration.
        It checks if existing resources match the incoming specs and updates them if they differ.

        Args:
            integration: SimpleCustomIntegration object containing the full integration definition

        Returns:
            CustomIntegrationDeploymentResult containing IDs of all created/updated resources
        """
        # Step 1: Create or update integration type
        log.info(f"Upserting custom integration: {integration.name}")

        # Check if integration type already exists
        existing_types = self.get_custom_integration_types()
        existing_type = next(
            (t for t in existing_types.types if t.name == integration.name),
            None
        )

        if existing_type:
            log.info(f"Integration type '{integration.name}' already exists with ID {existing_type.id}")
            integration.integration_type_id = existing_type.id

            # Check if existing integration type matches incoming specs
            needs_update = False
            update_fields = {}

            if existing_type.description != (integration.description or ""):
                needs_update = True
                update_fields['description'] = integration.description
                log.info(f"Description differs - will update")

            if existing_type.type != integration.type.to_protobuf():
                needs_update = True
                update_fields['type'] = integration.type.to_protobuf()
                log.info(f"Type differs - will update")

            if existing_type.icon_url != (integration.icon_url or ""):
                needs_update = True
                update_fields['icon_url'] = integration.icon_url
                log.info(f"Icon URL differs - will update")

            if needs_update:
                log.info(f"Updating integration type '{integration.name}' with fields: {list(update_fields.keys())}")
                updated_type = self.update_custom_integration_type(
                    integration_type_id=existing_type.id,
                    **update_fields
                )
                result = CustomIntegrationDeploymentResult(
                    integration_type_id=updated_type.id,
                    updated=True
                )
            else:
                log.info(f"Integration type '{integration.name}' matches specs - no update needed")
                result = CustomIntegrationDeploymentResult(
                    integration_type_id=existing_type.id,
                    updated=False
                )
        else:
            log.info(f"Creating new integration type: {integration.name}")
            created_type = self.create_custom_integration_type(
                name=integration.name,
                type=integration.type.to_protobuf(),
                description=integration.description,
                icon_url=integration.icon_url
            )
            integration.integration_type_id = created_type.id
            result = CustomIntegrationDeploymentResult(
                integration_type_id=created_type.id,
                created=True
            )
            log.info(f"Created integration type with ID: {created_type.id}")

        # Step 2: Create or update node types
        log.info(f"Deploying {len(integration.node_types)} node types")

        # Get existing node types for this integration
        all_node_types = self.get_custom_node_types()
        existing_node_types = {
            nt.name: nt for nt in all_node_types.types
            if nt.integration_type.id == integration.integration_type_id
        }

        # Check existing node types and separate new ones
        new_node_types = []
        for node_type in integration.node_types:
            if node_type.name in existing_node_types:
                existing = existing_node_types[node_type.name]
                node_type.id = existing.id
                result.node_type_ids[node_type.name] = existing.id
                log.info(f"Node type '{node_type.name}' already exists with ID {existing.id}")

                # Check if node type needs updating
                needs_update = False
                update_fields = {}

                if existing.name_plural != node_type.name_plural:
                    needs_update = True
                    update_fields['name_plural'] = node_type.name_plural
                    log.info(f"Node type '{node_type.name}' name_plural differs - will update")

                # Compare allowed_parent_types
                existing_parent_names = set(pt.name for pt in (existing.allowed_parent_types or []))
                incoming_parent_names = set(node_type.allowed_parent_types or [])
                if existing_parent_names != incoming_parent_names:
                    needs_update = True
                    # Build parent types list with proper structure
                    parent_types = [CustomNodeType(name=name) for name in incoming_parent_names]
                    update_fields['allowed_parent_types'] = parent_types
                    log.info(f"Node type '{node_type.name}' allowed_parent_types differ - will update")

                # Compare is_column_display value
                if existing.is_column_display != node_type.is_column_display:
                    needs_update = True
                    update_fields['is_column_display'] = node_type.is_column_display
                    log.info(f"Node type '{node_type.name}' is_column_display differs - will update")

                if needs_update:
                    log.info(f"Updating node type '{node_type.name}' with fields: {list(update_fields.keys())}")
                    self.update_custom_node_type(
                        node_type_id=existing.id,
                        **update_fields
                    )
                    result.updated = True
            else:
                new_node_types.append(node_type)

        # Create new node types in bulk if any
        if new_node_types:
            log.info(f"Creating {len(new_node_types)} new node types")
            protobuf_node_types = [
                nt.to_protobuf(integration.integration_type_id)
                for nt in new_node_types
            ]
            bulk_response = self.create_custom_node_types_bulk(protobuf_node_types)

            # Map IDs back to node type names
            # Note: The bulk response returns IDs in order, so we can match them
            if bulk_response.successful_ids:
                for i, node_type in enumerate(new_node_types):
                    if i < len(bulk_response.successful_ids):
                        node_id = bulk_response.successful_ids[i]
                        node_type.id = node_id
                        result.node_type_ids[node_type.name] = node_id
                        log.info(f"Created node type '{node_type.name}' with ID {node_id}")
                result.created = True

            if bulk_response.failed_updates:
                log.warning(f"Failed to create some node types: {bulk_response.failed_updates}")

        # Step 3: Create or update repositories
        if integration.repositories:
            log.info(f"Deploying {len(integration.repositories)} repositories")

            # Get existing repositories for this integration
            all_repos = self.get_custom_repositories()
            existing_repos = {
                r.name: r for r in all_repos.repositories
                if r.integration_type.id == integration.integration_type_id
            }

            for repo in integration.repositories:
                if repo.name in existing_repos:
                    existing = existing_repos[repo.name]
                    repo.id = existing.id
                    result.repository_ids[repo.name] = existing.id
                    log.info(f"Repository '{repo.name}' already exists with ID {existing.id}")
                else:
                    log.info(f"Creating repository: {repo.name}")
                    created_repo = self.create_custom_repository(
                        name=repo.name,
                        integration_type_id=integration.integration_type_id
                    )
                    repo.id = created_repo.id
                    result.repository_ids[repo.name] = created_repo.id
                    result.created = True
                    log.info(f"Created repository '{repo.name}' with ID {created_repo.id}")

        log.info(f"Successfully deployed custom integration '{integration.name}'")
        return result

    # Workspace Tags (v2 API)
    def get_tag(self, tag_id: int) -> Tag:
        """
        Get a single tag by ID.

        Args:
            tag_id: The ID of the tag

        Returns:
            Tag object
        """
        url = f"/api/v2/tags/{tag_id}"
        response = self._call_datawatch(Method.GET, url=url)
        return Tag().from_dict(response)

    def get_all_tags(self, get_tag_counts: bool = False) -> GetAllTagsResponse:
        """
        Get all tags with pagination and optional filtering.

        Returns:
            GetAllTagsResponse with tags and pagination info
        """
        request = GetAllTagsRequest()
        request.workspace_id = self.config.workspace_id
        request.get_tag_counts = get_tag_counts
        url = "/api/v2/tags/fetch"
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return GetAllTagsResponse().from_dict(response)

    def create_tag(self, request: CreateOrUpdateTagRequest) -> CreateOrUpdateTagResponse:
        """
        Create a new tag.

        Args:
            request: CreateOrUpdateTagRequest containing tag details (name, color_hex, workspace_id)

        Returns:
            CreateOrUpdateTagResponse with the created tag
        """
        url = "/api/v2/tags"
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return CreateOrUpdateTagResponse().from_dict(response)

    def update_tag(self, tag_id: int, request: CreateOrUpdateTagRequest) -> CreateOrUpdateTagResponse:
        """
        Update an existing tag.

        Args:
            tag_id: The ID of the tag to update
            request: CreateOrUpdateTagRequest containing updated tag details (name, color_hex)

        Returns:
            CreateOrUpdateTagResponse with the updated tag
        """
        url = f"/api/v2/tags/{tag_id}"
        response = self._call_datawatch(Method.PUT, url=url, body=request.to_json())
        return CreateOrUpdateTagResponse().from_dict(response)

    def delete_tag(self, tag_id: int) -> DeleteTagResponse:
        """
        Delete a tag.

        Args:
            tag_id: The ID of the tag to delete

        Returns:
            DeleteTagResponse with the deleted tag
        """
        url = f"/api/v2/tags/{tag_id}"
        response = self._call_datawatch(Method.DELETE, url=url)
        return DeleteTagResponse().from_dict(response)

    def tag(self, request: TagRequest) -> TagResponse:
        """
        Add a tag to an entity.

        Args:
            request: TagRequest containing the tag item and optional create_tag_if_does_not_exist flag

        Returns:
            TagResponse with the tagged item
        """
        url = "/api/v2/tags/tag"
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return TagResponse().from_dict(response)

    def untag(self, request: UntagRequest) -> UntagResponse:
        """
        Remove a tag from an entity.

        Args:
            request: UntagRequest containing the tag item details

        Returns:
            UntagResponse with the untagged item
        """
        url = "/api/v2/tags/untag"
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return UntagResponse().from_dict(response)

    def get_tagged_items(self, tag_id: int) -> List[TagItem]:
        """
        Get all items that have been tagged with a specific tag.

        Args:
            tag_id: The ID of the tag

        Returns:
            List of TagItem objects
        """
        url = f"/api/v2/tags/{tag_id}/items"
        response = self._call_datawatch(Method.GET, url=url)
        return GetTagItemResponse().from_dict(response).tags

    def get_catalog_entity_children(self, node_type: DataNodeType, node_id: int) -> GetCatalogEntityChildrenResponse:
        """
        Get children of a catalog entity. This is a generic method that works for any catalog entity type.

        Args:
            node_type: The type of the parent node (e.g., DataNodeType.DATA_NODE_TYPE_CUSTOM)
            node_id: The ID of the parent node

        Returns:
            GetCatalogEntityChildrenResponse containing all child entities
        """
        url = f"/api/v1/catalog-entities/{node_type.name}/{node_id}/children"
        request = GetCatalogEntityChildrenRequest()
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return GetCatalogEntityChildrenResponse().from_dict(response)

    def get_workflow_v2_status_bulk(self, workflow_v2_ids: List[WorkflowV2Id]) -> BulkWorkflowV2StatusResponse:
        """
        Get Workflow V2 status for a list of workflow IDs.
        """
        url = "/api/v2/workflows/status/bulk"
        request = BulkWorkflowV2StatusRequest(workflow_v2_ids=workflow_v2_ids)
        response = self._call_datawatch(Method.POST, url=url, body=request.to_json())
        return BulkWorkflowV2StatusResponse().from_dict(response)

    def wait_for_workflow_v2(
        self,
        workflow_id: WorkflowV2Id,
        poll_interval: int = 10,
        timeout: int = 600
    ) -> WorkflowV2StatusResponse:
        """Wait for a workflow to complete."""
        start_time = time.time()

        while True:
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(
                    f"Workflow {workflow_id} did not complete within {timeout} seconds"
                )

            # Get status
            response = self.get_workflow_v2_status_bulk(workflow_v2_ids=[workflow_id]).statuses[0]

            # Check status
            if response.status == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_COMPLETED:
                log.info(f"Workflow {workflow_id} completed successfully")
                return response
            elif response.status == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_FAILED:
                error_msg = response.error or "Unknown error"
                log.error(f"Workflow {workflow_id} failed: {error_msg}")
                raise Exception(f"Workflow failed: {error_msg}")
            elif response.status == WorkflowProcessingStatus.WORKFLOW_PROCESSING_STATUS_TIMED_OUT:
                log.warning(f"Workflow {workflow_id} has timed out")
                raise Exception("Workflow was cancelled")

            # Still running, log progress
            log.info(
                f"Workflow {workflow_id} status: {response.status.name} "
                f"(elapsed: {int(elapsed)}s)"
            )

            # Wait before next check
            time.sleep(poll_interval)

    def upsert_metric_to_collection(self,
                                    add_metric_ids: Union[int, List[int]],
                                    collection_name: Optional[str] = None,
                                    collection_id: Optional[int] = None) -> Collection:

        if not collection_name and not collection_id:
            raise InvalidConfigurationException("You must provide either a collection name or a collection id")

        if type(add_metric_ids) == int:
            mids = list(add_metric_ids)
        else:
            mids = add_metric_ids

        collections: List[Collection] = self.get_collections().collections

        if collection_name:
            collection_to_upsert = [c for c in collections
                                    if c.name.lower().strip() == collection_name.lower().strip()]
            if not collection_to_upsert:
                log.info(f"Collection {collection_name} does not exist. Creating with metric IDs {add_metric_ids}...")
                return self.create_collection(
                    collection_name=collection_name, description="Created via SDK", metric_ids=mids
                ).collection
        else:
            collection_to_upsert = [c for c in collections if c.id == collection_id]
            if not collection_to_upsert:
                raise CollectionNotFoundException(
                    f"Collection {collection_id} does not exist. Cannot create collection by ID."
                )

        collection = collection_to_upsert[0]
        for mid in mids:
            collection.metric_ids.append(mid)

        return self.update_collection(collection=collection).collection