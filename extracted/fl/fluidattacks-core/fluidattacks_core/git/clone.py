import asyncio
import base64
import json
import logging
import os
import uuid
from pathlib import Path

import aiofiles
import boto3
from botocore.exceptions import ClientError

from .codecommit_utils import (
    extract_region,
)
from .ssh_utils import (
    parse_ssh_url,
)
from .utils import (
    format_url,
)

LOGGER = logging.getLogger(__name__)
MSG = "Repo cloning failed"


async def ssh_clone(
    *,
    branch: str,
    credential_key: str,
    repo_url: str,
    temp_dir: str,
    mirror: bool = False,
) -> tuple[str | None, str | None]:
    parsed_repo_url = parse_ssh_url(repo_url)
    ssh_file_name = Path(f"{temp_dir}/{uuid.uuid4()!s}")
    async with aiofiles.open(
        os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
        "w",
        encoding="utf-8",
    ) as ssh_file:
        await ssh_file.write(base64.b64decode(credential_key).decode())

    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    try:
        proc = await asyncio.create_subprocess_exec(
            "git",
            "clone",
            *(
                ["--mirror"]
                if mirror
                else [
                    "--branch",
                    branch,
                    "--single-branch",
                ]
            ),
            "--",
            parsed_repo_url,
            folder_to_clone_root,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            env={
                **os.environ.copy(),
                "GIT_SSH_COMMAND": (
                    f"ssh -i {ssh_file_name}"
                    " -o UserKnownHostsFile=/dev/null"
                    " -o StrictHostKeyChecking=no"
                    " -o IdentitiesOnly=yes"
                    " -o HostkeyAlgorithms=+ssh-rsa"
                    " -o PubkeyAcceptedAlgorithms=+ssh-rsa"
                ),
            },
            cwd=temp_dir,
        )
        _, stderr = await proc.communicate()
    except OSError as ex:
        LOGGER.exception(ex, extra={"extra": {"branch": branch, "repo": repo_url}})

        return None, str(ex)

    os.remove(ssh_file_name)

    if mirror and proc.returncode == 0:
        with open(f"{folder_to_clone_root}/.info.json", "w") as f:  # noqa: ASYNC230
            json.dump({"fluid_branch": branch, "repo": repo_url}, f)
    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    LOGGER.error(MSG, extra={"extra": {"message": stderr.decode()}})

    return (None, stderr.decode("utf-8"))


async def https_clone(
    *,
    branch: str,
    repo_url: str,
    temp_dir: str,
    password: str | None = None,
    token: str | None = None,
    user: str | None = None,
    provider: str | None = None,
    is_pat: bool = False,
    follow_redirects: bool = False,
    mirror: bool = False,
) -> tuple[str | None, str | None]:
    url = format_url(
        repo_url=repo_url,
        user=user,
        password=password,
        token=token,
        provider=provider,
        is_pat=is_pat,
    )
    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    try:
        proc = await asyncio.create_subprocess_exec(
            "git",
            "-c",
            "http.sslVerify=false",
            "-c",
            f"http.followRedirects={follow_redirects}",
            *(
                [
                    "-c",
                    "http.extraHeader=Authorization: Basic "
                    + base64.b64encode(f":{token}".encode()).decode(),
                ]
                if is_pat
                else []
            ),
            "clone",
            *(
                ["--mirror"]
                if mirror
                else [
                    "--branch",
                    branch,
                    "--single-branch",
                ]
            ),
            "--",
            url,
            folder_to_clone_root,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            cwd=temp_dir,
        )
        _, stderr = await proc.communicate()
    except OSError as ex:
        LOGGER.exception(ex, extra={"extra": {"branch": branch, "repo": repo_url}})

        return None, str(ex)

    if mirror and proc.returncode == 0:
        with open(f"{folder_to_clone_root}/.info.json", "w") as f:  # noqa: ASYNC230
            json.dump({"fluid_branch": branch, "repo": repo_url}, f)

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    LOGGER.error(MSG, extra={"extra": {"message": stderr.decode()}})

    return (None, stderr.decode("utf-8"))


async def codecommit_clone(
    *,
    env: dict[str, str],
    branch: str,
    repo_url: str,
    temp_dir: str,
    mirror: bool = False,
    follow_redirects: bool = False,
) -> tuple[str | None, str | None]:
    folder_to_clone_root = f"{temp_dir}/{uuid.uuid4()}"
    try:
        proc = await asyncio.create_subprocess_exec(
            "git",
            "-c",
            "http.sslVerify=false",
            "-c",
            f"http.followRedirects={follow_redirects}",
            "clone",
            *(
                ["--mirror"]
                if mirror
                else [
                    "--branch",
                    branch,
                    "--single-branch",
                ]
            ),
            "--",
            repo_url,
            folder_to_clone_root,
            cwd=temp_dir,
            env={**os.environ.copy(), **env},
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
    except OSError as ex:
        LOGGER.exception(ex, extra={"extra": {"branch": branch, "repo": repo_url}})

        return None, str(ex)

    if mirror and proc.returncode == 0:
        with open(f"{folder_to_clone_root}/.info.json", "w") as f:  # noqa: ASYNC230
            json.dump({"fluid_branch": branch, "repo": repo_url}, f)

    if proc.returncode == 0:
        return (folder_to_clone_root, None)

    LOGGER.error(MSG, extra={"extra": {"message": stderr.decode()}})

    return (None, stderr.decode("utf-8"))


async def call_codecommit_clone(
    *,
    branch: str,
    repo_url: str,
    temp_dir: str,
    arn: str,
    org_external_id: str,
    follow_redirects: bool = False,
    mirror: bool = False,
) -> tuple[str | None, str | None]:
    try:
        sts_client = boto3.client("sts")
        assumed_role = sts_client.assume_role(
            RoleArn=arn,
            RoleSessionName=f"session-{uuid.uuid4()}",
            ExternalId=org_external_id,
        )
        credentials = assumed_role["Credentials"]

        return await codecommit_clone(
            env={
                "AWS_ACCESS_KEY_ID": credentials["AccessKeyId"],
                "AWS_SECRET_ACCESS_KEY": credentials["SecretAccessKey"],
                "AWS_SESSION_TOKEN": credentials["SessionToken"],
                "AWS_DEFAULT_REGION": extract_region(repo_url),
            },
            branch=branch,
            repo_url=repo_url,
            temp_dir=temp_dir,
            follow_redirects=follow_redirects,
            mirror=mirror,
        )

    except ClientError as exc:
        LOGGER.error(
            MSG,
            extra={
                "extra": {
                    "repo_url": repo_url,
                    "arn": arn,
                    "org_external_id": org_external_id,
                    "exc": exc,
                },
            },
        )

        return None, str(exc)
