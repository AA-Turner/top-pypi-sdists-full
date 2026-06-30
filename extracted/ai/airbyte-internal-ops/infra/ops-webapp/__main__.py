"""Pulumi IaC for the Airbyte Ops Webapp Cloud Run services.

Architecture:
  Cloud Run (`ops-webapp`)         <- serverless NEG <- external HTTPS LB <- users
  Cloud Run (`ops-webapp-preview`) <- serverless NEG <- same LB (host rule) <- users

IAP (Identity-Aware Proxy) on the webapp LB backends enforces @airbyte.io
Google Workspace SSO before requests reach Cloud Run. The app-level
Keycloak OAuth flow provides a second auth layer inside the webapp.

Canonical hosts:
- `ops.internal.airbyte.ai` (production webapp)
- `preview.ops.internal.airbyte.ai` (PR previews)

Keycloak client setup is intentionally out of scope — see
`docs/keycloak-client-admin.md`.

MCP server hosting was removed from this stack. See
https://github.com/airbytehq/airbyte-ops-mcp/issues/984 for the proposal
to host MCP servers in a dedicated `infra/internal-mcp-servers/` subproject.
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
MIN_INSTANCES = int(config.get("min-instances") or "1")
MAX_INSTANCES = int(config.get("max-instances") or "10")

SERVICE_NAME = "ops-webapp"
DOMAIN = config.get("domain") or "ops.internal.airbyte.ai"
PUBLIC_URL = config.get("public-url") or f"https://{DOMAIN}"

PREVIEW_SERVICE_NAME = "ops-webapp-preview"
PREVIEW_DOMAIN = f"preview.{DOMAIN}"
PREVIEW_PUBLIC_URL = f"https://{PREVIEW_DOMAIN}"

OAUTH_ISSUER = (
    config.get("oauth-issuer") or "https://cloud.airbyte.com/auth/realms/airbyte"
)
OAUTH_CLIENT_ID = config.get("oauth-client-id") or "airbyte-ops-webapp-client"
AIRBYTE_CONFIG_API_URL = (
    config.get("airbyte-config-api-url") or "https://cloud.airbyte.com/api/v1"
)

DNS_ZONE_PROJECT = config.get("dns-zone-project") or "airbyte-intranet"
DNS_ZONE_NAME = config.get("dns-zone-name") or "internal-airbyte-ai"

AIRBYTE_DOMAIN = "airbyte.io"

OAUTH_CLIENT_SECRET_ID = "ops-webapp-oauth-client-secret"
GOOGLE_OAUTH_CLIENT_SECRET_ID = "ops-webapp-google-oauth-client-secret"
# The container image tag is a placeholder — the deploy-ops-webapp workflow
# manages the actual image via `gcloud run services update --image=<sha-tag>`.
# Pulumi ignores changes to the container image (see ignore_changes below)
# to avoid overwriting the deploy workflow's SHA-tagged revision.
CONTAINER_IMAGE = (
    f"{REGION}-docker.pkg.dev/{PROJECT}/{SERVICE_NAME}/{SERVICE_NAME}:latest"
)


def define_apis() -> list[gcp.projects.Service]:
    """Define required API enablements for the runtime project."""
    api_ids = [
        "artifactregistry.googleapis.com",
        "compute.googleapis.com",
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
    }


def define_iap(
    api_services: list[gcp.projects.Service],
) -> gcp.projects.ServiceIdentity:
    """Provision the IAP service agent for the webapp LB backend services.

    IAP enforces `@airbyte.io` Google Workspace SSO at the load-balancer
    layer, before requests reach the Cloud Run webapp services.  The webapp
    backends use GCP's Google-managed OAuth client (no custom OAuth client
    required).

    A `ServiceIdentity` for `iap.googleapis.com` forces GCP to provision
    the IAP service agent before downstream IAM bindings reference it.

    Returns the IAP service identity (whose `.email` is used as the Cloud
    Run invoker instead of `allUsers`).
    """
    # Force-create the IAP service agent so it exists before IAM bindings.
    iap_identity = gcp.projects.ServiceIdentity(
        "iap-service-identity",
        service="iap.googleapis.com",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    return iap_identity


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
    *,
    iap_identity: gcp.projects.ServiceIdentity,
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
            ignore_changes=["template.containers[*].image"],
        ),
    )

    gcp.cloudrunv2.ServiceIamMember(
        f"{SERVICE_NAME}-iap-invoker",
        project=PROJECT,
        location=REGION,
        name=service.name,
        role="roles/run.invoker",
        member=iap_identity.email.apply(lambda email: f"serviceAccount:{email}"),
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=[service, iap_identity],
        ),
    )

    return service


def define_preview_cloud_run_service(
    service_account: gcp.serviceaccount.Account,
    api_services: list[gcp.projects.Service],
    *,
    iap_identity: gcp.projects.ServiceIdentity,
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
            ignore_changes=["template.containers[*].image"],
        ),
    )

    gcp.cloudrunv2.ServiceIamMember(
        f"{PREVIEW_SERVICE_NAME}-iap-invoker",
        project=PROJECT,
        location=REGION,
        name=service.name,
        role="roles/run.invoker",
        member=iap_identity.email.apply(lambda email: f"serviceAccount:{email}"),
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=[service, iap_identity],
        ),
    )

    return service


def _define_neg_and_backend(
    service_name: str,
    cloud_run_service: gcp.cloudrunv2.Service,
    *,
    enable_iap: bool = False,
) -> gcp.compute.BackendService:
    """Create a serverless NEG + backend service pair for a Cloud Run service.

    When `enable_iap` is `True`, IAP is enabled on the backend using GCP's
    Google-managed OAuth client and `@airbyte.io` domain access is granted
    via `roles/iap.httpsResourceAccessor`.
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
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=[cloud_run_service],
        ),
    )

    iap_args = None
    if enable_iap:
        # Use GCP's Google-managed OAuth client by passing single-space
        # values, per the IAP OAuth Admin API migration guide:
        # https://cloud.google.com/iap/docs/deprecations/migrate-oauth-client
        iap_args = gcp.compute.BackendServiceIapArgs(
            enabled=True,
            oauth2_client_id=" ",
            oauth2_client_secret=" ",
        )

    backend = gcp.compute.BackendService(
        f"{service_name}-backend",
        name=f"{service_name}-backend",
        project=PROJECT,
        protocol="HTTP",
        port_name="http",
        backends=[gcp.compute.BackendServiceBackendArgs(group=neg.id)],
        iap=iap_args,
        opts=pulumi.ResourceOptions(depends_on=[neg]),
    )

    if enable_iap:
        gcp.iap.WebBackendServiceIamMember(
            f"{service_name}-iap-domain-access",
            project=PROJECT,
            web_backend_service=backend.name,
            role="roles/iap.httpsResourceAccessor",
            member=f"domain:{AIRBYTE_DOMAIN}",
        )

    return backend


def define_load_balancer(
    *,
    webapp_service: gcp.cloudrunv2.Service,
    webapp_preview_service: gcp.cloudrunv2.Service,
    api_services: list[gcp.projects.Service],
) -> tuple[gcp.compute.GlobalAddress, gcp.compute.BackendService, OutputMap]:
    """Define the external HTTPS load balancer.

    Webapp traffic uses host-based routing (`ops.internal.airbyte.ai` and
    `preview.ops.internal.airbyte.ai`). IAP is enabled on both webapp
    backends (prod + preview) using GCP's Google-managed OAuth client.
    """
    ip_address = gcp.compute.GlobalAddress(
        f"{SERVICE_NAME}-lb-ip",
        name=f"{SERVICE_NAME}-lb-ip",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    # Webapp backends — IAP-gated (@airbyte.io Google SSO)
    webapp_backend = _define_neg_and_backend(
        SERVICE_NAME,
        webapp_service,
        enable_iap=True,
    )
    preview_backend = _define_neg_and_backend(
        PREVIEW_SERVICE_NAME,
        webapp_preview_service,
        enable_iap=True,
    )

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
        ],
        path_matchers=[
            gcp.compute.URLMapPathMatcherArgs(
                name="preview",
                default_service=preview_backend.self_link,
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
    """Define DNS A records for production and preview domains."""
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
    return {
        "dns.fqdn": DOMAIN,
        "dns.preview_fqdn": PREVIEW_DOMAIN,
        "dns.zone": DNS_ZONE_NAME,
        "dns.zone_project": DNS_ZONE_PROJECT,
        "dns.record": record.name,
        "dns.preview_record": preview_record.name,
    }


def main() -> None:
    """Define and export all Ops Webapp infrastructure."""
    api_services = define_apis()
    secrets = define_secrets()
    service_account = define_service_account(api_services)

    iap_identity = define_iap(api_services)

    cloud_run_service = define_cloud_run_service(
        service_account,
        api_services,
        iap_identity=iap_identity,
    )
    preview_service = define_preview_cloud_run_service(
        service_account,
        api_services,
        iap_identity=iap_identity,
    )

    lb_ip, backend, lb_outputs = define_load_balancer(
        webapp_service=cloud_run_service,
        webapp_preview_service=preview_service,
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
        "artifact_registry": f"{REGION}-docker.pkg.dev/{PROJECT}/{SERVICE_NAME}",
        "backend_service": backend.name,
        **lb_outputs,
        **dns_outputs,
    }

    for secret_id, secret in secrets.items():
        outputs[f"secret.{secret_id}"] = secret.name

    for name, value in outputs.items():
        pulumi.export(name, value)


main()
