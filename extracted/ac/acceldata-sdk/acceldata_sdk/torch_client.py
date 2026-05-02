from acceldata_sdk.errors import TorchSdkException
from acceldata_sdk.models.pipeline import CreatePipeline, Pipeline, PipelineRun
from acceldata_sdk.torch_http_client import TorchHttpClient
from acceldata_sdk.constants import RuleExecutionStatus, FailureStrategy, PolicyType, AssetSourceType, \
    MIN_TORCH_BACKEND_VERSION_SUPPORTED, SdkSupportedVersions, TorchBuildVersion

from acceldata_sdk.models.rule import RuleResource
from acceldata_sdk.models.common_types import PolicyExecutionRequest
from typing import List, Optional
from acceldata_sdk.utils.parsing import str_to_bool
import logging
from acceldata_sdk.models.ruleExecutionResult import RuleResult, PolicyFilter, RuleType
from acceldata_sdk.constants import TORCH_CONNECTION_TIMEOUT_MS, TORCH_READ_TIMEOUT_MS
import warnings


class TorchClient:
    logger = logging.getLogger('torch')
    logger.setLevel(logging.INFO)

    """
            Description : Torch user client is used to send data to catalog server.
            :param url: (String) url of the catalog server
            :param timeout_ms: (int) Request timeout to ADOC server, in milliseconds.
            :param access_key: (String) Access key of API key. You can generate API key from torch UI's setting
            :param secret_key: (String) Secret key of API key.
            :param do_version_check: (bool) Enable/Disable version compatibility check between sdk and ADOC. By default version checks are disabled.
            Ex.  TorchClient = TorchUserClient(url='https://torch.acceldata.local:5443', access_key='OY2VVIN2N6LJ', secret_key='da6bDBimQfXSMsyyhlPVJJfk7Zc2gs')
    """

    def __init__(self, url, torch_connection_timeout_ms=TORCH_CONNECTION_TIMEOUT_MS, access_key: str = None,
                 secret_key: str = None, do_version_check: bool = False, torch_read_timeout_ms=TORCH_READ_TIMEOUT_MS):

        """
                Description : Torch user client is used to send data to catalog server.
                :param url: (String) url of the catalog server
                :param torch_connection_timeout_ms: (int) Maximum time (in milliseconds) to wait while establishing a connection to the ADOC server. Default: 5000 ms.
                :param access_key: (String) Access key of API key. You can generate API key from torch UI's setting
                :param secret_key: (String) Secret key of API key.
                :param do_version_check: (bool) Enable/Disable version compatibility check between sdk and torch.
                :param torch_read_timeout_ms: (int) Maximum time (in milliseconds) to wait for a response from the ADOC server after a successful connection. Default: 15000 ms.

                Ex.  TorchClient = TorchUserClient(url='https://torch.acceldata.local:5443', access_key='OY2VVIN2N6LJ', secret_key='da6bDBimQfXSMsyyhlPVJJfk7Zc2gs')
        """
        self.logger.debug(f'torch_connection_timeout_ms {torch_connection_timeout_ms}')
        self.logger.debug(f'torch_read_timeout {torch_read_timeout_ms}')
        if access_key is None and secret_key is None:
            raise Exception("ADOC credentials are missing. Please provide both access_key and secret_key.")
        self.client = TorchHttpClient(url=url, access_key=access_key, secret_key=secret_key,
                                      torch_connection_timeout_ms=torch_connection_timeout_ms,
                                      torch_read_timeout_ms=torch_read_timeout_ms)
        if do_version_check:
            warnings.warn(
                "`do_version_check` is deprecated and will be removed in a future release.",
                DeprecationWarning,
                stacklevel=2,
            )
        self.do_version_check = False

    def get_supported_sdk_versions(self) -> SdkSupportedVersions:
        """
        Description:
            To get supported sdk versions
        :return: (SdkSupportedVersions) SdkSupportedVersions class instance
        """
        return self.client.get_supported_sdk_versions()

    def get_torch_version(self) -> TorchBuildVersion:
        """
        Description:
            To get supported torch version
        :return: (TorchBuildVersion)
        """
        return self.client.get_torch_version()

    def create_pipeline(self, pipeline: CreatePipeline) -> Pipeline:
        """
        Description:
            To create pipeline in torch catalog service
        :param pipeline: (CreatePipeline) class instance of the pipeline to be created
        :return: (Pipeline) newly created pipeline class instance
        """
        if pipeline.uid is None or pipeline.name is None:
            raise Exception('To create a pipeline, pipeline uid/name is required')
        return self.client.create_pipeline(pipeline)

    def get_pipeline(self, pipeline_identity) -> Pipeline:
        """
        Description:
            To get an existing pipeline from torch catalog
        :param pipeline_identity: uid or id of the pipeline
        :return:(Pipeline) pipeline class instance
        """
        return self.client.get_pipeline(pipeline_identity)

    def get_pipelines(self):
        """
        Description:
            To get an all pipelines from torch catalog
        :return:(List[PipelineListingInfo]) pipeline class instance
        """
        return self.client.get_pipelines()

    def get_spans(self, pipeline_run_id):
        """
        Description:
            To get an all spans from torch catalog
        :param pipeline_run_id: run_id of the pipeline
        :return:(List[Span]) pipeline class instance
        """
        return self.client.get_spans(pipeline_run_id)

    def get_pipeline_run(self, pipeline_run_id: str = None, continuation_id: str = None, pipeline_id: str = None) -> PipelineRun:
        """
        Description:
            To get an existing pipeline from torch catalog
        :param pipeline_run_id: run id of the pipeline run
        :param continuation_id: continuation id of the pipeline run
        :param pipeline_id: id of the pipeline. This is a mandatory parameter when run is being queried using continuation_id

        :return:(PipelineRun) pipeline run class instance
        """
        return self.client.get_pipeline_run(pipeline_run_id=pipeline_run_id, continuation_id=continuation_id, pipeline_id=pipeline_id)

    def get_pipeline_runs(self, pipeline_id) -> List[PipelineRun]:
        """
        Description:
            To get an all pipeline runs for a pipeline id from torch catalog
        :param pipeline_id: id of the pipeline
        :return:(List[PipelineRun]) List of pipeline run class instance
        """
        return self.client.get_pipeline_runs(pipeline_id)

    def get_datasource(self, assembly_identifier, properties=False):
        """
        Description:
            Find datasource by it's name or id in torch catalog
        :param assembly_identifier: name or id of the datasource given in torch
        :param properties: optional parameter, bool, to get datasource properties as well
        :return: (DataSource) datasource
        """
        return self.client.get_datasource(assembly_identifier, properties)

    def get_datasource_by_id(self, id: int, properties: bool = False):
        """
        Description:
            Find datasource by its id in torch catalog
        :param id: id of the datasource given in torch
        :return: (DataSource) datasource
        """
        return self.client.get_datasource_by_id(id, properties)

    def get_datasources(self, type: AssetSourceType = None):
        """
        Description:
            Find datasources by its type in torch catalog
        :param type: type of the datasource given in torch, optional
        :return: list(DataSource) datasource
        """
        return self.client.get_datasources(type)

    def get_all_datasources(self):
        """
        Description:
            list all datasources in torch catalog
        :return: (DataSource) list of datasource
        """
        return self.client.get_all_datasources()

    def start_crawler(self, datasource_name: str):
        """
        Description:
            Start crawler for datasource
        :param datasource_name: name of the datasource given in torch
        :return: (CrawlerStatus) CrawlerStatus
        """
        return self.client.start_crawler(datasource_name)

    def get_crawler_status(self, datasource_name: str):
        """
        Description:
            Get crawler status for datasource
        :param datasource_name: name of the datasource given in torch
        :return: (CrawlerStatus) CrawlerStatus
        """
        return self.client.get_crawler_status(datasource_name)

    def get_asset_types(self):
        """
        Description:
            get all asset types supported in torch catalog
        :return: list of asset types
        """
        return self.client.get_all_asset_types()

    def get_profile_status(self, asset_id: int, req_id: int):
        """
        Description:
            get status of asset profile for given request id
        :return: profiling status
        """
        return self.client.get_profile_request_details(asset_id=asset_id, req_id=req_id)

    def get_all_source_types(self):
        """
        Description:
            get all source types supported in torch catalog
        :return: list of all source type
        """
        return self.client.get_all_source_types()

    def get_property_templates(self):
        pass

    def get_connection_types(self):
        """
        Description:
            get all connection types supported in torch catalog
        :return: list of all connection types
        """
        return self.client.get_connection_types()

    def get_tags(self):
        return self.client.get_tags()

    def get_analysis_pipeline(self, id: int):
        return self.client.get_analysis_pipeline(id)

    def get_asset(self, identifier):
        """"
            Description:
                Find an asset of the datasource
            :param identifier: uid or ID of the asset
        """
        return self.client.get_asset(identifier)

    def get_policy(self, type: PolicyType = None, identifier=None) -> RuleResource:
        """"
            Description:
                Find policy
            :param identifier: ID or name of the policy
            :param type: (Optional) type of the policy
        """
        if identifier is None:
            raise ValueError("Parameter 'identifier' is mandatory.")

        if type is None:
            return self.client.get_policy(identifier)

        if type.value == PolicyType.DATA_QUALITY.value:
            return self.client.get_dq_rule(identifier)
        elif type.value == PolicyType.RECONCILIATION.value:
            return self.client.get_reconciliation_rule(identifier)
        elif type.value == PolicyType.DATA_CADENCE.value:
            return self.client.get_freshness_rule(identifier)
        else:
            raise TorchSdkException('Invalid policy type passed.')


    def list_all_policies(self, filter: PolicyFilter, page=0, size=25, withLatestExecution=True, sortBy='updatedAt:DESC'):
        """
        Description:
            To list all policies based on filter
        :param filter: (Enum PolicyFilter) Type of policies to be executed.
        PolicyFilter can have the following parameters
        period: Time period for which list should be filtered. It is an enum ExecutionPeriod
        tags: tags on which list should be filtered
        lastExecutionResult: lastExecution result on which list should be filtered
        asset: Assets for which policies should be filtered. This list should be of objects of type Asset returned by get_asset
        data_source:  Datasource for which policies should be filtered. This list should be of objects of type Datasource
        returned by get_datasource
        policyType: Type of policy policies should be filtered. This is an enum of type RuleType
        enable: To filter only for enabled policies set enable to True
        active: : To filter only for active policies set active to True
        :param page: (Int) page number of query output
        :param size: (Int) Size of each page
        :param sortBy: (Str) sorting order
        """
        return self.client.get_all_rules(filter=filter, page=page, size=size, sortBy=sortBy,
                                         withLatestExecution=withLatestExecution)

    def create_connection(self, create_connection):
        return self.client.create_connection(create_connection)

    def check_connection(self, connection):
        return self.client.check_connection(connection)

    def execute_dq_rule(self, rule_id, incremental=False, pipeline_run_id=None,
                        policy_execution_request: PolicyExecutionRequest = None):
        self.logger.info(
            "Invoked execute_dq_rule of the torch_client\n"
            f"Incremental flag: {incremental}\n"
            f"Policy Execution Request: {policy_execution_request.to_dict() if policy_execution_request else 'None'}"
        )

        return self.client.execute_dq_rule(rule_id=rule_id, incremental=incremental, pipeline_run_id=pipeline_run_id,
                                           policy_execution_request=policy_execution_request)

    def execute_reconciliation_rule(self, rule_id, incremental=False,pipeline_run_id=None,
                                    policy_execution_request: PolicyExecutionRequest = None):
        self.logger.info(
            "Invoked execute_reconciliation_rule of the torch_client\n"
            f"Incremental flag: {incremental}\n"
            f"Policy Execution Request: {policy_execution_request.to_dict() if policy_execution_request else 'None'}"
        )

        return self.client.execute_reconciliation_rule(rule_id=rule_id, incremental=incremental, pipeline_run_id=pipeline_run_id,
                                                       policy_execution_request=policy_execution_request)

    def execute_freshness_rule(self, rule_id, incremental=False, pipeline_run_id=None,
                                    policy_execution_request: PolicyExecutionRequest = None):
        self.logger.info(
            "Invoked execute_freshness_rule of the torch_client\n"
            f"Incremental flag: {incremental}\n"
            f"Policy Execution Request: {policy_execution_request.to_dict() if policy_execution_request else 'None'}"
        )

        return self.client.execute_freshness_rule(rule_id=rule_id, incremental=incremental, pipeline_run_id=pipeline_run_id,
                                                       policy_execution_request=policy_execution_request)

    def get_dq_rule_execution_details(self, execution_id):
        return self.client.get_dq_rule_execution_details(execution_id)

    def get_reconciliation_rule_execution_details(self, execution_id):
        return self.client.get_reconciliation_rule_execution_details(execution_id)

    def cancel_rule_execution(self, execution_id):
        return self.client.cancel_rule_execution(execution_id)

    def enable_rule(self, rule_id):
        return self.client.enable_rule(rule_id)

    def disable_rule(self, rule_id):
        return self.client.disable_rule(rule_id)

    def get_reconciliation_rule_result(self, execution_id) -> RuleResult:
        return self.client.get_reconciliation_rule_result(execution_id)

    def get_dq_rule_result(self, execution_id) -> RuleResult:
        return self.client.get_dq_rule_result(execution_id)

    def get_freshness_rule_result(self, execution_id) -> RuleResult:
        return self.client.get_freshness_rule_result(execution_id)

    def execute_policy(self, policy_type: PolicyType, policy_id, sync=True, incremental=False,
                       failure_strategy: FailureStrategy = FailureStrategy.DoNotFail, pipeline_run_id=None,
                       policy_execution_request: PolicyExecutionRequest = None):
        """
        Description:
            To execute policies synchronously and asynchronously
        :param policy_type: (PolicyType) Type of rule to be executed
        :param policy_id: (String) id of the rule to be executed
        :param sync: (bool) optional Set it to False if asynchronous execution has to be done
        :param incremental: (bool) optional Set it to True if full execution has to be done
        :param failure_strategy: (enum) optional Set it to decide if it should fail at error,
            fail at warning or never fail
        :param pipeline_run_id: (long) optional Run id of the pipeline run where the policy is being executed. This can
            be used to link a policy execution id with a particular pipeline run id
        :param policy_execution_request: (PolicyExecutionRequest) An optional parameter that allows you to provide
        additional options for executing the policy. It is an instance of the PolicyExecutionRequest modules class,
        which contains various properties that can be used to customize the policy execution, such as `executionType`,
        `markerConfigs`, `ruleItemSelections`, and more.
        """
        self.logger.info(f"Policy Execution Request: {policy_execution_request.to_dict() if policy_execution_request else 'None'}")

        return self.client.execute_rule(policy_type, policy_id, sync, incremental, failure_strategy, pipeline_run_id,
                                        policy_execution_request)

    def get_policy_status(self, policy_type, execution_id) -> RuleExecutionStatus:
        """
        Description:
            To get status of rule execution
        :param policy_type: (PolicyType) Type of rule to be executed
        :param execution_id: (String) ID of execution of the rule previously executed.
        """
        return self.client.get_rule_status(policy_type, execution_id)

    def get_policy_execution_result(self, policy_type: PolicyType, execution_id,
                                    failure_strategy: FailureStrategy = FailureStrategy.DoNotFail):
        """
        Description:
            To get result of rule execution
        :param policy_type: (PolicyType) Type of rule to be executed
        :param execution_id: (String) ID of execution of the rule previously executed.
        :param failure_strategy: (enum) optional Set it to decide if it should fail at error,
            fail at warning or never fail
        """
        return self.client.get_rule_execution_result(policy_type, execution_id, failure_strategy)

    def policy_executions(self, identifier, policy_type: RuleType, page=0, size=25, sortBy='finishedAt:DESC'):
        """
        Description:
            To list rule executions
        :param identifier: id or name of executed rule
        :param policy_type: (Enum RuleType) Type of executed rule
        :param page: (Int) page number of query output
        :param size: (Int) Size of each page
        :param sortBy: (Str) sorting order
        """
        return self.client.policy_executions(identifier, policy_type, page, size, sortBy)
