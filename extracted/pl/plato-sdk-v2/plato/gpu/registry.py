"""Pull credentials for private images, minted when a pod is created.

A registry pull is a Docker-protocol exchange, not a URL, so there is no
presigned form of it. What there is: a short-lived password the pod creator
mints right before the pod boots and hands to the provider as that pod's own
registry credential, deleted with the pod. For ECR that is
``GetAuthorizationToken`` (12 h), called with the same AWS credentials the
bucket uses, which must also allow ``ecr:GetAuthorizationToken`` and
``ecr:BatchGetImage`` on the repository.
"""

from __future__ import annotations

import asyncio
import base64
import re
import subprocess
from collections.abc import Awaitable, Callable
from typing import Protocol, cast

import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel

from plato.gpu.providers.base import RegistryCredential
from plato.gpu.settings import GpuSettings

_ECR_HOST = re.compile(r"^(?P<account>\d{12})\.dkr\.ecr\.(?P<region>[a-z0-9-]+)\.amazonaws\.com/")
_ECR_IMAGE = re.compile(
    r"^(?P<registry>(?P<account>\d{12})\.dkr\.ecr\.(?P<region>[a-z0-9-]+)\.amazonaws\.com)/"
    r"(?P<repository>[a-z0-9][a-z0-9._/-]*?)(?::(?P<tag>[^:@]+))?(?:@sha256:[0-9a-f]{64})?$"
)


class EcrImage(BaseModel):
    """An image reference on ECR, split: ``<account>.dkr.ecr.<region>.amazonaws.com/<repository>:<tag>``."""

    registry: str
    account: str
    region: str
    repository: str
    tag: str


def ecr_image(image: str) -> EcrImage | None:
    match = _ECR_IMAGE.match(image)
    if match is None:
        return None
    return EcrImage(
        registry=match.group("registry"),
        account=match.group("account"),
        region=match.group("region"),
        repository=match.group("repository"),
        tag=match.group("tag") or "latest",
    )


class EcrClient(Protocol):
    """What this module uses of boto3's ECR client; tests pass a fake."""

    def describe_repositories(self, *, registryId: str, repositoryNames: list[str]) -> object: ...
    def create_repository(self, *, registryId: str, repositoryName: str) -> object: ...
    def get_authorization_token(self) -> dict[str, list[dict[str, str]]]: ...


def _ecr_client(region: str, settings: GpuSettings) -> EcrClient:
    # boto3 builds clients at runtime; the stub types them as a bare BaseClient.
    return cast(
        EcrClient,
        boto3.client(
            "ecr",
            region_name=region,
            aws_access_key_id=settings.aws_access_key_id or None,
            aws_secret_access_key=settings.aws_secret_access_key or None,
            aws_session_token=settings.aws_session_token or None,
        ),
    )


def _code(error: ClientError) -> str:
    return str(error.response.get("Error", {}).get("Code", ""))


def _decode(token: str) -> RegistryCredential:
    username, _, password = base64.b64decode(token).decode().partition(":")
    return RegistryCredential(username=username, password=password)


Runner = Callable[..., subprocess.CompletedProcess[bytes]]


def push_to_ecr(
    image: str,
    *,
    source: str | None = None,
    settings: GpuSettings,
    run: Runner | None = None,
    client: EcrClient | None = None,
) -> EcrImage:
    """``docker push`` a local image to ECR with the caller's own AWS
    credentials, creating the repository when it is missing. ``source`` is
    the local image to tag as ``image`` first (default: ``image`` is already
    tagged locally). Raises :class:`ValueError` for a non-ECR reference,
    :class:`RuntimeError` when docker refuses."""

    target = ecr_image(image)
    if target is None:
        raise ValueError(
            f"{image} is not an ECR image; --push handles <account>.dkr.ecr.<region>.amazonaws.com/... only"
        )
    ecr = client or _ecr_client(target.region, settings)
    # registryId: the image's account, which the credentials may only be
    # allowed to push into (never the credentials' own account by default).
    try:
        ecr.describe_repositories(registryId=target.account, repositoryNames=[target.repository])
    except ClientError as error:
        if _code(error) != "RepositoryNotFoundException":
            raise
        try:
            ecr.create_repository(registryId=target.account, repositoryName=target.repository)
        except ClientError as race:
            # Another push created it between the two calls: the repository is there either way.
            if _code(race) != "RepositoryAlreadyExistsException":
                raise
    login = _decode(ecr.get_authorization_token()["authorizationData"][0]["authorizationToken"])
    steps: list[tuple[list[str], bytes | None]] = [
        (
            ["docker", "login", "--username", login.username, "--password-stdin", target.registry],
            login.password.encode(),
        ),
    ]
    if source and source != image:
        steps.append((["docker", "tag", source, image], None))
    steps.append((["docker", "push", image], None))
    for argv, stdin in steps:
        done = (run or subprocess.run)(argv, input=stdin, capture_output=True)
        if done.returncode != 0:
            # docker's own words, never the password (it went in on stdin).
            raise RuntimeError(f"{' '.join(argv[:2])} failed: {done.stderr.decode(errors='replace').strip()}")
    return target


def _ecr_token(region: str, settings: GpuSettings) -> RegistryCredential:
    client = _ecr_client(region, settings)
    return _decode(client.get_authorization_token()["authorizationData"][0]["authorizationToken"])


async def pull_credential(image: str, settings: GpuSettings) -> RegistryCredential | None:
    """A fresh credential for ``image`` when its registry is one this module
    can mint for (ECR); None otherwise, leaving the provider's stored
    credential (``runpod_registry_auth_id``) or a public pull."""

    match = _ECR_HOST.match(image)
    if match is None:
        return None
    return await asyncio.to_thread(_ecr_token, match.group("region"), settings)


PullCredential = Callable[[str, GpuSettings], Awaitable[RegistryCredential | None]]
