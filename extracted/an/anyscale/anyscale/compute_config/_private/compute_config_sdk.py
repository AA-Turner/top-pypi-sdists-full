from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple, Union

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.client.openapi_client.models import (
    Cloud,
    CloudProviders,
    ComputeNodeType,
    ComputeTemplateConfig,
    DecoratedComputeTemplate,
    DecoratedComputeTemplateConfig,
    Resources,
    WorkerNodeType,
)
from anyscale.cluster_compute import parse_cluster_compute_name_version
from anyscale.compute_config.models import (
    CloudDeployment,
    ComputeConfig,
    ComputeConfigVersion,
    HeadNodeConfig,
    MarketType,
    WorkerNodeGroupConfig,
)
from anyscale.sdk.anyscale_client.models import ClusterComputeConfig


# Used to explicitly make the head node unschedulable.
# We can't leave resources empty because the backend will fill in CPU and GPU
# to match the instance type hardware.
UNSCHEDULABLE_RESOURCES = Resources(cpu=0, gpu=0)


class PrivateComputeConfigSDK(BaseSDK):
    def _populate_advanced_instance_config(
        self,
        config: Union[ComputeConfig, HeadNodeConfig, WorkerNodeGroupConfig],
        api_model: Union[ComputeTemplateConfig, ComputeNodeType, WorkerNodeType],
        *,
        cloud: Cloud,
    ):
        """Populates the appropriate advanced instance config field of the API model in place."""
        if not config.advanced_instance_config:
            return

        # Always pass the advanced configuration through `advanced_configurations_json`.
        # After fully migrated, we can stop setting the cloud-specific advanced configurations here.
        api_model.advanced_configurations_json = config.advanced_instance_config

        if cloud.provider == CloudProviders.AWS:
            api_model.aws_advanced_configurations_json = config.advanced_instance_config
        elif cloud.provider == CloudProviders.GCP:
            api_model.gcp_advanced_configurations_json = config.advanced_instance_config

    def _convert_resource_dict_to_api_model(
        self, resource_dict: Optional[Dict[str, float]]
    ) -> Optional[Resources]:
        if resource_dict is None:
            return None

        resource_dict = deepcopy(resource_dict)
        return Resources(
            cpu=resource_dict.pop("CPU", None),
            gpu=resource_dict.pop("GPU", None),
            memory=resource_dict.pop("memory", None),
            object_store_memory=resource_dict.pop("object_store_memory", None),
            custom_resources=resource_dict or None,
        )

    def _convert_head_node_config_to_api_model(
        self,
        config: Union[None, Dict, HeadNodeConfig],
        *,
        cloud: Cloud,
        schedulable_by_default: bool,
    ) -> ComputeNodeType:
        if config is None:
            # If no head node config is provided, use the cloud default.
            default: ClusterComputeConfig = self._client.get_default_compute_config(
                cloud_id=cloud.id
            ).config

            api_model = ComputeNodeType(
                name="head-node",
                instance_type=default.head_node_type.instance_type,
                # Let the backend populate the physical resources
                # (regardless of what the default compute config says).
                resources=None if schedulable_by_default else UNSCHEDULABLE_RESOURCES,
                flags=default.flags,
            )
        else:
            # Make mypy happy.
            assert isinstance(config, HeadNodeConfig)

            flags: Dict[str, Any] = deepcopy(config.flags) if config.flags else {}
            if config.cloud_deployment:
                assert isinstance(config.cloud_deployment, CloudDeployment)
                flags["cloud_deployment"] = config.cloud_deployment.to_dict()

            api_model = ComputeNodeType(
                name="head-node",
                instance_type=config.instance_type,
                resources=self._convert_resource_dict_to_api_model(config.resources)
                if config.resources is not None or schedulable_by_default
                else UNSCHEDULABLE_RESOURCES,
                flags=flags or None,
            )
            self._populate_advanced_instance_config(
                config, api_model, cloud=cloud,
            )

        return api_model

    def _convert_worker_node_group_configs_to_api_models(
        self,
        configs: Optional[List[Union[Dict, WorkerNodeGroupConfig]]],
        *,
        cloud: Cloud,
    ) -> Optional[List[WorkerNodeType]]:
        if configs is None:
            return None

        api_models = []
        for config in configs:
            # Make mypy happy.
            assert isinstance(config, WorkerNodeGroupConfig)

            flags: Dict[str, Any] = deepcopy(config.flags) if config.flags else {}
            if config.cloud_deployment:
                assert isinstance(config.cloud_deployment, CloudDeployment)
                flags["cloud_deployment"] = config.cloud_deployment.to_dict()

            api_model = WorkerNodeType(
                name=config.name,
                instance_type=config.instance_type,
                resources=self._convert_resource_dict_to_api_model(config.resources),
                min_workers=config.min_nodes,
                max_workers=config.max_nodes,
                use_spot=config.market_type
                in {MarketType.SPOT, MarketType.PREFER_SPOT},
                fallback_to_ondemand=config.market_type == MarketType.PREFER_SPOT,
                flags=flags or None,
            )
            self._populate_advanced_instance_config(
                config, api_model, cloud=cloud,
            )
            api_models.append(api_model)

        return api_models

    def _convert_compute_config_to_api_model(
        self, compute_config: ComputeConfig
    ) -> ComputeTemplateConfig:
        # We should only make the head node schedulable when it's the *only* node in the cluster.
        # `worker_nodes=None` uses the default serverless config, so this only happens if `worker_nodes`
        # is explicitly set to an empty list.
        # Returns the default cloud if user-provided cloud is not specified (`None`).
        cloud_id = self.client.get_cloud_id(cloud_name=compute_config.cloud)  # type: ignore
        cloud = self.client.get_cloud(cloud_id=cloud_id)
        if cloud is None:
            raise RuntimeError(
                f"Cloud with ID '{cloud_id}' not found. "
                "This should never happen; please reach out to Anyscale support."
            )

        flags: Dict[str, Any] = deepcopy(
            compute_config.flags
        ) if compute_config.flags else {}
        flags["allow-cross-zone-autoscaling"] = compute_config.enable_cross_zone_scaling

        if compute_config.min_resources:
            flags["min_resources"] = compute_config.min_resources
        if compute_config.max_resources:
            flags["max_resources"] = compute_config.max_resources

        api_model = ComputeTemplateConfig(
            cloud_id=cloud_id,
            allowed_azs=compute_config.zones,
            region="",
            head_node_type=self._convert_head_node_config_to_api_model(
                compute_config.head_node,
                cloud=cloud,
                schedulable_by_default=compute_config.worker_nodes == [],
            ),
            worker_node_types=self._convert_worker_node_group_configs_to_api_models(
                compute_config.worker_nodes, cloud=cloud,
            ),
            auto_select_worker_config=compute_config.auto_select_worker_config,
            flags=flags,
        )
        self._populate_advanced_instance_config(
            compute_config, api_model, cloud=cloud,
        )
        return api_model

    def create_compute_config(
        self, compute_config: ComputeConfig, *, name: Optional[str] = None
    ) -> Tuple[str, str]:
        if name is not None:
            _, version = parse_cluster_compute_name_version(name)
            if version is not None:
                raise ValueError(
                    "A version tag cannot be provided when creating a compute config. "
                    "The latest version tag will be generated and returned."
                )

        """Register the provided compute config and return its internal ID."""
        compute_config_api_model = self._convert_compute_config_to_api_model(
            compute_config
        )
        full_name, compute_config_id = self.client.create_compute_config(
            compute_config_api_model, name=name
        )
        self.logger.info(f"Created compute config: '{full_name}'")
        ui_url = self.client.get_compute_config_ui_url(
            compute_config_id, cloud_id=compute_config_api_model.cloud_id
        )
        self.logger.info(f"View the compute config in the UI: '{ui_url}'")
        return full_name, compute_config_id

    def _convert_api_model_to_advanced_instance_config(
        self,
        api_model: Union[DecoratedComputeTemplate, ComputeNodeType, WorkerNodeType],
        *,
        cloud: Cloud,
    ) -> Optional[Dict]:
        if api_model.advanced_configurations_json:
            return api_model.advanced_configurations_json

        if cloud.provider == CloudProviders.AWS:
            return api_model.aws_advanced_configurations_json or None
        elif cloud.provider == CloudProviders.GCP:
            return api_model.gcp_advanced_configurations_json or None
        else:
            return None

    def _convert_api_model_to_resource_dict(
        self, resources: Optional[Resources]
    ) -> Optional[Dict[str, float]]:
        # Flatten the resource dict returned by the API and strip `None` values.
        if resources is None:
            return None

        return {
            k: v
            for k, v in {
                "CPU": resources.cpu,
                "GPU": resources.gpu,
                "memory": resources.memory,
                "object_store_memory": resources.object_store_memory,
                **(resources.custom_resources or {}),
            }.items()
            if v is not None
        }

    def _convert_api_model_to_head_node_config(
        self, api_model: ComputeNodeType, *, cloud: Cloud
    ) -> HeadNodeConfig:
        flags: Dict[str, Any] = deepcopy(api_model.flags) or {}

        cloud_deployment_dict = flags.pop("cloud_deployment", None)
        cloud_deployment = (
            CloudDeployment.from_dict(cloud_deployment_dict)
            if cloud_deployment_dict
            else None
        )

        return HeadNodeConfig(
            instance_type=api_model.instance_type,
            resources=self._convert_api_model_to_resource_dict(api_model.resources),
            advanced_instance_config=self._convert_api_model_to_advanced_instance_config(
                api_model, cloud=cloud,
            ),
            flags=flags or None,
            cloud_deployment=cloud_deployment,
        )

    def _convert_api_models_to_worker_node_group_configs(
        self, api_models: List[WorkerNodeType], *, cloud: Cloud
    ) -> List[WorkerNodeGroupConfig]:
        # TODO(edoakes): support advanced_instance_config.
        configs = []
        for api_model in api_models:
            if api_model.use_spot and api_model.fallback_to_ondemand:
                market_type = MarketType.PREFER_SPOT
            elif api_model.use_spot:
                market_type = MarketType.SPOT
            else:
                market_type = MarketType.ON_DEMAND

            min_nodes = api_model.min_workers
            if min_nodes is None:
                min_nodes = 0

            max_nodes = api_model.max_workers
            if max_nodes is None:
                # TODO(edoakes): this defaulting to 10 seems like really strange
                # behavior here but I'm copying what the UI does. In Shomil's new
                # API let's not make these optional.
                max_nodes = 10

            flags: Dict[str, Any] = deepcopy(api_model.flags) or {}

            cloud_deployment_dict = flags.pop("cloud_deployment", None)
            cloud_deployment = (
                CloudDeployment.from_dict(cloud_deployment_dict)
                if cloud_deployment_dict
                else None
            )

            configs.append(
                WorkerNodeGroupConfig(
                    name=api_model.name,
                    instance_type=api_model.instance_type,
                    resources=self._convert_api_model_to_resource_dict(
                        api_model.resources
                    ),
                    advanced_instance_config=self._convert_api_model_to_advanced_instance_config(
                        api_model, cloud=cloud,
                    ),
                    min_nodes=min_nodes,
                    max_nodes=max_nodes,
                    market_type=market_type,
                    flags=flags or None,
                    cloud_deployment=cloud_deployment,
                )
            )

        return configs

    def _convert_api_model_to_compute_config_version(
        self, api_model: DecoratedComputeTemplate  # noqa: ARG002
    ) -> ComputeConfigVersion:
        api_model_config: DecoratedComputeTemplateConfig = api_model.config
        cloud = self.client.get_cloud(cloud_id=api_model_config.cloud_id)
        if cloud is None:
            raise RuntimeError(
                f"Cloud with ID '{api_model_config.cloud_id}' not found. "
                "This should never happen; please reach out to Anyscale support."
            )

        worker_nodes = None
        if not api_model_config.auto_select_worker_config:
            if api_model_config.worker_node_types is not None:
                # Convert worker node types when they are present.
                worker_nodes = self._convert_api_models_to_worker_node_group_configs(
                    api_model_config.worker_node_types, cloud=cloud,
                )
            else:
                # An explicit head-node-only cluster (no worker nodes configured).
                worker_nodes = []

        zones = None
        # NOTE(edoakes): the API returns '["any"]' if no AZs are passed in on the creation path.
        if api_model_config.allowed_azs not in [["any"], []]:
            zones = api_model_config.allowed_azs

        enable_cross_zone_scaling = False
        flags: Dict[str, Any] = deepcopy(api_model_config.flags) or {}
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

        return ComputeConfigVersion(
            name=f"{api_model.name}:{api_model.version}",
            id=api_model.id,
            config=ComputeConfig(
                cloud=cloud.name,
                zones=zones,
                advanced_instance_config=self._convert_api_model_to_advanced_instance_config(
                    api_model_config, cloud=cloud,
                ),
                enable_cross_zone_scaling=enable_cross_zone_scaling,
                head_node=self._convert_api_model_to_head_node_config(
                    api_model_config.head_node_type, cloud=cloud
                ),
                worker_nodes=worker_nodes,  # type: ignore
                min_resources=min_resources,
                max_resources=max_resources or None,
                auto_select_worker_config=api_model_config.auto_select_worker_config,
                flags=flags,
            ),
        )

    def _resolve_id(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        include_archived: bool = False,
    ) -> str:
        if id is not None:
            compute_config_id = id
        elif name is not None:
            compute_config_id = self.client.get_compute_config_id(
                compute_config_name=name, cloud=cloud, include_archived=include_archived
            )
            if compute_config_id is None:
                raise RuntimeError(f"Compute config '{name}' not found.")
        else:
            raise ValueError("Either name or ID must be provided.")

        return compute_config_id

    def get_compute_config(
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        include_archived: bool = False,
    ) -> ComputeConfigVersion:
        """Get the compute config for the provided name.

        The name can contain an optional version, e.g., '<name>:<version>'.
        If no version is provided, the latest one will be returned.
        """
        compute_config_id = self._resolve_id(
            id=id, name=name, cloud=cloud, include_archived=include_archived
        )
        compute_config = self.client.get_compute_config(compute_config_id)
        if compute_config is None:
            raise RuntimeError(
                f"Compute config with ID '{compute_config_id}' not found.'"
            )
        return self._convert_api_model_to_compute_config_version(compute_config)

    def archive_compute_config(
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
    ):
        compute_config_id = self._resolve_id(id=id, name=name, cloud=cloud)
        self.client.archive_compute_config(compute_config_id=compute_config_id)
        self.logger.info("Compute config is successfully archived.")
