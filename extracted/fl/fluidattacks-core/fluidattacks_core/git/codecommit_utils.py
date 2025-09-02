import asyncio
import logging
import os
import re
import uuid

import boto3
from botocore.exceptions import (
    ClientError,
)

LOGGER = logging.getLogger(__name__)


def extract_region(url: str) -> str:
    pattern = r"codecommit::([a-z0-9-]+)://"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return "us-east-1"


async def assume_role_and_execute_git_ls_remote(
    arn: str,
    repo_url: str,
    branch: str,
    org_external_id: str,
    *,
    follow_redirects: bool = False,
) -> tuple[str | None, str | None]:
    try:
        sts_client = boto3.client("sts")
        assumed_role = sts_client.assume_role(
            RoleArn=arn,
            RoleSessionName=f"session-{uuid.uuid4()}",
            ExternalId=org_external_id,
        )
        credentials = assumed_role["Credentials"]

        return await codecommit_ls_remote(
            env={
                "AWS_ACCESS_KEY_ID": credentials["AccessKeyId"],
                "AWS_SECRET_ACCESS_KEY": credentials["SecretAccessKey"],
                "AWS_SESSION_TOKEN": credentials["SessionToken"],
                "AWS_DEFAULT_REGION": extract_region(repo_url),
            },
            branch=branch,
            repo_url=repo_url,
            follow_redirects=follow_redirects,
        )

    except ClientError as exc:
        err_message = "Error executing ls-remote with codecommit"
        LOGGER.exception(
            err_message,
            extra={
                "extra": {
                    "repo_url": repo_url,
                    "arn": arn,
                    "org_external_id": org_external_id,
                    "exc": exc,
                },
            },
        )

        return None, err_message


async def _execute_git_command(
    *,
    branch: str,
    env: dict[str, str],
    url: str,
    follow_redirects: bool = False,
) -> tuple[bytes, bytes, int | None]:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-c",
        "http.sslVerify=false",
        "-c",
        f"http.followRedirects={follow_redirects}",
        "ls-remote",
        "--",
        url,
        branch,
        env={**os.environ.copy(), **env},
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), 20)

    return stdout, stderr, proc.returncode


async def codecommit_ls_remote(
    *,
    branch: str,
    env: dict[str, str],
    repo_url: str,
    follow_redirects: bool = False,
) -> tuple[str | None, str | None]:
    try:
        stdout, stderr, return_code = await _execute_git_command(
            branch=branch,
            env=env,
            follow_redirects=follow_redirects,
            url=repo_url,
        )
    except asyncio.exceptions.TimeoutError:
        return None, "git ls-remote time out"

    if return_code == 0:
        return stdout.decode().split("\t")[0], None

    return None, stderr.decode("utf-8")


async def call_codecommit_ls_remote(
    repo_url: str,
    arn: str,
    branch: str,
    org_external_id: str,
    *,
    follow_redirects: bool = False,
) -> tuple[str | None, str | None]:
    return await assume_role_and_execute_git_ls_remote(
        repo_url=repo_url,
        arn=arn,
        branch=branch,
        org_external_id=org_external_id,
        follow_redirects=follow_redirects,
    )
