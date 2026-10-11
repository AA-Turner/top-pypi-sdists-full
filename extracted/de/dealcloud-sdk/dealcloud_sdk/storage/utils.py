"""
Storage protocols and fsspec-backed implementations.

All file writes use fsspec so local paths and cloud URIs share one code path.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, BinaryIO, Iterator, Protocol, Union, runtime_checkable

import fsspec


@runtime_checkable
class StorageBackend(Protocol):
    """Buffer-then-write storage (e.g. attachment exports with full bytes in memory)."""

    def write(self, path: str, content: bytes, content_type: str) -> str:
        """Write content to storage; returns full path or URL."""
        ...  # pragma: no cover

    def exists(self, path: str) -> bool:
        ...  # pragma: no cover


@runtime_checkable
class StreamingStorageBackend(Protocol):
    """Long-lived binary write for streaming downloads (e.g. site backups)."""

    def open_write(self, path: str, *, content_type: str) -> Any:
        """Return a context manager yielding a writable binary file-like object."""
        ...  # pragma: no cover


class LocalStorage:
    """Local filesystem storage using fsspec (file:// semantics)."""

    def __init__(self, base_dir: Union[str, Path]) -> None:
        self._root = str(Path(base_dir).resolve())
        fs = fsspec.filesystem("file")
        fs.makedirs(self._root, exist_ok=True)

    def _abspath(self, path: str) -> str:
        return str(Path(self._root) / path)

    def write(self, path: str, content: bytes, content_type: str) -> str:
        full = self._abspath(path)
        fs = fsspec.filesystem("file")
        parent = str(Path(full).parent)
        fs.makedirs(parent, exist_ok=True)
        with fsspec.open(full, "wb") as f:
            f.write(content)
        return full

    def exists(self, path: str) -> bool:
        fs = fsspec.filesystem("file")
        return bool(fs.exists(self._abspath(path)))

    def full_path(self, path: str) -> str:
        """Absolute local path for a relative key."""
        return self._abspath(path)

    @contextmanager
    def open_write(self, path: str, *, content_type: str) -> Iterator[BinaryIO]:
        full = self._abspath(path)
        fs = fsspec.filesystem("file")
        fs.makedirs(str(Path(full).parent), exist_ok=True)
        with fsspec.open(full, "wb") as f:
            yield f  # type: ignore[misc]


class FsspecStreamingStorage:
    """
    Streaming storage rooted at a URI (``file://``, ``s3://``, ``abfs://``, ``gs://``, …).

    Install optional backends: ``s3fs`` (S3), ``adlfs`` (Azure), ``gcsfs`` (GCS).
    """

    def __init__(self, base_uri: str, **storage_options: Any) -> None:
        self._base = base_uri.rstrip("/")
        self._storage_options = storage_options

    def _full_uri(self, path: str) -> str:
        rel = path.lstrip("/")
        return f"{self._base}/{rel}"

    def full_path(self, path: str) -> str:
        """Resolved URI for a relative key."""
        return self._full_uri(path)

    @contextmanager
    def open_write(self, path: str, *, content_type: str) -> Iterator[BinaryIO]:
        full = self._full_uri(path)
        opts = dict(self._storage_options)
        with fsspec.open(full, "wb", **opts) as f:
            yield f  # type: ignore[misc]
