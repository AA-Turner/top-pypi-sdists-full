"""Pulumi IaC for the Airbyte AG-UI chat services.

Architecture:
  Cloud Run (`agui-playground`) <- serverless NEG <- external HTTPS LB <- users
  Cloud Run (`agui-server`)     <- serverless NEG <- same LB (`/api/*` paths)

IAP (Identity-Aware Proxy) on both load-balancer backends enforces @airbyte.io
Google Workspace SSO before requests reach Cloud Run.

Primary host: `ops.internal.airbyte.ai/chat` via the ops-webapp URL map
(`/chat/api/*` -> agui-server, `/chat/*` -> agui-playground). The standalone
`chat.internal.airbyte.ai` LB/DNS below now 301-redirects every request there
instead of serving the app itself.

Container images are built and pushed by the publish workflows in
`airbytehq/airbyte-agui-server` and `airbytehq/airbyte-agui-sdk`. The tags in
`Pulumi.prod.yaml` only seed the first create — Pulumi ignores changes to the
container image (`ignore_changes` on `template.containers[*].image`) and the
`deploy-agui-command.yml` workflow manages the actual image via
`gcloud run services update --image=<tag>`.

Each service has a preview twin (`agui-server-preview`,
`agui-playground-preview`) reached only via `preview.ops.internal.airbyte.ai`
through the ops-webapp URL map — they are not attached to the standalone LB
below.
"""

from __future__ import annotations

import pulumi
import pulumi_gcp as gcp

OutputMap = dict[str, object]

config = pulumi.Config()
gcp_config = pulumi.Config("gcp")

PROJECT = gcp_config.require("project")
PROJECT_NUMBER = gcp.organizations.get_project_output(project_id=PROJECT).number
REGION = gcp_config.get("region") or "us-west3"
DOMAIN = config.get("domain") or "chat.internal.airbyte.ai"
# The standalone host no longer serves the app; every request redirects to the
# primary entrypoint on the ops-webapp host.
REDIRECT_HOST = config.get("redirect-host") or "ops.internal.airbyte.ai"
REDIRECT_PATH = config.get("redirect-path") or "/chat/"
MIN_INSTANCES = int(config.get("min-instances") or "0")
MAX_INSTANCES = int(config.get("max-instances") or "5")
DNS_ZONE_PROJECT = config.get("dns-zone-project") or "airbyte-intranet"
DNS_ZONE_NAME = config.get("dns-zone-name") or "internal-airbyte-ai"

AIRBYTE_DOMAIN = "airbyte.io"

SERVER_SERVICE_NAME = "agui-server"
PLAYGROUND_SERVICE_NAME = "agui-playground"
SERVER_PREVIEW_SERVICE_NAME = "agui-server-preview"
PLAYGROUND_PREVIEW_SERVICE_NAME = "agui-playground-preview"
AR_REPO_ID = "airbyte-agui-internal"
SERVER_IMAGE_TAG = config.require("server-image-tag")
PLAYGROUND_IMAGE_TAG = config.require("playground-image-tag")
SERVER_IMAGE = (
    f"{REGION}-docker.pkg.dev/{PROJECT}/{AR_REPO_ID}"
    f"/airbyte-agui-server:{SERVER_IMAGE_TAG}"
)
PLAYGROUND_IMAGE = f"ghcr.io/airbytehq/airbyte-agui-playground:{PLAYGROUND_IMAGE_TAG}"

MCP_URL = config.get("mcp-url") or "https://mcp.internal.airbyte.ai/ops-mcp"
AGENT_MODEL = config.get("agent-model") or ""
CHAT_ENABLED = config.get("chat-enabled") or "true"
MCP_UI = config.get("mcp-ui") or "true"
PATH_PREFIX = (config.get("path-prefix") or "").strip("/")
MCP_AUTH_MODE = config.get("mcp-auth-mode") or "bearer"

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
# service env without a cycle — operators read the backend ID with gcloud after
# the first apply and set `agent-chat-internal:server-iap-audience` (the ID is
# not exported as a stack output: Pulumi carries numbers as float64, which
# silently rounds the 19-digit ID — see BOOTSTRAP.md step 7).
SERVER_IAP_AUDIENCE = config.get("server-iap-audience") or ""
# Same for the `agui-server-preview` backend (preview.ops.internal.airbyte.ai).
PREVIEW_SERVER_IAP_AUDIENCE = config.get("preview-server-iap-audience") or ""


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


def define_runtime_service_account(
    api_services: list[gcp.projects.Service],
) -> gcp.serviceaccount.Account:
    """Define the agui-server runtime identity.

    Secret containers and this account's `secretAccessor` grants on them are
    bootstrap-owned (see `BOOTSTRAP.md`), matching the other stacks in this
    repo: the deployer SA cannot set IAM policy on secrets.
    """
    return gcp.serviceaccount.Account(
        "agui-server-sa",
        account_id="agui-server-sa",
        display_name="AG-UI server runtime service account",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )


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
            # settings; ignoring it avoids perpetual refresh drift. Image is
            # ignored too: the deploy-agui workflow owns it via
            # `gcloud run services update --image=<tag>`; the config tag only
            # seeds the first create.
            ignore_changes=["scaling", "template.containers[*].image"],
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
    api_services: list[gcp.projects.Service],
) -> gcp.compute.GlobalAddress:
    """Define the external HTTPS load balancer as a redirect to the primary host.

    Every request to `chat.internal.airbyte.ai` 301-redirects to
    `ops.internal.airbyte.ai/chat/` (`REDIRECT_HOST` + `REDIRECT_PATH`).
    HTTP traffic redirects to HTTPS first. The backends stay provisioned for
    the ops-webapp stack's `/chat` path rules, which look them up by name with
    `gcp.compute.get_backend_service_output`.
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
        default_url_redirect=gcp.compute.URLMapDefaultUrlRedirectArgs(
            host_redirect=REDIRECT_HOST,
            path_redirect=REDIRECT_PATH,
            # `https_redirect` is only permitted on maps behind a TargetHttpProxy;
            # this map is served over HTTPS already, so the scheme is preserved.
            https_redirect=False,
            strip_query=False,
            redirect_response_code="MOVED_PERMANENTLY_DEFAULT",
        ),
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


def _server_envs(
    iap_audience: str,
) -> list[gcp.cloudrunv2.ServiceTemplateContainerEnvArgs]:
    """Build the agui-server env list shared by the prod and preview services."""
    envs = [
        _env("AIRBYTE_AGUI_SERVER_ENABLED", CHAT_ENABLED),
        _env("AIRBYTE_AGUI_SERVER_AGENT_MODEL", AGENT_MODEL),
        _env("AIRBYTE_AGUI_SERVER_MCP_URL", MCP_URL),
        _env("AIRBYTE_AGUI_SERVER_MCP_AUTH_MODE", MCP_AUTH_MODE),
        _env("AIRBYTE_AGUI_SERVER_MCP_UI", MCP_UI),
    ]
    if PATH_PREFIX:
        envs.append(_env("AIRBYTE_AGUI_SERVER_PATH_PREFIX", PATH_PREFIX))
    if iap_audience:
        envs.append(_env("AIRBYTE_AGUI_SERVER_IAP_AUDIENCE", iap_audience))
    for env_name, secret_id in SECRET_ENVS.items():
        if secret_id:
            envs.append(_secret_env(env_name, secret_id))
    return envs


def main() -> None:
    """Define and export all AG-UI chat infrastructure."""
    api_services = define_apis()
    # The Artifact Registry repo, the identity that publishes to it, and its
    # IAM are bootstrap-owned (see BOOTSTRAP.md); the stack only consumes
    # the image by tag.
    service_account = define_runtime_service_account(api_services)

    iap_identity = gcp.projects.ServiceIdentity(
        "iap-service-identity",
        service="iap.googleapis.com",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    server_service = _define_cloud_run_service(
        SERVER_SERVICE_NAME,
        SERVER_IMAGE,
        "1Gi",
        _server_envs(SERVER_IAP_AUDIENCE),
        api_services,
        service_account=service_account,
        iap_identity=iap_identity,
    )
    playground_service = _define_cloud_run_service(
        PLAYGROUND_SERVICE_NAME,
        PLAYGROUND_IMAGE,
        "512Mi",
        [_env("AGUI_BASE_URL", f"/{PATH_PREFIX}" if PATH_PREFIX else "")],
        api_services,
        service_account=None,
        iap_identity=iap_identity,
    )

    # Preview twins, reached only via preview.ops.internal.airbyte.ai through
    # the ops-webapp URL map (not attached to the standalone LB below).
    server_preview_service = _define_cloud_run_service(
        SERVER_PREVIEW_SERVICE_NAME,
        SERVER_IMAGE,
        "1Gi",
        _server_envs(PREVIEW_SERVER_IAP_AUDIENCE),
        api_services,
        service_account=service_account,
        iap_identity=iap_identity,
    )
    playground_preview_service = _define_cloud_run_service(
        PLAYGROUND_PREVIEW_SERVICE_NAME,
        PLAYGROUND_IMAGE,
        "512Mi",
        [_env("AGUI_BASE_URL", f"/{PATH_PREFIX}" if PATH_PREFIX else "")],
        api_services,
        service_account=None,
        iap_identity=iap_identity,
    )

    server_backend = _define_neg_and_backend(SERVER_SERVICE_NAME, server_service)
    _define_neg_and_backend(PLAYGROUND_SERVICE_NAME, playground_service)
    server_preview_backend = _define_neg_and_backend(
        SERVER_PREVIEW_SERVICE_NAME, server_preview_service
    )
    _define_neg_and_backend(PLAYGROUND_PREVIEW_SERVICE_NAME, playground_preview_service)
    lb_ip = define_load_balancer(api_services)
    dns_record = define_dns(lb_ip)

    outputs: OutputMap = {
        "server_service": server_service.name,
        "playground_service": playground_service.name,
        "server_image": SERVER_IMAGE,
        "playground_image": PLAYGROUND_IMAGE,
        "artifact_registry_repository": (
            f"{REGION}-docker.pkg.dev/{PROJECT}/{AR_REPO_ID}"
        ),
        "lb_ip": lb_ip.address,
        "url": f"https://{DOMAIN}/{PATH_PREFIX}"
        if PATH_PREFIX
        else f"https://{DOMAIN}",
        "server_backend_service": server_backend.name,
        "preview_server_service": server_preview_service.name,
        "preview_playground_service": playground_preview_service.name,
        "preview_server_backend_service": server_preview_backend.name,
        "ops_webapp_url": (
            f"https://ops.internal.airbyte.ai/{PATH_PREFIX}" if PATH_PREFIX else ""
        ),
        "preview_ops_webapp_url": (
            f"https://preview.ops.internal.airbyte.ai/{PATH_PREFIX}"
            if PATH_PREFIX
            else ""
        ),
        "dns_record": dns_record.name,
    }
    for name, value in outputs.items():
        pulumi.export(name, value)


main()
