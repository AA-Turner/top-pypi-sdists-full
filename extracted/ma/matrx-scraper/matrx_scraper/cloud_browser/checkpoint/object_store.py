"""Object-store seam and an in-memory test stub (S3 §2.3, §9.4).

The engine speaks a tiny versioned object-store protocol — enough for
put / get(-stream) / head / delete(-version) / list-prefix — so it runs against
real S3, MinIO/localstack, or the :class:`InMemoryObjectStore` used by WS-3
standalone tests with no AWS account.

``object_ref`` is ``s3://<bucket>/<key>`` and is SERVER-ONLY: never a URL, never
signed, never returned to a client. The engine emits only refs and hashes; a test
asserts ``is_signed_url`` is never True over anything it emits.
"""

from __future__ import annotations

import io
from dataclasses import dataclass, field
from typing import BinaryIO, Iterator, Protocol, runtime_checkable


@dataclass(frozen=True)
class ObjectRef:
    """A parsed ``s3://<bucket>/<key>`` reference plus an optional version id."""

    bucket: str
    key: str
    version_id: str | None = None

    @property
    def uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"

    @classmethod
    def parse(cls, uri: str, version_id: str | None = None) -> "ObjectRef":
        if not uri.startswith("s3://"):
            raise ValueError(f"object ref must be an s3:// uri, got {uri!r}")
        rest = uri[len("s3://") :]
        bucket, _, key = rest.partition("/")
        if not bucket or not key:
            raise ValueError(f"malformed s3 uri: {uri!r}")
        return cls(bucket=bucket, key=key, version_id=version_id)


@dataclass(frozen=True)
class PutResult:
    version_id: str | None
    byte_count: int


@runtime_checkable
class ObjectStore(Protocol):
    """The minimal versioned object store the engine needs."""

    def put(self, key: str, data: bytes) -> PutResult: ...

    def open_stream(self, key: str, version_id: str | None = None) -> BinaryIO: ...

    def head(self, key: str, version_id: str | None = None) -> bool: ...

    def delete_all_versions(self, key: str) -> list[str]:
        """Delete every version of ``key``. Returns the deleted version ids."""
        ...

    def list_versions(self, key: str) -> list[str]: ...

    def list_prefix(self, prefix: str) -> list[str]:
        """Return the current (non-deleted) keys under ``prefix``."""
        ...


@dataclass
class _StoredObject:
    versions: dict[str, bytes] = field(default_factory=dict)
    order: list[str] = field(default_factory=list)  # version ids, oldest first
    deleted: bool = False


class InMemoryObjectStore:
    """A versioned, single-bucket object store held entirely in memory.

    Deterministic, fast, and enough to exercise the real capture / verify / restore /
    delete pipeline byte-for-byte. Version ids are monotonically assigned.
    """

    def __init__(self, bucket: str = "test-profile-bucket") -> None:
        self.bucket = bucket
        self._objects: dict[str, _StoredObject] = {}
        self._counter = 0

    # -- helpers -------------------------------------------------------------
    def uri(self, key: str) -> str:
        return f"s3://{self.bucket}/{key}"

    def _next_version(self) -> str:
        self._counter += 1
        return f"v{self._counter:08d}"

    # -- protocol ------------------------------------------------------------
    def put(self, key: str, data: bytes) -> PutResult:
        obj = self._objects.setdefault(key, _StoredObject())
        vid = self._next_version()
        obj.versions[vid] = bytes(data)
        obj.order.append(vid)
        obj.deleted = False
        return PutResult(version_id=vid, byte_count=len(data))

    def _resolve(self, key: str, version_id: str | None) -> bytes:
        obj = self._objects.get(key)
        if obj is None or obj.deleted:
            raise KeyError(key)
        if version_id is not None:
            if version_id not in obj.versions:
                raise KeyError(f"{key}@{version_id}")
            return obj.versions[version_id]
        if not obj.order:
            raise KeyError(key)
        return obj.versions[obj.order[-1]]

    def open_stream(self, key: str, version_id: str | None = None) -> BinaryIO:
        return io.BytesIO(self._resolve(key, version_id))

    def get_bytes(self, key: str, version_id: str | None = None) -> bytes:
        return self._resolve(key, version_id)

    def head(self, key: str, version_id: str | None = None) -> bool:
        try:
            self._resolve(key, version_id)
            return True
        except KeyError:
            return False

    def delete_all_versions(self, key: str) -> list[str]:
        obj = self._objects.get(key)
        if obj is None:
            return []
        deleted = list(obj.order)
        obj.versions.clear()
        obj.order.clear()
        obj.deleted = True
        return deleted

    def list_versions(self, key: str) -> list[str]:
        obj = self._objects.get(key)
        if obj is None or obj.deleted:
            return []
        return list(obj.order)

    def list_prefix(self, prefix: str) -> list[str]:
        return sorted(
            k
            for k, obj in self._objects.items()
            if k.startswith(prefix) and not obj.deleted and obj.order
        )

    # -- test corruption helpers (never used in production) ------------------
    def _tamper_byte(self, key: str, index: int) -> None:
        obj = self._objects[key]
        vid = obj.order[-1]
        data = bytearray(obj.versions[vid])
        data[index] ^= 0xFF
        obj.versions[vid] = bytes(data)

    def _truncate(self, key: str, keep: int) -> None:
        obj = self._objects[key]
        vid = obj.order[-1]
        obj.versions[vid] = obj.versions[vid][:keep]


def iter_stream(stream: BinaryIO, chunk: int) -> Iterator[bytes]:
    while True:
        block = stream.read(chunk)
        if not block:
            break
        yield block
