# Copyright 2021 StreamSets Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Abstractions for interacting with ControlHub."""

# fmt: off
import copy
import json
import logging
import threading
import uuid
import warnings
from enum import Enum

import requests

from . import aster_api, sch_api, sdc_models
from .analytics import analytics_class_decorator
from .constants import (
    ENGINELESS_ENGINE_ID, EXECUTOR_TO_DEPLOYMENT_MAP, SDC_DEPLOYMENT_TYPE, SDC_EXECUTOR_TYPE, SNOWFLAKE_ENGINE_ID,
    SNOWFLAKE_EXECUTOR_TYPE, STATUS_ERRORS, TRANSFORMER_DEPLOYMENT_TYPE, TRANSFORMER_EXECUTOR_TYPE,
)
from .exceptions import EnginelessError, JobInactiveError, ValidationError
from .sch_models import (
    ActionAudits, AdminTool, Alert, ApiCredentialBuilder, ApiCredentials, AWSEnvironment, AzureEnvironment,
    AzureVMDeployment, ClassificationRuleBuilder, Configuration, Connection, ConnectionAudits, ConnectionBuilder,
    Connections, ConnectionTags, ConnectionVerificationResult, DataSlaBuilder, Deployment, DeploymentBuilder,
    DeploymentEngineConfigurations, Deployments, DraftRuns, EC2Deployment, Engine, Engines, EnvironmentBuilder,
    Environments, GCEDeployment, GCPEnvironment, GroupBuilder, Groups, Job, JobBuilder, Jobs, JobSequence,
    JobSequenceBuilder, JobSequences, KubernetesDeployment, KubernetesEnvironment, LegacyDeploymentBuilder,
    LegacyDeployments, LoginAudits, MeteringUsage, NotImplementedDeployment, NotImplementedEnvironment,
    OrganizationBuilder, Organizations, Pipeline, PipelineBuilder, PipelineLabels, Pipelines, ProtectionMethodBuilder,
    ProtectionPolicies, ProtectionPolicy, ProtectionPolicyBuilder, ProvisioningAgents, ReportDefinitions, SAQLSearch,
    SAQLSearchBuilder, SAQLSearches, ScheduledTask, ScheduledTaskActions, ScheduledTaskBuilder, ScheduledTasks,
    SelfManagedDeployment, SelfManagedEnvironment, StPipelineBuilder, SubscriptionAudit, SubscriptionBuilder,
    Subscriptions, Topologies, Topology, TopologyBuilder, UserBuilder, Users,
)
from .utils import (
    SDC_DEFAULT_EXECUTION_MODE, TRANSFORMER_EXECUTION_MODES, SeekableList, get_stage_library_display_name_from_library,
    get_stage_library_name_from_display_name, reversed_dict, validate_pipeline_stages, wait_for_condition,
)

# fmt: on

logger = logging.getLogger(__name__)

DEFAULT_ASTER_SERVER_URL = 'https://cloud.login.streamsets.com'
DEFAULT_DATA_COLLECTOR_STAGE_LIBS = ['basic', 'dataformats', 'dev']
DEFAULT_SYSTEM_SDC_ID = 'SYSTEM_SDC_ID'
DEFAULT_TRANSFORMER_STAGE_LIBS = ['basic', 'file']
# Defaults as defined by the UI: https://t.ly/b-Ay
DEFAULT_USER_ROLES = [
    'connection:user',
    'csp:deployment-manager',
    'csp:environment-manager',
    'datacollector:admin',
    'jobrunner:operator',
    'notification:user',
    'org-user',
    'pipelinestore:pipelineEditor',
    'provisioning:operator',
    'sla:editor',
    'timeseries:reader',
    'topology:editor',
    'user',
]
DEFAULT_WAIT_FOR_STATUS_TIMEOUT = 300
DEFAULT_WAIT_FOR_METRIC_TIMEOUT = 200


@analytics_class_decorator
class ControlHub:
    """Class to interact with StreamSets Control Hub.

    Args:
        credential_id (:obj:`str`): ControlHub credential ID.
        token (:obj:`str`): ControlHub token.
        use_websocket_tunneling (:obj:`bool`, optional): use websocket tunneling. Default: ``True``.

    Attributes:
        version (:obj:`str`): Version of ControlHub.
        ldap_enabled (:obj:`bool`): Indication if LDAP is enabled or not.
        organization_global_configuration (:obj:`:py:class:`streamsets.sdk.models.Configuration``): Organization's Global Configuration instance.
        pipeline_labels (:py:class:`streamsets.sdk.sch_models.PipelineLabels`): Pipeline Labels.
        users (:py:class:`streamsets.sdk.sch_models.Users`): Organization's Users.
        login_audits (:py:class:`streamsets.sdk.sch_models.LoginAudits`): ControlHub Login Audits.
        action_audits (:py:class:`streamsets.sdk.sch_models.ActionAudits`): ControlHub Action Audits.
        connection_audits (:py:class:`streamsets.sdk.sch_models.ConnectionAudits`): ControlHub Connection Audits.
        groups (:py:class:`streamsets.sdk.sch_models.Groups`): ControlHub Groups.
        data_collectors (Returns a :py:class:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.DataCollector` instances.): Data Collector instances registered under ControlHub.
        transformers (Returns a :py:class:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Transformer` instances.): Transformer instances registered under ControlHub.
        provisioning_agents (:py:class:`streamsets.sdk.sch_models.ProvisioningAgents): Provisioning Agents registered to the ControlHub instance.
        legacy_deployments (:py:class:`streamsets.sdk.sch_models.LegacyDeployments`): LegacyDeployments instances.
        organizations (:py:class:`streamsets.sdk.sch_models.Organizations`): All the organizations that the current user belongs to.
        api_credentials (A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.ApiCredential`): ControlHub Api Credentials.
        pipelines (:py:class:`streamsets.sdk.sch_models.Pipelines`): ControlHub Pipelines.
        draft_runs (:py:class:`streamsets.sdk.sch_models.DraftRuns`): ControlHub Draft Runs.
        jobs (:py:class:`streamsets.sdk.sch_models.Jobs`): ControlHub Jobs.
        data_protector_enabled (::obj:`bool`): Whether Data Protector is enabled for the current organization.
        connection_tags (:py:class:`streamsets.sdk.sch_models.ConnectionTags`): ControlHub Connection Tags.
        alerts (A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Alert`): ControlHub Alerts.
        protection_policies (:py:class:`streamsets.sdk.sch_models.ProtectionPolicies`): ControlHub Protection Policies.
        scheduled_tasks (:py:class:`streamsets.sdk.sch_models.ScheduledTasks`): ControlHub Scheduled Tasks.
        subscriptions (:py:class:`streamsets.sdk.sch_models.Subscriptions`): ControlHub Subscriptions.
        subscription_audits ( A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.SubscriptionAudit`): ControlHub Subscription audits.
        topologies (:py:class:`streamsets.sdk.sch_models.Topologies`): ControlHub Topologies.
        connections (:py:class:`streamsets.sdk.sch_models.Connections`): ControlHub Connections.
        environments (:py:class:`streamsets.sdk.sch_models.Environments`): ControlHub Environments.
        engine_versions (:py:class:`streamsets.sdk.sch_models.DeploymentEngineConfiguration`): ControlHub Deployment Engine Configuration.
        deployments (:py:class:`streamsets.sdk.sch_models.Deployments`): ControlHub Deployments.
        engines (:py:class:`streamsets.sdk.sch_models.Engines`): ControlHub Engines.
        saql_saved_searches_pipeline (:py:class:`streamsets.sdk.sch_models.SAQLSearches`): ControlHub SAQL Searches for type Pipeline.
        saql_saved_searches_fragment (:py:class:`streamsets.sdk.sch_models.SAQLSearches`): ControlHub SAQL Searches for type Fragment.
        saql_saved_searches_job_instance (:py:class:`streamsets.sdk.sch_models.SAQLSearches`): ControlHub SAQL Searches for type Job Instance.
        saql_saved_searches_job_template (:py:class:`streamsets.sdk.sch_models.SAQLSearches`): ControlHub SAQL Searches for type Job Template.
        saql_saved_searches_draft_run (:py:class:`streamsets.sdk.sch_models.SAQLSearches`): ControlHub SAQL Searches for type Draft Run.
    """

    VERIFY_SSL_CERTIFICATES = True

    def __init__(self, credential_id, token, use_websocket_tunneling=True, **kwargs):
        self.credential_id = credential_id
        self.token = token
        self.use_websocket_tunneling = use_websocket_tunneling
        self._aster_url = kwargs.get('aster_url')
        self._landing_url = kwargs.get('landing_url')

        if self.use_websocket_tunneling:
            logger.info('Using WebSocket tunneling ...')

        self.session_attributes = {'verify': self.VERIFY_SSL_CERTIFICATES}
        self.api_client = sch_api.ApiClient(
            component_id=self.credential_id,
            auth_token=self.token,
            session_attributes=self.session_attributes,
            aster_url=self._aster_url,
            landing_url=self._landing_url,
        )
        self.server_url = self.api_client.base_url

        self.organization = self.api_client.get_current_user().response.json()['organizationId']

        self._roles = {user_role['id']: user_role['label'] for user_role in self.api_client.get_all_user_roles()}
        # Manually updating labels that have changed - reference security_data_service.spec.ts
        self._roles.update(
            {
                'datacollector:admin': 'Engine Administrator',
                'datacollector:creator': 'Engine Creator',
                'datacollector:guest': 'Engine Guest',
                'datacollector:manager': 'Engine Manager',
                'timeseries:reader': 'Metrics Reader',
            }
        )

        self._data_protector_version = None

        # We keep the Swagger API definitions as attributes for later use by various
        # builders.
        self._banner_api = self.api_client.get_banner_api()
        self._connection_api = self.api_client.get_connection_api()
        self._job_api = self.api_client.get_job_api()
        self._pipelinestore_api = self.api_client.get_pipelinestore_api()
        self._provisioning_api = self.api_client.get_provisioning_api()
        self._security_api = self.api_client.get_security_api()
        self._sequencing_api = self.api_client.get_sequencing_api()
        self._topology_api = self.api_client.get_topology_api()
        self._scheduler_api = self.api_client.get_scheduler_api()
        self._notification_api = self.api_client.get_notification_api()
        self._sla_api = self.api_client.get_sla_api()

        self._en_translations = self.api_client.get_translations_json()

        self._data_collectors = {}
        self._transformers = {}
        thread = threading.Thread(target=self._call_data_collectors)
        thread.start()

    def _call_data_collectors(self):
        self.data_collectors
        self.transformers

    def _get_aster_api_client(self):
        # Allows us to retrieve an ApiClient from aster_api ad-hoc without having to instantiate one when we initialize
        # a ControlHub object.
        aster_api_client = aster_api.ApiClient(
            server_url=self._aster_url or DEFAULT_ASTER_SERVER_URL,
            sch_auth_token=self.token,
            sch_credential_id=self.credential_id,
            session_attributes=self.session_attributes,
        )
        aster_api_client.login()
        return aster_api_client

    @property
    def version(self):
        # The version of the ControlHub server, determined
        # by making a URL call to the server
        server_info = self.api_client.get_server_info()
        return server_info.response.json()['version']

    @property
    def ldap_enabled(self):
        """Indication if LDAP is enabled or not.

        Returns:
            An instance of :obj:`boolean`.
        """
        return self.api_client.is_ldap_enabled().response.json()

    @property
    def organization_global_configuration(self):
        organization_global_configuration = self.api_client.get_organization_global_configurations().response.json()

        # Some of the config names are a bit long, so shorten them slightly...
        ID_TO_REMAP = {
            'Timestamp of the contract expiration': 'Timestamp of the contract expiration.'
            ' Only applicable to enterprise accounts',
            'Timestamp of the trial expiration': 'Timestamp of the trial expiration.'
            ' Only applicable to trial accounts',
        }
        return Configuration(
            configuration=organization_global_configuration,
            update_callable=self.api_client.update_organization_global_configurations,
            id_to_remap=ID_TO_REMAP,
        )

    @organization_global_configuration.setter
    def organization_global_configuration(self, value):
        self.api_client.update_organization_global_configurations(value._data)

    def _default_engine_version_id(self):
        command = self.api_client.get_all_engine_versions(
            offset=0,
            len=1,
            order_by="ENGINE_VERSION",
            order="DESC",
            engine_type="DC",
            designer=True,
            releases_only=True,
        )
        payload = command.response.json()
        return payload["data"][0]["id"]

    def get_pipeline_builder(self, engine_type=None, engine_id=None, fragment=False, **kwargs):
        """Get a pipeline builder instance with which a pipeline can be created.

        Args:
            engine_type (:obj:`str`): The type of pipeline that will be created. The options are ``'data_collector'``,
                                      ``'snowflake'`` or ``'transformer'``.
            engine_id (:obj:`str`): The ID of the Data Collector or Transformer in which to author the pipeline if not
                                    using Transformer for Snowflake.
            fragment (:obj:`boolean`, optional): Specify if a fragment builder. Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.PipelineBuilder` or
            :py:class:`streamsets.sdk.sch_models.StPipelineBuilder`.
        """

        deployment_types_with_engine_id = {'data_collector': 'COLLECTOR', 'transformer': 'TRANSFORMER'}
        engineless_design = False
        if not engine_type and not engine_id:
            engineless_design = True
            authoring_engine = None
        elif engine_type in deployment_types_with_engine_id:
            if not engine_id:
                raise ValueError("Pipelines of type 'data_collector' or 'transformer' require an engine id.")
            authoring_engine = self.engines.get(engine_type=deployment_types_with_engine_id[engine_type], id=engine_id)
        elif engine_type == 'snowflake':
            if engine_id:
                raise ValueError("Pipelines of type 'snowflake' do not use an engine id.")
            authoring_engine = None
        else:
            raise TypeError('unrecognised engine type: {!r} (ID={})'.format(engine_type, engine_id))

        pipeline = {property: None for property in self._pipelinestore_api['definitions']['PipelineJson']['properties']}

        if authoring_engine is not None:  # i.e. `data_collector` or `transformer`
            data_collector_instance = authoring_engine._instance
            if fragment:
                create_fragment_response = data_collector_instance.api_client.create_fragment(
                    'Pipeline Builder', draft=True
                ).response.json()
                pipeline_definition = json.dumps(create_fragment_response['pipelineFragmentConfig'])
                library_definitions = (
                    json.dumps(create_fragment_response['libraryDefinitions'])
                    if create_fragment_response['libraryDefinitions']
                    else None
                )
                commit_pipeline_json = {
                    'name': 'Pipeline Builder',
                    'sdcId': authoring_engine.id,
                    'fragment': True,
                    'pipelineDefinition': pipeline_definition,
                    'rulesDefinition': json.dumps(create_fragment_response['pipelineRules']),
                    'libraryDefinitions': library_definitions,
                }
                commit_pipeline_response = self.api_client.commit_pipeline(
                    new_pipeline=True, import_pipeline=False, body=commit_pipeline_json, fragment=fragment
                ).response.json()

                commit_id = commit_pipeline_response['commitId']
                pipeline_id = commit_pipeline_response['pipelineId']

                pipeline_commit = self.api_client.get_pipeline_commit(commit_id).response.json()
                pipeline_json = dict(
                    pipelineFragmentConfig=json.loads(pipeline_commit['pipelineDefinition']),
                    pipelineRules=json.loads(pipeline_commit['currentRules']['rulesDefinition']),
                    libraryDefinitions=pipeline_commit['libraryDefinitions'],
                )
                data_collector_instance._pipeline = pipeline_json
                self.api_client.delete_pipeline(pipeline_id)
            pipeline['sdcId'] = authoring_engine.id
            pipeline['sdcVersion'] = authoring_engine.version
            pipeline['executorType'] = (
                SDC_EXECUTOR_TYPE if engine_type == "data_collector" else TRANSFORMER_EXECUTOR_TYPE
            )
            executor_pipeline_builder = data_collector_instance.get_pipeline_builder(fragment=fragment)

        elif engine_type == 'snowflake':
            # A :py:class:`streamsets.sdk.sdc_models.PipelineBuilder` instance takes an empty pipeline and a
            # dictionary of definitions as arguments. To get the former, we generate a pipeline, export it,
            # and then delete it. For the latter, we simply pass along `aux_definitions`.
            commit_pipeline_json = {
                'name': 'Pipeline Builder',
                'sdcId': SNOWFLAKE_ENGINE_ID,
                'executorType': SNOWFLAKE_EXECUTOR_TYPE,
                'fragment': fragment,
                'failIfExists': True,
            }
            create_pipeline_response = self.api_client.commit_pipeline(
                new_pipeline=True,
                import_pipeline=False,
                execution_mode=SNOWFLAKE_EXECUTOR_TYPE,
                pipeline_type='SNOWPARK_PIPELINE',
                body=commit_pipeline_json,
                fragment=fragment,
            ).response.json()
            pipeline_id = create_pipeline_response['pipelineId']
            aux_definitions = self.api_client.get_pipelines_definitions(SNOWFLAKE_EXECUTOR_TYPE).response.json()

            pipeline_config = json.loads(create_pipeline_response['pipelineDefinition'])

            # pipeline cleanup to avoid showing errors
            pipeline_config['issues']['pipelineIssues'] = []
            pipeline_config['issues']['issueCount'] = 0
            pipeline_config['valid'] = True
            pipeline_config['previewable'] = True

            aux_pipeline = {
                'pipelineConfig': pipeline_config,
                'pipelineRules': json.loads(create_pipeline_response['currentRules']['rulesDefinition']),
                'libraryDefinitions': aux_definitions,
            }
            self.api_client.delete_pipeline(pipeline_id)
            executor_pipeline_builder = sdc_models.PipelineBuilder(
                pipeline=aux_pipeline, definitions=aux_definitions, fragment=fragment
            )
            pipeline['sdcVersion'] = create_pipeline_response['sdcVersion']
            pipeline['sdcId'] = create_pipeline_response['sdcId']
            pipeline['executorType'] = create_pipeline_response['executorType']

        elif engineless_design:
            engine_version_id = kwargs.get('engine_version_id', self._default_engine_version_id())
            empty_pipeline = self.api_client.create_designer_pipeline(engine_version_id).response.json()
            engine_definitions = self.api_client.get_designer_engine_definition(engine_version_id).response.json()
            executor_pipeline_builder = sdc_models.PipelineBuilder(
                pipeline=empty_pipeline, definitions=engine_definitions, fragment=False
            )
            pipeline['sdcId'] = "SYSTEM_DESIGNER"

        else:
            # this branch is to stop complaints about possibly undefined variables
            raise RuntimeError(
                'Should not have reached this point. '
                'Please try upgrading the SDK and contact streamsets for support if this error persists.'
            )

        if engine_type == 'transformer':
            return StPipelineBuilder(
                pipeline=pipeline,
                transformer_pipeline_builder=executor_pipeline_builder,
                control_hub=self,
                fragment=fragment,
                engine_start_up_time=authoring_engine._data["startUpTime"],
            )

        return PipelineBuilder(
            pipeline=pipeline,
            data_collector_pipeline_builder=executor_pipeline_builder,
            control_hub=self,
            fragment=fragment,
            engine_start_up_time=authoring_engine._data["startUpTime"] if authoring_engine else 0,
        )

    def publish_pipeline(self, pipeline, commit_message='New pipeline', draft=False, validate=False):
        """Publish a pipeline.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            commit_message (:obj:`str`, optional): Default: ``'New pipeline'``.
            draft (:obj:`boolean`, optional): Default: ``False``.
            validate (:obj:`boolean`, optional): Default: ``False``.
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        # Get the updated stage data and update it in the pipelineDefinition json string.
        pipeline_definition = pipeline._pipeline_definition
        validate_pipeline_stages(pipeline)
        pipeline_stages = pipeline.stages
        pipeline_definition['stages'] = []
        for stage in pipeline_stages:
            pipeline_definition['stages'].append(stage._data)
        pipeline._pipeline_definition = pipeline_definition
        pipeline._data['pipelineDefinition'] = pipeline_definition
        execution_mode = pipeline.configuration.get('executionMode', SDC_DEFAULT_EXECUTION_MODE)

        if execution_mode != SNOWFLAKE_EXECUTOR_TYPE:
            # A :py:class:`streamsets.sdk.sch_models.Pipeline` instance with no commit ID hasn't been
            # published to ControlHub before, so we do so first.
            if not pipeline.commit_id:
                commit_pipeline_json = {'name': pipeline._pipeline_definition['title'], 'sdcId': pipeline.sdc_id}
                if pipeline.sdc_id != DEFAULT_SYSTEM_SDC_ID:
                    commit_pipeline_json.update(
                        {
                            'pipelineDefinition': json.dumps(pipeline._pipeline_definition),
                            'rulesDefinition': json.dumps(pipeline._rules_definition),
                        }
                    )
                # fragmentCommitIds property is not returned by :py:meth:`streamsets.sdk.sch_api.ApiClient.commit_pipeline
                # and hence have to store it and add it to pipeline data before publishing the pipeline.
                fragment_commit_ids = pipeline._data.get('fragmentCommitIds')

                if execution_mode in TRANSFORMER_EXECUTION_MODES:
                    commit_pipeline_json.update({'executorType': 'TRANSFORMER'})
                pipeline._data = self.api_client.commit_pipeline(
                    new_pipeline=True,
                    import_pipeline=False,
                    fragment=pipeline.fragment,
                    execution_mode=execution_mode,
                    body=commit_pipeline_json,
                ).response.json()
                if pipeline.sdc_id == ENGINELESS_ENGINE_ID:
                    raise EnginelessError(
                        'The SDK does not support publishing engineless pipelines. Please visit the UI to get '
                        'instructions on how to install a deployment and engine, to proceed further.'
                    )

                # The pipeline description is overwritten when it is committed, so we account for it here.
                pipeline._data['description'] = pipeline._pipeline_definition['description']
                if fragment_commit_ids and not pipeline.fragment:
                    pipeline._data['fragmentCommitIds'] = fragment_commit_ids
            # If the pipeline does have a commit ID and is not a draft, we want to create a new draft and update the
            # existing one in the pipeline store instead of creating a new one.
            elif not getattr(pipeline, 'draft', False):
                pipeline._data = self.api_client.create_pipeline_draft(
                    commit_id=pipeline.commit_id,
                    authoring_sdc_id=pipeline.sdc_id,
                    authoring_sdc_version=pipeline.sdc_version,
                ).response.json()
                # The pipeline name & description is overwritten when drafts are created, so we account for it here.
                pipeline.name = pipeline._pipeline_definition['title']
                pipeline._data['description'] = pipeline._pipeline_definition['description']
            pipeline.commit_message = commit_message
            pipeline.current_rules['rulesDefinition'] = json.dumps(pipeline._rules_definition)
            pipeline._pipeline_definition['metadata'].update(
                {
                    'dpm.pipeline.rules.id': pipeline.current_rules['id'],
                    'dpm.pipeline.id': pipeline.pipeline_id,
                    'dpm.pipeline.version': pipeline.version,
                    'dpm.pipeline.commit.id': pipeline.commit_id,
                }
            )
            pipeline._data['pipelineDefinition'] = json.dumps(pipeline._pipeline_definition)

        # Translated js code from https://git.io/fj1kr.
        # Call sdc api to import pipeline and libraryDefinitions.
        pipeline_definition = (
            pipeline._data['pipelineDefinition']
            if isinstance(pipeline._data['pipelineDefinition'], dict)
            else json.loads(pipeline._data['pipelineDefinition'])
        )
        entity_id = 'fragmentId' if 'fragmentId' in pipeline_definition else 'pipelineId'
        sdc_pipeline_id = pipeline_definition[entity_id]

        if execution_mode == SNOWFLAKE_EXECUTOR_TYPE:
            if pipeline.commit_id and not getattr(pipeline, 'draft', False):
                pipeline._data = self.api_client.create_pipeline_draft(
                    commit_id=pipeline.commit_id,
                    authoring_sdc_id=pipeline.sdc_id,
                    authoring_sdc_version=pipeline.sdc_version,
                ).response.json()
                # The pipeline name & description is overwritten when drafts are created, so we account for it here.
                pipeline.name = pipeline._pipeline_definition['title']
                pipeline._data['description'] = pipeline._pipeline_definition['description']
                pipeline.commit_id = pipeline._data['commitId']

            pipeline.execution_mode = execution_mode
            library_definitions = self.api_client.get_pipelines_definitions(SNOWFLAKE_EXECUTOR_TYPE).response.text
            pipeline_envelope = {
                'pipelineDefinition': json.dumps(pipeline._pipeline_definition),
                'rulesDefinition': json.dumps(pipeline._rules_definition),
                'executorType': execution_mode,
                'failIfExists': False,
                'commitMessage': commit_message,
                'name': pipeline._pipeline_definition['title'],
                'libraryDefinitions': library_definitions,
            }
            config_key = 'pipelineDefinition'
            if not pipeline.commit_id:
                # fragmentCommitIds property is not returned by :py:meth:`streamsets.sdk.sch_api.ApiClient.commit_pipeline
                # and hence have to store it and add it to pipeline data before publishing the pipeline.
                fragment_commit_ids = pipeline._data.get('fragmentCommitIds')

                response_envelope = self.api_client.commit_pipeline(
                    new_pipeline=True,
                    import_pipeline=False,
                    fragment=pipeline.fragment,
                    execution_mode=execution_mode,
                    body=pipeline_envelope,
                ).response.json()
                if fragment_commit_ids and not pipeline.fragment:
                    pipeline._data['fragmentCommitIds'] = fragment_commit_ids
                pipeline.commit_id = response_envelope['commitId']
            else:
                response_envelope = pipeline_envelope
            response_envelope[config_key] = json.loads(response_envelope[config_key])
        else:
            config_key = 'pipelineFragmentConfig' if pipeline.fragment else 'pipelineConfig'
            pipeline_envelope = {config_key: pipeline._pipeline_definition, 'pipelineRules': pipeline._rules_definition}

            # Import the pipeline
            try:
                engine_api_client = self.engines.get(id=pipeline.sdc_id)._instance.api_client
                if pipeline.fragment:
                    response_envelope = engine_api_client.import_fragment(
                        fragment_id=sdc_pipeline_id,
                        fragment_json=pipeline_envelope,
                        include_library_definitions=True,
                        draft=True,
                    )
                else:
                    response_envelope = engine_api_client.import_pipeline(
                        pipeline_id=sdc_pipeline_id,
                        pipeline_json=pipeline_envelope,
                        overwrite=True,
                        include_library_definitions=True,
                        auto_generate_pipeline_id=True,
                        draft=True,
                    )
            except ValueError as ex:
                raise Exception(
                    'The authoring engine for this pipeline does not exist in Control Hub. Please update '
                    'the authoring engine via pipeline.sdc_id'
                ) from ex

        response_envelope[config_key]['pipelineId'] = sdc_pipeline_id
        if execution_mode in TRANSFORMER_EXECUTION_MODES:
            response_envelope[config_key].update({'executorType': 'TRANSFORMER'})
        pipeline._data['pipelineDefinition'] = json.dumps(response_envelope[config_key])
        if response_envelope['libraryDefinitions']:
            if type(response_envelope['libraryDefinitions']) is not str:
                pipeline._data['libraryDefinitions'] = json.dumps(response_envelope['libraryDefinitions'])
            else:
                pipeline._data['libraryDefinitions'] = response_envelope['libraryDefinitions']
        else:
            pipeline._data['libraryDefinitions'] = None
        if execution_mode == SNOWFLAKE_EXECUTOR_TYPE:
            if 'currentRules' in response_envelope:
                pipeline._data['currentRules'] = dict(
                    rulesDefinition=response_envelope['currentRules']['rulesDefinition']
                )
            elif 'rulesDefinition' in response_envelope:
                pipeline._data['currentRules'] = dict(rulesDefinition=response_envelope['rulesDefinition'])
        else:
            pipeline._data['currentRules']['rulesDefinition'] = json.dumps(response_envelope['pipelineRules'])
        save_pipeline_commit_command = self.api_client.save_pipeline_commit(
            commit_id=pipeline.commit_id, validate=validate, include_library_definitions=True, body=pipeline._data
        )
        if not draft:
            publish_pipeline_commit_command = self.api_client.publish_pipeline_commit(
                commit_id=pipeline.commit_id, commit_message=commit_message
            )
        # Due to DPM-4470, we need to do one more REST API call to get the correct pipeline data.
        pipeline_commit = self.api_client.get_pipeline_commit(commit_id=pipeline.commit_id).response.json()

        pipeline._data = pipeline_commit
        if pipeline._builder is not None:
            pipeline._builder._sch_pipeline = pipeline_commit
        return save_pipeline_commit_command if draft else publish_pipeline_commit_command

    def delete_pipeline(self, pipeline, only_selected_version=False):
        """Delete a pipeline.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            only_selected_version (:obj:`boolean`): Delete only current commit.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if only_selected_version:
            return self.api_client.delete_pipeline_commit(pipeline.commit_id)
        return self.api_client.delete_pipeline(pipeline.pipeline_id)

    def duplicate_pipeline(self, pipeline, name=None, description='New Pipeline', number_of_copies=1):
        """Duplicate an existing pipeline.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            name (:obj:`str`, optional): Name of the new pipeline(s). Default: ``None``.
            description (:obj:`str`, optional): Description for new pipeline(s). Default: ``'New Pipeline'``.
            number_of_copies (:obj:`int`, optional): Number of copies. Default: ``1``.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Pipeline`.
        """
        if name is None:
            name = '{} copy'.format(pipeline.name)
        # Add a unique name prefix to identify duplicated pipelines
        dummy_name_prefix = '{}:{}'.format(name, str(uuid.uuid4()))

        duplicated_pipelines = SeekableList()

        duplicate_pipeline_properties = self._pipelinestore_api['definitions']['DuplicatePipelineJson']['properties']
        duplicate_body = {property_: None for property_ in duplicate_pipeline_properties}
        duplicate_body.update(
            {'namePrefix': dummy_name_prefix, 'description': description, 'numberOfCopies': number_of_copies}
        )
        self.api_client.duplicate_pipeline(pipeline.commit_id, duplicate_body)

        if number_of_copies == 1:
            dummy_names = [dummy_name_prefix]
        else:
            dummy_names = ['{}{}'.format(dummy_name_prefix, i) for i in range(1, number_of_copies + 1)]
        # Update dummy names with actual names
        for i, dummy_name in enumerate(dummy_names):
            duplicated_pipeline = self.pipelines.get(only_published=False, name=dummy_name)
            if number_of_copies == 1:
                duplicated_pipeline.name = name
            else:
                duplicated_pipeline.name = '{}{}'.format(name, i + 1)
            self.api_client.save_pipeline_commit(
                commit_id=duplicated_pipeline.commit_id,
                include_library_definitions=True,
                body=duplicated_pipeline._data,
            )
            duplicated_pipelines.append(duplicated_pipeline)
        return duplicated_pipelines

    def update_pipelines_with_different_fragment_version(self, pipelines, from_fragment_version, to_fragment_version):
        """Update pipelines with latest pipeline fragment commit version.

        Args:
            pipelines (:obj:`list`): List of :py:class:`streamsets.sdk.sch_models.Pipeline` instances.
            from_fragment_version (:py:obj:`streamsets.sdk.sch_models.PipelineCommit`): commit of fragment from which
                                                                                        the pipeline needs to be
                                                                                        updated.
            to_fragment_version (:py:obj:`streamsets.sdk.sch_models.PipelineCommit`): commit of fragment to which
                                                                                      the pipeline needs to be updated.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        pipeline_commit_ids = [pipeline.commit_id for pipeline in pipelines]
        return self.api_client.update_pipelines_with_fragment_commit_version(
            pipeline_commit_ids, from_fragment_version.commit_id, to_fragment_version.commit_id
        )

    @property
    def pipeline_labels(self):
        """Pipeline labels.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.PipelineLabels`.
        """
        return PipelineLabels(self, organization=self.organization)

    def delete_pipeline_labels(self, *pipeline_labels):
        """Delete pipeline labels.

        Args:
            *pipeline_labels: One or more instances of :py:class:`streamsets.sdk.sch_models.PipelineLabel`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        pipeline_label_ids = [pipeline_label.id for pipeline_label in pipeline_labels]
        logger.info('Deleting pipeline labels %s ...', pipeline_label_ids)
        delete_pipeline_label_command = self.api_client.delete_pipeline_labels(body=pipeline_label_ids)
        return delete_pipeline_label_command

    def duplicate_job(self, job, name=None, description=None, number_of_copies=1):
        """Duplicate an existing job.

        Args:
            job (:py:obj:`streamsets.sdk.sch_models.Job`): Job object.
            name (:obj:`str`, optional): Name of the new job(s). Default: ``None``. If not specified, name of the job
                                         with ``' copy'`` appended to the end will be used.
            description (:obj:`str`, optional): Description for new job(s). Default: ``None``.
            number_of_copies (:obj:`int`, optional): Number of copies. Default: ``1``.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        if name is None:
            name = '{} copy'.format(job.job_name)

        # Add a unique name prefix to prevent accidentally retrieving a job of the same name
        dummy_name_prefix = '{}:{}'.format(name, str(uuid.uuid4()))

        duplicated_jobs = SeekableList()
        duplicate_job_properties = self._job_api['definitions']['DuplicateJobJson']['properties']
        duplicate_body = {property_: None for property_ in duplicate_job_properties}
        duplicate_body.update(
            {'namePrefix': dummy_name_prefix, 'description': description, 'numberOfCopies': number_of_copies}
        )
        self.api_client.duplicate_job(job_id=job.job_id, body=duplicate_body)

        for i in range(number_of_copies):
            job_name = '{}{}'.format(dummy_name_prefix, i + 1 if number_of_copies > 1 else '')
            # Retrieve the unique job
            duplicated_job = self.jobs.get(job_name=job_name, job_template=job.job_template)
            # Update the job with the appropriate name
            duplicated_job.job_name = '{}{}'.format(name, i + 1 if number_of_copies > 1 else '')
            self.update_job(duplicated_job)
            duplicated_jobs.append(duplicated_job)
        return duplicated_jobs

    def get_user_builder(self):
        """Get a user builder instance with which a user can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.UserBuilder`.
        """
        user = {}
        # Update the UserJson with the API definitions from Swagger.
        user_properties = self._security_api['definitions']['UserJson']['properties']
        user.update({property_: None for property_ in user_properties})

        # Set other properties based on defaults from the web UI.
        user_defaults = {
            'active': True,
            'groups': ['all@{}'.format(self.organization)],
            'organization': self.organization,
            'passwordGenerated': False,
            'roles': DEFAULT_USER_ROLES,
            'userDeleted': False,
        }
        user.update(user_defaults)

        return UserBuilder(user=user, roles=self._roles, control_hub=self)

    def invite_user(self, user):
        """Invite a user to the StreamSets Platform.

        Args:
            user (:py:class:`streamsets.sdk.sch_models.User`): User object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding a user %s ...', user.email_address)
        # First, invite the user via ASTER
        aster_api_client = self._get_aster_api_client()
        # User is an either an administrator for their organization ('ADMINISTRATOR') or a regular user ('OPERATOR').
        # The user's roles store either 'org-admin' or 'org-user' accordingly.
        user_data = {'email': user.email_address, 'role': 'ADMINISTRATOR' if 'org-admin' in user.roles else 'OPERATOR'}
        aster_user = aster_api_client.invite_org_users(body=user_data).response.json()
        # Second, retrieve the user entry from Platform and update the roles/groups selected during UserBuilder.build()
        sch_user_id = '{}@{}'.format(aster_user['data']['schUser'], self.organization)
        sch_user_json = self.api_client.get_user(org_id=self.organization, user_id=sch_user_id).response.json()
        sch_user_json.update({'roles': user._data['roles'], 'groups': user._data['groups']})
        update_user_command = self.api_client.update_user(
            org_id=self.organization, user_id=sch_user_id, body=sch_user_json
        )
        user._data = update_user_command.response.json()
        return update_user_command

    def update_user(self, user):
        """Update a user. Some user attributes are updated by ControlHub such as
            last_modified_by,
            last_modified_on.

        Args:
            user (:py:class:`streamsets.sdk.sch_models.User`): User object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating a user %s ...', user)
        update_user_command = self.api_client.update_user(body=user._data, org_id=self.organization, user_id=user.id)
        user._data = update_user_command.response.json()
        return update_user_command

    def activate_user(self, *users):
        """Activate users for all given User IDs.

        Args:
            *users: One or more instance of :py:class:`streamsets.sdk.sch_models.User`.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        user_ids = [user.id.split('@')[0] for user in users]
        logger.info('Activating user(s) %s ...', user_ids)
        aster_api_client = self._get_aster_api_client()
        aster_user_ids = [
            aster_api_client.get_org_users(search='schUser=={}'.format(user_id)).response.json()['data']['content'][0][
                'id'
            ]
            for user_id in user_ids
        ]
        return aster_api_client.activate_org_users(aster_user_ids)

    def deactivate_user(self, *users):
        """Deactivate Users for all given User IDs.

        Args:
            *users: One or more instances of :py:class:`streamsets.sdk.sch_models.User`.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        user_ids = [user.id.split('@')[0] for user in users]
        logger.info('Deactivating user(s) %s ...', user_ids)
        aster_api_client = self._get_aster_api_client()
        aster_user_ids = [
            aster_api_client.get_org_users(search='schUser=={}'.format(user_id)).response.json()['data']['content'][0][
                'id'
            ]
            for user_id in user_ids
        ]
        return aster_api_client.deactivate_org_users(body=aster_user_ids)

    def delete_user(self, *users, deactivate=False):
        """Delete users. Deactivate users before deleting if configured.

        Args:
            *users: One or more instances of :py:class:`streamsets.sdk.sch_models.User`.
            deactivate (:obj:`bool`, optional): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        if deactivate:
            self.deactivate_user(*users)

        user_ids = [user.id.split('@')[0] for user in users]
        logger.info('Deleting user(s) %s ...', user_ids)
        aster_api_client = self._get_aster_api_client()
        aster_user_ids = [
            aster_api_client.get_org_users(search='schUser=={}'.format(user_id)).response.json()['data']['content'][0][
                'id'
            ]
            for user_id in user_ids
        ]
        return aster_api_client.delete_org_users(body=aster_user_ids)

    def assign_administrator_role(self, user):
        """Designate the specified user as an Organization Administrator.

        Args:
            user (:py:class:`streamsets.sdk.sch_models.User`): User object.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        user_id = user.id.split('@')[0]
        logger.info('Giving admin rights to user %s', user_id)
        aster_api_client = self._get_aster_api_client()
        aster_user_json = aster_api_client.get_org_users(search='schUser=={}'.format(user_id)).response.json()['data'][
            'content'
        ][0]
        aster_user_json.update({'role': 'ADMINISTRATOR'})
        return aster_api_client.update_org_user(user_id=aster_user_json['id'], body=aster_user_json)

    def remove_administrator_role(self, user):
        """Remove the Organization Administrator status from the specified user.

        Args:
            user (:py:class:`streamsets.sdk.sch_models.User`): User object.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        user_id = user.id.split('@')[0]
        logger.info('Removing admin rights from user %s', user_id)
        aster_api_client = self._get_aster_api_client()
        aster_user_json = aster_api_client.get_org_users(search='schUser=={}'.format(user_id)).response.json()['data'][
            'content'
        ][0]
        aster_user_json.update({'role': 'OPERATOR'})
        return aster_api_client.update_org_user(user_id=aster_user_json['id'], body=aster_user_json)

    @property
    def users(self):
        """Users.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Users`.
        """
        return Users(self, self._roles, self.organization)

    @property
    def login_audits(self):
        """Login Audits.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.LoginAudits`.
        """
        return LoginAudits(self, self.organization)

    @property
    def action_audits(self):
        """Action Audits.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ActionAudits`.
        """
        return ActionAudits(self, self.organization)

    @property
    def connection_audits(self):
        """Connection Audits.

        Returns:
            An instance of :py:obj:`streamsets.sdk.sch_models.ConnectionAudits`.
        """
        return ConnectionAudits(self, self.organization)

    def get_group_builder(self):
        """Get a group builder instance with which a group can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.GroupBuilder`.
        """
        # Update the GroupJson with the API definitions from Swagger.
        group_properties = self._security_api['definitions']['GroupJson']['properties']
        group = {property_: None for property_ in group_properties}

        # Set other properties based on defaults from the web UI.
        group_defaults = {'organization': self.organization, 'roles': DEFAULT_USER_ROLES, 'users': []}
        group.update(group_defaults)

        return GroupBuilder(group=group, roles=self._roles, control_hub=self)

    def add_group(self, group):
        """Add a group.

        Args:
            group (:py:class:`streamsets.sdk.sch_models.Group`): Group object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding a group %s ...', group)
        create_group_command = self.api_client.create_group(self.organization, group._data)
        # Update :py:class:`streamsets.sdk.sch_models.Group` with updated Group metadata.
        group._data = create_group_command.response.json()
        return create_group_command

    def update_group(self, group):
        """Update a group.

        Args:
            group (:py:class:`streamsets.sdk.sch_models.Group`): Group object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating a group %s ...', group)
        update_group_command = self.api_client.update_group(
            body=group._data, org_id=self.organization, group_id=group.group_id
        )
        group._data = update_group_command.response.json()
        return update_group_command

    def delete_group(self, *groups):
        """Delete groups.

        Args:
            *groups: One or more instances of :py:class:`streamsets.sdk.sch_models.Group`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if len(groups) == 1:
            logger.info('Deleting a group %s ...', groups[0])
            delete_group_command = self.api_client.delete_group(org_id=self.organization, group_id=groups[0].group_id)
        else:
            group_ids = [group.group_id for group in groups]
            logger.info('Deleting groups %s ...', group_ids)
            delete_group_command = self.api_client.delete_groups(body=group_ids, org_id=self.organization)
        return delete_group_command

    @property
    def groups(self):
        """Groups.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Groups`.
        """
        return Groups(self, self._roles, self.organization)

    @property
    def data_collectors(self):
        """Data Collectors registered to the ControlHub instance.

        Returns:
            Returns a :py:class:`streamsets.sdk.utils.SeekableList` of
            :py:class:`streamsets.sdk.sch_models.DataCollector` instances.
        """
        return self.engines.get_all(engine_type='COLLECTOR')

    @property
    def transformers(self):
        """Transformers registered to the ControlHub instance.

        Returns:
            Returns a :py:class:`streamsets.sdk.utils.SeekableList` of
            :py:class:`streamsets.sdk.sch_models.Transformer` instances.
        """
        return self.engines.get_all(engine_type='TRANSFORMER')

    @property
    def provisioning_agents(self):
        """Provisioning Agents registered to the ControlHub instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ProvisioningAgents`.
        """
        return ProvisioningAgents(self, self.organization)

    def delete_provisioning_agent(self, provisioning_agent):
        """Delete provisioning agent.

        Args:
            provisioning_agent (:py:class:`streamets.sdk.sch_models.ProvisioningAgent`):

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_provisioning_agent(provisioning_agent.id)

    def deactivate_provisioning_agent(self, provisioning_agent):
        """Deactivate provisioning agent.

        Args:
            provisioning_agent (:py:class:`streamets.sdk.sch_models.ProvisioningAgent`):

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.deactivate_components(org_id=self.organization, components_json=[provisioning_agent.id])

    def activate_provisioning_agent(self, provisioning_agent):
        """Activate provisioning agent.

        Args:
            provisioning_agent (:py:class:`streamets.sdk.sch_models.ProvisioningAgent`):

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.activate_components(org_id=self.organization, components_json=[provisioning_agent.id])

    def delete_provisioning_agent_token(self, provisioning_agent):
        """Delete provisioning agent token.

        Args:
            provisioning_agent (:py:class:`streamets.sdk.sch_models.ProvisioningAgent`):

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_components(org_id=self.organization, components_json=[provisioning_agent.id])

    @property
    def legacy_deployments(self):
        """Deployments.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.LegacyDeployments`.
        """
        return LegacyDeployments(self, self.organization)

    def get_legacy_deployment_builder(self):
        """Get a deployment builder instance with which a legacy deployment can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.LegacyDeploymentBuilder`.
        """
        deployment = {
            'name': None,
            'description': None,
            'labels': None,
            'numInstances': None,
            'spec': None,
            'agentId': None,
        }
        return LegacyDeploymentBuilder(dict(deployment))

    def add_legacy_deployment(self, deployment):
        """Add a legacy deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.LegacyDeployment`): Deployment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        create_deployment_command = self.api_client.create_legacy_deployment(deployment._data)
        # Update :py:class:`streamsets.sdk.sch_models.LegacyDeployment` with updated Deployment metadata.
        deployment._data = create_deployment_command.response.json()
        deployment._control_hub = self
        return create_deployment_command

    def update_legacy_deployment(self, deployment):
        """Update a deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.LegacyDeployment`): Deployment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating deployment %s ...', deployment)
        update_deployment_command = self.api_client.update_legacy_deployment(
            deployment_id=deployment.id, body=deployment._data
        )
        deployment._data = update_deployment_command.response.json()
        return update_deployment_command

    def scale_legacy_deployment(self, deployment, num_instances):
        """Scale up/down active deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.LegacyDeployment`): Deployment object.
            num_instances (:obj:`int`): Number of sdc instances.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        scale_deployment_command = self.api_client.scale_legacy_deployment(
            deployment_id=deployment.id, num_instances=num_instances
        )
        deployment._data = self.legacy_deployments.get(id=deployment.id)._data
        return scale_deployment_command

    def delete_legacy_deployment(self, *deployments):
        """Delete deployments.

        Args:
            *deployments: One or more instances of :py:class:`streamsets.sdk.sch_models.LegacyDeployment`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if len(deployments) == 1:
            logger.info('Deleting deployment %s ...', deployments[0])
            delete_deployment_command = self.api_client.delete_legacy_deployment(deployment_id=deployments[0].id)
        else:
            deployment_ids = [deployment.id for deployment in deployments]
            logger.info('Deleting deployments %s ...', deployment_ids)
            delete_deployment_command = self.api_client.delete_legacy_deployments(body=deployment_ids)
        return delete_deployment_command

    def start_legacy_deployment(self, deployment, **kwargs):
        """Start Deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.LegacyDeployment`): Deployment instance.
            wait (:obj:`bool`, optional): Wait for deployment to start. Default: ``True``.
            wait_for_statuses (:obj:`list`, optional): Deployment statuses to wait on. Default: ``['ACTIVE']``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.DeploymentStartStopCommand`.
        """
        provisioning_agent_id = deployment.provisioning_agent.id
        start_cmd = self.api_client.start_legacy_deployment(deployment.id, provisioning_agent_id)
        if kwargs.get('wait', True):
            start_cmd.wait_for_legacy_deployment_statuses(kwargs.get('wait_for_statuses', ['ACTIVE']))
        return start_cmd

    def stop_legacy_deployment(self, deployment, wait_for_statuses=['INACTIVE']):
        """Stop Deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.LegacyDeployment`): Deployment instance.
            wait_for_statuses (:obj:`list`, optional): List of statuses to wait for. Default: ``['INACTIVE']``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.DeploymentStartStopCommand`.
        """
        stop_cmd = self.api_client.stop_legacy_deployment(deployment.id)
        if wait_for_statuses:
            stop_cmd.wait_for_legacy_deployment_statuses(wait_for_statuses)
        return stop_cmd

    def acknowledge_legacy_deployment_error(self, *deployments):
        """Acknowledge errors for one or more deployments.

        Args:
            *deployments: One or more instances of :py:class:`streamsets.sdk.sch_models.LegacyDeployment`.
        """
        deployment_ids = [deployment.id for deployment in deployments]
        logger.info('Acknowledging errors for deployment(s) %s ...', deployment_ids)
        self.api_client.legacy_deployments_acknowledge_errors(deployment_ids)

    def deactivate_engine(self, engine):
        """Deactivate an engine.

        Args:
           engine (:py:class:`streamsets.sdk.sch_models.Engine`): Engine instance.
        """
        logger.info(
            'Deactivating engine component from organization %s with component id %s ...', self.organization, engine.id
        )
        self.api_client.deactivate_components(org_id=self.organization, components_json=[engine.id])

    def activate_engine(self, engine):
        """Activate an engine.

        Args:
            engine (:py:class:`streamsets.sdk.sch_models.Engine`): Engine instance.
        """
        logger.info(
            'Activating engine component from organization %s with component id %s ...', self.organization, engine.id
        )
        self.api_client.activate_components(org_id=self.organization, components_json=[engine.id])

    def delete_engine(self, engine):
        """Delete an engine.

        Args:
            engine (:py:class:`streamsets.sdk.sch_models.Engine`): Engine instance.
        """
        logger.info('Deleting engine %s ...', engine.id)
        self.api_client.delete_sdc(data_collector_id=engine.id)

    def delete_and_unregister_engine(self, engine):
        """Delete and Unregister an engine.

        Args:
            engine (:py:class:`streamsets.sdk.sch_models.Engine`): Engine instance.
        """
        logger.info(
            'Deactivating engine component from organization %s with component id %s ...',
            engine.organization,
            engine.id,
        )
        self.api_client.deactivate_components(org_id=self.organization, components_json=[engine.id])
        logger.info(
            'Deleting engine component from organization %s with component id %s ...', engine.organization, engine.id
        )
        self.api_client.delete_components(org_id=self.organization, components_json=[engine.id])
        logger.info('Deleting engine from jobrunner %s ...', engine.id)
        self.api_client.delete_sdc(data_collector_id=engine.id)

    def update_engine_labels(self, engine):
        """Update an engine's labels.

        Args:
            engine (:py:class:`streamsets.sdk.sch_models.Engine`): Engine instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Engine`.
        """
        logger.info('Updating engine %s with labels %s ...', engine.id, engine.labels)
        return Engine(
            engine=self.api_client.update_sdc_labels(
                data_collector_id=engine.id, data_collector_json=engine._data
            ).response.json(),
            control_hub=self,
        )

    def get_engine_labels(self, engine):
        """Returns all labels assigned to an engine.

        Args:
            engine (:py:class:`streamsets.sdk.sch_models.Engine`): Engine instance.

        Returns:
            A :obj:`list` of engine assigned labels.
        """
        logger.info('Getting assigned labels for engine %s ...', engine.id)
        return self.api_client.get_sdc_labels(data_collector_id=engine.id).response.json()

    def update_engine_resource_thresholds(
        self, engine, max_cpu_load=None, max_memory_used=None, max_pipelines_running=None
    ):
        """Updates engine resource thresholds.

        Args:
            engine (:py:class:`streamsets.sdk.sch_models.Engine`): Engine instance.
            max_cpu_load (:obj:`float`, optional): Max CPU load in percentage. Default: ``None``.
            max_memory_used (:obj:`int`, optional): Max memory used in MB. Default: ``None``.
            max_pipelines_running (:obj:`int`, optional): Max pipelines running. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        thresholds = {
            'maxMemoryUsed': max_memory_used,
            'maxCpuLoad': max_cpu_load,
            'maxPipelinesRunning': max_pipelines_running,
        }
        thresholds_to_be_updated = {k: v for k, v in thresholds.items() if v is not None}
        engine_json = engine._data
        engine_json.update(thresholds_to_be_updated)
        cmd = self.api_client.update_sdc_resource_thresholds(engine.id, engine_json)
        engine.refresh()
        return cmd

    def balance_engines(self, *engines):
        """Balance all jobs running on given Engine.

        Args:
            *engines: One or more instances of :py:class:`streamsets.sdk.sch_models.Engine`.
        """
        engine_ids = [engine.id for engine in engines]
        logger.info('Balancing all jobs on Engine(s) %s ...', engine_ids)
        self.api_client.balance_data_collectors(engine_ids)

    def delete_unregistered_auth_tokens(self, executor_type):
        """Delete auth tokens for engines that have been unregistered.

        Args:
            executor_type (:obj:`str`): The executor type. Acceptable values are 'DATACOLLECTOR' or 'TRANSFORMER'.
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_non_registered_components(self.organization, executor_type)

    def shutdown_engines(self, *engines):
        """Call shutdown on the given engine(s).

        Args:
            *engines: One or more instances of :py:class:`streamsets.sdk.sch_models.DataCollector` or
                :py:class:`streamsets.sdk.sch_models.Transformer`.
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        engine_ids = [engine.id for engine in engines]
        return self.api_client.shutdown_deployment_engines(engine_ids)

    def restart_engines(self, *engines):
        """Restart the given engine(s).

        Args:
            *engines:  One or more instances of :py:class:`streamsets.sdk.sch_models.DataCollector` or
                :py:class:`streamsets.sdk.sch_models.Transformer`.
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        engine_ids = [engine.id for engine in engines]
        return self.api_client.restart_deployment_engines(engine_ids)

    def get_job_builder(self):
        """Get a job builder instance with which a job can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.JobBuilder`.
        """
        job_properties = self._job_api['definitions']['JobJson']['properties']
        job = {property_: None for property_ in job_properties}

        # Set other properties based on defaults from the web UI.
        JOB_DEFAULTS = {
            'forceStopTimeout': 120000,
            'labels': ['all'],
            'numInstances': 1,
            'statsRefreshInterval': 60000,
            'rawJobTags': [],
        }
        job.update(JOB_DEFAULTS)
        return JobBuilder(job=job, control_hub=self)

    def get_components(self, component_type_id, offset=None, len_=None, order_by='LAST_VALIDATED_ON', order='ASC'):
        """Get components.

        Args:
            component_type_id (:obj:`str`): Component type id.
            offset (:obj:`str`, optional): Default: ``None``.
            len_ (:obj:`str`, optional): Default: ``None``.
            order_by (:obj:`str`, optional): Default: ``'LAST_VALIDATED_ON'``.
            order (:obj:`str`, optional): Default: ``'ASC'``.
        """
        return self.api_client.get_components(
            org_id=self.organization,
            component_type_id=component_type_id,
            offset=offset,
            len=len_,
            order_by=order_by,
            order=order,
        )

    def create_components(self, component_type, number_of_components=1, active=True):
        """Create components.

        Args:
            component_type (:obj:`str`): Component type.
            number_of_components (:obj:`int`, optional): Default: ``1``.
            active (:obj:`bool`, optional): Default: ``True``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.CreateComponentsCommand`.
        """
        return self.api_client.create_components(
            org_id=self.organization,
            component_type=component_type,
            number_of_components=number_of_components,
            active=active,
        )

    def get_organization_builder(self):
        """Get an organization builder instance with which an organization can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.OrganizationBuilder`.
        """
        new_org_properties = self._security_api['definitions']['NewOrganizationJson']['properties']
        organization = {property_: None for property_ in new_org_properties}

        # Set other properties based on defaults from the web UI.
        organization_defaults = {
            'active': True,
            'passwordExpiryTimeInMillis': 5184000000,  # 60 days
            'validDomains': '*',
        }
        organization_admin_user_defaults = {
            'active': True,
            'roles': [
                'user',
                'org-admin',
                'datacollector:admin',
                'pipelinestore:pipelineEditor',
                'jobrunner:operator',
                'timeseries:reader',
                'timeseries:writer',
                'topology:editor',
                'notification:user',
                'sla:editor',
                'provisioning:operator',
            ],
        }
        organization['organization'] = organization_defaults
        organization['organizationAdminUser'] = organization_admin_user_defaults

        return OrganizationBuilder(
            organization=organization['organization'], organization_admin_user=organization['organizationAdminUser']
        )

    def add_organization(self, organization):
        """Add an organization.

        Args:
            organization (:py:obj:`streamsets.sdk.sch_models.Organization`): Organization object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding organization %s ...', organization.name)
        body = {'organization': organization._data, 'organizationAdminUser': organization._organization_admin_user}
        create_organization_command = self.api_client.create_organization(body)
        organization._data = create_organization_command.response.json()
        return create_organization_command

    def update_organization(self, organization):
        """Update an organization.

        Args:
            organization (:py:obj:`streamsets.sdk.sch_models.Organization`): Organization instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating organization %s ...', organization.name)
        update_organization_command = self.api_client.update_organization(
            org_id=organization.id, body=organization._data
        )
        organization._data = update_organization_command.response.json()
        return update_organization_command

    @property
    def organizations(self):
        """Organizations.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Organizations`.
        """
        return Organizations(self)

    @property
    def api_credentials(self):
        """Api Credentials.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.ApiCredential`.
        """
        return ApiCredentials(self)

    def get_api_credential_builder(self):
        """Get api credential Builder.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ApiCredentialBuilder`.
        """
        api_creds_properties = self._security_api['definitions']['ApiCredentialsJson']['properties']
        api_credential = {property_: None for property_ in api_creds_properties}
        return ApiCredentialBuilder(api_credential=api_credential, control_hub=self)

    def add_api_credential(self, api_credential):
        """Add an api credential. Some api credential attributes are updated by ControlHub such as
            created_by.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): An API credential instance, built
                via the :py:meth:`streamsets.sdk.sch_models.ApiCredentialBuilder.build` method.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not api_credential._request:
            raise AttributeError(
                'Malformed API Credential: the _request attribute is missing. Please verify that the '
                'API Credential was built using an APICredentialBuilder.'
            )
        logger.info('Adding an api credential %s ...', api_credential.name)
        create_api_credential_command = self.api_client.create_api_user_credential(
            self.organization, api_credential._request
        )
        # Update :py:class:`streamsets.sdk.sch_models.ApiCredential` with updated ApiCredential metadata.
        api_credential._data = create_api_credential_command.response.json()

        return create_api_credential_command

    def delete_api_credentials(self, *api_credentials):
        """Delete api_credentials.

        Args:
            *api_credentials: One or more instances of :py:class:`streamsets.sdk.sch_models.ApiCredential`.
        """
        for api_credential in api_credentials:
            logger.info('Deleting api credential %s ...', api_credential)
            self.api_client.delete_api_user_credential(
                org_id=self.organization, credential_id=api_credential.credential_id
            )

    def regenerate_api_credential_auth_token(self, api_credential):
        """Regenerate the auth token for an api credential.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): ApiCredential object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self._update_api_credential(api_credential, generate_auth_token=True)

    def rename_api_credential(self, api_credential):
        """Rename an api credential.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): ApiCredential object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self._update_api_credential(api_credential)

    def activate_api_credential(self, api_credential):
        """Activate an api credential.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): ApiCredential object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self._update_api_credential(api_credential, active=True)

    def deactivate_api_credential(self, api_credential):
        """Deactivate an api credential.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): ApiCredential object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self._update_api_credential(api_credential, active=False)

    def _update_api_credential(self, api_credential, active=None, generate_auth_token=False):
        """Update an api credential.

        Args:
            api_credential (:py:class:`streamsets.sdk.sch_models.ApiCredential`): ApiCredential object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        payload = dict(label=api_credential.name, generateAuthToken=generate_auth_token)
        if active is not None:
            payload['active'] = active

        update_api_credential_command = self.api_client.update_api_user_credential(
            org_id=self.organization, credential_id=api_credential.credential_id, api_user_credential_json=payload
        )
        api_credential._data = update_api_credential_command.response.json()

        return update_api_credential_command

    @property
    def pipelines(self):
        """Pipelines.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Pipelines`.
        """
        return Pipelines(self, self.organization)

    def import_pipelines_from_archive(self, archive, commit_message, fragments=False):
        """Import pipelines from archived zip directory.

        Args:
            archive (:obj:`file`): file containing the pipelines.
            commit_message (:obj:`str`): Commit message.
            fragments (:obj:`bool`, optional): Indicates if pipeline contains fragments.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Pipeline`.
        """
        return SeekableList(
            [
                Pipeline(
                    pipeline,
                    builder=None,
                    pipeline_definition=json.loads(pipeline['pipelineDefinition']),
                    rules_definition=json.loads(pipeline['currentRules']['rulesDefinition']),
                    control_hub=self,
                )
                for pipeline in self.api_client.import_pipelines(
                    commit_message=commit_message, pipelines_file=archive, fragments=fragments
                ).response.json()
            ]
        )

    def import_pipeline(self, pipeline, commit_message, name=None, data_collector_instance=None):
        """Import pipeline from json file.

        Args:
            pipeline (:obj:`dict`): A python dict representation of ControlHub Pipeline.
            commit_message (:obj:`str`): Commit message.
            name (:obj:`str`, optional): Name of the pipeline. If left out, pipeline name from JSON object will be
                                         used. Default ``None``.
            data_collector_instance (:py:class:`streamsets.sdk.sch_models.DataCollector`): If excluded, system sdc will
                                                                                           be used. Default ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Pipeline`.
        """
        if name is None:
            name = pipeline['pipelineConfig']['title']
        sdc_id = data_collector_instance.id if data_collector_instance is not None else DEFAULT_SYSTEM_SDC_ID
        pipeline['pipelineConfig']['info']['sdcId'] = sdc_id
        commit_pipeline_json = {
            'name': name,
            'commitMessage': commit_message,
            'pipelineDefinition': json.dumps(pipeline['pipelineConfig']),
            'libraryDefinitions': json.dumps(pipeline['libraryDefinitions']),
            'rulesDefinition': json.dumps(pipeline['pipelineRules']),
            'sdcId': sdc_id,
        }
        commit_pipeline_response = self.api_client.commit_pipeline(
            new_pipeline=False, import_pipeline=True, body=commit_pipeline_json
        ).response.json()
        commit_id = commit_pipeline_response['commitId']
        return self.pipelines.get(commit_id=commit_id)

    def export_pipelines(self, pipelines, fragments=False, include_plain_text_credentials=False):
        """Export pipelines.

        Args:
            pipelines (:obj:`list`): A list of :py:class:`streamsets.sdk.sch_models.Pipeline` instances.
            fragments (:obj:`bool`): Indicates if exporting fragments is needed.
            include_plain_text_credentials (:obj:`bool`): Indicates if plain text credentials should be included.

        Returns:
            An instance of type :py:obj:`bytes` indicating the content of zip file with pipeline json files.
        """
        commit_ids = [pipeline.commit_id for pipeline in pipelines]
        return self.api_client.export_pipelines(
            body=commit_ids, fragments=fragments, include_plain_text_credentials=include_plain_text_credentials
        ).response.content

    @property
    def draft_runs(self):
        """Draft Runs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.DraftRuns`.
        """
        return DraftRuns(self)

    def start_draft_run(self, pipeline, reset_origin=False, runtime_parameters=None):
        """Start a draft run.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object. (Must be in draft mode)
            reset_origin (:obj:`boolean`, optional): Default: ``False``.
            runtime_parameters (:obj:`dict`, optional): Pipeline runtime parameters. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not pipeline.draft:
            raise Exception("Pipeline isn't in draft mode, draft run can't be started.")

        job_response = self.api_client.get_draft_run_job_for_pipeline_id(pipeline.pipeline_id).response
        if job_response.content:
            job_id = job_response.json()["id"]
        else:
            job_builder = self.get_job_builder()
            job = job_builder.build('Draft Run for {}'.format(pipeline.name), pipeline=pipeline)
            job.draft_run = True
            job._data["labels"] = []
            job._data["runTimeParameters"] = runtime_parameters
            job_json = self.api_client.create_job(job._data).response.json()
            job_id = job_json["id"]

        if reset_origin:
            self.api_client.reset_jobs_offset(job_id)

        return self.api_client.start_job(job_id)

    def stop_draft_run(self, *draft_runs, force=False, timeout_sec=300):
        """Stop a draft run.

        Args:
            *draft_runs: One or more instances of :py:class:`streamsets.sdk.sch_models.DraftRuns`.
            force (:obj:`bool`, optional): Force draft run to stop. Default: ``False``.
            timeout_sec (:obj:`int`, optional): Timeout in secs. Default: ``300``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.StopJobsCommand`.
        """
        return self.stop_job(*draft_runs, force=force, timeout_sec=timeout_sec)

    def delete_draft_run(self, *draft_runs):
        """Remove a draft run.

        Args:
            *draft_runs: One or more instances of :py:class:`streamsets.sdk.sch_models.DraftRun`.
        """
        self.delete_job(*draft_runs)

    @property
    def jobs(self):
        """Jobs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Jobs`.
        """
        return Jobs(self)

    def wait_for_job_sequence_status(self, job_sequence, expected_status, timeout_sec=DEFAULT_WAIT_FOR_STATUS_TIMEOUT):
        """Block until the job sequence reaches the desired status.

        Args:
            job_sequence (:py:class:`streamsets.sdk.sch_models.JobSequence`): The JobSequence instance.
            expected_status (:obj:`str`): The desired status to wait for.
            timeout_sec (:obj:`int`, optional): Timeout to wait for ``job_sequence`` to reach ``expected_status``,
                in seconds. Default: :py:const:`streamsets.sdk.sch.DEFAULT_WAIT_FOR_STATUS_TIMEOUT`.

        Raises:
            TimeoutError: If ``timeout_sec`` passes without ``job_sequence`` reaching ``expected_status``.
            TypeError: If ``job_sequence`` is not a :py:class:`streamsets.sdk.sch_models.JobSequence` instance.
        """

        expected_status = JobSequence.JobSequenceStatusType(expected_status)

        if not isinstance(job_sequence, JobSequence):
            raise TypeError('job_sequence must be of type JobSequence')

        def condition():
            job_sequence.refresh()
            logger.debug(
                'Waiting for sequence `{}` status to change to `{}`, current status `{}`'.format(
                    job_sequence.name, expected_status.value, job_sequence.status
                )
            )
            return job_sequence.status == expected_status.value

        def success(time):
            logger.debug('Sequence turned to status %s in %s seconds.', expected_status.value, time)

        def failure(timeout):
            raise Exception(
                'Timed out after `{}` seconds waiting for sequence `{}` to turn to status `{}`'.format(
                    timeout, job_sequence.id, expected_status.value
                )
            )

        wait_for_condition(condition=condition, timeout=timeout_sec, success=success, failure=failure)

    def get_job_sequence_builder(self):
        """Get a job sequence builder instance with which a job sequence can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.JobSequenceBuilder`.
        """
        job_sequence = {property: None for property in self._sequencing_api['definitions']['USequence']['properties']}
        job_sequence['id'] = None
        job_sequence['nextRunTime'] = None

        return JobSequenceBuilder(job_sequence=job_sequence, control_hub=self)

    @property
    def job_sequences(self):
        """Job Sequences.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.JobSequences`.
        """
        return JobSequences(self)

    def publish_job_sequence(self, job_sequence):
        """Publishes an Job Sequence to ControlHub.

        Args:
            job_sequence: An instance of :py:class:`streamsets.sdk.sch_models.JobSequence`

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """

        if not isinstance(job_sequence, JobSequence):
            raise TypeError('The job sequence must be a JobSequence instance')

        response = self.api_client.create_job_sequence(job_sequence._data)

        job_sequence._data = response.response.json()

        return response

    def delete_job_sequences(self, *job_sequences):
        """Delete Job Sequences.

        Args:
            *job_sequences: One or more instances of :py:class:`streamsets.sdk.sch_models.JobSequence`

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """

        sequence_ids = []

        for sequence in job_sequences:
            if not isinstance(sequence, JobSequence):
                raise TypeError(
                    'Each job sequence must be an instance of' ' :py:class:`streamsets.sdk.sch_models.JobSequence`'
                )
            sequence_ids.append(sequence.id)

        return self.api_client.delete_job_sequences(sequence_ids)

    def update_job_sequence_metadata(self, job_sequence):
        """Update Job Sequence metadata.

        Args:
            job_sequence: An instance of :py:class:`streamsets.sdk.sch_models.JobSequence`

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """

        if not isinstance(job_sequence, JobSequence):
            raise TypeError('job_sequence must be an instance of :py:class:`streamsets.sdk.sch_models.JobSequence`')

        data = {
            "name": job_sequence.name,
            "description": job_sequence.description,
            "startTime": job_sequence.start_time,
            "endTime": job_sequence.end_time,
            "timezone": job_sequence.timezone,
            "crontabMask": job_sequence.crontab_mask,
        }

        response = self.api_client.update_job_sequence(job_sequence.id, data)
        job_sequence._data = response.response.json()

        return response

    def run_job_sequence(self, job_sequence, start_from_step_number=None, single_step=False):
        """Run the Job Sequence.

        Args:
            job_sequence: An instance of :py:class:`streamsets.sdk.sch_models.JobSequence`.
            start_from_step_number (:obj:`int`, optional): The Step to start execution from. Default: `None`.
            single_step (:obj:`bool`, optional): Whether to only run the specified step. Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not isinstance(job_sequence, JobSequence):
            raise TypeError('The job_sequence must be an instance of :py:class:`streamsets.sdk.sch_models.JobSequence`')

        if start_from_step_number and not isinstance(start_from_step_number, int):
            raise TypeError('start_from_step_number must be an int')

        if start_from_step_number and (start_from_step_number > len(job_sequence.steps) or start_from_step_number <= 0):
            raise ValueError('start_from_step_number must be a valid step number within the Job Sequence')

        if not isinstance(single_step, bool):
            raise TypeError('single_step must be of type bool`')

        if start_from_step_number is None and single_step is True:
            raise ValueError('single_step cannot be set to True if start_from_step_number has not been passed')

        allowed_statuses = [
            JobSequence.JobSequenceStatusType.INACTIVE.value,
            JobSequence.JobSequenceStatusType.ERROR.value,
        ]
        if job_sequence.status not in allowed_statuses:
            raise ValueError(
                "Can only run job sequence {} when it is in either {} status".format(job_sequence.id, allowed_statuses)
            )

        return self.api_client.run_job_sequence(
            sequence_id=job_sequence.id, step_number=start_from_step_number, single_step=single_step
        )

    def enable_job_sequence(self, job_sequence):
        """Enable the Job Sequence.

        Args:
            job_sequence: An instance of :py:class:`streamsets.sdk.sch_models.JobSequence`

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not isinstance(job_sequence, JobSequence):
            raise TypeError('The job_sequence must be an instance of :py:class:`streamsets.sdk.sch_models.JobSequence`')

        if job_sequence.status != JobSequence.JobSequenceStatusType.DISABLED.value:
            raise ValueError("Can only enable job sequence {} when it is in DISABLED status".format(job_sequence.id))

        return self.api_client.enable_job_sequence(job_sequence.id)

    def disable_job_sequence(self, job_sequence):
        """Disable the Job Sequence.

        Args:
            job_sequence: An instance of :py:class:`streamsets.sdk.sch_models.JobSequence`

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not isinstance(job_sequence, JobSequence):
            raise TypeError('The job_sequence must be an instance of :py:class:`streamsets.sdk.sch_models.JobSequence`')

        allowed_statuses = [
            JobSequence.JobSequenceStatusType.INACTIVE.value,
            JobSequence.JobSequenceStatusType.ERROR.value,
        ]
        if job_sequence.status not in allowed_statuses:
            raise ValueError(
                "Can only disable job sequence {} when it is in either {} status".format(
                    job_sequence.id, allowed_statuses
                )
            )

        return self.api_client.disable_job_sequence(job_sequence.id)

    @property
    def data_protector_enabled(self):
        """:obj:`bool`: Whether Data Protector is enabled for the current organization."""
        add_ons = self.api_client.get_available_add_ons().response.json()
        logger.debug('Add-ons: %s', add_ons)
        return all(app in add_ons['enabled'] for app in ['policy', 'sdp_classification'])

    @property
    def connection_tags(self):
        """Connection Tags.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ConnectionTags`.
        """
        return ConnectionTags(control_hub=self, organization=self.organization)

    @property
    def alerts(self):
        """Alerts.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Alert`.
        """
        # The SCH API requires fetching active and acknowledged alerts separately. As such we make two calls for each
        # of the active/acknowledged endpoints, combine them and sort chronologically by 'triggeredOn'.
        active_alerts = self.api_client.get_all_alerts(alert_status='ACTIVE').response.json()
        acknowledged_alerts = self.api_client.get_all_alerts(alert_status='ACKNOWLEDGED').response.json()

        sorted_alerts = sorted(active_alerts + acknowledged_alerts, key=lambda x: x['triggeredOn'])
        return SeekableList(Alert(alert, control_hub=self) for alert in sorted_alerts)

    def add_job(self, job):
        """Add a job.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        new_job_properties = self._job_api['definitions']['NewJobJson']['properties']
        new_job_json = {property_: value for property_, value in job._data.items() if property_ in new_job_properties}
        logger.info('Adding job %s ...', job.job_name)
        create_job_command = self.api_client.create_job(body=new_job_json)
        # Update :py:class:`streamsets.sdk.sch_models.Job` with updated Job metadata.
        job._data = create_job_command.response.json()

        if self.data_protector_enabled:
            policies = dict(jobId=job.job_id)
            if job.read_policy:
                policies['readPolicyId'] = job.read_policy._id
            else:
                read_protection_policies = self._get_protection_policies('Read')
                if len(read_protection_policies) == 1:
                    logger.warning(
                        'Read protection policy not set for job (%s). Setting to %s ...',
                        job.job_name,
                        read_protection_policies[0].name,
                    )
                    policies['readPolicyId'] = read_protection_policies[0]._id
                else:
                    raise Exception('Read policy not selected.')

            if job.write_policy:
                policies['writePolicyId'] = job.write_policy._id
            else:
                write_protection_policies = self._get_protection_policies('Write')
                if len(write_protection_policies) == 1:
                    logger.warning(
                        'Write protection policy not set for job (%s). Setting to %s ...',
                        job.job_name,
                        write_protection_policies[0].name,
                    )
                    policies['writePolicyId'] = write_protection_policies[0]._id
                else:
                    raise Exception('Write policy not selected.')
            self.api_client.update_job_policies(body=policies)
        return create_job_command

    def edit_job(self, job):
        """Edit a job.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        logger.warning('This method has been superseded by update_job and will be removed in a future release.')
        logger.info('Editing job %s with job id %s ...', job.job_name, job.job_id)
        return Job(self.api_client.update_job(job_id=job.job_id, job_json=job._data).response.json())

    def update_job(self, job):
        """Update a job.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        logger.info('Updating job %s with job id %s ...', job.job_name, job.job_id)
        return Job(self.api_client.update_job(job_id=job.job_id, job_json=job._data).response.json())

    def upgrade_job(self, *jobs):
        """Upgrade job(s) to latest pipeline version.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        self.api_client.upgrade_jobs(job_ids)
        return SeekableList(self.jobs.get(id=job_id) for job_id in job_ids)

    def import_jobs(
        self, archive, pipeline=True, number_of_instances=False, labels=False, runtime_parameters=False, **kwargs
    ):
        # update_migrate_offsets is not configurable through UI and is supported through kwargs.
        """Import jobs from archived zip directory.

        Args:
            archive (:obj:`file`): file containing the jobs.
            pipeline (:obj:`boolean`, optional): Indicate if pipeline should be imported. Default: ``True``.
            number_of_instances (:obj:`boolean`, optional): Indicate if number of instances should be imported.
                                                            Default: ``False``.
            labels (:obj:`boolean`, optional): Indicate if labels should be imported. Default: ``False``.
            runtime_parameters (:obj:`boolean`, optional): Indicate if runtime parameters should be imported.
                                                           Default: ``False``.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        imported_jobs = self.api_client.import_jobs(
            jobs_file=archive,
            update_pipeline_refs=pipeline,
            update_num_instances=number_of_instances,
            update_labels=labels,
            update_runtime_parameters=runtime_parameters,
            **kwargs,
        ).response.json()
        return SeekableList([Job(job['minimalJobJson'], control_hub=self) for job in imported_jobs])

    def export_jobs(self, jobs):
        """Export jobs to a compressed archive.

        Args:
            jobs (:obj:`list`): A list of :py:class:`streamsets.sdk.sch_models.Job` instances.

        Returns:
            An instance of type :py:obj:`bytes` indicating the content of zip file with job json files.
        """
        job_ids = [job.job_id for job in jobs]
        return self.api_client.export_jobs(body=job_ids).response.content

    def reset_origin(self, *jobs):
        # It is called reset_origin instead of reset_offset in the UI because that is how sdc calls it. If we change it
        # to reset_offset in sdc, it would affect a lot of people.
        """Reset all pipeline offsets for given jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        self.api_client.reset_jobs_offset(job_ids)
        return SeekableList(self.jobs.get(id=job_id) for job_id in job_ids)

    def upload_offset(self, job, offset_file=None, offset_json=None):
        """Upload offset for given job.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.
            offset_file (:obj:`file`, optional): File containing the offsets. Default: ``None``. Exactly one of
                                                 ``offset_file``, ``offset_json`` should specified.
            offset_json (:obj:`dict`, optional): Contents of offset. Default: ``None``. Exactly one of ``offset_file``,
                                                 ``offset_json`` should specified.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        # Comparing with None because, {} is also an accepted offset.
        if offset_file and offset_json is not None:
            raise ValueError("Cannot specify both the arguments offset_file and offset_json at the same time.")
        if not offset_file and offset_json is None:
            raise ValueError("Exactly one of the arguments offset_file and offset_json should be specified.")
        if offset_json is not None:
            job_json = self.api_client.upload_job_offset_as_json(job.job_id, offset_json).response.json()
        else:
            job_json = self.api_client.upload_job_offset(job.job_id, offset_file).response.json()
        return Job(job_json, self)

    def get_current_job_status(self, job):
        """Returns the current job status for given job id.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.
        """
        logger.info('Fetching job status for job id %s ...', job.job_id)
        return self.api_client.get_current_job_status(job_id=job.job_id)

    def delete_job(self, *jobs):
        """Delete one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = []
        job_template_ids = []
        for job in jobs:
            if job.job_template:
                job_template_ids.append(job.job_id)
            else:
                job_ids.append(job.job_id)

        if job_template_ids:
            self.api_client.cascade_delete_job_template(job_template_ids)
        logger.info('Deleting job(s) %s ...', job_ids)
        if len(job_ids) == 1:
            try:
                api_version = 2 if '/v2/job/{jobId}' in self._job_api['paths'] else 1
            except Exception:
                # Ignore any improper swagger setup and fall back to default version in case of any errors
                api_version = 1
            self.api_client.delete_job(job_ids[0], api_version=api_version)
        elif len(job_ids) > 1:
            self.api_client.delete_jobs(job_ids)

    def start_job(self, *jobs, wait=True, **kwargs):
        """Start one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
            wait (:obj:`bool`, optional): Wait for pipelines to reach RUNNING status before returning.
                Default: ``True``.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.StartJobsCommand`.
        """

        job_names = [job.job_name for job in jobs]
        logger.info('Starting %s (%s) ...', 'jobs' if len(job_names) > 1 else 'job', ', '.join(job_names))

        job_ids = [job.job_id for job in jobs]
        start_jobs_command = self.api_client.start_jobs(job_ids)
        # The startJobs endpoint in ControlHub returns an OK with no other data in the body. As such, we add
        #  the list of jobs passed to this method as an attribute to the StartJobsCommand returned by
        # :py:method:`streamsets.sdk.sch_api.ApiClient.start_jobs`.
        start_jobs_command.jobs = jobs
        wait_kwargs = {key: value for (key, value) in kwargs.items() if key == 'timeout_sec'}
        if wait:
            start_jobs_command.wait_for_pipelines(**wait_kwargs)
        return start_jobs_command

    def start_job_template(
        self,
        job_template,
        name=None,
        description=None,
        attach_to_template=True,
        delete_after_completion=False,
        instance_name_suffix='COUNTER',
        number_of_instances=1,
        parameter_name=None,
        raw_job_tags=None,
        runtime_parameters=None,
        wait_for_data_collectors=False,
        inherit_permissions=False,
        wait=True,
        asynchronous=False,
    ):
        """Start Job instances from a Job Template.

        Args:
            job_template (:py:class:`streamsets.sdk.sch_models.Job`): A Job instance with the property job_template set
                                                                      to ``True``.
            name (:obj:`str`, optional): Name of the new job(s). Default: ``None``. If not specified, name of the job
                                         template with ``' copy'`` appended to the end will be used.
            description (:obj:`str`, optional): Description for new job(s). Default: ``None``.
            attach_to_template (:obj:`bool`, optional): Default: ``True``.
            delete_after_completion (:obj:`bool`, optional): Default: ``False``.
            instance_name_suffix (:obj:`str`, optional): Suffix to be used for Job names in
                                                         {'COUNTER', 'TIME_STAMP', 'PARAM_VALUE'}. Default: ``COUNTER``.
            number_of_instances (:obj:`int`, optional): Number of instances to be started using given parameters.
                                                        Default: ``1``.
            parameter_name (:obj:`str`, optional): Specified when instance_name_suffix is 'PARAM_VALUE'.
                                                   Default: ``None``.
            raw_job_tags (:obj:`list`, optional): Default: ``None``.
            runtime_parameters (:obj:`dict`) or (:obj:`list`): Runtime Parameters to be used in the jobs. If a dict is
                                                               specified, ``number_of_instances`` jobs will be started.
                                                               If a list is specified, ``number_of_instances`` is
                                                               ignored and job instances will be started using the
                                                               elements of the list as Runtime Parameters for each job.
                                                               If left out, Runtime Parameters from Job Template will be
                                                               used. Default: ``None``.
            wait_for_data_collectors (:obj:`bool`, optional): Wait for the created job instance(s) to be assigned an
                engine before proceeding. Default: ``False``.
            inherit_permissions (:obj:`bool`, optional): Parameter to determine if the user wants to inherit the ACL
                                                         from the template instead of getting the default ACL for it.
                                                         Default: ``False``.
            wait (:obj:`bool`, optional): Wait for jobs to reach ACTIVE status before returning.
                Default: ``True``.
            asynchronous(:obj:`bool`, optional): Whether to start and create the jobs asynchronously or not.
                Default: ``False``.

        Returns:
            A :py:class:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Job` instances.
        """
        assert job_template.job_template, "Please specify a Job Template instance."
        if instance_name_suffix == 'PARAM_VALUE':
            assert parameter_name is not None, "Please specify a parameter name."

        job_template_properties = self._job_api['definitions']['JobTemplateCreationInfoJson']['properties']
        start_job_template_json = {property_: None for property_ in job_template_properties}

        if runtime_parameters is None:
            runtime_parameters = job_template.runtime_parameters._data
        if isinstance(runtime_parameters, dict):
            runtime_parameters = [runtime_parameters] * number_of_instances

        start_job_template_json.update(
            {
                'attachToTemplate': attach_to_template,
                'deleteAfterCompletion': delete_after_completion,
                'description': description,
                'name': name,
                'namePostfixType': instance_name_suffix,
                'paramName': parameter_name,
                'rawJobTags': raw_job_tags,
                'runtimeParametersList': runtime_parameters,
            }
        )

        # Note: create_and_start_job_instances returns a list of job statuses and hence the ID attribute is jobId.
        # However, create_and_start_job_instances_async returns a list of jobs and hence the ID attribute is id
        jobs_response = (
            self.api_client.create_and_start_job_instances(
                job_template.job_id, start_job_template_json, inherit_permissions
            )
            if not asynchronous
            else self.api_client.create_and_start_job_instances_async(
                job_template.job_id, start_job_template_json, inherit_permissions
            )
        )
        id_key = 'jobId' if not asynchronous else 'id'

        jobs = SeekableList()
        for job_response in jobs_response.response.json():
            job = self.jobs.get(id=job_response[id_key])
            if wait:
                self.api_client.wait_for_job_status(job_id=job.job_id, status='ACTIVE')
            if wait_for_data_collectors:

                def job_has_data_collector(job):
                    job.refresh()
                    job_data_collectors = job.data_collectors
                    logger.debug('Job Data Collectors: %s', job_data_collectors)
                    return len(job_data_collectors) > 0

                wait_for_condition(job_has_data_collector, [job], timeout=120)
            job.refresh()
            jobs.append(job)

        return jobs

    def stop_job(self, *jobs, force=False, timeout_sec=300):
        """Stop one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
            force (:obj:`bool`, optional): Force job to stop. Default: ``False``.
            timeout_sec (:obj:`int`, optional): Timeout in secs. Default: ``300``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.StopJobsCommand`.
        """
        jobs_ = {job.job_id: job for job in jobs}
        job_ids = list(jobs_.keys())
        logger.info('Stopping job(s) %s ...', job_ids)
        # At the end, we'll return the command from the job being stopped, so we hold onto it while we update
        # the underlying :py:class:`streamsets.sdk.sch_models.Job` instances.
        stop_jobs_command = self.api_client.force_stop_jobs(job_ids) if force else self.api_client.stop_jobs(job_ids)

        job_inactive_error = None
        for job_id in job_ids:
            try:
                self.api_client.wait_for_job_status(job_id=job_id, status='INACTIVE', timeout_sec=timeout_sec)
            except JobInactiveError as ex:
                job_inactive_error = ex
        updated_jobs = self.api_client.get_jobs(body=job_ids).response.json()
        for updated_job in updated_jobs:
            job_id = updated_job['id']
            jobs_[job_id]._data = updated_job
        if job_inactive_error and not force:
            raise job_inactive_error
        return stop_jobs_command

    def get_protection_policy_builder(self):
        """Get a protection policy builder instance with which a protection policy can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ProtectionPolicyBuilder`.
        """
        protection_policy = self.api_client.get_new_protection_policy().response.json()['response']['data']
        protection_policy.pop('messages', None)
        id_ = protection_policy['id']

        policy_procedure = self.api_client.get_new_policy_procedure(id_).response.json()['response']['data']
        policy_procedure.pop('messages', None)
        return ProtectionPolicyBuilder(self, protection_policy, policy_procedure)

    def get_protection_method_builder(self):
        """Get a protection method builder instance with which a protection method can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ProtectionMethodBuilder`.
        """
        return ProtectionMethodBuilder(self.get_pipeline_builder())

    def get_classification_rule_builder(self):
        """Get a classification rule builder instance with which a classification rule can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ClassificationRuleBuilder`.
        """
        classification_rule = self.api_client.get_new_classification_rule(
            self._classification_catalog_id
        ).response.json()['response']['data']
        # Remove 'messages' from the classification rule JSON.
        classification_rule.pop('messages', None)
        classifier = self.api_client.get_new_classification_classifier(self._classification_catalog_id).response.json()[
            'response'
        ]['data']
        # Remove 'messages' from the classifier JSON.
        classifier.pop('messages', None)
        return ClassificationRuleBuilder(classification_rule, classifier)

    @property
    def _classification_catalog_id(self):
        """Get the classification catalog id for the org.

        Returns:
            An instance of :obj:`str`:.
        """
        classification_catalog_list_response = self.api_client.get_classification_catalog_list().response.json()
        # We assume it's the first (and only) classification catalog id for the org
        return classification_catalog_list_response['response'][0]['data']['id']

    def add_protection_policy(self, protection_policy):
        """Add a protection policy.

        Args:
            protection_policy (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Protection Policy object.
        """
        protection_policy._id = self.api_client.create_protection_policy(
            {'data': protection_policy._data}
        ).response.json()['response']['data']['id']
        for procedure in protection_policy.procedures:
            new_policy_procedure = self.api_client.get_new_policy_procedure(protection_policy._id).response.json()[
                'response'
            ]['data']
            procedure._id = new_policy_procedure['id']
            procedure._policy_id = protection_policy._id
            self.api_client.create_policy_procedure({'data': procedure._data})

    def set_default_write_protection_policy(self, protection_policy):
        """Set a default write protection policy.

        Args:
            protection_policy
            (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Protection
            Policy object to be set as the default write policy.

        Returns:
            An updated instance of :py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`.

        """
        policy_id = protection_policy._data['id']
        self.api_client.set_default_write_protection_policy(policy_id)
        # Once the policy is updated, the local copy needs to be refreshed.
        # The post call itself doesn't return the latest data, so need to do
        # another lookup.  This mimics the UI in its behavior.
        return self.protection_policies.get(_id=policy_id)

    def set_default_read_protection_policy(self, protection_policy):
        """Set a default read protection policy.

        Args:
            protection_policy
            (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Protection
            Policy object to be set as the default read policy.

        Returns:
            An updated instance of :py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`.
        """
        policy_id = protection_policy._data['id']
        self.api_client.set_default_read_protection_policy(policy_id)
        # Once the policy is updated, the local copy needs to be refreshed.
        # The post call itself doesn't return the latest data, so need to do
        # another lookup.  This mimics the UI in its behavior.
        return self.protection_policies.get(_id=policy_id)

    def export_protection_policies(self, protection_policies):
        """Export protection policies to a compressed archive.

        Args:
            protection_policies (:obj:`list`): A list of :py:class:`streamsets.sdk.sch_models.ProtectionPolicy`
            instances.

        Returns:
            An instance of type :py:obj:`bytes` indicating the content of zip file with protection policy json files.
        """
        policy_ids = [policy._id for policy in protection_policies]
        return self.api_client.export_protection_policies(policy_ids=policy_ids).response.content

    def import_protection_policies(self, policies_archive):
        """Import protection policies from a compressed archive.

        Args:
            policies_archive (:obj:`file`): file containing the protection policies.

        Returns:
            A py:class:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.ProtectionPolicy`.
        """
        policies = self.api_client.import_protection_policies(policies_archive).response.json()['response']
        return SeekableList([ProtectionPolicy(policy['data']) for policy in policies])

    @property
    def protection_policies(self):
        """Protection policies.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ProtectionPolicies`.
        """
        return ProtectionPolicies(self)

    def validate_pipeline(self, pipeline):
        """Validate pipeline. Only Transformer for Snowflake pipelines are supported at this time.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline instance.

        Raises:
            :py:obj:`streamsets.sdk.exceptions.ValidationError`: If validation fails.
        """
        if not pipeline.pipeline_id:
            raise Exception('The pipeline must have been published to Control Hub before attempting to validate it')
        if pipeline.executor_type != 'SNOWPARK':
            engine_instance, engine_pipeline_id = self._add_pipeline_to_executor_if_not_exists(pipeline)
            if self.use_websocket_tunneling:
                tunneling_instance_id = self.api_client.get_tunneling_instance_id(pipeline.sdc_id).response.json()[
                    'instanceId'
                ]
                validate_command = self.api_client.validate_engine_pipeline(
                    engine_id=pipeline.sdc_id,
                    pipeline_id=engine_pipeline_id,
                    tunneling_instance_id=tunneling_instance_id,
                ).wait_for_validate(engine_id=pipeline.sdc_id, tunneling_instance_id=tunneling_instance_id)
            else:
                validate_command = engine_instance.api_client.validate_pipeline(engine_pipeline_id).wait_for_validate()
        else:
            _, engine_pipeline_id = self._add_pipeline_to_executor_if_not_exists(pipeline)
            validate_command = self.api_client.validate_snowflake_pipeline(
                engine_pipeline_id, timeout=500000
            ).wait_for_validate()
        response = validate_command.response.json()
        if response['status'] != 'VALID':
            if response.get('issues'):
                raise ValidationError(response['issues'])
            elif response.get('message'):
                raise ValidationError(response['message'])
            else:
                raise ValidationError('Unknown validation failure with status as {}'.format(response['status']))
        return response['status']

    def run_pipeline_preview(
        self,
        pipeline,
        batches=1,
        batch_size=10,
        skip_targets=True,
        skip_lifecycle_events=True,
        end_stage=None,
        only_schema=None,
        timeout=120000,
        test_origin=False,
        read_policy=None,
        write_policy=None,
        executor=None,
        **kwargs,
    ):
        """Run pipeline preview.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            batches (:obj:`int`, optional): Number of batches. Default: ``1``.
            batch_size (:obj:`int`, optional): Batch size. Default: ``10``.
            skip_targets (:obj:`bool`, optional): Skip targets. Default: ``True``.
            skip_lifecycle_events (:obj:`bool`, optional): Skip life cycle events. Default: ``True``.
            end_stage (:obj:`str`, optional): End stage. Default ``None``.
            only_schema (:obj:`bool`, optional): Only schema. Default: ``None``.
            timeout (:obj:`int`, optional): Timeout. Default: ``120000``.
            test_origin (:obj:`bool`, optional): Test origin. Default: ``False``.
            read_policy (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Read Policy for preview.
                If not provided, uses default read policy if one available. Default: ``None``.
            write_policy (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Write Policy for preview.
                If not provided, uses default write policy if one available. Default: ``None``.
            executor (:py:obj:`streamsets.sdk.sch_models.DataCollector`, optional): The Data Collector
                in which to preview the pipeline. If omitted, ControlHub's first executor SDC will be used.
                Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sdc_api.PreviewCommand`.
        """
        # Note: We only support SDC and Snowflake executor for now
        # Note: system data collector cannot be used for pipeline preview
        executor_type = getattr(pipeline, 'executor_type', 'COLLECTOR')
        if executor_type != SNOWFLAKE_EXECUTOR_TYPE and not executor and len(self.data_collectors) < 1:
            raise Exception('No executor found')

        if self.data_protector_enabled:
            executor_instance = (executor or self.data_collectors[0])._instance

            if not read_policy:
                read_protection_policies = self._get_protection_policies('Read')
                if len(read_protection_policies) == 1:
                    read_policy_id = read_protection_policies[0].id
                else:
                    raise Exception('Read policy not selected.')
            else:
                read_policy_id = read_policy.id

            if not write_policy:
                write_protection_policies = self._get_protection_policies('Write')
                if len(write_protection_policies) == 1:
                    write_policy_id = write_protection_policies[0].id
                else:
                    raise Exception('Write policy not selected.')
            else:
                write_policy_id = write_policy.id

            parameters = {
                'pipelineCommitId': pipeline.commit_id,
                'pipelineId': pipeline.pipeline_id,
                'read.policy.id': read_policy_id,
                'write.policy.id': write_policy_id,
                'classification.catalogId': self._classification_catalog_id,
            }

            return executor_instance.run_dynamic_pipeline_preview(
                type='PROTECTION_POLICY',
                parameters=parameters,
                batches=batches,
                batch_size=batch_size,
                skip_targets=skip_targets,
                skip_lifecycle_events=skip_lifecycle_events,
                end_stage=end_stage,
                timeout=timeout,
                test_origin=test_origin,
            )

        executor_instance, executor_pipeline_id = self._add_pipeline_to_executor_if_not_exists(pipeline)
        if executor_instance:
            return executor_instance.run_pipeline_preview(
                pipeline_id=executor_pipeline_id,
                batches=batches,
                batch_size=batch_size,
                skip_targets=skip_targets,
                end_stage=end_stage,
                timeout=timeout,
                test_origin=test_origin,
                wait=kwargs.get('wait', True),
                remote=kwargs.get('remote', False),
            )

        return self.run_snowflake_pipeline_preview(
            pipeline_id=executor_pipeline_id,
            batches=batches,
            batch_size=batch_size,
            skip_targets=skip_targets,
            end_stage=end_stage,
            only_schema=only_schema,
            push_limit_down=kwargs.get('push_limit_down', True),
            timeout=timeout,
            test_origin=test_origin,
            wait=kwargs.get('wait', True),
        )

    def run_snowflake_pipeline_preview(
        self,
        pipeline_id,
        rev=0,
        batches=1,
        batch_size=10,
        skip_targets=True,
        end_stage=None,
        only_schema=None,
        push_limit_down=True,
        timeout=2000,
        test_origin=False,
        stage_outputs_to_override_json=None,
        **kwargs,
    ):
        """Run Snowflake pipeline preview.

        Args:
            pipeline_id (:obj:`str`): The pipeline instance's ID.
            rev (:obj:`int`, optional): Pipeline revision. Default: ``0``.
            batches (:obj:`int`, optional): Number of batches. Default: ``1``.
            batch_size (:obj:`int`, optional): Batch size. Default: ``10``.
            skip_targets (:obj:`bool`, optional): Skip targets. Default: ``True``.
            end_stage (:obj:`str`, optional): End stage. Default: ``None``.
            only_schema (:obj:`bool`, optional): Only schema. Default: ``None``.
            push_limit_down (:obj:`bool`, optional): Push limit down. Default: ``True``.
            timeout (:obj:`int`, optional): Timeout. Default: ``2000``.
            test_origin (:obj:`bool`, optional): Test origin. Default: ``False``
            stage_outputs_to_override_json (:obj:`str`, optional): Stage outputs to override. Default: ``None``.
            wait (:obj:`bool`, optional): Wait for pipeline preview to finish. Default: ``True``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sdc_api.PreviewCommand`.
        """
        logger.info('Running preview for %s ...', pipeline_id)
        preview_command = self.api_client.run_snowflake_pipeline_preview(
            pipeline_id,
            rev,
            batches,
            batch_size,
            skip_targets,
            end_stage,
            only_schema,
            push_limit_down,
            timeout,
            test_origin,
            stage_outputs_to_override_json,
        )
        if kwargs.get('wait', True):
            preview_command.wait_for_finished()

        return preview_command

    def test_pipeline_run(self, pipeline, reset_origin=False, parameters=None):
        """Test run a pipeline.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            reset_origin (:obj:`boolean`, optional): Default: ``False``.
            parameters (:obj:`dict`, optional): Pipeline parameters. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sdc_api.StartPipelineCommand`.
        """
        executor_instance, executor_pipeline_id = self._add_pipeline_to_executor_if_not_exists(
            pipeline=pipeline, reset_origin=reset_origin, parameters=parameters
        )
        # Update pipeline rules as seen at https://git.io/JURT4
        pipeline_rules_command = executor_instance.api_client.get_pipeline_rules(pipeline_id=executor_pipeline_id)
        pipeline_rules = pipeline._rules_definition
        pipeline_rules['uuid'] = pipeline_rules_command.response.json()['uuid']
        executor_instance.api_client.update_pipeline_rules(pipeline_id=executor_pipeline_id, pipeline=pipeline_rules)
        start_pipeline_command = executor_instance.start_pipeline(executor_pipeline_id)
        start_pipeline_command.executor_pipeline = pipeline
        start_pipeline_command.executor_instance = executor_instance
        return start_pipeline_command

    def _add_pipeline_to_executor_if_not_exists(self, pipeline, reset_origin=False, parameters=None):
        """Util function to add ControlHub pipeline to executor.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            reset_origin (:obj:`boolean`, optional): Default: ``False``.
            parameters (:obj:`dict`, optional): Pipeline parameters. Default: ``None``.

        Returns:
            An instance of :obj:`tuple` of (:py:obj:`streamsets.sdk.DataCollector` or
                :py:obj:`streamsets.sdk.Transformer` and :py:obj:`streamsets.sdk.sdc_models.Pipeline`)
        """
        executor_type = getattr(pipeline, 'executor_type', 'COLLECTOR') or 'COLLECTOR'
        principal_user_id = self.api_client.get_current_user().response.json()['principalId']
        executor_pipeline_id = 'testRun__{}__{}__{}'.format(
            pipeline.pipeline_id.split(':')[0], self.organization, principal_user_id
        )
        if executor_type == SNOWFLAKE_EXECUTOR_TYPE:
            authoring_executor_instance = None
        else:
            authoring_executor = self.engines.get(id=pipeline.sdc_id)
            authoring_executor_instance = authoring_executor._instance
        if authoring_executor_instance:
            pipeline_status_command = authoring_executor_instance.api_client.get_pipeline_status(
                pipeline_id=executor_pipeline_id, only_if_exists=True
            )
        else:
            pipeline_status_command = self.api_client.get_snowflake_pipeline(
                pipeline_id=executor_pipeline_id, only_if_exists=True
            )
        if not pipeline_status_command.response.text:
            if authoring_executor_instance:
                authoring_executor_instance.api_client.create_pipeline(
                    pipeline_title=executor_pipeline_id,
                    description="New Pipeline",
                    auto_generate_pipeline_id=False,
                    draft=False,
                )
            else:
                self.api_client.create_snowflake_pipeline(
                    pipeline_title=executor_pipeline_id,
                    description="New Pipeline",
                    auto_generate_pipeline_id=False,
                    draft=False,
                )
        elif reset_origin:
            if authoring_executor_instance:
                authoring_executor_instance.api_client.reset_origin_offset(pipeline_id=executor_pipeline_id)
            else:
                self.api_client.reset_snowflake_origin_offset(pipeline_id=executor_pipeline_id)
        if authoring_executor_instance:
            pipeline_info = authoring_executor_instance.api_client.get_pipeline_configuration(
                pipeline_id=executor_pipeline_id, get='info'
            )
        else:
            pipeline_info = self.api_client.get_snowflake_pipeline_configuration(
                pipeline_id=executor_pipeline_id, get='info'
            )
        if parameters:
            pipeline.parameters = parameters
        executor_pipeline_json = pipeline._pipeline_definition
        executor_pipeline_json['pipelineId'] = executor_pipeline_id
        executor_pipeline_json['uuid'] = pipeline_info['uuid']
        if authoring_executor_instance:
            authoring_executor_instance.api_client.update_pipeline(
                pipeline_id=executor_pipeline_id, pipeline=executor_pipeline_json
            )
        else:
            self.api_client.update_snowflake_pipeline(pipeline_id=executor_pipeline_id, pipeline=executor_pipeline_json)
        return authoring_executor_instance, executor_pipeline_id

    def stop_test_pipeline_run(self, start_pipeline_command):
        """Stop the test run of pipeline.

        Args:
            start_pipeline_command (:py:class:`streamsets.sdk.sdc_api.StartPipelineCommand`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sdc_api.StopPipelineCommand`.
        """
        return start_pipeline_command.executor_instance.stop_pipeline(start_pipeline_command.executor_pipeline)

    def preview_classification_rule(self, classification_rule, parameter_data, data_collector=None):
        """Dynamic preview of a classification rule.

        Args:
            classification_rule (:py:obj:`streamsets.sdk.sch_models.ClassificationRule`): Classification Rule object.
            parameter_data (:obj:`dict`): A python dict representation of raw JSON parameters required for preview.
            data_collector (:py:obj:`streamsets.sdk.sch_models.DataCollector`, optional): The Data Collector
                in which to preview the pipeline. If omitted, ControlHub's first executor SDC will be used.
                Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sdc_api.PreviewCommand`.
        """
        if self.data_protector_enabled:
            # Note: system data collector cannot be used for dynamic preview
            if not data_collector and len(self.data_collectors) < 1:
                raise Exception('No executor DataCollector found')
            else:
                data_collector_instance = (data_collector or self.data_collectors[0])._instance
                parameters = {
                    'classification.catalogId': classification_rule.catalog_uuid,
                    'rawJson': json.dumps(parameter_data),
                }
                return data_collector_instance.run_dynamic_pipeline_preview(
                    type='CLASSIFICATION_CATALOG', parameters=parameters
                )

    def add_classification_rule(self, classification_rule, commit=False):
        """Add a classification rule.

        Args:
            classification_rule (:py:obj:`streamsets.sdk.sch_models.ClassificationRule`): Classification Rule object.
            commit (:obj:`bool`, optional): Whether to commit the rule after adding it. Default: ``False``.
        """
        self.api_client.create_classification_rule({'data': classification_rule._data})
        classifier_list = self.api_client.get_classification_classifier_list(classification_rule._data['id'])
        for classifier in classifier_list.response.json()['response']:
            classifier_id = classifier['data']['id']
            self.api_client.delete_classification_classifier(classifier_id)

        for classifier in classification_rule.classifiers:
            self.api_client.create_classification_classifier({'data': classifier._data})

        if commit:
            self.api_client.commit_classification_rules(self._classification_catalog_id)

    def get_snowflake_pipeline_defaults(self):
        """Get the Snowflake pipeline defaults for this user (if it exists).

        Returns:
            A :obj:`dict` of Snowflake pipeline defaults.
        """
        return self.api_client.get_snowflake_pipeline_defaults().response.json()

    def update_snowflake_pipeline_defaults(
        self, account_url=None, database=None, warehouse=None, schema=None, role=None
    ):
        """Create or update the Snowflake pipeline defaults for this user.

        Args:
            account_url (:obj:`str`, optional): Snowflake account url. Default: ``None``
            database (:obj:`str`, optional): Snowflake database to query against. Default: ``None``
            warehouse (:obj:`str`, optional): Snowflake warehouse. Default: ``None``
            schema (:obj:`str`, optional): Schema used. Default: ``None``
            role (:obj:`str`, optional): Role used. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        body = {'accountUrl': account_url, 'database': database, 'warehouse': warehouse, 'schema': schema, 'role': role}
        return self.api_client.update_snowflake_pipeline_defaults(body)

    def delete_snowflake_pipeline_defaults(self):
        """Delete the Snowflake pipeline defaults for this user.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_snowflake_pipeline_defaults()

    def get_snowflake_user_credentials(self):
        """Get the Snowflake user credentials (if they exist). They will be redacted.

        Returns:
            A :obj:`dict` of Snowflake user credentials (redacted).
        """
        return self.api_client.get_snowflake_user_credentials().response.json()

    def update_snowflake_user_credentials(
        self, username, snowflake_login_type, password=None, private_key=None, role=None
    ):
        """Create or update the Snowflake user credentials.

        Args:
            username (:obj:`str`): Snowflake account username.
            snowflake_login_type (:obj:`str`): Snowflake login type to use. Options are ``password`` and
                ``privateKey``.
            password (:obj:`str`, optional): Snowflake account password. Default: ``None``
            private_key (:obj:`str`, optional): Snowflake account private key. Default: ``None``
            role (:obj:`str`, optional): Snowflake role of the account. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        valid_snowflake_login_types = {'PASSWORD', 'PRIVATE_KEY'}
        if snowflake_login_type not in valid_snowflake_login_types:
            raise ValueError("snowflake_login_type must be either password or privateKey")
        elif snowflake_login_type == 'PASSWORD' and password is None:
            raise ValueError("password cannot be None when snowflake_login_type is 'PASSWORD'")
        elif snowflake_login_type == 'PRIVATE_KEY' and private_key is None:
            raise ValueError("private_key cannot be None when snowflake_login_type is 'PRIVATE_KEY'")

        body = {
            'username': username,
            'snowflakeLoginType': snowflake_login_type,
            'password': password,
            'privateKey': private_key,
            'role': role,
        }
        return self.api_client.update_snowflake_user_credentials(body)

    def delete_snowflake_user_credentials(self):
        """Delete the Snowflake user credentials.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_snowflake_user_credentials()

    def get_scheduled_task_builder(self):
        """Get a scheduled task builder instance with which a scheduled task can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ScheduledTaskBuilder`.
        """
        job_selection_types = self.api_client.get_job_selection_types(api_version=2).response.json()['response']['data']
        return ScheduledTaskBuilder(job_selection_types, self)

    def publish_scheduled_task(self, task):
        """Send the scheduled task to Control Hub. DEPRECATED

        Args:
            task (:py:class:`streamsets.sdk.sch_models.ScheduledTask`): Scheduled task object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        warnings.warn(
            'The publish_scheduled_task method has been deprecated and will be removed in a future release. '
            'Please use the add_scheduled_task method instead.',
            DeprecationWarning,
        )
        return self.add_scheduled_task(task)

    def add_scheduled_task(self, task):
        """Add the scheduled task to Control Hub.

        Args:
            task (:py:class:`streamsets.sdk.sch_models.ScheduledTask`): Scheduled task object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.

        Raises:
            Exception: Thrown if publishing the task was unsuccessful
        """
        create_task_command = self.api_client.create_scheduled_task(data={'data': task._data}, api_version=2)
        returned_data = create_task_command.response.json()

        # The API will send back a 200 response even if it failed to publish the task.
        # In the case that publishing was unsuccessful, we grab the error message (if it exists) out and raise it
        if not returned_data['response']['success']:
            # The structure of the response from the ScheduledTask API is very poorly designed. As a result, we
            # need to parse through several nested dicts (and nested lists of dicts..) to get the information required
            # to pass back to the user. This will be improved via Epic DPM-20808.
            if returned_data['response']['messages']:
                error_message = returned_data['response']['messages'][0]['message']
                # Parse fields out of returned_data IFF they are a dict and have a 'messages' key.
                fields_with_messages = [
                    item
                    for item in returned_data['response']['data']
                    if isinstance(returned_data['response']['data'][item], dict)
                    and returned_data['response']['data'][item].get('messages')
                ]
                root_cause = []
                for field in fields_with_messages:
                    # There can be more than one message per field, so we have to parse through all of them to find
                    # only the ERROR message types.
                    specific_errors = [
                        message['message']
                        for message in returned_data['response']['data'][field]['messages']
                        if message['type'] == 'ERROR'
                    ]
                    root_cause.extend(specific_errors)
                raise Exception(
                    'Could not publish Scheduled Task "{}" due to: {}, caused by: '
                    '{}.'.format(task.name, error_message, root_cause)
                )
            else:
                raise Exception('Could not publish Scheduled Task {}'.format(repr(task)))

        task._data = returned_data['response']['data']
        return create_task_command

    def update_scheduled_task(self, task):
        """Update an existing scheduled task in Control Hub.

        Args:
            task (:py:class:`streamsets.sdk.sch_models.ScheduleTask`): Scheduled task object.

        Returns:
            An instance of py:class:`streamsets.sdk.sch_api.Command`.
        """
        update_task_command = self.api_client.update_scheduled_task(
            data={'data': task._data}, id=task.id, api_version=2
        )
        task._data = update_task_command.response.json()['response']['data']
        return update_task_command

    def _validate_and_execute_scheduled_tasks_action(self, action, *scheduled_tasks):
        """Performs specified action on given scheduled tasks.

        Args:
            action (:py:class:`streamsets.sdk.sch_models.ScheduledTaskActions`): An enum of the action to be performed
            *scheduled_tasks:  One or more instances of :py:class:`streamsets.sdk.sch_models.ScheduledTask`
        Returns:
            An instance of:py:class:`streamsets.sdk.sch_api.Command`.
        """

        if not isinstance(action, ScheduledTaskActions):
            raise ValueError(
                'Action not permitted on scheduled task, should be of type '
                'streamsets.sdk.sch_models.ScheduledTaskActions'
            )

        scheduled_tasks_map = {}
        for scheduled_task in scheduled_tasks:
            if isinstance(scheduled_task, ScheduledTask):
                scheduled_tasks_map[scheduled_task.id] = scheduled_task
            else:
                logger.debug('{} was filtered for not being of type ScheduledTask'.format(scheduled_task))

        if not scheduled_tasks_map:
            raise ValueError('No valid scheduled task passed to the function')

        response_command = self.api_client.perform_bulk_action_on_scheduled_tasks(
            list(scheduled_tasks_map.keys()), action.value, api_version=2
        )
        # we want to update the internal data of each scheduled task object
        response_json = response_command.response.json()['response']
        for updated_task_data in response_json:
            if not updated_task_data['data']:
                # this occurs when the user passes an already deleted scheduled task object
                continue

            scheduled_task_id = updated_task_data['data']['id']
            if updated_task_data['data']['messages'] and updated_task_data['data']['messages'][0]['type'] == 'ERROR':
                error_message = updated_task_data['data']['messages'][0]['message']
                # only show the error message from the task id onwards as the rest doesn't make sense to the user
                error_message = error_message[error_message.find(scheduled_task_id) - 1 :]
                logger.error(error_message)
            # we get the data back from the ui, even on failure, so we can update the task's internal data
            scheduled_tasks_map[scheduled_task_id]._data = updated_task_data['data']
            del scheduled_tasks_map[scheduled_task_id]

        # for scheduled tasks that were already deleted
        if scheduled_tasks_map:
            logger.warning(
                'Scheduled tasks with ids {} were not found on Control Hub'.format(
                    ', '.join(scheduled_tasks_map.keys())
                )
            )

        return response_command

    def pause_scheduled_tasks(self, *scheduled_tasks):
        """Pause given scheduled tasks.

        Args:
            *scheduled_tasks: One or more instances of :py:class:`streamsets.sdk.sch_models.ScheduledTask`
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """

        return self._validate_and_execute_scheduled_tasks_action(ScheduledTaskActions.PAUSE, *scheduled_tasks)

    def resume_scheduled_tasks(self, *scheduled_tasks):
        """Resume given scheduled tasks.

        Args:
            *scheduled_tasks: One or more instances of :py:class:`streamsets.sdk.sch_models.ScheduledTask`
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """

        return self._validate_and_execute_scheduled_tasks_action(ScheduledTaskActions.RESUME, *scheduled_tasks)

    def kill_scheduled_tasks(self, *scheduled_tasks):
        """Kill given scheduled tasks.

        Args:
            *scheduled_tasks: One or more instances of :py:class:`streamsets.sdk.sch_models.ScheduledTask`
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """

        return self._validate_and_execute_scheduled_tasks_action(ScheduledTaskActions.KILL, *scheduled_tasks)

    def delete_scheduled_tasks(self, *scheduled_tasks):
        """Delete given scheduled tasks.

        Args:
            *scheduled_tasks: One or more instances of :py:class:`streamsets.sdk.sch_models.ScheduledTask`
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """

        return self._validate_and_execute_scheduled_tasks_action(ScheduledTaskActions.DELETE, *scheduled_tasks)

    @property
    def scheduled_tasks(self):
        """Scheduled Tasks.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ScheduledTasks`.
        """
        return ScheduledTasks(self)

    @property
    def subscriptions(self):
        """Event Subscriptions.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Subscriptions`.
        """
        return Subscriptions(self)

    def get_subscription_builder(self):
        """Get Event Subscription Builder.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.SubscriptionBuilder`.
        """
        event_sub_properties = self._notification_api['definitions']['EventSubscriptionJson']['properties']
        subscription = {property_: None for property_ in event_sub_properties}
        subscription.update(dict(enabled=True, deleted=False, events=[]))
        return SubscriptionBuilder(subscription=subscription, control_hub=self)

    def add_subscription(self, subscription):
        """Add Subscription to ControlHub.

        Args:
            subscription (:py:obj:`streamsets.sdk.sch_models.Subscription`): A Subscription instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        event_types = self._en_translations['notifications']['subscriptions']['events']
        subscription._data['events'] = [
            {'eventType': reversed_dict(event_types)[event.event_type], 'filter': event.filter}
            for event in subscription.events
        ]
        action_config = subscription._data['externalActions'][0]['config']
        encoded_config = json.dumps(action_config) if isinstance(action_config, dict) else action_config
        subscription._data['externalActions'][0]['config'] = encoded_config
        create_subscription_command = self.api_client.create_event_subscription(body=subscription._data)
        subscription._data = create_subscription_command.response.json()
        return create_subscription_command

    def update_subscription(self, subscription):
        """Update an existing Subscription.

        Args:
            subscription (:py:obj:`streamsets.sdk.sch_models.Subscription`): A Subscription instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        event_types = self._en_translations['notifications']['subscriptions']['events']
        subscription._data['events'] = [
            {'eventType': reversed_dict(event_types)[event.event_type], 'filter': event.filter}
            for event in subscription.events
        ]
        action_config = subscription._data['externalActions'][0]['config']
        encoded_config = json.dumps(action_config) if isinstance(action_config, dict) else action_config
        subscription._data['externalActions'][0]['config'] = encoded_config
        update_subscription_command = self.api_client.update_event_subscription(body=subscription._data)
        subscription._data = update_subscription_command.response.json()
        return update_subscription_command

    def delete_subscription(self, subscription):
        """Delete an exisiting Subscription.

        Args:
            subscription (:py:obj:`streamsets.sdk.sch_models.Subscription`): A Subscription instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_event_subscription(subscription_id=subscription.id)

    def acknowledge_event_subscription_error(self, subscription):
        """Acknowledge an error on given Event Subscription.

        Args:
            subscription (:py:obj:`streamsets.sdk.sch_models.Subscription`): A Subscription instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        cmd = self.api_client.event_subscription_acknowledge_error(subscription.id)
        subscription._data = cmd.response.json()
        return cmd

    @property
    def subscription_audits(self):
        """Subscription audits.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.SubscriptionAudit`.
        """
        cmd = self.api_client.get_all_subscription_audits()
        return SeekableList([SubscriptionAudit(audit) for audit in cmd.response.json()])

    def acknowledge_job_error(self, *jobs):
        """Acknowledge errors for one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Acknowledging errors for job(s) %s ...', job_ids)
        self.api_client.jobs_acknowledge_errors(job_ids)

    def sync_job(self, *jobs):
        """Sync one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Synchronizing job(s) %s ...', job_ids)
        self.api_client.sync_jobs(job_ids)

    def balance_job(self, *jobs):
        """Balance one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Balancing job(s) %s ...', job_ids)
        self.api_client.balance_jobs(job_ids)

    def get_topology_builder(self):
        """Get a topology builder instance with which a topology can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.TopologyBuilder`.
        """
        topology_json = {}
        # Update the topology_json with the API definitions from Swagger.
        topology_properties = self._topology_api['definitions']['TopologyJson']['properties']
        topology_json.update({property_: None for property_ in topology_properties})
        topology_json['organization'] = self.organization
        topology_json['topologyDefinition'] = {}
        topology_json['topologyDefinition']['schemaVersion'] = '1'
        topology_json['topologyDefinition']['topologyNodes'] = []
        topology_json['topologyDefinition']['stageIcons'] = {}
        topology_json['topologyDefinition']['valid'] = True

        return TopologyBuilder(topology=topology_json, control_hub=self)

    def get_data_sla_builder(self):
        """Get a Data SLA builder instance with which a Data SLA can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.DataSlaBuilder`.
        """
        sla_properties = self._sla_api['definitions']['DataSlaJson']['properties']
        data_sla = {property_: None for property_ in sla_properties}
        data_sla['organization'] = self.organization

        return DataSlaBuilder(data_sla, self)

    @property
    def topologies(self):
        """Topologies.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Topologies`.
        """
        return Topologies(self)

    def import_topologies(
        self, archive, import_number_of_instances=False, import_labels=False, import_runtime_parameters=False, **kwargs
    ):
        # update_migrate_offsets is not configurable through UI and is supported through kwargs.
        """Import topologies from archived zip directory.

        Args:
            archive (:obj:`file`): file containing the topologies.
            import_number_of_instances (:obj:`boolean`, optional): Indicate if number of instances should be imported.
                                                            Default: ``False``.
            import_labels (:obj:`boolean`, optional): Indicate if labels should be imported. Default: ``False``.
            import_runtime_parameters (:obj:`boolean`, optional): Indicate if runtime parameters should be imported.
                                                           Default: ``False``.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Topology`.
        """
        topologies = self.api_client.import_topologies(
            topologies_file=archive,
            update_num_instances=import_number_of_instances,
            update_labels=import_labels,
            update_runtime_parameters=import_runtime_parameters,
            **kwargs,
        )
        return SeekableList([Topology(topology, control_hub=self) for topology in topologies.response.json()])

    def export_topologies(self, topologies):
        """Export topologies.

        Args:
            topologies (:obj:`list`): A list of :py:class:`streamsets.sdk.sch_models.Topology` instances.

        Returns:
            An instance of type :py:obj:`bytes` indicating the content of zip file with pipeline json files.
        """
        commit_ids = [topology.commit_id for topology in topologies]
        return self.api_client.export_topologies(body=commit_ids).response.content

    def delete_topology(self, topology, only_selected_version=False):
        """Delete a topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object.
            only_selected_version (:obj:`boolean`): Delete only current commit.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if only_selected_version:
            logger.info('Deleting topology version %s for topology %s ...', topology.commit_id, topology.topology_name)
            return self.api_client.delete_topology_versions(commits_json=[topology.commit_id])
        logger.info('Deleting topology %s with topology id %s ...', topology.topology_name, topology.topology_id)
        return self.api_client.delete_topologies(topologies_json=[topology.topology_id])

    def publish_topology(self, topology, commit_message=None):
        """Publish a topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object to publish.
            commit_message (:obj:`str`, optional): Commit message to supply with the Topology. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        # If the topology already has a commit_id but isn't in draft mode, we assume it exists and create a new draft
        # in order to update the existing instance before publishing
        if topology.commit_id and not topology.draft:
            try:
                draft_topology = self.api_client.create_topology_draft(commit_id=topology.commit_id).response.json()
            except requests.exceptions.HTTPError:
                raise
            draft_topology.update({'topologyDefinition': topology._data['topologyDefinition']})
            created_topology = self.api_client.update_topology(
                commit_id=draft_topology['commitId'], topology_json=draft_topology
            ).response.json()
            response = self.api_client.publish_topology(
                commit_id=created_topology['commitId'], commit_message=commit_message
            )
        # This is a brand-new topology being created for the first time
        elif not topology.commit_id:
            created_topology = self.api_client.create_topology(topology_json=topology._data).response.json()
            response = self.api_client.publish_topology(
                commit_id=created_topology['commitId'], commit_message=commit_message
            )
        # This is an existing topology that's already in draft mode
        else:
            response = self.api_client.publish_topology(commit_id=topology.commit_id, commit_message=commit_message)
        # Refresh the in-memory representation of the topology
        topology.commit_id = response.response.json()['commitId']
        topology._refresh()

        return response

    @property
    def report_definitions(self):
        """Report Definitions.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ReportDefinitions`.
        """
        return ReportDefinitions(self)

    def add_report_definition(self, report_definition):
        """Add Report Definition to ControlHub.

        Args:
            report_definition (:py:class:`streamsets.sdk.sch_models.ReportDefinition`): Report Definition instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        create_report_definition_command = self.api_client.create_new_report_definition(report_definition._data)
        report_definition._data = create_report_definition_command.response.json()
        return create_report_definition_command

    def update_report_definition(self, report_definition):
        """Update an existing Report Definition.

        Args:
            report_definition (:py:class:`streamsets.sdk.sch_models.ReportDefinition`): Report Definition instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        update_report_definition_command = self.api_client.update_report_definition(
            report_definition.id, report_definition._data
        )
        report_definition._data = update_report_definition_command.response.json()
        return update_report_definition_command

    def delete_report_definition(self, report_definition):
        """Delete an existing Report Definition.

        Args:
            report_definition (:py:class:`streamsets.sdk.sch_models.ReportDefinition`): Report Definition instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        return self.api_client.delete_report_definition(report_definition.id)

    def get_connection_builder(self):
        """Get a connection builder instance with which a connection can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ConnectionBuilder`.
        """
        # Update the ConnectionJson with the API definitions from Swagger.
        connection_properties = self._connection_api['definitions']['ConnectionJson']['properties']
        connection = {property_: None for property_ in connection_properties}
        connection['organization'] = self.organization

        return ConnectionBuilder(connection=connection, control_hub=self)

    def add_connection(self, connection):
        """Add a connection.

        Args:
            connection (:py:class:`streamsets.sdk.sch_models.Connection`): Connection object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding a connection %s ...', connection)
        # Update _data with any changes made to the connection definition
        connection._data.update({'connectionDefinition': json.dumps(connection._connection_definition._data)})
        create_connection_command = self.api_client.create_connection(connection._data)
        # Update :py:class:`streamsets.sdk.sch_models.Connection` with updated Connection metadata.
        connection._data = create_connection_command.response.json()
        return create_connection_command

    @property
    def connections(self):
        """Connections.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Connections`.
        """
        return Connections(self, self.organization)

    def update_connection(self, connection):
        """Update a connection.

        Args:
            connection (:py:class:`streamsets.sdk.sch_models.Connection`): Connection object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating a connection %s ...', connection)
        # Update _data with any changes made to the connection definition
        connection._data.update({'connectionDefinition': json.dumps(connection._connection_definition._data)})
        update_connection_command = self.api_client.update_connection(
            connection_id=connection.id, body=connection._data
        )
        connection._data = update_connection_command.response.json()
        return update_connection_command

    def delete_connection(self, *connections):
        """Delete connections.

        Args:
            *connections: One or more instances of :py:class:`streamsets.sdk.sch_models.Connection`.
        """
        for connection in connections:
            logger.info('Deleting connection %s ...', connection)
            self.api_client.delete_connection(connection_id=connection.id)

    def verify_connection(self, connection, library=None):
        """Verify connection.

        Args:
            connection (:py:class:`streamsets.sdk.sch_models.Connection`): Connection object.
            library (:py:`str`, optional): Specify the library to test against. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ConnectionVerificationResult`.
        """
        if not isinstance(connection, Connection):
            raise TypeError("`connection` should be of type streamsets.sdk.sch_models.`Connection`")

        if library is not None and not isinstance(library, str):
            raise TypeError("`library` should be of type `str`")

        logger.info('Running dynamic preview for %s type ...', type)

        # get verifier information
        library_definition = json.loads(connection.library_definition)
        executor_type = self.engines.get(id=connection.sdc_id).engine_type
        verifier_definitions_map = dict()
        for verifier_definition in library_definition['verifierDefinitions']:
            library_name = get_stage_library_display_name_from_library(
                stage_library_name=verifier_definition['library'],
                deployment_type=EXECUTOR_TO_DEPLOYMENT_MAP.get(executor_type),
            )
            verifier_definitions_map[library_name] = verifier_definition

        if library is not None and library not in verifier_definitions_map:
            raise ValueError(
                "Invalid library passed, please choose from the following options: {}".format(
                    list(verifier_definitions_map.keys())
                )
            )

        if library is None:
            library = list(verifier_definitions_map.keys())[0]

        # As configured by UI at https://git.io/JUkz8
        parameters = {
            'connection': {
                'configuration': connection.connection_definition.configuration._data[0],
                'connectionId': connection.id,
                'type': connection.connection_type,
                'verifierDefinition': verifier_definitions_map[library],
                'version': library_definition['version'],
            }
        }
        dynamic_preview_request = {
            'dynamicPreviewRequestJson': {
                'batches': 2,
                'batchSize': 100,
                'parameters': parameters,
                'skipLifecycleEvents': True,
                'skipTargets': False,
                'testOrigin': False,
                'timeout': 120 * 1000,  # 120 seconds
                'type': 'CONNECTION_VERIFIER',
            },
            'stageOutputsToOverrideJson': [],
        }
        sdc = self.data_collectors.get(id=connection.sdc_id)._instance
        validate_command = sdc.api_client.run_dynamic_pipeline_preview_for_connection(dynamic_preview_request)
        return ConnectionVerificationResult(validate_command.wait_for_validate().response.json())

    @property
    def environments(self):
        """environments.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Environments`.
        """
        return Environments(self, self.organization)

    def activate_environment(self, *environments, timeout_sec=DEFAULT_WAIT_FOR_STATUS_TIMEOUT):
        """Activate environments.

        Args:
            *environments: One or more instances of :py:class:`streamsets.sdk.sch_models.Environment`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command` or None.
        """
        environments = [
            environment for environment in environments if not isinstance(environment, NotImplementedEnvironment)
        ]
        if not environments:
            logger.info('No environments to activate. Returning')
            return
        environment_ids = [environment.environment_id for environment in environments]
        logger.info('Activating environments %s ...', environment_ids)
        activate_environments_command = self.api_client.enable_environments(environment_ids)

        activate_environment_exception = None
        for environment in environments:
            try:
                self.api_client.wait_for_environment_state_display_label(
                    environment_id=environment.environment_id, state_display_label='ACTIVE', timeout_sec=timeout_sec
                )
            except Exception as ex:
                # just log the exceptions and ultimately raise the last one.
                logger.debug(ex)
                activate_environment_exception = ex
            # Update :py:class:`streamsets.sdk.sch_models.Environment` with updated data.
            environment.refresh()

        if activate_environment_exception:
            raise activate_environment_exception
        return activate_environments_command

    def deactivate_environment(self, *environments):
        """Deactivate environments.

        Args:
            *environments: One or more instances of :py:class:`streamsets.sdk.sch_models.Environment`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        environments = [
            environment for environment in environments if not isinstance(environment, NotImplementedEnvironment)
        ]
        if not environments:
            logger.info('No environments to deactivate. Returning')
            return
        environment_ids = [environment.environment_id for environment in environments]
        logger.info('Deactivating environments %s ...', environment_ids)
        deactivate_environments_command = self.api_client.disable_environments(environment_ids)

        deactivate_environment_exception = None
        for environment in environments:
            try:
                self.api_client.wait_for_environment_state_display_label(
                    environment_id=environment.environment_id, state_display_label='DEACTIVATED'
                )
                # Update :py:class:`streamsets.sdk.sch_models.Environment` with updated Environment metadata.
            except Exception as ex:
                # just log the exceptions and ultimately raise the last one.
                logger.debug(ex)
                deactivate_environment_exception = ex
            # Update :py:class:`streamsets.sdk.sch_models.Environment` with updated data.
            environment.refresh()

        if deactivate_environment_exception:
            raise deactivate_environment_exception
        return deactivate_environments_command

    def add_environment(self, environment):
        """Add an environment.

        Args:
            environment (:py:class:`streamsets.sdk.sch_models.Environment`): Environment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding an environment %s ...', environment.environment_name)
        complete = isinstance(environment, SelfManagedEnvironment)
        data = {
            'name': environment._data['name'],
            'type': environment._data['type'],
            'allowSnapshotEngineVersions': environment._data['allowSnapshotEngineVersions'],
            'rawEnvironmentTags': environment._data['rawEnvironmentTags'],
        }
        command = self.api_client.create_environment(data, complete=complete)
        fetched_data = command.response.json()
        original_environment_data = environment._data
        try:
            # Update with updated Environment metadata.Note, this is not an overwrite. Rather it preserves
            # any relevant data which environment had it before create_environment command was issued.
            if isinstance(environment, AWSEnvironment):
                fields = [
                    'credentialsType',
                    'credentials',
                    'defaultInstanceProfileArn',
                    'defaultManagedIdentity',
                    'region',
                    'vpcId',
                    'securityGroupId',
                    'subnetIds',
                ]
                created_dict = {field: environment._data.get(field, None) for field in fields}
            elif isinstance(environment, AzureEnvironment):
                fields = [
                    'credentialsType',
                    'credentials',
                    'defaultResourceGroup',
                    'region',
                    'vpcId',
                    'securityGroupId',
                    'subnetId',
                ]
                created_dict = {field: environment._data.get(field, None) for field in fields}
            elif isinstance(environment, GCPEnvironment):
                fields = ['credentialsType', 'credentials', 'projectId', 'vpcId', 'vpcProjectId']
                created_dict = {field: environment._data.get(field, None) for field in fields}
            elif isinstance(environment, KubernetesEnvironment):
                fields = ['agent']
                created_dict = {field: environment._data.get(field, None) for field in fields}
            if not isinstance(environment, SelfManagedEnvironment):
                if created_dict.get('credentialsType'):
                    # Map  the user entered value to internal constant
                    ui_value_map = environment.get_ui_value_mappings()
                    created_dict['credentialsType'] = ui_value_map['credentialsType'][created_dict['credentialsType']]
                fetched_data.update(created_dict)

            environment._data = fetched_data
            command = self.update_environment(environment)
            # Update :py:class:`streamsets.sdk.sch_models.Environment` with updated Environment metadata.
            environment._data = command.response.json()
        except Exception as ex:
            logger.error(ex)
            self.delete_environment(environment)
            environment._data = original_environment_data
            raise ex
        return command

    def update_environment(self, environment, timeout_sec=DEFAULT_WAIT_FOR_STATUS_TIMEOUT):
        """Update an environment.

        Args:
            environment (:py:class:`streamsets.sdk.sch_models.Environment`): environment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not environment:
            logger.info('No environment to update. Returning')
            return
        elif isinstance(environment, NotImplementedEnvironment):
            raise NotImplementedError("Cannot update NotImplementedEnvironment")
        logger.info('Updating an environment %s ...', environment)
        is_env_complete = environment.complete()
        is_complete = is_env_complete if is_env_complete else 'undefined'
        command = self.api_client.update_environment(
            environment_id=environment.environment_id,
            body=environment._data,
            complete=is_complete,
            process_if_enabled=is_complete,
        )
        self.api_client.wait_for_environment_status(
            environment_id=environment.environment_id, status='OK', timeout_sec=timeout_sec
        )

        environment._data = self.environments.get(environment_id=environment.environment_id)._data
        return command

    def delete_environment(self, *environments):
        """Delete environments.

        Args:
            *environments: One or more instances of :py:class:`streamsets.sdk.sch_models.Environment`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        environments = [
            environment for environment in environments if not isinstance(environment, NotImplementedEnvironment)
        ]
        if not environments:
            logger.info('No environments to delete. Returning')
            return
        enabled_environments = [environment for environment in environments if environment.json_state == 'ENABLED']
        if enabled_environments:
            logger.info(
                'Since only deactivated environments can be deleted, deactivating environment %s ...',
                [environment.environment_name for environment in enabled_environments],
            )
            self.deactivate_environment(*enabled_environments)

        environment_ids = [environment.environment_id for environment in environments]
        logger.info('Deleting environments %s ...', [environment.environment_name for environment in environments])
        self.api_client.delete_environments(environment_ids)

    def get_kubernetes_apply_agent_yaml_command(self, environment):
        """Get install script for a Kubernetes environment.

        Args:
            environment (:py:class:`streamsets.sdk.sch_models.Environment`): Environment object.

        Returns:
            An instance of :obj:`str`.
        """
        command = self.api_client.get_kubernetes_apply_agent_yaml_command(environment.environment_id)
        # Returned response header has content-type: text/plain, which returns as bytes, hence decode them to a string.
        return command.response.content.decode('utf-8')

    def get_kubernetes_environment_yaml(self, environment):
        """Get the YAML file for a Kubernetes environment.

        Args:
            environment (:py:class:`streamsets.sdk.sch_models.Environment`): Environment for which the YAML file should
                                                                             be fetched.

        Returns:
            An instance of :py:obj:`str`.
        """
        if environment.environment_type != "KUBERNETES":
            raise TypeError("Can only fetch YAML for Kubernetes environments.")

        command = self.api_client.get_kubernetes_environment_agent_yaml(environment.environment_id)
        return command.response.content.decode('utf-8')

    def get_environment_builder(self, environment_type='SELF'):
        """Get an environment builder instance with which an environment can be created.

        Args:
            environment_type (:obj: `str`, optional) Valid values are 'AWS', 'GCP', 'KUBERNETES' and 'SELF'.
             Default ``'SELF'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.EnvironmentBuilder`.
        """
        # Update the CSPEnvironmentJson with the API definitions from Swagger.
        definitions = self._provisioning_api['definitions']
        properties = copy.deepcopy(definitions['CspEnvironmentJson']['properties'])
        if environment_type == 'AWS':
            properties.update(definitions['AwsCspEnvironmentJson']['allOf'][1]['properties'])
        elif environment_type == 'AZURE':
            properties.update(definitions['AzureCspEnvironmentJson']['allOf'][1]['properties'])
        elif environment_type == 'GCP':
            properties.update(definitions['GcpCspEnvironmentJson']['allOf'][1]['properties'])
        elif environment_type == 'KUBERNETES':
            properties.update(definitions['KubernetesCspEnvironmentJson']['allOf'][1]['properties'])
        environment = {property_: None for property_ in properties}
        environment.update({'type': environment_type})

        return EnvironmentBuilder(environment=environment, control_hub=self)

    @property
    def engine_versions(self):
        """Deployment engine version. The engine_versions and engine_configuration (Deployment) properties
           have the same object structure represented by DeploymentEngineConfiguration.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.DeploymentEngineConfiguration`.
        """
        return DeploymentEngineConfigurations(self)

    @property
    def deployments(self):
        """Deployments.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Deployments`.
        """
        return Deployments(self, self.organization)

    def clone_deployment(self, deployment, name=None, deployment_tags=None, engine_labels=None, engine_version=None):
        """Clone a deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.Deployment`): Deployment object.
            name (:obj:`str`, optional): Name of the new deployment. Default: ``None``.
            deployment_tags (:obj:`list`, optional): Tags to add to the cloned deployment. Default: ```None``.
            engine_labels (:obj:`list`, optional): Labels to assign to engines belonging to this deployment. Default: ``None``.
            engine_version (:obj:`str`, optional): Engine Version ID Default: ``None``.

        Returns:
            An instance of  :py:class:`streamsets.sdk.sch_models.Deployment`.
        """
        if name is None:
            name = "Clone of {}".format(deployment.deployment_name)

        clone_deployment_properties = self._provisioning_api['definitions']['CspCloneDeploymentJson']['properties']
        clone_body = {property_: None for property_ in clone_deployment_properties}
        clone_body.update(
            {
                'name': name,
                'engineVersionId': engine_version,
                'deploymentTags': deployment_tags,
                'engineLabels': engine_labels,
            }
        )
        command = self.api_client.clone_deployment(deployment_id=deployment.deployment_id, body=clone_body)
        return Deployment(command.response.json()['deployment'])

    def start_deployment(self, *deployments):
        """Start Deployments.

        Args:
            *deployments: One or more instances of :py:class:`streamsets.sdk.sch_models.Deployment`.
        """
        deployments = [deployment for deployment in deployments if not isinstance(deployment, NotImplementedDeployment)]
        if not deployments:
            logger.info('No deployments to start. Returning')
            return
        deployment_ids = [deployment.deployment_id for deployment in deployments]
        logger.info('Starting deployments %s ...', deployment_ids)
        enable_deployments_command = self.api_client.enable_deployments(deployment_ids)

        start_deployment_exception = None
        for deployment in deployments:
            try:
                self.api_client.wait_for_deployment_state_display_label(
                    deployment_id=deployment.deployment_id, state_display_label='ACTIVE'
                )
            except Exception as ex:
                # just log the exceptions and ultimately raise the last one.
                logger.debug(ex)
                start_deployment_exception = ex
            # Update :py:class:`streamsets.sdk.sch_models.deployment` with updated data.
            deployment.refresh()

        if start_deployment_exception:
            raise start_deployment_exception
        return enable_deployments_command

    def stop_deployment(self, *deployments):
        """Stop Deployments.

        Args:
            *deployments: One or more instances of :py:class:`streamsets.sdk.sch_models.Deployment`.
        """
        deployments = [deployment for deployment in deployments if not isinstance(deployment, NotImplementedDeployment)]
        if not deployments:
            logger.info('No deployments to stop. Returning')
            return
        deployment_ids = [deployment.deployment_id for deployment in deployments]
        logger.info('Stopping deployments %s ...', deployment_ids)
        stop_deployments_command = self.api_client.disable_deployments(deployment_ids)

        stop_deployment_exception = None
        for deployment in deployments:
            try:
                self.api_client.wait_for_deployment_state_display_label(
                    deployment_id=deployment.deployment_id, state_display_label='DEACTIVATED'
                )
            except Exception as ex:
                # just log the exceptions and ultimately raise the last one.
                logger.debug(ex)
                stop_deployment_exception = ex
            # Update :py:class:`streamsets.sdk.sch_models.deployment` with updated data.
            deployment.refresh()

        if stop_deployment_exception:
            raise stop_deployment_exception
        return stop_deployments_command

    def add_deployment(self, deployment):
        """Add a deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.Deployment`): Deployment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding a deployment %s ...', deployment.deployment_name)

        engine_type = deployment._data['engineType']
        engine_version = deployment._data['engineVersion']
        maybe_engine_build = deployment._data.get("engineBuild", None)
        scala_binary_version = deployment._data['scalaBinaryVersion']

        if engine_type == 'DC':
            # The engine_id is used only when engineBuild is not None.
            # Otherwise, it is set to None, not affecting the following query
            if maybe_engine_build:
                engine_build = maybe_engine_build
                engine_id = f'{engine_type}:{engine_version}::{engine_build}'
                logger.info('The deployment has version %s and build %s', engine_version, engine_build)
            else:
                engine_id = None

            engine_version_config = self.engine_versions.get(
                engine_type=engine_type, engine_version=engine_version, id=engine_id
            )
        elif engine_type == 'TF':
            # The engine_id is used only when engineBuild is not None.
            # Otherwise, it is set to None, not affecting the following query
            if maybe_engine_build:
                engine_build = maybe_engine_build
                engine_id = f'{engine_type}:{engine_version}:{scala_binary_version}:{engine_build}'
                logger.info('The deployment has version %s and build %s', engine_version, engine_build)
            else:
                engine_id = None

            engine_version_config = self.engine_versions.get(
                engine_type=engine_type,
                engine_version=engine_version,
                id=engine_id,
                scala_binary_version=scala_binary_version,
            )

        data = {
            'name': deployment._data['name'],
            'type': deployment._data['type'],
            'engineType': engine_type,
            'engineVersion': engine_version,
            'engineVersionId': engine_version_config.id,
            'envId': deployment._data['envId'],
            'scalaBinaryVersion': scala_binary_version,
            'rawDeploymentTags': deployment._data['rawDeploymentTags'],
        }
        command = self.api_client.create_deployment(data)
        fetched_data = command.response.json()
        original_deployment_data = deployment._data
        # Wrapped in a try/except in case something goes wrong we can delete the deployment
        try:
            # Fill up jvm_config: default jvm config with logic as defined at https://git.io/JD2nf
            engine_config = deployment._data['engineConfiguration']
            if engine_config['jvmConfig']:
                requested_jvm_config = engine_config['jvmConfig']
                # The part after or in the following takes care of the case,
                # if user specified some of the jvm_config and not all.
                jvm_config = {
                    'jvmMinMemory': requested_jvm_config.get('jvmMinMemory', None) or 1024,
                    'jvmMinMemoryPercent': requested_jvm_config.get('jvmMinMemoryPercent', None) or 50,
                    'jvmMaxMemory': requested_jvm_config.get('jvmMaxMemory', None) or 1024,
                    'jvmMaxMemoryPercent': requested_jvm_config.get('jvmMaxMemoryPercent', None) or 50,
                    'extraJvmOpts': requested_jvm_config.get('extraJvmOpts', None) or '',
                    'memoryConfigStrategy': requested_jvm_config.get('memoryConfigStrategy', None) or 'PERCENTAGE',
                }

            # Fill up stage_libs: default_stage_libs logic as defined at https://t.ly/ErQH
            if engine_config['stageLibs']:
                stage_libs = engine_config['stageLibs']
            elif engine_type == SDC_DEPLOYMENT_TYPE:
                stage_libs = DEFAULT_DATA_COLLECTOR_STAGE_LIBS
            elif engine_type == TRANSFORMER_DEPLOYMENT_TYPE:
                stage_libs = DEFAULT_TRANSFORMER_STAGE_LIBS

            # Process the stage_libs
            processed_stage_libs = [
                get_stage_library_name_from_display_name(
                    stage_library_display_name=lib,
                    deployment_type=engine_type,
                    deployment_engine_version=engine_version,
                )
                for lib in stage_libs
            ]

            # Fill up engine_labels
            engine_labels = engine_config['labels'] or [deployment._data['name']]
            # Fill up external_resource_source
            external_resource_source = engine_config['externalResourcesUri'] or ''
            # Fill up default advanced_configuration for the specified engine version
            response = self.api_client.get_engine_version(engine_version_config.id).response.json()
            fetched_data['engineConfiguration'].update(
                {
                    'advancedConfiguration': response['advancedConfiguration'],
                    'externalResourcesUri': external_resource_source,
                    'maxCpuLoad': engine_config.get('maxCpuLoad'),
                    'maxMemoryUsed': engine_config.get('maxMemoryUsed'),
                    'maxPipelinesRunning': engine_config.get('maxPipelinesRunning'),
                    'jvmConfig': jvm_config,
                    'labels': engine_labels,
                    'stageLibs': processed_stage_libs,
                    'scalaBinaryVersion': scala_binary_version,
                }
            )
            # Update with updated Deployment metadata. Note, this is not an overwrite. Rather it preserves
            # any relevant data which deployment had it before create_deployment command was issued.
            if isinstance(deployment, SelfManagedDeployment):
                fields = ['installType']
                created_dict = {
                    field: deployment._data.get(field, None)
                    for field in fields
                    if deployment._data.get(field, None) is not None
                }
                fetched_data.update(created_dict)
            elif isinstance(deployment, AzureVMDeployment):
                fields = [
                    'attachPublicIp',
                    'desiredInstances',
                    'managedIdentity',
                    'resourceGroup',
                    'resourceTags',
                    'sshKeyPairName',
                    'sshKeySource',
                    'vmSize',
                    'zones',
                ]
                created_dict = {field: deployment._data.get(field, None) for field in fields}
                if created_dict.get('sshKeySource'):
                    # Map  the user entered value to internal constant
                    ui_value_map = deployment.get_ui_value_mappings()
                    created_dict['sshKeySource'] = ui_value_map['sshKeySource'][created_dict['sshKeySource']]
                fetched_data.update(created_dict)
            elif isinstance(deployment, EC2Deployment):
                fields = [
                    'desiredInstances',
                    'instanceProfileArn',
                    'instanceType',
                    'resourceTags',
                    'sshKeyPairName',
                    'sshKeySource',
                    'trackingUrl',
                ]
                created_dict = {field: deployment._data.get(field, None) for field in fields}
                fetched_data.update(created_dict)
            elif isinstance(deployment, GCEDeployment):
                fields = [
                    'blockProjectSshKeys',
                    'desiredInstances',
                    'instanceServiceAccountEmail',
                    'machineType',
                    'tags',
                    'publicSshKey',
                    'region',
                    'trackingUrl',
                    'resourceLabels',
                    'zones',
                    'subnetwork',
                ]
                created_dict = {field: deployment._data.get(field, None) for field in fields}
                fetched_data.update(created_dict)
            elif isinstance(deployment, KubernetesDeployment):
                fields = [
                    'useSpotInstances',
                    'kubernetesLabels',
                    'memoryRequest',
                    'cpuRequest',
                    'memoryLimit',
                    'cpuLimit',
                    'yaml',
                    'advancedMode',
                    'hpa',
                    'hpaMinReplicas',
                    'hpaMaxReplicas',
                    'hpaTargetCPUUtilizationPercentage',
                ]
                created_dict = {field: deployment._data.get(field, None) for field in fields}
                fetched_data.update(created_dict)
            deployment._data = fetched_data
            command = self.update_deployment(deployment)
            # Update :py:class:`streamsets.sdk.sch_models.Deployment` with updated Deployment metadata.
            deployment._data = command.response.json()
        except Exception as ex:
            logger.error(ex)
            self.delete_deployment(deployment)
            deployment._data = original_deployment_data
            raise ex
        return command

    def update_deployment(self, deployment):
        """Update a deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.Deployment`): deployment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not deployment:
            logger.info('No deployment to update. Returning')
            return
        elif isinstance(deployment, NotImplementedDeployment):
            raise NotImplementedError("Cannot update NotImplementedDeployment")
        logger.info('Updating a deployment %s ...', deployment)
        is_env_complete = deployment.complete()
        is_complete = is_env_complete if is_env_complete else 'undefined'
        command = self.api_client.update_deployment(
            deployment_id=deployment.deployment_id,
            body=deployment._data,
            complete=is_complete,
            process_if_enabled=is_complete,
        )
        self.api_client.wait_for_deployment_status(deployment_id=deployment.deployment_id, status='OK')
        deployment._data = self.deployments.get(deployment_id=deployment.deployment_id)._data
        return command

    def delete_deployment(self, *deployments, stop=True):
        """Delete deployments.

        Args:
            *deployments (:py:class:`streamsets.sdk.sch_models.Deployment`): One or more deployments.
            stop (:obj:`bool`): Stop the deployment. Default ``True``.
        """
        deployments = [deployment for deployment in deployments if not isinstance(deployment, NotImplementedDeployment)]
        if not deployments:
            logger.info('No deployments to delete. Returning')
            return

        enabled_deployments = [deployment for deployment in deployments if deployment.json_state == 'ENABLED']
        if enabled_deployments:
            logger.info(
                'Since only disabled deployments can be deleted, disabling deployment %s ...',
                [deployment.deployment_name for deployment in enabled_deployments],
            )

        deployment_ids = [deployment.deployment_id for deployment in deployments]
        logger.info('Deleting deployments %s ...', [deployment.deployment_name for deployment in deployments])
        self.api_client.delete_deployments(deployment_ids, stop=stop)

        delete_deployment_exception = None
        for deployment in deployments:
            try:
                self.api_client.wait_for_deployment_status(deployment_id=deployment.deployment_id, status='DELETED')
            except Exception as ex:
                # just log the exceptions and ultimately raise the last one.
                logger.debug(ex)
                delete_deployment_exception = ex
        if delete_deployment_exception:
            raise delete_deployment_exception

    def lock_deployment(self, deployment):
        """Lock deployment.

        Args:
            deployment: An instance of :py:class:`streamsets.sdk.sch_models.Deployment`.
        """
        if not deployment:
            logger.info('No deployment to lock. Returning')
            return
        elif isinstance(deployment, NotImplementedDeployment):
            raise NotImplementedError("Cannot lock NotImplementedDeployment")
        logger.info('Locking deployment %s ...', deployment.deployment_id)
        lock_deployment_command = self.api_client.lock_deployment(deployment.deployment_id)

        # Update :py:class:`streamsets.sdk.sch_models.Deployment` with updated data.
        deployment.refresh()

        return lock_deployment_command

    def unlock_deployment(self, deployment):
        """Unlock deployment.

        Args:
            deployment: An instance of :py:class:`streamsets.sdk.sch_models.Deployment`.
        """
        if not deployment:
            logger.info('No deployment to unlock. Returning')
            return
        elif isinstance(deployment, NotImplementedDeployment):
            raise NotImplementedError("Cannot unlock NotImplementedDeployment")
        logger.info('Unlocking deployment %s ...', deployment.deployment_id)
        unlock_deployment_command = self.api_client.unlock_deployment(deployment.deployment_id)

        # Update :py:class:`streamsets.sdk.sch_models.Deployment` with updated data.
        deployment.refresh()

        return unlock_deployment_command

    def get_self_managed_deployment_install_script(
        self, deployment, install_mechanism='DEFAULT', install_type=None, java_version=None
    ):
        """Get install script for a Self Managed deployment.

        Args:
            deployment (:py:class:`streamsets.sdk.sch_models.Deployment`): deployment object.
            install_mechanism (:obj:`str`, optional): Possible values for install are "DEFAULT", "BACKGROUND" and
                                                      "FOREGROUND". Default: ``DEFAULT``
            install_type (:obj:`str`, optional): Possible values for install are "DOCKER", "TARBALL". Default: ``None``.
                                                 If not provided will use the value supplied via the deployment.
            java_version (:obj:`str`, optional): Java Development Kit Version to be used. Example: "8".
                                                 Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not isinstance(deployment, SelfManagedDeployment):
            raise TypeError("Deployment must be of type SelfManagedDeployment")

        return deployment.install_script(install_mechanism, install_type, java_version)

    def get_deployment_builder(self, deployment_type='SELF'):
        """Get a deployment builder instance with which a deployment can be created.

        Args:
            deployment_type (:obj: `str`, optional) Valid values are 'AWS', 'GCP' and 'SELF'. Default ``'SELF'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.DeploymentBuilder`.
        """
        # Update the CSPDeploymentJson with the API definitions from Swagger.
        definitions = self._provisioning_api['definitions']
        properties = copy.deepcopy(definitions['CspDeploymentJson']['properties'])
        if deployment_type == 'SELF':
            properties.update(definitions['SelfManagedCspDeploymentJson']['allOf'][1]['properties'])
        elif deployment_type == 'AZURE_VM':
            properties.update(definitions['AzureVmCspDeploymentJson']['allOf'][1]['properties'])
        elif deployment_type == 'EC2':
            properties.update(definitions['Ec2CspDeploymentJson']['allOf'][1]['properties'])
        elif deployment_type == 'GCE':
            properties.update(definitions['GceCspDeploymentJson']['allOf'][1]['properties'])
        elif deployment_type == 'KUBERNETES':
            kubernetes_definition = {
                'kubernetesLabels': {'type': 'string'},
                'memoryRequest': {'type': 'string'},
                'cpuRequest': {'type': 'string'},
                'memoryLimit': {'type': 'string'},
                'cpuLimit': {'type': 'string'},
                'yaml': {'type': 'string'},
                'advancedMode': {'type': 'boolean'},
                'hpa': {'type': 'boolean'},
                'hpaMinReplicas': {'type': 'integer', 'format': 'int32'},
                'hpaMaxReplicas': {'type': 'integer', 'format': 'int32'},
                'hpaTargetCPUUtilizationPercentage': {'type': 'integer', 'format': 'int32'},
            }
            properties.update(kubernetes_definition)
            # TODO: Remove this hardcode when UI support is included - TLKT-1283
            # properties.update(definitions['KubernetesCspDeploymentJson']['allOf'][1]['properties'])
        # get engine configuration definitions
        engine_config_properties = definitions['EngineConfigurationJson']['properties']
        # get jvm config definitions
        jvm_config_properties = definitions['EngineJvmConfigJson']['properties']

        deployment = {property_: None for property_ in properties}
        deployment.update({'type': deployment_type})
        deployment['engineConfiguration'] = {property_: None for property_ in engine_config_properties}
        deployment['engineConfiguration']['jvmConfig'] = {property_: None for property_ in jvm_config_properties}

        return DeploymentBuilder(deployment=deployment, control_hub=self)

    @property
    def metering_and_usage(self):
        """Metering and usage for the Organization. By default, this will return a report for the last 30 days of
        metering data. A report for a custom time window can be retrieved by indexing this object with a slice that
        contains a datetime object for the start (required) and stop (optional, defaults to datetime.now()).

            ex. metering_and_usage[datetime(2022, 1, 1):datetime(2022, 1, 14)]
                metering_and_usage[datetime.now() - timedelta(7):]

        Returns:
              An instance of :py:class:`streamsets.sdk.sch_models.MeteringUsage`
        """
        return MeteringUsage(self)

    @property
    def engines(self):
        return Engines(self)

    def _get_protection_policies(self, policy_type):
        """An internal function that returns a list of protection policies

        Args:
            policy_type (str): The type of policies to return (Read, Write)

        Returns:
            A list of :py:class:`streamsets.sdk.utils.SeekableList`
        """
        return self.protection_policies.get_all(default_setting=policy_type) + self.protection_policies.get_all(
            default_setting='Both'
        )

    def get_admin_tool(self, base_url, username, password):
        """Get ControlHub admin tool.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.AdminTool`.
        """
        return AdminTool(base_url, username, password)

    def wait_for_job_status(self, job, status, check_failures=False, timeout_sec=DEFAULT_WAIT_FOR_STATUS_TIMEOUT):
        """Block until a job reaches the desired status.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): The job instance.
            status (:py:obj:`str`): The desired status to wait for.
            check_failures (:obj:`bool`, optional): Flag to check for job exceptions. Default: False
            timeout_sec (:obj:`int`, optional): Timeout to wait for ``job`` to reach ``status``, in seconds.
                Default: :py:const:`streamsets.sdk.sch.DEFAULT_WAIT_FOR_STATUS_TIMEOUT`.

        Raises:
            TimeoutError: If ``timeout_sec`` passes without ``job`` reaching ``status``.
        """

        def condition():
            job.refresh()
            logger.debug('Job has current status %s ...', job.status)

            if check_failures and job.history[0].errorMessage:
                # job.history stores all the different status a job has been, they are sorted from newest to oldest. So
                # job.history[0] always holds the newest status. With the next loop we can parse the error message of
                # the newest status and know which error type got triggered if any.
                for error_type in STATUS_ERRORS.keys():
                    if error_type in job.history[0].errorMessage:
                        raise STATUS_ERRORS.get(error_type)({"message": job.history[0].errorMessage})

            return job.status == status

        def failure(timeout):
            raise TimeoutError(
                'Timed out after {} seconds waiting for Job `{}` to reach status {}'.format(
                    timeout, job.job_name, status
                )
            )

        wait_for_condition(condition=condition, timeout=timeout_sec, failure=failure)

    def wait_for_job_metrics_record_count(self, job, count, timeout_sec=DEFAULT_WAIT_FOR_METRIC_TIMEOUT):
        """Block until a job's metrics reaches the desired count.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): The job instance.
            count (:obj:`int`): The desired value to wait for.
            timeout_sec (:obj:`int`, optional): Timeout to wait for ``metric`` to reach ``count``, in seconds.
                Default: :py:const:`streamsets.sdk.sch.DEFAULT_WAIT_FOR_METRIC_TIMEOUT`.

        Raises:
            TimeoutError: If ``timeout_sec`` passes without ``metric`` reaching ``value``.
        """

        def condition():
            job.refresh()
            current_value = job.metrics(metric_type='RECORD_COUNT', include_error_count=True).output_count['PIPELINE']
            logger.debug('Waiting for job metric `%s` status to become `%s`', current_value, count)
            return current_value == count

        def failure(timeout):
            metric = job.metrics(metric_type='RECORD_COUNT', include_error_count=True).output_count['PIPELINE']
            raise TimeoutError(
                'Timed out after {} seconds waiting for Job metric `{}` to become {}'.format(timeout, metric, count)
            )

        wait_for_condition(condition=condition, timeout=timeout_sec, failure=failure)

    def wait_for_job_metric(self, job, metric, value, timeout_sec=DEFAULT_WAIT_FOR_METRIC_TIMEOUT):
        """Block until a job's realtime summary reaches the desired value for the desired metric.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): The job instance.
            metric (:py:obj:`str`): The desired metric (e.g. ``'output_record_count'`` or ``'input_record_count'``).
            value (:obj:`int`): The desired value to wait for.
            timeout (:obj:`int`, optional): Timeout to wait for ``metric`` to reach ``value``, in seconds.
                Default: :py:const:`streamsets.sdk.sch.DEFAULT_WAIT_FOR_METRIC_TIMEOUT`.

        Raises:
            TimeoutError: If ``timeout`` passes without ``metric`` reaching ``value``.
        """

        def condition():
            executor_type = job.executor_type if job.executor_type else SDC_EXECUTOR_TYPE
            if executor_type != SDC_EXECUTOR_TYPE:
                raise Exception('This method is not yet supported for job with executor type other than COLLECTOR')

            current_value = getattr(job.realtime_summary, metric)
            logger.debug('Job realtime summary %s has current value %s ...', metric, current_value)
            return current_value >= value

        def failure(timeout):
            raise TimeoutError(
                'Job realtime summary {} did not reach value {} after {} s.'.format(metric, value, timeout)
            )

        wait_for_condition(condition=condition, timeout=timeout_sec, failure=failure)

    @property
    def saql_saved_searches_pipeline(self):
        """Get SAQL Searches for type Pipeline.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.SAQLSearches`.
        """
        return SAQLSearches(self, SAQLSearch.PipelineType.PIPELINE)

    @property
    def saql_saved_searches_fragment(self):
        """Get SAQL Searches for type Fragment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.SAQLSearches`.
        """
        return SAQLSearches(self, SAQLSearch.PipelineType.FRAGMENT)

    @property
    def saql_saved_searches_job_instance(self):
        """Get SAQL Searches for type Job Instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.SAQLSearches`.
        """
        return SAQLSearches(self, SAQLSearch.JobType.JOB_INSTANCE)

    @property
    def saql_saved_searches_job_template(self):
        """Get SAQL Searches for type Job Template.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.SAQLSearches`.
        """
        return SAQLSearches(self, SAQLSearch.JobType.JOB_TEMPLATE)

    @property
    def saql_saved_searches_draft_run(self):
        """Get SAQL Searches for type Draft Run.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.SAQLSearches`.
        """
        return SAQLSearches(self, SAQLSearch.JobType.JOB_DRAFT_RUN)

    def get_saql_search_builder(self, saql_search_type, mode='BASIC'):
        """Get SAQL Search Builder.

        saql_search_type (:py:obj:`str`): Type of SAQL search object, limited to``'PIPELINE'`` or ``'FRAGMENT'``,
                              ``'JOB_INSTANCE'``, ``'JOB_TEMPLATE'``,``'JOB_SEQUENCE'``, '``JOB_RUN'`` and
                               ``'JOB_DRAFT_RUN'``.
        mode (:py:obj:`str`, optional): mode of SAQL Search. Default: ``'BASIC'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.SAQLSearchBuilder`.
        """
        if not SAQLSearch.PipelineType.has_value(saql_search_type) and not SAQLSearch.JobType.has_value(
            saql_search_type
        ):
            raise (
                ValueError(
                    '{} is an invalid saql_search_type, the accepted values are: '
                    'PIPELINE, FRAGMENT, JOB_INSTANCE, JOB_TEMPLATE and JOB_DRAFT_RUN.'.format(saql_search_type)
                )
            )

        if not SAQLSearch.ModeType.has_value(mode):
            raise (ValueError('{} is an invalid mode value, the accepted values are: BASIC and ADVANCED.'.format(mode)))

        saql_search = {
            "id": None,
            "creator": None,
            "name": None,
            "type": saql_search_type,
            "mode": mode,
            "createTime": None,
            "query": '',
        }

        return SAQLSearchBuilder(saql_search=saql_search, control_hub=self, mode=mode)

    def save_saql_search(self, saql_search):
        """Save a saql search query.

        Args:
            saql_search (:py:class:`streamsets.sdk.sch_models.SAQLSearch`): The SAQL Search object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not isinstance(saql_search, SAQLSearch):
            raise TypeError(
                "saql_search must be an instance of streamsets.sdk.sch_models.SAQLSearch."
                "Please use get_saql_search_builder to retrieve a builder instance."
            )

        saql_search_json = saql_search._data
        saql_search_type = saql_search_json['type']

        if SAQLSearch.PipelineType.has_value(saql_search_type):
            response = self.api_client.create_saql_pipeline_search(saql_search_json)
        elif SAQLSearch.JobType.has_value(saql_search_type):
            response = self.api_client.create_saql_job_search(saql_search_json)
        else:
            raise TypeError("SDK method for type: {} has not yet been implemented.".format(saql_search_type))

        if response.response.status_code == 200:
            saql_search._data = response.response.json()

        return response

    def remove_saql_search(self, saql_search):
        """Remove a saql search.

        Args:
            saql_search (:py:class:`streamsets.sdk.sch_models.SAQLSearch`): The SAQL Search object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not isinstance(saql_search, SAQLSearch):
            raise TypeError(
                "saql_search must be an instance of streamsets.sdk.sch_models.SAQLSearch."
                "Please use one of the saql_saved_searches to retrieve the desired SAQL Search."
            )

        saql_search_id, saql_search_type = saql_search._data['id'], saql_search._data['type']

        if SAQLSearch.PipelineType.has_value(saql_search_type):
            return self.api_client.remove_saql_pipeline_search(saql_search_id)
        elif SAQLSearch.JobType.has_value(saql_search_type):
            return self.api_client.remove_saql_job_search(saql_search_id)
        else:
            raise TypeError("SDK method for type: {} has not yet been implemented.".format(saql_search_type))

    def mark_saql_search_as_favorite(self, saql_search):
        """Marks a saql search as a favorite. In other words, it stars an existing search query.

        Args:
            saql_search (:py:class:`streamsets.sdk.sch_models.SAQLSearch`): The SAQL Search.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not isinstance(saql_search, SAQLSearch):
            raise TypeError(
                "saql_search must be an instance of streamsets.sdk.sch_models.SAQLSearch."
                "Please use one of the saql_saved_searches to retrieve the desired SAQL Search."
            )

        saql_search_id, saql_search_type = saql_search._data['id'], saql_search._data['type']

        if SAQLSearch.PipelineType.has_value(saql_search_type):
            response = self.api_client.create_saql_fav_pipeline(saql_search_id)
        elif SAQLSearch.JobType.has_value(saql_search_type):
            response = self.api_client.create_saql_fav_job(saql_search_id)
        else:
            raise TypeError("SDK method for type: {} has not yet been implemented.".format(saql_search_type))

        if response.response.status_code == 200:
            saql_search._data['favorite']['favorite'] = response.response.json()

        return response

    def update_saql_search(self, saql_search):
        """Update a saql search query.

        Args:
            saql_search (:py:class:`streamsets.sdk.sch_models.SAQLSearch`): The SAQL Search object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """

        if not isinstance(saql_search, SAQLSearch):
            raise TypeError(
                "saql_search must be an instance of streamsets.sdk.sch_models.SAQLSearch."
                "Please use one of the saql_saved_searches to retrieve the desired SAQL Search."
            )

        saql_search_json = saql_search._data
        saql_search_id, saql_search_type = saql_search_json['id'], saql_search_json['type']

        if SAQLSearch.PipelineType.has_value(saql_search_type):
            response = self.api_client.update_saql_pipeline_search(saql_search_id, saql_search_json)
        elif SAQLSearch.JobType.has_value(saql_search_type):
            response = self.api_client.update_saql_job_search(saql_search_id, saql_search_json)
        else:
            raise TypeError("SDK method for type: {} has not yet been implemented.".format(saql_search_type))

        if response.response.status_code == 200:
            saql_search._data = response.response.json()

        return response

    def check_snowflake_account_validation(self, token):
        """Check the status of a snowflake account validation process.

        Args:
            token (:obj:`str`): Token of the validation process.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if not isinstance(token, str):
            TypeError("The token parameter must be a string value")
        return self.api_client.validate_snowflake_account_status(token=token)

    def validate_snowflake_account(
        self, account_url, mode, snowflake_login_type, username, password=None, private_key=None
    ):
        """Start a snowflake account validation process.

        Args:
            account_url (:obj:`str`): Snowflake url where the account should exist.
            mode (:obj:`str`): Mode of the account. Possible values are "EDIT", "PUBLISHED" and "CURRENT_CRED".
            snowflake_login_type (:obj:`str`): Login type for the snowflake account. Possible values are "PASSWORD" and
                                                "PRIVATE_KEY".
            username (:obj:`str`): Username of the snowflake account.
            password (:obj:`str`, optional): Password of the snowflake account. Default: ``None``.
            private_key (:obj:`str`, optional): Private key of the snowflake account. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """

        class Modes(Enum):
            EDIT = 'EDIT'
            PUBLISHED = 'PUBLISHED'
            CURRENT_CRED = 'CURRENT_CRED'

            @classmethod
            def has_value(cls, value):
                return value in cls._member_names_

        class LoginTypes(Enum):
            PASSWORD = 'PASSWORD'
            PRIVATE_KEY = 'PRIVATE_KEY'

            @classmethod
            def has_value(cls, value):
                return value in cls._member_names_

        if not Modes.has_value(mode):
            raise ValueError(
                (f"The mode must be either {', '.join(Modes._member_names_[:-1])} or " f"{Modes._member_names_[-1]}")
            )
        if not LoginTypes.has_value(snowflake_login_type):
            raise ValueError(
                (
                    f"The snowflake_login_type must be either {', '.join(LoginTypes._member_names_[:-1])} or "
                    f"{LoginTypes._member_names_[-1]}"
                )
            )
        if not password and snowflake_login_type == LoginTypes.PASSWORD.value:
            raise ValueError(
                ("If the snowflake_login_type is PASSWORD a password needs to be set to start the " "validation")
            )
        if not private_key and snowflake_login_type == LoginTypes.PRIVATE_KEY.value:
            raise ValueError(
                ("If the snowflake_login_type is PRIVATE_KEY a private_key needs to be set to start the " "validation")
            )

        validate_snowflake_account_json = {
            'accountUrl': account_url,
            'mode': mode,
            'password': password or "",
            'privateKey': private_key or "",
            'snowflakeLoginType': snowflake_login_type,
            'username': username,
        }
        return self.api_client.validate_snowflake_account(body=validate_snowflake_account_json)
