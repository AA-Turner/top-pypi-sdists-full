from __future__ import annotations

import sys
from dataclasses import replace
from datetime import datetime, time
from decimal import Decimal
from typing import Any
from unittest import mock

import pytest
from yarl import URL

from neuro_config_client.entities import (
    ACMEEnvironment,
    AddNodePoolRequest,
    AppsConfig,
    ARecord,
    AWSCloudProvider,
    AWSCredentials,
    AWSStorage,
    AzureCloudProvider,
    AzureCredentials,
    AzureReplicationType,
    AzureStorage,
    AzureStorageTier,
    BucketsConfig,
    CloudProviderOptions,
    CloudProviderType,
    Cluster,
    ClusterLocationType,
    ClusterStatus,
    CredentialsConfig,
    DisksConfig,
    DNSConfig,
    DockerRegistryConfig,
    EFSPerformanceMode,
    EFSThroughputMode,
    EMCECSCredentials,
    EnergyConfig,
    EnergySchedule,
    EnergySchedulePeriod,
    GoogleCloudProvider,
    GoogleFilestoreTier,
    GoogleStorage,
    GrafanaCredentials,
    HelmRegistryConfig,
    IdleJobConfig,
    IngressConfig,
    KubernetesCredentials,
    MetricsConfig,
    MinioCredentials,
    MonitoringConfig,
    NeuroAuthConfig,
    NodePool,
    NodePoolOptions,
    OnPremCloudProvider,
    OpenStackCredentials,
    OrchestratorConfig,
    PatchClusterRequest,
    PatchNodePoolResourcesRequest,
    PatchNodePoolSizeRequest,
    PatchOrchestratorConfigRequest,
    RegistryConfig,
    ResourcePoolType,
    ResourcePreset,
    Resources,
    SecretsConfig,
    SentryCredentials,
    StorageConfig,
    StorageInstance,
    TPUPreset,
    TPUResource,
    VCDCloudProvider,
    VCDCloudProviderOptions,
    VCDCredentials,
    VCDStorage,
    VolumeConfig,
)
from neuro_config_client.factories import EntityFactory, PayloadFactory

if sys.version_info >= (3, 9):
    from zoneinfo import ZoneInfo
else:
    # why not backports.zoneinfo: https://github.com/pganssle/zoneinfo/issues/125
    from backports.zoneinfo._zoneinfo import ZoneInfo


@pytest.fixture()
def nvidia_small_gpu() -> str:
    return "nvidia-tesla-k80"


@pytest.fixture()
def amd_small_gpu() -> str:
    return "instinct-mi25"


@pytest.fixture()
def intel_small_gpu() -> str:
    return "flex-170"


class TestEntityFactory:
    @pytest.fixture
    def factory(self) -> EntityFactory:
        return EntityFactory()

    def test_create_empty_cluster(self, factory: EntityFactory) -> None:
        result = factory.create_cluster(
            {"name": "default", "status": "blank", "created_at": str(datetime.now())}
        )

        assert result == Cluster(
            name="default", status=ClusterStatus.BLANK, created_at=mock.ANY
        )

    def test_create_cluster(
        self,
        factory: EntityFactory,
        google_cloud_provider_response: dict[str, Any],
        credentials: dict[str, Any],
    ) -> None:
        result = factory.create_cluster(
            {
                "name": "default",
                "status": "blank",
                "timezone": "America/Los_Angeles",
                "orchestrator": {
                    "job_hostname_template": "{job_id}.jobs-dev.neu.ro",
                    "job_fallback_hostname": "default.jobs-dev.neu.ro",
                    "job_schedule_timeout_s": 1,
                    "job_schedule_scale_up_timeout_s": 2,
                    "is_http_ingress_secure": False,
                    "resource_pool_types": [{"name": "node-pool"}],
                },
                "storage": {"url": "https://storage-dev.neu.ro"},
                "registry": {
                    "url": "https://registry-dev.neu.ro",
                    "email": "dev@neu.ro",
                },
                "monitoring": {"url": "https://monitoring-dev.neu.ro"},
                "secrets": {"url": "https://secrets-dev.neu.ro"},
                "metrics": {"url": "https://secrets-dev.neu.ro"},
                "disks": {
                    "url": "https://secrets-dev.neu.ro",
                    "storage_limit_per_user": 1024,
                },
                "ingress": {"acme_environment": "production"},
                "dns": {
                    "name": "neu.ro",
                    "a_records": [
                        {"name": "*.jobs-dev.neu.ro.", "ips": ["192.168.0.2"]}
                    ],
                },
                "cloud_provider": google_cloud_provider_response,
                "credentials": credentials,
                "created_at": str(datetime.now()),
            }
        )

        assert result.name == "default"
        assert result.status == ClusterStatus.BLANK
        assert result.timezone == ZoneInfo("America/Los_Angeles")
        assert result.orchestrator
        assert result.storage
        assert result.registry
        assert result.monitoring
        assert result.secrets
        assert result.metrics
        assert result.disks
        assert result.ingress
        assert result.dns
        assert result.cloud_provider
        assert result.credentials
        assert result.created_at

    def test_create_cluster__invalid_timezone(self, factory: EntityFactory) -> None:
        with pytest.raises(ValueError, match="invalid timezone"):
            factory.create_cluster(
                {
                    "name": "default",
                    "status": "blank",
                    "created_at": str(datetime.now()),
                    "timezone": "invalid",
                }
            )

    def test_create_orchestrator(self, factory: EntityFactory) -> None:
        result = factory.create_orchestrator(
            {
                "job_hostname_template": "{job_id}.jobs-dev.neu.ro",
                "job_internal_hostname_template": "{job_id}.platform-jobs",
                "job_fallback_hostname": "default.jobs-dev.neu.ro",
                "job_schedule_timeout_s": 1,
                "job_schedule_scale_up_timeout_s": 2,
                "is_http_ingress_secure": False,
                "resource_pool_types": [{"name": "node-pool"}],
                "resource_presets": [
                    {
                        "name": "cpu-micro",
                        "credits_per_hour": "10",
                        "cpu": 0.1,
                        "memory": 100,
                    }
                ],
                "allow_privileged_mode": True,
                "allow_job_priority": True,
                "pre_pull_images": ["neuromation/base"],
                "idle_jobs": [
                    {
                        "name": "idle",
                        "count": 1,
                        "image": "miner",
                        "resources": {
                            "cpu": 1,
                            "memory": 1024,
                            "nvidia_gpu": 1,
                            "amd_gpu": 2,
                            "intel_gpu": 3,
                        },
                    },
                    {
                        "name": "idle",
                        "count": 1,
                        "image": "miner",
                        "command": ["bash"],
                        "args": ["-c", "sleep infinity"],
                        "resources": {"cpu": 1, "memory": 1024},
                        "env": {"NAME": "VALUE"},
                        "node_selector": {"label": "value"},
                        "image_pull_secret": "secret",
                    },
                ],
            }
        )

        assert result == OrchestratorConfig(
            job_hostname_template="{job_id}.jobs-dev.neu.ro",
            job_internal_hostname_template="{job_id}.platform-jobs",
            job_fallback_hostname="default.jobs-dev.neu.ro",
            job_schedule_timeout_s=1,
            job_schedule_scale_up_timeout_s=2,
            is_http_ingress_secure=False,
            resource_pool_types=[mock.ANY],
            resource_presets=[mock.ANY],
            allow_privileged_mode=True,
            allow_job_priority=True,
            pre_pull_images=["neuromation/base"],
            idle_jobs=[
                IdleJobConfig(
                    name="idle",
                    count=1,
                    image="miner",
                    resources=Resources(
                        cpu=1,
                        memory=1024,
                        nvidia_gpu=1,
                        amd_gpu=2,
                        intel_gpu=3,
                    ),
                ),
                IdleJobConfig(
                    name="idle",
                    count=1,
                    image="miner",
                    command=["bash"],
                    args=["-c", "sleep infinity"],
                    resources=Resources(cpu=1, memory=1024),
                    env={"NAME": "VALUE"},
                    node_selector={"label": "value"},
                    image_pull_secret="secret",
                ),
            ],
        )

    def test_create_orchestrator_default(self, factory: EntityFactory) -> None:
        result = factory.create_orchestrator(
            {
                "job_hostname_template": "{job_id}.jobs-dev.neu.ro",
                "job_fallback_hostname": "default.jobs-dev.neu.ro",
                "job_schedule_timeout_s": 1,
                "job_schedule_scale_up_timeout_s": 2,
                "is_http_ingress_secure": False,
            }
        )

        assert result == OrchestratorConfig(
            job_hostname_template="{job_id}.jobs-dev.neu.ro",
            job_internal_hostname_template=None,
            job_fallback_hostname="default.jobs-dev.neu.ro",
            job_schedule_timeout_s=1,
            job_schedule_scale_up_timeout_s=2,
            is_http_ingress_secure=False,
            resource_pool_types=[],
            resource_presets=[],
            idle_jobs=[],
        )

    def test_create_resource_pool_type(
        self,
        factory: EntityFactory,
        nvidia_small_gpu: str,
        amd_small_gpu: str,
        intel_small_gpu: str,
    ) -> None:
        result = factory.create_resource_pool_type(
            {
                "name": "n1-highmem-4",
                "min_size": 1,
                "max_size": 2,
                "idle_size": 1,
                "cpu": 4.0,
                "available_cpu": 3.0,
                "memory": 12 * 1024,
                "available_memory": 10 * 1024,
                "disk_size": 700,
                "nvidia_gpu": 1,
                "amd_gpu": 2,
                "intel_gpu": 3,
                "nvidia_gpu_model": nvidia_small_gpu,
                "amd_gpu_model": amd_small_gpu,
                "intel_gpu_model": intel_small_gpu,
                "tpu": {
                    "ipv4_cidr_block": "10.0.0.0/8",
                    "types": ["tpu"],
                    "software_versions": ["v1"],
                },
                "is_preemptible": True,
                "price": "1.0",
                "currency": "USD",
                "cpu_min_watts": 1.0,
                "cpu_max_watts": 2.0,
            }
        )

        assert result == ResourcePoolType(
            name="n1-highmem-4",
            min_size=1,
            max_size=2,
            idle_size=1,
            cpu=4.0,
            available_cpu=3.0,
            memory=12 * 1024,
            available_memory=10 * 1024,
            gpu=1,
            gpu_model=nvidia_small_gpu,
            nvidia_gpu=1,
            nvidia_gpu_model=nvidia_small_gpu,
            amd_gpu=2,
            amd_gpu_model=amd_small_gpu,
            intel_gpu=3,
            intel_gpu_model=intel_small_gpu,
            tpu=mock.ANY,
            is_preemptible=True,
            price=Decimal("1.0"),
            currency="USD",
            cpu_min_watts=1.0,
            cpu_max_watts=2.0,
        )

    def test_create_empty_resource_pool_type(self, factory: EntityFactory) -> None:
        result = factory.create_resource_pool_type({"name": "node-pool"})

        assert result == ResourcePoolType(name="node-pool")

    def test_create_tpu_resource(self, factory: EntityFactory) -> None:
        result = factory.create_tpu_resource(
            {
                "ipv4_cidr_block": "10.0.0.0/8",
                "types": ["tpu"],
                "software_versions": ["v1"],
            }
        )

        assert result == TPUResource(
            ipv4_cidr_block="10.0.0.0/8", types=["tpu"], software_versions=["v1"]
        )

    def test_create_resource_preset_default(self, factory: EntityFactory) -> None:
        result = factory.create_resource_preset(
            {
                "name": "cpu-small",
                "credits_per_hour": "10",
                "cpu": 4.0,
                "memory": 1024,
            }
        )

        assert result == ResourcePreset(
            name="cpu-small", credits_per_hour=Decimal("10"), cpu=4.0, memory=1024
        )

    def test_create_resource_preset_custom(
        self,
        factory: EntityFactory,
        nvidia_small_gpu: str,
        amd_small_gpu: str,
        intel_small_gpu: str,
    ) -> None:
        result = factory.create_resource_preset(
            {
                "name": "gpu-small",
                "credits_per_hour": "10",
                "cpu": 4.0,
                "memory": 12288,
                "nvidia_gpu": 1,
                "amd_gpu": 2,
                "intel_gpu": 3,
                "nvidia_gpu_model": nvidia_small_gpu,
                "amd_gpu_model": amd_small_gpu,
                "intel_gpu_model": intel_small_gpu,
                "tpu": {"type": "tpu", "software_version": "v1"},
                "scheduler_enabled": True,
                "preemptible_node": True,
                "resource_pool_names": ["gpu"],
                "available_resource_pool_names": ["available-gpu"],
                "is_external_job": True,
            }
        )

        assert result == ResourcePreset(
            name="gpu-small",
            credits_per_hour=Decimal("10"),
            cpu=4.0,
            memory=12288,
            nvidia_gpu=1,
            nvidia_gpu_model=nvidia_small_gpu,
            amd_gpu=2,
            intel_gpu=3,
            amd_gpu_model=amd_small_gpu,
            intel_gpu_model=intel_small_gpu,
            tpu=TPUPreset(type="tpu", software_version="v1"),
            scheduler_enabled=True,
            preemptible_node=True,
            resource_pool_names=["gpu"],
            available_resource_pool_names=["available-gpu"],
            is_external_job=True,
        )

    def test_create_storage(self, factory: EntityFactory) -> None:
        result = factory.create_storage({"url": "https://storage-dev.neu.ro"})

        assert result == StorageConfig(
            url=URL("https://storage-dev.neu.ro"), volumes=[]
        )

    def test_create_storage_with_volumes(self, factory: EntityFactory) -> None:
        result = factory.create_storage(
            {
                "url": "https://storage-dev.neu.ro",
                "volumes": [
                    {"name": "test-1"},
                    {
                        "name": "test-2",
                        "path": "/volume",
                        "size": 1024,
                        "credits_per_hour_per_gb": "123",
                    },
                ],
            }
        )

        assert result == StorageConfig(
            url=URL("https://storage-dev.neu.ro"),
            volumes=[
                VolumeConfig(name="test-1"),
                VolumeConfig(
                    name="test-2",
                    path="/volume",
                    size=1024,
                    credits_per_hour_per_gb=Decimal(123),
                ),
            ],
        )

    def test_create_registry(self, factory: EntityFactory) -> None:
        result = factory.create_registry({"url": "https://registry-dev.neu.ro"})

        assert result == RegistryConfig(url=URL("https://registry-dev.neu.ro"))

    def test_create_monitoring(self, factory: EntityFactory) -> None:
        result = factory.create_monitoring({"url": "https://monitoring-dev.neu.ro"})

        assert result == MonitoringConfig(url=URL("https://monitoring-dev.neu.ro"))

    def test_create_secrets(self, factory: EntityFactory) -> None:
        result = factory.create_secrets({"url": "https://secrets-dev.neu.ro"})

        assert result == SecretsConfig(url=URL("https://secrets-dev.neu.ro"))

    def test_create_metrics(self, factory: EntityFactory) -> None:
        result = factory.create_metrics({"url": "https://metrics-dev.neu.ro"})

        assert result == MetricsConfig(url=URL("https://metrics-dev.neu.ro"))

    def test_create_dns(self, factory: EntityFactory) -> None:
        result = factory.create_dns(
            {
                "name": "neu.ro",
                "a_records": [{"name": "*.jobs-dev.neu.ro.", "ips": ["192.168.0.2"]}],
            }
        )

        assert result == DNSConfig(name="neu.ro", a_records=[mock.ANY])

    def test_create_a_record_with_ips(self, factory: EntityFactory) -> None:
        result = factory.create_a_record(
            {"name": "*.jobs-dev.neu.ro.", "ips": ["192.168.0.2"]}
        )

        assert result == ARecord(name="*.jobs-dev.neu.ro.", ips=["192.168.0.2"])

    def test_create_a_record_dns_name(self, factory: EntityFactory) -> None:
        result = factory.create_a_record(
            {
                "name": "*.jobs-dev.neu.ro.",
                "dns_name": "load-balancer",
                "zone_id": "/hostedzone/1",
                "evaluate_target_health": True,
            }
        )

        assert result == ARecord(
            name="*.jobs-dev.neu.ro.",
            dns_name="load-balancer",
            zone_id="/hostedzone/1",
            evaluate_target_health=True,
        )

    def test_create_disks(self, factory: EntityFactory) -> None:
        result = factory.create_disks(
            {"url": "https://metrics-dev.neu.ro", "storage_limit_per_user": 1024}
        )

        assert result == DisksConfig(
            url=URL("https://metrics-dev.neu.ro"), storage_limit_per_user=1024
        )

    def test_create_buckets(self, factory: EntityFactory) -> None:
        result = factory.create_buckets(
            {"url": "https://buckets-dev.neu.ro", "disable_creation": True}
        )

        assert result == BucketsConfig(
            url=URL("https://buckets-dev.neu.ro"), disable_creation=True
        )

    def test_create_ingress(self, factory: EntityFactory) -> None:
        result = factory.create_ingress(
            {
                "acme_environment": "production",
                "default_cors_origins": ["https://console.apolo.us"],
                "additional_cors_origins": ["https://custom.app"],
            }
        )

        assert result == IngressConfig(
            acme_environment=ACMEEnvironment.PRODUCTION,
            default_cors_origins=["https://console.apolo.us"],
            additional_cors_origins=["https://custom.app"],
        )

    def test_create_ingress_defaults(self, factory: EntityFactory) -> None:
        result = factory.create_ingress({"acme_environment": "production"})

        assert result == IngressConfig(acme_environment=ACMEEnvironment.PRODUCTION)

    @pytest.fixture
    def google_cloud_provider_response(self) -> dict[str, Any]:
        return {
            "type": "gcp",
            "location_type": "zonal",
            "region": "us-central1",
            "zones": ["us-central1-a"],
            "project": "project",
            "credentials": {
                "type": "service_account",
                "project_id": "project_id",
                "private_key_id": "private_key_id",
                "private_key": "private_key",
                "client_email": "service.account@gmail.com",
                "client_id": "client_id",
                "auth_uri": "https://auth_uri",
                "token_uri": "https://token_uri",
                "auth_provider_x509_cert_url": "https://auth_provider_x509_cert_url",
                "client_x509_cert_url": "https://client_x509_cert_url",
            },
            "node_pools": [
                {
                    "name": "n1-highmem-8",
                    "role": "platform_job",
                    "machine_type": "n1-highmem-8",
                    "min_size": 0,
                    "max_size": 1,
                    "cpu": 8.0,
                    "available_cpu": 7.0,
                    "memory": 52 * 1024,
                    "available_memory": 45 * 1024,
                    "disk_size": 700,
                    "available_disk_size": 670,
                },
                {
                    "name": "n1-highmem-32-1xk80-preemptible",
                    "role": "platform_job",
                    "machine_type": "n1-highmem-32",
                    "min_size": 0,
                    "max_size": 1,
                    "idle_size": 1,
                    "cpu": 32.0,
                    "available_cpu": 31.0,
                    "memory": 208 * 1024,
                    "available_memory": 201 * 1024,
                    "disk_size": 700,
                    "available_disk_size": 670,
                    "nvidia_gpu": 1,
                    "nvidia_gpu_model": "nvidia-tesla-k80",
                    "is_preemptible": True,
                },
            ],
            "storage": {
                "description": "GCP Filestore (Premium)",
                "backend": "filestore",
                "tier": "PREMIUM",
                "instances": [
                    {"name": "test-1", "size": 5 * 1024 * 1024, "ready": False},
                    {"name": "test-2", "size": 3 * 1024 * 1024, "ready": True},
                ],
            },
        }

    @pytest.fixture
    def google_cloud_provider(self) -> GoogleCloudProvider:
        return GoogleCloudProvider(
            location_type=ClusterLocationType.ZONAL,
            region="us-central1",
            zones=["us-central1-a"],
            project="project",
            credentials={
                "type": "service_account",
                "project_id": "project_id",
                "private_key_id": "private_key_id",
                "private_key": "private_key",
                "client_email": "service.account@gmail.com",
                "client_id": "client_id",
                "auth_uri": "https://auth_uri",
                "token_uri": "https://token_uri",
                "auth_provider_x509_cert_url": "https://auth_provider_x509_cert_url",
                "client_x509_cert_url": "https://client_x509_cert_url",
            },
            node_pools=[
                NodePool(
                    name="n1-highmem-8",
                    machine_type="n1-highmem-8",
                    min_size=0,
                    max_size=1,
                    cpu=8.0,
                    available_cpu=7.0,
                    memory=52 * 1024,
                    available_memory=45 * 1024,
                    disk_size=700,
                    available_disk_size=670,
                ),
                NodePool(
                    name="n1-highmem-32-1xk80-preemptible",
                    machine_type="n1-highmem-32",
                    min_size=0,
                    max_size=1,
                    idle_size=1,
                    cpu=32.0,
                    available_cpu=31.0,
                    memory=208 * 1024,
                    available_memory=201 * 1024,
                    disk_size=700,
                    available_disk_size=670,
                    gpu=1,
                    gpu_model="nvidia-tesla-k80",
                    nvidia_gpu=1,
                    nvidia_gpu_model="nvidia-tesla-k80",
                    is_preemptible=True,
                ),
            ],
            storage=GoogleStorage(
                description="GCP Filestore (Premium)",
                tier=GoogleFilestoreTier.PREMIUM,
                instances=[
                    StorageInstance(name="test-1", size=5 * 1024 * 1024),
                    StorageInstance(name="test-2", size=3 * 1024 * 1024, ready=True),
                ],
            ),
        )

    def test_create_cloud_provider_google(
        self,
        factory: EntityFactory,
        google_cloud_provider: GoogleCloudProvider,
        google_cloud_provider_response: dict[str, Any],
    ) -> None:
        result = factory.create_cloud_provider(google_cloud_provider_response)
        assert result == google_cloud_provider

    @pytest.fixture
    def aws_cloud_provider_response(self) -> dict[str, Any]:
        return {
            "type": "aws",
            "region": "us-central-1",
            "zones": ["us-central-1a"],
            "vpc_id": "test-vpc",
            "credentials": {
                "access_key_id": "access_key_id",
                "secret_access_key": "secret_access_key",
            },
            "node_pools": [
                {
                    "role": "platform_job",
                    "name": "m5-2xlarge",
                    "machine_type": "m5.2xlarge",
                    "min_size": 0,
                    "max_size": 1,
                    "cpu": 8.0,
                    "available_cpu": 7.0,
                    "memory": 32 * 1024,
                    "available_memory": 28 * 1024,
                    "disk_size": 700,
                    "available_disk_size": 670,
                },
                {
                    "role": "platform_job",
                    "name": "p2-xlarge-1xk80-preemptible",
                    "machine_type": "p2.xlarge",
                    "min_size": 0,
                    "max_size": 1,
                    "idle_size": 1,
                    "cpu": 4.0,
                    "available_cpu": 3.0,
                    "memory": 61 * 1024,
                    "available_memory": 57 * 1024,
                    "disk_size": 700,
                    "available_disk_size": 670,
                    "nvidia_gpu": 1,
                    "nvidia_gpu_model": "nvidia-tesla-k80",
                    "is_preemptible": True,
                },
            ],
            "storage": {
                "description": "AWS EFS (generalPurpose, bursting)",
                "performance_mode": "generalPurpose",
                "throughput_mode": "bursting",
                "instances": [
                    {"name": "test-1", "ready": False},
                    {"name": "test-2", "ready": True},
                ],
            },
        }

    @pytest.fixture
    def aws_cloud_provider(self) -> AWSCloudProvider:
        return AWSCloudProvider(
            region="us-central-1",
            zones=["us-central-1a"],
            vpc_id="test-vpc",
            credentials=AWSCredentials(
                access_key_id="access_key_id", secret_access_key="secret_access_key"
            ),
            node_pools=[
                NodePool(
                    name="m5-2xlarge",
                    machine_type="m5.2xlarge",
                    min_size=0,
                    max_size=1,
                    cpu=8.0,
                    available_cpu=7.0,
                    memory=32 * 1024,
                    available_memory=28 * 1024,
                    disk_size=700,
                    available_disk_size=670,
                ),
                NodePool(
                    name="p2-xlarge-1xk80-preemptible",
                    machine_type="p2.xlarge",
                    min_size=0,
                    max_size=1,
                    idle_size=1,
                    cpu=4.0,
                    available_cpu=3.0,
                    memory=61 * 1024,
                    available_memory=57 * 1024,
                    disk_size=700,
                    available_disk_size=670,
                    gpu=1,
                    gpu_model="nvidia-tesla-k80",
                    nvidia_gpu=1,
                    nvidia_gpu_model="nvidia-tesla-k80",
                    is_preemptible=True,
                ),
            ],
            storage=AWSStorage(
                description="AWS EFS (generalPurpose, bursting)",
                performance_mode=EFSPerformanceMode.GENERAL_PURPOSE,
                throughput_mode=EFSThroughputMode.BURSTING,
                instances=[
                    StorageInstance(name="test-1"),
                    StorageInstance(name="test-2", ready=True),
                ],
            ),
        )

    def test_create_cloud_provider_aws(
        self,
        factory: EntityFactory,
        aws_cloud_provider: AWSCloudProvider,
        aws_cloud_provider_response: dict[str, Any],
    ) -> None:
        result = factory.create_cloud_provider(aws_cloud_provider_response)
        assert result == aws_cloud_provider

    @pytest.fixture
    def azure_cloud_provider_response(self) -> dict[str, Any]:
        return {
            "type": "azure",
            "region": "westus",
            "resource_group": "resource_group",
            "credentials": {
                "subscription_id": "subscription_id",
                "tenant_id": "tenant_id",
                "client_id": "client_id",
                "client_secret": "client_secret",
            },
            "node_pools": [
                {
                    "role": "platform_job",
                    "name": "Standard_D8s_v3",
                    "machine_type": "Standard_D8s_v3",
                    "min_size": 0,
                    "max_size": 1,
                    "cpu": 8.0,
                    "available_cpu": 7.0,
                    "memory": 32 * 1024,
                    "available_memory": 28 * 1024,
                    "disk_size": 700,
                    "available_disk_size": 670,
                },
                {
                    "role": "platform_job",
                    "name": "Standard_NC6-1xk80-preemptible",
                    "machine_type": "Standard_NC6",
                    "min_size": 0,
                    "max_size": 1,
                    "idle_size": 1,
                    "cpu": 6.0,
                    "available_cpu": 5.0,
                    "memory": 56 * 1024,
                    "available_memory": 50 * 1024,
                    "disk_size": 700,
                    "available_disk_size": 670,
                    "nvidia_gpu": 1,
                    "nvidia_gpu_model": "nvidia-tesla-k80",
                    "is_preemptible": True,
                },
            ],
            "storage": {
                "description": "Azure Files (Premium, LRS replication)",
                "tier": "Premium",
                "replication_type": "LRS",
                "instances": [
                    {"name": "test-1", "size": 100 * 1024, "ready": False},
                    {"name": "test-2", "size": 200 * 1024, "ready": True},
                ],
            },
        }

    @pytest.fixture
    def azure_cloud_provider(self) -> AzureCloudProvider:
        return AzureCloudProvider(
            region="westus",
            resource_group="resource_group",
            credentials=AzureCredentials(
                subscription_id="subscription_id",
                tenant_id="tenant_id",
                client_id="client_id",
                client_secret="client_secret",
            ),
            node_pools=[
                NodePool(
                    name="Standard_D8s_v3",
                    machine_type="Standard_D8s_v3",
                    min_size=0,
                    max_size=1,
                    cpu=8.0,
                    available_cpu=7.0,
                    memory=32 * 1024,
                    available_memory=28 * 1024,
                    disk_size=700,
                    available_disk_size=670,
                ),
                NodePool(
                    name="Standard_NC6-1xk80-preemptible",
                    machine_type="Standard_NC6",
                    min_size=0,
                    max_size=1,
                    idle_size=1,
                    cpu=6.0,
                    available_cpu=5.0,
                    memory=56 * 1024,
                    available_memory=50 * 1024,
                    disk_size=700,
                    available_disk_size=670,
                    gpu=1,
                    gpu_model="nvidia-tesla-k80",
                    nvidia_gpu=1,
                    nvidia_gpu_model="nvidia-tesla-k80",
                    is_preemptible=True,
                ),
            ],
            storage=AzureStorage(
                description="Azure Files (Premium, LRS replication)",
                tier=AzureStorageTier.PREMIUM,
                replication_type=AzureReplicationType.LRS,
                instances=[
                    StorageInstance(name="test-1", size=100 * 1024),
                    StorageInstance(name="test-2", size=200 * 1024, ready=True),
                ],
            ),
        )

    def test_create_cloud_provider_azure(
        self,
        factory: EntityFactory,
        azure_cloud_provider: AzureCloudProvider,
        azure_cloud_provider_response: dict[str, Any],
    ) -> None:
        result = factory.create_cloud_provider(azure_cloud_provider_response)
        assert result == azure_cloud_provider

    @pytest.fixture
    def on_prem_cloud_provider_response(self) -> dict[str, Any]:
        return {
            "type": "on_prem",
            "kubernetes_url": "localhost:8001",
            "credentials": {
                "token": "kubernetes-token",
                "ca_data": "kubernetes-ca-data",
            },
            "node_pools": [
                {
                    "role": "platform_job",
                    "min_size": 1,
                    "max_size": 1,
                    "name": "cpu-machine",
                    "machine_type": "cpu-machine",
                    "cpu": 1.0,
                    "available_cpu": 1.0,
                    "memory": 1024,
                    "available_memory": 1024,
                    "disk_size": 700,
                },
                {
                    "role": "platform_job",
                    "min_size": 1,
                    "max_size": 1,
                    "name": "gpu-machine-1xk80",
                    "machine_type": "gpu-machine-1xk80",
                    "cpu": 1.0,
                    "available_cpu": 1.0,
                    "memory": 1024,
                    "available_memory": 1024,
                    "disk_size": 700,
                    "nvidia_gpu": 1,
                    "nvidia_gpu_model": "nvidia-tesla-k80",
                    "price": "0.9",
                    "currency": "USD",
                    "cpu_min_watts": 0.1,
                    "cpu_max_watts": 100,
                },
            ],
        }

    @pytest.fixture
    def on_prem_cloud_provider(self) -> OnPremCloudProvider:
        return OnPremCloudProvider(
            kubernetes_url=URL("localhost:8001"),
            credentials=KubernetesCredentials(
                token="kubernetes-token", ca_data="kubernetes-ca-data"
            ),
            node_pools=[
                NodePool(
                    min_size=1,
                    max_size=1,
                    name="cpu-machine",
                    cpu=1.0,
                    available_cpu=1.0,
                    memory=1024,
                    available_memory=1024,
                    disk_size=700,
                    available_disk_size=700,
                    machine_type="cpu-machine",
                ),
                NodePool(
                    min_size=1,
                    max_size=1,
                    name="gpu-machine-1xk80",
                    cpu=1.0,
                    available_cpu=1.0,
                    memory=1024,
                    available_memory=1024,
                    disk_size=700,
                    available_disk_size=700,
                    gpu=1,
                    gpu_model="nvidia-tesla-k80",
                    nvidia_gpu=1,
                    nvidia_gpu_model="nvidia-tesla-k80",
                    price=Decimal("0.9"),
                    currency="USD",
                    machine_type="gpu-machine-1xk80",
                    cpu_min_watts=0.1,
                    cpu_max_watts=100,
                ),
            ],
            storage=None,
        )

    def test_create_cloud_provider_on_prem(
        self,
        factory: EntityFactory,
        on_prem_cloud_provider: OnPremCloudProvider,
        on_prem_cloud_provider_response: dict[str, Any],
    ) -> None:
        result = factory.create_cloud_provider(on_prem_cloud_provider_response)
        assert result == on_prem_cloud_provider

    @pytest.fixture
    def vcd_cloud_provider_response(self) -> dict[str, Any]:
        return {
            "type": "vcd_mts",
            "url": "vcd_url",
            "organization": "vcd_org",
            "virtual_data_center": "vdc",
            "edge_name": "edge",
            "edge_external_network_name": "edge-external-network",
            "edge_public_ip": "10.0.0.1",
            "catalog_name": "catalog",
            "credentials": {
                "user": "vcd_user",
                "password": "vcd_password",
                "ssh_password": "ssh-password",
            },
            "node_pools": [
                {
                    "role": "platform_job",
                    "min_size": 1,
                    "max_size": 1,
                    "name": "Master-neuro",
                    "machine_type": "Master-neuro",
                    "cpu": 8.0,
                    "available_cpu": 7.0,
                    "memory": 32 * 1024,
                    "available_memory": 29 * 1024,
                    "disk_size": 700,
                    "available_disk_size": 670,
                },
                {
                    "role": "platform_job",
                    "min_size": 1,
                    "max_size": 1,
                    "name": "X16-neuro-1xk80",
                    "machine_type": "X16-neuro",
                    "cpu": 16.0,
                    "available_cpu": 15.0,
                    "memory": 40 * 1024,
                    "available_memory": 37 * 1024,
                    "disk_size": 700,
                    "available_disk_size": 670,
                    "nvidia_gpu": 1,
                    "nvidia_gpu_model": "nvidia-tesla-k80",
                    "price": "0.9",
                    "currency": "USD",
                    "cpu_min_watts": 0.1,
                    "cpu_max_watts": 100,
                },
            ],
            "storage": {
                "profile_name": "profile",
                "size": 10,
                "instances": [
                    {"name": "test-1", "size": 7 * 1024, "ready": False},
                    {"name": "test-2", "size": 3 * 1024, "ready": True},
                ],
                "description": "profile",
            },
        }

    @pytest.fixture
    def vcd_cloud_provider(self) -> VCDCloudProvider:
        return VCDCloudProvider(
            _type=CloudProviderType.VCD_MTS,
            url=URL("vcd_url"),
            organization="vcd_org",
            virtual_data_center="vdc",
            edge_name="edge",
            edge_external_network_name="edge-external-network",
            edge_public_ip="10.0.0.1",
            catalog_name="catalog",
            credentials=VCDCredentials(
                user="vcd_user", password="vcd_password", ssh_password="ssh-password"
            ),
            node_pools=[
                NodePool(
                    min_size=1,
                    max_size=1,
                    name="Master-neuro",
                    machine_type="Master-neuro",
                    cpu=8.0,
                    available_cpu=7.0,
                    memory=32 * 1024,
                    available_memory=29 * 1024,
                    disk_size=700,
                    available_disk_size=670,
                ),
                NodePool(
                    min_size=1,
                    max_size=1,
                    name="X16-neuro-1xk80",
                    machine_type="X16-neuro",
                    cpu=16.0,
                    available_cpu=15.0,
                    memory=40 * 1024,
                    available_memory=37 * 1024,
                    disk_size=700,
                    available_disk_size=670,
                    gpu=1,
                    gpu_model="nvidia-tesla-k80",
                    nvidia_gpu=1,
                    nvidia_gpu_model="nvidia-tesla-k80",
                    price=Decimal("0.9"),
                    currency="USD",
                    cpu_min_watts=0.1,
                    cpu_max_watts=100,
                ),
            ],
            storage=VCDStorage(
                description="profile",
                profile_name="profile",
                size=10,
                instances=[
                    StorageInstance(name="test-1", size=7 * 1024),
                    StorageInstance(name="test-2", size=3 * 1024, ready=True),
                ],
            ),
        )

    def test_create_cloud_provider_vcd(
        self,
        factory: EntityFactory,
        vcd_cloud_provider: VCDCloudProvider,
        vcd_cloud_provider_response: dict[str, Any],
    ) -> None:
        result = factory.create_cloud_provider(vcd_cloud_provider_response)
        assert result == vcd_cloud_provider

    @pytest.fixture
    def credentials(self) -> dict[str, Any]:
        return {
            "neuro": {
                "url": "https://neu.ro",
                "token": "cluster_token",
            },
            "neuro_registry": {
                "url": "https://ghcr.io/neuro-inc",
                "username": "username",
                "password": "password",
                "email": "username@neu.ro",
            },
            "neuro_helm": {
                "url": "oci://neuro-inc.ghcr.io",
                "username": "username",
                "password": "password",
            },
            "grafana": {
                "username": "username",
                "password": "password",
            },
            "sentry": {
                "client_key_id": "key",
                "public_dsn": "dsn",
                "sample_rate": 0.2,
            },
            "docker_hub": {
                "url": "https://index.docker.io/v1",
                "username": "test",
                "password": "password",
                "email": "test@neu.ro",
            },
            "minio": {
                "username": "test",
                "password": "password",
            },
            "emc_ecs": {
                "access_key_id": "key_id",
                "secret_access_key": "secret_key",
                "s3_endpoint": "https://emc-ecs.s3",
                "management_endpoint": "https://emc-ecs.management",
                "s3_assumable_role": "s3-role",
            },
            "open_stack": {
                "account_id": "id",
                "password": "password",
                "s3_endpoint": "https://os.s3",
                "endpoint": "https://os.management",
                "region_name": "region",
            },
        }

    def test_create_credentials(
        self, factory: EntityFactory, credentials: dict[str, Any]
    ) -> None:
        result = factory.create_credentials(credentials)

        assert result == CredentialsConfig(
            neuro=NeuroAuthConfig(
                url=URL("https://neu.ro"),
                token="cluster_token",
            ),
            neuro_registry=DockerRegistryConfig(
                url=URL("https://ghcr.io/neuro-inc"),
                username="username",
                password="password",
                email="username@neu.ro",
            ),
            neuro_helm=HelmRegistryConfig(
                url=URL("oci://neuro-inc.ghcr.io"),
                username="username",
                password="password",
            ),
            grafana=GrafanaCredentials(
                username="username",
                password="password",
            ),
            sentry=SentryCredentials(
                client_key_id="key", public_dsn=URL("dsn"), sample_rate=0.2
            ),
            docker_hub=DockerRegistryConfig(
                url=URL("https://index.docker.io/v1"),
                username="test",
                password="password",
                email="test@neu.ro",
            ),
            minio=MinioCredentials(
                username="test",
                password="password",
            ),
            emc_ecs=EMCECSCredentials(
                access_key_id="key_id",
                secret_access_key="secret_key",
                s3_endpoint=URL("https://emc-ecs.s3"),
                management_endpoint=URL("https://emc-ecs.management"),
                s3_assumable_role="s3-role",
            ),
            open_stack=OpenStackCredentials(
                account_id="id",
                password="password",
                s3_endpoint=URL("https://os.s3"),
                endpoint=URL("https://os.management"),
                region_name="region",
            ),
        )

    def test_create_minimal_credentials(
        self, factory: EntityFactory, credentials: dict[str, Any]
    ) -> None:
        del credentials["grafana"]
        del credentials["sentry"]
        del credentials["docker_hub"]
        del credentials["minio"]
        del credentials["emc_ecs"]
        del credentials["open_stack"]
        result = factory.create_credentials(credentials)

        assert result == CredentialsConfig(
            neuro=NeuroAuthConfig(
                url=URL("https://neu.ro"),
                token="cluster_token",
            ),
            neuro_registry=DockerRegistryConfig(
                url=URL("https://ghcr.io/neuro-inc"),
                username="username",
                password="password",
                email="username@neu.ro",
            ),
            neuro_helm=HelmRegistryConfig(
                url=URL("oci://neuro-inc.ghcr.io"),
                username="username",
                password="password",
            ),
        )

    @pytest.fixture
    def node_pool_options_response(self) -> dict[str, Any]:
        return {
            "machine_type": "Standard_ND24s",
            "cpu": 24,
            "available_cpu": 23,
            "memory": 458752,
            "available_memory": 452608,
            "gpu": 4,
            "gpu_model": "nvidia-tesla-p40",
            "extra_info": "will be ignored",
        }

    @pytest.fixture
    def node_pool_options(self) -> NodePoolOptions:
        return NodePoolOptions(
            machine_type="Standard_ND24s",
            cpu=24,
            available_cpu=23,
            memory=458752,
            available_memory=452608,
            nvidia_gpu=4,
            nvidia_gpu_model="nvidia-tesla-p40",
        )

    def test_aws_cloud_provider_options(
        self,
        factory: EntityFactory,
        node_pool_options_response: dict[str, Any],
        node_pool_options: NodePoolOptions,
    ) -> None:
        response = {
            "node_pools": [node_pool_options_response],
        }
        result = factory.create_cloud_provider_options(CloudProviderType.AWS, response)

        assert result == CloudProviderOptions(
            type=CloudProviderType.AWS,
            node_pools=[node_pool_options],
        )

    def test_aws_cloud_provider_options_defaults(self, factory: EntityFactory) -> None:
        result = factory.create_cloud_provider_options(CloudProviderType.AWS, {})

        assert result == CloudProviderOptions(type=CloudProviderType.AWS, node_pools=[])

    def test_google_cloud_provider_options(
        self,
        factory: EntityFactory,
        node_pool_options_response: dict[str, Any],
        node_pool_options: NodePoolOptions,
    ) -> None:
        response = {
            "node_pools": [node_pool_options_response],
        }
        result = factory.create_cloud_provider_options(CloudProviderType.GCP, response)

        assert result == CloudProviderOptions(
            type=CloudProviderType.GCP, node_pools=[node_pool_options]
        )

    def test_azure_cloud_provider_options(
        self,
        factory: EntityFactory,
        node_pool_options_response: dict[str, Any],
        node_pool_options: NodePoolOptions,
    ) -> None:
        response = {
            "node_pools": [node_pool_options_response],
        }
        result = factory.create_cloud_provider_options(
            CloudProviderType.AZURE, response
        )

        assert result == CloudProviderOptions(
            type=CloudProviderType.AZURE, node_pools=[node_pool_options]
        )

    def test_vcd_cloud_provider_options_defaults(
        self,
        factory: EntityFactory,
        node_pool_options_response: dict[str, Any],
        node_pool_options: NodePoolOptions,
    ) -> None:
        response = {
            "node_pools": [node_pool_options_response],
        }
        result = factory.create_cloud_provider_options(
            CloudProviderType.VCD_MTS, response
        )

        assert result == VCDCloudProviderOptions(
            type=CloudProviderType.VCD_MTS,
            node_pools=[node_pool_options],
        )

    def test_vcd_cloud_provider_options(
        self,
        factory: EntityFactory,
        node_pool_options_response: dict[str, Any],
        node_pool_options: NodePoolOptions,
    ) -> None:
        response = {
            "node_pools": [node_pool_options_response],
            "url": "https://vcd",
            "organization": "neuro-org",
            "edge_name_template": "neuro-edge",
            "edge_external_network_name": "neuro-edge-external",
            "catalog_name": "neuro",
            "storage_profile_names": ["neuro-storage"],
        }
        result = factory.create_cloud_provider_options(
            CloudProviderType.VCD_MTS, response
        )

        assert result == VCDCloudProviderOptions(
            type=CloudProviderType.VCD_MTS,
            node_pools=[node_pool_options],
            url=URL("https://vcd"),
            organization="neuro-org",
            edge_name_template="neuro-edge",
            edge_external_network_name="neuro-edge-external",
            catalog_name="neuro",
            storage_profile_names=["neuro-storage"],
        )

    def test_create_energy(self, factory: EntityFactory) -> None:
        timezone = ZoneInfo("America/Los_Angeles")
        energy = factory.create_energy(
            {
                "co2_grams_eq_per_kwh": 100,
                "schedules": [
                    {"name": "default", "price_per_kwh": "123.4"},
                    {
                        "name": "green",
                        "price_per_kwh": "123.4",
                        "periods": [
                            {"weekday": 1, "start_time": "23:00", "end_time": "00:00"}
                        ],
                    },
                ],
            },
            timezone=timezone,
        )

        assert energy == EnergyConfig(
            co2_grams_eq_per_kwh=100,
            schedules=[
                EnergySchedule(
                    name="default",
                    price_per_kwh=Decimal("123.4"),
                    periods=[],
                ),
                EnergySchedule(
                    name="green",
                    price_per_kwh=Decimal("123.4"),
                    periods=[
                        EnergySchedulePeriod(
                            weekday=1,
                            start_time=time(hour=23, minute=0, tzinfo=timezone),
                            end_time=time(hour=0, minute=0, tzinfo=timezone),
                        )
                    ],
                ),
            ],
        )

    @pytest.fixture
    def apps(self) -> AppsConfig:
        return AppsConfig(
            apps_hostname_templates=["{app_name}.apps.default.org.neu.ro"],
            app_proxy_url=URL("outputs-proxy.apps.default.org.neu.ro"),
        )

    @pytest.fixture
    def apps_dict(self) -> dict[str, Any]:
        return {
            "apps_hostname_templates": ["{app_name}.apps.default.org.neu.ro"],
            "app_proxy_url": "outputs-proxy.apps.default.org.neu.ro",
        }

    def test_create_apps(
        self, factory: EntityFactory, apps_dict: dict[str, Any], apps: AppsConfig
    ) -> None:
        result = factory.create_apps(apps_dict)
        assert result == apps

    def test_create_cluster_with_apps(
        self,
        factory: EntityFactory,
        google_cloud_provider_response: dict[str, Any],
        credentials: dict[str, Any],
        apps_dict: dict[str, Any],
    ) -> None:
        result = factory.create_cluster(
            {
                "name": "default",
                "status": "blank",
                "timezone": "America/Los_Angeles",
                "orchestrator": {
                    "job_hostname_template": "{job_id}.jobs-dev.neu.ro",
                    "job_fallback_hostname": "default.jobs-dev.neu.ro",
                    "job_schedule_timeout_s": 1,
                    "job_schedule_scale_up_timeout_s": 2,
                    "is_http_ingress_secure": False,
                },
                "storage": {"url": "https://storage-dev.neu.ro"},
                "registry": {"url": "https://registry-dev.neu.ro"},
                "monitoring": {"url": "https://monitoring-dev.neu.ro"},
                "secrets": {"url": "https://secrets-dev.neu.ro"},
                "metrics": {"url": "https://secrets-dev.neu.ro"},
                "disks": {
                    "url": "https://secrets-dev.neu.ro",
                    "storage_limit_per_user": 1024,
                },
                "ingress": {"acme_environment": "production"},
                "dns": {
                    "name": "neu.ro",
                    "a_records": [
                        {"name": "*.jobs-dev.neu.ro.", "ips": ["192.168.0.2"]}
                    ],
                },
                "cloud_provider": google_cloud_provider_response,
                "credentials": credentials,
                "apps": apps_dict,
                "created_at": str(datetime.now()),
            }
        )

        assert result.name == "default"
        assert result.status == ClusterStatus.BLANK
        assert result.timezone == ZoneInfo("America/Los_Angeles")
        assert result.orchestrator
        assert result.storage
        assert result.registry
        assert result.monitoring
        assert result.secrets
        assert result.metrics
        assert result.disks
        assert result.ingress
        assert result.dns
        assert result.cloud_provider
        assert result.credentials
        assert result.created_at
        assert result.apps
        assert result.apps.apps_hostname_templates == [
            "{app_name}.apps.default.org.neu.ro"
        ]
        assert result.apps.app_proxy_url == URL("outputs-proxy.apps.default.org.neu.ro")


class TestPayloadFactory:
    @pytest.fixture
    def factory(self) -> PayloadFactory:
        return PayloadFactory()

    def test_create_patch_cluster_request(
        self, factory: PayloadFactory, credentials: CredentialsConfig
    ) -> None:
        result = factory.create_patch_cluster_request(
            PatchClusterRequest(
                credentials=credentials,
                storage=StorageConfig(url=URL("https://storage-dev.neu.ro")),
                registry=RegistryConfig(url=URL("https://registry-dev.neu.ro")),
                orchestrator=PatchOrchestratorConfigRequest(),
                monitoring=MonitoringConfig(url=URL("https://monitoring-dev.neu.ro")),
                secrets=SecretsConfig(url=URL("https://secrets-dev.neu.ro")),
                metrics=MetricsConfig(url=URL("https://metrics-dev.neu.ro")),
                disks=DisksConfig(
                    url=URL("https://metrics-dev.neu.ro"), storage_limit_per_user=1024
                ),
                buckets=BucketsConfig(
                    url=URL("https://buckets-dev.neu.ro"), disable_creation=True
                ),
                ingress=IngressConfig(acme_environment=ACMEEnvironment.PRODUCTION),
                dns=DNSConfig(
                    name="neu.ro",
                    a_records=[ARecord(name="*.jobs-dev.neu.ro.", ips=["192.168.0.2"])],
                ),
                timezone=ZoneInfo("America/Los_Angeles"),
                energy=EnergyConfig(co2_grams_eq_per_kwh=100),
            )
        )

        assert result == {
            "credentials": mock.ANY,
            "storage": mock.ANY,
            "registry": mock.ANY,
            "orchestrator": mock.ANY,
            "monitoring": mock.ANY,
            "secrets": mock.ANY,
            "metrics": mock.ANY,
            "disks": mock.ANY,
            "buckets": mock.ANY,
            "ingress": mock.ANY,
            "dns": mock.ANY,
            "timezone": "America/Los_Angeles",
            "energy": mock.ANY,
        }

    def test_create_patch_cluster_request_default(
        self, factory: PayloadFactory
    ) -> None:
        result = factory.create_patch_cluster_request(PatchClusterRequest())

        assert result == {}

    def test_create_orchestrator(self, factory: PayloadFactory) -> None:
        result = factory.create_orchestrator(
            OrchestratorConfig(
                job_hostname_template="{job_id}.jobs-dev.neu.ro",
                job_internal_hostname_template="{job_id}.platform-jobs",
                job_fallback_hostname="default.jobs-dev.neu.ro",
                job_schedule_timeout_s=1,
                job_schedule_scale_up_timeout_s=2,
                is_http_ingress_secure=False,
                allow_privileged_mode=True,
                allow_job_priority=True,
                resource_pool_types=[ResourcePoolType(name="cpu")],
                resource_presets=[
                    ResourcePreset(
                        name="cpu-micro",
                        credits_per_hour=Decimal(10),
                        cpu=0.1,
                        memory=100,
                    )
                ],
                pre_pull_images=["neuromation/base"],
                idle_jobs=[
                    IdleJobConfig(
                        name="idle",
                        count=1,
                        image="miner",
                        resources=Resources(
                            cpu=1,
                            memory=1024,
                            nvidia_gpu=1,
                            amd_gpu=2,
                            intel_gpu=3,
                        ),
                    ),
                    IdleJobConfig(
                        name="idle",
                        count=1,
                        image="miner",
                        command=["bash"],
                        args=["-c", "sleep infinity"],
                        resources=Resources(cpu=1, memory=1024),
                        env={"NAME": "VALUE"},
                        node_selector={"label": "value"},
                        image_pull_secret="secret",
                    ),
                ],
            )
        )

        assert result == {
            "job_hostname_template": "{job_id}.jobs-dev.neu.ro",
            "job_internal_hostname_template": "{job_id}.platform-jobs",
            "job_fallback_hostname": "default.jobs-dev.neu.ro",
            "job_schedule_timeout_s": 1,
            "job_schedule_scale_up_timeout_s": 2,
            "is_http_ingress_secure": False,
            "resource_pool_types": [mock.ANY],
            "resource_presets": [mock.ANY],
            "allow_privileged_mode": True,
            "allow_job_priority": True,
            "pre_pull_images": ["neuromation/base"],
            "idle_jobs": [
                {
                    "name": "idle",
                    "count": 1,
                    "image": "miner",
                    "resources": {
                        "cpu": 1,
                        "memory": 1024,
                        "nvidia_gpu": 1,
                        "amd_gpu": 2,
                        "intel_gpu": 3,
                    },
                },
                {
                    "name": "idle",
                    "count": 1,
                    "image": "miner",
                    "command": ["bash"],
                    "args": ["-c", "sleep infinity"],
                    "resources": {"cpu": 1, "memory": 1024},
                    "env": {"NAME": "VALUE"},
                    "node_selector": {"label": "value"},
                    "image_pull_secret": "secret",
                },
            ],
        }

    def test_create_orchestrator_default(self, factory: PayloadFactory) -> None:
        result = factory.create_orchestrator(
            OrchestratorConfig(
                job_hostname_template="{job_id}.jobs-dev.neu.ro",
                job_internal_hostname_template="",
                job_fallback_hostname="default.jobs-dev.neu.ro",
                job_schedule_timeout_s=1,
                job_schedule_scale_up_timeout_s=2,
                is_http_ingress_secure=False,
            )
        )

        assert result == {
            "job_hostname_template": "{job_id}.jobs-dev.neu.ro",
            "job_fallback_hostname": "default.jobs-dev.neu.ro",
            "job_schedule_timeout_s": 1,
            "job_schedule_scale_up_timeout_s": 2,
            "is_http_ingress_secure": False,
        }

    def test_create_patch_orchestrator_request(self, factory: PayloadFactory) -> None:
        result = factory.create_patch_orchestrator_request(
            PatchOrchestratorConfigRequest(
                job_hostname_template="{job_id}.jobs-dev.neu.ro",
                job_internal_hostname_template="{job_id}.platform-jobs",
                job_fallback_hostname="default.jobs-dev.neu.ro",
                job_schedule_timeout_s=1,
                job_schedule_scale_up_timeout_s=2,
                is_http_ingress_secure=False,
                allow_privileged_mode=True,
                allow_job_priority=True,
                resource_pool_types=[ResourcePoolType(name="cpu")],
                resource_presets=[
                    ResourcePreset(
                        name="cpu-micro",
                        credits_per_hour=Decimal(10),
                        cpu=0.1,
                        memory=100,
                    )
                ],
                pre_pull_images=["neuromation/base"],
                idle_jobs=[
                    IdleJobConfig(
                        name="idle",
                        count=1,
                        image="miner",
                        resources=Resources(cpu=1, memory=1024),
                    )
                ],
            )
        )

        assert result == {
            "job_hostname_template": "{job_id}.jobs-dev.neu.ro",
            "job_internal_hostname_template": "{job_id}.platform-jobs",
            "job_fallback_hostname": "default.jobs-dev.neu.ro",
            "job_schedule_timeout_s": 1,
            "job_schedule_scale_up_timeout_s": 2,
            "is_http_ingress_secure": False,
            "resource_pool_types": [mock.ANY],
            "resource_presets": [mock.ANY],
            "allow_privileged_mode": True,
            "allow_job_priority": True,
            "pre_pull_images": ["neuromation/base"],
            "idle_jobs": [
                {
                    "name": "idle",
                    "count": 1,
                    "image": "miner",
                    "resources": {"cpu": 1, "memory": 1024},
                }
            ],
        }

    def test_create_patch_orchestrator_request_default(
        self, factory: PayloadFactory
    ) -> None:
        result = factory.create_patch_orchestrator_request(
            PatchOrchestratorConfigRequest()
        )

        assert result == {}

    def test_create_resource_pool_type(
        self,
        factory: PayloadFactory,
        nvidia_small_gpu: str,
        amd_small_gpu: str,
        intel_small_gpu: str,
    ) -> None:
        result = factory.create_resource_pool_type(
            ResourcePoolType(
                name="n1-highmem-4",
                min_size=1,
                max_size=2,
                idle_size=1,
                cpu=4.0,
                available_cpu=3.0,
                memory=12 * 1024,
                available_memory=10 * 1024,
                disk_size=700,
                available_disk_size=670,
                nvidia_gpu=1,
                amd_gpu=2,
                intel_gpu=3,
                nvidia_gpu_model=nvidia_small_gpu,
                amd_gpu_model=amd_small_gpu,
                intel_gpu_model=intel_small_gpu,
                tpu=TPUResource(
                    ipv4_cidr_block="10.0.0.0/8",
                    types=["tpu"],
                    software_versions=["v1"],
                ),
                is_preemptible=True,
                price=Decimal("1.0"),
                currency="USD",
                cpu_min_watts=1.0,
                cpu_max_watts=2.0,
            )
        )

        assert result == {
            "name": "n1-highmem-4",
            "min_size": 1,
            "max_size": 2,
            "idle_size": 1,
            "cpu": 4.0,
            "available_cpu": 3.0,
            "memory": 12 * 1024,
            "available_memory": 10 * 1024,
            "disk_size": 700,
            "available_disk_size": 670,
            "nvidia_gpu": 1,
            "amd_gpu": 2,
            "intel_gpu": 3,
            "nvidia_gpu_model": nvidia_small_gpu,
            "amd_gpu_model": amd_small_gpu,
            "intel_gpu_model": intel_small_gpu,
            "tpu": {
                "ipv4_cidr_block": "10.0.0.0/8",
                "types": ["tpu"],
                "software_versions": ["v1"],
            },
            "is_preemptible": True,
            "price": "1.0",
            "currency": "USD",
            "cpu_min_watts": 1.0,
            "cpu_max_watts": 2.0,
        }

    def test_create_empty_resource_pool_type(self, factory: PayloadFactory) -> None:
        result = factory.create_resource_pool_type(ResourcePoolType(name="node-pool"))

        assert result == {
            "name": "node-pool",
            "cpu": 1.0,
            "available_cpu": 1.0,
            "memory": 2**30,
            "available_memory": 2**30,
            "disk_size": 150 * 2**30,
            "available_disk_size": 150 * 2**30,
            "idle_size": 0,
            "is_preemptible": False,
            "min_size": 0,
            "max_size": 1,
        }

    def test_create_tpu_resource(self, factory: PayloadFactory) -> None:
        result = factory.create_tpu_resource(
            TPUResource(
                ipv4_cidr_block="10.0.0.0/8", types=["tpu"], software_versions=["v1"]
            )
        )

        assert result == {
            "ipv4_cidr_block": "10.0.0.0/8",
            "types": ["tpu"],
            "software_versions": ["v1"],
        }

    def test_create_resource_preset(self, factory: PayloadFactory) -> None:
        result = factory.create_resource_preset(
            ResourcePreset(
                name="cpu-small",
                credits_per_hour=Decimal("10"),
                cpu=4.0,
                memory=1024,
            )
        )

        assert result == {
            "name": "cpu-small",
            "credits_per_hour": "10",
            "cpu": 4.0,
            "memory": 1024,
        }

    def test_create_resource_preset__custom(self, factory: PayloadFactory) -> None:
        result = factory.create_resource_preset(
            ResourcePreset(
                name="gpu-small",
                credits_per_hour=Decimal("10"),
                cpu=4.0,
                memory=12288,
                nvidia_gpu=1,
                amd_gpu=2,
                intel_gpu=3,
                tpu=TPUPreset(type="tpu", software_version="v1"),
                scheduler_enabled=True,
                preemptible_node=True,
                resource_pool_names=["gpu"],
            )
        )

        assert result == {
            "name": "gpu-small",
            "credits_per_hour": "10",
            "cpu": 4.0,
            "memory": 12288,
            "nvidia_gpu": 1,
            "amd_gpu": 2,
            "intel_gpu": 3,
            "tpu": {"type": "tpu", "software_version": "v1"},
            "scheduler_enabled": True,
            "preemptible_node": True,
            "resource_pool_names": ["gpu"],
        }

    def test_create_storage(self, factory: PayloadFactory) -> None:
        result = factory.create_storage(
            StorageConfig(url=URL("https://storage-dev.neu.ro"))
        )

        assert result == {"url": "https://storage-dev.neu.ro"}

    def test_create_storage_with_volumes(self, factory: PayloadFactory) -> None:
        result = factory.create_storage(
            StorageConfig(
                url=URL("https://storage-dev.neu.ro"),
                volumes=[
                    VolumeConfig(name="test-1"),
                    VolumeConfig(
                        name="test-2",
                        path="/volume",
                        size=1024,
                        credits_per_hour_per_gb=Decimal(123),
                    ),
                ],
            )
        )

        assert result == {
            "url": "https://storage-dev.neu.ro",
            "volumes": [
                {
                    "name": "test-1",
                    "credits_per_hour_per_gb": "0",
                },
                {
                    "name": "test-2",
                    "path": "/volume",
                    "size": 1024,
                    "credits_per_hour_per_gb": "123",
                },
            ],
        }

    def test_create_registry(self, factory: PayloadFactory) -> None:
        result = factory.create_registry(
            RegistryConfig(url=URL("https://registry-dev.neu.ro"))
        )

        assert result == {"url": "https://registry-dev.neu.ro"}

    def test_create_monitoring(self, factory: PayloadFactory) -> None:
        result = factory.create_monitoring(
            MonitoringConfig(url=URL("https://monitoring-dev.neu.ro"))
        )

        assert result == {"url": "https://monitoring-dev.neu.ro"}

    def test_create_secrets(self, factory: PayloadFactory) -> None:
        result = factory.create_secrets(
            SecretsConfig(url=URL("https://secrets-dev.neu.ro"))
        )

        assert result == {"url": "https://secrets-dev.neu.ro"}

    def test_create_metrics(self, factory: PayloadFactory) -> None:
        result = factory.create_metrics(
            MetricsConfig(url=URL("https://metrics-dev.neu.ro"))
        )

        assert result == {"url": "https://metrics-dev.neu.ro"}

    def test_create_dns(self, factory: PayloadFactory) -> None:
        result = factory.create_dns(
            DNSConfig(
                name="neu.ro",
                a_records=[ARecord(name="*.jobs-dev.neu.ro.", ips=["192.168.0.2"])],
            )
        )

        assert result == {
            "name": "neu.ro",
            "a_records": [{"name": "*.jobs-dev.neu.ro.", "ips": ["192.168.0.2"]}],
        }

    def test_create_a_record_with_ips(self, factory: PayloadFactory) -> None:
        result = factory.create_a_record(
            ARecord(name="*.jobs-dev.neu.ro.", ips=["192.168.0.2"])
        )

        assert result == {"name": "*.jobs-dev.neu.ro.", "ips": ["192.168.0.2"]}

    def test_create_a_record_dns_name(self, factory: PayloadFactory) -> None:
        result = factory.create_a_record(
            ARecord(
                name="*.jobs-dev.neu.ro.",
                dns_name="load-balancer",
                zone_id="/hostedzone/1",
                evaluate_target_health=True,
            )
        )

        assert result == {
            "name": "*.jobs-dev.neu.ro.",
            "dns_name": "load-balancer",
            "zone_id": "/hostedzone/1",
            "evaluate_target_health": True,
        }

    def test_create_disks(self, factory: PayloadFactory) -> None:
        result = factory.create_disks(
            DisksConfig(
                url=URL("https://metrics-dev.neu.ro"), storage_limit_per_user=1024
            )
        )

        assert result == {
            "url": "https://metrics-dev.neu.ro",
            "storage_limit_per_user": 1024,
        }

    def test_create_buckets(self, factory: PayloadFactory) -> None:
        result = factory.create_buckets(
            BucketsConfig(url=URL("https://buckets-dev.neu.ro"), disable_creation=True)
        )

        assert result == {"url": "https://buckets-dev.neu.ro", "disable_creation": True}

    def test_create_ingress(self, factory: PayloadFactory) -> None:
        result = factory.create_ingress(
            IngressConfig(
                acme_environment=ACMEEnvironment.PRODUCTION,
                additional_cors_origins=["https://custom.app"],
            )
        )

        assert result == {
            "acme_environment": "production",
            "additional_cors_origins": ["https://custom.app"],
        }

    def test_create_ingress_defaults(self, factory: PayloadFactory) -> None:
        result = factory.create_ingress(
            IngressConfig(acme_environment=ACMEEnvironment.PRODUCTION)
        )

        assert result == {"acme_environment": "production"}

    @pytest.fixture
    def credentials(self) -> CredentialsConfig:
        return CredentialsConfig(
            neuro=NeuroAuthConfig(
                url=URL("https://neu.ro"),
                token="cluster_token",
            ),
            neuro_registry=DockerRegistryConfig(
                url=URL("https://ghcr.io/neuro-inc"),
                username="username",
                password="password",
                email="username@neu.ro",
            ),
            neuro_helm=HelmRegistryConfig(
                url=URL("oci://neuro-inc.ghcr.io"),
                username="username",
                password="password",
            ),
            grafana=GrafanaCredentials(
                username="username",
                password="password",
            ),
            sentry=SentryCredentials(
                client_key_id="key", public_dsn=URL("dsn"), sample_rate=0.2
            ),
            docker_hub=DockerRegistryConfig(
                url=URL("https://index.docker.io/v1"),
                username="test",
                password="password",
                email="test@neu.ro",
            ),
            minio=MinioCredentials(
                username="test",
                password="password",
            ),
            emc_ecs=EMCECSCredentials(
                access_key_id="key_id",
                secret_access_key="secret_key",
                s3_endpoint=URL("https://emc-ecs.s3"),
                management_endpoint=URL("https://emc-ecs.management"),
                s3_assumable_role="s3-role",
            ),
            open_stack=OpenStackCredentials(
                account_id="id",
                password="password",
                s3_endpoint=URL("https://os.s3"),
                endpoint=URL("https://os.management"),
                region_name="region",
            ),
        )

    def test_create_credentials(
        self, factory: PayloadFactory, credentials: CredentialsConfig
    ) -> None:
        result = factory.create_credentials(credentials)

        assert result == {
            "neuro": {"token": "cluster_token"},
            "neuro_registry": {"username": "username", "password": "password"},
            "neuro_helm": {"username": "username", "password": "password"},
            "grafana": {
                "username": "username",
                "password": "password",
            },
            "sentry": {
                "client_key_id": "key",
                "public_dsn": "dsn",
                "sample_rate": 0.2,
            },
            "docker_hub": {"username": "test", "password": "password"},
            "minio": {
                "username": "test",
                "password": "password",
            },
            "emc_ecs": {
                "access_key_id": "key_id",
                "secret_access_key": "secret_key",
                "s3_endpoint": "https://emc-ecs.s3",
                "management_endpoint": "https://emc-ecs.management",
                "s3_assumable_role": "s3-role",
            },
            "open_stack": {
                "account_id": "id",
                "password": "password",
                "s3_endpoint": "https://os.s3",
                "endpoint": "https://os.management",
                "region_name": "region",
            },
        }

    def test_create_minimal_credentials(
        self, factory: PayloadFactory, credentials: CredentialsConfig
    ) -> None:
        credentials = replace(
            credentials,
            grafana=None,
            sentry=None,
            docker_hub=None,
            minio=None,
            emc_ecs=None,
            open_stack=None,
        )
        result = factory.create_credentials(credentials)

        assert result == {
            "neuro": {"token": "cluster_token"},
            "neuro_registry": {"username": "username", "password": "password"},
            "neuro_helm": {"username": "username", "password": "password"},
        }

    @pytest.fixture
    def node_pool(self) -> NodePool:
        return NodePool(
            name="my-node-pool",
            min_size=0,
            max_size=10,
            idle_size=1,
            machine_type="some-machine-type",
            cpu=10,
            available_cpu=9,
            memory=2048,
            available_memory=1024,
            disk_size=100500,
            available_disk_size=100000,
            disk_type="some-disk-type",
            nvidia_gpu=1,
            nvidia_gpu_model="some-gpu-model",
            price=Decimal(180),
            currency="rabbits",
            is_preemptible=True,
            zones=("here", "there"),
            cpu_min_watts=0.01,
            cpu_max_watts=1000,
        )

    def test_create_add_node_pool_request(self, factory: PayloadFactory) -> None:
        node_pool = AddNodePoolRequest(
            name="my-node-pool",
            min_size=0,
            max_size=10,
            idle_size=1,
            machine_type="some-machine-type",
            cpu=10,
            available_cpu=9,
            memory=2048,
            available_memory=1024,
            disk_size=100500,
            available_disk_size=100000,
            disk_type="some-disk-type",
            nvidia_gpu=1,
            nvidia_gpu_model="some-gpu-model",
            price=Decimal(180),
            currency="rabbits",
            is_preemptible=True,
            zones=("here", "there"),
            cpu_min_watts=0.01,
            cpu_max_watts=1000,
        )
        payload = factory.create_add_node_pool_request(node_pool)

        assert payload == {
            "name": "my-node-pool",
            "role": "platform_job",
            "min_size": 0,
            "max_size": 10,
            "idle_size": 1,
            "is_preemptible": True,
            "machine_type": "some-machine-type",
            "cpu": 10,
            "available_cpu": 9,
            "memory": 2048,
            "available_memory": 1024,
            "disk_size": 100500,
            "available_disk_size": 100000,
            "disk_type": "some-disk-type",
            "nvidia_gpu": 1,
            "nvidia_gpu_model": "some-gpu-model",
            "zones": ("here", "there"),
            "price": "180",
            "currency": "rabbits",
            "cpu_min_watts": 0.01,
            "cpu_max_watts": 1000,
        }

    def test_create_add_node_pool_request_default(
        self, factory: PayloadFactory
    ) -> None:
        node_pool = AddNodePoolRequest(name="my-node-pool", min_size=0, max_size=1)

        payload = factory.create_add_node_pool_request(node_pool)

        assert payload == {
            "name": "my-node-pool",
            "role": "platform_job",
            "min_size": 0,
            "max_size": 1,
        }

    def test_create_patch_node_pool_size_request(self, factory: PayloadFactory) -> None:
        payload = factory.create_patch_node_pool_request(
            PatchNodePoolSizeRequest(min_size=1, max_size=3, idle_size=2)
        )

        assert payload == {
            "min_size": 1,
            "max_size": 3,
            "idle_size": 2,
        }

    def test_create_patch_node_pool_size_request_default(
        self, factory: PayloadFactory
    ) -> None:
        payload = factory.create_patch_node_pool_request(PatchNodePoolSizeRequest())

        assert payload == {}

    def test_create_patch_node_pool_resources_request(
        self, factory: PayloadFactory
    ) -> None:
        payload = factory.create_patch_node_pool_request(
            PatchNodePoolResourcesRequest(
                min_size=0,
                max_size=10,
                machine_type="n1-highmem-8",
                cpu=1,
                available_cpu=0.9,
                memory=1024,
                available_memory=1023,
                disk_size=100,
                available_disk_size=75,
                nvidia_gpu=1,
                nvidia_gpu_model="nvidia-gpu",
                amd_gpu=1,
                amd_gpu_model="amd-gpu",
                intel_gpu=1,
                intel_gpu_model="intel-gpu",
            )
        )

        assert payload == {
            "min_size": 0,
            "max_size": 10,
            "machine_type": "n1-highmem-8",
            "cpu": 1,
            "available_cpu": 0.9,
            "memory": 1024,
            "available_memory": 1023,
            "disk_size": 100,
            "available_disk_size": 75,
            "nvidia_gpu": 1,
            "nvidia_gpu_model": "nvidia-gpu",
            "amd_gpu": 1,
            "amd_gpu_model": "amd-gpu",
            "intel_gpu": 1,
            "intel_gpu_model": "intel-gpu",
        }

    def test_create_patch_node_pool_resources_request_default(
        self, factory: PayloadFactory
    ) -> None:
        payload = factory.create_patch_node_pool_request(
            PatchNodePoolResourcesRequest(
                cpu=1,
                available_cpu=0.9,
                memory=1024,
                available_memory=1023,
                disk_size=100,
                available_disk_size=75,
            )
        )

        assert payload == {
            "cpu": 1,
            "available_cpu": 0.9,
            "memory": 1024,
            "available_memory": 1023,
            "disk_size": 100,
            "available_disk_size": 75,
        }

    def test_create_energy(self, factory: PayloadFactory) -> None:
        timezone = ZoneInfo("America/Los_Angeles")
        energy = factory.create_energy(
            EnergyConfig(
                co2_grams_eq_per_kwh=100,
                schedules=[
                    EnergySchedule(name="default", price_per_kwh=Decimal("246.8")),
                    EnergySchedule(
                        name="green",
                        price_per_kwh=Decimal("123.4"),
                        periods=[
                            EnergySchedulePeriod(
                                weekday=1,
                                start_time=time(hour=23, minute=0, tzinfo=timezone),
                                end_time=time(hour=0, minute=0, tzinfo=timezone),
                            )
                        ],
                    ),
                ],
            )
        )

        assert energy == {
            "co2_grams_eq_per_kwh": 100,
            "schedules": [
                {"name": "default", "price_per_kwh": "246.8"},
                {
                    "name": "green",
                    "price_per_kwh": "123.4",
                    "periods": [
                        {"weekday": 1, "start_time": "23:00", "end_time": "00:00"}
                    ],
                },
            ],
        }

    @pytest.fixture
    def apps(self) -> AppsConfig:
        return AppsConfig(
            apps_hostname_templates=["{app_name}.apps.default.org.neu.ro"],
            app_proxy_url=URL("outputs-proxy.apps.default.org.neu.ro"),
        )

    def test_create_apps(self, factory: PayloadFactory, apps: AppsConfig) -> None:
        result = factory.create_apps(apps)
        assert result == {
            "apps_hostname_templates": ["{app_name}.apps.default.org.neu.ro"],
            "app_proxy_url": "outputs-proxy.apps.default.org.neu.ro",
        }

    def test_create_patch_cluster_request_with_apps(
        self, factory: PayloadFactory, credentials: CredentialsConfig, apps: AppsConfig
    ) -> None:
        result = factory.create_patch_cluster_request(
            PatchClusterRequest(
                credentials=credentials,
                storage=StorageConfig(url=URL("https://storage-dev.neu.ro")),
                registry=RegistryConfig(url=URL("https://registry-dev.neu.ro")),
                orchestrator=PatchOrchestratorConfigRequest(),
                monitoring=MonitoringConfig(url=URL("https://monitoring-dev.neu.ro")),
                secrets=SecretsConfig(url=URL("https://secrets-dev.neu.ro")),
                metrics=MetricsConfig(url=URL("https://metrics-dev.neu.ro")),
                disks=DisksConfig(
                    url=URL("https://metrics-dev.neu.ro"), storage_limit_per_user=1024
                ),
                buckets=BucketsConfig(
                    url=URL("https://buckets-dev.neu.ro"), disable_creation=True
                ),
                ingress=IngressConfig(acme_environment=ACMEEnvironment.PRODUCTION),
                dns=DNSConfig(
                    name="neu.ro",
                    a_records=[ARecord(name="*.jobs-dev.neu.ro.", ips=["192.168.0.2"])],
                ),
                timezone=ZoneInfo("America/Los_Angeles"),
                energy=EnergyConfig(co2_grams_eq_per_kwh=100),
                apps=apps,
            )
        )

        assert result == {
            "credentials": mock.ANY,
            "storage": mock.ANY,
            "registry": mock.ANY,
            "orchestrator": mock.ANY,
            "monitoring": mock.ANY,
            "secrets": mock.ANY,
            "metrics": mock.ANY,
            "disks": mock.ANY,
            "buckets": mock.ANY,
            "ingress": mock.ANY,
            "dns": mock.ANY,
            "timezone": "America/Los_Angeles",
            "energy": mock.ANY,
            "apps": {
                "apps_hostname_templates": ["{app_name}.apps.default.org.neu.ro"],
                "app_proxy_url": "outputs-proxy.apps.default.org.neu.ro",
            },
        }
