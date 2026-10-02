"""Set up an Anyscale KubeRay (connector) cloud on an existing Kubernetes cluster.

The KubeRay lane is opinionated: setup discovers the cluster's token issuer, infers
the hosting provider from it, creates the cloud's object-storage bucket together
with the IAM identity that lets the cluster's pods use it, registers the cloud,
installs the connector chart, and waits until Anyscale reports the connector
healthy. Trust still flows outward -- Anyscale verifies the connector's projected
service-account token against the issuer registered here -- so no dataplane
credential is ever handed to Anyscale.
"""

import json
import os
import re
import shutil
import subprocess
import time
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

import click
import requests

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
)


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
# registry/chart fetches.
HELM_INSTALL_TIMEOUT_SECONDS = 900
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
        # The controller's closing output (a "run this helm command" block)
        # doesn't apply here -- this command runs the install itself -- so the
        # controller gets a muted logger. Failures still surface as exceptions.
        self.cloud_controller = CloudController(log=CloudSetupLogger(log_output=False))
        self.debug = debug or os.environ.get("ANYSCALE_DEBUG") == "1"

    def run(  # noqa: PLR0913
        self,
        name: str,
        cluster_context: Optional[str],
        namespace: str,
        yes: bool,
        connector_chart: Optional[str] = None,
        connector_values: Optional[str] = None,
        auto_add_user: bool = True,
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
        self.log.open_block(
            "Setup",
            f"Setting up KubeRay cloud '{name}'",
        )
        try:
            self._check_required_tools()

            cluster_context = cluster_context or self._choose_cluster_context(yes)
            issuer = self._discover_issuer(cluster_context)
            provider_info = self._infer_provider(issuer)
            stack_name = self._stack_name(name)

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
                    "(S3 bucket + IAM role, created in your account)"
                )
                click.confirm("Continue?", abort=True)

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
        finally:
            self.log.close_block("Setup")

    def _debug(self, msg: str) -> None:
        if self.debug:
            self.log.info(f"[DEBUG] {msg}")

    def _check_required_tools(self) -> None:
        missing = [tool for tool in ("kubectl", "helm") if shutil.which(tool) is None]
        if missing:
            raise click.ClickException(f"Required tools not found on PATH: {', '.join(missing)}")

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

    def _setup_aws_infrastructure(  # noqa: PLR0913
        self,
        stack_name: str,
        cloud_name: str,
        issuer: str,
        region: str,
        namespace: str,
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

        oidc_provider_arn = self._ensure_oidc_provider(session, issuer)

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

    def _ensure_oidc_provider(self, session: Any, issuer: str) -> str:
        """Return the IAM OIDC provider ARN for the issuer, creating it if absent.

        IRSA requires the cluster's issuer registered as an IAM identity provider;
        a cluster that has never used IRSA won't have one yet.
        """
        sts = session.client("sts")
        iam = session.client("iam")
        try:
            account_id = sts.get_caller_identity()["Account"]
        except Exception as e:  # noqa: BLE001
            raise click.ClickException(
                f"Failed to resolve the AWS account (are AWS credentials configured?): {e}"
            )

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
        # letting `helm upgrade` fail mid-setup with a bare "not found".
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
    ) -> None:
        self.log.info("Installing Anyscale connector...", block_label="Setup")

        argv = [
            "helm",
            "upgrade",
            CONNECTOR_RELEASE_NAME,
            chart_reference,
            "--namespace",
            namespace,
            "--create-namespace",
            "--wait",
            "--timeout",
            HELM_WAIT_TIMEOUT,
            "-i",
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
        )
    except click.Abort:
        raise
    except Exception as e:  # noqa: BLE001
        click.echo(f"Setup failed: {e}", err=True)
        raise click.Abort()
