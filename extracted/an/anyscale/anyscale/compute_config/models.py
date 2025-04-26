from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, DefaultDict, Dict, List, Optional, Union

from anyscale._private.models import ModelBase, ModelEnum


ResourceDict = Dict[str, float]
AdvancedInstanceConfigDict = Dict[str, Any]


def _validate_resource_dict(r: Optional[ResourceDict], *, field_name: str):
    if r is None:
        return

    if not isinstance(r, dict):
        raise TypeError(f"'{field_name}' must be a Dict[str, float], but got: {r}")

    for k, v in r.items():
        if not isinstance(k, str):
            raise TypeError(f"'{field_name}' keys must be strings, but got: {k}")
        if isinstance(v, (int, float)):
            if v < 0:
                raise ValueError(
                    f"'{field_name}' values must be >= 0, but got: '{k}: {v}'"
                )
        else:
            raise TypeError(
                f"'{field_name}' values must be floats, but got: '{k}: {v}'"
            )


def _validate_advanced_instance_config_dict(c: Optional[AdvancedInstanceConfigDict]):
    if c is None:
        return

    if not isinstance(c, dict) or not all(isinstance(k, str) for k in c):
        raise TypeError("'advanced_instance_config' must be a Dict[str, Any]")


@dataclass(frozen=True)
class CloudDeployment(ModelBase):
    """Cloud deployment selectors for a node group; one or more selectors may be passed to target a specific deployment from all of a cloud's deployments."""

    __doc_py_example__ = """
from anyscale.compute_config.models import CloudDeployment

cloud_deployment = CloudDeployment(
    provider="aws",
    region="us-west-2",
    machine_pool="machine-pool-name",
    id="cldrsrc_1234567890",
)
"""

    __doc_yaml_example__ = """
cloud_deployment:
  provider: aws
  region: us-west-2
  machine_pool: machine-pool-name
  id: cldrsrc_1234567890
"""

    provider: Optional[str] = field(
        default=None,
        metadata={"docstring": "Cloud provider name, e.g., `aws` or `gcp`."},
    )

    def _validate_provider(self, provider: Optional[str]):
        if provider is not None and not isinstance(provider, str):
            raise TypeError("'provider' must be a string.")

    region: Optional[str] = field(
        default=None,
        metadata={"docstring": "Cloud provider region, e.g., `us-west-2`."},
    )

    def _validate_region(self, region: Optional[str]):
        if region is not None and not isinstance(region, str):
            raise TypeError("'region' must be a string.")

    machine_pool: Optional[str] = field(
        default=None, metadata={"docstring": "Machine pool name."}
    )

    def _validate_machine_pool(self, machine_pool: Optional[str]):
        if machine_pool is not None and not isinstance(machine_pool, str):
            raise TypeError("'machine_pool' must be a string.")

    id: Optional[str] = field(
        default=None, metadata={"docstring": "Cloud deployment ID from cloud setup."}
    )

    def _validate_id(self, id: Optional[str]):  # noqa: A002
        if id is not None and not isinstance(id, str):
            raise TypeError("'id' must be a string.")


@dataclass(frozen=True)
class _NodeConfig(ModelBase):
    instance_type: str = field(
        metadata={
            "docstring": "Cloud provider instance type, e.g., `m5.2xlarge` on AWS or `n2-standard-8` on GCP."
        }
    )

    def _validate_instance_type(self, instance_type: str):
        if not isinstance(instance_type, str):
            raise TypeError("'instance_type' must be a string.")

    resources: Optional[ResourceDict] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Logical resources that will be available on this node. Defaults to match the physical resources of the instance type."
        },
    )

    def _validate_resources(self, resources: Optional[ResourceDict]):
        _validate_resource_dict(resources, field_name="resources")

    advanced_instance_config: Optional[AdvancedInstanceConfigDict] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Advanced instance configurations that will be passed through to the cloud provider.",
            "customer_hosted_only": True,
        },
    )

    def _validate_advanced_instance_config(
        self, advanced_instance_config: Optional[AdvancedInstanceConfigDict]
    ):
        _validate_advanced_instance_config_dict(advanced_instance_config)

    flags: Optional[Dict[str, Any]] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Node-level flags specifying advanced or experimental options.",
            "customer_hosted_only": False,
        },
    )

    def _validate_flags(self, flags: Optional[Dict[str, Any]]):
        if flags is None:
            return

        if not isinstance(flags, dict):
            raise TypeError("'flags' must be a dict")

    cloud_deployment: Union[CloudDeployment, Dict[str, str], None] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Cloud deployment selectors for a node group; one or more selectors may be passed to target a specific deployment from all of a cloud's deployments.",
            "customer_hosted_only": False,
        },
    )

    def _validate_cloud_deployment(
        self, cloud_deployment: Union[CloudDeployment, Dict[str, str], None]
    ) -> Optional[CloudDeployment]:
        if cloud_deployment is None:
            return None
        if isinstance(cloud_deployment, dict):
            cloud_deployment = CloudDeployment.from_dict(cloud_deployment)
        if not isinstance(cloud_deployment, CloudDeployment):
            raise TypeError(
                "'cloud_deployment' must be a CloudDeployment or corresponding dict"
            )
        return cloud_deployment


@dataclass(frozen=True)
class HeadNodeConfig(_NodeConfig):
    """Configuration options for the head node of a cluster."""

    __doc_py_example__ = """
from anyscale.compute_config.models import ComputeConfig, HeadNodeConfig

config = ComputeConfig(
    head_node=HeadNodeConfig(
        instance_type="m5.8xlarge",
    ),
)
"""

    __doc_yaml_example__ = """
head_node:
  instance_type: m5.8xlarge
"""


class MarketType(ModelEnum):
    """Market type of instances to use (on-demand vs. spot)."""

    ON_DEMAND = "ON_DEMAND"
    SPOT = "SPOT"
    PREFER_SPOT = "PREFER_SPOT"

    __docstrings__ = {
        ON_DEMAND: "Use on-demand instances only.",
        SPOT: "Use spot instances only.",
        PREFER_SPOT: (
            "Prefer to use spot instances, but fall back to on-demand if necessary. "
            "If on-demand instances are running and spot instances become available, "
            "the on-demand instances will be evicted and replaced with spot instances."
        ),
    }


@dataclass(frozen=True)
class WorkerNodeGroupConfig(_NodeConfig):
    """Configuration options for a worker node group in a cluster.

    Clusters can have multiple worker node groups that use different instance types or configurations.
    """

    __doc_py_example__ = """
from anyscale.compute_config.models import ComputeConfig, MarketType, WorkerNodeGroupConfig

config = ComputeConfig(
    worker_nodes=[
        WorkerNodeGroupConfig(
            instance_type="m5.8xlarge",
            min_nodes=5,
            max_nodes=5,
        ),
        WorkerNodeGroupConfig(
            instance_type="m5.4xlarge",
            min_nodes=1,
            max_nodes=10,
            market_type=MarketType.SPOT,
        ),
    ],
)
"""

    __doc_yaml_example__ = """
worker_nodes:
- instance_type: m5.8xlarge
  min_nodes: 5
  max_nodes: 5
- instance_type: m5.4xlarge
  min_nodes: 1
  max_nodes: 10
  market_type: SPOT
"""

    name: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Unique name of this worker group. Defaults to a human-friendly representation of the instance type."
        },
    )

    def _validate_name(self, name: Optional[str]) -> str:
        # Default name to the instance type if not specified.
        if name is None:
            name = self.instance_type

        if not isinstance(name, str):
            raise TypeError("'name' must be a string")
        if len(name) == 0:
            raise ValueError("'name' cannot be empty")

        return name

    min_nodes: int = field(
        default=0,
        metadata={
            "docstring": "Minimum number of nodes of this type that will be kept running in the cluster."
        },
    )

    def _validate_min_nodes(self, min_nodes: int):
        if not isinstance(min_nodes, int):
            raise TypeError("'min_nodes' must be an int")
        if min_nodes < 0:
            raise ValueError("'min_nodes' must be >= 0")

    max_nodes: int = field(
        default=10,
        metadata={
            "docstring": "Maximum number of nodes of this type that can be running in the cluster."
        },
    )

    def _validate_max_nodes(self, max_nodes: int):
        if not isinstance(max_nodes, int):
            raise TypeError("'max_nodes' must be an int")
        if max_nodes < 1:
            raise ValueError("'max_nodes' must be >= 1")
        if max_nodes < self.min_nodes:
            raise ValueError(f"'max_nodes' must be >= 'min_nodes' ({self.min_nodes})")

    market_type: Union[str, MarketType] = field(
        default=MarketType.ON_DEMAND,
        metadata={
            "docstring": "The type of instances to use (see `MarketType` enum values for details).",
            "customer_hosted_only": True,
        },
    )

    def _validate_market_type(self, market_type: Union[str, MarketType]) -> MarketType:
        if isinstance(market_type, str):
            # This will raise a ValueError if the market_type is unrecognized.
            market_type = MarketType(market_type)
        elif not isinstance(market_type, MarketType):
            raise TypeError("'market_type' must be a MarketType.")

        return market_type


@dataclass(frozen=True)
class ComputeConfig(ModelBase):
    """Configuration for instance types and cloud resources for a cluster."""

    __doc_py_example__ = """
from anyscale.compute_config.models import (
    ComputeConfig, HeadNodeConfig, MarketType, WorkerNodeGroupConfig
)

config = ComputeConfig(
    cloud="my-cloud",
    head_node=HeadNodeConfig(
        instance_type="m5.8xlarge",
    ),
    worker_nodes=[
        WorkerNodeGroupConfig(
            instance_type="m5.8xlarge",
            min_nodes=5,
            max_nodes=5,
        ),
        WorkerNodeGroupConfig(
            instance_type="m5.4xlarge",
            min_nodes=1,
            max_nodes=10,
            market_type=MarketType.SPOT,
        ),
    ],
)
"""

    __doc_yaml_example__ = """
cloud: my-cloud
zones: # (Optional) Defaults to to all zones in a region.
  - us-west-2a
  - us-west-2b
head_node:
  instance_type: m5.8xlarge
worker_nodes:
- instance_type: m5.8xlarge
  min_nodes: 5
  max_nodes: 5
  market_type: PREFER_SPOT # (Optional) Defaults to ON_DEMAND
- instance_type: g5.4xlarge
  min_nodes: 1
  max_nodes: 10
  market_type: SPOT # (Optional) Defaults to ON_DEMAND
min_resources: # (Optional) Defaults to no minimum.
  CPU: 1
  GPU: 1
  CUSTOM_RESOURCE: 0
max_resources: # (Optional) Defaults to no maximum.
  CPU: 6
  GPU: 10
  CUSTOM_RESOURCE: 10
enable_cross_zone_scaling: true # (Optional) Defaults to false.
advanced_instance_config: # (Optional) Defaults to no advanced configurations.
  # AWS specific configuration example
  BlockDeviceMappings:
    - DeviceName: DEVICE_NAME
      Ebs:
        VolumeSize: VOLUME_SIZE
        DeleteOnTermination: DELETE_ON_TERMINATION
  IamInstanceProfile:
    Arn: IAM_INSTANCE_PROFILE_ARN
  NetworkInterfaces:
    - SubnetId: SUBNET_ID
      Groups:
        - SECURITY_GROUP_ID
      AssociatePublicIpAddress: ASSOCIATE_PUBLIC_IP
  TagSpecifications:
    - ResourceType: RESOURCE_TYPE
      Tags:
        - Key: TAG_KEY
          Value: TAG_VALUE
  # GCP specific configuration example
  instance_properties:
    disks:
      - boot: BOOT_OPTION
        auto_delete: AUTO_DELETE_OPTION
        initialize_params:
          disk_size_gb: DISK_SIZE_GB
    service_accounts:
      - email: SERVICE_ACCOUNT_EMAIL
        scopes:
          - SCOPE_URL
    network_interfaces:
      - subnetwork: SUBNETWORK_URL
        access_configs:
          - type: ACCESS_CONFIG_TYPE
    labels:
      LABEL_KEY: LABEL_VALUE
"""

    cloud: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace)."
        },
    )

    def _validate_cloud(self, cloud: Optional[str]):
        if cloud is not None and not isinstance(cloud, str):
            raise TypeError("'cloud' must be a string")

    head_node: Union[HeadNodeConfig, Dict, None] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Configuration options for the head node of the cluster. Defaults to the cloud's default head node configuration."
        },
    )

    def _validate_head_node(
        self, head_node: Union[HeadNodeConfig, Dict, None]
    ) -> Optional[HeadNodeConfig]:
        if head_node is None:
            return None

        if isinstance(head_node, dict):
            head_node = HeadNodeConfig.from_dict(head_node)
        if not isinstance(head_node, HeadNodeConfig):
            raise TypeError(
                "'head_node' must be a HeadNodeConfig or corresponding dict"
            )

        return head_node

    worker_nodes: Optional[List[Union[WorkerNodeGroupConfig, Dict]]] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Configuration options for the worker nodes of the cluster. If not provided, worker nodes will be automatically selected based on logical resource requests. To use a head-node only cluster, pass `[]` here."
        },
    )

    def _validate_worker_nodes(
        self, worker_nodes: Optional[List[Union[WorkerNodeGroupConfig, Dict]]]
    ) -> Optional[List[WorkerNodeGroupConfig]]:
        if worker_nodes is None:
            return None

        if not isinstance(worker_nodes, list) or not all(
            isinstance(c, (dict, WorkerNodeGroupConfig)) for c in worker_nodes
        ):
            raise TypeError(
                "'worker_nodes' must be a list of WorkerNodeGroupConfigs or corresponding dicts"
            )

        duplicate_names = set()
        name_counts: DefaultDict[str, int] = defaultdict(int)
        worker_node_models: List[WorkerNodeGroupConfig] = []
        for node in worker_nodes:
            if isinstance(node, dict):
                node = WorkerNodeGroupConfig.from_dict(node)

            assert isinstance(node, WorkerNodeGroupConfig)
            worker_node_models.append(node)
            name = node.name
            assert name is not None
            name_counts[name] += 1
            if name_counts[name] > 1:
                duplicate_names.add(name)

        if duplicate_names:
            raise ValueError(
                f"'worker_nodes' names must be unique, but got duplicate names: {duplicate_names}"
            )

        return worker_node_models

    min_resources: Optional[ResourceDict] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Total minimum logical resources across all nodes in the cluster. Resources omitted from this field have no minimum.",
            "customer_hosted_only": False,
        },
    )

    def _validate_min_resources(self, min_resources: Optional[ResourceDict]):
        _validate_resource_dict(min_resources, field_name="min_resources")

    max_resources: Optional[ResourceDict] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Total maximum logical resources across all nodes in the cluster. Resources omitted from this field have no maximum.",
            "customer_hosted_only": False,
        },
    )

    def _validate_max_resources(self, max_resources: Optional[ResourceDict]):
        _validate_resource_dict(max_resources, field_name="max_resources")

    zones: Optional[List[str]] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Availability zones to consider for this cluster. Defaults to all zones in the cloud's region. By default all instances with user workloads scheduled on them will run in the same zone to save cost, unless `enable_cross_zone_scaling` is set.",
            "customer_hosted_only": True,
        },
    )

    def _validate_zones(self, zones: Optional[List[str]]):
        if zones is None:
            return
        if not isinstance(zones, list) or not all(isinstance(z, str) for z in zones):
            raise TypeError("'zones' must be a List[str]")
        if len(zones) == 0:
            raise ValueError(
                "'zones' must not be an empty list. Set `None` to default to all zones."
            )

    enable_cross_zone_scaling: bool = field(
        default=False,
        repr=False,
        metadata={
            "docstring": "Allow instances in the cluster to be run across multiple zones. This is recommended when running production services (for fault-tolerance in a zone failure scenario). It is not recommended for workloads that have a large amount of inter-zone communication due to the possibility of higher costs and degraded performance. When false, all instances with user workloads scheduled on them (e.g. all worker nodes in multi-node clusters) will run in the same zone to save cost.",
            "customer_hosted_only": True,
        },
    )

    def _validate_enable_cross_zone_scaling(self, enable_cross_zone_scaling: bool):
        if not isinstance(enable_cross_zone_scaling, bool):
            raise TypeError("'enable_cross_zone_scaling' must be a boolean")

    advanced_instance_config: Optional[AdvancedInstanceConfigDict] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Advanced instance configurations that will be passed through to the cloud provider.",
            "customer_hosted_only": True,
        },
    )

    def _validate_advanced_instance_config(
        self, advanced_instance_config: Optional[AdvancedInstanceConfigDict],
    ):
        _validate_advanced_instance_config_dict(advanced_instance_config)

    flags: Optional[Dict[str, Any]] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Cluster-level flags specifying advanced or experimental options.",
            "customer_hosted_only": False,
        },
    )

    def _validate_flags(self, flags: Optional[Dict[str, Any]]):
        if flags is None:
            return

        if not isinstance(flags, dict):
            raise TypeError("'flags' must be a dict")


@dataclass(frozen=True)
class ComputeConfigVersion(ModelBase):
    """Details of a created version of a compute config.

    Includes the config options and metadata such as the name, version, and ID.
    """

    __doc_py_example__ = """
import anyscale
from anyscale.compute_config.models import (
    ComputeConfigVersion
)

version: ComputeConfigVersion = anyscale.compute_config.get("my-compute-config")
"""

    __doc_cli_example__ = """\
$ anyscale compute-config get -n my-compute-config
name: my-compute-config:1
id: cpt_r4b4b3621rl3uggg7llj3mvme6
config:
  cloud: my-cloud
  head_node:
    instance_type: m5.8xlarge
  worker_nodes:
  - instance_type: m5.8xlarge
    min_nodes: 5
    max_nodes: 5
  - instance_type: m5.4xlarge
    min_nodes: 1
    max_nodes: 10
    market_type: SPOT
"""

    name: str = field(
        metadata={
            "docstring": "Name of the compute config including the version tag, i.e., 'name:version'."
        }
    )

    def _validate_name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("'name' must be a string.")

        if not name.count(":") == 1:
            raise ValueError("'name' must be in the format: '<name>:<version>'.")

    id: str = field(metadata={"docstring": "Unique ID of the compute config."})

    def _validate_id(self, id: str):  # noqa: A002
        if not isinstance(id, str):
            raise TypeError("'id' must be a string.")

    config: ComputeConfig = field(metadata={"docstring": "The compute configuration."},)

    def _validate_config(self, config: ComputeConfig):
        if not isinstance(config, ComputeConfig):
            raise TypeError("'config' must be a ComputeConfig")
