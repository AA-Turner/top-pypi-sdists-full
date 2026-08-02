# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import base64
import logging
import tempfile
from datetime import datetime, timedelta
from typing import Any

from kubernetes import client, config

from geneva.cluster import K8sConfigMethod

_LOG = logging.getLogger(__name__)

# Default EKS token expiration period in seconds (30mins)
TOKEN_EXPIRATION_S = 1800


def build_api_client(
    config_method: K8sConfigMethod,
    region: str | None,
    cluster_name: str | None,
    role_name: str | None,
) -> Any | None:
    """Build the k8s API client based on the configuration method and region.
    Returns None for default config method (non-EKS).
    role_name can be an ARN or role name in current account.
    """

    if config_method == K8sConfigMethod.IN_CLUSTER:
        config.load_incluster_config()

        return None
    elif config_method == K8sConfigMethod.LOCAL:
        config.load_kube_config()

        return None
    elif config_method == K8sConfigMethod.EKS_AUTH:
        ca_data, endpoint, token = _eks_auth(cluster_name, region, role_name)
        cafile = _write_cafile(ca_data)
        c = _api_client(endpoint, token, cafile.name)
        return c
    else:
        raise Exception(f"unsupported config method: {config_method}")


def _eks_auth(
    cluster_name: str | None, region: str | None, role_name: str | None
) -> tuple[str, str, str]:
    role_name = role_name or "geneva-client-role"
    region = region or "us-east-1"
    cluster_name = cluster_name or "lancedb"

    _LOG.debug(f"authenticating with EKS. {role_name=}, {region=}, {cluster_name=}")
    # this role requires an EKS Access Entry for the
    # given cluster/namespace and must be assumable
    # by the current principal
    role_arn = _get_role_arn(region, role_name)

    # Get AWS session with assumed role credentials (if role provided)
    aws_session = _get_aws_session_with_role(region, role_arn)
    token = _get_token(cluster_name, role_arn, region, TOKEN_EXPIRATION_S)["status"][
        "token"
    ]

    eks_client = aws_session.client("eks")
    cluster_data = eks_client.describe_cluster(name=cluster_name)["cluster"]
    ca_data = cluster_data["certificateAuthority"]["data"]
    endpoint = cluster_data["endpoint"]
    _LOG.info(f"authenticated with EKS. {cluster_name=} {role_arn=}")

    return ca_data, endpoint, token


def _get_role_arn(region: str, role_name: str | None) -> str | None:
    import boto3

    # default to using current credentials
    role_arn = None
    if role_name:
        # use role ARN if provided
        if role_name.startswith("arn:aws:iam::"):
            role_arn = role_name
        else:
            # if role name is provided, assume it in the current account
            identity = boto3.client("sts", region_name=region).get_caller_identity()
            _LOG.debug("caller identity: %s", identity)
            acct_id = identity.get("Account")
            role_arn = f"arn:aws:iam::{acct_id}:role/{role_name}"

    return role_arn


def _write_cafile(data: str) -> tempfile.NamedTemporaryFile:  # type: ignore[type-arg]
    # ruff: noqa: SIM115
    cafile = tempfile.NamedTemporaryFile(mode="wb", delete=False)
    cadata_b64 = data
    cadata = base64.b64decode(cadata_b64)
    cafile.write(cadata)
    cafile.flush()
    return cafile


def _api_client(endpoint: str, token: str, cafile: str) -> Any:
    kconfig = config.kube_config.Configuration(
        host=endpoint, api_key={"authorization": "Bearer " + token}
    )
    # Set ssl_ca_cert only if the configuration supports it
    if hasattr(kconfig, "ssl_ca_cert"):
        kconfig.ssl_ca_cert = cafile  # type: ignore[assignment]
    kclient = client.ApiClient(configuration=kconfig)
    return kclient


def _get_expiration_time(token_expiration_s: int) -> str:
    token_expiration = datetime.utcnow() + timedelta(seconds=token_expiration_s)
    return token_expiration.strftime("%Y-%m-%dT%H:%M:%SZ")


def _get_exp_s() -> int:
    return TOKEN_EXPIRATION_S


def _get_token(
    cluster_name: str,
    role_arn: str | None,
    region_name: str,
    token_expiration_s: int = _get_exp_s(),
) -> dict:
    from awscli.customizations.eks.get_token import STSClientFactory, TokenGenerator
    from botocore import session

    work_session = session.get_session()
    client_factory = STSClientFactory(work_session)
    sts_client = client_factory.get_sts_client(
        role_arn=role_arn, region_name=region_name
    )

    token = TokenGenerator(sts_client).get_token(cluster_name)
    exp = _get_expiration_time(token_expiration_s)
    _LOG.debug(f"EKS token expiration: {exp}")
    return {
        "kind": "ExecCredential",
        "apiVersion": "client.authentication.k8s.io/v1beta1",
        "spec": {},
        "status": {
            "expirationTimestamp": exp,
            "token": token,
        },
    }


def _get_aws_session_with_role(region_name: str, role_arn: str | None) -> Any:
    """Get AWS session with assumed role if role_arn provided,
    otherwise default session"""
    import boto3

    if role_arn:
        # Assume the role to get temporary credentials
        sts = boto3.client("sts", region_name=region_name)
        assumed_role = sts.assume_role(
            RoleArn=role_arn, RoleSessionName="geneva-session"
        )
        credentials = assumed_role["Credentials"]

        # Create session with assumed role credentials
        return boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
            region_name=region_name,
        )
    else:
        # Use default session when no role is specified
        return boto3.Session(region_name=region_name)
