"""Pulumi IaC for the Airbyte AG-UI chat services.

Architecture:
  Cloud Run (`agui-playground`) <- serverless NEG <- external HTTPS LB <- users
  Cloud Run (`agui-server`)     <- serverless NEG <- same LB (`/api/*` paths)

IAP (Identity-Aware Proxy) on both load-balancer backends enforces @airbyte.io
Google Workspace SSO before requests reach Cloud Run.

Canonical host: `chat.internal.airbyte.ai`.

Container images are built and pushed by the publish workflows in
`airbytehq/airbyte-agui-server` and `airbytehq/airbyte-agui-sdk`; this stack
points each service at the tag configured in `Pulumi.prod.yaml`, so bumping the
tag and applying is the deploy mechanism (no `ignore_changes` on image).
"""

from __future__ import annotations

import pulumi
import pulumi_gcp as gcp

OutputMap = dict[str, object]

config = pulumi.Config()
gcp_config = pulumi.Config("gcp")

PROJECT = gcp_config.require("project")
PROJECT_NUMBER = gcp.organizations.get_project_output(project=PROJECT).number
REGION = gcp_config.get("region") or "us-west3"
DOMAIN = config.get("domain") or "chat.internal.airbyte.ai"
MIN_INSTANCES = int(config.get("min-instances") or "0")
MAX_INSTANCES = int(config.get("max-instances") or "5")
DNS_ZONE_PROJECT = config.get("dns-zone-project") or "airbyte-intranet"
DNS_ZONE_NAME = config.get("dns-zone-name") or "internal-airbyte-ai"

AIRBYTE_DOMAIN = "airbyte.io"

SERVER_SERVICE_NAME = "agui-server"
PLAYGROUND_SERVICE_NAME = "agui-playground"
AR_REPO_ID = "airbyte-agui-internal"
SERVER_IMAGE_TAG = config.require("server-image-tag")
PLAYGROUND_IMAGE_TAG = config.require("playground-image-tag")
SERVER_IMAGE = (
    f"{REGION}-docker.pkg.dev/{PROJECT}/{AR_REPO_ID}"
    f"/airbyte-agui-server:{SERVER_IMAGE_TAG}"
)
PLAYGROUND_IMAGE = f"ghcr.io/airbytehq/airbyte-agui-playground:{PLAYGROUND_IMAGE_TAG}"

PUBLISHER_GITHUB_REPO = "airbytehq/airbyte-agui-server"
WIF_POOL_ID = "github-actions"

MCP_URL = config.get("mcp-url") or "https://mcp.internal.airbyte.ai/ops-mcp"
AGENT_MODEL = config.get("agent-model") or ""
CHAT_ENABLED = config.get("chat-enabled") or "true"
MCP_UI = config.get("mcp-ui") or "true"

# Map of `AIRBYTE_AGUI_SERVER_*` env var -> Secret Manager container ID.
# Empty IDs omit both the env var and the secret-access grant.
SECRET_ENVS = {
    "AIRBYTE_AGUI_SERVER_ANTHROPIC_API_KEY": config.get("anthropic-secret-id") or "",
    "AIRBYTE_AGUI_SERVER_MCP_CLIENT_ID": config.get("mcp-client-id-secret-id") or "",
    "AIRBYTE_AGUI_SERVER_MCP_CLIENT_SECRET": (config.get("mcp-client-secret-id") or ""),
    "AIRBYTE_AGUI_SERVER_OAUTH_CLIENT_SECRET": config.get("oauth-secret-id") or "",
    "AIRBYTE_AGUI_SERVER_LOGFIRE_TOKEN": config.get("logfire-secret-id") or "",
}


# Expected IAP JWT audience for the agui-server backend service. The value
# (`/projects/<number>/global/backendServices/<numeric backend id>`) only
# exists after the backend is created, so it cannot be inlined into the
# service env without a cycle — operators copy the `server_iap_audience`
# stack output into `agent-chat-internal:server-iap-audience` after the first apply.
SERVER_IAP_AUDIENCE = config.get("server-iap-audience") or ""


def _env(name: str, value: str) -> gcp.cloudrunv2.ServiceTemplateContainerEnvArgs:
    """Define a Cloud Run literal environment variable."""
    return gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(name=name, value=value)


def _secret_env(
    name: str,
    secret_id: str,
) -> gcp.cloudrunv2.ServiceTemplateContainerEnvArgs:
    """Define a Cloud Run environment variable backed by Secret Manager."""
    return gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
        name=name,
        value_source=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceArgs(
            secret_key_ref=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceSecretKeyRefArgs(
                secret=secret_id,
                version="latest",
            ),
        ),
    )


def define_apis() -> list[gcp.projects.Service]:
    """Define required API enablements for the runtime project."""
    api_ids = [
        "artifactregistry.googleapis.com",
        "compute.googleapis.com",
        "iam.googleapis.com",
        "iap.googleapis.com",
        "run.googleapis.com",
        "secretmanager.googleapis.com",
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


def define_publisher(
    repository_id: pulumi.Input[str],
    api_services: list[gcp.projects.Service],
) -> gcp.serviceaccount.Account:
    """Define the image-publisher service account and its WIF binding.

    The `airbytehq/airbyte-agui-server` publish workflow impersonates this
    account through the shared GitHub Actions workload identity pool.
    """
    publisher = gcp.serviceaccount.Account(
        "airbyte-agui-publisher",
        account_id="airbyte-agui-publisher",
        display_name="Airbyte AG-UI image publisher",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    gcp.artifactregistry.RepositoryIamMember(
        "airbyte-agui-publisher-writer",
        repository=repository_id,
        location=REGION,
        project=PROJECT,
        role="roles/artifactregistry.writer",
        member=publisher.email.apply(lambda email: f"serviceAccount:{email}"),
    )
    gcp.serviceaccount.IAMMember(
        "airbyte-agui-publisher-wif",
        service_account_id=publisher.name,
        project=PROJECT,
        role="roles/iam.workloadIdentityUser",
        member=PROJECT_NUMBER.apply(
            lambda number: (
                "principalSet://iam.googleapis.com"
                f"/projects/{number}"
                f"/locations/global/workloadIdentityPools/{WIF_POOL_ID}"
                f"/attribute.repository/{PUBLISHER_GITHUB_REPO}"
            )
        ),
    )
    return publisher


def define_runtime_service_account(
    api_services: list[gcp.projects.Service],
) -> tuple[gcp.serviceaccount.Account, list[gcp.secretmanager.SecretIamMember]]:
    """Define the agui-server runtime identity and its secret grants.

    Secret containers are created out-of-band during bootstrap; this only
    grants the runtime account read access to the configured ones. The grants
    are returned so `agui-server` can depend on them — Cloud Run resolves
    secret references at revision creation and fails if the grant is not yet
    propagated.
    """
    account = gcp.serviceaccount.Account(
        "agui-server-sa",
        account_id="agui-server-sa",
        display_name="AG-UI server runtime service account",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    secret_grants = [
        gcp.secretmanager.SecretIamMember(
            f"agui-server-sa-secret-{env_name.lower().replace('_', '-')}",
            secret_id=secret_id,
            project=PROJECT,
            role="roles/secretmanager.secretAccessor",
            member=account.email.apply(lambda email: f"serviceAccount:{email}"),
        )
        for env_name, secret_id in SECRET_ENVS.items()
        if secret_id
    ]
    return account, secret_grants


def _define_cloud_run_service(
    service_name: str,
    image: str,
    memory: str,
    envs: list[gcp.cloudrunv2.ServiceTemplateContainerEnvArgs],
    api_services: list[gcp.projects.Service],
    *,
    service_account: gcp.serviceaccount.Account | None,
    iap_identity: gcp.projects.ServiceIdentity,
    depends_on: list[pulumi.Resource] | None = None,
) -> gcp.cloudrunv2.Service:
    """Define one internal-LB Cloud Run service behind IAP."""
    service = gcp.cloudrunv2.Service(
        service_name,
        name=service_name,
        project=PROJECT,
        location=REGION,
        description=f"Airbyte AG-UI {service_name} service",
        deletion_protection=False,
        ingress="INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER",
        template=gcp.cloudrunv2.ServiceTemplateArgs(
            service_account=service_account.email if service_account else None,
            max_instance_request_concurrency=40,
            scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
                min_instance_count=MIN_INSTANCES,
                max_instance_count=MAX_INSTANCES,
            ),
            containers=[
                gcp.cloudrunv2.ServiceTemplateContainerArgs(
                    image=image,
                    ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                        container_port=8080,
                    ),
                    resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                        limits={"cpu": "1", "memory": memory},
                        startup_cpu_boost=True,
                    ),
                    envs=envs,
                )
            ],
        ),
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=[*api_services, *(depends_on or [])],
            # Cloud Run auto-populates top-level `scaling` from template
            # settings; ignoring it avoids perpetual refresh drift.
            ignore_changes=["scaling"],
        ),
    )
    gcp.cloudrunv2.ServiceIamMember(
        f"{service_name}-iap-invoker",
        project=PROJECT,
        location=REGION,
        name=service.name,
        role="roles/run.invoker",
        member=iap_identity.email.apply(lambda email: f"serviceAccount:{email}"),
        opts=pulumi.ResourceOptions(depends_on=[service, iap_identity]),
    )
    return service


def _define_neg_and_backend(
    service_name: str,
    cloud_run_service: gcp.cloudrunv2.Service,
) -> gcp.compute.BackendService:
    """Create a serverless NEG + IAP-enabled backend for a Cloud Run service.

    Uses GCP's Google-managed OAuth client (single-space values) and grants
    `roles/iap.httpsResourceAccessor` to the `@airbyte.io` domain.
    """
    neg = gcp.compute.RegionNetworkEndpointGroup(
        f"{service_name}-neg",
        name=f"{service_name}-neg",
        project=PROJECT,
        region=REGION,
        network_endpoint_type="SERVERLESS",
        cloud_run=gcp.compute.RegionNetworkEndpointGroupCloudRunArgs(
            service=cloud_run_service.name,
        ),
        opts=pulumi.ResourceOptions(depends_on=[cloud_run_service]),
    )
    backend = gcp.compute.BackendService(
        f"{service_name}-backend",
        name=f"{service_name}-backend",
        project=PROJECT,
        protocol="HTTP",
        port_name="http",
        backends=[gcp.compute.BackendServiceBackendArgs(group=neg.id)],
        iap=gcp.compute.BackendServiceIapArgs(
            enabled=True,
            oauth2_client_id=" ",
            oauth2_client_secret=" ",
        ),
        opts=pulumi.ResourceOptions(depends_on=[neg]),
    )
    gcp.iap.WebBackendServiceIamMember(
        f"{service_name}-iap-domain-access",
        project=PROJECT,
        web_backend_service=backend.name,
        role="roles/iap.httpsResourceAccessor",
        member=f"domain:{AIRBYTE_DOMAIN}",
    )
    return backend


def define_load_balancer(
    server_backend: gcp.compute.BackendService,
    playground_backend: gcp.compute.BackendService,
    api_services: list[gcp.projects.Service],
) -> gcp.compute.GlobalAddress:
    """Define the external HTTPS load balancer with path-based routing.

    `/api` and `/api/*` route to the `agui-server` backend; everything else
    goes to `agui-playground`. HTTP traffic redirects to HTTPS.
    """
    ip_address = gcp.compute.GlobalAddress(
        "agent-chat-internal-lb-ip",
        name="agent-chat-internal-lb-ip",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    certificate = gcp.compute.ManagedSslCertificate(
        "agent-chat-internal-ssl-cert",
        name="agent-chat-internal-ssl-cert",
        project=PROJECT,
        managed=gcp.compute.ManagedSslCertificateManagedArgs(domains=[DOMAIN]),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    url_map = gcp.compute.URLMap(
        "agent-chat-internal-url-map",
        name="agent-chat-internal-url-map",
        project=PROJECT,
        default_service=playground_backend.self_link,
        host_rules=[
            gcp.compute.URLMapHostRuleArgs(
                hosts=[DOMAIN],
                path_matcher="chat",
            )
        ],
        path_matchers=[
            gcp.compute.URLMapPathMatcherArgs(
                name="chat",
                default_service=playground_backend.self_link,
                path_rules=[
                    gcp.compute.URLMapPathRuleArgs(
                        paths=["/api", "/api/*"],
                        service=server_backend.self_link,
                    )
                ],
            )
        ],
    )
    https_proxy = gcp.compute.TargetHttpsProxy(
        "agent-chat-internal-https-proxy",
        name="agent-chat-internal-https-proxy",
        project=PROJECT,
        url_map=url_map.self_link,
        ssl_certificates=[certificate.self_link],
    )
    gcp.compute.GlobalForwardingRule(
        "agent-chat-internal-https-forwarding-rule",
        name="agent-chat-internal-https-forwarding-rule",
        project=PROJECT,
        target=https_proxy.self_link,
        port_range="443",
        ip_address=ip_address.address,
        load_balancing_scheme="EXTERNAL",
    )

    http_url_map = gcp.compute.URLMap(
        "agent-chat-internal-http-redirect-url-map",
        name="agent-chat-internal-http-redirect-url-map",
        project=PROJECT,
        default_url_redirect=gcp.compute.URLMapDefaultUrlRedirectArgs(
            https_redirect=True,
            strip_query=False,
        ),
    )
    http_proxy = gcp.compute.TargetHttpProxy(
        "agent-chat-internal-http-redirect-proxy",
        name="agent-chat-internal-http-redirect-proxy",
        project=PROJECT,
        url_map=http_url_map.self_link,
    )
    gcp.compute.GlobalForwardingRule(
        "agent-chat-internal-http-forwarding-rule",
        name="agent-chat-internal-http-forwarding-rule",
        project=PROJECT,
        target=http_proxy.self_link,
        port_range="80",
        ip_address=ip_address.address,
        load_balancing_scheme="EXTERNAL",
    )
    return ip_address


def define_dns(lb_ip: gcp.compute.GlobalAddress) -> gcp.dns.RecordSet:
    """Define the DNS A record for the chat domain."""
    return gcp.dns.RecordSet(
        "agent-chat-internal-dns-record",
        name=f"{DOMAIN}.",
        type="A",
        ttl=300,
        managed_zone=DNS_ZONE_NAME,
        project=DNS_ZONE_PROJECT,
        rrdatas=[lb_ip.address],
    )


def main() -> None:
    """Define and export all AG-UI chat infrastructure."""
    api_services = define_apis()
    # The Artifact Registry repo is bootstrap-owned (see BOOTSTRAP.md) —
    # Pulumi references it read-only so bootstrap can publish the first
    # image before the stack exists.
    repository = gcp.artifactregistry.get_repository_output(
        location=REGION,
        repository_id=AR_REPO_ID,
        project=PROJECT,
    )
    publisher = define_publisher(repository.repository_id, api_services)
    service_account, secret_grants = define_runtime_service_account(api_services)

    iap_identity = gcp.projects.ServiceIdentity(
        "iap-service-identity",
        service="iap.googleapis.com",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    server_envs = [
        _env("AIRBYTE_AGUI_SERVER_ENABLED", CHAT_ENABLED),
        _env("AIRBYTE_AGUI_SERVER_AGENT_MODEL", AGENT_MODEL),
        _env("AIRBYTE_AGUI_SERVER_MCP_URL", MCP_URL),
        _env("AIRBYTE_AGUI_SERVER_MCP_AUTH_MODE", "bearer"),
        _env("AIRBYTE_AGUI_SERVER_MCP_UI", MCP_UI),
    ]
    if SERVER_IAP_AUDIENCE:
        server_envs.append(
            _env("AIRBYTE_AGUI_SERVER_IAP_AUDIENCE", SERVER_IAP_AUDIENCE)
        )
    for env_name, secret_id in SECRET_ENVS.items():
        if secret_id:
            server_envs.append(_secret_env(env_name, secret_id))

    server_service = _define_cloud_run_service(
        SERVER_SERVICE_NAME,
        SERVER_IMAGE,
        "1Gi",
        server_envs,
        api_services,
        service_account=service_account,
        iap_identity=iap_identity,
        depends_on=secret_grants,
    )
    playground_service = _define_cloud_run_service(
        PLAYGROUND_SERVICE_NAME,
        PLAYGROUND_IMAGE,
        "512Mi",
        [_env("AGUI_BASE_URL", "")],
        api_services,
        service_account=None,
        iap_identity=iap_identity,
    )

    server_backend = _define_neg_and_backend(SERVER_SERVICE_NAME, server_service)
    playground_backend = _define_neg_and_backend(
        PLAYGROUND_SERVICE_NAME, playground_service
    )
    lb_ip = define_load_balancer(server_backend, playground_backend, api_services)
    dns_record = define_dns(lb_ip)

    outputs: OutputMap = {
        "server_service": server_service.name,
        "playground_service": playground_service.name,
        "server_image": SERVER_IMAGE,
        "playground_image": PLAYGROUND_IMAGE,
        "artifact_registry_repository": (
            f"{REGION}-docker.pkg.dev/{PROJECT}/{AR_REPO_ID}"
        ),
        "publisher_service_account": publisher.email,
        "lb_ip": lb_ip.address,
        "url": f"https://{DOMAIN}",
        "server_iap_audience": pulumi.Output.concat(
            "/projects/",
            PROJECT_NUMBER,
            "/global/backendServices/",
            server_backend.generated_id,
        ),
        "dns_record": dns_record.name,
    }
    for name, value in outputs.items():
        pulumi.export(name, value)


main()
