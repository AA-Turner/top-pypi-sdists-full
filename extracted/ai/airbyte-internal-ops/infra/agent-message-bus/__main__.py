"""
Pulumi Infrastructure as Code for the Agent Message Bus webhook relay service.

This module manages GCP infrastructure for a webhook-to-Devin relay service
that handles GitHub webhook events and Slack interactive components, routing
notifications to Devin AI sessions.

Architecture: https://github.com/airbytehq/airbyte-ops-mcp/issues/448

COMPONENTS:
-----------
- internal-agent-bus-cloudrun: Cloud Run deployment behind GCLB + Cloud Armor
    for general webhook/API calls (GitHub webhooks, Zendesk webhooks,
    Devin subscriptions)
- slack-webhook-cloudrun: Cloud Run deployment with public HTTPS ingress,
    exclusively for Slack interactive components
- GCLB (Google Cloud Load Balancer) fronting internal-agent-bus-cloudrun
- Cloud Armor security policies (per-path IP allowlisting on GCLB)
- Firestore database (subscription state with TTL auto-expiry)
- Secret Manager secrets (webhook secrets, API tokens)

SECURITY MODEL:
--------------
Two ingress boundaries with distinct trust models:
  Internal (via GCLB + Cloud Armor):
    /github/webhook    -> GitHub webhook IPs + X-Hub-Signature-256
    /zendesk/webhook   -> Zendesk IPs (216.198.0.0/18) + HMAC-SHA256 signature
    /subscriptions/*   -> Devin static IPs + Bearer token
    /health            -> Allow all (health checks)
  External (direct Cloud Run HTTPS):
    /slack/webhook     -> X-Slack-Signature HMAC validation (Slack best practice)
"""

import pulumi
import pulumi_gcp as gcp

# =============================================================================
# CONFIGURATION
# =============================================================================

config = pulumi.Config()
gcp_config = pulumi.Config("gcp")

PROJECT = gcp_config.require("project")
REGION = gcp_config.get("region") or "us-central1"
MIN_INSTANCES = int(config.get("min-instances") or "1")
MAX_INSTANCES = int(config.get("max-instances") or "10")

SERVICE_NAME = "agent-message-bus"
DEVIN_ORG_ID = config.require("devin-org-id")
FIRESTORE_DATABASE = "(default)"
FIRESTORE_COLLECTION = "subscriptions"

# Devin AI static IPs (from Devin docs)
DEVIN_IPS = [
    "100.20.50.251",
    "44.238.19.62",
    "52.10.84.81",
    "52.183.72.253",
    "20.172.46.235",
    "52.159.232.99",
]

# GitHub webhook source IPs (from https://api.github.com/meta, "hooks" field)
# These are CIDR ranges. Updated 2025-03 — verify periodically.
GITHUB_HOOK_CIDRS = [
    "192.30.252.0/22",
    "185.199.108.0/22",
    "140.82.112.0/20",
    "143.55.64.0/20",
]

# Zendesk webhook source IPs (from https://support.zendesk.com/hc/en-us/articles/4408842860186)
# Zendesk consolidated all outbound IPs into a single range as of Feb 2025.
ZENDESK_WEBHOOK_CIDRS = [
    "216.198.0.0/18",
]

# Slack API source IPs — Slack does not publish a fixed list.
# The slack-webhook-cloudrun deployment relies on X-Slack-Signature
# HMAC validation as its trust boundary (Slack best practice).

INTERNAL_SERVICE_NAME = "internal-agent-bus-cloudrun"
SLACK_SERVICE_NAME = "slack-webhook-cloudrun"

# =============================================================================
# ENABLE REQUIRED APIs
# =============================================================================


def define_apis() -> list[gcp.projects.Service]:
    """Define required GCP API enablements for the project."""
    api_ids = [
        "run.googleapis.com",
        "firestore.googleapis.com",
        "compute.googleapis.com",
        "secretmanager.googleapis.com",
        "artifactregistry.googleapis.com",
        "cloudbuild.googleapis.com",
    ]
    services = []
    for api_id in api_ids:
        svc = gcp.projects.Service(
            f"enable-{api_id.replace('.', '-')}",
            service=api_id,
            project=PROJECT,
            disable_on_destroy=False,
        )
        services.append(svc)
    return services


# =============================================================================
# SECRET MANAGER
# =============================================================================


def define_secrets(
    api_services: list[gcp.projects.Service],
) -> dict[str, gcp.secretmanager.Secret]:
    """Define Secret Manager secrets for the service.

    The actual secret values must be added manually after deployment via:
        gcloud secrets versions add <secret-id> --data-file=-
    """
    secret_ids = [
        "github-webhook-secret",
        "slack-signing-secret",
        "slack-bot-token-hitl",
        "subscription-api-bearer-token",
        "devin-ai-api-key",
        "zendesk-webhook-signing-secret",
    ]
    secrets: dict[str, gcp.secretmanager.Secret] = {}
    for secret_id in secret_ids:
        secret = gcp.secretmanager.Secret(
            secret_id,
            secret_id=secret_id,
            project=PROJECT,
            replication=gcp.secretmanager.SecretReplicationArgs(
                auto=gcp.secretmanager.SecretReplicationAutoArgs(),
            ),
            opts=pulumi.ResourceOptions(depends_on=api_services),
        )
        secrets[secret_id] = secret
    return secrets


# =============================================================================
# CLOUD RUN SERVICE
# =============================================================================


def define_service_account(
    api_services: list[gcp.projects.Service],
    secrets: dict[str, gcp.secretmanager.Secret],
) -> tuple[gcp.serviceaccount.Account, list[pulumi.Resource]]:
    """Define a dedicated service account for the Cloud Run service.

    Returns:
        A tuple of (service_account, iam_bindings) where iam_bindings
        includes all IAM resources that must be created before Cloud Run
        can use the service account.
    """
    sa = gcp.serviceaccount.Account(
        f"{SERVICE_NAME}-sa",
        account_id=f"{SERVICE_NAME}-sa",
        display_name="Agent Message Bus Service Account",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    iam_bindings: list[pulumi.Resource] = []

    # Grant Firestore access
    firestore_binding = gcp.projects.IAMMember(
        f"{SERVICE_NAME}-firestore-user",
        project=PROJECT,
        role="roles/datastore.user",
        member=sa.email.apply(lambda email: f"serviceAccount:{email}"),
    )
    iam_bindings.append(firestore_binding)

    # Grant Artifact Registry reader access (so Cloud Run can pull images)
    ar_binding = gcp.projects.IAMMember(
        f"{SERVICE_NAME}-ar-reader",
        project=PROJECT,
        role="roles/artifactregistry.reader",
        member=sa.email.apply(lambda email: f"serviceAccount:{email}"),
    )
    iam_bindings.append(ar_binding)

    # Grant Secret Manager access for each secret
    for secret_id, secret in secrets.items():
        secret_binding = gcp.secretmanager.SecretIamMember(
            f"{SERVICE_NAME}-secret-{secret_id}",
            project=PROJECT,
            secret_id=secret.secret_id,
            role="roles/secretmanager.secretAccessor",
            member=sa.email.apply(lambda email: f"serviceAccount:{email}"),
        )
        iam_bindings.append(secret_binding)

    return sa, iam_bindings


def _secret_env(
    name: str, secret_id: str
) -> gcp.cloudrunv2.ServiceTemplateContainerEnvArgs:
    """Define a Cloud Run env var that references a Secret Manager secret."""
    return gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
        name=name,
        value_source=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceArgs(
            secret_key_ref=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceSecretKeyRefArgs(
                secret=secret_id,
                version="latest",
            ),
        ),
    )


def _cloud_run_template_args(
    sa: gcp.serviceaccount.Account,
) -> gcp.cloudrunv2.ServiceTemplateArgs:
    """Build the shared Cloud Run template used by both deployments.

    Both internal-agent-bus-cloudrun and slack-webhook-cloudrun run the same
    container image with the same env vars and secrets. Only the Cloud Run
    service-level settings (ingress, name) differ between them.
    """
    image = f"{REGION}-docker.pkg.dev/{PROJECT}/{SERVICE_NAME}/{SERVICE_NAME}:latest"
    return gcp.cloudrunv2.ServiceTemplateArgs(
        service_account=sa.email,
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
                    limits={
                        "cpu": "1",
                        "memory": "512Mi",
                    },
                ),
                envs=[
                    gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                        name="GCP_PROJECT",
                        value=PROJECT,
                    ),
                    gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                        name="DEVIN_ORG_ID",
                        value=DEVIN_ORG_ID,
                    ),
                    _secret_env("GITHUB_WEBHOOK_SECRET", "github-webhook-secret"),
                    _secret_env("SLACK_SIGNING_SECRET", "slack-signing-secret"),
                    _secret_env(
                        "SUBSCRIPTION_API_BEARER_TOKEN",
                        "subscription-api-bearer-token",
                    ),
                    _secret_env("DEVIN_AI_API_KEY", "devin-ai-api-key"),
                    _secret_env("SLACK_BOT_TOKEN_HITL", "slack-bot-token-hitl"),
                    _secret_env(
                        "ZENDESK_WEBHOOK_SIGNING_SECRET",
                        "zendesk-webhook-signing-secret",
                    ),
                ],
            ),
        ],
    )


def define_cloud_run_services(
    sa: gcp.serviceaccount.Account,
    secrets: dict[str, gcp.secretmanager.Secret],
    api_services: list[gcp.projects.Service],
    iam_bindings: list[pulumi.Resource],
) -> tuple[gcp.cloudrunv2.Service, gcp.cloudrunv2.Service]:
    """Define two Cloud Run v2 deployments of the same container image.

    The container image must be built and pushed separately before first deploy.
    Use the Dockerfile at infra/agent-message-bus/app/Dockerfile.

    Returns:
        A tuple of (internal_service, slack_service) where:
        - internal_service (internal-agent-bus-cloudrun): Lives behind the GCLB
          and Cloud Armor for general webhook/API calls (GitHub, subscriptions).
          Ingress restricted to INTERNAL_LOAD_BALANCER.
        - slack_service (slack-webhook-cloudrun): Public HTTPS ingress for
          Slack interactive components only. Security implemented via
          X-Slack-Signature HMAC validation (Slack best practice).
    """
    depends = api_services + list(secrets.values()) + iam_bindings
    template = _cloud_run_template_args(sa)

    # ---- internal-agent-bus-cloudrun ----
    # Lives behind GCLB + Cloud Armor. Only accepts traffic forwarded by the
    # load balancer. Handles /github/webhook, /subscriptions/*, /health.
    internal_service = gcp.cloudrunv2.Service(
        INTERNAL_SERVICE_NAME,
        name=INTERNAL_SERVICE_NAME,
        project=PROJECT,
        location=REGION,
        description=(
            "Internal agent message bus behind GCLB + Cloud Armor. "
            "Handles GitHub webhooks and Devin subscription API calls."
        ),
        ingress="INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER",
        scaling=gcp.cloudrunv2.ServiceScalingArgs(
            min_instance_count=0,
        ),
        template=template,
        opts=pulumi.ResourceOptions(depends_on=depends),
    )

    # Allow GCLB to invoke Cloud Run. Cloud Armor handles access control at the
    # edge, so the Cloud Run service itself must accept all traffic forwarded by
    # the load balancer. Without this binding, GCLB receives 403 from Cloud Run.
    gcp.cloudrunv2.ServiceIamMember(
        f"{INTERNAL_SERVICE_NAME}-invoker",
        project=PROJECT,
        location=REGION,
        name=internal_service.name,
        role="roles/run.invoker",
        member="allUsers",
        opts=pulumi.ResourceOptions(depends_on=[internal_service]),
    )

    # ---- slack-webhook-cloudrun ----
    # Public HTTPS ingress for Slack interactive components only.
    # Security relies on X-Slack-Signature HMAC validation (Slack best practice).
    # Slack does not publish source IPs, so signature validation is the
    # correct trust boundary.
    slack_service = gcp.cloudrunv2.Service(
        SLACK_SERVICE_NAME,
        name=SLACK_SERVICE_NAME,
        project=PROJECT,
        location=REGION,
        description=(
            "Public-facing Slack webhook receiver. Processes Slack interactive "
            "components only. Security via X-Slack-Signature HMAC validation."
        ),
        ingress="INGRESS_TRAFFIC_ALL",
        scaling=gcp.cloudrunv2.ServiceScalingArgs(
            min_instance_count=0,
        ),
        template=template,
        opts=pulumi.ResourceOptions(depends_on=depends),
    )

    # Allow public invocation of the Slack service. The application validates
    # X-Slack-Signature on every request to /slack/webhook.
    gcp.cloudrunv2.ServiceIamMember(
        f"{SLACK_SERVICE_NAME}-invoker",
        project=PROJECT,
        location=REGION,
        name=slack_service.name,
        role="roles/run.invoker",
        member="allUsers",
        opts=pulumi.ResourceOptions(depends_on=[slack_service]),
    )

    return internal_service, slack_service


# =============================================================================
# ARTIFACT REGISTRY
# =============================================================================


def define_artifact_registry(
    api_services: list[gcp.projects.Service],
) -> gcp.artifactregistry.Repository:
    """Define an Artifact Registry repository for container images."""
    repo = gcp.artifactregistry.Repository(
        f"{SERVICE_NAME}-repo",
        repository_id=SERVICE_NAME,
        project=PROJECT,
        location=REGION,
        format="DOCKER",
        description="Container images for the Agent Message Bus webhook relay service",
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )
    return repo


# =============================================================================
# CLOUD ARMOR SECURITY POLICY
# =============================================================================


def define_cloud_armor_policy(
    api_services: list[gcp.projects.Service],
) -> gcp.compute.SecurityPolicy:
    """Define Cloud Armor security policy with per-path IP allowlisting.

    This policy is attached to the GCLB backend that fronts
    internal-agent-bus-cloudrun. Slack traffic does not flow through the
    GCLB — it goes directly to slack-webhook-cloudrun.

    Rules (evaluated in priority order, lowest number = highest priority):
    1. /github/webhook  -> Allow only GitHub webhook IPs
    2. /zendesk/webhook -> Allow only Zendesk IPs (216.198.0.0/18)
    3. /subscriptions/* -> Allow only Devin static IPs
    4. /health          -> Allow all (health check endpoint)
    5. Default          -> Deny all
    """
    # Cloud Armor CEL has a max of 5 expressions per rule.
    # We split IP allowlists into chunks of 4 so each rule has
    # at most 1 (path match) + 4 (IP checks) = 5 expressions.
    max_ips_per_rule = 4

    def _chunk_list(lst: list[str], size: int) -> list[list[str]]:
        return [lst[i : i + size] for i in range(0, len(lst), size)]

    # Build rules for GitHub webhook path (split GitHub CIDRs into chunks)
    github_rules: list[gcp.compute.SecurityPolicyRuleArgs] = []
    for idx, cidr_chunk in enumerate(_chunk_list(GITHUB_HOOK_CIDRS, max_ips_per_rule)):
        ip_expr = " || ".join(f"inIpRange(origin.ip, '{cidr}')" for cidr in cidr_chunk)
        github_rules.append(
            gcp.compute.SecurityPolicyRuleArgs(
                action="allow",
                priority=100 + idx,
                description=f"Allow GitHub webhook IPs on /github/webhook (part {idx + 1})",
                match=gcp.compute.SecurityPolicyRuleMatchArgs(
                    expr=gcp.compute.SecurityPolicyRuleMatchExprArgs(
                        expression=(
                            f"request.path.matches('^/github/webhook$') && ({ip_expr})"
                        ),
                    ),
                ),
            ),
        )

    # Build rules for Zendesk webhook path (split Zendesk CIDRs into chunks)
    zendesk_rules: list[gcp.compute.SecurityPolicyRuleArgs] = []
    for idx, cidr_chunk in enumerate(
        _chunk_list(ZENDESK_WEBHOOK_CIDRS, max_ips_per_rule)
    ):
        ip_expr = " || ".join(f"inIpRange(origin.ip, '{cidr}')" for cidr in cidr_chunk)
        zendesk_rules.append(
            gcp.compute.SecurityPolicyRuleArgs(
                action="allow",
                priority=150 + idx,
                description=f"Allow Zendesk webhook IPs on /zendesk/webhook (part {idx + 1})",
                match=gcp.compute.SecurityPolicyRuleMatchArgs(
                    expr=gcp.compute.SecurityPolicyRuleMatchExprArgs(
                        expression=(
                            f"request.path.matches('^/zendesk/webhook$') && ({ip_expr})"
                        ),
                    ),
                ),
            ),
        )

    # Build rules for subscriptions path (split Devin IPs into chunks)
    devin_rules: list[gcp.compute.SecurityPolicyRuleArgs] = []
    for idx, ip_chunk in enumerate(
        _chunk_list([f"{ip}/32" for ip in DEVIN_IPS], max_ips_per_rule)
    ):
        ip_expr = " || ".join(f"inIpRange(origin.ip, '{cidr}')" for cidr in ip_chunk)
        devin_rules.append(
            gcp.compute.SecurityPolicyRuleArgs(
                action="allow",
                priority=200 + idx,
                description=f"Allow Devin IPs on /subscriptions/* (part {idx + 1})",
                match=gcp.compute.SecurityPolicyRuleMatchArgs(
                    expr=gcp.compute.SecurityPolicyRuleMatchExprArgs(
                        expression=(
                            f"request.path.matches('^/subscriptions') && ({ip_expr})"
                        ),
                    ),
                ),
            ),
        )

    policy = gcp.compute.SecurityPolicy(
        f"{SERVICE_NAME}-armor",
        name=f"{SERVICE_NAME}-armor",
        project=PROJECT,
        description="Per-path IP allowlisting for Agent Message Bus service",
        rules=[
            *github_rules,
            *zendesk_rules,
            *devin_rules,
            # Health check — allow all
            gcp.compute.SecurityPolicyRuleArgs(
                action="allow",
                priority=300,
                description="Allow health check endpoint",
                match=gcp.compute.SecurityPolicyRuleMatchArgs(
                    expr=gcp.compute.SecurityPolicyRuleMatchExprArgs(
                        expression="request.path.matches('^/health$')",
                    ),
                ),
            ),
            # Default deny
            gcp.compute.SecurityPolicyRuleArgs(
                action="deny(403)",
                priority=2147483647,
                description="Default deny all other traffic",
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
    return policy


# =============================================================================
# LOAD BALANCER (GCLB)
# =============================================================================


def define_load_balancer(
    internal_service: gcp.cloudrunv2.Service,
    armor_policy: gcp.compute.SecurityPolicy,
    api_services: list[gcp.projects.Service],
) -> dict[str, pulumi.Output]:
    """Define a Global HTTP(S) Load Balancer in front of internal-agent-bus-cloudrun.

    Components:
    - Serverless NEG pointing to internal-agent-bus-cloudrun
    - Backend service with Cloud Armor policy
    - URL map (simple default routing)
    - HTTP target proxy + global forwarding rule
    """
    # Serverless Network Endpoint Group
    neg = gcp.compute.RegionNetworkEndpointGroup(
        f"{SERVICE_NAME}-lb-neg",
        project=PROJECT,
        region=REGION,
        network_endpoint_type="SERVERLESS",
        cloud_run=gcp.compute.RegionNetworkEndpointGroupCloudRunArgs(
            service=internal_service.name,
        ),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    # Backend service
    backend = gcp.compute.BackendService(
        f"{SERVICE_NAME}-lb-backend",
        project=PROJECT,
        protocol="HTTPS",
        port_name="http",
        security_policy=armor_policy.self_link,
        backends=[
            gcp.compute.BackendServiceBackendArgs(
                group=neg.id,
            ),
        ],
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    # URL map (simple default routing — all paths go to one backend)
    url_map = gcp.compute.URLMap(
        f"{SERVICE_NAME}-lb-urlmap",
        project=PROJECT,
        default_service=backend.self_link,
    )

    # For initial deployment, use HTTP only. Managed SSL requires a domain.
    # Once a domain is configured, switch to HTTPS with managed cert.
    http_proxy = gcp.compute.TargetHttpProxy(
        f"{SERVICE_NAME}-lb-http-proxy",
        project=PROJECT,
        url_map=url_map.self_link,
    )

    # Global forwarding rule (HTTP)
    forwarding_rule = gcp.compute.GlobalForwardingRule(
        f"{SERVICE_NAME}-lb-forwarding-rule",
        project=PROJECT,
        target=http_proxy.self_link,
        port_range="80",
        ip_protocol="TCP",
    )

    return {
        "lb_ip": forwarding_rule.ip_address,
        "backend_service": backend.self_link,
    }


# =============================================================================
# FIRESTORE
# =============================================================================


def define_firestore(
    api_services: list[gcp.projects.Service],
) -> tuple[gcp.firestore.Database, gcp.firestore.Field]:
    """Define Firestore database and TTL policy.

    Creates the default Firestore database in Native mode and configures
    a TTL policy on the expires_at field for automatic subscription expiry.
    """
    database = gcp.firestore.Database(
        f"{SERVICE_NAME}-firestore-db",
        project=PROJECT,
        name=FIRESTORE_DATABASE,
        location_id=REGION,
        type="FIRESTORE_NATIVE",
        concurrency_mode="OPTIMISTIC",
        deletion_policy="DELETE",
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    ttl_field = gcp.firestore.Field(
        f"{SERVICE_NAME}-ttl-policy",
        project=PROJECT,
        database=FIRESTORE_DATABASE,
        collection=FIRESTORE_COLLECTION,
        field="expires_at",
        ttl_config=gcp.firestore.FieldTtlConfigArgs(),
        opts=pulumi.ResourceOptions(depends_on=[database]),
    )
    return database, ttl_field


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Define and deploy all infrastructure resources."""
    # Enable APIs first
    api_services = define_apis()

    # Secrets
    secrets = define_secrets(api_services)

    # Service account with access to Firestore + secrets
    sa, iam_bindings = define_service_account(api_services, secrets)

    # Artifact Registry for container images
    ar_repo = define_artifact_registry(api_services)

    # Cloud Run services (two deployments of the same image)
    internal_service, slack_service = define_cloud_run_services(
        sa, secrets, api_services, iam_bindings
    )

    # Cloud Armor policy (attached to GCLB, protects internal service only)
    armor_policy = define_cloud_armor_policy(api_services)

    # Load Balancer (fronts internal-agent-bus-cloudrun only)
    lb_outputs = define_load_balancer(internal_service, armor_policy, api_services)

    # Firestore database and TTL policy
    firestore_db, ttl_field = define_firestore(api_services)

    # Export outputs
    pulumi.export("project", PROJECT)
    pulumi.export("region", REGION)
    pulumi.export("internal_service_name", internal_service.name)
    pulumi.export("internal_service_url", internal_service.uri)
    pulumi.export("slack_service_name", slack_service.name)
    pulumi.export("slack_service_url", slack_service.uri)
    pulumi.export("lb_ip_address", lb_outputs["lb_ip"])
    pulumi.export(
        "artifact_registry",
        ar_repo.name.apply(lambda name: f"{REGION}-docker.pkg.dev/{PROJECT}/{name}"),
    )
    pulumi.export("cloud_armor_policy", armor_policy.name)
    pulumi.export("firestore_database", firestore_db.name)
    pulumi.export("firestore_ttl_field", ttl_field.name)

    # Export secret names for reference
    for secret_id, secret in secrets.items():
        pulumi.export(f"secret_{secret_id.replace('-', '_')}", secret.name)


main()
