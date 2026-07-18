"""Pulumi IaC for internal MCP Cloud Run services.

Architecture:
  Cloud Run (`ops-mcp`)         <- serverless NEG (Network Endpoint Group) <- external HTTPS LB <- users
  Cloud Run (`ops-mcp-preview`) <- serverless NEG                          <- same LB (path rule) <- users

Hosted MCP servers use FastMCP's `OIDCProxy` for Keycloak OIDC authentication
and are not IAP-gated.

All internal MCP services share a single domain (`mcp.internal.airbyte.ai`)
with path-based routing and URL rewriting at the load balancer:
- `/ops-mcp/*`           -> ops-mcp prod (rewritten to `/*`)
- `/ops-mcp-preview/*`   -> ops-mcp preview (rewritten to `/*`)
- `/cloud-mcp/*`         -> cloud-mcp prod (rewritten to `/*`)
- `/cloud-mcp-preview/*` -> cloud-mcp preview (rewritten to `/*`)
- `/agent-mcp/*`         -> agent-mcp prod (rewritten to `/*`)
- `/agent-mcp-preview/*` -> agent-mcp preview (rewritten to `/*`)

Canonical hosts:
- `mcp.internal.airbyte.ai` (internal hosted MCP servers)

Keycloak client setup is intentionally out of scope -- see
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
MIN_INSTANCES = int(config.get("min-instances") or "1")
MAX_INSTANCES = int(config.get("max-instances") or "10")

SERVICE_ACCOUNT_ID = "internal-mcp-sa"

MCP_DOMAIN = config.get("mcp-domain") or "mcp.internal.airbyte.ai"

OPS_MCP_SERVICE_NAME = "ops-mcp"
OPS_MCP_PREVIEW_SERVICE_NAME = "ops-mcp-preview"
OPS_MCP_PATH_PREFIX = "/ops-mcp"
OPS_MCP_PREVIEW_PATH_PREFIX = "/ops-mcp-preview"
OPS_MCP_PUBLIC_URL = f"https://{MCP_DOMAIN}{OPS_MCP_PATH_PREFIX}"
OPS_MCP_PREVIEW_PUBLIC_URL = f"https://{MCP_DOMAIN}{OPS_MCP_PREVIEW_PATH_PREFIX}"
OPS_MCP_OAUTH_CLIENT_ID = (
    config.get("ops-mcp-oauth-client-id") or "airbyte-ops-mcp-client"
)

OAUTH_ISSUER = (
    config.get("oauth-issuer") or "https://cloud.airbyte.com/auth/realms/airbyte"
)

DNS_ZONE_PROJECT = config.get("dns-zone-project") or "airbyte-intranet"
DNS_ZONE_NAME = config.get("dns-zone-name") or "internal-airbyte-ai"

CLOUD_MCP_SERVICE_NAME = "cloud-mcp"
CLOUD_MCP_PREVIEW_SERVICE_NAME = "cloud-mcp-preview"
CLOUD_MCP_PATH_PREFIX = "/cloud-mcp"
CLOUD_MCP_PREVIEW_PATH_PREFIX = "/cloud-mcp-preview"

CLOUD_MCP_PUBLIC_URL = f"https://{MCP_DOMAIN}{CLOUD_MCP_PATH_PREFIX}"
CLOUD_MCP_PREVIEW_PUBLIC_URL = f"https://{MCP_DOMAIN}{CLOUD_MCP_PREVIEW_PATH_PREFIX}"

# Agent MCP is the Airbyte Agents MCP served publicly at `mcp.airbyte.ai`.
# Its source is the `agent-engine-mcp` app in `airbytehq/sonar` (a distinct
# FastMCP server, not PyAirbyte). Its internal-mirror image build + deploy is
# currently paused pending a Porter-based cross-repo image bridge; until then
# the deploy workflow no-ops `agent-mcp` (see `pause-agent-mcp`). This internal
# deployment pair lets us offer alternative auth methods and stage updates
# internally before they reach end users.
AGENT_MCP_SERVICE_NAME = "agent-mcp"
AGENT_MCP_PREVIEW_SERVICE_NAME = "agent-mcp-preview"
AGENT_MCP_PATH_PREFIX = "/agent-mcp"
AGENT_MCP_PREVIEW_PATH_PREFIX = "/agent-mcp-preview"
AGENT_MCP_PUBLIC_URL = f"https://{MCP_DOMAIN}{AGENT_MCP_PATH_PREFIX}"
AGENT_MCP_PREVIEW_PUBLIC_URL = f"https://{MCP_DOMAIN}{AGENT_MCP_PREVIEW_PATH_PREFIX}"

OPS_MCP_OAUTH_CLIENT_SECRET_ID = "ops-mcp-oauth-client-secret"

# Backend credential secrets consumed by the Ops MCP server (prod + preview).
# Created during bootstrap (see `BOOTSTRAP.md`) and looked up read-only here;
# Pulumi never creates secret containers or values -- see `CONTRIBUTING.md`.
GITHUB_TOKEN_SECRET_ID = "internal-ops-github-pat"
"""Fine-grained GitHub PAT used for workflow dispatch and PR/issue reads/comments.

Shared container (`internal-ops-` prefix) so the Ops Webapp runtime SA can adopt
it too; see `BOOTSTRAP.md`."""

ORB_API_KEY_SECRET_ID = "internal-ops-orb-api-key"
"""Orb billing API key. Shared container so the Ops Webapp can adopt it too."""

MOTHERDUCK_ADMIN_TOKEN_SECRET_ID = "internal-ops-motherduck-api-key"
"""MotherDuck admin service-account token for the query-diagnostics tools.

Shared container so the Ops Webapp can adopt it too; consumed as env
`MOTHERDUCK_ADMIN_TOKEN`."""

SLACK_BOT_TOKEN_HITL_SECRET_ID = "slack-bot-token-hitl"
"""Shared Slack bot token created by the `agent-message-bus` bootstrap."""

# Secrets wired into the Ops MCP prod + preview services (beyond the OIDC
# client secret every MCP service receives). Kept in one place so the runtime
# `secretAccessor` grants and the Cloud Run env wiring stay in sync.
OPS_MCP_BACKEND_SECRET_IDS = [
    GITHUB_TOKEN_SECRET_ID,
    ORB_API_KEY_SECRET_ID,
    MOTHERDUCK_ADMIN_TOKEN_SECRET_ID,
    SLACK_BOT_TOKEN_HITL_SECRET_ID,
]

OPS_MCP_CONTAINER_IMAGE = (
    f"{REGION}-docker.pkg.dev/{PROJECT}/{OPS_MCP_SERVICE_NAME}"
    f"/{OPS_MCP_SERVICE_NAME}:latest"
)
"""Placeholder (dummy) image tag for Ops MCP.

The `deploy-mcp-command` workflow manages the actual image via
`gcloud run services update --image=<sha-tag>`. Pulumi ignores changes to the
container image (see `ignore_changes` on the Cloud Run service) so it never
overwrites the deploy workflow's SHA-tagged revision. See
[`CONTRIBUTING.md`](./CONTRIBUTING.md) for the full deploy-vs-Pulumi ownership
rules.
"""

CLOUD_MCP_CONTAINER_IMAGE = (
    f"{REGION}-docker.pkg.dev/{PROJECT}/{CLOUD_MCP_SERVICE_NAME}"
    f"/{CLOUD_MCP_SERVICE_NAME}:latest"
)
"""Placeholder (dummy) image tag for Cloud MCP. See `OPS_MCP_CONTAINER_IMAGE`."""

AGENT_MCP_CONTAINER_IMAGE = (
    f"{REGION}-docker.pkg.dev/{PROJECT}/{AGENT_MCP_SERVICE_NAME}"
    f"/{AGENT_MCP_SERVICE_NAME}:latest"
)
"""Placeholder (dummy) image tag for Agent MCP. See `OPS_MCP_CONTAINER_IMAGE`."""

LB_PREFIX = "internal-mcp"


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
    looked up here as read-only data sources. Pulumi never creates secrets --
    see `CONTRIBUTING.md` for the ownership rule.
    """
    secret_ids = [OPS_MCP_OAUTH_CLIENT_SECRET_ID, *OPS_MCP_BACKEND_SECRET_IDS]
    return {
        secret_id: gcp.secretmanager.get_secret(
            secret_id=secret_id,
            project=PROJECT,
        )
        for secret_id in secret_ids
    }


def define_service_account(
    api_services: list[gcp.projects.Service],
) -> gcp.serviceaccount.Account:
    """Define the Cloud Run runtime service account."""
    return gcp.serviceaccount.Account(
        SERVICE_ACCOUNT_ID,
        account_id=SERVICE_ACCOUNT_ID,
        display_name="Internal MCP servers runtime service account",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )


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
    min_instances: int = 0,
    extra_envs: list[gcp.cloudrunv2.ServiceTemplateContainerEnvArgs] | None = None,
    extra_depends: list[pulumi.Resource] | None = None,
) -> gcp.cloudrunv2.Service:
    """Define a hosted MCP Cloud Run service with OIDC auth.

    Generic factory used for ops-mcp and ops-mcp-preview services. Each
    gets its own Cloud Run instance behind the shared
    `mcp.internal.airbyte.ai` load balancer.
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

    depends: list[pulumi.Resource] = [*api_services]
    if extra_depends:
        depends.extend(extra_depends)

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
                min_instance_count=min_instances,
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
            ignore_changes=[
                "client",
                "clientVersion",
                "scaling",
                "template.containers[*].image",
                "template.containers[0].startupProbe",
            ],
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


def define_cloud_armor_policy(
    api_services: list[gcp.projects.Service],
) -> gcp.compute.SecurityPolicy:
    """Define a Cloud Armor security policy for MCP backend services.

    This policy provides network-layer rate limiting as defense in depth.
    Application-layer authentication (Keycloak OIDC via `OIDCProxy`) is the
    primary access control; Cloud Armor adds edge-level throttling.

    Rules (evaluated in priority order, lowest number = highest priority):
    1. Rate limit — throttle per-IP request rate
    2. Default  — allow all (OIDC handles identity)
    """
    return gcp.compute.SecurityPolicy(
        f"{LB_PREFIX}-armor",
        name=f"{LB_PREFIX}-armor",
        project=PROJECT,
        description="Rate limiting for internal MCP services",
        rules=[
            gcp.compute.SecurityPolicyRuleArgs(
                action="throttle",
                priority=100,
                description="Rate limit: 60 requests per minute per IP",
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
                        count=60,
                        interval_sec=60,
                    ),
                    enforce_on_key="IP",
                ),
            ),
            gcp.compute.SecurityPolicyRuleArgs(
                action="allow",
                priority=2147483647,
                description="Default allow — OIDC handles identity",
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
    """Create a serverless NEG (Network Endpoint Group) + backend service pair for a Cloud Run service.

    MCP backends do not use IAP -- authentication is handled at the
    application layer via OIDC. Cloud Armor is attached for rate limiting.
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

    backend = gcp.compute.BackendService(
        f"{service_name}-backend",
        name=f"{service_name}-backend",
        project=PROJECT,
        protocol="HTTP",
        port_name="http",
        security_policy=armor_policy.self_link,
        backends=[gcp.compute.BackendServiceBackendArgs(group=neg.id)],
        opts=pulumi.ResourceOptions(
            depends_on=[neg],
        ),
    )

    return backend


def _stamp_route_rule_priorities(
    rules: list[gcp.compute.URLMapPathMatcherRouteRuleArgs],
) -> None:
    """Assign each route rule a `priority` equal to its 1-based list position.

    GCP requires route rules within a pathMatcher to have unique priorities
    that strictly increase in list order. Deriving priority from position
    (rather than hardcoding literals) keeps that invariant true by construction
    when rules are added or reordered. Rules are built with a placeholder
    `priority` (`priority` is a required constructor argument) that this
    function overwrites.
    """
    for index, rule in enumerate(rules, start=1):
        rule.priority = index


def _mcp_path_route_rule(
    path_prefix: str,
    backend: gcp.compute.BackendService,
) -> gcp.compute.URLMapPathMatcherRouteRuleArgs:
    """Create a URL Map route rule that matches a path prefix and rewrites to root.

    The rule's `priority` is constructed with a placeholder `0` (not a valid
    final value) and overwritten by list position in `define_load_balancer` --
    see `_stamp_route_rule_priorities`.
    """
    return gcp.compute.URLMapPathMatcherRouteRuleArgs(
        priority=0,
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


def _oauth_discovery_route_rules(
    *,
    path_prefix: str,
    backend: gcp.compute.BackendService,
) -> tuple[
    gcp.compute.URLMapPathMatcherRouteRuleArgs,
    gcp.compute.URLMapPathMatcherRouteRuleArgs,
]:
    """Route a routed-root MCP server's OAuth discovery documents to its backend.

    An MCP server mounted under `path_prefix` (e.g. `/cloud-mcp`) advertises its
    OAuth metadata at origin-root well-known paths that fall outside its own
    prefix. Those requests would otherwise hit the load balancer's default
    service (`ops-mcp`) and 404, so a routed-root server needs explicit rules:

    - protected-resource metadata is forwarded verbatim (no rewrite);
    - authorization-server metadata is rewritten to the origin-root path the
      server actually serves it at.

    `ops-mcp` needs no such rules because it is the load balancer default
    service and already receives these origin-root paths.

    Returns the (protected-resource, authorization-server) rule pair.
    """
    server_suffix = path_prefix.lstrip("/")
    prm_path = f"/.well-known/oauth-protected-resource/{server_suffix}"
    as_path = f"/.well-known/oauth-authorization-server/{server_suffix}"
    protected_resource_rule = gcp.compute.URLMapPathMatcherRouteRuleArgs(
        priority=0,
        match_rules=[
            gcp.compute.URLMapPathMatcherRouteRuleMatchRuleArgs(
                prefix_match=f"{prm_path}/",
            ),
            gcp.compute.URLMapPathMatcherRouteRuleMatchRuleArgs(
                full_path_match=prm_path,
            ),
        ],
        service=backend.self_link,
    )
    authorization_server_rule = gcp.compute.URLMapPathMatcherRouteRuleArgs(
        priority=0,
        match_rules=[
            gcp.compute.URLMapPathMatcherRouteRuleMatchRuleArgs(
                prefix_match=f"{as_path}/",
            ),
            gcp.compute.URLMapPathMatcherRouteRuleMatchRuleArgs(
                full_path_match=as_path,
            ),
        ],
        route_action=gcp.compute.URLMapPathMatcherRouteRuleRouteActionArgs(
            url_rewrite=gcp.compute.URLMapPathMatcherRouteRuleRouteActionUrlRewriteArgs(
                path_prefix_rewrite="/.well-known/oauth-authorization-server",
            ),
        ),
        service=backend.self_link,
    )
    return protected_resource_rule, authorization_server_rule


def define_load_balancer(
    *,
    mcp_services: dict[str, gcp.cloudrunv2.Service],
    armor_policy: gcp.compute.SecurityPolicy,
    api_services: list[gcp.projects.Service],
) -> tuple[gcp.compute.GlobalAddress, OutputMap]:
    """Define the external HTTPS load balancer for MCP services.

    MCP traffic uses path-based routing under `mcp.internal.airbyte.ai`
    with URL rewriting to strip the path prefix before forwarding to each
    Cloud Run service.

    No IAP -- MCP backends use app-level OIDC auth. Cloud Armor provides
    rate limiting at the edge.
    """
    ip_address = gcp.compute.GlobalAddress(
        f"{LB_PREFIX}-lb-ip",
        name=f"{LB_PREFIX}-lb-ip",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    # MCP backends -- one per service (no IAP; app-level OIDC auth)
    mcp_backends: dict[str, gcp.compute.BackendService] = {
        name: _define_neg_and_backend(name, svc, armor_policy)
        for name, svc in mcp_services.items()
    }

    # SSL certificate
    ssl_certificate = gcp.compute.ManagedSslCertificate(
        f"{LB_PREFIX}-ssl-cert",
        name=f"{LB_PREFIX}-ssl-cert",
        project=PROJECT,
        managed=gcp.compute.ManagedSslCertificateManagedArgs(
            domains=[MCP_DOMAIN],
        ),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    # Every routed-root MCP server needs explicit OAuth discovery rules;
    # only `ops-mcp` is exempt because it is the LB default service and
    # already receives origin-root well-known paths. That includes all the
    # preview services (they are routed-root, not the default), so without
    # these rules a preview's OAuth discovery falls through to `ops-mcp` and
    # 404s -- breaking interactive login against any preview endpoint.
    (
        cloud_mcp_prm_rule,
        cloud_mcp_as_rule,
    ) = _oauth_discovery_route_rules(
        path_prefix=CLOUD_MCP_PATH_PREFIX,
        backend=mcp_backends[CLOUD_MCP_SERVICE_NAME],
    )
    (
        agent_mcp_prm_rule,
        agent_mcp_as_rule,
    ) = _oauth_discovery_route_rules(
        path_prefix=AGENT_MCP_PATH_PREFIX,
        backend=mcp_backends[AGENT_MCP_SERVICE_NAME],
    )
    (
        ops_mcp_preview_prm_rule,
        ops_mcp_preview_as_rule,
    ) = _oauth_discovery_route_rules(
        path_prefix=OPS_MCP_PREVIEW_PATH_PREFIX,
        backend=mcp_backends[OPS_MCP_PREVIEW_SERVICE_NAME],
    )
    (
        cloud_mcp_preview_prm_rule,
        cloud_mcp_preview_as_rule,
    ) = _oauth_discovery_route_rules(
        path_prefix=CLOUD_MCP_PREVIEW_PATH_PREFIX,
        backend=mcp_backends[CLOUD_MCP_PREVIEW_SERVICE_NAME],
    )
    (
        agent_mcp_preview_prm_rule,
        agent_mcp_preview_as_rule,
    ) = _oauth_discovery_route_rules(
        path_prefix=AGENT_MCP_PREVIEW_PATH_PREFIX,
        backend=mcp_backends[AGENT_MCP_PREVIEW_SERVICE_NAME],
    )

    # MCP path-based route rules. Priority is derived from list position (see
    # `_stamp_route_rule_priorities`), so the ordering here IS the precedence --
    # GCP requires strictly increasing, unique priorities within a pathMatcher.
    mcp_route_rules = [
        cloud_mcp_prm_rule,
        _mcp_path_route_rule(
            path_prefix=OPS_MCP_PREVIEW_PATH_PREFIX,
            backend=mcp_backends[OPS_MCP_PREVIEW_SERVICE_NAME],
        ),
        _mcp_path_route_rule(
            path_prefix=OPS_MCP_PATH_PREFIX,
            backend=mcp_backends[OPS_MCP_SERVICE_NAME],
        ),
        _mcp_path_route_rule(
            path_prefix=CLOUD_MCP_PREVIEW_PATH_PREFIX,
            backend=mcp_backends[CLOUD_MCP_PREVIEW_SERVICE_NAME],
        ),
        _mcp_path_route_rule(
            path_prefix=CLOUD_MCP_PATH_PREFIX,
            backend=mcp_backends[CLOUD_MCP_SERVICE_NAME],
        ),
        cloud_mcp_as_rule,
        _mcp_path_route_rule(
            path_prefix=AGENT_MCP_PREVIEW_PATH_PREFIX,
            backend=mcp_backends[AGENT_MCP_PREVIEW_SERVICE_NAME],
        ),
        _mcp_path_route_rule(
            path_prefix=AGENT_MCP_PATH_PREFIX,
            backend=mcp_backends[AGENT_MCP_SERVICE_NAME],
        ),
        agent_mcp_prm_rule,
        agent_mcp_as_rule,
        ops_mcp_preview_prm_rule,
        ops_mcp_preview_as_rule,
        cloud_mcp_preview_prm_rule,
        cloud_mcp_preview_as_rule,
        agent_mcp_preview_prm_rule,
        agent_mcp_preview_as_rule,
    ]
    _stamp_route_rule_priorities(mcp_route_rules)

    url_map = gcp.compute.URLMap(
        f"{LB_PREFIX}-url-map",
        name=f"{LB_PREFIX}-url-map",
        project=PROJECT,
        default_service=mcp_backends[OPS_MCP_SERVICE_NAME].self_link,
        path_matchers=[
            gcp.compute.URLMapPathMatcherArgs(
                name="internal-mcp",
                default_service=mcp_backends[OPS_MCP_SERVICE_NAME].self_link,
                route_rules=mcp_route_rules,
            ),
        ],
        host_rules=[
            gcp.compute.URLMapHostRuleArgs(
                hosts=[MCP_DOMAIN],
                path_matcher="internal-mcp",
            ),
        ],
    )

    https_proxy = gcp.compute.TargetHttpsProxy(
        f"{LB_PREFIX}-https-proxy",
        name=f"{LB_PREFIX}-https-proxy",
        project=PROJECT,
        url_map=url_map.self_link,
        ssl_certificates=[ssl_certificate.self_link],
    )

    gcp.compute.GlobalForwardingRule(
        f"{LB_PREFIX}-https-forwarding-rule",
        name=f"{LB_PREFIX}-https-forwarding-rule",
        project=PROJECT,
        target=https_proxy.self_link,
        port_range="443",
        ip_address=ip_address.address,
        load_balancing_scheme="EXTERNAL",
    )

    # HTTP -> HTTPS redirect
    http_url_map = gcp.compute.URLMap(
        f"{LB_PREFIX}-http-redirect-url-map",
        name=f"{LB_PREFIX}-http-redirect-url-map",
        project=PROJECT,
        default_url_redirect=gcp.compute.URLMapDefaultUrlRedirectArgs(
            https_redirect=True,
            strip_query=False,
        ),
    )

    http_proxy = gcp.compute.TargetHttpProxy(
        f"{LB_PREFIX}-http-redirect-proxy",
        name=f"{LB_PREFIX}-http-redirect-proxy",
        project=PROJECT,
        url_map=http_url_map.self_link,
    )

    gcp.compute.GlobalForwardingRule(
        f"{LB_PREFIX}-http-forwarding-rule",
        name=f"{LB_PREFIX}-http-forwarding-rule",
        project=PROJECT,
        target=http_proxy.self_link,
        port_range="80",
        ip_address=ip_address.address,
        load_balancing_scheme="EXTERNAL",
    )

    return (
        ip_address,
        {
            "lb.ip_address": ip_address.address,
            "lb.url_map": url_map.name,
        },
    )


def define_dns(
    lb_ip: gcp.compute.GlobalAddress,
) -> OutputMap:
    """Define the DNS A record for the internal MCP domain."""
    record = gcp.dns.RecordSet(
        f"{LB_PREFIX}-dns-record",
        name=f"{MCP_DOMAIN}.",
        type="A",
        ttl=300,
        managed_zone=DNS_ZONE_NAME,
        project=DNS_ZONE_PROJECT,
        rrdatas=[lb_ip.address],
    )
    return {
        "dns.mcp_fqdn": MCP_DOMAIN,
        "dns.zone": DNS_ZONE_NAME,
        "dns.zone_project": DNS_ZONE_PROJECT,
        "dns.record": record.name,
    }


def main() -> None:
    """Define and export all internal MCP server infrastructure."""
    api_services = define_apis()
    secrets = define_secrets()
    service_account = define_service_account(api_services)
    # The runtime-SA `secretAccessor` grants for the Ops MCP backend secrets
    # (GitHub PAT, Orb key, MotherDuck token, shared Slack token) are manual
    # bootstrap steps -- same as the OAuth client secret and the ops-webapp
    # secrets -- because the deployer identity holds `roles/editor` and cannot
    # `setIamPolicy` on secret containers it did not create. See `BOOTSTRAP.md`.
    ops_mcp_backend_envs = [
        _secret_env("GITHUB_TOKEN", GITHUB_TOKEN_SECRET_ID),
        _secret_env("ORB_API_KEY", ORB_API_KEY_SECRET_ID),
        _secret_env("MOTHERDUCK_ADMIN_TOKEN", MOTHERDUCK_ADMIN_TOKEN_SECRET_ID),
        _secret_env("SLACK_BOT_TOKEN_HITL", SLACK_BOT_TOKEN_HITL_SECRET_ID),
    ]
    # MCP services
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
        min_instances=MIN_INSTANCES,
        extra_envs=ops_mcp_backend_envs,
        **mcp_common,
    )
    ops_mcp_preview = define_mcp_cloud_run_service(
        service_name=OPS_MCP_PREVIEW_SERVICE_NAME,
        description="Airbyte Ops MCP preview server for PR deploys",
        container_image=OPS_MCP_CONTAINER_IMAGE,
        public_url=OPS_MCP_PREVIEW_PUBLIC_URL,
        oauth_client_id=OPS_MCP_OAUTH_CLIENT_ID,
        oauth_client_secret_id=OPS_MCP_OAUTH_CLIENT_SECRET_ID,
        extra_envs=ops_mcp_backend_envs,
        **mcp_common,
    )
    cloud_mcp = define_mcp_cloud_run_service(
        service_name=CLOUD_MCP_SERVICE_NAME,
        description="Airbyte Cloud (Replication) MCP hosted server",
        container_image=CLOUD_MCP_CONTAINER_IMAGE,
        public_url=CLOUD_MCP_PUBLIC_URL,
        oauth_client_id=OPS_MCP_OAUTH_CLIENT_ID,
        oauth_client_secret_id=OPS_MCP_OAUTH_CLIENT_SECRET_ID,
        min_instances=MIN_INSTANCES,
        **mcp_common,
    )
    cloud_mcp_preview = define_mcp_cloud_run_service(
        service_name=CLOUD_MCP_PREVIEW_SERVICE_NAME,
        description="Airbyte Cloud MCP preview server for PR deploys",
        container_image=CLOUD_MCP_CONTAINER_IMAGE,
        public_url=CLOUD_MCP_PREVIEW_PUBLIC_URL,
        oauth_client_id=OPS_MCP_OAUTH_CLIENT_ID,
        oauth_client_secret_id=OPS_MCP_OAUTH_CLIENT_SECRET_ID,
        **mcp_common,
    )
    agent_mcp = define_mcp_cloud_run_service(
        service_name=AGENT_MCP_SERVICE_NAME,
        description="Airbyte Agents MCP hosted server (internal mirror of mcp.airbyte.ai)",
        container_image=AGENT_MCP_CONTAINER_IMAGE,
        public_url=AGENT_MCP_PUBLIC_URL,
        oauth_client_id=OPS_MCP_OAUTH_CLIENT_ID,
        oauth_client_secret_id=OPS_MCP_OAUTH_CLIENT_SECRET_ID,
        min_instances=MIN_INSTANCES,
        **mcp_common,
    )
    agent_mcp_preview = define_mcp_cloud_run_service(
        service_name=AGENT_MCP_PREVIEW_SERVICE_NAME,
        description="Airbyte Agents MCP preview server for PR deploys",
        container_image=AGENT_MCP_CONTAINER_IMAGE,
        public_url=AGENT_MCP_PREVIEW_PUBLIC_URL,
        oauth_client_id=OPS_MCP_OAUTH_CLIENT_ID,
        oauth_client_secret_id=OPS_MCP_OAUTH_CLIENT_SECRET_ID,
        **mcp_common,
    )

    mcp_services = {
        OPS_MCP_SERVICE_NAME: ops_mcp,
        OPS_MCP_PREVIEW_SERVICE_NAME: ops_mcp_preview,
        CLOUD_MCP_SERVICE_NAME: cloud_mcp,
        CLOUD_MCP_PREVIEW_SERVICE_NAME: cloud_mcp_preview,
        AGENT_MCP_SERVICE_NAME: agent_mcp,
        AGENT_MCP_PREVIEW_SERVICE_NAME: agent_mcp_preview,
    }

    armor_policy = define_cloud_armor_policy(api_services)

    lb_ip, lb_outputs = define_load_balancer(
        mcp_services=mcp_services,
        armor_policy=armor_policy,
        api_services=api_services,
    )
    dns_outputs = define_dns(lb_ip)

    outputs: OutputMap = {
        "project": PROJECT,
        "region": REGION,
        "ops_mcp_service_name": ops_mcp.name,
        "ops_mcp_service_url": ops_mcp.uri,
        "ops_mcp_url": OPS_MCP_PUBLIC_URL,
        "ops_mcp_preview_service_name": ops_mcp_preview.name,
        "ops_mcp_preview_service_url": ops_mcp_preview.uri,
        "ops_mcp_preview_url": OPS_MCP_PREVIEW_PUBLIC_URL,
        "cloud_mcp_service_name": cloud_mcp.name,
        "cloud_mcp_service_url": cloud_mcp.uri,
        "cloud_mcp_url": CLOUD_MCP_PUBLIC_URL,
        "cloud_mcp_preview_service_name": cloud_mcp_preview.name,
        "cloud_mcp_preview_service_url": cloud_mcp_preview.uri,
        "cloud_mcp_preview_url": CLOUD_MCP_PREVIEW_PUBLIC_URL,
        "agent_mcp_service_name": agent_mcp.name,
        "agent_mcp_service_url": agent_mcp.uri,
        "agent_mcp_url": AGENT_MCP_PUBLIC_URL,
        "agent_mcp_preview_service_name": agent_mcp_preview.name,
        "agent_mcp_preview_service_url": agent_mcp_preview.uri,
        "agent_mcp_preview_url": AGENT_MCP_PREVIEW_PUBLIC_URL,
        "mcp_domain": MCP_DOMAIN,
        "ops_mcp_artifact_registry": (
            f"{REGION}-docker.pkg.dev/{PROJECT}/{OPS_MCP_SERVICE_NAME}"
        ),
        "cloud_mcp_artifact_registry": (
            f"{REGION}-docker.pkg.dev/{PROJECT}/{CLOUD_MCP_SERVICE_NAME}"
        ),
        "agent_mcp_artifact_registry": (
            f"{REGION}-docker.pkg.dev/{PROJECT}/{AGENT_MCP_SERVICE_NAME}"
        ),
        "cloud_armor_policy": armor_policy.name,
        **lb_outputs,
        **dns_outputs,
    }

    for secret_id, secret in secrets.items():
        outputs[f"secret.{secret_id}"] = secret.name

    for name, value in outputs.items():
        pulumi.export(name, value)


main()
