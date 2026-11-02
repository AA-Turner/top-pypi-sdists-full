"""The DAG bucket, reached with the environment's long-lived deployment key.

Credentials come only from ``AWS_ACCESS_KEY_ID`` / ``AWS_SECRET_ACCESS_KEY``
(and ``AWS_SESSION_TOKEN`` if set), never from ``~/.aws`` or a login, so a
deploy uses exactly the key CI was given or fails saying so.
"""

from __future__ import annotations

import contextlib
import hashlib
import os
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from databaas_utils.dags.layout import PREFIX_PATTERN
from databaas_utils.errors import ConfigurationError, LakehouseError
from databaas_utils.profiles import DEFAULT_REGION

ACCESS_KEY_VAR = "AWS_ACCESS_KEY_ID"
SECRET_KEY_VAR = "AWS_SECRET_ACCESS_KEY"
SESSION_TOKEN_VAR = "AWS_SESSION_TOKEN"
ENDPOINT_VARS = ("AWS_ENDPOINT_URL_S3", "AWS_ENDPOINT_URL")
REGION_VARS = ("AWS_REGION", "AWS_DEFAULT_REGION")
BUCKET_VAR = "DATABAAS_DAGS_BUCKET"
_DELETE_BATCH = 1000
_CHUNK = 1024 * 1024
_FORBIDDEN = ("AccessDenied", "403", "InvalidAccessKeyId", "SignatureDoesNotMatch")


class DagBucketError(LakehouseError):
    """S3 refused or failed a request to the DAG bucket."""


@contextlib.contextmanager
def _s3_errors(action: str, bucket: str, key: str) -> Iterator[None]:
    """Turn botocore failures into a `DagBucketError` naming what was attempted."""
    from botocore.exceptions import BotoCoreError, ClientError

    try:
        yield
    except ClientError as exc:
        error = exc.response.get("Error", {})
        code = str(error.get("Code", ""))
        hint = ""
        if code in _FORBIDDEN:
            hint = (
                " — check that the key is this environment's DAG deployment key and "
                "that the bucket and endpoint belong to the same environment"
            )
        raise DagBucketError(
            f"could not {action} s3://{bucket}/{key}: {code} {error.get('Message', '')}"
            f"{hint}"
        ) from exc
    except BotoCoreError as exc:
        raise DagBucketError(f"could not {action} s3://{bucket}/{key}: {exc}") from exc


def _missing_key_message(source: Mapping[str, str]) -> str:
    states = []
    for name in (ACCESS_KEY_VAR, SECRET_KEY_VAR):
        if source.get(name):
            continue
        states.append(f"{name} is {'empty' if name in source else 'not set'}")
    message = (
        "deploying DAGs needs the environment's DAG deployment key in "
        f"{ACCESS_KEY_VAR} and {SECRET_KEY_VAR}, but {' and '.join(states)}."
    )
    lookalikes = sorted(
        name
        for name in source
        if name not in (ACCESS_KEY_VAR, SECRET_KEY_VAR)
        and name.startswith(("AWS_", "SCW_"))
        and ("ACCESS" in name or "SECRET" in name)
    )
    if lookalikes:
        message += (
            f" Found {', '.join(lookalikes)}; only {ACCESS_KEY_VAR} and "
            f"{SECRET_KEY_VAR} are read."
        )
    return (
        message + " CI gets the key from repository secrets; deploying with your own "
        "`databaas login` is not available yet."
    )


@dataclass(frozen=True)
class DagBucket:
    """Where and as whom to deploy.

    Attributes:
        bucket: The environment's metadata bucket.
        endpoint_url: The S3 endpoint, e.g. ``https://s3.nl-ams.scw.cloud``.
        region: Signing region.
        access_key_id: The DAG deployment key's id.
        secret_access_key: Its secret.
        session_token: Optional session token.
    """

    bucket: str
    endpoint_url: str
    region: str
    access_key_id: str
    secret_access_key: str
    session_token: str = ""

    def __repr__(self) -> str:
        """Leaves the secret out."""
        return (
            f"DagBucket(bucket={self.bucket!r}, endpoint_url={self.endpoint_url!r}, "
            f"region={self.region!r}, access_key_id={self.access_key_id!r})"
        )

    @classmethod
    def from_env(
        cls,
        env: Mapping[str, str] | None = None,
        *,
        bucket: str | None = None,
        endpoint_url: str | None = None,
    ) -> DagBucket:
        """Read the key, endpoint, region and bucket from the environment.

        Args:
            env: Variables to read instead of ``os.environ``.
            bucket: Overrides ``DATABAAS_DAGS_BUCKET``.
            endpoint_url: Overrides ``AWS_ENDPOINT_URL_S3`` / ``AWS_ENDPOINT_URL``.

        Raises:
            ConfigurationError: If the key, the endpoint or the bucket is missing.
        """
        source = env if env is not None else os.environ
        access, secret = source.get(ACCESS_KEY_VAR), source.get(SECRET_KEY_VAR)
        if not access or not secret:
            raise ConfigurationError(_missing_key_message(source))
        endpoint = endpoint_url or next(
            (source[v] for v in ENDPOINT_VARS if source.get(v)), ""
        )
        if not endpoint:
            raise ConfigurationError(
                "set AWS_ENDPOINT_URL (e.g. https://s3.nl-ams.scw.cloud) or pass "
                "--endpoint-url"
            )
        name = bucket or source.get(BUCKET_VAR)
        if not name:
            raise ConfigurationError(f"set {BUCKET_VAR} or pass --bucket")
        region = next((source[v] for v in REGION_VARS if source.get(v)), DEFAULT_REGION)
        return cls(
            bucket=name,
            endpoint_url=endpoint,
            region=region,
            access_key_id=access,
            secret_access_key=secret,
            session_token=source.get(SESSION_TOKEN_VAR, ""),
        )

    def client(self) -> Any:
        """A boto3 S3 client for this bucket's endpoint, as the deployment key.

        Raises:
            ConfigurationError: If boto3 is not installed.
        """
        try:
            import boto3
        except ImportError as exc:
            raise ConfigurationError(
                "deploying DAGs needs boto3 — install databaas-utils[deploy]"
            ) from exc
        return boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            region_name=self.region,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            aws_session_token=self.session_token or None,
        )


@dataclass(frozen=True)
class RemoteObject:
    """An object under a target's prefix."""

    key: str
    size: int
    etag: str


@dataclass(frozen=True)
class SyncPlan:
    """What a sync uploads, skips and deletes, by key."""

    upload: tuple[str, ...]
    unchanged: tuple[str, ...]
    delete: tuple[str, ...]


def _check_prefix(prefix: str) -> None:
    if not PREFIX_PATTERN.fullmatch(prefix):
        raise ConfigurationError(f"refusing {prefix!r}: not in the dags/ layout")


def list_objects(client: Any, bucket: str, prefix: str) -> Iterator[RemoteObject]:
    """Every object under `prefix`."""
    _check_prefix(prefix)
    kwargs: dict[str, Any] = {"Bucket": bucket, "Prefix": prefix}
    while True:
        with _s3_errors("list", bucket, prefix):
            page = client.list_objects_v2(**kwargs)
        for item in page.get("Contents", []):
            yield RemoteObject(
                key=item["Key"], size=int(item["Size"]), etag=item["ETag"].strip('"')
            )
        if not page.get("IsTruncated"):
            return
        kwargs["ContinuationToken"] = page["NextContinuationToken"]


def _md5(path: Path) -> str:
    # Compared with the ETag S3 gives a single-part upload; not for security.
    digest = hashlib.md5()
    with path.open("rb") as handle:
        while chunk := handle.read(_CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def plan_sync(
    files: Mapping[str, Path], remote: Mapping[str, RemoteObject], prefix: str
) -> SyncPlan:
    """Compare local files (by relative path) with the objects under `prefix`.

    A file is unchanged when an object of the same size has its MD5 as ETag,
    which holds for every single-part upload; anything else is uploaded.
    """
    upload, unchanged = [], []
    for relative, path in sorted(files.items()):
        key = prefix + relative
        existing = remote.get(key)
        if (
            existing is not None
            and existing.size == path.stat().st_size
            and existing.etag == _md5(path)
        ):
            unchanged.append(key)
        else:
            upload.append(key)
    wanted = {prefix + relative for relative in files}
    stale = sorted(key for key in remote if key not in wanted)
    return SyncPlan(tuple(upload), tuple(unchanged), tuple(stale))


def upload(client: Any, bucket: str, key: str, path: Path) -> None:
    """Upload `path` as one part, so its ETag stays its MD5."""
    with path.open("rb") as body, _s3_errors("upload", bucket, key):
        client.put_object(Bucket=bucket, Key=key, Body=body)


def delete(client: Any, bucket: str, keys: tuple[str, ...], prefix: str) -> None:
    """Delete `keys`, all of which must be under `prefix`.

    Raises:
        ConfigurationError: If a key is outside `prefix`.
        DagBucketError: If S3 refuses the request or a key could not be deleted.
    """
    _check_prefix(prefix)
    outside = [key for key in keys if not key.startswith(prefix)]
    if outside:
        raise ConfigurationError(f"refusing to delete outside {prefix}: {outside[:3]}")
    for start in range(0, len(keys), _DELETE_BATCH):
        batch = keys[start : start + _DELETE_BATCH]
        with _s3_errors("delete under", bucket, prefix):
            response = client.delete_objects(
                Bucket=bucket,
                Delete={"Objects": [{"Key": key} for key in batch], "Quiet": True},
            )
        errors = response.get("Errors") or []
        if errors:
            first = errors[0]
            raise DagBucketError(
                f"could not delete {len(errors)} object(s), e.g. {first.get('Key')}: "
                f"{first.get('Code')} {first.get('Message')}"
            )
