from copy import deepcopy
from typing import Any, Dict, List, Optional, Union
import warnings

from anyscale._private.anyscale_client.common import AnyscaleClientInterface
from anyscale._private.models.model_base import ResultIterator
from anyscale._private.sdk.base_sdk import BaseSDK, Timer
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models.create_schedule import CreateSchedule
from anyscale.client.openapi_client.models.decorated_schedule import DecoratedSchedule
from anyscale.client.openapi_client.models.list_response_metadata import (
    ListResponseMetadata,
)
from anyscale.client.openapi_client.models.production_job_config import (
    ProductionJobConfig,
)
from anyscale.client.openapi_client.models.schedule_config import (
    ScheduleConfig as BackendScheduleConfig,
)
from anyscale.compute_config.models import (
    CloudDeployment,
    ComputeConfig,
    HeadNodeConfig,
    MarketType,
    MultiResourceComputeConfig,
    PhysicalResources as UserPhysicalResources,
    WorkerNodeGroupConfig,
)
from anyscale.job._private.job_sdk import PrivateJobSDK
from anyscale.job.models import JobConfig
from anyscale.schedule.models import ScheduleConfig, ScheduleState, ScheduleStatus
from anyscale.util import get_endpoint


logger = BlockLogger()

MAX_PAGE_SIZE = 50


class PrivateScheduleSDK(BaseSDK):
    def __init__(
        self,
        *,
        logger: Optional[BlockLogger] = None,
        client: Optional[AnyscaleClientInterface] = None,
        timer: Optional[Timer] = None,
    ):
        super().__init__(logger=logger, client=client, timer=timer)
        self._job_sdk = PrivateJobSDK(logger=self.logger, client=self.client)

    def apply(self, config: ScheduleConfig) -> str:
        job_config = config.job_config
        assert isinstance(job_config, JobConfig)

        # Add warning for max_retries default change
        if job_config.max_retries is None:
            warnings.warn(
                "The 'max_retries' option was not specified. The current default is 1, "
                "but this will change to 0 in a future release. To ensure consistent behavior, "
                "explicitly set 'max_retries' to your desired value.",
                UserWarning,
                stacklevel=3,  # Points to user's schedule.apply() call
            )
            job_config = job_config.options(max_retries=1)  # Apply current default

        name = job_config.name or self._job_sdk.get_default_name()

        compute_config_id, cloud_id = self._job_sdk.resolve_compute_config_and_cloud_id(
            compute_config=job_config.compute_config, cloud=job_config.cloud
        )

        project_id = self.client.get_project_id(
            parent_cloud_id=cloud_id, name=job_config.project
        )

        job_queue_config = None
        if job_config.job_queue_config is not None:
            job_queue_config = self._job_sdk.create_job_queue_config(
                job_config.job_queue_config
            )

        # Resolve connection names to IDs
        connection_ids = self._job_sdk.resolve_connection_ids(job_config.connections)

        schedule: DecoratedSchedule = self.client.apply_schedule(
            CreateSchedule(
                name=name,
                project_id=project_id,
                config=self._job_sdk.job_config_to_internal_prod_job_conf(
                    config=job_config,
                    name=name,
                    cloud_id=cloud_id,
                    compute_config_id=compute_config_id,
                    connection_ids=connection_ids,
                ),
                job_queue_config=job_queue_config,
                schedule=BackendScheduleConfig(
                    cron_expression=config.cron_expression, timezone=config.timezone,
                ),
            )
        )

        self.logger.info(f"Schedule '{name}' submitted, ID: '{schedule.id}'.")

        return schedule.id

    def _resolve_to_schedule_model(
        self,
        *,
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
    ) -> DecoratedSchedule:
        if name is None and id is None:
            raise ValueError("One of 'name' or 'id' must be provided.")

        if name is not None and id is not None:
            raise ValueError("Only one of 'name' or 'id' can be provided.")

        if id is not None and (cloud is not None or project is not None):
            raise ValueError("'cloud' and 'project' should only be used with 'name'.")

        model: Optional[DecoratedSchedule] = self.client.get_schedule(
            name=name, id=id, cloud=cloud, project=project,
        )

        if model is None:
            if name is not None:
                raise RuntimeError(f"Schedule with name '{name}' was not found.")
            else:
                raise RuntimeError(f"Schedule with ID '{id}' was not found.")

        return model

    def set_state(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        state: ScheduleState,
    ) -> str:
        schedule_model = self._resolve_to_schedule_model(
            name=name, id=id, cloud=cloud, project=project
        )
        is_paused = state == ScheduleState.DISABLED
        self.client.set_schedule_state(id=schedule_model.id, is_paused=is_paused)
        self.logger.info(f"Set schedule '{schedule_model.name}' to state {state}")
        return schedule_model.id

    def _schedule_model_to_status(self, model: DecoratedSchedule) -> ScheduleStatus:
        """Convert DecoratedSchedule to ScheduleStatus.

        Uses data from the backend response when available (build, compute_template, project)
        to avoid making additional API calls. Falls back to API calls for backward
        compatibility if these fields are not present.
        """
        # Use project from response if available (DecoratedSchedule includes MiniProject)
        project = None
        if hasattr(model, "project") and model.project is not None:
            if model.project.name != "default":
                project = model.project.name
        else:
            # Fallback for older backends that don't include project
            project_model = self.client.get_project(model.project_id)
            project = (
                project_model.name
                if project_model is not None and project_model.name != "default"
                else None
            )

        prod_job_config: ProductionJobConfig = model.config

        # Check if backend provides build, compute_template, and cloud fields
        # (after backend changes are deployed)
        has_build = hasattr(model, "build") and model.build is not None
        has_compute_template = (
            hasattr(model, "compute_template") and model.compute_template is not None
        )
        has_cloud = hasattr(model, "cloud") and model.cloud is not None

        if has_build and has_compute_template:
            # Use data from backend response - no additional API calls needed
            # Backward compatibility: replicate ImageURI.from_cluster_env_build
            # (use_image_alias=True) logic so the optimized path returns the same
            # image_uri format as the old API-call path.
            # TODO(praneethkaturi): Analyse whether the alias format
            # ("anyscale/image/{name}:{revision}") or the raw docker_image_name
            # is the correct value to surface to users, and consolidate.
            if (model.build.application_template_id or "").startswith(
                "DEFAULT_APP_CONFIG_ID"
            ):
                image_uri = model.build.docker_image_name
            else:
                image_uri = f"anyscale/image/{model.build.application_template_name}:{model.build.revision}"

            # Get cloud from backend response if available
            cloud = model.cloud.name if has_cloud else None

            # Check if compute config is anonymous with full_config available
            is_anonymous = getattr(model.compute_template, "anonymous", False)
            has_full_config = (
                getattr(model.compute_template, "full_config", None) is not None
            )

            if is_anonymous and has_full_config:
                # Convert full_config to ComputeConfig object (no API call needed)
                compute_config: Union[str, ComputeConfig] = (
                    self._convert_full_config_to_compute_config(
                        model.compute_template.full_config, cloud_name=cloud,
                    )
                )
            else:
                # Named config - use "name:version" string
                compute_config_name = model.compute_template.name
                if model.compute_template.version is not None:
                    compute_config_name += f":{model.compute_template.version}"
                compute_config = compute_config_name

            # Extract runtime_env fields (same as old path in job_sdk.py)
            runtime_env_config = (
                prod_job_config.runtime_env if prod_job_config else None
            )

            # Resolve connections from IDs if present
            connections = (
                self._job_sdk.resolve_connection_ids_to_configs(
                    prod_job_config.connection_ids
                )
                if prod_job_config and prod_job_config.connection_ids
                else None
            )

            job_config = JobConfig(
                name=model.name,
                image_uri=image_uri,
                compute_config=compute_config,
                cloud=cloud,
                entrypoint=prod_job_config.entrypoint if prod_job_config else None,
                requirements=runtime_env_config.pip if runtime_env_config else None,
                working_dir=runtime_env_config.working_dir
                if runtime_env_config
                else None,
                env_vars=runtime_env_config.env_vars if runtime_env_config else None,
                py_executable=runtime_env_config.py_executable
                if runtime_env_config
                else None,
                max_retries=prod_job_config.max_retries
                if prod_job_config
                and prod_job_config.max_retries is not None
                and prod_job_config.max_retries >= 0
                else None,
                project=project,
                connections=connections,
            )
        else:
            # Fallback to existing behavior (makes API calls for build_id and compute_config_id)
            job_config = self._job_sdk.prod_job_config_to_job_config(
                prod_job_config=prod_job_config, name=model.name, project=project
            )

        config = ScheduleConfig(
            job_config=job_config,
            cron_expression=model.schedule.cron_expression,
            timezone=model.schedule.timezone,
        )

        state = (
            ScheduleState.ENABLED
            if model.next_trigger_at is not None
            else ScheduleState.DISABLED
        )

        return ScheduleStatus(id=model.id, name=model.name, config=config, state=state)

    def _convert_api_model_to_advanced_instance_config(
        self, api_model: Any
    ) -> Optional[Dict]:
        """Convert API model's advanced instance config fields.

        Checks advanced_configurations_json, then aws/gcp variants.
        Uses truthy checks so empty dict {} returns None.
        Mirrors compute_config_sdk.py:431-446.
        """
        if getattr(api_model, "advanced_configurations_json", None):
            return api_model.advanced_configurations_json

        if getattr(api_model, "aws_advanced_configurations_json", None):
            return api_model.aws_advanced_configurations_json
        if getattr(api_model, "gcp_advanced_configurations_json", None):
            return api_model.gcp_advanced_configurations_json

        return None

    def _convert_api_model_to_resource_dict(
        self, resources: Any
    ) -> Optional[Dict[str, float]]:
        """Convert API Resources model to dict."""
        if resources is None:
            return None

        return {
            k: v
            for k, v in {
                "CPU": getattr(resources, "cpu", None),
                "GPU": getattr(resources, "gpu", None),
                "memory": getattr(resources, "memory", None),
                "object_store_memory": getattr(resources, "object_store_memory", None),
                **(getattr(resources, "custom_resources", None) or {}),
            }.items()
            if v is not None
        }

    def _convert_api_model_to_head_node_config(self, api_model: Any) -> HeadNodeConfig:
        """Convert API ComputeNodeType to HeadNodeConfig."""
        raw_flags = getattr(api_model, "flags", None)
        flags: Dict[str, Any] = deepcopy(raw_flags) if raw_flags else {}

        cloud_deployment_dict = flags.pop("cloud_deployment", None)
        cloud_deployment = (
            CloudDeployment.from_dict(cloud_deployment_dict)
            if cloud_deployment_dict
            else None
        )

        # Convert required_resources from API model to user-facing model
        required_resources = None
        if getattr(api_model, "required_resources", None) is not None:
            required_resources = UserPhysicalResources.from_dict(
                api_model.required_resources.to_dict()
            )

        return HeadNodeConfig(
            instance_type=api_model.instance_type,
            resources=self._convert_api_model_to_resource_dict(
                getattr(api_model, "resources", None)
            ),
            required_resources=required_resources,
            labels=getattr(api_model, "labels", None),
            required_labels=getattr(api_model, "required_labels", None),
            advanced_instance_config=self._convert_api_model_to_advanced_instance_config(
                api_model,
            ),
            flags=flags or None,
            cloud_deployment=cloud_deployment,
        )

    def _convert_api_models_to_worker_node_group_configs(
        self, api_models: List[Any]
    ) -> List[WorkerNodeGroupConfig]:
        """Convert API WorkerNodeType list to WorkerNodeGroupConfig list."""
        configs = []
        for api_model in api_models:
            if getattr(api_model, "use_spot", False) and getattr(
                api_model, "fallback_to_ondemand", False
            ):
                market_type = MarketType.PREFER_SPOT
            elif getattr(api_model, "use_spot", False):
                market_type = MarketType.SPOT
            else:
                market_type = MarketType.ON_DEMAND

            min_nodes = getattr(api_model, "min_workers", None)
            if min_nodes is None:
                min_nodes = 0

            max_nodes = getattr(api_model, "max_workers", None)
            if max_nodes is None:
                max_nodes = 10

            raw_flags = getattr(api_model, "flags", None)
            flags: Dict[str, Any] = deepcopy(raw_flags) if raw_flags else {}

            cloud_deployment_dict = flags.pop("cloud_deployment", None)
            cloud_deployment = (
                CloudDeployment.from_dict(cloud_deployment_dict)
                if cloud_deployment_dict
                else None
            )

            # Convert required_resources from API model to user-facing model
            required_resources = None
            if getattr(api_model, "required_resources", None) is not None:
                required_resources = UserPhysicalResources.from_dict(
                    api_model.required_resources.to_dict()
                )

            configs.append(
                WorkerNodeGroupConfig(
                    name=api_model.name,
                    instance_type=api_model.instance_type,
                    resources=self._convert_api_model_to_resource_dict(
                        getattr(api_model, "resources", None)
                    ),
                    required_resources=required_resources,
                    labels=getattr(api_model, "labels", None),
                    required_labels=getattr(api_model, "required_labels", None),
                    advanced_instance_config=self._convert_api_model_to_advanced_instance_config(
                        api_model,
                    ),
                    min_nodes=min_nodes,
                    max_nodes=max_nodes,
                    market_type=market_type,
                    flags=flags or None,
                    cloud_deployment=cloud_deployment,
                )
            )

        return configs

    def _convert_deployment_config_to_compute_config(
        self, dc: Any, cloud_name: Optional[str]
    ) -> ComputeConfig:
        """Convert a CloudDeploymentComputeConfig to CLI ComputeConfig.

        This handles compute configs that have deployment_configs, which include
        cloud_resource (cloud_deployment) information.
        Mirrors compute_config_sdk.py:562-609.
        """
        worker_nodes = None
        if not getattr(dc, "auto_select_worker_config", False):
            worker_node_types = getattr(dc, "worker_node_types", None)
            if worker_node_types is not None:
                worker_nodes = self._convert_api_models_to_worker_node_group_configs(
                    worker_node_types
                )
            else:
                worker_nodes = []

        zones = None
        allowed_azs = getattr(dc, "allowed_azs", None)
        if allowed_azs not in [["any"], [], None]:
            zones = allowed_azs

        enable_cross_zone_scaling = False
        raw_flags = getattr(dc, "flags", None)
        flags: Dict[str, Any] = deepcopy(raw_flags) if raw_flags else {}
        enable_cross_zone_scaling = flags.pop("allow-cross-zone-autoscaling", False)
        min_resources = flags.pop("min_resources", None)
        max_resources = flags.pop("max_resources", None)
        if max_resources is None:
            max_resources = {}
            max_cpus = flags.pop("max-cpus", None)
            if max_cpus:
                max_resources["CPU"] = max_cpus
            max_gpus = flags.pop("max-gpus", None)
            if max_gpus:
                max_resources["GPU"] = max_gpus

        return ComputeConfig(
            cloud=cloud_name,
            cloud_resource=getattr(dc, "cloud_deployment", None),
            zones=zones,
            advanced_instance_config=getattr(dc, "advanced_configurations_json", None)
            or None,
            enable_cross_zone_scaling=enable_cross_zone_scaling,
            head_node=self._convert_api_model_to_head_node_config(dc.head_node_type),
            worker_nodes=worker_nodes,
            min_resources=min_resources,
            max_resources=max_resources or None,
            flags=flags,
            auto_select_worker_config=getattr(dc, "auto_select_worker_config", False)
            or False,
        )

    def _convert_full_config_to_compute_config(
        self, full_config: Any, cloud_name: Optional[str]
    ) -> Union[ComputeConfig, MultiResourceComputeConfig]:
        """Convert backend ComputeTemplateConfig to CLI ComputeConfig.

        This is used for anonymous compute configs where the backend provides
        the full config data to avoid making additional API calls.
        """
        # Handle deployment_configs (sets cloud_resource, etc.)
        # Mirrors compute_config_sdk.py:622-641
        deployment_configs = getattr(full_config, "deployment_configs", None)
        if deployment_configs:
            configs = [
                self._convert_deployment_config_to_compute_config(dc, cloud_name)
                for dc in deployment_configs
            ]
            if len(configs) == 1:
                return configs[0]
            return MultiResourceComputeConfig(cloud=cloud_name, configs=configs)

        worker_nodes = None
        if not getattr(full_config, "auto_select_worker_config", False):
            worker_node_types = getattr(full_config, "worker_node_types", None)
            if worker_node_types is not None:
                worker_nodes = self._convert_api_models_to_worker_node_group_configs(
                    worker_node_types
                )
            else:
                # An explicit head-node-only cluster (no worker nodes configured).
                worker_nodes = []

        zones = None
        allowed_azs = getattr(full_config, "allowed_azs", None)
        if allowed_azs not in [["any"], [], None]:
            zones = allowed_azs

        enable_cross_zone_scaling = False
        raw_flags = getattr(full_config, "flags", None)
        flags: Dict[str, Any] = deepcopy(raw_flags) if raw_flags else {}
        enable_cross_zone_scaling = flags.pop("allow-cross-zone-autoscaling", False)
        min_resources = flags.pop("min_resources", None)
        max_resources = flags.pop("max_resources", None)
        if max_resources is None:
            max_resources = {}
            max_cpus = flags.pop("max-cpus", None)
            if max_cpus:
                max_resources["CPU"] = max_cpus
            max_gpus = flags.pop("max-gpus", None)
            if max_gpus:
                max_resources["GPU"] = max_gpus

        # Get advanced instance config
        advanced_instance_config = getattr(
            full_config, "advanced_configurations_json", None
        )
        if not advanced_instance_config:
            advanced_instance_config = getattr(
                full_config, "aws_advanced_configurations_json", None
            )
        if not advanced_instance_config:
            advanced_instance_config = getattr(
                full_config, "gcp_advanced_configurations_json", None
            )
        advanced_instance_config = advanced_instance_config or None

        return ComputeConfig(
            cloud=cloud_name,
            zones=zones,
            advanced_instance_config=advanced_instance_config,
            enable_cross_zone_scaling=enable_cross_zone_scaling,
            head_node=self._convert_api_model_to_head_node_config(
                full_config.head_node_type
            ),
            worker_nodes=worker_nodes,
            min_resources=min_resources,
            max_resources=max_resources or None,
            auto_select_worker_config=getattr(
                full_config, "auto_select_worker_config", False
            ),
            flags=flags,
        )

    def status(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> ScheduleStatus:
        schedule_model = self._resolve_to_schedule_model(
            name=name, id=id, cloud=cloud, project=project
        )
        return self._schedule_model_to_status(model=schedule_model)

    def trigger(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        schedule_model = self._resolve_to_schedule_model(
            name=name, id=id, cloud=cloud, project=project
        )
        self.client.trigger_schedule(id=schedule_model.id)
        self.logger.info(f"Triggered job for schedule '{schedule_model.name}'.")
        return schedule_model.id

    def delete(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        """Delete a schedule.

        If the schedule is active, it will be automatically paused before deletion.
        The schedule must have no active triggered jobs.

        Args:
            id: The schedule ID.
            name: The schedule name (requires cloud and project).
            cloud: Cloud name (required with name).
            project: Project name (required with name).

        Returns:
            The ID of the deleted schedule.
        """
        schedule_model = self._resolve_to_schedule_model(
            name=name, id=id, cloud=cloud, project=project
        )
        self.client.delete_schedule(schedule_id=schedule_model.id)
        self.logger.info(f"Schedule '{schedule_model.name}' deleted.")
        return schedule_model.id

    def url(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        """Get the web UI URL for a schedule.

        Args:
            id: The schedule ID.
            name: The schedule name (requires cloud and project).
            cloud: Cloud name (required with name).
            project: Project name (required with name).

        Returns:
            The URL string for viewing the schedule in the Anyscale console.
        """
        schedule_model = self._resolve_to_schedule_model(
            id=id, name=name, cloud=cloud, project=project
        )
        return get_endpoint(f"/scheduled-jobs/{schedule_model.id}")

    def list(  # noqa: PLR0913
        self,
        *,
        name: Optional[str] = None,
        schedule_id: Optional[str] = None,
        project: Optional[str] = None,
        cloud: Optional[str] = None,
        creator_id: Optional[str] = None,
        include_all_users: bool = False,
        page_size: Optional[int] = None,
        max_items: Optional[int] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> ResultIterator[ScheduleStatus]:
        """List schedules with filtering and pagination.

        Args:
            name: Filter by schedule name.
            schedule_id: Fetch a specific schedule by ID.
            project: Filter by project name.
            cloud: Filter by cloud name.
            creator_id: Filter by creator ID.
            include_all_users: Include schedules from all users.
            page_size: Number of items per page.
            max_items: Maximum total items to return.
            sort_field: Field to sort by (NAME, ID, CREATED_AT, NEXT_TRIGGER_AT).
            sort_order: Sort order (ASC or DESC).

        Returns a ResultIterator that lazily fetches pages of schedules.
        """
        # Validate page_size
        if page_size is not None and (page_size <= 0 or page_size > MAX_PAGE_SIZE):
            raise ValueError(f"page_size must be between 1 and {MAX_PAGE_SIZE}.")

        # If schedule_id provided, fetch single schedule
        if schedule_id is not None:
            schedule_model = self._resolve_to_schedule_model(id=schedule_id)
            status = self._schedule_model_to_status(model=schedule_model)

            def _fetch_single_page(token: Optional[str]):
                class SingleItemResponse:
                    results = [status] if token is None else []
                    metadata = ListResponseMetadata(total=1, next_paging_token=None)

                return SingleItemResponse()

            return ResultIterator(
                page_token=None,
                max_items=1,
                fetch_page=_fetch_single_page,
                parse_fn=lambda x: x,
            )

        # Resolve cloud and project IDs
        cloud_id = self.client.get_cloud_id(cloud_name=cloud) if cloud else None
        project_id = None
        if project:
            project_id = self.client.get_project_id(
                parent_cloud_id=cloud_id, name=project
            )

        # Auto-populate creator_id if not include_all_users and creator_id not specified
        resolved_creator_id = creator_id
        if not include_all_users and creator_id is None:
            user = self.client.get_user_info()
            resolved_creator_id = user.id if user else None

        def _fetch_page(token: Optional[str]):
            return self.client.list_schedules(
                name=name,
                project_id=project_id,
                cloud_id=cloud_id,
                creator_id=resolved_creator_id,
                count=page_size,
                paging_token=token,
                sort_field=sort_field,
                sort_order=sort_order,
            )

        def _parse_schedule(decorated_schedule: DecoratedSchedule) -> ScheduleStatus:
            return self._schedule_model_to_status(model=decorated_schedule)

        return ResultIterator(
            page_token=None,
            max_items=max_items,
            fetch_page=_fetch_page,
            parse_fn=_parse_schedule,
        )
