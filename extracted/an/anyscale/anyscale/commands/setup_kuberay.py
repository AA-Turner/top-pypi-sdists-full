"""Set up an Anyscale KubeRay (connector) cloud on an existing Kubernetes cluster.

The KubeRay lane is opinionated: setup discovers the cluster's token issuer, infers
the hosting provider from it, creates the cloud's object-storage bucket together
with the IAM identity that lets the cluster's pods use it, registers the cloud,
installs the connector chart, and waits until Anyscale reports the connector
healthy. Trust still flows outward -- Anyscale verifies the connector's projected
service-account token against the issuer registered here -- so no dataplane
credential is ever handed to Anyscale.
"""

from enum import Enum
import functools
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Tuple

import click
import requests
import yaml

from anyscale._private.anyscale_client.common import (
    DEFAULT_PYTHON_VERSION,
    DEFAULT_RAY_VERSION,
)
from anyscale.cli_logger import BlockLogger, CloudSetupLogger
from anyscale.client.openapi_client.models import (
    CloudDeployment,
    CloudProviders,
    ComputeStack,
    ConnectorConfig,
    ObjectStorage,
)
from anyscale.cloud_utils import get_cloud_id_and_name
from anyscale.controllers.cloud_controller import CloudController
from anyscale.controllers.kubernetes_verifier import KubectlOperations
from anyscale.shared_anyscale_utils.conf import (
    ANYSCALE_CORS_EXPOSE_HEADERS,
    ANYSCALE_CORS_ORIGIN,
    ANYSCALE_HOST,
)
from anyscale.util import get_endpoint
from anyscale.version import __version__


HELM_REPO_NAME = "anyscale"
HELM_REPO_URL = "https://anyscale.github.io/helm-charts"
CONNECTOR_CHART_REF = "anyscale/anyscale-connector"
CONNECTOR_RELEASE_NAME = "anyscale-connector"
# The chart's default service account (values.yaml connector.serviceAccount.name).
# The name registered with Anyscale and the name the chart deploys must agree --
# the token subject is verified against the registration -- so both sides read one
# constant and nothing lets them diverge.
CONNECTOR_SERVICE_ACCOUNT = "anyscale-connector"
IRSA_ROLE_ANNOTATION = "eks.amazonaws.com/role-arn"
# values.yaml paths of the chart's three ServiceAccounts (connector, Cluster
# Telemetry Gateway, Observability API); each takes its own annotations map.
CHART_SERVICE_ACCOUNT_VALUES = (
    "connector.serviceAccount",
    "clusterTelemetry.serviceAccount",
    "observabilityApi.serviceAccount",
)
# `helm repo update <name>` and the chart's subchart conditions need 3.7 or newer.
HELM_MIN_VERSION = (3, 7)
_HELM_VERSION_PATTERN = re.compile(r"^v?(\d+)\.(\d+)")


class KuberayOperatorMode(str, Enum):
    """Where the KubeRay operator comes from (--kuberay-operator)."""

    AUTO = "auto"
    INSTALL = "install"
    SKIP = "skip"


# The operator's pod label. The upstream chart puts it on the pod template only,
# so detection lists pods rather than Deployments.
KUBERAY_OPERATOR_POD_SELECTOR = "app.kubernetes.io/component=kuberay-operator"
# Condition of the kuberay-operator subchart bundled with the connector chart.
KUBERAY_OPERATOR_HELM_SET = "kuberay-operator.enabled=true"
RAYJOB_CRD = "rayjobs.ray.io"
# Service labels of the mainstream dcgm-exporter installs: the helm chart and NVIDIA's
# raw manifest, then the GPU Operator.
DCGM_SERVICE_SELECTORS = (
    "app.kubernetes.io/name=dcgm-exporter",
    "app=nvidia-dcgm-exporter",
)
# What the gateway scrapes when nothing names the Service (the GPU Operator's name).
DCGM_DEFAULT_SERVICE_NAME = "nvidia-dcgm-exporter"
# Condition of the dcgm-exporter subchart bundled with the connector chart.
DCGM_EXPORTER_HELM_SET = "dcgm-exporter.enabled=true"
GPU_ALLOCATABLE_KEY = "nvidia.com/gpu"
# The node labels the bundled exporter's affinity keys on (values.yaml dcgm-exporter.affinity).
GPU_NODE_LABELS = (
    "nvidia.com/gpu.present",
    "cloud.google.com/gke-accelerator",
    "k8s.amazonaws.com/accelerator",
    "karpenter.k8s.aws/instance-gpu-manufacturer",
)
# The chart's Ingress for the Observability API; KCP registers the console's DNS from its address.
OBSERVABILITY_INGRESS_NAME = "anyscale-connector-observability-api"
# Condition of the traefik ingress controller bundled with the connector chart.
BUNDLED_INGRESS_HELM_SET = "traefik.enabled=true"
# The chart's fullnameOverride for its traefik: the IngressClass an earlier setup left behind.
BUNDLED_INGRESS_CLASS_NAME = "anyscale-connector-traefik"
# The k8s lane's AWS annotations for a controller's LoadBalancer Service.
AWS_LB_SERVICE_ANNOTATIONS = (
    ("service.beta.kubernetes.io/aws-load-balancer-scheme", "internet-facing"),
    ("service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled", "true"),
    ("service.beta.kubernetes.io/aws-load-balancer-type", "nlb"),
)
INGRESS_ADDRESS_TIMEOUT_SECONDS = 120
INGRESS_ADDRESS_POLL_SECONDS = 10
# The sample RayJob: a few minutes of real CPU load so the console has something to show.
SAMPLE_RAYJOB_NAME = "anyscale-smoke"
SAMPLE_RAYJOB_FILE = "anyscale-smoke-rayjob.yaml"
# A cold node pulls the Ray image first, which takes minutes.
RAYJOB_RUNNING_TIMEOUT_SECONDS = 600
RAYJOB_POLL_SECONDS = 10
TRACKED_JOB_TIMEOUT_SECONDS = 120
TRACKED_JOB_POLL_SECONDS = 5
TRACKED_JOB_PAGE_SIZE = 100
TRACKED_JOB_MAX_PAGES = 4
_SAMPLE_RAYJOB_ENTRYPOINT = "python -c \"\nimport ray, socket, time, math\nray.init()\n\nprint('cluster resources:', ray.cluster_resources())\n\n@ray.remote\nclass Burner:\n    def __init__(self, idx):\n        self.idx = idx\n        self.host = socket.gethostname()\n    def burn(self, seconds):\n        # Real CPU work, so the metrics panels show something other than idle.\n        end = time.time() + seconds\n        n = 0\n        while time.time() < end:\n            for i in range(1, 5000):\n                math.sqrt(i) * math.sin(i)\n            n += 1\n        return (self.idx, self.host, n)\n\nactors = [Burner.remote(i) for i in range(4)]\nprint('actors placed on:', ray.get([a.burn.remote(1) for a in actors]))\n\nfor round_num in range(10):\n    results = ray.get([a.burn.remote(30) for a in actors])\n    print('round', round_num, 'iterations per actor:', [r[2] for r in results], flush=True)\n\nprint('smoke test done')\n\"\n"
# EKS issuers encode the hosting region; GKE issuers identify the provider only.
_EKS_ISSUER_PATTERN = re.compile(
    r"^https://oidc\.eks\.(?P<region>[a-z0-9-]+)\.amazonaws\.com/id/\S+$"
)
_GKE_ISSUER_PREFIX = "https://container.googleapis.com/"
_STACK_NAME_PREFIX = "anyscale-kuberay-"
_INFRA_TAG_KEY = "anyscale-kuberay-cloud-name"
_INFRA_ISSUER_TAG_KEY = "anyscale-kuberay-issuer"
# Kubernetes namespaces are RFC 1123 labels. Enforced up front because the
# namespace lands in the IAM trust policy, where StringLike would read `*`/`?`
# as wildcards long before helm rejects the bogus namespace.
_NAMESPACE_PATTERN = re.compile(r"^[a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?$")
# The obs-api pod turns Ready only after the control plane delivers the telemetry
# ConfigMap over the freshly established ConnectorSync stream, so helm's own wait
# doubles as an end-to-end connectivity check. Budget for that async delivery.
HELM_WAIT_TIMEOUT = "10m"
# Backstop above helm's own --timeout: that flag bounds the K8s wait, not
# registry/chart fetches, and a chart with a pre-install hook spends up to 3 min
# in the hook before that wait begins. Hook + wait + slack.
HELM_INSTALL_TIMEOUT_SECONDS = 180 + 600 + 240
CONNECTOR_HEALTHY_TIMEOUT_SECONDS = 300
CONNECTOR_HEALTHY_POLL_SECONDS = 10


class IssuerInfo(NamedTuple):
    issuer: str
    jwks_uri: str


class ProviderInfo(NamedTuple):
    provider: str
    region: str


class AwsInfra(NamedTuple):
    bucket_name: str
    role_arn: str
    stack_name: str
    region: str


class AwsIdentity(NamedTuple):
    account_id: str
    arn: str


class ScanPlan(NamedTuple):
    """One cluster-scan decision: a confirm-block line plus the helm argv it adds."""

    label: str
    summary: str
    helm_sets: Tuple[str, ...]
    # Whether the install leaves an Ingress whose address KCP must learn.
    expect_ingress_address: bool = False

    def line(self) -> str:
        return f"  {self.label + ':':<20}{self.summary}"


class DcgmService(NamedTuple):
    namespace: str
    name: str


class IngressClassInfo(NamedTuple):
    name: str
    controller: str


class _BlockScalarDumper(yaml.SafeDumper):
    """Multi-line strings as `|` blocks, so the written RayJob's entrypoint reads as a script."""


def _represent_str(dumper: yaml.SafeDumper, data: str) -> yaml.ScalarNode:
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_BlockScalarDumper.add_representer(str, _represent_str)


def _run(
    argv: List[str], timeout_seconds: int = 60, check: bool = False
) -> subprocess.CompletedProcess:
    # kubectl and helm both wait forever on a wedged endpoint by default; every
    # invocation gets a hard backstop.
    try:
        return subprocess.run(
            argv,
            capture_output=True,
            text=True,
            check=check,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        raise click.ClickException(f"'{' '.join(argv[:2])}' timed out after {timeout_seconds}s")


def _cloud_delete_command(name: str) -> str:
    return f"anyscale cloud delete --name '{name}' --yes"


def _helm_uninstall_command(namespace: str, cluster_context: Optional[str]) -> str:
    ctx = f" --kube-context {cluster_context}" if cluster_context else ""
    return f"helm{ctx} -n {namespace} uninstall {CONNECTOR_RELEASE_NAME}"


def _stack_delete_command(infra: AwsInfra) -> str:
    return (
        f"aws cloudformation delete-stack --region {infra.region} --stack-name {infra.stack_name}"
    )


class KubeRayCloudSetupCommand:
    """Command to set up a KubeRay (connector) cloud."""

    def __init__(self, logger: Optional[BlockLogger] = None, debug: bool = False):
        self.log = logger or BlockLogger()
        self.debug = debug or os.environ.get("ANYSCALE_DEBUG") == "1"
        # The controller's closing output (a "run this helm command" block)
        # doesn't apply here -- this command runs the install itself -- so the
        # controller gets a muted logger. Failures still surface as exceptions.
        try:
            self.cloud_controller = CloudController(log=CloudSetupLogger(log_output=False))
        except click.ClickException as e:
            # The credential loader says where to make an API key, not that this command
            # needs a login first.
            first = e.message.split(". ")[0].rstrip(".")
            raise click.ClickException(
                f"Not logged in to Anyscale ({ANYSCALE_HOST}): {first}. Run `anyscale login`, "
                "then re-run setup."
            )
        # Scan cache: nodes are listed once per run.
        self._nodes: Optional[List[Dict[str, Any]]] = None

    def run(  # noqa: PLR0913
        self,
        name: str,
        cluster_context: Optional[str],
        namespace: str,
        yes: bool,
        connector_chart: Optional[str] = None,
        connector_values: Optional[str] = None,
        auto_add_user: bool = True,
        kuberay_operator: KuberayOperatorMode = KuberayOperatorMode.AUTO,
        dcgm_namespace: Optional[str] = None,
        ingress_class: Optional[str] = None,
        test_job: Optional[bool] = None,
        control_plane_domain: Optional[str] = None,
    ) -> None:
        """Create a KubeRay cloud end to end: infra, registration, connector.

        Opinionated on scope too: workloads run in the connector's namespace.
        A cloud that needs more namespaces registers through `cloud register`,
        where allowed_namespaces is an explicit input.
        """
        if not _NAMESPACE_PATTERN.match(namespace):
            raise click.ClickException(
                f"'{namespace}' is not a valid Kubernetes namespace (lowercase "
                "RFC 1123 label, at most 63 characters)."
            )
        if dcgm_namespace is not None and not _NAMESPACE_PATTERN.match(dcgm_namespace):
            raise click.ClickException(
                f"--dcgm-namespace '{dcgm_namespace}' is not a valid Kubernetes namespace "
                "(lowercase RFC 1123 label, at most 63 characters)."
            )
        if ingress_class is not None and not ingress_class.strip():
            raise click.ClickException("--ingress-class must name an IngressClass.")
        self.log.open_block(
            "Setup",
            f"Setting up KubeRay cloud '{name}'",
        )
        try:
            self._check_required_tools()
            self._log_login()

            cluster_context = cluster_context or self._choose_cluster_context(yes)
            self._check_no_existing_release(namespace, cluster_context)
            issuer = self._discover_issuer(cluster_context)
            provider_info = self._infer_provider(issuer)
            stack_name = self._stack_name(name)
            aws_identity = self._resolve_aws_identity(provider_info.region)
            plans = [
                self._plan_control_plane(control_plane_domain),
                self._plan_kuberay_operator(
                    cluster_context=cluster_context, mode=kuberay_operator, yes=yes
                ),
                self._plan_gpu_metrics(
                    cluster_context=cluster_context, dcgm_namespace=dcgm_namespace, yes=yes
                ),
                self._plan_ingress(
                    cluster_context=cluster_context,
                    ingress_class=ingress_class,
                    provider=provider_info.provider,
                    yes=yes,
                ),
            ]
            scan_sets: Tuple[str, ...] = tuple(arg for plan in plans for arg in plan.helm_sets)

            if not yes:
                self.log.info(f"  Cluster context:    {cluster_context}")
                self.log.info(
                    f"  Provider:           {provider_info.provider.upper()} "
                    f"({provider_info.region}), inferred from the token issuer"
                )
                self.log.info(f"  Namespace:          {namespace}")
                self.log.info(f"  Token issuer:       {issuer}")
                self.log.info(
                    f"  Storage & IAM:      CloudFormation stack '{stack_name}' "
                    f"(S3 bucket + IAM role, created in AWS account {aws_identity.account_id})"
                )
                for plan in plans:
                    self.log.info(plan.line())
                click.confirm("Continue?", abort=True)
            else:
                # --yes skips the summary, but what the scan decided must still show.
                for plan in plans:
                    self.log.info(plan.line(), block_label="Setup")

            infra: Optional[AwsInfra] = None
            registered = False
            install_started = False
            try:
                # Probe the chart source before creating anything: with the chart
                # not yet published, this is the leg most likely to fail.
                chart_reference = self._ensure_chart(connector_chart)
                issuer_info = IssuerInfo(issuer=issuer, jwks_uri=self._resolve_public_jwks(issuer))

                infra = self._setup_aws_infrastructure(
                    stack_name=stack_name,
                    cloud_name=name,
                    issuer=issuer,
                    region=provider_info.region,
                    namespace=namespace,
                    account_id=aws_identity.account_id,
                )

                self._register_cloud(
                    name=name,
                    namespace=namespace,
                    infra=infra,
                    issuer_info=issuer_info,
                    auto_add_user=auto_add_user,
                )
                registered = True
                cloud_id, cloud_resource_id = self._resolve_cloud_ids(name)

                install_started = True
                self._install_connector(
                    chart_reference=chart_reference,
                    namespace=namespace,
                    cloud_id=cloud_id,
                    cloud_resource_id=cloud_resource_id,
                    cluster_context=cluster_context,
                    connector_values=connector_values,
                    role_arn=infra.role_arn,
                    extra_set_args=scan_sets,
                )
            # KeyboardInterrupt included: Ctrl+C during the 10-minute helm wait
            # must still tell the user what already exists.
            except (Exception, KeyboardInterrupt):
                self._log_cleanup_instructions(
                    name=name,
                    cloud_registered=registered,
                    namespace=namespace,
                    cluster_context=cluster_context,
                    install_started=install_started,
                    infra=infra,
                )
                raise
            assert infra is not None  # Set before registration.

            # Past this point nothing is half-created: a poll timeout's own
            # message carries the conditional cleanup guidance instead.
            self._annotate_workload_service_account(
                namespace=namespace,
                role_arn=infra.role_arn,
                cluster_context=cluster_context,
            )
            if any(plan.expect_ingress_address for plan in plans):
                self._wait_for_observability_ingress_address(
                    namespace=namespace, cluster_context=cluster_context
                )
            self._wait_for_connector_healthy(
                name=name,
                cloud_id=cloud_id,
                namespace=namespace,
                cluster_context=cluster_context,
                infra=infra,
            )

            self.log.info("")
            self.log.info("KubeRay cloud setup complete!")
            self.log.info("")
            self.log.info(f"  Cloud ID:          {cloud_id}")
            self.log.info(f"  Cloud resource ID: {cloud_resource_id}")
            self.log.info(f"  Object storage:    s3://{infra.bucket_name}")
            self.log.info(f"  IAM role:          {infra.role_arn}")
            self.log.info(f"  Run RayJobs in:    {namespace}")

            # Setup is done; everything from here is a warning at worst.
            self._offer_test_job(
                test_job=test_job,
                yes=yes,
                namespace=namespace,
                cluster_context=cluster_context,
                cloud_id=cloud_id,
                cloud_resource_id=cloud_resource_id,
            )
        finally:
            self.log.close_block("Setup")

    def _debug(self, msg: str) -> None:
        if self.debug:
            self.log.info(f"[DEBUG] {msg}")

    def _check_no_existing_release(self, namespace: str, cluster_context: Optional[str]) -> None:
        """Stop if the connector release exists: this command installs a fresh connector and
        never upgrades one, so a second run would replace a live install.
        """
        argv = ["helm", "status", CONNECTOR_RELEASE_NAME, "--namespace", namespace, "-o", "json"]
        if cluster_context:
            argv += ["--kube-context", cluster_context]
        result = _run(argv)
        if result.returncode != 0:
            if "not found" in (result.stderr or "").lower():
                return
            raise click.ClickException(
                f"Could not check for an existing connector release in namespace '{namespace}': "
                f"{(result.stderr or result.stdout).strip()}"
            )
        try:
            status = json.loads(result.stdout)["info"]["status"]
        except (ValueError, KeyError, TypeError):
            status = "unknown"
        context_flag = f" --kube-context {cluster_context}" if cluster_context else ""
        raise click.ClickException(
            f"Helm release '{CONNECTOR_RELEASE_NAME}' already exists in namespace '{namespace}' "
            f"(status: {status}). This command installs a fresh connector; to reinstall, run "
            f"`helm{context_flag} -n {namespace} uninstall {CONNECTOR_RELEASE_NAME}` first, or "
            "choose another namespace."
        )

    def _check_required_tools(self) -> None:
        missing = [tool for tool in ("kubectl", "helm") if shutil.which(tool) is None]
        if missing:
            raise click.ClickException(f"Required tools not found on PATH: {', '.join(missing)}")
        helm_version = self._helm_version()
        self.log.info(
            f"kubectl {self._kubectl_client_version()}, helm {helm_version}, "
            f"anyscale {__version__} found",
            block_label="Setup",
        )

    def _log_login(self) -> None:
        """Name the Anyscale host and organization this run acts on. Informational: the
        token already authenticated the controller, so a failed lookup is not fatal.
        """
        try:
            user = self.cloud_controller.api_client.get_user_info_api_v2_userinfo_get().result
            orgs = ", ".join(org.name for org in (user.organizations or [])) or "no organization"
        except Exception as e:  # noqa: BLE001
            self._debug(f"userinfo lookup failed: {e}")
            orgs = "organization unknown"
        self.log.info(f"Logged in to {ANYSCALE_HOST} (organization: {orgs})", block_label="Setup")

    def _helm_version(self) -> str:
        result = _run(["helm", "version", "--template", "{{.Version}}"])
        version = result.stdout.strip()
        match = _HELM_VERSION_PATTERN.match(version) if result.returncode == 0 else None
        if not match:
            raise click.ClickException(
                f"Could not determine the helm version: {(result.stderr or result.stdout).strip()}"
            )
        if (int(match.group(1)), int(match.group(2))) < HELM_MIN_VERSION:
            floor = ".".join(str(part) for part in HELM_MIN_VERSION)
            raise click.ClickException(
                f"helm {version} is too old: setup needs helm {floor} or newer "
                "(`helm repo update <repo>` and the chart's subchart switches)."
            )
        return version

    def _kubectl_client_version(self) -> str:
        # Informational: kubectl has no floor here, and --client never touches the cluster.
        result = _run(["kubectl", "version", "--client", "-o", "json"])
        try:
            return json.loads(result.stdout)["clientVersion"]["gitVersion"]
        except (ValueError, KeyError, TypeError):
            return "(version unknown)"

    def _kubectl(self, cluster_context: Optional[str]) -> List[str]:
        argv = ["kubectl"]
        if cluster_context:
            argv += ["--context", cluster_context]
        return argv

    def _choose_cluster_context(self, yes: bool) -> str:
        """Pick the kubeconfig context to target, pinning the run to one cluster.

        Interactive runs enumerate the kubeconfig's contexts and choose by
        number -- the same picker `cloud verify` uses. --yes has nobody to ask,
        so it takes the current context.
        """
        kubectl = KubectlOperations("", self.log)
        contexts = kubectl.get_available_contexts()
        if not contexts:
            raise click.ClickException(
                "No kubectl contexts found. Configure kubectl access to the "
                "target cluster, or pass --cluster-context."
            )
        current = kubectl.get_current_context()

        if yes:
            if current:
                self.log.info(f"Using current kubectl context: {current}", block_label="Setup")
                return current
            raise click.ClickException(
                "No current kubectl context is set and --yes suppresses the "
                "context picker. Pass --cluster-context <context>."
            )

        if len(contexts) == 1:
            self.log.info(f"Using kubectl context: {contexts[0]}", block_label="Setup")
            return contexts[0]

        self.log.info("Available kubectl contexts:")
        for i, ctx in enumerate(contexts):
            marker = " (current)" if ctx == current else ""
            self.log.info(f"  {i + 1}. {ctx}{marker}")
        default_choice = contexts.index(current) + 1 if current in contexts else 1
        choice = click.prompt(
            "Select context number",
            type=click.IntRange(1, len(contexts)),
            default=default_choice,
        )
        return contexts[choice - 1]

    def _infer_provider(self, issuer: str) -> ProviderInfo:
        """Infer the hosting provider and region from the cluster's token issuer.

        The bucket and IAM identity are created where the cluster runs, and the
        issuer is the one cluster-provided fact that names that place.
        """
        match = _EKS_ISSUER_PATTERN.match(issuer)
        if match:
            return ProviderInfo(provider="aws", region=match.group("region"))
        if issuer.startswith(_GKE_ISSUER_PREFIX):
            raise click.ClickException(
                "GKE clusters are not supported by `cloud setup --stack kuberay` "
                "yet; EKS clusters are supported today."
            )
        raise click.ClickException(
            f"Unrecognized token issuer '{issuer}'. This command supports "
            "cloud-hosted (EKS) Kubernetes clusters, whose issuer identifies the "
            "hosting provider."
        )

    @staticmethod
    def _stack_name(name: str) -> str:
        # Deterministic per cloud name, so a re-run after a partial failure finds
        # and reuses the stack instead of minting a second bucket.
        sanitized = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")[:30]
        return _STACK_NAME_PREFIX + (sanitized.rstrip("-") or "cloud")

    def _boto3_session(self, region: str) -> Any:
        try:
            from anyscale.util import _apn_boto3_session  # noqa: PLC0415
        except ImportError as e:
            raise click.ClickException(
                f"boto3 is required to create the cloud's AWS infrastructure: {e}"
            )
        return _apn_boto3_session(region_name=region)

    def _resolve_aws_identity(self, region: str) -> AwsIdentity:
        """Resolve the AWS principal this run provisions as, before anything is created.

        Otherwise the first AWS call lands after the confirmation prompt, where a
        missing profile is a generic "unexpected error" and a wrong one is a stack in
        the wrong account.
        """
        from botocore.exceptions import NoCredentialsError  # noqa: PLC0415

        try:
            # ProfileNotFound comes from the session, not the STS call.
            identity = self._boto3_session(region).client("sts").get_caller_identity()
        except click.ClickException:
            raise
        except NoCredentialsError:
            raise click.ClickException(
                "Unable to locate AWS credentials. The cloud's S3 bucket and IAM role are "
                "created in your AWS account: set AWS_PROFILE (or run `aws sso login`) "
                "and re-run."
            )
        except Exception as e:  # noqa: BLE001
            # botocore's own text is the specific part: an unknown profile names it,
            # an expired SSO session says to run `aws sso login`.
            raise click.ClickException(f"AWS credentials failed validation: {e}")
        aws_identity = AwsIdentity(account_id=identity["Account"], arn=identity["Arn"])
        self.log.info(
            f"AWS identity: {aws_identity.arn} (account {aws_identity.account_id})",
            block_label="Setup",
        )
        return aws_identity

    def _setup_aws_infrastructure(  # noqa: PLR0913
        self,
        stack_name: str,
        cloud_name: str,
        issuer: str,
        region: str,
        namespace: str,
        account_id: str,
    ) -> AwsInfra:
        """Create (or reuse) the cloud's bucket and IAM identity.

        One CloudFormation stack holds an S3 bucket and an IAM role the cluster's
        pods assume via IRSA. Mirrors the K8S lane's stack, with the trust policy
        widened to every principal that touches the bucket on a KubeRay cloud.
        """
        session = self._boto3_session(region)
        cfn = session.client("cloudformation", region_name=region)

        existing = self._find_reusable_stack(
            cfn,
            stack_name,
            region,
            cloud_name=cloud_name,
            issuer=issuer,
            namespace=namespace,
        )
        if existing is not None:
            bucket_name, role_arn = self._outputs_from_stack(existing, stack_name)
            self.log.info(
                f"Reusing existing infrastructure stack '{stack_name}' (bucket {bucket_name})",
                block_label="Setup",
            )
            return AwsInfra(bucket_name, role_arn, stack_name, region)

        oidc_provider_arn = self._ensure_oidc_provider(session, issuer, account_id)

        self.log.info(
            "Creating S3 bucket and IAM role (this may take a few minutes)...",
            block_label="Setup",
        )
        try:
            from anyscale.utils.cloudformation_utils import (  # noqa: PLC0415
                CloudFormationUtils,
            )
        except ImportError as e:
            raise click.ClickException(f"Failed to import required modules: {e}")

        template_body = self._generate_aws_cloudformation_template(oidc_provider_arn)
        try:
            stack = CloudFormationUtils(self.log).create_and_wait_for_stack(
                stack_name=stack_name,
                template_body=template_body,
                parameters=[
                    {"ParameterKey": "CloudName", "ParameterValue": cloud_name},
                    {"ParameterKey": "Issuer", "ParameterValue": issuer},
                    {"ParameterKey": "Namespace", "ParameterValue": namespace},
                    # Keeps the bucket name globally unique without making the
                    # stack name (the reuse key) random.
                    {
                        "ParameterKey": "BucketSuffix",
                        "ParameterValue": os.urandom(4).hex(),
                    },
                ],
                region=region,
                boto3_session=session,
            )
        except click.ClickException:
            raise
        except Exception as e:  # noqa: BLE001
            raise click.ClickException(
                f"Failed to create AWS infrastructure: {e}. If a partially "
                "created stack remains, delete it with: aws cloudformation "
                f"delete-stack --region {region} --stack-name {stack_name}"
            )

        bucket_name, role_arn = self._outputs_from_stack(stack, stack_name)
        self.log.info(
            f"Created bucket {bucket_name} and IAM role {role_arn}",
            block_label="Setup",
        )
        return AwsInfra(bucket_name, role_arn, stack_name, region)

    def _find_reusable_stack(  # noqa: PLR0913
        self,
        cfn: Any,
        stack_name: str,
        region: str,
        cloud_name: str,
        issuer: str,
        namespace: str,
    ) -> Optional[Dict[str, Any]]:
        """Description of a healthy existing stack, or None if it doesn't exist.

        The stack name folds and truncates the cloud name, so distinct clouds
        can collide on it -- and a stack carries one cluster's trust policy.
        Reuse therefore requires the stack's recorded parameters to match this
        run exactly; anything else fails with the delete command instead of
        silently handing this cloud another cloud's bucket or a dead trust.
        """
        from botocore.exceptions import ClientError  # noqa: PLC0415

        try:
            stacks = cfn.describe_stacks(StackName=stack_name)["Stacks"]
        except ClientError as e:
            if "does not exist" in str(e):
                return None
            raise click.ClickException(
                f"Failed to inspect CloudFormation stack '{stack_name}': {e}"
            )
        if not stacks:
            return None

        stack = stacks[0]
        status = stack.get("StackStatus")
        delete_hint = (
            f"aws cloudformation delete-stack --region {region} --stack-name {stack_name}"
        )
        if status not in ("CREATE_COMPLETE", "UPDATE_COMPLETE"):
            raise click.ClickException(
                f"CloudFormation stack '{stack_name}' exists in state {status} and "
                f"cannot be reused. Delete it and re-run: {delete_hint}"
            )

        recorded = {p["ParameterKey"]: p["ParameterValue"] for p in stack.get("Parameters", [])}
        expected = {"CloudName": cloud_name, "Issuer": issuer, "Namespace": namespace}
        mismatched = {
            key: recorded.get(key) for key, value in expected.items() if recorded.get(key) != value
        }
        if mismatched:
            details = ", ".join(
                f"{key}={value or '(not recorded)'}" for key, value in sorted(mismatched.items())
            )
            raise click.ClickException(
                f"CloudFormation stack '{stack_name}' was created for a different "
                f"setup ({details}) and cannot be reused for cloud '{cloud_name}' "
                "on this cluster. Rename the cloud, or delete the stack and "
                f"re-run: {delete_hint}"
            )
        return stack

    @staticmethod
    def _outputs_from_stack(stack: Dict[str, Any], stack_name: str) -> Tuple[str, str]:
        outputs = {o["OutputKey"]: o["OutputValue"] for o in stack.get("Outputs", [])}
        bucket_name = outputs.get("S3BucketName")
        role_arn = outputs.get("ConnectorRoleArn")
        if not bucket_name or not role_arn:
            raise click.ClickException(
                f"CloudFormation stack '{stack_name}' is missing the expected "
                "outputs; was it created by this command?"
            )
        return bucket_name, role_arn

    def _ensure_oidc_provider(self, session: Any, issuer: str, account_id: str) -> str:
        """Return the IAM OIDC provider ARN for the issuer, creating it if absent.

        IRSA requires the cluster's issuer registered as an IAM identity provider;
        a cluster that has never used IRSA won't have one yet.
        """
        iam = session.client("iam")
        provider_arn = f"arn:aws:iam::{account_id}:oidc-provider/" + issuer.removeprefix(
            "https://"
        )
        try:
            iam.get_open_id_connect_provider(OpenIDConnectProviderArn=provider_arn)
            self._debug(f"IAM OIDC provider exists: {provider_arn}")
            return provider_arn
        except iam.exceptions.NoSuchEntityException:
            pass

        self.log.info(
            "Registering the cluster's OIDC issuer with IAM (required for IRSA)...",
            block_label="Setup",
        )
        try:
            iam.create_open_id_connect_provider(
                Url=issuer,
                ClientIDList=["sts.amazonaws.com"],
            )
        except Exception as e:  # noqa: BLE001
            raise click.ClickException(
                f"Failed to register the IAM OIDC provider for {issuer}: {e}"
            )
        return provider_arn

    def _generate_aws_cloudformation_template(self, oidc_provider_arn: str) -> str:
        """CloudFormation template for the bucket and its IRSA role.

        Bucket properties mirror the K8S lane's. The trust policy differs by
        design, and mirrors how the control plane itself authorizes the
        connector: by namespace, not by service-account name. Everything that
        touches the bucket -- the chart's components and the workload pods --
        runs in the connector's namespace, so one wildcard subject covers it.
        """
        issuer_host_path = oidc_provider_arn.rsplit("oidc-provider/", maxsplit=1)[-1]

        # Via a parameter (not an f-string) so describe_stacks can prove, on
        # reuse, which namespace this stack's trust was built for. The issuer
        # can't be parameterized the same way -- it lives in condition KEYS --
        # so it is recorded as a parameter and checked the same way on reuse.
        subjects = [{"Fn::Sub": "system:serviceaccount:${Namespace}:*"}]

        tags = [{"Key": _INFRA_TAG_KEY, "Value": {"Ref": "CloudName"}}]
        role_tags = tags + [{"Key": _INFRA_ISSUER_TAG_KEY, "Value": {"Ref": "Issuer"}}]
        template: Dict[str, Any] = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "Anyscale KubeRay cloud infrastructure (S3 bucket + IRSA role)",
            "Parameters": {
                "CloudName": {
                    "Type": "String",
                    "Description": "Anyscale cloud name, recorded as a resource tag",
                },
                "Issuer": {
                    "Type": "String",
                    "Description": "Cluster token issuer this stack's trust policy was built for",
                },
                "Namespace": {
                    "Type": "String",
                    "Description": "Connector namespace the trust policy authorizes",
                },
                "BucketSuffix": {
                    "Type": "String",
                    "Description": "Random suffix keeping the bucket name globally unique",
                },
            },
            "Resources": {
                "AnyscaleBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {
                        "BucketName": {"Fn::Sub": "${AWS::StackName}-${BucketSuffix}"},
                        "VersioningConfiguration": {"Status": "Enabled"},
                        "PublicAccessBlockConfiguration": {
                            "BlockPublicAcls": True,
                            "BlockPublicPolicy": True,
                            "IgnorePublicAcls": True,
                            "RestrictPublicBuckets": True,
                        },
                        "CorsConfiguration": {
                            "CorsRules": [
                                {
                                    "AllowedHeaders": ["*"],
                                    "AllowedMethods": [
                                        "GET",
                                        "PUT",
                                        "POST",
                                        "HEAD",
                                        "DELETE",
                                    ],
                                    "AllowedOrigins": [ANYSCALE_CORS_ORIGIN],
                                    "ExposedHeaders": ANYSCALE_CORS_EXPOSE_HEADERS,
                                    "MaxAge": 3600,
                                },
                            ]
                        },
                        "Tags": tags,
                    },
                },
                "AnyscaleConnectorRole": {
                    "Type": "AWS::IAM::Role",
                    "Properties": {
                        "RoleName": {"Fn::Sub": "${AWS::StackName}-connector-role"},
                        "AssumeRolePolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Principal": {"Federated": oidc_provider_arn},
                                    "Action": "sts:AssumeRoleWithWebIdentity",
                                    "Condition": {
                                        "StringLike": {
                                            f"{issuer_host_path}:sub": subjects,
                                        },
                                        "StringEquals": {
                                            f"{issuer_host_path}:aud": "sts.amazonaws.com",
                                        },
                                    },
                                }
                            ],
                        },
                        "Policies": [
                            {
                                "PolicyName": "AnyscaleS3AccessPolicy",
                                "PolicyDocument": {
                                    "Version": "2012-10-17",
                                    "Statement": [
                                        {
                                            "Effect": "Allow",
                                            "Action": [
                                                "s3:GetObject",
                                                "s3:PutObject",
                                                "s3:DeleteObject",
                                                "s3:ListBucket",
                                            ],
                                            "Resource": [
                                                {
                                                    "Fn::GetAtt": [
                                                        "AnyscaleBucket",
                                                        "Arn",
                                                    ]
                                                },
                                                {"Fn::Sub": "${AnyscaleBucket.Arn}/*"},
                                            ],
                                        }
                                    ],
                                },
                            }
                        ],
                        "Tags": role_tags,
                    },
                },
            },
            "Outputs": {
                "S3BucketName": {
                    "Value": {"Ref": "AnyscaleBucket"},
                    "Description": "Name of the S3 bucket",
                },
                "ConnectorRoleArn": {
                    "Value": {"Fn::GetAtt": ["AnyscaleConnectorRole", "Arn"]},
                    "Description": "ARN of the IAM role the cluster's pods assume",
                },
            },
        }
        return json.dumps(template, indent=2)

    def _plan_control_plane(self, edge_domain: Optional[str]) -> ScanPlan:
        """Point the chart at the Anyscale environment this run is logged in to.

        The token audience the OIDC ingress checks follows ANYSCALE_HOST, the way the
        operator setup sets global.controlPlaneURL; in production that is the chart's
        default. The edge domain the connector dials stays the chart's default unless
        the hidden --control-plane-domain names a non-production one.
        """
        origin = ANYSCALE_HOST.rstrip("/")
        sets = ["--set-string", f"global.controlPlaneAudience={origin}"]
        summary = origin
        if edge_domain:
            sets += ["--set-string", f"global.controlPlaneDomain={edge_domain}"]
            summary = f"{origin} (edge domain {edge_domain})"
        return ScanPlan(label="Control plane", summary=summary, helm_sets=tuple(sets))

    def _plan_kuberay_operator(
        self, cluster_context: Optional[str], mode: KuberayOperatorMode, yes: bool
    ) -> ScanPlan:
        """Decide where the KubeRay operator comes from, before anything is created.

        Anyscale runs RayJobs through the operator, so a cluster without one gets the
        operator bundled in the connector chart.
        """
        operator = functools.partial(ScanPlan, "KubeRay operator")
        if mode is KuberayOperatorMode.SKIP:
            return operator(summary="managed by you (--kuberay-operator skip)", helm_sets=())

        self.log.info("Checking for a KubeRay operator on this cluster...", block_label="Setup")
        running = self._find_kuberay_operator(cluster_context)
        if running:
            if mode is KuberayOperatorMode.INSTALL:
                raise click.ClickException(
                    f"A KubeRay operator is already running ({running}); a second one "
                    "would reconcile the same RayJobs. Use --kuberay-operator auto to "
                    "keep it, or skip to manage it yourself."
                )
            return operator(summary=f"found: {running}", helm_sets=())

        if self._rayjob_crd_present(cluster_context):
            self.log.warning(
                f"The {RAYJOB_CRD} CRD is installed but no KubeRay operator pod is "
                "running; the bundled operator would reuse the installed CRDs."
            )
        if mode is KuberayOperatorMode.AUTO:
            self.log.info("KubeRay operator: not found. Anyscale runs RayJobs through it.")
            if not yes and not click.confirm(
                "Install the KubeRay operator bundled with the connector?", default=True
            ):
                raise click.ClickException(
                    "Install a KubeRay operator and re-run, or pass --kuberay-operator "
                    "skip to set up the connector without one."
                )
        return operator(
            summary="install the operator bundled with the connector chart",
            helm_sets=("--set", KUBERAY_OPERATOR_HELM_SET),
        )

    def _plan_gpu_metrics(
        self, cluster_context: Optional[str], dcgm_namespace: Optional[str], yes: bool
    ) -> ScanPlan:
        """Decide where the gateway's GPU metrics scrape points, before anything is created.

        The gateway keeps exactly one Service: the dcgm-exporter named by
        clusterTelemetry.dcgmNamespace/dcgmServiceName, so a wrong name is an empty GPU
        panel with only a startup warning. --dcgm-namespace names the namespace to look
        in; without it the scan looks everywhere, and a cluster with GPU nodes but no
        exporter gets the one bundled in the connector chart.
        """
        gpu = functools.partial(ScanPlan, "GPU metrics")
        self.log.info("Checking for a DCGM exporter on this cluster...", block_label="Setup")
        if dcgm_namespace is not None:
            services = self._find_dcgm_services(cluster_context, namespace=dcgm_namespace)
            if not services:
                raise click.ClickException(
                    f"No dcgm-exporter Service found in namespace '{dcgm_namespace}'. Install "
                    "one there, or drop --dcgm-namespace to let setup look for one."
                )
            chosen = self._pick_dcgm_service(services, yes)
            if chosen is None:
                listed = ", ".join(s.name for s in services)
                raise click.ClickException(
                    f"Several dcgm-exporter Services in '{dcgm_namespace}' ({listed}); run "
                    "without --yes to pick one."
                )
            return self._gpu_plan_for(chosen)

        services = self._find_dcgm_services(cluster_context, namespace=None)
        if services:
            chosen = self._pick_dcgm_service(services, yes)
            if chosen is None:
                listed = ", ".join(f"{s.namespace}/{s.name}" for s in services)
                return gpu(
                    summary=f"off (several DCGM exporters: {listed}; pass --dcgm-namespace <ns>)",
                    helm_sets=(),
                )
            return self._gpu_plan_for(chosen)

        gpu_nodes = self._count_gpu_nodes(cluster_context)
        if gpu_nodes == 0:
            return gpu(summary="off (no GPU nodes, no DCGM exporter)", helm_sets=())
        self.log.info(
            f"GPU metrics: {gpu_nodes} GPU node(s) and no DCGM exporter. GPU panels stay empty without one."
        )
        install = yes or click.confirm(
            "Install the dcgm-exporter bundled with the connector?", default=True
        )
        if not install:
            self.log.warning(
                "GPU metrics are off: the console's GPU panels will be empty for this cloud."
            )
        return gpu(
            summary="install the dcgm-exporter bundled with the connector chart"
            if install
            else "off (no DCGM exporter)",
            helm_sets=("--set", DCGM_EXPORTER_HELM_SET) if install else (),
        )

    @staticmethod
    def _gpu_plan_for(service: DcgmService) -> ScanPlan:
        sets = ["--set-string", f"clusterTelemetry.dcgmNamespace={service.namespace}"]
        # The chart's default name is the GPU Operator's; only another name needs setting.
        if service.name != DCGM_DEFAULT_SERVICE_NAME:
            sets += ["--set-string", f"clusterTelemetry.dcgmServiceName={service.name}"]
        return ScanPlan(
            label="GPU metrics",
            summary=f"found: {service.namespace}/{service.name}",
            helm_sets=tuple(sets),
        )

    def _pick_dcgm_service(self, services: List[DcgmService], yes: bool) -> Optional[DcgmService]:
        """One Service to scrape; None when there are several and --yes forbids a prompt."""
        if len(services) == 1:
            return services[0]
        if yes:
            return None
        self.log.info("Several DCGM exporters found:")
        for i, service in enumerate(services):
            self.log.info(f"  {i + 1}. {service.namespace}/{service.name}")
        choice = click.prompt(
            "Select the DCGM exporter to scrape", type=click.IntRange(1, len(services)), default=1
        )
        return services[choice - 1]

    def _find_dcgm_services(
        self, cluster_context: Optional[str], namespace: Optional[str]
    ) -> List[DcgmService]:
        """dcgm-exporter Services by label; inside a named namespace, also by name."""
        found: Dict[Tuple[str, str], DcgmService] = {}
        scope = ["--namespace", namespace] if namespace else ["--all-namespaces"]
        queries = [["-l", selector] for selector in DCGM_SERVICE_SELECTORS]
        if namespace:
            queries.append([])
        for query in queries:
            argv = self._kubectl(cluster_context) + [
                "--request-timeout=30s",
                "get",
                "services",
                *scope,
                *query,
                "-o",
                "json",
            ]
            self._debug(f"Looking for a DCGM exporter: {' '.join(argv)}")
            for item in self._kubectl_items(argv, what="a DCGM exporter"):
                metadata = item.get("metadata", {})
                name = metadata.get("name", "")
                if not query and "dcgm-exporter" not in name:
                    continue
                service = DcgmService(
                    namespace=metadata.get("namespace", namespace or ""), name=name
                )
                found.setdefault((service.namespace, service.name), service)
        return sorted(found.values())

    def _list_nodes(self, cluster_context: Optional[str]) -> List[Dict[str, Any]]:
        """The cluster's nodes, listed once per run."""
        if self._nodes is None:
            argv = self._kubectl(cluster_context) + [
                "--request-timeout=30s",
                "get",
                "nodes",
                "-o",
                "json",
            ]
            self._debug(f"Listing nodes: {' '.join(argv)}")
            self._nodes = self._kubectl_items(argv, what="nodes")
        return self._nodes

    def _count_gpu_nodes(self, cluster_context: Optional[str]) -> int:
        """Nodes exposing GPUs, by allocatable or by the labels the bundled exporter keys on."""
        count = 0
        for node in self._list_nodes(cluster_context):
            allocatable = str(
                node.get("status", {}).get("allocatable", {}).get(GPU_ALLOCATABLE_KEY, "0")
            )
            labels = node.get("metadata", {}).get("labels", {})
            if allocatable not in ("0", "") or any(label in labels for label in GPU_NODE_LABELS):
                count += 1
        return count

    def _kubectl_items(self, argv: List[str], what: str) -> List[Dict[str, Any]]:
        try:
            result = _run(argv, check=True)
        except subprocess.CalledProcessError as e:
            raise click.ClickException(
                f"Failed to look for {what} on the cluster: {e.stderr.strip()}"
            )
        try:
            items = json.loads(result.stdout).get("items", [])
        except (ValueError, AttributeError):
            raise click.ClickException(
                f"Unexpected kubectl output while looking for {what}: {result.stdout[:200]}"
            )
        return list(items)

    def _plan_ingress(  # noqa: PLR0913
        self,
        cluster_context: Optional[str],
        ingress_class: Optional[str],
        provider: str,
        yes: bool,
    ) -> ScanPlan:
        """Decide which ingress controller fronts the Observability API and the workload
        Ingresses, before anything is created.

        The console reaches the API through the chart's Ingress, and KCP registers the host's
        DNS from that Ingress's load-balancer address. --ingress-class names a controller on
        the cluster; otherwise the user picks one of the cluster's classes or the traefik the
        connector chart bundles, which --yes takes unasked. The bundled class left by an
        earlier setup is reused: its IngressClass is cluster-scoped, so a second install
        cannot own it.
        """
        self.log.info("Checking for ingress controllers on this cluster...", block_label="Setup")
        classes = self._list_ingress_classes(cluster_context)
        if ingress_class is not None:
            match = next((c for c in classes if c.name == ingress_class), None)
            if match is None:
                found = ", ".join(c.name for c in classes) or "none"
                raise click.ClickException(
                    f"No IngressClass '{ingress_class}' on the cluster (found: {found}). Install its "
                    "controller first, or drop --ingress-class to choose one."
                )
            return self._existing_ingress_plan(match, f"{match.name} ({match.controller})")
        bundled = next((c for c in classes if c.name == BUNDLED_INGRESS_CLASS_NAME), None)
        if bundled is not None:
            return self._existing_ingress_plan(
                bundled, f"{bundled.name} (installed by an earlier setup)"
            )
        if yes or not classes:
            return self._bundled_ingress_plan(provider)
        self.log.info("Ingress controllers on this cluster:")
        for i, info in enumerate(classes):
            self.log.info(f"  {i + 1}. {info.name} ({info.controller})")
        install = len(classes) + 1
        self.log.info(
            f"  {install}. Install the traefik ingress controller bundled with the connector chart"
        )
        choice = click.prompt(
            "Select the ingress controller for the Observability API",
            type=click.IntRange(1, install),
            default=install,
        )
        if choice == install:
            return self._bundled_ingress_plan(provider)
        match = classes[choice - 1]
        return self._existing_ingress_plan(match, f"{match.name} ({match.controller})")

    @staticmethod
    def _bundled_ingress_plan(provider: str) -> ScanPlan:
        sets = ["--set", BUNDLED_INGRESS_HELM_SET]
        if provider == "aws":
            for key, value in AWS_LB_SERVICE_ANNOTATIONS:
                escaped = key.replace(".", "\\.")
                sets += ["--set-string", f"traefik.service.annotations.{escaped}={value}"]
        return ScanPlan(
            label="Ingress",
            summary="install the traefik ingress controller bundled with the connector chart",
            helm_sets=tuple(sets),
            expect_ingress_address=True,
        )

    @staticmethod
    def _existing_ingress_plan(match: IngressClassInfo, summary: str) -> ScanPlan:
        # One class for the Observability API's Ingress and for the Ingresses Anyscale creates
        # for workloads (the connector's default class).
        return ScanPlan(
            label="Ingress",
            summary=summary,
            helm_sets=(
                "--set-string",
                f"observabilityApi.ingress.className={match.name}",
                "--set-string",
                f"global.ingressClassName={match.name}",
            ),
            expect_ingress_address=True,
        )

    def _list_ingress_classes(self, cluster_context: Optional[str]) -> List[IngressClassInfo]:
        argv = self._kubectl(cluster_context) + [
            "--request-timeout=30s",
            "get",
            "ingressclass",
            "-o",
            "json",
        ]
        self._debug(f"Listing ingress classes: {' '.join(argv)}")
        classes = []
        for item in self._kubectl_items(argv, what="ingress classes"):
            metadata = item.get("metadata", {})
            classes.append(
                IngressClassInfo(
                    name=metadata.get("name", ""),
                    controller=item.get("spec", {}).get("controller", "?"),
                )
            )
        return sorted(classes)

    def _wait_for_observability_ingress_address(
        self, namespace: str, cluster_context: Optional[str]
    ) -> None:
        """Warn when the Observability API's Ingress gets no load-balancer address: KCP needs one
        to register the console's DNS, and a class with a dead controller never produces it.
        """
        self.log.info(
            "Waiting for the Observability API ingress to get a load balancer address...",
            block_label="Setup",
        )
        argv = self._kubectl(cluster_context) + [
            "--request-timeout=30s",
            "get",
            "ingress",
            OBSERVABILITY_INGRESS_NAME,
            "-n",
            namespace,
            "-o",
            "json",
        ]
        kctx = f" --context {cluster_context}" if cluster_context else ""
        deadline = time.monotonic() + INGRESS_ADDRESS_TIMEOUT_SECONDS
        while True:
            try:
                result = _run(argv)
            except click.ClickException as e:
                # A kubectl hang (the exec credential plugin outlives --request-timeout) must
                # not end a setup that already succeeded.
                self.log.warning(
                    f"Could not read the Observability API Ingress ({e.message}). Check it with: "
                    f"kubectl{kctx} get ingress {OBSERVABILITY_INGRESS_NAME} -n {namespace}"
                )
                return
            if result.returncode == 0:
                try:
                    entries = (
                        json.loads(result.stdout)
                        .get("status", {})
                        .get("loadBalancer", {})
                        .get("ingress")
                        or []
                    )
                except (ValueError, AttributeError):
                    entries = []
                for entry in entries:
                    address = entry.get("hostname") or entry.get("ip")
                    if address:
                        self.log.info(
                            f"Observability API ingress address: {address}", block_label="Setup"
                        )
                        return
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            time.sleep(min(INGRESS_ADDRESS_POLL_SECONDS, remaining))
        self.log.warning(
            f"The Observability API Ingress has no load balancer address after "
            f"{INGRESS_ADDRESS_TIMEOUT_SECONDS}s, so the console cannot reach it yet. Check the "
            f"ingress controller: kubectl{kctx} describe ingress {OBSERVABILITY_INGRESS_NAME} -n {namespace}"
        )

    def _offer_test_job(  # noqa: PLR0913
        self,
        test_job: Optional[bool],
        yes: bool,
        namespace: str,
        cluster_context: Optional[str],
        cloud_id: str,
        cloud_resource_id: str,
    ) -> None:
        """Run the sample RayJob so the console shows logs and metrics minutes after setup.

        None asks; --yes skips unless --test-job. Declining still writes the YAML so it
        can run later. Nothing here can fail setup, which already succeeded.
        """
        if test_job is False or (test_job is None and yes):
            return
        try:
            self._run_test_job(test_job, namespace, cluster_context, cloud_id, cloud_resource_id)
        except click.Abort:
            raise
        except KeyboardInterrupt:
            # Setup already succeeded; stopping the wait must not turn it into a failure.
            self.log.warning(
                f"Stopped waiting on the sample RayJob; it keeps running. Watch it with: kubectl "
                f"-n {namespace} get rayjob {SAMPLE_RAYJOB_NAME}"
            )
        except Exception as e:  # noqa: BLE001
            self.log.warning(
                f"The sample RayJob step did not finish: {e}. Run it later with: kubectl apply "
                f"-f ./{SAMPLE_RAYJOB_FILE}"
            )

    def _run_test_job(  # noqa: PLR0913
        self,
        test_job: Optional[bool],
        namespace: str,
        cluster_context: Optional[str],
        cloud_id: str,
        cloud_resource_id: str,
    ) -> None:
        self.log.info("")
        run_now = test_job is True or click.confirm(
            "Run a sample RayJob now to see logs and metrics in Anyscale?", default=True
        )
        path = self._write_sample_rayjob(namespace)
        rerun = f"kubectl apply -f ./{SAMPLE_RAYJOB_FILE}"
        if not run_now:
            self.log.info(
                f"Wrote ./{SAMPLE_RAYJOB_FILE}; run it later with: {rerun}", block_label="Setup"
            )
            return
        self.log.info(
            f"Wrote ./{SAMPLE_RAYJOB_FILE} (head + 2 workers, about 5 minutes of CPU load)",
            block_label="Setup",
        )
        argv = self._kubectl(cluster_context) + [
            "--request-timeout=30s",
            "apply",
            "-f",
            str(path),
        ]
        self._debug(f"Submitting the sample RayJob: {' '.join(argv)}")
        result = _run(argv)
        if result.returncode != 0:
            self.log.warning(
                f"Could not submit the sample RayJob: {result.stderr.strip()}. The file is at "
                f"./{SAMPLE_RAYJOB_FILE}; run it later with: {rerun}"
            )
            return
        self.log.info(
            f"Submitted RayJob {SAMPLE_RAYJOB_NAME} to namespace {namespace}", block_label="Setup"
        )
        self._wait_for_rayjob_running(namespace, cluster_context)
        job = self._find_tracked_job(cloud_id, cloud_resource_id)
        if job is not None:
            self.log.info(f"Anyscale is tracking it as job {job.id}", block_label="Setup")
            self.log.info(f"  Sample job logs and dashboards: {get_endpoint(f'/jobs/{job.id}')}")
        self.log.info(
            "  The job runs for about 5 minutes and deletes itself 10 minutes after it finishes."
        )
        self.log.info(f"  Run it again with: {rerun}")

    @staticmethod
    def _sample_rayjob(namespace: str) -> Dict[str, Any]:
        image = f"anyscale/ray:{DEFAULT_RAY_VERSION}-{DEFAULT_PYTHON_VERSION}"
        resources = {
            "requests": {"cpu": "1", "memory": "2Gi"},
            "limits": {"cpu": "2", "memory": "4Gi"},
        }
        return {
            "apiVersion": "ray.io/v1",
            "kind": "RayJob",
            "metadata": {"name": SAMPLE_RAYJOB_NAME, "namespace": namespace},
            "spec": {
                "shutdownAfterJobFinishes": True,
                "ttlSecondsAfterFinished": 600,
                "entrypoint": _SAMPLE_RAYJOB_ENTRYPOINT,
                "rayClusterSpec": {
                    "rayVersion": DEFAULT_RAY_VERSION,
                    "headGroupSpec": {
                        "rayStartParams": {"dashboard-host": "0.0.0.0"},
                        "template": {
                            "spec": {
                                "containers": [
                                    {
                                        "name": "ray-head",
                                        "image": image,
                                        "ports": [
                                            {"containerPort": 6379, "name": "gcs"},
                                            {"containerPort": 8265, "name": "dashboard"},
                                            {"containerPort": 10001, "name": "client"},
                                        ],
                                        "resources": resources,
                                    }
                                ]
                            }
                        },
                    },
                    "workerGroupSpecs": [
                        {
                            "groupName": "small",
                            "replicas": 2,
                            "minReplicas": 2,
                            "maxReplicas": 2,
                            "rayStartParams": {},
                            "template": {
                                "spec": {
                                    "containers": [
                                        {
                                            "name": "ray-worker",
                                            "image": image,
                                            "resources": resources,
                                        }
                                    ]
                                }
                            },
                        }
                    ],
                },
            },
        }

    def _write_sample_rayjob(self, namespace: str) -> Path:
        path = Path.cwd() / SAMPLE_RAYJOB_FILE
        path.write_text(
            "# The connector tracks RayJobs in its own namespace only.\n"
            + yaml.dump(self._sample_rayjob(namespace), Dumper=_BlockScalarDumper, sort_keys=False)
        )
        return path

    def _wait_for_rayjob_running(self, namespace: str, cluster_context: Optional[str]) -> None:
        """Report the RayJob's deployment status until it runs, finishes, or the wait ends."""
        argv = self._kubectl(cluster_context) + [
            "--request-timeout=30s",
            "get",
            "rayjob",
            SAMPLE_RAYJOB_NAME,
            "-n",
            namespace,
            "-o",
            "json",
        ]
        started = time.monotonic()
        deadline = started + RAYJOB_RUNNING_TIMEOUT_SECONDS
        last = ""
        while True:
            result = _run(argv)
            status = ""
            if result.returncode == 0:
                try:
                    status = (
                        json.loads(result.stdout).get("status", {}).get("jobDeploymentStatus", "")
                        or ""
                    )
                except (ValueError, AttributeError):
                    status = ""
            if status and status != last:
                elapsed = int(time.monotonic() - started)
                self.log.info(f"  {last or SAMPLE_RAYJOB_NAME} -> {status} ({elapsed}s)")
                last = status
            if status in ("Running", "Complete"):
                return
            if status == "Failed":
                self.log.warning(
                    f"The sample RayJob failed. Inspect it with: kubectl describe rayjob "
                    f"{SAMPLE_RAYJOB_NAME} -n {namespace}"
                )
                return
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            time.sleep(min(RAYJOB_POLL_SECONDS, remaining))
        self.log.warning(
            f"The sample RayJob is not running after {RAYJOB_RUNNING_TIMEOUT_SECONDS}s (status: "
            f"{last or 'unknown'}). A first run pulls the Ray image, which can take a while. Check "
            f"it with: kubectl get rayjob {SAMPLE_RAYJOB_NAME} -n {namespace}"
        )

    def _find_tracked_job(self, cloud_id: str, cloud_resource_id: str) -> Any:
        """The Anyscale job imported for the sample RayJob: the workload of that name on this
        cluster. None after the wait, with a warning carrying the last lookup error.
        """
        deadline = time.monotonic() + TRACKED_JOB_TIMEOUT_SECONDS
        api = self.cloud_controller.api_client
        last_error: Optional[str] = None

        # The cluster's own workload listing, scoped by URL to this cloud resource and
        # with no required filters. The decorated jobs listing scopes by cloud at most
        # and rejects calls without a type_filter.
        def page(paging_token: Optional[str]) -> Any:
            return api.list_k8s_cluster_workloads_api_v2_clouds_cloud_id_k8s_clusters_cluster_id_workloads_get(
                cloud_id, cloud_resource_id, count=TRACKED_JOB_PAGE_SIZE, paging_token=paging_token
            )

        while True:
            match = None
            try:
                paging_token = None
                for _ in range(TRACKED_JOB_MAX_PAGES):
                    response = page(paging_token)
                    match = next(
                        (
                            workload
                            for workload in (getattr(response, "results", None) or [])
                            if getattr(workload, "name", None) == SAMPLE_RAYJOB_NAME
                        ),
                        None,
                    )
                    metadata = getattr(response, "metadata", None)
                    paging_token = getattr(metadata, "next_paging_token", None)
                    if match is not None or not paging_token:
                        break
            except Exception as e:  # noqa: BLE001
                last_error = str(e)
                self._debug(f"Workload lookup failed: {e}")
            if match is not None:
                return match
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            time.sleep(min(TRACKED_JOB_POLL_SECONDS, remaining))
        detail = f" Last lookup error: {last_error}" if last_error else ""
        self.log.warning(
            f"Anyscale has not picked up the sample RayJob after {TRACKED_JOB_TIMEOUT_SECONDS}s. It "
            "appears under Jobs in the console once the connector reports it; check the connector "
            f"pod logs if it does not.{detail}"
        )
        return None

    def _find_kuberay_operator(self, cluster_context: Optional[str]) -> Optional[str]:
        """Describe a live KubeRay operator pod as '<namespace>/<pod> (<image>)', or None."""
        argv = self._kubectl(cluster_context) + [
            "--request-timeout=30s",
            "get",
            "pods",
            "--all-namespaces",
            "-l",
            KUBERAY_OPERATOR_POD_SELECTOR,
            "-o",
            "json",
        ]
        self._debug(f"Looking for a KubeRay operator: {' '.join(argv)}")
        pods = self._kubectl_items(argv, what="a KubeRay operator")
        # Finished pods are leftovers, not an operator.
        live = [
            pod
            for pod in pods
            if pod.get("status", {}).get("phase") not in ("Succeeded", "Failed")
        ]
        if not live:
            return None
        pod = live[0]
        metadata = pod.get("metadata", {})
        containers = pod.get("spec", {}).get("containers", [])
        image = containers[0].get("image", "?") if containers else "?"
        phase = pod.get("status", {}).get("phase", "")
        state = "" if phase == "Running" else f", {phase}"
        return f"{metadata.get('namespace')}/{metadata.get('name')} ({image}{state})"

    def _rayjob_crd_present(self, cluster_context: Optional[str]) -> bool:
        argv = self._kubectl(cluster_context) + [
            "--request-timeout=30s",
            "get",
            "crd",
            RAYJOB_CRD,
            "-o",
            "name",
        ]
        return _run(argv).returncode == 0

    def _discover_issuer(self, cluster_context: Optional[str]) -> str:
        """Read the cluster's token issuer from its own discovery document.

        Provider-agnostic: every conformant apiserver serves service-account issuer
        discovery, so this needs no cloud API and no per-provider branch. Only the
        issuer is taken from this document -- its jwks_uri points at the apiserver's
        private address (observed on EKS), never at the key set the issuer serves
        publicly.
        """
        argv = self._kubectl(cluster_context) + [
            "--request-timeout=30s",
            "get",
            "--raw",
            "/.well-known/openid-configuration",
        ]
        self._debug(f"Discovering issuer: {' '.join(argv)}")
        try:
            result = _run(argv, check=True)
        except subprocess.CalledProcessError as e:
            raise click.ClickException(
                f"Failed to read the cluster's OIDC discovery document: {e.stderr.strip()}"
            )

        try:
            issuer = json.loads(result.stdout)["issuer"]
        except (ValueError, KeyError):
            raise click.ClickException(
                f"The cluster's OIDC discovery document is missing 'issuer': {result.stdout[:200]}"
            )

        self._debug(f"Discovered issuer={issuer}")
        return issuer

    def _resolve_public_jwks(self, issuer: str) -> str:
        """Resolve the issuer's JWKS the way Anyscale's verifier will.

        Anyscale discovers keys from the issuer's own discovery document, fetched from
        outside the cluster -- so resolving it here proves the exact chain token
        verification will use, and fails at setup instead of at the connector's first
        sync.
        """
        discovery_url = issuer.rstrip("/") + "/.well-known/openid-configuration"
        try:
            response = requests.get(discovery_url, timeout=10)
            response.raise_for_status()
            jwks_uri = response.json()["jwks_uri"]
        except Exception as e:  # noqa: BLE001
            raise click.ClickException(
                f"The cluster's token issuer is not publicly discoverable "
                f"({discovery_url}): {e}. Anyscale verifies connector tokens by "
                "fetching the issuer's keys, so the issuer must be reachable from "
                "outside the cluster."
            )
        try:
            requests.get(jwks_uri, timeout=10).raise_for_status()
        except Exception as e:  # noqa: BLE001
            raise click.ClickException(
                f"The issuer's JWKS endpoint is not reachable ({jwks_uri}): {e}"
            )
        self._debug(f"Resolved public jwks_uri={jwks_uri}")
        return jwks_uri

    def _register_cloud(
        self,
        name: str,
        namespace: str,
        infra: AwsInfra,
        issuer_info: IssuerInfo,
        auto_add_user: bool,
    ) -> None:
        self.log.info("Registering cloud with Anyscale...", block_label="Setup")

        cloud_deployment = CloudDeployment(
            name=name,
            provider=CloudProviders.GENERIC,
            compute_stack=ComputeStack.KUBERAY,
            region=infra.region,
            # The bucket's region matters: KCP renders the telemetry exporters
            # from it, falling back to the record's region when absent.
            object_storage=ObjectStorage(
                bucket_name=f"s3://{infra.bucket_name}",
                region=infra.region,
            ),
            # The IAM role is deliberately NOT registered: the server discards
            # kubernetes_config for KUBERAY resources (verified live), and the
            # role is recoverable from the deterministic, tagged stack.
            connector_config=ConnectorConfig(
                service_account_name=CONNECTOR_SERVICE_ACCOUNT,
                service_account_namespace=namespace,
                oidc_issuer=issuer_info.issuer,
                jwks_uri=issuer_info.jwks_uri,
                # Explicit, not omitted: an absent list reads as "unknown"
                # downstream (connectorconfig.go), not as this-namespace-only.
                allowed_namespaces=[namespace],
            ),
        )

        try:
            self.cloud_controller.register_azure_or_generic_cloud(
                name=name,
                provider="generic",
                cloud_resource=cloud_deployment,
                auto_add_user=auto_add_user,
            )
        except Exception as e:  # noqa: BLE001
            raise click.ClickException(f"Failed to register cloud: {e}")

    def _resolve_cloud_ids(self, name: str) -> Tuple[str, str]:
        """Fetch the ids of the cloud just registered under `name`.

        Separate from _register_cloud so a failure here still marks the cloud as
        registered for cleanup: the controller rolls back its own failures, but a
        fetch failure leaves the cloud in place.
        """
        try:
            cloud_id, _ = get_cloud_id_and_name(self.cloud_controller.api_client, cloud_name=name)
        except Exception as e:  # noqa: BLE001
            raise click.ClickException(f"Failed to find registered cloud: {e}")

        cloud_resources = self.cloud_controller.api_client.get_cloud_resources_api_v2_clouds_cloud_id_resources_get(
            cloud_id=cloud_id
        ).results
        if len(cloud_resources) != 1:
            raise click.ClickException(
                f"Expected 1 cloud resource after registration, got {len(cloud_resources)}"
            )

        cloud_resource_id = cloud_resources[0].cloud_resource_id
        self.log.info(f"Cloud registered with ID: {cloud_id}", block_label="Setup")
        return cloud_id, cloud_resource_id

    def _ensure_chart(self, connector_chart: Optional[str]) -> str:
        if connector_chart:
            self._debug(f"Using connector chart from: {connector_chart}")
            return connector_chart

        self.log.info("Configuring Anyscale Helm repository...", block_label="Setup")
        # Don't fail if the repo already exists.
        _run(["helm", "repo", "add", HELM_REPO_NAME, HELM_REPO_URL])
        try:
            _run(
                ["helm", "repo", "update", HELM_REPO_NAME],
                timeout_seconds=120,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise click.ClickException(f"Failed to update Helm repository: {e.stderr}")

        # The repository predates the connector chart, so probe for it instead of
        # letting `helm install` fail mid-setup with a bare "not found".
        result = _run(["helm", "search", "repo", CONNECTOR_CHART_REF, "-o", "json"])
        try:
            found = json.loads(result.stdout) if result.returncode == 0 else []
        except ValueError:
            found = []
        if not found:
            raise click.ClickException(
                f"The '{HELM_REPO_NAME}' Helm repository does not serve "
                f"{CONNECTOR_CHART_REF} yet. Pass --connector-chart <path> to install "
                "from a local chart."
            )
        return CONNECTOR_CHART_REF

    def _install_connector(  # noqa: PLR0913
        self,
        chart_reference: str,
        namespace: str,
        cloud_id: str,
        cloud_resource_id: str,
        cluster_context: Optional[str],
        connector_values: Optional[str],
        role_arn: str,
        extra_set_args: Sequence[str] = (),
    ) -> None:
        self.log.info("Installing Anyscale connector...", block_label="Setup")

        argv = [
            "helm",
            "install",
            CONNECTOR_RELEASE_NAME,
            chart_reference,
            "--namespace",
            namespace,
            "--create-namespace",
            "--wait",
            "--timeout",
            HELM_WAIT_TIMEOUT,
            "--set-string",
            f"global.cloudId={cloud_id}",
            "--set-string",
            f"global.cloudResourceId={cloud_resource_id}",
        ]
        # The chart takes one annotations map per ServiceAccount it creates; all
        # three components read the bucket, so the role lands on each. The dots
        # in the annotation key are escaped so helm keeps them in one key.
        escaped_key = IRSA_ROLE_ANNOTATION.replace(".", "\\.")
        for values_path in CHART_SERVICE_ACCOUNT_VALUES:
            argv += ["--set-string", f"{values_path}.annotations.{escaped_key}={role_arn}"]
        # What the cluster scan decided (today: the bundled KubeRay operator).
        argv += list(extra_set_args)
        # global.allowedNamespaces is not set: the chart's webhook selector
        # falls back to the release namespace, which is exactly the scope.
        if cluster_context:
            argv += ["--kube-context", cluster_context]
        if connector_values:
            argv += ["--values", connector_values]

        self._debug(f"Executing: {' '.join(argv)}")
        try:
            _run(argv, timeout_seconds=HELM_INSTALL_TIMEOUT_SECONDS, check=True)
        except subprocess.CalledProcessError as e:
            raise click.ClickException(f"Failed to install Anyscale connector: {e.stderr}")
        self.log.info("Connector installed", block_label="Setup")

    def _annotate_workload_service_account(
        self,
        namespace: str,
        role_arn: str,
        cluster_context: Optional[str],
    ) -> None:
        """Annotate the workload namespace's default ServiceAccount for IRSA.

        Dispatched Ray pods run under the namespace's default service account
        (nothing sets serviceAccountName on them), and their log-shipping sidecar
        writes the bucket with ambient credentials -- this annotation is what
        provides them. Non-fatal, hangs included: kubectl's exec credential
        plugin isn't bounded by --request-timeout, and a timeout here must not
        abort a setup whose cloud and install already succeeded.
        """
        existing = self._current_role_annotation(namespace, cluster_context)
        if existing and existing != role_arn:
            self.log.warning(
                f"Namespace '{namespace}': replacing the default service account's "
                f"existing {IRSA_ROLE_ANNOTATION} ({existing}) -- another "
                "Anyscale cloud may be sharing this namespace."
            )
        argv = self._kubectl(cluster_context) + [
            "--request-timeout=30s",
            "-n",
            namespace,
            "annotate",
            "serviceaccount",
            "default",
            f"{IRSA_ROLE_ANNOTATION}={role_arn}",
            "--overwrite",
        ]
        try:
            result = _run(argv)
            failure = result.stderr.strip() if result.returncode != 0 else None
        except click.ClickException as e:
            failure = e.message
        if failure is not None:
            self.log.warning(
                f"Could not annotate the default service account in namespace "
                f"'{namespace}' ({failure}). Workloads there cannot "
                f"reach the bucket until you run: {' '.join(argv)}"
            )

    def _current_role_annotation(
        self, namespace: str, cluster_context: Optional[str]
    ) -> Optional[str]:
        escaped_key = IRSA_ROLE_ANNOTATION.replace(".", r"\.")
        argv = self._kubectl(cluster_context) + [
            "--request-timeout=30s",
            "-n",
            namespace,
            "get",
            "serviceaccount",
            "default",
            "-o",
            f"jsonpath={{.metadata.annotations.{escaped_key}}}",
        ]
        try:
            result = _run(argv)
        except click.ClickException:
            return None  # A hung kubectl must not abort the non-fatal step.
        if result.returncode != 0:
            return None
        return result.stdout.strip() or None

    def _wait_for_connector_healthy(  # noqa: PLR0913
        self,
        name: str,
        cloud_id: str,
        namespace: str,
        cluster_context: Optional[str],
        infra: AwsInfra,
    ) -> None:
        """Poll the reachability Anyscale derives from the connector's own reports."""
        self.log.info(
            "Waiting for Anyscale to report the connector healthy...",
            block_label="Setup",
        )
        deadline = time.monotonic() + CONNECTOR_HEALTHY_TIMEOUT_SECONDS
        last_status = "UNKNOWN"
        last_error: Optional[str] = None
        while time.monotonic() < deadline:
            try:
                clusters = self.cloud_controller.api_client.list_k8s_clusters_api_v2_clouds_cloud_id_k8s_clusters_get(
                    cloud_id
                ).results
                last_error = None
            except Exception as e:  # noqa: BLE001
                self._debug(f"Status poll failed (will retry): {e}")
                last_error = str(e)
                clusters = []
            statuses = [c.status for c in clusters]
            if "HEALTHY" in statuses:
                self.log.info("Connector is HEALTHY", block_label="Setup")
                return
            if statuses:
                last_status = statuses[0]
            time.sleep(
                min(
                    CONNECTOR_HEALTHY_POLL_SECONDS,
                    max(0.0, deadline - time.monotonic()),
                )
            )

        status_note = (
            f"last status: {last_status}"
            if last_error is None
            else f"status could not be fetched: {last_error}"
        )
        kctx = f" --context {cluster_context}" if cluster_context else ""
        raise click.ClickException(
            f"The connector did not report healthy within "
            f"{CONNECTOR_HEALTHY_TIMEOUT_SECONDS}s ({status_note}). The install "
            f"itself succeeded and may still turn healthy; inspect with: "
            f"kubectl{kctx} -n {namespace} logs deploy/anyscale-connector "
            f"-c connector. If it never does, clean up with: "
            f"{_cloud_delete_command(name)} && "
            f"{_helm_uninstall_command(namespace, cluster_context)}, delete the "
            f"AWS infrastructure (empty the bucket first if it has data): "
            f"{_stack_delete_command(infra)}, and remove the identity annotation "
            f"from each workload namespace: kubectl{kctx} -n <namespace> annotate "
            f"serviceaccount default {IRSA_ROLE_ANNOTATION}-"
        )

    def _log_cleanup_instructions(  # noqa: PLR0913
        self,
        name: str,
        cloud_registered: bool,
        namespace: str,
        cluster_context: Optional[str],
        install_started: bool,
        infra: Optional[AwsInfra],
    ) -> None:
        if not cloud_registered and not install_started and infra is None:
            return  # Nothing was created.
        self.log.error("")
        self.log.error("Setup did not complete. To clean up:")
        if cloud_registered:
            self.log.error(f"  - Delete the cloud: {_cloud_delete_command(name)}")
        if install_started:
            self.log.error(
                f"  - Remove the install: {_helm_uninstall_command(namespace, cluster_context)}"
            )
        if infra is not None:
            self.log.error(
                f"  - Delete the AWS infrastructure (empty the S3 bucket "
                f"'{infra.bucket_name}' first if it has data): "
                f"{_stack_delete_command(infra)}"
            )


def setup_kuberay_cloud(  # noqa: PLR0913
    name: str,
    cluster_context: Optional[str],
    namespace: str,
    yes: bool = False,
    connector_chart: Optional[str] = None,
    connector_values: Optional[str] = None,
    auto_add_user: bool = True,
    debug: bool = False,
    kuberay_operator: KuberayOperatorMode = KuberayOperatorMode.AUTO,
    dcgm_namespace: Optional[str] = None,
    ingress_class: Optional[str] = None,
    test_job: Optional[bool] = None,
    control_plane_domain: Optional[str] = None,
) -> None:
    """Set up an Anyscale KubeRay (connector) cloud on a Kubernetes cluster."""
    cmd = KubeRayCloudSetupCommand(debug=debug)
    try:
        cmd.run(
            name=name,
            cluster_context=cluster_context,
            namespace=namespace,
            yes=yes,
            connector_chart=connector_chart,
            connector_values=connector_values,
            auto_add_user=auto_add_user,
            kuberay_operator=kuberay_operator,
            dcgm_namespace=dcgm_namespace,
            ingress_class=ingress_class,
            test_job=test_job,
            control_plane_domain=control_plane_domain,
        )
    except click.Abort:
        raise
    except Exception as e:  # noqa: BLE001
        click.echo(f"Setup failed: {e}", err=True)
        raise click.Abort()
