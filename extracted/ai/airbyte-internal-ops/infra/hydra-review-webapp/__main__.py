"""Pulumi infrastructure for Hydra Everywhere on Cloud Run.

The production, preview, and default-Hydra comparison services are fronted
by one HTTPS load balancer with IAP, Cloud Armor, managed certificates, and
internal DNS records.
"""

from __future__ import annotations

import pulumi
import pulumi_gcp as gcp
import pulumi_random as random

OutputMap = dict[str, object]

config = pulumi.Config("hydra-review-webapp")
gcp_config = pulumi.Config("gcp")


def _require_config(name: str) -> str:
    """Require a non-placeholder stack setting."""
    value = config.require(name)
    if value.startswith("REPLACE_WITH_"):
        raise ValueError(
            f"Set hydra-review-webapp:{name} to its real value before applying."
        )
    return value


PROJECT = gcp_config.require("project")
REGION = gcp_config.require("region")
DOMAIN = config.require("domain")
PREVIEW_DOMAIN = config.require("preview-domain")
HYDRA_PREVIEW_DOMAIN = config.require("hydra-preview-domain")
PUBLIC_URL = f"https://{DOMAIN}"
PREVIEW_PUBLIC_URL = f"https://{PREVIEW_DOMAIN}"
HYDRA_PREVIEW_PUBLIC_URL = f"https://{HYDRA_PREVIEW_DOMAIN}"
DEVIN_ORG_ID = _require_config("devin-org-id")
GITHUB_CLIENT_ID = _require_config("github-client-id")
DNS_ZONE_PROJECT = config.get("dns-zone-project") or "airbyte-intranet"
DNS_ZONE_NAME = config.get("dns-zone-name") or "internal-airbyte-ai"

SERVICE_NAME = "hydra-review-webapp"
PREVIEW_SERVICE_NAME = "hydra-review-webapp-preview"
HYDRA_PREVIEW_SERVICE_NAME = "hydra-review-webapp-hydra-preview"
RUNTIME_SERVICE_ACCOUNT_ID = "hydra-review-webapp-sa"
ARTIFACT_REGISTRY_REPOSITORY_ID = "hydra-review-webapp"
CONTAINER_IMAGE = "us-docker.pkg.dev/cloudrun/container/hello"
"""Pulumi placeholder image; the deploy workflow replaces it with SHA tags."""
CONTAINER_RESOURCES = {"cpu": "1", "memory": "1Gi"}
MAX_INSTANCE_REQUEST_CONCURRENCY = 40
AIRBYTE_DOMAIN = "airbyte.io"

GITHUB_CLIENT_SECRET_ID = "hydra-review-webapp-github-client-secret"
BETTER_AUTH_SECRET_ID = "hydra-review-webapp-better-auth-secret"
DEVIN_API_KEY_SECRET_ID = "devin-ai-api-key"


def define_apis() -> list[gcp.projects.Service]:
    """Enable APIs needed by the services and load balancer."""
    api_ids = [
        "artifactregistry.googleapis.com",
        "compute.googleapis.com",
        "dns.googleapis.com",
        "iap.googleapis.com",
        "iam.googleapis.com",
        "run.googleapis.com",
        "secretmanager.googleapis.com",
    ]
    return [
        gcp.projects.Service(
            f"hydra-review-webapp-enable-{api_id.replace('.', '-')}",
            service=api_id,
            project=PROJECT,
            disable_on_destroy=False,
        )
        for api_id in api_ids
    ]


def define_artifact_registry(
    api_services: list[gcp.projects.Service],
) -> gcp.artifactregistry.Repository:
    """Create the Docker repository used by the deployment workflow."""
    return gcp.artifactregistry.Repository(
        "hydra-review-webapp-artifact-registry",
        repository_id=ARTIFACT_REGISTRY_REPOSITORY_ID,
        location=REGION,
        project=PROJECT,
        format="DOCKER",
        description="Hydra Everywhere Cloud Run images",
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )


def define_service_account(
    api_services: list[gcp.projects.Service],
) -> gcp.serviceaccount.Account:
    """Create the Cloud Run runtime service account."""
    return gcp.serviceaccount.Account(
        "hydra-review-webapp-runtime-service-account",
        account_id=RUNTIME_SERVICE_ACCOUNT_ID,
        display_name="Hydra Everywhere Cloud Run runtime",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )


def define_secrets(
    service_account: gcp.serviceaccount.Account,
    api_services: list[gcp.projects.Service],
) -> tuple[
    dict[str, pulumi.Input[str]],
    list[gcp.secretmanager.SecretIamMember],
    gcp.secretmanager.SecretVersion,
]:
    """Look up shared secrets and generate the Better Auth secret."""
    secret_ids = [
        GITHUB_CLIENT_SECRET_ID,
        DEVIN_API_KEY_SECRET_ID,
    ]
    secrets: dict[str, pulumi.Input[str]] = {}
    grants: list[gcp.secretmanager.SecretIamMember] = []
    for secret_id in secret_ids:
        secret = gcp.secretmanager.get_secret(
            secret_id=secret_id,
            project=PROJECT,
        )
        secrets[secret_id] = secret.name
        grants.append(
            gcp.secretmanager.SecretIamMember(
                f"hydra-review-webapp-{secret_id}-runtime-access",
                project=PROJECT,
                secret_id=secret_id,
                role="roles/secretmanager.secretAccessor",
                member=service_account.email.apply(
                    lambda email: f"serviceAccount:{email}"
                ),
            )
        )

    secret_value = random.RandomBytes(
        "hydra-review-webapp-better-auth-secret-value",
        length=32,
        opts=pulumi.ResourceOptions(protect=True),
    )
    secret = gcp.secretmanager.Secret(
        "hydra-review-webapp-better-auth-secret",
        secret_id=BETTER_AUTH_SECRET_ID,
        project=PROJECT,
        replication=gcp.secretmanager.SecretReplicationArgs(
            auto=gcp.secretmanager.SecretReplicationAutoArgs()
        ),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    secrets[BETTER_AUTH_SECRET_ID] = secret.name
    version = gcp.secretmanager.SecretVersion(
        "hydra-review-webapp-better-auth-secret-version",
        secret=secret.id,
        secret_data=secret_value.base64,
    )
    grants.append(
        gcp.secretmanager.SecretIamMember(
            "hydra-review-webapp-better-auth-secret-runtime-access",
            project=PROJECT,
            secret_id=secret.id,
            role="roles/secretmanager.secretAccessor",
            member=service_account.email.apply(lambda email: f"serviceAccount:{email}"),
        )
    )
    return secrets, grants, version


def define_iap(
    api_services: list[gcp.projects.Service],
) -> gcp.projects.ServiceIdentity:
    """Ensure the project IAP service identity exists for Cloud Run invoker grants."""
    return gcp.projects.ServiceIdentity(
        "iap-service-identity",
        service="iap.googleapis.com",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )


def _env(
    name: str,
    value: str,
) -> gcp.cloudrunv2.ServiceTemplateContainerEnvArgs:
    """Define a literal Cloud Run environment variable."""
    return gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(name=name, value=value)


def _secret_env(
    name: str,
    secret_id: str,
) -> gcp.cloudrunv2.ServiceTemplateContainerEnvArgs:
    """Define an environment variable backed by Secret Manager."""
    return gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
        name=name,
        value_source=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceArgs(
            secret_key_ref=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceSecretKeyRefArgs(
                secret=secret_id,
                version="latest",
            ),
        ),
    )


def _define_cloud_run_service(
    *,
    name: str,
    public_url: str,
    github_client_id: str,
    github_client_secret_id: str,
    sentry_environment: str,
    mine_mode: bool,
    min_instances: int,
    max_instances: int,
    service_account: gcp.serviceaccount.Account,
    iap_identity: gcp.projects.ServiceIdentity,
    api_services: list[gcp.projects.Service],
    secret_grants: list[gcp.secretmanager.SecretIamMember],
    better_auth_secret_version: gcp.secretmanager.SecretVersion,
) -> gcp.cloudrunv2.Service:
    """Define one Hydra Everywhere Cloud Run service."""
    app_envs = [
        _env("APP_URL", public_url),
        _env("REQUIRED_ORG", "airbytehq"),
        _env("DEVIN_ORG_ID", DEVIN_ORG_ID),
        _env("GITHUB_CLIENT_ID", github_client_id),
        _env("SENTRY_ENVIRONMENT", sentry_environment),
    ]
    if mine_mode:
        app_envs.extend(
            [
                _env("APP_TITLE", "My PRs"),
                _env("APP_VIEWS", "mine"),
                _env("GITHUB_REPO_SEARCH_SCOPE", "org:airbytehq"),
                _env("PR_SEARCH_TARGETS", "author:@me,user-review-requested:@me"),
                _env("LABEL_DEFER", "ai-review-snooze"),
            ]
        )
    app_envs.extend(
        [
            _secret_env("GITHUB_CLIENT_SECRET", github_client_secret_id),
            _secret_env("BETTER_AUTH_SECRET", BETTER_AUTH_SECRET_ID),
            _secret_env("DEVIN_API_KEY", DEVIN_API_KEY_SECRET_ID),
        ]
    )
    service = gcp.cloudrunv2.Service(
        f"{name}-cloud-run-service",
        name=name,
        project=PROJECT,
        location=REGION,
        description=f"Hydra Everywhere service for {public_url}",
        deletion_protection=False,
        ingress="INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER",
        template=gcp.cloudrunv2.ServiceTemplateArgs(
            service_account=service_account.email,
            max_instance_request_concurrency=MAX_INSTANCE_REQUEST_CONCURRENCY,
            scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
                min_instance_count=min_instances,
                max_instance_count=max_instances,
            ),
            containers=[
                gcp.cloudrunv2.ServiceTemplateContainerArgs(
                    image=CONTAINER_IMAGE,
                    ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                        container_port=8080,
                    ),
                    resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                        limits=CONTAINER_RESOURCES,
                        startup_cpu_boost=True,
                    ),
                    envs=app_envs,
                )
            ],
        ),
        opts=pulumi.ResourceOptions(
            delete_before_replace=False,
            depends_on=[
                *api_services,
                *secret_grants,
                better_auth_secret_version,
            ],
            ignore_changes=[
                "client",
                "clientVersion",
                "scaling",
                "template.containers[*].image",
            ],
        ),
    )

    gcp.cloudrunv2.ServiceIamMember(
        f"{name}-iap-invoker",
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


def define_cloud_armor_policy(
    api_services: list[gcp.projects.Service],
) -> gcp.compute.SecurityPolicy:
    """Define edge rate limiting for the Hydra Everywhere backends."""
    return gcp.compute.SecurityPolicy(
        "hydra-review-webapp-armor",
        name="hydra-review-webapp-armor",
        project=PROJECT,
        description="Rate limiting for Hydra Everywhere backends",
        rules=[
            gcp.compute.SecurityPolicyRuleArgs(
                action="throttle",
                priority=100,
                description="Rate limit: 360 requests per minute per IP",
                match=gcp.compute.SecurityPolicyRuleMatchArgs(
                    versioned_expr="SRC_IPS_V1",
                    config=gcp.compute.SecurityPolicyRuleMatchConfigArgs(
                        src_ip_ranges=["*"],
                    ),
                ),
                rate_limit_options=gcp.compute.SecurityPolicyRuleRateLimitOptionsArgs(
                    conform_action="allow",
                    exceed_action="deny(429)",
                    rate_limit_threshold=gcp.compute.SecurityPolicyRuleRateLimitOptionsRateLimitThresholdArgs(
                        count=360,
                        interval_sec=60,
                    ),
                    enforce_on_key="IP",
                ),
            ),
            gcp.compute.SecurityPolicyRuleArgs(
                action="allow",
                priority=2147483647,
                description="Default allow; IAP handles identity",
                match=gcp.compute.SecurityPolicyRuleMatchArgs(
                    versioned_expr="SRC_IPS_V1",
                    config=gcp.compute.SecurityPolicyRuleMatchConfigArgs(
                        src_ip_ranges=["*"],
                    ),
                ),
            ),
        ],
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )


def _define_neg_and_backend(
    service_name: str,
    cloud_run_service: gcp.cloudrunv2.Service,
    armor_policy: gcp.compute.SecurityPolicy,
) -> gcp.compute.BackendService:
    """Create a serverless NEG and IAP-enabled backend for one service."""
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
        security_policy=armor_policy.self_link,
        opts=pulumi.ResourceOptions(
            depends_on=[neg, armor_policy],
        ),
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
    *,
    production_service: gcp.cloudrunv2.Service,
    preview_service: gcp.cloudrunv2.Service,
    hydra_preview_service: gcp.cloudrunv2.Service,
    armor_policy: gcp.compute.SecurityPolicy,
    api_services: list[gcp.projects.Service],
) -> tuple[gcp.compute.GlobalAddress, gcp.compute.BackendService]:
    """Define the shared HTTPS load balancer and its host rules."""
    ip_address = gcp.compute.GlobalAddress(
        "hydra-review-webapp-lb-ip",
        name="hydra-review-webapp-lb-ip",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    production_backend = _define_neg_and_backend(
        SERVICE_NAME,
        production_service,
        armor_policy,
    )
    preview_backend = _define_neg_and_backend(
        PREVIEW_SERVICE_NAME,
        preview_service,
        armor_policy,
    )
    hydra_preview_backend = _define_neg_and_backend(
        HYDRA_PREVIEW_SERVICE_NAME,
        hydra_preview_service,
        armor_policy,
    )
    production_certificate = gcp.compute.ManagedSslCertificate(
        "hydra-review-webapp-ssl-cert",
        name="hydra-review-webapp-ssl-cert",
        project=PROJECT,
        managed=gcp.compute.ManagedSslCertificateManagedArgs(
            domains=[DOMAIN],
        ),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    preview_certificate = gcp.compute.ManagedSslCertificate(
        "hydra-review-webapp-preview-ssl-cert",
        name="hydra-review-webapp-preview-ssl-cert",
        project=PROJECT,
        managed=gcp.compute.ManagedSslCertificateManagedArgs(
            domains=[PREVIEW_DOMAIN],
        ),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    hydra_preview_certificate = gcp.compute.ManagedSslCertificate(
        "hydra-review-webapp-hydra-preview-ssl-cert",
        name="hydra-review-webapp-hydra-preview-ssl-cert",
        project=PROJECT,
        managed=gcp.compute.ManagedSslCertificateManagedArgs(
            domains=[HYDRA_PREVIEW_DOMAIN],
        ),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    url_map = gcp.compute.URLMap(
        "hydra-review-webapp-url-map",
        name="hydra-review-webapp-url-map",
        project=PROJECT,
        default_service=production_backend.self_link,
        host_rules=[
            gcp.compute.URLMapHostRuleArgs(
                hosts=[DOMAIN],
                path_matcher="production",
            ),
            gcp.compute.URLMapHostRuleArgs(
                hosts=[PREVIEW_DOMAIN],
                path_matcher="preview",
            ),
            gcp.compute.URLMapHostRuleArgs(
                hosts=[HYDRA_PREVIEW_DOMAIN],
                path_matcher="hydra-preview",
            ),
        ],
        path_matchers=[
            gcp.compute.URLMapPathMatcherArgs(
                name="production",
                default_service=production_backend.self_link,
            ),
            gcp.compute.URLMapPathMatcherArgs(
                name="preview",
                default_service=preview_backend.self_link,
            ),
            gcp.compute.URLMapPathMatcherArgs(
                name="hydra-preview",
                default_service=hydra_preview_backend.self_link,
            ),
        ],
    )
    https_proxy = gcp.compute.TargetHttpsProxy(
        "hydra-review-webapp-https-proxy",
        name="hydra-review-webapp-https-proxy",
        project=PROJECT,
        url_map=url_map.self_link,
        ssl_certificates=[
            production_certificate.self_link,
            preview_certificate.self_link,
            hydra_preview_certificate.self_link,
        ],
    )
    gcp.compute.GlobalForwardingRule(
        "hydra-review-webapp-https-forwarding-rule",
        name="hydra-review-webapp-https-forwarding-rule",
        project=PROJECT,
        target=https_proxy.self_link,
        port_range="443",
        ip_address=ip_address.address,
        load_balancing_scheme="EXTERNAL",
    )
    redirect_map = gcp.compute.URLMap(
        "hydra-review-webapp-http-redirect-url-map",
        name="hydra-review-webapp-http-redirect-url-map",
        project=PROJECT,
        default_url_redirect=gcp.compute.URLMapDefaultUrlRedirectArgs(
            https_redirect=True,
            strip_query=False,
        ),
    )
    http_proxy = gcp.compute.TargetHttpProxy(
        "hydra-review-webapp-http-redirect-proxy",
        name="hydra-review-webapp-http-redirect-proxy",
        project=PROJECT,
        url_map=redirect_map.self_link,
    )
    gcp.compute.GlobalForwardingRule(
        "hydra-review-webapp-http-forwarding-rule",
        name="hydra-review-webapp-http-forwarding-rule",
        project=PROJECT,
        target=http_proxy.self_link,
        port_range="80",
        ip_address=ip_address.address,
        load_balancing_scheme="EXTERNAL",
    )
    return ip_address, production_backend


def define_dns(lb_ip: gcp.compute.GlobalAddress) -> None:
    """Create A records for the production and both preview hosts."""
    for name, domain in (
        (SERVICE_NAME, DOMAIN),
        (PREVIEW_SERVICE_NAME, PREVIEW_DOMAIN),
        (HYDRA_PREVIEW_SERVICE_NAME, HYDRA_PREVIEW_DOMAIN),
    ):
        gcp.dns.RecordSet(
            f"{name}-dns-record",
            name=f"{domain}.",
            type="A",
            ttl=300,
            managed_zone=DNS_ZONE_NAME,
            project=DNS_ZONE_PROJECT,
            rrdatas=[lb_ip.address],
        )


def main() -> None:
    """Define and export all Hydra Everywhere infrastructure."""
    api_services = define_apis()
    repository = define_artifact_registry(api_services)
    service_account = define_service_account(api_services)
    secrets, secret_grants, better_auth_secret_version = define_secrets(
        service_account,
        api_services,
    )
    iap_identity = define_iap(api_services)

    production_service = _define_cloud_run_service(
        name=SERVICE_NAME,
        public_url=PUBLIC_URL,
        github_client_id=GITHUB_CLIENT_ID,
        github_client_secret_id=GITHUB_CLIENT_SECRET_ID,
        sentry_environment="production",
        mine_mode=True,
        min_instances=1,
        max_instances=5,
        service_account=service_account,
        iap_identity=iap_identity,
        api_services=api_services,
        secret_grants=secret_grants,
        better_auth_secret_version=better_auth_secret_version,
    )
    preview_service = _define_cloud_run_service(
        name=PREVIEW_SERVICE_NAME,
        public_url=PREVIEW_PUBLIC_URL,
        github_client_id=GITHUB_CLIENT_ID,
        github_client_secret_id=GITHUB_CLIENT_SECRET_ID,
        sentry_environment="preview",
        mine_mode=True,
        min_instances=0,
        max_instances=2,
        service_account=service_account,
        iap_identity=iap_identity,
        api_services=api_services,
        secret_grants=secret_grants,
        better_auth_secret_version=better_auth_secret_version,
    )
    hydra_preview_service = _define_cloud_run_service(
        name=HYDRA_PREVIEW_SERVICE_NAME,
        public_url=HYDRA_PREVIEW_PUBLIC_URL,
        github_client_id=GITHUB_CLIENT_ID,
        github_client_secret_id=GITHUB_CLIENT_SECRET_ID,
        sentry_environment="hydra-preview",
        mine_mode=False,
        min_instances=0,
        max_instances=2,
        service_account=service_account,
        iap_identity=iap_identity,
        api_services=api_services,
        secret_grants=secret_grants,
        better_auth_secret_version=better_auth_secret_version,
    )
    armor_policy = define_cloud_armor_policy(api_services)
    lb_ip, production_backend = define_load_balancer(
        production_service=production_service,
        preview_service=preview_service,
        hydra_preview_service=hydra_preview_service,
        armor_policy=armor_policy,
        api_services=api_services,
    )
    define_dns(lb_ip)

    outputs: OutputMap = {
        "project": PROJECT,
        "region": REGION,
        "service_name": production_service.name,
        "service_url": PUBLIC_URL,
        "preview_service_name": preview_service.name,
        "preview_service_url": PREVIEW_PUBLIC_URL,
        "hydra_preview_service_name": hydra_preview_service.name,
        "hydra_preview_service_url": HYDRA_PREVIEW_PUBLIC_URL,
        "artifact_registry": repository.name,
        "artifact_registry_image": (
            f"{REGION}-docker.pkg.dev/{PROJECT}/"
            f"{ARTIFACT_REGISTRY_REPOSITORY_ID}/{SERVICE_NAME}"
        ),
        "runtime_service_account": service_account.email,
        "lb.ip_address": lb_ip.address,
        "lb.backend_service": production_backend.name,
        "dns.zone": DNS_ZONE_NAME,
        "dns.zone_project": DNS_ZONE_PROJECT,
    }
    for secret_id, secret in secrets.items():
        outputs[f"secret.{secret_id}"] = secret
    for name, value in outputs.items():
        pulumi.export(name, value)


main()
