"""Corvic system protocols for interacting with storage."""

from __future__ import annotations

import contextlib
import io
import uuid
from collections.abc import Iterator
from typing import Any, Literal

from typing_extensions import Protocol

from corvic.result import Error, Ok


class DataMisplacedError(Error):
    """Raised when assumptions about data's storage location are violated."""


class BlobClient(Protocol):
    """A Client is the front door for blob store resources."""

    def blob_from_url(self, url: str) -> Blob: ...

    def bucket(self, name: str) -> Bucket: ...


class Blob(Protocol):
    """A Blob is a blob store object that may or may not exist.

    Interface is a subset of google.cloud.storage.Blob's interface
    """

    @property
    def name(self) -> str: ...

    @property
    def physical_name(self) -> str:
        """The name of the blob as stored for cases where it differs from the name."""
        ...

    @property
    def bucket(self) -> Bucket: ...

    @property
    def size(self) -> int | None: ...

    @property
    def md5_hash(self) -> str | None: ...

    @property
    def metadata(self) -> dict[str, Any]: ...

    @metadata.setter
    def metadata(self, value: dict[str, Any]) -> None: ...

    @property
    def content_type(self) -> str: ...

    @content_type.setter
    def content_type(self, value: str) -> None: ...

    def patch(self) -> None: ...

    def reload(self) -> None: ...

    def exists(self) -> bool: ...

    def create_resumable_upload_session(
        self, content_type: str, origin: str | None = None, size: int | None = None
    ) -> str: ...

    @property
    def url(self) -> str: ...

    @contextlib.contextmanager
    def open(
        self, mode: Literal["rb", "wb"], **kwargs: Any
    ) -> Iterator[io.BytesIO]: ...

    def delete(self) -> None: ...

    def upload_from_string(
        self, data: bytes | str, content_type: str = "text/plain"
    ) -> None: ...

    def generate_signed_url(self, expiration: int) -> str: ...


class Bucket(Protocol):
    """A Bucket is a blob store container for objects.

    Interface is a subset of google.cloud.storage.Bucket's interface.
    """

    @property
    def name(self) -> str: ...

    def blob(self, name: str) -> Blob: ...

    def exists(self) -> bool: ...

    def create(self) -> None: ...

    def list_blobs(self) -> Iterator[Blob]: ...


class DataKindManager:
    """Manages the names of blobs that corvic stores for a particular data kind.

    Kinds are managaged by the NamespaceManager
    """

    def __init__(self, storage_manager: StorageManager, prefix: str):
        if prefix.endswith("/"):
            raise ValueError("prefix should not end with a path separator (/)")
        self._namespace_manager = storage_manager
        self._prefix = prefix

    @property
    def prefix(self):
        return self._prefix

    def make_anonymous_table_url(self):
        return self.blob(f"annonymous_tables/{uuid.uuid4()}.parquet").url

    def blob(self, blob_name: str):
        return self._namespace_manager.bucket.blob(f"{self.prefix}/{blob_name}")

    def _blob_from_url(self, url: str) -> Ok[Blob] | DataMisplacedError:
        blob = self._namespace_manager.blob_from_url(url)
        if self._namespace_manager.bucket.name != blob.bucket.name:
            return DataMisplacedError(
                "data stored at a different bucket than expected",
                url=url,
                expected_bucket=self._namespace_manager.bucket.name,
            )
        if not blob.name.startswith(self._prefix):
            return DataMisplacedError(
                "data stored at a different prefix than expected",
                url=url,
                expected_prefix=self._prefix,
            )
        return Ok(blob)

    def blob_name_from_url(self, url: str) -> Ok[str] | DataMisplacedError:
        def _to_name(blob: Blob) -> str:
            return blob.name.removeprefix(self._prefix + "/")

        return self._blob_from_url(url=url).map(_to_name)


class StorageManager:
    """Manages the names of blobs that corvic stores."""

    _blob_client: BlobClient
    _bucket_name: str
    _unstructured_manager: DataKindManager
    _tabular_manager: DataKindManager
    _space_run_manager: DataKindManager
    _vector_manager: DataKindManager

    def __init__(
        self,
        blob_client: BlobClient,
        *,
        bucket_name: str,
        unstructured_prefix: str,
        tabular_prefix: str,
        space_run_prefix: str,
        vector_prefix: str,
    ):
        self._blob_client = blob_client
        self._bucket_name = bucket_name

        self._unstructured_manager = DataKindManager(self, unstructured_prefix)
        self._tabular_manager = DataKindManager(self, tabular_prefix)
        self._space_run_manager = DataKindManager(self, space_run_prefix)
        self._vector_manager = DataKindManager(self, vector_prefix)

    def blob_from_url(self, url: str):
        return self._blob_client.blob_from_url(url)

    @property
    def bucket(self) -> Bucket:
        return self._blob_client.bucket(self._bucket_name)

    @property
    def tabular(self):
        return self._tabular_manager

    @property
    def unstructured(self):
        return self._unstructured_manager

    @property
    def space_run(self):
        return self._space_run_manager

    @property
    def vector(self):
        return self._vector_manager
