"""Pulumi IaC for the Airbyte Ops Webapp shared Cloud Run service.

Architecture:
  Cloud Run (`ops-webapp`) <- serverless NEG <- external HTTPS LB <- users

The app-level Keycloak OAuth flow protects the webapp itself. The bootstrap
process owns the image repository and OAuth secret container; this stack reuses
those prerequisites and owns the runtime and edge resources needed for the
canonical shared host `ops.internal.airbyte.ai`. Keycloak client setup is
intentionally out of scope.
"""

from __future__ import annotations

import pulumi
import pulumi_gcp as gcp

OutputMap = dict[str, object]
SecretRef = gcp.secretmanager.Secret | gcp.secretmanager.GetSecretResult

config = pulumi.Config()
gcp_config = pulumi.Config("gcp")

PROJECT = gcp_config.require("project")
REGION = gcp_config.get("region") or "us-west3"
MIN_INSTANCES = int(config.get("min-instances") or "0")
MAX_INSTANCES = int(config.get("max-instances") or "10")

SERVICE_NAME = "ops-webapp"
DOMAIN = config.get("domain") or "ops.internal.airbyte.ai"
PUBLIC_URL = config.get("public-url") or f"https://{DOMAIN}"
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
CONTAINER_IMAGE = (
    f"{REGION}-docker.pkg.dev/{PROJECT}/{SERVICE_NAME}/{SERVICE_NAME}:latest"
)


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
    """Read Secret Manager containers needed by the service."""
    return {
        OAUTH_CLIENT_SECRET_ID: gcp.secretmanager.get_secret(
            secret_id=OAUTH_CLIENT_SECRET_ID,
            project=PROJECT,
        )
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


def define_load_balancer(
    service: gcp.cloudrunv2.Service,
    api_services: list[gcp.projects.Service],
) -> tuple[gcp.compute.GlobalAddress, gcp.compute.BackendService, OutputMap]:
    """Define the external HTTP(S) load balancer for `ops.internal.airbyte.ai`."""
    ip_address = gcp.compute.GlobalAddress(
        f"{SERVICE_NAME}-lb-ip",
        name=f"{SERVICE_NAME}-lb-ip",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    neg = gcp.compute.RegionNetworkEndpointGroup(
        f"{SERVICE_NAME}-neg",
        name=f"{SERVICE_NAME}-neg",
        project=PROJECT,
        region=REGION,
        network_endpoint_type="SERVERLESS",
        cloud_run=gcp.compute.RegionNetworkEndpointGroupCloudRunArgs(
            service=service.name,
        ),
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=[service],
        ),
    )

    backend = gcp.compute.BackendService(
        f"{SERVICE_NAME}-backend",
        name=f"{SERVICE_NAME}-backend",
        project=PROJECT,
        protocol="HTTP",
        port_name="http",
        backends=[gcp.compute.BackendServiceBackendArgs(group=neg.id)],
        opts=pulumi.ResourceOptions(depends_on=[neg]),
    )

    ssl_certificate = gcp.compute.ManagedSslCertificate(
        f"{SERVICE_NAME}-ssl-cert",
        name=f"{SERVICE_NAME}-ssl-cert",
        project=PROJECT,
        managed=gcp.compute.ManagedSslCertificateManagedArgs(domains=[DOMAIN]),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    url_map = gcp.compute.URLMap(
        f"{SERVICE_NAME}-url-map",
        name=f"{SERVICE_NAME}-url-map",
        project=PROJECT,
        default_service=backend.self_link,
    )

    https_proxy = gcp.compute.TargetHttpsProxy(
        f"{SERVICE_NAME}-https-proxy",
        name=f"{SERVICE_NAME}-https-proxy",
        project=PROJECT,
        url_map=url_map.self_link,
        ssl_certificates=[ssl_certificate.self_link],
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
        backend,
        {
            "lb.ip_address": ip_address.address,
            "lb.backend_service": backend.name,
            "lb.url": PUBLIC_URL,
        },
    )


def define_dns(
    lb_ip: gcp.compute.GlobalAddress,
) -> OutputMap:
    """Define the DNS A record in the existing `internal.airbyte.ai` zone."""
    record = gcp.dns.RecordSet(
        f"{SERVICE_NAME}-dns-record",
        name=f"{DOMAIN}.",
        type="A",
        ttl=300,
        managed_zone=DNS_ZONE_NAME,
        project=DNS_ZONE_PROJECT,
        rrdatas=[lb_ip.address],
    )
    return {
        "dns.fqdn": DOMAIN,
        "dns.zone": DNS_ZONE_NAME,
        "dns.zone_project": DNS_ZONE_PROJECT,
        "dns.record": record.name,
    }


def main() -> None:
    """Define and export all Ops Webapp infrastructure resources."""
    api_services = define_apis()
    secrets = define_secrets()
    service_account = define_service_account(api_services)
    cloud_run_service = define_cloud_run_service(
        service_account,
        api_services,
    )
    lb_ip, backend, lb_outputs = define_load_balancer(cloud_run_service, api_services)
    dns_outputs = define_dns(lb_ip)

    outputs: OutputMap = {
        "project": PROJECT,
        "region": REGION,
        "service_name": cloud_run_service.name,
        "service_url": cloud_run_service.uri,
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
