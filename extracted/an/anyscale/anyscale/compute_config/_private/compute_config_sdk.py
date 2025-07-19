from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple, Union

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.client.openapi_client.models import (
    Cloud,
    CloudDeploymentComputeConfig,
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
    MultiDeploymentComputeConfig,
    WorkerNodeGroupConfig,
)
from anyscale.sdk.anyscale_client.models import ClusterComputeConfig


# Used to explicitly make the head node unschedulable.
# We can't leave resources empty because the backend will fill in CPU and GPU
# to match the instance type hardware.
UNSCHEDULABLE_RESOURCES = Resources(cpu=0, gpu=0)


class PrivateComputeConfigSDK(BaseSDK):
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
                advanced_configurations_json=config.advanced_instance_config or None,
            )

        return api_model

    def _convert_worker_node_group_configs_to_api_models(
        self, configs: Optional[List[Union[Dict, WorkerNodeGroupConfig]]],
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
                advanced_configurations_json=config.advanced_instance_config or None,
            )
            api_models.append(api_model)

        return api_models

    def _convert_compute_config_to_api_model(
        self, compute_config: ComputeConfig
    ) -> CloudDeploymentComputeConfig:
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

        return CloudDeploymentComputeConfig(
            cloud_deployment=compute_config.cloud_deployment,
            allowed_azs=compute_config.zones,
            head_node_type=self._convert_head_node_config_to_api_model(
                compute_config.head_node,
                cloud=cloud,
                schedulable_by_default=(
                    not compute_config.worker_nodes
                    and not compute_config.auto_select_worker_config
                ),
            ),
            worker_node_types=self._convert_worker_node_group_configs_to_api_models(
                compute_config.worker_nodes,
            ),
            auto_select_worker_config=compute_config.auto_select_worker_config,
            flags=flags,
            advanced_configurations_json=compute_config.advanced_instance_config
            or None,
        )

    def create_compute_config(
        self, compute_config: ComputeConfig, *, name: Optional[str] = None
    ) -> Tuple[str, str]:
        """Register the provided compute config and return its internal ID."""

        if name is not None:
            _, version = parse_cluster_compute_name_version(name)
            if version is not None:
                raise ValueError(
                    "A version tag cannot be provided when creating a compute config. "
                    "The latest version tag will be generated and returned."
                )

        # Returns the default cloud if user-provided cloud is not specified (`None`).
        cloud_id = self.client.get_cloud_id(cloud_name=compute_config.cloud)  # type: ignore

        deployment_config = self._convert_compute_config_to_api_model(compute_config)

        compute_config_api_model = ComputeTemplateConfig(
            cloud_id=cloud_id,
            deployment_configs=[deployment_config],
            # For compatibility, continue setting the top-level fields.
            allowed_azs=deployment_config.allowed_azs,
            head_node_type=deployment_config.head_node_type,
            worker_node_types=deployment_config.worker_node_types,
            auto_select_worker_config=deployment_config.auto_select_worker_config,
            flags=deployment_config.flags,
            advanced_configurations_json=deployment_config.advanced_configurations_json
            or None,
        )

        full_name, compute_config_id = self.client.create_compute_config(
            compute_config_api_model, name=name
        )
        self.logger.info(f"Created compute config: '{full_name}'")
        ui_url = self.client.get_compute_config_ui_url(
            compute_config_id, cloud_id=cloud_id
        )
        self.logger.info(f"View the compute config in the UI: '{ui_url}'")
        return full_name, compute_config_id

    def create_multi_deployment_compute_config(
        self,
        compute_config: MultiDeploymentComputeConfig,
        *,
        name: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Register the provided multi-deployment compute config and return its internal ID."""
        if name is not None:
            _, version = parse_cluster_compute_name_version(name)
            if version is not None:
                raise ValueError(
                    "A version tag cannot be provided when creating a compute config. "
                    "The latest version tag will be generated and returned."
                )

        # Returns the default cloud if user-provided cloud is not specified (`None`).
        cloud_id = self.client.get_cloud_id(cloud_name=compute_config.cloud)  # type: ignore

        # Convert each compute config to the CloudDeploymentComputeConfig API model.
        assert compute_config.configs
        deployment_configs = []
        for config in compute_config.configs:
            assert isinstance(config, ComputeConfig)
            deployment_configs.append(self._convert_compute_config_to_api_model(config))
        default_config = deployment_configs[0]

        compute_config_api_model = ComputeTemplateConfig(
            cloud_id=cloud_id,
            deployment_configs=deployment_configs,
            # For compatibility, use the first deployment config to set the top-level fields.
            allowed_azs=default_config.allowed_azs,
            head_node_type=default_config.head_node_type,
            worker_node_types=default_config.worker_node_types,
            auto_select_worker_config=default_config.auto_select_worker_config,
            flags=default_config.flags,
            advanced_configurations_json=default_config.advanced_configurations_json
            or None,
        )
        full_name, compute_config_id = self.client.create_compute_config(
            compute_config_api_model, name=name
        )
        self.logger.info(f"Created compute config: '{full_name}'")

        # TODO(janet): add this back after the UI has been updated to support multi-deployment compute configs.
        # ui_url = self.client.get_compute_config_ui_url(
        #     compute_config_id, cloud_id=cloud_id
        # )
        # self.logger.info(f"View the compute config in the UI: '{ui_url}'")

        return full_name, compute_config_id

    def _convert_api_model_to_advanced_instance_config(
        self,
        api_model: Union[
            DecoratedComputeTemplateConfig, ComputeNodeType, WorkerNodeType
        ],
    ) -> Optional[Dict]:
        if api_model.advanced_configurations_json:
            return api_model.advanced_configurations_json

        # Only one of aws_advanced_configurations_json or gcp_advanced_configurations_json will be set.
        if api_model.aws_advanced_configurations_json:
            return api_model.aws_advanced_configurations_json
        if api_model.gcp_advanced_configurations_json:
            return api_model.gcp_advanced_configurations_json

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
        self, api_model: ComputeNodeType
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
                api_model,
            ),
            flags=flags or None,
            cloud_deployment=cloud_deployment,
        )

    def _convert_api_models_to_worker_node_group_configs(
        self, api_models: List[WorkerNodeType]
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

    def _convert_cloud_deployment_compute_config_api_model_to_compute_config(
        self, cloud_name: str, api_model: CloudDeploymentComputeConfig,
    ) -> ComputeConfig:
        worker_nodes = None
        if not api_model.auto_select_worker_config:
            if api_model.worker_node_types is not None:
                # Convert worker node types when they are present.
                worker_nodes = self._convert_api_models_to_worker_node_group_configs(
                    api_model.worker_node_types
                )
            else:
                # An explicit head-node-only cluster (no worker nodes configured).
                worker_nodes = []

        zones = None
        # NOTE(edoakes): the API returns '["any"]' if no AZs are passed in on the creation path.
        if api_model.allowed_azs not in [["any"], []]:
            zones = api_model.allowed_azs

        enable_cross_zone_scaling = False
        flags: Dict[str, Any] = deepcopy(api_model.flags) or {}
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
            cloud_deployment=api_model.cloud_deployment,
            zones=zones,
            advanced_instance_config=api_model.advanced_configurations_json or None,
            enable_cross_zone_scaling=enable_cross_zone_scaling,
            head_node=self._convert_api_model_to_head_node_config(
                api_model.head_node_type
            ),
            worker_nodes=worker_nodes,
            min_resources=min_resources,
            max_resources=max_resources or None,
            flags=flags,
        )

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

        configs = None
        if api_model_config.deployment_configs:
            configs = [
                self._convert_cloud_deployment_compute_config_api_model_to_compute_config(
                    cloud.name, config
                )
                for config in api_model_config.deployment_configs
            ]
            if len(configs) == 1:
                # If there's only one deployment config, return it directly.
                return ComputeConfigVersion(
                    name=f"{api_model.name}:{api_model.version}",
                    id=api_model.id,
                    config=configs[0],
                )
            return ComputeConfigVersion(
                name=f"{api_model.name}:{api_model.version}",
                id=api_model.id,
                multi_deployment_config=MultiDeploymentComputeConfig(
                    cloud=cloud.name, configs=configs,
                ),
            )

        # If there are no deployment configs, this is a compute config for a single cloud deployment - parse the top-level fields.

        worker_nodes = None
        if not api_model_config.auto_select_worker_config:
            if api_model_config.worker_node_types is not None:
                # Convert worker node types when they are present.
                worker_nodes = self._convert_api_models_to_worker_node_group_configs(
                    api_model_config.worker_node_types
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
                    api_model_config
                ),
                enable_cross_zone_scaling=enable_cross_zone_scaling,
                head_node=self._convert_api_model_to_head_node_config(
                    api_model_config.head_node_type
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
