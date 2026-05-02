import json
import logging
import time
import warnings
from abc import ABC
from dataclasses import asdict
from typing import List

import requests
from acceldata_sdk.client import TorchClientInterFace
from acceldata_sdk.common import Executor
from acceldata_sdk.constants import AssetSourceType, SdkSupportedVersions, TorchBuildVersion
from acceldata_sdk.constants import PolicyType, FailureStrategy, RuleExecutionStatus, \
    MIN_TORCH_BACKEND_VERSION_FOR_RULE_ID_API, TORCH_CONNECTION_TIMEOUT_MS, TORCH_READ_TIMEOUT_MS
from acceldata_sdk.errors import APIError, TorchSdkException
from acceldata_sdk.models.asset import Asset, Metadata
from acceldata_sdk.models.assetType import AssetType
from acceldata_sdk.models.common_types import PolicyExecutionRequest, ExecutionType
from acceldata_sdk.models.connection import ConnectionType, AnalyticsPipeline, Connection, ConnectionCheck, \
    ConnectionCheckStatus
from acceldata_sdk.models.datasource import DataSource, SourceType, CrawlerStatus
from acceldata_sdk.models.dqrule import DataQualityExecutionResult, DataQualityRuleResource
from acceldata_sdk.models.freshnessrule import FreshnessRuleResource
from acceldata_sdk.models.job import Job
from acceldata_sdk.models.pipeline import CreatePipeline, Pipeline, PipelineRun, PipelineDetails, PipelineSourceType, \
    PipelineListingInfo, PipelineSummaryMeta, PipelineSummary
from acceldata_sdk.models.profile import Profile, ProfileRequest
from acceldata_sdk.models.reconcillationrule import ReconciliationExecutionResult, ReconciliationRuleResource
from acceldata_sdk.models.rule import Rule, RuleCancelResponse, RuleExecution, ExecutionResult
from acceldata_sdk.models.ruleExecutionResult import RuleResult, PolicyFilter, RuleType, \
    RuleExecutionSummary
from acceldata_sdk.models.span import Span, SpanContextEvent, CreateSpanEvent
from acceldata_sdk.models.tags import TAG, AssetTag, AssetLabel
from acceldata_sdk.time_range_utils import TimeRangeCalculator
from acceldata_sdk.utils.api_version_utils import APIVersionUtils
from requests_toolbelt import MultipartEncoder
from semantic_version import Version, SimpleSpec

_HEADERS = {'User-Agent': 'Acceldata-sdk', 'accessKey': None, 'secretKey': None, 'Content-Type': 'application/json'}
catalog_api_path = "/catalog-server/api"
pipeline_api_path = "/torch-pipeline/api"
admin_api_path = "/admin/api"

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TorchHttpClient(TorchClientInterFace, ABC):
    access_key = None
    secret_key = None
    logger = logging.getLogger('torch')
    logger.setLevel(logging.INFO)

    # Create torch client by passing secret and access keys of catalog server for a given url
    def __init__(self, url, torch_connection_timeout_ms=TORCH_CONNECTION_TIMEOUT_MS, access_key: str = None,
                 secret_key: str = None, torch_read_timeout_ms=TORCH_READ_TIMEOUT_MS):
        """
            Description : Torch client is used to send data to catalog server.

            :param url: (String) url of the catalog server
                        ex:  https://torch.acceldata.local:5443
            :param torch_connection_timeout_ms: (int) Maximum time (in milliseconds) to wait while establishing a connection to the ADOC server. Default: 5000 ms.
            :param access_key: (String) Access key of API key. You can generate API key from torch ui's setting
            :param secret_key: (String) Secret key of API key.
            :param torch_read_timeout_ms: (int) Maximum time (in milliseconds) to wait for a response from the ADOC server after a successful connection. Default: 15000 ms.

            : TorchClient = TorchClient(url='https://torch.acceldata.local:5443', access_key='OY2VVIN2N6LJ', secret_key='da6bDBimQfXSMsyyhlPVJJfk7Zc2gs')
        """
        self.logger.debug(f'timeout_ms {torch_connection_timeout_ms}')
        self._torch_connection_timeout = torch_connection_timeout_ms / 1000
        self._torch_read_timeout = torch_read_timeout_ms / 1000
        self._catalog_api_base = f"{url}{catalog_api_path}"
        self._pipeline_api_base = f"{url}{pipeline_api_path}"
        is_onprem = url.endswith('/torch')
        loc = url.rfind('/torch')
        if is_onprem:
            self._admin_api_base = f"{url[:loc]}{admin_api_path}"
        else:
            self._admin_api_base = f"{url}{admin_api_path}"

        if access_key is None and secret_key is None:
            raise Exception("ADOC credentials are missing. Please provide both access_key and secret_key.")
        self.access_key = access_key
        self.secret_key = secret_key

        _HEADERS['accessKey'] = access_key
        _HEADERS['secretKey'] = secret_key

    # # convert pipeline object to dict type
    def _convert_pipeline_to_dict(self, pipeline: CreatePipeline):
        """
        Description:
            Convert pipeline object to dict type.
        :param pipeline: createPipeline class instance
        :return: pipeline in dict type
        """
        pipeline_dict = {k: v for k, v in pipeline.__dict__.items() if v is not None}
        if pipeline.meta is not None:
            meta = asdict(pipeline.meta)
            pipeline_dict['meta'] = meta
            # Check if sourceType is an instance of PipelineSourceType, and convert it using to_dict
        if isinstance(pipeline.sourceType, PipelineSourceType):
            pipeline_dict['sourceType'] = pipeline.sourceType.to_dict()
        return pipeline_dict

    def get_supported_sdk_versions(self) -> SdkSupportedVersions:
        warnings.warn(
            "`do_version_check` is deprecated and will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        response = self._get(
            f'{self._catalog_api_base}/sdk/compatible-versions'
        )
        return SdkSupportedVersions(**response['versions'])

    def get_torch_version(self) -> TorchBuildVersion:
        response = self._get(
            f'{self._admin_api_base}/build-details'
        )
        return TorchBuildVersion(**response)

    # function to create pipeline
    def create_pipeline(self, pipeline: CreatePipeline) -> Pipeline:
        """
        Description:
            Used to create pipeline
        :param pipeline: createPipeline class instance that you want to create
        :return: pipeline class instance
        """
        payload = self._convert_pipeline_to_dict(pipeline)
        pipeline_payload = {'pipeline': payload}
        response = self._put(
            f'{self._pipeline_api_base}/pipelines',
            payload=pipeline_payload
        )
        response['pipeline']['client'] = self
        self.logger.info('Pipeline Created')
        return Pipeline(**response['pipeline'])

    # function to delete pipeline
    def delete_pipeline(self, id):
        """
        Description:
            Used to delete pipeline
        :param id: id of pipeline
        """

        response = self._delete(
            f'{self._pipeline_api_base}/pipelines/{id}'
        )
        self.logger.info(f'Pipeline {id} deleted')
        return response

    # get pipeline by uid or id
    def get_pipeline(self, pipeline_identity) -> Pipeline:
        """
            Description:
                To get an existing pipeline from torch catalog
        :param pipeline_identity: uid or id of the pipeline
        :return:(Pipeline) pipeline class instance
        """
        url = f'{self._pipeline_api_base}/pipelines/{pipeline_identity}'
        response = self._get(url)
        response['pipeline']['client'] = self
        return Pipeline(**response['pipeline'])

    # get all pipelines
    def get_pipelines(self) -> List[PipelineListingInfo]:
        """
            Description:
                To get all pipelines from ADOC
        :return:(List[PipelineListingInfo]) PipelineListingInfo class instance
        """
        url = f'{self._pipeline_api_base}/pipelines/summary'
        response = self._get(url)
        pipelines_infos = list()
        pipelines = response['pipelines']
        for obj in pipelines:
            pipeline_summary_meta = PipelineSummaryMeta(
                codeLocation=obj['pipelineSummary']['meta']['codeLocation'],
                owner=obj['pipelineSummary']['meta']['owner'],
                team=obj['pipelineSummary']['meta']['team']
            )
            pipeline_summary = PipelineSummary(
                id=obj['pipelineSummary']['id'],
                name=obj['pipelineSummary']['name'],
                meta=pipeline_summary_meta
            )
            pipelines_infos.append(
                PipelineListingInfo(
                    assetNodesCount=obj['assetNodesCount'],
                    functionalNodesCount=obj['functionalNodesCount'],
                    latestRunFinishedAt=obj['latestRunFinishedAt'],
                    latestRunId=obj['latestRunId'],
                    latestRunResult=obj['latestRunResult'],
                    latestRunStartedAt=obj['latestRunStartedAt'],
                    latestRunVersionId=obj['latestRunVersionId'],
                    pipelineSummary=pipeline_summary,
                    successfulPoliciesCount=obj['policyCounts']['SUCCESSFUL'],
                    totalPoliciesCount=obj['policyCounts']['TOTAL'],
                    totalRunsCount=obj['totalRunsCount']
                )
            )

        return pipelines_infos

    # to create job for any given pipeline
    def create_job(self, job: {}, pipelineId: int) -> Job:
        """
        Description:
            Used to create job in a pipeline
        :param pipelineId: pipeline id of the respective pipeline
        :param job: createJob class instance that you want to add in pipeline
        :return: Job class instance of created job
        """
        response = self._put(
            f'{self._pipeline_api_base}/pipelines/{pipelineId}/jobs',
            payload=job
        )
        self.logger.info('Pipeline Job Created')
        return Job(**response['node'])

    def delete_datasource(self, datasource_id: int):
        """
        Description:
            used to delete datasource
        :param datasource_id: id of the datasource to be updated
        :return: response of the operation
        """
        response = self._delete(
            f'{self._catalog_api_base}/assemblies/{datasource_id}'
        )
        return response

    def start_crawler(self, datasource_name) -> CrawlerStatus:
        response = self._post(
            f'{self._catalog_api_base}/crawler/{datasource_name}',
            payload={}
        )
        return CrawlerStatus(**response['data'])

    def get_crawler_status(self, datasource_name) -> CrawlerStatus:
        response = self._get(
            f'{self._catalog_api_base}/crawler/{datasource_name}',
        )
        return CrawlerStatus(**response['data'])

    # create run for a pipeline
    def create_pipeline_run(self, pipeline_run: {}) -> PipelineRun:
        """
        Description:
            used to create a pipeline run
        :param pipeline_run:
        :return: pipelineRun class instance
        """
        pipelineId = pipeline_run['run']['pipelineId']
        response = self._post(
            f'{self._pipeline_api_base}/pipelines/{pipelineId}/runs',
            payload=pipeline_run
        )
        response['run']['client'] = self
        self.logger.info('Pipeline Run Created')
        return PipelineRun(**response['run'])

    # update run for a pipeline
    def update_pipeline_run(self, pipeline_run_id: int, pipeline_run: {}) -> PipelineRun:
        """
        Description:
            used to update an existing pipeline run
        :param pipeline_run_id: pipeline run id that you want to update
        :param pipeline_run: pipelineRun class instance that you want to update
        :return: updated pipelineRun class instance
        """
        response = self._put(
            f'{self._pipeline_api_base}/pipelines/runs/{pipeline_run_id}',
            payload=pipeline_run
        )
        response['run']['client'] = self
        self.logger.info('Pipeline Run Updated')
        return PipelineRun(**response['run'])

    # get latest pipeline run
    def get_latest_pipeline_run(self, pipeline_id: int) -> PipelineRun:
        """
            Description:
                To get latest pipeline run instance of any pipeline
        :param pipeline_id: id of the pipeline
        :return: PipelineRun instance
        """
        url = f'{self._pipeline_api_base}/pipelines/{pipeline_id}/latestRun'
        response = self._get(url)
        response['run']['client'] = self
        return PipelineRun(**response['run'])

    # get pipeline run with particular continuation id or run id
    def get_pipeline_run(self, pipeline_run_id: int = None, continuation_id: str = None,
                         pipeline_id: str = None) -> PipelineRun:
        """
            Description:
                To get pipeline run with particular id or continuation id of any pipeline
        :param pipeline_run_id: run id of the pipeline run
        :param continuation_id: continuation id of the pipeline run
        :param pipeline_id: id of the pipeline. This is a mandatory parameter when run is being queried using continuation_id
        :return: PipelineRun instance
        """
        if pipeline_run_id is not None:
            url = f'{self._pipeline_api_base}/pipelines/runs/{pipeline_run_id}'
            response = self._get(url)
            return_run = response['run']
        elif continuation_id is not None and pipeline_id is not None:
            url = f'{self._pipeline_api_base}/pipelines/{pipeline_id}/runs'
            payload = {"continuationId": continuation_id}
            response = self._get(url, params=payload)
            if response["runs"] is not None and len(response["runs"]) > 0:
                return_run = response["runs"][0]
            else:
                raise TorchSdkException(f"No runs found against the given continuation_id: {continuation_id}")
        else:
            raise TorchSdkException('Please provide either continuation_id and pipeline_id or pipeline_run_id')

        return_run['client'] = self
        return PipelineRun(**return_run)

    # get pipeline runs for a pipeline
    def get_pipeline_runs(self, pipeline_id: int) -> List[PipelineRun]:
        """
            Description:
                To get pipeline run  id of any pipeline
        :param pipeline_id: id of the pipeline
        :return: List[PipelineRun] instance
        """
        url = f'{self._pipeline_api_base}/pipelines/{pipeline_id}/runs'
        response = self._get(url)
        runs = list(response['runs'])
        runs_list = []
        for res in runs:
            res['client'] = self
            runs_list.append(PipelineRun(**res))
        return runs_list

    # create span for pipeline run
    def create_span(self, pipeline_run_id: int, span: dict) -> Span:
        """
        Description:
            used to create span for any pipeline run
        :param pipeline_run_id:
        :param span: Span class instance
        :return: Span
        """
        response = self._post(
            f'{self._pipeline_api_base}/pipelines/runs/{pipeline_run_id}/spans',
            payload=span
        )
        self.logger.info('Span Created')
        return Span(**response['span'])

    def get_child_spans(self, span_id: int):
        response = self._get(
            f'{self._pipeline_api_base}/pipelines/spans/{span_id}/childSpans'
        )
        self.logger.info('Fetched child spans.')
        child_spans = list(response['childSpans'])
        child_spans_res = []
        for res in child_spans:
            child_spans_res.append(Span(**res))
        return child_spans_res

    def get_span(self, pipeline_run_id: int, uid: str) -> Span:
        """
            Description:
                Get span of the pipeline run by uid
        :param pipeline_run_id: pipeline run id
        :param uid: uid of the span
        :return: SpanContext instance of the input span uid
        """
        url = f'{self._pipeline_api_base}/pipelines/runs/{pipeline_run_id}/spans/{uid}'
        response = self._get(url)
        response['span']['client'] = self
        return Span(**response['span'])

    def get_root_span(self, pipeline_run_id: int) -> Span:
        """
            Description:
                Get root span of the pipeline run
        :param pipeline_run_id: pipeline run id
        :return: SpanContext instance of the root span
        """
        url = f'{self._pipeline_api_base}/pipelines/runs/{pipeline_run_id}/spans'
        params = {"onlyRootSpan": "true"}
        response = self._get(url, params=params)
        return_value = dict()
        return_value['span'] = dict()
        return_value['span']['client'] = self
        if response['spans']:
            return_value['span'] = response['spans'][0]
            return_value['span']['client'] = self
            return Span(**return_value['span'])
        else:
            return None

    def get_spans(self, pipeline_run_id):
        response = self._get(
            f'{self._pipeline_api_base}/pipelines/runs/{pipeline_run_id}/spans'
        )
        self.logger.info('Fetched spans.')
        spans = list(response['spans'])
        spans_res = []
        for res in spans:
            spans_res.append(Span(**res))
        return spans_res

    # convert span object to dict type
    def convert_span_event_to_dict(self, span_event: CreateSpanEvent):
        """
            Description:
                Convert CreateSpanEvent class instance to dict type
            :param spanEvent: CreateSpanEvent class instance
            :return: dict form of CreateSpanEvent class instance
        """
        payload = span_event.__dict__
        # payload['eventUid'] = span_event.eventType
        event_payload = {'event': payload}
        return event_payload

    # create span event for any span
    def create_span_event(self, span_event: CreateSpanEvent) -> SpanContextEvent:
        """
        Description:
            used to create span event
        :param span_event: CreateSpanEvent class instance that you want to create
        :return: SpanContextEvent class instance
        """
        payload = self.convert_span_event_to_dict(span_event)
        if span_event.spanId is None:
            Exception('To update a pipeline run, id is required.')
        response = self._post(
            f'{self._pipeline_api_base}/pipelines/spans/{span_event.spanId}/events',
            payload=payload
        )
        self.logger.info('Span Event Created')
        return SpanContextEvent(**response['event'])

    def get_run_details(self, pipeline_id: int, version_id: int):
        """
            Description:
                Get details of the pipeline by versionid
        :param pipeline_id: pipeline  id
        :param version_id: version_id of the pipeline
        :return: SpanContext instance of the input span uid
        """
        url = f'{self._pipeline_api_base}/pipelines/{pipeline_id}/graph?versionId={version_id}'
        response = self._get(url)
        details = response['details']
        details['pipeline']['client'] = self
        return PipelineDetails(**details)

    def get_all_asset_types(self):
        """
        Description:
            get all asset types supported in torch xatalog
        :return: list of asset types
        """
        response = self._get(
            f'{self._catalog_api_base}/asset-types'
        )
        asset_types = list(response['data'])
        asset_types_res = []
        for res in asset_types:
            asset_types_res.append(AssetType(**res))
        return asset_types_res

    def get_all_source_types(self):
        """
        Description:
            get all source types supported in torch catalog
        :return: list of all source type
        """
        response = self._get(
            f'{self._catalog_api_base}/source-types'
        )
        source_types = list(response['data'])
        source_types_res = []
        for res in source_types:
            source_types_res.append(SourceType(**res))
        return source_types_res

    def get_connection_types(self):
        """
        Description:
            get all source types supported in torch catalog
        :return: list of all source type
        """
        response = self._get(
            f'{self._catalog_api_base}/connection-types'
        )
        connection_types = list(response['data'])
        conn_type_response = []
        for res in connection_types:
            conn_type_response.append(ConnectionType(**res))
        return conn_type_response

    def get_tags(self):
        response = self._get(
            f'{self._catalog_api_base}/assets/tags'
        )
        tags = list(response['tags'])
        tags_list = []
        for res in tags:
            tags_list.append(TAG(**res))
        return tags_list

    def get_datasource(self, assembly_identifier, properties: bool = False) -> DataSource:
        """
        Description:
            Find datasource by its name or id in torch catalog
        :param assembly_identifier: name or id of the datasource given in torch
        :param properties: optional parameter, bool, to get datasource properties as well
        :return: (DataSource) datasource
        """
        url = f'{self._catalog_api_base}/assemblies/{assembly_identifier}?properties={properties}'

        response = self._get(url)
        datasource = response['data']
        if len(datasource) > 0:
            datasource['client'] = self
            return DataSource(**datasource)
        raise Exception('Datasource not found.')

    def get_datasources(self, type: AssetSourceType = None) -> List[DataSource]:
        """
        Description:
            Find datasources by its type in torch catalog
        :param type: type of the datasource given in torch, optional
        :return: list(DataSource) datasource
        """
        url = f'{self._catalog_api_base}/assemblies'
        if type is not None:
            params = dict()
            params['sourceType'] = type.name
            response = self._get(url, params=params)
        else:
            response = self._get(url)
        datasources = list(response['data'])
        ds_list = []
        for res in datasources:
            res['client'] = self
            ds_list.append(DataSource(**res))
        return ds_list
        raise Exception('Datasource not found.')

    def get_all_datasources(self):
        """
        Description:
            list all datasources in torch catalog
        :return: (DataSource) list of datasource
        """
        url = f'{self._catalog_api_base}/assemblies'
        response = self._get(url)
        datasources = list(response['data'])
        ds_list = []
        for res in datasources:
            ds_list.append(DataSource(**res))
        return ds_list

    def get_asset(self, identifier):
        """"
            Description:
                Find an asset of the datasource
            :param identifier: uid or ID of the asset
        """
        if TimeRangeCalculator.check_int(identifier):
            return self.get_asset_by_id(id=identifier)
        else:
            return self.get_asset_by_uid(uid=identifier)

    def get_asset_by_id(self, id: int) -> Asset:
        """
        Description:
            used to find an asset
        :param id: id of an asset
        :return: asset data (Asset)
        """
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets?ids={id}'
        asset = self._get_asset(url)
        asset_res = list(asset['data'])[0]
        asset_res['client'] = self
        return Asset(**asset_res)

    def get_asset_by_uid(self, uid: str):
        """
        Description:
            used to find an asset
        :param uid: uid of an asset
        :return: asset data (Asset)
        """
        if uid is None:
            raise Exception('Asset uid is required')
        url = f'{self._catalog_api_base}/assets?uid={uid}'
        asset = self._get_asset(url)
        if asset is None:
            return None
        asset_data = asset['data']
        if asset_data is None or not asset_data or len(asset_data) == 0:
            return None
        asset_res = list(asset_data)[0]
        asset_res['client'] = self
        return Asset(**asset_res)

    def _get_asset(self, url: str):
        response = self._get(
            url=url
        )
        return response

    def get_asset_metadata(self, id: int):
        url = f'{self._catalog_api_base}/assets/{id}/metadata'
        response = self._get(
            url=url
        )
        metadata = Metadata(**response['data'])
        return metadata

    def add_custom_metadata(self, id: int, custom_metadata: dict):
        url = f'{self._catalog_api_base}/assets/{id}/metadata/custom'
        response = self._post(
            url=url,
            payload=custom_metadata
        )
        metadata = Metadata(**response['data'])
        return metadata

    def profile_asset(self, id: int, payload: dict) -> Profile:
        url = f'{self._catalog_api_base}/assets/{id}/profile'
        response = self._post(
            url=url,
            payload=payload
        )
        response['data']['client'] = self
        profile_response = Profile(**response['data'])
        return profile_response

    def sample_data(self, asset_id: int):
        url = f'{self._catalog_api_base}/assets/{asset_id}/sample/async'
        response = self._post(url=url, as_json=True, payload={})

        # This is a file/kafka based asset sampling
        if response is not None and response.get('requestId') is not None:
            request_id = response['requestId']
            sample_data_result = self.get_sample_data_result(request_id)

            while sample_data_result['jobExecutionStatus'] == 'IN_PROGRESS':
                time.sleep(5)
                sample_data_result = self.get_sample_data_result(request_id)

            return sample_data_result
        else:
            return response

    def get_sample_data_result(self, request_id: str):
        url = f'{self._catalog_api_base}/assets/sample/result/{request_id}'
        response = self._get(
            url=url
        )
        return response

    def get_profile_request_details(self, asset_id: int, req_id: int):
        url = f'{self._catalog_api_base}/assets/{asset_id}/profile/{req_id}'
        response = self._get(
            url=url
        )
        return response

    def get_latest_profile_status(self, id: int):
        url = f'{self._catalog_api_base}/assets/{id}/profile'
        response = self._get(
            url=url
        )
        response['data']['client'] = self
        profile_response = ProfileRequest(**response['data'])
        return profile_response

    def cancel_profile(self, profile_req_id: int):
        url = f'{self._catalog_api_base}/assets/profile/{profile_req_id}/cancel'
        response = self._put(
            url=url,
            payload={}
        )
        return response['result']

    def get_asset_tags(self, id: int):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/tags'
        response = self._get(
            url=url
        )
        tags = list(response['assetTags'])
        tags_list = []
        for res in tags:
            tags_list.append(AssetTag(**res))
        return tags_list

    def add_asset_tag(self, id: int, payload: dict):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/tag'
        response = self._post(
            url=url, payload=payload
        )
        return AssetTag(**response)

    def add_asset_labels(self, id: int, payload: dict):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/labels'
        response = self._put(
            url=url, payload=payload
        )
        labels = list(response)
        labels_list = []
        for lbl in labels:
            labels_list.append(AssetLabel(**lbl))
        return labels_list

    def get_asset_labels(self, id: int):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/labels'
        response = self._get(
            url=url
        )
        labels = list(response)
        labels_list = []
        for lbl in labels:
            labels_list.append(AssetLabel(**lbl))
        return labels_list

    def get_analysis_pipeline(self, id: int) -> AnalyticsPipeline:
        response = self._get(
            url=f'{self._catalog_api_base}/analytics-pipelines/{id}'
        )
        return AnalyticsPipeline(**response['pipeline'])

    def check_connection(self, create_connection):
        create_conn = create_connection.__dict__
        config_prop = []
        for cp in create_connection.properties:
            config_prop.append(asdict(cp))
        create_conn['properties'] = config_prop
        payload = {
            'connection': create_conn
        }
        url = f'{self._catalog_api_base}/connections/check'
        response = self._post_form_data(
            url=url,
            payload=payload
        )
        check_res = ConnectionCheck(**response['result'])
        if check_res.status == ConnectionCheckStatus.SUCCESS.value:
            return check_res
        if check_res.status == ConnectionCheckStatus.FAILURE.value:
            raise TorchSdkException(f'Error: {check_res.message}')
        return check_res

    def create_connection(self, create_connection) -> Connection:
        create_conn = create_connection.__dict__
        config_prop = []
        # for cp in create_connection.properties:
        #     config_prop.append(asdict(cp))
        # create_conn['properties'] = config_prop
        payload = {
            'connection': create_conn
        }
        url = f'{self._catalog_api_base}/connections'
        response = self._post_form_data(
            url=url,
            payload=payload
        )
        return Connection(**response['connection'])

    def enable_rule(self, rule_id) -> Rule:
        payload = {
            "enable": True
        }
        response = self._put(
            url=f'{self._catalog_api_base}/rules/{rule_id}/enable',
            payload=payload
        )
        return Rule(**response['rule'])

    def disable_rule(self, rule_id) -> Rule:
        payload = {
            "enable": False
        }
        response = self._put(
            url=f'{self._catalog_api_base}/rules/{rule_id}/enable',
            payload=payload
        )
        return Rule(**response['rule'])

    def cancel_rule_execution(self, execution_id) -> RuleCancelResponse:
        response = self._put(
            url=f'{self._catalog_api_base}/rules/execution/{execution_id}/cancel',
            payload={}
        )
        return RuleCancelResponse(**response['result'])

    def execute_rule(self, rule_type: PolicyType, rule_id, sync=True, incremental=False,
                     failure_strategy: FailureStrategy = FailureStrategy.DoNotFail, pipeline_run_id=None,
                     policy_execution_request: PolicyExecutionRequest = None):
        """
        Description:
            To execute rule synchronously and asynchronously
        :param rule_type: (PolicyType) Type of rule to be executed
        :param rule_id: (String) id of the rule to be executed
        :param sync: (bool) optional Set it to False if asynchronous execution has to be done
        :param incremental: (bool) optional Set it to True if full execution has to be done
        :param failure_strategy: (enum) optional Set it to decide if it should fail at error,
            fail at warning or never fail
        :param policy_execution_request: (PolicyExecutionRequest) An optional parameter that allows you to provide
        additional options for executing the policy. It is an instance of the PolicyExecutionRequest modules class,
        which contains various properties that can be used to customize the policy execution, such as `executionType`,
        `markerConfigs`, `ruleItemSelections`, and more.
        """
        self.logger.info(
            f"Policy Execution Request: {policy_execution_request.to_dict() if policy_execution_request else 'None'}")

        rule_executor = Executor(rule_type, self, sync=sync)
        rule_executor.execute(rule_id, incremental, failure_strategy=failure_strategy, pipeline_run_id=pipeline_run_id,
                              policy_execution_request=policy_execution_request)
        return rule_executor

    def get_rule_status(self, rule_type, execution_id) -> RuleExecutionStatus:
        """
        Description:
            To get status of rule execution
        :param rule_type: (String) Type of rule to be executed
        :param execution_id: (String) ID of execution of the rule previously executed.
        """
        rule_executor = Executor(rule_type, self)
        return rule_executor.get_execution_status(execution_id)

    def get_rule_execution_result(self, rule_type, execution_id,
                                  failure_strategy: FailureStrategy = FailureStrategy.DoNotFail):
        """
        Description:
            To get result of rule execution
        :param rule_type: (String) Type of rule to be executed
        :param execution_id: (String) ID of execution of the rule previously executed.
        :param failure_strategy: (enum) optional Set it to decide if it should fail at error,
            fail at warning or never fail
        """
        rule_executor = Executor(rule_type, self)
        return rule_executor.get_execution_result(execution_id, failure_strategy=failure_strategy)

    def execute_dq_rule(self, rule_id, incremental=False, pipeline_run_id=None,
                        policy_execution_request: PolicyExecutionRequest = None) -> RuleExecution:

        self.logger.info(
            f"Invoked execute_dq_rule of the torch_http_client\n"
            f"Incremental flag: {incremental}\n"
            f"Policy Execution Request: {policy_execution_request.to_dict() if policy_execution_request else 'None'}"
        )
        payload_temp = dict()

        if policy_execution_request is None and not incremental:
            self.logger.info(
                "policy_execution_request is None and incremental is also false. Setting the executionType to FULL")
            payload_temp['executionType'] = "FULL"

        if pipeline_run_id is not None:
            self.logger.info(f"Setting up pipeline run ID: {pipeline_run_id}")
            payload_temp['pipelineRunId'] = pipeline_run_id

        if policy_execution_request is not None:
            self.logger.info(f"Marker config: {policy_execution_request.markerConfigs}")
            if policy_execution_request.executionType == ExecutionType.SELECTIVE and policy_execution_request.markerConfigs is None:
                raise TorchSdkException(
                    f'markerConfig is a mandatory parameter for execution type {ExecutionType.SELECTIVE}')
            else:
                self.logger.info("Converting policy_execution_request to dictionary")
                payload_temp = policy_execution_request.to_dict()

        elif incremental:
            self.logger.info("Setting the executionType to INCREMENTAL")
            payload_temp['executionType'] = "INCREMENTAL"

        self.logger.info(f"Executing DQ policy with the following payload: {payload_temp}")
        response = self._post(
            url=f'{self._catalog_api_base}/rules/data-quality/{rule_id}/executions',
            payload=payload_temp
        )
        return RuleExecution(**response['execution'])

    def execute_reconciliation_rule(self, rule_id, incremental=False, pipeline_run_id=None,
                                    policy_execution_request: PolicyExecutionRequest = None) -> RuleExecution:
        self.logger.info(
            f"Invoked execute_reconciliation_rule of the torch_http_client\n"
            f"Incremental flag: {incremental}\n"
            f"Policy Execution Request: {policy_execution_request.to_dict() if policy_execution_request else 'None'}"
        )
        payload_temp = dict()

        if policy_execution_request is None and not incremental:
            self.logger.info(
                "Policy execution request is None and incremental is also false. Setting the executionType to FULL")
            payload_temp['executionType'] = "FULL"

        if pipeline_run_id is not None:
            self.logger.info(f"Setting up pipeline run ID: {pipeline_run_id}")
            payload_temp['pipelineRunId'] = pipeline_run_id

        if policy_execution_request is not None:
            self.logger.info(f"Marker config: {policy_execution_request.markerConfigs}")
            if policy_execution_request.executionType == ExecutionType.SELECTIVE and policy_execution_request.markerConfigs is None:
                raise TorchSdkException(
                    f'markerConfig is a mandatory parameter for execution type {ExecutionType.SELECTIVE}')
            else:
                self.logger.info("Converting policy_execution_request to dictionary")
                payload_temp = policy_execution_request.to_dict()
                self.logger.info(f"Policy execution request to dictionary: {payload_temp}")
        elif incremental:
            self.logger.info("Setting the executionType to INCREMENTAL")
            payload_temp['executionType'] = "INCREMENTAL"

        self.logger.info(f"Executing Reconciliation policy with the following payload: {payload_temp}")
        response = self._post(
            url=f'{self._catalog_api_base}/rules/reconciliation/{rule_id}/executions',
            payload=payload_temp
        )
        return RuleExecution(**response['execution'])

    def execute_freshness_rule(self, rule_id, incremental=False, pipeline_run_id=None,
                               policy_execution_request: PolicyExecutionRequest = None) -> RuleExecution:
        self.logger.info(
            f"Invoked execute_freshness_rule of the torch_http_client\n"
            f"Incremental flag: {incremental}\n"
            f"Policy Execution Request: {policy_execution_request.to_dict() if policy_execution_request else 'None'}"
        )
        payload_temp = dict()

        if policy_execution_request is None and not incremental:
            self.logger.info(
                "Policy execution request is None and incremental is also false. Setting the executionType to FULL")
            payload_temp['executionType'] = "FULL"

        if pipeline_run_id is not None:
            self.logger.info(f"Setting up pipeline run ID: {pipeline_run_id}")
            payload_temp['pipelineRunId'] = pipeline_run_id

        if policy_execution_request is not None:
            self.logger.info(f"Marker config: {policy_execution_request.markerConfigs}")
            if policy_execution_request.executionType == ExecutionType.SELECTIVE and policy_execution_request.markerConfigs is None:
                raise TorchSdkException(
                    f'markerConfig is a mandatory parameter for execution type {ExecutionType.SELECTIVE}')
            else:
                self.logger.info("Converting policy_execution_request to dictionary")
                payload_temp = policy_execution_request.to_dict()
                self.logger.info(f"Policy execution request to dictionary: {payload_temp}")
        elif incremental:
            self.logger.info("Setting the executionType to INCREMENTAL")
            payload_temp['executionType'] = "INCREMENTAL"

        self.logger.info(f"Executing Freshness policy with the following payload: {payload_temp}")
        response = self._post(
            url=f'{self._catalog_api_base}/rules/data-cadence/{rule_id}/executions',
            payload=payload_temp
        )
        return RuleExecution(**response['execution'])

    def get_dq_rule(self, rule_id) -> DataQualityRuleResource:
        response = self._get(
            url=f'{self._catalog_api_base}/rules/data-quality/{rule_id}'
        )
        response['client'] = self
        return DataQualityRuleResource(**response)

    def get_reconciliation_rule(self, rule_id) -> ReconciliationRuleResource:
        response = self._get(
            url=f'{self._catalog_api_base}/rules/reconciliation/{rule_id}'
        )
        response['client'] = self
        return ReconciliationRuleResource(**response)

    def get_freshness_rule(self, rule_id) -> FreshnessRuleResource:
        response = self._get(
            url=f'{self._catalog_api_base}/rules/data-cadence/{rule_id}'
        )
        response['client'] = self
        return FreshnessRuleResource(**response)

    def get_policy(self, identifier) -> Rule:
        """
        Description:
                To get an existing policy from torch catalog
        :param identifier: uid or id of the policy
        :return:(Policy) policy class instance
        """

        torch_version = self.get_torch_version()
        actual_version = APIVersionUtils.extract_actual_version(torch_version)
        APIVersionUtils.validate_torch_version_for_rule_id_api(actual_version)

        if Version(MIN_TORCH_BACKEND_VERSION_FOR_RULE_ID_API) in SimpleSpec(f'<={actual_version}'):
            url = f'{self._catalog_api_base}/rules/{identifier}'
            response = self._get(url)
            response['client'] = self
            return Rule(**response)
        else:
            raise TorchSdkException(
                f'This API is supported starting version: {self.MIN_TORCH_BACKEND_VERSION_FOR_RULE_ID_API}')

    def get_dq_rule_execution_details(self, execution_id) -> ExecutionResult:
        response = self._get(
            url=f'{self._catalog_api_base}/rules/data-quality/executions/{execution_id}'
        )
        return ExecutionResult(**response)

    def get_reconciliation_rule_execution_details(self, execution_id) -> ExecutionResult:
        response = self._get(
            url=f'{self._catalog_api_base}/rules/reconciliation/executions/{execution_id}'
        )
        return ExecutionResult(**response)

    def get_reconciliation_rule_result(self, execution_id) -> RuleResult:
        response = self._get(
            url=f'{self._catalog_api_base}/rules/reconciliation/executions/{execution_id}/result'
        )
        return ReconciliationExecutionResult(**response)

    def get_freshness_rule_result(self, execution_id) -> RuleResult:
        response = self._get(
            url=f'{self._catalog_api_base}/rules/data-cadence/executions/{execution_id}/result'
        )
        self.logger.info(response)
        return ExecutionResult(**response)

    def get_dq_rule_result(self, execution_id) -> RuleResult:
        response = self._get(
            url=f'{self._catalog_api_base}/rules/data-quality/executions/{execution_id}/result'
        )
        return DataQualityExecutionResult(**response)

    def policy_executions(self, identifier, rule_type: RuleType, page=0, size=25,
                          sortBy='finishedAt:DESC') -> List[RuleExecutionSummary]:
        params = dict()
        params['page'] = page
        params['size'] = size
        params['sortBy'] = sortBy
        rule_id = identifier
        if not TimeRangeCalculator.check_int(identifier):
            if rule_type.value == RuleType.DATA_QUALITY.value:
                rule_res = self.get_dq_rule(identifier)
            elif rule_type.value == RuleType.RECONCILIATION.value:
                rule_res = self.get_reconciliation_rule(identifier)
            rule_id = rule_res.rule.id

        response = self._get(
            url=f'{self._catalog_api_base}/rules/{rule_type.value.lower()}/{rule_id}/executions', params=params
        )
        executions = list(response['executions'])
        rule_execution_list = []
        for res in executions:
            execution = res['execution']
            rule_execution_list.append(RuleExecutionSummary(**execution))
        return rule_execution_list

    def get_all_rules(self, filter: PolicyFilter, page=0, size=25, withLatestExecution=True,
                      sortBy='updatedAt:DESC') -> RuleResult:
        params = dict()
        params['page'] = page
        params['size'] = size
        params['withLatestExecution'] = withLatestExecution
        params['sortBy'] = sortBy
        if filter.policyType is not None:
            params['ruleType'] = filter.policyType.name
            if filter.policyType.name == RuleType.RECONCILIATION.name:
                params['ruleType'] = params['ruleType'] + ',EQUALITY'
        # TODO: More handling as new parameter has come
        if filter.lastExecutionResult is not None:
            params['resultStatus'] = filter.lastExecutionResult.name
        if filter.enable is not None:
            params['enabled'] = filter.enable
        if filter.active is not None and filter.active is True:
            params['ruleStatus'] = 'ACTIVE'
        else:
            params['ruleStatus'] = 'ALL'
        if filter.assets is not None:
            params['assetIds'] = ",".join([str(i.id) for i in filter.assets])
        if filter.data_sources is not None:
            params['assemblyIds'] = ",".join([str(i.id) for i in filter.data_sources])
        if filter.period is not None:
            finished_before_time, started_after_time = TimeRangeCalculator.calculate_time_range(filter)
            if started_after_time is not None:
                params['startedAfter'] = int(round(started_after_time.timestamp() * 1000))
            params['finishedBefore'] = int(round(finished_before_time.timestamp() * 1000))

        self.logger.info(params)
        response = self._get(
            url=f'{self._catalog_api_base}/rules',
            params=params
        )
        rules = list(response['rules'])
        rule_list = []
        for res in rules:
            rule = res['rule']
            # TODO Check why are we sending DataQualityRule here
            rule_list.append(Rule(**rule))
        return rule_list

    @staticmethod
    def now_ms():
        return int(round(time.time() * 1000))

    def _post(self, url, payload=None, as_json=True):
        now_ms = self.now_ms()
        if _HEADERS['accessKey'] is None:
            _HEADERS['accessKey'] = self.access_key
        if _HEADERS['secretKey'] is None:
            _HEADERS['secretKey'] = self.secret_key
        response = requests.post(
            url=url, headers=_HEADERS, json=payload, timeout=(self._torch_connection_timeout, self._torch_read_timeout),
            verify=False
        )
        self.logger.info(
            f" POST {url} "
            f"payload={json.dumps(payload)} "
            f"duration_ms={self.now_ms() - now_ms}"
        )

        return self._response(response, as_json)

    def _put(self, url, payload=None, as_json=True):
        now_ms = self.now_ms()
        if _HEADERS['accessKey'] is None:
            _HEADERS['accessKey'] = self.access_key
        if _HEADERS['secretKey'] is None:
            _HEADERS['secretKey'] = self.secret_key
        response = requests.put(
            url=url, headers=_HEADERS, json=payload, timeout=(self._torch_connection_timeout, self._torch_read_timeout),
            verify=False
        )
        self.logger.info(
            f" PUT {url} "
            f"payload={json.dumps(payload)} "
            f"duration_ms={self.now_ms() - now_ms}"
        )

        return self._response(response, as_json)

    def _get(self, url, params=None, as_json=True):
        now_ms = self.now_ms()
        if _HEADERS['accessKey'] is None:
            _HEADERS['accessKey'] = self.access_key
        if _HEADERS['secretKey'] is None:
            _HEADERS['secretKey'] = self.secret_key
        response = requests.get(
            url=url, params=params, headers=_HEADERS,
            timeout=(self._torch_connection_timeout, self._torch_read_timeout), verify=False
        )
        self.logger.info(
            f" GET {url} "
            f"duration_ms={self.now_ms() - now_ms}"
        )

        return self._response(response, as_json)

    def _post_form_data(self, url, payload=None, as_json=True):
        now_ms = self.now_ms()
        if _HEADERS['accessKey'] is None:
            _HEADERS['accessKey'] = self.access_key
        if _HEADERS['secretKey'] is None:
            _HEADERS['secretKey'] = self.secret_key

        params = {
            'request': json.dumps(payload)
        }
        data = MultipartEncoder(fields=params)
        _HEADERS['Content-Type'] = data.content_type
        response = requests.post(
            url=url, headers=_HEADERS, data=data, timeout=(self._torch_connection_timeout, self._torch_read_timeout),
            verify=False
        )
        self.logger.info(
            f" POST {url} "
            f"payload={json.dumps(payload)} "
            f"duration_ms={self.now_ms() - now_ms}"
        )

        return self._response(response, as_json)

    def _put_form_data(self, url, payload=None, as_json=True):
        now_ms = self.now_ms()
        if _HEADERS['accessKey'] is None:
            _HEADERS['accessKey'] = self.access_key
        if _HEADERS['secretKey'] is None:
            _HEADERS['secretKey'] = self.secret_key

        params = {
            'request': json.dumps(payload)
        }
        data = MultipartEncoder(fields=params)
        _HEADERS['Content-Type'] = data.content_type
        response = requests.put(
            url=url, headers=_HEADERS, data=data, timeout=(self._torch_connection_timeout, self._torch_read_timeout),
            verify=False
        )
        self.logger.info(
            f" POSPUTT {url} "
            f"payload={json.dumps(payload)} "
            f"duration_ms={self.now_ms() - now_ms}"
        )

        return self._response(response, as_json)

    def _delete(self, url, params=None, as_json=True):
        now_ms = self.now_ms()
        if _HEADERS['accessKey'] is None:
            _HEADERS['accessKey'] = self.access_key
        if _HEADERS['secretKey'] is None:
            _HEADERS['secretKey'] = self.secret_key
        response = requests.delete(
            url=url, params=params, headers=_HEADERS,
            timeout=(self._torch_connection_timeout, self._torch_read_timeout), verify=False
        )
        self.logger.info(
            f" DELETE {url} "
            f"duration_ms={self.now_ms() - now_ms}"
        )

        return response

    def _response(self, response, as_json):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.logger.error(f' {response.text}')
            self._raise_api_error(e, response.text)

        return response.json() if as_json else response.text

    def _raise_api_error(self, e, text):
        raise APIError(text) from e
