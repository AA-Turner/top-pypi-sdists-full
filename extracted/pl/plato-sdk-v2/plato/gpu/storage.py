"""The bucket GPU work moves through, as presigned URLs.

A worker or a pod never holds a credential: it gets one presigned GET per
input and one presigned PUT per output, hours long at most. The client with
the credentials is this process, and it signs; it reads the bucket only to
check an upload landed and to fetch what a worker wrote.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

import boto3
from botocore.config import Config

from plato.gpu.settings import GpuSettings

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


class StorageError(RuntimeError):
    """The bucket refused or failed a request for a reason other than a
    missing object; carries the service's error code."""


class ObjectStore(Protocol):
    """One bucket: sign grants for one object at a time."""

    def presign_get(self, key: str, ttl_seconds: int) -> str: ...

    def presign_put(self, key: str, ttl_seconds: int, content_type: str = "") -> str: ...


class S3Store:
    """An S3 bucket, signed against its regional endpoint (the global one
    307-redirects for a new bucket, and a presigned PUT cannot follow)."""

    def __init__(self, settings: GpuSettings) -> None:
        if not settings.bucket:
            raise StorageError("no bucket configured")
        self.bucket = settings.bucket
        self._client: S3Client = boto3.client(
            "s3",
            region_name=settings.region,
            endpoint_url=f"https://s3.{settings.region}.amazonaws.com",
            config=Config(signature_version="s3v4"),
            aws_access_key_id=settings.aws_access_key_id or None,
            aws_secret_access_key=settings.aws_secret_access_key or None,
            aws_session_token=settings.aws_session_token or None,
        )

    def presign_get(self, key: str, ttl_seconds: int) -> str:
        return self._client.generate_presigned_url(
            "get_object", Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=ttl_seconds
        )

    def presign_put(self, key: str, ttl_seconds: int, content_type: str = "") -> str:
        params: dict[str, str] = {"Bucket": self.bucket, "Key": key}
        if content_type:
            params["ContentType"] = content_type
        return self._client.generate_presigned_url("put_object", Params=params, ExpiresIn=ttl_seconds)
