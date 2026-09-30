"""Pulumi IaC for the Airmux control plane, console, and gateway edge.

Architecture (prod and `-preview` twin):
  Cloud Run control plane (single replica) <- Cloud SQL Postgres
  Cloud Run console <- external HTTPS LB + IAP (browser users)
  Regional internal HTTPS ALB <- PSC service attachment <- agent-plane VPC

Pulumi owns the Artifact Registry remote repository and every Secret
Manager secret/version; only the deployer IAM delta is bootstrap.
`AIRMUX_VERSION` pins one release tag used by every service and job.
Pulumi ignores service image changes after creation (the `airmux-migrate`
and `airmux-taxonomy` job images are Pulumi-managed so their
token-triggered executions run the pinned head); roll images with
`.github/workflows/deploy-airmux-command.yml` (preview via
`/deploy-airmux` or dispatch, production via `target=production` dispatch).

The console image's nginx proxies `/api/` over HTTP to its configured
upstream. Consequently the external URL map routes `/api` and `/api/*`
directly to the control-plane backend, while the console receives browser
assets. The gateway URL map exposes only the Airmux data-plane API paths.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pulumi
import pulumi_gcp as gcp
import pulumi_random as random

config = pulumi.Config()
gcp_config = pulumi.Config("gcp")
PROJECT = gcp_config.require("project")
PROJECT_NUMBER = gcp.organizations.get_project_output(project_id=PROJECT).number
REGION = gcp_config.get("region") or "us-west3"
DNS_ZONE_PROJECT = config.get("dns-zone-project") or "airbyte-intranet"
DNS_ZONE_NAME = config.get("dns-zone-name") or "internal-airbyte-ai"
PSC_CONSUMERS = config.get_object("psc-consumer-projects") or [
    "airbyte-agent-plane-dev"
]
CONFIG_SECRET = config.get("config-secret-id") or "airmux-config"
# Provider env var -> full cross-project secret resource name; the control
# plane's env secrets store only accepts a credential matching its own env.
PROVIDER_KEY_SECRETS = config.get_object("provider-key-secrets") or {}

# One pinned release tag for every service/job; the deploy workflow resolves
# it to a digest through the `airmux-upstream` remote repo.
AIRMUX_VERSION = Path(__file__).with_name("AIRMUX_VERSION").read_text().strip()
IMAGE = (
    "us-west3-docker.pkg.dev/internal-airbyte-ai-infra/airmux-upstream/"
    f"michel-tricot/airmux:{AIRMUX_VERSION}"
)
# Execution-name suffix for the in-apply jobs; tokens accept only [a-z0-9-].
JOB_EXECUTION_TOKEN = re.sub(r"[^a-z0-9-]", "-", AIRMUX_VERSION.lower())


@dataclass(frozen=True)
class Variant:
    """One deployment of the control plane (prod or `-preview` twin)."""

    suffix: str  # "" for prod, "-preview" for the preview twin
    console_domain: str
    gateway_domain: str
    db_name: str
    database_url_secret: str
    management_key_secret: str
    runtime_sa_id: str
    db_user: str


PROD = Variant(
    suffix="",
    console_domain=config.get("console-domain") or "airmux.internal.airbyte.ai",
    gateway_domain=config.get("gateway-domain") or "airmux-cp.internal.airbyte.ai",
    db_name="airmux",
    database_url_secret=config.get("database-url-secret-id") or "airmux-database-url",
    management_key_secret=(
        config.get("management-key-secret-id") or "airmux-dataplane-management-key"
    ),
    runtime_sa_id="airmux-cp-sa",
    db_user="airmux",
)
PREVIEW = Variant(
    suffix="-preview",
    console_domain=(
        config.get("preview-console-domain") or "preview.airmux.internal.airbyte.ai"
    ),
    gateway_domain=(
        config.get("preview-gateway-domain") or "airmux-cp-preview.internal.airbyte.ai"
    ),
    db_name="airmux_preview",
    database_url_secret=(
        config.get("preview-database-url-secret-id") or "airmux-preview-database-url"
    ),
    management_key_secret=(
        config.get("preview-management-key-secret-id")
        or "airmux-preview-dataplane-management-key"
    ),
    runtime_sa_id="airmux-cp-sa-preview",
    db_user="airmux_preview",
)
VARIANTS = (PROD, PREVIEW)


def _env(
    name: str, value: pulumi.Input[str]
) -> gcp.cloudrunv2.ServiceTemplateContainerEnvArgs:
    return gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(name=name, value=value)


def _secret_env(
    name: str, secret: str
) -> gcp.cloudrunv2.ServiceTemplateContainerEnvArgs:
    return gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
        name=name,
        value_source=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceArgs(
            secret_key_ref=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceSecretKeyRefArgs(
                secret=secret, version="latest"
            )
        ),
    )


def _secret_volume(
    secret: str, version: pulumi.Input[str]
) -> gcp.cloudrunv2.ServiceTemplateVolumeArgs:
    # The version is templated (not `latest`) so a new SecretVersion changes
    # the Service/Job template and rolls a revision that picks up the config.
    return gcp.cloudrunv2.ServiceTemplateVolumeArgs(
        name="airmux-config",
        secret=gcp.cloudrunv2.ServiceTemplateVolumeSecretArgs(
            secret=secret,
            items=[
                gcp.cloudrunv2.ServiceTemplateVolumeSecretItemArgs(
                    path="airmux.yml", version=version
                )
            ],
        ),
    )


def _cloud_sql_volume(
    connection_name: pulumi.Input[str],
) -> gcp.cloudrunv2.ServiceTemplateVolumeArgs:
    return gcp.cloudrunv2.ServiceTemplateVolumeArgs(
        name="cloudsql",
        cloud_sql_instance=gcp.cloudrunv2.ServiceTemplateVolumeCloudSqlInstanceArgs(
            instances=[connection_name]
        ),
    )


def define_apis() -> list[gcp.projects.Service]:
    """Enable APIs required by this stack."""
    api_ids = [
        "artifactregistry.googleapis.com",
        "certificatemanager.googleapis.com",
        "compute.googleapis.com",
        "dns.googleapis.com",
        "iam.googleapis.com",
        "iap.googleapis.com",
        "run.googleapis.com",
        "secretmanager.googleapis.com",
        "sqladmin.googleapis.com",
    ]
    return [
        gcp.projects.Service(
            f"enable-{api_id.replace('.', '-')}",
            service=api_id,
            project=PROJECT,
            disable_on_destroy=False,
        )
        for api_id in api_ids
    ]


def define_artifact_repo(
    api_services: list[gcp.projects.Service],
) -> gcp.artifactregistry.Repository:
    """Remote AR repo mirroring ghcr.io; the deploy workflow pulls through it
    and pins RepoDigests[0]."""
    return gcp.artifactregistry.Repository(
        "airmux-upstream",
        repository_id="airmux-upstream",
        project=PROJECT,
        location=REGION,
        format="DOCKER",
        mode="REMOTE_REPOSITORY",
        remote_repository_config=gcp.artifactregistry.RepositoryRemoteRepositoryConfigArgs(
            # Per-format blocks are mutually exclusive with common_repository;
            # a DOCKER-format remote uses common_repository.uri alone.
            common_repository=gcp.artifactregistry.RepositoryRemoteRepositoryConfigCommonRepositoryArgs(
                uri="https://ghcr.io"
            ),
        ),
        description="Public Airmux images from GHCR",
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )


def define_network(
    api_services: list[gcp.projects.Service],
) -> tuple[
    gcp.compute.Network,
    gcp.compute.Subnetwork,
    gcp.compute.Subnetwork,
    gcp.compute.Subnetwork,
]:
    network = gcp.compute.Network(
        "airmux-net",
        name="airmux-net",
        project=PROJECT,
        auto_create_subnetworks=False,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    proxy = gcp.compute.Subnetwork(
        "airmux-proxy-only",
        name="airmux-proxy-only",
        project=PROJECT,
        region=REGION,
        network=network.id,
        ip_cidr_range="10.82.0.0/23",
        purpose="REGIONAL_MANAGED_PROXY",
        role="ACTIVE",
    )
    psc_nat = gcp.compute.Subnetwork(
        "airmux-psc-nat",
        name="airmux-psc-nat",
        project=PROJECT,
        region=REGION,
        network=network.id,
        ip_cidr_range="10.82.2.0/24",
        purpose="PRIVATE_SERVICE_CONNECT",
    )
    ilb = gcp.compute.Subnetwork(
        "airmux-ilb",
        name="airmux-ilb",
        project=PROJECT,
        region=REGION,
        network=network.id,
        ip_cidr_range="10.82.3.0/24",
    )
    return network, proxy, psc_nat, ilb


def define_sql(
    api_services: list[gcp.projects.Service],
) -> tuple[
    dict[Variant, gcp.sql.DatabaseInstance],
    dict[Variant, gcp.secretmanager.Secret],
    dict[Variant, gcp.secretmanager.SecretVersion],
    dict[Variant, gcp.sql.Database],
    dict[Variant, gcp.sql.User],
]:
    """One Cloud SQL instance per variant for instance-level prod/preview
    isolation. Passwords are Pulumi-generated and live only in state; Pulumi
    also owns the per-variant DATABASE_URL secret it composes. Databases and
    users are `protect`ed: a leaked/preview credential must never cascade a
    destructive drop.
    """
    instances: dict[Variant, gcp.sql.DatabaseInstance] = {}
    url_secrets: dict[Variant, gcp.secretmanager.Secret] = {}
    url_versions: dict[Variant, gcp.secretmanager.SecretVersion] = {}
    databases: dict[Variant, gcp.sql.Database] = {}
    users: dict[Variant, gcp.sql.User] = {}
    for variant in VARIANTS:
        instance = gcp.sql.DatabaseInstance(
            f"airmux-sql{variant.suffix}",
            name=f"airmux{variant.suffix}",
            project=PROJECT,
            region=REGION,
            database_version="POSTGRES_16",
            deletion_protection=True,
            settings=gcp.sql.DatabaseInstanceSettingsArgs(
                tier="db-f1-micro",
                edition="ENTERPRISE",
                availability_type="ZONAL",
                deletion_protection_enabled=True,
                backup_configuration=gcp.sql.DatabaseInstanceSettingsBackupConfigurationArgs(
                    enabled=True,
                    point_in_time_recovery_enabled=True,
                    start_time="03:00",
                ),
            ),
            opts=pulumi.ResourceOptions(depends_on=api_services),
        )
        instances[variant] = instance
        databases[variant] = gcp.sql.Database(
            f"airmux-database{variant.suffix}",
            name=variant.db_name,
            instance=instance.name,
            project=PROJECT,
            opts=pulumi.ResourceOptions(protect=True, depends_on=[instance]),
        )
        pwd = random.RandomPassword(
            f"airmux-db-password{variant.suffix}",
            length=32,
            special=False,
        )
        users[variant] = gcp.sql.User(
            f"airmux-db-user{variant.suffix}",
            name=variant.db_user,
            instance=instance.name,
            project=PROJECT,
            password=pwd.result,
            opts=pulumi.ResourceOptions(protect=True, depends_on=[instance]),
        )
        secret = gcp.secretmanager.Secret(
            f"airmux-database-url{variant.suffix}",
            secret_id=variant.database_url_secret,
            project=PROJECT,
            replication=gcp.secretmanager.SecretReplicationArgs(
                auto=gcp.secretmanager.SecretReplicationAutoArgs()
            ),
            opts=pulumi.ResourceOptions(depends_on=api_services),
        )
        url_secrets[variant] = secret
        url_versions[variant] = gcp.secretmanager.SecretVersion(
            f"airmux-database-url{variant.suffix}",
            secret=secret.id,
            secret_data=pulumi.Output.all(instance.connection_name, pwd.result).apply(
                lambda a, v=variant: (
                    f"postgresql+asyncpg://{v.db_user}:{a[1]}"
                    f"@/{v.db_name}?host=/cloudsql/{a[0]}"
                )
            ),
        )
    return instances, url_secrets, url_versions, databases, users


def define_secrets(
    api_services: list[gcp.projects.Service],
) -> tuple[
    dict[Variant, gcp.secretmanager.Secret],
    dict[Variant, gcp.secretmanager.SecretVersion],
    dict[Variant, pulumi.Output[str]],
    gcp.secretmanager.Secret,
    gcp.secretmanager.SecretVersion,
]:
    """Pulumi-owned secrets: per-variant management keys + shared airmux config.

    The management key is a generated `sk-cp-` token (airmux only hashes it);
    the config secret publishes the checked-in airmux.yml verbatim.
    """
    mgmt_secrets: dict[Variant, gcp.secretmanager.Secret] = {}
    mgmt_versions: dict[Variant, gcp.secretmanager.SecretVersion] = {}
    mgmt_keys: dict[Variant, pulumi.Output[str]] = {}
    for variant in VARIANTS:
        pwd = random.RandomPassword(
            f"airmux-management-key{variant.suffix}", length=48, special=False
        )
        key = pwd.result.apply(lambda r: f"sk-cp-{r}")
        mgmt_keys[variant] = key
        secret = gcp.secretmanager.Secret(
            f"airmux-management-key{variant.suffix}",
            secret_id=variant.management_key_secret,
            project=PROJECT,
            replication=gcp.secretmanager.SecretReplicationArgs(
                auto=gcp.secretmanager.SecretReplicationAutoArgs()
            ),
            opts=pulumi.ResourceOptions(depends_on=api_services),
        )
        mgmt_secrets[variant] = secret
        mgmt_versions[variant] = gcp.secretmanager.SecretVersion(
            f"airmux-management-key{variant.suffix}",
            secret=secret.id,
            secret_data=key,
        )
    config_secret = gcp.secretmanager.Secret(
        "airmux-config",
        secret_id=CONFIG_SECRET,
        project=PROJECT,
        replication=gcp.secretmanager.SecretReplicationArgs(
            auto=gcp.secretmanager.SecretReplicationAutoArgs()
        ),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    config_version = gcp.secretmanager.SecretVersion(
        "airmux-config",
        secret=config_secret.id,
        secret_data=Path(__file__).with_name("airmux.yml").read_text(),
    )
    return mgmt_secrets, mgmt_versions, mgmt_keys, config_secret, config_version


def define_runtime_identity(
    api_services: list[gcp.projects.Service],
) -> tuple[dict[Variant, gcp.serviceaccount.Account], gcp.serviceaccount.Account]:
    runtime = {
        variant: gcp.serviceaccount.Account(
            variant.runtime_sa_id,
            account_id=variant.runtime_sa_id,
            display_name=f"Airmux control plane runtime{variant.suffix}",
            project=PROJECT,
            opts=pulumi.ResourceOptions(depends_on=api_services),
        )
        for variant in VARIANTS
    }
    console = gcp.serviceaccount.Account(
        "airmux-console-sa",
        account_id="airmux-console-sa",
        display_name="Airmux console runtime",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    return runtime, console


def _service(
    name: str,
    args: gcp.cloudrunv2.ServiceTemplateArgs,
    api_services: list[gcp.projects.Service],
    *,
    iap_identity: gcp.projects.ServiceIdentity,
    allow_all: bool = False,
    extra_depends: list[pulumi.Resource] | None = None,
) -> gcp.cloudrunv2.Service:
    service = gcp.cloudrunv2.Service(
        name,
        name=name,
        project=PROJECT,
        location=REGION,
        deletion_protection=False,
        ingress="INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER",
        template=args,
        opts=pulumi.ResourceOptions(
            depends_on=[*api_services, *(extra_depends or [])],
            ignore_changes=["scaling", "template.containers[*].image"],
        ),
    )
    gcp.cloudrunv2.ServiceIamMember(
        f"{name}-invoker",
        project=PROJECT,
        location=REGION,
        name=service.name,
        role="roles/run.invoker",
        member=(
            "allUsers"
            if allow_all
            else iap_identity.email.apply(lambda email: f"serviceAccount:{email}")
        ),
        opts=pulumi.ResourceOptions(depends_on=[service, iap_identity]),
    )
    return service


def _runtime_template(
    service_account: gcp.serviceaccount.Account,
    sql_connection: pulumi.Input[str],
    envs: list[gcp.cloudrunv2.ServiceTemplateContainerEnvArgs],
    volumes: list[gcp.cloudrunv2.ServiceTemplateVolumeArgs],
    args: list[str],
    port: int,
    memory: str,
) -> gcp.cloudrunv2.ServiceTemplateArgs:
    return gcp.cloudrunv2.ServiceTemplateArgs(
        service_account=service_account.email,
        scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
            min_instance_count=1, max_instance_count=1
        ),
        volumes=[*volumes, _cloud_sql_volume(sql_connection)],
        containers=[
            gcp.cloudrunv2.ServiceTemplateContainerArgs(
                image=IMAGE,
                args=args,
                ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                    container_port=port
                ),
                resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                    limits={"cpu": "1", "memory": memory}, startup_cpu_boost=True
                ),
                envs=envs,
                volume_mounts=[
                    gcp.cloudrunv2.ServiceTemplateContainerVolumeMountArgs(
                        name="airmux-config", mount_path="/config"
                    ),
                    gcp.cloudrunv2.ServiceTemplateContainerVolumeMountArgs(
                        name="cloudsql", mount_path="/cloudsql"
                    ),
                ],
                startup_probe=gcp.cloudrunv2.ServiceTemplateContainerStartupProbeArgs(
                    http_get=gcp.cloudrunv2.ServiceTemplateContainerStartupProbeHttpGetArgs(
                        path="/healthz", port=port
                    ),
                    period_seconds=10,
                    timeout_seconds=5,
                    failure_threshold=12,
                ),
            )
        ],
    )


def define_services(
    api_services: list[gcp.projects.Service],
    runtime_sas: dict[Variant, gcp.serviceaccount.Account],
    console_sa: gcp.serviceaccount.Account,
    sql_instance: gcp.sql.DatabaseInstance,
    secret_versions: list[pulumi.Resource],
    migrate_depends: list[pulumi.Resource],
    config_version: gcp.secretmanager.SecretVersion,
    iap_identity: gcp.projects.ServiceIdentity,
    variant: Variant,
) -> tuple[
    gcp.cloudrunv2.Service,
    gcp.cloudrunv2.Service,
    gcp.cloudrunv2.Job,
    gcp.cloudrunv2.Job,
]:
    service_account = runtime_sas[variant]
    connection = sql_instance.connection_name
    common = [
        _secret_env("DATABASE_URL", variant.database_url_secret),
        _env("AIRMUX_CONSOLE_URL", f"https://{variant.console_domain}"),
        _secret_env("AIRMUX_DATAPLANE_MANAGEMENT_KEY", variant.management_key_secret),
        _env("FORWARDED_ALLOW_IPS", "*"),
    ]
    # Only the control plane needs the vendor keys: airmux's `env` secrets
    # store accepts a credential only when its value matches the process env.
    control_env = [
        *common,
        *[
            _secret_env(env_name, secret_ref)
            for env_name, secret_ref in PROVIDER_KEY_SECRETS.items()
        ],
    ]
    config_volume = _secret_volume(CONFIG_SECRET, config_version.version)

    def job_template(command: str) -> gcp.cloudrunv2.JobTemplateArgs:
        return gcp.cloudrunv2.JobTemplateArgs(
            template=gcp.cloudrunv2.JobTemplateTemplateArgs(
                service_account=service_account.email,
                max_retries=1,
                timeout="3600s",
                volumes=[config_volume, _cloud_sql_volume(connection)],
                containers=[
                    gcp.cloudrunv2.JobTemplateTemplateContainerArgs(
                        image=IMAGE,
                        args=[command],
                        envs=common,
                        volume_mounts=[
                            gcp.cloudrunv2.JobTemplateTemplateContainerVolumeMountArgs(
                                name="airmux-config", mount_path="/config"
                            ),
                            gcp.cloudrunv2.JobTemplateTemplateContainerVolumeMountArgs(
                                name="cloudsql", mount_path="/cloudsql"
                            ),
                        ],
                    )
                ],
            )
        )

    migrate = gcp.cloudrunv2.Job(
        f"airmux-migrate{variant.suffix}",
        name=f"airmux-migrate{variant.suffix}",
        project=PROJECT,
        location=REGION,
        template=job_template("migrate"),
        # The job becomes ready only once an execution completes, and it
        # re-executes whenever this token changes — i.e., on every image
        # bump. This keeps the control plane off an empty/behind schema
        # (upstream refuses to start there) with no manual step.
        run_execution_token=JOB_EXECUTION_TOKEN,
        # No ignore_changes on this job's image: the apply must deploy the new
        # tag BEFORE its token-triggered execution, otherwise the in-apply
        # migration would run the previously deployed image.
        opts=pulumi.ResourceOptions(
            depends_on=[
                *api_services,
                sql_instance,
                *secret_versions,
                *migrate_depends,
            ],
        ),
    )
    taxonomy = gcp.cloudrunv2.Job(
        f"airmux-taxonomy{variant.suffix}",
        name=f"airmux-taxonomy{variant.suffix}",
        project=PROJECT,
        location=REGION,
        template=job_template("taxonomy"),
        # Same token mechanics as migrate: run once on first apply and on
        # every image bump, after the schema exists; no ignore_changes so
        # the apply deploys the new tag before the execution fires.
        run_execution_token=JOB_EXECUTION_TOKEN,
        opts=pulumi.ResourceOptions(
            depends_on=[*api_services, sql_instance, *secret_versions, migrate],
        ),
    )
    control = _service(
        f"airmux-control-plane{variant.suffix}",
        _runtime_template(
            service_account,
            connection,
            control_env,
            [config_volume],
            ["control-plane"],
            8000,
            "1Gi",
        ),
        api_services,
        iap_identity=iap_identity,
        allow_all=True,
        # Wait on the secrets it reads and on migrate+taxonomy having run
        # once — the control plane refuses to start on an empty/behind
        # schema.
        extra_depends=[*secret_versions, migrate, taxonomy],
    )
    console_env = [
        _env("AIRMUX_CONSOLE_URL", f"https://{variant.console_domain}"),
        _env("CONTROL_PLANE_UPSTREAM", "127.0.0.1:9"),
        _env("DATA_PLANE_UPSTREAM", "127.0.0.1:9"),
    ]
    console = _service(
        f"airmux-console{variant.suffix}",
        gcp.cloudrunv2.ServiceTemplateArgs(
            service_account=console_sa.email,
            scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
                min_instance_count=1, max_instance_count=1
            ),
            containers=[
                gcp.cloudrunv2.ServiceTemplateContainerArgs(
                    image=IMAGE,
                    args=["console"],
                    ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                        container_port=8080
                    ),
                    envs=console_env,
                    resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                        limits={"cpu": "1", "memory": "512Mi"}, startup_cpu_boost=True
                    ),
                    # The console's /healthz is an nginx auth_request to the
                    # dummy upstreams and always 503s; `/` serves index.html.
                    startup_probe=gcp.cloudrunv2.ServiceTemplateContainerStartupProbeArgs(
                        http_get=gcp.cloudrunv2.ServiceTemplateContainerStartupProbeHttpGetArgs(
                            path="/", port=8080
                        )
                    ),
                )
            ],
        ),
        api_services,
        iap_identity=iap_identity,
    )

    return control, console, migrate, taxonomy


def _neg(
    name: str, service: gcp.cloudrunv2.Service
) -> gcp.compute.RegionNetworkEndpointGroup:
    return gcp.compute.RegionNetworkEndpointGroup(
        name,
        name=name,
        project=PROJECT,
        region=REGION,
        network_endpoint_type="SERVERLESS",
        cloud_run=gcp.compute.RegionNetworkEndpointGroupCloudRunArgs(
            service=service.name
        ),
    )


def _iap_backend(
    name: str, neg: gcp.compute.RegionNetworkEndpointGroup
) -> gcp.compute.BackendService:
    return gcp.compute.BackendService(
        name,
        name=name,
        project=PROJECT,
        protocol="HTTP",
        port_name="http",
        backends=[gcp.compute.BackendServiceBackendArgs(group=neg.id)],
        iap=gcp.compute.BackendServiceIapArgs(
            enabled=True, oauth2_client_id=" ", oauth2_client_secret=" "
        ),
    )


def define_external_lb(
    services: dict[Variant, tuple[gcp.cloudrunv2.Service, gcp.cloudrunv2.Service]],
    api_services: list[gcp.projects.Service],
) -> gcp.compute.GlobalAddress:
    backends: dict[
        Variant, tuple[gcp.compute.BackendService, gcp.compute.BackendService]
    ] = {}
    for variant, (control, console) in services.items():
        cneg = _neg(f"console-neg{variant.suffix}", console)
        pneg = _neg(f"control-neg{variant.suffix}", control)
        cb = _iap_backend(f"console-backend{variant.suffix}", cneg)
        pb = _iap_backend(f"control-backend{variant.suffix}", pneg)
        backends[variant] = (cb, pb)
        for name, backend in [("console", cb), ("control", pb)]:
            gcp.iap.WebBackendServiceIamMember(
                f"{name}-iap-domain{variant.suffix}",
                project=PROJECT,
                web_backend_service=backend.name,
                role="roles/iap.httpsResourceAccessor",
                member="domain:airbyte.io",
            )
    address = gcp.compute.GlobalAddress(
        "airmux-console-ip",
        name="airmux-console-ip",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    cert = gcp.compute.ManagedSslCertificate(
        "airmux-console-cert",
        name="airmux-console-cert",
        project=PROJECT,
        managed=gcp.compute.ManagedSslCertificateManagedArgs(
            domains=[variant.console_domain for variant in VARIANTS]
        ),
    )
    urlmap = gcp.compute.URLMap(
        "airmux-console-url-map",
        name="airmux-console-url-map",
        project=PROJECT,
        default_service=backends[PROD][0].self_link,
        host_rules=[
            gcp.compute.URLMapHostRuleArgs(
                hosts=[variant.console_domain],
                path_matcher=f"airmux{variant.suffix or '-prod'}",
            )
            for variant in VARIANTS
        ],
        path_matchers=[
            gcp.compute.URLMapPathMatcherArgs(
                name=f"airmux{variant.suffix or '-prod'}",
                default_service=backends[variant][0].self_link,
                path_rules=[
                    gcp.compute.URLMapPathMatcherPathRuleArgs(
                        paths=["/api", "/api/*"],
                        service=backends[variant][1].self_link,
                    )
                ],
            )
            for variant in VARIANTS
        ],
    )
    proxy = gcp.compute.TargetHttpsProxy(
        "airmux-console-https",
        name="airmux-console-https",
        project=PROJECT,
        url_map=urlmap.self_link,
        ssl_certificates=[cert.self_link],
    )
    gcp.compute.GlobalForwardingRule(
        "airmux-console-forwarding",
        name="airmux-console-forwarding",
        project=PROJECT,
        target=proxy.self_link,
        port_range="443",
        ip_address=address.address,
        load_balancing_scheme="EXTERNAL",
    )
    redirect = gcp.compute.URLMap(
        "airmux-console-redirect-map",
        name="airmux-console-redirect-map",
        project=PROJECT,
        default_url_redirect=gcp.compute.URLMapDefaultUrlRedirectArgs(
            https_redirect=True, strip_query=False
        ),
    )
    http_proxy = gcp.compute.TargetHttpProxy(
        "airmux-console-http",
        name="airmux-console-http",
        project=PROJECT,
        url_map=redirect.self_link,
    )
    gcp.compute.GlobalForwardingRule(
        "airmux-console-http-forwarding",
        name="airmux-console-http-forwarding",
        project=PROJECT,
        target=http_proxy.self_link,
        port_range="80",
        ip_address=address.address,
        load_balancing_scheme="EXTERNAL",
    )
    for variant in VARIANTS:
        gcp.dns.RecordSet(
            f"airmux-console-dns{variant.suffix}",
            name=f"{variant.console_domain}.",
            type="A",
            ttl=300,
            managed_zone=DNS_ZONE_NAME,
            project=DNS_ZONE_PROJECT,
            rrdatas=[address.address],
        )
    return address


# Exact upstream call sites (data_plane bundle/remote.py, outbox/sqlite.py,
# heartbeat.py, budgets.py): bundles/manifest, bundles/{id}, events,
# heartbeat, policy-state/sync. Anything else gets a synthetic 404 at the LB.
# Exact data-plane call sites only (upstream routes/sync.py serves just
# GET /bundles/manifest and GET /bundles/{bundle_id}): bare /bundles and
# nested paths must not pass.
GATEWAY_ALLOWED_REGEX = (
    r"^/api/v1/(bundles/(manifest|[^/]+)|events|heartbeat|policy-state/sync)$"
)


def _gateway_matcher(
    name: str, backend: gcp.compute.RegionBackendService
) -> gcp.compute.RegionUrlMapPathMatcherArgs:
    return gcp.compute.RegionUrlMapPathMatcherArgs(
        name=name,
        default_service=backend.self_link,
        route_rules=[
            gcp.compute.RegionUrlMapPathMatcherRouteRuleArgs(
                priority=1,
                match_rules=[
                    gcp.compute.RegionUrlMapPathMatcherRouteRuleMatchRuleArgs(
                        regex_match=GATEWAY_ALLOWED_REGEX
                    )
                ],
                service=backend.self_link,
            ),
            gcp.compute.RegionUrlMapPathMatcherRouteRuleArgs(
                priority=2,
                match_rules=[
                    gcp.compute.RegionUrlMapPathMatcherRouteRuleMatchRuleArgs(
                        prefix_match="/"
                    )
                ],
                route_action=gcp.compute.RegionUrlMapPathMatcherRouteRuleRouteActionArgs(
                    weighted_backend_services=[
                        gcp.compute.RegionUrlMapPathMatcherRouteRuleRouteActionWeightedBackendServiceArgs(
                            backend_service=backend.self_link, weight=100
                        )
                    ],
                    fault_injection_policy=gcp.compute.RegionUrlMapPathMatcherRouteRuleRouteActionFaultInjectionPolicyArgs(
                        abort=gcp.compute.RegionUrlMapPathMatcherRouteRuleRouteActionFaultInjectionPolicyAbortArgs(
                            http_status=404, percentage=100
                        )
                    ),
                ),
            ),
        ],
    )


def define_gateway_edge(
    controls: dict[Variant, gcp.cloudrunv2.Service],
    network: gcp.compute.Network,
    proxy_subnet: gcp.compute.Subnetwork,
    psc_nat: gcp.compute.Subnetwork,
    ilb_subnet: gcp.compute.Subnetwork,
    api_services: list[gcp.projects.Service],
) -> tuple[gcp.compute.ServiceAttachment, pulumi.Output[str], str]:
    backends: dict[Variant, gcp.compute.RegionBackendService] = {}
    for variant, control in controls.items():
        neg = _neg(f"gateway-neg{variant.suffix}", control)
        backends[variant] = gcp.compute.RegionBackendService(
            f"gateway-backend{variant.suffix}",
            name=f"airmux-gateway-backend{variant.suffix}",
            project=PROJECT,
            region=REGION,
            protocol="HTTP",
            load_balancing_scheme="INTERNAL_MANAGED",
            network=network.id,
            backends=[gcp.compute.RegionBackendServiceBackendArgs(group=neg.id)],
        )
    gateway_map = gcp.compute.RegionUrlMap(
        "gateway-url-map",
        name="airmux-gateway-url-map",
        project=PROJECT,
        region=REGION,
        # Unreachable: the `*` host rule below catches every host, so the
        # required top-level default_service never matches.
        default_service=backends[PROD].self_link,
        host_rules=[
            *[
                gcp.compute.RegionUrlMapHostRuleArgs(
                    hosts=[variant.gateway_domain],
                    path_matcher=f"gateway{variant.suffix or '-prod'}",
                )
                for variant in VARIANTS
            ],
            # GCP evaluates exact hosts before the wildcard; unmatched hosts
            # hit the `reject` matcher and get a synthetic 404 rather than
            # bypassing the path allowlist via default_service.
            gcp.compute.RegionUrlMapHostRuleArgs(hosts=["*"], path_matcher="reject"),
        ],
        path_matchers=[
            *[
                _gateway_matcher(
                    f"gateway{variant.suffix or '-prod'}", backends[variant]
                )
                for variant in VARIANTS
            ],
            gcp.compute.RegionUrlMapPathMatcherArgs(
                name="reject",
                default_service=backends[PROD].self_link,
                default_route_action=gcp.compute.RegionUrlMapPathMatcherDefaultRouteActionArgs(
                    fault_injection_policy=gcp.compute.RegionUrlMapPathMatcherDefaultRouteActionFaultInjectionPolicyArgs(
                        abort=gcp.compute.RegionUrlMapPathMatcherDefaultRouteActionFaultInjectionPolicyAbortArgs(
                            http_status=404, percentage=100
                        )
                    )
                ),
            ),
        ],
    )
    # One DnsAuthorization + authz record per gateway hostname; the regional
    # cert covers both SANs.
    cert_auths = {
        variant.gateway_domain: gcp.certificatemanager.DnsAuthorization(
            f"gateway-dns-auth{variant.suffix}",
            name=f"airmux-gateway-dns-auth{variant.suffix}",
            domain=variant.gateway_domain,
            location=REGION,
            project=PROJECT,
            # No input ties this resource to an API enablement, so without an
            # explicit depends_on a first apply races
            # certificatemanager.googleapis.com finishing activation.
            opts=pulumi.ResourceOptions(depends_on=api_services),
        )
        for variant in VARIANTS
    }
    cert = gcp.certificatemanager.Certificate(
        "gateway-cert",
        name="airmux-gateway-cert",
        location=REGION,
        project=PROJECT,
        managed=gcp.certificatemanager.CertificateManagedArgs(
            domains=[variant.gateway_domain for variant in VARIANTS],
            dns_authorizations=[auth.id for auth in cert_auths.values()],
        ),
    )
    for variant in VARIANTS:
        records = cert_auths[variant.gateway_domain].dns_resource_records
        gcp.dns.RecordSet(
            f"gateway-dns-auth-record{variant.suffix}",
            name=records.apply(lambda values: values[0].name),
            type=records.apply(lambda values: values[0].type),
            ttl=300,
            managed_zone=DNS_ZONE_NAME,
            project=DNS_ZONE_PROJECT,
            rrdatas=[records.apply(lambda values: values[0].data)],
        )
    https_proxy = gcp.compute.RegionTargetHttpsProxy(
        "gateway-https-proxy",
        name="airmux-gateway-https-proxy",
        project=PROJECT,
        region=REGION,
        url_map=gateway_map.id,
        certificate_manager_certificates=[cert.id],
    )
    address = gcp.compute.Address(
        "gateway-ilb-ip",
        name="airmux-gateway-ilb-ip",
        project=PROJECT,
        region=REGION,
        subnetwork=ilb_subnet.id,
        address_type="INTERNAL",
    )
    forwarding = gcp.compute.ForwardingRule(
        "gateway-forwarding",
        name="airmux-gateway-forwarding",
        project=PROJECT,
        region=REGION,
        network=network.id,
        subnetwork=ilb_subnet.id,
        ip_address=address.address,
        target=https_proxy.id,
        ports=["443"],
        load_balancing_scheme="INTERNAL_MANAGED",
        allow_global_access=True,
        # The proxy-only subnet must exist before a regional internal ALB's
        # forwarding rule can be created.
        opts=pulumi.ResourceOptions(depends_on=[proxy_subnet]),
    )
    attachment = gcp.compute.ServiceAttachment(
        "gateway-service-attachment",
        name="airmux-gateway-psc",
        project=PROJECT,
        region=REGION,
        target_service=forwarding.id,
        connection_preference="ACCEPT_MANUAL",
        consumer_accept_lists=[
            gcp.compute.ServiceAttachmentConsumerAcceptListArgs(
                project_id_or_num=project, connection_limit=10
            )
            for project in PSC_CONSUMERS
        ],
        nat_subnets=[psc_nat.id],
        enable_proxy_protocol=False,
    )
    return attachment, attachment.self_link, PROD.gateway_domain


def main() -> None:
    apis = define_apis()
    artifact_repo = define_artifact_repo(apis)
    network, proxy_subnet, psc_nat, ilb_subnet = define_network(apis)
    sql_instances, url_secrets, url_versions, databases, users = define_sql(apis)
    runtime_sas, console_sa = define_runtime_identity(apis)
    # cloudsql.client is a plain IAM member — automatable, so Pulumi owns it.
    cloudsql_members: dict[Variant, gcp.projects.IAMMember] = {}
    for variant in VARIANTS:
        cloudsql_members[variant] = gcp.projects.IAMMember(
            f"airmux-cloudsql-client{variant.suffix}",
            project=PROJECT,
            role="roles/cloudsql.client",
            member=runtime_sas[variant].email.apply(
                lambda email: f"serviceAccount:{email}"
            ),
        )
    mgmt_secrets, mgmt_versions, mgmt_keys, config_secret, config_version = (
        define_secrets(apis)
    )
    # All secret values are Pulumi-owned, so Pulumi grants the runtime SAs
    # read access; nothing here is human-seeded anymore.
    accessor_members: dict[Variant, list[gcp.secretmanager.SecretIamMember]] = {
        variant: [] for variant in VARIANTS
    }
    for variant in VARIANTS:
        for name, secret in [
            ("db-url", url_secrets[variant]),
            ("management-key", mgmt_secrets[variant]),
            ("config", config_secret),
        ]:
            accessor_members[variant].append(
                gcp.secretmanager.SecretIamMember(
                    f"airmux-{name}-accessor{variant.suffix}",
                    secret_id=secret.id,
                    role="roles/secretmanager.secretAccessor",
                    member=runtime_sas[variant].email.apply(
                        lambda email: f"serviceAccount:{email}"
                    ),
                    project=PROJECT,
                )
            )
    # Optional cross-project handoff of the prod management key into the
    # agent-plane project (deployer needs secretVersionAdder there).
    agent_plane_key_secret = config.get("agent-plane-management-key-secret")
    if agent_plane_key_secret:
        gcp.secretmanager.SecretVersion(
            "agent-plane-management-key",
            secret=agent_plane_key_secret,
            secret_data=mgmt_keys[PROD],
        )
    iap_identity = gcp.projects.ServiceIdentity(
        "iap-service-identity",
        service="iap.googleapis.com",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=apis),
    )
    per_variant: dict[
        Variant,
        tuple[
            gcp.cloudrunv2.Service,
            gcp.cloudrunv2.Service,
            gcp.cloudrunv2.Job,
            gcp.cloudrunv2.Job,
        ],
    ] = {
        variant: define_services(
            apis,
            runtime_sas,
            console_sa,
            sql_instances[variant],
            [url_versions[variant], mgmt_versions[variant], config_version],
            [
                databases[variant],
                users[variant],
                artifact_repo,
                cloudsql_members[variant],
                *accessor_members[variant],
            ],
            config_version,
            iap_identity,
            variant,
        )
        for variant in VARIANTS
    }
    define_external_lb(
        {variant: (svc[0], svc[1]) for variant, svc in per_variant.items()}, apis
    )
    _, attachment_uri, _ = define_gateway_edge(
        {variant: svc[0] for variant, svc in per_variant.items()},
        network,
        proxy_subnet,
        psc_nat,
        ilb_subnet,
        apis,
    )
    prod = per_variant[PROD]
    preview = per_variant[PREVIEW]
    outputs = {
        "console_url": f"https://{PROD.console_domain}",
        "control_plane_service": prod[0].name,
        "console_service": prod[1].name,
        "migrate_job": prod[2].name,
        "taxonomy_job": prod[3].name,
        "preview_console_url": f"https://{PREVIEW.console_domain}",
        "preview_control_plane_service": preview[0].name,
        "preview_console_service": preview[1].name,
        "preview_migrate_job": preview[2].name,
        "preview_taxonomy_job": preview[3].name,
        "sql_connection_name": sql_instances[PROD].connection_name,
        "preview_sql_connection_name": sql_instances[PREVIEW].connection_name,
        "service_attachment_uri": attachment_uri,
        "gateway_hostname": PROD.gateway_domain,
        "preview_gateway_hostname": PREVIEW.gateway_domain,
        "management_key_secret": PROD.management_key_secret,
        "preview_management_key_secret": PREVIEW.management_key_secret,
        "airmux_version": AIRMUX_VERSION,
        "image": IMAGE,
    }
    for name, value in outputs.items():
        pulumi.export(name, value)


main()
