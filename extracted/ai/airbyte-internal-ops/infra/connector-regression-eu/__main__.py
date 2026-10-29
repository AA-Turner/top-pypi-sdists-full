"""
Pulumi Infrastructure as Code for EU connector regression testing on Cloud Batch.

This module manages the EU (GDPR data-residency) infrastructure used to run
connector regression tests on Google Cloud Batch.

Tracking issue: https://github.com/airbytehq/airbyte-ops-mcp/issues/1480

SECURITY / RESIDENCY MODEL:
---------------------------
- Every resource is regional and EU-scoped: a europe-west9 subnet, a
  EUROPE-WEST9 output bucket, and a europe-west9 log bucket.
- Batch VMs run with no external IP address on a dedicated custom-mode VPC;
  egress flows through Cloud NAT. There is no ingress and no firewall rules.
- Regression test outputs land in a bucket that auto-deletes objects after
  `RETENTION_DAYS` and enforces public access prevention. Soft delete is off,
  so a deleted report cannot outlive `RETENTION_DAYS`; raise that setting to
  retain outputs and logs longer, and never re-enable soft delete.
- Batch logs and this stack's Cloud NAT error logs (which carry source and
  destination IPs) are routed to a dedicated regional log bucket that keeps
  them for the same 2 days, and excluded from the global `_Default` bucket.
- Humans in `dev-connectors-org@airbyte.io` have read-only access to EU output
  objects through Pulumi and the EU log bucket's `_AllLogs` view through a
  one-time owner grant in BOOTSTRAP.md. These group grants support the GitHub
  step-summary links; no individual human grants are made.
- Project-level IAM grants are one-time owner grants by design, so the apply
  does not depend on `roles/resourcemanager.projectIamAdmin`. The submitter's
  `roles/iam.serviceAccountUser` grant on the job service account and `_AllLogs`
  view IAM grant are also owner-managed because the deployer cannot set
  service-account IAM or `logging.views.setIamPolicy`. The job service
  account's project roles, the job submitter's grants, and operator access to
  `_AllLogs` are one-time owner grants listed in BOOTSTRAP.md.

COMPONENTS:
-----------
- API enablements: batch, compute, logging, secretmanager
- Network: custom-mode VPC, europe-west9 subnet (10.90.0.0/24, Private
  Google Access), Cloud Router + Cloud NAT
- connector-regression-eu-job service account (Batch task identity)
- internal-airbyte-ai-infra-connector-regression-eu output bucket, with
  storage.objectAdmin for the job SA on this bucket only
- connector-regression-eu log bucket + sink + _Default exclusion
"""

import pulumi
import pulumi_gcp as gcp

# =============================================================================
# CONFIGURATION
# =============================================================================

gcp_config = pulumi.Config("gcp")

PROJECT = gcp_config.require("project")
REGION = gcp_config.get("region") or "europe-west9"

PREFIX = "connector-regression-eu"
SUBNET_CIDR = "10.90.0.0/24"
OUTPUT_BUCKET_NAME = "internal-airbyte-ai-infra-connector-regression-eu"
# It reads EU reports and logs through the GitHub step-summary links.
OPERATOR_GROUP = "dev-connectors-org@airbyte.io"
# Output objects and log entries are kept for the same number of days.
RETENTION_DAYS = 2
BATCH_LOG_FILTER = 'logName:("/logs/batch_task_logs" OR "/logs/batch_agent_logs")'
NAT_LOG_FILTER = (
    'resource.type="nat_gateway"'
    f' AND resource.labels.region="{REGION}"'
    f' AND resource.labels.gateway_name="{PREFIX}"'
)
# Logging query language binds OR tighter than AND, so keep the parentheses.
EU_LOG_FILTER = f"({BATCH_LOG_FILTER}) OR ({NAT_LOG_FILTER})"

# =============================================================================
# ENABLE REQUIRED APIs
# =============================================================================


def define_apis() -> list[gcp.projects.Service]:
    """Define required GCP API enablements for the project."""
    api_ids = [
        "batch.googleapis.com",
        "compute.googleapis.com",
        "logging.googleapis.com",
        "secretmanager.googleapis.com",
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
# NETWORK
# =============================================================================


def define_network(
    api_services: list[gcp.projects.Service],
) -> tuple[gcp.compute.Network, gcp.compute.Subnetwork]:
    """Define the VPC, regional subnet, and Cloud NAT for Batch VMs.

    The VPC is custom-mode with no firewall rules: Batch VMs have no external
    IP and accept no ingress. Private Google Access plus Cloud NAT covers the
    Google API and image-pull egress the jobs need. NAT error logs name source
    and destination IPs, so `define_logging` routes them to the EU log bucket.
    """
    network = gcp.compute.Network(
        f"{PREFIX}-network",
        name=PREFIX,
        project=PROJECT,
        auto_create_subnetworks=False,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    subnet = gcp.compute.Subnetwork(
        f"{PREFIX}-subnet",
        name=PREFIX,
        project=PROJECT,
        region=REGION,
        network=network.id,
        ip_cidr_range=SUBNET_CIDR,
        private_ip_google_access=True,
        opts=pulumi.ResourceOptions(depends_on=[network]),
    )

    router = gcp.compute.Router(
        f"{PREFIX}-router",
        name=PREFIX,
        project=PROJECT,
        region=REGION,
        network=network.id,
        opts=pulumi.ResourceOptions(depends_on=[network]),
    )

    gcp.compute.RouterNat(
        f"{PREFIX}-nat",
        name=PREFIX,
        project=PROJECT,
        region=REGION,
        router=router.name,
        nat_ip_allocate_option="AUTO_ONLY",
        source_subnetwork_ip_ranges_to_nat="ALL_SUBNETWORKS_ALL_IP_RANGES",
        log_config=gcp.compute.RouterNatLogConfigArgs(
            enable=True,
            filter="ERRORS_ONLY",
        ),
        opts=pulumi.ResourceOptions(depends_on=[router, subnet]),
    )

    return network, subnet


# =============================================================================
# JOB SERVICE ACCOUNT
# =============================================================================


def define_job_service_account(
    api_services: list[gcp.projects.Service],
) -> gcp.serviceaccount.Account:
    """Define the service account Batch tasks run as.

    Its project roles (`roles/batch.agentReporter`, `roles/logging.logWriter`)
    are owner grants in BOOTSTRAP.md, run once after this account exists.
    """
    return gcp.serviceaccount.Account(
        f"{PREFIX}-job-sa",
        account_id=f"{PREFIX}-job",
        display_name="Connector Regression EU Batch job identity",
        project=PROJECT,
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )


# =============================================================================
# CLOUD API CREDENTIALS SECRET
# =============================================================================


def define_cloud_api_secret(
    sa: gcp.serviceaccount.Account,
    api_services: list[gcp.projects.Service],
) -> gcp.secretmanager.Secret:
    """Define the regional Cloud API credentials secret and its job-SA grant.

    The credential owner adds a version after the secret is created. Pulumi
    creates no SecretVersion. The secret is protected because its versions are
    owner-managed outside Pulumi.
    """
    secret = gcp.secretmanager.Secret(
        f"{PREFIX}-cloud-api-secret",
        secret_id="connector-regression-eu-cloud-api",
        project=PROJECT,
        replication=gcp.secretmanager.SecretReplicationArgs(
            user_managed=gcp.secretmanager.SecretReplicationUserManagedArgs(
                replicas=[
                    gcp.secretmanager.SecretReplicationUserManagedReplicaArgs(
                        location=REGION,
                    )
                ],
            ),
        ),
        opts=pulumi.ResourceOptions(
            depends_on=api_services,
            protect=True,
        ),
    )

    gcp.secretmanager.SecretIamMember(
        f"{PREFIX}-cloud-api-secret-access",
        project=PROJECT,
        secret_id=secret.secret_id,
        role="roles/secretmanager.secretAccessor",
        member=sa.email.apply(lambda email: f"serviceAccount:{email}"),
    )

    return secret


# =============================================================================
# OUTPUT BUCKET
# =============================================================================


def define_output_bucket(
    sa: gcp.serviceaccount.Account,
    api_services: list[gcp.projects.Service],
) -> gcp.storage.Bucket:
    """Define the regression-test output bucket.

    Regional (EUROPE-WEST9), uniform bucket-level access, public access
    prevention enforced, and a `RETENTION_DAYS` lifecycle delete so test
    artifacts do not accumulate. Soft delete is off, so a deleted report
    cannot outlive `RETENTION_DAYS`. Raise `RETENTION_DAYS` to retain outputs
    and EU logs longer; never re-enable soft delete.
    """
    bucket = gcp.storage.Bucket(
        f"{PREFIX}-outputs",
        name=OUTPUT_BUCKET_NAME,
        project=PROJECT,
        location="EUROPE-WEST9",
        uniform_bucket_level_access=True,
        public_access_prevention="enforced",
        soft_delete_policy=gcp.storage.BucketSoftDeletePolicyArgs(
            retention_duration_seconds=0
        ),
        lifecycle_rules=[
            gcp.storage.BucketLifecycleRuleArgs(
                action=gcp.storage.BucketLifecycleRuleActionArgs(type="Delete"),
                condition=gcp.storage.BucketLifecycleRuleConditionArgs(
                    age=RETENTION_DAYS
                ),
            ),
        ],
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    gcp.storage.BucketIAMMember(
        f"{PREFIX}-job-object-admin",
        bucket=bucket.name,
        role="roles/storage.objectAdmin",
        member=sa.email.apply(lambda email: f"serviceAccount:{email}"),
    )

    gcp.storage.BucketIAMMember(
        f"{PREFIX}-operator-object-viewer",
        bucket=bucket.name,
        role="roles/storage.objectViewer",
        member=f"group:{OPERATOR_GROUP}",
    )

    return bucket


# =============================================================================
# LOGGING
# =============================================================================


def define_logging(
    api_services: list[gcp.projects.Service],
) -> gcp.logging.ProjectBucketConfig:
    """Route Batch logs and Cloud NAT error logs to a regional log bucket.

    A log bucket in europe-west9 keeps Batch task and agent logs, and this
    stack's NAT error logs, in-region for `RETENTION_DAYS`, the same as the
    output bucket. A project sink routes them there and a matching exclusion
    keeps them out of the global `_Default` bucket. Sinks to same-project log
    buckets need no unique writer identity.
    """
    log_bucket = gcp.logging.ProjectBucketConfig(
        f"{PREFIX}-log-bucket",
        project=PROJECT,
        location=REGION,
        bucket_id=PREFIX,
        retention_days=RETENTION_DAYS,
        description=(
            "Cloud Batch and Cloud NAT logs for EU connector regression tests."
        ),
        opts=pulumi.ResourceOptions(depends_on=api_services),
    )

    gcp.logging.ProjectSink(
        f"{PREFIX}-logs-sink",
        name=PREFIX,
        project=PROJECT,
        destination=pulumi.Output.all(
            project=PROJECT, location=REGION, bucket_id=log_bucket.bucket_id
        ).apply(
            lambda args: (
                f"logging.googleapis.com/projects/{args['project']}"
                f"/locations/{args['location']}/buckets/{args['bucket_id']}"
            )
        ),
        filter=EU_LOG_FILTER,
        opts=pulumi.ResourceOptions(depends_on=[log_bucket]),
    )

    gcp.logging.ProjectExclusion(
        f"{PREFIX}-default-exclusion",
        name=PREFIX,
        project=PROJECT,
        filter=EU_LOG_FILTER,
        description=(
            "Keep EU regression Batch logs and Cloud NAT logs out of the "
            "_Default bucket."
        ),
        opts=pulumi.ResourceOptions(depends_on=[log_bucket]),
    )

    return log_bucket


# =============================================================================
# MAIN
# =============================================================================


api_services = define_apis()
network, subnet = define_network(api_services)
job_sa = define_job_service_account(api_services)
cloud_api_secret = define_cloud_api_secret(job_sa, api_services)
output_bucket = define_output_bucket(job_sa, api_services)
log_bucket = define_logging(api_services)

pulumi.export("region", REGION)
pulumi.export("network_self_link", network.self_link)
pulumi.export("subnet_self_link", subnet.self_link)
pulumi.export("job_service_account_email", job_sa.email)
pulumi.export("cloud_api_secret_id", cloud_api_secret.secret_id)
pulumi.export("output_bucket_name", output_bucket.name)
pulumi.export("log_bucket_id", log_bucket.bucket_id)
