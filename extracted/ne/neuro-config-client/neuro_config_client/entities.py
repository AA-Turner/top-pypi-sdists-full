from __future__ import annotations

import abc
import enum
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import datetime, time, tzinfo
from decimal import Decimal

from yarl import URL

if sys.version_info >= (3, 9):
    from zoneinfo import ZoneInfo
else:
    # why not backports.zoneinfo: https://github.com/pganssle/zoneinfo/issues/125
    from backports.zoneinfo._zoneinfo import ZoneInfo


class NotificationType(str, enum.Enum):
    SUCCESS = "success"
    ERROR = "error"
    CLUSTER_UPDATING = "cluster_updating"
    CLUSTER_UPDATE_SUCCEEDED = "cluster_update_succeeded"
    CLUSTER_UPDATE_FAILED = "cluster_update_failed"


class CloudProviderType(str, enum.Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    ON_PREM = "on_prem"
    VCD_MTS = "vcd_mts"
    VCD_SELECTEL = "vcd_selectel"

    @property
    def is_vcd(self) -> bool:
        return self.startswith("vcd_")


@dataclass(frozen=True)
class CloudProviderOptions:
    type: CloudProviderType
    node_pools: list[NodePoolOptions]


@dataclass(frozen=True)
class VCDCloudProviderOptions(CloudProviderOptions):
    url: URL | None = None
    organization: str | None = None
    edge_name_template: str | None = None
    edge_external_network_name: str | None = None
    catalog_name: str | None = None
    storage_profile_names: list[str] | None = None


@dataclass(frozen=True)
class NodePoolOptions:
    machine_type: str
    cpu: float
    memory: int
    available_cpu: float | None = None
    available_memory: int | None = None
    nvidia_gpu: int | None = None
    nvidia_gpu_model: str | None = None


class NodeRole(str, enum.Enum):
    KUBERNETES = "kubernetes"
    PLATFORM = "platform"
    PLATFORM_JOB = "platform_job"


@dataclass(frozen=True)
class NodePool:
    name: str

    cpu: float
    available_cpu: float
    memory: int
    available_memory: int
    disk_size: int
    available_disk_size: int

    role: NodeRole = NodeRole.PLATFORM_JOB

    min_size: int = 0
    max_size: int = 1
    idle_size: int | None = None

    machine_type: str | None = None

    disk_type: str | None = None

    gpu: int | None = None  # Deprecated. Use nvidia_gpu instead
    gpu_model: str | None = None  # Deprecated. Use nvidia_gpu_model instead
    nvidia_gpu: int | None = None
    nvidia_gpu_model: str | None = None
    amd_gpu: int | None = None
    amd_gpu_model: str | None = None
    intel_gpu: int | None = None
    intel_gpu_model: str | None = None

    price: Decimal | None = None
    currency: str | None = None

    is_preemptible: bool | None = None

    zones: tuple[str, ...] | None = None

    cpu_min_watts: float = 0.0
    cpu_max_watts: float = 0.0


@dataclass(frozen=True)
class AddNodePoolRequest:
    name: str

    min_size: int
    max_size: int
    idle_size: int | None = None

    role: NodeRole = NodeRole.PLATFORM_JOB

    machine_type: str | None = None

    cpu: float | None = None
    available_cpu: float | None = None
    memory: int | None = None
    available_memory: int | None = None
    disk_type: str | None = None
    disk_size: int | None = None
    available_disk_size: int | None = None

    nvidia_gpu: int | None = None
    nvidia_gpu_model: str | None = None
    amd_gpu: int | None = None
    amd_gpu_model: str | None = None
    intel_gpu: int | None = None
    intel_gpu_model: str | None = None

    price: Decimal | None = None
    currency: str | None = None

    is_preemptible: bool | None = None

    zones: tuple[str, ...] | None = None

    cpu_min_watts: float | None = None
    cpu_max_watts: float | None = None


PutNodePoolRequest = AddNodePoolRequest


@dataclass(frozen=True)
class PatchNodePoolSizeRequest:
    min_size: int | None = None
    max_size: int | None = None
    idle_size: int | None = None


@dataclass(frozen=True)
class PatchNodePoolResourcesRequest:
    cpu: float
    available_cpu: float
    memory: int
    available_memory: int
    disk_size: int
    available_disk_size: int

    nvidia_gpu: int | None = None
    nvidia_gpu_model: str | None = None
    amd_gpu: int | None = None
    amd_gpu_model: str | None = None
    intel_gpu: int | None = None
    intel_gpu_model: str | None = None

    machine_type: str | None = None

    min_size: int | None = None
    max_size: int | None = None


@dataclass(frozen=True)
class StorageInstance:
    name: str
    size: int | None = None
    ready: bool = False


@dataclass(frozen=True)
class Storage:
    instances: Sequence[StorageInstance]


@dataclass(frozen=True)
class CloudProvider(abc.ABC):
    node_pools: Sequence[NodePool]
    storage: Storage | None

    @property
    @abc.abstractmethod
    def type(self) -> CloudProviderType:
        pass


@dataclass(frozen=True, repr=False)
class AWSCredentials:
    access_key_id: str
    secret_access_key: str = field(repr=False)


class EFSPerformanceMode(str, enum.Enum):
    GENERAL_PURPOSE = "generalPurpose"
    MAX_IO = "maxIO"


class EFSThroughputMode(str, enum.Enum):
    BURSTING = "bursting"
    PROVISIONED = "provisioned"


@dataclass(frozen=True)
class AWSStorage(Storage):
    description: str
    performance_mode: EFSPerformanceMode
    throughput_mode: EFSThroughputMode
    provisioned_throughput_mibps: int | None = None


@dataclass(frozen=True)
class AWSCloudProvider(CloudProvider):
    region: str
    zones: Sequence[str]
    credentials: AWSCredentials = field(repr=False)
    storage: AWSStorage | None
    vpc_id: str | None = None

    @property
    def type(self) -> CloudProviderType:
        return CloudProviderType.AWS


class ClusterLocationType(str, enum.Enum):
    ZONAL = "zonal"
    REGIONAL = "regional"


class GoogleFilestoreTier(str, enum.Enum):
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"


@dataclass(frozen=True)
class GoogleStorage(Storage):
    description: str
    tier: GoogleFilestoreTier


@dataclass(frozen=True)
class GoogleCloudProvider(CloudProvider):
    region: str
    zones: Sequence[str]
    project: str
    credentials: dict[str, str] = field(repr=False)
    location_type: ClusterLocationType = ClusterLocationType.ZONAL
    tpu_enabled: bool = False

    @property
    def type(self) -> CloudProviderType:
        return CloudProviderType.GCP


@dataclass(frozen=True)
class AzureCredentials:
    subscription_id: str
    tenant_id: str
    client_id: str
    client_secret: str = field(repr=False)


class AzureStorageTier(str, enum.Enum):
    STANDARD = "Standard"
    PREMIUM = "Premium"


class AzureReplicationType(str, enum.Enum):
    LRS = "LRS"
    ZRS = "ZRS"


@dataclass(frozen=True)
class AzureStorage(Storage):
    description: str
    tier: AzureStorageTier
    replication_type: AzureReplicationType


@dataclass(frozen=True)
class AzureCloudProvider(CloudProvider):
    region: str
    resource_group: str
    credentials: AzureCredentials
    virtual_network_cidr: str | None = None

    @property
    def type(self) -> CloudProviderType:
        return CloudProviderType.AZURE


@dataclass(frozen=True)
class KubernetesCredentials:
    ca_data: str
    token: str | None = field(repr=False, default=None)
    client_key_data: str | None = field(repr=False, default=None)
    client_cert_data: str | None = field(repr=False, default=None)


@dataclass(frozen=True)
class OnPremCloudProvider(CloudProvider):
    kubernetes_url: URL | None = None
    credentials: KubernetesCredentials | None = None

    @property
    def type(self) -> CloudProviderType:
        return CloudProviderType.ON_PREM


@dataclass(frozen=True)
class VCDCredentials:
    user: str
    password: str = field(repr=False)
    ssh_password: str = field(repr=False)


@dataclass(frozen=True)
class VCDStorage(Storage):
    description: str
    profile_name: str
    size: int


@dataclass(frozen=True)
class VCDCloudProvider(CloudProvider):
    _type: CloudProviderType
    url: URL
    organization: str
    virtual_data_center: str
    edge_name: str
    edge_public_ip: str
    edge_external_network_name: str
    catalog_name: str
    credentials: VCDCredentials

    @property
    def type(self) -> CloudProviderType:
        return self._type


@dataclass(frozen=True)
class NeuroAuthConfig:
    url: URL
    token: str = field(repr=False)


@dataclass(frozen=True)
class HelmRegistryConfig:
    url: URL
    username: str | None = None
    password: str | None = field(repr=False, default=None)


@dataclass(frozen=True)
class DockerRegistryConfig:
    url: URL
    username: str | None = None
    password: str | None = field(repr=False, default=None)
    email: str | None = None


@dataclass(frozen=True)
class GrafanaCredentials:
    username: str
    password: str = field(repr=False)


@dataclass(frozen=True)
class SentryCredentials:
    client_key_id: str
    public_dsn: URL
    sample_rate: float = 0.01


@dataclass(frozen=True)
class MinioCredentials:
    username: str
    password: str = field(repr=False)


@dataclass(frozen=True)
class EMCECSCredentials:
    """
    Credentials to EMC ECS (blob storage engine developed by vmware creators)
    """

    access_key_id: str
    secret_access_key: str = field(repr=False)
    s3_endpoint: URL
    management_endpoint: URL
    s3_assumable_role: str


@dataclass(frozen=True)
class OpenStackCredentials:
    account_id: str
    password: str = field(repr=False)
    endpoint: URL
    s3_endpoint: URL
    region_name: str


@dataclass(frozen=True)
class CredentialsConfig:
    neuro: NeuroAuthConfig
    neuro_helm: HelmRegistryConfig
    neuro_registry: DockerRegistryConfig
    grafana: GrafanaCredentials | None = None
    sentry: SentryCredentials | None = None
    docker_hub: DockerRegistryConfig | None = None
    minio: MinioCredentials | None = None
    emc_ecs: EMCECSCredentials | None = None
    open_stack: OpenStackCredentials | None = None


@dataclass(frozen=True)
class VolumeConfig:
    name: str
    size: int | None = None
    path: str | None = None
    credits_per_hour_per_gb: Decimal = Decimal(0)


@dataclass(frozen=True)
class StorageConfig:
    url: URL
    volumes: Sequence[VolumeConfig] = ()


@dataclass(frozen=True)
class RegistryConfig:
    url: URL


@dataclass(frozen=True)
class MonitoringConfig:
    url: URL


@dataclass(frozen=True)
class MetricsConfig:
    url: URL


@dataclass(frozen=True)
class SecretsConfig:
    url: URL


@dataclass(frozen=True)
class DisksConfig:
    url: URL
    storage_limit_per_user: int


@dataclass(frozen=True)
class BucketsConfig:
    url: URL
    disable_creation: bool = False


class ACMEEnvironment(str, enum.Enum):
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass(frozen=True)
class IngressConfig:
    acme_environment: ACMEEnvironment
    default_cors_origins: Sequence[str] = ()
    additional_cors_origins: Sequence[str] = ()


@dataclass(frozen=True)
class TPUResource:
    ipv4_cidr_block: str
    types: Sequence[str] = ()
    software_versions: Sequence[str] = ()


@dataclass(frozen=True)
class TPUPreset:
    type: str
    software_version: str


@dataclass(frozen=True)
class ResourcePreset:
    name: str
    credits_per_hour: Decimal
    cpu: float
    memory: int
    nvidia_gpu: int | None = None
    amd_gpu: int | None = None
    intel_gpu: int | None = None
    nvidia_gpu_model: str | None = None
    amd_gpu_model: str | None = None
    intel_gpu_model: str | None = None
    tpu: TPUPreset | None = None
    scheduler_enabled: bool = False
    preemptible_node: bool = False
    is_external_job: bool = False
    resource_pool_names: Sequence[str] = ()
    available_resource_pool_names: Sequence[str] = ()


@dataclass(frozen=True)
class ResourcePoolType:
    name: str
    min_size: int = 0
    max_size: int = 1
    idle_size: int = 0

    cpu: float = 1.0
    available_cpu: float = 1.0
    memory: int = 2**30  # 1gb
    available_memory: int = 2**30
    disk_size: int = 150 * 2**30  # 150gb
    available_disk_size: int = 150 * 2**30  # 150gb

    gpu: int | None = None  # Deprecated. Use nvidia_gpu instead
    gpu_model: str | None = None  # Deprecated. Use nvidia_gpu_model instead
    nvidia_gpu: int | None = None
    nvidia_gpu_model: str | None = None
    amd_gpu: int | None = None
    amd_gpu_model: str | None = None
    intel_gpu: int | None = None
    intel_gpu_model: str | None = None
    tpu: TPUResource | None = None

    price: Decimal = Decimal()
    currency: str | None = None

    is_preemptible: bool = False

    cpu_min_watts: float = 0.0
    cpu_max_watts: float = 0.0


@dataclass(frozen=True)
class Resources:
    cpu: float
    memory: int
    nvidia_gpu: int = 0
    amd_gpu: int = 0
    intel_gpu: int = 0


@dataclass(frozen=True)
class IdleJobConfig:
    name: str
    count: int
    image: str
    resources: Resources
    command: list[str] = field(default_factory=list)
    args: list[str] = field(default_factory=list)
    image_pull_secret: str | None = None
    env: dict[str, str] = field(default_factory=dict)
    node_selector: dict[str, str] = field(default_factory=dict)


@dataclass
class OrchestratorConfig:
    job_hostname_template: str
    job_internal_hostname_template: str | None
    job_fallback_hostname: str
    job_schedule_timeout_s: float
    job_schedule_scale_up_timeout_s: float
    is_http_ingress_secure: bool = True
    resource_pool_types: Sequence[ResourcePoolType] = ()
    resource_presets: Sequence[ResourcePreset] = ()
    allow_privileged_mode: bool = False
    allow_job_priority: bool = False
    pre_pull_images: Sequence[str] = ()
    idle_jobs: Sequence[IdleJobConfig] = ()


@dataclass
class PatchOrchestratorConfigRequest:
    job_hostname_template: str | None = None
    job_internal_hostname_template: str | None = None
    job_fallback_hostname: str | None = None
    job_schedule_timeout_s: float | None = None
    job_schedule_scale_up_timeout_s: float | None = None
    is_http_ingress_secure: bool | None = None
    resource_pool_types: Sequence[ResourcePoolType] | None = None
    resource_presets: Sequence[ResourcePreset] | None = None
    allow_privileged_mode: bool | None = None
    allow_job_priority: bool | None = None
    pre_pull_images: Sequence[str] | None = None
    idle_jobs: Sequence[IdleJobConfig] | None = None


@dataclass
class ARecord:
    name: str
    ips: Sequence[str] = ()
    dns_name: str | None = None
    zone_id: str | None = None
    evaluate_target_health: bool = False


@dataclass
class DNSConfig:
    name: str
    a_records: Sequence[ARecord] = ()


class ClusterStatus(str, enum.Enum):
    BLANK = "blank"
    DEPLOYING = "deploying"
    DESTROYING = "destroying"
    TESTING = "testing"
    DEPLOYED = "deployed"
    DESTROYED = "destroyed"
    FAILED = "failed"


@dataclass(frozen=True)
class EnergySchedulePeriod:
    # ISO 8601 weekday number (1-7)
    weekday: int
    start_time: time
    end_time: time


@dataclass(frozen=True)
class EnergySchedule:
    name: str
    periods: Sequence[EnergySchedulePeriod] = ()
    price_per_kwh: Decimal = Decimal("0")


@dataclass(frozen=True)
class EnergyConfig:
    co2_grams_eq_per_kwh: float = 0
    schedules: Sequence[EnergySchedule] = ()


@dataclass(frozen=True)
class AppsConfig:
    apps_hostname_templates: list[str]
    app_proxy_url: URL


@dataclass(frozen=True)
class Cluster:
    name: str
    status: ClusterStatus
    created_at: datetime
    timezone: tzinfo = ZoneInfo("UTC")
    platform_infra_image_tag: str | None = None
    cloud_provider: CloudProvider | None = None
    credentials: CredentialsConfig | None = None
    orchestrator: OrchestratorConfig | None = None
    storage: StorageConfig | None = None
    registry: RegistryConfig | None = None
    monitoring: MonitoringConfig | None = None
    secrets: SecretsConfig | None = None
    metrics: MetricsConfig | None = None
    dns: DNSConfig | None = None
    disks: DisksConfig | None = None
    buckets: BucketsConfig | None = None
    ingress: IngressConfig | None = None
    energy: EnergyConfig | None = None
    apps: AppsConfig | None = None


@dataclass(frozen=True)
class PatchClusterRequest:
    credentials: CredentialsConfig | None = None
    storage: StorageConfig | None = None
    registry: RegistryConfig | None = None
    orchestrator: PatchOrchestratorConfigRequest | None = None
    monitoring: MonitoringConfig | None = None
    secrets: SecretsConfig | None = None
    metrics: MetricsConfig | None = None
    disks: DisksConfig | None = None
    buckets: BucketsConfig | None = None
    ingress: IngressConfig | None = None
    dns: DNSConfig | None = None
    timezone: ZoneInfo | None = None
    energy: EnergyConfig | None = None
    apps: AppsConfig | None = None
