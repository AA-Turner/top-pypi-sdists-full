"""Pulumi IaC for the Airbyte Ops Webapp and internal MCP Cloud Run services.

Architecture:
  Cloud Run (`ops-webapp`)         <- serverless NEG <- external HTTPS LB <- users
  Cloud Run (`ops-webapp-preview`) <- serverless NEG <- same LB (host rule) <- users
  Cloud Run (`ops-mcp`)            <- serverless NEG <- same LB (path rule) <- users
  Cloud Run (`ops-mcp-preview`)    <- serverless NEG <- same LB (path rule) <- users
  Cloud Run (`cloud-mcp`)          <- serverless NEG <- same LB (path rule) <- users
  Cloud Run (`cloud-mcp-preview`)  <- serverless NEG <- same LB (path rule) <- users

The app-level Keycloak OAuth flow protects the webapp services. Hosted MCP
servers use FastMCP's `OIDCProxy` for Keycloak OIDC authentication.

All internal MCP services share a single domain (`mcp.internal.airbyte.ai`)
with path-based routing and URL rewriting at the load balancer:
- `/ops-mcp/*`           → ops-mcp prod (rewritten to `/*`)
- `/ops-mcp-preview/*`   → ops-mcp preview (rewritten to `/*`)
- `/cloud-mcp/*`         → cloud-mcp prod (rewritten to `/*`)
- `/cloud-mcp-preview/*` → cloud-mcp preview (rewritten to `/*`)

Canonical hosts:
- `ops.internal.airbyte.ai` (production webapp)
- `preview.ops.internal.airbyte.ai` (PR previews)
- `mcp.internal.airbyte.ai` (internal hosted MCP servers)

Keycloak client setup is intentionally out of scope — see
`docs/keycloak-client-admin.md`.
"""

from __future__ import annotations

import pulumi
import pulumi_gcp as gcp

OutputMap = dict[str, object]
SecretRef = gcp.secretmanager.GetSecretResult

config = pulumi.Config()
gcp_config = pulumi.Config("gcp")

PROJECT = gcp_config.require("project")
REGION = gcp_config.get("region") or "us-west3"
MIN_INSTANCES = int(config.get("min-instances") or "0")
MAX_INSTANCES = int(config.get("max-instances") or "10")

SERVICE_NAME = "ops-webapp"
DOMAIN = config.get("domain") or "ops.internal.airbyte.ai"
PUBLIC_URL = config.get("public-url") or f"https://{DOMAIN}"

PREVIEW_SERVICE_NAME = "ops-webapp-preview"
PREVIEW_DOMAIN = f"preview.{DOMAIN}"
PREVIEW_PUBLIC_URL = f"https://{PREVIEW_DOMAIN}"

MCP_DOMAIN = config.get("mcp-domain") or "mcp.internal.airbyte.ai"

OPS_MCP_SERVICE_NAME = "ops-mcp"
OPS_MCP_PREVIEW_SERVICE_NAME = "ops-mcp-preview"
OPS_MCP_PATH_PREFIX = "/ops-mcp"
OPS_MCP_PREVIEW_PATH_PREFIX = "/ops-mcp-preview"
OPS_MCP_PUBLIC_URL = f"https://{MCP_DOMAIN}{OPS_MCP_PATH_PREFIX}"
OPS_MCP_PREVIEW_PUBLIC_URL = f"https://{MCP_DOMAIN}{OPS_MCP_PREVIEW_PATH_PREFIX}"
OPS_MCP_OAUTH_CLIENT_ID = config.get("ops-mcp-oauth-client-id") or "ops-mcp-client"

CLOUD_MCP_SERVICE_NAME = "cloud-mcp"
CLOUD_MCP_PREVIEW_SERVICE_NAME = "cloud-mcp-preview"
CLOUD_MCP_PATH_PREFIX = "/cloud-mcp"
CLOUD_MCP_PREVIEW_PATH_PREFIX = "/cloud-mcp-preview"
CLOUD_MCP_PUBLIC_URL = f"https://{MCP_DOMAIN}{CLOUD_MCP_PATH_PREFIX}"
CLOUD_MCP_PREVIEW_PUBLIC_URL = f"https://{MCP_DOMAIN}{CLOUD_MCP_PREVIEW_PATH_PREFIX}"
CLOUD_MCP_OAUTH_CLIENT_ID = (
    config.get("cloud-mcp-oauth-client-id") or "cloud-mcp-client"
)
OAUTH_ISSUER = (
    config.get("oauth-issuer") or "https://cloud.airbyte.com/auth/realms/airbyte"
)
OAUTH_CLIENT_ID = config.get("oauth-client-id") or "airbyte-ops-webapp-client"
AIRBYTE_CONFIG_API_URL = (
    config.get("airbyte-config-api-url") or "https://cloud.airbyte.com/api/v1"
)

DNS_ZONE_PROJECT = config.get("dns-zone-project") or "airbyte-intranet"
DNS_ZONE_NAME = config.get("dns-zone-name") or "internal-airbyte-ai"

OAUTH_CLIENT_SECRET_ID = "ops-webapp-oauth-client-secret"
GOOGLE_OAUTH_CLIENT_SECRET_ID = "ops-webapp-google-oauth-client-secret"
OPS_MCP_OAUTH_CLIENT_SECRET_ID = "ops-mcp-oauth-client-secret"
CLOUD_MCP_OAUTH_CLIENT_SECRET_ID = "cloud-mcp-oauth-client-secret"
CONTAINER_IMAGE = (
    f"{REGION}-docker.pkg.dev/{PROJECT}/{SERVICE_NAME}/{SERVICE_NAME}:latest"
)
OPS_MCP_CONTAINER_IMAGE = f"{REGION}-docker.pkg.dev/{PROJECT}/{OPS_MCP_SERVICE_NAME}/{OPS_MCP_SERVICE_NAME}:latest"
CLOUD_MCP_CONTAINER_IMAGE = f"{REGION}-docker.pkg.dev/{PROJECT}/{CLOUD_MCP_SERVICE_NAME}/{CLOUD_MCP_SERVICE_NAME}:latest"


def define_apis() -> list[gcp.projects.Service]:
    """Define required API enablements for the runtime project."""
    api_ids = [
        "artifactregistry.googleapis.com",
        "compute.googleapis.com",
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


def define_secrets() -> dict[str, SecretRef]:
    """Look up bootstrap-managed Secret Manager containers.

    All secrets are created during bootstrap (see `BOOTSTRAP.md` Stage 0) and
    looked up here as read-only data sources. Pulumi never creates secrets —
    see `CONTRIBUTING.md` for the ownership rule.
    """
    return {
        OAUTH_CLIENT_SECRET_ID: gcp.secretmanager.get_secret(
            secret_id=OAUTH_CLIENT_SECRET_ID,
            project=PROJECT,
        ),
        GOOGLE_OAUTH_CLIENT_SECRET_ID: gcp.secretmanager.get_secret(
            secret_id=GOOGLE_OAUTH_CLIENT_SECRET_ID,
            project=PROJECT,
        ),
        OPS_MCP_OAUTH_CLIENT_SECRET_ID: gcp.secretmanager.get_secret(
            secret_id=OPS_MCP_OAUTH_CLIENT_SECRET_ID,
            project=PROJECT,
        ),
        CLOUD_MCP_OAUTH_CLIENT_SECRET_ID: gcp.secretmanager.get_secret(
            secret_id=CLOUD_MCP_OAUTH_CLIENT_SECRET_ID,
            project=PROJECT,
        ),
    }


def define_service_account(
    api_services: list[gcp.projects.Service],
) -> gcp.serviceaccount.Account:
    """Define the Cloud Run runtime service account."""
    account = gcp.serviceaccount.Account(
        f"{SERVICE_NAME}-sa",
        account_id=f"{SERVICE_NAME}-sa",
        display_name="Ops Webapp runtime service account",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    return account


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


def define_cloud_run_service(
    service_account: gcp.serviceaccount.Account,
    api_services: list[gcp.projects.Service],
) -> gcp.cloudrunv2.Service:
    """Define the shared Ops Webapp Cloud Run service."""
    service = gcp.cloudrunv2.Service(
        SERVICE_NAME,
        name=SERVICE_NAME,
        project=PROJECT,
        location=REGION,
        description="Airbyte Ops Webapp shared n=1 service",
        deletion_protection=False,
        ingress="INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER",
        template=gcp.cloudrunv2.ServiceTemplateArgs(
            service_account=service_account.email,
            scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
                min_instance_count=MIN_INSTANCES,
                max_instance_count=MAX_INSTANCES,
            ),
            containers=[
                gcp.cloudrunv2.ServiceTemplateContainerArgs(
                    image=CONTAINER_IMAGE,
                    ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                        container_port=8080,
                    ),
                    resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                        limits={"cpu": "1", "memory": "1Gi"},
                    ),
                    envs=[
                        _env("GCP_PROJECT", PROJECT),
                        _env("AIRBYTE_OPS_WEBAPP_PUBLIC_URL", PUBLIC_URL),
                        _env("AIRBYTE_OPS_WEBAPP_OAUTH_ISSUER", OAUTH_ISSUER),
                        _env("AIRBYTE_OPS_WEBAPP_OAUTH_CLIENT_ID", OAUTH_CLIENT_ID),
                        _env("AIRBYTE_CLOUD_CONFIG_API_URL", AIRBYTE_CONFIG_API_URL),
                        _secret_env(
                            "AIRBYTE_OPS_WEBAPP_OAUTH_CLIENT_SECRET",
                            OAUTH_CLIENT_SECRET_ID,
                        ),
                        _secret_env(
                            "AIRBYTE_OPS_WEBAPP_GOOGLE_CLIENT_SECRET",
                            GOOGLE_OAUTH_CLIENT_SECRET_ID,
                        ),
                    ],
                )
            ],
        ),
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=api_services,
        ),
    )

    gcp.cloudrunv2.ServiceIamMember(
        f"{SERVICE_NAME}-lb-invoker",
        project=PROJECT,
        location=REGION,
        name=service.name,
        role="roles/run.invoker",
        member="allUsers",
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=[service],
        ),
    )

    return service


def define_preview_cloud_run_service(
    service_account: gcp.serviceaccount.Account,
    api_services: list[gcp.projects.Service],
) -> gcp.cloudrunv2.Service:
    """Define the preview Cloud Run service for PR deploy previews.

    Shares the same service account, secrets, and OAuth config as production
    but serves at `preview.ops.internal.airbyte.ai`. Each PR deploy replaces
    the previous preview (only one preview active at a time).
    """
    service = gcp.cloudrunv2.Service(
        PREVIEW_SERVICE_NAME,
        name=PREVIEW_SERVICE_NAME,
        project=PROJECT,
        location=REGION,
        description="Airbyte Ops Webapp preview service for PR deploys",
        deletion_protection=False,
        ingress="INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER",
        template=gcp.cloudrunv2.ServiceTemplateArgs(
            service_account=service_account.email,
            scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
                min_instance_count=0,
                max_instance_count=2,
            ),
            containers=[
                gcp.cloudrunv2.ServiceTemplateContainerArgs(
                    image=CONTAINER_IMAGE,
                    ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                        container_port=8080,
                    ),
                    resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                        limits={"cpu": "1", "memory": "1Gi"},
                    ),
                    envs=[
                        _env("GCP_PROJECT", PROJECT),
                        _env("AIRBYTE_OPS_WEBAPP_PUBLIC_URL", PREVIEW_PUBLIC_URL),
                        _env("AIRBYTE_OPS_WEBAPP_OAUTH_ISSUER", OAUTH_ISSUER),
                        _env("AIRBYTE_OPS_WEBAPP_OAUTH_CLIENT_ID", OAUTH_CLIENT_ID),
                        _env("AIRBYTE_CLOUD_CONFIG_API_URL", AIRBYTE_CONFIG_API_URL),
                        _secret_env(
                            "AIRBYTE_OPS_WEBAPP_OAUTH_CLIENT_SECRET",
                            OAUTH_CLIENT_SECRET_ID,
                        ),
                        _secret_env(
                            "AIRBYTE_OPS_WEBAPP_GOOGLE_CLIENT_SECRET",
                            GOOGLE_OAUTH_CLIENT_SECRET_ID,
                        ),
                    ],
                )
            ],
        ),
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=api_services,
        ),
    )

    gcp.cloudrunv2.ServiceIamMember(
        f"{PREVIEW_SERVICE_NAME}-lb-invoker",
        project=PROJECT,
        location=REGION,
        name=service.name,
        role="roles/run.invoker",
        member="allUsers",
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=[service],
        ),
    )

    return service


def define_mcp_cloud_run_service(
    *,
    service_name: str,
    description: str,
    container_image: str,
    public_url: str,
    oauth_client_id: str,
    oauth_client_secret_id: str,
    service_account: gcp.serviceaccount.Account,
    api_services: list[gcp.projects.Service],
    extra_envs: list[gcp.cloudrunv2.ServiceTemplateContainerEnvArgs] | None = None,
) -> gcp.cloudrunv2.Service:
    """Define a hosted MCP Cloud Run service with OIDC auth.

    Generic factory used for ops-mcp, ops-mcp-preview, cloud-mcp, and
    cloud-mcp-preview services. Each gets its own Cloud Run instance behind
    the shared `mcp.internal.airbyte.ai` load balancer.
    """
    envs = [
        _env("GCP_PROJECT", PROJECT),
        _env("MCP_SERVER_URL", public_url),
        _env(
            "OIDC_CONFIG_URL",
            f"{OAUTH_ISSUER}/.well-known/openid-configuration",
        ),
        _env("OIDC_CLIENT_ID", oauth_client_id),
        _secret_env("OIDC_CLIENT_SECRET", oauth_client_secret_id),
    ]
    if extra_envs:
        envs.extend(extra_envs)

    depends: list[pulumi.Resource] = list(api_services)

    service = gcp.cloudrunv2.Service(
        service_name,
        name=service_name,
        project=PROJECT,
        location=REGION,
        description=description,
        deletion_protection=False,
        ingress="INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER",
        template=gcp.cloudrunv2.ServiceTemplateArgs(
            service_account=service_account.email,
            scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
                min_instance_count=0,
                max_instance_count=MAX_INSTANCES,
            ),
            containers=[
                gcp.cloudrunv2.ServiceTemplateContainerArgs(
                    image=container_image,
                    ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                        container_port=8080,
                    ),
                    resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                        limits={"cpu": "1", "memory": "1Gi"},
                    ),
                    envs=envs,
                )
            ],
        ),
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=depends,
        ),
    )

    gcp.cloudrunv2.ServiceIamMember(
        f"{service_name}-lb-invoker",
        project=PROJECT,
        location=REGION,
        name=service.name,
        role="roles/run.invoker",
        member="allUsers",
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=[service],
        ),
    )

    return service


def _define_neg_and_backend(
    service_name: str,
    cloud_run_service: gcp.cloudrunv2.Service,
) -> gcp.compute.BackendService:
    """Create a serverless NEG + backend service pair for a Cloud Run service."""
    neg = gcp.compute.RegionNetworkEndpointGroup(
        f"{service_name}-neg",
        name=f"{service_name}-neg",
        project=PROJECT,
        region=REGION,
        network_endpoint_type="SERVERLESS",
        cloud_run=gcp.compute.RegionNetworkEndpointGroupCloudRunArgs(
            service=cloud_run_service.name,
        ),
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=[cloud_run_service],
        ),
    )
    return gcp.compute.BackendService(
        f"{service_name}-backend",
        name=f"{service_name}-backend",
        project=PROJECT,
        protocol="HTTP",
        port_name="http",
        backends=[gcp.compute.BackendServiceBackendArgs(group=neg.id)],
        opts=pulumi.ResourceOptions(depends_on=[neg]),
    )


def _mcp_path_route_rule(
    priority: int,
    path_prefix: str,
    backend: gcp.compute.BackendService,
) -> gcp.compute.URLMapPathMatcherRouteRuleArgs:
    """Create a URL Map route rule that matches a path prefix and rewrites to root."""
    return gcp.compute.URLMapPathMatcherRouteRuleArgs(
        priority=priority,
        match_rules=[
            gcp.compute.URLMapPathMatcherRouteRuleMatchRuleArgs(
                prefix_match=f"{path_prefix}/",
            ),
            gcp.compute.URLMapPathMatcherRouteRuleMatchRuleArgs(
                full_path_match=path_prefix,
            ),
        ],
        route_action=gcp.compute.URLMapPathMatcherRouteRuleRouteActionArgs(
            url_rewrite=gcp.compute.URLMapPathMatcherRouteRuleRouteActionUrlRewriteArgs(
                path_prefix_rewrite="/",
            ),
        ),
        service=backend.self_link,
    )


def define_load_balancer(
    *,
    webapp_service: gcp.cloudrunv2.Service,
    webapp_preview_service: gcp.cloudrunv2.Service,
    mcp_services: dict[str, gcp.cloudrunv2.Service],
    api_services: list[gcp.projects.Service],
) -> tuple[gcp.compute.GlobalAddress, gcp.compute.BackendService, OutputMap]:
    """Define the external HTTPS load balancer.

    Webapp traffic uses host-based routing (`ops.internal.airbyte.ai` and
    `preview.ops.internal.airbyte.ai`). MCP traffic uses path-based routing
    under `mcp.internal.airbyte.ai` with URL rewriting to strip the prefix.
    """
    ip_address = gcp.compute.GlobalAddress(
        f"{SERVICE_NAME}-lb-ip",
        name=f"{SERVICE_NAME}-lb-ip",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    # Webapp backends
    webapp_backend = _define_neg_and_backend(SERVICE_NAME, webapp_service)
    preview_backend = _define_neg_and_backend(
        PREVIEW_SERVICE_NAME,
        webapp_preview_service,
    )

    # MCP backends — one per service
    mcp_backends: dict[str, gcp.compute.BackendService] = {
        name: _define_neg_and_backend(name, svc) for name, svc in mcp_services.items()
    }

    # SSL certificates
    ssl_certificate = gcp.compute.ManagedSslCertificate(
        f"{SERVICE_NAME}-ssl-cert",
        name=f"{SERVICE_NAME}-ssl-cert",
        project=PROJECT,
        managed=gcp.compute.ManagedSslCertificateManagedArgs(domains=[DOMAIN]),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    preview_ssl_certificate = gcp.compute.ManagedSslCertificate(
        f"{PREVIEW_SERVICE_NAME}-ssl-cert",
        name=f"{PREVIEW_SERVICE_NAME}-ssl-cert",
        project=PROJECT,
        managed=gcp.compute.ManagedSslCertificateManagedArgs(
            domains=[PREVIEW_DOMAIN],
        ),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    mcp_ssl_certificate = gcp.compute.ManagedSslCertificate(
        "internal-mcp-ssl-cert",
        name="internal-mcp-ssl-cert",
        project=PROJECT,
        managed=gcp.compute.ManagedSslCertificateManagedArgs(
            domains=[MCP_DOMAIN],
        ),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    # MCP path-based route rules (longer prefixes get higher priority)
    mcp_route_rules = [
        _mcp_path_route_rule(
            priority=1,
            path_prefix=OPS_MCP_PREVIEW_PATH_PREFIX,
            backend=mcp_backends[OPS_MCP_PREVIEW_SERVICE_NAME],
        ),
        _mcp_path_route_rule(
            priority=2,
            path_prefix=CLOUD_MCP_PREVIEW_PATH_PREFIX,
            backend=mcp_backends[CLOUD_MCP_PREVIEW_SERVICE_NAME],
        ),
        _mcp_path_route_rule(
            priority=3,
            path_prefix=OPS_MCP_PATH_PREFIX,
            backend=mcp_backends[OPS_MCP_SERVICE_NAME],
        ),
        _mcp_path_route_rule(
            priority=4,
            path_prefix=CLOUD_MCP_PATH_PREFIX,
            backend=mcp_backends[CLOUD_MCP_SERVICE_NAME],
        ),
    ]

    url_map = gcp.compute.URLMap(
        f"{SERVICE_NAME}-url-map",
        name=f"{SERVICE_NAME}-url-map",
        project=PROJECT,
        default_service=webapp_backend.self_link,
        host_rules=[
            gcp.compute.URLMapHostRuleArgs(
                hosts=[PREVIEW_DOMAIN],
                path_matcher="preview",
            ),
            gcp.compute.URLMapHostRuleArgs(
                hosts=[MCP_DOMAIN],
                path_matcher="internal-mcp",
            ),
        ],
        path_matchers=[
            gcp.compute.URLMapPathMatcherArgs(
                name="preview",
                default_service=preview_backend.self_link,
            ),
            gcp.compute.URLMapPathMatcherArgs(
                name="internal-mcp",
                default_service=mcp_backends[OPS_MCP_SERVICE_NAME].self_link,
                route_rules=mcp_route_rules,
            ),
        ],
    )

    https_proxy = gcp.compute.TargetHttpsProxy(
        f"{SERVICE_NAME}-https-proxy",
        name=f"{SERVICE_NAME}-https-proxy",
        project=PROJECT,
        url_map=url_map.self_link,
        ssl_certificates=[
            ssl_certificate.self_link,
            preview_ssl_certificate.self_link,
            mcp_ssl_certificate.self_link,
        ],
    )

    gcp.compute.GlobalForwardingRule(
        f"{SERVICE_NAME}-https-forwarding-rule",
        name=f"{SERVICE_NAME}-https-forwarding-rule",
        project=PROJECT,
        target=https_proxy.self_link,
        port_range="443",
        ip_address=ip_address.address,
        load_balancing_scheme="EXTERNAL",
    )

    http_url_map = gcp.compute.URLMap(
        f"{SERVICE_NAME}-http-redirect-url-map",
        name=f"{SERVICE_NAME}-http-redirect-url-map",
        project=PROJECT,
        default_url_redirect=gcp.compute.URLMapDefaultUrlRedirectArgs(
            https_redirect=True,
            strip_query=False,
        ),
    )

    http_proxy = gcp.compute.TargetHttpProxy(
        f"{SERVICE_NAME}-http-redirect-proxy",
        name=f"{SERVICE_NAME}-http-redirect-proxy",
        project=PROJECT,
        url_map=http_url_map.self_link,
    )

    gcp.compute.GlobalForwardingRule(
        f"{SERVICE_NAME}-http-forwarding-rule",
        name=f"{SERVICE_NAME}-http-forwarding-rule",
        project=PROJECT,
        target=http_proxy.self_link,
        port_range="80",
        ip_address=ip_address.address,
        load_balancing_scheme="EXTERNAL",
    )

    return (
        ip_address,
        webapp_backend,
        {
            "lb.ip_address": ip_address.address,
            "lb.backend_service": webapp_backend.name,
            "lb.url": PUBLIC_URL,
        },
    )


def define_dns(
    lb_ip: gcp.compute.GlobalAddress,
) -> OutputMap:
    """Define DNS A records for production, preview, and internal MCP domains."""
    record = gcp.dns.RecordSet(
        f"{SERVICE_NAME}-dns-record",
        name=f"{DOMAIN}.",
        type="A",
        ttl=300,
        managed_zone=DNS_ZONE_NAME,
        project=DNS_ZONE_PROJECT,
        rrdatas=[lb_ip.address],
    )
    preview_record = gcp.dns.RecordSet(
        f"{PREVIEW_SERVICE_NAME}-dns-record",
        name=f"{PREVIEW_DOMAIN}.",
        type="A",
        ttl=300,
        managed_zone=DNS_ZONE_NAME,
        project=DNS_ZONE_PROJECT,
        rrdatas=[lb_ip.address],
    )
    mcp_record = gcp.dns.RecordSet(
        "internal-mcp-dns-record",
        name=f"{MCP_DOMAIN}.",
        type="A",
        ttl=300,
        managed_zone=DNS_ZONE_NAME,
        project=DNS_ZONE_PROJECT,
        rrdatas=[lb_ip.address],
    )
    return {
        "dns.fqdn": DOMAIN,
        "dns.preview_fqdn": PREVIEW_DOMAIN,
        "dns.mcp_fqdn": MCP_DOMAIN,
        "dns.zone": DNS_ZONE_NAME,
        "dns.zone_project": DNS_ZONE_PROJECT,
        "dns.record": record.name,
        "dns.preview_record": preview_record.name,
        "dns.mcp_record": mcp_record.name,
    }


def main() -> None:
    """Define and export all Ops Webapp and internal MCP infrastructure."""
    api_services = define_apis()
    secrets = define_secrets()
    service_account = define_service_account(api_services)

    # Webapp services
    cloud_run_service = define_cloud_run_service(
        service_account,
        api_services,
    )
    preview_service = define_preview_cloud_run_service(
        service_account,
        api_services,
    )

    # MCP services — all share the same service account and LB domain
    mcp_common = {
        "service_account": service_account,
        "api_services": api_services,
    }
    ops_mcp = define_mcp_cloud_run_service(
        service_name=OPS_MCP_SERVICE_NAME,
        description="Airbyte Ops MCP hosted server",
        container_image=OPS_MCP_CONTAINER_IMAGE,
        public_url=OPS_MCP_PUBLIC_URL,
        oauth_client_id=OPS_MCP_OAUTH_CLIENT_ID,
        oauth_client_secret_id=OPS_MCP_OAUTH_CLIENT_SECRET_ID,
        **mcp_common,
    )
    ops_mcp_preview = define_mcp_cloud_run_service(
        service_name=OPS_MCP_PREVIEW_SERVICE_NAME,
        description="Airbyte Ops MCP preview server for PR deploys",
        container_image=OPS_MCP_CONTAINER_IMAGE,
        public_url=OPS_MCP_PREVIEW_PUBLIC_URL,
        oauth_client_id=OPS_MCP_OAUTH_CLIENT_ID,
        oauth_client_secret_id=OPS_MCP_OAUTH_CLIENT_SECRET_ID,
        **mcp_common,
    )
    cloud_mcp = define_mcp_cloud_run_service(
        service_name=CLOUD_MCP_SERVICE_NAME,
        description="Airbyte Cloud (Replication) MCP hosted server",
        container_image=CLOUD_MCP_CONTAINER_IMAGE,
        public_url=CLOUD_MCP_PUBLIC_URL,
        oauth_client_id=CLOUD_MCP_OAUTH_CLIENT_ID,
        oauth_client_secret_id=CLOUD_MCP_OAUTH_CLIENT_SECRET_ID,
        **mcp_common,
    )
    cloud_mcp_preview = define_mcp_cloud_run_service(
        service_name=CLOUD_MCP_PREVIEW_SERVICE_NAME,
        description="Airbyte Cloud (Replication) MCP preview server for PR deploys",
        container_image=CLOUD_MCP_CONTAINER_IMAGE,
        public_url=CLOUD_MCP_PREVIEW_PUBLIC_URL,
        oauth_client_id=CLOUD_MCP_OAUTH_CLIENT_ID,
        oauth_client_secret_id=CLOUD_MCP_OAUTH_CLIENT_SECRET_ID,
        **mcp_common,
    )

    mcp_services = {
        OPS_MCP_SERVICE_NAME: ops_mcp,
        OPS_MCP_PREVIEW_SERVICE_NAME: ops_mcp_preview,
        CLOUD_MCP_SERVICE_NAME: cloud_mcp,
        CLOUD_MCP_PREVIEW_SERVICE_NAME: cloud_mcp_preview,
    }

    lb_ip, backend, lb_outputs = define_load_balancer(
        webapp_service=cloud_run_service,
        webapp_preview_service=preview_service,
        mcp_services=mcp_services,
        api_services=api_services,
    )
    dns_outputs = define_dns(lb_ip)

    outputs: OutputMap = {
        "project": PROJECT,
        "region": REGION,
        "service_name": cloud_run_service.name,
        "service_url": cloud_run_service.uri,
        "preview_service_name": preview_service.name,
        "preview_service_url": preview_service.uri,
        "preview_url": PREVIEW_PUBLIC_URL,
        "ops_mcp_service_name": ops_mcp.name,
        "ops_mcp_service_url": ops_mcp.uri,
        "ops_mcp_url": OPS_MCP_PUBLIC_URL,
        "cloud_mcp_service_name": cloud_mcp.name,
        "cloud_mcp_service_url": cloud_mcp.uri,
        "cloud_mcp_url": CLOUD_MCP_PUBLIC_URL,
        "mcp_domain": MCP_DOMAIN,
        "artifact_registry": f"{REGION}-docker.pkg.dev/{PROJECT}/{SERVICE_NAME}",
        "ops_mcp_artifact_registry": f"{REGION}-docker.pkg.dev/{PROJECT}/{OPS_MCP_SERVICE_NAME}",
        "cloud_mcp_artifact_registry": f"{REGION}-docker.pkg.dev/{PROJECT}/{CLOUD_MCP_SERVICE_NAME}",
        "backend_service": backend.name,
        **lb_outputs,
        **dns_outputs,
    }

    for secret_id, secret in secrets.items():
        outputs[f"secret.{secret_id}"] = secret.name

    for name, value in outputs.items():
        pulumi.export(name, value)


main()
