"""Blob store backed by a local directory."""

from __future__ import annotations

import base64
import contextlib
import copy
import dataclasses
import hashlib
import io
import json
import os
import re
import tempfile
import urllib.parse
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Literal, cast


def _url_to_bucket_blob(url: str) -> tuple[str, str]:
    match = re.match(r"gs://([^/]+)/(.*)", url)
    if not match:
        raise ValueError("URL was malformed")

    if not match.group(1):
        raise ValueError("Bucket cannot be empty")

    if not match.group(2):
        raise ValueError("Object name cannot be empty")

    bucket = match.group(1)
    obj_name = match.group(2)

    return bucket, obj_name


def _upload_url_to_bucket_blob(url: str) -> tuple[str, str]:
    match = re.match(r"https?://([^/]+)/(.*)", url)
    if not match:
        raise ValueError("upload url was malformed")
    return match.group(1), urllib.parse.unquote_plus(match.group(2))


@dataclasses.dataclass
class BlobMetadata:
    """Data about blobs."""

    user_metadata: dict[str, Any] = dataclasses.field(default_factory=dict)
    content_type: str = ""
    md5_hash: str | None = None
    size: int | None = None


class FSBlob:
    """Maps the blob interface to the file system."""

    _bucket: FSBucket
    _name: str
    _metadata: BlobMetadata

    def __init__(self, bucket: FSBucket, name: str):
        self._bucket = bucket
        self._name = name
        self._metadata = BlobMetadata()

    @property
    def client(self):
        return self._bucket.client

    @property
    def name(self) -> str:
        return self._name

    @property
    def bucket(self) -> FSBucket:
        return self._bucket

    @property
    def size(self) -> int | None:
        return self._metadata.size

    @property
    def md5_hash(self) -> str | None:
        return self._metadata.md5_hash

    @property
    def metadata(self) -> dict[str, Any]:
        return copy.deepcopy(self._metadata.user_metadata)

    @metadata.setter
    def metadata(self, value: dict[str, Any]) -> None:
        self._metadata.user_metadata.update(value)

    @property
    def content_type(self) -> str:
        return self._metadata.content_type

    @content_type.setter
    def content_type(self, value: str) -> None:
        self._metadata.content_type = value

    @classmethod
    def from_path(cls, bucket: FSBucket, path: Path) -> FSBlob:
        return FSBlob(
            bucket, base64.urlsafe_b64decode(path.name.encode("utf-8")).decode("utf-8")
        )

    @property
    def physical_name(self) -> str:
        return base64.urlsafe_b64encode(self.name.encode("utf-8")).decode("utf-8")

    def path(self) -> Path:
        return self._bucket.path() / self.physical_name

    def metadata_path(self) -> Path:
        content_path = self.path()
        return content_path.parent / (content_path.name + ".metadata")

    def _load_metadata(self) -> BlobMetadata:
        metadata_path = self.metadata_path()
        if not metadata_path.exists():
            return BlobMetadata()
        with metadata_path.open("r") as stream:
            return BlobMetadata(**json.load(stream))

    def _store_metadata(self) -> None:
        metadata_path = self.metadata_path()
        with tempfile.NamedTemporaryFile(mode="w", dir=self._bucket.path()) as stream:
            json.dump(dataclasses.asdict(self._metadata), stream)
            metadata_path.unlink(missing_ok=True)
            os.link(stream.name, metadata_path)

    def patch(self) -> None:
        metadata = self._load_metadata()
        if self.content_type:
            metadata.content_type = self.content_type = self.content_type
        if self.md5_hash is not None:
            metadata.md5_hash = self.md5_hash
        if self.size is not None:
            metadata.size = self.size

        metadata.user_metadata.update(self._metadata.user_metadata)
        self._metadata = metadata
        self._store_metadata()

    def reload(self) -> None:
        self._metadata = self._load_metadata()

    def exists(self) -> bool:
        return self.path().exists()

    def create_resumable_upload_session(
        self, content_type: str, origin: str | None = None, size: int | None = None
    ) -> str:
        if content_type:
            self._metadata.content_type = content_type
        self._store_metadata()
        return self.client.bucket_blob_to_upload_url(self._bucket.name, self.name)

    @property
    def url(self) -> str:
        return f"gs://{self._bucket.name}/{self.name}"

    @contextlib.contextmanager
    def open(self, mode: Literal["rb", "wb"], **kwargs: Any) -> Iterator[io.BytesIO]:
        content_path = self.path()
        content_type = kwargs.get("content_type", "")
        if mode == "rb" and content_type:
            raise ValueError("cannot set content_type on read operation")
        with content_path.open(mode=mode) as stream:
            # TODO(thunt): The type for open in the protocol should really be
            # "IO[bytes]" but polars is strict about this type so avoiding the cast
            # here would involve more invasive changes. Faking it has worked out well
            # so far; i.e., system_gcs also does an ugly cast like this. We should
            # address this soon.
            yield cast(io.BytesIO, stream)

        if mode == "wb":
            if content_type:
                self.content_type = content_type

            with content_path.open(mode="rb") as stream:
                self._metadata.md5_hash = hashlib.md5(stream.read()).hexdigest()
            self._metadata.size = content_path.stat().st_size
            self.patch()

    def delete(self) -> None:
        self.metadata_path().unlink()
        self.path().unlink()

    def upload_from_string(
        self, data: bytes | str, content_type: str = "text/plain"
    ) -> None:
        if isinstance(data, str):
            data = data.encode()
        with self.open("wb", content_type=content_type) as stream:
            stream.write(data)

    def generate_signed_url(self, expiration: int) -> str:
        return f"http://{self._bucket.name}/{self.name}"


class FSBucket:
    """Maps the bucket interface to the local filesystem."""

    _client: FSBlobClient
    _name: str

    def __init__(self, client: FSBlobClient, name: str):
        self._client = client
        self._name = name

    @property
    def client(self):
        return self._client

    @property
    def name(self) -> str:
        return self._name

    def blob(self, name: str) -> FSBlob:
        return FSBlob(name=name, bucket=self)

    def exists(self) -> bool:
        return self.path().exists()

    def create(self) -> None:
        return self.path().mkdir()

    def list_blobs(self) -> Iterator[FSBlob]:
        for entry in self.path().glob("*"):
            if not entry.name.endswith(".metadata"):
                yield FSBlob.from_path(self, entry)

    def path(self) -> Path:
        return self.client.root() / self.name


class FSBlobClient:
    """A Client is the front door for blob store resources."""

    _root: Path

    def __init__(self, root: Path):
        root.mkdir(exist_ok=True)
        self._root = root

    def blob_from_url(self, url: str) -> FSBlob:
        bucket_name, blob_name = _url_to_bucket_blob(url)
        bucket = self.bucket(bucket_name)
        return bucket.blob(blob_name)

    def blob_from_signed_url(self, url: str) -> FSBlob:
        bucket_name, blob_name = _upload_url_to_bucket_blob(url)
        bucket = self.bucket(bucket_name)
        return bucket.blob(blob_name)

    def bucket(self, name: str) -> FSBucket:
        return FSBucket(client=self, name=name)

    def root(self):
        return self._root

    def http_put(self, url: str, content: bytes) -> None:
        bucket_name, blob_name = _upload_url_to_bucket_blob(url)
        bucket = self.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        with blob.open("wb") as stream:
            stream.write(content)

    @staticmethod
    def bucket_blob_to_upload_url(bucket: str, blob: str) -> str:
        return f"http://{bucket}/{urllib.parse.quote_plus(blob)}"
