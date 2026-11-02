from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ephemeral_objects import EphemeralObjectPolicy


@dataclass(frozen=True, slots=True)
class ObjectInfo:
    """One stored object, with the metadata a reconciler needs.

    ``path`` is the backend-native ``bucket/key`` (the same shape
    ``list_files`` returns), so it can be compared directly against a
    ``storage_uri``'s parsed path.

    ``last_modified`` is the load-bearing field: any sweep that DELETES
    unreferenced objects MUST honor an age floor, because the write path
    PUTs bytes to storage BEFORE the DB row is inserted (and presigned/TUS
    uploads leave an object before finalize). A freshly-written object with
    no row yet is an in-flight upload, not an orphan. Backends that cannot
    report it return ``None`` — a destructive caller must then refuse to act.
    """

    path: str
    size: int | None = None
    last_modified: datetime | None = None
    etag: str | None = None


class StorageBackend(ABC):
    """Abstract base for all cloud/remote storage backends.

    Every backend implements both a synchronous and an asynchronous API
    with identical signatures. The sync API is safe to call from scripts
    and tests. The async API must be used inside FastAPI routes and any
    other async context to avoid blocking the event loop.

    S3Backend async methods run the synchronous boto3 calls in a thread-pool
    executor (run_in_executor) — genuinely non-blocking to the event loop,
    the standard pattern for boto3 in async applications.

    Concrete backends may override async methods with native clients.

    ServerBackend async methods use httpx.AsyncClient.
    """

    # ------------------------------------------------------------------
    # Synchronous API
    # ------------------------------------------------------------------

    @abstractmethod
    def is_configured(self) -> bool:
        """Return True if all required credentials/settings are present."""

    @abstractmethod
    def read(self, path: str) -> bytes:
        """Read and return the raw bytes at *path*."""

    @abstractmethod
    def write(self, path: str, content: bytes | str, content_type: str | None = None) -> bool:
        """Write *content* to *path*, overwriting if it already exists.

        ``content_type`` is the authoritative MIME for the object. Backends
        that store HTTP-served bytes (S3) MUST stamp it (and a matching
        ``Content-Disposition``) onto the object so a bare public URL renders
        correctly. When None, the backend derives a definitive type from the
        key's extension — it never leaves a known type as octet-stream.
        """

    @abstractmethod
    def append(self, path: str, content: bytes | str) -> bool:
        """Append *content* to the object at *path*."""

    @abstractmethod
    def delete(self, path: str) -> bool:
        """Delete the object at *path*. Returns True on success."""

    @abstractmethod
    def get_url(
        self,
        path: str,
        expires_in: int = 3600,
        *,
        response_content_disposition: str | None = None,
        response_content_type: str | None = None,
    ) -> str:
        """Return a time-limited or permanent URL for *path*.

        ``response_content_disposition`` and ``response_content_type`` are
        S3-style response-header overrides. Backends that don't support
        them MUST ignore the kwargs (never raise) so the URL is still
        usable — the override is best-effort, not a correctness boundary.
        """

    @abstractmethod
    def list_files(self, prefix: str = "") -> list[str]:
        """Return a list of object keys/paths that start with *prefix*."""

    # ------------------------------------------------------------------
    # Asynchronous API
    # ------------------------------------------------------------------

    @abstractmethod
    async def read_async(self, path: str) -> bytes:
        """Async version of read()."""

    @abstractmethod
    async def write_async(self, path: str, content: bytes | str, content_type: str | None = None) -> bool:
        """Async version of write()."""

    @abstractmethod
    async def append_async(self, path: str, content: bytes | str) -> bool:
        """Async version of append()."""

    @abstractmethod
    async def delete_async(self, path: str) -> bool:
        """Async version of delete()."""

    @abstractmethod
    async def get_url_async(
        self,
        path: str,
        expires_in: int = 3600,
        *,
        response_content_disposition: str | None = None,
        response_content_type: str | None = None,
    ) -> str:
        """Async version of get_url()."""

    @abstractmethod
    async def list_files_async(self, prefix: str = "") -> list[str]:
        """Async version of list_files()."""

    # ------------------------------------------------------------------
    # Row-less ephemeral objects (explicit opt-in; not every backend can
    # provide atomic lifecycle tags, so unsupported backends fail loudly).
    # ------------------------------------------------------------------

    def write_ephemeral(
        self,
        path: str,
        content: bytes | str,
        *,
        policy: EphemeralObjectPolicy,
        content_type: str | None = None,
    ) -> bool:
        """Write row-less scratch with the policy's lifecycle tags atomically."""
        raise NotImplementedError(
            f"{self.__class__.__name__} cannot atomically tag ephemeral writes"
        )

    async def write_ephemeral_async(
        self,
        path: str,
        content: bytes | str,
        *,
        policy: EphemeralObjectPolicy,
        content_type: str | None = None,
    ) -> bool:
        """Async version of :meth:`write_ephemeral`."""
        import asyncio
        from functools import partial

        fn = partial(
            self.write_ephemeral,
            path,
            content,
            policy=policy,
            content_type=content_type,
        )
        return await asyncio.get_running_loop().run_in_executor(None, fn)

    def download_to_path(self, path: str, local_path: str) -> int:
        """Materialize an object at *local_path* and return bytes written.

        The portable fallback buffers through :meth:`read`. Backends with a
        native streaming download API should override this method so large
        objects never need to coexist in process memory (S3 does).
        """
        content = self.read(path)
        Path(local_path).write_bytes(content)
        return len(content)

    async def download_to_path_async(self, path: str, local_path: str) -> int:
        """Async version of :meth:`download_to_path`."""
        import asyncio

        return await asyncio.to_thread(self.download_to_path, path, local_path)

    # ------------------------------------------------------------------
    # Listing WITH metadata (not abstract — a backend that can't report
    # metadata inherits the degraded default below rather than breaking).
    # ------------------------------------------------------------------

    def list_objects(self, prefix: str = "") -> list[ObjectInfo]:
        """List objects under *prefix* with size/last-modified metadata.

        The default degrades to :meth:`list_files` with ``last_modified=None``.
        A caller that DELETES based on this list MUST treat a ``None``
        ``last_modified`` as "unknown age" and refuse to delete — see
        :class:`ObjectInfo`. Override in backends that can do better (S3 does).
        """
        return [ObjectInfo(path=p) for p in self.list_files(prefix)]

    async def list_objects_async(self, prefix: str = "") -> list[ObjectInfo]:
        """Async version of list_objects()."""
        return [ObjectInfo(path=p) for p in await self.list_files_async(prefix)]

    # ------------------------------------------------------------------
    # Batch delete (not abstract — degrades to a per-key loop).
    # ------------------------------------------------------------------

    def delete_many(self, paths: list[str]) -> tuple[int, list[tuple[str, str]]]:
        """Delete many objects. Returns ``(deleted_count, [(path, error), ...])``.

        A per-key error is RETURNED, never raised — one bad key must not abort a
        bulk reclaim. The default loops; S3 overrides with a real batch API.
        """
        deleted = 0
        errors: list[tuple[str, str]] = []
        for p in paths:
            try:
                self.delete(p)
                deleted += 1
            except Exception as e:  # noqa: BLE001 — per-key isolation is the point
                errors.append((p, str(e)))
        return deleted, errors

    async def delete_many_async(self, paths: list[str]) -> tuple[int, list[tuple[str, str]]]:
        """Async version of delete_many()."""
        deleted = 0
        errors: list[tuple[str, str]] = []
        for p in paths:
            try:
                await self.delete_async(p)
                deleted += 1
            except Exception as e:  # noqa: BLE001
                errors.append((p, str(e)))
        return deleted, errors

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _require_configured(self) -> None:
        if not self.is_configured():
            raise RuntimeError(
                f"{self.__class__.__name__} is not configured. "
                "Check that all required environment variables are set."
            )
