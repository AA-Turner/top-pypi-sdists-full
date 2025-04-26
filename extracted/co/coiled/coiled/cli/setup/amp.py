import json
from typing import List, Optional

import boto3
import click
from rich import print

from ..utils import CONTEXT_SETTINGS


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--name",
    default="Coiled",
    help="Name of the AMP workspace to create",
)
@click.option(
    "--region",
    default=None,
    help="Region of the AMP workspace to create (doesn't need to match region of cluster sending metrics)",
)
@click.option(
    "--make-creds",
    default=None,
    type=click.Choice(["read", "write", "both"], case_sensitive=False),
    help="Make access key, options are read/write/both or unspecified (don't make access keys)",
)
@click.option(
    "--profile",
    default=None,
    envvar="AWS_PROFILE",
    help="AWS profile to use from your local AWS credentials file",
)
def aws_amp_setup(
    name: str,
    region: Optional[str],
    make_creds: Optional[str],
    profile: Optional[str],
):
    make_prometheus_workspace_and_creds(name=name, region=region, make_creds=make_creds, profile=profile, verbose=True)


def make_prometheus_workspace_and_creds(
    name: str,
    region: Optional[str],
    make_creds: Optional[str],
    profile: Optional[str],
    verbose: bool = False,
):
    created_info = {}

    session = boto3.Session(profile_name=profile, region_name=region)
    iam = session.client("iam")
    sts = session.client("sts")

    identity = sts.get_caller_identity()
    account = identity.get("Account")

    amp_arn, workspace_id = make_amp_workspace(session, name, region)

    api_endpoint = f"https://aps-workspaces.{region}.amazonaws.com/workspaces/{workspace_id}"
    created_info["api_endpoint"] = api_endpoint
    created_info["amp_region"] = region

    do_write_setup = False
    do_read_setup = False

    if make_creds:
        if make_creds in ("write", "both"):
            do_write_setup = True
        if make_creds in ("read", "both"):
            do_read_setup = True

    if do_write_setup:
        key, secret = setup_auth(
            user_policy_name=f"PrometheusWrite-{name}",
            policy_doc_func=amp_write_policy_doc,
            amp_arn=amp_arn,
            iam=iam,
            account=account,
        )

        write_auth = {"sigv4": {"region": region, "access_key": key, "secret_key": secret}}
        created_info["write_auth"] = write_auth

        if verbose:
            print(f"Endpoint:\t{api_endpoint}")
            print(json.dumps(write_auth))

    if do_read_setup:
        key, secret = setup_auth(
            user_policy_name=f"PrometheusRead-{name}",
            policy_doc_func=amp_read_policy_doc,
            amp_arn=amp_arn,
            iam=iam,
            account=account,
        )

        created_info["amp_read_access_key_id"] = key
        created_info["amp_read_secret_access_key"] = secret

        if verbose:
            print(f"Endpoint:\t{api_endpoint}")
            print(f"Region:\t{region}")
            print(f"Access Key:\t{key}")
            print(f"Secret Key:\t{secret}")

    return created_info


def setup_auth(user_policy_name, policy_doc_func, amp_arn, iam, account):
    from .aws import (
        attach_user_policy,
        create_or_update_policy,
        create_user,
        make_access_key,
    )

    create_user(iam, user_policy_name, track=False)
    policy_arn = create_or_update_policy(iam, account, user_policy_name, policy_doc_func([amp_arn]), track=False)
    attach_user_policy(iam, user_policy_name, policy_arn, track=False)
    return make_access_key(iam, user_policy_name, track=False)


def make_amp_workspace(session, name, region):
    amp = session.client("amp")

    # check for existing workspace matching the name
    result = None
    existing = amp.list_workspaces().get("workspaces", [])
    for workspace in existing:
        if workspace["alias"] == name:
            result = workspace
            break

    if not result:
        result = amp.create_workspace(alias=name)

    workspace_id = result["workspaceId"]

    return result["arn"], workspace_id


def amp_write_policy_doc(workspace_arns: List[str]) -> str:
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "CoiledPrometheusWrite",
                "Effect": "Allow",
                "Action": ["aps:RemoteWrite"],
                "Resource": workspace_arns,
            }
        ],
    }
    return json.dumps(policy)


def amp_read_policy_doc(workspace_arns: List[str]) -> str:
    # actions match AmazonPrometheusQueryAccess, but scoped to specific workspace
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "CoiledPrometheusRead",
                "Effect": "Allow",
                "Action": [
                    "aps:GetLabels",
                    "aps:GetMetricMetadata",
                    "aps:GetSeries",
                    "aps:QueryMetrics",
                ],
                "Resource": workspace_arns,
            }
        ],
    }
    return json.dumps(policy)
