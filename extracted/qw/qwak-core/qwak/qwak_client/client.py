from datetime import timedelta
from functools import lru_cache
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from _qwak_proto.qwak.build.v1.build_pb2 import DESCRIPTOR
from qwak.clients.analytics.client import AnalyticsEngineClient
from qwak.clients.automation_management.client import AutomationsManagementClient
from qwak.clients.batch_job_management.client import BatchJobManagerClient
from qwak.clients.build_orchestrator.client import BuildFilter, BuildOrchestratorClient
from qwak.clients.data_versioning.client import DataVersioningManagementClient
from qwak.clients.data_versioning.data_tag_filter import DataTagFilter
from qwak.clients.deployment.client import DeploymentManagementClient
from qwak.clients.feature_store import FeatureRegistryClient
from qwak.clients.file_versioning.client import FileVersioningManagementClient
from qwak.clients.file_versioning.file_tag_filter import FileTagFilter
from qwak.clients.instance_template.client import InstanceTemplateManagementClient
from qwak.clients.model_management.client import ModelsManagementClient
from qwak.clients.project.client import ProjectsManagementClient
from qwak.exceptions import QwakException
from qwak.feature_store.feature_sets.batch import BatchFeatureSet
from qwak.inner.build_config.build_config_v1 import BuildConfigV1
from qwak.inner.tool import Auth0ClientBase
from qwak.model.base import QwakModel
from qwak.qwak_client.batch_jobs.execution import Execution
from qwak.qwak_client.batch_jobs.task import Task
from qwak.qwak_client.builds.build import Build
from qwak.qwak_client.builds.filters.metric_filter import MetricFilter
from qwak.qwak_client.builds.filters.parameter_filter import ParameterFilter
from qwak.qwak_client.data_versioning.data_tag import DataTag
from qwak.qwak_client.deployments.deployment import Deployment, EnvironmentAudienceRoute
from qwak.qwak_client.file_versioning.file_tag import FileTag
from qwak.qwak_client.models.model import Model
from qwak.qwak_client.models.model_metadata import ModelMetadata
from qwak.qwak_client.projects.project import Project

if TYPE_CHECKING:
    try:
        import pandas as pd
    except ImportError:
        pass


class QwakClient:
    """
    Comprehensive Qwak client to manage operations performed against the Qwak system.
    Acts as a wrapper and single entry point for the different Qwak clients - BatchClient,
    DeploymentClient, and more.
    """

    @lru_cache(maxsize=1)
    def _get_project_management(self):
        return ProjectsManagementClient()

    @lru_cache(maxsize=1)
    def _get_model_management(self):
        return ModelsManagementClient()

    @lru_cache(maxsize=1)
    def _get_build_orchestrator(self):
        return BuildOrchestratorClient()

    @lru_cache(maxsize=1)
    def _get_batch_job_manager(self):
        return BatchJobManagerClient()

    @lru_cache(maxsize=1)
    def _get_file_versioning_management(self):
        return FileVersioningManagementClient()

    @lru_cache(maxsize=1)
    def _get_data_versioning_management(self):
        return DataVersioningManagementClient()

    @lru_cache(maxsize=1)
    def _get_deployment_management(self):
        return DeploymentManagementClient()

    @lru_cache(maxsize=1)
    def _get_feature_registry_client(self):
        return FeatureRegistryClient()

    @lru_cache(maxsize=1)
    def _get_automations_client(self):
        return AutomationsManagementClient()

    @lru_cache(maxsize=1)
    def _get_analytics_engine(self):
        return AnalyticsEngineClient()

    @lru_cache(maxsize=1)
    def _get_instance_template_client(self):
        return InstanceTemplateManagementClient()

    @lru_cache(maxsize=1)
    def _get_auth_client(self, api_key):
        return Auth0ClientBase(api_key)

    def get_token(self, api_key: Optional[str] = None) -> str:
        """
        Retrieve a token by apy key.
        Use Cases:
        Default - from already configured (qwak configured) - conf file
        Support QWAK_API_KEY environment variable
        Get token for a specified API key
        Args:
            api_key (str): a key for token exchange
        Returns:
            str: a client token
        """
        client = self._get_auth_client(api_key)
        return client.get_token()

    def get_latest_build(
        self, model_id: str, build_status: str = "SUCCESSFUL"
    ) -> Optional[str]:
        """
        Get the latest build by its model ID.
        Optionally gets a build_status, by default filters on 'SUCCESSFUL'

        Args:
            model_id (str): The model ID
            build_status (str): build statuses to filter on. Valid values are 'SUCCESSFUL', 'IN_PROGRESS', 'FAILED'

        Returns:
             str: The build ID of the latest build according to the build status. None if no builds match the filter.

        """
        if (
            build_status
            not in DESCRIPTOR.enum_types_by_name["BuildStatus"].values_by_name
        ):
            raise QwakException(
                f"Invalid build status {build_status}. Valid options are 'SUCCESSFUL', 'IN_PROGRESS', 'FAILED'"
            )

        model = self._get_model_management().get_model(model_id=model_id)
        model_uuid = model.uuid

        builds = self._get_build_orchestrator().list_builds(model_uuid=model_uuid).build
        if not builds:
            return None

        builds = [
            build
            for build in builds
            if build.build_status
            == DESCRIPTOR.enum_types_by_name["BuildStatus"]
            .values_by_name[build_status]
            .number
        ]
        builds.sort(key=lambda r: r.audit.created_at.seconds)

        return builds[-1].buildId if builds else None

    def get_builds_by_tags(
        self,
        model_id: str,
        tags: List[str],
        match_any: bool = True,
        include_extra_tags: bool = True,
    ) -> List[Build]:
        """
        Get builds by its model ID and explicit tags

        Args:
            model_id (str): The model ID
            tags (List[str]): List of tags to filter by
            match_any (bool): Whether matching any tag is enough to return a build (default: True)
            include_extra_tags (bool): Whether builds are allowed to have more tags than the ones specified in the tags list (default: True)

        Returns:
             List[Build]: List of builds that contains the requested tags.

        """
        model = self._get_model_management().get_model(model_id=model_id)
        model_uuid = model.uuid

        builds_proto = (
            self._get_build_orchestrator()
            .list_builds(
                model_uuid=model_uuid,
                build_filter=BuildFilter(
                    tags=tags,
                    require_all_tags=not match_any,
                    include_extra_tags=include_extra_tags,
                ),
            )
            .build
        )

        builds = [Build.from_proto(build) for build in builds_proto]

        return builds if builds else None

    def get_build(self, build_id: str) -> Build:
        """
        Get builds by its build ID

        Args:
            build_id (str): The build ID

        Returns:
             Build: The requested build.

        """
        build_proto = self._get_build_orchestrator().get_build(build_id).build

        build = Build.from_proto(build_proto)

        if build:
            model_proto = self._get_model_management().get_model_by_uuid(
                model_uuid=build_proto.model_uuid
            )
            build.model_id = model_proto.model_id

        return build if build else None

    def list_builds(
        self,
        model_id: str,
        tags: List[str],
        filters: List[Union[MetricFilter, ParameterFilter]],
    ) -> List[Build]:
        """
        List builds by its model ID and explicit filters

        Args:
            model_id (str): The model ID
            tags (List[str]): List of tags to filter by
            filters (List[str]): List of metric and parameter filters

        Returns:
             List[Build]: List of builds that contains the requested filters.

        """
        model = self._get_model_management().get_model(model_id=model_id)
        model_uuid = model.uuid

        metric_filters = list()
        parameter_filters = list()

        for build_filter in filters:
            if isinstance(build_filter, MetricFilter):
                metric_filters.append(MetricFilter.to_proto(build_filter))
            else:
                parameter_filters.append(ParameterFilter.to_proto(build_filter))

        builds_proto = (
            self._get_build_orchestrator()
            .list_builds(
                model_uuid=model_uuid,
                build_filter=BuildFilter(
                    tags=tags,
                    metric_filters=metric_filters,
                    parameter_filters=parameter_filters,
                ),
            )
            .build
        )

        return [Build.from_proto(build) for build in builds_proto]

    def list_file_tags(
        self,
        model_id: str,
        build_id: str = "",
        filter: Optional[FileTagFilter] = None,
    ) -> List[FileTag]:
        """
        List file tags by its model ID

        Args:
            model_id (str): The model ID
            build_id (str): The build ID - optional.
                If not specified, returns all model file tags.
            filter (FileTagFilter): Filter list by - optional.
                value (str): The filter value.
                type (enum): The filter type - FILE_TAG_FILTER_TYPE_CONTAINS/FILE_TAG_FILTER_TYPE_PREFIX.
                If not specified, returns all model file tags.


        Returns:
             List[FileTag]: List of file tags with their specifications.

        """
        model_file_tags_proto = (
            self._get_file_versioning_management().get_model_file_tags(
                model_id=model_id,
                build_id=build_id,
                file_tag_filter=None if filter is None else filter.to_proto(),
            )
        )

        return [
            FileTag.from_proto(file_tag) for file_tag in model_file_tags_proto.file_tags
        ]

    def list_data_tags(
        self,
        model_id: str,
        build_id: str = "",
        filter: Optional[DataTagFilter] = None,
    ) -> List[DataTag]:
        """
        List data tags by its model ID

        Args:
            model_id (str): The model ID
            build_id (str): The build ID - optional.
                If not specified, returns all model data tags.
            filter (DataTagFilter): Filter list by - optional.
                value (str): The filter value.
                type (enum): The filter type - DATA_TAG_FILTER_TYPE_CONTAINS/DATA_TAG_FILTER_TYPE_PREFIX.
                If not specified, returns all model file tags.

        Returns:
             List[DataTag]: List of data tags with their specifications.

        """
        model_data_tags_proto = (
            self._get_data_versioning_management().get_model_data_tags(
                model_id=model_id,
                build_id=build_id,
                data_tag_filter=None if filter is None else filter.to_proto(),
            )
        )

        return [
            DataTag.from_proto(data_tag) for data_tag in model_data_tags_proto.data_tags
        ]

    def set_tag(self, build_id: str, tag: str) -> None:
        """
        Assign a tag to an existing build

        Args:
            build_id (str): The build ID
            tag (str): The tag to assign

        """
        self._get_build_orchestrator().register_tags(build_id=build_id, tags=[tag])

    def set_tags(self, build_id: str, tags: List[str]) -> None:
        """
        Assign a list of tags to an existing build

        Args:
            build_id (str): The build ID
            tags (List[str]): List of tags to assign
        """
        self._get_build_orchestrator().register_tags(build_id=build_id, tags=tags)

    def create_project(
        self,
        project_name: str,
        project_description: str,
        jfrog_project_key: Optional[str] = None,
    ) -> str:
        """
        Create project

        Args:
            project_name (str): The requested name
            project_description (str): The requested description
            jfrog_project_key (Optional[str]): The requested jfrog project key

        Returns:
             str: The project ID of the newly created project

        """
        project = self._get_project_management().create_project(
            project_name=project_name,
            project_description=project_description,
            jfrog_project_key=jfrog_project_key,
        )

        return project.project.project_id

    def get_project(self, project_id: str) -> Optional[Project]:
        """
        Get model by its project ID

        Args:
            project_id (str): The model ID

        Returns:
             Optional[Project]: Project by ID.

        """
        return Project.from_proto(
            self._get_project_management().get_project(project_id).project.spec
        )

    def list_projects(self) -> List[Project]:
        """
        List projects

        Returns:
             List[Project]: List of projects

        """
        projects_proto = self._get_project_management().list_projects().projects

        return [Project.from_proto(project) for project in projects_proto]

    def delete_project(self, project_id: str) -> None:
        """
        Delete project by its project ID

        Args:
            project_id (str): The project ID
        """
        return self._get_project_management().delete_project(project_id=project_id)

    def create_model(
        self,
        project_id: str,
        model_name: str,
        model_description: str,
        jfrog_project_key: Optional[str] = None,
    ) -> str:
        """
        Create model

        Args:
            project_id (str): The project ID to associate the model
            model_name (str): The requested name
            model_description (str): The requested description
            jfrog_project_key (Optional[str]): The jfrog project key

        Returns:
             str: The model ID of the newly created project

        """
        model = self._get_model_management().create_model(
            project_id=project_id,
            model_name=model_name,
            model_description=model_description,
            jfrog_project_key=jfrog_project_key,
        )

        return model.model_id

    def get_model(self, model_id: str) -> Optional[Model]:
        """
        Get model by its model ID

        Args:
            model_id (str): The model ID

        Returns:
             Optional[Model]: Model by ID.

        """
        return Model.from_proto(
            self._get_model_management().get_model(model_id=model_id)
        )

    def list_model_metadata(self, project_id: str) -> List[ModelMetadata]:
        """
        Lists metadata of all models in a project.
        Args:
            project_id (str): The project ID
        Returns:
            List[ModelMetadata]: List of model metadata
        """
        service_response = self._get_model_management().list_models_metadata(project_id)
        model_metadata_from_service = service_response.model_metadata

        result = []
        for metadata_source in model_metadata_from_service:
            model_metadata = ModelMetadata()

            model_metadata.model = Model.from_proto(metadata_source.model)
            model_metadata.deployed_builds = [
                Build.from_proto(build) for build in metadata_source.build
            ]
            model_metadata.deployments = [
                Deployment.from_proto(deployment)
                for deployment in metadata_source.deployment_details
            ]

            audience_routes = []
            for (
                env_id,
                env,
            ) in metadata_source.audience_routes_grouped_by_environment.items():
                for route in env.audience_routes:
                    audience_routes.append(
                        EnvironmentAudienceRoute.from_proto(route, env_id)
                    )

            model_metadata.audience_routes = audience_routes
            result.append(model_metadata)

        return result

    def list_models(self, project_id: str) -> List[Model]:
        """
        List models

        Args:
            project_id (str): The project ID to list models from

        Returns:
             List[Model]: List of models

        """
        models_proto = (
            self._get_model_management().list_models(project_id=project_id).models
        )

        return [Model.from_proto(model) for model in models_proto]

    def get_model_metadata(self, model_id: str) -> ModelMetadata:
        """
        Get model metadata by its model ID

        Args:
            model_id (str): The model ID

        Returns:
            Model metadata by ID.
        """
        service_response = self._get_model_management().get_model_metadata(model_id)
        model_metadata_from_service = service_response.model_metadata
        model_metadata = ModelMetadata()

        model_metadata.model = Model.from_proto(model_metadata_from_service.model)
        model_metadata.deployed_builds = [
            Build.from_builds_management(build)
            for build in model_metadata_from_service.build
        ]
        model_metadata.deployments = [
            Deployment.from_proto(deployment)
            for deployment in model_metadata_from_service.deployment_details
        ]

        audience_routes = []
        for (
            env_id,
            env,
        ) in model_metadata_from_service.audience_routes_grouped_by_environment.items():
            for route in env.audience_routes:
                audience_routes.append(
                    EnvironmentAudienceRoute.from_proto(env_id, route)
                )
        model_metadata.audience_routes = audience_routes

        return model_metadata

    def list_models_metadata(self, project_id: str) -> List[ModelMetadata]:
        """
        List models metadata

        Args:
            project_id (str): The project ID to list models metadata from

        Returns:
             List[ModelMetadata]: List of models metadata

        """
        models_metadata_proto = (
            self._get_model_management()
            .list_models_metadata(project_id=project_id)
            .model_metadata
        )

        return [
            ModelMetadata.from_proto(model_metadata)
            for model_metadata in models_metadata_proto
        ]

    def delete_model(self, model_id: str) -> None:
        """
        Delete model by its model ID

        Args:
            model_id (str): The model ID
        """
        return self._get_model_management().delete_model(
            project_id=self.get_model(model_id).project_id, model_id=model_id
        )

    def get_deployed_build_id_per_environment(
        self, model_id: str
    ) -> Optional[Dict[str, Dict[str, str]]]:
        """
        Get deployed build ID per environment by its model ID

        Args:
            model_id (str): The model ID

        Returns:
             Dict[str, str]: Map environment to deployed build ID. None if the model is not deployed.

        """
        model = self._get_model_management().get_model(model_id=model_id)
        model_uuid = model.uuid

        deployment_details = self._get_deployment_management().get_deployment_details(
            model_id=model_id, model_uuid=model_uuid
        )

        if not deployment_details:
            return None

        environment_to_deployment_details = (
            deployment_details.environment_to_deployment_details
        )

        return {
            env_id: {
                deployment.variation.name: deployment.build_id
                for deployment in v.deployments_details
            }
            for env_id, v in environment_to_deployment_details.items()
        }

    def run_analytics_query(
        self, query: str, timeout: timedelta = None
    ) -> "pd.DataFrame":
        """
        Runs a Qwak Analytics Query and returns the Pandas DataFrame with the results.

        Args:
            query (str): The query to run
            timeout (timedelta): The timeout for the query - optional.
                If not specified, the function will wait indefinitely.

        Returns:
            pd.DataFrame: The results of the query
        """
        try:
            import pandas as pd
        except ImportError:
            raise QwakException(
                "Missing Pandas dependency required for running an analytics query."
            )
        client = self._get_analytics_engine()
        url = client.get_analytics_data(query=query, timeout=timeout)
        return pd.read_csv(url)

    def list_feature_sets(self) -> List[BatchFeatureSet]:
        """
        List all feature sets

        Returns:
            List[FeatureSet]: List of feature sets
        """
        client = self._get_feature_registry_client()
        feature_set_protos = client.list_feature_sets().feature_families

        return [
            BatchFeatureSet._from_proto(
                feature_set.feature_set_definition.feature_set_spec
            )
            for feature_set in feature_set_protos
        ]

    def delete_feature_set(self, feature_set_name: str):
        """
        Delete a feature set

        Args:
            feature_set_name (str): The feature set name
        """
        client = self._get_feature_registry_client()
        feature_set_def = client.get_feature_set_by_name(
            feature_set_name=feature_set_name
        )
        if feature_set_def:
            client.delete_feature_set(
                feature_set_def.feature_set.feature_set_definition.feature_set_id
            )
        else:
            raise QwakException(f"Feature set named '{feature_set_name}' not found")

    def delete_featureset_version(self, featureset_name: str, version_number: int):
        """
        Delete a feature set version

        Args:
            featureset_name (str): The feature set name
            version_number (int): version number
        """
        client = self._get_feature_registry_client()

        client.delete_featureset_version(
            featureset_name=featureset_name, version_number=version_number
        )

    def set_featureset_active_version(self, featureset_name: str, version_number: int):
        """
        Set active feature set version

        Args:
            featureset_name (str): The feature set name
            version_number (int): version number
        """
        client = self._get_feature_registry_client()

        client.set_active_featureset_version(
            featureset_name=featureset_name, version_number=version_number
        )

    def delete_data_source(self, data_source_name: str):
        """
        Delete a data source

        Args:
            data_source_name (str): The data source name
        """
        client = self._get_feature_registry_client()
        data_source_def = client.get_data_source_by_name(
            data_source_name=data_source_name
        )
        if data_source_def:
            client.delete_data_source(
                data_source_def.data_source.data_source_definition.data_source_id
            )
        else:
            raise QwakException(f"Data source named '{data_source_name}' not found")

    def delete_entity(self, entity_name: str):
        """
        Delete an entity_name

        Args:
            entity_name (str): The entity name
        """
        client = self._get_feature_registry_client()
        entity_def = client.get_entity_by_name(entity_name=entity_name)
        if entity_def:
            client.delete_entity(entity_def.entity.entity_definition.entity_id)
        else:
            raise QwakException(f"Entity named '{entity_name}' not found")

    def trigger_batch_feature_set(self, feature_set_name):
        """
        Triggers a batch feature set ingestion job immediately.

        Args:
            feature_set_name (str): The feature set name
        """
        client = self._get_feature_registry_client()
        client.run_feature_set(feature_set_name=feature_set_name)

    def trigger_automation(self, automation_name):
        """
        Triggers an automation immediately.

        Args:
            automation_name (str): The automation name
        """
        client = self._get_automations_client()
        automation = client.get_automation_by_name(automation_name=automation_name)
        if not automation:
            raise QwakException(
                f"Could not find automation with given name '{automation_name}'"
            )
        client.run_automation(automation_id=automation.id)

    def build_model(
        self,
        model_id: str,
        main_module_path: str = ".",
        dependencies_file: Optional[str] = None,
        dependencies_list: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        instance: str = "small",
        gpu_compatible: bool = False,
        run_tests: bool = True,
        validate_build_artifact: bool = True,
        validate_build_artifact_timeout: Optional[int] = None,
        prebuilt_qwak_model: Optional[QwakModel] = None,
        base_image: Optional[str] = None,
        build_name: str = "",
    ):
        from qwak.qwak_client.build_api_helpers.trigger_build_api import (
            trigger_build_api,
        )

        config = BuildConfigV1()
        config.build_properties.model_id = model_id
        config.build_properties.build_name = build_name
        config.build_properties.model_uri.uri = main_module_path
        config.build_env.python_env.dependency_file_path = dependencies_file
        config.build_properties.tags = tags if tags else []
        config.build_env.remote.resources.instance = instance
        config.build_properties.gpu_compatible = gpu_compatible
        config.step.validate_build_artifact = validate_build_artifact
        config.step.tests = run_tests
        config.fetch_base_docker_image_name(
            self._get_build_orchestrator(), self._get_instance_template_client()
        )
        config.pre_built_model = prebuilt_qwak_model
        if validate_build_artifact_timeout:
            config.step.validate_build_artifact_timeout = (
                validate_build_artifact_timeout
            )
        if base_image:
            config.build_env.docker.base_image = base_image
        if dependencies_list:
            with TemporaryDirectory() as temporary_directory:
                requirements_filename = Path(temporary_directory) / "requirements.txt"
                with open(requirements_filename, "w") as temp_dependencies_file:
                    temp_dependencies_file.write("\n".join(dependencies_list))
                config.build_env.python_env.dependency_file_path = requirements_filename
                return trigger_build_api(config)
        else:
            return trigger_build_api(config)

    def list_executions(
        self,
        model_id: str,
        build_id: str = "",
    ) -> List[Execution]:
        """
        List batch executions by its model ID

        Args:
            model_id (str): The model ID
            build_id (str): The build ID - optional.
                If not specified, returns all model executions.


        Returns:
             List[Execution]: List of executions with their specifications.

        """
        model_executions_proto = self._get_batch_job_manager().list_batch_jobs(
            model_id=model_id,
            build_id=build_id,
        )

        return [
            Execution.from_proto(execution)
            for execution in model_executions_proto.batch_jobs
        ]

    def list_execution_tasks(
        self,
        execution_id: str,
    ) -> List[Task]:
        """
        List batch executions tasks by its job ID

        Args:
            execution_id (str): The execution ID


        Returns:
             List[Task]: List of execution tasks with their specifications.

        """
        model_execution_tasks_proto = (
            self._get_batch_job_manager().get_batch_job_details(
                job_id=execution_id,
            )
        )

        return [
            Task.from_proto(task)
            for task in model_execution_tasks_proto.batch_job.task_executions
        ]
